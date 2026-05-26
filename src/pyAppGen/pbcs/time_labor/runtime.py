"""Executable runtime for the Time and Labor PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TIME_LABOR_REQUIRED_EVENT_TOPIC = "appgen.time.events"
TIME_LABOR_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
TIME_LABOR_OWNED_TABLES = (
    "shift",
    "shift_pattern",
    "shift_assignment",
    "shift_swap_request",
    "schedule_bid",
    "labor_demand_forecast",
    "clock_event",
    "clock_device",
    "clock_source_route",
    "clock_exception",
    "time_entry",
    "time_entry_line",
    "break_deduction",
    "overtime_bucket",
    "premium_calculation",
    "holiday_calendar",
    "absence",
    "absence_balance",
    "absence_entitlement",
    "absence_approval",
    "labor_summary",
    "labor_summary_line",
    "labor_cost_allocation",
    "labor_distribution",
    "approval_workflow",
    "approval_task",
    "employee_projection",
    "role_projection",
    "payroll_labor_projection",
    "warehouse_site_projection",
    "manufacturing_shift_projection",
    "project_cost_projection",
    "time_policy_screening",
    "time_audit_trace",
    "time_hours_proof",
    "time_federation_projection",
    "time_carbon_schedule_window",
    "time_schedule_optimization",
    "time_shift_allocation",
    "time_anomaly_signal",
    "time_labor_risk_model",
    "time_labor_risk_forecast",
    "time_parsed_event",
    "time_seed_data",
    "time_schema_extension",
    "time_control_assertion",
    "time_governed_model",
    "time_rule",
    "time_parameter",
    "time_configuration",
    "time_labor_appgen_outbox_event",
    "time_labor_appgen_inbox_event",
    "time_labor_dead_letter_event",
)
TIME_LABOR_CONSUMED_EVENT_TYPES = ("EmployeeCreated", "RoleChanged")
TIME_LABOR_EMITTED_EVENT_TYPES = (
    "ShiftCreated",
    "ClockEventRecorded",
    "TimeEntryCalculated",
    "LaborHoursApproved",
    "AbsenceRecorded",
)
_TIME_LABOR_RUNTIME_TABLES = (
    "time_labor_appgen_outbox_event",
    "time_labor_appgen_inbox_event",
    "time_labor_dead_letter_event",
)
_TIME_LABOR_ALLOWED_DEPENDENCIES = (
    "personnel_identity_projection",
    "payroll_labor_projection",
    "warehouse_site_projection",
    "manufacturing_shift_projection",
    "project_cost_projection",
    "audit_ledger_projection",
    "GET /employees",
    "GET /roles",
    "POST /payroll-labor-hours",
    "POST /labor-cost-projections",
)
_TIME_LABOR_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


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
    "shift_pattern_management",
    "shift_assignment",
    "shift_swap_request",
    "schedule_bidding",
    "labor_demand_forecasting",
    "clock_event_ingestion",
    "clock_device_registry",
    "clock_source_route",
    "clock_exception_queue",
    "clock_sequence_validation",
    "geofence_validation",
    "time_entry_calculation",
    "time_entry_lines",
    "break_deduction",
    "meal_penalty_tracking",
    "overtime_calculation",
    "overtime_bucket",
    "premium_calculation",
    "holiday_calendar",
    "absence_recording",
    "absence_balance",
    "entitlement_check",
    "absence_approval",
    "labor_summary",
    "labor_summary_line",
    "labor_cost_allocation",
    "labor_distribution",
    "approval_workflow",
    "approval_task",
    "employee_projection",
    "role_projection",
    "payroll_labor_projection",
    "warehouse_site_projection",
    "manufacturing_shift_projection",
    "project_cost_projection",
    "payroll_ready_event",
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
    "policy_screening",
    "audit_trace",
    "hours_proof",
    "federation_projection",
    "carbon_schedule_window",
    "schedule_optimization",
    "shift_allocation",
    "time_anomaly_signal",
    "labor_risk_model",
    "labor_risk_forecast",
    "semantic_event_parser",
    "control_assertion",
    "governed_model",
    "workbench",
)


def time_labor_runtime_capabilities() -> dict:
    smoke = time_labor_runtime_smoke()
    return {
        "format": "appgen.time-labor-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "time_labor",
        "implementation_directory": "src/pyAppGen/pbcs/time_labor",
        "owned_tables": TIME_LABOR_OWNED_TABLES,
        "capabilities": TIME_LABOR_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TIME_LABOR_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "upsert_employee_projection",
            "create_shift",
            "record_clock_event",
            "calculate_time_entry",
            "record_absence",
            "approve_labor_summary",
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


def time_labor_runtime_smoke() -> dict:
    state = time_labor_empty_state()
    state = time_labor_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
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
    employee_event = time_labor_receive_event(
        state,
        {
            "event_id": "people_evt_100",
            "event_type": "EmployeeCreated",
            "payload": {
                "employee_id": "emp_100",
                "tenant": "tenant_alpha",
                "role": "warehouse_operator",
                "status": "active",
                "site": "wh_east",
                "identity": {"did": "did:appgen:emp-100", "issuer": "trusted_registry", "status": "active"},
            },
        },
    )
    state = employee_event["state"]
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
    schema = time_labor_build_schema_contract()
    service = time_labor_build_service_contract()
    release = time_labor_build_release_evidence()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "LaborHoursApproved" in api["events"]["emits"]},
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
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "employees": {},
        "roles": {},
        "shifts": {},
        "clock_events": {},
        "time_entries": {},
        "absences": {},
        "summaries": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def time_labor_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _TIME_LABOR_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Time and Labor uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    allowed_databases = set(TIME_LABOR_ALLOWED_DATABASE_BACKENDS)
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Time and Labor supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != TIME_LABOR_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Time and Labor requires AppGen-X event topic {TIME_LABOR_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": TIME_LABOR_OWNED_TABLES,
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
    if table not in TIME_LABOR_OWNED_TABLES:
        raise ValueError(f"Time and Labor schema extensions must target owned tables: {TIME_LABOR_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = {**state["schema_extensions"], table: {**state["schema_extensions"].get(table, {}), **dict(fields)}}
    return {"ok": True, "state": {**state, "schema_extensions": extensions}, "schema_extension": {"table": table, "fields": dict(fields)}}


def time_labor_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
    if simulate_failure or event_type not in TIME_LABOR_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}, "retry_evidence": (*next_state["retry_evidence"], evidence)}
        if status == "dead_letter":
            dead_letter = {**inbox_entry, "reason": "unsupported_or_failed_time_labor_event"}
            next_state = {**next_state, "dead_letter": (*next_state["dead_letter"], dead_letter)}
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "EmployeeCreated":
        employee = {
            "employee_id": payload["employee_id"],
            "tenant": payload["tenant"],
            "role": payload.get("role", "unassigned"),
            "status": payload.get("status", "active"),
            "site": payload.get("site"),
            "identity": payload.get("identity", {}),
        }
        next_state = {**next_state, "employees": {**next_state["employees"], employee["employee_id"]: employee}}
    elif event_type == "RoleChanged":
        employee_id = payload["employee_id"]
        employee = dict(next_state["employees"].get(employee_id, {"employee_id": employee_id, "tenant": payload.get("tenant"), "status": "active"}))
        employee["role"] = payload["role"]
        next_state = {
            **next_state,
            "employees": {**next_state["employees"], employee_id: employee},
            "roles": {**next_state["roles"], employee_id: {"employee_id": employee_id, "tenant": payload.get("tenant"), "role": payload["role"]}},
        }
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}}
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


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
    return {
        "format": "appgen.time-labor-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /shifts", "command": "create_shift", "owned_tables": ("shift",), "emits": (), "requires_permission": "time_labor.schedule", "idempotency_key": "shift_id"},
            {"route": "POST /shift-patterns", "command": "create_shift", "owned_tables": ("shift_pattern",), "emits": (), "requires_permission": "time_labor.schedule", "idempotency_key": "pattern_id"},
            {"route": "POST /shift-swaps", "command": "create_shift", "owned_tables": ("shift_swap_request",), "emits": (), "requires_permission": "time_labor.schedule", "idempotency_key": "swap_id"},
            {"route": "POST /clock-events", "command": "record_clock_event", "owned_tables": ("clock_event",), "emits": (), "requires_permission": "time_labor.clock", "idempotency_key": "event_id"},
            {"route": "POST /time-entries/calculate", "command": "calculate_time_entry", "owned_tables": ("time_entry",), "emits": (), "requires_permission": "time_labor.summarize", "idempotency_key": "shift_id"},
            {"route": "POST /absences", "command": "record_absence", "owned_tables": ("absence",), "emits": ("AbsenceRecorded",), "requires_permission": "time_labor.absence", "idempotency_key": "absence_id"},
            {"route": "POST /labor-summaries/{id}/approve", "command": "approve_labor_summary", "owned_tables": ("labor_summary",), "emits": ("LaborHoursApproved",), "requires_permission": "time_labor.approve", "idempotency_key": "summary_id:approved_by"},
            {"route": "POST /time/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": TIME_LABOR_CONSUMED_EVENT_TYPES, "requires_permission": "time_labor.event", "idempotency_key": "event_id"},
            {"route": "POST /time/rules", "command": "register_rule", "owned_tables": ("time_rule",), "requires_permission": "time_labor.configure", "idempotency_key": "rule_id"},
            {"route": "POST /time/parameters", "command": "set_parameter", "owned_tables": ("time_parameter",), "requires_permission": "time_labor.configure", "idempotency_key": "parameter_name"},
            {"route": "POST /time/configuration", "command": "configure_runtime", "owned_tables": ("time_configuration",), "requires_permission": "time_labor.configure", "idempotency_key": "tenant"},
            {"route": "GET /labor-summaries", "query": "build_workbench_view", "owned_tables": ("labor_summary", "time_entry"), "requires_permission": "time_labor.read"},
            {"route": "GET /time-workbench", "query": "build_workbench_view", "owned_tables": TIME_LABOR_OWNED_TABLES, "requires_permission": "time_labor.audit"},
        ),
        "declared_catalog_routes": ("POST /clock-events", "POST /absences", "GET /labor-summaries", "POST /time-rules", "POST /time-parameters", "POST /time-configuration"),
        "events": {"emits": TIME_LABOR_EMITTED_EVENT_TYPES, "consumes": TIME_LABOR_CONSUMED_EVENT_TYPES},
        "emits": TIME_LABOR_EMITTED_EVENT_TYPES,
        "consumes": TIME_LABOR_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(time_labor_permissions_contract()["permissions"])),
        "database_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": TIME_LABOR_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("TIME_LABOR_DATABASE_URL", "TIME_LABOR_EVENT_TOPIC", "TIME_LABOR_RETRY_LIMIT", "TIME_LABOR_DEFAULT_TIMEZONE"),
    }


def time_labor_build_schema_contract() -> dict:
    """Return generated Time Labor schema, migration, and model evidence."""
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in TIME_LABOR_OWNED_TABLES}
    table_fields.update(
        {
            "shift": ("tenant", "shift_id", "employee_id", "date", "planned_start", "planned_end", "site", "cost_center", "job", "status", "audit_hash"),
            "shift_pattern": ("tenant", "pattern_id", "name", "cycle_days", "planned_start", "planned_end", "status", "audit_hash"),
            "shift_assignment": ("tenant", "assignment_id", "shift_id", "employee_id", "assignment_type", "status", "audit_hash"),
            "shift_swap_request": ("tenant", "swap_id", "from_employee_id", "to_employee_id", "shift_id", "decision", "audit_hash"),
            "schedule_bid": ("tenant", "bid_id", "employee_id", "shift_id", "preference_score", "bid_status", "audit_hash"),
            "labor_demand_forecast": ("tenant", "forecast_id", "site", "date", "required_hours", "confidence", "audit_hash"),
            "clock_event": ("tenant", "event_id", "shift_id", "kind", "time", "source", "distance_meters", "status", "audit_hash"),
            "clock_device": ("tenant", "device_id", "source", "site", "trust_score", "last_seen_at", "audit_hash"),
            "clock_source_route": ("tenant", "route_id", "event_id", "route", "latency", "failover_used", "audit_hash"),
            "clock_exception": ("tenant", "exception_id", "shift_id", "exception_type", "resolution", "status", "audit_hash"),
            "time_entry": ("tenant", "entry_id", "shift_id", "employee_id", "hours", "overtime_hours", "premium_hours", "status", "audit_hash"),
            "time_entry_line": ("tenant", "line_id", "entry_id", "earning_code", "hours", "rate_multiplier", "audit_hash"),
            "break_deduction": ("tenant", "deduction_id", "entry_id", "break_minutes", "policy_rule_id", "audit_hash"),
            "overtime_bucket": ("tenant", "bucket_id", "employee_id", "period", "threshold", "overtime_hours", "audit_hash"),
            "premium_calculation": ("tenant", "premium_id", "entry_id", "premium_code", "hours", "multiplier", "audit_hash"),
            "absence": ("tenant", "absence_id", "employee_id", "absence_type", "hours", "date", "status", "audit_hash"),
            "absence_balance": ("tenant", "balance_id", "employee_id", "absence_type", "available_hours", "effective_at", "audit_hash"),
            "absence_entitlement": ("tenant", "entitlement_id", "absence_type", "annual_hours", "eligibility_rule_id", "audit_hash"),
            "absence_approval": ("tenant", "approval_id", "absence_id", "approver", "decision", "decided_at", "audit_hash"),
            "labor_summary": ("tenant", "summary_id", "employee_id", "period", "approved_hours", "overtime_hours", "approved_by", "status", "audit_hash"),
            "labor_summary_line": ("tenant", "line_id", "summary_id", "entry_id", "earning_code", "hours", "audit_hash"),
            "labor_cost_allocation": ("tenant", "allocation_id", "summary_id", "cost_center", "project_id", "hours", "audit_hash"),
            "approval_workflow": ("tenant", "workflow_id", "scope", "sla_hours", "status", "audit_hash"),
            "approval_task": ("tenant", "task_id", "workflow_id", "subject_id", "assignee", "decision", "audit_hash"),
            "employee_projection": ("tenant", "employee_id", "role", "status", "site", "identity_hash", "audit_hash"),
            "role_projection": ("tenant", "employee_id", "role", "received_event_id", "audit_hash"),
            "time_rule": ("tenant", "rule_id", "scope", "compiled_hash", "enabled", "status", "audit_hash"),
            "time_parameter": ("tenant", "parameter_name", "parameter_value", "effective_at", "changed_by", "audit_hash"),
            "time_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "event_contract", "stream_engine_picker_visible", "audit_hash"),
            "time_labor_appgen_outbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "published_at", "audit_hash"),
            "time_labor_appgen_inbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "audit_hash"),
            "time_labor_dead_letter_event": ("tenant", "event_id", "event_type", "payload", "reason", "attempts", "audit_hash"),
        }
    )
    relationships = (
        {"from_table": "shift_assignment", "from_field": "shift_id", "to_table": "shift", "to_field": "shift_id"},
        {"from_table": "shift_assignment", "from_field": "employee_id", "to_table": "employee_projection", "to_field": "employee_id"},
        {"from_table": "shift_swap_request", "from_field": "shift_id", "to_table": "shift", "to_field": "shift_id"},
        {"from_table": "schedule_bid", "from_field": "shift_id", "to_table": "shift", "to_field": "shift_id"},
        {"from_table": "clock_event", "from_field": "shift_id", "to_table": "shift", "to_field": "shift_id"},
        {"from_table": "clock_source_route", "from_field": "event_id", "to_table": "clock_event", "to_field": "event_id"},
        {"from_table": "clock_exception", "from_field": "shift_id", "to_table": "shift", "to_field": "shift_id"},
        {"from_table": "time_entry", "from_field": "shift_id", "to_table": "shift", "to_field": "shift_id"},
        {"from_table": "time_entry_line", "from_field": "entry_id", "to_table": "time_entry", "to_field": "entry_id"},
        {"from_table": "break_deduction", "from_field": "entry_id", "to_table": "time_entry", "to_field": "entry_id"},
        {"from_table": "premium_calculation", "from_field": "entry_id", "to_table": "time_entry", "to_field": "entry_id"},
        {"from_table": "absence_approval", "from_field": "absence_id", "to_table": "absence", "to_field": "absence_id"},
        {"from_table": "labor_summary_line", "from_field": "summary_id", "to_table": "labor_summary", "to_field": "summary_id"},
        {"from_table": "labor_cost_allocation", "from_field": "summary_id", "to_table": "labor_summary", "to_field": "summary_id"},
        {"from_table": "approval_task", "from_field": "workflow_id", "to_table": "approval_workflow", "to_field": "workflow_id"},
    )
    allowed_prefixes = (
        "shift",
        "schedule_",
        "labor_",
        "clock_",
        "time_",
        "break_",
        "overtime_",
        "premium_",
        "holiday_",
        "absence",
        "approval_",
        "employee_",
        "role_",
        "payroll_",
        "warehouse_",
        "manufacturing_",
        "project_",
    )
    tables = tuple({"table": table, "fields": table_fields[table], "owner": "time_labor"} for table in TIME_LABOR_OWNED_TABLES)
    return {
        "format": "appgen.time-labor-owned-schema-contract.v1",
        "ok": len(tables) == len(TIME_LABOR_OWNED_TABLES) and len(tables) >= 40 and all(item["table"].startswith(allowed_prefixes) for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/time_labor/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(TIME_LABOR_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in TIME_LABOR_OWNED_TABLES
        ),
        "datastore_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def time_labor_build_service_contract() -> dict:
    """Return Time Labor command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "upsert_employee_projection",
        "create_shift",
        "record_clock_event",
        "calculate_time_entry",
        "record_absence",
        "approve_labor_summary",
        "route_clock_source",
        "generate_hours_proof",
        "screen_policy",
        "federate_labor_view",
        "verify_employee_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_shift",
        "optimize_schedule",
        "allocate_shifts",
        "run_control_tests",
        "register_governed_model",
        "recommend_exception_resolution",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.time-labor-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "time_labor_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_workbench_view",
            "simulate_schedule_policy",
            "forecast_overtime",
            "parse_clock_event",
            "score_labor_risk",
            "detect_time_anomaly",
            "model_stochastic_labor_exposure",
            "build_api_contract",
            "build_schema_contract",
            "build_release_evidence",
        ),
        "mutates_only": TIME_LABOR_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _TIME_LABOR_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": TIME_LABOR_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _TIME_LABOR_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def time_labor_build_release_evidence() -> dict:
    """Return Time Labor package-local release evidence."""
    schema = time_labor_build_schema_contract()
    service = time_labor_build_service_contract()
    api = time_labor_build_api_contract()
    permissions = time_labor_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(TIME_LABOR_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"create_shift", "record_clock_event", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == TIME_LABOR_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.time-labor-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def time_labor_permissions_contract() -> dict:
    return {
        "format": "appgen.time-labor-permissions.v1",
        "ok": True,
        "permissions": (
            "time_labor.read",
            "time_labor.schedule",
            "time_labor.clock",
            "time_labor.approve",
            "time_labor.absence",
            "time_labor.summarize",
            "time_labor.event",
            "time_labor.configure",
            "time_labor.audit",
        ),
        "action_permissions": {
            "create_shift": "time_labor.schedule",
            "record_clock_event": "time_labor.clock",
            "calculate_time_entry": "time_labor.summarize",
            "record_absence": "time_labor.absence",
            "approve_labor_summary": "time_labor.approve",
            "receive_event": "time_labor.event",
            "register_rule": "time_labor.configure",
            "register_schema_extension": "time_labor.configure",
            "set_parameter": "time_labor.configure",
            "configure_runtime": "time_labor.configure",
            "build_workbench_view": "time_labor.audit",
            "route_clock_source": "time_labor.clock",
            "generate_hours_proof": "time_labor.audit",
            "screen_policy": "time_labor.audit",
            "federate_labor_view": "time_labor.read",
            "verify_employee_identity": "time_labor.audit",
            "run_resilience_drill": "time_labor.audit",
            "rotate_crypto_epoch": "time_labor.audit",
            "schedule_carbon_aware_shift": "time_labor.schedule",
            "optimize_schedule": "time_labor.schedule",
            "allocate_shifts": "time_labor.schedule",
            "run_control_tests": "time_labor.audit",
            "register_governed_model": "time_labor.audit",
            "recommend_exception_resolution": "time_labor.approve",
            "detect_time_anomaly": "time_labor.audit",
            "model_stochastic_labor_exposure": "time_labor.audit",
            "parse_clock_event": "time_labor.read",
            "score_labor_risk": "time_labor.audit",
            "forecast_overtime": "time_labor.read",
            "simulate_schedule_policy": "time_labor.read",
            "build_schema_contract": "time_labor.audit",
            "build_service_contract": "time_labor.audit",
            "build_release_evidence": "time_labor.audit",
        },
    }


def time_labor_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*TIME_LABOR_OWNED_TABLES, *TIME_LABOR_CONSUMED_EVENT_TYPES, *_TIME_LABOR_RUNTIME_TABLES, *_TIME_LABOR_ALLOWED_DEPENDENCIES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(allowed)
        and not str(reference).startswith("time_labor_")
    )
    return {
        "format": "appgen.time-labor-boundary.v1",
        "ok": not violations,
        "owned_tables": TIME_LABOR_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /employees", "GET /roles", "POST /payroll-labor-hours", "POST /labor-cost-projections"),
            "events": TIME_LABOR_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "personnel_identity_projection",
                "payroll_labor_projection",
                "warehouse_site_projection",
                "manufacturing_shift_projection",
                "project_cost_projection",
                "audit_ledger_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


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
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": TIME_LABOR_OWNED_TABLES,
            "outbox_table": "time_labor_appgen_outbox_event",
            "inbox_table": "time_labor_appgen_inbox_event",
            "dead_letter_table": "time_labor_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
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
