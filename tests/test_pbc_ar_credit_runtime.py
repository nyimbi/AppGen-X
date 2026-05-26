import pytest

from pyAppGen.pbc import AR_CREDIT_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import ar_credit_apply_cash
from pyAppGen.pbc import ar_credit_build_workbench_view
from pyAppGen.pbc import ar_credit_calculate_aging
from pyAppGen.pbc import ar_credit_configure_runtime
from pyAppGen.pbc import ar_credit_create_credit_memo
from pyAppGen.pbc import ar_credit_create_dunning_plan
from pyAppGen.pbc import ar_credit_empty_state
from pyAppGen.pbc import ar_credit_generate_customer_statement
from pyAppGen.pbc import ar_credit_issue_invoice
from pyAppGen.pbc import ar_credit_issue_refund
from pyAppGen.pbc import ar_credit_onboard_customer
from pyAppGen.pbc import ar_credit_parse_remittance
from pyAppGen.pbc import ar_credit_record_delivery_confirmation
from pyAppGen.pbc import ar_credit_record_unapplied_cash
from pyAppGen.pbc import ar_credit_recognize_revenue_schedule
from pyAppGen.pbc import ar_credit_register_rule
from pyAppGen.pbc import ar_credit_render_workbench
from pyAppGen.pbc import ar_credit_runtime_capabilities
from pyAppGen.pbc import ar_credit_runtime_smoke
from pyAppGen.pbc import ar_credit_schedule_collection_action
from pyAppGen.pbc import ar_credit_set_parameter
from pyAppGen.pbc import ar_credit_ui_contract
from pyAppGen.pbc import ar_credit_write_off_receivable
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit


def test_ar_credit_runtime_executes_all_documented_advanced_capabilities() -> None:
    runtime = ar_credit_runtime_capabilities()
    smoke = ar_credit_runtime_smoke()

    assert runtime["format"] == "appgen.ar-credit-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/ar_credit"
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(AR_CREDIT_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("ar_credit")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ArConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(AR_CREDIT_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("ar_credit",))["ok"] is True
    assert pbc_implemented_capability_audit(("ar_credit",))["ok"] is True
    assert pbc_release_audit()["ok"] is True


def test_ar_credit_runtime_handles_core_receivables_cash_application() -> None:
    state = ar_credit_empty_state()
    state = ar_credit_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.ar.events",
            "retry_limit": 3,
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
            "rule_id": "rule_beta",
            "tenant": "tenant_beta",
            "scope": "cash_application",
            "auto_cash_threshold": 0.95,
            "requires_delivery_confirmation": True,
            "status": "active",
        },
    )["state"]
    customer = ar_credit_onboard_customer(
        state,
        {
            "customer_id": "customer_beta",
            "tenant": "tenant_beta",
            "name": "Beta Buyer",
            "parent": "holding_beta",
            "beneficial_owners": ("owner_a",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "payment_latency": 0, "industry_stress": 0},
            "identity": {"did": "did:appgen:customer-beta", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = customer["state"]
    invoice = ar_credit_issue_invoice(
        state,
        {
            "invoice_id": "ar_inv_beta",
            "tenant": "tenant_beta",
            "customer_id": "customer_beta",
            "currency": "USD",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "tax": {"jurisdiction": "US-NY", "amount": 40, "rate": 0.08},
            "performance_obligations": ({"obligation": "deliver_service", "satisfied": True, "allocation": 500},),
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "revenue"},),
        },
    )
    assert invoice["invoice"]["subtotal"] == 500
    assert invoice["invoice"]["total"] == 540
    state = invoice["state"]
    delivery = ar_credit_record_delivery_confirmation(
        state,
        {"delivery_id": "deliv_beta", "tenant": "tenant_beta", "invoice_id": "ar_inv_beta", "lines": ({"sku": "service", "quantity": 2},)},
    )
    state = delivery["state"]

    remittance = ar_credit_parse_remittance("PAY ar_inv_beta amount 540 bank_ref BAI-002")
    assert remittance["ok"] is True
    cash = ar_credit_apply_cash(
        state,
        {"receipt_id": "rcpt_beta", "tenant": "tenant_beta", "amount": 540, "currency": "USD", "remittance": remittance},
    )

    assert cash["ok"] is True
    assert cash["decision"] == "auto_clear"
    assert cash["confidence"] == 0.99
    assert cash["state"]["invoices"]["ar_inv_beta"]["status"] == "cleared"
    assert cash["state"]["outbox"][-1]["idempotency_key"] == "ar_credit:PaymentReceived:ar_evt_000004"

    workbench = ar_credit_build_workbench_view(cash["state"], tenant="tenant_beta", as_of="2026-06-24")
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2

    ui_contract = ar_credit_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "auto_cash_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = ar_credit_render_workbench(
        cash["state"],
        tenant="tenant_beta",
        principal_permissions=(
            "ar_credit.customer",
            "ar_credit.invoice",
            "ar_credit.delivery",
            "ar_credit.cash",
            "ar_credit.adjustment",
            "ar_credit.refund",
            "ar_credit.collection",
            "ar_credit.credit",
            "ar_credit.configure",
            "ar_credit.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 4
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_ar_credit_runtime_covers_usual_ar_operations() -> None:
    state = ar_credit_empty_state()
    state = ar_credit_onboard_customer(
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
    )["state"]
    state = ar_credit_issue_invoice(
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
    )["state"]
    state = ar_credit_record_delivery_confirmation(
        state,
        {"delivery_id": "deliv_ops", "tenant": "tenant_ops", "invoice_id": "ar_inv_ops", "lines": ({"sku": "service", "quantity": 2},)},
    )["state"]

    partial = ar_credit_apply_cash(
        state,
        {
            "receipt_id": "rcpt_partial",
            "tenant": "tenant_ops",
            "amount": 200,
            "currency": "USD",
            "remittance": ar_credit_parse_remittance("PAY ar_inv_ops amount 200 bank_ref BAI-003"),
        },
    )
    assert partial["state"]["invoices"]["ar_inv_ops"]["open_amount"] == 340
    assert partial["state"]["invoices"]["ar_inv_ops"]["status"] == "partial"
    state = partial["state"]

    state = ar_credit_record_unapplied_cash(
        state,
        {"receipt_id": "rcpt_unapplied", "tenant": "tenant_ops", "amount": 75, "currency": "USD", "reason": "missing_remittance"},
    )["state"]
    credit_memo = ar_credit_create_credit_memo(
        state,
        {"credit_memo_id": "cm_ops", "invoice_id": "ar_inv_ops", "customer_id": "customer_ops", "amount": 40, "reason": "service_adjustment"},
    )
    assert credit_memo["invoice"]["open_amount"] == 300
    state = credit_memo["state"]

    aging = ar_credit_calculate_aging(state, tenant="tenant_ops", as_of="2026-07-30")
    assert aging["buckets"]["31_60"] == 300
    dunning = ar_credit_create_dunning_plan(state, tenant="tenant_ops", as_of="2026-07-30")
    assert dunning["notices"][0]["level"] == "standard"
    state = ar_credit_schedule_collection_action(
        state,
        {
            "tenant": "tenant_ops",
            "customer_id": "customer_ops",
            "invoice_id": "ar_inv_ops",
            "channel": "portal",
            "due_date": "2026-07-31",
        },
    )["state"]

    statement = ar_credit_generate_customer_statement(state, customer_id="customer_ops", as_of="2026-07-30")
    assert statement["statement"]["open_balance"] == 300
    state = statement["state"]
    revenue = ar_credit_recognize_revenue_schedule(state, "ar_inv_ops")
    assert revenue["schedule"]["recognized_amount"] == 500
    state = revenue["state"]

    write_off = ar_credit_write_off_receivable(
        state,
        {"write_off_id": "wo_ops", "invoice_id": "ar_inv_ops", "amount": 300, "approved_by": "controller", "reason": "immaterial_balance"},
    )
    assert write_off["ok"] is True
    assert write_off["invoice"]["status"] == "written_off"
    state = write_off["state"]
    refund = ar_credit_issue_refund(
        state,
        {"refund_id": "refund_ops", "tenant": "tenant_ops", "customer_id": "customer_ops", "amount": 25, "currency": "USD", "reason": "overpayment"},
    )
    assert refund["refund"]["status"] == "scheduled"
    state = refund["state"]

    workbench = ar_credit_build_workbench_view(state, tenant="tenant_ops", as_of="2026-07-30")
    assert workbench["open_balance"] == 0
    assert workbench["unapplied_cash_total"] == 75
    assert workbench["collection_action_count"] == 1


def test_ar_credit_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = ar_credit_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        ar_credit_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.ar.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported AR Credit parameter"):
        ar_credit_set_parameter(state, "stream_engine", "hidden_picker")
