from pyAppGen.pbcs.audit_ledger import (
    AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
    audit_ledger_build_notarization_bundle,
    audit_ledger_build_release_evidence,
    audit_ledger_configure_runtime,
    audit_ledger_define_retention_policy,
    audit_ledger_empty_state,
    audit_ledger_plan_correction_event,
    audit_ledger_plan_disclosure_minimization,
    audit_ledger_record_audit_event,
    audit_ledger_register_rule,
    audit_ledger_set_parameter,
    audit_ledger_verify_signature_chain,
)
from pyAppGen.pbcs.audit_ledger.agent import audit_event_preview, forensic_export_preview
from pyAppGen.pbcs.audit_ledger.ledger_proofs import (
    audit_ledger_proof_slice_release_evidence,
    payload_digest,
)
from pyAppGen.pbcs.audit_ledger.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.audit_ledger.runtime import audit_ledger_prepare_forensic_export
from pyAppGen.pbcs.audit_ledger.services import AuditLedgerService


def _configured_state():
    state = audit_ledger_empty_state()
    state = audit_ledger_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "signature_algorithm": "dilithium3_simulated",
            "allowed_classifications": ("internal", "regulated"),
            "export_modes": ("proof_bundle",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = audit_ledger_set_parameter(state, "retention_days", 2555)["state"]
    state = audit_ledger_set_parameter(state, "proof_disclosure_limit", 4)["state"]
    state = audit_ledger_register_rule(
        state,
        {
            "rule_id": "regulated_export_rule",
            "tenant": "tenant-a",
            "scope": "export",
            "classification": "regulated",
            "minimum_retention_days": 2555,
            "requires_legal_hold_review": True,
            "requires_export_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = audit_ledger_define_retention_policy(
        state,
        {
            "policy_id": "regulated-policy",
            "tenant": "tenant-a",
            "classification": "regulated",
            "retention_days": 2555,
            "legal_hold": False,
            "disposal_action": "review",
        },
    )["state"]
    return state


def test_canonical_payload_digest_is_deterministic_for_equivalent_payloads():
    first = payload_digest({"payload": {"b": [2, 1], "a": {"y": 2, "x": 1}}})
    second = payload_digest({"payload": {"a": {"x": 1, "y": 2}, "b": [2, 1]}})

    assert first["ok"] is True
    assert second["ok"] is True
    assert first["hash"] == second["hash"]
    assert first["canonical_payload"] == second["canonical_payload"]


def test_sealing_supports_immutable_correction_lineage_and_chain_proofs():
    state = _configured_state()
    first = audit_ledger_record_audit_event(
        state,
        {
            "audit_id": "audit-1",
            "tenant": "tenant-a",
            "source_pbc": "workflow_orchestration",
            "aggregate_id": "wf-1",
            "actor": "ops-user",
            "action": "complete_workflow",
            "classification": "regulated",
            "payload": {"status": "completed", "workflow_id": "wf-1"},
            "occurred_at": "2026-05-28T09:00:00Z",
        },
    )
    correction_plan = audit_ledger_plan_correction_event(
        first["state"],
        "audit-1",
        corrected_fields={"status": "voided"},
        reason="operator_override",
        authority="chief_auditor",
    )
    corrected = audit_ledger_record_audit_event(
        first["state"],
        {
            "audit_id": "audit-2",
            "tenant": "tenant-a",
            "source_pbc": "workflow_orchestration",
            "aggregate_id": "wf-1",
            "actor": "chief-auditor",
            "action": "correct_audit_event",
            "classification": "regulated",
            "payload": {"status": "voided"},
            "occurred_at": "2026-05-28T09:05:00Z",
            "correction_of": "audit-1",
            "corrected_fields": ("status",),
            "correction_reason": "operator_override",
            "correction_authority": "chief_auditor",
        },
    )
    proof = audit_ledger_verify_signature_chain(corrected["state"], tenant="tenant-a")

    assert correction_plan["ok"] is True
    assert corrected["ok"] is True
    assert corrected["audit_event"]["admissibility"]["admissible"] is True
    assert corrected["audit_event"]["correction"]["verified"] is True
    assert proof["ok"] is True
    assert proof["correction_links"] == (("audit-1", "audit-2"),)
    assert proof["invalid_payload_digests"] == ()
    assert proof["inadmissible_events"] == ()


def test_service_and_agent_previews_surface_sealing_and_export_minimization():
    service = AuditLedgerService()
    seal_preview = service.record_audit_event(
        {
            "audit_id": "audit-preview",
            "tenant": "tenant-a",
            "source_pbc": "gateway",
            "aggregate_id": "route-1",
            "actor": "ops-user",
            "action": "publish_route",
            "classification": "regulated",
            "payload": {"route_id": "route-1"},
        }
    )
    export_preview = service.prepare_forensic_export(
        {
            "classification": "regulated",
            "disclosure": ("actor", "action", "payload"),
            "approval_required": True,
            "sample_events": (
                {
                    "audit_id": "audit-preview",
                    "tenant": "tenant-a",
                    "source_pbc": "gateway",
                    "aggregate_id": "route-1",
                    "actor": "ops-user",
                    "action": "publish_route",
                    "classification": "regulated",
                    "sequence": 1,
                    "payload": {"route_id": "route-1"},
                    "payload_hash": "payload-hash",
                    "event_hash": "event-hash",
                },
            ),
        }
    )

    assert seal_preview["ok"] is True
    assert seal_preview["preview"]["preview"]["admissible"] is True
    assert export_preview["ok"] is True
    assert "sensitive_payload_requested" in export_preview["preview"]["preview"]["risk_flags"]
    assert audit_event_preview(seal_preview["payload"])["ok"] is True
    assert forensic_export_preview(export_preview["payload"])["ok"] is True


def test_export_planning_and_release_evidence_include_notarization_bundle():
    state = _configured_state()
    recorded = audit_ledger_record_audit_event(
        state,
        {
            "audit_id": "audit-export",
            "tenant": "tenant-a",
            "source_pbc": "schema_registry",
            "aggregate_id": "subject-1",
            "actor": "platform-user",
            "action": "accept_schema",
            "classification": "regulated",
            "payload": {"subject_id": "subject-1", "version": 7},
            "occurred_at": "2026-05-28T10:00:00Z",
        },
    )
    plan = audit_ledger_plan_disclosure_minimization(
        recorded["state"],
        tenant="tenant-a",
        classification="regulated",
        requested_fields=("actor", "action", "payload"),
    )
    export = audit_ledger_prepare_forensic_export(
        recorded["state"],
        {
            "export_id": "export-1",
            "tenant": "tenant-a",
            "classification": "regulated",
            "requested_by": "auditor",
            "purpose": "regulatory_review",
            "disclosure": ("actor", "action", "payload"),
        },
    )
    notarization = audit_ledger_build_notarization_bundle(export["state"], tenant="tenant-a")
    proof_slice = audit_ledger_proof_slice_release_evidence()
    release = audit_ledger_build_release_evidence()
    manifest = release_readiness_manifest()

    assert plan["ok"] is True
    assert plan["plan"]["approval_required"] is True
    assert "payload_hash" in plan["plan"]["selected_fields"]
    assert "sensitive_payload_requested" in plan["plan"]["risk_flags"]
    assert export["ok"] is True
    assert export["export"]["approval_required"] is True
    assert export["export"]["proof_coverage"]["event_count"] == 1
    assert notarization["ok"] is True
    assert notarization["bundle"]["boundary_ok"] is True
    assert notarization["bundle"]["chain_link_count"] == 1
    assert proof_slice["ok"] is True
    assert "release_evidence_notarization_bundle" in proof_slice["implemented_backlog_items"]
    assert release["ok"] is True
    assert release["proof_slice"]["implemented_backlog_items"] == proof_slice["implemented_backlog_items"]
    assert release["notarization_bundle"]["ok"] is True
    assert manifest["ok"] is True
    assert "proof_slice" in manifest["sections"]
