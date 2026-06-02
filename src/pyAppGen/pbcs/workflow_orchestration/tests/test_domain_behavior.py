"""Executable domain behavior tests for the workflow_orchestration PBC."""

import pytest

from .. import agent
from .. import routes
from .. import runtime
from .. import services
from .. import ui
from ..permissions import permission_manifest


TENANT = "tenant_workflow_alpha"
WORKFLOW_ID = "order_fulfillment_saga"
INSTANCE_ID = "order_fulfillment_instance_1"


def _configuration():
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "allowed_signal_sources": ("api_gateway_mesh", "schema_registry", "dom", "payment_orchestration", "wms_core"),
        "default_versioning": "semantic",
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _all_permissions():
    return tuple(dict.fromkeys(permission_manifest()["action_permissions"].values()))


def _configured_service():
    service = services.WorkflowOrchestrationService()
    configured = service.configure_runtime({"configuration": _configuration()})
    assert configured["ok"] is True, configured
    for name, value in {
        "default_retry_limit": 3,
        "timer_jitter_seconds": 30,
        "sla_breach_threshold": 0.25,
        "compensation_risk_threshold": 0.55,
        "max_parallel_steps": 8,
        "review_sla_hours": 24,
    }.items():
        result = service.set_parameter({"name": name, "value": value})
        assert result["ok"] is True, result
    rule = service.register_rule(
        {
            "rule": {
                "rule_id": "workflow.alpha.release_gate",
                "tenant": TENANT,
                "scope": "saga",
                "trigger": "signal_received",
                "allowed_signals": ("reserve", "pay", "ship", "complete", "cancel"),
                "requires_compensation": True,
                "severity": "blocking",
                "status": "active",
            }
        }
    )
    assert rule["ok"] is True, rule
    extension = runtime.workflow_orchestration_register_schema_extension(
        service.state,
        "workflow_instance",
        {"external_trace": "jsonb"},
    )
    assert extension["ok"] is True, extension
    service._sync(extension)
    return service


def _populated_service():
    service = _configured_service()
    definition = service.define_workflow(
        {
            "workflow": {
                "workflow_id": WORKFLOW_ID,
                "tenant": TENANT,
                "owner_pbc": "dom",
                "version": "1.0.0",
                "states": ("created", "reserved", "paid", "shipped", "completed", "cancelled"),
                "transitions": (
                    ("created", "reserve", "reserved"),
                    ("reserved", "pay", "paid"),
                    ("paid", "ship", "shipped"),
                    ("shipped", "complete", "completed"),
                    ("reserved", "cancel", "cancelled"),
                ),
                "participants": ("dom", "payment_orchestration", "wms_core"),
            }
        }
    )
    version = service.publish_workflow_version(
        {
            "version": {
                "version_id": "order_fulfillment_saga_v1",
                "tenant": TENANT,
                "workflow_id": WORKFLOW_ID,
                "semantic_version": "1.0.0",
                "status": "published",
            }
        }
    )
    guard = service.register_transition_guard(
        {
            "guard": {
                "guard_id": "guard_pay_after_reserve",
                "tenant": TENANT,
                "workflow_id": WORKFLOW_ID,
                "from_state": "reserved",
                "signal": "pay",
                "expression": "context.reserved == true",
                "status": "active",
            }
        }
    )
    retry_policy = service.register_retry_policy(
        {
            "policy": {
                "policy_id": "retry_payment",
                "tenant": TENANT,
                "workflow_id": WORKFLOW_ID,
                "max_attempts": 3,
                "backoff": "exponential",
                "status": "active",
            }
        }
    )
    sla_policy = service.register_sla_policy(
        {
            "policy": {
                "policy_id": "sla_ship",
                "tenant": TENANT,
                "workflow_id": WORKFLOW_ID,
                "threshold_seconds": 7200,
                "severity": "warning",
                "status": "active",
            }
        }
    )
    escalation = service.register_escalation_rule(
        {
            "rule": {
                "escalation_id": "esc_ship_delay",
                "tenant": TENANT,
                "workflow_id": WORKFLOW_ID,
                "trigger": "sla_breach",
                "target_group": "fulfillment_ops",
                "status": "active",
            }
        }
    )
    endpoint = service.register_integration_endpoint(
        {
            "endpoint": {
                "endpoint_id": "endpoint_payment_capture",
                "tenant": TENANT,
                "participant_pbc": "payment_orchestration",
                "route": "POST /payments/capture",
                "status": "active",
            }
        }
    )
    instance = service.start_instance(
        {
            "instance": {
                "instance_id": INSTANCE_ID,
                "tenant": TENANT,
                "workflow_id": WORKFLOW_ID,
                "correlation_id": "order-1001",
                "context": {"order_id": "order-1001", "reserved": True, "amount": 125.5},
            }
        }
    )
    reserve = service.signal_instance(
        {"instance_id": INSTANCE_ID, "signal": {"signal": "reserve", "source_pbc": "dom", "payload": {"reserved": True}}}
    )
    pay = service.signal_instance(
        {"instance_id": INSTANCE_ID, "signal": {"signal": "pay", "source_pbc": "payment_orchestration", "payload": {"captured": True}}}
    )
    timer = service.schedule_timer(
        {"timer": {"timer_id": "timer_ship_sla", "tenant": TENANT, "instance_id": INSTANCE_ID, "deadline_seconds": 3600, "action": "escalate_if_not_shipped"}}
    )
    step = service.record_step_result(
        {"step": {"step_id": "step_capture_payment", "tenant": TENANT, "instance_id": INSTANCE_ID, "participant_pbc": "payment_orchestration", "command": "capture", "status": "completed", "duration_ms": 240}}
    )
    compensation = service.execute_compensation(
        {"compensation": {"compensation_id": "comp_release_reservation", "tenant": TENANT, "instance_id": INSTANCE_ID, "step_id": "step_capture_payment", "command": "release_reservation", "reason": "participant_timeout"}}
    )
    assignment = service.assign_human_task(
        {"assignment": {"assignment_id": "assign_review", "tenant": TENANT, "task_id": "task_review", "instance_id": INSTANCE_ID, "assignee_group": "fulfillment_ops", "status": "assigned"}}
    )
    decision = service.record_approval_decision(
        {"decision": {"decision_id": "decision_review", "tenant": TENANT, "task_id": "task_review", "decision": "approve", "decided_by": "ops_lead", "status": "completed"}}
    )
    correlation = service.correlate_event(
        {"correlation": {"correlation_id": "corr_order_1001", "tenant": TENANT, "instance_id": INSTANCE_ID, "source_event": "OrderVerified", "business_key": "order-1001"}}
    )
    metric = service.capture_metric_snapshot(
        {"snapshot": {"snapshot_id": "metric_order", "tenant": TENANT, "workflow_id": WORKFLOW_ID, "instance_count": 1, "completed_count": 0, "compensation_count": 1}}
    )
    exception = service.open_exception_case(
        {"case": {"case_id": "case_timeout", "tenant": TENANT, "instance_id": INSTANCE_ID, "case_type": "participant_timeout", "severity": "high", "status": "open"}}
    )
    simulation = service.record_simulation_run(
        {"simulation": {"simulation_id": "sim_policy", "tenant": TENANT, "workflow_id": WORKFLOW_ID, "scenario": "lower_retry_limit", "risk_delta": 0.1, "status": "recorded"}}
    )
    screening = service.record_policy_screening(
        {"screening": {"screening_id": "screen_release", "tenant": TENANT, "workflow_id": WORKFLOW_ID, "decision": "clear", "status": "complete"}}
    )
    proof_preview = runtime.workflow_orchestration_generate_completion_proof(service.state, INSTANCE_ID, disclosure=("instance_id", "status", "current_state"))
    proof = service.record_completion_proof(
        {"proof": {"proof_id": "proof_order", "tenant": TENANT, "instance_id": INSTANCE_ID, "proof_hash": proof_preview["hash"], "proof_type": "zk_completion"}}
    )
    audit = service.append_audit_entry({"action": "operator_review", "entry_payload": {"tenant": TENANT, "instance_id": INSTANCE_ID}})
    model_evidence = service.register_governed_model_evidence(
        {"evidence": {"evidence_id": "model_workflow_risk", "tenant": TENANT, "model_id": "workflow_risk", "auc": 0.91, "drift_score": 0.03, "status": "approved"}}
    )
    ship = service.signal_instance(
        {"instance_id": INSTANCE_ID, "signal": {"signal": "ship", "source_pbc": "wms_core", "payload": {"shipped": True}}}
    )
    complete_signal = service.signal_instance(
        {"instance_id": INSTANCE_ID, "signal": {"signal": "complete", "source_pbc": "wms_core", "payload": {"delivered": True}}}
    )
    complete = service.complete_workflow({"instance_id": INSTANCE_ID})
    return service, locals()


def test_workflow_lifecycle_is_executable_through_service_routes_ui_and_agent():
    service, results = _populated_service()
    workbench = service.build_workbench_view({"tenant": TENANT})
    rendered = ui.workflow_orchestration_render_workbench(service.state, tenant=TENANT, principal_permissions=_all_permissions())
    standalone = ui.workflow_orchestration_render_standalone_app(service.state, tenant=TENANT, principal_permissions=_all_permissions())
    routed = routes.dispatch_route("GET", "/api/pbc/workflow_orchestration/workflows/workbench", {"tenant": TENANT}, service=service)
    assistant_plan = agent.document_instruction_plan(
        "states: created, reserved, paid, shipped, completed",
        "workflow order_fulfillment_saga with 4 hours timer and approval escalation",
    )
    crud_plan = agent.datastore_crud_plan("create", "workflow_orchestration_workflow_instance", {"instance_id": INSTANCE_ID})
    action_preview = agent.operational_action_preview("execute_compensation", tenant=TENANT, instance_id=INSTANCE_ID, reason="participant_timeout")

    assert results["definition"]["result"]["workflow"]["graph_edges"] == 5
    assert results["version"]["result"]["version"]["status"] == "published"
    assert results["guard"]["result"]["guard"]["compiled_hash"]
    assert results["retry_policy"]["ok"] is True
    assert results["sla_policy"]["ok"] is True
    assert results["escalation"]["ok"] is True
    assert results["endpoint"]["ok"] is True
    assert results["instance"]["result"]["instance"]["status"] == "running"
    assert results["reserve"]["result"]["signal"]["accepted"] is True
    assert results["pay"]["result"]["instance"]["current_state"] == "paid"
    assert results["timer"]["result"]["timer"]["status"] == "scheduled"
    assert results["step"]["result"]["step"]["completed"] is True
    assert results["compensation"]["result"]["compensation"]["side_effect_boundary"] == "declared_api_or_event"
    assert results["assignment"]["result"]["task"]["status"] == "assigned"
    assert results["decision"]["result"]["decision"]["decision"] == "approve"
    assert results["correlation"]["ok"] is True
    assert results["metric"]["result"]["snapshot"]["compensation_count"] == 1
    assert results["exception"]["result"]["case"]["recommended_action"] == "execute_compensation_then_retry"
    assert results["simulation"]["ok"] is True
    assert results["screening"]["result"]["screening"]["decision"] == "clear"
    assert results["proof"]["result"]["proof"]["status"] == "sealed"
    assert results["audit"]["result"]["audit_entry"]["status"] == "sealed"
    assert results["model_evidence"]["result"]["evidence"]["status"] == "approved"
    assert results["ship"]["ok"] is True
    assert results["complete_signal"]["ok"] is True
    assert results["complete"]["result"]["instance"]["status"] == "completed"
    assert workbench["result"]["workbench"]["completed_count"] == 1
    assert rendered["ok"] is True
    assert "define_workflow" in rendered["visible_actions"]
    assert standalone["workbench"]["cards"][1]["value"] == 1
    assert routed["ok"] is True
    assert routed["result"]["result"]["workbench"]["tenant"] == TENANT
    assert assistant_plan["ok"] is True
    assert crud_plan["ok"] is True
    assert action_preview["candidate_operation"] == "execute_compensation"
    assert all(event["idempotency_key"].startswith("workflow_orchestration:") for event in service.state["outbox"])
    assert any(event["event_type"] == "WorkflowCompleted" for event in service.state["outbox"])


def test_event_handlers_are_idempotent_and_capture_retry_dead_letter_evidence():
    service = _configured_service()
    event = {
        "event_id": "schema_accepted_order",
        "event_type": "SchemaAccepted",
        "idempotency_key": "schema:order:v1",
        "payload": {"tenant": TENANT, "subject_id": "order_schema", "version": "1.0.0"},
    }
    processed = service.receive_event({"envelope": event})
    duplicate = service.receive_event({"envelope": event})
    unsupported = {"event_id": "bad_workflow_evt", "event_type": "UnsupportedWorkflowEvent", "idempotency_key": "bad:workflow", "payload": {"tenant": TENANT}}
    retry_1 = service.receive_event({"envelope": unsupported})
    retry_2 = service.receive_event({"envelope": unsupported})
    dead_letter = service.receive_event({"envelope": unsupported})

    assert processed["result"]["handler"]["status"] == "processed"
    assert duplicate["result"]["duplicate"] is True
    assert retry_1["result"]["handler"]["status"] == "retrying"
    assert retry_2["result"]["handler"]["status"] == "retrying"
    assert dead_letter["result"]["handler"]["status"] == "dead_letter"
    assert service.state["dead_letter"][-1]["reason"] == "unsupported_or_failed_workflow_event"
    assert service.state["retry_evidence"][-1]["attempts"] == 3


def test_advanced_workflow_controls_are_domain_specific_and_executable():
    service, _ = _populated_service()
    state = service.state

    simulation = runtime.workflow_orchestration_simulate_saga_policy(state, WORKFLOW_ID, retry_limit=2, parallel_steps=4)
    forecast = runtime.workflow_orchestration_forecast_workflow_health((0.99, 0.94, 0.9), horizon_hours=24)
    parsed = runtime.workflow_orchestration_parse_workflow_intent("workflow order_fulfillment_saga instance order_1001 signal pay")
    risk = runtime.workflow_orchestration_score_saga_risk({"sla": 0.3, "retry": 0.2, "compensation": 0.4, "participant": 0.2})
    recommendation = runtime.workflow_orchestration_recommend_compensation("participant_timeout")
    selected = runtime.workflow_orchestration_select_execution_route(
        {"event_id": "workflow_route"},
        rails=({"route": "primary", "available": False, "latency": 2}, {"route": "outbox_replay", "available": True, "latency": 6}),
    )
    proof = runtime.workflow_orchestration_generate_completion_proof(state, INSTANCE_ID, disclosure=("instance_id", "status"))
    screening = runtime.workflow_orchestration_screen_policy(state, WORKFLOW_ID, severities=("blocking",))
    controls = runtime.workflow_orchestration_run_control_tests(state)
    federation = runtime.workflow_orchestration_federate_workflow_view(state, INSTANCE_ID, systems=("gateway", "schema", "audit"))
    identity = runtime.workflow_orchestration_verify_actor_identity({"did": "did:appgen:actor:ops", "issuer": "trusted_registry", "status": "active"})
    resilience = runtime.workflow_orchestration_run_resilience_drill(state, "signal_handler_timeout")
    crypto = runtime.workflow_orchestration_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.workflow_orchestration_schedule_carbon_aware_work(({"window": "day", "carbon": 190}, {"window": "night", "carbon": 75}))
    allocation = runtime.workflow_orchestration_allocate_saga_resources(({"participant": "payments", "criticality": 0.9}, {"participant": "warehouse", "criticality": 0.5}), capacity=10)
    anomaly = runtime.workflow_orchestration_detect_workflow_anomaly(state)
    stochastic = runtime.workflow_orchestration_model_stochastic_workflow_exposure(duration_path=(10, 20, 35), volatility=0.15)
    model = runtime.workflow_orchestration_register_governed_model("workflow_risk", {"auc": 0.9, "drift_score": 0.03, "features": ("sla", "retry")})
    release = service.build_release_evidence({})

    assert simulation["ok"] is True
    assert forecast["trend"] == "declining"
    assert parsed["workflow_id"] == WORKFLOW_ID
    assert risk["risk_score"] > 0
    assert recommendation["action"] == "execute_compensation_then_retry"
    assert selected["route"] == "outbox_replay"
    assert selected["failover_used"] is True
    assert proof["proof"].startswith("zk_workflow_")
    assert screening["decision"] == "clear"
    assert controls["ok"] is True
    assert federation["ok"] is True
    assert identity["ok"] is True
    assert resilience["ok"] is True
    assert crypto["epoch"] == 2
    assert carbon["window"] == "night"
    assert allocation["allocations"][0]["capacity"] > allocation["allocations"][1]["capacity"]
    assert anomaly["ok"] is True
    assert stochastic["tail_risk"] > 0
    assert model["ok"] is True
    assert release["result"]["ok"] is True


def test_runtime_configuration_rejects_unsupported_backends_and_eventing_choices():
    state = runtime.workflow_orchestration_empty_state()
    config = _configuration()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.workflow_orchestration_configure_runtime(state, {**config, "database_backend": "sqlite"})

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.workflow_orchestration_configure_runtime(state, {**config, "stream_engine": "kafka"})


def test_owned_boundary_allows_declared_dependencies_and_rejects_shared_tables():
    allowed = runtime.workflow_orchestration_verify_owned_table_boundary(("workflow_instance", "SchemaAccepted", "GET /schemas/subjects", "gateway_workflow_projection"))
    blocked = runtime.workflow_orchestration_verify_owned_table_boundary(("shared_order_table", "external_task_registry"))

    assert allowed["ok"] is True
    assert allowed["declared_dependencies"]["shared_tables"] == ()
    assert blocked["ok"] is False
    assert blocked["violations"] == ("shared_order_table", "external_task_registry")


def test_contract_builders_return_release_ready_workflow_package_evidence():
    assert runtime.workflow_orchestration_build_api_contract()["ok"] is True
    assert runtime.workflow_orchestration_build_schema_contract()["ok"] is True
    assert runtime.workflow_orchestration_build_service_contract()["ok"] is True
    evidence = runtime.workflow_orchestration_build_release_evidence()

    assert evidence["ok"] is True
    assert evidence["api"]["event_contract"] == "AppGen-X"
    assert all(check["ok"] for check in evidence["checks"])
    assert evidence["service"]["external_dependencies"]["shared_tables"] == ()
