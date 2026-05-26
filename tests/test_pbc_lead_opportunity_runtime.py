import pytest

from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_OWNED_TABLES
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_RUNTIME_TABLES
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_advance_opportunity
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_build_api_contract
from pyAppGen.pbcs.lead_opportunity import implementation_contract as lead_opportunity_implementation_contract
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_build_release_evidence
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_build_schema_contract
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_build_service_contract
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_build_workbench_view
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_configure_runtime
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_create_account_hierarchy
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_create_lead
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_create_opportunity
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_empty_state
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_permissions_contract
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_qualify_lead
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_receive_event
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_record_sales_activity
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_register_rule
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_register_schema_extension
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_render_workbench
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_runtime_capabilities
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_runtime_smoke
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_set_parameter
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_ui_contract
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_verify_owned_table_boundary
from pyAppGen.pbcs.lead_opportunity import lead_opportunity_win_opportunity


def test_lead_opportunity_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = lead_opportunity_runtime_capabilities()
    smoke = lead_opportunity_runtime_smoke()

    assert runtime["format"] == "appgen.lead-opportunity-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/lead_opportunity"
    assert runtime["owned_tables"] == LEAD_OPPORTUNITY_OWNED_TABLES
    assert runtime["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert len(runtime["standard_features"]) >= 30
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert "quote_proposal_handoff" in runtime["standard_features"]
    assert "coaching_insights" in runtime["standard_features"]
    assert "owned_datastore_boundary" in runtime["standard_features"]
    assert "release_gate" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    direct_contract = lead_opportunity_implementation_contract()
    assert direct_contract["pbc"] == "lead_opportunity"
    assert direct_contract["advanced_runtime"]["ok"] is True
    assert direct_contract["owned_tables"] == LEAD_OPPORTUNITY_OWNED_TABLES
    assert direct_contract["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert direct_contract["required_event_topic"] == LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
    assert direct_contract["consumes"] == LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES
    assert direct_contract["emits"] == LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES
    assert direct_contract["schema_contract"]["ok"] is True
    assert len(direct_contract["schema_contract"]["owned_tables"]) >= 18
    assert direct_contract["service_contract"]["ok"] is True
    assert direct_contract["release_evidence_contract"]["ok"] is True
    assert not direct_contract["release_evidence_contract"]["blocking_gaps"]
    assert direct_contract["boundary_contract"]["ok"] is True

    schema = lead_opportunity_build_schema_contract()
    service = lead_opportunity_build_service_contract()
    release = lead_opportunity_build_release_evidence()
    assert schema["runtime_tables"][0]["table"] == LEAD_OPPORTUNITY_RUNTIME_TABLES[0]
    assert len(schema["migrations"]) == len(LEAD_OPPORTUNITY_OWNED_TABLES)
    assert len(schema["models"]) == len(LEAD_OPPORTUNITY_OWNED_TABLES)
    assert service["event_contract"]["required_topic"] == LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
    assert service["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert release["ok"] is True
    assert release["workbench"]["binding_evidence"]["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert direct_contract["ui_contract"]["ok"] is True
    assert "RevenueConfigurationPanel" in direct_contract["ui_contract"]["fragments"]
    assert direct_contract["permissions_contract"]["action_permissions"]["win_opportunity"] == "lead_opportunity.opportunity.write"


def test_lead_opportunity_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    extension = lead_opportunity_register_schema_extension(
        state, "opportunity", {"mutual_action_plan": "jsonb"}
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1
    assert extension["extension"]["migration_descriptor"].endswith("_opportunity.sql")
    state = lead_opportunity_receive_event(
        state,
        {"event_id": "segment_ops", "event_type": "CustomerSegmentUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "segment": "enterprise", "fit_score": 0.9}},
    )["state"]
    state = lead_opportunity_create_account_hierarchy(
        state,
        {"account_id": "acct_ops", "tenant": "tenant_ops", "name": "Ops Account", "region": "US", "parent_account_id": None, "customer_id": "cust_ops", "owner": "seller_ops"},
    )["state"]
    state = lead_opportunity_create_lead(
        state,
        {
            "lead_id": "lead_ops",
            "tenant": "tenant_ops",
            "account_id": "acct_ops",
            "customer_id": "cust_ops",
            "email": "buyer@example.com",
            "company": "Ops Account",
            "source": "partner",
            "region": "US",
            "currency": "USD",
            "engagement_score": 0.84,
            "estimated_value": 90000.0,
        },
    )["state"]
    qualified = lead_opportunity_qualify_lead(state, "lead_ops")
    state = qualified["state"]
    assert qualified["lead"]["status"] == "qualified"
    state = lead_opportunity_create_opportunity(
        state,
        {"opportunity_id": "opp_ops", "tenant": "tenant_ops", "lead_id": "lead_ops", "account_id": "acct_ops", "name": "Ops Expansion", "amount": 90000.0, "currency": "USD", "stage": "qualified", "close_date": "2026-06-30"},
    )["state"]
    state = lead_opportunity_record_sales_activity(
        state,
        {"activity_id": "act_ops", "tenant": "tenant_ops", "opportunity_id": "opp_ops", "activity_type": "meeting", "subject": "Discovery", "sentiment": 0.88, "occurred_at": "2026-05-26T00:00:00Z", "owner": "seller_ops"},
    )["state"]
    state = lead_opportunity_advance_opportunity(state, "opp_ops", "proposal")["state"]
    state = lead_opportunity_win_opportunity(state, "opp_ops")["state"]
    assert state["outbox"][-1]["idempotency_key"].startswith("lead_opportunity:CustomerUpdated")

    workbench = lead_opportunity_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["lead_count"] == 1
    assert workbench["qualified_lead_count"] == 1
    assert workbench["opportunity_count"] == 1
    assert workbench["won_opportunity_count"] == 1
    assert workbench["activity_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert workbench["binding_evidence"]["configuration"] == {
        "bound": True,
        "database_backend": "postgresql",
        "event_contract": "AppGen-X",
        "event_topic": LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC,
        "visible_event_contracts": ("AppGen-X",),
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "supported_fields": (
            "database_backend",
            "event_topic",
            "retry_limit",
            "default_currency",
            "supported_currencies",
            "supported_regions",
            "pipeline_stages",
            "default_timezone",
            "assignment_mode",
            "workbench_limit",
        ),
    }
    assert workbench["binding_evidence"]["rules"] == (
        {
            "rule_id": "rule_ops",
            "scope": "lead_opportunity",
            "compiled_hash": state["rules"]["rule_ops"]["compiled_hash"],
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "allowed_regions",
                "allowed_currencies",
                "allowed_segments",
                "qualification_policy",
                "assignment_policy",
            ),
        },
    )
    assert workbench["binding_evidence"]["parameters"]["supported"][-1] == "workbench_limit"
    assert workbench["binding_evidence"]["parameters"]["active"][0] == "deal_slippage_threshold"

    ui_contract = lead_opportunity_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = lead_opportunity_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "lead_opportunity.lead.write",
            "lead_opportunity.opportunity.write",
            "lead_opportunity.activity.write",
            "lead_opportunity.event.consume",
            "lead_opportunity.configure",
            "lead_opportunity.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == LEAD_OPPORTUNITY_OWNED_TABLES
    assert rendered["binding_evidence"]["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES

    api_contract = lead_opportunity_build_api_contract()
    assert api_contract["database_backends"] == LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
    assert api_contract["event_contract"] == "AppGen-X"
    assert api_contract["required_event_topic"] == LEAD_OPPORTUNITY_REQUIRED_EVENT_TOPIC
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["user_selectable_event_contract"] is False
    assert api_contract["shared_table_access"] is False
    assert api_contract["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert api_contract["events"]["emits"] == LEAD_OPPORTUNITY_EMITTED_EVENT_TYPES
    assert api_contract["events"]["consumes"] == LEAD_OPPORTUNITY_CONSUMED_EVENT_TYPES
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "create_account_hierarchy",
        "create_lead",
        "qualify_lead",
        "create_opportunity",
        "record_sales_activity",
        "advance_opportunity",
        "win_opportunity",
        "receive_event",
    }
    assert {route["route"] for route in api_contract["routes"]} >= {
        "GET /lead-opportunity/schema-contract",
        "GET /lead-opportunity/service-contract",
        "GET /lead-opportunity/release-evidence",
    }
    permissions = lead_opportunity_permissions_contract()
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "lead_opportunity.audit"
    assert permissions["action_permissions"]["build_schema_contract"] == "lead_opportunity.audit"
    assert permissions["action_permissions"]["build_service_contract"] == "lead_opportunity.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "lead_opportunity.audit"


def test_lead_opportunity_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = lead_opportunity_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        lead_opportunity_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.lead_opportunity.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "pipeline_stages": ("prospect", "qualified", "won"),
                "default_timezone": "UTC",
                "assignment_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Lead Opportunity parameter"):
        lead_opportunity_set_parameter(state, "stream_engine", 1)

    failed = lead_opportunity_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "CustomerSegmentUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_fail"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert failed["handler"]["runtime_table"] == LEAD_OPPORTUNITY_RUNTIME_TABLES[2]
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = lead_opportunity_verify_owned_table_boundary(
        (
            "lead",
            "opportunity",
            "account_hierarchy",
            "sales_activity",
            "CustomerSegmentUpdated",
            "customer_segment_projection",
            "lead_opportunity_appgen_outbox_event",
        )
    )
    assert boundary["ok"] is True
    assert {"lead", "opportunity", "account_hierarchy", "sales_activity"} <= set(boundary["owned_tables"])
    assert boundary["runtime_tables"] == LEAD_OPPORTUNITY_RUNTIME_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    assert "customer_segment_projection" in boundary["declared_dependencies"]["api_projections"]
    violated = lead_opportunity_verify_owned_table_boundary(("customer",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer",)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        lead_opportunity_register_schema_extension(state, "customer", {"email": "text"})


def _configured_state() -> dict:
    state = lead_opportunity_empty_state()
    state = lead_opportunity_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.lead_opportunity.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "pipeline_stages": ("prospect", "qualified", "proposal", "negotiation", "won", "lost"),
            "default_timezone": "UTC",
            "assignment_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("qualification_score_threshold", 0.65),
        ("win_probability_threshold", 0.7),
        ("stale_activity_days", 21),
        ("forecast_confidence_floor", 0.7),
        ("deal_slippage_threshold", 0.6),
        ("lead_source_weight", 0.3),
        ("segment_fit_weight", 0.4),
        ("engagement_weight", 0.3),
        ("max_open_opportunities_per_account", 10),
        ("workbench_limit", 50),
    ):
        state = lead_opportunity_set_parameter(state, name, value)["state"]
    state = lead_opportunity_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "lead_opportunity",
            "status": "active",
            "allowed_regions": ("US",),
            "allowed_currencies": ("USD",),
            "allowed_segments": ("growth", "enterprise"),
            "qualification_policy": {"minimum_score": 0.65, "required_fields": ("email", "company")},
            "assignment_policy": {"mode": "territory", "default_owner": "seller_ops"},
        },
    )["state"]
    return state
