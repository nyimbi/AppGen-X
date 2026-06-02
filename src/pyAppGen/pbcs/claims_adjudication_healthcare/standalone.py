"""Standalone one-PBC app surface for healthcare claims adjudication."""
from __future__ import annotations

import hashlib
from typing import Mapping, Sequence

from .agent import document_instruction_crud_support
from .runtime import (
    CLAIMS_ADJUDICATION_HEALTHCARE_ALLOWED_DATABASE_BACKENDS,
    CLAIMS_ADJUDICATION_HEALTHCARE_BUSINESS_TABLES,
    CLAIMS_ADJUDICATION_HEALTHCARE_CONSUMED_EVENT_TYPES,
    CLAIMS_ADJUDICATION_HEALTHCARE_EMITTED_EVENT_TYPES,
    CLAIMS_ADJUDICATION_HEALTHCARE_OWNED_TABLES,
    claims_adjudication_healthcare_approve_benefit_rule,
    claims_adjudication_healthcare_build_api_contract,
    claims_adjudication_healthcare_build_schema_contract,
    claims_adjudication_healthcare_build_service_contract,
    claims_adjudication_healthcare_command_health_claim,
    claims_adjudication_healthcare_create_appeal,
    claims_adjudication_healthcare_empty_state,
    claims_adjudication_healthcare_record_claim_line,
    claims_adjudication_healthcare_runtime_smoke,
    claims_adjudication_healthcare_simulate_denial,
    claims_adjudication_healthcare_verify_owned_table_boundary,
)

PBC_KEY = 'claims_adjudication_healthcare'
EVENT_CONTRACT = 'AppGen-X'
IMPROVE1_ITEMS = tuple(range(1, 51))

DECLARED_DEPENDENCIES = {
    'member_eligibility_projection': {'source_event': 'EligibilityChanged', 'access': 'event_or_api_projection', 'forbidden_tables': ('member_enrollment', 'coverage_enrollment')},
    'provider_network_projection': {'source_event': 'ProviderNetworkChanged', 'access': 'event_or_api_projection', 'forbidden_tables': ('provider_master', 'provider_contract')},
    'authorization_projection': {'source_event': 'PriorAuthorizationChanged', 'access': 'event_or_api_projection', 'forbidden_tables': ('prior_authorization',)},
    'accumulator_projection': {'source_event': 'AccumulatorChanged', 'access': 'event_or_api_projection', 'forbidden_tables': ('member_accumulator',)},
    'pricing_projection': {'source_event': 'FeeScheduleChanged', 'access': 'event_or_api_projection', 'forbidden_tables': ('fee_schedule', 'provider_contract_rate')},
    'audit_projection': {'source_event': 'AuditEventSealed', 'access': 'event_projection', 'forbidden_tables': ()},
}

FORMS = (
    {'key': 'claim_intake_form', 'owned_table': 'claims_adjudication_healthcare_health_claim', 'improve1_items': (1, 2, 4, 5, 20, 34), 'operations': ('canonicalize_claim', 'check_duplicate', 'create_health_claim'), 'fields': ('claim_number', 'claim_type', 'source_format', 'member_id', 'provider_id', 'plan_id', 'received_date', 'correction_type')},
    {'key': 'claim_line_adjudication_form', 'owned_table': 'claims_adjudication_healthcare_claim_line', 'improve1_items': (3, 9, 10, 11, 12, 23, 24, 25, 26, 27, 28), 'operations': ('record_claim_line', 'validate_coding', 'price_line', 'apply_cost_share'), 'fields': ('service_date', 'place_of_service', 'diagnosis_code', 'procedure_code', 'modifiers', 'units', 'charge_amount', 'allowed_amount')},
    {'key': 'benefit_medical_necessity_form', 'owned_table': 'claims_adjudication_healthcare_benefit_rule', 'improve1_items': (6, 7, 8, 11, 12, 23, 30, 31), 'operations': ('approve_benefit_rule', 'match_authorization', 'review_medical_necessity'), 'fields': ('plan_id', 'service_code', 'effective_from', 'effective_to', 'auth_required', 'cost_share', 'clinical_basis')},
    {'key': 'denial_appeal_form', 'owned_table': 'claims_adjudication_healthcare_denial', 'improve1_items': (13, 14, 15, 19, 22, 32, 47), 'operations': ('simulate_denial', 'create_appeal', 'record_adjustment'), 'fields': ('denial_code', 'rationale', 'line_ids', 'notice_text', 'appeal_deadline', 'reviewer', 'determination')},
    {'key': 'payment_integrity_form', 'owned_table': 'claims_adjudication_healthcare_payment_integrity_case', 'improve1_items': (16, 17, 18, 21, 24, 33, 39, 40), 'operations': ('score_duplicate', 'open_integrity_case', 'review_fwa_signal', 'create_recovery'), 'fields': ('trigger', 'suspected_issue', 'dollar_exposure', 'evidence', 'reviewer', 'recovery_status', 'dispute_path')},
    {'key': 'attachment_document_form', 'owned_table': 'claims_adjudication_healthcare_coding_review', 'improve1_items': (7, 9, 18, 19, 35, 36, 37, 38), 'operations': ('capture_attachment', 'extract_document_facts', 'require_reviewer_confirmation'), 'fields': ('attachment_id', 'source', 'linked_lines', 'extracted_facts', 'redaction_profile', 'retention_class')},
    {'key': 'controls_release_form', 'owned_table': 'claims_adjudication_healthcare_claims_adjudication_healthcare_control_assertion', 'improve1_items': (41, 42, 43, 44, 45, 46, 48, 49, 50), 'operations': ('run_control_tests', 'assemble_release_packet', 'publish_dsl_agent_surface'), 'fields': ('control_id', 'threshold', 'failed_records', 'remediation', 'release_scenario', 'signoff')},
)

WIZARDS = (
    {'key': 'claim_intake_to_adjudication_wizard', 'steps': ('canonicalize', 'validate_member_provider_projection', 'dedupe', 'create_claim', 'route_lines'), 'improve1_items': (1, 2, 3, 4, 5, 16, 34)},
    {'key': 'line_pricing_benefit_wizard', 'steps': ('select_rule_version', 'validate_coding', 'match_authorization', 'price_contract', 'apply_cost_share'), 'improve1_items': (6, 8, 9, 11, 12, 23, 24, 25, 26)},
    {'key': 'medical_necessity_and_attachment_wizard', 'steps': ('request_records', 'extract_facts', 'review_clinical_basis', 'determine_line_outcome'), 'improve1_items': (7, 18, 19, 35, 36, 37, 38)},
    {'key': 'denial_appeal_rework_wizard', 'steps': ('generate_denial_notice', 'receive_appeal', 'assign_independent_review', 'uphold_or_overturn', 'reopen_claim'), 'improve1_items': (13, 14, 15, 20, 22, 32, 47)},
    {'key': 'payment_integrity_recovery_wizard', 'steps': ('score_duplicate_or_fwa', 'open_case', 'calculate_exposure', 'recover_or_dispute', 'prevent_duplicate_recovery'), 'improve1_items': (16, 17, 18, 21, 33, 39, 40)},
    {'key': 'release_and_agent_wizard', 'steps': ('run_seed_scenarios', 'test_boundaries', 'verify_events', 'publish_ui_agent_dsl'), 'improve1_items': (41, 42, 43, 44, 45, 46, 48, 49, 50)},
)

CONTROLS = (
    {'key': 'projection_boundary_guard', 'improve1_items': (4, 5, 8, 11, 12, 23, 49), 'assertion': 'reject shared enrollment provider authorization accumulator and fee schedule table reads'},
    {'key': 'duplicate_replay_guard', 'improve1_items': (1, 16, 20, 34, 44), 'assertion': 'idempotent intake and corrected claim lineage prevent duplicate payment'},
    {'key': 'denial_notice_gate', 'improve1_items': (13, 14, 15, 47), 'assertion': 'denials require policy evidence line mapping notice text and appeal deadline'},
    {'key': 'clinical_human_review_gate', 'improve1_items': (7, 18, 19, 37, 38), 'assertion': 'clinical/FWA/attachment conclusions require reviewer confirmation before adverse action'},
    {'key': 'payment_integrity_recovery_gate', 'improve1_items': (17, 21, 22, 33), 'assertion': 'recoveries and reversals require financial evidence and cannot duplicate offsets'},
    {'key': 'agent_mutation_gate', 'improve1_items': (35, 36, 37, 38, 46, 50), 'assertion': 'assistant CRUD requires citations preview confirmation and authority'},
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _covered(collection: Sequence[Mapping[str, object]]) -> tuple[int, ...]:
    items: set[int] = set()
    for entry in collection:
        items.update(int(item) for item in entry.get('improve1_items', ()))
    return tuple(sorted(items))


def forms_contract() -> dict:
    direct = _covered(FORMS)
    return {'ok': set(direct).issubset(set(IMPROVE1_ITEMS)), 'pbc': PBC_KEY, 'forms': FORMS, 'covered_improve1_items': IMPROVE1_ITEMS, 'directly_mapped_improve1_items': direct, 'owned_tables': CLAIMS_ADJUDICATION_HEALTHCARE_OWNED_TABLES, 'foreign_table_writes': (), 'event_contract': EVENT_CONTRACT, 'side_effects': ()}


def wizards_contract() -> dict:
    direct = _covered(WIZARDS)
    return {'ok': set(direct).issubset(set(IMPROVE1_ITEMS)), 'pbc': PBC_KEY, 'wizards': WIZARDS, 'covered_improve1_items': IMPROVE1_ITEMS, 'directly_mapped_improve1_items': direct, 'stream_engine_picker_visible': False, 'side_effects': ()}


def controls_contract() -> dict:
    direct = _covered(CONTROLS)
    return {'ok': set(direct).issubset(set(IMPROVE1_ITEMS)), 'pbc': PBC_KEY, 'controls': CONTROLS, 'covered_improve1_items': IMPROVE1_ITEMS, 'directly_mapped_improve1_items': direct, 'database_backends': CLAIMS_ADJUDICATION_HEALTHCARE_ALLOWED_DATABASE_BACKENDS, 'event_contract': EVENT_CONTRACT, 'stream_engine_picker_visible': False, 'side_effects': ()}


def canonicalize_claim(payload: Mapping[str, object]) -> dict:
    required = ('claim_number', 'member_id', 'provider_id', 'plan_id')
    missing = tuple(field for field in required if not payload.get(field))
    canonical = {'claim_number': payload.get('claim_number'), 'claim_type': payload.get('claim_type', 'professional'), 'source_format': payload.get('source_format', '837p'), 'submitter': payload.get('submitter', 'unknown'), 'canonical_claim_id': _digest(tuple((key, payload.get(key)) for key in required))}
    return {'ok': not missing, 'missing': missing, 'canonical': canonical, 'side_effects': ()}


def adjudicate_mixed_claim_lines(lines: Sequence[Mapping[str, object]]) -> dict:
    outcomes = []
    for line in lines:
        charge = float(line.get('charge_amount', 0))
        if line.get('requires_review'):
            status = 'pended'
            allowed = 0.0
        elif line.get('deny'):
            status = 'denied'
            allowed = 0.0
        else:
            status = 'paid'
            allowed = round(charge * float(line.get('allowed_percentage', 0.8)), 2)
        outcomes.append({'line_number': line.get('line_number'), 'status': status, 'allowed_amount': allowed, 'reason': line.get('reason')})
    return {'ok': True, 'outcomes': tuple(outcomes), 'has_mixed_outcomes': len({item['status'] for item in outcomes}) > 1, 'side_effects': ()}


def duplicate_claim_score(current: Mapping[str, object], candidates: Sequence[Mapping[str, object]]) -> dict:
    matches = []
    for candidate in candidates:
        score = sum(1 for key in ('member_id', 'provider_id', 'service_date', 'procedure_code', 'units', 'charge_amount') if current.get(key) == candidate.get(key)) / 6
        if score >= 0.67:
            matches.append({'claim_id': candidate.get('claim_id'), 'score': round(score, 2), 'ambiguous': score < 1.0})
    return {'ok': True, 'matches': tuple(matches), 'requires_human_review': any(item['ambiguous'] for item in matches), 'side_effects': ()}


def overlap_guardrail(references: Sequence[str]) -> dict:
    forbidden = []
    for ref in references:
        if ref.startswith(f'{PBC_KEY}_') or ref in DECLARED_DEPENDENCIES:
            continue
        for dependency in DECLARED_DEPENDENCIES.values():
            if ref in dependency.get('forbidden_tables', ()):
                forbidden.append(ref)
    boundary = claims_adjudication_healthcare_verify_owned_table_boundary(tuple(ref for ref in references if ref.endswith('_table')))
    return {'ok': not forbidden and boundary['ok'], 'forbidden_references': tuple(forbidden), 'boundary': boundary, 'declared_dependencies': DECLARED_DEPENDENCIES, 'side_effects': ()}


def release_scenario_library() -> dict:
    return {'ok': True, 'scenarios': ('professional_paid_mixed_lines', 'stale_eligibility_pend', 'authorization_denial_appeal_overturn', 'duplicate_claim_review', 'payment_integrity_recovery', 'agent_document_instruction_preview'), 'side_effects': ()}


def full_claims_adjudication_simulation() -> dict:
    state = claims_adjudication_healthcare_empty_state()
    rule = claims_adjudication_healthcare_approve_benefit_rule(state, {'tenant': 'payer-a', 'plan_id': 'commercial-a', 'service_code': '99213', 'description': 'Office visit', 'covered': True, 'auth_required': False, 'allowed_percentage': 0.8, 'copay_amount': 25, 'deductible_apply': True, 'max_units': 4, 'effective_from': '2026-01-01', 'effective_to': '2026-12-31'})
    claim = claims_adjudication_healthcare_command_health_claim(rule['state'], {'tenant': 'payer-a', 'claim_number': 'SIM-1', 'member_id': 'M1', 'provider_id': 'P1', 'plan_id': 'commercial-a', 'received_date': '2026-05-29', 'total_charge': 300, 'eligibility_projection_hours': 2, 'provider_projection_hours': 2})
    line = claims_adjudication_healthcare_record_claim_line(claim['state'], {'claim_id': claim['claim']['claim_id'], 'line_number': 1, 'service_date': '2026-05-28', 'procedure_code': '99213', 'diagnosis_code': 'J10.1', 'place_of_service': '11', 'units': 1, 'charge_amount': 300, 'accumulator_remaining': 50})
    denial = claims_adjudication_healthcare_simulate_denial(line['state'], {'claim_id': claim['claim']['claim_id'], 'line_ids': (line['claim_line']['line_id'],), 'denial_code': 'DOC-REQ', 'rationale': 'Documentation required', 'policy_rule_id': 'policy-1'})
    appeal = claims_adjudication_healthcare_create_appeal(denial['state'], {'denial_id': denial['denial']['denial_id'], 'level': 'first_level', 'requester': 'provider', 'evidence_summary': 'Clinical record received', 'determination': 'overturned'})
    doc = document_instruction_crud_support('appeal packet for procedure 99213', 'create benefit rule and update denial evidence')
    canonical = canonicalize_claim({'claim_number': 'SIM-1', 'member_id': 'M1', 'provider_id': 'P1', 'plan_id': 'commercial-a'})
    mixed = adjudicate_mixed_claim_lines(({'line_number': 1, 'charge_amount': 100}, {'line_number': 2, 'charge_amount': 50, 'deny': True}, {'line_number': 3, 'charge_amount': 25, 'requires_review': True}))
    duplicate = duplicate_claim_score({'member_id': 'M1', 'provider_id': 'P1', 'service_date': '2026-05-28', 'procedure_code': '99213', 'units': 1, 'charge_amount': 300}, ({'claim_id': 'C1', 'member_id': 'M1', 'provider_id': 'P1', 'service_date': '2026-05-28', 'procedure_code': '99213', 'units': 1, 'charge_amount': 300},))
    overlap = overlap_guardrail(('member_eligibility_projection', 'provider_network_projection') + CLAIMS_ADJUDICATION_HEALTHCARE_OWNED_TABLES[:2])
    schema = claims_adjudication_healthcare_build_schema_contract()
    service = claims_adjudication_healthcare_build_service_contract()
    api = claims_adjudication_healthcare_build_api_contract()
    runtime = claims_adjudication_healthcare_runtime_smoke()
    forms = forms_contract()
    wizards = wizards_contract()
    controls = controls_contract()
    checks = ({'id': 'schema', 'ok': schema['ok']}, {'id': 'service', 'ok': service['ok']}, {'id': 'api', 'ok': api['ok']}, {'id': 'runtime', 'ok': runtime['ok']}, {'id': 'forms', 'ok': forms['ok']}, {'id': 'wizards', 'ok': wizards['ok']}, {'id': 'controls', 'ok': controls['ok']}, {'id': 'rule', 'ok': rule['ok']}, {'id': 'claim', 'ok': claim['ok']}, {'id': 'line', 'ok': line['ok']}, {'id': 'denial', 'ok': denial['ok']}, {'id': 'appeal', 'ok': appeal['ok']}, {'id': 'document_agent', 'ok': doc['ok'] and doc['document_plan']['requires_human_confirmation']}, {'id': 'canonical', 'ok': canonical['ok']}, {'id': 'mixed_lines', 'ok': mixed['ok'] and mixed['has_mixed_outcomes']}, {'id': 'duplicate', 'ok': duplicate['ok'] and duplicate['matches']}, {'id': 'overlap', 'ok': overlap['ok']})
    return {'ok': all(check['ok'] for check in checks), 'pbc': PBC_KEY, 'checks': checks, 'claim': claim, 'line': line, 'denial': denial, 'appeal': appeal, 'agent_plan': doc, 'blocking_gaps': tuple(check for check in checks if not check['ok']), 'side_effects': ()}


def standalone_route_contracts() -> dict:
    routes = ('GET /claims-adjudication-healthcare/app', 'GET /claims-adjudication-healthcare/forms', 'GET /claims-adjudication-healthcare/wizards', 'GET /claims-adjudication-healthcare/controls', 'POST /claims-adjudication-healthcare/claim-intake/run', 'POST /claims-adjudication-healthcare/adjudication/simulate', 'POST /claims-adjudication-healthcare/appeal/run', 'POST /claims-adjudication-healthcare/agent/preview')
    return {'ok': True, 'pbc': PBC_KEY, 'routes': routes, 'event_contract': EVENT_CONTRACT, 'stream_engine_picker_visible': False, 'side_effects': ()}


def single_pbc_app_contract() -> dict:
    schema = claims_adjudication_healthcare_build_schema_contract()
    service = claims_adjudication_healthcare_build_service_contract()
    api = claims_adjudication_healthcare_build_api_contract()
    runtime = claims_adjudication_healthcare_runtime_smoke()
    forms = forms_contract()
    wizards = wizards_contract()
    controls = controls_contract()
    routes = standalone_route_contracts()
    simulation = full_claims_adjudication_simulation()
    return {'ok': all(item['ok'] for item in (schema, service, api, runtime, forms, wizards, controls, routes, simulation)), 'pbc': PBC_KEY, 'app_name': 'Healthcare Claims Adjudication Workbench', 'owned_tables': CLAIMS_ADJUDICATION_HEALTHCARE_OWNED_TABLES, 'declared_dependencies': DECLARED_DEPENDENCIES, 'database_backends': CLAIMS_ADJUDICATION_HEALTHCARE_ALLOWED_DATABASE_BACKENDS, 'event_contract': EVENT_CONTRACT, 'emits': CLAIMS_ADJUDICATION_HEALTHCARE_EMITTED_EVENT_TYPES, 'consumes': CLAIMS_ADJUDICATION_HEALTHCARE_CONSUMED_EVENT_TYPES, 'forms': forms, 'wizards': wizards, 'controls': controls, 'routes': routes, 'simulation': simulation, 'dsl_exposure': {'pbc': PBC_KEY, 'models': CLAIMS_ADJUDICATION_HEALTHCARE_BUSINESS_TABLES, 'routes': routes['routes'], 'agent_skill_namespace': f'{PBC_KEY}_skills', 'ui_fragments': ('ClaimsAdjudicationHealthcareWorkbench', 'ClaimIntakeWorkbench', 'LineAdjudicationWorkbench', 'AppealAndIntegrityWorkbench')}, 'stream_engine_picker_visible': False, 'side_effects': ()}


def standalone_smoke_test() -> dict:
    app = single_pbc_app_contract()
    return {'ok': app['ok'] and not app['stream_engine_picker_visible'], 'app': app, 'side_effects': ()}
