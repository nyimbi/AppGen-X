import pytest

from pyAppGen.pbcs.ar_credit import AR_CREDIT_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.ar_credit import AR_CREDIT_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.ar_credit import AR_CREDIT_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.ar_credit import AR_CREDIT_OWNED_TABLES
from pyAppGen.pbcs.ar_credit import AR_CREDIT_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.ar_credit import AR_CREDIT_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.ar_credit import ar_credit_apply_cash
from pyAppGen.pbcs.ar_credit import ar_credit_build_api_contract
from pyAppGen.pbcs.ar_credit import ar_credit_build_release_evidence
from pyAppGen.pbcs.ar_credit import ar_credit_build_schema_contract
from pyAppGen.pbcs.ar_credit import ar_credit_build_service_contract
from pyAppGen.pbcs.ar_credit import ar_credit_build_workbench_view
from pyAppGen.pbcs.ar_credit import ar_credit_calculate_aging
from pyAppGen.pbcs.ar_credit import ar_credit_configure_runtime
from pyAppGen.pbcs.ar_credit import ar_credit_create_credit_memo
from pyAppGen.pbcs.ar_credit import ar_credit_create_dunning_plan
from pyAppGen.pbcs.ar_credit import ar_credit_empty_state
from pyAppGen.pbcs.ar_credit import ar_credit_extend_credit
from pyAppGen.pbcs.ar_credit import ar_credit_forecast_revenue_to_cash
from pyAppGen.pbcs.ar_credit import ar_credit_generate_customer_statement
from pyAppGen.pbcs.ar_credit import ar_credit_issue_invoice
from pyAppGen.pbcs.ar_credit import ar_credit_issue_refund
from pyAppGen.pbcs.ar_credit import ar_credit_onboard_customer
from pyAppGen.pbcs.ar_credit import ar_credit_optimize_collection_strategy
from pyAppGen.pbcs.ar_credit import ar_credit_parse_remittance
from pyAppGen.pbcs.ar_credit import ar_credit_permissions_contract
from pyAppGen.pbcs.ar_credit import ar_credit_receive_event
from pyAppGen.pbcs.ar_credit import ar_credit_record_delivery_confirmation
from pyAppGen.pbcs.ar_credit import ar_credit_record_unapplied_cash
from pyAppGen.pbcs.ar_credit import ar_credit_recognize_revenue_schedule
from pyAppGen.pbcs.ar_credit import ar_credit_register_rule
from pyAppGen.pbcs.ar_credit import ar_credit_register_schema_extension
from pyAppGen.pbcs.ar_credit import ar_credit_render_workbench
from pyAppGen.pbcs.ar_credit import ar_credit_resolve_dispute
from pyAppGen.pbcs.ar_credit import ar_credit_route_collection
from pyAppGen.pbcs.ar_credit import ar_credit_run_control_tests
from pyAppGen.pbcs.ar_credit import ar_credit_runtime_capabilities
from pyAppGen.pbcs.ar_credit import ar_credit_runtime_smoke
from pyAppGen.pbcs.ar_credit import ar_credit_schedule_collection_action
from pyAppGen.pbcs.ar_credit import ar_credit_score_customer_default
from pyAppGen.pbcs.ar_credit import ar_credit_screen_customer_network
from pyAppGen.pbcs.ar_credit import ar_credit_set_parameter
from pyAppGen.pbcs.ar_credit import ar_credit_submit_e_invoice
from pyAppGen.pbcs.ar_credit import ar_credit_ui_contract
from pyAppGen.pbcs.ar_credit import ar_credit_verify_owned_table_boundary
from pyAppGen.pbcs.ar_credit import ar_credit_verify_revenue_proof
from pyAppGen.pbcs.ar_credit import ar_credit_write_off_receivable
from pyAppGen.pbcs.ar_credit import implementation_contract


def test_ar_credit_runtime_executes_standard_and_advanced_contracts() -> None:
    runtime = ar_credit_runtime_capabilities()
    smoke = ar_credit_runtime_smoke()

    assert runtime["format"] == "appgen.ar-credit-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/ar_credit"
    assert runtime["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 35
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert "customer_site_management" in runtime["standard_features"]
    assert "customer_credit_profile" in runtime["standard_features"]
    assert "invoice_line_management" in runtime["standard_features"]
    assert "cash_application_batching" in runtime["standard_features"]
    assert "dispute_case_management" in runtime["standard_features"]
    assert "revenue_recognition" in runtime["standard_features"]
    assert "e_invoice_submission" in runtime["standard_features"]
    assert "invoice_financing" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert set(runtime["capabilities"]) == set(AR_CREDIT_RUNTIME_CAPABILITY_KEYS)
    assert smoke["ok"] is True
    assert not smoke["blocking_gaps"]

    contract = implementation_contract()
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert contract["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert contract["allowed_database_backends"] == AR_CREDIT_ALLOWED_DATABASE_BACKENDS
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["required_event_topic"] == AR_CREDIT_REQUIRED_EVENT_TOPIC
    assert contract["consumes"] == AR_CREDIT_CONSUMED_EVENT_TYPES
    assert contract["emits"] == AR_CREDIT_EMITTED_EVENT_TYPES
    assert contract["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["api_contract"]["shared_table_access"] is False
    assert contract["permissions_contract"]["action_permissions"]["receive_event"] == "ar_credit.event"

    api = ar_credit_build_api_contract()
    schema = ar_credit_build_schema_contract()
    service = ar_credit_build_service_contract()
    release = ar_credit_build_release_evidence()
    permissions = ar_credit_permissions_contract()
    assert api["format"] == "appgen.ar-credit-api-contract.v1"
    assert api["database_backends"] == AR_CREDIT_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert api["emits"] == AR_CREDIT_EMITTED_EVENT_TYPES
    assert api["consumes"] == AR_CREDIT_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {
        "POST /ar/invoices",
        "POST /ar/events/inbox",
        "GET /ar/workbench",
    }
    assert schema["format"] == "appgen.ar-credit-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(AR_CREDIT_OWNED_TABLES)
    assert len(schema["migrations"]) == len(AR_CREDIT_OWNED_TABLES)
    assert {
        "ar_customer_credit_profile",
        "ar_invoice_line",
        "ar_cash_application",
        "ar_revenue_schedule_line",
        "ar_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.ar-credit-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.ar-credit-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "ar_credit.audit"


def test_ar_credit_runtime_handles_receivables_credit_rules_parameters_and_ui() -> None:
    state = _configured_state()
    extension = ar_credit_register_schema_extension(
        state,
        "ar_invoice",
        {"contract_obligations": "jsonb", "jurisdiction_tax": "jsonb"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["ar_invoice"]["contract_obligations"] == "jsonb"

    processed = ar_credit_receive_event(
        state,
        {
            "event_id": "evt_identity_ops",
            "event_type": "CustomerIdentityVerified",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "customer_ops",
                "status": "verified",
                "policy_id": "policy_ops",
            },
        },
    )
    state = processed["state"]
    assert processed["handler"]["status"] == "processed"
    assert state["customer_identity_projections"]["customer_ops"]["status"] == "verified"

    duplicate = ar_credit_receive_event(
        state,
        {
            "event_id": "evt_identity_ops",
            "event_type": "CustomerIdentityVerified",
            "payload": {
                "tenant": "tenant_ops",
                "customer_id": "customer_ops",
                "status": "verified",
                "policy_id": "policy_ops",
            },
        },
    )
    assert duplicate["duplicate"] is True

    customer = ar_credit_onboard_customer(
        state,
        {
            "customer_id": "customer_ops",
            "tenant": "tenant_ops",
            "name": "Operations Buyer",
            "parent": "holding_ops",
            "beneficial_owners": ("owner_ops",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "payment_latency": 0.04, "industry_stress": 0.03},
            "identity": {"did": "did:appgen:customer-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = customer["state"]
    invoice = ar_credit_issue_invoice(
        state,
        {
            "invoice_id": "ar_inv_ops",
            "tenant": "tenant_ops",
            "customer_id": "customer_ops",
            "currency": "USD",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "tax": {"jurisdiction": "US-NY", "amount": 40, "rate": 0.08},
            "performance_obligations": ({"obligation": "deliver_service", "satisfied": True, "allocation": 500},),
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "revenue"},),
        },
    )
    state = invoice["state"]
    assert invoice["invoice"]["total"] == 540

    state = ar_credit_record_delivery_confirmation(
        state,
        {"delivery_id": "deliv_ops", "tenant": "tenant_ops", "invoice_id": "ar_inv_ops", "lines": ({"sku": "service", "quantity": 2},)},
    )["state"]

    cash = ar_credit_apply_cash(
        state,
        {
            "receipt_id": "rcpt_ops",
            "tenant": "tenant_ops",
            "amount": 540,
            "currency": "USD",
            "remittance": ar_credit_parse_remittance("PAY ar_inv_ops amount 540 bank_ref BAI-002"),
        },
    )
    state = cash["state"]
    assert cash["decision"] == "auto_clear"
    assert state["invoices"]["ar_inv_ops"]["status"] == "cleared"
    assert state["outbox"][-1]["idempotency_key"] == "ar_credit:PaymentReceived:ar_evt_000004"

    credit = ar_credit_extend_credit(state, "customer_ops", liquidity_forecast=(2500, 2600, 2550), macro_risk=0.06)
    collection = ar_credit_optimize_collection_strategy(state, "customer_ops", dso_target=25)
    forecast = ar_credit_forecast_revenue_to_cash(state, "tenant_ops")
    dispute = ar_credit_resolve_dispute(
        state,
        {"dispute_id": "disp_ops", "invoice_id": "ar_inv_ops", "reason": "service", "evidence_score": 0.82, "amount": 25},
    )
    risk = ar_credit_score_customer_default(state, "customer_ops")
    route = ar_credit_route_collection(
        state,
        "customer_ops",
        channels=(
            {"channel": "portal", "cost": 1, "response_rate": 0.9, "available": False},
            {"channel": "api", "cost": 2, "response_rate": 0.86, "available": True},
            {"channel": "email", "cost": 0.5, "response_rate": 0.4, "available": True},
        ),
    )
    proof = ar_credit_verify_revenue_proof(invoice["invoice"])
    e_invoice = ar_credit_submit_e_invoice(state, "ar_inv_ops", jurisdiction="US-NY")
    sanctions = ar_credit_screen_customer_network(state, "customer_ops", sanction_entities=("blocked_owner",))
    controls = ar_credit_run_control_tests(state)

    assert credit["recommended_limit"] > 0
    assert collection["expected_dso_delta"] > 0
    assert forecast["forecast"][0]["amount"] == 540
    assert dispute["decision"] == "credit_memo_suggested"
    assert 0 < risk["default_probability"] < 1
    assert route["channel"] == "api"
    assert route["failover_used"] is True
    assert proof["ok"] is True
    assert e_invoice["ok"] is True
    assert sanctions["decision"] == "clear"
    assert controls["appgen_x_contract_enforced"] is True

    workbench = ar_credit_build_workbench_view(state, tenant="tenant_ops", as_of="2026-06-24")
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2
    assert workbench["inbox_count"] == 1
    assert workbench["dead_letter_count"] == 0
    assert workbench["binding_evidence"]["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["shared_table_access"] is False

    ui_contract = ar_credit_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == AR_CREDIT_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == AR_CREDIT_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_selectable_event_contract"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False

    rendered = ar_credit_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=tuple(sorted(ar_credit_permissions_contract()["permissions"])),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 4
    assert rendered["inbox_count"] == 1
    assert rendered["dead_letter_count"] == 0
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert rendered["binding_evidence"]["shared_table_access"] is False


def test_ar_credit_runtime_handles_standard_receivable_follow_up_workflows() -> None:
    state = _configured_state()
    state = ar_credit_onboard_customer(
        state,
        {
            "customer_id": "customer_follow_up",
            "tenant": "tenant_ops",
            "name": "Follow Up Buyer",
            "parent": "holding_ops",
            "beneficial_owners": ("owner_ops",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "payment_latency": 0.04, "industry_stress": 0.03},
            "identity": {"did": "did:appgen:customer-follow-up", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = ar_credit_issue_invoice(
        state,
        {
            "invoice_id": "ar_inv_follow_up",
            "tenant": "tenant_ops",
            "customer_id": "customer_follow_up",
            "currency": "USD",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "tax": {"jurisdiction": "US-NY", "amount": 40, "rate": 0.08},
            "performance_obligations": ({"obligation": "deliver_service", "satisfied": True, "allocation": 500},),
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "revenue"},),
        },
    )["state"]
    state = ar_credit_record_delivery_confirmation(
        state,
        {"delivery_id": "deliv_follow_up", "tenant": "tenant_ops", "invoice_id": "ar_inv_follow_up", "lines": ({"sku": "service", "quantity": 2},)},
    )["state"]

    partial = ar_credit_apply_cash(
        state,
        {
            "receipt_id": "rcpt_partial",
            "tenant": "tenant_ops",
            "amount": 200,
            "currency": "USD",
            "remittance": ar_credit_parse_remittance("PAY ar_inv_follow_up amount 200 bank_ref BAI-003"),
        },
    )
    state = partial["state"]
    assert state["invoices"]["ar_inv_follow_up"]["open_amount"] == 340
    assert state["invoices"]["ar_inv_follow_up"]["status"] == "partial"

    state = ar_credit_record_unapplied_cash(
        state,
        {"receipt_id": "rcpt_unapplied", "tenant": "tenant_ops", "amount": 75, "currency": "USD", "reason": "missing_remittance"},
    )["state"]
    credit_memo = ar_credit_create_credit_memo(
        state,
        {"credit_memo_id": "cm_follow_up", "invoice_id": "ar_inv_follow_up", "customer_id": "customer_follow_up", "amount": 40, "reason": "service_adjustment"},
    )
    state = credit_memo["state"]
    assert credit_memo["invoice"]["open_amount"] == 300

    aging = ar_credit_calculate_aging(state, tenant="tenant_ops", as_of="2026-07-30")
    assert aging["buckets"]["31_60"] == 300
    dunning = ar_credit_create_dunning_plan(state, tenant="tenant_ops", as_of="2026-07-30")
    assert dunning["notices"][0]["level"] == "standard"

    scheduled = ar_credit_schedule_collection_action(
        state,
        {
            "tenant": "tenant_ops",
            "customer_id": "customer_follow_up",
            "invoice_id": "ar_inv_follow_up",
            "channel": "portal",
            "due_date": "2026-07-31",
        },
    )
    state = scheduled["state"]
    assert scheduled["action"]["idempotency_key"] == "ar_credit:CollectionAction:ar_inv_follow_up:portal"

    statement = ar_credit_generate_customer_statement(state, customer_id="customer_follow_up", as_of="2026-07-30")
    state = statement["state"]
    assert statement["statement"]["open_balance"] == 300

    revenue = ar_credit_recognize_revenue_schedule(state, "ar_inv_follow_up")
    state = revenue["state"]
    assert revenue["schedule"]["recognized_amount"] == 500

    write_off = ar_credit_write_off_receivable(
        state,
        {"write_off_id": "wo_follow_up", "invoice_id": "ar_inv_follow_up", "amount": 300, "approved_by": "controller", "reason": "immaterial_balance"},
    )
    state = write_off["state"]
    assert write_off["invoice"]["status"] == "written_off"

    refund = ar_credit_issue_refund(
        state,
        {"refund_id": "refund_follow_up", "tenant": "tenant_ops", "customer_id": "customer_follow_up", "amount": 25, "currency": "USD", "reason": "overpayment"},
    )
    state = refund["state"]
    assert refund["refund"]["status"] == "scheduled"

    workbench = ar_credit_build_workbench_view(state, tenant="tenant_ops", as_of="2026-07-30")
    assert workbench["open_balance"] == 0
    assert workbench["unapplied_cash_total"] == 75
    assert workbench["collection_action_count"] == 1


def test_ar_credit_runtime_enforces_boundaries_and_idempotent_event_failures() -> None:
    state = ar_credit_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        ar_credit_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        ar_credit_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.other.events",
                "retry_limit": 2,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="uses the AppGen-X event contract"):
        ar_credit_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported AR Credit parameter"):
        ar_credit_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        ar_credit_register_schema_extension(state, "customer_master", {"shadow_copy": "jsonb"})

    failed_once = ar_credit_receive_event(
        state,
        {
            "event_id": "evt_fail_ops",
            "event_type": "UnknownArEvent",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed_once["ok"] is False
    assert failed_once["handler"]["status"] == "retrying"
    assert len(failed_once["state"]["retry_evidence"]) == 1

    failed_twice = ar_credit_receive_event(
        failed_once["state"],
        {
            "event_id": "evt_fail_ops",
            "event_type": "UnknownArEvent",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed_twice["ok"] is False
    assert failed_twice["handler"]["status"] == "dead_letter"
    assert len(failed_twice["state"]["dead_letter"]) == 1
    assert failed_twice["state"]["dead_letter"][0]["reason"] == "unsupported_or_failed_ar_credit_event"

    boundary = ar_credit_verify_owned_table_boundary(
        (
            "ar_invoice",
            "CustomerIdentityVerified",
            "customer_identity_projection",
            "ar_credit_appgen_inbox_event",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == AR_CREDIT_OWNED_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    violated = ar_credit_verify_owned_table_boundary(("gl_core_journal_entry", "customer_master"))
    assert violated["ok"] is False
    assert violated["violations"] == ("gl_core_journal_entry", "customer_master")

    api = ar_credit_build_api_contract()
    ui_contract = ar_credit_ui_contract()
    assert api["shared_table_access"] is False
    assert ui_contract["binding_evidence"]["shared_table_access"] is False


def _configured_state() -> dict:
    state = ar_credit_empty_state()
    state = ar_credit_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_collection_channels": ("portal", "api", "email"),
            "workbench_limit": 50,
        },
    )["state"]
    state = ar_credit_set_parameter(state, "auto_cash_threshold", 0.95)["state"]
    state = ar_credit_set_parameter(state, "credit_limit_buffer", 0.2)["state"]
    state = ar_credit_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "cash_application",
            "auto_cash_threshold": 0.95,
            "requires_delivery_confirmation": True,
            "status": "active",
        },
    )["state"]
    return state
