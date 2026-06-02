"""Focused standalone tests for land_real_estate_development."""

from pathlib import Path

from .. import controls, forms, release_evidence, standalone, wizards


BASE_PROJECT = {
    "project_id": "ridge-gateway",
    "tenant": "tenant-test",
    "name": "Ridge Gateway",
    "seller_price_expectation": 9000000,
    "control_threshold_pct": 70,
    "target_density_per_net_acre": 20,
}


BASE_PARCEL = {
    "project_id": "ridge-gateway",
    "parcel_id": "parcel-1",
    "apn": "09-777-100",
    "acreage": 18.0,
    "district": "MU-40",
    "environmental_status": "phase_i_clear",
    "wetlands_pct": 3.0,
    "floodplain_pct": 2.0,
    "easement_burden_pct": 4.0,
    "utilities": {
        "water": {"available": True, "capacity": 180},
        "sewer": {"available": True, "capacity": 170},
        "power": {"available": True, "capacity": 190},
        "telecom": {"available": True, "capacity": 160},
    },
}


def _seed_core_project(store: standalone.LandRealEstateDevelopmentStandaloneStore) -> None:
    assert store.create_project(BASE_PROJECT)["ok"] is True
    assert store.register_parcel(BASE_PARCEL)["ok"] is True
    assert store.record_land_acquisition(
        {
            "project_id": "ridge-gateway",
            "parcel_id": "parcel-1",
            "agreement_type": "option",
            "control_status": "controlled",
            "purchase_price": 8200000,
            "deposit_at_risk": 250000,
            "days_to_expiry": 45,
            "contingency_clear": True,
        }
    )["ok"] is True
    assert store.record_zoning_case(
        {
            "project_id": "ridge-gateway",
            "zoning_case_id": "zone-1",
            "district": "MU-40",
            "requested_use": "mixed_use_residential",
            "requested_units": 280,
            "by_right_units": 280,
            "status": "approved",
        }
    )["ok"] is True
    assert store.submit_entitlement(
        {
            "project_id": "ridge-gateway",
            "entitlement_id": "ent-1",
            "zoning_case_id": "zone-1",
            "entitlement_type": "tentative_map",
            "status": "approved",
            "unresolved_conditions": 0,
        }
    )["ok"] is True
    assert store.submit_permit_application(
        {
            "project_id": "ridge-gateway",
            "permit_id": "permit-1",
            "permit_type": "grading",
            "status": "issued",
            "blocking_comments": 0,
            "will_serve_status": "issued",
        }
    )["ok"] is True
    assert store.record_site_plan(
        {
            "project_id": "ridge-gateway",
            "site_plan_id": "site-1",
            "approved": True,
            "open_space_pct": 21,
            "parking_ratio": 1.6,
        }
    )["ok"] is True
    assert store.run_feasibility(
        {
            "project_id": "ridge-gateway",
            "feasibility_id": "fm-1",
            "planned_units": 280,
            "gross_revenue": 118000000,
            "vertical_cost": 64000000,
            "infrastructure_cost": 9000000,
            "soft_cost": 7400000,
            "financing_cost": 6200000,
            "contingency": 3400000,
            "developer_margin_pct": 14,
        }
    )["ok"] is True
    for approval_type in standalone.REQUIRED_APPROVAL_TYPES:
        assert store.record_approval(
            {
                "project_id": "ridge-gateway",
                "approval_type": approval_type,
                "status": "approved",
                "approved_by": "approver-test",
            }
        )["ok"] is True


def test_standalone_store_executes_domain_deep_land_flow() -> None:
    store = standalone.LandRealEstateDevelopmentStandaloneStore()
    try:
        _seed_core_project(store)
        readiness = store.assess_construction_readiness("ridge-gateway")
        sales = store.prepare_sales_handoff(
            {
                "project_id": "ridge-gateway",
                "map_recorded": True,
                "disclosures_ready": True,
                "pricing_basis_locked": True,
                "hoa_ready": True,
                "model_approvals_complete": True,
            }
        )
        lease = store.prepare_lease_handoff(
            {
                "project_id": "ridge-gateway",
                "tco_received": True,
                "common_area_ready": True,
                "turnover_units_ready": 60,
                "operating_budget_locked": True,
                "lease_constraints_reviewed": True,
            }
        )
        detail = store.get_project_detail("ridge-gateway")
        workbench = store.build_workbench("tenant-test")
        document_preview = store.preview_document_instruction(
            "Tentative map packet with utility will-serve and wetlands memo",
            "Update permit and parcel records for Ridge Gateway",
        )
        crud_preview = store.preview_datastore_crud(
            "update",
            standalone.OWNED_BUSINESS_TABLES[4],
            {"project_id": "ridge-gateway", "permit_id": "permit-1"},
        )
        assert readiness["ready"] is True
        assert sales["handoff"]["status"] == "ready"
        assert lease["handoff"]["status"] == "ready"
        assert detail["construction_readiness"]["ready"] is True
        assert workbench["construction_ready_count"] == 1
        assert workbench["handoff_ready_count"] == 1
        assert document_preview["preview"]["candidate_tables"]
        assert crud_preview["preview"]["route_candidates"]
    finally:
        store.close()


def test_standalone_controls_block_unready_project() -> None:
    store = standalone.LandRealEstateDevelopmentStandaloneStore()
    try:
        assert store.create_project(BASE_PROJECT)["ok"] is True
        assert store.register_parcel(
            {
                **BASE_PARCEL,
                "environmental_status": "phase_ii_required",
                "utilities": {
                    "water": {"available": True},
                    "sewer": {"available": False},
                    "power": {"available": True},
                    "telecom": {"available": False},
                },
            }
        )["ok"] is True
        assert store.record_land_acquisition(
            {
                "project_id": "ridge-gateway",
                "parcel_id": "parcel-1",
                "control_status": "under_loi",
                "days_to_expiry": 7,
                "contingency_clear": False,
            }
        )["ok"] is True
        assert store.run_feasibility(
            {
                "project_id": "ridge-gateway",
                "gross_revenue": 40000000,
                "vertical_cost": 36000000,
                "infrastructure_cost": 9000000,
                "soft_cost": 4500000,
                "financing_cost": 3000000,
                "contingency": 2000000,
                "developer_margin_pct": 18,
            }
        )["ok"] is True
        readiness = store.assess_construction_readiness("ridge-gateway")
        sales = store.prepare_sales_handoff({"project_id": "ridge-gateway"})
        assert readiness["ready"] is False
        assert "land_control_threshold_control" in readiness["blockers"]
        assert "environmental_constraint_control" in readiness["blockers"]
        assert "utility_availability_control" in readiness["blockers"]
        assert sales["handoff"]["status"] == "blocked"
    finally:
        store.close()


def test_route_surface_contracts_and_release_evidence_hold() -> None:
    service = standalone.LandRealEstateDevelopmentStandaloneService()
    try:
        project = standalone.dispatch_standalone_route(
            "POST",
            "/app/land-real-estate-development/projects",
            BASE_PROJECT,
            service=service,
        )
        workbench = standalone.dispatch_standalone_route(
            "GET",
            "/app/land-real-estate-development/workbench",
            {"tenant": "tenant-test"},
            service=service,
        )
        rendered = standalone.land_real_estate_development_render_standalone_workbench(workbench["result"])
        app_contract = standalone.land_real_estate_development_standalone_app_contract()
        smoke = standalone.land_real_estate_development_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert project["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert forms.form_contracts()["ok"] is True
        assert wizards.wizard_contracts()["ok"] is True
        assert controls.control_contracts()["ok"] is True
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
        assert evidence["documentation"]["ok"] is True
        assert release_evidence.validate_release_evidence()["ok"] is True
    finally:
        service.close()


def test_package_local_docs_exist() -> None:
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
