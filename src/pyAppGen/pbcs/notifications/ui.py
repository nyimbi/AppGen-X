"""UI contract for the Notifications PBC."""

from __future__ import annotations

from .runtime import NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import NOTIFICATIONS_OWNED_TABLES


NOTIFICATIONS_UI_FRAGMENT_KEYS = (
    "NotificationsWorkbench",
    "TemplateDesigner",
    "DeliveryChannelConsole",
    "MessageComposer",
    "PreferenceSnapshotPanel",
    "DeliveryStatusBoard",
    "ChannelRoutingBoard",
    "ConsentPolicyPanel",
    "NotificationRuleStudio",
    "NotificationParameterConsole",
    "NotificationConfigurationPanel",
    "NotificationEventOutbox",
    "NotificationDeadLetterQueue",
)


def notifications_ui_contract() -> dict:
    return {
        "format": "appgen.notifications-ui-contract.v1",
        "ok": True,
        "pbc": "notifications",
        "implementation_directory": "src/pyAppGen/pbcs/notifications",
        "fragments": NOTIFICATIONS_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/notifications",
            "/workbench/pbcs/notifications/templates",
            "/workbench/pbcs/notifications/channels",
            "/workbench/pbcs/notifications/messages",
            "/workbench/pbcs/notifications/preferences",
            "/workbench/pbcs/notifications/configuration",
        ),
        "panels": (
            {"key": "templates", "fragment": "TemplateDesigner", "binds_to": ("notification_template",), "commands": ("register_template", "send_message")},
            {"key": "channels", "fragment": "DeliveryChannelConsole", "binds_to": ("delivery_channel",), "commands": ("register_channel",)},
            {"key": "deliveries", "fragment": "DeliveryStatusBoard", "binds_to": ("message_delivery", "preference_snapshot"), "commands": ("record_delivery_attempt", "receive_event")},
            {"key": "governance", "fragment": "NotificationRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "register_template": "notifications.template.write",
            "register_channel": "notifications.channel.write",
            "send_message": "notifications.message.send",
            "record_delivery_attempt": "notifications.message.send",
            "receive_event": "notifications.event.consume",
            "register_rule": "notifications.configure",
            "set_parameter": "notifications.configure",
            "configure_runtime": "notifications.configure",
            "run_control_tests": "notifications.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_locale", "default_timezone", "delivery_mode"),
            "allowed_database_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
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
            ),
        },
        "rule_editor": {
            "rule_types": ("consent", "delivery", "channel", "template", "fatigue"),
            "required_fields": ("rule_id", "tenant", "scope", "status", "allowed_channels", "allowed_locales", "allowed_message_types", "consent_policy", "delivery_policy"),
        },
        "event_surfaces": {
            "emits": ("MessageDelivered", "MessageFailed"),
            "consumes": ("PreferenceChanged", "SlaBreached", "WorkflowCompleted"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def notifications_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = notifications_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "templates", "value": view["template_count"], "fragment": "TemplateDesigner"},
        {"key": "channels", "value": view["channel_count"], "fragment": "DeliveryChannelConsole"},
        {"key": "deliveries", "value": view["delivery_count"], "fragment": "DeliveryStatusBoard"},
        {"key": "delivered", "value": view["delivered_count"], "fragment": "DeliveryStatusBoard"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "NotificationEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "NotificationDeadLetterQueue"},
    )
    return {
        "format": "appgen.notifications-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/notifications",
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
    templates = tuple(item for item in state.get("notification_templates", {}).values() if item["tenant"] == tenant)
    channels = tuple(item for item in state.get("delivery_channels", {}).values() if item["tenant"] == tenant)
    deliveries = tuple(item for item in state.get("message_deliveries", {}).values() if item["tenant"] == tenant)
    return {
        "template_count": len(templates),
        "channel_count": len(channels),
        "delivery_count": len(deliveries),
        "delivered_count": len(tuple(item for item in deliveries if item["status"] == "delivered")),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": NOTIFICATIONS_OWNED_TABLES,
        },
    }
