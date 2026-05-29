"""Release evidence aggregation for the cdp_segmentation PBC."""

from __future__ import annotations

from pathlib import Path

from . import agent
from . import events
from . import handlers
from . import permissions
from . import routes
from . import services
from . import ui
from .runtime import cdp_segmentation_build_release_evidence


def build_release_evidence() -> dict:
    """Return aggregated release evidence for this package-local slice."""
    runtime_evidence = cdp_segmentation_build_release_evidence()
    from . import standalone

    package_dir = Path(__file__).resolve().parent
    documentation = {
        'README.md': (package_dir / 'README.md').exists(),
        'implementation-plan.md': (package_dir / 'implementation-plan.md').exists(),
        'implementation-status.md': (package_dir / 'implementation-status.md').exists(),
        'RELEASE_EVIDENCE.md': (package_dir / 'RELEASE_EVIDENCE.md').exists(),
        'SPECIFICATION.md': (package_dir / 'SPECIFICATION.md').exists(),
    }
    tests = {
        'tests/test_contract.py': (package_dir / 'tests' / 'test_contract.py').exists(),
        'tests/test_execution.py': (package_dir / 'tests' / 'test_execution.py').exists(),
        'tests/test_standalone.py': (package_dir / 'tests' / 'test_standalone.py').exists(),
    }
    standalone_contract = standalone.standalone_app_manifest()
    standalone_smoke = standalone.workbench_smoke_test()
    return {
        **runtime_evidence,
        'ui': ui.cdp_segmentation_ui_contract(),
        'events': events.event_contract_manifest(),
        'handlers': handlers.handler_manifest(),
        'routes': routes.api_route_contracts(),
        'service_execution': services.service_operation_manifest(),
        'agent': agent.composed_agent_contribution(),
        'standalone': {
            'contract': standalone_contract,
            'smoke': standalone_smoke,
        },
        'documentation_inventory': documentation,
        'test_inventory': tests,
    }


RELEASE_EVIDENCE = build_release_evidence()


def release_readiness_manifest() -> dict:
    """Return side-effect-free release readiness sections and gate metadata."""
    evidence = build_release_evidence()
    sections = tuple(
        name
        for name in (
            'schema',
            'service',
            'api',
            'permissions',
            'ui',
            'events',
            'handlers',
            'routes',
            'service_execution',
            'agent',
            'standalone',
        )
        if isinstance(evidence.get(name), dict)
    )
    checks = tuple(evidence.get('checks', ()))
    missing_docs = tuple(name for name, present in evidence['documentation_inventory'].items() if not present)
    missing_tests = tuple(name for name, present in evidence['test_inventory'].items() if not present)
    return {
        'ok': evidence.get('ok') is True and bool(checks) and not missing_docs and not missing_tests,
        'pbc': 'cdp_segmentation',
        'format': evidence.get('format'),
        'sections': sections,
        'checks': checks,
        'blocking_gaps': tuple(evidence.get('blocking_gaps', ())),
        'missing_docs': missing_docs,
        'missing_tests': missing_tests,
        'required_sections': ('schema', 'service', 'api', 'permissions', 'ui', 'events', 'agent', 'standalone'),
        'side_effects': (),
    }


def validate_release_evidence() -> dict:
    """Validate release evidence, blocking gaps, and package-local coverage."""
    evidence = build_release_evidence()
    manifest = release_readiness_manifest()
    missing_sections = tuple(section for section in manifest['required_sections'] if section not in manifest['sections'])
    failed_checks = tuple(check for check in manifest['checks'] if check.get('ok') is not True)
    boundary_gaps = tuple(
        gap
        for gap, failed in (
            ('schema_shared_table_access', evidence['schema'].get('shared_table_access') is not False),
            ('service_shared_table_access', evidence['service'].get('shared_table_access') is True),
            ('route_shared_table_access', evidence['routes'].get('ok') is not True),
            ('handler_contract_missing', evidence['handlers'].get('ok') is not True),
            ('standalone_contract_missing', evidence['standalone']['contract'].get('ok') is not True),
            ('standalone_smoke_failed', evidence['standalone']['smoke'].get('ok') is not True),
        )
        if failed
    )
    return {
        'ok': manifest['ok']
        and evidence.get('pbc') == manifest['pbc']
        and not manifest['blocking_gaps']
        and not missing_sections
        and not failed_checks
        and not boundary_gaps,
        'pbc': 'cdp_segmentation',
        'manifest': manifest,
        'missing_sections': missing_sections,
        'failed_checks': failed_checks,
        'boundary_gaps': boundary_gaps,
        'side_effects': (),
    }


def smoke_test() -> dict:
    """Exercise release readiness validation side-effect-free."""
    validation = validate_release_evidence()
    evidence = build_release_evidence()
    return {
        'ok': validation['ok'] and evidence.get('ok') is True,
        'validation': validation,
        'evidence': evidence,
        'side_effects': (),
    }
