from pyAppGen.pbcs.building_information_modeling_ops import bim_control as bc
from pyAppGen.pbcs.building_information_modeling_ops import routes, runtime, ui
from pyAppGen.pbcs.building_information_modeling_ops.release_evidence import release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.building_information_modeling_ops.services import BuildingInformationModelingOpsService


def test_bim_control_primitives_cover_all_improve1_capabilities():
    version = {
        "version_id": "VER-1",
        "discipline": "architectural",
        "authoring_party": "Studio",
        "coordinate_basis": "grid-a",
        "issue_purpose": "shared",
        "spatial_coverage": ("tower-a",),
        "lod_target": "LOD-300",
        "approval_state": "approved",
        "checksum": "sha256:ver1",
        "survey_point": {"x": 1000, "y": 2000, "z": 15},
        "project_base_point": {"x": 995, "y": 1995, "z": 15},
        "true_north_degrees": 12.0,
        "elevation_datum": "msl",
        "unit_scale": 1.0,
    }
    baseline = {key: version[key] for key in ("coordinate_basis", "survey_point", "project_base_point", "true_north_degrees", "elevation_datum", "unit_scale")}
    assets = (
        {"asset_id": "AHU-1", "tag": "MEP-AHU-001", "asset_class": "ahu", "system": "HVAC", "zone": "Z1", "location": "L1", "complete": True, "discipline": "mechanical", "prerequisites": ("test",), "completed_prerequisites": ("test",)},
    )
    results = [
        bc.build_federation_registry((version,)),
        bc.validate_coordinate_assurance(version, baseline),
        bc.govern_issue_purpose(version, "construction"),
        bc.link_drawing_revision(version, ({"drawing_id": "A-101", "approval_state": "approved", "revision": "P01"},)),
        bc.validate_spatial_hierarchy(({"id": "SP-1", "site": "S", "building": "B", "storey": "01", "zone": "Z1", "space": "101"},)),
        bc.create_quantity_snapshot(version, ({"category": "walls", "unit": "m2", "quantity": 20}, {"category": "doors", "unit": "each", "quantity": 2})),
        bc.classify_clash_issue({"clash_type": "clearance", "severity": "high"}),
        bc.group_duplicate_clashes(({"issue_id": "C1", "location": "L1", "discipline_pair": "M/E", "system": "HVAC", "root_condition": "riser"}, {"issue_id": "C2", "location": "L1", "discipline_pair": "M/E", "system": "HVAC", "root_condition": "riser"})),
        bc.build_model_issue_ledger(({"issue_id": "I1", "source": "clash", "blocking": True, "status": "closed"},)),
        bc.route_approval_matrix({"discipline": "architectural", "zone": "Z1", "issue_purpose": "construction", "risk_score": 30}, ({"discipline": "architectural", "zone": "Z1", "issue_purpose": "construction", "required_roles": ("architect", "bim_manager")},)),
        bc.evaluate_partial_publish({"scope_slice": ("tower-a",)}, ()),
        bc.compare_model_versions({"version_id": "V1", "geometry": 1, "quantities": 10}, {"version_id": "V2", "geometry": 2, "quantities": 12}),
        bc.validate_asset_tags(assets, ("MEP-",)),
        bc.validate_structured_handover({"facility": True, "floor": True, "space": True, "system": True, "component": True, "type": True, "contact": True, "spares": True, "warranty": True, "maintenance": True}),
        bc.check_space_room_integrity(({"space_id": "101", "room_number": "101", "operational_classification": "plant"},)),
        bc.govern_system_zone_membership(assets, ("ahu",)),
        bc.validate_location_asset_consistency(assets, ("L1",)),
        bc.build_drawing_dependency_register(({"drawing_id": "A-101", "required": True, "revision_state": "P01", "model_revision_state": "P01"},)),
        bc.control_revision_transmittals(({"transmittal_id": "T1", "ack_required": True, "acknowledged_at": "2026-05-01"},)),
        bc.create_work_package_snapshot({"scope": "riser-zone"}, version),
        bc.intake_field_verification({"observation_id": "OBS-1", "deviation_type": "geometry", "evidence": ("photo-1",)}),
        bc.govern_temporary_works_model({"expiry_date": "2026-06-30", "review_cadence_days": 7}, as_of="2026-05-30"),
        bc.reconcile_as_built(({"asset_id": "AHU-1", "location": "L1"},), ({"asset_id": "AHU-1", "location": "L1"},)),
        bc.score_handover_readiness({"building": "B"}, assets, (), ({"asset_id": "AHU-1", "approved": True},)),
        bc.validate_om_document_links(({"asset_id": "AHU-1", "purpose": "manual", "approved": True},), assets),
        bc.track_commissioning_prerequisites(assets),
        bc.gate_digital_twin_activation({"link_id": "DT-1"}, {"approved_asset_identifiers": True, "stable_spatial_hierarchy": True, "accepted_handover_data": True, "verified_event_mappings": True}),
        bc.evaluate_quantity_change_thresholds(({"category": "steel", "delta_percent": 12},), {"steel": 10}),
        bc.enforce_naming_classification_policy(({"name": "A-WALL-001", "classification": "wall"},), {"accepted_prefixes": ("A-",), "accepted_classes": ("wall",)}),
        bc.normalize_units_measurements(({"value": 2500, "unit": "mm"},), {"length": "m"}),
        bc.calculate_model_health_score({"clash_severity": 0.1, "quantity_variance": 0.1, "missing_classifications": 0.0, "site_findings": 0.0, "handover_completeness": 1.0, "policy_exceptions": 0.0}),
        bc.build_external_event_boundary(),
        bc.handle_incoming_policy_kpi_event({"event_type": "OperationalKpiChanged", "idempotency_key": "kpi-1"}, ({"record_id": "V1"},)),
        bc.build_heavy_model_api_boundary(),
        bc.generate_release_evidence_bundle({"model_versions": ("V1",), "drawings": ("A-101",), "issues": ("I1",), "approvals": ("APP",), "quantities": ("Q1",), "handover_checks": ("H1",)}),
        bc.evaluate_continuous_bim_controls(({"assertion_id": "A1", "status": "pass"},)),
        bc.summarize_clash_triage(({"issue_id": "C1", "trade_pair": "M/E", "level": "L1", "root_cause": "riser"},)),
        bc.detect_handover_gaps({"facility": True, "floor": True, "space": True, "system": True, "component": True, "type": True, "contact": True, "spares": True, "warranty": True, "maintenance": True}, assets),
        bc.build_revision_impact_brief({"version_id": "V1", "spaces": 10}, {"version_id": "V2", "spaces": 12}),
        bc.build_federation_operations_workbench(({"federation_id": "FED-1", "status": "active", "health_score": 91, "blockers": ()},)),
        bc.build_issue_triage_workbench(({"issue_id": "C1", "level": "L1", "status": "open"},), {"level": "L1"}),
        bc.build_asset_handover_workbench(assets, ({"package_id": "H1", "documents": ({"asset_id": "AHU-1", "approved": True},)},)),
        bc.build_approval_evidence_workbench({"revision_delta": True, "unresolved_issues": (), "quantity_changes": (), "control_assertions": True, "required_approvers": ("bim_manager",), "release_bundle": "B1"}),
        bc.classify_exception_service_levels(({"exception_id": "E1", "class": "coordination_critical", "opened_date": "2026-05-29"},), as_of="2026-05-30"),
        bc.enforce_project_tenant_isolation({"tenant": "t1", "project_id": "P1"}, {"tenant": "t1", "project_id": "P1"}),
        bc.register_handover_schema_extension({"field_name": "criticality", "asset_classes": ("ahu",), "validation_rule": "required", "migration_history": ("v1",), "export_compatibility": True, "table": "building_information_modeling_ops_asset_object"}),
        bc.trace_carbon_sustainability(({"metric_id": "C1", "model_version_id": "V1", "quantity_snapshot_id": "Q1", "asset_id": "AHU-1"},)),
        bc.check_construction_sequence_readiness({"package_id": "WP1", "predecessor_complete": True, "access_zone_clear": True, "temporary_works_ready": True, "trade_window_confirmed": True}),
        bc.govern_archive_supersession({"record_id": "V1", "superseded_by": "V2", "approved_date": "2026-05-30"}),
        bc.build_operational_kpi_pack({"federation_health": 95, "blocking_clash_burn_down": 4, "asset_data_completeness": 98, "handover_readiness": 92, "approval_latency": 2, "revision_churn": 1, "release_rework_rate": 0.02}),
    ]

    assert len(bc.BIM_CONTROL_CAPABILITIES) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(bc.BIM_CONTROL_CAPABILITIES)
    assert results[1]["coordinate_ok"] is True
    assert results[7]["duplicate_reduction"] == 1
    assert results[26]["activation_allowed"] is True
    assert results[34]["release_ready"] is True
    assert results[49]["release_confidence"] == "high"


def test_bim_runtime_ui_service_routes_and_release_evidence_surface_controls():
    service = BuildingInformationModelingOpsService()
    configured = service.configure_runtime({"database_backend": "postgresql", "event_topic": runtime.BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC})
    baseline = service.configure_project_coordinates(
        {
            "tenant": "tenant-a",
            "coordinate_basis": "grid-a",
            "survey_point": {"x": 1000, "y": 2000, "z": 15},
            "project_base_point": {"x": 995, "y": 1995, "z": 15},
            "true_north_degrees": 12.0,
            "elevation_datum": "msl",
            "unit_scale": 1.0,
        }
    )
    package = service.register_model_package(
        {
            "tenant": "tenant-a",
            "model_id": "MODEL-A",
            "version_id": "VER-A1",
            "discipline": "architectural",
            "authoring_party": "Studio",
            "coordinate_basis": "grid-a",
            "survey_point": {"x": 1000, "y": 2000, "z": 15},
            "project_base_point": {"x": 995, "y": 1995, "z": 15},
            "true_north_degrees": 12.0,
            "elevation_datum": "msl",
            "unit_scale": 1.0,
            "issue_purpose": "shared",
            "spatial_coverage": ("tower-a",),
            "lod_target": "LOD-300",
            "approval_state": "approved",
            "checksum": "sha256:ver-a1",
        }
    )
    route = routes.dispatch_route("POST /federations/model-packages", {"version_id": "VER-A1"})
    release = runtime.building_information_modeling_ops_build_release_evidence()
    ui_contract = ui.building_information_modeling_ops_ui_contract()
    boundary = runtime.building_information_modeling_ops_verify_owned_table_boundary(("building_information_modeling_ops_bim_model", "project_table"))

    assert configured["ok"] is True
    assert baseline["ok"] is True
    assert package["ok"] is True
    assert route["ok"] is True
    assert runtime.BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert boundary["ok"] is False
    assert ui_contract["stream_engine_picker_visible"] is False
    assert len(ui_contract["bim_control_panels"]) == 50
    assert release["generated_artifacts"]["improve1_bim_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_bim_control" and check["ok"] for check in release["checks"])


def test_bim_release_readiness_and_runtime_smoke_include_control_contract():
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    smoke = runtime.building_information_modeling_ops_runtime_smoke()
    capabilities = runtime.building_information_modeling_ops_runtime_capabilities()
    contract = bc.improve1_bim_control_contract()

    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert capabilities["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["shared_table_access"] is False
    assert contract["stream_engine_picker_visible"] is False
