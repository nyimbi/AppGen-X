"""Focused standalone tests for insurance underwriting."""

from pyAppGen.pbcs.insurance_underwriting import smoke_test
from pyAppGen.pbcs.insurance_underwriting import standalone as standalone_app
from pyAppGen.pbcs.insurance_underwriting import agent, models, release_evidence, routes, services, ui


def test_standalone_store_executes_core_underwriting_lifecycle():
    store = models.InsuranceUnderwritingStandaloneStore()
    try:
        submission = store.create_submission(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "product_line": "property",
                "applicant_name": "Acme Fabrication",
                "jurisdiction": "US-IL",
                "requested_limit": 1200000.0,
                "declared_revenue": 4200000.0,
                "effective_date": "2026-07-01",
                "exposure_locations": ("Chicago", "Aurora"),
                "documents": ("application.pdf", "loss_run.pdf"),
                "prior_losses": ({"year": 2024, "paid": 15000},),
            }
        )
        risk = store.build_risk_profile(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "industry_code": "MFG",
                "hazard_factors": ("fire", "heavy_equipment"),
                "catastrophe_score": 0.18,
                "prior_loss_count": 1,
            }
        )
        factor = store.review_rating_factor(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "factor_id": "factor-test",
                "factor_type": "sprinkler_credit",
                "selected_value": 0.94,
                "weight": 0.12,
                "source": "inspection",
            }
        )
        quote = store.generate_quote(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "quote_id": "quote-test",
                "scenario_name": "quoted",
            }
        )
        decision = store.issue_underwriting_decision(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "quote_id": "quote-test",
                "decision_id": "decision-test",
                "authority_level": "senior",
                "approved_by": "senior-underwriter",
            }
        )
        exclusion = store.record_exclusion(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "quote_id": "quote-test",
                "exclusion_id": "excl-test",
                "clause_code": "HOTWORK",
                "reason": "Uncontrolled hot work exposure",
                "customer_explanation": "Hot work remains excluded until the controls survey is complete.",
            }
        )
        bind = store.assemble_bind_package(
            {
                "submission_id": "submission-test",
                "tenant": "tenant-test",
                "quote_id": "quote-test",
                "bind_package_id": "bind-test",
                "subjectivities": ({"name": "signed_application", "satisfied": True},),
                "documents": ("signed_application",),
                "payment_confirmed": True,
            }
        )
        event = store.receive_event(
            {
                "event_type": "PolicyChanged",
                "source_pbc": "policy_admin",
                "tenant": "tenant-test",
                "payload": {"submission_id": "submission-test", "status": "issued"},
                "idempotency_key": "policy-change-test",
            }
        )
        detail = store.get_submission_detail("submission-test")
        workbench = store.build_workbench("tenant-test")
        timeline = store.build_timeline("submission-test")
        assert all(item["ok"] is True for item in (submission, risk, factor, quote, decision, exclusion, bind, event, detail, workbench, timeline))
        assert workbench["submission_count"] == 1
        assert detail["submission"]["submission_id"] == "submission-test"
        assert timeline["event_count"] >= 4
    finally:
        store.close()


def test_quote_generation_rejects_incomplete_submission():
    store = models.InsuranceUnderwritingStandaloneStore()
    try:
        store.create_submission(
            {
                "submission_id": "incomplete-submission",
                "tenant": "tenant-test",
                "product_line": "property",
                "applicant_name": "Sparse Applicant",
                "jurisdiction": "US-TX",
                "requested_limit": 500000.0,
            }
        )
        result = store.generate_quote({"submission_id": "incomplete-submission", "tenant": "tenant-test"})
        assert result["ok"] is False
        assert result["reason"] == "submission_incomplete"
    finally:
        store.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.InsuranceUnderwritingStandaloneService()
    try:
        intake = routes.dispatch_standalone_route(
            "POST",
            "/app/insurance-underwriting/workflows/intake",
            {
                "submission_id": "route-test",
                "tenant": "tenant-route",
                "product_line": "property",
                "applicant_name": "Route Risk",
                "jurisdiction": "US-CA",
                "requested_limit": 900000.0,
                "declared_revenue": 3000000.0,
                "effective_date": "2026-07-01",
                "exposure_locations": ("San Diego",),
                "documents": ("application.pdf",),
                "prior_losses": (),
            },
            service=service,
        )
        bind = routes.dispatch_standalone_route(
            "POST",
            "/app/insurance-underwriting/workflows/quote-to-bind",
            {
                "submission_id": "route-test",
                "tenant": "tenant-route",
                "authority_level": "chief",
                "approved_by": "chief-underwriter",
            },
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/insurance-underwriting/workbench",
            {"tenant": "tenant-route"},
            service=service,
        )
        rendered = ui.insurance_underwriting_render_standalone_workbench(workbench["result"]["result"])
        document_plan = agent.document_instruction_plan("inspection report", "bind this account after quote review")
        crud_plan = agent.datastore_crud_plan("create", "insurance_underwriting_underwriting_submission", {"submission_id": "route-test"})
        app_contract = standalone_app.insurance_underwriting_standalone_app_contract()
        smoke = standalone_app.insurance_underwriting_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert intake["ok"] is True
        assert bind["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert evidence["documentation"]["ok"] is True
    finally:
        service.close()


def test_package_smoke_test_passes():
    assert smoke_test()["ok"] is True
