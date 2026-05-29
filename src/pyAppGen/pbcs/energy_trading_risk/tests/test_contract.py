import unittest

from pyAppGen.pbcs.energy_trading_risk import implementation_contract
from pyAppGen.pbcs.energy_trading_risk import package_discovery_plan
from pyAppGen.pbcs.energy_trading_risk import package_metadata_manifest
from pyAppGen.pbcs.energy_trading_risk import validate_package_metadata
from pyAppGen.pbcs.energy_trading_risk.agent import agent_skill_manifest
from pyAppGen.pbcs.energy_trading_risk.agent import assistant_help_manifest
from pyAppGen.pbcs.energy_trading_risk.agent import chatbot_interface_contract
from pyAppGen.pbcs.energy_trading_risk.agent import datastore_crud_plan
from pyAppGen.pbcs.energy_trading_risk.agent import document_instruction_plan
from pyAppGen.pbcs.energy_trading_risk.application import EnergyTradingRiskApp
from pyAppGen.pbcs.energy_trading_risk.controls import energy_trading_risk_control_catalog
from pyAppGen.pbcs.energy_trading_risk.forms import energy_trading_risk_form_catalog
from pyAppGen.pbcs.energy_trading_risk.models import model_contracts
from pyAppGen.pbcs.energy_trading_risk.release_evidence import build_release_evidence
from pyAppGen.pbcs.energy_trading_risk.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.energy_trading_risk.release_evidence import validate_release_evidence
from pyAppGen.pbcs.energy_trading_risk.events import event_contract_manifest
from pyAppGen.pbcs.energy_trading_risk.events import validate_event_contract
from pyAppGen.pbcs.energy_trading_risk.handlers import dispatch_event
from pyAppGen.pbcs.energy_trading_risk.handlers import handler_manifest
from pyAppGen.pbcs.energy_trading_risk.routes import api_route_contracts
from pyAppGen.pbcs.energy_trading_risk.routes import validate_api_route_contracts
from pyAppGen.pbcs.energy_trading_risk.schema_contract import build_schema_contract
from pyAppGen.pbcs.energy_trading_risk.service_contract import build_service_contract
from pyAppGen.pbcs.energy_trading_risk.services import service_operation_contracts
from pyAppGen.pbcs.energy_trading_risk.ui import energy_trading_risk_single_pbc_app_ui_contract
from pyAppGen.pbcs.energy_trading_risk.wizards import energy_trading_risk_wizard_catalog


class ContractTests(unittest.TestCase):
    def test_generated_schema_service_and_release_evidence(self):
        self.assertTrue(build_schema_contract()["ok"])
        self.assertTrue(build_service_contract()["ok"])
        self.assertTrue(build_release_evidence()["ok"])
        self.assertTrue(release_readiness_manifest()["ok"])
        self.assertTrue(validate_release_evidence()["ok"])

    def test_manifest_and_event_contract(self):
        self.assertEqual(implementation_contract()["pbc"], "energy_trading_risk")
        self.assertTrue(event_contract_manifest()["ok"])
        self.assertTrue(validate_event_contract()["ok"])

    def test_app_surface_contracts_are_present(self):
        self.assertTrue(energy_trading_risk_form_catalog()["ok"])
        self.assertTrue(energy_trading_risk_wizard_catalog()["ok"])
        self.assertTrue(energy_trading_risk_control_catalog()["ok"])
        self.assertTrue(energy_trading_risk_single_pbc_app_ui_contract()["ok"])
        self.assertTrue(model_contracts()["ok"])

    def test_agent_chatbot_skills_are_executable(self):
        self.assertTrue(agent_skill_manifest()["ok"])
        self.assertTrue(assistant_help_manifest()["ok"])
        self.assertTrue(chatbot_interface_contract()["ok"])
        self.assertTrue(document_instruction_plan("doc", "create")["ok"])
        self.assertTrue(datastore_crud_plan("create")["ok"])
        self.assertFalse(datastore_crud_plan("update", table="foreign_table")["ok"])

    def test_registration_plan_is_side_effect_free(self):
        self.assertEqual(package_metadata_manifest()["pbc"], "energy_trading_risk")
        self.assertTrue(validate_package_metadata()["ok"])
        self.assertTrue(package_discovery_plan()["ok"])
        self.assertEqual(package_discovery_plan()["side_effects"], ())

    def test_service_and_route_surface_are_executable(self):
        self.assertTrue(service_operation_contracts()["ok"])
        self.assertTrue(api_route_contracts()["ok"])
        self.assertTrue(validate_api_route_contracts()["ok"])
        self.assertTrue(service_operation_contracts()["operation_contract"])

    def test_release_evidence_requires_docs_and_app_surfaces(self):
        validation = validate_release_evidence()
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["manifest"]["docs_present"]["README.md"])
        self.assertTrue(validation["manifest"]["docs_present"]["implementation-plan.md"])
        self.assertTrue(validation["manifest"]["docs_present"]["implementation-status.md"])

    def test_event_handlers_are_idempotent_and_retryable(self):
        manifest = handler_manifest()
        self.assertTrue(manifest["ok"])
        self.assertTrue(dispatch_event({"event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0], "idempotency_key": "idem-energy_trading_risk-contract"})["ok"])
        self.assertTrue(dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-energy_trading_risk-contract"})["dead_letter_table"].endswith("dead_letter_event"))

    def test_application_contract_is_executable(self):
        app = EnergyTradingRiskApp()
        try:
            contract = app.app_contract()
            self.assertTrue(contract["ok"])
            self.assertFalse(contract["database"]["shared_table_access"])
            self.assertIn("trade_capture_release", contract["wizards"]["wizard_ids"])
        finally:
            app.close()


if __name__ == "__main__":
    unittest.main()
