"""Focused standalone app tests for audit_ledger."""

from pathlib import Path

from .. import agent, release_evidence, routes, services, standalone, ui
from ..repository import AuditLedgerRepository


def test_repository_persists_core_audit_flows():
    repository = AuditLedgerRepository()
    try:
        repository.configure_runtime(
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.audit.events",
                "retry_limit": 3,
                "signature_algorithm": "dilithium3_simulated",
                "allowed_classifications": ("public", "internal", "regulated"),
                "export_modes": ("proof_bundle", "forensic_archive"),
                "default_timezone": "UTC",
                "workbench_limit": 100,
            }
        )
        repository.set_parameter("retention_days", 2555)
        repository.register_rule(
            {
                "rule_id": "audit_ledger.repository_test",
                "tenant": "tenant_test",
                "scope": "release_gate",
                "classification": "regulated",
                "minimum_retention_days": 2555,
                "requires_legal_hold_review": True,
                "requires_export_approval": True,
                "severity": "blocking",
                "status": "active",
            }
        )
        received = repository.receive_event(
            {
                "event_id": "route_test",
                "event_type": "RoutePublished",
                "payload": {"tenant": "tenant_test", "route_id": "route_test", "service_id": "svc_test"},
            }
        )
        event = repository.record_audit_event(
            {
                "audit_id": "audit_test",
                "tenant": "tenant_test",
                "source_pbc": "api_gateway_mesh",
                "aggregate_id": "route_test",
                "actor": "operator",
                "action": "publish_route",
                "classification": "regulated",
                "payload": {"route_id": "route_test", "method": "POST"},
                "occurred_at": "2026-05-29T10:00:00Z",
            }
        )
        access = repository.record_access_evidence(
            {
                "evidence_id": "access_test",
                "tenant": "tenant_test",
                "principal": "operator",
                "resource": "route_test",
                "action": "publish_route",
                "decision": "allow",
                "context": {"risk": "low"},
                "policy_source": "identity_access_projection",
            }
        )
        policy = repository.define_retention_policy(
            {
                "policy_id": "retention_test",
                "tenant": "tenant_test",
                "classification": "regulated",
                "retention_days": 2555,
                "legal_hold": False,
                "disposal_action": "review",
            }
        )
        control = repository.assert_control(
            {
                "control_id": "control_test",
                "tenant": "tenant_test",
                "control": "signature_chain_complete",
                "status": "pass",
                "severity": "blocking",
                "evidence": ("audit_test",),
            }
        )
        export = repository.prepare_forensic_export(
            {
                "export_id": "export_test",
                "tenant": "tenant_test",
                "classification": "regulated",
                "requested_by": "auditor",
                "purpose": "regulator_review",
                "disclosure": ("audit_id", "actor", "action", "payload_hash"),
            }
        )
        verified = repository.verify_signature_chain(tenant="tenant_test")
        projection = repository.publish_audit_projection("audit_test", systems=("identity", "gateway"))
        workbench = repository.build_workbench(tenant="tenant_test")
        release_snapshot = repository.release_snapshot(tenant="tenant_test")
        assert all(
            item["ok"] is True
            for item in (received, event, access, policy, control, export, verified, projection, workbench, release_snapshot)
        )
        assert workbench["snapshot"]["event_count"] == 1
        assert workbench["snapshot"]["pending_export_approval_count"] == 1
        assert release_snapshot["notarization"]["chain_link_count"] == 1
    finally:
        repository.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    app = standalone.AuditLedgerStandaloneApp()
    try:
        loaded = app.load_demo_workspace(tenant="tenant_route")
        rendered = app.render_workbench(tenant="tenant_route")
        service = app.service
        summary = routes.dispatch_standalone_route(
            "GET",
            "/app/audit-ledger/summary",
            {"tenant": "tenant_route"},
            service=service,
        )
        release_route = routes.dispatch_standalone_route(
            "GET",
            "/app/audit-ledger/release-snapshot",
            {"tenant": "tenant_route"},
            service=service,
        )
        document_plan = agent.document_instruction_plan(
            "export incident packet",
            "prepare a regulator export for route publication evidence",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "audit_ledger_forensic_export",
            {"export_id": "export_route"},
        )
        ui_contract = ui.audit_ledger_ui_contract()
        evidence = release_evidence.build_release_evidence()
        assert loaded["ok"] is True
        assert rendered["ok"] is True
        assert summary["ok"] is True
        assert release_route["ok"] is True
        assert ui_contract["forms"]
        assert ui_contract["wizards"]
        assert ui_contract["controls"]
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["standalone_app"]["ok"] is True
        assert evidence["repository"]["ok"] is True
        assert evidence["documentation"]["ok"] is True
        assert standalone.smoke_test()["ok"] is True
    finally:
        app.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
