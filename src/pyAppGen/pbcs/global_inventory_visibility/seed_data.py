"""Executable seed-data contract for the global_inventory_visibility PBC."""

from __future__ import annotations

from copy import deepcopy


PBC_KEY = "global_inventory_visibility"
_SEED_TENANT = "tenant_demo"


def standalone_seed_bundle(*, tenant: str = _SEED_TENANT) -> dict:
    """Return realistic package-local standalone seeds without writing rows."""
    return {
        "pbc": PBC_KEY,
        "tenant": tenant,
        "configuration": {
            "database_backend": "postgresql",
            "event_topic": "appgen.global_inventory_visibility.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "projection_horizon_days": 21,
            "staleness_sla_minutes": 90,
            "workbench_limit": 100,
        },
        "parameters": {
            "safety_stock_percent": 0.18,
            "freshness_half_life_hours": 48.0,
            "availability_confidence_floor": 0.58,
            "reservation_ttl_minutes": 180.0,
            "projection_horizon_days": 21.0,
            "stockout_risk_threshold": 0.37,
            "staleness_sla_minutes": 90.0,
            "carbon_cost_weight": 0.45,
            "federation_lag_tolerance_minutes": 30.0,
            "workbench_limit": 100.0,
        },
        "rules": (
            {
                "rule_id": "giv.demo.primary_pool_allocation",
                "tenant": tenant,
                "scope": "enterprise_pool",
                "status": "active",
                "rule_type": "allocation",
                "preferred_nodes": ("node_us_east", "node_us_west"),
                "freshness_floor": 0.62,
                "safety_stock_override": 18,
                "policy": "balanced_margin",
            },
            {
                "rule_id": "giv.demo.release_gate",
                "tenant": tenant,
                "scope": "release_gate",
                "status": "active",
                "rule_type": "exception_resolution",
                "required_event_contract": "AppGen-X",
                "max_dead_letters": 0,
                "max_stale_snapshots": 1,
                "requires_release_refresh": True,
            },
        ),
        "supply_nodes": (
            {
                "node_id": "node_us_east",
                "tenant": tenant,
                "node_type": "warehouse",
                "country": "US",
                "region": "EAST",
                "health_score": 0.96,
                "latency_ms": 18,
                "carbon_intensity": 145,
                "federated_systems": ("wms", "tms", "erp"),
                "identity": {
                    "did": "did:appgen:giv:node_us_east",
                    "issuer": "trusted_registry",
                    "status": "active",
                },
            },
            {
                "node_id": "node_us_west",
                "tenant": tenant,
                "node_type": "warehouse",
                "country": "US",
                "region": "WEST",
                "health_score": 0.88,
                "latency_ms": 24,
                "carbon_intensity": 95,
                "federated_systems": ("wms", "3pl"),
                "identity": {
                    "did": "did:appgen:giv:node_us_west",
                    "issuer": "trusted_registry",
                    "status": "active",
                },
            },
            {
                "node_id": "node_rotterdam_port",
                "tenant": tenant,
                "node_type": "port_hub",
                "country": "NL",
                "region": "EU",
                "health_score": 0.91,
                "latency_ms": 42,
                "carbon_intensity": 72,
                "federated_systems": ("tms", "customs", "erp"),
                "identity": {
                    "did": "did:appgen:giv:node_rotterdam_port",
                    "issuer": "trusted_registry",
                    "status": "active",
                },
            },
        ),
        "inventory_pools": (
            {
                "pool_id": "pool_global_primary",
                "tenant": tenant,
                "item_id": "sku_100",
                "pool_type": "enterprise",
                "node_ids": ("node_us_east", "node_us_west"),
                "allocation_policy": "balanced_margin",
                "safety_stock_units": 18,
                "lead_time_days": 3,
            },
            {
                "pool_id": "pool_transit_import",
                "tenant": tenant,
                "item_id": "sku_200",
                "pool_type": "in_transit",
                "node_ids": ("node_rotterdam_port", "node_us_east"),
                "allocation_policy": "import_lane_priority",
                "safety_stock_units": 12,
                "lead_time_days": 9,
            },
        ),
        "availability_snapshots": (
            {
                "snapshot_id": "snap_primary_east",
                "tenant": tenant,
                "pool_id": "pool_global_primary",
                "node_id": "node_us_east",
                "on_hand": 140.0,
                "reserved": 12.0,
                "allocated": 14.0,
                "in_transit": 20.0,
                "safety_stock": 12.0,
                "freshness_age_hours": 4.0,
                "staleness_minutes": 16.0,
            },
            {
                "snapshot_id": "snap_primary_west",
                "tenant": tenant,
                "pool_id": "pool_global_primary",
                "node_id": "node_us_west",
                "on_hand": 92.0,
                "reserved": 8.0,
                "allocated": 9.0,
                "in_transit": 14.0,
                "safety_stock": 9.0,
                "freshness_age_hours": 7.0,
                "staleness_minutes": 24.0,
            },
            {
                "snapshot_id": "snap_import_port",
                "tenant": tenant,
                "pool_id": "pool_transit_import",
                "node_id": "node_rotterdam_port",
                "on_hand": 35.0,
                "reserved": 4.0,
                "allocated": 6.0,
                "in_transit": 64.0,
                "safety_stock": 8.0,
                "freshness_age_hours": 5.0,
                "staleness_minutes": 18.0,
            },
            {
                "snapshot_id": "snap_import_east",
                "tenant": tenant,
                "pool_id": "pool_transit_import",
                "node_id": "node_us_east",
                "on_hand": 28.0,
                "reserved": 2.0,
                "allocated": 4.0,
                "in_transit": 18.0,
                "safety_stock": 6.0,
                "freshness_age_hours": 9.0,
                "staleness_minutes": 30.0,
            },
        ),
        "reservations": (
            {
                "reservation_id": "reservation_seed_web",
                "tenant": tenant,
                "pool_id": "pool_global_primary",
                "order_id": "so_seed_1001",
                "quantity": 11.0,
                "channel": "web",
            },
        ),
        "events": (
            {
                "event_id": "evt_seed_goods_receipt",
                "event_type": "GoodsReceiptPosted",
                "tenant": tenant,
                "pool_id": "pool_transit_import",
                "node_id": "node_rotterdam_port",
                "quantity": 22.0,
            },
            {
                "event_id": "evt_seed_shipment_delivered",
                "event_type": "ShipmentDelivered",
                "tenant": tenant,
                "pool_id": "pool_global_primary",
                "node_id": "node_us_west",
                "quantity": 9.0,
            },
            {
                "event_id": "evt_seed_inventory_allocated",
                "event_type": "InventoryAllocated",
                "tenant": tenant,
                "pool_id": "pool_global_primary",
                "node_id": "node_us_east",
                "quantity": 5.0,
            },
        ),
    }


def _seed_rows(*, tenant: str = _SEED_TENANT) -> tuple[dict, ...]:
    bundle = standalone_seed_bundle(tenant=tenant)
    return (
        {
            "table": "global_inventory_visibility_inventory_configuration",
            "rows": (
                {
                    "code": "GIV-CONFIG-001",
                    "configuration_id": "active",
                    "status": "active",
                    "tenant": tenant,
                    **bundle["configuration"],
                },
            ),
        },
        {
            "table": "global_inventory_visibility_inventory_parameter",
            "rows": tuple(
                {
                    "code": f"GIV-PARAM-{index:03d}",
                    "status": "active",
                    "tenant": tenant,
                    "parameter_name": name,
                    "parameter_value": value,
                }
                for index, (name, value) in enumerate(bundle["parameters"].items(), start=1)
            ),
        },
        {
            "table": "global_inventory_visibility_inventory_rule",
            "rows": tuple(
                {
                    "code": f"GIV-RULE-{index:03d}",
                    "status": rule["status"],
                    "tenant": tenant,
                    **rule,
                }
                for index, rule in enumerate(bundle["rules"], start=1)
            ),
        },
        {
            "table": "global_inventory_visibility_supply_node",
            "rows": tuple(
                {
                    "code": f"GIV-NODE-{index:03d}",
                    "status": "active",
                    "tenant": tenant,
                    **node,
                }
                for index, node in enumerate(bundle["supply_nodes"], start=1)
            ),
        },
        {
            "table": "global_inventory_visibility_inventory_pool",
            "rows": tuple(
                {
                    "code": f"GIV-POOL-{index:03d}",
                    "status": "active",
                    "tenant": tenant,
                    **pool,
                }
                for index, pool in enumerate(bundle["inventory_pools"], start=1)
            ),
        },
        {
            "table": "global_inventory_visibility_availability_snapshot",
            "rows": tuple(
                {
                    "code": f"GIV-SNAPSHOT-{index:03d}",
                    "status": "active",
                    "tenant": tenant,
                    **snapshot,
                }
                for index, snapshot in enumerate(bundle["availability_snapshots"], start=1)
            ),
        },
        {
            "table": "global_inventory_visibility_inventory_reservation",
            "rows": tuple(
                {
                    "code": f"GIV-RESERVATION-{index:03d}",
                    "status": "active",
                    "tenant": tenant,
                    **reservation,
                }
                for index, reservation in enumerate(bundle["reservations"], start=1)
            ),
        },
        {
            "table": "global_inventory_visibility_appgen_inbox_event",
            "rows": tuple(
                {
                    "code": f"GIV-EVENT-{index:03d}",
                    "status": "pending",
                    "tenant": tenant,
                    **event,
                }
                for index, event in enumerate(bundle["events"], start=1)
            ),
        },
    )


SEED_DATA = _seed_rows()


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": deepcopy(SEED_DATA),
        "bundle": standalone_seed_bundle(),
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership, minimum row shape, and standalone realism."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    required_domain_fields = (
        "pool_id",
        "node_id",
        "snapshot_id",
        "reservation_id",
        "rule_id",
        "parameter_name",
        "event_id",
        "configuration_id",
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code")
        or not row.get("status")
        or not row.get("tenant")
        or not any(field in row for field in required_domain_fields)
    )
    bundle = standalone_seed_bundle()
    realism_gaps = tuple(
        gap
        for gap, failed in (
            ("supply_nodes", len(bundle["supply_nodes"]) < 2),
            ("inventory_pools", len(bundle["inventory_pools"]) < 2),
            ("availability_snapshots", len(bundle["availability_snapshots"]) < 4),
            ("reservation_seed", len(bundle["reservations"]) < 1),
            ("event_seed", len(bundle["events"]) < 3),
        )
        if failed
    )
    plan = seed_plan()
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows and not realism_gaps,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "realism_gaps": realism_gaps,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
