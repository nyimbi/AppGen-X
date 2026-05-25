from pyAppGen.pbc import TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import tax_localization_build_workbench_view
from pyAppGen.pbc import tax_localization_calculate_tax_quote
from pyAppGen.pbc import tax_localization_classify_product
from pyAppGen.pbc import tax_localization_empty_state
from pyAppGen.pbc import tax_localization_prepare_tax_filing
from pyAppGen.pbc import tax_localization_record_invoice_tax
from pyAppGen.pbc import tax_localization_register_jurisdiction
from pyAppGen.pbc import tax_localization_register_tax_rule
from pyAppGen.pbc import tax_localization_runtime_capabilities
from pyAppGen.pbc import tax_localization_runtime_smoke
from pyAppGen.pbc import tax_localization_validate_exemption_certificate


def test_tax_localization_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = tax_localization_runtime_capabilities()
    smoke = tax_localization_runtime_smoke()

    assert runtime["format"] == "appgen.tax-localization-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/tax_localization"
    assert len(runtime["standard_features"]) >= 18
    assert smoke["ok"] is True
    assert set(TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("tax_localization")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("tax_localization",))["ok"] is True
    assert pbc_implemented_capability_audit(("tax_localization",))["ok"] is True


def test_tax_localization_runtime_handles_core_tax_workflows() -> None:
    state = tax_localization_empty_state()
    state = tax_localization_register_jurisdiction(
        state,
        {
            "jurisdiction_id": "us_ny_new_york",
            "tenant": "tenant_ops",
            "country": "US",
            "region": "NY",
            "locality": "New York",
            "currency": "USD",
            "authority_channel": "authority_api",
            "filing_frequency": "monthly",
            "due_day": 20,
            "risk_signals": {"late_filing_rate": 0.01, "rule_volatility": 0.05, "channel_failure": 0.02},
            "identity": {"did": "did:appgen:tax-authority-ny", "issuer": "trusted_registry", "status": "active"},
        },
    )["state"]
    state = tax_localization_register_tax_rule(
        state,
        {
            "rule_id": "rule_books",
            "tenant": "tenant_ops",
            "jurisdiction_id": "us_ny_new_york",
            "tax_type": "sales_tax",
            "product_class": "standard_goods",
            "rate": 0.08875,
            "effective_from": "2026-01-01",
            "effective_to": "2026-12-31",
            "version": 1,
            "status": "active",
            "approval": {"approved_by": "tax_controller", "approved_at": "2026-05-26"},
        },
    )["state"]

    classification = tax_localization_classify_product(
        "standard goods travel bag",
        taxonomy=("standard_goods", "food", "medical_device"),
    )
    assert classification["class"] == "standard_goods"
    assert classification["confidence"] >= 0.8

    quote = tax_localization_calculate_tax_quote(
        state,
        {
            "quote_id": "tax_quote_ops",
            "tenant": "tenant_ops",
            "jurisdiction_id": "us_ny_new_york",
            "customer_id": "customer_ops",
            "order_id": "order_ops",
            "lines": (
                {"line_id": "line_ops", "product_id": "sku_ops", "product_class": classification["class"], "amount": 200, "quantity": 3},
            ),
        },
    )
    state = quote["state"]
    assert quote["calculation"]["taxable_total"] == 600
    assert quote["calculation"]["tax_total"] == 53.25
    assert state["outbox"][-1]["idempotency_key"] == "tax_localization:TaxCalculated:tax_evt_000003"

    invoice = tax_localization_record_invoice_tax(state, "invoice_ops", "tax_quote_ops")
    state = invoice["state"]
    assert invoice["record"]["tax_total"] == 53.25

    certificate = tax_localization_validate_exemption_certificate(
        {"certificate_id": "cert_ops", "status": "active", "expires": "2027-01-01", "jurisdiction_id": "us_ny_new_york"}
    )
    assert certificate["decision"] == "valid"

    filing = tax_localization_prepare_tax_filing(
        state,
        filing_id="filing_ops",
        jurisdiction_id="us_ny_new_york",
        period="2026-06",
        approved_by="tax_controller",
    )
    state = filing["state"]
    assert filing["filing"]["liability"] == 53.25
    assert state["outbox"][-1]["idempotency_key"] == "tax_localization:TaxFilingPrepared:tax_evt_000005"

    workbench = tax_localization_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["jurisdiction_count"] == 1
    assert workbench["calculation_count"] == 1
    assert workbench["filing_count"] == 1
    assert workbench["open_liability"] == 0
