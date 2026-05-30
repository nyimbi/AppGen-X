"""World-class domain depth contract for the water_wastewater_operations PBC."""

from __future__ import annotations

from .operations_engine import (
    ADVANCED_CAPABILITIES,
    ALLOWED_DATABASE_BACKENDS,
    BUSINESS_TABLES,
    CONSUMED_EVENT_TYPES,
    CONTROL_DEFINITIONS,
    DOMAIN_OPERATIONS,
    EMITTED_EVENT_TYPES,
    FORM_DEFINITIONS,
    PARAMETER_SPECS,
    PBC_KEY,
    RULES,
    UI_FRAGMENTS,
    WIZARD_DEFINITIONS,
    WORKBENCH_SECTIONS,
    preview_domain_operation,
)

DOMAIN_ENTITY = "treatment_plant"
DOMAIN_PURPOSE = (
    "Treatment plant operations, source-water oversight, production, distribution pressure and quality, "
    "pump/valve work, sewer and lift-station risk, wastewater treatment, permits, incidents, flushing, "
    "hydrants, asset isolation, SCADA projections, and governed operator assistance."
)
DOMAIN_OWNED_TABLES = BUSINESS_TABLES
DOMAIN_RULES = RULES
DOMAIN_PARAMETERS = tuple(PARAMETER_SPECS)
DOMAIN_EVENTS = EMITTED_EVENT_TYPES
DOMAIN_CONSUMED_EVENTS = CONSUMED_EVENT_TYPES
DOMAIN_ADVANCED_CAPABILITIES = ADVANCED_CAPABILITIES
DOMAIN_WORKBENCH_VIEWS = WORKBENCH_SECTIONS
DOMAIN_EDGE_CASES = (
    "invalid_plant_mode_transition",
    "sample_missing_chain_of_custody",
    "pressure_loss_requires_boil_water_review",
    "lift_station_overflow_threshold_crossed",
    "lab_result_requires_resample",
    "hydrant_follow_up_required",
    "scada_projection_stale",
    "agent_mutation_missing_confirmation",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        DOMAIN_ADVANCED_CAPABILITIES
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + (
            "specialist_sample_interpretation",
            "specialist_incident_narration",
            "specialist_asset_isolation",
            "specialist_scada_projection_review",
        )
    )
)


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
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "ui_fragments": UI_FRAGMENTS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 20,
        "minimum_domain_operations": 15,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    return preview_domain_operation(operation, payload)


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(preview_domain_operation(operation, {"tenant": "tenant-smoke"}) for operation in DOMAIN_OPERATIONS[:6])
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


def domain_capability_surface_contract() -> dict:
    operation_surfaces = tuple(
        {
            "operation": operation,
            "surface": f"{PBC_KEY}.ui.operation.{operation}",
            "action": operation,
            "target_table": preview_domain_operation(operation, {})["target_table"],
            "permission": f"{PBC_KEY}.operate",
            "requires_confirmation": True,
            "agent_tool": f"{PBC_KEY}_skills.{operation}",
            "event": preview_domain_operation(operation, {})["emitted_event"],
        }
        for operation in DOMAIN_OPERATIONS
    )
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": operation_surfaces,
        "rule_surfaces": tuple(
            {"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True}
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": name,
                "surface": f"{PBC_KEY}.ui.parameter.{name}",
                "bounded": True,
                "editable": True,
            }
            for name in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{index}",
                "explainable": True,
            }
            for index, capability in enumerate(DOMAIN_ADVANCED_CAPABILITIES, start=1)
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
            {"owned_table": table, "surface": f"{PBC_KEY}.ui.table.{table}", "read_model": True, "mutation_guard": True}
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
