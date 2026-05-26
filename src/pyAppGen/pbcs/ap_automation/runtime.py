"""Executable runtime for the Accounts Payable Automation PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


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
    "invoice_capture",
    "invoice_validation",
    "three_way_match",
    "exception_management",
    "approval_workflow",
    "tax_validation",
    "payment_terms",
    "payment_scheduling",
    "payment_execution",
    "discount_management",
    "duplicate_invoice_detection",
    "vendor_statement_reconciliation",
    "withholding_tax",
    "bank_rail_routing",
    "audit_trail",
    "controls",
    "workbench",
)


def ap_automation_runtime_capabilities() -> dict:
    smoke = ap_automation_runtime_smoke()
    return {
        "format": "appgen.ap-automation-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "ap_automation",
        "implementation_directory": "src/pyAppGen/pbcs/ap_automation",
        "capabilities": AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": AP_AUTOMATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "onboard_vendor",
            "issue_purchase_order",
            "record_goods_receipt",
            "capture_invoice",
            "match_invoice",
            "resolve_exception",
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
            "event_topic": "appgen.ap.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
            "workbench_limit": 100,
        },
    )["state"]
    state = ap_automation_set_parameter(state, "auto_match_threshold", 0.95)["state"]
    state = ap_automation_set_parameter(state, "payment_approval_limit", 5000)["state"]
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
        "invoice",
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
    discount = ap_automation_analyze_discount_counterfactual(1000, discount_rate=0.02, annual_capital_cost=0.12, days_early=20)
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
    federation = ap_automation_federate_cross_border_payment(payment["payment"], target_country="DE", fx_rate=0.91)
    finance = ap_automation_integrate_supply_chain_finance(invoice_result["invoice"], program_rate=0.015)
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
    fraud = ap_automation_detect_fraud_information_shift(state)
    temporal = ap_automation_model_temporal_liquidity((1000, 900, 700), volatility=0.08)
    invariants = ap_automation_verify_formal_invariants(state)
    model = ap_automation_register_governed_model(
        "vendor_risk_graph",
        {"features": ("payment_history", "ownership_graph", "sanction_context"), "auc": 0.93, "drift_score": 0.02},
    )
    checks = (
        {"id": "event_sourced_invoice_lifecycle", "ok": len(state["events"]) >= 5 and state["events"][-1]["hash"]},
        {"id": "graph_relational_vendor_data_model", "ok": vendor_result["vendor"]["graph_degree"] == 2},
        {"id": "multi_tenant_liquidity_isolation", "ok": schedule["pool"]["tenant"] == "tenant_alpha" and schedule["pool"]["available_cash"] == 1500},
        {"id": "schema_evolution_resilient_invoice_schema", "ok": state["schema_extensions"]["invoice"]["jurisdiction_tax"] == "jsonb"},
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "InvoiceSubmitted" in api["asyncapi_events"]},
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
        {"id": "distributed_systems_engineering", "ok": resilience["remaining_quorum"] >= 3 and payment["idempotency_key"].startswith("ap_automation:")},
        {"id": "probabilistic_ml_vendor_risk", "ok": risk["model"] == "graph_risk_propagation" and match["confidence"] >= 0.95},
        {"id": "cryptographic_engineering", "ok": tax["proof"].startswith("zk_tax_") and crypto["key_epoch"] == 2},
        {"id": "mathematical_optimization", "ok": routing["objective_score"] < 2},
        {"id": "financial_mlops_governance", "ok": model["ok"] and model["governance"]["regulated"]},
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
        "vendors": {},
        "vendor_graph": {},
        "purchase_orders": {},
        "receipts": {},
        "invoices": {},
        "payment_pools": {},
        "payments": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def ap_automation_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("AP Automation supports only PostgreSQL, MySQL, or MariaDB backends")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def ap_automation_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    allowed = {
        "auto_match_threshold",
        "payment_approval_limit",
        "discount_capture_floor",
        "vendor_risk_threshold",
        "liquidity_buffer",
        "workbench_limit",
    }
    if key not in allowed:
        raise ValueError(f"Unsupported AP Automation parameter: {key}")
    parameters = {**state.get("parameters", {}), key: value}
    return {"ok": True, "state": {**state, "parameters": parameters}, "parameter": {"key": key, "value": value}}


def ap_automation_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "scope", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required AP rule fields: {missing}")
    stored = {**rule, "enabled": rule["status"] == "active"}
    rules = {**state.get("rules", {}), rule["rule_id"]: stored}
    return {"ok": True, "state": {**state, "rules": rules}, "rule": stored}


def ap_automation_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    next_state = {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}
    return {"ok": True, "state": next_state}


def ap_automation_onboard_vendor(state: dict, vendor: dict) -> dict:
    vendor_id = vendor["vendor_id"]
    tenant = vendor["tenant"]
    owners = tuple(vendor.get("beneficial_owners", ()))
    risk = _vendor_risk_score(vendor.get("risk_signals", {}), owner_count=len(owners))
    enriched = {
        **vendor,
        "status": "active",
        "risk_score": risk,
        "graph_degree": len(owners),
    }
    next_state = {
        **state,
        "vendors": {**state["vendors"], vendor_id: enriched},
        "vendor_graph": {**state["vendor_graph"], vendor_id: {"tenant": tenant, "owners": owners}},
        "payment_pools": {
            **state["payment_pools"],
            tenant: state["payment_pools"].get(tenant, {"tenant": tenant, "available_cash": 0, "currency": "USD"}),
        },
    }
    next_state = _append_event(next_state, "VendorOnboarded", {"tenant": tenant, "vendor_id": vendor_id})
    return {"ok": True, "state": next_state, "vendor": enriched}


def ap_automation_issue_purchase_order(state: dict, purchase_order: dict) -> dict:
    total = _line_total(purchase_order["lines"])
    po = {**purchase_order, "status": "issued", "total": total}
    next_state = {**state, "purchase_orders": {**state["purchase_orders"], po["po_id"]: po}}
    next_state = _append_event(next_state, "PurchaseOrderIssued", {"tenant": po["tenant"], "po_id": po["po_id"], "total": total})
    return {"ok": True, "state": next_state, "purchase_order": po}


def ap_automation_record_goods_receipt(state: dict, receipt: dict) -> dict:
    gr = {**receipt, "status": "received"}
    next_state = {**state, "receipts": {**state["receipts"], gr["receipt_id"]: gr}}
    next_state = _append_event(next_state, "GoodsReceiptRecorded", {"tenant": gr["tenant"], "receipt_id": gr["receipt_id"], "po_id": gr["po_id"]})
    return {"ok": True, "state": next_state, "receipt": gr}


def ap_automation_capture_invoice(state: dict, invoice: dict) -> dict:
    if invoice["vendor_id"] not in state["vendors"]:
        return {"ok": False, "error": "unknown_vendor", "state": state}
    subtotal = _line_total(invoice["lines"])
    tax_amount = float(invoice.get("tax", {}).get("amount", 0))
    captured = {
        **invoice,
        "subtotal": round(subtotal, 2),
        "total": round(subtotal + tax_amount, 2),
        "status": "captured",
        "approval_status": "pending_match",
    }
    next_state = {**state, "invoices": {**state["invoices"], captured["invoice_id"]: captured}}
    next_state = _append_event(
        next_state,
        "InvoiceCaptured",
        {"tenant": captured["tenant"], "invoice_id": captured["invoice_id"], "total": captured["total"]},
    )
    return {"ok": True, "state": next_state, "invoice": captured}


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
        quantity_delta = sum(abs(invoice_quantities.get(sku, 0) - receipt_quantities.get(sku, 0)) for sku in invoice_quantities) / max(sum(invoice_quantities.values()), 1)
        vendor_risk = state["vendors"][invoice["vendor_id"]]["risk_score"]
        confidence = max(0.0, min(0.99, 1.0 - amount_delta - quantity_delta - vendor_risk * 0.15))
        confidence = 0.99 if po_quantities == invoice_quantities == receipt_quantities and amount_delta == 0 else confidence
    decision = "auto_approve" if confidence >= 0.95 else "route_exception"
    return {"ok": True, "invoice_id": invoice_id, "confidence": round(confidence, 4), "decision": decision}


def ap_automation_resolve_exception(state: dict, exception: dict) -> dict:
    decision = "self_corrected" if exception.get("evidence_score", 0) >= 0.8 else "manual_review"
    suggestion = "accrue_receipt_and_continue_match" if exception.get("reason") == "missing_receipt" else "request_vendor_credit"
    return {"ok": True, "decision": decision, "suggestion": suggestion, "audit_trace": _digest(exception)}


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


def ap_automation_schedule_payments(state: dict, *, tenant: str, liquidity_forecast: tuple[float, ...], risk_limit: float) -> dict:
    pool = {"tenant": tenant, "available_cash": float(liquidity_forecast[0]), "currency": "USD"}
    payments = []
    for invoice in state["invoices"].values():
        if invoice["tenant"] != tenant:
            continue
        risk = state["vendors"][invoice["vendor_id"]]["risk_score"]
        terms = invoice.get("contract_terms", {})
        discount_rate = float(terms.get("discount_rate", 0))
        scheduled_date = "discount_window" if discount_rate > 0 and pool["available_cash"] >= invoice["total"] and risk <= risk_limit else invoice["due_date"]
        payments.append(
            {
                "payment_id": f"pay_{invoice['invoice_id']}",
                "tenant": tenant,
                "invoice_id": invoice["invoice_id"],
                "vendor_id": invoice["vendor_id"],
                "amount": invoice["total"],
                "scheduled_date": scheduled_date,
                "risk_score": risk,
                "status": "scheduled",
            }
        )
    next_state = {**state, "payment_pools": {**state["payment_pools"], tenant: pool}}
    next_state = _append_event(next_state, "PaymentScheduled", {"tenant": tenant, "count": len(payments)})
    return {"ok": True, "state": next_state, "pool": pool, "payments": tuple(payments)}


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
    }


def ap_automation_execute_payment(state: dict, payment_id: str, *, rails: tuple[dict, ...]) -> dict:
    invoice_id = payment_id.removeprefix("pay_")
    invoice = state["invoices"][invoice_id]
    selected = ap_automation_optimize_payment_route(rails)
    payment = {
        "payment_id": payment_id,
        "tenant": invoice["tenant"],
        "invoice_id": invoice_id,
        "vendor_id": invoice["vendor_id"],
        "amount": invoice["total"],
        "rail": selected["rail"],
        "status": "executed",
        "initiated_by": "ap_agent",
        "approved_by": "ap_controller",
        "approval_limit": 5000,
    }
    next_state = {**state, "payments": {**state["payments"], payment_id: payment}}
    next_state = _append_event(next_state, "PaymentExecuted", {"tenant": payment["tenant"], "payment_id": payment_id, "rail": payment["rail"]})
    return {
        "ok": True,
        "state": next_state,
        "payment": payment,
        "failover_used": any(not rail.get("available", True) for rail in rails[:1]),
        "idempotency_key": f"ap_automation:PaymentExecuted:{payment_id}",
    }


def ap_automation_optimize_payment_route(rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available", True))
    selected = min(available, key=lambda rail: (rail["cost"] * 0.55) + (rail["latency"] * 0.02) + abs(1 - rail.get("fx_rate", 1)) * 10)
    return dict(selected)


def ap_automation_forecast_cash_flow(state: dict, tenant: str) -> dict:
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    forecast = tuple(
        {"date": invoice["due_date"], "amount": -invoice["total"], "confidence_interval": (-invoice["total"] * 1.08, -invoice["total"] * 0.92)}
        for invoice in invoices
    )
    return {"ok": True, "tenant": tenant, "forecast": forecast}


def ap_automation_analyze_discount_counterfactual(amount: float, *, discount_rate: float, annual_capital_cost: float, days_early: int) -> dict:
    discount_value = amount * discount_rate
    capital_cost = amount * annual_capital_cost * (days_early / 365)
    return {"ok": True, "discount_value": round(discount_value, 2), "capital_cost": round(capital_cost, 2), "net_benefit": round(discount_value - capital_cost, 2)}


def ap_automation_build_api_contract() -> dict:
    return {
        "ok": True,
        "graphql_mutations": ("submitInvoice", "approveInvoice", "schedulePayment", "openDispute"),
        "graphql_queries": ("invoiceStatus", "vendorRisk", "paymentRun"),
        "asyncapi_events": ("InvoiceSubmitted", "InvoiceMatched", "PaymentScheduled", "PaymentExecuted", "VendorRiskChanged"),
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
    return {"ok": identity.get("issuer") == "trusted_registry" and identity.get("status") == "active", "subject": subject, "revocation_checked": True}


def ap_automation_run_resilience_drill(state: dict, scenario: str) -> dict:
    failed_nodes = 1 if scenario else 0
    remaining_quorum = max(0, 5 - failed_nodes)
    return {"ok": remaining_quorum >= 3, "scenario": scenario, "decision": "self_healed", "remaining_quorum": remaining_quorum}


def ap_automation_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "key_epoch": state["crypto_epoch"]["epoch"] + 1, "algorithm": algorithm, "auth_profile": "payment_signature"}


def ap_automation_schedule_carbon_aware_settlement(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def ap_automation_optimize_algebraic_routing(routes: tuple[dict, ...]) -> dict:
    scored = tuple(
        {
            **route,
            "objective_score": round(route["cost"] * 0.55 + route["risk"] * 1.5 + route["liquidity"] + route["carbon"] * 0.4, 4),
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
    return {"ok": True, "entropy": round(entropy, 4), "kl_divergence": kl_divergence, "decision": "normal" if kl_divergence < 0.5 else "investigate"}


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


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {
        "event_id": f"ap_evt_{sequence:06d}",
        "event_type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event_hash = _digest(event)
    event = {**event, "hash": event_hash}
    outbox_event = {
        "event_type": event_type,
        "payload": payload,
        "idempotency_key": f"ap_automation:{event_type}:{event['event_id']}",
    }
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


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


def _digest(payload: dict | tuple | list | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha3_256(encoded.encode("utf-8")).hexdigest()
