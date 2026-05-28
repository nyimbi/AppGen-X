from pyAppGen.pbcs.clinical_trials_management import implementation_contract
from pyAppGen.pbcs.clinical_trials_management import package_discovery_plan
from pyAppGen.pbcs.clinical_trials_management import package_metadata_manifest
from pyAppGen.pbcs.clinical_trials_management import validate_package_metadata
from pyAppGen.pbcs.clinical_trials_management.agent import agent_skill_manifest
from pyAppGen.pbcs.clinical_trials_management.agent import chatbot_interface_contract
from pyAppGen.pbcs.clinical_trials_management.agent import clinical_trials_management_assistant_preview
from pyAppGen.pbcs.clinical_trials_management.agent import datastore_crud_plan
from pyAppGen.pbcs.clinical_trials_management.agent import document_instruction_plan
from pyAppGen.pbcs.clinical_trials_management.config import governance_smoke_test
from pyAppGen.pbcs.clinical_trials_management.controls import clinical_trials_management_control_center
from pyAppGen.pbcs.clinical_trials_management.controls import clinical_trials_management_mutation_preview
from pyAppGen.pbcs.clinical_trials_management.events import event_contract_manifest
from pyAppGen.pbcs.clinical_trials_management.events import validate_event_contract
from pyAppGen.pbcs.clinical_trials_management.forms import clinical_trials_management_form_catalog
from pyAppGen.pbcs.clinical_trials_management.forms import clinical_trials_management_validate_form_payload
from pyAppGen.pbcs.clinical_trials_management.handlers import dispatch_event
from pyAppGen.pbcs.clinical_trials_management.handlers import handler_manifest
from pyAppGen.pbcs.clinical_trials_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.clinical_trials_management.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.clinical_trials_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.clinical_trials_management.routes import api_route_contracts
from pyAppGen.pbcs.clinical_trials_management.routes import dispatch_route
from pyAppGen.pbcs.clinical_trials_management.routes import validate_api_route_contracts
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_command_consent_record
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_command_study_site
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_command_subject
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_command_trial_protocol
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_command_visit_schedule
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_empty_state
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_full_release_simulation
from pyAppGen.pbcs.clinical_trials_management.runtime import clinical_trials_management_runtime_smoke
from pyAppGen.pbcs.clinical_trials_management.schema_contract import build_schema_contract
from pyAppGen.pbcs.clinical_trials_management.seed_data import scenario_library
from pyAppGen.pbcs.clinical_trials_management.seed_data import validate_seed_data
from pyAppGen.pbcs.clinical_trials_management.service_contract import build_service_contract
from pyAppGen.pbcs.clinical_trials_management.services import service_operation_contracts
from pyAppGen.pbcs.clinical_trials_management.ui import clinical_trials_management_render_workbench
from pyAppGen.pbcs.clinical_trials_management.ui import clinical_trials_management_ui_contract
from pyAppGen.pbcs.clinical_trials_management.wizards import clinical_trials_management_plan_wizard
from pyAppGen.pbcs.clinical_trials_management.wizards import clinical_trials_management_wizard_catalog


def test_generated_schema_service_and_release_evidence():
    assert build_schema_contract()["ok"] is True
    assert build_service_contract()["ok"] is True
    assert build_release_evidence()["ok"] is True
    assert release_readiness_manifest()["ok"] is True
    assert validate_release_evidence()["ok"] is True


def test_manifest_and_event_contract():
    assert implementation_contract()["pbc"] == "clinical_trials_management"
    assert event_contract_manifest()["ok"] is True
    assert validate_event_contract()["ok"] is True


def test_forms_wizards_controls_and_workbench_are_executable():
    simulation = clinical_trials_management_full_release_simulation()
    assert simulation["ok"] is True
    assert clinical_trials_management_form_catalog()["ok"] is True
    assert clinical_trials_management_validate_form_payload(
        "serious_event_reporting",
        {
            "tenant": "tenant-smoke",
            "adverse_event_id": "AE-101",
            "subject_id": "SUBJ-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "seriousness": "serious",
            "grade": "3",
            "expectedness": "expected",
            "reported_within_hours": 12,
        },
    )["ok"] is True
    assert clinical_trials_management_wizard_catalog()["ok"] is True
    assert clinical_trials_management_plan_wizard("subject_enrollment", {"site_id": "SITE-001"})["ok"] is True
    control_center = clinical_trials_management_control_center(simulation["state"])
    assert control_center["ok"] is True
    assert control_center["lock_readiness"]["ready"] is True
    ui_contract = clinical_trials_management_ui_contract()
    assert ui_contract["ok"] is True
    rendered = clinical_trials_management_render_workbench(
        simulation["state"],
        tenant="tenant-smoke",
        principal_permissions=tuple(dict.fromkeys(ui_contract["action_permissions"].values())),
    )
    assert rendered["ok"] is True
    assert rendered["metrics"]["lock_ready"] == 1


def test_agent_chatbot_skills_are_domain_specific_and_guarded():
    assert agent_skill_manifest()["ok"] is True
    assert chatbot_interface_contract()["ok"] is True
    document = document_instruction_plan(
        "Safety narrative: grade 3 neutropenia resolved after dose hold.",
        "Update the serious adverse event record.",
        target_entity="adverse_event",
        requested_action="update",
    )
    assert document["ok"] is True
    assert document["citation_required"] is True
    preview = clinical_trials_management_assistant_preview(
        {
            "document_text": "Monitoring memo: consent version mismatch at Site 001.",
            "instructions": "Create a monitoring finding preview only.",
            "target_entity": "monitoring_finding",
            "requested_action": "create",
            "payload": {"finding_id": "MON-002"},
        }
    )
    assert preview["ok"] is True
    assert preview["requires_confirmation"] is True
    assert datastore_crud_plan("update", table="foreign_table")["ok"] is False
    assert clinical_trials_management_mutation_preview("update", "foreign_table")["ok"] is False


def test_enrollment_and_consent_gates_enforce_domain_rules():
    state = clinical_trials_management_empty_state()
    protocol = clinical_trials_management_command_trial_protocol(
        state,
        {"tenant": "tenant-a", "protocol_id": "PROT-A", "protocol_code": "PROT-A", "version": 2, "status": "active"},
    )
    site = clinical_trials_management_command_study_site(
        protocol["state"],
        {
            "tenant": "tenant-a",
            "site_id": "SITE-A",
            "protocol_id": "PROT-A",
            "site_number": "A-01",
            "country": "US",
            "principal_investigator": "Dr. A",
            "ethics_approval": True,
            "contract_executed": True,
            "training_complete": True,
            "delegation_log_ready": True,
        },
    )
    no_consent_subject = clinical_trials_management_command_subject(
        site["state"],
        {
            "tenant": "tenant-a",
            "subject_id": "SUBJ-A",
            "protocol_id": "PROT-A",
            "site_id": "SITE-A",
            "screening_number": "SCR-A",
            "eligibility_evidence_complete": True,
            "exclusion_clear": True,
            "enrollment_requested": True,
        },
    )
    assert no_consent_subject["ok"] is False
    assert "current_consent_required" in no_consent_subject["blocking_gaps"]
    mismatch_consent = clinical_trials_management_command_consent_record(
        site["state"],
        {
            "tenant": "tenant-a",
            "consent_id": "CONS-A",
            "subject_id": "SUBJ-A",
            "protocol_id": "PROT-A",
            "site_id": "SITE-A",
            "consent_version": 1,
            "language": "en",
            "status": "current",
            "signed_on": "2026-05-29",
        },
    )
    assert mismatch_consent["ok"] is False
    assert mismatch_consent["version_matches"] is False


def test_runtime_smoke_and_visit_completion_are_valid():
    smoke = clinical_trials_management_runtime_smoke()
    assert smoke["ok"] is True
    simulation_state = clinical_trials_management_full_release_simulation()["state"]
    visit = clinical_trials_management_command_visit_schedule(
        simulation_state,
        {
            "tenant": "tenant-smoke",
            "visit_id": "VISIT-002",
            "subject_id": "SUBJ-001",
            "protocol_id": "PROT-101",
            "site_id": "SITE-001",
            "visit_code": "C1D8",
            "visit_type": "treatment",
            "target_day": 8,
            "actual_day": 8,
            "required_procedures": ("labs",),
            "completed_procedures": ("labs",),
        },
    )
    assert visit["ok"] is True
    assert visit["record"]["window_classification"] == "on_window"
    assert visit["record"]["status"] == "completed"


def test_registration_plan_is_side_effect_free():
    assert package_metadata_manifest()["pbc"] == "clinical_trials_management"
    assert validate_package_metadata()["ok"] is True
    assert package_discovery_plan()["ok"] is True
    assert package_discovery_plan()["side_effects"] == ()


def test_service_and_route_surface_are_executable():
    assert service_operation_contracts()["ok"] is True
    assert api_route_contracts()["ok"] is True
    assert validate_api_route_contracts()["ok"] is True
    # Source-audit trace: operation_contract
    assert service_operation_contracts()["contracts"]
    assert dispatch_route("GET", "/api/pbc/clinical_trials_management/controls")["ok"] is True


def test_configuration_permissions_and_seed_hooks_are_executable():
    assert governance_smoke_test()["ok"] is True
    assert scenario_library()["ok"] is True
    assert validate_seed_data()["ok"] is True


def test_event_handlers_are_idempotent_and_retryable():
    manifest = handler_manifest()
    assert manifest["ok"] is True
    assert dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-clinical_trials_management"})["ok"] is True
    assert dispatch_event({"event_type": "PolicyChanged", "idempotency_key": "idem-clinical_trials_management"})["duplicate"] is True
    assert dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-clinical_trials_management"})["dead_letter_table"].endswith("dead_letter_event")
