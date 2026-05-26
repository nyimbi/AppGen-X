import pytest

from pyAppGen.pbcs.tax_localization import TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.tax_localization import TAX_LOCALIZATION_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.tax_localization import TAX_LOCALIZATION_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.tax_localization import TAX_LOCALIZATION_OWNED_TABLES
from pyAppGen.pbcs.tax_localization import TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.tax_localization import tax_localization_build_api_contract
from pyAppGen.pbcs.tax_localization import tax_localization_permissions_contract
from pyAppGen.pbcs.tax_localization import tax_localization_receive_event
from pyAppGen.pbcs.tax_localization import tax_localization_register_schema_extension
from pyAppGen.pbcs.tax_localization import tax_localization_verify_owned_table_boundary
from pyAppGen.pbc import TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import tax_localization_build_workbench_view
from pyAppGen.pbc import tax_localization_calculate_tax_quote
from pyAppGen.pbc import tax_localization_classify_product
from pyAppGen.pbc import tax_localization_configure_runtime
from pyAppGen.pbc import tax_localization_empty_state
from pyAppGen.pbc import tax_localization_prepare_tax_filing
from pyAppGen.pbc import tax_localization_record_invoice_tax
from pyAppGen.pbc import tax_localization_register_jurisdiction
from pyAppGen.pbc import tax_localization_register_rule
from pyAppGen.pbc import tax_localization_render_workbench
from pyAppGen.pbc import tax_localization_register_tax_rule
from pyAppGen.pbc import tax_localization_runtime_capabilities
from pyAppGen.pbc import tax_localization_runtime_smoke
from pyAppGen.pbc import tax_localization_set_parameter
from pyAppGen.pbc import tax_localization_ui_contract
from pyAppGen.pbc import tax_localization_validate_exemption_certificate


def test_tax_localization_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = tax_localization_runtime_capabilities()
    smoke = tax_localization_runtime_smoke()

    assert runtime["format"] == "appgen.tax-localization-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/tax_localization"
    assert runtime["owned_tables"] == TAX_LOCALIZATION_OWNED_TABLES
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert len(runtime["standard_features"]) >= 18
    assert smoke["ok"] is True
    assert set(TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("tax_localization")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == TAX_LOCALIZATION_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "tax_localization.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TaxConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TAX_LOCALIZATION_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("tax_localization",))["ok"] is True
    assert pbc_implemented_capability_audit(("tax_localization",))["ok"] is True

    api = tax_localization_build_api_contract()
    permissions = tax_localization_permissions_contract()
    assert api["format"] == "appgen.tax-localization-api-contract.v1"
    assert api["owned_tables"] == TAX_LOCALIZATION_OWNED_TABLES
    assert api["database_backends"] == TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == TAX_LOCALIZATION_EMITTED_EVENT_TYPES
    assert api["consumes"] == TAX_LOCALIZATION_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /tax/quotes", "POST /tax/events/inbox", "GET /tax/workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["receive_event"] == "tax_localization.event"


def test_tax_localization_runtime_handles_core_tax_workflows() -> None:
    state = tax_localization_empty_state()
    state = tax_localization_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "authority_channels": ("authority_api", "secure_outbox"),
            "workbench_limit": 50,
        },
    )["state"]
    state = tax_localization_set_parameter(state, "tax_quote_precision", 2)["state"]
    state = tax_localization_set_parameter(state, "filing_reconciliation_tolerance", 0.01)["state"]
    state = tax_localization_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "filing",
            "approval_required": True,
            "reconciliation_tolerance": 0.01,
            "status": "active",
        },
    )["state"]
    extension = tax_localization_register_schema_extension(state, "tax_rule", {"clearance_metadata": "jsonb", "local_authority_payload": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["tax_rule"]["clearance_metadata"] == "jsonb"
    consumed = tax_localization_receive_event(
        state,
        {
            "event_id": "evt_product_ops",
            "event_type": "ProductClassified",
            "payload": {"tenant": "tenant_ops", "product_id": "sku_ops", "product_class": "standard_goods", "confidence": 0.93},
        },
    )
    state = consumed["state"]
    assert consumed["handler"]["status"] == "processed"
    assert state["product_taxability_projections"]["sku_ops"]["product_class"] == "standard_goods"
    duplicate = tax_localization_receive_event(
        state,
        {
            "event_id": "evt_product_ops",
            "event_type": "ProductClassified",
            "payload": {"tenant": "tenant_ops", "product_id": "sku_ops", "product_class": "standard_goods", "confidence": 0.93},
        },
    )
    assert duplicate["duplicate"] is True
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
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == TAX_LOCALIZATION_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = tax_localization_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == TAX_LOCALIZATION_OWNED_TABLES
    assert "tax_quote_precision" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = tax_localization_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "tax_localization.jurisdiction",
            "tax_localization.rule_admin",
            "tax_localization.calculate",
            "tax_localization.invoice",
            "tax_localization.file",
            "tax_localization.exemption",
            "tax_localization.reconcile",
            "tax_localization.event",
            "tax_localization.audit",
            "tax_localization.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 5
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == TAX_LOCALIZATION_OWNED_TABLES

    boundary = tax_localization_verify_owned_table_boundary(
        ("tax_calculation", "ProductClassified", "product_taxability_projection", "POST /audit/tax-events", "tax_localization_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation_boundary = tax_localization_verify_owned_table_boundary(("ap_invoice",))
    assert violation_boundary["ok"] is False
    assert violation_boundary["violations"] == ("ap_invoice",)


def test_tax_localization_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = tax_localization_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        tax_localization_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event topic"):
        tax_localization_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.tax.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        tax_localization_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "stream_engine_picker": "user_visible",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Tax Localization parameter"):
        tax_localization_set_parameter(state, "stream_engine", "hidden_picker")

    configured = tax_localization_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
        },
    )["state"]
    with pytest.raises(ValueError, match="owned tables"):
        tax_localization_register_schema_extension(configured, "invoice_header", {"foreign_payload": "jsonb"})

    invalid = tax_localization_register_schema_extension(configured, "tax_rule", {"InvalidField": "jsonb"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    retry = tax_localization_receive_event(
        configured,
        {"event_id": "evt_unknown", "event_type": "UnknownEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = tax_localization_receive_event(
        retry["state"],
        {"event_id": "evt_unknown", "event_type": "UnknownEvent", "payload": {"tenant": "tenant_ops"}},
    )
    assert dead["handler"]["status"] == "dead_letter"
    assert dead["state"]["dead_letter"][-1]["reason"] == "unsupported_or_failed_tax_event"
