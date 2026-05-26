import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import service_ticketing_assign_ticket
from pyAppGen.pbc import service_ticketing_build_api_contract
from pyAppGen.pbc import service_ticketing_build_workbench_view
from pyAppGen.pbc import service_ticketing_configure_runtime
from pyAppGen.pbc import service_ticketing_create_sla_policy
from pyAppGen.pbc import service_ticketing_empty_state
from pyAppGen.pbc import service_ticketing_open_ticket
from pyAppGen.pbc import service_ticketing_permissions_contract
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
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_OWNED_TABLES
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.service_ticketing import SERVICE_TICKETING_RUNTIME_TABLES
from pyAppGen.pbcs.service_ticketing import implementation_contract
from pyAppGen.pbcs.service_ticketing import service_ticketing_build_release_evidence
from pyAppGen.pbcs.service_ticketing import service_ticketing_build_schema_contract
from pyAppGen.pbcs.service_ticketing import service_ticketing_build_service_contract
from pyAppGen.pbcs.service_ticketing import service_ticketing_register_schema_extension
from pyAppGen.pbcs.service_ticketing import service_ticketing_run_control_tests
from pyAppGen.pbcs.service_ticketing import service_ticketing_ui_binding_contract


def test_service_ticketing_runtime_exposes_hardened_contracts() -> None:
    runtime = service_ticketing_runtime_capabilities()
    smoke = service_ticketing_runtime_smoke()
    schema = service_ticketing_build_schema_contract()
    service = service_ticketing_build_service_contract()
    release = service_ticketing_build_release_evidence()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.service-ticketing-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/service_ticketing"
    assert runtime["owned_tables"] == SERVICE_TICKETING_OWNED_TABLES
    assert runtime["runtime_tables"] == SERVICE_TICKETING_RUNTIME_TABLES
    assert runtime["required_event_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    assert len(runtime["standard_features"]) >= 20
    assert "queue_management" in runtime["standard_features"]
    assert "automation_insight" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    assert schema["ok"] is True
    assert len(schema["tables"]) == len(SERVICE_TICKETING_OWNED_TABLES)
    assert len(schema["migrations"]) == len(SERVICE_TICKETING_OWNED_TABLES)
    assert len(schema["models"]) == len(SERVICE_TICKETING_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == SERVICE_TICKETING_RUNTIME_TABLES

    assert service["ok"] is True
    assert service["event_contract"]["contract"] == "AppGen-X"
    assert service["event_contract"]["required_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    assert service["event_contract"]["stream_engine_picker_visible"] is False
    assert "build_release_evidence" in service["query_methods"]
    assert "receive_event" in service["idempotent_handlers"]

    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["required_event_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    assert contract["consumed_events"] == SERVICE_TICKETING_CONSUMED_EVENT_TYPES
    assert contract["emitted_events"] == SERVICE_TICKETING_EMITTED_EVENT_TYPES
    assert contract["ui_binding_contract"]["binding_evidence"]["runtime_tables"] == SERVICE_TICKETING_RUNTIME_TABLES

    package_contract = pbc_implementation_contract("service_ticketing")
    assert package_contract["source_package"]["ok"] is True
    assert package_contract["source_package"]["schema_contract"]["ok"] is True
    assert package_contract["source_package"]["service_contract"]["ok"] is True
    assert package_contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert pbc_implementation_release_audit(("service_ticketing",))["ok"] is True


def test_service_ticketing_runtime_covers_table_stakes_and_ui_bindings() -> None:
    state = _configured_state()
    extension = service_ticketing_register_schema_extension(
        state,
        "knowledge_suggestion",
        {"retrieval_trace": "jsonb"},
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1

    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "customer_ops",
            "event_type": "CustomerUpdated",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "tier": "enterprise",
                "health_score": 0.7,
                "entitlements": ("priority_support", "field_service"),
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "pref_ops",
            "event_type": "PreferenceChanged",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "preferred_channel": "chat",
                "locale": "en-US",
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "ent_ops",
            "event_type": "EntitlementUpdated",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "tier": "enterprise",
                "entitlements": ("priority_support", "field_service"),
            },
        },
    )["state"]
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "knowledge_ops",
            "event_type": "KnowledgeSuggested",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "ticket_id": "case_ops",
                "article_ref": "kb://service/recovery",
                "recommendation": "Follow the recovery checklist",
                "confidence": 0.84,
            },
        },
    )["state"]
    state = service_ticketing_create_sla_policy(
        state,
        {
            "sla_policy_id": "sla_ops",
            "tenant": "tenant_ops",
            "name": "Ops Critical",
            "priority": "critical",
            "first_response_minutes": 15,
            "resolution_target_hours": 8,
            "status": "active",
        },
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
    assert opened["ticket"]["queue"] == "tier_2"

    state = service_ticketing_assign_ticket(
        state,
        {
            "assignment_id": "assign_ops",
            "tenant": "tenant_ops",
            "ticket_id": "case_ops",
            "owner": "agent_ops",
            "queue": "tier_2",
            "skills": ("technical", "billing"),
        },
    )["state"]
    state = service_ticketing_record_escalation(state, "case_ops", reason="customer_impact")["state"]
    state = service_ticketing_resolve_ticket(
        state,
        "case_ops",
        resolution="Integration credentials rotated",
    )["state"]

    assert state["service_queues"]
    assert state["service_priorities"]
    assert state["ticket_interactions"]
    assert state["knowledge_suggestions"]
    assert state["entitlement_snapshots"]
    assert state["case_lifecycle_states"]["case_ops"]["stage"] == "resolved"
    assert state["field_service_handoffs"]
    assert state["customer_updates"]
    assert state["resolution_records"]
    assert state["csat_responses"]
    assert state["ticket_audit_logs"]
    assert state["automation_insights"]
    assert any(item["event_type"] == "FieldServiceHandoffPrepared" for item in state["outbox"])
    assert any(item["event_type"] == "ResolutionRecorded" for item in state["outbox"])
    assert any(item["idempotency_key"].startswith("service_ticketing:CustomerUpdated") for item in state["outbox"])

    workbench = service_ticketing_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["ticket_count"] == 1
    assert workbench["resolved_ticket_count"] == 1
    assert workbench["queue_count"] >= 3
    assert workbench["priority_count"] >= 4
    assert workbench["sla_policy_count"] == 1
    assert workbench["assignment_count"] == 1
    assert workbench["escalation_count"] >= 1
    assert workbench["interaction_count"] >= 1
    assert workbench["knowledge_suggestion_count"] >= 1
    assert workbench["entitlement_count"] >= 1
    assert workbench["handoff_count"] >= 1
    assert workbench["customer_update_count"] >= 1
    assert workbench["resolution_count"] >= 1
    assert workbench["csat_pending_count"] >= 1
    assert workbench["audit_count"] >= 1
    assert workbench["automation_insight_count"] >= 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["binding_evidence"]["runtime_tables"] == SERVICE_TICKETING_RUNTIME_TABLES
    assert workbench["binding_evidence"]["eventing"]["required_event_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC

    ui_contract = service_ticketing_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "ServiceQueueManager" in ui_contract["fragments"]
    assert "FieldServiceHandoffPanel" in ui_contract["fragments"]
    rendered = service_ticketing_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "service_ticketing.ticket.write",
            "service_ticketing.assignment.write",
            "service_ticketing.escalation.write",
            "service_ticketing.customer.update",
            "service_ticketing.event.consume",
            "service_ticketing.configure",
            "service_ticketing.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == SERVICE_TICKETING_OWNED_TABLES
    assert rendered["binding_evidence"]["runtime_tables"] == SERVICE_TICKETING_RUNTIME_TABLES
    assert rendered["binding_evidence"]["eventing"]["event_contract"] == "AppGen-X"

    ui_binding = service_ticketing_ui_binding_contract()
    assert ui_binding["binding_evidence"]["outbox_table"] == SERVICE_TICKETING_RUNTIME_TABLES[0]
    assert ui_binding["binding_evidence"]["event_contract"] == "AppGen-X"


def test_service_ticketing_contracts_prove_boundary_idempotency_and_dead_letters() -> None:
    state = service_ticketing_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        service_ticketing_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
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
    with pytest.raises(ValueError, match="does not expose stream-engine pickers"):
        service_ticketing_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_region": "US",
                "supported_regions": ("US",),
                "channels": ("chat",),
                "priority_levels": ("critical",),
                "default_timezone": "UTC",
                "assignment_mode": "policy",
                "workbench_limit": 50,
                "stream_engine": "hidden",
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Service Ticketing parameter"):
        service_ticketing_set_parameter(state, "stream_engine", 1)

    handled = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_dupe",
            "event_type": "CustomerUpdated",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "tier": "standard"},
        },
    )
    state = handled["state"]
    duplicate = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_dupe",
            "event_type": "CustomerUpdated",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "tier": "standard"},
        },
    )
    assert handled["handler"]["status"] == "handled"
    assert duplicate["handler"]["status"] == "duplicate"

    failed = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_fail",
            "event_type": "KnowledgeSuggested",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "ticket_id": "case_fail"},
        },
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = service_ticketing_verify_owned_table_boundary(
        (
            "support_ticket",
            "service_queue",
            "knowledge_suggestion",
            SERVICE_TICKETING_RUNTIME_TABLES[0],
            "customer_context_projection",
            "POST /field-service/handoffs",
            "KnowledgeSuggested",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == SERVICE_TICKETING_OWNED_TABLES
    assert boundary["runtime_tables"] == SERVICE_TICKETING_RUNTIME_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    assert "entitlement_projection" in boundary["declared_dependencies"]["api_projections"]
    violated = service_ticketing_verify_owned_table_boundary(("customer_profile",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer_profile",)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        service_ticketing_register_schema_extension(state, "customer_profile", {"email": "text"})

    api_contract = service_ticketing_build_api_contract()
    assert api_contract["database_backends"] == SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
    assert api_contract["event_contract"] == "AppGen-X"
    assert api_contract["required_event_topic"] == SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["shared_table_access"] is False
    assert {route["query"] for route in api_contract["routes"] if "query" in route} >= {
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    }

    permissions = service_ticketing_permissions_contract()
    assert permissions["action_permissions"]["register_schema_extension"] == "service_ticketing.configure"
    assert permissions["action_permissions"]["build_release_evidence"] == "service_ticketing.audit"
    assert permissions["action_permissions"]["resolve_ticket"] == "service_ticketing.customer.update"

    service_contract = service_ticketing_build_service_contract()
    assert service_contract["transaction_boundary"] == "service_ticketing_owned_datastore_plus_appgen_outbox"
    assert service_contract["retry_policy"]["dead_letter_table"] == SERVICE_TICKETING_RUNTIME_TABLES[2]
    assert service_contract["event_contract"]["consumes"] == SERVICE_TICKETING_CONSUMED_EVENT_TYPES

    control = service_ticketing_run_control_tests(_exercised_state())
    assert control["ok"] is True

    release = service_ticketing_build_release_evidence()
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def _configured_state() -> dict:
    state = service_ticketing_empty_state()
    state = service_ticketing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
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
            "assignment_policy": {
                "default_queue": "tier_2",
                "default_owner": "agent_ops",
                "skills": ("technical", "billing"),
            },
            "escalation_policy": {
                "critical_queue": "priority_response",
                "breach_owner": "manager_ops",
            },
        },
    )["state"]
    return state


def _exercised_state() -> dict:
    state = _configured_state()
    state = service_ticketing_receive_event(
        state,
        {
            "event_id": "evt_customer",
            "event_type": "CustomerUpdated",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "cust_ops",
                "tier": "enterprise",
                "entitlements": ("priority_support",),
            },
        },
    )["state"]
    state = service_ticketing_create_sla_policy(
        state,
        {
            "sla_policy_id": "sla_ops",
            "tenant": "tenant_ops",
            "name": "Ops Critical",
            "priority": "critical",
            "first_response_minutes": 15,
            "resolution_target_hours": 8,
            "status": "active",
        },
    )["state"]
    state = service_ticketing_open_ticket(
        state,
        {
            "ticket_id": "case_ops",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "subject": "Runtime proof",
            "description": "Control-test proof case",
            "channel": "chat",
            "priority": "critical",
            "region": "US",
            "sentiment": -0.4,
            "sla_policy_id": "sla_ops",
        },
    )["state"]
    state = service_ticketing_assign_ticket(
        state,
        {
            "assignment_id": "assign_ops",
            "tenant": "tenant_ops",
            "ticket_id": "case_ops",
            "owner": "agent_ops",
            "queue": "tier_2",
            "skills": ("technical",),
        },
    )["state"]
    state = service_ticketing_record_escalation(state, "case_ops", reason="proof")["state"]
    state = service_ticketing_resolve_ticket(state, "case_ops", resolution="Resolved for control test")["state"]
    return state
