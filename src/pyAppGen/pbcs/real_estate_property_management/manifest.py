"""Package manifest for the real_estate_property_management PBC."""
from .standalone import PBC_MANIFEST as PBC_MANIFEST

PBC_KEY_LITERAL = 'real_estate_property_management'
# standard_features and advanced_capabilities are materialized in PBC_MANIFEST.
STANDARD_FEATURES = PBC_MANIFEST['standard_features']
ADVANCED_CAPABILITIES = PBC_MANIFEST['advanced_capabilities']
