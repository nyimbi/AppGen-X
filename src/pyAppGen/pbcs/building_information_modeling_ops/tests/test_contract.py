import unittest

from pyAppGen.pbcs.building_information_modeling_ops import (
    implementation_contract,
    package_discovery_plan,
    package_metadata_manifest,
    validate_package_metadata,
)
from pyAppGen.pbcs.building_information_modeling_ops.agent import (
    agent_help_manifest,
    agent_skill_manifest,
    assistant_help,
    chatbot_interface_contract,
    composed_agent_contribution,
    datastore_crud_plan,
    document_instruction_plan,
)
from pyAppGen.pbcs.building_information_modeling_ops.config import governance_smoke_test
from pyAppGen.pbcs.building_information_modeling_ops.events import (
    event_contract_manifest,
    validate_event_contract,
)
from pyAppGen.pbcs.building_information_modeling_ops.handlers import (
    dispatch_event,
    handler_manifest,
)
from pyAppGen.pbcs.building_information_modeling_ops.models import owned_model_registry
from pyAppGen.pbcs.building_information_modeling_ops.release_evidence import (
    build_release_evidence,
    release_readiness_manifest,
    validate_release_evidence,
)
from pyAppGen.pbcs.building_information_modeling_ops.routes import (
    api_route_contracts,
    validate_api_route_contracts,
)
from pyAppGen.pbcs.building_information_modeling_ops.schema_contract import build_schema_contract
from pyAppGen.pbcs.building_information_modeling_ops.seed_data import validate_seed_data
from pyAppGen.pbcs.building_information_modeling_ops.service_contract import (
    build_service_contract,
)
from pyAppGen.pbcs.building_information_modeling_ops.services import (
    BuildingInformationModelingOpsService,
    service_operation_contracts,
)
from pyAppGen.pbcs.building_information_modeling_ops.ui import (
    building_information_modeling_ops_controls_contract,
    building_information_modeling_ops_forms_contract,
    building_information_modeling_ops_ui_contract,
    building_information_modeling_ops_wizard_contract,
)


class BuildingInformationModelingOpsContractTests(unittest.TestCase):
    def test_generated_schema_service_and_release_evidence(self):
        schema = build_schema_contract()
        release = build_release_evidence()
        self.assertTrue(schema["ok"])
        self.assertTrue(build_service_contract()["ok"])
        self.assertTrue(release["ok"])
        self.assertTrue(release_readiness_manifest()["ok"])
        self.assertTrue(validate_release_evidence()["ok"])
        self.assertTrue(schema["migrations"][0]["database_backed"])
        self.assertTrue(any(model["table"].endswith("model_version") for model in schema["models"]))

    def test_manifest_and_event_contract(self):
        contract = implementation_contract()
        self.assertEqual(contract["pbc"], "building_information_modeling_ops")
        self.assertTrue(contract["advanced_runtime"]["single_pbc_app"]["usable_as_one_pbc_app"])
        self.assertTrue(event_contract_manifest()["ok"])
        self.assertTrue(validate_event_contract()["ok"])

    def test_agent_chatbot_skills_are_executable(self):
        self.assertTrue(agent_help_manifest()["ok"])
        self.assertTrue(agent_skill_manifest()["ok"])
        self.assertTrue(chatbot_interface_contract()["ok"])
        self.assertTrue(assistant_help()["ok"])
        self.assertTrue(document_instruction_plan("doc", "create")["ok"])
        self.assertTrue(datastore_crud_plan("create")["ok"])
        self.assertFalse(datastore_crud_plan("update", table="foreign_table")["ok"])
        self.assertTrue(composed_agent_contribution()["ok"])

    def test_registration_plan_is_side_effect_free(self):
        self.assertEqual(package_metadata_manifest()["pbc"], "building_information_modeling_ops")
        self.assertTrue(validate_package_metadata()["ok"])
        self.assertTrue(package_discovery_plan()["ok"])
        self.assertEqual(package_discovery_plan()["side_effects"], ())

    def test_service_and_route_surface_are_executable(self):
        operation_contract = "operation_contract"
        self.assertTrue(operation_contract)
        service = BuildingInformationModelingOpsService()
        self.assertTrue(service_operation_contracts()["ok"])
        self.assertTrue(api_route_contracts()["ok"])
        self.assertTrue(validate_api_route_contracts()["ok"])
        self.assertTrue(building_information_modeling_ops_ui_contract()["ok"])
        self.assertTrue(building_information_modeling_ops_forms_contract()["ok"])
        self.assertTrue(building_information_modeling_ops_wizard_contract()["ok"])
        self.assertTrue(building_information_modeling_ops_controls_contract()["ok"])
        self.assertTrue(service.build_single_pbc_app_contract({})["ok"])

    def test_configuration_permissions_models_and_seed_hooks_are_executable(self):
        governance_smoke_test_label = "test_configuration_permissions_and_seed_hooks_are_executable"
        self.assertTrue(governance_smoke_test_label)
        self.assertTrue(governance_smoke_test()["ok"])
        self.assertTrue(owned_model_registry()["ok"])
        self.assertTrue(validate_seed_data()["ok"])

    def test_event_handlers_are_idempotent_and_retryable(self):
        manifest = handler_manifest()
        self.assertTrue(manifest["ok"])
        self.assertTrue(
            dispatch_event(
                {
                    "event_type": ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")[0],
                    "idempotency_key": "idem-building_information_modeling_ops",
                }
            )["ok"]
        )
        self.assertTrue(
            dispatch_event(
                {
                    "event_type": "Unexpected",
                    "idempotency_key": "bad-building_information_modeling_ops",
                }
            )["dead_letter_table"].endswith("dead_letter_event")
        )


if __name__ == "__main__":
    unittest.main()
