
"""Domain behavior tests for energy grid improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.energy_grid_operations.energy_grid_control import (
    ENERGY_GRID_ALLOWED_DATABASE_BACKENDS,
    ENERGY_GRID_DECLARED_DEPENDENCIES,
    ENERGY_GRID_OWNED_TABLES,
    ENERGY_GRID_REQUIRED_EVENT_TOPIC,
    evaluate_energy_grid_control,
    improve1_energy_grid_control_contract,
)
from pyAppGen.pbcs.energy_grid_operations.runtime import (
    energy_grid_operations_build_release_evidence,
    energy_grid_operations_runtime_capabilities,
    energy_grid_operations_runtime_smoke,
)
from pyAppGen.pbcs.energy_grid_operations.ui import energy_grid_operations_ui_contract


def test_all_improve1_controls_have_executable_domain_evidence():
    contract = improve1_energy_grid_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == ENERGY_GRID_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == ENERGY_GRID_ALLOWED_DATABASE_BACKENDS
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
        assert set(evidence["owned_tables"]).issubset(set(ENERGY_GRID_OWNED_TABLES))
        assert set(evidence["declared_dependencies"]).issubset(set(ENERGY_GRID_DECLARED_DEPENDENCIES))


def test_grid_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    release = energy_grid_operations_build_release_evidence()
    runtime = energy_grid_operations_runtime_smoke()
    capabilities = energy_grid_operations_runtime_capabilities()
    ui = energy_grid_operations_ui_contract()

    assert release["ok"] is True
    assert release["energy_grid_control"]["ok"] is True
    assert runtime["ok"] is True
    assert runtime["checks_by_id"]["improve1_energy_grid_control_contract"] is True
    assert runtime["energy_grid_control"]["capability_count"] == 50
    assert "improve1_energy_grid_control_contract" in capabilities["operations"]
    assert len(capabilities["improve1_energy_grid_control_capabilities"]) == 50
    assert ui["energy_grid_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["energy_grid_control_panels"]) == 50


def test_switching_and_dispatch_guardrails_block_unsafe_grid_operations():
    no_hold = evaluate_energy_grid_control(5, {"hold_points": (), "ordered_steps": True})
    mutating_simulation = evaluate_energy_grid_control(6, {"validation_only": True, "mutation_count": 1})
    stale_dispatch = evaluate_energy_grid_control(8, {"telemetry_freshness_seconds": 900})

    assert no_hold["ok"] is False
    assert "hold points" in no_hold["findings"][0]
    assert mutating_simulation["ok"] is False
    assert "side-effect free" in mutating_simulation["findings"][0]
    assert stale_dispatch["ok"] is False
    assert "stale telemetry" in stale_dispatch["findings"][0]


def test_forecast_constraint_and_restoration_rules_are_domain_specific():
    missing_forecast_lineage = evaluate_energy_grid_control(12, {"confidence_metadata": ""})
    invalid_constraint = evaluate_energy_grid_control(13, {"constraint_type": "generic_threshold"})
    weak_restoration = evaluate_energy_grid_control(14, {"candidate_paths": ("single-path",)})

    assert missing_forecast_lineage["ok"] is False
    assert "source and confidence lineage" in missing_forecast_lineage["findings"][0]
    assert invalid_constraint["ok"] is False
    assert "grid operating constraint types" in invalid_constraint["findings"][0]
    assert weak_restoration["ok"] is False
    assert "ranked alternative paths" in weak_restoration["findings"][0]


def test_boundary_event_and_agent_controls_enforce_appgen_x_contract():
    tenant_leak = evaluate_energy_grid_control(29, {"cross_tenant_lookup": True})
    foreign_table = evaluate_energy_grid_control(30, {"target_table": "external_grid_asset"})
    event_picker = evaluate_energy_grid_control(44, {"stream_engine_picker_visible": True})
    unsafe_agent = evaluate_energy_grid_control(39, {"permission_checked": False})

    assert tenant_leak["ok"] is False
    assert "cross-tenant" in tenant_leak["findings"][0]
    assert foreign_table["ok"] is False
    assert "owned tables" in foreign_table["findings"][0]
    assert event_picker["ok"] is False
    assert "AppGen-X topic" in event_picker["findings"][0]
    assert unsafe_agent["ok"] is False
    assert "permission checks" in unsafe_agent["findings"][0]


def test_release_and_readiness_controls_cover_control_room_operations():
    bad_carbon = evaluate_energy_grid_control(37, {"reliability_priority": "secondary"})
    weak_packet = evaluate_energy_grid_control(48, {"citation_spans": (), "draft_side_effect_free": True})
    failed_release = evaluate_energy_grid_control(49, {"metric_gate": "failed"})
    unresolved_risk = evaluate_energy_grid_control(50, {"unresolved_risks": ("open_switching_gap",)})

    assert bad_carbon["ok"] is False
    assert "outrank safety or reliability" in bad_carbon["findings"][0]
    assert weak_packet["ok"] is False
    assert "citation backed" in weak_packet["findings"][0]
    assert failed_release["ok"] is False
    assert "release assurance" in failed_release["findings"][0]
    assert unresolved_risk["ok"] is False
    assert "readiness pack" in unresolved_risk["findings"][0]
