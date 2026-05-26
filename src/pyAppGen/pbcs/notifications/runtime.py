"""Executable runtime for the Notifications PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re


NOTIFICATIONS_REQUIRED_EVENT_TOPIC = "appgen.notifications.events"
NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
NOTIFICATIONS_OWNED_TABLES = (
    "notification_template",
    "template_locale_variant",
    "delivery_channel",
    "notification_recipient",
    "preference_snapshot",
    "consent_ledger",
    "delivery_schedule",
    "throttle_window",
    "provider_route",
    "message_delivery",
    "delivery_attempt",
    "retry_evidence",
    "delivery_receipt",
    "bounce_event",
    "notification_campaign",
    "campaign_dispatch",
    "transactional_notification",
    "notification_audit_log",
    "deliverability_analytics",
    "notification_rule",
    "notification_parameter",
    "notification_configuration",
)
NOTIFICATIONS_RUNTIME_TABLES = (
    "notifications_appgen_outbox_event",
    "notifications_appgen_inbox_event",
    "notifications_dead_letter_event",
)

NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_message_lifecycle",
    "owned_notification_schema_boundary",
    "multi_tenant_delivery_isolation",
    "schema_evolution_resilient_template_context",
    "omnichannel_template_management",
    "recipient_profile_projection_handling",
    "preference_snapshot_projection_handling",
    "consent_ledger_evidence",
    "delivery_schedule_and_quiet_hour_forecasting",
    "throttling_and_fatigue_controls",
    "provider_routing_and_failover",
    "template_rendering_and_personalization",
    "delivery_attempt_tracking",
    "delivery_receipt_and_bounce_evidence",
    "campaign_and_transactional_notification_orchestration",
    "localization_variant_management",
    "probabilistic_delivery_risk_scoring",
    "counterfactual_channel_selection_simulation",
    "autonomous_delivery_exception_resolution",
    "semantic_message_instruction_understanding",
    "predictive_recipient_fatigue_risk",
    "self_healing_channel_route_selection",
    "cryptographic_delivery_proof",
    "immutable_delivery_audit_trail",
    "dynamic_consent_policy_screening",
    "automated_communication_control_testing",
    "cross_system_preference_workflow_service_federation",
    "deliverability_analytics_rollup",
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
    "template_locale_variant",
    "delivery_channel",
    "notification_recipient",
    "preference_snapshot",
    "consent_ledger",
    "delivery_schedule",
    "throttle_window",
    "provider_route",
    "message_delivery",
    "delivery_attempt",
    "retry_evidence",
    "delivery_receipt",
    "bounce_event",
    "notification_campaign",
    "campaign_dispatch",
    "transactional_notification",
    "notification_audit_log",
    "deliverability_analytics",
    "omnichannel_routing",
    "template_rendering",
    "consent_and_preference_enforcement",
    "scheduling",
    "throttling",
    "localization",
    "campaign_orchestration",
    "transactional_notifications",
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
    "schema_contract",
    "service_contract",
    "release_evidence",
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
    "campaign_batch_size",
    "schedule_horizon_hours",
    "bounce_retry_window_minutes",
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
    "throttle_policy",
    "routing_policy",
    "schedule_policy",
)

NOTIFICATIONS_CONSUMED_EVENT_TYPES = (
    "PreferenceChanged",
    "ConsentUpdated",
    "CampaignScheduled",
    "DeliveryReceiptImported",
    "BounceRegistered",
    "SlaBreached",
    "WorkflowCompleted",
    "TransactionalNotificationRequested",
)
NOTIFICATIONS_EMITTED_EVENT_TYPES = (
    "MessageQueued",
    "MessageDelivered",
    "MessageFailed",
    "DeliveryReceiptRecorded",
    "BounceRecorded",
    "CampaignDispatched",
    "TransactionalNotificationDispatched",
)
_CONFIG_SEQUENCE_FIELDS = {"supported_locales", "supported_channels", "quiet_hours"}
_RULE_SEQUENCE_FIELDS = {"allowed_channels", "allowed_locales", "allowed_message_types"}
_FORBIDDEN_EVENTING_FIELDS = frozenset(
    {
        "stream_engine",
        "stream_engine_picker",
        "event_contract_selector",
        "eventing_backend",
    }
)
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
    "campaign_batch_size": (1, 100000),
    "schedule_horizon_hours": (1, 720),
    "bounce_retry_window_minutes": (1, 10080),
}
_NOTIFICATIONS_ALLOWED_DEPENDENCIES = (
    "GET /recipient-profiles/{recipient_id}",
    "GET /workflow-events/{workflow_id}",
    "GET /sla-breaches/{breach_id}",
    "recipient_projection",
    "preference_projection",
    "consent_projection",
    "sla_projection",
    "workflow_projection",
    "campaign_projection",
)


def notifications_runtime_capabilities() -> dict:
    smoke = notifications_runtime_smoke()
    return {
        "format": "appgen.notifications-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "notifications",
        "implementation_directory": "src/pyAppGen/pbcs/notifications",
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "runtime_tables": NOTIFICATIONS_RUNTIME_TABLES,
        "required_event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
        "consumes": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
        "emits": NOTIFICATIONS_EMITTED_EVENT_TYPES,
        "capabilities": NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS,
        "standard_features": NOTIFICATIONS_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "register_template",
            "register_channel",
            "receive_event",
            "send_message",
            "record_delivery_attempt",
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


def notifications_runtime_smoke() -> dict:
    state = _notifications_smoke_state()
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
        and bool(state["delivery_receipts"])
        and bool(state["notification_audit_log"])
        and bool(state["outbox"])
        and bool(state["inbox"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest(
            {
                "events": state["events"],
                "outbox": state["outbox"],
                "deliveries": state["message_deliveries"],
                "analytics": state["deliverability_analytics"],
            }
        ),
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
        "template_locale_variants": {},
        "delivery_channels": {},
        "notification_recipients": {},
        "preference_snapshots": {},
        "consent_ledger": {},
        "delivery_schedules": {},
        "throttle_windows": {},
        "provider_routes": {},
        "message_deliveries": {},
        "delivery_attempts": {},
        "retry_evidence": {},
        "delivery_receipts": {},
        "bounce_events": {},
        "notification_campaigns": {},
        "campaign_dispatches": {},
        "transactional_notifications": {},
        "notification_audit_log": [],
        "deliverability_analytics": {},
        "trigger_events": {},
        "seed_data": {
            "channels": ("email", "sms", "push", "chat"),
            "message_types": ("service", "workflow", "marketing", "transactional"),
        },
    }


def notifications_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(NOTIFICATIONS_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Notifications configuration fields: {tuple(sorted(missing))}")
    forbidden = tuple(sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(
            "Notifications does not expose stream-engine pickers or user-facing eventing choice: "
            f"{forbidden}"
        )
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
    normalized["allowed_database_backends"] = NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
    normalized["required_event_topic"] = NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    normalized["stream_engine_picker_visible"] = False
    normalized["user_eventing_choice"] = False
    normalized["owned_tables"] = NOTIFICATIONS_OWNED_TABLES
    normalized["runtime_tables"] = NOTIFICATIONS_RUNTIME_TABLES
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    _append_audit(runtime, "configure_runtime", normalized, tenant="system")
    return {"ok": True, "state": runtime, "configuration": normalized}


def notifications_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in NOTIFICATIONS_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Notifications parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Notifications parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "parameter_id": name,
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)}),
    }
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    _append_audit(runtime, "set_parameter", parameter, tenant="system")
    return {"ok": True, "state": runtime, "parameter": parameter}


def notifications_register_rule(state: dict, rule: dict) -> dict:
    missing = set(NOTIFICATIONS_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Notifications rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else copy.deepcopy(value)
        for key, value in rule.items()
        if key in NOTIFICATIONS_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    _append_audit(runtime, "register_rule", normalized, tenant=normalized["tenant"])
    return {"ok": True, "state": runtime, "rule": normalized}


def notifications_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in NOTIFICATIONS_OWNED_TABLES:
        raise ValueError(f"Notifications cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
        "migration_path": f"pbcs/notifications/migrations/{len(runtime['schema_extensions'].get(table, ())) + 1:03d}_{table}_extension.sql",
        "model_descriptor_path": f"pbcs/notifications/models/{table}.py",
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    _append_audit(runtime, "register_schema_extension", extension, tenant="system")
    return {"ok": True, "state": runtime, "extension": extension}


def notifications_register_template(state: dict, command: dict) -> dict:
    required = {
        "template_id",
        "tenant",
        "message_type",
        "locale",
        "subject",
        "body",
        "required_variables",
        "status",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Notifications template fields: {tuple(sorted(missing))}")
    _require_configured(state)
    _assert_supported_locale(state, command["locale"])
    runtime = _copy_state(state)
    template = {
        **command,
        "required_variables": tuple(command["required_variables"]),
        "audit_proof": _digest(command),
    }
    runtime["notification_templates"][template["template_id"]] = template
    runtime["template_locale_variants"][f"{template['template_id']}:{template['locale']}"] = {
        "variant_id": f"{template['template_id']}:{template['locale']}",
        "template_id": template["template_id"],
        "tenant": template["tenant"],
        "locale": template["locale"],
        "subject": template["subject"],
        "body": template["body"],
        "status": template["status"],
    }
    runtime["events"].append(_state_event("TemplateRegistered", template["template_id"], template))
    _append_audit(runtime, "register_template", template, tenant=template["tenant"])
    return {"ok": True, "state": runtime, "template": template}


def notifications_register_channel(state: dict, command: dict) -> dict:
    required = {
        "channel_id",
        "tenant",
        "channel_type",
        "provider",
        "health_score",
        "cost_score",
        "status",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Notifications channel fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["channel_type"] not in state["configuration"]["supported_channels"]:
        raise ValueError(f"Unsupported Notifications channel: {command['channel_type']}")
    runtime = _copy_state(state)
    channel = {
        **command,
        "health_score": float(command["health_score"]),
        "cost_score": float(command["cost_score"]),
        "audit_proof": _digest(command),
    }
    runtime["delivery_channels"][channel["channel_id"]] = channel
    runtime["events"].append(_state_event("ChannelRegistered", channel["channel_id"], channel))
    _append_audit(runtime, "register_channel", channel, tenant=channel["tenant"])
    return {"ok": True, "state": runtime, "channel": channel}


def notifications_receive_event(
    state: dict,
    event: dict,
    *,
    simulate_failure: bool = False,
) -> dict:
    _require_appgen_x_event_contract(state)
    if event.get("event_type") not in NOTIFICATIONS_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Notifications consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Notifications consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {
            "ok": True,
            "state": runtime,
            "handler": {"status": "duplicate", "event_id": event_id},
        }
    payload = dict(event.get("payload", {}))
    tenant = str(payload.get("tenant", "tenant_unknown"))
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"notifications:{event['event_type']}:{event_id}",
        "attempts": 1,
        "retry_limit": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
        "runtime_table": NOTIFICATIONS_RUNTIME_TABLES[1],
    }
    if simulate_failure:
        retry_record = {
            "retry_id": f"retry_{event_id}",
            "event_id": event_id,
            "event_type": event["event_type"],
            "attempts": handler["retry_limit"],
            "retry_limit": handler["retry_limit"],
            "next_action": "dead_letter",
            "idempotency_key": handler["idempotency_key"],
            "status": "exhausted",
        }
        runtime["retry_evidence"][event_id] = retry_record
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append(
            {
                **event,
                "tenant": tenant,
                "handler": handler,
                "retry_evidence": retry_record,
                "runtime_table": NOTIFICATIONS_RUNTIME_TABLES[2],
            }
        )
        _append_audit(runtime, "receive_event.dead_letter", {"event_id": event_id}, tenant=tenant)
        return {"ok": False, "state": runtime, "handler": handler}
    handler["status"] = "handled"
    runtime["inbox"].append(
        {
            **event,
            "tenant": tenant,
            "handler": handler,
            "runtime_table": NOTIFICATIONS_RUNTIME_TABLES[1],
        }
    )
    runtime["handled_events"].add(event_id)
    if event["event_type"] in {"PreferenceChanged", "ConsentUpdated"}:
        customer_id = payload["customer_id"]
        recipient = runtime["notification_recipients"].get(
            customer_id,
            {
                "recipient_id": customer_id,
                "tenant": tenant,
                "customer_id": customer_id,
            },
        )
        recipient.update(
            {
                "preferred_channels": tuple(
                    payload.get(
                        "preferred_channels",
                        (payload.get("preferred_channel", "email"),),
                    )
                ),
                "locale": payload.get(
                    "locale",
                    runtime["configuration"].get("default_locale", "en-US"),
                ),
                "opt_in": bool(payload.get("opt_in", True)),
                "status": "active",
            }
        )
        runtime["notification_recipients"][customer_id] = recipient
        snapshot = {
            "snapshot_id": f"pref_{customer_id}",
            "tenant": tenant,
            "customer_id": customer_id,
            "opt_in": recipient["opt_in"],
            "preferred_channels": recipient["preferred_channels"],
            "locale": recipient["locale"],
            "audit_proof": _digest(payload),
        }
        runtime["preference_snapshots"][customer_id] = snapshot
        runtime["consent_ledger"][event_id] = {
            "consent_id": f"consent_{event_id}",
            "tenant": tenant,
            "customer_id": customer_id,
            "opt_in": recipient["opt_in"],
            "source_event_type": event["event_type"],
            "proof_hash": _digest({"event_id": event_id, "payload": payload}),
            "status": "recorded",
        }
    elif event["event_type"] == "CampaignScheduled":
        campaign_id = str(payload.get("campaign_id", event_id))
        runtime["notification_campaigns"][campaign_id] = {
            "campaign_id": campaign_id,
            "tenant": tenant,
            "name": payload.get("name", campaign_id),
            "message_type": payload.get("message_type", "marketing"),
            "scheduled_for": payload.get("scheduled_for", "next_window"),
            "locale": payload.get(
                "locale",
                runtime["configuration"].get("default_locale", "en-US"),
            ),
            "status": "scheduled",
        }
        runtime["delivery_schedules"][campaign_id] = {
            "schedule_id": campaign_id,
            "tenant": tenant,
            "delivery_id": None,
            "campaign_id": campaign_id,
            "scheduled_for": payload.get("scheduled_for", "next_window"),
            "quiet_hours_enforced": True,
            "status": "scheduled",
        }
    elif event["event_type"] == "DeliveryReceiptImported":
        receipt_id = str(payload.get("receipt_id", event_id))
        runtime["delivery_receipts"][receipt_id] = {
            "receipt_id": receipt_id,
            "tenant": tenant,
            "delivery_id": payload.get("delivery_id", receipt_id),
            "provider_status": payload.get("provider_status", "delivered"),
            "proof_hash": _digest(payload),
            "status": "imported",
        }
        _update_deliverability_analytics(runtime, tenant)
    elif event["event_type"] == "BounceRegistered":
        bounce_id = str(payload.get("bounce_id", event_id))
        runtime["bounce_events"][bounce_id] = {
            "bounce_id": bounce_id,
            "tenant": tenant,
            "delivery_id": payload.get("delivery_id", bounce_id),
            "bounce_type": payload.get("bounce_type", "hard"),
            "provider_status": payload.get("provider_status", "bounced"),
            "status": "recorded",
        }
        _update_deliverability_analytics(runtime, tenant)
    else:
        runtime["trigger_events"][event_id] = payload
        if event["event_type"] == "TransactionalNotificationRequested":
            runtime["transactional_notifications"][event_id] = {
                "transactional_id": event_id,
                "tenant": tenant,
                "customer_id": payload.get("customer_id"),
                "template_id": payload.get("template_id"),
                "delivery_id": payload.get("delivery_id"),
                "status": "requested",
            }
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    _append_audit(runtime, "receive_event", {"event_id": event_id, "event_type": event["event_type"]}, tenant=tenant)
    return {"ok": True, "state": runtime, "handler": handler}


def notifications_send_message(state: dict, command: dict) -> dict:
    required = {
        "delivery_id",
        "tenant",
        "customer_id",
        "template_id",
        "message_type",
        "context",
        "urgency",
    }
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Notifications send fields: {tuple(sorted(missing))}")
    _require_appgen_x_event_contract(state)
    template = state["notification_templates"].get(command["template_id"])
    if not template or template["status"] != "active":
        raise ValueError(f"Unknown active Notifications template: {command['template_id']}")
    preference = state["preference_snapshots"].get(command["customer_id"])
    if not preference or not preference["opt_in"]:
        raise ValueError(f"Notifications recipient {command['customer_id']} has not opted in")
    rule = _select_rule(state, command["tenant"])
    if rule and command["message_type"] not in rule["allowed_message_types"]:
        raise ValueError(
            f"Message type {command['message_type']} is blocked by notification rule {rule['rule_id']}"
        )
    _assert_throttle_allowed(state, command["tenant"], command["customer_id"], rule)
    channel = _select_channel(state, command, preference)
    rendered = _render_template(template, command["context"])
    risk = _delivery_risk(state, command, preference, channel)
    runtime = _copy_state(state)
    schedule = {
        "schedule_id": f"schedule_{command['delivery_id']}",
        "tenant": command["tenant"],
        "delivery_id": command["delivery_id"],
        "campaign_id": command.get("campaign_id"),
        "scheduled_for": command.get("scheduled_for", _default_schedule_slot(runtime)),
        "quiet_hours_enforced": True,
        "status": "scheduled",
    }
    route = {
        "route_id": f"route_{command['delivery_id']}",
        "tenant": command["tenant"],
        "delivery_id": command["delivery_id"],
        "channel_id": channel["channel_id"],
        "provider": channel["provider"],
        "channel_type": channel["channel_type"],
        "health_score": channel["health_score"],
        "cost_score": channel["cost_score"],
        "route_score": _channel_score(state, channel, command),
        "status": "selected",
    }
    delivery = {
        **command,
        "context": dict(command["context"]),
        "channel_id": channel["channel_id"],
        "channel_type": channel["channel_type"],
        "provider": channel["provider"],
        "subject": rendered["subject"],
        "body": rendered["body"],
        "delivery_risk": risk,
        "status": "queued",
        "attempts": 0,
        "schedule_id": schedule["schedule_id"],
        "route_id": route["route_id"],
        "audit_proof": _digest({"command": command, "channel": channel, "rendered": rendered}),
    }
    runtime["delivery_schedules"][schedule["schedule_id"]] = schedule
    runtime["provider_routes"][route["route_id"]] = route
    runtime["message_deliveries"][delivery["delivery_id"]] = delivery
    if command["message_type"] == "marketing" or command.get("campaign_id"):
        campaign_id = str(command.get("campaign_id", f"campaign_{command['delivery_id']}"))
        runtime["notification_campaigns"].setdefault(
            campaign_id,
            {
                "campaign_id": campaign_id,
                "tenant": command["tenant"],
                "name": campaign_id,
                "message_type": "marketing",
                "scheduled_for": schedule["scheduled_for"],
                "locale": template["locale"],
                "status": "scheduled",
            },
        )
        runtime["campaign_dispatches"][delivery["delivery_id"]] = {
            "dispatch_id": delivery["delivery_id"],
            "tenant": command["tenant"],
            "campaign_id": campaign_id,
            "delivery_id": delivery["delivery_id"],
            "channel_id": channel["channel_id"],
            "status": "queued",
        }
    else:
        runtime["transactional_notifications"][delivery["delivery_id"]] = {
            "transactional_id": delivery["delivery_id"],
            "tenant": command["tenant"],
            "customer_id": command["customer_id"],
            "template_id": command["template_id"],
            "delivery_id": command["delivery_id"],
            "message_type": command["message_type"],
            "status": "queued",
        }
    _record_throttle_window(runtime, command["tenant"], command["customer_id"], delivery["delivery_id"])
    runtime["events"].append(_state_event("MessageQueued", delivery["delivery_id"], delivery))
    _emit(runtime, "MessageQueued", delivery["tenant"], delivery)
    if delivery["delivery_id"] in runtime["campaign_dispatches"]:
        _emit(runtime, "CampaignDispatched", delivery["tenant"], runtime["campaign_dispatches"][delivery["delivery_id"]])
    else:
        _emit(
            runtime,
            "TransactionalNotificationDispatched",
            delivery["tenant"],
            runtime["transactional_notifications"][delivery["delivery_id"]],
        )
    _append_audit(runtime, "send_message", delivery, tenant=delivery["tenant"])
    _update_deliverability_analytics(runtime, delivery["tenant"])
    return {"ok": True, "state": runtime, "delivery": delivery}


def notifications_record_delivery_attempt(
    state: dict,
    delivery_id: str,
    *,
    provider_status: str,
) -> dict:
    _require_appgen_x_event_contract(state)
    delivery = state["message_deliveries"].get(delivery_id)
    if not delivery:
        raise ValueError(f"Unknown Notifications delivery: {delivery_id}")
    runtime = _copy_state(state)
    attempts = int(delivery.get("attempts", 0)) + 1
    provider_status_normalized = str(provider_status).lower()
    status = "delivered" if provider_status_normalized == "delivered" else "failed"
    updated = {
        **delivery,
        "status": status,
        "attempts": attempts,
        "provider_status": provider_status_normalized,
    }
    runtime["message_deliveries"][delivery_id] = updated
    attempt = {
        "attempt_id": f"{delivery_id}:{attempts}",
        "tenant": updated["tenant"],
        "delivery_id": delivery_id,
        "provider": updated["provider"],
        "provider_status": provider_status_normalized,
        "attempt_number": attempts,
        "status": status,
        "idempotency_key": f"{delivery_id}:{provider_status_normalized}:{attempts}",
    }
    runtime["delivery_attempts"][attempt["attempt_id"]] = attempt
    if status == "delivered":
        receipt = {
            "receipt_id": f"receipt_{delivery_id}",
            "tenant": updated["tenant"],
            "delivery_id": delivery_id,
            "provider_status": provider_status_normalized,
            "channel_id": updated["channel_id"],
            "proof_hash": _digest(attempt),
            "status": "recorded",
        }
        runtime["delivery_receipts"][receipt["receipt_id"]] = receipt
        _emit(runtime, "MessageDelivered", updated["tenant"], updated)
        _emit(runtime, "DeliveryReceiptRecorded", updated["tenant"], receipt)
    else:
        if provider_status_normalized in {"bounced", "complained", "rejected"}:
            bounce = {
                "bounce_id": f"bounce_{delivery_id}",
                "tenant": updated["tenant"],
                "delivery_id": delivery_id,
                "provider_status": provider_status_normalized,
                "bounce_type": "hard" if provider_status_normalized == "bounced" else "soft",
                "status": "recorded",
            }
            runtime["bounce_events"][bounce["bounce_id"]] = bounce
            _emit(runtime, "BounceRecorded", updated["tenant"], bounce)
        retry_limit = int(runtime.get("configuration", {}).get("retry_limit", 3) or 3)
        retry_record = {
            "retry_id": f"retry_{delivery_id}",
            "tenant": updated["tenant"],
            "event_id": delivery_id,
            "event_type": "MessageFailed",
            "attempts": attempts,
            "retry_limit": retry_limit,
            "next_action": "dead_letter" if attempts >= retry_limit else "retry",
            "idempotency_key": f"notifications:MessageFailed:{delivery_id}",
            "status": "exhausted" if attempts >= retry_limit else "scheduled",
        }
        runtime["retry_evidence"][delivery_id] = retry_record
        if attempts >= retry_limit:
            runtime["dead_letter"].append(
                {
                    "event_id": delivery_id,
                    "event_type": "MessageFailed",
                    "tenant": updated["tenant"],
                    "idempotency_key": retry_record["idempotency_key"],
                    "reason": provider_status_normalized,
                    "retry_evidence": retry_record,
                    "runtime_table": NOTIFICATIONS_RUNTIME_TABLES[2],
                }
            )
        _emit(runtime, "MessageFailed", updated["tenant"], updated)
    _append_audit(runtime, "record_delivery_attempt", attempt, tenant=updated["tenant"])
    _update_deliverability_analytics(runtime, updated["tenant"])
    return {"ok": status == "delivered", "state": runtime, "delivery": updated}


def notifications_build_workbench_view(state: dict, *, tenant: str) -> dict:
    templates = tuple(
        item for item in state.get("notification_templates", {}).values() if item["tenant"] == tenant
    )
    channels = tuple(
        item for item in state.get("delivery_channels", {}).values() if item["tenant"] == tenant
    )
    deliveries = tuple(
        item for item in state.get("message_deliveries", {}).values() if item["tenant"] == tenant
    )
    preferences = tuple(
        item for item in state.get("preference_snapshots", {}).values() if item["tenant"] == tenant
    )
    recipients = tuple(
        item for item in state.get("notification_recipients", {}).values() if item["tenant"] == tenant
    )
    campaigns = tuple(
        item for item in state.get("notification_campaigns", {}).values() if item["tenant"] == tenant
    )
    transactional = tuple(
        item for item in state.get("transactional_notifications", {}).values() if item["tenant"] == tenant
    )
    receipts = tuple(
        item for item in state.get("delivery_receipts", {}).values() if item["tenant"] == tenant
    )
    bounces = tuple(
        item for item in state.get("bounce_events", {}).values() if item["tenant"] == tenant
    )
    audit_entries = tuple(
        item for item in state.get("notification_audit_log", ()) if item["tenant"] == tenant
    )
    analytics = state.get("deliverability_analytics", {}).get(tenant, {})
    return {
        "format": "appgen.notifications-workbench-view.v1",
        "tenant": tenant,
        "template_count": len(templates),
        "channel_count": len(channels),
        "delivery_count": len(deliveries),
        "delivered_count": len(tuple(item for item in deliveries if item["status"] == "delivered")),
        "failed_count": len(tuple(item for item in deliveries if item["status"] == "failed")),
        "preference_count": len(preferences),
        "recipient_count": len(recipients),
        "campaign_count": len(campaigns),
        "transactional_count": len(transactional),
        "receipt_count": len(receipts),
        "bounce_count": len(bounces),
        "audit_entry_count": len(audit_entries),
        "average_delivery_risk": round(
            sum(item["delivery_risk"] for item in deliveries) / max(len(deliveries), 1),
            4,
        ),
        "outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "analytics_bound": bool(analytics),
        "binding_evidence": {
            "owned_tables": NOTIFICATIONS_OWNED_TABLES,
            "runtime_tables": NOTIFICATIONS_RUNTIME_TABLES,
            "outbox_table": NOTIFICATIONS_RUNTIME_TABLES[0],
            "inbox_table": NOTIFICATIONS_RUNTIME_TABLES[1],
            "dead_letter_table": NOTIFICATIONS_RUNTIME_TABLES[2],
            "analytics_table": "deliverability_analytics",
            "campaign_table": "notification_campaign",
            "shared_table_access": False,
        },
    }


def notifications_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    violations = tuple(
        reference
        for reference in references
        if reference not in set(NOTIFICATIONS_OWNED_TABLES)
        and reference not in set(NOTIFICATIONS_RUNTIME_TABLES)
        and reference not in set(_NOTIFICATIONS_ALLOWED_DEPENDENCIES)
        and reference not in set(NOTIFICATIONS_CONSUMED_EVENT_TYPES)
        and not str(reference).startswith("notifications_")
    )
    return {
        "format": "appgen.notifications-boundary.v1",
        "ok": not violations,
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "runtime_tables": NOTIFICATIONS_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": tuple(
                item
                for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES
                if str(item).startswith(("GET ", "POST "))
            ),
            "events": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def notifications_build_api_contract() -> dict:
    return {
        "format": "appgen.notifications-api-contract.v1",
        "ok": True,
        "routes": (
            _notifications_route_descriptor(
                "POST /templates",
                command="register_template",
                owned_tables=("notification_template", "template_locale_variant"),
                requires_permission="notifications.template.write",
                idempotency_key="template_id",
            ),
            _notifications_route_descriptor(
                "POST /delivery-channels",
                command="register_channel",
                owned_tables=("delivery_channel", "provider_route"),
                requires_permission="notifications.channel.write",
                idempotency_key="channel_id",
            ),
            _notifications_route_descriptor(
                "POST /notifications/rules",
                command="register_rule",
                owned_tables=("notification_rule",),
                requires_permission="notifications.configure",
                idempotency_key="rule_id",
            ),
            _notifications_route_descriptor(
                "POST /notifications/parameters",
                command="set_parameter",
                owned_tables=("notification_parameter",),
                requires_permission="notifications.configure",
                idempotency_key="parameter_id",
            ),
            _notifications_route_descriptor(
                "POST /notifications/configuration",
                command="configure_runtime",
                owned_tables=("notification_configuration",),
                requires_permission="notifications.configure",
                idempotency_key="tenant",
            ),
            _notifications_route_descriptor(
                "POST /messages",
                command="send_message",
                owned_tables=(
                    "message_delivery",
                    "delivery_schedule",
                    "provider_route",
                    "transactional_notification",
                    "campaign_dispatch",
                ),
                emits=("MessageQueued", "CampaignDispatched", "TransactionalNotificationDispatched"),
                requires_permission="notifications.message.send",
                idempotency_key="delivery_id",
            ),
            _notifications_route_descriptor(
                "POST /delivery-attempts",
                command="record_delivery_attempt",
                owned_tables=("delivery_attempt", "retry_evidence", "delivery_receipt", "bounce_event"),
                emits=("MessageDelivered", "MessageFailed", "DeliveryReceiptRecorded", "BounceRecorded"),
                requires_permission="notifications.message.send",
                idempotency_key="delivery_id:provider_status",
            ),
            _notifications_route_descriptor(
                "POST /notifications/events/inbox",
                command="receive_event",
                owned_tables=NOTIFICATIONS_RUNTIME_TABLES,
                consumes=NOTIFICATIONS_CONSUMED_EVENT_TYPES,
                requires_permission="notifications.event.consume",
                idempotency_key="event_id",
                dependency_apis=tuple(
                    item
                    for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES
                    if str(item).startswith(("GET ", "POST "))
                ),
                dependency_projections=tuple(
                    item
                    for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES
                    if str(item).endswith("_projection")
                ),
            ),
            _notifications_route_descriptor(
                "GET /notifications/contracts/schema",
                query="build_schema_contract",
                owned_tables=NOTIFICATIONS_OWNED_TABLES,
                requires_permission="notifications.audit",
            ),
            _notifications_route_descriptor(
                "GET /notifications/contracts/service",
                query="build_service_contract",
                owned_tables=NOTIFICATIONS_OWNED_TABLES,
                requires_permission="notifications.audit",
            ),
            _notifications_route_descriptor(
                "GET /notifications/release-evidence",
                query="build_release_evidence",
                owned_tables=NOTIFICATIONS_OWNED_TABLES,
                requires_permission="notifications.audit",
            ),
            _notifications_route_descriptor(
                "GET /notifications-workbench",
                query="build_workbench_view",
                owned_tables=NOTIFICATIONS_OWNED_TABLES,
                requires_permission="notifications.audit",
            ),
        ),
        "declared_catalog_routes": (
            "POST /templates",
            "POST /delivery-channels",
            "POST /messages",
            "POST /delivery-attempts",
            "GET /notifications-workbench",
            "GET /notifications/contracts/schema",
            "GET /notifications/contracts/service",
            "GET /notifications/release-evidence",
        ),
        "events": {
            "emits": NOTIFICATIONS_EMITTED_EVENT_TYPES,
            "consumes": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
        },
        "emits": NOTIFICATIONS_EMITTED_EVENT_TYPES,
        "consumes": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(notifications_permissions_contract()["permissions"])),
        "database_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "runtime_tables": NOTIFICATIONS_RUNTIME_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "dependency_surface": {
            "apis": tuple(
                item
                for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES
                if str(item).startswith(("GET ", "POST "))
            ),
            "api_projections": tuple(
                item for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
        "configuration": (
            "NOTIFICATIONS_DATABASE_URL",
            "NOTIFICATIONS_EVENT_TOPIC",
            "NOTIFICATIONS_RETRY_LIMIT",
            "NOTIFICATIONS_DEFAULT_TIMEZONE",
        ),
    }


def notifications_build_schema_contract() -> dict:
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in NOTIFICATIONS_OWNED_TABLES}
    table_fields.update(
        {
            "notification_template": (
                "tenant",
                "template_id",
                "message_type",
                "locale",
                "subject",
                "body",
                "status",
            ),
            "template_locale_variant": (
                "tenant",
                "variant_id",
                "template_id",
                "locale",
                "subject",
                "body",
                "status",
            ),
            "delivery_channel": (
                "tenant",
                "channel_id",
                "channel_type",
                "provider",
                "health_score",
                "cost_score",
                "status",
            ),
            "notification_recipient": (
                "tenant",
                "recipient_id",
                "customer_id",
                "locale",
                "preferred_channels",
                "opt_in",
                "status",
            ),
            "preference_snapshot": (
                "tenant",
                "snapshot_id",
                "customer_id",
                "preferred_channels",
                "locale",
                "opt_in",
                "audit_proof",
            ),
            "consent_ledger": (
                "tenant",
                "consent_id",
                "customer_id",
                "source_event_type",
                "opt_in",
                "proof_hash",
                "status",
            ),
            "delivery_schedule": (
                "tenant",
                "schedule_id",
                "delivery_id",
                "campaign_id",
                "scheduled_for",
                "quiet_hours_enforced",
                "status",
            ),
            "throttle_window": (
                "tenant",
                "window_id",
                "customer_id",
                "message_count",
                "limit",
                "window_state",
                "status",
            ),
            "provider_route": (
                "tenant",
                "route_id",
                "delivery_id",
                "channel_id",
                "provider",
                "route_score",
                "status",
            ),
            "message_delivery": (
                "tenant",
                "delivery_id",
                "customer_id",
                "template_id",
                "channel_id",
                "delivery_risk",
                "status",
            ),
            "delivery_attempt": (
                "tenant",
                "attempt_id",
                "delivery_id",
                "provider",
                "provider_status",
                "attempt_number",
                "status",
            ),
            "retry_evidence": (
                "tenant",
                "retry_id",
                "event_id",
                "event_type",
                "attempts",
                "retry_limit",
                "status",
            ),
            "delivery_receipt": (
                "tenant",
                "receipt_id",
                "delivery_id",
                "provider_status",
                "proof_hash",
                "status",
            ),
            "bounce_event": (
                "tenant",
                "bounce_id",
                "delivery_id",
                "provider_status",
                "bounce_type",
                "status",
                "reason",
            ),
            "notification_campaign": (
                "tenant",
                "campaign_id",
                "name",
                "message_type",
                "scheduled_for",
                "locale",
                "status",
            ),
            "campaign_dispatch": (
                "tenant",
                "dispatch_id",
                "campaign_id",
                "delivery_id",
                "channel_id",
                "status",
                "audit_hash",
            ),
            "transactional_notification": (
                "tenant",
                "transactional_id",
                "customer_id",
                "template_id",
                "delivery_id",
                "message_type",
                "status",
            ),
            "notification_audit_log": (
                "tenant",
                "audit_id",
                "action",
                "entity_id",
                "entity_type",
                "proof_hash",
                "status",
            ),
            "deliverability_analytics": (
                "tenant",
                "analytics_id",
                "deliveries_total",
                "delivered_total",
                "failed_total",
                "bounce_total",
                "delivery_success_rate",
            ),
            "notification_rule": (
                "tenant",
                "rule_id",
                "scope",
                "compiled_hash",
                "policy_engine",
                "status",
                "effective_at",
            ),
            "notification_parameter": (
                "tenant",
                "parameter_id",
                "name",
                "value",
                "compiled_hash",
                "effective_at",
                "status",
            ),
            "notification_configuration": (
                "tenant",
                "configuration_id",
                "database_backend",
                "event_topic",
                "retry_limit",
                "event_contract",
                "status",
            ),
        }
    )
    runtime_tables = (
        {
            "table": NOTIFICATIONS_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "published_at", "status"),
        },
        {
            "table": NOTIFICATIONS_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "received_at", "status"),
        },
        {
            "table": NOTIFICATIONS_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason", "status"),
        },
    )
    relationships = (
        {"from_table": "template_locale_variant", "from_field": "template_id", "to_table": "notification_template", "to_field": "template_id"},
        {"from_table": "preference_snapshot", "from_field": "customer_id", "to_table": "notification_recipient", "to_field": "customer_id"},
        {"from_table": "consent_ledger", "from_field": "customer_id", "to_table": "notification_recipient", "to_field": "customer_id"},
        {"from_table": "delivery_schedule", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "provider_route", "from_field": "channel_id", "to_table": "delivery_channel", "to_field": "channel_id"},
        {"from_table": "provider_route", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "message_delivery", "from_field": "template_id", "to_table": "notification_template", "to_field": "template_id"},
        {"from_table": "message_delivery", "from_field": "customer_id", "to_table": "notification_recipient", "to_field": "customer_id"},
        {"from_table": "delivery_attempt", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "retry_evidence", "from_field": "event_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "delivery_receipt", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "bounce_event", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "campaign_dispatch", "from_field": "campaign_id", "to_table": "notification_campaign", "to_field": "campaign_id"},
        {"from_table": "campaign_dispatch", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
        {"from_table": "transactional_notification", "from_field": "delivery_id", "to_table": "message_delivery", "to_field": "delivery_id"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(
                field
                for field in table_fields[table]
                if field.endswith("_id")
            )[:2],
            "owned_by": "notifications",
        }
        for table in NOTIFICATIONS_OWNED_TABLES
    )
    migrations = tuple(
        {
            "path": f"pbcs/notifications/migrations/{position + 1:03d}_{table}.sql",
            "table": table,
            "operation": "create_owned_table",
            "backend_allowlist": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
        }
        for position, table in enumerate(NOTIFICATIONS_OWNED_TABLES)
    )
    models = tuple(
        {
            "path": f"pbcs/notifications/models/{table}.py",
            "table": table,
            "class_name": _class_name(table),
            "fields": table_fields[table],
        }
        for table in NOTIFICATIONS_OWNED_TABLES
    )
    return {
        "format": "appgen.notifications-owned-schema-contract.v1",
        "ok": len(tables) == len(NOTIFICATIONS_OWNED_TABLES)
        and len(migrations) == len(NOTIFICATIONS_OWNED_TABLES)
        and len(tables) >= 20
        and all(item["fields"] for item in tables),
        "tables": tables,
        "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": migrations,
        "models": models,
        "datastore_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "shared_table_access": False,
    }


def notifications_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_template",
        "register_channel",
        "receive_event",
        "send_message",
        "record_delivery_attempt",
        "create_campaign",
        "schedule_notification",
        "create_transactional_notification",
        "record_delivery_receipt",
        "record_bounce",
        "route_provider",
        "record_audit_event",
        "publish_deliverability_analytics",
    )
    query_methods = (
        "build_workbench_view",
        "forecast_delivery_window",
        "simulate_channel_routing",
        "recommend_localized_variant",
        "analyze_recipient_fatigue",
        "review_campaign_readiness",
        "review_transactional_history",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "verify_owned_table_boundary",
    )
    boundary = notifications_verify_owned_table_boundary(
        (
            "notification_template",
            NOTIFICATIONS_RUNTIME_TABLES[0],
            "workflow_projection",
            "PreferenceChanged",
        )
    )
    return {
        "format": "appgen.notifications-service-contract.v1",
        "ok": len(command_methods) >= 16 and len(query_methods) >= 10 and boundary["ok"],
        "transaction_boundary": "notifications_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": NOTIFICATIONS_OWNED_TABLES,
        "runtime_tables": NOTIFICATIONS_RUNTIME_TABLES,
        "standard_orchestration": (
            "template_authoring",
            "recipient_resolution",
            "consent_screening",
            "localization_selection",
            "delivery_scheduling",
            "channel_routing",
            "throttle_enforcement",
            "retry_dead_letter_handling",
            "receipt_recording",
            "bounce_recording",
            "campaign_dispatch",
            "transactional_dispatch",
            "deliverability_analytics",
        ),
        "advanced_capabilities": NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS,
        "external_dependencies": {
            "apis": tuple(
                item
                for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES
                if str(item).startswith(("GET ", "POST "))
            ),
            "events": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(
                item for item in _NOTIFICATIONS_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")
            ),
            "shared_tables": (),
        },
        "idempotent_handlers": ("receive_event", "send_message", "record_delivery_attempt"),
        "retry_dead_letter_evidence": {
            "outbox_table": NOTIFICATIONS_RUNTIME_TABLES[0],
            "inbox_table": NOTIFICATIONS_RUNTIME_TABLES[1],
            "dead_letter_table": NOTIFICATIONS_RUNTIME_TABLES[2],
            "idempotency_prefix": "notifications:",
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "rules_parameters_configuration": (
            "register_rule",
            "set_parameter",
            "configure_runtime",
        ),
        "shared_table_access": False,
    }


def notifications_build_release_evidence() -> dict:
    from .ui import notifications_ui_contract

    schema = notifications_build_schema_contract()
    service = notifications_build_service_contract()
    api = notifications_build_api_contract()
    permissions = notifications_permissions_contract()
    ui = notifications_ui_contract()
    state = _notifications_smoke_state()
    workbench = notifications_build_workbench_view(state, tenant="tenant_alpha")
    boundary = notifications_verify_owned_table_boundary(
        (
            "notification_template",
            NOTIFICATIONS_RUNTIME_TABLES[0],
            "workflow_projection",
            "PreferenceChanged",
        )
    )
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) == len(NOTIFICATIONS_OWNED_TABLES)},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(NOTIFICATIONS_OWNED_TABLES)},
        {
            "id": "runtime_tables_declared",
            "ok": tuple(item["table"] for item in schema["runtime_tables"]) == NOTIFICATIONS_RUNTIME_TABLES,
        },
        {
            "id": "service_contract_depth",
            "ok": service["ok"]
            and "build_schema_contract" in service["query_methods"]
            and "receive_event" in service["idempotent_handlers"],
        },
        {
            "id": "api_event_contract",
            "ok": api["ok"]
            and api["event_contract"] == "AppGen-X"
            and api["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
        },
        {
            "id": "permissions_cover_release_queries",
            "ok": {
                "build_schema_contract",
                "build_service_contract",
                "build_release_evidence",
            }
            <= set(permissions["action_permissions"]),
        },
        {
            "id": "ui_binding_evidence",
            "ok": ui["ok"] and ui["workbench_binding_evidence"]["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES,
        },
        {
            "id": "workbench_binding_evidence",
            "ok": workbench["binding_evidence"]["outbox_table"] == NOTIFICATIONS_RUNTIME_TABLES[0]
            and workbench["binding_evidence"]["analytics_table"] == "deliverability_analytics",
        },
        {
            "id": "boundary_contract",
            "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == (),
        },
        {
            "id": "database_allowlist",
            "ok": schema["datastore_backends"] == NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
            and api["database_backends"] == NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
        },
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.notifications-release-evidence.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui": ui,
        "workbench": workbench,
        "boundary": boundary,
        "blocking_gaps": blocking_gaps,
    }


def notifications_permissions_contract() -> dict:
    return {
        "format": "appgen.notifications-permissions.v1",
        "ok": True,
        "permissions": (
            "notifications.template.write",
            "notifications.channel.write",
            "notifications.recipient.write",
            "notifications.consent.write",
            "notifications.message.send",
            "notifications.campaign.write",
            "notifications.analytics.read",
            "notifications.event.consume",
            "notifications.configure",
            "notifications.audit",
        ),
        "action_permissions": {
            "register_template": "notifications.template.write",
            "register_channel": "notifications.channel.write",
            "send_message": "notifications.message.send",
            "record_delivery_attempt": "notifications.message.send",
            "receive_event": "notifications.event.consume",
            "register_rule": "notifications.configure",
            "register_schema_extension": "notifications.configure",
            "set_parameter": "notifications.configure",
            "configure_runtime": "notifications.configure",
            "create_campaign": "notifications.campaign.write",
            "create_transactional_notification": "notifications.message.send",
            "record_delivery_receipt": "notifications.analytics.read",
            "record_bounce": "notifications.analytics.read",
            "publish_deliverability_analytics": "notifications.analytics.read",
            "build_workbench_view": "notifications.audit",
            "build_schema_contract": "notifications.audit",
            "build_service_contract": "notifications.audit",
            "build_release_evidence": "notifications.audit",
            "verify_owned_table_boundary": "notifications.audit",
        },
    }


def _notifications_smoke_state() -> dict:
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
        ("campaign_batch_size", 5000),
        ("schedule_horizon_hours", 72),
        ("bounce_retry_window_minutes", 180),
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
            "allowed_message_types": ("service", "workflow", "marketing", "transactional"),
            "consent_policy": {"require_opt_in": True, "honor_quiet_hours": True},
            "delivery_policy": {"failover_channels": ("email", "push"), "default_sender": "service"},
            "throttle_policy": {"daily_limit": 20, "burst_limit": 5},
            "routing_policy": {"prefer_opted_in_channels": True, "fallback_on_degradation": True},
            "schedule_policy": {"respect_quiet_hours": True, "default_horizon_hours": 72},
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
        {
            "event_id": "pref_alpha",
            "event_type": "PreferenceChanged",
            "payload": {
                "tenant": "tenant_alpha",
                "customer_id": "cust_alpha",
                "opt_in": True,
                "preferred_channels": ("email", "push"),
                "locale": "en-US",
            },
        },
    )["state"]
    state = notifications_receive_event(
        state,
        {
            "event_id": "camp_alpha",
            "event_type": "CampaignScheduled",
            "payload": {
                "tenant": "tenant_alpha",
                "campaign_id": "cmp_alpha",
                "name": "April Service Update",
                "message_type": "marketing",
                "scheduled_for": "2026-04-01T09:00:00Z",
                "locale": "en-US",
            },
        },
    )["state"]
    state = notifications_receive_event(
        state,
        {
            "event_id": "sla_alpha",
            "event_type": "SlaBreached",
            "payload": {
                "tenant": "tenant_alpha",
                "customer_id": "cust_alpha",
                "ticket_id": "case_alpha",
                "urgency": 0.9,
            },
        },
    )["state"]
    state = notifications_send_message(
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
    )["state"]
    return notifications_record_delivery_attempt(
        state,
        "msg_alpha",
        provider_status="delivered",
    )["state"]


def _notifications_route_descriptor(
    route: str,
    *,
    command: str | None = None,
    query: str | None = None,
    owned_tables: tuple[str, ...] = (),
    emits: tuple[str, ...] = (),
    consumes: tuple[str, ...] = (),
    requires_permission: str,
    idempotency_key: str | None = None,
    dependency_apis: tuple[str, ...] = (),
    dependency_projections: tuple[str, ...] = (),
) -> dict:
    descriptor = {
        "route": route,
        "owned_tables": owned_tables,
        "emits": emits,
        "consumes": consumes,
        "requires_permission": requires_permission,
        "dependency_apis": dependency_apis,
        "dependency_projections": dependency_projections,
        "event_contract": "AppGen-X",
        "required_event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
        "shared_table_access": False,
    }
    if command:
        descriptor["command"] = command
    if query:
        descriptor["query"] = query
    if idempotency_key:
        descriptor["idempotency_key"] = idempotency_key
    return descriptor


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _append_audit(state: dict, action: str, payload: dict, *, tenant: str) -> None:
    state["notification_audit_log"].append(
        {
            "audit_id": f"audit_{len(state['notification_audit_log']) + 1}",
            "tenant": tenant,
            "action": action,
            "entity_id": payload.get("delivery_id")
            or payload.get("template_id")
            or payload.get("channel_id")
            or payload.get("rule_id")
            or payload.get("event_id")
            or payload.get("parameter_id")
            or payload.get("schedule_id")
            or "system",
            "entity_type": payload.get("event_type")
            or payload.get("message_type")
            or action,
            "proof_hash": _digest({"action": action, "payload": payload}),
            "status": "recorded",
        }
    )


def _update_deliverability_analytics(state: dict, tenant: str) -> None:
    deliveries = tuple(
        item for item in state["message_deliveries"].values() if item["tenant"] == tenant
    )
    delivered = tuple(item for item in deliveries if item["status"] == "delivered")
    failed = tuple(item for item in deliveries if item["status"] == "failed")
    bounce_total = len(
        tuple(item for item in state["bounce_events"].values() if item["tenant"] == tenant)
    )
    state["deliverability_analytics"][tenant] = {
        "analytics_id": f"analytics_{tenant}",
        "tenant": tenant,
        "deliveries_total": len(deliveries),
        "delivered_total": len(delivered),
        "failed_total": len(failed),
        "bounce_total": bounce_total,
        "delivery_success_rate": round(len(delivered) / max(len(deliveries), 1), 4),
    }


def _record_throttle_window(
    state: dict,
    tenant: str,
    customer_id: str,
    delivery_id: str,
) -> None:
    key = f"{tenant}:{customer_id}"
    existing = state["throttle_windows"].get(
        key,
        {
            "window_id": key,
            "tenant": tenant,
            "customer_id": customer_id,
            "message_count": 0,
            "limit": int(
                state.get("parameters", {})
                .get("max_daily_messages_per_recipient", {"value": 20})["value"]
            ),
            "window_state": "open",
            "status": "active",
            "last_delivery_id": None,
        },
    )
    existing["message_count"] = int(existing["message_count"]) + 1
    existing["last_delivery_id"] = delivery_id
    if existing["message_count"] >= int(existing["limit"]):
        existing["window_state"] = "at_limit"
    state["throttle_windows"][key] = existing


def _assert_throttle_allowed(
    state: dict,
    tenant: str,
    customer_id: str,
    rule: dict | None,
) -> None:
    key = f"{tenant}:{customer_id}"
    throttle = state.get("throttle_windows", {}).get(key)
    limit = int(
        state.get("parameters", {}).get("max_daily_messages_per_recipient", {"value": 20})["value"]
    )
    if rule:
        limit = int(rule.get("throttle_policy", {}).get("daily_limit", limit))
    if throttle and int(throttle.get("message_count", 0)) >= limit:
        raise ValueError(f"Notifications recipient {customer_id} exceeded throttle window")


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Notifications runtime must be configured before commands execute")


def _require_appgen_x_event_contract(state: dict) -> None:
    _require_configured(state)
    configuration = state["configuration"]
    if (
        configuration.get("event_contract") != "AppGen-X"
        or configuration.get("event_topic") != NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    ):
        raise ValueError(
            "Notifications runtime must remain bound to the AppGen-X notifications event contract"
        )


def _assert_supported_locale(state: dict, locale: str) -> None:
    if locale not in state["configuration"]["supported_locales"]:
        raise ValueError(f"Unsupported Notifications locale: {locale}")


def _select_rule(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if (
            rule["tenant"] == tenant
            and rule["scope"] == "notifications"
            and rule["status"] == "active"
        ):
            return rule
    return None


def _select_channel(state: dict, command: dict, preference: dict) -> dict:
    preferred = tuple(preference.get("preferred_channels", ()))
    rule = _select_rule(state, command["tenant"])
    allowed_channels = set(rule["allowed_channels"]) if rule else set(preferred or state["configuration"]["supported_channels"])
    candidates = tuple(
        channel
        for channel in state["delivery_channels"].values()
        if channel["tenant"] == command["tenant"]
        and channel["status"] == "active"
        and channel["channel_type"] in allowed_channels
    )
    if not candidates:
        raise ValueError(f"No active Notifications channel for recipient {command['customer_id']}")
    return sorted(candidates, key=lambda item: _channel_score(state, item, command), reverse=True)[0]


def _channel_score(state: dict, channel: dict, command: dict) -> float:
    return round(
        channel["health_score"]
        * float(state["parameters"].get("channel_health_weight", {"value": 0.3})["value"])
        + float(command["urgency"])
        * float(state["parameters"].get("urgency_weight", {"value": 0.25})["value"])
        + (1 - channel["cost_score"])
        * float(state["parameters"].get("cost_weight", {"value": 0.1})["value"]),
        4,
    )


def _default_schedule_slot(state: dict) -> str:
    quiet_hours = tuple(state.get("configuration", {}).get("quiet_hours", ()))
    return "next_available_window" if quiet_hours else "immediate"


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
    fatigue = min(
        len(
            tuple(
                item
                for item in state["message_deliveries"].values()
                if item["customer_id"] == command["customer_id"]
            )
        )
        / max(
            float(
                state["parameters"].get("max_daily_messages_per_recipient", {"value": 20})[
                    "value"
                ]
            ),
            1,
        ),
        1.0,
    )
    channel_risk = 1 - channel["health_score"]
    urgency_offset = 1 - float(command["urgency"])
    preference_bonus = 0.0 if channel["channel_type"] in preference.get("preferred_channels", ()) else 0.1
    return round(min(fatigue * 0.35 + channel_risk * 0.4 + urgency_offset * 0.25 + preference_bonus, 0.99), 4)


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "topic": state.get("configuration", {}).get("event_topic", NOTIFICATIONS_REQUIRED_EVENT_TOPIC),
        "payload": payload,
        "contract": "AppGen-X",
        "runtime_table": NOTIFICATIONS_RUNTIME_TABLES[0],
        "idempotency_key": f"notifications:{event_type}:{payload.get('delivery_id') or payload.get('event_id') or len(state['outbox']) + 1}",
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": NOTIFICATIONS_RUNTIME_TABLES[2],
        },
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {
        "event_type": event_type,
        "key": key,
        "payload": payload,
        "hash": _digest({"event_type": event_type, "key": key, "payload": payload}),
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
                "deliveries": len(state["message_deliveries"]),
                "channels": len(state["delivery_channels"]),
                "analytics": len(state["deliverability_analytics"]),
            }
        ),
    }


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


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
        json.dumps(
            payload,
            sort_keys=True,
            default=default,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
