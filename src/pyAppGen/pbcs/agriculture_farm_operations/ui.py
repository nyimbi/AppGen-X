"""UI contract and standalone workbench surface for agriculture_farm_operations."""

from __future__ import annotations

from .permissions import permission_manifest
from .runtime import (
    AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES,
    AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES,
    AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES,
    AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
    AGRICULTURE_FARM_OPERATIONS_RUNTIME_TABLES,
    agriculture_farm_operations_build_workbench_view,
    agriculture_farm_operations_command_field,
    agriculture_farm_operations_empty_state,
    agriculture_farm_operations_query_workbench,
    agriculture_farm_operations_record_crop_plan,
    agriculture_farm_operations_workflow_catalog,
)
from .crop_planning import PLANTING_WINDOW_STATUSES

PBC_KEY = "agriculture_farm_operations"
AGRICULTURE_FARM_OPERATIONS_UI_FRAGMENT_KEYS = (
    "AgricultureFarmOperationsWorkbench",
    "AgricultureFarmOperationsDetail",
    "AgricultureFarmOperationsAssistantPanel",
)
AGRICULTURE_FARM_OPERATIONS_FORM_KEYS = (
    "field_setup_form",
    "crop_plan_form",
    "blocked_operation_resolution_form",
    "document_instruction_form",
)
AGRICULTURE_FARM_OPERATIONS_WIZARD_KEYS = (
    "field_onboarding_wizard",
    "seasonal_crop_plan_wizard",
    "exception_recovery_wizard",
)
AGRICULTURE_FARM_OPERATIONS_CONTROL_KEYS = (
    "tenant_scope_picker",
    "season_timeline",
    "window_status_chips",
    "blocked_operations_board",
    "assistant_recommendation_panel",
)


def agriculture_farm_operations_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "field_setup_form",
            "title": "Field Setup",
            "command": "command_field",
            "fields": ("field_id", "tenant", "code", "name", "region", "acreage", "management_zones"),
        },
        {
            "key": "crop_plan_form",
            "title": "Seasonal Crop Plan",
            "command": "record_crop_plan",
            "fields": (
                "plan_id",
                "tenant",
                "field_id",
                "management_zone",
                "crop",
                "season",
                "market_year",
                "planting_date",
            ),
        },
        {
            "key": "blocked_operation_resolution_form",
            "title": "Blocked Operation Resolution",
            "command": "record_crop_plan",
            "fields": ("plan_id", "owner", "reason_codes", "override_note"),
        },
        {
            "key": "document_instruction_form",
            "title": "Document to Draft",
            "command": "parse_document_instruction",
            "fields": ("document", "instruction", "context"),
        },
    )


def agriculture_farm_operations_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "field_onboarding_wizard",
            "steps": ("field_setup_form",),
            "goal": "Create a farm field with region and management-zone context.",
        },
        {
            "key": "seasonal_crop_plan_wizard",
            "steps": ("field_setup_form", "crop_plan_form", "document_instruction_form"),
            "goal": "Build one season-aware crop plan with assistant-ready evidence.",
        },
        {
            "key": "exception_recovery_wizard",
            "steps": ("blocked_operation_resolution_form", "crop_plan_form"),
            "goal": "Resolve blocked planning exceptions and resubmit safely.",
        },
    )


def agriculture_farm_operations_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "season_timeline", "type": "timeline", "binds_to": "crop_plans"},
        {"key": "window_status_chips", "type": "status_group", "binds_to": "planting_window.status"},
        {"key": "blocked_operations_board", "type": "queue", "binds_to": "planning_exceptions"},
        {"key": "assistant_recommendation_panel", "type": "panel", "binds_to": "assistant_plans"},
    )


def agriculture_farm_operations_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_id": "agriculture_farm_operations_one_pbc_app",
        "workbench_route": "/workbench/pbcs/agriculture_farm_operations",
        "navigation": (
            {"key": "overview", "route": "/workbench/pbcs/agriculture_farm_operations"},
            {"key": "fields", "route": "/workbench/pbcs/agriculture_farm_operations/fields"},
            {"key": "crop-plans", "route": "/workbench/pbcs/agriculture_farm_operations/crop-plans"},
            {"key": "exceptions", "route": "/workbench/pbcs/agriculture_farm_operations/exceptions"},
            {"key": "assistant", "route": "/workbench/pbcs/agriculture_farm_operations/assistant"},
            {"key": "release", "route": "/workbench/pbcs/agriculture_farm_operations/release"},
        ),
        "forms": AGRICULTURE_FARM_OPERATIONS_FORM_KEYS,
        "wizards": AGRICULTURE_FARM_OPERATIONS_WIZARD_KEYS,
        "controls": AGRICULTURE_FARM_OPERATIONS_CONTROL_KEYS,
        "single_agent_namespace": "agriculture_farm_operations_skills",
        "side_effects": (),
    }


def agriculture_farm_operations_ui_contract() -> dict:
    permissions = permission_manifest()
    return {
        "format": "appgen.agriculture-farm-operations-ui-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/agriculture_farm_operations",
        "fragments": AGRICULTURE_FARM_OPERATIONS_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in agriculture_farm_operations_standalone_app_contract()["navigation"]),
        "panels": (
            {
                "key": "fields",
                "fragment": "AgricultureFarmOperationsWorkbench",
                "binds_to": ("agriculture_farm_operations_field",),
                "commands": ("command_field",),
            },
            {
                "key": "crop_plans",
                "fragment": "AgricultureFarmOperationsDetail",
                "binds_to": ("agriculture_farm_operations_crop_plan",),
                "commands": ("record_crop_plan", "run_advanced_assessment"),
            },
            {
                "key": "assistant",
                "fragment": "AgricultureFarmOperationsAssistantPanel",
                "binds_to": (
                    "agriculture_farm_operations_crop_plan",
                    "agriculture_farm_operations_agriculture_farm_operations_governed_model",
                ),
                "commands": ("parse_document_instruction",),
            },
        ),
        "forms": agriculture_farm_operations_form_catalog(),
        "wizards": agriculture_farm_operations_wizard_catalog(),
        "controls": agriculture_farm_operations_control_catalog(),
        "standalone_app": agriculture_farm_operations_standalone_app_contract(),
        "action_permissions": permissions["action_permissions"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_region",
                "calendar_profile",
                "workbench_limit",
            ),
            "allowed_database_backends": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "bounded_supported_parameters": True,
            "planning_window_statuses": PLANTING_WINDOW_STATUSES,
        },
        "rule_editor": {
            "rule_types": (
                "field_policy",
                "crop_plan_policy",
                "exception_triage_policy",
            ),
            "compiled_evidence_required": True,
        },
        "workflow_catalog": agriculture_farm_operations_workflow_catalog(),
        "event_surfaces": {
            "emits": AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES,
            "consumes": AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES,
            "runtime_tables": AGRICULTURE_FARM_OPERATIONS_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
        },
        "side_effects": (),
    }


def agriculture_farm_operations_render_workbench(
    state: dict | None = None,
    *,
    tenant: str = "default",
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    state = state or agriculture_farm_operations_empty_state()
    contract = agriculture_farm_operations_ui_contract()
    shell = agriculture_farm_operations_standalone_app_contract()
    snapshot = agriculture_farm_operations_query_workbench(state, {"tenant": tenant})
    permissions = set(principal_permissions or tuple(sorted(set(contract["action_permissions"].values()))))
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.agriculture-farm-operations-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": snapshot["cards"],
        "workflows": snapshot["workflows"],
        "alerts": snapshot["crop_plan_summary"]["alerts"],
        "exception_queue": snapshot["planning_exceptions"],
        "assistant_plans": snapshot["assistant_plans"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "shell": shell,
        "workbench": snapshot,
        "binding_evidence": contract["binding_evidence"],
        "side_effects": (),
    }


def agriculture_farm_operations_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    workbench = agriculture_farm_operations_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=principal_permissions,
    )
    return {
        "ok": workbench["ok"],
        "pbc": PBC_KEY,
        "shell": agriculture_farm_operations_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


def smoke_test() -> dict:
    state = agriculture_farm_operations_empty_state()
    field = agriculture_farm_operations_command_field(
        state,
        {
            "tenant": "tenant-ui-smoke",
            "field_id": "field-ui-smoke",
            "code": "FIELD-UI",
            "name": "UI Smoke Field",
        },
    )
    crop_plan = agriculture_farm_operations_record_crop_plan(
        field["state"],
        {
            "tenant": "tenant-ui-smoke",
            "field_id": "field-ui-smoke",
            "crop": "maize",
            "season": "long_rains",
            "market_year": 2026,
            "planting_date": "2026-04-24",
            "planting_window": {
                "start": "2026-04-10",
                "optimal_start": "2026-04-20",
                "optimal_end": "2026-05-05",
                "latest": "2026-05-15",
            },
            "readiness": {
                "soil_fit": True,
                "fertility_ready": True,
                "equipment_ready": True,
                "crew_assigned": True,
            },
        },
    )
    rendered = agriculture_farm_operations_render_workbench(crop_plan["state"], tenant="tenant-ui-smoke")
    return {
        "ok": agriculture_farm_operations_ui_contract()["ok"] and rendered["ok"] and bool(rendered["cards"]),
        "manifest": {"fragments": agriculture_farm_operations_ui_contract()["fragments"]},
        "rendered": rendered,
        "side_effects": (),
    }
