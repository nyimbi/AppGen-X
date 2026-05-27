"""UI contract for the Lead Opportunity PBC."""

from __future__ import annotations

from .runtime import LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
from .runtime import LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
from .runtime import LEAD_OPPORTUNITY_OWNED_TABLES
from .runtime import LEAD_OPPORTUNITY_RUNTIME_TABLES


LEAD_OPPORTUNITY_UI_FRAGMENT_KEYS = (
    "LeadOpportunityWorkbench",
    "LeadInbox",
    "LeadEnrichmentBoard",
    "DedupResolutionQueue",
    "QualificationDecisionLedger",
    "AccountHierarchyMap",
    "LeadQualificationBoard",
    "OpportunityPipeline",
    "SalesActivityTimeline",
    "ForecastRollupPanel",
    "QuoteProposalHandoffPanel",
    "WinLossOutcomeBoard",
    "SalesCoachingPanel",
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
            {"key": "leads", "fragment": "LeadInbox", "binds_to": ("lead", "lead_enrichment_snapshot", "lead_dedup_case", "lead_score_snapshot", "lead_assignment", "qualification_decision"), "commands": ("create_lead", "enrich_lead", "qualify_lead")},
            {"key": "accounts", "fragment": "AccountHierarchyMap", "binds_to": ("account_hierarchy",), "commands": ("create_account_hierarchy",)},
            {"key": "pipeline", "fragment": "OpportunityPipeline", "binds_to": ("opportunity", "opportunity_stage_history", "pipeline_forecast_snapshot", "quote_proposal_handoff", "opportunity_outcome", "sales_activity", "sales_coaching_insight"), "commands": ("create_opportunity", "advance_opportunity", "create_quote_proposal_handoff", "win_opportunity", "lose_opportunity", "record_sales_activity")},
            {"key": "governance", "fragment": "RevenueRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "create_account_hierarchy": "lead_opportunity.lead.write",
            "create_lead": "lead_opportunity.lead.write",
            "enrich_lead": "lead_opportunity.lead.write",
            "qualify_lead": "lead_opportunity.lead.write",
            "create_opportunity": "lead_opportunity.opportunity.write",
            "advance_opportunity": "lead_opportunity.opportunity.write",
            "create_quote_proposal_handoff": "lead_opportunity.opportunity.write",
            "win_opportunity": "lead_opportunity.opportunity.write",
            "lose_opportunity": "lead_opportunity.opportunity.write",
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
            "required_event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
            "emits": ("LeadQualified", "OpportunityWon", "OpportunityLost", "CustomerUpdated", "QuoteProposalRequested"),
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
        {"key": "enrichment", "value": view["lead_enrichment_count"], "fragment": "LeadEnrichmentBoard"},
        {"key": "dedup", "value": view["lead_dedup_case_count"], "fragment": "DedupResolutionQueue"},
        {"key": "qualification_decisions", "value": view["qualification_decision_count"], "fragment": "QualificationDecisionLedger"},
        {"key": "opportunities", "value": view["opportunity_count"], "fragment": "OpportunityPipeline"},
        {"key": "won", "value": view["won_opportunity_count"], "fragment": "ForecastRollupPanel"},
        {"key": "handoffs", "value": view["quote_handoff_count"], "fragment": "QuoteProposalHandoffPanel"},
        {"key": "outcomes", "value": view["opportunity_outcome_count"], "fragment": "WinLossOutcomeBoard"},
        {"key": "coaching", "value": view["sales_coaching_insight_count"], "fragment": "SalesCoachingPanel"},
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
    enrichment = tuple(item for item in state.get("lead_enrichment_snapshots", {}).values() if item["tenant"] == tenant)
    dedup_cases = tuple(item for item in state.get("lead_dedup_cases", {}).values() if item["tenant"] == tenant)
    qualification_decisions = tuple(item for item in state.get("qualification_decisions", {}).values() if item["tenant"] == tenant)
    handoffs = tuple(item for item in state.get("quote_proposal_handoffs", {}).values() if item["tenant"] == tenant)
    outcomes = tuple(item for item in state.get("opportunity_outcomes", {}).values() if item["tenant"] == tenant)
    coaching = tuple(item for item in state.get("sales_coaching_insights", {}).values() if item["tenant"] == tenant)
    return {
        "lead_count": len(leads),
        "qualified_lead_count": len(tuple(item for item in leads if item["status"] == "qualified")),
        "lead_enrichment_count": len(enrichment),
        "lead_dedup_case_count": len(dedup_cases),
        "qualification_decision_count": len(qualification_decisions),
        "opportunity_count": len(opportunities),
        "won_opportunity_count": len(tuple(item for item in opportunities if item["status"] == "won")),
        "quote_handoff_count": len(handoffs),
        "opportunity_outcome_count": len(outcomes),
        "sales_coaching_insight_count": len(coaching),
        "activity_count": len(activities),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
            "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
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
    contract = lead_opportunity_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = lead_opportunity_render_workbench(
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
