"""Contract and execution tests for the energy_grid_operations package."""

from __future__ import annotations

import unittest

from pyAppGen.pbcs.energy_grid_operations import implementation_contract
from pyAppGen.pbcs.energy_grid_operations import package_discovery_plan
from pyAppGen.pbcs.energy_grid_operations import package_metadata_manifest
from pyAppGen.pbcs.energy_grid_operations import validate_package_metadata
from pyAppGen.pbcs.energy_grid_operations.agent import agent_skill_manifest
from pyAppGen.pbcs.energy_grid_operations.agent import chatbot_interface_contract
from pyAppGen.pbcs.energy_grid_operations.agent import datastore_crud_plan
from pyAppGen.pbcs.energy_grid_operations.agent import document_instruction_plan
from pyAppGen.pbcs.energy_grid_operations.config import governance_smoke_test
from pyAppGen.pbcs.energy_grid_operations.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.energy_grid_operations.handlers import dispatch_event, handler_manifest, reset_handler_state
from pyAppGen.pbcs.energy_grid_operations.release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from pyAppGen.pbcs.energy_grid_operations.routes import api_route_contracts, dispatch_route, validate_api_route_contracts
from pyAppGen.pbcs.energy_grid_operations.schema_contract import build_schema_contract
from pyAppGen.pbcs.energy_grid_operations.seed_data import seed_plan, validate_seed_data
from pyAppGen.pbcs.energy_grid_operations.service_contract import build_service_contract
from pyAppGen.pbcs.energy_grid_operations.services import EnergyGridOperationsService, service_operation_contracts


class EnergyGridOperationsContractTests(unittest.TestCase):
    def test_generated_schema_service_and_release_evidence(self):
        self.assertTrue(build_schema_contract()["ok"])
        self.assertTrue(build_service_contract()["ok"])
        self.assertTrue(build_release_evidence()["ok"])
        self.assertTrue(release_readiness_manifest()["ok"])
        self.assertTrue(validate_release_evidence()["ok"])

    def test_manifest_and_event_contract(self):
        self.assertEqual(implementation_contract()["pbc"], "energy_grid_operations")
        self.assertTrue(event_contract_manifest()["ok"])
        self.assertTrue(validate_event_contract()["ok"])

    def test_agent_chatbot_skills_are_executable(self):
        self.assertTrue(agent_skill_manifest()["ok"])
        self.assertTrue(chatbot_interface_contract()["ok"])
        plan = document_instruction_plan("planned switching order", "simulate the feeder transfer")
        self.assertTrue(plan["ok"])
        self.assertIn("review_switching_order", plan["candidate_operations"])
        self.assertTrue(datastore_crud_plan("create")["ok"])
        self.assertFalse(datastore_crud_plan("update", table="foreign_table")["ok"])

    def test_registration_plan_is_side_effect_free(self):
        self.assertEqual(package_metadata_manifest()["pbc"], "energy_grid_operations")
        self.assertTrue(validate_package_metadata()["ok"])
        discovery = package_discovery_plan()
        self.assertTrue(discovery["ok"])
        self.assertEqual(discovery["side_effects"], ())

    def test_service_and_route_surface_are_executable(self):
        service = EnergyGridOperationsService()
        self.assertTrue(service_operation_contracts()["ok"])
        self.assertTrue(api_route_contracts()["ok"])
        self.assertTrue(validate_api_route_contracts()["ok"])

        created = dispatch_route(
            "POST",
            "/grid-assets",
            {
                "asset_id": "asset_contract",
                "tenant": "tenant_contract",
                "asset_type": "breaker",
                "asset_name": "Contract Breaker",
                "voltage_kv": 11,
                "substation_id": "sub_contract",
                "feeder_id": "feeder_contract",
                "normal_state": "closed",
            },
            service=service,
        )
        topology = service.execute(
            "record_grid_topology",
            {
                "topology_id": "topology_contract",
                "tenant": "tenant_contract",
                "feeder_id": "feeder_contract",
                "source_asset_id": "asset_contract",
                "energized_sections": ("section_1",),
            },
        )
        switching = dispatch_route(
            "POST",
            "/switching-orders",
            {
                "switching_order_id": "switch_contract",
                "tenant": "tenant_contract",
                "feeder_id": "feeder_contract",
                "substation_id": "sub_contract",
                "clearance_id": "clr_contract",
                "requested_by": "dispatcher",
                "steps": (
                    {"sequence": 1, "action": "open", "target": "asset_contract", "hold_point": True, "description": "Open breaker"},
                    {"sequence": 2, "action": "verify", "target": "asset_contract", "description": "Verify isolation"},
                ),
            },
            service=service,
        )
        workbench = dispatch_route("GET", "/energy-grid-operations-workbench", {"tenant": "tenant_contract"}, service=service)

        self.assertTrue(created["ok"])
        self.assertTrue(topology["ok"])
        self.assertTrue(switching["ok"])
        self.assertTrue(workbench["ok"])
        self.assertGreaterEqual(workbench["result"]["result"]["asset_count"], 1)

    def test_configuration_permissions_and_seed_hooks_are_executable(self):
        self.assertTrue(governance_smoke_test()["ok"])
        self.assertTrue(seed_plan()["ok"])
        self.assertTrue(validate_seed_data()["ok"])

    def test_event_handlers_are_idempotent_and_retryable(self):
        reset_handler_state()
        manifest = handler_manifest()
        self.assertTrue(manifest["ok"])
        first = dispatch_event({"event_type": "PolicyChanged", "event_id": "idem-energy-grid", "payload": {"tenant": "tenant_contract"}})
        second = dispatch_event({"event_type": "PolicyChanged", "event_id": "idem-energy-grid", "payload": {"tenant": "tenant_contract"}})
        failed = dispatch_event({"event_type": "Unexpected", "event_id": "bad-energy-grid", "payload": {"tenant": "tenant_contract"}})
        self.assertTrue(first["ok"])
        self.assertTrue(second["duplicate"])
        self.assertTrue(failed["dead_letter_table"].endswith("dead_letter_event"))


if __name__ == "__main__":
    unittest.main()
