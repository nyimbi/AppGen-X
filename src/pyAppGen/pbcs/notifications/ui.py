"""UI contract for the Notifications PBC."""

from __future__ import annotations

from .runtime import NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import NOTIFICATIONS_CONSUMED_EVENT_TYPES
from .runtime import NOTIFICATIONS_EMITTED_EVENT_TYPES
from .runtime import NOTIFICATIONS_OWNED_TABLES
from .runtime import NOTIFICATIONS_REQUIRED_EVENT_TOPIC
from .runtime import NOTIFICATIONS_RUNTIME_TABLES
from .runtime import notifications_build_workbench_view
from .runtime import notifications_permissions_contract


NOTIFICATIONS_UI_FRAGMENT_KEYS = (
    "NotificationsWorkbench",
    "TemplateDesigner",
    "LocalizationStudio",
    "DeliveryChannelConsole",
    "RecipientDirectory",
    "PreferenceSnapshotPanel",
    "ConsentLedgerPanel",
    "ScheduleBoard",
    "ThrottlePolicyBoard",
    "ProviderRoutingConsole",
    "MessageComposer",
    "DeliveryStatusBoard",
    "DeliveryReceiptPanel",
    "BounceQueuePanel",
    "CampaignPlanner",
    "TransactionalNotificationConsole",
    "NotificationRuleStudio",
    "NotificationParameterConsole",
    "NotificationConfigurationPanel",
    "NotificationEventOutbox",
    "NotificationDeadLetterQueue",
    "NotificationAuditTrail",
    "DeliverabilityAnalyticsBoard",
)


def notifications_ui_contract() -> dict:
    permissions = notifications_permissions_contract()["action_permissions"]
    return {
        "format": "appgen.notifications-ui-contract.v1",
        "ok": True,
        "pbc": "notifications",
        "implementation_directory": "src/pyAppGen/pbcs/notifications",
        "fragments": NOTIFICATIONS_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/notifications",
            "/workbench/pbcs/notifications/templates",
            "/workbench/pbcs/notifications/localization",
            "/workbench/pbcs/notifications/channels",
            "/workbench/pbcs/notifications/recipients",
            "/workbench/pbcs/notifications/preferences",
            "/workbench/pbcs/notifications/schedules",
            "/workbench/pbcs/notifications/campaigns",
            "/workbench/pbcs/notifications/transactional",
            "/workbench/pbcs/notifications/analytics",
            "/workbench/pbcs/notifications/configuration",
        ),
        "panels": (
            {
                "key": "templates",
                "fragment": "TemplateDesigner",
                "binds_to": ("notification_template", "template_locale_variant"),
                "commands": ("register_template",),
            },
            {
                "key": "recipients",
                "fragment": "RecipientDirectory",
                "binds_to": ("notification_recipient", "preference_snapshot", "consent_ledger"),
                "commands": ("receive_event",),
            },
            {
                "key": "delivery",
                "fragment": "DeliveryStatusBoard",
                "binds_to": (
                    "message_delivery",
                    "delivery_attempt",
                    "delivery_receipt",
                    "bounce_event",
                    "retry_evidence",
                ),
                "commands": ("send_message", "record_delivery_attempt"),
            },
            {
                "key": "campaigns",
                "fragment": "CampaignPlanner",
                "binds_to": ("notification_campaign", "campaign_dispatch", "delivery_schedule"),
                "commands": ("create_campaign", "schedule_notification"),
            },
            {
                "key": "governance",
                "fragment": "NotificationRuleStudio",
                "binds_to": ("notification_rule", "notification_parameter", "notification_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
            {
                "key": "analytics",
                "fragment": "DeliverabilityAnalyticsBoard",
                "binds_to": ("deliverability_analytics", "notification_audit_log"),
                "commands": ("publish_deliverability_analytics", "build_release_evidence"),
            },
        ),
        "action_permissions": {
            **permissions,
            "run_control_tests": "notifications.audit",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_locale",
                "default_timezone",
                "delivery_mode",
            ),
            "allowed_database_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
                "campaign_batch_size",
                "schedule_horizon_hours",
                "bounce_retry_window_minutes",
            ),
        },
        "rule_editor": {
            "rule_types": (
                "consent",
                "delivery",
                "channel",
                "template",
                "fatigue",
                "campaign",
                "transactional",
                "release_gate",
            ),
            "required_fields": (
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
            ),
        },
        "event_surfaces": {
            "emits": NOTIFICATIONS_EMITTED_EVENT_TYPES,
            "consumes": NOTIFICATIONS_CONSUMED_EVENT_TYPES,
            "required_event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": NOTIFICATIONS_OWNED_TABLES,
            "runtime_tables": NOTIFICATIONS_RUNTIME_TABLES,
            "outbox_table": NOTIFICATIONS_RUNTIME_TABLES[0],
            "inbox_table": NOTIFICATIONS_RUNTIME_TABLES[1],
            "dead_letter_table": NOTIFICATIONS_RUNTIME_TABLES[2],
            "permissions": permissions,
            "configuration": {
                "event_contract": "AppGen-X",
                "event_topic": NOTIFICATIONS_REQUIRED_EVENT_TOPIC,
                "allowed_database_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
                "stream_engine_picker_visible": False,
            },
        },
    }


def notifications_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = notifications_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required in contract["action_permissions"].items()
        if required in permissions
    )
    view = notifications_build_workbench_view(state, tenant=tenant)
    cards = (
        {"key": "templates", "value": view["template_count"], "fragment": "TemplateDesigner"},
        {"key": "channels", "value": view["channel_count"], "fragment": "DeliveryChannelConsole"},
        {"key": "deliveries", "value": view["delivery_count"], "fragment": "DeliveryStatusBoard"},
        {"key": "receipts", "value": view["receipt_count"], "fragment": "DeliveryReceiptPanel"},
        {"key": "bounces", "value": view["bounce_count"], "fragment": "BounceQueuePanel"},
        {"key": "campaigns", "value": view["campaign_count"], "fragment": "CampaignPlanner"},
        {"key": "transactional", "value": view["transactional_count"], "fragment": "TransactionalNotificationConsole"},
        {"key": "analytics", "value": 1 if view["analytics_bound"] else 0, "fragment": "DeliverabilityAnalyticsBoard"},
    )
    return {
        "format": "appgen.notifications-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/notifications",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in contract["action_permissions"] if action not in visible_actions
        ),
        "configuration_bound": view["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": view["outbox_count"],
        "event_inbox_count": view["inbox_count"],
        "dead_letter_count": view["dead_letter_count"],
        "binding_evidence": contract["workbench_binding_evidence"],
    }
