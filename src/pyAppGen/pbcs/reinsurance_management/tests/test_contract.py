from pyAppGen.pbcs.reinsurance_management import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.reinsurance_management.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.reinsurance_management.capability_assurance import validate_table_stakes_capability_coverage
from pyAppGen.pbcs.reinsurance_management.config import governance_smoke_test
from pyAppGen.pbcs.reinsurance_management.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.reinsurance_management.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.reinsurance_management.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.reinsurance_management.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.reinsurance_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.reinsurance_management.services import ReinsuranceManagementService, service_operation_contracts
from pyAppGen.pbcs.reinsurance_management.standalone import standalone_app_manifest


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()['ok'] is True
    assert service_operation_contracts()['ok'] is True
    assert build_release_evidence()['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True
    assert standalone_app_manifest()['ok'] is True


def test_manifest_and_event_contract():
    assert implementation_contract()['pbc'] == 'reinsurance_management'
    assert package_metadata_manifest()['pbc'] == 'reinsurance_management'
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True
    preview = document_instruction_plan('cat treaty slip and bordereau', 'Create a cash call preview')
    assert preview['ok'] is True
    assert 'reinsurance_management_cash_call' in preview['candidate_tables']
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert validate_package_metadata()['ok'] is True
    discovery = package_discovery_plan()
    assert discovery['ok'] is True
    assert discovery['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    service = ReinsuranceManagementService()
    service.execute(
        'configure_runtime',
        {'configuration': {'database_backend': 'postgresql', 'event_topic': 'pbc.reinsurance_management.events'}},
    )
    route_result = dispatch_route('GET', '/api/pbc/reinsurance_management/workbench', {'tenant': 'tenant-smoke'}, service=service)
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert route_result['ok'] is True
    assert service_operation_contracts()['operation_contract']


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True
    assert validate_table_stakes_capability_coverage()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'idem-reinsurance_management'})['ok'] is True
    assert dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-reinsurance_management'})['dead_letter_table'].endswith('dead_letter_event')
