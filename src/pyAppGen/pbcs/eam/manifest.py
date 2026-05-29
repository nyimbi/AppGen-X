"""Manifest for the Enterprise Asset Management PBC."""

from .runtime import EAM_CONSUMED_EVENT_TYPES
from .runtime import EAM_EMITTED_EVENT_TYPES
from .runtime import EAM_OWNED_TABLES
from .runtime import EAM_REQUIRED_CONFIGURATION_FIELDS
from .runtime import EAM_RUNTIME_CAPABILITY_KEYS
from .runtime import EAM_STANDARD_FEATURE_KEYS


PBC_KEY = 'eam'

PBC_MANIFEST = {
    "pbc": "eam",
    "label": "Enterprise Asset Management",
    "mesh": "opsmfg",
    "description": (
        "Asset hierarchy, preventive and predictive maintenance, condition monitoring, "
        "work orders, safety permits, spares, vendor service, reliability analytics, "
        "and governed maintenance automation."
    ),
    "datastore_backend": "postgresql",
    "tables": EAM_OWNED_TABLES,
    "apis": (
        "POST /equipment",
        "POST /maintenance-plans",
        "POST /work-orders",
        "POST /work-orders/{id}/schedule",
        "POST /work-orders/{id}/complete",
        "POST /condition-readings",
        "POST /meter-readings",
        "POST /spare-usage",
        "POST /safety-permits",
        "GET /maintenance-workbench",
        "POST /maintenance-rules",
        "POST /maintenance-parameters",
        "POST /maintenance-configuration",
    ),
    "emits": EAM_EMITTED_EVENT_TYPES,
    "consumes": EAM_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
        "MaintenanceWorkbench",
        "EquipmentRegistry",
        "AssetHierarchyMap",
        "MaintenancePlanConsole",
        "ConditionMonitoringPanel",
        "WorkOrderBoard",
        "MaintenanceScheduler",
        "SpareUsageConsole",
        "SafetyPermitConsole",
        "ReliabilityDashboard",
        "VendorServicePanel",
        "MaintenanceRuleStudio",
        "MaintenanceParameterConsole",
        "MaintenanceConfigurationPanel",
    ),
    "permissions": (
        "eam.read",
        "eam.equipment",
        "eam.plan",
        "eam.execute",
        "eam.safety",
        "eam.configure",
        "eam.audit",
    ),
    "configuration": EAM_REQUIRED_CONFIGURATION_FIELDS,
    "capabilities": tuple(f"eam.{table}" for table in EAM_OWNED_TABLES),
    "standard_features": EAM_STANDARD_FEATURE_KEYS,
    "workflows": (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_equipment",
        "create_maintenance_plan",
        "record_condition_reading",
        "record_meter_reading",
        "create_safety_permit",
        "create_work_order",
        "schedule_work_order",
        "issue_spare_part",
        "complete_work_order",
        "build_workbench_view",
    ),
    "analytics": (
        "plan_adherence",
        "backlog_risk",
        "schedule_compliance",
        "downtime_hours",
        "mtbf",
        "mttr",
        "spare_cost",
        "critical_work_order_count",
        "maintenance_completed_throughput",
        "vendor_performance_updated_throughput",
    ),
    "advanced_capabilities": EAM_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": (
        "SPECIFICATION.md",
        "RELEASE_EVIDENCE.md",
        "implementation-plan.md",
        "implementation-status.md",
        "README.md",
    ),
}
