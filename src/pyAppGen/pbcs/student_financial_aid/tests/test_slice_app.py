from pyAppGen.pbcs.student_financial_aid.slice_app import (
    BUSINESS_TABLES,
    EVENT_TABLES,
    build_release_evidence,
    build_standalone_app,
    dispatch_route,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
    slice_app_smoke_test,
    verify_owned_table_boundary,
)


def test_slice_app_bootstraps_owned_tables_and_application_flow():
    app = build_standalone_app()
    year = app.setup_aid_year({"tenant": "tenant-a", "aid_year_code": "2026-2027", "owner": "director"})
    profile = app.create_student_aid_profile({"tenant": "tenant-a", "aid_year_code": "2026-2027", "student_id": "STU-1", "student_name": "Amina Omari"})
    application = app.intake_aid_application({
        "tenant": "tenant-a",
        "aid_year_code": "2026-2027",
        "student_aid_profile_id": profile["record"]["id"],
        "application_id": "APP-1",
        "student_aid_index": 1500,
        "verification_selected": True,
        "documents": ("tax-transcript", "identity-form"),
    })
    workbench = app.query_workbench("tenant-a")
    assert year["ok"] is True
    assert profile["ok"] is True
    assert application["ok"] is True
    assert workbench["summary"]["application_count"] == 1
    assert len(application["verification_items"]) == 3


def test_need_packaging_disbursement_and_exception_flow_is_executable():
    app = build_standalone_app()
    profile = app.create_student_aid_profile({"tenant": "tenant-b", "aid_year_code": "2026-2027", "student_id": "STU-2"})
    budget = app.capture_cost_of_attendance({"tenant": "tenant-b", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "tuition": 10000, "housing": 5000})
    need = app.analyze_need({"tenant": "tenant-b", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "coa_total": budget["total"], "student_aid_index": 1200, "external_resources": 500})
    package = app.package_awards({"tenant": "tenant-b", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "unmet_need": need["unmet_need"], "coa_total": budget["total"], "external_resources": 500})
    disbursement = app.schedule_disbursement({"tenant": "tenant-b", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "award_package_id": package["record"]["id"], "scheduled_amount": package["record"]["amount"]})
    exception = app.review_return_refund_overaward({"tenant": "tenant-b", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "disbursed_amount": package["record"]["amount"], "earned_percent": 0.4})
    assert need["ok"] is True
    assert package["ok"] is True
    assert package["award_lines"]
    assert disbursement["ok"] is True
    assert exception["ok"] is True


def test_professional_judgment_appeal_route_and_assistant_previews_are_executable():
    app = build_standalone_app()
    profile = app.create_student_aid_profile({"tenant": "tenant-c", "aid_year_code": "2026-2027", "student_id": "STU-3"})
    judgment = app.submit_professional_judgment({"tenant": "tenant-c", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "status": "approved"})
    appeal = app.record_appeal({"tenant": "tenant-c", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "professional_judgment_case_id": judgment["record"]["id"], "committee_decision": "approved"})
    route = dispatch_route("GET", "/student-financial-aid-workbench", {"tenant": "tenant-c"}, app=app)
    document_plan = app.document_instruction_plan("Appeal memo and SAP plan", "update appeal and sap")
    crud_plan = app.datastore_crud_plan("update", table=BUSINESS_TABLES[19], payload={"status": "approved"})
    assert judgment["ok"] is True
    assert appeal["ok"] is True
    assert route["ok"] is True
    assert document_plan["ok"] is True
    assert crud_plan["ok"] is True


def test_event_idempotency_boundary_and_release_audits_hold():
    app = build_standalone_app()
    handled = app.receive_event({"event_type": "PolicyChanged", "tenant": "tenant-d", "idempotency_key": "evt-1"})
    duplicate = app.receive_event({"event_type": "PolicyChanged", "tenant": "tenant-d", "idempotency_key": "evt-1"})
    unknown = app.receive_event({"event_type": "UnexpectedEvent", "tenant": "tenant-d", "idempotency_key": "evt-2"})
    assert handled["ok"] is True
    assert duplicate["duplicate"] is True
    assert unknown["ok"] is False
    assert verify_owned_table_boundary(BUSINESS_TABLES + EVENT_TABLES)["ok"] is True
    assert verify_owned_table_boundary(("foreign_table",))["ok"] is False
    assert slice_app_smoke_test()["ok"] is True
    assert pbc_source_artifact_contract()["ok"] is True
    assert pbc_implementation_release_audit()["ok"] is True
    assert pbc_generation_smoke_audit()["ok"] is True
    evidence = build_release_evidence()
    assert evidence["ok"] is True
    assert {check["id"] for check in evidence["checks"]} >= {
        "pbc_source_artifact_contract",
        "pbc_implementation_release_audit",
        "pbc_generation_smoke_audit",
    }
