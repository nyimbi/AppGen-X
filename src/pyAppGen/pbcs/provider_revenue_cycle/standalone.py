"""Standalone single-PBC application surface for provider_revenue_cycle."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import runtime

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "workbench_limit": 50,
    "statement_cycle_days": 30,
    "appeal_deadline_warning_days": 7,
    "stream_engine_picker_visible": False,
}
DEFAULT_PARAMETERS = {
    "workbench_limit": 50,
    "materiality_threshold": 5.0,
    "timely_filing_warning_days": 12,
    "claim_scrub_warning_limit": 3,
    "underpayment_variance_threshold": 5.0,
    "patient_statement_cycle_days": 30,
    "collections_hold_days": 30,
    "appeal_deadline_warning_days": 7,
    "default_payment_plan_term_months": 12,
    "charity_auto_hold_threshold": 500.0,
}
DEFAULT_RULES = (
    {
        "rule_id": "patient_account_policy",
        "rule_type": "registration_gate",
        "status": "active",
        "required_fields": ("patient_id", "guarantor", "coverage_priority", "financial_class"),
    },
    {
        "rule_id": "claim_scrub_policy",
        "rule_type": "claim_scrub",
        "status": "active",
        "fatal_requirements": ("eligibility", "coding", "charges", "payer_contract"),
    },
    {
        "rule_id": "patient_balance_policy",
        "rule_type": "patient_balance_protection",
        "status": "active",
        "prevent_collections_when": ("active_dispute", "assistance_pending", "assistance_approved"),
    },
    {
        "rule_id": "reconciliation_policy",
        "rule_type": "close_gate",
        "status": "active",
        "requires_zero_open_variance": True,
    },
)
DEFAULT_GOVERNED_MODELS = (
    {
        "model_id": "provider_revenue_cycle_denial_risk_model",
        "model_purpose": "Predict preventable denial risk",
        "status": "active",
        "approval_state": "approved",
    },
    {
        "model_id": "provider_revenue_cycle_underpayment_model",
        "model_purpose": "Explain underpayment recovery priority",
        "status": "active",
        "approval_state": "approved",
    },
)
DEFAULT_CONTROLS = (
    {
        "control_id": "registration_readiness_gate",
        "control_family": "front_end_revenue_integrity",
        "severity": "high",
        "status": "active",
    },
    {
        "control_id": "claim_scrub_fatal_gate",
        "control_family": "clean_claim",
        "severity": "critical",
        "status": "active",
    },
    {
        "control_id": "patient_protection_hold",
        "control_family": "patient_billing_protection",
        "severity": "high",
        "status": "active",
    },
)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _now_hint(prefix: str, existing: dict[str, Any]) -> str:
    return f"{prefix}_{len(existing) + 1:05d}"


def _append_event(app: "ProviderRevenueCycleStandaloneApplication", event_type: str, payload: dict[str, Any]) -> None:
    app.state = runtime.append_outbox_event(app.state, event_type, payload)


def _append_audit(app: "ProviderRevenueCycleStandaloneApplication", entry_type: str, payload: dict[str, Any]) -> None:
    app.state = runtime.append_audit_log(app.state, entry_type, payload)


class ProviderRevenueCycleStandaloneApplication:
    """Executable one-PBC provider revenue cycle application."""

    def __init__(self, tenant: str = "default") -> None:
        self.tenant = tenant
        self.state = runtime.provider_revenue_cycle_empty_state()

    def configure(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        result = runtime.provider_revenue_cycle_configure_runtime(self.state, {**DEFAULT_CONFIGURATION, **_copy_payload(config)})
        self.state = result["state"]
        return {"ok": result["ok"], "configuration": result["configuration"], "side_effects": ()}

    def register_defaults(self) -> dict[str, Any]:
        for name, value in DEFAULT_PARAMETERS.items():
            result = runtime.provider_revenue_cycle_set_parameter(self.state, name, value)
            self.state = result["state"]
        for rule in DEFAULT_RULES:
            result = runtime.provider_revenue_cycle_register_rule(self.state, rule)
            self.state = result["state"]
        self.state["governed_models"] = {
            model["model_id"]: deepcopy(model)
            for model in DEFAULT_GOVERNED_MODELS
        }
        self.state["control_assertions"] = {
            control["control_id"]: deepcopy(control)
            for control in DEFAULT_CONTROLS
        }
        return {"ok": True, "parameters": deepcopy(self.state["parameters"]), "rules": deepcopy(self.state["rules"]), "side_effects": ()}

    def intake_patient_account(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        account_id = supplied.get("account_id") or _now_hint("acct", self.state["accounts"])
        readiness_gaps = []
        for field in ("patient_id", "encounter_id", "coverage_priority", "financial_class"):
            if not supplied.get(field):
                readiness_gaps.append(field)
        account = {
            "account_id": account_id,
            "tenant": supplied.get("tenant", self.tenant),
            "patient_id": supplied.get("patient_id"),
            "encounter_id": supplied.get("encounter_id"),
            "registration_status": supplied.get("registration_status", "registered"),
            "account_state": "registered" if not readiness_gaps else "registration_deficient",
            "coverage_priority": supplied.get("coverage_priority"),
            "financial_class": supplied.get("financial_class"),
            "guarantor": supplied.get("guarantor", {}),
            "eligibility_status": "pending",
            "authorization_status": "pending",
            "charge_status": "pending",
            "coding_status": "pending",
            "claim_status": "pending",
            "days_in_ar": int(supplied.get("days_in_ar", 0)),
            "patient_balance": float(supplied.get("patient_balance", 0.0)),
            "readiness_gaps": tuple(readiness_gaps),
            "claims": (),
            "authorizations": (),
            "notes": tuple(supplied.get("notes", ())),
        }
        self.state["accounts"][account_id] = account
        self.state["records"][account_id] = deepcopy(account)
        _append_audit(self, "patient_account_intake", {"account_id": account_id, "readiness_gaps": readiness_gaps})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[0], {"entity": "patient_account", "account_id": account_id})
        return {"ok": True, "account": deepcopy(account), "side_effects": ()}

    def review_eligibility_and_benefits(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        account = deepcopy(self.state["accounts"][account_id])
        eligibility = {
            "payer_id": payload.get("payer_id", "payer_unknown"),
            "coverage_active": bool(payload.get("coverage_active", False)),
            "benefit_summary": payload.get("benefit_summary", ""),
            "patient_responsibility_estimate": float(payload.get("patient_responsibility_estimate", 0.0)),
            "freshness_hours": int(payload.get("freshness_hours", 2)),
            "response_time_ms": int(payload.get("response_time_ms", 250)),
        }
        account["eligibility"] = eligibility
        account["eligibility_status"] = "verified" if eligibility["coverage_active"] else "inactive"
        account["patient_balance"] = eligibility["patient_responsibility_estimate"]
        if eligibility["coverage_active"]:
            account["readiness_gaps"] = tuple(gap for gap in account["readiness_gaps"] if gap != "eligibility")
        self.state["accounts"][account_id] = account
        _append_audit(self, "eligibility_benefits_review", {"account_id": account_id, "eligibility_status": account["eligibility_status"]})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[1], {"entity": "eligibility", "account_id": account_id})
        return {"ok": True, "account": deepcopy(account), "eligibility": deepcopy(eligibility), "side_effects": ()}

    def link_prior_authorization(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        account = deepcopy(self.state["accounts"][account_id])
        authorization = {
            "authorization_id": payload.get("authorization_id") or _now_hint("auth", {item["authorization_id"]: item for item in account.get("authorizations", ())}),
            "service_code": payload.get("service_code"),
            "status": payload.get("status", "submitted"),
            "units_remaining": int(payload.get("units_remaining", 0)),
            "validity_end": payload.get("validity_end"),
        }
        account["authorizations"] = tuple(account.get("authorizations", ())) + (authorization,)
        account["authorization_status"] = "approved" if authorization["status"] == "approved" else authorization["status"]
        self.state["accounts"][account_id] = account
        _append_audit(self, "prior_authorization_link", {"account_id": account_id, "authorization_id": authorization["authorization_id"]})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[1], {"entity": "prior_authorization", "account_id": account_id})
        return {"ok": True, "authorization": deepcopy(authorization), "account": deepcopy(account), "side_effects": ()}

    def capture_charge(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        charge_id = supplied.get("charge_id") or _now_hint("chg", self.state["charges"])
        expected_amount = float(supplied.get("expected_amount", 0.0))
        captured_amount = float(supplied.get("captured_amount", 0.0))
        charge = {
            "charge_id": charge_id,
            "account_id": account_id,
            "tenant": supplied.get("tenant", self.tenant),
            "service_date": supplied.get("service_date"),
            "charge_code": supplied.get("charge_code"),
            "department": supplied.get("department"),
            "performing_clinician": supplied.get("performing_clinician"),
            "expected_amount": expected_amount,
            "captured_amount": captured_amount,
            "variance_amount": round(captured_amount - expected_amount, 2),
            "status": "captured" if captured_amount else "missing",
        }
        self.state["charges"][charge_id] = charge
        account = deepcopy(self.state["accounts"][account_id])
        account["charge_status"] = "captured" if captured_amount else "missing"
        self.state["accounts"][account_id] = account
        _append_audit(self, "charge_capture", {"account_id": account_id, "charge_id": charge_id, "variance": charge["variance_amount"]})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[1], {"entity": "charge_capture", "charge_id": charge_id})
        return {"ok": True, "charge": deepcopy(charge), "side_effects": ()}

    def review_coding(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        case_id = supplied.get("coding_case_id") or _now_hint("coding", self.state["coding_cases"])
        case = {
            "coding_case_id": case_id,
            "account_id": account_id,
            "tenant": supplied.get("tenant", self.tenant),
            "case_type": supplied.get("case_type", "professional"),
            "documentation_status": supplied.get("documentation_status", "missing"),
            "diagnosis_codes": tuple(supplied.get("diagnosis_codes", ())),
            "procedure_codes": tuple(supplied.get("procedure_codes", ())),
            "modifiers": tuple(supplied.get("modifiers", ())),
            "cdi_queries": tuple(supplied.get("cdi_queries", ())),
            "coding_status": "final" if supplied.get("documentation_status") == "complete" and supplied.get("procedure_codes") else "pending",
        }
        self.state["coding_cases"][case_id] = case
        account = deepcopy(self.state["accounts"][account_id])
        account["coding_status"] = case["coding_status"]
        self.state["accounts"][account_id] = account
        _append_audit(self, "coding_review", {"account_id": account_id, "coding_case_id": case_id, "status": case["coding_status"]})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[1], {"entity": "coding_case", "coding_case_id": case_id})
        return {"ok": True, "coding_case": deepcopy(case), "side_effects": ()}

    def upsert_payer_contract(self, payload: dict[str, Any]) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        contract_id = supplied.get("contract_id") or _now_hint("contract", self.state["payer_contracts"])
        contract = {
            "contract_id": contract_id,
            "payer_id": supplied.get("payer_id"),
            "expected_rate": float(supplied.get("expected_rate", 0.0)),
            "timely_filing_days": int(supplied.get("timely_filing_days", 90)),
            "status": supplied.get("status", "active"),
        }
        self.state["payer_contracts"][contract_id] = contract
        _append_audit(self, "payer_contract_edit", {"contract_id": contract_id, "payer_id": contract["payer_id"]})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[1], {"entity": "payer_contract", "contract_id": contract_id})
        return {"ok": True, "contract": deepcopy(contract), "side_effects": ()}

    def _find_account_for_claim(self, claim_id: str) -> str | None:
        claim = self.state["claims"].get(claim_id)
        return claim.get("account_id") if claim else None

    def create_claim(self, account_id: str) -> dict[str, Any]:
        account = deepcopy(self.state["accounts"][account_id])
        contract = next(iter(self.state["payer_contracts"].values()), None)
        claim_id = _now_hint("claim", self.state["claims"])
        charge_lines = tuple(charge for charge in self.state["charges"].values() if charge["account_id"] == account_id)
        coding_case = next((case for case in self.state["coding_cases"].values() if case["account_id"] == account_id), None)
        claim = {
            "claim_id": claim_id,
            "account_id": account_id,
            "tenant": account.get("tenant", self.tenant),
            "charge_ids": tuple(line["charge_id"] for line in charge_lines),
            "coding_case_id": coding_case.get("coding_case_id") if coding_case else None,
            "payer_id": account.get("eligibility", {}).get("payer_id"),
            "expected_reimbursement": float(contract.get("expected_rate", 0.0)) if contract else 0.0,
            "status": "draft",
            "scrub": {"fatal": (), "warning": ()},
        }
        self.state["claims"][claim_id] = claim
        account["claims"] = tuple(account.get("claims", ())) + (claim_id,)
        account["claim_status"] = "created"
        self.state["accounts"][account_id] = account
        _append_audit(self, "claim_create", {"claim_id": claim_id, "account_id": account_id})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[0], {"entity": "claim", "claim_id": claim_id})
        return {"ok": True, "claim": deepcopy(claim), "side_effects": ()}

    def scrub_claim(self, claim_id: str) -> dict[str, Any]:
        claim = deepcopy(self.state["claims"][claim_id])
        account = deepcopy(self.state["accounts"][claim["account_id"]])
        fatal = []
        warning = []
        if account.get("registration_status") != "ready":
            fatal.append("registration_incomplete")
        if account.get("eligibility_status") != "verified":
            fatal.append("eligibility_not_verified")
        if account.get("authorization_status") not in {"approved", "not_required"}:
            fatal.append("authorization_not_ready")
        if account.get("charge_status") != "captured":
            fatal.append("charges_missing")
        if account.get("coding_status") != "final":
            fatal.append("coding_not_final")
        if not self.state["payer_contracts"]:
            fatal.append("payer_contract_missing")
        if account.get("patient_balance", 0.0) > 1000:
            warning.append("high_patient_responsibility")
        claim["scrub"] = {"fatal": tuple(fatal), "warning": tuple(warning)}
        claim["status"] = "scrub_failed" if fatal else "ready_to_submit"
        self.state["claims"][claim_id] = claim
        account["claim_status"] = claim["status"]
        self.state["accounts"][claim["account_id"]] = account
        _append_audit(self, "claim_scrub", {"claim_id": claim_id, "fatal": fatal, "warning": warning})
        return {
            "ok": not fatal,
            "claim": deepcopy(claim),
            "fatal_findings": tuple(fatal),
            "warning_findings": tuple(warning),
            "side_effects": (),
        }

    def submit_claim(self, claim_id: str) -> dict[str, Any]:
        claim = deepcopy(self.state["claims"][claim_id])
        if claim.get("status") != "ready_to_submit":
            return {"ok": False, "reason": "claim_not_ready", "claim": claim, "side_effects": ()}
        batch_id = _now_hint("batch", self.state["claim_batches"])
        batch = {
            "claim_batch_id": batch_id,
            "tenant": claim["tenant"],
            "payer_id": claim.get("payer_id"),
            "batch_type": "professional",
            "account_ids": (claim["account_id"],),
            "claim_ids": (claim_id,),
            "validation_status": "clean",
            "submission_status": "submitted",
            "acknowledgement_status": "accepted",
        }
        self.state["claim_batches"][batch_id] = batch
        claim["status"] = "submitted"
        claim["claim_batch_id"] = batch_id
        self.state["claims"][claim_id] = claim
        account = deepcopy(self.state["accounts"][claim["account_id"]])
        account["claim_status"] = "submitted"
        account["account_state"] = "billed"
        self.state["accounts"][claim["account_id"]] = account
        _append_audit(self, "claim_submit", {"claim_id": claim_id, "batch_id": batch_id})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[2], {"entity": "claim_submission", "claim_id": claim_id, "batch_id": batch_id})
        return {"ok": True, "claim": deepcopy(claim), "batch": deepcopy(batch), "side_effects": ()}

    def open_denial_case(self, claim_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        claim = deepcopy(self.state["claims"][claim_id])
        denial_id = payload.get("denial_case_id") or _now_hint("denial", self.state["denials"])
        denial = {
            "denial_case_id": denial_id,
            "claim_id": claim_id,
            "account_id": claim["account_id"],
            "tenant": claim["tenant"],
            "category": payload.get("category", "medical_necessity"),
            "payer_reason": payload.get("payer_reason", "Unspecified"),
            "root_cause": payload.get("root_cause", "unknown"),
            "preventable": bool(payload.get("preventable", True)),
            "appeal_level": int(payload.get("appeal_level", 0)),
            "status": payload.get("status", "open"),
            "amount": float(payload.get("amount", 0.0)),
        }
        self.state["denials"][denial_id] = denial
        account = deepcopy(self.state["accounts"][claim["account_id"]])
        account["account_state"] = "denied"
        self.state["accounts"][claim["account_id"]] = account
        _append_audit(self, "denial_open", {"claim_id": claim_id, "denial_case_id": denial_id, "category": denial["category"]})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[3], {"entity": "denial", "denial_case_id": denial_id})
        return {"ok": True, "denial": deepcopy(denial), "side_effects": ()}

    def appeal_denial(self, denial_case_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        denial = deepcopy(self.state["denials"][denial_case_id])
        denial["appeal_level"] = int(payload.get("appeal_level", denial.get("appeal_level", 0) + 1))
        denial["packet_complete"] = bool(payload.get("packet_complete", False))
        denial["submission_proof"] = payload.get("submission_proof")
        denial["status"] = "appealed" if denial["packet_complete"] else "appeal_pending"
        self.state["denials"][denial_case_id] = denial
        _append_audit(self, "denial_appeal", {"denial_case_id": denial_case_id, "appeal_level": denial["appeal_level"]})
        return {"ok": True, "denial": deepcopy(denial), "side_effects": ()}

    def detect_underpayment(self, claim_id: str) -> dict[str, Any]:
        claim = deepcopy(self.state["claims"][claim_id])
        postings = [posting for posting in self.state["payment_postings"].values() if posting["claim_id"] == claim_id]
        paid = sum(float(item.get("payment_amount", 0.0)) for item in postings)
        expected = float(claim.get("expected_reimbursement", 0.0))
        variance = round(expected - paid, 2)
        if variance > float(self.state["parameters"].get("underpayment_variance_threshold", {}).get("value", 5.0)):
            denial = self.open_denial_case(
                claim_id,
                {
                    "category": "underpayment",
                    "payer_reason": "Paid below contracted rate",
                    "root_cause": "contract_variance",
                    "preventable": False,
                    "amount": variance,
                },
            )
            return {"ok": True, "variance": variance, "denial": denial["denial"], "side_effects": ()}
        return {"ok": True, "variance": variance, "denial": None, "side_effects": ()}

    def post_remittance_era(self, claim_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        claim = deepcopy(self.state["claims"][claim_id])
        posting_id = payload.get("payment_posting_id") or _now_hint("post", self.state["payment_postings"])
        posting = {
            "payment_posting_id": posting_id,
            "claim_id": claim_id,
            "account_id": claim["account_id"],
            "tenant": claim["tenant"],
            "remittance_source": payload.get("remittance_source", "era"),
            "allowed_amount": float(payload.get("allowed_amount", 0.0)),
            "payment_amount": float(payload.get("payment_amount", 0.0)),
            "adjustment_amount": float(payload.get("adjustment_amount", 0.0)),
            "patient_responsibility_amount": float(payload.get("patient_responsibility_amount", 0.0)),
            "credit_balance_amount": float(payload.get("credit_balance_amount", 0.0)),
            "status": "posted",
        }
        self.state["payment_postings"][posting_id] = posting
        account = deepcopy(self.state["accounts"][claim["account_id"]])
        account["patient_balance"] = round(posting["patient_responsibility_amount"] + posting["credit_balance_amount"], 2)
        account["account_state"] = "patient_balance" if account["patient_balance"] > 0 else "paid"
        self.state["accounts"][claim["account_id"]] = account
        _append_audit(self, "remit_era_posting", {"claim_id": claim_id, "payment_posting_id": posting_id})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[1], {"entity": "payment_posting", "payment_posting_id": posting_id})
        underpayment = self.detect_underpayment(claim_id)
        return {"ok": True, "posting": deepcopy(posting), "underpayment": underpayment, "side_effects": ()}

    def generate_patient_statement(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        account = deepcopy(self.state["accounts"][account_id])
        statement_id = payload.get("statement_id") or _now_hint("stmt", self.state["patient_statements"])
        statement = {
            "statement_id": statement_id,
            "account_id": account_id,
            "patient_balance": account.get("patient_balance", 0.0),
            "delivery_channel": payload.get("delivery_channel", "paper"),
            "status": "issued",
        }
        self.state["patient_statements"][statement_id] = statement
        _append_audit(self, "patient_statement_issue", {"account_id": account_id, "statement_id": statement_id})
        return {"ok": True, "statement": deepcopy(statement), "side_effects": ()}

    def enroll_payment_plan(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        plan_id = payload.get("plan_id") or _now_hint("plan", self.state["payment_plans"])
        plan = {
            "plan_id": plan_id,
            "account_id": account_id,
            "monthly_amount": float(payload.get("monthly_amount", 0.0)),
            "term_months": int(payload.get("term_months", self.state["parameters"].get("default_payment_plan_term_months", {}).get("value", 12))),
            "status": "active",
        }
        self.state["payment_plans"][plan_id] = plan
        collection = self.state["collection_accounts"].get(account_id, {"account_id": account_id})
        collection["payment_plan_status"] = "active"
        collection["collection_hold"] = True
        self.state["collection_accounts"][account_id] = collection
        _append_audit(self, "payment_plan_enroll", {"account_id": account_id, "plan_id": plan_id})
        return {"ok": True, "payment_plan": deepcopy(plan), "side_effects": ()}

    def issue_refund_or_credit(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        refund_id = payload.get("refund_id") or _now_hint("refund", self.state["refunds"])
        if refund_id in self.state["refunds"]:
            return {"ok": False, "reason": "duplicate_refund", "refund_id": refund_id, "side_effects": ()}
        refund = {
            "refund_id": refund_id,
            "account_id": account_id,
            "type": payload.get("type", "refund"),
            "amount": float(payload.get("amount", 0.0)),
            "status": "pending_approval",
        }
        self.state["refunds"][refund_id] = refund
        _append_audit(self, "refund_credit_issue", {"account_id": account_id, "refund_id": refund_id})
        return {"ok": True, "refund": deepcopy(refund), "side_effects": ()}

    def evaluate_financial_assistance(self, account_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        assistance_id = payload.get("assistance_id") or _now_hint("assist", self.state["assistance_cases"])
        assistance = {
            "assistance_id": assistance_id,
            "account_id": account_id,
            "status": payload.get("status", "pending"),
            "discount_percent": float(payload.get("discount_percent", 0.0)),
            "presumptive_eligibility": bool(payload.get("presumptive_eligibility", False)),
        }
        self.state["assistance_cases"][assistance_id] = assistance
        account = deepcopy(self.state["accounts"][account_id])
        if assistance["status"] == "approved":
            account["patient_balance"] = round(account.get("patient_balance", 0.0) * (1 - (assistance["discount_percent"] / 100.0)), 2)
            account["account_state"] = "patient_balance"
        self.state["accounts"][account_id] = account
        collection = self.state["collection_accounts"].get(account_id, {"account_id": account_id})
        collection["assistance_status"] = assistance["status"]
        collection["collection_hold"] = assistance["status"] in {"pending", "approved"}
        self.state["collection_accounts"][account_id] = collection
        _append_audit(self, "financial_assistance", {"account_id": account_id, "assistance_id": assistance_id, "status": assistance["status"]})
        return {"ok": True, "assistance": deepcopy(assistance), "side_effects": ()}

    def build_ar_workqueue(self, tenant: str | None = None) -> dict[str, Any]:
        return runtime.provider_revenue_cycle_build_workbench_view(state=self.state, tenant=tenant or self.tenant)

    def reconcile_close(self, account_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        supplied = _copy_payload(payload)
        account = deepcopy(self.state["accounts"][account_id])
        open_denials = [item for item in self.state["denials"].values() if item["account_id"] == account_id and item["status"] not in {"closed", "resolved"}]
        if open_denials:
            return {"ok": False, "reason": "open_denials", "denials": deepcopy(open_denials), "side_effects": ()}
        if float(account.get("patient_balance", 0.0)) > 0 and supplied.get("expected_close_state") != "approved_writeoff":
            return {"ok": False, "reason": "open_patient_balance", "patient_balance": account["patient_balance"], "side_effects": ()}
        account["account_state"] = "closed"
        self.state["accounts"][account_id] = account
        _append_audit(self, "reconcile_close", {"account_id": account_id, "reconciled_by": supplied.get("reconciled_by")})
        _append_event(self, runtime.PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[2], {"entity": "close", "account_id": account_id})
        return {"ok": True, "account": deepcopy(account), "side_effects": ()}

    def account_snapshot(self, account_id: str) -> dict[str, Any]:
        account = deepcopy(self.state["accounts"][account_id])
        claims = tuple(self.state["claims"][claim_id] for claim_id in account.get("claims", ()) if claim_id in self.state["claims"])
        denials = tuple(item for item in self.state["denials"].values() if item["account_id"] == account_id)
        return {
            "ok": True,
            "account": account,
            "claims": deepcopy(claims),
            "denials": deepcopy(denials),
            "charges": tuple(deepcopy(item) for item in self.state["charges"].values() if item["account_id"] == account_id),
            "payment_postings": tuple(deepcopy(item) for item in self.state["payment_postings"].values() if item["account_id"] == account_id),
            "payment_plans": tuple(deepcopy(item) for item in self.state["payment_plans"].values() if item["account_id"] == account_id),
            "refunds": tuple(deepcopy(item) for item in self.state["refunds"].values() if item["account_id"] == account_id),
            "assistance_cases": tuple(deepcopy(item) for item in self.state["assistance_cases"].values() if item["account_id"] == account_id),
            "side_effects": (),
        }

    def assistant_preview(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        from .agent import provider_revenue_cycle_assistant_preview

        return provider_revenue_cycle_assistant_preview(payload or {})


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": runtime.PBC_KEY,
        "app_class": "ProviderRevenueCycleStandaloneApplication",
        "implementation_directory": "src/pyAppGen/pbcs/provider_revenue_cycle",
        "service_methods": (
            "configure",
            "register_defaults",
            "intake_patient_account",
            "review_eligibility_and_benefits",
            "link_prior_authorization",
            "capture_charge",
            "review_coding",
            "upsert_payer_contract",
            "create_claim",
            "scrub_claim",
            "submit_claim",
            "post_remittance_era",
            "open_denial_case",
            "appeal_denial",
            "detect_underpayment",
            "generate_patient_statement",
            "enroll_payment_plan",
            "issue_refund_or_credit",
            "evaluate_financial_assistance",
            "build_ar_workqueue",
            "reconcile_close",
            "account_snapshot",
            "assistant_preview",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench", "assistant"),
        "docs": ("SPECIFICATION.md", "improve1.md", "RELEASE_EVIDENCE.md"),
        "event_contract": "AppGen-X",
        "event_topic": runtime.PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": runtime.PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
    }


def documentation_presence() -> dict[str, Any]:
    docs_base = Path(__file__).resolve().parent
    docs = tuple(
        {
            "path": name,
            "exists": (docs_base / name).exists(),
        }
        for name in standalone_manifest()["docs"]
    )
    return {"ok": all(item["exists"] for item in docs), "docs": docs, "side_effects": ()}


def standalone_smoke_test() -> dict[str, Any]:
    app = ProviderRevenueCycleStandaloneApplication(tenant="tenant_alpha")
    app.configure()
    app.register_defaults()
    account = app.intake_patient_account(
        {
            "tenant": "tenant_alpha",
            "account_id": "acct_100",
            "patient_id": "patient_100",
            "encounter_id": "enc_100",
            "registration_status": "ready",
            "coverage_priority": "primary",
            "financial_class": "commercial",
            "guarantor": {"name": "Ada Guarantor"},
        }
    )
    eligibility = app.review_eligibility_and_benefits(
        "acct_100",
        {
            "payer_id": "payer_alpha",
            "coverage_active": True,
            "benefit_summary": "Office visit and labs covered",
            "patient_responsibility_estimate": 100.0,
        },
    )
    authorization = app.link_prior_authorization(
        "acct_100",
        {"authorization_id": "auth_100", "service_code": "99213", "status": "approved", "units_remaining": 4},
    )
    charge = app.capture_charge(
        "acct_100",
        {
            "charge_id": "chg_100",
            "service_date": "2026-05-30",
            "charge_code": "99213",
            "expected_amount": 180.0,
            "captured_amount": 180.0,
            "department": "clinic",
            "performing_clinician": "dr_smith",
        },
    )
    coding = app.review_coding(
        "acct_100",
        {
            "coding_case_id": "coding_100",
            "case_type": "professional",
            "documentation_status": "complete",
            "diagnosis_codes": ("I10",),
            "procedure_codes": ("99213",),
            "modifiers": ("25",),
        },
    )
    contract = app.upsert_payer_contract({"contract_id": "contract_100", "payer_id": "payer_alpha", "expected_rate": 150.0, "timely_filing_days": 90})
    claim = app.create_claim("acct_100")
    scrub = app.scrub_claim(claim["claim"]["claim_id"])
    submitted = app.submit_claim(claim["claim"]["claim_id"])
    remit = app.post_remittance_era(
        claim["claim"]["claim_id"],
        {
            "payment_posting_id": "post_100",
            "allowed_amount": 150.0,
            "payment_amount": 140.0,
            "adjustment_amount": 10.0,
            "patient_responsibility_amount": 20.0,
        },
    )
    denial = app.detect_underpayment(claim["claim"]["claim_id"])
    statement = app.generate_patient_statement("acct_100", {"statement_id": "stmt_100"})
    plan = app.enroll_payment_plan("acct_100", {"plan_id": "plan_100", "monthly_amount": 10.0, "term_months": 2})
    assistance = app.evaluate_financial_assistance("acct_100", {"assistance_id": "assist_100", "status": "approved", "discount_percent": 50.0})
    refund = app.issue_refund_or_credit("acct_100", {"refund_id": "refund_100", "type": "credit_balance", "amount": 5.0})
    snapshot = app.account_snapshot("acct_100")
    workbench = app.build_ar_workqueue("tenant_alpha")
    preview = app.assistant_preview({"document_text": "Please update the claim scrub rule", "instructions": "update the payer contract threshold", "requested_action": "update"})
    return {
        "ok": account["ok"]
        and eligibility["ok"]
        and authorization["ok"]
        and charge["ok"]
        and coding["ok"]
        and contract["ok"]
        and claim["ok"]
        and scrub["ok"]
        and submitted["ok"]
        and remit["ok"]
        and denial["ok"]
        and statement["ok"]
        and plan["ok"]
        and assistance["ok"]
        and refund["ok"]
        and snapshot["ok"]
        and workbench["ok"]
        and preview["ok"],
        "manifest": standalone_manifest(),
        "state": deepcopy(app.state),
        "workbench": workbench,
        "snapshot": snapshot,
        "preview": preview,
        "side_effects": (),
    }
