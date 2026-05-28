"""Focused standalone application tests for the DOM PBC."""

from .. import agent, audit, routes, services, standalone, ui


def _service():
    service = services.DomStandaloneService(tenant="tenant_alpha")
    service.configure()
    service.register_defaults()
    service.upsert_customer_projection(
        {
            "tenant": "tenant_alpha",
            "customer_id": "cust_100",
            "status": "active",
            "risk": 0.05,
        }
    )
    return service


def test_standalone_order_journey_runs_end_to_end():
    service = _service()
    captured = service.capture_order(
        {
            "tenant": "tenant_alpha",
            "order_id": "order_100",
            "customer_id": "cust_100",
            "channel": "web",
            "destination": "BOS",
            "service_level": "standard",
            "currency": "USD",
            "lines": (
                {"line_id": "line_1", "item_id": "sku_100", "quantity": 2, "unit_price": 100},
                {"line_id": "line_2", "item_id": "sku_200", "quantity": 1, "unit_price": 50},
            ),
        }
    )
    taxed = service.apply_tax_projection("order_100", {"calculation_id": "tax_100", "tax_total": 25.0, "status": "calculated"})
    screened = service.screen_fraud("order_100", signals={"ip_risk": 0.05, "velocity": 0.05, "customer_risk": 0.05})
    verified = service.verify_order("order_100")
    priced = service.price_order("order_100")
    allocated = service.apply_inventory_allocation(
        "order_100",
        (
            {"allocation_id": "alloc_100", "item_id": "sku_100", "quantity": 2, "node_id": "node_east", "confidence": 0.9},
            {"allocation_id": "alloc_101", "item_id": "sku_200", "quantity": 1, "node_id": "node_west", "confidence": 0.88},
        ),
    )
    planned = service.create_fulfillment_plan("order_100")
    routed = service.route_fulfillment("order_100")
    shipped = service.confirm_order_shipped("order_100", shipment_id="ship_100")
    snapshot = service.get_order_snapshot("order_100")

    assert captured["ok"] is True
    assert taxed["ok"] is True
    assert screened["decision"] == "clear"
    assert verified["ok"] is True
    assert priced["order"]["total"] == 275.0
    assert allocated["ok"] is True
    assert len(allocated["allocation_set"]) == 2
    assert planned["ok"] is True
    assert len(planned["split_shipments"]) == 2
    assert routed["ok"] is True
    assert routed["route"] == "outbox"
    assert shipped["ok"] is True
    assert snapshot["order"]["status"] == "shipped"


def test_hold_release_cancellation_backorder_and_substitution_are_governed():
    service = _service()
    capture = service.capture_order(
        {
            "tenant": "tenant_alpha",
            "order_id": "order_200",
            "customer_id": "cust_100",
            "channel": "web",
            "destination": "BOS",
            "service_level": "standard",
            "lines": (
                {"line_id": "line_1", "item_id": "sku_300", "quantity": 4, "unit_price": 30},
            ),
        }
    )
    hold = service.app.apply_hold(order_id="order_200", hold_type="manual_review", reason="address mismatch")
    blocked = service.verify_order("order_200")
    released = service.release_hold(order_id="order_200", hold_id=hold["hold"]["hold_id"], released_by="qa")
    backorder = service.create_backorder(order_id="order_200", line_id="line_1", quantity=2, reason="supply_shortage")
    substitution = service.apply_substitution(order_id="order_200", line_id="line_1", substitute_item_id="sku_301")
    cancellation = service.request_cancellation(order_id="order_200", reason="customer changed mind")

    assert capture["ok"] is True
    assert hold["ok"] is True
    assert blocked["ok"] is False
    assert blocked["reason"] == "blocking_hold"
    assert released["ok"] is True
    assert backorder["ok"] is True
    assert substitution["ok"] is True
    assert cancellation["ok"] is True
    assert cancellation["cancellation"]["status"] == "approved"


def test_ui_agent_routes_and_audit_expose_standalone_surface():
    service = _service()
    dispatch = routes.dispatch_standalone_route(
        service,
        "POST",
        "/dom/orders",
        {
            "tenant": "tenant_alpha",
            "order_id": "order_300",
            "customer_id": "cust_100",
            "channel": "web",
            "destination": "BOS",
            "service_level": "express",
            "lines": ({"line_id": "line_1", "item_id": "sku_500", "quantity": 1, "unit_price": 200},),
        },
    )
    intake = agent.document_instruction_plan(
        "Order order_300 customer cust_100 channel web destination BOS amount 200 sku_500 x1 @200",
        "create the order and prepare the verification workbench",
    )
    workbench = service.workbench(tenant="tenant_alpha")
    ui_smoke = ui.smoke_test()
    audit_result = audit.run_dom_pbc_audit()

    assert dispatch["ok"] is True
    assert intake["ok"] is True
    assert intake["extracted"]["order_id"] == "order_300"
    assert intake["mutation_plan"]["ok"] is True
    assert workbench["ok"] is True
    assert workbench["forms"]
    assert workbench["wizards"]
    assert workbench["controls"]
    assert ui_smoke["ok"] is True
    assert audit_result["ok"] is True


def test_standalone_smoke_and_docs_presence():
    smoke = standalone.standalone_smoke_test()
    docs = standalone.documentation_presence()

    assert smoke["ok"] is True
    assert docs["ok"] is True
