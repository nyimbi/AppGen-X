import pytest

from pyAppGen.pbc import lead_opportunity_advance_opportunity
from pyAppGen.pbc import lead_opportunity_build_workbench_view
from pyAppGen.pbc import lead_opportunity_configure_runtime
from pyAppGen.pbc import lead_opportunity_create_account_hierarchy
from pyAppGen.pbc import lead_opportunity_create_lead
from pyAppGen.pbc import lead_opportunity_create_opportunity
from pyAppGen.pbc import lead_opportunity_empty_state
from pyAppGen.pbc import lead_opportunity_qualify_lead
from pyAppGen.pbc import lead_opportunity_receive_event
from pyAppGen.pbc import lead_opportunity_record_sales_activity
from pyAppGen.pbc import lead_opportunity_register_rule
from pyAppGen.pbc import lead_opportunity_render_workbench
from pyAppGen.pbc import lead_opportunity_runtime_capabilities
from pyAppGen.pbc import lead_opportunity_runtime_smoke
from pyAppGen.pbc import lead_opportunity_set_parameter
from pyAppGen.pbc import lead_opportunity_ui_contract
from pyAppGen.pbc import lead_opportunity_verify_owned_table_boundary
from pyAppGen.pbc import lead_opportunity_win_opportunity
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_OWNED_TABLES
from pyAppGen.pbcs.lead_opportunity import LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS


def test_lead_opportunity_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = lead_opportunity_runtime_capabilities()
    smoke = lead_opportunity_runtime_smoke()

    assert runtime["format"] == "appgen.lead-opportunity-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/lead_opportunity"
    assert runtime["owned_tables"] == LEAD_OPPORTUNITY_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(LEAD_OPPORTUNITY_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("lead_opportunity")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "RevenueConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("lead_opportunity",))["ok"] is True


def test_lead_opportunity_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
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

    ui_contract = lead_opportunity_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == LEAD_OPPORTUNITY_ALLOWED_DATABASE_BACKENDS
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
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = lead_opportunity_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("lead", "opportunity", "account_hierarchy", "sales_activity")
    assert boundary["declared_dependencies"]["shared_tables"] == ()


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
