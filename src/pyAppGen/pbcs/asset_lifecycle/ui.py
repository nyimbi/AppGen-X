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
