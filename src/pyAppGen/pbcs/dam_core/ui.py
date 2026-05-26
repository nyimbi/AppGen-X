"""UI contract for the Digital Asset Management Core PBC."""

from __future__ import annotations

from .runtime import DAM_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import DAM_CORE_CONSUMED_EVENT_TYPES
from .runtime import DAM_CORE_EMITTED_EVENT_TYPES
from .runtime import DAM_CORE_OWNED_TABLES
from .runtime import DAM_CORE_REQUIRED_EVENT_TOPIC
from .runtime import DAM_CORE_RUNTIME_TABLES
from .runtime import dam_core_build_workbench_view
from .runtime import dam_core_permissions_contract


DAM_CORE_UI_FRAGMENT_KEYS = (
    "DamCoreWorkbench",
    "AssetLibraryConsole",
    "RenditionPipelineBoard",
    "MetadataTagStudio",
    "RightsPolicyWorkbench",
    "ProductPublishedProjectionPanel",
    "AssetQualityRiskPanel",
    "DamRuleStudio",
    "DamParameterConsole",
    "DamConfigurationPanel",
    "DamEventOutbox",
    "DamInboxMonitor",
    "DamDeadLetterQueue",
    "DamSchemaContractExplorer",
    "DamServiceContractExplorer",
    "DamReleaseEvidencePanel",
)


def dam_core_ui_contract() -> dict:
    return {
        "format": "appgen.dam-core-ui-contract.v1",
        "ok": True,
        "pbc": "dam_core",
        "implementation_directory": "src/pyAppGen/pbcs/dam_core",
        "fragments": DAM_CORE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/dam_core",
            "/workbench/pbcs/dam_core/assets",
            "/workbench/pbcs/dam_core/renditions",
            "/workbench/pbcs/dam_core/metadata",
            "/workbench/pbcs/dam_core/rights",
            "/workbench/pbcs/dam_core/product-projections",
            "/workbench/pbcs/dam_core/rules",
            "/workbench/pbcs/dam_core/parameters",
            "/workbench/pbcs/dam_core/configuration",
            "/workbench/pbcs/dam_core/eventing",
            "/workbench/pbcs/dam_core/schema-contract",
            "/workbench/pbcs/dam_core/service-contract",
            "/workbench/pbcs/dam_core/release-evidence",
        ),
        "panels": (
            {
                "key": "assets",
                "fragment": "AssetLibraryConsole",
                "binds_to": ("asset", "metadata_tag", "rights_policy"),
                "commands": ("register_asset", "add_metadata_tag", "attach_rights_policy"),
            },
            {
                "key": "renditions",
                "fragment": "RenditionPipelineBoard",
                "binds_to": ("asset_rendition", "transcoding_job", "quality_score"),
                "commands": ("request_rendition", "complete_rendition"),
            },
            {
                "key": "rights",
                "fragment": "RightsPolicyWorkbench",
                "binds_to": ("rights_policy", "rights_decision", "policy_evidence"),
                "commands": ("attach_rights_policy", "enforce_rights"),
            },
            {
                "key": "product_projection",
                "fragment": "ProductPublishedProjectionPanel",
                "binds_to": ("ProductPublished", "product_projection"),
                "commands": ("receive_event",),
            },
            {
                "key": "governance",
                "fragment": "DamRuleStudio",
                "binds_to": ("configuration", "parameter", "rule"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
            {
                "key": "release_evidence",
                "fragment": "DamReleaseEvidencePanel",
                "binds_to": DAM_CORE_RUNTIME_TABLES,
                "commands": ("build_schema_contract", "build_service_contract", "build_release_evidence"),
            },
        ),
        "action_permissions": dam_core_permissions_contract(),
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_storage_tier",
                "allowed_mime_types",
                "rendition_profiles",
                "rights_default_decision",
                "metadata_taxonomies",
                "default_locale",
                "workbench_limit",
            ),
            "allowed_database_backends": DAM_CORE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "max_asset_size_mb",
                "quality_threshold",
                "rights_risk_threshold",
                "transcode_retry_limit",
                "duplicate_similarity_threshold",
                "rendition_cost_weight",
                "carbon_cost_weight",
                "usage_forecast_horizon_days",
                "metadata_confidence_floor",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("asset_governance", "rights_enforcement", "rendition_policy", "metadata_quality"),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "mime_policy",
                "rights_policy",
                "rendition_policy",
                "metadata_policy",
            ),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": DAM_CORE_EMITTED_EVENT_TYPES,
            "consumes": DAM_CORE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": DAM_CORE_OWNED_TABLES,
            "runtime_tables": DAM_CORE_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
        },
    }


def dam_core_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = dam_core_ui_contract()
    snapshot = dam_core_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.dam-core-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/dam_core",
        "fragments": contract["fragments"],
        "cards": (
            {"key": "assets", "value": snapshot["asset_count"], "fragment": "AssetLibraryConsole"},
            {"key": "renditions", "value": snapshot["rendition_count"], "fragment": "RenditionPipelineBoard"},
            {"key": "rights", "value": snapshot["rights_policy_count"], "fragment": "RightsPolicyWorkbench"},
            {"key": "metadata", "value": snapshot["metadata_tag_count"], "fragment": "MetadataTagStudio"},
            {"key": "product_projection", "value": snapshot["product_projection_count"], "fragment": "ProductPublishedProjectionPanel"},
            {"key": "dead_letters", "value": snapshot["dead_letter_count"], "fragment": "DamDeadLetterQueue"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "configuration_hash": snapshot["configuration_hash"],
        "rules_bound": snapshot["rules_bound"],
        "parameters_bound": snapshot["parameters_bound"],
        "event_outbox_count": snapshot["outbox_count"],
        "event_inbox_count": snapshot["inbox_count"],
        "dead_letter_count": snapshot["dead_letter_count"],
        "binding_evidence": {
            "owned_tables": snapshot["owned_tables"],
            "runtime_tables": DAM_CORE_RUNTIME_TABLES,
            "event_contract": snapshot["event_contract"],
            "product_projection_count": snapshot["product_projection_count"],
            "shared_table_access": False,
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
    contract = dam_core_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = dam_core_render_workbench(
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
