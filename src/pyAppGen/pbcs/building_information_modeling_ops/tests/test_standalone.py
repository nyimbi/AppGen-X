import unittest

from pyAppGen.pbcs.building_information_modeling_ops.config import compile_rule
from pyAppGen.pbcs.building_information_modeling_ops.standalone import (
    BuildingInformationModelingOpsStandaloneApp,
    smoke_test,
    standalone_app_manifest,
)


class BuildingInformationModelingOpsStandaloneTests(unittest.TestCase):
    def test_standalone_app_bootstraps_and_exposes_workbench(self):
        app = BuildingInformationModelingOpsStandaloneApp()

        loaded = app.load_demo_workspace()
        rendered = app.render_workbench()

        self.assertTrue(loaded["ok"])
        self.assertTrue(rendered["ok"])
        self.assertEqual(rendered["workbench"]["kpis"]["active_federations"], 1)
        self.assertEqual(len(rendered["workbench"]["active_federations"]), 1)

    def test_assistant_planning_and_release_snapshot_are_available(self):
        app = BuildingInformationModelingOpsStandaloneApp()
        app.load_demo_workspace()

        document_plan = app.plan_document_instruction(
            "Shared coordination issue.",
            "Create a coordination release summary.",
            actor={"id": "operator-1"},
        )
        crud_plan = app.plan_datastore_crud(
            "create",
            table="building_information_modeling_ops_model_version",
            payload={"version_id": "VER-A2"},
            actor={"id": "operator-1"},
        )
        release = app.release_snapshot()

        self.assertTrue(document_plan["ok"])
        self.assertEqual(document_plan["authorization"]["permission"], "building_information_modeling_ops.create")
        self.assertTrue(crud_plan["ok"])
        self.assertTrue(crud_plan["authorization"]["ok"])
        self.assertTrue(release["ok"])

    def test_rule_compilation_is_deterministic_and_manifest_is_standalone_ready(self):
        first = compile_rule({"rule_id": "demo", "scope": "release"})
        second = compile_rule({"scope": "release", "rule_id": "demo"})
        manifest = standalone_app_manifest()
        smoke = smoke_test()

        self.assertEqual(first["compiled_hash"], second["compiled_hash"])
        self.assertTrue(manifest["ok"])
        self.assertTrue(manifest["assistant"]["document_instruction_planning"])
        self.assertTrue(smoke["ok"])


if __name__ == "__main__":
    unittest.main()
