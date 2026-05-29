"""Standalone one-PBC application surface for cdp_segmentation."""

from __future__ import annotations

from . import agent
from . import routes
from . import services
from . import ui
from .runtime import cdp_segmentation_empty_state
from .seed_data import standalone_seed_bundle


def standalone_route_contracts() -> dict:
    contracts = (
        {
            'route_id': 'POST /app/cdp-segmentation/runtime/configuration',
            'method': 'POST',
            'path': '/app/cdp-segmentation/runtime/configuration',
            'operation': 'configure_runtime',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.configure',
            'target_method': 'POST',
            'target_path': '/cdp-segmentation/configuration',
            'form': 'CustomerEventIntakeForm',
            'wizard': None,
        },
        {
            'route_id': 'POST /app/cdp-segmentation/runtime/parameters',
            'method': 'POST',
            'path': '/app/cdp-segmentation/runtime/parameters',
            'operation': 'set_parameter',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.configure',
            'target_method': 'POST',
            'target_path': '/cdp-segmentation/parameters',
            'form': None,
            'wizard': None,
        },
        {
            'route_id': 'POST /app/cdp-segmentation/runtime/rules',
            'method': 'POST',
            'path': '/app/cdp-segmentation/runtime/rules',
            'operation': 'register_rule',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.configure',
            'target_method': 'POST',
            'target_path': '/cdp-segmentation/rules',
            'form': None,
            'wizard': None,
        },
        {
            'route_id': 'POST /app/cdp-segmentation/events',
            'method': 'POST',
            'path': '/app/cdp-segmentation/events',
            'operation': 'ingest_customer_event',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.event.write',
            'target_method': 'POST',
            'target_path': '/events',
            'form': 'CustomerEventIntakeForm',
            'wizard': 'DocumentInstructionWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/profile-properties',
            'method': 'POST',
            'path': '/app/cdp-segmentation/profile-properties',
            'operation': 'upsert_profile_property',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.event.write',
            'target_method': 'POST',
            'target_path': '/profile-properties',
            'form': 'ProfilePropertyForm',
            'wizard': 'AudienceRecoveryWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/segments',
            'method': 'POST',
            'path': '/app/cdp-segmentation/segments',
            'operation': 'define_segment',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.segment.write',
            'target_method': 'POST',
            'target_path': '/segments',
            'form': 'SegmentDefinitionForm',
            'wizard': 'SegmentSimulationWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/segment-rules/parse',
            'method': 'POST',
            'path': '/app/cdp-segmentation/segment-rules/parse',
            'operation': 'parse_segment_rule',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.segment.write',
            'target_method': 'POST',
            'target_path': '/segment-rules/parse',
            'form': 'SegmentRuleDocumentForm',
            'wizard': 'DocumentInstructionWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/segment-evaluations',
            'method': 'POST',
            'path': '/app/cdp-segmentation/segment-evaluations',
            'operation': 'evaluate_segments',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.membership.evaluate',
            'target_method': 'POST',
            'target_path': '/segment-evaluations',
            'form': None,
            'wizard': 'SegmentSimulationWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/segment-activations',
            'method': 'POST',
            'path': '/app/cdp-segmentation/segment-activations',
            'operation': 'activate_segment',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.membership.evaluate',
            'target_method': 'POST',
            'target_path': '/segment-activations',
            'form': None,
            'wizard': 'ActivationReadinessWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/activation-allocations',
            'method': 'POST',
            'path': '/app/cdp-segmentation/activation-allocations',
            'operation': 'allocate_activation',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.membership.evaluate',
            'target_method': 'POST',
            'target_path': '/activation-allocations',
            'form': 'ActivationAllocationForm',
            'wizard': 'ActivationReadinessWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/audience-forecasts',
            'method': 'POST',
            'path': '/app/cdp-segmentation/audience-forecasts',
            'operation': 'forecast_audience',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.analytics.write',
            'target_method': 'POST',
            'target_path': '/audience-forecasts',
            'form': None,
            'wizard': 'ActivationReadinessWizard',
        },
        {
            'route_id': 'POST /app/cdp-segmentation/data-quality-controls',
            'method': 'POST',
            'path': '/app/cdp-segmentation/data-quality-controls',
            'operation': 'run_data_quality_controls',
            'operation_kind': 'command',
            'permission': 'cdp_segmentation.audit',
            'target_method': 'POST',
            'target_path': '/data-quality-controls',
            'form': None,
            'wizard': None,
        },
        {
            'route_id': 'GET /app/cdp-segmentation/workbench',
            'method': 'GET',
            'path': '/app/cdp-segmentation/workbench',
            'operation': 'build_workbench_view',
            'operation_kind': 'query',
            'permission': 'cdp_segmentation.audit',
            'target_method': 'GET',
            'target_path': '/memberships',
            'form': None,
            'wizard': None,
        },
        {
            'route_id': 'GET /app/cdp-segmentation/release-evidence',
            'method': 'GET',
            'path': '/app/cdp-segmentation/release-evidence',
            'operation': 'build_release_evidence',
            'operation_kind': 'query',
            'permission': 'cdp_segmentation.audit',
            'target_method': 'GET',
            'target_path': '/cdp-segmentation/release-evidence',
            'form': None,
            'wizard': None,
        },
        {
            'route_id': 'GET /app/cdp-segmentation/seed-bundle',
            'method': 'GET',
            'path': '/app/cdp-segmentation/seed-bundle',
            'operation': 'standalone_seed_bundle',
            'operation_kind': 'query',
            'permission': 'cdp_segmentation.audit',
            'target_method': None,
            'target_path': None,
            'form': None,
            'wizard': None,
        },
        {
            'route_id': 'POST /app/cdp-segmentation/assistant/document-preview',
            'method': 'POST',
            'path': '/app/cdp-segmentation/assistant/document-preview',
            'operation': 'document_instruction_crud_support',
            'operation_kind': 'query',
            'permission': 'cdp_segmentation.audit',
            'target_method': None,
            'target_path': None,
            'form': 'SegmentRuleDocumentForm',
            'wizard': 'DocumentInstructionWizard',
        },
    )
    return {
        'format': 'appgen.cdp-segmentation-standalone-route-contract.v1',
        'ok': bool(contracts),
        'pbc': 'cdp_segmentation',
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    route_manifest = standalone_route_contracts()
    return {
        'format': 'appgen.cdp-segmentation-standalone-app.v1',
        'ok': route_manifest['ok'] and ui.cdp_segmentation_standalone_app_contract()['ok'],
        'pbc': 'cdp_segmentation',
        'app': ui.cdp_segmentation_standalone_app_contract(),
        'routes': route_manifest['routes'],
        'service': services.service_operation_manifest(),
        'agent': agent.composed_agent_contribution(),
        'seed_bundle': standalone_seed_bundle(),
        'side_effects': (),
    }


class CdpSegmentationStandaloneApp:
    """Package-local standalone app that owns the CDP runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or cdp_segmentation_empty_state()

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return dispatch_standalone_route(method, path, payload, app=self)

    def bootstrap(self, *, tenant: str = 'tenant_demo') -> dict:
        bundle = standalone_seed_bundle(tenant=tenant)
        self.dispatch('POST', '/app/cdp-segmentation/runtime/configuration', bundle['configuration'])
        for name, value in bundle['parameters'].items():
            self.dispatch('POST', '/app/cdp-segmentation/runtime/parameters', {'name': name, 'value': value})
        for rule in bundle['rules']:
            self.dispatch('POST', '/app/cdp-segmentation/runtime/rules', rule)
        self.state['cdp_seed_data'][tenant] = {
            'tenant': tenant,
            'tables': bundle['tables'],
            'row_count': bundle['row_count'],
        }
        return {'ok': True, 'tenant': tenant, 'seed_bundle': bundle, 'state': self.state, 'side_effects': ()}

    def load_demo_workspace(self, *, tenant: str = 'tenant_demo') -> dict:
        self.bootstrap(tenant=tenant)
        for event in (
            {
                'event_id': f'profile_{tenant}',
                'tenant': tenant,
                'customer_id': 'cust_demo',
                'event_type': 'profile',
                'region': 'US',
                'properties': {'customer_id': 'cust_demo', 'email': 'demo@example.com', 'opt_in': True},
            },
            {
                'event_id': f'payment_{tenant}',
                'tenant': tenant,
                'customer_id': 'cust_demo',
                'event_type': 'payment',
                'region': 'US',
                'properties': {'amount': 2400.0, 'currency': 'USD'},
            },
            {
                'event_id': f'shipment_{tenant}',
                'tenant': tenant,
                'customer_id': 'cust_demo',
                'event_type': 'shipment',
                'region': 'US',
                'properties': {'order_id': 'ord_demo'},
            },
            {
                'event_id': f'engagement_{tenant}',
                'tenant': tenant,
                'customer_id': 'cust_demo',
                'event_type': 'engagement',
                'region': 'US',
                'properties': {'clicks': 8, 'session_minutes': 14},
            },
        ):
            self.dispatch('POST', '/app/cdp-segmentation/events', event)
        self.dispatch(
            'POST',
            '/app/cdp-segmentation/profile-properties',
            {
                'property_id': f'consent_{tenant}',
                'tenant': tenant,
                'customer_id': 'cust_demo',
                'name': 'consent_status',
                'value': 'opt_in',
                'source': 'standalone_demo',
            },
        )
        self.dispatch(
            'POST',
            '/app/cdp-segmentation/segments',
            {
                'segment_id': 'seg_demo',
                'tenant': tenant,
                'name': 'High Value Opted-In Buyers',
                'criteria': {'min_payment_value': 1000, 'requires_shipment': True, 'min_engagement': 0.2},
                'status': 'active',
            },
        )
        self.dispatch(
            'POST',
            '/app/cdp-segmentation/segment-rules/parse',
            {
                'rule_text': 'high value audience with shipment and engagement',
                'tenant': tenant,
                'segment_id': 'seg_demo',
            },
        )
        self.dispatch('POST', '/app/cdp-segmentation/segment-evaluations', {'customer_id': 'cust_demo'})
        self.dispatch('POST', '/app/cdp-segmentation/segment-activations', {'segment_id': 'seg_demo'})
        self.dispatch(
            'POST',
            '/app/cdp-segmentation/audience-forecasts',
            {'forecast_id': f'forecast_{tenant}', 'tenant': tenant, 'segment_id': 'seg_demo', 'horizon_days': 30},
        )
        self.dispatch(
            'POST',
            '/app/cdp-segmentation/activation-allocations',
            {'allocation_id': f'alloc_{tenant}', 'tenant': tenant, 'segment_id': 'seg_demo', 'destination': 'notifications', 'budget': 1000},
        )
        self.dispatch('POST', '/app/cdp-segmentation/data-quality-controls', {'tenant': tenant})
        return {
            'ok': True,
            'tenant': tenant,
            'workbench': self.render_workbench(tenant=tenant),
            'side_effects': (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.cdp_segmentation_ui_contract()['action_permissions'].values())))
        return ui.cdp_segmentation_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def assistant_preview(self, document: str, instructions: str, *, payload: dict | None = None) -> dict:
        return agent.document_instruction_crud_support(document, instructions, payload=payload)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    app: CdpSegmentationStandaloneApp | None = None,
) -> dict:
    """Dispatch one standalone-app route to the package-local runtime."""
    manifest = standalone_route_contracts()
    route = next(
        (
            item
            for item in manifest['contracts']
            if item['method'] == method and item['path'] == path
        ),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found', 'side_effects': ()}
    local_app = app or CdpSegmentationStandaloneApp()
    request = dict(payload or {})
    if route['operation'] == 'standalone_seed_bundle':
        result = standalone_seed_bundle(tenant=request.get('tenant', 'tenant_demo'))
        return {'ok': result.get('ok') is True, 'handled': True, 'route': route, 'result': result, 'side_effects': ()}
    if route['operation'] == 'document_instruction_crud_support':
        result = local_app.assistant_preview(
            request.get('document', ''),
            request.get('instructions', ''),
            payload=request.get('payload'),
        )
        return {'ok': result.get('ok') is True, 'handled': True, 'route': route, 'result': result, 'side_effects': ()}
    request['state'] = local_app.state
    dispatched = routes.dispatch_route(route['target_method'], route['target_path'], request)
    next_state = dispatched.get('state')
    if next_state is not None:
        local_app.state = next_state
    return {
        'ok': dispatched.get('ok') is True,
        'handled': True,
        'route': route,
        'result': dispatched,
        'state': local_app.state,
        'side_effects': (),
    }


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = CdpSegmentationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    release_snapshot = app.release_snapshot()
    preview = app.assistant_preview(
        'Retention audience memo',
        'Create a governed segment for high value opted-in buyers.',
    )
    return {
        'ok': loaded['ok']
        and rendered['ok']
        and rendered['workbench']['cards'][0]['value'] >= 1
        and preview['ok']
        and release_snapshot['ok'],
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'preview': preview,
        'release_snapshot': release_snapshot,
        'side_effects': (),
    }


def workbench_smoke_test() -> dict:
    """Exercise bootstrap, route dispatch, and rendering without release recursion."""
    app = CdpSegmentationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    preview = dispatch_standalone_route(
        'POST',
        '/app/cdp-segmentation/assistant/document-preview',
        {
            'document': 'Audience growth memo',
            'instructions': 'Create the owned-table preview for a new segment.',
        },
        app=app,
    )
    return {
        'ok': loaded['ok'] and rendered['ok'] and preview['ok'] and rendered['workbench']['cards'][0]['value'] >= 1,
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'preview': preview,
        'side_effects': (),
    }
