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
