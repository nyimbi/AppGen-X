"""Focused standalone workflow tests for inventory_positioning."""

from __future__ import annotations

from ..permissions import permission_manifest
from ..standalone import InventoryPositioningStandaloneApp
from ..standalone import standalone_app_contract


def test_standalone_bootstrap_and_workflow() -> None:
    app = InventoryPositioningStandaloneApp()
    bootstrap = app.bootstrap()
    assert bootstrap["ok"] is True
    workbench = app.render_workbench("tenant_alpha", permission_manifest()["permissions"])
    assert workbench["ok"] is True
    availability = app.dispatch("GET", "/inventory/availability", {"tenant": "tenant_alpha", "item_id": "sku_100", "demand_class": "standard"})
    assert availability["ok"] is True
    assert availability["result"]["available_to_promise"] > 0
    allocation = app.dispatch(
        "POST",
        "/inventory/allocations",
        {
            "allocation_id": "alloc_test_001",
            "tenant": "tenant_alpha",
            "order_id": "order_test_001",
            "item_id": "sku_100",
            "quantity": 15.0,
            "demand_class": "standard",
        },
    )
    assert allocation["ok"] is True
    release = app.dispatch("POST", "/inventory/allocations/alloc_test_001/release", {"reason": "customer_request"})
    assert release["ok"] is True
    hold = app.dispatch(
        "POST",
        "/inventory/quality-holds",
        {
            "hold_id": "hold_test_001",
            "node_id": "node_east",
            "item_id": "sku_100",
            "quantity": 3.0,
            "reason": "inspection",
        },
    )
    assert hold["ok"] is True
    assert standalone_app_contract()["ok"] is True
