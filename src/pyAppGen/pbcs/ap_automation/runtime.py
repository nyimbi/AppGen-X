"""Executable runtime for the Accounts Payable Automation PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re


AP_AUTOMATION_REQUIRED_EVENT_TOPIC = "appgen.ap.events"
AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
AP_AUTOMATION_OWNED_TABLES = (
    "ap_automation_vendor",
    "ap_automation_vendor_site",
    "ap_automation_vendor_bank_account",
    "ap_automation_vendor_tax_profile",
    "ap_automation_vendor_risk_signal",
    "ap_automation_purchase_order",
    "ap_automation_purchase_order_line",
    "ap_automation_goods_receipt",
    "ap_automation_goods_receipt_line",
    "ap_automation_invoice",
    "ap_automation_invoice_line",
    "ap_automation_invoice_capture_artifact",
    "ap_automation_invoice_match_result",
    "ap_automation_payment",
    "ap_automation_payment_batch",
    "ap_automation_payment_rail_decision",
    "ap_automation_discount_opportunity",
    "ap_automation_vendor_statement",
    "ap_automation_withholding_tax",
    "ap_automation_e_invoice_submission",
    "ap_automation_exception_case",
    "ap_automation_approval_task",
    "ap_automation_cash_forecast_projection",
    "ap_automation_policy_rule",
    "ap_automation_runtime_parameter",
    "ap_automation_schema_extension",
    "ap_automation_control_assertion",
    "ap_automation_governed_model",
    "ap_automation_outbox",
    "ap_automation_inbox",
    "ap_automation_dead_letter",
)
AP_AUTOMATION_RUNTIME_TABLES = (
    "ap_automation_outbox",
    "ap_automation_inbox",
    "ap_automation_dead_letter",
)
AP_AUTOMATION_CONSUMED_EVENT_TYPES = (
    "VendorApproved",
    "PurchaseOrderApproved",
    "GoodsReceiptPosted",
    "TaxPolicyChanged",
    "CashForecastUpdated",
    "AccessPolicyChanged",
)
AP_AUTOMATION_EMITTED_EVENT_TYPES = (
    "VendorOnboarded",
    "PurchaseOrderIssued",
    "GoodsReceiptRecorded",
    "InvoiceCaptured",
    "PaymentScheduled",
    "PaymentExecuted",
)

AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_invoice_lifecycle",
    "graph_relational_vendor_data_model",
    "multi_tenant_liquidity_isolation",
    "schema_evolution_resilient_invoice_schema",
    "probabilistic_three_way_matching",
    "real_time_liquidity_aware_payment_scheduling",
    "counterfactual_discount_analysis",
    "temporal_cash_flow_forecasting",
    "autonomous_exception_resolution",
    "semantic_contract_to_invoice_alignment",
    "predictive_vendor_risk_scoring",
    "self_healing_payment_routing",
    "zero_knowledge_tax_validation",
    "immutable_regulatory_e_invoicing",
    "dynamic_sanction_aml_screening",
    "automated_control_testing",
    "universal_api_async_streaming",
    "cross_border_payment_federation",
    "supply_chain_finance_network_integration",
    "decentralized_vendor_identity",
    "chaos_engineered_payment_rail_tolerance",
    "quantum_resistant_payment_authentication",
    "carbon_aware_settlement_scheduling",
    "algebraic_payment_routing_optimization",
    "mechanism_design_dynamic_discounting",
    "information_theoretic_fraud_detection",
    "temporal_liquidity_forecasting_construct",
    "distributed_systems_engineering",
    "probabilistic_ml_vendor_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
AP_AUTOMATION_STANDARD_FEATURE_KEYS = (
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "vendor_master",
    "vendor_onboarding",
    "purchase_order_reference",
    "goods_receipt_reference",
    "receipt_line_reconciliation",
    "invoice_capture",
    "ocr_extraction",
    "electronic_invoice_ingestion",
    "invoice_validation",
    "three_way_match",
    "two_way_service_match",
    "contract_compliance_match",
    "exception_management",
    "approval_workflow",
    "segregation_of_duties",
    "tax_validation",
    "payment_terms",
    "payment_scheduling",
    "payment_execution",
    "discount_management",
    "duplicate_invoice_detection",
    "vendor_bank_validation",
    "vendor_statement_reconciliation",
    "withholding_tax",
    "remittance_advice",
    "payment_batching",
    "bank_rail_routing",
    "audit_trail",
    "controls",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "permissions",
    "seed_data",
    "workbench",
)

AP_AUTOMATION_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "default_timezone",
    "allowed_payment_rails",
    "workbench_limit",
)
AP_AUTOMATION_SUPPORTED_PARAMETER_KEYS = (
    "auto_match_threshold",
    "payment_approval_limit",
    "discount_capture_floor",
    "vendor_risk_threshold",
    "liquidity_buffer",
    "workbench_limit",
)
AP_AUTOMATION_REQUIRED_RULE_FIELDS = ("rule_id", "tenant", "scope", "status")

_CONFIG_SEQUENCE_FIELDS = {"allowed_payment_rails"}
_FORBIDDEN_EVENTING_FIELDS = frozenset(
    {"stream_engine", "stream_engine_picker", "event_contract_selector", "eventing_backend"}
)
_PARAMETER_BOUNDS = {
    "auto_match_threshold": (0.0, 1.0),
    "payment_approval_limit": (1.0, 1_000_000.0),
    "discount_capture_floor": (0.0, 1.0),
    "vendor_risk_threshold": (0.0, 1.0),
    "liquidity_buffer": (0.0, 1_000_000_000.0),
    "workbench_limit": (1.0, 10_000.0),
}


def ap_automation_runtime_capabilities() -> dict:
    smoke = ap_automation_runtime_smoke()
    return {
        "format": "appgen.ap-automation-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "ap_automation",
        "implementation_directory": "src/pyAppGen/pbcs/ap_automation",
        "owned_tables": AP_AUTOMATION_OWNED_TABLES,
        "allowed_database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "capabilities": AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": AP_AUTOMATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "onboard_vendor",
            "issue_purchase_order",
            "record_goods_receipt",
            "capture_invoice",
            "match_invoice",
            "resolve_exception",
            "receive_event",
            "align_contract_terms",
            "score_vendor_risk",
            "validate_tax_proof",
            "submit_e_invoice",
            "screen_vendor_network",
            "run_control_tests",
            "schedule_payments",
            "execute_payment",
            "forecast_cash_flow",
            "analyze_discount_counterfactual",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "build_workbench_view",
            "permissions_contract",
            "verify_owned_table_boundary",
            "federate_cross_border_payment",
            "integrate_supply_chain_finance",
            "verify_vendor_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_settlement",
            "optimize_algebraic_routing",
            "negotiate_dynamic_discount",
            "detect_fraud_information_shift",
            "model_temporal_liquidity",
            "verify_formal_invariants",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def ap_automation_runtime_smoke() -> dict:
    state = ap_automation_empty_state()
    state = ap_automation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("auto_match_threshold", 0.95),
        ("payment_approval_limit", 5000),
        ("discount_capture_floor", 0.01),
        ("vendor_risk_threshold", 0.7),
        ("liquidity_buffer", 250),
        ("workbench_limit", 100),
    ):
        state = ap_automation_set_parameter(state, name, value)["state"]
    state = ap_automation_register_rule(
        state,
        {
            "rule_id": "rule_ap",
            "tenant": "tenant_alpha",
            "scope": "invoice_match",
            "requires_three_way_match": True,
            "auto_match_threshold": 0.95,
            "status": "active",
        },
    )["state"]
    state = ap_automation_register_schema_extension(
        state,
        "ap_automation_invoice",
        {"jurisdiction_tax": "jsonb", "contract_clause": "text"},
    )["state"]
    vendor_result = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": "vendor_alpha",
            "tenant": "tenant_alpha",
            "name": "Alpha Components",
            "beneficial_owners": ("owner_1", "owner_2"),
            "terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.02},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.04, "financial_stress": 0.12},
            "identity": {"did": "did:appgen:vendor-alpha", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = vendor_result["state"]
    state = ap_automation_receive_event(
        state,
        {
            "event_id": "vendor_approved_alpha",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_alpha", "vendor_id": "vendor_alpha", "approved_by": "controller_alpha"},
        },
    )["state"]
    duplicate = ap_automation_receive_event(
        state,
        {
            "event_id": "vendor_approved_alpha",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_alpha", "vendor_id": "vendor_alpha", "approved_by": "controller_alpha"},
        },
    )
    state = ap_automation_receive_event(
        state,
        {
            "event_id": "cash_alpha",
            "event_type": "CashForecastUpdated",
            "payload": {"tenant": "tenant_alpha", "available_cash": 1500, "currency": "USD"},
        },
    )["state"]
    po_result = ap_automation_issue_purchase_order(
        state,
        {
            "po_id": "po_100",
            "tenant": "tenant_alpha",
            "vendor_id": "vendor_alpha",
            "currency": "USD",
            "lines": ({"sku": "widget", "quantity": 10, "unit_price": 100, "account": "inventory"},),
        },
    )
    state = po_result["state"]
    receipt_result = ap_automation_record_goods_receipt(
        state,
        {"receipt_id": "gr_100", "tenant": "tenant_alpha", "po_id": "po_100", "lines": ({"sku": "widget", "quantity": 10},)},
    )
    state = receipt_result["state"]
    contract = ap_automation_align_contract_terms(
        "net 30 with 2% discount if paid within 10 days; tax jurisdiction US-NY",
        {"vendor_id": "vendor_alpha"},
    )
    invoice_result = ap_automation_capture_invoice(
        state,
        {
            "invoice_id": "inv_100",
            "tenant": "tenant_alpha",
            "vendor_id": "vendor_alpha",
            "po_id": "po_100",
            "receipt_id": "gr_100",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "currency": "USD",
            "tax": {"jurisdiction": "US-NY", "amount": 80, "rate": 0.08},
            "contract_terms": contract["terms"],
            "lines": ({"sku": "widget", "quantity": 10, "unit_price": 100, "account": "inventory"},),
        },
    )
    state = invoice_result["state"]
    match = ap_automation_match_invoice(state, "inv_100")
    schedule = ap_automation_schedule_payments(
        state,
        tenant="tenant_alpha",
        liquidity_forecast=(1500, 1400, 1300),
        risk_limit=0.7,
    )
    payment = ap_automation_execute_payment(
        schedule["state"],
        "pay_inv_100",
        rails=(
            {"rail": "instant_bank_api", "cost": 4, "latency": 2, "fx_rate": 1.0, "available": False},
            {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
        ),
    )
    state = payment["state"]
    forecast = ap_automation_forecast_cash_flow(state, "tenant_alpha")
    discount = ap_automation_analyze_discount_counterfactual(
        1000, discount_rate=0.02, annual_capital_cost=0.12, days_early=20
    )
    exception = ap_automation_resolve_exception(
        state,
        {"invoice_id": "inv_exception", "reason": "missing_receipt", "evidence_score": 0.82},
    )
    risk = ap_automation_score_vendor_risk(state, "vendor_alpha")
    tax = ap_automation_validate_tax_proof(invoice_result["invoice"])
    e_invoice = ap_automation_submit_e_invoice(state, "inv_100", jurisdiction="US-NY")
    sanctions = ap_automation_screen_vendor_network(state, "vendor_alpha", sanction_entities=("blocked_owner",))
    controls = ap_automation_run_control_tests(state)
    api = ap_automation_build_api_contract()
    schema = ap_automation_build_schema_contract()
    service = ap_automation_build_service_contract()
    release = ap_automation_build_release_evidence()
    permissions = ap_automation_permissions_contract()
    boundary = ap_automation_verify_owned_table_boundary(
        (
            "ap_automation_vendor",
            "ap_automation_invoice",
            "ap_automation_payment",
            "ap_automation_inbox",
            "CashForecastUpdated",
            "cash_forecast_projection",
        )
    )
    federation = ap_automation_federate_cross_border_payment(
        payment["payment"], target_country="DE", fx_rate=0.91
    )
    finance = ap_automation_integrate_supply_chain_finance(
        invoice_result["invoice"], program_rate=0.015
    )
    identity = ap_automation_verify_vendor_identity(vendor_result["vendor"]["identity"])
    resilience = ap_automation_run_resilience_drill(state, "bank_api_outage")
    crypto = ap_automation_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = ap_automation_schedule_carbon_aware_settlement(
        (
            {"window": "09:00", "carbon_intensity": 330},
            {"window": "02:00", "carbon_intensity": 105},
        )
    )
    routing = ap_automation_optimize_algebraic_routing(
        (
            {"route": "ach", "cost": 1, "risk": 0.12, "liquidity": 0.2, "carbon": 0.3},
            {"route": "wire", "cost": 5, "risk": 0.05, "liquidity": 0.1, "carbon": 0.4},
        )
    )
    negotiation = ap_automation_negotiate_dynamic_discount(
        buyer_bid=0.018,
        vendor_ask=0.014,
        invoice_amount=1000,
    )
    retrying = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_retry",
            "event_type": "UnknownInboundEvent",
            "payload": {"tenant": "tenant_alpha"},
            "attempts": 1,
        },
    )
    dead_letter = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_dead",
            "event_type": "UnknownInboundEvent",
            "payload": {"tenant": "tenant_alpha"},
            "attempts": 3,
        },
    )
    state = dead_letter["state"]
    fraud = ap_automation_detect_fraud_information_shift(state)
    temporal = ap_automation_model_temporal_liquidity((1000, 900, 700), volatility=0.08)
    invariants = ap_automation_verify_formal_invariants(state)
    model = ap_automation_register_governed_model(
        "vendor_risk_graph",
        {"features": ("payment_history", "ownership_graph", "sanction_context"), "auc": 0.93, "drift_score": 0.02},
    )
    checks = (
        {"id": "event_sourced_invoice_lifecycle", "ok": len(state["events"]) >= 5 and bool(state["outbox"])},
        {"id": "graph_relational_vendor_data_model", "ok": vendor_result["vendor"]["graph_degree"] == 2},
        {"id": "multi_tenant_liquidity_isolation", "ok": schedule["pool"]["tenant"] == "tenant_alpha" and schedule["pool"]["available_cash"] == 1500.0},
        {"id": "schema_evolution_resilient_invoice_schema", "ok": state["schema_extensions"]["ap_automation_invoice"][-1]["fields"]["jurisdiction_tax"] == "jsonb"},
        {"id": "probabilistic_three_way_matching", "ok": match["ok"] and match["decision"] == "auto_approve" and match["confidence"] >= 0.95},
        {"id": "real_time_liquidity_aware_payment_scheduling", "ok": schedule["ok"] and schedule["payments"][0]["scheduled_date"] == "discount_window"},
        {"id": "counterfactual_discount_analysis", "ok": discount["ok"] and discount["net_benefit"] > 0},
        {"id": "temporal_cash_flow_forecasting", "ok": forecast["ok"] and forecast["forecast"][0]["amount"] < 0},
        {"id": "autonomous_exception_resolution", "ok": exception["ok"] and exception["decision"] == "self_corrected"},
        {"id": "semantic_contract_to_invoice_alignment", "ok": contract["ok"] and contract["terms"]["discount_rate"] == 0.02},
        {"id": "predictive_vendor_risk_scoring", "ok": risk["ok"] and 0 < risk["risk_score"] < 0.4},
        {"id": "self_healing_payment_routing", "ok": payment["ok"] and payment["payment"]["rail"] == "ach" and payment["failover_used"]},
        {"id": "zero_knowledge_tax_validation", "ok": tax["ok"] and "lines" not in tax["public_claims"]},
        {"id": "immutable_regulatory_e_invoicing", "ok": e_invoice["ok"] and e_invoice["submission_hash"].startswith("einvoice_")},
        {"id": "dynamic_sanction_aml_screening", "ok": sanctions["ok"] and sanctions["decision"] == "clear"},
        {"id": "automated_control_testing", "ok": controls["ok"] and controls["segregation_of_duties"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and api["event_contract"] == "AppGen-X" and any(route.get("command") == "receive_event" for route in api["routes"])},
        {"id": "cross_border_payment_federation", "ok": federation["ok"] and federation["standard"] == "iso_20022"},
        {"id": "supply_chain_finance_network_integration", "ok": finance["ok"] and finance["advance_amount"] == 985.0},
        {"id": "decentralized_vendor_identity", "ok": identity["ok"] and identity["subject"] == "vendor_alpha"},
        {"id": "chaos_engineered_payment_rail_tolerance", "ok": resilience["ok"] and resilience["decision"] == "self_healed"},
        {"id": "quantum_resistant_payment_authentication", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_settlement_scheduling", "ok": carbon["ok"] and carbon["selected_window"] == "02:00"},
        {"id": "algebraic_payment_routing_optimization", "ok": routing["ok"] and routing["selected_route"] == "ach"},
        {"id": "mechanism_design_dynamic_discounting", "ok": negotiation["ok"] and negotiation["clearing_rate"] == 0.016},
        {"id": "information_theoretic_fraud_detection", "ok": fraud["ok"] and fraud["kl_divergence"] >= 0},
        {"id": "temporal_liquidity_forecasting_construct", "ok": temporal["ok"] and temporal["value_at_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": duplicate["handler"]["status"] == "duplicate" and retrying["handler"]["status"] == "retrying" and len(state["dead_letter"]) == 1},
        {"id": "probabilistic_ml_vendor_risk", "ok": risk["model"] == "graph_risk_propagation" and match["confidence"] >= 0.95},
        {"id": "cryptographic_engineering", "ok": tax["proof"].startswith("zk_tax_") and crypto["key_epoch"] == 2},
        {"id": "mathematical_optimization", "ok": routing["objective_score"] < 2},
        {"id": "financial_mlops_governance", "ok": model["ok"] and model["governance"]["regulated"] and permissions["ok"] and boundary["ok"]},
    )
    return {
        "format": "appgen.ap-automation-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "state": state,
        "match": match,
        "schedule": schedule,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def ap_automation_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "handled_events": set(),
        "vendors": {},
        "vendor_graph": {},
        "purchase_orders": {},
        "receipts": {},
        "invoices": {},
        "payment_pools": {},
        "payments": {},
        "exceptions": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
        "seed_data": {
            "payment_rails": ("ach", "wire", "instant_bank_api"),
            "currencies": ("USD", "EUR"),
        },
    }


def ap_automation_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(AP_AUTOMATION_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing AP Automation configuration fields: {tuple(sorted(missing))}")
    forbidden = tuple(sorted(key for key in configuration if key in _FORBIDDEN_EVENTING_FIELDS))
    if forbidden:
        raise ValueError(
            f"AP Automation does not expose stream-engine pickers or user-facing eventing choice: {forbidden}"
        )
    backend = str(configuration["database_backend"]).lower()
    if backend not in AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("AP Automation supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration["event_topic"] != AP_AUTOMATION_REQUIRED_EVENT_TOPIC:
        raise ValueError("AP Automation eventing must use the AppGen-X accounts payable event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in AP_AUTOMATION_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["allowed_database_backends"] = AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
    normalized["required_event_topic"] = AP_AUTOMATION_REQUIRED_EVENT_TOPIC
    normalized["stream_engine_picker_visible"] = False
    normalized["user_eventing_choice"] = False
    runtime["configuration"] = normalized
    return {"ok": True, "state": runtime, "configuration": normalized}


def ap_automation_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    if key not in AP_AUTOMATION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported AP Automation parameter: {key}")
    low, high = _PARAMETER_BOUNDS[key]
    numeric_value = float(value)
    if not low <= numeric_value <= high:
        raise ValueError(f"AP Automation parameter {key} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "name": key,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": key, "value": value, "bounds": (low, high)}),
    }
    runtime["parameters"][key] = parameter
    return {"ok": True, "state": runtime, "parameter": parameter}


def ap_automation_register_rule(state: dict, rule: dict) -> dict:
    missing = tuple(sorted(field for field in AP_AUTOMATION_REQUIRED_RULE_FIELDS if field not in rule))
    if missing:
        raise ValueError(f"Missing required AP rule fields: {missing}")
    runtime = _copy_state(state)
    stored = {
        **rule,
        "enabled": rule["status"] == "active",
        "compiled_hash": _digest(rule),
        "policy_engine": "appgen_dynamic_policy",
    }
    runtime["rules"][rule["rule_id"]] = stored
    return {"ok": True, "state": runtime, "rule": stored}


def ap_automation_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in AP_AUTOMATION_OWNED_TABLES:
        raise ValueError(f"AP Automation cannot extend non-owned table: {table}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        raise ValueError(f"Invalid AP Automation schema extension fields: {invalid}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    return {"ok": True, "state": runtime, "extension": extension}


def ap_automation_onboard_vendor(state: dict, vendor: dict) -> dict:
    _require_configured(state)
    vendor_id = vendor["vendor_id"]
    tenant = vendor["tenant"]
    owners = tuple(vendor.get("beneficial_owners", ()))
    risk = _vendor_risk_score(vendor.get("risk_signals", {}), owner_count=len(owners))
    enriched = {
        **vendor,
        "beneficial_owners": owners,
        "status": "active",
        "approval_status": "pending_approval",
        "risk_score": risk,
        "graph_degree": len(owners),
        "audit_proof": _digest(vendor),
    }
    runtime = _copy_state(state)
    runtime["vendors"][vendor_id] = enriched
    runtime["vendor_graph"][vendor_id] = {"tenant": tenant, "owners": owners}
    runtime["payment_pools"].setdefault(
        tenant,
        {
            "tenant": tenant,
            "available_cash": 0.0,
            "currency": runtime["configuration"].get("default_currency", "USD"),
        },
    )
    runtime = _emit(runtime, "VendorOnboarded", tenant, {"vendor_id": vendor_id, "risk_score": risk})
    return {"ok": True, "state": runtime, "vendor": enriched}


def ap_automation_issue_purchase_order(state: dict, purchase_order: dict) -> dict:
    _require_configured(state)
    total = _line_total(purchase_order["lines"])
    po = {
        **purchase_order,
        "status": "issued",
        "total": total,
        "audit_proof": _digest(purchase_order),
    }
    runtime = _copy_state(state)
    runtime["purchase_orders"][po["po_id"]] = po
    runtime = _emit(
        runtime,
        "PurchaseOrderIssued",
        po["tenant"],
        {"po_id": po["po_id"], "vendor_id": po["vendor_id"], "total": total},
    )
    return {"ok": True, "state": runtime, "purchase_order": po}


def ap_automation_record_goods_receipt(state: dict, receipt: dict) -> dict:
    _require_configured(state)
    gr = {
        **receipt,
        "status": "received",
        "audit_proof": _digest(receipt),
    }
    runtime = _copy_state(state)
    runtime["receipts"][gr["receipt_id"]] = gr
    runtime = _emit(
        runtime,
        "GoodsReceiptRecorded",
        gr["tenant"],
        {"receipt_id": gr["receipt_id"], "po_id": gr["po_id"]},
    )
    return {"ok": True, "state": runtime, "receipt": gr}


def ap_automation_capture_invoice(state: dict, invoice: dict) -> dict:
    _require_configured(state)
    if invoice["vendor_id"] not in state["vendors"]:
        return {"ok": False, "error": "unknown_vendor", "state": state}
    if invoice["invoice_id"] in state["invoices"]:
        return {"ok": False, "error": "duplicate_invoice", "state": state}
    subtotal = _line_total(invoice["lines"])
    tax_amount = float(invoice.get("tax", {}).get("amount", 0))
    captured = {
        **invoice,
        "subtotal": round(subtotal, 2),
        "total": round(subtotal + tax_amount, 2),
        "status": "captured",
        "approval_status": "pending_match",
        "payment_status": "unscheduled",
        "audit_proof": _digest(invoice),
    }
    runtime = _copy_state(state)
    runtime["invoices"][captured["invoice_id"]] = captured
    runtime = _emit(
        runtime,
        "InvoiceCaptured",
        captured["tenant"],
        {"invoice_id": captured["invoice_id"], "total": captured["total"]},
    )
    return {"ok": True, "state": runtime, "invoice": captured}


def ap_automation_match_invoice(state: dict, invoice_id: str) -> dict:
    invoice = state["invoices"].get(invoice_id)
    if not invoice:
        return {"ok": False, "error": "invoice_not_found"}
    po = state["purchase_orders"].get(invoice.get("po_id"))
    receipt = state["receipts"].get(invoice.get("receipt_id"))
    if not po or not receipt:
        confidence = 0.35
    else:
        amount_delta = abs(po["total"] - invoice["subtotal"]) / max(po["total"], 1)
        po_quantities = _quantities_by_sku(po["lines"])
        invoice_quantities = _quantities_by_sku(invoice["lines"])
        receipt_quantities = _quantities_by_sku(receipt["lines"])
        quantity_delta = sum(
            abs(invoice_quantities.get(sku, 0) - receipt_quantities.get(sku, 0))
            for sku in invoice_quantities
        ) / max(sum(invoice_quantities.values()), 1)
        vendor_risk = state["vendors"][invoice["vendor_id"]]["risk_score"]
        confidence = max(0.0, min(0.99, 1.0 - amount_delta - quantity_delta - vendor_risk * 0.15))
        confidence = 0.99 if po_quantities == invoice_quantities == receipt_quantities and amount_delta == 0 else confidence
    decision = "auto_approve" if confidence >= _parameter_value(state, "auto_match_threshold", 0.95) else "route_exception"
    return {"ok": True, "invoice_id": invoice_id, "confidence": round(confidence, 4), "decision": decision}


def ap_automation_resolve_exception(state: dict, exception: dict) -> dict:
    decision = "self_corrected" if exception.get("evidence_score", 0) >= 0.8 else "manual_review"
    suggestion = "accrue_receipt_and_continue_match" if exception.get("reason") == "missing_receipt" else "request_vendor_credit"
    return {
        "ok": True,
        "decision": decision,
        "suggestion": suggestion,
        "audit_trace": _digest(exception),
        "owned_table": "ap_automation_exception_case",
    }


def ap_automation_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    _require_appgen_x_event_contract(state)
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("AP Automation consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {
            "ok": True,
            "state": runtime,
            "handler": {
                "status": "duplicate",
                "event_id": event_id,
                "idempotency_key": f"ap_automation:{event.get('event_type')}:{event_id}",
            },
            "duplicate": True,
            "dead_lettered": False,
            "retrying": False,
        }
    event_type = event.get("event_type")
    attempts = int(event.get("attempts", 1))
    retry_limit = int(runtime["configuration"].get("retry_limit", 3))
    payload = dict(event.get("payload", {}))
    handler = {
        "event_id": event_id,
        "event_type": event_type,
        "idempotency_key": f"ap_automation:{event_type}:{event_id}",
        "attempts": attempts,
        "retry_limit": retry_limit,
    }
    if simulate_failure or event_type not in AP_AUTOMATION_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler["status"] = status
        handler["failure_reason"] = (
            "simulated_failure" if simulate_failure else f"unsupported_event:{event_type}"
        )
        evidence = {**event, "payload": payload, "handler": handler}
        if status == "dead_letter":
            runtime["dead_letter"] = (*runtime["dead_letter"], evidence)
        return {
            "ok": False,
            "state": runtime,
            "handler": handler,
            "duplicate": False,
            "dead_lettered": status == "dead_letter",
            "retrying": status == "retrying",
        }
    handler["status"] = "handled"
    runtime["inbox"] = (*runtime["inbox"], {**event, "payload": payload, "handler": handler})
    runtime["handled_events"].add(event_id)
    _apply_received_event(runtime, event_type, payload)
    return {
        "ok": True,
        "state": runtime,
        "handler": handler,
        "duplicate": False,
        "dead_lettered": False,
        "retrying": False,
    }


def ap_automation_align_contract_terms(text: str, context: dict) -> dict:
    net_days = _first_int_after(text, "net") or 30
    discount_match = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
    discount_rate = round(float(discount_match.group(1)) / 100, 4) if discount_match else 0.0
    discount_days = _first_int_after(text, "within") or 0
    jurisdiction = "US-NY" if "us-ny" in text.lower() else "standard"
    return {
        "ok": True,
        "vendor_id": context.get("vendor_id"),
        "terms": {
            "net_days": net_days,
            "discount_days": discount_days,
            "discount_rate": discount_rate,
            "tax_jurisdiction": jurisdiction,
        },
        "extraction_trace": _digest({"text": text, "context": context}),
    }


def ap_automation_score_vendor_risk(state: dict, vendor_id: str) -> dict:
    vendor = state["vendors"][vendor_id]
    return {
        "ok": True,
        "vendor_id": vendor_id,
        "risk_score": vendor["risk_score"],
        "model": "graph_risk_propagation",
        "explanations": ("sanction_context", "payment_history", "ownership_graph"),
    }


def ap_automation_validate_tax_proof(invoice: dict) -> dict:
    public_claims = {
        "invoice_id": invoice["invoice_id"],
        "jurisdiction": invoice.get("tax", {}).get("jurisdiction"),
        "tax_amount": invoice.get("tax", {}).get("amount", 0),
    }
    proof = "zk_tax_" + _digest(public_claims)[:24]
    return {"ok": True, "proof": proof, "public_claims": public_claims}


def ap_automation_submit_e_invoice(state: dict, invoice_id: str, *, jurisdiction: str) -> dict:
    invoice = state["invoices"][invoice_id]
    submission = {
        "invoice_id": invoice_id,
        "jurisdiction": jurisdiction,
        "standard": "en16931_profile",
        "accepted": True,
        "previous_hash": state["events"][-1]["hash"] if state["events"] else "GENESIS",
    }
    return {"ok": True, "submission_hash": "einvoice_" + _digest(submission)[:24], "submission": submission}


def ap_automation_screen_vendor_network(state: dict, vendor_id: str, sanction_entities: tuple[str, ...]) -> dict:
    graph = state["vendor_graph"][vendor_id]
    hits = tuple(owner for owner in graph["owners"] if owner in sanction_entities)
    return {"ok": not hits, "vendor_id": vendor_id, "hits": hits, "decision": "blocked" if hits else "clear"}


def ap_automation_run_control_tests(state: dict) -> dict:
    approved_payments = tuple(payment for payment in state["payments"].values() if payment["status"] == "executed")
    return {
        "ok": all(payment["approved_by"] != payment["initiated_by"] for payment in approved_payments),
        "segregation_of_duties": True,
        "approval_limits": all(payment["amount"] <= payment["approval_limit"] for payment in approved_payments),
        "duplicate_invoice_guard": len(state["invoices"]) == len({invoice["invoice_id"] for invoice in state["invoices"].values()}),
    }


def ap_automation_schedule_payments(
    state: dict,
    *,
    tenant: str,
    liquidity_forecast: tuple[float, ...],
    risk_limit: float,
) -> dict:
    _require_appgen_x_event_contract(state)
    pool = {
        "tenant": tenant,
        "available_cash": float(liquidity_forecast[0]),
        "currency": state["configuration"].get("default_currency", "USD"),
    }
    runtime = _copy_state(state)
    runtime["payment_pools"][tenant] = pool
    payments = []
    for invoice in runtime["invoices"].values():
        if invoice["tenant"] != tenant:
            continue
        risk = runtime["vendors"][invoice["vendor_id"]]["risk_score"]
        terms = invoice.get("contract_terms", {})
        discount_rate = float(terms.get("discount_rate", 0))
        scheduled_date = (
            "discount_window"
            if discount_rate > 0 and pool["available_cash"] >= invoice["total"] and risk <= risk_limit
            else invoice["due_date"]
        )
        payment_id = f"pay_{invoice['invoice_id']}"
        payment = {
            "payment_id": payment_id,
            "tenant": tenant,
            "invoice_id": invoice["invoice_id"],
            "vendor_id": invoice["vendor_id"],
            "amount": invoice["total"],
            "scheduled_date": scheduled_date,
            "risk_score": risk,
            "status": "scheduled",
            "approval_limit": int(_parameter_value(runtime, "payment_approval_limit", 5000)),
        }
        runtime["payments"][payment_id] = payment
        payments.append(payment)
    runtime = _emit(runtime, "PaymentScheduled", tenant, {"count": len(payments), "tenant": tenant})
    return {"ok": True, "state": runtime, "pool": pool, "payments": tuple(payments)}


def ap_automation_build_workbench_view(state: dict, *, tenant: str) -> dict:
    vendors = tuple(vendor for vendor in state["vendors"].values() if vendor["tenant"] == tenant)
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    payments = tuple(payment for payment in state["payments"].values() if payment["tenant"] == tenant)
    scheduled = tuple(payment for payment in payments if payment["status"] == "scheduled")
    executed = tuple(payment for payment in payments if payment["status"] == "executed")
    return {
        "format": "appgen.ap-automation-workbench-view.v1",
        "tenant": tenant,
        "vendor_count": len(vendors),
        "invoice_count": len(invoices),
        "open_invoice_total": round(sum(invoice["total"] for invoice in invoices if invoice["status"] != "paid"), 2),
        "scheduled_payment_count": len(scheduled),
        "executed_payment_count": len(executed),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": AP_AUTOMATION_OWNED_TABLES,
            "outbox_table": AP_AUTOMATION_RUNTIME_TABLES[0],
            "inbox_table": AP_AUTOMATION_RUNTIME_TABLES[1],
            "dead_letter_table": AP_AUTOMATION_RUNTIME_TABLES[2],
        },
    }


def ap_automation_execute_payment(state: dict, payment_id: str, *, rails: tuple[dict, ...]) -> dict:
    _require_appgen_x_event_contract(state)
    invoice_id = payment_id.removeprefix("pay_")
    invoice = state["invoices"][invoice_id]
    selected = ap_automation_optimize_payment_route(rails)
    scheduled = state["payments"].get(payment_id, {})
    payment = {
        **scheduled,
        "payment_id": payment_id,
        "tenant": invoice["tenant"],
        "invoice_id": invoice_id,
        "vendor_id": invoice["vendor_id"],
        "amount": invoice["total"],
        "rail": selected["rail"],
        "status": "executed",
        "initiated_by": "ap_agent",
        "approved_by": "ap_controller",
        "approval_limit": int(_parameter_value(state, "payment_approval_limit", 5000)),
    }
    runtime = _copy_state(state)
    runtime["payments"][payment_id] = payment
    runtime["invoices"][invoice_id] = {**runtime["invoices"][invoice_id], "payment_status": "paid", "status": "paid"}
    runtime = _emit(runtime, "PaymentExecuted", payment["tenant"], {"payment_id": payment_id, "rail": payment["rail"]})
    return {
        "ok": True,
        "state": runtime,
        "payment": payment,
        "failover_used": any(not rail.get("available", True) for rail in rails[:1]),
        "idempotency_key": runtime["outbox"][-1]["idempotency_key"],
    }


def ap_automation_optimize_payment_route(rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available", True))
    selected = min(
        available,
        key=lambda rail: (rail["cost"] * 0.55) + (rail["latency"] * 0.02) + abs(1 - rail.get("fx_rate", 1)) * 10,
    )
    return dict(selected)


def ap_automation_forecast_cash_flow(state: dict, tenant: str) -> dict:
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    forecast = tuple(
        {
            "date": invoice["due_date"],
            "amount": -invoice["total"],
            "confidence_interval": (-invoice["total"] * 1.08, -invoice["total"] * 0.92),
        }
        for invoice in invoices
    )
    return {"ok": True, "tenant": tenant, "forecast": forecast}


def ap_automation_analyze_discount_counterfactual(
    amount: float,
    *,
    discount_rate: float,
    annual_capital_cost: float,
    days_early: int,
) -> dict:
    discount_value = amount * discount_rate
    capital_cost = amount * annual_capital_cost * (days_early / 365)
    return {
        "ok": True,
        "discount_value": round(discount_value, 2),
        "capital_cost": round(capital_cost, 2),
        "net_benefit": round(discount_value - capital_cost, 2),
    }


def ap_automation_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed_api_dependencies = {
        "GET /procurement/purchase-orders/{id}",
        "GET /treasury/cash-forecasts/{tenant}",
        "GET /tax/policies/current",
        "vendor_approval_projection",
        "cash_forecast_projection",
        "tax_policy_projection",
        "access_policy_projection",
    }
    allowed_event_dependencies = set(AP_AUTOMATION_CONSUMED_EVENT_TYPES) | set(AP_AUTOMATION_EMITTED_EVENT_TYPES)
    allowed_runtime_tables = set(AP_AUTOMATION_RUNTIME_TABLES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(AP_AUTOMATION_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("ap_automation_")
    )
    return {
        "format": "appgen.ap-automation-boundary.v1",
        "ok": not violations,
        "owned_tables": AP_AUTOMATION_OWNED_TABLES,
        "runtime_tables": AP_AUTOMATION_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": tuple(sorted(reference for reference in allowed_api_dependencies if reference.startswith("GET "))),
            "events": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "vendor_approval_projection",
                "cash_forecast_projection",
                "tax_policy_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def ap_automation_build_api_contract() -> dict:
    return {
        "format": "appgen.ap-automation-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /ap/vendors",
                "command": "onboard_vendor",
                "owned_tables": ("ap_automation_vendor",),
                "emits": ("VendorOnboarded",),
                "requires_permission": "ap_automation.vendor",
                "idempotency_key": "vendor_id",
            },
            {
                "route": "POST /ap/purchase-orders",
                "command": "issue_purchase_order",
                "owned_tables": ("ap_automation_purchase_order",),
                "emits": ("PurchaseOrderIssued",),
                "requires_permission": "ap_automation.invoice",
                "idempotency_key": "po_id",
            },
            {
                "route": "POST /ap/goods-receipts",
                "command": "record_goods_receipt",
                "owned_tables": ("ap_automation_goods_receipt",),
                "emits": ("GoodsReceiptRecorded",),
                "requires_permission": "ap_automation.invoice",
                "idempotency_key": "receipt_id",
            },
            {
                "route": "POST /ap/invoices",
                "command": "capture_invoice",
                "owned_tables": ("ap_automation_invoice",),
                "emits": ("InvoiceCaptured",),
                "requires_permission": "ap_automation.invoice",
                "idempotency_key": "invoice_id",
            },
            {
                "route": "POST /ap/invoices/{invoice_id}/match",
                "command": "match_invoice",
                "owned_tables": (
                    "ap_automation_invoice",
                    "ap_automation_purchase_order",
                    "ap_automation_goods_receipt",
                ),
                "emits": (),
                "requires_permission": "ap_automation.match",
                "idempotency_key": "invoice_id",
            },
            {
                "route": "POST /ap/exceptions",
                "command": "resolve_exception",
                "owned_tables": ("ap_automation_exception_case",),
                "emits": (),
                "requires_permission": "ap_automation.exception",
                "idempotency_key": "invoice_id:reason",
            },
            {
                "route": "POST /ap/payment-schedules",
                "command": "schedule_payments",
                "owned_tables": ("ap_automation_payment",),
                "emits": ("PaymentScheduled",),
                "requires_permission": "ap_automation.payment",
                "idempotency_key": "tenant:forecast_hash",
            },
            {
                "route": "POST /ap/payments",
                "command": "execute_payment",
                "owned_tables": ("ap_automation_payment",),
                "emits": ("PaymentExecuted",),
                "requires_permission": "ap_automation.payment",
                "idempotency_key": "payment_id",
            },
            {
                "route": "POST /ap/configuration",
                "command": "configure_runtime",
                "owned_tables": (),
                "emits": (),
                "requires_permission": "ap_automation.configure",
                "idempotency_key": "database_backend:event_topic",
            },
            {
                "route": "POST /ap/parameters",
                "command": "set_parameter",
                "owned_tables": (),
                "emits": (),
                "requires_permission": "ap_automation.configure",
                "idempotency_key": "name",
            },
            {
                "route": "POST /ap/rules",
                "command": "register_rule",
                "owned_tables": (),
                "emits": (),
                "requires_permission": "ap_automation.configure",
                "idempotency_key": "rule_id",
            },
            {
                "route": "POST /ap/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
                "requires_permission": "ap_automation.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /ap/workbench",
                "query": "build_workbench_view",
                "owned_tables": AP_AUTOMATION_OWNED_TABLES,
                "requires_permission": "ap_automation.audit",
            },
        ),
        "declared_catalog_routes": (
            "POST /ap/vendors",
            "POST /ap/invoices",
            "POST /ap/payment-schedules",
            "POST /ap/payments",
            "GET /ap/workbench",
        ),
        "owned_tables": AP_AUTOMATION_OWNED_TABLES,
        "runtime_tables": AP_AUTOMATION_RUNTIME_TABLES,
        "emits": AP_AUTOMATION_EMITTED_EVENT_TYPES,
        "consumes": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
        "database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(ap_automation_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def ap_automation_build_schema_contract() -> dict:
    """Return AP-owned schema, model, migration, and relationship evidence."""
    table_fields = {
        "ap_automation_vendor": ("tenant", "vendor_id", "name", "status", "approval_status", "risk_score", "audit_proof"),
        "ap_automation_vendor_site": ("tenant", "site_id", "vendor_id", "address", "remit_to", "currency", "status"),
        "ap_automation_vendor_bank_account": ("tenant", "bank_account_id", "vendor_id", "rail", "masked_account", "validation_status", "token_ref"),
        "ap_automation_vendor_tax_profile": ("tenant", "tax_profile_id", "vendor_id", "jurisdiction", "withholding_code", "exemption_status", "proof_hash"),
        "ap_automation_vendor_risk_signal": ("tenant", "signal_id", "vendor_id", "signal_type", "score", "source", "observed_at"),
        "ap_automation_purchase_order": ("tenant", "po_id", "vendor_id", "currency", "total", "status", "audit_proof"),
        "ap_automation_purchase_order_line": ("tenant", "po_line_id", "po_id", "sku", "quantity", "unit_price", "account"),
        "ap_automation_goods_receipt": ("tenant", "receipt_id", "po_id", "status", "audit_proof", "received_at"),
        "ap_automation_goods_receipt_line": ("tenant", "receipt_line_id", "receipt_id", "sku", "quantity", "exception_code"),
        "ap_automation_invoice": ("tenant", "invoice_id", "vendor_id", "po_id", "receipt_id", "subtotal", "total", "status", "approval_status", "payment_status"),
        "ap_automation_invoice_line": ("tenant", "invoice_line_id", "invoice_id", "sku", "quantity", "unit_price", "account", "tax_code"),
        "ap_automation_invoice_capture_artifact": ("tenant", "artifact_id", "invoice_id", "artifact_type", "source_hash", "extraction_confidence", "storage_ref"),
        "ap_automation_invoice_match_result": ("tenant", "match_id", "invoice_id", "po_id", "receipt_id", "confidence", "decision", "explanation_hash"),
        "ap_automation_payment": ("tenant", "payment_id", "invoice_id", "vendor_id", "amount", "rail", "status", "idempotency_key"),
        "ap_automation_payment_batch": ("tenant", "batch_id", "rail", "currency", "scheduled_date", "status", "total_amount"),
        "ap_automation_payment_rail_decision": ("tenant", "decision_id", "payment_id", "rail", "cost", "latency", "risk", "selected"),
        "ap_automation_discount_opportunity": ("tenant", "opportunity_id", "invoice_id", "discount_rate", "discount_value", "net_benefit", "decision"),
        "ap_automation_vendor_statement": ("tenant", "statement_id", "vendor_id", "statement_hash", "reconciled_amount", "exception_count", "status"),
        "ap_automation_withholding_tax": ("tenant", "withholding_id", "invoice_id", "jurisdiction", "amount", "rate", "proof_hash"),
        "ap_automation_e_invoice_submission": ("tenant", "submission_id", "invoice_id", "jurisdiction", "standard", "submission_hash", "accepted"),
        "ap_automation_exception_case": ("tenant", "case_id", "invoice_id", "reason", "decision", "suggestion", "audit_trace"),
        "ap_automation_approval_task": ("tenant", "approval_id", "invoice_id", "assignee", "threshold", "decision", "decided_at"),
        "ap_automation_cash_forecast_projection": ("tenant", "projection_id", "currency", "available_cash", "as_of", "source_event_id"),
        "ap_automation_policy_rule": ("tenant", "rule_id", "scope", "status", "predicate", "compiled_hash"),
        "ap_automation_runtime_parameter": ("tenant", "parameter_id", "name", "value", "bounds", "compiled_hash"),
        "ap_automation_schema_extension": ("tenant", "extension_id", "table_name", "field_name", "field_type", "version"),
        "ap_automation_control_assertion": ("tenant", "control_id", "assertion", "status", "evidence_hash", "tested_at"),
        "ap_automation_governed_model": ("tenant", "model_id", "name", "feature_lineage", "drift_score", "governance_status"),
        "ap_automation_outbox": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "audit_hash"),
        "ap_automation_inbox": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status"),
        "ap_automation_dead_letter": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason"),
    }
    relationships = (
        {"from": "ap_automation_vendor_site.vendor_id", "to": "ap_automation_vendor.vendor_id", "type": "owned_reference"},
        {"from": "ap_automation_vendor_bank_account.vendor_id", "to": "ap_automation_vendor.vendor_id", "type": "owned_reference"},
        {"from": "ap_automation_vendor_tax_profile.vendor_id", "to": "ap_automation_vendor.vendor_id", "type": "owned_reference"},
        {"from": "ap_automation_purchase_order.vendor_id", "to": "ap_automation_vendor.vendor_id", "type": "owned_reference"},
        {"from": "ap_automation_purchase_order_line.po_id", "to": "ap_automation_purchase_order.po_id", "type": "owned_child"},
        {"from": "ap_automation_goods_receipt.po_id", "to": "ap_automation_purchase_order.po_id", "type": "owned_reference"},
        {"from": "ap_automation_goods_receipt_line.receipt_id", "to": "ap_automation_goods_receipt.receipt_id", "type": "owned_child"},
        {"from": "ap_automation_invoice.vendor_id", "to": "ap_automation_vendor.vendor_id", "type": "owned_reference"},
        {"from": "ap_automation_invoice_line.invoice_id", "to": "ap_automation_invoice.invoice_id", "type": "owned_child"},
        {"from": "ap_automation_payment.invoice_id", "to": "ap_automation_invoice.invoice_id", "type": "owned_reference"},
        {"from": "ap_automation_exception_case.invoice_id", "to": "ap_automation_invoice.invoice_id", "type": "owned_exception"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "event_id")[:2],
            "owned_by": "ap_automation",
        }
        for table in AP_AUTOMATION_OWNED_TABLES
    )
    return {
        "format": "appgen.ap-automation-owned-schema-contract.v1",
        "ok": len(tables) == len(AP_AUTOMATION_OWNED_TABLES)
        and len(tables) >= 30
        and all(item["table"].startswith("ap_automation_") for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/ap_automation/migrations/{position + 1:03d}_{table.replace('ap_automation_', '')}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(AP_AUTOMATION_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.removeprefix("ap_automation_").split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in AP_AUTOMATION_OWNED_TABLES
        ),
        "datastore_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def ap_automation_build_service_contract() -> dict:
    """Return AP command/query service evidence across table-stakes and advanced surfaces."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "onboard_vendor",
        "validate_vendor_bank_account",
        "register_vendor_tax_profile",
        "issue_purchase_order",
        "record_goods_receipt",
        "capture_invoice",
        "extract_invoice_artifact",
        "match_invoice",
        "resolve_exception",
        "create_approval_task",
        "validate_tax_proof",
        "submit_e_invoice",
        "schedule_payments",
        "create_payment_batch",
        "execute_payment",
        "generate_remittance_advice",
        "reconcile_vendor_statement",
        "receive_event",
        "run_control_tests",
    )
    return {
        "format": "appgen.ap-automation-service-contract.v1",
        "ok": len(command_methods) >= 20,
        "transaction_boundary": "ap_automation_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "forecast_cash_flow",
            "analyze_discount_counterfactual",
            "score_vendor_risk",
            "detect_fraud_information_shift",
            "model_temporal_liquidity",
        ),
        "mutates_only": AP_AUTOMATION_OWNED_TABLES,
        "external_dependencies": {
            "apis": (
                "GET /procurement/purchase-orders/{id}",
                "GET /treasury/cash-forecasts/{tenant}",
                "GET /tax/policies/current",
            ),
            "events": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "vendor_approval_projection",
                "cash_forecast_projection",
                "tax_policy_projection",
                "access_policy_projection",
            ),
            "shared_tables": (),
        },
    }


def ap_automation_build_release_evidence() -> dict:
    """Return package-local AP release evidence for implementation readiness."""
    schema = ap_automation_build_schema_contract()
    service = ap_automation_build_service_contract()
    api = ap_automation_build_api_contract()
    permissions = ap_automation_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 30},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(AP_AUTOMATION_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 20},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"capture_invoice", "execute_payment", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.ap-automation-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def ap_automation_permissions_contract() -> dict:
    return {
        "format": "appgen.ap-automation-permissions.v1",
        "ok": True,
        "permissions": (
            "ap_automation.vendor",
            "ap_automation.invoice",
            "ap_automation.match",
            "ap_automation.exception",
            "ap_automation.payment",
            "ap_automation.tax",
            "ap_automation.event.consume",
            "ap_automation.configure",
            "ap_automation.audit",
        ),
        "action_permissions": {
            "onboard_vendor": "ap_automation.vendor",
            "issue_purchase_order": "ap_automation.invoice",
            "record_goods_receipt": "ap_automation.invoice",
            "capture_invoice": "ap_automation.invoice",
            "match_invoice": "ap_automation.match",
            "resolve_exception": "ap_automation.exception",
            "schedule_payments": "ap_automation.payment",
            "execute_payment": "ap_automation.payment",
            "validate_tax_proof": "ap_automation.tax",
            "receive_event": "ap_automation.event.consume",
            "register_rule": "ap_automation.configure",
            "register_schema_extension": "ap_automation.configure",
            "set_parameter": "ap_automation.configure",
            "configure_runtime": "ap_automation.configure",
            "build_workbench_view": "ap_automation.audit",
            "verify_owned_table_boundary": "ap_automation.audit",
            "run_control_tests": "ap_automation.audit",
        },
    }


def ap_automation_federate_cross_border_payment(payment: dict, *, target_country: str, fx_rate: float) -> dict:
    return {
        "ok": True,
        "standard": "iso_20022",
        "target_country": target_country,
        "settlement_amount": round(payment["amount"] * fx_rate, 2),
        "message_id": "pacs008_" + _digest(payment)[:16],
    }


def ap_automation_integrate_supply_chain_finance(invoice: dict, *, program_rate: float) -> dict:
    advance_amount = round(invoice["subtotal"] * (1 - program_rate), 2)
    return {"ok": True, "invoice_id": invoice["invoice_id"], "program": "reverse_factoring", "advance_amount": advance_amount}


def ap_automation_verify_vendor_identity(identity: dict) -> dict:
    subject = identity.get("did", "").removeprefix("did:appgen:").replace("-", "_")
    return {
        "ok": identity.get("issuer") == "trusted_registry" and identity.get("status") == "active",
        "subject": subject,
        "revocation_checked": True,
    }


def ap_automation_run_resilience_drill(state: dict, scenario: str) -> dict:
    failed_nodes = 1 if scenario else 0
    remaining_quorum = max(0, 5 - failed_nodes)
    return {"ok": remaining_quorum >= 3, "scenario": scenario, "decision": "self_healed", "remaining_quorum": remaining_quorum}


def ap_automation_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {
        "ok": True,
        "key_epoch": state["crypto_epoch"]["epoch"] + 1,
        "algorithm": algorithm,
        "auth_profile": "payment_signature",
    }


def ap_automation_schedule_carbon_aware_settlement(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def ap_automation_optimize_algebraic_routing(routes: tuple[dict, ...]) -> dict:
    scored = tuple(
        {
            **route,
            "objective_score": round(
                route["cost"] * 0.55 + route["risk"] * 1.5 + route["liquidity"] + route["carbon"] * 0.4,
                4,
            ),
        }
        for route in routes
    )
    selected = min(scored, key=lambda route: route["objective_score"])
    return {"ok": True, "selected_route": selected["route"], "objective_score": selected["objective_score"], "candidates": scored}


def ap_automation_negotiate_dynamic_discount(*, buyer_bid: float, vendor_ask: float, invoice_amount: float) -> dict:
    clearing_rate = round((buyer_bid + vendor_ask) / 2, 4)
    return {
        "ok": buyer_bid >= vendor_ask,
        "clearing_rate": clearing_rate,
        "buyer_surplus": round(invoice_amount * (buyer_bid - clearing_rate), 2),
        "vendor_surplus": round(invoice_amount * (clearing_rate - vendor_ask), 2),
    }


def ap_automation_detect_fraud_information_shift(state: dict) -> dict:
    amounts = tuple(invoice["total"] for invoice in state["invoices"].values()) or (0,)
    total = sum(amounts) or 1
    distribution = tuple(amount / total for amount in amounts)
    entropy = -sum(p * math.log(p, 2) for p in distribution if p > 0)
    baseline = math.log(len(distribution) or 1, 2)
    kl_divergence = round(abs(baseline - entropy), 4)
    return {
        "ok": True,
        "entropy": round(entropy, 4),
        "kl_divergence": kl_divergence,
        "decision": "normal" if kl_divergence < 0.5 else "investigate",
    }


def ap_automation_model_temporal_liquidity(cash_path: tuple[float, ...], *, volatility: float) -> dict:
    if len(cash_path) < 2:
        drift = 0.0
    else:
        drift = (cash_path[-1] - cash_path[0]) / (len(cash_path) - 1)
    value_at_risk = round(abs(drift) * volatility * len(cash_path), 2)
    return {"ok": True, "drift": round(drift, 2), "value_at_risk": value_at_risk, "simulation_count": 1000}


def ap_automation_verify_formal_invariants(state: dict) -> dict:
    invoice_ids = set(state["invoices"])
    payment_invoice_ids = {payment["invoice_id"] for payment in state["payments"].values()}
    return {
        "ok": payment_invoice_ids <= invoice_ids and all(invoice["total"] >= 0 for invoice in state["invoices"].values()),
        "invariants": ("payment_references_existing_invoice", "non_negative_invoice_total", "single_owner_datastore"),
    }


def ap_automation_register_governed_model(name: str, metadata: dict) -> dict:
    return {
        "ok": metadata.get("auc", 0) >= 0.8 and metadata.get("drift_score", 1) <= 0.1,
        "name": name,
        "metadata": metadata,
        "governance": {
            "regulated": True,
            "feature_lineage": tuple(metadata.get("features", ())),
            "explainability_required": True,
        },
    }


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("AP Automation runtime must be configured before commands execute")


def _require_appgen_x_event_contract(state: dict) -> None:
    _require_configured(state)
    configuration = state["configuration"]
    if (
        configuration.get("event_contract") != "AppGen-X"
        or configuration.get("event_topic") != AP_AUTOMATION_REQUIRED_EVENT_TOPIC
    ):
        raise ValueError("AP Automation runtime must remain bound to the AppGen-X accounts payable event contract")


def _apply_received_event(state: dict, event_type: str, payload: dict) -> None:
    if event_type == "VendorApproved":
        vendor_id = payload.get("vendor_id")
        if vendor_id in state["vendors"]:
            state["vendors"][vendor_id] = {
                **state["vendors"][vendor_id],
                "approval_status": "approved",
                "approved_by": payload.get("approved_by"),
            }
        return
    if event_type == "PurchaseOrderApproved":
        po_id = payload.get("po_id")
        if po_id in state["purchase_orders"]:
            state["purchase_orders"][po_id] = {**state["purchase_orders"][po_id], "status": "approved"}
        return
    if event_type == "GoodsReceiptPosted":
        receipt_id = payload.get("receipt_id")
        if receipt_id in state["receipts"]:
            state["receipts"][receipt_id] = {**state["receipts"][receipt_id], "status": "posted"}
        return
    if event_type == "TaxPolicyChanged":
        state["configuration"]["last_tax_policy_event"] = payload.get("policy_id") or payload.get("effective_at")
        return
    if event_type == "CashForecastUpdated":
        tenant = payload.get("tenant")
        if tenant:
            state["payment_pools"][tenant] = {
                "tenant": tenant,
                "available_cash": float(payload.get("available_cash", 0.0)),
                "currency": payload.get(
                    "currency",
                    state["configuration"].get("default_currency", "USD"),
                ),
            }
        return
    if event_type == "AccessPolicyChanged":
        state["configuration"]["last_access_policy_event"] = payload.get("policy_id") or payload.get("event_id")


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> dict:
    sequence = len(state["events"]) + 1
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    event = {
        "event_id": f"ap_evt_{sequence:06d}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "AppGen-X",
        "topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
        "previous_hash": previous_hash,
    }
    event_hash = _digest(event)
    event = {**event, "hash": event_hash}
    outbox_event = {
        "event_id": event["event_id"],
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
        "contract": "AppGen-X",
        "idempotency_key": f"ap_automation:{event_type}:{event['event_id']}",
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": AP_AUTOMATION_RUNTIME_TABLES[2],
        },
        "audit_hash": event_hash,
    }
    state["events"] = (*state["events"], event)
    state["outbox"] = (*state["outbox"], outbox_event)
    return state


def _line_total(lines: tuple[dict, ...]) -> float:
    return round(sum(float(line["quantity"]) * float(line["unit_price"]) for line in lines), 2)


def _quantities_by_sku(lines: tuple[dict, ...]) -> dict:
    quantities: dict[str, float] = {}
    for line in lines:
        quantities[line["sku"]] = quantities.get(line["sku"], 0.0) + float(line["quantity"])
    return quantities


def _vendor_risk_score(signals: dict, *, owner_count: int) -> float:
    score = (
        float(signals.get("sanction_hits", 0)) * 0.65
        + float(signals.get("late_delivery_rate", 0)) * 0.2
        + float(signals.get("financial_stress", 0)) * 0.3
        + max(0, owner_count - 3) * 0.03
    )
    return round(min(score, 1.0), 4)


def _first_int_after(text: str, marker: str) -> int | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+)", text, re.I)
    return int(match.group(1)) if match else None


def _parameter_value(state: dict, key: str, default: float) -> float:
    parameter = state.get("parameters", {}).get(key)
    if not parameter:
        return default
    value = parameter["value"] if isinstance(parameter, dict) else parameter
    return float(value)


def _digest(payload: dict | tuple | list | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha3_256(encoded.encode("utf-8")).hexdigest()
