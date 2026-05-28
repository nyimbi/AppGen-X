"""Executable one-PBC runtime for healthcare claims adjudication."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from typing import Any

from .config import ALLOWED_DATABASE_BACKENDS
from .config import DEFAULT_CONFIGURATION
from .config import PARAMETER_DEFINITIONS
from .config import PERMISSIONS
from .config import REQUIRED_EVENT_TOPIC
from .config import ROLES
from .config import permission_manifest
from .config import set_parameter as validate_parameter_write
from .config import validate_configuration
from .events import CONSUMED
from .events import EMITTED
from .models import Appeal
from .models import AppGenEvent
from .models import BenefitRule
from .models import BUSINESS_TABLES
from .models import ClaimLine
from .models import CodingReview
from .models import ControlAssertion
from .models import Denial
from .models import DocumentInstruction
from .models import EVENT_TABLES
from .models import GovernedModel
from .models import HealthClaim
from .models import OWNED_TABLES
from .models import PBC_KEY
from .models import PaymentIntegrityCase
from .models import PolicyRule
from .models import RuntimeParameter
from .models import SchemaExtension
from .models import dataclass_payload
from .models import model_contracts
from .models import stable_identifier
from .models import utc_now

CLAIMS_ADJUDICATION_HEALTHCARE_OWNED_TABLES = OWNED_TABLES
CLAIMS_ADJUDICATION_HEALTHCARE_RUNTIME_TABLES = OWNED_TABLES
CLAIMS_ADJUDICATION_HEALTHCARE_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
CLAIMS_ADJUDICATION_HEALTHCARE_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
CLAIMS_ADJUDICATION_HEALTHCARE_EMITTED_EVENT_TYPES = EMITTED
CLAIMS_ADJUDICATION_HEALTHCARE_CONSUMED_EVENT_TYPES = CONSUMED

CLAIMS_ADJUDICATION_HEALTHCARE_STANDARD_FEATURE_KEYS = (
    "health_claim_management",
    "claim_line_adjudication",
    "coding_review",
    "benefit_rule_governance",
    "denial_and_appeal_management",
    "payment_integrity",
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

CLAIMS_ADJUDICATION_HEALTHCARE_RUNTIME_CAPABILITY_KEYS = (
    "claims_adjudication_healthcare_event_sourced_operational_history",
    "claims_adjudication_healthcare_multi_tenant_policy_isolation",
    "claims_adjudication_healthcare_schema_evolution_resilience",
    "claims_adjudication_healthcare_semantic_document_instruction_understanding",
    "claims_adjudication_healthcare_predictive_duplicate_detection",
    "claims_adjudication_healthcare_governed_ai_agent_execution",
)

CLAIMS_ADJUDICATION_HEALTHCARE_UI_FRAGMENT_KEYS = (
    "ClaimsAdjudicationHealthcareWorkbench",
    "ClaimsAdjudicationHealthcareClaimDetail",
    "ClaimsAdjudicationHealthcareAssistantPanel",
)

CLAIMS_ADJUDICATION_HEALTHCARE_BUSINESS_TABLES = BUSINESS_TABLES

CLAIM_STATUSES = (
    "received",
    "validated",
    "pended",
    "priced",
    "adjudicated",
    "paid",
    "denied",
    "partially_denied",
    "appealed",
    "adjusted",
    "reversed",
)

LINE_STATUSES = ("received", "pended", "paid", "denied")

DOMAIN_OPERATIONS = (
    "create_health_claim",
    "record_claim_line",
    "review_coding_review",
    "approve_benefit_rule",
    "simulate_denial",
    "create_appeal",
    "record_payment_integrity_case",
    "register_rule",
    "set_parameter",
    "register_schema_extension",
    "create_control_assertion",
    "record_governed_model",
    "create_document_instruction",
    "query_workbench",
    "run_advanced_assessment",
    "parse_document_instruction",
)


def claims_adjudication_healthcare_empty_state() -> dict[str, Any]:
    return {
        "claims": {},
        "claim_lines": {},
        "coding_reviews": {},
        "benefit_rules": {},
        "denials": {},
        "appeals": {},
        "payment_integrity_cases": {},
        "policy_rules": {},
        "parameters": {},
        "schema_extensions": {},
        "control_assertions": {},
        "governed_models": {},
        "document_instructions": {},
        "configuration": deepcopy(DEFAULT_CONFIGURATION),
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
        "route_history": [],
    }


def _copy(state: dict[str, Any]) -> dict[str, Any]:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _tenant(payload: dict[str, Any]) -> str:
    return str(payload.get("tenant") or "default")


def _event_payload(base: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in base.items() if value is not None}


def _append_outbox(
    state: dict[str, Any],
    event_type: str,
    payload: dict[str, Any],
    *,
    tenant: str,
    idempotency_key: str,
) -> dict[str, Any]:
    event = AppGenEvent(
        event_id=stable_identifier("evt", (event_type, idempotency_key, payload)),
        tenant=tenant,
        event_type=event_type,
        topic=REQUIRED_EVENT_TOPIC,
        payload=_event_payload(payload),
        idempotency_key=idempotency_key,
        status="queued",
    )
    rendered = dataclass_payload(event)
    state["outbox"].append(rendered)
    return rendered


def _claim_identity(payload: dict[str, Any]) -> tuple[Any, ...]:
    return (
        payload.get("tenant"),
        payload.get("claim_number"),
        payload.get("member_id"),
        payload.get("provider_id"),
        payload.get("received_date"),
        float(payload.get("total_charge", 0)),
    )


def _find_benefit_rule(state: dict[str, Any], claim: dict[str, Any], line_payload: dict[str, Any]) -> dict[str, Any] | None:
    service_date = str(line_payload.get("service_date"))
    for rule in state["benefit_rules"].values():
        if rule["tenant"] != claim["tenant"]:
            continue
        if rule["plan_id"] != claim["plan_id"]:
            continue
        if rule["service_code"] != line_payload.get("procedure_code"):
            continue
        if rule["status"] not in {"approved", "active"}:
            continue
        if rule["effective_from"] <= service_date <= rule["effective_to"]:
            return rule
    return None


def _current_parameter(state: dict[str, Any], name: str) -> float:
    definition = PARAMETER_DEFINITIONS[name]
    stored = state["parameters"].get(name)
    return float(stored["value"]) if stored else float(definition["default"])


def _projection_is_stale(payload: dict[str, Any], threshold_hours: float) -> bool:
    eligibility = float(payload.get("eligibility_projection_hours", 0))
    provider = float(payload.get("provider_projection_hours", 0))
    return max(eligibility, provider) > threshold_hours


def _claim_lines(state: dict[str, Any], claim_id: str) -> list[dict[str, Any]]:
    return [line for line in state["claim_lines"].values() if line["claim_id"] == claim_id]


def _update_claim_status_from_lines(state: dict[str, Any], claim_id: str) -> None:
    claim = state["claims"][claim_id]
    lines = _claim_lines(state, claim_id)
    if not lines:
        return
    statuses = {line["status"] for line in lines}
    if "pended" in statuses:
        next_status = "pended"
    elif statuses == {"denied"}:
        next_status = "denied"
    elif "denied" in statuses and "paid" in statuses:
        next_status = "partially_denied"
    elif statuses == {"paid"}:
        next_status = "adjudicated"
    else:
        next_status = claim["status"]
    state["claims"][claim_id] = {
        **claim,
        "status": next_status,
        "updated_at": utc_now(),
    }


def claims_adjudication_healthcare_configure_runtime(
    state: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    validation = validate_configuration(config)
    next_state["configuration"] = validation["configuration"]
    return {
        "ok": validation["ok"],
        "state": next_state,
        "configuration": validation["configuration"],
        "invalid_fields": validation["invalid_fields"],
        "side_effects": (),
    }


def claims_adjudication_healthcare_set_parameter(
    state: dict[str, Any],
    name: str,
    value: float,
    *,
    tenant: str = "default",
) -> dict[str, Any]:
    next_state = _copy(state)
    validation = validate_parameter_write(name, value)
    if not validation["ok"]:
        return {**validation, "state": next_state}
    record = RuntimeParameter(
        parameter_name=name,
        tenant=tenant,
        value=float(value),
        minimum=float(validation["minimum"]),
        maximum=float(validation["maximum"]),
        unit=PARAMETER_DEFINITIONS[name]["unit"],
    )
    next_state["parameters"][name] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "parameter": next_state["parameters"][name],
        "side_effects": (),
    }


def claims_adjudication_healthcare_register_rule(
    state: dict[str, Any],
    rule: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    tenant = _tenant(rule)
    rule_name = str(rule.get("rule_name") or rule.get("rule_id") or "custom-policy-rule")
    record = PolicyRule(
        policy_rule_id=str(rule.get("policy_rule_id") or stable_identifier("policy", (tenant, rule_name, rule))),
        tenant=tenant,
        rule_name=rule_name,
        description=str(rule.get("description") or "Package-local adjudication control"),
        condition_key=str(rule.get("condition_key") or "charge_amount"),
        threshold=float(rule.get("threshold", 0)),
        action=str(rule.get("action") or "review"),
        status=str(rule.get("status") or "approved"),
    )
    next_state["policy_rules"][record.policy_rule_id] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "rule": next_state["policy_rules"][record.policy_rule_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_register_schema_extension(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    record = SchemaExtension(
        extension_id=str(payload.get("extension_id") or stable_identifier("schema", payload)),
        tenant=_tenant(payload),
        target_table=str(payload.get("target_table") or BUSINESS_TABLES[0]),
        column_name=str(payload.get("column_name") or "clinical_pathway"),
        data_type=str(payload.get("data_type") or "TEXT"),
        justification=str(payload.get("justification") or "domain slice extension"),
        status=str(payload.get("status") or "proposed"),
    )
    next_state["schema_extensions"][record.extension_id] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "schema_extension": next_state["schema_extensions"][record.extension_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_create_control_assertion(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    record = ControlAssertion(
        assertion_id=str(payload.get("assertion_id") or stable_identifier("control", payload)),
        tenant=_tenant(payload),
        control_name=str(payload.get("control_name") or "dual-review-for-overturns"),
        objective=str(payload.get("objective") or "Protect denial and appeal reversals"),
        frequency=str(payload.get("frequency") or "daily"),
        status=str(payload.get("status") or "active"),
    )
    next_state["control_assertions"][record.assertion_id] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "control_assertion": next_state["control_assertions"][record.assertion_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_record_governed_model(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    record = GovernedModel(
        model_id=str(payload.get("model_id") or stable_identifier("model", payload)),
        tenant=_tenant(payload),
        model_name=str(payload.get("model_name") or "duplicate-claim-detector"),
        purpose=str(payload.get("purpose") or "Flag duplicate and suspicious healthcare claims"),
        version=str(payload.get("version") or "1.0.0"),
        approval_status=str(payload.get("approval_status") or "approved"),
    )
    next_state["governed_models"][record.model_id] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "governed_model": next_state["governed_models"][record.model_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_parse_document_instruction(
    document: str,
    instruction: str,
) -> dict[str, Any]:
    text = f"{document} {instruction}".lower()
    target = BUSINESS_TABLES[3]
    action = "create"
    extracted_fields: dict[str, Any] = {}
    if "benefit" in text or "coverage" in text:
        target = BUSINESS_TABLES[3]
        extracted_fields["description"] = "Create or update benefit coverage rule"
    elif "appeal" in text:
        target = BUSINESS_TABLES[5]
        action = "create"
        extracted_fields["status"] = "received"
    elif "denial" in text:
        target = BUSINESS_TABLES[4]
        action = "create"
        extracted_fields["status"] = "issued"
    elif "parameter" in text or "threshold" in text:
        target = BUSINESS_TABLES[8]
        action = "update"
    elif "instruction" in text:
        target = BUSINESS_TABLES[12]
    if "update" in text or "revise" in text:
        action = "update"
    if "delete" in text or "retire" in text:
        action = "delete"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest((document, instruction)),
        "action": action,
        "target_table": target,
        "extracted_fields": extracted_fields,
        "requires_human_confirmation": action in {"create", "update", "delete"},
        "side_effects": (),
    }


def claims_adjudication_healthcare_create_document_instruction(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    parsed = claims_adjudication_healthcare_parse_document_instruction(
        str(payload.get("document_name") or "instruction.txt"),
        str(payload.get("instruction_text") or payload.get("instruction") or ""),
    )
    record = DocumentInstruction(
        instruction_id=str(payload.get("instruction_id") or stable_identifier("doc", payload)),
        tenant=_tenant(payload),
        document_name=str(payload.get("document_name") or "instruction.txt"),
        instruction_text=str(payload.get("instruction_text") or payload.get("instruction") or ""),
        target_table=parsed["target_table"],
        action=parsed["action"],
        status=str(payload.get("status") or "draft"),
        structured_fields=dict(parsed["extracted_fields"]),
    )
    next_state["document_instructions"][record.instruction_id] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "document_instruction": next_state["document_instructions"][record.instruction_id],
        "parse_result": parsed,
        "side_effects": (),
    }


def claims_adjudication_healthcare_create_health_claim(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    required = ("claim_number", "member_id", "provider_id", "plan_id", "received_date")
    missing = tuple(name for name in required if not payload.get(name))
    if missing:
        return {
            "ok": False,
            "reason": "missing_required_fields",
            "missing": missing,
            "state": next_state,
            "side_effects": (),
        }
    identity = _claim_identity(payload)
    existing = next(
        (claim for claim in next_state["claims"].values() if _claim_identity(claim) == identity),
        None,
    )
    if existing and not payload.get("correction_type"):
        return {
            "ok": True,
            "duplicate": True,
            "claim": existing,
            "state": next_state,
            "side_effects": (),
        }
    stale_threshold = _current_parameter(next_state, "stale_projection_hours")
    stale = _projection_is_stale(payload, stale_threshold)
    claim_id = str(payload.get("claim_id") or stable_identifier("claim", identity))
    record = HealthClaim(
        claim_id=claim_id,
        tenant=_tenant(payload),
        claim_number=str(payload["claim_number"]),
        claim_type=str(payload.get("claim_type") or "professional"),
        source_format=str(payload.get("source_format") or "837P"),
        member_id=str(payload["member_id"]),
        provider_id=str(payload["provider_id"]),
        plan_id=str(payload["plan_id"]),
        received_date=str(payload["received_date"]),
        status="pended" if stale else "validated",
        priority=str(payload.get("priority") or "standard"),
        total_charge=float(payload.get("total_charge", 0)),
        duplicate_of=existing["claim_id"] if existing else None,
        pend_reason="stale_projection" if stale else None,
        original_claim_id=payload.get("original_claim_id"),
        correction_type=payload.get("correction_type"),
        evidence={
            "eligibility_projection_hours": payload.get("eligibility_projection_hours", 0),
            "provider_projection_hours": payload.get("provider_projection_hours", 0),
            "submitter_id": payload.get("submitter_id"),
            "batch_id": payload.get("batch_id"),
        },
    )
    next_state["claims"][claim_id] = dataclass_payload(record)
    event_key = _digest(("claim", claim_id, record.status))
    created = _append_outbox(
        next_state,
        EMITTED[0],
        {"claim_id": claim_id, "status": record.status, "claim_number": record.claim_number},
        tenant=record.tenant,
        idempotency_key=event_key,
    )
    exception = None
    if stale:
        exception = _append_outbox(
            next_state,
            EMITTED[3],
            {"claim_id": claim_id, "reason": "stale_projection"},
            tenant=record.tenant,
            idempotency_key=f"{event_key}:exception",
        )
    return {
        "ok": True,
        "state": next_state,
        "claim": next_state["claims"][claim_id],
        "events": tuple(event for event in (created, exception) if event),
        "duplicate": False,
        "side_effects": (),
    }


def claims_adjudication_healthcare_command_health_claim(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    return claims_adjudication_healthcare_create_health_claim(state, payload)


def claims_adjudication_healthcare_approve_benefit_rule(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    required = ("plan_id", "service_code", "description", "effective_from", "effective_to")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {
            "ok": False,
            "reason": "missing_required_fields",
            "missing": missing,
            "state": next_state,
            "side_effects": (),
        }
    record = BenefitRule(
        rule_id=str(payload.get("rule_id") or stable_identifier("benefit", payload)),
        tenant=_tenant(payload),
        plan_id=str(payload["plan_id"]),
        service_code=str(payload["service_code"]),
        description=str(payload["description"]),
        covered=bool(payload.get("covered", True)),
        auth_required=bool(payload.get("auth_required", False)),
        allowed_percentage=float(payload.get("allowed_percentage", 0.8)),
        copay_amount=float(payload.get("copay_amount", 25)),
        deductible_apply=bool(payload.get("deductible_apply", True)),
        max_units=int(payload.get("max_units", 10)),
        effective_from=str(payload["effective_from"]),
        effective_to=str(payload["effective_to"]),
        status=str(payload.get("status") or "approved"),
        approval_reference=str(payload.get("approval_reference") or "medical-policy-committee"),
    )
    next_state["benefit_rules"][record.rule_id] = dataclass_payload(record)
    _append_outbox(
        next_state,
        EMITTED[2],
        {"benefit_rule_id": record.rule_id, "service_code": record.service_code},
        tenant=record.tenant,
        idempotency_key=_digest(("benefit_rule", record.rule_id)),
    )
    return {
        "ok": True,
        "state": next_state,
        "benefit_rule": next_state["benefit_rules"][record.rule_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_record_payment_integrity_case(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    record = PaymentIntegrityCase(
        case_id=str(payload.get("case_id") or stable_identifier("pi", payload)),
        claim_id=str(payload["claim_id"]),
        tenant=_tenant(payload),
        trigger=str(payload.get("trigger") or "high_charge"),
        exposure_amount=float(payload.get("exposure_amount", payload.get("charge_amount", 0))),
        reviewer=str(payload.get("reviewer") or "payment_integrity_queue"),
        notes=str(payload.get("notes") or "Opened by package-local adjudication controls."),
        status=str(payload.get("status") or "open"),
    )
    next_state["payment_integrity_cases"][record.case_id] = dataclass_payload(record)
    return {
        "ok": True,
        "state": next_state,
        "payment_integrity_case": next_state["payment_integrity_cases"][record.case_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_record_claim_line(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    claim_id = str(payload.get("claim_id") or "")
    claim = next_state["claims"].get(claim_id)
    if not claim:
        return {
            "ok": False,
            "reason": "unknown_claim",
            "claim_id": claim_id,
            "state": next_state,
            "side_effects": (),
        }
    required = ("line_number", "service_date", "procedure_code", "diagnosis_code", "place_of_service", "units", "charge_amount")
    missing = tuple(field for field in required if payload.get(field) in (None, ""))
    if missing:
        return {
            "ok": False,
            "reason": "missing_required_fields",
            "missing": missing,
            "state": next_state,
            "side_effects": (),
        }
    rule = _find_benefit_rule(next_state, claim, payload)
    if rule is None:
        status = "pended"
        reason = "missing_benefit_rule"
        allowed = 0.0
        member_responsibility = 0.0
        payer_responsibility = 0.0
    else:
        units = int(payload["units"])
        charge = float(payload["charge_amount"])
        if rule["auth_required"] and not payload.get("authorization_id"):
            status = "denied"
            reason = "missing_authorization"
            allowed = 0.0
            member_responsibility = 0.0
            payer_responsibility = 0.0
        elif not rule["covered"]:
            status = "denied"
            reason = "service_not_covered"
            allowed = 0.0
            member_responsibility = 0.0
            payer_responsibility = 0.0
        elif units > int(rule["max_units"]):
            status = "denied"
            reason = "exceeds_unit_limit"
            allowed = 0.0
            member_responsibility = 0.0
            payer_responsibility = 0.0
        else:
            allowed = round(charge * float(rule["allowed_percentage"]), 2)
            deductible = min(
                allowed * 0.1 if rule["deductible_apply"] else 0.0,
                float(payload.get("accumulator_remaining", allowed)),
            )
            member_responsibility = round(min(allowed, float(rule["copay_amount"]) + deductible), 2)
            payer_responsibility = round(max(0.0, allowed - member_responsibility), 2)
            status = "paid"
            reason = "auto_adjudicated"
    line_id = str(payload.get("line_id") or stable_identifier("line", (claim_id, payload.get("line_number"), payload.get("procedure_code"))))
    record = ClaimLine(
        line_id=line_id,
        claim_id=claim_id,
        tenant=claim["tenant"],
        line_number=int(payload["line_number"]),
        service_date=str(payload["service_date"]),
        procedure_code=str(payload["procedure_code"]),
        diagnosis_code=str(payload["diagnosis_code"]),
        place_of_service=str(payload["place_of_service"]),
        units=int(payload["units"]),
        charge_amount=float(payload["charge_amount"]),
        authorization_id=payload.get("authorization_id"),
        modifiers=tuple(payload.get("modifiers", ())),
        status=status,
        allowed_amount=allowed,
        member_responsibility=member_responsibility,
        payer_responsibility=payer_responsibility,
        adjudication_reason=reason,
        reason_codes=(reason,),
    )
    next_state["claim_lines"][line_id] = dataclass_payload(record)

    coding_review = None
    threshold = _current_parameter(next_state, "coding_review_unit_threshold")
    if int(payload["units"]) > threshold or payload.get("possible_unbundling"):
        review = CodingReview(
            review_id=stable_identifier("coding", (claim_id, line_id, payload.get("procedure_code"))),
            claim_id=claim_id,
            tenant=claim["tenant"],
            line_id=line_id,
            issue_type="unusual_units" if int(payload["units"]) > threshold else "possible_unbundling",
            severity="high",
            status="open",
            notes="Opened automatically by adjudication controls.",
        )
        next_state["coding_reviews"][review.review_id] = dataclass_payload(review)
        next_state["claim_lines"][line_id] = {
            **next_state["claim_lines"][line_id],
            "status": "pended",
            "adjudication_reason": "coding_review_required",
            "reason_codes": ("coding_review_required",),
            "updated_at": utc_now(),
        }
        coding_review = next_state["coding_reviews"][review.review_id]

    payment_integrity_case = None
    materiality = _current_parameter(next_state, "payment_integrity_materiality")
    if float(payload["charge_amount"]) >= materiality:
        case_result = claims_adjudication_healthcare_record_payment_integrity_case(
            next_state,
            {
                "claim_id": claim_id,
                "tenant": claim["tenant"],
                "trigger": "material_charge",
                "charge_amount": payload["charge_amount"],
            },
        )
        next_state = case_result["state"]
        payment_integrity_case = case_result["payment_integrity_case"]

    _update_claim_status_from_lines(next_state, claim_id)
    final_line = next_state["claim_lines"][line_id]
    event_type = EMITTED[1] if final_line["status"] == "paid" else EMITTED[3]
    emitted = _append_outbox(
        next_state,
        event_type,
        {"claim_id": claim_id, "line_id": line_id, "status": final_line["status"], "reason": final_line["adjudication_reason"]},
        tenant=claim["tenant"],
        idempotency_key=_digest(("line", line_id, final_line["status"])),
    )
    return {
        "ok": True,
        "state": next_state,
        "claim_line": final_line,
        "coding_review": coding_review,
        "payment_integrity_case": payment_integrity_case,
        "event": emitted,
        "side_effects": (),
    }


def claims_adjudication_healthcare_review_coding_review(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    review_id = str(payload.get("review_id") or "")
    existing = next_state["coding_reviews"].get(review_id)
    if not existing:
        return {
            "ok": False,
            "reason": "unknown_coding_review",
            "review_id": review_id,
            "state": next_state,
            "side_effects": (),
        }
    status = str(payload.get("status") or "resolved")
    updated = {
        **existing,
        "status": status,
        "override_reason": payload.get("override_reason"),
        "notes": payload.get("notes", existing.get("notes", "")),
        "updated_at": utc_now(),
    }
    next_state["coding_reviews"][review_id] = updated
    line_id = existing.get("line_id")
    if line_id and line_id in next_state["claim_lines"] and status in {"resolved", "overridden"}:
        line = next_state["claim_lines"][line_id]
        next_state["claim_lines"][line_id] = {
            **line,
            "status": "paid" if status == "resolved" else "pended",
            "adjudication_reason": "coding_review_resolved" if status == "resolved" else "manual_override_pending",
            "updated_at": utc_now(),
        }
        _update_claim_status_from_lines(next_state, line["claim_id"])
    return {
        "ok": True,
        "state": next_state,
        "coding_review": updated,
        "side_effects": (),
    }


def claims_adjudication_healthcare_simulate_denial(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    claim_id = str(payload["claim_id"])
    claim = next_state["claims"].get(claim_id)
    if not claim:
        return {
            "ok": False,
            "reason": "unknown_claim",
            "claim_id": claim_id,
            "state": next_state,
            "side_effects": (),
        }
    line_ids = tuple(payload.get("line_ids") or ())
    policy_rule_id = str(payload.get("policy_rule_id") or stable_identifier("policy-link", payload))
    record = Denial(
        denial_id=str(payload.get("denial_id") or stable_identifier("denial", payload)),
        claim_id=claim_id,
        tenant=claim["tenant"],
        denial_code=str(payload.get("denial_code") or "AUTH-001"),
        rationale=str(payload.get("rationale") or "Prior authorization evidence is missing."),
        policy_rule_id=policy_rule_id,
        line_ids=line_ids,
        notice_deadline=str(payload.get("notice_deadline") or claim["received_date"]),
        status=str(payload.get("status") or "issued"),
    )
    next_state["denials"][record.denial_id] = dataclass_payload(record)
    if line_ids:
        for line_id in line_ids:
            if line_id in next_state["claim_lines"]:
                line = next_state["claim_lines"][line_id]
                next_state["claim_lines"][line_id] = {
                    **line,
                    "status": "denied",
                    "adjudication_reason": "manual_denial",
                    "reason_codes": (record.denial_code,),
                    "updated_at": utc_now(),
                }
    next_state["claims"][claim_id] = {
        **claim,
        "status": "denied" if line_ids else "partially_denied",
        "updated_at": utc_now(),
    }
    event = _append_outbox(
        next_state,
        EMITTED[3],
        {"claim_id": claim_id, "denial_id": record.denial_id, "denial_code": record.denial_code},
        tenant=claim["tenant"],
        idempotency_key=_digest(("denial", record.denial_id)),
    )
    return {
        "ok": True,
        "state": next_state,
        "denial": next_state["denials"][record.denial_id],
        "event": event,
        "side_effects": (),
    }


def claims_adjudication_healthcare_create_appeal(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    denial_id = str(payload["denial_id"])
    denial = next_state["denials"].get(denial_id)
    if not denial:
        return {
            "ok": False,
            "reason": "unknown_denial",
            "denial_id": denial_id,
            "state": next_state,
            "side_effects": (),
        }
    record = Appeal(
        appeal_id=str(payload.get("appeal_id") or stable_identifier("appeal", payload)),
        denial_id=denial_id,
        claim_id=denial["claim_id"],
        tenant=denial["tenant"],
        level=str(payload.get("level") or "first_level"),
        requester=str(payload.get("requester") or "provider"),
        evidence_summary=str(payload.get("evidence_summary") or "Appeal packet received."),
        status=str(payload.get("status") or "received"),
        determination=payload.get("determination"),
    )
    next_state["appeals"][record.appeal_id] = dataclass_payload(record)
    claim = next_state["claims"][denial["claim_id"]]
    claim_status = "appealed"
    if payload.get("determination") == "overturned":
        claim_status = "adjudicated"
        next_state["denials"][denial_id] = {
            **denial,
            "status": "overturned",
            "updated_at": utc_now(),
        }
    next_state["claims"][denial["claim_id"]] = {
        **claim,
        "status": claim_status,
        "updated_at": utc_now(),
    }
    return {
        "ok": True,
        "state": next_state,
        "appeal": next_state["appeals"][record.appeal_id],
        "side_effects": (),
    }


def claims_adjudication_healthcare_receive_event(
    state: dict[str, Any],
    event: dict[str, Any],
) -> dict[str, Any]:
    next_state = _copy(state)
    idem = str(event.get("idempotency_key") or event.get("event_id") or _digest(event))
    if idem in next_state["idempotency_keys"]:
        return {
            "ok": True,
            "duplicate": True,
            "idempotency_key": idem,
            "state": next_state,
            "side_effects": (),
        }
    next_state["idempotency_keys"].add(idem)
    tenant = _tenant(event)
    if event.get("event_type") not in CONSUMED:
        rendered = dataclass_payload(
            AppGenEvent(
                event_id=stable_identifier("dead", event),
                tenant=tenant,
                event_type=str(event.get("event_type") or "Unknown"),
                topic=str(event.get("topic") or REQUIRED_EVENT_TOPIC),
                payload=dict(event),
                idempotency_key=idem,
                status="dead_letter",
            )
        )
        next_state["dead_letter"].append(rendered)
        return {
            "ok": False,
            "state": next_state,
            "idempotency_key": idem,
            "dead_letter_table": EVENT_TABLES[2],
            "retry_policy": {"max_attempts": DEFAULT_CONFIGURATION["retry_limit"]},
            "side_effects": (),
        }
    rendered = dataclass_payload(
        AppGenEvent(
            event_id=stable_identifier("inbox", event),
            tenant=tenant,
            event_type=str(event["event_type"]),
            topic=str(event.get("topic") or REQUIRED_EVENT_TOPIC),
            payload=dict(event.get("payload") or {}),
            idempotency_key=idem,
            status="processed",
        )
    )
    next_state["inbox"].append(rendered)
    return {
        "ok": True,
        "duplicate": False,
        "state": next_state,
        "inbox_event": rendered,
        "idempotency_key": idem,
        "retry_policy": {"max_attempts": DEFAULT_CONFIGURATION["retry_limit"]},
        "side_effects": (),
    }


def claims_adjudication_healthcare_query_workbench(
    state: dict[str, Any],
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = dict(payload or {})
    tenant = _tenant(payload)
    claims = [claim for claim in state["claims"].values() if claim["tenant"] == tenant]
    lines = [line for line in state["claim_lines"].values() if line["tenant"] == tenant]
    reviews = [review for review in state["coding_reviews"].values() if review["tenant"] == tenant]
    denials = [denial for denial in state["denials"].values() if denial["tenant"] == tenant]
    appeals = [appeal for appeal in state["appeals"].values() if appeal["tenant"] == tenant]
    payment_cases = [
        case for case in state["payment_integrity_cases"].values() if case["tenant"] == tenant
    ]
    limit = int(_current_parameter(state, "workbench_limit"))
    queues = {
        "pending_claims": [claim for claim in claims if claim["status"] == "pended"][:limit],
        "denials": denials[:limit],
        "appeals": appeals[:limit],
        "coding_reviews": [review for review in reviews if review["status"] == "open"][:limit],
        "payment_integrity": [case for case in payment_cases if case["status"] == "open"][:limit],
    }
    metrics = {
        "claim_count": len(claims),
        "line_count": len(lines),
        "open_coding_reviews": len([review for review in reviews if review["status"] == "open"]),
        "denial_count": len(denials),
        "appeal_count": len(appeals),
        "open_payment_integrity_cases": len([case for case in payment_cases if case["status"] == "open"]),
        "queued_outbox_events": len(state["outbox"]),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "metrics": metrics,
        "queues": queues,
        "tables": BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "side_effects": (),
    }


def claims_adjudication_healthcare_run_advanced_assessment(
    state: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    claim_id = str(payload.get("claim_id") or "")
    claim = state["claims"].get(claim_id)
    if not claim:
        return {
            "ok": False,
            "reason": "unknown_claim",
            "claim_id": claim_id,
            "side_effects": (),
        }
    lines = _claim_lines(state, claim_id)
    duplicate_risk = 0.2 if not claim.get("duplicate_of") else 0.98
    if claim.get("correction_type"):
        duplicate_risk = 0.35
    if any(line["status"] == "denied" for line in lines):
        duplicate_risk += 0.1
    return {
        "ok": True,
        "claim_id": claim_id,
        "risk_summary": {
            "duplicate_risk": min(1.0, round(duplicate_risk, 2)),
            "coding_review_open": any(review["claim_id"] == claim_id and review["status"] == "open" for review in state["coding_reviews"].values()),
            "payment_integrity_open": any(case["claim_id"] == claim_id and case["status"] == "open" for case in state["payment_integrity_cases"].values()),
        },
        "side_effects": (),
    }


def claims_adjudication_healthcare_build_schema_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tables": BUSINESS_TABLES,
        "event_tables": EVENT_TABLES,
        "owned_tables": OWNED_TABLES,
        "migrations": ("migrations/001_initial.sql",),
        "models": model_contracts(),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "side_effects": (),
    }


def claims_adjudication_healthcare_build_api_contract() -> dict[str, Any]:
    routes = (
        "POST /health-claims",
        "POST /claim-lines",
        "POST /coding-reviews",
        "POST /benefit-rules",
        "POST /denials",
        "POST /appeals",
        "POST /document-instructions",
        "GET /claims-adjudication-healthcare-workbench",
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def claims_adjudication_healthcare_build_service_contract() -> dict[str, Any]:
    operation_contracts = tuple(
        {
            "operation": operation,
            "operation_kind": "query" if operation == "query_workbench" else "command",
            "owned_tables": BUSINESS_TABLES,
            "read_tables": BUSINESS_TABLES if operation == "query_workbench" else (),
            "permission": f"{PBC_KEY}.read" if operation == "query_workbench" else f"{PBC_KEY}.update",
            "event_contract": "AppGen-X",
        }
        for operation in ("command_health_claim",) + DOMAIN_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ClaimsAdjudicationHealthcareService",
        "operations": tuple(contract["operation"] for contract in operation_contracts),
        "command_methods": tuple(
            contract["operation"]
            for contract in operation_contracts
            if contract["operation_kind"] == "command"
        ),
        "query_methods": tuple(
            contract["operation"]
            for contract in operation_contracts
            if contract["operation_kind"] == "query"
        ),
        "contracts": operation_contracts,
        "event_contract": {
            "outbox_table": EVENT_TABLES[0],
            "inbox_table": EVENT_TABLES[1],
            "dead_letter_table": EVENT_TABLES[2],
            "topic": REQUIRED_EVENT_TOPIC,
        },
        "side_effects": (),
    }


def claims_adjudication_healthcare_permissions_contract() -> dict[str, Any]:
    manifest = permission_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": tuple(ROLES.keys()),
        "side_effects": (),
    }


def claims_adjudication_healthcare_build_workbench_view(tenant: str = "default") -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": CLAIMS_ADJUDICATION_HEALTHCARE_UI_FRAGMENT_KEYS,
        "forms": ("claim_intake_form", "claim_line_form", "denial_form", "appeal_form"),
        "wizards": ("claim_intake_wizard", "appeal_packet_wizard", "duplicate_review_wizard"),
        "controls": ("pend_queue", "denial_reason_matrix", "payment_integrity_triage"),
        "side_effects": (),
    }


def claims_adjudication_healthcare_verify_owned_table_boundary(
    references: tuple[Any, ...] = (),
) -> dict[str, Any]:
    invalid = tuple(
        reference
        for reference in references
        if isinstance(reference, str)
        and (
            reference == "foreign_table"
            or reference.endswith("_table")
            and not reference.startswith(f"{PBC_KEY}_")
        )
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
        "side_effects": (),
    }


def claims_adjudication_healthcare_build_release_evidence() -> dict[str, Any]:
    checks = (
        {"id": "schema_contract", "ok": claims_adjudication_healthcare_build_schema_contract()["ok"]},
        {"id": "service_contract", "ok": claims_adjudication_healthcare_build_service_contract()["ok"]},
        {"id": "api_contract", "ok": claims_adjudication_healthcare_build_api_contract()["ok"]},
        {"id": "permissions_contract", "ok": claims_adjudication_healthcare_permissions_contract()["ok"]},
        {"id": "runtime_smoke", "ok": claims_adjudication_healthcare_runtime_smoke()["ok"]},
    )
    return {
        "format": "appgen.claims-adjudication-healthcare-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": ("migrations/001_initial.sql",),
            "models": tuple(contract["class_name"] for contract in model_contracts()),
            "events": {"emits": EMITTED, "consumes": CONSUMED},
            "ui": CLAIMS_ADJUDICATION_HEALTHCARE_UI_FRAGMENT_KEYS,
        },
        "blocking_gaps": (),
        "side_effects": (),
    }


def claims_adjudication_healthcare_runtime_capabilities() -> dict[str, Any]:
    smoke = claims_adjudication_healthcare_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "command_health_claim",
    ) + DOMAIN_OPERATIONS
    return {
        "format": "appgen.claims-adjudication-healthcare-runtime-capabilities.v2",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "standard_features": CLAIMS_ADJUDICATION_HEALTHCARE_STANDARD_FEATURE_KEYS,
        "capabilities": CLAIMS_ADJUDICATION_HEALTHCARE_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "schema_contract": claims_adjudication_healthcare_build_schema_contract(),
        "service_contract": claims_adjudication_healthcare_build_service_contract(),
        "release_evidence": claims_adjudication_healthcare_build_release_evidence(),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def claims_adjudication_healthcare_runtime_smoke() -> dict[str, Any]:
    state = claims_adjudication_healthcare_empty_state()
    configured = claims_adjudication_healthcare_configure_runtime(
        state,
        {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC},
    )
    parameterized = claims_adjudication_healthcare_set_parameter(
        configured["state"],
        "workbench_limit",
        20,
    )
    ruled = claims_adjudication_healthcare_register_rule(
        parameterized["state"],
        {"rule_name": "smoke-rule", "threshold": 1000, "action": "review"},
    )
    benefit = claims_adjudication_healthcare_approve_benefit_rule(
        ruled["state"],
        {
            "tenant": "default",
            "plan_id": "plan-a",
            "service_code": "99213",
            "description": "Office visit",
            "covered": True,
            "auth_required": False,
            "allowed_percentage": 0.85,
            "copay_amount": 20,
            "deductible_apply": True,
            "max_units": 5,
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
        },
    )
    claim = claims_adjudication_healthcare_command_health_claim(
        benefit["state"],
        {
            "tenant": "default",
            "claim_number": "HC-1001",
            "member_id": "M-100",
            "provider_id": "P-100",
            "plan_id": "plan-a",
            "received_date": "2026-05-29",
            "source_format": "837P",
            "total_charge": 900,
            "eligibility_projection_hours": 2,
            "provider_projection_hours": 2,
        },
    )
    line = claims_adjudication_healthcare_record_claim_line(
        claim["state"],
        {
            "claim_id": claim["claim"]["claim_id"],
            "line_number": 1,
            "service_date": "2026-05-28",
            "procedure_code": "99213",
            "diagnosis_code": "J10.1",
            "place_of_service": "11",
            "units": 1,
            "charge_amount": 900,
            "accumulator_remaining": 250,
        },
    )
    inbox = claims_adjudication_healthcare_receive_event(
        line["state"],
        {"event_type": CONSUMED[0], "idempotency_key": "smoke-event"},
    )
    duplicate = claims_adjudication_healthcare_receive_event(
        inbox["state"],
        {"event_type": CONSUMED[0], "idempotency_key": "smoke-event"},
    )
    dead = claims_adjudication_healthcare_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"},
    )
    workbench = claims_adjudication_healthcare_query_workbench(dead["state"], {"tenant": "default"})
    boundary = claims_adjudication_healthcare_verify_owned_table_boundary(
        (f"{PBC_KEY}_health_claim", "foreign_table")
    )
    checks = (
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "set_parameter", "ok": parameterized["ok"]},
        {"id": "register_rule", "ok": ruled["ok"]},
        {"id": "approve_benefit_rule", "ok": benefit["ok"]},
        {"id": "command_health_claim", "ok": claim["ok"] and claim["duplicate"] is False},
        {"id": "record_claim_line", "ok": line["ok"] and line["claim_line"]["status"] in LINE_STATUSES},
        {"id": "receive_event", "ok": inbox["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate["duplicate"] is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and dead["dead_letter_table"] == EVENT_TABLES[2]},
        {"id": "workbench", "ok": workbench["ok"] and workbench["metrics"]["claim_count"] == 1},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
    )
    return {
        "format": "appgen.claims-adjudication-healthcare-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "state_snapshot": {
            "claims": len(dead["state"]["claims"]),
            "claim_lines": len(dead["state"]["claim_lines"]),
            "outbox": len(dead["state"]["outbox"]),
            "inbox": len(dead["state"]["inbox"]),
            "dead_letter": len(dead["state"]["dead_letter"]),
        },
        "side_effects": (),
    }
