"""UI contract for the Quality Assurance PBC."""

from __future__ import annotations

from .runtime import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
from .runtime import QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_OWNED_TABLES
from .runtime import QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS
from .runtime import QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
from .runtime import QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS
from .runtime import QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES
from .runtime import QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES
from .runtime import quality_assurance_binding_evidence
from .runtime import quality_assurance_permissions_contract

QUALITY_ASSURANCE_UI_FRAGMENT_KEYS = (
    "QualityAssuranceWorkbench",
    "InspectionPlanConsole",
    "InspectionResultCapture",
    "SpcDashboard",
    "QualityHoldBoard",
    "NonConformanceBoard",
    "CapaConsole",
    "QualityRuleStudio",
    "QualityParameterConsole",
    "QualityConfigurationPanel",
)


def quality_assurance_ui_contract() -> dict:
    permissions = quality_assurance_permissions_contract()["action_permissions"]
    return {
        "format": "appgen.quality-assurance-ui-contract.v1",
        "ok": True,
        "pbc": "quality_assurance",
        "implementation_directory": "src/pyAppGen/pbcs/quality_assurance",
        "fragments": QUALITY_ASSURANCE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/quality_assurance",
            "/workbench/pbcs/quality_assurance/plans",
            "/workbench/pbcs/quality_assurance/results",
            "/workbench/pbcs/quality_assurance/spc",
            "/workbench/pbcs/quality_assurance/holds",
            "/workbench/pbcs/quality_assurance/non-conformances",
            "/workbench/pbcs/quality_assurance/capa",
            "/workbench/pbcs/quality_assurance/rules",
            "/workbench/pbcs/quality_assurance/parameters",
            "/workbench/pbcs/quality_assurance/configuration",
        ),
        "panels": (
            {
                "key": "inspection_plans",
                "fragment": "InspectionPlanConsole",
                "binds_to": ("inspection_plan", "inspection_result", "production_completion_projection", "goods_receipt_projection"),
                "commands": ("create_inspection_plan", "record_inspection_result"),
            },
            {
                "key": "holds",
                "fragment": "QualityHoldBoard",
                "binds_to": ("quality_hold", "inspection_result", "outbox"),
                "commands": ("create_quality_hold", "release_quality_hold"),
            },
            {
                "key": "nonconformances",
                "fragment": "NonConformanceBoard",
                "binds_to": ("non_conformance", "inspection_result"),
                "commands": ("raise_nonconformance", "disposition_nonconformance"),
            },
            {
                "key": "governance_studio",
                "fragment": "QualityRuleStudio",
                "binds_to": ("quality_rule", "quality_parameter", "quality_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "runtime_tables": {
            "outbox": "quality_assurance_appgen_outbox_event",
            "inbox": "quality_assurance_appgen_inbox_event",
            "dead_letter": "quality_assurance_dead_letter_event",
        },
        "action_permissions": permissions,
        "configuration_editor": {
            "required_fields": QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS,
            "supported_fields": QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS,
            "allowed_database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_eventing_choice_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES,
        },
        "rule_editor": {
            "rule_types": tuple(rule_type for rule_type in QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES if rule_type != "quality"),
            "legacy_rule_type_aliases": ("quality",),
            "required_fields": QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS,
        },
        "event_surfaces": {
            "emits": QUALITY_ASSURANCE_EMITTED_EVENT_TYPES,
            "consumes": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "stream_engine_picker_visible": False,
        },
    }


def quality_assurance_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = quality_assurance_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    plans = tuple(plan for plan in state["plans"].values() if plan["tenant"] == tenant)
    results = tuple(result for result in state["results"].values() if result["tenant"] == tenant)
    holds = tuple(hold for hold in state["holds"].values() if hold["tenant"] == tenant)
    ncs = tuple(nc for nc in state["nonconformances"].values() if nc["tenant"] == tenant)
    cards = (
        {"key": "inspection_plans", "value": len(plans), "fragment": "InspectionPlanConsole"},
        {"key": "inspection_results", "value": len(results), "fragment": "InspectionResultCapture"},
        {"key": "failed_inspections", "value": len(tuple(result for result in results if result["decision"] == "fail")), "fragment": "SpcDashboard"},
        {"key": "quality_holds", "value": len(holds), "fragment": "QualityHoldBoard"},
        {"key": "released_holds", "value": len(tuple(hold for hold in holds if hold["status"] == "released")), "fragment": "QualityHoldBoard"},
        {"key": "nonconformances", "value": len(ncs), "fragment": "NonConformanceBoard"},
    )
    binding_evidence = quality_assurance_binding_evidence(state)
    return {
        "format": "appgen.quality-assurance-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/quality_assurance",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letters", ())),
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "binding_evidence": {
            **binding_evidence,
            "ui_bindings": {
                "configuration_fragment": "QualityConfigurationPanel",
                "rule_fragment": "QualityRuleStudio",
                "parameter_fragment": "QualityParameterConsole",
                "outbox_table": "quality_assurance_appgen_outbox_event",
                "inbox_table": "quality_assurance_appgen_inbox_event",
                "dead_letter_table": "quality_assurance_dead_letter_event",
                "rbac": contract["action_permissions"],
            },
        },
    }
