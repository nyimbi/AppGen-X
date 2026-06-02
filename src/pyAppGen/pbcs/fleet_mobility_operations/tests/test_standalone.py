from pyAppGen.pbcs.fleet_mobility_operations.controls import evaluate_control
from pyAppGen.pbcs.fleet_mobility_operations.forms import form_catalog
from pyAppGen.pbcs.fleet_mobility_operations.release_evidence import validate_release_evidence
from pyAppGen.pbcs.fleet_mobility_operations.standalone import FleetMobilityOperationsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.fleet_mobility_operations.ui import fleet_mobility_operations_standalone_ui_contract
from pyAppGen.pbcs.fleet_mobility_operations.wizards import wizard_catalog


def test_standalone_app_runs_dispatch_to_incident_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['demo']['blocked_assignment']['ok'] is False
    assert smoke['demo']['duplicate_telematics']['ok'] is False
    assert smoke['demo']['reprojection']['emitted_event'] == 'FleetRouteReprojected'
    assert smoke['demo']['incident']['incident']['state'] == 'contained'


def test_forms_wizards_controls_surface_fleet_domain():
    assert len(form_catalog()['forms']) >= 7
    assert len(wizard_catalog()['wizards']) >= 6
    assert fleet_mobility_operations_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('dispatch_readiness_control', {'failures': ('dispatch',)})
    assert blocked['ok'] is False
    assert 'dispatch' in blocked['blocked_actions']


def test_agent_replan_preview_stays_owned_and_confirmation_gated():
    app = FleetMobilityOperationsStandaloneApp()
    preview = app.assistant_replan_preview('breakdown memo', 'update route priority')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'fleet_mobility_operations_route_plan'
    assert preview['requires_confirmation'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('fleet_mobility_operations_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    assert validate_release_evidence()['ok'] is True
