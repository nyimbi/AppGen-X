"""Seed data for a one-PBC case and knowledge app slice."""

from __future__ import annotations

from .domain_depth import PBC_KEY


SEED_ROWS = (
    {
        "table": f"{PBC_KEY}_case_queue",
        "values": {
            "id": "queue-triage-global",
            "tenant": "default",
            "code": "triage-global",
            "label": "Global Triage",
            "region": "global",
            "language": "en",
            "product_scope": "general",
            "capacity_limit": 18,
            "active_load": 0,
            "health": "healthy",
        },
    },
    {
        "table": f"{PBC_KEY}_case_queue",
        "values": {
            "id": "queue-api-platform",
            "tenant": "default",
            "code": "api-platform",
            "label": "API Platform",
            "region": "global",
            "language": "en",
            "product_scope": "platform",
            "capacity_limit": 12,
            "active_load": 0,
            "health": "healthy",
        },
    },
    {
        "table": f"{PBC_KEY}_case_queue",
        "values": {
            "id": "queue-billing-escalations",
            "tenant": "default",
            "code": "billing-escalations",
            "label": "Billing Escalations",
            "region": "global",
            "language": "en",
            "product_scope": "billing",
            "capacity_limit": 8,
            "active_load": 0,
            "health": "healthy",
        },
    },
    {
        "table": f"{PBC_KEY}_case_governed_model",
        "values": {
            "id": "model-support-grounded-assistant",
            "tenant": "default",
            "model_name": "support-grounded-assistant",
            "use_case": "next_best_resolution",
            "status": "active",
            "grounding_required": True,
            "citation_mode": "required",
        },
    },
    {
        "table": f"{PBC_KEY}_case_control_assertion",
        "values": {
            "id": "control-owned-table-boundary",
            "tenant": "default",
            "control_code": "owned_table_only",
            "subject_ref": "agent",
            "status": "active",
            "evidence": "All mutations must stay within case_knowledge_management_* tables.",
        },
    },
)


def seed_plan() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rows": SEED_ROWS,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    return {
        "ok": all(row["table"].startswith(f"{PBC_KEY}_") for row in SEED_ROWS),
        "rows": SEED_ROWS,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": seed_plan()["ok"] and validate_seed_data()["ok"],
        "side_effects": (),
    }
