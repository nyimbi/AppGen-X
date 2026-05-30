from pyAppGen.pbcs.rail_operations_management.standalone import RailOperationsManagementStandaloneApp, smoke_test, standalone_app_manifest


def test_standalone_app_loads_demo_workspace_and_renders_workbench():
    app = RailOperationsManagementStandaloneApp()
    loaded = app.load_demo_workspace(tenant='tenant_demo')
    rendered = app.render_workbench(tenant='tenant_demo')

    assert loaded['ok'] is True
    assert rendered['ok'] is True
    assert rendered['cards'][0]['value'] >= 1
    assert rendered['assistant_panel']['latest_preview_count'] >= 1
    assert rendered['analytics']['capacity_conflicts'] >= 1
    assert any(item['train_id'] == 'ROM-1001' for item in rendered['dispatch_board'])


def test_standalone_route_dispatch_handles_preview_and_release_snapshot():
    app = RailOperationsManagementStandaloneApp()
    app.bootstrap(tenant='tenant_demo')
    preview = app.dispatch(
        'POST',
        '/api/pbc/rail_operations_management/assistant/document-previews',
        {
            'document': 'Freight bulletin: hold RFX-77 at terminal, review carbon impact, and update SLA watchlist.',
            'instruction': 'Create preview for freight, terminal, carbon, and sla actions',
        },
    )
    snapshot = app.release_snapshot()

    assert preview['ok'] is True
    assert snapshot['ok'] is True
    assert preview['result']['result']['record']['payload']['crud_preview']


def test_standalone_smoke_test_passes():
    result = smoke_test()
    manifest = standalone_app_manifest()

    assert result['ok'] is True
    assert manifest['ok'] is True
    assert manifest['app']['app_id'] == 'rail_operations_management_one_pbc_app'
