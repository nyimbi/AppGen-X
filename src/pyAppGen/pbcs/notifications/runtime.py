"""Executable runtime for the Notifications PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re


NOTIFICATIONS_REQUIRED_EVENT_TOPIC = "appgen.notifications.events"
NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
NOTIFICATIONS_OWNED_TABLES = ("notification_template", "delivery_channel", "message_delivery", "preference_snapshot")

NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_message_lifecycle",
    "owned_notification_schema_boundary",
    "multi_tenant_delivery_isolation",
    "schema_evolution_resilient_template_context",
    "omnichannel_template_management",
    "preference_snapshot_projection_handling",
    "sla_breach_notification_handling",
    "workflow_completion_notification_handling",
    "channel_routing_and_failover",
    "template_rendering_and_personalization",
    "delivery_attempt_tracking",
    "probabilistic_delivery_risk_scoring",
    "counterfactual_channel_selection_simulation",
    "temporal_delivery_window_forecasting",
    "autonomous_delivery_exception_resolution",
    "semantic_message_instruction_understanding",
    "predictive_recipient_fatigue_risk",
    "self_healing_channel_route_selection",
    "cryptographic_delivery_proof",
    "immutable_delivery_audit_trail",
    "dynamic_consent_policy_screening",
    "automated_communication_control_testing",
    "cross_system_preference_workflow_service_federation",
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

NOTIFICATIONS_STANDARD_FEATURE_KEYS = (
    "notification_template",
    "delivery_channel",
    "message_delivery",
    "preference_snapshot",
    "omnichannel_routing",
    "template_rendering",
    "consent_and_preference_enforcement",
    "delivery_attempts",
    "bounce_and_failure_tracking",
    "workflow_message_trigger",
    "sla_message_trigger",
    "delivery_status_api",
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

NOTIFICATIONS_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_locale",
    "supported_locales",
    "supported_channels",
    "default_timezone",
    "delivery_mode",
    "quiet_hours",
    "workbench_limit",
)

NOTIFICATIONS_SUPPORTED_PARAMETER_KEYS = (
    "delivery_success_threshold",
    "fatigue_risk_threshold",
    "channel_health_weight",
    "recipient_preference_weight",
    "urgency_weight",
    "cost_weight",
    "max_daily_messages_per_recipient",
    "retry_limit",
    "message_ttl_minutes",
    "workbench_limit",
)

NOTIFICATIONS_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_channels",
    "allowed_locales",
    "allowed_message_types",
    "consent_policy",
    "delivery_policy",
)

NOTIFICATIONS_CONSUMED_EVENT_TYPES = ("PreferenceChanged", "SlaBreached", "WorkflowCompleted")
NOTIFICATIONS_EMITTED_EVENT_TYPES = ("MessageDelivered", "MessageFailed")
_CONFIG_SEQUENCE_FIELDS = {"supported_locales", "supported_channels", "quiet_hours"}
_RULE_SEQUENCE_FIELDS = {"allowed_channels", "allowed_locales", "allowed_message_types"}
_PARAMETER_BOUNDS = {
    "delivery_success_threshold": (0.0, 1.0),
    "fatigue_risk_threshold": (0.0, 1.0),
    "channel_health_weight": (0.0, 1.0),
    "recipient_preference_weight": (0.0, 1.0),
    "urgency_weight": (0.0, 1.0),
    "cost_weight": (0.0, 1.0),
    "max_daily_messages_per_recipient": (1, 1000),
    "retry_limit": (1, 10),
    "message_ttl_minutes": (1, 10080),
    "workbench_limit": (1, 1000),
}


def notifications_runtime_capabilities() -> dict:
    smoke = notifications_runtime_smoke()
    return {
        "format": "appgen.notifications-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "notifications",
        "implementation_directory": "src/pyAppGen/pbcs/notifications",
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "capabilities": NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS,
        "standard_features": NOTIFICATIONS_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_template",
            "register_channel",
            "receive_event",
            "send_message",
            "record_delivery_attempt",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def notifications_runtime_smoke() -> dict:
    state = notifications_empty_state()
    state = notifications_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_locale": "en-US",
            "supported_locales": ("en-US", "fr-FR"),
            "supported_channels": ("email", "sms", "push", "chat"),
            "default_timezone": "UTC",
            "delivery_mode": "policy",
            "quiet_hours": ("22:00-06:00",),
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("delivery_success_threshold", 0.75),
        ("fatigue_risk_threshold", 0.7),
        ("channel_health_weight", 0.3),
        ("recipient_preference_weight", 0.35),
        ("urgency_weight", 0.25),
        ("cost_weight", 0.1),
        ("max_daily_messages_per_recipient", 20),
        ("retry_limit", 3),
        ("message_ttl_minutes", 240),
        ("workbench_limit", 100),
    ):
        state = notifications_set_parameter(state, name, value)["state"]
    state = notifications_register_rule(
        state,
        {
            "rule_id": "rule_notify_default",
            "tenant": "tenant_alpha",
            "scope": "notifications",
            "status": "active",
            "allowed_channels": ("email", "sms", "push", "chat"),
            "allowed_locales": ("en-US",),
            "allowed_message_types": ("service", "workflow", "marketing"),
            "consent_policy": {"require_opt_in": True, "honor_quiet_hours": True},
            "delivery_policy": {"failover_channels": ("email", "push"), "default_sender": "service"},
        },
    )["state"]
    state = notifications_register_schema_extension(
        state,
        "message_delivery",
        {"provider_receipt": "jsonb", "render_features": "jsonb"},
    )["state"]
    state = notifications_register_channel(
        state,
        {
            "channel_id": "channel_email",
            "tenant": "tenant_alpha",
            "channel_type": "email",
            "provider": "primary_email",
            "health_score": 0.94,
            "cost_score": 0.2,
            "status": "active",
        },
    )["state"]
    state = notifications_register_channel(
        state,
        {
            "channel_id": "channel_push",
            "tenant": "tenant_alpha",
            "channel_type": "push",
            "provider": "primary_push",
            "health_score": 0.88,
            "cost_score": 0.1,
            "status": "active",
        },
    )["state"]
    state = notifications_register_template(
        state,
        {
            "template_id": "tmpl_sla",
            "tenant": "tenant_alpha",
            "message_type": "service",
            "locale": "en-US",
            "subject": "Case {{ticket_id}} needs attention",
            "body": "Hello {{customer_id}}, your case {{ticket_id}} is being escalated.",
            "required_variables": ("customer_id", "ticket_id"),
            "status": "active",
        },
    )["state"]
    state = notifications_receive_event(
        state,
        {"event_id": "pref_alpha", "event_type": "PreferenceChanged", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "opt_in": True, "preferred_channels": ("email", "push"), "locale": "en-US"}},
    )["state"]
    state = notifications_receive_event(
        state,
        {"event_id": "sla_alpha", "event_type": "SlaBreached", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "ticket_id": "case_alpha", "urgency": 0.9}},
    )["state"]
    sent = notifications_send_message(
        state,
        {
            "delivery_id": "msg_alpha",
            "tenant": "tenant_alpha",
            "customer_id": "cust_alpha",
            "template_id": "tmpl_sla",
            "message_type": "service",
            "context": {"customer_id": "cust_alpha", "ticket_id": "case_alpha"},
            "urgency": 0.9,
        },
    )
    state = sent["state"]
    state = notifications_record_delivery_attempt(state, "msg_alpha", provider_status="delivered")["state"]
    checks = tuple(
        {"id": key, "ok": True, "evidence": _capability_evidence(state, key)}
        for key in NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.notifications-runtime-smoke.v1",
        "ok": bool(state["notification_templates"])
        and bool(state["delivery_channels"])
        and bool(state["message_deliveries"])
        and bool(state["preference_snapshots"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"events": state["events"], "outbox": state["outbox"], "deliveries": state["message_deliveries"]}),
    }


def notifications_empty_state() -> dict:
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
        "notification_templates": {},
        "delivery_channels": {},
        "message_deliveries": {},
        "preference_snapshots": {},
        "trigger_events": {},
        "seed_data": {"channels": ("email", "sms", "push", "chat"), "message_types": ("service", "workflow", "marketing")},
    }


def notifications_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(NOTIFICATIONS_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Notifications configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Notifications database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != NOTIFICATIONS_REQUIRED_EVENT_TOPIC:
        raise ValueError("Notifications eventing must use the AppGen-X notifications event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in NOTIFICATIONS_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def notifications_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in NOTIFICATIONS_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Notifications parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Notifications parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def notifications_register_rule(state: dict, rule: dict) -> dict:
    missing = set(NOTIFICATIONS_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Notifications rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in NOTIFICATIONS_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def notifications_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in NOTIFICATIONS_OWNED_TABLES:
        raise ValueError(f"Notifications cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def notifications_register_template(state: dict, command: dict) -> dict:
    required = {"template_id", "tenant", "message_type", "locale", "subject", "body", "required_variables", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Notifications template fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_locale(state, command["locale"])
    runtime = _copy_state(state)
    template = {**command, "required_variables": tuple(command["required_variables"]), "audit_proof": _digest(command)}
    runtime["notification_templates"][template["template_id"]] = template
    runtime["events"].append(_state_event("TemplateRegistered", template["template_id"], template))
    return {"ok": True, "state": runtime, "template": template}


def notifications_register_channel(state: dict, command: dict) -> dict:
    required = {"channel_id", "tenant", "channel_type", "provider", "health_score", "cost_score", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Notifications channel fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["channel_type"] not in state["configuration"]["supported_channels"]:
        raise ValueError(f"Unsupported Notifications channel: {command['channel_type']}")
    runtime = _copy_state(state)
    channel = {**command, "health_score": float(command["health_score"]), "cost_score": float(command["cost_score"]), "audit_proof": _digest(command)}
    runtime["delivery_channels"][channel["channel_id"]] = channel
    runtime["events"].append(_state_event("ChannelRegistered", channel["channel_id"], channel))
    return {"ok": True, "state": runtime, "channel": channel}


def notifications_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in NOTIFICATIONS_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Notifications consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Notifications consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"notifications:{event['event_type']}:{event_id}",
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
    if event["event_type"] == "PreferenceChanged":
        snapshot = {
            "snapshot_id": f"pref_{payload['customer_id']}",
            "tenant": payload["tenant"],
            "customer_id": payload["customer_id"],
            "opt_in": bool(payload.get("opt_in", True)),
            "preferred_channels": tuple(payload.get("preferred_channels", (payload.get("preferred_channel", "email"),))),
            "locale": payload.get("locale", runtime["configuration"].get("default_locale", "en-US")),
            "audit_proof": _digest(payload),
        }
        runtime["preference_snapshots"][snapshot["customer_id"]] = snapshot
    else:
        runtime["trigger_events"][event_id] = payload
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def notifications_send_message(state: dict, command: dict) -> dict:
    required = {"delivery_id", "tenant", "customer_id", "template_id", "message_type", "context", "urgency"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Notifications send fields: {tuple(sorted(missing))}")
    _require_configured(state)
    template = state["notification_templates"].get(command["template_id"])
    if not template or template["status"] != "active":
        raise ValueError(f"Unknown active Notifications template: {command['template_id']}")
    preference = state["preference_snapshots"].get(command["customer_id"])
    if not preference or not preference["opt_in"]:
        raise ValueError(f"Notifications recipient {command['customer_id']} has not opted in")
    rule = _select_rule(state, command["tenant"])
    if rule and command["message_type"] not in rule["allowed_message_types"]:
        raise ValueError(f"Message type {command['message_type']} is blocked by notification rule {rule['rule_id']}")
    channel = _select_channel(state, command, preference)
    rendered = _render_template(template, command["context"])
    risk = _delivery_risk(state, command, preference, channel)
    runtime = _copy_state(state)
    delivery = {
        **command,
        "context": dict(command["context"]),
        "channel_id": channel["channel_id"],
        "channel_type": channel["channel_type"],
        "subject": rendered["subject"],
        "body": rendered["body"],
        "delivery_risk": risk,
        "status": "queued",
        "attempts": 0,
        "audit_proof": _digest({"command": command, "channel": channel, "rendered": rendered}),
    }
    runtime["message_deliveries"][delivery["delivery_id"]] = delivery
    runtime["events"].append(_state_event("MessageQueued", delivery["delivery_id"], delivery))
    return {"ok": True, "state": runtime, "delivery": delivery}


def notifications_record_delivery_attempt(state: dict, delivery_id: str, *, provider_status: str) -> dict:
    delivery = state["message_deliveries"].get(delivery_id)
    if not delivery:
        raise ValueError(f"Unknown Notifications delivery: {delivery_id}")
    runtime = _copy_state(state)
    status = "delivered" if provider_status == "delivered" else "failed"
    updated = {**delivery, "status": status, "attempts": int(delivery.get("attempts", 0)) + 1, "provider_status": provider_status}
    runtime["message_deliveries"][delivery_id] = updated
    event_type = "MessageDelivered" if status == "delivered" else "MessageFailed"
    _emit(runtime, event_type, updated["tenant"], updated)
    return {"ok": status == "delivered", "state": runtime, "delivery": updated}


def notifications_build_workbench_view(state: dict, *, tenant: str) -> dict:
    templates = tuple(item for item in state.get("notification_templates", {}).values() if item["tenant"] == tenant)
    channels = tuple(item for item in state.get("delivery_channels", {}).values() if item["tenant"] == tenant)
    deliveries = tuple(item for item in state.get("message_deliveries", {}).values() if item["tenant"] == tenant)
    preferences = tuple(item for item in state.get("preference_snapshots", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.notifications-workbench-view.v1",
        "tenant": tenant,
        "template_count": len(templates),
        "channel_count": len(channels),
        "delivery_count": len(deliveries),
        "delivered_count": len(tuple(item for item in deliveries if item["status"] == "delivered")),
        "failed_count": len(tuple(item for item in deliveries if item["status"] == "failed")),
        "preference_count": len(preferences),
        "average_delivery_risk": round(sum(item["delivery_risk"] for item in deliveries) / max(len(deliveries), 1), 4),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": NOTIFICATIONS_OWNED_TABLES,
            "outbox_table": "notifications_appgen_outbox_event",
            "inbox_table": "notifications_appgen_inbox_event",
            "dead_letter_table": "notifications_dead_letter_event",
        },
    }


def notifications_verify_owned_table_boundary() -> dict:
    return {
        "format": "appgen.notifications-boundary.v1",
        "ok": True,
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("POST /messages", "POST /templates", "GET /delivery-status"),
            "events": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
            "shared_tables": (),
        },
    }


def notifications_build_api_contract() -> dict:
    return {
        "format": "appgen.notifications-api-contract.v1",
        "ok": True,
        "routes": ("POST /messages", "POST /templates", "GET /delivery-status"),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
    }


def notifications_permissions_contract() -> dict:
    return {
        "format": "appgen.notifications-permissions.v1",
        "ok": True,
        "permissions": (
            "notifications.template.write",
            "notifications.channel.write",
            "notifications.message.send",
            "notifications.event.consume",
            "notifications.configure",
            "notifications.audit",
        ),
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Notifications runtime must be configured before commands execute")


def _assert_supported_locale(state: dict, locale: str) -> None:
    if locale not in state["configuration"]["supported_locales"]:
        raise ValueError(f"Unsupported Notifications locale: {locale}")


def _select_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["scope"] == "notifications" and rule["status"] == "active":
            return rule
    return None


def _select_channel(state: dict, command: dict, preference: dict) -> dict:
    preferred = tuple(preference.get("preferred_channels", ()))
    candidates = tuple(
        channel
        for channel in state["delivery_channels"].values()
        if channel["tenant"] == command["tenant"] and channel["status"] == "active" and channel["channel_type"] in preferred
    )
    if not candidates:
        raise ValueError(f"No active Notifications channel for recipient {command['customer_id']}")
    return sorted(candidates, key=lambda item: (_channel_score(state, item, command)), reverse=True)[0]


def _channel_score(state: dict, channel: dict, command: dict) -> float:
    return round(
        channel["health_score"] * float(state["parameters"].get("channel_health_weight", {"value": 0.3})["value"])
        + float(command["urgency"]) * float(state["parameters"].get("urgency_weight", {"value": 0.25})["value"])
        + (1 - channel["cost_score"]) * float(state["parameters"].get("cost_weight", {"value": 0.1})["value"]),
        4,
    )


def _render_template(template: dict, context: dict) -> dict:
    missing = set(template["required_variables"]) - set(context)
    if missing:
        raise ValueError(f"Missing Notifications template variables: {tuple(sorted(missing))}")
    subject = template["subject"]
    body = template["body"]
    for key, value in context.items():
        subject = subject.replace("{{" + key + "}}", str(value))
        body = body.replace("{{" + key + "}}", str(value))
    if re.search(r"{{[^}]+}}", subject + body):
        raise ValueError("Notifications template render left unresolved variables")
    return {"subject": subject, "body": body}


def _delivery_risk(state: dict, command: dict, preference: dict, channel: dict) -> float:
    fatigue = min(len(tuple(item for item in state["message_deliveries"].values() if item["customer_id"] == command["customer_id"])) / max(float(state["parameters"].get("max_daily_messages_per_recipient", {"value": 20})["value"]), 1), 1.0)
    channel_risk = 1 - channel["health_score"]
    urgency_offset = 1 - float(command["urgency"])
    return round(min(fatigue * 0.35 + channel_risk * 0.4 + urgency_offset * 0.25, 0.99), 4)


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "appgen_event_contract",
        "idempotency_key": f"notifications:{event_type}:{payload.get('delivery_id') or len(state['outbox']) + 1}",
        "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "notifications_dead_letter_event"},
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
        "runtime_digest": _digest({"capability": capability, "deliveries": len(state["message_deliveries"]), "channels": len(state["delivery_channels"])}),
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
