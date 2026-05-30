from pyAppGen.pbcs.customer_success_management.runtime import (
    CUSTOMER_SUCCESS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    CUSTOMER_SUCCESS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    customer_success_management_build_release_evidence,
    customer_success_management_runtime_capabilities,
    customer_success_management_runtime_smoke,
)
from pyAppGen.pbcs.customer_success_management.success_control import (
    CAPABILITY_TABLES,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    SLUG_BY_NUMBER,
    SUCCESS_CONTROL_CAPABILITIES,
    SUCCESS_CONTROL_FUNCTIONS,
    evaluate_success_control,
    improve1_success_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.customer_success_management.ui import customer_success_management_ui_contract


def test_all_50_success_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(SUCCESS_CONTROL_CAPABILITIES) == 50
    assert set(SUCCESS_CONTROL_CAPABILITIES) == set(SUCCESS_CONTROL_FUNCTIONS)

    for capability in SUCCESS_CONTROL_CAPABILITIES:
        result = SUCCESS_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("customer_success_management_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == CUSTOMER_SUCCESS_MANAGEMENT_REQUIRED_EVENT_TOPIC
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == CUSTOMER_SUCCESS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        assert result["agent_skill"].startswith("customer_success_management_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_success_controls_reject_missing_fields_and_foreign_table_access():
    first = SUCCESS_CONTROL_CAPABILITIES[0]
    missing = evaluate_success_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("customer_master_table",)
    rejected = evaluate_success_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("customer_master_table",)


def test_account_health_playbook_escalation_and_renewal_controls_surface_findings():
    account = sample_payload_for(SLUG_BY_NUMBER[1])
    account["customer_projection"] = ""
    assert "success_account_requires_customer_projection" in evaluate_success_control(SLUG_BY_NUMBER[1], account)["domain_findings"]

    lifecycle = sample_payload_for(SLUG_BY_NUMBER[2])
    lifecycle["target_state"] = "quietly_churned"
    assert "success_account_lifecycle_state_invalid" in evaluate_success_control(SLUG_BY_NUMBER[2], lifecycle)["domain_findings"]

    health = sample_payload_for(SLUG_BY_NUMBER[6])
    health["components"] = ()
    assert "health_score_requires_components" in evaluate_success_control(SLUG_BY_NUMBER[6], health)["domain_findings"]

    task = sample_payload_for(SLUG_BY_NUMBER[13])
    task["completion_proof"] = ""
    assert "playbook_task_requires_completion_proof" in evaluate_success_control(SLUG_BY_NUMBER[13], task)["domain_findings"]

    renewal = sample_payload_for(SLUG_BY_NUMBER[16])
    renewal["value_evidence"] = ""
    assert "renewal_motion_requires_value_evidence" in evaluate_success_control(SLUG_BY_NUMBER[16], renewal)["domain_findings"]


def test_boundary_schema_agent_control_ethics_and_release_readiness_require_governance():
    boundary = sample_payload_for(SLUG_BY_NUMBER[34])
    boundary["dependency_mode"] = "shared_table"
    assert "cross_pbc_boundary_must_use_api_event_or_projection" in evaluate_success_control(SLUG_BY_NUMBER[34], boundary)["domain_findings"]

    extension = sample_payload_for(SLUG_BY_NUMBER[31])
    extension["owned_table"] = "customer_profile_table"
    assert "schema_extension_must_target_owned_success_table" in evaluate_success_control(SLUG_BY_NUMBER[31], extension)["domain_findings"]

    agent = sample_payload_for(SLUG_BY_NUMBER[41])
    agent["human_confirmation"] = False
    agent_review = evaluate_success_control(SLUG_BY_NUMBER[41], agent)
    assert "agent_success_plan_requires_human_confirmation" in agent_review["domain_findings"]
    assert agent_review["requires_human_confirmation"] is True

    ethics = sample_payload_for(SLUG_BY_NUMBER[48])
    ethics.update({"unresolved_risk": True, "expansion_pressure": "high"})
    assert "ethics_guardrail_blocks_expansion_over_unresolved_risk" in evaluate_success_control(SLUG_BY_NUMBER[48], ethics)["domain_findings"]

    proof = sample_payload_for(SLUG_BY_NUMBER[50])
    proof["boundary_verification"] = False
    assert "end_to_end_success_proof_requires_boundary_verification" in evaluate_success_control(SLUG_BY_NUMBER[50], proof)["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_success_control_contract():
    contract = improve1_success_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CUSTOMER_SUCCESS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS

    runtime = customer_success_management_runtime_capabilities()
    smoke = customer_success_management_runtime_smoke()
    release = customer_success_management_build_release_evidence()
    ui = customer_success_management_ui_contract()

    assert runtime["improve1_success_control"]["ok"] is True
    assert smoke["improve1_success_control"]["ok"] is True
    assert any(check["id"] == "improve1_success_control" and check["ok"] for check in smoke["checks"])
    assert release["improve1_success_control"]["capability_count"] == 50
    assert len(ui["success_control_panels"]) == 50
    assert ui["success_control_contract"]["ok"] is True
