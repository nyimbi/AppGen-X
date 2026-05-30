"""Package manifest for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import (
    ADVANCED_CAPABILITIES,
    BUSINESS_TABLE_BLUEPRINTS,
    CONSUMED_EVENTS,
    EMITTED_EVENTS,
    ROUTE_DEFINITIONS,
    STANDARD_FEATURES,
    UI_FRAGMENTS,
    PBC_KEY,
)

PBC_MANIFEST = {
    'pbc': PBC_KEY,
    'label': 'Sustainability ESG Reporting',
    'mesh': 'finops',
    'description': 'Standalone sustainability and ESG reporting package with materiality, facility activity data, Scope 1/2/3 calculations, renewable claims, disclosure packets, assurance evidence, board packs, regulator filings, and governed AI previews.',
    'version': '1.0.0',
    'datastore_backend': 'postgresql',
    'tables': tuple(item.logical_name for item in BUSINESS_TABLE_BLUEPRINTS),
    'apis': tuple(f"{route['method']} {route['path']}" for route in ROUTE_DEFINITIONS),
    'emits': tuple(EMITTED_EVENTS),
    'consumes': tuple(CONSUMED_EVENTS),
    'template': 'reporting',
    'ui_fragments': UI_FRAGMENTS,
    'permissions': (
        'sustainability_esg_reporting.read',
        'sustainability_esg_reporting.create',
        'sustainability_esg_reporting.update',
        'sustainability_esg_reporting.approve',
        'sustainability_esg_reporting.admin',
        'sustainability_esg_reporting.operate',
    ),
    'configuration': (
        'SUSTAINABILITY_ESG_REPORTING_DATABASE_URL',
        'SUSTAINABILITY_ESG_REPORTING_EVENT_TOPIC',
        'SUSTAINABILITY_ESG_REPORTING_RETRY_LIMIT',
        'SUSTAINABILITY_ESG_REPORTING_DEFAULT_POLICY',
    ),
    'migrations': ('migrations/001_initial.sql',),
    'seed_data': ('seed_data.py',),
    'tests': ('tests/test_contract.py',),
    'docs': ('SPECIFICATION.md', 'RELEASE_EVIDENCE.md', 'improve1.md'),
    'capabilities': tuple(STANDARD_FEATURES) + tuple(ADVANCED_CAPABILITIES),
    'standard_features': tuple(STANDARD_FEATURES),
    'advanced_capabilities': tuple(ADVANCED_CAPABILITIES),
    'workflows': (
        'materiality_assessment_workflow',
        'scope_boundary_workflow',
        'disclosure_packet_workflow',
        'board_pack_and_regulator_filing_workflow',
    ),
    'analytics': (
        'sustainability_esg_reporting_quality_score',
        'sustainability_esg_reporting_target_progress',
        'sustainability_esg_reporting_scope_totals',
        'sustainability_esg_reporting_assurance_readiness',
    ),
}
