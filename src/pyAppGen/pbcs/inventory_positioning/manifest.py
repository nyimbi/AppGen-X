"""Package manifest for the inventory_positioning PBC."""

from __future__ import annotations

from .runtime import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from .runtime import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_OWNED_TABLES
from .runtime import INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS
from .runtime import INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS


PBC_MANIFEST = {
    "pbc": "inventory_positioning",
    "label": "Inventory Positioning and State",
    "mesh": "scl",
    "description": "Inventory truth for items, nodes, lots, positions, receipts, adjustments, reservations, allocations, holds, in-transit projections, replenishment, and stock risk.",
    "datastore_backend": "postgresql",
    "database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
    "tables": tuple(table.removeprefix("inventory_positioning_") for table in INVENTORY_POSITIONING_OWNED_TABLES),
    "owned_tables": INVENTORY_POSITIONING_OWNED_TABLES,
    "apis": (
        "POST /inventory/items",
        "POST /inventory/nodes",
        "POST /inventory/receipts",
        "POST /inventory/adjustments",
        "GET /inventory/availability",
        "POST /inventory/allocations",
        "POST /inventory/allocations/{id}/release",
        "POST /inventory/quality-holds",
        "POST /inventory/events/inbox",
        "GET /inventory/workbench",
    ),
    "emits": INVENTORY_POSITIONING_EMITTED_EVENT_TYPES,
    "consumes": INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES,
    "template": "inventory",
    "ui_fragments": (
        "InventoryPositioningWorkbench",
        "ItemMasterConsole",
        "InventoryNodeConsole",
        "GoodsReceiptBoard",
        "InventoryAdjustmentConsole",
        "AvailabilityWorkbench",
        "AllocationConsole",
        "QualityHoldPanel",
        "TraceabilityPanel",
        "ReplenishmentSignalConsole",
        "InventoryConfigurationPanel",
        "InventoryAgentPanel",
    ),
    "permissions": (
        "inventory_positioning.read",
        "inventory_positioning.master",
        "inventory_positioning.receive",
        "inventory_positioning.adjust",
        "inventory_positioning.allocate",
        "inventory_positioning.release",
        "inventory_positioning.quality",
        "inventory_positioning.replenish",
        "inventory_positioning.reconcile",
        "inventory_positioning.event",
        "inventory_positioning.configure",
        "inventory_positioning.audit",
    ),
    "configuration": (
        "database_backend",
        "event_topic",
        "retry_limit",
        "default_uom",
        "precision",
        "allowed_statuses",
        "workbench_limit",
    ),
    "capabilities": INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS,
    "standard_features": INVENTORY_POSITIONING_STANDARD_FEATURE_KEYS,
    "workflows": (
        "register_item",
        "register_node",
        "post_goods_receipt",
        "post_adjustment",
        "calculate_availability",
        "allocate_inventory",
        "release_allocation",
        "apply_quality_hold",
        "receive_event",
        "build_workbench_view",
        "generate_replenishment_signal",
        "reconcile_inventory",
    ),
    "advanced_capabilities": INVENTORY_POSITIONING_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": (
        "tests/test_contract.py",
        "tests/test_runtime_capabilities.py",
        "tests/test_standalone_app.py",
        "tests/run_focused.py",
    ),
    "docs": (
        "README.md",
        "RELEASE_EVIDENCE.md",
        "implementation-plan.md",
        "implementation-status.md",
    ),
}
