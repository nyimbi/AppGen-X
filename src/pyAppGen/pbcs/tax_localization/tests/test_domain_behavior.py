"""Domain behavior tests for the tax_localization PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from ..services import TaxLocalizationService
from ..repository import TaxLocalizationRepository
from ..services import service_operation_manifest
from ..ui import tax_localization_render_workbench
from ..ui import tax_localization_ui_contract


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.TAX_LOCALIZATION_REQUIRED_EVENT_TOPIC,
    "retry_limit": 2,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "workbench_limit": 100,
}


def configured_state() -> dict:
    state = runtime.tax_localization_empty_state()
    state = runtime.tax_localization_configure_runtime(state, CONFIGURATION)["state"]
    for key, value in (
        ("tax_quote_precision", 2),
        ("filing_reconciliation_tolerance", 0.01),
        ("authority_retry_limit", 3),
        ("exemption_expiry_warning_days", 45),
        ("nexus_sales_threshold", 100000),
        ("workbench_limit", 100),
    ):
        state = runtime.tax_localization_set_parameter(state, key, value)["state"]
    state = runtime.tax_localization_register_rule(
        state,
        {
            "rule_id": "tax-filing-governance",
            "tenant": "tenant_tax",
            "scope": "filing",
            "status": "active",
            "requires_controller_approval": True,
        },
    )["state"]
    state = runtime.tax_localization_register_schema_extension(
        state,
        "tax_rule",
        {"local_authority_payload": "jsonb"},
    )["state"]
    return state


def tax_service() -> TaxLocalizationService:
    return TaxLocalizationService(configured_state())


def jurisdiction_payload() -> dict:
    return {
        "jurisdiction_id": "us_ca_san_francisco",
        "tenant": "tenant_tax",
        "country": "US",
        "region": "CA",
        "locality": "San Francisco",
        "authority_channel": "ca_cdtfa_api",
        "currency": "USD",
        "tax_types": ("sales_tax", "district_tax"),
        "filing_frequency": "monthly",
        "risk_signals": {"late_filing_rate": 0.02, "rule_volatility": 0.08, "channel_failure": 0.01},
        "identity": {"did": "did:appgen:tax-authority-ca", "issuer": "trusted_registry", "status": "active"},
    }


def tax_rule_payload() -> dict:
    return {
        "rule_id": "rule-standard-goods-ca-sf",
        "tenant": "tenant_tax",
        "jurisdiction_id": "us_ca_san_francisco",
        "tax_type": "sales_tax",
        "product_class": "standard_goods",
        "rate": 0.0875,
        "effective_from": "2026-01-01",
        "effective_to": None,
        "version": 1,
        "status": "active",
        "approval": "tax_controller",
        "rounding": {"precision": 2, "mode": "half_up"},
    }


def quote_payload(quote_id: str = "tax-quote-001") -> dict:
    return {
        "quote_id": quote_id,
        "tenant": "tenant_tax",
        "jurisdiction_id": "us_ca_san_francisco",
        "customer_id": "customer-001",
        "order_id": "order-001",
        "lines": (
            {"line_id": "line-001", "product_id": "sku-001", "product_class": "standard_goods", "amount": 1000.0, "quantity": 2},
        ),
    }


def configured_tax_service() -> TaxLocalizationService:
    service = tax_service()
    jurisdiction = service.command_tax_jurisdictions({"jurisdiction": jurisdiction_payload()})
    rule = service.command_tax_rules({"rule": tax_rule_payload()})
    assert jurisdiction["ok"] is True
    assert rule["ok"] is True
    return service


def test_tax_jurisdiction_rule_quote_invoice_and_filing_lifecycle_executes():
    service = configured_tax_service()
    classification = runtime.tax_localization_classify_product(
        "insulated bottle standard goods", taxonomy=("standard_goods", "food", "medical_device")
    )
    quote = service.command_tax_quotes({"quote": quote_payload()})
    invoice = service.command_tax_invoices_id_tax_records(
        {"invoice_id": "invoice-001", "calculation_id": quote["calculation"]["calculation_id"]}
    )
    filing = service.command_tax_filings(
        {
            "filing_id": "filing-2026-06",
            "jurisdiction_id": "us_ca_san_francisco",
            "period": "2026-06",
            "approved_by": "tax_controller",
        }
    )
    reconciliation = runtime.tax_localization_reconcile_tax_collected(
        service.state,
        jurisdiction_id="us_ca_san_francisco",
        collected=175.0,
        remitted=filing["filing"]["liability"],
    )
    route = runtime.tax_localization_route_tax_filing(
        filing["filing"],
        rails=(
            {"route": "authority_api", "available": False, "latency": 2},
            {"route": "secure_outbox", "available": True, "latency": 4},
        ),
    )
    workbench = service.query_tax_workbench({"tenant": "tenant_tax"})

    assert service.state["jurisdictions"]["us_ca_san_francisco"]["graph_degree"] >= 5
    assert service.state["rules"]["rule-standard-goods-ca-sf"]["compiled_hash"]
    assert classification["class"] == "standard_goods"
    assert classification["confidence"] >= 0.8
    assert quote["calculation"]["taxable_total"] == 2000.0
    assert quote["calculation"]["tax_total"] == 175.0
    assert quote["calculation"]["trace"][0]["rule_id"] == "rule-standard-goods-ca-sf"
    assert invoice["record"]["status"] == "recorded"
    assert filing["filing"]["liability"] == 175.0
    assert filing["filing"]["calculation_count"] == 1
    assert reconciliation["ok"] is True
    assert route["route"] == "secure_outbox"
    assert route["failover_used"] is True
    assert workbench["jurisdiction_count"] == 1
    assert workbench["calculation_count"] == 1
    assert workbench["filing_count"] == 1
    assert workbench["open_liability"] == 0.0
    assert {event["event_type"] for event in service.state["outbox"]} >= {
        "TaxJurisdictionRegistered",
        "TaxRuleActivated",
        "TaxCalculated",
        "InvoiceTaxRecorded",
        "TaxFilingPrepared",
    }


def test_tax_advanced_compliance_controls_and_simulations_are_executable():
    service = configured_tax_service()
    quote = service.command_tax_quotes({"quote": quote_payload()})
    invoice = service.command_tax_invoices_id_tax_records(
        {"invoice_id": "invoice-001", "calculation_id": quote["calculation"]["calculation_id"]}
    )
    filing = service.command_tax_filings(
        {
            "filing_id": "filing-2026-06",
            "jurisdiction_id": "us_ca_san_francisco",
            "period": "2026-06",
            "approved_by": "tax_controller",
        }
    )
    certificate = runtime.tax_localization_validate_exemption_certificate(
        {"certificate_id": "cert-001", "status": "active", "expires": "2027-01-01", "jurisdiction_id": "us_ca_san_francisco"}
    )
    nexus = runtime.tax_localization_determine_nexus(
        sales_amount=125000.0,
        transaction_count=180,
        thresholds={"sales_amount": 100000.0, "transaction_count": 200},
    )
    duty = runtime.tax_localization_calculate_cross_border_duties(goods_value=5000.0, duty_rate=0.04, de_minimis=800.0)
    compiled = runtime.tax_localization_compile_regulatory_rule(tax_rule_payload(), effective_date="2026-01-01")
    simulation = runtime.tax_localization_simulate_tax_policy_change(
        service.state,
        jurisdiction_id="us_ca_san_francisco",
        proposed_rate=0.095,
    )
    forecast = runtime.tax_localization_forecast_tax_liability((1000.0, 1500.0, 2000.0), effective_rate=0.0875, seasonality=1.1)
    proof = runtime.tax_localization_generate_tax_audit_proof(
        service.state,
        filing["filing"]["filing_id"],
        disclosure=("filing_id", "period", "liability"),
    )
    policy = runtime.tax_localization_screen_tax_policy(service.state, quote["calculation"]["calculation_id"], restricted_jurisdictions=("restricted_zone",))
    controls = runtime.tax_localization_run_control_tests(service.state)
    federation = runtime.tax_localization_federate_tax_view(service.state, "us_ca_san_francisco", external_systems=("ledger", "commerce"))
    document = runtime.tax_localization_integrate_digital_document_network(
        service.state,
        invoice["record"]["invoice_id"],
        {"clearance_id": "clear-001", "status": "cleared", "authority": "ca_cdtfa_api"},
    )
    identity = runtime.tax_localization_verify_tax_identity(jurisdiction_payload()["identity"])
    resilience = runtime.tax_localization_run_resilience_drill(service.state, "authority_channel_timeout")
    crypto = runtime.tax_localization_rotate_crypto_epoch(service.state, "dilithium3")
    carbon = runtime.tax_localization_schedule_carbon_aware_filing(
        ({"window": "09:00", "carbon_intensity": 330}, {"window": "02:00", "carbon_intensity": 105})
    )
    remittance = runtime.tax_localization_optimize_tax_remittance(
        liabilities=(
            {"jurisdiction_id": "us_ca_san_francisco", "amount": 175.0, "due_in_days": 10, "penalty_rate": 0.02},
            {"jurisdiction_id": "us_wa", "amount": 80.0, "due_in_days": 30, "penalty_rate": 0.01},
        ),
        available_cash=200.0,
    )
    allocation = runtime.tax_localization_allocate_shared_tax_liability(
        parties=(
            {"party": "seller", "exposure": 0.7, "bid": 1.0},
            {"party": "marketplace", "exposure": 0.3, "bid": 1.0},
        ),
        liability=175.0,
    )
    anomaly = runtime.tax_localization_detect_tax_anomaly(service.state)
    exposure = runtime.tax_localization_model_stochastic_tax_exposure(volume_path=(1000.0, 1400.0, 1600.0), rate_volatility=0.03)
    parsed = runtime.tax_localization_parse_tax_document("certificate cert_9 rate 8.75 jurisdiction us_ca")
    risk = runtime.tax_localization_score_jurisdiction_risk(service.state["jurisdictions"]["us_ca_san_francisco"])
    invariants = runtime.tax_localization_verify_formal_invariants(service.state)
    governed = runtime.tax_localization_register_governed_model(
        "taxability_classifier",
        {"auc": 0.91, "drift_score": 0.03, "features": ("description", "jurisdiction", "product_class")},
    )

    assert certificate["decision"] == "valid"
    assert nexus["nexus_required"] is True
    assert duty["duty"] == 168.0
    assert compiled["compiled_hash"] == service.state["rules"]["rule-standard-goods-ca-sf"]["compiled_hash"]
    assert simulation["delta_tax"] == 15.0
    assert forecast["expected_liability"] == 433.13
    assert proof["proof"].startswith("zk_tax_")
    assert policy["decision"] == "clear"
    assert controls["ok"] is True
    assert federation["systems"] == ("ledger", "commerce")
    assert document["status"] == "cleared"
    assert identity["ok"] is True
    assert resilience["mode"] == "degraded_authority_route"
    assert crypto["algorithm"] == "dilithium3"
    assert carbon["selected_window"] == "02:00"
    assert remittance["selected"][0]["jurisdiction_id"] == "us_ca_san_francisco"
    assert allocation["ok"] is True
    assert anomaly["ok"] is True
    assert exposure["tail_risk"] > exposure["expected_exposure"]
    assert parsed["certificate_id"] == "cert_9"
    assert risk["risk_score"] < 0.2
    assert invariants["ok"] is True
    assert governed["ok"] is True


def test_tax_ui_forms_wizards_controls_and_configuration_are_executable():
    service = configured_tax_service()
    quote = service.command_tax_quotes({"quote": quote_payload()})
    service.command_tax_invoices_id_tax_records({"invoice_id": "invoice-001", "calculation_id": quote["calculation"]["calculation_id"]})
    service.command_tax_filings(
        {
            "filing_id": "filing-2026-06",
            "jurisdiction_id": "us_ca_san_francisco",
            "period": "2026-06",
            "approved_by": "tax_controller",
        }
    )
    ui_contract = tax_localization_ui_contract()
    rendered = tax_localization_render_workbench(
        service.state,
        tenant="tenant_tax",
        principal_permissions=tuple(set(ui_contract["action_permissions"].values())),
    )

    assert ui_contract["ok"] is True
    assert rendered["ok"] is True
    assert "TaxLocalizationWorkbench" in rendered["fragments"]
    assert "TaxQuoteWorkbench" in rendered["fragments"]
    assert rendered["cards"][0]["key"] == "jurisdictions"
    assert rendered["cards"][1]["value"] == 1
    assert rendered["cards"][3]["value"] == 1
    assert rendered["forms"]
    assert rendered["wizards"]
    assert rendered["controls"]
    assert rendered["single_pbc_app"]["single_pbc_app"] is True
    assert rendered["binding_evidence"]["shared_table_access"] is False
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False



def test_tax_agent_routes_repository_and_release_surfaces_are_executable():
    service = configured_tax_service()
    quote = service.command_tax_quotes({"quote": quote_payload("tax-quote-surface")})
    invoice = service.command_tax_invoices_id_tax_records(
        {"invoice_id": "invoice-surface-001", "calculation_id": quote["calculation"]["calculation_id"]}
    )
    filing = service.command_tax_filings(
        {
            "filing_id": "filing-surface-2026-06",
            "jurisdiction_id": "us_ca_san_francisco",
            "period": "2026-06",
            "approved_by": "tax_controller",
        }
    )

    route_validation = routes.validate_api_route_contracts()
    route_dispatch = routes.dispatch_route(
        "POST",
        "/api/pbc/tax_localization/tax/jurisdictions",
        {
            "jurisdiction": {
                **jurisdiction_payload(),
                "jurisdiction_id": "us_wa_seattle",
                "region": "WA",
                "locality": "Seattle",
                "authority_channel": "wa_dor_api",
            }
        },
    )
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "California exemption certificate cert-001 and monthly filing instruction.",
        "Update the exemption certificate and prepare filing remittance evidence.",
        target_entity="exemption_certificate",
        requested_action="update",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        table="tax_localization_tax_filing",
        payload={"filing_id": "filing-agent", "jurisdiction_id": "us_ca_san_francisco"},
    )
    blocked_crud = agent.datastore_crud_plan("update", table="treasury_cash_bank_account", payload={"account_id": "bad"})
    assistant_preview = agent.tax_localization_assistant_preview(
        {
            "document_text": "Nexus threshold update for California filings.",
            "instructions": "Update the tax parameter and preview the mutation.",
            "target_entity": "tax_parameter",
            "requested_action": "update",
            "payload": {"name": "nexus_sales_threshold", "value": 150000},
        }
    )
    contribution = agent.composed_agent_contribution()

    repository = TaxLocalizationRepository()
    try:
        tables = repository.apply_schema()
        persisted = repository.save_runtime_snapshot(service.state)
        jurisdictions = repository.list_jurisdictions()
        calculations = repository.list_calculations()
        filings = repository.list_filings()
        outbox = repository.list_outbox_events()
        repo_manifest = repository.database_manifest()
    finally:
        repository.close()

    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()

    assert quote["ok"] is True
    assert invoice["record"]["status"] == "recorded"
    assert filing["filing"]["status"] == "prepared"
    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert all(contract["shared_table_access"] is False for contract in route_validation["contracts"])
    assert route_dispatch["ok"] is True
    assert route_dispatch["result"]["jurisdiction"]["status"] == "active"
    assert route_dispatch["side_effects"] == ()
    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document_plan["ok"] is True
    assert document_plan["candidate_table"] == "tax_localization_exemption_certificate"
    assert crud_plan["ok"] is True
    assert crud_plan["requires_confirmation"] is True
    assert crud_plan["event_contract"] == "AppGen-X"
    assert blocked_crud["ok"] is False
    assert assistant_preview["ok"] is True
    assert assistant_preview["mutation_preview"]["requires_confirmation"] is True
    assert contribution["ok"] is True
    assert "tax_localization_crud" in contribution["dsl_tools"]
    assert set(tables) >= {"tax_localization_tax_jurisdiction", "tax_localization_tax_filing", "tax_localization_appgen_outbox_event"}
    assert persisted["ok"] is True
    assert persisted["counts"]["jurisdictions"] == 1
    assert persisted["counts"]["calculations"] == 1
    assert persisted["counts"]["filings"] == 1
    assert len(jurisdictions) == 1
    assert calculations[0]["tax_total"] == 175.0
    assert filings[0]["liability"] == 175.0
    assert len(outbox) >= 5
    assert repo_manifest["shared_table_access"] is False
    assert repo_manifest["local_repository_backend"] == "sqlite"
    assert release_validation["ok"] is True
    assert release_smoke["ok"] is True


def test_tax_events_retry_dead_letter_manifest_and_configuration_guards():
    service = tax_service()
    processed = service.command_tax_events_inbox(
        {
            "event": {
                "event_id": "product-classified-evt-001",
                "event_type": "ProductClassified",
                "payload": {"tenant": "tenant_tax", "product_id": "sku-001", "product_class": "standard_goods", "confidence": 0.92},
            }
        }
    )
    duplicate = service.command_tax_events_inbox(
        {
            "event": {
                "event_id": "product-classified-evt-001",
                "event_type": "ProductClassified",
                "payload": {"tenant": "tenant_tax", "product_id": "sku-001", "product_class": "standard_goods"},
            }
        }
    )
    retrying = service.command_tax_events_inbox(
        {"event": {"event_id": "bad-tax-event", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_tax"}}}
    )
    dead_letter = service.command_tax_events_inbox(
        {"event": {"event_id": "bad-tax-event", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_tax"}}}
    )
    manifest = service_operation_manifest()

    assert processed["handler"]["status"] == "processed"
    assert service.state["product_taxability_projections"]["sku-001"]["confidence"] == 0.92
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(service.state["dead_letter"]) == 1
    assert manifest["event_contract"]["contract"] == "appgen_event_contract"
    assert {"command_tax_jurisdictions", "command_tax_quotes", "query_tax_workbench"} <= set(manifest["operations"])

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.tax_localization_configure_runtime(runtime.tax_localization_empty_state(), {**CONFIGURATION, "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.tax_localization_configure_runtime(runtime.tax_localization_empty_state(), {**CONFIGURATION, "stream_engine_picker": "kafka"})
