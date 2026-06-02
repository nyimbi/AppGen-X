"""One-PBC application surface for notification operations."""

from __future__ import annotations

import hashlib


PBC_KEY = "notifications"
OWNED_TABLES = (
    "notifications_notification_template",
    "notifications_template_locale_variant",
    "notifications_delivery_channel",
    "notifications_notification_recipient",
    "notifications_preference_snapshot",
    "notifications_consent_ledger",
    "notifications_delivery_schedule",
    "notifications_throttle_window",
    "notifications_provider_route",
    "notifications_message_delivery",
    "notifications_delivery_attempt",
    "notifications_retry_evidence",
    "notifications_delivery_receipt",
    "notifications_bounce_event",
    "notifications_notification_campaign",
    "notifications_campaign_dispatch",
    "notifications_transactional_notification",
    "notifications_notification_audit_log",
    "notifications_deliverability_analytics",
    "notifications_notification_rule",
    "notifications_notification_parameter",
    "notifications_notification_configuration",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def notifications_forms_contract() -> dict:
    """Return database-backed forms for a one-PBC notification operations app."""
    forms = (
        {"form_id": "template_authoring_form", "writes_table": "notifications_notification_template", "command": "register_template", "fields": ("tenant", "template_id", "message_type", "locale", "subject", "body", "status"), "validations": ("message_type_required", "locale_supported", "render_variables_declared", "approval_required_before_active")},
        {"form_id": "localized_variant_form", "writes_table": "notifications_template_locale_variant", "command": "register_template", "fields": ("tenant", "variant_id", "template_id", "locale", "subject", "body", "status"), "validations": ("parent_template_exists", "locale_supported", "translation_review_complete")},
        {"form_id": "channel_provider_form", "writes_table": "notifications_delivery_channel", "command": "register_channel", "fields": ("tenant", "channel_id", "channel_type", "provider", "health_score", "cost_score", "status"), "validations": ("channel_type_supported", "provider_credentials_bound", "health_score_in_range")},
        {"form_id": "recipient_preference_form", "writes_table": "notifications_notification_recipient", "command": "receive_event", "fields": ("tenant", "recipient_id", "customer_id", "locale", "preferred_channels", "opt_in", "status"), "validations": ("customer_projection_bound", "preferred_channel_registered", "consent_status_required")},
        {"form_id": "consent_capture_form", "writes_table": "notifications_consent_ledger", "command": "receive_event", "fields": ("tenant", "consent_id", "customer_id", "source_event_type", "opt_in", "proof_hash", "status"), "validations": ("proof_hash_required", "source_event_recorded", "immutable_consent_history")},
        {"form_id": "message_composition_form", "writes_table": "notifications_message_delivery", "command": "send_message", "fields": ("tenant", "delivery_id", "customer_id", "template_id", "channel_id", "delivery_risk", "status"), "validations": ("template_active", "recipient_opted_in", "quiet_hours_checked", "fatigue_risk_checked")},
        {"form_id": "campaign_planning_form", "writes_table": "notifications_notification_campaign", "command": "create_campaign", "fields": ("tenant", "campaign_id", "name", "message_type", "scheduled_for", "locale", "status"), "validations": ("audience_projection_required", "schedule_in_future", "throttle_budget_available")},
        {"form_id": "delivery_schedule_form", "writes_table": "notifications_delivery_schedule", "command": "schedule_notification", "fields": ("tenant", "schedule_id", "delivery_id", "campaign_id", "scheduled_for", "quiet_hours_enforced", "status"), "validations": ("delivery_exists", "quiet_hours_enforced", "schedule_horizon_respected")},
        {"form_id": "transactional_notification_form", "writes_table": "notifications_transactional_notification", "command": "create_transactional_notification", "fields": ("tenant", "transactional_id", "customer_id", "template_id", "delivery_id", "message_type", "status"), "validations": ("transactional_request_bound", "template_type_matches", "idempotency_key_required")},
        {"form_id": "receipt_and_bounce_form", "writes_table": "notifications_delivery_receipt", "command": "record_delivery_receipt", "fields": ("tenant", "receipt_id", "delivery_id", "provider_status", "proof_hash", "status"), "validations": ("delivery_exists", "provider_status_normalized", "proof_hash_required")},
        {"form_id": "bounce_triage_form", "writes_table": "notifications_bounce_event", "command": "record_bounce", "fields": ("tenant", "bounce_id", "delivery_id", "provider_status", "bounce_type", "status", "reason"), "validations": ("delivery_exists", "bounce_type_classified", "suppression_policy_evaluated")},
        {"form_id": "notification_governance_form", "writes_table": "notifications_notification_rule", "command": "register_rule", "fields": ("tenant", "rule_id", "scope", "allowed_channels", "allowed_locales", "consent_policy", "delivery_policy", "throttle_policy", "routing_policy", "status"), "validations": ("rule_compiles_to_hash", "impact_simulation_required", "rollback_plan_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def notifications_wizards_contract() -> dict:
    """Return guided notification workflows for operators, marketers, and support teams."""
    wizards = (
        {"wizard_id": "template_launch_wizard", "steps": ("author_template", "declare_variables", "add_localized_variants", "preview_channels", "approve_template"), "completion_event": "NotificationTemplateApproved"},
        {"wizard_id": "recipient_consent_wizard", "steps": ("import_preference_event", "verify_consent_proof", "select_locale", "apply_suppression_policy", "activate_recipient"), "completion_event": "ConsentUpdated"},
        {"wizard_id": "campaign_dispatch_wizard", "steps": ("select_audience", "choose_template", "simulate_fatigue", "schedule_batches", "monitor_dispatch"), "completion_event": "CampaignDispatched"},
        {"wizard_id": "transactional_send_wizard", "steps": ("bind_request_event", "choose_template", "resolve_channel", "create_delivery", "publish_outbox_event"), "completion_event": "TransactionalNotificationDispatched"},
        {"wizard_id": "provider_failover_wizard", "steps": ("detect_provider_degradation", "score_alternative_channels", "adjust_throttle_window", "route_delivery", "record_audit_event"), "completion_event": "ProviderRouteAdjusted"},
        {"wizard_id": "bounce_recovery_wizard", "steps": ("classify_bounce", "update_suppression_state", "decide_retry", "record_dead_letter_if_needed", "report_deliverability_impact"), "completion_event": "BounceRecorded"},
        {"wizard_id": "notification_policy_change_wizard", "steps": ("draft_rule_or_parameter", "simulate_delivery_impact", "approve_change", "activate_configuration", "monitor_control_tests"), "completion_event": "NotificationPolicyChanged"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def notifications_controls_contract() -> dict:
    """Return notification controls for consent, deliverability, compliance, and resilience."""
    controls = (
        {"control_id": "template_approval_and_variable_gate", "blocks_on_failure": True, "table_scope": ("notifications_notification_template", "notifications_template_locale_variant")},
        {"control_id": "recipient_consent_and_suppression_gate", "blocks_on_failure": True, "table_scope": ("notifications_notification_recipient", "notifications_consent_ledger", "notifications_preference_snapshot")},
        {"control_id": "quiet_hours_and_timezone_gate", "blocks_on_failure": True, "table_scope": ("notifications_delivery_schedule", "notifications_notification_configuration")},
        {"control_id": "fatigue_and_frequency_cap_gate", "blocks_on_failure": True, "table_scope": ("notifications_throttle_window", "notifications_message_delivery")},
        {"control_id": "provider_health_and_failover_gate", "blocks_on_failure": True, "table_scope": ("notifications_delivery_channel", "notifications_provider_route")},
        {"control_id": "campaign_batch_budget_gate", "blocks_on_failure": True, "table_scope": ("notifications_notification_campaign", "notifications_campaign_dispatch", "notifications_throttle_window")},
        {"control_id": "transactional_idempotency_gate", "blocks_on_failure": True, "table_scope": ("notifications_transactional_notification", "notifications_message_delivery")},
        {"control_id": "receipt_bounce_and_suppression_gate", "blocks_on_failure": True, "table_scope": ("notifications_delivery_receipt", "notifications_bounce_event", "notifications_consent_ledger")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("notifications_appgen_outbox_event", "notifications_appgen_inbox_event", "notifications_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_notifications_app_contract() -> dict:
    """Return evidence that this PBC can stand alone as a notification operations app."""
    forms = notifications_forms_contract()["forms"]
    wizards = notifications_wizards_contract()["wizards"]
    controls = notifications_controls_contract()["controls"]
    return {
        "ok": bool(forms) and bool(wizards) and bool(controls),
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "workbench": "NotificationsWorkbench",
        "assistant_panel": "NotificationsAgent",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_notifications_plan(document: str, instructions: str) -> dict:
    """Map notification documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "template" in text or "copy" in text or "locale" in text or "translation" in text:
        operation, table = "register_template", "notifications_notification_template"
    elif "channel" in text or "provider" in text or "failover" in text:
        operation, table = "register_channel", "notifications_delivery_channel"
    elif "consent" in text or "preference" in text or "opt" in text or "suppression" in text:
        operation, table = "receive_event", "notifications_consent_ledger"
    elif "campaign" in text or "audience" in text or "batch" in text:
        operation, table = "create_campaign", "notifications_notification_campaign"
    elif "schedule" in text or "quiet" in text or "timezone" in text:
        operation, table = "schedule_notification", "notifications_delivery_schedule"
    elif "transactional" in text or "receipt" in text or "otp" in text or "password" in text:
        operation, table = "create_transactional_notification", "notifications_transactional_notification"
    elif "bounce" in text or "undeliver" in text or "suppress" in text:
        operation, table = "record_bounce", "notifications_bounce_event"
    elif "delivery receipt" in text or "delivered" in text:
        operation, table = "record_delivery_receipt", "notifications_delivery_receipt"
    elif "rule" in text or "parameter" in text or "policy" in text or "configuration" in text:
        operation, table = "register_rule", "notifications_notification_rule"
    else:
        operation, table = "send_message", "notifications_message_delivery"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document, instructions),
        "proposed_operation": operation,
        "target_table": table,
        "requires_human_confirmation": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def app_surface_smoke_test() -> dict:
    """Exercise standalone notification app contracts."""
    app = single_pbc_notifications_app_contract()
    consent_plan = document_instruction_notifications_plan("customer consent update", "apply opt out")
    campaign_plan = document_instruction_notifications_plan("launch promotion campaign", "schedule batches")
    checks = (
        app["ok"],
        len(app["forms"]) >= 12,
        len(app["wizards"]) >= 7,
        len(app["controls"]) >= 10,
        consent_plan["target_table"] == "notifications_consent_ledger",
        campaign_plan["target_table"] == "notifications_notification_campaign",
        all(table.startswith("notifications_") for control in app["controls"] for table in control["table_scope"]),
    )
    return {
        "ok": all(checks),
        "single_pbc_app": app,
        "document_plans": (consent_plan, campaign_plan),
        "side_effects": (),
    }
