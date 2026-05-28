from pyAppGen.pbcs.case_knowledge_management.application import create_app
from pyAppGen.pbcs.case_knowledge_management.routes import dispatch_route
from pyAppGen.pbcs.case_knowledge_management.services import CaseKnowledgeManagementService


def test_case_to_resolution_and_knowledge_flow():
    app = create_app()

    created = app.create_support_case(
        {
            "tenant": "tenant-acme",
            "title": "API token rotation caused 500s",
            "summary": "Enterprise customers see 500 errors after rotating a token.",
            "severity": "high",
            "product_area": "platform",
            "customer_ref": "acme-01",
            "contact": {"name": "Mara", "email": "mara@acme.test"},
        }
    )
    case_id = created["record"]["id"]

    classified = app.classify_case({"case_id": case_id})
    routed = app.route_case_queue({"case_id": case_id})
    assigned = app.assign_case({"case_id": case_id, "candidate_agents": ("agent-zoe", "agent-musa")})
    sla = app.start_sla_timer({"case_id": case_id})
    interaction = app.record_case_interaction({"case_id": case_id, "summary": "Captured failing trace IDs."})
    escalation = app.open_case_escalation({"case_id": case_id, "reason": "Major customer impact."})
    root_cause = app.identify_root_cause({"case_id": case_id, "category": "token", "corrective_action": "Re-issue the edge token."})
    resolution = app.resolve_case({"case_id": case_id, "summary": "Re-issued token and restored traffic.", "confirmed": True})

    article = app.publish_knowledge_article(
        {
            "tenant": "tenant-acme",
            "title": "Recovering from failed API token rotation",
            "product_area": "platform",
            "body": "Re-issue the failing token, confirm regional health, and validate replay traffic.",
            "approved_by": "approver-1",
        }
    )
    article_id = article["record"]["id"]
    feedback = app.capture_article_feedback({"tenant": "tenant-acme", "article_id": article_id, "source_case_id": case_id, "rating": 5, "theme": "fast_resolution"})
    quality = app.score_article_quality({"tenant": "tenant-acme", "article_id": article_id, "readability": 0.9, "deflection_rate": 0.6})
    recommendation = app.recommend_next_best_resolution({"case_id": case_id})

    assert created["ok"] is True
    assert classified["record"]["product_component"] == "platform"
    assert routed["queue"]["code"] == "api-platform"
    assert assigned["record"]["assignee_id"] in {"agent-zoe", "agent-musa"}
    assert sla["record"]["risk_level"] in {"watch", "high"}
    assert interaction["record"]["summary"] == "Captured failing trace IDs."
    assert escalation["record"]["target_team"] == "product-engineering"
    assert root_cause["record"]["category"] == "token"
    assert resolution["record"]["confirmed"] is True
    assert article["record"]["lifecycle_state"] == "published"
    assert feedback["record"]["rating"] == 5
    assert quality["article"]["quality_score"] >= 0.7
    assert recommendation["record"]["citations"]
    assert any(event["event_type"] == "CaseResolved" for event in app.snapshot()["outbox"])


def test_governed_crud_and_event_idempotency_boundaries():
    app = create_app()

    blocked = app.governed_datastore_crud(
        "create",
        "case_queue",
        {
            "tenant": "default",
            "code": "new-queue",
            "label": "New Queue",
            "region": "global",
            "language": "en",
            "product_scope": "general",
            "capacity_limit": 10,
            "active_load": 0,
            "health": "healthy",
        },
        confirmed=False,
    )
    allowed = app.governed_datastore_crud(
        "create",
        "case_queue",
        {
            "tenant": "default",
            "code": "new-queue",
            "label": "New Queue",
            "region": "global",
            "language": "en",
            "product_scope": "general",
            "capacity_limit": 10,
            "active_load": 0,
            "health": "healthy",
        },
        confirmed=True,
    )
    foreign = app.governed_datastore_crud("update", "foreign_table", {"id": "x"}, confirmed=True)

    first = app.receive_event({"event_type": "SearchIndexRefreshed", "event_id": "evt-1", "payload": {"tenant": "default", "article_id": "article-api-timeout-playbook"}})
    duplicate = app.receive_event({"event_type": "SearchIndexRefreshed", "event_id": "evt-1", "payload": {"tenant": "default", "article_id": "article-api-timeout-playbook"}})
    dead = app.receive_event({"event_type": "NotSupported", "event_id": "evt-bad", "payload": {"tenant": "default"}})

    assert blocked["reason"] == "confirmation_required"
    assert allowed["ok"] is True
    assert foreign["reason"] == "foreign_table_rejected"
    assert first["ok"] is True
    assert duplicate["duplicate"] is True
    assert dead["ok"] is False


def test_routes_and_service_wrap_the_same_slice_shape():
    service = CaseKnowledgeManagementService()
    created = service.create_support_case(
        {
            "tenant": "tenant-route",
            "title": "Billing invoice mismatch",
            "summary": "Invoices include duplicate charges after retry.",
            "severity": "medium",
            "product_area": "billing",
            "customer_ref": "cust-billing",
        }
    )
    case_id = created["result"]["record"]["id"]

    routed = dispatch_route("/support-cases/route", {"case_id": case_id}, method="POST", state=created["state"])
    workbench = dispatch_route("/knowledge-workbench", {}, method="GET", state=routed["state"])

    assert created["ok"] is True
    assert routed["ok"] is True
    assert workbench["ok"] is True
    assert workbench["result"]["metrics"]["open_cases"] >= 1
