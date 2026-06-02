"""Fraud-domain behavior checks for the improve1 executable control surface."""

from ..fraud_control import (
    EVENT_CONTRACT,
    FRAUD_CONTROL_ALLOWED_DATABASE_BACKENDS,
    FRAUD_CONTROL_OWNED_TABLES,
    FRAUD_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_fraud_control,
    improve1_fraud_control_contract,
)
from ..release_evidence import release_readiness_manifest, validate_release_evidence, build_release_evidence
from ..runtime import fraud_anomaly_detection_runtime_capabilities
from ..ui import _appgen_smoke_state, fraud_anomaly_detection_ui_contract, fraud_anomaly_detection_render_workbench


def test_all_improve1_features_have_executable_fraud_control_evidence():
    contract = improve1_fraud_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == FRAUD_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == FRAUD_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in FRAUD_CONTROL_OWNED_TABLES
            assert table.startswith("fraud_anomaly_detection_")


def test_runtime_release_and_ui_expose_fraud_control_contract():
    runtime = fraud_anomaly_detection_runtime_capabilities()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = fraud_anomaly_detection_ui_contract()
    permissions = tuple(dict.fromkeys(ui.get("action_permissions", {}).values()))
    workbench = fraud_anomaly_detection_render_workbench(_appgen_smoke_state(), tenant="smoke", principal_permissions=permissions)
    assert runtime["ok"] is True
    assert "improve1_fraud_control_contract" in runtime["operations"]
    assert runtime["fraud_control"]["capability_count"] == 50
    assert release["ok"] is True and release["fraud_control"]["ok"] is True
    assert manifest["ok"] is True and "complete_fraud_workbench" in manifest["sections"]
    assert validation["ok"] is True and validation["fraud_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["fraud_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["fraud_control_service_actions"]) == 50


def test_risk_signal_canonicalization_requires_provenance_and_idempotency():
    result = evaluate_fraud_control(1, {"provenance_hash": "", "idempotency_key": "", "confidence": 0})
    assert result["ok"] is False
    assert "canonicalization" in result["findings"][0]


def test_signal_quality_quarantines_invalid_or_duplicate_signals():
    result = evaluate_fraud_control(2, {"schema_validity": False, "duplicate_status": "duplicate", "quarantine_required": True})
    assert result["ok"] is False
    assert "quality gate" in result["findings"][0]


def test_rule_lifecycle_blocks_unapproved_activation():
    result = evaluate_fraud_control(14, {"rule_state": "draft", "activation_allowed": False})
    assert result["ok"] is False
    assert "lifecycle" in result["findings"][0]


def test_counterfactual_simulation_is_side_effect_free():
    result = evaluate_fraud_control(15, {"live_mutation_blocked": False})
    assert result["ok"] is False
    assert "side-effect free" in result["findings"][0]


def test_explanations_block_sensitive_tactic_leakage():
    result = evaluate_fraud_control(17, {"tactic_leakage_blocked": False})
    assert result["ok"] is False
    assert "sensitive fraud tactics" in result["findings"][0]


def test_tenant_region_isolation_blocks_cross_tenant_mutation():
    result = evaluate_fraud_control(33, {"cross_tenant_mutation_blocked": False, "region_authorized": False})
    assert result["ok"] is False
    assert "tenant and region isolation" in result["findings"][0]


def test_agent_investigation_requires_citations_and_confirmation():
    result = evaluate_fraud_control(44, {"source_citations": (), "human_confirmation": False})
    assert result["ok"] is False
    assert "agent-assisted fraud investigation" in result["findings"][0]


def test_cross_pbc_boundary_requires_owned_mutations_and_declared_dependencies():
    result = evaluate_fraud_control(47, {"owned_mutation_only": False, "appgen_runtime_tables_only": False, "dependency_declared": False})
    assert result["ok"] is False
    assert "cross-PBC boundary" in result["findings"][0]


def test_fraud_release_pack_requires_scoring_fairness_ui_and_agent_evidence():
    result = evaluate_fraud_control(49, {"scoring_backtests": False, "fairness_checks": False, "agent_manifests": False})
    assert result["ok"] is False
    assert "release evidence pack" in result["findings"][0]
