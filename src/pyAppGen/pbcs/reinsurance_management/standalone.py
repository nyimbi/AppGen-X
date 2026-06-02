"""Standalone one-PBC application surface for reinsurance_management."""

from __future__ import annotations

from . import routes, ui
from .runtime import REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .services import ReinsuranceManagementService

DEFAULT_CONFIGURATION = {
    'database_backend': 'postgresql',
    'event_topic': REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    'retry_limit': 5,
    'default_currency': 'USD',
    'default_hours_clause': 168,
    'workbench_limit': 100,
}
DEFAULT_PARAMETERS = {
    'quality_score_floor': 0.7,
    'materiality_threshold': 500000.0,
    'approval_sla_hours': 24,
    'risk_threshold': 0.65,
    'cat_event_hours_clause': 168,
    'counterparty_watch_threshold': 35.0,
    'workbench_limit': 100,
}
DEFAULT_RULE = {
    'rule_id': 'reinsurance_management.release_readiness',
    'tenant': 'tenant_demo',
    'scope': 'reinsurance_program',
    'status': 'active',
    'credit_policy': {'minimum_rating': 'BBB'},
    'cession_policy': {'require_line_match': True},
    'bordereau_policy': {'reject_duplicates': True},
    'cash_call_policy': {'materiality_threshold': 500000.0},
}


def standalone_app_manifest() -> dict:
    service_manifest = ReinsuranceManagementService().query_service_contract({})['result']
    return {
        'ok': True,
        'pbc': 'reinsurance_management',
        'app': ui.reinsurance_management_standalone_app_contract(),
        'routes': routes.api_route_contracts()['routes'],
        'service': service_manifest,
        'side_effects': (),
    }


class ReinsuranceManagementStandaloneApp:
    def __init__(self, state: dict | None = None):
        self.service = ReinsuranceManagementService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = 'tenant_demo') -> dict:
        self.dispatch('POST', '/api/pbc/reinsurance_management/runtime/configuration', {'configuration': DEFAULT_CONFIGURATION})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch('POST', '/api/pbc/reinsurance_management/runtime/parameters', {'name': name, 'value': value})
        self.dispatch('POST', '/api/pbc/reinsurance_management/runtime/rules', {'rule': {**DEFAULT_RULE, 'tenant': tenant}})
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/events/inbox',
            {
                'envelope': {
                    'event_type': 'PolicyChanged',
                    'event_id': f'policy-{tenant}',
                    'payload': {'tenant': tenant, 'policy_id': 'POL-BASE', 'status': 'active'},
                }
            },
        )
        return {'ok': True, 'tenant': tenant, 'state': self.state, 'side_effects': ()}

    def load_demo_workspace(self, *, tenant: str = 'tenant_demo') -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/counterparties',
            {
                'counterparty': {
                    'counterparty_id': f'CP-{tenant}',
                    'tenant': tenant,
                    'role': 'reinsurer',
                    'rating': 'A',
                    'domicile': 'Bermuda',
                    'signed_share_pct': 35.0,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/exposure-layers',
            {
                'layer': {
                    'layer_id': f'LAYER-{tenant}',
                    'tenant': tenant,
                    'peril': 'windstorm',
                    'attachment_point': 100000.0,
                    'exhaustion_point': 600000.0,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/reinsurance-treaties',
            {
                'treaty': {
                    'treaty_id': f'TRT-{tenant}',
                    'tenant': tenant,
                    'treaty_type': 'catastrophe',
                    'cedant': 'Demo Insurance Co',
                    'effective_from': '2026-01-01',
                    'effective_to': '2026-12-31',
                    'covered_lines': ('property', 'engineering'),
                    'participants': ({'counterparty_id': f'CP-{tenant}', 'signed_share_pct': 35.0},),
                    'layers': ({'layer_id': f'LAYER-{tenant}', 'limit': 500000.0},),
                    'aggregate_limit': 1000000.0,
                    'reinstatements': 1,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/facultative-placements',
            {
                'placement': {
                    'placement_id': f'FAC-{tenant}',
                    'tenant': tenant,
                    'risk_reference': 'PLANT-77',
                    'required_share_pct': 100.0,
                    'signed_lines': ({'counterparty_id': f'CP-{tenant}', 'signed_share_pct': 100.0},),
                    'subjectivities': ({'name': 'engineering_survey', 'satisfied': True},),
                    'quote_terms': ({'market': 'Lead Re', 'rate_on_line': 0.12},),
                    'bind_requested': True,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/cessions',
            {
                'cession': {
                    'cession_id': f'CES-{tenant}',
                    'tenant': tenant,
                    'treaty_id': f'TRT-{tenant}',
                    'layer_id': f'LAYER-{tenant}',
                    'policy_reference': 'POL-123',
                    'line_of_business': 'property',
                    'gross_premium': 900000.0,
                    'gross_loss': 420000.0,
                    'share': 0.35,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/bordereaux',
            {
                'bordereau': {
                    'bordereau_id': f'BOR-{tenant}',
                    'tenant': tenant,
                    'bordereau_type': 'loss',
                    'period': '2026-05',
                    'rows': (
                        {'row_id': '1', 'claim_reference': 'CLM-001', 'ceded_loss': 147000.0},
                        {'row_id': '2', 'claim_reference': 'CLM-002', 'ceded_loss': 21000.0},
                    ),
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/recoverables',
            {
                'recoverable': {
                    'recoverable_id': f'REC-{tenant}',
                    'tenant': tenant,
                    'cession_id': f'CES-{tenant}',
                    'counterparty_id': f'CP-{tenant}',
                    'days_outstanding': 45,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/claim-recoveries',
            {
                'claim_recovery': {
                    'recovery_id': f'CLR-{tenant}',
                    'tenant': tenant,
                    'claim_reference': 'CLM-001',
                    'recoverable_id': f'REC-{tenant}',
                    'required_documents': ('proof_of_loss', 'adjuster_report'),
                    'submitted_documents': ('proof_of_loss', 'adjuster_report'),
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/collateral-positions',
            {
                'collateral': {
                    'collateral_id': f'COL-{tenant}',
                    'tenant': tenant,
                    'counterparty_id': f'CP-{tenant}',
                    'required_amount': 200000.0,
                    'posted_amount': 175000.0,
                    'expiry_date': '2026-12-31',
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/catastrophe-events',
            {
                'event': {
                    'event_id': f'CAT-{tenant}',
                    'tenant': tenant,
                    'peril': 'windstorm',
                    'occurrence_start': '2026-05-01T00:00:00Z',
                    'occurrence_end': '2026-05-03T23:59:59Z',
                    'claims': (
                        {'claim_reference': 'CLM-001', 'gross_loss': 300000.0, 'ceded_estimate': 105000.0},
                        {'claim_reference': 'CLM-002', 'gross_loss': 120000.0, 'ceded_estimate': 42000.0},
                    ),
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/retrocession-programs',
            {
                'retrocession_program': {
                    'retro_program_id': f'RETRO-{tenant}',
                    'tenant': tenant,
                    'source_treaty_id': f'TRT-{tenant}',
                    'retro_share_pct': 0.2,
                    'retro_limit': 300000.0,
                    'protection_basis': 'losses_occurring',
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/statements',
            {
                'statement': {
                    'statement_id': f'STM-{tenant}',
                    'tenant': tenant,
                    'counterparty_id': f'CP-{tenant}',
                    'statement_period': '2026-05',
                    'lines': (
                        {'type': 'loss_recovery', 'amount': 147000.0},
                        {'type': 'commission_offset', 'amount': -12000.0},
                    ),
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/cash-calls',
            {
                'cash_call': {
                    'cash_call_id': f'CC-{tenant}',
                    'tenant': tenant,
                    'statement_id': f'STM-{tenant}',
                    'urgent': True,
                    'due_date': '2026-06-15',
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/commutations',
            {
                'commutation': {
                    'commutation_id': f'COM-{tenant}',
                    'tenant': tenant,
                    'treaty_id': f'TRT-{tenant}',
                    'recoverable_ids': (f'REC-{tenant}',),
                    'negotiated_amount': 130000.0,
                    'approval_state': 'approved',
                    'status': 'settled',
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/reconciliations',
            {
                'reconciliation': {
                    'reconciliation_id': f'RECON-{tenant}',
                    'tenant': tenant,
                    'source_total': 147000.0,
                    'ledger_total': 130000.0,
                    'statement_total': 5000.0,
                }
            },
        )
        self.dispatch(
            'POST',
            '/api/pbc/reinsurance_management/assistant/previews',
            {
                'tenant': tenant,
                'document': 'Catastrophe treaty slip and statement support with cash call instruction.',
                'instruction': 'Create a preview for cash call and statement updates tied to the catastrophe recovery.',
            },
        )
        return {
            'ok': True,
            'tenant': tenant,
            'workbench': self.render_workbench(tenant=tenant),
            'side_effects': (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(ui.reinsurance_management_ui_contract()['action_permissions'].values())
        return ui.reinsurance_management_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def workbench_smoke_test() -> dict:
    app = ReinsuranceManagementStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant='tenant_demo')
    return {
        'ok': loaded['ok'] and rendered['ok'] and rendered['workbench']['cards'][0]['value'] >= 1,
        'manifest': standalone_app_manifest(),
        'loaded': loaded,
        'rendered': rendered,
        'side_effects': (),
    }


def smoke_test() -> dict:
    app = ReinsuranceManagementStandaloneApp()
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
