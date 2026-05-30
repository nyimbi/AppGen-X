from pathlib import Path

from pyAppGen.pbcs.agri_supply_chain_traceability import implementation_contract
from pyAppGen.pbcs.agri_supply_chain_traceability import package_discovery_plan
from pyAppGen.pbcs.agri_supply_chain_traceability import package_metadata_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability import smoke_test
from pyAppGen.pbcs.agri_supply_chain_traceability import validate_package_metadata
from pyAppGen.pbcs.agri_supply_chain_traceability.agent import agent_skill_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.agent import chatbot_interface_contract
from pyAppGen.pbcs.agri_supply_chain_traceability.agent import composed_agent_contribution
from pyAppGen.pbcs.agri_supply_chain_traceability.agent import datastore_crud_plan
from pyAppGen.pbcs.agri_supply_chain_traceability.agent import document_instruction_plan
from pyAppGen.pbcs.agri_supply_chain_traceability.events import event_contract_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.events import validate_event_contract
from pyAppGen.pbcs.agri_supply_chain_traceability.handlers import dispatch_event
from pyAppGen.pbcs.agri_supply_chain_traceability.handlers import handler_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.models import database_model_contract
from pyAppGen.pbcs.agri_supply_chain_traceability.models import model_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.release_evidence import build_release_evidence
from pyAppGen.pbcs.agri_supply_chain_traceability.release_evidence import pbc_generation_smoke_audit
from pyAppGen.pbcs.agri_supply_chain_traceability.release_evidence import pbc_implementation_release_audit
from pyAppGen.pbcs.agri_supply_chain_traceability.release_evidence import pbc_source_artifact_contract
from pyAppGen.pbcs.agri_supply_chain_traceability.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.release_evidence import validate_release_evidence
from pyAppGen.pbcs.agri_supply_chain_traceability.routes import api_route_contracts
from pyAppGen.pbcs.agri_supply_chain_traceability.routes import validate_api_route_contracts
from pyAppGen.pbcs.agri_supply_chain_traceability.schema_contract import build_schema_contract
from pyAppGen.pbcs.agri_supply_chain_traceability.service_contract import build_service_contract
from pyAppGen.pbcs.agri_supply_chain_traceability.services import service_operation_contracts
from pyAppGen.pbcs.agri_supply_chain_traceability.standalone import standalone_app_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.ui import agri_supply_chain_traceability_standalone_app_contract


PACKAGE_DIR = Path(__file__).resolve().parent.parent


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()['ok'] is True
    assert build_service_contract()['ok'] is True
    assert build_release_evidence()['ok'] is True
    assert release_readiness_manifest()['ok'] is True
    assert validate_release_evidence()['ok'] is True


def test_manifest_event_model_and_standalone_contracts():
    contract = implementation_contract()
    assert contract['pbc'] == 'agri_supply_chain_traceability'
    assert contract['standalone_app_contract']['ok'] is True
    assert contract['standalone_app_manifest']['ok'] is True
    assert event_contract_manifest()['ok'] is True
    assert validate_event_contract()['ok'] is True
    assert model_manifest()['ok'] is True
    assert database_model_contract()['ok'] is True


def test_agent_chatbot_skills_are_executable():
    plan = document_instruction_plan('Certificate and shipping manifest', 'prepare release review')
    assert agent_skill_manifest()['ok'] is True
    assert chatbot_interface_contract()['ok'] is True
    assert composed_agent_contribution()['ok'] is True
    assert plan['ok'] is True
    assert plan['release_gate_preview']['suggested'] is True
    assert datastore_crud_plan('create')['ok'] is True
    assert datastore_crud_plan('update', table='foreign_table')['ok'] is False


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()['pbc'] == 'agri_supply_chain_traceability'
    assert validate_package_metadata()['ok'] is True
    assert package_discovery_plan()['ok'] is True
    assert package_discovery_plan()['side_effects'] == ()
    assert smoke_test()['ok'] is True


def test_service_and_route_surface_are_executable():
    routes = api_route_contracts()
    services = service_operation_contracts()
    standalone = agri_supply_chain_traceability_standalone_app_contract()
    assert services['ok'] is True
    assert routes['ok'] is True
    assert validate_api_route_contracts()['ok'] is True
    assert 'POST /api/pbc/agri_supply_chain_traceability/input-batches' in routes['routes']
    assert 'GET /api/pbc/agri_supply_chain_traceability/service-contract' in routes['routes']
    assert standalone['forms']
    assert standalone['wizards']
    assert standalone['controls']


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest['ok'] is True
    assert dispatch_event({'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'idem-agri_supply_chain_traceability'})['ok'] is True
    assert dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-agri_supply_chain_traceability'})['dead_letter_table'].endswith('dead_letter_event')


def test_repo_gate_audits_and_artifacts():
    expected = (
        'README.md',
        'SPECIFICATION.md',
        'implementation-plan.md',
        'implementation-status.md',
        'RELEASE_EVIDENCE.md',
        'standalone.py',
        'migrations/001_initial.sql',
        'tests/test_contract.py',
        'tests/test_standalone.py',
    )
    missing = tuple(path for path in expected if not (PACKAGE_DIR / path).exists())
    evidence = build_release_evidence()
    assert not missing
    assert standalone_app_manifest()['ok'] is True
    assert pbc_source_artifact_contract()['ok'] is True
    assert pbc_implementation_release_audit()['ok'] is True
    assert pbc_generation_smoke_audit()['ok'] is True
    assert evidence['repo_gate_results']['pbc_source_artifact_contract'] is True
    assert evidence['repo_gate_results']['pbc_implementation_release_audit'] is True
    assert evidence['repo_gate_results']['pbc_generation_smoke_audit'] is True
