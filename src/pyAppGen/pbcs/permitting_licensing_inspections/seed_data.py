"""Seed data and demo bootstrap for permitting_licensing_inspections."""
from __future__ import annotations

from copy import deepcopy

from .runtime import DEFAULT_CONFIGURATION, DEFAULT_PARAMETERS, DEFAULT_RULES, PBC_KEY


BOOTSTRAP_STEPS = (
    {
        'operation': 'capture_pre_application',
        'payload': {
            'tenant': 'tenant_demo',
            'application_type': 'building_permit',
            'site_address': '17 Civic Center Road',
            'parcel_id': 'PAR-401',
            'advisory_notes': ('public notice likely', 'utilities review required'),
            'likely_review_disciplines': ('zoning', 'structural', 'fire', 'utilities'),
            'public_notice_required': True,
        },
    },
    {
        'operation': 'command_application',
        'payload': {
            'tenant': 'tenant_demo',
            'application_id': 'APP-DEMO-001',
            'application_type': 'building_permit',
            'submittal_kind': 'new',
            'site_address': '17 Civic Center Road',
            'parcel_id': 'PAR-401',
            'responsible_parties': {'applicant': 'North Block Builders', 'owner': 'Civic Holdings'},
            'documents': ('site_plan', 'architectural_drawings', 'owner_authorization'),
            'attestations': ('code_compliance', 'responsible_designer'),
            'consultation_id': 'CONS-0001',
        },
    },
    {
        'operation': 'add_plan_set',
        'payload': {
            'application_id': 'APP-DEMO-001',
            'plan_set_id': 'APP-DEMO-001-v1',
            'version_label': 'v1',
            'revision_date': '2026-05-30',
            'sheet_inventory': ('A001', 'A101', 'C201'),
            'comparison_notes': ('initial intake package',),
        },
    },
    {
        'operation': 'approve_review_task',
        'payload': {
            'tenant': 'tenant_demo',
            'task_id': 'REVIEW-ZONING-001',
            'application_id': 'APP-DEMO-001',
            'discipline': 'zoning',
            'plan_set_id': 'APP-DEMO-001-v1',
            'comment_template': 'zoning-core',
        },
    },
    {
        'operation': 'simulate_fee_assessment',
        'payload': {
            'tenant': 'tenant_demo',
            'assessment_id': 'FEE-DEMO-001',
            'application_id': 'APP-DEMO-001',
            'application_type': 'building_permit',
            'valuation': 325000,
            'inspection_count': 2,
            'payment_status': 'confirmed',
        },
    },
    {
        'operation': 'record_permit',
        'payload': {
            'tenant': 'tenant_demo',
            'permit_id': 'PERMIT-DEMO-001',
            'application_id': 'APP-DEMO-001',
            'payment_status': 'confirmed',
            'conditions': ('stormwater plan on site', 'fire marshal signoff before occupancy'),
        },
    },
    {
        'operation': 'create_inspection',
        'payload': {
            'tenant': 'tenant_demo',
            'inspection_id': 'INSP-DEMO-001',
            'permit_id': 'PERMIT-DEMO-001',
            'inspection_type': 'final',
            'scheduled_for': '2026-06-05T09:00:00Z',
            'result': 'failed',
            'findings': ('egress lighting incomplete',),
            'reinspection_required': True,
        },
    },
    {
        'operation': 'record_violation',
        'payload': {
            'tenant': 'tenant_demo',
            'violation_id': 'VIO-DEMO-001',
            'inspection_id': 'INSP-DEMO-001',
            'severity': 'major',
            'code_sections': ('IBC-1008',),
            'cure_deadline': '2026-06-20',
        },
    },
    {
        'operation': 'evaluate_renewal',
        'payload': {
            'tenant': 'tenant_demo',
            'renewal_id': 'RENEW-DEMO-001',
            'license_id': 'LIC-DEMO-001',
            'active_violations': 1,
            'failed_inspections': 1,
            'payment_status': 'confirmed',
            'attestations_complete': True,
            'insurance_verified': True,
        },
    },
)


def bootstrap_seed_bundle():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'configuration': deepcopy(DEFAULT_CONFIGURATION),
        'parameters': deepcopy(DEFAULT_PARAMETERS),
        'rules': tuple(deepcopy(rule) for rule in DEFAULT_RULES.values()),
        'steps': tuple(deepcopy(step) for step in BOOTSTRAP_STEPS),
        'side_effects': (),
    }


def seed_plan():
    bundle = bootstrap_seed_bundle()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'records': tuple({'operation': step['operation'], 'code': step['payload'].get('application_id') or step['payload'].get('permit_id') or step['payload'].get('inspection_id') or step['payload'].get('violation_id') or step['payload'].get('renewal_id') or step['payload'].get('consultation_id')} for step in bundle['steps']),
        'steps': bundle['steps'],
        'side_effects': (),
    }


def validate_seed_data():
    bundle = bootstrap_seed_bundle()
    step_names = tuple(step['operation'] for step in bundle['steps'])
    return {
        'ok': 'command_application' in step_names and 'record_permit' in step_names and 'record_violation' in step_names,
        'pbc': PBC_KEY,
        'step_count': len(bundle['steps']),
        'side_effects': (),
    }


def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
