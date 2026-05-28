"""Executable payment-clearing operations for the bank_payments_clearing PBC."""

from __future__ import annotations

import hashlib
import json


PBC_KEY = "bank_payments_clearing"
EVENT_TOPIC = "pbc.bank_payments_clearing.events"
OWNED_TABLES = (
    "bank_payments_clearing_payment_instruction",
    "bank_payments_clearing_clearing_batch",
    "bank_payments_clearing_settlement_file",
    "bank_payments_clearing_return_item",
    "bank_payments_clearing_exception_case",
    "bank_payments_clearing_bank_reconciliation",
    "bank_payments_clearing_participant_bank",
    "bank_payments_clearing_appgen_outbox_event",
)
PAYMENT_STATES = (
    "drafted",
    "validated",
    "repair_required",
    "approved",
    "released",
    "batched",
    "cleared",
    "settled",
    "returned",
    "repaired",
    "canceled",
    "reconciled",
    "archived",
)
RAIL_PROFILES = {
    "ach": {
        "message_format": "ach_nacha_like",
        "settlement_basis": "deferred_net",
        "limit": 100000.0,
        "requires_batch": True,
        "cutoff": "17:00",
        "repairable_fields": ("beneficiary_name", "purpose_code"),
    },
    "wire": {
        "message_format": "iso_20022_pacs008",
        "settlement_basis": "gross",
        "limit": 10000000.0,
        "requires_batch": False,
        "cutoff": "16:00",
        "repairable_fields": ("beneficiary_address", "purpose_code"),
    },
    "instant": {
        "message_format": "iso_20022_instant",
        "settlement_basis": "real_time_final",
        "limit": 25000.0,
        "requires_batch": False,
        "cutoff": "24x7",
        "repairable_fields": (),
    },
    "card_settlement": {
        "message_format": "card_settlement_cycle",
        "settlement_basis": "scheme_net",
        "limit": 5000000.0,
        "requires_batch": True,
        "cutoff": "23:00",
        "repairable_fields": ("merchant_batch_reference",),
    },
}
RETURN_REASON_PROFILES = {
    "administrative": {"repair_eligible": True, "deadline_days": 2},
    "insufficient_funds": {"repair_eligible": False, "deadline_days": 2},
    "unauthorized": {"repair_eligible": False, "deadline_days": 60},
    "closed_account": {"repair_eligible": True, "deadline_days": 2},
    "late_return": {"repair_eligible": False, "deadline_days": 0},
}


def empty_operations_state() -> dict:
    return {
        "participant_banks": {},
        "payment_instructions": {},
        "clearing_batches": {},
        "settlement_files": {},
        "acknowledgements": {},
        "return_items": {},
        "exception_cases": {},
        "bank_reconciliations": {},
        "control_assertions": {},
        "outbox": (),
        "idempotency": {},
    }


def register_participant_bank(state: dict, profile: dict) -> dict:
    next_state = _copy(state)
    bank_id = profile["participant_bank_id"]
    stored = {
        **profile,
        "status": profile.get("status", "active"),
        "supported_rails": tuple(profile.get("supported_rails", ())),
        "active_windows": tuple(profile.get("active_windows", ("business_day",))),
        "routing_identifier": profile["routing_identifier"],
        "audit_hash": _digest(profile),
    }
    next_state["participant_banks"][bank_id] = stored
    return {"ok": True, "state": next_state, "participant_bank": stored, "side_effects": ()}


def create_payment_instruction(state: dict, instruction: dict) -> dict:
    next_state = _copy(state)
    instruction_id = instruction["instruction_id"]
    duplicate = _find_duplicate(next_state, instruction)
    validation = validate_payment_instruction(next_state, instruction)
    stored = {
        **instruction,
        "state": "validated" if validation["ok"] and not duplicate else "repair_required",
        "rail_profile": validation.get("rail_profile"),
        "validation_findings": validation["findings"],
        "duplicate_candidates": duplicate,
        "screening_evidence": dict(instruction.get("screening_evidence", {})),
        "audit_hash": _digest(instruction),
        "event_contract": "AppGen-X",
    }
    if duplicate:
        stored["validation_findings"] = (*stored["validation_findings"], "possible_duplicate")
    next_state["payment_instructions"][instruction_id] = stored
    if stored["state"] == "repair_required":
        next_state = _open_exception(
            next_state,
            "validation",
            instruction_id,
            stored["validation_findings"],
            severity="high" if duplicate else "medium",
        )
    next_state = _emit(next_state, "BankPaymentsClearingCreated", {"instruction_id": instruction_id, "state": stored["state"]})
    return {
        "ok": stored["state"] == "validated",
        "state": next_state,
        "instruction": stored,
        "validation": validation,
        "duplicate_candidates": duplicate,
        "side_effects": (),
    }


def validate_payment_instruction(state: dict, instruction: dict) -> dict:
    findings = []
    rail = instruction.get("rail")
    rail_profile = RAIL_PROFILES.get(rail)
    participant = state.get("participant_banks", {}).get(instruction.get("participant_bank_id"))
    if not rail_profile:
        findings.append("unsupported_rail")
    if not participant:
        findings.append("unknown_participant_bank")
    elif participant.get("status") != "active":
        findings.append("participant_bank_inactive")
    elif rail not in participant.get("supported_rails", ()):
        findings.append("participant_bank_does_not_support_rail")
    if float(instruction.get("amount", 0)) <= 0:
        findings.append("amount_must_be_positive")
    if rail_profile and float(instruction.get("amount", 0)) > rail_profile["limit"]:
        findings.append("rail_limit_breach")
    if not str(instruction.get("beneficiary_account", "")).isdigit():
        findings.append("beneficiary_account_format")
    if not instruction.get("originator_authorized"):
        findings.append("originator_not_authorized")
    screening = dict(instruction.get("screening_evidence", {}))
    if screening.get("decision") != "clear":
        findings.append("screening_not_clear")
    if screening.get("freshness") not in {"current", "same_day"}:
        findings.append("screening_stale")
    return {
        "ok": not findings,
        "findings": tuple(findings),
        "rail_profile": rail_profile,
        "participant_bank": participant,
        "side_effects": (),
    }


def release_payment_instruction(state: dict, instruction_id: str, *, maker: str, checker: str, liquidity: dict) -> dict:
    instruction = state["payment_instructions"][instruction_id]
    next_state = _copy(state)
    findings = []
    if instruction["state"] not in {"validated", "approved"}:
        findings.append("instruction_not_validated")
    if maker == checker:
        findings.append("maker_checker_conflict")
    if float(liquidity.get("available", 0)) < float(instruction["amount"]) + float(liquidity.get("buffer", 0)):
        findings.append("liquidity_buffer_breach")
    released = not findings
    updated = {
        **instruction,
        "state": "released" if released else "repair_required",
        "approved_by": checker,
        "released_by": checker if released else None,
        "liquidity_evidence": dict(liquidity),
        "release_findings": tuple(findings),
    }
    next_state["payment_instructions"][instruction_id] = updated
    if released:
        next_state = _emit(next_state, "BankPaymentsClearingApproved", {"instruction_id": instruction_id, "state": "released"})
    else:
        next_state = _open_exception(next_state, "release", instruction_id, findings, severity="high")
    return {"ok": released, "state": next_state, "instruction": updated, "findings": tuple(findings), "side_effects": ()}


def assemble_clearing_batch(state: dict, batch_id: str, *, rail: str, participant_bank_id: str, cutoff_context: dict) -> dict:
    next_state = _copy(state)
    if batch_id in next_state["clearing_batches"]:
        return {"ok": True, "duplicate": True, "state": next_state, "batch": next_state["clearing_batches"][batch_id], "side_effects": ()}
    candidates = tuple(
        item
        for item in next_state["payment_instructions"].values()
        if item["state"] == "released"
        and item["rail"] == rail
        and item["participant_bank_id"] == participant_bank_id
        and not item.get("batch_id")
    )
    total = round(sum(float(item["amount"]) for item in candidates), 2)
    hash_total = _digest(tuple((item["instruction_id"], item["amount"], item["currency"]) for item in candidates))
    missed_cutoff = cutoff_context.get("missed_cutoff") is True
    batch = {
        "batch_id": batch_id,
        "rail": rail,
        "participant_bank_id": participant_bank_id,
        "state": "held_for_next_window" if missed_cutoff else "finalized",
        "item_count": len(candidates),
        "total_amount": total,
        "hash_total": hash_total,
        "cutoff_context": dict(cutoff_context),
        "finalization_lock": not missed_cutoff,
        "instruction_ids": tuple(item["instruction_id"] for item in candidates),
    }
    next_state["clearing_batches"][batch_id] = batch
    for instruction_id in batch["instruction_ids"]:
        next_state["payment_instructions"][instruction_id] = {
            **next_state["payment_instructions"][instruction_id],
            "state": "batched" if batch["finalization_lock"] else "released",
            "batch_id": batch_id if batch["finalization_lock"] else None,
        }
    next_state = _emit(next_state, "BankPaymentsClearingUpdated", {"batch_id": batch_id, "item_count": len(candidates)})
    return {"ok": bool(candidates) and not missed_cutoff, "duplicate": False, "state": next_state, "batch": batch, "side_effects": ()}


def generate_settlement_file(state: dict, file_id: str, batch_id: str, *, sequence: int, channel: str) -> dict:
    batch = state["clearing_batches"][batch_id]
    next_state = _copy(state)
    content = {
        "file_id": file_id,
        "batch_id": batch_id,
        "sequence": sequence,
        "rail": batch["rail"],
        "item_count": batch["item_count"],
        "control_total": batch["total_amount"],
        "item_hash": batch["hash_total"],
    }
    file_hash = _digest(content)
    settlement_file = {
        **content,
        "channel": channel,
        "state": "generated",
        "checksum": file_hash,
        "signature": "appgen_payment_file_sig_" + file_hash[:20],
        "transmission_status": "ready",
    }
    next_state["settlement_files"][file_id] = settlement_file
    return {"ok": True, "state": next_state, "settlement_file": settlement_file, "side_effects": ()}


def handle_settlement_acknowledgement(state: dict, acknowledgement: dict) -> dict:
    next_state = _copy(state)
    ack_id = acknowledgement["acknowledgement_id"]
    if ack_id in next_state["acknowledgements"]:
        return {"ok": True, "duplicate": True, "state": next_state, "acknowledgement": next_state["acknowledgements"][ack_id], "side_effects": ()}
    file_record = next_state["settlement_files"][acknowledgement["file_id"]]
    accepted = int(acknowledgement.get("accepted_count", 0))
    rejected = int(acknowledgement.get("rejected_count", 0))
    ack_type = "accepted" if accepted == file_record["item_count"] and rejected == 0 else "partial" if accepted else "rejected"
    stored = {**acknowledgement, "ack_type": ack_type, "state": "processed"}
    next_state["acknowledgements"][ack_id] = stored
    next_state["settlement_files"][file_record["file_id"]] = {
        **file_record,
        "transmission_status": ack_type,
        "accepted_count": accepted,
        "rejected_count": rejected,
    }
    if rejected:
        next_state = _open_exception(next_state, "acknowledgement", file_record["file_id"], ("settlement_rejections",), severity="high")
    return {"ok": rejected == 0, "duplicate": False, "state": next_state, "acknowledgement": stored, "side_effects": ()}


def process_return_item(state: dict, return_item: dict) -> dict:
    next_state = _copy(state)
    profile = RETURN_REASON_PROFILES.get(return_item.get("reason_code"), {"repair_eligible": False, "deadline_days": 0})
    original = next_state["payment_instructions"][return_item["instruction_id"]]
    stored = {
        **return_item,
        "repair_eligible": profile["repair_eligible"],
        "return_deadline_days": profile["deadline_days"],
        "financial_impact": float(original["amount"]),
        "state": "representment_ready" if profile["repair_eligible"] else "reversal_required",
        "notification_required": True,
    }
    next_state["return_items"][return_item["return_id"]] = stored
    next_state["payment_instructions"][original["instruction_id"]] = {**original, "state": "returned"}
    next_state = _emit(next_state, "BankPaymentsClearingExceptionOpened", {"return_id": return_item["return_id"], "reason": return_item.get("reason_code")})
    return {"ok": True, "state": next_state, "return_item": stored, "side_effects": ()}


def reconcile_bank_statement(state: dict, reconciliation_id: str, statement_lines: tuple[dict, ...]) -> dict:
    next_state = _copy(state)
    by_reference = {
        item.get("external_reference"): item
        for item in next_state["payment_instructions"].values()
        if item.get("external_reference")
    }
    matches = []
    exceptions = []
    fees = []
    for line in statement_lines:
        if line.get("line_type") == "fee":
            fees.append(line)
            continue
        instruction = by_reference.get(line.get("external_reference"))
        if not instruction:
            exceptions.append({"line": line, "reason": "unmatched_statement_line"})
            continue
        amount_delta = abs(float(line.get("amount", 0)) - float(instruction["amount"]))
        match_type = "one_to_one" if amount_delta <= 0.01 else "amount_variance"
        matches.append({"instruction_id": instruction["instruction_id"], "match_type": match_type, "amount_delta": round(amount_delta, 2)})
        if match_type != "one_to_one":
            exceptions.append({"line": line, "instruction_id": instruction["instruction_id"], "reason": match_type})
    record = {
        "reconciliation_id": reconciliation_id,
        "match_count": len(matches),
        "fee_count": len(fees),
        "exception_count": len(exceptions),
        "matches": tuple(matches),
        "fees": tuple(fees),
        "exceptions": tuple(exceptions),
        "state": "reconciled" if not exceptions else "breaks_open",
    }
    next_state["bank_reconciliations"][reconciliation_id] = record
    for match in matches:
        if match["match_type"] == "one_to_one":
            instruction = next_state["payment_instructions"][match["instruction_id"]]
            next_state["payment_instructions"][match["instruction_id"]] = {**instruction, "state": "reconciled"}
    return {"ok": not exceptions, "state": next_state, "reconciliation": record, "side_effects": ()}


def build_payment_operations_workbench(state: dict) -> dict:
    instructions = tuple(state.get("payment_instructions", {}).values())
    exceptions = tuple(state.get("exception_cases", {}).values())
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}/payments",
        "cards": (
            {"key": "instructions", "value": len(instructions)},
            {"key": "released", "value": len(tuple(item for item in instructions if item["state"] == "released"))},
            {"key": "batches", "value": len(state.get("clearing_batches", {}))},
            {"key": "settlement_files", "value": len(state.get("settlement_files", {}))},
            {"key": "returns", "value": len(state.get("return_items", {}))},
            {"key": "open_exceptions", "value": len(tuple(item for item in exceptions if item["state"] == "open"))},
        ),
        "queues": {
            "repair": tuple(item["instruction_id"] for item in instructions if item["state"] == "repair_required"),
            "returns": tuple(state.get("return_items", {})),
            "reconciliation_breaks": tuple(
                key
                for key, record in state.get("bank_reconciliations", {}).items()
                if record["state"] == "breaks_open"
            ),
        },
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_payment_operations_release_evidence() -> dict:
    state = empty_operations_state()
    state = register_participant_bank(
        state,
        {
            "participant_bank_id": "bank_a",
            "routing_identifier": "021000021",
            "supported_rails": ("ach", "wire"),
            "status": "active",
        },
    )["state"]
    instruction = create_payment_instruction(
        state,
        {
            "instruction_id": "pay_1",
            "tenant": "tenant_a",
            "rail": "ach",
            "participant_bank_id": "bank_a",
            "amount": 1250.0,
            "currency": "USD",
            "beneficiary_account": "123456789",
            "beneficiary_name": "Supplier One",
            "originator_authorized": True,
            "external_reference": "EXT-1",
            "screening_evidence": {"decision": "clear", "freshness": "current"},
        },
    )
    state = instruction["state"]
    state = release_payment_instruction(state, "pay_1", maker="maker", checker="checker", liquidity={"available": 5000, "buffer": 500})["state"]
    batch = assemble_clearing_batch(state, "batch_1", rail="ach", participant_bank_id="bank_a", cutoff_context={"missed_cutoff": False})
    state = batch["state"]
    file_result = generate_settlement_file(state, "file_1", "batch_1", sequence=1, channel="host_to_host")
    state = file_result["state"]
    ack = handle_settlement_acknowledgement(state, {"acknowledgement_id": "ack_1", "file_id": "file_1", "accepted_count": 1, "rejected_count": 0})
    state = ack["state"]
    reconciliation = reconcile_bank_statement(state, "recon_1", ({"external_reference": "EXT-1", "amount": 1250.0},))
    workbench = build_payment_operations_workbench(reconciliation["state"])
    checks = (
        {"id": "participant_bank_registry", "ok": "bank_a" in state["participant_banks"]},
        {"id": "instruction_validation", "ok": instruction["ok"] and instruction["instruction"]["state"] == "validated"},
        {"id": "maker_checker_release", "ok": batch["ok"]},
        {"id": "settlement_file_integrity", "ok": file_result["settlement_file"]["signature"].startswith("appgen_payment_file_sig_")},
        {"id": "acknowledgement_handling", "ok": ack["ok"] and ack["acknowledgement"]["ack_type"] == "accepted"},
        {"id": "reconciliation", "ok": reconciliation["ok"]},
        {"id": "workbench", "ok": workbench["ok"]},
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "workbench": workbench,
        "event_contract": "AppGen-X",
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def _open_exception(state: dict, exception_type: str, object_id: str, findings: tuple[str, ...] | list[str], *, severity: str) -> dict:
    exception_id = f"exception_{len(state['exception_cases']) + 1}"
    state["exception_cases"][exception_id] = {
        "exception_id": exception_id,
        "exception_type": exception_type,
        "object_id": object_id,
        "findings": tuple(findings),
        "severity": severity,
        "owner_queue": f"{exception_type}_operations",
        "state": "open",
        "closure_requires_evidence": True,
    }
    return _emit(state, "BankPaymentsClearingExceptionOpened", {"exception_id": exception_id, "object_id": object_id})


def _find_duplicate(state: dict, instruction: dict) -> tuple[dict, ...]:
    candidates = []
    for existing in state.get("payment_instructions", {}).values():
        same_facts = (
            existing.get("participant_bank_id") == instruction.get("participant_bank_id")
            and existing.get("beneficiary_account") == instruction.get("beneficiary_account")
            and existing.get("amount") == instruction.get("amount")
            and existing.get("currency") == instruction.get("currency")
            and existing.get("external_reference") == instruction.get("external_reference")
        )
        if same_facts:
            candidates.append({"instruction_id": existing["instruction_id"], "reason": "same_bank_beneficiary_amount_reference"})
    return tuple(candidates)


def _emit(state: dict, event_type: str, payload: dict) -> dict:
    event = {
        "event_id": f"{PBC_KEY}_evt_{len(state['outbox']) + 1:06d}",
        "event_type": event_type,
        "topic": EVENT_TOPIC,
        "contract": "AppGen-X",
        "payload": dict(payload),
        "idempotency_key": _digest((event_type, payload)),
    }
    state["outbox"] = (*state.get("outbox", ()), event)
    return state


def _copy(state: dict) -> dict:
    return {
        "participant_banks": {key: dict(value) for key, value in state.get("participant_banks", {}).items()},
        "payment_instructions": {key: dict(value) for key, value in state.get("payment_instructions", {}).items()},
        "clearing_batches": {key: dict(value) for key, value in state.get("clearing_batches", {}).items()},
        "settlement_files": {key: dict(value) for key, value in state.get("settlement_files", {}).items()},
        "acknowledgements": {key: dict(value) for key, value in state.get("acknowledgements", {}).items()},
        "return_items": {key: dict(value) for key, value in state.get("return_items", {}).items()},
        "exception_cases": {key: dict(value) for key, value in state.get("exception_cases", {}).items()},
        "bank_reconciliations": {key: dict(value) for key, value in state.get("bank_reconciliations", {}).items()},
        "control_assertions": {key: dict(value) for key, value in state.get("control_assertions", {}).items()},
        "outbox": tuple(state.get("outbox", ())),
        "idempotency": dict(state.get("idempotency", {})),
    }


def _digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
