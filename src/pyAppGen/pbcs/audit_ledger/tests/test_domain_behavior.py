"""Executable domain behavior coverage for the Audit Ledger PBC."""

from .. import agent, routes, runtime, ui
from ..services import AuditLedgerStandaloneService


TENANT = "tenant_behavior"


def _configuration(retry_limit=3):
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
        "retry_limit": retry_limit,
        "signature_algorithm": "dilithium3_simulated",
        "allowed_classifications": ("public", "internal", "regulated"),
        "export_modes": ("proof_bundle", "forensic_archive"),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _configure(service):
    configured = service.configure_runtime({"configuration": _configuration()})
    assert configured["ok"] is True
    for name, value in (
        ("retention_days", 2555),
        ("export_batch_limit", 1000),
        ("tamper_risk_threshold", 0.35),
        ("control_failure_threshold", 0.2),
        ("proof_disclosure_limit", 4),
    ):
        assert service.set_parameter({"name": name, "value": value})["ok"] is True
    assert service.register_rule(
        {
            "rule": {
                "rule_id": "audit_ledger.behavior.release_gate",
                "tenant": TENANT,
                "scope": "release_gate",
                "classification": "regulated",
                "minimum_retention_days": 2555,
                "requires_legal_hold_review": True,
                "requires_export_approval": True,
                "severity": "blocking",
                "status": "active",
            }
        }
    )["ok"] is True


def _populate(service):
    assert service.receive_event(
        {
            "envelope": {
                "event_id": "route_behavior",
                "event_type": "RoutePublished",
                "idempotency_key": "route:behavior",
                "payload": {
                    "tenant": TENANT,
                    "route_id": "route_behavior",
                    "service_id": "svc_behavior",
                },
            }
        }
    )["ok"] is True
    duplicate = service.receive_event(
        {
            "envelope": {
                "event_id": "route_behavior",
                "event_type": "RoutePublished",
                "idempotency_key": "route:behavior",
                "payload": {
                    "tenant": TENANT,
                    "route_id": "route_behavior",
                    "service_id": "svc_behavior",
                },
            }
        }
    )
    assert duplicate["ok"] is True
    assert duplicate["result"]["duplicate"] is True
    event = service.record_audit_event(
        {
            "audit_event": {
                "audit_id": "audit_behavior",
                "tenant": TENANT,
                "source_pbc": "api_gateway_mesh",
                "aggregate_id": "route_behavior",
                "actor": "ops_user",
                "action": "publish_route",
                "classification": "regulated",
                "payload": {"route_id": "route_behavior", "method": "POST"},
                "occurred_at": "2026-05-29T10:00:00Z",
            }
        }
    )
    assert event["ok"] is True
    assert event["result"]["audit_event"]["sealed"] is True
    assert service.record_access_evidence(
        {
            "evidence": {
                "evidence_id": "access_behavior",
                "tenant": TENANT,
                "principal": "ops_user",
                "resource": "route_behavior",
                "action": "publish_route",
                "decision": "allow",
                "context": {"risk": "low", "session": "session_behavior"},
                "policy_source": "identity_access_projection",
            }
        }
    )["ok"] is True
    assert service.define_retention_policy(
        {
            "policy": {
                "policy_id": "retention_behavior",
                "tenant": TENANT,
                "classification": "regulated",
                "retention_days": 2555,
                "legal_hold": False,
                "disposal_action": "review",
            }
        }
    )["ok"] is True
    assert service.assert_control(
        {
            "assertion": {
                "control_id": "control_behavior",
                "tenant": TENANT,
                "control": "signature_chain_complete",
                "status": "pass",
                "severity": "blocking",
                "evidence": ("audit_behavior",),
            }
        }
    )["ok"] is True
    export = service.prepare_forensic_export(
        {
            "export": {
                "export_id": "export_behavior",
                "tenant": TENANT,
                "classification": "regulated",
                "requested_by": "auditor",
                "purpose": "regulator_review",
                "disclosure": ("audit_id", "actor", "action", "payload_hash"),
            }
        }
    )
    assert export["ok"] is True
    assert export["result"]["export"]["approval_required"] is True
    assert service.verify_signature_chain({"tenant": TENANT})["ok"] is True
    projection = service.publish_audit_projection(
        {"audit_id": "audit_behavior", "systems": ("identity", "gateway", "schema", "workflow", "composition")}
    )
    assert projection["ok"] is True
    assert projection["result"]["handoffs"] == (
        "identity_audit_projection",
        "gateway_audit_projection",
        "schema_audit_projection",
        "workflow_audit_projection",
        "composition_audit_projection",
    )


def test_standalone_app_covers_audit_lifecycle_ui_agent_and_release_evidence():
    service = AuditLedgerStandaloneService()
    try:
        _configure(service)
        _populate(service)
        state = service.repository.load_state()
        workbench = service.build_workbench({"tenant": TENANT})
        summary = service.ledger_summary({"tenant": TENANT})
        release = service.release_snapshot({"tenant": TENANT})
        route_summary = routes.dispatch_standalone_route(
            "GET", "/app/audit-ledger/summary", {"tenant": TENANT}, service=service
        )
        rendered = ui.audit_ledger_render_standalone_app(
            state,
            tenant=TENANT,
            principal_permissions=(
                "audit_ledger.read",
                "audit_ledger.seal",
                "audit_ledger.verify",
                "audit_ledger.export",
                "audit_ledger.publish",
                "audit_ledger.event",
                "audit_ledger.configure",
                "audit_ledger.audit",
            ),
        )
        document_plan = agent.document_instruction_plan(
            "Regulator asks for the evidence package for route_behavior.",
            "Prepare a minimized forensic export and explain the retained evidence.",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "audit_ledger_forensic_export",
            {"export_id": "export_behavior"},
        )
        assert workbench["ok"] is True
        assert workbench["result"]["snapshot"]["event_count"] == 1
        assert workbench["result"]["snapshot"]["access_evidence_count"] == 1
        assert workbench["result"]["snapshot"]["export_count"] == 1
        assert workbench["result"]["snapshot"]["pending_export_approval_count"] == 1
        assert summary["result"]["outbox_count"] >= 4
        assert release["ok"] is True
        assert release["result"]["notarization"]["boundary_ok"] is True
        assert route_summary["ok"] is True
        assert rendered["ok"] is True
        assert rendered["workbench"]["release_evidence_ready"] is True
        assert "record_audit_event" in rendered["visible_actions"]
        assert "prepare_forensic_export" in rendered["visible_actions"]
        assert document_plan["ok"] is True
        assert "AuditLedgerForensicExportWizard" in tuple(
            contract["wizard"] for contract in service.standalone_service_manifest()["contracts"] if contract["wizard"]
        )
        assert crud_plan["ok"] is True
        assert crud_plan["event_contract"] == "AppGen-X"
        assert crud_plan["stream_engine_picker_visible"] is False
    finally:
        service.close()


def test_retry_dead_letter_and_idempotency_are_persisted_without_duplicate_key_failure():
    service = AuditLedgerStandaloneService()
    try:
        configured = service.configure_runtime({"configuration": _configuration(retry_limit=3)})
        assert configured["ok"] is True
        envelope = {
            "event_id": "unsupported_behavior",
            "event_type": "UnsupportedAuditEvent",
            "idempotency_key": "unsupported:behavior",
            "payload": {"tenant": TENANT},
        }
        first = service.receive_event({"envelope": envelope, "simulate_failure": True})
        second = service.receive_event({"envelope": envelope, "simulate_failure": True})
        third = service.receive_event({"envelope": envelope, "simulate_failure": True})
        assert first["ok"] is False
        assert second["ok"] is False
        assert third["ok"] is False
        assert first["result"]["handler"]["status"] == "retrying"
        assert second["result"]["handler"]["attempts"] == 2
        assert third["result"]["handler"]["status"] == "dead_letter"
        state = service.repository.load_state()
        workbench = ui.audit_ledger_render_workbench(
            state,
            tenant=TENANT,
            principal_permissions=("audit_ledger.read", "audit_ledger.event"),
        )
        assert state["handled_events"]["unsupported:behavior"]["attempts"] == 3
        assert state["dead_letter"][0]["reason"] == "unsupported_or_failed_audit_event"
        assert workbench["retry_evidence_count"] == 1
        assert workbench["dead_letter_count"] == 1
    finally:
        service.close()


def test_advanced_audit_runtime_and_boundary_contracts_are_executable():
    smoke = runtime.audit_ledger_runtime_smoke()
    state = smoke["state"]
    assert smoke["ok"] is True
    assert not smoke["blocking_gaps"]
    proof = runtime.audit_ledger_generate_disclosure_proof(
        state, "audit_route", disclosure=("audit_id", "actor", "action")
    )
    minimization = runtime.audit_ledger_plan_disclosure_minimization(
        state,
        tenant="tenant_alpha",
        classification="regulated",
        requested_fields=("audit_id", "actor", "action", "payload_hash", "payload"),
    )
    correction = runtime.audit_ledger_plan_correction_event(
        state,
        "audit_route",
        corrected_fields={"method": "PUT"},
        reason="source correction",
        authority="controller",
    )
    control_tests = runtime.audit_ledger_run_control_tests(state)
    notarization = runtime.audit_ledger_build_notarization_bundle(state, tenant="tenant_alpha")
    allowed_boundary = runtime.audit_ledger_verify_owned_table_boundary(
        (
            "audit_ledger_audit_event",
            "audit_ledger_appgen_outbox_event",
            "WorkflowCompleted",
            "GET /workflow/instances",
            "workflow_completion_projection",
        )
    )
    blocked_boundary = runtime.audit_ledger_verify_owned_table_boundary(("workflow_internal_table",))
    release = runtime.audit_ledger_build_release_evidence()
    assert proof["ok"] is True
    assert proof["proof"].startswith("zk_audit_")
    assert minimization["ok"] is True
    assert "payload_hash" in minimization["plan"]["selected_fields"]
    assert correction["ok"] is True
    assert correction["plan"]["correction"]["correction_of"] == "audit_route"
    assert control_tests["ok"] is True
    assert control_tests["hash_chain_valid"] is True
    assert notarization["ok"] is True
    assert notarization["bundle"]["boundary_ok"] is True
    assert allowed_boundary["ok"] is True
    assert blocked_boundary["ok"] is False
    assert blocked_boundary["violations"] == ("workflow_internal_table",)
    assert release["ok"] is True
    assert release["schema"]["datastore_backends"] == runtime.AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
    assert release["api"]["event_contract"] == "AppGen-X"
    assert release["api"]["stream_engine_picker_visible"] is False


def test_configuration_rejects_forbidden_backends_and_eventing_pickers():
    state = runtime.audit_ledger_empty_state()
    bad_backend = {**_configuration(), "database_backend": "sqlite"}
    bad_eventing = {**_configuration(), "stream_engine": "kafka"}
    bad_topic = {**_configuration(), "event_topic": "custom.audit.topic"}
    for payload, expected in (
        (bad_backend, "PostgreSQL, MySQL, or MariaDB"),
        (bad_eventing, "AppGen-X event contract"),
        (bad_topic, runtime.AUDIT_LEDGER_REQUIRED_EVENT_TOPIC),
    ):
        try:
            runtime.audit_ledger_configure_runtime(state, payload)
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"configuration unexpectedly accepted {payload}")
