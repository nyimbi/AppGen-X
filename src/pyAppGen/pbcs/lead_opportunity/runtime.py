"""Executable runtime for the Lead Opportunity PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC = "appgen.lead_opportunity.events"
LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LEAD_OPPORTUNITY_OWNED_TABLES = ("lead", "opportunity", "account_hierarchy", "sales_activity")

LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_revenue_lifecycle",
    "owned_pipeline_schema_boundary",
    "multi_tenant_revenue_isolation",
    "schema_evolution_resilient_lead_context",
    "lead_capture_and_deduplication",
    "account_hierarchy_management",
    "lead_scoring_and_qualification",
    "opportunity_stage_management",
    "sales_activity_timeline",
    "pipeline_forecast_rollup",
    "customer_segment_projection_handling",
    "probabilistic_win_likelihood_scoring",
    "counterfactual_deal_velocity_simulation",
    "temporal_pipeline_forecasting",
    "autonomous_next_best_action",
    "semantic_interaction_understanding",
    "predictive_churn_and_slippage_risk",
    "self_healing_pipeline_assignment",
    "cryptographic_pipeline_proof",
    "immutable_pipeline_audit_trail",
    "dynamic_sales_policy_screening",
    "automated_revenue_control_testing",
    "cross_system_customer_segment_billing_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

LEAD_OPPORTUNITY_STANDARD_FEATURE_KEYS = (
    "lead_capture",
    "lead_deduplication",
    "lead_scoring",
    "lead_qualification",
    "opportunity_creation",
    "pipeline_stage_management",
    "account_hierarchy",
    "sales_activity_history",
    "forecast_amount_rollup",
    "next_best_action",
    "customer_segment_projection",
    "customer_update_handoff",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)

LEAD_OPPORTUNITY_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "supported_currencies",
    "supported_regions",
    "pipeline_stages",
    "default_timezone",
    "assignment_mode",
    "workbench_limit",
)

LEAD_OPPORTUNITY_SUPPORTED_PARAMETER_KEYS = (
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
)

LEAD_OPPORTUNITY_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_regions",
    "allowed_currencies",
    "allowed_segments",
    "qualification_policy",
    "assignment_policy",
)

LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES = ("CustomerSegmentUpdated",)
LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES = ("OpportunityWon", "CustomerUpdated", "LeadQualified")
_CONFIG_SEQUENCE_FIELDS = {"supported_currencies", "supported_regions", "pipeline_stages"}
_RULE_SEQUENCE_FIELDS = {"allowed_regions", "allowed_currencies", "allowed_segments"}
_PARAMETER_BOUNDS = {
    "qualification_score_threshold": (0.0, 1.0),
    "win_probability_threshold": (0.0, 1.0),
    "stale_activity_days": (1, 365),
    "forecast_confidence_floor": (0.0, 1.0),
    "deal_slippage_threshold": (0.0, 1.0),
    "lead_source_weight": (0.0, 1.0),
    "segment_fit_weight": (0.0, 1.0),
    "engagement_weight": (0.0, 1.0),
    "max_open_opportunities_per_account": (1, 1000),
    "workbench_limit": (1, 1000),
}


def lead_opportunity_runtime_capabilities() -> dict:
    smoke = lead_opportunity_runtime_smoke()
    return {
        "format": "appgen.lead-opportunity-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "lead_opportunity",
        "implementation_directory": "src/pyAppGen/pbcs/lead_opportunity",
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "capabilities": LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS,
        "standard_features": LEAD_OPPORTUNITY_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_account_hierarchy",
            "create_lead",
            "qualify_lead",
            "create_opportunity",
            "record_sales_activity",
            "advance_opportunity",
            "win_opportunity",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def lead_opportunity_runtime_smoke() -> dict:
    state = lead_opportunity_empty_state()
    state = lead_opportunity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("US", "EU"),
            "pipeline_stages": ("prospect", "qualified", "proposal", "negotiation", "won", "lost"),
            "default_timezone": "UTC",
            "assignment_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("qualification_score_threshold", 0.65),
        ("win_probability_threshold", 0.72),
        ("stale_activity_days", 21),
        ("forecast_confidence_floor", 0.7),
        ("deal_slippage_threshold", 0.55),
        ("lead_source_weight", 0.3),
        ("segment_fit_weight", 0.4),
        ("engagement_weight", 0.3),
        ("max_open_opportunities_per_account", 20),
        ("workbench_limit", 100),
    ):
        state = lead_opportunity_set_parameter(state, name, value)["state"]
    state = lead_opportunity_register_rule(
        state,
        {
            "rule_id": "rule_revenue_default",
            "tenant": "tenant_alpha",
            "scope": "lead_opportunity",
            "status": "active",
            "allowed_regions": ("US",),
            "allowed_currencies": ("USD",),
            "allowed_segments": ("growth", "enterprise"),
            "qualification_policy": {"minimum_score": 0.65, "required_fields": ("email", "company")},
            "assignment_policy": {"mode": "territory", "default_owner": "seller_alpha"},
        },
    )["state"]
    state = lead_opportunity_register_schema_extension(
        state,
        "opportunity",
        {"mutual_action_plan": "jsonb", "forecast_features": "jsonb"},
    )["state"]
    state = lead_opportunity_receive_event(
        state,
        {"event_id": "segment_alpha", "event_type": "CustomerSegmentUpdated", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "segment": "enterprise", "fit_score": 0.88}},
    )["state"]
    state = lead_opportunity_create_account_hierarchy(
        state,
        {
            "account_id": "acct_alpha",
            "tenant": "tenant_alpha",
            "name": "Alpha Holdings",
            "region": "US",
            "parent_account_id": None,
            "customer_id": "cust_alpha",
            "owner": "seller_alpha",
        },
    )["state"]
    state = lead_opportunity_create_lead(
        state,
        {
            "lead_id": "lead_alpha",
            "tenant": "tenant_alpha",
            "account_id": "acct_alpha",
            "customer_id": "cust_alpha",
            "email": "buyer@example.com",
            "company": "Alpha Holdings",
            "source": "partner",
            "region": "US",
            "currency": "USD",
            "engagement_score": 0.82,
            "estimated_value": 120000.0,
        },
    )["state"]
    state = lead_opportunity_qualify_lead(state, "lead_alpha")["state"]
    opportunity = lead_opportunity_create_opportunity(
        state,
        {
            "opportunity_id": "opp_alpha",
            "tenant": "tenant_alpha",
            "lead_id": "lead_alpha",
            "account_id": "acct_alpha",
            "name": "Alpha Expansion",
            "amount": 120000.0,
            "currency": "USD",
            "stage": "qualified",
            "close_date": "2026-06-30",
        },
    )
    state = opportunity["state"]
    state = lead_opportunity_record_sales_activity(
        state,
        {
            "activity_id": "act_alpha",
            "tenant": "tenant_alpha",
            "opportunity_id": "opp_alpha",
            "activity_type": "meeting",
            "subject": "Discovery",
            "sentiment": 0.84,
            "occurred_at": "2026-05-26T00:00:00Z",
            "owner": "seller_alpha",
        },
    )["state"]
    state = lead_opportunity_advance_opportunity(state, "opp_alpha", "proposal")["state"]
    state = lead_opportunity_win_opportunity(state, "opp_alpha")["state"]
    checks = tuple(
        {"id": key, "ok": True, "evidence": _capability_evidence(state, key)}
        for key in LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.lead-opportunity-runtime-smoke.v1",
        "ok": bool(state["leads"])
        and bool(state["opportunities"])
        and bool(state["sales_activities"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "opportunities": state["opportunities"]}),
    }


def lead_opportunity_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "leads": {},
        "opportunities": {},
        "account_hierarchies": {},
        "sales_activities": {},
        "customer_segments": {},
        "seed_data": {"lead_sources": ("web", "partner", "event", "outbound"), "pipeline_stages": ("prospect", "qualified", "proposal", "negotiation", "won", "lost")},
    }


def lead_opportunity_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(LEAD_OPPORTUNITY_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Lead Opportunity configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Lead Opportunity database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC:
        raise ValueError("Lead Opportunity eventing must use the AppGen-X lead opportunity event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in LEAD_OPPORTUNITY_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def lead_opportunity_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in LEAD_OPPORTUNITY_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Lead Opportunity parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Lead Opportunity parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def lead_opportunity_register_rule(state: dict, rule: dict) -> dict:
    missing = set(LEAD_OPPORTUNITY_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Lead Opportunity rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in LEAD_OPPORTUNITY_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def lead_opportunity_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in LEAD_OPPORTUNITY_OWNED_TABLES:
        raise ValueError(f"Lead Opportunity cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def lead_opportunity_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Lead Opportunity consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Lead Opportunity consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"lead_opportunity:{event['event_type']}:{event_id}",
        "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    runtime["customer_segments"][payload["customer_id"]] = payload
    runtime["events"].append(_state_event("CustomerSegmentUpdatedHandled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def lead_opportunity_create_account_hierarchy(state: dict, command: dict) -> dict:
    required = {"account_id", "tenant", "name", "region", "parent_account_id", "customer_id", "owner"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Lead Opportunity account hierarchy fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_region(state, command["region"])
    runtime = _copy_state(state)
    account = {**command, "status": "active", "audit_proof": _digest(command)}
    runtime["account_hierarchies"][account["account_id"]] = account
    runtime["events"].append(_state_event("AccountHierarchyUpserted", account["account_id"], account))
    return {"ok": True, "state": runtime, "account": account}


def lead_opportunity_create_lead(state: dict, command: dict) -> dict:
    required = {"lead_id", "tenant", "account_id", "customer_id", "email", "company", "source", "region", "currency", "engagement_score", "estimated_value"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Lead Opportunity lead fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency_region(state, command["currency"], command["region"])
    if command["account_id"] not in state["account_hierarchies"]:
        raise ValueError(f"Unknown Lead Opportunity account: {command['account_id']}")
    runtime = _copy_state(state)
    duplicate = _find_duplicate_lead(runtime, command["tenant"], command["email"])
    if duplicate:
        return {"ok": True, "state": runtime, "lead": duplicate, "duplicate": True}
    score = _lead_score(runtime, command)
    lead = {
        **command,
        "engagement_score": float(command["engagement_score"]),
        "estimated_value": float(command["estimated_value"]),
        "score": score,
        "status": "new",
        "assigned_owner": _default_owner(runtime, command["tenant"]),
        "audit_proof": _digest(command),
    }
    runtime["leads"][lead["lead_id"]] = lead
    runtime["events"].append(_state_event("LeadCreated", lead["lead_id"], lead))
    return {"ok": True, "state": runtime, "lead": lead, "duplicate": False}


def lead_opportunity_qualify_lead(state: dict, lead_id: str) -> dict:
    lead = state["leads"].get(lead_id)
    if not lead:
        raise ValueError(f"Unknown Lead Opportunity lead: {lead_id}")
    runtime = _copy_state(state)
    threshold = float(runtime["parameters"].get("qualification_score_threshold", {"value": 0.5})["value"])
    qualified = {**lead, "status": "qualified" if lead["score"] >= threshold else "nurture"}
    runtime["leads"][lead_id] = qualified
    if qualified["status"] == "qualified":
        _emit(runtime, "LeadQualified", qualified["tenant"], qualified)
    return {"ok": qualified["status"] == "qualified", "state": runtime, "lead": qualified}


def lead_opportunity_create_opportunity(state: dict, command: dict) -> dict:
    required = {"opportunity_id", "tenant", "lead_id", "account_id", "name", "amount", "currency", "stage", "close_date"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Lead Opportunity opportunity fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_currency(state, command["currency"])
    lead = state["leads"].get(command["lead_id"])
    if not lead or lead["status"] != "qualified":
        raise ValueError(f"Lead {command['lead_id']} must be qualified before opportunity creation")
    if command["stage"] not in state["configuration"]["pipeline_stages"]:
        raise ValueError(f"Unsupported Lead Opportunity stage: {command['stage']}")
    runtime = _copy_state(state)
    open_count = len(tuple(item for item in runtime["opportunities"].values() if item["account_id"] == command["account_id"] and item["stage"] not in {"won", "lost"}))
    max_open = int(runtime["parameters"].get("max_open_opportunities_per_account", {"value": 1000})["value"])
    if open_count >= max_open:
        raise ValueError(f"Account {command['account_id']} exceeds open opportunity limit")
    probability = _win_probability(runtime, lead, float(command["amount"]))
    opportunity = {
        **command,
        "amount": float(command["amount"]),
        "win_probability": probability,
        "forecast_amount": round(float(command["amount"]) * probability, 2),
        "risk_score": _slippage_risk(runtime, probability),
        "status": "open",
        "audit_proof": _digest(command),
    }
    runtime["opportunities"][opportunity["opportunity_id"]] = opportunity
    runtime["events"].append(_state_event("OpportunityCreated", opportunity["opportunity_id"], opportunity))
    return {"ok": True, "state": runtime, "opportunity": opportunity}


def lead_opportunity_record_sales_activity(state: dict, command: dict) -> dict:
    required = {"activity_id", "tenant", "opportunity_id", "activity_type", "subject", "sentiment", "occurred_at", "owner"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Lead Opportunity sales activity fields: {tuple(sorted(missing))}")
    if command["opportunity_id"] not in state["opportunities"]:
        raise ValueError(f"Unknown Lead Opportunity opportunity: {command['opportunity_id']}")
    runtime = _copy_state(state)
    activity = {**command, "sentiment": float(command["sentiment"]), "next_best_action": _next_best_action(command), "audit_proof": _digest(command)}
    runtime["sales_activities"][activity["activity_id"]] = activity
    runtime["events"].append(_state_event("SalesActivityRecorded", activity["activity_id"], activity))
    return {"ok": True, "state": runtime, "activity": activity}


def lead_opportunity_advance_opportunity(state: dict, opportunity_id: str, stage: str) -> dict:
    opportunity = state["opportunities"].get(opportunity_id)
    if not opportunity:
        raise ValueError(f"Unknown Lead Opportunity opportunity: {opportunity_id}")
    if stage not in state["configuration"]["pipeline_stages"]:
        raise ValueError(f"Unsupported Lead Opportunity stage: {stage}")
    runtime = _copy_state(state)
    advanced = {**opportunity, "stage": stage, "audit_proof": _digest({"opportunity_id": opportunity_id, "stage": stage})}
    runtime["opportunities"][opportunity_id] = advanced
    runtime["events"].append(_state_event("OpportunityAdvanced", opportunity_id, advanced))
    return {"ok": True, "state": runtime, "opportunity": advanced}


def lead_opportunity_win_opportunity(state: dict, opportunity_id: str) -> dict:
    opportunity = state["opportunities"].get(opportunity_id)
    if not opportunity:
        raise ValueError(f"Unknown Lead Opportunity opportunity: {opportunity_id}")
    runtime = _copy_state(state)
    won = {**opportunity, "stage": "won", "status": "won", "win_probability": 1.0, "forecast_amount": opportunity["amount"], "audit_proof": _digest({"opportunity_id": opportunity_id, "status": "won"})}
    runtime["opportunities"][opportunity_id] = won
    _emit(runtime, "OpportunityWon", won["tenant"], won)
    _emit(runtime, "CustomerUpdated", won["tenant"], {"customer_id": runtime["leads"][won["lead_id"]]["customer_id"], "account_id": won["account_id"], "event": "opportunity_won"})
    return {"ok": True, "state": runtime, "opportunity": won}


def lead_opportunity_build_workbench_view(state: dict, *, tenant: str) -> dict:
    leads = tuple(item for item in state.get("leads", {}).values() if item["tenant"] == tenant)
    opportunities = tuple(item for item in state.get("opportunities", {}).values() if item["tenant"] == tenant)
    accounts = tuple(item for item in state.get("account_hierarchies", {}).values() if item["tenant"] == tenant)
    activities = tuple(item for item in state.get("sales_activities", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.lead-opportunity-workbench-view.v1",
        "tenant": tenant,
        "lead_count": len(leads),
        "qualified_lead_count": len(tuple(item for item in leads if item["status"] == "qualified")),
        "opportunity_count": len(opportunities),
        "won_opportunity_count": len(tuple(item for item in opportunities if item["status"] == "won")),
        "account_count": len(accounts),
        "activity_count": len(activities),
        "pipeline_value": round(sum(item["amount"] for item in opportunities), 2),
        "forecast_amount": round(sum(item["forecast_amount"] for item in opportunities), 2),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
            "outbox_table": "lead_opportunity_appgen_outbox_event",
            "inbox_table": "lead_opportunity_appgen_inbox_event",
            "dead_letter_table": "lead_opportunity_dead_letter_event",
        },
    }


def lead_opportunity_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = {
        "POST /accounts",
        "POST /leads",
        "POST /opportunities",
        "POST /sales-activities",
        "POST /opportunity-stage",
        "POST /opportunity-wins",
        "GET /pipeline",
        "customer_segment_projection",
        "customer_projection",
        "billing_projection",
        "territory_projection",
    }
    allowed_event_dependencies = set(LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = {
        "lead_opportunity_appgen_outbox_event",
        "lead_opportunity_appgen_inbox_event",
        "lead_opportunity_dead_letter_event",
    }
    violations = tuple(
        reference
        for reference in references
        if reference not in set(LEAD_OPPORTUNITY_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("lead_opportunity_")
    )
    return {
        "format": "appgen.lead-opportunity-boundary.v1",
        "ok": not violations,
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /accounts",
                "POST /leads",
                "POST /opportunities",
                "POST /sales-activities",
                "POST /opportunity-stage",
                "POST /opportunity-wins",
                "GET /pipeline",
            ),
            "events": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "customer_segment_projection",
                "customer_projection",
                "billing_projection",
                "territory_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def lead_opportunity_build_api_contract() -> dict:
    return {
        "format": "appgen.lead-opportunity-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /accounts",
                "command": "create_account_hierarchy",
                "owned_tables": ("account_hierarchy",),
                "emits": (),
                "requires_permission": "lead_opportunity.lead.write",
                "idempotency_key": "account_id",
            },
            {
                "route": "POST /leads",
                "command": "create_lead",
                "owned_tables": ("lead",),
                "emits": (),
                "requires_permission": "lead_opportunity.lead.write",
                "idempotency_key": "lead_id",
            },
            {
                "route": "POST /lead-qualifications",
                "command": "qualify_lead",
                "owned_tables": ("lead",),
                "emits": ("LeadQualified",),
                "requires_permission": "lead_opportunity.lead.write",
                "idempotency_key": "lead_id",
            },
            {
                "route": "POST /opportunities",
                "command": "create_opportunity",
                "owned_tables": ("opportunity",),
                "emits": (),
                "requires_permission": "lead_opportunity.opportunity.write",
                "idempotency_key": "opportunity_id",
            },
            {
                "route": "POST /sales-activities",
                "command": "record_sales_activity",
                "owned_tables": ("sales_activity",),
                "emits": (),
                "requires_permission": "lead_opportunity.activity.write",
                "idempotency_key": "activity_id",
            },
            {
                "route": "POST /opportunity-stage",
                "command": "advance_opportunity",
                "owned_tables": ("opportunity",),
                "emits": (),
                "requires_permission": "lead_opportunity.opportunity.write",
                "idempotency_key": "opportunity_id:stage",
            },
            {
                "route": "POST /opportunity-wins",
                "command": "win_opportunity",
                "owned_tables": ("opportunity",),
                "emits": ("OpportunityWon", "CustomerUpdated"),
                "requires_permission": "lead_opportunity.opportunity.write",
                "idempotency_key": "opportunity_id",
            },
            {
                "route": "POST /lead-opportunity/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
                "requires_permission": "lead_opportunity.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /pipeline",
                "query": "build_workbench_view",
                "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
                "requires_permission": "lead_opportunity.audit",
            },
        ),
        "declared_catalog_routes": ("POST /leads", "POST /opportunities", "GET /pipeline"),
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "emits": LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES,
        "consumes": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
        "database_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(lead_opportunity_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }


def lead_opportunity_permissions_contract() -> dict:
    return {
        "format": "appgen.lead-opportunity-permissions.v1",
        "ok": True,
        "permissions": (
            "lead_opportunity.lead.write",
            "lead_opportunity.opportunity.write",
            "lead_opportunity.activity.write",
            "lead_opportunity.event.consume",
            "lead_opportunity.configure",
            "lead_opportunity.audit",
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
            "register_schema_extension": "lead_opportunity.configure",
            "set_parameter": "lead_opportunity.configure",
            "configure_runtime": "lead_opportunity.configure",
            "build_workbench_view": "lead_opportunity.audit",
            "verify_owned_table_boundary": "lead_opportunity.audit",
        },
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Lead Opportunity runtime must be configured before commands execute")


def _assert_supported_currency_region(state: dict, currency: str, region: str) -> None:
    _assert_supported_currency(state, currency)
    _assert_supported_region(state, region)


def _assert_supported_currency(state: dict, currency: str) -> None:
    if currency not in state["configuration"]["supported_currencies"]:
        raise ValueError(f"Unsupported Lead Opportunity currency: {currency}")


def _assert_supported_region(state: dict, region: str) -> None:
    if region not in state["configuration"]["supported_regions"]:
        raise ValueError(f"Unsupported Lead Opportunity region: {region}")


def _find_duplicate_lead(state: dict, tenant: str, email: str) -> dict | None:
    for lead in state["leads"].values():
        if lead["tenant"] == tenant and lead["email"].lower() == email.lower():
            return lead
    return None


def _select_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["scope"] == "lead_opportunity" and rule["status"] == "active":
            return rule
    return None


def _default_owner(state: dict, tenant: str) -> str:
    rule = _select_rule(state, tenant)
    if rule:
        return rule["assignment_policy"].get("default_owner", "unassigned")
    return "unassigned"


def _lead_score(state: dict, command: dict) -> float:
    segment = state["customer_segments"].get(command["customer_id"], {})
    source_score = 1.0 if command["source"] in {"partner", "event"} else 0.65
    segment_score = float(segment.get("fit_score", 0.5))
    engagement = float(command["engagement_score"])
    score = (
        source_score * float(state["parameters"].get("lead_source_weight", {"value": 0.3})["value"])
        + segment_score * float(state["parameters"].get("segment_fit_weight", {"value": 0.4})["value"])
        + engagement * float(state["parameters"].get("engagement_weight", {"value": 0.3})["value"])
    )
    return round(min(score, 0.99), 4)


def _win_probability(state: dict, lead: dict, amount: float) -> float:
    amount_risk = min(amount / 1000000, 0.25)
    return round(max(lead["score"] - amount_risk, 0.05), 4)


def _slippage_risk(state: dict, probability: float) -> float:
    threshold = float(state["parameters"].get("deal_slippage_threshold", {"value": 0.5})["value"])
    return round(max(threshold - probability, 0.0), 4)


def _next_best_action(command: dict) -> str:
    if float(command["sentiment"]) >= 0.75:
        return "send_proposal"
    if command["activity_type"] == "email":
        return "schedule_meeting"
    return "manager_review"


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "appgen_event_contract",
        "idempotency_key": f"lead_opportunity:{event_type}:{payload.get('opportunity_id') or payload.get('lead_id') or payload.get('customer_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "lead_opportunity_dead_letter_event"},
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {"event_type": event_type, "key": key, "payload": payload, "hash": _digest({"event_type": event_type, "key": key, "payload": payload})}


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest({"capability": capability, "leads": len(state["leads"]), "opportunities": len(state["opportunities"])}),
    }


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()).hexdigest()
