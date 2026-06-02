
"""Domain behavior tests for Enterprise PIM improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.enterprise_pim.pim_control import (
    PIM_ALLOWED_DATABASE_BACKENDS,
    PIM_DECLARED_DEPENDENCIES,
    PIM_OWNED_TABLES,
    PIM_REQUIRED_EVENT_TOPIC,
    evaluate_pim_control,
    improve1_pim_control_contract,
)
from pyAppGen.pbcs.enterprise_pim.runtime import (
    enterprise_pim_build_release_evidence,
    enterprise_pim_runtime_capabilities,
    enterprise_pim_runtime_smoke,
)
from pyAppGen.pbcs.enterprise_pim.ui import enterprise_pim_ui_contract


def test_all_improve1_controls_have_executable_domain_evidence():
    contract = improve1_pim_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == PIM_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == PIM_ALLOWED_DATABASE_BACKENDS
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        evidence = item["evidence"]
        assert item["ok"] is True, item
        assert evidence["owned_tables"]
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()
        assert set(evidence["owned_tables"]).issubset(set(PIM_OWNED_TABLES))
        assert set(evidence["declared_dependencies"]).issubset(set(PIM_DECLARED_DEPENDENCIES))


def test_pim_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    release = enterprise_pim_build_release_evidence()
    runtime = enterprise_pim_runtime_smoke()
    capabilities = enterprise_pim_runtime_capabilities()
    ui = enterprise_pim_ui_contract()

    assert release["ok"] is True
    assert release["pim_control"]["ok"] is True
    assert runtime["ok"] is True
    assert runtime["checks_by_id"]["improve1_pim_control_contract"] is True
    assert runtime["pim_control"]["capability_count"] == 50
    assert "improve1_pim_control_contract" in capabilities["operations"]
    assert len(capabilities["improve1_pim_control_capabilities"]) == 50
    assert ui["pim_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["pim_control_panels"]) == 50


def test_taxonomy_attribute_and_localization_guardrails_block_bad_master_data():
    incompatible_taxonomy = evaluate_pim_control(1, {"dependency_compatibility": "breaking"})
    cyclic_relationship = evaluate_pim_control(3, {"acyclic": False})
    bad_content = evaluate_pim_control(12, {"content_state": "machine_translated", "quality_score": 0.4})
    forbidden_translation = evaluate_pim_control(14, {"forbidden_phrase_flags": ("unsafe",)})

    assert incompatible_taxonomy["ok"] is False
    assert "compatible dependency" in incompatible_taxonomy["findings"][0]
    assert cyclic_relationship["ok"] is False
    assert "acyclic" in cyclic_relationship["findings"][0]
    assert bad_content["ok"] is False
    assert "localized content" in bad_content["findings"][0]
    assert forbidden_translation["ok"] is False
    assert "forbidden phrase" in forbidden_translation["findings"][0]


def test_publication_dependency_and_channel_controls_are_domain_specific():
    low_completeness = evaluate_pim_control(16, {"readiness_score": 0.5})
    stale_projection = evaluate_pim_control(22, {"freshness": "stale"})
    blocked_channel = evaluate_pim_control(20, {"publication_window": "closed"})
    bad_bundle = evaluate_pim_control(27, {"price_tax_inventory_checks": "failed"})

    assert low_completeness["ok"] is False
    assert "below publication threshold" in low_completeness["findings"][0]
    assert stale_projection["ok"] is False
    assert "stale" in stale_projection["findings"][0]
    assert blocked_channel["ok"] is False
    assert "closed windows" in blocked_channel["findings"][0]
    assert bad_bundle["ok"] is False
    assert "price/tax/inventory" in bad_bundle["findings"][0]


def test_agent_event_boundary_and_control_assertions_enforce_safe_pim_operations():
    mutating_agent = evaluate_pim_control(33, {"confirmation_required": False})
    bad_inbox = evaluate_pim_control(34, {"schema_validation": "failed"})
    foreign_access = evaluate_pim_control(36, {"foreign_table_access": ("commerce.product",)})
    failing_controls = evaluate_pim_control(48, {"agent_preview_assertion": "failed"})

    assert mutating_agent["ok"] is False
    assert "preview-only" in mutating_agent["findings"][0]
    assert bad_inbox["ok"] is False
    assert "schema validation" in bad_inbox["findings"][0]
    assert foreign_access["ok"] is False
    assert "foreign table" in foreign_access["findings"][0]
    assert failing_controls["ok"] is False
    assert "failing assertions" in failing_controls["findings"][0]


def test_readiness_model_carbon_workbench_and_end_to_end_publication_are_gated():
    unapproved_model = evaluate_pim_control(44, {"approval_status": "pending"})
    carbon_sla = evaluate_pim_control(45, {"sla_guardrail": "missed"})
    incomplete_workbench = evaluate_pim_control(46, {"dependencies": "hidden"})
    low_readiness = evaluate_pim_control(49, {"readiness_score": 0.7})
    failed_publication = evaluate_pim_control(50, {"publication_step": "failed"})

    assert unapproved_model["ok"] is False
    assert "governance approval" in unapproved_model["findings"][0]
    assert carbon_sla["ok"] is False
    assert "SLA guardrails" in carbon_sla["findings"][0]
    assert incomplete_workbench["ok"] is False
    assert "command center" in incomplete_workbench["findings"][0]
    assert low_readiness["ok"] is False
    assert "readiness score" in low_readiness["findings"][0]
    assert failed_publication["ok"] is False
    assert "publication proof" in failed_publication["findings"][0]
