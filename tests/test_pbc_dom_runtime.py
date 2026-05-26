import pytest

from pyAppGen.pbc import DOM_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import dom_apply_inventory_allocation
from pyAppGen.pbc import dom_apply_tax_projection
from pyAppGen.pbc import dom_build_workbench_view
from pyAppGen.pbc import dom_capture_order
from pyAppGen.pbc import dom_configure_runtime
from pyAppGen.pbc import dom_confirm_order_shipped
from pyAppGen.pbc import dom_create_fulfillment_plan
from pyAppGen.pbc import dom_empty_state
from pyAppGen.pbc import dom_price_order
from pyAppGen.pbc import dom_register_rule
from pyAppGen.pbc import dom_render_workbench
from pyAppGen.pbc import dom_runtime_capabilities
from pyAppGen.pbc import dom_runtime_smoke
from pyAppGen.pbc import dom_screen_fraud
from pyAppGen.pbc import dom_set_parameter
from pyAppGen.pbc import dom_ui_contract
from pyAppGen.pbc import dom_upsert_customer_projection
from pyAppGen.pbc import dom_verify_order
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.dom import DOM_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.dom import DOM_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.dom import DOM_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.dom import DOM_OWNED_TABLES
from pyAppGen.pbcs.dom import DOM_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.dom import dom_build_api_contract
from pyAppGen.pbcs.dom import dom_permissions_contract
from pyAppGen.pbcs.dom import dom_receive_event
from pyAppGen.pbcs.dom import dom_register_schema_extension
from pyAppGen.pbcs.dom import dom_verify_owned_table_boundary


def test_dom_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = dom_runtime_capabilities()
    smoke = dom_runtime_smoke()

    assert runtime["format"] == "appgen.dom-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/dom"
    assert len(runtime["standard_features"]) >= 18
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(DOM_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("dom")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "DomConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(DOM_ADVANCED_CAPABILITY_KEYS)
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "dom.event"
    assert contract["source_package"]["owned_tables"] == DOM_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == DOM_ALLOWED_DATABASE_BACKENDS
    assert pbc_implementation_release_audit(("dom",))["ok"] is True
    assert pbc_implemented_capability_audit(("dom",))["ok"] is True


def test_dom_runtime_applies_rules_parameters_and_configuration() -> None:
    state = dom_empty_state()
    state = dom_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": DOM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "allowed_channels": ("web", "store"),
            "allowed_statuses": ("captured", "verified", "priced", "planned", "shipped"),
            "workbench_limit": 50,
        },
    )["state"]
    state = dom_set_parameter(state, "fraud_threshold", 0.7)["state"]
    state = dom_set_parameter(state, "allocation_confidence_threshold", 0.75)["state"]
    state = dom_set_parameter(state, "partial_fulfillment_threshold", 0.5)["state"]
    state = dom_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "order_orchestration",
            "channels": ("web",),
            "customer_statuses": ("active",),
            "allow_split": True,
            "preferred_nodes": ("node_ops",),
            "restricted_destinations": ("restricted_zone",),
            "requires_tax": True,
            "status": "active",
        },
    )["state"]
    state = dom_upsert_customer_projection(
        state,
        {"customer_id": "cust_ops", "tenant": "tenant_ops", "status": "active", "risk": 0.08, "identity": {"did": "did:appgen:cust-ops", "issuer": "trusted_registry", "status": "active"}},
    )["state"]
    order = dom_capture_order(
        state,
        {
            "order_id": "order_ops",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "channel": "web",
            "currency": "USD",
            "destination": "SFO",
            "service_level": "standard",
            "lines": ({"line_id": "line_ops", "item_id": "sku_ops", "quantity": 1, "unit_price": 200},),
        },
    )
    state = order["state"]
    assert order["order"]["status"] == "captured"

    state = dom_apply_tax_projection(state, "order_ops", {"calculation_id": "tax_ops", "tax_total": 18, "status": "calculated"})["state"]
    state = dom_screen_fraud(state, "order_ops", signals={"ip_risk": 0.05, "velocity": 0.1, "customer_risk": 0.08})["state"]
    verified = dom_verify_order(state, "order_ops")
    state = verified["state"]
    assert verified["order"]["status"] == "verified"

    priced = dom_price_order(state, "order_ops")
    state = priced["state"]
    assert priced["order"]["total"] == 218

    allocation = dom_apply_inventory_allocation(
        state,
        "order_ops",
        {"allocation_id": "alloc_ops", "item_id": "sku_ops", "quantity": 1, "node_id": "node_ops", "confidence": 0.9},
    )
    state = allocation["state"]
    assert allocation["ok"] is True

    plan = dom_create_fulfillment_plan(state, "order_ops")
    state = plan["state"]
    assert plan["plan"]["node_id"] == "node_ops"
    assert plan["plan"]["status"] == "planned"

    shipped = dom_confirm_order_shipped(state, "order_ops", shipment_id="ship_ops")
    state = shipped["state"]
    assert shipped["order"]["status"] == "shipped"
    assert state["outbox"][-1]["idempotency_key"] == "dom:OrderShipped:dom_evt_000008"

    workbench = dom_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["order_count"] == 1
    assert workbench["shipped_count"] == 1
    assert workbench["open_order_count"] == 0
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 3
    assert workbench["binding_evidence"]["owned_tables"] == DOM_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["event_topic"] == DOM_REQUIRED_EVENT_TOPIC
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False

    ui_contract = dom_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == DOM_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["fixed_event_topic"] == DOM_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert "fraud_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert ui_contract["event_surfaces"]["emits"] == DOM_EMITTED_EVENT_TYPES
    assert ui_contract["event_surfaces"]["consumes"] == DOM_CONSUMED_EVENT_TYPES
    rendered = dom_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "dom.create",
            "dom.verify",
            "dom.price",
            "dom.allocate",
            "dom.plan",
            "dom.ship",
            "dom.event",
            "dom.audit",
            "dom.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 8
    assert rendered["event_inbox_count"] == 0
    assert rendered["dead_letter_count"] == 0
    assert rendered["binding_evidence"]["owned_tables"] == DOM_OWNED_TABLES
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_dom_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = dom_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        dom_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": DOM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Distributed Order Management parameter"):
        dom_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        dom_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.dom.events",
                "retry_limit": 3,
                "default_currency": "USD",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        dom_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": DOM_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "stream_engine_picker": "visible",
            },
        )


def test_dom_contracts_events_schema_and_boundaries_are_package_local() -> None:
    state = dom_configure_runtime(
        dom_empty_state(),
        {
            "database_backend": "mariadb",
            "event_topic": DOM_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "allowed_channels": ("web", "store"),
            "allowed_statuses": ("captured", "verified", "priced", "planned", "shipped"),
        },
    )["state"]

    extension = dom_register_schema_extension(
        state,
        "sales_order",
        {"channel_metadata": "jsonb", "promise_confidence": "numeric"},
    )
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["sales_order"]["promise_confidence"] == "numeric"

    with pytest.raises(ValueError, match="owned tables"):
        dom_register_schema_extension(state, "inventory_balance", {"foreign_stock": "numeric"})

    invalid = dom_register_schema_extension(state, "sales_order", {"BadField": "text"})
    assert invalid["ok"] is False
    assert invalid["error"] == "invalid_extension_field"

    api = dom_build_api_contract()
    assert api["format"] == "appgen.dom-api-contract.v1"
    assert api["database_backends"] == DOM_ALLOWED_DATABASE_BACKENDS
    assert api["owned_tables"] == DOM_OWNED_TABLES
    assert api["events"]["emits"] == DOM_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == DOM_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert any(route["command"] == "receive_event" for route in api["routes"])

    permissions = dom_permissions_contract()
    assert permissions["ok"] is True
    assert permissions["action_permissions"]["receive_event"] == "dom.event"
    assert "dom.configure" in permissions["permissions"]

    processed = dom_receive_event(
        state,
        {
            "event_id": "evt_alloc_1",
            "event_type": "InventoryAllocated",
            "payload": {"tenant": "tenant_ops", "allocation_id": "alloc_1", "item_id": "sku_ops", "quantity": 10},
        },
    )
    state = processed["state"]
    assert processed["ok"] is True
    assert state["inventory_allocation_projections"]["alloc_1"]["quantity"] == 10
    duplicate = dom_receive_event(
        state,
        {
            "event_id": "evt_alloc_1",
            "event_type": "InventoryAllocated",
            "payload": {"tenant": "tenant_ops", "allocation_id": "alloc_1"},
        },
    )
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    retry = dom_receive_event(
        state,
        {
            "event_id": "evt_bad",
            "event_type": "UnknownDomEvent",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert retry["ok"] is False
    assert retry["handler"]["status"] == "retrying"
    dead = dom_receive_event(retry["state"], {"event_id": "evt_bad", "event_type": "UnknownDomEvent", "payload": {"tenant": "tenant_ops"}})
    assert dead["handler"]["status"] == "dead_letter"
    assert dead["state"]["dead_letters"][-1]["reason"] == "unsupported_or_failed_dom_event"

    boundary = dom_verify_owned_table_boundary(("sales_order", "InventoryAllocated", "inventory_allocation_projection", "dom_custom_projection"))
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = dom_verify_owned_table_boundary(("inventory_balance", "customer_account"))
    assert violation["ok"] is False
    assert violation["violations"] == ("inventory_balance", "customer_account")
