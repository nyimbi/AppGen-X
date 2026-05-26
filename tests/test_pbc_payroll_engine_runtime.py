import pytest

from pyAppGen.pbc import PAYROLL_ENGINE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbc import PAYROLL_ENGINE_CONSUMED_EVENT_TYPES
from pyAppGen.pbc import PAYROLL_ENGINE_EMITTED_EVENT_TYPES
from pyAppGen.pbc import PAYROLL_ENGINE_OWNED_TABLES
from pyAppGen.pbc import PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbc import payroll_engine_allocate_benefit
from pyAppGen.pbc import payroll_engine_apply_deduction
from pyAppGen.pbc import payroll_engine_build_api_contract
from pyAppGen.pbc import payroll_engine_build_workbench_view
from pyAppGen.pbc import payroll_engine_calculate_payslip
from pyAppGen.pbc import payroll_engine_configure_runtime
from pyAppGen.pbc import payroll_engine_create_payroll_run
from pyAppGen.pbc import payroll_engine_empty_state
from pyAppGen.pbc import payroll_engine_ingest_labor_hours
from pyAppGen.pbc import payroll_engine_post_payroll_run
from pyAppGen.pbc import payroll_engine_prepare_payroll_filing
from pyAppGen.pbc import payroll_engine_permissions_contract
from pyAppGen.pbc import payroll_engine_receive_event
from pyAppGen.pbc import payroll_engine_register_rule
from pyAppGen.pbc import payroll_engine_register_schema_extension
from pyAppGen.pbc import payroll_engine_render_workbench
from pyAppGen.pbc import payroll_engine_runtime_capabilities
from pyAppGen.pbc import payroll_engine_runtime_smoke
from pyAppGen.pbc import payroll_engine_set_parameter
from pyAppGen.pbc import payroll_engine_ui_contract
from pyAppGen.pbc import payroll_engine_upsert_worker_projection
from pyAppGen.pbc import payroll_engine_verify_owned_table_boundary
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_payroll_engine_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = payroll_engine_runtime_capabilities()
    smoke = payroll_engine_runtime_smoke()

    assert runtime["format"] == "appgen.payroll-engine-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/payroll_engine"
    assert runtime["owned_tables"] == PAYROLL_ENGINE_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 24
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(PAYROLL_ENGINE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("payroll_engine")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == PAYROLL_ENGINE_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "payroll_engine.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "PayrollConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(PAYROLL_ENGINE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("payroll_engine",))["ok"] is True
    assert pbc_implemented_capability_audit(("payroll_engine",))["ok"] is True

    api = payroll_engine_build_api_contract()
    permissions = payroll_engine_permissions_contract()
    assert api["format"] == "appgen.payroll-engine-api-contract.v1"
    assert api["owned_tables"] == PAYROLL_ENGINE_OWNED_TABLES
    assert api["database_backends"] == PAYROLL_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == PAYROLL_ENGINE_EMITTED_EVENT_TYPES
    assert api["consumes"] == PAYROLL_ENGINE_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /payroll-runs", "POST /payroll/events/inbox", "GET /payroll-workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["post_payroll_run"] == "payroll_engine.approve"


def test_payroll_engine_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = payroll_engine_empty_state()
    state = payroll_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_countries": ("US",),
            "allowed_payment_rails": ("ach",),
            "allowed_filing_channels": ("federal_e_file",),
            "payroll_precision": 2,
            "workbench_limit": 50,
        },
    )["state"]
    state = payroll_engine_set_parameter(state, "standard_period_hours", 40)["state"]
    state = payroll_engine_set_parameter(state, "overtime_multiplier", 1.5)["state"]
    state = payroll_engine_set_parameter(state, "supplemental_rate", 0.2)["state"]
    state = payroll_engine_set_parameter(state, "net_pay_floor", 0)["state"]
    state = payroll_engine_set_parameter(state, "approval_amount_threshold", 5000)["state"]
    state = payroll_engine_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "pay",
            "eligible_worker_types": ("employee",),
            "allowed_countries": ("US",),
            "deduction_limit_percent": 0.5,
            "benefit_classes": ("health", "retirement"),
            "filing_channels": {"US": "federal_e_file"},
            "garnishment_priority": ("court", "tax", "loan"),
            "status": "active",
        },
    )["state"]
    extension = payroll_engine_register_schema_extension(state, "payslip", {"equity_payload": "jsonb", "retro_adjustment_payload": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["payslip"]["retro_adjustment_payload"] == "jsonb"
    state = payroll_engine_upsert_worker_projection(
        state,
        {
            "employee_id": "emp_ops",
            "tenant": "tenant_ops",
            "worker_type": "employee",
            "country": "US",
            "legal_entity": "entity_ops",
            "currency": "USD",
            "hourly_rate": 25,
            "salary_per_period": 0,
            "identity": {"did": "did:appgen:emp-ops", "issuer": "trusted_registry", "status": "active"},
            "status": "active",
        },
    )["state"]
    run = payroll_engine_create_payroll_run(
        state,
        {
            "run_id": "run_ops",
            "tenant": "tenant_ops",
            "period": "2026-W22",
            "country": "US",
            "legal_entity": "entity_ops",
            "currency": "USD",
            "run_type": "regular",
        },
    )
    state = run["state"]
    assert run["payroll_run"]["status"] == "open"

    received_labor = payroll_engine_receive_event(
        state,
        {"event_id": "evt_labor_ops", "event_type": "LaborHoursApproved", "payload": {"tenant": "tenant_ops", "employee_id": "emp_ops", "period": "2026-W22", "approved_hours": 42, "overtime_hours": 2}},
    )
    state = received_labor["state"]
    assert received_labor["handler"]["status"] == "processed"
    duplicate = payroll_engine_receive_event(
        state,
        {"event_id": "evt_labor_ops", "event_type": "LaborHoursApproved", "payload": {"tenant": "tenant_ops", "employee_id": "emp_ops", "period": "2026-W22", "approved_hours": 42, "overtime_hours": 2}},
    )
    assert duplicate["duplicate"] is True
    payslip = payroll_engine_calculate_payslip(state, "run_ops", "emp_ops")
    state = payslip["state"]
    assert payslip["gross_pay"] == 1075
    assert payslip["tax_withheld"] == 215
    assert payslip["net_pay"] == 860

    deduction = payroll_engine_apply_deduction(
        state,
        "payslip_run_ops_emp_ops",
        {"deduction_id": "ded_ops", "deduction_type": "retirement", "amount": 100, "priority": "loan"},
    )
    state = deduction["state"]
    assert deduction["deduction"]["status"] == "applied"

    benefit = payroll_engine_allocate_benefit(
        state,
        "payslip_run_ops_emp_ops",
        {"benefit_id": "ben_ops", "benefit_type": "health", "employer_amount": 125, "employee_amount": 25},
    )
    state = benefit["state"]
    assert benefit["benefit"]["status"] == "allocated"

    posted = payroll_engine_post_payroll_run(state, "run_ops", approved_by="payroll_ops")
    state = posted["state"]
    assert posted["payroll_run"]["status"] == "posted"
    assert posted["handoffs"] == ("treasury_payment_batch", "ledger_journal_request", "tax_wage_base_projection")

    filing = payroll_engine_prepare_payroll_filing(state, "filing_ops", run_id="run_ops", jurisdiction="US", channel="federal_e_file")
    state = filing["state"]
    assert filing["filing"]["status"] == "prepared"
    assert state["outbox"][-1]["idempotency_key"] == "payroll_engine:PayrollFilingPrepared:payroll_evt_000006"

    workbench = payroll_engine_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["posted_run_count"] == 1
    assert workbench["payslip_count"] == 1
    assert workbench["deduction_count"] == 1
    assert workbench["benefit_count"] == 1
    assert workbench["filing_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == PAYROLL_ENGINE_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = payroll_engine_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["required_event_topic"] == PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == PAYROLL_ENGINE_OWNED_TABLES
    assert "standard_period_hours" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = payroll_engine_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "payroll_engine.run",
            "payroll_engine.approve",
            "payroll_engine.file",
            "payroll_engine.event",
            "payroll_engine.configure",
            "payroll_engine.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == PAYROLL_ENGINE_OWNED_TABLES

    boundary = payroll_engine_verify_owned_table_boundary(
        ("payslip", "LaborHoursApproved", "time_labor_projection", "POST /payment-batches", "payroll_engine_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = payroll_engine_verify_owned_table_boundary(("personnel_identity",))
    assert violation["ok"] is False
    assert violation["violations"] == ("personnel_identity",)


def test_payroll_engine_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = payroll_engine_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        payroll_engine_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        payroll_engine_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Payroll Engine parameter"):
        payroll_engine_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        payroll_engine_register_schema_extension(state, "personnel_identity", {"pay_class": "jsonb"})

    configured = payroll_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PAYROLL_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "allowed_countries": ("US",),
            "allowed_payment_rails": ("ach",),
            "allowed_filing_channels": ("federal_e_file",),
            "payroll_precision": 2,
            "workbench_limit": 50,
        },
    )["state"]
    retrying = payroll_engine_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = payroll_engine_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
