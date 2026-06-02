from pyAppGen.pbcs.identity_kyc_aml_compliance.runtime import (
    identity_kyc_aml_compliance_advance_kyc_profile_lifecycle,
    identity_kyc_aml_compliance_challenge_risk_score,
    identity_kyc_aml_compliance_create_kyc_profile,
    identity_kyc_aml_compliance_empty_state,
    identity_kyc_aml_compliance_promote_alert_to_case,
    identity_kyc_aml_compliance_receive_event,
    identity_kyc_aml_compliance_record_compliance_review,
    identity_kyc_aml_compliance_record_identity_document,
    identity_kyc_aml_compliance_record_screening_hit,
    identity_kyc_aml_compliance_register_beneficial_owner,
    identity_kyc_aml_compliance_resolve_screening_hit,
    identity_kyc_aml_compliance_triage_monitoring_alert,
)


def _base_profile_payload(**overrides):
    payload = {
        "tenant": "tenant-workflow",
        "subject_name": "Workflow User",
        "customer_type": "individual",
        "jurisdiction": "KE",
        "product_exposure": "checking",
        "channel": "remote",
        "expected_activity": "salary",
    }
    payload.update(overrides)
    return payload


def test_profile_cannot_progress_to_screening_without_document_but_can_approve_after_evidence():
    state = identity_kyc_aml_compliance_empty_state()
    profile = identity_kyc_aml_compliance_create_kyc_profile(state, _base_profile_payload())
    blocked = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        profile["state"],
        {"profile_id": profile["record"]["id"], "target_status": "pending_screening", "reason_code": "attempt_without_evidence"},
    )
    assert blocked["ok"] is False
    assert "document_verification_incomplete" in blocked["blocking_reasons"]

    document = identity_kyc_aml_compliance_record_identity_document(
        profile["state"],
        {
            "profile_id": profile["record"]["id"],
            "document_class": "passport",
            "jurisdiction": "KE",
            "issuing_authority": "State",
            "identifier": "P-123",
            "issue_date": "2024-01-01",
            "expiry_date": "2030-01-01",
            "capture_method": "mobile_app",
            "face_match_confidence": 0.95,
            "liveness_outcome": "pass",
        },
    )
    pending_screening = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        document["state"],
        {"profile_id": profile["record"]["id"], "target_status": "pending_screening", "reason_code": "docs_verified"},
    )
    approved = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        pending_screening["state"],
        {"profile_id": profile["record"]["id"], "target_status": "approved", "reason_code": "clear_screening"},
    )
    assert pending_screening["ok"] is True
    assert approved["ok"] is True
    assert approved["profile"]["status"] == "approved"


def test_pep_hit_forces_edd_and_beneficial_owner_coverage_before_approval():
    state = identity_kyc_aml_compliance_empty_state()
    profile = identity_kyc_aml_compliance_create_kyc_profile(
        state,
        _base_profile_payload(customer_type="entity", registration_number="REG-1", subject_name="Entity Ltd", complex_ownership=True),
    )
    document = identity_kyc_aml_compliance_record_identity_document(
        profile["state"],
        {
            "profile_id": profile["record"]["id"],
            "document_class": "certificate_of_incorporation",
            "jurisdiction": "KE",
            "issuing_authority": "Registrar",
            "identifier": "COI-1",
            "issue_date": "2020-01-01",
            "expiry_date": "2030-01-01",
            "capture_method": "branch_scan",
        },
    )
    pending_screening = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        document["state"],
        {"profile_id": profile["record"]["id"], "target_status": "pending_screening", "reason_code": "docs_verified"},
    )
    pep = identity_kyc_aml_compliance_record_screening_hit(
        pending_screening["state"],
        {
            "profile_id": profile["record"]["id"],
            "category": "pep",
            "severity": "high",
            "confidence": 0.88,
            "disposition": "open",
        },
    )
    blocked = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        pep["state"],
        {"profile_id": profile["record"]["id"], "target_status": "approved", "reason_code": "attempt_before_edd"},
    )
    assert blocked["ok"] is False
    assert "blocking_screening_hit_open" in blocked["blocking_reasons"] or "edd_packet_incomplete" in blocked["blocking_reasons"]

    cleared = identity_kyc_aml_compliance_resolve_screening_hit(
        pep["state"],
        {"screening_hit_id": pep["record"]["id"], "disposition": "cleared", "resolved_by": "analyst"},
    )
    review = identity_kyc_aml_compliance_record_compliance_review(
        cleared["state"],
        {
            "profile_id": profile["record"]["id"],
            "review_type": "edd_packet",
            "review_status": "completed",
            "reviewer": "approver",
        },
    )
    still_blocked = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        review["state"],
        {"profile_id": profile["record"]["id"], "target_status": "approved", "reason_code": "edd_complete"},
    )
    assert still_blocked["ok"] is False
    assert "beneficial_owner_coverage_incomplete" in still_blocked["blocking_reasons"]

    owner = identity_kyc_aml_compliance_register_beneficial_owner(
        review["state"],
        {
            "profile_id": profile["record"]["id"],
            "owner_name": "Ultimate Owner",
            "role_type": "ultimate_beneficial_owner",
            "ownership_pct": 80,
        },
    )
    approved = identity_kyc_aml_compliance_advance_kyc_profile_lifecycle(
        owner["state"],
        {"profile_id": profile["record"]["id"], "target_status": "approved", "reason_code": "edd_and_ownership_complete"},
    )
    assert approved["ok"] is True
    assert approved["profile"]["status"] == "approved"


def test_policy_event_creates_follow_up_alert_and_duplicate_guard():
    state = identity_kyc_aml_compliance_empty_state()
    first = identity_kyc_aml_compliance_receive_event(
        state,
        {"event_type": "PolicyChanged", "tenant": "tenant-workflow", "idempotency_key": "event-1"},
    )
    second = identity_kyc_aml_compliance_receive_event(
        first["state"],
        {"event_type": "PolicyChanged", "tenant": "tenant-workflow", "idempotency_key": "event-1"},
    )
    assert first["ok"] is True
    assert first["follow_up"]["record"]["source_type"] == "policy_change"
    assert second["duplicate"] is True


def test_high_severity_alert_promotes_to_case():
    state = identity_kyc_aml_compliance_empty_state()
    alert = identity_kyc_aml_compliance_triage_monitoring_alert(
        state,
        {
            "tenant": "tenant-workflow",
            "source_type": "transaction_monitoring",
            "typology": "rapid_in_out",
            "severity": "high",
        },
    )
    case = identity_kyc_aml_compliance_promote_alert_to_case(
        alert["state"],
        {"alert_id": alert["record"]["id"], "profile_id": "manual-profile", "escalation_reason": "typology_confirmed"},
    )
    assert case["ok"] is True
    assert case["record"]["alert_id"] == alert["record"]["id"]


def test_risk_score_challenge_requires_supervisor_and_updates_profile():
    state = identity_kyc_aml_compliance_empty_state()
    profile = identity_kyc_aml_compliance_create_kyc_profile(
        state,
        _base_profile_payload(jurisdiction="IRN", pep_exposure=True),
    )
    blocked = identity_kyc_aml_compliance_challenge_risk_score(
        profile["state"],
        {"profile_id": profile["record"]["id"], "challenged_score": 0.2},
    )
    assert blocked["ok"] is False

    resolved = identity_kyc_aml_compliance_challenge_risk_score(
        profile["state"],
        {
            "profile_id": profile["record"]["id"],
            "challenged_score": 0.4,
            "challenge_note": "False positive geography flag",
            "supervisor": "chief-compliance",
            "reviewer": "analyst-1",
        },
    )
    assert resolved["ok"] is True
    assert resolved["profile"]["risk_score"] == 0.4
    assert resolved["review"]["review_type"] == "risk_score_challenge"
