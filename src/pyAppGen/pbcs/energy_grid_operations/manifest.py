"""Package manifest for the energy_grid_operations PBC."""

from __future__ import annotations

from .runtime import (
    ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_OWNED_TABLES,
    ENERGY_GRID_OPERATIONS_STANDARD_FEATURE_KEYS,
    PBC_KEY,
    energy_grid_operations_build_api_contract,
    energy_grid_operations_permissions_contract,
    energy_grid_operations_runtime_capabilities,
)

_RUNTIME_CAPABILITIES = energy_grid_operations_runtime_capabilities()
_API_CONTRACT = energy_grid_operations_build_api_contract()

PBC_MANIFEST = {
    "pbc": PBC_KEY,
    "label": "Energy Grid Operations",
    "mesh": "opsmfg",
    "description": "Standalone grid operations package for assets, topology, switching, dispatch, outages, reliability constraints, governance, and control-room evidence.",
    "datastore_backend": "postgresql",
    "tables": ENERGY_GRID_OPERATIONS_OWNED_TABLES,
    "apis": _API_CONTRACT["declared_catalog_routes"],
    "emits": ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
    "consumes": ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
    "template": "standalone_one_pbc_app",
    "ui_fragments": (
        "EnergyGridOperationsWorkbench",
        "EnergyGridOperationsSwitchingWorkbench",
        "EnergyGridOperationsOutageWorkbench",
        "EnergyGridOperationsGovernanceWorkbench",
        "EnergyGridOperationsAssistantPanel",
    ),
    "permissions": tuple(sorted(set(energy_grid_operations_permissions_contract()["permission_set"]))),
    "configuration": (
        "database_backend",
        "event_topic",
        "retry_limit",
        "default_policy_version",
        "simulation_depth",
        "storm_mode_enabled",
        "tenant_isolation",
    ),
    "capabilities": tuple(f"energy_grid_operations.{table.removeprefix('energy_grid_operations_')}" for table in ENERGY_GRID_OPERATIONS_OWNED_TABLES[:12]),
    "standard_features": ENERGY_GRID_OPERATIONS_STANDARD_FEATURE_KEYS,
    "workflows": tuple(
        operation
        for operation in _RUNTIME_CAPABILITIES["operations"]
        if operation not in {"set_parameter", "register_rule", "receive_event", "build_workbench_view", "query_timeline"}
    ),
    "analytics": (
        "feeder_risk_score",
        "switching_readiness",
        "dispatch_conflict_count",
        "restoration_priority",
        "constraint_pressure",
        "release_gate_coverage",
    ),
    "advanced_capabilities": _RUNTIME_CAPABILITIES["capabilities"],
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": (
        "tests/test_contract.py",
        "tests/test_standalone.py",
    ),
    "docs": (
        "SPECIFICATION.md",
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
        "RELEASE_EVIDENCE.md",
    ),
    "version": "2.0.0",
}
