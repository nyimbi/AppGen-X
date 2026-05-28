import unittest

from pyAppGen.pbcs.capital_markets_trading_ops import implementation_contract, package_discovery_plan, package_metadata_manifest, validate_package_metadata
from pyAppGen.pbcs.capital_markets_trading_ops.schema_contract import build_schema_contract
from pyAppGen.pbcs.capital_markets_trading_ops.service_contract import build_service_contract
from pyAppGen.pbcs.capital_markets_trading_ops.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.capital_markets_trading_ops.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.capital_markets_trading_ops.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.capital_markets_trading_ops.services import service_operation_contracts
from pyAppGen.pbcs.capital_markets_trading_ops.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.capital_markets_trading_ops.config import governance_smoke_test
from pyAppGen.pbcs.capital_markets_trading_ops.agent import agent_skill_manifest, assistant_help_manifest, chatbot_interface_contract, document_instruction_plan, datastore_crud_plan
from pyAppGen.pbcs.capital_markets_trading_ops.application import CapitalMarketsTradingOpsApp
from pyAppGen.pbcs.capital_markets_trading_ops.ui import capital_markets_trading_ops_control_manifest, capital_markets_trading_ops_form_contract, capital_markets_trading_ops_single_pbc_app_ui_contract, capital_markets_trading_ops_wizard_contract


class ContractTests(unittest.TestCase):
    def test_generated_schema_service_and_release_evidence(self):
        self.assertTrue(build_schema_contract()['ok'])
        self.assertTrue(build_service_contract()['ok'])
        self.assertTrue(build_release_evidence()['ok'])
        self.assertTrue(release_readiness_manifest()['ok'])
        self.assertTrue(validate_release_evidence()['ok'])

    def test_manifest_and_event_contract(self):
        self.assertEqual(implementation_contract()['pbc'], 'capital_markets_trading_ops')
        self.assertTrue(event_contract_manifest()['ok'])
        self.assertTrue(validate_event_contract()['ok'])

    def test_agent_chatbot_skills_are_executable(self):
        self.assertTrue(agent_skill_manifest()['ok'])
        self.assertTrue(chatbot_interface_contract()['ok'])
        self.assertTrue(assistant_help_manifest()['ok'])
        self.assertTrue(document_instruction_plan('doc', 'create')['ok'])
        self.assertTrue(datastore_crud_plan('create')['ok'])
        self.assertFalse(datastore_crud_plan('update', table='foreign_table')['ok'])

    def test_registration_plan_is_side_effect_free(self):
        self.assertEqual(package_metadata_manifest()['pbc'], 'capital_markets_trading_ops')
        self.assertTrue(validate_package_metadata()['ok'])
        self.assertTrue(package_discovery_plan()['ok'])
        self.assertEqual(package_discovery_plan()['side_effects'], ())

    def test_service_and_route_surface_are_executable(self):
        self.assertTrue(service_operation_contracts()['ok'])
        self.assertTrue(api_route_contracts()['ok'])
        self.assertTrue(validate_api_route_contracts()['ok'])
        self.assertTrue(capital_markets_trading_ops_form_contract()['ok'])
        self.assertTrue(capital_markets_trading_ops_wizard_contract()['ok'])
        self.assertTrue(capital_markets_trading_ops_control_manifest()['ok'])
        self.assertTrue(capital_markets_trading_ops_single_pbc_app_ui_contract()['ok'])
        self.assertTrue(bool(service_operation_contracts()['operation_contract']))

    def test_configuration_permissions_and_seed_hooks_are_executable(self):
        self.assertTrue(governance_smoke_test()['ok'])

    def test_event_handlers_are_idempotent_and_retryable(self):
        manifest = handler_manifest()
        self.assertTrue(manifest['ok'])
        self.assertTrue(dispatch_event({'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'idem-capital_markets_trading_ops'})['ok'])
        self.assertTrue(dispatch_event({'event_type': 'Unexpected', 'idempotency_key': 'bad-capital_markets_trading_ops'})['dead_letter_table'].endswith('dead_letter_event'))

    def test_single_pbc_app_contract_is_executable(self):
        app = CapitalMarketsTradingOpsApp()
        try:
            contract = app.app_contract()
            self.assertTrue(contract['ok'])
            self.assertFalse(contract['database']['shared_table_access'])
            self.assertIn('trade_order_release_wizard', contract['app']['wizards'])
        finally:
            app.close()


if __name__ == '__main__':
    unittest.main()
