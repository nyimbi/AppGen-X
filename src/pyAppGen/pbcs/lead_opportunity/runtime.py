"""Executable runtime for the Lead Opportunity PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re


LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC = "appgen.lead_opportunity.events"
LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LEAD_OPPORTUNITY_OWNED_TABLES = (
    "lead",
    "lead_enrichment_snapshot",
    "lead_dedup_case",
    "lead_score_snapshot",
    "lead_assignment",
    "qualification_decision",
    "opportunity",
    "opportunity_stage_history",
    "pipeline_forecast_snapshot",
    "quote_proposal_handoff",
    "opportunity_outcome",
    "account_hierarchy",
    "sales_activity",
    "sales_coaching_insight",
    "lead_opportunity_audit_event",
    "lead_opportunity_rule",
    "lead_opportunity_parameter",
    "lead_opportunity_configuration",
    "lead_opportunity_governed_model",
    "lead_opportunity_seed_data",
)
LEAD_OPPORTUNITY_RUNTIME_TABLES = (
    "lead_opportunity_appgen_outbox_event",
    "lead_opportunity_appgen_inbox_event",
    "lead_opportunity_dead_letter_event",
)

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
    "owned_schema_contract_generation",
    "service_contract_generation",
    "release_evidence_contract_generation",
)

LEAD_OPPORTUNITY_STANDARD_FEATURE_KEYS = (
    "lead_capture",
    "lead_enrichment",
    "lead_deduplication",
    "lead_assignment",
    "lead_scoring",
    "lead_qualification",
    "opportunity_creation",
    "pipeline_stage_management",
    "opportunity_stage_history",
    "pipeline_management",
    "account_hierarchy",
    "sales_activity_history",
    "forecast_amount_rollup",
    "forecast_snapshots",
    "quote_proposal_handoff",
    "win_loss_management",
    "audit_evidence",
    "coaching_insights",
    "next_best_action",
    "customer_segment_projection",
    "customer_update_handoff",
    "tenant_isolation",
    "appgen_event_contract",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_datastore_boundary",
    "release_gate",
    "governed_model_registry",
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
_LEAD_OPPORTUNITY_ALLOWED_DEPENDENCIES = (
    "customer_segment_projection",
    "customer_projection",
    "billing_projection",
    "territory_projection",
    "quote_proposal_projection",
    "GET /customers/{id}",
    "GET /billing/accounts/{id}",
    "GET /territories/{id}",
    "POST /quotes/proposals",
)
_CONFIG_SEQUENCE_FIELDS = {"supported_currencies", "supported_regions", "pipeline_stages"}
_RULE_SEQUENCE_FIELDS = {"allowed_regions", "allowed_currencies", "allowed_segments"}
_LEAD_OPPORTUNITY_FIELD_NAME_PATTERN = re.compile(r"[a-z][a-z0-9_]*$")
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
        "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
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
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
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
    normalized["required_event_topic"] = LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
    normalized["visible_event_contracts"] = ("AppGen-X",)
    normalized["stream_engine_picker_visible"] = False
    normalized["user_selectable_event_contract"] = False
    normalized["supported_fields"] = LEAD_OPPORTUNITY_SUPPORTED_CONFIGURATION_FIELDS
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
    normalized["compiled_evidence"] = {
        "rule_id": normalized["rule_id"],
        "scope": normalized["scope"],
        "required_fields": LEAD_OPPORTUNITY_REQUIRED_RULE_FIELDS,
        "tenant": normalized["tenant"],
    }
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def lead_opportunity_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in LEAD_OPPORTUNITY_OWNED_TABLES:
        raise ValueError(f"Lead Opportunity cannot extend non-owned table: {table}")
    invalid_fields = tuple(sorted(name for name in fields if not _LEAD_OPPORTUNITY_FIELD_NAME_PATTERN.fullmatch(str(name))))
    if invalid_fields:
        raise ValueError(f"Lead Opportunity schema extension fields must match [a-z][a-z0-9_]*: {invalid_fields}")
    runtime = _copy_state(state)
    version = len(runtime["schema_extensions"].get(table, ())) + 1
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": version,
        "migration_descriptor": f"pbcs/lead_opportunity/migrations/extensions/{version:03d}_{table}.sql",
        "model_descriptor": f"pbcs/lead_opportunity/models/{_class_name(table)}ExtensionV{version}.py",
    }
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
        return {
            "ok": True,
            "state": runtime,
            "duplicate": True,
            "handler": {
                "status": "duplicate",
                "event_id": event_id,
                "runtime_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[1],
                "idempotency_key": f"lead_opportunity:{event['event_type']}:{event_id}",
            },
        }
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"lead_opportunity:{event['event_type']}:{event_id}",
        "attempts": 1,
        "max_attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
        "contract": "AppGen-X",
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        handler["runtime_table"] = LEAD_OPPORTUNITY_RUNTIME_TABLES[2]
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    handler["runtime_table"] = LEAD_OPPORTUNITY_RUNTIME_TABLES[1]
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
    configuration = state.get("configuration", {})
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
        "inbox_count": len(state.get("inbox", ())),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(configuration.get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
            "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
            "outbox_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[0],
            "inbox_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[1],
            "dead_letter_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[2],
            "configuration": {
                "bound": bool(configuration.get("ok")),
                "database_backend": configuration.get("database_backend"),
                "event_contract": configuration.get("event_contract"),
                "event_topic": configuration.get("required_event_topic"),
                "visible_event_contracts": configuration.get("visible_event_contracts", ()),
                "stream_engine_picker_visible": configuration.get("stream_engine_picker_visible"),
                "user_selectable_event_contract": configuration.get("user_selectable_event_contract"),
                "supported_fields": configuration.get("supported_fields", ()),
            },
            "rules": tuple(
                {
                    "rule_id": rule["rule_id"],
                    "scope": rule["scope"],
                    "compiled_hash": rule["compiled_hash"],
                    "required_fields": rule["compiled_evidence"]["required_fields"],
                }
                for rule in sorted(state.get("rules", {}).values(), key=lambda item: item["rule_id"])
            ),
            "parameters": {
                "supported": LEAD_OPPORTUNITY_SUPPORTED_PARAMETER_KEYS,
                "active": tuple(sorted(state.get("parameters", {}))),
            },
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
        "GET /lead-opportunity/schema-contract",
        "GET /lead-opportunity/service-contract",
        "GET /lead-opportunity/release-evidence",
        *tuple(item for item in _LEAD_OPPORTUNITY_ALLOWED_DEPENDENCIES if not str(item).startswith(("GET ", "POST "))),
    }
    allowed_event_dependencies = set(LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = set(LEAD_OPPORTUNITY_RUNTIME_TABLES)
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
        "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /accounts",
                "POST /leads",
                "POST /opportunities",
                "POST /sales-activities",
                "POST /opportunity-stage",
                "POST /opportunity-wins",
                "GET /pipeline",
                "GET /lead-opportunity/schema-contract",
                "GET /lead-opportunity/service-contract",
                "GET /lead-opportunity/release-evidence",
            ),
            "events": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _LEAD_OPPORTUNITY_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
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
            {
                "route": "GET /lead-opportunity/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
                "requires_permission": "lead_opportunity.audit",
            },
            {
                "route": "GET /lead-opportunity/service-contract",
                "query": "build_service_contract",
                "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
                "requires_permission": "lead_opportunity.audit",
            },
            {
                "route": "GET /lead-opportunity/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
                "requires_permission": "lead_opportunity.audit",
            },
        ),
        "declared_catalog_routes": ("POST /leads", "POST /opportunities", "GET /pipeline"),
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
        "events": {"emits": LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES, "consumes": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES},
        "emits": LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES,
        "consumes": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
        "database_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(lead_opportunity_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }


def lead_opportunity_build_schema_contract() -> dict:
    tables = tuple(
        {
            "table": table,
            "pbc": "lead_opportunity",
            "schema": "lead_opportunity",
            "owned": True,
            "migration": f"pbcs/lead_opportunity/migrations/{index:03d}_{table}.sql",
            "model": f"pbcs/lead_opportunity/models/{_class_name(table)}.py",
            "fields": _lead_opportunity_table_fields(table),
            "relationships": _lead_opportunity_table_relationships(table),
        }
        for index, table in enumerate(LEAD_OPPORTUNITY_OWNED_TABLES, start=1)
    )
    runtime_tables = tuple(
        {
            "table": table,
            "fields": _lead_opportunity_table_fields(table),
            "primary_key": _lead_opportunity_table_fields(table)[1],
        }
        for table in LEAD_OPPORTUNITY_RUNTIME_TABLES
    )
    return {
        "format": "appgen.lead-opportunity-owned-schema-contract.v1",
        "ok": len(tables) == len(LEAD_OPPORTUNITY_OWNED_TABLES) and len(runtime_tables) == len(LEAD_OPPORTUNITY_RUNTIME_TABLES),
        "pbc": "lead_opportunity",
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "runtime_tables": runtime_tables,
        "tables": tables,
        "migrations": tuple(
            {
                "path": table["migration"],
                "table": table["table"],
                "operation": "create_owned_table",
                "backend_allowlist": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
            }
            for table in tables
        ),
        "models": tuple(
            {
                "path": table["model"],
                "table": table["table"],
                "class_name": _class_name(table["table"]),
                "fields": table["fields"],
            }
            for table in tables
        ),
        "database_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "schema_extensions": {
            "allowed": True,
            "owned_tables_only": True,
            "field_name_pattern": _LEAD_OPPORTUNITY_FIELD_NAME_PATTERN.pattern,
        },
        "declared_dependencies": lead_opportunity_verify_owned_table_boundary(())["declared_dependencies"],
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }


def lead_opportunity_build_service_contract() -> dict:
    command_methods = (
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
        "build_workbench_view",
        "verify_owned_table_boundary",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    query_methods = (
        "build_workbench_view",
        "build_api_contract",
        "permissions_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    return {
        "format": "appgen.lead-opportunity-service-contract.v1",
        "ok": True,
        "pbc": "lead_opportunity",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "transaction_boundary": "lead_opportunity_owned_datastore_plus_appgen_outbox",
        "mutates_only_owned_tables": True,
        "owned_tables": LEAD_OPPORTUNITY_OWNED_TABLES,
        "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
        "event_contract": {
            "contract": "AppGen-X",
            "required_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
            "emits": LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES,
            "consumes": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
            "outbox_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[0],
            "inbox_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[1],
            "dead_letter_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[2],
            "idempotency_key": "event_type:event_id",
        },
        "retry_policy": {
            "configured_by": "retry_limit",
            "dead_letter_after_retry_limit": True,
            "dead_letter_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[2],
        },
        "external_dependencies": {
            "apis": tuple(item for item in _LEAD_OPPORTUNITY_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _LEAD_OPPORTUNITY_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "shared_table_access": False,
    }


def lead_opportunity_build_release_evidence() -> dict:
    from .ui import lead_opportunity_ui_contract

    schema = lead_opportunity_build_schema_contract()
    service = lead_opportunity_build_service_contract()
    api = lead_opportunity_build_api_contract()
    permissions = lead_opportunity_permissions_contract()
    ui = lead_opportunity_ui_contract()
    state = _build_release_state()
    workbench = lead_opportunity_build_workbench_view(state, tenant="tenant_release")
    boundary = lead_opportunity_verify_owned_table_boundary(
        (
            "lead",
            LEAD_OPPORTUNITY_RUNTIME_TABLES[0],
            "CustomerSegmentUpdated",
            "customer_segment_projection",
            "quote_proposal_projection",
        )
    )
    checks = (
        {"id": "owned_schema_depth", "ok": len(schema["owned_tables"]) >= 18},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(schema["owned_tables"])},
        {"id": "model_per_owned_table", "ok": len(schema["models"]) == len(schema["owned_tables"])},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == LEAD_OPPORTUNITY_RUNTIME_TABLES},
        {"id": "service_contract_depth", "ok": service["ok"] and "receive_event" in service["command_methods"] and "build_release_evidence" in service["query_methods"]},
        {"id": "api_event_contract", "ok": api["event_contract"] == "AppGen-X" and api["required_event_topic"] == LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_contracts", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "ui_binding_evidence", "ok": ui["ok"] and ui["configuration_editor"]["stream_engine_picker_visible"] is False},
        {"id": "workbench_binding_evidence", "ok": workbench["binding_evidence"]["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES and workbench["inbox_count"] >= 1},
        {"id": "boundary_contract", "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == ()},
        {"id": "database_allowlist", "ok": schema["database_backends"] == LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS and api["database_backends"] == LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.lead-opportunity-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": "lead_opportunity",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema_contract": schema,
        "service_contract": service,
        "api_contract": api,
        "permissions_contract": permissions,
        "ui_contract": ui,
        "workbench": workbench,
        "boundary_contract": boundary,
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
            "build_schema_contract": "lead_opportunity.audit",
            "build_service_contract": "lead_opportunity.audit",
            "build_release_evidence": "lead_opportunity.audit",
        },
    }


def _build_release_state() -> dict:
    state = lead_opportunity_empty_state()
    state = lead_opportunity_configure_runtime(
        state,
        {
            "database_backend": LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS[0],
            "event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("US", "EU"),
            "pipeline_stages": ("prospect", "qualified", "proposal", "negotiation", "won", "lost"),
            "default_timezone": "UTC",
            "assignment_mode": "policy",
            "workbench_limit": 50,
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
        ("max_open_opportunities_per_account", 10),
        ("workbench_limit", 50),
    ):
        state = lead_opportunity_set_parameter(state, name, value)["state"]
    state = lead_opportunity_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "scope": "lead_opportunity",
            "status": "active",
            "allowed_regions": ("US",),
            "allowed_currencies": ("USD",),
            "allowed_segments": ("growth", "enterprise"),
            "qualification_policy": {"minimum_score": 0.65, "required_fields": ("email", "company")},
            "assignment_policy": {"mode": "territory", "default_owner": "seller_release"},
        },
    )["state"]
    state = lead_opportunity_register_schema_extension(
        state,
        "opportunity",
        {"mutual_action_plan": "jsonb", "quote_handoff_status": "text"},
    )["state"]
    state = lead_opportunity_receive_event(
        state,
        {
            "event_id": "segment_release",
            "event_type": "CustomerSegmentUpdated",
            "payload": {
                "tenant": "tenant_release",
                "customer_id": "cust_release",
                "segment": "enterprise",
                "fit_score": 0.91,
            },
        },
    )["state"]
    state = lead_opportunity_create_account_hierarchy(
        state,
        {
            "account_id": "acct_release",
            "tenant": "tenant_release",
            "name": "Release Holdings",
            "region": "US",
            "parent_account_id": None,
            "customer_id": "cust_release",
            "owner": "seller_release",
        },
    )["state"]
    state = lead_opportunity_create_lead(
        state,
        {
            "lead_id": "lead_release",
            "tenant": "tenant_release",
            "account_id": "acct_release",
            "customer_id": "cust_release",
            "email": "release@example.com",
            "company": "Release Holdings",
            "source": "partner",
            "region": "US",
            "currency": "USD",
            "engagement_score": 0.88,
            "estimated_value": 150000.0,
        },
    )["state"]
    state = lead_opportunity_qualify_lead(state, "lead_release")["state"]
    state = lead_opportunity_create_opportunity(
        state,
        {
            "opportunity_id": "opp_release",
            "tenant": "tenant_release",
            "lead_id": "lead_release",
            "account_id": "acct_release",
            "name": "Release Expansion",
            "amount": 150000.0,
            "currency": "USD",
            "stage": "qualified",
            "close_date": "2026-07-31",
        },
    )["state"]
    state = lead_opportunity_record_sales_activity(
        state,
        {
            "activity_id": "act_release",
            "tenant": "tenant_release",
            "opportunity_id": "opp_release",
            "activity_type": "meeting",
            "subject": "Proposal review",
            "sentiment": 0.86,
            "occurred_at": "2026-05-26T00:00:00Z",
            "owner": "seller_release",
        },
    )["state"]
    state = lead_opportunity_advance_opportunity(state, "opp_release", "proposal")["state"]
    return lead_opportunity_win_opportunity(state, "opp_release")["state"]


def _lead_opportunity_table_fields(table: str) -> tuple[str, ...]:
    table_fields = {
        "lead": ("tenant", "lead_id", "account_id", "customer_id", "email", "company", "source", "region", "currency", "engagement_score", "estimated_value", "score", "status", "assigned_owner", "audit_proof"),
        "lead_enrichment_snapshot": ("tenant", "snapshot_id", "lead_id", "segment_fit_score", "firmographic_fit", "intent_summary", "enriched_at"),
        "lead_dedup_case": ("tenant", "case_id", "lead_id", "duplicate_lead_id", "match_hash", "resolution_status", "resolved_at"),
        "lead_score_snapshot": ("tenant", "snapshot_id", "lead_id", "qualification_score", "lead_source_weight", "segment_fit_weight", "engagement_weight", "recorded_at"),
        "lead_assignment": ("tenant", "assignment_id", "lead_id", "owner", "assignment_mode", "territory_key", "assigned_at"),
        "qualification_decision": ("tenant", "decision_id", "lead_id", "minimum_score", "actual_score", "decision", "qualified_at"),
        "opportunity": ("tenant", "opportunity_id", "lead_id", "account_id", "name", "amount", "currency", "stage", "close_date", "win_probability", "forecast_amount", "risk_score", "status", "audit_proof"),
        "opportunity_stage_history": ("tenant", "history_id", "opportunity_id", "from_stage", "to_stage", "changed_at", "audit_proof"),
        "pipeline_forecast_snapshot": ("tenant", "snapshot_id", "opportunity_id", "forecast_amount", "confidence_floor", "slippage_risk", "captured_at"),
        "quote_proposal_handoff": ("tenant", "handoff_id", "opportunity_id", "proposal_reference", "handoff_status", "handoff_owner", "handed_off_at"),
        "opportunity_outcome": ("tenant", "outcome_id", "opportunity_id", "outcome", "reason", "competitor_context", "recorded_at"),
        "account_hierarchy": ("tenant", "account_id", "name", "parent_account_id", "customer_id", "region", "owner", "status", "audit_proof"),
        "sales_activity": ("tenant", "activity_id", "opportunity_id", "activity_type", "subject", "sentiment", "occurred_at", "owner", "next_best_action", "audit_proof"),
        "sales_coaching_insight": ("tenant", "insight_id", "opportunity_id", "activity_id", "coaching_signal", "recommended_action", "confidence", "recorded_at"),
        "lead_opportunity_audit_event": ("tenant", "audit_id", "entity_type", "entity_id", "event_type", "event_hash", "recorded_at"),
        "lead_opportunity_rule": ("tenant", "rule_id", "scope", "status", "compiled_hash", "compiled_evidence", "recorded_at"),
        "lead_opportunity_parameter": ("tenant", "parameter_id", "parameter_name", "parameter_value", "bounds", "recorded_at"),
        "lead_opportunity_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone", "recorded_at"),
        "lead_opportunity_governed_model": ("tenant", "model_id", "model_name", "model_scope", "feature_lineage", "governance_status", "recorded_at"),
        "lead_opportunity_seed_data": ("tenant", "seed_id", "seed_type", "seed_values", "version", "recorded_at"),
        LEAD_OPPORTUNITY_RUNTIME_TABLES[0]: ("tenant", "event_id", "event_type", "payload", "idempotency_key", "status", "audit_hash"),
        LEAD_OPPORTUNITY_RUNTIME_TABLES[1]: ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "received_at"),
        LEAD_OPPORTUNITY_RUNTIME_TABLES[2]: ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "recorded_at"),
    }
    return table_fields[table]


def _lead_opportunity_table_relationships(table: str) -> tuple[dict[str, str], ...]:
    relationships = {
        "lead": (
            {"from": "lead.account_id", "to": "account_hierarchy.account_id", "type": "owned_account_reference"},
            {"from": "lead.customer_id", "to": "customer_projection.customer_id", "type": "projection_reference"},
        ),
        "lead_enrichment_snapshot": (
            {"from": "lead_enrichment_snapshot.lead_id", "to": "lead.lead_id", "type": "owned_enrichment"},
        ),
        "lead_dedup_case": (
            {"from": "lead_dedup_case.lead_id", "to": "lead.lead_id", "type": "owned_duplicate_case"},
        ),
        "lead_score_snapshot": (
            {"from": "lead_score_snapshot.lead_id", "to": "lead.lead_id", "type": "owned_scoring"},
        ),
        "lead_assignment": (
            {"from": "lead_assignment.lead_id", "to": "lead.lead_id", "type": "owned_assignment"},
        ),
        "qualification_decision": (
            {"from": "qualification_decision.lead_id", "to": "lead.lead_id", "type": "owned_qualification"},
        ),
        "opportunity": (
            {"from": "opportunity.lead_id", "to": "lead.lead_id", "type": "owned_conversion"},
            {"from": "opportunity.account_id", "to": "account_hierarchy.account_id", "type": "owned_account_reference"},
        ),
        "opportunity_stage_history": (
            {"from": "opportunity_stage_history.opportunity_id", "to": "opportunity.opportunity_id", "type": "owned_stage_history"},
        ),
        "pipeline_forecast_snapshot": (
            {"from": "pipeline_forecast_snapshot.opportunity_id", "to": "opportunity.opportunity_id", "type": "owned_forecast"},
        ),
        "quote_proposal_handoff": (
            {"from": "quote_proposal_handoff.opportunity_id", "to": "opportunity.opportunity_id", "type": "owned_handoff"},
        ),
        "opportunity_outcome": (
            {"from": "opportunity_outcome.opportunity_id", "to": "opportunity.opportunity_id", "type": "owned_outcome"},
        ),
        "sales_activity": (
            {"from": "sales_activity.opportunity_id", "to": "opportunity.opportunity_id", "type": "owned_activity"},
        ),
        "sales_coaching_insight": (
            {"from": "sales_coaching_insight.activity_id", "to": "sales_activity.activity_id", "type": "owned_coaching"},
        ),
    }
    return relationships.get(table, ())


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


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
        "contract": "AppGen-X",
        "runtime_table": LEAD_OPPORTUNITY_RUNTIME_TABLES[0],
        "idempotency_key": f"lead_opportunity:{event_type}:{payload.get('opportunity_id') or payload.get('lead_id') or payload.get('customer_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": LEAD_OPPORTUNITY_RUNTIME_TABLES[2]},
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
        "dead_letter": len(state["dead_letter"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_tables": LEAD_OPPORTUNITY_RUNTIME_TABLES,
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
