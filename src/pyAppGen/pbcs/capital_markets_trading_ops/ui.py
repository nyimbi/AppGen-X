from .domain_depth import domain_capability_surface_contract, DOMAIN_OPERATIONS, DOMAIN_RULES, DOMAIN_PARAMETERS, DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_OWNED_TABLES, DOMAIN_EDGE_CASES
PBC_KEY = 'capital_markets_trading_ops'


def capital_markets_trading_ops_form_contract():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'form_id': 'trade_order_intake',
        'title': 'Trade Order Intake',
        'entity': 'trade_order',
        'fields': (
            {'name': 'tenant', 'required': True, 'control': 'text'},
            {'name': 'instrument_id', 'required': True, 'control': 'text'},
            {'name': 'product_type', 'required': True, 'control': 'select', 'options': ('equity', 'fixed_income', 'fx', 'listed_derivative')},
            {'name': 'trading_account', 'required': True, 'control': 'text'},
            {'name': 'desk', 'required': True, 'control': 'text'},
            {'name': 'trader', 'required': True, 'control': 'text'},
            {'name': 'book', 'required': True, 'control': 'text'},
            {'name': 'broker', 'required': True, 'control': 'text'},
            {'name': 'venue', 'required': True, 'control': 'text'},
            {'name': 'settlement_model', 'required': True, 'control': 'select', 'options': ('DVP', 'FOP', 'CCP')},
            {'name': 'regulatory_classification', 'required': True, 'control': 'text'},
            {'name': 'side', 'required': True, 'control': 'radio', 'options': ('BUY', 'SELL')},
            {'name': 'quantity', 'required': True, 'control': 'number'},
            {'name': 'limit_price', 'required': True, 'control': 'number'},
            {'name': 'submitted_at', 'required': True, 'control': 'datetime'},
            {'name': 'approval_state', 'required': False, 'control': 'approval-status'},
        ),
        'submission_route': 'POST /trade-orders',
        'validation_mode': 'server_authoritative',
        'shared_table_access': False,
        'side_effects': (),
    }


def capital_markets_trading_ops_wizard_contract():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'wizard_id': 'trade_order_release_wizard',
        'title': 'Trade Order Release Wizard',
        'steps': (
            {'id': 'capture_trade_order', 'title': 'Capture Order', 'form_id': 'trade_order_intake'},
            {'id': 'validate_reference_data', 'title': 'Validate Reference Data', 'control': 'reference_data_checklist'},
            {'id': 'run_pre_trade_controls', 'title': 'Run Pre-Trade Controls', 'control': 'risk_gate_panel'},
            {'id': 'review_release_decision', 'title': 'Review Release Decision', 'control': 'release_decision_card'},
        ),
        'supports_resume': True,
        'workbench_route': 'GET /capital-markets-trading-ops-workbench',
        'shared_table_access': False,
        'side_effects': (),
    }


def capital_markets_trading_ops_control_manifest():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'controls': (
            {
                'control_id': 'reference_data_checklist',
                'type': 'checklist',
                'gates': (
                    'instrument_id',
                    'trading_account',
                    'desk',
                    'trader',
                    'broker',
                    'venue',
                    'settlement_model',
                    'regulatory_classification',
                ),
            },
            {
                'control_id': 'risk_gate_panel',
                'type': 'policy-panel',
                'gates': (
                    'quantity_threshold',
                    'risk_threshold',
                    'restricted_book',
                    'blocked_counterparty',
                    'duplicate_instruction_window',
                    'four_eyes_approval',
                ),
            },
            {
                'control_id': 'release_decision_card',
                'type': 'decision-card',
                'actions': ('release', 'hold', 'escalate'),
            },
        ),
        'shared_table_access': False,
        'side_effects': (),
    }


def capital_markets_trading_ops_single_pbc_app_ui_contract():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'app_shell': 'CapitalMarketsTradingOpsAppShell',
        'forms': ('trade_order_intake',),
        'wizards': ('trade_order_release_wizard',),
        'controls': ('reference_data_checklist', 'risk_gate_panel', 'release_decision_card'),
        'workbench_views': ('trade_order_exceptions', 'ready_for_release', 'all_trade_orders'),
        'agent_help_surface': 'CapitalMarketsTradingOpsAssistantPanel',
        'shared_table_access': False,
        'side_effects': (),
    }


def capital_markets_trading_ops_ui_contract():
    surface = domain_capability_surface_contract()
    return {'ok': True, 'pbc': PBC_KEY, 'fragments': ('CapitalMarketsTradingOpsWorkbench',
 'CapitalMarketsTradingOpsDetail',
 'CapitalMarketsTradingOpsAssistantPanel'), 'configuration_editor': True, 'stream_engine_picker_visible': False, 'action_permissions': ('capital_markets_trading_ops.read',
 'capital_markets_trading_ops.create',
 'capital_markets_trading_ops.update',
 'capital_markets_trading_ops.approve',
 'capital_markets_trading_ops.admin'), 'forms': (capital_markets_trading_ops_form_contract(),), 'wizards': (capital_markets_trading_ops_wizard_contract(),), 'controls': capital_markets_trading_ops_control_manifest()['controls'], 'app_shell': capital_markets_trading_ops_single_pbc_app_ui_contract(), 'full_capability_surface': {'operation_actions': DOMAIN_OPERATIONS, 'rule_editors': DOMAIN_RULES, 'parameter_editors': DOMAIN_PARAMETERS, 'advanced_panels': DOMAIN_ADVANCED_CAPABILITIES, 'table_browsers': DOMAIN_OWNED_TABLES, 'edge_case_queues': DOMAIN_EDGE_CASES, 'agent_tools': tuple(f'{PBC_KEY}_skills.{op}' for op in DOMAIN_OPERATIONS), 'navigation_sections': ('overview','trade_order_intake','trade_order_release_wizard','workbench','edge_case_triage','advanced_intelligence','release_evidence'), 'coverage': surface['coverage']}, 'side_effects': ()}

def capital_markets_trading_ops_render_workbench():
    ui = capital_markets_trading_ops_ui_contract(); full = ui['full_capability_surface']
    return {'ok': True, 'pbc': PBC_KEY, 'route': f'/workbench/pbcs/{PBC_KEY}', 'operation_actions': full['operation_actions'], 'table_browsers': full['table_browsers'], 'queue_views': capital_markets_trading_ops_single_pbc_app_ui_contract()['workbench_views'], 'columns': ('id', 'tenant', 'status_badge', 'lifecycle_state', 'workbench_queue', 'release_ready'), 'controls': capital_markets_trading_ops_control_manifest()['controls'], 'side_effects': ()}

def smoke_test():
    return {'ok': capital_markets_trading_ops_ui_contract()['ok'] and capital_markets_trading_ops_render_workbench()['ok'] and capital_markets_trading_ops_form_contract()['ok'] and capital_markets_trading_ops_wizard_contract()['ok'] and capital_markets_trading_ops_control_manifest()['ok'], 'side_effects': ()}


def capital_markets_trading_ops_standalone_app_contract():
    base = capital_markets_trading_ops_single_pbc_app_ui_contract()
    forms = (
        'trade_order_intake',
        'execution_capture_form',
        'allocation_split_form',
        'confirmation_match_form',
        'settlement_instruction_form',
        'trade_break_resolution_form',
        'position_snapshot_review_form',
        'agent_document_instruction_form',
    )
    wizards = (
        'trade_order_release_wizard',
        'execution_allocation_wizard',
        'confirmation_affirmation_wizard',
        'settlement_fail_buy_in_wizard',
        'break_resolution_wizard',
        'release_evidence_wizard',
    )
    controls = (
        'reference_data_checklist',
        'risk_gate_panel',
        'release_decision_card',
        'allocation_eligibility_gate',
        'confirmation_economic_match_gate',
        'ssi_effectivity_gate',
        'settlement_fail_penalty_gate',
        'agent_mutation_confirmation_gate',
    )
    return {
        'ok': base['ok'] and len(forms) >= 8 and len(wizards) >= 6 and len(controls) >= 8,
        'pbc': PBC_KEY,
        'app_id': 'capital_markets_trading_ops_one_pbc_app',
        'forms': forms,
        'wizards': wizards,
        'controls': controls,
        'workbench_views': (
            'trade_order_exceptions',
            'ready_for_release',
            'execution_allocation_queue',
            'confirmation_mismatch_queue',
            'settlement_fails_and_buyins',
            'break_resolution_queue',
            'position_provenance_review',
        ),
        'agent_tools': tuple(f'{PBC_KEY}_skills.{name}' for name in ('triage_order', 'explain_break', 'draft_allocation', 'summarize_confirmation', 'prepare_settlement_repair')),
        'configuration_editor': True,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }
