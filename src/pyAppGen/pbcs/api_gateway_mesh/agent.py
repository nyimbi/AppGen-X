"""AI agent and chatbot skill contract for the api_gateway_mesh PBC."""

from __future__ import annotations

import hashlib

from .manifest import PBC_MANIFEST
from . import routes
from . import runtime
from . import services
from . import ui


PBC_KEY = 'api_gateway_mesh'
AGENT_NAME = 'ApiGatewayMeshAgent'
_DOCUMENT_ACTIONS = ('summarize', 'extract_fields', 'validate_against_rules', 'draft_crud_plan')
_CRUD_ACTIONS = ('create', 'read', 'update', 'delete')
_SKILL_NAMES = (
    f'{PBC_KEY}.task_guidance',
    f'{PBC_KEY}.document_instruction_intake',
    f'{PBC_KEY}.governed_create',
    f'{PBC_KEY}.governed_read',
    f'{PBC_KEY}.governed_update',
    f'{PBC_KEY}.governed_delete',
    f'{PBC_KEY}.policy_explanation',
    f'{PBC_KEY}.workbench_navigation',
)


def _owned_tables():
    return tuple(
        table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in PBC_MANIFEST.get('tables', ())
    )


def _query_operations():
    return services.service_operation_manifest().get('query_operations', ())


def _command_operations():
    return services.service_operation_manifest().get('command_operations', ())


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
        'capabilities': (
            'task_guidance',
            'document_and_instruction_intake',
            'governed_datastore_crud',
            'policy_and_permission_explanation',
            'workbench_navigation',
            'route_publication_readiness',
            'incident_triage',
        ),
        'professional_controls': (
            'citation_required_for_document_facts',
            'mutation_preview_before_commit',
            'permission_check_before_mutation',
            'owned_table_boundary_check',
            'audit_event_plan',
            'route_publication_safety_case_preview',
        ),
        'side_effects': (),
    }


def document_instruction_plan(document=None, instructions=None):
    """Plan document/instruction handling without mutating state."""
    document_text = str(document or '')
    instruction_text = str(instructions or '')
    digest = hashlib.sha256(f'{PBC_KEY}:{document_text}:{instruction_text}'.encode('utf-8')).hexdigest()
    return {
        'ok': bool(document_text or instruction_text),
        'pbc': PBC_KEY,
        'document_digest': digest,
        'document_actions': _DOCUMENT_ACTIONS,
        'candidate_tables': _owned_tables(),
        'candidate_operations': _command_operations() + _query_operations(),
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
    return {
        'ok': allowed and bool(operation_pool),
        'pbc': PBC_KEY,
        'action': normalized_action,
        'table': selected_table,
        'payload_keys': tuple(sorted(dict(payload or {}))),
        'owned_tables': owned_tables,
        'candidate_operations': operation_pool,
        'requires_confirmation': normalized_action != 'read',
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
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


def route_publication_readiness_preview(state: dict, route_payload: dict) -> dict:
    """Preview route publication safety, collisions, and required operator actions."""
    collision = runtime.api_gateway_mesh_analyze_route_collisions(state, route_payload)
    safety_case = runtime.api_gateway_mesh_build_route_publication_safety_case(state, route_payload)
    actions = []
    if collision["blocking"]:
        actions.append("resolve host/path/method collision before publication")
    if "workload_identity_verified" in safety_case["blocking_items"]:
        actions.append("verify workload identity before publication")
    if "tenant_rule_match" in safety_case["blocking_items"]:
        actions.append("activate a tenant route rule covering method and protocol")
    if "service_registered" in safety_case["blocking_items"]:
        actions.append("register the service before publishing the route")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route_id": route_payload.get("route_id"),
        "ready_to_publish": safety_case["ready_to_publish"],
        "blocking_items": safety_case["blocking_items"],
        "collision_analysis": collision,
        "safety_case": safety_case,
        "recommended_actions": tuple(actions),
        "side_effects": (),
    }


def incident_triage_preview(state: dict, *, tenant: str) -> dict:
    """Summarize gateway incident blast radius and first-pass remediation options."""
    workbench = runtime.api_gateway_mesh_build_workbench_view(state, tenant=tenant)
    rendered = ui.api_gateway_mesh_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=tuple(ui.api_gateway_mesh_ui_contract()["action_permissions"].values()),
    )
    degraded_services = tuple(
        health["service_id"]
        for health in state.get("health", {}).values()
        if health.get("tenant") == tenant and health.get("status") != "healthy"
    )
    blocked_routes = tuple(
        route["route_id"]
        for route in state.get("routes", {}).values()
        if route.get("tenant") == tenant and route.get("status") != "published"
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "blast_radius": {
            "degraded_services": degraded_services,
            "blocked_routes": blocked_routes,
            "dead_letter_count": workbench["dead_letter_count"],
            "retry_evidence_count": workbench["retry_evidence_count"],
        },
        "recommended_actions": tuple(
            action
            for action in (
                "inspect release blockers" if workbench["release_blocking_count"] else None,
                "review dead-letter backlog" if workbench["dead_letter_count"] else None,
                "rebalance traffic or fail over" if degraded_services else None,
            )
            if action
        ),
        "rendered_workbench": rendered,
        "side_effects": (),
    }


def smoke_test():
    """Exercise guidance, document intake, CRUD planning, and composition contribution."""
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    document = document_instruction_plan('sample instruction', 'create or update the primary record')
    read_plan = datastore_crud_plan('read')
    create_plan = datastore_crud_plan('create', payload={'status': 'draft'})
    contribution = composed_agent_contribution()
    state = runtime.api_gateway_mesh_empty_state()
    state = runtime.api_gateway_mesh_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "allowed_regions": ("us-east",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = runtime.api_gateway_mesh_register_rule(
        state,
        {
            "rule_id": "agent_rule",
            "tenant": "tenant_agent",
            "rule_type": "routing",
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "required_identity": True,
            "blocked_paths": (),
            "status": "active",
        },
    )["state"]
    readiness = route_publication_readiness_preview(
        state,
        {
            "route_id": "route_agent",
            "tenant": "tenant_agent",
            "service_id": "svc_missing",
            "host": "api.example.com",
            "path": "/catalog",
            "method": "POST",
            "protocol": "http",
        },
    )
    triage = incident_triage_preview(state, tenant="tenant_agent")
    return {
        'ok': skills['ok']
        and chatbot['ok']
        and document['ok']
        and read_plan['ok']
        and create_plan['ok']
        and contribution['ok']
        and readiness['ok']
        and triage['ok']
        and not create_plan['stream_engine_picker_visible'],
        'skills': skills,
        'chatbot': chatbot,
        'document': document,
        'read_plan': read_plan,
        'create_plan': create_plan,
        'contribution': contribution,
        'readiness': readiness,
        'triage': triage,
        'side_effects': (),
    }
