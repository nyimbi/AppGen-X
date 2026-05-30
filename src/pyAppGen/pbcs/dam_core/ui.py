"""UI contract and standalone workbench surface for the dam_core PBC."""

from __future__ import annotations

from .dam_control import improve1_dam_control_contract
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
    "DamCoreAssetWorkbench",
    "DamCoreRightsWorkbench",
    "DamCoreOperationsWorkbench",
    "DamCoreReleaseWorkbench",
)
DAM_CORE_FORM_KEYS = (
    "asset_intake_form",
    "rights_policy_form",
    "metadata_tag_form",
    "rendition_request_form",
    "document_intake_form",
)
DAM_CORE_WIZARD_KEYS = (
    "asset_onboarding_wizard",
    "rights_clearance_wizard",
    "release_readiness_wizard",
)
DAM_CORE_CONTROL_KEYS = (
    "tenant_scope_picker",
    "asset_status_chips",
    "event_stream_timeline",
    "document_dropzone",
    "audit_evidence_drawer",
    "release_gate_banner",
)


def dam_core_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "asset_intake_form",
            "title": "Asset Intake",
            "command": "register_asset",
            "fields": ("asset_id", "tenant", "filename", "mime_type", "size_mb", "storage_uri", "created_by"),
        },
        {
            "key": "rights_policy_form",
            "title": "Rights Policy",
            "command": "attach_rights_policy",
            "fields": ("policy_id", "asset_id", "tenant", "license_type", "allowed_markets", "blocked_markets", "expires_at", "approver"),
        },
        {
            "key": "metadata_tag_form",
            "title": "Metadata Tagging",
            "command": "add_metadata_tag",
            "fields": ("tag_id", "asset_id", "tenant", "taxonomy", "value", "confidence", "source"),
        },
        {
            "key": "rendition_request_form",
            "title": "Rendition Request",
            "command": "request_rendition",
            "fields": ("rendition_id", "asset_id", "tenant", "profile", "target_mime_type", "width", "height"),
        },
        {
            "key": "document_intake_form",
            "title": "Document Intake",
            "command": "document_instruction_plan",
            "fields": ("document", "instructions"),
        },
    )


def dam_core_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "asset_onboarding_wizard",
            "steps": ("asset_intake_form", "rights_policy_form", "metadata_tag_form", "rendition_request_form"),
            "goal": "Register one asset and make it publication-ready inside dam_core only.",
        },
        {
            "key": "rights_clearance_wizard",
            "steps": ("rights_policy_form", "document_intake_form"),
            "goal": "Capture rights evidence, draft entitlement work, and explain required approvals.",
        },
        {
            "key": "release_readiness_wizard",
            "steps": ("asset_intake_form", "metadata_tag_form", "document_intake_form"),
            "goal": "Drive one release-ready review flow with workbench and gate evidence.",
        },
    )


def dam_core_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "asset_status_chips", "type": "status_group", "binds_to": "asset.status"},
        {"key": "event_stream_timeline", "type": "timeline", "binds_to": "events"},
        {"key": "document_dropzone", "type": "upload", "binds_to": "agent.document_intake"},
        {"key": "audit_evidence_drawer", "type": "drawer", "binds_to": "release_evidence"},
        {"key": "release_gate_banner", "type": "banner", "binds_to": "release_gates"},
    )


def dam_core_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "dam_core",
        "app_id": "dam_core_one_pbc_app",
        "workbench_route": "/workbench/pbcs/dam_core",
        "navigation": (
            {"key": "assets", "route": "/workbench/pbcs/dam_core/assets"},
            {"key": "rights", "route": "/workbench/pbcs/dam_core/rights"},
            {"key": "metadata", "route": "/workbench/pbcs/dam_core/metadata"},
            {"key": "operations", "route": "/workbench/pbcs/dam_core/operations"},
            {"key": "release", "route": "/workbench/pbcs/dam_core/release"},
        ),
        "forms": DAM_CORE_FORM_KEYS,
        "wizards": DAM_CORE_WIZARD_KEYS,
        "controls": DAM_CORE_CONTROL_KEYS,
        "single_agent_namespace": "dam_core_skills",
        "side_effects": (),
    }


def dam_core_ui_contract() -> dict:
    return {
        "format": "appgen.dam-core-ui-contract.v2",
        "ok": True,
        "pbc": "dam_core",
        "implementation_directory": "src/pyAppGen/pbcs/dam_core",
        "fragments": DAM_CORE_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in dam_core_standalone_app_contract()["navigation"]) + (
            "/workbench/pbcs/dam_core",
        ),
        "panels": (
            {"key": "assets", "fragment": "DamCoreAssetWorkbench", "binds_to": ("asset", "asset_collection", "asset_rendition"), "commands": ("register_asset", "create_asset_collection", "request_rendition")},
            {"key": "rights", "fragment": "DamCoreRightsWorkbench", "binds_to": ("rights_policy", "license_agreement", "usage_entitlement"), "commands": ("attach_rights_policy", "register_license_agreement", "grant_usage_entitlement", "enforce_rights")},
            {"key": "operations", "fragment": "DamCoreOperationsWorkbench", "binds_to": ("metadata_tag", "metadata_taxonomy", "asset_workflow_case", "asset_exception"), "commands": ("add_metadata_tag", "register_metadata_taxonomy", "start_asset_workflow", "open_asset_exception")},
            {"key": "release", "fragment": "DamCoreReleaseWorkbench", "binds_to": DAM_CORE_RUNTIME_TABLES, "commands": ("build_schema_contract", "build_service_contract", "build_release_evidence")},
        ),
        "forms": dam_core_form_catalog(),
        "wizards": dam_core_wizard_catalog(),
        "controls": dam_core_control_catalog(),
        "dam_control_panels": tuple(item["ui_surface"] for item in improve1_dam_control_contract()["capabilities"]),
        "standalone_app": dam_core_standalone_app_contract(),
        "action_permissions": dam_core_permissions_contract(),
        "dam_control_contract": improve1_dam_control_contract(),
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
    shell = dam_core_standalone_app_contract()
    snapshot = dam_core_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.dam-core-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "assets", "value": snapshot["asset_count"], "fragment": "DamCoreAssetWorkbench"},
            {"key": "renditions", "value": snapshot["ready_rendition_count"], "fragment": "DamCoreAssetWorkbench"},
            {"key": "rights", "value": snapshot["rights_policy_count"], "fragment": "DamCoreRightsWorkbench"},
            {"key": "metadata", "value": snapshot["metadata_tag_count"], "fragment": "DamCoreOperationsWorkbench"},
            {"key": "workflow", "value": snapshot["approved_workflow_count"], "fragment": "DamCoreOperationsWorkbench"},
            {"key": "exceptions", "value": snapshot["resolved_exception_count"], "fragment": "DamCoreOperationsWorkbench"},
            {"key": "events", "value": snapshot["outbox_count"] + snapshot["inbox_count"], "fragment": "DamCoreReleaseWorkbench"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "configuration_hash": snapshot["configuration_hash"],
        "rules_bound": snapshot["rules_bound"],
        "parameters_bound": snapshot["parameters_bound"],
        "binding_evidence": {
            "owned_tables": snapshot["owned_tables"],
            "runtime_tables": DAM_CORE_RUNTIME_TABLES,
            "event_contract": snapshot["event_contract"],
            "product_projection_count": snapshot["product_projection_count"],
            "shared_table_access": False,
        },
    }


def dam_core_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render the package-local standalone app shell."""
    workbench = dam_core_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)
    return {
        "ok": workbench["ok"],
        "pbc": "dam_core",
        "shell": dam_core_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
            "events": (),
            "assets": {},
            "asset_renditions": {},
            "rights_policies": {},
            "metadata_tags": {},
            "asset_collections": {},
            "license_agreements": {},
            "usage_entitlements": {},
            "metadata_enrichments": {},
            "semantic_annotations": {},
            "asset_workflow_cases": {},
            "asset_exceptions": {},
            "asset_usage_snapshots": {},
            "asset_duplicate_candidates": {},
            "asset_lineage": {},
            "product_projection": {},
            "processed_event_keys": (),
        }
    )


def smoke_test() -> dict:
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = dam_core_ui_contract()
    rendered = dam_core_render_standalone_app(
        _appgen_smoke_state(),
        tenant="tenant_smoke",
        principal_permissions=tuple(sorted(set(dam_core_permissions_contract().values()))),
    )
    return {
        "ok": contract["ok"] and rendered["ok"] and bool(contract["forms"]) and bool(contract["wizards"]),
        "manifest": contract,
        "rendered": rendered["workbench"],
        "side_effects": (),
    }
