import pytest

from pyAppGen.pbc import notifications_build_api_contract
from pyAppGen.pbc import notifications_build_workbench_view
from pyAppGen.pbc import notifications_configure_runtime
from pyAppGen.pbc import notifications_empty_state
from pyAppGen.pbc import notifications_permissions_contract
from pyAppGen.pbc import notifications_receive_event
from pyAppGen.pbc import notifications_record_delivery_attempt
from pyAppGen.pbc import notifications_register_channel
from pyAppGen.pbc import notifications_register_rule
from pyAppGen.pbc import notifications_register_template
from pyAppGen.pbc import notifications_render_workbench
from pyAppGen.pbc import notifications_runtime_capabilities
from pyAppGen.pbc import notifications_runtime_smoke
from pyAppGen.pbc import notifications_send_message
from pyAppGen.pbc import notifications_set_parameter
from pyAppGen.pbc import notifications_ui_contract
from pyAppGen.pbc import notifications_verify_owned_table_boundary
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.notifications import NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.notifications import NOTIFICATIONS_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.notifications import NOTIFICATIONS_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.notifications import NOTIFICATIONS_OWNED_TABLES
from pyAppGen.pbcs.notifications import NOTIFICATIONS_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.notifications import NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.notifications import NOTIFICATIONS_RUNTIME_TABLES
from pyAppGen.pbcs.notifications import implementation_contract
from pyAppGen.pbcs.notifications import notifications_build_release_evidence
from pyAppGen.pbcs.notifications import notifications_build_schema_contract
from pyAppGen.pbcs.notifications import notifications_build_service_contract
from pyAppGen.pbcs.notifications import notifications_register_schema_extension


def test_notifications_runtime_and_package_contract_are_complete() -> None:
    runtime = notifications_runtime_capabilities()
    smoke = notifications_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.notifications-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/notifications"
    assert runtime["owned_tables"] == NOTIFICATIONS_OWNED_TABLES
    assert runtime["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES
    assert runtime["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    assert runtime["consumes"] == NOTIFICATIONS_CONSUMED_EVENT_TYPES
    assert runtime["emits"] == NOTIFICATIONS_EMITTED_EVENT_TYPES
    assert len(runtime["standard_features"]) >= 30
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    assert contract["pbc"] == "notifications"
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    assert contract["consumes"] == NOTIFICATIONS_CONSUMED_EVENT_TYPES
    assert contract["emits"] == NOTIFICATIONS_EMITTED_EVENT_TYPES
    assert contract["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES
    assert pbc_implementation_release_audit(("notifications",))["ok"] is True


def test_notifications_schema_service_api_ui_and_release_contracts_are_hardened() -> None:
    api = notifications_build_api_contract()
    schema = notifications_build_schema_contract()
    service = notifications_build_service_contract()
    release = notifications_build_release_evidence()
    permissions = notifications_permissions_contract()
    ui_contract = notifications_ui_contract()

    assert api["ok"] is True
    assert api["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    assert api["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert api["dependency_surface"]["shared_tables"] == ()
    assert {route["route"] for route in api["routes"]} >= {
        "POST /notifications/configuration",
        "POST /notifications/rules",
        "POST /notifications/parameters",
        "GET /notifications/contracts/schema",
        "GET /notifications/contracts/service",
        "GET /notifications/release-evidence",
    }

    assert schema["ok"] is True
    assert schema["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    assert schema["event_contract"] == "AppGen-X"
    assert schema["shared_table_access"] is False
    assert len(schema["tables"]) == len(NOTIFICATIONS_OWNED_TABLES)
    assert len(schema["tables"]) >= 20
    assert len(schema["migrations"]) == len(NOTIFICATIONS_OWNED_TABLES)
    assert len(schema["models"]) == len(NOTIFICATIONS_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == NOTIFICATIONS_RUNTIME_TABLES
    assert {
        item["table"]
        for item in schema["tables"]
    } >= {
        "notification_recipient",
        "consent_ledger",
        "delivery_schedule",
        "throttle_window",
        "provider_route",
        "delivery_receipt",
        "bounce_event",
        "notification_campaign",
        "transactional_notification",
        "deliverability_analytics",
    }

    assert service["ok"] is True
    assert service["transaction_boundary"] == "notifications_owned_datastore_plus_appgen_outbox"
    assert "send_message" in service["command_methods"]
    assert "record_delivery_receipt" in service["command_methods"]
    assert "build_schema_contract" in service["query_methods"]
    assert "build_release_evidence" in service["query_methods"]
    assert "receive_event" in service["idempotent_handlers"]
    assert service["retry_dead_letter_evidence"]["outbox_table"] == NOTIFICATIONS_RUNTIME_TABLES[0]
    assert service["external_dependencies"]["shared_tables"] == ()
    assert service["shared_table_access"] is False

    assert permissions["action_permissions"]["build_schema_contract"] == "notifications.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "notifications.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "notifications.audit"
    assert permissions["action_permissions"]["record_delivery_receipt"] == "notifications.analytics.read"

    assert ui_contract["configuration_editor"]["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["event_surfaces"]["emits"] == NOTIFICATIONS_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == NOTIFICATIONS_CONSUMED_EVENT_TYPES
    assert ui_contract["workbench_binding_evidence"]["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES
    assert "DeliverabilityAnalyticsBoard" in ui_contract["fragments"]
    assert "CampaignPlanner" in ui_contract["fragments"]

    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert {
        check["id"]
        for check in release["checks"]
    } >= {
        "owned_schema_depth",
        "migration_per_owned_table",
        "runtime_tables_declared",
        "service_contract_depth",
        "api_event_contract",
        "permissions_cover_release_queries",
        "ui_binding_evidence",
        "workbench_binding_evidence",
        "boundary_contract",
        "database_allowlist",
    }
    assert release["api"]["required_event_topic"] == NOTIFICATIONS_REQUIRED_EVENT_TOPIC
    assert release["ui"]["workbench_binding_evidence"]["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES


def test_notifications_runtime_executes_configuration_rules_events_delivery_and_ui() -> None:
    state = _configured_state()
    extension = notifications_register_schema_extension(
        state,
        "message_delivery",
        {"provider_receipt": "jsonb", "routing_trace": "jsonb"},
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1

    state = notifications_register_channel(
        state,
        {
            "channel_id": "channel_email",
            "tenant": "tenant_ops",
            "channel_type": "email",
            "provider": "email_primary",
            "health_score": 0.96,
            "cost_score": 0.2,
            "status": "active",
        },
    )["state"]
    state = notifications_register_channel(
        state,
        {
            "channel_id": "channel_push",
            "tenant": "tenant_ops",
            "channel_type": "push",
            "provider": "push_primary",
            "health_score": 0.93,
            "cost_score": 0.1,
            "status": "active",
        },
    )["state"]
    state = notifications_register_template(
        state,
        {
            "template_id": "tmpl_ops",
            "tenant": "tenant_ops",
            "message_type": "service",
            "locale": "en-US",
            "subject": "Case {{ticket_id}} update",
            "body": "Hello {{customer_id}}, case {{ticket_id}} changed.",
            "required_variables": ("customer_id", "ticket_id"),
            "status": "active",
        },
    )["state"]
    state = notifications_receive_event(
        state,
        {
            "event_id": "pref_ops",
            "event_type": "PreferenceChanged",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "opt_in": True,
                "preferred_channels": ("email", "push"),
                "locale": "en-US",
            },
        },
    )["state"]
    state = notifications_receive_event(
        state,
        {
            "event_id": "campaign_ops",
            "event_type": "CampaignScheduled",
            "payload": {
                "tenant": "tenant_ops",
                "campaign_id": "cmp_ops",
                "name": "May Ops Campaign",
                "message_type": "marketing",
                "scheduled_for": "2026-05-26T08:00:00Z",
                "locale": "en-US",
            },
        },
    )["state"]
    state = notifications_receive_event(
        state,
        {
            "event_id": "sla_ops",
            "event_type": "SlaBreached",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "ticket_id": "case_ops",
                "urgency": 0.9,
            },
        },
    )["state"]
    sent = notifications_send_message(
        state,
        {
            "delivery_id": "msg_ops",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "template_id": "tmpl_ops",
            "message_type": "service",
            "context": {"customer_id": "cust_ops", "ticket_id": "case_ops"},
            "urgency": 0.9,
        },
    )
    state = sent["state"]
    assert sent["delivery"]["subject"] == "Case case_ops update"
    assert sent["delivery"]["route_id"].startswith("route_")
    assert sent["delivery"]["schedule_id"].startswith("schedule_")

    state = notifications_record_delivery_attempt(
        state,
        "msg_ops",
        provider_status="delivered",
    )["state"]
    event_types = {event["event_type"] for event in state["outbox"]}
    assert {
        "MessageQueued",
        "TransactionalNotificationDispatched",
        "MessageDelivered",
        "DeliveryReceiptRecorded",
    } <= event_types
    assert state["delivery_receipts"]["receipt_msg_ops"]["status"] == "recorded"
    assert state["deliverability_analytics"]["tenant_ops"]["delivery_success_rate"] == 1.0

    workbench = notifications_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["template_count"] == 1
    assert workbench["channel_count"] == 2
    assert workbench["delivery_count"] == 1
    assert workbench["delivered_count"] == 1
    assert workbench["preference_count"] == 1
    assert workbench["recipient_count"] == 1
    assert workbench["campaign_count"] == 1
    assert workbench["transactional_count"] == 1
    assert workbench["receipt_count"] == 1
    assert workbench["analytics_bound"] is True
    assert workbench["binding_evidence"]["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES

    rendered = notifications_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "notifications.template.write",
            "notifications.channel.write",
            "notifications.message.send",
            "notifications.campaign.write",
            "notifications.analytics.read",
            "notifications.event.consume",
            "notifications.configure",
            "notifications.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["runtime_tables"] == NOTIFICATIONS_RUNTIME_TABLES
    assert rendered["event_inbox_count"] == 3
    assert rendered["event_outbox_count"] >= 4


def test_notifications_reject_invalid_inputs_and_prove_boundary_bounce_and_dead_letter_evidence() -> None:
    state = notifications_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        notifications_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_locale": "en-US",
                "supported_locales": ("en-US",),
                "supported_channels": ("email",),
                "default_timezone": "UTC",
                "delivery_mode": "policy",
                "quiet_hours": ("22:00-06:00",),
                "workbench_limit": 50,
            },
        )
    with pytest.raises(ValueError, match="AppGen-X notifications event contract"):
        notifications_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.notifications.legacy",
                "retry_limit": 3,
                "default_locale": "en-US",
                "supported_locales": ("en-US",),
                "supported_channels": ("email",),
                "default_timezone": "UTC",
                "delivery_mode": "policy",
                "quiet_hours": ("22:00-06:00",),
                "workbench_limit": 50,
            },
        )
    with pytest.raises(ValueError, match="stream-engine pickers"):
        notifications_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_locale": "en-US",
                "supported_locales": ("en-US",),
                "supported_channels": ("email",),
                "default_timezone": "UTC",
                "delivery_mode": "policy",
                "quiet_hours": ("22:00-06:00",),
                "workbench_limit": 50,
                "stream_engine": "legacy_stream",
            },
        )

    state = _delivery_ready_state()
    with pytest.raises(ValueError, match="Unsupported Notifications parameter"):
        notifications_set_parameter(state, "stream_engine", 1)

    failed = notifications_receive_event(
        state,
        {
            "event_id": "evt_fail",
            "event_type": "PreferenceChanged",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_fail"},
        },
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert failed["state"]["retry_evidence"]["evt_fail"]["next_action"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    state = notifications_send_message(
        state,
        {
            "delivery_id": "msg_bounce",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "template_id": "tmpl_ops",
            "message_type": "service",
            "context": {"customer_id": "cust_ops", "ticket_id": "case_ops"},
            "urgency": 0.8,
        },
    )["state"]
    for _ in range(3):
        state = notifications_record_delivery_attempt(
            state,
            "msg_bounce",
            provider_status="bounced",
        )["state"]
    assert state["bounce_events"]["bounce_msg_bounce"]["status"] == "recorded"
    assert state["retry_evidence"]["msg_bounce"]["next_action"] == "dead_letter"
    assert any(item["event_id"] == "msg_bounce" for item in state["dead_letter"])

    boundary = notifications_verify_owned_table_boundary(
        (
            "notification_template",
            "notification_recipient",
            "preference_snapshot",
            "workflow_projection",
            NOTIFICATIONS_RUNTIME_TABLES[0],
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violated = notifications_verify_owned_table_boundary(("customer_profile",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer_profile",)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        notifications_register_schema_extension(state, "customer_profile", {"email": "text"})


def _configured_state() -> dict:
    state = notifications_empty_state()
    state = notifications_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_locale": "en-US",
            "supported_locales": ("en-US",),
            "supported_channels": ("email", "sms", "push", "chat"),
            "default_timezone": "UTC",
            "delivery_mode": "policy",
            "quiet_hours": ("22:00-06:00",),
            "workbench_limit": 50,
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
        ("workbench_limit", 50),
        ("campaign_batch_size", 1000),
        ("schedule_horizon_hours", 72),
        ("bounce_retry_window_minutes", 180),
    ):
        state = notifications_set_parameter(state, name, value)["state"]
    state = notifications_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "notifications",
            "status": "active",
            "allowed_channels": ("email", "push"),
            "allowed_locales": ("en-US",),
            "allowed_message_types": ("service", "workflow", "transactional"),
            "consent_policy": {"require_opt_in": True, "honor_quiet_hours": True},
            "delivery_policy": {"failover_channels": ("email", "push"), "default_sender": "service"},
            "throttle_policy": {"daily_limit": 20, "burst_limit": 5},
            "routing_policy": {"prefer_opted_in_channels": True, "fallback_on_degradation": True},
            "schedule_policy": {"respect_quiet_hours": True, "default_horizon_hours": 72},
        },
    )["state"]
    return state


def _delivery_ready_state() -> dict:
    state = _configured_state()
    state = notifications_register_channel(
        state,
        {
            "channel_id": "channel_email",
            "tenant": "tenant_ops",
            "channel_type": "email",
            "provider": "email_primary",
            "health_score": 0.96,
            "cost_score": 0.2,
            "status": "active",
        },
    )["state"]
    state = notifications_register_template(
        state,
        {
            "template_id": "tmpl_ops",
            "tenant": "tenant_ops",
            "message_type": "service",
            "locale": "en-US",
            "subject": "Case {{ticket_id}} update",
            "body": "Hello {{customer_id}}, case {{ticket_id}} changed.",
            "required_variables": ("customer_id", "ticket_id"),
            "status": "active",
        },
    )["state"]
    return notifications_receive_event(
        state,
        {
            "event_id": "pref_ops",
            "event_type": "PreferenceChanged",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "opt_in": True,
                "preferred_channels": ("email",),
                "locale": "en-US",
            },
        },
    )["state"]
