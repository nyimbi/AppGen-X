"""Executable domain behavior tests for the advertising_campaign_operations PBC."""

from __future__ import annotations

from .. import agent
from .. import implementation_contract
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import smoke_test
from .. import standalone
from .. import ui
from ..campaign_planning import build_campaign_plan
from ..campaign_planning import build_command_center_summary
from ..campaign_planning import normalize_campaign_brief
from ..campaign_planning import review_launch_readiness
from ..domain_depth import DOMAIN_OPERATIONS
from ..domain_depth import domain_capability_surface_contract
from ..domain_depth import domain_depth_contract
from ..domain_depth import execute_domain_operation
from ..services import AdvertisingCampaignOperationsService
from ..services import service_operation_contracts
from ..services import service_operation_manifest
from ..workflows import run_campaign_brief_workflow
from ..workflows import run_document_instruction_workflow
from ..workflows import run_launch_gate_workflow
from ..workflows import workflow_catalog


TENANT = "tenant_alpha"
CAMPAIGN_ID = "Q4-GROWTH"

BRIEF = {
    "objective": "Acquire qualified trial signups",
    "offer": "Free 30-day trial",
    "audience_promise": "Reach in-market buyers with category intent",
    "channels": ("search", "social", "display"),
    "primary_kpi": "qualified_signups",
    "guardrails": (
        {"metric": "cpa", "operator": "lte", "value": 45, "severity": "blocker"},
        {"metric": "frequency", "operator": "lte", "value": 4},
    ),
    "launch_dependencies": ("tracking", "creative-final", "supplier-clearance"),
}

READY = {
    "budget_approved": True,
    "creative_approved": True,
    "audience_ready": True,
    "placements_ready": True,
    "tracking_ready": True,
    "suppliers_eligible": True,
    "policy_compliant": True,
    "dependency_status": {
        "tracking": True,
        "creative-final": True,
        "supplier-clearance": True,
    },
}

BLOCKED = {
    "budget_approved": True,
    "creative_approved": False,
    "creative_approved_detail": "Creative legal review is still open.",
    "audience_ready": True,
    "placements_ready": False,
    "tracking_ready": True,
    "suppliers_eligible": True,
    "policy_compliant": True,
    "dependency_status": {
        "tracking": True,
        "creative-final": False,
        "supplier-clearance": True,
    },
}

CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "workbench_limit": 50,
}

SUPPLIER_EVENT = {
    "event_type": "SupplierQualified",
    "event_id": "supplier_evt_001",
    "idempotency_key": "supplier:qualified:001",
    "payload": {"tenant": TENANT, "supplier_id": "supplier_001", "qualified": True},
}


def _configured_state() -> dict:
    state = runtime.advertising_campaign_operations_empty_state()
    state = runtime.advertising_campaign_operations_configure_runtime(state, CONFIGURATION)["state"]
    state = runtime.advertising_campaign_operations_set_parameter(state, "workbench_limit", 50)["state"]
    state = runtime.advertising_campaign_operations_register_rule(
        state,
        {"rule_id": "launch_gate", "scope": "launch_readiness", "status": "active", "required_flags": tuple(READY)[:7]},
    )["state"]
    state = runtime.advertising_campaign_operations_register_schema_extension(
        state,
        "ad_campaign",
        {"brief_fingerprint": "text", "launch_gate": "jsonb"},
    )["state"]
    return state


def _planned_state() -> dict:
    state = _configured_state()
    event = runtime.advertising_campaign_operations_receive_event(state, SUPPLIER_EVENT)
    state = event["state"]
    planned = runtime.advertising_campaign_operations_create_campaign_plan(
        state,
        {"tenant": TENANT, "code": CAMPAIGN_ID, "brief": BRIEF},
    )
    return {"state": planned["state"], "event": event, "planned": planned}


def test_campaign_brief_planning_launch_gate_and_command_center_are_executable() -> None:
    normalized = normalize_campaign_brief(BRIEF)
    incomplete = normalize_campaign_brief({"objective": "Launch trial"})
    plan = build_campaign_plan({"tenant": TENANT, "code": CAMPAIGN_ID, "brief": BRIEF})
    blocked = review_launch_readiness({"campaign_plan": plan["campaign_plan"], "readiness": BLOCKED})
    ready = review_launch_readiness({"campaign_plan": plan["campaign_plan"], "readiness": READY})
    summary = build_command_center_summary((plan["campaign_plan"],))
    brief_workflow = run_campaign_brief_workflow({"tenant": TENANT, "code": CAMPAIGN_ID, "brief": BRIEF})
    launch_workflow = run_launch_gate_workflow({"campaign_plan": plan["campaign_plan"], "readiness": READY})
    document_workflow = run_document_instruction_workflow("Create campaign brief for Q4 trial launch.", "create campaign plan")

    assert normalized["ok"] is True
    assert normalized["brief"]["channels"] == ("display", "search", "social")
    assert len(normalized["brief"]["guardrails"]) == 2
    assert incomplete["ok"] is False and "offer" in incomplete["missing_fields"]
    assert plan["ok"] is True
    assert plan["campaign_plan"]["campaign_id"] == CAMPAIGN_ID
    assert plan["campaign_plan"]["primary_channel"] == "display"
    assert plan["campaign_plan"]["launch_gate"]["ready"] is False
    assert blocked["ok"] is True and blocked["launch_report"]["ready"] is False
    assert any(item["check"] == "creative_approved" for item in blocked["launch_report"]["blockers"])
    assert ready["ok"] is True and ready["launch_report"]["ready"] is True
    assert summary["ok"] is True and summary["summary"]["campaign_count"] == 1
    assert brief_workflow["ok"] is True
    assert launch_workflow["ok"] is True and launch_workflow["result"]["launch_report"]["ready"] is True
    assert document_workflow["ok"] is True and document_workflow["result"]["target_table"] == "advertising_campaign_operations_ad_campaign"


def test_campaign_runtime_events_services_routes_ui_and_agent_are_executable() -> None:
    bundle = _planned_state()
    state = bundle["state"]
    duplicate = runtime.advertising_campaign_operations_receive_event(state, SUPPLIER_EVENT)
    dead = runtime.advertising_campaign_operations_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "bad_evt", "idempotency_key": "bad_evt", "payload": {"tenant": TENANT}},
    )
    blocked_launch = runtime.advertising_campaign_operations_attempt_launch_campaign(state, {"campaign_id": CAMPAIGN_ID, "readiness": BLOCKED})
    launched = runtime.advertising_campaign_operations_attempt_launch_campaign(blocked_launch["state"], {"campaign_id": CAMPAIGN_ID, "readiness": READY})
    query = runtime.advertising_campaign_operations_query_workbench(launched["state"], {"tenant": TENANT})
    workbench = runtime.advertising_campaign_operations_build_workbench_view(tenant=TENANT, state=launched["state"])
    assessment = runtime.advertising_campaign_operations_run_advanced_assessment(launched["state"], {"tenant": TENANT})
    parser = runtime.advertising_campaign_operations_parse_document_instruction("Q4 campaign launch brief", "create campaign plan")
    bad_extension = runtime.advertising_campaign_operations_register_schema_extension(launched["state"], "shared_campaign_table", {"x": "jsonb"})
    schema = runtime.advertising_campaign_operations_build_schema_contract()
    service_contract = runtime.advertising_campaign_operations_build_service_contract()
    api_contract = runtime.advertising_campaign_operations_build_api_contract()
    release = runtime.advertising_campaign_operations_build_release_evidence()
    permissions = runtime.advertising_campaign_operations_permissions_contract()
    boundary_ok = runtime.advertising_campaign_operations_verify_owned_table_boundary(runtime.ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES[:2])
    boundary_bad = runtime.advertising_campaign_operations_verify_owned_table_boundary(("foreign_table",))
    capabilities = runtime.advertising_campaign_operations_runtime_capabilities()
    runtime_smoke = runtime.advertising_campaign_operations_runtime_smoke()

    service = AdvertisingCampaignOperationsService()
    service_config = service.configure_runtime({"configuration": CONFIGURATION})
    service_plan = service.create_campaign_plan({"tenant": TENANT, "code": "SERVICE-Q4", "brief": BRIEF})
    service_launch = service.attempt_launch_campaign({"campaign_id": "SERVICE-Q4", "readiness": READY})
    service_query = service.query_workbench({"tenant": TENANT})
    route_validation = routes.validate_api_route_contracts()
    route_plan = routes.dispatch_route("POST", "/api/pbc/advertising_campaign_operations/campaign-plans", {"tenant": TENANT, "code": "ROUTE-Q4", "brief": BRIEF})
    route_assistant = routes.dispatch_route("POST", "/api/pbc/advertising_campaign_operations/assistant/document-plans", {"document": "Campaign brief", "instruction": "create campaign plan"})
    ui_contract = ui.advertising_campaign_operations_ui_contract()
    rendered = ui.advertising_campaign_operations_render_workbench(launched["state"], tenant=TENANT)
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan("Campaign brief for Q4 launch", "create campaign plan")
    creative_plan = agent.document_instruction_plan("Creative refresh request", "update creative asset")
    crud_plan = agent.datastore_crud_plan("create", "advertising_campaign_operations_ad_campaign", {"campaign_id": CAMPAIGN_ID})
    blocked_plan = agent.datastore_crud_plan("update", "shared_campaign_table", {})
    contribution = agent.composed_agent_contribution()

    assert bundle["event"]["ok"] is True
    assert bundle["planned"]["ok"] is True and bundle["planned"]["campaign_plan"]["code"] == CAMPAIGN_ID
    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "advertising_campaign_operations_appgen_dead_letter_event"
    assert blocked_launch["ok"] is False and blocked_launch["record"]["status"] == "launch_blocked"
    assert blocked_launch["state"]["outbox"][-1]["event_type"] == "AdvertisingCampaignOperationsExceptionOpened"
    assert launched["ok"] is True and launched["ready"] is True
    assert launched["state"]["outbox"][-1]["event_type"] == "AdvertisingCampaignOperationsApproved"
    assert query["ok"] is True and query["command_center"]["summary"]["ready_count"] == 1
    assert workbench["ok"] is True and "launch_readiness_gate" in workbench["planning_panels"]
    assert assessment["ok"] is True and "agent_review_ready" in assessment["explanations"]
    assert parser["ok"] is True and parser["requires_human_confirmation"] is True
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert schema["ok"] is True and schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert service_contract["ok"] is True and "attempt_launch_campaign" in service_contract["command_methods"]
    assert api_contract["ok"] is True and api_contract["stream_engine_picker_visible"] is False
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["ok"] is True and "advertising_campaign_operations.admin" in permissions["permissions"]
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["invalid_references"] == ("foreign_table",)
    assert capabilities["ok"] is True and capabilities["event_contract"] == "AppGen-X"
    assert runtime_smoke["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_config["ok"] is True
    assert service_plan["ok"] is True and service_plan["emits"] == ("AdvertisingCampaignOperationsCreated",)
    assert service_launch["ok"] is True and service_launch["emits"] == ("AdvertisingCampaignOperationsApproved",)
    assert service_query["ok"] is True and service_query["read_only"] is True
    assert route_validation["ok"] is True
    assert route_plan["ok"] is True
    assert route_assistant["ok"] is True
    assert ui_contract["ok"] is True and ui_contract["binding_evidence"]["shared_table_access"] is False
    assert rendered["ok"] is True and rendered["cards"][0]["value"] == 1
    assert rendered["cards"][1]["value"] == 1
    assert skills["ok"] is True and skills["workflow_support"]
    assert chatbot["ok"] is True and chatbot["single_agent_contribution"] == "advertising_campaign_operations_skills"
    assert document_plan["ok"] is True and document_plan["target_table"] == "advertising_campaign_operations_ad_campaign"
    assert creative_plan["ok"] is True and creative_plan["target_table"] == "advertising_campaign_operations_creative_asset"
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True and "advertising_campaign_operations_crud" in contribution["dsl_tools"]


def test_campaign_standalone_release_workflows_and_package_contract_are_executable() -> None:
    app = standalone.AdvertisingCampaignOperationsStandaloneApp()
    bootstrapped = app.bootstrap(tenant=TENANT)
    loaded = app.load_demo_workspace(tenant=TENANT)
    rendered = app.render_workbench(tenant=TENANT)
    snapshot = app.release_snapshot()
    standalone_manifest = standalone.standalone_app_manifest()
    standalone_smoke = standalone.smoke_test()
    release_build = release_evidence.build_release_evidence(state=app.state)
    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    workflows = workflow_catalog()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed_operations = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert bootstrapped["ok"] is True and bootstrapped["state"]["configuration"]["event_contract"] == "AppGen-X"
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "advertising_campaign_operations_one_pbc_app"
    assert snapshot["ok"] is True and snapshot["state_summary"]["campaign_plan_count"] >= 1
    assert standalone_manifest["ok"] is True and standalone_manifest["app"]["forms"]
    assert standalone_smoke["ok"] is True
    assert release_build["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["standalone_app"]["ok"] is True
    assert package_smoke["ok"] is True
    assert workflows["ok"] is True and len(workflows["workflows"]) == 3
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(result["ok"] is True for result in executed_operations)
    assert all(result["target_table"].startswith("advertising_campaign_operations_") for result in executed_operations)
