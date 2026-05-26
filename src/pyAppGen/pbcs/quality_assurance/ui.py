"""UI contract for the Quality Assurance PBC."""

from __future__ import annotations

from .runtime import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
from .runtime import QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS
from .runtime import QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS
from .runtime import QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES
from .runtime import QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES
from .runtime import quality_assurance_binding_evidence

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
                "binds_to": ("inspection_plan", "inspection_result"),
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
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": {
            "create_inspection_plan": "quality_assurance.inspect",
            "record_inspection_result": "quality_assurance.inspect",
            "create_quality_hold": "quality_assurance.hold",
            "release_quality_hold": "quality_assurance.hold",
            "raise_nonconformance": "quality_assurance.disposition",
            "disposition_nonconformance": "quality_assurance.disposition",
            "register_rule": "quality_assurance.configure",
            "set_parameter": "quality_assurance.configure",
            "configure_runtime": "quality_assurance.configure",
            "run_control_tests": "quality_assurance.audit",
        },
        "configuration_editor": {
            "required_fields": QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS,
            "supported_fields": QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS,
            "allowed_database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
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
            "emits": ("QualityHoldReleased", "NonConformanceRaised"),
            "consumes": ("ProductionCompleted", "GoodsReceiptPosted"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
        "binding_evidence": {
            **binding_evidence,
            "ui_bindings": {
                "configuration_fragment": "QualityConfigurationPanel",
                "rule_fragment": "QualityRuleStudio",
                "parameter_fragment": "QualityParameterConsole",
            },
        },
    }
