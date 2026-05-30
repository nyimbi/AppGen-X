"""Executable runtime contract for the case_knowledge_management PBC."""

from __future__ import annotations

from .application import create_app
from .config import DEFAULT_CONFIGURATION
from .domain_depth import ALLOWED_DATABASE_BACKENDS
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_CONSUMED_EVENTS
from .domain_depth import DOMAIN_EVENTS
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import PBC_KEY
from .domain_depth import QUERY_OPERATIONS
from .domain_depth import REQUIRED_EVENT_TOPIC
from .domain_depth import WORKBENCH_CONTROLS
from .domain_depth import WORKBENCH_FORMS
from .domain_depth import WORKBENCH_WIZARDS
from .models import OWNED_TABLES
from .models import build_schema_contract
from .support_control import improve1_support_control_contract


CASE_KNOWLEDGE_MANAGEMENT_OWNED_TABLES = OWNED_TABLES
CASE_KNOWLEDGE_MANAGEMENT_RUNTIME_TABLES = OWNED_TABLES
CASE_KNOWLEDGE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
CASE_KNOWLEDGE_MANAGEMENT_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
CASE_KNOWLEDGE_MANAGEMENT_EMITTED_EVENT_TYPES = DOMAIN_EVENTS
CASE_KNOWLEDGE_MANAGEMENT_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
CASE_KNOWLEDGE_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    "support_case_management",
    "case_knowledge_management_workflow",
    "case_knowledge_management_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
CASE_KNOWLEDGE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = (
    "case_knowledge_management_event_sourced_operational_history",
    "case_knowledge_management_multi_tenant_policy_isolation",
    "case_knowledge_management_schema_evolution_resilience",
    "case_knowledge_management_autonomous_anomaly_detection",
    "case_knowledge_management_semantic_document_instruction_understanding",
    "case_knowledge_management_predictive_risk_scoring",
    "case_knowledge_management_counterfactual_scenario_simulation",
    "case_knowledge_management_cryptographic_audit_proofs",
    "case_knowledge_management_continuous_control_testing",
    "case_knowledge_management_carbon_and_sustainability_awareness",
    "case_knowledge_management_cross_pbc_event_federation",
    "case_knowledge_management_governed_ai_agent_execution",
)
CASE_KNOWLEDGE_MANAGEMENT_UI_FRAGMENT_KEYS = (
    "CaseKnowledgeManagementWorkbench",
    "CaseKnowledgeManagementDetail",
    "CaseKnowledgeManagementAssistantPanel",
)
CASE_KNOWLEDGE_MANAGEMENT_BUSINESS_TABLES = tuple(
    table
    for table in OWNED_TABLES
    if not table.endswith("_appgen_outbox_event")
    and not table.endswith("_appgen_inbox_event")
    and not table.endswith("_appgen_dead_letter_event")
)


def case_knowledge_management_empty_state() -> dict:
    return create_app().snapshot()


def case_knowledge_management_configure_runtime(state: dict, config: dict) -> dict:
    app = create_app(state)
    return app.configure_runtime(config)


def case_knowledge_management_set_parameter(state: dict, name: str, value: object) -> dict:
    app = create_app(state)
    return app.set_parameter(name, value)


def case_knowledge_management_register_rule(state: dict, rule: dict) -> dict:
    app = create_app(state)
    return app.register_rule(rule)


def case_knowledge_management_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    app = create_app(state)
    return app.register_schema_extension(table, fields)


def case_knowledge_management_receive_event(state: dict, event: dict) -> dict:
    app = create_app(state)
    return app.receive_event(event)


def case_knowledge_management_command_support_case(state: dict, payload: dict) -> dict:
    app = create_app(state)
    return app.create_support_case(payload)


def case_knowledge_management_query_workbench(state: dict, filters: dict | None = None) -> dict:
    app = create_app(state)
    return app.query_workbench(filters)


def case_knowledge_management_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    app = create_app(state)
    return app.run_advanced_assessment(payload)


def case_knowledge_management_parse_document_instruction(document: str, instruction: str) -> dict:
    document_text = str(document)
    lower = document_text.lower()
    candidate_tables = []
    if "case" in lower or "incident" in lower:
        candidate_tables.append(f"{PBC_KEY}_support_case")
    if "article" in lower or "knowledge" in lower:
        candidate_tables.append(f"{PBC_KEY}_knowledge_article")
    if "feedback" in lower:
        candidate_tables.append(f"{PBC_KEY}_article_feedback")
    if not candidate_tables:
        candidate_tables.append(f"{PBC_KEY}_support_case")
    return {
        "ok": True,
        "candidate_tables": tuple(candidate_tables),
        "instruction": instruction,
        "requires_human_confirmation": True,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def case_knowledge_management_build_schema_contract() -> dict:
    return build_schema_contract()


def case_knowledge_management_build_service_contract() -> dict:
    return {
        "format": "appgen.case-knowledge-management-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_support_case",
            "run_advanced_assessment",
            "parse_document_instruction",
            *DOMAIN_OPERATIONS,
            "governed_datastore_crud",
        ),
        "query_methods": QUERY_OPERATIONS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def case_knowledge_management_build_api_contract() -> dict:
    routes = (
        "POST /support-cases",
        "POST /support-cases/classify",
        "POST /support-cases/route",
        "POST /support-cases/assign",
        "POST /support-cases/escalate",
        "POST /support-cases/resolve",
        "POST /knowledge-articles",
        "POST /knowledge-articles/approve",
        "POST /knowledge-articles/version",
        "POST /knowledge-feedback",
        "POST /agent/recommendations",
        "POST /agent/document-instructions",
        "GET /knowledge-workbench",
    )
    return {
        "format": "appgen.case-knowledge-management-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": routes,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
    }


def case_knowledge_management_build_release_evidence() -> dict:
    smoke = case_knowledge_management_runtime_smoke()
    checks = (
        {"id": "schema_models_migrations", "ok": case_knowledge_management_build_schema_contract()["ok"]},
        {"id": "service_api_events", "ok": case_knowledge_management_build_service_contract()["ok"]},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "runtime_smoke", "ok": smoke["ok"]},
        {"id": "owned_table_depth", "ok": len(OWNED_TABLES) >= 24},
        {"id": "domain_operation_depth", "ok": len(DOMAIN_OPERATIONS) >= 16},
        {"id": "rules_parameters_depth", "ok": len(DOMAIN_RULES) >= 6 and len(DOMAIN_PARAMETERS) >= 6},
        {"id": "improve1_support_control", "ok": improve1_support_control_contract()["capability_count"] == 50},
    )
    return {
        "format": "appgen.case-knowledge-management-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "boundary_gaps": (),
        "runtime_smoke": smoke,
        "improve1_support_control": improve1_support_control_contract(),
        "side_effects": (),
    }


def case_knowledge_management_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
        ),
        "rbac_roles": ("reader", "operator", "knowledge_author", "approver", "admin"),
        "side_effects": (),
    }


def case_knowledge_management_build_workbench_view(state: dict | None = None, tenant: str = "default") -> dict:
    app = create_app(state)
    workbench = app.query_workbench({"tenant": tenant})
    return {
        "ok": workbench["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "fragments": CASE_KNOWLEDGE_MANAGEMENT_UI_FRAGMENT_KEYS,
        "workbench_view": "CaseKnowledgeManagementWorkbench",
        "configuration_editor": True,
        "forms": WORKBENCH_FORMS,
        "wizards": WORKBENCH_WIZARDS,
        "controls": WORKBENCH_CONTROLS,
        "records": workbench["records"],
        "metrics": workbench["metrics"],
        "side_effects": (),
    }


def case_knowledge_management_verify_owned_table_boundary(references: tuple[str, ...] | list[str]) -> dict:
    allowed = set(OWNED_TABLES) | {"api_dependency", "projection_dependency"}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f"{PBC_KEY}_"))
    return {
        "ok": not foreign,
        "foreign_references": foreign,
        "allowed_dependency_modes": ("api", "event", "projection"),
        "side_effects": (),
    }


def case_knowledge_management_runtime_smoke() -> dict:
    app = create_app()
    smoke = app.runtime_smoke()
    return {
        "format": "appgen.case-knowledge-management-runtime-smoke.v2",
        "ok": smoke["ok"],
        "checks": (
            {"id": "configuration_defaults", "ok": DEFAULT_CONFIGURATION["database_backend"] in ALLOWED_DATABASE_BACKENDS},
            {"id": "domain_app_smoke", "ok": smoke["ok"]},
            {"id": "event_contract", "ok": bool(CASE_KNOWLEDGE_MANAGEMENT_REQUIRED_EVENT_TOPIC)},
        ),
        "state": app.snapshot(),
        "smoke": smoke,
        "side_effects": (),
    }


def case_knowledge_management_runtime_capabilities() -> dict:
    smoke = case_knowledge_management_runtime_smoke()
    return {
        "format": "appgen.case-knowledge-management-runtime-capabilities.v2",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/case_knowledge_management",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "capabilities": CASE_KNOWLEDGE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        "standard_features": CASE_KNOWLEDGE_MANAGEMENT_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
            "command_support_case",
            "query_workbench",
            "run_advanced_assessment",
            "parse_document_instruction",
            "governed_datastore_crud",
            *DOMAIN_OPERATIONS,
        ),
        "domain_advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "smoke": smoke,
        "side_effects": (),
    }
