from pyAppGen.pbcs.advertising_campaign_operations import (
    advertising_campaign_operations_attempt_launch_campaign,
    advertising_campaign_operations_create_campaign_plan,
    advertising_campaign_operations_empty_state,
    advertising_campaign_operations_query_workbench,
    advertising_campaign_operations_review_launch_readiness,
)
from pyAppGen.pbcs.advertising_campaign_operations.agent import campaign_brief_preview, launch_readiness_preview
from pyAppGen.pbcs.advertising_campaign_operations.services import AdvertisingCampaignOperationsService


def _brief(channels=("search", "social"), dependencies=("tracking-tags", "creative-final")):
    return {
        "objective": "Acquire qualified trial signups",
        "offer": "Free 30-day trial",
        "audience_promise": "Show only to in-market buyers",
        "channels": channels,
        "primary_kpi": "qualified_signups",
        "guardrails": (
            {"metric": "cpa", "operator": "lte", "value": 40, "window": "flight"},
            {"metric": "brand_safety", "operator": "inform", "value": "strict"},
        ),
        "launch_dependencies": dependencies,
    }


def test_campaign_plan_creation_is_deterministic_for_equivalent_briefs():
    state = advertising_campaign_operations_empty_state()
    first = advertising_campaign_operations_create_campaign_plan(
        state,
        {"tenant": "tenant-a", "code": "SPRING-LAUNCH", "brief": _brief()},
    )
    second = advertising_campaign_operations_create_campaign_plan(
        state,
        {
            "tenant": "tenant-a",
            "code": "SPRING-LAUNCH",
            "brief": _brief(channels=("social", "search"), dependencies=("creative-final", "tracking-tags")),
        },
    )

    assert first["ok"] is True
    assert second["ok"] is True
    assert first["campaign_plan"]["brief"] == second["campaign_plan"]["brief"]
    assert first["campaign_plan"]["brief_fingerprint"] == second["campaign_plan"]["brief_fingerprint"]
    assert first["campaign_plan"]["launch_gate"]["ready"] is False
    assert first["state"]["outbox"][-1]["event_type"] == "AdvertisingCampaignOperationsCreated"


def test_service_and_agent_surfaces_reject_incomplete_campaign_briefs():
    service = AdvertisingCampaignOperationsService()
    plan = service.create_campaign_plan({"tenant": "tenant-a", "brief": {"objective": "Acquire signups"}})
    agent_preview = campaign_brief_preview({"tenant": "tenant-a", "brief": {"objective": "Acquire signups"}})

    assert plan["ok"] is False
    assert "offer" in plan["missing_fields"]
    assert agent_preview["ok"] is False
    assert "channels" in agent_preview["missing_fields"]


def test_launch_readiness_blocks_then_allows_launch_with_complete_evidence():
    state = advertising_campaign_operations_empty_state()
    created = advertising_campaign_operations_create_campaign_plan(
        state,
        {"tenant": "tenant-a", "code": "SPRING-LAUNCH", "brief": _brief()},
    )

    blocked_review = advertising_campaign_operations_review_launch_readiness(
        created["state"],
        {"campaign_id": "SPRING-LAUNCH"},
    )
    blocked_attempt = advertising_campaign_operations_attempt_launch_campaign(
        created["state"],
        {"campaign_id": "SPRING-LAUNCH"},
    )

    readiness = {
        "budget_approved": True,
        "creative_approved": True,
        "audience_ready": True,
        "placements_ready": True,
        "tracking_ready": True,
        "suppliers_eligible": True,
        "policy_compliant": True,
        "dependency_status": {
            "tracking-tags": {"ready": True, "detail": "tags verified"},
            "creative-final": True,
        },
    }
    ready_attempt = advertising_campaign_operations_attempt_launch_campaign(
        created["state"],
        {"campaign_id": "SPRING-LAUNCH", "readiness": readiness},
    )
    ready_preview = launch_readiness_preview(
        {"campaign_plan": created["campaign_plan"], "readiness": readiness}
    )
    workbench = advertising_campaign_operations_query_workbench(
        ready_attempt["state"],
        {"tenant": "tenant-a"},
    )

    assert blocked_review["ok"] is True
    assert blocked_review["launch_report"]["ready"] is False
    assert any(blocker["check"] == "budget_approved" for blocker in blocked_review["launch_report"]["blockers"])
    assert blocked_attempt["ok"] is False
    assert blocked_attempt["state"]["outbox"][-1]["event_type"] == "AdvertisingCampaignOperationsExceptionOpened"

    assert ready_attempt["ok"] is True
    assert ready_attempt["record"]["status"] == "ready_for_launch"
    assert ready_attempt["state"]["outbox"][-1]["event_type"] == "AdvertisingCampaignOperationsApproved"
    assert ready_preview["launch_report"]["ready"] is True
    assert workbench["command_center"]["summary"]["ready_count"] == 1
