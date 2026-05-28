from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'bank_payments_clearing'

PAYMENT_FORMS = (
    {
        'form': 'PaymentInstructionForm',
        'route': '/workbench/pbcs/bank_payments_clearing/payment-instructions/new',
        'owned_table': 'bank_payments_clearing_payment_instruction',
        'fields': (
            'instruction_id',
            'tenant',
            'rail',
            'participant_bank_id',
            'amount',
            'currency',
            'beneficiary_account',
            'beneficiary_name',
            'originator_authorized',
            'external_reference',
            'screening_evidence',
        ),
        'submit_action': 'create_validated_payment_instruction',
        'validation_controls': ('rail_limit', 'participant_bank_support', 'screening_freshness', 'duplicate_detection'),
    },
    {
        'form': 'ParticipantBankForm',
        'route': '/workbench/pbcs/bank_payments_clearing/participant-banks/new',
        'owned_table': 'bank_payments_clearing_participant_bank',
        'fields': ('participant_bank_id', 'routing_identifier', 'supported_rails', 'active_windows', 'status'),
        'submit_action': 'register_participant_bank',
        'validation_controls': ('routing_identifier_required', 'supported_rail_required', 'active_status_required'),
    },
    {
        'form': 'SettlementAcknowledgementForm',
        'route': '/workbench/pbcs/bank_payments_clearing/settlement-acknowledgements/new',
        'owned_table': 'bank_payments_clearing_settlement_file',
        'fields': ('acknowledgement_id', 'file_id', 'accepted_count', 'rejected_count', 'reason'),
        'submit_action': 'handle_settlement_acknowledgement',
        'validation_controls': ('file_exists', 'accepted_rejected_count_consistency', 'duplicate_acknowledgement_guard'),
    },
    {
        'form': 'ReturnItemForm',
        'route': '/workbench/pbcs/bank_payments_clearing/returns/new',
        'owned_table': 'bank_payments_clearing_return_item',
        'fields': ('return_id', 'instruction_id', 'reason_code', 'effective_date', 'received_at'),
        'submit_action': 'process_return_item',
        'validation_controls': ('reason_code_profile', 'return_deadline', 'original_instruction_required'),
    },
    {
        'form': 'BankReconciliationForm',
        'route': '/workbench/pbcs/bank_payments_clearing/reconciliations/new',
        'owned_table': 'bank_payments_clearing_bank_reconciliation',
        'fields': ('reconciliation_id', 'statement_lines', 'tolerance', 'statement_source'),
        'submit_action': 'reconcile_bank_statement',
        'validation_controls': ('statement_line_shape', 'fee_line_classification', 'unmatched_break_creation'),
    },
)

PAYMENT_WIZARDS = (
    {
        'wizard': 'PaymentReleaseWizard',
        'steps': (
            'select_validated_instruction',
            'review_validation_and_screening',
            'confirm_maker_checker_separation',
            'attach_liquidity_evidence',
            'release_or_route_exception',
        ),
        'commands': ('release_payment_instruction',),
        'controls': ('maker_checker', 'liquidity_buffer', 'screening_freshness'),
    },
    {
        'wizard': 'ClearingBatchWizard',
        'steps': (
            'select_rail_and_participant',
            'review_cutoff_window',
            'preview_batch_totals',
            'finalize_batch_lock',
            'generate_settlement_file',
        ),
        'commands': ('assemble_clearing_batch', 'generate_settlement_file'),
        'controls': ('cutoff_calendar', 'hash_total', 'finalization_lock'),
    },
    {
        'wizard': 'ReturnAndReconciliationWizard',
        'steps': (
            'capture_return_or_statement',
            'classify_reason_or_match_type',
            'open_breaks_for_unmatched_lines',
            'prepare_repair_or_reversal',
            'record_operator_evidence',
        ),
        'commands': ('process_return_item', 'reconcile_bank_statement'),
        'controls': ('return_reason_profile', 'fee_classification', 'exception_evidence_required'),
    },
)

PAYMENT_CONTROLS = (
    {'control': 'rail_profile_validation', 'enforced_by': 'create_validated_payment_instruction'},
    {'control': 'participant_bank_capability', 'enforced_by': 'create_validated_payment_instruction'},
    {'control': 'duplicate_payment_prevention', 'enforced_by': 'create_validated_payment_instruction'},
    {'control': 'maker_checker_release', 'enforced_by': 'release_payment_instruction'},
    {'control': 'liquidity_buffer_check', 'enforced_by': 'release_payment_instruction'},
    {'control': 'settlement_file_integrity', 'enforced_by': 'generate_settlement_file'},
    {'control': 'acknowledgement_idempotency', 'enforced_by': 'handle_settlement_acknowledgement'},
    {'control': 'return_reason_deadline', 'enforced_by': 'process_return_item'},
    {'control': 'reconciliation_break_creation', 'enforced_by': 'reconcile_bank_statement'},
)

def bank_payments_clearing_ui_contract():
    surface = domain_capability_surface_contract()
    payment_actions = (
        'register_participant_bank',
        'create_validated_payment_instruction',
        'release_payment_instruction',
        'assemble_clearing_batch',
        'generate_settlement_file',
        'handle_settlement_acknowledgement',
        'process_return_item',
        'reconcile_bank_statement',
    )
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('BankPaymentsClearingWorkbench',
 'BankPaymentsClearingDetail',
 'BankPaymentsClearingAssistantPanel',
 'PaymentInstructionReleaseConsole',
 'ClearingBatchAssemblyBoard',
 'SettlementFileIntegrityPanel',
 'ReturnAndReconciliationWorkbench'), 'forms': PAYMENT_FORMS, 'wizards': PAYMENT_WIZARDS, 'controls': PAYMENT_CONTROLS, 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('bank_payments_clearing.read',
 'bank_payments_clearing.create',
 'bank_payments_clearing.update',
 'bank_payments_clearing.approve',
 'bank_payments_clearing.admin'), 'payment_actions': payment_actions, 'full_capability_surface': {'operation_actions': tuple(dict.fromkeys(payment_actions + tuple(DOMAIN_OPERATIONS))), 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in tuple(dict.fromkeys(payment_actions + tuple(DOMAIN_OPERATIONS)))), 'navigation_sections': ('overview','payment_release','clearing_batches','settlement_files','returns_reconciliation','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def bank_payments_clearing_render_workbench():
    ui = bank_payments_clearing_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'forms': ui['forms'], 'wizards': ui['wizards'], 'controls': ui['controls'], 'side_effects': ()}

def bank_payments_clearing_single_pbc_app_contract():
    ui = bank_payments_clearing_ui_contract()
    database_backing = {
        'owned_tables': DOMAIN_OWNED_TABLES,
        'migration': 'migrations/001_initial.sql',
        'models_module': 'models.py',
        'schema_contract_module': 'schema_contract.py',
    }
    return {
        'ok': bool(ui['forms']) and bool(ui['wizards']) and bool(ui['controls']) and bool(database_backing['owned_tables']),
        'pbc': PBC_KEY,
        'database_backing': database_backing,
        'forms': ui['forms'],
        'wizards': ui['wizards'],
        'controls': ui['controls'],
        'workbench_route': f'/workbench/pbcs/{PBC_KEY}',
        'agent_panel': 'BankPaymentsClearingAssistantPanel',
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def smoke_test():
    app = bank_payments_clearing_single_pbc_app_contract()
    return {'ok': bank_payments_clearing_ui_contract()['ok'] and bank_payments_clearing_render_workbench()['ok'] and app['ok'], 'single_pbc_app': app, 'side_effects': ()}
