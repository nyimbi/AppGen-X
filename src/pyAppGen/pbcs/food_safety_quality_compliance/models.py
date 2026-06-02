"""Owned model definitions for the food_safety_quality_compliance PBC."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .slice_app import TABLE_DEFINITIONS


@dataclass(frozen=True)
class FoodSafetyQualityComplianceHaccpPlan:
    id: str
    tenant: str
    plan_code: str
    version: str
    facility_code: str
    product_scope: tuple[str, ...] = ()
    lifecycle_state: str = "draft"
    process_steps: tuple[dict[str, Any], ...] = ()
    hazard_analysis: tuple[dict[str, Any], ...] = ()
    approvals: dict[str, bool] = field(default_factory=dict)
    effective_from: str | None = None
    supersedes_plan_id: str | None = None
    supersession_reason: str | None = None
    evidence_hash: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceCriticalControlPoint:
    id: str
    tenant: str
    plan_id: str
    process_step_code: str
    hazard_id: str
    limit_min: float
    limit_max: float
    unit: str
    monitoring_method: str
    monitoring_frequency_minutes: int
    responsible_role: str = "line_quality"
    verification_requirement: str = "daily_supervisor_review"
    corrective_action: str = "Hold affected lots and investigate root cause."
    status: str = "active"
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceInspection:
    id: str
    tenant: str
    plan_id: str
    plan_code: str
    plan_version: str
    facility_code: str
    area: str
    checklist: tuple[str, ...] = ()
    findings: tuple[dict[str, Any], ...] = ()
    score: int = 100
    repeat_findings: tuple[str, ...] = ()
    status: str = "review_complete"
    created_hold_ids: tuple[str, ...] = ()
    created_nonconformance_ids: tuple[str, ...] = ()
    inspector: str = ""
    started_at: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceNonconformance:
    id: str
    tenant: str
    category: str
    severity: str
    product_impact: str
    process_step_code: str = ""
    containment_action: str = ""
    corrective_action: str = ""
    preventive_action: str = ""
    root_cause_method: str = ""
    confirmed_root_cause: str = ""
    effectiveness_evidence: str = ""
    recurrence_flag: bool = False
    status: str = "open"
    source_inspection_id: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceRecallEvent:
    id: str
    tenant: str
    classification: str
    reason: str
    consumer_risk: str
    distribution_scope: str
    affected_lots: tuple[str, ...] = ()
    customers: tuple[str, ...] = ()
    regulator_notification: dict[str, Any] = field(default_factory=dict)
    communication_plan: dict[str, Any] = field(default_factory=dict)
    is_mock_drill: bool = False
    trace_elapsed_minutes: int = 0
    projection_boundary_ok: bool = True
    status: str = "draft"
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceSupplierAudit:
    id: str
    tenant: str
    supplier_projection: dict[str, Any] = field(default_factory=dict)
    commodity: str = ""
    audit_type: str = ""
    risk_rating: str = "medium"
    findings: tuple[dict[str, Any], ...] = ()
    corrective_actions: tuple[str, ...] = ()
    approval_status: str = "approved"
    expiry_date: str = ""
    days_until_expiry: int = 0
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceQualityHold:
    id: str
    tenant: str
    hold_reason: str
    affected_lots: tuple[str, ...] = ()
    quantity: float = 0.0
    location: str = ""
    release_criteria: tuple[str, ...] = ()
    disposition: str = "pending"
    approved_by: tuple[str, ...] = ()
    released_at: str | None = None
    source_inspection_id: str = ""
    haccp_plan_id: str = ""
    haccp_plan_version: str = ""
    status: str = "open"
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityCompliancePolicyRule:
    id: str
    tenant: str
    rule_id: str
    scope: str
    status: str
    rule_text: str
    compiled_hash: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceRuntimeParameter:
    id: str
    tenant: str
    parameter_name: str
    parameter_value: Any
    unit: str
    bounded: bool
    status: str
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceSchemaExtension:
    id: str
    tenant: str
    table_name: str
    field_map: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    status: str = "proposed"
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceControlAssertion:
    id: str
    tenant: str
    control_id: str
    control_name: str
    frequency: str
    status: str
    assertion_payload: dict[str, Any] = field(default_factory=dict)
    evidence_hash: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FoodSafetyQualityComplianceGovernedModel:
    id: str
    tenant: str
    artifact_type: str
    artifact_key: str
    status: str
    document_digest: str
    instruction_payload: dict[str, Any] = field(default_factory=dict)
    mutation_preview: dict[str, Any] = field(default_factory=dict)
    citations: tuple[str, ...] = ()
    human_confirmation_state: str = "required"
    approved_by: str = ""
    created_at: str = ""
    updated_at: str = ""


MODEL_CLASSES = (
    FoodSafetyQualityComplianceHaccpPlan,
    FoodSafetyQualityComplianceCriticalControlPoint,
    FoodSafetyQualityComplianceInspection,
    FoodSafetyQualityComplianceNonconformance,
    FoodSafetyQualityComplianceRecallEvent,
    FoodSafetyQualityComplianceSupplierAudit,
    FoodSafetyQualityComplianceQualityHold,
    FoodSafetyQualityCompliancePolicyRule,
    FoodSafetyQualityComplianceRuntimeParameter,
    FoodSafetyQualityComplianceSchemaExtension,
    FoodSafetyQualityComplianceControlAssertion,
    FoodSafetyQualityComplianceGovernedModel,
)


def model_contracts() -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "class_name": item["class_name"],
            "table": item["table"],
            "fields": item["fields"],
            "domain_role": item["domain_role"],
        }
        for item in TABLE_DEFINITIONS
    )


def model_instance_examples() -> dict[str, dict[str, Any]]:
    plan = FoodSafetyQualityComplianceHaccpPlan(
        id="plan-RTE-1",
        tenant="tenant-demo",
        plan_code="RTE-CHILL",
        version="2",
        facility_code="FAC-1",
        product_scope=("ready_to_eat_meals",),
        lifecycle_state="approved",
        process_steps=({"step_code": "cook"}, {"step_code": "chill"}),
        hazard_analysis=({"hazard_id": "haz-1", "process_step_code": "cook", "requires_ccp": True},),
        approvals={"food_safety": True, "quality": True, "operations": True},
        effective_from="2026-01-03",
        evidence_hash="demo",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )
    ccp = FoodSafetyQualityComplianceCriticalControlPoint(
        id="ccp-1",
        tenant="tenant-demo",
        plan_id=plan.id,
        process_step_code="cook",
        hazard_id="haz-1",
        limit_min=74.0,
        limit_max=76.0,
        unit="celsius",
        monitoring_method="probe",
        monitoring_frequency_minutes=15,
    )
    inspection = FoodSafetyQualityComplianceInspection(
        id="inspection-1",
        tenant="tenant-demo",
        plan_id=plan.id,
        plan_code=plan.plan_code,
        plan_version=plan.version,
        facility_code=plan.facility_code,
        area="cooling-room",
        checklist=("preop", "temperature"),
        findings=({"category": "temperature", "severity": "critical"},),
        score=70,
        created_hold_ids=("hold-1",),
        created_nonconformance_ids=("nc-1",),
        inspector="qa.lead",
    )
    hold = FoodSafetyQualityComplianceQualityHold(
        id="hold-1",
        tenant="tenant-demo",
        hold_reason="Rapid chill exceeded safe temperature.",
        affected_lots=("LOT-100",),
        quantity=42.0,
        location="quality-cage",
        release_criteria=("approved_disposition",),
        haccp_plan_id=plan.id,
        haccp_plan_version=plan.version,
    )
    recall = FoodSafetyQualityComplianceRecallEvent(
        id="recall-1",
        tenant="tenant-demo",
        classification="mock_recall",
        reason="annual_readiness",
        consumer_risk="moderate",
        distribution_scope="national",
        affected_lots=("LOT-100",),
        customers=("Retailer A",),
        is_mock_drill=True,
        trace_elapsed_minutes=80,
    )
    return {
        "plan": asdict(plan),
        "critical_control_point": asdict(ccp),
        "inspection": asdict(inspection),
        "quality_hold": asdict(hold),
        "recall": asdict(recall),
    }
