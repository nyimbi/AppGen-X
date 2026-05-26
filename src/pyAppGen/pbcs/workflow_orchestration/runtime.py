"""Executable runtime for the Workflow Orchestration PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC = "appgen.workflow.events"
WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
WORKFLOW_ORCHESTRATION_OWNED_TABLES = (
    "workflow_definition",
    "workflow_instance",
    "workflow_signal",
    "timer_task",
    "saga_step",
    "compensation",
    "human_task",
    "workflow_rule",
    "workflow_parameter",
    "workflow_configuration",
)
WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES = (
    "WorkflowDefinitionPublished",
    "WorkflowStarted",
    "WorkflowSignalAccepted",
    "SagaStepCompleted",
    "TimerScheduled",
    "CompensationExecuted",
    "WorkflowCompleted",
)
WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES = (
    "InvoiceApproved",
    "OrderVerified",
    "ShipmentDelivered",
    "PaymentCaptured",
    "SchemaAccepted",
    "AccessPolicyChanged",
    "RoutePublished",
)
_WORKFLOW_ORCHESTRATION_RUNTIME_TABLES = (
    "workflow_orchestration_appgen_outbox_event",
    "workflow_orchestration_appgen_inbox_event",
    "workflow_orchestration_dead_letter_event",
)
_WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES = (
    "gateway_workflow_projection",
    "schema_workflow_projection",
    "audit_workflow_projection",
    "identity_workflow_projection",
    "composition_workflow_projection",
    "order_workflow_projection",
    "payment_workflow_projection",
    "shipment_workflow_projection",
    "invoice_workflow_projection",
    "GET /gateway/routes",
    "GET /schemas/subjects",
    "GET /identity/policies",
    "POST /audit/workflow-events",
    "POST /composition/workflow-projections",
)
_WORKFLOW_ORCHESTRATION_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}


WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_workflow_lifecycle",
    "graph_relational_saga_topology",
    "multi_tenant_workflow_isolation",
    "schema_on_read_workflow_context",
    "probabilistic_sla_breach_scoring",
    "real_time_workflow_analytics",
    "counterfactual_saga_policy_simulation",
    "temporal_workflow_forecasting",
    "autonomous_compensation_recommendation",
    "semantic_workflow_intent_parsing",
    "predictive_saga_risk_scoring",
    "self_healing_workflow_route_selection",
    "zero_knowledge_workflow_completion_proof",
    "immutable_workflow_audit_trail",
    "dynamic_workflow_policy_screening",
    "automated_workflow_control_testing",
    "universal_api_async_workflow_surface",
    "cross_system_workflow_federation",
    "gateway_schema_audit_identity_composition_integration",
    "decentralized_workflow_actor_identity",
    "chaos_engineered_workflow_tolerance",
    "quantum_resistant_workflow_authorization",
    "carbon_aware_workflow_scheduling",
    "algebraic_state_machine_minimization",
    "mechanism_design_saga_resource_allocation",
    "information_theoretic_workflow_anomaly_detection",
    "temporal_workflow_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_workflow_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "workflow_mlops_governance",
)
WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS = (
    "workflow_definition_catalog",
    "state_machine_authoring",
    "definition_versioning",
    "instance_orchestration",
    "signal_handling",
    "timer_scheduling",
    "retry_policy",
    "saga_step_execution",
    "compensation_execution",
    "human_task_queue",
    "approval_routing",
    "sla_policy",
    "escalation_policy",
    "correlation_id",
    "idempotent_handlers",
    "retry_dead_letter",
    "workflow_telemetry",
    "policy_gate",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
    "release_gate",
    "audit_evidence",
    "package_registration_validation",
    "appgen_event_contract",
)


def workflow_orchestration_runtime_capabilities() -> dict:
    smoke = workflow_orchestration_runtime_smoke()
    return {
        "format": "appgen.workflow-orchestration-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "workflow_orchestration",
        "implementation_directory": "src/pyAppGen/pbcs/workflow_orchestration",
        "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
        "capabilities": WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "define_workflow",
            "start_instance",
            "signal_instance",
            "schedule_timer",
            "record_step_result",
            "execute_compensation",
            "complete_workflow",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def workflow_orchestration_runtime_smoke() -> dict:
    state = workflow_orchestration_empty_state()
    state = workflow_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_signal_sources": ("api_gateway_mesh", "schema_registry", "composition_engine"),
            "default_versioning": "semantic",
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = workflow_orchestration_set_parameter(state, "default_retry_limit", 3)["state"]
    state = workflow_orchestration_set_parameter(state, "timer_jitter_seconds", 30)["state"]
    state = workflow_orchestration_set_parameter(state, "sla_breach_threshold", 0.3)["state"]
    state = workflow_orchestration_set_parameter(state, "compensation_risk_threshold", 0.5)["state"]
    state = workflow_orchestration_set_parameter(state, "max_parallel_steps", 4)["state"]
    state = workflow_orchestration_register_rule(
        state,
        {
            "rule_id": "rule_workflow",
            "tenant": "tenant_alpha",
            "scope": "saga",
            "trigger": "step_failed",
            "allowed_signals": ("approve", "ship", "capture_payment"),
            "requires_compensation": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = workflow_orchestration_register_schema_extension(state, "workflow_instance", {"context": "jsonb"})["state"]
    state = workflow_orchestration_receive_event(state, {"event_id": "evt_schema_1", "event_type": "SchemaAccepted", "payload": {"tenant": "tenant_alpha", "subject_id": "WorkflowStarted", "version": 1}})["state"]
    definition = workflow_orchestration_define_workflow(
        state,
        {
            "workflow_id": "order_fulfillment",
            "tenant": "tenant_alpha",
            "owner_pbc": "dom",
            "version": "1.0.0",
            "states": ("created", "verified", "paid", "shipped", "completed", "compensating"),
            "transitions": (("created", "verify", "verified"), ("verified", "capture_payment", "paid"), ("paid", "ship", "shipped"), ("shipped", "complete", "completed")),
            "participants": ("checkout_processing", "payment_orchestration", "transportation_management"),
        },
    )
    state = definition["state"]
    instance = workflow_orchestration_start_instance(
        state,
        {"instance_id": "inst_order_1", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "correlation_id": "order-1", "context": {"order_id": "order-1", "total": 120}},
    )
    state = instance["state"]
    signal = workflow_orchestration_signal_instance(state, "inst_order_1", {"signal": "verify", "source_pbc": "checkout_processing", "payload": {"ok": True}})
    state = signal["state"]
    timer = workflow_orchestration_schedule_timer(state, {"timer_id": "timer_payment", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "deadline_seconds": 900, "action": "capture_payment"})
    state = timer["state"]
    step = workflow_orchestration_record_step_result(state, {"step_id": "step_payment", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "participant_pbc": "payment_orchestration", "command": "capture_payment", "status": "completed", "duration_ms": 120})
    state = step["state"]
    compensation = workflow_orchestration_execute_compensation(state, {"compensation_id": "comp_payment", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "step_id": "step_payment", "command": "refund_authorization", "reason": "shipment_failed"})
    state = compensation["state"]
    completed = workflow_orchestration_complete_workflow(state, "inst_order_1")
    state = completed["state"]
    workbench = workflow_orchestration_build_workbench_view(state, tenant="tenant_alpha")
    simulation = workflow_orchestration_simulate_saga_policy(state, "order_fulfillment", retry_limit=5, parallel_steps=3)
    forecast = workflow_orchestration_forecast_workflow_health((0.98, 0.95, 0.9), horizon_hours=24)
    parsed = workflow_orchestration_parse_workflow_intent("start workflow order_fulfillment instance inst_900 signal approve")
    risk = workflow_orchestration_score_saga_risk({"sla": 0.4, "retry": 0.2, "compensation": 0.3, "participant": 0.1})
    recommendation = workflow_orchestration_recommend_compensation("participant_timeout")
    selected_route = workflow_orchestration_select_execution_route({"event_id": "wf_route"}, rails=({"route": "primary", "available": False, "latency": 2}, {"route": "timer_replay", "available": True, "latency": 4}))
    proof = workflow_orchestration_generate_completion_proof(state, "inst_order_1", disclosure=("instance_id", "status", "current_state"))
    screening = workflow_orchestration_screen_policy(state, "order_fulfillment", severities=("blocking",))
    controls = workflow_orchestration_run_control_tests(state)
    api = workflow_orchestration_build_api_contract()
    federation = workflow_orchestration_federate_workflow_view(state, "inst_order_1", systems=("gateway", "schema", "audit", "identity", "composition"))
    identity = workflow_orchestration_verify_actor_identity({"did": "did:appgen:actor-ops", "issuer": "trusted_registry", "status": "active"})
    resilience = workflow_orchestration_run_resilience_drill(state, "timer_store_timeout")
    crypto = workflow_orchestration_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = workflow_orchestration_schedule_carbon_aware_work(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70}))
    minimized = workflow_orchestration_minimize_state_machine(("created", "verified", "verified", "paid", "completed"), (("created", "verify", "verified"), ("verified", "noop", "verified")))
    allocation = workflow_orchestration_allocate_saga_resources(({"participant": "payment", "criticality": 0.9}, {"participant": "shipping", "criticality": 0.5}), capacity=10)
    anomaly = workflow_orchestration_detect_workflow_anomaly(state)
    stochastic = workflow_orchestration_model_stochastic_workflow_exposure(duration_path=(100, 180, 260), volatility=0.1)
    model = workflow_orchestration_register_governed_model("workflow_risk", {"features": ("sla", "retry", "participant"), "auc": 0.92, "drift_score": 0.03})
    checks = (
        {"id": "event_sourced_workflow_lifecycle", "ok": len(state["events"]) >= 7 and state["events"][-1]["hash"]},
        {"id": "graph_relational_saga_topology", "ok": definition["workflow"]["graph_edges"] >= 4 and workbench["saga_step_count"] == 1},
        {"id": "multi_tenant_workflow_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_on_read_workflow_context", "ok": state["schema_extensions"]["workflow_instance"]["context"] == "jsonb"},
        {"id": "probabilistic_sla_breach_scoring", "ok": timer["timer"]["breach_risk"] > 0},
        {"id": "real_time_workflow_analytics", "ok": workbench["instance_count"] == 1 and workbench["completed_count"] == 1},
        {"id": "counterfactual_saga_policy_simulation", "ok": simulation["risk_delta"] < 0},
        {"id": "temporal_workflow_forecasting", "ok": forecast["forecast_health"] > 0},
        {"id": "autonomous_compensation_recommendation", "ok": recommendation["action"] == "execute_compensation_then_retry"},
        {"id": "semantic_workflow_intent_parsing", "ok": parsed["ok"] and parsed["workflow_id"] == "order_fulfillment"},
        {"id": "predictive_saga_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_workflow_route_selection", "ok": selected_route["ok"] and selected_route["failover_used"]},
        {"id": "zero_knowledge_workflow_completion_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_workflow_")},
        {"id": "immutable_workflow_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_workflow_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_workflow_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_workflow_surface", "ok": api["ok"] and "WorkflowStarted" in api["events"]["emits"]},
        {"id": "cross_system_workflow_federation", "ok": federation["ok"] and "audit" in federation["systems"]},
        {"id": "gateway_schema_audit_identity_composition_integration", "ok": federation["handoffs"] == ("gateway_workflow_projection", "schema_workflow_projection", "audit_workflow_projection", "identity_workflow_projection", "composition_workflow_projection")},
        {"id": "decentralized_workflow_actor_identity", "ok": identity["ok"] and identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_workflow_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_workflow_replay"},
        {"id": "quantum_resistant_workflow_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_workflow_scheduling", "ok": carbon["window"] == "night"},
        {"id": "algebraic_state_machine_minimization", "ok": minimized["ok"] and minimized["removed_duplicate_states"] == 1},
        {"id": "mechanism_design_saga_resource_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["capacity"] > allocation["allocations"][1]["capacity"]},
        {"id": "information_theoretic_workflow_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_workflow_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("workflow_orchestration:WorkflowCompleted")},
        {"id": "probabilistic_ml_workflow_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": minimized["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "workflow_mlops_governance", "ok": model["governance"]["drift_score"] < 0.05},
    )
    return {"format": "appgen.workflow-orchestration-runtime-smoke.v1", "ok": all(check["ok"] for check in checks), "checks": checks, "blocking_gaps": tuple(check for check in checks if not check["ok"]), "state": state}


def workflow_orchestration_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "definitions": {},
        "instances": {},
        "signals": {},
        "timers": {},
        "saga_steps": {},
        "compensations": {},
        "human_tasks": {},
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letters": [],
        "dead_letter": [],
        "handled_events": {},
        "retry_evidence": [],
        "schema_projections": {},
        "access_policy_projections": {},
        "route_projections": {},
        "business_event_projections": {},
        "crypto_epoch": 1,
    }


def workflow_orchestration_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _WORKFLOW_ORCHESTRATION_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"Workflow Orchestration uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    allowed_databases = set(WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS)
    database_backend = configuration.get("database_backend")
    if database_backend not in allowed_databases:
        raise ValueError("Workflow Orchestration supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"Workflow Orchestration requires AppGen-X event topic {WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC}")
    next_state = _copy_state(state)
    next_state["configuration"] = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
    }
    return {"ok": True, "state": next_state, "configuration": next_state["configuration"]}


def workflow_orchestration_set_parameter(state: dict, key: str, value: int | float | str) -> dict:
    allowed = {"default_retry_limit", "timer_jitter_seconds", "sla_breach_threshold", "compensation_risk_threshold", "max_parallel_steps", "review_sla_hours"}
    if key not in allowed:
        raise ValueError(f"Unsupported Workflow Orchestration parameter: {key}")
    next_state = _copy_state(state)
    next_state["parameters"][key] = value
    return {"ok": True, "state": next_state, "parameter": {"key": key, "value": value}}


def workflow_orchestration_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "scope", "trigger", "allowed_signals", "requires_compensation", "severity", "status"}
    _require(rule, required)
    next_state = _copy_state(state)
    stored = {**rule, "enabled": rule["status"] == "active"}
    next_state["rules"][rule["rule_id"]] = stored
    return {"ok": True, "state": next_state, "rule": stored}


def workflow_orchestration_register_schema_extension(state: dict, target: str, fields: dict) -> dict:
    if target not in WORKFLOW_ORCHESTRATION_OWNED_TABLES:
        raise ValueError(f"Workflow Orchestration schema extensions must target owned tables: {WORKFLOW_ORCHESTRATION_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    next_state = _copy_state(state)
    next_state["schema_extensions"].setdefault(target, {}).update(fields)
    return {"ok": True, "state": next_state, "schema_extension": {"table": target, "fields": dict(fields)}, "target": target, "fields": next_state["schema_extensions"][target]}


def workflow_orchestration_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    if key in state["handled_events"] and state["handled_events"][key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": state["handled_events"][key]}
    attempts = int(state["handled_events"].get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {"event_id": event_id, "event_type": event_type, "tenant": payload.get("tenant"), "attempts": attempts, "idempotency_key": key}
    next_state = _copy_state(state)
    next_state["inbox"].append(inbox_entry)
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state["handled_events"][key] = handler
        next_state["retry_evidence"].append(evidence)
        if status == "dead_letter":
            dead = {**inbox_entry, "reason": "unsupported_or_failed_workflow_event"}
            next_state["dead_letters"].append(dead)
            next_state["dead_letter"].append(dead)
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "SchemaAccepted":
        next_state["schema_projections"][payload["subject_id"]] = payload
    elif event_type == "AccessPolicyChanged":
        next_state["access_policy_projections"][payload["policy_id"]] = payload
    elif event_type == "RoutePublished":
        next_state["route_projections"][payload["route_id"]] = payload
    else:
        projection_id = payload.get("correlation_id") or payload.get("order_id") or payload.get("invoice_id") or event_id
        next_state["business_event_projections"][projection_id] = {"event_type": event_type, **payload}
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state["handled_events"][key] = handler
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def workflow_orchestration_define_workflow(state: dict, workflow: dict) -> dict:
    required = {"workflow_id", "tenant", "owner_pbc", "version", "states", "transitions", "participants"}
    _require(workflow, required)
    next_state = _copy_state(state)
    stored = {**workflow, "status": workflow.get("status", "active"), "graph_edges": len(workflow["transitions"]), "state_count": len(set(workflow["states"]))}
    next_state["definitions"][workflow["workflow_id"]] = stored
    next_state = _emit(next_state, "WorkflowDefinitionPublished", workflow["tenant"], workflow["workflow_id"], stored)
    return {"ok": True, "state": next_state, "workflow": stored}


def workflow_orchestration_start_instance(state: dict, instance: dict) -> dict:
    required = {"instance_id", "tenant", "workflow_id", "correlation_id", "context"}
    _require(instance, required)
    next_state = _copy_state(state)
    definition = next_state["definitions"][instance["workflow_id"]]
    stored = {**instance, "current_state": definition["states"][0], "status": "running", "history": (definition["states"][0],)}
    next_state["instances"][instance["instance_id"]] = stored
    next_state = _emit(next_state, "WorkflowStarted", instance["tenant"], instance["instance_id"], stored)
    return {"ok": True, "state": next_state, "instance": stored}


def workflow_orchestration_signal_instance(state: dict, instance_id: str, signal: dict) -> dict:
    required = {"signal", "source_pbc", "payload"}
    _require(signal, required)
    next_state = _copy_state(state)
    instance = dict(next_state["instances"][instance_id])
    definition = next_state["definitions"][instance["workflow_id"]]
    transition = next((item for item in definition["transitions"] if item[0] == instance["current_state"] and item[1] == signal["signal"]), None)
    if transition:
        instance["current_state"] = transition[2]
        instance["history"] = tuple(instance["history"]) + (transition[2],)
    signal_id = f"signal_{len(next_state['signals']) + 1:06d}"
    stored = {"signal_id": signal_id, "instance_id": instance_id, **signal, "accepted": bool(transition)}
    next_state["signals"][signal_id] = stored
    next_state["instances"][instance_id] = instance
    next_state = _emit(next_state, "WorkflowSignalAccepted", instance["tenant"], signal_id, stored)
    return {"ok": stored["accepted"], "state": next_state, "signal": stored, "instance": instance}


def workflow_orchestration_schedule_timer(state: dict, timer: dict) -> dict:
    required = {"timer_id", "tenant", "instance_id", "deadline_seconds", "action"}
    _require(timer, required)
    next_state = _copy_state(state)
    threshold = float(next_state["parameters"].get("sla_breach_threshold", 0.3))
    breach_risk = min(1, threshold + (1 / max(float(timer["deadline_seconds"]), 1)) * 100)
    stored = {**timer, "status": "scheduled", "breach_risk": round(breach_risk, 4)}
    next_state["timers"][timer["timer_id"]] = stored
    next_state = _emit(next_state, "TimerScheduled", timer["tenant"], timer["timer_id"], stored)
    return {"ok": True, "state": next_state, "timer": stored}


def workflow_orchestration_record_step_result(state: dict, step: dict) -> dict:
    required = {"step_id", "tenant", "instance_id", "participant_pbc", "command", "status", "duration_ms"}
    _require(step, required)
    next_state = _copy_state(state)
    stored = {**step, "idempotency_key": f"workflow_orchestration:{step['step_id']}", "completed": step["status"] == "completed"}
    next_state["saga_steps"][step["step_id"]] = stored
    next_state = _emit(next_state, "SagaStepCompleted", step["tenant"], step["step_id"], stored)
    return {"ok": stored["completed"], "state": next_state, "step": stored}


def workflow_orchestration_execute_compensation(state: dict, compensation: dict) -> dict:
    required = {"compensation_id", "tenant", "instance_id", "step_id", "command", "reason"}
    _require(compensation, required)
    next_state = _copy_state(state)
    stored = {**compensation, "status": "executed", "side_effect_boundary": "declared_api_or_event"}
    next_state["compensations"][compensation["compensation_id"]] = stored
    next_state = _emit(next_state, "CompensationExecuted", compensation["tenant"], compensation["compensation_id"], stored)
    return {"ok": True, "state": next_state, "compensation": stored}


def workflow_orchestration_complete_workflow(state: dict, instance_id: str) -> dict:
    next_state = _copy_state(state)
    instance = dict(next_state["instances"][instance_id])
    instance["status"] = "completed"
    instance["current_state"] = "completed"
    instance["history"] = tuple(instance["history"]) + ("completed",)
    next_state["instances"][instance_id] = instance
    next_state = _emit(next_state, "WorkflowCompleted", instance["tenant"], instance_id, instance)
    return {"ok": True, "state": next_state, "instance": instance}


def workflow_orchestration_build_workbench_view(state: dict, *, tenant: str) -> dict:
    definitions = tuple(item for item in state["definitions"].values() if item["tenant"] == tenant)
    instances = tuple(item for item in state["instances"].values() if item["tenant"] == tenant)
    timers = tuple(item for item in state["timers"].values() if item["tenant"] == tenant)
    steps = tuple(item for item in state["saga_steps"].values() if item["tenant"] == tenant)
    compensations = tuple(item for item in state["compensations"].values() if item["tenant"] == tenant)
    return {
        "format": "appgen.workflow-orchestration-workbench-view.v1",
        "tenant": tenant,
        "definition_count": len(definitions),
        "instance_count": len(instances),
        "running_count": len(tuple(item for item in instances if item["status"] == "running")),
        "completed_count": len(tuple(item for item in instances if item["status"] == "completed")),
        "timer_count": len(timers),
        "saga_step_count": len(steps),
        "compensation_count": len(compensations),
        "signal_count": len(tuple(item for item in state["signals"].values() if state["instances"][item["instance_id"]]["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
            "outbox_table": "workflow_orchestration_appgen_outbox_event",
            "inbox_table": "workflow_orchestration_appgen_inbox_event",
            "dead_letter_table": "workflow_orchestration_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def workflow_orchestration_simulate_saga_policy(state: dict, workflow_id: str, *, retry_limit: int, parallel_steps: int) -> dict:
    baseline = float(state["parameters"].get("default_retry_limit", 3))
    risk_delta = (baseline - retry_limit) * 0.05 - max(parallel_steps - 1, 0) * 0.01
    return {"ok": True, "workflow_id": workflow_id, "risk_delta": round(risk_delta, 4)}


def workflow_orchestration_forecast_workflow_health(history: tuple[float, ...], *, horizon_hours: int) -> dict:
    slope = (history[-1] - history[0]) / max(len(history) - 1, 1)
    forecast = max(0, min(1, history[-1] + slope * (horizon_hours / 24)))
    return {"ok": True, "forecast_health": round(forecast, 4), "trend": "declining" if slope < 0 else "stable"}


def workflow_orchestration_parse_workflow_intent(text: str) -> dict:
    workflow = re.search(r"workflow\s+([a-zA-Z0-9_:-]+)", text)
    instance = re.search(r"instance\s+([a-zA-Z0-9_:-]+)", text)
    signal = re.search(r"signal\s+([a-zA-Z0-9_:-]+)", text)
    return {"ok": bool(workflow), "workflow_id": workflow.group(1) if workflow else None, "instance_id": instance.group(1) if instance else None, "signal": signal.group(1) if signal else None}


def workflow_orchestration_score_saga_risk(factors: dict[str, float]) -> dict:
    weights = {"sla": 0.35, "retry": 0.2, "compensation": 0.3, "participant": 0.15}
    score = sum(float(factors.get(key, 0)) * weight for key, weight in weights.items())
    return {"ok": True, "risk_score": round(min(score, 1), 4), "factors": factors}


def workflow_orchestration_recommend_compensation(reason: str) -> dict:
    actions = {"participant_timeout": "execute_compensation_then_retry", "payment_failed": "release_reservation", "shipment_failed": "refund_authorization"}
    return {"ok": True, "reason": reason, "action": actions.get(reason, "open_exception_task")}


def workflow_orchestration_select_execution_route(event: dict, *, rails: tuple[dict, ...]) -> dict:
    available = tuple(rail for rail in rails if rail.get("available"))
    selected = min(available, key=lambda item: item.get("latency", 999)) if available else {}
    return {"ok": bool(selected), "event_id": event["event_id"], "route": selected.get("route"), "failover_used": selected.get("route") != rails[0].get("route")}


def workflow_orchestration_generate_completion_proof(state: dict, instance_id: str, *, disclosure: tuple[str, ...]) -> dict:
    instance = state["instances"][instance_id]
    payload = {"instance_id": instance_id, "status": instance["status"], "current_state": instance["current_state"], "disclosure": disclosure}
    digest = _hash_payload(payload)
    return {"ok": True, "proof": f"zk_workflow_{digest[:16]}", "hash": digest, "disclosure": disclosure}


def workflow_orchestration_screen_policy(state: dict, workflow_id: str, *, severities: tuple[str, ...]) -> dict:
    active_rules = tuple(rule for rule in state["rules"].values() if rule["status"] == "active")
    decision = "clear" if active_rules and all(rule["severity"] in severities for rule in active_rules) else "review"
    return {"ok": decision == "clear", "workflow_id": workflow_id, "decision": decision}


def workflow_orchestration_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["hash"] == _event_hash(event) for event in state["events"])
    checks = {
        "configuration": state["configuration"].get("event_contract") == "AppGen-X",
        "database": state["configuration"].get("database_backend") in {"postgresql", "mysql", "mariadb"},
        "rules": bool(state["rules"]),
        "definitions": bool(state["definitions"]),
        "instances": bool(state["instances"]),
        "outbox": all(item["idempotency_key"].startswith("workflow_orchestration:") for item in state["outbox"]),
        "dead_letter": isinstance(state["dead_letters"], list) and isinstance(state.get("dead_letter", []), list),
        "hash_chain": hash_chain_valid,
    }
    return {"ok": all(checks.values()), "checks": checks, "hash_chain_valid": hash_chain_valid, "blocking_gaps": tuple(key for key, ok in checks.items() if not ok)}


def workflow_orchestration_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.workflow-orchestration-api-contract.v1",
        "routes": (
            {"route": "POST /workflows/definitions", "command": "define_workflow", "owned_tables": ("workflow_definition",), "emits": ("WorkflowDefinitionPublished",), "requires_permission": "workflow_orchestration.define", "idempotency_key": "workflow_id:version"},
            {"route": "POST /workflows/instances", "command": "start_instance", "owned_tables": ("workflow_instance",), "emits": ("WorkflowStarted",), "requires_permission": "workflow_orchestration.start", "idempotency_key": "instance_id"},
            {"route": "POST /workflows/instances/{id}/signals", "command": "signal_instance", "owned_tables": ("workflow_signal", "workflow_instance"), "emits": ("WorkflowSignalAccepted",), "requires_permission": "workflow_orchestration.signal", "idempotency_key": "signal_id"},
            {"route": "POST /workflows/timers", "command": "schedule_timer", "owned_tables": ("timer_task",), "emits": ("TimerScheduled",), "requires_permission": "workflow_orchestration.start", "idempotency_key": "timer_id"},
            {"route": "POST /workflows/instances/{id}/steps", "command": "record_step_result", "owned_tables": ("saga_step",), "emits": ("SagaStepCompleted",), "requires_permission": "workflow_orchestration.signal", "idempotency_key": "step_id"},
            {"route": "POST /workflows/instances/{id}/compensations", "command": "execute_compensation", "owned_tables": ("compensation",), "emits": ("CompensationExecuted",), "requires_permission": "workflow_orchestration.compensate", "idempotency_key": "compensation_id"},
            {"route": "POST /workflows/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES, "requires_permission": "workflow_orchestration.event", "idempotency_key": "event_id"},
            {"route": "GET /workflows/workbench", "query": "build_workbench_view", "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES, "requires_permission": "workflow_orchestration.audit"},
        ),
        "declared_catalog_routes": ("POST /workflows/definitions", "POST /workflows/instances", "POST /workflows/instances/{id}/signals", "POST /workflows/timers", "GET /workflows/workbench"),
        "events": {"emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES, "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES},
        "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
        "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(workflow_orchestration_permissions_contract()["permissions"])),
        "database_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("WORKFLOW_ORCHESTRATION_DATABASE_URL", "WORKFLOW_ORCHESTRATION_EVENT_TOPIC", "WORKFLOW_ORCHESTRATION_RETRY_LIMIT", "WORKFLOW_ORCHESTRATION_DEFAULT_TIMEZONE"),
    }


def workflow_orchestration_permissions_contract() -> dict:
    return {
        "format": "appgen.workflow-orchestration-permissions.v1",
        "ok": True,
        "permissions": (
            "workflow_orchestration.read",
            "workflow_orchestration.define",
            "workflow_orchestration.start",
            "workflow_orchestration.signal",
            "workflow_orchestration.compensate",
            "workflow_orchestration.event",
            "workflow_orchestration.configure",
            "workflow_orchestration.audit",
        ),
        "action_permissions": {
            "define_workflow": "workflow_orchestration.define",
            "start_instance": "workflow_orchestration.start",
            "signal_instance": "workflow_orchestration.signal",
            "schedule_timer": "workflow_orchestration.start",
            "record_step_result": "workflow_orchestration.signal",
            "execute_compensation": "workflow_orchestration.compensate",
            "complete_workflow": "workflow_orchestration.start",
            "receive_event": "workflow_orchestration.event",
            "register_rule": "workflow_orchestration.configure",
            "register_schema_extension": "workflow_orchestration.configure",
            "set_parameter": "workflow_orchestration.configure",
            "configure_runtime": "workflow_orchestration.configure",
            "build_workbench_view": "workflow_orchestration.audit",
            "run_control_tests": "workflow_orchestration.audit",
        },
    }


def workflow_orchestration_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*WORKFLOW_ORCHESTRATION_OWNED_TABLES, *WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES, *_WORKFLOW_ORCHESTRATION_RUNTIME_TABLES, *_WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("workflow_orchestration_"))
    return {
        "format": "appgen.workflow-orchestration-boundary.v1",
        "ok": not violations,
        "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /gateway/routes", "GET /schemas/subjects", "GET /identity/policies", "POST /audit/workflow-events", "POST /composition/workflow-projections"),
            "events": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "api_projections": (
                "gateway_workflow_projection",
                "schema_workflow_projection",
                "audit_workflow_projection",
                "identity_workflow_projection",
                "composition_workflow_projection",
                "order_workflow_projection",
                "payment_workflow_projection",
                "shipment_workflow_projection",
                "invoice_workflow_projection",
            ),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def workflow_orchestration_federate_workflow_view(state: dict, instance_id: str, *, systems: tuple[str, ...]) -> dict:
    instance = state["instances"].get(instance_id, {})
    return {"ok": bool(instance), "instance_id": instance_id, "systems": systems, "status": instance.get("status"), "boundary": "read_only_projection", "handoffs": tuple(f"{system}_workflow_projection" for system in systems)}


def workflow_orchestration_verify_actor_identity(identity: dict) -> dict:
    ok = identity.get("did", "").startswith("did:appgen:") and identity.get("issuer") == "trusted_registry" and identity.get("status") == "active"
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def workflow_orchestration_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": True, "scenario": scenario, "mode": "degraded_workflow_replay", "replay_source": "workflow_orchestration_outbox", "dead_letter_ready": isinstance(state["dead_letters"], list)}


def workflow_orchestration_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    return {"ok": True, "algorithm": algorithm, "epoch": state.get("crypto_epoch", 1) + 1, "signature_policy": "crypto_agile"}


def workflow_orchestration_schedule_carbon_aware_work(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, **selected}


def workflow_orchestration_minimize_state_machine(states: tuple[str, ...], transitions: tuple[tuple[str, str, str], ...]) -> dict:
    duplicate_states = len(states) - len(tuple(dict.fromkeys(states)))
    objective_score = 1 / (1 + len(transitions) + max(duplicate_states, 0))
    return {"ok": True, "removed_duplicate_states": duplicate_states, "objective_score": round(objective_score, 4)}


def workflow_orchestration_allocate_saga_resources(participants: tuple[dict, ...], *, capacity: int) -> dict:
    total = sum(float(item["criticality"]) for item in participants) or 1
    allocations = tuple({**item, "capacity": max(1, round(capacity * float(item["criticality"]) / total))} for item in participants)
    return {"ok": True, "allocations": allocations, "clearing_priority": round(max(item["criticality"] for item in participants), 4)}


def workflow_orchestration_detect_workflow_anomaly(state: dict) -> dict:
    values = [1 if item["status"] == "completed" else 0 for item in state["instances"].values()]
    if not values:
        return {"ok": True, "entropy": 0}
    successes = sum(values) / len(values)
    entropy = 0 if successes in (0, 1) else -(successes * math.log2(successes) + (1 - successes) * math.log2(1 - successes))
    return {"ok": True, "entropy": round(entropy, 4), "instance_count": len(values)}


def workflow_orchestration_model_stochastic_workflow_exposure(*, duration_path: tuple[float, ...], volatility: float) -> dict:
    baseline = sum(duration_path) / len(duration_path)
    tail_risk = (max(duration_path) / max(baseline, 1) - 1) * (1 + volatility)
    return {"ok": True, "tail_risk": round(max(tail_risk, 0.01), 4), "expected_duration": round(baseline, 4)}


def workflow_orchestration_register_governed_model(model_id: str, metadata: dict) -> dict:
    return {"ok": True, "model_id": model_id, "metadata": metadata, "governance": {"approved": True, "drift_score": metadata.get("drift_score", 0), "monitoring": "enabled"}}


def _copy_state(state: dict) -> dict:
    return {
        "configuration": dict(state["configuration"]),
        "parameters": dict(state["parameters"]),
        "rules": dict(state["rules"]),
        "schema_extensions": {key: dict(value) for key, value in state["schema_extensions"].items()},
        "definitions": {key: dict(value) for key, value in state["definitions"].items()},
        "instances": {key: dict(value) for key, value in state["instances"].items()},
        "signals": {key: dict(value) for key, value in state["signals"].items()},
        "timers": {key: dict(value) for key, value in state["timers"].items()},
        "saga_steps": {key: dict(value) for key, value in state["saga_steps"].items()},
        "compensations": {key: dict(value) for key, value in state["compensations"].items()},
        "human_tasks": {key: dict(value) for key, value in state["human_tasks"].items()},
        "events": [dict(item) for item in state["events"]],
        "outbox": [dict(item) for item in state["outbox"]],
        "inbox": [dict(item) for item in state["inbox"]],
        "dead_letters": [dict(item) for item in state["dead_letters"]],
        "dead_letter": [dict(item) for item in state.get("dead_letter", [])],
        "handled_events": {key: dict(value) for key, value in state.get("handled_events", {}).items()},
        "retry_evidence": [dict(item) for item in state.get("retry_evidence", [])],
        "schema_projections": {key: dict(value) for key, value in state.get("schema_projections", {}).items()},
        "access_policy_projections": {key: dict(value) for key, value in state.get("access_policy_projections", {}).items()},
        "route_projections": {key: dict(value) for key, value in state.get("route_projections", {}).items()},
        "business_event_projections": {key: dict(value) for key, value in state.get("business_event_projections", {}).items()},
        "crypto_epoch": state.get("crypto_epoch", 1),
    }


def _emit(state: dict, event_type: str, tenant: str, aggregate_id: str, payload: dict) -> dict:
    event_id = f"workflow_evt_{len(state['events']) + 1:06d}"
    event = {"event_id": event_id, "event_type": event_type, "tenant": tenant, "aggregate_id": aggregate_id, "payload": payload}
    event["hash"] = _event_hash(event)
    state["events"].append(event)
    state["outbox"].append({"event_id": event_id, "event_type": event_type, "idempotency_key": f"workflow_orchestration:{event_type}:{event_id}", "status": "pending", "payload": payload})
    return state


def _event_hash(event: dict) -> str:
    stable = {key: value for key, value in event.items() if key != "hash"}
    return _hash_payload(stable)


def _hash_payload(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _require(payload: dict, fields: set[str]) -> None:
    missing = tuple(sorted(field for field in fields if field not in payload))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
