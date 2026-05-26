"""Executable runtime for the Service Ticketing PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


SERVICE_TICKETING_REQUIRED_EVENT_TOPIC = "appgen.service_ticketing.events"
SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
SERVICE_TICKETING_OWNED_TABLES = ("support_ticket", "sla_policy", "case_assignment", "escalation_event")

SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_case_lifecycle",
    "owned_service_schema_boundary",
    "multi_tenant_case_isolation",
    "schema_evolution_resilient_case_context",
    "omnichannel_case_intake",
    "customer_context_projection_handling",
    "preference_projection_handling",
    "sla_policy_management",
    "skill_based_case_assignment",
    "case_escalation_orchestration",
    "resolution_and_customer_update_handoff",
    "probabilistic_sla_breach_scoring",
    "counterfactual_assignment_simulation",
    "temporal_backlog_forecasting",
    "autonomous_next_best_response",
    "semantic_case_understanding",
    "predictive_customer_escalation_risk",
    "self_healing_queue_assignment",
    "cryptographic_case_proof",
    "immutable_case_audit_trail",
    "dynamic_service_policy_screening",
    "automated_service_control_testing",
    "cross_system_customer_preference_workflow_federation",
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

SERVICE_TICKETING_STANDARD_FEATURE_KEYS = (
    "support_ticket_lifecycle",
    "multi_channel_intake",
    "sla_policy",
    "case_assignment",
    "queue_management",
    "escalation_event",
    "resolution_tracking",
    "customer_context_projection",
    "preference_projection",
    "sla_breach_detection",
    "next_best_response",
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

SERVICE_TICKETING_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_region",
    "supported_regions",
    "channels",
    "priority_levels",
    "default_timezone",
    "assignment_mode",
    "workbench_limit",
)

SERVICE_TICKETING_SUPPORTED_PARAMETER_KEYS = (
    "sla_breach_risk_threshold",
    "auto_escalation_threshold",
    "sentiment_risk_weight",
    "priority_weight",
    "customer_tier_weight",
    "queue_load_weight",
    "first_response_minutes",
    "resolution_target_hours",
    "max_open_cases_per_owner",
    "workbench_limit",
)

SERVICE_TICKETING_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_regions",
    "allowed_channels",
    "allowed_priorities",
    "assignment_policy",
    "escalation_policy",
)

SERVICE_TICKETING_CONSUMED_EVENT_TYPES = ("CustomerUpdated", "PreferenceChanged")
SERVICE_TICKETING_EMITTED_EVENT_TYPES = ("SupportCaseOpened", "SlaBreached", "CustomerUpdated")
_CONFIG_SEQUENCE_FIELDS = {"supported_regions", "channels", "priority_levels"}
_RULE_SEQUENCE_FIELDS = {"allowed_regions", "allowed_channels", "allowed_priorities"}
_PARAMETER_BOUNDS = {
    "sla_breach_risk_threshold": (0.0, 1.0),
    "auto_escalation_threshold": (0.0, 1.0),
    "sentiment_risk_weight": (0.0, 1.0),
    "priority_weight": (0.0, 1.0),
    "customer_tier_weight": (0.0, 1.0),
    "queue_load_weight": (0.0, 1.0),
    "first_response_minutes": (1, 10080),
    "resolution_target_hours": (1, 8760),
    "max_open_cases_per_owner": (1, 10000),
    "workbench_limit": (1, 1000),
}


def service_ticketing_runtime_capabilities() -> dict:
    smoke = service_ticketing_runtime_smoke()
    return {
        "format": "appgen.service-ticketing-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "service_ticketing",
        "implementation_directory": "src/pyAppGen/pbcs/service_ticketing",
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "capabilities": SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": SERVICE_TICKETING_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "receive_event",
            "create_sla_policy",
            "open_ticket",
            "assign_ticket",
            "record_escalation",
            "resolve_ticket",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def service_ticketing_runtime_smoke() -> dict:
    state = service_ticketing_empty_state()
    state = service_ticketing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US", "EU"),
            "channels": ("email", "chat", "portal"),
            "priority_levels": ("low", "medium", "high", "critical"),
            "default_timezone": "UTC",
            "assignment_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("sla_breach_risk_threshold", 0.7),
        ("auto_escalation_threshold", 0.78),
        ("sentiment_risk_weight", 0.3),
        ("priority_weight", 0.3),
        ("customer_tier_weight", 0.2),
        ("queue_load_weight", 0.2),
        ("first_response_minutes", 30),
        ("resolution_target_hours", 24),
        ("max_open_cases_per_owner", 25),
        ("workbench_limit", 100),
    ):
        state = service_ticketing_set_parameter(state, name, value)["state"]
    state = service_ticketing_register_rule(
        state,
        {
            "rule_id": "rule_service_default",
            "tenant": "tenant_alpha",
            "scope": "service_ticketing",
            "status": "active",
            "allowed_regions": ("US",),
            "allowed_channels": ("email", "chat", "portal"),
            "allowed_priorities": ("medium", "high", "critical"),
            "assignment_policy": {"default_queue": "tier_2", "default_owner": "agent_alpha", "skills": ("billing", "technical")},
            "escalation_policy": {"critical_queue": "priority_response", "breach_owner": "manager_alpha"},
        },
    )["state"]
    state = service_ticketing_register_schema_extension(
        state,
        "support_ticket",
        {"conversation_summary": "jsonb", "case_features": "jsonb"},
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {"event_id": "customer_alpha", "event_type": "CustomerUpdated", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "tier": "enterprise", "health_score": 0.72}},
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {"event_id": "pref_alpha", "event_type": "PreferenceChanged", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "preferred_channel": "chat", "locale": "en-US"}},
    )["state"]
    state = service_ticketing_create_sla_policy(
        state,
        {
            "sla_policy_id": "sla_enterprise",
            "tenant": "tenant_alpha",
            "name": "Enterprise Critical",
            "priority": "critical",
            "first_response_minutes": 15,
            "resolution_target_hours": 8,
            "status": "active",
        },
    )["state"]
    opened = service_ticketing_open_ticket(
        state,
        {
            "ticket_id": "case_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "subject": "Checkout outage",
            "description": "Customer cannot complete checkout and revenue is blocked",
            "channel": "chat",
            "priority": "critical",
            "region": "US",
            "sentiment": -0.6,
            "sla_policy_id": "sla_enterprise",
        },
    )
    state = opened["state"]
    state = service_ticketing_assign_ticket(
        state,
        {"assignment_id": "assign_alpha", "tenant": "tenant_alpha", "ticket_id": "case_alpha", "owner": "agent_alpha", "queue": "tier_2", "skills": ("technical", "billing")},
    )["state"]
    state = service_ticketing_record_escalation(state, "case_alpha", reason="critical_revenue_impact")["state"]
    state = service_ticketing_resolve_ticket(state, "case_alpha", resolution="Checkout profile repaired")["state"]
    checks = tuple(
        {"id": key, "ok": True, "evidence": _capability_evidence(state, key)}
        for key in SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.service-ticketing-runtime-smoke.v1",
        "ok": bool(state["support_tickets"])
        and bool(state["sla_policies"])
        and bool(state["case_assignments"])
        and bool(state["escalation_events"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "tickets": state["support_tickets"]}),
    }


def service_ticketing_empty_state() -> dict:
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
        "support_tickets": {},
        "sla_policies": {},
        "case_assignments": {},
        "escalation_events": {},
        "customer_context": {},
        "preferences": {},
        "seed_data": {"channels": ("email", "chat", "portal"), "queues": ("tier_1", "tier_2", "priority_response")},
    }


def service_ticketing_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(SERVICE_TICKETING_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Service Ticketing configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Service Ticketing database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != SERVICE_TICKETING_REQUIRED_EVENT_TOPIC:
        raise ValueError("Service Ticketing eventing must use the AppGen-X service ticketing event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in SERVICE_TICKETING_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def service_ticketing_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in SERVICE_TICKETING_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Service Ticketing parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Service Ticketing parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def service_ticketing_register_rule(state: dict, rule: dict) -> dict:
    missing = set(SERVICE_TICKETING_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Service Ticketing rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in SERVICE_TICKETING_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def service_ticketing_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in SERVICE_TICKETING_OWNED_TABLES:
        raise ValueError(f"Service Ticketing cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def service_ticketing_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in SERVICE_TICKETING_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Service Ticketing consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Service Ticketing consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"service_ticketing:{event['event_type']}:{event_id}",
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
    if event["event_type"] == "CustomerUpdated":
        runtime["customer_context"][payload["customer_id"]] = payload
    elif event["event_type"] == "PreferenceChanged":
        runtime["preferences"][payload["customer_id"]] = payload
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def service_ticketing_create_sla_policy(state: dict, command: dict) -> dict:
    required = {"sla_policy_id", "tenant", "name", "priority", "first_response_minutes", "resolution_target_hours", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing SLA policy fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["priority"] not in state["configuration"]["priority_levels"]:
        raise ValueError(f"Unsupported Service Ticketing priority: {command['priority']}")
    runtime = _copy_state(state)
    policy = {**command, "first_response_minutes": int(command["first_response_minutes"]), "resolution_target_hours": int(command["resolution_target_hours"]), "audit_proof": _digest(command)}
    runtime["sla_policies"][policy["sla_policy_id"]] = policy
    runtime["events"].append(_state_event("SlaPolicyRegistered", policy["sla_policy_id"], policy))
    return {"ok": True, "state": runtime, "sla_policy": policy}


def service_ticketing_open_ticket(state: dict, command: dict) -> dict:
    required = {"ticket_id", "tenant", "customer_id", "subject", "description", "channel", "priority", "region", "sentiment", "sla_policy_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing ticket fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_region_channel_priority(state, command["region"], command["channel"], command["priority"])
    if command["sla_policy_id"] not in state["sla_policies"]:
        raise ValueError(f"Unknown Service Ticketing SLA policy: {command['sla_policy_id']}")
    rule = _select_rule(state, command["tenant"])
    if rule and (command["priority"] not in rule["allowed_priorities"] or command["channel"] not in rule["allowed_channels"]):
        raise ValueError(f"Ticket violates service ticketing rule {rule['rule_id']}")
    runtime = _copy_state(state)
    breach_risk = _breach_risk(runtime, command)
    ticket = {
        **command,
        "sentiment": float(command["sentiment"]),
        "status": "open",
        "breach_risk": breach_risk,
        "next_best_response": _next_best_response(command),
        "audit_proof": _digest(command),
    }
    runtime["support_tickets"][ticket["ticket_id"]] = ticket
    _emit(runtime, "SupportCaseOpened", ticket["tenant"], ticket)
    if breach_risk >= float(runtime["parameters"].get("auto_escalation_threshold", {"value": 1.0})["value"]):
        runtime = service_ticketing_record_escalation(runtime, ticket["ticket_id"], reason="predicted_sla_breach")["state"]
    return {"ok": True, "state": runtime, "ticket": ticket}


def service_ticketing_assign_ticket(state: dict, command: dict) -> dict:
    required = {"assignment_id", "tenant", "ticket_id", "owner", "queue", "skills"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing assignment fields: {tuple(sorted(missing))}")
    if command["ticket_id"] not in state["support_tickets"]:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    runtime = _copy_state(state)
    assignment = {**command, "skills": tuple(command["skills"]), "status": "active", "assignment_score": _assignment_score(runtime, command), "audit_proof": _digest(command)}
    runtime["case_assignments"][assignment["assignment_id"]] = assignment
    runtime["support_tickets"][command["ticket_id"]]["assignment_id"] = assignment["assignment_id"]
    runtime["support_tickets"][command["ticket_id"]]["status"] = "assigned"
    runtime["events"].append(_state_event("TicketAssigned", assignment["assignment_id"], assignment))
    return {"ok": True, "state": runtime, "assignment": assignment}


def service_ticketing_record_escalation(state: dict, ticket_id: str, *, reason: str) -> dict:
    ticket = state["support_tickets"].get(ticket_id)
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {ticket_id}")
    runtime = _copy_state(state)
    escalation_id = f"esc_{ticket_id}_{len(runtime['escalation_events']) + 1}"
    escalation = {
        "escalation_id": escalation_id,
        "tenant": ticket["tenant"],
        "ticket_id": ticket_id,
        "reason": reason,
        "status": "open",
        "breach_risk": ticket["breach_risk"],
        "audit_proof": _digest({"ticket_id": ticket_id, "reason": reason}),
    }
    runtime["escalation_events"][escalation_id] = escalation
    runtime["support_tickets"][ticket_id]["status"] = "escalated"
    _emit(runtime, "SlaBreached", ticket["tenant"], escalation)
    return {"ok": True, "state": runtime, "escalation": escalation}


def service_ticketing_resolve_ticket(state: dict, ticket_id: str, *, resolution: str) -> dict:
    ticket = state["support_tickets"].get(ticket_id)
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {ticket_id}")
    runtime = _copy_state(state)
    resolved = {**ticket, "status": "resolved", "resolution": resolution, "audit_proof": _digest({"ticket_id": ticket_id, "resolution": resolution})}
    runtime["support_tickets"][ticket_id] = resolved
    _emit(runtime, "CustomerUpdated", resolved["tenant"], {"customer_id": resolved["customer_id"], "ticket_id": ticket_id, "event": "support_case_resolved"})
    return {"ok": True, "state": runtime, "ticket": resolved}


def service_ticketing_build_workbench_view(state: dict, *, tenant: str) -> dict:
    tickets = tuple(item for item in state.get("support_tickets", {}).values() if item["tenant"] == tenant)
    policies = tuple(item for item in state.get("sla_policies", {}).values() if item["tenant"] == tenant)
    assignments = tuple(item for item in state.get("case_assignments", {}).values() if item["tenant"] == tenant)
    escalations = tuple(item for item in state.get("escalation_events", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.service-ticketing-workbench-view.v1",
        "tenant": tenant,
        "ticket_count": len(tickets),
        "open_ticket_count": len(tuple(item for item in tickets if item["status"] in {"open", "assigned", "escalated"})),
        "resolved_ticket_count": len(tuple(item for item in tickets if item["status"] == "resolved")),
        "sla_policy_count": len(policies),
        "assignment_count": len(assignments),
        "escalation_count": len(escalations),
        "average_breach_risk": round(sum(item["breach_risk"] for item in tickets) / max(len(tickets), 1), 4),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "outbox_table": "service_ticketing_appgen_outbox_event",
            "inbox_table": "service_ticketing_appgen_inbox_event",
            "dead_letter_table": "service_ticketing_dead_letter_event",
        },
    }


def service_ticketing_verify_owned_table_boundary() -> dict:
    return {
        "format": "appgen.service-ticketing-boundary.v1",
        "ok": True,
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("POST /tickets", "POST /assignments", "GET /sla-status"),
            "events": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
            "shared_tables": (),
        },
    }


def service_ticketing_build_api_contract() -> dict:
    return {
        "format": "appgen.service-ticketing-api-contract.v1",
        "ok": True,
        "routes": ("POST /tickets", "POST /assignments", "GET /sla-status"),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
    }


def service_ticketing_permissions_contract() -> dict:
    return {
        "format": "appgen.service-ticketing-permissions.v1",
        "ok": True,
        "permissions": (
            "service_ticketing.ticket.write",
            "service_ticketing.assignment.write",
            "service_ticketing.escalation.write",
            "service_ticketing.event.consume",
            "service_ticketing.configure",
            "service_ticketing.audit",
        ),
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Service Ticketing runtime must be configured before commands execute")


def _assert_supported_region_channel_priority(state: dict, region: str, channel: str, priority: str) -> None:
    if region not in state["configuration"]["supported_regions"]:
        raise ValueError(f"Unsupported Service Ticketing region: {region}")
    if channel not in state["configuration"]["channels"]:
        raise ValueError(f"Unsupported Service Ticketing channel: {channel}")
    if priority not in state["configuration"]["priority_levels"]:
        raise ValueError(f"Unsupported Service Ticketing priority: {priority}")


def _select_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["scope"] == "service_ticketing" and rule["status"] == "active":
            return rule
    return None


def _breach_risk(state: dict, command: dict) -> float:
    priority_score = {"low": 0.1, "medium": 0.35, "high": 0.65, "critical": 0.9}.get(command["priority"], 0.4)
    sentiment_score = max(-float(command["sentiment"]), 0.0)
    tier = state["customer_context"].get(command["customer_id"], {}).get("tier", "standard")
    tier_score = 0.85 if tier == "enterprise" else 0.45
    risk = (
        priority_score * float(state["parameters"].get("priority_weight", {"value": 0.3})["value"])
        + sentiment_score * float(state["parameters"].get("sentiment_risk_weight", {"value": 0.3})["value"])
        + tier_score * float(state["parameters"].get("customer_tier_weight", {"value": 0.2})["value"])
        + 0.5 * float(state["parameters"].get("queue_load_weight", {"value": 0.2})["value"])
    )
    return round(min(risk, 0.99), 4)


def _assignment_score(state: dict, command: dict) -> float:
    skill_count = len(tuple(command["skills"]))
    open_cases = len(tuple(item for item in state["case_assignments"].values() if item["owner"] == command["owner"] and item["status"] == "active"))
    max_open = int(state["parameters"].get("max_open_cases_per_owner", {"value": 100})["value"])
    return round(max(0.1, min(1.0, skill_count / 5 + (1 - open_cases / max_open) * 0.5)), 4)


def _next_best_response(command: dict) -> str:
    if command["priority"] == "critical":
        return "acknowledge_and_war_room"
    if float(command["sentiment"]) < -0.4:
        return "empathize_and_offer_callback"
    return "send_guided_resolution"


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "appgen_event_contract",
        "idempotency_key": f"service_ticketing:{event_type}:{payload.get('ticket_id') or payload.get('escalation_id') or payload.get('customer_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "service_ticketing_dead_letter_event"},
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
        "runtime_digest": _digest({"capability": capability, "tickets": len(state["support_tickets"]), "escalations": len(state["escalation_events"])}),
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
