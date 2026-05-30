from pyAppGen.pbcs.capital_projects_delivery import project_control as pc
from pyAppGen.pbcs.capital_projects_delivery import routes, runtime, ui
from pyAppGen.pbcs.capital_projects_delivery.release_evidence import release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.capital_projects_delivery.services import CapitalProjectsDeliveryService


def test_project_control_primitives_cover_all_improve1_capabilities():
    results = [
        pc.evaluate_stage_gate("idea", "screening", {"business_case_defined": True}, "project_sponsor", "project_sponsor"),
        pc.validate_wbs_hierarchy(({"wbs_id": "1", "area": "A", "discipline": "civil", "control_account": "CA1"}, {"wbs_id": "1.1", "parent_id": "1"})),
        pc.control_estimate_basis(({"estimate_id": "E1", "status": "sanctioned", "effective_at": "2026-01-01"}, {"estimate_id": "E2", "predecessor_id": "E1", "status": "forecast", "effective_at": "2026-05-01"})),
        pc.govern_schedule_baseline(({"baseline_id": "B1", "current": True, "total_float_days": 10, "float_threshold_days": 5},)),
        pc.build_milestone_library(({"milestone_type": "mechanical_completion", "success_criteria": "signed", "phase": "commissioning"},)),
        pc.control_package_cost(({"package_id": "P1", "approved_budget": 100, "awarded_value": 90, "forecast_final_cost": 95},)),
        pc.earn_progress(({"rule_of_credit": "installed_quantity", "earned_quantity": 50, "total_quantity": 100},)),
        pc.calculate_performance_indices({"planned_value": 100, "earned_value": 90, "actual_cost": 95, "trend": "down"}),
        pc.track_change_order({"state": "approved", "approved_impact": 10, "estimated_impact": 12, "schedule_entitlement": "granted"}),
        pc.manage_early_warning(({"event_date": "2026-05-25", "sla_days": 10},), as_of="2026-05-30"),
        pc.quantify_risks(({"probability": 0.5, "cost_impact": 100, "schedule_days": 10, "triggered": True},)),
        pc.manage_opportunities(({"status": "approved", "expected_benefit": 100, "confidence": 0.8},)),
        pc.build_permit_dependency_matrix(({"status": "approved", "tied_workfront": "WF1", "expiry": "2026-06-10"},)),
        pc.track_long_lead_equipment(({"item_id": "LL1", "shipment_status": "on_time", "received": True, "site_ready": True},)),
        pc.evaluate_package_readiness({"scope_freeze": True, "ifc_maturity": True, "material_strategy": True, "access_handoff": True, "temporary_facilities": True, "owner_furnished_items": True, "interface_agreement": True}),
        pc.manage_field_constraints(({"start_date": "2026-05-28", "status": "open", "sla_days": 5},), as_of="2026-05-30"),
        pc.manage_interfaces(({"interface_id": "I1", "status": "accepted", "due_date": "2026-05-01"},)),
        pc.evaluate_mechanical_completion(({"system_id": "S1", "mapped_work_complete": True, "completion_criteria_met": True},)),
        pc.control_punch_list(({"severity": "B", "status": "open"},)),
        pc.track_pre_commissioning(({"activity_id": "A1", "status": "passed"},)),
        pc.control_commissioning_sequence(({"system_id": "S1", "utility_available": True, "vendor_attendance": True, "energization_approved": True, "startup_permit": True},)),
        pc.validate_handover_dossier({"as_built_drawings": True, "test_packs": True, "warranties": True, "spares": True, "training": True, "operating_procedures": True, "asset_data": True}),
        pc.track_post_handover_obligations(({"critical": False, "status": "open"},)),
        pc.check_funding_appropriation({"committed_amount": 80, "pending_exposure": 10, "approved_amount": 100}),
        pc.govern_contingency_drawdown(({"amount": 10, "linked_risk_or_change": "R1"},)),
        pc.track_productivity_risk(({"planned_productivity": 10, "actual_productivity": 11},)),
        pc.model_weather_disruption(({"delay_type": "weather", "days": 2}, {"delay_type": "access", "days": 1})),
        pc.manage_quality_hold_points(({"point_id": "H1", "status": "released"},)),
        pc.build_sequence_workbench(({"package_id": "P1", "area": "A", "system": "S", "blocker": None},)),
        pc.generate_monthly_review_pack({"capital_project": True, "epc_package": True, "project_risk": True, "progress_measurement": True, "turnover_package": True}),
        pc.build_readiness_release_evidence({"sanction": True, "field_execution": True, "startup_readiness": True, "handover": True}),
        pc.plan_assistant_project_controls("scheduler", "draft schedule diagnostics"),
        pc.parse_project_document({"date": "2026-05-30", "party": "contractor", "package": "P1"}, "notice"),
        pc.refine_event_boundary({"lifecycle_stage": "screening", "affected_object_type": "capital_project", "project_key": "CP1", "wbs_scope": "A", "package_reference": "P1", "system_reference": "S1"}),
        pc.handle_consumed_project_event({"event_type": "PolicyChanged"}, ({"record_id": "CP1"},)),
        pc.harden_api_boundary("POST /capital-projects", {"fields_changed": ("name",)}),
        pc.guard_idempotent_update("progress_import", {"idempotency_key": "K1"}, ("K0",)),
        pc.triage_dead_letter({"code": "missing_project", "object_type": "permit_milestone"}),
        pc.version_configuration_change({"name": "float_threshold", "value": 5, "approved_by": "pm", "effective_at": "2026-05-30"}),
        pc.evaluate_policy_rule({"rule_id": "permit_before_work", "required_flag": "permit_ready"}, {"permit_ready": True}),
        pc.run_control_assertions(({"record_id": "R1", "stale_forecast": False},)),
        pc.register_owner_schema_extension({"field_name": "facility_code", "purpose": "owner", "owning_team": "controls", "projection_impact": "none", "validation_rule": "required", "rollout_plan": "phased", "table": "capital_projects_delivery_capital_project"}),
        pc.define_governed_model_semantics(({"term": "mechanical_complete", "definition": "construction scope signed"},)),
        pc.build_portfolio_rollup(({"project_id": "CP1", "forecast": 110, "sanctioned_budget": 100, "red_driver": "permit"},)),
        pc.map_cross_pbc_boundaries(),
        pc.review_startup_readiness({"construction_complete": True, "commissioning_passed": True, "permits_ready": True, "training_complete": True, "risks_accepted": True, "authorization": True}),
        pc.verify_operations_handover({"operator_training": True, "operating_procedures": True, "maintenance_task_seeds": True, "spares_available": True, "vendor_support": True}),
        pc.onboard_live_project({"capital_project": True, "epc_package": True, "permit_milestone": True, "progress_measurement": True, "project_risk": True}),
        pc.assure_domain_scenarios({"gate_approval": True, "wbs_rollup": True, "long_lead_slip": True, "permit_expiry": True, "change_order_approval": True, "system_completion": True, "startup_readiness": True, "handover_dossier": True}),
        pc.capture_closeout_knowledge({"final_cost_variance": 1, "milestone_slippage_causes": "permits", "change_concentration": "civil", "startup_bottlenecks": "utility", "handover_defects": "none", "lessons_summary": "start permits early"}),
    ]
    assert len(pc.PROJECT_CONTROL_CAPABILITIES) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(pc.PROJECT_CONTROL_CAPABILITIES)
    assert results[0]["transition_allowed"] is True
    assert results[7]["spi"] == 0.9
    assert results[30]["release_ready"] is True
    assert results[48]["release_allowed"] is True
    assert results[49]["closeout_allowed"] is True


def test_project_runtime_ui_service_routes_and_release_evidence_surface_controls():
    service = CapitalProjectsDeliveryService()
    created = service.command_capital_project({"tenant": "tenant-a", "code": "CP-1", "name": "Project 1", "reported_at": "2026-05-30"})
    checklist = service.record_gate_checklist({"project_id": "CP-1", "criteria_status": {"business_case_defined": True, "sponsorship_assigned": True}, "updated_by": "pm", "updated_at": "2026-05-30"})
    approved = service.approve_capital_project_gate({"project_id": "CP-1", "target_stage": "screening", "approver_role": "project_sponsor", "approved_by": "sponsor", "approved_at": "2026-05-30"})
    route = routes.dispatch_route("GET /capital-projects-delivery-workbench", {"tenant": "tenant-a"}, service=service)
    release = runtime.capital_projects_delivery_build_release_evidence()
    ui_contract = ui.capital_projects_delivery_ui_contract()
    boundary = runtime.capital_projects_delivery_verify_owned_table_boundary(("capital_projects_delivery_capital_project", "finance_table"))
    assert created["ok"] is True
    assert checklist["ok"] is True
    assert approved["ok"] is True
    assert route["ok"] is True
    assert runtime.CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert boundary["ok"] is False
    assert ui_contract["stream_engine_picker_visible"] is False
    assert len(ui_contract["full_capability_surface"]["project_control_panels"]) == 50
    assert release["generated_artifacts"]["improve1_project_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_project_control" and check["ok"] for check in release["checks"])


def test_project_release_readiness_and_runtime_smoke_include_control_contract():
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    smoke = runtime.capital_projects_delivery_runtime_smoke()
    capabilities = runtime.capital_projects_delivery_runtime_capabilities()
    contract = pc.improve1_project_control_contract()
    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert capabilities["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["shared_table_access"] is False
    assert contract["stream_engine_picker_visible"] is False
