"""Focused standalone one-PBC tests for customer_360."""

from pathlib import Path

from .. import agent, models, release_evidence, routes, services, standalone, ui


def test_standalone_store_persists_core_customer_flows():
    store = models.Customer360StandaloneStore()
    try:
        profile = store.create_profile(
            {
                "profile_id": "cust_test",
                "tenant": "tenant_test",
                "display_name": "Ada Customer",
                "region": "US",
            }
        )
        identity = store.link_identity(
            {
                "identity_id": "id_test",
                "tenant": "tenant_test",
                "profile_id": "cust_test",
                "identity_type": "email",
                "value": "ada@example.com",
                "confidence": 0.99,
                "verified": True,
            }
        )
        consent = store.record_consent(
            {
                "consent_id": "consent_test",
                "tenant": "tenant_test",
                "profile_id": "cust_test",
                "purpose": "marketing",
                "region": "US",
                "status": "granted",
                "confidence": 0.95,
            }
        )
        preference = store.set_preference(
            {
                "preference_id": "pref_test",
                "tenant": "tenant_test",
                "profile_id": "cust_test",
                "channel": "email",
                "topic": "offers",
                "status": "opt_in",
            }
        )
        touchpoint = store.capture_touchpoint(
            {
                "touchpoint_id": "tp_test",
                "tenant": "tenant_test",
                "profile_id": "cust_test",
                "channel": "web",
                "source": "portal",
            }
        )
        engagement = store.ingest_engagement_event(
            {
                "event_id": "eng_test",
                "tenant": "tenant_test",
                "profile_id": "cust_test",
                "event_type": "purchase",
                "channel": "web",
                "value": 200.0,
            }
        )
        merge_case = store.open_merge_case(
            {
                "merge_case_id": "merge_test",
                "tenant": "tenant_test",
                "winning_profile_id": "cust_test",
                "candidate_profile_id": "cust_duplicate",
                "match_score": 0.91,
                "reason": "same_email",
            }
        )
        resolved = store.resolve_merge_case("merge_test", "operator_test")
        inbox = store.receive_event(
            {
                "event_id": "invoice_test",
                "event_type": "InvoiceIssued",
                "payload": {
                    "tenant": "tenant_test",
                    "profile_id": "cust_test",
                    "amount": 200.0,
                },
            }
        )
        timeline = store.build_timeline("cust_test")
        workbench = store.build_workbench("tenant_test")
        assert all(
            item["ok"] is True
            for item in (profile, identity, consent, preference, touchpoint, engagement, merge_case, resolved, inbox, timeline, workbench)
        )
        assert timeline["event_count"] >= 5
        assert workbench["profile_count"] == 1
        assert workbench["open_merge_case_count"] == 0
        assert workbench["outbox_count"] >= 7
    finally:
        store.close()


def test_standalone_service_routes_ui_agent_and_release_surface():
    service = services.Customer360StandaloneService()
    try:
        create = routes.dispatch_standalone_route(
            "POST",
            "/app/customer-360/profiles",
            {
                "profile_id": "cust_route_test",
                "tenant": "tenant_route_test",
                "display_name": "Route Customer",
                "region": "US",
            },
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/customer-360/workbench",
            {"tenant": "tenant_route_test"},
            service=service,
        )
        rendered = ui.customer_360_render_standalone_workbench(workbench["result"]["result"])
        document_plan = agent.document_instruction_plan(
            "identity card",
            "onboard customer cust_route_test and record consent",
        )
        crud_plan = agent.datastore_crud_plan(
            "create",
            "customer_360_customer_profile",
            {"profile_id": "cust_route_test"},
        )
        app_contract = standalone.customer_360_standalone_app_contract()
        smoke = standalone.customer_360_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert create["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["documentation"]["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
    finally:
        service.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
