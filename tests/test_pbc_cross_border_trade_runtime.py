import pytest

from pyAppGen.pbcs.cross_border_trade import CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.cross_border_trade import implementation_contract
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_build_workbench_view
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_classify_product
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_configure_runtime
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_empty_state
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_file_customs_declaration
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_quote_landed_cost
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_receive_event
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_register_rule
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_render_workbench
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_runtime_capabilities
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_runtime_smoke
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_screen_export_control
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_set_parameter
from pyAppGen.pbcs.cross_border_trade import cross_border_trade_ui_contract


def test_cross_border_trade_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = cross_border_trade_runtime_capabilities()
    smoke = cross_border_trade_runtime_smoke()

    assert runtime["format"] == "appgen.cross-border-trade-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/cross_border_trade"
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(CROSS_BORDER_TRADE_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = implementation_contract()
    assert contract["ok"] is True
    assert contract["side_effect_free"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert "TradeConfigurationPanel" in contract["ui_contract"]["fragments"]
    assert contract["api_contract"]["shared_table_access"] is False


def test_cross_border_trade_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = cross_border_trade_empty_state()
    state = cross_border_trade_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.cross_border_trade.events",
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_countries": ("US", "CA"),
            "supported_incoterms": ("DAP", "DDP"),
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("classification_confidence_threshold", 0.75),
        ("restricted_party_review_threshold", 0.8),
        ("duty_variance_tolerance", 10.0),
        ("de_minimis_value", 800.0),
        ("broker_latency_weight", 0.25),
        ("broker_cost_weight", 0.25),
        ("broker_compliance_weight", 0.35),
        ("carbon_weight", 0.15),
    ):
        state = cross_border_trade_set_parameter(state, name, value)["state"]
    rule = cross_border_trade_register_rule(
        state,
        {
            "rule_id": "rule_trade_ops",
            "tenant": "tenant_ops",
            "scope": "cross_border_trade",
            "status": "active",
            "classification_policy": {"confidence_floor": 0.75, "restricted_keywords": ("encryption",), "manual_review_keywords": ("battery",)},
            "landed_cost_policy": {"default_duty_rate": 0.08, "default_tax_rate": 0.12, "broker_fee": 24.0, "insurance_rate": 0.01},
            "export_control_policy": {"blocked_destinations": ("restricted_zone",), "license_required_keywords": ("encryption",), "review_score": 0.8},
            "declaration_policy": {"required_documents": ("commercial_invoice", "packing_list"), "preferred_brokers": ("broker_priority",), "submit_when_cleared": True},
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]

    state = cross_border_trade_receive_event(
        state,
        {
            "event_id": "evt_order_ops",
            "event_type": "OrderPlaced",
            "idempotency_key": "order:ops:v1",
            "payload": {
                "tenant": "tenant_ops",
                "order_id": "order_ops",
                "customer_id": "cust_ops",
                "destination_country": "CA",
                "currency": "USD",
                "items": ({"product_id": "sku_ops", "quantity": 1, "unit_value": 120.0},),
            },
        },
    )["state"]
    classification = cross_border_trade_classify_product(
        state,
        {
            "classification_id": "hsc_ops",
            "tenant": "tenant_ops",
            "product_id": "sku_ops",
            "description": "digital camera kit",
            "country_of_origin": "US",
            "destination_country": "CA",
            "material_facts": ("camera",),
        },
    )
    state = classification["state"]
    assert classification["hs_classification"]["hs_code"] == "8525.80"
    quote = cross_border_trade_quote_landed_cost(
        state,
        {
            "quote_id": "lcq_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "classification_id": "hsc_ops",
            "incoterm": "DDP",
            "origin_country": "US",
            "destination_country": "CA",
            "goods_value": 120.0,
            "shipping_cost": 15.0,
            "currency": "USD",
        },
    )
    state = quote["state"]
    assert quote["landed_cost_quote"]["landed_total"] > 120.0
    export_check = cross_border_trade_screen_export_control(
        state,
        {
            "check_id": "ecc_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "classification_id": "hsc_ops",
            "destination_country": "CA",
            "counterparties": ({"name": "Aster Distribution", "risk_score": 0.05},),
        },
    )
    state = export_check["state"]
    assert export_check["export_control_check"]["decision"] == "cleared"
    declaration = cross_border_trade_file_customs_declaration(
        state,
        {
            "declaration_id": "ccd_ops",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "quote_id": "lcq_ops",
            "check_id": "ecc_ops",
            "documents": ("commercial_invoice", "packing_list"),
        },
    )
    state = declaration["state"]
    assert declaration["customs_declaration"]["status"] == "filed"
    assert state["outbox"][-1]["idempotency_key"].startswith("cross_border_trade:CustomsDeclarationFiled")

    workbench = cross_border_trade_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["classification_count"] == 1
    assert workbench["quote_count"] == 1
    assert workbench["export_control_count"] == 1
    assert workbench["declaration_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 8

    ui_contract = cross_border_trade_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["user_eventing_choice"] is False
    rendered = cross_border_trade_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "cross_border_trade.classify",
            "cross_border_trade.quote",
            "cross_border_trade.screen",
            "cross_border_trade.declare",
            "cross_border_trade.audit",
            "cross_border_trade.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert not rendered["locked_actions"]
    assert rendered["owned_tables"] == ("hs_classification", "landed_cost_quote", "export_control_check", "customs_declaration")


def test_cross_border_trade_rejects_invalid_runtime_inputs_and_records_dead_letters() -> None:
    state = cross_border_trade_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        cross_border_trade_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.cross_border_trade.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_countries": ("US",),
                "supported_incoterms": ("DDP",),
            },
        )
    state = cross_border_trade_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.cross_border_trade.events",
            "retry_limit": 1,
            "default_currency": "USD",
            "supported_countries": ("US",),
            "supported_incoterms": ("DDP",),
        },
    )["state"]
    with pytest.raises(ValueError, match="Unsupported Cross Border Trade parameter"):
        cross_border_trade_set_parameter(state, "stream_engine", 1)
    failed = cross_border_trade_receive_event(
        state,
        {"event_id": "evt_unknown", "event_type": "UnknownEvent", "idempotency_key": "unknown:1", "attempts": 1, "payload": {"tenant": "tenant_ops"}},
    )
    assert failed["ok"] is False
    assert failed["dead_lettered"] is True
    assert len(failed["state"]["dead_letter"]) == 1
