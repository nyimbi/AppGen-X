"""Construction project controls domain surface metadata."""
from __future__ import annotations

import hashlib

PBC_KEY = "construction_project_controls"
DOMAIN_ENTITY = "construction_project"
DOMAIN_PURPOSE = (
    "Govern WBS hierarchy, frozen baselines, quantity-based progress, earned-value rollups, "
    "schedule risk escalation, and release-ready reporting packs for construction projects."
)
DOMAIN_OWNED_TABLES = (
    "construction_project_controls_construction_project",
    "construction_project_controls_work_package",
    "construction_project_controls_rfi",
    "construction_project_controls_submittal",
    "construction_project_controls_site_progress",
    "construction_project_controls_change_event",
    "construction_project_controls_schedule_risk",
    "construction_project_controls_construction_project_controls_policy_rule",
    "construction_project_controls_construction_project_controls_runtime_parameter",
    "construction_project_controls_construction_project_controls_schema_extension",
    "construction_project_controls_construction_project_controls_control_assertion",
    "construction_project_controls_construction_project_controls_governed_model",
    "construction_project_controls_appgen_outbox_event",
    "construction_project_controls_appgen_inbox_event",
    "construction_project_controls_appgen_dead_letter_event",
)
DOMAIN_OPERATIONS = (
    "create_construction_project",
    "approve_baseline_revision",
    "record_work_package",
    "review_rfi",
    "approve_submittal",
    "record_site_progress",
    "create_change_event",
    "record_schedule_risk",
    "freeze_reporting_period",
    "reopen_reporting_period",
    "review_policy_rule",
    "approve_runtime_parameter",
    "record_control_assertion",
    "record_governed_model",
    "simulate_recovery_scenario",
    "publish_release_readiness",
)
DOMAIN_RULES = (
    "baseline_freeze_policy",
    "progress_evidence_policy",
    "float_threshold_policy",
    "period_freeze_policy",
    "release_readiness_policy",
    "approval_threshold_policy",
)
DOMAIN_PARAMETERS = (
    "workbench_limit",
    "float_near_critical_days",
    "float_critical_days",
    "progress_evidence_required",
    "forecast_horizon_days",
    "risk_score_floor",
    "variance_warning_percent",
)
DOMAIN_EVENTS = (
    "ConstructionProjectControlsCreated",
    "ConstructionProjectControlsUpdated",
    "ConstructionProjectControlsApproved",
    "ConstructionProjectControlsExceptionOpened",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
DOMAIN_ADVANCED_CAPABILITIES = (
    "construction project controls event sourced operational history",
    "construction project controls predictive risk scoring",
    "construction project controls release readiness automation",
    "construction project controls governed assistant previews",
    "construction project controls schedule exception management",
    "construction project controls quantity-based earned value analytics",
)
DOMAIN_WORKBENCH_VIEWS = (
    "portfolio risk board",
    "wbs rollup tree",
    "earned value dashboard",
    "exception queue",
)


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 15,
        "minimum_domain_operations": 15,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {
            "ok": False,
            "reason": "unknown_domain_operation",
            "operation": operation,
            "side_effects": (),
        }
    index = DOMAIN_OPERATIONS.index(operation)
    target_table = DOMAIN_OWNED_TABLES[min(index, len(DOMAIN_OWNED_TABLES) - 1)]
    emitted_event = DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": (),
        "emitted_event": emitted_event,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:4],
        "permission": f"{PBC_KEY}.operate",
        "evidence_hash": _digest((operation, payload, target_table, emitted_event)),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(
        execute_domain_operation(operation, {"tenant": "tenant-smoke"})
        for operation in DOMAIN_OPERATIONS[:5]
    )
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions)
        and all(item["target_table"].startswith(f"{PBC_KEY}_") for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = (
    "duplicate_progress_submission",
    "missing_parent_wbs_code",
    "baseline_without_approval_evidence",
    "progress_without_evidence",
    "quantity_overstatement",
    "reporting_period_frozen",
    "negative_float_spike",
    "cross_tenant_access_attempt",
    "document_instruction_without_confirmation",
    "release_evidence_locked",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        tuple(DOMAIN_ADVANCED_CAPABILITIES)
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": DOMAIN_OWNED_TABLES[min(index, len(DOMAIN_OWNED_TABLES) - 1)],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": operation
                in ("approve_baseline_revision", "freeze_reporting_period", "publish_release_readiness"),
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)],
            }
            for index, operation in enumerate(DOMAIN_OPERATIONS)
        ),
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "bounded": True,
                "editable": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }
