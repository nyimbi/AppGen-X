import unittest

from pyAppGen.pbcs.cybersecurity_operations_center.standalone import (
    CybersecurityOperationsCenterStandaloneApp,
    smoke_test,
    standalone_application_manifest,
    validate_standalone_application,
)


class StandaloneSuite(unittest.TestCase):
    def test_standalone_manifest_and_smoke(self) -> None:
        manifest = standalone_application_manifest()
        validation = validate_standalone_application()
        app_smoke = smoke_test()
        self.assertTrue(manifest["ok"])
        self.assertTrue(validation["ok"])
        self.assertTrue(app_smoke["ok"])
        self.assertTrue(manifest["ui"]["ok"])
        self.assertTrue(manifest["workflows"])

    def test_standalone_app_loads_demo_workspace(self) -> None:
        app = CybersecurityOperationsCenterStandaloneApp()
        loaded = app.load_demo_workspace(tenant="tenant-standalone")
        rendered = app.render_workbench(tenant="tenant-standalone")
        detail = app.render_case_detail(loaded["incident_id"])
        self.assertTrue(loaded["ok"])
        self.assertTrue(rendered["ok"])
        self.assertTrue(detail["ok"])
        self.assertEqual(rendered["shell"]["app_id"], "cybersecurity_operations_center_one_pbc_app")
        self.assertGreaterEqual(len(rendered["workbench"]["lanes"]["urgent"]), 1)
        self.assertEqual(detail["detail"]["case_type"], "incident")


if __name__ == "__main__":
    unittest.main()
