"""UI contract for the Asset Lifecycle PBC."""

from __future__ import annotations

from .runtime import ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
from .runtime import ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES
from .runtime import ASSET_LIFECYCLE_EMITTED_EVENT_TYPES
from .runtime import ASSET_LIFECYCLE_OWNED_TABLES
from .runtime import ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
from .runtime import asset_lifecycle_permissions_contract


ASSET_LIFECYCLE_UI_FRAGMENT_KEYS = (
    "AssetLifecycleWorkbench",
    "AssetRegisterConsole",
    "CapitalizationQueue",
    "PlacedInServiceBoard",
    "DepreciationScheduleView",
    "DepreciationRunConsole",
    "DepreciationRevisionConsole",
    "AssetTransferBoard",
    "RevaluationImpairmentPanel",
    "MaintenanceAdjustmentView",
    "InsuranceWarrantyPanel",
    "PhysicalVerificationConsole",
    "AssetRetirementConsole",
    "AssetRiskPanel",
    "AssetRuleStudio",
    "AssetParameterConsole",
    "AssetConfigurationPanel",
)


def asset_lifecycle_ui_contract() -> dict:
    return {
        "format": "appgen.asset-lifecycle-ui-contract.v1",
        "ok": True,
        "pbc": "asset_lifecycle",
        "implementation_directory": "src/pyAppGen/pbcs/asset_lifecycle",
        "fragments": ASSET_LIFECYCLE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/asset_lifecycle",
            "/workbench/pbcs/asset_lifecycle/register",
            "/workbench/pbcs/asset_lifecycle/capitalization",
            "/workbench/pbcs/asset_lifecycle/service",
            "/workbench/pbcs/asset_lifecycle/depreciation-schedules",
            "/workbench/pbcs/asset_lifecycle/depreciation-runs",
            "/workbench/pbcs/asset_lifecycle/depreciation-revisions",
            "/workbench/pbcs/asset_lifecycle/transfers",
            "/workbench/pbcs/asset_lifecycle/valuations",
            "/workbench/pbcs/asset_lifecycle/maintenance",
            "/workbench/pbcs/asset_lifecycle/insurance",
            "/workbench/pbcs/asset_lifecycle/verification",
            "/workbench/pbcs/asset_lifecycle/retirement",
            "/workbench/pbcs/asset_lifecycle/risk",
            "/workbench/pbcs/asset_lifecycle/rules",
            "/workbench/pbcs/asset_lifecycle/parameters",
            "/workbench/pbcs/asset_lifecycle/configuration",
        ),
        "panels": (
            {
                "key": "register",
                "fragment": "AssetRegisterConsole",
                "binds_to": ("asset", "asset_graph", "identity"),
                "commands": ("register_asset", "parse_capitalization_document", "verify_asset_identity"),
            },
            {
                "key": "depreciation",
                "fragment": "DepreciationRunConsole",
                "binds_to": ("schedule", "depreciation_run", "outbox"),
                "commands": ("build_depreciation_schedule", "run_depreciation", "route_depreciation_journal"),
            },
            {
                "key": "depreciation_revision",
                "fragment": "DepreciationRevisionConsole",
                "binds_to": ("schedule_versions", "revision_flag", "idempotency"),
                "commands": ("build_depreciation_schedule", "review_depreciation_plan"),
            },
            {
                "key": "valuation",
                "fragment": "RevaluationImpairmentPanel",
                "binds_to": ("asset", "revaluation", "impairment", "valuation_projection"),
                "commands": ("revalue_asset", "impair_asset", "project_asset_valuation", "recommend_impairment"),
            },
            {
                "key": "operations",
                "fragment": "AssetTransferBoard",
                "binds_to": ("asset", "location", "custodian", "cost_center"),
                "commands": ("transfer_asset", "record_maintenance_adjustment", "retire_asset"),
            },
            {
                "key": "governance",
                "fragment": "AssetRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "register_asset": "asset_lifecycle.register",
            "place_asset_in_service": "asset_lifecycle.service",
            "build_depreciation_schedule": "asset_lifecycle.depreciation",
            "run_depreciation": "asset_lifecycle.depreciation",
            "review_depreciation_plan": "asset_lifecycle.depreciation",
            "transfer_asset": "asset_lifecycle.transfer",
            "revalue_asset": "asset_lifecycle.valuation",
            "impair_asset": "asset_lifecycle.valuation",
            "record_maintenance_adjustment": "asset_lifecycle.maintenance",
            "retire_asset": "asset_lifecycle.retirement",
            "generate_asset_audit_proof": "asset_lifecycle.audit",
            "register_rule": "asset_lifecycle.configure",
            "set_parameter": "asset_lifecycle.configure",
            "configure_runtime": "asset_lifecycle.configure",
            "run_control_tests": "asset_lifecycle.audit",
            "receive_event": "asset_lifecycle.event",
            "register_schema_extension": "asset_lifecycle.configure",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "fixed_event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "capitalization_threshold",
                "impairment_indicator_threshold",
                "physical_verification_interval_days",
                "depreciation_batch_size",
                "retirement_approval_limit",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("capitalization", "depreciation", "transfer", "valuation", "retirement", "verification", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": ASSET_LIFECYCLE_EMITTED_EVENT_TYPES,
            "consumes": ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
            "outbox_table": "asset_lifecycle_appgen_outbox_event",
            "inbox_table": "asset_lifecycle_appgen_inbox_event",
            "dead_letter_table": "asset_lifecycle_dead_letter_event",
            "permissions": asset_lifecycle_permissions_contract()["action_permissions"],
            "configuration": {
                "event_contract": "AppGen-X",
                "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
                "allowed_database_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
                "stream_engine_picker_visible": False,
            },
        },
    }


def asset_lifecycle_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = asset_lifecycle_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    assets = tuple(asset for asset in state["assets"].values() if asset["tenant"] == tenant)
    schedules = tuple(schedule for schedule in state["schedules"].values() if state["assets"].get(schedule["asset_id"], {}).get("tenant") == tenant)
    depreciation_runs = tuple(state["depreciation_runs"].values())
    cards = (
        {"key": "assets", "value": len(assets), "fragment": "AssetRegisterConsole"},
        {"key": "in_service", "value": len(tuple(asset for asset in assets if asset["status"] == "in_service")), "fragment": "PlacedInServiceBoard"},
        {"key": "retired", "value": len(tuple(asset for asset in assets if asset["status"] == "retired")), "fragment": "AssetRetirementConsole"},
        {"key": "net_book_value", "value": round(sum(asset["book_value"] for asset in assets), 2), "fragment": "AssetLifecycleWorkbench"},
        {"key": "schedules", "value": len(schedules), "fragment": "DepreciationScheduleView"},
        {"key": "depreciation_runs", "value": len(depreciation_runs), "fragment": "DepreciationRunConsole"},
        {"key": "pending_schedule_revisions", "value": len(tuple(asset for asset in assets if asset.get("schedule_revision_required"))), "fragment": "DepreciationRevisionConsole"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "AssetRuleStudio"},
    )
    return {
        "format": "appgen.asset-lifecycle-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/asset_lifecycle",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", {})),
        "dead_letter_count": len(state.get("dead_letters", ())),
        "binding_evidence": contract["workbench_binding_evidence"],
        "depreciation_controls": {
            "pending_schedule_revisions": len(tuple(asset for asset in assets if asset.get("schedule_revision_required"))),
            "active_schedule_versions": {
                asset["asset_id"]: asset.get("active_schedule_version", 0)
                for asset in assets
                if asset.get("active_schedule_id")
            },
            "idempotency_keys": tuple(sorted(state.get("depreciation_run_index", {}))),
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
    contract = asset_lifecycle_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = asset_lifecycle_render_workbench(
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



def asset_lifecycle_form_contracts() -> dict:
    contracts=(
        {'key':'AssetConfigurationForm','operation':'configure_runtime','table':'asset_lifecycle_asset_configuration','fields':('database_backend','event_topic','retry_limit','default_currency','default_timezone','default_book'),'permission':'asset_lifecycle.configure','keywords':('configure','book','currency')},
        {'key':'AssetRegisterForm','operation':'register_asset','table':'asset_lifecycle_fixed_asset','fields':('asset_id','tenant','legal_entity','description','category','cost','residual_value','useful_life_months','book','location','custodian','cost_center','components'),'permission':'asset_lifecycle.register','keywords':('asset','capitalization','register')},
        {'key':'PlaceInServiceForm','operation':'place_asset_in_service','table':'asset_lifecycle_fixed_asset','fields':('asset_id','service_date'),'permission':'asset_lifecycle.service','keywords':('service','placed in service','in service')},
        {'key':'DepreciationScheduleForm','operation':'build_depreciation_schedule','table':'asset_lifecycle_asset_depreciation_schedule','fields':('asset_id','method'),'permission':'asset_lifecycle.depreciation','keywords':('schedule','depreciation','method')},
        {'key':'DepreciationRunForm','operation':'run_depreciation','table':'asset_lifecycle_asset_depreciation_run','fields':('run_id','period'),'permission':'asset_lifecycle.depreciation','keywords':('run','post depreciation','period')},
        {'key':'AssetTransferForm','operation':'transfer_asset','table':'asset_lifecycle_asset_transfer','fields':('asset_id','location','cost_center','approved_by'),'permission':'asset_lifecycle.transfer','keywords':('transfer','location','cost center')},
        {'key':'ValuationForm','operation':'revalue_asset','table':'asset_lifecycle_asset_valuation_adjustment','fields':('asset_id','fair_value','recoverable_amount','approved_by'),'permission':'asset_lifecycle.valuation','keywords':('revalue','impair','valuation')},
        {'key':'MaintenanceAdjustmentForm','operation':'record_maintenance_adjustment','table':'asset_lifecycle_asset_maintenance_adjustment','fields':('asset_id','useful_life_delta_months','evidence'),'permission':'asset_lifecycle.maintenance','keywords':('maintenance','life extension','adjustment')},
    )
    return {'format':'appgen.asset-lifecycle-standalone-forms.v1','ok':all(i['table'].startswith('asset_lifecycle_') for i in contracts),'pbc':'asset_lifecycle','contracts':contracts,'side_effects':()}

def asset_lifecycle_wizard_contracts() -> dict:
    contracts=(
        {'key':'AssetCapitalizationWizard','steps':('parse_capitalization_packet','register_asset','validate_threshold','preview_owned_record'),'forms':('AssetRegisterForm',),'keywords':('document','capitalization','asset','receipt')},
        {'key':'PlaceInServiceWizard','steps':('validate_service_date','place_in_service','emit_appgen_event'),'forms':('PlaceInServiceForm',),'keywords':('service','in service')},
        {'key':'DepreciationScheduleWizard','steps':('build_schedule','review_revision','store_schedule_version'),'forms':('DepreciationScheduleForm',),'keywords':('schedule','revision','depreciation')},
        {'key':'DepreciationRunWizard','steps':('select_due_lines','post_run','emit_journal_event','record_idempotency'),'forms':('DepreciationRunForm',),'keywords':('run','post','journal','period')},
        {'key':'AssetTransferWizard','steps':('validate_policy','update_location_cost_center','emit_transfer_event'),'forms':('AssetTransferForm',),'keywords':('transfer','location')},
        {'key':'AssetAuditProofWizard','steps':('run_controls','select_disclosure','generate_zero_knowledge_proof'),'forms':('AssetRegisterForm',),'keywords':('audit','proof','control')},
    )
    return {'format':'appgen.asset-lifecycle-standalone-wizards.v1','ok':all(i['steps'] for i in contracts),'pbc':'asset_lifecycle','contracts':contracts,'side_effects':()}

def asset_lifecycle_control_catalog() -> dict:
    contracts=(
        {'key':'asset_backend_event_contract','operation':'run_control_tests','table':'asset_lifecycle_asset_control_assertion','permission':'asset_lifecycle.audit'},
        {'key':'depreciation_idempotency_control','operation':'run_control_tests','table':'asset_lifecycle_asset_depreciation_run','permission':'asset_lifecycle.audit'},
        {'key':'asset_audit_proof_control','operation':'generate_asset_audit_proof','table':'asset_lifecycle_asset_audit_proof','permission':'asset_lifecycle.audit'},
    )
    return {'format':'appgen.asset-lifecycle-standalone-controls.v1','ok':all(i['table'].startswith('asset_lifecycle_') for i in contracts),'pbc':'asset_lifecycle','contracts':contracts,'side_effects':()}

def asset_lifecycle_standalone_workbench_blueprint() -> dict:
    forms=asset_lifecycle_form_contracts(); wizards=asset_lifecycle_wizard_contracts(); controls=asset_lifecycle_control_catalog()
    return {'format':'appgen.asset-lifecycle-standalone-workbench.v1','ok':forms['ok'] and wizards['ok'] and controls['ok'],'pbc':'asset_lifecycle','forms':forms['contracts'],'wizards':wizards['contracts'],'controls':controls['contracts'],'panels':asset_lifecycle_ui_contract()['panels'],'side_effects':()}

def asset_lifecycle_render_standalone_workbench(workbench: dict) -> dict:
    bp=asset_lifecycle_standalone_workbench_blueprint(); cards=(
        {'key':'assets','value':workbench.get('asset_count',0),'fragment':'AssetRegisterConsole'},
        {'key':'in_service','value':workbench.get('in_service_count',0),'fragment':'PlacedInServiceBoard'},
        {'key':'retired','value':workbench.get('retired_count',0),'fragment':'AssetRetirementConsole'},
        {'key':'net_book_value','value':workbench.get('net_book_value',0),'fragment':'AssetLifecycleWorkbench'},
        {'key':'pending_schedule_revisions','value':workbench.get('pending_schedule_revisions',0),'fragment':'DepreciationRevisionConsole'},)
    return {'format':'appgen.asset-lifecycle-standalone-render.v1','ok':bp['ok'] and bool(cards),'pbc':'asset_lifecycle','tenant':workbench.get('tenant'),'cards':cards,'forms':tuple(i['key'] for i in bp['forms']),'wizards':tuple(i['key'] for i in bp['wizards']),'controls':tuple(i['key'] for i in bp['controls']),'side_effects':()}
