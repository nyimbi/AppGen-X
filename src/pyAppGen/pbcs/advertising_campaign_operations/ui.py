"""UI contract and standalone workbench surface for the advertising campaign slice."""

from __future__ import annotations

from .permissions import permission_manifest
from .permissions import principal_permissions
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_RUNTIME_TABLES
from .runtime import advertising_campaign_operations_build_workbench_view
from .workflows import workflow_catalog

PBC_KEY = "advertising_campaign_operations"
UI_FRAGMENT_KEYS = (
    "AdvertisingCampaignOperationsWorkbench",
    "AdvertisingCampaignOperationsLaunchPlanner",
    "AdvertisingCampaignOperationsBuyerWorkbench",
    "AdvertisingCampaignOperationsAssistantPanel",
    "AdvertisingCampaignOperationsReleaseWorkbench",
)
FORM_KEYS = (
    "campaign_brief_form",
    "launch_readiness_form",
    "runtime_configuration_form",
    "policy_rule_form",
    "document_instruction_form",
)
WIZARD_KEYS = (
    "campaign_planning_wizard",
    "launch_gate_wizard",
    "release_evidence_wizard",
)
CONTROL_KEYS = (
    "tenant_scope_picker",
    "channel_mix_grid",
    "launch_gate_banner",
    "blocker_queue",
    "assistant_crud_preview",
    "release_evidence_drawer",
)


def advertising_campaign_operations_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "campaign_brief_form",
            "title": "Campaign Brief",
            "command": "create_campaign_plan",
            "fields": (
                "tenant",
                "code",
                "brief.objective",
                "brief.offer",
                "brief.audience_promise",
                "brief.channels",
                "brief.primary_kpi",
                "brief.guardrails",
                "brief.launch_dependencies",
            ),
        },
        {
            "key": "launch_readiness_form",
            "title": "Launch Readiness",
            "command": "attempt_launch_campaign",
            "fields": (
                "campaign_id",
                "readiness.budget_approved",
                "readiness.creative_approved",
                "readiness.audience_ready",
                "readiness.placements_ready",
                "readiness.tracking_ready",
                "readiness.suppliers_eligible",
                "readiness.policy_compliant",
                "readiness.dependency_status",
            ),
        },
        {
            "key": "runtime_configuration_form",
            "title": "Runtime Configuration",
            "command": "configure_runtime",
            "fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "default_timezone",
                "budget_control_mode",
                "tracking_required",
                "workbench_limit",
            ),
        },
        {
            "key": "policy_rule_form",
            "title": "Launch Policy Rule",
            "command": "register_rule",
            "fields": ("rule_id", "scope", "required_flags"),
        },
        {
            "key": "document_instruction_form",
            "title": "Document Instruction Plan",
            "command": "document_instruction_plan",
            "fields": ("document", "instruction"),
        },
    )


def advertising_campaign_operations_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "campaign_planning_wizard",
            "steps": ("campaign_brief_form", "document_instruction_form"),
            "goal": "Capture one brief and produce one deterministic campaign plan.",
        },
        {
            "key": "launch_gate_wizard",
            "steps": ("launch_readiness_form", "policy_rule_form"),
            "goal": "Review blockers, apply launch policies, and decide whether launch may proceed.",
        },
        {
            "key": "release_evidence_wizard",
            "steps": ("runtime_configuration_form", "document_instruction_form"),
            "goal": "Collect evidence for package-local release readiness and assistant planning.",
        },
    )


def advertising_campaign_operations_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "channel_mix_grid", "type": "grid", "binds_to": "campaign_plan.brief.channels"},
        {"key": "launch_gate_banner", "type": "banner", "binds_to": "command_center.summary"},
        {"key": "blocker_queue", "type": "list", "binds_to": "launch_queue"},
        {"key": "assistant_crud_preview", "type": "drawer", "binds_to": "assistant.document_plan"},
        {"key": "release_evidence_drawer", "type": "drawer", "binds_to": "release_evidence"},
    )


def advertising_campaign_operations_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_id": "advertising_campaign_operations_one_pbc_app",
        "workbench_route": f"/workbench/pbcs/{PBC_KEY}",
        "navigation": (
            {"key": "overview", "route": f"/workbench/pbcs/{PBC_KEY}"},
            {"key": "plans", "route": f"/workbench/pbcs/{PBC_KEY}/plans"},
            {"key": "launch", "route": f"/workbench/pbcs/{PBC_KEY}/launch"},
            {"key": "assistant", "route": f"/workbench/pbcs/{PBC_KEY}/assistant"},
            {"key": "release", "route": f"/workbench/pbcs/{PBC_KEY}/release"},
        ),
        "forms": FORM_KEYS,
        "wizards": WIZARD_KEYS,
        "controls": CONTROL_KEYS,
        "single_agent_namespace": f"{PBC_KEY}_skills",
        "side_effects": (),
    }


def advertising_campaign_operations_ui_contract() -> dict:
    permissions = permission_manifest()
    workflows = workflow_catalog()
    return {
        "format": "appgen.advertising-campaign-operations-ui-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "fragments": UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in advertising_campaign_operations_standalone_app_contract()["navigation"]),
        "forms": advertising_campaign_operations_form_catalog(),
        "wizards": advertising_campaign_operations_wizard_catalog(),
        "controls": advertising_campaign_operations_control_catalog(),
        "standalone_app": advertising_campaign_operations_standalone_app_contract(),
        "action_permissions": permissions["action_permissions"],
        "workflow_catalog": workflows["workflows"],
        "binding_evidence": {
            "owned_tables": ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES,
            "runtime_tables": ADVERTISING_CAMPAIGN_OPERATIONS_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def advertising_campaign_operations_render_workbench(
    state: dict | None = None,
    *,
    tenant: str = "default",
    principal_permissions_override: tuple[str, ...] | None = None,
) -> dict:
    contract = advertising_campaign_operations_ui_contract()
    shell = advertising_campaign_operations_standalone_app_contract()
    snapshot = advertising_campaign_operations_build_workbench_view(tenant=tenant, state=state or {})
    granted_permissions = principal_permissions_override or principal_permissions({"roles": ("administrator",)})
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in granted_permissions
    )
    summary = snapshot["command_center"]["summary"]
    return {
        "format": "appgen.advertising-campaign-operations-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "campaigns", "value": summary["campaign_count"], "fragment": "AdvertisingCampaignOperationsWorkbench"},
            {"key": "ready_to_launch", "value": summary["ready_count"], "fragment": "AdvertisingCampaignOperationsLaunchPlanner"},
            {"key": "blocked", "value": summary["blocked_count"], "fragment": "AdvertisingCampaignOperationsLaunchPlanner"},
            {"key": "outbox_events", "value": len((state or {}).get("outbox", ())), "fragment": "AdvertisingCampaignOperationsReleaseWorkbench"},
        ),
        "launch_queue": snapshot["command_center"]["launch_queue"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "binding_evidence": contract["binding_evidence"],
        "workflow_catalog": contract["workflow_catalog"],
        "workbench": snapshot,
        "side_effects": (),
    }


def advertising_campaign_operations_render_standalone_app(
    state: dict | None = None,
    *,
    tenant: str = "default",
    principal_permissions_override: tuple[str, ...] | None = None,
) -> dict:
    rendered = advertising_campaign_operations_render_workbench(
        state or {},
        tenant=tenant,
        principal_permissions_override=principal_permissions_override,
    )
    return {
        "ok": rendered["ok"],
        "pbc": PBC_KEY,
        "shell": advertising_campaign_operations_standalone_app_contract(),
        "workbench": rendered,
        "side_effects": (),
    }


def smoke_test() -> dict:
    rendered = advertising_campaign_operations_render_standalone_app(
        {"campaign_plans": {}, "outbox": []},
        tenant="tenant-smoke",
    )
    return {
        "ok": advertising_campaign_operations_ui_contract()["ok"] and rendered["ok"] and bool(rendered["workbench"]["forms"]) and bool(rendered["workbench"]["wizards"]),
        "rendered": rendered,
        "side_effects": (),
    }
