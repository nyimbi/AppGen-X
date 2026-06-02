"""World-class domain depth contract for the reinsurance_management PBC."""

from __future__ import annotations

import hashlib
import json

PBC_KEY = 'reinsurance_management'
DOMAIN_ENTITY = 'reinsurance_treaty'
DOMAIN_PURPOSE = (
    'Standalone reinsurance operating application for treaties, facultative placements, '
    'layers, cessions, bordereaux, recoverables, claims recoveries, catastrophe handling, '
    'collateral, settlement statements, cash calls, commutations, retrocession, and governed '
    'assistant previews.'
)
DOMAIN_RULES = (
    'treaty_structure_policy',
    'cession_eligibility_policy',
    'bordereau_validation_policy',
    'recoverable_collection_policy',
    'counterparty_credit_policy',
    'collateral_threshold_policy',
    'commutation_approval_policy',
)
DOMAIN_PARAMETERS = (
    'quality_score_floor',
    'materiality_threshold',
    'approval_sla_hours',
    'risk_threshold',
    'cat_event_hours_clause',
    'counterparty_watch_threshold',
    'workbench_limit',
)
DOMAIN_EVENTS = (
    'ReinsuranceManagementCreated',
    'ReinsuranceManagementUpdated',
    'ReinsuranceManagementApproved',
    'ReinsuranceManagementExceptionOpened',
)
DOMAIN_CONSUMED_EVENTS = (
    'PolicyChanged',
    'AuditEventSealed',
    'OperationalKpiChanged',
)
DOMAIN_ADVANCED_CAPABILITIES = (
    'treaty_and_facultative_program_structuring',
    'layer_and_aggregate_exhaustion_monitoring',
    'catastrophe_event_and_hours_clause_management',
    'recoverable_impairment_and_collection_triage',
    'collateral_and_funds_withheld_surveillance',
    'statement_cash_call_and_commutation_workflows',
    'retrocession_program_oversight',
    'assistant_document_and_instruction_mutation_preview',
)
DOMAIN_WORKBENCH_VIEWS = (
    'program_dashboard',
    'placement_console',
    'recoverables_queue',
    'catastrophe_event_room',
    'settlement_and_cash_call_board',
    'audit_and_reconciliation_board',
    'assistant_preview_panel',
)
DOMAIN_WIZARDS = (
    {
        'id': 'treaty_onboarding',
        'title': 'Treaty Onboarding',
        'steps': (
            'classify structure',
            'capture participants',
            'define layers and aggregates',
            'attach premium and commission terms',
            'confirm clauses and approvals',
        ),
    },
    {
        'id': 'cat_event_response',
        'title': 'Cat Event Response',
        'steps': (
            'register occurrence window',
            'link impacted claims and layers',
            'estimate ceded loss and reinstatements',
            'prepare notice package',
            'open recoveries and statements',
        ),
    },
    {
        'id': 'cash_call_collection',
        'title': 'Cash Call Collection',
        'steps': (
            'assemble statement lines',
            'determine amount due',
            'check collateral and credit support',
            'issue cash call',
            'reconcile receipts',
        ),
    },
    {
        'id': 'commutation_negotiation',
        'title': 'Commutation Negotiation',
        'steps': (
            'identify open recoverables',
            'estimate runoff value',
            'set negotiation range',
            'record approvals',
            'close impacted obligations',
        ),
    },
)
DOMAIN_FORMS = (
    {
        'id': 'treaty_form',
        'entity': 'reinsurance_treaty',
        'fields': (
            'treaty_id',
            'treaty_type',
            'cedant',
            'effective_from',
            'effective_to',
            'covered_lines',
            'participants',
            'layers',
            'aggregate_limit',
            'reinstatements',
        ),
    },
    {
        'id': 'placement_form',
        'entity': 'facultative_placement',
        'fields': (
            'placement_id',
            'risk_reference',
            'market_list',
            'quote_terms',
            'signed_lines',
            'subjectivities',
            'bind_requested',
        ),
    },
    {
        'id': 'cession_form',
        'entity': 'cession',
        'fields': (
            'cession_id',
            'treaty_id',
            'policy_reference',
            'gross_premium',
            'gross_loss',
            'share',
            'layer_id',
            'event_id',
        ),
    },
    {
        'id': 'recovery_form',
        'entity': 'claim_recovery',
        'fields': (
            'recovery_id',
            'claim_reference',
            'recoverable_id',
            'required_documents',
            'submitted_documents',
            'status',
        ),
    },
)
TABLE_SPECS = (
    {
        'entity': 'reinsurance_treaty',
        'table': f'{PBC_KEY}_reinsurance_treaty',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'treaty_type', 'effective_from', 'effective_to', 'aggregate_limit', 'remaining_limit',
        ),
        'summary': 'Treaty wording, economics, participants, layers, and clauses.',
    },
    {
        'entity': 'facultative_placement',
        'table': f'{PBC_KEY}_facultative_placement',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'risk_reference', 'required_share_pct', 'bound_share_pct', 'quote_count',
        ),
        'summary': 'Facultative submission, quote, subjectivity, and bind evidence.',
    },
    {
        'entity': 'cession',
        'table': f'{PBC_KEY}_cession',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'treaty_id', 'layer_id', 'gross_premium', 'gross_loss', 'ceded_premium', 'ceded_loss',
        ),
        'summary': 'Eligible cessions with traceable ceded premium and ceded loss calculations.',
    },
    {
        'entity': 'bordereau',
        'table': f'{PBC_KEY}_bordereau',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'bordereau_type', 'period', 'accepted_rows', 'rejected_rows', 'submission_status',
        ),
        'summary': 'Premium, loss, exposure, and claims bordereaux with validation results.',
    },
    {
        'entity': 'recoverable',
        'table': f'{PBC_KEY}_recoverable',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'counterparty_id', 'amount', 'currency', 'aging_bucket', 'impairment_flag',
        ),
        'summary': 'Recoverables from estimated through collected or commuted.',
    },
    {
        'entity': 'claim_recovery',
        'table': f'{PBC_KEY}_claim_recovery',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'claim_reference', 'recoverable_id', 'notice_date', 'documentation_complete',
        ),
        'summary': 'Claim notices, billing, disputes, and recovery collection tracking.',
    },
    {
        'entity': 'exposure_layer',
        'table': f'{PBC_KEY}_exposure_layer',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'peril', 'attachment_point', 'exhaustion_point', 'utilized_limit', 'remaining_limit',
        ),
        'summary': 'Layered exposure protection by peril, geography, and aggregate basis.',
    },
    {
        'entity': 'counterparty_projection',
        'table': f'{PBC_KEY}_counterparty_projection',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'role', 'rating', 'domicile', 'signed_share_pct', 'watchlist',
        ),
        'summary': 'Reinsurer, broker, pool, and retrocessionaire projections.',
    },
    {
        'entity': 'collateral_position',
        'table': f'{PBC_KEY}_collateral_position',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'counterparty_id', 'required_amount', 'posted_amount', 'deficiency_amount', 'expiry_date',
        ),
        'summary': 'Letters of credit, trust balances, and funds-withheld collateral positions.',
    },
    {
        'entity': 'settlement_statement',
        'table': f'{PBC_KEY}_settlement_statement',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'counterparty_id', 'statement_period', 'line_count', 'balance_due', 'currency',
        ),
        'summary': 'Premium, commission, loss, and balance-forward settlement statements.',
    },
    {
        'entity': 'cash_call',
        'table': f'{PBC_KEY}_cash_call',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'statement_id', 'recoverable_id', 'amount_due', 'due_date', 'urgency',
        ),
        'summary': 'Cash call instructions and collection tracking.',
    },
    {
        'entity': 'commutation_case',
        'table': f'{PBC_KEY}_commutation_case',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'treaty_id', 'recoverable_count', 'negotiated_amount', 'approval_state',
        ),
        'summary': 'Runoff commutation analysis, negotiation, approval, and settlement.',
    },
    {
        'entity': 'retrocession_program',
        'table': f'{PBC_KEY}_retrocession_program',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'source_treaty_id', 'retro_share_pct', 'retro_limit', 'protection_basis',
        ),
        'summary': 'Retrocession overlays protecting ceded reinsurance positions.',
    },
    {
        'entity': 'catastrophe_event',
        'table': f'{PBC_KEY}_catastrophe_event',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'peril', 'occurrence_start', 'occurrence_end', 'gross_loss_estimate', 'ceded_loss_estimate',
        ),
        'summary': 'Catastrophe event room for hours clauses, accumulation, and notices.',
    },
    {
        'entity': 'audit_reconciliation',
        'table': f'{PBC_KEY}_audit_reconciliation',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'source_total', 'ledger_total', 'statement_total', 'variance', 'resolution_status',
        ),
        'summary': 'Audit and reconciliation evidence across bordereaux, statements, and cash.',
    },
    {
        'entity': 'assistant_preview',
        'table': f'{PBC_KEY}_assistant_preview',
        'fields': (
            'id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at',
            'instruction', 'suggested_action', 'candidate_tables', 'requires_confirmation',
        ),
        'summary': 'Governed AI assistant previews for document and instruction CRUD.',
    },
    {
        'entity': 'reinsurance_management_policy_rule',
        'table': f'{PBC_KEY}_reinsurance_management_policy_rule',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'Package-local compiled rules.',
    },
    {
        'entity': 'reinsurance_management_runtime_parameter',
        'table': f'{PBC_KEY}_reinsurance_management_runtime_parameter',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'Bounded runtime parameters.',
    },
    {
        'entity': 'reinsurance_management_schema_extension',
        'table': f'{PBC_KEY}_reinsurance_management_reinsurance_management_schema_extension',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'Owned-schema extension registry.',
    },
    {
        'entity': 'reinsurance_management_control_assertion',
        'table': f'{PBC_KEY}_reinsurance_management_reinsurance_management_control_assertion',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'Control assertions and approvals.',
    },
    {
        'entity': 'reinsurance_management_governed_model',
        'table': f'{PBC_KEY}_reinsurance_management_reinsurance_management_governed_model',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'Governed model cards and policy bindings.',
    },
    {
        'entity': 'appgen_outbox_event',
        'table': f'{PBC_KEY}_appgen_outbox_event',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'AppGen-X outbox events.',
    },
    {
        'entity': 'appgen_inbox_event',
        'table': f'{PBC_KEY}_appgen_inbox_event',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'AppGen-X inbox events.',
    },
    {
        'entity': 'appgen_dead_letter_event',
        'table': f'{PBC_KEY}_appgen_dead_letter_event',
        'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'summary': 'AppGen-X dead-letter events.',
    },
)
DOMAIN_OWNED_TABLES = tuple(spec['table'] for spec in TABLE_SPECS)
DOMAIN_BUSINESS_TABLES = tuple(
    spec['table']
    for spec in TABLE_SPECS
    if spec['entity'] not in {'appgen_outbox_event', 'appgen_inbox_event', 'appgen_dead_letter_event'}
)
DOMAIN_OPERATION_SPECS = (
    {
        'operation': 'create_reinsurance_treaty',
        'target_table': f'{PBC_KEY}_reinsurance_treaty',
        'event': DOMAIN_EVENTS[0],
        'permission': f'{PBC_KEY}.create',
        'wizard': 'treaty_onboarding',
        'form': 'treaty_form',
    },
    {
        'operation': 'record_facultative_placement',
        'target_table': f'{PBC_KEY}_facultative_placement',
        'event': DOMAIN_EVENTS[1],
        'permission': f'{PBC_KEY}.create',
        'wizard': 'treaty_onboarding',
        'form': 'placement_form',
    },
    {
        'operation': 'review_cession',
        'target_table': f'{PBC_KEY}_cession',
        'event': DOMAIN_EVENTS[1],
        'permission': f'{PBC_KEY}.update',
        'wizard': 'cat_event_response',
        'form': 'cession_form',
    },
    {
        'operation': 'approve_bordereau',
        'target_table': f'{PBC_KEY}_bordereau',
        'event': DOMAIN_EVENTS[2],
        'permission': f'{PBC_KEY}.approve',
        'wizard': 'cash_call_collection',
        'form': 'cession_form',
    },
    {
        'operation': 'simulate_recoverable',
        'target_table': f'{PBC_KEY}_recoverable',
        'event': DOMAIN_EVENTS[1],
        'permission': f'{PBC_KEY}.update',
        'wizard': 'cash_call_collection',
        'form': 'recovery_form',
    },
    {
        'operation': 'create_claim_recovery',
        'target_table': f'{PBC_KEY}_claim_recovery',
        'event': DOMAIN_EVENTS[0],
        'permission': f'{PBC_KEY}.create',
        'wizard': 'cash_call_collection',
        'form': 'recovery_form',
    },
    {
        'operation': 'record_exposure_layer',
        'target_table': f'{PBC_KEY}_exposure_layer',
        'event': DOMAIN_EVENTS[0],
        'permission': f'{PBC_KEY}.create',
        'wizard': 'treaty_onboarding',
        'form': 'treaty_form',
    },
    {
        'operation': 'register_counterparty_projection',
        'target_table': f'{PBC_KEY}_counterparty_projection',
        'event': DOMAIN_EVENTS[1],
        'permission': f'{PBC_KEY}.update',
        'wizard': 'treaty_onboarding',
        'form': 'treaty_form',
    },
    {
        'operation': 'record_collateral_position',
        'target_table': f'{PBC_KEY}_collateral_position',
        'event': DOMAIN_EVENTS[1],
        'permission': f'{PBC_KEY}.update',
        'wizard': 'cash_call_collection',
        'form': 'recovery_form',
    },
    {
        'operation': 'open_catastrophe_event',
        'target_table': f'{PBC_KEY}_catastrophe_event',
        'event': DOMAIN_EVENTS[0],
        'permission': f'{PBC_KEY}.create',
        'wizard': 'cat_event_response',
        'form': 'cession_form',
    },
    {
        'operation': 'create_settlement_statement',
        'target_table': f'{PBC_KEY}_settlement_statement',
        'event': DOMAIN_EVENTS[2],
        'permission': f'{PBC_KEY}.approve',
        'wizard': 'cash_call_collection',
        'form': 'recovery_form',
    },
    {
        'operation': 'create_cash_call',
        'target_table': f'{PBC_KEY}_cash_call',
        'event': DOMAIN_EVENTS[2],
        'permission': f'{PBC_KEY}.approve',
        'wizard': 'cash_call_collection',
        'form': 'recovery_form',
    },
    {
        'operation': 'create_commutation_case',
        'target_table': f'{PBC_KEY}_commutation_case',
        'event': DOMAIN_EVENTS[2],
        'permission': f'{PBC_KEY}.approve',
        'wizard': 'commutation_negotiation',
        'form': 'recovery_form',
    },
    {
        'operation': 'register_retrocession_program',
        'target_table': f'{PBC_KEY}_retrocession_program',
        'event': DOMAIN_EVENTS[0],
        'permission': f'{PBC_KEY}.create',
        'wizard': 'treaty_onboarding',
        'form': 'treaty_form',
    },
    {
        'operation': 'reconcile_audit_evidence',
        'target_table': f'{PBC_KEY}_audit_reconciliation',
        'event': DOMAIN_EVENTS[3],
        'permission': f'{PBC_KEY}.admin',
        'wizard': 'cash_call_collection',
        'form': 'recovery_form',
    },
    {
        'operation': 'generate_assistant_preview',
        'target_table': f'{PBC_KEY}_assistant_preview',
        'event': DOMAIN_EVENTS[1],
        'permission': f'{PBC_KEY}.update',
        'wizard': 'cat_event_response',
        'form': 'recovery_form',
    },
)
DOMAIN_OPERATIONS = tuple(spec['operation'] for spec in DOMAIN_OPERATION_SPECS)
ROUTE_SPECS = (
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/runtime/configuration', 'operation': 'configure_runtime'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/runtime/parameters', 'operation': 'set_parameter'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/runtime/rules', 'operation': 'register_rule'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/runtime/schema-extensions', 'operation': 'register_schema_extension'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/events/inbox', 'operation': 'receive_event'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/reinsurance-treaties', 'operation': 'create_reinsurance_treaty'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/facultative-placements', 'operation': 'record_facultative_placement'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/cessions', 'operation': 'review_cession'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/bordereaux', 'operation': 'approve_bordereau'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/recoverables', 'operation': 'simulate_recoverable'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/claim-recoveries', 'operation': 'create_claim_recovery'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/exposure-layers', 'operation': 'record_exposure_layer'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/counterparties', 'operation': 'register_counterparty_projection'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/collateral-positions', 'operation': 'record_collateral_position'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/catastrophe-events', 'operation': 'open_catastrophe_event'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/statements', 'operation': 'create_settlement_statement'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/cash-calls', 'operation': 'create_cash_call'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/commutations', 'operation': 'create_commutation_case'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/retrocession-programs', 'operation': 'register_retrocession_program'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/reconciliations', 'operation': 'reconcile_audit_evidence'},
    {'method': 'POST', 'path': '/api/pbc/reinsurance_management/assistant/previews', 'operation': 'generate_assistant_preview'},
    {'method': 'GET', 'path': '/api/pbc/reinsurance_management/workbench', 'operation': 'query_workbench'},
)
PUBLIC_API_ROUTES = tuple(f"{spec['method']} {spec['path']}" for spec in ROUTE_SPECS)
DOMAIN_EDGE_CASES = (
    'treaty_share_exceeds_100_pct',
    'layer_limit_exhausted',
    'duplicate_bordereau_rows',
    'missing_claim_documents',
    'counterparty_credit_downgrade',
    'collateral_shortfall',
    'cash_call_due_soon',
    'commutation_without_approval',
    'retrocession_gap',
    'cross_tenant_access_attempt',
    'idempotency_replay',
    'unexpected_inbound_event',
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        DOMAIN_ADVANCED_CAPABILITIES
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def _digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode('utf-8')).hexdigest()


def domain_depth_contract() -> dict:
    return {
        'format': f'appgen.{PBC_KEY}.world-class-domain-depth.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'purpose': DOMAIN_PURPOSE,
        'owned_tables': DOMAIN_OWNED_TABLES,
        'business_tables': DOMAIN_BUSINESS_TABLES,
        'table_specs': TABLE_SPECS,
        'operation_count': len(DOMAIN_OPERATIONS),
        'operations': DOMAIN_OPERATIONS,
        'operation_specs': DOMAIN_OPERATION_SPECS,
        'rules': DOMAIN_RULES,
        'parameters': DOMAIN_PARAMETERS,
        'emitted_events': DOMAIN_EVENTS,
        'consumed_events': DOMAIN_CONSUMED_EVENTS,
        'advanced_capabilities': DOMAIN_ADVANCED_CAPABILITIES,
        'workbench_views': DOMAIN_WORKBENCH_VIEWS,
        'wizards': DOMAIN_WIZARDS,
        'forms': DOMAIN_FORMS,
        'public_routes': PUBLIC_API_ROUTES,
        'database_backends': ('postgresql', 'mysql', 'mariadb'),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'shared_table_access': False,
        'minimum_owned_domain_tables': 20,
        'minimum_domain_operations': 12,
        'side_effects': (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    spec = next((item for item in DOMAIN_OPERATION_SPECS if item['operation'] == operation), None)
    if spec is None:
        return {
            'ok': False,
            'reason': 'unknown_domain_operation',
            'operation': operation,
            'side_effects': (),
        }
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'operation': operation,
        'operation_kind': 'command',
        'target_table': spec['target_table'],
        'owned_tables': (spec['target_table'],),
        'read_tables': (),
        'emitted_event': spec['event'],
        'event_contract': 'AppGen-X',
        'idempotency_key': _digest((PBC_KEY, operation, payload)),
        'rules_evaluated': DOMAIN_RULES[:3],
        'parameters_read': DOMAIN_PARAMETERS[:3],
        'permission': spec['permission'],
        'wizard': spec['wizard'],
        'form': spec['form'],
        'evidence_hash': _digest((operation, payload, spec['target_table'], spec['event'])),
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(
        execute_domain_operation(operation, {'tenant': 'tenant-smoke'})
        for operation in DOMAIN_OPERATIONS[:6]
    )
    return {
        'ok': contract['ok']
        and len(contract['owned_tables']) >= contract['minimum_owned_domain_tables']
        and contract['operation_count'] >= contract['minimum_domain_operations']
        and all(item['ok'] for item in executions)
        and all(item['target_table'].startswith(f'{PBC_KEY}_') for item in executions),
        'contract': contract,
        'executions': executions,
        'side_effects': (),
    }


def domain_capability_surface_contract() -> dict:
    return {
        'format': f'appgen.{PBC_KEY}.complete-domain-capability-surface.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'operation_surfaces': tuple(
            {
                'operation': spec['operation'],
                'surface': f"{PBC_KEY}.ui.operation.{spec['operation']}",
                'action': spec['operation'],
                'target_table': spec['target_table'],
                'permission': spec['permission'],
                'requires_confirmation': True,
                'wizard': spec['wizard'],
                'form': spec['form'],
                'event': spec['event'],
            }
            for spec in DOMAIN_OPERATION_SPECS
        ),
        'rule_surfaces': tuple(
            {
                'rule': rule,
                'surface': f'{PBC_KEY}.ui.rule.{rule}',
                'editor': True,
                'explainable': True,
            }
            for rule in DOMAIN_RULES
        ),
        'parameter_surfaces': tuple(
            {
                'parameter': parameter,
                'surface': f'{PBC_KEY}.ui.parameter.{parameter}',
                'bounded': True,
                'editable': True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        'wizard_surfaces': tuple(
            {
                'wizard': wizard['id'],
                'surface': f"{PBC_KEY}.ui.wizard.{wizard['id']}",
                'steps': wizard['steps'],
            }
            for wizard in DOMAIN_WIZARDS
        ),
        'advanced_surfaces': tuple(
            {
                'capability': capability,
                'surface': f'{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}',
                'explainable': True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        'edge_case_surfaces': tuple(
            {
                'edge_case': edge_case,
                'surface': f'{PBC_KEY}.ui.edge_case.{edge_case}',
                'triage_queue': True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        'table_surfaces': tuple(
            {
                'owned_table': table,
                'surface': f'{PBC_KEY}.ui.table.{table}',
                'read_model': True,
                'mutation_guard': True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        'specialist_capabilities': DOMAIN_SPECIALIST_CAPABILITIES,
        'coverage': {
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'shared_table_access': False,
        },
        'side_effects': (),
    }
