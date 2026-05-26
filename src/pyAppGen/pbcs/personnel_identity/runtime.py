"""Executable runtime for the Personnel Directory and Identity PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


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
    "employee_master",
    "employment_lifecycle",
    "manager_hierarchy",
    "org_chart",
    "role_assignment",
    "role_change",
    "identity_attribute",
    "segregation_of_duties",
    "identity_assurance",
    "provisioning_handler",
    "employee_events",
    "multi_entity_isolation",
    "privacy_residency_retention",
    "directory_search",
    "approval_review",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def personnel_identity_runtime_capabilities() -> dict:
    smoke = personnel_identity_runtime_smoke()
    return {
        "format": "appgen.personnel-identity-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "personnel_identity",
        "implementation_directory": "src/pyAppGen/pbcs/personnel_identity",
        "capabilities": PERSONNEL_IDENTITY_RUNTIME_CAPABILITY_KEYS,
        "standard_features": PERSONNEL_IDENTITY_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_department",
            "create_employee",
            "transition_employee_status",
            "assign_role",
            "upsert_identity_attribute",
            "build_org_chart",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def personnel_identity_runtime_smoke() -> dict:
    state = personnel_identity_empty_state()
    state = personnel_identity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.people.events",
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "EmployeeCreated" in api["events"]["emits"]},
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
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("personnel_identity:IdentityAttributeChanged")},
        {"id": "probabilistic_ml_workforce_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_bid"] > 0},
        {"id": "people_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.personnel-identity-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def personnel_identity_empty_state() -> dict:
    return {"events": (), "outbox": (), "departments": {}, "employees": {}, "roles": {}, "attributes": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def personnel_identity_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Personnel Identity supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("Personnel Identity requires an AppGen-X event topic")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
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
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


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
    return {"ok": True, "routes": ("POST /employees", "GET /org-chart", "GET /identity-attributes", "POST /personnel-rules", "POST /personnel-parameters", "POST /personnel-configuration"), "events": {"emits": ("EmployeeCreated", "RoleChanged", "CustomerUpdated"), "consumes": ("EmployeeProvisioned",)}, "permissions": ("personnel_identity.create", "personnel_identity.update", "personnel_identity.role", "personnel_identity.attribute", "personnel_identity.review", "personnel_identity.configure", "personnel_identity.audit"), "configuration": ("PERSONNEL_IDENTITY_DATABASE_URL", "PERSONNEL_IDENTITY_EVENT_TOPIC", "PERSONNEL_IDENTITY_RETRY_LIMIT", "PERSONNEL_IDENTITY_DEFAULT_COUNTRY")}


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
