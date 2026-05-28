import unittest

from pyAppGen.pbcs.cybersecurity_operations_center.routes import dispatch_route
from pyAppGen.pbcs.cybersecurity_operations_center.runtime import (
    cybersecurity_operations_center_build_case_detail,
    cybersecurity_operations_center_build_workbench_view,
    cybersecurity_operations_center_empty_state,
    cybersecurity_operations_center_generate_handoff_packet,
)
from pyAppGen.pbcs.cybersecurity_operations_center.services import CybersecurityOperationsCenterService


def _create_service_with_alert() -> tuple[CybersecurityOperationsCenterService, str]:
    service = CybersecurityOperationsCenterService(cybersecurity_operations_center_empty_state())
    created = service.command_security_alert(
        {
            "tenant": "tenant-test",
            "severity": "critical",
            "confidence": 0.91,
            "asset_ref": "srv-critical-01",
            "principal_ref": "alice",
            "indicator_value": "198.51.100.4",
            "actor": "sensor",
            "detection_context": {
                "source_event_id": "evt-test-1",
                "detection_timestamp": "2026-05-29T00:00:00+00:00",
                "detection_rule_id": "sigma-1",
                "evidence_checksum": "sha256:test-1",
            },
        }
    )
    alert_id = created["result"]["created"][0]["id"]
    return service, alert_id


class WorkflowSuite(unittest.TestCase):
    def test_alert_lifecycle_and_deduplication_flow(self) -> None:
        service, alert_id = _create_service_with_alert()
        duplicate = service.command_security_alert(
            {
                "tenant": "tenant-test",
                "severity": "critical",
                "confidence": 0.93,
                "asset_ref": "srv-critical-01",
                "principal_ref": "alice",
                "indicator_value": "198.51.100.4",
                "actor": "sensor",
                "detection_context": {
                    "source_event_id": "evt-test-2",
                    "detection_timestamp": "2026-05-29T00:30:00+00:00",
                    "detection_rule_id": "sigma-1",
                    "evidence_checksum": "sha256:test-1",
                },
            }
        )
        enriched = service.enrich_security_alert(alert_id, {"asset_criticality": "critical", "prior_incident_links": ["INC-123"]}, "analyst")
        triaged = service.transition_alert(alert_id, "triaged", "analyst", "Validated malicious activity")
        self.assertTrue(duplicate["result"]["duplicates"])
        self.assertEqual(enriched["result"]["record"]["status"], "enriched")
        self.assertEqual(triaged["result"]["record"]["status"], "triaged")

    def test_incident_evidence_and_workbench_projection(self) -> None:
        service, alert_id = _create_service_with_alert()
        service.transition_alert(alert_id, "triaged", "analyst", "Ready for escalation")
        incident = service.record_security_incident(
            {
                "tenant": "tenant-test",
                "alert_ids": [alert_id],
                "asset_criticality": "critical",
                "containment_required": True,
                "commander": "lead",
                "actor": "analyst",
            }
        )
        incident_id = incident["result"]["record"]["id"]
        evidence = service.record_response_evidence(
            {
                "tenant": "tenant-test",
                "case_id": incident_id,
                "source_system": "edr",
                "storage_reference": "vault://tenant-test/evidence-1",
                "actor": "analyst",
            }
        )
        containment = service.create_containment_action(
            {
                "tenant": "tenant-test",
                "incident_id": incident_id,
                "action_type": "host_isolation",
                "approved_by": "supervisor",
                "actor": "analyst",
            }
        )
        workbench = cybersecurity_operations_center_build_workbench_view(service.state, tenant="tenant-test")
        detail = cybersecurity_operations_center_build_case_detail(service.state, incident_id)
        packet = cybersecurity_operations_center_generate_handoff_packet(service.state, tenant="tenant-test")
        self.assertEqual(evidence["result"]["record"]["case_id"], incident_id)
        self.assertEqual(containment["result"]["record"]["approval_path"], "supervisor_approval")
        self.assertEqual(workbench["metrics"]["incident_counts"]["open"], 1)
        self.assertTrue(detail["relationship_graph"]["edges"])
        self.assertTrue(packet["packet"]["pending_evidence"])

    def test_route_dispatch_supports_command_and_query_paths(self) -> None:
        service, alert_id = _create_service_with_alert()
        triage = dispatch_route(
            "POST /security-alerts/triage",
            {"alert_id": alert_id, "next_status": "triaged", "actor": "analyst", "reason": "Validated"},
            service=service,
        )
        workbench = dispatch_route(
            "GET /cybersecurity-operations-center-workbench",
            {"tenant": "tenant-test"},
            service=service,
        )
        self.assertTrue(triage["ok"])
        self.assertTrue(workbench["ok"])
        self.assertTrue(workbench["result"]["result"]["route"].endswith("cybersecurity_operations_center"))


if __name__ == "__main__":
    unittest.main()
