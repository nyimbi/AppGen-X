"""One-PBC application surface for field service operations."""

from __future__ import annotations

import hashlib

PBC_KEY = "field_service_management"
OWNED_TABLES = tuple(f"{PBC_KEY}_{name}" for name in (
    "field_work_order", "dispatch_assignment", "technician_profile", "mobile_task", "parts_usage",
    "service_sla", "service_history", "customer_service_update", "technician_live_location",
    "technician_location_breadcrumb", "technician_availability", "technician_home_base",
    "service_route_plan", "service_route_stop", "service_route_leg", "route_reoptimization",
    "mobile_task_dependency", "task_safety_gate", "job_tool_requirement", "tool_inventory",
    "tool_calibration", "van_stock_position", "skill_assignment_score", "assignment_constraint",
    "geofence_event", "location_privacy_consent",
))


def _digest(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def field_service_management_forms_contract() -> dict:
    forms = (
        {"form_id": "work_order_form", "writes_table": "field_service_management_field_work_order", "command": "create_field_work_order", "fields": ("tenant", "work_order_id", "customer_id", "site_id", "priority", "required_skills", "status"), "validations": ("customer_bound", "site_required", "priority_supported", "required_skills_declared")},
        {"form_id": "technician_profile_form", "writes_table": "field_service_management_technician_profile", "command": "upsert_technician_profile", "fields": ("tenant", "technician_id", "name", "skills", "certifications", "home_base", "status"), "validations": ("skills_required", "certifications_current", "home_base_geocoded")},
        {"form_id": "technician_location_form", "writes_table": "field_service_management_technician_live_location", "command": "record_technician_location", "fields": ("tenant", "location_id", "technician_id", "latitude", "longitude", "accuracy_meters", "recorded_at"), "validations": ("privacy_consent_active", "accuracy_in_range", "geofence_checked")},
        {"form_id": "availability_form", "writes_table": "field_service_management_technician_availability", "command": "update_technician_availability", "fields": ("tenant", "availability_id", "technician_id", "shift_start", "shift_end", "capacity", "status"), "validations": ("shift_range_valid", "capacity_positive", "labor_rule_checked")},
        {"form_id": "dispatch_assignment_form", "writes_table": "field_service_management_dispatch_assignment", "command": "assign_dispatch", "fields": ("tenant", "assignment_id", "work_order_id", "technician_id", "route_id", "assignment_score", "status"), "validations": ("technician_available", "skills_match", "tools_available", "travel_time_feasible")},
        {"form_id": "route_plan_form", "writes_table": "field_service_management_service_route_plan", "command": "optimize_route", "fields": ("tenant", "route_id", "technician_id", "start_location", "stops", "optimization_goal", "status"), "validations": ("stops_geocoded", "sla_windows_respected", "traffic_model_bound")},
        {"form_id": "mobile_task_form", "writes_table": "field_service_management_mobile_task", "command": "create_mobile_task", "fields": ("tenant", "task_id", "work_order_id", "sequence", "task_type", "instructions", "status"), "validations": ("work_order_exists", "sequence_unique", "instructions_required")},
        {"form_id": "task_dependency_form", "writes_table": "field_service_management_mobile_task_dependency", "command": "plan_task_dependencies", "fields": ("tenant", "dependency_id", "task_id", "depends_on_task_id", "dependency_type", "blocking", "status"), "validations": ("no_cycles", "tasks_same_work_order", "blocking_reason_required")},
        {"form_id": "job_tool_requirement_form", "writes_table": "field_service_management_job_tool_requirement", "command": "validate_job_tools", "fields": ("tenant", "requirement_id", "work_order_id", "tool_type", "quantity", "calibration_required", "status"), "validations": ("tool_type_supported", "quantity_positive", "calibration_status_checked")},
        {"form_id": "van_stock_form", "writes_table": "field_service_management_van_stock_position", "command": "reserve_van_stock", "fields": ("tenant", "stock_id", "technician_id", "part_id", "quantity_on_hand", "reserved_quantity", "status"), "validations": ("part_projection_bound", "quantity_available", "reservation_audited")},
        {"form_id": "sla_safety_form", "writes_table": "field_service_management_task_safety_gate", "command": "evaluate_task_safety", "fields": ("tenant", "safety_gate_id", "task_id", "hazard_type", "required_ppe", "approval_status", "status"), "validations": ("ppe_required", "hazard_acknowledged", "approval_before_start")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def field_service_management_wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "work_order_dispatch_wizard", "steps": ("capture_work_order", "score_skills", "check_tools", "optimize_route", "assign_technician"), "completion_event": "TechnicianDispatched"},
        {"wizard_id": "live_route_reoptimization_wizard", "steps": ("monitor_location", "detect_delay", "reoptimize_route", "notify_customer", "update_assignment"), "completion_event": "RouteReoptimizationRequested"},
        {"wizard_id": "mobile_task_execution_wizard", "steps": ("download_tasks", "check_dependencies", "pass_safety_gate", "capture_parts", "complete_task"), "completion_event": "FieldTaskCompleted"},
        {"wizard_id": "job_tool_readiness_wizard", "steps": ("derive_tool_requirements", "check_inventory", "verify_calibration", "reserve_tools", "release_after_job"), "completion_event": "JobToolsReserved"},
        {"wizard_id": "skills_based_assignment_wizard", "steps": ("parse_job_requirements", "score_technicians", "apply_constraints", "explain_assignment", "confirm_dispatch"), "completion_event": "SkillBasedAssignmentRecommended"},
        {"wizard_id": "sla_recovery_wizard", "steps": ("detect_sla_risk", "find_nearest_skilled_worker", "resequence_route", "notify_customer", "record_recovery"), "completion_event": "ServiceSlaBreached"},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def field_service_management_controls_contract() -> dict:
    controls = (
        {"control_id": "location_privacy_consent_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_technician_live_location", "field_service_management_location_privacy_consent")},
        {"control_id": "skills_assignment_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_skill_assignment_score", "field_service_management_dispatch_assignment")},
        {"control_id": "route_sla_window_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_service_route_plan", "field_service_management_service_route_stop", "field_service_management_service_sla")},
        {"control_id": "task_dependency_safety_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_mobile_task_dependency", "field_service_management_task_safety_gate")},
        {"control_id": "tool_calibration_custody_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_job_tool_requirement", "field_service_management_tool_calibration", "field_service_management_tool_inventory")},
        {"control_id": "van_stock_reservation_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_van_stock_position", "field_service_management_parts_usage")},
        {"control_id": "customer_update_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_customer_service_update", "field_service_management_service_history")},
        {"control_id": "appgen_event_replay_gate", "blocks_on_failure": True, "table_scope": ("field_service_management_appgen_outbox_event", "field_service_management_appgen_inbox_event", "field_service_management_appgen_dead_letter_event")},
        {"control_id": "owned_boundary_and_no_shared_tables_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_field_service_management_app_contract() -> dict:
    forms = field_service_management_forms_contract()["forms"]
    wizards = field_service_management_wizards_contract()["wizards"]
    controls = field_service_management_controls_contract()["controls"]
    return {"ok": bool(forms) and bool(wizards) and bool(controls), "pbc": PBC_KEY, "single_pbc_app": True, "database_backed": True, "allowed_database_backends": ("postgresql", "mysql", "mariadb"), "owned_tables": OWNED_TABLES, "forms": forms, "wizards": wizards, "controls": controls, "workbench": "FieldServiceManagementWorkbench", "assistant_panel": "FieldServiceManagementAssistantPanel", "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "side_effects": ()}


def document_instruction_field_service_management_plan(document: str, instructions: str) -> dict:
    text = f"{document} {instructions}".lower()
    if "where" in text or "location" in text or "gps" in text:
        operation, table = "record_technician_location", "field_service_management_technician_live_location"
    elif "route" in text or "drive" in text or "traffic" in text:
        operation, table = "optimize_route", "field_service_management_service_route_plan"
    elif "tool" in text or "calibration" in text:
        operation, table = "validate_job_tools", "field_service_management_job_tool_requirement"
    elif "skill" in text or "assign" in text or "technician" in text:
        operation, table = "assign_dispatch", "field_service_management_dispatch_assignment"
    elif "task" in text or "dependency" in text or "safety" in text:
        operation, table = "plan_task_dependencies", "field_service_management_mobile_task_dependency"
    elif "stock" in text or "part" in text:
        operation, table = "reserve_van_stock", "field_service_management_van_stock_position"
    else:
        operation, table = "create_field_work_order", "field_service_management_field_work_order"
    return {"ok": True, "pbc": PBC_KEY, "document_digest": _digest(document, instructions), "proposed_operation": operation, "target_table": table, "requires_human_confirmation": True, "crud_datastore_mutation": True, "event_contract": "AppGen-X", "side_effects": ()}


def app_surface_smoke_test() -> dict:
    app = single_pbc_field_service_management_app_contract()
    location = document_instruction_field_service_management_plan("where are technicians", "show live location")
    route = document_instruction_field_service_management_plan("urgent job", "optimize route and assign skills")
    checks = (app["ok"], len(app["forms"]) >= 11, len(app["wizards"]) >= 6, len(app["controls"]) >= 9, location["target_table"] == "field_service_management_technician_live_location", route["target_table"] == "field_service_management_service_route_plan", all(table.startswith("field_service_management_") for control in app["controls"] for table in control["table_scope"]))
    return {"ok": all(checks), "single_pbc_app": app, "document_plans": (location, route), "side_effects": ()}
