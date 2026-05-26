"""UI contract for the Lead Opportunity PBC."""

from __future__ import annotations

from .runtime import LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
from .runtime import LEAD_OPPORTUNITY_OWNED_TABLES


LEAD_OPPORTUNITY_UI_FRAGMENT_KEYS = (
    "LeadOpportunityWorkbench",
    "LeadInbox",
    "AccountHierarchyMap",
    "LeadQualificationBoard",
    "OpportunityPipeline",
    "SalesActivityTimeline",
    "ForecastRollupPanel",
    "NextBestActionPanel",
    "CustomerSegmentProjectionPanel",
    "RevenueRuleStudio",
    "RevenueParameterConsole",
    "RevenueConfigurationPanel",
    "RevenueEventOutbox",
    "RevenueDeadLetterQueue",
)


def lead_opportunity_ui_contract() -> dict:
    return {
        "format": "appgen.lead-opportunity-ui-contract.v1",
        "ok": True,
        "pbc": "lead_opportunity",
        "implementation_directory": "src/pyAppGen/pbcs/lead_opportunity",
        "fragments": LEAD_OPPORTUNITY_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/lead_opportunity",
            "/workbench/pbcs/lead_opportunity/leads",
            "/workbench/pbcs/lead_opportunity/accounts",
            "/workbench/pbcs/lead_opportunity/opportunities",
            "/workbench/pbcs/lead_opportunity/activities",
            "/workbench/pbcs/lead_opportunity/forecast",
            "/workbench/pbcs/lead_opportunity/configuration",
        ),
        "panels": (
            {"key": "leads", "fragment": "LeadInbox", "binds_to": ("lead",), "commands": ("create_lead", "qualify_lead")},
            {"key": "accounts", "fragment": "AccountHierarchyMap", "binds_to": ("account_hierarchy",), "commands": ("create_account_hierarchy",)},
            {"key": "pipeline", "fragment": "OpportunityPipeline", "binds_to": ("opportunity", "sales_activity"), "commands": ("create_opportunity", "advance_opportunity", "win_opportunity")},
            {"key": "governance", "fragment": "RevenueRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "create_account_hierarchy": "lead_opportunity.lead.write",
            "create_lead": "lead_opportunity.lead.write",
            "qualify_lead": "lead_opportunity.lead.write",
            "create_opportunity": "lead_opportunity.opportunity.write",
            "advance_opportunity": "lead_opportunity.opportunity.write",
            "win_opportunity": "lead_opportunity.opportunity.write",
            "record_sales_activity": "lead_opportunity.activity.write",
            "receive_event": "lead_opportunity.event.consume",
            "register_rule": "lead_opportunity.configure",
            "set_parameter": "lead_opportunity.configure",
            "configure_runtime": "lead_opportunity.configure",
            "run_control_tests": "lead_opportunity.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone", "assignment_mode"),
            "allowed_database_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "qualification_score_threshold",
                "win_probability_threshold",
                "stale_activity_days",
                "forecast_confidence_floor",
                "deal_slippage_threshold",
                "lead_source_weight",
                "segment_fit_weight",
                "engagement_weight",
                "max_open_opportunities_per_account",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("qualification", "assignment", "forecast", "pipeline", "activity"),
            "required_fields": ("rule_id", "tenant", "scope", "status", "allowed_regions", "allowed_currencies", "allowed_segments", "qualification_policy", "assignment_policy"),
        },
        "event_surfaces": {
            "emits": ("OpportunityWon", "CustomerUpdated", "LeadQualified"),
            "consumes": ("CustomerSegmentUpdated",),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def lead_opportunity_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = lead_opportunity_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "leads", "value": view["lead_count"], "fragment": "LeadInbox"},
        {"key": "qualified", "value": view["qualified_lead_count"], "fragment": "LeadQualificationBoard"},
        {"key": "opportunities", "value": view["opportunity_count"], "fragment": "OpportunityPipeline"},
        {"key": "won", "value": view["won_opportunity_count"], "fragment": "ForecastRollupPanel"},
        {"key": "activities", "value": view["activity_count"], "fragment": "SalesActivityTimeline"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "RevenueEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "RevenueDeadLetterQueue"},
    )
    return {
        "format": "appgen.lead-opportunity-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/lead_opportunity",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    leads = tuple(item for item in state.get("leads", {}).values() if item["tenant"] == tenant)
    opportunities = tuple(item for item in state.get("opportunities", {}).values() if item["tenant"] == tenant)
    activities = tuple(item for item in state.get("sales_activities", {}).values() if item["tenant"] == tenant)
    return {
        "lead_count": len(leads),
        "qualified_lead_count": len(tuple(item for item in leads if item["status"] == "qualified")),
        "opportunity_count": len(opportunities),
        "won_opportunity_count": len(tuple(item for item in opportunities if item["status"] == "won")),
        "activity_count": len(activities),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        },
    }
