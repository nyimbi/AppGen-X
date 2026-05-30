"""Executable runtime contract for the gaming_casino_operations PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from typing import Any
from uuid import uuid4

from . import config
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_OPERATIONS,
    DOMAIN_WORKFLOWS,
    domain_depth_contract,
    domain_depth_smoke_test,
    execute_domain_operation as build_domain_operation_plan,
)
from .events import CONSUMED, EMITTED, REQUIRED_TOPIC, build_event_envelope, event_contract_manifest
from .handlers import dispatch_event as dispatch_consumed_event
from .models import (
    BUSINESS_TABLES,
    CONTROL_ASSERTION_TABLE,
    DEAD_LETTER_EVENT_TABLE,
    EVENT_TABLES,
    GAMING_COMPLIANCE_TABLE,
    GOVERNED_MODEL_TABLE,
    INBOX_EVENT_TABLE,
    OUTBOX_EVENT_TABLE,
    OWNED_TABLES,
    PAYOUT_TABLE,
    PLAYER_PROFILE_TABLE,
    POLICY_RULE_TABLE,
    RESPONSIBLE_GAMING_CASE_TABLE,
    RUNTIME_PARAMETER_TABLE,
    SCHEMA_EXTENSION_TABLE,
    SLOT_MACHINE_TABLE,
    TABLE_DEFINITIONS,
    TABLE_GAME_TABLE,
    WAGER_SESSION_TABLE,
    create_model_record,
    model_alignment_smoke_test,
    model_contracts,
)


PBC_KEY = "gaming_casino_operations"
GAMING_CASINO_OPERATIONS_OWNED_TABLES = OWNED_TABLES
GAMING_CASINO_OPERATIONS_RUNTIME_TABLES = OWNED_TABLES
GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC = REQUIRED_TOPIC
GAMING_CASINO_OPERATIONS_EMITTED_EVENT_TYPES = EMITTED
GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES = CONSUMED
GAMING_CASINO_OPERATIONS_STANDARD_FEATURE_KEYS = (
    "player_profile_management",
    "gaming_casino_operations_workflow",
    "gaming_casino_operations_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
GAMING_CASINO_OPERATIONS_RUNTIME_CAPABILITY_KEYS = tuple(
    capability.replace(" ", "_") for capability in DOMAIN_ADVANCED_CAPABILITIES
)
GAMING_CASINO_OPERATIONS_UI_FRAGMENT_KEYS = (
    "GamingCasinoOperationsWorkbench",
    "GamingCasinoOperationsDetail",
    "GamingCasinoOperationsAssistantPanel",
)
GAMING_CASINO_OPERATIONS_BUSINESS_TABLES = BUSINESS_TABLES
GAMING_CASINO_OPERATIONS_WORKFLOW_KEYS = DOMAIN_WORKFLOWS

_STATE_BUCKETS = {
    PLAYER_PROFILE_TABLE: "player_profiles",
    TABLE_GAME_TABLE: "table_games",
    SLOT_MACHINE_TABLE: "slot_machines",
    WAGER_SESSION_TABLE: "wager_sessions",
    PAYOUT_TABLE: "payouts",
    RESPONSIBLE_GAMING_CASE_TABLE: "responsible_gaming_cases",
    GAMING_COMPLIANCE_TABLE: "gaming_compliance_cases",
    POLICY_RULE_TABLE: "policy_rules",
    RUNTIME_PARAMETER_TABLE: "runtime_parameters",
    SCHEMA_EXTENSION_TABLE: "schema_extensions",
    CONTROL_ASSERTION_TABLE: "control_assertions",
    GOVERNED_MODEL_TABLE: "governed_models",
}


def gaming_casino_operations_empty_state() -> dict[str, Any]:
    return {
        "configuration": dict(config.DEFAULT_CONFIGURATION),
        "parameters": {
            name: {
                "name": name,
                "value": spec["default"],
                "scope": "domain",
                "status": "active",
            }
            for name, spec in config.PARAMETER_SPECS.items()
        },
        "rules": {
            rule["rule_id"]: {
                **dict(rule),
                "compiled_hash": config.compile_rule(rule)["compiled_hash"],
            }
            for rule in config.DEFAULT_RULES
        },
        "player_profiles": {},
        "table_games": {},
        "slot_machines": {},
        "wager_sessions": {},
        "payouts": {},
        "responsible_gaming_cases": {},
        "gaming_compliance_cases": {},
        "policy_rules": {},
        "runtime_parameters": {},
        "schema_extensions": {},
        "control_assertions": {},
        "governed_models": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "event_history": [],
        "workflow_runs": [],
        "document_intakes": [],
        "audit_log": [],
        "idempotency_keys": set(),
    }


def _copy(state: dict[str, Any]) -> dict[str, Any]:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _timestamp(state: dict[str, Any]) -> str:
    ordinal = (
        len(state.get("event_history", []))
        + len(state.get("audit_log", []))
        + len(state.get("outbox", []))
        + len(state.get("inbox", []))
        + len(state.get("dead_letter", []))
        + 1
    )
    minute, second = divmod(ordinal, 60)
    return f"2026-05-30T00:{minute:02d}:{second:02d}Z"


def _sequence_id(prefix: str, bucket: dict[str, Any] | list[Any]) -> str:
    return f"{prefix}_{len(bucket) + 1:04d}"


def _parameter_value(state: dict[str, Any], name: str) -> Any:
    item = state.get("parameters", {}).get(name)
    if item:
        return item["value"]
    return config.PARAMETER_SPECS[name]["default"]


def _store_record(state: dict[str, Any], table: str, record: dict[str, Any]) -> None:
    bucket_name = _STATE_BUCKETS[table]
    state[bucket_name][record["id"]] = record


def _record_audit(
    state: dict[str, Any],
    *,
    action: str,
    subject_table: str,
    subject_id: str,
    details: dict[str, Any],
) -> None:
    state["audit_log"].append(
        {
            "audit_id": _sequence_id("audit", state["audit_log"]),
            "action": action,
            "subject_table": subject_table,
            "subject_id": subject_id,
            "details": deepcopy(details),
            "recorded_at": _timestamp(state),
        }
    )


def _record_workflow(
    state: dict[str, Any],
    *,
    workflow: str,
    status: str,
    payload: dict[str, Any],
    outputs: dict[str, Any] | None = None,
) -> None:
    state["workflow_runs"].append(
        {
            "workflow_run_id": _sequence_id("workflow", state["workflow_runs"]),
            "workflow": workflow,
            "status": status,
            "payload": deepcopy(payload),
            "outputs": deepcopy(outputs or {}),
            "recorded_at": _timestamp(state),
        }
    )


def _event_record(table: str, envelope: dict[str, Any], status: str) -> dict[str, Any]:
    timestamp = envelope["payload"].get("recorded_at", "2026-05-30T00:00:00Z")
    model = create_model_record(
        table,
        {
            "id": envelope["event_id"],
            "tenant": envelope.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "event_type": envelope["event_type"],
            "aggregate_table": envelope.get("aggregate_table"),
            "aggregate_id": envelope.get("aggregate_id"),
            "topic": envelope["topic"],
            "event_status": status,
            "payload": envelope,
        },
    )
    return model["record"]


def _emit_event(
    state: dict[str, Any],
    event_type: str,
    *,
    payload: dict[str, Any],
    aggregate_table: str,
    aggregate_id: str,
) -> dict[str, Any]:
    event_payload = dict(payload)
    event_payload.setdefault("aggregate_table", aggregate_table)
    event_payload.setdefault("aggregate_id", aggregate_id)
    event_payload.setdefault("tenant", payload.get("tenant", "default"))
    event_payload.setdefault("recorded_at", _timestamp(state))
    envelope = build_event_envelope(event_type, event_payload)
    record = _event_record(OUTBOX_EVENT_TABLE, envelope, "pending")
    state["outbox"].append(record)
    state["event_history"].append(
        {
            "event_type": event_type,
            "aggregate_table": aggregate_table,
            "aggregate_id": aggregate_id,
            "payload": deepcopy(event_payload),
            "direction": "outbound",
            "topic": REQUIRED_TOPIC,
        }
    )
    return record


def _find_player_duplicates(state: dict[str, Any], payload: dict[str, Any]) -> tuple[str, ...]:
    government_id = payload.get("government_id")
    legal_name = payload.get("legal_name")
    date_of_birth = payload.get("date_of_birth")
    tenant = payload.get("tenant", "default")
    matches = []
    for record in state.get("player_profiles", {}).values():
        existing_payload = record.get("payload", {})
        if record.get("tenant") != tenant:
            continue
        same_identity = bool(government_id) and existing_payload.get("government_id") == government_id
        same_demographics = record.get("legal_name") == legal_name and record.get("date_of_birth") == date_of_birth
        if same_identity or same_demographics:
            matches.append(record["id"])
    return tuple(matches)


def _asset_lookup(state: dict[str, Any], asset_kind: str, asset_id: str) -> dict[str, Any] | None:
    if asset_kind == "table":
        return state.get("table_games", {}).get(asset_id)
    if asset_kind == "slot":
        return state.get("slot_machines", {}).get(asset_id)
    return None


def _asset_operational(asset_kind: str, record: dict[str, Any] | None) -> bool:
    if not record:
        return False
    if asset_kind == "table":
        return record.get("table_status") == "open"
    if asset_kind == "slot":
        return record.get("operational_state") == "active"
    return False


def gaming_casino_operations_register_defaults(state: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    next_state["configuration"] = dict(config.DEFAULT_CONFIGURATION)
    for name, spec in config.PARAMETER_SPECS.items():
        next_state["parameters"][name] = {
            "name": name,
            "value": spec["default"],
            "scope": "domain",
            "status": "active",
        }
    for rule in config.DEFAULT_RULES:
        next_state["rules"][rule["rule_id"]] = {
            **dict(rule),
            "compiled_hash": config.compile_rule(rule)["compiled_hash"],
        }
    return {
        "ok": True,
        "state": next_state,
        "configuration": next_state["configuration"],
        "parameters": next_state["parameters"],
        "rules": next_state["rules"],
        "side_effects": (),
    }


def gaming_casino_operations_configure_runtime(state: dict[str, Any], config_payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    validation = config.validate_configuration(config_payload)
    next_state["configuration"] = validation["configuration"]
    return {
        "ok": validation["ok"],
        "state": next_state,
        "configuration": next_state["configuration"],
        "validation": validation,
        "side_effects": (),
    }


def gaming_casino_operations_set_parameter(state: dict[str, Any], name: str, value: Any) -> dict[str, Any]:
    next_state = _copy(state)
    parameter_check = config.set_parameter(name, value)
    if parameter_check["ok"] is not True:
        return {**parameter_check, "state": next_state}
    timestamp = _timestamp(next_state)
    artifact_id = f"param-{name}"
    model = create_model_record(
        RUNTIME_PARAMETER_TABLE,
        {
            "id": artifact_id,
            "tenant": next_state["configuration"].get("property_id", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "parameter_name": name,
            "parameter_value": value,
            "scope": "domain",
            "parameter_status": "active",
        },
    )
    record = model["record"]
    next_state["parameters"][name] = {"name": name, "value": value, "scope": "domain", "status": "active"}
    next_state["runtime_parameters"][artifact_id] = record
    _record_audit(next_state, action="set_parameter", subject_table=RUNTIME_PARAMETER_TABLE, subject_id=artifact_id, details=record)
    return {"ok": True, "state": next_state, "parameter": record, "side_effects": ()}


def gaming_casino_operations_register_rule(state: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    compiled = config.compile_rule(rule)
    timestamp = _timestamp(next_state)
    rule_id = rule.get("rule_id", _sequence_id("rule", next_state["policy_rules"]))
    model = create_model_record(
        POLICY_RULE_TABLE,
        {
            "id": rule_id,
            "tenant": rule.get("tenant", next_state["configuration"].get("property_id", "default")),
            "created_at": timestamp,
            "updated_at": timestamp,
            "rule_id": rule_id,
            "jurisdiction": rule.get("jurisdiction", next_state["configuration"].get("jurisdiction", "NV")),
            "scope": rule.get("scope", "floor"),
            "rule_status": rule.get("status", "active"),
            "version": int(rule.get("version", 1)),
            "effective_from": rule.get("effective_from", timestamp),
            "effective_to": rule.get("effective_to"),
            "payload": {**dict(rule), "compiled_hash": compiled["compiled_hash"]},
        },
    )
    record = model["record"]
    next_state["rules"][rule_id] = {**dict(rule), "compiled_hash": compiled["compiled_hash"]}
    next_state["policy_rules"][rule_id] = record
    _record_audit(next_state, action="register_rule", subject_table=POLICY_RULE_TABLE, subject_id=rule_id, details=record)
    return {"ok": True, "state": next_state, "rule": record, "side_effects": ()}


def gaming_casino_operations_register_schema_extension(state: dict[str, Any], table: str, fields: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in GAMING_CASINO_OPERATIONS_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    timestamp = _timestamp(next_state)
    extension_id = _sequence_id("schema_extension", next_state["schema_extensions"])
    model = create_model_record(
        SCHEMA_EXTENSION_TABLE,
        {
            "id": extension_id,
            "tenant": next_state["configuration"].get("property_id", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "table_name": owned_name,
            "extension_name": f"{owned_name}.custom_fields",
            "extension_status": "proposed",
            "fields_json": deepcopy(fields),
        },
    )
    record = model["record"]
    next_state["schema_extensions"][extension_id] = record
    _record_audit(next_state, action="register_schema_extension", subject_table=SCHEMA_EXTENSION_TABLE, subject_id=extension_id, details=record)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": deepcopy(fields), "record": record, "side_effects": ()}


def gaming_casino_operations_receive_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    envelope = build_event_envelope(event.get("event_type", "UnexpectedEvent"), event)
    idem = envelope["idempotency_key"]
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    handler = dispatch_consumed_event(envelope)
    if handler.get("duplicate") is True:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    if handler["ok"] is not True:
        record = _event_record(DEAD_LETTER_EVENT_TABLE, envelope, "dead_letter")
        next_state["dead_letter"].append(record)
        next_state["event_history"].append(
            {
                "event_type": envelope["event_type"],
                "aggregate_table": envelope.get("aggregate_table"),
                "aggregate_id": envelope.get("aggregate_id"),
                "payload": deepcopy(envelope),
                "direction": "dead_letter",
                "topic": REQUIRED_TOPIC,
            }
        )
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": DEAD_LETTER_EVENT_TABLE,
            "side_effects": (),
        }
    record = _event_record(INBOX_EVENT_TABLE, envelope, "received")
    next_state["inbox"].append(record)
    next_state["event_history"].append(
        {
            "event_type": envelope["event_type"],
            "aggregate_table": envelope.get("aggregate_table"),
            "aggregate_id": envelope.get("aggregate_id"),
            "payload": deepcopy(envelope),
            "direction": "inbound",
            "topic": REQUIRED_TOPIC,
        }
    )
    _record_workflow(
        next_state,
        workflow=f"{PBC_KEY}_event_reaction",
        status="pending_review",
        payload=envelope,
        outputs={"reaction": handler["reaction"], "review_task": handler["review_task"]},
    )
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "reaction": handler["reaction"],
        "review_task": handler["review_task"],
        "side_effects": (),
    }


def gaming_casino_operations_create_player_profile(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    record_id = payload.get("id") or payload.get("player_profile_id") or _sequence_id("player", next_state["player_profiles"])
    duplicates = _find_player_duplicates(next_state, payload)
    rule_eval = config.evaluate_rule(
        "player_profile_policy",
        {
            "age_verified": payload.get("age_verified", False),
            "identity_confidence": payload.get("identity_confidence", 0.0),
        },
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    review_reasons = list(rule_eval["reasons"])
    if duplicates:
        review_reasons.append("duplicate_identity_review_required")
    review_required = bool(review_reasons)
    model = create_model_record(
        PLAYER_PROFILE_TABLE,
        {
            "id": record_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "player_number": payload.get("player_number", record_id.upper()),
            "legal_name": payload.get("legal_name", "Unknown Patron"),
            "date_of_birth": payload.get("date_of_birth", "1970-01-01"),
            "loyalty_tier": payload.get("loyalty_tier", "standard"),
            "enrollment_status": "review_pending" if review_required else payload.get("enrollment_status", "active"),
            "identity_confidence": float(payload.get("identity_confidence", 0.0)),
            "age_verified": bool(payload.get("age_verified", False)),
            "restriction_state": payload.get("restriction_state", "clear"),
            "property_id": payload.get("property_id", next_state["configuration"].get("property_id", "property-default")),
            "host_id": payload.get("host_id"),
            "duplicate_review_state": "pending" if duplicates else "not_required",
            "payload": {
                **dict(payload),
                "duplicate_candidates": duplicates,
                "review_reasons": tuple(review_reasons),
            },
        },
    )
    record = model["record"]
    _store_record(next_state, PLAYER_PROFILE_TABLE, record)
    _record_audit(next_state, action="create_player_profile", subject_table=PLAYER_PROFILE_TABLE, subject_id=record_id, details=record)
    _emit_event(next_state, EMITTED[0], payload=record, aggregate_table=PLAYER_PROFILE_TABLE, aggregate_id=record_id)
    if review_required:
        _emit_event(next_state, EMITTED[3], payload={"tenant": record["tenant"], "record": record}, aggregate_table=PLAYER_PROFILE_TABLE, aggregate_id=record_id)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "review_required": review_required,
        "duplicate_candidates": duplicates,
        "side_effects": (),
    }


def gaming_casino_operations_apply_player_restriction(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    record_id = payload.get("player_profile_id")
    existing = next_state["player_profiles"].get(record_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "player_not_found", "side_effects": ()}
    updated = {
        **existing,
        "restriction_state": payload.get("restriction_state", "cooling_off"),
        "updated_at": _timestamp(next_state),
        "payload": {
            **existing.get("payload", {}),
            "restrictions": tuple(payload.get("restrictions", (payload.get("restriction_state", "cooling_off"),))),
            "restriction_applied_by": payload.get("applied_by", "system"),
            "restriction_reason": payload.get("reason", "policy_intervention"),
            "effective_until": payload.get("effective_until"),
        },
    }
    next_state["player_profiles"][record_id] = updated
    _record_audit(next_state, action="apply_player_restriction", subject_table=PLAYER_PROFILE_TABLE, subject_id=record_id, details=updated)
    _emit_event(next_state, EMITTED[1], payload=updated, aggregate_table=PLAYER_PROFILE_TABLE, aggregate_id=record_id)
    _emit_event(next_state, EMITTED[3], payload=updated, aggregate_table=PLAYER_PROFILE_TABLE, aggregate_id=record_id)
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def gaming_casino_operations_open_table(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    table_id = payload.get("id") or payload.get("table_id") or _sequence_id("table", next_state["table_games"])
    opening_bankroll = float(payload.get("opening_bankroll", 0.0))
    model = create_model_record(
        TABLE_GAME_TABLE,
        {
            "id": table_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "table_number": payload.get("table_number", table_id.upper()),
            "pit": payload.get("pit", "main"),
            "game_variant": payload.get("game_variant", "blackjack"),
            "table_status": "open",
            "shift_id": payload.get("shift_id", _sequence_id("shift", next_state["workflow_runs"])),
            "opening_bankroll": opening_bankroll,
            "current_bankroll": opening_bankroll,
            "dealer_id": payload.get("dealer_id", "dealer-unassigned"),
            "supervisor_id": payload.get("supervisor_id", "supervisor-unassigned"),
            "dispute_state": "clear",
            "payload": {
                **dict(payload),
                "inventory_events": (
                    {
                        "event_type": "opening_bankroll",
                        "amount": opening_bankroll,
                        "recorded_at": timestamp,
                    },
                ),
            },
        },
    )
    record = model["record"]
    _store_record(next_state, TABLE_GAME_TABLE, record)
    _record_audit(next_state, action="open_table", subject_table=TABLE_GAME_TABLE, subject_id=table_id, details=record)
    _emit_event(next_state, EMITTED[0], payload=record, aggregate_table=TABLE_GAME_TABLE, aggregate_id=table_id)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def gaming_casino_operations_record_table_inventory_movement(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    table_id = payload.get("table_id")
    existing = next_state["table_games"].get(table_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "table_not_found", "side_effects": ()}
    movement_type = payload.get("movement_type", "fill")
    approvals = tuple(payload.get("approvals", ()))
    requires_dual_control = movement_type in {"fill", "credit", "emergency_adjustment"}
    if requires_dual_control and len(approvals) < 2:
        return {
            "ok": False,
            "state": next_state,
            "reason": "dual_control_evidence_required",
            "side_effects": (),
        }
    amount = float(payload.get("amount", 0.0))
    direction = 1 if movement_type in {"fill", "buy_in", "marker_redemption"} else -1
    inventory_events = tuple(existing.get("payload", {}).get("inventory_events", ())) + (
        {
            "event_type": movement_type,
            "amount": amount,
            "approvals": approvals,
            "recorded_at": _timestamp(next_state),
        },
    )
    updated = {
        **existing,
        "current_bankroll": round(float(existing.get("current_bankroll", 0.0)) + (direction * amount), 2),
        "updated_at": _timestamp(next_state),
        "payload": {**existing.get("payload", {}), "inventory_events": inventory_events},
    }
    next_state["table_games"][table_id] = updated
    _record_audit(next_state, action="record_table_inventory_movement", subject_table=TABLE_GAME_TABLE, subject_id=table_id, details=updated)
    _emit_event(next_state, EMITTED[1], payload=updated, aggregate_table=TABLE_GAME_TABLE, aggregate_id=table_id)
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def gaming_casino_operations_close_table(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    table_id = payload.get("table_id")
    existing = next_state["table_games"].get(table_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "table_not_found", "side_effects": ()}
    closing_bankroll = float(payload.get("closing_bankroll", existing.get("current_bankroll", 0.0)))
    variance = round(closing_bankroll - float(existing.get("current_bankroll", 0.0)), 2)
    rule_eval = config.evaluate_rule(
        "table_inventory_policy",
        {
            "action": "close",
            "supervisor_signed": bool(payload.get("supervisor_signed")),
            "reconciliation_complete": bool(payload.get("reconciliation_complete")),
            "variance": variance,
        },
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    if rule_eval["passed"] is not True:
        return {
            "ok": False,
            "state": next_state,
            "reason": "table_close_rejected",
            "rule_evaluation": rule_eval,
            "variance": variance,
            "side_effects": (),
        }
    updated = {
        **existing,
        "table_status": "closed",
        "current_bankroll": closing_bankroll,
        "updated_at": _timestamp(next_state),
        "payload": {
            **existing.get("payload", {}),
            "closing_bankroll": closing_bankroll,
            "variance": variance,
            "closure_reason": payload.get("closure_reason", "shift_complete"),
            "supervisor_signed": True,
            "reconciliation_complete": True,
        },
    }
    next_state["table_games"][table_id] = updated
    _record_audit(next_state, action="close_table", subject_table=TABLE_GAME_TABLE, subject_id=table_id, details=updated)
    _emit_event(next_state, EMITTED[2], payload=updated, aggregate_table=TABLE_GAME_TABLE, aggregate_id=table_id)
    return {"ok": True, "state": next_state, "record": updated, "variance": variance, "side_effects": ()}


def gaming_casino_operations_register_slot_machine(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    slot_id = payload.get("id") or payload.get("slot_machine_id") or _sequence_id("slot", next_state["slot_machines"])
    action = payload.get("action", "install")
    approvals = tuple(payload.get("approvals", ()))
    existing = next_state["slot_machines"].get(slot_id)
    conversion_history = tuple(existing.get("payload", {}).get("conversion_history", ())) if existing else ()
    if action == "convert":
        conversion_history = conversion_history + (
            {
                "from": payload.get("conversion_from", existing.get("paytable_version") if existing else None),
                "to": payload.get("paytable_version"),
                "approvals": approvals,
                "recorded_at": timestamp,
            },
        )
    rule_eval = config.evaluate_rule(
        "slot_machine_policy",
        {
            "action": action,
            "has_meter_snapshot": bool(payload.get("meter_snapshot")) or action == "install",
            "has_approval": bool(approvals) or action == "install",
        },
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    review_required = action == "convert" and rule_eval["passed"] is not True
    model = create_model_record(
        SLOT_MACHINE_TABLE,
        {
            "id": slot_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": existing.get("created_at", timestamp) if existing else timestamp,
            "updated_at": timestamp,
            "asset_code": payload.get("asset_code", slot_id.upper()),
            "bank_location": payload.get("bank_location", existing.get("bank_location") if existing else "bank-01"),
            "denomination": float(payload.get("denomination", existing.get("denomination", 1.0) if existing else 1.0)),
            "paytable_version": payload.get("paytable_version", existing.get("paytable_version") if existing else "base-v1"),
            "progressive_link": payload.get("progressive_link", existing.get("progressive_link") if existing else None),
            "operational_state": "approval_pending" if review_required else payload.get("operational_state", existing.get("operational_state") if existing else "active"),
            "fault_state": payload.get("fault_state", existing.get("fault_state") if existing else "clear"),
            "jurisdiction_approval_state": "pending" if review_required else payload.get("jurisdiction_approval_state", existing.get("jurisdiction_approval_state") if existing else "approved"),
            "last_meter_reading": float(payload.get("last_meter_reading", existing.get("last_meter_reading", 0.0) if existing else 0.0)),
            "payload": {
                **(existing.get("payload", {}) if existing else {}),
                **dict(payload),
                "conversion_history": conversion_history,
            },
        },
    )
    record = model["record"]
    next_state["slot_machines"][slot_id] = record
    _record_audit(next_state, action="register_slot_machine", subject_table=SLOT_MACHINE_TABLE, subject_id=slot_id, details=record)
    _emit_event(next_state, EMITTED[1 if existing else 0], payload=record, aggregate_table=SLOT_MACHINE_TABLE, aggregate_id=slot_id)
    if review_required:
        _emit_event(next_state, EMITTED[3], payload=record, aggregate_table=SLOT_MACHINE_TABLE, aggregate_id=slot_id)
    return {"ok": True, "state": next_state, "record": record, "review_required": review_required, "rule_evaluation": rule_eval, "side_effects": ()}


def gaming_casino_operations_recover_slot_fault(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    slot_id = payload.get("slot_machine_id")
    existing = next_state["slot_machines"].get(slot_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "slot_machine_not_found", "side_effects": ()}
    rule_eval = config.evaluate_rule(
        "slot_machine_policy",
        {
            "action": "recover",
            "has_meter_snapshot": bool(payload.get("meter_snapshot")),
            "has_approval": bool(payload.get("recovery_approval")),
        },
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    if rule_eval["passed"] is not True:
        return {
            "ok": False,
            "state": next_state,
            "reason": "slot_recovery_rejected",
            "rule_evaluation": rule_eval,
            "side_effects": (),
        }
    updated = {
        **existing,
        "operational_state": "active",
        "fault_state": "clear",
        "last_meter_reading": float(payload.get("meter_snapshot", existing.get("last_meter_reading", 0.0))),
        "updated_at": _timestamp(next_state),
        "payload": {
            **existing.get("payload", {}),
            "fault_history": tuple(existing.get("payload", {}).get("fault_history", ()))
            + ({"fault_state": payload.get("fault_state", existing.get("fault_state")), "meter_snapshot": payload.get("meter_snapshot"), "recorded_at": _timestamp(next_state)},),
            "recovery_approval": payload.get("recovery_approval"),
        },
    }
    next_state["slot_machines"][slot_id] = updated
    _record_audit(next_state, action="recover_slot_fault", subject_table=SLOT_MACHINE_TABLE, subject_id=slot_id, details=updated)
    _emit_event(next_state, EMITTED[2], payload=updated, aggregate_table=SLOT_MACHINE_TABLE, aggregate_id=slot_id)
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def gaming_casino_operations_open_wager_session(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    session_id = payload.get("id") or payload.get("session_id") or _sequence_id("session", next_state["wager_sessions"])
    player_id = payload.get("player_profile_id")
    player = next_state["player_profiles"].get(player_id)
    if not player:
        return {"ok": False, "state": next_state, "reason": "player_not_found", "side_effects": ()}
    asset_kind = payload.get("asset_kind", "table")
    asset_id = payload.get("asset_id")
    asset = _asset_lookup(next_state, asset_kind, asset_id)
    rule_eval = config.evaluate_rule(
        "wager_session_policy",
        {
            "restriction_state": player.get("restriction_state"),
            "asset_operational": _asset_operational(asset_kind, asset),
        },
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    if rule_eval["passed"] is not True:
        return {
            "ok": False,
            "state": next_state,
            "reason": "session_open_rejected",
            "rule_evaluation": rule_eval,
            "side_effects": (),
        }
    model = create_model_record(
        WAGER_SESSION_TABLE,
        {
            "id": session_id,
            "tenant": payload.get("tenant", player.get("tenant", "default")),
            "created_at": timestamp,
            "updated_at": timestamp,
            "player_profile_id": player_id,
            "asset_kind": asset_kind,
            "asset_id": asset_id,
            "session_status": "active",
            "rating_status": "suppressed" if player.get("restriction_state") == "ratings_suppressed" else "provisional",
            "average_bet": payload.get("average_bet"),
            "theoretical_win": payload.get("theoretical_win"),
            "dispute_flag": bool(payload.get("dispute_flag", False)),
            "started_at": payload.get("started_at", timestamp),
            "ended_at": None,
            "payload": {
                **dict(payload),
                "host_touchpoint": payload.get("host_touchpoint"),
                "loyalty_offer": payload.get("loyalty_offer"),
            },
        },
    )
    record = model["record"]
    next_state["wager_sessions"][session_id] = record
    _record_audit(next_state, action="open_wager_session", subject_table=WAGER_SESSION_TABLE, subject_id=session_id, details=record)
    _emit_event(next_state, EMITTED[0], payload=record, aggregate_table=WAGER_SESSION_TABLE, aggregate_id=session_id)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def gaming_casino_operations_close_wager_session(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    session_id = payload.get("session_id")
    existing = next_state["wager_sessions"].get(session_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "session_not_found", "side_effects": ()}
    updated = {
        **existing,
        "session_status": "closed",
        "ended_at": payload.get("ended_at", _timestamp(next_state)),
        "average_bet": payload.get("average_bet", existing.get("average_bet")),
        "theoretical_win": payload.get("theoretical_win", existing.get("theoretical_win")),
        "updated_at": _timestamp(next_state),
        "payload": {**existing.get("payload", {}), **dict(payload)},
    }
    next_state["wager_sessions"][session_id] = updated
    _record_audit(next_state, action="close_wager_session", subject_table=WAGER_SESSION_TABLE, subject_id=session_id, details=updated)
    _emit_event(next_state, EMITTED[2], payload=updated, aggregate_table=WAGER_SESSION_TABLE, aggregate_id=session_id)
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def gaming_casino_operations_capture_player_rating(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    session_id = payload.get("session_id")
    existing = next_state["wager_sessions"].get(session_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "session_not_found", "side_effects": ()}
    updated = {
        **existing,
        "rating_status": "final" if payload.get("supervisor_override") else "reviewed",
        "average_bet": float(payload.get("average_bet", existing.get("average_bet") or 0.0)),
        "theoretical_win": float(payload.get("theoretical_win", existing.get("theoretical_win") or 0.0)),
        "updated_at": _timestamp(next_state),
        "payload": {
            **existing.get("payload", {}),
            "rating_source": payload.get("rating_source", "pit_supervisor"),
            "game_pace": payload.get("game_pace"),
            "skill_adjustment": payload.get("skill_adjustment"),
            "supervisor_override": bool(payload.get("supervisor_override")),
            "comp_justification": payload.get("comp_justification"),
        },
    }
    next_state["wager_sessions"][session_id] = updated
    _record_audit(next_state, action="capture_player_rating", subject_table=WAGER_SESSION_TABLE, subject_id=session_id, details=updated)
    _emit_event(next_state, EMITTED[1], payload=updated, aggregate_table=WAGER_SESSION_TABLE, aggregate_id=session_id)
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def gaming_casino_operations_create_payout(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    payout_id = payload.get("id") or payload.get("payout_id") or _sequence_id("payout", next_state["payouts"])
    amount = float(payload.get("amount", 0.0))
    if amount <= 0:
        return {"ok": False, "state": next_state, "reason": "invalid_payout_amount", "side_effects": ()}
    rule_eval = config.evaluate_rule(
        "payout_approval_policy",
        {"amount": amount, "has_approval": bool(payload.get("approved_by"))},
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    approval_state = "approved" if rule_eval["passed"] else "pending_review"
    suspicious_flag = "compliance_review_recommended" in rule_eval["reasons"] or bool(payload.get("suspicious_activity_flag"))
    model = create_model_record(
        PAYOUT_TABLE,
        {
            "id": payout_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "payout_number": payload.get("payout_number", payout_id.upper()),
            "source_type": payload.get("source_type", "wager_session"),
            "source_id": payload.get("source_id", payload.get("session_id", "unknown-source")),
            "payout_kind": payload.get("payout_kind", "jackpot"),
            "amount": amount,
            "currency": payload.get("currency", next_state["configuration"].get("default_currency", "USD")),
            "approval_state": approval_state,
            "patron_verification_level": payload.get("patron_verification_level", "id_checked"),
            "suspicious_activity_flag": suspicious_flag,
            "payload": {
                **dict(payload),
                "rule_reasons": rule_eval["reasons"],
                "approval_required": approval_state != "approved",
            },
        },
    )
    record = model["record"]
    next_state["payouts"][payout_id] = record
    _record_audit(next_state, action="create_payout", subject_table=PAYOUT_TABLE, subject_id=payout_id, details=record)
    _emit_event(next_state, EMITTED[0], payload=record, aggregate_table=PAYOUT_TABLE, aggregate_id=payout_id)
    if approval_state != "approved":
        _emit_event(next_state, EMITTED[3], payload=record, aggregate_table=PAYOUT_TABLE, aggregate_id=payout_id)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "approval_required": approval_state != "approved",
        "rule_evaluation": rule_eval,
        "side_effects": (),
    }


def gaming_casino_operations_approve_payout(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    payout_id = payload.get("payout_id")
    existing = next_state["payouts"].get(payout_id)
    if not existing:
        return {"ok": False, "state": next_state, "reason": "payout_not_found", "side_effects": ()}
    if not payload.get("approved_by") or not payload.get("witness_id"):
        return {"ok": False, "state": next_state, "reason": "approval_evidence_missing", "side_effects": ()}
    updated = {
        **existing,
        "approval_state": "approved",
        "updated_at": _timestamp(next_state),
        "payload": {
            **existing.get("payload", {}),
            "approved_by": payload["approved_by"],
            "witness_id": payload["witness_id"],
            "approval_notes": payload.get("approval_notes"),
        },
    }
    next_state["payouts"][payout_id] = updated
    _record_audit(next_state, action="approve_payout", subject_table=PAYOUT_TABLE, subject_id=payout_id, details=updated)
    _emit_event(next_state, EMITTED[2], payload=updated, aggregate_table=PAYOUT_TABLE, aggregate_id=payout_id)
    return {"ok": True, "state": next_state, "record": updated, "side_effects": ()}


def gaming_casino_operations_open_responsible_gaming_case(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    case_id = payload.get("id") or payload.get("case_id") or _sequence_id("rg_case", next_state["responsible_gaming_cases"])
    player_id = payload.get("player_profile_id")
    if player_id and player_id not in next_state["player_profiles"]:
        return {"ok": False, "state": next_state, "reason": "player_not_found", "side_effects": ()}
    cooling_off_hours = int(payload.get("cooling_off_hours", _parameter_value(next_state, "cooling_off_hours")))
    rule_eval = config.evaluate_rule(
        "responsible_gaming_policy",
        {"cooling_off_hours": cooling_off_hours},
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    if rule_eval["passed"] is not True:
        return {"ok": False, "state": next_state, "reason": "responsible_gaming_policy_rejected", "rule_evaluation": rule_eval, "side_effects": ()}
    model = create_model_record(
        RESPONSIBLE_GAMING_CASE_TABLE,
        {
            "id": case_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "case_number": payload.get("case_number", case_id.upper()),
            "player_profile_id": player_id,
            "risk_level": payload.get("risk_level", "high"),
            "intervention_state": payload.get("intervention_state", "cooling_off"),
            "cooling_off_until": payload.get("cooling_off_until", f"T+{cooling_off_hours}h"),
            "owner_id": payload.get("owner_id", "responsible-gaming-team"),
            "payload": {**dict(payload), "cooling_off_hours": cooling_off_hours},
        },
    )
    record = model["record"]
    next_state["responsible_gaming_cases"][case_id] = record
    if player_id and payload.get("intervention_state", "cooling_off") in {"cooling_off", "self_excluded"}:
        player_payload = {
            "player_profile_id": player_id,
            "restriction_state": payload.get("intervention_state", "cooling_off"),
            "reason": "responsible_gaming_intervention",
            "applied_by": payload.get("owner_id", "responsible-gaming-team"),
            "effective_until": record.get("cooling_off_until"),
        }
        restriction_result = gaming_casino_operations_apply_player_restriction(next_state, player_payload)
        next_state = restriction_result["state"]
    _record_audit(next_state, action="open_responsible_gaming_case", subject_table=RESPONSIBLE_GAMING_CASE_TABLE, subject_id=case_id, details=record)
    _emit_event(next_state, EMITTED[3], payload=record, aggregate_table=RESPONSIBLE_GAMING_CASE_TABLE, aggregate_id=case_id)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def gaming_casino_operations_record_compliance_case(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    timestamp = _timestamp(next_state)
    case_id = payload.get("id") or payload.get("case_id") or _sequence_id("compliance_case", next_state["gaming_compliance_cases"])
    rule_eval = config.evaluate_rule(
        "compliance_case_policy",
        {
            "compliance_type": payload.get("compliance_type", "surveillance_review"),
            "surveillance_request": bool(payload.get("surveillance_request")),
        },
        parameters={name: _parameter_value(next_state, name) for name in config.PARAMETERS},
    )
    model = create_model_record(
        GAMING_COMPLIANCE_TABLE,
        {
            "id": case_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "case_number": payload.get("case_number", case_id.upper()),
            "compliance_type": payload.get("compliance_type", "surveillance_review"),
            "severity": payload.get("severity", "high"),
            "case_status": payload.get("case_status", "open"),
            "jurisdiction": payload.get("jurisdiction", next_state["configuration"].get("jurisdiction", "NV")),
            "owner_id": payload.get("owner_id", "compliance-team"),
            "payload": {**dict(payload), "rule_reasons": rule_eval["reasons"]},
        },
    )
    record = model["record"]
    next_state["gaming_compliance_cases"][case_id] = record
    _record_audit(next_state, action="record_compliance_case", subject_table=GAMING_COMPLIANCE_TABLE, subject_id=case_id, details=record)
    _emit_event(next_state, EMITTED[3], payload=record, aggregate_table=GAMING_COMPLIANCE_TABLE, aggregate_id=case_id)
    return {"ok": True, "state": next_state, "record": record, "rule_evaluation": rule_eval, "side_effects": ()}


def gaming_casino_operations_request_surveillance_review(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    return gaming_casino_operations_record_compliance_case(
        state,
        {
            **dict(payload),
            "compliance_type": "surveillance_review",
            "surveillance_request": True,
            "case_status": payload.get("case_status", "requested"),
        },
    )


def gaming_casino_operations_create_control_assertion(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    assertion_id = payload.get("assertion_id") or _sequence_id("assertion", next_state["control_assertions"])
    timestamp = _timestamp(next_state)
    model = create_model_record(
        CONTROL_ASSERTION_TABLE,
        {
            "id": assertion_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "assertion_id": assertion_id,
            "control_name": payload.get("control_name", "jackpot_dual_control"),
            "frequency": payload.get("frequency", "per_shift"),
            "assertion_status": payload.get("assertion_status", "passed"),
            "owner_id": payload.get("owner_id", "internal-audit"),
            "payload": dict(payload),
        },
    )
    record = model["record"]
    next_state["control_assertions"][assertion_id] = record
    _record_audit(next_state, action="create_control_assertion", subject_table=CONTROL_ASSERTION_TABLE, subject_id=assertion_id, details=record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def gaming_casino_operations_register_governed_model(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy(state)
    model_id = payload.get("id") or payload.get("model_id") or _sequence_id("governed_model", next_state["governed_models"])
    timestamp = _timestamp(next_state)
    model = create_model_record(
        GOVERNED_MODEL_TABLE,
        {
            "id": model_id,
            "tenant": payload.get("tenant", "default"),
            "created_at": timestamp,
            "updated_at": timestamp,
            "model_name": payload.get("model_name", "gaming-floor-assistant"),
            "model_version": payload.get("model_version", "1.0.0"),
            "approval_state": payload.get("approval_state", "approved"),
            "drift_state": payload.get("drift_state", "within_tolerance"),
            "last_reviewed_at": payload.get("last_reviewed_at", timestamp),
            "payload": dict(payload),
        },
    )
    record = model["record"]
    next_state["governed_models"][model_id] = record
    _record_audit(next_state, action="register_governed_model", subject_table=GOVERNED_MODEL_TABLE, subject_id=model_id, details=record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def gaming_casino_operations_handle_table_game(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    action = payload.get("action", "open")
    if action == "close":
        return gaming_casino_operations_close_table(state, payload)
    if action == "inventory":
        return gaming_casino_operations_record_table_inventory_movement(state, payload)
    return gaming_casino_operations_open_table(state, payload)


def gaming_casino_operations_handle_slot_machine(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    action = payload.get("action", "install")
    if action == "recover":
        return gaming_casino_operations_recover_slot_fault(state, payload)
    return gaming_casino_operations_register_slot_machine(state, payload)


def gaming_casino_operations_handle_wager_session(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    action = payload.get("action", "open")
    if action == "close":
        return gaming_casino_operations_close_wager_session(state, payload)
    if action == "rate":
        return gaming_casino_operations_capture_player_rating(state, payload)
    return gaming_casino_operations_open_wager_session(state, payload)


def gaming_casino_operations_handle_payout(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    action = payload.get("action", "create")
    if action == "approve":
        return gaming_casino_operations_approve_payout(state, payload)
    return gaming_casino_operations_create_payout(state, payload)


def gaming_casino_operations_build_workbench_view(state: dict[str, Any], tenant: str = "default") -> dict[str, Any]:
    limit = int(_parameter_value(state, "workbench_limit"))
    players = tuple(record for record in state.get("player_profiles", {}).values() if record.get("tenant") == tenant)
    tables = tuple(record for record in state.get("table_games", {}).values() if record.get("tenant") == tenant)
    slots = tuple(record for record in state.get("slot_machines", {}).values() if record.get("tenant") == tenant)
    sessions = tuple(record for record in state.get("wager_sessions", {}).values() if record.get("tenant") == tenant)
    payouts = tuple(record for record in state.get("payouts", {}).values() if record.get("tenant") == tenant)
    rg_cases = tuple(record for record in state.get("responsible_gaming_cases", {}).values() if record.get("tenant") == tenant)
    compliance = tuple(record for record in state.get("gaming_compliance_cases", {}).values() if record.get("tenant") == tenant)
    queues = {
        "patron_identity_reviews": tuple(record for record in players if record.get("enrollment_status") == "review_pending")[:limit],
        "restricted_players": tuple(record for record in players if record.get("restriction_state") != "clear")[:limit],
        "open_tables": tuple(record for record in tables if record.get("table_status") == "open")[:limit],
        "slot_faults": tuple(record for record in slots if record.get("fault_state") != "clear")[:limit],
        "active_sessions": tuple(record for record in sessions if record.get("session_status") == "active")[:limit],
        "pending_payouts": tuple(record for record in payouts if record.get("approval_state") != "approved")[:limit],
        "responsible_gaming_cases": tuple(record for record in rg_cases if record.get("intervention_state") not in {"closed", "resolved"})[:limit],
        "compliance_cases": tuple(record for record in compliance if record.get("case_status") not in {"closed", "resolved"})[:limit],
        "dead_letters": tuple(record for record in state.get("dead_letter", ()))[:limit],
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "summary": {
            "player_count": len(players),
            "restricted_player_count": len(queues["restricted_players"]),
            "table_count": len(tables),
            "slot_count": len(slots),
            "active_session_count": len(queues["active_sessions"]),
            "pending_payout_count": len(queues["pending_payouts"]),
            "responsible_gaming_case_count": len(queues["responsible_gaming_cases"]),
            "compliance_case_count": len(queues["compliance_cases"]),
        },
        "queues": queues,
        "persona_views": {
            "floor_supervisor": ("patron_identity_reviews", "open_tables", "pending_payouts"),
            "cage_operations": ("pending_payouts", "dead_letters"),
            "slot_operations": ("slot_faults", "dead_letters"),
            "responsible_gaming": ("restricted_players", "responsible_gaming_cases"),
            "compliance_command": ("compliance_cases", "dead_letters"),
        },
        "side_effects": (),
    }


def gaming_casino_operations_query_workbench(state: dict[str, Any], filters: dict[str, Any] | None = None) -> dict[str, Any]:
    filters = dict(filters or {})
    workbench = gaming_casino_operations_build_workbench_view(state, tenant=filters.get("tenant", "default"))
    return {"ok": True, "result": workbench, "filters": filters, "read_only": True, "side_effects": ()}


def gaming_casino_operations_run_advanced_assessment(state: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    workbench = gaming_casino_operations_build_workbench_view(state, tenant=dict(payload or {}).get("tenant", "default"))
    pending = workbench["summary"]["pending_payout_count"] + workbench["summary"]["compliance_case_count"]
    restricted = workbench["summary"]["restricted_player_count"]
    score = round(min(0.99, 0.62 + (pending * 0.03) + (restricted * 0.02)), 4)
    return {
        "ok": True,
        "score": score,
        "risk_posture": "elevated" if score >= 0.75 else "stable",
        "explanations": (
            "pending_payout_review_pressure",
            "restriction_case_density",
            "owned_boundary_respected",
        ),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def gaming_casino_operations_parse_document_instruction(document: str, instruction: str) -> dict[str, Any]:
    text = f"{document}\n{instruction}".lower()
    workflow = DOMAIN_WORKFLOWS[0]
    candidate_tables = [PLAYER_PROFILE_TABLE]
    if "shift close" in text or "bankroll" in text or "pit" in text:
        workflow = "gaming_casino_operations_table_shift_close_workflow"
        candidate_tables = [TABLE_GAME_TABLE, PAYOUT_TABLE]
    elif "jackpot" in text or "handpay" in text or "payout" in text:
        workflow = "gaming_casino_operations_jackpot_handpay_workflow"
        candidate_tables = [PAYOUT_TABLE, WAGER_SESSION_TABLE]
    elif "slot" in text and ("fault" in text or "offline" in text or "tilt" in text):
        workflow = "gaming_casino_operations_slot_fault_recovery_workflow"
        candidate_tables = [SLOT_MACHINE_TABLE, GAMING_COMPLIANCE_TABLE]
    elif "responsible" in text or "self exclude" in text or "cooling off" in text:
        workflow = "gaming_casino_operations_responsible_gaming_intervention_workflow"
        candidate_tables = [RESPONSIBLE_GAMING_CASE_TABLE, PLAYER_PROFILE_TABLE]
    return {
        "ok": True,
        "candidate_tables": tuple(candidate_tables),
        "workflow": workflow,
        "instruction": instruction,
        "document_digest": _digest(document),
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def gaming_casino_operations_run_player_enrollment_workflow(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    result = gaming_casino_operations_create_player_profile(state, payload)
    next_state = result["state"]
    _record_workflow(next_state, workflow="gaming_casino_operations_patron_enrollment_workflow", status="review_pending" if result["review_required"] else "completed", payload=payload, outputs={"player_profile_id": result["record"]["id"]})
    return {"ok": True, "state": next_state, "steps": ("identity_review", "enrollment_decision"), "result": result, "side_effects": ()}


def gaming_casino_operations_run_table_shift_close_workflow(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    result = gaming_casino_operations_close_table(state, payload)
    next_state = result.get("state", _copy(state))
    _record_workflow(next_state, workflow="gaming_casino_operations_table_shift_close_workflow", status="completed" if result["ok"] else "blocked", payload=payload, outputs={"variance": result.get("variance"), "reason": result.get("reason")})
    return {"ok": result["ok"], "state": next_state, "steps": ("variance_check", "supervisor_signoff", "closure_publish"), "result": result, "side_effects": ()}


def gaming_casino_operations_run_slot_fault_recovery_workflow(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    result = gaming_casino_operations_recover_slot_fault(state, payload)
    next_state = result.get("state", _copy(state))
    _record_workflow(next_state, workflow="gaming_casino_operations_slot_fault_recovery_workflow", status="completed" if result["ok"] else "blocked", payload=payload, outputs={"slot_machine_id": payload.get("slot_machine_id")})
    return {"ok": result["ok"], "state": next_state, "steps": ("capture_meter_snapshot", "approval_check", "return_to_service"), "result": result, "side_effects": ()}


def gaming_casino_operations_run_jackpot_handpay_workflow(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    created = gaming_casino_operations_create_payout(state, payload)
    next_state = created["state"]
    approved = None
    if created["record"]["approval_state"] != "approved" and payload.get("approved_by") and payload.get("witness_id"):
        approved = gaming_casino_operations_approve_payout(next_state, {"payout_id": created["record"]["id"], "approved_by": payload.get("approved_by"), "witness_id": payload.get("witness_id"), "approval_notes": payload.get("approval_notes")})
        next_state = approved["state"]
    _record_workflow(next_state, workflow="gaming_casino_operations_jackpot_handpay_workflow", status="completed" if (approved or created)["ok"] else "blocked", payload=payload, outputs={"payout_id": created["record"]["id"], "approved": approved["ok"] if approved else created["record"]["approval_state"] == "approved"})
    return {"ok": created["ok"] and (approved is None or approved["ok"]), "state": next_state, "steps": ("create_payout", "supervisor_approval", "release_to_cage"), "created": created, "approved": approved, "side_effects": ()}


def gaming_casino_operations_run_responsible_gaming_intervention_workflow(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    result = gaming_casino_operations_open_responsible_gaming_case(state, payload)
    next_state = result.get("state", _copy(state))
    _record_workflow(next_state, workflow="gaming_casino_operations_responsible_gaming_intervention_workflow", status="completed" if result["ok"] else "blocked", payload=payload, outputs={"case_id": result.get("record", {}).get("id")})
    return {"ok": result["ok"], "state": next_state, "steps": ("risk_review", "intervention_plan", "player_restriction_sync"), "result": result, "side_effects": ()}


def gaming_casino_operations_build_schema_contract() -> dict[str, Any]:
    models = model_contracts()
    return {
        "format": "appgen.gaming-casino-operations-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": models,
        "owned_tables": GAMING_CASINO_OPERATIONS_OWNED_TABLES,
        "migrations": (
            {
                "path": "pbcs/gaming_casino_operations/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": GAMING_CASINO_OPERATIONS_OWNED_TABLES,
                "backend_allowlist": GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": tuple(
            {
                "class_name": item["class_name"],
                "table": item["table"],
                "fields": tuple(field["name"] for field in item["fields"]),
            }
            for item in models
        ),
        "datastore_backends": GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def gaming_casino_operations_build_service_contract() -> dict[str, Any]:
    command_methods = (
        "register_defaults",
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_player_profile",
        "apply_player_restriction",
        "handle_table_game",
        "handle_slot_machine",
        "handle_wager_session",
        "handle_payout",
        "open_responsible_gaming_case",
        "record_compliance_case",
        "request_surveillance_review",
        "create_control_assertion",
        "register_governed_model",
        "run_player_enrollment_workflow",
        "run_table_shift_close_workflow",
        "run_slot_fault_recovery_workflow",
        "run_jackpot_handpay_workflow",
        "run_responsible_gaming_intervention_workflow",
    )
    query_methods = (
        "query_workbench",
        "build_workbench_view",
        "run_advanced_assessment",
        "parse_document_instruction",
        "build_schema_contract",
    )
    return {
        "format": "appgen.gaming-casino-operations-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": command_methods,
        "query_methods": query_methods,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "workflows": GAMING_CASINO_OPERATIONS_WORKFLOW_KEYS,
    }


def gaming_casino_operations_build_api_contract() -> dict[str, Any]:
    return {
        "format": "appgen.gaming-casino-operations-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": (
            "POST /player-profiles",
            "POST /table-games",
            "POST /slot-machines",
            "POST /wager-sessions",
            "POST /payouts",
            "GET /gaming-casino-operations-workbench",
        ),
        "standalone_routes": (
            "POST /app/gaming-casino-operations/player-profiles",
            "POST /app/gaming-casino-operations/table-games",
            "POST /app/gaming-casino-operations/slot-machines",
            "POST /app/gaming-casino-operations/wager-sessions",
            "POST /app/gaming-casino-operations/payouts",
            "POST /app/gaming-casino-operations/responsible-gaming-cases",
            "POST /app/gaming-casino-operations/compliance-cases",
            "GET /app/gaming-casino-operations/workbench",
        ),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": GAMING_CASINO_OPERATIONS_OWNED_TABLES,
    }


def gaming_casino_operations_build_release_evidence() -> dict[str, Any]:
    schema = gaming_casino_operations_build_schema_contract()
    service = gaming_casino_operations_build_service_contract()
    events = event_contract_manifest()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"]},
        {"id": "service_contract_depth", "ok": service["ok"] and len(service["command_methods"]) >= 10},
        {"id": "event_contract_only", "ok": events["event_contract"] == "AppGen-X"},
        {"id": "owned_boundary", "ok": gaming_casino_operations_verify_owned_table_boundary(GAMING_CASINO_OPERATIONS_OWNED_TABLES)["ok"]},
        {"id": "workflow_surface", "ok": len(GAMING_CASINO_OPERATIONS_WORKFLOW_KEYS) >= 4},
        {"id": "model_alignment_smoke", "ok": model_alignment_smoke_test()["ok"]},
    )
    return {
        "format": "appgen.gaming-casino-operations-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "schema": schema,
        "service": service,
        "events": events,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "ui": GAMING_CASINO_OPERATIONS_UI_FRAGMENT_KEYS,
            "workflows": GAMING_CASINO_OPERATIONS_WORKFLOW_KEYS,
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def gaming_casino_operations_permissions_contract() -> dict[str, Any]:
    from .permissions import permission_manifest

    return permission_manifest()


def gaming_casino_operations_verify_owned_table_boundary(references: tuple[str, ...] | list[str] = ()) -> dict[str, Any]:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.startswith(f"{PBC_KEY}_")
        and ref not in GAMING_CASINO_OPERATIONS_OWNED_TABLES
    )
    foreign = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid and not foreign,
        "pbc": PBC_KEY,
        "invalid_references": invalid + foreign,
        "allowed_tables": GAMING_CASINO_OPERATIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def gaming_casino_operations_runtime_capabilities() -> dict[str, Any]:
    domain = domain_depth_contract()
    smoke = gaming_casino_operations_runtime_smoke()
    operations = (
        "register_defaults",
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "query_workbench",
        "run_advanced_assessment",
        "parse_document_instruction",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    ) + DOMAIN_OPERATIONS
    return {
        "format": "appgen.gaming-casino-operations-runtime-capabilities.v2",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": GAMING_CASINO_OPERATIONS_OWNED_TABLES,
        "allowed_database_backends": GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": GAMING_CASINO_OPERATIONS_STANDARD_FEATURE_KEYS,
        "capabilities": GAMING_CASINO_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "workflows": GAMING_CASINO_OPERATIONS_WORKFLOW_KEYS,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def gaming_casino_operations_runtime_smoke() -> dict[str, Any]:
    state = gaming_casino_operations_empty_state()
    defaults = gaming_casino_operations_register_defaults(state)
    cfg = gaming_casino_operations_configure_runtime(defaults["state"], {"database_backend": "postgresql", "event_topic": REQUIRED_TOPIC, "workbench_limit": 25})
    player = gaming_casino_operations_create_player_profile(
        cfg["state"],
        {
            "tenant": "tenant-smoke",
            "player_number": "P-SMOKE",
            "legal_name": "Smoke Patron",
            "date_of_birth": "1988-01-01",
            "identity_confidence": 0.98,
            "age_verified": True,
            "property_id": "property-smoke",
        },
    )
    table = gaming_casino_operations_open_table(
        player["state"],
        {
            "tenant": "tenant-smoke",
            "table_number": "BJ-12",
            "pit": "north",
            "opening_bankroll": 25000.0,
            "dealer_id": "dealer-smoke",
            "supervisor_id": "supervisor-smoke",
        },
    )
    slot = gaming_casino_operations_register_slot_machine(
        table["state"],
        {
            "tenant": "tenant-smoke",
            "asset_code": "SL-100",
            "bank_location": "bank-a",
            "denomination": 1.0,
            "paytable_version": "v1",
        },
    )
    session = gaming_casino_operations_open_wager_session(
        slot["state"],
        {
            "tenant": "tenant-smoke",
            "player_profile_id": player["record"]["id"],
            "asset_kind": "table",
            "asset_id": table["record"]["id"],
        },
    )
    payout = gaming_casino_operations_create_payout(
        session["state"],
        {
            "tenant": "tenant-smoke",
            "session_id": session["record"]["id"],
            "source_id": session["record"]["id"],
            "amount": 1800.0,
            "approved_by": "supervisor-smoke",
            "currency": "USD",
        },
    )
    rg_case = gaming_casino_operations_open_responsible_gaming_case(
        payout["state"],
        {
            "tenant": "tenant-smoke",
            "player_profile_id": player["record"]["id"],
            "owner_id": "rg-officer",
            "cooling_off_hours": 96,
        },
    )
    smoke_key = f"smoke-event-{uuid4().hex[:12]}"
    dead_key = f"bad-event-{uuid4().hex[:12]}"
    received = gaming_casino_operations_receive_event(rg_case["state"], {"event_type": CONSUMED[0], "tenant": "tenant-smoke", "idempotency_key": smoke_key})
    duplicate = gaming_casino_operations_receive_event(received["state"], {"event_type": CONSUMED[0], "tenant": "tenant-smoke", "idempotency_key": smoke_key})
    dead = gaming_casino_operations_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "tenant": "tenant-smoke", "idempotency_key": dead_key})
    workbench = gaming_casino_operations_build_workbench_view(dead["state"], tenant="tenant-smoke")
    release = gaming_casino_operations_build_release_evidence()
    checks = (
        {"id": "register_defaults", "ok": defaults["ok"]},
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "create_player_profile", "ok": player["ok"]},
        {"id": "open_table", "ok": table["ok"]},
        {"id": "register_slot_machine", "ok": slot["ok"]},
        {"id": "open_wager_session", "ok": session["ok"]},
        {"id": "create_payout", "ok": payout["ok"]},
        {"id": "open_responsible_gaming_case", "ok": rg_case["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "release_evidence", "ok": release["ok"]},
        {"id": "domain_depth", "ok": domain_depth_smoke_test()["ok"]},
    )
    return {
        "format": "appgen.gaming-casino-operations-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "workbench": workbench,
        "release": release,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


def gaming_casino_operations_execute_domain_operation(state: dict[str, Any], operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    handlers = {
        "enroll_player_profile": gaming_casino_operations_create_player_profile,
        "apply_player_restriction": gaming_casino_operations_apply_player_restriction,
        "open_table": gaming_casino_operations_open_table,
        "close_table": gaming_casino_operations_close_table,
        "record_table_inventory_movement": gaming_casino_operations_record_table_inventory_movement,
        "register_slot_machine": gaming_casino_operations_register_slot_machine,
        "recover_slot_fault": gaming_casino_operations_recover_slot_fault,
        "open_wager_session": gaming_casino_operations_open_wager_session,
        "close_wager_session": gaming_casino_operations_close_wager_session,
        "capture_player_rating": gaming_casino_operations_capture_player_rating,
        "create_payout": gaming_casino_operations_create_payout,
        "approve_payout": gaming_casino_operations_approve_payout,
        "open_responsible_gaming_case": gaming_casino_operations_open_responsible_gaming_case,
        "record_compliance_case": gaming_casino_operations_record_compliance_case,
        "request_surveillance_review": gaming_casino_operations_request_surveillance_review,
        "register_policy_rule": lambda s, p: gaming_casino_operations_register_rule(s, p),
        "update_runtime_parameter": lambda s, p: gaming_casino_operations_set_parameter(s, p["name"], p["value"]),
        "attest_control_assertion": gaming_casino_operations_create_control_assertion,
        "register_governed_model": gaming_casino_operations_register_governed_model,
    }
    handler = handlers.get(operation)
    if handler is None:
        return {"ok": False, "state": _copy(state), "reason": "unknown_domain_operation", "operation": operation, "plan": build_domain_operation_plan(operation, payload), "side_effects": ()}
    result = handler(state, payload)
    result["operation_plan"] = build_domain_operation_plan(operation, payload)
    return result


from .casino_control import improve1_casino_control_contract as gaming_casino_operations_improve1_casino_control_contract

_gaming_casino_operations_base_build_release_evidence = gaming_casino_operations_build_release_evidence
_gaming_casino_operations_base_runtime_capabilities = gaming_casino_operations_runtime_capabilities

def gaming_casino_operations_build_release_evidence() -> dict[str, Any]:
    evidence = _gaming_casino_operations_base_build_release_evidence()
    control = gaming_casino_operations_improve1_casino_control_contract()
    checks = tuple(evidence.get('checks', ())) + ({'id': 'improve1_casino_control', 'ok': control['ok']},)
    generated = dict(evidence.get('generated_artifacts', {}))
    generated['casino_control'] = {'capability_count': control['capability_count'], 'owned_tables': control['owned_tables'], 'event_contract': control['event_contract'], 'required_event_topic': control['required_event_topic']}
    return {**evidence, 'ok': evidence.get('ok') is True and control['ok'], 'checks': checks, 'generated_artifacts': generated, 'casino_control': control, 'blocking_gaps': tuple(evidence.get('blocking_gaps', ())) + tuple(control.get('blocking_gaps', ())), 'side_effects': ()}

def gaming_casino_operations_runtime_capabilities() -> dict[str, Any]:
    runtime = _gaming_casino_operations_base_runtime_capabilities()
    control = gaming_casino_operations_improve1_casino_control_contract()
    operations = tuple(runtime.get('operations', ())) + ('improve1_casino_control_contract',)
    return {**runtime, 'ok': runtime.get('ok') is True and control['ok'], 'operations': operations, 'casino_control': control, 'improve1_capabilities': tuple(item['slug'] for item in control['capabilities']), 'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(control['owned_tables']))), 'allowed_database_backends': control['allowed_database_backends'], 'event_contract': control['event_contract'], 'stream_engine_picker_visible': False, 'side_effects': ()}
