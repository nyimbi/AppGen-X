from pyAppGen.pbcs.rail_operations_management import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.rail_operations_management.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.rail_operations_management.config import governance_smoke_test
from pyAppGen.pbcs.rail_operations_management.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.rail_operations_management.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.rail_operations_management.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.rail_operations_management.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.rail_operations_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.rail_operations_management.service_contract import build_service_contract
from pyAppGen.pbcs.rail_operations_management.services import service_operation_contracts
from pyAppGen.pbcs.rail_operations_management.standalone import standalone_app_manifest
from pyAppGen.pbcs.rail_operations_management.runtime import (
    rail_operations_management_build_workbench_view,
    rail_operations_management_empty_state,
    rail_operations_management_runtime_smoke,
    rail_operations_management_run_advanced_assessment,
    rail_operations_management_verify_owned_table_boundary,
)


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    assert schema['ok'] is True
    assert len(schema['tables']) >= 24
    assert build_service_contract()['ok'] is True
    assert build_release_evidence()['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract['pbc'] == 'rail_operations_management'
    assert contract['standalone_app']['app_id'] == 'rail_operations_management_one_pbc_app'
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True
    assert 'TrainPlanValidated' in contract['emits']


def test_agent_chatbot_skills_are_executable():
    parsed = document_instruction_plan(
        'Dispatch bulletin: revise train ROM-1001 path, assign crew relief at JCT, and update passenger plan.',
        'Create preview for dispatch, crew, and passenger recovery changes',
    )
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    assert parsed['ok'] is True
    assert 'rail_operations_management_train_plan' in parsed['candidate_tables']
    assert datastore_crud_plan('create')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'rail_operations_management'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    contracts = service_operation_contracts()
    routes = api_route_contracts()
    assert contracts['ok'] is True
    assert len(contracts['command_operations']) >= 20
    assert routes['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert standalone_app_manifest()['ok'] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': 'PolicyChanged', 'idempotency_key': 'idem-rail_operations_management'})['ok'] is True
    assert dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-rail_operations_management'})['dead_letter_table'].endswith('dead_letter_event')


def test_runtime_smoke_and_boundary_validation_are_executable():
    smoke = rail_operations_management_runtime_smoke()
    assert smoke['ok'] is True
    assert smoke['assessment']['recommendations']
    assert rail_operations_management_verify_owned_table_boundary(('rail_operations_management_train_plan', 'foreign_table'))['ok'] is False


def test_empty_workbench_and_advanced_assessment_are_available():
    state = rail_operations_management_empty_state()
    workbench = rail_operations_management_build_workbench_view(state, tenant='default')
    assessment = rail_operations_management_run_advanced_assessment(state, {'tenant': 'default'})
    assert workbench['ok'] is True
    assert len(workbench['summary_cards']) == 4
    assert assessment['ok'] is True
    assert assessment['score'] <= 1.0
