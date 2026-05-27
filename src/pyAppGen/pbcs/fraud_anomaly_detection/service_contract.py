"""Generated service evidence for the fraud_anomaly_detection PBC."""

from __future__ import annotations

from .runtime import fraud_anomaly_detection_build_service_contract

SERVICE_CONTRACT = fraud_anomaly_detection_build_service_contract()


def build_service_contract():
    """Return generated command, eventing, and handler evidence."""
    return dict(SERVICE_CONTRACT)


def validate_service_contract():
    contract = build_service_contract()
    return {
        "ok": contract["ok"]
        and contract["shared_table_access"] is False
        and "receive_event" in contract["idempotent_handlers"]
        and {"link_identity", "project_loss_exposure", "enqueue_analyst_case"} <= set(contract["command_methods"]),
        "contract": contract,
        "side_effects": (),
    }


def smoke_test():
    return validate_service_contract()
