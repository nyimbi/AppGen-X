"""Standalone one-PBC application surface for insurance_claims_policy."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from typing import Any

from . import config
from . import events
from . import handlers
from .domain_depth import DOMAIN_OPERATIONS
from .models import MODEL_BY_LOGICAL_TABLE
from .models import OWNED_TABLES
from .permissions import PERMISSIONS

PBC_KEY = "insurance_claims_policy"

SECTION_BY_LOGICAL = {
    "insurance_policy": "insurance_policies",
    "policy_holder": "policy_holders",
    "policy_coverage": "policy_coverages",
    "policy_endorsement": "policy_endorsements",
    "premium_schedule": "premium_schedules",
    "premium_payment": "premium_payments",
    "claim_record": "claim_records",
    "loss_event": "loss_events",
    "claimant": "claimants",
    "claim_document": "claim_documents",
    "coverage_determination": "coverage_determinations",
    "claim_reserve": "claim_reserves",
    "reserve_change": "reserve_changes",
    "claim_adjudication": "claim_adjudications",
    "settlement_offer": "settlement_offers",
    "settlement_payment": "settlement_payments",
    "subrogation_recovery": "subrogation_recoveries",
    "claim_communication": "claim_communications",
    "fraud_indicator": "fraud_indicators",
    "claim_exception_case": "claim_exception_cases",
    "insurance_policy_rule": "rules",
    "insurance_runtime_parameter": "parameters",
    "insurance_schema_extension": "schema_extensions",
    "insurance_control_assertion": "control_assertions",
    "insurance_governed_model": "governed_models",
}

DEFAULT_STATE = {
    "configuration": {},
    "parameters": {},
    "rules": {},
    "schema_extensions": {},
    "control_assertions": {},
    "governed_models": {},
    "insurance_policies": {},
    "policy_holders": {},
    "policy_coverages": {},
    "policy_endorsements": {},
    "premium_schedules": {},
    "premium_payments": {},
    "claim_records": {},
    "loss_events": {},
    "claimants": {},
    "claim_documents": {},
    "coverage_determinations": {},
    "claim_reserves": {},
    "reserve_changes": {},
    "claim_adjudications": {},
    "settlement_offers": {},
    "settlement_payments": {},
    "subrogation_recoveries": {},
    "claim_communications": {},
    "fraud_indicators": {},
    "claim_exception_cases": {},
    "workflows": {},
    "outbox": (),
    "inbox": (),
    "dead_letters": (),
    "handled_events": {},
    "audit_traces": (),
}

DEFAULT_RULES = config.rule_defaults()
DEFAULT_PARAMETERS = config.parameter_defaults()
DEFAULT_CONFIGURATION = deepcopy(config.DEFAULT_CONFIGURATION)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _ensure_state(state: dict[str, Any] | None) -> dict[str, Any]:
    enriched = deepcopy(state or {})
    for key, default in DEFAULT_STATE.items():
        if key not in enriched:
            enriched[key] = deepcopy(default)
    return enriched


def _sequence_id(prefix: str, existing: dict[str, Any] | tuple[Any, ...]) -> str:
    return f"{prefix}_{len(existing) + 1:05d}"


def _timestamp(collection_size: int) -> str:
    minute = collection_size % 60
    return f"2026-05-30T00:{minute:02d}:00Z"


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _append_audit_trace(state: dict[str, Any], *, aggregate_id: str | None, action: str, data: dict[str, Any]) -> dict[str, Any]:
    traces = tuple(state.get("audit_traces", ()))
    entry = {
        "trace_id": _sequence_id("trace", traces),
        "aggregate_id": aggregate_id,
        "action": action,
        "data": deepcopy(data),
    }
    return {**state, "audit_traces": (*traces, entry)}


def _emit(state: dict[str, Any], event_type: str, *, aggregate_id: str, tenant: str, payload: dict[str, Any]) -> dict[str, Any]:
    outbox = tuple(state.get("outbox", ()))
    envelope = events.build_event_envelope(event_type, payload, aggregate_id=aggregate_id, tenant=tenant)
    return {**state, "outbox": (*outbox, envelope)}


def _store(state: dict[str, Any], section: str, record_id: str, record: dict[str, Any]) -> dict[str, Any]:
    bucket = deepcopy(state.get(section, {}))
    bucket[record_id] = record
    return {**state, section: bucket}


def _require(section: dict[str, Any], record_id: str, reason: str) -> dict | None:
    if record_id not in section:
        return {"ok": False, "reason": reason, "missing_id": record_id, "side_effects": ()}
    return None


def _policy_premium_current(state: dict[str, Any], policy_id: str) -> bool:
    policy = state.get("insurance_policies", {}).get(policy_id, {})
    if policy.get("premium_status") == "current":
        return True
    payments = tuple(payment for payment in state.get("premium_payments", {}).values() if payment["policy_id"] == policy_id)
    return bool(payments and payments[-1].get("payment_status") == "captured")


def _coverage_match(state: dict[str, Any], policy_id: str, peril_code: str | None) -> dict | None:
    for coverage in state.get("policy_coverages", {}).values():
        if coverage["policy_id"] == policy_id and coverage["peril_code"] == peril_code:
            return coverage
    return None


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_class": "InsuranceClaimsPolicyStandaloneApp",
        "implementation_directory": "src/pyAppGen/pbcs/insurance_claims_policy",
        "service_methods": (
            "configure",
            "register_defaults",
            "create_insurance_policy",
            "register_policy_holder",
            "define_policy_coverage",
            "record_endorsement",
            "create_premium_schedule",
            "record_premium_payment",
            "open_claim",
            "record_loss_event",
            "register_claimant",
            "attach_claim_document",
            "determine_coverage",
            "set_claim_reserve",
            "record_reserve_change",
            "adjudicate_claim",
            "create_settlement_offer",
            "execute_settlement_payment",
            "record_subrogation_recovery",
            "send_claim_communication",
            "score_fraud_indicator",
            "resolve_claim_exception",
            "compile_insurance_rule",
            "simulate_loss_exposure",
            "receive_event",
            "document_intake",
            "crud_mutation_plan",
            "get_policy_snapshot",
            "get_claim_snapshot",
            "workbench",
            "release_snapshot",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
        "workflows": (
            "policy_issuance_readiness",
            "claim_fnol_triage",
            "coverage_reasoning",
            "reserve_management",
            "fraud_escalation",
            "settlement_execution",
            "subrogation_tracking",
        ),
        "docs": ("README.md", "implementation-status.md", "RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
        "event_contract": "AppGen-X",
        "event_topic": config.REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": config.ALLOWED_DATABASE_BACKENDS,
        "owned_tables": OWNED_TABLES,
    }


class InsuranceClaimsPolicyStandaloneApp:
    def __init__(self, state: dict[str, Any] | None = None):
        self.state = _ensure_state(state)

    def configure(self, configuration: dict | None = None) -> dict:
        validation = config.validate_configuration(configuration)
        if validation["ok"]:
            self.state = {**self.state, "configuration": validation["config"]}
        return {"ok": validation["ok"], "configuration": validation["config"], "state": self.state, "side_effects": ()}

    def set_parameter(self, name: str, value) -> dict:
        result = config.set_parameter(self.state, name, value)
        if result["ok"]:
            self.state = {**self.state, "parameters": result["parameters"]}
        return {"ok": result["ok"], "parameter": result.get("parameter"), "state": self.state, "side_effects": ()}

    def register_rule(self, rule: dict) -> dict:
        compiled = config.compile_rule(rule)
        if not compiled["ok"]:
            return {"ok": False, "reason": compiled["reason"], "state": self.state, "side_effects": ()}
        rules = deepcopy(self.state.get("rules", {}))
        rules[compiled["rule"]["rule_id"]] = compiled["rule"]
        self.state = {**self.state, "rules": rules}
        self.state = _append_audit_trace(self.state, aggregate_id=compiled["rule"]["rule_id"], action="register_rule", data=compiled["rule"])
        return {"ok": True, "rule": compiled["rule"], "state": self.state, "side_effects": ()}

    def register_schema_extension(self, extension: dict) -> dict:
        target_table = extension.get("target_table")
        if target_table not in OWNED_TABLES:
            return {"ok": False, "reason": "unknown_owned_table", "table": target_table, "state": self.state, "side_effects": ()}
        extension_id = extension.get("extension_id") or _sequence_id("schema_extension", self.state["schema_extensions"])
        record = {
            "id": extension_id,
            "tenant": extension.get("tenant", "default"),
            "code": extension.get("code", extension_id),
            "status": extension.get("approval_status", "proposed"),
            "version": 1,
            "target_table": target_table,
            "extension_key": extension.get("extension_key", "custom"),
            "approval_status": extension.get("approval_status", "proposed"),
            "extension_payload": _copy_payload(extension.get("extension_payload", {})),
            "payload": _copy_payload(extension),
            "effective_at": extension.get("effective_at"),
            "created_at": _timestamp(len(self.state["schema_extensions"])),
            "updated_at": _timestamp(len(self.state["schema_extensions"]) + 1),
        }
        self.state = _store(self.state, "schema_extensions", extension_id, record)
        return {"ok": True, "schema_extension": record, "state": self.state, "side_effects": ()}

    def register_defaults(self, *, tenant: str = "tenant_demo") -> dict:
        self.configure(DEFAULT_CONFIGURATION)
        for name, value in DEFAULT_PARAMETERS.items():
            self.set_parameter(name, value)
        for rule in DEFAULT_RULES:
            self.register_rule({**rule, "tenant": tenant})
        control_id = _sequence_id("control", self.state["control_assertions"])
        control = {
            "id": control_id,
            "tenant": tenant,
            "code": control_id,
            "status": "passing",
            "version": 1,
            "control_name": "release_readiness_gate",
            "control_status": "passing",
            "last_checked_at": _timestamp(len(self.state["control_assertions"])),
            "evidence_ref": "release-evidence",
            "payload": {"checks": ("coverage", "reserve", "settlement")},
            "effective_at": None,
            "created_at": _timestamp(len(self.state["control_assertions"])),
            "updated_at": _timestamp(len(self.state["control_assertions"]) + 1),
        }
        self.state = _store(self.state, "control_assertions", control_id, control)
        model_id = _sequence_id("model", self.state["governed_models"])
        model = {
            "id": model_id,
            "tenant": tenant,
            "code": model_id,
            "status": "approved",
            "version": 1,
            "model_name": "claims_triage_assistant",
            "model_purpose": "severity_and_fraud_triage",
            "model_version": "v1",
            "approval_status": "approved",
            "payload": {"explainable": True},
            "effective_at": None,
            "created_at": _timestamp(len(self.state["governed_models"])),
            "updated_at": _timestamp(len(self.state["governed_models"]) + 1),
        }
        self.state = _store(self.state, "governed_models", model_id, model)
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def create_insurance_policy(self, policy: dict) -> dict:
        policy_id = policy.get("policy_id") or _sequence_id("policy", self.state["insurance_policies"])
        record = {
            "id": policy_id,
            "tenant": policy.get("tenant", "default"),
            "code": policy.get("policy_number", policy_id),
            "status": policy.get("status", "issued"),
            "version": 1,
            "policy_number": policy.get("policy_number", policy_id),
            "product_code": policy.get("product_code", "commercial_property"),
            "policy_state": policy.get("policy_state", "bound"),
            "premium_status": policy.get("premium_status", "current"),
            "payload": _copy_payload(policy),
            "effective_at": policy.get("effective_start"),
            "created_at": _timestamp(len(self.state["insurance_policies"])),
            "updated_at": _timestamp(len(self.state["insurance_policies"]) + 1),
        }
        self.state = _store(self.state, "insurance_policies", policy_id, record)
        self.state = _append_audit_trace(self.state, aggregate_id=policy_id, action="create_insurance_policy", data=record)
        self.state = _emit(self.state, "PolicyCreated", aggregate_id=policy_id, tenant=record["tenant"], payload={"policy_id": policy_id, "policy_number": record["policy_number"]})
        return {"ok": True, "policy": record, "state": self.state, "emitted_event": "PolicyCreated", "side_effects": ()}

    def register_policy_holder(self, holder: dict) -> dict:
        missing = _require(self.state["insurance_policies"], holder.get("policy_id"), "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        holder_id = holder.get("holder_id") or _sequence_id("holder", self.state["policy_holders"])
        record = {
            "id": holder_id,
            "tenant": holder.get("tenant", "default"),
            "code": holder.get("code", holder_id),
            "status": holder.get("status", "active"),
            "version": 1,
            "policy_id": holder["policy_id"],
            "holder_role": holder.get("holder_role", "named_insured"),
            "party_name": holder.get("party_name", "Unnamed Insured"),
            "authority_status": holder.get("authority_status", "verified"),
            "payload": _copy_payload(holder),
            "effective_at": holder.get("effective_at"),
            "created_at": _timestamp(len(self.state["policy_holders"])),
            "updated_at": _timestamp(len(self.state["policy_holders"]) + 1),
        }
        self.state = _store(self.state, "policy_holders", holder_id, record)
        self.state = _append_audit_trace(self.state, aggregate_id=holder["policy_id"], action="register_policy_holder", data=record)
        return {"ok": True, "policy_holder": record, "state": self.state, "side_effects": ()}

    def define_policy_coverage(self, coverage: dict) -> dict:
        missing = _require(self.state["insurance_policies"], coverage.get("policy_id"), "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        coverage_id = coverage.get("coverage_id") or _sequence_id("coverage", self.state["policy_coverages"])
        record = {
            "id": coverage_id,
            "tenant": coverage.get("tenant", "default"),
            "code": coverage.get("coverage_code", coverage_id),
            "status": coverage.get("status", "active"),
            "version": 1,
            "policy_id": coverage["policy_id"],
            "coverage_code": coverage.get("coverage_code", "property_damage"),
            "peril_code": coverage.get("peril_code", "fire"),
            "limit_amount": float(coverage.get("limit_amount", 100000.0)),
            "deductible_amount": float(coverage.get("deductible_amount", 1000.0)),
            "payload": _copy_payload(coverage),
            "effective_at": coverage.get("effective_at"),
            "created_at": _timestamp(len(self.state["policy_coverages"])),
            "updated_at": _timestamp(len(self.state["policy_coverages"]) + 1),
        }
        self.state = _store(self.state, "policy_coverages", coverage_id, record)
        self.state = _append_audit_trace(self.state, aggregate_id=coverage["policy_id"], action="define_policy_coverage", data=record)
        return {"ok": True, "coverage": record, "state": self.state, "side_effects": ()}

    def record_endorsement(self, endorsement: dict) -> dict:
        missing = _require(self.state["insurance_policies"], endorsement.get("policy_id"), "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        endorsement_id = endorsement.get("endorsement_id") or _sequence_id("endorsement", self.state["policy_endorsements"])
        record = {
            "id": endorsement_id,
            "tenant": endorsement.get("tenant", "default"),
            "code": endorsement.get("endorsement_code", endorsement_id),
            "status": endorsement.get("status", "approved"),
            "version": 1,
            "policy_id": endorsement["policy_id"],
            "endorsement_code": endorsement.get("endorsement_code", endorsement_id),
            "requested_change": endorsement.get("requested_change", "limit_increase"),
            "premium_delta": float(endorsement.get("premium_delta", 0.0)),
            "payload": _copy_payload(endorsement),
            "effective_at": endorsement.get("effective_at"),
            "created_at": _timestamp(len(self.state["policy_endorsements"])),
            "updated_at": _timestamp(len(self.state["policy_endorsements"]) + 1),
        }
        self.state = _store(self.state, "policy_endorsements", endorsement_id, record)
        return {"ok": True, "endorsement": record, "state": self.state, "side_effects": ()}

    def create_premium_schedule(self, schedule: dict) -> dict:
        missing = _require(self.state["insurance_policies"], schedule.get("policy_id"), "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        schedule_id = schedule.get("schedule_id") or _sequence_id("schedule", self.state["premium_schedules"])
        record = {
            "id": schedule_id,
            "tenant": schedule.get("tenant", "default"),
            "code": schedule.get("code", schedule_id),
            "status": schedule.get("status", "active"),
            "version": 1,
            "policy_id": schedule["policy_id"],
            "billing_frequency": schedule.get("billing_frequency", "monthly"),
            "installment_amount": float(schedule.get("installment_amount", 1000.0)),
            "due_date": schedule.get("due_date", "2026-06-30"),
            "payload": _copy_payload(schedule),
            "effective_at": schedule.get("effective_at"),
            "created_at": _timestamp(len(self.state["premium_schedules"])),
            "updated_at": _timestamp(len(self.state["premium_schedules"]) + 1),
        }
        self.state = _store(self.state, "premium_schedules", schedule_id, record)
        return {"ok": True, "premium_schedule": record, "state": self.state, "side_effects": ()}

    def record_premium_payment(self, payment: dict) -> dict:
        missing = _require(self.state["insurance_policies"], payment.get("policy_id"), "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        payment_id = payment.get("payment_id") or _sequence_id("payment", self.state["premium_payments"])
        record = {
            "id": payment_id,
            "tenant": payment.get("tenant", "default"),
            "code": payment.get("code", payment_id),
            "status": payment.get("payment_status", "captured"),
            "version": 1,
            "policy_id": payment["policy_id"],
            "schedule_id": payment.get("schedule_id"),
            "amount_paid": float(payment.get("amount_paid", 0.0)),
            "paid_at": payment.get("paid_at", "2026-05-30T00:00:00Z"),
            "payment_status": payment.get("payment_status", "captured"),
            "payload": _copy_payload(payment),
            "effective_at": payment.get("effective_at"),
            "created_at": _timestamp(len(self.state["premium_payments"])),
            "updated_at": _timestamp(len(self.state["premium_payments"]) + 1),
        }
        self.state = _store(self.state, "premium_payments", payment_id, record)
        policies = deepcopy(self.state["insurance_policies"])
        if payment["policy_id"] in policies:
            policies[payment["policy_id"]]["premium_status"] = "current"
            self.state = {**self.state, "insurance_policies": policies}
        return {"ok": True, "premium_payment": record, "state": self.state, "side_effects": ()}

    def open_claim(self, claim: dict) -> dict:
        missing = _require(self.state["insurance_policies"], claim.get("policy_id"), "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        claim_id = claim.get("claim_id") or _sequence_id("claim", self.state["claim_records"])
        record = {
            "id": claim_id,
            "tenant": claim.get("tenant", "default"),
            "code": claim.get("claim_number", claim_id),
            "status": claim.get("status", "open"),
            "version": 1,
            "policy_id": claim["policy_id"],
            "claim_number": claim.get("claim_number", claim_id),
            "loss_date": claim.get("loss_date", "2026-05-01"),
            "severity_band": claim.get("severity_band", "medium"),
            "claim_stage": claim.get("claim_stage", "fnol"),
            "payload": _copy_payload(claim),
            "effective_at": claim.get("effective_at"),
            "created_at": _timestamp(len(self.state["claim_records"])),
            "updated_at": _timestamp(len(self.state["claim_records"]) + 1),
        }
        self.state = _store(self.state, "claim_records", claim_id, record)
        workflow = {
            "claim_id": claim_id,
            "stage": "fnol_triage",
            "pending_actions": ("collect_loss_details", "assign_adjuster", "run_coverage_check"),
            "severity_band": record["severity_band"],
        }
        workflows = deepcopy(self.state["workflows"])
        workflows[claim_id] = workflow
        self.state = {**self.state, "workflows": workflows}
        self.state = _append_audit_trace(self.state, aggregate_id=claim_id, action="open_claim", data=record)
        self.state = _emit(self.state, "ClaimOpened", aggregate_id=claim_id, tenant=record["tenant"], payload={"claim_id": claim_id, "policy_id": claim["policy_id"]})
        return {"ok": True, "claim": record, "workflow": workflow, "state": self.state, "emitted_event": "ClaimOpened", "side_effects": ()}

    def record_loss_event(self, loss_event: dict) -> dict:
        missing = _require(self.state["claim_records"], loss_event.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        loss_event_id = loss_event.get("loss_event_id") or _sequence_id("loss", self.state["loss_events"])
        record = {
            "id": loss_event_id,
            "tenant": loss_event.get("tenant", "default"),
            "code": loss_event.get("code", loss_event_id),
            "status": loss_event.get("status", "captured"),
            "version": 1,
            "claim_id": loss_event["claim_id"],
            "event_type": loss_event.get("event_type", "fire"),
            "occurred_at": loss_event.get("occurred_at", "2026-05-01T12:00:00Z"),
            "location_code": loss_event.get("location_code", "KE-NRB"),
            "catastrophe_flag": bool(loss_event.get("catastrophe_flag", False)),
            "payload": _copy_payload(loss_event),
            "effective_at": loss_event.get("effective_at"),
            "created_at": _timestamp(len(self.state["loss_events"])),
            "updated_at": _timestamp(len(self.state["loss_events"]) + 1),
        }
        self.state = _store(self.state, "loss_events", loss_event_id, record)
        return {"ok": True, "loss_event": record, "state": self.state, "side_effects": ()}

    def register_claimant(self, claimant: dict) -> dict:
        missing = _require(self.state["claim_records"], claimant.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        claimant_id = claimant.get("claimant_id") or _sequence_id("claimant", self.state["claimants"])
        record = {
            "id": claimant_id,
            "tenant": claimant.get("tenant", "default"),
            "code": claimant.get("code", claimant_id),
            "status": claimant.get("status", "active"),
            "version": 1,
            "claim_id": claimant["claim_id"],
            "claimant_role": claimant.get("claimant_role", "insured"),
            "claimant_name": claimant.get("claimant_name", "Claimant"),
            "relationship_to_insured": claimant.get("relationship_to_insured", "self"),
            "payload": _copy_payload(claimant),
            "effective_at": claimant.get("effective_at"),
            "created_at": _timestamp(len(self.state["claimants"])),
            "updated_at": _timestamp(len(self.state["claimants"]) + 1),
        }
        self.state = _store(self.state, "claimants", claimant_id, record)
        return {"ok": True, "claimant": record, "state": self.state, "side_effects": ()}

    def attach_claim_document(self, document: dict) -> dict:
        missing = _require(self.state["claim_records"], document.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        document_id = document.get("document_id") or _sequence_id("document", self.state["claim_documents"])
        record = {
            "id": document_id,
            "tenant": document.get("tenant", "default"),
            "code": document.get("code", document_id),
            "status": document.get("verification_status", "pending"),
            "version": 1,
            "claim_id": document["claim_id"],
            "document_type": document.get("document_type", "proof_of_loss"),
            "source_channel": document.get("source_channel", "portal"),
            "received_at": document.get("received_at", "2026-05-30T00:00:00Z"),
            "verification_status": document.get("verification_status", "pending"),
            "payload": _copy_payload(document),
            "effective_at": document.get("effective_at"),
            "created_at": _timestamp(len(self.state["claim_documents"])),
            "updated_at": _timestamp(len(self.state["claim_documents"]) + 1),
        }
        self.state = _store(self.state, "claim_documents", document_id, record)
        return {"ok": True, "claim_document": record, "state": self.state, "side_effects": ()}

    def determine_coverage(self, determination: dict) -> dict:
        missing_claim = _require(self.state["claim_records"], determination.get("claim_id"), "claim_not_found")
        if missing_claim:
            return {**missing_claim, "state": self.state}
        claim = self.state["claim_records"][determination["claim_id"]]
        peril_code = determination.get("peril_code")
        coverage = _coverage_match(self.state, claim["policy_id"], peril_code)
        premium_current = _policy_premium_current(self.state, claim["policy_id"])
        allowed = coverage is not None and premium_current
        decision = determination.get("decision", "approved" if allowed else "denied")
        covered_amount = min(float(determination.get("covered_amount", 0.0) or 0.0), float(coverage["limit_amount"]) if coverage else 0.0)
        determination_id = determination.get("determination_id") or _sequence_id("determination", self.state["coverage_determinations"])
        record = {
            "id": determination_id,
            "tenant": determination.get("tenant", claim["tenant"]),
            "code": determination.get("code", determination_id),
            "status": "completed",
            "version": 1,
            "policy_id": claim["policy_id"],
            "claim_id": claim["id"],
            "decision": decision,
            "covered_amount": covered_amount,
            "reasoning_hash": _digest((claim["id"], peril_code, decision, premium_current)),
            "payload": {"matched_coverage": coverage["id"] if coverage else None, "premium_current": premium_current, **_copy_payload(determination)},
            "effective_at": determination.get("effective_at"),
            "created_at": _timestamp(len(self.state["coverage_determinations"])),
            "updated_at": _timestamp(len(self.state["coverage_determinations"]) + 1),
        }
        self.state = _store(self.state, "coverage_determinations", determination_id, record)
        claims = deepcopy(self.state["claim_records"])
        claims[claim["id"]]["coverage_position"] = decision
        claims[claim["id"]]["claim_stage"] = "coverage_review"
        self.state = {**self.state, "claim_records": claims}
        self.state = _emit(self.state, "CoverageDetermined", aggregate_id=claim["id"], tenant=record["tenant"], payload={"claim_id": claim["id"], "decision": decision})
        return {"ok": True, "coverage_determination": record, "state": self.state, "emitted_event": "CoverageDetermined", "side_effects": ()}

    def set_claim_reserve(self, reserve: dict) -> dict:
        missing = _require(self.state["claim_records"], reserve.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        approved_amount = float(reserve.get("approved_amount", reserve.get("recommended_amount", 0.0)))
        threshold = float(self.state.get("parameters", {}).get("reserve_review_threshold", {}).get("value", DEFAULT_PARAMETERS["reserve_review_threshold"]))
        adequacy_band = reserve.get("adequacy_band", "review" if approved_amount >= threshold else "within_authority")
        reserve_id = reserve.get("reserve_id") or _sequence_id("reserve", self.state["claim_reserves"])
        record = {
            "id": reserve_id,
            "tenant": reserve.get("tenant", "default"),
            "code": reserve.get("code", reserve_id),
            "status": reserve.get("status", "active"),
            "version": 1,
            "claim_id": reserve["claim_id"],
            "reserve_type": reserve.get("reserve_type", "indemnity"),
            "recommended_amount": float(reserve.get("recommended_amount", approved_amount)),
            "approved_amount": approved_amount,
            "adequacy_band": adequacy_band,
            "payload": _copy_payload(reserve),
            "effective_at": reserve.get("effective_at"),
            "created_at": _timestamp(len(self.state["claim_reserves"])),
            "updated_at": _timestamp(len(self.state["claim_reserves"]) + 1),
        }
        self.state = _store(self.state, "claim_reserves", reserve_id, record)
        self.state = _emit(self.state, "ReserveChanged", aggregate_id=reserve["claim_id"], tenant=record["tenant"], payload={"claim_id": reserve["claim_id"], "approved_amount": approved_amount})
        return {"ok": True, "claim_reserve": record, "state": self.state, "emitted_event": "ReserveChanged", "side_effects": ()}

    def record_reserve_change(self, change: dict) -> dict:
        missing_claim = _require(self.state["claim_records"], change.get("claim_id"), "claim_not_found")
        if missing_claim:
            return {**missing_claim, "state": self.state}
        missing_reserve = _require(self.state["claim_reserves"], change.get("reserve_id"), "reserve_not_found")
        if missing_reserve:
            return {**missing_reserve, "state": self.state}
        change_id = change.get("change_id") or _sequence_id("reserve_change", self.state["reserve_changes"])
        delta = float(change.get("delta_amount", 0.0))
        record = {
            "id": change_id,
            "tenant": change.get("tenant", "default"),
            "code": change.get("code", change_id),
            "status": "recorded",
            "version": 1,
            "claim_id": change["claim_id"],
            "reserve_id": change["reserve_id"],
            "delta_amount": delta,
            "reason_code": change.get("reason_code", "fact_development"),
            "authority_level": change.get("authority_level", "supervisor"),
            "payload": _copy_payload(change),
            "effective_at": change.get("effective_at"),
            "created_at": _timestamp(len(self.state["reserve_changes"])),
            "updated_at": _timestamp(len(self.state["reserve_changes"]) + 1),
        }
        self.state = _store(self.state, "reserve_changes", change_id, record)
        reserves = deepcopy(self.state["claim_reserves"])
        reserves[change["reserve_id"]]["approved_amount"] = round(float(reserves[change["reserve_id"]]["approved_amount"]) + delta, 2)
        self.state = {**self.state, "claim_reserves": reserves}
        self.state = _emit(self.state, "ReserveChanged", aggregate_id=change["claim_id"], tenant=record["tenant"], payload={"claim_id": change["claim_id"], "delta_amount": delta})
        return {"ok": True, "reserve_change": record, "state": self.state, "emitted_event": "ReserveChanged", "side_effects": ()}

    def adjudicate_claim(self, adjudication: dict) -> dict:
        missing = _require(self.state["claim_records"], adjudication.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        claim_id = adjudication["claim_id"]
        determinations = tuple(item for item in self.state["coverage_determinations"].values() if item["claim_id"] == claim_id)
        if not determinations:
            return {"ok": False, "reason": "coverage_not_determined", "claim_id": claim_id, "state": self.state, "side_effects": ()}
        fraud_items = tuple(item for item in self.state["fraud_indicators"].values() if item["claim_id"] == claim_id)
        fraud_score = max((float(item["score"]) for item in fraud_items), default=0.0)
        threshold = float(self.state.get("parameters", {}).get("fraud_score_threshold", {}).get("value", DEFAULT_PARAMETERS["fraud_score_threshold"]))
        decision = adjudication.get("decision", "approved" if determinations[-1]["decision"] == "approved" and fraud_score < threshold else "held")
        adjudication_id = adjudication.get("adjudication_id") or _sequence_id("adjudication", self.state["claim_adjudications"])
        record = {
            "id": adjudication_id,
            "tenant": adjudication.get("tenant", "default"),
            "code": adjudication.get("code", adjudication_id),
            "status": "completed",
            "version": 1,
            "claim_id": claim_id,
            "decision": decision,
            "liability_position": adjudication.get("liability_position", "covered" if decision == "approved" else "investigate"),
            "reviewer_role": adjudication.get("reviewer_role", "adjuster"),
            "reviewed_at": adjudication.get("reviewed_at", "2026-05-30T00:00:00Z"),
            "payload": {"fraud_score": fraud_score, **_copy_payload(adjudication)},
            "effective_at": adjudication.get("effective_at"),
            "created_at": _timestamp(len(self.state["claim_adjudications"])),
            "updated_at": _timestamp(len(self.state["claim_adjudications"]) + 1),
        }
        self.state = _store(self.state, "claim_adjudications", adjudication_id, record)
        workflows = deepcopy(self.state["workflows"])
        if claim_id in workflows:
            workflows[claim_id]["stage"] = "settlement_ready" if decision == "approved" else "investigation_hold"
            workflows[claim_id]["pending_actions"] = ("prepare_offer",) if decision == "approved" else ("fraud_review", "supervisor_review")
            self.state = {**self.state, "workflows": workflows}
        self.state = _emit(self.state, "ClaimAdjudicated", aggregate_id=claim_id, tenant=record["tenant"], payload={"claim_id": claim_id, "decision": decision})
        return {"ok": True, "claim_adjudication": record, "state": self.state, "emitted_event": "ClaimAdjudicated", "side_effects": ()}

    def create_settlement_offer(self, offer: dict) -> dict:
        missing = _require(self.state["claim_records"], offer.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        limit = float(self.state.get("parameters", {}).get("settlement_authority_limit", {}).get("value", DEFAULT_PARAMETERS["settlement_authority_limit"]))
        amount = float(offer.get("offer_amount", 0.0))
        status = "awaiting_authority" if amount > limit else offer.get("negotiation_status", "proposed")
        offer_id = offer.get("offer_id") or _sequence_id("offer", self.state["settlement_offers"])
        record = {
            "id": offer_id,
            "tenant": offer.get("tenant", "default"),
            "code": offer.get("code", offer_id),
            "status": status,
            "version": 1,
            "claim_id": offer["claim_id"],
            "offer_amount": amount,
            "negotiation_status": status,
            "authority_required": "executive" if amount > limit else "adjuster",
            "expires_at": offer.get("expires_at", "2026-06-15T00:00:00Z"),
            "payload": _copy_payload(offer),
            "effective_at": offer.get("effective_at"),
            "created_at": _timestamp(len(self.state["settlement_offers"])),
            "updated_at": _timestamp(len(self.state["settlement_offers"]) + 1),
        }
        self.state = _store(self.state, "settlement_offers", offer_id, record)
        return {"ok": True, "settlement_offer": record, "state": self.state, "side_effects": ()}

    def execute_settlement_payment(self, payment: dict) -> dict:
        missing_claim = _require(self.state["claim_records"], payment.get("claim_id"), "claim_not_found")
        if missing_claim:
            return {**missing_claim, "state": self.state}
        missing_offer = _require(self.state["settlement_offers"], payment.get("settlement_offer_id"), "offer_not_found")
        if missing_offer:
            return {**missing_offer, "state": self.state}
        offer = self.state["settlement_offers"][payment["settlement_offer_id"]]
        if offer["negotiation_status"] == "awaiting_authority":
            return {"ok": False, "reason": "settlement_authority_pending", "claim_id": payment["claim_id"], "state": self.state, "side_effects": ()}
        payment_id = payment.get("payment_id") or _sequence_id("settlement_payment", self.state["settlement_payments"])
        record = {
            "id": payment_id,
            "tenant": payment.get("tenant", "default"),
            "code": payment.get("code", payment_id),
            "status": payment.get("payment_status", "scheduled"),
            "version": 1,
            "claim_id": payment["claim_id"],
            "settlement_offer_id": payment["settlement_offer_id"],
            "payee_name": payment.get("payee_name", "Primary Insured"),
            "payment_amount": float(payment.get("payment_amount", offer["offer_amount"])),
            "payment_status": payment.get("payment_status", "scheduled"),
            "payload": _copy_payload(payment),
            "effective_at": payment.get("effective_at"),
            "created_at": _timestamp(len(self.state["settlement_payments"])),
            "updated_at": _timestamp(len(self.state["settlement_payments"]) + 1),
        }
        self.state = _store(self.state, "settlement_payments", payment_id, record)
        self.state = _emit(self.state, "SettlementPaid", aggregate_id=payment["claim_id"], tenant=record["tenant"], payload={"claim_id": payment["claim_id"], "payment_amount": record["payment_amount"]})
        return {"ok": True, "settlement_payment": record, "state": self.state, "emitted_event": "SettlementPaid", "side_effects": ()}

    def record_subrogation_recovery(self, recovery: dict) -> dict:
        missing = _require(self.state["claim_records"], recovery.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        recovery_id = recovery.get("recovery_id") or _sequence_id("recovery", self.state["subrogation_recoveries"])
        record = {
            "id": recovery_id,
            "tenant": recovery.get("tenant", "default"),
            "code": recovery.get("code", recovery_id),
            "status": recovery.get("status", "open"),
            "version": 1,
            "claim_id": recovery["claim_id"],
            "target_party": recovery.get("target_party", "Third Party"),
            "recovery_amount": float(recovery.get("recovery_amount", 0.0)),
            "recovery_stage": recovery.get("recovery_stage", "investigate"),
            "statute_deadline": recovery.get("statute_deadline", "2027-05-30"),
            "payload": _copy_payload(recovery),
            "effective_at": recovery.get("effective_at"),
            "created_at": _timestamp(len(self.state["subrogation_recoveries"])),
            "updated_at": _timestamp(len(self.state["subrogation_recoveries"]) + 1),
        }
        self.state = _store(self.state, "subrogation_recoveries", recovery_id, record)
        return {"ok": True, "subrogation_recovery": record, "state": self.state, "side_effects": ()}

    def send_claim_communication(self, communication: dict) -> dict:
        missing = _require(self.state["claim_records"], communication.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        communication_id = communication.get("communication_id") or _sequence_id("communication", self.state["claim_communications"])
        record = {
            "id": communication_id,
            "tenant": communication.get("tenant", "default"),
            "code": communication.get("code", communication_id),
            "status": communication.get("delivery_status", "queued"),
            "version": 1,
            "claim_id": communication["claim_id"],
            "channel": communication.get("channel", "email"),
            "recipient_role": communication.get("recipient_role", "insured"),
            "response_due_at": communication.get("response_due_at"),
            "delivery_status": communication.get("delivery_status", "queued"),
            "payload": _copy_payload(communication),
            "effective_at": communication.get("effective_at"),
            "created_at": _timestamp(len(self.state["claim_communications"])),
            "updated_at": _timestamp(len(self.state["claim_communications"]) + 1),
        }
        self.state = _store(self.state, "claim_communications", communication_id, record)
        return {"ok": True, "claim_communication": record, "state": self.state, "side_effects": ()}

    def score_fraud_indicator(self, indicator: dict) -> dict:
        missing = _require(self.state["claim_records"], indicator.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        score = float(indicator.get("score", 0.35 + 0.15 * int(bool(indicator.get("late_report"))) + 0.2 * int(bool(indicator.get("multiple_claimants"))) + 0.1 * int(bool(indicator.get("catastrophe_flag")))))
        fraud_id = indicator.get("fraud_indicator_id") or _sequence_id("fraud", self.state["fraud_indicators"])
        threshold = float(self.state.get("parameters", {}).get("fraud_score_threshold", {}).get("value", DEFAULT_PARAMETERS["fraud_score_threshold"]))
        review_status = "siu_review" if score >= threshold else "monitor"
        record = {
            "id": fraud_id,
            "tenant": indicator.get("tenant", "default"),
            "code": indicator.get("code", fraud_id),
            "status": review_status,
            "version": 1,
            "claim_id": indicator["claim_id"],
            "signal_type": indicator.get("signal_type", "pattern_anomaly"),
            "score": round(score, 4),
            "disposition": indicator.get("disposition", "open"),
            "review_status": review_status,
            "payload": _copy_payload(indicator),
            "effective_at": indicator.get("effective_at"),
            "created_at": _timestamp(len(self.state["fraud_indicators"])),
            "updated_at": _timestamp(len(self.state["fraud_indicators"]) + 1),
        }
        self.state = _store(self.state, "fraud_indicators", fraud_id, record)
        if score >= threshold:
            self.resolve_claim_exception({
                "claim_id": indicator["claim_id"],
                "exception_type": "fraud_review_required",
                "severity": "high",
                "queue_name": "siu",
                "resolution_status": "open",
            }, open_case=True)
        return {"ok": True, "fraud_indicator": record, "state": self.state, "side_effects": ()}

    def resolve_claim_exception(self, exception_case: dict, *, open_case: bool = False) -> dict:
        missing = _require(self.state["claim_records"], exception_case.get("claim_id"), "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        existing = next(
            (
                key
                for key, item in self.state["claim_exception_cases"].items()
                if item["claim_id"] == exception_case["claim_id"] and item["exception_type"] == exception_case.get("exception_type")
            ),
            None,
        )
        case_id = existing or exception_case.get("exception_case_id") or _sequence_id("exception", self.state["claim_exception_cases"])
        status = exception_case.get("resolution_status", "open" if open_case else "resolved")
        record = {
            "id": case_id,
            "tenant": exception_case.get("tenant", "default"),
            "code": exception_case.get("code", case_id),
            "status": status,
            "version": 1,
            "claim_id": exception_case["claim_id"],
            "exception_type": exception_case.get("exception_type", "general_exception"),
            "severity": exception_case.get("severity", "medium"),
            "queue_name": exception_case.get("queue_name", "supervisor"),
            "resolution_status": status,
            "payload": _copy_payload(exception_case),
            "effective_at": exception_case.get("effective_at"),
            "created_at": _timestamp(len(self.state["claim_exception_cases"])),
            "updated_at": _timestamp(len(self.state["claim_exception_cases"]) + 1),
        }
        self.state = _store(self.state, "claim_exception_cases", case_id, record)
        return {"ok": True, "claim_exception_case": record, "state": self.state, "side_effects": ()}

    def compile_insurance_rule(self, payload: dict) -> dict:
        compiled = config.compile_rule(payload)
        if not compiled["ok"]:
            return {"ok": False, "reason": compiled["reason"], "state": self.state, "side_effects": ()}
        return self.register_rule(compiled["rule"])

    def simulate_loss_exposure(self, payload: dict | None = None) -> dict:
        payload = _copy_payload(payload)
        claim_id = payload.get("claim_id")
        claim = self.state["claim_records"].get(claim_id, {}) if claim_id else {}
        reserve_total = sum(float(item["approved_amount"]) for item in self.state["claim_reserves"].values() if not claim_id or item["claim_id"] == claim_id)
        recovery_total = sum(float(item["recovery_amount"]) for item in self.state["subrogation_recoveries"].values() if not claim_id or item["claim_id"] == claim_id)
        fraud_drag = max((float(item["score"]) for item in self.state["fraud_indicators"].values() if not claim_id or item["claim_id"] == claim_id), default=0.0)
        expected = round(max(reserve_total - recovery_total, 0.0) * (1.0 + min(fraud_drag, 0.5)), 2)
        return {
            "ok": True,
            "claim_id": claim_id,
            "claim_number": claim.get("claim_number"),
            "expected_loss": expected,
            "range": {"low": round(expected * 0.9, 2), "high": round(expected * 1.15 + 5000.0, 2)},
            "drivers": ("reserve_total", "recovery_total", "fraud_drag"),
            "side_effects": (),
        }

    def receive_event(self, envelope: dict) -> dict:
        result = handlers.dispatch_event(envelope, self.state)
        self.state = _ensure_state(result.get("state", self.state))
        if result.get("ok") is False:
            dead_letters = tuple(self.state.get("dead_letters", ()))
            self.state = {**self.state, "dead_letters": (*dead_letters, dict(envelope))}
        return {**result, "state": self.state}

    def document_intake(self, document: str, instruction: str) -> dict:
        instruction_text = f"{document} {instruction}".lower()
        candidate_operations = []
        if "policy" in instruction_text:
            candidate_operations.append("create_insurance_policy")
        if "coverage" in instruction_text:
            candidate_operations.append("determine_coverage")
        if "reserve" in instruction_text:
            candidate_operations.append("set_claim_reserve")
        if "settlement" in instruction_text or "payment" in instruction_text:
            candidate_operations.append("create_settlement_offer")
        if "fraud" in instruction_text:
            candidate_operations.append("score_fraud_indicator")
        if "recovery" in instruction_text or "subrogation" in instruction_text:
            candidate_operations.append("record_subrogation_recovery")
        if not candidate_operations:
            candidate_operations.append("open_claim")
        citations = tuple({"quote": snippet.strip(), "source": f"document:{index + 1}"} for index, snippet in enumerate(str(document).split(".")[:2]) if snippet.strip())
        operation_table_map = {
            "create_insurance_policy": "insurance_policy",
            "register_policy_holder": "policy_holder",
            "define_policy_coverage": "policy_coverage",
            "record_endorsement": "policy_endorsement",
            "create_premium_schedule": "premium_schedule",
            "record_premium_payment": "premium_payment",
            "open_claim": "claim_record",
            "record_loss_event": "loss_event",
            "register_claimant": "claimant",
            "attach_claim_document": "claim_document",
            "determine_coverage": "coverage_determination",
            "set_claim_reserve": "claim_reserve",
            "record_reserve_change": "reserve_change",
            "adjudicate_claim": "claim_adjudication",
            "create_settlement_offer": "settlement_offer",
            "execute_settlement_payment": "settlement_payment",
            "record_subrogation_recovery": "subrogation_recovery",
            "send_claim_communication": "claim_communication",
            "score_fraud_indicator": "fraud_indicator",
            "resolve_claim_exception": "claim_exception_case",
            "compile_insurance_rule": "insurance_policy_rule",
            "simulate_loss_exposure": "claim_record",
        }
        affected_tables = tuple(
            MODEL_BY_LOGICAL_TABLE[operation_table_map[operation]]["table"]
            for operation in candidate_operations
            if operation in operation_table_map
        )
        return {
            "ok": True,
            "document_digest": _digest(document),
            "instruction": instruction,
            "candidate_operations": tuple(candidate_operations),
            "candidate_tables": affected_tables,
            "citations": citations,
            "requires_human_confirmation": True,
            "side_effects": (),
        }

    def crud_mutation_plan(self, action: str, table: str | None = None, payload: dict | None = None) -> dict:
        target = table or OWNED_TABLES[0]
        if target not in OWNED_TABLES:
            return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
        mutation = action in {"create", "update", "delete"}
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "action": action,
            "table": target,
            "payload": _copy_payload(payload),
            "requires_confirmation": mutation,
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def get_policy_snapshot(self, policy_id: str) -> dict:
        missing = _require(self.state["insurance_policies"], policy_id, "policy_not_found")
        if missing:
            return {**missing, "state": self.state}
        return {
            "ok": True,
            "policy": deepcopy(self.state["insurance_policies"][policy_id]),
            "holders": tuple(item for item in self.state["policy_holders"].values() if item["policy_id"] == policy_id),
            "coverages": tuple(item for item in self.state["policy_coverages"].values() if item["policy_id"] == policy_id),
            "endorsements": tuple(item for item in self.state["policy_endorsements"].values() if item["policy_id"] == policy_id),
            "premium_schedules": tuple(item for item in self.state["premium_schedules"].values() if item["policy_id"] == policy_id),
            "premium_payments": tuple(item for item in self.state["premium_payments"].values() if item["policy_id"] == policy_id),
            "claims": tuple(item for item in self.state["claim_records"].values() if item["policy_id"] == policy_id),
            "side_effects": (),
        }

    def get_claim_snapshot(self, claim_id: str) -> dict:
        missing = _require(self.state["claim_records"], claim_id, "claim_not_found")
        if missing:
            return {**missing, "state": self.state}
        return {
            "ok": True,
            "claim": deepcopy(self.state["claim_records"][claim_id]),
            "loss_events": tuple(item for item in self.state["loss_events"].values() if item["claim_id"] == claim_id),
            "claimants": tuple(item for item in self.state["claimants"].values() if item["claim_id"] == claim_id),
            "documents": tuple(item for item in self.state["claim_documents"].values() if item["claim_id"] == claim_id),
            "coverage_determinations": tuple(item for item in self.state["coverage_determinations"].values() if item["claim_id"] == claim_id),
            "reserves": tuple(item for item in self.state["claim_reserves"].values() if item["claim_id"] == claim_id),
            "adjudications": tuple(item for item in self.state["claim_adjudications"].values() if item["claim_id"] == claim_id),
            "settlement_offers": tuple(item for item in self.state["settlement_offers"].values() if item["claim_id"] == claim_id),
            "settlement_payments": tuple(item for item in self.state["settlement_payments"].values() if item["claim_id"] == claim_id),
            "fraud_indicators": tuple(item for item in self.state["fraud_indicators"].values() if item["claim_id"] == claim_id),
            "exceptions": tuple(item for item in self.state["claim_exception_cases"].values() if item["claim_id"] == claim_id),
            "workflow": deepcopy(self.state["workflows"].get(claim_id, {})),
            "side_effects": (),
        }

    def workbench(self, *, tenant: str | None = None, permissions: tuple[str, ...] | None = None) -> dict:
        active_tenant = tenant or "default"
        allowed = permissions or PERMISSIONS
        claims = tuple(item for item in self.state["claim_records"].values() if item["tenant"] == active_tenant)
        fraud_threshold = float(self.state.get("parameters", {}).get("fraud_score_threshold", {}).get("value", DEFAULT_PARAMETERS["fraud_score_threshold"]))
        fraud_queue = tuple(item for item in self.state["fraud_indicators"].values() if item["tenant"] == active_tenant and float(item["score"]) >= fraud_threshold)
        reserve_queue = tuple(item for item in self.state["claim_reserves"].values() if item["tenant"] == active_tenant and item["adequacy_band"] != "within_authority")
        settlement_queue = tuple(item for item in self.state["settlement_offers"].values() if item["tenant"] == active_tenant and item["negotiation_status"] in {"proposed", "awaiting_authority"})
        workflows = tuple(item for claim_id, item in self.state["workflows"].items() if self.state["claim_records"].get(claim_id, {}).get("tenant") == active_tenant)
        return {
            "ok": True,
            "tenant": active_tenant,
            "cards": (
                {"key": "policies", "value": sum(1 for item in self.state["insurance_policies"].values() if item["tenant"] == active_tenant)},
                {"key": "open_claims", "value": len(claims)},
                {"key": "coverage_decisions", "value": sum(1 for item in self.state["coverage_determinations"].values() if item["tenant"] == active_tenant)},
                {"key": "reserve_reviews", "value": len(reserve_queue)},
                {"key": "fraud_queue", "value": len(fraud_queue)},
                {"key": "settlement_queue", "value": len(settlement_queue)},
                {"key": "recoveries", "value": sum(1 for item in self.state["subrogation_recoveries"].values() if item["tenant"] == active_tenant)},
                {"key": "dead_letters", "value": len(self.state.get("dead_letters", ()))},
            ),
            "queues": {
                "fnol": tuple(item["id"] for item in claims if item.get("claim_stage") in {"fnol", "coverage_review"}),
                "fraud": tuple(item["id"] for item in fraud_queue),
                "reserves": tuple(item["id"] for item in reserve_queue),
                "settlement": tuple(item["id"] for item in settlement_queue),
            },
            "workflow_board": workflows,
            "visible_permissions": allowed,
            "configuration_bound": bool(self.state.get("configuration")),
            "parameter_count": len(self.state.get("parameters", {})),
            "rule_count": len(self.state.get("rules", {})),
            "event_outbox_count": len(self.state.get("outbox", ())),
            "event_inbox_count": len(self.state.get("inbox", ())),
            "side_effects": (),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.register_defaults(tenant=tenant)
        policy = self.create_insurance_policy({"tenant": tenant, "policy_number": f"POL-{tenant}", "product_code": "commercial_property", "effective_start": "2026-01-01", "premium_status": "current"})
        self.register_policy_holder({"tenant": tenant, "policy_id": policy["policy"]["id"], "party_name": "Acme Manufacturing Ltd", "holder_role": "named_insured"})
        self.define_policy_coverage({"tenant": tenant, "policy_id": policy["policy"]["id"], "coverage_code": "building", "peril_code": "fire", "limit_amount": 250000.0, "deductible_amount": 5000.0})
        self.create_premium_schedule({"tenant": tenant, "policy_id": policy["policy"]["id"], "installment_amount": 4500.0, "due_date": "2026-06-30"})
        self.record_premium_payment({"tenant": tenant, "policy_id": policy["policy"]["id"], "amount_paid": 4500.0, "payment_status": "captured"})
        claim = self.open_claim({"tenant": tenant, "policy_id": policy["policy"]["id"], "claim_number": f"CLM-{tenant}", "loss_date": "2026-05-02", "severity_band": "high"})
        self.record_loss_event({"tenant": tenant, "claim_id": claim["claim"]["id"], "event_type": "fire", "location_code": "KE-NRB"})
        self.register_claimant({"tenant": tenant, "claim_id": claim["claim"]["id"], "claimant_name": "Acme Manufacturing Ltd"})
        self.attach_claim_document({"tenant": tenant, "claim_id": claim["claim"]["id"], "document_type": "proof_of_loss", "verification_status": "verified"})
        self.determine_coverage({"tenant": tenant, "claim_id": claim["claim"]["id"], "peril_code": "fire", "covered_amount": 120000.0})
        self.set_claim_reserve({"tenant": tenant, "claim_id": claim["claim"]["id"], "recommended_amount": 90000.0, "approved_amount": 90000.0})
        self.score_fraud_indicator({"tenant": tenant, "claim_id": claim["claim"]["id"], "signal_type": "late_report", "late_report": True})
        self.adjudicate_claim({"tenant": tenant, "claim_id": claim["claim"]["id"], "reviewer_role": "adjuster"})
        self.create_settlement_offer({"tenant": tenant, "claim_id": claim["claim"]["id"], "offer_amount": 75000.0})
        self.record_subrogation_recovery({"tenant": tenant, "claim_id": claim["claim"]["id"], "target_party": "Electrical Contractor", "recovery_amount": 12000.0})
        self.send_claim_communication({"tenant": tenant, "claim_id": claim["claim"]["id"], "channel": "email", "delivery_status": "sent"})
        return {"ok": True, "tenant": tenant, "policy_id": policy["policy"]["id"], "claim_id": claim["claim"]["id"], "state": self.state, "side_effects": ()}

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    app = InsuranceClaimsPolicyStandaloneApp()
    loaded = app.load_demo_workspace()
    claim_id = loaded["claim_id"]
    exposure = app.simulate_loss_exposure({"claim_id": claim_id})
    intake = app.document_intake("Customer requests reserve review after a fire loss.", "prepare the coverage and reserve workbench")
    workbench = app.workbench(tenant="tenant_demo")
    claim = app.get_claim_snapshot(claim_id)
    return {
        "ok": loaded["ok"] and exposure["ok"] and intake["ok"] and workbench["ok"] and claim["ok"] and workbench["cards"][1]["value"] >= 1,
        "manifest": standalone_manifest(),
        "loaded": loaded,
        "exposure": exposure,
        "intake": intake,
        "workbench": workbench,
        "claim": claim,
        "side_effects": (),
    }
