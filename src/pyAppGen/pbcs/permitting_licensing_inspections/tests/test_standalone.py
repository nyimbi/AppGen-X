"""Standalone app smoke tests for permitting_licensing_inspections."""
from __future__ import annotations

from ..standalone import PermittingLicensingInspectionsStandaloneApp, smoke_test
from ..ui import permitting_licensing_inspections_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = permitting_licensing_inspections_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract['ok'] is True
    assert app_smoke['ok'] is True
    assert contract['forms']
    assert contract['wizards']
    assert contract['controls']


def test_standalone_app_can_bootstrap_render_and_dispatch():
    app = PermittingLicensingInspectionsStandaloneApp()
    rendered = app.render_shell(tenant='tenant_demo')
    assert rendered['ok'] is True
    assert rendered['shell']['app_id'] == 'permitting_licensing_inspections_one_pbc_app'
    assert rendered['workbench']['cards'][0]['value'] >= 1

    route = app.dispatch_route('POST', '/applications', {
        'tenant': 'tenant_demo',
        'application_type': 'business_license',
        'site_address': '99 Trade Avenue',
        'parcel_id': 'PAR-777',
        'responsible_parties': {'applicant': 'Market Owner', 'owner': 'Market Owner'},
        'documents': ('business_registration', 'tax_clearance', 'owner_authorization'),
        'attestations': ('tax_compliance', 'zoning_acknowledgement'),
    })
    assert route['ok'] is True
    workbench = app.workbench(tenant='tenant_demo')
    assert workbench['cards'][0]['value'] >= 2
