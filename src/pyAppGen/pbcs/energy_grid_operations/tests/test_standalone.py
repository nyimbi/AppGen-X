"""Standalone app tests for the energy_grid_operations package."""

from __future__ import annotations

import unittest

from pyAppGen.pbcs.energy_grid_operations.routes import dispatch_standalone_route
from pyAppGen.pbcs.energy_grid_operations.standalone import EnergyGridOperationsStandaloneApp
from pyAppGen.pbcs.energy_grid_operations.standalone import smoke_test, standalone_app_manifest
from pyAppGen.pbcs.energy_grid_operations.ui import energy_grid_operations_standalone_app_contract


class EnergyGridOperationsStandaloneTests(unittest.TestCase):
    def test_standalone_manifest_and_smoke(self):
        contract = energy_grid_operations_standalone_app_contract()
        manifest = standalone_app_manifest()
        app_smoke = smoke_test()
        self.assertTrue(contract["ok"])
        self.assertTrue(manifest["ok"])
        self.assertTrue(app_smoke["ok"])
        self.assertTrue(contract["forms"])
        self.assertTrue(contract["wizards"])
        self.assertTrue(contract["controls"])

    def test_standalone_app_can_bootstrap_and_render(self):
        app = EnergyGridOperationsStandaloneApp()
        app.load_demo_workspace(tenant="tenant_standalone")
        rendered = app.render_workbench(tenant="tenant_standalone")
        self.assertTrue(rendered["ok"])
        self.assertGreaterEqual(rendered["workbench"]["cards"][0]["value"], 1)
        self.assertEqual(rendered["shell"]["app_id"], "energy_grid_operations_one_pbc_app")

    def test_policy_change_marks_existing_work_for_review(self):
        tenant = "tenant_policy"
        app = EnergyGridOperationsStandaloneApp()
        app.load_demo_workspace(tenant=tenant)
        result = dispatch_standalone_route(
            "POST",
            "/api/pbc/energy_grid_operations/events/inbox",
            {
                "envelope": {
                    "event_type": "PolicyChanged",
                    "event_id": f"policy-{tenant}",
                    "payload": {"tenant": tenant, "policy_version": "grid-policy-2026.07"},
                }
            },
            service=app.service,
        )
        self.assertTrue(result["ok"])
        switching = app.state["records"]["switching_order"][f"switch_{tenant}"]
        self.assertTrue(switching["review_required"])


if __name__ == "__main__":
    unittest.main()
