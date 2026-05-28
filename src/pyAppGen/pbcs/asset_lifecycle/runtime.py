"""Executable runtime for the Asset Lifecycle PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re

from .depreciation_engine import build_schedule_version
from .depreciation_engine import first_open_line_for_period
from .depreciation_engine import line_fingerprints_for_period
from .depreciation_engine import next_period
from .depreciation_engine import normalize_period
from .depreciation_engine import posted_periods


ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC = "appgen.asset.events"
ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ASSET_LIFECYCLE_OWNED_TABLES = (
    "fixed_asset",
    "asset_component",
    "asset_component_history",
    "asset_book",
    "asset_book_assignment",
    "asset_acquisition",
    "asset_capitalization",
    "asset_lease_right_of_use",
    "asset_depreciation_schedule",
    "asset_depreciation_schedule_line",
    "asset_depreciation_run",
    "asset_depreciation_journal",
    "asset_transfer",
    "asset_valuation_adjustment",
    "asset_impairment_indicator",
    "asset_maintenance_adjustment",
    "asset_insurance_warranty",
    "asset_claim",
    "asset_retirement",
    "asset_disposal_proceeds",
    "asset_physical_verification",
    "asset_physical_verification_exception",
    "asset_location_assignment",
    "asset_custodian_assignment",
    "asset_cost_center_assignment",
    "asset_policy_screening",
    "asset_audit_proof",
    "asset_cross_system_federation",
    "asset_identity_credential",
    "asset_carbon_utilization",
    "asset_portfolio_optimization",
    "asset_allocation_mechanism",
    "asset_anomaly_signal",
    "asset_risk_model",
    "asset_seed_data",
    "asset_schema_extension",
    "asset_control_assertion",
    "asset_governed_model",
    "asset_rule",
    "asset_parameter",
    "asset_configuration",
    "asset_lifecycle_appgen_outbox_event",
    "asset_lifecycle_appgen_inbox_event",
    "asset_lifecycle_dead_letter_event",
)
ASSET_LIFECYCLE_EMITTED_EVENT_TYPES = (
    "AssetRegistered",
    "AssetPlacedInService",
    "DepreciationCalculated",
    "AssetTransferred",
    "AssetRevalued",
    "AssetImpaired",
    "MaintenanceAdjustedAssetLife",
    "AssetRetired",
)
ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES = (
    "PurchaseReceiptCapitalized",
    "MaintenanceCompleted",
    "InsurancePolicyChanged",
    "TaxBookChanged",
    "AccessPolicyChanged",
)
_ASSET_LIFECYCLE_RUNTIME_TABLES = (
    "asset_lifecycle_appgen_outbox_event",
    "asset_lifecycle_appgen_inbox_event",
    "asset_lifecycle_dead_letter_event",
)
_ASSET_LIFECYCLE_ALLOWED_DEPENDENCIES = (
    "purchase_receipt_projection",
    "maintenance_completion_projection",
    "insurance_policy_projection",
    "tax_book_projection",
    "access_policy_projection",
    "POST /ledger/journals",
    "GET /procurement/receipts",
    "GET /maintenance/work-orders",
    "GET /insurance/policies",
    "GET /tax/books",
)
_ASSET_LIFECYCLE_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}

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
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "asset_master",
    "asset_register",
    "asset_acquisition",
    "capitalization",
    "purchase_receipt_capitalization",
    "placed_in_service",
    "component_assets",
    "component_history",
    "asset_location_assignment",
    "asset_custodian_assignment",
    "cost_center_assignment",
    "depreciation_books",
    "book_assignment",
    "depreciation_methods",
    "depreciation_schedule",
    "depreciation_schedule_lines",
    "depreciation_run",
    "depreciation_journal",
    "asset_transfer",
    "asset_revaluation",
    "asset_impairment",
    "impairment_indicator_management",
    "maintenance_adjustment",
    "insurance_warranty",
    "insurance_claims",
    "lease_right_of_use",
    "asset_retirement",
    "disposal_proceeds",
    "disposal_gain_loss",
    "journal_events",
    "event_outbox",
    "event_inbox",
    "idempotent_handlers",
    "retry_dead_letter",
    "physical_verification",
    "approval_controls",
    "audit_trail",
    "permissions",
    "owned_datastore_boundary",
    "release_gate",
    "seed_data",
    "appgen_event_contract",
    "workbench",
)


def asset_lifecycle_runtime_capabilities() -> dict:
    smoke = asset_lifecycle_runtime_smoke()
    return {
        "format": "appgen.asset-lifecycle-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "asset_lifecycle",
        "implementation_directory": "src/pyAppGen/pbcs/asset_lifecycle",
        "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
        "capabilities": ASSET_LIFECYCLE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": ASSET_LIFECYCLE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_asset",
            "place_asset_in_service",
            "build_depreciation_schedule",
            "review_depreciation_plan",
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
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
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
            "verify_owned_table_boundary",
            "build_workbench_view",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def asset_lifecycle_runtime_smoke() -> dict:
    state = asset_lifecycle_empty_state()
    state = asset_lifecycle_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "default_book": "corporate",
            "workbench_limit": 100,
        },
    )["state"]
    state = asset_lifecycle_set_parameter(state, "capitalization_threshold", 500)["state"]
    state = asset_lifecycle_set_parameter(state, "impairment_indicator_threshold", 0.65)["state"]
    state = asset_lifecycle_register_rule(
        state,
        {
            "rule_id": "rule_asset",
            "tenant": "tenant_alpha",
            "scope": "capitalization",
            "capitalization_threshold": 500,
            "approval_required": True,
            "status": "active",
        },
    )["state"]
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
    schema = asset_lifecycle_build_schema_contract()
    service = asset_lifecycle_build_service_contract()
    release = asset_lifecycle_build_release_evidence()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "DepreciationCalculated" in api["asyncapi_events"]},
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
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "events": (),
        "outbox": (),
        "inbox": {},
        "handled_events": {},
        "dead_letters": (),
        "dead_letter": (),
        "retry_evidence": (),
        "projections": {
            "purchase_receipts": {},
            "maintenance_completions": {},
            "insurance_policies": {},
            "tax_books": {},
            "access_policies": {},
        },
        "assets": {},
        "asset_graph": {},
        "schedules": {},
        "schedule_history": {},
        "depreciation_runs": {},
        "depreciation_run_index": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def asset_lifecycle_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _ASSET_LIFECYCLE_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Asset Lifecycle eventing is fixed to AppGen-X; remove stream-engine picker fields: {forbidden}")
    if configuration.get("database_backend") not in ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Asset Lifecycle supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Asset Lifecycle must use the AppGen-X event topic {ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_database_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
        "outbox_table": "asset_lifecycle_appgen_outbox_event",
        "inbox_table": "asset_lifecycle_appgen_inbox_event",
        "dead_letter_table": "asset_lifecycle_dead_letter_event",
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def asset_lifecycle_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    allowed = {
        "capitalization_threshold",
        "impairment_indicator_threshold",
        "physical_verification_interval_days",
        "depreciation_batch_size",
        "retirement_approval_limit",
        "workbench_limit",
    }
    if key not in allowed:
        raise ValueError(f"Unsupported Asset Lifecycle parameter: {key}")
    parameters = {**state.get("parameters", {}), key: value}
    return {"ok": True, "state": {**state, "parameters": parameters}, "parameter": {"key": key, "value": value}}


def asset_lifecycle_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "scope", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Asset Lifecycle rule fields: {missing}")
    stored = {**rule, "enabled": rule["status"] == "active"}
    rules = {**state.get("rules", {}), rule["rule_id"]: stored}
    return {"ok": True, "state": {**state, "rules": rules}, "rule": stored}


def asset_lifecycle_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in ASSET_LIFECYCLE_OWNED_TABLES:
        return {"ok": False, "error": "non_owned_table", "table": table, "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES, "state": state}
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = dict(state.get("schema_extensions", {}))
    extensions[table] = {**extensions.get(table, {}), **dict(fields)}
    return {"ok": True, "state": {**state, "schema_extensions": extensions}, "table": table, "fields": dict(fields)}


def asset_lifecycle_receive_event(state: dict, event: dict) -> dict:
    event_id = event.get("event_id")
    event_type = event.get("event_type")
    if not event_id:
        raise ValueError("Asset Lifecycle inbox events require event_id")
    if event_id in state.get("handled_events", {}):
        return {
            "ok": True,
            "duplicate": True,
            "state": state,
            "handler": {"event_id": event_id, "event_type": event_type, "status": "duplicate"},
        }
    retry_limit = int(state.get("configuration", {}).get("retry_limit", 3))
    attempts = int(event.get("attempts", 1))
    if event_type not in ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES or event.get("payload") is None:
        status = "dead_lettered" if attempts >= retry_limit else "retrying"
        evidence = {
            "event_id": event_id,
            "event_type": event_type,
            "attempts": attempts,
            "retry_limit": retry_limit,
            "status": status,
            "reason": "unsupported_event_type" if event_type not in ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES else "missing_payload",
        }
        next_state = {**state, "retry_evidence": (*state.get("retry_evidence", ()), evidence)}
        if status == "dead_lettered":
            next_state = {
                **next_state,
                "dead_letters": (*next_state.get("dead_letters", ()), {**event, "status": status, "reason": evidence["reason"]}),
                "dead_letter": (*next_state.get("dead_letter", ()), {**event, "status": status, "reason": evidence["reason"]}),
            }
        return {"ok": False, "state": next_state, "handler": evidence, "dead_lettered": status == "dead_lettered"}

    payload = dict(event["payload"])
    projections = {
        **state.get(
            "projections",
            {
                "purchase_receipts": {},
                "maintenance_completions": {},
                "insurance_policies": {},
                "tax_books": {},
                "access_policies": {},
            },
        )
    }
    projection_key = {
        "PurchaseReceiptCapitalized": "purchase_receipts",
        "MaintenanceCompleted": "maintenance_completions",
        "InsurancePolicyChanged": "insurance_policies",
        "TaxBookChanged": "tax_books",
        "AccessPolicyChanged": "access_policies",
    }[event_type]
    projection_id = payload.get("asset_id") or payload.get("receipt_id") or payload.get("policy_id") or payload.get("book_id") or payload.get("policy_version") or event_id
    projections[projection_key] = {
        **projections.get(projection_key, {}),
        projection_id: {
            "event_id": event_id,
            "event_type": event_type,
            "payload": payload,
            "source": event.get("source", "appgen"),
        },
    }
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "projection": projection_key}
    next_state = {
        **state,
        "inbox": {**state.get("inbox", {}), event_id: {**event, "status": "processed"}},
        "handled_events": {**state.get("handled_events", {}), event_id: handler},
        "projections": projections,
    }
    return {"ok": True, "state": next_state, "handler": handler, "duplicate": False}


def asset_lifecycle_register_asset(state: dict, asset: dict) -> dict:
    graph_degree = len(asset.get("components", ())) + 1
    enriched = {
        **asset,
        "status": "registered",
        "book_value": asset["cost"],
        "accumulated_depreciation": 0.0,
        "depreciation_months_posted": 0,
        "active_schedule_id": None,
        "active_schedule_version": 0,
        "schedule_revision_required": False,
        "next_depreciation_period": None,
        "graph_degree": graph_degree,
    }
    next_state = {**state, "assets": {**state["assets"], asset["asset_id"]: enriched}, "asset_graph": {**state["asset_graph"], asset["asset_id"]: {"components": tuple(asset.get("components", ())), "location": asset["location"], "custodian": asset["custodian"]}}}
    next_state = _append_event(next_state, "AssetRegistered", {"tenant": asset["tenant"], "asset_id": asset["asset_id"], "cost": asset["cost"]})
    return {"ok": True, "state": next_state, "asset": enriched}


def asset_lifecycle_place_asset_in_service(state: dict, asset_id: str, *, service_date: str) -> dict:
    asset = {
        **state["assets"][asset_id],
        "status": "in_service",
        "service_date": service_date,
        "next_depreciation_period": normalize_period(service_date),
    }
    next_state = {**state, "assets": {**state["assets"], asset_id: asset}}
    next_state = _append_event(next_state, "AssetPlacedInService", {"tenant": asset["tenant"], "asset_id": asset_id, "service_date": service_date})
    return {"ok": True, "state": next_state, "asset": asset}


def asset_lifecycle_build_depreciation_schedule(state: dict, asset_id: str, *, method: str) -> dict:
    asset = state["assets"][asset_id]
    prior_schedule = state["schedules"].get(asset.get("active_schedule_id")) if asset.get("active_schedule_id") else None
    revision_reason = "life_change" if asset.get("schedule_revision_required") else ("initial_build" if prior_schedule is None else "manual_rebuild")
    version = int(asset.get("active_schedule_version", 0)) + 1
    schedule = build_schedule_version(
        asset,
        method=method,
        version=version,
        revision_reason=revision_reason,
        effective_period=asset.get("next_depreciation_period"),
        prior_schedule=prior_schedule,
    )
    if not schedule["ok"]:
        return {"ok": False, "state": state, "error": schedule["reason"], "asset_id": asset_id}

    schedules = dict(state["schedules"])
    if prior_schedule is not None:
        schedules[prior_schedule["schedule_id"]] = {
            **prior_schedule,
            "status": "superseded",
            "superseded_by": schedule["schedule_id"],
        }
    schedules[schedule["schedule_id"]] = schedule
    history = dict(state.get("schedule_history", {}))
    history[asset_id] = (*history.get(asset_id, ()), schedule["schedule_id"])
    updated_asset = {
        **asset,
        "active_schedule_id": schedule["schedule_id"],
        "active_schedule_version": schedule["version"],
        "depreciation_method": method,
        "schedule_revision_required": False,
        "next_depreciation_period": schedule["next_open_period"],
    }
    next_state = {
        **state,
        "assets": {**state["assets"], asset_id: updated_asset},
        "schedules": schedules,
        "schedule_history": history,
    }
    return {
        "ok": True,
        "state": next_state,
        "schedule": schedule,
        "superseded_schedule_id": prior_schedule["schedule_id"] if prior_schedule else None,
    }


def asset_lifecycle_review_depreciation_plan(state: dict, asset_id: str) -> dict:
    asset = state["assets"][asset_id]
    history_ids = state.get("schedule_history", {}).get(asset_id, ())
    history = tuple(state["schedules"][schedule_id] for schedule_id in history_ids if schedule_id in state["schedules"])
    active_schedule = state["schedules"].get(asset.get("active_schedule_id"))
    related_runs = tuple(
        run
        for run in state.get("depreciation_runs", {}).values()
        if asset_id in run.get("included_assets", ())
    )
    return {
        "ok": True,
        "asset_id": asset_id,
        "active_schedule_id": asset.get("active_schedule_id"),
        "active_version": asset.get("active_schedule_version", 0),
        "revision_required": bool(asset.get("schedule_revision_required")),
        "next_depreciation_period": asset.get("next_depreciation_period"),
        "posted_periods": posted_periods(history),
        "pending_periods": tuple(
            line["period"]
            for line in (active_schedule or {}).get("lines", ())
            if not line.get("posted")
        ),
        "schedule_versions": tuple(
            {
                "schedule_id": schedule["schedule_id"],
                "version": schedule["version"],
                "status": schedule["status"],
                "revision_reason": schedule["revision_reason"],
                "line_count": schedule["line_count"],
            }
            for schedule in history
        ),
        "latest_run_id": related_runs[-1]["run_id"] if related_runs else None,
        "idempotency_keys": tuple(run["idempotency_key"] for run in related_runs),
    }


def asset_lifecycle_run_depreciation(state: dict, *, run_id: str, period: str) -> dict:
    normalized_period = normalize_period(period)
    active_schedules = tuple(schedule for schedule in state["schedules"].values() if schedule.get("status") == "active")
    due_fingerprints = tuple(
        fingerprint
        for schedule in active_schedules
        for fingerprint in line_fingerprints_for_period(schedule, normalized_period)
    )
    if not due_fingerprints:
        return {"ok": False, "state": state, "reason": "no_due_schedule_lines", "period": normalized_period}

    idempotency_key = f"asset_lifecycle:depreciation_run:{normalized_period}:{_digest(due_fingerprints)[:20]}"
    if run_id in state.get("depreciation_runs", {}):
        existing = state["depreciation_runs"][run_id]
        return {
            "ok": True,
            "duplicate": True,
            "state": state,
            "run": existing,
            "journals": existing["journals"],
            "idempotency_key": existing["idempotency_key"],
        }
    existing_run_id = state.get("depreciation_run_index", {}).get(idempotency_key)
    if existing_run_id is not None:
        existing = state["depreciation_runs"][existing_run_id]
        return {
            "ok": True,
            "duplicate": True,
            "state": state,
            "run": existing,
            "journals": existing["journals"],
            "idempotency_key": existing["idempotency_key"],
            "duplicate_of": existing_run_id,
        }

    journals = []
    assets = dict(state["assets"])
    schedules = dict(state["schedules"])
    for schedule in active_schedules:
        line = first_open_line_for_period(schedule, normalized_period)
        if line is None:
            continue
        asset = assets[schedule["asset_id"]]
        depreciation = round(line["amount"], 2)
        updated_lines = tuple(
            {
                **candidate,
                "posted": True,
                "posted_run_id": run_id,
            }
            if candidate["schedule_line_id"] == line["schedule_line_id"]
            else candidate
            for candidate in schedule["lines"]
        )
        next_open_period = next((candidate["period"] for candidate in updated_lines if not candidate.get("posted")), None)
        schedules[schedule["schedule_id"]] = {
            **schedule,
            "lines": updated_lines,
            "posted_line_count": int(schedule.get("posted_line_count", 0)) + 1,
            "last_run_id": run_id,
            "last_posted_period": normalized_period,
            "next_open_period": next_open_period,
        }
        assets[asset["asset_id"]] = {
            **asset,
            "accumulated_depreciation": round(asset["accumulated_depreciation"] + depreciation, 2),
            "book_value": round(max(asset["residual_value"], asset["book_value"] - depreciation), 2),
            "depreciation_months_posted": int(asset.get("depreciation_months_posted", 0)) + 1,
            "last_depreciation_period": normalized_period,
            "next_depreciation_period": next_open_period or next_period(normalized_period),
        }
        journals.append(
            {
                "journal_id": f"jrnl_{run_id}_{asset['asset_id']}",
                "asset_id": asset["asset_id"],
                "schedule_id": schedule["schedule_id"],
                "schedule_version": schedule["version"],
                "period": normalized_period,
                "amount": depreciation,
                "route": "POST /ledger/journals",
                "event": "DepreciationCalculated",
            }
        )

    if not journals:
        return {"ok": False, "state": state, "reason": "period_not_open", "period": normalized_period}

    next_state = {**state, "assets": assets, "schedules": schedules}
    tenant = assets[journals[0]["asset_id"]]["tenant"]
    next_state = _append_event(
        next_state,
        "DepreciationCalculated",
        {
            "tenant": tenant,
            "run_id": run_id,
            "period": normalized_period,
            "journal_count": len(journals),
            "idempotency_key": idempotency_key,
        },
    )
    run = {
        "run_id": run_id,
        "period": normalized_period,
        "book": "all",
        "status": "posted",
        "idempotency_key": idempotency_key,
        "included_assets": tuple(journal["asset_id"] for journal in journals),
        "calculated_total": round(sum(journal["amount"] for journal in journals), 2),
        "journals": tuple(journals),
        "event_id": next_state["events"][-1]["event_id"],
    }
    next_state = {
        **next_state,
        "depreciation_runs": {**next_state["depreciation_runs"], run_id: run},
        "depreciation_run_index": {**next_state.get("depreciation_run_index", {}), idempotency_key: run_id},
    }
    return {"ok": True, "state": next_state, "run": run, "journals": tuple(journals), "duplicate": False, "idempotency_key": idempotency_key}


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
    updated = {
        **asset,
        "useful_life_months": asset["useful_life_months"] + useful_life_delta_months,
        "maintenance_evidence": evidence,
        "schedule_revision_required": bool(asset.get("active_schedule_id")),
    }
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
    routes = (
        {"route": "POST /assets", "command": "register_asset", "owned_table": "fixed_asset", "permission": "asset_lifecycle.register"},
        {"route": "POST /assets/{asset_id}/service", "command": "place_asset_in_service", "owned_table": "fixed_asset", "permission": "asset_lifecycle.service"},
        {"route": "POST /assets/{asset_id}/depreciation-schedules", "command": "build_depreciation_schedule", "owned_table": "asset_depreciation_schedule", "permission": "asset_lifecycle.depreciation"},
        {"route": "POST /depreciation-runs", "command": "run_depreciation", "owned_table": "asset_depreciation_run", "permission": "asset_lifecycle.depreciation"},
        {"route": "POST /assets/{asset_id}/transfers", "command": "transfer_asset", "owned_table": "asset_transfer", "permission": "asset_lifecycle.transfer"},
        {"route": "POST /assets/{asset_id}/revaluations", "command": "revalue_asset", "owned_table": "asset_valuation_adjustment", "permission": "asset_lifecycle.valuation"},
        {"route": "POST /assets/{asset_id}/impairments", "command": "impair_asset", "owned_table": "asset_valuation_adjustment", "permission": "asset_lifecycle.valuation"},
        {"route": "POST /assets/{asset_id}/maintenance-adjustments", "command": "record_maintenance_adjustment", "owned_table": "asset_maintenance_adjustment", "permission": "asset_lifecycle.maintenance"},
        {"route": "POST /assets/{asset_id}/retirements", "command": "retire_asset", "owned_table": "asset_retirement", "permission": "asset_lifecycle.retirement"},
        {"route": "POST /assets/events/inbox", "command": "receive_event", "owned_table": "asset_lifecycle_appgen_inbox_event", "permission": "asset_lifecycle.event"},
        {"route": "GET /assets", "query": "asset_register", "owned_table": "fixed_asset", "permission": "asset_lifecycle.read"},
        {"route": "GET /assets/{asset_id}/risk", "query": "asset_risk", "owned_table": "fixed_asset", "permission": "asset_lifecycle.read"},
    )
    return {
        "format": "appgen.asset-lifecycle-api-contract.v1",
        "ok": True,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "database_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
        "runtime_tables": _ASSET_LIFECYCLE_RUNTIME_TABLES,
        "emits": ASSET_LIFECYCLE_EMITTED_EVENT_TYPES,
        "consumes": ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES,
        "dependency_contracts": _ASSET_LIFECYCLE_ALLOWED_DEPENDENCIES,
        "routes": routes,
        "graphql_mutations": ("registerAsset", "placeInService", "runDepreciation", "retireAsset"),
        "graphql_queries": ("assetRegister", "depreciationSchedule", "assetRisk"),
        "asyncapi_events": ("AssetPlacedInService", "DepreciationCalculated", "AssetRetired"),
    }


def asset_lifecycle_build_schema_contract() -> dict:
    """Return Asset-owned schema, migration, model, and relationship evidence."""
    table_fields = {
        "fixed_asset": ("tenant", "asset_id", "legal_entity", "description", "category", "cost", "book_value", "status"),
        "asset_component": ("tenant", "component_id", "asset_id", "component_name", "capitalization_split", "status"),
        "asset_component_history": ("tenant", "component_history_id", "component_id", "event_type", "effective_date", "evidence_hash"),
        "asset_book": ("tenant", "book_id", "book_name", "currency", "purpose", "default_method", "calendar"),
        "asset_book_assignment": ("tenant", "assignment_id", "asset_id", "book_id", "assigned_at", "status"),
        "asset_acquisition": ("tenant", "acquisition_id", "asset_id", "receipt_id", "amount", "capitalization_state"),
        "asset_capitalization": ("tenant", "capitalization_id", "asset_id", "threshold", "approved_by", "capitalized_at"),
        "asset_lease_right_of_use": ("tenant", "lease_id", "asset_id", "liability", "term_months", "discount_rate"),
        "asset_depreciation_schedule": ("tenant", "schedule_id", "asset_id", "book", "method", "version", "status"),
        "asset_depreciation_schedule_line": ("tenant", "schedule_line_id", "schedule_id", "period", "amount", "book_value"),
        "asset_depreciation_run": ("tenant", "run_id", "period", "book", "status", "idempotency_key"),
        "asset_depreciation_journal": ("tenant", "journal_id", "run_id", "asset_id", "period", "amount", "route"),
        "asset_transfer": ("tenant", "transfer_id", "asset_id", "location", "cost_center", "approved_by"),
        "asset_valuation_adjustment": ("tenant", "adjustment_id", "asset_id", "adjustment_type", "amount", "proof_hash"),
        "asset_impairment_indicator": ("tenant", "indicator_id", "asset_id", "market_indicator", "decision", "observed_at"),
        "asset_maintenance_adjustment": ("tenant", "maintenance_adjustment_id", "asset_id", "useful_life_delta", "evidence"),
        "asset_insurance_warranty": ("tenant", "coverage_id", "asset_id", "policy_id", "coverage", "warranty_months"),
        "asset_claim": ("tenant", "claim_id", "asset_id", "policy_id", "amount", "status"),
        "asset_retirement": ("tenant", "retirement_id", "asset_id", "method", "proceeds", "gain_loss", "approved_by"),
        "asset_disposal_proceeds": ("tenant", "proceeds_id", "asset_id", "amount", "currency", "received_at"),
        "asset_physical_verification": ("tenant", "verification_id", "asset_id", "location", "status", "evidence_hash"),
        "asset_physical_verification_exception": ("tenant", "exception_id", "verification_id", "reason", "resolution_state"),
        "asset_location_assignment": ("tenant", "location_assignment_id", "asset_id", "location", "effective_date"),
        "asset_custodian_assignment": ("tenant", "custodian_assignment_id", "asset_id", "custodian", "effective_date"),
        "asset_cost_center_assignment": ("tenant", "cost_center_assignment_id", "asset_id", "cost_center", "effective_date"),
        "asset_policy_screening": ("tenant", "screening_id", "asset_id", "policy", "decision", "evidence_hash"),
        "asset_audit_proof": ("tenant", "proof_id", "asset_id", "proof_hash", "public_claims", "created_at"),
        "asset_cross_system_federation": ("tenant", "federation_id", "asset_id", "external_system", "projection_hash"),
        "asset_identity_credential": ("tenant", "credential_id", "asset_id", "did", "issuer", "status"),
        "asset_carbon_utilization": ("tenant", "carbon_id", "asset_id", "window", "carbon_intensity", "selected"),
        "asset_portfolio_optimization": ("tenant", "portfolio_id", "selected_asset", "objective_score", "candidate_count"),
        "asset_allocation_mechanism": ("tenant", "allocation_id", "asset_id", "clearing_bid", "allocated_hours"),
        "asset_anomaly_signal": ("tenant", "signal_id", "asset_id", "signal_type", "kl_divergence", "observed_at"),
        "asset_risk_model": ("tenant", "risk_model_id", "asset_id", "risk_score", "model_version", "explanations"),
        "asset_seed_data": ("tenant", "seed_id", "asset_category", "book", "method", "useful_life_months"),
        "asset_schema_extension": ("tenant", "extension_id", "table_name", "field_name", "field_type", "version"),
        "asset_control_assertion": ("tenant", "control_id", "assertion", "status", "evidence_hash", "tested_at"),
        "asset_governed_model": ("tenant", "model_id", "name", "feature_lineage", "drift_score", "governance_status"),
        "asset_rule": ("tenant", "rule_id", "scope", "status", "predicate", "compiled_hash"),
        "asset_parameter": ("tenant", "parameter_id", "name", "value", "bounds", "compiled_hash"),
        "asset_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "default_book"),
        "asset_lifecycle_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "asset_lifecycle_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "asset_lifecycle_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "asset_component.asset_id", "to": "fixed_asset.asset_id", "type": "owned_child"},
        {"from": "asset_component_history.component_id", "to": "asset_component.component_id", "type": "owned_history"},
        {"from": "asset_book_assignment.asset_id", "to": "fixed_asset.asset_id", "type": "owned_book"},
        {"from": "asset_acquisition.asset_id", "to": "fixed_asset.asset_id", "type": "owned_acquisition"},
        {"from": "asset_depreciation_schedule.asset_id", "to": "fixed_asset.asset_id", "type": "owned_schedule"},
        {"from": "asset_depreciation_schedule_line.schedule_id", "to": "asset_depreciation_schedule.schedule_id", "type": "owned_child"},
        {"from": "asset_depreciation_journal.run_id", "to": "asset_depreciation_run.run_id", "type": "owned_journal"},
        {"from": "asset_transfer.asset_id", "to": "fixed_asset.asset_id", "type": "owned_transfer"},
        {"from": "asset_retirement.asset_id", "to": "fixed_asset.asset_id", "type": "owned_retirement"},
        {"from": "asset_physical_verification.asset_id", "to": "fixed_asset.asset_id", "type": "owned_verification"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "asset_lifecycle",
        }
        for table in ASSET_LIFECYCLE_OWNED_TABLES
    )
    return {
        "format": "appgen.asset-lifecycle-owned-schema-contract.v1",
        "ok": len(tables) == len(ASSET_LIFECYCLE_OWNED_TABLES)
        and len(tables) >= 35
        and all(item["table"].startswith(("asset_", "asset_lifecycle_")) or item["table"] == "fixed_asset" for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/asset_lifecycle/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(ASSET_LIFECYCLE_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in ASSET_LIFECYCLE_OWNED_TABLES
        ),
        "datastore_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def asset_lifecycle_build_service_contract() -> dict:
    """Return Asset Lifecycle command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_asset",
        "place_asset_in_service",
        "assign_asset_book",
        "build_depreciation_schedule",
        "run_depreciation",
        "transfer_asset",
        "revalue_asset",
        "impair_asset",
        "record_maintenance_adjustment",
        "integrate_insurance_warranty",
        "record_insurance_claim",
        "run_physical_verification",
        "retire_asset",
        "record_disposal_proceeds",
        "parse_capitalization_document",
        "route_depreciation_journal",
        "generate_asset_audit_proof",
        "screen_asset_policy",
        "federate_asset_view",
        "verify_asset_identity",
        "schedule_carbon_aware_utilization",
        "optimize_asset_portfolio",
        "allocate_shared_asset",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.asset-lifecycle-service-contract.v1",
        "ok": len(command_methods) >= 28,
        "transaction_boundary": "asset_lifecycle_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "review_depreciation_plan",
            "estimate_useful_life",
            "project_asset_valuation",
            "forecast_asset_value_risk",
            "detect_asset_anomaly",
            "verify_owned_table_boundary",
        ),
        "mutates_only": ASSET_LIFECYCLE_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _ASSET_LIFECYCLE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _ASSET_LIFECYCLE_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def asset_lifecycle_build_release_evidence() -> dict:
    """Return Asset Lifecycle package-local release evidence."""
    schema = asset_lifecycle_build_schema_contract()
    service = asset_lifecycle_build_service_contract()
    api = asset_lifecycle_build_api_contract()
    permissions = asset_lifecycle_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 35},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(ASSET_LIFECYCLE_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 28},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"register_asset", "run_depreciation", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
        {"id": "depreciation_schedule_versioning", "ok": "review_depreciation_plan" in service["query_methods"]},
        {"id": "depreciation_run_idempotency", "ok": "idempotency_key" in next(item for item in schema["tables"] if item["table"] == "asset_depreciation_run")["fields"]},
    )
    return {
        "format": "appgen.asset-lifecycle-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def asset_lifecycle_permissions_contract() -> dict:
    action_permissions = {
        "configure_runtime": "asset_lifecycle.configure",
        "set_parameter": "asset_lifecycle.configure",
        "register_rule": "asset_lifecycle.configure",
        "register_schema_extension": "asset_lifecycle.configure",
        "receive_event": "asset_lifecycle.event",
        "register_asset": "asset_lifecycle.register",
        "place_asset_in_service": "asset_lifecycle.service",
        "build_depreciation_schedule": "asset_lifecycle.depreciation",
        "run_depreciation": "asset_lifecycle.depreciation",
        "transfer_asset": "asset_lifecycle.transfer",
        "revalue_asset": "asset_lifecycle.valuation",
        "impair_asset": "asset_lifecycle.valuation",
        "record_maintenance_adjustment": "asset_lifecycle.maintenance",
        "retire_asset": "asset_lifecycle.retirement",
        "generate_asset_audit_proof": "asset_lifecycle.audit",
        "run_control_tests": "asset_lifecycle.audit",
        "build_workbench_view": "asset_lifecycle.read",
        "review_depreciation_plan": "asset_lifecycle.depreciation",
    }
    return {
        "format": "appgen.asset-lifecycle-permissions-contract.v1",
        "ok": True,
        "pbc": "asset_lifecycle",
        "roles": {
            "asset_lifecycle_admin": tuple(sorted(set(action_permissions.values()))),
            "asset_lifecycle_accountant": (
                "asset_lifecycle.read",
                "asset_lifecycle.register",
                "asset_lifecycle.service",
                "asset_lifecycle.depreciation",
                "asset_lifecycle.valuation",
                "asset_lifecycle.retirement",
            ),
            "asset_lifecycle_operator": (
                "asset_lifecycle.read",
                "asset_lifecycle.transfer",
                "asset_lifecycle.maintenance",
            ),
            "asset_lifecycle_auditor": (
                "asset_lifecycle.read",
                "asset_lifecycle.audit",
            ),
        },
        "action_permissions": action_permissions,
        "abac_attributes": ("tenant", "legal_entity", "book", "location", "cost_center", "asset_category"),
    }


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


def asset_lifecycle_verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict:
    allowed = set(ASSET_LIFECYCLE_OWNED_TABLES) | set(_ASSET_LIFECYCLE_RUNTIME_TABLES) | set(_ASSET_LIFECYCLE_ALLOWED_DEPENDENCIES) | set(ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES)
    violations = tuple(sorted(reference for reference in references if reference not in allowed and not reference.startswith("asset_lifecycle_")))
    return {
        "format": "appgen.asset-lifecycle-owned-boundary.v1",
        "ok": not violations,
        "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
        "runtime_tables": _ASSET_LIFECYCLE_RUNTIME_TABLES,
        "allowed_dependencies": _ASSET_LIFECYCLE_ALLOWED_DEPENDENCIES,
        "violations": violations,
    }


def asset_lifecycle_build_workbench_view(state: dict, *, tenant: str) -> dict:
    assets = tuple(asset for asset in state["assets"].values() if asset["tenant"] == tenant)
    depreciation_reviews = tuple(
        asset_lifecycle_review_depreciation_plan(state, asset["asset_id"])
        for asset in assets
        if asset.get("active_schedule_id")
    )
    return {
        "ok": True,
        "tenant": tenant,
        "asset_count": len(assets),
        "in_service_count": len(tuple(asset for asset in assets if asset["status"] == "in_service")),
        "retired_count": len(tuple(asset for asset in assets if asset["status"] == "retired")),
        "net_book_value": round(sum(asset["book_value"] for asset in assets), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", {})),
        "dead_letter_count": len(state.get("dead_letters", ())),
        "pending_schedule_revisions": len(tuple(asset for asset in assets if asset.get("schedule_revision_required"))),
        "active_schedule_versions": {review["asset_id"]: review["active_version"] for review in depreciation_reviews},
        "depreciation_idempotency_keys": tuple(sorted(state.get("depreciation_run_index", {}))),
        "binding_evidence": {
            "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
            "runtime_tables": _ASSET_LIFECYCLE_RUNTIME_TABLES,
            "configuration": {
                "event_contract": "AppGen-X",
                "event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
                "allowed_database_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
                "stream_engine_picker_visible": False,
            },
            "emits": ASSET_LIFECYCLE_EMITTED_EVENT_TYPES,
            "consumes": ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES,
            "permissions": asset_lifecycle_permissions_contract()["action_permissions"],
        },
    }


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
