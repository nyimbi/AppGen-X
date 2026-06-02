PBC_KEY = 'environment_health_safety'
"""Package manifest for the environment_health_safety PBC."""

from .standalone import build_manifest

PBC_MANIFEST = build_manifest()


STANDARD_FEATURES = tuple(PBC_MANIFEST.get('standard_features', ()))
ADVANCED_CAPABILITIES = tuple(PBC_MANIFEST.get('advanced_capabilities', ()))
# Source-audit fields: standard_features and advanced_capabilities are materialized by build_manifest().
