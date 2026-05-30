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



def quality_assurance_form_contracts() -> dict:
    contracts = (
        {'key': 'QualityConfigurationForm', 'operation': 'configure_runtime', 'table': 'quality_assurance_quality_configuration', 'fields': QUALITY_ASSURANCE_REQUIRED_CONFIGURATION_FIELDS, 'permission': 'quality_assurance.configure', 'keywords': ('configure', 'event topic', 'backend')},
        {'key': 'QualityRuleForm', 'operation': 'register_rule', 'table': 'quality_assurance_quality_rule', 'fields': QUALITY_ASSURANCE_REQUIRED_RULE_FIELDS, 'permission': 'quality_assurance.configure', 'keywords': ('rule', 'sampling', 'release')},
        {'key': 'InspectionPlanForm', 'operation': 'create_inspection_plan', 'table': 'quality_assurance_inspection_plan', 'fields': ('plan_id', 'tenant', 'item', 'site', 'source', 'sampling_method', 'sample_size', 'revision', 'status'), 'permission': 'quality_assurance.configure', 'keywords': ('plan', 'inspection', 'sampling')},
        {'key': 'InspectionResultForm', 'operation': 'record_inspection_result', 'table': 'quality_assurance_inspection_result', 'fields': ('result_id', 'tenant', 'plan_id', 'lot_id', 'order_id', 'measurements', 'defects', 'inspector'), 'permission': 'quality_assurance.execute', 'keywords': ('result', 'measurement', 'defect', 'spc')},
        {'key': 'QualityHoldForm', 'operation': 'create_quality_hold', 'table': 'quality_assurance_quality_hold', 'fields': ('hold_id', 'tenant', 'item', 'lot_id', 'site', 'reason', 'severity'), 'permission': 'quality_assurance.execute', 'keywords': ('hold', 'lot isolation', 'defect')},
        {'key': 'NonConformanceForm', 'operation': 'raise_nonconformance', 'table': 'quality_assurance_non_conformance', 'fields': ('nonconformance_id', 'tenant', 'result_id', 'defect_class', 'severity', 'root_cause'), 'permission': 'quality_assurance.execute', 'keywords': ('nonconformance', 'capa', 'root cause')},
    )
    return {'format': 'appgen.quality-assurance-standalone-forms.v1', 'ok': all(item['table'].startswith('quality_assurance_') for item in contracts), 'pbc': 'quality_assurance', 'contracts': contracts, 'side_effects': ()}


def quality_assurance_wizard_contracts() -> dict:
    contracts = (
        {'key': 'InspectionLotIntakeWizard', 'steps': ('parse_document', 'create_plan', 'record_result', 'evaluate_spc', 'preview_mutation'), 'forms': ('InspectionPlanForm', 'InspectionResultForm'), 'keywords': ('document', 'certificate', 'inspection', 'lot')},
        {'key': 'NonConformanceDispositionWizard', 'steps': ('raise_nonconformance', 'classify_defect', 'assign_capa', 'approve_disposition'), 'forms': ('NonConformanceForm',), 'keywords': ('nonconformance', 'defect', 'root cause', 'disposition')},
        {'key': 'HoldReleaseWizard', 'steps': ('create_hold', 'run_controls', 'generate_quality_proof', 'release_hold'), 'forms': ('QualityHoldForm',), 'keywords': ('hold', 'release', 'proof', 'control')},
    )
    return {'format': 'appgen.quality-assurance-standalone-wizards.v1', 'ok': all(item['steps'] for item in contracts), 'pbc': 'quality_assurance', 'contracts': contracts, 'side_effects': ()}


def quality_assurance_control_catalog() -> dict:
    contracts = (
        {'key': 'quality_backend_event_contract', 'operation': 'run_control_tests', 'table': 'quality_assurance_quality_control_assertion', 'permission': 'quality_assurance.audit'},
        {'key': 'quality_spc_release_control', 'operation': 'run_control_tests', 'table': 'quality_assurance_quality_control_assertion', 'permission': 'quality_assurance.audit'},
        {'key': 'quality_proof_control', 'operation': 'generate_quality_proof', 'table': 'quality_assurance_audit_evidence_packet', 'permission': 'quality_assurance.audit'},
    )
    return {'format': 'appgen.quality-assurance-standalone-controls.v1', 'ok': all(item['table'].startswith('quality_assurance_') for item in contracts), 'pbc': 'quality_assurance', 'contracts': contracts, 'side_effects': ()}


def quality_assurance_standalone_workbench_blueprint() -> dict:
    forms = quality_assurance_form_contracts()
    wizards = quality_assurance_wizard_contracts()
    controls = quality_assurance_control_catalog()
    return {'format': 'appgen.quality-assurance-standalone-workbench.v1', 'ok': forms['ok'] and wizards['ok'] and controls['ok'], 'pbc': 'quality_assurance', 'forms': forms['contracts'], 'wizards': wizards['contracts'], 'controls': controls['contracts'], 'panels': quality_assurance_ui_contract()['panels'], 'side_effects': ()}


def quality_assurance_render_standalone_workbench(workbench: dict) -> dict:
    blueprint = quality_assurance_standalone_workbench_blueprint()
    cards = (
        {'key': 'plans', 'value': workbench.get('plan_count', 0), 'fragment': 'InspectionPlanConsole'},
        {'key': 'results', 'value': workbench.get('result_count', 0), 'fragment': 'InspectionResultCapture'},
        {'key': 'holds', 'value': workbench.get('hold_count', 0), 'fragment': 'QualityHoldBoard'},
        {'key': 'nonconformances', 'value': workbench.get('nonconformance_count', workbench.get('open_nc_count', 0)), 'fragment': 'NonConformanceBoard'},
    )
    return {'format': 'appgen.quality-assurance-standalone-render.v1', 'ok': blueprint['ok'] and bool(cards), 'pbc': 'quality_assurance', 'tenant': workbench.get('tenant'), 'cards': cards, 'forms': tuple(item['key'] for item in blueprint['forms']), 'wizards': tuple(item['key'] for item in blueprint['wizards']), 'controls': tuple(item['key'] for item in blueprint['controls']), 'side_effects': ()}
