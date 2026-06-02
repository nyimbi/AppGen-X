"""UI contract for the Global Inventory Visibility PBC."""

from __future__ import annotations

from .runtime import GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
from .runtime import GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
from .runtime import GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
from .runtime import global_inventory_visibility_permissions_contract


GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS = (
    "GlobalInventoryWorkbench",
    "InventoryPoolStudio",
    "SupplyNodeConsole",
    "AvailabilitySnapshotBoard",
    "GlobalAvailabilityConsole",
    "ProjectionLedgerView",
    "ReservationVisibilityPanel",
    "InTransitNetworkView",
    "FreshnessRiskPanel",
    "NodeHealthPanel",
    "PoolRuleStudio",
    "InventoryParameterConsole",
    "InventoryConfigurationPanel",
    "FederationEvidenceView",
    "DeadLetterAuditView",
)


def global_inventory_visibility_ui_contract() -> dict:
    return {
        "format": "appgen.global-inventory-visibility-ui-contract.v1",
        "ok": True,
        "pbc": "global_inventory_visibility",
        "implementation_directory": "src/pyAppGen/pbcs/global_inventory_visibility",
        "fragments": GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/global_inventory_visibility",
            "/workbench/pbcs/global_inventory_visibility/pools",
            "/workbench/pbcs/global_inventory_visibility/nodes",
            "/workbench/pbcs/global_inventory_visibility/snapshots",
            "/workbench/pbcs/global_inventory_visibility/projections",
            "/workbench/pbcs/global_inventory_visibility/reservations",
            "/workbench/pbcs/global_inventory_visibility/in-transit",
            "/workbench/pbcs/global_inventory_visibility/freshness",
            "/workbench/pbcs/global_inventory_visibility/rules",
            "/workbench/pbcs/global_inventory_visibility/parameters",
            "/workbench/pbcs/global_inventory_visibility/configuration",
            "/workbench/pbcs/global_inventory_visibility/audit",
        ),
        "panels": (
            {
                "key": "master_data",
                "fragment": "InventoryPoolStudio",
                "binds_to": ("inventory_pool", "supply_node", "identity"),
                "commands": (
                    "register_inventory_pool",
                    "register_supply_node",
                    "verify_supply_identity",
                ),
            },
            {
                "key": "projection",
                "fragment": "GlobalAvailabilityConsole",
                "binds_to": ("availability_snapshot", "inventory_projection", "in_transit"),
                "commands": (
                    "record_availability_snapshot",
                    "project_availability",
                    "get_global_availability",
                    "route_projection",
                ),
            },
            {
                "key": "execution",
                "fragment": "ReservationVisibilityPanel",
                "binds_to": ("reservation", "allocation", "inbox", "outbox"),
                "commands": (
                    "reserve_inventory",
                    "ingest_event",
                    "simulate_counterfactual_allocation",
                    "resolve_exception",
                ),
            },
            {
                "key": "governance",
                "fragment": "PoolRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": (
                    "register_rule",
                    "set_parameter",
                    "configure_runtime",
                    "run_control_tests",
                ),
            },
            {
                "key": "audit",
                "fragment": "DeadLetterAuditView",
                "binds_to": ("dead_letter", "proof", "governed_model"),
                "commands": (
                    "generate_availability_proof",
                    "register_governed_model",
                    "federate_inventory_view",
                ),
            },
        ),
        "action_permissions": global_inventory_visibility_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "projection_horizon_days",
                "staleness_sla_minutes",
                "workbench_limit",
            ),
            "allowed_database_backends": GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_facing_stream_engine_picker": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "safety_stock_percent",
                "freshness_half_life_hours",
                "availability_confidence_floor",
                "reservation_ttl_minutes",
                "projection_horizon_days",
                "stockout_risk_threshold",
                "staleness_sla_minutes",
                "carbon_cost_weight",
                "federation_lag_tolerance_minutes",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": (
                "allocation",
                "availability",
                "freshness",
                "reservation",
                "projection_route",
                "exception_resolution",
            ),
            "required_fields": ("rule_id", "tenant", "scope", "status", "rule_type"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES,
            "consumes": GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "event_contract": "AppGen-X",
            "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "user_facing_stream_engine_picker": False,
        },
        "binding_evidence": {
            "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
            "runtime_tables": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES,
            "outbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[0],
            "inbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[1],
            "dead_letter_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[2],
            "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "shared_table_access": False,
        },
    }


def global_inventory_visibility_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = global_inventory_visibility_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required in contract["action_permissions"].items()
        if required in permissions
    )
    pools = tuple(
        pool for pool in state["inventory_pools"].values() if pool["tenant"] == tenant
    )
    projections = tuple(
        projection
        for projection in state["inventory_projections"].values()
        if projection["tenant"] == tenant
    )
    cards = (
        {"key": "pools", "value": len(pools), "fragment": "InventoryPoolStudio"},
        {
            "key": "nodes",
            "value": len(tuple(node for node in state["supply_nodes"].values() if node["tenant"] == tenant)),
            "fragment": "SupplyNodeConsole",
        },
        {
            "key": "available_to_promise",
            "value": round(sum(projection["available_to_promise"] for projection in projections), 2),
            "fragment": "GlobalAvailabilityConsole",
        },
        {
            "key": "in_transit",
            "value": round(sum(projection["in_transit"] for projection in projections), 2),
            "fragment": "InTransitNetworkView",
        },
        {
            "key": "rules",
            "value": len(tuple(rule for rule in state["rules"].values() if rule["tenant"] == tenant)),
            "fragment": "PoolRuleStudio",
        },
        {
            "key": "dead_letters",
            "value": len(state.get("dead_letters", ())),
            "fragment": "DeadLetterAuditView",
        },
    )
    return {
        "format": "appgen.global-inventory-visibility-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/global_inventory_visibility",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in contract["action_permissions"] if action not in visible_actions
        ),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(
            sorted(rule_id for rule_id, rule in state.get("rules", {}).items() if rule["tenant"] == tenant)
        ),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "binding_evidence": {
            "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
            "runtime_tables": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES,
            "outbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[0],
            "inbox_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[1],
            "dead_letter_table": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES[2],
            "configuration": state.get("configuration", {}).get("event_topic"),
            "configuration_state": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "rule_hashes": tuple(
                sorted(
                    rule["compiled_hash"]
                    for rule in state.get("rules", {}).values()
                    if rule["tenant"] == tenant
                )
            ),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "ui_bindings": {
                "configuration_fragment": "InventoryConfigurationPanel",
                "rule_fragment": "PoolRuleStudio",
                "parameter_fragment": "InventoryParameterConsole",
                "workbench_fragment": "GlobalInventoryWorkbench",
                "rbac": contract["action_permissions"],
            },
        },
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letters", ())),
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = global_inventory_visibility_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = global_inventory_visibility_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }



def global_inventory_visibility_form_contracts() -> dict:
    """Return package-local forms for the standalone inventory workbench."""
    contracts = (
        {
            "key": "InventoryConfigurationForm",
            "title": "Inventory configuration",
            "operation": "configure_runtime",
            "table": "global_inventory_visibility_inventory_configuration",
            "fields": ("database_backend", "event_topic", "retry_limit", "projection_horizon_days", "staleness_sla_minutes", "workbench_limit"),
            "permission": "global_inventory_visibility.configure",
            "keywords": ("configure", "backend", "event topic", "runtime"),
        },
        {
            "key": "SupplyNodeForm",
            "title": "Supply node",
            "operation": "register_supply_node",
            "table": "global_inventory_visibility_supply_node",
            "fields": ("node_id", "tenant", "node_type", "country", "region", "health_score", "latency_ms", "carbon_intensity", "identity"),
            "permission": "global_inventory_visibility.configure",
            "keywords": ("node", "warehouse", "port", "identity"),
        },
        {
            "key": "InventoryPoolForm",
            "title": "Inventory pool",
            "operation": "register_inventory_pool",
            "table": "global_inventory_visibility_inventory_pool",
            "fields": ("pool_id", "tenant", "item_id", "pool_type", "node_ids", "allocation_policy", "safety_stock_units"),
            "permission": "global_inventory_visibility.configure",
            "keywords": ("pool", "sku", "allocation", "safety stock"),
        },
        {
            "key": "AvailabilitySnapshotForm",
            "title": "Availability snapshot",
            "operation": "record_availability_snapshot",
            "table": "global_inventory_visibility_availability_snapshot",
            "fields": ("snapshot_id", "tenant", "pool_id", "node_id", "on_hand", "reserved", "allocated", "in_transit", "safety_stock", "freshness_age_hours", "staleness_minutes"),
            "permission": "global_inventory_visibility.configure",
            "keywords": ("snapshot", "on hand", "in transit", "freshness"),
        },
        {
            "key": "ReservationForm",
            "title": "Inventory reservation",
            "operation": "reserve_inventory",
            "table": "global_inventory_visibility_inventory_reservation",
            "fields": ("reservation_id", "tenant", "pool_id", "order_id", "quantity", "channel"),
            "permission": "global_inventory_visibility.reserve",
            "keywords": ("reserve", "reservation", "order", "channel"),
        },
        {
            "key": "InventoryEventInboxForm",
            "title": "Inventory event intake",
            "operation": "receive_event",
            "table": "global_inventory_visibility_appgen_inbox_event",
            "fields": ("event_id", "event_type", "tenant", "pool_id", "node_id", "quantity"),
            "permission": "global_inventory_visibility.configure",
            "keywords": ("event", "receipt", "shipment", "allocation"),
        },
    )
    return {
        "format": "appgen.global-inventory-visibility-standalone-forms.v1",
        "ok": all(item["table"].startswith("global_inventory_visibility_") for item in contracts),
        "pbc": "global_inventory_visibility",
        "contracts": contracts,
        "side_effects": (),
    }


def global_inventory_visibility_wizard_contracts() -> dict:
    """Return guided workflows for a one-PBC inventory visibility app."""
    contracts = (
        {
            "key": "InventoryInstructionIntakeWizard",
            "title": "Document and instruction intake",
            "steps": ("classify_inventory_document", "extract_pool_node_snapshot_fields", "preview_crud_plan", "require_confirmation"),
            "forms": ("InventoryPoolForm", "SupplyNodeForm", "AvailabilitySnapshotForm", "InventoryEventInboxForm"),
            "keywords": ("document", "instruction", "asn", "handoff", "spreadsheet", "inventory file"),
        },
        {
            "key": "AvailabilityProjectionWizard",
            "title": "Global availability projection",
            "steps": ("validate_configuration", "capture_supply_nodes", "capture_pool", "record_snapshots", "refresh_projection", "publish_appgen_event"),
            "forms": ("InventoryConfigurationForm", "SupplyNodeForm", "InventoryPoolForm", "AvailabilitySnapshotForm"),
            "keywords": ("availability", "projection", "atp", "ctp", "freshness"),
        },
        {
            "key": "ReservationControlWizard",
            "title": "Reservation and control workflow",
            "steps": ("read_latest_projection", "screen_reservation", "create_reservation", "refresh_projection", "run_control_tests"),
            "forms": ("ReservationForm",),
            "keywords": ("reservation", "reserve", "promise", "channel"),
        },
    )
    return {
        "format": "appgen.global-inventory-visibility-standalone-wizards.v1",
        "ok": all(item["steps"] for item in contracts),
        "pbc": "global_inventory_visibility",
        "contracts": contracts,
        "side_effects": (),
    }


def global_inventory_visibility_control_catalog() -> dict:
    """Return executable controls surfaced by the standalone workbench."""
    contracts = (
        {
            "key": "backend_event_contract_allowlist",
            "title": "Backend and AppGen-X event contract",
            "operation": "build_release_read_model",
            "table": "global_inventory_visibility_inventory_control_assertion",
            "permission": "global_inventory_visibility.audit",
        },
        {
            "key": "freshness_sla_control",
            "title": "Freshness SLA and stale snapshot control",
            "operation": "build_release_read_model",
            "table": "global_inventory_visibility_inventory_control_assertion",
            "permission": "global_inventory_visibility.audit",
        },
        {
            "key": "owned_boundary_control",
            "title": "Owned datastore boundary",
            "operation": "build_release_read_model",
            "table": "global_inventory_visibility_inventory_control_assertion",
            "permission": "global_inventory_visibility.audit",
        },
    )
    return {
        "format": "appgen.global-inventory-visibility-standalone-controls.v1",
        "ok": all(item["table"].startswith("global_inventory_visibility_") for item in contracts),
        "pbc": "global_inventory_visibility",
        "contracts": contracts,
        "side_effects": (),
    }


def global_inventory_visibility_standalone_workbench_blueprint() -> dict:
    """Return the standalone UI blueprint with forms, wizards, controls, and panels."""
    forms = global_inventory_visibility_form_contracts()
    wizards = global_inventory_visibility_wizard_contracts()
    controls = global_inventory_visibility_control_catalog()
    base_contract = global_inventory_visibility_ui_contract()
    return {
        "format": "appgen.global-inventory-visibility-standalone-workbench.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and base_contract["ok"],
        "pbc": "global_inventory_visibility",
        "forms": forms["contracts"],
        "wizards": wizards["contracts"],
        "controls": controls["contracts"],
        "panels": base_contract["panels"],
        "routes": base_contract["routes"],
        "side_effects": (),
    }


def global_inventory_visibility_render_standalone_workbench(workbench: dict) -> dict:
    """Render a repository read model into deterministic workbench sections."""
    blueprint = global_inventory_visibility_standalone_workbench_blueprint()
    cards = (
        {"key": "pools", "value": workbench.get("pool_count", 0), "fragment": "InventoryPoolStudio"},
        {"key": "nodes", "value": workbench.get("node_count", 0), "fragment": "SupplyNodeConsole"},
        {"key": "available_to_promise", "value": workbench.get("available_to_promise", 0), "fragment": "GlobalAvailabilityConsole"},
        {"key": "freshness_alerts", "value": workbench.get("freshness_alert_count", 0), "fragment": "FreshnessRiskPanel"},
        {"key": "control_failures", "value": workbench.get("release_control_failure_count", 0), "fragment": "DeadLetterAuditView"},
    )
    return {
        "format": "appgen.global-inventory-visibility-standalone-render.v1",
        "ok": blueprint["ok"] and bool(cards),
        "pbc": "global_inventory_visibility",
        "tenant": workbench.get("tenant"),
        "cards": cards,
        "forms": tuple(item["key"] for item in blueprint["forms"]),
        "wizards": tuple(item["key"] for item in blueprint["wizards"]),
        "controls": tuple(item["key"] for item in blueprint["controls"]),
        "pool_read_models": workbench.get("pool_read_models", ()),
        "side_effects": (),
    }
