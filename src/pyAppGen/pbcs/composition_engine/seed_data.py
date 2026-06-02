"""Executable seed-data contract for the composition_engine PBC."""

from __future__ import annotations

PBC_KEY = "composition_engine"
SEED_DATA = (
    {
        "table": "composition_engine_composition_configuration",
        "rows": (
            {
                "code": "COMPOSITION-CONFIG-DEFAULT",
                "status": "active",
                "database_backend": "postgresql",
                "event_topic": "appgen.composition.events",
            },
        ),
    },
    {
        "table": "composition_engine_composition_parameter",
        "rows": (
            {"code": "PARAM-ROUTE-BUDGET", "status": "active", "key": "route_budget", "value": 24},
            {"code": "PARAM-PREVIEW-BATCH", "status": "active", "key": "preview_batch_limit", "value": 50},
        ),
    },
    {
        "table": "composition_engine_composition_rule",
        "rows": (
            {
                "code": "RULE-RELEASE-GATE",
                "status": "active",
                "scope": "workspace",
                "required_fragments": ("CompositionWorkbench",),
                "allowed_meshes": ("platform", "relationship", "operations"),
            },
        ),
    },
    {
        "table": "composition_engine_composition_workspace",
        "rows": (
            {
                "code": "WS-COMPOSITION-DEMO",
                "status": "draft",
                "tenant": "tenant_demo",
                "workspace_id": "ws_demo",
                "name": "Customer Ops Console",
            },
        ),
    },
    {
        "table": "composition_engine_ui_fragment",
        "rows": (
            {
                "code": "FRAGMENT-COMPOSITION-WORKBENCH",
                "status": "active",
                "fragment_id": "frag_composition_workbench",
                "route": "/customers/ops",
            },
        ),
    },
)


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    plan = seed_plan()
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
