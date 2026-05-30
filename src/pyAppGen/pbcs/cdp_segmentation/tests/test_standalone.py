"""Standalone app smoke tests for cdp_segmentation."""

from __future__ import annotations

from ..agent import document_instruction_crud_support
from ..standalone import CdpSegmentationStandaloneApp
from ..standalone import dispatch_standalone_route
from ..standalone import smoke_test
from ..standalone import standalone_app_manifest
from ..standalone import standalone_route_contracts
from ..ui import cdp_segmentation_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = cdp_segmentation_standalone_app_contract()
    route_manifest = standalone_route_contracts()
    app_manifest = standalone_app_manifest()
    app_smoke = smoke_test()
    assert contract['ok'] is True
    assert route_manifest['ok'] is True
    assert app_manifest['ok'] is True
    assert app_smoke['ok'] is True
    assert contract['forms']
    assert contract['wizards']
    assert contract['controls']
    assert any(route.endswith('/assistant/document-preview') for route in contract['service_routes'])


def test_standalone_app_can_bootstrap_render_and_preview_document_mutations():
    app = CdpSegmentationStandaloneApp()
    app.load_demo_workspace(tenant='tenant_standalone')
    rendered = app.render_workbench(tenant='tenant_standalone')
    preview = app.assistant_preview(
        'Create a consent-safe retention audience for high value buyers.',
        'Draft the governed mutation preview and show the target owned table.',
    )
    route_preview = dispatch_standalone_route(
        'POST',
        '/app/cdp-segmentation/assistant/document-preview',
        {
            'document': 'Escalate a profile conflict for review.',
            'instructions': 'Prepare the preview for resolving the audience exception.',
        },
        app=app,
    )
    release = app.release_snapshot()

    assert rendered['ok'] is True
    assert rendered['shell']['app_id'] == 'cdp_segmentation_one_pbc_app'
    assert rendered['workbench']['cards'][0]['value'] >= 1
    assert preview['ok'] is True
    assert preview['preferred_route']
    assert preview['mutation_preview']['boundary']['ok'] is True
    assert route_preview['ok'] is True
    assert route_preview['result']['preferred_operation'] == 'resolve_audience_exception'
    assert release['ok'] is True
    assert release['standalone']['contract']['ok'] is True
    assert release['standalone']['smoke']['ok'] is True


def test_document_instruction_support_targets_owned_tables_only():
    support = document_instruction_crud_support(
        'Audience rule memo',
        'Create a segment rule for shipment-backed high value customers.',
    )
    assert support['ok'] is True
    assert support['document_plan']['target_table'] == 'cdp_segmentation_segment_rule'
    assert support['crud_plan']['table'] == 'cdp_segmentation_segment_rule'
    assert support['mutation_preview']['boundary']['ok'] is True
