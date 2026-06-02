"""Wizard contracts for the Port Terminal Operations standalone PBC app."""

from __future__ import annotations

PBC_KEY = "port_terminal_operations"

PORT_TERMINAL_OPERATIONS_WIZARD_CONTRACTS = (
    {
        "key": "VesselArrivalNominationWizard",
        "steps": ("eta_intake", "confidence_review", "berth_nomination", "readiness_gate"),
        "forms": ("PortTerminalVesselCallForm", "PortTerminalBerthPlanForm"),
        "keywords": ("vessel", "eta", "arrival", "berth", "nomination"),
    },
    {
        "key": "ContainerFlowExceptionWizard",
        "steps": ("move_review", "yard_slot", "customs_release", "gate_resolution"),
        "forms": (
            "PortTerminalContainerMoveForm",
            "PortTerminalYardSlotForm",
            "PortTerminalCustomsHandoffForm",
            "PortTerminalGateTransactionForm",
        ),
        "keywords": ("container", "move", "yard", "customs", "gate", "exception"),
    },
    {
        "key": "EquipmentFallbackDispatchWizard",
        "steps": ("equipment_health", "fallback_assignment", "berth_replan"),
        "forms": (
            "PortTerminalEquipmentDispatchForm",
            "PortTerminalBerthPlanForm",
            "PortTerminalContainerMoveForm",
        ),
        "keywords": ("equipment", "outage", "fallback", "dispatch", "crane"),
    },
    {
        "key": "DocumentInstructionIntakeWizard",
        "steps": ("document_review", "field_extraction", "crud_preview", "human_confirmation"),
        "forms": (
            "PortTerminalEventInboxForm",
            "PortTerminalPolicyRuleForm",
            "PortTerminalRuntimeParameterForm",
        ),
        "keywords": ("document", "instruction", "crud", "preview", "policy"),
    },
    {
        "key": "ReleaseReadinessWizard",
        "steps": ("control_assertion", "governed_model", "release_evidence", "signoff"),
        "forms": (
            "PortTerminalControlAssertionForm",
            "PortTerminalGovernedModelForm",
            "PortTerminalSchemaExtensionForm",
        ),
        "keywords": ("release", "evidence", "control", "model", "signoff"),
    },
)

PORT_TERMINAL_OPERATIONS_WIZARD_KEYS = tuple(item["key"] for item in PORT_TERMINAL_OPERATIONS_WIZARD_CONTRACTS)


def port_terminal_operations_wizard_contracts() -> dict:
    return {
        "format": "appgen.port-terminal-operations-wizard-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": PORT_TERMINAL_OPERATIONS_WIZARD_CONTRACTS,
        "side_effects": (),
    }
