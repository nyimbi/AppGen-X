"""Owned model metadata for the construction_project_controls PBC."""
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .runtime import construction_project_controls_build_schema_contract

PBC_KEY = "construction_project_controls"


@dataclass(frozen=True)
class ConstructionProjectModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    name: str = ""
    status: str = ""
    project_manager: str = ""
    contractor: str = ""
    original_budget: float = 0.0
    approved_budget: float = 0.0
    active_baseline_revision_id: str | None = None
    baseline_revisions: tuple[dict[str, Any], ...] = ()
    reporting_periods: tuple[str, ...] = ()
    release_scorecard: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class WorkPackageModel:
    id: str = ""
    tenant: str = ""
    project_id: str = ""
    wbs_code: str = ""
    parent_wbs_code: str | None = None
    control_account: str = ""
    discipline: str = ""
    area: str = ""
    contractor: str = ""
    progress_method: str = ""
    planned_quantity: float = 0.0
    installed_quantity: float = 0.0
    measurement_unit: str = ""
    planned_percent_complete: float = 0.0
    percent_complete: float = 0.0
    original_budget: float = 0.0
    approved_budget: float = 0.0
    actual_cost: float = 0.0
    forecast_remaining_cost: float = 0.0
    payment_readiness: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class RfiModel:
    id: str = ""
    tenant: str = ""
    project_id: str = ""
    code: str = ""
    status: str = ""
    subject: str = ""
    affected_wbs_code: str | None = None
    required_by_date: str | None = None
    schedule_impact_classification: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class SubmittalModel:
    id: str = ""
    tenant: str = ""
    project_id: str = ""
    code: str = ""
    status: str = ""
    linked_wbs_code: str | None = None
    planned_submit_date: str | None = None
    required_approval_date: str | None = None
    approval_cycle_count: int = 0
    blocked_work: tuple[str, ...] = ()
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class SiteProgressModel:
    id: str = ""
    tenant: str = ""
    project_id: str = ""
    work_package_id: str = ""
    submission_key: str = ""
    measurement_date: str = ""
    progress_method: str = ""
    installed_quantity: float = 0.0
    measurement_unit: str = ""
    percent_complete: float = 0.0
    accepted_status: str = ""
    evidence_bundle: dict[str, Any] = field(default_factory=dict)
    actual_cost_incurred: float = 0.0
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ChangeEventModel:
    id: str = ""
    tenant: str = ""
    project_id: str = ""
    code: str = ""
    status: str = ""
    trend_reference: str | None = None
    cause_category: str = ""
    affected_wbs_codes: tuple[str, ...] = ()
    cost_impact: float = 0.0
    schedule_impact_days: float = 0.0
    approval_state: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ScheduleRiskModel:
    id: str = ""
    tenant: str = ""
    project_id: str = ""
    code: str = ""
    status: str = ""
    work_package_id: str | None = None
    current_float_days: float = 0.0
    prior_float_days: float = 0.0
    path_status: str = ""
    owner: str = ""
    issue_state: str = ""
    escalation_required: bool = False
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class PolicyRuleModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class RuntimeParameterModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class SchemaExtensionModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class ControlAssertionModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class GovernedModelRecord:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class OutboxEventModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class InboxEventModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class DeadLetterEventModel:
    id: str = ""
    tenant: str = ""
    code: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


TABLE_TO_CLASS = (
    (f"{PBC_KEY}_construction_project", ConstructionProjectModel),
    (f"{PBC_KEY}_work_package", WorkPackageModel),
    (f"{PBC_KEY}_rfi", RfiModel),
    (f"{PBC_KEY}_submittal", SubmittalModel),
    (f"{PBC_KEY}_site_progress", SiteProgressModel),
    (f"{PBC_KEY}_change_event", ChangeEventModel),
    (f"{PBC_KEY}_schedule_risk", ScheduleRiskModel),
    (f"{PBC_KEY}_construction_project_controls_policy_rule", PolicyRuleModel),
    (f"{PBC_KEY}_construction_project_controls_runtime_parameter", RuntimeParameterModel),
    (f"{PBC_KEY}_construction_project_controls_schema_extension", SchemaExtensionModel),
    (f"{PBC_KEY}_construction_project_controls_control_assertion", ControlAssertionModel),
    (f"{PBC_KEY}_construction_project_controls_governed_model", GovernedModelRecord),
    (f"{PBC_KEY}_appgen_outbox_event", OutboxEventModel),
    (f"{PBC_KEY}_appgen_inbox_event", InboxEventModel),
    (f"{PBC_KEY}_appgen_dead_letter_event", DeadLetterEventModel),
)


def _schema_tables() -> tuple[dict[str, Any], ...]:
    return construction_project_controls_build_schema_contract()["tables"]


def _model_registry() -> tuple[dict[str, Any], ...]:
    schema_by_table = {table["table"]: table for table in _schema_tables()}
    return tuple(
        {
            "class_name": model_class.__name__,
            "table": table_name,
            "fields": tuple(schema_by_table[table_name]["fields"]),
            "domain_role": table_name.removeprefix(f"{PBC_KEY}_"),
            "model_class": model_class,
        }
        for table_name, model_class in TABLE_TO_CLASS
    )


MODEL_REGISTRY = _model_registry()


def model_contracts() -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "class_name": entry["class_name"],
            "table": entry["table"],
            "fields": entry["fields"],
            "domain_role": entry["domain_role"],
        }
        for entry in MODEL_REGISTRY
    )


def model_catalog() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "models": tuple(entry["table"] for entry in MODEL_REGISTRY),
        "side_effects": (),
    }


def model_manifest() -> dict[str, Any]:
    schema_tables = tuple(table["table"] for table in _schema_tables())
    model_tables = tuple(entry["table"] for entry in MODEL_REGISTRY)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f"{PBC_KEY}_"))
    return {
        "ok": bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models,
        "pbc": PBC_KEY,
        "schema_tables": schema_tables,
        "model_tables": model_tables,
        "missing_models": missing_models,
        "external_models": external_models,
        "cross_pbc_relationships": (),
        "relationship_targets": (),
        "side_effects": (),
    }


def instantiate_model(table_name: str, values: dict[str, Any] | None = None) -> dict[str, Any]:
    entry = next((item for item in MODEL_REGISTRY if item["table"] == table_name), None)
    if entry is None:
        return {
            "ok": False,
            "reason": "unknown_model",
            "table": table_name,
            "side_effects": (),
        }
    supplied = dict(values or {})
    fields = tuple(entry["fields"])
    payload = {field_name: supplied.get(field_name) for field_name in fields}
    instance_values = {
        field_name: supplied[field_name]
        for field_name in fields
        if field_name in supplied
    }
    instance = entry["model_class"](**instance_values)
    return {
        "ok": table_name.startswith(f"{PBC_KEY}_") and bool(fields),
        "pbc": PBC_KEY,
        "model": entry["class_name"],
        "table": table_name,
        "fields": fields,
        "payload": payload,
        "instance": asdict(instance),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    manifest = model_manifest()
    first_table = manifest["model_tables"][0] if manifest["model_tables"] else None
    instance = (
        instantiate_model(
            first_table,
            {"id": "CP-001", "tenant": "tenant-smoke", "code": "CP-001", "name": "Smoke Tower"},
        )
        if first_table
        else {"ok": False}
    )
    return {
        "ok": manifest["ok"] and instance.get("ok") is True,
        "manifest": manifest,
        "instance": instance,
        "side_effects": (),
    }
