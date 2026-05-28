"""Domain models and schema metadata for the healthcare claims adjudication PBC."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime
import hashlib
from typing import Any

PBC_KEY = "claims_adjudication_healthcare"

BUSINESS_TABLES = (
    f"{PBC_KEY}_health_claim",
    f"{PBC_KEY}_claim_line",
    f"{PBC_KEY}_coding_review",
    f"{PBC_KEY}_benefit_rule",
    f"{PBC_KEY}_denial",
    f"{PBC_KEY}_appeal",
    f"{PBC_KEY}_payment_integrity_case",
    f"{PBC_KEY}_policy_rule",
    f"{PBC_KEY}_runtime_parameter",
    f"{PBC_KEY}_schema_extension",
    f"{PBC_KEY}_control_assertion",
    f"{PBC_KEY}_governed_model",
    f"{PBC_KEY}_document_instruction",
)

EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)

OWNED_TABLES = BUSINESS_TABLES + EVENT_TABLES


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def stable_identifier(prefix: str, payload: Any) -> str:
    digest = hashlib.sha256(repr(payload).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


@dataclass(slots=True, frozen=True)
class HealthClaim:
    claim_id: str
    tenant: str
    claim_number: str
    claim_type: str
    source_format: str
    member_id: str
    provider_id: str
    plan_id: str
    received_date: str
    status: str = "received"
    priority: str = "standard"
    total_charge: float = 0.0
    duplicate_of: str | None = None
    pend_reason: str | None = None
    original_claim_id: str | None = None
    correction_type: str | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ClaimLine:
    line_id: str
    claim_id: str
    tenant: str
    line_number: int
    service_date: str
    procedure_code: str
    diagnosis_code: str
    place_of_service: str
    units: int
    charge_amount: float
    authorization_id: str | None = None
    modifiers: tuple[str, ...] = ()
    status: str = "received"
    allowed_amount: float = 0.0
    member_responsibility: float = 0.0
    payer_responsibility: float = 0.0
    adjudication_reason: str | None = None
    reason_codes: tuple[str, ...] = ()
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class CodingReview:
    review_id: str
    claim_id: str
    tenant: str
    issue_type: str
    severity: str
    status: str = "open"
    line_id: str | None = None
    notes: str = ""
    override_reason: str | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class BenefitRule:
    rule_id: str
    tenant: str
    plan_id: str
    service_code: str
    description: str
    covered: bool
    auth_required: bool
    allowed_percentage: float
    copay_amount: float
    deductible_apply: bool
    max_units: int
    effective_from: str
    effective_to: str
    status: str = "draft"
    approval_reference: str | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class Denial:
    denial_id: str
    claim_id: str
    tenant: str
    denial_code: str
    rationale: str
    policy_rule_id: str
    line_ids: tuple[str, ...]
    notice_deadline: str
    status: str = "issued"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class Appeal:
    appeal_id: str
    denial_id: str
    claim_id: str
    tenant: str
    level: str
    requester: str
    evidence_summary: str
    status: str = "received"
    determination: str | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class PaymentIntegrityCase:
    case_id: str
    claim_id: str
    tenant: str
    trigger: str
    exposure_amount: float
    reviewer: str
    notes: str
    status: str = "open"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class PolicyRule:
    policy_rule_id: str
    tenant: str
    rule_name: str
    description: str
    condition_key: str
    threshold: float
    action: str
    status: str = "approved"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class RuntimeParameter:
    parameter_name: str
    tenant: str
    value: float
    minimum: float
    maximum: float
    unit: str
    status: str = "active"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class SchemaExtension:
    extension_id: str
    tenant: str
    target_table: str
    column_name: str
    data_type: str
    justification: str
    status: str = "proposed"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class ControlAssertion:
    assertion_id: str
    tenant: str
    control_name: str
    objective: str
    frequency: str
    status: str = "active"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class GovernedModel:
    model_id: str
    tenant: str
    model_name: str
    purpose: str
    version: str
    approval_status: str
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class DocumentInstruction:
    instruction_id: str
    tenant: str
    document_name: str
    instruction_text: str
    target_table: str
    action: str
    status: str = "draft"
    structured_fields: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True, frozen=True)
class AppGenEvent:
    event_id: str
    tenant: str
    event_type: str
    topic: str
    payload: dict[str, Any]
    idempotency_key: str
    status: str
    created_at: str = field(default_factory=utc_now)


MODEL_INDEX = {
    "health_claim": (HealthClaim, BUSINESS_TABLES[0]),
    "claim_line": (ClaimLine, BUSINESS_TABLES[1]),
    "coding_review": (CodingReview, BUSINESS_TABLES[2]),
    "benefit_rule": (BenefitRule, BUSINESS_TABLES[3]),
    "denial": (Denial, BUSINESS_TABLES[4]),
    "appeal": (Appeal, BUSINESS_TABLES[5]),
    "payment_integrity_case": (PaymentIntegrityCase, BUSINESS_TABLES[6]),
    "policy_rule": (PolicyRule, BUSINESS_TABLES[7]),
    "runtime_parameter": (RuntimeParameter, BUSINESS_TABLES[8]),
    "schema_extension": (SchemaExtension, BUSINESS_TABLES[9]),
    "control_assertion": (ControlAssertion, BUSINESS_TABLES[10]),
    "governed_model": (GovernedModel, BUSINESS_TABLES[11]),
    "document_instruction": (DocumentInstruction, BUSINESS_TABLES[12]),
    "outbox_event": (AppGenEvent, EVENT_TABLES[0]),
    "inbox_event": (AppGenEvent, EVENT_TABLES[1]),
    "dead_letter_event": (AppGenEvent, EVENT_TABLES[2]),
}


def dataclass_payload(record: Any) -> dict[str, Any]:
    return asdict(record)


def model_contracts() -> tuple[dict[str, Any], ...]:
    contracts: list[dict[str, Any]] = []
    for entity, (model_cls, table) in MODEL_INDEX.items():
        contracts.append(
            {
                "entity": entity,
                "table": table,
                "class_name": model_cls.__name__,
                "fields": tuple(model_cls.__dataclass_fields__.keys()),
                "owned": True,
                "event_sourced": entity.endswith("_event"),
            }
        )
    return tuple(contracts)


def model_lookup(entity: str) -> dict[str, Any]:
    model_cls, table = MODEL_INDEX[entity]
    return {
        "entity": entity,
        "table": table,
        "class_name": model_cls.__name__,
        "fields": tuple(model_cls.__dataclass_fields__.keys()),
    }
