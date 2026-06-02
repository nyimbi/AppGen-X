"""Focused unittest coverage for the enterprise_pim standalone surface."""

from __future__ import annotations

import unittest

from pyAppGen.pbcs.enterprise_pim import release_evidence
from pyAppGen.pbcs.enterprise_pim import seed_data
from pyAppGen.pbcs.enterprise_pim.standalone import create_standalone_app


class EnterprisePimStandaloneTests(unittest.TestCase):
    def test_bootstrap_and_workbench_are_executable(self):
        app = create_standalone_app()
        state = app.state_snapshot()

        self.assertEqual(state["product_taxonomy"]["tax_demo_pumps"]["status"], "ready")
        self.assertTrue(state["outbox"])

        workbench = app.dispatch_route("GET", "/api/pbc/enterprise_pim/pim-workbench", {"tenant": "tenant_demo"})
        self.assertTrue(workbench["ok"])
        self.assertTrue(workbench["result"]["workbench"]["ok"])

        ui_manifest = app.describe_ui()
        self.assertTrue(ui_manifest["forms"])
        self.assertTrue(ui_manifest["wizards"])
        self.assertTrue(ui_manifest["controls"])

    def test_permission_gate_blocks_and_allows_route_dispatch(self):
        app = create_standalone_app(seed_demo=False)
        payload = {
            "taxonomy_id": "tax_route_test",
            "tenant": "tenant_demo",
            "code": "route/test",
            "name": "Route Test",
            "parent_id": None,
            "localized_names": {"en-US": "Route Test"},
        }

        blocked = app.dispatch_route(
            "POST",
            "/api/pbc/enterprise_pim/product-taxonomies",
            payload,
            granted_permissions=(),
        )
        self.assertFalse(blocked["ok"])
        self.assertEqual(blocked["reason"], "forbidden")

        allowed = app.dispatch_route(
            "POST",
            "/api/pbc/enterprise_pim/product-taxonomies",
            payload,
            granted_permissions=("enterprise_pim.taxonomy",),
        )
        self.assertTrue(allowed["ok"])
        self.assertEqual(allowed["result"]["taxonomy"]["taxonomy_id"], "tax_route_test")

    def test_release_evidence_and_seed_bundle_are_valid(self):
        seed_validation = seed_data.validate_seed_data()
        release_validation = release_evidence.validate_release_evidence()

        self.assertTrue(seed_validation["ok"])
        self.assertTrue(release_validation["ok"])
        self.assertFalse(release_validation["missing_sections"])
        self.assertFalse(release_validation["failed_checks"])
        self.assertFalse(release_validation["boundary_gaps"])

    def test_agent_document_and_crud_planning_are_available(self):
        app = create_standalone_app()

        document_plan = app.document_plan("industrial pumps", "summarize and prepare update")
        read_plan = app.crud_plan("read")
        create_plan = app.crud_plan("create", table="enterprise_pim_product_taxonomy", payload={"status": "draft"})

        self.assertTrue(document_plan["ok"])
        self.assertTrue(read_plan["ok"])
        self.assertTrue(create_plan["ok"])
        self.assertTrue(create_plan["requires_confirmation"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
