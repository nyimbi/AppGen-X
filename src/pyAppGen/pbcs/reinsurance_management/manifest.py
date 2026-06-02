"""Package manifest for the reinsurance_management PBC."""

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES, DOMAIN_BUSINESS_TABLES, PUBLIC_API_ROUTES
from .runtime import (
    REINSURANCE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    REINSURANCE_MANAGEMENT_STANDARD_FEATURE_KEYS,
    REINSURANCE_MANAGEMENT_UI_FRAGMENT_KEYS,
)

PBC_MANIFEST = {
    'pbc': 'reinsurance_management',
    'label': 'Reinsurance Management',
    'mesh': 'finops',
    'version': '1.1.0',
    'template': 'standalone_operations',
    'description': 'Standalone reinsurance operating app for treaties, placements, cessions, recoverables, cat events, statementing, and governed assistant previews',
    'advanced_capabilities': tuple(DOMAIN_ADVANCED_CAPABILITIES),
    'analytics': ('recoverable_aging', 'catastrophe_loss', 'collateral_deficiency', 'statement_balance'),
    'apis': PUBLIC_API_ROUTES,
    'capabilities': REINSURANCE_MANAGEMENT_STANDARD_FEATURE_KEYS + REINSURANCE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    'configuration': (
        'REINSURANCE_MANAGEMENT_DATABASE_URL',
        'REINSURANCE_MANAGEMENT_EVENT_TOPIC',
        'REINSURANCE_MANAGEMENT_RETRY_LIMIT',
        'REINSURANCE_MANAGEMENT_DEFAULT_POLICY',
    ),
    'consumes': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'),
    'datastore_backend': 'postgresql',
    'docs': ('SPECIFICATION.md', 'RELEASE_EVIDENCE.md', 'improve1.md'),
    'emits': (
        'ReinsuranceManagementCreated',
        'ReinsuranceManagementUpdated',
        'ReinsuranceManagementApproved',
        'ReinsuranceManagementExceptionOpened',
    ),
    'migrations': ('migrations/001_initial.sql',),
    'permissions': (
        'reinsurance_management.read',
        'reinsurance_management.create',
        'reinsurance_management.update',
        'reinsurance_management.approve',
        'reinsurance_management.admin',
    ),
    'seed_data': ('seed_data.py',),
    'standard_features': REINSURANCE_MANAGEMENT_STANDARD_FEATURE_KEYS,
    'tables': tuple(table.split('reinsurance_management_', 1)[-1] for table in DOMAIN_BUSINESS_TABLES),
    'tests': ('tests/test_contract.py', 'tests/test_standalone.py'),
    'ui_fragments': REINSURANCE_MANAGEMENT_UI_FRAGMENT_KEYS,
    'workflows': (
        'reinsurance_management_treaty_onboarding',
        'reinsurance_management_cat_event_response',
        'reinsurance_management_cash_call_collection',
        'reinsurance_management_commutation_negotiation',
    ),
}
