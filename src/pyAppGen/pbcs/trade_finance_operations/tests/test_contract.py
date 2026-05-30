from pyAppGen.pbcs.trade_finance_operations import implementation_contract
from pyAppGen.pbcs.trade_finance_operations import package_discovery_plan
from pyAppGen.pbcs.trade_finance_operations import package_metadata_manifest
from pyAppGen.pbcs.trade_finance_operations import validate_package_metadata
from pyAppGen.pbcs.trade_finance_operations.agent import agent_skill_manifest
from pyAppGen.pbcs.trade_finance_operations.agent import chatbot_interface_contract
from pyAppGen.pbcs.trade_finance_operations.agent import composed_agent_contribution
from pyAppGen.pbcs.trade_finance_operations.agent import datastore_crud_plan
from pyAppGen.pbcs.trade_finance_operations.agent import document_instruction_plan
from pyAppGen.pbcs.trade_finance_operations.capability_assurance import smoke_test as capability_assurance_smoke
from pyAppGen.pbcs.trade_finance_operations.capability_assurance import table_stakes_capability_manifest
from pyAppGen.pbcs.trade_finance_operations.capability_assurance import validate_table_stakes_capability_coverage
from pyAppGen.pbcs.trade_finance_operations.config import governance_smoke_test
from pyAppGen.pbcs.trade_finance_operations.controls import smoke_test as control_smoke_test
from pyAppGen.pbcs.trade_finance_operations.events import event_contract_manifest
from pyAppGen.pbcs.trade_finance_operations.events import validate_event_contract
from pyAppGen.pbcs.trade_finance_operations.forms import smoke_test as form_smoke_test
from pyAppGen.pbcs.trade_finance_operations.handlers import dispatch_event
from pyAppGen.pbcs.trade_finance_operations.handlers import handler_manifest
from pyAppGen.pbcs.trade_finance_operations.release_evidence import build_release_evidence
from pyAppGen.pbcs.trade_finance_operations.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.trade_finance_operations.release_evidence import validate_release_evidence
from pyAppGen.pbcs.trade_finance_operations.routes import api_route_contracts
from pyAppGen.pbcs.trade_finance_operations.routes import standalone_route_contracts
from pyAppGen.pbcs.trade_finance_operations.routes import validate_api_route_contracts
from pyAppGen.pbcs.trade_finance_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.trade_finance_operations.service_contract import build_service_contract
from pyAppGen.pbcs.trade_finance_operations.services import service_operation_contracts
from pyAppGen.pbcs.trade_finance_operations.ui import smoke_test as ui_smoke_test
from pyAppGen.pbcs.trade_finance_operations.wizards import smoke_test as wizard_smoke_test


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    manifest = implementation_contract()
    events = event_contract_manifest()
    validation = validate_event_contract()
    assert manifest["pbc"] == "trade_finance_operations"
    assert events["ok"] is True
    assert validation["ok"] is True
    assert events["stream_engine_picker_visible"] is False
    assert "TradeFinanceSwiftEvidenceCreated" in events["emitted"]


def test_agent_chatbot_skills_are_executable():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    assert document_instruction_plan("doc", "create") ["ok"] is True
    assert datastore_crud_plan("create")["ok"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False
    assert composed_agent_contribution()["ok"] is True


def test_registration_plan_is_side_effect_free():
    metadata = package_metadata_manifest()
    assert metadata["pbc"] == "trade_finance_operations"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()
    assert metadata["stream_engine_picker_visible"] is False
    assert metadata["event_contract"] == "AppGen-X"


def test_service_and_route_surface_are_executable():
    services = service_operation_contracts()
    routes = api_route_contracts()
    standalone = standalone_route_contracts()
    assert services["ok"] is True
    assert routes["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    assert services["operation_contract"]
    assert standalone["ok"] is True
    assert len(routes["contracts"]) >= 10


def test_configuration_permissions_and_seed_hooks_are_executable():
    smoke = governance_smoke_test()
    assert smoke["ok"] is True
    assert smoke["parameter"]["accepted"] is True
    assert smoke["compiled_rule"]["compiled"] is True
    assert smoke["rule_decision"]["allowed"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-trade_finance_operations"})["ok"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-trade_finance_operations"})["dead_letter_table"].endswith("dead_letter_event")


def test_ui_forms_wizards_controls_and_capability_assurance_are_executable():
    assert form_smoke_test()["ok"] is True
    assert wizard_smoke_test()["ok"] is True
    assert control_smoke_test()["ok"] is True
    assert ui_smoke_test()["ok"] is True
    manifest = table_stakes_capability_manifest()
    validation = validate_table_stakes_capability_coverage()
    assert manifest["ok"] is True
    assert validation["ok"] is True
    assert capability_assurance_smoke()["ok"] is True
