"""Executable domain behavior tests for the schema_registry PBC."""

import pytest

from .. import agent
from .. import routes
from .. import runtime
from .. import services
from .. import ui


TENANT = "tenant_schema_alpha"
SUBJECT_ID = "subject_orders_created"


def _configuration():
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "allowed_formats": ("json", "avro", "event", "api", "projection"),
        "default_compatibility": "backward_forward",
        "namespace_policy": "tenant_scoped",
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _all_permissions():
    return tuple(dict.fromkeys(ui.schema_registry_ui_contract()["action_permissions"].values()))


def _configured_service():
    service = services.SchemaRegistryService()
    configured = service.configure_runtime({"configuration": _configuration()})
    assert configured["ok"] is True, configured
    for name, value in {
        "compatibility_threshold": 0.9,
        "max_schema_fields": 64,
        "semantic_similarity_floor": 0.82,
        "violation_risk_threshold": 0.45,
        "review_sla_hours": 24,
        "retention_days": 365,
    }.items():
        result = service.set_parameter({"name": name, "value": value})
        assert result["ok"] is True, result
    rule = service.register_rule(
        {
            "rule": {
                "rule_id": "rule_schema_alpha",
                "tenant": TENANT,
                "scope": "event",
                "mode": "backward_forward",
                "classification": "regulated",
                "severity": "blocking",
                "status": "active",
            }
        }
    )
    assert rule["ok"] is True, rule
    extension = runtime.schema_registry_register_schema_extension(
        service.repository._state,
        "schema_version",
        {"semantic_tags": "jsonb"},
    )
    assert extension["ok"] is True, extension
    service.repository._state = extension["state"]
    return service


def _populated_service():
    service = _configured_service()
    subject = service.register_subject(
        {
            "subject": {
                "subject_id": SUBJECT_ID,
                "tenant": TENANT,
                "owner_pbc": "order_routing_optimization",
                "name": "OrdersCreated",
                "channel": "event",
                "format": "json",
                "namespace": "commerce.orders",
            }
        }
    )
    compatibility_rule = service.define_compatibility_rule(
        {
            "rule": {
                "rule_id": "compat_orders",
                "tenant": TENANT,
                "subject_id": SUBJECT_ID,
                "mode": "backward_forward",
                "status": "active",
            }
        }
    )
    consumer = service.register_consumer_binding(
        {
            "binding": {
                "binding_id": "consumer_dom",
                "tenant": TENANT,
                "subject_id": SUBJECT_ID,
                "consumer_pbc": "dom",
                "consumer_type": "handler",
                "min_version": 1,
            }
        }
    )
    v1_schema = {
        "fields": {
            "order_id": {"type": "string", "required": True},
            "total": {"type": "number", "required": True},
        }
    }
    v1 = service.submit_schema_version(
        {
            "version": {
                "version_id": "orders_created_v1",
                "tenant": TENANT,
                "subject_id": SUBJECT_ID,
                "semantic_version": "1.0.0",
                "schema": v1_schema,
            }
        }
    )
    compatible = service.run_compatibility_check(
        {
            "subject_id": SUBJECT_ID,
            "proposed_schema": {
                "fields": {
                    "order_id": {"type": "string", "required": True},
                    "total": {"type": "number", "required": True},
                    "currency": {"type": "string", "required": False},
                }
            },
        }
    )
    v2 = service.submit_schema_version(
        {
            "version": {
                "version_id": "orders_created_v2",
                "tenant": TENANT,
                "subject_id": SUBJECT_ID,
                "semantic_version": "1.1.0",
                "schema": compatible["result"]["proposed_schema"],
            }
        }
    )
    blocked = service.run_compatibility_check(
        {
            "subject_id": SUBJECT_ID,
            "proposed_schema": {"fields": {"order_id": {"type": "number", "required": True}}},
        }
    )
    payload = service.validate_payload(
        {
            "subject_id": SUBJECT_ID,
            "payload": {"order_id": "ORD-1", "total": 150.25, "currency": "USD"},
        }
    )
    violation = service.record_contract_violation(
        {
            "violation": {
                "violation_id": "viol_orders_type_change",
                "tenant": TENANT,
                "subject_id": SUBJECT_ID,
                "producer_pbc": "order_routing_optimization",
                "consumer_pbc": "dom",
                "severity": "high",
                "reason": "type_change",
                "status": "open",
            }
        }
    )
    projection = service.publish_contract_projection(
        {"subject_id": SUBJECT_ID, "systems": ("gateway", "audit", "composition", "workflow")}
    )
    return service, {
        "subject": subject,
        "compatibility_rule": compatibility_rule,
        "consumer": consumer,
        "v1": v1,
        "compatible": compatible,
        "v2": v2,
        "blocked": blocked,
        "payload": payload,
        "violation": violation,
        "projection": projection,
    }


def test_schema_lifecycle_is_executable_through_service_routes_ui_and_agent():
    service, results = _populated_service()
    subject_query = service.query_subjects({"tenant": TENANT})
    workbench = service.query_workbench({"tenant": TENANT})
    rendered = ui.schema_registry_render_workbench(
        service.state,
        tenant=TENANT,
        principal_permissions=_all_permissions(),
    )
    standalone = ui.schema_registry_render_standalone_app(
        service.state,
        tenant=TENANT,
        principal_permissions=_all_permissions(),
    )
    routed = routes.dispatch_route(
        "GET",
        "/api/pbc/schema_registry/workbench",
        {"tenant": TENANT},
        service=service,
    )
    assistant_plan = agent.document_instruction_plan(
        "Register an OrdersCreated event schema and validate payload compatibility for DOM consumers.",
        "create schema subject subject_orders_created and publish contract projection",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "schema_registry_schema_subject",
        {"subject_id": SUBJECT_ID},
    )
    session = agent.assistant_session_plan("Review breaking compatibility risk", {"subject_id": SUBJECT_ID})

    assert results["subject"]["result"]["subject"]["status"] == "active"
    assert results["compatibility_rule"]["ok"] is True
    assert results["consumer"]["result"]["binding"]["status"] == "active"
    assert results["v1"]["result"]["decision"] == "accepted"
    assert results["compatible"]["result"]["decision"] == "accepted"
    assert results["v2"]["result"]["version"]["version_number"] == 2
    assert results["blocked"]["ok"] is False
    assert results["blocked"]["result"]["decision"] == "blocked"
    assert results["payload"]["result"]["validation"]["ok"] is True
    assert results["violation"]["result"]["violation"]["release_blocking"] is True
    assert results["projection"]["result"]["handoffs"] == (
        "gateway_contract_projection",
        "audit_contract_projection",
        "composition_contract_projection",
        "workflow_contract_projection",
    )
    assert subject_query["result"]["count"] == 1
    assert workbench["result"]["view"]["version_count"] == 2
    assert rendered["ok"] is True
    assert "register_subject" in rendered["visible_actions"]
    assert standalone["workbench"]["cards"][0]["value"] == 1
    assert routed["ok"] is True
    assert routed["result"]["result"]["view"]["tenant"] == TENANT
    assert assistant_plan["ok"] is True
    assert crud_plan["ok"] is True
    assert session["wizard"] == "breaking_change_review_wizard"
    assert all(event["idempotency_key"].startswith("schema_registry:") for event in service.state["outbox"])
    assert any(event["event_type"] == "SchemaAccepted" for event in service.state["outbox"])


def test_event_handlers_are_idempotent_and_capture_retry_dead_letter_evidence():
    service = _configured_service()
    event = {
        "event_id": "route_published_orders",
        "event_type": "RoutePublished",
        "idempotency_key": "route:orders:v1",
        "payload": {"tenant": TENANT, "route_id": "route_orders", "path": "/orders"},
    }
    processed = service.receive_event({"envelope": event})
    duplicate = service.receive_event({"envelope": event})
    unsupported = {
        "event_id": "unsupported_schema_evt",
        "event_type": "UnsupportedSchemaEvent",
        "idempotency_key": "unsupported:schema",
        "payload": {"tenant": TENANT},
    }
    retry_1 = service.receive_event({"envelope": unsupported})
    retry_2 = service.receive_event({"envelope": unsupported})
    dead_letter = service.receive_event({"envelope": unsupported})

    assert processed["result"]["handler"]["status"] == "processed"
    assert duplicate["result"]["duplicate"] is True
    assert retry_1["result"]["handler"]["status"] == "retrying"
    assert retry_2["result"]["handler"]["status"] == "retrying"
    assert dead_letter["result"]["handler"]["status"] == "dead_letter"
    assert service.state["dead_letter"][-1]["reason"] == "unsupported_or_failed_schema_event"
    assert service.state["retry_evidence"][-1]["attempts"] == 3


def test_advanced_schema_controls_are_domain_specific_and_executable():
    service, _ = _populated_service()
    state = service.state

    simulation = runtime.schema_registry_simulate_schema_evolution(
        state,
        SUBJECT_ID,
        remove_required_fields=1,
        add_optional_fields=2,
    )
    forecast = runtime.schema_registry_forecast_compatibility_health((0.99, 0.96, 0.91), horizon_days=30)
    parsed = runtime.schema_registry_parse_schema_intent("register event subject subject_900 owner inventory_positioning version 2")
    risk = runtime.schema_registry_score_contract_risk({"breaking": 0.4, "consumer": 0.3, "payload": 0.2, "governance": 0.1})
    remediation = runtime.schema_registry_recommend_remediation("required_field_removed")
    selected = runtime.schema_registry_select_validation_route(
        {"event_id": "schema_check"},
        rails=(
            {"route": "primary", "available": False, "latency": 2},
            {"route": "outbox_replay", "available": True, "latency": 5},
        ),
    )
    proof = runtime.schema_registry_generate_schema_proof(
        state,
        SUBJECT_ID,
        disclosure=("subject_id", "latest_version", "fingerprint"),
    )
    screening = runtime.schema_registry_screen_policy(state, SUBJECT_ID, classifications=("regulated",))
    controls = runtime.schema_registry_run_control_tests(state)
    federation = runtime.schema_registry_federate_contract_view(state, SUBJECT_ID, systems=("gateway", "audit", "composition"))
    identity = runtime.schema_registry_verify_contract_identity(
        {"did": "did:appgen:producer-orders", "issuer": "trusted_registry", "status": "active"}
    )
    resilience = runtime.schema_registry_run_resilience_drill(state, "validator_timeout")
    crypto = runtime.schema_registry_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.schema_registry_schedule_carbon_aware_validation(
        ({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70})
    )
    diff = runtime.schema_registry_minimize_schema_diff({"remove": 1, "change_type": 1, "add_optional": 2})
    allocation = runtime.schema_registry_allocate_consumer_impact(
        ({"consumer": "dom", "criticality": 0.9}, {"consumer": "analytics", "criticality": 0.4}),
        review_slots=10,
    )
    anomaly = runtime.schema_registry_detect_validation_anomaly(state)
    stochastic = runtime.schema_registry_model_stochastic_contract_exposure(
        compatibility_path=(0.99, 0.93, 0.88),
        volatility=0.08,
    )
    model = runtime.schema_registry_register_governed_model(
        "contract_risk",
        {"features": ("breaking", "consumer", "payload"), "auc": 0.91, "drift_score": 0.03},
    )
    release_query = service.query_release_evidence({})

    assert simulation["risk_delta"] > 0
    assert forecast["trend"] == "declining"
    assert parsed["subject_id"] == "subject_900"
    assert risk["risk_score"] > 0
    assert remediation["action"] == "publish_additive_version"
    assert selected["route"] == "outbox_replay"
    assert selected["failover_used"] is True
    assert proof["proof"].startswith("zk_schema_")
    assert screening["decision"] == "clear"
    assert controls["ok"] is True
    assert federation["ok"] is True
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_contract_validation"
    assert crypto["epoch"] == 2
    assert carbon["window"] == "night"
    assert diff["breaking_operations"] == 2
    assert allocation["allocations"][0]["slots"] > allocation["allocations"][1]["slots"]
    assert anomaly["ok"] is True
    assert stochastic["tail_risk"] > 0
    assert model["governance"]["monitoring"] == "enabled"
    assert release_query["result"]["release_evidence"]["ok"] is True


def test_runtime_configuration_rejects_unsupported_backends_and_eventing_choices():
    state = runtime.schema_registry_empty_state()
    config = _configuration()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.schema_registry_configure_runtime(state, {**config, "database_backend": "sqlite"})

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.schema_registry_configure_runtime(state, {**config, "stream_engine": "kafka"})


def test_owned_boundary_allows_declared_dependencies_and_rejects_shared_tables():
    allowed = runtime.schema_registry_verify_owned_table_boundary(
        (
            "schema_subject",
            "RoutePublished",
            "GET /gateway/routes",
            "gateway_contract_projection",
        )
    )
    blocked = runtime.schema_registry_verify_owned_table_boundary(
        ("shared_gateway_route_table", "external_schema_catalog")
    )

    assert allowed["ok"] is True
    assert allowed["declared_dependencies"]["shared_tables"] == ()
    assert blocked["ok"] is False
    assert blocked["violations"] == ("shared_gateway_route_table", "external_schema_catalog")


def test_contract_builders_return_release_ready_schema_package_evidence():
    assert runtime.schema_registry_build_api_contract()["ok"] is True
    assert runtime.schema_registry_build_schema_contract()["ok"] is True
    assert runtime.schema_registry_build_service_contract()["ok"] is True
    evidence = runtime.schema_registry_build_release_evidence()

    assert evidence["ok"] is True
    assert evidence["api"]["event_contract"] == "AppGen-X"
    assert all(check["ok"] for check in evidence["checks"])
    assert evidence["service"]["external_dependencies"]["shared_tables"] == ()
