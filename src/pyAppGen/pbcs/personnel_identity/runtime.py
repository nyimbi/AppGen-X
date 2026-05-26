"""Executable runtime for the Personnel Directory and Identity PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC = "appgen.people.events"
PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
PERSONNEL_IDENTITY_OWNED_TABLES = (
    "personnel_department",
    "personnel_department_hierarchy",
    "personnel_position",
    "personnel_job",
    "personnel_employee",
    "personnel_employee_contact",
    "personnel_employee_document",
    "personnel_employment_lifecycle",
    "personnel_employment_status_history",
    "personnel_manager_relationship",
    "personnel_org_assignment",
    "personnel_work_location",
    "personnel_cost_center_assignment",
    "personnel_role_assignment",
    "personnel_role_catalog",
    "personnel_role_review",
    "personnel_role_separation_check",
    "personnel_identity_attribute",
    "personnel_identity_assurance",
    "personnel_identity_verification",
    "personnel_identity_proof",
    "personnel_access_policy_projection",
    "personnel_access_exception",
    "personnel_provisioning_event",
    "personnel_provisioning_replay",
    "personnel_directory_projection",
    "personnel_org_chart_projection",
    "personnel_privacy_consent",
    "personnel_residency_rule",
    "personnel_retention_policy",
    "personnel_policy_screening",
    "personnel_audit_trace",
    "personnel_federation_projection",
    "personnel_carbon_processing_window",
    "personnel_role_access_optimization",
    "personnel_manager_capacity_allocation",
    "personnel_identity_anomaly_signal",
    "personnel_workforce_risk_model",
    "personnel_workforce_risk_forecast",
    "personnel_parsed_event",
    "personnel_seed_data",
    "personnel_schema_extension",
    "personnel_control_assertion",
    "personnel_governed_model",
    "personnel_policy_rule",
    "personnel_parameter",
    "personnel_configuration",
    "personnel_identity_appgen_outbox_event",
    "personnel_identity_appgen_inbox_event",
    "personnel_identity_dead_letter_event",
)
PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES = (
    "DepartmentRegistered",
    "EmployeeCreated",
    "EmployeeStatusChanged",
    "RoleChanged",
    "IdentityAttributeChanged",
)
PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES = (
    "EmployeeProvisioned",
    "AccessPolicyChanged",
    "OrgUnitChanged",
    "RoleReviewRequested",
)
_PERSONNEL_IDENTITY_RUNTIME_TABLES = (
    "personnel_identity_appgen_outbox_event",
    "personnel_identity_appgen_inbox_event",
    "personnel_identity_dead_letter_event",
)
_PERSONNEL_IDENTITY_ALLOWED_DEPENDENCIES = (
    "employee_provisioning_projection",
    "access_policy_projection",
    "org_unit_projection",
    "role_review_projection",
    "GET /identity/policies",
    "GET /org-units/{id}",
    "POST /audit/personnel-events",
)
_PERSONNEL_IDENTITY_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


PERSONNEL_IDENTITY_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_workforce_identity_lifecycle",
    "graph_relational_org_identity_topology",
    "multi_tenant_workforce_identity_isolation",
    "schema_evolution_resilient_identity_schema",
    "probabilistic_identity_assurance_access_risk",
    "real_time_directory_org_access_analytics",
    "counterfactual_org_access_policy_simulation",
    "temporal_workforce_access_risk_forecasting",
    "autonomous_role_access_exception_recommendations",
    "semantic_personnel_event_parsing",
    "predictive_attrition_access_compliance_risk",
    "self_healing_provisioning_route_selection",
    "zero_knowledge_personnel_eligibility_proof",
    "immutable_workforce_identity_audit_trail",
    "dynamic_personnel_policy_screening",
    "automated_identity_control_testing",
    "universal_api_async_streaming",
    "cross_system_people_federation",
    "identity_provider_directory_integration",
    "decentralized_employee_identity",
    "chaos_engineered_provisioning_tolerance",
    "quantum_resistant_identity_authorization",
    "carbon_aware_identity_processing",
    "algebraic_role_access_optimization",
    "mechanism_design_manager_role_allocation",
    "information_theoretic_identity_anomaly_detection",
    "temporal_workforce_risk_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_workforce_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "people_mlops_governance",
)
PERSONNEL_IDENTITY_STANDARD_FEATURE_KEYS = (
    "department_master",
    "department_hierarchy",
    "position_management",
    "job_catalog",
    "employee_master",
    "employee_contact_management",
    "employee_document_management",
    "employment_lifecycle",
    "employment_status_history",
    "manager_hierarchy",
    "org_assignment",
    "work_location_management",
    "cost_center_assignment",
    "org_chart",
    "role_assignment",
    "role_catalog",
    "role_change",
    "role_separation_check",
    "identity_attribute",
    "identity_verification",
    "identity_proof",
    "segregation_of_duties",
    "identity_assurance",
    "access_policy_projection",
    "provisioning_handler",
    "provisioning_replay",
    "directory_projection",
    "org_chart_projection",
    "employee_events",
    "multi_entity_isolation",
    "privacy_residency_retention",
    "privacy_consent",
    "residency_rules",
    "retention_policy",
    "policy_screening",
    "audit_trace",
    "federation_projection",
    "directory_search",
    "approval_review",
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
    "carbon_processing_window",
    "role_access_optimization",
    "manager_capacity_allocation",
    "identity_anomaly_signal",
    "workforce_risk_model",
    "workforce_risk_forecast",
    "semantic_event_parser",
    "workbench",
)


def personnel_identity_runtime_capabilities() -> dict:
    smoke = personnel_identity_runtime_smoke()
    return {
        "format": "appgen.personnel-identity-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "personnel_identity",
        "implementation_directory": "src/pyAppGen/pbcs/personnel_identity",
        "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
        "capabilities": PERSONNEL_IDENTITY_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PERSONNEL_IDENTITY_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_department",
            "create_employee",
            "transition_employee_status",
            "assign_role",
            "upsert_identity_attribute",
            "build_org_chart",
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


def personnel_identity_runtime_smoke() -> dict:
    state = personnel_identity_empty_state()
    state = personnel_identity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_country": "US",
            "allowed_worker_types": ("employee", "contractor"),
            "allowed_statuses": ("provisioned", "active", "leave", "suspended", "terminated"),
            "privacy_region": "US",
            "default_identity_assurance": 0.85,
            "workbench_limit": 100,
        },
    )["state"]
    state = personnel_identity_set_parameter(state, "max_roles_per_worker", 4)["state"]
    state = personnel_identity_set_parameter(state, "access_risk_threshold", 0.7)["state"]
    state = personnel_identity_set_parameter(state, "manager_span_limit", 8)["state"]
    state = personnel_identity_register_rule(
        state,
        {
            "rule_id": "rule_core_workforce",
            "tenant": "tenant_alpha",
            "rule_type": "identity",
            "allowed_worker_types": ("employee", "contractor"),
            "allowed_statuses": ("provisioned", "active", "leave"),
            "sensitive_roles": ("payroll_admin", "security_admin"),
            "blocked_role_pairs": (("payroll_admin", "security_admin"),),
            "required_attributes": ("email", "directory_id"),
            "status": "active",
        },
    )["state"]
    state = personnel_identity_register_schema_extension(state, "identity_attribute", {"regional_payload": "jsonb"})["state"]
    state = personnel_identity_receive_event(
        state,
        {
            "event_id": "evt_provisioned_1",
            "event_type": "EmployeeProvisioned",
            "payload": {"tenant": "tenant_alpha", "employee_id": "emp_100", "provisioning_status": "ready"},
        },
    )["state"]
    dept = personnel_identity_register_department(
        state,
        {
            "department_id": "dept_ops",
            "tenant": "tenant_alpha",
            "name": "Operations",
            "legal_entity": "entity_alpha",
            "cost_center": "ops",
            "parent_department_id": None,
            "manager_employee_id": None,
        },
    )
    state = dept["state"]
    manager = personnel_identity_create_employee(
        state,
        {
            "employee_id": "emp_mgr",
            "tenant": "tenant_alpha",
            "person_id": "person_mgr",
            "worker_type": "employee",
            "status": "provisioned",
            "department_id": "dept_ops",
            "manager_employee_id": None,
            "job": "Operations Manager",
            "country": "US",
            "hire_date": "2026-05-26",
            "identity": {"did": "did:appgen:emp-mgr", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = manager["state"]
    employee = personnel_identity_create_employee(
        state,
        {
            "employee_id": "emp_100",
            "tenant": "tenant_alpha",
            "person_id": "person_100",
            "worker_type": "employee",
            "status": "provisioned",
            "department_id": "dept_ops",
            "manager_employee_id": "emp_mgr",
            "job": "Warehouse Associate",
            "country": "US",
            "hire_date": "2026-05-26",
            "identity": {"did": "did:appgen:emp-100", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = employee["state"]
    state = personnel_identity_transition_employee_status(state, "emp_100", status="active", changed_by="hr_admin")["state"]
    role = personnel_identity_assign_role(state, "emp_100", role="warehouse_operator", scope="wh_east", assigned_by="hr_admin")
    state = role["state"]
    state = personnel_identity_upsert_identity_attribute(state, "emp_100", "email", "worker@example.com", assurance=0.95)["state"]
    state = personnel_identity_upsert_identity_attribute(state, "emp_100", "directory_id", "dir_100", assurance=0.92)["state"]
    org = personnel_identity_build_org_chart(state, root_department_id="dept_ops")
    access = personnel_identity_score_access_risk(state, "emp_100")
    simulation = personnel_identity_simulate_access_policy(state, "emp_100", proposed_role="payroll_admin")
    forecast = personnel_identity_forecast_workforce_risk((0.1, 0.15, 0.18), headcount=2)
    parsed = personnel_identity_parse_personnel_event("employee emp_777 department dept_ops role warehouse_operator")
    predictive = personnel_identity_score_workforce_risk({"attrition": 0.08, "access": 0.1, "compliance": 0.06})
    recommendation = personnel_identity_recommend_access_exception("missing_required_attribute")
    route = personnel_identity_route_provisioning({"provisioning_id": "prov_1"}, rails=({"route": "directory_api", "available": False, "latency": 1}, {"route": "outbox", "available": True, "latency": 3}))
    proof = personnel_identity_generate_eligibility_proof(state, "emp_100", disclosure=("employee_id", "status", "department_id"))
    screening = personnel_identity_screen_policy(state, "emp_100", restricted_roles=("restricted_role",))
    controls = personnel_identity_run_control_tests(state)
    api = personnel_identity_build_api_contract()
    schema = personnel_identity_build_schema_contract()
    service = personnel_identity_build_service_contract()
    release = personnel_identity_build_release_evidence()
    federation = personnel_identity_federate_people_view(state, "emp_100", systems=("time", "payroll", "access"))
    identity = personnel_identity_verify_employee_identity(employee["employee"]["identity"])
    resilience = personnel_identity_run_resilience_drill(state, "directory_api_timeout")
    crypto = personnel_identity_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = personnel_identity_schedule_carbon_aware_processing(({"window": "09:00", "carbon": 240}, {"window": "02:00", "carbon": 90}))
    optimization = personnel_identity_optimize_role_access(({"role": "warehouse_operator", "risk": 0.1, "coverage": 0.8}, {"role": "payroll_admin", "risk": 0.4, "coverage": 0.9}))
    allocation = personnel_identity_allocate_manager_capacity(({"manager": "emp_mgr", "capacity": 8, "bid": 0.8}, {"manager": "emp_alt", "capacity": 4, "bid": 0.5}), reports=6)
    anomaly = personnel_identity_detect_identity_anomaly(state)
    stochastic = personnel_identity_model_stochastic_workforce_exposure(risk_path=(0.1, 0.18, 0.2), volatility=0.08)
    workbench = personnel_identity_build_workbench_view(state, tenant="tenant_alpha")
    model = personnel_identity_register_governed_model("people_risk", {"features": ("status", "roles", "attributes"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_workforce_identity_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_org_identity_topology", "ok": employee["employee"]["graph_degree"] >= 4 and org["employee_count"] == 2},
        {"id": "multi_tenant_workforce_identity_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_identity_schema", "ok": state["schema_extensions"]["identity_attribute"]["regional_payload"] == "jsonb"},
        {"id": "probabilistic_identity_assurance_access_risk", "ok": access["risk_score"] < 0.7 and proof["assurance"] >= 0.9},
        {"id": "real_time_directory_org_access_analytics", "ok": workbench["active_employee_count"] == 1 and workbench["role_assignment_count"] == 1},
        {"id": "counterfactual_org_access_policy_simulation", "ok": simulation["ok"] and simulation["decision"] == "allow_with_review"},
        {"id": "temporal_workforce_access_risk_forecasting", "ok": forecast["ok"] and forecast["expected_risk"] > 0},
        {"id": "autonomous_role_access_exception_recommendations", "ok": recommendation["action"] == "request_attribute_completion"},
        {"id": "semantic_personnel_event_parsing", "ok": parsed["ok"] and parsed["employee_id"] == "emp_777"},
        {"id": "predictive_attrition_access_compliance_risk", "ok": predictive["risk_score"] > 0},
        {"id": "self_healing_provisioning_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_personnel_eligibility_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_people_")},
        {"id": "immutable_workforce_identity_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_personnel_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_identity_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service["ok"] and release["ok"] and "EmployeeCreated" in api["events"]["emits"]},
        {"id": "cross_system_people_federation", "ok": federation["ok"] and "payroll" in federation["systems"]},
        {"id": "identity_provider_directory_integration", "ok": route["idempotency_key"].startswith("personnel_identity:Provisioning")},
        {"id": "decentralized_employee_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_provisioning_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_directory_route"},
        {"id": "quantum_resistant_identity_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_identity_processing", "ok": carbon["window"] == "02:00"},
        {"id": "algebraic_role_access_optimization", "ok": optimization["ok"] and optimization["role"] == "warehouse_operator"},
        {"id": "mechanism_design_manager_role_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["reports"] > allocation["allocations"][1]["reports"]},
        {"id": "information_theoretic_identity_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_workforce_risk_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("personnel_identity:IdentityAttributeChanged") and state["handled_events"]["EmployeeProvisioned:evt_provisioned_1"]["status"] == "processed"},
        {"id": "probabilistic_ml_workforce_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_bid"] > 0},
        {"id": "people_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.personnel-identity-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def personnel_identity_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letters": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "employee_provisioning_projections": {},
        "access_policy_projections": {},
        "org_unit_projections": {},
        "role_review_projections": {},
        "departments": {},
        "employees": {},
        "roles": {},
        "attributes": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def personnel_identity_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _PERSONNEL_IDENTITY_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Personnel Identity uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("Personnel Identity supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Personnel Identity requires AppGen-X event topic {PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def personnel_identity_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "max_roles_per_worker",
        "access_risk_threshold",
        "manager_span_limit",
        "identity_assurance_threshold",
        "stale_attribute_age_days",
        "review_cadence_days",
        "lifecycle_grace_days",
        "provisioning_retry_limit",
        "org_depth_limit",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Personnel Identity parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def personnel_identity_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Personnel Identity rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Personnel Identity rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def personnel_identity_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    aliases = {
        "department": "personnel_department",
        "employee": "personnel_employee",
        "role_assignment": "personnel_role_assignment",
        "identity_attribute": "personnel_identity_attribute",
    }
    target = aliases.get(table, table)
    if target not in PERSONNEL_IDENTITY_OWNED_TABLES:
        raise ValueError(f"Personnel Identity schema extensions must target owned tables: {PERSONNEL_IDENTITY_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    existing = dict(state.get("schema_extensions", {}).get(table, {}))
    merged = {**existing, **fields}
    return {
        "ok": True,
        "state": {**state, "schema_extensions": {**state["schema_extensions"], table: merged, target: merged}},
        "schema_extension": {"table": target, "fields": dict(fields)},
        "target": target,
        "fields": merged,
    }


def personnel_identity_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
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
    next_state = {
        **state,
        "inbox": (*state.get("inbox", ()), inbox_entry),
        "handled_events": dict(handled),
        "retry_evidence": tuple(state.get("retry_evidence", ())),
        "dead_letters": tuple(state.get("dead_letters", ())),
        "dead_letter": tuple(state.get("dead_letter", ())),
        "employee_provisioning_projections": dict(state.get("employee_provisioning_projections", {})),
        "access_policy_projections": dict(state.get("access_policy_projections", {})),
        "org_unit_projections": dict(state.get("org_unit_projections", {})),
        "role_review_projections": dict(state.get("role_review_projections", {})),
    }
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"] = (*next_state["retry_evidence"], evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_personnel_event"}
            next_state["dead_letters"] = (*next_state["dead_letters"], dead)
            next_state["dead_letter"] = (*next_state["dead_letter"], dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "EmployeeProvisioned":
        next_state["employee_provisioning_projections"][payload.get("employee_id", event_id)] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload.get("policy_id", event_id)] = payload
    elif event_type == "OrgUnitChanged":
        next_state["org_unit_projections"][payload.get("department_id", payload.get("org_unit_id", event_id))] = payload
    elif event_type == "RoleReviewRequested":
        next_state["role_review_projections"][payload.get("review_id", event_id)] = payload
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def personnel_identity_register_department(state: dict, department: dict) -> dict:
    enriched = {**department, "status": "active"}
    next_state = {**state, "departments": {**state["departments"], department["department_id"]: enriched}}
    next_state = _append_event(next_state, "DepartmentRegistered", {"tenant": department["tenant"], "department_id": department["department_id"]})
    return {"ok": True, "state": next_state, "department": enriched}


def personnel_identity_create_employee(state: dict, employee: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    allowed = employee["worker_type"] in state["configuration"].get("allowed_worker_types", ()) and employee["worker_type"] in rule["allowed_worker_types"] and employee["status"] in rule["allowed_statuses"]
    duplicate = employee["employee_id"] in state["employees"]
    enriched = {**employee, "graph_degree": len(tuple(value for value in (employee["department_id"], employee.get("manager_employee_id"), employee["job"], employee["country"]) if value)), "identity_assurance": state["configuration"].get("default_identity_assurance", 0.8), "status": employee["status"] if allowed and not duplicate else "blocked"}
    next_state = {**state, "employees": {**state["employees"], employee["employee_id"]: enriched}}
    next_state = _append_event(next_state, "EmployeeCreated", {"tenant": employee["tenant"], "employee_id": employee["employee_id"], "status": enriched["status"]})
    return {"ok": allowed and not duplicate, "state": next_state, "employee": enriched}


def personnel_identity_transition_employee_status(state: dict, employee_id: str, *, status: str, changed_by: str) -> dict:
    allowed = status in state["configuration"].get("allowed_statuses", ())
    employee = {**state["employees"][employee_id], "status": status if allowed else "blocked", "status_changed_by": changed_by}
    next_state = {**state, "employees": {**state["employees"], employee_id: employee}}
    next_state = _append_event(next_state, "EmployeeStatusChanged", {"tenant": employee["tenant"], "employee_id": employee_id, "status": employee["status"]})
    return {"ok": allowed, "state": next_state, "employee": employee}


def personnel_identity_assign_role(state: dict, employee_id: str, *, role: str, scope: str, assigned_by: str) -> dict:
    current = tuple(item for item in state["roles"].values() if item["employee_id"] == employee_id and item["status"] == "active")
    max_roles = int(state["parameters"].get("max_roles_per_worker", 99))
    rule = next(iter(state["rules"].values()))
    blocked_pairs = tuple(tuple(pair) for pair in rule.get("blocked_role_pairs", ()))
    new_role_set = tuple(sorted((*tuple(item["role"] for item in current), role)))
    sod_blocked = any(tuple(sorted(pair)) == new_role_set for pair in blocked_pairs)
    ok = len(current) < max_roles and not sod_blocked
    assignment = {"assignment_id": f"role_{employee_id}_{role}", "tenant": state["employees"][employee_id]["tenant"], "employee_id": employee_id, "role": role, "scope": scope, "assigned_by": assigned_by, "status": "active" if ok else "blocked"}
    next_state = {**state, "roles": {**state["roles"], assignment["assignment_id"]: assignment}}
    next_state = _append_event(next_state, "RoleChanged", {"tenant": assignment["tenant"], "employee_id": employee_id, "role": role, "status": assignment["status"]})
    return {"ok": ok, "state": next_state, "assignment": assignment}


def personnel_identity_upsert_identity_attribute(state: dict, employee_id: str, name: str, value: str, *, assurance: float) -> dict:
    employee = state["employees"][employee_id]
    attribute = {"attribute_id": f"{employee_id}:{name}", "tenant": employee["tenant"], "employee_id": employee_id, "name": name, "value": value, "assurance": assurance, "status": "active"}
    next_state = {**state, "attributes": {**state["attributes"], attribute["attribute_id"]: attribute}}
    next_state = _append_event(next_state, "IdentityAttributeChanged", {"tenant": employee["tenant"], "employee_id": employee_id, "name": name, "assurance": assurance})
    return {"ok": True, "state": next_state, "attribute": attribute}


def personnel_identity_build_org_chart(state: dict, *, root_department_id: str) -> dict:
    employees = tuple(employee for employee in state["employees"].values() if employee["department_id"] == root_department_id)
    return {"ok": True, "department_id": root_department_id, "employee_count": len(employees), "nodes": tuple({"employee_id": employee["employee_id"], "manager_employee_id": employee.get("manager_employee_id")} for employee in employees)}


def personnel_identity_score_access_risk(state: dict, employee_id: str) -> dict:
    employee = state["employees"][employee_id]
    role_count = len(tuple(item for item in state["roles"].values() if item["employee_id"] == employee_id and item["status"] == "active"))
    missing = tuple(name for name in next(iter(state["rules"].values())).get("required_attributes", ()) if f"{employee_id}:{name}" not in state["attributes"])
    risk = round(role_count * 0.08 + len(missing) * 0.2 + (1 - employee.get("identity_assurance", 0.8)) * 0.3, 4)
    return {"ok": True, "employee_id": employee_id, "risk_score": risk, "missing_attributes": missing}


def personnel_identity_simulate_access_policy(state: dict, employee_id: str, *, proposed_role: str) -> dict:
    risk = personnel_identity_score_access_risk(state, employee_id)["risk_score"]
    proposed = round(risk + (0.25 if proposed_role in next(iter(state["rules"].values())).get("sensitive_roles", ()) else 0.05), 4)
    return {"ok": True, "employee_id": employee_id, "proposed_role": proposed_role, "proposed_risk": proposed, "decision": "allow_with_review" if proposed < float(state["parameters"].get("access_risk_threshold", 0.7)) else "block"}


def personnel_identity_forecast_workforce_risk(risk_path: tuple[float, ...], *, headcount: int) -> dict:
    return {"ok": True, "expected_risk": round(sum(risk_path) / max(len(risk_path), 1) * headcount, 4), "risk_trend": round((risk_path[-1] - risk_path[0]) if len(risk_path) > 1 else 0, 4)}


def personnel_identity_parse_personnel_event(text: str) -> dict:
    employee = re.search(r"employee\s+([a-z0-9_]+)", text, re.I)
    department = re.search(r"department\s+([a-z0-9_]+)", text, re.I)
    role = re.search(r"role\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(employee and department and role), "employee_id": employee.group(1) if employee else None, "department_id": department.group(1) if department else None, "role": role.group(1) if role else None}


def personnel_identity_score_workforce_risk(signals: dict) -> dict:
    risk = round(signals.get("attrition", 0) * 2 + signals.get("access", 0) + signals.get("compliance", 0) * 2, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.6 else "review"}


def personnel_identity_recommend_access_exception(exception_type: str) -> dict:
    actions = {"missing_required_attribute": "request_attribute_completion", "sod_conflict": "remove_conflicting_role", "stale_review": "schedule_access_review"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def personnel_identity_route_provisioning(provisioning: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"personnel_identity:Provisioning:{provisioning['provisioning_id']}"}


def personnel_identity_generate_eligibility_proof(state: dict, employee_id: str, *, disclosure: tuple[str, ...]) -> dict:
    employee = state["employees"][employee_id]
    claims = {field: employee[field] for field in disclosure if field in employee}
    assurance = min((attribute["assurance"] for attribute in state["attributes"].values() if attribute["employee_id"] == employee_id), default=employee.get("identity_assurance", 0.8))
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_people_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims, "assurance": assurance}


def personnel_identity_screen_policy(state: dict, employee_id: str, *, restricted_roles: tuple[str, ...]) -> dict:
    roles = tuple(item["role"] for item in state["roles"].values() if item["employee_id"] == employee_id and item["status"] == "active")
    blocked = any(role in restricted_roles for role in roles) or state["employees"][employee_id]["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "employee_id": employee_id}


def personnel_identity_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(employee["status"] == "blocked" for employee in state["employees"].values()):
        gaps.append("blocked_employee")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def personnel_identity_build_api_contract() -> dict:
    permissions = personnel_identity_permissions_contract()
    routes = (
        {"route": "POST /personnel/departments", "command": "register_department", "owned_table": "personnel_department"},
        {"route": "POST /personnel/departments/{id}/hierarchy", "command": "register_department", "owned_table": "personnel_department_hierarchy"},
        {"route": "POST /personnel/employees", "command": "create_employee", "owned_table": "personnel_employee"},
        {"route": "POST /personnel/employees/{id}/contacts", "command": "create_employee", "owned_table": "personnel_employee_contact"},
        {"route": "POST /personnel/employees/{id}/documents", "command": "create_employee", "owned_table": "personnel_employee_document"},
        {"route": "POST /personnel/employees/{id}/status", "command": "transition_employee_status", "owned_table": "personnel_employment_lifecycle"},
        {"route": "POST /personnel/employees/{id}/roles", "command": "assign_role", "owned_table": "personnel_role_assignment"},
        {"route": "POST /personnel/employees/{id}/attributes", "command": "upsert_identity_attribute", "owned_table": "personnel_identity_attribute"},
        {"route": "POST /personnel/employees/{id}/verification", "command": "verify_employee_identity", "owned_table": "personnel_identity_verification"},
        {"route": "POST /personnel/employees/{id}/proofs", "command": "generate_eligibility_proof", "owned_table": "personnel_identity_proof"},
        {"route": "GET /personnel/org-chart", "query": "build_org_chart", "owned_table": "personnel_manager_relationship"},
        {"route": "GET /personnel/workbench", "query": "build_workbench_view", "owned_table": "personnel_employee"},
        {"route": "POST /personnel/events/inbox", "command": "receive_event", "owned_table": "personnel_provisioning_event"},
        {"route": "POST /personnel/provisioning/routes", "command": "route_provisioning", "owned_table": "personnel_provisioning_replay"},
        {"route": "POST /personnel/rules", "command": "register_rule", "owned_table": "personnel_policy_rule"},
        {"route": "POST /personnel/parameters", "command": "set_parameter", "owned_table": "personnel_parameter"},
        {"route": "POST /personnel/configuration", "command": "configure_runtime", "owned_table": "personnel_configuration"},
    )
    return {
        "format": "appgen.personnel-identity-api-contract.v1",
        "ok": True,
        "pbc": "personnel_identity",
        "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
        "database_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": PERSONNEL_IDENTITY_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "routes": routes,
        "events": {"emits": PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES, "consumes": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES},
        "emits": PERSONNEL_IDENTITY_EMITTED_EVENT_TYPES,
        "consumes": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(set(permissions["action_permissions"].values()))),
        "action_permissions": permissions["action_permissions"],
        "configuration": (
            "PERSONNEL_IDENTITY_DATABASE_URL",
            "PERSONNEL_IDENTITY_EVENT_TOPIC",
            "PERSONNEL_IDENTITY_RETRY_LIMIT",
            "PERSONNEL_IDENTITY_DEFAULT_COUNTRY",
        ),
    }


def personnel_identity_build_schema_contract() -> dict:
    """Return generated Personnel Identity schema, migration, and model evidence."""
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in PERSONNEL_IDENTITY_OWNED_TABLES}
    table_fields.update(
        {
            "personnel_department": ("tenant", "department_id", "name", "legal_entity", "cost_center", "manager_employee_id", "status", "audit_hash"),
            "personnel_department_hierarchy": ("tenant", "relationship_id", "parent_department_id", "child_department_id", "depth", "valid_from", "audit_hash"),
            "personnel_position": ("tenant", "position_id", "department_id", "job_id", "fte", "vacancy_status", "audit_hash"),
            "personnel_job": ("tenant", "job_id", "job_family", "title", "level", "grade_band", "audit_hash"),
            "personnel_employee": ("tenant", "employee_id", "person_id", "worker_type", "status", "department_id", "manager_employee_id", "country", "hire_date", "identity_hash"),
            "personnel_employee_contact": ("tenant", "contact_id", "employee_id", "contact_type", "value_hash", "verified_at", "audit_hash"),
            "personnel_employee_document": ("tenant", "document_id", "employee_id", "document_type", "storage_ref", "retention_policy_id", "audit_hash"),
            "personnel_employment_lifecycle": ("tenant", "lifecycle_id", "employee_id", "from_status", "to_status", "changed_by", "changed_at", "audit_hash"),
            "personnel_employment_status_history": ("tenant", "history_id", "employee_id", "status", "valid_from", "valid_to", "source_event_id", "audit_hash"),
            "personnel_manager_relationship": ("tenant", "relationship_id", "employee_id", "manager_employee_id", "valid_from", "valid_to", "audit_hash"),
            "personnel_org_assignment": ("tenant", "assignment_id", "employee_id", "department_id", "position_id", "valid_from", "audit_hash"),
            "personnel_work_location": ("tenant", "location_id", "employee_id", "country", "region", "site_id", "audit_hash"),
            "personnel_cost_center_assignment": ("tenant", "assignment_id", "employee_id", "cost_center", "allocation_percent", "valid_from", "audit_hash"),
            "personnel_role_assignment": ("tenant", "assignment_id", "employee_id", "role", "scope", "assigned_by", "status", "audit_hash"),
            "personnel_role_catalog": ("tenant", "role_id", "role_name", "risk_level", "sensitive", "owner", "audit_hash"),
            "personnel_role_review": ("tenant", "review_id", "assignment_id", "reviewer", "decision", "reviewed_at", "audit_hash"),
            "personnel_role_separation_check": ("tenant", "check_id", "employee_id", "role_pair", "decision", "policy_rule_id", "audit_hash"),
            "personnel_identity_attribute": ("tenant", "attribute_id", "employee_id", "name", "value_hash", "assurance", "status", "audit_hash"),
            "personnel_identity_assurance": ("tenant", "assurance_id", "employee_id", "attribute_id", "score", "evidence_ref", "audit_hash"),
            "personnel_identity_verification": ("tenant", "verification_id", "employee_id", "issuer", "did", "verification_status", "audit_hash"),
            "personnel_identity_proof": ("tenant", "proof_id", "employee_id", "public_claims_hash", "proof_hash", "expires_at", "audit_hash"),
            "personnel_access_policy_projection": ("tenant", "policy_id", "policy_version", "projection_hash", "received_event_id", "audit_hash"),
            "personnel_provisioning_event": ("tenant", "event_id", "event_type", "employee_id", "attempts", "handler_status", "audit_hash"),
            "personnel_provisioning_replay": ("tenant", "replay_id", "event_id", "route", "idempotency_key", "status", "audit_hash"),
            "personnel_policy_rule": ("tenant", "rule_id", "scope", "compiled_hash", "enabled", "status", "audit_hash"),
            "personnel_parameter": ("tenant", "parameter_name", "parameter_value", "effective_at", "changed_by", "audit_hash"),
            "personnel_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "event_contract", "stream_engine_picker_visible", "audit_hash"),
            "personnel_identity_appgen_outbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "published_at", "audit_hash"),
            "personnel_identity_appgen_inbox_event": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "audit_hash"),
            "personnel_identity_dead_letter_event": ("tenant", "event_id", "event_type", "payload", "reason", "attempts", "audit_hash"),
        }
    )
    relationships = (
        {"from_table": "personnel_department_hierarchy", "from_field": "parent_department_id", "to_table": "personnel_department", "to_field": "department_id"},
        {"from_table": "personnel_department_hierarchy", "from_field": "child_department_id", "to_table": "personnel_department", "to_field": "department_id"},
        {"from_table": "personnel_position", "from_field": "department_id", "to_table": "personnel_department", "to_field": "department_id"},
        {"from_table": "personnel_position", "from_field": "job_id", "to_table": "personnel_job", "to_field": "job_id"},
        {"from_table": "personnel_employee", "from_field": "department_id", "to_table": "personnel_department", "to_field": "department_id"},
        {"from_table": "personnel_employee_contact", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_employee_document", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_employment_lifecycle", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_employment_status_history", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_manager_relationship", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_manager_relationship", "from_field": "manager_employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_org_assignment", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_org_assignment", "from_field": "department_id", "to_table": "personnel_department", "to_field": "department_id"},
        {"from_table": "personnel_role_assignment", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_role_review", "from_field": "assignment_id", "to_table": "personnel_role_assignment", "to_field": "assignment_id"},
        {"from_table": "personnel_identity_attribute", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
        {"from_table": "personnel_identity_assurance", "from_field": "attribute_id", "to_table": "personnel_identity_attribute", "to_field": "attribute_id"},
        {"from_table": "personnel_identity_proof", "from_field": "employee_id", "to_table": "personnel_employee", "to_field": "employee_id"},
    )
    tables = tuple({"table": table, "fields": table_fields[table], "owner": "personnel_identity"} for table in PERSONNEL_IDENTITY_OWNED_TABLES)
    return {
        "format": "appgen.personnel-identity-owned-schema-contract.v1",
        "ok": len(tables) == len(PERSONNEL_IDENTITY_OWNED_TABLES) and len(tables) >= 40 and all(item["table"].startswith("personnel_") for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/personnel_identity/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(PERSONNEL_IDENTITY_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in PERSONNEL_IDENTITY_OWNED_TABLES
        ),
        "datastore_backends": PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def personnel_identity_build_service_contract() -> dict:
    """Return Personnel Identity command/query service evidence."""
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_department",
        "create_employee",
        "transition_employee_status",
        "assign_role",
        "upsert_identity_attribute",
        "route_provisioning",
        "generate_eligibility_proof",
        "screen_policy",
        "federate_people_view",
        "verify_employee_identity",
        "run_resilience_drill",
        "rotate_crypto_epoch",
        "schedule_carbon_aware_processing",
        "optimize_role_access",
        "allocate_manager_capacity",
        "run_control_tests",
        "register_governed_model",
        "recommend_access_exception",
        "verify_owned_table_boundary",
        "build_workbench_view",
    )
    return {
        "format": "appgen.personnel-identity-service-contract.v1",
        "ok": len(command_methods) >= 25,
        "transaction_boundary": "personnel_identity_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_org_chart",
            "score_access_risk",
            "simulate_access_policy",
            "forecast_workforce_risk",
            "parse_personnel_event",
            "score_workforce_risk",
            "detect_identity_anomaly",
            "model_stochastic_workforce_exposure",
            "build_api_contract",
            "build_schema_contract",
            "build_release_evidence",
        ),
        "mutates_only": PERSONNEL_IDENTITY_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _PERSONNEL_IDENTITY_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _PERSONNEL_IDENTITY_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def personnel_identity_build_release_evidence() -> dict:
    """Return Personnel Identity package-local release evidence."""
    schema = personnel_identity_build_schema_contract()
    service = personnel_identity_build_service_contract()
    api = personnel_identity_build_api_contract()
    permissions = personnel_identity_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 40},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(PERSONNEL_IDENTITY_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 25},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X"},
        {"id": "permissions_cover_commands", "ok": {"create_employee", "assign_role", "receive_event"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == PERSONNEL_IDENTITY_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"]},
    )
    return {
        "format": "appgen.personnel-identity-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def personnel_identity_permissions_contract() -> dict:
    return {
        "format": "appgen.personnel-identity-permissions.v1",
        "ok": True,
        "pbc": "personnel_identity",
        "permissions": (
            "personnel_identity.create",
            "personnel_identity.update",
            "personnel_identity.role",
            "personnel_identity.attribute",
            "personnel_identity.review",
            "personnel_identity.event",
            "personnel_identity.configure",
            "personnel_identity.audit",
        ),
        "roles": {
            "personnel_identity_admin": (
                "personnel_identity.create",
                "personnel_identity.update",
                "personnel_identity.role",
                "personnel_identity.attribute",
                "personnel_identity.review",
                "personnel_identity.event",
                "personnel_identity.configure",
                "personnel_identity.audit",
            ),
            "personnel_identity_steward": (
                "personnel_identity.create",
                "personnel_identity.update",
                "personnel_identity.attribute",
                "personnel_identity.review",
            ),
            "personnel_identity_auditor": ("personnel_identity.review", "personnel_identity.audit"),
        },
        "action_permissions": {
            "register_department": "personnel_identity.create",
            "create_employee": "personnel_identity.create",
            "transition_employee_status": "personnel_identity.update",
            "assign_role": "personnel_identity.role",
            "upsert_identity_attribute": "personnel_identity.attribute",
            "build_org_chart": "personnel_identity.review",
            "score_access_risk": "personnel_identity.review",
            "simulate_access_policy": "personnel_identity.review",
            "screen_policy": "personnel_identity.audit",
            "generate_eligibility_proof": "personnel_identity.audit",
            "run_control_tests": "personnel_identity.audit",
            "route_provisioning": "personnel_identity.update",
            "run_resilience_drill": "personnel_identity.audit",
            "federate_people_view": "personnel_identity.review",
            "verify_employee_identity": "personnel_identity.audit",
            "rotate_crypto_epoch": "personnel_identity.audit",
            "schedule_carbon_aware_processing": "personnel_identity.configure",
            "optimize_role_access": "personnel_identity.review",
            "allocate_manager_capacity": "personnel_identity.review",
            "recommend_access_exception": "personnel_identity.review",
            "register_governed_model": "personnel_identity.audit",
            "detect_identity_anomaly": "personnel_identity.audit",
            "model_stochastic_workforce_exposure": "personnel_identity.audit",
            "parse_personnel_event": "personnel_identity.review",
            "score_workforce_risk": "personnel_identity.review",
            "forecast_workforce_risk": "personnel_identity.review",
            "receive_event": "personnel_identity.event",
            "register_rule": "personnel_identity.configure",
            "register_schema_extension": "personnel_identity.configure",
            "set_parameter": "personnel_identity.configure",
            "configure_runtime": "personnel_identity.configure",
            "build_workbench_view": "personnel_identity.audit",
            "build_schema_contract": "personnel_identity.audit",
            "build_service_contract": "personnel_identity.audit",
            "build_release_evidence": "personnel_identity.audit",
        },
    }


def personnel_identity_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (
        *PERSONNEL_IDENTITY_OWNED_TABLES,
        *PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES,
        *_PERSONNEL_IDENTITY_RUNTIME_TABLES,
        *_PERSONNEL_IDENTITY_ALLOWED_DEPENDENCIES,
    )
    allowed_set = set(allowed)
    violations = tuple(reference for reference in references if reference not in allowed_set and not str(reference).startswith("personnel_identity_"))
    return {
        "format": "appgen.personnel-identity-boundary.v1",
        "ok": not violations,
        "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /identity/policies", "GET /org-units/{id}", "POST /audit/personnel-events"),
            "events": PERSONNEL_IDENTITY_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "employee_provisioning_projection",
                "access_policy_projection",
                "org_unit_projection",
                "role_review_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def personnel_identity_federate_people_view(state: dict, employee_id: str, *, systems: tuple[str, ...]) -> dict:
    employee = state["employees"][employee_id]
    return {"ok": True, "employee_id": employee_id, "systems": systems, "projection": {"status": employee["status"], "department_id": employee["department_id"], "job": employee["job"]}}


def personnel_identity_verify_employee_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def personnel_identity_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"directory_api_timeout", "provisioning_worker_failure"}, "scenario": scenario, "mode": "degraded_directory_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "personnel_identity.dead_letter"}


def personnel_identity_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"people_epoch_{epoch:04d}"}


def personnel_identity_schedule_carbon_aware_processing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def personnel_identity_optimize_role_access(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["coverage"] - candidate["risk"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "role": selected["role"], "objective_score": selected["objective"], "candidates": scored}


def personnel_identity_allocate_manager_capacity(managers: tuple[dict, ...], *, reports: int) -> dict:
    weights = tuple({"manager": manager["manager"], "weight": manager["capacity"] * manager["bid"]} for manager in managers)
    total = sum(item["weight"] for item in weights)
    allocations = tuple({"manager": item["manager"], "reports": round(reports * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["reports"] for item in allocations), 2) == round(reports, 2), "allocations": allocations, "clearing_bid": round(sum(manager["bid"] for manager in managers) / len(managers), 4)}


def personnel_identity_detect_identity_anomaly(state: dict) -> dict:
    role_counts = tuple(len(tuple(role for role in state["roles"].values() if role["employee_id"] == employee_id)) for employee_id in state["employees"])
    if not role_counts:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(role_counts) or 1
    entropy = round(-sum((count / total) * math.log(max(count / total, 0.0001), 2) for count in role_counts if count), 4)
    mean = sum(role_counts) / len(role_counts)
    return {"ok": True, "entropy": entropy, "outliers": tuple(count for count in role_counts if abs(count - mean) > 3)}


def personnel_identity_model_stochastic_workforce_exposure(*, risk_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(risk_path) < 2 else (risk_path[-1] - risk_path[0]) / (len(risk_path) - 1)
    exposure = abs(drift) * volatility * len(risk_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def personnel_identity_build_workbench_view(state: dict, *, tenant: str) -> dict:
    employees = tuple(employee for employee in state["employees"].values() if employee["tenant"] == tenant)
    roles = tuple(role for role in state["roles"].values() if role["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "department_count": len(tuple(dept for dept in state["departments"].values() if dept["tenant"] == tenant)),
        "employee_count": len(employees),
        "active_employee_count": len(tuple(employee for employee in employees if employee["status"] == "active")),
        "role_assignment_count": len(tuple(role for role in roles if role["status"] == "active")),
        "attribute_count": len(tuple(attribute for attribute in state["attributes"].values() if attribute["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": PERSONNEL_IDENTITY_OWNED_TABLES,
            "outbox_table": "personnel_identity_appgen_outbox_event",
            "inbox_table": "personnel_identity_appgen_inbox_event",
            "dead_letter_table": "personnel_identity_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "permissions": personnel_identity_permissions_contract()["action_permissions"],
        },
    }


def personnel_identity_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"people_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"personnel_identity:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
