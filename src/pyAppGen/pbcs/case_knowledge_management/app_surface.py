"""Standalone application surface for the case_knowledge_management PBC."""

from __future__ import annotations

from .runtime import (
    CASE_KNOWLEDGE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    CASE_KNOWLEDGE_MANAGEMENT_BUSINESS_TABLES,
    CASE_KNOWLEDGE_MANAGEMENT_OWNED_TABLES,
    CASE_KNOWLEDGE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    CASE_KNOWLEDGE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
    CASE_KNOWLEDGE_MANAGEMENT_STANDARD_FEATURE_KEYS,
    PBC_KEY,
    WORKBENCH_CONTROLS,
    WORKBENCH_FORMS,
    WORKBENCH_WIZARDS,
    case_knowledge_management_build_api_contract,
    case_knowledge_management_build_schema_contract,
    case_knowledge_management_build_service_contract,
    case_knowledge_management_build_workbench_view,
    case_knowledge_management_parse_document_instruction,
    case_knowledge_management_runtime_capabilities,
)
from .seed_data import seed_plan


def case_knowledge_management_forms_contract() -> dict:
    form_details = tuple(
        {
            "id": form,
            "title": form.replace("_", " ").title(),
            "target_table": {
                "case_intake_form": "case_knowledge_management_support_case",
                "case_interaction_form": "case_knowledge_management_case_interaction",
                "escalation_form": "case_knowledge_management_case_escalation",
                "knowledge_article_form": "case_knowledge_management_knowledge_article",
                "article_feedback_form": "case_knowledge_management_article_feedback",
                "rule_editor_form": "case_knowledge_management_case_policy_rule",
                "parameter_editor_form": "case_knowledge_management_case_runtime_parameter",
            }[form],
        }
        for form in WORKBENCH_FORMS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": form_details,
        "covered_operations": (
            "create_support_case",
            "record_case_interaction",
            "open_case_escalation",
            "publish_knowledge_article",
            "capture_article_feedback",
            "register_rule",
            "set_parameter",
        ),
        "owned_tables": CASE_KNOWLEDGE_MANAGEMENT_OWNED_TABLES,
        "writes_foreign_tables": False,
    }


def case_knowledge_management_wizards_contract() -> dict:
    details = tuple(
        {
            "id": wizard,
            "title": wizard.replace("_", " ").title(),
            "steps": {
                "case_triage_wizard": ("intake", "classification", "queue", "assignment", "sla"),
                "knowledge_publish_wizard": ("draft", "semantic_index", "review", "publish", "freshness"),
                "duplicate_resolution_wizard": ("detect", "cluster", "compare", "merge", "notify"),
                "agent_instruction_wizard": ("document", "intent", "crud_preview", "confirmation", "event_plan"),
            }[wizard],
        }
        for wizard in WORKBENCH_WIZARDS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": details,
        "supports_case_to_resolution": True,
        "supports_knowledge_authoring": True,
        "supports_agent_document_intake": True,
    }


def case_knowledge_management_controls_contract() -> dict:
    details = tuple(
        {
            "id": control,
            "title": control.replace("_", " ").title(),
            "type": {
                "queue_capacity_meter": "load_control",
                "sla_risk_badge": "sla_control",
                "freshness_watchlist": "knowledge_quality_control",
                "agent_grounding_toggle": "assistant_safety_control",
                "duplicate_cluster_panel": "deduplication_control",
            }[control],
        }
        for control in WORKBENCH_CONTROLS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": details,
        "control_ids": tuple(control["id"] for control in details),
        "database_backends": CASE_KNOWLEDGE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "event_topic": CASE_KNOWLEDGE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def standalone_seed_bundle() -> tuple[dict, ...]:
    seeded = tuple(seed_plan()["rows"])
    return seeded + (
        {"table": "case_knowledge_management_support_case", "values": {"id": "case-demo-api", "tenant": "default", "title": "API timeout after token rotation", "severity": "high", "status": "open"}},
        {"table": "case_knowledge_management_knowledge_article", "values": {"id": "article-demo-token", "tenant": "default", "title": "Recovering failed token rotations", "lifecycle_state": "published"}},
    )


def single_pbc_case_knowledge_management_app_contract(state=None) -> dict:
    schema = case_knowledge_management_build_schema_contract()
    service = case_knowledge_management_build_service_contract()
    api = case_knowledge_management_build_api_contract()
    runtime = case_knowledge_management_runtime_capabilities()
    workbench = case_knowledge_management_build_workbench_view(state=state)
    forms = case_knowledge_management_forms_contract()
    wizards = case_knowledge_management_wizards_contract()
    controls = case_knowledge_management_controls_contract()
    return {
        "ok": all(item["ok"] for item in (schema, service, api, runtime, workbench, forms, wizards, controls))
        and len(standalone_seed_bundle()) >= 4,
        "pbc": PBC_KEY,
        "application_mode": "single_pbc_standalone",
        "owned_tables": runtime["owned_tables"],
        "schema": schema,
        "service": service,
        "api": api,
        "workbench": workbench,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "seed_data": standalone_seed_bundle(),
        "standard_features": CASE_KNOWLEDGE_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "advanced_capabilities": CASE_KNOWLEDGE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "dependency_boundary": {
            "writes_foreign_tables": False,
            "cross_pbc_dependencies": ("api", "event", "projection"),
            "event_contract": "AppGen-X",
        },
    }


def document_instruction_case_knowledge_management_plan(document: str, instructions: str) -> dict:
    plan = case_knowledge_management_parse_document_instruction(document, instructions)
    text = f"{document}\n{instructions}".lower()
    if "article" in text or "knowledge" in text:
        candidate_tables = ("case_knowledge_management_knowledge_article", "case_knowledge_management_semantic_knowledge_index")
    elif "feedback" in text:
        candidate_tables = ("case_knowledge_management_article_feedback",)
    elif "escalat" in text:
        candidate_tables = ("case_knowledge_management_case_escalation", "case_knowledge_management_support_case")
    else:
        candidate_tables = tuple(plan.get("candidate_tables", ("case_knowledge_management_support_case",)))
    return {
        **plan,
        "ok": plan["ok"] and all(table in CASE_KNOWLEDGE_MANAGEMENT_OWNED_TABLES for table in candidate_tables),
        "candidate_tables": candidate_tables,
        "single_pbc_ready": True,
        "assistant_surface": "CaseKnowledgeManagementAssistantPanel",
        "allowed_mutation_boundary": CASE_KNOWLEDGE_MANAGEMENT_OWNED_TABLES,
    }


def standalone_route_contracts() -> tuple[dict, ...]:
    app_routes = (
        {"method": "GET", "path": "/case-knowledge-management/app", "operation": "single_pbc_case_knowledge_management_app_contract"},
        {"method": "GET", "path": "/case-knowledge-management/forms", "operation": "case_knowledge_management_forms_contract"},
        {"method": "GET", "path": "/case-knowledge-management/wizards", "operation": "case_knowledge_management_wizards_contract"},
        {"method": "GET", "path": "/case-knowledge-management/controls", "operation": "case_knowledge_management_controls_contract"},
    )
    return tuple(
        {
            **route,
            "pbc": PBC_KEY,
            "required_permission": "case_knowledge_management.read",
            "idempotency_key": f"{PBC_KEY}:{route['method']}:{route['path']}",
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for route in app_routes
    )


def app_surface_smoke_test() -> dict:
    app = single_pbc_case_knowledge_management_app_contract()
    instruction = document_instruction_case_knowledge_management_plan(
        "Customer reports API timeout and asks for a knowledge article update.",
        "create case, escalate if high impact, and update knowledge article",
    )
    route_paths = tuple(route["path"] for route in standalone_route_contracts())
    return {
        "ok": app["ok"] and instruction["ok"] and "/case-knowledge-management/app" in route_paths,
        "app": app,
        "instruction": instruction,
        "route_paths": route_paths,
    }
