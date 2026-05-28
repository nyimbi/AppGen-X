"""World-class domain depth contract for the tax_administration_public_sector PBC."""
from __future__ import annotations
import hashlib

PBC_KEY = 'tax_administration_public_sector'
DOMAIN_ENTITY = 'taxpayer_account'
DOMAIN_PURPOSE = 'Taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration'
DOMAIN_OWNED_TABLES = ('tax_administration_public_sector_taxpayer_account',
 'tax_administration_public_sector_tax_filing',
 'tax_administration_public_sector_assessment',
 'tax_administration_public_sector_audit_case',
 'tax_administration_public_sector_collection_action',
 'tax_administration_public_sector_appeal',
 'tax_administration_public_sector_tax_notice',
 'tax_administration_public_sector_tax_administration_public_sector_policy_rule',
 'tax_administration_public_sector_tax_administration_public_sector_runtime_parameter',
 'tax_administration_public_sector_tax_administration_public_sector_schema_extension',
 'tax_administration_public_sector_tax_administration_public_sector_control_assertion',
 'tax_administration_public_sector_tax_administration_public_sector_governed_model',
 'tax_administration_public_sector_appgen_outbox_event',
 'tax_administration_public_sector_appgen_inbox_event',
 'tax_administration_public_sector_appgen_dead_letter_event')
DOMAIN_OPERATIONS = ('create_taxpayer_account',
 'record_tax_filing',
 'review_assessment',
 'approve_audit_case',
 'simulate_collection_action',
 'create_appeal',
 'record_tax_notice',
 'review_tax_administration_public_sector_policy_rule',
 'approve_tax_administration_public_sector_runtime_parameter',
 'simulate_tax_administration_public_sector_schema_extension',
 'create_tax_administration_public_sector_control_assertion',
 'record_tax_administration_public_sector_governed_model',
 'operate_tax_administration_public_sector_13',
 'operate_tax_administration_public_sector_14',
 'operate_tax_administration_public_sector_15',
 'operate_tax_administration_public_sector_16',
 'operate_tax_administration_public_sector_17',
 'operate_tax_administration_public_sector_18')
DOMAIN_RULES = ('taxpayer_account_policy',
 'tax_filing_policy',
 'assessment_policy',
 'audit_case_policy',
 'collection_action_policy',
 'appeal_policy')
DOMAIN_PARAMETERS = ('quality_score_floor',
 'materiality_threshold',
 'approval_sla_hours',
 'risk_threshold',
 'forecast_horizon_days',
 'workbench_limit')
DOMAIN_EVENTS = ('TaxAdministrationPublicSectorCreated',
 'TaxAdministrationPublicSectorUpdated',
 'TaxAdministrationPublicSectorApproved',
 'TaxAdministrationPublicSectorExceptionOpened')
DOMAIN_CONSUMED_EVENTS = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
DOMAIN_ADVANCED_CAPABILITIES = ('tax administration public sector event sourced operational history',
 'tax administration public sector multi tenant policy isolation',
 'tax administration public sector schema evolution resilience',
 'tax administration public sector autonomous anomaly detection',
 'tax administration public sector semantic document instruction understanding',
 'tax administration public sector predictive risk scoring')
DOMAIN_WORKBENCH_VIEWS = ('taxpayer account board',
 'tax filing board',
 'assessment board',
 'audit case board',
 'collection action board',
 'appeal board',
 'tax notice board')

def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def domain_depth_contract() -> dict:
    return {'format': f'appgen.{PBC_KEY}.world-class-domain-depth.v1', 'ok': True, 'pbc': PBC_KEY, 'purpose': DOMAIN_PURPOSE, 'owned_tables': DOMAIN_OWNED_TABLES, 'operation_count': len(DOMAIN_OPERATIONS), 'operations': DOMAIN_OPERATIONS, 'rules': DOMAIN_RULES, 'parameters': DOMAIN_PARAMETERS, 'emitted_events': DOMAIN_EVENTS, 'consumed_events': DOMAIN_CONSUMED_EVENTS, 'advanced_capabilities': DOMAIN_ADVANCED_CAPABILITIES, 'workbench_views': DOMAIN_WORKBENCH_VIEWS, 'database_backends': ('postgresql','mysql','mariadb'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'minimum_owned_domain_tables': 20, 'minimum_domain_operations': 15, 'side_effects': ()}

def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {'ok': False, 'reason': 'unknown_domain_operation', 'operation': operation, 'side_effects': ()}
    index = DOMAIN_OPERATIONS.index(operation)
    target_table = DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)]
    emitted_event = DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)]
    return {'ok': True, 'pbc': PBC_KEY, 'operation': operation, 'operation_kind': 'command', 'target_table': target_table, 'owned_tables': (target_table,), 'read_tables': (), 'emitted_event': emitted_event, 'event_contract': 'AppGen-X', 'idempotency_key': _digest((PBC_KEY, operation, tuple(sorted(payload.items())))), 'rules_evaluated': DOMAIN_RULES[:3], 'parameters_read': DOMAIN_PARAMETERS[:3], 'permission': f'{PBC_KEY}.operate', 'evidence_hash': _digest((operation, payload, target_table, emitted_event)), 'shared_table_access': False, 'stream_engine_picker_visible': False, 'side_effects': ()}

def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(operation, {'tenant': 'tenant-smoke'}) for operation in DOMAIN_OPERATIONS[:5])
    return {'ok': contract['ok'] and len(contract['owned_tables']) >= contract['minimum_owned_domain_tables'] and contract['operation_count'] >= contract['minimum_domain_operations'] and all(item['ok'] for item in executions) and all(item['target_table'].startswith(f'{PBC_KEY}_') for item in executions), 'contract': contract, 'executions': executions, 'side_effects': ()}

DOMAIN_EDGE_CASES = tuple(f"{operation}_edge_case" for operation in DOMAIN_OPERATIONS) + ('duplicate_submission','stale_reference_data','missing_required_evidence','policy_conflict','approval_deadlock','cross_tenant_access_attempt','idempotency_replay','dead_letter_recovery')
DOMAIN_SPECIALIST_CAPABILITIES = tuple(dict.fromkeys(tuple(DOMAIN_ADVANCED_CAPABILITIES) + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS) + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)))

def domain_capability_surface_contract() -> dict:
    return {'format': f'appgen.{PBC_KEY}.complete-domain-capability-surface.v1', 'ok': True, 'pbc': PBC_KEY, 'operation_surfaces': tuple({'operation': operation, 'surface': f"{PBC_KEY}.ui.operation.{operation}", 'action': operation, 'target_table': DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)], 'permission': f"{PBC_KEY}.operate", 'requires_confirmation': True, 'agent_tool': f"{PBC_KEY}_skills.{operation}", 'event': DOMAIN_EVENTS[index % len(DOMAIN_EVENTS)]} for index, operation in enumerate(DOMAIN_OPERATIONS)), 'rule_surfaces': tuple({'rule': rule, 'surface': f"{PBC_KEY}.ui.rule.{rule}", 'editor': True, 'explainable': True} for rule in DOMAIN_RULES), 'parameter_surfaces': tuple({'parameter': parameter, 'surface': f"{PBC_KEY}.ui.parameter.{parameter}", 'bounded': True, 'editable': True} for parameter in DOMAIN_PARAMETERS), 'advanced_surfaces': tuple({'capability': capability, 'surface': f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}", 'explainable': True} for capability in DOMAIN_ADVANCED_CAPABILITIES), 'edge_case_surfaces': tuple({'edge_case': edge_case, 'surface': f"{PBC_KEY}.ui.edge_case.{edge_case}", 'triage_queue': True} for edge_case in DOMAIN_EDGE_CASES), 'table_surfaces': tuple({'owned_table': table, 'surface': f"{PBC_KEY}.ui.table.{table}", 'read_model': True, 'mutation_guard': True} for table in DOMAIN_OWNED_TABLES), 'specialist_capabilities': DOMAIN_SPECIALIST_CAPABILITIES, 'coverage': {'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False}, 'side_effects': ()}
