"""AI agent and chatbot skill contract for the cdp_segmentation PBC."""

from __future__ import annotations

import hashlib

from .manifest import PBC_MANIFEST
from . import routes
from . import services


PBC_KEY = 'cdp_segmentation'
AGENT_NAME = 'CdpSegmentationAgent'
_DOCUMENT_ACTIONS = ('summarize', 'extract_fields', 'validate_against_rules', 'draft_crud_plan')
_CRUD_ACTIONS = ('create', 'read', 'update', 'delete')
_SKILL_NAMES = (
    f'{PBC_KEY}.task_guidance',
    f'{PBC_KEY}.document_instruction_intake',
    f'{PBC_KEY}.segment_definition_drafting',
    f'{PBC_KEY}.consent_screening_guidance',
    f'{PBC_KEY}.governed_create',
    f'{PBC_KEY}.governed_read',
    f'{PBC_KEY}.governed_update',
    f'{PBC_KEY}.governed_delete',
    f'{PBC_KEY}.policy_explanation',
    f'{PBC_KEY}.workbench_navigation',
)


def _owned_tables():
    return tuple(
        table if str(table).startswith(f'{PBC_KEY}_') else f"{PBC_KEY}_{table}"
        for table in PBC_MANIFEST.get('tables', ())
    )


def _query_operations():
    return services.service_operation_manifest().get('query_operations', ())


def _command_operations():
    return services.service_operation_manifest().get('command_operations', ())


def _route_for_operation(operation_name: str) -> dict | None:
    route_manifest = routes.api_route_contracts()
    return next(
        (item for item in route_manifest.get('contracts', ()) if item.get('operation') == operation_name),
        None,
    )


def _document_target(lower_text: str, suggested_action: str) -> tuple[str, str, dict]:
    if suggested_action == 'define_segment':
        if 'rule' in lower_text or 'criteria' in lower_text:
            return (
                f'{PBC_KEY}_segment_rule',
                'parse_segment_rule',
                {
                    'tenant': 'tenant_demo',
                    'segment_id': 'seg_from_document',
                    'rule_text': lower_text.strip() or 'segment audience criteria',
                },
            )
        return (
            f'{PBC_KEY}_segment_definition',
            'define_segment',
            {
                'segment_id': 'seg_from_document',
                'tenant': 'tenant_demo',
                'name': 'Document Authored Segment',
                'criteria': {
                    'min_payment_value': 1000 if 'high value' in lower_text else 0,
                    'requires_shipment': 'shipment' in lower_text or 'deliver' in lower_text,
                    'min_engagement': 0.2 if 'engagement' in lower_text else 0.0,
                },
                'status': 'draft',
            },
        )
    if suggested_action == 'upsert_profile_property':
        property_name = 'consent_status' if 'consent' in lower_text or 'opt in' in lower_text or 'opt-in' in lower_text else 'profile_attribute'
        property_value = 'opt_in' if property_name == 'consent_status' else 'document_capture'
        return (
            f'{PBC_KEY}_profile_property',
            'upsert_profile_property',
            {
                'property_id': 'prop_from_document',
                'tenant': 'tenant_demo',
                'customer_id': 'cust_demo',
                'name': property_name,
                'value': property_value,
                'source': 'document_instruction',
            },
        )
    if suggested_action == 'resolve_audience_exception':
        return (
            f'{PBC_KEY}_profile_exception',
            'resolve_audience_exception',
            {
                'exception_id': 'exc_from_document',
                'tenant': 'tenant_demo',
                'customer_id': 'cust_demo',
                'reason': 'document_identified_conflict',
                'resolution': 'route_to_segmentation_steward',
            },
        )
    return (
        f'{PBC_KEY}_profile',
        'build_workbench_view',
        {
            'tenant': 'tenant_demo',
        },
    )


def agent_skill_manifest():
    """Return the skills this PBC contributes to the composed application assistant."""
    return {
        'ok': bool(_SKILL_NAMES) and bool(_owned_tables()) and bool(_query_operations()),
        'pbc': PBC_KEY,
        'agent': AGENT_NAME,
        'skills': tuple(
            {
                'name': skill,
                'scope': PBC_KEY,
                'owned_tables': _owned_tables(),
                'allowed_crud_actions': _CRUD_ACTIONS,
                'document_actions': _DOCUMENT_ACTIONS,
                'requires_confirmation_for_mutation': True,
                'uses_appgen_event_contract': True,
                'stream_engine_picker_visible': False,
            }
            for skill in _SKILL_NAMES
        ),
        'query_operations': _query_operations(),
        'command_operations': _command_operations(),
        'side_effects': (),
    }


def chatbot_interface_contract():
    """Return the professional help/chatbot surface contract for this PBC."""
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'agent': AGENT_NAME,
        'entrypoint': f'/assistant/pbc/{PBC_KEY}',
        'single_agent_contribution': f'{PBC_KEY}_skills',
        'single_agent_skill_namespace': f'{PBC_KEY}_skills',
        'capabilities': (
            'task_guidance',
            'document_and_instruction_intake',
            'governed_datastore_crud',
            'policy_and_permission_explanation',
            'workbench_navigation',
            'mutation_preview',
        ),
        'professional_controls': (
            'citation_required_for_document_facts',
            'mutation_preview_before_commit',
            'permission_check_before_mutation',
            'owned_table_boundary_check',
            'audit_event_plan',
        ),
        'side_effects': (),
    }


def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or '')
    instruction_text = str(instructions or '')
    digest = hashlib.sha256(f'{PBC_KEY}:{document_text}:{instruction_text}'.encode('utf-8')).hexdigest()
    lower = f"{document_text}\n{instruction_text}".lower()
    suggested_action = (
        'resolve_audience_exception' if 'exception' in lower or 'conflict' in lower else
        'define_segment' if 'segment' in lower or 'audience' in lower else
        'upsert_profile_property' if 'profile' in lower or 'consent' in lower else
        'read'
    )
    target_table, preferred_operation, payload_template = _document_target(lower, suggested_action)
    preferred_route = _route_for_operation(preferred_operation)
    candidate_tables = _owned_tables()
    return {
        'ok': bool(document_text or instruction_text),
        'pbc': PBC_KEY,
        'document_digest': digest,
        'document_actions': _DOCUMENT_ACTIONS,
        'candidate_tables': candidate_tables,
        'candidate_operations': _command_operations() + _query_operations(),
        'suggested_action': suggested_action,
        'suggested_crud_action': 'update' if suggested_action in {'define_segment', 'upsert_profile_property', 'resolve_audience_exception'} else 'read',
        'target_table': target_table,
        'preferred_operation': preferred_operation,
        'preferred_route': preferred_route['route_id'] if preferred_route else None,
        'payload_template': payload_template,
        'domain_entities': (
            'profile',
            'profile_consent',
            'segment_definition',
            'segment_membership',
            'activation_run',
            'profile_exception',
        ),
        'instruction_preview': {
            'segment_intent': 'segment' in lower or 'audience' in lower,
            'consent_intent': 'consent' in lower or 'opt in' in lower or 'opt-in' in lower,
            'activation_intent': 'activate' in lower or 'delivery' in lower,
            'exception_intent': 'exception' in lower or 'conflict' in lower,
        },
        'requires_human_confirmation': True,
        'side_effects': (),
    }


def datastore_crud_plan(action='read', table=None, payload=None):
    """Plan governed CRUD against owned tables only."""
    normalized_action = str(action).lower()
    owned_tables = _owned_tables()
    selected_table = table or (owned_tables[0] if owned_tables else None)
    allowed = normalized_action in _CRUD_ACTIONS and selected_table in owned_tables
    operation_pool = _query_operations() if normalized_action == 'read' else _command_operations()
    preferred_operation = (
        'define_segment' if selected_table == f'{PBC_KEY}_segment_definition' else
        'parse_segment_rule' if selected_table == f'{PBC_KEY}_segment_rule' else
        'upsert_profile_property' if selected_table in {f'{PBC_KEY}_profile_property', f'{PBC_KEY}_profile_consent'} else
        'resolve_audience_exception' if selected_table == f'{PBC_KEY}_profile_exception' else
        ('build_workbench_view' if normalized_action == 'read' else None)
    )
    preferred_route = _route_for_operation(preferred_operation) if preferred_operation else None
    return {
        'ok': allowed and bool(operation_pool),
        'pbc': PBC_KEY,
        'action': normalized_action,
        'table': selected_table,
        'allowed_tables': owned_tables,
        'payload_keys': tuple(sorted(dict(payload or {}))),
        'owned_tables': owned_tables,
        'candidate_operations': operation_pool,
        'preferred_operation': preferred_operation,
        'preferred_route': preferred_route['route_id'] if preferred_route else None,
        'requires_confirmation': normalized_action != 'read',
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def document_instruction_crud_support(document=None, instructions=None, *, payload=None):
    """Return a governed mutation preview for document/instruction intake."""
    plan = document_instruction_plan(document=document, instructions=instructions)
    preview_payload = dict(payload or plan.get('payload_template') or {})
    crud = datastore_crud_plan(
        plan['suggested_crud_action'],
        table=plan['target_table'],
        payload=preview_payload,
    )
    route_contract = _route_for_operation(plan['preferred_operation'])
    permission = route_contract['permission'] if route_contract else None
    boundary_ok = bool(crud['ok']) and plan['target_table'] in set(_owned_tables())
    return {
        'ok': plan['ok'] and crud['ok'] and boundary_ok and permission is not None,
        'pbc': PBC_KEY,
        'document_plan': plan,
        'crud_plan': crud,
        'preferred_operation': plan['preferred_operation'],
        'preferred_route': plan['preferred_route'],
        'permission': permission,
        'requires_confirmation': crud['requires_confirmation'],
        'mutation_preview': {
            'table': plan['target_table'],
            'payload': preview_payload,
            'payload_keys': tuple(sorted(preview_payload)),
            'boundary': {
                'ok': boundary_ok,
                'table': plan['target_table'],
                'owned_tables': _owned_tables(),
            },
            'event_contract': 'AppGen-X',
        },
        'side_effects': (),
    }


def composed_agent_contribution():
    """Return the package contribution to the application's single assistant."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    return {
        'ok': skills['ok'] and chatbot['ok'],
        'pbc': PBC_KEY,
        'agent': AGENT_NAME,
        'single_agent_skill_namespace': f'{PBC_KEY}_skills',
        'dsl_tools': (f'{PBC_KEY}_skills', f'{PBC_KEY}_documents', f'{PBC_KEY}_crud'),
        'skills': tuple(item['name'] for item in skills['skills']),
        'chatbot': chatbot,
        'side_effects': (),
    }


def smoke_test():
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan('sample instruction', 'create or update the primary record')
    support = document_instruction_crud_support(
        'Retention audience brief',
        'Create a segment for high value opted-in customers and preview the mutation.',
    )
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', table='cdp_segmentation_segment_definition', payload={'status': 'draft'})
    contribution = composed_agent_contribution()
    return {
        'ok': skills['ok']
        and chatbot['ok']
        and document['ok']
        and support['ok']
        and read_plan['ok']
        and create_plan['ok']
        and contribution['ok']
        and not create_plan['stream_engine_picker_visible'],
        'skills': skills,
        'chatbot': chatbot,
        'document': document,
        'support': support,
        'read_plan': read_plan,
        'create_plan': create_plan,
        'contribution': contribution,
        'side_effects': (),
    }
