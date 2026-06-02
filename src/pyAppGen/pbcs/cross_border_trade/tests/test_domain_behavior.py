from pyAppGen.pbcs.cross_border_trade.runtime import (
    CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS,
    CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC,
    cross_border_trade_build_release_evidence,
    cross_border_trade_runtime_capabilities,
    cross_border_trade_runtime_smoke,
)
from pyAppGen.pbcs.cross_border_trade.trade_control import (
    CAPABILITY_TABLES,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    SLUG_BY_NUMBER,
    TRADE_CONTROL_CAPABILITIES,
    TRADE_CONTROL_FUNCTIONS,
    evaluate_trade_control,
    improve1_trade_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.cross_border_trade.ui import cross_border_trade_ui_contract


def test_all_50_trade_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(TRADE_CONTROL_CAPABILITIES) == 50
    assert set(TRADE_CONTROL_CAPABILITIES) == set(TRADE_CONTROL_FUNCTIONS)

    for capability in TRADE_CONTROL_CAPABILITIES:
        result = TRADE_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == CROSS_BORDER_TRADE_REQUIRED_EVENT_TOPIC
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS
        assert result["agent_skill"].startswith("cross_border_trade_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_trade_controls_reject_missing_fields_and_foreign_table_access():
    first = TRADE_CONTROL_CAPABILITIES[0]
    missing = evaluate_trade_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("order_header_table",)
    rejected = evaluate_trade_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("order_header_table",)


def test_classification_landed_cost_screening_declaration_and_release_controls_surface_findings():
    classification = sample_payload_for(SLUG_BY_NUMBER[1])
    classification["confidence"] = 0.4
    assert "hs_classification_requires_review_threshold" in evaluate_trade_control(SLUG_BY_NUMBER[1], classification)["domain_findings"]

    lifecycle = sample_payload_for(SLUG_BY_NUMBER[2])
    lifecycle["state"] = "quietly_approved"
    assert "classification_lifecycle_state_invalid" in evaluate_trade_control(SLUG_BY_NUMBER[2], lifecycle)["domain_findings"]

    quote = sample_payload_for(SLUG_BY_NUMBER[5])
    quote["incoterm"] = "FREEFORM"
    assert "landed_cost_requires_supported_incoterm" in evaluate_trade_control(SLUG_BY_NUMBER[5], quote)["domain_findings"]

    screening = sample_payload_for(SLUG_BY_NUMBER[9])
    screening["list_sources"] = ()
    assert "denied_party_screening_requires_list_sources" in evaluate_trade_control(SLUG_BY_NUMBER[9], screening)["domain_findings"]

    release_gate = sample_payload_for(SLUG_BY_NUMBER[18])
    release_gate["hold_status"] = "open"
    assert "declaration_release_gate_blocks_open_hold" in evaluate_trade_control(SLUG_BY_NUMBER[18], release_gate)["domain_findings"]


def test_boundary_schema_control_agent_and_release_readiness_require_governance():
    boundary = sample_payload_for(SLUG_BY_NUMBER[38])
    boundary["dependency_mode"] = "shared_table"
    assert "cross_pbc_boundary_must_use_api_event_or_projection" in evaluate_trade_control(SLUG_BY_NUMBER[38], boundary)["domain_findings"]

    extension = sample_payload_for(SLUG_BY_NUMBER[40])
    extension["owned_table"] = "broker_shared_table"
    assert "schema_extension_must_target_owned_trade_table" in evaluate_trade_control(SLUG_BY_NUMBER[40], extension)["domain_findings"]

    control = sample_payload_for(SLUG_BY_NUMBER[45])
    control["failure_type"] = "agent_preview_bypass"
    assert "continuous_control_blocks_agent_preview_bypass" in evaluate_trade_control(SLUG_BY_NUMBER[45], control)["domain_findings"]

    agent = sample_payload_for(SLUG_BY_NUMBER[48])
    agent["human_confirmation"] = False
    agent_review = evaluate_trade_control(SLUG_BY_NUMBER[48], agent)
    assert "agent_trade_plan_requires_human_confirmation" in agent_review["domain_findings"]
    assert agent_review["requires_human_confirmation"] is True

    proof = sample_payload_for(SLUG_BY_NUMBER[50])
    proof["boundary_verification"] = False
    assert "end_to_end_release_requires_boundary_verification" in evaluate_trade_control(SLUG_BY_NUMBER[50], proof)["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_trade_control_contract():
    contract = improve1_trade_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CROSS_BORDER_TRADE_ALLOWED_DATABASE_BACKENDS

    runtime = cross_border_trade_runtime_capabilities()
    smoke = cross_border_trade_runtime_smoke()
    release = cross_border_trade_build_release_evidence()
    ui = cross_border_trade_ui_contract()

    assert runtime["improve1_trade_control"]["ok"] is True
    assert smoke["improve1_trade_control"]["ok"] is True
    assert any(check["id"] == "improve1_trade_control" and check["ok"] for check in smoke["checks"])
    assert release["improve1_trade_control"]["capability_count"] == 50
    assert len(ui["trade_control_panels"]) == 50
    assert ui["trade_control_contract"]["ok"] is True
