from pyAppGen.pbc import ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import asset_lifecycle_build_depreciation_schedule
from pyAppGen.pbc import asset_lifecycle_build_workbench_view
from pyAppGen.pbc import asset_lifecycle_empty_state
from pyAppGen.pbc import asset_lifecycle_place_asset_in_service
from pyAppGen.pbc import asset_lifecycle_register_asset
from pyAppGen.pbc import asset_lifecycle_retire_asset
from pyAppGen.pbc import asset_lifecycle_run_depreciation
from pyAppGen.pbc import asset_lifecycle_runtime_capabilities
from pyAppGen.pbc import asset_lifecycle_runtime_smoke
from pyAppGen.pbc import asset_lifecycle_transfer_asset
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_asset_lifecycle_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = asset_lifecycle_runtime_capabilities()
    smoke = asset_lifecycle_runtime_smoke()

    assert runtime["format"] == "appgen.asset-lifecycle-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/asset_lifecycle"
    assert len(runtime["standard_features"]) >= 18
    assert smoke["ok"] is True
    assert set(ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("asset_lifecycle")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(ASSET_LIFECYCLE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("asset_lifecycle",))["ok"] is True
    assert pbc_implemented_capability_audit(("asset_lifecycle",))["ok"] is True


def test_asset_lifecycle_runtime_handles_core_fixed_asset_workflows() -> None:
    state = asset_lifecycle_empty_state()
    state = asset_lifecycle_register_asset(
        state,
        {
            "asset_id": "asset_ops",
            "tenant": "tenant_ops",
            "legal_entity": "entity_ops",
            "description": "Packaging Robot",
            "category": "equipment",
            "cost": 6000,
            "residual_value": 600,
            "currency": "USD",
            "book": "corporate",
            "useful_life_months": 36,
            "location": "plant_1",
            "custodian": "ops_manager",
            "cost_center": "manufacturing",
            "components": ("arm", "controller"),
            "identity": {"did": "did:appgen:asset-ops", "issuer": "asset_registry", "status": "active"},
        },
    )["state"]
    state = asset_lifecycle_place_asset_in_service(state, "asset_ops", service_date="2026-05-26")["state"]

    schedule = asset_lifecycle_build_depreciation_schedule(state, "asset_ops", method="straight_line")
    state = schedule["state"]
    assert schedule["schedule"]["lines"][0]["amount"] == 150

    depreciation = asset_lifecycle_run_depreciation(state, run_id="dep_ops", period="2026-06")
    state = depreciation["state"]
    assert depreciation["journals"][0]["amount"] == 150
    assert state["assets"]["asset_ops"]["book_value"] == 5850
    assert state["outbox"][-1]["idempotency_key"] == "asset_lifecycle:DepreciationCalculated:asset_evt_000003"

    state = asset_lifecycle_transfer_asset(
        state,
        "asset_ops",
        location="plant_2",
        cost_center="maintenance",
        approved_by="controller",
    )["state"]
    assert state["assets"]["asset_ops"]["location"] == "plant_2"
    assert state["assets"]["asset_ops"]["cost_center"] == "maintenance"

    retirement = asset_lifecycle_retire_asset(state, "asset_ops", proceeds=5000, approved_by="controller")
    state = retirement["state"]
    assert retirement["asset"]["status"] == "retired"
    assert retirement["asset"]["disposal_gain_loss"] == -850

    workbench = asset_lifecycle_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["asset_count"] == 1
    assert workbench["retired_count"] == 1
