"""Standalone one-PBC application surface for rail_operations_management."""

from __future__ import annotations

from . import routes, ui
from .runtime import DEFAULT_CONFIGURATION, DEFAULT_PARAMETERS, DEFAULT_RULE
from .services import RailOperationsManagementService


def standalone_app_manifest() -> dict:
    service_manifest = RailOperationsManagementService().query_service_contract({})['result']
    return {
        'ok': True,
        'pbc': 'rail_operations_management',
        'app': ui.rail_operations_management_standalone_app_contract(),
        'routes': routes.api_route_contracts()['routes'],
        'service': service_manifest,
        'side_effects': (),
    }


class RailOperationsManagementStandaloneApp:
    """Package-local standalone app that owns the rail operations runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = RailOperationsManagementService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = 'tenant_demo') -> dict:
        self.dispatch('POST', '/api/pbc/rail_operations_management/runtime/configuration', {'configuration': DEFAULT_CONFIGURATION})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch('POST', '/api/pbc/rail_operations_management/runtime/parameters', {'name': name, 'value': value})
        self.dispatch('POST', '/api/pbc/rail_operations_management/runtime/rules', {'rule': {**DEFAULT_RULE, 'tenant': tenant}})
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/events/inbox',
            {
                'envelope': {
                    'event_type': 'PolicyChanged',
                    'event_id': f'policy-{tenant}',
                    'payload': {'tenant': tenant, 'policy_id': 'daily-rail', 'scope': 'network_control'},
                }
            },
        )
        return {'ok': True, 'tenant': tenant, 'state': self.state, 'side_effects': ()}

    def load_demo_workspace(self, *, tenant: str = 'tenant_demo') -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/train-plans',
            {
                'tenant': tenant,
                'train_id': 'ROM-1001',
                'code': 'ROM-1001',
                'service_type': 'passenger',
                'corridor': 'Northern Corridor',
                'line_id': 'NOR-1',
                'path_id': 'PATH-1001',
                'published_departure_at': '2026-05-30T05:00:00+00:00',
                'working_departure_at': '2026-05-30T05:05:00+00:00',
                'control_departure_at': '2026-05-30T05:07:00+00:00',
                'published_arrival_at': '2026-05-30T07:45:00+00:00',
                'station_calls': ('NBI', 'A104', 'JCT', 'ELD'),
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/route-paths',
            {
                'tenant': tenant,
                'path_id': 'PATH-1001',
                'code': 'PATH-1001',
                'line_id': 'NOR-1',
                'primary_path': ('NBI-A104', 'A104-JCT', 'JCT-ELD'),
                'fallback_paths': (('NBI-BYP', 'BYP-JCT', 'JCT-ELD'),),
                'junctions': ('A104', 'JCT'),
                'headway_minutes': 5,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/consists',
            {
                'tenant': tenant,
                'consist_id': 'CONS-1001',
                'code': 'CONS-1001',
                'train_id': 'ROM-1001',
                'locomotive_class': 'EMU-12',
                'vehicle_order': ('EMU-12A', 'EMU-12B', 'EMU-12C'),
                'length_meters': 186,
                'seats': 812,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/rolling-stock',
            {
                'tenant': tenant,
                'record_id': 'RS-EMU-12A',
                'code': 'EMU-12A',
                'fleet_type': 'electric_multiple_unit',
                'status': 'available',
                'depot': 'NBI',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/crew-assignments',
            {
                'tenant': tenant,
                'assignment_id': 'CREW-1001',
                'code': 'CREW-1001',
                'train_id': 'ROM-1001',
                'driver_id': 'DRV-77',
                'conductor_id': 'COND-44',
                'remaining_legal_minutes': 320,
                'handover_station': 'JCT',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/dispatch-decisions',
            {
                'tenant': tenant,
                'decision_id': 'DEC-1001',
                'code': 'DEC-1001',
                'train_id': 'ROM-1001',
                'selected_action': 'hold_for_path_clearance',
                'hold_reason': 'junction_conflict',
                'approved_by': 'desk-chief',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/signal-restrictions',
            {
                'tenant': tenant,
                'restriction_id': 'SIG-101',
                'code': 'SIG-101',
                'line_id': 'NOR-1',
                'start_point': 'A104',
                'end_point': 'JCT',
                'restriction_type': 'approach_locking',
                'severity': 'medium',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/track-restrictions',
            {
                'tenant': tenant,
                'restriction_id': 'TRK-201',
                'code': 'TRK-201',
                'line_id': 'NOR-1',
                'start_point': 'JCT',
                'end_point': 'ELD',
                'restriction_type': 'temporary_speed_restriction',
                'severity': 'medium',
                'speed_limit_kph': 45,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/yard-plans',
            {
                'tenant': tenant,
                'yard_plan_id': 'YARD-51',
                'code': 'YARD-51',
                'origin_track': 'Y1',
                'destination_track': 'DEP-3',
                'propelling_move': True,
                'ground_staff_confirmed': True,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/terminal-slots',
            {
                'tenant': tenant,
                'slot_id': 'TERM-22',
                'code': 'TERM-22',
                'terminal_id': 'ELD',
                'platform_id': 'P2',
                'occupation_start_at': '2026-05-30T07:40:00+00:00',
                'occupation_end_at': '2026-05-30T08:05:00+00:00',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/maintenance-windows',
            {
                'tenant': tenant,
                'record_id': 'MW-77',
                'code': 'MW-77',
                'line_id': 'NOR-1',
                'blocked_tracks': ('UP-MAIN',),
                'window_start_at': '2026-05-30T06:15:00+00:00',
                'window_end_at': '2026-05-30T06:45:00+00:00',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/delays',
            {
                'tenant': tenant,
                'record_id': 'DLY-1001',
                'code': 'DLY-1001',
                'train_id': 'ROM-1001',
                'delay_minutes': 11,
                'cause_code': 'junction_conflict',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/disruptions',
            {
                'tenant': tenant,
                'record_id': 'DIS-1001',
                'code': 'DIS-1001',
                'severity': 'high',
                'location': 'JCT',
                'affected_trains': ('ROM-1001',),
                'status': 'active',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/passenger-service-plans',
            {
                'tenant': tenant,
                'plan_id': 'PSP-1001',
                'code': 'PSP-1001',
                'service_type': 'passenger',
                'impacted_trains': ('ROM-1001',),
                'playbook': 'skip_stop_recovery',
                'approval_state': 'approved',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/freight-service-plans',
            {
                'tenant': tenant,
                'plan_id': 'FSP-77',
                'code': 'FSP-77',
                'service_type': 'freight',
                'impacted_trains': ('RFX-77',),
                'playbook': 're-slot_after_passenger_peak',
                'approval_state': 'pending',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/safety-rules',
            {
                'tenant': tenant,
                'record_id': 'SAFE-01',
                'code': 'SAFE-01',
                'rule_family': 'yard_propelling',
                'status': 'active',
                'requires_ground_staff_confirmation': True,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/incident-responses',
            {
                'tenant': tenant,
                'incident_id': 'INC-1001',
                'code': 'INC-1001',
                'severity': 'high',
                'location': 'JCT',
                'protection_state': 'blocked_and_protected',
                'handover_summary': 'Crew, dispatch, and maintenance desks aligned on controlled recovery.',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/capacity-conflicts',
            {
                'tenant': tenant,
                'record_id': 'CC-301',
                'code': 'CC-301',
                'train_id': 'ROM-1001',
                'conflict_type': 'junction_headway',
                'severity': 'high',
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/energy-profiles',
            {
                'tenant': tenant,
                'record_id': 'ENG-1001',
                'code': 'ENG-1001',
                'train_id': 'ROM-1001',
                'energy_kwh': 1840,
                'carbon_kg': 265,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/sla-snapshots',
            {
                'tenant': tenant,
                'record_id': 'SLA-1001',
                'code': 'SLA-1001',
                'service_group': 'commuter_peak',
                'status': 'breach',
                'reliability_score': 0.83,
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/rail_operations_management/assistant/document-previews',
            {
                'document': 'Control circular: adjust ROM-1001, hold at JCT, protect maintenance limits, brief passenger and freight desks.',
                'instruction': f'Create governed preview for tenant {tenant} dispatch, maintenance, and service recovery actions',
            },
        )
        return {'ok': True, 'tenant': tenant, 'workbench': self.render_workbench(tenant=tenant), 'side_effects': ()}

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.rail_operations_management_ui_contract()['action_permissions'].values())))
        return ui.rail_operations_management_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    app = RailOperationsManagementStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    release_snapshot = app.release_snapshot()
    return {
        'ok': loaded['ok'] and rendered['ok'] and rendered['cards'][0]['value'] >= 1 and release_snapshot['ok'],
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'release_snapshot': release_snapshot,
        'side_effects': (),
    }
