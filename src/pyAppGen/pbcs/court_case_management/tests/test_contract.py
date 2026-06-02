from pyAppGen.pbcs.court_case_management import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.court_case_management.agent import agent_skill_manifest, chatbot_interface_contract, document_instruction_plan, datastore_crud_plan
from pyAppGen.pbcs.court_case_management.audit import run_court_case_management_pbc_audit
from pyAppGen.pbcs.court_case_management.config import governance_smoke_test
from pyAppGen.pbcs.court_case_management.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.court_case_management.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.court_case_management.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.court_case_management.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.court_case_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.court_case_management.service_contract import build_service_contract
from pyAppGen.pbcs.court_case_management.services import service_operation_contracts, standalone_service_manifest
from pyAppGen.pbcs.court_case_management.standalone import documentation_presence, pbc_generation_smoke_audit, pbc_implementation_release_audit, pbc_source_artifact_contract, standalone_manifest, standalone_smoke_test


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()['ok'] is True
    assert build_service_contract()['ok'] is True
    evidence = build_release_evidence()
    assert evidence['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True
    assert {check['id'] for check in evidence['checks']} >= {
        'runtime_release_evidence',
        'source_artifacts',
        'implementation_audit',
        'generation_audit',
        'focused_package_audit',
    }


def test_manifest_and_event_contract():
    assert implementation_contract()['pbc'] == 'court_case_management'
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()['ok'] is True
    assert len(agent_skill_manifest()['skills']) >= 3
    assert chatbot_interface_contract()['ok'] is True
    assert document_instruction_plan('Exhibit A', 'log evidence')['ok'] is True
    assert datastore_crud_plan('create', table='court_case_management_case_task')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'court_case_management'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()['ok'] is True
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert service_operation_contracts()['operation_contract']
    assert standalone_service_manifest()['ok'] is True
    assert standalone_manifest()['ok'] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True
    assert documentation_presence()['ok'] is True
    assert pbc_source_artifact_contract()['ok'] is True
    assert pbc_implementation_release_audit()['ok'] is True
    assert pbc_generation_smoke_audit()['ok'] is True
    assert standalone_smoke_test()['ok'] is True
    assert run_court_case_management_pbc_audit()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'idem-court_case_management'})['ok'] is True
    assert dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-court_case_management'})['dead_letter_table'].endswith('dead_letter_event')
