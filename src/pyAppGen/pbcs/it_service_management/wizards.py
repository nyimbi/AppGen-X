"""Guided ITSM workflows for the it_service_management PBC."""
from __future__ import annotations

PBC_KEY = "it_service_management"

WIZARD_CATALOG = (
    {
        "key": "major_incident_command_wizard",
        "title": "Declare and run a major incident",
        "steps": (
            "classify_impact_urgency", "assign_commander_and_bridge", "roll_up_duplicate_incidents",
            "freeze_evidence_timeline", "publish_customer_updates", "confirm_exit_criteria",
        ),
        "owned_tables": ("it_service_management_it_incident", "it_service_management_sla_clock"),
        "emits": ("ItServiceManagementExceptionOpened", "ItServiceManagementUpdated"),
    },
    {
        "key": "catalog_request_fulfillment_wizard",
        "title": "Fulfill a catalog service request",
        "steps": (
            "validate_catalog_item", "check_entitlement", "fan_out_fulfillment_tasks",
            "collect_delivery_evidence", "requester_confirmation", "close_or_reopen",
        ),
        "owned_tables": ("it_service_management_service_request", "it_service_management_sla_clock"),
        "emits": ("ItServiceManagementCreated", "ItServiceManagementUpdated"),
    },
    {
        "key": "access_request_governance_wizard",
        "title": "Approve governed access",
        "steps": (
            "parse_access_instruction", "manager_approval", "system_owner_approval",
            "segregation_of_duties_check", "time_box_access", "schedule_recertification",
        ),
        "owned_tables": ("it_service_management_service_request",),
        "emits": ("ItServiceManagementApproved",),
    },
    {
        "key": "change_risk_and_cab_wizard",
        "title": "Assess, approve, and review a change",
        "steps": (
            "select_change_class", "score_blast_radius", "validate_maintenance_window",
            "prepare_cab_agenda", "record_cab_decision", "schedule_post_implementation_review",
        ),
        "owned_tables": ("it_service_management_change_request", "it_service_management_configuration_item"),
        "emits": ("ItServiceManagementApproved", "ItServiceManagementUpdated"),
    },
    {
        "key": "problem_rca_to_known_error_wizard",
        "title": "Turn recurring incidents into a known error",
        "steps": (
            "detect_recurrence", "link_incidents_and_changes", "choose_rca_template",
            "validate_root_cause", "approve_workaround", "publish_knowledge_article",
        ),
        "owned_tables": (
            "it_service_management_problem_record", "it_service_management_it_incident",
            "it_service_management_knowledge_article",
        ),
        "emits": ("ItServiceManagementCreated", "ItServiceManagementApproved"),
    },
    {
        "key": "cmdb_impact_preview_wizard",
        "title": "Model CI relationships and preview service impact",
        "steps": (
            "capture_ci_ownership", "validate_relationship_graph", "detect_stale_or_drifted_records",
            "traverse_dependency_paths", "notify_support_groups", "attach_impact_preview_to_change",
        ),
        "owned_tables": ("it_service_management_configuration_item", "it_service_management_change_request"),
        "emits": ("ItServiceManagementUpdated",),
    },
)


def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARD_CATALOG, "side_effects": ()}


def smoke_test() -> dict:
    return {
        "ok": len(WIZARD_CATALOG) >= 6 and all(wizard["owned_tables"] for wizard in WIZARD_CATALOG),
        "side_effects": (),
    }
