"""UI/workbench contracts for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_EDGE_CASES,
    DOMAIN_OPERATIONS,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_capability_surface_contract,
)
from .runtime import (
    cybersecurity_operations_center_build_case_detail,
    cybersecurity_operations_center_build_workbench_view,
    cybersecurity_operations_center_empty_state,
)

PBC_KEY = "cybersecurity_operations_center"


def _forms() -> tuple[dict[str, Any], ...]:
    return (
        {
            "id": "alert_intake_form",
            "title": "Detection to Alert Intake",
            "fields": (
                "tenant",
                "severity",
                "confidence",
                "asset_ref",
                "principal_ref",
                "indicator_value",
                "detection_context.source_event_id",
                "detection_context.detection_timestamp",
                "detection_context.detection_rule_id",
                "detection_context.evidence_checksum",
            ),
            "supports_validation_only": True,
        },
        {
            "id": "incident_promotion_form",
            "title": "Incident Promotion",
            "fields": ("alert_ids", "asset_criticality", "containment_required", "commander", "communications_owner"),
            "supports_preview": True,
        },
        {
            "id": "evidence_request_form",
            "title": "Evidence Capture",
            "fields": ("case_id", "source_system", "storage_reference", "admissibility_notes"),
            "supports_chain_of_custody": True,
        },
        {
            "id": "containment_approval_form",
            "title": "Containment Approval",
            "fields": ("incident_id", "action_type", "risk_level", "approved_by", "rollback_instructions"),
            "supports_risk_gate": True,
        },
    )


def _wizards() -> tuple[dict[str, Any], ...]:
    return (
        {
            "id": "alert_triage_wizard",
            "steps": ("validate_detection", "enrich_context", "triage_state", "incident_preview", "next_action"),
            "persona": "analyst",
        },
        {
            "id": "incident_promotion_wizard",
            "steps": ("select_alert_cluster", "preview_score", "assign_owners", "create_incident"),
            "persona": "incident_commander",
        },
        {
            "id": "playbook_run_wizard",
            "steps": ("preconditions", "approval_breakpoints", "containment", "validation", "closure_verification"),
            "persona": "responder",
        },
        {
            "id": "shift_handoff_wizard",
            "steps": ("active_cases", "pending_approvals", "pending_evidence", "open_questions", "packet_export"),
            "persona": "supervisor",
        },
    )


def _controls() -> tuple[dict[str, Any], ...]:
    return (
        {"id": "severity_lane_filter", "type": "filter", "options": ("urgent", "backlog", "watchlist", "suppressed")},
        {"id": "confidence_slider", "type": "range", "minimum": 0.0, "maximum": 1.0},
        {"id": "event_lineage_panel", "type": "drawer", "shows": ("outbox", "inbox", "dead_letter")},
        {"id": "relationship_graph_toggle", "type": "toggle", "shows": "case_relationship_graph"},
    )


def cybersecurity_operations_center_ui_contract() -> dict[str, Any]:
    surface = domain_capability_surface_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "CybersecurityOperationsCenterWorkbench",
            "CybersecurityOperationsCenterDetail",
            "CybersecurityOperationsCenterAssistantPanel",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "cybersecurity_operations_center.read",
            "cybersecurity_operations_center.create",
            "cybersecurity_operations_center.update",
            "cybersecurity_operations_center.approve",
            "cybersecurity_operations_center.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "triage_lanes",
                "supervisor_board",
                "evidence_review",
                "detail_graph",
                "assistant_plans",
                "release_evidence",
            ),
            "forms": _forms(),
            "wizards": _wizards(),
            "controls": _controls(),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def cybersecurity_operations_center_render_workbench(
    state: dict[str, Any] | None = None,
    tenant: str = "default",
) -> dict[str, Any]:
    active_state = state or cybersecurity_operations_center_empty_state()
    workbench = cybersecurity_operations_center_build_workbench_view(active_state, tenant=tenant)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "workbench": workbench,
        "forms": _forms(),
        "wizards": _wizards(),
        "controls": _controls(),
        "assistant_panel": {
            "skills": ("triage_summary", "missing_evidence", "threat_intel_recommendation", "handoff_packet"),
            "requires_human_confirmation_for_mutation": True,
        },
        "side_effects": (),
    }


def cybersecurity_operations_center_render_detail(
    state: dict[str, Any],
    case_id: str,
) -> dict[str, Any]:
    detail = cybersecurity_operations_center_build_case_detail(state, case_id)
    if not detail["ok"]:
        return detail
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "detail": detail,
        "tabs": ("timeline", "evidence", "containment", "event_lineage", "relationship_graph"),
        "graph_enabled": True,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    state = cybersecurity_operations_center_empty_state()
    workbench = cybersecurity_operations_center_render_workbench(state)
    return {
        "ok": cybersecurity_operations_center_ui_contract()["ok"] and workbench["ok"],
        "workbench": workbench,
        "side_effects": (),
    }
