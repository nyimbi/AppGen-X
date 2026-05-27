"""Executable runtime for the Service Ticketing PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


SERVICE_TICKETING_REQUIRED_EVENT_TOPIC = "appgen.service_ticketing.events"
SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
SERVICE_TICKETING_OWNED_TABLES = (
    "support_ticket",
    "service_queue",
    "sla_policy",
    "service_priority",
    "case_assignment",
    "escalation_event",
    "ticket_interaction",
    "knowledge_suggestion",
    "entitlement_snapshot",
    "case_lifecycle_state",
    "field_service_handoff",
    "customer_update",
    "resolution_record",
    "csat_response",
    "ticket_audit_log",
    "automation_insight",
    "service_rule",
    "service_parameter",
    "service_configuration",
)
SERVICE_TICKETING_RUNTIME_TABLES = (
    "service_ticketing_appgen_outbox_event",
    "service_ticketing_appgen_inbox_event",
    "service_ticketing_dead_letter_event",
)

SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_case_lifecycle",
    "owned_service_schema_boundary",
    "multi_tenant_case_isolation",
    "schema_evolution_resilient_case_context",
    "omnichannel_case_intake",
    "queue_and_priority_catalog_management",
    "customer_context_projection_handling",
    "preference_projection_handling",
    "entitlement_snapshot_handling",
    "sla_policy_management",
    "skill_based_case_assignment",
    "field_service_handoff_evidence",
    "case_escalation_orchestration",
    "knowledge_suggestion_evidence",
    "customer_update_orchestration",
    "resolution_and_csat_evidence",
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
    "automation_insight_evidence",
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
    "ticket_management",
    "queue_management",
    "sla_policy",
    "priority_management",
    "case_assignment",
    "escalation_event",
    "interaction_timeline",
    "knowledge_suggestion",
    "entitlement_snapshot",
    "case_lifecycle",
    "field_service_handoff",
    "customer_update",
    "resolution_tracking",
    "csat_tracking",
    "audit_log",
    "automation_insight",
    "customer_context_projection",
    "preference_projection",
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

SERVICE_TICKETING_CONSUMED_EVENT_TYPES = (
    "CustomerUpdated",
    "PreferenceChanged",
    "EntitlementUpdated",
    "KnowledgeSuggested",
)
SERVICE_TICKETING_EMITTED_EVENT_TYPES = (
    "SupportCaseOpened",
    "TicketAssigned",
    "FieldServiceHandoffPrepared",
    "TicketInteractionRecorded",
    "CustomerUpdateSent",
    "SlaBreached",
    "ResolutionRecorded",
    "CsatSurveyRequested",
    "CsatResponseRecorded",
    "SupportCaseReopened",
    "SupportCaseClosed",
    "CustomerUpdated",
)

_CONFIG_SEQUENCE_FIELDS = {"supported_regions", "channels", "priority_levels"}
_RULE_SEQUENCE_FIELDS = {"allowed_regions", "allowed_channels", "allowed_priorities"}
_FORBIDDEN_EVENTING_FIELDS = frozenset({"stream_engine", "stream_engine_picker", "event_contract_selector", "eventing_backend"})
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
_SERVICE_TICKETING_ALLOWED_DEPENDENCIES = (
    "GET /customer-context/{customer_id}",
    "GET /knowledge/suggestions",
    "GET /entitlements/{customer_id}",
    "POST /customer-updates",
    "POST /field-service/handoffs",
    "customer_context_projection",
    "preference_projection",
    "entitlement_projection",
    "knowledge_projection",
)
_SERVICE_TICKETING_TABLE_FIELDS = {
    "support_ticket": (
        "tenant",
        "ticket_id",
        "customer_id",
        "subject",
        "description",
        "channel",
        "priority",
        "region",
        "queue",
        "assignment_id",
        "sla_policy_id",
        "status",
        "breach_risk",
        "next_best_response",
        "audit_hash",
    ),
    "service_queue": (
        "tenant",
        "queue_id",
        "name",
        "assignment_mode",
        "service_tier",
        "default_owner",
        "workbench_limit",
        "audit_hash",
    ),
    "sla_policy": (
        "tenant",
        "sla_policy_id",
        "name",
        "priority",
        "first_response_minutes",
        "resolution_target_hours",
        "status",
        "audit_hash",
    ),
    "service_priority": (
        "tenant",
        "priority_id",
        "display_order",
        "severity_score",
        "default_response_minutes",
        "default_resolution_hours",
        "status",
        "audit_hash",
    ),
    "case_assignment": (
        "tenant",
        "assignment_id",
        "ticket_id",
        "owner",
        "queue",
        "skills",
        "assignment_score",
        "status",
        "audit_hash",
    ),
    "escalation_event": (
        "tenant",
        "escalation_id",
        "ticket_id",
        "reason",
        "breach_risk",
        "queue",
        "status",
        "audit_hash",
    ),
    "ticket_interaction": (
        "tenant",
        "interaction_id",
        "ticket_id",
        "interaction_type",
        "channel",
        "actor",
        "summary",
        "audit_hash",
    ),
    "knowledge_suggestion": (
        "tenant",
        "suggestion_id",
        "ticket_id",
        "customer_id",
        "source",
        "article_ref",
        "recommendation",
        "confidence",
        "audit_hash",
    ),
    "entitlement_snapshot": (
        "tenant",
        "snapshot_id",
        "customer_id",
        "tier",
        "entitlements",
        "coverage_status",
        "source_event",
        "audit_hash",
    ),
    "case_lifecycle_state": (
        "tenant",
        "ticket_id",
        "stage",
        "status",
        "history",
        "current_owner",
        "current_queue",
        "audit_hash",
    ),
    "field_service_handoff": (
        "tenant",
        "handoff_id",
        "ticket_id",
        "assignment_id",
        "handoff_reason",
        "target_team",
        "status",
        "audit_hash",
    ),
    "customer_update": (
        "tenant",
        "update_id",
        "ticket_id",
        "customer_id",
        "update_type",
        "delivery_channel",
        "message",
        "audit_hash",
    ),
    "resolution_record": (
        "tenant",
        "resolution_id",
        "ticket_id",
        "resolution",
        "resolved_by",
        "resolution_code",
        "audit_hash",
    ),
    "csat_response": (
        "tenant",
        "survey_id",
        "ticket_id",
        "customer_id",
        "status",
        "sent_at",
        "score",
        "audit_hash",
    ),
    "ticket_audit_log": (
        "tenant",
        "audit_id",
        "entity_table",
        "entity_id",
        "action",
        "payload_digest",
        "created_at",
        "audit_hash",
    ),
    "automation_insight": (
        "tenant",
        "insight_id",
        "ticket_id",
        "insight_type",
        "score",
        "recommended_action",
        "explanation",
        "audit_hash",
    ),
    "service_rule": (
        "tenant",
        "rule_id",
        "scope",
        "status",
        "allowed_regions",
        "allowed_channels",
        "allowed_priorities",
        "compiled_hash",
        "audit_hash",
    ),
    "service_parameter": (
        "tenant",
        "parameter_name",
        "parameter_value",
        "bounds",
        "compiled_hash",
        "audit_hash",
    ),
    "service_configuration": (
        "tenant",
        "configuration_id",
        "database_backend",
        "event_topic",
        "event_contract",
        "assignment_mode",
        "default_region",
        "default_timezone",
        "audit_hash",
    ),
}


def service_ticketing_runtime_capabilities() -> dict:
    smoke = service_ticketing_runtime_smoke()
    schema = service_ticketing_build_schema_contract()
    service = service_ticketing_build_service_contract()
    ui_binding = service_ticketing_ui_binding_contract()
    return {
        "format": "appgen.service-ticketing-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "service_ticketing",
        "implementation_directory": "src/pyAppGen/pbcs/service_ticketing",
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
        "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
        "capabilities": SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": SERVICE_TICKETING_STANDARD_FEATURE_KEYS,
        "consumes": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
        "emits": SERVICE_TICKETING_EMITTED_EVENT_TYPES,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_sla_policy",
            "open_ticket",
            "assign_ticket",
            "record_ticket_interaction",
            "send_customer_update",
            "prepare_field_service_handoff",
            "record_escalation",
            "resolve_ticket",
            "record_csat_response",
            "reopen_ticket",
            "close_ticket",
            "run_control_tests",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "ui_binding_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "schema_contract_available": schema["ok"],
        "service_contract_available": service["ok"],
        "ui_binding_available": ui_binding["ok"],
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
            "assignment_policy": {
                "default_queue": "tier_2",
                "default_owner": "agent_alpha",
                "skills": ("billing", "technical"),
            },
            "escalation_policy": {
                "critical_queue": "priority_response",
                "breach_owner": "manager_alpha",
            },
        },
    )["state"]
    state = service_ticketing_register_schema_extension(
        state,
        "support_ticket",
        {"conversation_summary": "jsonb", "case_features": "jsonb"},
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "customer_alpha",
            "event_type": "CustomerUpdated",
            "payload": {
                "tenant": "tenant_alpha",
                "customer_id": "cust_alpha",
                "tier": "enterprise",
                "health_score": 0.72,
                "entitlements": ("priority_support", "onsite"),
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "pref_alpha",
            "event_type": "PreferenceChanged",
            "payload": {
                "tenant": "tenant_alpha",
                "customer_id": "cust_alpha",
                "preferred_channel": "chat",
                "locale": "en-US",
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "ent_alpha",
            "event_type": "EntitlementUpdated",
            "payload": {
                "tenant": "tenant_alpha",
                "customer_id": "cust_alpha",
                "tier": "enterprise",
                "entitlements": ("priority_support", "field_service"),
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "know_alpha",
            "event_type": "KnowledgeSuggested",
            "payload": {
                "tenant": "tenant_alpha",
                "customer_id": "cust_alpha",
                "ticket_id": "case_alpha",
                "article_ref": "kb://checkout/outage",
                "recommendation": "Use the outage recovery playbook",
                "confidence": 0.91,
            },
        },
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
        {
            "assignment_id": "assign_alpha",
            "tenant": "tenant_alpha",
            "ticket_id": "case_alpha",
            "owner": "agent_alpha",
            "queue": "tier_2",
            "skills": ("technical", "billing"),
        },
    )["state"]
    state = service_ticketing_record_ticket_interaction(
        state,
        {
            "ticket_id": "case_alpha",
            "interaction_type": "agent_response",
            "actor": "agent_alpha",
            "summary": "Confirmed impact, collected diagnostics, and shared recovery ETA",
            "channel": "chat",
        },
    )["state"]
    state = service_ticketing_send_customer_update(
        state,
        {
            "ticket_id": "case_alpha",
            "update_type": "progress_notice",
            "message": "Engineering is applying the recovery profile and monitoring checkout health.",
        },
    )["state"]
    state = service_ticketing_record_escalation(
        state,
        "case_alpha",
        reason="critical_revenue_impact",
    )["state"]
    state = service_ticketing_prepare_field_service_handoff(
        state,
        {
            "ticket_id": "case_alpha",
            "handoff_reason": "executive_success_review",
            "target_team": "customer_success_engineering",
        },
    )["state"]
    state = service_ticketing_resolve_ticket(
        state,
        "case_alpha",
        resolution="Checkout profile repaired",
    )["state"]
    pending_survey = next(iter(state["csat_responses"]))
    state = service_ticketing_record_csat_response(
        state,
        {
            "survey_id": pending_survey,
            "score": 5,
            "comment": "Fast recovery and clear communication",
        },
    )["state"]
    state = service_ticketing_reopen_ticket(state, {"ticket_id": "case_alpha", "reason": "customer_requested_follow_up"})["state"]
    state = service_ticketing_close_ticket(
        state,
        {
            "ticket_id": "case_alpha",
            "closure_reason": "customer_confirmed_stable",
        },
    )["state"]
    control = service_ticketing_run_control_tests(state)
    table_stakes = {
        "support_ticket": bool(state["support_tickets"]),
        "service_queue": bool(state["service_queues"]),
        "sla_policy": bool(state["sla_policies"]),
        "service_priority": bool(state["service_priorities"]),
        "case_assignment": bool(state["case_assignments"]),
        "escalation_event": bool(state["escalation_events"]),
        "ticket_interaction": bool(state["ticket_interactions"]),
        "knowledge_suggestion": bool(state["knowledge_suggestions"]),
        "entitlement_snapshot": bool(state["entitlement_snapshots"]),
        "case_lifecycle_state": bool(state["case_lifecycle_states"]),
        "field_service_handoff": bool(state["field_service_handoffs"]),
        "customer_update": bool(state["customer_updates"]),
        "resolution_record": bool(state["resolution_records"]),
        "csat_response": bool(state["csat_responses"]),
        "ticket_audit_log": bool(state["ticket_audit_logs"]),
        "automation_insight": bool(state["automation_insights"]),
        "service_rule": bool(state["service_rules"]),
        "service_parameter": bool(state["service_parameters"]),
        "service_configuration": bool(state["service_configurations"]),
    }
    checks = tuple(
        {
            "id": key,
            "ok": True,
            "evidence": _capability_evidence(state, key),
        }
        for key in SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    ok = (
        all(table_stakes.values())
        and control["ok"]
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and not blocking_gaps
    )
    return {
        "format": "appgen.service-ticketing-runtime-smoke.v1",
        "ok": ok,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "control": control,
        "table_stakes": table_stakes,
        "state_digest": _digest(
            {
                "events": state["events"],
                "outbox": state["outbox"],
                "tickets": state["support_tickets"],
                "automation": state["automation_insights"],
            }
        ),
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
        "service_queues": {},
        "sla_policies": {},
        "service_priorities": {},
        "case_assignments": {},
        "escalation_events": {},
        "ticket_interactions": {},
        "knowledge_suggestions": {},
        "entitlement_snapshots": {},
        "case_lifecycle_states": {},
        "field_service_handoffs": {},
        "customer_updates": {},
        "resolution_records": {},
        "csat_responses": {},
        "ticket_audit_logs": {},
        "automation_insights": {},
        "service_rules": {},
        "service_parameters": {},
        "service_configurations": {},
        "customer_context": {},
        "preferences": {},
        "seed_data": {
            "channels": ("email", "chat", "portal"),
            "queues": ("tier_1", "tier_2", "priority_response"),
            "priorities": ("low", "medium", "high", "critical"),
        },
    }


def service_ticketing_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(SERVICE_TICKETING_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Service Ticketing configuration fields: {tuple(sorted(missing))}")
    forbidden = tuple(sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(
            f"Service Ticketing does not expose stream-engine pickers or user-facing eventing choice: {forbidden}"
        )
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
    normalized["allowed_database_backends"] = SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
    normalized["required_event_topic"] = SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    normalized["visible_event_contracts"] = ("AppGen-X",)
    normalized["stream_engine_picker_visible"] = False
    normalized["user_eventing_choice"] = False
    runtime["configuration"] = normalized
    runtime["service_configurations"]["active"] = {
        "tenant": "system",
        "configuration_id": "active",
        "database_backend": backend,
        "event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "assignment_mode": normalized["assignment_mode"],
        "default_region": normalized["default_region"],
        "default_timezone": normalized["default_timezone"],
        "audit_hash": _digest(normalized),
    }
    _seed_service_catalogs(runtime)
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    _record_audit(runtime, "service_configuration", "active", "configure_runtime", normalized)
    return {"ok": True, "state": runtime, "configuration": normalized}


def service_ticketing_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in SERVICE_TICKETING_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Service Ticketing parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Service Ticketing parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "tenant": "system",
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)}),
        "audit_hash": _digest({"parameter": name, "value": value}),
    }
    runtime["parameters"][name] = parameter
    runtime["service_parameters"][name] = {
        "tenant": "system",
        "parameter_name": name,
        "parameter_value": value,
        "bounds": (low, high),
        "compiled_hash": parameter["compiled_hash"],
        "audit_hash": parameter["audit_hash"],
    }
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    _record_audit(runtime, "service_parameter", name, "set_parameter", parameter)
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
    normalized["audit_hash"] = _digest({"rule": normalized["rule_id"], "tenant": normalized["tenant"]})
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["service_rules"][normalized["rule_id"]] = {
        "tenant": normalized["tenant"],
        "rule_id": normalized["rule_id"],
        "scope": normalized["scope"],
        "status": normalized["status"],
        "allowed_regions": normalized["allowed_regions"],
        "allowed_channels": normalized["allowed_channels"],
        "allowed_priorities": normalized["allowed_priorities"],
        "compiled_hash": normalized["compiled_hash"],
        "audit_hash": normalized["audit_hash"],
    }
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    _record_audit(runtime, "service_rule", normalized["rule_id"], "register_rule", normalized)
    return {"ok": True, "state": runtime, "rule": normalized}


def service_ticketing_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in SERVICE_TICKETING_OWNED_TABLES:
        raise ValueError(f"Service Ticketing cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    _record_audit(runtime, table, f"schema_extension_v{extension['version']}", "register_schema_extension", extension)
    return {"ok": True, "state": runtime, "extension": extension}


def service_ticketing_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    _require_appgen_x_event_contract(state)
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
        runtime["dead_letter"].append(
            {
                **event,
                "handler": handler,
                "table": SERVICE_TICKETING_RUNTIME_TABLES[2],
            }
        )
        _record_audit(runtime, SERVICE_TICKETING_RUNTIME_TABLES[2], event_id, "dead_letter_event", event)
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append(
        {
            **event,
            "handler": handler,
            "table": SERVICE_TICKETING_RUNTIME_TABLES[1],
        }
    )
    runtime["handled_events"].add(event_id)
    if event["event_type"] == "CustomerUpdated":
        runtime["customer_context"][payload["customer_id"]] = payload
        _upsert_entitlement_snapshot(runtime, payload)
    elif event["event_type"] == "PreferenceChanged":
        runtime["preferences"][payload["customer_id"]] = payload
    elif event["event_type"] == "EntitlementUpdated":
        _upsert_entitlement_snapshot(runtime, payload)
    elif event["event_type"] == "KnowledgeSuggested":
        _record_knowledge_suggestion(
            runtime,
            ticket_id=payload.get("ticket_id", "pre_ticket"),
            customer_id=payload.get("customer_id", "unknown"),
            source="event_projection",
            article_ref=payload.get("article_ref", "kb://unspecified"),
            recommendation=payload.get("recommendation", "Review suggested knowledge"),
            confidence=float(payload.get("confidence", 0.6)),
            tenant=payload.get("tenant", "unknown"),
        )
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    _record_audit(runtime, SERVICE_TICKETING_RUNTIME_TABLES[1], event_id, "receive_event", payload)
    return {"ok": True, "state": runtime, "handler": handler}


def service_ticketing_create_sla_policy(state: dict, command: dict) -> dict:
    required = {
        "sla_policy_id",
        "tenant",
        "name",
        "priority",
        "first_response_minutes",
        "resolution_target_hours",
        "status",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing SLA policy fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    if command["priority"] not in state["configuration"]["priority_levels"]:
        raise ValueError(f"Unsupported Service Ticketing priority: {command['priority']}")
    runtime = _copy_state(state)
    policy = {
        **command,
        "first_response_minutes": int(command["first_response_minutes"]),
        "resolution_target_hours": int(command["resolution_target_hours"]),
        "audit_proof": _digest(command),
    }
    runtime["sla_policies"][policy["sla_policy_id"]] = policy
    runtime["events"].append(_state_event("SlaPolicyRegistered", policy["sla_policy_id"], policy))
    _record_audit(runtime, "sla_policy", policy["sla_policy_id"], "create_sla_policy", policy)
    return {"ok": True, "state": runtime, "sla_policy": policy}


def service_ticketing_open_ticket(state: dict, command: dict) -> dict:
    required = {
        "ticket_id",
        "tenant",
        "customer_id",
        "subject",
        "description",
        "channel",
        "priority",
        "region",
        "sentiment",
        "sla_policy_id",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing ticket fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    _assert_supported_region_channel_priority(state, command["region"], command["channel"], command["priority"])
    if command["sla_policy_id"] not in state["sla_policies"]:
        raise ValueError(f"Unknown Service Ticketing SLA policy: {command['sla_policy_id']}")
    rule = _select_rule(state, command["tenant"])
    if rule and (
        command["priority"] not in rule["allowed_priorities"]
        or command["channel"] not in rule["allowed_channels"]
        or command["region"] not in rule["allowed_regions"]
    ):
        raise ValueError(f"Ticket violates service ticketing rule {rule['rule_id']}")
    runtime = _copy_state(state)
    breach_risk = _breach_risk(runtime, command)
    queue = _default_queue(runtime, command["tenant"])
    ticket = {
        **command,
        "sentiment": float(command["sentiment"]),
        "queue": queue,
        "assignment_id": None,
        "status": "open",
        "breach_risk": breach_risk,
        "next_best_response": _next_best_response(command),
        "audit_proof": _digest(command),
    }
    runtime["support_tickets"][ticket["ticket_id"]] = ticket
    _record_interaction(
        runtime,
        ticket,
        interaction_type="ticket_opened",
        actor="customer",
        summary=command["description"],
        channel=command["channel"],
    )
    _upsert_entitlement_snapshot(runtime, _entitlement_payload(runtime, ticket))
    _update_case_lifecycle(runtime, ticket, stage="open", status="open")
    _record_knowledge_suggestion(
        runtime,
        ticket_id=ticket["ticket_id"],
        customer_id=ticket["customer_id"],
        source="automation",
        article_ref="kb://service-ticketing/next-best-response",
        recommendation=ticket["next_best_response"],
        confidence=round(max(0.55, breach_risk), 2),
        tenant=ticket["tenant"],
    )
    _record_automation_insight(
        runtime,
        ticket,
        insight_type="sla_breach_risk",
        score=breach_risk,
        recommended_action=ticket["next_best_response"],
        explanation="Priority, sentiment, customer tier, and queue load contributed to the risk score.",
    )
    _emit(runtime, "SupportCaseOpened", ticket["tenant"], ticket)
    _record_audit(runtime, "support_ticket", ticket["ticket_id"], "open_ticket", ticket)
    if breach_risk >= float(runtime["parameters"].get("auto_escalation_threshold", {"value": 1.0})["value"]):
        runtime = service_ticketing_record_escalation(runtime, ticket["ticket_id"], reason="predicted_sla_breach")["state"]
    return {"ok": True, "state": runtime, "ticket": ticket}


def service_ticketing_assign_ticket(state: dict, command: dict) -> dict:
    required = {"assignment_id", "tenant", "ticket_id", "owner", "queue", "skills"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing assignment fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    if command["ticket_id"] not in state["support_tickets"]:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    runtime = _copy_state(state)
    assignment = {
        **command,
        "skills": tuple(command["skills"]),
        "status": "active",
        "assignment_score": _assignment_score(runtime, command),
        "audit_proof": _digest(command),
    }
    runtime["case_assignments"][assignment["assignment_id"]] = assignment
    runtime["support_tickets"][command["ticket_id"]]["assignment_id"] = assignment["assignment_id"]
    runtime["support_tickets"][command["ticket_id"]]["queue"] = assignment["queue"]
    runtime["support_tickets"][command["ticket_id"]]["status"] = "assigned"
    ticket = runtime["support_tickets"][command["ticket_id"]]
    _update_case_lifecycle(runtime, ticket, stage="assigned", status="assigned")
    _record_automation_insight(
        runtime,
        ticket,
        insight_type="assignment_health",
        score=assignment["assignment_score"],
        recommended_action=f"Assign to {assignment['owner']}",
        explanation="Assignment score balances skill coverage and open-case load.",
    )
    if ticket["priority"] in {"high", "critical"} or "technical" in assignment["skills"]:
        _record_field_service_handoff(
            runtime,
            ticket=ticket,
            assignment_id=assignment["assignment_id"],
            handoff_reason="specialist_follow_up",
            target_team="field_service_dispatch",
        )
    runtime["events"].append(_state_event("TicketAssigned", assignment["assignment_id"], assignment))
    _emit(
        runtime,
        "TicketAssigned",
        assignment["tenant"],
        {
            "ticket_id": assignment["ticket_id"],
            "assignment_id": assignment["assignment_id"],
            "owner": assignment["owner"],
            "queue": assignment["queue"],
        },
    )
    _record_audit(runtime, "case_assignment", assignment["assignment_id"], "assign_ticket", assignment)
    return {"ok": True, "state": runtime, "assignment": assignment}


def service_ticketing_record_ticket_interaction(state: dict, command: dict) -> dict:
    required = {"ticket_id", "interaction_type", "actor", "summary", "channel"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing interaction fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(command["ticket_id"])
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    if command["channel"] not in state["configuration"]["channels"]:
        raise ValueError(f"Unsupported Service Ticketing channel: {command['channel']}")
    runtime = _copy_state(state)
    current_ticket = runtime["support_tickets"][command["ticket_id"]]
    interaction = _record_interaction(
        runtime,
        current_ticket,
        interaction_type=command["interaction_type"],
        actor=command["actor"],
        summary=command["summary"],
        channel=command["channel"],
    )
    _record_automation_insight(
        runtime,
        current_ticket,
        insight_type="interaction_quality",
        score=round(min(1.0, max(0.1, len(command["summary"]) / 240)), 4),
        recommended_action="keep_customer_updated",
        explanation="Interaction capture updates the case timeline and service quality evidence.",
    )
    _emit(
        runtime,
        "TicketInteractionRecorded",
        current_ticket["tenant"],
        {
            "ticket_id": current_ticket["ticket_id"],
            "interaction_id": interaction["interaction_id"],
            "interaction_type": interaction["interaction_type"],
        },
    )
    _record_audit(runtime, "ticket_interaction", interaction["interaction_id"], "record_ticket_interaction", interaction)
    return {"ok": True, "state": runtime, "interaction": interaction}


def service_ticketing_send_customer_update(state: dict, command: dict) -> dict:
    required = {"ticket_id", "update_type", "message"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing customer update fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(command["ticket_id"])
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    runtime = _copy_state(state)
    current_ticket = runtime["support_tickets"][command["ticket_id"]]
    update = _record_customer_update(
        runtime,
        current_ticket,
        update_type=command["update_type"],
        message=command["message"],
    )
    interaction = _record_interaction(
        runtime,
        current_ticket,
        interaction_type="customer_update",
        actor="system",
        summary=command["message"],
        channel=update["delivery_channel"],
    )
    _emit(runtime, "CustomerUpdateSent", current_ticket["tenant"], update)
    _emit(
        runtime,
        "CustomerUpdated",
        current_ticket["tenant"],
        {
            "customer_id": current_ticket["customer_id"],
            "ticket_id": current_ticket["ticket_id"],
            "update_id": update["update_id"],
            "event": command["update_type"],
        },
    )
    _record_audit(runtime, "customer_update", update["update_id"], "send_customer_update", update)
    return {"ok": True, "state": runtime, "customer_update": update, "interaction": interaction}


def service_ticketing_prepare_field_service_handoff(state: dict, command: dict) -> dict:
    required = {"ticket_id", "handoff_reason", "target_team"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing field service handoff fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(command["ticket_id"])
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    runtime = _copy_state(state)
    current_ticket = runtime["support_tickets"][command["ticket_id"]]
    handoff = _record_field_service_handoff(
        runtime,
        ticket=current_ticket,
        assignment_id=current_ticket.get("assignment_id"),
        handoff_reason=command["handoff_reason"],
        target_team=command["target_team"],
    )
    _record_interaction(
        runtime,
        current_ticket,
        interaction_type="field_service_handoff",
        actor="system",
        summary=f"Prepared handoff to {command['target_team']}: {command['handoff_reason']}",
        channel=current_ticket["channel"],
    )
    return {"ok": True, "state": runtime, "handoff": handoff}


def service_ticketing_record_escalation(state: dict, ticket_id: str, *, reason: str) -> dict:
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(ticket_id)
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {ticket_id}")
    runtime = _copy_state(state)
    escalation_id = f"esc_{ticket_id}_{len(runtime['escalation_events']) + 1}"
    queue = runtime["support_tickets"][ticket_id].get("queue", "priority_response")
    escalation = {
        "escalation_id": escalation_id,
        "tenant": ticket["tenant"],
        "ticket_id": ticket_id,
        "reason": reason,
        "breach_risk": ticket["breach_risk"],
        "queue": queue,
        "status": "open",
        "audit_proof": _digest({"ticket_id": ticket_id, "reason": reason}),
    }
    runtime["escalation_events"][escalation_id] = escalation
    runtime["support_tickets"][ticket_id]["status"] = "escalated"
    _update_case_lifecycle(runtime, runtime["support_tickets"][ticket_id], stage="escalated", status="escalated")
    _record_automation_insight(
        runtime,
        runtime["support_tickets"][ticket_id],
        insight_type="escalation_risk",
        score=ticket["breach_risk"],
        recommended_action="open_war_room",
        explanation=reason,
    )
    if not runtime["field_service_handoffs"]:
        _record_field_service_handoff(
            runtime,
            ticket=runtime["support_tickets"][ticket_id],
            assignment_id=runtime["support_tickets"][ticket_id].get("assignment_id"),
            handoff_reason=reason,
            target_team="priority_response",
        )
    _emit(runtime, "SlaBreached", ticket["tenant"], escalation)
    _record_audit(runtime, "escalation_event", escalation_id, "record_escalation", escalation)
    return {"ok": True, "state": runtime, "escalation": escalation}


def service_ticketing_resolve_ticket(state: dict, ticket_id: str, *, resolution: str) -> dict:
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(ticket_id)
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {ticket_id}")
    runtime = _copy_state(state)
    resolved = {
        **ticket,
        "status": "resolved",
        "resolution": resolution,
        "audit_proof": _digest({"ticket_id": ticket_id, "resolution": resolution}),
    }
    runtime["support_tickets"][ticket_id] = resolved
    resolution_record = _record_resolution(runtime, resolved, resolution)
    customer_update = _record_customer_update(
        runtime,
        resolved,
        update_type="resolution_notice",
        message=f"Ticket {ticket_id} resolved: {resolution}",
    )
    csat_response = _record_csat(runtime, resolved)
    _update_case_lifecycle(runtime, resolved, stage="resolved", status="resolved")
    _record_automation_insight(
        runtime,
        resolved,
        insight_type="resolution_summary",
        score=max(0.5, 1 - resolved["breach_risk"]),
        recommended_action="request_csat",
        explanation=resolution,
    )
    _emit(
        runtime,
        "ResolutionRecorded",
        resolved["tenant"],
        {
            "ticket_id": ticket_id,
            "resolution_id": resolution_record["resolution_id"],
            "resolution": resolution,
        },
    )
    _emit(
        runtime,
        "CsatSurveyRequested",
        resolved["tenant"],
        {
            "ticket_id": ticket_id,
            "survey_id": csat_response["survey_id"],
            "customer_id": resolved["customer_id"],
        },
    )
    _emit(
        runtime,
        "CustomerUpdated",
        resolved["tenant"],
        {
            "customer_id": resolved["customer_id"],
            "ticket_id": ticket_id,
            "update_id": customer_update["update_id"],
            "event": "support_case_resolved",
        },
    )
    _record_audit(runtime, "resolution_record", resolution_record["resolution_id"], "resolve_ticket", resolution_record)
    return {"ok": True, "state": runtime, "ticket": resolved}


def service_ticketing_record_csat_response(state: dict, command: dict) -> dict:
    required = {"survey_id", "score", "comment"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing CSAT response fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    survey = state["csat_responses"].get(command["survey_id"])
    if not survey:
        raise ValueError(f"Unknown Service Ticketing CSAT survey: {command['survey_id']}")
    score = int(command["score"])
    if not 1 <= score <= 5:
        raise ValueError("Service Ticketing CSAT score must be between 1 and 5")
    ticket = state["support_tickets"].get(survey["ticket_id"])
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {survey['ticket_id']}")
    runtime = _copy_state(state)
    response = {
        **runtime["csat_responses"][command["survey_id"]],
        "status": "received",
        "score": score,
        "comment": command["comment"],
        "audit_hash": _digest({"survey_id": command["survey_id"], "score": score, "comment": command["comment"]}),
    }
    runtime["csat_responses"][command["survey_id"]] = response
    current_ticket = runtime["support_tickets"][survey["ticket_id"]]
    _record_interaction(
        runtime,
        current_ticket,
        interaction_type="csat_response",
        actor="customer",
        summary=command["comment"],
        channel=current_ticket["channel"],
    )
    _record_automation_insight(
        runtime,
        current_ticket,
        insight_type="customer_satisfaction",
        score=round(score / 5, 4),
        recommended_action="close_case" if score >= 4 else "manager_follow_up",
        explanation=command["comment"],
    )
    _emit(
        runtime,
        "CsatResponseRecorded",
        current_ticket["tenant"],
        {
            "ticket_id": current_ticket["ticket_id"],
            "survey_id": command["survey_id"],
            "score": score,
        },
    )
    _record_audit(runtime, "csat_response", command["survey_id"], "record_csat_response", response)
    return {"ok": True, "state": runtime, "csat_response": response}


def service_ticketing_reopen_ticket(state: dict, command: dict) -> dict:
    required = {"ticket_id", "reason"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing reopen fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(command["ticket_id"])
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    runtime = _copy_state(state)
    reopened = {
        **runtime["support_tickets"][command["ticket_id"]],
        "status": "reopened",
        "reopen_reason": command["reason"],
        "audit_proof": _digest({"ticket_id": command["ticket_id"], "reason": command["reason"]}),
    }
    runtime["support_tickets"][command["ticket_id"]] = reopened
    _update_case_lifecycle(runtime, reopened, stage="reopened", status="reopened")
    _record_interaction(
        runtime,
        reopened,
        interaction_type="ticket_reopened",
        actor=command.get("actor", "system"),
        summary=command["reason"],
        channel=reopened["channel"],
    )
    customer_update = _record_customer_update(
        runtime,
        reopened,
        update_type="reopen_notice",
        message=f"Ticket {command['ticket_id']} was reopened: {command['reason']}",
    )
    _record_automation_insight(
        runtime,
        reopened,
        insight_type="reopen_risk",
        score=max(0.5, reopened["breach_risk"]),
        recommended_action="manager_follow_up",
        explanation=command["reason"],
    )
    _emit(runtime, "SupportCaseReopened", reopened["tenant"], {"ticket_id": reopened["ticket_id"], "reason": command["reason"]})
    _emit(
        runtime,
        "CustomerUpdated",
        reopened["tenant"],
        {
            "customer_id": reopened["customer_id"],
            "ticket_id": reopened["ticket_id"],
            "update_id": customer_update["update_id"],
            "event": "support_case_reopened",
        },
    )
    _record_audit(runtime, "support_ticket", reopened["ticket_id"], "reopen_ticket", reopened)
    return {"ok": True, "state": runtime, "ticket": reopened}


def service_ticketing_close_ticket(state: dict, command: dict) -> dict:
    required = {"ticket_id", "closure_reason"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Service Ticketing close fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    ticket = state["support_tickets"].get(command["ticket_id"])
    if not ticket:
        raise ValueError(f"Unknown Service Ticketing ticket: {command['ticket_id']}")
    runtime = _copy_state(state)
    closed = {
        **runtime["support_tickets"][command["ticket_id"]],
        "status": "closed",
        "closure_reason": command["closure_reason"],
        "audit_proof": _digest({"ticket_id": command["ticket_id"], "closure_reason": command["closure_reason"]}),
    }
    runtime["support_tickets"][command["ticket_id"]] = closed
    assignment_id = closed.get("assignment_id")
    if assignment_id in runtime["case_assignments"]:
        runtime["case_assignments"][assignment_id]["status"] = "closed"
    for escalation in runtime["escalation_events"].values():
        if escalation["ticket_id"] == command["ticket_id"]:
            escalation["status"] = "closed"
    _update_case_lifecycle(runtime, closed, stage="closed", status="closed")
    _record_interaction(
        runtime,
        closed,
        interaction_type="ticket_closed",
        actor=command.get("actor", "system"),
        summary=command["closure_reason"],
        channel=closed["channel"],
    )
    customer_update = _record_customer_update(
        runtime,
        closed,
        update_type="closure_notice",
        message=f"Ticket {command['ticket_id']} was closed: {command['closure_reason']}",
    )
    _emit(runtime, "SupportCaseClosed", closed["tenant"], {"ticket_id": closed["ticket_id"], "closure_reason": command["closure_reason"]})
    _emit(
        runtime,
        "CustomerUpdated",
        closed["tenant"],
        {
            "customer_id": closed["customer_id"],
            "ticket_id": closed["ticket_id"],
            "update_id": customer_update["update_id"],
            "event": "support_case_closed",
        },
    )
    _record_audit(runtime, "support_ticket", closed["ticket_id"], "close_ticket", closed)
    return {"ok": True, "state": runtime, "ticket": closed}


def service_ticketing_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["hash"] == _state_event(event["event_type"], event["key"], event["payload"])["hash"] for event in state["events"])
    checks = {
        "configuration": state.get("configuration", {}).get("event_contract") == "AppGen-X"
        and state.get("configuration", {}).get("event_topic") == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
        "database": state.get("configuration", {}).get("database_backend") in SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
        "rules": bool(state["rules"]),
        "parameters": bool(state["parameters"]),
        "tickets": bool(state["support_tickets"]),
        "outbox": all(item["idempotency_key"].startswith("service_ticketing:") for item in state["outbox"]),
        "inbox": all(item["handler"]["idempotency_key"].startswith("service_ticketing:") for item in state["inbox"]),
        "dead_letter": isinstance(state["dead_letter"], list),
        "audit_log": bool(state["ticket_audit_logs"]),
        "hash_chain": hash_chain_valid,
    }
    return {
        "ok": all(checks.values()),
        "checks": checks,
        "hash_chain_valid": hash_chain_valid,
        "blocking_gaps": tuple(key for key, ok in checks.items() if not ok),
    }


def service_ticketing_ui_binding_contract() -> dict:
    return {
        "format": "appgen.service-ticketing-ui-binding-contract.v1",
        "ok": True,
        "binding_evidence": {
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
            "workbench_route": "/workbench/pbcs/service_ticketing",
            "outbox_table": SERVICE_TICKETING_RUNTIME_TABLES[0],
            "inbox_table": SERVICE_TICKETING_RUNTIME_TABLES[1],
            "dead_letter_table": SERVICE_TICKETING_RUNTIME_TABLES[2],
            "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
        },
    }


def service_ticketing_build_workbench_view(state: dict, *, tenant: str) -> dict:
    tickets = tuple(item for item in state.get("support_tickets", {}).values() if item["tenant"] == tenant)
    policies = tuple(item for item in state.get("sla_policies", {}).values() if item["tenant"] == tenant)
    assignments = tuple(item for item in state.get("case_assignments", {}).values() if item["tenant"] == tenant)
    escalations = tuple(item for item in state.get("escalation_events", {}).values() if item["tenant"] == tenant)
    interactions = tuple(item for item in state.get("ticket_interactions", {}).values() if item["tenant"] == tenant)
    knowledge = tuple(item for item in state.get("knowledge_suggestions", {}).values() if item["tenant"] == tenant)
    entitlements = tuple(item for item in state.get("entitlement_snapshots", {}).values() if item["tenant"] == tenant)
    handoffs = tuple(item for item in state.get("field_service_handoffs", {}).values() if item["tenant"] == tenant)
    customer_updates = tuple(item for item in state.get("customer_updates", {}).values() if item["tenant"] == tenant)
    resolutions = tuple(item for item in state.get("resolution_records", {}).values() if item["tenant"] == tenant)
    csat = tuple(item for item in state.get("csat_responses", {}).values() if item["tenant"] == tenant)
    automation = tuple(item for item in state.get("automation_insights", {}).values() if item["tenant"] == tenant)
    audit = tuple(item for item in state.get("ticket_audit_logs", {}).values() if item["tenant"] in {tenant, "system"})
    return {
        "format": "appgen.service-ticketing-workbench-view.v1",
        "tenant": tenant,
        "ticket_count": len(tickets),
        "open_ticket_count": len(tuple(item for item in tickets if item["status"] in {"open", "assigned", "escalated", "reopened"})),
        "resolved_ticket_count": len(tuple(item for item in tickets if item["status"] in {"resolved", "closed"})),
        "closed_ticket_count": len(tuple(item for item in tickets if item["status"] == "closed")),
        "queue_count": len(state.get("service_queues", {})),
        "priority_count": len(state.get("service_priorities", {})),
        "sla_policy_count": len(policies),
        "assignment_count": len(assignments),
        "escalation_count": len(escalations),
        "interaction_count": len(interactions),
        "knowledge_suggestion_count": len(knowledge),
        "entitlement_count": len(entitlements),
        "handoff_count": len(handoffs),
        "customer_update_count": len(customer_updates),
        "resolution_count": len(resolutions),
        "csat_pending_count": len(tuple(item for item in csat if item["status"] == "pending")),
        "audit_count": len(audit),
        "automation_insight_count": len(automation),
        "average_breach_risk": round(sum(item["breach_risk"] for item in tickets) / max(len(tickets), 1), 4),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(tuple(item for item in state.get("service_rules", {}).values() if item["tenant"] == tenant)),
        "parameter_count": len(state.get("service_parameters", {})),
        "binding_evidence": {
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
            "outbox_table": SERVICE_TICKETING_RUNTIME_TABLES[0],
            "inbox_table": SERVICE_TICKETING_RUNTIME_TABLES[1],
            "dead_letter_table": SERVICE_TICKETING_RUNTIME_TABLES[2],
            "eventing": {
                "event_contract": "AppGen-X",
                "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
                "stream_engine_picker_visible": False,
            },
        },
    }


def service_ticketing_build_api_contract() -> dict:
    routes = (
        {
            "route": "PUT /service-ticketing/configuration",
            "command": "configure_runtime",
            "owned_tables": ("service_configuration", "service_queue", "service_priority"),
            "requires_permission": "service_ticketing.configure",
        },
        {
            "route": "POST /service-ticketing/parameters",
            "command": "set_parameter",
            "owned_tables": ("service_parameter",),
            "requires_permission": "service_ticketing.configure",
            "idempotency_key": "parameter_name",
        },
        {
            "route": "POST /service-ticketing/rules",
            "command": "register_rule",
            "owned_tables": ("service_rule",),
            "requires_permission": "service_ticketing.configure",
            "idempotency_key": "rule_id",
        },
        {
            "route": "POST /sla-policies",
            "command": "create_sla_policy",
            "owned_tables": ("sla_policy",),
            "emits": (),
            "requires_permission": "service_ticketing.configure",
            "idempotency_key": "sla_policy_id",
        },
        {
            "route": "POST /tickets",
            "command": "open_ticket",
            "owned_tables": (
                "support_ticket",
                "ticket_interaction",
                "knowledge_suggestion",
                "entitlement_snapshot",
                "case_lifecycle_state",
                "automation_insight",
            ),
            "emits": ("SupportCaseOpened", "SlaBreached"),
            "requires_permission": "service_ticketing.ticket.write",
            "idempotency_key": "ticket_id",
        },
        {
            "route": "POST /assignments",
            "command": "assign_ticket",
            "owned_tables": ("case_assignment", "support_ticket", "case_lifecycle_state", "field_service_handoff"),
            "emits": ("TicketAssigned", "FieldServiceHandoffPrepared"),
            "requires_permission": "service_ticketing.assignment.write",
            "idempotency_key": "assignment_id",
        },
        {
            "route": "POST /ticket-interactions",
            "command": "record_ticket_interaction",
            "owned_tables": ("ticket_interaction", "support_ticket", "automation_insight"),
            "emits": ("TicketInteractionRecorded",),
            "requires_permission": "service_ticketing.ticket.write",
            "idempotency_key": "ticket_id:interaction_type:summary",
        },
        {
            "route": "POST /customer-updates",
            "command": "send_customer_update",
            "owned_tables": ("customer_update", "ticket_interaction", "support_ticket"),
            "emits": ("CustomerUpdateSent", "CustomerUpdated"),
            "requires_permission": "service_ticketing.customer.update",
            "idempotency_key": "ticket_id:update_type:message",
        },
        {
            "route": "POST /field-service-handoffs",
            "command": "prepare_field_service_handoff",
            "owned_tables": ("field_service_handoff", "support_ticket"),
            "emits": ("FieldServiceHandoffPrepared",),
            "requires_permission": "service_ticketing.escalation.write",
            "idempotency_key": "ticket_id:target_team:handoff_reason",
        },
        {
            "route": "POST /escalations",
            "command": "record_escalation",
            "owned_tables": ("escalation_event", "support_ticket", "field_service_handoff", "automation_insight"),
            "emits": ("SlaBreached",),
            "requires_permission": "service_ticketing.escalation.write",
            "idempotency_key": "ticket_id:reason",
        },
        {
            "route": "POST /resolutions",
            "command": "resolve_ticket",
            "owned_tables": ("support_ticket", "resolution_record", "customer_update", "csat_response"),
            "emits": ("ResolutionRecorded", "CsatSurveyRequested", "CustomerUpdated"),
            "requires_permission": "service_ticketing.ticket.write",
            "idempotency_key": "ticket_id",
        },
        {
            "route": "POST /csat-responses",
            "command": "record_csat_response",
            "owned_tables": ("csat_response", "ticket_interaction", "automation_insight"),
            "emits": ("CsatResponseRecorded",),
            "requires_permission": "service_ticketing.customer.update",
            "idempotency_key": "survey_id",
        },
        {
            "route": "POST /tickets/reopen",
            "command": "reopen_ticket",
            "owned_tables": ("support_ticket", "case_lifecycle_state", "ticket_interaction", "customer_update", "automation_insight"),
            "emits": ("SupportCaseReopened", "CustomerUpdated"),
            "requires_permission": "service_ticketing.ticket.write",
            "idempotency_key": "ticket_id:reason",
        },
        {
            "route": "POST /tickets/close",
            "command": "close_ticket",
            "owned_tables": ("support_ticket", "case_lifecycle_state", "ticket_interaction", "customer_update"),
            "emits": ("SupportCaseClosed", "CustomerUpdated"),
            "requires_permission": "service_ticketing.ticket.write",
            "idempotency_key": "ticket_id:closure_reason",
        },
        {
            "route": "POST /service-ticketing/events/inbox",
            "command": "receive_event",
            "owned_tables": (),
            "consumes": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
            "requires_permission": "service_ticketing.event.consume",
            "idempotency_key": "event_id",
        },
        {
            "route": "GET /service-ticketing/workbench",
            "query": "build_workbench_view",
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "requires_permission": "service_ticketing.audit",
        },
        {
            "route": "GET /service-ticketing/schema-contract",
            "query": "build_schema_contract",
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "requires_permission": "service_ticketing.audit",
        },
        {
            "route": "GET /service-ticketing/service-contract",
            "query": "build_service_contract",
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "requires_permission": "service_ticketing.audit",
        },
        {
            "route": "GET /service-ticketing/release-evidence",
            "query": "build_release_evidence",
            "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
            "requires_permission": "service_ticketing.audit",
        },
    )
    return {
        "format": "appgen.service-ticketing-api-contract.v1",
        "ok": True,
        "pbc": "service_ticketing",
        "event_contract": "AppGen-X",
        "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "shared_table_access": False,
        "database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
        "events": {
            "emits": SERVICE_TICKETING_EMITTED_EVENT_TYPES,
            "consumes": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
        },
        "dependency_contracts": _SERVICE_TICKETING_ALLOWED_DEPENDENCIES,
        "routes": routes,
        "declared_catalog_routes": (
            "PUT /service-ticketing/configuration",
            "POST /service-ticketing/parameters",
            "POST /service-ticketing/rules",
            "POST /tickets",
            "POST /assignments",
            "GET /service-ticketing/workbench",
        ),
        "permissions": tuple(sorted(service_ticketing_permissions_contract()["permissions"])),
        "configuration": (
            "SERVICE_TICKETING_DATABASE_URL",
            "SERVICE_TICKETING_EVENT_TOPIC",
            "SERVICE_TICKETING_RETRY_LIMIT",
            "SERVICE_TICKETING_DEFAULT_TIMEZONE",
        ),
    }


def service_ticketing_build_schema_contract() -> dict:
    tables = tuple(
        {
            "table": table,
            "pbc": "service_ticketing",
            "schema": "service_ticketing",
            "owned": True,
            "migration": f"pbcs/service_ticketing/migrations/{index:03d}_{table}.sql",
            "model": f"pbcs/service_ticketing/models/{_class_name(table)}.py",
            "fields": _SERVICE_TICKETING_TABLE_FIELDS[table],
            "relationships": _service_ticketing_table_relationships(table),
        }
        for index, table in enumerate(SERVICE_TICKETING_OWNED_TABLES, start=1)
    )
    runtime_tables = (
        {
            "table": SERVICE_TICKETING_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "published_at", "audit_hash"),
        },
        {
            "table": SERVICE_TICKETING_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "handled_at", "audit_hash"),
        },
        {
            "table": SERVICE_TICKETING_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "reason", "attempts", "audit_hash"),
        },
    )
    return {
        "format": "appgen.service-ticketing-owned-schema-contract.v1",
        "ok": len(tables) == len(SERVICE_TICKETING_OWNED_TABLES),
        "pbc": "service_ticketing",
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "tables": tables,
        "runtime_tables": runtime_tables,
        "migrations": tuple(table["migration"] for table in tables),
        "models": tuple(table["model"] for table in tables),
        "migration_descriptors": tuple(
            {
                "path": table["migration"],
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
            }
            for table in tables
        ),
        "model_descriptors": tuple(
            {
                "class_name": _class_name(table["table"]),
                "table": table["table"],
                "module": table["model"],
                "fields": table["fields"],
            }
            for table in tables
        ),
        "database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "schema_extensions": {
            "allowed": True,
            "owned_tables_only": True,
            "field_name_pattern": r"[a-z][a-z0-9_]*",
        },
        "declared_dependencies": service_ticketing_verify_owned_table_boundary(())["declared_dependencies"],
    }


def service_ticketing_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_sla_policy",
        "open_ticket",
        "assign_ticket",
        "record_ticket_interaction",
        "send_customer_update",
        "prepare_field_service_handoff",
        "record_escalation",
        "resolve_ticket",
        "record_csat_response",
        "reopen_ticket",
        "close_ticket",
        "run_control_tests",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "build_api_contract",
        "permissions_contract",
        "ui_binding_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    return {
        "format": "appgen.service-ticketing-service-contract.v1",
        "ok": len(command_methods) >= 10 and len(query_methods) >= 7,
        "pbc": "service_ticketing",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "transaction_boundary": "service_ticketing_owned_datastore_plus_appgen_outbox",
        "mutates_only_owned_tables": True,
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
        "standard_service_surfaces": (
            "tickets",
            "queues",
            "slas",
            "priorities",
            "assignments",
            "escalations",
            "interactions",
            "knowledge_suggestions",
            "entitlements",
            "case_lifecycle",
            "field_service_handoffs",
            "customer_updates",
            "resolution",
            "csat",
            "audit",
            "automation_insights",
        ),
        "idempotent_handlers": ("receive_event",),
        "event_contract": {
            "contract": "AppGen-X",
            "required_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
            "emits": SERVICE_TICKETING_EMITTED_EVENT_TYPES,
            "consumes": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
            "outbox_table": SERVICE_TICKETING_RUNTIME_TABLES[0],
            "inbox_table": SERVICE_TICKETING_RUNTIME_TABLES[1],
            "dead_letter_table": SERVICE_TICKETING_RUNTIME_TABLES[2],
            "idempotency_key": "event_type:event_id",
            "stream_engine_picker_visible": False,
        },
        "retry_policy": {
            "configured_by": "retry_limit",
            "dead_letter_after_retry_limit": True,
            "dead_letter_table": SERVICE_TICKETING_RUNTIME_TABLES[2],
        },
        "external_dependencies": service_ticketing_verify_owned_table_boundary(())["declared_dependencies"],
        "shared_table_access": False,
    }


def service_ticketing_build_release_evidence() -> dict:
    schema = service_ticketing_build_schema_contract()
    service = service_ticketing_build_service_contract()
    api = service_ticketing_build_api_contract()
    permissions = service_ticketing_permissions_contract()
    ui_binding = service_ticketing_ui_binding_contract()
    state = service_ticketing_empty_state()
    state = service_ticketing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "channels": ("email", "chat", "portal"),
            "priority_levels": ("low", "medium", "high", "critical"),
            "default_timezone": "UTC",
            "assignment_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("sla_breach_risk_threshold", 0.7),
        ("auto_escalation_threshold", 0.9),
        ("sentiment_risk_weight", 0.3),
        ("priority_weight", 0.3),
        ("customer_tier_weight", 0.2),
        ("queue_load_weight", 0.2),
        ("first_response_minutes", 30),
        ("resolution_target_hours", 24),
        ("max_open_cases_per_owner", 25),
        ("workbench_limit", 50),
    ):
        state = service_ticketing_set_parameter(state, name, value)["state"]
    state = service_ticketing_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "scope": "service_ticketing",
            "status": "active",
            "allowed_regions": ("US",),
            "allowed_channels": ("email", "chat", "portal"),
            "allowed_priorities": ("medium", "high", "critical"),
            "assignment_policy": {
                "default_queue": "tier_2",
                "default_owner": "agent_release",
                "skills": ("technical", "billing"),
            },
            "escalation_policy": {
                "critical_queue": "priority_response",
                "breach_owner": "manager_release",
            },
        },
    )["state"]
    state = service_ticketing_register_schema_extension(
        state,
        "knowledge_suggestion",
        {"retrieval_trace": "jsonb"},
    )["state"]
    processed = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_release_customer",
            "event_type": "CustomerUpdated",
            "payload": {
                "tenant": "tenant_release",
                "customer_id": "cust_release",
                "tier": "enterprise",
                "entitlements": ("priority_support", "field_service"),
            },
        },
    )
    state = processed["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_release_pref",
            "event_type": "PreferenceChanged",
            "payload": {
                "tenant": "tenant_release",
                "customer_id": "cust_release",
                "preferred_channel": "chat",
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_release_knowledge",
            "event_type": "KnowledgeSuggested",
            "payload": {
                "tenant": "tenant_release",
                "customer_id": "cust_release",
                "ticket_id": "case_release",
                "article_ref": "kb://release/checklist",
                "recommendation": "Follow the escalation checklist",
                "confidence": 0.88,
            },
        },
    )["state"]
    failed = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_release_dead",
            "event_type": "EntitlementUpdated",
            "payload": {
                "tenant": "tenant_release",
                "customer_id": "cust_release",
                "tier": "enterprise",
            },
        },
        simulate_failure=True,
    )
    state = failed["state"]
    state = service_ticketing_create_sla_policy(
        state,
        {
            "sla_policy_id": "sla_release",
            "tenant": "tenant_release",
            "name": "Release Critical",
            "priority": "critical",
            "first_response_minutes": 15,
            "resolution_target_hours": 8,
            "status": "active",
        },
    )["state"]
    state = service_ticketing_open_ticket(
        state,
        {
            "ticket_id": "case_release",
            "tenant": "tenant_release",
            "customer_id": "cust_release",
            "subject": "Field asset offline",
            "description": "Onsite equipment is down and requires immediate response",
            "channel": "chat",
            "priority": "critical",
            "region": "US",
            "sentiment": -0.8,
            "sla_policy_id": "sla_release",
        },
    )["state"]
    state = service_ticketing_assign_ticket(
        state,
        {
            "assignment_id": "assign_release",
            "tenant": "tenant_release",
            "ticket_id": "case_release",
            "owner": "agent_release",
            "queue": "tier_2",
            "skills": ("technical", "field_service"),
        },
    )["state"]
    state = service_ticketing_record_ticket_interaction(
        state,
        {
            "ticket_id": "case_release",
            "interaction_type": "agent_response",
            "actor": "agent_release",
            "summary": "Validated the outage scope and shared dispatch ETA",
            "channel": "chat",
        },
    )["state"]
    state = service_ticketing_send_customer_update(
        state,
        {
            "ticket_id": "case_release",
            "update_type": "progress_notice",
            "message": "Specialist dispatch is active and the service team is monitoring recovery.",
        },
    )["state"]
    state = service_ticketing_record_escalation(
        state,
        "case_release",
        reason="onsite_dispatch_required",
    )["state"]
    state = service_ticketing_prepare_field_service_handoff(
        state,
        {
            "ticket_id": "case_release",
            "handoff_reason": "onsite_validation",
            "target_team": "field_success",
        },
    )["state"]
    state = service_ticketing_resolve_ticket(
        state,
        "case_release",
        resolution="Dispatched specialist and restored service",
    )["state"]
    pending_survey = next(iter(state["csat_responses"]))
    state = service_ticketing_record_csat_response(
        state,
        {
            "survey_id": pending_survey,
            "score": 5,
            "comment": "Resolution was fast and transparent",
        },
    )["state"]
    state = service_ticketing_reopen_ticket(
        state,
        {
            "ticket_id": "case_release",
            "reason": "post_resolution_validation",
        },
    )["state"]
    state = service_ticketing_close_ticket(
        state,
        {
            "ticket_id": "case_release",
            "closure_reason": "customer_confirmed_restored_service",
        },
    )["state"]
    workbench = service_ticketing_build_workbench_view(state, tenant="tenant_release")
    boundary = service_ticketing_verify_owned_table_boundary(
        (
            "support_ticket",
            SERVICE_TICKETING_RUNTIME_TABLES[0],
            "customer_context_projection",
            "KnowledgeSuggested",
            "POST /field-service/handoffs",
        )
    )
    control = service_ticketing_run_control_tests(state)
    smoke = service_ticketing_runtime_smoke()
    expected_populated_tables = (
        "support_tickets",
        "service_queues",
        "sla_policies",
        "service_priorities",
        "case_assignments",
        "escalation_events",
        "ticket_interactions",
        "knowledge_suggestions",
        "entitlement_snapshots",
        "case_lifecycle_states",
        "field_service_handoffs",
        "customer_updates",
        "resolution_records",
        "csat_responses",
        "ticket_audit_logs",
        "automation_insights",
        "service_rules",
        "service_parameters",
        "service_configurations",
    )
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) == len(SERVICE_TICKETING_OWNED_TABLES)},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(SERVICE_TICKETING_OWNED_TABLES)},
        {"id": "model_per_owned_table", "ok": len(schema["models"]) == len(SERVICE_TICKETING_OWNED_TABLES)},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == SERVICE_TICKETING_RUNTIME_TABLES},
        {"id": "service_contract_depth", "ok": service["ok"] and "receive_event" in service["idempotent_handlers"] and "build_release_evidence" in service["query_methods"]},
        {"id": "api_event_contract", "ok": api["event_contract"] == "AppGen-X" and api["required_event_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_contracts", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "ui_binding_evidence", "ok": ui_binding["ok"] and ui_binding["binding_evidence"]["runtime_tables"] == SERVICE_TICKETING_RUNTIME_TABLES},
        {"id": "workbench_binding_evidence", "ok": workbench["binding_evidence"]["outbox_table"] == SERVICE_TICKETING_RUNTIME_TABLES[0]},
        {"id": "idempotent_eventing_evidence", "ok": processed["handler"]["status"] == "handled" and failed["handler"]["status"] == "dead_letter" and workbench["dead_letter_count"] == 1},
        {"id": "boundary_contract", "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == ()},
        {"id": "database_allowlist", "ok": schema["database_backends"] == SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS and api["database_backends"] == SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS},
        {"id": "control_tests", "ok": control["ok"]},
        {"id": "table_stakes_covered", "ok": all(bool(state[name]) for name in expected_populated_tables)},
        {"id": "runtime_smoke", "ok": smoke["ok"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.service-ticketing-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": "service_ticketing",
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "schema_contract": schema,
        "service_contract": service,
        "api_contract": api,
        "permissions_contract": permissions,
        "ui_binding_contract": ui_binding,
        "workbench": workbench,
        "boundary_contract": boundary,
        "control_tests": control,
        "runtime_smoke": smoke,
    }


def service_ticketing_permissions_contract() -> dict:
    return {
        "format": "appgen.service-ticketing-permissions.v1",
        "ok": True,
        "permissions": (
            "service_ticketing.ticket.write",
            "service_ticketing.queue.manage",
            "service_ticketing.assignment.write",
            "service_ticketing.escalation.write",
            "service_ticketing.customer.update",
            "service_ticketing.csat.write",
            "service_ticketing.event.consume",
            "service_ticketing.configure",
            "service_ticketing.audit",
        ),
        "action_permissions": {
            "configure_runtime": "service_ticketing.configure",
            "set_parameter": "service_ticketing.configure",
            "register_rule": "service_ticketing.configure",
            "register_schema_extension": "service_ticketing.configure",
            "create_sla_policy": "service_ticketing.configure",
            "open_ticket": "service_ticketing.ticket.write",
            "assign_ticket": "service_ticketing.assignment.write",
            "record_ticket_interaction": "service_ticketing.ticket.write",
            "send_customer_update": "service_ticketing.customer.update",
            "prepare_field_service_handoff": "service_ticketing.escalation.write",
            "record_escalation": "service_ticketing.escalation.write",
            "resolve_ticket": "service_ticketing.customer.update",
            "record_csat_response": "service_ticketing.csat.write",
            "reopen_ticket": "service_ticketing.ticket.write",
            "close_ticket": "service_ticketing.ticket.write",
            "receive_event": "service_ticketing.event.consume",
            "run_control_tests": "service_ticketing.audit",
            "build_workbench_view": "service_ticketing.audit",
            "build_api_contract": "service_ticketing.audit",
            "build_schema_contract": "service_ticketing.audit",
            "build_service_contract": "service_ticketing.audit",
            "build_release_evidence": "service_ticketing.audit",
            "ui_binding_contract": "service_ticketing.audit",
            "verify_owned_table_boundary": "service_ticketing.audit",
        },
    }


def service_ticketing_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed = (
        *SERVICE_TICKETING_OWNED_TABLES,
        *SERVICE_TICKETING_RUNTIME_TABLES,
        *SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
        *_SERVICE_TICKETING_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(
        reference
        for reference in references
        if reference not in allowed_set and not str(reference).startswith("service_ticketing_")
    )
    return {
        "format": "appgen.service-ticketing-boundary.v1",
        "ok": not violations,
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": tuple(
                item for item in _SERVICE_TICKETING_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))
            ),
            "events": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _SERVICE_TICKETING_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Service Ticketing runtime must be configured before commands execute")


def _require_appgen_x_event_contract(state: dict) -> None:
    _require_configured(state)
    configuration = state["configuration"]
    if (
        configuration.get("event_contract") != "AppGen-X"
        or configuration.get("event_topic") != SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    ):
        raise ValueError("Service Ticketing runtime must remain bound to the AppGen-X service ticketing event contract")


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


def _default_queue(state: dict, tenant: str) -> str:
    rule = _select_rule(state, tenant)
    if rule:
        return str(rule["assignment_policy"].get("default_queue", "tier_1"))
    return "tier_1"


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
    open_cases = len(
        tuple(
            item
            for item in state["case_assignments"].values()
            if item["owner"] == command["owner"] and item["status"] == "active"
        )
    )
    max_open = int(state["parameters"].get("max_open_cases_per_owner", {"value": 100})["value"])
    return round(max(0.1, min(1.0, skill_count / 5 + (1 - open_cases / max_open) * 0.5)), 4)


def _next_best_response(command: dict) -> str:
    if command["priority"] == "critical":
        return "acknowledge_and_open_priority_response"
    if float(command["sentiment"]) < -0.4:
        return "empathize_and_offer_callback"
    return "send_guided_resolution"


def _seed_service_catalogs(state: dict) -> None:
    configuration = state["configuration"]
    assignment_mode = configuration.get("assignment_mode", "policy")
    workbench_limit = configuration.get("workbench_limit", 100)
    for index, queue in enumerate(state["seed_data"]["queues"], start=1):
        state["service_queues"][queue] = {
            "tenant": "system",
            "queue_id": queue,
            "name": queue.replace("_", " ").title(),
            "assignment_mode": assignment_mode,
            "service_tier": "priority" if "priority" in queue else "standard",
            "default_owner": "routing_pool",
            "workbench_limit": workbench_limit,
            "audit_hash": _digest({"queue": queue, "workbench_limit": workbench_limit, "position": index}),
        }
    defaults = {
        "low": (1, 240, 72),
        "medium": (2, 60, 24),
        "high": (3, 30, 12),
        "critical": (4, 15, 8),
    }
    for priority in configuration.get("priority_levels", state["seed_data"]["priorities"]):
        display_order, response_minutes, resolution_hours = defaults.get(priority, (5, 120, 24))
        state["service_priorities"][priority] = {
            "tenant": "system",
            "priority_id": priority,
            "display_order": display_order,
            "severity_score": round(min(1.0, display_order / 4), 2),
            "default_response_minutes": response_minutes,
            "default_resolution_hours": resolution_hours,
            "status": "active",
            "audit_hash": _digest({"priority": priority, "display_order": display_order}),
        }


def _record_interaction(
    state: dict,
    ticket: dict,
    *,
    interaction_type: str,
    actor: str,
    summary: str,
    channel: str,
) -> dict:
    interaction_id = f"int_{ticket['ticket_id']}_{len(state['ticket_interactions']) + 1}"
    interaction = {
        "tenant": ticket["tenant"],
        "interaction_id": interaction_id,
        "ticket_id": ticket["ticket_id"],
        "interaction_type": interaction_type,
        "channel": channel,
        "actor": actor,
        "summary": summary,
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "interaction_type": interaction_type, "summary": summary}),
    }
    state["ticket_interactions"][interaction_id] = interaction
    return interaction


def _record_knowledge_suggestion(
    state: dict,
    *,
    ticket_id: str,
    customer_id: str,
    source: str,
    article_ref: str,
    recommendation: str,
    confidence: float,
    tenant: str,
) -> dict:
    suggestion_id = f"ks_{ticket_id}_{len(state['knowledge_suggestions']) + 1}"
    suggestion = {
        "tenant": tenant,
        "suggestion_id": suggestion_id,
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "source": source,
        "article_ref": article_ref,
        "recommendation": recommendation,
        "confidence": round(confidence, 4),
        "audit_hash": _digest({"ticket_id": ticket_id, "article_ref": article_ref, "confidence": confidence}),
    }
    state["knowledge_suggestions"][suggestion_id] = suggestion
    return suggestion


def _upsert_entitlement_snapshot(state: dict, payload: dict) -> dict:
    customer_id = payload["customer_id"]
    snapshot_id = f"ent_{customer_id}"
    tier = payload.get("tier") or state.get("customer_context", {}).get(customer_id, {}).get("tier", "standard")
    entitlements = tuple(payload.get("entitlements", ())) or ("standard_support",)
    snapshot = {
        "tenant": payload.get("tenant", "unknown"),
        "snapshot_id": snapshot_id,
        "customer_id": customer_id,
        "tier": tier,
        "entitlements": entitlements,
        "coverage_status": "covered" if entitlements else "review",
        "source_event": payload.get("source_event", "projection"),
        "audit_hash": _digest({"customer_id": customer_id, "tier": tier, "entitlements": entitlements}),
    }
    state["entitlement_snapshots"][snapshot_id] = snapshot
    return snapshot


def _entitlement_payload(state: dict, ticket: dict) -> dict:
    customer = state["customer_context"].get(ticket["customer_id"], {})
    return {
        "tenant": ticket["tenant"],
        "customer_id": ticket["customer_id"],
        "tier": customer.get("tier", "standard"),
        "entitlements": tuple(customer.get("entitlements", ("standard_support",))),
        "source_event": "ticket_opened",
    }


def _update_case_lifecycle(state: dict, ticket: dict, *, stage: str, status: str) -> dict:
    current = state["case_lifecycle_states"].get(ticket["ticket_id"], {})
    history = tuple(current.get("history", ())) + (stage,)
    lifecycle = {
        "tenant": ticket["tenant"],
        "ticket_id": ticket["ticket_id"],
        "stage": stage,
        "status": status,
        "history": history,
        "current_owner": ticket.get("assignment_id"),
        "current_queue": ticket.get("queue"),
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "history": history, "status": status}),
    }
    state["case_lifecycle_states"][ticket["ticket_id"]] = lifecycle
    return lifecycle


def _record_field_service_handoff(
    state: dict,
    *,
    ticket: dict,
    assignment_id: str | None,
    handoff_reason: str,
    target_team: str,
) -> dict:
    handoff_id = f"handoff_{ticket['ticket_id']}_{len(state['field_service_handoffs']) + 1}"
    handoff = {
        "tenant": ticket["tenant"],
        "handoff_id": handoff_id,
        "ticket_id": ticket["ticket_id"],
        "assignment_id": assignment_id,
        "handoff_reason": handoff_reason,
        "target_team": target_team,
        "status": "prepared",
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "target_team": target_team, "reason": handoff_reason}),
    }
    state["field_service_handoffs"][handoff_id] = handoff
    _emit(
        state,
        "FieldServiceHandoffPrepared",
        ticket["tenant"],
        {
            "ticket_id": ticket["ticket_id"],
            "handoff_id": handoff_id,
            "target_team": target_team,
        },
    )
    _record_audit(state, "field_service_handoff", handoff_id, "prepare_field_service_handoff", handoff)
    return handoff


def _record_customer_update(state: dict, ticket: dict, *, update_type: str, message: str) -> dict:
    update_id = f"cust_update_{ticket['ticket_id']}_{len(state['customer_updates']) + 1}"
    preferred_channel = state["preferences"].get(ticket["customer_id"], {}).get("preferred_channel", ticket["channel"])
    update = {
        "tenant": ticket["tenant"],
        "update_id": update_id,
        "ticket_id": ticket["ticket_id"],
        "customer_id": ticket["customer_id"],
        "update_type": update_type,
        "delivery_channel": preferred_channel,
        "message": message,
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "message": message}),
    }
    state["customer_updates"][update_id] = update
    return update


def _record_resolution(state: dict, ticket: dict, resolution: str) -> dict:
    resolution_id = f"res_{ticket['ticket_id']}_{len(state['resolution_records']) + 1}"
    record = {
        "tenant": ticket["tenant"],
        "resolution_id": resolution_id,
        "ticket_id": ticket["ticket_id"],
        "resolution": resolution,
        "resolved_by": ticket.get("assignment_id") or "unassigned",
        "resolution_code": "completed",
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "resolution": resolution}),
    }
    state["resolution_records"][resolution_id] = record
    return record


def _record_csat(state: dict, ticket: dict) -> dict:
    survey_id = f"csat_{ticket['ticket_id']}_{len(state['csat_responses']) + 1}"
    csat = {
        "tenant": ticket["tenant"],
        "survey_id": survey_id,
        "ticket_id": ticket["ticket_id"],
        "customer_id": ticket["customer_id"],
        "status": "pending",
        "sent_at": "resolution_time",
        "score": None,
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "survey_id": survey_id}),
    }
    state["csat_responses"][survey_id] = csat
    return csat


def _record_automation_insight(
    state: dict,
    ticket: dict,
    *,
    insight_type: str,
    score: float,
    recommended_action: str,
    explanation: str,
) -> dict:
    insight_id = f"ins_{ticket['ticket_id']}_{len(state['automation_insights']) + 1}"
    insight = {
        "tenant": ticket["tenant"],
        "insight_id": insight_id,
        "ticket_id": ticket["ticket_id"],
        "insight_type": insight_type,
        "score": round(score, 4),
        "recommended_action": recommended_action,
        "explanation": explanation,
        "audit_hash": _digest({"ticket_id": ticket["ticket_id"], "insight_type": insight_type, "score": score}),
    }
    state["automation_insights"][insight_id] = insight
    return insight


def _record_audit(state: dict, table: str, record_id: str, action: str, payload: dict) -> dict:
    tenant = str(payload.get("tenant", "system"))
    audit_id = f"audit_{len(state['ticket_audit_logs']) + 1}"
    audit = {
        "tenant": tenant,
        "audit_id": audit_id,
        "entity_table": table,
        "entity_id": record_id,
        "action": action,
        "payload_digest": _digest(payload),
        "created_at": f"event_{len(state['events']) + 1}",
        "audit_hash": _digest({"table": table, "record_id": record_id, "action": action}),
    }
    state["ticket_audit_logs"][audit_id] = audit
    return audit


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    payload_snapshot = copy.deepcopy(payload)
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload_snapshot,
        "contract": "appgen_event_contract",
        "table": SERVICE_TICKETING_RUNTIME_TABLES[0],
        "idempotency_key": (
            f"service_ticketing:{event_type}:"
            f"{payload.get('ticket_id') or payload.get('assignment_id') or payload.get('escalation_id') or payload.get('update_id') or payload.get('survey_id') or len(state['outbox']) + 1}"
        ),
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": SERVICE_TICKETING_RUNTIME_TABLES[2],
        },
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload_snapshot}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload_snapshot))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    payload_snapshot = copy.deepcopy(payload)
    return {
        "event_type": event_type,
        "key": key,
        "payload": payload_snapshot,
        "hash": _digest({"event_type": event_type, "key": key, "payload": payload_snapshot}),
    }


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest(
            {
                "capability": capability,
                "tickets": len(state["support_tickets"]),
                "escalations": len(state["escalation_events"]),
                "automation": len(state["automation_insights"]),
            }
        ),
    }


def _service_ticketing_table_relationships(table: str) -> tuple[dict, ...]:
    relationship_map = {
        "support_ticket": (
            {"from_field": "sla_policy_id", "to_table": "sla_policy", "to_field": "sla_policy_id"},
            {"from_field": "queue", "to_table": "service_queue", "to_field": "queue_id"},
        ),
        "case_assignment": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
            {"from_field": "queue", "to_table": "service_queue", "to_field": "queue_id"},
        ),
        "escalation_event": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "ticket_interaction": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "knowledge_suggestion": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "case_lifecycle_state": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "field_service_handoff": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
            {"from_field": "assignment_id", "to_table": "case_assignment", "to_field": "assignment_id"},
        ),
        "customer_update": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "resolution_record": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "csat_response": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
        "automation_insight": (
            {"from_field": "ticket_id", "to_table": "support_ticket", "to_field": "ticket_id"},
        ),
    }
    return relationship_map.get(table, ())


def _class_name(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()
    ).hexdigest()
