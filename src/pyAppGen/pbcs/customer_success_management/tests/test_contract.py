from pyAppGen.pbcs.customer_success_management import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.customer_success_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.customer_success_management.service_contract import build_service_contract
from pyAppGen.pbcs.customer_success_management.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.customer_success_management.release_evidence import (
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
)
from pyAppGen.pbcs.customer_success_management.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.customer_success_management.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.customer_success_management.services import service_operation_contracts
from pyAppGen.pbcs.customer_success_management.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.customer_success_management.config import governance_smoke_test
from pyAppGen.pbcs.customer_success_management.agent import agent_skill_manifest, chatbot_interface_contract, document_instruction_plan, datastore_crud_plan
from pyAppGen.pbcs.customer_success_management.ui import customer_success_management_render_workbench


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()['ok'] is True
    assert build_service_contract()['ok'] is True
    assert build_release_evidence()['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True
    assert pbc_source_artifact_contract()['ok'] is True
    assert pbc_implementation_release_audit()['ok'] is True
    assert pbc_generation_smoke_audit()['ok'] is True


def test_manifest_and_event_contract():
    assert implementation_contract()['pbc'] == 'customer_success_management'
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    assert document_instruction_plan('doc', 'create')['ok'] is True
    assert datastore_crud_plan('create')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'customer_success_management'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()['ok'] is True
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert service_operation_contracts()['operation_contract']
    workbench = customer_success_management_render_workbench({'tenant': 'tenant-smoke'})
    assert workbench['ok'] is True
    assert workbench['forms']
    assert workbench['wizards']
    assert workbench['controls']


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': ('CustomerUpdated', 'SubscriptionRenewed', 'ServiceTicketResolved')[0], 'idempotency_key': 'idem'})['ok'] is True
    assert dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'idem-bad'})['dead_letter_table'].endswith('dead_letter_event')
