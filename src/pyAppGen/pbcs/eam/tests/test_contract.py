"""Generated contract smoke tests for eam."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'eam'
    assert SCHEMA_CONTRACT['ok'] is True
    assert len(SCHEMA_CONTRACT['owned_tables']) >= 16
    assert 'eam_condition_reading' in SCHEMA_CONTRACT['owned_tables']
    assert 'eam_maintenance_dead_letter' in SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert len(model_smoke['manifest']['model_tables']) == len(SCHEMA_CONTRACT['owned_tables'])
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'eam'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'eam'
    assert RELEASE_EVIDENCE['ok'] is True


    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    assert release_manifest['ok'] is True
    assert release_validation['ok'] is True
    assert release_smoke['ok'] is True
    assert not release_manifest['blocking_gaps']
    assert not release_validation['missing_sections']
    assert not release_validation['failed_checks']
    assert not release_validation['boundary_gaps']
    assert not release_manifest['side_effects']
    assert not release_validation['side_effects']
    assert not release_smoke['side_effects']


def test_manifest_and_event_contract():
    from .. import events

    assert PBC_MANIFEST['pbc'] == 'eam'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert len(PBC_MANIFEST['tables']) >= 16
    assert 'POST /maintenance-configuration' in PBC_MANIFEST['apis']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('eam_')
    assert EVENT_CONTRACT['inbox_table'].startswith('eam_')
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    smoke = events.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['stream_engine_picker_visible'] is False
    assert len(manifest['emitted']) >= 10
    assert len(manifest['consumed']) >= 5
    assert {event['event_type'] for event in manifest['emitted']} >= {'EquipmentRegistered', 'SafetyPermitApproved', 'MaintenanceCompleted'}
    assert {event['event_type'] for event in manifest['consumed']} >= {'InventoryReservationConfirmed', 'AssetLifecycleUpdated'}
    assert not validation['invalid_tables']
    assert not validation['invalid_emitted']
    assert not validation['invalid_consumed']
    assert smoke['emitted']['table'] == EVENT_CONTRACT['outbox_table']
    assert smoke['consumed']['table'] == EVENT_CONTRACT['inbox_table']
    assert smoke['emitted']['retry_policy']['max_attempts'] >= 3
    assert smoke['consumed']['dead_letter_table'].startswith(PBC_MANIFEST['pbc'] + '_')
    assert not manifest['side_effects']
    assert not validation['side_effects']
    assert not smoke['side_effects']


def test_registration_plan_is_side_effect_free():
    from .. import package_discovery_plan, package_metadata_manifest, register_pbc, registration_plan, validate_package_metadata

    assert register_pbc()['pbc'] == 'eam'
    plan = registration_plan()
    assert plan['ok'] is True
    assert plan['catalog_patch']
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()
    assert metadata['ok'] is True
    assert metadata_validation['ok'] is True
    assert discovery['ok'] is True
    assert metadata['stream_engine_picker_visible'] is False
    assert metadata['event_contract'] == 'AppGen-X'
    assert not metadata_validation['missing_entrypoints']
    assert not metadata_validation['missing_publish_artifacts']
    assert not metadata_validation['missing_capability_evidence']
    assert not metadata_validation['invalid']
    assert not discovery['side_effects']


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    operation_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke['ok'] is True
    assert operation_contracts['ok'] is True
    assert route_contracts['ok'] is True
    assert route_validation['ok'] is True
    assert len(route_contracts['contracts']) >= 13
    assert 'configure_runtime' in operation_contracts['operations']
    assert 'build_workbench_view' in operation_contracts['operations']
    assert all(item['permission'] for item in route_contracts['contracts'])
    assert all(item['event_contract'] == 'AppGen-X' for item in route_contracts['contracts'])
    assert all(item['stream_engine_picker_visible'] is False for item in route_contracts['contracts'])
    assert all(item['shared_table_access'] is False for item in route_contracts['contracts'])
    assert not route_validation['service_mismatches']
    assert not route_validation['missing_idempotency']
    assert not route_validation['invalid_table_scope']
    assert service_smoke['result']['operation_contract']['route']['path']
    assert service_smoke['result']['operation_contract']['permission']
    assert service_smoke['result']['operation_contract']['event_contract'] == 'AppGen-X'
    assert service_smoke['result']['operation_contract']['owned_tables'] or service_smoke['result']['operation_contract']['read_tables']
    assert route_smoke['ok'] is True
    assert not service_smoke['side_effects']
    assert not operation_contracts['side_effects']
    assert not route_contracts['side_effects']
    assert not route_validation['side_effects']
    assert not route_smoke['side_effects']


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    governance_smoke = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    assert config_smoke['ok'] is True
    assert governance_smoke['ok'] is True
    assert governance_smoke['parameter']['accepted'] is True
    assert governance_smoke['compiled_rule']['compiled'] is True
    assert governance_smoke['rule_decision']['allowed'] is True
    assert permission_smoke['ok'] is True
    assert seed_smoke['ok'] is True
    assert not config_smoke['side_effects']
    assert not governance_smoke['side_effects']
    assert not permission_smoke['side_effects']
    assert not seed_smoke['side_effects']


def test_ui_workbench_surface_is_executable():
    from .. import ui

    if hasattr(ui, 'smoke_test'):
        smoke = ui.smoke_test()
    else:
        contract = getattr(ui, f"{PBC_MANIFEST['pbc']}_ui_contract")()
        rendered = {
            'ok': contract['ok'],
            'cards': contract.get('panels') or contract.get('fragments'),
            'route': (contract.get('routes') or (None,))[0],
        }
        smoke = {
            'ok': contract['ok'] and bool(contract.get('fragments')) and bool(rendered['cards']),
            'manifest': {'fragments': contract.get('fragments', ())},
            'rendered': rendered,
            'side_effects': (),
        }
    assert smoke['ok'] is True
    assert smoke['manifest']['fragments']
    assert smoke['rendered']['cards']
    assert not smoke['side_effects']


def test_event_handlers_are_idempotent_and_retryable():
    from .. import handlers

    smoke = handlers.smoke_test()
    assert smoke['ok'] is True
    assert smoke['manifest']['handlers']
    assert smoke['first_result']['retry_policy']
    assert smoke['first_result']['dead_letter_table'].startswith('eam_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']

def test_table_stakes_and_advanced_capability_assurance_is_executable():
    from .. import capability_assurance

    manifest = capability_assurance.table_stakes_capability_manifest()
    validation = capability_assurance.validate_table_stakes_capability_coverage()
    smoke = capability_assurance.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['standard_features']
    assert manifest['advanced_capabilities']
    assert not validation['missing_standard']
    assert not validation['missing_advanced']
    assert not validation['missing_operations']
    assert not validation['uncovered_features']
    assert not validation['invalid_tables']
    assert not validation['invalid_backends']
    assert validation['stream_picker_visible'] is False
    assert validation['event_contract'] == 'AppGen-X'
    assert validation['boundary_rejection']['ok'] is False
    assert validation['boundary_rejection']['violations']
    assert not smoke['side_effects']


def test_standalone_eam_lifecycle_proof():
    from .. import agent, runtime

    state = runtime.eam_empty_state()
    state = runtime.eam_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.maintenance.events",
            "retry_limit": 3,
            "allowed_sites": ("plant_east", "plant_west"),
            "allowed_priorities": ("low", "medium", "high", "critical"),
            "allowed_work_types": ("preventive", "predictive", "corrective", "calibration"),
            "allowed_permit_types": ("electrical", "confined_space", "hot_work"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    for key, value in (
        ("default_pm_interval_days", 30),
        ("failure_risk_threshold", 0.65),
        ("mttr_target_hours", 6),
        ("criticality_weight", 0.4),
        ("safety_risk_threshold", 0.7),
        ("retention_days", 365),
    ):
        state = runtime.eam_set_parameter(state, key, value)["state"]
    state = runtime.eam_register_rule(
        state,
        {
            "rule_id": "eam.asset_readiness_gate",
            "tenant": "tenant_alpha",
            "rule_type": "maintenance",
            "eligible_work_types": ("preventive", "predictive", "corrective"),
            "allowed_sites": ("plant_east", "plant_west"),
            "status": "active",
            "criticality_classes": ("A", "B", "C"),
        },
    )["state"]
    equipment_result = runtime.eam_register_equipment(
        state,
        {
            "tenant": "tenant_alpha",
            "equipment_id": "pump_001",
            "site": "plant_east",
            "asset_tag": "P-1001",
            "criticality": "A",
            "location": "Area-1",
            "parent_equipment_id": None,
            "warranty_until": "2027-12-31",
        },
    )
    assert equipment_result["ok"] is True
    state = equipment_result["state"]
    plan_result = runtime.eam_create_maintenance_plan(
        state,
        {
            "tenant": "tenant_alpha",
            "plan_id": "pm_001",
            "equipment_id": "pump_001",
            "strategy": "preventive",
            "interval_days": 30,
            "meter_threshold": 100.0,
            "condition_threshold": 0.6,
            "status": "released",
        },
    )
    assert plan_result["ok"] is True
    state = plan_result["state"]
    state = runtime.eam_record_condition_reading(
        state,
        {
            "tenant": "tenant_alpha",
            "reading_id": "cond_001",
            "equipment_id": "pump_001",
            "sensor": "vibration",
            "value": 0.58,
            "unit": "ips",
        },
    )["state"]
    meter_result = runtime.eam_record_meter_reading(
        state,
        {
            "tenant": "tenant_alpha",
            "meter_id": "meter_001",
            "equipment_id": "pump_001",
            "meter_name": "runtime_hours",
            "value": 120.0,
            "unit": "hours",
        },
    )
    assert meter_result["meter_reading"]["triggered_plans"] == ("pm_001",)
    state = meter_result["state"]
    permit_result = runtime.eam_create_safety_permit(
        state,
        {
            "tenant": "tenant_alpha",
            "permit_id": "permit_001",
            "equipment_id": "pump_001",
            "permit_type": "electrical",
            "risk_score": 0.4,
            "approved_by": "supervisor_1",
        },
    )
    assert permit_result["ok"] is True
    state = permit_result["state"]
    work_order_result = runtime.eam_create_work_order(
        state,
        {
            "tenant": "tenant_alpha",
            "work_order_id": "wo_001",
            "equipment_id": "pump_001",
            "plan_id": "pm_001",
            "work_type": "preventive",
            "priority": "critical",
            "permit_id": "permit_001",
        },
    )
    assert work_order_result["ok"] is True
    state = work_order_result["state"]
    state = runtime.eam_schedule_work_order(
        state,
        "wo_001",
        window={"start": "2026-06-01T08:00:00Z", "end": "2026-06-01T12:00:00Z"},
        technician="tech_01",
    )["state"]
    state = runtime.eam_issue_spare_part(
        state,
        {
            "tenant": "tenant_alpha",
            "usage_id": "usage_001",
            "work_order_id": "wo_001",
            "part_number": "BRG-100",
            "quantity": 2,
            "unit_cost": 45.5,
        },
    )["state"]
    receive_event = runtime.eam_receive_event(
        state,
        {
            "event_type": "InventoryReservationConfirmed",
            "event_id": "evt_inv_001",
            "tenant": "tenant_alpha",
            "payload": {"reservation_id": "res_001", "work_order_id": "wo_001", "quantity": 2},
        },
    )
    assert receive_event["ok"] is True
    state = receive_event["state"]
    complete_result = runtime.eam_complete_work_order(
        state,
        "wo_001",
        completed_by="tech_01",
        actual_hours=3.5,
        downtime_hours=1.25,
        resolution="Bearing replaced and aligned",
    )
    assert complete_result["ok"] is True
    state = complete_result["state"]

    control_result = runtime.eam_run_control_tests(state)
    proof = runtime.eam_generate_compliance_proof(state, "wo_001", disclosure=("status", "completed_by", "resolution"))
    workbench = runtime.eam_build_workbench_view(state, tenant="tenant_alpha")
    mutation_plan = agent.governed_mutation_plan("complete_work_order", {"work_order_id": "wo_001"})
    document_plan = agent.document_instruction_plan("equipment pump_001 permit packet", "complete corrective work with permit and spare evidence")

    assert control_result["ok"] is True
    assert proof["ok"] is True
    assert proof["public_claims"]["status"] == "completed"
    assert workbench["completed_work_order_count"] == 1
    assert workbench["critical_work_order_count"] == 1
    assert workbench["spare_usage_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["binding_evidence"]["shared_table_access"] is False
    assert mutation_plan["ok"] is True
    assert mutation_plan["expected_event"] == "MaintenanceCompleted"
    assert document_plan["ok"] is True
    assert "equipment" in document_plan["detected_terms"]
    assert receive_event["projection"] == "inventory_spares_projection"
    assert [event["event_type"] for event in state["events"]] == [
        "EquipmentRegistered",
        "MaintenancePlanReleased",
        "ConditionReadingRecorded",
        "MeterReadingRecorded",
        "SafetyPermitApproved",
        "WorkOrderCreated",
        "WorkOrderScheduled",
        "SparePartUsed",
        "MaintenanceCompleted",
    ]
