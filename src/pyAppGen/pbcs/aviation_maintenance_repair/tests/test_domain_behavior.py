"""Executable domain behavior tests for the aviation_maintenance_repair PBC."""

from __future__ import annotations

from pyAppGen.pbcs.aviation_maintenance_repair import implementation_contract, smoke_test
from pyAppGen.pbcs.aviation_maintenance_repair import runtime
from pyAppGen.pbcs.aviation_maintenance_repair.agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.aviation_maintenance_repair.agent import assistant_planning_contract
from pyAppGen.pbcs.aviation_maintenance_repair.capability_assurance import validate_table_stakes_capability_coverage
from pyAppGen.pbcs.aviation_maintenance_repair.domain_depth import DOMAIN_OPERATIONS, domain_capability_surface_contract, domain_depth_contract, execute_domain_operation
from pyAppGen.pbcs.aviation_maintenance_repair.maintenance_release import build_release_to_service_pack, evaluate_component_installation, evaluate_work_card_closeout
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import MRO_CONTROL_CAPABILITIES
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import assemble_defect_troubleshooting_evidence
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_aircraft_configuration_baseline
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_aog_triage_workbench
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_api_boundary_expansion
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_base_maintenance_control_tower
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_configuration_drift_dashboard
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_continuous_airworthiness_dashboard
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_cross_linked_audit_trail
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_defect_log
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_defect_risk_board
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_event_boundary_catalog
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_line_maintenance_workbench
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_maintenance_forecast
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_material_readiness_board
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_redelivery_readiness_package
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_serialized_component_history
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import build_shift_handover
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import calculate_life_limited_part_status
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import capture_inspection_evidence
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import compute_reliability_metrics
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import control_work_card_revision
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import correct_signed_record
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import detect_repeat_defect
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import draft_work_scope_from_planning_package
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import enforce_agent_certification_guardrails
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import enforce_duplicate_inspection
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import evaluate_consumable_life
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import evaluate_maintenance_program_applicability
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import evaluate_mel_cdl_deferment
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import evaluate_technician_authorization
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import evaluate_tooling_lockout
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import evaluate_vendor_repair_station_work
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import forecast_deferred_defect_breach
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import generate_non_routine_card
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import generate_release_evidence_pack
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import govern_cannibalization
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import govern_engineering_order
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import improve1_mro_control_contract
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import ingest_technical_document_revision
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import link_reliability_to_planning
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import manage_structural_corrosion_campaign
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import orchestrate_inspection_campaign
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import plan_airworthiness_directive_compliance
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import plan_maintenance_visit
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import quarantine_part_flow
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import register_service_bulletin_decision
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import run_pre_close_release_gate
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import synchronize_utilization_timeline
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import track_rotable_lifecycle
from pyAppGen.pbcs.aviation_maintenance_repair.mro_control import validate_parts_traceability_pack
from pyAppGen.pbcs.aviation_maintenance_repair.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.aviation_maintenance_repair.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.aviation_maintenance_repair.services import AviationMaintenanceRepairService, service_operation_contracts, service_operation_manifest
from pyAppGen.pbcs.aviation_maintenance_repair.ui import aviation_maintenance_repair_render_workbench, aviation_maintenance_repair_ui_contract


TENANT = "tenant_alpha"
AIRCRAFT = {"tenant": TENANT, "tail_number": "5Y-MRO", "aircraft_type": "B737", "fleet_subtype": "-800", "option_codes": ("ETOPS", "SATCOM"), "embodiment_status": {"MOD-1": "embodied"}, "flight_hours": 1000, "flight_cycles": 700}
COMPONENT = {"tenant": TENANT, "component_id": "COMP-LLP", "serial_number": "SER-LLP", "remaining_hours": 120, "remaining_cycles": 80, "limit_hours": 1000, "hours_since_new": 970, "limit_cycles": 600, "cycles_since_new": 590, "soft_alert_hours": 50, "soft_alert_cycles": 25, "release_certificate": "ARC-1", "source_chain": "approved-distributor", "life_document": "LLP-BTB", "effectivity_aircraft_types": ("B737",)}
WORK_CARD = {"tenant": TENANT, "work_card_id": "WC-100", "status": "closed", "task_family": "line", "aircraft_type": "B737", "source_revision": "AMM-42", "effectivity": ("B737",), "required_signoff_roles": ("performer", "duplicate_inspector"), "duplicate_inspection_required": True, "signoffs": ({"role": "performer", "technician_id": "tech-1"}, {"role": "duplicate_inspector", "technician_id": "tech-2"}), "controlled_tools": ({"tool_id": "torque-1", "returned": True, "calibration_due": "2026-12-31"},), "consumables": ({"batch_id": "sealant-1", "expiry": "2026-12-31"},)}
AUTHORIZATIONS = ({"technician_id": "tech-1", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"}, {"technician_id": "tech-2", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"})
POLICY_EVENT = {"event_type": "PolicyChanged", "event_id": "policy-alpha-001", "idempotency_key": "policy:alpha:001", "payload": {"tenant": TENANT, "policy_id": "mro-release"}}


def _ready_state() -> dict:
    state = runtime.aviation_maintenance_repair_empty_state()
    state = runtime.aviation_maintenance_repair_configure_runtime(state, {"database_backend": "postgresql", "event_topic": runtime.AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC})["state"]
    state = runtime.aviation_maintenance_repair_set_parameter(state, "workbench_limit", 50)["state"]
    state = runtime.aviation_maintenance_repair_register_rule(state, {"rule_id": "certifier_required_for_release", "tenant": TENANT, "scope": "release_to_service", "status": "active"})["state"]
    state = runtime.aviation_maintenance_repair_register_schema_extension(state, "work_card", {"inspection_media_hash": "text", "release_gate_score": "numeric"})["state"]
    state = runtime.aviation_maintenance_repair_receive_event(state, POLICY_EVENT)["state"]
    aircraft = runtime.aviation_maintenance_repair_record_aircraft(state, AIRCRAFT)
    component = runtime.aviation_maintenance_repair_record_component(aircraft["state"], COMPONENT)
    work_card = runtime.aviation_maintenance_repair_record_work_card(component["state"], WORK_CARD)
    directive = runtime.aviation_maintenance_repair_record_airworthiness_directive(work_card["state"], {"tenant": TENANT, "ad_id": "AD-100", "status": "complied", "applicable": True})
    defect = runtime.aviation_maintenance_repair_record_deferred_defect(directive["state"], {"tenant": TENANT, "defect_id": "DEF-100", "status": "closed", "expiry_date": "2026-12-31"})
    return defect["state"]


def test_aviation_mro_control_primitives_cover_all_improve1_capabilities() -> None:
    baseline = build_aircraft_configuration_baseline(AIRCRAFT, ({"task_id": "MPD-1", "option_code": "ETOPS", "mod_standard": "MOD-1"}, {"task_id": "MPD-2", "option_code": "HUD"}))
    utilization = synchronize_utilization_timeline(AIRCRAFT, ({"day": "2026-05-30", "flight_hours": 5.5, "flight_cycles": 3, "status": "flying"}, {"day": "2026-05-31", "status": "maintenance"}))
    history = build_serialized_component_history("SER-LLP", ({"position": "LH-engine", "event": "installed"}, {"position": "shop", "event": "removed", "defect_id": "DEF-1"}))
    life = calculate_life_limited_part_status(COMPONENT, as_of="2026-05-30")
    program = evaluate_maintenance_program_applicability({"revision": "AMP-9", "fleet_subtypes": ("-800",), "interval_source": "operator_amp", "escalation_reference": "ESC-1"}, AIRCRAFT)
    revision = control_work_card_revision(WORK_CARD, {"revision": "AMM-42"})
    non_routine = generate_non_routine_card(WORK_CARD, {"zone": "144", "ata": "32", "critical_path": True})
    defect_log = build_defect_log({"defect_id": "DEF-1", "status": "open"}, ({"action": "pilot_report"}, {"action": "troubleshooting"}, {"action": "rectified"}))
    deferment = evaluate_mel_cdl_deferment({"defect_id": "DEF-2", "category": "B", "expiry_date": "2026-06-01", "operational_procedures": ("placard",)}, {"days_until_next_maintenance": 5}, as_of="2026-05-30")
    ad_plan = plan_airworthiness_directive_compliance({"ad_id": "AD-200", "aircraft_types": ("B737",)}, ({"tail_number": "5Y-MRO", "aircraft_type": "B737", "days_to_due": -1},))
    sb = register_service_bulletin_decision({"sb_id": "SB-1", "decision": "adopt", "embodiment_strategy": "next_c_check", "affected_fleet": ("5Y-MRO",)})
    eo = govern_engineering_order({"engineering_order_id": "EO-1", "applicability": ("5Y-MRO",), "approval_basis": "Part-145", "repair_classification": "structural"}, AIRCRAFT)
    visit = plan_maintenance_visit({"visit_id": "VIS-1"}, ({**WORK_CARD, "critical_path": True, "slip_hours": 2},), ({"work_card_id": "WC-100", "status": "short"},))
    campaign = orchestrate_inspection_campaign({"campaign_id": "CORR-1"}, ({"zone": "144", "status": "open"},))
    duplicate = enforce_duplicate_inspection(WORK_CARD)
    auth = evaluate_technician_authorization({"technician_id": "tech-1", "task_family": "line", "aircraft_type": "B737"}, AUTHORIZATIONS, as_of="2026-05-30")
    handover = build_shift_handover({"visit_id": "VIS-1"}, ({"work_card_id": "WC-100", "isolated_system": "hydraulic-a", "safety_critical": True},))
    tooling = evaluate_tooling_lockout(({"tool_id": "torque-1", "returned": False, "calibration_due": "2026-12-31"},), as_of="2026-05-30")
    consumables = evaluate_consumable_life(({"batch_id": "sealant-1", "expiry": "2026-05-01"},), as_of="2026-05-30")
    material = build_material_readiness_board(({**WORK_CARD, "critical_path": True},), ({"work_card_id": "WC-100", "status": "short"},))
    traceability = validate_parts_traceability_pack(COMPONENT)
    quarantine = quarantine_part_flow({**COMPONENT, "quarantine_state": "suspect"})
    rotable = track_rotable_lifecycle(COMPONENT, ({"event": "removed"}, {"event": "repair_dispatched"}, {"event": "removed"}))
    cannibalization = govern_cannibalization({"donor_aircraft": "5Y-DON", "recipient_aircraft": "5Y-MRO", "restoration_due_date": "2026-06-15"})
    vendor = evaluate_vendor_repair_station_work({"repair_order_id": "RO-1", "vendor_capability_basis": "capability-list", "release_document": "EASA-F1", "technical_acceptance": True})
    inspection = capture_inspection_evidence({"evidence_id": "NDT-1", "method": "eddy-current", "inspector_qualification": "level-2", "measured_result": "within limit", "disposition": "accepted", "media": ("img-1",)})
    release_pack = generate_release_evidence_pack({"release_id": "REL-1", "signed_cards": ("WC-100",), "duplicate_inspections": ("DI-1",), "deferred_defects": ("DEF-100",), "parts_traceability": ("COMP-LLP",), "authorization_checks": ("AUTH-1",)})
    risk_board = build_defect_risk_board(({"defect_id": "DEF-2", "mel_category": "B", "recurrence_count": 3, "days_remaining": 1},))
    repeat = detect_repeat_defect({"defect_id": "DEF-3", "tail_number": "5Y-MRO", "ata": "32", "symptom": "shimmy"}, ({"tail_number": "5Y-MRO", "ata": "32", "symptom": "shimmy", "days_since_clearance": 7},))
    reliability = compute_reliability_metrics(({"ata": "32"}, {"ata": "32"}), ({"ata": "73"},))
    breach = forecast_deferred_defect_breach({"defect_id": "DEF-2", "expiry_date": "2026-06-01"}, {"days_until_next_maintenance": 5}, as_of="2026-05-30")
    forecast = build_maintenance_forecast(({"task_id": "MPD-1", "hour_interval": 1020, "cycle_interval": 730},), {"projected_hours": 1000, "projected_cycles": 700})
    aog = build_aog_triage_workbench({"tail_number": "5Y-MRO"}, {"authorized_staff": True, "nearby_parts": False})
    line = build_line_maintenance_workbench({"tail_number": "5Y-MRO", "open_defects": ({"defect_id": "DEF-2", "dispatch_critical": True},)})
    base = build_base_maintenance_control_tower(({"visit_id": "VIS-1", "dock": "D1", "critical_path_slipped": True},))
    events = build_event_boundary_catalog()
    api = build_api_boundary_expansion()
    audit = build_cross_linked_audit_trail(({"aircraft": "5Y-MRO", "component": "SER-LLP", "work_card": "WC-100", "certifier": "cert-1"},))
    correction = correct_signed_record({"work_card_id": "WC-100", "statement": "old"}, {"requested_by": "qa", "reason": "typo", "approved_by": "cert-1", "superseding_statement": "corrected"})
    document = ingest_technical_document_revision({"document_type": "AMM", "revision": "AMM-43"}, ({"work_card_id": "WC-100", "current_revision": "AMM-42"},))
    scope = draft_work_scope_from_planning_package({"due_tasks": ({"task_id": "MPD-1", "reason": "due"},), "open_defects": ({"defect_id": "DEF-2"},)})
    troubleshooting = assemble_defect_troubleshooting_evidence({"defect_id": "DEF-3", "ata": "32", "symptom": "shimmy"}, ({"ata": "32", "symptom": "shimmy", "finding": "prior tire change"},), ({"reference": "AMM-32", "approved": True},))
    guardrail = enforce_agent_certification_guardrails({"action": "issue_crs"})
    feedback = link_reliability_to_planning({"finding_id": "REL-1", "ata": "32", "repeat_count": 3, "component_family": "wheel"})
    drift = build_configuration_drift_dashboard(({"tail_number": "5Y-MRO", "baseline": "MOD-A", "configuration": "MOD-A"}, {"tail_number": "5Y-OLD", "configuration": "MOD-B"}))
    redelivery = build_redelivery_readiness_package(AIRCRAFT, {"configuration_history": True, "major_maintenance": True, "ad_status": True})
    corrosion = manage_structural_corrosion_campaign({"campaign_id": "CORR-1"}, ({"zone": "144", "follow_up_required": True},))
    preclose = run_pre_close_release_gate({"open_work_cards": (), "outstanding_defects": ("DEF-2",), "invalid_signoff_authority": ()})
    dashboard = build_continuous_airworthiness_dashboard({"open_ad_count": 1, "open_deferred_defects": 6, "repeat_defects": 2, "release_confidence": 0.75, "readiness": 0.9, "available_certifiers": 3})
    contract = improve1_mro_control_contract()

    results = (baseline, utilization, history, life, program, revision, non_routine, defect_log, deferment, ad_plan, sb, eo, visit, campaign, duplicate, auth, handover, tooling, consumables, material, traceability, quarantine, rotable, cannibalization, vendor, inspection, release_pack, risk_board, repeat, reliability, breach, forecast, aog, line, base, events, api, audit, correction, document, scope, troubleshooting, guardrail, feedback, drift, redelivery, corrosion, preclose, dashboard, contract)

    assert len(MRO_CONTROL_CAPABILITIES) == 50
    assert all(result["ok"] is True for result in results)
    assert baseline["applicable_requirements"][0]["task_id"] == "MPD-1"
    assert utilization["totals"]["grounded_intervals"] == 1
    assert life["status"] == "alert"
    assert deferment["breach_before_maintenance"] is True
    assert visit["release_risk"] == "high"
    assert duplicate["valid"] is True
    assert tooling["release_blocked"] is True
    assert consumables["release_blocked"] is True
    assert traceability["complete"] is True
    assert quarantine["installation_blocked"] is True
    assert release_pack["ready"] is True
    assert repeat["recurrent"] is True
    assert aog["next_decision"] == "resolve_blockers"
    assert guardrail["blocked"] is True and guardrail["reason"] == "human_certifier_required"
    assert preclose["release_blocked"] is True
    assert dashboard["posture"] == "watch"
    assert contract["capability_count"] == 50
    assert all(not result["shared_table_access"] for result in results)


def test_aviation_runtime_services_routes_ui_and_agent_are_executable() -> None:
    state = _ready_state()
    duplicate = runtime.aviation_maintenance_repair_receive_event(state, POLICY_EVENT)
    dead = runtime.aviation_maintenance_repair_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "event_id": "bad-event", "idempotency_key": "bad-event", "payload": {"tenant": TENANT}})
    release = runtime.aviation_maintenance_repair_assess_release_to_service(dead["state"], {"release_id": "REL-100", "tail_number": "5Y-MRO", "component_ids": ("COMP-LLP",), "work_card_ids": ("WC-100",), "deferred_defect_ids": ("DEF-100",), "airworthiness_directive_ids": ("AD-100",), "technician_authorizations": AUTHORIZATIONS, "certifier": {"technician_id": "cert-1", "release_authorization": True}, "as_of": "2026-05-30"})
    blocked = runtime.aviation_maintenance_repair_assess_release_to_service(release["state"], {"release_id": "REL-BLOCKED", "tail_number": "5Y-MRO", "work_cards": ({**WORK_CARD, "status": "open"},), "technician_authorizations": AUTHORIZATIONS, "as_of": "2026-05-30"})
    doc_plan = runtime.aviation_maintenance_repair_plan_document_instruction(blocked["state"], "AMM revision and defect log", "Create work card release signoff package", {"tail_number": "5Y-MRO"})
    query = runtime.aviation_maintenance_repair_query_workbench(doc_plan["state"], {"tail_number": "5Y-MRO"})
    assessment = runtime.aviation_maintenance_repair_run_advanced_assessment(doc_plan["state"], {"tenant": TENANT})
    bad_extension = runtime.aviation_maintenance_repair_register_schema_extension(doc_plan["state"], "shared_mro_table", {"x": "jsonb"})
    service = AviationMaintenanceRepairService()
    service_release = service.assess_release_to_service({"release_id": "REL-SVC", "aircraft": AIRCRAFT, "work_cards": (WORK_CARD,), "components": (COMPONENT,), "technician_authorizations": AUTHORIZATIONS, "certifier": {"technician_id": "cert-1", "release_authorization": True}, "as_of": "2026-05-30"})
    service_query = service.query_workbench({"tenant": TENANT})
    route_dispatch = dispatch_route("POST /aviation-maintenance-repair/release-plans", {"release_id": "REL-100"})
    ui = aviation_maintenance_repair_ui_contract()
    rendered = aviation_maintenance_repair_render_workbench(query["release_queue"], query["instruction_queue"])
    agent_plan = document_instruction_plan("defect and component evidence", "update defect and component release evidence", {"tail_number": "5Y-MRO"})
    crud = datastore_crud_plan("create", "aviation_maintenance_repair_work_card", {"work_card_id": "WC-200"})
    rejected_crud = datastore_crud_plan("update", "shared_mro_table", {})

    assert duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "aviation_maintenance_repair_appgen_dead_letter_event"
    assert release["ok"] is True and release["release_pack"]["status"] == "release_ready"
    assert blocked["ok"] is False and any(item["code"] == "human_certifier_required" for item in blocked["release_pack"]["blockers"])
    assert doc_plan["document_plan"]["requires_human_confirmation"] is True
    assert query["ok"] is True and query["release_queue"]
    assert assessment["ok"] is True and "release_workflow_visible" in assessment["explanations"]
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert runtime.aviation_maintenance_repair_build_schema_contract()["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert runtime.aviation_maintenance_repair_build_api_contract()["stream_engine_picker_visible"] is False
    assert runtime.aviation_maintenance_repair_build_release_evidence()["generated_artifacts"]["improve1_mro_control"]["capability_count"] == 50
    assert runtime.aviation_maintenance_repair_verify_owned_table_boundary(("foreign_table",))["ok"] is False
    assert runtime.aviation_maintenance_repair_runtime_smoke()["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_release["ok"] is True and service_release["emits"] == ("AviationMaintenanceRepairApproved",)
    assert service_query["read_only"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert route_dispatch["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["mro_control_panels"]) == 50
    assert rendered["ok"] is True
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["single_agent_contribution"] == "aviation_maintenance_repair_skills"
    assert assistant_planning_contract()["guardrails"]["assistant_can_certify"] is False
    assert agent_plan["release_to_service_preview"]["assistant_can_certify"] is False
    assert crud["ok"] is True and crud["requires_confirmation"] is True
    assert rejected_crud["ok"] is False
    assert composed_agent_contribution()["ok"] is True


def test_aviation_release_evidence_and_package_contract_are_executable() -> None:
    component_ok = evaluate_component_installation(COMPONENT, AIRCRAFT, as_of="2026-05-30")
    component_bad = evaluate_component_installation({**COMPONENT, "remaining_cycles": 0}, AIRCRAFT, as_of="2026-05-30")
    card_ok = evaluate_work_card_closeout(WORK_CARD, AUTHORIZATIONS, as_of="2026-05-30")
    self_signed = evaluate_work_card_closeout({**WORK_CARD, "signoffs": ({"role": "performer", "technician_id": "tech-1"}, {"role": "duplicate_inspector", "technician_id": "tech-1"})}, AUTHORIZATIONS, as_of="2026-05-30")
    release_ready = build_release_to_service_pack({"release_id": "REL-PACK", "aircraft": AIRCRAFT, "components": (COMPONENT,), "work_cards": (WORK_CARD,), "deferred_defects": ({"defect_id": "DEF-100", "status": "closed", "expiry_date": "2026-12-31"},), "airworthiness_directives": ({"ad_id": "AD-100", "status": "complied", "applicable": True},), "technician_authorizations": AUTHORIZATIONS, "certifier": {"technician_id": "cert-1", "release_authorization": True}, "as_of": "2026-05-30"})
    release_build = build_release_evidence()
    release_manifest = release_readiness_manifest()
    release_validation = validate_release_evidence()
    capability_validation = validate_table_stakes_capability_coverage()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert component_ok["ok"] is True
    assert component_bad["ok"] is False and component_bad["blockers"][0]["code"] == "life_limit_cycles_exhausted"
    assert card_ok["ok"] is True
    assert self_signed["ok"] is False and any(item["code"] == "self_inspection_blocked" for item in self_signed["blockers"])
    assert release_ready["ok"] is True and release_ready["status"] == "release_ready"
    assert release_build["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert capability_validation["ok"] is True
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["ui_contract"]["full_capability_surface"]["mro_control_panels"]
    assert package_smoke["ok"] is True
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(item["ok"] is True for item in executed)
    assert all(item["target_table"].startswith("aviation_maintenance_repair_") for item in executed)
