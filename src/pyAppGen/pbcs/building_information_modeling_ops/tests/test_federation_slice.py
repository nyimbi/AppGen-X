import sqlite3
import unittest
from pathlib import Path

from pyAppGen.pbcs.building_information_modeling_ops.release_evidence import build_release_evidence
from pyAppGen.pbcs.building_information_modeling_ops.runtime import (
    building_information_modeling_ops_build_federation_release_evidence,
    building_information_modeling_ops_empty_state,
)
from pyAppGen.pbcs.building_information_modeling_ops.services import BuildingInformationModelingOpsService
from pyAppGen.pbcs.building_information_modeling_ops.ui import building_information_modeling_ops_ui_contract


def _baseline_payload():
    return {
        "tenant": "tenant-a",
        "coordinate_basis": "project-grid-a",
        "survey_point": {"x": 1000, "y": 2000, "z": 15},
        "project_base_point": {"x": 995, "y": 1995, "z": 15},
        "true_north_degrees": 12.0,
        "elevation_datum": "msl",
        "unit_scale": 1.0,
    }


def _package_payload(version_id: str, **overrides):
    payload = {
        "tenant": "tenant-a",
        "model_id": f"MODEL-{version_id}",
        "version_id": version_id,
        "discipline": "architectural",
        "authoring_party": "Design Studio",
        "coordinate_basis": "project-grid-a",
        "survey_point": {"x": 1005, "y": 2002, "z": 15},
        "project_base_point": {"x": 997, "y": 1997, "z": 15},
        "true_north_degrees": 12.1,
        "elevation_datum": "msl",
        "unit_scale": 1.0,
        "issue_purpose": "shared",
        "spatial_coverage": ("tower-a", "levels-01-05"),
        "lod_target": "LOD-300",
        "approval_state": "approved",
        "checksum": f"sha256:{version_id}",
    }
    payload.update(overrides)
    return payload


class BuildingInformationModelingOpsFederationTests(unittest.TestCase):
    def test_coordinate_validation_marks_misaligned_package_blocked(self):
        service = BuildingInformationModelingOpsService()
        service.configure_runtime(
            {
                "database_backend": "postgresql",
                "event_topic": "pbc.building_information_modeling_ops.events",
            }
        )
        service.configure_project_coordinates(_baseline_payload())

        result = service.register_model_package(
            _package_payload("VER-BAD", survey_point={"x": 1100, "y": 2002, "z": 15})
        )

        self.assertTrue(result["ok"])
        self.assertFalse(result["package"]["coordinate_validation"]["ok"])
        self.assertIn(
            "survey_point_out_of_tolerance",
            result["package"]["federation_eligibility"]["blockers"],
        )

    def test_issue_purpose_and_approval_gates_block_federation_assembly(self):
        service = BuildingInformationModelingOpsService()
        service.configure_runtime(
            {
                "database_backend": "postgresql",
                "event_topic": "pbc.building_information_modeling_ops.events",
            }
        )
        service.configure_project_coordinates(_baseline_payload())
        service.register_model_package(
            _package_payload("VER-WIP", issue_purpose="wip", approval_state="approved")
        )

        federation = service.assemble_federation(
            {
                "tenant": "tenant-a",
                "federation_id": "FED-BLOCKED",
                "version_ids": ("VER-WIP",),
                "intended_use": "coordination",
            }
        )

        self.assertFalse(federation["ok"])
        self.assertEqual(federation["reason"], "federation_blocked")
        self.assertIn("VER-WIP:issue_purpose_not_publishable", federation["blockers"])

    def test_service_builds_active_federation_and_release_evidence(self):
        service = BuildingInformationModelingOpsService()
        service.configure_runtime(
            {
                "database_backend": "postgresql",
                "event_topic": "pbc.building_information_modeling_ops.events",
            }
        )
        service.configure_project_coordinates(_baseline_payload())
        service.register_model_package(_package_payload("VER-A1", discipline="architectural"))
        service.register_model_package(_package_payload("VER-S1", discipline="structural"))

        federation = service.assemble_federation(
            {
                "tenant": "tenant-a",
                "federation_id": "FED-01",
                "version_ids": ("VER-A1", "VER-S1"),
                "intended_use": "coordination",
            }
        )
        evidence = service.build_federation_release_evidence({"federation_id": "FED-01"})
        workbench = service.query_workbench({})

        self.assertTrue(federation["ok"])
        self.assertTrue(evidence["ok"])
        self.assertTrue(evidence["validation_summary"]["all_approved"])
        self.assertEqual(
            {item["discipline"] for item in evidence["contributors"]},
            {"architectural", "structural"},
        )
        self.assertEqual(workbench["workbench"]["kpis"]["active_federations"], 1)

    def test_policy_change_event_revalidates_existing_packages(self):
        service = BuildingInformationModelingOpsService()
        service.configure_runtime(
            {
                "database_backend": "postgresql",
                "event_topic": "pbc.building_information_modeling_ops.events",
            }
        )
        service.configure_project_coordinates(_baseline_payload())
        service.register_model_package(
            _package_payload("VER-A1", survey_point={"x": 1020, "y": 2000, "z": 15})
        )

        received = service.receive_event(
            {
                "event_type": "PolicyChanged",
                "idempotency_key": "policy-tighten",
                "payload": {"coordinate_tolerance_mm": 10.0},
            }
        )
        workbench = service.query_workbench({})

        self.assertTrue(received["ok"])
        self.assertEqual(received["trace"]["result"], "policy_revalidated")
        self.assertEqual(workbench["workbench"]["blocked_packages"][0]["version_id"], "VER-A1")

    def test_migration_sql_executes_and_creates_owned_tables(self):
        migration_path = Path(__file__).resolve().parent.parent / "migrations" / "001_initial.sql"
        sql = migration_path.read_text()
        connection = sqlite3.connect(":memory:")
        try:
            connection.executescript(sql)
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
        finally:
            connection.close()

        self.assertIn("building_information_modeling_ops_model_version", tables)
        self.assertIn(
            "building_information_modeling_ops_building_information_modeling_ops_governed_model",
            tables,
        )
        self.assertIn("building_information_modeling_ops_appgen_outbox_event", tables)

    def test_single_pbc_app_surfaces_and_release_bundle_are_explicit(self):
        ui = building_information_modeling_ops_ui_contract()
        release = build_release_evidence()
        state = building_information_modeling_ops_empty_state()
        unknown = building_information_modeling_ops_build_federation_release_evidence(
            state, "missing"
        )

        self.assertTrue(ui["ok"])
        self.assertGreaterEqual(len(ui["forms"]), 3)
        self.assertGreaterEqual(len(ui["wizards"]), 2)
        self.assertGreaterEqual(len(ui["controls"]), 4)
        self.assertTrue(
            release["generated_artifacts"]["single_pbc_app"]["usable_as_one_pbc_app"]
        )
        self.assertFalse(unknown["ok"])


if __name__ == "__main__":
    unittest.main()
