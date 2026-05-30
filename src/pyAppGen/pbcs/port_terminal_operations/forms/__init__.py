"""Form contracts for the Port Terminal Operations standalone PBC app."""

from __future__ import annotations

PBC_KEY = "port_terminal_operations"

PORT_TERMINAL_OPERATIONS_FORM_CONTRACTS = (
    {
        "key": "PortTerminalVesselCallForm",
        "table": "port_terminal_operations_vessel_call",
        "operation": "create_vessel_call",
        "fields": (
            "record_id",
            "tenant",
            "vessel_code",
            "service_lane",
            "eta",
            "confidence_band",
            "berth_preference",
            "revision_reason",
        ),
    },
    {
        "key": "PortTerminalBerthPlanForm",
        "table": "port_terminal_operations_berth_plan",
        "operation": "record_berth_plan",
        "fields": (
            "record_id",
            "tenant",
            "vessel_code",
            "berth_id",
            "window_start",
            "window_end",
            "tide_window",
            "crane_plan",
        ),
    },
    {
        "key": "PortTerminalContainerMoveForm",
        "table": "port_terminal_operations_container_move",
        "operation": "review_container_move",
        "fields": (
            "record_id",
            "tenant",
            "container_id",
            "move_kind",
            "source_location",
            "target_location",
            "priority",
            "exception_reason",
        ),
    },
    {
        "key": "PortTerminalYardSlotForm",
        "table": "port_terminal_operations_yard_slot",
        "operation": "approve_yard_slot",
        "fields": (
            "record_id",
            "tenant",
            "slot_code",
            "flow_type",
            "capacity_class",
            "reserved_capacity",
            "rehandle_risk_score",
        ),
    },
    {
        "key": "PortTerminalGateTransactionForm",
        "table": "port_terminal_operations_gate_transaction",
        "operation": "simulate_gate_transaction",
        "fields": (
            "record_id",
            "tenant",
            "transaction_id",
            "appointment_window",
            "truck_id",
            "driver_id",
            "hold_status",
            "direction",
        ),
    },
    {
        "key": "PortTerminalEquipmentDispatchForm",
        "table": "port_terminal_operations_terminal_equipment",
        "operation": "create_terminal_equipment",
        "fields": (
            "record_id",
            "tenant",
            "equipment_id",
            "equipment_type",
            "operating_state",
            "fallback_pool",
            "battery_or_fuel_state",
        ),
    },
    {
        "key": "PortTerminalCustomsHandoffForm",
        "table": "port_terminal_operations_customs_handoff",
        "operation": "record_customs_handoff",
        "fields": (
            "record_id",
            "tenant",
            "container_id",
            "release_state",
            "inspection_requirement",
            "scan_result",
            "expiry_timestamp",
        ),
    },
    {
        "key": "PortTerminalPolicyRuleForm",
        "table": "port_terminal_operations_port_terminal_operations_policy_rule",
        "operation": "review_port_terminal_operations_policy_rule",
        "fields": (
            "record_id",
            "tenant",
            "rule_id",
            "scope",
            "precedence",
            "status",
            "compiled_reasoning",
        ),
    },
    {
        "key": "PortTerminalRuntimeParameterForm",
        "table": "port_terminal_operations_port_terminal_operations_runtime_parameter",
        "operation": "approve_port_terminal_operations_runtime_parameter",
        "fields": (
            "record_id",
            "tenant",
            "parameter_name",
            "parameter_value",
            "effective_from",
            "reviewed_by",
        ),
    },
    {
        "key": "PortTerminalSchemaExtensionForm",
        "table": "port_terminal_operations_port_terminal_operations_schema_extension",
        "operation": "simulate_port_terminal_operations_schema_extension",
        "fields": (
            "record_id",
            "tenant",
            "target_table",
            "field_name",
            "field_type",
            "compatibility_expectation",
        ),
    },
    {
        "key": "PortTerminalControlAssertionForm",
        "table": "port_terminal_operations_port_terminal_operations_control_assertion",
        "operation": "create_port_terminal_operations_control_assertion",
        "fields": (
            "record_id",
            "tenant",
            "assertion_id",
            "control_family",
            "expected_result",
            "evidence_reference",
        ),
    },
    {
        "key": "PortTerminalGovernedModelForm",
        "table": "port_terminal_operations_port_terminal_operations_governed_model",
        "operation": "record_port_terminal_operations_governed_model",
        "fields": (
            "record_id",
            "tenant",
            "model_name",
            "model_version",
            "usage_scope",
            "approval_status",
            "evidence_hash",
        ),
    },
    {
        "key": "PortTerminalEventInboxForm",
        "table": "port_terminal_operations_appgen_inbox_event",
        "operation": "receive_event",
        "fields": ("event_id", "event_type", "payload", "idempotency_key"),
    },
)

PORT_TERMINAL_OPERATIONS_FORM_KEYS = tuple(item["key"] for item in PORT_TERMINAL_OPERATIONS_FORM_CONTRACTS)


def port_terminal_operations_form_contracts() -> dict:
    return {
        "format": "appgen.port-terminal-operations-form-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": PORT_TERMINAL_OPERATIONS_FORM_CONTRACTS,
        "side_effects": (),
    }
