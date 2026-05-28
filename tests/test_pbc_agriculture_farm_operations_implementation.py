from pyAppGen.pbcs.agriculture_farm_operations import (
    agriculture_farm_operations_build_release_evidence,
    agriculture_farm_operations_build_service_contract,
    agriculture_farm_operations_empty_state,
    agriculture_farm_operations_query_workbench,
    agriculture_farm_operations_record_crop_plan,
)
from pyAppGen.pbcs.agriculture_farm_operations.services import AgricultureFarmOperationsService, service_operation_manifest


def _base_payload(**overrides):
    payload = {
        "tenant": "tenant-farm",
        "field_id": "field-001",
        "management_zone": "north-block",
        "crop": "maize",
        "season": "long_rains",
        "market_year": 2026,
        "planting_date": "2026-04-24",
        "planned_start": "2026-04-24",
        "planned_end": "2026-09-15",
        "planting_window": {
            "start": "2026-04-10",
            "optimal_start": "2026-04-20",
            "optimal_end": "2026-05-05",
            "latest": "2026-05-15",
            "minimum_soil_temperature_c": 12,
            "maximum_frost_risk": 0.2,
            "minimum_rainfall_outlook_mm": 20,
            "requires_irrigation_ready": True,
        },
        "conditions": {
            "soil_temperature_c": 15,
            "frost_risk": 0.05,
            "rainfall_outlook_mm": 24,
        },
        "readiness": {
            "soil_fit": True,
            "fertility_ready": True,
            "equipment_ready": True,
            "crew_assigned": True,
            "irrigation_ready": True,
        },
    }
    payload.update(overrides)
    return payload


def test_record_crop_plan_accepts_optimal_window_and_updates_workbench():
    state = agriculture_farm_operations_empty_state()

    decision = agriculture_farm_operations_record_crop_plan(state, _base_payload())

    assert decision["ok"] is True
    assert decision["accepted"] is True
    assert decision["plan"]["status"] == "planned"
    assert decision["plan"]["planting_window"]["status"] == "optimal"
    assert decision["state"]["outbox"][-1]["event_type"] == "AgricultureFarmOperationsCreated"

    workbench = agriculture_farm_operations_query_workbench(decision["state"])

    assert len(workbench["crop_plans"]) == 1
    assert workbench["crop_plan_summary"]["accepted_count"] == 1
    assert workbench["crop_plan_summary"]["window_status_counts"]["optimal"] == 1


def test_record_crop_plan_blocks_overlapping_active_plan_on_same_zone():
    state = agriculture_farm_operations_empty_state()
    first = agriculture_farm_operations_record_crop_plan(state, _base_payload())

    second = agriculture_farm_operations_record_crop_plan(
        first["state"],
        _base_payload(
            plan_id="maize-overlap",
            crop="soybean",
            planting_date="2026-04-28",
            planned_start="2026-04-28",
            planned_end="2026-09-01",
        ),
    )

    assert second["ok"] is False
    assert second["accepted"] is False
    assert second["conflicts"][0]["reason_code"] == "overlapping_active_crop_plan"
    assert second["exception"]["exception_code"] == "crop_plan_blocked"
    assert second["state"]["outbox"][-1]["event_type"] == "AgricultureFarmOperationsExceptionOpened"
    assert len(second["state"]["crop_plans"]) == 1
    assert len(second["state"]["planning_exceptions"]) == 1


def test_record_crop_plan_allows_replant_linkage_and_replaces_prior_plan():
    state = agriculture_farm_operations_empty_state()
    first = agriculture_farm_operations_record_crop_plan(state, _base_payload(plan_id="plan-original"))

    replant = agriculture_farm_operations_record_crop_plan(
        first["state"],
        _base_payload(
            plan_id="plan-replant",
            replant_of="plan-original",
            previous_crop="maize",
            planting_date="2026-05-02",
            planned_start="2026-05-02",
            planned_end="2026-09-20",
        ),
    )

    assert replant["ok"] is True
    assert replant["accepted"] is True
    assert replant["plan"]["replant_of"] == "plan-original"
    assert replant["state"]["crop_plans"]["plan-original"]["status"] == "replaced_by_replant"
    assert replant["state"]["crop_plans"]["plan-original"]["replaced_by_replant"] == "plan-replant"


def test_record_crop_plan_blocks_when_readiness_and_window_thresholds_fail():
    state = agriculture_farm_operations_empty_state()

    decision = agriculture_farm_operations_record_crop_plan(
        state,
        _base_payload(
            conditions={
                "soil_temperature_c": 9,
                "frost_risk": 0.3,
                "rainfall_outlook_mm": 8,
            },
            readiness={
                "soil_fit": True,
                "fertility_ready": False,
                "equipment_ready": True,
                "crew_assigned": False,
                "irrigation_ready": False,
            },
        ),
    )

    assert decision["ok"] is False
    assert decision["accepted"] is False
    assert "missing_fertility_ready" in decision["plan"]["readiness"]["blockers"]
    assert "missing_crew_assigned" in decision["plan"]["readiness"]["blockers"]
    assert "soil_temperature_below_threshold" in decision["plan"]["readiness"]["blockers"]
    assert "frost_risk_above_threshold" in decision["plan"]["readiness"]["blockers"]
    assert "dry_outlook_without_irrigation" in decision["plan"]["readiness"]["blockers"]


def test_service_record_crop_plan_returns_real_planning_preview():
    service = AgricultureFarmOperationsService()

    preview = service.record_crop_plan(_base_payload())

    assert preview["ok"] is True
    assert preview["planning_preview"]["plan"]["planting_window"]["status"] == "optimal"
    assert preview["planning_preview"]["plan"]["readiness"]["status"] == "ready"
    assert preview["operation_contract"]["owned_tables"] == ("agriculture_farm_operations_crop_plan",)


def test_crop_plan_operation_is_advertised_in_runtime_contracts():
    service_contract = agriculture_farm_operations_build_service_contract()
    release = agriculture_farm_operations_build_release_evidence()

    assert "record_crop_plan" in service_contract["command_methods"]
    assert any(check["id"] == "crop_plan_execution" and check["ok"] for check in release["checks"])
    assert "record_crop_plan" in service_operation_manifest()["command_operations"]
