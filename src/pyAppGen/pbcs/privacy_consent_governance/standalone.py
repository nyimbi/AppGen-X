"""Standalone one-PBC application surface for privacy_consent_governance."""

from __future__ import annotations

from . import routes
from . import ui
from .runtime import PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC
from .seed_data import seed_bundle
from .services import PrivacyConsentGovernanceService

DEFAULT_CONFIGURATION = {
    'database_backend': 'postgresql',
    'event_topic': PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
    'retry_limit': 5,
    'default_policy_family': 'global-privacy',
    'workbench_limit': 100,
}
DEFAULT_PARAMETERS = {
    'dsar_sla_days': 30,
    'consent_reconfirmation_days': 365,
    'retention_review_days': 90,
    'cross_border_risk_threshold': 0.7,
    'auto_revocation_guard_days': 14,
    'workbench_limit': 100,
}
DEFAULT_RULE = {
    'rule_id': 'lawful_basis_required',
    'scope': 'consent',
    'condition': 'lawful_basis_present',
    'status': 'active',
}


def standalone_app_manifest() -> dict:
    service_manifest = PrivacyConsentGovernanceService().query_service_contract({})['result']
    return {
        'ok': True,
        'pbc': 'privacy_consent_governance',
        'app': ui.privacy_consent_governance_standalone_app_contract(),
        'routes': routes.api_route_contracts()['routes'],
        'service': service_manifest,
        'side_effects': (),
    }


class PrivacyConsentGovernanceStandaloneApp:
    def __init__(self, state: dict | None = None):
        self.service = PrivacyConsentGovernanceService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = 'tenant_demo') -> dict:
        self.dispatch('POST', '/api/pbc/privacy_consent_governance/runtime/configuration', {'configuration': DEFAULT_CONFIGURATION})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch('POST', '/api/pbc/privacy_consent_governance/runtime/parameters', {'name': name, 'value': value})
        rule = {**DEFAULT_RULE, 'tenant': tenant}
        self.dispatch('POST', '/api/pbc/privacy_consent_governance/runtime/rules', {'rule': rule})
        self.dispatch(
            'POST',
            '/api/pbc/privacy_consent_governance/events/inbox',
            {'envelope': {'event_type': 'IdentityVerified', 'event_id': f'identity-{tenant}', 'payload': {'tenant': tenant, 'subject_identifier': f'customer-{tenant}'}}},
        )
        return {'ok': True, 'tenant': tenant, 'state': self.state, 'side_effects': ()}

    def load_demo_workspace(self, *, tenant: str = 'tenant_demo') -> dict:
        self.bootstrap(tenant=tenant)
        for entry in seed_bundle(tenant):
            self.dispatch(entry['method'], entry['path'], entry['payload'])
        self.dispatch(
            'POST',
            '/api/pbc/privacy_consent_governance/consents/revoke',
            {
                'record': {
                    'id': f'revocation-{tenant}',
                    'tenant': tenant,
                    'code': f'REVOCATION-{tenant}',
                    'consent_capture_id': f'consent-{tenant}',
                    'revocation_reason': 'user_preference_change',
                }
            },
        )
        return {'ok': True, 'tenant': tenant, 'workbench': self.render_workbench(tenant=tenant), 'side_effects': ()}

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or ('privacy_consent_governance.read', 'privacy_consent_governance.create', 'privacy_consent_governance.update', 'privacy_consent_governance.approve', 'privacy_consent_governance.admin')
        return ui.privacy_consent_governance_render_workbench(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    app = PrivacyConsentGovernanceStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    release_snapshot = app.release_snapshot()
    return {
        'ok': loaded['ok'] and rendered['ok'] and rendered['workbench']['cards'][0]['value'] >= 1 and release_snapshot['ok'],
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'release_snapshot': release_snapshot,
        'side_effects': (),
    }


def workbench_smoke_test() -> dict:
    app = PrivacyConsentGovernanceStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    return {
        'ok': loaded['ok'] and rendered['ok'] and rendered['workbench']['cards'][0]['value'] >= 1,
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'side_effects': (),
    }
