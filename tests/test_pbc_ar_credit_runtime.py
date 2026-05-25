from pyAppGen.pbc import AR_CREDIT_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import ar_credit_apply_cash
from pyAppGen.pbc import ar_credit_empty_state
from pyAppGen.pbc import ar_credit_issue_invoice
from pyAppGen.pbc import ar_credit_onboard_customer
from pyAppGen.pbc import ar_credit_parse_remittance
from pyAppGen.pbc import ar_credit_record_delivery_confirmation
from pyAppGen.pbc import ar_credit_runtime_capabilities
from pyAppGen.pbc import ar_credit_runtime_smoke
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit


def test_ar_credit_runtime_executes_all_documented_advanced_capabilities() -> None:
    runtime = ar_credit_runtime_capabilities()
    smoke = ar_credit_runtime_smoke()

    assert runtime["format"] == "appgen.ar-credit-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/ar_credit"
    assert smoke["ok"] is True
    assert set(AR_CREDIT_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("ar_credit")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(AR_CREDIT_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("ar_credit",))["ok"] is True
    assert pbc_release_audit()["ok"] is True


def test_ar_credit_runtime_handles_core_receivables_cash_application() -> None:
    state = ar_credit_empty_state()
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
