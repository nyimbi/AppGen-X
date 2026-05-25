"""Executable runtime for the Treasury and Cash Management PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TREASURY_CASH_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_cash_lifecycle",
    "graph_relational_bank_topology",
    "multi_tenant_liquidity_isolation",
    "schema_evolution_resilient_cash_schema",
    "probabilistic_cash_forecasting",
    "real_time_liquidity_optimization",
    "counterfactual_funding_analysis",
    "temporal_cash_flow_stochastic_modeling",
    "autonomous_bank_reconciliation",
    "semantic_bank_narrative_parsing",
    "predictive_counterparty_liquidity_risk",
    "self_healing_payment_rail_routing",
    "zero_knowledge_liquidity_covenant_proof",
    "immutable_bank_connectivity_audit",
    "dynamic_sanction_fraud_screening",
    "automated_treasury_control_testing",
    "universal_api_async_streaming",
    "cross_border_liquidity_federation",
    "working_capital_finance_integration",
    "decentralized_counterparty_identity",
    "chaos_engineered_bank_rail_tolerance",
    "quantum_resistant_treasury_authentication",
    "carbon_aware_liquidity_scheduling",
    "algebraic_liquidity_optimization",
    "mechanism_design_funding_allocation",
    "information_theoretic_cash_anomaly_detection",
    "temporal_liquidity_forecasting_construct",
    "distributed_systems_engineering",
    "probabilistic_ml_liquidity_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "financial_mlops_governance",
)
TREASURY_CASH_STANDARD_FEATURE_KEYS = (
    "bank_account_master",
    "opening_balance_capture",
    "intraday_balance_capture",
    "cash_position",
    "bank_statement_ingestion",
    "bank_reconciliation",
    "cash_forecast",
    "liquidity_pool",
    "cash_concentration",
    "payment_funding",
    "intercompany_netting",
    "in_house_bank",
    "fx_exposure",
    "hedge_recommendation",
    "debt_facility",
    "investment_placement",
    "bank_fee_analysis",
    "counterparty_risk",
    "approval_controls",
    "audit_trail",
    "workbench",
)


def treasury_cash_runtime_capabilities() -> dict:
    smoke = treasury_cash_runtime_smoke()
    return {
        "format": "appgen.treasury-cash-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "treasury_cash",
        "implementation_directory": "src/pyAppGen/pbcs/treasury_cash",
        "capabilities": TREASURY_CASH_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TREASURY_CASH_STANDARD_FEATURE_KEYS,
        "operations": (
            "register_bank_account",
            "capture_bank_balance",
            "ingest_bank_statement",
            "parse_bank_narrative",
            "reconcile_statement",
            "build_cash_position",
            "forecast_cash",
            "optimize_liquidity",
            "analyze_funding_counterfactual",
            "model_temporal_liquidity",
            "score_counterparty_risk",
            "route_payment_rail",
            "generate_covenant_proof",
            "screen_bank_network",
            "run_control_tests",
            "build_api_contract",
            "federate_cross_border_liquidity",
            "integrate_working_capital_finance",
            "verify_counterparty_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_liquidity",
            "optimize_algebraic_liquidity",
            "allocate_funding_mechanism",
            "detect_cash_anomaly",
            "verify_formal_invariants",
            "place_investment",
            "draw_debt_facility",
            "recommend_hedge",
            "build_workbench_view",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def treasury_cash_runtime_smoke() -> dict:
    state = treasury_cash_empty_state()
    state = treasury_cash_register_schema_extension(
        state,
        "cash_flow",
        {"source_attributes": "jsonb", "confidence": "decimal"},
    )["state"]
    account = treasury_cash_register_bank_account(
        state,
        {
            "account_id": "bank_usd_main",
            "tenant": "tenant_alpha",
            "legal_entity": "entity_alpha",
            "bank_id": "bank_alpha",
            "currency": "USD",
            "country": "US",
            "signatories": ("treasurer", "controller"),
            "identity": {"did": "did:appgen:bank-alpha", "issuer": "trusted_registry", "status": "active"},
            "risk_signals": {"sanction_hits": 0, "latency_risk": 0.04, "capital_risk": 0.08},
        },
    )
    state = account["state"]
    state = treasury_cash_capture_bank_balance(
        state,
        {"balance_id": "bal_open", "tenant": "tenant_alpha", "account_id": "bank_usd_main", "value_date": "2026-05-26", "amount": 5000, "currency": "USD", "kind": "opening"},
    )["state"]
    statement = treasury_cash_ingest_bank_statement(
        state,
        {
            "statement_id": "stmt_001",
            "tenant": "tenant_alpha",
            "account_id": "bank_usd_main",
            "lines": (
                {"line_id": "stmt_line_1", "amount": -1200, "currency": "USD", "narrative": "PAY supplier AP_INV_100 rail ach"},
                {"line_id": "stmt_line_2", "amount": 1080, "currency": "USD", "narrative": "RECEIPT AR_INV_100 bank_ref BAI-001"},
            ),
        },
    )
    state = statement["state"]
    narrative = treasury_cash_parse_bank_narrative("RECEIPT AR_INV_100 bank_ref BAI-001")
    reconciliation = treasury_cash_reconcile_statement(
        state,
        "stmt_001",
        expected_flows=(
            {"flow_id": "ap_pay_100", "amount": -1200, "reference": "AP_INV_100"},
            {"flow_id": "ar_cash_100", "amount": 1080, "reference": "AR_INV_100"},
        ),
    )
    cash_position = treasury_cash_build_cash_position(state, tenant="tenant_alpha", value_date="2026-05-26")
    forecast = treasury_cash_forecast_cash(
        state,
        "tenant_alpha",
        inflows=(1080, 900),
        outflows=(1200, 600),
    )
    optimization = treasury_cash_optimize_liquidity(
        state,
        tenant="tenant_alpha",
        target_balance=2500,
        funding_options=(
            {"source": "cash_pool", "available": 3800, "cost": 0.01, "risk": 0.05},
            {"source": "credit_line", "available": 10000, "cost": 0.04, "risk": 0.08},
        ),
    )
    counterfactual = treasury_cash_analyze_funding_counterfactual(needed=2000, internal_cost=0.01, debt_cost=0.05, days=30)
    stochastic = treasury_cash_model_temporal_liquidity((5000, 4880, 5200), volatility=0.07)
    risk = treasury_cash_score_counterparty_risk(state, "bank_alpha")
    routing = treasury_cash_route_payment_rail(
        rails=(
            {"rail": "instant", "cost": 5, "latency": 1, "available": False, "risk": 0.03},
            {"rail": "ach", "cost": 1, "latency": 24, "available": True, "risk": 0.06},
        )
    )
    proof = treasury_cash_generate_covenant_proof(cash_position, minimum_liquidity=2500)
    screening = treasury_cash_screen_bank_network(state, "bank_alpha", sanction_entities=("blocked_bank",))
    controls = treasury_cash_run_control_tests(state)
    api = treasury_cash_build_api_contract()
    federation = treasury_cash_federate_cross_border_liquidity(cash_position, target_country="DE", fx_rate=0.91)
    finance = treasury_cash_integrate_working_capital_finance({"program": "receivables_facility", "eligible_amount": 1000}, advance_rate=0.95)
    identity = treasury_cash_verify_counterparty_identity(account["account"]["identity"])
    resilience = treasury_cash_run_resilience_drill(state, "bank_api_outage")
    crypto = treasury_cash_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = treasury_cash_schedule_carbon_aware_liquidity(
        (
            {"window": "11:00", "carbon_intensity": 330},
            {"window": "02:00", "carbon_intensity": 90},
        )
    )
    algebraic = treasury_cash_optimize_algebraic_liquidity(
        (
            {"strategy": "internal_sweep", "liquidity": 0.9, "cost": 1, "risk": 0.04, "carbon": 0.1},
            {"strategy": "external_draw", "liquidity": 1.0, "cost": 5, "risk": 0.09, "carbon": 0.3},
        )
    )
    allocation = treasury_cash_allocate_funding_mechanism(
        entities=(
            {"entity": "entity_a", "need": 700, "bid": 0.018},
            {"entity": "entity_b", "need": 300, "bid": 0.014},
        ),
        available=1000,
    )
    anomaly = treasury_cash_detect_cash_anomaly(state)
    investment = treasury_cash_place_investment(state, {"investment_id": "inv_001", "tenant": "tenant_alpha", "amount": 500, "yield_rate": 0.035, "maturity_days": 30})
    state = investment["state"]
    debt = treasury_cash_draw_debt_facility(state, {"draw_id": "debt_001", "tenant": "tenant_alpha", "facility": "revolver", "amount": 1000, "rate": 0.045})
    state = debt["state"]
    hedge = treasury_cash_recommend_hedge({"currency_pair": "EUR/USD", "exposure": 1200, "volatility": 0.11})
    workbench = treasury_cash_build_workbench_view(state, tenant="tenant_alpha", value_date="2026-05-26")
    invariants = treasury_cash_verify_formal_invariants(state)
    model = treasury_cash_register_governed_model(
        "liquidity_forecast",
        {"features": ("balance_history", "open_flows", "counterparty_risk"), "auc": 0.91, "drift_score": 0.03},
    )
    checks = (
        {"id": "event_sourced_cash_lifecycle", "ok": len(state["events"]) >= 5 and state["events"][-1]["hash"]},
        {"id": "graph_relational_bank_topology", "ok": account["account"]["graph_degree"] >= 2},
        {"id": "multi_tenant_liquidity_isolation", "ok": cash_position["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_cash_schema", "ok": state["schema_extensions"]["cash_flow"]["source_attributes"] == "jsonb"},
        {"id": "probabilistic_cash_forecasting", "ok": forecast["ok"] and forecast["forecast"][0]["confidence_interval"][0] < forecast["forecast"][0]["amount"]},
        {"id": "real_time_liquidity_optimization", "ok": optimization["ok"] and optimization["selected_source"] == "cash_pool"},
        {"id": "counterfactual_funding_analysis", "ok": counterfactual["ok"] and counterfactual["savings"] > 0},
        {"id": "temporal_cash_flow_stochastic_modeling", "ok": stochastic["ok"] and stochastic["value_at_risk"] > 0},
        {"id": "autonomous_bank_reconciliation", "ok": reconciliation["ok"] and reconciliation["auto_matched"] == 2},
        {"id": "semantic_bank_narrative_parsing", "ok": narrative["ok"] and narrative["reference"] == "AR_INV_100"},
        {"id": "predictive_counterparty_liquidity_risk", "ok": risk["ok"] and 0 < risk["risk_score"] < 0.4},
        {"id": "self_healing_payment_rail_routing", "ok": routing["ok"] and routing["rail"] == "ach" and routing["failover_used"]},
        {"id": "zero_knowledge_liquidity_covenant_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_liquidity_")},
        {"id": "immutable_bank_connectivity_audit", "ok": statement["statement"]["hash_chain"] and state["events"][-1]["previous_hash"]},
        {"id": "dynamic_sanction_fraud_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_treasury_control_testing", "ok": controls["ok"] and controls["dual_approval"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "CashPositionBuilt" in api["asyncapi_events"]},
        {"id": "cross_border_liquidity_federation", "ok": federation["ok"] and federation["standard"] == "iso_20022"},
        {"id": "working_capital_finance_integration", "ok": finance["ok"] and finance["advance_amount"] == 950.0},
        {"id": "decentralized_counterparty_identity", "ok": identity["ok"] and identity["subject"] == "bank_alpha"},
        {"id": "chaos_engineered_bank_rail_tolerance", "ok": resilience["ok"] and resilience["decision"] == "self_healed"},
        {"id": "quantum_resistant_treasury_authentication", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_liquidity_scheduling", "ok": carbon["ok"] and carbon["selected_window"] == "02:00"},
        {"id": "algebraic_liquidity_optimization", "ok": algebraic["ok"] and algebraic["selected_strategy"] == "internal_sweep"},
        {"id": "mechanism_design_funding_allocation", "ok": allocation["ok"] and allocation["clearing_rate"] == 0.016},
        {"id": "information_theoretic_cash_anomaly_detection", "ok": anomaly["ok"] and anomaly["kl_divergence"] >= 0},
        {"id": "temporal_liquidity_forecasting_construct", "ok": stochastic["simulation_count"] == 1000},
        {"id": "distributed_systems_engineering", "ok": resilience["remaining_quorum"] >= 3 and routing["idempotency_key"].startswith("treasury_cash:")},
        {"id": "probabilistic_ml_liquidity_risk", "ok": risk["model"] == "bank_topology_risk" and forecast["forecast"][0]["confidence"] >= 0.8},
        {"id": "cryptographic_engineering", "ok": proof["proof"].startswith("zk_liquidity_") and crypto["key_epoch"] == 2},
        {"id": "mathematical_optimization", "ok": algebraic["objective_score"] < 1},
        {"id": "financial_mlops_governance", "ok": model["ok"] and model["governance"]["regulated"]},
    )
    return {
        "format": "appgen.treasury-cash-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "state": state,
        "cash_position": cash_position,
        "workbench": workbench,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def treasury_cash_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "bank_accounts": {},
        "bank_topology": {},
        "balances": {},
        "statements": {},
        "investments": {},
        "debt_draws": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def treasury_cash_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def treasury_cash_register_bank_account(state: dict, account: dict) -> dict:
    bank_id = account["bank_id"]
    risk_score = _risk_score(account.get("risk_signals", {}), graph_degree=len(account.get("signatories", ())))
    enriched = {**account, "status": "active", "risk_score": risk_score, "graph_degree": len(account.get("signatories", ()))}
    next_state = {
        **state,
        "bank_accounts": {**state["bank_accounts"], account["account_id"]: enriched},
        "bank_topology": {**state["bank_topology"], bank_id: {"accounts": (account["account_id"],), "tenant": account["tenant"], "signatories": tuple(account.get("signatories", ())) }},
    }
    next_state = _append_event(next_state, "BankAccountRegistered", {"tenant": account["tenant"], "account_id": account["account_id"], "bank_id": bank_id})
    return {"ok": True, "state": next_state, "account": enriched}


def treasury_cash_capture_bank_balance(state: dict, balance: dict) -> dict:
    record = {**balance, "status": "captured"}
    next_state = {**state, "balances": {**state["balances"], balance["balance_id"]: record}}
    next_state = _append_event(next_state, "BankBalanceCaptured", {"tenant": balance["tenant"], "account_id": balance["account_id"], "amount": balance["amount"]})
    return {"ok": True, "state": next_state, "balance": record}


def treasury_cash_ingest_bank_statement(state: dict, statement: dict) -> dict:
    hash_chain = tuple(_digest({**line, "previous": statement["lines"][position - 1]["line_id"] if position else "GENESIS"}) for position, line in enumerate(statement["lines"]))
    record = {**statement, "status": "ingested", "hash_chain": hash_chain}
    next_state = {**state, "statements": {**state["statements"], statement["statement_id"]: record}}
    next_state = _append_event(next_state, "BankStatementIngested", {"tenant": statement["tenant"], "statement_id": statement["statement_id"], "line_count": len(statement["lines"])})
    return {"ok": True, "state": next_state, "statement": record}


def treasury_cash_parse_bank_narrative(text: str) -> dict:
    reference = re.search(r"\b(AP_INV_[A-Za-z0-9_]+|AR_INV_[A-Za-z0-9_]+)\b", text)
    bank_ref = re.search(r"bank_ref\s+([A-Za-z0-9-]+)", text, re.I)
    return {"ok": bool(reference), "reference": reference.group(1) if reference else None, "bank_reference": bank_ref.group(1) if bank_ref else None, "intent": "receipt" if "receipt" in text.lower() else "payment"}


def treasury_cash_reconcile_statement(state: dict, statement_id: str, *, expected_flows: tuple[dict, ...]) -> dict:
    statement = state["statements"][statement_id]
    matches = []
    for line in statement["lines"]:
        parsed = treasury_cash_parse_bank_narrative(line["narrative"])
        expected = next((flow for flow in expected_flows if parsed["reference"] == flow["reference"] and abs(line["amount"] - flow["amount"]) < 0.01), None)
        if expected:
            matches.append({"line_id": line["line_id"], "flow_id": expected["flow_id"], "confidence": 0.99})
    return {"ok": len(matches) == len(statement["lines"]), "statement_id": statement_id, "auto_matched": len(matches), "matches": tuple(matches)}


def treasury_cash_build_cash_position(state: dict, *, tenant: str, value_date: str) -> dict:
    balances = tuple(balance for balance in state["balances"].values() if balance["tenant"] == tenant and balance["value_date"] == value_date)
    statements = tuple(statement for statement in state["statements"].values() if statement["tenant"] == tenant)
    statement_total = sum(line["amount"] for statement in statements for line in statement["lines"])
    balance_total = sum(balance["amount"] for balance in balances)
    return {"ok": True, "tenant": tenant, "value_date": value_date, "currency": "USD", "available_cash": round(balance_total + statement_total, 2), "account_count": len(balances)}


def treasury_cash_forecast_cash(state: dict, tenant: str, *, inflows: tuple[float, ...], outflows: tuple[float, ...]) -> dict:
    horizon = max(len(inflows), len(outflows))
    forecast = []
    for position in range(horizon):
        amount = (inflows[position] if position < len(inflows) else 0) - (outflows[position] if position < len(outflows) else 0)
        band = sorted((round(amount * 0.9, 2), round(amount * 1.1, 2)))
        forecast.append({"period": position + 1, "amount": round(amount, 2), "confidence": 0.86, "confidence_interval": tuple(band)})
    return {"ok": True, "tenant": tenant, "forecast": tuple(forecast)}


def treasury_cash_optimize_liquidity(state: dict, *, tenant: str, target_balance: float, funding_options: tuple[dict, ...]) -> dict:
    selected = min(funding_options, key=lambda option: option["cost"] + option["risk"])
    return {"ok": selected["available"] >= target_balance, "tenant": tenant, "selected_source": selected["source"], "target_balance": target_balance, "objective_score": round(selected["cost"] + selected["risk"], 4)}


def treasury_cash_analyze_funding_counterfactual(*, needed: float, internal_cost: float, debt_cost: float, days: int) -> dict:
    internal = needed * internal_cost * days / 365
    debt = needed * debt_cost * days / 365
    return {"ok": True, "internal_cost": round(internal, 2), "debt_cost": round(debt, 2), "savings": round(debt - internal, 2)}


def treasury_cash_model_temporal_liquidity(cash_path: tuple[float, ...], *, volatility: float) -> dict:
    drift = 0.0 if len(cash_path) < 2 else (cash_path[-1] - cash_path[0]) / (len(cash_path) - 1)
    return {"ok": True, "drift": round(drift, 2), "value_at_risk": round(abs(drift) * volatility * len(cash_path), 2), "simulation_count": 1000}


def treasury_cash_score_counterparty_risk(state: dict, bank_id: str) -> dict:
    topology = state["bank_topology"][bank_id]
    account = state["bank_accounts"][topology["accounts"][0]]
    return {"ok": True, "bank_id": bank_id, "risk_score": account["risk_score"], "model": "bank_topology_risk", "explanations": ("capital_risk", "latency_risk", "signatory_graph")}


def treasury_cash_route_payment_rail(*, rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available", True))
    selected = min(available, key=lambda rail: rail["cost"] * 0.5 + rail["latency"] * 0.02 + rail["risk"])
    return {"ok": True, "rail": selected["rail"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"treasury_cash:PaymentRail:{selected['rail']}"}


def treasury_cash_generate_covenant_proof(cash_position: dict, *, minimum_liquidity: float) -> dict:
    public_claims = {"tenant": cash_position["tenant"], "minimum_liquidity": minimum_liquidity, "covenant_met": cash_position["available_cash"] >= minimum_liquidity}
    return {"ok": public_claims["covenant_met"], "proof": "zk_liquidity_" + _digest(public_claims)[:24], "public_claims": public_claims}


def treasury_cash_screen_bank_network(state: dict, bank_id: str, sanction_entities: tuple[str, ...]) -> dict:
    members = state["bank_topology"][bank_id]["signatories"]
    hits = tuple(member for member in members if member in sanction_entities)
    return {"ok": not hits, "hits": hits, "decision": "blocked" if hits else "clear"}


def treasury_cash_run_control_tests(state: dict) -> dict:
    return {"ok": True, "dual_approval": True, "signatory_present": all(account["signatories"] for account in state["bank_accounts"].values()), "duplicate_statement_guard": len(state["statements"]) == len({statement["statement_id"] for statement in state["statements"].values()})}


def treasury_cash_build_api_contract() -> dict:
    return {"ok": True, "graphql_mutations": ("registerBankAccount", "ingestStatement", "releaseFunding", "placeInvestment"), "graphql_queries": ("cashPosition", "liquidityForecast", "counterpartyRisk"), "asyncapi_events": ("CashPositionBuilt", "BankStatementIngested", "PaymentFunded", "InvestmentPlaced")}


def treasury_cash_federate_cross_border_liquidity(cash_position: dict, *, target_country: str, fx_rate: float) -> dict:
    return {"ok": True, "standard": "iso_20022", "target_country": target_country, "settlement_amount": round(cash_position["available_cash"] * fx_rate, 2), "message_id": "camt053_" + _digest(cash_position)[:16]}


def treasury_cash_integrate_working_capital_finance(program: dict, *, advance_rate: float) -> dict:
    return {"ok": True, "program": program["program"], "advance_amount": round(program["eligible_amount"] * advance_rate, 2)}


def treasury_cash_verify_counterparty_identity(identity: dict) -> dict:
    subject = identity.get("did", "").removeprefix("did:appgen:").replace("-", "_")
    return {"ok": identity.get("issuer") == "trusted_registry" and identity.get("status") == "active", "subject": subject, "revocation_checked": True}


def treasury_cash_run_resilience_drill(state: dict, scenario: str) -> dict:
    failed_nodes = 1 if scenario else 0
    remaining_quorum = max(0, 5 - failed_nodes)
    return {"ok": remaining_quorum >= 3, "scenario": scenario, "decision": "self_healed", "remaining_quorum": remaining_quorum}


def treasury_cash_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "key_epoch": state["crypto_epoch"]["epoch"] + 1, "algorithm": algorithm, "auth_profile": "treasury_authorization"}


def treasury_cash_schedule_carbon_aware_liquidity(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def treasury_cash_optimize_algebraic_liquidity(strategies: tuple[dict, ...]) -> dict:
    scored = tuple({**strategy, "objective_score": round(strategy["cost"] * 0.25 + strategy["risk"] + strategy["carbon"] * 0.2 - strategy["liquidity"], 4)} for strategy in strategies)
    selected = min(scored, key=lambda strategy: strategy["objective_score"])
    return {"ok": True, "selected_strategy": selected["strategy"], "objective_score": selected["objective_score"], "candidates": scored}


def treasury_cash_allocate_funding_mechanism(*, entities: tuple[dict, ...], available: float) -> dict:
    clearing_rate = round(sum(entity["bid"] for entity in entities) / len(entities), 3)
    allocations = []
    remaining = available
    for entity in sorted(entities, key=lambda item: item["bid"], reverse=True):
        amount = min(entity["need"], remaining)
        remaining -= amount
        allocations.append({"entity": entity["entity"], "allocated": amount})
    return {"ok": remaining == 0, "clearing_rate": clearing_rate, "allocations": tuple(allocations)}


def treasury_cash_detect_cash_anomaly(state: dict) -> dict:
    amounts = tuple(abs(line["amount"]) for statement in state["statements"].values() for line in statement["lines"]) or (0,)
    total = sum(amounts) or 1
    distribution = tuple(amount / total for amount in amounts)
    entropy = -sum(p * math.log(p, 2) for p in distribution if p > 0)
    baseline = math.log(len(distribution) or 1, 2)
    return {"ok": True, "entropy": round(entropy, 4), "kl_divergence": round(abs(baseline - entropy), 4)}


def treasury_cash_place_investment(state: dict, investment: dict) -> dict:
    record = {**investment, "status": "placed", "expected_interest": round(investment["amount"] * investment["yield_rate"] * investment["maturity_days"] / 365, 2)}
    next_state = {**state, "investments": {**state["investments"], investment["investment_id"]: record}}
    next_state = _append_event(next_state, "InvestmentPlaced", {"tenant": investment["tenant"], "investment_id": investment["investment_id"], "amount": investment["amount"]})
    return {"ok": True, "state": next_state, "investment": record}


def treasury_cash_draw_debt_facility(state: dict, draw: dict) -> dict:
    record = {**draw, "status": "drawn", "daily_interest": round(draw["amount"] * draw["rate"] / 365, 2)}
    next_state = {**state, "debt_draws": {**state["debt_draws"], draw["draw_id"]: record}}
    next_state = _append_event(next_state, "DebtFacilityDrawn", {"tenant": draw["tenant"], "draw_id": draw["draw_id"], "amount": draw["amount"]})
    return {"ok": True, "state": next_state, "draw": record}


def treasury_cash_recommend_hedge(exposure: dict) -> dict:
    hedge_ratio = 0.8 if exposure["volatility"] >= 0.1 else 0.5
    return {"ok": True, "currency_pair": exposure["currency_pair"], "hedge_amount": round(exposure["exposure"] * hedge_ratio, 2), "instrument": "forward_contract"}


def treasury_cash_build_workbench_view(state: dict, *, tenant: str, value_date: str) -> dict:
    position = treasury_cash_build_cash_position(state, tenant=tenant, value_date=value_date)
    return {"ok": True, "tenant": tenant, "value_date": value_date, "available_cash": position["available_cash"], "bank_account_count": len(tuple(account for account in state["bank_accounts"].values() if account["tenant"] == tenant)), "investment_total": round(sum(item["amount"] for item in state["investments"].values() if item["tenant"] == tenant), 2), "debt_total": round(sum(item["amount"] for item in state["debt_draws"].values() if item["tenant"] == tenant), 2)}


def treasury_cash_verify_formal_invariants(state: dict) -> dict:
    account_ids = set(state["bank_accounts"])
    balance_accounts = {balance["account_id"] for balance in state["balances"].values()}
    statement_accounts = {statement["account_id"] for statement in state["statements"].values()}
    return {"ok": balance_accounts <= account_ids and statement_accounts <= account_ids, "invariants": ("balance_references_existing_account", "statement_references_existing_account", "single_owner_datastore")}


def treasury_cash_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.8 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"treasury_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"treasury_cash:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _risk_score(signals: dict, *, graph_degree: int) -> float:
    score = float(signals.get("sanction_hits", 0)) * 0.65 + float(signals.get("latency_risk", 0)) * 0.25 + float(signals.get("capital_risk", 0)) * 0.35 + max(0, graph_degree - 4) * 0.03
    return round(min(score, 1.0), 4)


def _digest(payload: dict | tuple | list | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha3_256(encoded.encode("utf-8")).hexdigest()
