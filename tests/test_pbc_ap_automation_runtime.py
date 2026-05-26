from pyAppGen.pbc import AP_AUTOMATION_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import ap_automation_build_workbench_view
from pyAppGen.pbc import ap_automation_capture_invoice
from pyAppGen.pbc import ap_automation_configure_runtime
from pyAppGen.pbc import ap_automation_empty_state
from pyAppGen.pbc import ap_automation_issue_purchase_order
from pyAppGen.pbc import ap_automation_match_invoice
from pyAppGen.pbc import ap_automation_onboard_vendor
from pyAppGen.pbc import ap_automation_record_goods_receipt
from pyAppGen.pbc import ap_automation_register_rule
from pyAppGen.pbc import ap_automation_render_workbench
from pyAppGen.pbc import ap_automation_runtime_capabilities
from pyAppGen.pbc import ap_automation_runtime_smoke
from pyAppGen.pbc import ap_automation_set_parameter
from pyAppGen.pbc import ap_automation_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit


def test_ap_automation_runtime_executes_all_documented_advanced_capabilities() -> None:
    runtime = ap_automation_runtime_capabilities()
    smoke = ap_automation_runtime_smoke()

    assert runtime["format"] == "appgen.ap-automation-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/ap_automation"
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(AP_AUTOMATION_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("ap_automation")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ApConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(AP_AUTOMATION_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("ap_automation",))["ok"] is True
    assert pbc_implemented_capability_audit(("ap_automation",))["ok"] is True
    assert pbc_release_audit()["ok"] is True


def test_ap_automation_runtime_handles_core_accounts_payable_lifecycle() -> None:
    state = ap_automation_empty_state()
    state = ap_automation_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.ap.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire"),
            "workbench_limit": 50,
        },
    )["state"]
    state = ap_automation_set_parameter(state, "auto_match_threshold", 0.95)["state"]
    state = ap_automation_set_parameter(state, "payment_approval_limit", 5000)["state"]
    state = ap_automation_register_rule(
        state,
        {
            "rule_id": "rule_beta",
            "tenant": "tenant_beta",
            "scope": "invoice_match",
            "requires_three_way_match": True,
            "auto_match_threshold": 0.95,
            "status": "active",
        },
    )["state"]
    vendor = ap_automation_onboard_vendor(
        state,
        {
            "vendor_id": "vendor_beta",
            "tenant": "tenant_beta",
            "name": "Beta Services",
            "beneficial_owners": ("owner_a",),
            "terms": {"net_days": 30},
            "risk_signals": {"sanction_hits": 0, "late_delivery_rate": 0, "financial_stress": 0},
            "identity": {"did": "did:appgen:vendor-beta", "issuer": "trusted_registry", "status": "active"},
        },
    )
    assert vendor["ok"] is True
    state = vendor["state"]

    po = ap_automation_issue_purchase_order(
        state,
        {
            "po_id": "po_beta",
            "tenant": "tenant_beta",
            "vendor_id": "vendor_beta",
            "currency": "USD",
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "expense"},),
        },
    )
    state = po["state"]
    receipt = ap_automation_record_goods_receipt(
        state,
        {"receipt_id": "gr_beta", "tenant": "tenant_beta", "po_id": "po_beta", "lines": ({"sku": "service", "quantity": 2},)},
    )
    state = receipt["state"]
    invoice = ap_automation_capture_invoice(
        state,
        {
            "invoice_id": "inv_beta",
            "tenant": "tenant_beta",
            "vendor_id": "vendor_beta",
            "po_id": "po_beta",
            "receipt_id": "gr_beta",
            "invoice_date": "2026-05-25",
            "due_date": "2026-06-24",
            "currency": "USD",
            "tax": {"jurisdiction": "US-NY", "amount": 40, "rate": 0.08},
            "contract_terms": {"net_days": 30},
            "lines": ({"sku": "service", "quantity": 2, "unit_price": 250, "account": "expense"},),
        },
    )
    assert invoice["ok"] is True
    assert invoice["invoice"]["subtotal"] == 500
    assert invoice["invoice"]["total"] == 540
    assert invoice["state"]["outbox"][-1]["idempotency_key"] == "ap_automation:InvoiceCaptured:ap_evt_000004"

    match = ap_automation_match_invoice(invoice["state"], "inv_beta")
    assert match["decision"] == "auto_approve"
    assert match["confidence"] == 0.99

    workbench = ap_automation_build_workbench_view(invoice["state"], tenant="tenant_beta")
    assert workbench["vendor_count"] == 1
    assert workbench["invoice_count"] == 1
    assert workbench["open_invoice_total"] == 540
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2

    ui_contract = ap_automation_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "auto_match_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = ap_automation_render_workbench(
        invoice["state"],
        tenant="tenant_beta",
        principal_permissions=(
            "ap_automation.vendor",
            "ap_automation.invoice",
            "ap_automation.match",
            "ap_automation.exception",
            "ap_automation.payment",
            "ap_automation.tax",
            "ap_automation.configure",
            "ap_automation.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 4
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
