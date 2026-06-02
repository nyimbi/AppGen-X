from pyAppGen.pbcs.claims_adjudication_healthcare import claims_control as cc, runtime, ui
from pyAppGen.pbcs.claims_adjudication_healthcare.release_evidence import release_readiness_manifest, validate_release_evidence


def _payload_for(capability: str) -> dict:
    payload = {field: f"{capability}-{field}" for field in cc.REQUIRED_FIELDS[capability]}
    payload.update({
        "claim_id": "CLAIM-900",
        "line_id": "LINE-900",
        "confidence": 0.95,
        "table_refs": (cc.CAPABILITY_TABLES[capability],),
        "effective_at": "2026-05-30",
    })
    return payload


def test_claims_control_primitives_cover_all_improve1_capabilities():
    results = tuple(function(_payload_for(capability)) for capability, function in cc.CLAIMS_CONTROL_FUNCTIONS.items())
    assert len(cc.CLAIMS_CONTROL_CAPABILITIES) == 50
    assert len(cc.CLAIMS_CONTROL_FUNCTIONS) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(cc.CLAIMS_CONTROL_CAPABILITIES)
    assert all(result["owned_table"].startswith("claims_adjudication_healthcare_") for result in results)
    assert all(result["event_contract"] == "AppGen-X" for result in results)
    assert all(result["stream_engine_picker_visible"] is False for result in results)
    assert cc.plan_agent_assisted_claim_review(_payload_for("agent_assisted_claim_review"))["agent_plan_only"] is True
    assert cc.manage_medical_necessity_review(_payload_for("medical_necessity_review"))["clinical_or_financial_review_required"] is True


def test_claims_controls_block_foreign_tables_and_missing_required_fields():
    missing = cc.canonicalize_claim_intake({"claim_type": "professional"})
    foreign = cc.prove_claims_package_boundaries({
        **_payload_for("package_boundary_proofs"),
        "table_refs": ("member_enrollment_table",),
    })
    assert missing["ok"] is False
    assert "source_format" in missing["missing_fields"]
    assert foreign["ok"] is False
    assert foreign["foreign_references"] == ("member_enrollment_table",)
    assert foreign["shared_table_access"] is False


def test_runtime_ui_and_release_evidence_surface_claims_controls():
    contract = cc.improve1_claims_control_contract()
    release = runtime.claims_adjudication_healthcare_build_release_evidence()
    ui_contract = ui.claims_adjudication_healthcare_ui_contract()
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    boundary = runtime.claims_adjudication_healthcare_verify_owned_table_boundary((
        "claims_adjudication_healthcare_health_claim",
        "foreign_table",
    ))
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert release["ok"] is True
    assert release["generated_artifacts"]["improve1_claims_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_claims_control" and check["ok"] for check in release["checks"])
    assert len(ui_contract["full_capability_surface"]["claims_control_panels"]) == 50
    assert ui_contract["full_capability_surface"]["claims_control_contract"]["shared_table_access"] is False
    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert runtime.CLAIMS_ADJUDICATION_HEALTHCARE_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert boundary["ok"] is False
