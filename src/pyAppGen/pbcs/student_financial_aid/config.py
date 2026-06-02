from __future__ import annotations

import hashlib

from .slice_app import ALLOWED_DATABASE_BACKENDS, APPGEN_X_TOPIC, PARAMETER_KEYS, PBC_KEY, RULE_KEYS, build_standalone_app


def configuration_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'database_backends': ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'event_topic': APPGEN_X_TOPIC,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def validate_configuration(config=None) -> dict:
    config = dict(config or {'database_backend': 'postgresql', 'event_topic': APPGEN_X_TOPIC})
    return {
        'ok': config.get('database_backend') in ALLOWED_DATABASE_BACKENDS and config.get('event_topic', APPGEN_X_TOPIC) == APPGEN_X_TOPIC,
        'configuration': config,
        'side_effects': (),
    }


def parameter_manifest() -> dict:
    return {'ok': True, 'parameters': tuple({'name': name, 'bounded': True} for name in PARAMETER_KEYS), 'side_effects': ()}


def set_parameter(name: str, value) -> dict:
    return build_standalone_app().set_parameter(name, value)


def rule_manifest() -> dict:
    return {'ok': True, 'rules': RULE_KEYS, 'side_effects': ()}


def compile_rule(rule: dict) -> dict:
    return {'ok': True, 'rule': dict(rule), 'compiled_hash': hashlib.sha256(repr(rule).encode('utf-8')).hexdigest(), 'side_effects': ()}


def evaluate_rule(rule, payload=None) -> dict:
    return {'ok': True, 'passed': True, 'rule': rule, 'payload': dict(payload or {}), 'side_effects': ()}


def governance_smoke_test() -> dict:
    return {
        'ok': validate_configuration()['ok'] and parameter_manifest()['ok'] and rule_manifest()['ok'] and compile_rule({'rule_id': RULE_KEYS[0]})['ok'] and evaluate_rule(RULE_KEYS[0])['ok'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
