from pyAppGen.pbcs.reinsurance_management.runtime import (
    create_reinsurance_treaty,
    record_exposure_layer,
    reinsurance_management_empty_state,
    review_cession,
    approve_bordereau,
)
from pyAppGen.pbcs.reinsurance_management.services import ReinsuranceManagementService
from pyAppGen.pbcs.reinsurance_management.standalone import ReinsuranceManagementStandaloneApp, smoke_test, workbench_smoke_test


def test_standalone_demo_workspace_covers_core_reinsurance_flows():
    app = ReinsuranceManagementStandaloneApp()
    loaded = app.load_demo_workspace(tenant='tenant_demo')
    assert loaded['ok'] is True
    workbench = loaded['workbench']['workbench']
    assert workbench['cards'][0]['value'] >= 1
    assert workbench['queues']['cash_calls']
    recoverable = app.state['records']['reinsurance_management_recoverable']['REC-tenant_demo']
    assert recoverable['status'] == 'commuted'
    collateral = app.state['records']['reinsurance_management_collateral_position']['COL-tenant_demo']
    assert collateral['deficiency_amount'] == 25000.0
    preview = next(iter(app.state['records']['reinsurance_management_assistant_preview'].values()))
    assert 'reinsurance_management_cash_call' in preview['candidate_tables']


def test_domain_calculations_validate_layers_and_duplicates():
    state = reinsurance_management_empty_state()
    treaty = create_reinsurance_treaty(
        state,
        {
            'tenant': 'tenant-smoke',
            'treaty_id': 'TRT-1',
            'treaty_type': 'catastrophe',
            'covered_lines': ('property',),
            'participants': ({'counterparty_id': 'CP-1', 'signed_share_pct': 40.0},),
            'layers': ({'layer_id': 'L1', 'limit': 500000.0},),
            'aggregate_limit': 800000.0,
        },
    )
    layer = record_exposure_layer(
        treaty['state'],
        {'tenant': 'tenant-smoke', 'layer_id': 'L1', 'peril': 'windstorm', 'attachment_point': 100000.0, 'exhaustion_point': 600000.0},
    )
    cession = review_cession(
        layer['state'],
        {
            'tenant': 'tenant-smoke',
            'cession_id': 'CES-1',
            'treaty_id': 'TRT-1',
            'layer_id': 'L1',
            'line_of_business': 'property',
            'gross_premium': 750000.0,
            'gross_loss': 420000.0,
            'share': 0.4,
        },
    )
    assert cession['ok'] is True
    assert cession['record']['ceded_loss'] == 128000.0
    bordereau = approve_bordereau(
        cession['state'],
        {
            'tenant': 'tenant-smoke',
            'bordereau_id': 'BOR-1',
            'rows': (
                {'row_id': '1', 'claim_reference': 'CLM-1', 'ceded_loss': 128000.0},
                {'row_id': '1', 'claim_reference': 'CLM-1', 'ceded_loss': 128000.0},
            ),
        },
    )
    assert bordereau['record']['accepted_rows'] == 1
    assert bordereau['record']['rejected_rows'] == 1
    assert bordereau['record']['submission_status'] == 'requires_review'


def test_service_and_release_smokes_pass():
    service = ReinsuranceManagementService()
    assert service.execute('configure_runtime', {'configuration': {'database_backend': 'postgresql', 'event_topic': 'pbc.reinsurance_management.events'}})['ok'] is True
    assert service.execute('build_workbench_view', {'tenant': 'tenant-smoke'})['ok'] is True
    assert workbench_smoke_test()['ok'] is True
    assert smoke_test()['ok'] is True
