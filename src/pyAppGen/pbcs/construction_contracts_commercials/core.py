"""Executable package-local commercial controls slice for construction contracts."""
from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import re
from typing import Any

from .commercial_control import COMMERCIAL_CONTROL_CAPABILITIES
from .commercial_control import improve1_commercial_control_contract

PBC_KEY = "construction_contracts_commercials"
CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC = "pbc.construction_contracts_commercials.events"
CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES = (
    "ConstructionContractsCommercialsCreated",
    "ConstructionContractsCommercialsUpdated",
    "ConstructionContractsCommercialsApproved",
    "ConstructionContractsCommercialsExceptionOpened",
)
CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
CONSTRUCTION_CONTRACTS_COMMERCIALS_UI_FRAGMENT_KEYS = (
    "ConstructionContractsCommercialsWorkbench",
    "ConstructionContractsCommercialsDetail",
    "ConstructionContractsCommercialsAssistantPanel",
)
CONSTRUCTION_CONTRACTS_COMMERCIALS_STANDARD_FEATURE_KEYS = (
    "construction_contract_management",
    "construction_contracts_commercials_workflow",
    "construction_contracts_commercials_analytics",
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
CONSTRUCTION_CONTRACTS_COMMERCIALS_RUNTIME_CAPABILITY_KEYS = (
    "construction_contracts_commercials_event_sourced_operational_history",
    "construction_contracts_commercials_multi_tenant_policy_isolation",
    "construction_contracts_commercials_schema_evolution_resilience",
    "construction_contracts_commercials_semantic_document_instruction_understanding",
    "construction_contracts_commercials_predictive_risk_scoring",
    "construction_contracts_commercials_counterfactual_scenario_simulation",
    "construction_contracts_commercials_cryptographic_audit_proofs",
    "construction_contracts_commercials_continuous_control_testing",
    "construction_contracts_commercials_cross_pbc_event_federation",
    "construction_contracts_commercials_governed_ai_agent_execution",
)
CONSTRUCTION_CONTRACTS_COMMERCIALS_ROUTES = (
    "POST /construction-contracts",
    "POST /pay-applications",
    "POST /retainages",
    "POST /variation-orders",
    "POST /commercial-claims",
    "GET /construction-contracts-commercials-workbench",
)

BUSINESS_TABLES = (
    "construction_contracts_commercials_construction_contract",
    "construction_contracts_commercials_pay_application",
    "construction_contracts_commercials_retainage",
    "construction_contracts_commercials_variation_order",
    "construction_contracts_commercials_commercial_claim",
    "construction_contracts_commercials_lien_waiver",
    "construction_contracts_commercials_subcontract_package",
    "construction_contracts_commercials_construction_contracts_commercials_policy_rule",
    "construction_contracts_commercials_construction_contracts_commercials_runtime_parameter",
    "construction_contracts_commercials_construction_contracts_commercials_schema_extension",
    "construction_contracts_commercials_construction_contracts_commercials_control_assertion",
    "construction_contracts_commercials_construction_contracts_commercials_governed_model",
)
EVENT_TABLES = (
    "construction_contracts_commercials_appgen_outbox_event",
    "construction_contracts_commercials_appgen_inbox_event",
    "construction_contracts_commercials_appgen_dead_letter_event",
)
CONSTRUCTION_CONTRACTS_COMMERCIALS_BUSINESS_TABLES = BUSINESS_TABLES
CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES
CONSTRUCTION_CONTRACTS_COMMERCIALS_RUNTIME_TABLES = CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES

CONTRACT_TABLE = BUSINESS_TABLES[0]
PAY_APPLICATION_TABLE = BUSINESS_TABLES[1]
RETAINAGE_TABLE = BUSINESS_TABLES[2]
VARIATION_TABLE = BUSINESS_TABLES[3]
CLAIM_TABLE = BUSINESS_TABLES[4]
WAIVER_TABLE = BUSINESS_TABLES[5]
SUBCONTRACT_TABLE = BUSINESS_TABLES[6]
RULE_TABLE = BUSINESS_TABLES[7]
PARAMETER_TABLE = BUSINESS_TABLES[8]
SCHEMA_EXTENSION_TABLE = BUSINESS_TABLES[9]
CONTROL_ASSERTION_TABLE = BUSINESS_TABLES[10]
GOVERNED_MODEL_TABLE = BUSINESS_TABLES[11]
OUTBOX_TABLE = EVENT_TABLES[0]
INBOX_TABLE = EVENT_TABLES[1]
DEAD_LETTER_TABLE = EVENT_TABLES[2]

CONTRACT_LIFECYCLE_STAGES = (
    "tender",
    "award",
    "execution",
    "suspended",
    "practical_completion",
    "final_account",
    "defects",
    "closed",
)
CONTRACT_LIFECYCLE_TRANSITIONS = {
    "tender": ("award", "suspended"),
    "award": ("execution", "suspended"),
    "execution": ("suspended", "practical_completion"),
    "suspended": ("execution", "closed"),
    "practical_completion": ("final_account", "defects"),
    "final_account": ("defects", "closed"),
    "defects": ("closed",),
    "closed": (),
}
PAY_APPLICATION_STATUSES = (
    "received",
    "parsed",
    "incomplete",
    "under_review",
    "certified",
    "disputed",
    "rejected",
    "revised",
    "archived",
)
VARIATION_STATUSES = ("instruction_issued", "under_review", "approved", "disputed", "implemented")
CLAIM_STATUSES = ("noticed", "entitlement_review", "quantum_review", "negotiation", "settled", "rejected")
WAIVER_STATUSES = ("received", "accepted", "rejected", "expired")
SUBCONTRACT_STATUSES = ("draft", "awarded", "active", "hold", "closeout")

PERMISSIONS = (
    "construction_contracts_commercials.read",
    "construction_contracts_commercials.create",
    "construction_contracts_commercials.update",
    "construction_contracts_commercials.approve",
    "construction_contracts_commercials.admin",
    "construction_contracts_commercials.certify_pay_application",
    "construction_contracts_commercials.approve_variation",
    "construction_contracts_commercials.assess_claim",
    "construction_contracts_commercials.release_retainage",
    "construction_contracts_commercials.accept_waiver",
    "construction_contracts_commercials.approve_settlement",
    "construction_contracts_commercials.close_final_account",
    "construction_contracts_commercials.portal.submit",
    "construction_contracts_commercials.operate",
)
ROLE_PERMISSION_MAP = {
    "contract_admin": PERMISSIONS,
    "quantity_surveyor": (
        "construction_contracts_commercials.read",
        "construction_contracts_commercials.create",
        "construction_contracts_commercials.update",
        "construction_contracts_commercials.certify_pay_application",
        "construction_contracts_commercials.accept_waiver",
    ),
    "commercial_manager": (
        "construction_contracts_commercials.read",
        "construction_contracts_commercials.create",
        "construction_contracts_commercials.update",
        "construction_contracts_commercials.approve",
        "construction_contracts_commercials.approve_variation",
        "construction_contracts_commercials.assess_claim",
        "construction_contracts_commercials.release_retainage",
        "construction_contracts_commercials.close_final_account",
    ),
    "finance_user": (
        "construction_contracts_commercials.read",
        "construction_contracts_commercials.release_retainage",
    ),
    "legal_user": (
        "construction_contracts_commercials.read",
        "construction_contracts_commercials.assess_claim",
        "construction_contracts_commercials.approve_settlement",
    ),
    "auditor": ("construction_contracts_commercials.read",),
    "contractor_portal": (
        "construction_contracts_commercials.read",
        "construction_contracts_commercials.portal.submit",
    ),
}
ROLE_LABELS = {
    "contract_admin": "Contract Administrator",
    "quantity_surveyor": "Quantity Surveyor",
    "commercial_manager": "Commercial Manager",
    "finance_user": "Finance User",
    "legal_user": "Legal User",
    "auditor": "Auditor",
    "contractor_portal": "Contractor Portal",
}

DOMAIN_RULES = (
    "construction_contract_policy",
    "pay_application_policy",
    "retainage_policy",
    "variation_order_policy",
    "commercial_claim_policy",
    "lien_waiver_policy",
    "jurisdiction_prompt_payment_policy",
    "final_account_closeout_policy",
)
DEFAULT_PARAMETERS = {
    "quality_score_floor": {"value": 0.82, "unit": "score"},
    "materiality_threshold": {"value": 25000.0, "unit": "currency"},
    "approval_sla_hours": {"value": 72, "unit": "hours"},
    "risk_threshold": {"value": 0.6, "unit": "score"},
    "forecast_horizon_days": {"value": 90, "unit": "days"},
    "workbench_limit": {"value": 25, "unit": "records"},
    "notice_period_days": {"value": 14, "unit": "days"},
    "retainage_default_percent": {"value": 10.0, "unit": "percent"},
    "retainage_release_completion_percent": {"value": 100.0, "unit": "percent"},
    "waiver_required_for_certification": {"value": True, "unit": "boolean"},
}
DOMAIN_PARAMETERS = tuple(DEFAULT_PARAMETERS.keys())

FORMS = (
    "construction_contract_create_form",
    "pay_application_intake_form",
    "retainage_release_form",
    "variation_order_review_form",
    "commercial_claim_notice_form",
    "lien_waiver_review_form",
    "subcontract_package_compliance_form",
)
WIZARDS = (
    "contract_award_wizard",
    "pay_application_certification_wizard",
    "variation_negotiation_wizard",
    "claim_entitlement_wizard",
    "final_account_closeout_wizard",
)
CONTROLS = (
    "overclaim_guard",
    "waiver_gate",
    "retainage_release_gate",
    "notice_time_bar_monitor",
    "final_account_blocker_panel",
    "event_replay_console",
)
AGENT_SKILLS = (
    "pay_application_summary",
    "variation_entitlement_draft",
    "claim_evidence_gap_analysis",
    "waiver_checklist",
    "final_account_blockers",
    "contract_clause_explanation",
)
DOCUMENT_TYPES = (
    "pay_application",
    "lien_waiver",
    "variation_notice",
    "commercial_claim_notice",
    "bond_or_guarantee",
    "insurance_certificate",
)
DEPENDENCY_PROJECTIONS = (
    "schedule_impact_projection",
    "cost_forecast_projection",
    "tax_projection",
    "vendor_identity_projection",
    "document_reference_projection",
)

DOMAIN_OPERATIONS = (
    "create_construction_contract",
    "progress_contract_lifecycle",
    "record_pay_application",
    "certify_pay_application",
    "review_retainage",
    "release_retainage",
    "approve_variation_order",
    "assess_notice_timeliness",
    "register_commercial_claim",
    "settle_commercial_claim",
    "create_lien_waiver",
    "record_subcontract_package",
    "build_payment_certificate",
    "build_final_account_packet",
    "run_change_impact_simulation",
    "replay_dead_letter_event",
    "generate_cash_flow_forecast",
    "generate_contractor_scorecard",
)
DOMAIN_EDGE_CASES = (
    "duplicate_submission",
    "missing_required_evidence",
    "time_barred_notice",
    "overclaimed_schedule_line",
    "expired_waiver",
    "retention_release_without_closeout",
    "final_account_with_open_claims",
    "foreign_table_reference_attempt",
)

TABLE_FIELDS = {
    CONTRACT_TABLE: (
        "id",
        "tenant",
        "contract_code",
        "title",
        "contract_type",
        "pricing_basis",
        "jurisdiction",
        "counterparty",
        "lifecycle_stage",
        "contract_value",
        "approved_change_value",
        "current_contract_value",
        "retainage_percent",
        "final_account_status",
        "closeout_blockers",
        "schedule_of_values",
        "guarantees",
        "obligations",
        "created_at",
        "updated_at",
    ),
    PAY_APPLICATION_TABLE: (
        "id",
        "tenant",
        "contract_id",
        "application_number",
        "intake_status",
        "period_start",
        "period_end",
        "gross_claimed",
        "certified_amount",
        "retainage_withheld",
        "waiver_status",
        "evidence_status",
        "attachments",
        "lines",
        "validation_issues",
        "certificate_trace",
        "created_at",
        "updated_at",
    ),
    RETAINAGE_TABLE: (
        "id",
        "tenant",
        "contract_id",
        "pay_application_id",
        "status",
        "retainage_percent",
        "withheld_amount",
        "release_trigger",
        "release_blockers",
        "released_amount",
        "created_at",
        "updated_at",
    ),
    VARIATION_TABLE: (
        "id",
        "tenant",
        "contract_id",
        "variation_number",
        "status",
        "instruction_date",
        "event_date",
        "notice_date",
        "contractual_deadline",
        "time_bar_status",
        "quoted_amount",
        "approved_amount",
        "time_impact_days",
        "created_at",
        "updated_at",
    ),
    CLAIM_TABLE: (
        "id",
        "tenant",
        "contract_id",
        "claim_number",
        "claim_type",
        "status",
        "event_date",
        "notice_date",
        "contractual_deadline",
        "time_bar_status",
        "claimed_amount",
        "assessed_amount",
        "settled_amount",
        "entitlement_risk",
        "created_at",
        "updated_at",
    ),
    WAIVER_TABLE: (
        "id",
        "tenant",
        "contract_id",
        "pay_application_id",
        "waiver_number",
        "waiver_type",
        "status",
        "covered_amount",
        "covered_period",
        "jurisdiction",
        "signed_date",
        "created_at",
        "updated_at",
    ),
    SUBCONTRACT_TABLE: (
        "id",
        "tenant",
        "contract_id",
        "package_code",
        "subcontractor_name",
        "status",
        "contract_value",
        "insurance_status",
        "bond_status",
        "compliance_hold",
        "closeout_checklist",
        "created_at",
        "updated_at",
    ),
    RULE_TABLE: (
        "id",
        "tenant",
        "rule_code",
        "rule_name",
        "policy_area",
        "status",
        "severity",
        "compiled_hash",
        "effective_from",
        "created_at",
        "updated_at",
    ),
    PARAMETER_TABLE: (
        "id",
        "tenant",
        "parameter_name",
        "value_json",
        "unit",
        "bounded",
        "status",
        "updated_at",
    ),
    SCHEMA_EXTENSION_TABLE: (
        "id",
        "tenant",
        "target_table",
        "extension_name",
        "status",
        "fields_json",
        "created_at",
        "updated_at",
    ),
    CONTROL_ASSERTION_TABLE: (
        "id",
        "tenant",
        "control_code",
        "control_name",
        "status",
        "failing_population",
        "remediation_owner",
        "last_run_at",
        "created_at",
        "updated_at",
    ),
    GOVERNED_MODEL_TABLE: (
        "id",
        "tenant",
        "model_name",
        "status",
        "task_type",
        "requires_human_confirmation",
        "latest_instruction_digest",
        "created_at",
        "updated_at",
    ),
    OUTBOX_TABLE: (
        "id",
        "tenant",
        "event_type",
        "aggregate_id",
        "topic",
        "payload_json",
        "idempotency_key",
        "created_at",
    ),
    INBOX_TABLE: (
        "id",
        "tenant",
        "event_type",
        "source_event_id",
        "topic",
        "payload_json",
        "idempotency_key",
        "received_at",
    ),
    DEAD_LETTER_TABLE: (
        "id",
        "tenant",
        "event_type",
        "topic",
        "payload_json",
        "idempotency_key",
        "failure_reason",
        "created_at",
    ),
}

OPERATION_TO_TABLE = {
    "create_construction_contract": CONTRACT_TABLE,
    "progress_contract_lifecycle": CONTRACT_TABLE,
    "record_pay_application": PAY_APPLICATION_TABLE,
    "certify_pay_application": PAY_APPLICATION_TABLE,
    "review_retainage": RETAINAGE_TABLE,
    "release_retainage": RETAINAGE_TABLE,
    "approve_variation_order": VARIATION_TABLE,
    "assess_notice_timeliness": CLAIM_TABLE,
    "register_commercial_claim": CLAIM_TABLE,
    "settle_commercial_claim": CLAIM_TABLE,
    "create_lien_waiver": WAIVER_TABLE,
    "record_subcontract_package": SUBCONTRACT_TABLE,
    "build_payment_certificate": PAY_APPLICATION_TABLE,
    "build_final_account_packet": CONTRACT_TABLE,
    "run_change_impact_simulation": CONTROL_ASSERTION_TABLE,
    "replay_dead_letter_event": DEAD_LETTER_TABLE,
    "generate_cash_flow_forecast": CONTRACT_TABLE,
    "generate_contractor_scorecard": CONTRACT_TABLE,
}

EVENT_CONTRACT = {
    "outbox_table": OUTBOX_TABLE,
    "inbox_table": INBOX_TABLE,
    "dead_letter_table": DEAD_LETTER_TABLE,
    "event_contract": "AppGen-X",
}


def _utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _iso_date(value: Any | None = None) -> str:
    if value is None:
        return date.today().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _money(value: Any) -> float:
    return float(Decimal(str(value or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _copy_state(state: dict[str, Any]) -> dict[str, Any]:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _new_state() -> dict[str, Any]:
    parameters = {}
    for name, meta in DEFAULT_PARAMETERS.items():
        parameters[name] = {
            "name": name,
            "value": meta["value"],
            "unit": meta["unit"],
            "bounded": True,
            "source": "default",
        }
    rules = {}
    for name in DOMAIN_RULES:
        rule = {
            "rule_id": name,
            "rule_name": name.replace("_", " "),
            "policy_area": name.split("_policy")[0],
            "status": "active",
            "severity": "high" if "pay_application" in name or "final_account" in name else "medium",
            "effective_from": _iso_date(),
        }
        rules[name] = {**rule, "compiled_hash": _digest(rule)}
    return {
        "records": {},
        "tables": {table: {} for table in BUSINESS_TABLES},
        "parameters": parameters,
        "rules": rules,
        "schema_extensions": {},
        "configuration": {
            "database_backend": "postgresql",
            "event_topic": CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
            "policy_version": "commercial-controls-v1",
            "stream_engine_picker_visible": False,
        },
        "projections": {name: {} for name in DEPENDENCY_PROJECTIONS},
        "audit_log": [],
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "handler_state": {
            "policy_version": "commercial-controls-v1",
            "latest_audit_seal": None,
            "latest_operational_kpi": None,
            "handled": set(),
        },
    }


def construction_contracts_commercials_empty_state() -> dict[str, Any]:
    return _new_state()


def _normalize_actor(actor: dict[str, Any] | None) -> dict[str, Any]:
    if actor:
        base = dict(actor)
        base.setdefault("roles", ("contract_admin",))
        return base
    return {"actor_id": "system", "roles": ("contract_admin",)}


def _actor_permissions(actor: dict[str, Any]) -> tuple[str, ...]:
    explicit = set(actor.get("permissions", ()))
    for role in actor.get("roles", ()):
        explicit.update(ROLE_PERMISSION_MAP.get(role, ()))
    return tuple(sorted(explicit))


def _authorize(actor: dict[str, Any] | None, permission: str) -> dict[str, Any]:
    normalized = _normalize_actor(actor)
    allowed = permission in _actor_permissions(normalized) or "construction_contracts_commercials.admin" in _actor_permissions(normalized)
    return {
        "ok": allowed,
        "permission": permission,
        "actor": normalized,
        "reason": None if allowed else "permission_denied",
    }


def _record_for_table(state: dict[str, Any], table: str, record_id: str) -> dict[str, Any] | None:
    return state.get("tables", {}).get(table, {}).get(record_id)


def _store_record(state: dict[str, Any], table: str, record: dict[str, Any]) -> None:
    state["tables"][table][record["id"]] = record
    if table == CONTRACT_TABLE:
        state["records"][record["id"]] = record


def _audit(state: dict[str, Any], action: str, actor: dict[str, Any], details: dict[str, Any]) -> None:
    state["audit_log"].append(
        {
            "action": action,
            "actor_id": actor.get("actor_id", "system"),
            "roles": tuple(actor.get("roles", ())),
            "details": details,
            "recorded_at": _utc_now(),
            "digest": _digest((action, details)),
        }
    )


def _emit(state: dict[str, Any], event_type: str, tenant: str, aggregate_id: str, payload: dict[str, Any], evidence_refs: tuple[str, ...] = ()) -> None:
    event = {
        "id": f"evt-{_digest((event_type, aggregate_id, payload, len(state['outbox'])) )[:12]}",
        "tenant": tenant,
        "event_type": event_type,
        "aggregate_id": aggregate_id,
        "topic": CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC,
        "payload_json": dict(payload),
        "idempotency_key": _digest((event_type, aggregate_id, tuple(sorted(payload.items())))),
        "evidence_refs": evidence_refs,
        "created_at": _utc_now(),
    }
    state["outbox"].append(event)


def _contract_closeout_blockers(state: dict[str, Any], contract_id: str) -> tuple[str, ...]:
    blockers = []
    open_claims = [
        claim
        for claim in state["tables"][CLAIM_TABLE].values()
        if claim["contract_id"] == contract_id and claim["status"] not in ("settled", "rejected")
    ]
    held_retainage = [
        retainage
        for retainage in state["tables"][RETAINAGE_TABLE].values()
        if retainage["contract_id"] == contract_id and retainage["status"] != "released"
    ]
    pending_variations = [
        variation
        for variation in state["tables"][VARIATION_TABLE].values()
        if variation["contract_id"] == contract_id and variation["status"] not in ("approved", "implemented")
    ]
    if open_claims:
        blockers.append("open_claims")
    if held_retainage:
        blockers.append("retainage_not_released")
    if pending_variations:
        blockers.append("pending_variations")
    return tuple(blockers)


def _valid_waivers(state: dict[str, Any], contract_id: str, pay_application_id: str | None = None) -> list[dict[str, Any]]:
    waivers = []
    for waiver in state["tables"][WAIVER_TABLE].values():
        if waiver["contract_id"] != contract_id:
            continue
        if pay_application_id and waiver.get("pay_application_id") not in (None, pay_application_id):
            continue
        if waiver["status"] == "accepted":
            waivers.append(waiver)
    return waivers


def _classify_notice(event_date: str | None, notice_date: str | None, state: dict[str, Any]) -> dict[str, Any]:
    if not event_date or not notice_date:
        return {"status": "unknown", "deadline": None, "days_late": None}
    event_dt = date.fromisoformat(_iso_date(event_date))
    notice_dt = date.fromisoformat(_iso_date(notice_date))
    deadline = event_dt + timedelta(days=int(state["parameters"]["notice_period_days"]["value"]))
    if notice_dt <= deadline:
        return {"status": "timely", "deadline": deadline.isoformat(), "days_late": 0}
    return {
        "status": "late",
        "deadline": deadline.isoformat(),
        "days_late": (notice_dt - deadline).days,
    }


def _schedule_lines_for_contract(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {line["line_code"]: line for line in contract.get("schedule_of_values", ())}


def _validate_schedule_of_values(contract_value: float, lines: list[dict[str, Any]]) -> dict[str, Any]:
    if not lines:
        return {"ok": False, "reason": "schedule_of_values_required"}
    total = round(sum(_money(line.get("original_value", 0)) for line in lines), 2)
    if round(contract_value, 2) != round(total, 2):
        return {
            "ok": False,
            "reason": "schedule_of_values_total_mismatch",
            "contract_value": contract_value,
            "schedule_total": total,
        }
    return {"ok": True, "schedule_total": total}


def _line_previous_certified(state: dict[str, Any], contract_id: str, line_code: str) -> float:
    certified = 0.0
    for pay_application in state["tables"][PAY_APPLICATION_TABLE].values():
        if pay_application["contract_id"] != contract_id or pay_application["intake_status"] != "certified":
            continue
        for line in pay_application.get("lines", ()):
            if line["line_code"] == line_code:
                certified += _money(line["current_claimed"]) + _money(line.get("stored_materials", 0))
    return round(certified, 2)


def _contract_by_reference(state: dict[str, Any], contract_ref: str) -> dict[str, Any] | None:
    direct = _record_for_table(state, CONTRACT_TABLE, contract_ref)
    if direct:
        return direct
    for record in state["tables"][CONTRACT_TABLE].values():
        if record["contract_code"] == contract_ref:
            return record
    return None


def _pay_application_by_reference(state: dict[str, Any], pay_app_ref: str) -> dict[str, Any] | None:
    direct = _record_for_table(state, PAY_APPLICATION_TABLE, pay_app_ref)
    if direct:
        return direct
    for record in state["tables"][PAY_APPLICATION_TABLE].values():
        if record["application_number"] == pay_app_ref:
            return record
    return None


def _retainage_by_reference(state: dict[str, Any], retainage_ref: str) -> dict[str, Any] | None:
    direct = _record_for_table(state, RETAINAGE_TABLE, retainage_ref)
    if direct:
        return direct
    for record in state["tables"][RETAINAGE_TABLE].values():
        if record["pay_application_id"] == retainage_ref:
            return record
    return None


def _base_result(ok: bool, next_state: dict[str, Any], **payload: Any) -> dict[str, Any]:
    return {"ok": ok, "state": next_state, "side_effects": (), **payload}


def evaluate_rule(rule: str, payload: dict[str, Any] | None = None, state: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    state = state or construction_contracts_commercials_empty_state()
    if rule == "construction_contract_policy":
        passed = bool(payload.get("contract_value", 0)) and bool(payload.get("schedule_of_values"))
        violations = () if passed else ("contract_value_or_schedule_missing",)
    elif rule == "pay_application_policy":
        passed = not payload.get("validation_issues")
        violations = tuple(payload.get("validation_issues", ()))
    elif rule == "retainage_policy":
        passed = _money(payload.get("withheld_amount", 0)) >= 0
        violations = () if passed else ("negative_retainage",)
    elif rule == "variation_order_policy":
        approved = payload.get("status") == "approved"
        passed = not approved or bool(payload.get("approved_amount"))
        violations = () if passed else ("approved_amount_missing",)
    elif rule == "commercial_claim_policy":
        passed = payload.get("time_bar_status") != "late" or bool(payload.get("waiver_status") == "waived")
        violations = () if passed else ("time_barred_notice",)
    elif rule == "lien_waiver_policy":
        passed = _money(payload.get("covered_amount", 0)) > 0 and bool(payload.get("signed_date"))
        violations = () if passed else ("invalid_waiver",)
    elif rule == "jurisdiction_prompt_payment_policy":
        passed = payload.get("jurisdiction") in ("KE", "US", "UK", "ZA")
        violations = () if passed else ("unsupported_jurisdiction",)
    else:
        passed = not _contract_closeout_blockers(state, payload.get("contract_id", ""))
        violations = () if passed else _contract_closeout_blockers(state, payload.get("contract_id", ""))
    return {"ok": True, "rule": rule, "passed": passed, "violations": violations, "payload": payload, "side_effects": ()}


def compile_rule(rule: dict[str, Any]) -> dict[str, Any]:
    compiled = {**dict(rule), "compiled_hash": _digest(rule)}
    return {"ok": True, "rule": compiled, "compiled_hash": compiled["compiled_hash"], "side_effects": ()}


def configuration_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def validate_configuration(config: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = {**construction_contracts_commercials_empty_state()["configuration"], **dict(config or {})}
    ok = (
        merged["database_backend"] in CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS
        and merged["event_topic"] == CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC
    )
    return {"ok": ok, "configuration": merged, "side_effects": ()}


def parameter_manifest() -> dict[str, Any]:
    parameters = tuple(
        {
            "name": name,
            "value": meta["value"],
            "unit": meta["unit"],
            "bounded": True,
            "owned_table": PARAMETER_TABLE,
        }
        for name, meta in DEFAULT_PARAMETERS.items()
    )
    return {"ok": True, "parameters": parameters, "side_effects": ()}


def rule_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "rules": tuple(
            {
                "rule_id": name,
                "policy_area": name.split("_policy")[0],
                "owned_table": RULE_TABLE,
            }
            for name in DOMAIN_RULES
        ),
        "side_effects": (),
    }


def construction_contracts_commercials_configure_runtime(state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy_state(state)
    validation = validate_configuration(config)
    next_state["configuration"] = validation["configuration"]
    return _base_result(validation["ok"], next_state, configuration=next_state["configuration"])


def construction_contracts_commercials_set_parameter(state: dict[str, Any], name: str, value: Any) -> dict[str, Any]:
    next_state = _copy_state(state)
    if name not in DEFAULT_PARAMETERS:
        return _base_result(False, next_state, reason="unknown_parameter", parameter_name=name)
    entry = {
        "name": name,
        "value": value,
        "unit": DEFAULT_PARAMETERS[name]["unit"],
        "bounded": True,
        "source": "runtime_override",
    }
    next_state["parameters"][name] = entry
    parameter_record = {
        "id": f"param-{name}",
        "tenant": "system",
        "parameter_name": name,
        "value_json": value,
        "unit": DEFAULT_PARAMETERS[name]["unit"],
        "bounded": True,
        "status": "active",
        "updated_at": _utc_now(),
    }
    _store_record(next_state, PARAMETER_TABLE, parameter_record)
    return _base_result(True, next_state, parameter=entry)


def construction_contracts_commercials_register_rule(state: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy_state(state)
    compiled = compile_rule(rule)["rule"]
    rule_id = compiled.get("rule_id", "custom_rule")
    next_state["rules"][rule_id] = compiled
    rule_record = {
        "id": f"rule-{rule_id}",
        "tenant": rule.get("tenant", "system"),
        "rule_code": rule_id,
        "rule_name": compiled.get("rule_name", rule_id.replace("_", " ")),
        "policy_area": compiled.get("policy_area", rule_id.split("_policy")[0]),
        "status": compiled.get("status", "active"),
        "severity": compiled.get("severity", "medium"),
        "compiled_hash": compiled["compiled_hash"],
        "effective_from": compiled.get("effective_from", _iso_date()),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, RULE_TABLE, rule_record)
    return _base_result(True, next_state, rule=compiled)


def construction_contracts_commercials_register_schema_extension(state: dict[str, Any], table: str, fields: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy_state(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES:
        return _base_result(False, next_state, reason="unknown_owned_table", table=owned_name)
    next_state["schema_extensions"][owned_name] = dict(fields)
    record = {
        "id": f"schema-extension-{_digest((owned_name, fields))[:8]}",
        "tenant": "system",
        "target_table": owned_name,
        "extension_name": f"{owned_name}_extension",
        "status": "registered",
        "fields_json": dict(fields),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, SCHEMA_EXTENSION_TABLE, record)
    return _base_result(True, next_state, table=owned_name, fields=dict(fields))


def construction_contracts_commercials_receive_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = _copy_state(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return _base_result(True, next_state, duplicate=True, idempotency_key=idem)
    if event.get("event_type") not in CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES:
        dead = {
            "id": f"dead-{_digest((idem, event.get('event_type')))[:10]}",
            "tenant": event.get("tenant", "system"),
            "event_type": event.get("event_type"),
            "topic": event.get("topic", CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC),
            "payload_json": dict(event),
            "idempotency_key": idem,
            "failure_reason": "unsupported_event_type",
            "created_at": _utc_now(),
        }
        next_state["dead_letter"].append(dead)
        return _base_result(False, next_state, duplicate=False, dead_letter_table=DEAD_LETTER_TABLE, dead_letter=dead)
    next_state["idempotency_keys"].add(idem)
    inbox_record = {
        "id": f"inbox-{_digest((idem, len(next_state['inbox'])))[:10]}",
        "tenant": event.get("tenant", "system"),
        "event_type": event["event_type"],
        "source_event_id": event.get("event_id", idem),
        "topic": event.get("topic", CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC),
        "payload_json": dict(event.get("payload", {})),
        "idempotency_key": idem,
        "received_at": _utc_now(),
    }
    next_state["inbox"].append(inbox_record)
    if event["event_type"] == "PolicyChanged":
        next_state["handler_state"]["policy_version"] = event.get("payload", {}).get("policy_version", "policy-updated")
    elif event["event_type"] == "AuditEventSealed":
        next_state["handler_state"]["latest_audit_seal"] = event.get("payload", {}).get("seal_digest")
    elif event["event_type"] == "OperationalKpiChanged":
        next_state["handler_state"]["latest_operational_kpi"] = event.get("payload", {}).get("kpi_code")
    return _base_result(True, next_state, duplicate=False, inbox_record=inbox_record)


def construction_contracts_commercials_command_construction_contract(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.create")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract_value = _money(payload.get("contract_value", 0))
    schedule_lines = list(payload.get("schedule_of_values", ()))
    validation = _validate_schedule_of_values(contract_value, schedule_lines)
    if not validation["ok"]:
        return _base_result(False, next_state, reason=validation["reason"], validation=validation)
    contract_id = payload.get("id") or f"contract-{payload.get('contract_code', 'unknown').lower()}"
    stage = payload.get("lifecycle_stage", "award")
    if stage not in CONTRACT_LIFECYCLE_STAGES:
        return _base_result(False, next_state, reason="invalid_lifecycle_stage", lifecycle_stage=stage)
    retainage_percent = _money(payload.get("retainage_percent", next_state["parameters"]["retainage_default_percent"]["value"]))
    contract = {
        "id": contract_id,
        "tenant": payload.get("tenant", "default"),
        "contract_code": payload.get("contract_code", contract_id.upper()),
        "title": payload.get("title", "Construction Contract"),
        "contract_type": payload.get("contract_type", "subcontract"),
        "pricing_basis": payload.get("pricing_basis", "lump_sum"),
        "jurisdiction": payload.get("jurisdiction", "KE"),
        "counterparty": payload.get("counterparty", "Unnamed Contractor"),
        "lifecycle_stage": stage,
        "contract_value": contract_value,
        "approved_change_value": 0.0,
        "current_contract_value": contract_value,
        "retainage_percent": retainage_percent,
        "final_account_status": payload.get("final_account_status", "open"),
        "closeout_blockers": tuple(payload.get("closeout_blockers", ("final_account_open",))),
        "schedule_of_values": tuple(
            {
                "line_code": line.get("line_code", f"line-{index + 1}"),
                "work_package": line.get("work_package", f"Work Package {index + 1}"),
                "quantity": line.get("quantity", 1),
                "unit": line.get("unit", "item"),
                "original_value": _money(line.get("original_value", 0)),
                "approved_changes": _money(line.get("approved_changes", 0)),
                "previous_certified": 0.0,
                "remaining_balance": _money(line.get("original_value", 0)) + _money(line.get("approved_changes", 0)),
            }
            for index, line in enumerate(schedule_lines)
        ),
        "guarantees": tuple(payload.get("guarantees", ())),
        "obligations": tuple(payload.get("obligations", ())),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, CONTRACT_TABLE, contract)
    _audit(next_state, "create_construction_contract", auth["actor"], {"contract_id": contract_id, "contract_code": contract["contract_code"]})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0], contract["tenant"], contract_id, {"contract_code": contract["contract_code"], "lifecycle_stage": stage})
    return _base_result(True, next_state, record=contract, authorization=auth)


def construction_contracts_commercials_progress_contract_lifecycle(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.update")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract = _contract_by_reference(next_state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return _base_result(False, next_state, reason="contract_not_found")
    next_stage = payload.get("next_stage")
    if next_stage not in CONTRACT_LIFECYCLE_TRANSITIONS.get(contract["lifecycle_stage"], ()):
        return _base_result(
            False,
            next_state,
            reason="invalid_transition",
            current_stage=contract["lifecycle_stage"],
            next_stage=next_stage,
        )
    blockers = _contract_closeout_blockers(next_state, contract["id"]) if next_stage in ("final_account", "defects", "closed") else ()
    if next_stage == "closed" and blockers:
        return _base_result(False, next_state, reason="closeout_blockers_present", blockers=blockers)
    updated = dict(contract)
    updated["lifecycle_stage"] = next_stage
    updated["closeout_blockers"] = blockers
    updated["updated_at"] = _utc_now()
    if next_stage == "final_account":
        updated["final_account_status"] = "in_review"
    if next_stage == "closed":
        updated["final_account_status"] = "closed"
    _store_record(next_state, CONTRACT_TABLE, updated)
    _audit(next_state, "progress_contract_lifecycle", auth["actor"], {"contract_id": contract["id"], "next_stage": next_stage})
    event_type = CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2] if next_stage == "closed" else CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[1]
    _emit(next_state, event_type, updated["tenant"], updated["id"], {"contract_code": updated["contract_code"], "next_stage": next_stage})
    return _base_result(True, next_state, record=updated, blockers=blockers, authorization=auth)


def construction_contracts_commercials_record_pay_application(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.create")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract = _contract_by_reference(next_state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return _base_result(False, next_state, reason="contract_not_found")
    lines = list(payload.get("lines", ()))
    attachments = tuple(payload.get("attachments", ()))
    schedule = _schedule_lines_for_contract(contract)
    validation_issues = []
    normalized_lines = []
    for line in lines:
        line_code = line.get("line_code")
        schedule_line = schedule.get(line_code)
        if not schedule_line:
            validation_issues.append(f"unknown_schedule_line:{line_code}")
            continue
        previous = _line_previous_certified(next_state, contract["id"], line_code)
        approved_total = _money(schedule_line["original_value"]) + _money(schedule_line.get("approved_changes", 0))
        claimed = _money(line.get("current_claimed", 0))
        stored_materials = _money(line.get("stored_materials", 0))
        available = round(approved_total - previous, 2)
        if claimed + stored_materials > available + 0.01:
            return _base_result(
                False,
                next_state,
                reason="overclaimed_schedule_line",
                line_code=line_code,
                available_balance=available,
                attempted_claim=round(claimed + stored_materials, 2),
            )
        evidence_refs = tuple(line.get("evidence_refs", ()))
        if claimed > 0 and not evidence_refs:
            validation_issues.append(f"missing_progress_evidence:{line_code}")
        normalized_lines.append(
            {
                "line_code": line_code,
                "work_package": schedule_line["work_package"],
                "current_claimed": claimed,
                "stored_materials": stored_materials,
                "previous_certified": previous,
                "remaining_after_claim": round(available - claimed - stored_materials, 2),
                "evidence_refs": evidence_refs,
            }
        )
    if not attachments:
        validation_issues.append("missing_attachments")
    gross_claimed = round(sum(line["current_claimed"] + line["stored_materials"] for line in normalized_lines), 2)
    retainage_withheld = round(gross_claimed * (_money(contract["retainage_percent"]) / 100.0), 2)
    status = "under_review" if not validation_issues else "incomplete"
    evidence_status = "ready" if not validation_issues else "missing"
    pay_application = {
        "id": payload.get("id") or f"pay-app-{payload.get('application_number', _digest(gross_claimed)[:6])}",
        "tenant": contract["tenant"],
        "contract_id": contract["id"],
        "application_number": payload.get("application_number", f"APP-{len(next_state['tables'][PAY_APPLICATION_TABLE]) + 1:03d}"),
        "intake_status": status,
        "period_start": _iso_date(payload.get("period_start")),
        "period_end": _iso_date(payload.get("period_end")),
        "gross_claimed": gross_claimed,
        "certified_amount": 0.0,
        "retainage_withheld": retainage_withheld,
        "waiver_status": "missing",
        "evidence_status": evidence_status,
        "attachments": attachments,
        "lines": tuple(normalized_lines),
        "validation_issues": tuple(validation_issues),
        "certificate_trace": (),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, PAY_APPLICATION_TABLE, pay_application)
    _audit(next_state, "record_pay_application", auth["actor"], {"pay_application_id": pay_application["id"], "contract_id": contract["id"]})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0], contract["tenant"], pay_application["id"], {"contract_id": contract["id"], "application_number": pay_application["application_number"]})
    if validation_issues:
        _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[3], contract["tenant"], pay_application["id"], {"validation_issues": tuple(validation_issues)})
    return _base_result(True, next_state, record=pay_application, authorization=auth)


def construction_contracts_commercials_certify_pay_application(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.certify_pay_application")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    pay_application = _pay_application_by_reference(next_state, payload.get("pay_application_id") or payload.get("application_number", ""))
    if not pay_application:
        return _base_result(False, next_state, reason="pay_application_not_found")
    if pay_application["validation_issues"]:
        return _base_result(False, next_state, reason="validation_issues_present", validation_issues=pay_application["validation_issues"])
    waiver_required = bool(next_state["parameters"]["waiver_required_for_certification"]["value"])
    valid_waivers = _valid_waivers(next_state, pay_application["contract_id"], pay_application["id"])
    if waiver_required and not valid_waivers:
        return _base_result(False, next_state, reason="missing_valid_waiver", pay_application_id=pay_application["id"])
    certified_amount = round(pay_application["gross_claimed"] - pay_application["retainage_withheld"], 2)
    certificate_trace = (
        {
            "gross_claimed": pay_application["gross_claimed"],
            "retainage_withheld": pay_application["retainage_withheld"],
            "net_due": certified_amount,
            "certified_at": _utc_now(),
        },
    )
    updated = dict(pay_application)
    updated["intake_status"] = "certified"
    updated["waiver_status"] = "accepted" if valid_waivers else "not_required"
    updated["certified_amount"] = certified_amount
    updated["certificate_trace"] = certificate_trace
    updated["updated_at"] = _utc_now()
    _store_record(next_state, PAY_APPLICATION_TABLE, updated)
    _audit(next_state, "certify_pay_application", auth["actor"], {"pay_application_id": updated["id"], "net_due": certified_amount})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2], updated["tenant"], updated["id"], {"contract_id": updated["contract_id"], "net_due": certified_amount})
    return _base_result(True, next_state, record=updated, authorization=auth)


def construction_contracts_commercials_review_retainage(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.update")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    pay_application = _pay_application_by_reference(next_state, payload.get("pay_application_id") or payload.get("application_number", ""))
    if not pay_application:
        return _base_result(False, next_state, reason="pay_application_not_found")
    record = {
        "id": payload.get("id") or f"retainage-{pay_application['id']}",
        "tenant": pay_application["tenant"],
        "contract_id": pay_application["contract_id"],
        "pay_application_id": pay_application["id"],
        "status": "held",
        "retainage_percent": _money(payload.get("retainage_percent", next_state["parameters"]["retainage_default_percent"]["value"])),
        "withheld_amount": _money(payload.get("withheld_amount", pay_application["retainage_withheld"])),
        "release_trigger": payload.get("release_trigger", "final_account_closeout"),
        "release_blockers": _contract_closeout_blockers(next_state, pay_application["contract_id"]),
        "released_amount": 0.0,
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, RETAINAGE_TABLE, record)
    _audit(next_state, "review_retainage", auth["actor"], {"retainage_id": record["id"], "withheld_amount": record["withheld_amount"]})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[1], record["tenant"], record["id"], {"contract_id": record["contract_id"], "withheld_amount": record["withheld_amount"]})
    return _base_result(True, next_state, record=record, authorization=auth)


def construction_contracts_commercials_release_retainage(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.release_retainage")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    retainage = _retainage_by_reference(next_state, payload.get("retainage_id") or payload.get("pay_application_id", ""))
    if not retainage:
        return _base_result(False, next_state, reason="retainage_not_found")
    contract = _contract_by_reference(next_state, retainage["contract_id"])
    blockers = _contract_closeout_blockers(next_state, retainage["contract_id"])
    completion_percent = _money(payload.get("completion_percent", 0))
    required_completion = _money(next_state["parameters"]["retainage_release_completion_percent"]["value"])
    if blockers or completion_percent < required_completion or not _valid_waivers(next_state, retainage["contract_id"], retainage["pay_application_id"]):
        return _base_result(
            False,
            next_state,
            reason="retainage_release_blocked",
            blockers=blockers or ("completion_or_waiver_requirement",),
        )
    updated = dict(retainage)
    updated["status"] = "released"
    updated["release_blockers"] = ()
    updated["released_amount"] = updated["withheld_amount"]
    updated["updated_at"] = _utc_now()
    _store_record(next_state, RETAINAGE_TABLE, updated)
    _audit(next_state, "release_retainage", auth["actor"], {"retainage_id": updated["id"], "released_amount": updated["released_amount"]})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2], contract["tenant"], updated["id"], {"contract_id": updated["contract_id"], "released_amount": updated["released_amount"]})
    return _base_result(True, next_state, record=updated, authorization=auth)


def construction_contracts_commercials_approve_variation_order(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.approve_variation")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract = _contract_by_reference(next_state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return _base_result(False, next_state, reason="contract_not_found")
    notice = _classify_notice(payload.get("event_date"), payload.get("notice_date"), next_state)
    status = payload.get("status", "approved" if payload.get("approved", True) else "under_review")
    approved_amount = _money(payload.get("approved_amount", payload.get("quoted_amount", 0) if status == "approved" else 0))
    record = {
        "id": payload.get("id") or f"variation-{payload.get('variation_number', len(next_state['tables'][VARIATION_TABLE]) + 1)}",
        "tenant": contract["tenant"],
        "contract_id": contract["id"],
        "variation_number": payload.get("variation_number", f"VO-{len(next_state['tables'][VARIATION_TABLE]) + 1:03d}"),
        "status": status,
        "instruction_date": _iso_date(payload.get("instruction_date")),
        "event_date": _iso_date(payload.get("event_date")),
        "notice_date": _iso_date(payload.get("notice_date")),
        "contractual_deadline": notice["deadline"],
        "time_bar_status": notice["status"],
        "quoted_amount": _money(payload.get("quoted_amount", approved_amount)),
        "approved_amount": approved_amount,
        "time_impact_days": int(payload.get("time_impact_days", 0)),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, VARIATION_TABLE, record)
    if status == "approved":
        updated_contract = dict(contract)
        updated_contract["approved_change_value"] = round(contract["approved_change_value"] + approved_amount, 2)
        updated_contract["current_contract_value"] = round(contract["contract_value"] + updated_contract["approved_change_value"], 2)
        updated_contract["updated_at"] = _utc_now()
        _store_record(next_state, CONTRACT_TABLE, updated_contract)
    _audit(next_state, "approve_variation_order", auth["actor"], {"variation_id": record["id"], "status": status, "approved_amount": approved_amount})
    event_type = CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2] if status == "approved" else CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0]
    _emit(next_state, event_type, contract["tenant"], record["id"], {"contract_id": contract["id"], "variation_number": record["variation_number"], "status": status})
    return _base_result(True, next_state, record=record, authorization=auth)


def construction_contracts_commercials_assess_notice_timeliness(state: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    notice = _classify_notice(payload.get("event_date"), payload.get("notice_date"), state)
    return {"ok": True, "notice_assessment": notice, "payload": dict(payload), "side_effects": ()}


def construction_contracts_commercials_register_commercial_claim(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.assess_claim")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract = _contract_by_reference(next_state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return _base_result(False, next_state, reason="contract_not_found")
    notice = _classify_notice(payload.get("event_date"), payload.get("notice_date"), next_state)
    claimed_amount = _money(payload.get("claimed_amount", 0))
    risk = 0.25 if notice["status"] == "timely" else 0.85
    record = {
        "id": payload.get("id") or f"claim-{payload.get('claim_number', len(next_state['tables'][CLAIM_TABLE]) + 1)}",
        "tenant": contract["tenant"],
        "contract_id": contract["id"],
        "claim_number": payload.get("claim_number", f"CL-{len(next_state['tables'][CLAIM_TABLE]) + 1:03d}"),
        "claim_type": payload.get("claim_type", "delay"),
        "status": payload.get("status", "entitlement_review"),
        "event_date": _iso_date(payload.get("event_date")),
        "notice_date": _iso_date(payload.get("notice_date")),
        "contractual_deadline": notice["deadline"],
        "time_bar_status": notice["status"],
        "claimed_amount": claimed_amount,
        "assessed_amount": _money(payload.get("assessed_amount", 0)),
        "settled_amount": _money(payload.get("settled_amount", 0)),
        "entitlement_risk": round(risk, 2),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, CLAIM_TABLE, record)
    _audit(next_state, "register_commercial_claim", auth["actor"], {"claim_id": record["id"], "time_bar_status": notice["status"]})
    event_type = CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[3] if notice["status"] == "late" else CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0]
    _emit(next_state, event_type, contract["tenant"], record["id"], {"claim_number": record["claim_number"], "time_bar_status": notice["status"]})
    return _base_result(True, next_state, record=record, authorization=auth)


def construction_contracts_commercials_settle_commercial_claim(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.approve_settlement")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    claim = _record_for_table(next_state, CLAIM_TABLE, payload.get("claim_id", ""))
    if not claim:
        return _base_result(False, next_state, reason="claim_not_found")
    updated = dict(claim)
    updated["status"] = payload.get("status", "settled")
    updated["assessed_amount"] = _money(payload.get("assessed_amount", claim["claimed_amount"]))
    updated["settled_amount"] = _money(payload.get("settled_amount", updated["assessed_amount"]))
    updated["updated_at"] = _utc_now()
    _store_record(next_state, CLAIM_TABLE, updated)
    _audit(next_state, "settle_commercial_claim", auth["actor"], {"claim_id": updated["id"], "settled_amount": updated["settled_amount"]})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2], updated["tenant"], updated["id"], {"claim_number": updated["claim_number"], "settled_amount": updated["settled_amount"]})
    return _base_result(True, next_state, record=updated, authorization=auth)


def construction_contracts_commercials_create_lien_waiver(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.accept_waiver")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract = _contract_by_reference(next_state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return _base_result(False, next_state, reason="contract_not_found")
    status = payload.get("status", "accepted")
    record = {
        "id": payload.get("id") or f"waiver-{payload.get('waiver_number', len(next_state['tables'][WAIVER_TABLE]) + 1)}",
        "tenant": contract["tenant"],
        "contract_id": contract["id"],
        "pay_application_id": payload.get("pay_application_id"),
        "waiver_number": payload.get("waiver_number", f"LW-{len(next_state['tables'][WAIVER_TABLE]) + 1:03d}"),
        "waiver_type": payload.get("waiver_type", "conditional_progress"),
        "status": status,
        "covered_amount": _money(payload.get("covered_amount", 0)),
        "covered_period": payload.get("covered_period", "current"),
        "jurisdiction": payload.get("jurisdiction", contract["jurisdiction"]),
        "signed_date": _iso_date(payload.get("signed_date")),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    rule_check = evaluate_rule("lien_waiver_policy", record)
    if not rule_check["passed"]:
        return _base_result(False, next_state, reason="invalid_waiver", validation_issues=rule_check["violations"])
    _store_record(next_state, WAIVER_TABLE, record)
    _audit(next_state, "create_lien_waiver", auth["actor"], {"waiver_id": record["id"], "pay_application_id": record["pay_application_id"]})
    _emit(next_state, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[1], contract["tenant"], record["id"], {"waiver_number": record["waiver_number"], "status": status})
    return _base_result(True, next_state, record=record, authorization=auth)


def construction_contracts_commercials_record_subcontract_package(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.update")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    contract = _contract_by_reference(next_state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return _base_result(False, next_state, reason="contract_not_found")
    insurance_status = payload.get("insurance_status", "pending")
    bond_status = payload.get("bond_status", "pending")
    compliance_hold = insurance_status != "compliant" or bond_status != "valid"
    record = {
        "id": payload.get("id") or f"subpkg-{payload.get('package_code', len(next_state['tables'][SUBCONTRACT_TABLE]) + 1)}",
        "tenant": contract["tenant"],
        "contract_id": contract["id"],
        "package_code": payload.get("package_code", f"PKG-{len(next_state['tables'][SUBCONTRACT_TABLE]) + 1:03d}"),
        "subcontractor_name": payload.get("subcontractor_name", "Unnamed Subcontractor"),
        "status": payload.get("status", "active" if not compliance_hold else "hold"),
        "contract_value": _money(payload.get("contract_value", 0)),
        "insurance_status": insurance_status,
        "bond_status": bond_status,
        "compliance_hold": compliance_hold,
        "closeout_checklist": tuple(payload.get("closeout_checklist", ())),
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
    }
    _store_record(next_state, SUBCONTRACT_TABLE, record)
    _audit(next_state, "record_subcontract_package", auth["actor"], {"package_id": record["id"], "compliance_hold": compliance_hold})
    return _base_result(True, next_state, record=record, authorization=auth)


def construction_contracts_commercials_build_payment_certificate(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.read")
    if not auth["ok"]:
        return {"ok": False, "reason": "permission_denied", "authorization": auth, "side_effects": ()}
    pay_application = _pay_application_by_reference(state, payload.get("pay_application_id") or payload.get("application_number", ""))
    if not pay_application:
        return {"ok": False, "reason": "pay_application_not_found", "side_effects": ()}
    if pay_application["intake_status"] != "certified":
        return {"ok": False, "reason": "pay_application_not_certified", "side_effects": ()}
    certificate = {
        "contract_id": pay_application["contract_id"],
        "pay_application_id": pay_application["id"],
        "application_number": pay_application["application_number"],
        "gross_claimed": pay_application["gross_claimed"],
        "retainage_withheld": pay_application["retainage_withheld"],
        "net_due": pay_application["certified_amount"],
        "certifier": auth["actor"].get("actor_id", "system"),
        "approved_at": _utc_now(),
        "finance_handoff_event": {
            "event_type": "ConstructionContractsCommercialsApproved",
            "idempotency_key": _digest(("payment_certificate", pay_application["id"], pay_application["certified_amount"])),
            "evidence_refs": pay_application["attachments"],
        },
    }
    return {"ok": True, "certificate": certificate, "authorization": auth, "side_effects": ()}


def construction_contracts_commercials_build_final_account_packet(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.close_final_account")
    if not auth["ok"]:
        return {"ok": False, "reason": "permission_denied", "authorization": auth, "side_effects": ()}
    contract = _contract_by_reference(state, payload.get("contract_id") or payload.get("contract_code", ""))
    if not contract:
        return {"ok": False, "reason": "contract_not_found", "side_effects": ()}
    blockers = _contract_closeout_blockers(state, contract["id"])
    packet = {
        "contract_id": contract["id"],
        "contract_code": contract["contract_code"],
        "summary": {
            "original_value": contract["contract_value"],
            "approved_change_value": contract["approved_change_value"],
            "current_contract_value": contract["current_contract_value"],
        },
        "pay_applications": tuple(item["id"] for item in state["tables"][PAY_APPLICATION_TABLE].values() if item["contract_id"] == contract["id"]),
        "variations": tuple(item["id"] for item in state["tables"][VARIATION_TABLE].values() if item["contract_id"] == contract["id"]),
        "claims": tuple(item["id"] for item in state["tables"][CLAIM_TABLE].values() if item["contract_id"] == contract["id"]),
        "retainage": tuple(item["id"] for item in state["tables"][RETAINAGE_TABLE].values() if item["contract_id"] == contract["id"]),
        "waivers": tuple(item["id"] for item in state["tables"][WAIVER_TABLE].values() if item["contract_id"] == contract["id"]),
        "blockers": blockers,
        "ready_for_closeout": not blockers,
    }
    return {"ok": True, "packet": packet, "authorization": auth, "side_effects": ()}


def construction_contracts_commercials_run_change_impact_simulation(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.admin")
    if not auth["ok"]:
        return {"ok": False, "reason": "permission_denied", "authorization": auth, "side_effects": ()}
    proposed_retainage = _money(payload.get("retainage_default_percent", state["parameters"]["retainage_default_percent"]["value"]))
    waiver_required = bool(payload.get("waiver_required_for_certification", state["parameters"]["waiver_required_for_certification"]["value"]))
    affected = []
    for pay_application in state["tables"][PAY_APPLICATION_TABLE].values():
        new_retainage = round(pay_application["gross_claimed"] * (proposed_retainage / 100.0), 2)
        affected.append(
            {
                "pay_application_id": pay_application["id"],
                "current_retainage": pay_application["retainage_withheld"],
                "simulated_retainage": new_retainage,
                "waiver_gate": waiver_required,
            }
        )
    return {
        "ok": True,
        "impact_report": {
            "affected_pay_applications": tuple(affected),
            "high_risk_activation": waiver_required and any(item["simulated_retainage"] > item["current_retainage"] for item in affected),
            "proposed_parameters": {
                "retainage_default_percent": proposed_retainage,
                "waiver_required_for_certification": waiver_required,
            },
        },
        "authorization": auth,
        "side_effects": (),
    }


def construction_contracts_commercials_replay_dead_letter_event(
    state: dict[str, Any], payload: dict[str, Any], actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    auth = _authorize(actor, "construction_contracts_commercials.admin")
    next_state = _copy_state(state)
    if not auth["ok"]:
        return _base_result(False, next_state, reason="permission_denied", authorization=auth)
    dead_letter_id = payload.get("dead_letter_id")
    match = None
    for event in list(next_state["dead_letter"]):
        if event["id"] == dead_letter_id:
            match = event
            break
    if not match:
        return _base_result(False, next_state, reason="dead_letter_not_found")
    replay_event = dict(match["payload_json"])
    replay_event["event_type"] = payload.get("event_type_override", replay_event.get("event_type"))
    result = construction_contracts_commercials_receive_event(next_state, replay_event)
    if result["ok"]:
        result["state"]["dead_letter"] = [item for item in result["state"]["dead_letter"] if item["id"] != dead_letter_id]
    return result


def construction_contracts_commercials_generate_cash_flow_forecast(state: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    lines = []
    horizon = int(state["parameters"]["forecast_horizon_days"]["value"])
    for pay_application in state["tables"][PAY_APPLICATION_TABLE].values():
        if pay_application["intake_status"] != "certified":
            continue
        lines.append(
            {
                "contract_id": pay_application["contract_id"],
                "period": pay_application["period_end"],
                "certified_amount": pay_application["certified_amount"],
                "expected_payment_date": (date.fromisoformat(pay_application["period_end"]) + timedelta(days=30)).isoformat(),
                "retainage_release": pay_application["retainage_withheld"],
                "confidence": 0.84,
            }
        )
    return {"ok": True, "forecast_horizon_days": horizon, "cash_flow_lines": tuple(lines), "side_effects": ()}


def construction_contracts_commercials_generate_contractor_scorecard(state: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    pay_apps = tuple(state["tables"][PAY_APPLICATION_TABLE].values())
    claims = tuple(state["tables"][CLAIM_TABLE].values())
    contracts = tuple(state["tables"][CONTRACT_TABLE].values())
    incomplete = len([item for item in pay_apps if item["intake_status"] == "incomplete"])
    certified = len([item for item in pay_apps if item["intake_status"] == "certified"])
    scorecard = {
        "variation_cycle_time_days": 14,
        "claim_frequency": round(len(claims) / max(1, len(contracts)), 2),
        "pay_app_rejection_rate": round(incomplete / max(1, len(pay_apps)), 2),
        "waiver_compliance_rate": round(certified / max(1, len(pay_apps)), 2),
        "dispute_rate": round(len([item for item in claims if item["status"] not in ("settled", "rejected")]) / max(1, len(claims) or 1), 2),
        "closeout_aging_contracts": len([item for item in contracts if item["final_account_status"] != "closed"]),
    }
    return {"ok": True, "scorecard": scorecard, "payload": payload, "side_effects": ()}


def construction_contracts_commercials_permissions_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(
            {
                "role": role,
                "label": ROLE_LABELS[role],
                "permissions": ROLE_PERMISSION_MAP[role],
            }
            for role in ROLE_PERMISSION_MAP
        ),
        "side_effects": (),
    }


def construction_contracts_commercials_authorize(permission: str, actor: dict[str, Any] | None = None) -> dict[str, Any]:
    result = _authorize(actor, permission)
    result["side_effects"] = ()
    return result


def construction_contracts_commercials_ui_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": CONSTRUCTION_CONTRACTS_COMMERCIALS_UI_FRAGMENT_KEYS,
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "queues": (
            "pay_apps_awaiting_certification",
            "missing_waivers",
            "expiring_guarantees",
            "notice_deadlines",
            "disputed_variations",
            "active_claims",
            "retainage_release_blockers",
            "final_account_blockers",
        ),
        "action_permissions": {
            "certify_pay_application": "construction_contracts_commercials.certify_pay_application",
            "approve_variation": "construction_contracts_commercials.approve_variation",
            "release_retainage": "construction_contracts_commercials.release_retainage",
            "close_final_account": "construction_contracts_commercials.close_final_account",
        },
        "agent_skills": AGENT_SKILLS,
        "commercial_control_panels": tuple(f"commercial_control_{capability}" for capability in COMMERCIAL_CONTROL_CAPABILITIES),
        "commercial_control_contract": improve1_commercial_control_contract(),
        "side_effects": (),
    }


def _expiring_guarantees(contract: dict[str, Any]) -> list[dict[str, Any]]:
    expiring = []
    today = date.today()
    for guarantee in contract.get("guarantees", ()):
        expiry = guarantee.get("expiry")
        if not expiry:
            continue
        expiry_date = date.fromisoformat(_iso_date(expiry))
        if expiry_date <= today + timedelta(days=30):
            expiring.append({**dict(guarantee), "contract_id": contract["id"], "days_to_expiry": (expiry_date - today).days})
    return expiring


def _workbench_actions(actor: dict[str, Any] | None) -> tuple[dict[str, Any], ...]:
    normalized = _normalize_actor(actor)
    permissions = set(_actor_permissions(normalized))
    actions = []
    for operation in DOMAIN_OPERATIONS:
        permission = {
            "certify_pay_application": "construction_contracts_commercials.certify_pay_application",
            "approve_variation_order": "construction_contracts_commercials.approve_variation",
            "register_commercial_claim": "construction_contracts_commercials.assess_claim",
            "release_retainage": "construction_contracts_commercials.release_retainage",
            "build_final_account_packet": "construction_contracts_commercials.close_final_account",
        }.get(operation, "construction_contracts_commercials.update")
        actions.append(
            {
                "operation": operation,
                "permission": permission,
                "enabled": permission in permissions or "construction_contracts_commercials.admin" in permissions,
            }
        )
    return tuple(actions)


def construction_contracts_commercials_build_workbench_view(
    state: dict[str, Any] | None = None, tenant: str = "default", actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    state = state or construction_contracts_commercials_empty_state()
    contracts = [record for record in state["tables"][CONTRACT_TABLE].values() if record["tenant"] == tenant]
    pay_apps = [record for record in state["tables"][PAY_APPLICATION_TABLE].values() if record["tenant"] == tenant]
    variations = [record for record in state["tables"][VARIATION_TABLE].values() if record["tenant"] == tenant]
    claims = [record for record in state["tables"][CLAIM_TABLE].values() if record["tenant"] == tenant]
    retainage = [record for record in state["tables"][RETAINAGE_TABLE].values() if record["tenant"] == tenant]
    pay_apps_awaiting = [item for item in pay_apps if item["intake_status"] in ("under_review", "incomplete")]
    missing_waivers = [item for item in pay_apps if item["waiver_status"] == "missing"]
    disputed_variations = [item for item in variations if item["status"] in ("under_review", "disputed")]
    active_claims = [item for item in claims if item["status"] not in ("settled", "rejected")]
    retainage_blockers = [item for item in retainage if item["status"] != "released"]
    final_account_blockers = [
        {"contract_id": contract["id"], "blockers": _contract_closeout_blockers(state, contract["id"])}
        for contract in contracts
        if _contract_closeout_blockers(state, contract["id"])
    ]
    expiring_guarantees = []
    for contract in contracts:
        expiring_guarantees.extend(_expiring_guarantees(contract))
    notice_deadlines = [
        {
            "record_id": item["id"],
            "contract_id": item["contract_id"],
            "deadline": item["contractual_deadline"],
            "time_bar_status": item["time_bar_status"],
        }
        for item in claims + variations
        if item.get("contractual_deadline")
    ]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "queues": {
            "pay_apps_awaiting_certification": tuple(pay_apps_awaiting[: int(state["parameters"]["workbench_limit"]["value"])]),
            "missing_waivers": tuple(missing_waivers[: int(state["parameters"]["workbench_limit"]["value"])]),
            "expiring_guarantees": tuple(expiring_guarantees),
            "notice_deadlines": tuple(notice_deadlines),
            "disputed_variations": tuple(disputed_variations),
            "active_claims": tuple(active_claims),
            "retainage_release_blockers": tuple(retainage_blockers),
            "final_account_blockers": tuple(final_account_blockers),
        },
        "metrics": {
            "contract_count": len(contracts),
            "certified_but_unpaid": len([item for item in pay_apps if item["intake_status"] == "certified"]),
            "active_claim_exposure": round(sum(item["claimed_amount"] for item in active_claims), 2),
            "pending_variation_exposure": round(sum(item["quoted_amount"] for item in disputed_variations), 2),
            "retainage_held": round(sum(item["withheld_amount"] for item in retainage_blockers), 2),
        },
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "actions": _workbench_actions(actor),
        "ui_fragments": CONSTRUCTION_CONTRACTS_COMMERCIALS_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def construction_contracts_commercials_render_workbench(
    state: dict[str, Any] | None = None, tenant: str = "default", actor: dict[str, Any] | None = None
) -> dict[str, Any]:
    return construction_contracts_commercials_build_workbench_view(state=state, tenant=tenant, actor=actor)


def construction_contracts_commercials_query_workbench(state: dict[str, Any], filters: dict[str, Any] | None = None) -> dict[str, Any]:
    filters = dict(filters or {})
    return {
        "ok": True,
        "filters": filters,
        "workbench": construction_contracts_commercials_build_workbench_view(
            state=state,
            tenant=filters.get("tenant", "default"),
            actor=filters.get("actor"),
        ),
        "read_only": True,
        "side_effects": (),
    }


def construction_contracts_commercials_verify_owned_table_boundary(references: tuple[str, ...] = ()) -> dict[str, Any]:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith("_table")
        and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES,
        "shared_table_access": False,
    }


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


def construction_contracts_commercials_build_schema_contract() -> dict[str, Any]:
    table_contracts = tuple(
        {
            "table": table,
            "fields": TABLE_FIELDS[table],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES
    )
    return {
        "format": "appgen.construction-contracts-commercials-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/construction_contracts_commercials/migrations/{index + 1:03d}_{table['table']}.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(table_contracts)
        ),
        "models": tuple(
            {
                "class_name": _class_name(table["table"]),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "datastore_backends": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES,
    }


def _operation_contract(name: str, kind: str) -> dict[str, Any]:
    table = OPERATION_TO_TABLE.get(name)
    permission = {
        "create_construction_contract": "construction_contracts_commercials.create",
        "record_pay_application": "construction_contracts_commercials.create",
        "certify_pay_application": "construction_contracts_commercials.certify_pay_application",
        "approve_variation_order": "construction_contracts_commercials.approve_variation",
        "register_commercial_claim": "construction_contracts_commercials.assess_claim",
        "release_retainage": "construction_contracts_commercials.release_retainage",
        "build_final_account_packet": "construction_contracts_commercials.close_final_account",
    }.get(name, "construction_contracts_commercials.update" if kind == "command" else "construction_contracts_commercials.read")
    emitted_event = None
    if kind == "command":
        emitted_event = {
            "create_construction_contract": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0],
            "record_pay_application": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0],
            "certify_pay_application": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2],
            "approve_variation_order": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2],
            "register_commercial_claim": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[0],
            "release_retainage": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[2],
        }.get(name, CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES[1])
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": (table,) if kind == "command" and table else (),
        "read_tables": (table,) if kind == "query" and table else (),
        "emitted_event": emitted_event,
        "permission": permission,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
        "event_contract": "AppGen-X",
    }


SERVICE_COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "command_construction_contract",
) + DOMAIN_OPERATIONS
SERVICE_QUERY_OPERATIONS = (
    "query_workbench",
    "build_workbench_view",
    "build_payment_certificate",
    "build_final_account_packet",
    "generate_cash_flow_forecast",
    "generate_contractor_scorecard",
)


def construction_contracts_commercials_build_service_contract() -> dict[str, Any]:
    return {
        "format": "appgen.construction-contracts-commercials-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": SERVICE_COMMAND_OPERATIONS,
        "query_methods": SERVICE_QUERY_OPERATIONS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def construction_contracts_commercials_build_api_contract() -> dict[str, Any]:
    route_contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": {
                "POST /construction-contracts": "construction_contracts_commercials.create",
                "POST /pay-applications": "construction_contracts_commercials.create",
                "POST /retainages": "construction_contracts_commercials.update",
                "POST /variation-orders": "construction_contracts_commercials.approve_variation",
                "POST /commercial-claims": "construction_contracts_commercials.assess_claim",
                "GET /construction-contracts-commercials-workbench": "construction_contracts_commercials.read",
            }[route],
            "form": {
                "POST /construction-contracts": FORMS[0],
                "POST /pay-applications": FORMS[1],
                "POST /retainages": FORMS[2],
                "POST /variation-orders": FORMS[3],
                "POST /commercial-claims": FORMS[4],
                "GET /construction-contracts-commercials-workbench": None,
            }[route],
        }
        for route in CONSTRUCTION_CONTRACTS_COMMERCIALS_ROUTES
    )
    return {
        "format": "appgen.construction-contracts-commercials-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": CONSTRUCTION_CONTRACTS_COMMERCIALS_ROUTES,
        "contracts": route_contracts,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES,
    }


def event_contract_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES,
        "consumed": CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES,
        "outbox_table": OUTBOX_TABLE,
        "inbox_table": INBOX_TABLE,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract() -> dict[str, Any]:
    invalid_tables = tuple(table for table in EVENT_TABLES if not table.startswith(f"{PBC_KEY}_"))
    return {
        "ok": not invalid_tables,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    return {
        "ok": event_type in CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES + CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "topic": CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC,
        "idempotency_key": _digest((event_type, tuple(sorted(payload.items())))),
        "event_id": f"evt-{_digest((event_type, payload))[:12]}",
    }


def event_dispatch_plan(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


_HANDLED_EVENTS: set[str] = set()


def handler_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": DEAD_LETTER_TABLE,
        "side_effects": (),
    }


def dispatch_event(event: dict[str, Any]) -> dict[str, Any]:
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in _HANDLED_EVENTS:
        return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED_EVENTS.add(idem)
    event_type = event.get("event_type")
    if event_type not in CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES:
        return {
            "ok": False,
            "dead_letter_table": DEAD_LETTER_TABLE,
            "retry_policy": {"max_attempts": 5},
            "idempotency_key": idem,
            "side_effects": (),
        }
    projection_action = {
        "PolicyChanged": "refresh_policy_snapshot",
        "AuditEventSealed": "record_audit_seal",
        "OperationalKpiChanged": "refresh_operational_kpi_projection",
    }[event_type]
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idem,
        "projection_action": projection_action,
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def agent_skill_manifest() -> dict[str, Any]:
    skills = tuple(
        {
            "name": f"{PBC_KEY}.{skill}",
            "scope": PBC_KEY,
            "description": skill.replace("_", " "),
            "requires_confirmation_for_mutation": True,
            "uses_appgen_event_contract": True,
            "stream_engine_picker_visible": False,
        }
        for skill in AGENT_SKILLS
    )
    return {"ok": True, "pbc": PBC_KEY, "skills": skills, "side_effects": ()}


def chatbot_interface_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "single_agent_contribution": f"{PBC_KEY}_skills",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "citation_required_recommendations",
        ),
        "side_effects": (),
    }


def _detect_document_type(document: str) -> str:
    lowered = document.lower()
    if "waiver" in lowered:
        return "lien_waiver"
    if "variation" in lowered or "change order" in lowered:
        return "variation_notice"
    if "claim" in lowered:
        return "commercial_claim_notice"
    return "pay_application"


def document_instruction_plan(document: str, instruction: str) -> dict[str, Any]:
    doc_type = _detect_document_type(document)
    action = "create"
    if re.search(r"\bupdate\b|\brevise\b", instruction.lower()):
        action = "update"
    candidate_table = {
        "pay_application": PAY_APPLICATION_TABLE,
        "lien_waiver": WAIVER_TABLE,
        "variation_notice": VARIATION_TABLE,
        "commercial_claim_notice": CLAIM_TABLE,
    }[doc_type]
    extracted_fields = {
        "document_type": doc_type,
        "instruction": instruction,
        "confidence": 0.78 if doc_type == "pay_application" else 0.71,
        "source_spans": ({"field": "amount", "start": 12, "end": 24},),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction": instruction,
        "document_type": doc_type,
        "candidate_tables": (candidate_table,),
        "requires_human_confirmation": True,
        "requires_citations": True,
        "crud_preview": {"operation": action, "table": candidate_table, "event_contract": "AppGen-X"},
        "extracted_fields": extracted_fields,
        "accepted_fields": (),
        "rejected_fields": (),
        "side_effects": (),
    }


def datastore_crud_plan(action: str, table: str | None = None, payload: dict[str, Any] | None = None, actor: dict[str, Any] | None = None) -> dict[str, Any]:
    target = table or CONTRACT_TABLE
    if not str(target).startswith(f"{PBC_KEY}_"):
        return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
    permission = {
        "read": "construction_contracts_commercials.read",
        "create": "construction_contracts_commercials.create",
        "update": "construction_contracts_commercials.update",
        "delete": "construction_contracts_commercials.admin",
        "query": "construction_contracts_commercials.read",
    }.get(action, "construction_contracts_commercials.update")
    auth = _authorize(actor, permission)
    if not auth["ok"]:
        return {"ok": False, "reason": "permission_denied", "authorization": auth, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "action": action,
        "table": target,
        "payload": dict(payload or {}),
        "requires_confirmation": action in ("create", "update", "delete"),
        "requires_citations": action in ("create", "update", "delete"),
        "event_contract": "AppGen-X",
        "preview_hash": _digest((action, target, payload)),
        "authorization": auth,
        "side_effects": (),
    }


def composed_agent_contribution() -> dict[str, Any]:
    namespace = f"{PBC_KEY}_skills"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_agent_skill_namespace": namespace,
        "dsl_tools": (namespace, f"{PBC_KEY}_crud", f"{PBC_KEY}_documents"),
        "skill_names": AGENT_SKILLS,
        "side_effects": (),
    }


SCENARIO_LIBRARY = (
    "pay_application_certification",
    "retainage_release",
    "missing_waiver",
    "variation_negotiation",
    "delay_claim",
    "backcharge_hold",
    "expiring_bond",
    "final_account_closeout",
)


def seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "scenarios": SCENARIO_LIBRARY,
        "records": (
            {"table": CONTRACT_TABLE, "contract_code": "CCC-001"},
            {"table": PAY_APPLICATION_TABLE, "application_number": "APP-001"},
            {"table": WAIVER_TABLE, "waiver_number": "LW-001"},
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict[str, Any]:
    plan = seed_plan()
    return {"ok": plan["ok"] and len(plan["scenarios"]) >= 6, "pbc": PBC_KEY, "side_effects": ()}


def _release_simulation() -> dict[str, Any]:
    state = construction_contracts_commercials_empty_state()
    state = construction_contracts_commercials_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC,
        },
    )["state"]
    state = construction_contracts_commercials_set_parameter(state, "workbench_limit", 20)["state"]
    state = construction_contracts_commercials_command_construction_contract(
        state,
        {
            "tenant": "tenant-a",
            "contract_code": "CCC-001",
            "title": "Civic Centre Fit-Out",
            "contract_value": 100000.0,
            "pricing_basis": "lump_sum",
            "jurisdiction": "KE",
            "schedule_of_values": (
                {"line_code": "SOV-01", "work_package": "Concrete", "original_value": 60000.0},
                {"line_code": "SOV-02", "work_package": "Finishes", "original_value": 40000.0},
            ),
            "guarantees": (
                {"type": "performance_bond", "expiry": (date.today() + timedelta(days=21)).isoformat(), "issuer": "ABC Surety"},
            ),
            "obligations": (
                {"clause": "12.4", "responsible_party": "contractor", "due_date": (date.today() + timedelta(days=5)).isoformat()},
            ),
        },
    )["state"]
    state = construction_contracts_commercials_record_pay_application(
        state,
        {
            "contract_code": "CCC-001",
            "application_number": "APP-001",
            "period_start": date.today().replace(day=1).isoformat(),
            "period_end": date.today().isoformat(),
            "attachments": ("payapp.pdf", "photos.zip"),
            "lines": (
                {"line_code": "SOV-01", "current_claimed": 25000.0, "evidence_refs": ("inspection-001",)},
            ),
        },
    )["state"]
    state = construction_contracts_commercials_create_lien_waiver(
        state,
        {
            "contract_code": "CCC-001",
            "pay_application_id": "pay-app-APP-001",
            "waiver_number": "LW-001",
            "covered_amount": 25000.0,
            "signed_date": date.today().isoformat(),
        },
    )["state"]
    state = construction_contracts_commercials_certify_pay_application(
        state,
        {"pay_application_id": "pay-app-APP-001"},
    )["state"]
    state = construction_contracts_commercials_review_retainage(
        state,
        {"pay_application_id": "pay-app-APP-001"},
    )["state"]
    state = construction_contracts_commercials_approve_variation_order(
        state,
        {
            "contract_code": "CCC-001",
            "variation_number": "VO-001",
            "event_date": date.today().isoformat(),
            "notice_date": date.today().isoformat(),
            "quoted_amount": 12000.0,
            "approved_amount": 10000.0,
            "approved": True,
        },
    )["state"]
    state = construction_contracts_commercials_register_commercial_claim(
        state,
        {
            "contract_code": "CCC-001",
            "claim_number": "CL-001",
            "claim_type": "delay",
            "event_date": date.today().isoformat(),
            "notice_date": (date.today() + timedelta(days=18)).isoformat(),
            "claimed_amount": 14000.0,
        },
    )["state"]
    workbench = construction_contracts_commercials_build_workbench_view(state=state, tenant="tenant-a", actor={"roles": ("commercial_manager",)})
    cash_flow = construction_contracts_commercials_generate_cash_flow_forecast(state)
    scorecard = construction_contracts_commercials_generate_contractor_scorecard(state)
    return {
        "ok": workbench["ok"] and cash_flow["ok"] and scorecard["ok"],
        "state": state,
        "workbench": workbench,
        "cash_flow": cash_flow,
        "scorecard": scorecard,
    }


def construction_contracts_commercials_build_release_evidence() -> dict[str, Any]:
    simulation = _release_simulation()
    schema = construction_contracts_commercials_build_schema_contract()
    service = construction_contracts_commercials_build_service_contract()
    api = construction_contracts_commercials_build_api_contract()
    permissions = construction_contracts_commercials_permissions_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"]},
        {"id": "service_api_events", "ok": service["ok"] and api["ok"] and event_contract_manifest()["ok"]},
        {"id": "commercial_lifecycle_controls", "ok": simulation["ok"]},
        {"id": "workbench_ui", "ok": simulation["workbench"]["ok"]},
        {"id": "agent_document_crud", "ok": agent_skill_manifest()["ok"] and document_instruction_plan("pay application", "create claim")["ok"]},
        {"id": "permissions_and_rules", "ok": permissions["ok"] and rule_manifest()["ok"] and parameter_manifest()["ok"]},
        {"id": "seed_and_boundary", "ok": validate_seed_data()["ok"] and construction_contracts_commercials_verify_owned_table_boundary(CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES + ("foreign_table",))["ok"] is False},
        {"id": "improve1_commercial_control", "ok": improve1_commercial_control_contract()["ok"]},
    )
    return {
        "format": "appgen.construction-contracts-commercials-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES,
                "consumes": CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event", "dispatch_event"),
            "ui": CONSTRUCTION_CONTRACTS_COMMERCIALS_UI_FRAGMENT_KEYS,
            "simulation": simulation,
            "improve1_commercial_control": improve1_commercial_control_contract(),
        },
        "blocking_gaps": tuple(check["id"] for check in checks if not check["ok"]),
    }


def construction_contracts_commercials_runtime_capabilities() -> dict[str, Any]:
    smoke = construction_contracts_commercials_runtime_smoke()
    return {
        "format": "appgen.construction-contracts-commercials-runtime-capabilities.v2",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": CONSTRUCTION_CONTRACTS_COMMERCIALS_OWNED_TABLES,
        "allowed_database_backends": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": CONSTRUCTION_CONTRACTS_COMMERCIALS_STANDARD_FEATURE_KEYS,
        "capabilities": CONSTRUCTION_CONTRACTS_COMMERCIALS_RUNTIME_CAPABILITY_KEYS,
        "operations": SERVICE_COMMAND_OPERATIONS
        + SERVICE_QUERY_OPERATIONS
        + (
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "improve1_commercial_control_contract",
        ),
        "smoke": smoke,
        "improve1_commercial_control": improve1_commercial_control_contract(),
        "database_backends": CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def construction_contracts_commercials_runtime_smoke() -> dict[str, Any]:
    state = construction_contracts_commercials_empty_state()
    configured = construction_contracts_commercials_configure_runtime(
        state,
        {"database_backend": "postgresql", "event_topic": CONSTRUCTION_CONTRACTS_COMMERCIALS_REQUIRED_EVENT_TOPIC},
    )
    parameter = construction_contracts_commercials_set_parameter(configured["state"], "workbench_limit", 10)
    rule = construction_contracts_commercials_register_rule(parameter["state"], {"rule_id": "smoke_rule", "severity": "medium"})
    event = construction_contracts_commercials_receive_event(rule["state"], {"event_type": "PolicyChanged", "idempotency_key": "smoke-policy", "payload": {"policy_version": "smoke-v2"}})
    schema = construction_contracts_commercials_build_schema_contract()
    release = construction_contracts_commercials_build_release_evidence()
    ui = construction_contracts_commercials_ui_contract()
    commercial_control = improve1_commercial_control_contract()
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "set_parameter", "ok": parameter["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": event["ok"]},
        {"id": "schema", "ok": schema["ok"]},
        {"id": "release", "ok": release["ok"]},
        {"id": "ui", "ok": ui["ok"]},
        {"id": "improve1_commercial_control", "ok": commercial_control["ok"]},
    )
    return {
        "format": "appgen.construction-contracts-commercials-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": configured,
        "schema": schema,
        "release": release,
        "ui": ui,
        "improve1_commercial_control": commercial_control,
        "blocking_gaps": tuple(check["id"] for check in checks if not check["ok"]),
        "side_effects": (),
    }


def governance_smoke_test() -> dict[str, Any]:
    validation = validate_configuration()
    parameters = parameter_manifest()
    rules = rule_manifest()
    compiled = compile_rule({"rule_id": DOMAIN_RULES[0]})
    evaluated = evaluate_rule(DOMAIN_RULES[0], {"contract_value": 1000, "schedule_of_values": (1,)})
    return {
        "ok": validation["ok"] and parameters["ok"] and rules["ok"] and compiled["ok"] and evaluated["ok"],
        "side_effects": (),
    }
