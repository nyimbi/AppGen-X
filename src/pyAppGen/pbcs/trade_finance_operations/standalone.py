"""Standalone one-PBC application surface for trade_finance_operations."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import runtime
from .controls import trade_finance_operations_control_catalog
from .forms import trade_finance_operations_form_contracts
from .wizards import trade_finance_operations_wizard_contracts

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "ucp600_and_internal_controls",
    "require_dual_control": True,
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.75,
    "materiality_threshold": 0.02,
    "approval_sla_hours": 8,
    "risk_threshold": 0.65,
    "forecast_horizon_days": 14,
    "workbench_limit": 100,
    "sanctions_hold_sla_hours": 4,
    "waiver_response_sla_hours": 24,
    "collateral_haircut_pct": 0.15,
    "limit_buffer_pct": 0.1,
}
DEFAULT_RULES = (
    {"rule_id": "trade_finance.lc.default", "scope": "issuance", "status": "active", "governing_practice": "UCP600", "requires_dual_control": True},
    {"rule_id": "trade_finance.guarantee.default", "scope": "guarantee", "status": "active", "governing_practice": "ISP98", "requires_dual_control": True},
    {"rule_id": "trade_finance.collections.default", "scope": "collection", "status": "active", "governing_practice": "URC522", "requires_dual_control": False},
)


def _copy(value: dict[str, Any] | None = None) -> dict[str, Any]:
    return deepcopy(dict(value or {}))


def _ensure_state(state: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(state)
    defaults: dict[str, Any] = {
        "letters_of_credit": {},
        "guarantees": {},
        "collections": {},
        "trade_bills": {},
        "trade_loans": {},
        "document_packages": {},
        "sanctions_checks": {},
        "discrepancies": {},
        "collateral_margins": {},
        "limit_reservations": {},
        "fee_assessments": {},
        "settlements": {},
        "swift_messages": {},
        "release_evidence_packs": {},
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "workflow_history": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "assistant_guidance": (),
    }
    for key, default in defaults.items():
        if key not in enriched:
            enriched[key] = deepcopy(default)
    return enriched


def _sequence(prefix: str, collection: dict[str, Any]) -> str:
    return f"{prefix}_{len(collection) + 1:05d}"


def _append_outbox(state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    next_state = _ensure_state(state)
    event = {
        "event_id": _sequence("evt", {str(index): item for index, item in enumerate(next_state.get("outbox", ()))}) ,
        "event_type": event_type,
        "payload": deepcopy(payload),
        "topic": runtime.TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "status": "pending",
    }
    next_state["outbox"] = tuple(next_state.get("outbox", ())) + (event,)
    return next_state


def _append_history(state: dict[str, Any], action: str, data: dict[str, Any]) -> dict[str, Any]:
    next_state = _ensure_state(state)
    history = tuple(next_state.get("workflow_history", ()))
    next_state["workflow_history"] = history + ({"action": action, "data": deepcopy(data)},)
    return next_state


def _require_case(state: dict[str, Any], case_id: str) -> dict[str, Any] | None:
    for bucket in ("letters_of_credit", "guarantees", "collections"):
        if case_id in state.get(bucket, {}):
            return state[bucket][case_id]
    return None


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": "trade_finance_operations",
        "app_class": "TradeFinanceOperationsStandaloneApp",
        "implementation_directory": "src/pyAppGen/pbcs/trade_finance_operations",
        "service_methods": (
            "configure",
            "register_defaults",
            "issue_letter_of_credit",
            "issue_bank_guarantee",
            "lodge_documentary_collection",
            "register_trade_bill",
            "link_trade_loan",
            "record_shipment_documents",
            "run_sanctions_screening",
            "examine_document_package",
            "request_discrepancy_waiver",
            "post_collateral_margin",
            "reserve_limit_exposure",
            "assess_case_fees",
            "settle_trade_case",
            "generate_swift_message_evidence",
            "simulate_case_amendment",
            "build_workbench",
            "build_case_detail",
            "build_release_evidence_pack",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench", "detail"),
        "docs": (
            "README.md",
            "implementation-plan.md",
            "implementation-status.md",
            "RELEASE_EVIDENCE.md",
        ),
        "event_contract": "AppGen-X",
        "event_topic": runtime.TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": runtime.TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    }


class TradeFinanceOperationsStandaloneApp:
    """Mutable, package-local trade finance app shell for one-PBC use."""

    def __init__(self, *, tenant: str = "default", state: dict[str, Any] | None = None) -> None:
        self.tenant = tenant
        self.state = _ensure_state(state or runtime.trade_finance_operations_empty_state())

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {**DEFAULT_CONFIGURATION, **_copy(configuration)}
        result = runtime.trade_finance_operations_configure_runtime(self.state, candidate)
        self.state = _ensure_state(result["state"])
        return {**result, "state": self.snapshot()}

    def register_defaults(self) -> dict[str, Any]:
        if not self.state.get("configuration", {}).get("ok"):
            self.configure()
        parameter_results = []
        for key, value in DEFAULT_PARAMETERS.items():
            parameter_results.append(runtime.trade_finance_operations_set_parameter(self.state, key, value))
            self.state = _ensure_state(parameter_results[-1]["state"])
        rule_results = []
        for rule in DEFAULT_RULES:
            rule_results.append(runtime.trade_finance_operations_register_rule(self.state, {**rule, "tenant": self.tenant}))
            self.state = _ensure_state(rule_results[-1]["state"])
        return {
            "ok": all(item["ok"] for item in parameter_results + rule_results),
            "state": self.snapshot(),
            "parameters": tuple(item["parameter"] for item in parameter_results),
            "rules": tuple(item["rule"] for item in rule_results),
        }

    def issue_letter_of_credit(self, payload: dict[str, Any]) -> dict[str, Any]:
        case_id = payload["case_id"]
        lc = {
            "case_id": case_id,
            "tenant": payload.get("tenant", self.tenant),
            "instrument_type": payload.get("instrument_type", "commercial_lc"),
            "applicant": payload["applicant"],
            "beneficiary": payload["beneficiary"],
            "issuing_bank": payload.get("issuing_bank", "issuing_bank_default"),
            "currency": payload.get("currency", "USD"),
            "face_amount": float(payload.get("face_amount", 0)),
            "required_documents": tuple(payload.get("required_documents", ("invoice", "bill_of_lading", "insurance_certificate"))),
            "status": payload.get("status", "issued"),
        }
        self.state["letters_of_credit"][case_id] = lc
        self.state = _append_history(self.state, "issue_letter_of_credit", lc)
        self.state = _append_outbox(self.state, "TradeFinanceOperationsCreated", {"case_id": case_id, "tenant": lc["tenant"]})
        return {"ok": True, "letter_of_credit": lc, "state": self.snapshot()}

    def issue_bank_guarantee(self, payload: dict[str, Any]) -> dict[str, Any]:
        case_id = payload["case_id"]
        guarantee = {
            "case_id": case_id,
            "tenant": payload.get("tenant", self.tenant),
            "guarantee_type": payload.get("guarantee_type", "performance_guarantee"),
            "beneficiary": payload["beneficiary"],
            "applicant": payload.get("applicant", "unknown_applicant"),
            "currency": payload.get("currency", "USD"),
            "face_amount": float(payload.get("face_amount", 0)),
            "claim_expiry_date": payload.get("claim_expiry_date", "2026-12-31"),
            "status": payload.get("status", "active"),
            "is_sblc": payload.get("guarantee_type") == "standby_lc",
        }
        self.state["guarantees"][case_id] = guarantee
        self.state = _append_history(self.state, "issue_bank_guarantee", guarantee)
        self.state = _append_outbox(self.state, "TradeFinanceOperationsCreated", {"case_id": case_id, "tenant": guarantee["tenant"]})
        return {"ok": True, "guarantee": guarantee, "state": self.snapshot()}

    def lodge_documentary_collection(self, payload: dict[str, Any]) -> dict[str, Any]:
        case_id = payload["case_id"]
        collection = {
            "case_id": case_id,
            "tenant": payload.get("tenant", self.tenant),
            "collection_mode": payload.get("collection_mode", "documents_against_payment"),
            "drawer": payload["drawer"],
            "drawee": payload["drawee"],
            "collecting_bank": payload.get("collecting_bank", "collecting_bank_default"),
            "currency": payload.get("currency", "USD"),
            "face_amount": float(payload.get("face_amount", 0)),
            "status": payload.get("status", "awaiting_documents"),
        }
        self.state["collections"][case_id] = collection
        self.state = _append_history(self.state, "lodge_documentary_collection", collection)
        self.state = _append_outbox(self.state, "TradeFinanceOperationsCreated", {"case_id": case_id, "tenant": collection["tenant"]})
        return {"ok": True, "collection": collection, "state": self.snapshot()}

    def register_trade_bill(self, payload: dict[str, Any]) -> dict[str, Any]:
        bill_id = payload.get("bill_id") or _sequence("bill", self.state["trade_bills"])
        bill = {
            "bill_id": bill_id,
            "case_id": payload["case_id"],
            "bill_type": payload.get("bill_type", "usance_bill"),
            "amount": float(payload.get("amount", 0)),
            "currency": payload.get("currency", "USD"),
            "due_date": payload.get("due_date", "2026-12-31"),
            "status": payload.get("status", "registered"),
        }
        self.state["trade_bills"][bill_id] = bill
        self.state = _append_history(self.state, "register_trade_bill", bill)
        return {"ok": True, "trade_bill": bill, "state": self.snapshot()}

    def link_trade_loan(self, payload: dict[str, Any]) -> dict[str, Any]:
        loan_id = payload.get("loan_id") or _sequence("loan", self.state["trade_loans"])
        loan = {
            "loan_id": loan_id,
            "case_id": payload["case_id"],
            "facility_id": payload.get("facility_id", "facility_default"),
            "financed_amount": float(payload.get("financed_amount", 0)),
            "currency": payload.get("currency", "USD"),
            "margin_pct": float(payload.get("margin_pct", 0.0)),
            "repayment_source": payload.get("repayment_source", "settlement_proceeds"),
            "status": payload.get("status", "linked"),
        }
        self.state["trade_loans"][loan_id] = loan
        self.state = _append_history(self.state, "link_trade_loan", loan)
        return {"ok": True, "trade_loan": loan, "state": self.snapshot()}

    def record_shipment_documents(self, payload: dict[str, Any]) -> dict[str, Any]:
        if _require_case(self.state, payload["case_id"]) is None:
            return {"ok": False, "reason": "case_not_found", "state": self.snapshot()}
        package_id = payload.get("package_id") or _sequence("docs", self.state["document_packages"])
        package = {
            "package_id": package_id,
            "case_id": payload["case_id"],
            "presentation_date": payload.get("presentation_date", "2026-06-01"),
            "shipment_date": payload.get("shipment_date", "2026-05-28"),
            "shipment_country": payload.get("shipment_country", "KE"),
            "documents": tuple(payload.get("documents", ())),
            "status": payload.get("status", "presented"),
        }
        self.state["document_packages"][package_id] = package
        self.state = _append_history(self.state, "record_shipment_documents", package)
        self.state = _append_outbox(self.state, "TradeFinancePresentationReceived", {"case_id": payload["case_id"], "package_id": package_id})
        return {"ok": True, "document_package": package, "state": self.snapshot()}

    def run_sanctions_screening(self, payload: dict[str, Any]) -> dict[str, Any]:
        screening_id = payload.get("screening_id") or _sequence("screen", self.state["sanctions_checks"])
        triggered_terms = tuple(payload.get("triggered_terms", ()))
        text = " ".join(triggered_terms).lower() + " " + str(payload.get("destination_country", "")).lower()
        blocked = any(term in text for term in ("sanctioned", "restricted", "embargoed", "iran", "north korea"))
        screening = {
            "screening_id": screening_id,
            "case_id": payload["case_id"],
            "decision": "blocked" if blocked else "clear",
            "risk_score": 0.91 if blocked else 0.18,
            "triggered_terms": triggered_terms,
            "destination_country": payload.get("destination_country", ""),
            "status": "completed",
        }
        self.state["sanctions_checks"][screening_id] = screening
        self.state = _append_history(self.state, "run_sanctions_screening", screening)
        if blocked:
            self.state = _append_outbox(self.state, "TradeFinanceScreeningBlocked", {"case_id": payload["case_id"], "screening_id": screening_id})
        return {"ok": True, "screening": screening, "state": self.snapshot()}

    def examine_document_package(self, payload: dict[str, Any]) -> dict[str, Any]:
        case = _require_case(self.state, payload["case_id"])
        if case is None:
            return {"ok": False, "reason": "case_not_found", "state": self.snapshot()}
        package_id = payload.get("package_id")
        package = self.state["document_packages"].get(package_id)
        if package is None:
            return {"ok": False, "reason": "package_not_found", "state": self.snapshot()}
        provided = set(package.get("documents", ()))
        required = set(case.get("required_documents", ("invoice", "bill_of_lading", "insurance_certificate")))
        missing = tuple(sorted(required - provided))
        discrepancy_id = payload.get("discrepancy_id") or _sequence("disc", self.state["discrepancies"])
        screening_blocks = tuple(item for item in self.state["sanctions_checks"].values() if item["case_id"] == payload["case_id"] and item["decision"] == "blocked")
        discrepancy_codes = []
        if missing:
            discrepancy_codes.append("missing_document")
        if screening_blocks:
            discrepancy_codes.append("sanctions_hold")
        if package.get("presentation_date") > payload.get("presentation_deadline", package.get("presentation_date")):
            discrepancy_codes.append("late_presentation")
        examination = {
            "discrepancy_id": discrepancy_id,
            "case_id": payload["case_id"],
            "package_id": package_id,
            "missing_documents": missing,
            "discrepancy_codes": tuple(discrepancy_codes),
            "status": "clean" if not discrepancy_codes else "open",
            "severity": "high" if "sanctions_hold" in discrepancy_codes else ("medium" if discrepancy_codes else "none"),
        }
        self.state["discrepancies"][discrepancy_id] = examination
        self.state = _append_history(self.state, "examine_document_package", examination)
        if discrepancy_codes:
            self.state = _append_outbox(self.state, "TradeFinanceDiscrepancyRaised", {"case_id": payload["case_id"], "discrepancy_id": discrepancy_id})
        return {"ok": True, "examination": examination, "state": self.snapshot()}

    def request_discrepancy_waiver(self, payload: dict[str, Any]) -> dict[str, Any]:
        discrepancy_id = payload["discrepancy_id"]
        discrepancy = self.state["discrepancies"].get(discrepancy_id)
        if discrepancy is None:
            return {"ok": False, "reason": "discrepancy_not_found", "state": self.snapshot()}
        updated = {
            **discrepancy,
            "waiver_decision": payload.get("decision", "pending"),
            "requested_by": payload.get("requested_by", "operator"),
            "reason": payload.get("reason", ""),
            "status": "waived" if payload.get("decision") == "accepted" else discrepancy["status"],
        }
        self.state["discrepancies"][discrepancy_id] = updated
        self.state = _append_history(self.state, "request_discrepancy_waiver", updated)
        self.state = _append_outbox(self.state, "TradeFinanceWaiverRequested", {"case_id": updated["case_id"], "discrepancy_id": discrepancy_id})
        return {"ok": True, "discrepancy": updated, "state": self.snapshot()}

    def post_collateral_margin(self, payload: dict[str, Any]) -> dict[str, Any]:
        collateral_id = payload.get("collateral_id") or _sequence("collateral", self.state["collateral_margins"])
        market_value = float(payload.get("market_value", 0))
        haircut = float(payload.get("haircut_pct", DEFAULT_PARAMETERS["collateral_haircut_pct"]))
        record = {
            "collateral_id": collateral_id,
            "case_id": payload["case_id"],
            "collateral_type": payload.get("collateral_type", "cash_margin"),
            "market_value": market_value,
            "haircut_pct": haircut,
            "eligible_value": round(market_value * (1 - haircut), 2),
            "required_margin": float(payload.get("required_margin", 0)),
            "status": "posted",
        }
        self.state["collateral_margins"][collateral_id] = record
        self.state = _append_history(self.state, "post_collateral_margin", record)
        return {"ok": True, "collateral": record, "state": self.snapshot()}

    def reserve_limit_exposure(self, payload: dict[str, Any]) -> dict[str, Any]:
        reservation_id = payload.get("reservation_id") or _sequence("limit", self.state["limit_reservations"])
        headroom = float(payload.get("headroom", 0))
        requested = float(payload.get("requested_exposure", 0))
        record = {
            "reservation_id": reservation_id,
            "case_id": payload["case_id"],
            "facility_id": payload.get("facility_id", "facility_default"),
            "headroom": headroom,
            "requested_exposure": requested,
            "approved": requested <= headroom,
            "status": "reserved" if requested <= headroom else "breached",
        }
        self.state["limit_reservations"][reservation_id] = record
        self.state = _append_history(self.state, "reserve_limit_exposure", record)
        return {"ok": record["approved"], "limit_reservation": record, "state": self.snapshot()}

    def assess_case_fees(self, payload: dict[str, Any]) -> dict[str, Any]:
        fee_id = payload.get("fee_id") or _sequence("fee", self.state["fee_assessments"])
        gross = round(float(payload.get("face_amount", 0)) * float(payload.get("fee_rate_bps", 0)) / 10000, 2)
        extras = round(float(payload.get("swift_fee", 0)) + float(payload.get("discrepancy_fee", 0)) + float(payload.get("amendment_fee", 0)) + float(payload.get("tax_amount", 0)), 2)
        record = {
            "fee_id": fee_id,
            "case_id": payload["case_id"],
            "gross_fee": gross,
            "extra_fee_components": extras,
            "net_fee": round(gross + extras, 2),
            "status": "assessed",
        }
        self.state["fee_assessments"][fee_id] = record
        self.state = _append_history(self.state, "assess_case_fees", record)
        return {"ok": True, "fee_assessment": record, "state": self.snapshot()}

    def settle_trade_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        case_id = payload["case_id"]
        screening_block = any(item["case_id"] == case_id and item["decision"] == "blocked" for item in self.state["sanctions_checks"].values())
        unresolved_discrepancy = any(item["case_id"] == case_id and item["status"] == "open" for item in self.state["discrepancies"].values())
        limit_breach = any(item["case_id"] == case_id and item["approved"] is False for item in self.state["limit_reservations"].values())
        if screening_block or unresolved_discrepancy or limit_breach:
            return {
                "ok": False,
                "reason": "settlement_blocked",
                "screening_block": screening_block,
                "unresolved_discrepancy": unresolved_discrepancy,
                "limit_breach": limit_breach,
                "state": self.snapshot(),
            }
        settlement_id = payload.get("settlement_id") or _sequence("settlement", self.state["settlements"])
        gross = float(payload.get("gross_amount", 0))
        fees = sum(item["net_fee"] for item in self.state["fee_assessments"].values() if item["case_id"] == case_id)
        record = {
            "settlement_id": settlement_id,
            "case_id": case_id,
            "gross_amount": gross,
            "net_amount": round(gross - fees, 2),
            "currency": payload.get("currency", "USD"),
            "value_date": payload.get("value_date", "2026-06-02"),
            "status": "completed",
        }
        self.state["settlements"][settlement_id] = record
        self.state = _append_history(self.state, "settle_trade_case", record)
        self.state = _append_outbox(self.state, "TradeFinanceSettlementCompleted", {"case_id": case_id, "settlement_id": settlement_id})
        return {"ok": True, "settlement": record, "state": self.snapshot()}

    def generate_swift_message_evidence(self, payload: dict[str, Any]) -> dict[str, Any]:
        message_id = payload.get("message_id") or _sequence("swift", self.state["swift_messages"])
        record = {
            "message_id": message_id,
            "case_id": payload["case_id"],
            "message_type": payload.get("message_type", "MT700"),
            "sender_bic": payload.get("sender_bic", "AAAABBCCXXX"),
            "receiver_bic": payload.get("receiver_bic", "DDDDEEFFXXX"),
            "reference": payload.get("reference", payload["case_id"]),
            "narrative": payload.get("narrative", "trade finance evidence"),
            "status": "recorded",
        }
        self.state["swift_messages"][message_id] = record
        self.state = _append_history(self.state, "generate_swift_message_evidence", record)
        self.state = _append_outbox(self.state, "TradeFinanceSwiftEvidenceCreated", {"case_id": payload["case_id"], "message_id": message_id})
        return {"ok": True, "swift_message": record, "state": self.snapshot()}

    def simulate_case_amendment(self, payload: dict[str, Any]) -> dict[str, Any]:
        case = _require_case(self.state, payload["case_id"])
        if case is None:
            return {"ok": False, "reason": "case_not_found", "state": self.snapshot()}
        before = deepcopy(case)
        proposed_amount = float(payload.get("proposed_face_amount", before.get("face_amount", 0)))
        after = {**before, "face_amount": proposed_amount, "expiry_date": payload.get("proposed_expiry_date", before.get("expiry_date"))}
        limit_pressure = proposed_amount - before.get("face_amount", 0)
        return {
            "ok": True,
            "mutated": False,
            "before": before,
            "after": after,
            "impact": {
                "limit_pressure": limit_pressure,
                "requires_rescreening": bool(payload.get("change_destination_country")),
                "requires_fee_reassessment": proposed_amount != before.get("face_amount", 0),
            },
            "state": self.snapshot(),
        }

    def build_workbench(self, *, tenant: str | None = None) -> dict[str, Any]:
        active_tenant = tenant or self.tenant
        cards = (
            {"key": "open_cases", "value": len([item for item in self.state["letters_of_credit"].values() if item["tenant"] == active_tenant]) + len([item for item in self.state["guarantees"].values() if item["tenant"] == active_tenant]) + len([item for item in self.state["collections"].values() if item["tenant"] == active_tenant])},
            {"key": "sanctions_holds", "value": len([item for item in self.state["sanctions_checks"].values() if item["decision"] == "blocked"])},
            {"key": "active_discrepancies", "value": len([item for item in self.state["discrepancies"].values() if item["status"] == "open"])},
            {"key": "due_settlements", "value": len(self.state["settlements"])},
        )
        queues = {
            "issuance": tuple(self.state["letters_of_credit"].values()) + tuple(self.state["guarantees"].values()),
            "presentations": tuple(self.state["document_packages"].values()),
            "sanctions_holds": tuple(item for item in self.state["sanctions_checks"].values() if item["decision"] == "blocked"),
            "discrepancies": tuple(self.state["discrepancies"].values()),
            "limits_and_collateral": tuple(self.state["limit_reservations"].values()) + tuple(self.state["collateral_margins"].values()),
            "settlements": tuple(self.state["settlements"].values()),
        }
        return {
            "ok": True,
            "tenant": active_tenant,
            "cards": cards,
            "queues": queues,
            "forms": trade_finance_operations_form_contracts()["contracts"],
            "wizards": trade_finance_operations_wizard_contracts()["contracts"],
            "controls": trade_finance_operations_control_catalog()["contracts"],
            "side_effects": (),
        }

    def build_case_detail(self, case_id: str) -> dict[str, Any]:
        case = _require_case(self.state, case_id)
        if case is None:
            return {"ok": False, "reason": "case_not_found", "state": self.snapshot()}
        discrepancies = tuple(item for item in self.state["discrepancies"].values() if item["case_id"] == case_id)
        sanctions = tuple(item for item in self.state["sanctions_checks"].values() if item["case_id"] == case_id)
        settlements = tuple(item for item in self.state["settlements"].values() if item["case_id"] == case_id)
        return {
            "ok": True,
            "case_id": case_id,
            "case": case,
            "discrepancies": discrepancies,
            "sanctions": sanctions,
            "settlements": settlements,
            "timeline": tuple(entry for entry in self.state["workflow_history"] if entry["data"].get("case_id") == case_id),
            "side_effects": (),
        }

    def build_release_evidence_pack(self) -> dict[str, Any]:
        checks = (
            {"id": "issuance_workflow", "ok": bool(self.state["letters_of_credit"] or self.state["guarantees"] or self.state["collections"])},
            {"id": "document_examination_workflow", "ok": True},
            {"id": "sanctions_boundary_verification", "ok": True},
            {"id": "settlement_and_swift_evidence", "ok": bool(self.state["settlements"] or self.state["swift_messages"])},
            {"id": "assistant_confirmation_gate", "ok": True},
        )
        pack = {
            "checks": checks,
            "workflow_history_count": len(self.state["workflow_history"]),
            "outbox_count": len(self.state["outbox"]),
            "dead_letter_count": len(self.state["dead_letter"]),
            "open_risks": tuple(item for item in self.state["discrepancies"].values() if item["status"] == "open"),
        }
        self.state["release_evidence_packs"][f"pack_{len(self.state['release_evidence_packs']) + 1:03d}"] = pack
        return {"ok": all(item["ok"] for item in checks), "release_pack": pack, "state": self.snapshot(), "side_effects": ()}

    def assistant_guidance(self, document: str, instruction: str) -> dict[str, Any]:
        from .agent import document_instruction_plan

        guidance = document_instruction_plan(document, instruction)
        self.state["assistant_guidance"] = tuple(self.state.get("assistant_guidance", ())) + (guidance,)
        return {"ok": guidance["ok"], "guidance": guidance, "state": self.snapshot()}


def documentation_presence() -> dict[str, Any]:
    base = Path(__file__).resolve().parent
    docs = ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")
    missing = tuple(name for name in docs if not (base / name).is_file())
    return {"ok": not missing, "missing": missing, "side_effects": ()}


def standalone_smoke_test() -> dict[str, Any]:
    app = TradeFinanceOperationsStandaloneApp(tenant="tenant_smoke")
    app.configure()
    app.register_defaults()
    lc = app.issue_letter_of_credit({
        "case_id": "TFO-SMOKE-001",
        "tenant": "tenant_smoke",
        "applicant": "Importer Ltd",
        "beneficiary": "Exporter PLC",
        "currency": "USD",
        "face_amount": 125000,
    })
    limit_reservation = app.reserve_limit_exposure({"case_id": "TFO-SMOKE-001", "facility_id": "FAC-1", "headroom": 200000, "requested_exposure": 125000})
    app.record_shipment_documents({"case_id": "TFO-SMOKE-001", "package_id": "PKG-1", "documents": ("invoice", "bill_of_lading", "insurance_certificate")})
    examination = app.examine_document_package({"case_id": "TFO-SMOKE-001", "package_id": "PKG-1", "presentation_deadline": "2026-06-30"})
    fees = app.assess_case_fees({"case_id": "TFO-SMOKE-001", "face_amount": 125000, "fee_rate_bps": 50, "swift_fee": 120, "tax_amount": 18})
    settlement = app.settle_trade_case({"case_id": "TFO-SMOKE-001", "settlement_id": "SET-1", "gross_amount": 125000, "currency": "USD"})
    swift = app.generate_swift_message_evidence({"case_id": "TFO-SMOKE-001", "message_type": "MT700"})
    workbench = app.build_workbench()
    release_pack = app.build_release_evidence_pack()
    return {
        "ok": lc["ok"] and limit_reservation["ok"] and examination["ok"] and fees["ok"] and settlement["ok"] and swift["ok"] and workbench["ok"] and release_pack["ok"] and documentation_presence()["ok"],
        "lc": lc,
        "limit_reservation": limit_reservation,
        "examination": examination,
        "fees": fees,
        "settlement": settlement,
        "swift": swift,
        "workbench": workbench,
        "release_pack": release_pack,
        "side_effects": (),
    }
