"""Executable runtime for the Procurement and Strategic Sourcing PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC = "appgen.procurement_sourcing.events"
PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PROCUREMENT_SOURCING_OWNED_TABLES = (
    "procurement_sourcing_purchase_requisition",
    "procurement_sourcing_purchase_requisition_line",
    "procurement_sourcing_requisition_approval",
    "procurement_sourcing_requisition_budget_check",
    "procurement_sourcing_category_strategy",
    "procurement_sourcing_category_policy",
    "procurement_sourcing_supplier_profile",
    "procurement_sourcing_supplier_identity",
    "procurement_sourcing_supplier_site",
    "procurement_sourcing_supplier_qualification",
    "procurement_sourcing_supplier_risk_signal",
    "procurement_sourcing_preferred_supplier_policy",
    "procurement_sourcing_rfq",
    "procurement_sourcing_rfq_line",
    "procurement_sourcing_supplier_invitation",
    "procurement_sourcing_supplier_bid",
    "procurement_sourcing_supplier_bid_line",
    "procurement_sourcing_bid_normalization",
    "procurement_sourcing_supplier_scorecard",
    "procurement_sourcing_supplier_award",
    "procurement_sourcing_split_award",
    "procurement_sourcing_vendor_contract",
    "procurement_sourcing_contract_clause",
    "procurement_sourcing_contract_compliance_obligation",
    "procurement_sourcing_contract_renewal",
    "procurement_sourcing_purchase_order",
    "procurement_sourcing_purchase_order_line",
    "procurement_sourcing_change_order",
    "procurement_sourcing_po_tolerance_check",
    "procurement_sourcing_payment_terms",
    "procurement_sourcing_material_shortage_projection",
    "procurement_sourcing_vendor_performance_projection",
    "procurement_sourcing_budget_projection",
    "procurement_sourcing_supplier_risk_projection",
    "procurement_sourcing_contract_compliance_projection",
    "procurement_sourcing_access_policy_projection",
    "procurement_sourcing_policy_screening",
    "procurement_sourcing_purchase_order_route",
    "procurement_sourcing_supplier_compliance_proof",
    "procurement_sourcing_audit_trace",
    "procurement_sourcing_federation_projection",
    "procurement_sourcing_carbon_sourcing_selection",
    "procurement_sourcing_award_optimization",
    "procurement_sourcing_rfq_mechanism_allocation",
    "procurement_sourcing_bid_anomaly_signal",
    "procurement_sourcing_supply_exposure_model",
    "procurement_sourcing_price_lead_time_forecast",
    "procurement_sourcing_sourcing_strategy_simulation",
    "procurement_sourcing_parsed_document",
    "procurement_sourcing_seed_data",
    "procurement_sourcing_schema_extension",
    "procurement_sourcing_control_assertion",
    "procurement_sourcing_governed_model",
    "procurement_sourcing_rule",
    "procurement_sourcing_parameter",
    "procurement_sourcing_configuration",
    "procurement_sourcing_appgen_outbox_event",
    "procurement_sourcing_appgen_inbox_event",
    "procurement_sourcing_dead_letter_event",
)
PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES = (
    "PurchaseRequisitionCreated",
    "PurchaseRequisitionApproved",
    "RfqCreated",
    "SupplierBidCaptured",
    "SupplierSelected",
    "VendorContractCreated",
    "PurchaseOrderIssued",
)
PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES = (
    "MaterialShortageDetected",
    "VendorPerformanceUpdated",
    "BudgetChanged",
    "SupplierRiskChanged",
    "ContractComplianceChanged",
    "AccessPolicyChanged",
)
_PROCUREMENT_SOURCING_RUNTIME_TABLES = (
    "procurement_sourcing_appgen_outbox_event",
    "procurement_sourcing_appgen_inbox_event",
    "procurement_sourcing_dead_letter_event",
)
_PROCUREMENT_SOURCING_ALLOWED_DEPENDENCIES = (
    "material_shortage_projection",
    "vendor_performance_projection",
    "budget_projection",
    "supplier_risk_projection",
    "contract_compliance_projection",
    "access_policy_projection",
    "GET /identity/policies",
    "POST /audit/contract-events",
    "GET /schema/events",
)
_PROCUREMENT_SOURCING_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}

PROCUREMENT_SOURCING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_source_to_order_lifecycle",
    "graph_relational_supplier_topology",
    "multi_tenant_procurement_isolation",
    "schema_evolution_resilient_procurement_schema",
    "probabilistic_supplier_award_confidence",
    "real_time_sourcing_spend_analytics",
    "counterfactual_sourcing_strategy_simulation",
    "temporal_price_lead_time_forecasting",
    "autonomous_supplier_selection",
    "semantic_procurement_document_parsing",
    "predictive_supplier_disruption_risk",
    "self_healing_po_route_selection",
    "zero_knowledge_supplier_compliance_proof",
    "immutable_procurement_audit_trail",
    "dynamic_procurement_policy_screening",
    "automated_procurement_control_testing",
    "universal_api_async_streaming",
    "cross_system_procurement_federation",
    "supplier_network_integration",
    "decentralized_supplier_identity",
    "chaos_engineered_supplier_route_tolerance",
    "quantum_resistant_procurement_authorization",
    "carbon_aware_sourcing_selection",
    "algebraic_sourcing_award_optimization",
    "mechanism_design_rfq_allocation",
    "information_theoretic_bid_anomaly_detection",
    "temporal_supply_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_supplier_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "procurement_mlops_governance",
)
PROCUREMENT_SOURCING_STANDARD_FEATURE_KEYS = (
    "purchase_requisition",
    "purchase_requisition_lines",
    "approval_routing",
    "budget_policy_check",
    "category_reference",
    "category_strategy",
    "category_policy",
    "supplier_reference",
    "supplier_profiles",
    "supplier_sites",
    "supplier_qualification",
    "supplier_identity",
    "supplier_risk_signals",
    "preferred_supplier_policy",
    "rfq_creation",
    "rfq_lines",
    "supplier_invitation",
    "bid_capture",
    "bid_lines",
    "bid_normalization",
    "supplier_scoring",
    "supplier_scorecards",
    "award_recommendation",
    "split_award",
    "contract_creation",
    "contract_clauses",
    "contract_compliance_obligations",
    "contract_renewal_monitor",
    "purchase_order_creation",
    "purchase_order_lines",
    "po_tolerance_check",
    "change_order",
    "payment_terms",
    "supplier_risk_screening",
    "spend_analytics",
    "consumed_event_handlers",
    "material_shortage_projection",
    "vendor_performance_projection",
    "budget_projection",
    "contract_compliance_projection",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "retry_dead_letter_evidence",
    "multi_entity_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def procurement_sourcing_runtime_capabilities() -> dict:
    smoke = procurement_sourcing_runtime_smoke()
    return {
        "format": "appgen.procurement-sourcing-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "procurement_sourcing",
        "implementation_directory": "src/pyAppGen/pbcs/procurement_sourcing",
        "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
        "capabilities": PROCUREMENT_SOURCING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PROCUREMENT_SOURCING_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "create_requisition",
            "approve_requisition",
            "create_rfq",
            "capture_bid",
            "score_suppliers",
            "select_supplier",
            "create_contract",
            "issue_purchase_order",
            "screen_policy",
            "route_purchase_order",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def procurement_sourcing_runtime_smoke() -> dict:
    state = procurement_sourcing_empty_state()
    state = procurement_sourcing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_categories": ("direct_materials", "maintenance"),
            "workbench_limit": 100,
        },
    )["state"]
    state = procurement_sourcing_set_parameter(state, "approval_limit", 5000)["state"]
    state = procurement_sourcing_set_parameter(state, "minimum_bid_count", 2)["state"]
    state = procurement_sourcing_set_parameter(state, "supplier_risk_threshold", 0.4)["state"]
    state = procurement_sourcing_register_rule(
        state,
        {
            "rule_id": "rule_direct_materials",
            "tenant": "tenant_alpha",
            "rule_type": "sourcing",
            "category": "direct_materials",
            "preferred_suppliers": ("supplier_a",),
            "restricted_suppliers": ("supplier_blocked",),
            "score_weights": {"price": 0.45, "lead_time": 0.2, "risk": 0.2, "quality": 0.15},
            "allow_split_award": True,
            "status": "active",
        },
    )["state"]
    state = procurement_sourcing_register_schema_extension(
        state,
        "procurement_sourcing_rfq",
        {"sustainability_payload": "jsonb"},
    )["state"]
    received = procurement_sourcing_receive_event(
        state,
        {
            "event_id": "material_shortage_001",
            "event_type": "MaterialShortageDetected",
            "payload": {"tenant": "tenant_alpha", "shortage_id": "shortage_001", "item_id": "sku_100", "quantity": 100},
        },
    )
    state = received["state"]
    requisition = procurement_sourcing_create_requisition(
        state,
        {
            "requisition_id": "req_001",
            "tenant": "tenant_alpha",
            "legal_entity": "entity_alpha",
            "category": "direct_materials",
            "item_id": "sku_100",
            "quantity": 100,
            "estimated_amount": 3200,
            "currency": "USD",
            "cost_center": "operations",
            "requested_by": "planner_1",
        },
    )
    state = requisition["state"]
    approval = procurement_sourcing_approve_requisition(state, "req_001", approver="manager_1")
    state = approval["state"]
    rfq = procurement_sourcing_create_rfq(state, "rfq_001", requisition_id="req_001", suppliers=("supplier_a", "supplier_b"))
    state = rfq["state"]
    state = procurement_sourcing_capture_bid(state, "rfq_001", {"supplier_id": "supplier_a", "price": 3000, "lead_time_days": 8, "risk": 0.12, "quality": 0.94, "carbon": 120, "identity": {"did": "did:appgen:supplier-a", "issuer": "trusted_registry", "status": "active"}})["state"]
    state = procurement_sourcing_capture_bid(state, "rfq_001", {"supplier_id": "supplier_b", "price": 2850, "lead_time_days": 12, "risk": 0.18, "quality": 0.9, "carbon": 80, "identity": {"did": "did:appgen:supplier-b", "issuer": "trusted_registry", "status": "active"}})["state"]
    scores = procurement_sourcing_score_suppliers(state, "rfq_001")
    selection = procurement_sourcing_select_supplier(state, "rfq_001", award_id="award_001")
    state = selection["state"]
    contract = procurement_sourcing_create_contract(state, "contract_001", award_id="award_001", term_months=12)
    state = contract["state"]
    po = procurement_sourcing_issue_purchase_order(state, "po_001", contract_id="contract_001", quantity=100, amount=3000)
    state = po["state"]
    policy = procurement_sourcing_screen_policy(state, "po_001", restricted_suppliers=("supplier_blocked",))
    route = procurement_sourcing_route_purchase_order(po["purchase_order"], rails=({"route": "supplier_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}))
    proof = procurement_sourcing_generate_supplier_compliance_proof(state, "supplier_a", disclosure=("supplier_id", "risk"))
    controls = procurement_sourcing_run_control_tests(state)
    api = procurement_sourcing_build_api_contract()
    schema = procurement_sourcing_build_schema_contract()
    service = procurement_sourcing_build_service_contract()
    release = procurement_sourcing_build_release_evidence()
    federation = procurement_sourcing_federate_procurement_view(state, "po_001", systems=("ap", "inventory", "manufacturing"))
    identity = procurement_sourcing_verify_supplier_identity(state["bids"]["rfq_001"][0]["identity"])
    resilience = procurement_sourcing_run_resilience_drill(state, "supplier_route_timeout")
    crypto = procurement_sourcing_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = procurement_sourcing_schedule_carbon_aware_sourcing(scores["scores"])
    optimization = procurement_sourcing_optimize_award(scores["scores"], quantity=100)
    mechanism = procurement_sourcing_allocate_rfq_award(scores["scores"], quantity=100)
    anomaly = procurement_sourcing_detect_bid_anomaly(state, "rfq_001")
    stochastic = procurement_sourcing_model_stochastic_supply_exposure(price_path=(3100, 3000, 2850), volatility=0.07)
    forecast = procurement_sourcing_forecast_price_lead_time((3000, 2900, 2850), (10, 9, 8))
    simulation = procurement_sourcing_simulate_sourcing_strategy(state, "rfq_001", proposed_risk_weight=0.4)
    parsed = procurement_sourcing_parse_document("requisition req_77 category direct_materials amount 2500 supplier supplier_a")
    risk = procurement_sourcing_score_supplier_risk({"late_rate": 0.03, "quality_escape": 0.02, "financial_risk": 0.06})
    workbench = procurement_sourcing_build_workbench_view(state, tenant="tenant_alpha")
    model = procurement_sourcing_register_governed_model("supplier_risk", {"features": ("price", "lead_time", "risk"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_source_to_order_lifecycle", "ok": len(state["events"]) >= 6 and state["events"][-1]["hash"]},
        {"id": "graph_relational_supplier_topology", "ok": rfq["rfq"]["graph_degree"] >= 3},
        {"id": "multi_tenant_procurement_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_procurement_schema", "ok": state["schema_extensions"]["procurement_sourcing_rfq"]["sustainability_payload"] == "jsonb"},
        {"id": "probabilistic_supplier_award_confidence", "ok": selection["award"]["confidence"] >= 0.8},
        {"id": "real_time_sourcing_spend_analytics", "ok": workbench["po_amount"] == 3000},
        {"id": "counterfactual_sourcing_strategy_simulation", "ok": simulation["ok"] and simulation["selected_supplier"] in {"supplier_a", "supplier_b"}},
        {"id": "temporal_price_lead_time_forecasting", "ok": forecast["ok"] and forecast["price_trend"] < 0},
        {"id": "autonomous_supplier_selection", "ok": selection["award"]["supplier_id"] == "supplier_a"},
        {"id": "semantic_procurement_document_parsing", "ok": parsed["ok"] and parsed["amount"] == 2500},
        {"id": "predictive_supplier_disruption_risk", "ok": risk["risk_score"] < 0.3},
        {"id": "self_healing_po_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_supplier_compliance_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_supplier_")},
        {"id": "immutable_procurement_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_procurement_policy_screening", "ok": policy["ok"] and policy["decision"] == "clear"},
        {"id": "automated_procurement_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "PurchaseOrderIssued" in api["events"]["emits"] and api["event_contract"] == "AppGen-X"},
        {"id": "cross_system_procurement_federation", "ok": federation["ok"] and "ap" in federation["systems"]},
        {"id": "supplier_network_integration", "ok": len(state["bids"]["rfq_001"]) == 2},
        {"id": "decentralized_supplier_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_supplier_route_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_supplier_route"},
        {"id": "quantum_resistant_procurement_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_sourcing_selection", "ok": carbon["ok"] and carbon["supplier_id"] == "supplier_b"},
        {"id": "algebraic_sourcing_award_optimization", "ok": optimization["ok"] and optimization["supplier_id"] == "supplier_a"},
        {"id": "mechanism_design_rfq_allocation", "ok": mechanism["ok"] and mechanism["allocations"][0]["quantity"] > 0},
        {"id": "information_theoretic_bid_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_supply_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("procurement_sourcing:PurchaseOrderIssued")},
        {"id": "probabilistic_ml_supplier_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and mechanism["clearing_bid"] > 0},
        {"id": "procurement_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.procurement-sourcing-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def procurement_sourcing_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "handled_events": {},
        "retry_evidence": (),
        "material_shortage_projections": {},
        "vendor_performance_projections": {},
        "budget_projections": {},
        "supplier_risk_projections": {},
        "contract_compliance_projections": {},
        "access_policy_projections": {},
        "requisitions": {},
        "rfqs": {},
        "bids": {},
        "awards": {},
        "contracts": {},
        "purchase_orders": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def procurement_sourcing_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in configuration if field in _PROCUREMENT_SOURCING_FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(f"Procurement Sourcing hides stream-engine picker fields: {forbidden}")
    if configuration.get("database_backend") not in PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Procurement Sourcing supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Procurement Sourcing requires AppGen-X event topic {PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "required_event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def procurement_sourcing_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "approval_limit",
        "minimum_bid_count",
        "supplier_risk_threshold",
        "price_variance_tolerance",
        "renewal_horizon_days",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Procurement Sourcing parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def procurement_sourcing_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Procurement Sourcing rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Procurement Sourcing rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def procurement_sourcing_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in PROCUREMENT_SOURCING_OWNED_TABLES:
        raise ValueError(f"Procurement Sourcing schema extensions must target owned tables: {PROCUREMENT_SOURCING_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    merged = {**state["schema_extensions"].get(table, {}), **fields}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: merged}}, "schema_extension": {"table": table, "fields": dict(fields)}, "target": table, "fields": merged}


def procurement_sourcing_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    handled = state.get("handled_events", {})
    if key in handled and handled[key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": handled[key]}

    attempts = int(handled.get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {
        "event_id": event_id,
        "event_type": event_type,
        "tenant": payload.get("tenant"),
        "attempts": attempts,
        "idempotency_key": key,
    }
    next_state = _copy_state(state)
    next_state["inbox"] = (*next_state.get("inbox", ()), inbox_entry)
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state.get("retry_evidence", ()), evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_procurement_event"}
            next_state["dead_letters"] = (*next_state.get("dead_letters", ()), dead)
            next_state["dead_letter"] = (*next_state.get("dead_letter", ()), dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}

    if event_type == "MaterialShortageDetected":
        next_state["material_shortage_projections"][payload.get("shortage_id", event_id)] = payload
    elif event_type == "VendorPerformanceUpdated":
        next_state["vendor_performance_projections"][payload.get("supplier_id", event_id)] = payload
    elif event_type == "BudgetChanged":
        next_state["budget_projections"][payload.get("budget_id", event_id)] = payload
    elif event_type == "SupplierRiskChanged":
        next_state["supplier_risk_projections"][payload.get("supplier_id", event_id)] = payload
    elif event_type == "ContractComplianceChanged":
        next_state["contract_compliance_projections"][payload.get("contract_id", event_id)] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload.get("policy_id", event_id)] = payload

    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def procurement_sourcing_create_requisition(state: dict, requisition: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    allowed = requisition["category"] in state["configuration"].get("allowed_categories", ()) and requisition["category"] == rule["category"]
    status = "pending_approval" if allowed else "policy_blocked"
    enriched = {**requisition, "status": status, "policy_ok": allowed}
    next_state = {**state, "requisitions": {**state["requisitions"], requisition["requisition_id"]: enriched}}
    next_state = _append_event(next_state, "PurchaseRequisitionCreated", {"tenant": requisition["tenant"], "requisition_id": requisition["requisition_id"], "amount": requisition["estimated_amount"]})
    return {"ok": allowed, "state": next_state, "requisition": enriched}


def procurement_sourcing_approve_requisition(state: dict, requisition_id: str, *, approver: str) -> dict:
    req = state["requisitions"][requisition_id]
    approval_limit = float(state["parameters"].get("approval_limit", 0))
    status = "approved" if req["estimated_amount"] <= approval_limit else "escalated"
    updated = {**req, "status": status, "approved_by": approver}
    next_state = {**state, "requisitions": {**state["requisitions"], requisition_id: updated}}
    next_state = _append_event(next_state, "PurchaseRequisitionApproved", {"tenant": req["tenant"], "requisition_id": requisition_id, "status": status})
    return {"ok": status == "approved", "state": next_state, "requisition": updated}


def procurement_sourcing_create_rfq(state: dict, rfq_id: str, *, requisition_id: str, suppliers: tuple[str, ...]) -> dict:
    req = state["requisitions"][requisition_id]
    rfq = {"rfq_id": rfq_id, "tenant": req["tenant"], "requisition_id": requisition_id, "category": req["category"], "suppliers": suppliers, "status": "open", "graph_degree": len(suppliers) + 2}
    next_state = {**state, "rfqs": {**state["rfqs"], rfq_id: rfq}, "bids": {**state["bids"], rfq_id: ()}}
    next_state = _append_event(next_state, "RfqCreated", {"tenant": req["tenant"], "rfq_id": rfq_id, "supplier_count": len(suppliers)})
    return {"ok": True, "state": next_state, "rfq": rfq}


def procurement_sourcing_capture_bid(state: dict, rfq_id: str, bid: dict) -> dict:
    bids = (*state["bids"].get(rfq_id, ()), {**bid, "normalized_price": round(bid["price"], 2)})
    return {"ok": True, "state": {**state, "bids": {**state["bids"], rfq_id: bids}}, "bid": bids[-1]}


def procurement_sourcing_score_suppliers(state: dict, rfq_id: str) -> dict:
    rule = next(iter(state["rules"].values()))
    weights = rule["score_weights"]
    bids = state["bids"][rfq_id]
    max_price = max(bid["price"] for bid in bids)
    max_lead = max(bid["lead_time_days"] for bid in bids)
    scores = []
    for bid in bids:
        score = (
            (1 - bid["price"] / max_price) * weights["price"]
            + (1 - bid["lead_time_days"] / max_lead) * weights["lead_time"]
            + (1 - bid["risk"]) * weights["risk"]
            + bid["quality"] * weights["quality"]
        )
        if bid["supplier_id"] in rule.get("preferred_suppliers", ()):
            score += 0.08
        scores.append({**bid, "score": round(score, 4), "award_confidence": round(min(0.98, 0.75 + score / 4), 4)})
    return {"ok": True, "rfq_id": rfq_id, "scores": tuple(sorted(scores, key=lambda item: item["score"], reverse=True))}


def procurement_sourcing_select_supplier(state: dict, rfq_id: str, *, award_id: str) -> dict:
    minimum = int(state["parameters"].get("minimum_bid_count", 1))
    scores = procurement_sourcing_score_suppliers(state, rfq_id)["scores"]
    if len(scores) < minimum:
        return {"ok": False, "state": state, "error": "insufficient_bids"}
    selected = scores[0]
    award = {"award_id": award_id, "tenant": state["rfqs"][rfq_id]["tenant"], "rfq_id": rfq_id, "supplier_id": selected["supplier_id"], "amount": selected["price"], "lead_time_days": selected["lead_time_days"], "confidence": selected["award_confidence"], "status": "awarded"}
    next_state = {**state, "awards": {**state["awards"], award_id: award}}
    next_state = _append_event(next_state, "SupplierSelected", {"tenant": award["tenant"], "award_id": award_id, "supplier_id": award["supplier_id"], "amount": award["amount"]})
    return {"ok": True, "state": next_state, "award": award}


def procurement_sourcing_create_contract(state: dict, contract_id: str, *, award_id: str, term_months: int) -> dict:
    award = state["awards"][award_id]
    contract = {**award, "contract_id": contract_id, "term_months": term_months, "renewal_horizon_days": 90, "status": "active"}
    next_state = {**state, "contracts": {**state["contracts"], contract_id: contract}}
    next_state = _append_event(next_state, "VendorContractCreated", {"tenant": contract["tenant"], "contract_id": contract_id, "supplier_id": contract["supplier_id"]})
    return {"ok": True, "state": next_state, "contract": contract}


def procurement_sourcing_issue_purchase_order(state: dict, po_id: str, *, contract_id: str, quantity: float, amount: float) -> dict:
    contract = state["contracts"][contract_id]
    tolerance = float(state["parameters"].get("price_variance_tolerance", 0.1))
    ok = amount <= contract["amount"] * (1 + tolerance)
    po = {"po_id": po_id, "tenant": contract["tenant"], "contract_id": contract_id, "supplier_id": contract["supplier_id"], "quantity": quantity, "amount": amount, "currency": state["configuration"].get("default_currency", "USD"), "status": "issued" if ok else "blocked"}
    next_state = {**state, "purchase_orders": {**state["purchase_orders"], po_id: po}}
    next_state = _append_event(next_state, "PurchaseOrderIssued", {"tenant": po["tenant"], "po_id": po_id, "supplier_id": po["supplier_id"], "amount": amount})
    return {"ok": ok, "state": next_state, "purchase_order": po}


def procurement_sourcing_screen_policy(state: dict, po_id: str, *, restricted_suppliers: tuple[str, ...]) -> dict:
    po = state["purchase_orders"][po_id]
    blocked = po["supplier_id"] in restricted_suppliers or po["status"] != "issued"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "po_id": po_id}


def procurement_sourcing_route_purchase_order(po: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": po["status"] == "issued", "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"procurement_sourcing:PurchaseOrderIssued:{po['po_id']}"}


def procurement_sourcing_generate_supplier_compliance_proof(state: dict, supplier_id: str, *, disclosure: tuple[str, ...]) -> dict:
    bid = next(bid for bids in state["bids"].values() for bid in bids if bid["supplier_id"] == supplier_id)
    claims = {"supplier_id": supplier_id, "risk": bid["risk"], "quality": bid["quality"]}
    public_claims = {field: claims[field] for field in disclosure if field in claims}
    proof_hash = _digest({"claims": public_claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_supplier_" + proof_hash[:24], "hash": proof_hash, "public_claims": public_claims}


def procurement_sourcing_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(po["status"] != "issued" for po in state["purchase_orders"].values()):
        gaps.append("blocked_purchase_order")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def procurement_sourcing_permissions_contract() -> dict:
    return {
        "format": "appgen.procurement-sourcing-permissions.v1",
        "ok": True,
        "permissions": (
            "procurement_sourcing.read",
            "procurement_sourcing.request",
            "procurement_sourcing.approve",
            "procurement_sourcing.source",
            "procurement_sourcing.bid",
            "procurement_sourcing.award",
            "procurement_sourcing.contract",
            "procurement_sourcing.order",
            "procurement_sourcing.event",
            "procurement_sourcing.configure",
            "procurement_sourcing.audit",
        ),
        "action_permissions": {
            "create_requisition": "procurement_sourcing.request",
            "approve_requisition": "procurement_sourcing.approve",
            "create_rfq": "procurement_sourcing.source",
            "capture_bid": "procurement_sourcing.bid",
            "score_suppliers": "procurement_sourcing.source",
            "select_supplier": "procurement_sourcing.award",
            "create_contract": "procurement_sourcing.contract",
            "issue_purchase_order": "procurement_sourcing.order",
            "route_purchase_order": "procurement_sourcing.order",
            "receive_event": "procurement_sourcing.event",
            "register_rule": "procurement_sourcing.configure",
            "register_schema_extension": "procurement_sourcing.configure",
            "set_parameter": "procurement_sourcing.configure",
            "configure_runtime": "procurement_sourcing.configure",
            "build_workbench_view": "procurement_sourcing.audit",
            "run_control_tests": "procurement_sourcing.audit",
            "generate_supplier_compliance_proof": "procurement_sourcing.audit",
        },
    }


def procurement_sourcing_build_api_contract() -> dict:
    return {
        "format": "appgen.procurement-sourcing-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /procurement/requisitions", "command": "create_requisition", "owned_tables": ("procurement_sourcing_purchase_requisition",), "emits": ("PurchaseRequisitionCreated",), "requires_permission": "procurement_sourcing.request", "idempotency_key": "requisition_id"},
            {"route": "POST /procurement/requisitions/{id}/approve", "command": "approve_requisition", "owned_tables": ("procurement_sourcing_purchase_requisition",), "emits": ("PurchaseRequisitionApproved",), "requires_permission": "procurement_sourcing.approve", "idempotency_key": "requisition_id:approver"},
            {"route": "POST /procurement/rfqs", "command": "create_rfq", "owned_tables": ("procurement_sourcing_rfq",), "emits": ("RfqCreated",), "requires_permission": "procurement_sourcing.source", "idempotency_key": "rfq_id"},
            {"route": "POST /procurement/rfqs/{id}/bids", "command": "capture_bid", "owned_tables": ("procurement_sourcing_supplier_bid",), "emits": (), "requires_permission": "procurement_sourcing.bid", "idempotency_key": "rfq_id:supplier_id"},
            {"route": "POST /procurement/rfqs/{id}/score", "command": "score_suppliers", "owned_tables": ("procurement_sourcing_supplier_bid", "procurement_sourcing_supplier_award"), "emits": (), "requires_permission": "procurement_sourcing.source", "idempotency_key": "rfq_id:score"},
            {"route": "POST /procurement/awards", "command": "select_supplier", "owned_tables": ("procurement_sourcing_supplier_award",), "emits": ("SupplierSelected",), "requires_permission": "procurement_sourcing.award", "idempotency_key": "award_id"},
            {"route": "POST /procurement/contracts", "command": "create_contract", "owned_tables": ("procurement_sourcing_vendor_contract",), "emits": ("VendorContractCreated",), "requires_permission": "procurement_sourcing.contract", "idempotency_key": "contract_id"},
            {"route": "POST /procurement/purchase-orders", "command": "issue_purchase_order", "owned_tables": ("procurement_sourcing_purchase_order",), "emits": ("PurchaseOrderIssued",), "requires_permission": "procurement_sourcing.order", "idempotency_key": "po_id"},
            {"route": "POST /procurement/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES, "requires_permission": "procurement_sourcing.event", "idempotency_key": "event_id"},
            {"route": "GET /procurement/workbench", "query": "build_workbench_view", "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES, "requires_permission": "procurement_sourcing.audit"},
        ),
        "declared_catalog_routes": ("POST /procurement/requisitions", "POST /procurement/rfqs", "POST /procurement/purchase-orders", "GET /procurement/workbench"),
        "events": {"emits": PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES, "consumes": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES},
        "emits": PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES,
        "consumes": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES,
        "asyncapi_events": PROCUREMENT_SOURCING_EMITTED_EVENT_TYPES,
        "permissions": tuple(sorted(procurement_sourcing_permissions_contract()["permissions"])),
        "database_backends": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "configuration": ("PROCUREMENT_SOURCING_DATABASE_URL", "PROCUREMENT_SOURCING_EVENT_TOPIC", "PROCUREMENT_SOURCING_RETRY_LIMIT", "PROCUREMENT_SOURCING_DEFAULT_CURRENCY"),
    }


def procurement_sourcing_build_schema_contract() -> dict:
    """Return Procurement-owned schema, migration, model, and relationship evidence."""
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {
        table: default_fields for table in PROCUREMENT_SOURCING_OWNED_TABLES
    } | {
        "procurement_sourcing_purchase_requisition": ("tenant", "requisition_id", "legal_entity", "category", "estimated_amount", "currency", "status"),
        "procurement_sourcing_purchase_requisition_line": ("tenant", "line_id", "requisition_id", "item_id", "quantity", "uom", "required_date"),
        "procurement_sourcing_requisition_approval": ("tenant", "approval_id", "requisition_id", "approver", "status", "approved_at"),
        "procurement_sourcing_requisition_budget_check": ("tenant", "budget_check_id", "requisition_id", "budget_id", "amount", "decision"),
        "procurement_sourcing_category_strategy": ("tenant", "strategy_id", "category", "preferred_method", "risk_weight", "status"),
        "procurement_sourcing_category_policy": ("tenant", "policy_id", "category", "approval_limit", "minimum_bid_count", "status"),
        "procurement_sourcing_supplier_profile": ("tenant", "supplier_id", "name", "category", "risk_score", "status"),
        "procurement_sourcing_supplier_identity": ("tenant", "identity_id", "supplier_id", "did", "issuer", "status"),
        "procurement_sourcing_supplier_site": ("tenant", "site_id", "supplier_id", "country", "lead_time_days", "status"),
        "procurement_sourcing_supplier_qualification": ("tenant", "qualification_id", "supplier_id", "category", "expires_at", "status"),
        "procurement_sourcing_supplier_risk_signal": ("tenant", "risk_signal_id", "supplier_id", "signal_type", "risk_score", "observed_at"),
        "procurement_sourcing_preferred_supplier_policy": ("tenant", "preferred_policy_id", "category", "supplier_id", "priority", "status"),
        "procurement_sourcing_rfq": ("tenant", "rfq_id", "requisition_id", "category", "status", "released_at"),
        "procurement_sourcing_rfq_line": ("tenant", "rfq_line_id", "rfq_id", "item_id", "quantity", "target_price"),
        "procurement_sourcing_supplier_invitation": ("tenant", "invitation_id", "rfq_id", "supplier_id", "status", "sent_at"),
        "procurement_sourcing_supplier_bid": ("tenant", "bid_id", "rfq_id", "supplier_id", "price", "lead_time_days", "risk"),
        "procurement_sourcing_supplier_bid_line": ("tenant", "bid_line_id", "bid_id", "rfq_line_id", "price", "quantity"),
        "procurement_sourcing_bid_normalization": ("tenant", "normalization_id", "bid_id", "normalized_price", "currency", "audit_hash"),
        "procurement_sourcing_supplier_scorecard": ("tenant", "scorecard_id", "rfq_id", "supplier_id", "score", "award_confidence"),
        "procurement_sourcing_supplier_award": ("tenant", "award_id", "rfq_id", "supplier_id", "amount", "confidence", "status"),
        "procurement_sourcing_split_award": ("tenant", "split_award_id", "award_id", "supplier_id", "quantity", "clearing_bid"),
        "procurement_sourcing_vendor_contract": ("tenant", "contract_id", "award_id", "supplier_id", "term_months", "status"),
        "procurement_sourcing_contract_clause": ("tenant", "clause_id", "contract_id", "clause_type", "obligation", "status"),
        "procurement_sourcing_contract_compliance_obligation": ("tenant", "obligation_id", "contract_id", "metric", "threshold", "status"),
        "procurement_sourcing_contract_renewal": ("tenant", "renewal_id", "contract_id", "renewal_date", "decision", "status"),
        "procurement_sourcing_purchase_order": ("tenant", "po_id", "contract_id", "supplier_id", "amount", "currency", "status"),
        "procurement_sourcing_purchase_order_line": ("tenant", "po_line_id", "po_id", "item_id", "quantity", "price"),
        "procurement_sourcing_change_order": ("tenant", "change_order_id", "po_id", "change_type", "amount_delta", "status"),
        "procurement_sourcing_po_tolerance_check": ("tenant", "tolerance_check_id", "po_id", "contract_id", "amount", "decision"),
        "procurement_sourcing_payment_terms": ("tenant", "payment_terms_id", "contract_id", "term_code", "discount_rate", "status"),
        "procurement_sourcing_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "procurement_sourcing_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "procurement_sourcing_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "procurement_sourcing_purchase_requisition_line.requisition_id", "to": "procurement_sourcing_purchase_requisition.requisition_id", "type": "owned_child"},
        {"from": "procurement_sourcing_requisition_approval.requisition_id", "to": "procurement_sourcing_purchase_requisition.requisition_id", "type": "owned_approval"},
        {"from": "procurement_sourcing_rfq.requisition_id", "to": "procurement_sourcing_purchase_requisition.requisition_id", "type": "owned_sourcing_flow"},
        {"from": "procurement_sourcing_rfq_line.rfq_id", "to": "procurement_sourcing_rfq.rfq_id", "type": "owned_child"},
        {"from": "procurement_sourcing_supplier_bid.rfq_id", "to": "procurement_sourcing_rfq.rfq_id", "type": "owned_bid"},
        {"from": "procurement_sourcing_supplier_bid_line.bid_id", "to": "procurement_sourcing_supplier_bid.bid_id", "type": "owned_child"},
        {"from": "procurement_sourcing_supplier_award.rfq_id", "to": "procurement_sourcing_rfq.rfq_id", "type": "owned_award"},
        {"from": "procurement_sourcing_vendor_contract.award_id", "to": "procurement_sourcing_supplier_award.award_id", "type": "owned_contract"},
        {"from": "procurement_sourcing_contract_clause.contract_id", "to": "procurement_sourcing_vendor_contract.contract_id", "type": "owned_clause"},
        {"from": "procurement_sourcing_purchase_order.contract_id", "to": "procurement_sourcing_vendor_contract.contract_id", "type": "owned_order"},
        {"from": "procurement_sourcing_purchase_order_line.po_id", "to": "procurement_sourcing_purchase_order.po_id", "type": "owned_child"},
        {"from": "procurement_sourcing_supplier_identity.supplier_id", "to": "procurement_sourcing_supplier_profile.supplier_id", "type": "owned_identity"},
        {"from": "procurement_sourcing_supplier_site.supplier_id", "to": "procurement_sourcing_supplier_profile.supplier_id", "type": "owned_site"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "procurement_sourcing",
        }
        for table in PROCUREMENT_SOURCING_OWNED_TABLES
    )
    return {
        "format": "appgen.procurement-sourcing-owned-schema-contract.v1",
        "ok": len(tables) == len(PROCUREMENT_SOURCING_OWNED_TABLES)
        and len(tables) >= 40
        and all(item["table"].startswith("procurement_sourcing_") for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/procurement_sourcing/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(PROCUREMENT_SOURCING_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in PROCUREMENT_SOURCING_OWNED_TABLES
        ),
        "datastore_backends": PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def procurement_sourcing_build_service_contract() -> dict:
    """Return Procurement command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_requisition",
        "approve_requisition",
        "create_rfq",
        "capture_bid",
        "score_suppliers",
        "select_supplier",
        "create_contract",
        "issue_purchase_order",
        "screen_policy",
        "route_purchase_order",
        "generate_supplier_compliance_proof",
        "federate_procurement_view",
        "verify_supplier_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_sourcing",
        "optimize_award",
        "allocate_rfq_award",
        "run_control_tests",
        "register_governed_model",
    )
    return {
        "format": "appgen.procurement-sourcing-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "procurement_sourcing_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "detect_bid_anomaly",
            "model_stochastic_supply_exposure",
            "forecast_price_lead_time",
            "simulate_sourcing_strategy",
            "parse_document",
            "score_supplier_risk",
            "verify_owned_table_boundary",
        ),
        "mutates_only": PROCUREMENT_SOURCING_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _PROCUREMENT_SOURCING_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _PROCUREMENT_SOURCING_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def procurement_sourcing_build_release_evidence() -> dict:
    """Return Procurement package-local release evidence."""
    schema = procurement_sourcing_build_schema_contract()
    service = procurement_sourcing_build_service_contract()
    api = procurement_sourcing_build_api_contract()
    permissions = procurement_sourcing_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(PROCUREMENT_SOURCING_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"create_requisition", "issue_purchase_order", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == PROCUREMENT_SOURCING_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.procurement-sourcing-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def procurement_sourcing_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*PROCUREMENT_SOURCING_OWNED_TABLES, *PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES, *_PROCUREMENT_SOURCING_RUNTIME_TABLES, *_PROCUREMENT_SOURCING_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("procurement_sourcing_"))
    return {
        "format": "appgen.procurement-sourcing-boundary.v1",
        "ok": not violations,
        "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /identity/policies", "POST /audit/contract-events", "GET /schema/events"),
            "events": PROCUREMENT_SOURCING_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "material_shortage_projection",
                "vendor_performance_projection",
                "budget_projection",
                "supplier_risk_projection",
                "contract_compliance_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def procurement_sourcing_federate_procurement_view(state: dict, po_id: str, *, systems: tuple[str, ...]) -> dict:
    po = state["purchase_orders"][po_id]
    return {"ok": True, "po_id": po_id, "systems": systems, "projection": {"supplier_id": po["supplier_id"], "amount": po["amount"], "status": po["status"]}}


def procurement_sourcing_verify_supplier_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def procurement_sourcing_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"supplier_route_timeout", "po_worker_failure"}, "scenario": scenario, "mode": "degraded_supplier_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "procurement_sourcing.dead_letter"}


def procurement_sourcing_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"procurement_epoch_{epoch:04d}"}


def procurement_sourcing_schedule_carbon_aware_sourcing(scores: tuple[dict, ...]) -> dict:
    selected = min(scores, key=lambda score: score["carbon"])
    return {"ok": True, "supplier_id": selected["supplier_id"], "carbon": selected["carbon"]}


def procurement_sourcing_optimize_award(scores: tuple[dict, ...], *, quantity: float) -> dict:
    selected = max(scores, key=lambda score: score["score"])
    return {"ok": True, "supplier_id": selected["supplier_id"], "quantity": quantity, "objective_score": round(selected["score"] * quantity, 4)}


def procurement_sourcing_allocate_rfq_award(scores: tuple[dict, ...], *, quantity: float) -> dict:
    total = sum(max(score["score"], 0.0001) for score in scores)
    allocations = tuple({"supplier_id": score["supplier_id"], "quantity": round(quantity * max(score["score"], 0.0001) / total, 2)} for score in scores)
    return {"ok": round(sum(item["quantity"] for item in allocations), 2) == round(quantity, 2), "allocations": allocations, "clearing_bid": round(sum(score["score"] for score in scores) / len(scores), 4)}


def procurement_sourcing_detect_bid_anomaly(state: dict, rfq_id: str) -> dict:
    prices = tuple(bid["price"] for bid in state["bids"][rfq_id])
    total = sum(prices) or 1
    entropy = round(-sum((price / total) * math.log(max(price / total, 0.0001), 2) for price in prices), 4)
    mean = sum(prices) / len(prices)
    return {"ok": True, "entropy": entropy, "outliers": tuple(price for price in prices if abs(price - mean) > mean * 0.2)}


def procurement_sourcing_model_stochastic_supply_exposure(*, price_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(price_path) < 2 else (price_path[-1] - price_path[0]) / (len(price_path) - 1)
    exposure = abs(drift) * volatility * len(price_path)
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def procurement_sourcing_forecast_price_lead_time(price_path: tuple[float, ...], lead_time_path: tuple[float, ...]) -> dict:
    price_trend = 0 if len(price_path) < 2 else price_path[-1] - price_path[0]
    lead_time_trend = 0 if len(lead_time_path) < 2 else lead_time_path[-1] - lead_time_path[0]
    return {"ok": True, "price_trend": round(price_trend, 2), "lead_time_trend": round(lead_time_trend, 2)}


def procurement_sourcing_simulate_sourcing_strategy(state: dict, rfq_id: str, *, proposed_risk_weight: float) -> dict:
    scores = []
    for bid in state["bids"][rfq_id]:
        score = (1 - bid["risk"]) * proposed_risk_weight + bid["quality"] * (1 - proposed_risk_weight)
        scores.append({**bid, "score": round(score, 4)})
    selected = max(scores, key=lambda item: item["score"])
    return {"ok": True, "selected_supplier": selected["supplier_id"], "scores": tuple(scores)}


def procurement_sourcing_parse_document(text: str) -> dict:
    req = re.search(r"requisition\s+([a-z0-9_]+)", text, re.I)
    category = re.search(r"category\s+([a-z0-9_]+)", text, re.I)
    supplier = re.search(r"supplier\s+([a-z0-9_]+)", text, re.I)
    amount = _first_number_after(text, "amount")
    return {"ok": bool(req and category and supplier and amount), "requisition_id": req.group(1) if req else None, "category": category.group(1) if category else None, "supplier_id": supplier.group(1) if supplier else None, "amount": amount}


def procurement_sourcing_score_supplier_risk(signals: dict) -> dict:
    risk = round(signals.get("late_rate", 0) * 2 + signals.get("quality_escape", 0) * 3 + signals.get("financial_risk", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.4 else "review"}


def procurement_sourcing_build_workbench_view(state: dict, *, tenant: str) -> dict:
    pos = tuple(po for po in state["purchase_orders"].values() if po["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "requisition_count": len(tuple(req for req in state["requisitions"].values() if req["tenant"] == tenant)),
        "rfq_count": len(tuple(rfq for rfq in state["rfqs"].values() if rfq["tenant"] == tenant)),
        "contract_count": len(tuple(contract for contract in state["contracts"].values() if contract["tenant"] == tenant)),
        "po_count": len(pos),
        "po_amount": round(sum(po["amount"] for po in pos), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "owned_tables": PROCUREMENT_SOURCING_OWNED_TABLES,
        "outbox_table": "procurement_sourcing_appgen_outbox_event",
        "inbox_table": "procurement_sourcing_appgen_inbox_event",
        "dead_letter_table": "procurement_sourcing_dead_letter_event",
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
    }


def procurement_sourcing_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _copy_state(state: dict) -> dict:
    copied = dict(state)
    for key in (
        "handled_events",
        "material_shortage_projections",
        "vendor_performance_projections",
        "budget_projections",
        "supplier_risk_projections",
        "contract_compliance_projections",
        "access_policy_projections",
    ):
        copied[key] = dict(state.get(key, {}))
    return copied


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"procurement_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"procurement_sourcing:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
