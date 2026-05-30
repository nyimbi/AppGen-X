from pyAppGen.pbcs.education_student_lifecycle.agent import document_instruction_plan
from pyAppGen.pbcs.education_student_lifecycle.services import EducationStudentLifecycleService
from pyAppGen.pbcs.education_student_lifecycle.student_lifecycle_app import (
    activate_enrollment,
    award_credential,
    build_student_lifecycle_workbench,
    controls_contract,
    empty_student_lifecycle_state,
    evaluate_degree_audit,
    finalize_assessment_result,
    forms_contract,
    maintain_curriculum_plan,
    open_advising_case,
    prepare_graduation_clearance,
    project_student_risk,
    record_engagement_projection,
    record_hold_projection,
    record_intervention_plan,
    record_transfer_credit,
    register_course_attempt,
    register_student_applicant,
    review_applicant_documents,
    single_pbc_app_contract,
    student_lifecycle_app_smoke_test,
    submit_academic_petition,
    wizards_contract,
)


def test_single_pbc_app_has_forms_wizards_controls_and_database_contract():
    app = single_pbc_app_contract()

    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert {form["command"] for form in forms_contract()["forms"]} >= {
        "register_student_applicant",
        "review_applicant_documents",
        "activate_enrollment",
        "maintain_curriculum_plan",
        "register_course_attempt",
        "open_advising_case",
        "submit_academic_petition",
        "award_credential",
    }
    assert any(wizard["wizard_id"] == "graduation_clearance_wizard" for wizard in wizards_contract()["wizards"])
    assert all(control["blocks_on_failure"] for control in controls_contract()["controls"])


def test_admissions_enrollment_and_degree_audit_flow_can_complete():
    state = empty_student_lifecycle_state()
    applicant = register_student_applicant(
        state,
        {
            "applicant_id": "app-a",
            "student_name": "Amina Rao",
            "program_code": "BSCS",
            "catalog_year": 2026,
            "intake_term": "2026-FALL",
            "application_stage": "application_submitted",
            "decision_status": "pending",
        },
    )
    document = review_applicant_documents(
        applicant["state"],
        {
            "applicant_id": "app-a",
            "document_type": "transcript",
            "authenticity_status": "verified",
            "reviewer": "admissions-1",
            "confidence": 0.96,
        },
    )
    accepted = register_student_applicant(
        document["state"],
        {
            "applicant_id": "app-a",
            "student_name": "Amina Rao",
            "program_code": "BSCS",
            "catalog_year": 2026,
            "intake_term": "2026-FALL",
            "application_stage": "accepted",
            "decision_status": "accepted",
            "required_documents": ("transcript",),
            "documents_received": ("transcript",),
        },
    )
    enrollment = activate_enrollment(accepted["state"], {"applicant_id": "app-a", "student_id": "student-a", "term": "2026-FALL"})
    plan = maintain_curriculum_plan(
        enrollment["state"],
        {
            "student_id": "student-a",
            "program_code": "BSCS",
            "catalog_year": 2026,
            "required_credits": 6,
            "requirements": ("CS101", "CS102"),
            "required_competencies": ("communication",),
        },
    )
    course = register_course_attempt(
        plan["state"],
        {
            "student_id": "student-a",
            "course_code": "CS101",
            "term": "2026-FALL",
            "status": "completed",
            "grade": "A",
            "credits": 3,
            "prerequisites_satisfied": True,
        },
    )
    transfer = record_transfer_credit(
        course["state"],
        {
            "student_id": "student-a",
            "source_institution": "Regional College",
            "source_course": "ENG101",
            "equivalency": "GEN-communication",
            "credits_awarded": 3,
        },
    )
    assessment = finalize_assessment_result(
        transfer["state"],
        {
            "student_id": "student-a",
            "assessment_type": "capstone",
            "score": 91,
            "competencies": ("communication",),
            "achieved": True,
            "moderation_status": "final",
            "scorer": "faculty-1",
        },
    )
    audit = evaluate_degree_audit(assessment["state"], {"student_id": "student-a"})
    clearance = prepare_graduation_clearance(audit["state"], {"student_id": "student-a"})
    credential = award_credential(clearance["state"], {"student_id": "student-a", "program_code": "BSCS"})

    assert applicant["ok"] is True
    assert document["ok"] is True
    assert accepted["ok"] is True
    assert enrollment["ok"] is True
    assert audit["degree_audit"]["status"] == "complete"
    assert clearance["graduation_clearance"]["status"] == "ready"
    assert credential["credential"]["status"] == "conferred"


def test_registration_and_intervention_controls_block_bad_actions():
    state = empty_student_lifecycle_state()
    blocked_attempt = register_course_attempt(
        state,
        {
            "student_id": "student-b",
            "course_code": "CS201",
            "term": "2026-FALL",
            "credits": 3,
            "prerequisites_satisfied": False,
        },
    )
    case = open_advising_case(state, {"case_id": "case-b", "student_id": "student-b", "case_type": "risk_intervention"})
    intervention = record_intervention_plan(
        case["state"],
        {
            "case_id": "case-b",
            "student_id": "student-b",
            "objective": "Mandate coaching",
            "high_impact": True,
            "reviewer_confirmed": False,
        },
    )

    assert blocked_attempt["ok"] is False
    assert "active_enrollment_required" in blocked_attempt["course_attempt"]["blockers"]
    assert "missing_prerequisite_or_override" in blocked_attempt["course_attempt"]["blockers"]
    assert intervention["ok"] is False
    assert "human_review_required" in intervention["intervention_plan"]["blockers"]


def test_risk_petition_hold_and_workbench_queues_surface_operating_backlog():
    state = empty_student_lifecycle_state()
    hold = record_hold_projection(
        state,
        {"hold_id": "hold-a", "student_id": "student-c", "hold_type": "finance", "blocking_actions": ("register_course", "graduate")},
    )
    engagement = record_engagement_projection(
        hold["state"],
        {"student_id": "student-c", "attendance_rate": 0.52, "risk_contribution": 0.2, "missing_work_flag": True},
    )
    petition = submit_academic_petition(
        engagement["state"],
        {
            "petition_id": "pet-a",
            "student_id": "student-c",
            "petition_type": "late_drop",
            "requested_exception": "Late withdrawal",
            "evidence": ("advisor_note",),
        },
    )
    risk = project_student_risk(petition["state"], {"student_id": "student-c", "gpa": 1.7})
    workbench = build_student_lifecycle_workbench(risk["state"])

    assert hold["ok"] is True
    assert petition["ok"] is True
    assert risk["student_risk_signal"]["risk_band"] == "high"
    assert workbench["queue_counts"]["high_risk_students"] == 1
    assert workbench["queue_counts"]["petition_review"] == 1
    assert workbench["queue_counts"]["exception_backlog"] >= 1


def test_graduation_clearance_blocks_when_hold_present():
    state = empty_student_lifecycle_state()
    applicant = register_student_applicant(
        state,
        {
            "applicant_id": "app-d",
            "program_code": "BBA",
            "catalog_year": 2026,
            "application_stage": "accepted",
            "decision_status": "accepted",
            "required_documents": (),
        },
    )
    enrollment = activate_enrollment(applicant["state"], {"applicant_id": "app-d", "student_id": "student-d", "term": "2026-FALL"})
    plan = maintain_curriculum_plan(
        enrollment["state"],
        {
            "student_id": "student-d",
            "program_code": "BBA",
            "catalog_year": 2026,
            "required_credits": 0,
            "requirements": ("BUS499",),
            "required_competencies": (),
        },
    )
    hold = record_hold_projection(plan["state"], {"student_id": "student-d", "hold_type": "disciplinary", "blocking_actions": ("graduate",)})
    audit = evaluate_degree_audit(hold["state"], {"student_id": "student-d"})
    clearance = prepare_graduation_clearance(audit["state"], {"student_id": "student-d"})

    assert audit["ok"] is False
    assert "graduation_blocking_hold_present" in audit["degree_audit"]["blockers"]
    assert clearance["ok"] is False
    assert clearance["graduation_clearance"]["status"] == "blocked"


def test_agent_document_plan_is_stable_and_domain_routed():
    first = document_instruction_plan("degree audit packet", "prepare graduation review")
    second = document_instruction_plan("degree audit packet", "prepare graduation review")
    petition = document_instruction_plan("petition memo", "submit waiver petition")

    assert first["document_digest"] == second["document_digest"]
    assert first["domain_plan"]["target_table"] == "education_student_lifecycle_degree_audit"
    assert petition["domain_plan"]["proposed_operation"] == "submit_academic_petition"
    assert first["requires_human_confirmation"] is True


def test_stateful_service_executes_domain_app_commands_and_queries():
    service = EducationStudentLifecycleService()
    applicant = service.register_student_applicant({"applicant_id": "app-svc", "program_code": "BSCS", "required_documents": (), "application_stage": "accepted", "decision_status": "accepted"})
    enrollment = service.activate_enrollment({"applicant_id": "app-svc", "student_id": "student-svc", "term": "2026-FALL"})
    workbench = service.build_student_lifecycle_workbench({})

    assert applicant["ok"] is True
    assert enrollment["ok"] is True
    assert workbench["ok"] is True
    assert "app-svc" in service.state["applicants"]
    assert any(item.get("student_id") == "student-svc" for item in service.state["enrollments"].values())


def test_student_lifecycle_app_smoke_covers_end_to_end_flow():
    assert student_lifecycle_app_smoke_test()["ok"] is True
