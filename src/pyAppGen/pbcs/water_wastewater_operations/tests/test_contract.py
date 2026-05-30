from pyAppGen.pbcs.water_wastewater_operations import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.water_wastewater_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.water_wastewater_operations.service_contract import build_service_contract
from pyAppGen.pbcs.water_wastewater_operations.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.water_wastewater_operations.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.water_wastewater_operations.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.water_wastewater_operations.services import service_operation_contracts
from pyAppGen.pbcs.water_wastewater_operations.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.water_wastewater_operations.config import governance_smoke_test
from pyAppGen.pbcs.water_wastewater_operations.agent import agent_skill_manifest, chatbot_interface_contract, document_instruction_plan, datastore_crud_plan


def test_generated_schema_service_and_release_evidence():
    schema = build_schema_contract()
    release = build_release_evidence()
    assert schema['ok'] is True
    assert build_service_contract()['ok'] is True
    assert release['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True
    assert release['control']['summary']['smoke_scenario_count'] >= 8


def test_manifest_and_event_contract():
    assert implementation_contract()['pbc'] == 'water_wastewater_operations'
    event_manifest = event_contract_manifest()
    assert event_manifest['ok'] is True
    assert 'sample_collected' in event_manifest['domain_event_specializations']
    assert validate_event_contract()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    plan = document_instruction_plan('incident report', 'create governed_datastore_crud incident draft')
    assert skills['ok'] is True
    assert chatbot['ok'] is True
    assert 'governed_datastore_crud' in chatbot['capabilities']
    assert all(skill['requires_confirmation'] is True for skill in skills['skills'])
    assert plan['ok'] is True
    assert plan['requires_human_confirmation'] is True
    assert datastore_crud_plan('create')['ok'] is True
    assert datastore_crud_plan('read')['requires_confirmation'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'water_wastewater_operations'
    assert validate_package_metadata()['ok'] is True
    discovery = package_discovery_plan()
    assert discovery['ok'] is True
    assert discovery['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    service_contracts = service_operation_contracts()
    api_contracts = api_route_contracts()
    assert service_contracts['ok'] is True
    assert api_contracts['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert service_contracts['operation_contract']
    assert any(contract.get('command') == 'record_pressure_quality_sample' for contract in api_contracts['contracts'])
    assert any(contract.get('query') == 'build_release_evidence' for contract in api_contracts['contracts'])


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'idem-water_wastewater_operations'})['ok'] is True
    assert dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-water_wastewater_operations'})['dead_letter_table'].endswith('dead_letter_event')
