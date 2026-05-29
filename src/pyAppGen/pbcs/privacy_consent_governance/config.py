"""Configuration, rules, and parameters for the privacy_consent_governance PBC."""

from __future__ import annotations

PBC_KEY = 'privacy_consent_governance'
REQUIRED_EVENT_TOPIC = 'appgen.privacy_consent_governance.events'
ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
DOMAIN_PARAMETER_SCHEMA = (
    {'key': 'dsar_sla_days', 'scope': 'workflow', 'default': 30, 'minimum': 1, 'maximum': 90},
    {'key': 'consent_reconfirmation_days', 'scope': 'consent', 'default': 365, 'minimum': 30, 'maximum': 730},
    {'key': 'retention_review_days', 'scope': 'retention', 'default': 90, 'minimum': 7, 'maximum': 365},
    {'key': 'cross_border_risk_threshold', 'scope': 'transfers', 'default': 0.7, 'minimum': 0.1, 'maximum': 1.0},
    {'key': 'auto_revocation_guard_days', 'scope': 'consent', 'default': 14, 'minimum': 1, 'maximum': 60},
    {'key': 'workbench_limit', 'scope': 'workbench', 'default': 100, 'minimum': 10, 'maximum': 500},
)
DOMAIN_RULE_SCHEMA = (
    {'rule_id': 'lawful_basis_required', 'scope': 'consent', 'condition': 'lawful_basis_present'},
    {'rule_id': 'purpose_must_exist', 'scope': 'consent', 'condition': 'purpose_registered'},
    {'rule_id': 'cross_border_transfer_needs_assessment', 'scope': 'transfer', 'condition': 'assessment_required'},
    {'rule_id': 'dsar_due_date_enforced', 'scope': 'rights', 'condition': 'due_date_present'},
    {'rule_id': 'erasure_requires_legal_hold_check', 'scope': 'rights', 'condition': 'legal_hold_checked'},
    {'rule_id': 'policy_publication_requires_notice', 'scope': 'policy', 'condition': 'notice_linked'},
)


def configuration_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'database_backends': ALLOWED_DATABASE_BACKENDS,
        'required_event_topic': REQUIRED_EVENT_TOPIC,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'domain_parameter_schema': DOMAIN_PARAMETER_SCHEMA,
        'domain_rule_schema': DOMAIN_RULE_SCHEMA,
        'side_effects': (),
    }


def parameter_manifest() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'parameters': DOMAIN_PARAMETER_SCHEMA, 'side_effects': ()}


def rule_manifest() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'rules': DOMAIN_RULE_SCHEMA, 'side_effects': ()}


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {'database_backend': 'postgresql', 'event_topic': REQUIRED_EVENT_TOPIC})
    ok = (
        config.get('database_backend', 'postgresql') in ALLOWED_DATABASE_BACKENDS
        and config.get('event_topic', REQUIRED_EVENT_TOPIC) == REQUIRED_EVENT_TOPIC
    )
    return {'ok': ok, 'config': config, 'side_effects': ()}


def set_parameter(state: dict | None, key: str, value) -> dict:
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item['key'] == key), None)
    if schema is None:
        return {'ok': False, 'parameter': key, 'value': value, 'reason': 'unknown_parameter', 'side_effects': ()}
    bounded = schema['minimum'] <= value <= schema['maximum'] if isinstance(value, (int, float)) else True
    return {
        'ok': bounded,
        'parameter': key,
        'value': value,
        'parameter_scope': schema['scope'],
        'bounded': bounded,
        'side_effects': (),
    }


def compile_rule(rule: dict) -> dict:
    if 'stream_engine' in rule or 'stream_engine_picker' in rule:
        return {'ok': False, 'compiled': False, 'reason': 'stream_engine_picker_disallowed', 'side_effects': ()}
    allowed = {item['rule_id'] for item in DOMAIN_RULE_SCHEMA}
    rule_id = rule.get('rule_id')
    return {
        'ok': rule_id in allowed,
        'compiled': rule_id in allowed,
        'rule': dict(rule),
        'scope': rule.get('scope'),
        'condition': rule.get('condition'),
        'side_effects': (),
    }


def evaluate_rule(compiled: dict, context: dict | None = None) -> dict:
    context = dict(context or {})
    return {
        'ok': compiled.get('ok') is True,
        'allowed': compiled.get('ok') is True,
        'scope': compiled.get('scope'),
        'context': context,
        'side_effects': (),
    }


def governance_smoke_test() -> dict:
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    parameter = set_parameter({}, 'workbench_limit', 100)
    return {
        'ok': configuration_manifest()['ok']
        and parameter_manifest()['ok']
        and rule_manifest()['ok']
        and evaluate_rule(compiled)['allowed']
        and parameter['ok'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
