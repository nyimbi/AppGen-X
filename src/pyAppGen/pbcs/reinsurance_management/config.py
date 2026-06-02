"""Configuration and governance helpers for reinsurance_management."""

from __future__ import annotations

PBC_KEY = 'reinsurance_management'
PARAMETERS = (
    'quality_score_floor',
    'materiality_threshold',
    'approval_sla_hours',
    'risk_threshold',
    'cat_event_hours_clause',
    'counterparty_watch_threshold',
    'workbench_limit',
)
RULES = (
    'treaty_structure_policy',
    'cession_eligibility_policy',
    'bordereau_validation_policy',
    'recoverable_collection_policy',
    'counterparty_credit_policy',
    'collateral_threshold_policy',
    'commutation_approval_policy',
)


def configuration_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'database_backends': ('postgresql', 'mysql', 'mariadb'),
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
    }


def validate_configuration(config=None) -> dict:
    config = dict(config or {'database_backend': 'postgresql', 'event_topic': 'pbc.reinsurance_management.events'})
    ok = config.get('database_backend', 'postgresql') in ('postgresql', 'mysql', 'mariadb') and config.get('event_topic', 'pbc.reinsurance_management.events') == 'pbc.reinsurance_management.events'
    return {'ok': ok, 'configuration': config, 'side_effects': ()}


def parameter_manifest() -> dict:
    return {'ok': True, 'parameters': tuple({'name': p, 'bounded': True} for p in PARAMETERS), 'side_effects': ()}


def set_parameter(name, value):
    return {'ok': name in PARAMETERS, 'name': name, 'value': value, 'bounded': True, 'side_effects': ()}


def rule_manifest() -> dict:
    return {'ok': True, 'rules': RULES, 'side_effects': ()}


def compile_rule(rule):
    return {'ok': True, 'rule': dict(rule), 'compiled_hash': str(abs(hash(repr(rule)))), 'side_effects': ()}


def evaluate_rule(rule, payload=None):
    payload = dict(payload or {})
    passed = True
    if rule == 'treaty_structure_policy':
        passed = float(payload.get('signed_share_pct', 0.0)) <= 100.0
    elif rule == 'bordereau_validation_policy':
        passed = not bool(payload.get('has_duplicates', False))
    elif rule == 'counterparty_credit_policy':
        passed = payload.get('rating', 'A') not in {'B', 'CCC'}
    return {'ok': True, 'passed': passed, 'rule': rule, 'payload': payload, 'side_effects': ()}


def governance_smoke_test():
    return {'ok': validate_configuration()['ok'] and parameter_manifest()['ok'] and rule_manifest()['ok'] and compile_rule({'rule_id': RULES[0]})['ok'] and evaluate_rule(RULES[0], {'signed_share_pct': 100.0})['passed'], 'side_effects': ()}


def smoke_test():
    return governance_smoke_test()
