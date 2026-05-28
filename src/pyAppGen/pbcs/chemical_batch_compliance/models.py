"""Owned model definitions for the chemical_batch_compliance PBC."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .slice_app import TABLE_DEFINITIONS


@dataclass(frozen=True)
class ChemicalBatchComplianceChemicalFormula:
    id: str
    tenant: str
    formula_code: str
    revision: str
    lifecycle_state: str
    product_name: str
    target_concentration: dict[str, Any] = field(default_factory=dict)
    composition_window: dict[str, Any] = field(default_factory=dict)
    approved_substitutes: tuple[dict[str, Any], ...] = ()
    required_sds_ids: tuple[str, ...] = ()
    required_hazard_material_ids: tuple[str, ...] = ()
    required_permits: tuple[str, ...] = ()
    equipment_classes: tuple[str, ...] = ()
    approvals: dict[str, bool] = field(default_factory=dict)
    effectivity_start: str = ""
    effectivity_end: str | None = None
    process_steps: tuple[dict[str, Any], ...] = ()
    evidence_hash: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceBatchRecord:
    id: str
    tenant: str
    batch_number: str
    formula_id: str
    formula_revision: str
    lifecycle_state: str
    equipment_profile: dict[str, Any] = field(default_factory=dict)
    step_timeline: tuple[dict[str, Any], ...] = ()
    dispense_reconciliation: tuple[dict[str, Any], ...] = ()
    parameter_log: tuple[dict[str, Any], ...] = ()
    sampling_plan: tuple[dict[str, Any], ...] = ()
    deviation_summary: tuple[str, ...] = ()
    release_decision: str = "pending_quality"
    risk_score: float = 0.0
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceSdsDocument:
    id: str
    tenant: str
    material_code: str
    revision: str
    status: str
    issue_date: str
    expiration_date: str
    jurisdictions: tuple[str, ...] = ()
    hazard_summary: dict[str, Any] = field(default_factory=dict)
    exposure_controls: tuple[str, ...] = ()
    document_digest: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceHazardousMaterial:
    id: str
    tenant: str
    material_code: str
    status: str
    un_number: str = ""
    ghs_classification: tuple[str, ...] = ()
    storage_class: str = ""
    approved_sources: tuple[str, ...] = ()
    ppe_requirements: tuple[str, ...] = ()
    label_profile: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceRegulatorySubmission:
    id: str
    tenant: str
    dossier_number: str
    status: str
    jurisdiction: str
    submission_type: str
    product_code: str
    source_record_ids: tuple[str, ...] = ()
    commitment_actions: tuple[str, ...] = ()
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceQualityTest:
    id: str
    tenant: str
    batch_id: str
    sample_point: str
    test_name: str
    specification: dict[str, Any] = field(default_factory=dict)
    result_value: Any = None
    result_status: str = "pass"
    requires_hold: bool = False
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceComplianceHold:
    id: str
    tenant: str
    entity_type: str
    entity_id: str
    hold_reason: str
    severity: str
    status: str
    disposition: str
    released_by: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchCompliancePolicyRule:
    id: str
    tenant: str
    rule_id: str
    status: str
    scope: str
    rule_kind: str
    threshold_json: dict[str, Any] = field(default_factory=dict)
    compiled_hash: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceRuntimeParameter:
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
class ChemicalBatchComplianceSchemaExtension:
    id: str
    tenant: str
    table_name: str
    status: str
    field_map: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceControlAssertion:
    id: str
    tenant: str
    control_id: str
    control_name: str
    status: str
    frequency: str
    assertion_payload: dict[str, Any] = field(default_factory=dict)
    evidence_hash: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChemicalBatchComplianceGovernedModel:
    id: str
    tenant: str
    artifact_type: str
    artifact_key: str
    status: str
    document_digest: str
    instruction_payload: dict[str, Any] = field(default_factory=dict)
    mutation_preview: dict[str, Any] = field(default_factory=dict)
    human_confirmation_state: str = "required"
    created_at: str = ""
    updated_at: str = ""


MODEL_CLASSES = (
    ChemicalBatchComplianceChemicalFormula,
    ChemicalBatchComplianceBatchRecord,
    ChemicalBatchComplianceSdsDocument,
    ChemicalBatchComplianceHazardousMaterial,
    ChemicalBatchComplianceRegulatorySubmission,
    ChemicalBatchComplianceQualityTest,
    ChemicalBatchComplianceComplianceHold,
    ChemicalBatchCompliancePolicyRule,
    ChemicalBatchComplianceRuntimeParameter,
    ChemicalBatchComplianceSchemaExtension,
    ChemicalBatchComplianceControlAssertion,
    ChemicalBatchComplianceGovernedModel,
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
    sample_formula = ChemicalBatchComplianceChemicalFormula(
        id="formula-CBR-77-rev-A",
        tenant="tenant-demo",
        formula_code="CBR-77",
        revision="A",
        lifecycle_state="effective",
        product_name="Catalyst Blend 77",
        target_concentration={"assay_pct": 98.5},
        composition_window={"solvent_pct_min": 30, "solvent_pct_max": 32},
        required_sds_ids=("sds-SOLV-100-7",),
        required_hazard_material_ids=("hazmat-SOLV-100",),
        required_permits=("hot_work",),
        equipment_classes=("reactor_train_a",),
        approvals={"technical": True, "quality": True, "ehs": True},
        effectivity_start="2026-01-02",
        process_steps=({"step_code": "charge", "critical": True},),
        evidence_hash="demo",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )
    sample_batch = ChemicalBatchComplianceBatchRecord(
        id="batch-BATCH-1001",
        tenant="tenant-demo",
        batch_number="BATCH-1001",
        formula_id=sample_formula.id,
        formula_revision="A",
        lifecycle_state="review_pending",
        equipment_profile={"line_clearance": True},
        step_timeline=({"step_code": "charge", "status": "complete"},),
        release_decision="pending_quality",
        risk_score=0.22,
        created_at="2026-01-01T00:00:01Z",
        updated_at="2026-01-01T00:00:01Z",
    )
    return {"formula": asdict(sample_formula), "batch": asdict(sample_batch)}
