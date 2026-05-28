import pytest

from pyAppGen.pbcs.asset_lifecycle import ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.asset_lifecycle.agent import depreciation_revision_preview
from pyAppGen.pbcs.asset_lifecycle.events import event_contract_manifest
from pyAppGen.pbcs.asset_lifecycle.release_evidence import build_release_evidence
from pyAppGen.pbcs.asset_lifecycle.release_evidence import validate_release_evidence
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_build_depreciation_schedule
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_configure_runtime
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_empty_state
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_place_asset_in_service
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_record_maintenance_adjustment
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_register_asset
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_review_depreciation_plan
from pyAppGen.pbcs.asset_lifecycle.runtime import asset_lifecycle_run_depreciation
from pyAppGen.pbcs.asset_lifecycle.services import AssetLifecycleService
from pyAppGen.pbcs.asset_lifecycle.services import operation_plan
from pyAppGen.pbcs.asset_lifecycle.ui import asset_lifecycle_render_workbench
from pyAppGen.pbcs.asset_lifecycle.ui import asset_lifecycle_ui_contract


def _configured_state():
    state = asset_lifecycle_empty_state()
    return asset_lifecycle_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "default_book": "corporate",
            "workbench_limit": 50,
        },
    )["state"]


def _register_asset(state, *, asset_id="asset_dep"):
    state = asset_lifecycle_register_asset(
        state,
        {
            "asset_id": asset_id,
            "tenant": "tenant_dep",
            "legal_entity": "entity_dep",
            "description": "CNC Router",
            "category": "equipment",
            "cost": 24000,
            "residual_value": 0,
            "currency": "USD",
            "book": "corporate",
            "useful_life_months": 24,
            "location": "plant_1",
            "custodian": "ops_manager",
            "cost_center": "manufacturing",
            "components": ("frame", "spindle"),
            "identity": {"did": f"did:appgen:{asset_id}", "issuer": "asset_registry", "status": "active"},
        },
    )["state"]
    return asset_lifecycle_place_asset_in_service(state, asset_id, service_date="2026-01-15")["state"]


def test_depreciation_schedule_revision_versions_remaining_life_and_history():
    state = _register_asset(_configured_state())

    initial = asset_lifecycle_build_depreciation_schedule(state, "asset_dep", method="straight_line")
    state = initial["state"]
    first_run = asset_lifecycle_run_depreciation(state, run_id="dep_jan", period="2026-01")
    state = first_run["state"]
    maintenance = asset_lifecycle_record_maintenance_adjustment(
        state,
        "asset_dep",
        useful_life_delta_months=12,
        evidence="major_overhaul",
    )
    state = maintenance["state"]
    before_revision = asset_lifecycle_review_depreciation_plan(state, "asset_dep")
    revised = asset_lifecycle_build_depreciation_schedule(state, "asset_dep", method="straight_line")
    after_revision = asset_lifecycle_review_depreciation_plan(revised["state"], "asset_dep")

    assert initial["schedule"]["version"] == 1
    assert initial["schedule"]["revision_reason"] == "initial_build"
    assert first_run["run"]["calculated_total"] == 1000
    assert before_revision["revision_required"] is True
    assert revised["schedule"]["version"] == 2
    assert revised["superseded_schedule_id"] == initial["schedule"]["schedule_id"]
    assert revised["schedule"]["revision_reason"] == "life_change"
    assert revised["schedule"]["assumptions"]["remaining_months"] == 35
    assert revised["schedule"]["lines"][0]["period"] == "2026-02"
    assert sum(line["amount"] for line in revised["schedule"]["lines"]) == pytest.approx(23000.0)
    assert after_revision["revision_required"] is False
    assert after_revision["posted_periods"] == ("2026-01",)
    assert [item["status"] for item in after_revision["schedule_versions"]] == ["superseded", "active"]


def test_depreciation_run_replays_prior_evidence_for_duplicate_period():
    state = _register_asset(_configured_state(), asset_id="asset_idem")
    state = asset_lifecycle_build_depreciation_schedule(state, "asset_idem", method="straight_line")["state"]

    first = asset_lifecycle_run_depreciation(state, run_id="dep_feb_primary", period="2026-02")
    replay = asset_lifecycle_run_depreciation(first["state"], run_id="dep_feb_retry", period="2026-02")
    review = asset_lifecycle_review_depreciation_plan(first["state"], "asset_idem")

    assert first["ok"] is True
    assert first["duplicate"] is False
    assert replay["ok"] is True
    assert replay["duplicate"] is True
    assert replay["duplicate_of"] == "dep_feb_primary"
    assert replay["run"]["run_id"] == "dep_feb_primary"
    assert replay["idempotency_key"] == first["idempotency_key"]
    assert len(first["state"]["depreciation_runs"]) == 1
    assert len(first["state"]["outbox"]) == 3
    assert first["state"]["assets"]["asset_idem"]["book_value"] == 23000
    assert review["idempotency_keys"] == (first["idempotency_key"],)


def test_service_ui_agent_and_release_evidence_expose_depreciation_slice():
    service = AssetLifecycleService()
    preview = service.preview_depreciation_plan(
        {
            "asset": {
                "asset_id": "asset_preview",
                "cost": 12000,
                "book_value": 11800,
                "residual_value": 1000,
                "useful_life_months": 60,
                "depreciation_months_posted": 12,
                "service_date": "2025-01-15",
                "next_depreciation_period": "2026-01",
            },
            "current_schedule": {"schedule_id": "sch_asset_preview_v1", "version": 1},
            "revision_reason": "maintenance_review",
        }
    )

    runtime_state = _register_asset(_configured_state(), asset_id="asset_ui")
    runtime_state = asset_lifecycle_build_depreciation_schedule(runtime_state, "asset_ui", method="straight_line")["state"]
    runtime_state = asset_lifecycle_run_depreciation(runtime_state, run_id="dep_ui_jan", period="2026-01")["state"]
    runtime_state = asset_lifecycle_record_maintenance_adjustment(
        runtime_state,
        "asset_ui",
        useful_life_delta_months=6,
        evidence="refurbishment",
    )["state"]
    rendered = asset_lifecycle_render_workbench(
        runtime_state,
        tenant="tenant_dep",
        principal_permissions=("asset_lifecycle.read", "asset_lifecycle.depreciation"),
    )

    agent_preview = depreciation_revision_preview(
        {
            "asset": {
                "asset_id": "asset_agent",
                "cost": 9000,
                "book_value": 9000,
                "residual_value": 0,
                "useful_life_months": 36,
                "service_date": "2026-01-01",
            }
        }
    )
    ui_contract = asset_lifecycle_ui_contract()
    event_manifest = event_contract_manifest()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert preview["ok"] is True
    assert preview["preview"]["version"] == 2
    assert preview["preview"]["revision_reason"] == "maintenance_review"
    assert "preview_depreciation_plan" in service.preview_depreciation_plan.__name__
    assert operation_plan("command_depreciation_runs")["emitted_event"] == "DepreciationCalculated"
    assert operation_plan("command_assets_events_inbox")["emitted_event"] is None

    assert "DepreciationRevisionConsole" in ui_contract["fragments"]
    assert "review_depreciation_plan" in ui_contract["action_permissions"]
    assert rendered["depreciation_controls"]["pending_schedule_revisions"] == 1
    assert rendered["depreciation_controls"]["active_schedule_versions"]["asset_ui"] == 1
    assert rendered["depreciation_controls"]["idempotency_keys"]

    assert agent_preview["ok"] is True
    assert agent_preview["preview"]["schedule_id"].startswith("sch_asset_agent_v")
    assert event_manifest["topic"] == ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
    assert event_manifest["dead_letter_table"] == "asset_lifecycle_dead_letter_event"

    check_ids = {check["id"] for check in release["checks"]}
    assert {"appgen_event_alignment", "depreciation_preview_surface", "depreciation_revision_ui_surface"} <= check_ids
    assert validation["ok"] is True
