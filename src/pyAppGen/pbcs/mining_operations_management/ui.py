"""UI contract for the Mining Operations Management PBC."""

from __future__ import annotations

from .controls import mining_operations_management_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import mining_operations_management_form_catalog
from .routes import standalone_route_contracts
from .runtime import MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES
from .runtime import MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES
from .runtime import MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES
from .runtime import MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .wizards import mining_operations_management_wizard_catalog


PBC_KEY = "mining_operations_management"
MINING_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "MiningOperationsManagementWorkbench",
    "MiningOperationsManagementDetail",
    "MiningOperationsManagementAssistantPanel",
    "MiningOperationsManagementDispatchBoard",
    "MiningOperationsManagementBlastGate",
    "MiningOperationsManagementStockpileGenealogy",
    "MiningOperationsManagementGeotechRestrictionPanel",
    "MiningOperationsManagementShiftHandover",
)


def mining_operations_management_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    forms = mining_operations_management_form_catalog()
    wizards = mining_operations_management_wizard_catalog()
    controls = mining_operations_management_control_catalog()
    return {
        "format": "appgen.mining-operations-management-ui-contract.v1",
        "ok": surface["ok"] and forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/mining_operations_management",
        "fragments": MINING_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS,
        "forms": forms["form_ids"],
        "wizards": wizards["wizard_ids"],
        "controls": controls["control_ids"],
        "routes": (
            "/workbench/pbcs/mining_operations_management",
            "/workbench/pbcs/mining_operations_management/dispatch",
            "/workbench/pbcs/mining_operations_management/blast-gate",
            "/workbench/pbcs/mining_operations_management/stockpile",
            "/workbench/pbcs/mining_operations_management/geotech",
            "/workbench/pbcs/mining_operations_management/handover",
            "/workbench/pbcs/mining_operations_management/release-evidence",
        ),
        "action_permissions": {
            "create_mine_plan": "mining_operations_management.create",
            "record_pit_block": "mining_operations_management.update",
            "review_extraction_shift": "mining_operations_management.update",
            "approve_haulage_cycle": "mining_operations_management.approve",
            "simulate_fleet_asset": "mining_operations_management.update",
            "create_ore_quality": "mining_operations_management.approve",
            "record_stockpile": "mining_operations_management.update",
            "review_mining_operations_management_policy_rule": "mining_operations_management.approve",
            "create_mining_operations_management_control_assertion": "mining_operations_management.update",
            "build_release_evidence": "mining_operations_management.admin",
        },
        "configuration_editor": {
            "allowed_database_backends": MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "supported_parameters": DOMAIN_PARAMETERS,
            "bounded": True,
        },
        "rule_editor": {
            "supported_rules": DOMAIN_RULES,
            "explainable": True,
        },
        "event_surfaces": {
            "emits": MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES,
            "consumes": MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES,
            "shared_table_access": False,
        },
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "dispatch",
                "ore_control",
                "geotech",
                "handover",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def mining_operations_management_render_workbench(summary: dict | None = None) -> dict:
    contract = mining_operations_management_ui_contract()
    payload = dict(summary or {})
    cards = (
        {
            "key": "mine_plans",
            "value": payload.get("plan_count", 0),
            "fragment": "MiningOperationsManagementWorkbench",
        },
        {
            "key": "dispatch_assignments",
            "value": payload.get("dispatch_assignment_count", 0),
            "fragment": "MiningOperationsManagementDispatchBoard",
        },
        {
            "key": "pending_blast_clearance",
            "value": payload.get("pending_blast_clearance_count", 0),
            "fragment": "MiningOperationsManagementBlastGate",
        },
        {
            "key": "stockpile_delta",
            "value": payload.get("stockpile_tonnes_delta", 0.0),
            "fragment": "MiningOperationsManagementStockpileGenealogy",
        },
        {
            "key": "blocked_areas",
            "value": payload.get("blocked_area_count", 0),
            "fragment": "MiningOperationsManagementGeotechRestrictionPanel",
        },
        {
            "key": "open_handover",
            "value": payload.get("open_handover_count", 0),
            "fragment": "MiningOperationsManagementShiftHandover",
        },
    )
    return {
        "format": "appgen.mining-operations-management-workbench-render.v1",
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "tenant": payload.get("tenant", "default"),
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "cards": cards,
        "forms": mining_operations_management_form_catalog()["forms"],
        "wizards": mining_operations_management_wizard_catalog()["wizards"],
        "controls": mining_operations_management_control_catalog()["controls"],
        "binding_evidence": contract["binding_evidence"],
        "side_effects": (),
    }


def mining_operations_management_standalone_workbench_blueprint() -> dict:
    routes = standalone_route_contracts()
    forms = mining_operations_management_form_catalog()
    wizards = mining_operations_management_wizard_catalog()
    controls = mining_operations_management_control_catalog()
    return {
        "format": "appgen.mining-operations-management-standalone-workbench.v1",
        "ok": routes["ok"] and forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "route_manifest": routes["routes"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "side_effects": (),
    }


def mining_operations_management_render_standalone_workbench(summary: dict) -> dict:
    blueprint = mining_operations_management_standalone_workbench_blueprint()
    cards = (
        {
            "key": "plan_count",
            "value": summary.get("plan_count", 0),
            "control": "release_readiness",
        },
        {
            "key": "dispatch_assignment_count",
            "value": summary.get("dispatch_assignment_count", 0),
            "control": "dispatch_boundary_proof",
        },
        {
            "key": "pending_blast_clearance_count",
            "value": summary.get("pending_blast_clearance_count", 0),
            "control": "blast_clearance_gate",
        },
        {
            "key": "stockpile_tonnes_delta",
            "value": summary.get("stockpile_tonnes_delta", 0.0),
            "control": "stockpile_genealogy_integrity",
        },
    )
    return {
        "format": "appgen.mining-operations-management-standalone-workbench-render.v1",
        "ok": blueprint["ok"],
        "tenant": summary.get("tenant", "default"),
        "cards": cards,
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "route_manifest": blueprint["route_manifest"],
        "risk_flags": summary.get("risk_flags", ()),
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = mining_operations_management_ui_contract()
    rendered = mining_operations_management_render_workbench({"tenant": "tenant-smoke"})
    standalone = mining_operations_management_render_standalone_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": contract["ok"]
        and rendered["ok"]
        and standalone["ok"]
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls")),
        "contract": contract,
        "rendered": rendered,
        "standalone": standalone,
        "side_effects": (),
    }
