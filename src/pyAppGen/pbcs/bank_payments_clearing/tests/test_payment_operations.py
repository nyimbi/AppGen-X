"""Executable payment clearing tests for the bank_payments_clearing PBC."""

from .. import (
    bank_payments_clearing_assemble_clearing_batch,
    bank_payments_clearing_build_payment_operations_release_evidence,
    bank_payments_clearing_build_payment_operations_workbench,
    bank_payments_clearing_create_validated_payment_instruction,
    bank_payments_clearing_empty_operations_state,
    bank_payments_clearing_generate_settlement_file,
    bank_payments_clearing_handle_settlement_acknowledgement,
    bank_payments_clearing_process_return_item,
    bank_payments_clearing_reconcile_bank_statement,
    bank_payments_clearing_register_participant_bank,
    bank_payments_clearing_release_payment_instruction,
)
from .. import agent, release_evidence, services, ui


def test_payment_instruction_validation_duplicate_and_maker_checker_release():
    state = _participant_state()
    first = bank_payments_clearing_create_validated_payment_instruction(state, _instruction("pay_1", external_reference="EXT-1"))
    state = first["state"]
    duplicate = bank_payments_clearing_create_validated_payment_instruction(state, _instruction("pay_2", external_reference="EXT-1"))
    assert first["ok"] is True
    assert first["instruction"]["state"] == "validated"
    assert duplicate["ok"] is False
    assert duplicate["instruction"]["state"] == "repair_required"
    assert duplicate["duplicate_candidates"][0]["instruction_id"] == "pay_1"

    conflict = bank_payments_clearing_release_payment_instruction(
        state,
        "pay_1",
        maker="same_user",
        checker="same_user",
        liquidity={"available": 5000, "buffer": 250},
    )
    assert conflict["ok"] is False
    assert "maker_checker_conflict" in conflict["findings"]

    released = bank_payments_clearing_release_payment_instruction(
        state,
        "pay_1",
        maker="maker",
        checker="checker",
        liquidity={"available": 5000, "buffer": 250},
    )
    assert released["ok"] is True
    assert released["instruction"]["state"] == "released"


def test_batch_settlement_ack_return_and_reconciliation_flow():
    state = _participant_state()
    state = bank_payments_clearing_create_validated_payment_instruction(state, _instruction("pay_1", external_reference="EXT-1"))["state"]
    state = bank_payments_clearing_release_payment_instruction(
        state,
        "pay_1",
        maker="maker",
        checker="checker",
        liquidity={"available": 5000, "buffer": 250},
    )["state"]
    batch = bank_payments_clearing_assemble_clearing_batch(
        state,
        "batch_1",
        rail="ach",
        participant_bank_id="bank_a",
        cutoff_context={"missed_cutoff": False, "window": "same_day"},
    )
    state = batch["state"]
    settlement_file = bank_payments_clearing_generate_settlement_file(
        state,
        "file_1",
        "batch_1",
        sequence=7,
        channel="host_to_host",
    )
    state = settlement_file["state"]
    acknowledgement = bank_payments_clearing_handle_settlement_acknowledgement(
        state,
        {"acknowledgement_id": "ack_1", "file_id": "file_1", "accepted_count": 1, "rejected_count": 0},
    )
    state = acknowledgement["state"]
    returned = bank_payments_clearing_process_return_item(
        state,
        {"return_id": "return_1", "instruction_id": "pay_1", "reason_code": "closed_account"},
    )
    state = returned["state"]
    reconciliation = bank_payments_clearing_reconcile_bank_statement(
        state,
        "recon_1",
        (
            {"external_reference": "EXT-1", "amount": 1250.0},
            {"external_reference": "UNKNOWN", "amount": 50.0},
            {"line_type": "fee", "amount": 2.5},
        ),
    )
    workbench = bank_payments_clearing_build_payment_operations_workbench(reconciliation["state"])

    assert batch["ok"] is True
    assert batch["batch"]["finalization_lock"] is True
    assert settlement_file["settlement_file"]["signature"].startswith("appgen_payment_file_sig_")
    assert acknowledgement["acknowledgement"]["ack_type"] == "accepted"
    assert returned["return_item"]["repair_eligible"] is True
    assert reconciliation["ok"] is False
    assert reconciliation["reconciliation"]["fee_count"] == 1
    assert reconciliation["reconciliation"]["exception_count"] == 1
    assert workbench["ok"] is True
    assert workbench["stream_engine_picker_visible"] is False


def test_release_service_ui_and_agent_surfaces_include_payment_operations():
    evidence = bank_payments_clearing_build_payment_operations_release_evidence()
    release = release_evidence.build_release_evidence()
    service = services.service_operation_manifest()
    ui_contract = ui.bank_payments_clearing_ui_contract()
    app_contract = ui.bank_payments_clearing_single_pbc_app_contract()
    contribution = agent.composed_agent_contribution()

    required = {
        "register_participant_bank",
        "create_validated_payment_instruction",
        "release_payment_instruction",
        "assemble_clearing_batch",
        "generate_settlement_file",
        "handle_settlement_acknowledgement",
        "process_return_item",
        "reconcile_bank_statement",
    }
    assert evidence["ok"] is True
    assert release["ok"] is True
    assert {"payment_operations_execution", "single_pbc_app_forms_wizards_controls"} <= {
        check["id"] for check in release["checks"]
    }
    assert required <= set(service["payment_operations"])
    assert required <= set(ui_contract["payment_actions"])
    assert app_contract["ok"] is True
    assert app_contract["database_backing"]["owned_tables"]
    assert {form["form"] for form in app_contract["forms"]} >= {
        "PaymentInstructionForm",
        "ParticipantBankForm",
        "SettlementAcknowledgementForm",
        "ReturnItemForm",
        "BankReconciliationForm",
    }
    assert {wizard["wizard"] for wizard in app_contract["wizards"]} >= {
        "PaymentReleaseWizard",
        "ClearingBatchWizard",
        "ReturnAndReconciliationWizard",
    }
    assert {control["control"] for control in app_contract["controls"]} >= {
        "maker_checker_release",
        "settlement_file_integrity",
        "reconciliation_break_creation",
    }
    assert required <= set(contribution["execution_operations"])


def _participant_state():
    return bank_payments_clearing_register_participant_bank(
        bank_payments_clearing_empty_operations_state(),
        {
            "participant_bank_id": "bank_a",
            "routing_identifier": "021000021",
            "supported_rails": ("ach", "wire"),
            "status": "active",
        },
    )["state"]


def _instruction(instruction_id, *, external_reference):
    return {
        "instruction_id": instruction_id,
        "tenant": "tenant_a",
        "rail": "ach",
        "participant_bank_id": "bank_a",
        "amount": 1250.0,
        "currency": "USD",
        "beneficiary_account": "123456789",
        "beneficiary_name": "Supplier One",
        "originator_authorized": True,
        "external_reference": external_reference,
        "screening_evidence": {"decision": "clear", "freshness": "current"},
    }
