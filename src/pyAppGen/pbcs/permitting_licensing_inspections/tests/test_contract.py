from pyAppGen.pbcs.permitting_licensing_inspections import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.permitting_licensing_inspections.agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.permitting_licensing_inspections.controls import control_contracts
from pyAppGen.pbcs.permitting_licensing_inspections.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.permitting_licensing_inspections.forms import form_contracts
from pyAppGen.pbcs.permitting_licensing_inspections.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.permitting_licensing_inspections.routes import api_route_contracts, resolve_route, validate_api_route_contracts
from pyAppGen.pbcs.permitting_licensing_inspections.schema_contract import build_schema_contract
from pyAppGen.pbcs.permitting_licensing_inspections.services import service_operation_contracts
from pyAppGen.pbcs.permitting_licensing_inspections.ui import permitting_licensing_inspections_standalone_app_contract, permitting_licensing_inspections_ui_contract
from pyAppGen.pbcs.permitting_licensing_inspections.wizards import wizard_contracts
from pyAppGen.pbcs.permitting_licensing_inspections.config import governance_smoke_test


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()['ok'] is True
    assert service_operation_contracts()['ok'] is True
    assert build_release_evidence()['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True


def test_manifest_and_event_contract():
    implementation = implementation_contract()
    assert implementation['pbc'] == 'permitting_licensing_inspections'
    assert implementation['standalone_app_contract']['app_id'].endswith('_one_pbc_app')
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    plan = document_instruction_plan('failed inspection and renewal hold', 'draft next steps')
    assert plan['ok'] is True
    assert plan['candidate_forms']
    assert datastore_crud_plan('create')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False
    assert composed_agent_contribution()['ok'] is True


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'permitting_licensing_inspections'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()


def test_service_route_and_ui_surface_are_executable():
    assert api_route_contracts()['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert resolve_route('GET', '/permitting-licensing-inspections-workbench')['handled'] is True
    assert permitting_licensing_inspections_ui_contract()['ok'] is True
    assert permitting_licensing_inspections_standalone_app_contract()['ok'] is True
    assert form_contracts()['ok'] is True
    assert wizard_contracts()['ok'] is True
    assert control_contracts()['ok'] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()['ok'] is True
