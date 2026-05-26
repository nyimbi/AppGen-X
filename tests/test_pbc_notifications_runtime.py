import pytest

from pyAppGen.pbc import notifications_build_workbench_view
from pyAppGen.pbc import notifications_configure_runtime
from pyAppGen.pbc import notifications_empty_state
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
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.notifications import NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.notifications import NOTIFICATIONS_OWNED_TABLES
from pyAppGen.pbcs.notifications import NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS


def test_notifications_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = notifications_runtime_capabilities()
    smoke = notifications_runtime_smoke()

    assert runtime["format"] == "appgen.notifications-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/notifications"
    assert runtime["owned_tables"] == NOTIFICATIONS_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(NOTIFICATIONS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("notifications")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "NotificationConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("notifications",))["ok"] is True


def test_notifications_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    state = notifications_register_channel(
        state,
        {"channel_id": "channel_email", "tenant": "tenant_ops", "channel_type": "email", "provider": "email_primary", "health_score": 0.96, "cost_score": 0.2, "status": "active"},
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
        {"event_id": "pref_ops", "event_type": "PreferenceChanged", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "opt_in": True, "preferred_channels": ("email",), "locale": "en-US"}},
    )["state"]
    state = notifications_receive_event(
        state,
        {"event_id": "sla_ops", "event_type": "SlaBreached", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "ticket_id": "case_ops", "urgency": 0.9}},
    )["state"]
    sent = notifications_send_message(
        state,
        {"delivery_id": "msg_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "template_id": "tmpl_ops", "message_type": "service", "context": {"customer_id": "cust_ops", "ticket_id": "case_ops"}, "urgency": 0.9},
    )
    state = sent["state"]
    assert sent["delivery"]["subject"] == "Case case_ops update"
    state = notifications_record_delivery_attempt(state, "msg_ops", provider_status="delivered")["state"]
    assert state["outbox"][-1]["idempotency_key"].startswith("notifications:MessageDelivered")

    workbench = notifications_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["template_count"] == 1
    assert workbench["channel_count"] == 1
    assert workbench["delivery_count"] == 1
    assert workbench["delivered_count"] == 1
    assert workbench["preference_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = notifications_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = notifications_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "notifications.template.write",
            "notifications.channel.write",
            "notifications.message.send",
            "notifications.event.consume",
            "notifications.configure",
            "notifications.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == NOTIFICATIONS_OWNED_TABLES


def test_notifications_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = notifications_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        notifications_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.notifications.events",
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

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Notifications parameter"):
        notifications_set_parameter(state, "stream_engine", 1)

    failed = notifications_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "PreferenceChanged", "payload": {"tenant": "tenant_ops", "customer_id": "cust_fail"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = notifications_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("notification_template", "delivery_channel", "message_delivery", "preference_snapshot")
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = notifications_empty_state()
    state = notifications_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.notifications.events",
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
            "allowed_message_types": ("service", "workflow"),
            "consent_policy": {"require_opt_in": True, "honor_quiet_hours": True},
            "delivery_policy": {"failover_channels": ("email", "push"), "default_sender": "service"},
        },
    )["state"]
    return state
