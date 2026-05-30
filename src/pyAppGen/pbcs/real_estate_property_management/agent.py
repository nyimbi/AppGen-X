"""Agent and chatbot skills for real estate property management."""
from .standalone import (
    PBC_KEY,
    REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES as OWNED_TABLES,
    agent_skill_manifest as _agent_skill_manifest,
    chatbot_interface_contract as _chatbot_interface_contract,
    datastore_crud_plan as _datastore_crud_plan,
    composed_agent_contribution as _composed_agent_contribution,
    real_estate_property_management_parse_document_instruction,
)


def agent_skill_manifest():
    manifest = _agent_skill_manifest()
    skills = tuple({**skill, 'scope': PBC_KEY, 'requires_confirmation_for_mutation': True, 'uses_appgen_event_contract': True, 'stream_engine_picker_visible': False} for skill in manifest.get('skills', ()))
    return {**manifest, 'skills': skills, 'side_effects': ()}


def chatbot_interface_contract():
    contract = _chatbot_interface_contract()
    return {**contract, 'single_agent_skill_namespace': f'{PBC_KEY}_skills', 'stream_engine_picker_visible': False, 'side_effects': ()}


def document_instruction_plan(document, instruction):
    return real_estate_property_management_parse_document_instruction(document, instruction)


def datastore_crud_plan(action, table=None, payload=None):
    target = table or OWNED_TABLES[0]
    if not str(target).startswith(f'{PBC_KEY}_'):
        return {'ok': False, 'reason': 'foreign_table_rejected', 'table': target, 'side_effects': ()}
    plan = _datastore_crud_plan(action, table=target, payload=payload)
    if plan.get('ok') is True:
        plan['event_contract'] = 'AppGen-X'
    return plan


def composed_agent_contribution():
    contribution = _composed_agent_contribution()
    namespace = f'{PBC_KEY}_skills'
    tools = tuple(contribution.get('dsl_tools', ()))
    if namespace not in tools:
        tools = (namespace,) + tools
    return {**contribution, 'single_agent_skill_namespace': namespace, 'dsl_tools': tools, 'side_effects': ()}


def smoke_test():
    return {
        'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('lease doc', 'create renewal preview')['ok'] and datastore_crud_plan('create', table=f'{PBC_KEY}_assistant_artifact')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'],
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }
