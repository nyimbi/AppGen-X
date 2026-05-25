from pyAppGen.pbc import TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import talent_onboarding_accept_offer
from pyAppGen.pbc import talent_onboarding_advance_candidate_stage
from pyAppGen.pbc import talent_onboarding_build_workbench_view
from pyAppGen.pbc import talent_onboarding_complete_onboarding_task
from pyAppGen.pbc import talent_onboarding_configure_runtime
from pyAppGen.pbc import talent_onboarding_create_candidate
from pyAppGen.pbc import talent_onboarding_create_job_requisition
from pyAppGen.pbc import talent_onboarding_create_onboarding_task
from pyAppGen.pbc import talent_onboarding_empty_state
from pyAppGen.pbc import talent_onboarding_extend_offer
from pyAppGen.pbc import talent_onboarding_provision_employee
from pyAppGen.pbc import talent_onboarding_record_background_check
from pyAppGen.pbc import talent_onboarding_register_rule
from pyAppGen.pbc import talent_onboarding_render_workbench
from pyAppGen.pbc import talent_onboarding_runtime_capabilities
from pyAppGen.pbc import talent_onboarding_runtime_smoke
from pyAppGen.pbc import talent_onboarding_set_parameter
from pyAppGen.pbc import talent_onboarding_ui_contract


def test_talent_onboarding_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = talent_onboarding_runtime_capabilities()
    smoke = talent_onboarding_runtime_smoke()

    assert runtime["format"] == "appgen.talent-onboarding-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/talent_onboarding"
    assert len(runtime["standard_features"]) >= 24
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("talent_onboarding")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TalentConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("talent_onboarding",))["ok"] is True
    assert pbc_implemented_capability_audit(("talent_onboarding",))["ok"] is True


def test_talent_onboarding_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = talent_onboarding_empty_state()
    state = talent_onboarding_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.talent.events",
            "retry_limit": 3,
            "allowed_countries": ("US",),
            "allowed_candidate_sources": ("referral", "career_site"),
            "allowed_check_providers": ("trusted_screen",),
            "allowed_task_types": ("identity", "equipment", "policy"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = talent_onboarding_set_parameter(state, "minimum_match_score", 0.7)["state"]
    state = talent_onboarding_set_parameter(state, "offer_expiry_days", 7)["state"]
    state = talent_onboarding_set_parameter(state, "onboarding_sla_days", 5)["state"]
    state = talent_onboarding_set_parameter(state, "background_check_confidence_threshold", 0.85)["state"]
    state = talent_onboarding_set_parameter(state, "retention_days", 365)["state"]
    state = talent_onboarding_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "hiring",
            "eligible_worker_types": ("employee",),
            "allowed_countries": ("US",),
            "required_candidate_consents": ("privacy", "screening"),
            "allowed_stages": ("applied", "screen", "interview", "offer", "hired"),
            "required_check_types": ("identity",),
            "task_templates": ("identity", "equipment"),
            "status": "active",
        },
    )["state"]
    requisition = talent_onboarding_create_job_requisition(
        state,
        {
            "requisition_id": "req_ops",
            "tenant": "tenant_ops",
            "title": "Operations Analyst",
            "department": "Operations",
            "manager_employee_id": "mgr_ops",
            "country": "US",
            "location": "NYC",
            "worker_type": "employee",
            "headcount": 1,
            "budget": 120000,
        },
    )
    state = requisition["state"]
    assert requisition["requisition"]["status"] == "open"

    candidate = talent_onboarding_create_candidate(
        state,
        {
            "candidate_id": "cand_ops",
            "tenant": "tenant_ops",
            "requisition_id": "req_ops",
            "name": "Ada Worker",
            "source": "referral",
            "country": "US",
            "skills": ("operations", "analytics"),
            "match_score": 0.88,
            "consents": ("privacy", "screening"),
            "identity": {"did": "did:appgen:cand-ops", "issuer": "trusted_registry", "status": "active"},
        },
    )
    state = candidate["state"]
    assert candidate["candidate"]["stage"] == "applied"
    assert candidate["candidate"]["status"] == "active"

    state = talent_onboarding_advance_candidate_stage(state, "cand_ops", stage="interview", actor="recruiter_ops")["state"]
    check = talent_onboarding_record_background_check(
        state,
        {"check_id": "check_ops", "tenant": "tenant_ops", "candidate_id": "cand_ops", "provider": "trusted_screen", "check_type": "identity", "confidence": 0.94, "result": "clear"},
    )
    state = check["state"]
    assert check["check"]["status"] == "clear"

    offer = talent_onboarding_extend_offer(state, "cand_ops", {"offer_id": "offer_ops", "salary": 95000, "currency": "USD", "start_date": "2026-06-15", "expires_in_days": 7})
    state = offer["state"]
    assert offer["offer"]["status"] == "extended"

    state = talent_onboarding_accept_offer(state, "cand_ops", accepted_by="candidate")["state"]
    task = talent_onboarding_create_onboarding_task(state, "cand_ops", {"task_id": "task_ops", "task_type": "identity", "assignee": "hr_ops", "due_in_days": 3})
    state = task["state"]
    assert task["task"]["status"] == "open"

    state = talent_onboarding_complete_onboarding_task(state, "task_ops", completed_by="hr_ops")["state"]
    provisioned = talent_onboarding_provision_employee(state, "cand_ops", provisioned_by="hr_ops")
    state = provisioned["state"]
    assert provisioned["candidate"]["status"] == "provisioned"
    assert provisioned["handoffs"] == ("personnel_identity_projection", "access_preload_request", "notification_welcome_sequence")
    assert state["outbox"][-1]["idempotency_key"] == "talent_onboarding:EmployeeProvisioned:talent_evt_000010"

    workbench = talent_onboarding_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["requisition_count"] == 1
    assert workbench["candidate_count"] == 1
    assert workbench["hired_count"] == 1
    assert workbench["provisioned_count"] == 1
    assert workbench["background_check_count"] == 1
    assert workbench["offer_count"] == 1
    assert workbench["completed_task_count"] == 1

    ui_contract = talent_onboarding_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "minimum_match_score" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = talent_onboarding_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "talent_onboarding.requisition",
            "talent_onboarding.candidate",
            "talent_onboarding.offer",
            "talent_onboarding.onboard",
            "talent_onboarding.configure",
            "talent_onboarding.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 10
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
