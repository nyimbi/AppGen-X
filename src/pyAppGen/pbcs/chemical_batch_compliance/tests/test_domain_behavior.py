from pyAppGen.pbcs.chemical_batch_compliance import chemical_control as cc, runtime, ui
from pyAppGen.pbcs.chemical_batch_compliance.release_evidence import release_readiness_manifest, validate_release_evidence


def _payload_for(capability: str) -> dict:
    payload = {field: f"{capability}-{field}" for field in cc.REQUIRED_FIELDS[capability]}
    payload.update({
        "batch_id": "BATCH-900",
        "lot_id": "LOT-900",
        "confidence": 0.95,
        "table_refs": (cc.CAPABILITY_TABLES[capability],),
        "effective_at": "2026-05-30",
    })
    return payload


def test_chemical_control_primitives_cover_all_improve1_capabilities():
    results = tuple(function(_payload_for(capability)) for capability, function in cc.CHEMICAL_CONTROL_FUNCTIONS.items())
    assert len(cc.CHEMICAL_CONTROL_CAPABILITIES) == 50
    assert len(cc.CHEMICAL_CONTROL_FUNCTIONS) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(cc.CHEMICAL_CONTROL_CAPABILITIES)
    assert all(result["owned_table"].startswith("chemical_batch_compliance_") for result in results)
    assert all(result["event_contract"] == "AppGen-X" for result in results)
    assert all(result["stream_engine_picker_visible"] is False for result in results)
    assert cc.enforce_governed_agent_guardrails(_payload_for("governed_agent_action_guardrails"))["agent_plan_only"] is True
    assert cc.gate_exposure_ppe_permit_work(_payload_for("exposure_ppe_permit_to_work_gating"))["quality_or_ehs_review_required"] is True


def test_chemical_controls_block_foreign_tables_and_missing_required_fields():
    missing = cc.govern_master_recipe_revision({"revision_state": "draft"})
    foreign = cc.evaluate_domain_complete_release_gate({
        **_payload_for("domain_complete_release_gate"),
        "table_refs": ("foreign_quality_table",),
    })
    assert missing["ok"] is False
    assert "ingredient_list" in missing["missing_fields"]
    assert foreign["ok"] is False
    assert foreign["foreign_references"] == ("foreign_quality_table",)
    assert foreign["shared_table_access"] is False


def test_runtime_ui_and_release_evidence_surface_chemical_controls():
    contract = cc.improve1_chemical_control_contract()
    release = runtime.chemical_batch_compliance_build_release_evidence()
    ui_contract = ui.chemical_batch_compliance_ui_contract()
    readiness = release_readiness_manifest()
    validation = validate_release_evidence()
    boundary = runtime.chemical_batch_compliance_verify_owned_table_boundary((
        "chemical_batch_compliance_batch_record",
        "foreign_table",
    ))
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert release["ok"] is True
    assert release["improve1_chemical_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_chemical_control" and check["ok"] for check in release["checks"])
    assert len(ui_contract["full_capability_surface"]["chemical_control_panels"]) == 50
    assert ui_contract["full_capability_surface"]["chemical_control_contract"]["shared_table_access"] is False
    assert readiness["ok"] is True
    assert validation["ok"] is True
    assert runtime.CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert boundary["ok"] is False
