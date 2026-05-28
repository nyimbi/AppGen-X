"""Domain vocabulary and capability surfaces for case_knowledge_management."""

from __future__ import annotations

import hashlib


PBC_KEY = "case_knowledge_management"
DOMAIN_ENTITY = "support_case"
DOMAIN_PURPOSE = (
    "Owns support case intake, classification, routing, assignment, SLA oversight, "
    "escalations, knowledge authoring, article quality, and governed agent assistance."
)

DOMAIN_TABLE_NAMES = (
    "support_case",
    "case_contact",
    "case_classification",
    "case_queue",
    "case_assignment",
    "case_sla",
    "sla_timer_event",
    "case_interaction",
    "case_escalation",
    "case_resolution",
    "knowledge_article",
    "article_version",
    "article_feedback",
    "article_quality_score",
    "root_cause",
    "case_duplicate_link",
    "case_exception_case",
    "case_policy_rule",
    "case_runtime_parameter",
    "case_schema_extension",
    "case_control_assertion",
    "case_governed_model",
    "semantic_knowledge_index",
    "case_deflection_event",
    "knowledge_approval",
    "content_freshness_signal",
    "agent_assist_recommendation",
    "appgen_outbox_event",
    "appgen_inbox_event",
    "appgen_dead_letter_event",
)
DOMAIN_OWNED_TABLES = tuple(f"{PBC_KEY}_{name}" for name in DOMAIN_TABLE_NAMES)

DOMAIN_OPERATIONS = (
    "create_support_case",
    "classify_case",
    "route_case_queue",
    "assign_case",
    "start_sla_timer",
    "record_case_interaction",
    "open_case_escalation",
    "resolve_case",
    "publish_knowledge_article",
    "approve_knowledge_article",
    "version_article",
    "capture_article_feedback",
    "score_article_quality",
    "identify_root_cause",
    "link_duplicate_case",
    "resolve_case_exception",
    "record_case_deflection",
    "recommend_next_best_resolution",
)
RUNTIME_COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "governed_datastore_crud",
    "run_advanced_assessment",
    "parse_document_instruction",
)
QUERY_OPERATIONS = (
    "query_workbench",
    "build_workbench_view",
    "list_table_rows",
)

DOMAIN_RULES = (
    "case_routing_policy",
    "severity_override_policy",
    "sla_pause_policy",
    "knowledge_publish_policy",
    "duplicate_case_policy",
    "agent_mutation_policy",
    "freshness_review_policy",
)
DOMAIN_PARAMETERS = (
    "sla_warning_minutes",
    "duplicate_similarity_threshold",
    "article_quality_floor",
    "escalation_age_hours",
    "queue_capacity_limit",
    "workbench_case_limit",
    "agent_write_requires_confirmation",
    "freshness_review_days",
)
DOMAIN_EVENTS = (
    "CaseCreated",
    "CaseClassified",
    "CaseAssigned",
    "SlaRiskChanged",
    "CaseEscalated",
    "CaseResolved",
    "KnowledgeArticlePublished",
    "KnowledgeArticleApproved",
    "KnowledgeArticleVersioned",
    "ArticleFeedbackCaptured",
    "CaseDeflected",
    "AgentAssistRecommended",
    "ContentFreshnessFlagged",
)
DOMAIN_CONSUMED_EVENTS = (
    "ServiceTicketOpened",
    "CustomerUpdated",
    "SearchIndexRefreshed",
    "ProductPublished",
    "PolicyChanged",
    "WorkflowTaskCompleted",
)
DOMAIN_ADVANCED_CAPABILITIES = (
    "semantic case classification",
    "queue load aware routing",
    "SLA breach prediction",
    "knowledge freshness monitoring",
    "duplicate case graphing",
    "grounded next-best-resolution assistance",
)
DOMAIN_WORKBENCH_VIEWS = (
    "case workbench",
    "queue board",
    "SLA timer console",
    "escalation room",
    "knowledge studio",
    "quality and freshness panel",
    "release evidence desk",
)
WORKBENCH_FORMS = (
    "case_intake_form",
    "case_interaction_form",
    "escalation_form",
    "knowledge_article_form",
    "article_feedback_form",
    "rule_editor_form",
    "parameter_editor_form",
)
WORKBENCH_WIZARDS = (
    "case_triage_wizard",
    "knowledge_publish_wizard",
    "duplicate_resolution_wizard",
    "agent_instruction_wizard",
)
WORKBENCH_CONTROLS = (
    "queue_capacity_meter",
    "sla_risk_badge",
    "freshness_watchlist",
    "agent_grounding_toggle",
    "duplicate_cluster_panel",
)
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
)
RBAC_ROLES = ("reader", "operator", "knowledge_author", "approver", "admin")
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"

OPERATION_TABLE_MAP = {
    "create_support_case": f"{PBC_KEY}_support_case",
    "classify_case": f"{PBC_KEY}_case_classification",
    "route_case_queue": f"{PBC_KEY}_case_queue",
    "assign_case": f"{PBC_KEY}_case_assignment",
    "start_sla_timer": f"{PBC_KEY}_case_sla",
    "record_case_interaction": f"{PBC_KEY}_case_interaction",
    "open_case_escalation": f"{PBC_KEY}_case_escalation",
    "resolve_case": f"{PBC_KEY}_case_resolution",
    "publish_knowledge_article": f"{PBC_KEY}_knowledge_article",
    "approve_knowledge_article": f"{PBC_KEY}_knowledge_approval",
    "version_article": f"{PBC_KEY}_article_version",
    "capture_article_feedback": f"{PBC_KEY}_article_feedback",
    "score_article_quality": f"{PBC_KEY}_article_quality_score",
    "identify_root_cause": f"{PBC_KEY}_root_cause",
    "link_duplicate_case": f"{PBC_KEY}_case_duplicate_link",
    "resolve_case_exception": f"{PBC_KEY}_case_exception_case",
    "record_case_deflection": f"{PBC_KEY}_case_deflection_event",
    "recommend_next_best_resolution": f"{PBC_KEY}_agent_assist_recommendation",
}
OPERATION_EVENT_MAP = {
    "create_support_case": "CaseCreated",
    "classify_case": "CaseClassified",
    "assign_case": "CaseAssigned",
    "start_sla_timer": "SlaRiskChanged",
    "open_case_escalation": "CaseEscalated",
    "resolve_case": "CaseResolved",
    "publish_knowledge_article": "KnowledgeArticlePublished",
    "approve_knowledge_article": "KnowledgeArticleApproved",
    "version_article": "KnowledgeArticleVersioned",
    "capture_article_feedback": "ArticleFeedbackCaptured",
    "record_case_deflection": "CaseDeflected",
    "recommend_next_best_resolution": "AgentAssistRecommended",
    "score_article_quality": "ContentFreshnessFlagged",
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def operation_to_table(operation: str) -> str | None:
    return OPERATION_TABLE_MAP.get(operation)


def operation_to_event(operation: str) -> str | None:
    return OPERATION_EVENT_MAP.get(operation)


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.domain-depth.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "entity": DOMAIN_ENTITY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operations": DOMAIN_OPERATIONS,
        "runtime_commands": RUNTIME_COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "operation_count": len(DOMAIN_OPERATIONS),
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "forms": WORKBENCH_FORMS,
        "wizards": WORKBENCH_WIZARDS,
        "controls": WORKBENCH_CONTROLS,
        "permissions": PERMISSIONS,
        "rbac_roles": RBAC_ROLES,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 24,
        "minimum_domain_operations": 16,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    table = operation_to_table(operation)
    if operation not in DOMAIN_OPERATIONS or table is None:
        return {
            "ok": False,
            "reason": "unknown_domain_operation",
            "operation": operation,
            "side_effects": (),
        }
    event_type = operation_to_event(operation)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": table,
        "owned_tables": (table,),
        "read_tables": (),
        "emitted_event": event_type,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": f"{PBC_KEY}.update",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    plans = tuple(execute_domain_operation(name, {"tenant": "tenant-smoke"}) for name in DOMAIN_OPERATIONS[:6])
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(plan["ok"] for plan in plans),
        "contract": contract,
        "plans": plans,
        "side_effects": (),
    }


def domain_capability_surface_contract() -> dict:
    operation_surfaces = tuple(
        {
            "operation": operation,
            "surface": f"{PBC_KEY}.ui.operation.{operation}",
            "action": operation,
            "target_table": operation_to_table(operation),
            "permission": f"{PBC_KEY}.update",
            "requires_confirmation": operation not in {"classify_case", "route_case_queue"},
            "event": operation_to_event(operation),
        }
        for operation in DOMAIN_OPERATIONS
    )
    return {
        "format": f"appgen.{PBC_KEY}.capability-surface.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": operation_surfaces,
        "rule_surfaces": tuple(
            {
                "rule": rule,
                "surface": f"{PBC_KEY}.ui.rule.{rule}",
                "editor": True,
                "explainable": True,
            }
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {
                "parameter": parameter,
                "surface": f"{PBC_KEY}.ui.parameter.{parameter}",
                "editable": True,
                "bounded": True,
            }
            for parameter in DOMAIN_PARAMETERS
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "coverage_counts": {
            "operations": len(operation_surfaces),
            "rules": len(DOMAIN_RULES),
            "parameters": len(DOMAIN_PARAMETERS),
            "advanced_capabilities": len(DOMAIN_ADVANCED_CAPABILITIES),
            "owned_tables": len(DOMAIN_OWNED_TABLES),
        },
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def ui_capability_surface_contract() -> dict:
    surface = domain_capability_surface_contract()
    return {
        "format": f"appgen.{PBC_KEY}.ui-surface.v2",
        "ok": surface["ok"],
        "pbc": PBC_KEY,
        "navigation_sections": (
            "command_center",
            "queue_board",
            "cases",
            "knowledge_studio",
            "quality_and_freshness",
            "rules_and_parameters",
            "agent_assistant",
            "release_evidence",
        ),
        "operation_actions": tuple(item["action"] for item in surface["operation_surfaces"]),
        "rule_editors": tuple(item["rule"] for item in surface["rule_surfaces"]),
        "parameter_editors": tuple(item["parameter"] for item in surface["parameter_surfaces"]),
        "advanced_panels": tuple(item["capability"] for item in surface["advanced_surfaces"]),
        "table_browsers": tuple(item["owned_table"] for item in surface["table_surfaces"]),
        "forms": WORKBENCH_FORMS,
        "wizards": WORKBENCH_WIZARDS,
        "controls": WORKBENCH_CONTROLS,
        "coverage": surface,
        "side_effects": (),
    }
