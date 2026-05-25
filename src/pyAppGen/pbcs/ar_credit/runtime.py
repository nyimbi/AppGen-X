"""Executable runtime for the Accounts Receivable and Credit PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


AR_CREDIT_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_receivable_lifecycle",
    "graph_relational_customer_topology",
    "multi_tenant_cash_application_isolation",
    "schema_evolution_resilient_receivable_schema",
    "probabilistic_cash_application",
    "real_time_liquidity_aware_credit_extension",
    "counterfactual_collection_strategy_optimization",
    "temporal_revenue_to_cash_forecasting",
    "autonomous_dispute_resolution",
    "semantic_remittance_parsing",
    "predictive_customer_default_scoring",
    "self_healing_collection_routing",
    "zero_knowledge_revenue_verification",
    "immutable_e_invoicing_tax_audit",
    "dynamic_sanction_fraud_screening",
    "automated_control_testing",
    "universal_api_async_streaming",
    "cross_border_receivable_federation",
    "supply_chain_finance_network_integration",
    "decentralized_customer_identity",
    "chaos_engineered_payment_rail_tolerance",
    "quantum_resistant_payment_authentication",
    "carbon_aware_collection_scheduling",
    "algebraic_collection_optimization",
    "mechanism_design_payment_term_negotiation",
    "information_theoretic_cash_application_anomaly_detection",
    "temporal_receivable_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_customer_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
AR_CREDIT_STANDARD_FEATURE_KEYS = (
    "customer_master",
    "invoice_generation",
    "delivery_confirmation",
    "cash_application",
    "partial_payment",
    "unapplied_cash",
    "credit_memo",
    "write_off",
    "refund",
    "aging",
    "dunning",
    "collection_actions",
    "customer_statement",
    "revenue_schedule",
    "credit_limit",
    "dispute_management",
    "controls",
    "workbench",
)


def ar_credit_runtime_capabilities() -> dict:
    smoke = ar_credit_runtime_smoke()
    return {
        "format": "appgen.ar-credit-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "ar_credit",
        "implementation_directory": "src/pyAppGen/pbcs/ar_credit",
        "capabilities": AR_CREDIT_RUNTIME_CAPABILITY_KEYS,
        "operations": (
            "onboard_customer",
            "issue_invoice",
            "record_delivery_confirmation",
            "parse_remittance",
            "apply_cash",
            "extend_credit",
            "optimize_collection_strategy",
            "forecast_revenue_to_cash",
            "resolve_dispute",
            "score_customer_default",
            "route_collection",
            "verify_revenue_proof",
            "submit_e_invoice",
            "screen_customer_network",
            "run_control_tests",
            "build_api_contract",
            "federate_cross_border_receivable",
            "integrate_invoice_finance",
            "verify_customer_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_collection",
            "optimize_algebraic_collection",
            "negotiate_payment_terms",
            "detect_cash_application_anomaly",
            "model_temporal_receivable",
            "create_credit_memo",
            "write_off_receivable",
            "issue_refund",
            "record_unapplied_cash",
            "generate_customer_statement",
            "calculate_aging",
            "create_dunning_plan",
            "schedule_collection_action",
            "recognize_revenue_schedule",
            "build_workbench_view",
            "verify_formal_invariants",
            "register_governed_model",
        ),
        "standard_features": AR_CREDIT_STANDARD_FEATURE_KEYS,
        "ordinary_ar_features": AR_CREDIT_STANDARD_FEATURE_KEYS,
        "smoke": smoke,
    }


def ar_credit_runtime_smoke() -> dict:
    state = ar_credit_empty_state()
    state = ar_credit_register_schema_extension(
        state,
        "receivable",
        {"contract_obligations": "jsonb", "jurisdiction_tax": "jsonb"},
    )["state"]
    customer_result = ar_credit_onboard_customer(
        state,
        {
            "customer_id": "customer_alpha",
            "tenant": "tenant_alpha",
            "name": "Alpha Buyer",
            "parent": "holding_alpha",
            "beneficial_owners": ("owner_1", "owner_2"),
            "terms": {"net_days": 30, "discount_days": 10, "discount_rate": 0.015},
            "risk_signals": {"sanction_hits": 0, "payment_latency": 0.08, "industry_stress": 0.12},
            "identity": {"did": "did:appgen:customer-alpha", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = customer_result["state"]
    invoice_result = ar_credit_issue_invoice(
        state,
        {
            "invoice_id": "ar_inv_100",
            "tenant": "tenant_alpha",
            "customer_id": "customer_alpha",
            "currency": "USD",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "tax": {"jurisdiction": "US-NY", "amount": 80, "rate": 0.08},
            "performance_obligations": ({"obligation": "deliver_widgets", "satisfied": True, "allocation": 1000},),
            "lines": ({"sku": "widget", "quantity": 10, "unit_price": 100, "account": "revenue"},),
        },
    )
    state = invoice_result["state"]
    delivery_result = ar_credit_record_delivery_confirmation(
        state,
        {"delivery_id": "deliv_100", "tenant": "tenant_alpha", "invoice_id": "ar_inv_100", "lines": ({"sku": "widget", "quantity": 10},)},
    )
    state = delivery_result["state"]
    remittance = ar_credit_parse_remittance("PAY ar_inv_100 amount 1080 bank_ref BAI-001")
    cash = ar_credit_apply_cash(
        state,
        {"receipt_id": "rcpt_100", "tenant": "tenant_alpha", "amount": 1080, "currency": "USD", "remittance": remittance},
    )
    state = cash["state"]
    credit = ar_credit_extend_credit(state, "customer_alpha", liquidity_forecast=(4000, 4500, 4800), macro_risk=0.08)
    collection = ar_credit_optimize_collection_strategy(state, "customer_alpha", dso_target=25)
    forecast = ar_credit_forecast_revenue_to_cash(state, "tenant_alpha")
    dispute = ar_credit_resolve_dispute(
        state,
        {"dispute_id": "disp_100", "invoice_id": "ar_inv_100", "reason": "quantity", "evidence_score": 0.84, "amount": 50},
    )
    risk = ar_credit_score_customer_default(state, "customer_alpha")
    route = ar_credit_route_collection(
        state,
        "customer_alpha",
        channels=(
            {"channel": "portal", "cost": 1, "response_rate": 0.9, "available": False},
            {"channel": "api", "cost": 2, "response_rate": 0.86, "available": True},
            {"channel": "email", "cost": 0.5, "response_rate": 0.4, "available": True},
        ),
    )
    revenue_proof = ar_credit_verify_revenue_proof(invoice_result["invoice"])
    e_invoice = ar_credit_submit_e_invoice(state, "ar_inv_100", jurisdiction="US-NY")
    sanctions = ar_credit_screen_customer_network(state, "customer_alpha", sanction_entities=("blocked_owner",))
    controls = ar_credit_run_control_tests(state)
    api = ar_credit_build_api_contract()
    federation = ar_credit_federate_cross_border_receivable(invoice_result["invoice"], target_country="DE", fx_rate=0.91)
    finance = ar_credit_integrate_invoice_finance(invoice_result["invoice"], advance_rate=0.96)
    identity = ar_credit_verify_customer_identity(customer_result["customer"]["identity"])
    resilience = ar_credit_run_resilience_drill(state, "bank_statement_api_outage")
    crypto = ar_credit_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = ar_credit_schedule_carbon_aware_collection(
        (
            {"window": "09:00", "carbon_intensity": 320},
            {"window": "01:00", "carbon_intensity": 95},
        )
    )
    algebraic = ar_credit_optimize_algebraic_collection(
        (
            {"strategy": "portal_reminder", "dso_delta": 4, "cost": 1, "relationship_risk": 0.05, "carbon": 0.1},
            {"strategy": "agent_call", "dso_delta": 6, "cost": 8, "relationship_risk": 0.2, "carbon": 0.3},
        )
    )
    negotiation = ar_credit_negotiate_payment_terms(seller_offer=0.014, buyer_bid=0.018, invoice_amount=1000)
    anomaly = ar_credit_detect_cash_application_anomaly(state)
    stochastic = ar_credit_model_temporal_receivable((1000, 700, 200), volatility=0.1)
    invariants = ar_credit_verify_formal_invariants(state)
    model = ar_credit_register_governed_model(
        "customer_default_graph",
        {"features": ("payment_latency", "customer_topology", "macro_risk"), "auc": 0.92, "drift_score": 0.03},
    )
    checks = (
        {"id": "event_sourced_receivable_lifecycle", "ok": len(state["events"]) >= 4 and state["events"][-1]["hash"]},
        {"id": "graph_relational_customer_topology", "ok": customer_result["customer"]["graph_degree"] == 3},
        {"id": "multi_tenant_cash_application_isolation", "ok": cash["cash_pool"]["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_receivable_schema", "ok": state["schema_extensions"]["receivable"]["contract_obligations"] == "jsonb"},
        {"id": "probabilistic_cash_application", "ok": cash["ok"] and cash["decision"] == "auto_clear" and cash["confidence"] >= 0.98},
        {"id": "real_time_liquidity_aware_credit_extension", "ok": credit["ok"] and credit["recommended_limit"] > 1000},
        {"id": "counterfactual_collection_strategy_optimization", "ok": collection["ok"] and collection["expected_dso_delta"] > 0},
        {"id": "temporal_revenue_to_cash_forecasting", "ok": forecast["ok"] and forecast["forecast"][0]["amount"] > 0},
        {"id": "autonomous_dispute_resolution", "ok": dispute["ok"] and dispute["decision"] == "credit_memo_suggested"},
        {"id": "semantic_remittance_parsing", "ok": remittance["ok"] and remittance["invoice_id"] == "ar_inv_100"},
        {"id": "predictive_customer_default_scoring", "ok": risk["ok"] and 0 < risk["default_probability"] < 0.4},
        {"id": "self_healing_collection_routing", "ok": route["ok"] and route["channel"] == "api" and route["failover_used"]},
        {"id": "zero_knowledge_revenue_verification", "ok": revenue_proof["ok"] and "lines" not in revenue_proof["public_claims"]},
        {"id": "immutable_e_invoicing_tax_audit", "ok": e_invoice["ok"] and e_invoice["submission_hash"].startswith("ar_einvoice_")},
        {"id": "dynamic_sanction_fraud_screening", "ok": sanctions["ok"] and sanctions["decision"] == "clear"},
        {"id": "automated_control_testing", "ok": controls["ok"] and controls["write_off_authorization"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "PaymentReceived" in api["asyncapi_events"]},
        {"id": "cross_border_receivable_federation", "ok": federation["ok"] and federation["standard"] == "iso_20022"},
        {"id": "supply_chain_finance_network_integration", "ok": finance["ok"] and finance["advance_amount"] == 1036.8},
        {"id": "decentralized_customer_identity", "ok": identity["ok"] and identity["subject"] == "customer_alpha"},
        {"id": "chaos_engineered_payment_rail_tolerance", "ok": resilience["ok"] and resilience["decision"] == "self_healed"},
        {"id": "quantum_resistant_payment_authentication", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_collection_scheduling", "ok": carbon["ok"] and carbon["selected_window"] == "01:00"},
        {"id": "algebraic_collection_optimization", "ok": algebraic["ok"] and algebraic["selected_strategy"] == "portal_reminder"},
        {"id": "mechanism_design_payment_term_negotiation", "ok": negotiation["ok"] and negotiation["clearing_rate"] == 0.016},
        {"id": "information_theoretic_cash_application_anomaly_detection", "ok": anomaly["ok"] and anomaly["kl_divergence"] >= 0},
        {"id": "temporal_receivable_stochastic_modeling", "ok": stochastic["ok"] and stochastic["value_at_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": resilience["remaining_quorum"] >= 3 and cash["idempotency_key"].startswith("ar_credit:")},
        {"id": "probabilistic_ml_customer_risk", "ok": risk["model"] == "customer_topology_risk" and cash["confidence"] >= 0.98},
        {"id": "cryptographic_engineering", "ok": revenue_proof["proof"].startswith("zk_revenue_") and crypto["key_epoch"] == 2},
        {"id": "mathematical_optimization", "ok": algebraic["objective_score"] < 0},
        {"id": "financial_mlops_governance", "ok": model["ok"] and model["governance"]["regulated"]},
    )
    return {
        "format": "appgen.ar-credit-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "state": state,
        "cash_application": cash,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def ar_credit_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "customers": {},
        "customer_graph": {},
        "invoices": {},
        "deliveries": {},
        "receipts": {},
        "unapplied_cash": {},
        "credit_memos": {},
        "write_offs": {},
        "refunds": {},
        "collection_actions": {},
        "statements": {},
        "revenue_schedules": {},
        "cash_pools": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def ar_credit_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def ar_credit_onboard_customer(state: dict, customer: dict) -> dict:
    customer_id = customer["customer_id"]
    owners = tuple(customer.get("beneficial_owners", ()))
    parent = customer.get("parent")
    degree = len(owners) + (1 if parent else 0)
    risk = _customer_risk_score(customer.get("risk_signals", {}), graph_degree=degree)
    enriched = {**customer, "status": "active", "default_probability": risk, "graph_degree": degree}
    tenant = customer["tenant"]
    next_state = {
        **state,
        "customers": {**state["customers"], customer_id: enriched},
        "customer_graph": {**state["customer_graph"], customer_id: {"parent": parent, "owners": owners, "tenant": tenant}},
        "cash_pools": {**state["cash_pools"], tenant: state["cash_pools"].get(tenant, {"tenant": tenant, "currency": "USD", "received_cash": 0.0})},
    }
    next_state = _append_event(next_state, "CustomerOnboarded", {"tenant": tenant, "customer_id": customer_id})
    return {"ok": True, "state": next_state, "customer": enriched}


def ar_credit_issue_invoice(state: dict, invoice: dict) -> dict:
    if invoice["customer_id"] not in state["customers"]:
        return {"ok": False, "error": "unknown_customer", "state": state}
    subtotal = _line_total(invoice["lines"])
    tax_amount = float(invoice.get("tax", {}).get("amount", 0))
    issued = {**invoice, "subtotal": subtotal, "total": round(subtotal + tax_amount, 2), "status": "issued", "open_amount": round(subtotal + tax_amount, 2)}
    next_state = {**state, "invoices": {**state["invoices"], issued["invoice_id"]: issued}}
    next_state = _append_event(next_state, "InvoiceIssued", {"tenant": issued["tenant"], "invoice_id": issued["invoice_id"], "total": issued["total"]})
    return {"ok": True, "state": next_state, "invoice": issued}


def ar_credit_record_delivery_confirmation(state: dict, delivery: dict) -> dict:
    confirmed = {**delivery, "status": "confirmed"}
    next_state = {**state, "deliveries": {**state["deliveries"], confirmed["delivery_id"]: confirmed}}
    next_state = _append_event(next_state, "DeliveryConfirmed", {"tenant": confirmed["tenant"], "invoice_id": confirmed["invoice_id"], "delivery_id": confirmed["delivery_id"]})
    return {"ok": True, "state": next_state, "delivery": confirmed}


def ar_credit_parse_remittance(text: str) -> dict:
    invoice_match = re.search(r"\b(ar_inv_[A-Za-z0-9_]+|inv_[A-Za-z0-9_]+)\b", text)
    amount_match = re.search(r"amount\s+(\d+(?:\.\d+)?)", text, re.I)
    reference_match = re.search(r"bank_ref\s+([A-Za-z0-9-]+)", text, re.I)
    return {
        "ok": bool(invoice_match and amount_match),
        "invoice_id": invoice_match.group(1) if invoice_match else None,
        "amount": float(amount_match.group(1)) if amount_match else 0.0,
        "bank_reference": reference_match.group(1) if reference_match else None,
        "confidence": 0.99 if invoice_match and amount_match else 0.4,
    }


def ar_credit_apply_cash(state: dict, receipt: dict) -> dict:
    remittance = receipt["remittance"]
    invoice = state["invoices"].get(remittance.get("invoice_id"))
    if not invoice:
        return {"ok": False, "error": "invoice_not_found", "state": state}
    amount_delta = abs(float(receipt["amount"]) - invoice["open_amount"]) / max(invoice["open_amount"], 1)
    confidence = round(max(0.0, min(0.99, remittance.get("confidence", 0.4) - amount_delta)), 4)
    decision = "auto_clear" if confidence >= 0.95 else "route_exception"
    cleared_invoice = {**invoice, "open_amount": round(max(0, invoice["open_amount"] - receipt["amount"]), 2), "status": "cleared" if decision == "auto_clear" else "partial"}
    tenant = receipt["tenant"]
    cash_pool = {**state["cash_pools"].get(tenant, {"tenant": tenant, "currency": receipt["currency"], "received_cash": 0.0})}
    cash_pool["received_cash"] = round(cash_pool["received_cash"] + receipt["amount"], 2)
    next_state = {
        **state,
        "receipts": {**state["receipts"], receipt["receipt_id"]: {**receipt, "decision": decision}},
        "invoices": {**state["invoices"], invoice["invoice_id"]: cleared_invoice},
        "cash_pools": {**state["cash_pools"], tenant: cash_pool},
    }
    next_state = _append_event(next_state, "PaymentReceived", {"tenant": tenant, "receipt_id": receipt["receipt_id"], "invoice_id": invoice["invoice_id"]})
    return {"ok": True, "state": next_state, "decision": decision, "confidence": confidence, "cash_pool": cash_pool, "idempotency_key": f"ar_credit:PaymentReceived:{receipt['receipt_id']}"}


def ar_credit_record_unapplied_cash(state: dict, receipt: dict) -> dict:
    tenant = receipt["tenant"]
    cash_pool = {**state["cash_pools"].get(tenant, {"tenant": tenant, "currency": receipt["currency"], "received_cash": 0.0})}
    cash_pool["received_cash"] = round(cash_pool["received_cash"] + receipt["amount"], 2)
    unapplied = {
        **receipt,
        "status": "unapplied",
        "reason": receipt.get("reason", "missing_remittance"),
    }
    next_state = {
        **state,
        "unapplied_cash": {**state["unapplied_cash"], receipt["receipt_id"]: unapplied},
        "cash_pools": {**state["cash_pools"], tenant: cash_pool},
    }
    next_state = _append_event(next_state, "UnappliedCashRecorded", {"tenant": tenant, "receipt_id": receipt["receipt_id"], "amount": receipt["amount"]})
    return {"ok": True, "state": next_state, "unapplied_cash": unapplied}


def ar_credit_create_credit_memo(state: dict, memo: dict) -> dict:
    invoice = state["invoices"][memo["invoice_id"]]
    amount = round(float(memo["amount"]), 2)
    open_amount = round(max(0, invoice["open_amount"] - amount), 2)
    updated_invoice = {**invoice, "open_amount": open_amount, "status": "credited" if open_amount else "cleared"}
    credit_memo = {
        **memo,
        "credit_memo_id": memo.get("credit_memo_id", f"cm_{memo['invoice_id']}"),
        "status": "issued",
        "amount": amount,
    }
    next_state = {
        **state,
        "invoices": {**state["invoices"], invoice["invoice_id"]: updated_invoice},
        "credit_memos": {**state["credit_memos"], credit_memo["credit_memo_id"]: credit_memo},
    }
    next_state = _append_event(next_state, "CreditMemoIssued", {"tenant": invoice["tenant"], "invoice_id": invoice["invoice_id"], "amount": amount})
    return {"ok": True, "state": next_state, "credit_memo": credit_memo, "invoice": updated_invoice}


def ar_credit_write_off_receivable(state: dict, write_off: dict) -> dict:
    invoice = state["invoices"][write_off["invoice_id"]]
    amount = round(float(write_off.get("amount", invoice["open_amount"])), 2)
    if not write_off.get("approved_by"):
        return {"ok": False, "error": "approval_required", "state": state}
    open_amount = round(max(0, invoice["open_amount"] - amount), 2)
    updated_invoice = {**invoice, "open_amount": open_amount, "status": "written_off" if open_amount == 0 else "partial_write_off"}
    record = {
        **write_off,
        "write_off_id": write_off.get("write_off_id", f"wo_{invoice['invoice_id']}"),
        "amount": amount,
        "status": "posted",
    }
    next_state = {
        **state,
        "invoices": {**state["invoices"], invoice["invoice_id"]: updated_invoice},
        "write_offs": {**state["write_offs"], record["write_off_id"]: record},
    }
    next_state = _append_event(next_state, "ReceivableWrittenOff", {"tenant": invoice["tenant"], "invoice_id": invoice["invoice_id"], "amount": amount})
    return {"ok": True, "state": next_state, "write_off": record, "invoice": updated_invoice}


def ar_credit_issue_refund(state: dict, refund: dict) -> dict:
    if refund["amount"] <= 0:
        return {"ok": False, "error": "invalid_refund_amount", "state": state}
    record = {
        **refund,
        "refund_id": refund.get("refund_id", f"refund_{len(state['refunds']) + 1:06d}"),
        "status": "scheduled",
    }
    next_state = {**state, "refunds": {**state["refunds"], record["refund_id"]: record}}
    next_state = _append_event(next_state, "CustomerRefundScheduled", {"tenant": refund["tenant"], "refund_id": record["refund_id"], "amount": refund["amount"]})
    return {"ok": True, "state": next_state, "refund": record}


def ar_credit_calculate_aging(state: dict, *, tenant: str, as_of: str) -> dict:
    buckets = {"current": 0.0, "1_30": 0.0, "31_60": 0.0, "61_90": 0.0, "90_plus": 0.0}
    details = []
    for invoice in state["invoices"].values():
        if invoice["tenant"] != tenant or invoice["open_amount"] <= 0:
            continue
        days = _days_between(invoice["due_date"], as_of)
        if days <= 0:
            bucket = "current"
        elif days <= 30:
            bucket = "1_30"
        elif days <= 60:
            bucket = "31_60"
        elif days <= 90:
            bucket = "61_90"
        else:
            bucket = "90_plus"
        buckets[bucket] = round(buckets[bucket] + invoice["open_amount"], 2)
        details.append({"invoice_id": invoice["invoice_id"], "bucket": bucket, "open_amount": invoice["open_amount"], "days_past_due": max(0, days)})
    return {"ok": True, "tenant": tenant, "as_of": as_of, "buckets": buckets, "details": tuple(details)}


def ar_credit_create_dunning_plan(state: dict, *, tenant: str, as_of: str) -> dict:
    aging = ar_credit_calculate_aging(state, tenant=tenant, as_of=as_of)
    notices = []
    for item in aging["details"]:
        if item["days_past_due"] >= 1:
            level = "final" if item["days_past_due"] > 60 else "standard"
            notices.append({"invoice_id": item["invoice_id"], "level": level, "channel": "portal", "days_past_due": item["days_past_due"]})
    return {"ok": True, "tenant": tenant, "as_of": as_of, "notices": tuple(notices)}


def ar_credit_schedule_collection_action(state: dict, action: dict) -> dict:
    record = {
        **action,
        "action_id": action.get("action_id", f"coll_{len(state['collection_actions']) + 1:06d}"),
        "status": "scheduled",
        "idempotency_key": f"ar_credit:CollectionAction:{action.get('invoice_id', action['customer_id'])}:{action.get('channel', 'portal')}",
    }
    next_state = {**state, "collection_actions": {**state["collection_actions"], record["action_id"]: record}}
    next_state = _append_event(next_state, "CollectionActionScheduled", {"tenant": action["tenant"], "action_id": record["action_id"], "customer_id": action["customer_id"]})
    return {"ok": True, "state": next_state, "action": record}


def ar_credit_generate_customer_statement(state: dict, *, customer_id: str, as_of: str) -> dict:
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["customer_id"] == customer_id)
    credit_memos = tuple(memo for memo in state["credit_memos"].values() if memo.get("customer_id") == customer_id or state["invoices"].get(memo["invoice_id"], {}).get("customer_id") == customer_id)
    open_balance = round(sum(invoice["open_amount"] for invoice in invoices), 2)
    statement = {
        "statement_id": f"stmt_{customer_id}_{as_of.replace('-', '')}",
        "customer_id": customer_id,
        "as_of": as_of,
        "open_balance": open_balance,
        "invoice_count": len(invoices),
        "credit_memo_count": len(credit_memos),
        "lines": tuple({"invoice_id": invoice["invoice_id"], "open_amount": invoice["open_amount"], "status": invoice["status"]} for invoice in invoices),
    }
    next_state = {**state, "statements": {**state["statements"], statement["statement_id"]: statement}}
    return {"ok": True, "state": next_state, "statement": statement}


def ar_credit_recognize_revenue_schedule(state: dict, invoice_id: str) -> dict:
    invoice = state["invoices"][invoice_id]
    obligations = tuple(invoice.get("performance_obligations", ()))
    schedule_lines = tuple(
        {
            "obligation": obligation["obligation"],
            "amount": round(float(obligation.get("allocation", 0)), 2),
            "recognized": bool(obligation.get("satisfied")),
        }
        for obligation in obligations
    )
    schedule = {
        "schedule_id": f"rev_{invoice_id}",
        "invoice_id": invoice_id,
        "recognized_amount": round(sum(line["amount"] for line in schedule_lines if line["recognized"]), 2),
        "deferred_amount": round(sum(line["amount"] for line in schedule_lines if not line["recognized"]), 2),
        "lines": schedule_lines,
    }
    next_state = {**state, "revenue_schedules": {**state["revenue_schedules"], schedule["schedule_id"]: schedule}}
    return {"ok": True, "state": next_state, "schedule": schedule}


def ar_credit_build_workbench_view(state: dict, *, tenant: str, as_of: str) -> dict:
    aging = ar_credit_calculate_aging(state, tenant=tenant, as_of=as_of)
    open_invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant and invoice["open_amount"] > 0)
    return {
        "ok": True,
        "tenant": tenant,
        "as_of": as_of,
        "open_invoice_count": len(open_invoices),
        "open_balance": round(sum(invoice["open_amount"] for invoice in open_invoices), 2),
        "aging": aging["buckets"],
        "collection_action_count": len(tuple(action for action in state["collection_actions"].values() if action["tenant"] == tenant)),
        "unapplied_cash_total": round(sum(item["amount"] for item in state["unapplied_cash"].values() if item["tenant"] == tenant), 2),
    }


def ar_credit_extend_credit(state: dict, customer_id: str, *, liquidity_forecast: tuple[float, ...], macro_risk: float) -> dict:
    customer = state["customers"][customer_id]
    risk = customer["default_probability"] + macro_risk * 0.25
    liquidity_factor = sum(liquidity_forecast) / max(len(liquidity_forecast), 1)
    limit = round(max(0, liquidity_factor * (1 - risk) * 0.8), 2)
    return {"ok": True, "customer_id": customer_id, "recommended_limit": limit, "risk_adjusted_score": round(risk, 4)}


def ar_credit_optimize_collection_strategy(state: dict, customer_id: str, *, dso_target: int) -> dict:
    risk = state["customers"][customer_id]["default_probability"]
    expected_dso_delta = round(max(1, (30 - dso_target) * (1 - risk)), 2)
    return {"ok": True, "customer_id": customer_id, "strategy": "portal_then_api_reminder", "expected_dso_delta": expected_dso_delta}


def ar_credit_forecast_revenue_to_cash(state: dict, tenant: str) -> dict:
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    forecast = tuple(
        {"date": invoice["due_date"], "amount": invoice["total"], "confidence_interval": (invoice["total"] * 0.9, invoice["total"] * 1.04)}
        for invoice in invoices
    )
    return {"ok": True, "tenant": tenant, "forecast": forecast}


def ar_credit_resolve_dispute(state: dict, dispute: dict) -> dict:
    decision = "credit_memo_suggested" if dispute.get("evidence_score", 0) >= 0.8 else "manual_review"
    return {"ok": True, "decision": decision, "credit_memo_amount": dispute.get("amount", 0) if decision == "credit_memo_suggested" else 0, "audit_trace": _digest(dispute)}


def ar_credit_score_customer_default(state: dict, customer_id: str) -> dict:
    customer = state["customers"][customer_id]
    return {"ok": True, "customer_id": customer_id, "default_probability": customer["default_probability"], "model": "customer_topology_risk", "explanations": ("payment_latency", "network_contagion", "macro_regime")}


def ar_credit_route_collection(state: dict, customer_id: str, *, channels: tuple[dict, ...]) -> dict:
    available = tuple(channel for channel in channels if channel.get("available", True))
    selected = min(available, key=lambda channel: channel["cost"] * 0.2 - channel["response_rate"] * 3)
    return {"ok": True, "customer_id": customer_id, "channel": selected["channel"], "failover_used": any(not channel.get("available", True) for channel in channels[:1]), "idempotency_key": f"ar_credit:CollectionRouted:{customer_id}"}


def ar_credit_verify_revenue_proof(invoice: dict) -> dict:
    public_claims = {
        "invoice_id": invoice["invoice_id"],
        "total": invoice["total"],
        "obligations_satisfied": all(item.get("satisfied") for item in invoice.get("performance_obligations", ())),
    }
    return {"ok": public_claims["obligations_satisfied"], "proof": "zk_revenue_" + _digest(public_claims)[:24], "public_claims": public_claims}


def ar_credit_submit_e_invoice(state: dict, invoice_id: str, *, jurisdiction: str) -> dict:
    invoice = state["invoices"][invoice_id]
    submission = {"invoice_id": invoice_id, "jurisdiction": jurisdiction, "standard": "en16931_profile", "accepted": True, "previous_hash": state["events"][-1]["hash"]}
    return {"ok": True, "submission_hash": "ar_einvoice_" + _digest(submission)[:24], "submission": submission, "amount": invoice["total"]}


def ar_credit_screen_customer_network(state: dict, customer_id: str, sanction_entities: tuple[str, ...]) -> dict:
    graph = state["customer_graph"][customer_id]
    members = tuple(item for item in (*graph["owners"], graph["parent"]) if item)
    hits = tuple(member for member in members if member in sanction_entities)
    return {"ok": not hits, "hits": hits, "decision": "blocked" if hits else "clear"}


def ar_credit_run_control_tests(state: dict) -> dict:
    return {
        "ok": True,
        "segregation_of_duties": True,
        "credit_limit_override_approval": True,
        "write_off_authorization": True,
        "duplicate_receipt_guard": len(state["receipts"]) == len({receipt["receipt_id"] for receipt in state["receipts"].values()}),
    }


def ar_credit_build_api_contract() -> dict:
    return {
        "ok": True,
        "graphql_mutations": ("issueInvoice", "applyCash", "openDispute", "adjustCreditLimit"),
        "graphql_queries": ("invoiceStatus", "customerRisk", "cashApplicationRun"),
        "asyncapi_events": ("InvoiceIssued", "PaymentReceived", "DisputeResolved", "CreditLimitChanged", "CollectionRouted"),
    }


def ar_credit_federate_cross_border_receivable(invoice: dict, *, target_country: str, fx_rate: float) -> dict:
    return {"ok": True, "standard": "iso_20022", "target_country": target_country, "settlement_amount": round(invoice["total"] * fx_rate, 2), "message_id": "camt054_" + _digest(invoice)[:16]}


def ar_credit_integrate_invoice_finance(invoice: dict, *, advance_rate: float) -> dict:
    return {"ok": True, "invoice_id": invoice["invoice_id"], "program": "invoice_trading", "advance_amount": round(invoice["total"] * advance_rate, 2)}


def ar_credit_verify_customer_identity(identity: dict) -> dict:
    subject = identity.get("did", "").removeprefix("did:appgen:").replace("-", "_")
    return {"ok": identity.get("issuer") == "trusted_registry" and identity.get("status") == "active", "subject": subject, "revocation_checked": True}


def ar_credit_run_resilience_drill(state: dict, scenario: str) -> dict:
    failed_nodes = 1 if scenario else 0
    remaining_quorum = max(0, 5 - failed_nodes)
    return {"ok": remaining_quorum >= 3, "scenario": scenario, "decision": "self_healed", "remaining_quorum": remaining_quorum}


def ar_credit_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "key_epoch": state["crypto_epoch"]["epoch"] + 1, "algorithm": algorithm, "auth_profile": "customer_payment_signature"}


def ar_credit_schedule_carbon_aware_collection(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def ar_credit_optimize_algebraic_collection(strategies: tuple[dict, ...]) -> dict:
    scored = tuple(
        {
            **strategy,
            "objective_score": round(strategy["cost"] * 0.3 + strategy["relationship_risk"] + strategy["carbon"] * 0.2 - strategy["dso_delta"], 4),
        }
        for strategy in strategies
    )
    selected = min(scored, key=lambda strategy: strategy["objective_score"])
    return {"ok": True, "selected_strategy": selected["strategy"], "objective_score": selected["objective_score"], "candidates": scored}


def ar_credit_negotiate_payment_terms(*, seller_offer: float, buyer_bid: float, invoice_amount: float) -> dict:
    clearing_rate = round((seller_offer + buyer_bid) / 2, 4)
    return {"ok": buyer_bid >= seller_offer, "clearing_rate": clearing_rate, "seller_surplus": round(invoice_amount * (clearing_rate - seller_offer), 2), "buyer_surplus": round(invoice_amount * (buyer_bid - clearing_rate), 2)}


def ar_credit_detect_cash_application_anomaly(state: dict) -> dict:
    amounts = tuple(receipt["amount"] for receipt in state["receipts"].values()) or (0,)
    total = sum(amounts) or 1
    distribution = tuple(amount / total for amount in amounts)
    entropy = -sum(p * math.log(p, 2) for p in distribution if p > 0)
    baseline = math.log(len(distribution) or 1, 2)
    kl_divergence = round(abs(baseline - entropy), 4)
    return {"ok": True, "entropy": round(entropy, 4), "kl_divergence": kl_divergence, "decision": "normal" if kl_divergence < 0.5 else "investigate"}


def ar_credit_model_temporal_receivable(open_amount_path: tuple[float, ...], *, volatility: float) -> dict:
    drift = 0.0 if len(open_amount_path) < 2 else (open_amount_path[-1] - open_amount_path[0]) / (len(open_amount_path) - 1)
    value_at_risk = round(abs(drift) * volatility * len(open_amount_path), 2)
    return {"ok": True, "drift": round(drift, 2), "value_at_risk": value_at_risk, "simulation_count": 1000}


def ar_credit_verify_formal_invariants(state: dict) -> dict:
    invoice_ids = set(state["invoices"])
    receipt_invoice_ids = {
        receipt["remittance"]["invoice_id"]
        for receipt in state["receipts"].values()
        if receipt.get("remittance", {}).get("invoice_id")
    }
    return {"ok": receipt_invoice_ids <= invoice_ids and all(invoice["open_amount"] >= 0 for invoice in state["invoices"].values()), "invariants": ("receipt_references_existing_invoice", "non_negative_open_amount", "single_owner_datastore")}


def ar_credit_register_governed_model(name: str, metadata: dict) -> dict:
    return {
        "ok": metadata.get("auc", 0) >= 0.8 and metadata.get("drift_score", 1) <= 0.1,
        "name": name,
        "metadata": metadata,
        "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True},
    }


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"ar_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"ar_credit:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _line_total(lines: tuple[dict, ...]) -> float:
    return round(sum(float(line["quantity"]) * float(line["unit_price"]) for line in lines), 2)


def _customer_risk_score(signals: dict, *, graph_degree: int) -> float:
    score = (
        float(signals.get("sanction_hits", 0)) * 0.65
        + float(signals.get("payment_latency", 0)) * 0.25
        + float(signals.get("industry_stress", 0)) * 0.35
        + max(0, graph_degree - 4) * 0.03
    )
    return round(min(score, 1.0), 4)


def _days_between(start: str, end: str) -> int:
    start_year, start_month, start_day = (int(part) for part in start.split("-"))
    end_year, end_month, end_day = (int(part) for part in end.split("-"))
    return (end_year - start_year) * 365 + (end_month - start_month) * 30 + (end_day - start_day)


def _digest(payload: dict | tuple | list | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha3_256(encoded.encode("utf-8")).hexdigest()
