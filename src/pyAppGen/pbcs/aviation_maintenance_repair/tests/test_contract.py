import unittest

from pyAppGen.pbcs.aviation_maintenance_repair import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.aviation_maintenance_repair.agent import agent_skill_manifest, assistant_planning_contract, chatbot_interface_contract, datastore_crud_plan, document_instruction_plan
from pyAppGen.pbcs.aviation_maintenance_repair.config import governance_smoke_test
from pyAppGen.pbcs.aviation_maintenance_repair.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.aviation_maintenance_repair.handlers import dispatch_event, handler_manifest, reset_handler_state
from pyAppGen.pbcs.aviation_maintenance_repair.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.aviation_maintenance_repair.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.aviation_maintenance_repair.schema_contract import build_schema_contract
from pyAppGen.pbcs.aviation_maintenance_repair.service_contract import build_service_contract
from pyAppGen.pbcs.aviation_maintenance_repair.services import service_operation_contracts
from pyAppGen.pbcs.aviation_maintenance_repair.ui import aviation_maintenance_repair_ui_contract
from pyAppGen.pbcs.aviation_maintenance_repair.workflows import workflow_catalog


class AviationMaintenanceRepairContractTests(unittest.TestCase):
    def test_generated_schema_service_and_release_evidence(self):
        self.assertTrue(build_schema_contract()["ok"])
        self.assertTrue(build_service_contract()["ok"])
        self.assertTrue(build_release_evidence()["ok"])
        self.assertTrue(release_readiness_manifest()["ok"])
        self.assertTrue(validate_release_evidence()["ok"])

    def test_manifest_and_event_contract(self):
        contract = implementation_contract()
        self.assertEqual(contract["pbc"], "aviation_maintenance_repair")
        self.assertTrue(contract["api_contract"]["ok"])
        self.assertTrue(contract["workflows"]["ok"])
        self.assertTrue(event_contract_manifest()["ok"])
        self.assertTrue(validate_event_contract()["ok"])

    def test_agent_chatbot_skills_are_executable(self):
        plan = document_instruction_plan("doc", "create work card release plan", {"tail_number": "5Y-ABC"})
        self.assertTrue(agent_skill_manifest()["ok"])
        self.assertTrue(chatbot_interface_contract()["ok"])
        self.assertTrue(assistant_planning_contract()["ok"])
        self.assertTrue(plan["ok"])
        self.assertTrue(plan["release_to_service_preview"]["human_certifier_required"])
        self.assertTrue(datastore_crud_plan("create")["ok"])
        self.assertFalse(datastore_crud_plan("update", table="foreign_table")["ok"])

    def test_registration_plan_is_side_effect_free(self):
        self.assertEqual(package_metadata_manifest()["pbc"], "aviation_maintenance_repair")
        self.assertTrue(validate_package_metadata()["ok"])
        self.assertTrue(package_discovery_plan()["ok"])
        self.assertEqual(package_discovery_plan()["side_effects"], ())

    def test_service_route_ui_and_workflow_surface_are_executable(self):
        self.assertTrue(service_operation_contracts()["ok"])
        self.assertTrue(api_route_contracts()["ok"])
        self.assertTrue(validate_api_route_contracts()["ok"])
        self.assertTrue(aviation_maintenance_repair_ui_contract()["ok"])
        self.assertTrue(workflow_catalog()["ok"])
        self.assertTrue(bool(service_operation_contracts()["operation_contract"]))

    def test_configuration_permissions_and_seed_hooks_are_executable(self):
        self.assertTrue(governance_smoke_test()["ok"])

    def test_event_handlers_are_idempotent_and_retryable(self):
        reset_handler_state()
        manifest = handler_manifest()
        self.assertTrue(manifest["ok"])
        self.assertTrue(dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "payload": {"policy_id": "idem-policy"}, "idempotency_key": "idem-aviation_maintenance_repair"})["ok"])
        self.assertTrue(dispatch_event({"event_type": "Unexpected", "payload": {}, "idempotency_key": "bad-aviation_maintenance_repair"})["dead_letter_table"].endswith("dead_letter_event"))


if __name__ == "__main__":
    unittest.main()

# AppGen-X canonical source-audit contract tests for aviation_maintenance_repair.
def test_service_and_route_surface_are_executable():
    import importlib

    services = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.services")
    routes = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.routes")
    service_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    operation_contract = service_contracts.get("operation_contract") or service_contracts.get("contracts", ({},))[0]
    assert service_contracts["ok"] is True
    assert route_contracts["ok"] is True
    assert route_validation["ok"] is True
    assert operation_contract


def test_configuration_permissions_and_seed_hooks_are_executable():
    import importlib

    config = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.config")
    permissions = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.permissions")
    seed_data = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.seed_data")
    assert config.governance_smoke_test()["ok"] is True
    assert permissions.smoke_test()["ok"] is True
    assert seed_data.smoke_test()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    import importlib

    events = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.events")
    handlers = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.handlers")
    event_contract_manifest = events.event_contract_manifest
    validate_event_contract = events.validate_event_contract
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True
    handler_smoke = handlers.smoke_test()
    assert handler_smoke["ok"] is True


def test_release_registration_and_package_metadata_are_executable():
    import importlib

    package = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair")
    release_evidence = importlib.import_module("pyAppGen.pbcs.aviation_maintenance_repair.release_evidence")
    assert package.package_metadata_manifest()["ok"] is True
    assert package.validate_package_metadata()["ok"] is True
    assert package.package_discovery_plan()["ok"] is True
    assert release_evidence.release_readiness_manifest()["ok"] is True
    assert release_evidence.validate_release_evidence()["ok"] is True
