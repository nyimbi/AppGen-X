"""Executable seed-data contract for the EAM PBC."""

from __future__ import annotations


PBC_KEY = "eam"
SEED_DATA = (
    {
        "table": "eam_maintenance_configuration",
        "rows": (
            {"code": "default_runtime", "status": "active", "database_backend": "postgresql", "event_topic": "appgen.maintenance.events"},
        ),
    },
    {
        "table": "eam_maintenance_parameter",
        "rows": (
            {"code": "default_pm_interval_days", "status": "active", "value": 30},
            {"code": "failure_risk_threshold", "status": "active", "value": 0.65},
            {"code": "safety_risk_threshold", "status": "active", "value": 0.70},
        ),
    },
    {
        "table": "eam_maintenance_rule",
        "rows": (
            {"code": "asset_readiness_gate", "status": "active", "rule_type": "maintenance"},
            {"code": "permit_required_for_execution", "status": "active", "rule_type": "safety"},
        ),
    },
    {
        "table": "eam_work_order",
        "rows": (
            {"code": "planned", "status": "active", "lane": "planning"},
            {"code": "scheduled", "status": "active", "lane": "dispatch"},
            {"code": "completed", "status": "active", "lane": "closure"},
        ),
    },
    {
        "table": "eam_meter_reading",
        "rows": (
            {"code": "hours", "status": "active", "category": "runtime_unit"},
            {"code": "cycles", "status": "active", "category": "runtime_unit"},
        ),
    },
    {
        "table": "eam_safety_permit",
        "rows": (
            {"code": "electrical", "status": "active", "category": "permit_class"},
            {"code": "hot_work", "status": "active", "category": "permit_class"},
            {"code": "confined_space", "status": "active", "category": "permit_class"},
        ),
    },
    {
        "table": "eam_spare_part_usage",
        "rows": (
            {"code": "planned_issue", "status": "active", "category": "consumption_reason"},
            {"code": "emergency_issue", "status": "active", "category": "consumption_reason"},
        ),
    },
    {
        "table": "eam_service_vendor_event",
        "rows": (
            {"code": "oem_service", "status": "active", "category": "vendor_service_class"},
            {"code": "specialist_repair", "status": "active", "category": "vendor_service_class"},
        ),
    },
    {
        "table": "eam_failure_event",
        "rows": (
            {"code": "low_risk", "status": "active", "band": "0.00-0.39"},
            {"code": "medium_risk", "status": "active", "band": "0.40-0.69"},
            {"code": "high_risk", "status": "active", "band": "0.70-1.00"},
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
        "category_count": len(SEED_DATA),
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_"))
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    required_seed_tables = {
        "eam_maintenance_configuration",
        "eam_maintenance_parameter",
        "eam_maintenance_rule",
        "eam_work_order",
        "eam_meter_reading",
        "eam_safety_permit",
        "eam_spare_part_usage",
        "eam_service_vendor_event",
        "eam_failure_event",
    }
    plan = seed_plan()
    missing_required = tuple(sorted(required_seed_tables - set(plan["tables"])))
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows and not missing_required,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "missing_required": missing_required,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
