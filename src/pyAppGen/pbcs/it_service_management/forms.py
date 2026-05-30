"""Domain forms for the it_service_management PBC."""
from __future__ import annotations

PBC_KEY = "it_service_management"

FORM_CATALOG = (
    {
        "key": "major_incident_form",
        "title": "Major incident declaration",
        "target_table": "it_service_management_it_incident",
        "fields": (
            "incident_id", "affected_business_services", "impact", "urgency", "severity",
            "commander", "bridge_url", "customer_communication_cadence", "exit_criteria",
        ),
        "validations": ("severity_matrix_applied", "commander_assigned", "exit_criteria_present"),
        "permission": "it_service_management.approve",
    },
    {
        "key": "service_request_catalog_form",
        "title": "Catalog-backed service request",
        "target_table": "it_service_management_service_request",
        "fields": (
            "request_id", "catalog_item", "requester", "entitlement", "required_fields",
            "fulfillment_template", "approval_policy", "expected_lead_time_hours",
        ),
        "validations": ("catalog_item_active", "requester_entitled", "required_fields_complete"),
        "permission": "it_service_management.create",
    },
    {
        "key": "access_request_form",
        "title": "Access request entitlement review",
        "target_table": "it_service_management_service_request",
        "fields": (
            "request_id", "identity", "manager", "target_system", "access_level",
            "segregation_conflicts", "system_owner_approval", "expiry_date",
        ),
        "validations": ("manager_approval_present", "system_owner_approval_present", "sod_clear", "expiry_required"),
        "permission": "it_service_management.approve",
    },
    {
        "key": "change_request_form",
        "title": "Standard, normal, and emergency change",
        "target_table": "it_service_management_change_request",
        "fields": (
            "change_id", "change_class", "affected_configuration_items", "risk_score",
            "implementation_window", "validation_steps", "backout_triggers", "rollback_owner",
            "post_implementation_review_due",
        ),
        "validations": ("change_class_valid", "risk_scored", "window_allowed", "backout_plan_complete"),
        "permission": "it_service_management.approve",
    },
    {
        "key": "cab_decision_form",
        "title": "CAB agenda and decision capture",
        "target_table": "it_service_management_change_request",
        "fields": (
            "cab_id", "agenda_order", "attendees", "quorum_status", "risk_summary",
            "decision", "follow_ups", "resubmission_requirements",
        ),
        "validations": ("quorum_met", "decision_recorded", "follow_ups_owned"),
        "permission": "it_service_management.approve",
    },
    {
        "key": "problem_rca_form",
        "title": "Problem root-cause analysis",
        "target_table": "it_service_management_problem_record",
        "fields": (
            "problem_id", "linked_incidents", "linked_changes", "rca_template", "hypotheses",
            "validated_causes", "corrective_actions", "preventive_actions", "known_error_visibility",
        ),
        "validations": ("incident_links_consistent", "rca_method_complete", "actions_approved"),
        "permission": "it_service_management.update",
    },
    {
        "key": "configuration_item_form",
        "title": "Configuration item ownership and relationship graph",
        "target_table": "it_service_management_configuration_item",
        "fields": (
            "ci_id", "ci_type", "service_owner", "technical_owner", "support_group", "criticality",
            "relationships", "maintenance_calendar", "last_verified_at",
        ),
        "validations": ("owners_present", "support_group_present", "relationship_graph_valid", "verification_current"),
        "permission": "it_service_management.update",
    },
    {
        "key": "sla_clock_form",
        "title": "SLA, OLA, and underpinning commitment clock",
        "target_table": "it_service_management_sla_clock",
        "fields": (
            "clock_id", "record_id", "commitment_type", "acknowledgement_due", "restoration_due",
            "workaround_due", "resolution_due", "pause_reason", "business_calendar",
        ),
        "validations": ("commitment_type_valid", "milestones_present", "pause_reason_allowed", "calendar_applied"),
        "permission": "it_service_management.update",
    },
    {
        "key": "knowledge_article_form",
        "title": "Known error and workaround publication",
        "target_table": "it_service_management_knowledge_article",
        "fields": (
            "article_id", "problem_id", "workaround_steps", "customer_safe_summary",
            "internal_resolver_notes", "visibility", "approval_status", "expiry_review_date",
        ),
        "validations": ("visibility_separated", "workaround_approved", "review_date_present"),
        "permission": "it_service_management.approve",
    },
)


def form_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "forms": FORM_CATALOG, "side_effects": ()}


def smoke_test() -> dict:
    return {
        "ok": len(FORM_CATALOG) >= 9 and all(form["target_table"].startswith(f"{PBC_KEY}_") for form in FORM_CATALOG),
        "side_effects": (),
    }
