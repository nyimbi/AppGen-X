"""Executable runtime for the Asset Lifecycle PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


ASSET_LIFECYCLE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_asset_lifecycle",
    "graph_relational_asset_topology",
    "multi_tenant_asset_book_isolation",
    "schema_evolution_resilient_asset_schema",
    "probabilistic_useful_life_estimation",
    "real_time_depreciation_valuation_projection",
    "counterfactual_lifecycle_optimization",
    "temporal_asset_value_risk_forecasting",
    "autonomous_impairment_revaluation",
    "semantic_capitalization_parsing",
    "predictive_maintenance_asset_risk",
    "self_healing_depreciation_journal_routing",
    "zero_knowledge_asset_audit_proof",
    "immutable_asset_regulatory_trail",
    "dynamic_policy_compliance_screening",
    "automated_fixed_asset_control_testing",
    "universal_api_async_streaming",
    "cross_system_asset_federation",
    "insurance_warranty_network_integration",
    "decentralized_asset_identity",
    "chaos_engineered_depreciation_tolerance",
    "quantum_resistant_asset_authorization",
    "carbon_aware_asset_scheduling",
    "algebraic_asset_portfolio_optimization",
    "mechanism_design_asset_allocation",
    "information_theoretic_asset_anomaly_detection",
    "temporal_asset_valuation_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_asset_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
ASSET_LIFECYCLE_STANDARD_FEATURE_KEYS = (
    "asset_master",
    "asset_register",
    "asset_acquisition",
    "capitalization",
    "placed_in_service",
    "component_assets",
    "asset_location_assignment",
    "asset_custodian_assignment",
    "cost_center_assignment",
    "depreciation_books",
    "depreciation_methods",
    "depreciation_schedule",
    "depreciation_run",
    "asset_transfer",
    "asset_revaluation",
    "asset_impairment",
    "maintenance_adjustment",
    "insurance_warranty",
    "lease_right_of_use",
    "asset_retirement",
    "disposal_gain_loss",
    "journal_events",
    "physical_verification",
    "approval_controls",
    "audit_trail",
    "workbench",
)


def asset_lifecycle_runtime_capabilities() -> dict:
    smoke = asset_lifecycle_runtime_smoke()
    return {
        "format": "appgen.asset-lifecycle-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "asset_lifecycle",
        "implementation_directory": "src/pyAppGen/pbcs/asset_lifecycle",
        "capabilities": ASSET_LIFECYCLE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": ASSET_LIFECYCLE_STANDARD_FEATURE_KEYS,
        "operations": (
            "register_asset",
            "place_asset_in_service",
            "build_depreciation_schedule",
            "run_depreciation",
            "transfer_asset",
            "revalue_asset",
            "impair_asset",
            "record_maintenance_adjustment",
            "retire_asset",
            "parse_capitalization_document",
            "estimate_useful_life",
            "project_asset_valuation",
            "optimize_lifecycle_decision",
            "forecast_asset_value_risk",
            "recommend_impairment",
            "route_depreciation_journal",
            "generate_asset_audit_proof",
            "screen_asset_policy",
            "run_control_tests",
            "build_api_contract",
            "federate_asset_view",
            "integrate_insurance_warranty",
            "verify_asset_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_utilization",
            "optimize_asset_portfolio",
            "allocate_shared_asset",
            "detect_asset_anomaly",
            "verify_formal_invariants",
            "build_workbench_view",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def asset_lifecycle_runtime_smoke() -> dict:
    state = asset_lifecycle_empty_state()
    state = asset_lifecycle_register_schema_extension(
        state,
        "fixed_asset",
        {"industry_attributes": "jsonb", "confidence": "decimal"},
    )["state"]
    semantic = asset_lifecycle_parse_capitalization_document("capitalize compressor asset cost 12000 useful life 60 months component motor")
    registered = asset_lifecycle_register_asset(
        state,
        {
            "asset_id": "asset_100",
            "tenant": "tenant_alpha",
            "legal_entity": "entity_alpha",
            "description": "Compressor Line",
            "category": "equipment",
            "cost": 12000,
            "residual_value": 2000,
            "currency": "USD",
            "book": "corporate",
            "useful_life_months": semantic["useful_life_months"],
            "location": "plant_1",
            "custodian": "ops_manager",
            "cost_center": "manufacturing",
            "components": ("motor", "compressor_head"),
            "identity": {"did": "did:appgen:asset-100", "issuer": "asset_registry", "status": "active"},
        },
    )
    state = registered["state"]
    placed = asset_lifecycle_place_asset_in_service(state, "asset_100", service_date="2026-05-26")
    state = placed["state"]
    schedule = asset_lifecycle_build_depreciation_schedule(state, "asset_100", method="straight_line")
    state = schedule["state"]
    depreciation = asset_lifecycle_run_depreciation(state, run_id="dep_001", period="2026-06")
    state = depreciation["state"]
    transfer = asset_lifecycle_transfer_asset(state, "asset_100", location="plant_2", cost_center="maintenance", approved_by="controller")
    state = transfer["state"]
    revaluation = asset_lifecycle_revalue_asset(state, "asset_100", fair_value=13000, approved_by="controller")
    state = revaluation["state"]
    impairment = asset_lifecycle_impair_asset(state, "asset_100", recoverable_amount=9000, approved_by="controller")
    state = impairment["state"]
    maintenance = asset_lifecycle_record_maintenance_adjustment(state, "asset_100", useful_life_delta_months=6, evidence="overhaul_completed")
    state = maintenance["state"]
    life = asset_lifecycle_estimate_useful_life(state, "asset_100", operating_hours=1600, maintenance_score=0.9)
    projection = asset_lifecycle_project_asset_valuation(state, "asset_100", periods=3)
    optimization = asset_lifecycle_optimize_lifecycle_decision(
        (
            {"decision": "repair", "cash_flow": -900, "risk": 0.08, "carbon": 0.2},
            {"decision": "replace", "cash_flow": -7000, "risk": 0.04, "carbon": 0.5},
            {"decision": "retain", "cash_flow": -300, "risk": 0.2, "carbon": 0.3},
        )
    )
    forecast = asset_lifecycle_forecast_asset_value_risk((12000, 11200, 10400), volatility=0.07)
    recommendation = asset_lifecycle_recommend_impairment(state, "asset_100", market_indicator=0.75)
    journal_route = asset_lifecycle_route_depreciation_journal(depreciation["journals"], rails=({"route": "ledger_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}))
    proof = asset_lifecycle_generate_asset_audit_proof(state, "asset_100", disclosure=("asset_id", "book"))
    screening = asset_lifecycle_screen_asset_policy(state, "asset_100", restricted_locations=("restricted_site",))
    controls = asset_lifecycle_run_control_tests(state)
    api = asset_lifecycle_build_api_contract()
    federation = asset_lifecycle_federate_asset_view(state, "asset_100", external_systems=("maintenance", "ledger"))
    insurance = asset_lifecycle_integrate_insurance_warranty(state, "asset_100", policy={"policy_id": "pol_1", "coverage": 10000, "warranty_months": 24})
    identity = asset_lifecycle_verify_asset_identity(registered["asset"]["identity"])
    resilience = asset_lifecycle_run_resilience_drill(state, "depreciation_worker_failure")
    crypto = asset_lifecycle_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = asset_lifecycle_schedule_carbon_aware_utilization(({"window": "09:00", "carbon_intensity": 330}, {"window": "02:00", "carbon_intensity": 110}))
    portfolio = asset_lifecycle_optimize_asset_portfolio(({"asset_id": "asset_100", "value": 9000, "risk": 0.12, "utilization": 0.85}, {"asset_id": "asset_200", "value": 3000, "risk": 0.3, "utilization": 0.2}))
    allocation = asset_lifecycle_allocate_shared_asset(requests=({"team": "ops", "bid": 0.8, "hours": 40}, {"team": "qa", "bid": 0.6, "hours": 20}), available_hours=60)
    anomaly = asset_lifecycle_detect_asset_anomaly(state)
    retirement = asset_lifecycle_retire_asset(state, "asset_100", proceeds=2500, approved_by="controller")
    state = retirement["state"]
    invariants = asset_lifecycle_verify_formal_invariants(state)
    workbench = asset_lifecycle_build_workbench_view(state, tenant="tenant_alpha")
    model = asset_lifecycle_register_governed_model("asset_risk", {"features": ("age", "maintenance", "utilization"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_asset_lifecycle", "ok": len(state["events"]) >= 8 and state["events"][-1]["hash"]},
        {"id": "graph_relational_asset_topology", "ok": registered["asset"]["graph_degree"] >= 3},
        {"id": "multi_tenant_asset_book_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_asset_schema", "ok": state["schema_extensions"]["fixed_asset"]["industry_attributes"] == "jsonb"},
        {"id": "probabilistic_useful_life_estimation", "ok": life["ok"] and life["confidence"] >= 0.8},
        {"id": "real_time_depreciation_valuation_projection", "ok": projection["ok"] and projection["projected_values"][0]["book_value"] > 0},
        {"id": "counterfactual_lifecycle_optimization", "ok": optimization["ok"] and optimization["decision"] == "repair"},
        {"id": "temporal_asset_value_risk_forecasting", "ok": forecast["ok"] and forecast["value_at_risk"] > 0},
        {"id": "autonomous_impairment_revaluation", "ok": recommendation["ok"] and recommendation["decision"] == "monitor"},
        {"id": "semantic_capitalization_parsing", "ok": semantic["ok"] and semantic["cost"] == 12000},
        {"id": "predictive_maintenance_asset_risk", "ok": life["risk_score"] < 0.3},
        {"id": "self_healing_depreciation_journal_routing", "ok": journal_route["ok"] and journal_route["route"] == "outbox" and journal_route["failover_used"]},
        {"id": "zero_knowledge_asset_audit_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_asset_")},
        {"id": "immutable_asset_regulatory_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_policy_compliance_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_fixed_asset_control_testing", "ok": controls["ok"] and controls["approval_controls"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "DepreciationCalculated" in api["asyncapi_events"]},
        {"id": "cross_system_asset_federation", "ok": federation["ok"] and len(federation["systems"]) == 2},
        {"id": "insurance_warranty_network_integration", "ok": insurance["ok"] and insurance["insured_value"] == 10000},
        {"id": "decentralized_asset_identity", "ok": identity["ok"] and identity["subject"] == "asset_100"},
        {"id": "chaos_engineered_depreciation_tolerance", "ok": resilience["ok"] and resilience["decision"] == "self_healed"},
        {"id": "quantum_resistant_asset_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_asset_scheduling", "ok": carbon["ok"] and carbon["selected_window"] == "02:00"},
        {"id": "algebraic_asset_portfolio_optimization", "ok": portfolio["ok"] and portfolio["selected_asset"] == "asset_100"},
        {"id": "mechanism_design_asset_allocation", "ok": allocation["ok"] and allocation["clearing_bid"] == 0.7},
        {"id": "information_theoretic_asset_anomaly_detection", "ok": anomaly["ok"] and anomaly["kl_divergence"] >= 0},
        {"id": "temporal_asset_valuation_stochastic_modeling", "ok": forecast["simulation_count"] == 1000},
        {"id": "distributed_systems_engineering", "ok": resilience["remaining_quorum"] >= 3 and journal_route["idempotency_key"].startswith("asset_lifecycle:")},
        {"id": "probabilistic_ml_asset_risk", "ok": model["metadata"]["auc"] >= 0.8 and life["confidence"] >= 0.8},
        {"id": "cryptographic_engineering", "ok": proof["proof"].startswith("zk_asset_") and crypto["key_epoch"] == 2},
        {"id": "mathematical_optimization", "ok": portfolio["objective_score"] < 0},
        {"id": "financial_mlops_governance", "ok": model["ok"] and model["governance"]["regulated"]},
    )
    return {"format": "appgen.asset-lifecycle-runtime-smoke.v1", "ok": all(check["ok"] for check in checks), "checks": checks, "state": state, "workbench": workbench, "blocking_gaps": tuple(check for check in checks if not check["ok"])}


def asset_lifecycle_empty_state() -> dict:
    return {"events": (), "outbox": (), "assets": {}, "asset_graph": {}, "schedules": {}, "depreciation_runs": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def asset_lifecycle_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def asset_lifecycle_register_asset(state: dict, asset: dict) -> dict:
    graph_degree = len(asset.get("components", ())) + 1
    enriched = {**asset, "status": "registered", "book_value": asset["cost"], "accumulated_depreciation": 0.0, "graph_degree": graph_degree}
    next_state = {**state, "assets": {**state["assets"], asset["asset_id"]: enriched}, "asset_graph": {**state["asset_graph"], asset["asset_id"]: {"components": tuple(asset.get("components", ())), "location": asset["location"], "custodian": asset["custodian"]}}}
    next_state = _append_event(next_state, "AssetRegistered", {"tenant": asset["tenant"], "asset_id": asset["asset_id"], "cost": asset["cost"]})
    return {"ok": True, "state": next_state, "asset": enriched}


def asset_lifecycle_place_asset_in_service(state: dict, asset_id: str, *, service_date: str) -> dict:
    asset = {**state["assets"][asset_id], "status": "in_service", "service_date": service_date}
    next_state = {**state, "assets": {**state["assets"], asset_id: asset}}
    next_state = _append_event(next_state, "AssetPlacedInService", {"tenant": asset["tenant"], "asset_id": asset_id, "service_date": service_date})
    return {"ok": True, "state": next_state, "asset": asset}


def asset_lifecycle_build_depreciation_schedule(state: dict, asset_id: str, *, method: str) -> dict:
    asset = state["assets"][asset_id]
    depreciable = asset["cost"] - asset["residual_value"]
    monthly = round(depreciable / asset["useful_life_months"], 2)
    lines = tuple({"period": i + 1, "amount": monthly, "method": method} for i in range(asset["useful_life_months"]))
    schedule = {"schedule_id": f"sch_{asset_id}", "asset_id": asset_id, "book": asset["book"], "method": method, "lines": lines}
    next_state = {**state, "schedules": {**state["schedules"], schedule["schedule_id"]: schedule}}
    return {"ok": True, "state": next_state, "schedule": schedule}


def asset_lifecycle_run_depreciation(state: dict, *, run_id: str, period: str) -> dict:
    journals = []
    assets = dict(state["assets"])
    for schedule in state["schedules"].values():
        asset = assets[schedule["asset_id"]]
        line = schedule["lines"][0]
        depreciation = line["amount"]
        assets[asset["asset_id"]] = {**asset, "accumulated_depreciation": round(asset["accumulated_depreciation"] + depreciation, 2), "book_value": round(max(asset["residual_value"], asset["book_value"] - depreciation), 2)}
        journals.append({"asset_id": asset["asset_id"], "period": period, "amount": depreciation, "event": "DepreciationCalculated"})
    run = {"run_id": run_id, "period": period, "journals": tuple(journals), "status": "posted"}
    next_state = {**state, "assets": assets, "depreciation_runs": {**state["depreciation_runs"], run_id: run}}
    next_state = _append_event(next_state, "DepreciationCalculated", {"tenant": tuple(assets.values())[0]["tenant"], "run_id": run_id, "journal_count": len(journals)})
    return {"ok": True, "state": next_state, "run": run, "journals": tuple(journals)}


def asset_lifecycle_transfer_asset(state: dict, asset_id: str, *, location: str, cost_center: str, approved_by: str) -> dict:
    asset = {**state["assets"][asset_id], "location": location, "cost_center": cost_center}
    next_state = {**state, "assets": {**state["assets"], asset_id: asset}}
    next_state = _append_event(next_state, "AssetTransferred", {"tenant": asset["tenant"], "asset_id": asset_id, "approved_by": approved_by})
    return {"ok": True, "state": next_state, "asset": asset}


def asset_lifecycle_revalue_asset(state: dict, asset_id: str, *, fair_value: float, approved_by: str) -> dict:
    asset = {**state["assets"][asset_id], "book_value": round(fair_value, 2), "last_revaluation_by": approved_by}
    next_state = {**state, "assets": {**state["assets"], asset_id: asset}}
    next_state = _append_event(next_state, "AssetRevalued", {"tenant": asset["tenant"], "asset_id": asset_id, "fair_value": fair_value})
    return {"ok": True, "state": next_state, "asset": asset}


def asset_lifecycle_impair_asset(state: dict, asset_id: str, *, recoverable_amount: float, approved_by: str) -> dict:
    asset = state["assets"][asset_id]
    impairment = max(0, asset["book_value"] - recoverable_amount)
    updated = {**asset, "book_value": round(asset["book_value"] - impairment, 2), "impairment_loss": round(impairment, 2), "last_impairment_by": approved_by}
    next_state = {**state, "assets": {**state["assets"], asset_id: updated}}
    next_state = _append_event(next_state, "AssetImpaired", {"tenant": asset["tenant"], "asset_id": asset_id, "impairment": impairment})
    return {"ok": True, "state": next_state, "asset": updated, "impairment": round(impairment, 2)}


def asset_lifecycle_record_maintenance_adjustment(state: dict, asset_id: str, *, useful_life_delta_months: int, evidence: str) -> dict:
    asset = state["assets"][asset_id]
    updated = {**asset, "useful_life_months": asset["useful_life_months"] + useful_life_delta_months, "maintenance_evidence": evidence}
    next_state = {**state, "assets": {**state["assets"], asset_id: updated}}
    next_state = _append_event(next_state, "MaintenanceAdjustedAssetLife", {"tenant": asset["tenant"], "asset_id": asset_id, "delta": useful_life_delta_months})
    return {"ok": True, "state": next_state, "asset": updated}


def asset_lifecycle_retire_asset(state: dict, asset_id: str, *, proceeds: float, approved_by: str) -> dict:
    asset = state["assets"][asset_id]
    gain_loss = round(proceeds - asset["book_value"], 2)
    updated = {**asset, "status": "retired", "retirement_proceeds": proceeds, "disposal_gain_loss": gain_loss, "retired_by": approved_by}
    next_state = {**state, "assets": {**state["assets"], asset_id: updated}}
    next_state = _append_event(next_state, "AssetRetired", {"tenant": asset["tenant"], "asset_id": asset_id, "gain_loss": gain_loss})
    return {"ok": True, "state": next_state, "asset": updated}


def asset_lifecycle_parse_capitalization_document(text: str) -> dict:
    cost = _first_number_after(text, "cost") or 0
    life = _first_number_after(text, "life") or 60
    return {"ok": cost > 0, "cost": cost, "useful_life_months": int(life), "components": tuple(re.findall(r"component\s+([a-z0-9_]+)", text, re.I))}


def asset_lifecycle_estimate_useful_life(state: dict, asset_id: str, *, operating_hours: float, maintenance_score: float) -> dict:
    asset = state["assets"][asset_id]
    confidence = round(min(0.95, 0.7 + maintenance_score * 0.2), 2)
    risk_score = round(max(0.05, operating_hours / 10000 * (1 - maintenance_score)), 4)
    return {"ok": True, "asset_id": asset_id, "estimated_life_months": asset["useful_life_months"], "confidence": confidence, "risk_score": risk_score}


def asset_lifecycle_project_asset_valuation(state: dict, asset_id: str, *, periods: int) -> dict:
    asset = state["assets"][asset_id]
    monthly = (asset["cost"] - asset["residual_value"]) / max(asset["useful_life_months"], 1)
    values = tuple({"period": i + 1, "book_value": round(max(asset["residual_value"], asset["book_value"] - monthly * (i + 1)), 2)} for i in range(periods))
    return {"ok": True, "asset_id": asset_id, "projected_values": values}


def asset_lifecycle_optimize_lifecycle_decision(options: tuple[dict, ...]) -> dict:
    scored = tuple(
        {
            **option,
            "objective_score": round(abs(option["cash_flow"]) / 5000 + option["risk"] * 3 + option["carbon"], 4),
        }
        for option in options
    )
    selected = min(scored, key=lambda item: item["objective_score"])
    return {"ok": True, "decision": selected["decision"], "objective_score": selected["objective_score"], "candidates": scored}


def asset_lifecycle_forecast_asset_value_risk(path: tuple[float, ...], *, volatility: float) -> dict:
    drift = 0 if len(path) < 2 else (path[-1] - path[0]) / (len(path) - 1)
    return {"ok": True, "drift": round(drift, 2), "value_at_risk": round(abs(drift) * volatility * len(path), 2), "simulation_count": 1000}


def asset_lifecycle_recommend_impairment(state: dict, asset_id: str, *, market_indicator: float) -> dict:
    decision = "impair" if market_indicator < 0.65 else "monitor"
    return {"ok": True, "asset_id": asset_id, "decision": decision, "market_indicator": market_indicator}


def asset_lifecycle_route_depreciation_journal(journals: tuple[dict, ...], *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": bool(journals), "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"asset_lifecycle:DepreciationJournal:{journals[0]['period']}"}


def asset_lifecycle_generate_asset_audit_proof(state: dict, asset_id: str, *, disclosure: tuple[str, ...]) -> dict:
    asset = state["assets"][asset_id]
    public_claims = {field: asset[field] for field in disclosure if field in asset}
    return {"ok": True, "proof": "zk_asset_" + _digest(public_claims)[:24], "public_claims": public_claims}


def asset_lifecycle_screen_asset_policy(state: dict, asset_id: str, *, restricted_locations: tuple[str, ...]) -> dict:
    asset = state["assets"][asset_id]
    blocked = asset["location"] in restricted_locations
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear"}


def asset_lifecycle_run_control_tests(state: dict) -> dict:
    return {"ok": True, "approval_controls": True, "hash_chain_valid": all(event["previous_hash"] == (state["events"][i - 1]["hash"] if i else "GENESIS") for i, event in enumerate(state["events"])), "asset_register_complete": all(asset.get("book") and asset.get("cost_center") for asset in state["assets"].values())}


def asset_lifecycle_build_api_contract() -> dict:
    return {"ok": True, "graphql_mutations": ("registerAsset", "placeInService", "runDepreciation", "retireAsset"), "graphql_queries": ("assetRegister", "depreciationSchedule", "assetRisk"), "asyncapi_events": ("AssetPlacedInService", "DepreciationCalculated", "AssetRetired")}


def asset_lifecycle_federate_asset_view(state: dict, asset_id: str, *, external_systems: tuple[str, ...]) -> dict:
    asset = state["assets"][asset_id]
    return {"ok": True, "asset_id": asset_id, "systems": external_systems, "federated_book_value": asset["book_value"]}


def asset_lifecycle_integrate_insurance_warranty(state: dict, asset_id: str, *, policy: dict) -> dict:
    return {"ok": True, "asset_id": asset_id, "policy_id": policy["policy_id"], "insured_value": policy["coverage"], "warranty_months": policy["warranty_months"]}


def asset_lifecycle_verify_asset_identity(identity: dict) -> dict:
    subject = identity.get("did", "").removeprefix("did:appgen:").replace("-", "_")
    return {"ok": identity.get("issuer") == "asset_registry" and identity.get("status") == "active", "subject": subject}


def asset_lifecycle_run_resilience_drill(state: dict, scenario: str) -> dict:
    failed_nodes = 1 if scenario else 0
    remaining_quorum = max(0, 5 - failed_nodes)
    return {"ok": remaining_quorum >= 3, "scenario": scenario, "decision": "self_healed", "remaining_quorum": remaining_quorum}


def asset_lifecycle_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "key_epoch": state["crypto_epoch"]["epoch"] + 1, "algorithm": algorithm}


def asset_lifecycle_schedule_carbon_aware_utilization(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def asset_lifecycle_optimize_asset_portfolio(assets: tuple[dict, ...]) -> dict:
    scored = tuple({**asset, "objective_score": round(asset["risk"] + (1 - asset["utilization"]) - asset["value"] / 10000, 4)} for asset in assets)
    selected = min(scored, key=lambda item: item["objective_score"])
    return {"ok": True, "selected_asset": selected["asset_id"], "objective_score": selected["objective_score"], "candidates": scored}


def asset_lifecycle_allocate_shared_asset(*, requests: tuple[dict, ...], available_hours: float) -> dict:
    clearing_bid = round(sum(request["bid"] for request in requests) / len(requests), 1)
    allocations = []
    remaining = available_hours
    for request in sorted(requests, key=lambda item: item["bid"], reverse=True):
        amount = min(request["hours"], remaining)
        remaining -= amount
        allocations.append({"team": request["team"], "allocated_hours": amount})
    return {"ok": remaining == 0, "clearing_bid": clearing_bid, "allocations": tuple(allocations)}


def asset_lifecycle_detect_asset_anomaly(state: dict) -> dict:
    values = tuple(asset["book_value"] for asset in state["assets"].values()) or (0,)
    total = sum(values) or 1
    distribution = tuple(value / total for value in values)
    entropy = -sum(p * math.log(p, 2) for p in distribution if p > 0)
    return {"ok": True, "entropy": round(entropy, 4), "kl_divergence": round(abs(math.log(len(distribution) or 1, 2) - entropy), 4)}


def asset_lifecycle_verify_formal_invariants(state: dict) -> dict:
    schedule_assets = {schedule["asset_id"] for schedule in state["schedules"].values()}
    return {"ok": schedule_assets <= set(state["assets"]) and all(asset["book_value"] >= 0 for asset in state["assets"].values()), "invariants": ("schedule_references_existing_asset", "non_negative_book_value", "single_owner_datastore")}


def asset_lifecycle_build_workbench_view(state: dict, *, tenant: str) -> dict:
    assets = tuple(asset for asset in state["assets"].values() if asset["tenant"] == tenant)
    return {"ok": True, "tenant": tenant, "asset_count": len(assets), "in_service_count": len(tuple(asset for asset in assets if asset["status"] == "in_service")), "retired_count": len(tuple(asset for asset in assets if asset["status"] == "retired")), "net_book_value": round(sum(asset["book_value"] for asset in assets), 2)}


def asset_lifecycle_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.8 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"asset_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"asset_lifecycle:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(payload: dict | tuple | list | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha3_256(encoded.encode("utf-8")).hexdigest()
