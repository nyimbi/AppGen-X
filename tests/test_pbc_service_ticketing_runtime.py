import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import service_ticketing_assign_ticket
from pyAppGen.pbc import service_ticketing_build_workbench_view
from pyAppGen.pbc import service_ticketing_configure_runtime
from pyAppGen.pbc import service_ticketing_create_sla_policy
from pyAppGen.pbc import service_ticketing_empty_state
from pyAppGen.pbc import service_ticketing_open_ticket
from pyAppGen.pbc import service_ticketing_receive_event
from pyAppGen.pbc import service_ticketing_record_escalation
from pyAppGen.pbc import service_ticketing_register_rule
from pyAppGen.pbc import service_ticketing_render_workbench
from pyAppGen.pbc import service_ticketing_resolve_ticket
from pyAppGen.pbc import service_ticketing_runtime_capabilities
from pyAppGen.pbc import service_ticketing_runtime_smoke
from pyAppGen.pbc import service_ticketing_set_parameter
from pyAppGen.pbc import service_ticketing_ui_contract
from pyAppGen.pbc import service_ticketing_verify_owned_table_boundary
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_OWNED_TABLES
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS


def test_service_ticketing_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = service_ticketing_runtime_capabilities()
    smoke = service_ticketing_runtime_smoke()

    assert runtime["format"] == "appgen.service-ticketing-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/service_ticketing"
    assert runtime["owned_tables"] == SERVICE_TICKETING_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("service_ticketing")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ServiceConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("service_ticketing",))["ok"] is True


def test_service_ticketing_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    state = service_ticketing_receive_event(
        state,
        {"event_id": "customer_ops", "event_type": "CustomerUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "tier": "enterprise", "health_score": 0.7}},
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {"event_id": "pref_ops", "event_type": "PreferenceChanged", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "preferred_channel": "chat", "locale": "en-US"}},
    )["state"]
    state = service_ticketing_create_sla_policy(
        state,
        {"sla_policy_id": "sla_ops", "tenant": "tenant_ops", "name": "Ops Critical", "priority": "critical", "first_response_minutes": 15, "resolution_target_hours": 8, "status": "active"},
    )["state"]
    opened = service_ticketing_open_ticket(
        state,
        {
            "ticket_id": "case_ops",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "subject": "Integration outage",
            "description": "Integration is down for enterprise customer",
            "channel": "chat",
            "priority": "critical",
            "region": "US",
            "sentiment": -0.7,
            "sla_policy_id": "sla_ops",
        },
    )
    state = opened["state"]
    assert opened["ticket"]["breach_risk"] > 0.5
    state = service_ticketing_assign_ticket(
        state,
        {"assignment_id": "assign_ops", "tenant": "tenant_ops", "ticket_id": "case_ops", "owner": "agent_ops", "queue": "tier_2", "skills": ("technical", "billing")},
    )["state"]
    state = service_ticketing_record_escalation(state, "case_ops", reason="customer_impact")["state"]
    state = service_ticketing_resolve_ticket(state, "case_ops", resolution="Integration credentials rotated")["state"]
    assert state["outbox"][-1]["idempotency_key"].startswith("service_ticketing:CustomerUpdated")

    workbench = service_ticketing_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["ticket_count"] == 1
    assert workbench["resolved_ticket_count"] == 1
    assert workbench["sla_policy_count"] == 1
    assert workbench["assignment_count"] == 1
    assert workbench["escalation_count"] >= 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = service_ticketing_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = service_ticketing_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "service_ticketing.ticket.write",
            "service_ticketing.assignment.write",
            "service_ticketing.escalation.write",
            "service_ticketing.event.consume",
            "service_ticketing.configure",
            "service_ticketing.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == SERVICE_TICKETING_OWNED_TABLES


def test_service_ticketing_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = service_ticketing_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        service_ticketing_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.service_ticketing.events",
                "retry_limit": 3,
                "default_region": "US",
                "supported_regions": ("US",),
                "channels": ("chat",),
                "priority_levels": ("critical",),
                "default_timezone": "UTC",
                "assignment_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Service Ticketing parameter"):
        service_ticketing_set_parameter(state, "stream_engine", 1)

    failed = service_ticketing_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "CustomerUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_fail"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = service_ticketing_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("support_ticket", "sla_policy", "case_assignment", "escalation_event")
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = service_ticketing_empty_state()
    state = service_ticketing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.service_ticketing.events",
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "channels": ("email", "chat", "portal"),
            "priority_levels": ("low", "medium", "high", "critical"),
            "default_timezone": "UTC",
            "assignment_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("sla_breach_risk_threshold", 0.7),
        ("auto_escalation_threshold", 0.95),
        ("sentiment_risk_weight", 0.3),
        ("priority_weight", 0.3),
        ("customer_tier_weight", 0.2),
        ("queue_load_weight", 0.2),
        ("first_response_minutes", 30),
        ("resolution_target_hours", 24),
        ("max_open_cases_per_owner", 25),
        ("workbench_limit", 50),
    ):
        state = service_ticketing_set_parameter(state, name, value)["state"]
    state = service_ticketing_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "service_ticketing",
            "status": "active",
            "allowed_regions": ("US",),
            "allowed_channels": ("email", "chat", "portal"),
            "allowed_priorities": ("medium", "high", "critical"),
            "assignment_policy": {"default_queue": "tier_2", "default_owner": "agent_ops", "skills": ("technical", "billing")},
            "escalation_policy": {"critical_queue": "priority_response", "breach_owner": "manager_ops"},
        },
    )["state"]
    return state
