from pyAppGen.pbcs.case_knowledge_management import runtime, support_control as sc, ui
from pyAppGen.pbcs.case_knowledge_management.release_evidence import release_readiness_manifest, validate_release_evidence


def _payload_for(capability: str) -> dict:
    payload = {field: f"{capability}-{field}" for field in sc.REQUIRED_FIELDS[capability]}
    payload.update({
        "case_id": "CASE-900",
        "article_id": "KA-900",
        "confidence": 0.92,
        "owned_table_refs": (sc.CAPABILITY_TABLES[capability],),
        "effective_at": "2026-05-30",
    })
    return payload


def test_support_control_primitives_cover_all_improve1_capabilities():
    results = tuple(function(_payload_for(capability)) for capability, function in sc.SUPPORT_CONTROL_FUNCTIONS.items())
    assert len(sc.CASE_KNOWLEDGE_CAPABILITIES) == 50
    assert len(sc.SUPPORT_CONTROL_FUNCTIONS) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(sc.CASE_KNOWLEDGE_CAPABILITIES)
    assert all(result["owned_table"].startswith("case_knowledge_management_") for result in results)
    assert all(result["event_contract"] == "AppGen-X" for result in results)
    assert all(result["stream_engine_picker_visible"] is False for result in results)
    assert sc.govern_security_privacy_case(_payload_for("security_privacy_case_handling"))["policy_review_required"] is True
    assert sc.plan_agent_assisted_crud(_payload_for("agent_assisted_case_knowledge_crud"))["requires_human_confirmation"] is True


def test_support_controls_block_cross_pbc_table_references_and_missing_fields():
    missing = sc.normalize_omnichannel_intake({"channel": "email"})
    foreign = sc.prove_cross_pbc_boundaries({
        **_payload_for("cross_pbc_boundary_projection_proofs"),
        "owned_table_refs": ("customer_360_customer",),
    })
    assert missing["ok"] is False
    assert "source_transcript" in missing["missing_fields"]
    assert foreign["ok"] is False
    assert foreign["foreign_references"] == ("customer_360_customer",)
    assert foreign["shared_table_access"] is False


def test_runtime_ui_and_release_evidence_surface_support_controls():
    contract = sc.improve1_support_control_contract()
    release = runtime.case_knowledge_management_build_release_evidence()
    ui_contract = ui.case_knowledge_management_ui_contract()
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    boundary = runtime.case_knowledge_management_verify_owned_table_boundary((
        "case_knowledge_management_support_case",
        "foreign_support_table",
    ))
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert release["ok"] is True
    assert release["improve1_support_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_support_control" and check["ok"] for check in release["checks"])
    assert len(ui_contract["support_control_panels"]) == 50
    assert ui_contract["support_control_contract"]["shared_table_access"] is False
    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert boundary["ok"] is False
