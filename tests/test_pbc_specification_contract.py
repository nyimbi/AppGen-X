from pyAppGen.pbc import pbc_agent_capability_contract
from pyAppGen.pbc import pbc_agent_capability_release_audit
from pyAppGen.pbc import pbc_specification_contract
from pyAppGen.pbc import pbc_specification_release_audit


def test_pbc_specifications_cover_agents_skills_and_registration():
    audit = pbc_specification_release_audit()
    assert audit["ok"] is True
    assert audit["pbc_count"] >= 47
    required_ids = {concept["id"] for concept in audit["required_concepts"]}
    assert "agent_chatbot_skills" in required_ids
    assert "side_effect_free_self_registration" in required_ids
    assert not audit["blocking_gaps"]


def test_multi_sided_market_specification_is_traceable_to_agent_contract():
    contract = pbc_specification_contract("multi_sided_market")
    assert contract["ok"] is True
    assert not contract["missing_concepts"]
    assert contract["manifest_traceability"]["ok"] is True
    required_ids = {concept["id"] for concept in contract["required_concepts"]}
    assert {
        "agent_chatbot_skills",
        "side_effect_free_self_registration",
    } <= required_ids


def test_all_pbc_agent_capabilities_are_executable_and_composable():
    audit = pbc_agent_capability_release_audit()
    assert audit["ok"] is True
    assert audit["pbc_count"] >= 47
    assert not audit["blocking_gaps"]
    assert all(contract["namespace"].endswith("_skills") for contract in audit["contracts"])


def test_multi_sided_market_agent_rejects_foreign_table_mutations():
    contract = pbc_agent_capability_contract("multi_sided_market")
    assert contract["ok"] is True
    assert contract["chatbot"]["entrypoint"] == "/assistant/pbc/multi_sided_market"
    assert contract["contribution"]["single_agent_skill_namespace"] == "multi_sided_market_skills"
    assert contract["create_plan"]["requires_confirmation"] is True
    assert contract["rejected_plan"]["ok"] is False
