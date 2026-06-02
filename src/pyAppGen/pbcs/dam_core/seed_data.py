"""Executable seed-data contract for the dam_core PBC."""

from __future__ import annotations


PBC_KEY = "dam_core"
SEED_DATA = (
    {
        "table": "dam_core_dam_configuration",
        "rows": (
            {
                "code": "dam-core-default-config",
                "status": "active",
                "default_storage_tier": "warm",
                "default_locale": "en-US",
            },
        ),
    },
    {
        "table": "dam_core_rendition_profile",
        "rows": (
            {"code": "thumbnail", "status": "active", "mime_type": "image/jpeg"},
            {"code": "web_large", "status": "active", "mime_type": "image/jpeg"},
            {"code": "social_square", "status": "active", "mime_type": "image/jpeg"},
        ),
    },
    {
        "table": "dam_core_metadata_taxonomy",
        "rows": (
            {"code": "product", "status": "active"},
            {"code": "campaign", "status": "active"},
            {"code": "usage", "status": "active"},
        ),
    },
    {
        "table": "dam_core_rights_policy",
        "rows": (
            {"code": "commercial", "status": "active"},
            {"code": "editorial", "status": "active"},
            {"code": "restricted_review", "status": "active"},
        ),
    },
)


def seed_plan() -> dict:
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "row_count": sum(len(item["rows"]) for item in SEED_DATA),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
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
        "ok": plan["ok"] and not invalid_tables and not invalid_rows and plan["row_count"] >= 4,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
