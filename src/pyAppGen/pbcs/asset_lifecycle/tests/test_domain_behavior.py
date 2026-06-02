"""Domain behavior tests for the asset_lifecycle PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from ..repository import AssetLifecycleStandaloneRepository
from ..repository import standalone_repository_smoke_test
from ..services import AssetLifecycleService
from ..services import service_operation_manifest
from ..ui import asset_lifecycle_form_contracts
from ..ui import asset_lifecycle_render_workbench
from ..ui import asset_lifecycle_standalone_workbench_blueprint
from ..ui import asset_lifecycle_ui_contract
from ..standalone import asset_lifecycle_standalone_app_smoke
from ..standalone import standalone_release_snapshot
from ..ui import asset_lifecycle_wizard_contracts


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 2,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "default_book": "corporate",
    "workbench_limit": 100,
}


def configured_state() -> dict:
    state = runtime.asset_lifecycle_empty_state()
    state = runtime.asset_lifecycle_configure_runtime(state, CONFIGURATION)["state"]
    for key, value in (
        ("capitalization_threshold", 2500),
        ("impairment_indicator_threshold", 0.65),
        ("physical_verification_interval_days", 365),
        ("depreciation_batch_size", 500),
        ("retirement_approval_limit", 10000),
        ("workbench_limit", 100),
    ):
        state = runtime.asset_lifecycle_set_parameter(state, key, value)["state"]
    state = runtime.asset_lifecycle_register_rule(
        state,
        {
            "rule_id": "asset-capitalization-policy",
            "tenant": "tenant_asset",
            "scope": "capitalization",
            "threshold": 2500,
            "controlled_classes": ("manufacturing_equipment",),
            "status": "active",
        },
    )["state"]
    return state


def asset_payload(asset_id: str = "asset-001", *, cost: float = 12000.0) -> dict:
    return {
        "asset_id": asset_id,
        "tenant": "tenant_asset",
        "legal_entity": "ManufacturingCo US",
        "description": "CNC milling center",
        "category": "manufacturing_equipment",
        "cost": cost,
        "residual_value": 2000.0,
        "useful_life_months": 60,
        "book": "corporate",
        "location": "plant-a",
        "custodian": "ops_manager",
        "cost_center": "production",
        "components": (
            {"component_id": f"{asset_id}-spindle", "component_name": "spindle", "capitalization_split": 0.35},
            {"component_id": f"{asset_id}-controller", "component_name": "controller", "capitalization_split": 0.25},
        ),
        "identity": {"did": f"did:appgen:{asset_id}", "issuer": "asset_registry", "status": "active"},
        "acquisition": {"receipt_id": "receipt-001", "supplier_invoice": "sup-inv-001", "cip_project": "cip-line-1"},
    }


def asset_service() -> AssetLifecycleService:
    return AssetLifecycleService(configured_state())


def register_service_and_schedule(service: AssetLifecycleService) -> dict:
    registered = service.command_assets({"asset": asset_payload()})
    placed = service.command_assets_asset_id_service({"asset_id": "asset-001", "service_date": "2026-01-01"})
    schedule = service.command_assets_asset_id_depreciation_schedules({"asset_id": "asset-001", "method": "straight_line"})
    assert registered["ok"] is True
    assert placed["asset"]["status"] == "in_service"
    assert schedule["ok"] is True
    return schedule


def test_asset_acquisition_service_depreciation_and_idempotent_run_lifecycle():
    service = asset_service()
    schedule = register_service_and_schedule(service)
    plan = service.preview_depreciation_plan({"asset": asset_payload("asset-preview"), "method": "straight_line"})
    run = service.command_depreciation_runs({"run_id": "dep-run-001", "period": "2026-01"})
    duplicate = service.command_depreciation_runs({"run_id": "dep-run-001", "period": "2026-01"})
    review = runtime.asset_lifecycle_review_depreciation_plan(service.state, "asset-001")
    assets = service.query_assets({"tenant": "tenant_asset"})
    risk = service.query_assets_asset_id_risk({"asset_id": "asset-001", "operating_hours": 1600, "maintenance_score": 0.9})

    assert schedule["schedule"]["version"] == 1
    assert schedule["schedule"]["revision_reason"] == "initial_build"
    assert plan["ok"] is True
    assert run["ok"] is True
    assert run["duplicate"] is False
    assert run["run"]["status"] == "posted"
    assert run["run"]["calculated_total"] > 0
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert duplicate["idempotency_key"] == run["idempotency_key"]
    assert service.state["assets"]["asset-001"]["accumulated_depreciation"] == run["run"]["calculated_total"]
    assert review["latest_run_id"] == "dep-run-001"
    assert review["active_version"] == 1
    assert assets["count"] == 1
    assert risk["risk_score"] < 0.3
    assert {event["event_type"] for event in service.state["outbox"]} >= {
        "AssetRegistered",
        "AssetPlacedInService",
        "DepreciationCalculated",
    }


def test_asset_transfer_valuation_maintenance_revision_and_retirement_execute():
    service = asset_service()
    register_service_and_schedule(service)
    service.command_depreciation_runs({"run_id": "dep-run-001", "period": "2026-01"})
    transfer = service.command_assets_asset_id_transfers(
        {"asset_id": "asset-001", "location": "plant-b", "cost_center": "maintenance", "approved_by": "controller"}
    )
    revaluation = service.command_assets_asset_id_revaluations(
        {"asset_id": "asset-001", "fair_value": 13000.0, "approved_by": "controller"}
    )
    impairment = service.command_assets_asset_id_impairments(
        {"asset_id": "asset-001", "recoverable_amount": 9000.0, "approved_by": "controller"}
    )
    maintenance = service.command_assets_asset_id_maintenance_adjustments(
        {"asset_id": "asset-001", "useful_life_delta_months": 6, "evidence": "major_overhaul_completed"}
    )
    revision = service.command_assets_asset_id_depreciation_schedules({"asset_id": "asset-001", "method": "straight_line"})
    projection = runtime.asset_lifecycle_project_asset_valuation(service.state, "asset-001", periods=3)
    impairment_recommendation = runtime.asset_lifecycle_recommend_impairment(service.state, "asset-001", market_indicator=0.6)
    journal_route = runtime.asset_lifecycle_route_depreciation_journal(
        service.state["depreciation_runs"]["dep-run-001"]["journals"],
        rails=({"route": "ledger_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}),
    )
    retirement = service.command_assets_asset_id_retirements(
        {"asset_id": "asset-001", "proceeds": 2500.0, "approved_by": "controller"}
    )
    workbench = runtime.asset_lifecycle_build_workbench_view(service.state, tenant="tenant_asset")

    assert transfer["asset"]["location"] == "plant-b"
    assert transfer["asset"]["cost_center"] == "maintenance"
    assert revaluation["asset"]["book_value"] == 13000.0
    assert impairment["impairment"] == 4000.0
    assert maintenance["asset"]["useful_life_months"] == 66
    assert maintenance["asset"]["schedule_revision_required"] is True
    assert revision["schedule"]["version"] == 2
    assert revision["schedule"]["revision_reason"] == "life_change"
    assert projection["projected_values"][0]["book_value"] < service.state["assets"]["asset-001"]["book_value"]
    assert impairment_recommendation["decision"] == "impair"
    assert journal_route["route"] == "outbox"
    assert journal_route["failover_used"] is True
    assert retirement["asset"]["status"] == "retired"
    assert retirement["asset"]["disposal_gain_loss"] == -6500.0
    assert workbench["retired_count"] == 1
    assert workbench["active_schedule_versions"]["asset-001"] == 2


def test_asset_advanced_controls_federation_identity_ui_and_portfolio_are_executable():
    service = asset_service()
    register_service_and_schedule(service)
    service.command_depreciation_runs({"run_id": "dep-run-001", "period": "2026-01"})
    parsed = runtime.asset_lifecycle_parse_capitalization_document("cost 12000 life 60 component spindle component controller")
    insurance = runtime.asset_lifecycle_integrate_insurance_warranty(
        service.state,
        "asset-001",
        policy={"policy_id": "policy-asset-001", "coverage": 15000.0, "warranty_months": 24},
    )
    federation = runtime.asset_lifecycle_federate_asset_view(service.state, "asset-001", external_systems=("maintenance", "ledger"))
    identity = runtime.asset_lifecycle_verify_asset_identity({"did": "did:appgen:asset-001", "issuer": "asset_registry", "status": "active"})
    audit = runtime.asset_lifecycle_generate_asset_audit_proof(
        service.state,
        "asset-001",
        disclosure=("asset_id", "status", "book_value", "location"),
    )
    policy = runtime.asset_lifecycle_screen_asset_policy(service.state, "asset-001", restricted_locations=("restricted-yard",))
    controls = runtime.asset_lifecycle_run_control_tests(service.state)
    resilience = runtime.asset_lifecycle_run_resilience_drill(service.state, "depreciation_worker_failure")
    crypto = runtime.asset_lifecycle_rotate_crypto_epoch(service.state, "dilithium3")
    carbon = runtime.asset_lifecycle_schedule_carbon_aware_utilization(
        ({"window": "day", "carbon_intensity": 0.44}, {"window": "night", "carbon_intensity": 0.18})
    )
    portfolio = runtime.asset_lifecycle_optimize_asset_portfolio(
        (
            {"asset_id": "asset-001", "value": 9000.0, "risk": 0.12, "utilization": 0.85},
            {"asset_id": "asset-002", "value": 2500.0, "risk": 0.35, "utilization": 0.2},
        )
    )
    allocation = runtime.asset_lifecycle_allocate_shared_asset(
        requests=({"team": "ops", "hours": 20.0, "bid": 8.0}, {"team": "quality", "hours": 10.0, "bid": 6.0}),
        available_hours=30.0,
    )
    anomaly = runtime.asset_lifecycle_detect_asset_anomaly(service.state)
    invariants = runtime.asset_lifecycle_verify_formal_invariants(service.state)
    governed = runtime.asset_lifecycle_register_governed_model(
        "asset_lifecycle_risk_model",
        {"auc": 0.9, "drift_score": 0.04, "features": ("age", "maintenance", "utilization")},
    )
    ui_contract = asset_lifecycle_ui_contract()
    rendered = asset_lifecycle_render_workbench(
        service.state,
        tenant="tenant_asset",
        principal_permissions=tuple(set(ui_contract["action_permissions"].values())),
    )
    forms = asset_lifecycle_form_contracts()
    wizards = asset_lifecycle_wizard_contracts()
    blueprint = asset_lifecycle_standalone_workbench_blueprint()

    assert parsed["cost"] == 12000.0
    assert parsed["components"] == ("spindle", "controller")
    assert insurance["insured_value"] == 15000.0
    assert federation["systems"] == ("maintenance", "ledger")
    assert identity["ok"] is True
    assert audit["proof"].startswith("zk_asset_")
    assert policy["decision"] == "clear"
    assert controls["hash_chain_valid"] is True
    assert resilience["decision"] == "self_healed"
    assert crypto["algorithm"] == "dilithium3"
    assert carbon["selected_window"] == "night"
    assert portfolio["selected_asset"] == "asset-001"
    assert allocation["ok"] is True
    assert anomaly["ok"] is True
    assert invariants["ok"] is True
    assert governed["ok"] is True
    assert rendered["ok"] is True
    assert "AssetLifecycleWorkbench" in rendered["fragments"]
    assert forms["ok"] is True
    assert "AssetRegisterForm" in tuple(form["key"] for form in forms["contracts"])
    assert wizards["ok"] is True
    assert "DepreciationRunWizard" in tuple(wizard["key"] for wizard in wizards["contracts"])
    assert blueprint["ok"] is True



def test_asset_routes_repository_agent_standalone_and_release_surfaces_are_executable():
    service = asset_service()
    register_service_and_schedule(service)
    service.command_depreciation_runs({"run_id": "dep-run-surface", "period": "2026-02"})

    route_validation = routes.validate_api_route_contracts()
    route_dispatch = routes.dispatch_route(
        "POST",
        "/api/pbc/asset_lifecycle/assets",
        {"asset": asset_payload("asset-route-001", cost=9000.0)},
    )
    standalone_routes = routes.standalone_route_contracts()
    standalone_seed = routes.dispatch_standalone_route(
        "POST",
        "/app/asset-lifecycle/demo-workspace",
        {"tenant": "tenant_demo"},
    )
    skills = agent.agent_skill_manifest()
    workspace = agent.standalone_agent_workspace_contract()
    document_plan = agent.document_instruction_plan(
        "Capitalization packet for CNC equipment with maintenance overhaul evidence.",
        "Create asset, place in service, revise depreciation schedule, and generate audit proof.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        table="asset_lifecycle_fixed_asset",
        payload={"asset_id": "asset-agent", "cost": 12000.0},
    )
    blocked_crud = agent.datastore_crud_plan("update", table="gl_core_journal_entry", payload={"journal_id": "bad"})
    contribution = agent.composed_agent_contribution()
    depreciation_preview = agent.depreciation_revision_preview(
        {
            "asset": {
                "asset_id": "asset-preview-surface",
                "cost": 10000.0,
                "book_value": 10000.0,
                "residual_value": 1000.0,
                "useful_life_months": 36,
                "service_date": "2026-01-01",
            },
            "method": "straight_line",
        }
    )

    repository = AssetLifecycleStandaloneRepository()
    try:
        migrations = repository.apply_migrations()
        repository.configure_runtime("tenant_asset", CONFIGURATION)
        for key, value in (
            ("capitalization_threshold", 2500),
            ("impairment_indicator_threshold", 0.65),
            ("physical_verification_interval_days", 365),
            ("depreciation_batch_size", 500),
            ("retirement_approval_limit", 10000),
            ("workbench_limit", 100),
        ):
            repository.set_parameter("tenant_asset", key, value)
        repository.register_rule(
            "tenant_asset",
            {
                "rule_id": "asset-capitalization-policy",
                "tenant": "tenant_asset",
                "scope": "capitalization",
                "threshold": 2500,
                "controlled_classes": ("manufacturing_equipment",),
                "status": "active",
            },
        )
        registered = repository.register_asset("tenant_asset", asset_payload("asset-repo-001"))
        placed = repository.place_asset_in_service("tenant_asset", "asset-repo-001", "2026-01-01")
        scheduled = repository.build_depreciation_schedule("tenant_asset", "asset-repo-001")
        dep_run = repository.run_depreciation("tenant_asset", "dep-repo-001", "2026-01")
        proof = repository.generate_asset_audit_proof("tenant_asset", "asset-repo-001", ("asset_id", "status", "book_value"))
        agent_run = repository.run_agent_skill(
            "tenant_asset",
            "asset_lifecycle.document_instruction_intake",
            {"document": "capitalization packet", "instructions": "revise depreciation", "scope": "asset"},
        )
        workbench = repository.build_workbench("tenant_asset")
        read_model = repository.read_model("tenant_asset")
        counts = repository.activity_counts("tenant_asset")
    finally:
        repository.close()

    repo_smoke = standalone_repository_smoke_test()
    standalone_smoke = asset_lifecycle_standalone_app_smoke()
    release_snapshot = standalone_release_snapshot()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()

    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert all(contract["shared_table_access"] is False for contract in route_validation["contracts"])
    assert route_dispatch["ok"] is True
    assert route_dispatch["result"]["asset"]["status"] == "registered"
    assert route_dispatch["side_effects"] == ()
    assert standalone_routes["ok"] is True
    assert standalone_seed["ok"] is True
    assert skills["ok"] is True
    assert workspace["ok"] is True
    assert document_plan["ok"] is True
    assert "AssetCapitalizationWizard" in document_plan["wizard_candidates"]
    assert crud_plan["ok"] is True
    assert crud_plan["requires_confirmation"] is True
    assert crud_plan["event_contract"] == "AppGen-X"
    assert blocked_crud["ok"] is False
    assert contribution["ok"] is True
    assert "asset_lifecycle_crud" in contribution["dsl_tools"]
    assert depreciation_preview["ok"] is True
    assert set(migrations) >= {"asset_lifecycle_runtime_state", "asset_lifecycle_workbench_read_model"}
    assert registered["asset"]["asset_id"] == "asset-repo-001"
    assert placed["asset"]["status"] == "in_service"
    assert scheduled["schedule"]["version"] == 1
    assert dep_run["run"]["status"] == "posted"
    assert proof["ok"] is True
    assert agent_run["ok"] is True
    assert workbench["ok"] is True
    assert read_model["ok"] is True
    assert counts["forms"] >= 4
    assert counts["workflows"] >= 3
    assert counts["agent_sessions"] == 1
    assert repo_smoke["ok"] is True
    assert standalone_smoke["ok"] is True
    assert release_snapshot["ok"] is True
    assert release_validation["ok"] is True
    assert release_smoke["ok"] is True


def test_asset_events_retry_dead_letter_manifest_and_configuration_guards():
    service = asset_service()
    processed = service.command_assets_events_inbox(
        {
            "event": {
                "event_id": "purchase-cap-evt-001",
                "event_type": "PurchaseReceiptCapitalized",
                "payload": {"tenant": "tenant_asset", "receipt_id": "receipt-001", "asset_id": "asset-001", "amount": 12000.0},
            }
        }
    )
    duplicate = service.command_assets_events_inbox(
        {
            "event": {
                "event_id": "purchase-cap-evt-001",
                "event_type": "PurchaseReceiptCapitalized",
                "payload": {"tenant": "tenant_asset", "receipt_id": "receipt-001", "asset_id": "asset-001"},
            }
        }
    )
    retrying = service.command_assets_events_inbox(
        {"event": {"event_id": "bad-asset-event", "event_type": "UnknownInboundEvent", "attempts": 1, "payload": {"tenant": "tenant_asset"}}}
    )
    dead_letter = service.command_assets_events_inbox(
        {"event": {"event_id": "bad-asset-event", "event_type": "UnknownInboundEvent", "attempts": 2, "payload": {"tenant": "tenant_asset"}}}
    )
    manifest = service_operation_manifest()

    assert processed["handler"]["status"] == "processed"
    assert "asset-001" in service.state["projections"]["purchase_receipts"]
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_lettered"
    assert len(service.state["dead_letter"]) == 1
    assert manifest["event_contract"]["contract"] == "appgen_event_contract"
    assert {"command_assets", "command_depreciation_runs", "query_assets_asset_id_risk"} <= set(manifest["operations"])

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.asset_lifecycle_configure_runtime(runtime.asset_lifecycle_empty_state(), {**CONFIGURATION, "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X"):
        runtime.asset_lifecycle_configure_runtime(runtime.asset_lifecycle_empty_state(), {**CONFIGURATION, "stream_engine_picker": "kafka"})
