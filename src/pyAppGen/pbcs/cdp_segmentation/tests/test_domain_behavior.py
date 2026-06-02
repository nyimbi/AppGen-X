from pyAppGen.pbcs.cdp_segmentation import cdp_control as cc, runtime, ui


def _payload_for(capability: str) -> dict:
    payload = {field: f"{capability}-{field}" for field in cc.REQUIRED_FIELDS[capability]}
    payload.update({
        "customer_id": "cust-900",
        "segment_id": "seg-900",
        "confidence": 0.94,
        "table_refs": (cc.CAPABILITY_TABLES[capability],),
        "effective_at": "2026-05-30",
    })
    return payload


def test_cdp_control_primitives_cover_all_improve1_capabilities():
    results = tuple(function(_payload_for(capability)) for capability, function in cc.CDP_CONTROL_FUNCTIONS.items())
    assert len(cc.CDP_CONTROL_CAPABILITIES) == 50
    assert len(cc.CDP_CONTROL_FUNCTIONS) == 50
    assert len(results) == 50
    assert all(result["ok"] is True for result in results)
    assert {result["capability"] for result in results} == set(cc.CDP_CONTROL_CAPABILITIES)
    assert all(result["owned_table"] in cc.OWNED_TABLES for result in results)
    assert all(result["event_contract"] == "AppGen-X" for result in results)
    assert all(result["stream_engine_picker_visible"] is False for result in results)
    assert cc.protect_sensitive_attributes(_payload_for("sensitive_attribute_protection"))["privacy_review_required"] is True
    assert cc.build_natural_language_audience_plan(_payload_for("natural_language_audience_builder"))["agent_plan_only"] is True


def test_cdp_controls_block_foreign_tables_and_missing_required_fields():
    missing = cc.build_event_ingestion_contract({"event_family": "commerce"})
    foreign = cc.prove_cross_pbc_projection_boundary({
        **_payload_for("cross_pbc_projection_boundary_proof"),
        "table_refs": ("customer_360_customer",),
    })
    assert missing["ok"] is False
    assert "identity_keys" in missing["missing_fields"]
    assert foreign["ok"] is False
    assert foreign["foreign_references"] == ("customer_360_customer",)
    assert foreign["shared_table_access"] is False


def test_runtime_ui_and_release_evidence_surface_cdp_controls():
    contract = cc.improve1_cdp_control_contract()
    release = runtime.cdp_segmentation_build_release_evidence()
    ui_contract = ui.cdp_segmentation_ui_contract()
    boundary = runtime.cdp_segmentation_verify_owned_table_boundary((
        "customer_event",
        "customer_360_customer",
    ))
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert release["ok"] is True
    assert release["improve1_cdp_control"]["capability_count"] == 50
    assert any(check["id"] == "improve1_cdp_control" and check["ok"] for check in release["checks"])
    assert len(ui_contract["cdp_control_panels"]) == 50
    assert ui_contract["cdp_control_contract"]["shared_table_access"] is False
    assert runtime.CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert boundary["ok"] is False
