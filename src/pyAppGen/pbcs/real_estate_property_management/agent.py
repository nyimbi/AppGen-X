from .standalone import (
    PBC_KEY,
    REAL_ESTATE_PROPERTY_MANAGEMENT_OWNED_TABLES as OWNED_TABLES,
    agent_skill_manifest,
    chatbot_interface_contract,
    datastore_crud_plan,
    composed_agent_contribution,
    real_estate_property_management_parse_document_instruction,
)


def document_instruction_plan(document, instruction):
    return real_estate_property_management_parse_document_instruction(document, instruction)


def smoke_test():
    return {
        'ok': agent_skill_manifest()['ok'] and chatbot_interface_contract()['ok'] and document_instruction_plan('lease doc', 'create renewal preview')['ok'] and datastore_crud_plan('create', table=f'{PBC_KEY}_assistant_artifact')['ok'] and datastore_crud_plan('update', table='foreign_table')['ok'] is False and composed_agent_contribution()['ok'],
        'side_effects': (),
    }
