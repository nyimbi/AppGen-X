"""One-PBC application surface for service ticketing operations."""

from __future__ import annotations

import hashlib

PBC_KEY = "service_ticketing"
OWNED_TABLES = (
    "service_ticketing_support_ticket",
    "service_ticketing_service_queue",
    "service_ticketing_sla_policy",
    "service_ticketing_service_priority",
    "service_ticketing_case_assignment",
    "service_ticketing_escalation_event",
    "service_ticketing_ticket_interaction",
    "service_ticketing_knowledge_suggestion",
    "service_ticketing_entitlement_snapshot",
    "service_ticketing_case_lifecycle_state",
    "service_ticketing_field_service_handoff",
    "service_ticketing_customer_update",
    "service_ticketing_resolution_record",
    "service_ticketing_csat_response",
    "service_ticketing_ticket_audit_log",
    "service_ticketing_automation_insight",
    "service_ticketing_service_rule",
    "service_ticketing_service_parameter",
    "service_ticketing_service_configuration",
)


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def service_ticketing_forms_contract() -> dict:
    """Return database-backed forms for a one-PBC service desk app."""
    forms = (
        {"form_id": "ticket_intake_form", "writes_table": "service_ticketing_support_ticket", "command": "open_ticket", "fields": ("tenant", "ticket_id", "customer_id", "subject", "description", "channel", "priority", "region", "queue"), "validations": ("subject_required", "customer_required", "channel_supported", "priority_evidence_required")},
        {"form_id": "queue_configuration_form", "writes_table": "service_ticketing_service_queue", "command": "configure_runtime", "fields": ("tenant", "queue_id", "name", "assignment_mode", "service_tier", "default_owner", "workbench_limit"), "validations": ("queue_id_required", "assignment_mode_supported", "owner_required")},
        {"form_id": "sla_policy_form", "writes_table": "service_ticketing_sla_policy", "command": "create_sla_policy", "fields": ("tenant", "sla_policy_id", "name", "priority", "first_response_minutes", "resolution_target_hours", "status"), "validations": ("priority_supported", "response_less_than_resolution", "active_policy_version_required")},
        {"form_id": "priority_matrix_form", "writes_table": "service_ticketing_service_priority", "command": "register_rule", "fields": ("tenant", "priority_id", "display_order", "severity_score", "default_response_minutes", "default_resolution_hours", "status"), "validations": ("severity_evidence_required", "customer_pressure_not_severity", "display_order_unique")},
        {"form_id": "case_assignment_form", "writes_table": "service_ticketing_case_assignment", "command": "assign_ticket", "fields": ("tenant", "assignment_id", "ticket_id", "owner", "queue", "skills", "assignment_score", "status"), "validations": ("ticket_exists", "owner_has_skills", "queue_capacity_checked", "fairness_evidence_required")},
        {"form_id": "ticket_interaction_form", "writes_table": "service_ticketing_ticket_interaction", "command": "record_ticket_interaction", "fields": ("tenant", "interaction_id", "ticket_id", "interaction_type", "channel", "actor", "summary", "redaction_status"), "validations": ("ticket_exists", "actor_required", "redaction_required_for_sensitive_data")},
        {"form_id": "customer_update_form", "writes_table": "service_ticketing_customer_update", "command": "send_customer_update", "fields": ("tenant", "update_id", "ticket_id", "customer_id", "update_type", "delivery_channel", "message", "approval_status"), "validations": ("entitlement_checked", "approval_required_before_send", "promised_update_tracked")},
        {"form_id": "field_service_handoff_form", "writes_table": "service_ticketing_field_service_handoff", "command": "prepare_field_service_handoff", "fields": ("tenant", "handoff_id", "ticket_id", "assignment_id", "handoff_reason", "target_team", "site_requirements", "status"), "validations": ("assignment_exists", "site_requirements_required", "handoff_status_tracked")},
        {"form_id": "escalation_form", "writes_table": "service_ticketing_escalation_event", "command": "record_escalation", "fields": ("tenant", "escalation_id", "ticket_id", "reason", "breach_risk", "queue", "status"), "validations": ("reason_required", "breach_risk_scored", "queue_owner_notified")},
        {"form_id": "resolution_and_csat_form", "writes_table": "service_ticketing_resolution_record", "command": "resolve_ticket", "fields": ("tenant", "resolution_id", "ticket_id", "resolution", "resolved_by", "resolution_code", "send_csat"), "validations": ("resolution_code_required", "customer_update_completed", "csat_created_when_required")},
        {"form_id": "service_governance_form", "writes_table": "service_ticketing_service_rule", "command": "register_rule", "fields": ("tenant", "rule_id", "scope", "allowed_regions", "allowed_channels", "allowed_priorities", "assignment_policy", "escalation_policy", "status"), "validations": ("rule_compiles_to_hash", "impact_simulation_required", "rollback_plan_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def service_ticketing_wizards_contract() -> dict:
    """Return guided support workflows for agents and supervisors."""
    wizards = (
        {"wizard_id": "case_intake_triage_wizard", "steps": ("capture_ticket", "classify_priority", "match_entitlement", "assign_queue", "start_sla_clock"), "completion_event": "TicketOpened"},
        {"wizard_id": "sla_escalation_wizard", "steps": ("detect_breach_risk", "explain_sla_clock", "notify_owner", "record_escalation", "track_recovery"), "completion_event": "TicketEscalated"},
        {"wizard_id": "customer_update_wizard", "steps": ("draft_response", "cite_ticket_context", "redact_sensitive_data", "approve_message", "publish_update"), "completion_event": "CustomerUpdateSent"},
        {"wizard_id": "field_service_handoff_wizard", "steps": ("verify_remote_resolution_blocker", "collect_site_requirements", "select_target_team", "prepare_handoff", "monitor_acceptance"), "completion_event": "FieldServiceHandoffPrepared"},
        {"wizard_id": "resolution_closure_wizard", "steps": ("validate_resolution_evidence", "send_final_update", "close_ticket", "send_csat", "capture_reopen_conditions"), "completion_event": "TicketResolved"},
        {"wizard_id": "service_policy_change_wizard", "steps": ("draft_rule_or_parameter", "simulate_queue_sla_impact", "approve_change", "activate_policy", "monitor_anomalies"), "completion_event": "ServicePolicyChanged"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def service_ticketing_controls_contract() -> dict:
    """Return support controls for quality, SLA, customer safety, and release readiness."""
    controls = (
        {"control_id": "ticket_intake_completeness_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_support_ticket", "service_ticketing_case_lifecycle_state")},
        {"control_id": "severity_priority_evidence_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_support_ticket", "service_ticketing_service_priority")},
        {"control_id": "sla_clock_and_escalation_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_sla_policy", "service_ticketing_escalation_event")},
        {"control_id": "assignment_skill_fairness_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_case_assignment", "service_ticketing_service_queue")},
        {"control_id": "customer_update_approval_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_customer_update", "service_ticketing_ticket_interaction")},
        {"control_id": "field_service_handoff_readiness_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_field_service_handoff", "service_ticketing_case_assignment")},
        {"control_id": "resolution_csat_closure_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_resolution_record", "service_ticketing_csat_response")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("service_ticketing_appgen_outbox_event", "service_ticketing_appgen_inbox_event", "service_ticketing_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_service_ticketing_app_contract() -> dict:
    """Return evidence that this PBC can stand alone as a service desk app."""
    forms = service_ticketing_forms_contract()["forms"]
    wizards = service_ticketing_wizards_contract()["wizards"]
    controls = service_ticketing_controls_contract()["controls"]
    return {"ok": bool(forms) and bool(wizards) and bool(controls), "pbc": PBC_KEY, "single_pbc_app": True, "database_backed": True, "allowed_database_backends": ("postgresql", "mysql", "mariadb"), "owned_tables": OWNED_TABLES, "forms": forms, "wizards": wizards, "controls": controls, "workbench": "ServiceTicketingWorkbench", "assistant_panel": "ServiceTicketingAgent", "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "side_effects": ()}


def document_instruction_service_ticketing_plan(document: str, instructions: str) -> dict:
    """Map service documents and instructions to governed CRUD previews."""
    text = f"{document} {instructions}".lower()
    if "sla" in text or "breach" in text:
        operation, table = "create_sla_policy", "service_ticketing_sla_policy"
    elif "assign" in text or "skill" in text or "queue" in text:
        operation, table = "assign_ticket", "service_ticketing_case_assignment"
    elif "field" in text or "handoff" in text or "site" in text:
        operation, table = "prepare_field_service_handoff", "service_ticketing_field_service_handoff"
    elif "update" in text or "reply" in text or "email" in text:
        operation, table = "send_customer_update", "service_ticketing_customer_update"
    elif "escalat" in text:
        operation, table = "record_escalation", "service_ticketing_escalation_event"
    elif "resolve" in text or "close" in text or "csat" in text:
        operation, table = "resolve_ticket", "service_ticketing_resolution_record"
    elif "interaction" in text or "call" in text or "note" in text:
        operation, table = "record_ticket_interaction", "service_ticketing_ticket_interaction"
    elif "rule" in text or "parameter" in text or "policy" in text:
        operation, table = "register_rule", "service_ticketing_service_rule"
    else:
        operation, table = "open_ticket", "service_ticketing_support_ticket"
    return {"ok": True, "pbc": PBC_KEY, "document_digest": _digest(document, instructions), "proposed_operation": operation, "target_table": table, "requires_human_confirmation": True, "crud_datastore_mutation": True, "event_contract": "AppGen-X", "side_effects": ()}


def app_surface_smoke_test() -> dict:
    """Exercise standalone service-ticketing app contracts."""
    app = single_pbc_service_ticketing_app_contract()
    handoff_plan = document_instruction_service_ticketing_plan("site visit required", "prepare field handoff")
    update_plan = document_instruction_service_ticketing_plan("customer email", "draft approved update")
    checks = (app["ok"], len(app["forms"]) >= 10, len(app["wizards"]) >= 6, len(app["controls"]) >= 9, handoff_plan["target_table"] == "service_ticketing_field_service_handoff", update_plan["target_table"] == "service_ticketing_customer_update", all(table.startswith("service_ticketing_") for control in app["controls"] for table in control["table_scope"]))
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (handoff_plan, update_plan), "side_effects": ()}
