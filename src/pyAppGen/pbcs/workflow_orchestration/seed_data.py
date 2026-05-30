"""Executable seed-data contract for the workflow_orchestration PBC."""

from __future__ import annotations

from .repository import workflow_orchestration_repository_contract


PBC_KEY = "workflow_orchestration"
SEED_DATA = (
    {
        "table": "workflow_orchestration_workflow_configuration",
        "rows": (
            {
                "configuration_id": "workflow_orchestration.default",
                "tenant": "tenant_demo",
                "database_backend": "postgresql",
                "event_topic": "appgen.workflow.events",
                "event_contract": "AppGen-X",
                "default_timezone": "UTC",
                "status": "active",
            },
        ),
    },
    {
        "table": "workflow_orchestration_workflow_parameter",
        "rows": (
            {"parameter_name": "default_retry_limit", "parameter_value": 3, "tenant": "tenant_demo", "status": "active"},
            {"parameter_name": "sla_breach_threshold", "parameter_value": 0.3, "tenant": "tenant_demo", "status": "active"},
        ),
    },
    {
        "table": "workflow_orchestration_workflow_definition",
        "rows": (
            {
                "workflow_id": "invoice_recovery",
                "tenant": "tenant_demo",
                "owner_pbc": "invoice_management",
                "version": "1.0.0",
                "status": "active",
            },
        ),
    },
    {
        "table": "workflow_orchestration_workflow_version",
        "rows": (
            {
                "version_id": "invoice_recovery_v1",
                "tenant": "tenant_demo",
                "workflow_id": "invoice_recovery",
                "semantic_version": "1.0.0",
                "status": "published",
            },
        ),
    },
    {
        "table": "workflow_orchestration_workflow_integration_endpoint",
        "rows": (
            {
                "endpoint_id": "endpoint_invoice_management",
                "tenant": "tenant_demo",
                "participant_pbc": "invoice_management",
                "route": "POST /invoices/recover",
                "status": "active",
            },
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
        "repository": workflow_orchestration_repository_contract(),
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
        if not row.get("tenant") or not row.get("status")
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


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
