"""UI contract for the Port Terminal Operations PBC."""

from __future__ import annotations

from .controls import PORT_TERMINAL_OPERATIONS_CONTROL_KEYS
from .controls import port_terminal_operations_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import PORT_TERMINAL_OPERATIONS_FORM_KEYS
from .forms import port_terminal_operations_form_contracts
from .runtime import PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES
from .runtime import PORT_TERMINAL_OPERATIONS_EMITTED_EVENT_TYPES
from .runtime import PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC
from .runtime import port_terminal_operations_permissions_contract
from .wizards import PORT_TERMINAL_OPERATIONS_WIZARD_KEYS
from .wizards import port_terminal_operations_wizard_contracts

PBC_KEY = "port_terminal_operations"
PORT_TERMINAL_OPERATIONS_UI_FRAGMENT_KEYS = (
    "PortTerminalOperationsWorkbench",
    "PortTerminalOperationsDetail",
    "PortTerminalOperationsAssistantPanel",
    "PortTerminalOperationsRuleStudio",
    "PortTerminalOperationsParameterConsole",
    "PortTerminalOperationsReleaseEvidencePanel",
    "PortTerminalOperationsExceptionQueue",
)


ACTION_PERMISSIONS = {
    "create_vessel_call": "port_terminal_operations.create",
    "record_berth_plan": "port_terminal_operations.update",
    "review_container_move": "port_terminal_operations.update",
    "approve_yard_slot": "port_terminal_operations.approve",
    "simulate_gate_transaction": "port_terminal_operations.update",
    "create_terminal_equipment": "port_terminal_operations.create",
    "record_customs_handoff": "port_terminal_operations.update",
    "review_port_terminal_operations_policy_rule": "port_terminal_operations.admin",
    "approve_port_terminal_operations_runtime_parameter": "port_terminal_operations.admin",
    "simulate_port_terminal_operations_schema_extension": "port_terminal_operations.admin",
    "create_port_terminal_operations_control_assertion": "port_terminal_operations.approve",
    "record_port_terminal_operations_governed_model": "port_terminal_operations.admin",
    "receive_event": "port_terminal_operations.admin",
    "build_release_evidence": "port_terminal_operations.admin",
}


def port_terminal_operations_ui_contract() -> dict:
    forms = port_terminal_operations_form_contracts()
    wizards = port_terminal_operations_wizard_contracts()
    controls = port_terminal_operations_control_catalog()
    surface = domain_capability_surface_contract()
    permissions = port_terminal_operations_permissions_contract()
    return {
        "format": "appgen.port-terminal-operations-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and surface["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "fragments": PORT_TERMINAL_OPERATIONS_UI_FRAGMENT_KEYS,
        "forms": PORT_TERMINAL_OPERATIONS_FORM_KEYS,
        "wizards": PORT_TERMINAL_OPERATIONS_WIZARD_KEYS,
        "controls": PORT_TERMINAL_OPERATIONS_CONTROL_KEYS,
        "routes": (
            "/workbench/pbcs/port_terminal_operations",
            "/workbench/pbcs/port_terminal_operations/vessel-calls",
            "/workbench/pbcs/port_terminal_operations/berth-plans",
            "/workbench/pbcs/port_terminal_operations/container-moves",
            "/workbench/pbcs/port_terminal_operations/yard-slots",
            "/workbench/pbcs/port_terminal_operations/gate-transactions",
            "/workbench/pbcs/port_terminal_operations/equipment",
            "/workbench/pbcs/port_terminal_operations/customs",
            "/workbench/pbcs/port_terminal_operations/rules",
            "/workbench/pbcs/port_terminal_operations/parameters",
            "/workbench/pbcs/port_terminal_operations/release-evidence",
        ),
        "panels": (
            {
                "key": "vessel_berth_board",
                "fragment": "PortTerminalOperationsWorkbench",
                "binds_to": (
                    "port_terminal_operations_vessel_call",
                    "port_terminal_operations_berth_plan",
                ),
                "commands": ("create_vessel_call", "record_berth_plan"),
            },
            {
                "key": "container_yard_flow",
                "fragment": "PortTerminalOperationsDetail",
                "binds_to": (
                    "port_terminal_operations_container_move",
                    "port_terminal_operations_yard_slot",
                    "port_terminal_operations_gate_transaction",
                ),
                "commands": (
                    "review_container_move",
                    "approve_yard_slot",
                    "simulate_gate_transaction",
                ),
            },
            {
                "key": "equipment_customs",
                "fragment": "PortTerminalOperationsExceptionQueue",
                "binds_to": (
                    "port_terminal_operations_terminal_equipment",
                    "port_terminal_operations_customs_handoff",
                ),
                "commands": ("create_terminal_equipment", "record_customs_handoff"),
            },
            {
                "key": "governance",
                "fragment": "PortTerminalOperationsRuleStudio",
                "binds_to": (
                    "port_terminal_operations_port_terminal_operations_policy_rule",
                    "port_terminal_operations_port_terminal_operations_runtime_parameter",
                    "port_terminal_operations_port_terminal_operations_schema_extension",
                ),
                "commands": (
                    "review_port_terminal_operations_policy_rule",
                    "approve_port_terminal_operations_runtime_parameter",
                    "simulate_port_terminal_operations_schema_extension",
                ),
            },
            {
                "key": "release_evidence",
                "fragment": "PortTerminalOperationsReleaseEvidencePanel",
                "binds_to": (
                    "port_terminal_operations_port_terminal_operations_control_assertion",
                    "port_terminal_operations_port_terminal_operations_governed_model",
                    "port_terminal_operations_appgen_outbox_event",
                    "port_terminal_operations_appgen_dead_letter_event",
                ),
                "commands": (
                    "create_port_terminal_operations_control_assertion",
                    "record_port_terminal_operations_governed_model",
                    "build_release_evidence",
                ),
            },
        ),
        "action_permissions": ACTION_PERMISSIONS,
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_policy",
                "tenant_isolation",
                "workbench_limit",
            ),
            "allowed_database_backends": PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "fixed_event_topic": PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": DOMAIN_PARAMETERS,
            "supported_parameters": DOMAIN_PARAMETERS,
        },
        "rule_editor": {
            "rule_types": DOMAIN_RULES,
            "required_fields": ("rule_id", "scope", "status"),
        },
        "event_surfaces": {
            "emits": PORT_TERMINAL_OPERATIONS_EMITTED_EVENT_TYPES,
            "consumes": PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": DOMAIN_OWNED_TABLES,
            "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
            "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "permissions": permissions["permissions"],
            "shared_table_access": False,
        },
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "forms": forms["contracts"],
            "wizards": wizards["contracts"],
            "controls": controls["contracts"],
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def port_terminal_operations_render_workbench(
    summary: dict | None = None,
    *,
    tenant: str = "default",
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    contract = port_terminal_operations_ui_contract()
    data = dict(summary or {})
    active_tenant = data.get("tenant", tenant)
    granted = set(principal_permissions or tuple(dict.fromkeys(contract["action_permissions"].values())))
    visible_actions = tuple(
        action
        for action, permission in contract["action_permissions"].items()
        if permission in granted
    )
    cards = (
        {"key": "vessel_calls", "value": data.get("vessel_call_count", 0), "control": "VesselCallBoardCards"},
        {"key": "berth_plans", "value": data.get("berth_plan_count", 0), "control": "BerthWindowConflictControl"},
        {"key": "yard_slots", "value": data.get("yard_slot_count", 0), "control": "YardCongestionHeatmapControl"},
        {"key": "gate_queue", "value": data.get("gate_transaction_count", 0), "control": "GateQueueControl"},
        {"key": "equipment", "value": data.get("equipment_count", 0), "control": "EquipmentHealthFallbackControl"},
        {"key": "customs", "value": data.get("customs_handoff_count", 0), "control": "CustomsHoldControl"},
        {"key": "outbox", "value": data.get("outbox_count", 0), "control": "ReleaseEvidenceConsole"},
    )
    return {
        "format": "appgen.port-terminal-operations-workbench-render.v1",
        "ok": True,
        "tenant": active_tenant,
        "route": "/workbench/pbcs/port_terminal_operations",
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "forms": port_terminal_operations_form_contracts()["contracts"],
        "wizards": port_terminal_operations_wizard_contracts()["contracts"],
        "controls": port_terminal_operations_control_catalog()["contracts"],
        "binding_evidence": contract["binding_evidence"],
        "records": tuple(data.get("records", ())),
        "side_effects": (),
    }


def port_terminal_operations_standalone_workbench_blueprint() -> dict:
    from .standalone import port_terminal_operations_standalone_route_contracts

    routes = port_terminal_operations_standalone_route_contracts()
    forms = port_terminal_operations_form_contracts()
    wizards = port_terminal_operations_wizard_contracts()
    controls = port_terminal_operations_control_catalog()
    return {
        "format": "appgen.port-terminal-operations-standalone-workbench.v1",
        "ok": routes["ok"] and forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "route_manifest": routes,
        "forms": forms["contracts"],
        "wizards": wizards["contracts"],
        "controls": controls["contracts"],
        "side_effects": (),
    }


def port_terminal_operations_render_standalone_workbench(summary: dict) -> dict:
    blueprint = port_terminal_operations_standalone_workbench_blueprint()
    cards = (
        {"key": "vessel_calls", "value": summary.get("vessel_call_count", 0), "control": "VesselCallBoardCards"},
        {"key": "berth_conflicts", "value": summary.get("berth_plan_count", 0), "control": "BerthWindowConflictControl"},
        {"key": "container_flow", "value": summary.get("container_move_count", 0), "control": "YardCongestionHeatmapControl"},
        {"key": "gate_queue", "value": summary.get("gate_transaction_count", 0), "control": "GateQueueControl"},
        {"key": "release_evidence", "value": summary.get("outbox_count", 0), "control": "ReleaseEvidenceConsole"},
    )
    return {
        "format": "appgen.port-terminal-operations-standalone-workbench-render.v1",
        "ok": blueprint["ok"],
        "tenant": summary.get("tenant"),
        "cards": cards,
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "route_manifest": blueprint["route_manifest"]["routes"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = port_terminal_operations_ui_contract()
    rendered = port_terminal_operations_render_workbench({"tenant": "smoke"})
    standalone = port_terminal_operations_render_standalone_workbench({"tenant": "smoke"})
    return {
        "format": "appgen.port-terminal-operations-ui-smoke-test.v1",
        "ok": contract["ok"]
        and rendered["ok"]
        and standalone["ok"]
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and contract["configuration_editor"].get("stream_engine_picker_visible") is False,
        "contract": contract,
        "rendered": rendered,
        "standalone": standalone,
        "side_effects": (),
    }
