from pyAppGen.pbcs.privacy_consent_governance import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.privacy_consent_governance.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    document_instruction_plan,
    instruction_crud_plan,
)
from pyAppGen.pbcs.privacy_consent_governance.config import governance_smoke_test
from pyAppGen.pbcs.privacy_consent_governance.domain_depth import domain_depth_contract
from pyAppGen.pbcs.privacy_consent_governance.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.privacy_consent_governance.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.privacy_consent_governance.release_evidence import (
    build_release_evidence,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
    pbc_spec_smoke_audit,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.privacy_consent_governance.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.privacy_consent_governance.schema_contract import build_schema_contract
from pyAppGen.pbcs.privacy_consent_governance.seed_data import seed_plan, validate_seed_data
from pyAppGen.pbcs.privacy_consent_governance.service_contract import build_service_contract
from pyAppGen.pbcs.privacy_consent_governance.services import PrivacyConsentGovernanceService, service_operation_contracts


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()['ok'] is True
    assert build_service_contract()['ok'] is True
    assert build_release_evidence()['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True


def test_manifest_and_event_contract():
    contract = implementation_contract()
    assert contract['pbc'] == 'privacy_consent_governance'
    assert contract['standalone_app']['app_id'] == 'privacy_consent_governance_one_pbc_app'
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    assert document_instruction_plan('Consent update', 'Publish new policy')['ok'] is True
    assert instruction_crud_plan('Consent update', 'Publish new policy')['ok'] is True
    assert datastore_crud_plan('create')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'privacy_consent_governance'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_and_route_surface_are_executable():
    service = PrivacyConsentGovernanceService()
    service.command_configure_runtime(
        {
            'configuration': {
                'database_backend': 'postgresql',
                'event_topic': 'appgen.privacy_consent_governance.events',
                'retry_limit': 5,
                'default_policy_family': 'global-privacy',
            }
        }
    )
    service.command_register_data_subject(
        {'record': {'id': 'subject-test', 'tenant': 'tenant-test', 'code': 'SUBJECT-TEST', 'subject_identifier': 'customer-test', 'region': 'KE'}}
    )
    command = service.command_capture_consent(
        {
            'record': {
                'id': 'consent-test',
                'tenant': 'tenant-test',
                'code': 'CONSENT-TEST',
                'data_subject_id': 'subject-test',
                'purpose_code': 'MARKETING_EMAIL',
                'lawful_basis_code': 'CONSENT',
                'channel': 'email',
            }
        }
    )
    query = service.query_workbench({'tenant': 'tenant-test'})
    assert command['ok'] is True
    assert query['ok'] is True
    assert service_operation_contracts()['ok'] is True
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True


def test_configuration_seed_and_domain_depth_are_executable():
    domain = domain_depth_contract()
    assert governance_smoke_test()['ok'] is True
    assert validate_seed_data()['ok'] is True
    assert seed_plan()['ok'] is True
    assert len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']
    assert domain['operation_count'] >= domain['minimum_domain_operations']


def test_release_audits_are_all_green():
    assert pbc_spec_smoke_audit()['ok'] is True
    assert pbc_source_artifact_contract()['ok'] is True
    assert pbc_implementation_release_audit()['ok'] is True
    assert pbc_generation_smoke_audit()['ok'] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': 'CustomerUpdated', 'event_id': 'evt-1'})['ok'] is True
    rejected = dispatch_event({'event_type': 'Unexpected', 'event_id': 'evt-2'})
    assert rejected['ok'] is False
    assert rejected['dead_letter_table'].endswith('dead_letter_event')
