"""IT service management behavior checks for the improve1 executable control surface."""

from ..itsm_control import (
    EVENT_CONTRACT,
    ITSM_CONTROL_ALLOWED_DATABASE_BACKENDS,
    ITSM_CONTROL_OWNED_TABLES,
    ITSM_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_itsm_control,
    improve1_itsm_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import it_service_management_build_release_evidence, it_service_management_runtime_capabilities
from ..ui import it_service_management_render_workbench, it_service_management_ui_contract


def test_all_improve1_features_have_executable_itsm_control_evidence():
    contract = improve1_itsm_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == ITSM_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == ITSM_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in ITSM_CONTROL_OWNED_TABLES
            assert table.startswith("it_service_management_")


def test_runtime_release_and_ui_expose_itsm_control_contract():
    runtime = it_service_management_runtime_capabilities()
    runtime_release = it_service_management_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = it_service_management_ui_contract()
    workbench = it_service_management_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_itsm_control_contract" in runtime["operations"]
    assert runtime["itsm_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["itsm_control"]["ok"] is True
    assert release["ok"] is True and release["itsm_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["itsm_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["itsm_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["itsm_control_service_actions"]) == 50


def test_major_incident_declaration_requires_command_and_war_room_evidence():
    result = evaluate_itsm_control(1, {"major_incident": False, "war_room_opened": False})
    assert result["ok"] is False
    assert "Major incident" in result["findings"][0]


def test_access_request_entitlement_validation_blocks_invalid_provisioning():
    result = evaluate_itsm_control(8, {"provisioning_blocked_until_valid": False, "sod_check": False})
    assert result["ok"] is False
    assert "Access request" in result["findings"][0]


def test_change_calendar_and_cab_controls_block_unsafe_changes():
    blackout = evaluate_itsm_control(13, {"schedule_blocked_on_blackout": False})
    cab = evaluate_itsm_control(14, {"quorum_met": False, "minutes_captured": False})
    backout = evaluate_itsm_control(15, {"implementation_blocked_without_plan": False})
    assert blackout["ok"] is False and "Maintenance windows" in blackout["findings"][0]
    assert cab["ok"] is False and "CAB" in cab["findings"][0]
    assert backout["ok"] is False and "Backout" in backout["findings"][0]


def test_sla_pause_and_document_intake_require_audit_and_confirmation():
    pause = evaluate_itsm_control(26, {"manual_pause_guard": False})
    intake = evaluate_itsm_control(31, {"human_confirmation": False, "direct_mutation_blocked": False, "source_citations": ()})
    assert pause["ok"] is False and "Calendar-aware" in pause["findings"][0]
    assert intake["ok"] is False and "Structured intake" in intake["findings"][0]


def test_dead_letter_crypto_and_tenant_controls_have_safe_boundaries():
    dead_letter = evaluate_itsm_control(35, {"safe_replay_allowed": False})
    crypto = evaluate_itsm_control(40, {"proof_verified": False})
    tenant = evaluate_itsm_control(41, {"cross_tenant_access_blocked": False})
    assert dead_letter["ok"] is False and "Dead-letter" in dead_letter["findings"][0]
    assert crypto["ok"] is False and "Cryptographic" in crypto["findings"][0]
    assert tenant["ok"] is False and "Tenant isolation" in tenant["findings"][0]


def test_api_idempotency_and_end_to_end_scenario_are_required():
    api = evaluate_itsm_control(49, {"duplicate_prevented": False, "stable_response": False})
    scenario = evaluate_itsm_control(50, {"events_emitted": False, "release_documents_updated": False})
    assert api["ok"] is False and "API completeness" in api["findings"][0]
    assert scenario["ok"] is False and "End-to-end" in scenario["findings"][0]
