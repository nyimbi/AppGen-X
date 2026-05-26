import pytest

from pyAppGen.pbc import TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbc import TALENT_ONBOARDING_CONSUMED_EVENT_TYPES
from pyAppGen.pbc import TALENT_ONBOARDING_EMITTED_EVENT_TYPES
from pyAppGen.pbc import TALENT_ONBOARDING_OWNED_TABLES
from pyAppGen.pbc import TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import talent_onboarding_accept_offer
from pyAppGen.pbc import talent_onboarding_advance_candidate_stage
from pyAppGen.pbc import talent_onboarding_build_api_contract
from pyAppGen.pbc import talent_onboarding_build_release_evidence
from pyAppGen.pbc import talent_onboarding_build_schema_contract
from pyAppGen.pbc import talent_onboarding_build_service_contract
from pyAppGen.pbc import talent_onboarding_build_workbench_view
from pyAppGen.pbc import talent_onboarding_complete_onboarding_task
from pyAppGen.pbc import talent_onboarding_configure_runtime
from pyAppGen.pbc import talent_onboarding_create_candidate
from pyAppGen.pbc import talent_onboarding_create_job_requisition
from pyAppGen.pbc import talent_onboarding_create_onboarding_task
from pyAppGen.pbc import talent_onboarding_empty_state
from pyAppGen.pbc import talent_onboarding_extend_offer
from pyAppGen.pbc import talent_onboarding_provision_employee
from pyAppGen.pbc import talent_onboarding_permissions_contract
from pyAppGen.pbc import talent_onboarding_receive_event
from pyAppGen.pbc import talent_onboarding_record_background_check
from pyAppGen.pbc import talent_onboarding_register_rule
from pyAppGen.pbc import talent_onboarding_register_schema_extension
from pyAppGen.pbc import talent_onboarding_render_workbench
from pyAppGen.pbc import talent_onboarding_runtime_capabilities
from pyAppGen.pbc import talent_onboarding_runtime_smoke
from pyAppGen.pbc import talent_onboarding_set_parameter
from pyAppGen.pbc import talent_onboarding_ui_contract
from pyAppGen.pbc import talent_onboarding_verify_owned_table_boundary


def test_talent_onboarding_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = talent_onboarding_runtime_capabilities()
    smoke = talent_onboarding_runtime_smoke()

    assert runtime["format"] == "appgen.talent-onboarding-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/talent_onboarding"
    assert runtime["owned_tables"] == TALENT_ONBOARDING_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 40
    assert len(runtime["standard_features"]) >= 40
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("talent_onboarding")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == TALENT_ONBOARDING_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "talent_onboarding.event"
    assert contract["source_package"]["required_event_topic"] == TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == TALENT_ONBOARDING_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == TALENT_ONBOARDING_EMITTED_EVENT_TYPES
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TalentConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TALENT_ONBOARDING_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("talent_onboarding",))["ok"] is True
    assert pbc_implemented_capability_audit(("talent_onboarding",))["ok"] is True

    api = talent_onboarding_build_api_contract()
    schema = talent_onboarding_build_schema_contract()
    service = talent_onboarding_build_service_contract()
    release = talent_onboarding_build_release_evidence()
    permissions = talent_onboarding_permissions_contract()
    assert api["format"] == "appgen.talent-onboarding-api-contract.v1"
    assert api["owned_tables"] == TALENT_ONBOARDING_OWNED_TABLES
    assert api["database_backends"] == TALENT_ONBOARDING_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == TALENT_ONBOARDING_EMITTED_EVENT_TYPES
    assert api["consumes"] == TALENT_ONBOARDING_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /candidates", "POST /talent/events/inbox", "GET /talent-workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert schema["format"] == "appgen.talent-onboarding-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(TALENT_ONBOARDING_OWNED_TABLES)
    assert len(schema["migrations"]) == len(TALENT_ONBOARDING_OWNED_TABLES)
    assert {
        "job_requisition_approval",
        "candidate_stage_history",
        "interview_schedule",
        "offer_acceptance",
        "talent_governed_model",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.talent-onboarding-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 25
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.talent-onboarding-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert permissions["action_permissions"]["provision_employee"] == "talent_onboarding.onboard"


def test_talent_onboarding_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = talent_onboarding_empty_state()
    state = talent_onboarding_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC,
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
    extension = talent_onboarding_register_schema_extension(state, "candidate", {"portfolio_payload": "jsonb", "screening_features": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["candidate"]["screening_features"] == "jsonb"
    role_event = talent_onboarding_receive_event(
        state,
        {"event_id": "evt_role_ops", "event_type": "RoleChanged", "payload": {"tenant": "tenant_ops", "role_id": "role_ops", "title": "Operations Analyst"}},
    )
    state = role_event["state"]
    assert role_event["handler"]["status"] == "processed"
    duplicate = talent_onboarding_receive_event(
        state,
        {"event_id": "evt_role_ops", "event_type": "RoleChanged", "payload": {"tenant": "tenant_ops", "role_id": "role_ops", "title": "Operations Analyst"}},
    )
    assert duplicate["duplicate"] is True
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
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == TALENT_ONBOARDING_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = talent_onboarding_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["required_event_topic"] == TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == TALENT_ONBOARDING_OWNED_TABLES
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
            "talent_onboarding.event",
            "talent_onboarding.configure",
            "talent_onboarding.audit",
            "talent_onboarding.read",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 10
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == TALENT_ONBOARDING_OWNED_TABLES

    boundary = talent_onboarding_verify_owned_table_boundary(
        ("candidate", "RoleChanged", "role_projection", "POST /notifications", "talent_onboarding_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = talent_onboarding_verify_owned_table_boundary(("personnel_identity",))
    assert violation["ok"] is False
    assert violation["violations"] == ("personnel_identity",)


def test_talent_onboarding_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = talent_onboarding_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        talent_onboarding_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        talent_onboarding_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Talent Onboarding parameter"):
        talent_onboarding_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        talent_onboarding_register_schema_extension(state, "personnel_identity", {"candidate_ref": "jsonb"})

    configured = talent_onboarding_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TALENT_ONBOARDING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_countries": ("US",),
            "allowed_candidate_sources": ("referral",),
            "allowed_check_providers": ("trusted_screen",),
            "allowed_task_types": ("identity",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = talent_onboarding_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = talent_onboarding_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
