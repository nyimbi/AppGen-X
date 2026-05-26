import pytest

from pyAppGen.pbc import TREASURY_CASH_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import treasury_cash_build_cash_position
from pyAppGen.pbc import treasury_cash_build_release_evidence
from pyAppGen.pbc import treasury_cash_build_schema_contract
from pyAppGen.pbc import treasury_cash_build_service_contract
from pyAppGen.pbc import treasury_cash_build_workbench_view
from pyAppGen.pbc import treasury_cash_capture_bank_balance
from pyAppGen.pbc import treasury_cash_configure_runtime
from pyAppGen.pbc import treasury_cash_empty_state
from pyAppGen.pbc import treasury_cash_forecast_cash
from pyAppGen.pbc import treasury_cash_ingest_bank_statement
from pyAppGen.pbc import treasury_cash_optimize_liquidity
from pyAppGen.pbc import treasury_cash_reconcile_statement
from pyAppGen.pbc import treasury_cash_register_bank_account
from pyAppGen.pbc import treasury_cash_register_rule
from pyAppGen.pbc import treasury_cash_render_workbench
from pyAppGen.pbc import treasury_cash_runtime_capabilities
from pyAppGen.pbc import treasury_cash_runtime_smoke
from pyAppGen.pbc import treasury_cash_set_parameter
from pyAppGen.pbc import treasury_cash_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.treasury_cash import TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.treasury_cash import TREASURY_CASH_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.treasury_cash import TREASURY_CASH_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.treasury_cash import TREASURY_CASH_OWNED_TABLES
from pyAppGen.pbcs.treasury_cash import TREASURY_CASH_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.treasury_cash import implementation_contract as treasury_cash_package_contract
from pyAppGen.pbcs.treasury_cash import treasury_cash_build_api_contract
from pyAppGen.pbcs.treasury_cash import treasury_cash_permissions_contract
from pyAppGen.pbcs.treasury_cash import treasury_cash_receive_event
from pyAppGen.pbcs.treasury_cash import treasury_cash_register_schema_extension
from pyAppGen.pbcs.treasury_cash import treasury_cash_verify_owned_table_boundary


def test_treasury_cash_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = treasury_cash_runtime_capabilities()
    smoke = treasury_cash_runtime_smoke()

    assert runtime["format"] == "appgen.treasury-cash-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/treasury_cash"
    assert runtime["owned_tables"] == TREASURY_CASH_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 35
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "bank_signatory_management" in runtime["standard_features"]
    assert "statement_line_hash_chain" in runtime["standard_features"]
    assert "reconciliation_exception_management" in runtime["standard_features"]
    assert "forecast_line_confidence_bands" in runtime["standard_features"]
    assert "payment_rail_routing" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert len(runtime["standard_features"]) >= 18
    assert smoke["ok"] is True
    assert set(TREASURY_CASH_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("treasury_cash")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TreasuryConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TREASURY_CASH_ADVANCED_CAPABILITY_KEYS)

    package_contract = treasury_cash_package_contract()
    assert package_contract["api_contract"]["event_contract"] == "AppGen-X"
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["permissions_contract"]["action_permissions"]["receive_event"] == "treasury_cash.event"
    assert package_contract["owned_tables"] == TREASURY_CASH_OWNED_TABLES
    assert package_contract["allowed_database_backends"] == TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
    assert package_contract["required_event_topic"] == TREASURY_CASH_REQUIRED_EVENT_TOPIC
    assert package_contract["consumes"] == TREASURY_CASH_CONSUMED_EVENT_TYPES
    assert package_contract["emits"] == TREASURY_CASH_EMITTED_EVENT_TYPES

    schema = treasury_cash_build_schema_contract()
    service = treasury_cash_build_service_contract()
    release = treasury_cash_build_release_evidence()
    assert schema["format"] == "appgen.treasury-cash-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(TREASURY_CASH_OWNED_TABLES)
    assert len(schema["migrations"]) == len(TREASURY_CASH_OWNED_TABLES)
    assert {
        "treasury_cash_bank_account_signatory",
        "treasury_cash_statement_line",
        "treasury_cash_cash_forecast_line",
        "treasury_cash_payment_rail_route",
        "treasury_cash_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.treasury-cash-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 28
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.treasury-cash-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert pbc_implementation_release_audit(("treasury_cash",))["ok"] is True
    assert pbc_implemented_capability_audit(("treasury_cash",))["ok"] is True


def test_treasury_cash_runtime_handles_core_treasury_workflows() -> None:
    state = treasury_cash_empty_state()
    state = treasury_cash_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TREASURY_CASH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire"),
            "workbench_limit": 50,
        },
    )["state"]
    state = treasury_cash_set_parameter(state, "minimum_liquidity_buffer", 2000)["state"]
    state = treasury_cash_set_parameter(state, "counterparty_risk_threshold", 0.3)["state"]
    state = treasury_cash_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "liquidity",
            "minimum_liquidity_buffer": 2000,
            "dual_approval_required": True,
            "status": "active",
        },
    )["state"]
    state = treasury_cash_register_bank_account(
        state,
        {
            "account_id": "bank_ops",
            "tenant": "tenant_ops",
            "legal_entity": "entity_ops",
            "bank_id": "bank_ops_id",
            "currency": "USD",
            "country": "US",
            "signatories": ("treasurer", "controller"),
            "identity": {"did": "did:appgen:bank-ops", "issuer": "trusted_registry", "status": "active"},
            "risk_signals": {"sanction_hits": 0, "latency_risk": 0.01, "capital_risk": 0.02},
        },
    )["state"]
    state = treasury_cash_capture_bank_balance(
        state,
        {"balance_id": "bal_ops", "tenant": "tenant_ops", "account_id": "bank_ops", "value_date": "2026-05-26", "amount": 3000, "currency": "USD", "kind": "opening"},
    )["state"]
    state = treasury_cash_ingest_bank_statement(
        state,
        {
            "statement_id": "stmt_ops",
            "tenant": "tenant_ops",
            "account_id": "bank_ops",
            "lines": ({"line_id": "line_ops", "amount": -500, "currency": "USD", "narrative": "PAY supplier AP_INV_500 rail ach"},),
        },
    )["state"]

    reconciliation = treasury_cash_reconcile_statement(
        state,
        "stmt_ops",
        expected_flows=({"flow_id": "flow_ops", "amount": -500, "reference": "AP_INV_500"},),
    )
    assert reconciliation["ok"] is True
    assert reconciliation["auto_matched"] == 1

    position = treasury_cash_build_cash_position(state, tenant="tenant_ops", value_date="2026-05-26")
    assert position["available_cash"] == 2500
    forecast = treasury_cash_forecast_cash(state, "tenant_ops", inflows=(1000,), outflows=(400,))
    assert forecast["forecast"][0]["amount"] == 600
    optimization = treasury_cash_optimize_liquidity(
        state,
        tenant="tenant_ops",
        target_balance=2000,
        funding_options=(
            {"source": "cash_pool", "available": 2500, "cost": 0.01, "risk": 0.03},
            {"source": "credit_line", "available": 5000, "cost": 0.05, "risk": 0.05},
        ),
    )
    assert optimization["selected_source"] == "cash_pool"

    workbench = treasury_cash_build_workbench_view(state, tenant="tenant_ops", value_date="2026-05-26")
    assert workbench["available_cash"] == 2500
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2
    assert workbench["owned_tables"] == TREASURY_CASH_OWNED_TABLES
    assert workbench["inbox_table"] == "treasury_cash_appgen_inbox_event"

    ui_contract = treasury_cash_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == TREASURY_CASH_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["event_surfaces"]["emits"] == TREASURY_CASH_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == TREASURY_CASH_CONSUMED_EVENT_TYPES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False
    assert "minimum_liquidity_buffer" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = treasury_cash_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "treasury_cash.bank",
            "treasury_cash.balance",
            "treasury_cash.statement",
            "treasury_cash.reconcile",
            "treasury_cash.position",
            "treasury_cash.forecast",
            "treasury_cash.funding",
            "treasury_cash.payment",
            "treasury_cash.investment",
            "treasury_cash.debt",
            "treasury_cash.fx",
            "treasury_cash.configure",
            "treasury_cash.event",
            "treasury_cash.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 3
    assert rendered["inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == TREASURY_CASH_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_treasury_cash_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = treasury_cash_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        treasury_cash_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": TREASURY_CASH_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Treasury Cash parameter"):
        treasury_cash_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match=TREASURY_CASH_REQUIRED_EVENT_TOPIC):
        treasury_cash_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.treasury.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        treasury_cash_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": TREASURY_CASH_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "stream_engine": "user_picker",
            },
        )


def test_treasury_cash_hardened_contract_handles_schema_events_and_boundaries() -> None:
    state = treasury_cash_empty_state()
    state = treasury_cash_configure_runtime(
        state,
        {
            "database_backend": "mariadb",
            "event_topic": TREASURY_CASH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire"),
        },
    )["state"]

    extension = treasury_cash_register_schema_extension(
        state,
        "treasury_cash_liquidity_plan",
        {"scenario_metadata": "jsonb", "confidence": "decimal"},
    )
    assert extension["ok"] is True
    state = extension["state"]
    assert state["schema_extensions"]["treasury_cash_liquidity_plan"]["scenario_metadata"] == "jsonb"

    with pytest.raises(ValueError, match="owned tables"):
        treasury_cash_register_schema_extension(state, "ap_invoice", {"external_field": "text"})

    invalid = treasury_cash_register_schema_extension(state, "treasury_cash_liquidity_plan", {"BadField": "text"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    event = {
        "event_id": "evt_payable_001",
        "event_type": "PayablePaymentScheduled",
        "payload": {"tenant": "tenant_ops", "schedule_id": "sched_ops", "amount": 500, "currency": "USD"},
    }
    received = treasury_cash_receive_event(state, event)
    assert received["ok"] is True
    assert received["handler"]["status"] == "processed"
    state = received["state"]
    assert state["payable_payment_projections"]["sched_ops"]["amount"] == 500
    assert len(state["inbox"]) == 1

    duplicate = treasury_cash_receive_event(state, event)
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert duplicate["state"] is state

    failed = treasury_cash_receive_event(
        state,
        {"event_id": "evt_bad_001", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "retrying"
    failed = treasury_cash_receive_event(failed["state"], {"event_id": "evt_bad_001", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}})
    assert failed["handler"]["status"] == "dead_letter"
    assert failed["state"]["dead_letter"][0]["reason"] == "unsupported_or_failed_treasury_event"

    api = treasury_cash_build_api_contract()
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert api["shared_table_access"] is False
    assert api["database_backends"] == TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == TREASURY_CASH_EMITTED_EVENT_TYPES
    assert api["consumes"] == TREASURY_CASH_CONSUMED_EVENT_TYPES
    assert any(route.get("command") == "receive_event" for route in api["routes"])

    permissions = treasury_cash_permissions_contract()
    assert permissions["action_permissions"]["register_schema_extension"] == "treasury_cash.configure"
    assert permissions["action_permissions"]["receive_event"] == "treasury_cash.event"

    valid_boundary = treasury_cash_verify_owned_table_boundary(
        ("treasury_cash_bank_account", "treasury_cash_appgen_outbox_event", "PayablePaymentScheduled", "fx_rate_projection")
    )
    assert valid_boundary["ok"] is True
    invalid_boundary = treasury_cash_verify_owned_table_boundary(("gl_journal_entry",))
    assert invalid_boundary["ok"] is False
    assert invalid_boundary["violations"] == ("gl_journal_entry",)
