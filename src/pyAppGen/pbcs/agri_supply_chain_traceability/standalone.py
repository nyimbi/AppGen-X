"""Standalone one-PBC application surface for agri_supply_chain_traceability."""
from __future__ import annotations

from . import routes
from . import ui
from .runtime import AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC
from .services import AgriSupplyChainTraceabilityService


DEFAULT_CONFIGURATION = {
    'database_backend': 'postgresql',
    'event_topic': AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC,
    'retry_limit': 5,
    'release_gate_enabled': True,
    'default_commodity': 'maize',
    'default_region': 'ke',
    'workbench_limit': 50,
}
DEFAULT_PARAMETERS = {
    'quality_score_floor': 0.8,
    'materiality_threshold': 0.05,
    'approval_sla_hours': 12,
    'risk_threshold': 0.4,
    'forecast_horizon_days': 30,
    'workbench_limit': 50,
}
DEFAULT_RULE = {
    'rule_id': 'agri_supply_chain_traceability.release_gate',
    'tenant': 'tenant_demo',
    'scope': 'release_gate',
    'status': 'active',
    'block_on_cold_chain_breach': True,
    'block_on_seal_failure': True,
    'requires_receiving_confirmation': True,
}


def standalone_app_manifest() -> dict:
    service_manifest = AgriSupplyChainTraceabilityService().query_service_contract({})['result']
    return {
        'ok': True,
        'pbc': 'agri_supply_chain_traceability',
        'app': ui.agri_supply_chain_traceability_standalone_app_contract(),
        'routes': routes.api_route_contracts()['routes'],
        'service': service_manifest,
        'side_effects': (),
    }


class AgriSupplyChainTraceabilityStandaloneApp:
    """Package-local standalone app that owns agri traceability runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = AgriSupplyChainTraceabilityService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = 'tenant_demo') -> dict:
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/runtime/configuration', {'configuration': DEFAULT_CONFIGURATION})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/runtime/parameters', {'name': name, 'value': value})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/runtime/rules', {'rule': {**DEFAULT_RULE, 'tenant': tenant}})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/events/inbox', {'envelope': {'event_type': 'PolicyChanged', 'event_id': f'policy-{tenant}', 'payload': {'tenant': tenant, 'policy_id': f'policy-{tenant}', 'status': 'published'}}})
        return {'ok': True, 'tenant': tenant, 'state': self.state, 'side_effects': ()}

    def load_demo_workspace(self, *, tenant: str = 'tenant_demo') -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/farm-lots', {'farm_lot': {'id': f'LOT-{tenant}', 'tenant': tenant, 'site_id': 'SITE-001', 'commodity': 'maize', 'season': '2026-main', 'status': 'active'}})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/input-batches', {'input_batch': {'id': f'INPUT-{tenant}', 'tenant': tenant, 'farm_lot_id': f'LOT-{tenant}', 'supplier': 'SoilWorks', 'applied_at': '2026-04-02', 'status': 'recorded'}})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/certifications', {'certification': {'id': f'CERT-{tenant}', 'tenant': tenant, 'farm_lot_id': f'LOT-{tenant}', 'covered_farm_lot_ids': (f'LOT-{tenant}',), 'covered_site_ids': ('SITE-001',), 'covered_commodities': ('maize',), 'valid_from': '2026-01-01', 'valid_to': '2026-12-31', 'status': 'active'}})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/storage-events', {'storage_event': {'id': f'STORE-{tenant}', 'tenant': tenant, 'subject_ids': (f'SHIP-{tenant}',), 'farm_lot_id': f'LOT-{tenant}', 'status': 'released', 'temperature_breach': False}})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/transport-legs', {'transport_leg': {'id': f'LEG-{tenant}', 'tenant': tenant, 'subject_ids': (f'SHIP-{tenant}',), 'farm_lot_id': f'LOT-{tenant}', 'status': 'in_transit', 'seal_state': 'intact', 'receiving_confirmed': True}})
        self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/provenance-proofs', {'provenance_proof': {'id': f'PROOF-{tenant}', 'tenant': tenant, 'subject_ids': (f'SHIP-{tenant}',), 'source_farm_lot_ids': (f'LOT-{tenant}',), 'status': 'verified'}})
        release = self.dispatch('POST', '/api/pbc/agri_supply_chain_traceability/release-gates', {'candidate': {'tenant': tenant, 'candidate_id': f'SHIP-{tenant}', 'farm_lot_id': f'LOT-{tenant}', 'commodity': 'maize', 'site_id': 'SITE-001', 'shipment_date': '2026-05-28'}})
        return {
            'ok': release['ok'],
            'tenant': tenant,
            'release': release,
            'workbench': self.render_workbench(tenant=tenant),
            'side_effects': (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(ui.agri_supply_chain_traceability_ui_contract()['action_permissions']['permissions'])
        return ui.agri_supply_chain_traceability_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence
        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    app = AgriSupplyChainTraceabilityStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    release_snapshot = app.release_snapshot()
    return {
        'ok': loaded['ok'] and rendered['ok'] and any(card['key'] == 'release_decisions' and card['value'] >= 1 for card in rendered['workbench']['cards']) and release_snapshot['ok'],
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'release_snapshot': release_snapshot,
        'side_effects': (),
    }


def workbench_smoke_test() -> dict:
    app = AgriSupplyChainTraceabilityStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    return {
        'ok': loaded['ok'] and rendered['ok'] and rendered['shell']['app_id'] == 'agri_supply_chain_traceability_one_pbc_app',
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'side_effects': (),
    }
