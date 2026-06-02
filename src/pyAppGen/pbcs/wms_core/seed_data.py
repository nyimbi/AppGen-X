"""Executable seed-data contract for the wms_core PBC."""

from __future__ import annotations

from .runtime import WMS_CORE_REQUIRED_EVENT_TOPIC


PBC_KEY = "wms_core"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "timezone": "Africa/Nairobi",
    "label_format": "zpl",
    "edge_device_mode": "managed",
    "workbench_limit": 75,
}
DEFAULT_PARAMETERS = {
    "bin_capacity_tolerance": 0.95,
    "pick_wave_size": 4,
    "partial_pick_threshold": 0.5,
    "dock_queue_warning": 3,
    "labor_utilization_target": 0.82,
    "workbench_limit": 75,
}
DEFAULT_RULE = {
    "rule_id": "wms_core.putaway.fast_pick",
    "tenant": "tenant_demo",
    "scope": "putaway",
    "status": "active",
    "preferred_zones": ("fast_pick", "ambient_reserve"),
    "pick_method": "wave",
    "pack_material": "corrugate_medium",
    "hazard_compatible": True,
}


def demo_workspace_seed_bundle(tenant: str = "tenant_demo") -> dict:
    warehouse_id = f"wh_{tenant}"
    warehouse = {
        "warehouse_id": warehouse_id,
        "tenant": tenant,
        "name": "Nairobi Fulfillment Hub",
        "timezone": "Africa/Nairobi",
        "zones": ("fast_pick", "ambient_reserve", "crossdock"),
        "dock_doors": ("door_in_01", "door_out_01"),
        "pack_stations": ("pack_01", "pack_02"),
        "calendar": "weekday_day_shift",
        "identity": {
            "did": f"did:appgen:{tenant}:warehouse",
            "issuer": "trusted_registry",
            "status": "active",
        },
    }
    bins = (
        {
            "bin_id": f"bin_{tenant}_fp_01",
            "tenant": tenant,
            "warehouse_id": warehouse_id,
            "zone": "fast_pick",
            "capacity": 120.0,
            "current_load": 20.0,
            "status": "available",
            "temperature": "ambient",
            "hazard": "none",
            "pick_sequence": 10,
        },
        {
            "bin_id": f"bin_{tenant}_ar_01",
            "tenant": tenant,
            "warehouse_id": warehouse_id,
            "zone": "ambient_reserve",
            "capacity": 300.0,
            "current_load": 40.0,
            "status": "available",
            "temperature": "ambient",
            "hazard": "none",
            "pick_sequence": 20,
        },
    )
    receipt = {
        "receipt_id": f"rcpt_{tenant}_001",
        "tenant": tenant,
        "warehouse_id": warehouse_id,
        "item_id": "sku-coffee-1kg",
        "quantity": 36.0,
        "dock_door": "door_in_01",
        "lot_id": "lot-2026-05",
    }
    wave = {
        "wave_id": f"wave_{tenant}_001",
        "tenant": tenant,
        "warehouse_id": warehouse_id,
        "method": "cluster",
        "orders": (
            {
                "order_id": f"order_{tenant}_001",
                "item_id": receipt["item_id"],
                "quantity": 12.0,
                "priority": "cutoff",
            },
            {
                "order_id": f"order_{tenant}_002",
                "item_id": receipt["item_id"],
                "quantity": 8.0,
                "priority": "standard",
            },
        ),
    }
    inbound_events = (
        {
            "event_id": f"alloc_{tenant}_001",
            "event_type": "InventoryAllocated",
            "payload": {
                "tenant": tenant,
                "allocation_id": f"alloc_{tenant}_001",
                "item_id": receipt["item_id"],
                "quantity": receipt["quantity"],
            },
        },
        {
            "event_id": f"carrier_{tenant}_001",
            "event_type": "CarrierBooked",
            "payload": {
                "tenant": tenant,
                "booking_id": f"carrier_{tenant}_001",
                "carrier": "swiftline",
                "dock_door": "door_out_01",
            },
        },
        {
            "event_id": f"policy_{tenant}_001",
            "event_type": "AccessPolicyChanged",
            "payload": {
                "tenant": tenant,
                "policy_id": f"policy_{tenant}_001",
                "zone": "fast_pick",
                "status": "clear",
            },
        },
    )
    edge_command = {
        "command_id": f"edge_{tenant}_001",
        "device_id": "printer-pack-01",
        "kind": "print_label",
        "route": "primary",
        "payload": {"label_format": "zpl"},
    }
    rails = (
        {"route": "primary", "latency": 18, "available": True},
        {"route": "failover", "latency": 42, "available": True},
    )
    seed_rows = (
        {
            "table": "wms_core_warehouse",
            "rows": ({"tenant": tenant, "warehouse_id": warehouse_id, "name": warehouse["name"], "status": "active"},),
        },
        {
            "table": "wms_core_bin_location",
            "rows": tuple(
                {
                    "tenant": tenant,
                    "bin_id": item["bin_id"],
                    "warehouse_id": warehouse_id,
                    "zone": item["zone"],
                    "status": item["status"],
                }
                for item in bins
            ),
        },
        {
            "table": "wms_core_inbound_receipt",
            "rows": ({"tenant": tenant, "receipt_id": receipt["receipt_id"], "warehouse_id": warehouse_id, "status": "received"},),
        },
        {
            "table": "wms_core_pick_wave",
            "rows": ({"tenant": tenant, "wave_id": wave["wave_id"], "warehouse_id": warehouse_id, "status": "released"},),
        },
        {
            "table": "wms_core_wms_rule",
            "rows": ({"tenant": tenant, "rule_id": DEFAULT_RULE["rule_id"], "status": "active"},),
        },
        {
            "table": "wms_core_wms_parameter",
            "rows": tuple(
                {"tenant": tenant, "parameter": key, "status": "configured"}
                for key in DEFAULT_PARAMETERS
            ),
        },
        {
            "table": "wms_core_wms_configuration",
            "rows": ({"tenant": tenant, "configuration_id": f"cfg_{tenant}", "status": "configured"},),
        },
    )
    return {
        "tenant": tenant,
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": dict(DEFAULT_PARAMETERS),
        "rule": {**DEFAULT_RULE, "tenant": tenant},
        "warehouse": warehouse,
        "bins": bins,
        "receipt": receipt,
        "wave": wave,
        "projection_events": inbound_events,
        "edge_command": edge_command,
        "edge_rails": rails,
        "seed_rows": seed_rows,
    }


SEED_DATA = demo_workspace_seed_bundle()["seed_rows"]


def seed_plan(tenant: str = "tenant_demo") -> dict:
    """Return deterministic seed rows without applying them."""
    bundle = demo_workspace_seed_bundle(tenant=tenant)
    tables = tuple(dict.fromkeys(item["table"] for item in bundle["seed_rows"]))
    return {
        "ok": bool(bundle["seed_rows"]),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": bundle["seed_rows"],
        "configuration": bundle["configuration"],
        "parameters": bundle["parameters"],
        "side_effects": (),
    }


def validate_seed_data(tenant: str = "tenant_demo") -> dict:
    """Validate seed ownership and minimum row shape."""
    plan = seed_plan(tenant=tenant)
    invalid_tables = tuple(
        item["table"] for item in plan["rows"] if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in plan["rows"]
        for row in item.get("rows", ())
        if not row.get("tenant") or not any(
            key in row
            for key in (
                "warehouse_id",
                "bin_id",
                "receipt_id",
                "wave_id",
                "rule_id",
                "parameter",
                "configuration_id",
            )
        )
    )
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    bundle = demo_workspace_seed_bundle()
    validation = validate_seed_data()
    return {
        "ok": validation["ok"] and bundle["warehouse"]["name"] == "Nairobi Fulfillment Hub",
        "bundle": bundle,
        "validation": validation,
        "side_effects": (),
    }
