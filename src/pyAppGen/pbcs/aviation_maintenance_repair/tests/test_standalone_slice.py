import unittest

from pyAppGen.pbcs.aviation_maintenance_repair.agent import document_instruction_plan
from pyAppGen.pbcs.aviation_maintenance_repair.config import evaluate_rule
from pyAppGen.pbcs.aviation_maintenance_repair.permissions import operation_authorization
from pyAppGen.pbcs.aviation_maintenance_repair.runtime import (
    aviation_maintenance_repair_assess_release_to_service,
    aviation_maintenance_repair_empty_state,
    aviation_maintenance_repair_plan_document_instruction,
    aviation_maintenance_repair_query_workbench,
    aviation_maintenance_repair_record_aircraft,
    aviation_maintenance_repair_record_airworthiness_directive,
    aviation_maintenance_repair_record_component,
    aviation_maintenance_repair_record_deferred_defect,
    aviation_maintenance_repair_record_work_card,
)
from pyAppGen.pbcs.aviation_maintenance_repair.services import AviationMaintenanceRepairService
from pyAppGen.pbcs.aviation_maintenance_repair.workflows import build_release_to_service_workflow


class AviationMaintenanceRepairStandaloneTests(unittest.TestCase):
    def _build_ready_state(self):
        state = aviation_maintenance_repair_empty_state()
        aircraft = aviation_maintenance_repair_record_aircraft(state, {"tenant": "tenant-1", "tail_number": "5Y-ABC", "aircraft_type": "B737", "fleet_subtype": "-800"})
        component = aviation_maintenance_repair_record_component(aircraft["state"], {"tenant": "tenant-1", "component_id": "COMP-1", "serial_number": "SER-1", "remaining_hours": 120, "remaining_cycles": 80, "release_certificate": "ARC-1", "effectivity_aircraft_types": ("B737",)})
        work_card = aviation_maintenance_repair_record_work_card(component["state"], {"tenant": "tenant-1", "work_card_id": "WC-1", "status": "closed", "task_family": "line", "aircraft_type": "B737", "required_signoff_roles": ("performer", "duplicate_inspector"), "duplicate_inspection_required": True, "signoffs": ({"role": "performer", "technician_id": "tech-1"}, {"role": "duplicate_inspector", "technician_id": "tech-2"}), "controlled_tools": ({"tool_id": "tool-1", "returned": True, "calibration_due": "2026-12-31"},), "consumables": ({"batch_id": "batch-1", "expiry": "2026-12-31"},)})
        directive = aviation_maintenance_repair_record_airworthiness_directive(work_card["state"], {"tenant": "tenant-1", "ad_id": "AD-1", "status": "complied", "applicable": True})
        defect = aviation_maintenance_repair_record_deferred_defect(directive["state"], {"tenant": "tenant-1", "defect_id": "DEF-1", "status": "closed", "expiry_date": "2026-12-31"})
        return defect["state"], aircraft["record"], component["record"], work_card["record"], directive["record"], defect["record"]

    def test_runtime_release_workflow_reaches_release_ready(self):
        state, aircraft, component, work_card, directive, defect = self._build_ready_state()
        result = aviation_maintenance_repair_assess_release_to_service(
            state,
            {
                "release_id": "REL-1",
                "tail_number": aircraft["tail_number"],
                "work_card_ids": (work_card["id"],),
                "component_ids": (component["id"],),
                "deferred_defect_ids": (defect["id"],),
                "airworthiness_directive_ids": (directive["id"],),
                "technician_authorizations": (
                    {"technician_id": "tech-1", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"},
                    {"technician_id": "tech-2", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"},
                ),
                "certifier": {"technician_id": "cert-1", "release_authorization": True},
                "as_of": "2026-05-28",
            },
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["release_pack"]["status"], "release_ready")
        self.assertEqual(result["workflow"]["next_action"], "issue_release")
        self.assertEqual(result["state"]["outbox"][-1]["event_type"], "AviationMaintenanceRepairApproved")

    def test_runtime_release_workflow_blocks_expired_defect_and_missing_certifier(self):
        state = aviation_maintenance_repair_empty_state()
        aircraft = aviation_maintenance_repair_record_aircraft(state, {"tenant": "tenant-1", "tail_number": "5Y-BAD", "aircraft_type": "B737"})
        work_card = aviation_maintenance_repair_record_work_card(aircraft["state"], {"tenant": "tenant-1", "work_card_id": "WC-BAD", "status": "open", "task_family": "line", "aircraft_type": "B737", "required_signoff_roles": ("performer",), "signoffs": ({"role": "performer", "technician_id": "tech-1"},)})
        defect = aviation_maintenance_repair_record_deferred_defect(work_card["state"], {"tenant": "tenant-1", "defect_id": "DEF-BAD", "status": "deferred", "expiry_date": "2026-01-01"})
        result = aviation_maintenance_repair_assess_release_to_service(
            defect["state"],
            {
                "release_id": "REL-BAD",
                "tail_number": "5Y-BAD",
                "work_card_ids": (work_card["record"]["id"],),
                "deferred_defect_ids": (defect["record"]["id"],),
                "technician_authorizations": ({"technician_id": "tech-1", "task_family": "line", "aircraft_type": "B737", "valid_to": "2026-12-31"},),
                "as_of": "2026-05-28",
            },
        )
        self.assertFalse(result["ok"])
        self.assertTrue({item["code"] for item in result["release_pack"]["blockers"]} >= {"work_card_not_closed", "deferred_defect_expired", "human_certifier_required"})
        self.assertEqual(result["state"]["outbox"][-1]["event_type"], "AviationMaintenanceRepairExceptionOpened")

    def test_document_instruction_planning_and_workbench_surface_are_connected(self):
        state, _, _, _, _, _ = self._build_ready_state()
        plan = aviation_maintenance_repair_plan_document_instruction(state, "maintenance log", "Create component update and release signoff plan", {"tail_number": "5Y-ABC"})
        workbench = aviation_maintenance_repair_query_workbench(plan["state"])
        self.assertEqual(plan["document_plan"]["workflow"]["workflow_id"], "document_instruction_planning")
        self.assertFalse(plan["document_plan"]["release_to_service_preview"]["assistant_can_certify"])
        self.assertTrue(workbench["workbench"]["wizards"])
        self.assertTrue(workbench["instruction_queue"][0]["requires_human_confirmation"])

    def test_service_and_rule_contracts_reflect_standalone_slice(self):
        service = AviationMaintenanceRepairService()
        document_plan = service.plan_document_instruction({"document": "log", "instruction": "update work card release"})
        workflow = build_release_to_service_workflow({"aircraft": {"tail_number": "5Y-ABC", "aircraft_type": "B737"}})
        duplicate_rule = evaluate_rule("critical_tasks_require_duplicate_inspection", {"critical_task": True, "duplicate_inspection_required": True})
        permission = operation_authorization("assess_release_to_service", {"roles": ("certifier",)})
        self.assertTrue(document_plan["ok"])
        self.assertEqual(workflow["workflow_id"], "release_to_service")
        self.assertTrue(duplicate_rule["passed"])
        self.assertTrue(permission["ok"])
        self.assertTrue(document_instruction_plan("doc", "create aircraft update")["ok"])


if __name__ == "__main__":
    unittest.main()
