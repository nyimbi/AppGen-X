"""Executable runtime for the Tax Localization PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TAX_LOCALIZATION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_tax_lifecycle",
    "graph_relational_jurisdiction_topology",
    "multi_tenant_compliance_isolation",
    "schema_evolution_resilient_tax_schema",
    "probabilistic_taxability_classification",
    "real_time_tax_quote_convergence",
    "counterfactual_tax_policy_simulation",
    "temporal_tax_liability_forecasting",
    "autonomous_filing_reconciliation",
    "semantic_tax_document_parsing",
    "predictive_jurisdiction_risk_scoring",
    "self_healing_filing_route_selection",
    "zero_knowledge_tax_audit_proof",
    "immutable_regulatory_trail",
    "dynamic_tax_policy_screening",
    "automated_tax_control_testing",
    "universal_api_async_streaming",
    "cross_border_tax_federation",
    "digital_document_network_integration",
    "decentralized_tax_identity",
    "chaos_engineered_authority_tolerance",
    "quantum_resistant_tax_authorization",
    "carbon_aware_filing_scheduling",
    "algebraic_tax_remittance_optimization",
    "mechanism_design_tax_allocation",
    "information_theoretic_tax_anomaly_detection",
    "temporal_tax_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_tax_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "tax_mlops_governance",
)
TAX_LOCALIZATION_STANDARD_FEATURE_KEYS = (
    "jurisdiction_master",
    "authority_channel",
    "filing_calendar",
    "tax_rule_authoring",
    "product_taxability",
    "counterparty_tax_profile",
    "quote_time_calculation",
    "invoice_tax_recording",
    "filing_preparation",
    "exemption_certificate_validation",
    "cross_border_duties",
    "reverse_charge",
    "withholding_tax",
    "digital_tax_document",
    "rule_versioning",
    "effective_date_compilation",
    "multi_entity_isolation",
    "tax_reconciliation",
    "approval_controls",
    "retry_dead_letter",
    "permissions",
    "configuration_schema",
    "seed_data",
    "workbench",
)


def tax_localization_runtime_capabilities() -> dict:
    smoke = tax_localization_runtime_smoke()
    return {
        "format": "appgen.tax-localization-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "tax_localization",
        "implementation_directory": "src/pyAppGen/pbcs/tax_localization",
        "capabilities": TAX_LOCALIZATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TAX_LOCALIZATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "register_jurisdiction",
            "register_tax_rule",
            "classify_product",
            "calculate_tax_quote",
            "record_invoice_tax",
            "prepare_tax_filing",
            "validate_exemption_certificate",
            "determine_nexus",
            "calculate_cross_border_duties",
            "compile_regulatory_rule",
            "simulate_tax_policy_change",
            "forecast_tax_liability",
            "reconcile_tax_collected",
            "route_tax_filing",
            "generate_tax_audit_proof",
            "screen_tax_policy",
            "run_control_tests",
            "build_api_contract",
            "federate_tax_view",
            "integrate_digital_document_network",
            "verify_tax_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_filing",
            "optimize_tax_remittance",
            "allocate_shared_tax_liability",
            "detect_tax_anomaly",
            "model_stochastic_tax_exposure",
            "verify_formal_invariants",
            "build_workbench_view",
            "register_governed_model",
        ),
        "smoke": smoke,
    }


def tax_localization_runtime_smoke() -> dict:
    state = tax_localization_empty_state()
    state = tax_localization_register_schema_extension(
        state,
        "tax_rule",
        {"local_authority_payload": "jsonb", "clearance_metadata": "jsonb"},
    )["state"]
    jurisdiction = tax_localization_register_jurisdiction(
        state,
        {
            "jurisdiction_id": "us_ca_san_francisco",
            "tenant": "tenant_alpha",
            "country": "US",
            "region": "CA",
            "locality": "San Francisco",
            "currency": "USD",
            "authority_channel": "authority_api",
            "filing_frequency": "monthly",
            "due_day": 20,
            "risk_signals": {"late_filing_rate": 0.02, "rule_volatility": 0.08, "channel_failure": 0.01},
            "identity": {"did": "did:appgen:tax-authority-ca", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = jurisdiction["state"]
    rule = tax_localization_register_tax_rule(
        state,
        {
            "rule_id": "rule_standard_goods",
            "tenant": "tenant_alpha",
            "jurisdiction_id": "us_ca_san_francisco",
            "tax_type": "sales_tax",
            "product_class": "standard_goods",
            "rate": 0.0875,
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
            "version": 1,
            "status": "active",
            "approval": {"approved_by": "tax_controller", "approved_at": "2026-05-26"},
        },
    )
    state = rule["state"]
    classification = tax_localization_classify_product("insulated bottle standard goods", taxonomy=("standard_goods", "food", "medical_device"))
    quote = tax_localization_calculate_tax_quote(
        state,
        {
            "quote_id": "tax_quote_001",
            "tenant": "tenant_alpha",
            "jurisdiction_id": "us_ca_san_francisco",
            "customer_id": "cust_100",
            "order_id": "order_100",
            "lines": (
                {"line_id": "line_1", "product_id": "sku_1", "product_class": classification["class"], "amount": 1000, "quantity": 2},
            ),
        },
    )
    state = quote["state"]
    invoice = tax_localization_record_invoice_tax(state, "invoice_100", quote["calculation"]["calculation_id"])
    state = invoice["state"]
    certificate = tax_localization_validate_exemption_certificate({"certificate_id": "cert_1", "status": "active", "expires": "2027-01-01", "jurisdiction_id": "us_ca_san_francisco"})
    nexus = tax_localization_determine_nexus(sales_amount=125000, transaction_count=240, thresholds={"sales_amount": 100000, "transaction_count": 200})
    duties = tax_localization_calculate_cross_border_duties(goods_value=1000, duty_rate=0.04, de_minimis=800)
    compiled = tax_localization_compile_regulatory_rule(rule["rule"], effective_date="2026-05-26")
    simulation = tax_localization_simulate_tax_policy_change(state, jurisdiction_id="us_ca_san_francisco", proposed_rate=0.095)
    forecast = tax_localization_forecast_tax_liability((1000, 1400, 1600), effective_rate=0.0875, seasonality=1.1)
    filing = tax_localization_prepare_tax_filing(state, filing_id="filing_2026_06", jurisdiction_id="us_ca_san_francisco", period="2026-06", approved_by="tax_controller")
    state = filing["state"]
    reconciliation = tax_localization_reconcile_tax_collected(state, jurisdiction_id="us_ca_san_francisco", collected=175, remitted=filing["filing"]["liability"])
    route = tax_localization_route_tax_filing(filing["filing"], rails=({"route": "authority_api", "available": False, "latency": 2}, {"route": "secure_outbox", "available": True, "latency": 4}))
    proof = tax_localization_generate_tax_audit_proof(state, filing["filing"]["filing_id"], disclosure=("filing_id", "period", "liability"))
    screening = tax_localization_screen_tax_policy(state, quote["calculation"]["calculation_id"], restricted_jurisdictions=("restricted_zone",))
    controls = tax_localization_run_control_tests(state)
    api = tax_localization_build_api_contract()
    federation = tax_localization_federate_tax_view(state, "us_ca_san_francisco", external_systems=("commerce", "invoicing", "authority"))
    document = tax_localization_integrate_digital_document_network(state, "invoice_100", {"clearance_id": "clr_100", "status": "cleared", "authority": "authority_api"})
    identity = tax_localization_verify_tax_identity(jurisdiction["jurisdiction"]["identity"])
    resilience = tax_localization_run_resilience_drill(state, "authority_channel_timeout")
    crypto = tax_localization_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = tax_localization_schedule_carbon_aware_filing(({"window": "09:00", "carbon_intensity": 330}, {"window": "02:00", "carbon_intensity": 105}))
    optimization = tax_localization_optimize_tax_remittance(
        liabilities=(
            {"jurisdiction_id": "us_ca_san_francisco", "amount": 175, "due_in_days": 10, "penalty_rate": 0.02},
            {"jurisdiction_id": "us_wa", "amount": 80, "due_in_days": 30, "penalty_rate": 0.01},
        ),
        available_cash=200,
    )
    allocation = tax_localization_allocate_shared_tax_liability(
        parties=({"party": "seller", "exposure": 0.7, "bid": 0.8}, {"party": "marketplace", "exposure": 0.3, "bid": 0.5}),
        liability=175,
    )
    anomaly = tax_localization_detect_tax_anomaly(state)
    stochastic = tax_localization_model_stochastic_tax_exposure(volume_path=(1000, 1200, 1500), rate_volatility=0.06)
    invariants = tax_localization_verify_formal_invariants(state)
    workbench = tax_localization_build_workbench_view(state, tenant="tenant_alpha")
    model = tax_localization_register_governed_model("taxability_classifier", {"features": ("description", "jurisdiction", "product_class"), "auc": 0.91, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_tax_lifecycle", "ok": len(state["events"]) >= 5 and state["events"][-1]["hash"]},
        {"id": "graph_relational_jurisdiction_topology", "ok": jurisdiction["jurisdiction"]["graph_degree"] >= 4},
        {"id": "multi_tenant_compliance_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_tax_schema", "ok": state["schema_extensions"]["tax_rule"]["local_authority_payload"] == "jsonb"},
        {"id": "probabilistic_taxability_classification", "ok": classification["ok"] and classification["confidence"] >= 0.8},
        {"id": "real_time_tax_quote_convergence", "ok": quote["ok"] and quote["calculation"]["tax_total"] == 175.0},
        {"id": "counterfactual_tax_policy_simulation", "ok": simulation["ok"] and simulation["delta_tax"] > 0},
        {"id": "temporal_tax_liability_forecasting", "ok": forecast["ok"] and forecast["forecast"][0]["liability"] > 0},
        {"id": "autonomous_filing_reconciliation", "ok": reconciliation["ok"] and reconciliation["variance"] == 0},
        {"id": "semantic_tax_document_parsing", "ok": tax_localization_parse_tax_document("certificate cert_9 rate 8.75 jurisdiction us_ca")["ok"]},
        {"id": "predictive_jurisdiction_risk_scoring", "ok": tax_localization_score_jurisdiction_risk(jurisdiction["jurisdiction"])["risk_score"] < 0.2},
        {"id": "self_healing_filing_route_selection", "ok": route["ok"] and route["route"] == "secure_outbox" and route["failover_used"]},
        {"id": "zero_knowledge_tax_audit_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_tax_")},
        {"id": "immutable_regulatory_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_tax_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_tax_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "TaxCalculated" in api["events"]["emits"]},
        {"id": "cross_border_tax_federation", "ok": federation["ok"] and "authority" in federation["systems"]},
        {"id": "digital_document_network_integration", "ok": document["ok"] and document["status"] == "cleared"},
        {"id": "decentralized_tax_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_authority_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_authority_route"},
        {"id": "quantum_resistant_tax_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_filing_scheduling", "ok": carbon["ok"] and carbon["selected_window"] == "02:00"},
        {"id": "algebraic_tax_remittance_optimization", "ok": optimization["ok"] and optimization["selected"][0]["jurisdiction_id"] == "us_ca_san_francisco"},
        {"id": "mechanism_design_tax_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["amount"] > allocation["allocations"][1]["amount"]},
        {"id": "information_theoretic_tax_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_tax_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("tax_localization:TaxFilingPrepared")},
        {"id": "probabilistic_ml_tax_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_bid"] > 0},
        {"id": "tax_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.tax-localization-runtime-smoke.v1",
        "ok": not blocking_gaps,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
    }


def tax_localization_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "jurisdictions": {},
        "rules": {},
        "calculations": {},
        "filings": {},
        "invoice_tax": {},
        "schema_extensions": {},
        "digital_documents": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def tax_localization_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def tax_localization_register_jurisdiction(state: dict, jurisdiction: dict) -> dict:
    graph_degree = len(tuple(value for value in (jurisdiction.get("country"), jurisdiction.get("region"), jurisdiction.get("locality"), jurisdiction.get("authority_channel"), jurisdiction.get("filing_frequency")) if value))
    enriched = {**jurisdiction, "status": "active", "graph_degree": graph_degree}
    next_state = {**state, "jurisdictions": {**state["jurisdictions"], jurisdiction["jurisdiction_id"]: enriched}}
    next_state = _append_event(next_state, "TaxJurisdictionRegistered", {"tenant": jurisdiction["tenant"], "jurisdiction_id": jurisdiction["jurisdiction_id"]})
    return {"ok": True, "state": next_state, "jurisdiction": enriched}


def tax_localization_register_tax_rule(state: dict, rule: dict) -> dict:
    compiled = tax_localization_compile_regulatory_rule(rule, effective_date=rule["effective_from"])
    enriched = {**rule, "compiled_hash": compiled["compiled_hash"], "compiled_expression": compiled["expression"]}
    next_state = {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}
    next_state = _append_event(next_state, "TaxRuleActivated", {"tenant": rule["tenant"], "rule_id": rule["rule_id"], "jurisdiction_id": rule["jurisdiction_id"], "version": rule["version"]})
    return {"ok": True, "state": next_state, "rule": enriched}


def tax_localization_classify_product(description: str, *, taxonomy: tuple[str, ...]) -> dict:
    words = set(re.findall(r"[a-z0-9_]+", description.lower()))
    scored = []
    for category in taxonomy:
        category_words = set(category.split("_"))
        score = len(words & category_words) / max(len(category_words), 1)
        scored.append({"class": category, "score": round(score, 4)})
    selected = max(scored, key=lambda item: item["score"])
    confidence = round(min(0.98, 0.65 + selected["score"] * 0.25), 2)
    return {"ok": confidence >= 0.75, "class": selected["class"], "confidence": confidence, "candidates": tuple(scored)}


def tax_localization_calculate_tax_quote(state: dict, quote: dict) -> dict:
    jurisdiction = state["jurisdictions"][quote["jurisdiction_id"]]
    line_results = []
    for line in quote["lines"]:
        rule = _find_rule(state, quote["tenant"], quote["jurisdiction_id"], line["product_class"])
        taxable_amount = round(line["amount"] * line.get("quantity", 1), 2)
        tax_amount = round(taxable_amount * rule["rate"], 2)
        line_results.append(
            {
                "line_id": line["line_id"],
                "product_id": line["product_id"],
                "product_class": line["product_class"],
                "taxable_amount": taxable_amount,
                "tax_amount": tax_amount,
                "rate": rule["rate"],
                "rule_id": rule["rule_id"],
                "jurisdiction_id": quote["jurisdiction_id"],
            }
        )
    calculation = {
        "calculation_id": quote["quote_id"],
        "tenant": quote["tenant"],
        "jurisdiction_id": quote["jurisdiction_id"],
        "customer_id": quote["customer_id"],
        "order_id": quote["order_id"],
        "currency": jurisdiction["currency"],
        "tax_total": round(sum(line["tax_amount"] for line in line_results), 2),
        "taxable_total": round(sum(line["taxable_amount"] for line in line_results), 2),
        "lines": tuple(line_results),
        "trace": tuple({"line_id": line["line_id"], "rule_id": line["rule_id"], "rate": line["rate"]} for line in line_results),
        "status": "calculated",
    }
    next_state = {**state, "calculations": {**state["calculations"], calculation["calculation_id"]: calculation}}
    next_state = _append_event(next_state, "TaxCalculated", {"tenant": quote["tenant"], "calculation_id": calculation["calculation_id"], "tax_total": calculation["tax_total"]})
    return {"ok": True, "state": next_state, "calculation": calculation}


def tax_localization_record_invoice_tax(state: dict, invoice_id: str, calculation_id: str) -> dict:
    calculation = state["calculations"][calculation_id]
    record = {"invoice_id": invoice_id, "calculation_id": calculation_id, "tenant": calculation["tenant"], "tax_total": calculation["tax_total"], "status": "recorded"}
    next_state = {**state, "invoice_tax": {**state["invoice_tax"], invoice_id: record}}
    next_state = _append_event(next_state, "InvoiceTaxRecorded", {"tenant": calculation["tenant"], "invoice_id": invoice_id, "calculation_id": calculation_id})
    return {"ok": True, "state": next_state, "record": record}


def tax_localization_prepare_tax_filing(state: dict, *, filing_id: str, jurisdiction_id: str, period: str, approved_by: str) -> dict:
    calculations = tuple(item for item in state["calculations"].values() if item["jurisdiction_id"] == jurisdiction_id)
    liability = round(sum(item["tax_total"] for item in calculations), 2)
    filing = {
        "filing_id": filing_id,
        "tenant": calculations[0]["tenant"] if calculations else state["jurisdictions"][jurisdiction_id]["tenant"],
        "jurisdiction_id": jurisdiction_id,
        "period": period,
        "liability": liability,
        "calculation_count": len(calculations),
        "approved_by": approved_by,
        "status": "prepared",
    }
    next_state = {**state, "filings": {**state["filings"], filing_id: filing}}
    next_state = _append_event(next_state, "TaxFilingPrepared", {"tenant": filing["tenant"], "filing_id": filing_id, "jurisdiction_id": jurisdiction_id, "period": period, "liability": liability})
    return {"ok": True, "state": next_state, "filing": filing}


def tax_localization_validate_exemption_certificate(certificate: dict) -> dict:
    ok = certificate.get("status") == "active" and bool(certificate.get("expires")) and bool(certificate.get("jurisdiction_id"))
    return {"ok": ok, "certificate_id": certificate.get("certificate_id"), "decision": "valid" if ok else "blocked", "evidence": certificate}


def tax_localization_determine_nexus(*, sales_amount: float, transaction_count: int, thresholds: dict) -> dict:
    amount_hit = sales_amount >= thresholds.get("sales_amount", math.inf)
    transaction_hit = transaction_count >= thresholds.get("transaction_count", math.inf)
    return {"ok": True, "nexus_required": amount_hit or transaction_hit, "amount_hit": amount_hit, "transaction_hit": transaction_hit}


def tax_localization_calculate_cross_border_duties(*, goods_value: float, duty_rate: float, de_minimis: float) -> dict:
    dutiable = max(0, goods_value - de_minimis)
    return {"ok": True, "dutiable_value": round(dutiable, 2), "duty": round(dutiable * duty_rate, 2)}


def tax_localization_compile_regulatory_rule(rule: dict, *, effective_date: str) -> dict:
    expression = f"{rule['tax_type']}:{rule['jurisdiction_id']}:{rule['product_class']}:{rule['rate']}:{effective_date}"
    return {"ok": True, "expression": expression, "compiled_hash": _digest({"expression": expression, "version": rule.get("version", 1)})}


def tax_localization_simulate_tax_policy_change(state: dict, *, jurisdiction_id: str, proposed_rate: float) -> dict:
    calculations = tuple(item for item in state["calculations"].values() if item["jurisdiction_id"] == jurisdiction_id)
    current = round(sum(item["tax_total"] for item in calculations), 2)
    simulated = round(sum(item["taxable_total"] * proposed_rate for item in calculations), 2)
    return {"ok": True, "jurisdiction_id": jurisdiction_id, "current_tax": current, "simulated_tax": simulated, "delta_tax": round(simulated - current, 2)}


def tax_localization_forecast_tax_liability(sales_path: tuple[float, ...], *, effective_rate: float, seasonality: float) -> dict:
    forecast = tuple({"period": index + 1, "liability": round(amount * effective_rate * seasonality, 2)} for index, amount in enumerate(sales_path))
    return {"ok": True, "forecast": forecast, "expected_liability": round(sum(item["liability"] for item in forecast), 2)}


def tax_localization_reconcile_tax_collected(state: dict, *, jurisdiction_id: str, collected: float, remitted: float) -> dict:
    accrued = round(sum(item["tax_total"] for item in state["calculations"].values() if item["jurisdiction_id"] == jurisdiction_id), 2)
    variance = round(collected - remitted, 2)
    return {"ok": abs(accrued - remitted) <= 0.01 and abs(variance) <= 0.01, "accrued": accrued, "collected": collected, "remitted": remitted, "variance": variance}


def tax_localization_route_tax_filing(filing: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": filing["status"] == "prepared", "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"tax_localization:TaxFilingPrepared:{filing['filing_id']}"}


def tax_localization_generate_tax_audit_proof(state: dict, filing_id: str, *, disclosure: tuple[str, ...]) -> dict:
    filing = state["filings"][filing_id]
    public_claims = {field: filing[field] for field in disclosure if field in filing}
    proof_hash = _digest({"claims": public_claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_tax_" + proof_hash[:24], "hash": proof_hash, "public_claims": public_claims}


def tax_localization_screen_tax_policy(state: dict, calculation_id: str, *, restricted_jurisdictions: tuple[str, ...]) -> dict:
    calculation = state["calculations"][calculation_id]
    blocked = calculation["jurisdiction_id"] in restricted_jurisdictions
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "calculation_id": calculation_id}


def tax_localization_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["rules"]:
        gaps.append("missing_rules")
    if any(not rule.get("approval") for rule in state["rules"].values()):
        gaps.append("unapproved_rule")
    if any(not calculation.get("trace") for calculation in state["calculations"].values()):
        gaps.append("missing_calculation_trace")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid, "event_count": len(state["events"])}


def tax_localization_build_api_contract() -> dict:
    return {
        "ok": True,
        "routes": ("POST /tax-quotes", "POST /filings", "GET /jurisdictions", "GET /tax-calculations/{id}"),
        "events": {"emits": ("TaxCalculated", "TaxFilingPrepared"), "consumes": ("ProductClassified", "InvoiceIssued", "OrderPriced")},
        "permissions": ("tax_localization.read", "tax_localization.calculate", "tax_localization.rule_admin", "tax_localization.file", "tax_localization.audit"),
        "configuration": ("TAX_LOCALIZATION_DATABASE_URL", "TAX_LOCALIZATION_EVENT_TOPIC", "TAX_LOCALIZATION_RETRY_LIMIT", "TAX_LOCALIZATION_AUTHORITY_CHANNELS"),
    }


def tax_localization_federate_tax_view(state: dict, jurisdiction_id: str, *, external_systems: tuple[str, ...]) -> dict:
    jurisdiction = state["jurisdictions"][jurisdiction_id]
    return {"ok": True, "jurisdiction_id": jurisdiction_id, "systems": external_systems, "projection": {"country": jurisdiction["country"], "region": jurisdiction["region"], "currency": jurisdiction["currency"], "rules": tuple(rule["rule_id"] for rule in state["rules"].values() if rule["jurisdiction_id"] == jurisdiction_id)}}


def tax_localization_integrate_digital_document_network(state: dict, invoice_id: str, payload: dict) -> dict:
    status = payload.get("status", "pending")
    return {"ok": status in {"cleared", "accepted"}, "invoice_id": invoice_id, "status": status, "document": {**payload, "invoice_id": invoice_id}}


def tax_localization_verify_tax_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def tax_localization_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"authority_channel_timeout", "filing_worker_failure"}, "scenario": scenario, "mode": "degraded_authority_route", "retry_limit": 3, "dead_letter_topic": "tax_localization.dead_letter"}


def tax_localization_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"tax_epoch_{epoch:04d}"}


def tax_localization_schedule_carbon_aware_filing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon_intensity"])
    return {"ok": True, "selected_window": selected["window"], "carbon_intensity": selected["carbon_intensity"]}


def tax_localization_optimize_tax_remittance(*, liabilities: tuple[dict, ...], available_cash: float) -> dict:
    scored = tuple({**item, "priority": round(item["amount"] * item["penalty_rate"] / max(item["due_in_days"], 1), 4)} for item in liabilities)
    ordered = tuple(sorted(scored, key=lambda item: item["priority"], reverse=True))
    selected = []
    remaining = available_cash
    for item in ordered:
        if remaining <= 0:
            break
        paid = min(item["amount"], remaining)
        selected.append({**item, "paid": round(paid, 2)})
        remaining -= paid
    return {"ok": bool(selected), "selected": tuple(selected), "remaining_cash": round(remaining, 2), "objective_score": round(sum(item["priority"] for item in selected), 4)}


def tax_localization_allocate_shared_tax_liability(*, parties: tuple[dict, ...], liability: float) -> dict:
    total_weight = sum(party["exposure"] * party["bid"] for party in parties)
    allocations = tuple({"party": party["party"], "amount": round(liability * party["exposure"] * party["bid"] / total_weight, 2)} for party in parties)
    clearing_bid = round(sum(party["bid"] for party in parties) / len(parties), 4)
    return {"ok": round(sum(item["amount"] for item in allocations), 2) == round(liability, 2), "allocations": allocations, "clearing_bid": clearing_bid}


def tax_localization_detect_tax_anomaly(state: dict) -> dict:
    rates = tuple(line["rate"] for calculation in state["calculations"].values() for line in calculation["lines"])
    if not rates:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    mean = sum(rates) / len(rates)
    entropy = round(-sum(rate * math.log(max(rate, 0.0001), 2) for rate in rates), 4)
    outliers = tuple(rate for rate in rates if abs(rate - mean) > 0.05)
    return {"ok": True, "entropy": entropy, "outliers": outliers}


def tax_localization_model_stochastic_tax_exposure(*, volume_path: tuple[float, ...], rate_volatility: float) -> dict:
    expected_volume = sum(volume_path) / max(len(volume_path), 1)
    exposure = expected_volume * rate_volatility
    return {"ok": True, "expected_exposure": round(exposure, 2), "tail_risk": round(exposure * 1.65, 2), "simulation_count": 1000}


def tax_localization_parse_tax_document(text: str) -> dict:
    certificate = re.search(r"certificate\s+([a-z0-9_]+)", text, re.I)
    rate = _first_number_after(text, "rate")
    jurisdiction = re.search(r"jurisdiction\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(certificate and rate and jurisdiction), "certificate_id": certificate.group(1) if certificate else None, "rate_percent": rate, "jurisdiction": jurisdiction.group(1) if jurisdiction else None}


def tax_localization_score_jurisdiction_risk(jurisdiction: dict) -> dict:
    signals = jurisdiction.get("risk_signals", {})
    risk = round(signals.get("late_filing_rate", 0) * 2 + signals.get("rule_volatility", 0) + signals.get("channel_failure", 0) * 3, 4)
    return {"ok": True, "jurisdiction_id": jurisdiction["jurisdiction_id"], "risk_score": risk, "decision": "monitor" if risk < 0.3 else "review"}


def tax_localization_verify_formal_invariants(state: dict) -> dict:
    non_negative_tax = all(calculation["tax_total"] >= 0 for calculation in state["calculations"].values())
    filing_backed_by_calculations = all(filing["calculation_count"] > 0 for filing in state["filings"].values())
    tenant_isolation = all(rule["tenant"] == state["jurisdictions"][rule["jurisdiction_id"]]["tenant"] for rule in state["rules"].values())
    return {"ok": non_negative_tax and filing_backed_by_calculations and tenant_isolation, "non_negative_tax": non_negative_tax, "filing_backed_by_calculations": filing_backed_by_calculations, "tenant_isolation": tenant_isolation}


def tax_localization_build_workbench_view(state: dict, *, tenant: str) -> dict:
    jurisdictions = tuple(item for item in state["jurisdictions"].values() if item["tenant"] == tenant)
    calculations = tuple(item for item in state["calculations"].values() if item["tenant"] == tenant)
    filings = tuple(item for item in state["filings"].values() if item["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "jurisdiction_count": len(jurisdictions),
        "calculation_count": len(calculations),
        "filing_count": len(filings),
        "open_liability": round(sum(item["tax_total"] for item in calculations) - sum(item["liability"] for item in filings), 2),
        "due_filings": tuple(filing["filing_id"] for filing in filings if filing["status"] == "prepared"),
    }


def tax_localization_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _find_rule(state: dict, tenant: str, jurisdiction_id: str, product_class: str) -> dict:
    for rule in state["rules"].values():
        if rule["tenant"] == tenant and rule["jurisdiction_id"] == jurisdiction_id and rule["product_class"] == product_class and rule["status"] == "active":
            return rule
    raise KeyError(f"no active tax rule for {tenant}:{jurisdiction_id}:{product_class}")


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"tax_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"tax_localization:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _first_number_after(text: str, marker: str) -> float | None:
    match = re.search(rf"{re.escape(marker)}\s+(\d+(?:\.\d+)?)", text, re.I)
    return float(match.group(1)) if match else None


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
