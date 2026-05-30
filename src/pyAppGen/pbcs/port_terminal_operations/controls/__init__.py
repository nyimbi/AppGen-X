"""Control catalog for the Port Terminal Operations standalone PBC app."""

from __future__ import annotations

PBC_KEY = "port_terminal_operations"

PORT_TERMINAL_OPERATIONS_CONTROL_CONTRACTS = (
    {
        "key": "VesselCallBoardCards",
        "type": "cards",
        "binds_to": ("port_terminal_operations_vessel_call", "port_terminal_operations_berth_plan"),
    },
    {
        "key": "BerthWindowConflictControl",
        "type": "timeline",
        "binds_to": ("port_terminal_operations_berth_plan",),
    },
    {
        "key": "YardCongestionHeatmapControl",
        "type": "heatmap",
        "binds_to": (
            "port_terminal_operations_yard_slot",
            "port_terminal_operations_container_move",
        ),
    },
    {
        "key": "GateQueueControl",
        "type": "queue",
        "binds_to": ("port_terminal_operations_gate_transaction",),
    },
    {
        "key": "EquipmentHealthFallbackControl",
        "type": "equipment_status",
        "binds_to": ("port_terminal_operations_terminal_equipment",),
    },
    {
        "key": "CustomsHoldControl",
        "type": "hold_console",
        "binds_to": ("port_terminal_operations_customs_handoff",),
    },
    {
        "key": "ReleaseEvidenceConsole",
        "type": "audit_console",
        "binds_to": (
            "port_terminal_operations_port_terminal_operations_control_assertion",
            "port_terminal_operations_port_terminal_operations_governed_model",
            "port_terminal_operations_appgen_outbox_event",
            "port_terminal_operations_appgen_dead_letter_event",
        ),
    },
)

PORT_TERMINAL_OPERATIONS_CONTROL_KEYS = tuple(item["key"] for item in PORT_TERMINAL_OPERATIONS_CONTROL_CONTRACTS)


def port_terminal_operations_control_catalog() -> dict:
    return {
        "format": "appgen.port-terminal-operations-control-catalog.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": PORT_TERMINAL_OPERATIONS_CONTROL_CONTRACTS,
        "side_effects": (),
    }
