"""Seed bundle for the privacy_consent_governance PBC."""

from __future__ import annotations

from .models import OWNED_TABLES, PBC_KEY


def seed_bundle(tenant: str = 'tenant_demo') -> tuple[dict, ...]:
    return (
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/data-subjects',
            'payload': {
                'record': {
                    'id': f'subject-{tenant}',
                    'tenant': tenant,
                    'code': f'SUBJECT-{tenant}',
                    'subject_identifier': f'customer-{tenant}',
                    'region': 'KE',
                    'email': f'{tenant}@example.com',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/processing-purposes',
            'payload': {
                'record': {
                    'id': f'purpose-{tenant}',
                    'tenant': tenant,
                    'code': 'MARKETING_EMAIL',
                    'data_category': 'contact',
                    'purpose_owner': 'marketing',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/lawful-bases',
            'payload': {
                'record': {
                    'id': f'basis-{tenant}',
                    'tenant': tenant,
                    'code': 'CONSENT',
                    'purpose_code': 'MARKETING_EMAIL',
                    'jurisdiction': 'KE',
                    'basis_type': 'consent',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/consents/capture',
            'payload': {
                'record': {
                    'id': f'consent-{tenant}',
                    'tenant': tenant,
                    'code': f'CONSENT-{tenant}',
                    'data_subject_id': f'subject-{tenant}',
                    'purpose_code': 'MARKETING_EMAIL',
                    'lawful_basis_code': 'CONSENT',
                    'channel': 'email',
                    'consent_state': 'granted',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/preferences',
            'payload': {
                'record': {
                    'id': f'preference-{tenant}',
                    'tenant': tenant,
                    'code': f'PREFERENCE-{tenant}',
                    'data_subject_id': f'subject-{tenant}',
                    'channel': 'email',
                    'preference_state': 'opt_in',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/policy-versions',
            'payload': {
                'record': {
                    'id': f'policy-{tenant}',
                    'tenant': tenant,
                    'code': f'POLICY-{tenant}',
                    'notice_id': f'notice-{tenant}',
                    'version_label': '2026.05',
                    'effective_from': '2026-05-01T00:00:00Z',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/dsars',
            'payload': {
                'record': {
                    'id': f'dsar-{tenant}',
                    'tenant': tenant,
                    'code': f'DSAR-{tenant}',
                    'data_subject_id': f'subject-{tenant}',
                    'request_type': 'access',
                    'due_at': '2026-06-15T00:00:00Z',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/retention-schedules',
            'payload': {
                'record': {
                    'id': f'retention-{tenant}',
                    'tenant': tenant,
                    'code': f'RETENTION-{tenant}',
                    'data_category': 'contact',
                    'retention_days': 365,
                    'legal_basis': 'consent',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/cross-border-restrictions',
            'payload': {
                'record': {
                    'id': f'xborder-{tenant}',
                    'tenant': tenant,
                    'code': f'XBR-{tenant}',
                    'destination_country': 'US',
                    'transfer_mechanism': 'scc',
                    'restriction_level': 'review',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/audit-proofs',
            'payload': {
                'record': {
                    'id': f'proof-{tenant}',
                    'tenant': tenant,
                    'code': f'PROOF-{tenant}',
                    'control_name': 'consent_capture_control',
                    'proof_hash': f'hash-{tenant}',
                    'proof_scope': 'release',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/documents',
            'payload': {
                'record': {
                    'id': f'doc-{tenant}',
                    'tenant': tenant,
                    'code': f'DOC-{tenant}',
                    'document_digest': f'digest-{tenant}',
                    'document_kind': 'policy-redline',
                }
            },
        },
        {
            'method': 'POST',
            'path': '/api/pbc/privacy_consent_governance/instructions/plan',
            'payload': {
                'record': {
                    'id': f'plan-{tenant}',
                    'tenant': tenant,
                    'code': f'PLAN-{tenant}',
                    'document_intake_id': f'doc-{tenant}',
                    'target_operation': 'publish_policy_version',
                    'confirmation_required': True,
                }
            },
        },
    )


def seed_plan(tenant: str = 'tenant_demo') -> dict:
    bundle = seed_bundle(tenant)
    rows = tuple(
        {
            'table': entry['path'].rsplit('/', 1)[-1].replace('-', '_'),
            'code': entry['payload']['record']['code'],
            'path': entry['path'],
        }
        for entry in bundle
    )
    return {'ok': True, 'pbc': PBC_KEY, 'rows': rows, 'bundle': bundle, 'side_effects': ()}


def validate_seed_data() -> dict:
    bundle = seed_bundle()
    invalid_targets = tuple(
        entry['path']
        for entry in bundle
        if entry['method'] != 'POST' or not entry['path'].startswith('/api/pbc/privacy_consent_governance/')
    )
    owned = all(table.startswith(f'{PBC_KEY}_') for table in OWNED_TABLES)
    return {
        'ok': not invalid_targets and owned,
        'bundle': bundle,
        'invalid_targets': invalid_targets,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return {
        'ok': seed_plan()['ok'] and validate_seed_data()['ok'],
        'side_effects': (),
    }
