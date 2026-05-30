import pytest

from pyAppGen.pbcs.water_wastewater_operations import (
    water_wastewater_operations_build_release_evidence,
    water_wastewater_operations_build_workbench_view,
    water_wastewater_operations_configure_runtime,
    water_wastewater_operations_create_asset_isolation_plan,
    water_wastewater_operations_define_distribution_zone,
    water_wastewater_operations_empty_state,
    water_wastewater_operations_inspect_hydrant_asset,
    water_wastewater_operations_plan_flushing_program,
    water_wastewater_operations_project_scada_snapshot,
    water_wastewater_operations_record_lab_compliance_case,
    water_wastewater_operations_record_pressure_quality_sample,
    water_wastewater_operations_register_lift_station,
    water_wastewater_operations_register_treatment_plant,
)


def _configured_state():
    return water_wastewater_operations_configure_runtime(
        water_wastewater_operations_empty_state(),
        {'database_backend': 'postgresql', 'event_topic': 'pbc.water_wastewater_operations.events', 'retry_limit': 5},
    )['state']


def test_operational_slice_tracks_samples_lift_stations_and_scada_without_shared_tables():
    state = _configured_state()
    state = water_wastewater_operations_register_treatment_plant(
        state,
        {'tenant': 'tenant-a', 'plant_code': 'WTP-1', 'plant_name': 'North Plant', 'utility_type': 'drinking_water', 'operating_state': 'normal'},
    )['state']
    state = water_wastewater_operations_define_distribution_zone(
        state,
        {'tenant': 'tenant-a', 'zone_code': 'ZONE-1', 'zone_name': 'North Zone', 'service_population': 12000, 'critical_customers': ('hospital',)},
    )['state']
    sample = water_wastewater_operations_record_pressure_quality_sample(
        state,
        {
            'tenant': 'tenant-a',
            'sample_code': 'SAMPLE-1',
            'zone_code': 'ZONE-1',
            'sample_point': 'DP-17',
            'collected_at': '2026-05-30T06:00:00Z',
            'pressure_psi': 24,
            'disinfectant_residual_mg_l': 0.1,
            'turbidity_ntu': 1.6,
            'chain_of_custody_complete': True,
            'holding_time_ok': True,
        },
    )
    lift_station = water_wastewater_operations_register_lift_station(
        sample['state'],
        {'tenant': 'tenant-a', 'station_code': 'LS-7', 'service_area': 'North Basin', 'wet_well_level_pct': 92, 'generator_available': False},
    )
    scada = water_wastewater_operations_project_scada_snapshot(
        lift_station['state'],
        {'tenant': 'tenant-a', 'projection_code': 'SCADA-1', 'asset_code': 'LS-7', 'captured_at': '2026-05-30T06:10:00Z', 'freshness_minutes': 18, 'tags': ('wet_well_level', 'pump_a_status')},
    )
    workbench = water_wastewater_operations_build_workbench_view(scada['state'], tenant='tenant-a')

    assert sample['record']['status'] == 'action_required'
    assert 'low_pressure' in sample['record']['summary']['risk_reasons']
    assert lift_station['record']['summary']['overflow_risk'] is True
    assert scada['record']['summary']['projection_only'] is True
    assert scada['record']['summary']['historian_boundary'] == 'projection_only'
    assert workbench['command_center']['samples_requiring_action'] == 1
    assert workbench['command_center']['lift_station_overflow_risk'] == 1
    assert workbench['command_center']['stale_scada_projections'] == 1
    assert workbench['forms']
    assert workbench['wizards']
    assert workbench['controls']


def test_operational_slice_enforces_chain_of_custody_lab_and_hydrant_follow_up_rules():
    state = _configured_state()
    with pytest.raises(ValueError, match='cannot approve a sample without custody and holding-time evidence'):
        water_wastewater_operations_record_pressure_quality_sample(
            state,
            {
                'tenant': 'tenant-a',
                'sample_code': 'SAMPLE-2',
                'zone_code': 'ZONE-1',
                'sample_point': 'DP-19',
                'collected_at': '2026-05-30T07:00:00Z',
                'approval_status': 'approved',
                'chain_of_custody_complete': False,
                'holding_time_ok': True,
            },
        )

    hydrant = water_wastewater_operations_inspect_hydrant_asset(
        state,
        {'tenant': 'tenant-a', 'hydrant_code': 'HY-3', 'zone_code': 'ZONE-1', 'inspection_date': '2026-05-30', 'flow_gpm': 500, 'condition': 'painted_outlet_damage'},
    )
    flush = water_wastewater_operations_plan_flushing_program(
        hydrant['state'],
        {'tenant': 'tenant-a', 'program_code': 'FL-1', 'zone_code': 'ZONE-1', 'hydrant_codes': ('HY-3',), 'expected_flow_m3': 25.0, 'discoloration_watch': True},
    )
    lab_case = water_wastewater_operations_record_lab_compliance_case(
        flush['state'],
        {'tenant': 'tenant-a', 'case_code': 'LAB-3', 'sample_code': 'SAMPLE-3', 'parameter': 'e_coli', 'result_value': 1.0, 'limit_value': 0.0, 'holding_time_ok': True, 'chain_of_custody_complete': True},
    )

    assert hydrant['record']['status'] == 'repair_required'
    assert hydrant['record']['summary']['follow_up_required'] is True
    assert flush['record']['summary']['discoloration_watch'] is True
    assert lab_case['record']['status'] == 'non_compliant'
    assert lab_case['record']['summary']['requires_resample'] is True


def test_operational_slice_release_smoke_and_isolation_plan_cover_governed_actions():
    state = _configured_state()
    isolation = water_wastewater_operations_create_asset_isolation_plan(
        state,
        {'tenant': 'tenant-a', 'plan_code': 'ISO-9', 'asset_code': 'MAIN-44', 'valve_sequence': ('V-1', 'V-2'), 'affected_connections': 900, 'verification_complete': True},
    )
    release = water_wastewater_operations_build_release_evidence()

    assert isolation['record']['requires_human_confirmation'] is True
    assert isolation['record']['summary']['verification_complete'] is True
    assert release['ok'] is True
    assert release['control']['summary']['smoke_scenario_count'] >= 8
    assert any(scenario['operation'] == 'report_operations_incident' for scenario in release['scenarios'])
