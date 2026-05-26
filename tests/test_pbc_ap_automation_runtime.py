import pytest

from pyAppGen.pbcs.ap_automation import AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.ap_automation import AP_AUTOMATION_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.ap_automation import AP_AUTOMATION_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.ap_automation import AP_AUTOMATION_OWNED_TABLES
from pyAppGen.pbcs.ap_automation import AP_AUTOMATION_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.ap_automation import AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.ap_automation import ap_automation_align_contract_terms
from pyAppGen.pbcs.ap_automation import ap_automation_analyze_discount_counterfactual
from pyAppGen.pbcs.ap_automation import ap_automation_build_api_contract
from pyAppGen.pbcs.ap_automation import ap_automation_build_workbench_view
from pyAppGen.pbcs.ap_automation import ap_automation_capture_invoice
from pyAppGen.pbcs.ap_automation import ap_automation_configure_runtime
from pyAppGen.pbcs.ap_automation import ap_automation_empty_state
from pyAppGen.pbcs.ap_automation import ap_automation_execute_payment
from pyAppGen.pbcs.ap_automation import ap_automation_forecast_cash_flow
from pyAppGen.pbcs.ap_automation import ap_automation_issue_purchase_order
from pyAppGen.pbcs.ap_automation import ap_automation_match_invoice
from pyAppGen.pbcs.ap_automation import ap_automation_onboard_vendor
from pyAppGen.pbcs.ap_automation import ap_automation_permissions_contract
from pyAppGen.pbcs.ap_automation import ap_automation_receive_event
from pyAppGen.pbcs.ap_automation import ap_automation_record_goods_receipt
from pyAppGen.pbcs.ap_automation import ap_automation_register_rule
from pyAppGen.pbcs.ap_automation import ap_automation_register_schema_extension
from pyAppGen.pbcs.ap_automation import ap_automation_render_workbench
from pyAppGen.pbcs.ap_automation import ap_automation_runtime_capabilities
from pyAppGen.pbcs.ap_automation import ap_automation_runtime_smoke
from pyAppGen.pbcs.ap_automation import ap_automation_schedule_payments
from pyAppGen.pbcs.ap_automation import ap_automation_set_parameter
from pyAppGen.pbcs.ap_automation import ap_automation_ui_contract
from pyAppGen.pbcs.ap_automation import ap_automation_verify_owned_table_boundary
from pyAppGen.pbcs.ap_automation import implementation_contract


def test_ap_automation_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = ap_automation_runtime_capabilities()
    smoke = ap_automation_runtime_smoke()

    assert runtime["format"] == "appgen.ap-automation-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/ap_automation"
    assert runtime["owned_tables"] == AP_AUTOMATION_OWNED_TABLES
    assert runtime["allowed_database_backends"] == AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "permissions" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = implementation_contract()
    assert contract["pbc"] == "ap_automation"
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert contract["api_contract"]["ok"] is True
    assert contract["permissions_contract"]["ok"] is True
    assert contract["owned_tables"] == AP_AUTOMATION_OWNED_TABLES
    assert contract["allowed_database_backends"] == AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
    assert contract["required_event_topic"] == AP_AUTOMATION_REQUIRED_EVENT_TOPIC
    assert contract["consumes"] == AP_AUTOMATION_CONSUMED_EVENT_TYPES
    assert contract["emits"] == AP_AUTOMATION_EMITTED_EVENT_TYPES
    assert "ApConfigurationPanel" in contract["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(AP_AUTOMATION_RUNTIME_CAPABILITY_KEYS)


def test_ap_automation_runtime_applies_accounts_payable_workflows_and_contracts() -> None:
    state = _configured_state()
    extension = ap_automation_register_schema_extension(
        state,
        "ap_automation_invoice",
        {"jurisdiction_tax": "jsonb", "contract_clause": "text"},
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1

    vendor = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": "vendor_ops",
            "tenant": "tenant_ops",
            "name": "Operations Supplies",
            "beneficial_owners": ("owner_ops",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.01, "financial_stress": 0.02},
            "identity": {"did": "did:appgen:vendor-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = vendor["state"]
    state = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_vendor_ops",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_ops", "vendor_id": "vendor_ops", "approved_by": "controller_ops"},
        },
    )["state"]
    state = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_cash_ops",
            "event_type": "CashForecastUpdated",
            "payload": {"tenant": "tenant_ops", "available_cash": 1800, "currency": "USD"},
        },
    )["state"]
    po = ap_automation_issue_purchase_order(
        state,
        {
            "po_id": "po_ops",
            "tenant": "tenant_ops",
            "vendor_id": "vendor_ops",
            "currency": "USD",
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "expense"},),
        },
    )
    state = po["state"]
    receipt = ap_automation_record_goods_receipt(
        state,
        {
            "receipt_id": "gr_ops",
            "tenant": "tenant_ops",
            "po_id": "po_ops",
            "lines": ({"sku": "service", "quantity": 2},),
        },
    )
    state = receipt["state"]
    contract_terms = ap_automation_align_contract_terms(
        "net 30 with 2% discount if paid within 10 days; tax jurisdiction US-NY",
        {"vendor_id": "vendor_ops"},
    )
    invoice = ap_automation_capture_invoice(
        state,
        {
            "invoice_id": "inv_ops",
            "tenant": "tenant_ops",
            "vendor_id": "vendor_ops",
            "po_id": "po_ops",
            "receipt_id": "gr_ops",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "currency": "USD",
            "tax": {"jurisdiction": "US-NY", "amount": 40, "rate": 0.08},
            "contract_terms": contract_terms["terms"],
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "expense"},),
        },
    )
    state = invoice["state"]
    assert invoice["ok"] is True
    assert invoice["invoice"]["subtotal"] == 500
    assert invoice["invoice"]["total"] == 540
    assert invoice["state"]["outbox"][-1]["idempotency_key"].startswith(
        "ap_automation:InvoiceCaptured:"
    )

    match = ap_automation_match_invoice(state, "inv_ops")
    assert match["decision"] == "auto_approve"
    assert match["confidence"] == 0.99

    schedule = ap_automation_schedule_payments(
        state,
        tenant="tenant_ops",
        liquidity_forecast=(1800, 1600, 1400),
        risk_limit=0.7,
    )
    state = schedule["state"]
    assert schedule["pool"]["available_cash"] == 1800.0
    assert schedule["payments"][0]["scheduled_date"] == "discount_window"

    execution = ap_automation_execute_payment(
        state,
        "pay_inv_ops",
        rails=(
            {"rail": "instant_bank_api", "cost": 4, "latency": 2, "fx_rate": 1.0, "available": False},
            {"rail": "ach", "cost": 1, "latency": 24, "fx_rate": 1.0, "available": True},
        ),
    )
    state = execution["state"]
    assert execution["payment"]["rail"] == "ach"
    assert execution["payment"]["status"] == "executed"
    assert execution["failover_used"] is True

    workbench = ap_automation_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["vendor_count"] == 1
    assert workbench["invoice_count"] == 1
    assert workbench["open_invoice_total"] == 0
    assert workbench["executed_payment_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 6
    assert workbench["inbox_count"] == 2
    assert workbench["dead_letter_count"] == 0
    assert workbench["binding_evidence"]["owned_tables"] == AP_AUTOMATION_OWNED_TABLES

    forecast = ap_automation_forecast_cash_flow(state, "tenant_ops")
    discount = ap_automation_analyze_discount_counterfactual(
        540, discount_rate=0.02, annual_capital_cost=0.12, days_early=20
    )
    assert forecast["ok"] is True
    assert forecast["forecast"][0]["amount"] == -540
    assert discount["net_benefit"] > 0

    ui_contract = ap_automation_ui_contract()
    assert (
        ui_contract["configuration_editor"]["allowed_database_backends"]
        == AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
    )
    assert ui_contract["configuration_editor"]["required_event_topic"] == AP_AUTOMATION_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["event_surfaces"]["contract"] == "AppGen-X"
    rendered = ap_automation_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "ap_automation.vendor",
            "ap_automation.invoice",
            "ap_automation.match",
            "ap_automation.exception",
            "ap_automation.payment",
            "ap_automation.tax",
            "ap_automation.event.consume",
            "ap_automation.configure",
            "ap_automation.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["event_inbox_count"] == 2
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == AP_AUTOMATION_OWNED_TABLES
    assert not rendered["locked_actions"]

    api_contract = ap_automation_build_api_contract()
    assert api_contract["database_backends"] == AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
    assert api_contract["event_contract"] == "AppGen-X"
    assert api_contract["required_event_topic"] == AP_AUTOMATION_REQUIRED_EVENT_TOPIC
    assert api_contract["shared_table_access"] is False
    assert api_contract["stream_engine_picker_visible"] is False
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "onboard_vendor",
        "issue_purchase_order",
        "record_goods_receipt",
        "capture_invoice",
        "match_invoice",
        "schedule_payments",
        "execute_payment",
        "receive_event",
    }
    permissions = ap_automation_permissions_contract()
    assert permissions["action_permissions"]["receive_event"] == "ap_automation.event.consume"
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "ap_automation.audit"


def test_ap_automation_proves_boundaries_and_idempotent_event_handling() -> None:
    state = ap_automation_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        ap_automation_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "allowed_payment_rails": ("ach",),
                "workbench_limit": 50,
            },
        )
    with pytest.raises(ValueError, match="AppGen-X accounts payable event contract"):
        ap_automation_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.ap.legacy",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "allowed_payment_rails": ("ach",),
                "workbench_limit": 50,
            },
        )
    with pytest.raises(ValueError, match="stream-engine pickers"):
        ap_automation_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "allowed_payment_rails": ("ach",),
                "workbench_limit": 50,
                "stream_engine": "legacy_stream",
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported AP Automation parameter"):
        ap_automation_set_parameter(state, "stream_engine", 1)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        ap_automation_register_schema_extension(state, "gl_journal_entry", {"posting_id": "text"})

    vendor = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": "vendor_boundary",
            "tenant": "tenant_ops",
            "name": "Boundary Vendor",
            "beneficial_owners": ("owner_boundary",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0.01, "financial_stress": 0.02},
            "identity": {"did": "did:appgen:vendor-boundary", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = vendor["state"]

    received = ap_automation_receive_event(
        state,
        {
            "event_id": "evt_vendor_boundary",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_ops", "vendor_id": "vendor_boundary", "approved_by": "controller_ops"},
        },
    )
    assert received["ok"] is True
    assert received["handler"]["status"] == "handled"
    assert len(received["state"]["inbox"]) == 1

    duplicate = ap_automation_receive_event(
        received["state"],
        {
            "event_id": "evt_vendor_boundary",
            "event_type": "VendorApproved",
            "payload": {"tenant": "tenant_ops", "vendor_id": "vendor_boundary", "approved_by": "controller_ops"},
        },
    )
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert duplicate["handler"]["status"] == "duplicate"
    assert len(duplicate["state"]["inbox"]) == 1

    retrying = ap_automation_receive_event(
        received["state"],
        {
            "event_id": "evt_retry_ops",
            "event_type": "UnknownInboundEvent",
            "payload": {"tenant": "tenant_ops"},
            "attempts": 1,
        },
    )
    assert retrying["ok"] is False
    assert retrying["retrying"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert len(retrying["state"]["dead_letter"]) == 0

    dead_letter = ap_automation_receive_event(
        received["state"],
        {
            "event_id": "evt_dead_ops",
            "event_type": "UnknownInboundEvent",
            "payload": {"tenant": "tenant_ops"},
            "attempts": 3,
        },
    )
    assert dead_letter["ok"] is False
    assert dead_letter["dead_lettered"] is True
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1

    boundary = ap_automation_verify_owned_table_boundary(
        (
            "ap_automation_vendor",
            "ap_automation_invoice",
            "ap_automation_payment",
            "ap_automation_inbox",
            "VendorApproved",
            "cash_forecast_projection",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == AP_AUTOMATION_OWNED_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    assert "cash_forecast_projection" in boundary["declared_dependencies"]["api_projections"]
    violated = ap_automation_verify_owned_table_boundary(("gl_journal_entry",))
    assert violated["ok"] is False
    assert violated["violations"] == ("gl_journal_entry",)


def _configured_state() -> dict:
    state = ap_automation_empty_state()
    state = ap_automation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("auto_match_threshold", 0.95),
        ("payment_approval_limit", 5000),
        ("discount_capture_floor", 0.01),
        ("vendor_risk_threshold", 0.7),
        ("liquidity_buffer", 250),
        ("workbench_limit", 50),
    ):
        state = ap_automation_set_parameter(state, name, value)["state"]
    state = ap_automation_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "invoice_match",
            "requires_three_way_match": True,
            "auto_match_threshold": 0.95,
            "status": "active",
        },
    )["state"]
    return state
