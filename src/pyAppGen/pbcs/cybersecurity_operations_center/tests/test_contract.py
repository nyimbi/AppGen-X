import unittest

from pyAppGen.pbcs.cybersecurity_operations_center import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    smoke_test,
    validate_package_metadata,
)
from pyAppGen.pbcs.cybersecurity_operations_center.agent import (
    agent_skill_manifest,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
    handoff_packet_plan,
)
from pyAppGen.pbcs.cybersecurity_operations_center.config import governance_smoke_test
from pyAppGen.pbcs.cybersecurity_operations_center.events import event_contract_manifest, validate_event_contract
from pyAppGen.pbcs.cybersecurity_operations_center.handlers import dispatch_event, handler_manifest
from pyAppGen.pbcs.cybersecurity_operations_center.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.cybersecurity_operations_center.routes import api_route_contracts, validate_api_route_contracts
from pyAppGen.pbcs.cybersecurity_operations_center.schema_contract import build_schema_contract
from pyAppGen.pbcs.cybersecurity_operations_center.service_contract import build_service_contract
from pyAppGen.pbcs.cybersecurity_operations_center.services import service_operation_contracts


class ContractSuite(unittest.TestCase):
    def test_generated_schema_service_and_release_evidence(self) -> None:
        schema = build_schema_contract()
        release = build_release_evidence()
        self.assertTrue(schema["ok"])
        self.assertTrue(build_service_contract()["ok"])
        self.assertTrue(release["ok"])
        self.assertTrue(any(check["id"] == "pbc_source_artifact_contract" for check in release["checks"]))
        self.assertTrue(release_readiness_manifest()["ok"])
        self.assertTrue(validate_release_evidence()["ok"])

    def test_manifest_and_event_contract(self) -> None:
        contract = implementation_contract()
        self.assertEqual(contract["pbc"], "cybersecurity_operations_center")
        self.assertTrue(event_contract_manifest()["ok"])
        self.assertTrue(validate_event_contract()["ok"])
        self.assertTrue(contract["boundary_contract"]["ok"])

    def test_agent_chatbot_skills_are_executable(self) -> None:
        self.assertTrue(agent_skill_manifest()["ok"])
        self.assertTrue(chatbot_interface_contract()["ok"])
        self.assertTrue(document_instruction_plan("alert evidence", "promote incident")["ok"])
        self.assertTrue(datastore_crud_plan("create")["ok"])
        self.assertFalse(datastore_crud_plan("update", table="foreign_table")["ok"])
        self.assertTrue(handoff_packet_plan()["ok"])
        self.assertTrue(composed_agent_contribution()["ok"])

    def test_registration_plan_is_side_effect_free(self) -> None:
        self.assertEqual(package_metadata_manifest()["pbc"], "cybersecurity_operations_center")
        self.assertTrue(validate_package_metadata()["ok"])
        discovery = package_discovery_plan()
        self.assertTrue(discovery["ok"])
        self.assertEqual(discovery["side_effects"], ())

    def test_service_and_route_surface_are_executable(self) -> None:
        self.assertTrue(service_operation_contracts()["ok"])
        self.assertTrue(api_route_contracts()["ok"])
        self.assertTrue(validate_api_route_contracts()["ok"])
        self.assertEqual(service_operation_contracts()["operation_contract"]["operation_kind"], "command")

    def test_configuration_permissions_and_seed_hooks_are_executable(self) -> None:
        self.assertTrue(governance_smoke_test()["ok"])

    def test_event_handlers_are_idempotent_and_retryable(self) -> None:
        manifest = handler_manifest()
        self.assertTrue(manifest["ok"])
        first = dispatch_event(
            {
                "event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0],
                "idempotency_key": "idem-cybersecurity_operations_center",
                "payload": {"dedup_window_hours": 4},
            }
        )
        duplicate = dispatch_event(
            {
                "event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0],
                "idempotency_key": "idem-cybersecurity_operations_center",
                "payload": {"dedup_window_hours": 4},
            },
            state=first["state"],
        )
        failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-cybersecurity_operations_center"})
        self.assertTrue(first["ok"])
        self.assertTrue(duplicate["duplicate"])
        self.assertTrue(failed["dead_letter_table"].endswith("dead_letter_event"))

    def test_package_smoke_is_executable(self) -> None:
        self.assertTrue(smoke_test()["ok"])


if __name__ == "__main__":
    unittest.main()
