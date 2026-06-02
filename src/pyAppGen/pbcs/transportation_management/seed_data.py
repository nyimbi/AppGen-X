"""Executable seed-data contract for the transportation_management PBC."""

from __future__ import annotations

from .runtime import TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC


PBC_KEY = "transportation_management"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "allowed_modes": ("truckload", "ltl", "parcel"),
    "telematics_providers": ("carrier_api", "gps_feed"),
    "timezone": "UTC",
    "workbench_limit": 75,
}
DEFAULT_PARAMETERS = {
    "max_cost_per_mile": 3.0,
    "on_time_weight": 0.35,
    "carbon_weight": 0.15,
    "service_level_weight": 0.2,
    "tracking_staleness_minutes": 45,
    "eta_confidence_threshold": 0.75,
    "tender_timeout_minutes": 20,
    "consolidation_threshold": 2,
    "delay_risk_threshold": 0.4,
    "exception_escalation_minutes": 60,
    "workbench_limit": 75,
}
DEFAULT_RULE = {
    "rule_id": "transportation_management.truckload.expedited",
    "tenant": "tenant_demo",
    "rule_type": "carrier_selection",
    "allowed_modes": ("truckload", "ltl"),
    "preferred_carriers": ("carrier_fast",),
    "restricted_carriers": ("carrier_suspended",),
    "service_level": "expedited",
    "hazmat_allowed": False,
    "status": "active",
}


def demo_workspace_seed_bundle(tenant: str = "tenant_demo") -> dict:
    shipment_id = f"ship_{tenant}_001"
    shipment = {
        "shipment_id": shipment_id,
        "tenant": tenant,
        "source_ref": f"packed_{tenant}_001",
        "origin": "LAX",
        "destination": "SFO",
        "weight": 800.0,
        "mode": "truckload",
        "service_level": "expedited",
        "hazmat": False,
        "temperature_controlled": False,
    }
    carriers = (
        {
            "carrier_id": "carrier_fast",
            "tenant": tenant,
            "mode": "truckload",
            "service_levels": ("expedited", "standard"),
            "lanes": (("LAX", "SFO"), ("LAX", "LAS")),
            "cost_per_mile": 2.35,
            "on_time_rate": 0.96,
            "carbon_per_mile": 132,
            "risk": 0.07,
            "identity": {"did": "did:appgen:carrier-fast", "issuer": "trusted_registry", "status": "active"},
        },
        {
            "carrier_id": "carrier_green",
            "tenant": tenant,
            "mode": "truckload",
            "service_levels": ("expedited", "economy"),
            "lanes": (("LAX", "SFO"), ("PHX", "DEN")),
            "cost_per_mile": 2.1,
            "on_time_rate": 0.88,
            "carbon_per_mile": 82,
            "risk": 0.12,
            "identity": {"did": "did:appgen:carrier-green", "issuer": "trusted_registry", "status": "active"},
        },
    )
    projection_events = (
        {
            "event_id": f"packed_{tenant}_001",
            "event_type": "Packed",
            "payload": {"tenant": tenant, "pack_id": f"packed_{tenant}_001", "shipment_id": shipment_id, "package_count": 3},
        },
        {
            "event_id": f"po_{tenant}_001",
            "event_type": "PurchaseOrderIssued",
            "payload": {"tenant": tenant, "purchase_order_id": f"po_{tenant}_001", "supplier_id": "supplier_demo"},
        },
        {
            "event_id": f"policy_{tenant}_001",
            "event_type": "AccessPolicyChanged",
            "payload": {"tenant": tenant, "policy_id": f"policy_{tenant}_001", "status": "clear"},
        },
    )
    seed_rows = (
        {"table": "transportation_management_shipment", "rows": ({"tenant": tenant, "shipment_id": shipment_id, "status": "delivered"},)},
        {"table": "transportation_management_carrier", "rows": tuple({"tenant": tenant, "carrier_id": item["carrier_id"], "status": "active"} for item in carriers)},
        {"table": "transportation_management_freight_route", "rows": ({"tenant": tenant, "route_id": f"route_{shipment_id}", "shipment_id": shipment_id, "status": "planned"},)},
        {"table": "transportation_management_tracking_event", "rows": ({"tenant": tenant, "event_id": f"track_{tenant}_001", "shipment_id": shipment_id, "status": "observed"},)},
        {"table": "transportation_management_delivery_proof", "rows": ({"tenant": tenant, "proof_id": f"proof_{shipment_id}", "shipment_id": shipment_id, "status": "confirmed"},)},
        {"table": "transportation_management_transportation_rule", "rows": ({"tenant": tenant, "record_id": DEFAULT_RULE["rule_id"], "status": "active"},)},
        {"table": "transportation_management_transportation_parameter", "rows": tuple({"tenant": tenant, "record_id": key, "status": "configured"} for key in DEFAULT_PARAMETERS)},
        {"table": "transportation_management_transportation_configuration", "rows": ({"tenant": tenant, "record_id": f"cfg_{tenant}", "status": "configured"},)},
    )
    return {
        "tenant": tenant,
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": dict(DEFAULT_PARAMETERS),
        "rule": {**DEFAULT_RULE, "tenant": tenant},
        "shipment": shipment,
        "carriers": carriers,
        "distance_miles": 380.0,
        "stops": ("LAX", "Bakersfield", "SFO"),
        "tracking_event": {"event_id": f"track_{tenant}_001", "location": "Bakersfield", "distance_remaining": 180, "delay_minutes": 10},
        "projection_events": projection_events,
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
    invalid_tables = tuple(item["table"] for item in plan["rows"] if not item.get("table", "").startswith(f"{PBC_KEY}_"))
    invalid_rows = tuple(
        row
        for item in plan["rows"]
        for row in item.get("rows", ())
        if not row.get("tenant") or not any(key in row for key in ("shipment_id", "carrier_id", "route_id", "event_id", "proof_id", "record_id"))
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
        "ok": validation["ok"] and bundle["shipment"]["mode"] == "truckload",
        "bundle": bundle,
        "validation": validation,
        "side_effects": (),
    }
