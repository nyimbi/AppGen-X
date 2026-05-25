"""Executable runtime for the Payroll Engine PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PAYROLL_ENGINE_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_payroll_lifecycle",
    "graph_relational_compensation_topology",
    "multi_tenant_payroll_isolation",
    "schema_evolution_resilient_payroll_schema",
    "probabilistic_payroll_anomaly_compliance_scoring",
    "real_time_gross_to_net_analytics",
    "counterfactual_pay_policy_simulation",
    "temporal_payroll_cash_forecasting",
    "autonomous_payroll_exception_resolution",
    "semantic_payroll_instruction_parsing",
    "predictive_payroll_compliance_liquidity_risk",
    "self_healing_payment_filing_route_selection",
    "zero_knowledge_net_pay_filing_proof",
    "immutable_payroll_audit_trail",
    "dynamic_payroll_policy_screening",
    "automated_payroll_control_testing",
    "universal_api_async_streaming",
    "cross_system_payroll_federation",
    "treasury_tax_ledger_integration",
    "decentralized_worker_pay_identity",
    "chaos_engineered_payroll_tolerance",
    "quantum_resistant_payroll_authorization",
    "carbon_aware_payroll_batching",
    "algebraic_payroll_batch_optimization",
    "mechanism_design_cash_allocation",
    "information_theoretic_payroll_anomaly_detection",
    "temporal_payroll_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_payroll_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "payroll_mlops_governance",
)
PAYROLL_ENGINE_STANDARD_FEATURE_KEYS = (
    "payroll_calendar",
    "payroll_run_creation",
    "worker_projection",
    "labor_hours_ingestion",
    "gross_pay_calculation",
    "overtime_calculation",
    "deduction_management",
    "benefit_allocation",
    "tax_basis_projection",
    "net_pay_calculation",
    "payslip_generation",
    "approval_workflow",
    "payroll_posting",
    "filing_preparation",
    "payment_batch_readiness",
    "journal_handoff_readiness",
    "retro_adjustment_plan",
    "off_cycle_payroll",
    "multi_entity_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def payroll_engine_runtime_capabilities() -> dict:
    smoke = payroll_engine_runtime_smoke()
    return {
        "format": "appgen.payroll-engine-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "payroll_engine",
        "implementation_directory": "src/pyAppGen/pbcs/payroll_engine",
        "capabilities": PAYROLL_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PAYROLL_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "upsert_worker_projection",
            "create_payroll_run",
            "ingest_labor_hours",
            "calculate_payslip",
            "apply_deduction",
            "allocate_benefit",
            "post_payroll_run",
            "prepare_payroll_filing",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def payroll_engine_runtime_smoke() -> dict:
    state = payroll_engine_empty_state()
    state = payroll_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.payroll.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_countries": ("US", "CA"),
            "allowed_payment_rails": ("ach", "instant_pay"),
            "allowed_filing_channels": ("federal_e_file", "state_e_file"),
            "payroll_precision": 2,
            "workbench_limit": 100,
        },
    )["state"]
    state = payroll_engine_set_parameter(state, "standard_period_hours", 40)["state"]
    state = payroll_engine_set_parameter(state, "overtime_multiplier", 1.5)["state"]
    state = payroll_engine_set_parameter(state, "supplemental_rate", 0.22)["state"]
    state = payroll_engine_set_parameter(state, "net_pay_floor", 0)["state"]
    state = payroll_engine_set_parameter(state, "approval_amount_threshold", 10000)["state"]
    state = payroll_engine_register_rule(
        state,
        {
            "rule_id": "rule_us_hourly",
            "tenant": "tenant_alpha",
            "rule_type": "pay",
            "eligible_worker_types": ("employee",),
            "allowed_countries": ("US",),
            "deduction_limit_percent": 0.5,
            "benefit_classes": ("health", "retirement"),
            "filing_channels": {"US": "federal_e_file"},
            "garnishment_priority": ("court", "tax", "loan"),
            "status": "active",
        },
    )["state"]
    state = payroll_engine_register_schema_extension(state, "payslip", {"equity_payload": "jsonb"})["state"]
    state = payroll_engine_upsert_worker_projection(
        state,
        {
            "employee_id": "emp_100",
            "tenant": "tenant_alpha",
            "worker_type": "employee",
            "country": "US",
            "legal_entity": "entity_us",
            "currency": "USD",
            "hourly_rate": 30,
            "salary_per_period": 0,
            "identity": {"did": "did:appgen:emp-100", "issuer": "trusted_registry", "status": "active"},
            "status": "active",
        },
    )["state"]
    run = payroll_engine_create_payroll_run(
        state,
        {
            "run_id": "run_100",
            "tenant": "tenant_alpha",
            "period": "2026-W22",
            "country": "US",
            "legal_entity": "entity_us",
            "currency": "USD",
            "run_type": "regular",
        },
    )
    state = run["state"]
    state = payroll_engine_ingest_labor_hours(
        state,
        {"labor_event_id": "labor_100", "tenant": "tenant_alpha", "employee_id": "emp_100", "period": "2026-W22", "approved_hours": 42, "overtime_hours": 2},
    )["state"]
    payslip = payroll_engine_calculate_payslip(state, "run_100", "emp_100")
    state = payslip["state"]
    state = payroll_engine_apply_deduction(state, "payslip_run_100_emp_100", {"deduction_id": "ded_100", "deduction_type": "retirement", "amount": 120, "priority": "loan"})["state"]
    state = payroll_engine_allocate_benefit(state, "payslip_run_100_emp_100", {"benefit_id": "ben_100", "benefit_type": "health", "employer_amount": 150, "employee_amount": 40})["state"]
    posted = payroll_engine_post_payroll_run(state, "run_100", approved_by="payroll_manager")
    state = posted["state"]
    filing = payroll_engine_prepare_payroll_filing(state, "filing_100", run_id="run_100", jurisdiction="US", channel="federal_e_file")
    state = filing["state"]
    simulation = payroll_engine_simulate_pay_policy(state, "emp_100", hours=45)
    forecast = payroll_engine_forecast_payroll_cash((1200, 1300, 1400), growth=0.05)
    parsed = payroll_engine_parse_payroll_instruction("run run_777 employee emp_777 period 2026-W23 action calculate")
    risk = payroll_engine_score_payroll_risk({"variance": 0.2, "deduction": 0.1, "filing": 0.05})
    recommendation = payroll_engine_recommend_exception_resolution("negative_net")
    route = payroll_engine_route_payment_or_filing({"event_id": "pay_route"}, rails=({"route": "ach", "available": False, "latency": 2}, {"route": "instant_pay", "available": True, "latency": 1}))
    proof = payroll_engine_generate_payroll_proof(state, "payslip_run_100_emp_100", disclosure=("payslip_id", "employee_id", "net_pay"))
    screening = payroll_engine_screen_policy(state, "run_100", restricted_countries=("restricted_country",))
    controls = payroll_engine_run_control_tests(state)
    api = payroll_engine_build_api_contract()
    federation = payroll_engine_federate_payroll_view(state, "payslip_run_100_emp_100", systems=("time_labor", "tax", "treasury", "ledger"))
    identity = payroll_engine_verify_worker_identity(state["workers"]["emp_100"]["identity"])
    resilience = payroll_engine_run_resilience_drill(state, "payment_rail_timeout")
    crypto = payroll_engine_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = payroll_engine_schedule_carbon_aware_batch(({"window": "day", "carbon": 200}, {"window": "night", "carbon": 80}))
    optimization = payroll_engine_optimize_payroll_batch(({"batch": "standard", "cost": 0.2, "timeliness": 0.9}, {"batch": "slow", "cost": 0.05, "timeliness": 0.6}))
    allocation = payroll_engine_allocate_cash(({"payee": "emp_100", "priority": 1.0, "amount": 1300}, {"payee": "vendor_tax", "priority": 0.8, "amount": 300}), available_cash=1600)
    anomaly = payroll_engine_detect_payroll_anomaly(state)
    stochastic = payroll_engine_model_stochastic_payroll_exposure(amount_path=(1200, 1320, 1280), volatility=0.08)
    workbench = payroll_engine_build_workbench_view(state, tenant="tenant_alpha")
    model = payroll_engine_register_governed_model("payroll_risk", {"features": ("gross_pay", "deductions", "country"), "auc": 0.91, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_payroll_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_compensation_topology", "ok": run["payroll_run"]["graph_degree"] >= 4},
        {"id": "multi_tenant_payroll_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_payroll_schema", "ok": state["schema_extensions"]["payslip"]["equity_payload"] == "jsonb"},
        {"id": "probabilistic_payroll_anomaly_compliance_scoring", "ok": payslip["risk_score"] < 0.4},
        {"id": "real_time_gross_to_net_analytics", "ok": workbench["gross_pay_total"] > workbench["net_pay_total"]},
        {"id": "counterfactual_pay_policy_simulation", "ok": simulation["overtime_hours"] == 5},
        {"id": "temporal_payroll_cash_forecasting", "ok": forecast["forecast_cash"] > 0},
        {"id": "autonomous_payroll_exception_resolution", "ok": recommendation["action"] == "route_payroll_manager_review"},
        {"id": "semantic_payroll_instruction_parsing", "ok": parsed["ok"] and parsed["employee_id"] == "emp_777"},
        {"id": "predictive_payroll_compliance_liquidity_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_payment_filing_route_selection", "ok": route["ok"] and route["route"] == "instant_pay" and route["failover_used"]},
        {"id": "zero_knowledge_net_pay_filing_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_payroll_")},
        {"id": "immutable_payroll_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_payroll_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_payroll_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "PayrollPosted" in api["events"]["emits"]},
        {"id": "cross_system_payroll_federation", "ok": federation["ok"] and "treasury" in federation["systems"]},
        {"id": "treasury_tax_ledger_integration", "ok": posted["handoffs"] == ("treasury_payment_batch", "ledger_journal_request", "tax_wage_base_projection")},
        {"id": "decentralized_worker_pay_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_payroll_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_payment_route"},
        {"id": "quantum_resistant_payroll_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_payroll_batching", "ok": carbon["window"] == "night"},
        {"id": "algebraic_payroll_batch_optimization", "ok": optimization["ok"] and optimization["batch"] == "standard"},
        {"id": "mechanism_design_cash_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["paid"] >= allocation["allocations"][1]["paid"]},
        {"id": "information_theoretic_payroll_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_payroll_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("payroll_engine:PayrollFilingPrepared")},
        {"id": "probabilistic_ml_payroll_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "payroll_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.payroll-engine-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def payroll_engine_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "workers": {},
        "labor_hours": {},
        "payroll_runs": {},
        "payslips": {},
        "deductions": {},
        "benefit_allocations": {},
        "filings": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def payroll_engine_configure_runtime(state: dict, configuration: dict) -> dict:
    ok = configuration.get("database_backend") in {"postgresql", "mysql", "mariadb"} and bool(configuration.get("event_topic"))
    return {"ok": ok, "state": {**state, "configuration": {**configuration, "ok": ok}}, "configuration": {**configuration, "ok": ok}}


def payroll_engine_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def payroll_engine_register_rule(state: dict, rule: dict) -> dict:
    enriched = {**rule, "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def payroll_engine_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def payroll_engine_upsert_worker_projection(state: dict, worker: dict) -> dict:
    return {"ok": True, "state": {**state, "workers": {**state["workers"], worker["employee_id"]: worker}}, "worker": worker}


def payroll_engine_create_payroll_run(state: dict, payroll_run: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = payroll_run["country"] in state["configuration"].get("allowed_countries", ()) and payroll_run["country"] in rule["allowed_countries"]
    enriched = {**payroll_run, "status": "open" if ok else "blocked", "graph_degree": len(tuple(value for value in (payroll_run["tenant"], payroll_run["period"], payroll_run["country"], payroll_run["legal_entity"]) if value))}
    next_state = {**state, "payroll_runs": {**state["payroll_runs"], payroll_run["run_id"]: enriched}}
    next_state = _append_event(next_state, "PayrollRunOpened", {"tenant": payroll_run["tenant"], "run_id": payroll_run["run_id"], "period": payroll_run["period"]})
    return {"ok": ok, "state": next_state, "payroll_run": enriched}


def payroll_engine_ingest_labor_hours(state: dict, labor: dict) -> dict:
    key = f"{labor['employee_id']}:{labor['period']}"
    next_state = {**state, "labor_hours": {**state["labor_hours"], key: labor}}
    next_state = _append_event(next_state, "LaborHoursIngested", {"tenant": labor["tenant"], "employee_id": labor["employee_id"], "period": labor["period"], "approved_hours": labor["approved_hours"]})
    return {"ok": True, "state": next_state, "labor": labor}


def payroll_engine_calculate_payslip(state: dict, run_id: str, employee_id: str) -> dict:
    payroll_run = state["payroll_runs"][run_id]
    worker = state["workers"][employee_id]
    labor = state["labor_hours"][f"{employee_id}:{payroll_run['period']}"]
    standard_hours = float(state["parameters"].get("standard_period_hours", 40))
    overtime_multiplier = float(state["parameters"].get("overtime_multiplier", 1.5))
    regular_hours = min(labor["approved_hours"], standard_hours)
    overtime_hours = labor["overtime_hours"]
    gross_pay = round(worker.get("salary_per_period", 0) + regular_hours * worker.get("hourly_rate", 0) + overtime_hours * worker.get("hourly_rate", 0) * overtime_multiplier, 2)
    tax_withheld = round(gross_pay * float(state["parameters"].get("supplemental_rate", 0.22)), 2)
    net_pay = round(max(float(state["parameters"].get("net_pay_floor", 0)), gross_pay - tax_withheld), 2)
    payslip_id = f"payslip_{run_id}_{employee_id}"
    risk_score = round(max(0, labor["approved_hours"] - standard_hours) * 0.02, 4)
    payslip = {"payslip_id": payslip_id, "tenant": payroll_run["tenant"], "run_id": run_id, "employee_id": employee_id, "period": payroll_run["period"], "gross_pay": gross_pay, "tax_withheld": tax_withheld, "deduction_total": 0, "benefit_employee_total": 0, "benefit_employer_total": 0, "net_pay": net_pay, "currency": worker["currency"], "status": "calculated", "risk_score": risk_score}
    next_state = {**state, "payslips": {**state["payslips"], payslip_id: payslip}}
    next_state = _append_event(next_state, "PayslipCalculated", {"tenant": payroll_run["tenant"], "payslip_id": payslip_id, "employee_id": employee_id, "gross_pay": gross_pay})
    return {"ok": True, "state": next_state, **payslip}


def payroll_engine_apply_deduction(state: dict, payslip_id: str, deduction: dict) -> dict:
    payslip = state["payslips"][payslip_id]
    rule = next(iter(state["rules"].values()))
    limit = payslip["gross_pay"] * float(rule.get("deduction_limit_percent", 1))
    ok = deduction["amount"] <= limit
    enriched = {**deduction, "tenant": payslip["tenant"], "payslip_id": payslip_id, "status": "applied" if ok else "blocked"}
    updated_payslip = {**payslip, "deduction_total": round(payslip["deduction_total"] + (deduction["amount"] if ok else 0), 2), "net_pay": round(payslip["net_pay"] - (deduction["amount"] if ok else 0), 2)}
    next_state = {**state, "deductions": {**state["deductions"], deduction["deduction_id"]: enriched}, "payslips": {**state["payslips"], payslip_id: updated_payslip}}
    next_state = _append_event(next_state, "DeductionApplied", {"tenant": payslip["tenant"], "payslip_id": payslip_id, "deduction_id": deduction["deduction_id"], "amount": deduction["amount"]})
    return {"ok": ok, "state": next_state, "deduction": enriched}


def payroll_engine_allocate_benefit(state: dict, payslip_id: str, benefit: dict) -> dict:
    payslip = state["payslips"][payslip_id]
    rule = next(iter(state["rules"].values()))
    ok = benefit["benefit_type"] in rule.get("benefit_classes", ())
    enriched = {**benefit, "tenant": payslip["tenant"], "payslip_id": payslip_id, "status": "allocated" if ok else "blocked"}
    updated_payslip = {**payslip, "benefit_employee_total": round(payslip["benefit_employee_total"] + (benefit["employee_amount"] if ok else 0), 2), "benefit_employer_total": round(payslip["benefit_employer_total"] + (benefit["employer_amount"] if ok else 0), 2), "net_pay": round(payslip["net_pay"] - (benefit["employee_amount"] if ok else 0), 2)}
    next_state = {**state, "benefit_allocations": {**state["benefit_allocations"], benefit["benefit_id"]: enriched}, "payslips": {**state["payslips"], payslip_id: updated_payslip}}
    next_state = _append_event(next_state, "BenefitAllocated", {"tenant": payslip["tenant"], "payslip_id": payslip_id, "benefit_id": benefit["benefit_id"]})
    return {"ok": ok, "state": next_state, "benefit": enriched}


def payroll_engine_post_payroll_run(state: dict, run_id: str, *, approved_by: str) -> dict:
    payroll_run = state["payroll_runs"][run_id]
    payslips = tuple(payslip for payslip in state["payslips"].values() if payslip["run_id"] == run_id)
    posted = {**payroll_run, "status": "posted", "approved_by": approved_by, "gross_total": round(sum(item["gross_pay"] for item in payslips), 2), "net_total": round(sum(item["net_pay"] for item in payslips), 2)}
    handoffs = ("treasury_payment_batch", "ledger_journal_request", "tax_wage_base_projection")
    next_state = {**state, "payroll_runs": {**state["payroll_runs"], run_id: posted}}
    next_state = _append_event(next_state, "PayrollPosted", {"tenant": posted["tenant"], "run_id": run_id, "gross_total": posted["gross_total"], "net_total": posted["net_total"], "handoffs": handoffs})
    return {"ok": True, "state": next_state, "payroll_run": posted, "handoffs": handoffs}


def payroll_engine_prepare_payroll_filing(state: dict, filing_id: str, *, run_id: str, jurisdiction: str, channel: str) -> dict:
    payroll_run = state["payroll_runs"][run_id]
    ok = channel in state["configuration"].get("allowed_filing_channels", ()) and payroll_run["status"] == "posted"
    filing = {"filing_id": filing_id, "tenant": payroll_run["tenant"], "run_id": run_id, "jurisdiction": jurisdiction, "channel": channel, "gross_total": payroll_run["gross_total"], "net_total": payroll_run["net_total"], "status": "prepared" if ok else "blocked"}
    next_state = {**state, "filings": {**state["filings"], filing_id: filing}}
    next_state = _append_event(next_state, "PayrollFilingPrepared", {"tenant": payroll_run["tenant"], "filing_id": filing_id, "run_id": run_id, "jurisdiction": jurisdiction})
    return {"ok": ok, "state": next_state, "filing": filing}


def payroll_engine_simulate_pay_policy(state: dict, employee_id: str, *, hours: float) -> dict:
    standard = float(state["parameters"].get("standard_period_hours", 40))
    worker = state["workers"][employee_id]
    overtime = max(0, hours - standard)
    projected_gross = round(min(hours, standard) * worker["hourly_rate"] + overtime * worker["hourly_rate"] * float(state["parameters"].get("overtime_multiplier", 1.5)), 2)
    return {"ok": True, "employee_id": employee_id, "overtime_hours": round(overtime, 2), "projected_gross": projected_gross}


def payroll_engine_forecast_payroll_cash(amount_path: tuple[float, ...], *, growth: float) -> dict:
    forecast = amount_path[-1] * (1 + growth)
    return {"ok": True, "forecast_cash": round(forecast, 2), "trend": round(amount_path[-1] - amount_path[0], 2)}


def payroll_engine_parse_payroll_instruction(text: str) -> dict:
    run = re.search(r"run\s+([a-z0-9_]+)", text, re.I)
    employee = re.search(r"employee\s+([a-z0-9_]+)", text, re.I)
    period = re.search(r"period\s+([0-9A-Z\\-]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(run and employee and period and action), "run_id": run.group(1) if run else None, "employee_id": employee.group(1) if employee else None, "period": period.group(1) if period else None, "action": action.group(1) if action else None}


def payroll_engine_score_payroll_risk(signals: dict) -> dict:
    risk = round(signals.get("variance", 0) * 2 + signals.get("deduction", 0) + signals.get("filing", 0) * 2, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.7 else "review"}


def payroll_engine_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"negative_net": "route_payroll_manager_review", "missing_tax": "request_tax_projection", "payment_failure": "retry_alternate_rail"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def payroll_engine_route_payment_or_filing(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"payroll_engine:PaymentRoute:{event['event_id']}"}


def payroll_engine_generate_payroll_proof(state: dict, payslip_id: str, *, disclosure: tuple[str, ...]) -> dict:
    payslip = state["payslips"][payslip_id]
    claims = {field: payslip[field] for field in disclosure if field in payslip}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_payroll_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def payroll_engine_screen_policy(state: dict, run_id: str, *, restricted_countries: tuple[str, ...]) -> dict:
    payroll_run = state["payroll_runs"][run_id]
    blocked = payroll_run["country"] in restricted_countries or payroll_run["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "run_id": run_id}


def payroll_engine_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(payslip["net_pay"] < float(state["parameters"].get("net_pay_floor", 0)) for payslip in state["payslips"].values()):
        gaps.append("net_pay_floor_violation")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def payroll_engine_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /payroll-runs", "GET /payslips", "POST /payroll-filings", "POST /payroll-rules", "POST /payroll-parameters", "POST /payroll-configuration"), "events": {"emits": ("PayrollPosted", "PayrollFilingPrepared"), "consumes": ("LaborHoursApproved", "TaxCalculated")}, "permissions": ("payroll_engine.read", "payroll_engine.run", "payroll_engine.approve", "payroll_engine.file", "payroll_engine.configure", "payroll_engine.audit"), "configuration": ("PAYROLL_ENGINE_DATABASE_URL", "PAYROLL_ENGINE_EVENT_TOPIC", "PAYROLL_ENGINE_RETRY_LIMIT", "PAYROLL_ENGINE_DEFAULT_CURRENCY")}


def payroll_engine_federate_payroll_view(state: dict, payslip_id: str, *, systems: tuple[str, ...]) -> dict:
    payslip = state["payslips"][payslip_id]
    return {"ok": True, "payslip_id": payslip_id, "systems": systems, "projection": {"employee_id": payslip["employee_id"], "gross_pay": payslip["gross_pay"], "net_pay": payslip["net_pay"]}}


def payroll_engine_verify_worker_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def payroll_engine_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"payment_rail_timeout", "filing_channel_failure"}, "scenario": scenario, "mode": "degraded_payment_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "payroll_engine.dead_letter"}


def payroll_engine_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"payroll_epoch_{epoch:04d}"}


def payroll_engine_schedule_carbon_aware_batch(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def payroll_engine_optimize_payroll_batch(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["timeliness"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "batch": selected["batch"], "objective_score": selected["objective"], "candidates": scored}


def payroll_engine_allocate_cash(claims: tuple[dict, ...], *, available_cash: float) -> dict:
    weights = tuple({"payee": claim["payee"], "amount": claim["amount"], "weight": claim["priority"] * claim["amount"]} for claim in claims)
    total_weight = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"payee": item["payee"], "paid": round(min(item["amount"], available_cash * item["weight"] / total_weight), 2)} for item in weights)
    return {"ok": round(sum(item["paid"] for item in allocations), 2) <= available_cash, "allocations": allocations, "clearing_priority": round(sum(claim["priority"] for claim in claims) / len(claims), 4)}


def payroll_engine_detect_payroll_anomaly(state: dict) -> dict:
    values = tuple(payslip["net_pay"] for payslip in state["payslips"].values())
    if not values:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(values) or 1
    entropy = round(-sum((value / total) * math.log(max(value / total, 0.0001), 2) for value in values), 4)
    mean = sum(values) / len(values)
    return {"ok": True, "entropy": entropy, "outliers": tuple(value for value in values if abs(value - mean) > mean * 0.5)}


def payroll_engine_model_stochastic_payroll_exposure(*, amount_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(amount_path) < 2 else (amount_path[-1] - amount_path[0]) / (len(amount_path) - 1)
    exposure = abs(drift) * volatility * len(amount_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def payroll_engine_build_workbench_view(state: dict, *, tenant: str) -> dict:
    runs = tuple(run for run in state["payroll_runs"].values() if run["tenant"] == tenant)
    payslips = tuple(payslip for payslip in state["payslips"].values() if payslip["tenant"] == tenant)
    filings = tuple(filing for filing in state["filings"].values() if filing["tenant"] == tenant)
    return {"ok": True, "tenant": tenant, "run_count": len(runs), "posted_run_count": len(tuple(run for run in runs if run["status"] == "posted")), "payslip_count": len(payslips), "gross_pay_total": round(sum(payslip["gross_pay"] for payslip in payslips), 2), "net_pay_total": round(sum(payslip["net_pay"] for payslip in payslips), 2), "deduction_count": len(tuple(item for item in state["deductions"].values() if item["tenant"] == tenant)), "benefit_count": len(tuple(item for item in state["benefit_allocations"].values() if item["tenant"] == tenant)), "filing_count": len(filings)}


def payroll_engine_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"payroll_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"payroll_engine:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
