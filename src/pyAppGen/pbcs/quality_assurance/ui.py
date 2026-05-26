"""UI contract for the Quality Assurance PBC."""

from __future__ import annotations

from .runtime import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
from .runtime import QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_OWNED_TABLES
from .runtime import QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS
from .runtime import QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
from .runtime import QUALITY_ASSURANCE_RUNTIME_TABLES
from .runtime import QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS
from .runtime import QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES
from .runtime import QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES
from .runtime import quality_assurance_binding_evidence
from .runtime import quality_assurance_permissions_contract
from .runtime import quality_assurance_ui_binding_contract

QUALITY_ASSURANCE_UI_FRAGMENT_KEYS = (
    "QualityAssuranceWorkbench",
    "InspectionPlanConsole",
    "InspectionResultCapture",
    "SamplingWorkbench",
    "SpcDashboard",
    "QualityHoldBoard",
    "NonConformanceBoard",
    "CapaConsole",
    "CalibrationConsole",
    "ProcedureLibrary",
    "SupplierQualityDesk",
    "CustomerQualityDesk",
    "AuditEvidenceViewer",
    "QualityRuleStudio",
    "QualityParameterConsole",
    "QualityConfigurationPanel",
    "ReleaseEvidencePanel",
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
            "/workbench/pbcs/quality_assurance/sampling",
            "/workbench/pbcs/quality_assurance/spc",
            "/workbench/pbcs/quality_assurance/holds",
            "/workbench/pbcs/quality_assurance/non-conformances",
            "/workbench/pbcs/quality_assurance/capa",
            "/workbench/pbcs/quality_assurance/calibration",
            "/workbench/pbcs/quality_assurance/procedures",
            "/workbench/pbcs/quality_assurance/supplier-quality",
            "/workbench/pbcs/quality_assurance/customer-quality",
            "/workbench/pbcs/quality_assurance/audit-evidence",
            "/workbench/pbcs/quality_assurance/rules",
            "/workbench/pbcs/quality_assurance/parameters",
            "/workbench/pbcs/quality_assurance/configuration",
            "/workbench/pbcs/quality_assurance/release-evidence",
        ),
        "panels": (
            {
                "key": "inspection_plans",
                "fragment": "InspectionPlanConsole",
                "binds_to": ("inspection_plan", "sampling_scheme", "lot_batch_profile", "inspection_test_definition", "inspection_result", "production_completion_projection", "goods_receipt_projection"),
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
                "binds_to": ("non_conformance", "quality_capa", "quality_release", "inspection_result"),
                "commands": ("raise_nonconformance", "disposition_nonconformance"),
            },
            {
                "key": "metrology",
                "fragment": "CalibrationConsole",
                "binds_to": ("calibration_asset", "calibration_schedule", "procedure_revision"),
                "commands": ("run_control_tests",),
            },
            {
                "key": "partner_quality",
                "fragment": "SupplierQualityDesk",
                "binds_to": ("supplier_quality_profile", "supplier_quality_incident", "customer_quality_case", "audit_evidence_packet"),
                "commands": ("build_release_evidence",),
            },
            {
                "key": "governance_studio",
                "fragment": "QualityRuleStudio",
                "binds_to": ("quality_rule", "quality_parameter", "quality_configuration", "quality_schema_extension", "quality_governed_model", "quality_control_assertion"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "build_schema_contract", "build_service_contract", "build_release_evidence", "run_control_tests"),
            },
        ),
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "runtime_tables": {
            "outbox": QUALITY_ASSURANCE_RUNTIME_TABLES[0],
            "inbox": QUALITY_ASSURANCE_RUNTIME_TABLES[1],
            "dead_letter": QUALITY_ASSURANCE_RUNTIME_TABLES[2],
        },
        "action_permissions": permissions,
        "configuration_editor": {
            "required_fields": QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS,
            "supported_fields": QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS,
            "allowed_database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
            "event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
            "visible_event_contracts": ("AppGen-X",),
            "stream_engine_picker_visible": False,
            "user_eventing_choice_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES,
            "supported_parameters": QUALITY_ASSURANCE_SUPPORTED_PARAMETER_NAMES,
        },
        "rule_editor": {
            "rule_types": tuple(rule_type for rule_type in QUALITY_ASSURANCE_SUPPORTED_RULE_TYPES if rule_type != "quality"),
            "legacy_rule_type_aliases": ("quality",),
            "required_fields": QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS,
            "compiled_evidence_fields": ("compiled_hash", "compile_evidence"),
        },
        "event_surfaces": {
            "emits": QUALITY_ASSURANCE_EMITTED_EVENT_TYPES,
            "consumes": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
            "required_event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "stream_engine_picker_visible": False,
        },
        "binding_evidence": quality_assurance_ui_binding_contract()["binding_evidence"],
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
        {"key": "dead_letters", "value": len(state.get("dead_letters", ())), "fragment": "AuditEvidenceViewer"},
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
                "audit_fragment": "AuditEvidenceViewer",
                "release_fragment": "ReleaseEvidencePanel",
                "outbox_table": QUALITY_ASSURANCE_RUNTIME_TABLES[0],
                "inbox_table": QUALITY_ASSURANCE_RUNTIME_TABLES[1],
                "dead_letter_table": QUALITY_ASSURANCE_RUNTIME_TABLES[2],
                "rbac": contract["action_permissions"],
            },
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = quality_assurance_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = quality_assurance_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
