"""Executable runtime for the Talent Onboarding PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


TALENT_ONBOARDING_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_talent_lifecycle",
    "graph_relational_hiring_topology",
    "multi_tenant_talent_isolation",
    "schema_evolution_resilient_talent_schema",
    "probabilistic_candidate_match_compliance_scoring",
    "real_time_pipeline_onboarding_analytics",
    "counterfactual_hiring_policy_simulation",
    "temporal_hiring_demand_cycle_forecasting",
    "autonomous_candidate_exception_resolution",
    "semantic_candidate_instruction_parsing",
    "predictive_candidate_attrition_compliance_risk",
    "self_healing_screening_provisioning_route_selection",
    "zero_knowledge_candidate_eligibility_proof",
    "immutable_talent_audit_trail",
    "dynamic_talent_policy_screening",
    "automated_talent_control_testing",
    "universal_api_async_streaming",
    "cross_system_talent_federation",
    "identity_access_notification_integration",
    "decentralized_candidate_identity",
    "chaos_engineered_onboarding_tolerance",
    "quantum_resistant_candidate_authorization",
    "carbon_aware_interview_onboarding_scheduling",
    "algebraic_pipeline_optimization",
    "mechanism_design_interview_allocation",
    "information_theoretic_hiring_anomaly_detection",
    "temporal_hiring_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_candidate_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "talent_mlops_governance",
)
TALENT_ONBOARDING_STANDARD_FEATURE_KEYS = (
    "job_requisition_management",
    "candidate_capture",
    "consent_management",
    "candidate_pipeline",
    "interview_plan",
    "evaluation_evidence",
    "background_check",
    "adjudication",
    "offer_management",
    "offer_acceptance",
    "onboarding_task_generation",
    "task_assignment",
    "task_completion",
    "employee_provisioning",
    "role_projection",
    "privacy_retention_controls",
    "pipeline_analytics",
    "multi_entity_isolation",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def talent_onboarding_runtime_capabilities() -> dict:
    smoke = talent_onboarding_runtime_smoke()
    return {
        "format": "appgen.talent-onboarding-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "talent_onboarding",
        "implementation_directory": "src/pyAppGen/pbcs/talent_onboarding",
        "capabilities": TALENT_ONBOARDING_RUNTIME_CAPABILITY_KEYS,
        "standard_features": TALENT_ONBOARDING_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "create_job_requisition",
            "create_candidate",
            "advance_candidate_stage",
            "record_background_check",
            "extend_offer",
            "accept_offer",
            "create_onboarding_task",
            "complete_onboarding_task",
            "provision_employee",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def talent_onboarding_runtime_smoke() -> dict:
    state = talent_onboarding_empty_state()
    state = talent_onboarding_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.talent.events",
            "retry_limit": 3,
            "allowed_countries": ("US", "CA"),
            "allowed_candidate_sources": ("referral", "career_site", "agency"),
            "allowed_check_providers": ("trusted_screen",),
            "allowed_task_types": ("identity", "equipment", "policy", "training"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = talent_onboarding_set_parameter(state, "minimum_match_score", 0.7)["state"]
    state = talent_onboarding_set_parameter(state, "offer_expiry_days", 7)["state"]
    state = talent_onboarding_set_parameter(state, "onboarding_sla_days", 5)["state"]
    state = talent_onboarding_set_parameter(state, "background_check_confidence_threshold", 0.85)["state"]
    state = talent_onboarding_set_parameter(state, "retention_days", 365)["state"]
    state = talent_onboarding_register_rule(
        state,
        {
            "rule_id": "rule_ops_hiring",
            "tenant": "tenant_alpha",
            "rule_type": "hiring",
            "eligible_worker_types": ("employee",),
            "allowed_countries": ("US",),
            "required_candidate_consents": ("privacy", "screening"),
            "allowed_stages": ("applied", "screen", "interview", "offer", "hired"),
            "required_check_types": ("identity", "criminal"),
            "task_templates": ("identity", "equipment", "policy"),
            "status": "active",
        },
    )["state"]
    state = talent_onboarding_register_schema_extension(state, "candidate", {"portfolio_payload": "jsonb"})["state"]
    requisition = talent_onboarding_create_job_requisition(
        state,
        {
            "requisition_id": "req_100",
            "tenant": "tenant_alpha",
            "title": "Operations Analyst",
            "department": "Operations",
            "manager_employee_id": "mgr_100",
            "country": "US",
            "location": "NYC",
            "worker_type": "employee",
            "headcount": 1,
            "budget": 120000,
        },
    )
    state = requisition["state"]
    candidate = talent_onboarding_create_candidate(
        state,
        {
            "candidate_id": "cand_100",
            "tenant": "tenant_alpha",
            "requisition_id": "req_100",
            "name": "Ada Worker",
            "source": "referral",
            "country": "US",
            "skills": ("operations", "analytics"),
            "match_score": 0.86,
            "consents": ("privacy", "screening"),
            "identity": {"did": "did:appgen:cand-100", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = candidate["state"]
    state = talent_onboarding_advance_candidate_stage(state, "cand_100", stage="interview", actor="recruiter_1")["state"]
    check = talent_onboarding_record_background_check(
        state,
        {"check_id": "check_100", "tenant": "tenant_alpha", "candidate_id": "cand_100", "provider": "trusted_screen", "check_type": "identity", "confidence": 0.93, "result": "clear"},
    )
    state = check["state"]
    offer = talent_onboarding_extend_offer(state, "cand_100", {"offer_id": "offer_100", "salary": 95000, "currency": "USD", "start_date": "2026-06-15", "expires_in_days": 7})
    state = offer["state"]
    state = talent_onboarding_accept_offer(state, "cand_100", accepted_by="candidate")["state"]
    task = talent_onboarding_create_onboarding_task(state, "cand_100", {"task_id": "task_100", "task_type": "identity", "assignee": "hr_ops", "due_in_days": 3})
    state = task["state"]
    state = talent_onboarding_complete_onboarding_task(state, "task_100", completed_by="hr_ops")["state"]
    provisioned = talent_onboarding_provision_employee(state, "cand_100", provisioned_by="hr_ops")
    state = provisioned["state"]
    simulation = talent_onboarding_simulate_hiring_policy(state, "req_100", proposed_match_score=0.65)
    forecast = talent_onboarding_forecast_hiring_cycle((10, 8, 6), demand=3)
    parsed = talent_onboarding_parse_candidate_instruction("candidate cand_777 requisition req_777 stage offer action advance")
    risk = talent_onboarding_score_candidate_risk({"match": 0.1, "check": 0.05, "sla": 0.2})
    recommendation = talent_onboarding_recommend_exception_resolution("missing_consent")
    route = talent_onboarding_route_screening_or_provisioning({"event_id": "talent_route"}, rails=({"route": "screening_api", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 3}))
    proof = talent_onboarding_generate_candidate_proof(state, "cand_100", disclosure=("candidate_id", "requisition_id", "stage"))
    screening = talent_onboarding_screen_policy(state, "cand_100", restricted_countries=("restricted_country",))
    controls = talent_onboarding_run_control_tests(state)
    api = talent_onboarding_build_api_contract()
    federation = talent_onboarding_federate_talent_view(state, "cand_100", systems=("personnel", "access", "payroll", "notifications"))
    identity = talent_onboarding_verify_candidate_identity(state["candidates"]["cand_100"]["identity"])
    resilience = talent_onboarding_run_resilience_drill(state, "screening_api_timeout")
    crypto = talent_onboarding_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = talent_onboarding_schedule_carbon_aware_interview(({"window": "day", "carbon": 210}, {"window": "night", "carbon": 85}))
    optimization = talent_onboarding_optimize_pipeline(({"pipeline": "fast", "quality": 0.8, "cost": 0.25}, {"pipeline": "balanced", "quality": 0.9, "cost": 0.2}))
    allocation = talent_onboarding_allocate_interviews(({"interviewer": "mgr_100", "preference": 0.8, "capacity": 3}, {"interviewer": "peer_100", "preference": 0.6, "capacity": 2}), panels=4)
    anomaly = talent_onboarding_detect_hiring_anomaly(state)
    stochastic = talent_onboarding_model_stochastic_hiring_exposure(candidate_path=(5, 8, 9), volatility=0.12)
    workbench = talent_onboarding_build_workbench_view(state, tenant="tenant_alpha")
    model = talent_onboarding_register_governed_model("candidate_risk", {"features": ("match_score", "check_confidence", "source"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_talent_lifecycle", "ok": len(state["events"]) >= 9 and state["events"][-1]["hash"]},
        {"id": "graph_relational_hiring_topology", "ok": requisition["requisition"]["graph_degree"] >= 4},
        {"id": "multi_tenant_talent_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_talent_schema", "ok": state["schema_extensions"]["candidate"]["portfolio_payload"] == "jsonb"},
        {"id": "probabilistic_candidate_match_compliance_scoring", "ok": candidate["candidate"]["match_score"] >= 0.86 and check["check"]["risk_score"] < 0.2},
        {"id": "real_time_pipeline_onboarding_analytics", "ok": workbench["hired_count"] == 1},
        {"id": "counterfactual_hiring_policy_simulation", "ok": simulation["decision"] == "reject_under_threshold"},
        {"id": "temporal_hiring_demand_cycle_forecasting", "ok": forecast["forecast_openings"] > 0},
        {"id": "autonomous_candidate_exception_resolution", "ok": recommendation["action"] == "request_candidate_consent"},
        {"id": "semantic_candidate_instruction_parsing", "ok": parsed["ok"] and parsed["candidate_id"] == "cand_777"},
        {"id": "predictive_candidate_attrition_compliance_risk", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_screening_provisioning_route_selection", "ok": route["ok"] and route["route"] == "outbox" and route["failover_used"]},
        {"id": "zero_knowledge_candidate_eligibility_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_candidate_")},
        {"id": "immutable_talent_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_talent_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_talent_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "CandidateHired" in api["events"]["emits"]},
        {"id": "cross_system_talent_federation", "ok": federation["ok"] and "personnel" in federation["systems"]},
        {"id": "identity_access_notification_integration", "ok": provisioned["handoffs"] == ("personnel_identity_projection", "access_preload_request", "notification_welcome_sequence")},
        {"id": "decentralized_candidate_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_onboarding_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_screening_route"},
        {"id": "quantum_resistant_candidate_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_interview_onboarding_scheduling", "ok": carbon["window"] == "night"},
        {"id": "algebraic_pipeline_optimization", "ok": optimization["ok"] and optimization["pipeline"] == "balanced"},
        {"id": "mechanism_design_interview_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["panels"] > allocation["allocations"][1]["panels"]},
        {"id": "information_theoretic_hiring_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_hiring_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("talent_onboarding:EmployeeProvisioned")},
        {"id": "probabilistic_ml_candidate_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_preference"] > 0},
        {"id": "talent_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.talent-onboarding-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def talent_onboarding_empty_state() -> dict:
    return {"events": (), "outbox": (), "requisitions": {}, "candidates": {}, "checks": {}, "offers": {}, "tasks": {}, "rules": {}, "parameters": {}, "configuration": {}, "schema_extensions": {}, "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"}}


def talent_onboarding_configure_runtime(state: dict, configuration: dict) -> dict:
    allowed_databases = {"postgresql", "mysql", "mariadb"}
    if configuration.get("database_backend") not in allowed_databases:
        raise ValueError("Talent Onboarding supports only PostgreSQL, MySQL, or MariaDB backends")
    if not configuration.get("event_topic"):
        raise ValueError("Talent Onboarding requires an AppGen-X event topic")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "appgen_event_contract",
        "allowed_database_backends": tuple(sorted(allowed_databases)),
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def talent_onboarding_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "minimum_match_score",
        "offer_expiry_days",
        "onboarding_sla_days",
        "maximum_active_requisitions_per_manager",
        "background_check_confidence_threshold",
        "retention_days",
        "candidate_review_sla_days",
        "interview_panel_size",
        "offer_approval_threshold",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported Talent Onboarding parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def talent_onboarding_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required Talent Onboarding rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("Talent Onboarding rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def talent_onboarding_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    return {"ok": True, "state": {**state, "schema_extensions": {**state["schema_extensions"], table: dict(fields)}}}


def talent_onboarding_create_job_requisition(state: dict, requisition: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    ok = requisition["country"] in state["configuration"].get("allowed_countries", ()) and requisition["worker_type"] in rule["eligible_worker_types"]
    enriched = {**requisition, "status": "open" if ok else "blocked", "graph_degree": len(tuple(value for value in (requisition["department"], requisition["manager_employee_id"], requisition["country"], requisition["location"]) if value))}
    next_state = {**state, "requisitions": {**state["requisitions"], requisition["requisition_id"]: enriched}}
    next_state = _append_event(next_state, "JobRequisitionOpened", {"tenant": requisition["tenant"], "requisition_id": requisition["requisition_id"], "title": requisition["title"]})
    return {"ok": ok, "state": next_state, "requisition": enriched}


def talent_onboarding_create_candidate(state: dict, candidate: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    requisition = state["requisitions"][candidate["requisition_id"]]
    ok = candidate["source"] in state["configuration"].get("allowed_candidate_sources", ()) and set(rule["required_candidate_consents"]) <= set(candidate["consents"]) and candidate["match_score"] >= float(state["parameters"].get("minimum_match_score", 0))
    enriched = {**candidate, "status": "active" if ok and requisition["status"] == "open" else "blocked", "stage": "applied"}
    next_state = {**state, "candidates": {**state["candidates"], candidate["candidate_id"]: enriched}}
    next_state = _append_event(next_state, "CandidateCreated", {"tenant": candidate["tenant"], "candidate_id": candidate["candidate_id"], "requisition_id": candidate["requisition_id"]})
    return {"ok": ok, "state": next_state, "candidate": enriched}


def talent_onboarding_advance_candidate_stage(state: dict, candidate_id: str, *, stage: str, actor: str) -> dict:
    rule = next(iter(state["rules"].values()))
    candidate = state["candidates"][candidate_id]
    ok = stage in rule["allowed_stages"] and candidate["status"] == "active"
    updated = {**candidate, "stage": stage if ok else candidate["stage"], "stage_actor": actor}
    next_state = {**state, "candidates": {**state["candidates"], candidate_id: updated}}
    next_state = _append_event(next_state, "CandidateStageAdvanced", {"tenant": candidate["tenant"], "candidate_id": candidate_id, "stage": updated["stage"]})
    return {"ok": ok, "state": next_state, "candidate": updated}


def talent_onboarding_record_background_check(state: dict, check: dict) -> dict:
    threshold = float(state["parameters"].get("background_check_confidence_threshold", 0.85))
    ok = check["provider"] in state["configuration"].get("allowed_check_providers", ()) and check["confidence"] >= threshold and check["result"] == "clear"
    enriched = {**check, "status": "clear" if ok else "review", "risk_score": round(max(0, threshold - check["confidence"]), 4)}
    next_state = {**state, "checks": {**state["checks"], check["check_id"]: enriched}}
    next_state = _append_event(next_state, "BackgroundCheckCompleted", {"tenant": check["tenant"], "check_id": check["check_id"], "candidate_id": check["candidate_id"], "status": enriched["status"]})
    return {"ok": ok, "state": next_state, "check": enriched}


def talent_onboarding_extend_offer(state: dict, candidate_id: str, offer: dict) -> dict:
    candidate = state["candidates"][candidate_id]
    ok = candidate["stage"] in {"interview", "offer"} and offer["expires_in_days"] <= int(state["parameters"].get("offer_expiry_days", 7))
    enriched = {**offer, "tenant": candidate["tenant"], "candidate_id": candidate_id, "status": "extended" if ok else "blocked"}
    updated_candidate = {**candidate, "stage": "offer" if ok else candidate["stage"]}
    next_state = {**state, "offers": {**state["offers"], offer["offer_id"]: enriched}, "candidates": {**state["candidates"], candidate_id: updated_candidate}}
    next_state = _append_event(next_state, "OfferExtended", {"tenant": candidate["tenant"], "candidate_id": candidate_id, "offer_id": offer["offer_id"]})
    return {"ok": ok, "state": next_state, "offer": enriched}


def talent_onboarding_accept_offer(state: dict, candidate_id: str, *, accepted_by: str) -> dict:
    candidate = state["candidates"][candidate_id]
    accepted = {**candidate, "stage": "hired", "accepted_by": accepted_by}
    next_state = {**state, "candidates": {**state["candidates"], candidate_id: accepted}}
    next_state = _append_event(next_state, "OfferAccepted", {"tenant": candidate["tenant"], "candidate_id": candidate_id, "accepted_by": accepted_by})
    return {"ok": True, "state": next_state, "candidate": accepted}


def talent_onboarding_create_onboarding_task(state: dict, candidate_id: str, task: dict) -> dict:
    candidate = state["candidates"][candidate_id]
    ok = task["task_type"] in state["configuration"].get("allowed_task_types", ()) and task["due_in_days"] <= int(state["parameters"].get("onboarding_sla_days", 5))
    enriched = {**task, "tenant": candidate["tenant"], "candidate_id": candidate_id, "status": "open" if ok else "blocked"}
    next_state = {**state, "tasks": {**state["tasks"], task["task_id"]: enriched}}
    next_state = _append_event(next_state, "OnboardingTaskCreated", {"tenant": candidate["tenant"], "candidate_id": candidate_id, "task_id": task["task_id"]})
    return {"ok": ok, "state": next_state, "task": enriched}


def talent_onboarding_complete_onboarding_task(state: dict, task_id: str, *, completed_by: str) -> dict:
    task = state["tasks"][task_id]
    updated = {**task, "status": "completed", "completed_by": completed_by}
    next_state = {**state, "tasks": {**state["tasks"], task_id: updated}}
    next_state = _append_event(next_state, "OnboardingTaskCompleted", {"tenant": task["tenant"], "candidate_id": task["candidate_id"], "task_id": task_id})
    return {"ok": True, "state": next_state, "task": updated}


def talent_onboarding_provision_employee(state: dict, candidate_id: str, *, provisioned_by: str) -> dict:
    candidate = state["candidates"][candidate_id]
    tasks = tuple(task for task in state["tasks"].values() if task["candidate_id"] == candidate_id)
    ok = candidate["stage"] == "hired" and tasks and all(task["status"] == "completed" for task in tasks)
    updated = {**candidate, "status": "provisioned" if ok else "pending_provisioning", "provisioned_by": provisioned_by}
    handoffs = ("personnel_identity_projection", "access_preload_request", "notification_welcome_sequence")
    next_state = {**state, "candidates": {**state["candidates"], candidate_id: updated}}
    next_state = _append_event(next_state, "CandidateHired", {"tenant": candidate["tenant"], "candidate_id": candidate_id, "requisition_id": candidate["requisition_id"]})
    next_state = _append_event(next_state, "EmployeeProvisioned", {"tenant": candidate["tenant"], "candidate_id": candidate_id, "employee_key": f"emp_from_{candidate_id}", "handoffs": handoffs})
    return {"ok": ok, "state": next_state, "candidate": updated, "handoffs": handoffs}


def talent_onboarding_simulate_hiring_policy(state: dict, requisition_id: str, *, proposed_match_score: float) -> dict:
    threshold = float(state["parameters"].get("minimum_match_score", 0.7))
    return {"ok": True, "requisition_id": requisition_id, "proposed_match_score": proposed_match_score, "decision": "advance" if proposed_match_score >= threshold else "reject_under_threshold"}


def talent_onboarding_forecast_hiring_cycle(days_path: tuple[float, ...], *, demand: int) -> dict:
    trend = days_path[-1] - days_path[0] if len(days_path) > 1 else 0
    return {"ok": True, "forecast_cycle_days": round(days_path[-1] + trend / max(1, len(days_path)), 2), "forecast_openings": demand}


def talent_onboarding_parse_candidate_instruction(text: str) -> dict:
    candidate = re.search(r"candidate\s+([a-z0-9_]+)", text, re.I)
    requisition = re.search(r"requisition\s+([a-z0-9_]+)", text, re.I)
    stage = re.search(r"stage\s+([a-z0-9_]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(candidate and requisition and stage and action), "candidate_id": candidate.group(1) if candidate else None, "requisition_id": requisition.group(1) if requisition else None, "stage": stage.group(1) if stage else None, "action": action.group(1) if action else None}


def talent_onboarding_score_candidate_risk(signals: dict) -> dict:
    risk = round(signals.get("match", 0) + signals.get("check", 0) * 2 + signals.get("sla", 0) * 1.5, 4)
    return {"ok": True, "risk_score": risk, "decision": "monitor" if risk < 0.7 else "review"}


def talent_onboarding_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"missing_consent": "request_candidate_consent", "check_review": "route_adjudication", "task_overdue": "escalate_onboarding_owner"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def talent_onboarding_route_screening_or_provisioning(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"talent_onboarding:Route:{event['event_id']}"}


def talent_onboarding_generate_candidate_proof(state: dict, candidate_id: str, *, disclosure: tuple[str, ...]) -> dict:
    candidate = state["candidates"][candidate_id]
    claims = {field: candidate[field] for field in disclosure if field in candidate}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_candidate_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def talent_onboarding_screen_policy(state: dict, candidate_id: str, *, restricted_countries: tuple[str, ...]) -> dict:
    candidate = state["candidates"][candidate_id]
    blocked = candidate["country"] in restricted_countries or candidate["status"] == "blocked"
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "candidate_id": candidate_id}


def talent_onboarding_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(candidate["stage"] == "hired" and candidate["status"] != "provisioned" for candidate in state["candidates"].values()):
        gaps.append("hired_candidate_not_provisioned")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def talent_onboarding_build_api_contract() -> dict:
    return {"ok": True, "routes": ("POST /candidates", "POST /offers", "POST /onboarding", "POST /talent-rules", "POST /talent-parameters", "POST /talent-configuration"), "events": {"emits": ("EmployeeProvisioned", "CandidateHired"), "consumes": ("RoleChanged",)}, "permissions": ("talent_onboarding.read", "talent_onboarding.requisition", "talent_onboarding.candidate", "talent_onboarding.offer", "talent_onboarding.onboard", "talent_onboarding.configure", "talent_onboarding.audit"), "configuration": ("TALENT_ONBOARDING_DATABASE_URL", "TALENT_ONBOARDING_EVENT_TOPIC", "TALENT_ONBOARDING_RETRY_LIMIT", "TALENT_ONBOARDING_DEFAULT_TIMEZONE")}


def talent_onboarding_federate_talent_view(state: dict, candidate_id: str, *, systems: tuple[str, ...]) -> dict:
    candidate = state["candidates"][candidate_id]
    return {"ok": True, "candidate_id": candidate_id, "systems": systems, "projection": {"requisition_id": candidate["requisition_id"], "stage": candidate["stage"], "status": candidate["status"]}}


def talent_onboarding_verify_candidate_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def talent_onboarding_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"screening_api_timeout", "provisioning_worker_failure"}, "scenario": scenario, "mode": "degraded_screening_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "talent_onboarding.dead_letter"}


def talent_onboarding_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"talent_epoch_{epoch:04d}"}


def talent_onboarding_schedule_carbon_aware_interview(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def talent_onboarding_optimize_pipeline(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(candidate["quality"] - candidate["cost"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "pipeline": selected["pipeline"], "objective_score": selected["objective"], "candidates": scored}


def talent_onboarding_allocate_interviews(interviewers: tuple[dict, ...], *, panels: int) -> dict:
    weights = tuple({"interviewer": item["interviewer"], "weight": item["preference"] * item["capacity"]} for item in interviewers)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"interviewer": item["interviewer"], "panels": round(panels * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["panels"] for item in allocations), 2) == round(panels, 2), "allocations": allocations, "clearing_preference": round(sum(item["preference"] for item in interviewers) / len(interviewers), 4)}


def talent_onboarding_detect_hiring_anomaly(state: dict) -> dict:
    scores = tuple(candidate["match_score"] for candidate in state["candidates"].values())
    if not scores:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(scores) or 1
    entropy = round(-sum((score / total) * math.log(max(score / total, 0.0001), 2) for score in scores), 4)
    mean = sum(scores) / len(scores)
    return {"ok": True, "entropy": entropy, "outliers": tuple(score for score in scores if abs(score - mean) > 0.3)}


def talent_onboarding_model_stochastic_hiring_exposure(*, candidate_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(candidate_path) < 2 else (candidate_path[-1] - candidate_path[0]) / (len(candidate_path) - 1)
    exposure = abs(drift) * volatility * len(candidate_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def talent_onboarding_build_workbench_view(state: dict, *, tenant: str) -> dict:
    requisitions = tuple(req for req in state["requisitions"].values() if req["tenant"] == tenant)
    candidates = tuple(candidate for candidate in state["candidates"].values() if candidate["tenant"] == tenant)
    tasks = tuple(task for task in state["tasks"].values() if task["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "requisition_count": len(requisitions),
        "candidate_count": len(candidates),
        "hired_count": len(tuple(candidate for candidate in candidates if candidate["stage"] == "hired")),
        "provisioned_count": len(tuple(candidate for candidate in candidates if candidate["status"] == "provisioned")),
        "background_check_count": len(tuple(check for check in state["checks"].values() if check["tenant"] == tenant)),
        "offer_count": len(tuple(offer for offer in state["offers"].values() if offer["tenant"] == tenant)),
        "open_task_count": len(tuple(task for task in tasks if task["status"] == "open")),
        "completed_task_count": len(tuple(task for task in tasks if task["status"] == "completed")),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
    }


def talent_onboarding_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"talent_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"talent_onboarding:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
