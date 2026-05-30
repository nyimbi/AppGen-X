"""Owned model metadata for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .slice_app import build_models_contract

_MODELS = build_models_contract()
OWNED_SCHEMA = _MODELS['schema']
MODELS = _MODELS['models']


def build_models_manifest() -> dict:
    return build_models_contract()


def validate_models_manifest() -> dict:
    manifest = build_models_contract()
    return {
        'ok': manifest['ok'] and len(manifest['models']) >= 24,
        'manifest': manifest,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return validate_models_manifest()
