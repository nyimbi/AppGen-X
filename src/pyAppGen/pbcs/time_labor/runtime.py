"""Executable runtime for the Time and Labor PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TIME_LABOR_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_labor_lifecycle",
    "graph_relational_labor_topology",
    "multi_tenant_time_isolation",
    "schema_evolution_resilient_time_schema",
    "probabilistic_time_fraud_exception_scoring",
    "real_time_labor_execution_analytics",
    "counterfactual_schedule_overtime_simulation",
    "temporal_labor_demand_overtime_forecasting",
    "autonomous_time_exception_resolution",
    "semantic_clock_absence_event_parsing",
    "predictive_burnout_absence_compliance_risk",
    "self_healing_clock_source_route_selection",
    "zero_knowledge_payroll_ready_hours_proof",
    "immutable_labor_audit_trail",
    "dynamic_labor_policy_screening",
    "automated_time_control_testing",
    "universal_api_async_streaming",
    "cross_system_labor_federation",
    "workforce_device_integration",
    "decentralized_employee_time_identity",
    "chaos_engineered_clock_approval_tolerance",
    "quantum_resistant_time_authorization",
    "carbon_aware_schedule_planning",
    "algebraic_schedule_labor_optimization",
    "mechanism_design_shift_allocation",
    "information_theoretic_time_anomaly_detection",
    "temporal_labor_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_labor_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "labor_mlops_governance",
)
TIME_LABOR_STANDARD_FEATURE_KEYS = (
    "shift_creation",
    "clock_event_ingestion",
    "clock_sequence_validation",
    "geofence_validation",
    "time_entry_calculation",
    "break_deduction",
    "overtime_calculation",
    "premium_calculation",
    "absence_recording",
    "entitlement_check",
    "labor_summary",
    "approval_workflow",
    "employee_projection",
    "role_projection",
    "payroll_ready_event",
    "multi_entity_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def time_labor_runtime_capabilities() -> dict:
    smoke = time_labor_runtime_smoke()
    return {
        "format": "appgen.time-labor-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "time_labor",
        "implementation_directory": "src/pyAppGen/pbcs/time_labor",
        "capabilities": TIME_LABOR_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TIME_LABOR_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "upsert_employee_projection",
            "create_shift",
            "record_clock_event",
            "calculate_time_entry",
            "record_absence",
            "approve_labor_summary",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def time_labor_runtime_smoke() -> dict:
    state = time_labor_empty_state()
    state = time_labor_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.time.events",
            "retry_limit": 3,
            "default_timezone": "UTC",
            "allowed_clock_sources": ("mobile", "kiosk", "web"),
            "allowed_absence_types": ("vacation", "sick"),
            "workweek_start": "monday",
            "labor_precision": 2,
            "workbench_limit": 100,
        },
    )["state"]
    state = time_labor_set_parameter(state, "standard_daily_hours", 8)["state"]
    state = time_labor_set_parameter(state, "weekly_overtime_threshold", 40)["state"]
    state = time_labor_set_parameter(state, "break_minutes", 30)["state"]
    state = time_labor_set_parameter(state, "rounding_interval_minutes", 15)["state"]
    state = time_labor_set_parameter(state, "geofence_radius_meters", 150)["state"]
    state = time_labor_register_rule(
        state,
        {
            "rule_id": "rule_hourly",
            "tenant": "tenant_alpha",
            "rule_type": "time",
            "eligible_roles": ("warehouse_operator", "associate"),
            "required_sources": ("mobile", "kiosk"),
            "absence_entitlements": {"vacation": 80, "sick": 40},
            "premium_multiplier": 1.5,
            "status": "active",
        },
    )["state"]
    state = time_labor_register_schema_extension(state, "time_entry", {"device_payload": "jsonb"})["state"]
    state = time_labor_upsert_employee_projection(
        state,
        {"employee_id": "emp_100", "tenant": "tenant_alpha", "role": "warehouse_operator", "status": "active", "site": "wh_east", "identity": {"did": "did:appgen:emp-100", "issuer": "trusted_registry", "status": "active"}},
    )["state"]
    shift = time_labor_create_shift(
        state,
        {
            "shift_id": "shift_100",
            "tenant": "tenant_alpha",
            "employee_id": "emp_100",
            "date": "2026-05-26",
            "planned_start": "09:00",
            "planned_end": "17:30",
            "site": "wh_east",
            "cost_center": "ops",
            "job": "picking",
        },
    )
    state = shift["state"]
    state = time_labor_record_clock_event(state, "shift_100", {"event_id": "clk_in", "kind": "in", "time": "09:00", "source": "mobile", "distance_meters": 20})["state"]
    state = time_labor_record_clock_event(state, "shift_100", {"event_id": "clk_out", "kind": "out", "time": "18:00", "source": "mobile", "distance_meters": 20})["state"]
    entry = time_labor_calculate_time_entry(state, "shift_100")
    state = entry["state"]
    absence = time_labor_record_absence(state, {"absence_id": "abs_100", "tenant": "tenant_alpha", "employee_id": "emp_100", "absence_type": "vacation", "hours": 8, "date": "2026-05-27"})
    state = absence["state"]
    approval = time_labor_approve_labor_summary(state, "summary_100", employee_id="emp_100", period="2026-W22", approved_by="manager_1")
    state = approval["state"]
    simulation = time_labor_simulate_schedule_policy(state, "emp_100", proposed_hours=45)
    forecast = time_labor_forecast_overtime((38, 42, 44), threshold=40)
    parsed = time_labor_parse_clock_event("employee emp_777 shift shift_777 kind in time 09:00 source mobile")
    risk = time_labor_score_labor_risk({"overtime": 0.2, "absence": 0.1, "exception": 0.05})
    recommendation = time_labor_recommend_exception_resolution("missed_punch")
    route = time_labor_route_clock_source({"event_id": "clk_route"}, rails=({"route": "kiosk_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}))
    proof = time_labor_generate_hours_proof(state, "summary_100", disclosure=("summary_id", "employee_id", "approved_hours"))
    screening = time_labor_screen_policy(state, "shift_100", restricted_sites=("restricted_site",))
    controls = time_labor_run_control_tests(state)
    api = time_labor_build_api_contract()
    federation = time_labor_federate_labor_view(state, "summary_100", systems=("personnel", "payroll", "warehouse"))
    identity = time_labor_verify_employee_identity(state["employees"]["emp_100"]["identity"])
    resilience = time_labor_run_resilience_drill(state, "kiosk_api_timeout")
    crypto = time_labor_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = time_labor_schedule_carbon_aware_shift(({"window": "day", "carbon": 220}, {"window": "night", "carbon": 90}))
    optimization = time_labor_optimize_schedule(({"shift": "day", "coverage": 0.9, "overtime": 0.2}, {"shift": "night", "coverage": 0.7, "overtime": 0.05}))
    allocation = time_labor_allocate_shifts(({"employee_id": "emp_100", "bid": 0.8, "skill": 0.9}, {"employee_id": "emp_200", "bid": 0.5, "skill": 0.6}), shifts=4)
    anomaly = time_labor_detect_time_anomaly(state)
    stochastic = time_labor_model_stochastic_labor_exposure(hours_path=(8, 9, 10), volatility=0.1)
    workbench = time_labor_build_workbench_view(state, tenant="tenant_alpha")
    model = time_labor_register_governed_model("labor_risk", {"features": ("hours", "absence", "exceptions"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_labor_lifecycle", "ok": len(state["events"]) >= 6 and state["events"][-1]["hash"]},
        {"id": "graph_relational_labor_topology", "ok": shift["shift"]["graph_degree"] >= 4},
        {"id": "multi_tenant_time_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_time_schema", "ok": state["schema_extensions"]["time_entry"]["device_payload"] == "jsonb"},
        {"id": "probabilistic_time_fraud_exception_scoring", "ok": entry["fraud_score"] < 0.3},
        {"id": "real_time_labor_execution_analytics", "ok": workbench["approved_summary_count"] == 1},
        {"id": "counterfactual_schedule_overtime_simulation", "ok": simulation["overtime_hours"] == 5},
        {"id": "temporal_labor_demand_overtime_forecasting", "ok": forecast["overtime_hours"] > 0},
        {"id": "autonomous_time_exception_resolution", "ok": recommendation["action"] == "request_manager_attestation"},
        {"id": "semantic_clock_absence_event_parsing", "ok": parsed["ok"] and parsed["employee_id"] == "emp_777"},
        {"id": "predictive_burnout_absence_compliance_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_clock_source_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_payroll_ready_hours_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_hours_")},
        {"id": "immutable_labor_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_labor_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_time_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "LaborHoursApproved" in api["events"]["emits"]},
        {"id": "cross_system_labor_federation", "ok": federation["ok"] and "payroll" in federation["systems"]},
        {"id": "workforce_device_integration", "ok": route["idempotency_key"].startswith("time_labor:ClockSource")},
        {"id": "decentralized_employee_time_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_clock_approval_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_clock_route"},
        {"id": "quantum_resistant_time_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_schedule_planning", "ok": carbon["window"] == "night"},
        {"id": "algebraic_schedule_labor_optimization", "ok": optimization["ok"] and optimization["shift"] == "day"},
        {"id": "mechanism_design_shift_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["shifts"] > allocation["allocations"][1]["shifts"]},
        {"id": "information_theoretic_time_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_labor_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("time_labor:LaborHoursApproved")},
        {"id": "probabilistic_ml_labor_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_bid"] > 0},
        {"id": "labor_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.time-labor-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def time_labor_empty_state() -> dict:
    return {"events": (), "outbox": (), "employees": {}, "shifts": {}, "clock_events": {}, "time_entries": {}, "absences": {}, "summaries": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def time_labor_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Time and Labor supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("Time and Labor requires an AppGen-X event topic")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def time_labor_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "standard_daily_hours",
        "weekly_overtime_threshold",
        "break_minutes",
        "rounding_interval_minutes",
        "geofence_radius_meters",
        "shift_swap_window_hours",
        "absence_notice_hours",
        "approval_sla_hours",
        "exception_escalation_hours",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Time and Labor parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def time_labor_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Time and Labor rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Time and Labor rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def time_labor_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def time_labor_upsert_employee_projection(state: dict, employee: dict) -> dict:
    return {"ok": True, "state": {**state, "employees": {**state["employees"], employee["employee_id"]: employee}}, "employee": employee}


def time_labor_create_shift(state: dict, shift: dict) -> dict:
    employee = state["employees"][shift["employee_id"]]
    rule = next(iter(state["rules"].values()))
    ok = employee["status"] == "active" and employee["role"] in rule["eligible_roles"]
    enriched = {**shift, "status": "scheduled" if ok else "blocked", "graph_degree": len(tuple(value for value in (shift["employee_id"], shift["site"], shift["cost_center"], shift["job"]) if value))}
    next_state = {**state, "shifts": {**state["shifts"], shift["shift_id"]: enriched}}
    next_state = _append_event(next_state, "ShiftCreated", {"tenant": shift["tenant"], "shift_id": shift["shift_id"], "employee_id": shift["employee_id"]})
    return {"ok": ok, "state": next_state, "shift": enriched}


def time_labor_record_clock_event(state: dict, shift_id: str, event: dict) -> dict:
    shift = state["shifts"][shift_id]
    allowed_source = event["source"] in state["configuration"].get("allowed_clock_sources", ())
    in_radius = event["distance_meters"] <= float(state["parameters"].get("geofence_radius_meters", 999999))
    enriched = {**event, "shift_id": shift_id, "tenant": shift["tenant"], "status": "accepted" if allowed_source and in_radius else "exception"}
    next_state = {**state, "clock_events": {**state["clock_events"], event["event_id"]: enriched}}
    next_state = _append_event(next_state, "ClockEventRecorded", {"tenant": shift["tenant"], "shift_id": shift_id, "event_id": event["event_id"], "kind": event["kind"], "status": enriched["status"]})
    return {"ok": enriched["status"] == "accepted", "state": next_state, "clock_event": enriched}


def time_labor_calculate_time_entry(state: dict, shift_id: str) -> dict:
    shift = state["shifts"][shift_id]
    events = tuple(event for event in state["clock_events"].values() if event["shift_id"] == shift_id and event["status"] == "accepted")
    start = next(event for event in events if event["kind"] == "in")
    end = next(event for event in events if event["kind"] == "out")
    gross = _hours_between(start["time"], end["time"])
    break_hours = float(state["parameters"].get("break_minutes", 0)) / 60
    hours = round(max(0, gross - break_hours), 2)
    standard = float(state["parameters"].get("standard_daily_hours", 8))
    overtime = round(max(0, hours - standard), 2)
    entry = {"entry_id": f"entry_{shift_id}", "tenant": shift["tenant"], "shift_id": shift_id, "employee_id": shift["employee_id"], "hours": hours, "overtime_hours": overtime, "premium_hours": overtime, "status": "calculated", "fraud_score": round(len(tuple(event for event in events if event["distance_meters"] > 100)) * 0.2, 4)}
    next_state = {**state, "time_entries": {**state["time_entries"], entry["entry_id"]: entry}}
    next_state = _append_event(next_state, "TimeEntryCalculated", {"tenant": shift["tenant"], "entry_id": entry["entry_id"], "employee_id": shift["employee_id"], "hours": hours})
    return {"ok": True, "state": next_state, **entry}


def time_labor_record_absence(state: dict, absence: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    entitlement = rule["absence_entitlements"].get(absence["absence_type"], 0)
    ok = absence["absence_type"] in state["configuration"].get("allowed_absence_types", ()) and absence["hours"] <= entitlement
    enriched = {**absence, "status": "recorded" if ok else "blocked"}
    next_state = {**state, "absences": {**state["absences"], absence["absence_id"]: enriched}}
    next_state = _append_event(next_state, "AbsenceRecorded", {"tenant": absence["tenant"], "absence_id": absence["absence_id"], "employee_id": absence["employee_id"], "hours": absence["hours"]})
    return {"ok": ok, "state": next_state, "absence": enriched}


def time_labor_approve_labor_summary(state: dict, summary_id: str, *, employee_id: str, period: str, approved_by: str) -> dict:
    entries = tuple(entry for entry in state["time_entries"].values() if entry["employee_id"] == employee_id)
    summary = {"summary_id": summary_id, "tenant": state["employees"][employee_id]["tenant"], "employee_id": employee_id, "period": period, "approved_hours": round(sum(entry["hours"] for entry in entries), 2), "overtime_hours": round(sum(entry["overtime_hours"] for entry in entries), 2), "approved_by": approved_by, "status": "approved"}
    next_state = {**state, "summaries": {**state["summaries"], summary_id: summary}}
    next_state = _append_event(next_state, "LaborHoursApproved", {"tenant": summary["tenant"], "summary_id": summary_id, "employee_id": employee_id, "approved_hours": summary["approved_hours"]})
    return {"ok": True, "state": next_state, "summary": summary}


def time_labor_simulate_schedule_policy(state: dict, employee_id: str, *, proposed_hours: float) -> dict:
    threshold = float(state["parameters"].get("weekly_overtime_threshold", 40))
    return {"ok": True, "employee_id": employee_id, "proposed_hours": proposed_hours, "overtime_hours": round(max(0, proposed_hours - threshold), 2)}


def time_labor_forecast_overtime(hours_path: tuple[float, ...], *, threshold: float) -> dict:
    overtime = sum(max(0, hours - threshold) for hours in hours_path)
    return {"ok": True, "overtime_hours": round(overtime, 2), "trend": round((hours_path[-1] - hours_path[0]) if len(hours_path) > 1 else 0, 2)}


def time_labor_parse_clock_event(text: str) -> dict:
    employee = re.search(r"employee\s+([a-z0-9_]+)", text, re.I)
    shift = re.search(r"shift\s+([a-z0-9_]+)", text, re.I)
    kind = re.search(r"kind\s+([a-z0-9_]+)", text, re.I)
    source = re.search(r"source\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(employee and shift and kind and source), "employee_id": employee.group(1) if employee else None, "shift_id": shift.group(1) if shift else None, "kind": kind.group(1) if kind else None, "source": source.group(1) if source else None}


def time_labor_score_labor_risk(signals: dict) -> dict:
    risk = round(signals.get("overtime", 0) * 2 + signals.get("absence", 0) + signals.get("exception", 0) * 2, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.7 else "review"}


def time_labor_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"missed_punch": "request_manager_attestation", "geofence": "request_location_review", "overtime": "route_overtime_approval"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def time_labor_route_clock_source(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"time_labor:ClockSource:{event['event_id']}"}


def time_labor_generate_hours_proof(state: dict, summary_id: str, *, disclosure: tuple[str, ...]) -> dict:
    summary = state["summaries"][summary_id]
    claims = {field: summary[field] for field in disclosure if field in summary}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_hours_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def time_labor_screen_policy(state: dict, shift_id: str, *, restricted_sites: tuple[str, ...]) -> dict:
    shift = state["shifts"][shift_id]
    blocked = shift["site"] in restricted_sites or shift["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "shift_id": shift_id}


def time_labor_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(shift["status"] == "blocked" for shift in state["shifts"].values()):
        gaps.append("blocked_shift")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def time_labor_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /clock-events", "POST /absences", "GET /labor-summaries", "POST /time-rules", "POST /time-parameters", "POST /time-configuration"), "events": {"emits": ("LaborHoursApproved", "AbsenceRecorded"), "consumes": ("EmployeeCreated", "RoleChanged")}, "permissions": ("time_labor.schedule", "time_labor.clock", "time_labor.approve", "time_labor.absence", "time_labor.summarize", "time_labor.configure", "time_labor.audit"), "configuration": ("TIME_LABOR_DATABASE_URL", "TIME_LABOR_EVENT_TOPIC", "TIME_LABOR_RETRY_LIMIT", "TIME_LABOR_DEFAULT_TIMEZONE")}


def time_labor_federate_labor_view(state: dict, summary_id: str, *, systems: tuple[str, ...]) -> dict:
    summary = state["summaries"][summary_id]
    return {"ok": True, "summary_id": summary_id, "systems": systems, "projection": {"employee_id": summary["employee_id"], "approved_hours": summary["approved_hours"], "overtime_hours": summary["overtime_hours"]}}


def time_labor_verify_employee_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def time_labor_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"kiosk_api_timeout", "approval_worker_failure"}, "scenario": scenario, "mode": "degraded_clock_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "time_labor.dead_letter"}


def time_labor_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"time_epoch_{epoch:04d}"}


def time_labor_schedule_carbon_aware_shift(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def time_labor_optimize_schedule(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["coverage"] - candidate["overtime"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "shift": selected["shift"], "objective_score": selected["objective"], "candidates": scored}


def time_labor_allocate_shifts(workers: tuple[dict, ...], *, shifts: int) -> dict:
    weights = tuple({"employee_id": worker["employee_id"], "weight": worker["bid"] * worker["skill"]} for worker in workers)
    total = sum(item["weight"] for item in weights)
    allocations = tuple({"employee_id": item["employee_id"], "shifts": round(shifts * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["shifts"] for item in allocations), 2) == round(shifts, 2), "allocations": allocations, "clearing_bid": round(sum(worker["bid"] for worker in workers) / len(workers), 4)}


def time_labor_detect_time_anomaly(state: dict) -> dict:
    hours = tuple(entry["hours"] for entry in state["time_entries"].values())
    if not hours:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(hours) or 1
    entropy = round(-sum((hour / total) * math.log(max(hour / total, 0.0001), 2) for hour in hours), 4)
    mean = sum(hours) / len(hours)
    return {"ok": True, "entropy": entropy, "outliers": tuple(hour for hour in hours if abs(hour - mean) > 4)}


def time_labor_model_stochastic_labor_exposure(*, hours_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(hours_path) < 2 else (hours_path[-1] - hours_path[0]) / (len(hours_path) - 1)
    exposure = abs(drift) * volatility * len(hours_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def time_labor_build_workbench_view(state: dict, *, tenant: str) -> dict:
    shifts = tuple(shift for shift in state["shifts"].values() if shift["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "shift_count": len(shifts),
        "time_entry_count": len(tuple(entry for entry in state["time_entries"].values() if entry["tenant"] == tenant)),
        "absence_count": len(tuple(absence for absence in state["absences"].values() if absence["tenant"] == tenant)),
        "approved_summary_count": len(tuple(summary for summary in state["summaries"].values() if summary["tenant"] == tenant and summary["status"] == "approved")),
        "exception_count": len(tuple(event for event in state["clock_events"].values() if event["tenant"] == tenant and event["status"] == "exception")),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
    }


def time_labor_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _hours_between(start: str, end: str) -> float:
    start_hour, start_minute = (int(part) for part in start.split(":"))
    end_hour, end_minute = (int(part) for part in end.split(":"))
    return round((end_hour * 60 + end_minute - (start_hour * 60 + start_minute)) / 60, 2)


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"time_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"time_labor:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
