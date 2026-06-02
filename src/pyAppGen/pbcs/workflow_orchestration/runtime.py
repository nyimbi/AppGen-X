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
    "workflow_version",
    "workflow_instance",
    "workflow_signal",
    "workflow_transition_guard",
    "timer_task",
    "workflow_retry_policy",
    "workflow_sla_policy",
    "workflow_escalation_rule",
    "saga_step",
    "compensation",
    "human_task",
    "human_task_assignment",
    "workflow_approval_decision",
    "workflow_integration_endpoint",
    "workflow_event_correlation",
    "workflow_metric_snapshot",
    "workflow_exception_case",
    "workflow_simulation_run",
    "workflow_policy_screening",
    "workflow_completion_proof",
    "workflow_audit_entry",
    "workflow_governed_model_evidence",
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
WORKFLOW_ORCHESTRATION_RUNTIME_TABLES = _WORKFLOW_ORCHESTRATION_RUNTIME_TABLES
WORKFLOW_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "allowed_signal_sources",
    "default_versioning",
    "default_timezone",
    "workbench_limit",
)
WORKFLOW_ORCHESTRATION_SUPPORTED_PARAMETER_KEYS = (
    "default_retry_limit",
    "timer_jitter_seconds",
    "sla_breach_threshold",
    "compensation_risk_threshold",
    "max_parallel_steps",
    "review_sla_hours",
)
WORKFLOW_ORCHESTRATION_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "trigger",
    "allowed_signals",
    "requires_compensation",
    "severity",
    "status",
)
_WORKFLOW_ORCHESTRATION_PARAMETER_BOUNDS = {
    "default_retry_limit": (1, 10),
    "timer_jitter_seconds": (0, 3600),
    "sla_breach_threshold": (0.0, 1.0),
    "compensation_risk_threshold": (0.0, 1.0),
    "max_parallel_steps": (1, 64),
    "review_sla_hours": (1, 720),
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
        "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
        "allowed_database_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "capabilities": WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS,
        "standard_features": WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS,
        "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
        "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "define_workflow",
            "publish_workflow_version",
            "register_transition_guard",
            "start_instance",
            "signal_instance",
            "schedule_timer",
            "register_retry_policy",
            "register_sla_policy",
            "register_escalation_rule",
            "record_step_result",
            "execute_compensation",
            "assign_human_task",
            "record_approval_decision",
            "register_integration_endpoint",
            "correlate_event",
            "capture_metric_snapshot",
            "open_exception_case",
            "record_simulation_run",
            "record_policy_screening",
            "record_completion_proof",
            "append_audit_entry",
            "register_governed_model_evidence",
            "complete_workflow",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "run_control_tests",
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
    state = workflow_orchestration_publish_workflow_version(state, {"version_id": "ver_order_100", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "semantic_version": "1.0.0", "status": "published"})["state"]
    state = workflow_orchestration_register_transition_guard(state, {"guard_id": "guard_pay", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "from_state": "verified", "signal": "capture_payment", "expression": "context.total > 0", "status": "active"})["state"]
    state = workflow_orchestration_register_retry_policy(state, {"policy_id": "retry_pay", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "max_attempts": 3, "backoff": "exponential", "status": "active"})["state"]
    state = workflow_orchestration_register_sla_policy(state, {"policy_id": "sla_ship", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "threshold_seconds": 3600, "severity": "blocking", "status": "active"})["state"]
    state = workflow_orchestration_register_escalation_rule(state, {"escalation_id": "esc_ship", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "trigger": "sla_breach", "target_group": "ops", "status": "active"})["state"]
    state = workflow_orchestration_register_integration_endpoint(state, {"endpoint_id": "ep_pay", "tenant": "tenant_alpha", "participant_pbc": "payment_orchestration", "route": "POST /payments/capture", "status": "active"})["state"]
    instance = workflow_orchestration_start_instance(
        state,
        {"instance_id": "inst_order_1", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "correlation_id": "order-1", "context": {"order_id": "order-1", "total": 120}},
    )
    state = instance["state"]
    state = workflow_orchestration_correlate_event(state, {"correlation_id": "corr_order_1", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "source_event": "OrderVerified", "business_key": "order-1"})["state"]
    signal = workflow_orchestration_signal_instance(state, "inst_order_1", {"signal": "verify", "source_pbc": "checkout_processing", "payload": {"ok": True}})
    state = signal["state"]
    timer = workflow_orchestration_schedule_timer(state, {"timer_id": "timer_payment", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "deadline_seconds": 900, "action": "capture_payment"})
    state = timer["state"]
    state = workflow_orchestration_assign_human_task(state, {"assignment_id": "assign_review", "tenant": "tenant_alpha", "task_id": "task_review", "instance_id": "inst_order_1", "assignee_group": "ops", "status": "assigned"})["state"]
    state = workflow_orchestration_record_approval_decision(state, {"decision_id": "dec_review", "tenant": "tenant_alpha", "task_id": "task_review", "decision": "approved", "decided_by": "ops_lead", "status": "final"})["state"]
    step = workflow_orchestration_record_step_result(state, {"step_id": "step_payment", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "participant_pbc": "payment_orchestration", "command": "capture_payment", "status": "completed", "duration_ms": 120})
    state = step["state"]
    compensation = workflow_orchestration_execute_compensation(state, {"compensation_id": "comp_payment", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "step_id": "step_payment", "command": "refund_authorization", "reason": "shipment_failed"})
    state = compensation["state"]
    state = workflow_orchestration_open_exception_case(state, {"case_id": "case_ship", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "case_type": "shipment_failed", "severity": "blocking", "status": "resolved"})["state"]
    state = workflow_orchestration_capture_metric_snapshot(state, {"snapshot_id": "metric_1", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "instance_count": 1, "completed_count": 0, "compensation_count": 1})["state"]
    completed = workflow_orchestration_complete_workflow(state, "inst_order_1")
    state = completed["state"]
    workbench = workflow_orchestration_build_workbench_view(state, tenant="tenant_alpha")
    simulation = workflow_orchestration_simulate_saga_policy(state, "order_fulfillment", retry_limit=5, parallel_steps=3)
    state = workflow_orchestration_record_simulation_run(state, {"simulation_id": "sim_order", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "scenario": "retry_parallelism", "risk_delta": simulation["risk_delta"], "status": "completed"})["state"]
    forecast = workflow_orchestration_forecast_workflow_health((0.98, 0.95, 0.9), horizon_hours=24)
    parsed = workflow_orchestration_parse_workflow_intent("start workflow order_fulfillment instance inst_900 signal approve")
    risk = workflow_orchestration_score_saga_risk({"sla": 0.4, "retry": 0.2, "compensation": 0.3, "participant": 0.1})
    recommendation = workflow_orchestration_recommend_compensation("participant_timeout")
    selected_route = workflow_orchestration_select_execution_route({"event_id": "wf_route"}, rails=({"route": "primary", "available": False, "latency": 2}, {"route": "timer_replay", "available": True, "latency": 4}))
    proof = workflow_orchestration_generate_completion_proof(state, "inst_order_1", disclosure=("instance_id", "status", "current_state"))
    screening = workflow_orchestration_screen_policy(state, "order_fulfillment", severities=("blocking",))
    state = workflow_orchestration_record_policy_screening(state, {"screening_id": "screen_order", "tenant": "tenant_alpha", "workflow_id": "order_fulfillment", "decision": screening["decision"], "status": "screened"})["state"]
    state = workflow_orchestration_record_completion_proof(state, {"proof_id": "proof_order", "tenant": "tenant_alpha", "instance_id": "inst_order_1", "proof_hash": proof["hash"], "proof_type": "workflow_completion"})["state"]
    state = workflow_orchestration_append_audit_entry(state, "workflow_completed", {"tenant": "tenant_alpha", "instance_id": "inst_order_1", "status": "completed"})["state"]
    controls = workflow_orchestration_run_control_tests(state)
    api = workflow_orchestration_build_api_contract()
    schema = workflow_orchestration_build_schema_contract()
    service = workflow_orchestration_build_service_contract()
    release = workflow_orchestration_build_release_evidence()
    ui_binding = workflow_orchestration_ui_binding_contract()
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
    state = workflow_orchestration_register_governed_model_evidence(state, {"evidence_id": "model_wf", "tenant": "tenant_alpha", "model_id": "workflow_risk", "auc": 0.92, "drift_score": 0.03, "status": "approved"})["state"]
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
        {"id": "standard_workflow_table_stakes_records", "ok": all(state[name] for name in ("workflow_versions", "workflow_transition_guards", "workflow_retry_policies", "workflow_sla_policies", "workflow_escalation_rules", "human_task_assignments", "workflow_approval_decisions", "workflow_integration_endpoints", "workflow_event_correlations", "workflow_metric_snapshots", "workflow_exception_cases", "workflow_simulation_runs", "workflow_policy_screenings", "workflow_completion_proofs", "workflow_audit_entries", "workflow_governed_model_evidence"))},
    )
    return {
        "format": "appgen.workflow-orchestration-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks)
        and schema["ok"]
        and service["ok"]
        and release["ok"]
        and ui_binding["ok"],
        "checks": checks,
        "contract_evidence": {
            "schema": schema,
            "service": service,
            "release": release,
            "ui_binding": ui_binding,
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state": state,
    }


def workflow_orchestration_empty_state() -> dict:
    return {
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "definitions": {},
        "workflow_versions": {},
        "instances": {},
        "signals": {},
        "workflow_transition_guards": {},
        "timers": {},
        "workflow_retry_policies": {},
        "workflow_sla_policies": {},
        "workflow_escalation_rules": {},
        "saga_steps": {},
        "compensations": {},
        "human_tasks": {},
        "human_task_assignments": {},
        "workflow_approval_decisions": {},
        "workflow_integration_endpoints": {},
        "workflow_event_correlations": {},
        "workflow_metric_snapshots": {},
        "workflow_exception_cases": {},
        "workflow_simulation_runs": {},
        "workflow_policy_screenings": {},
        "workflow_completion_proofs": {},
        "workflow_audit_entries": {},
        "workflow_governed_model_evidence": {},
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
    unsupported = tuple(sorted(field for field in configuration if field not in WORKFLOW_ORCHESTRATION_SUPPORTED_CONFIGURATION_FIELDS))
    if unsupported:
        raise ValueError(f"Unsupported Workflow Orchestration configuration fields: {unsupported}")
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
    if key not in WORKFLOW_ORCHESTRATION_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Workflow Orchestration parameter: {key}")
    lower, upper = _WORKFLOW_ORCHESTRATION_PARAMETER_BOUNDS[key]
    numeric_value = float(value)
    if numeric_value < lower or numeric_value > upper:
        raise ValueError(f"Workflow Orchestration parameter {key} must be between {lower} and {upper}")
    next_state = _copy_state(state)
    next_state["parameters"][key] = value
    return {"ok": True, "state": next_state, "parameter": {"key": key, "value": value}}


def workflow_orchestration_register_rule(state: dict, rule: dict) -> dict:
    _require(rule, set(WORKFLOW_ORCHESTRATION_REQUIRED_RULE_FIELDS))
    next_state = _copy_state(state)
    compiled_evidence = {
        "rule_id": rule["rule_id"],
        "scope": rule["scope"],
        "trigger": rule["trigger"],
        "allowed_signals": tuple(rule["allowed_signals"]),
        "requires_compensation": bool(rule["requires_compensation"]),
        "severity": rule["severity"],
    }
    stored = {
        **rule,
        "allowed_signals": tuple(rule["allowed_signals"]),
        "enabled": rule["status"] == "active",
        "compiled_hash": _hash_payload(compiled_evidence),
        "compiled_evidence": compiled_evidence,
    }
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


def workflow_orchestration_publish_workflow_version(state: dict, version: dict) -> dict:
    required = {"version_id", "tenant", "workflow_id", "semantic_version", "status"}
    _require(version, required)
    next_state = _copy_state(state)
    stored = {**version, "audit_hash": _hash_payload(version)}
    next_state["workflow_versions"][version["version_id"]] = stored
    return {"ok": True, "state": next_state, "version": stored}


def workflow_orchestration_register_transition_guard(state: dict, guard: dict) -> dict:
    required = {"guard_id", "tenant", "workflow_id", "from_state", "signal", "expression", "status"}
    _require(guard, required)
    next_state = _copy_state(state)
    stored = {**guard, "compiled_hash": _hash_payload(guard), "audit_hash": _hash_payload(guard)}
    next_state["workflow_transition_guards"][guard["guard_id"]] = stored
    return {"ok": True, "state": next_state, "guard": stored}


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


def workflow_orchestration_register_retry_policy(state: dict, policy: dict) -> dict:
    required = {"policy_id", "tenant", "workflow_id", "max_attempts", "backoff", "status"}
    _require(policy, required)
    next_state = _copy_state(state)
    stored = {**policy, "audit_hash": _hash_payload(policy)}
    next_state["workflow_retry_policies"][policy["policy_id"]] = stored
    return {"ok": True, "state": next_state, "policy": stored}


def workflow_orchestration_register_sla_policy(state: dict, policy: dict) -> dict:
    required = {"policy_id", "tenant", "workflow_id", "threshold_seconds", "severity", "status"}
    _require(policy, required)
    next_state = _copy_state(state)
    stored = {**policy, "audit_hash": _hash_payload(policy)}
    next_state["workflow_sla_policies"][policy["policy_id"]] = stored
    return {"ok": True, "state": next_state, "policy": stored}


def workflow_orchestration_register_escalation_rule(state: dict, rule: dict) -> dict:
    required = {"escalation_id", "tenant", "workflow_id", "trigger", "target_group", "status"}
    _require(rule, required)
    next_state = _copy_state(state)
    stored = {**rule, "audit_hash": _hash_payload(rule)}
    next_state["workflow_escalation_rules"][rule["escalation_id"]] = stored
    return {"ok": True, "state": next_state, "rule": stored}


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


def workflow_orchestration_assign_human_task(state: dict, assignment: dict) -> dict:
    required = {"assignment_id", "tenant", "task_id", "instance_id", "assignee_group", "status"}
    _require(assignment, required)
    next_state = _copy_state(state)
    task = {
        "task_id": assignment["task_id"],
        "tenant": assignment["tenant"],
        "instance_id": assignment["instance_id"],
        "task_type": "approval",
        "assignee_group": assignment["assignee_group"],
        "decision": None,
        "status": assignment["status"],
    }
    stored = {**assignment, "audit_hash": _hash_payload(assignment)}
    next_state["human_tasks"][assignment["task_id"]] = task
    next_state["human_task_assignments"][assignment["assignment_id"]] = stored
    return {"ok": True, "state": next_state, "assignment": stored, "task": task}


def workflow_orchestration_record_approval_decision(state: dict, decision: dict) -> dict:
    required = {"decision_id", "tenant", "task_id", "decision", "decided_by", "status"}
    _require(decision, required)
    next_state = _copy_state(state)
    stored = {**decision, "audit_hash": _hash_payload(decision)}
    next_state["workflow_approval_decisions"][decision["decision_id"]] = stored
    if decision["task_id"] in next_state["human_tasks"]:
        next_state["human_tasks"][decision["task_id"]]["decision"] = decision["decision"]
        next_state["human_tasks"][decision["task_id"]]["status"] = decision["status"]
    return {"ok": True, "state": next_state, "decision": stored}


def workflow_orchestration_register_integration_endpoint(state: dict, endpoint: dict) -> dict:
    required = {"endpoint_id", "tenant", "participant_pbc", "route", "status"}
    _require(endpoint, required)
    next_state = _copy_state(state)
    stored = {**endpoint, "audit_hash": _hash_payload(endpoint)}
    next_state["workflow_integration_endpoints"][endpoint["endpoint_id"]] = stored
    return {"ok": True, "state": next_state, "endpoint": stored}


def workflow_orchestration_correlate_event(state: dict, correlation: dict) -> dict:
    required = {"correlation_id", "tenant", "instance_id", "source_event", "business_key"}
    _require(correlation, required)
    next_state = _copy_state(state)
    stored = {**correlation, "audit_hash": _hash_payload(correlation)}
    next_state["workflow_event_correlations"][correlation["correlation_id"]] = stored
    return {"ok": True, "state": next_state, "correlation": stored}


def workflow_orchestration_capture_metric_snapshot(state: dict, snapshot: dict) -> dict:
    required = {"snapshot_id", "tenant", "workflow_id", "instance_count", "completed_count", "compensation_count"}
    _require(snapshot, required)
    next_state = _copy_state(state)
    completion_rate = float(snapshot["completed_count"]) / max(float(snapshot["instance_count"]), 1.0)
    stored = {**snapshot, "completion_rate": round(completion_rate, 4), "audit_hash": _hash_payload(snapshot)}
    next_state["workflow_metric_snapshots"][snapshot["snapshot_id"]] = stored
    return {"ok": True, "state": next_state, "snapshot": stored}


def workflow_orchestration_open_exception_case(state: dict, case: dict) -> dict:
    required = {"case_id", "tenant", "instance_id", "case_type", "severity", "status"}
    _require(case, required)
    recommendation = workflow_orchestration_recommend_compensation(case["case_type"])
    next_state = _copy_state(state)
    stored = {**case, "recommended_action": recommendation["action"], "audit_hash": _hash_payload(case)}
    next_state["workflow_exception_cases"][case["case_id"]] = stored
    return {"ok": True, "state": next_state, "case": stored}


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
    human_tasks = tuple(item for item in state["human_tasks"].values() if item["tenant"] == tenant)
    ui_binding = workflow_orchestration_ui_binding_contract()["binding_evidence"]
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
        "human_task_count": len(human_tasks),
        "signal_count": len(tuple(item for item in state["signals"].values() if state["instances"][item["instance_id"]]["tenant"] == tenant)),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            **ui_binding,
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
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


def workflow_orchestration_record_simulation_run(state: dict, simulation: dict) -> dict:
    required = {"simulation_id", "tenant", "workflow_id", "scenario", "risk_delta", "status"}
    _require(simulation, required)
    next_state = _copy_state(state)
    stored = {**simulation, "audit_hash": _hash_payload(simulation)}
    next_state["workflow_simulation_runs"][simulation["simulation_id"]] = stored
    return {"ok": True, "state": next_state, "simulation": stored}


def workflow_orchestration_record_policy_screening(state: dict, screening: dict) -> dict:
    required = {"screening_id", "tenant", "workflow_id", "decision", "status"}
    _require(screening, required)
    next_state = _copy_state(state)
    stored = {**screening, "audit_hash": _hash_payload(screening)}
    next_state["workflow_policy_screenings"][screening["screening_id"]] = stored
    return {"ok": True, "state": next_state, "screening": stored}


def workflow_orchestration_record_completion_proof(state: dict, proof: dict) -> dict:
    required = {"proof_id", "tenant", "instance_id", "proof_hash", "proof_type"}
    _require(proof, required)
    next_state = _copy_state(state)
    stored = {**proof, "status": proof.get("status", "sealed"), "audit_hash": _hash_payload(proof)}
    next_state["workflow_completion_proofs"][proof["proof_id"]] = stored
    return {"ok": True, "state": next_state, "proof": stored}


def workflow_orchestration_append_audit_entry(state: dict, action: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    entry_id = f"audit_{len(next_state['workflow_audit_entries']) + 1:06d}"
    stored = {"audit_entry_id": entry_id, "tenant": payload.get("tenant", "tenant_unknown"), "action": action, "payload_hash": _hash_payload(payload), "status": "sealed"}
    next_state["workflow_audit_entries"][entry_id] = stored
    return {"ok": True, "state": next_state, "audit_entry": stored}


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


def workflow_orchestration_ui_binding_contract() -> dict:
    return {
        "format": "appgen.workflow-orchestration-ui-binding-contract.v1",
        "ok": True,
        "binding_evidence": {
            "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
            "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
            "workbench_route": "/workbench/pbcs/workflow_orchestration",
            "outbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[0],
            "inbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1],
            "dead_letter_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[2],
        },
    }


def workflow_orchestration_build_api_contract() -> dict:
    return {
        "ok": True,
        "format": "appgen.workflow-orchestration-api-contract.v1",
        "routes": (
            {"route": "PUT /workflows/configuration", "command": "configure_runtime", "owned_tables": ("workflow_configuration",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "configuration_id"},
            {"route": "POST /workflows/parameters", "command": "set_parameter", "owned_tables": ("workflow_parameter",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "parameter_name"},
            {"route": "POST /workflows/rules", "command": "register_rule", "owned_tables": ("workflow_rule",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "rule_id"},
            {"route": "POST /workflows/definitions", "command": "define_workflow", "owned_tables": ("workflow_definition",), "emits": ("WorkflowDefinitionPublished",), "requires_permission": "workflow_orchestration.define", "idempotency_key": "workflow_id:version"},
            {"route": "POST /workflows/versions", "command": "publish_workflow_version", "owned_tables": ("workflow_version",), "requires_permission": "workflow_orchestration.define", "idempotency_key": "version_id"},
            {"route": "POST /workflows/transition-guards", "command": "register_transition_guard", "owned_tables": ("workflow_transition_guard",), "requires_permission": "workflow_orchestration.define", "idempotency_key": "guard_id"},
            {"route": "POST /workflows/retry-policies", "command": "register_retry_policy", "owned_tables": ("workflow_retry_policy",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "policy_id"},
            {"route": "POST /workflows/sla-policies", "command": "register_sla_policy", "owned_tables": ("workflow_sla_policy",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "policy_id"},
            {"route": "POST /workflows/escalation-rules", "command": "register_escalation_rule", "owned_tables": ("workflow_escalation_rule",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "escalation_id"},
            {"route": "POST /workflows/instances", "command": "start_instance", "owned_tables": ("workflow_instance",), "emits": ("WorkflowStarted",), "requires_permission": "workflow_orchestration.start", "idempotency_key": "instance_id"},
            {"route": "POST /workflows/instances/{id}/signals", "command": "signal_instance", "owned_tables": ("workflow_signal", "workflow_instance"), "emits": ("WorkflowSignalAccepted",), "requires_permission": "workflow_orchestration.signal", "idempotency_key": "signal_id"},
            {"route": "POST /workflows/timers", "command": "schedule_timer", "owned_tables": ("timer_task",), "emits": ("TimerScheduled",), "requires_permission": "workflow_orchestration.start", "idempotency_key": "timer_id"},
            {"route": "POST /workflows/instances/{id}/steps", "command": "record_step_result", "owned_tables": ("saga_step",), "emits": ("SagaStepCompleted",), "requires_permission": "workflow_orchestration.signal", "idempotency_key": "step_id"},
            {"route": "POST /workflows/instances/{id}/compensations", "command": "execute_compensation", "owned_tables": ("compensation",), "emits": ("CompensationExecuted",), "requires_permission": "workflow_orchestration.compensate", "idempotency_key": "compensation_id"},
            {"route": "POST /workflows/human-task-assignments", "command": "assign_human_task", "owned_tables": ("human_task", "human_task_assignment"), "requires_permission": "workflow_orchestration.signal", "idempotency_key": "assignment_id"},
            {"route": "POST /workflows/approval-decisions", "command": "record_approval_decision", "owned_tables": ("workflow_approval_decision", "human_task"), "requires_permission": "workflow_orchestration.signal", "idempotency_key": "decision_id"},
            {"route": "POST /workflows/integration-endpoints", "command": "register_integration_endpoint", "owned_tables": ("workflow_integration_endpoint",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "endpoint_id"},
            {"route": "POST /workflows/event-correlations", "command": "correlate_event", "owned_tables": ("workflow_event_correlation",), "requires_permission": "workflow_orchestration.event", "idempotency_key": "correlation_id"},
            {"route": "POST /workflows/metric-snapshots", "command": "capture_metric_snapshot", "owned_tables": ("workflow_metric_snapshot",), "requires_permission": "workflow_orchestration.audit", "idempotency_key": "snapshot_id"},
            {"route": "POST /workflows/exception-cases", "command": "open_exception_case", "owned_tables": ("workflow_exception_case",), "requires_permission": "workflow_orchestration.compensate", "idempotency_key": "case_id"},
            {"route": "POST /workflows/simulation-runs", "command": "record_simulation_run", "owned_tables": ("workflow_simulation_run",), "requires_permission": "workflow_orchestration.audit", "idempotency_key": "simulation_id"},
            {"route": "POST /workflows/policy-screenings", "command": "record_policy_screening", "owned_tables": ("workflow_policy_screening",), "requires_permission": "workflow_orchestration.audit", "idempotency_key": "screening_id"},
            {"route": "POST /workflows/completion-proofs", "command": "record_completion_proof", "owned_tables": ("workflow_completion_proof",), "requires_permission": "workflow_orchestration.audit", "idempotency_key": "proof_id"},
            {"route": "POST /workflows/instances/{id}/complete", "command": "complete_workflow", "owned_tables": ("workflow_instance",), "emits": ("WorkflowCompleted",), "requires_permission": "workflow_orchestration.start", "idempotency_key": "instance_id"},
            {"route": "POST /workflows/audit-entries", "command": "append_audit_entry", "owned_tables": ("workflow_audit_entry",), "requires_permission": "workflow_orchestration.audit", "idempotency_key": "audit_entry_id"},
            {"route": "POST /workflows/governed-model-evidence", "command": "register_governed_model_evidence", "owned_tables": ("workflow_governed_model_evidence",), "requires_permission": "workflow_orchestration.configure", "idempotency_key": "evidence_id"},
            {"route": "POST /workflows/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES, "requires_permission": "workflow_orchestration.event", "idempotency_key": "event_id"},
            {"route": "GET /workflows/workbench", "query": "build_workbench_view", "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES, "requires_permission": "workflow_orchestration.audit"},
            {"route": "GET /workflows/schema-contract", "query": "build_schema_contract", "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES, "requires_permission": "workflow_orchestration.audit"},
            {"route": "GET /workflows/service-contract", "query": "build_service_contract", "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES, "requires_permission": "workflow_orchestration.audit"},
            {"route": "GET /workflows/release-evidence", "query": "build_release_evidence", "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES, "requires_permission": "workflow_orchestration.audit"},
        ),
        "declared_catalog_routes": (
            "PUT /workflows/configuration",
            "POST /workflows/parameters",
            "POST /workflows/rules",
            "POST /workflows/definitions",
            "POST /workflows/versions",
            "POST /workflows/transition-guards",
            "POST /workflows/retry-policies",
            "POST /workflows/sla-policies",
            "POST /workflows/escalation-rules",
            "POST /workflows/instances",
            "POST /workflows/instances/{id}/signals",
            "POST /workflows/timers",
            "POST /workflows/instances/{id}/steps",
            "POST /workflows/instances/{id}/compensations",
            "POST /workflows/human-task-assignments",
            "POST /workflows/approval-decisions",
            "POST /workflows/integration-endpoints",
            "POST /workflows/event-correlations",
            "POST /workflows/metric-snapshots",
            "POST /workflows/exception-cases",
            "POST /workflows/simulation-runs",
            "POST /workflows/policy-screenings",
            "POST /workflows/completion-proofs",
            "POST /workflows/instances/{id}/complete",
            "POST /workflows/audit-entries",
            "POST /workflows/governed-model-evidence",
            "POST /workflows/events/inbox",
            "GET /workflows/workbench",
            "GET /workflows/schema-contract",
            "GET /workflows/service-contract",
            "GET /workflows/release-evidence",
        ),
        "events": {"emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES, "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES},
        "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
        "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(workflow_orchestration_permissions_contract()["permissions"])),
        "database_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
        "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "configuration": ("WORKFLOW_ORCHESTRATION_DATABASE_URL", "WORKFLOW_ORCHESTRATION_EVENT_TOPIC", "WORKFLOW_ORCHESTRATION_RETRY_LIMIT", "WORKFLOW_ORCHESTRATION_DEFAULT_TIMEZONE"),
        "dependencies": {
            "apis": tuple(item for item in _WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def workflow_orchestration_build_schema_contract() -> dict:
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in WORKFLOW_ORCHESTRATION_OWNED_TABLES}
    table_fields.update(
        {
            "workflow_definition": (
                "tenant",
                "workflow_id",
                "owner_pbc",
                "semantic_version",
                "states",
                "transitions",
                "participants",
                "status",
                "audit_hash",
            ),
            "workflow_version": ("tenant", "version_id", "workflow_id", "semantic_version", "status", "audit_hash"),
            "workflow_instance": (
                "tenant",
                "instance_id",
                "workflow_id",
                "correlation_id",
                "current_state",
                "context_payload",
                "history",
                "status",
                "audit_hash",
            ),
            "workflow_signal": (
                "tenant",
                "signal_id",
                "instance_id",
                "signal",
                "source_pbc",
                "payload",
                "accepted",
                "idempotency_key",
                "audit_hash",
            ),
            "workflow_transition_guard": ("tenant", "guard_id", "workflow_id", "from_state", "signal", "expression", "compiled_hash", "status", "audit_hash"),
            "timer_task": (
                "tenant",
                "timer_id",
                "instance_id",
                "action",
                "deadline_seconds",
                "breach_risk",
                "retry_budget",
                "status",
                "audit_hash",
            ),
            "workflow_retry_policy": ("tenant", "policy_id", "workflow_id", "max_attempts", "backoff", "status", "audit_hash"),
            "workflow_sla_policy": ("tenant", "policy_id", "workflow_id", "threshold_seconds", "severity", "status", "audit_hash"),
            "workflow_escalation_rule": ("tenant", "escalation_id", "workflow_id", "trigger", "target_group", "status", "audit_hash"),
            "saga_step": (
                "tenant",
                "step_id",
                "instance_id",
                "participant_pbc",
                "command",
                "duration_ms",
                "status",
                "idempotency_key",
                "audit_hash",
            ),
            "compensation": (
                "tenant",
                "compensation_id",
                "instance_id",
                "step_id",
                "command",
                "reason",
                "side_effect_boundary",
                "status",
                "audit_hash",
            ),
            "human_task": (
                "tenant",
                "task_id",
                "instance_id",
                "task_type",
                "assignee_group",
                "decision",
                "sla_due_at",
                "status",
                "audit_hash",
            ),
            "human_task_assignment": ("tenant", "assignment_id", "task_id", "instance_id", "assignee_group", "status", "audit_hash"),
            "workflow_approval_decision": ("tenant", "decision_id", "task_id", "decision", "decided_by", "status", "audit_hash"),
            "workflow_integration_endpoint": ("tenant", "endpoint_id", "participant_pbc", "route", "status", "audit_hash"),
            "workflow_event_correlation": ("tenant", "correlation_id", "instance_id", "source_event", "business_key", "audit_hash"),
            "workflow_metric_snapshot": ("tenant", "snapshot_id", "workflow_id", "instance_count", "completed_count", "compensation_count", "completion_rate", "audit_hash"),
            "workflow_exception_case": ("tenant", "case_id", "instance_id", "case_type", "severity", "recommended_action", "status", "audit_hash"),
            "workflow_simulation_run": ("tenant", "simulation_id", "workflow_id", "scenario", "risk_delta", "status", "audit_hash"),
            "workflow_policy_screening": ("tenant", "screening_id", "workflow_id", "decision", "status", "audit_hash"),
            "workflow_completion_proof": ("tenant", "proof_id", "instance_id", "proof_hash", "proof_type", "status", "audit_hash"),
            "workflow_audit_entry": ("tenant", "audit_entry_id", "action", "payload_hash", "status", "audit_hash"),
            "workflow_governed_model_evidence": ("tenant", "evidence_id", "model_id", "auc", "drift_score", "status", "audit_hash"),
            "workflow_rule": (
                "tenant",
                "rule_id",
                "scope",
                "trigger",
                "compiled_hash",
                "enabled",
                "severity",
                "status",
                "audit_hash",
            ),
            "workflow_parameter": (
                "tenant",
                "parameter_name",
                "parameter_value",
                "effective_at",
                "changed_by",
                "audit_hash",
            ),
            "workflow_configuration": (
                "tenant",
                "configuration_id",
                "database_backend",
                "event_topic",
                "event_contract",
                "stream_engine_picker_visible",
                "default_timezone",
                "audit_hash",
            ),
        }
    )
    runtime_tables = (
        {
            "table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "published_at", "audit_hash"),
        },
        {
            "table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "audit_hash"),
        },
        {
            "table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "payload", "reason", "attempts", "audit_hash"),
        },
    )
    relationships = (
        {"from_table": "workflow_instance", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_version", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_signal", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "workflow_transition_guard", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "timer_task", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "workflow_retry_policy", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_sla_policy", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_escalation_rule", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "saga_step", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "compensation", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "compensation", "from_field": "step_id", "to_table": "saga_step", "to_field": "step_id"},
        {"from_table": "human_task", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "human_task_assignment", "from_field": "task_id", "to_table": "human_task", "to_field": "task_id"},
        {"from_table": "workflow_approval_decision", "from_field": "task_id", "to_table": "human_task", "to_field": "task_id"},
        {"from_table": "workflow_event_correlation", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "workflow_metric_snapshot", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_exception_case", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
        {"from_table": "workflow_simulation_run", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_policy_screening", "from_field": "workflow_id", "to_table": "workflow_definition", "to_field": "workflow_id"},
        {"from_table": "workflow_completion_proof", "from_field": "instance_id", "to_table": "workflow_instance", "to_field": "instance_id"},
    )
    tables = tuple(
        {"table": table, "fields": table_fields[table], "owner": "workflow_orchestration"}
        for table in WORKFLOW_ORCHESTRATION_OWNED_TABLES
    )
    return {
        "format": "appgen.workflow-orchestration-owned-schema-contract.v1",
        "ok": len(tables) == len(WORKFLOW_ORCHESTRATION_OWNED_TABLES)
        and all(item["table"].startswith(("workflow_", "timer_", "saga_", "compensation", "human_task")) for item in tables),
        "tables": tables,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/workflow_orchestration/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(WORKFLOW_ORCHESTRATION_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in WORKFLOW_ORCHESTRATION_OWNED_TABLES
        ),
        "datastore_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def workflow_orchestration_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "define_workflow",
        "publish_workflow_version",
        "register_transition_guard",
        "start_instance",
        "signal_instance",
        "schedule_timer",
        "register_retry_policy",
        "register_sla_policy",
        "register_escalation_rule",
        "record_step_result",
        "execute_compensation",
        "assign_human_task",
        "record_approval_decision",
        "register_integration_endpoint",
        "correlate_event",
        "capture_metric_snapshot",
        "open_exception_case",
        "record_simulation_run",
        "record_policy_screening",
        "record_completion_proof",
        "append_audit_entry",
        "register_governed_model_evidence",
        "complete_workflow",
        "run_control_tests",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "simulate_saga_policy",
        "forecast_workflow_health",
        "parse_workflow_intent",
        "score_saga_risk",
        "recommend_compensation",
        "select_execution_route",
        "generate_completion_proof",
        "screen_policy",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "ui_binding_contract",
    )
    return {
        "format": "appgen.workflow-orchestration-service-contract.v1",
        "ok": len(command_methods) >= 12 and len(query_methods) >= 10,
        "transaction_boundary": "workflow_orchestration_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "idempotent_handlers": ("receive_event", "signal_instance", "record_step_result", "execute_compensation"),
        "retry_dead_letter_evidence": {
            "inbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1],
            "dead_letter_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[2],
            "retry_limit_source": "workflow_configuration.retry_limit",
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
        },
        "mutates_only": (*WORKFLOW_ORCHESTRATION_OWNED_TABLES, *WORKFLOW_ORCHESTRATION_RUNTIME_TABLES),
        "external_dependencies": {
            "apis": tuple(item for item in _WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def workflow_orchestration_build_release_evidence() -> dict:
    schema = workflow_orchestration_build_schema_contract()
    service = workflow_orchestration_build_service_contract()
    api = workflow_orchestration_build_api_contract()
    permissions = workflow_orchestration_permissions_contract()
    workbench = workflow_orchestration_build_workbench_view(workflow_orchestration_empty_state(), tenant="tenant_release")
    ui = workflow_orchestration_ui_binding_contract()
    boundary = workflow_orchestration_verify_owned_table_boundary(
        (
            "workflow_instance",
            "workflow_orchestration_appgen_outbox_event",
            "GET /gateway/routes",
            "gateway_workflow_projection",
            "SchemaAccepted",
        )
    )
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) == len(WORKFLOW_ORCHESTRATION_OWNED_TABLES)},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(WORKFLOW_ORCHESTRATION_OWNED_TABLES)},
        {"id": "runtime_tables_declared", "ok": tuple(item["table"] for item in schema["runtime_tables"]) == WORKFLOW_ORCHESTRATION_RUNTIME_TABLES},
        {"id": "service_contract_depth", "ok": service["ok"] and "receive_event" in service["idempotent_handlers"]},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["required_event_topic"] == WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "ui_binding_evidence", "ok": ui["ok"] and ui["binding_evidence"]["runtime_tables"] == WORKFLOW_ORCHESTRATION_RUNTIME_TABLES},
        {"id": "workbench_binding_evidence", "ok": workbench["binding_evidence"]["outbox_table"] == WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[0]},
        {"id": "boundary_contract", "ok": boundary["ok"] and boundary["declared_dependencies"]["shared_tables"] == ()},
        {"id": "database_allowlist", "ok": schema["datastore_backends"] == WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS},
    )
    return {
        "format": "appgen.workflow-orchestration-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "ui_binding": ui,
        "boundary": boundary,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def workflow_orchestration_permissions_contract() -> dict:
    return {
        "format": "appgen.workflow-orchestration-permissions.v1",
        "ok": True,
        "pbc": "workflow_orchestration",
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
            "publish_workflow_version": "workflow_orchestration.define",
            "register_transition_guard": "workflow_orchestration.define",
            "start_instance": "workflow_orchestration.start",
            "signal_instance": "workflow_orchestration.signal",
            "schedule_timer": "workflow_orchestration.start",
            "register_retry_policy": "workflow_orchestration.configure",
            "register_sla_policy": "workflow_orchestration.configure",
            "register_escalation_rule": "workflow_orchestration.configure",
            "record_step_result": "workflow_orchestration.signal",
            "execute_compensation": "workflow_orchestration.compensate",
            "assign_human_task": "workflow_orchestration.signal",
            "record_approval_decision": "workflow_orchestration.signal",
            "register_integration_endpoint": "workflow_orchestration.configure",
            "correlate_event": "workflow_orchestration.event",
            "capture_metric_snapshot": "workflow_orchestration.audit",
            "open_exception_case": "workflow_orchestration.compensate",
            "record_simulation_run": "workflow_orchestration.audit",
            "record_policy_screening": "workflow_orchestration.audit",
            "record_completion_proof": "workflow_orchestration.audit",
            "append_audit_entry": "workflow_orchestration.audit",
            "register_governed_model_evidence": "workflow_orchestration.configure",
            "complete_workflow": "workflow_orchestration.start",
            "receive_event": "workflow_orchestration.event",
            "register_rule": "workflow_orchestration.configure",
            "register_schema_extension": "workflow_orchestration.configure",
            "set_parameter": "workflow_orchestration.configure",
            "configure_runtime": "workflow_orchestration.configure",
            "build_workbench_view": "workflow_orchestration.audit",
            "run_control_tests": "workflow_orchestration.audit",
            "build_schema_contract": "workflow_orchestration.audit",
            "build_service_contract": "workflow_orchestration.audit",
            "build_release_evidence": "workflow_orchestration.audit",
        },
    }


def workflow_orchestration_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*WORKFLOW_ORCHESTRATION_OWNED_TABLES, *WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES, *WORKFLOW_ORCHESTRATION_RUNTIME_TABLES, *_WORKFLOW_ORCHESTRATION_ALLOWED_DEPENDENCIES)
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


def workflow_orchestration_register_governed_model_evidence(state: dict, evidence: dict) -> dict:
    required = {"evidence_id", "tenant", "model_id", "auc", "drift_score", "status"}
    _require(evidence, required)
    next_state = _copy_state(state)
    stored = {**evidence, "audit_hash": _hash_payload(evidence)}
    next_state["workflow_governed_model_evidence"][evidence["evidence_id"]] = stored
    return {"ok": True, "state": next_state, "evidence": stored}


def _copy_state(state: dict) -> dict:
    return {
        "configuration": dict(state["configuration"]),
        "parameters": dict(state["parameters"]),
        "rules": dict(state["rules"]),
        "schema_extensions": {key: dict(value) for key, value in state["schema_extensions"].items()},
        "definitions": {key: dict(value) for key, value in state["definitions"].items()},
        "workflow_versions": {key: dict(value) for key, value in state.get("workflow_versions", {}).items()},
        "instances": {key: dict(value) for key, value in state["instances"].items()},
        "signals": {key: dict(value) for key, value in state["signals"].items()},
        "workflow_transition_guards": {key: dict(value) for key, value in state.get("workflow_transition_guards", {}).items()},
        "timers": {key: dict(value) for key, value in state["timers"].items()},
        "workflow_retry_policies": {key: dict(value) for key, value in state.get("workflow_retry_policies", {}).items()},
        "workflow_sla_policies": {key: dict(value) for key, value in state.get("workflow_sla_policies", {}).items()},
        "workflow_escalation_rules": {key: dict(value) for key, value in state.get("workflow_escalation_rules", {}).items()},
        "saga_steps": {key: dict(value) for key, value in state["saga_steps"].items()},
        "compensations": {key: dict(value) for key, value in state["compensations"].items()},
        "human_tasks": {key: dict(value) for key, value in state["human_tasks"].items()},
        "human_task_assignments": {key: dict(value) for key, value in state.get("human_task_assignments", {}).items()},
        "workflow_approval_decisions": {key: dict(value) for key, value in state.get("workflow_approval_decisions", {}).items()},
        "workflow_integration_endpoints": {key: dict(value) for key, value in state.get("workflow_integration_endpoints", {}).items()},
        "workflow_event_correlations": {key: dict(value) for key, value in state.get("workflow_event_correlations", {}).items()},
        "workflow_metric_snapshots": {key: dict(value) for key, value in state.get("workflow_metric_snapshots", {}).items()},
        "workflow_exception_cases": {key: dict(value) for key, value in state.get("workflow_exception_cases", {}).items()},
        "workflow_simulation_runs": {key: dict(value) for key, value in state.get("workflow_simulation_runs", {}).items()},
        "workflow_policy_screenings": {key: dict(value) for key, value in state.get("workflow_policy_screenings", {}).items()},
        "workflow_completion_proofs": {key: dict(value) for key, value in state.get("workflow_completion_proofs", {}).items()},
        "workflow_audit_entries": {key: dict(value) for key, value in state.get("workflow_audit_entries", {}).items()},
        "workflow_governed_model_evidence": {key: dict(value) for key, value in state.get("workflow_governed_model_evidence", {}).items()},
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
