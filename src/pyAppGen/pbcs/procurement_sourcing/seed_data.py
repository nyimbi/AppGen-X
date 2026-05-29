"""Executable seed-data contract for the procurement_sourcing PBC."""

from __future__ import annotations

from .runtime import PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC


PBC_KEY = "procurement_sourcing"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": PROCUREMENT_SOURCING_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "allowed_categories": ("direct_materials", "maintenance", "professional_services"),
    "workbench_limit": 75,
}
DEFAULT_PARAMETERS = {
    "approval_limit": 5000,
    "minimum_bid_count": 2,
    "supplier_risk_threshold": 0.4,
    "price_variance_tolerance": 0.1,
    "renewal_horizon_days": 90,
    "workbench_limit": 75,
}
DEFAULT_RULE = {
    "rule_id": "procurement_sourcing.direct_materials.source_to_contract",
    "tenant": "tenant_demo",
    "rule_type": "sourcing",
    "category": "direct_materials",
    "preferred_suppliers": ("supplier_alpha",),
    "restricted_suppliers": ("supplier_sanctioned",),
    "score_weights": {"price": 0.45, "lead_time": 0.2, "risk": 0.2, "quality": 0.15},
    "allow_split_award": True,
    "status": "active",
}


def demo_workspace_seed_bundle(tenant: str = "tenant_demo") -> dict:
    requisition_id = f"req_{tenant}_001"
    rfq_id = f"rfq_{tenant}_001"
    award_id = f"award_{tenant}_001"
    contract_id = f"contract_{tenant}_001"
    po_id = f"po_{tenant}_001"
    requisition = {
        "requisition_id": requisition_id,
        "tenant": tenant,
        "legal_entity": "entity_demo",
        "category": "direct_materials",
        "item_id": "sku-copper-wire-10mm",
        "quantity": 120.0,
        "estimated_amount": 3600.0,
        "currency": "USD",
        "cost_center": "manufacturing",
        "requested_by": "planner.demo",
    }
    suppliers = ("supplier_alpha", "supplier_beta", "supplier_gamma")
    bids = (
        {
            "supplier_id": "supplier_alpha",
            "price": 3450.0,
            "lead_time_days": 8,
            "risk": 0.12,
            "quality": 0.96,
            "carbon": 125.0,
            "identity": {"did": "did:appgen:supplier-alpha", "issuer": "trusted_registry", "status": "active"},
        },
        {
            "supplier_id": "supplier_beta",
            "price": 3325.0,
            "lead_time_days": 12,
            "risk": 0.18,
            "quality": 0.91,
            "carbon": 80.0,
            "identity": {"did": "did:appgen:supplier-beta", "issuer": "trusted_registry", "status": "active"},
        },
        {
            "supplier_id": "supplier_gamma",
            "price": 3500.0,
            "lead_time_days": 9,
            "risk": 0.22,
            "quality": 0.92,
            "carbon": 97.0,
            "identity": {"did": "did:appgen:supplier-gamma", "issuer": "trusted_registry", "status": "active"},
        },
    )
    projection_events = (
        {
            "event_id": f"shortage_{tenant}_001",
            "event_type": "MaterialShortageDetected",
            "payload": {"tenant": tenant, "shortage_id": f"shortage_{tenant}_001", "item_id": requisition["item_id"], "quantity": requisition["quantity"]},
        },
        {
            "event_id": f"budget_{tenant}_001",
            "event_type": "BudgetChanged",
            "payload": {"tenant": tenant, "budget_id": f"budget_{tenant}_001", "cost_center": requisition["cost_center"], "available_amount": 25000.0},
        },
        {
            "event_id": f"risk_{tenant}_001",
            "event_type": "SupplierRiskChanged",
            "payload": {"tenant": tenant, "supplier_id": "supplier_alpha", "risk_score": 0.12, "status": "clear"},
        },
    )
    seed_rows = (
        {
            "table": "procurement_sourcing_purchase_requisition",
            "rows": ({"tenant": tenant, "requisition_id": requisition_id, "status": "approved", "estimated_amount": requisition["estimated_amount"]},),
        },
        {
            "table": "procurement_sourcing_rfq",
            "rows": ({"tenant": tenant, "rfq_id": rfq_id, "requisition_id": requisition_id, "status": "open"},),
        },
        {
            "table": "procurement_sourcing_supplier_bid",
            "rows": tuple({"tenant": tenant, "bid_id": f"bid_{tenant}_{index}", "rfq_id": rfq_id, "supplier_id": bid["supplier_id"], "price": bid["price"]} for index, bid in enumerate(bids, 1)),
        },
        {
            "table": "procurement_sourcing_supplier_award",
            "rows": ({"tenant": tenant, "award_id": award_id, "rfq_id": rfq_id, "status": "awarded"},),
        },
        {
            "table": "procurement_sourcing_vendor_contract",
            "rows": ({"tenant": tenant, "contract_id": contract_id, "award_id": award_id, "status": "active"},),
        },
        {
            "table": "procurement_sourcing_purchase_order",
            "rows": ({"tenant": tenant, "po_id": po_id, "contract_id": contract_id, "status": "issued"},),
        },
        {
            "table": "procurement_sourcing_rule",
            "rows": ({"tenant": tenant, "record_id": DEFAULT_RULE["rule_id"], "status": "active"},),
        },
        {
            "table": "procurement_sourcing_parameter",
            "rows": tuple({"tenant": tenant, "record_id": key, "status": "configured"} for key in DEFAULT_PARAMETERS),
        },
        {
            "table": "procurement_sourcing_configuration",
            "rows": ({"tenant": tenant, "record_id": f"cfg_{tenant}", "status": "configured"},),
        },
    )
    return {
        "tenant": tenant,
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": dict(DEFAULT_PARAMETERS),
        "rule": {**DEFAULT_RULE, "tenant": tenant},
        "requisition": requisition,
        "rfq_id": rfq_id,
        "suppliers": suppliers,
        "bids": bids,
        "award_id": award_id,
        "contract_id": contract_id,
        "po_id": po_id,
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
    invalid_tables = tuple(
        item["table"] for item in plan["rows"] if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in plan["rows"]
        for row in item.get("rows", ())
        if not row.get("tenant") or not any(key in row for key in ("requisition_id", "rfq_id", "bid_id", "award_id", "contract_id", "po_id", "record_id"))
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
        "ok": validation["ok"] and bundle["requisition"]["category"] == "direct_materials",
        "bundle": bundle,
        "validation": validation,
        "side_effects": (),
    }
