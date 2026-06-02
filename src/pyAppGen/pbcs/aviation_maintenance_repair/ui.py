"""Workbench UI metadata for the standalone aviation maintenance repair slice."""
from __future__ import annotations

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_EDGE_CASES, DOMAIN_OPERATIONS, DOMAIN_PARAMETERS, DOMAIN_RULES
from .models import BUSINESS_TABLES
from .mro_control import MRO_CONTROL_CAPABILITIES
from .workflows import workflow_catalog

PBC_KEY = "aviation_maintenance_repair"


def aviation_maintenance_repair_form_contracts() -> tuple[dict, ...]:
    return (
        {
            "form_id": "aircraft_intake_form",
            "title": "Aircraft Intake",
            "binds_table": f"{PBC_KEY}_aircraft",
            "fields": ("tail_number", "aircraft_type", "fleet_subtype", "status"),
        },
        {
            "form_id": "component_installation_form",
            "title": "Component Eligibility",
            "binds_table": f"{PBC_KEY}_component",
            "fields": ("component_id", "serial_number", "remaining_hours", "remaining_cycles", "release_certificate", "quarantine_state"),
        },
        {
            "form_id": "work_card_closeout_form",
            "title": "Work Card Closeout",
            "binds_table": f"{PBC_KEY}_work_card",
            "fields": ("work_card_id", "task_family", "status", "required_signoff_roles", "duplicate_inspection_required", "signoffs"),
        },
        {
            "form_id": "release_to_service_form",
            "title": "Release To Service",
            "binds_table": f"{PBC_KEY}_compliance_release",
            "fields": ("release_id", "tail_number", "certifier", "passed_checks", "pending_checks"),
        },
    )


def aviation_maintenance_repair_wizard_contracts() -> tuple[dict, ...]:
    workflows = workflow_catalog()["workflows"]
    return tuple(
        {
            "wizard_id": workflow["wizard"],
            "workflow_id": workflow["workflow_id"],
            "label": workflow["label"],
            "steps": workflow["steps"],
        }
        for workflow in workflows
    )


def aviation_maintenance_repair_control_catalog() -> tuple[dict, ...]:
    return (
        {"control_id": "tail_lookup", "type": "search", "label": "Tail Lookup"},
        {"control_id": "release_ready_badge", "type": "status_badge", "label": "Release Ready"},
        {"control_id": "blocker_table", "type": "table", "label": "Blockers"},
        {"control_id": "certifier_selector", "type": "picker", "label": "Certifier"},
        {"control_id": "document_intake_dropzone", "type": "upload", "label": "Document Intake"},
    )


def aviation_maintenance_repair_ui_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "AviationMaintenanceRepairWorkbench",
            "AviationMaintenanceRepairDetail",
            "AviationMaintenanceRepairAssistantPanel",
        ),
        "forms": aviation_maintenance_repair_form_contracts(),
        "wizards": aviation_maintenance_repair_wizard_contracts(),
        "controls": aviation_maintenance_repair_control_catalog(),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS + ("record_aircraft", "record_component", "record_work_card", "record_deferred_defect", "record_airworthiness_directive", "plan_document_instruction", "assess_release_to_service"),
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES + MRO_CONTROL_CAPABILITIES,
            "mro_control_panels": tuple(f"mro_control_{capability}" for capability in MRO_CONTROL_CAPABILITIES),
            "table_browsers": BUSINESS_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "release_panels": ("release_to_service_pack", "duplicate_inspection_evidence", "component_life_traceability", "tooling_and_consumable_lockouts"),
            "navigation_sections": ("overview", "release_to_service", "document_intake", "operations", "governance", "release_evidence"),
        },
        "side_effects": (),
    }


def aviation_maintenance_repair_render_workbench(release_queue=(), instruction_queue=()):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "forms": aviation_maintenance_repair_form_contracts(),
        "wizards": aviation_maintenance_repair_wizard_contracts(),
        "controls": aviation_maintenance_repair_control_catalog(),
        "table_browsers": BUSINESS_TABLES,
        "release_queue": tuple(release_queue),
        "instruction_queue": tuple(instruction_queue),
        "side_effects": (),
    }


def smoke_test():
    ui = aviation_maintenance_repair_ui_contract()
    return {"ok": ui["ok"] and bool(ui["forms"]) and bool(ui["wizards"]) and aviation_maintenance_repair_render_workbench()["ok"], "side_effects": ()}
