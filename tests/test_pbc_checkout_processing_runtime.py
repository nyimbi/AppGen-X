import pytest

from pyAppGen.pbcs.checkout_processing import CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.checkout_processing import CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.checkout_processing import CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.checkout_processing import CHECKOUT_PROCESSING_OWNED_TABLES
from pyAppGen.pbcs.checkout_processing import CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.checkout_processing import CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.checkout_processing import checkout_processing_apply_coupon
from pyAppGen.pbcs.checkout_processing import checkout_processing_apply_tax_handoff
from pyAppGen.pbcs.checkout_processing import checkout_processing_build_api_contract
from pyAppGen.pbcs.checkout_processing import checkout_processing_build_workbench_view
from pyAppGen.pbcs.checkout_processing import checkout_processing_complete_checkout
from pyAppGen.pbcs.checkout_processing import checkout_processing_configure_runtime
from pyAppGen.pbcs.checkout_processing import checkout_processing_create_cart
from pyAppGen.pbcs.checkout_processing import checkout_processing_create_payment_intent
from pyAppGen.pbcs.checkout_processing import checkout_processing_empty_state
from pyAppGen.pbcs.checkout_processing import checkout_processing_open_checkout_session
from pyAppGen.pbcs.checkout_processing import checkout_processing_permissions_contract
from pyAppGen.pbcs.checkout_processing import checkout_processing_receive_event
from pyAppGen.pbcs.checkout_processing import checkout_processing_register_schema_extension
from pyAppGen.pbcs.checkout_processing import checkout_processing_register_rule
from pyAppGen.pbcs.checkout_processing import checkout_processing_render_workbench
from pyAppGen.pbcs.checkout_processing import checkout_processing_reserve_inventory_handoff
from pyAppGen.pbcs.checkout_processing import checkout_processing_runtime_capabilities
from pyAppGen.pbcs.checkout_processing import checkout_processing_runtime_smoke
from pyAppGen.pbcs.checkout_processing import checkout_processing_screen_risk
from pyAppGen.pbcs.checkout_processing import checkout_processing_set_parameter
from pyAppGen.pbcs.checkout_processing import checkout_processing_ui_contract
from pyAppGen.pbcs.checkout_processing import checkout_processing_validate_shipping_address
from pyAppGen.pbcs.checkout_processing import checkout_processing_verify_owned_table_boundary
from pyAppGen.pbcs.checkout_processing import checkout_processing_add_cart_line
from pyAppGen.pbcs.checkout_processing import implementation_contract


def test_checkout_processing_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = checkout_processing_runtime_capabilities()
    smoke = checkout_processing_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.checkout-processing-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/checkout_processing"
    assert runtime["owned_tables"] == CHECKOUT_PROCESSING_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    assert contract["pbc"] == "checkout_processing"
    assert contract["implementation_directory"] == "src/pyAppGen/pbcs/checkout_processing"
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["advanced_runtime"]["owned_tables"] == CHECKOUT_PROCESSING_OWNED_TABLES
    assert contract["ui_contract"]["ok"] is True
    assert contract["owned_tables"] == CHECKOUT_PROCESSING_OWNED_TABLES
    assert contract["allowed_database_backends"] == CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS
    assert contract["required_event_topic"] == CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC
    assert contract["emits"] == CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES
    assert contract["consumes"] == CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES
    assert contract["api_contract"]["shared_table_access"] is False
    assert contract["permissions_contract"]["action_permissions"]["receive_event"] == "checkout_processing.event.consume"
    assert contract["boundary_contract"]["ok"] is True
    assert "CheckoutConfigurationPanel" in contract["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS)

    api = checkout_processing_build_api_contract()
    permissions = checkout_processing_permissions_contract()
    assert api["format"] == "appgen.checkout-processing-api-contract.v1"
    assert api["owned_tables"] == CHECKOUT_PROCESSING_OWNED_TABLES
    assert api["database_backends"] == CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES
    assert api["consumes"] == CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert api["shared_table_access"] is False
    assert {route["route"] for route in api["routes"]} >= {
        "POST /carts",
        "POST /cart-lines",
        "POST /checkout",
        "POST /checkout/completions",
        "POST /checkout-processing/events/inbox",
        "GET /checkout-workbench",
    }
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["complete_checkout"] == "checkout_processing.checkout"
    assert permissions["action_permissions"]["receive_event"] == "checkout_processing.event.consume"


def test_checkout_processing_runtime_handles_checkout_flow_and_workbench_evidence() -> None:
    state = checkout_processing_empty_state()
    state = checkout_processing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_country": "US",
            "supported_shipping_options": ("standard", "express", "pickup"),
            "supported_payment_methods": ("card", "wallet"),
            "workbench_limit": 50,
        },
    )["state"]
    state = checkout_processing_set_parameter(state, "risk_threshold", 0.65)["state"]
    state = checkout_processing_set_parameter(state, "max_retry_attempts", 3)["state"]
    state = checkout_processing_set_parameter(state, "promotion_cap_rate", 0.15)["state"]
    extension = checkout_processing_register_schema_extension(
        state,
        "checkout_session",
        {"fraud_features": "jsonb", "delivery_promise_features": "jsonb"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["checkout_session"]["fraud_features"] == "jsonb"

    rule = checkout_processing_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "checkout_guard",
            "status": "active",
            "promotion_policy": {"max_discount_rate": 0.15, "stackable": False},
            "shipping_policy": {"allowed_countries": ("US",), "preferred_options": ("standard", "express")},
            "risk_policy": {"manual_review_threshold": 0.65, "block_threshold": 0.9},
            "payment_policy": {"allowed_methods": ("card",), "capture_mode": "authorize_then_capture"},
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"] == checkout_processing_register_rule(
        checkout_processing_empty_state(),
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "checkout_guard",
            "status": "active",
            "promotion_policy": {"max_discount_rate": 0.15, "stackable": False},
            "shipping_policy": {"allowed_countries": ("US",), "preferred_options": ("standard", "express")},
            "risk_policy": {"manual_review_threshold": 0.65, "block_threshold": 0.9},
            "payment_policy": {"allowed_methods": ("card",), "capture_mode": "authorize_then_capture"},
        },
    )["rule"]["compiled_hash"]

    product_event = {
        "event_id": "evt_product_ops",
        "event_type": "ProductPublished",
        "idempotency_key": "product:sku_ops:v1",
        "payload": {"tenant": "tenant_ops", "product_id": "sku_ops", "name": "Ops Pack", "category": "bags"},
    }
    state = checkout_processing_receive_event(state, product_event)["state"]
    duplicate = checkout_processing_receive_event(state, product_event)
    state = duplicate["state"]
    assert duplicate["duplicate"] is True

    state = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_price_ops",
            "event_type": "PriceOptimized",
            "idempotency_key": "price:sku_ops:v1",
            "payload": {"tenant": "tenant_ops", "product_id": "sku_ops", "unit_price": 120.0, "currency": "USD"},
        },
    )["state"]
    state = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_tax_ops",
            "event_type": "TaxCalculated",
            "idempotency_key": "tax:cart_ops:v1",
            "payload": {"tenant": "tenant_ops", "calculation_id": "tax_ops", "cart_id": "cart_ops", "tax_total": 11.4, "status": "calculated"},
        },
    )["state"]

    cart = checkout_processing_create_cart(
        state,
        {"cart_id": "cart_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "channel": "web", "currency": "USD", "market": "us"},
    )
    state = cart["state"]
    assert cart["cart"]["status"] == "open"

    line = checkout_processing_add_cart_line(
        state,
        {"line_id": "line_ops", "cart_id": "cart_ops", "tenant": "tenant_ops", "product_id": "sku_ops", "quantity": 1},
    )
    state = line["state"]
    assert line["line"]["unit_price"] == 120.0

    coupon = checkout_processing_apply_coupon(
        state,
        "cart_ops",
        {"coupon_code": "SAVE15", "requested_rate": 0.15, "campaign": "ops"},
    )
    state = coupon["state"]
    assert coupon["redemption"]["discount_total"] == 18.0

    address = checkout_processing_validate_shipping_address(
        state,
        "cart_ops",
        {"country": "US", "region": "CA", "city": "San Francisco", "postal_code": "94105", "shipping_option": "standard"},
    )
    state = address["state"]
    assert address["validation"]["status"] == "validated"

    session = checkout_processing_open_checkout_session(
        state,
        {"session_id": "chk_ops", "cart_id": "cart_ops", "tenant": "tenant_ops", "channel": "web", "instructions": "coupon SAVE15 ship standard"},
    )
    state = session["state"]
    assert session["session"]["order_id"] == "order_chk_ops"

    state = checkout_processing_apply_tax_handoff(state, "chk_ops", state["tax_quotes"]["tax_ops"])["state"]
    reservation = checkout_processing_reserve_inventory_handoff(
        state,
        "chk_ops",
        {"reservation_id": "res_ops", "tenant": "tenant_ops", "lines": ({"product_id": "sku_ops", "quantity": 1, "node_id": "node_ops"},), "confidence": 0.91},
    )
    state = reservation["state"]
    assert reservation["ok"] is True

    risk = checkout_processing_screen_risk(
        state,
        "chk_ops",
        {"velocity": 0.08, "account_age": 0.9, "address_match": 1.0, "payment_reputation": 0.95},
    )
    state = risk["state"]
    assert risk["decision"] == "clear"

    payment = checkout_processing_create_payment_intent(
        state,
        "chk_ops",
        {"payment_intent_id": "pi_ops", "tenant": "tenant_ops", "method": "card", "gateway": "appgen_pay"},
    )
    state = payment["state"]
    assert payment["payment_intent"]["amount"] == 118.4

    completed = checkout_processing_complete_checkout(state, "chk_ops")
    state = completed["state"]
    assert completed["ok"] is True
    assert completed["session"]["status"] == "completed"
    assert state["outbox"][-1]["idempotency_key"] == "checkout_processing:CheckoutCompleted:checkout_evt_000011"

    workbench = checkout_processing_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["cart_count"] == 1
    assert workbench["completed_checkout_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 3
    assert workbench["processed_event_count"] == 3
    assert workbench["rule_evidence"] == (rule["rule"]["compiled_hash"],)
    assert workbench["binding_evidence"]["owned_tables"] == CHECKOUT_PROCESSING_OWNED_TABLES

    ui_contract = checkout_processing_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["required_event_topic"] == CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["user_eventing_choice"] is False
    assert "risk_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "payment_policy" in ui_contract["rule_editor"]["required_fields"]

    rendered = checkout_processing_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "checkout_processing.cart",
            "checkout_processing.checkout",
            "checkout_processing.pricing",
            "checkout_processing.promotion",
            "checkout_processing.inventory",
            "checkout_processing.payment",
            "checkout_processing.risk",
            "checkout_processing.configure",
            "checkout_processing.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 11
    assert rendered["event_inbox_count"] == 3
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]

    boundary = checkout_processing_verify_owned_table_boundary(
        (
            "cart",
            "checkout_session",
            "ProductPublished",
            "price_projection",
            "POST /payment-intents",
            "checkout_processing_appgen_outbox_event",
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    violation = checkout_processing_verify_owned_table_boundary(("customer",))
    assert violation["ok"] is False
    assert violation["violations"] == ("customer",)


def test_checkout_processing_rejects_invalid_runtime_inputs_and_dead_letters_bad_events() -> None:
    state = checkout_processing_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        checkout_processing_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="requires the AppGen-X event topic"):
        checkout_processing_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.checkout.experimental",
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="stream-engine pickers or user-facing eventing choice"):
        checkout_processing_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "stream_engine": "forbidden_picker",
            },
        )

    state = checkout_processing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_country": "US",
            "supported_shipping_options": ("standard",),
            "supported_payment_methods": ("card",),
            "workbench_limit": 25,
        },
    )["state"]

    with pytest.raises(ValueError, match="Unsupported Checkout Processing parameter"):
        checkout_processing_set_parameter(state, "stream_engine", "forbidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        checkout_processing_register_schema_extension(state, "customer", {"profile": "jsonb"})

    with pytest.raises(ValueError, match="Missing required Checkout Processing rule fields"):
        checkout_processing_register_rule(
            state,
            {
                "rule_id": "bad_rule",
                "tenant": "tenant_ops",
                "scope": "checkout_guard",
                "status": "active",
            },
        )

    bad_event = checkout_processing_receive_event(
        state,
        {
            "event_id": "evt_bad",
            "event_type": "UnsupportedEvent",
            "idempotency_key": "bad:event",
            "attempts": 3,
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert bad_event["ok"] is False
    assert bad_event["dead_lettered"] is True
    assert bad_event["state"]["dead_letter"][0]["reason"] == "unsupported_event"
