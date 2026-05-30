"""Service contract for the enterprise_risk_controls PBC."""

from __future__ import annotations

from .services import service_operation_contracts
from .services import service_operation_manifest


def build_service_contract():
    manifest = service_operation_manifest()
    return {
        "format": "appgen.enterprise-risk-controls-service-contract.v1",
        "ok": manifest["ok"],
        "pbc": "enterprise_risk_controls",
        "command_methods": manifest["command_operations"],
        "query_methods": manifest["query_operations"],
        "operations": manifest["operations"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "service_class": manifest["service_class"],
        "side_effects": (),
    }


def enterprise_risk_controls_build_service_contract():
    return build_service_contract()


def validate_service_contract():
    contract = build_service_contract()
    required_commands = {
        "register_risk",
        "assess_inherent_risk",
        "define_control",
        "schedule_control_test",
        "record_attestation",
        "open_remediation",
        "generate_assurance_packet",
    }
    required_queries = {
        "query_enterprise_risk_controls_workbench",
        "query_enterprise_risk_controls_controls",
        "query_enterprise_risk_controls_assistant_preview",
    }
    return {
        "ok": contract["ok"]
        and required_commands <= set(contract["command_methods"])
        and required_queries <= set(contract["query_methods"])
        and contract["shared_table_access"] is False,
        "contract": contract,
        "operation_contracts": service_operation_contracts(),
        "side_effects": (),
    }


def smoke_test():
    return validate_service_contract()
