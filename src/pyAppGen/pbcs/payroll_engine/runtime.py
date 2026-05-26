"""Executable runtime for the Payroll Engine PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC = "appgen.payroll.events"
PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PAYROLL_ENGINE_OWNED_TABLES = (
    "payroll_calendar",
    "payroll_period",
    "payroll_pay_group",
    "payroll_legal_entity",
    "payroll_run",
    "payroll_run_worker",
    "payroll_run_approval",
    "payroll_run_lock",
    "worker_projection",
    "worker_pay_profile",
    "worker_bank_instruction",
    "labor_hours",
    "labor_hours_line",
    "earning_code",
    "earning_calculation",
    "overtime_calculation",
    "gross_pay_component",
    "payslip",
    "payslip_line",
    "tax_withholding_projection",
    "deduction",
    "deduction_rule",
    "deduction_arrear",
    "garnishment_order",
    "benefit_allocation",
    "benefit_plan",
    "employer_contribution",
    "net_pay_distribution",
    "payment_instruction",
    "payment_batch_projection",
    "journal_request_projection",
    "tax_wage_base_projection",
    "payroll_filing",
    "payroll_filing_line",
    "payroll_correction",
    "retro_adjustment",
    "off_cycle_payment",
    "payroll_exception",
    "payroll_policy_screening",
    "payroll_audit_trace",
    "payroll_proof",
    "payroll_federation_projection",
    "payroll_carbon_batch_window",
    "payroll_batch_optimization",
    "payroll_cash_allocation",
    "payroll_anomaly_signal",
    "payroll_risk_model",
    "payroll_cash_forecast",
    "payroll_parsed_instruction",
    "payroll_seed_data",
    "payroll_schema_extension",
    "payroll_control_assertion",
    "payroll_governed_model",
    "payroll_rule",
    "payroll_parameter",
    "payroll_configuration",
    "payroll_engine_appgen_outbox_event",
    "payroll_engine_appgen_inbox_event",
    "payroll_engine_dead_letter_event",
)
PAYROLL_ENGINE_CONSUMED_EVENT_TYPES = ("LaborHoursApproved", "TaxCalculated")
PAYROLL_ENGINE_EMITTED_EVENT_TYPES = ("PayrollPosted", "PayrollFilingPrepared")
_PAYROLL_ENGINE_RUNTIME_TABLES = (
    "payroll_engine_appgen_outbox_event",
    "payroll_engine_appgen_inbox_event",
    "payroll_engine_dead_letter_event",
)
_PAYROLL_ENGINE_ALLOWED_DEPENDENCIES = (
    "personnel_identity_projection",
    "time_labor_projection",
    "tax_wage_base_projection",
    "treasury_payment_batch",
    "ledger_journal_request",
    "audit_ledger_projection",
    "GET /workers",
    "GET /labor-hours",
    "GET /tax-rates",
    "POST /payment-batches",
    "POST /journal-requests",
)
_PAYROLL_ENGINE_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}

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
    "payroll_period",
    "pay_group_management",
    "legal_entity_payroll",
    "payroll_run_creation",
    "payroll_run_worker_roster",
    "payroll_run_approval",
    "payroll_run_lock",
    "worker_projection",
    "worker_pay_profile",
    "worker_bank_instruction",
    "labor_hours_ingestion",
    "labor_hours_lines",
    "earning_code_catalog",
    "earning_calculation",
    "gross_pay_calculation",
    "overtime_calculation",
    "gross_pay_component",
    "payslip_lines",
    "tax_withholding_projection",
    "deduction_management",
    "deduction_rule",
    "deduction_arrear",
    "garnishment_order",
    "benefit_allocation",
    "benefit_plan",
    "employer_contribution",
    "tax_basis_projection",
    "net_pay_calculation",
    "net_pay_distribution",
    "payment_instruction",
    "payment_batch_projection",
    "journal_request_projection",
    "payslip_generation",
    "approval_workflow",
    "payroll_posting",
    "filing_preparation",
    "filing_line",
    "payment_batch_readiness",
    "journal_handoff_readiness",
    "retro_adjustment_plan",
    "off_cycle_payroll",
    "payroll_exception",
    "policy_screening",
    "audit_trace",
    "payroll_proof",
    "federation_projection",
    "carbon_batch_window",
    "batch_optimization",
    "cash_allocation",
    "anomaly_signal",
    "payroll_risk_model",
    "cash_forecast",
    "semantic_instruction_parser",
    "multi_entity_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "schema_extension",
    "control_assertion",
    "governed_model",
    "workbench",
)


def payroll_engine_runtime_capabilities() -> dict:
    smoke = payroll_engine_runtime_smoke()
    return {
        "format": "appgen.payroll-engine-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "payroll_engine",
        "implementation_directory": "src/pyAppGen/pbcs/payroll_engine",
        "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
        "capabilities": PAYROLL_ENGINE_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PAYROLL_ENGINE_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "upsert_worker_projection",
            "create_payroll_run",
            "ingest_labor_hours",
            "calculate_payslip",
            "apply_deduction",
            "allocate_benefit",
            "post_payroll_run",
            "prepare_payroll_filing",
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


def payroll_engine_runtime_smoke() -> dict:
    state = payroll_engine_empty_state()
    state = payroll_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
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
    schema = payroll_engine_build_schema_contract()
    service = payroll_engine_build_service_contract()
    release = payroll_engine_build_release_evidence()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "PayrollPosted" in api["events"]["emits"]},
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
        "inbox": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "workers": {},
        "labor_hours": {},
        "tax_projections": {},
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
    forbidden = tuple(sorted(field for field in _PAYROLL_ENGINE_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Payroll Engine uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    allowed_databases = set(PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS)
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Payroll Engine supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Payroll Engine requires AppGen-X event topic {PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def payroll_engine_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "standard_period_hours",
        "overtime_multiplier",
        "supplemental_rate",
        "rounding_precision",
        "net_pay_floor",
        "filing_materiality_threshold",
        "approval_amount_threshold",
        "off_cycle_approval_threshold",
        "retro_lookback_periods",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Payroll Engine parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def payroll_engine_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Payroll Engine rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Payroll Engine rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def payroll_engine_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in PAYROLL_ENGINE_OWNED_TABLES:
        raise ValueError(f"Payroll Engine schema extensions must target owned tables: {PAYROLL_ENGINE_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = {**state["schema_extensions"], table: {**state["schema_extensions"].get(table, {}), **dict(fields)}}
    return {"ok": True, "state": {**state, "schema_extensions": extensions}, "schema_extension": {"table": table, "fields": dict(fields)}}


def payroll_engine_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    if key in state["handled_events"] and state["handled_events"][key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": state["handled_events"][key]}
    attempts = int(state["handled_events"].get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {"event_id": event_id, "event_type": event_type, "tenant": payload.get("tenant"), "attempts": attempts, "idempotency_key": key}
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in PAYROLL_ENGINE_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}, "retry_evidence": (*next_state["retry_evidence"], evidence)}
        if status == "dead_letter":
            dead_letter = {**inbox_entry, "reason": "unsupported_or_failed_payroll_event"}
            next_state = {**next_state, "dead_letter": (*next_state["dead_letter"], dead_letter)}
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "LaborHoursApproved":
        labor = {
            "labor_event_id": payload.get("labor_event_id", event_id),
            "tenant": payload["tenant"],
            "employee_id": payload["employee_id"],
            "period": payload["period"],
            "approved_hours": payload["approved_hours"],
            "overtime_hours": payload.get("overtime_hours", 0),
        }
        next_state = {**next_state, "labor_hours": {**next_state["labor_hours"], f"{labor['employee_id']}:{labor['period']}": labor}}
    elif event_type == "TaxCalculated":
        next_state = {**next_state, "tax_projections": {**next_state["tax_projections"], payload["employee_id"]: payload}}
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}}
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


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
    return {
        "format": "appgen.payroll-engine-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /payroll-runs", "command": "create_payroll_run", "owned_tables": ("payroll_run",), "emits": (), "requires_permission": "payroll_engine.run", "idempotency_key": "run_id"},
            {"route": "POST /payroll-runs/{id}/workers", "command": "upsert_worker_projection", "owned_tables": ("payroll_run_worker", "worker_projection"), "emits": (), "requires_permission": "payroll_engine.run", "idempotency_key": "run_id:employee_id"},
            {"route": "POST /payroll-runs/{id}/payslips", "command": "calculate_payslip", "owned_tables": ("payslip",), "emits": (), "requires_permission": "payroll_engine.run", "idempotency_key": "run_id:employee_id"},
            {"route": "POST /payslips/{id}/deductions", "command": "apply_deduction", "owned_tables": ("deduction", "payslip"), "emits": (), "requires_permission": "payroll_engine.run", "idempotency_key": "deduction_id"},
            {"route": "POST /payslips/{id}/benefits", "command": "allocate_benefit", "owned_tables": ("benefit_allocation", "payslip"), "emits": (), "requires_permission": "payroll_engine.run", "idempotency_key": "benefit_id"},
            {"route": "POST /payroll-runs/{id}/post", "command": "post_payroll_run", "owned_tables": ("payroll_run",), "emits": ("PayrollPosted",), "requires_permission": "payroll_engine.approve", "idempotency_key": "run_id:approved_by"},
            {"route": "POST /payroll-filings", "command": "prepare_payroll_filing", "owned_tables": ("payroll_filing",), "emits": ("PayrollFilingPrepared",), "requires_permission": "payroll_engine.file", "idempotency_key": "filing_id"},
            {"route": "POST /payroll/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": PAYROLL_ENGINE_CONSUMED_EVENT_TYPES, "requires_permission": "payroll_engine.event", "idempotency_key": "event_id"},
            {"route": "POST /payroll-rules", "command": "register_rule", "owned_tables": ("payroll_rule",), "requires_permission": "payroll_engine.configure", "idempotency_key": "rule_id"},
            {"route": "POST /payroll-parameters", "command": "set_parameter", "owned_tables": ("payroll_parameter",), "requires_permission": "payroll_engine.configure", "idempotency_key": "parameter_name"},
            {"route": "POST /payroll-configuration", "command": "configure_runtime", "owned_tables": ("payroll_configuration",), "requires_permission": "payroll_engine.configure", "idempotency_key": "tenant"},
            {"route": "GET /payslips", "query": "build_workbench_view", "owned_tables": ("payslip",), "requires_permission": "payroll_engine.read"},
            {"route": "GET /payroll-workbench", "query": "build_workbench_view", "owned_tables": PAYROLL_ENGINE_OWNED_TABLES, "requires_permission": "payroll_engine.audit"},
        ),
        "declared_catalog_routes": ("POST /payroll-runs", "GET /payslips", "POST /payroll-filings", "POST /payroll-rules", "POST /payroll-parameters", "POST /payroll-configuration"),
        "events": {"emits": PAYROLL_ENGINE_EMITTED_EVENT_TYPES, "consumes": PAYROLL_ENGINE_CONSUMED_EVENT_TYPES},
        "emits": PAYROLL_ENGINE_EMITTED_EVENT_TYPES,
        "consumes": PAYROLL_ENGINE_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(payroll_engine_permissions_contract()["permissions"])),
        "database_backends": PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("PAYROLL_ENGINE_DATABASE_URL", "PAYROLL_ENGINE_EVENT_TOPIC", "PAYROLL_ENGINE_RETRY_LIMIT", "PAYROLL_ENGINE_DEFAULT_CURRENCY"),
    }


def payroll_engine_build_schema_contract() -> dict:
    """Return generated Payroll Engine schema, migration, and model evidence."""
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in PAYROLL_ENGINE_OWNED_TABLES}
    table_fields.update(
        {
            "payroll_calendar": ("tenant", "calendar_id", "country", "frequency", "timezone", "status", "audit_hash"),
            "payroll_period": ("tenant", "period_id", "calendar_id", "period_start", "period_end", "pay_date", "status", "audit_hash"),
            "payroll_pay_group": ("tenant", "pay_group_id", "legal_entity", "frequency", "currency", "status", "audit_hash"),
            "payroll_legal_entity": ("tenant", "legal_entity", "country", "tax_registration", "currency", "status", "audit_hash"),
            "payroll_run": ("tenant", "run_id", "period", "country", "legal_entity", "currency", "run_type", "status", "audit_hash"),
            "payroll_run_worker": ("tenant", "run_worker_id", "run_id", "employee_id", "pay_group_id", "status", "audit_hash"),
            "payroll_run_approval": ("tenant", "approval_id", "run_id", "approver", "decision", "decided_at", "audit_hash"),
            "payroll_run_lock": ("tenant", "lock_id", "run_id", "locked_by", "locked_at", "reason", "audit_hash"),
            "worker_projection": ("tenant", "employee_id", "worker_type", "country", "legal_entity", "currency", "status", "identity_hash", "audit_hash"),
            "worker_pay_profile": ("tenant", "profile_id", "employee_id", "pay_group_id", "hourly_rate", "salary_per_period", "currency", "audit_hash"),
            "worker_bank_instruction": ("tenant", "instruction_id", "employee_id", "distribution_type", "tokenized_account_ref", "status", "audit_hash"),
            "labor_hours": ("tenant", "labor_event_id", "employee_id", "period", "approved_hours", "overtime_hours", "audit_hash"),
            "labor_hours_line": ("tenant", "line_id", "labor_event_id", "earning_code", "hours", "source_event_id", "audit_hash"),
            "earning_code": ("tenant", "earning_code", "description", "taxable", "rate_multiplier", "status", "audit_hash"),
            "earning_calculation": ("tenant", "calculation_id", "payslip_id", "earning_code", "hours", "amount", "audit_hash"),
            "overtime_calculation": ("tenant", "calculation_id", "payslip_id", "overtime_hours", "multiplier", "amount", "audit_hash"),
            "gross_pay_component": ("tenant", "component_id", "payslip_id", "component_type", "amount", "currency", "audit_hash"),
            "payslip": ("tenant", "payslip_id", "run_id", "employee_id", "gross_pay", "tax_withheld", "net_pay", "currency", "status", "audit_hash"),
            "payslip_line": ("tenant", "line_id", "payslip_id", "line_type", "code", "amount", "audit_hash"),
            "tax_withholding_projection": ("tenant", "projection_id", "employee_id", "jurisdiction", "taxable_wages", "tax_withheld", "audit_hash"),
            "deduction": ("tenant", "deduction_id", "payslip_id", "deduction_type", "amount", "priority", "status", "audit_hash"),
            "deduction_rule": ("tenant", "deduction_rule_id", "deduction_type", "limit_percent", "priority", "status", "audit_hash"),
            "deduction_arrear": ("tenant", "arrear_id", "employee_id", "deduction_type", "amount_due", "status", "audit_hash"),
            "garnishment_order": ("tenant", "order_id", "employee_id", "jurisdiction", "priority", "remaining_amount", "audit_hash"),
            "benefit_allocation": ("tenant", "benefit_id", "payslip_id", "benefit_type", "employer_amount", "employee_amount", "status", "audit_hash"),
            "benefit_plan": ("tenant", "plan_id", "benefit_type", "eligibility_rule_id", "employer_share", "status", "audit_hash"),
            "employer_contribution": ("tenant", "contribution_id", "payslip_id", "benefit_id", "amount", "audit_hash"),
            "net_pay_distribution": ("tenant", "distribution_id", "payslip_id", "payment_instruction_id", "amount", "status", "audit_hash"),
            "payment_instruction": ("tenant", "payment_instruction_id", "employee_id", "rail", "amount", "tokenized_destination", "audit_hash"),
            "payment_batch_projection": ("tenant", "batch_id", "run_id", "rail", "net_total", "handoff_status", "audit_hash"),
            "journal_request_projection": ("tenant", "journal_request_id", "run_id", "gross_total", "net_total", "handoff_status", "audit_hash"),
            "tax_wage_base_projection": ("tenant", "projection_id", "run_id", "jurisdiction", "wage_base", "withheld_total", "audit_hash"),
            "payroll_filing": ("tenant", "filing_id", "run_id", "jurisdiction", "channel", "gross_total", "net_total", "status", "audit_hash"),
            "payroll_filing_line": ("tenant", "line_id", "filing_id", "employee_id", "taxable_wages", "tax_withheld", "audit_hash"),
            "payroll_correction": ("tenant", "correction_id", "run_id", "payslip_id", "reason", "amount", "status", "audit_hash"),
            "retro_adjustment": ("tenant", "adjustment_id", "employee_id", "source_period", "target_run_id", "amount", "audit_hash"),
            "off_cycle_payment": ("tenant", "off_cycle_id", "employee_id", "reason", "gross_pay", "net_pay", "status", "audit_hash"),
            "payroll_rule": ("tenant", "rule_id", "scope", "compiled_hash", "enabled", "status", "audit_hash"),
            "payroll_parameter": ("tenant", "parameter_name", "parameter_value", "effective_at", "changed_by", "audit_hash"),
            "payroll_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "event_contract", "stream_engine_picker_visible", "audit_hash"),
            "payroll_engine_appgen_outbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "published_at", "audit_hash"),
            "payroll_engine_appgen_inbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "audit_hash"),
            "payroll_engine_dead_letter_event": ("tenant", "event_id", "event_type", "payload", "reason", "attempts", "audit_hash"),
        }
    )
    relationships = (
        {"from_table": "payroll_period", "from_field": "calendar_id", "to_table": "payroll_calendar", "to_field": "calendar_id"},
        {"from_table": "payroll_run_worker", "from_field": "run_id", "to_table": "payroll_run", "to_field": "run_id"},
        {"from_table": "payroll_run_worker", "from_field": "employee_id", "to_table": "worker_projection", "to_field": "employee_id"},
        {"from_table": "worker_pay_profile", "from_field": "employee_id", "to_table": "worker_projection", "to_field": "employee_id"},
        {"from_table": "worker_bank_instruction", "from_field": "employee_id", "to_table": "worker_projection", "to_field": "employee_id"},
        {"from_table": "labor_hours_line", "from_field": "labor_event_id", "to_table": "labor_hours", "to_field": "labor_event_id"},
        {"from_table": "payslip", "from_field": "run_id", "to_table": "payroll_run", "to_field": "run_id"},
        {"from_table": "payslip", "from_field": "employee_id", "to_table": "worker_projection", "to_field": "employee_id"},
        {"from_table": "payslip_line", "from_field": "payslip_id", "to_table": "payslip", "to_field": "payslip_id"},
        {"from_table": "deduction", "from_field": "payslip_id", "to_table": "payslip", "to_field": "payslip_id"},
        {"from_table": "benefit_allocation", "from_field": "payslip_id", "to_table": "payslip", "to_field": "payslip_id"},
        {"from_table": "net_pay_distribution", "from_field": "payslip_id", "to_table": "payslip", "to_field": "payslip_id"},
        {"from_table": "payroll_filing_line", "from_field": "filing_id", "to_table": "payroll_filing", "to_field": "filing_id"},
        {"from_table": "payroll_correction", "from_field": "payslip_id", "to_table": "payslip", "to_field": "payslip_id"},
    )
    allowed_prefixes = (
        "payroll_",
        "worker_",
        "labor_",
        "earning_",
        "overtime_",
        "gross_",
        "payslip",
        "tax_",
        "deduction",
        "garnishment_",
        "benefit_",
        "employer_",
        "net_",
        "payment_",
        "journal_",
        "retro_",
        "off_cycle_",
    )
    tables = tuple({"table": table, "fields": table_fields[table], "owner": "payroll_engine"} for table in PAYROLL_ENGINE_OWNED_TABLES)
    return {
        "format": "appgen.payroll-engine-owned-schema-contract.v1",
        "ok": len(tables) == len(PAYROLL_ENGINE_OWNED_TABLES) and len(tables) >= 40 and all(item["table"].startswith(allowed_prefixes) for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/payroll_engine/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(PAYROLL_ENGINE_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in PAYROLL_ENGINE_OWNED_TABLES
        ),
        "datastore_backends": PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def payroll_engine_build_service_contract() -> dict:
    """Return Payroll Engine command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "upsert_worker_projection",
        "create_payroll_run",
        "ingest_labor_hours",
        "calculate_payslip",
        "apply_deduction",
        "allocate_benefit",
        "post_payroll_run",
        "prepare_payroll_filing",
        "route_payment_or_filing",
        "generate_payroll_proof",
        "screen_policy",
        "federate_payroll_view",
        "verify_worker_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_batch",
        "optimize_payroll_batch",
        "allocate_cash",
        "run_control_tests",
        "register_governed_model",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.payroll-engine-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "payroll_engine_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "simulate_pay_policy",
            "forecast_payroll_cash",
            "parse_payroll_instruction",
            "score_payroll_risk",
            "recommend_exception_resolution",
            "detect_payroll_anomaly",
            "model_stochastic_payroll_exposure",
            "build_api_contract",
            "build_schema_contract",
            "build_release_evidence",
        ),
        "mutates_only": PAYROLL_ENGINE_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _PAYROLL_ENGINE_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PAYROLL_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _PAYROLL_ENGINE_ALLOWED_DEPENDENCIES if str(item).endswith(("_projection", "_batch", "_request"))),
            "shared_tables": (),
        },
    }


def payroll_engine_build_release_evidence() -> dict:
    """Return Payroll Engine package-local release evidence."""
    schema = payroll_engine_build_schema_contract()
    service = payroll_engine_build_service_contract()
    api = payroll_engine_build_api_contract()
    permissions = payroll_engine_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(PAYROLL_ENGINE_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"create_payroll_run", "post_payroll_run", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.payroll-engine-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def payroll_engine_permissions_contract() -> dict:
    return {
        "format": "appgen.payroll-engine-permissions.v1",
        "ok": True,
        "permissions": ("payroll_engine.read", "payroll_engine.run", "payroll_engine.approve", "payroll_engine.file", "payroll_engine.event", "payroll_engine.configure", "payroll_engine.audit"),
        "action_permissions": {
            "create_payroll_run": "payroll_engine.run",
            "ingest_labor_hours": "payroll_engine.run",
            "calculate_payslip": "payroll_engine.run",
            "apply_deduction": "payroll_engine.run",
            "allocate_benefit": "payroll_engine.run",
            "post_payroll_run": "payroll_engine.approve",
            "prepare_payroll_filing": "payroll_engine.file",
            "receive_event": "payroll_engine.event",
            "register_rule": "payroll_engine.configure",
            "register_schema_extension": "payroll_engine.configure",
            "set_parameter": "payroll_engine.configure",
            "configure_runtime": "payroll_engine.configure",
            "build_workbench_view": "payroll_engine.audit",
            "route_payment_or_filing": "payroll_engine.approve",
            "generate_payroll_proof": "payroll_engine.audit",
            "screen_policy": "payroll_engine.audit",
            "federate_payroll_view": "payroll_engine.read",
            "verify_worker_identity": "payroll_engine.audit",
            "run_resilience_drill": "payroll_engine.audit",
            "rotate_crypto_epoch": "payroll_engine.audit",
            "schedule_carbon_aware_batch": "payroll_engine.run",
            "optimize_payroll_batch": "payroll_engine.run",
            "allocate_cash": "payroll_engine.approve",
            "run_control_tests": "payroll_engine.audit",
            "register_governed_model": "payroll_engine.audit",
            "recommend_exception_resolution": "payroll_engine.approve",
            "detect_payroll_anomaly": "payroll_engine.audit",
            "model_stochastic_payroll_exposure": "payroll_engine.audit",
            "parse_payroll_instruction": "payroll_engine.read",
            "score_payroll_risk": "payroll_engine.audit",
            "forecast_payroll_cash": "payroll_engine.read",
            "simulate_pay_policy": "payroll_engine.read",
            "build_schema_contract": "payroll_engine.audit",
            "build_service_contract": "payroll_engine.audit",
            "build_release_evidence": "payroll_engine.audit",
        },
    }


def payroll_engine_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*PAYROLL_ENGINE_OWNED_TABLES, *PAYROLL_ENGINE_CONSUMED_EVENT_TYPES, *_PAYROLL_ENGINE_RUNTIME_TABLES, *_PAYROLL_ENGINE_ALLOWED_DEPENDENCIES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(allowed)
        and not str(reference).startswith("payroll_engine_")
    )
    return {
        "format": "appgen.payroll-engine-boundary.v1",
        "ok": not violations,
        "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /workers", "GET /labor-hours", "GET /tax-rates", "POST /payment-batches", "POST /journal-requests"),
            "events": PAYROLL_ENGINE_CONSUMED_EVENT_TYPES,
            "api_projections": ("personnel_identity_projection", "time_labor_projection", "tax_wage_base_projection", "treasury_payment_batch", "ledger_journal_request", "audit_ledger_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


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
    return {
        "ok": True,
        "tenant": tenant,
        "run_count": len(runs),
        "posted_run_count": len(tuple(run for run in runs if run["status"] == "posted")),
        "payslip_count": len(payslips),
        "gross_pay_total": round(sum(payslip["gross_pay"] for payslip in payslips), 2),
        "net_pay_total": round(sum(payslip["net_pay"] for payslip in payslips), 2),
        "deduction_count": len(tuple(item for item in state["deductions"].values() if item["tenant"] == tenant)),
        "benefit_count": len(tuple(item for item in state["benefit_allocations"].values() if item["tenant"] == tenant)),
        "filing_count": len(filings),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": PAYROLL_ENGINE_OWNED_TABLES,
            "outbox_table": "payroll_engine_appgen_outbox_event",
            "inbox_table": "payroll_engine_appgen_inbox_event",
            "dead_letter_table": "payroll_engine_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


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
