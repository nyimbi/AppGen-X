from pyAppGen.pbcs.field_service_management import implementation_contract, field_service_management_runtime_capabilities, field_service_management_runtime_smoke, field_service_management_build_schema_contract, field_service_management_build_service_contract, field_service_management_build_release_evidence, field_service_management_receive_event, field_service_management_ui_contract, field_service_management_verify_owned_table_boundary, field_service_management_configure_runtime, field_service_management_set_parameter, field_service_management_register_rule
from pyAppGen.pbcs.field_service_management import field_service_management_advanced_field_operations_smoke, field_service_management_assign_by_skill_location_and_tools, field_service_management_optimize_service_route, field_service_management_plan_mobile_task_dependencies, field_service_management_track_technician_location, field_service_management_validate_job_tool_requirements, field_service_management_workforce_capability_contract


def test_field_service_management_runtime_capabilities_and_smoke():
    runtime = field_service_management_runtime_capabilities()
    smoke = field_service_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'field_service_management'


def test_field_service_management_contracts_events_workbench_and_boundary():
    assert field_service_management_build_schema_contract()['ok'] is True
    assert field_service_management_build_service_contract()['ok'] is True
    assert field_service_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'field_service_management'
    assert field_service_management_receive_event(field_service_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.field_service_management.events'})['state'], {'event_type': ('ServiceTicketOpened', 'InventoryPositionUpdated', 'CustomerUpdated')[0], 'event_id': 'evt'})['ok'] is True
    assert field_service_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert field_service_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert field_service_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.field_service_management.events'})['ok'] is True
    assert field_service_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert field_service_management_register_rule(state, {'rule_id':'r1'})['ok'] is True


def test_field_service_management_tracks_routes_tasks_tools_and_skill_assignment():
    contract = field_service_management_workforce_capability_contract()
    runtime = field_service_management_runtime_capabilities()
    release = field_service_management_build_release_evidence()
    ui = field_service_management_ui_contract()
    schema = field_service_management_build_schema_contract()
    service = field_service_management_build_service_contract()

    assert contract['tracks_live_technician_location'] is True
    assert contract['supports_route_optimization'] is True
    assert contract['supports_task_dependency_planning'] is True
    assert contract['supports_job_tool_requirements'] is True
    assert contract['supports_skill_based_assignment'] is True
    assert set(contract['owned_tables']) <= set(schema['owned_tables'])
    assert set(contract['operations']) <= set(runtime['operations'])
    assert set(contract['operations']) <= set(service['command_methods'])
    assert release['ok'] is True
    assert release['workforce_capability_contract']['ok'] is True
    assert {'live_workforce_map', 'route_optimizer', 'skill_assignment_console', 'job_tool_requirement_planner', 'task_dependency_board'} <= set(ui['advanced_panels'])

    location_without_consent = field_service_management_track_technician_location({}, {'technician_id': 'tech-1', 'lat': 1, 'lon': 2})
    assert location_without_consent['ok'] is False
    assert location_without_consent['reason'] == 'location_privacy_consent_required'

    location = field_service_management_track_technician_location({}, {'technician_id': 'tech-1', 'lat': -1.2921, 'lon': 36.8219, 'privacy_consent': True})
    assert location['ok'] is True
    route = field_service_management_optimize_service_route(location['state'], {'route_id': 'route-1', 'stops': ({'stop_id': 'wo-1', 'priority': 1, 'lat': -1.30, 'lon': 36.83, 'window_start': '09:00', 'window_end': '10:00'},)})
    assert route['ok'] is True
    assert route['route']['route_legs']
    tasks = field_service_management_plan_mobile_task_dependencies(route['state'], {'work_order_id': 'wo-1', 'tasks': ({'task_id': 'isolate-power'}, {'task_id': 'replace-part', 'depends_on': ('isolate-power',)})})
    assert tasks['ok'] is True
    tools = field_service_management_validate_job_tool_requirements(tasks['state'], {'work_order_id': 'wo-1', 'required_tools': ({'tool_type': 'multimeter', 'calibrated': True},), 'available_tools': ({'tool_type': 'multimeter', 'calibrated': True},)})
    assert tools['ok'] is True
    assignment = field_service_management_assign_by_skill_location_and_tools(tools['state'], {'work_order_id': 'wo-1', 'job_location': {'lat': -1.30, 'lon': 36.83}, 'required_skills': ('hvac',), 'required_tools': ('multimeter',), 'candidates': ({'technician_id': 'tech-1', 'skills': ('hvac',), 'tools': ('multimeter',), 'availability': 'available', 'location': {'lat': -1.2921, 'lon': 36.8219}}, {'technician_id': 'tech-2', 'skills': (), 'tools': (), 'availability': 'busy', 'location': {'lat': 0, 'lon': 0}})})
    assert assignment['ok'] is True
    assert assignment['assignment']['recommended_assignment']['technician_id'] == 'tech-1'
    assert field_service_management_advanced_field_operations_smoke()['ok'] is True
