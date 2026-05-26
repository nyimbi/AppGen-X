import importlib

from pyAppGen.dsl import schema_from_dsl
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS
from pyAppGen.pbc import pbc_composition_dsl
from pyAppGen.pbc import pbc_source_artifact_release_audit


def test_every_pbc_exposes_agent_chatbot_skills_and_governed_crud() -> None:
    for key in IMPLEMENTED_PBC_KEYS:
        agent = importlib.import_module(f"pyAppGen.pbcs.{key}.agent")

        skills = agent.agent_skill_manifest()
        chatbot = agent.chatbot_interface_contract()
        document = agent.document_instruction_plan("uploaded document", "create the relevant record")
        read_plan = agent.datastore_crud_plan("read")
        create_plan = agent.datastore_crud_plan("create", payload={"status": "draft"})
        rejected_foreign = agent.datastore_crud_plan("update", table="foreign_table", payload={"status": "draft"})
        contribution = agent.composed_agent_contribution()
        smoke = agent.smoke_test()

        assert skills["ok"] is True
        assert chatbot["ok"] is True
        assert document["ok"] is True
        assert read_plan["ok"] is True
        assert create_plan["ok"] is True
        assert rejected_foreign["ok"] is False
        assert contribution["ok"] is True
        assert smoke["ok"] is True
        assert all(skill["requires_confirmation_for_mutation"] for skill in skills["skills"])
        assert all(skill["stream_engine_picker_visible"] is False for skill in skills["skills"])
        assert read_plan["requires_confirmation"] is False
        assert create_plan["requires_confirmation"] is True
        assert contribution["single_agent_skill_namespace"] == f"{key}_skills"
        assert f"{key}_crud" in contribution["dsl_tools"]


def test_source_package_audit_requires_agent_chatbot_artifact() -> None:
    audit = pbc_source_artifact_release_audit(IMPLEMENTED_PBC_KEYS)

    assert audit["ok"] is True
    assert "agent.py" in audit["required_artifacts"]
    for contract in audit["contracts"]:
        assert any(
            check["id"] == "agent_chatbot_skills_materialized" and check["ok"]
            for check in contract["checks"]
        )


def test_pbc_composition_dsl_includes_single_composed_agent_with_pbc_skills() -> None:
    selected = ("gl_core", "ap_automation", "checkout_processing")
    dsl = pbc_composition_dsl(selected, app_name="AgenticPbcSuite", targets=("web", "chatbot"))
    schema = schema_from_dsl(dsl, source_name="agentic-pbc-suite.appgen")

    assert "llm AppGenXLocalModel" in dsl
    assert "agent AgenticPbcSuiteAssistant" in dsl
    for key in selected:
        assert f"{key}_skills" in dsl
    assert schema.llm_providers
    assert schema.agents
    assert schema.agents[0].provider == "AppGenXLocalModel"
    assert set(schema.agents[0].tools) >= {f"{key}_skills" for key in selected}
