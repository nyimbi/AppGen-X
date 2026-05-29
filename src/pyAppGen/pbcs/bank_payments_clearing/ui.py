"""UI contracts for the standalone bank_payments_clearing package."""

from __future__ import annotations

from .payment_operations import build_payment_operations_workbench, empty_operations_state
from .permissions import permission_manifest
from .runtime import BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS


PBC_KEY = "bank_payments_clearing"
PAYMENT_FORMS = (
    {
        "form": "PaymentInstructionForm",
        "route": "/payment-instructions",
        "owned_table": "bank_payments_clearing_payment_instruction",
        "fields": (
            "instruction_id",
            "tenant",
            "rail",
            "participant_bank_id",
            "amount",
            "currency",
            "beneficiary_account",
            "beneficiary_name",
            "originator_authorized",
            "external_reference",
            "screening_evidence",
        ),
        "submit_action": "create_validated_payment_instruction",
        "validation_controls": (
            "rail_profile_validation",
            "participant_bank_capability",
            "screening_freshness",
            "duplicate_payment_prevention",
        ),
    },
    {
        "form": "ParticipantBankForm",
        "route": "/participant-banks",
        "owned_table": "bank_payments_clearing_participant_bank",
        "fields": (
            "participant_bank_id",
            "routing_identifier",
            "supported_rails",
            "active_windows",
            "status",
        ),
        "submit_action": "register_participant_bank",
        "validation_controls": (
            "routing_identifier_required",
            "supported_rail_required",
            "active_status_required",
        ),
    },
    {
        "form": "SettlementAcknowledgementForm",
        "route": "/settlement-acknowledgements",
        "owned_table": "bank_payments_clearing_settlement_file",
        "fields": ("acknowledgement_id", "file_id", "accepted_count", "rejected_count", "reason"),
        "submit_action": "handle_settlement_acknowledgement",
        "validation_controls": (
            "file_exists",
            "accepted_rejected_count_consistency",
            "acknowledgement_idempotency",
        ),
    },
    {
        "form": "ReturnItemForm",
        "route": "/return-items",
        "owned_table": "bank_payments_clearing_return_item",
        "fields": ("return_id", "instruction_id", "reason_code", "effective_date", "received_at"),
        "submit_action": "process_return_item",
        "validation_controls": (
            "return_reason_deadline",
            "original_instruction_required",
            "notification_required",
        ),
    },
    {
        "form": "BankReconciliationForm",
        "route": "/reconciliations",
        "owned_table": "bank_payments_clearing_bank_reconciliation",
        "fields": ("reconciliation_id", "statement_lines", "tolerance", "statement_source"),
        "submit_action": "reconcile_bank_statement",
        "validation_controls": (
            "statement_line_shape",
            "fee_classification",
            "reconciliation_break_creation",
        ),
    },
    {
        "form": "DocumentInstructionForm",
        "route": "/assistant/document-instructions",
        "owned_table": "bank_payments_clearing_bank_payments_clearing_governed_model",
        "fields": ("document", "instruction"),
        "submit_action": "document_instruction_plan",
        "validation_controls": ("mutation_preview", "owned_table_boundary", "human_confirmation_required"),
    },
)
PAYMENT_WIZARDS = (
    {
        "wizard": "PaymentReleaseWizard",
        "steps": (
            "select_validated_instruction",
            "review_validation_and_screening",
            "confirm_maker_checker_separation",
            "attach_liquidity_evidence",
            "release_or_route_exception",
        ),
        "commands": ("release_payment_instruction",),
        "controls": ("maker_checker_release", "liquidity_buffer_check", "screening_freshness"),
    },
    {
        "wizard": "ClearingBatchWizard",
        "steps": (
            "select_rail_and_participant",
            "review_cutoff_window",
            "preview_batch_totals",
            "finalize_batch_lock",
            "generate_settlement_file",
        ),
        "commands": ("assemble_clearing_batch", "generate_settlement_file"),
        "controls": ("cutoff_calendar", "hash_total", "finalization_lock"),
    },
    {
        "wizard": "ReturnAndReconciliationWizard",
        "steps": (
            "capture_return_or_statement",
            "classify_reason_or_match_type",
            "open_breaks_for_unmatched_lines",
            "prepare_repair_or_reversal",
            "record_operator_evidence",
        ),
        "commands": ("process_return_item", "reconcile_bank_statement"),
        "controls": ("return_reason_profile", "fee_classification", "exception_evidence_required"),
    },
    {
        "wizard": "AssistantInstructionWizard",
        "steps": (
            "capture_document_or_chat_instruction",
            "extract_candidate_mutations",
            "review_permission_and_route_preview",
            "require_human_confirmation",
        ),
        "commands": ("document_instruction_plan", "datastore_crud_plan"),
        "controls": ("document_instruction_preview", "permission_gate", "release_evidence_gate"),
    },
)
PAYMENT_CONTROLS = (
    {"control": "rail_profile_validation", "enforced_by": "create_validated_payment_instruction"},
    {"control": "participant_bank_capability", "enforced_by": "create_validated_payment_instruction"},
    {"control": "duplicate_payment_prevention", "enforced_by": "create_validated_payment_instruction"},
    {"control": "maker_checker_release", "enforced_by": "release_payment_instruction"},
    {"control": "liquidity_buffer_check", "enforced_by": "release_payment_instruction"},
    {"control": "settlement_file_integrity", "enforced_by": "generate_settlement_file"},
    {"control": "acknowledgement_idempotency", "enforced_by": "handle_settlement_acknowledgement"},
    {"control": "return_reason_deadline", "enforced_by": "process_return_item"},
    {"control": "reconciliation_break_creation", "enforced_by": "reconcile_bank_statement"},
    {"control": "document_instruction_preview", "enforced_by": "document_instruction_plan"},
    {"control": "permission_gate", "enforced_by": "datastore_crud_plan"},
    {"control": "release_evidence_gate", "enforced_by": "release_snapshot"},
)
PAYMENT_WORKFLOWS = (
    {
        "workflow": "instruction_intake_to_release",
        "steps": (
            "register_participant_bank",
            "create_validated_payment_instruction",
            "release_payment_instruction",
        ),
    },
    {
        "workflow": "batch_settlement_to_acknowledgement",
        "steps": (
            "assemble_clearing_batch",
            "generate_settlement_file",
            "handle_settlement_acknowledgement",
        ),
    },
    {
        "workflow": "return_to_reconciliation",
        "steps": ("process_return_item", "reconcile_bank_statement"),
    },
    {
        "workflow": "assistant_document_to_crud_preview",
        "steps": ("document_instruction_plan", "datastore_crud_plan"),
    },
)


def bank_payments_clearing_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_id": "bank_payments_clearing_one_pbc_app",
        "workbench_route": "/bank-payments-clearing-workbench",
        "release_route": "/bank-payments-clearing-release-evidence",
        "navigation": (
            {"key": "workbench", "route": "/bank-payments-clearing-workbench"},
            {"key": "payment_release", "route": "/payment-instructions/release"},
            {"key": "clearing_batches", "route": "/clearing-batches"},
            {"key": "settlement_files", "route": "/settlement-files"},
            {"key": "returns_reconciliation", "route": "/reconciliations"},
            {"key": "assistant", "route": "/assistant/document-instructions"},
        ),
        "forms": PAYMENT_FORMS,
        "wizards": PAYMENT_WIZARDS,
        "controls": PAYMENT_CONTROLS,
        "workflows": PAYMENT_WORKFLOWS,
        "database_backing": {
            "owned_tables": tuple(item["owned_table"] for item in PAYMENT_FORMS),
            "migration": "migrations/001_initial.sql",
            "models_module": "models.py",
            "schema_contract_module": "schema_contract.py",
            "database_backends": BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS,
        },
        "single_agent_namespace": "bank_payments_clearing_skills",
        "assistant_panel": "BankPaymentsClearingAssistantPanel",
        "side_effects": (),
    }


def bank_payments_clearing_ui_contract() -> dict:
    permissions = permission_manifest()
    payment_actions = (
        "register_participant_bank",
        "create_validated_payment_instruction",
        "release_payment_instruction",
        "assemble_clearing_batch",
        "generate_settlement_file",
        "handle_settlement_acknowledgement",
        "process_return_item",
        "reconcile_bank_statement",
    )
    return {
        "format": "appgen.bank-payments-clearing-ui-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "BankPaymentsClearingWorkbench",
            "BankPaymentsClearingDetail",
            "BankPaymentsClearingAssistantPanel",
            "PaymentInstructionReleaseConsole",
            "ClearingBatchAssemblyBoard",
            "SettlementFileIntegrityPanel",
            "ReturnAndReconciliationWorkbench",
        ),
        "forms": PAYMENT_FORMS,
        "wizards": PAYMENT_WIZARDS,
        "controls": PAYMENT_CONTROLS,
        "workflows": PAYMENT_WORKFLOWS,
        "payment_actions": payment_actions,
        "action_permissions": permissions["permissions"],
        "standalone_app": bank_payments_clearing_standalone_app_contract(),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def bank_payments_clearing_render_workbench(state: dict | None = None) -> dict:
    state = state or empty_operations_state()
    base = build_payment_operations_workbench(state)
    app = bank_payments_clearing_standalone_app_contract()
    return {
        "ok": base["ok"] and app["ok"],
        "pbc": PBC_KEY,
        "route": app["workbench_route"],
        "cards": base["cards"],
        "queues": base["queues"],
        "forms": app["forms"],
        "wizards": app["wizards"],
        "controls": app["controls"],
        "workflows": app["workflows"],
        "navigation": app["navigation"],
        "assistant_panel": app["assistant_panel"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def bank_payments_clearing_single_pbc_app_contract() -> dict:
    app = bank_payments_clearing_standalone_app_contract()
    return {
        "ok": app["ok"],
        "pbc": PBC_KEY,
        "database_backing": app["database_backing"],
        "forms": app["forms"],
        "wizards": app["wizards"],
        "controls": app["controls"],
        "workflows": app["workflows"],
        "workbench_route": app["workbench_route"],
        "agent_panel": app["assistant_panel"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def smoke_test() -> dict:
    app = bank_payments_clearing_standalone_app_contract()
    workbench = bank_payments_clearing_render_workbench()
    return {
        "ok": bank_payments_clearing_ui_contract()["ok"] and app["ok"] and workbench["ok"],
        "single_pbc_app": app,
        "side_effects": (),
    }
