"""Configuration, rules, and parameters for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import ALLOWED_DATABASE_BACKENDS, APPGEN_X_TOPIC, PARAMETER_DEFINITIONS, PBC_KEY, RULE_DEFINITIONS
from .slice_app import build_configuration_contract, build_standalone_app

DOMAIN_PARAMETER_SCHEMA = tuple(PARAMETER_DEFINITIONS)
DOMAIN_RULE_SCHEMA = tuple(RULE_DEFINITIONS)


def configuration_manifest() -> dict:
    return build_configuration_contract()


def parameter_manifest() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'parameters': DOMAIN_PARAMETER_SCHEMA, 'side_effects': ()}


def rule_manifest() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'rules': DOMAIN_RULE_SCHEMA, 'side_effects': ()}


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {'database_backend': 'postgresql', 'event_topic': APPGEN_X_TOPIC})
    ok = config.get('database_backend') in ALLOWED_DATABASE_BACKENDS and config.get('event_topic', APPGEN_X_TOPIC) == APPGEN_X_TOPIC
    return {'ok': ok, 'config': config, 'side_effects': ()}


def set_parameter(state: dict, key: str, value):
    app = build_standalone_app()
    return app.set_parameter(key, value)


def compile_rule(rule: dict) -> dict:
    if 'stream_engine' in rule or 'stream_engine_picker' in rule:
        return {'ok': False, 'compiled': False, 'reason': 'stream_engine_picker_disallowed', 'side_effects': ()}
    compiled = {**dict(rule), 'compiled': True, 'event_contract': 'AppGen-X'}
    return {'ok': True, 'compiled': True, 'rule': compiled, 'scope': rule.get('scope'), 'condition': rule.get('condition'), 'side_effects': ()}


def evaluate_rule(compiled: dict, context: dict | None = None) -> dict:
    return {'ok': compiled.get('ok', True) is True, 'allowed': compiled.get('ok', True) is True, 'scope': compiled.get('scope'), 'context': dict(context or {}), 'side_effects': ()}


def governance_smoke_test() -> dict:
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    return {
        'ok': configuration_manifest()['ok'] and parameter_manifest()['ok'] and rule_manifest()['ok'] and evaluate_rule(compiled)['allowed'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
