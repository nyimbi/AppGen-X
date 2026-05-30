"""UI contract for the Enterprise Search Vector PBC."""

from __future__ import annotations

from .runtime import ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS
from .runtime import ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES
from .search_control import improve1_search_control_contract


ENTERPRISE_SEARCH_VECTOR_UI_FRAGMENT_KEYS = (
    "EnterpriseSearchWorkbench",
    "SearchIndexRegistry",
    "VectorDocumentExplorer",
    "EmbeddingJobConsole",
    "HybridQueryWorkbench",
    "QueryTraceExplorer",
    "SearchIndexFreshnessBoard",
    "AclFilteredResultsPanel",
    "RelevanceFeedbackPanel",
    "SearchRuleStudio",
    "SearchParameterConsole",
    "SearchConfigurationPanel",
    "SearchEventOutbox",
    "SearchDeadLetterQueue",
)


def enterprise_search_vector_ui_blueprint() -> dict:
    """Return forms, wizards, and controls for the standalone workbench."""
    forms = (
        {
            "form_id": "bootstrap_runtime",
            "title": "Bootstrap Search Runtime",
            "action": "configure_runtime",
            "permission": "enterprise_search_vector.configure",
            "fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_locale",
                "supported_locales",
                "supported_sources",
                "embedding_dimensions",
                "retention_days",
                "ranking_mode",
                "workbench_limit",
            ),
        },
        {
            "form_id": "create_index",
            "title": "Create Search Index",
            "action": "create_index",
            "permission": "enterprise_search_vector.index.write",
            "fields": ("index_id", "tenant", "name", "source", "locale", "status"),
        },
        {
            "form_id": "ingest_document",
            "title": "Ingest Search Document",
            "action": "ingest_document",
            "permission": "enterprise_search_vector.document.write",
            "fields": ("document_id", "tenant", "source", "locale", "title", "body", "acl"),
        },
        {
            "form_id": "run_embedding_job",
            "title": "Run Embedding Job",
            "action": "run_embedding_job",
            "permission": "enterprise_search_vector.document.write",
            "fields": ("job_id", "tenant", "index_id", "document_ids", "status"),
        },
        {
            "form_id": "run_hybrid_query",
            "title": "Run Hybrid Query",
            "action": "query",
            "permission": "enterprise_search_vector.query",
            "fields": ("query_id", "tenant", "text", "principal_permissions", "locale"),
        },
        {
            "form_id": "register_rule",
            "title": "Register Search Rule",
            "action": "register_rule",
            "permission": "enterprise_search_vector.configure",
            "fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "allowed_sources",
                "allowed_locales",
                "acl_policy",
                "ranking_policy",
                "retention_policy",
            ),
        },
        {
            "form_id": "register_governed_model",
            "title": "Register Governed Model",
            "action": "register_governed_model",
            "permission": "enterprise_search_vector.configure",
            "fields": ("model_id", "tenant", "model_type", "version", "status"),
        },
    )
    wizards = (
        {
            "wizard_id": "bootstrap_standalone_search",
            "title": "Bootstrap Standalone Search App",
            "permission": "enterprise_search_vector.configure",
            "steps": ("configure_runtime", "set_parameter", "register_rule", "create_index"),
            "outcome": "standalone_runtime_ready",
        },
        {
            "wizard_id": "governed_retrieval",
            "title": "Governed Retrieval Session",
            "permission": "enterprise_search_vector.query",
            "steps": (
                "ingest_document",
                "run_embedding_job",
                "query",
                "score_query_intent_risk",
                "run_relevance_controls",
            ),
            "outcome": "grounded_search_trace",
        },
        {
            "wizard_id": "quality_recovery",
            "title": "Quality Recovery Loop",
            "permission": "enterprise_search_vector.quality.write",
            "steps": (
                "forecast_index_freshness",
                "remediate_search_quality",
                "generate_index_proof",
            ),
            "outcome": "governed_remediation_evidence",
        },
    )
    controls = (
        {
            "control_id": "semantic_weight",
            "label": "Semantic Weight",
            "type": "slider",
            "action": "set_parameter",
            "permission": "enterprise_search_vector.configure",
            "bounds": (0.0, 1.0),
        },
        {
            "control_id": "keyword_weight",
            "label": "Keyword Weight",
            "type": "slider",
            "action": "set_parameter",
            "permission": "enterprise_search_vector.configure",
            "bounds": (0.0, 1.0),
        },
        {
            "control_id": "acl_preview",
            "label": "ACL Preview",
            "type": "preview",
            "action": "screen_search_policy",
            "permission": "enterprise_search_vector.policy.write",
            "bounds": (),
        },
        {
            "control_id": "freshness_forecast",
            "label": "Freshness Forecast",
            "type": "panel",
            "action": "forecast_index_freshness",
            "permission": "enterprise_search_vector.intelligence.write",
            "bounds": (1, 365),
        },
        {
            "control_id": "intent_risk_screen",
            "label": "Intent Risk Screen",
            "type": "panel",
            "action": "score_query_intent_risk",
            "permission": "enterprise_search_vector.policy.write",
            "bounds": (0.0, 1.0),
        },
        {
            "control_id": "proof_generation",
            "label": "Index Proof",
            "type": "action",
            "action": "generate_index_proof",
            "permission": "enterprise_search_vector.audit",
            "bounds": (),
        },
    )
    return {
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "workflow_board": (
            {
                "lane": "bootstrap",
                "fragments": ("SearchConfigurationPanel", "SearchParameterConsole", "SearchRuleStudio"),
            },
            {
                "lane": "operations",
                "fragments": ("SearchIndexRegistry", "VectorDocumentExplorer", "EmbeddingJobConsole"),
            },
            {
                "lane": "governance",
                "fragments": ("AclFilteredResultsPanel", "SearchIndexFreshnessBoard", "SearchEventOutbox"),
            },
        ),
    }


def enterprise_search_vector_ui_contract() -> dict:
    blueprint = enterprise_search_vector_ui_blueprint()
    return {
        "format": "appgen.enterprise-search-vector-ui-contract.v2",
        "ok": True,
        "pbc": "enterprise_search_vector",
        "implementation_directory": "src/pyAppGen/pbcs/enterprise_search_vector",
        "fragments": ENTERPRISE_SEARCH_VECTOR_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/enterprise_search_vector",
            "/workbench/pbcs/enterprise_search_vector/indexes",
            "/workbench/pbcs/enterprise_search_vector/documents",
            "/workbench/pbcs/enterprise_search_vector/jobs",
            "/workbench/pbcs/enterprise_search_vector/queries",
            "/workbench/pbcs/enterprise_search_vector/feedback",
            "/workbench/pbcs/enterprise_search_vector/configuration",
        ),
        "action_permissions": {
            "create_index": "enterprise_search_vector.index.write",
            "refresh_index": "enterprise_search_vector.index.write",
            "ingest_document": "enterprise_search_vector.document.write",
            "run_embedding_job": "enterprise_search_vector.document.write",
            "query": "enterprise_search_vector.query",
            "record_feedback": "enterprise_search_vector.query",
            "receive_event": "enterprise_search_vector.event.consume",
            "register_rule": "enterprise_search_vector.configure",
            "set_parameter": "enterprise_search_vector.configure",
            "configure_runtime": "enterprise_search_vector.configure",
            "run_control_tests": "enterprise_search_vector.audit",
            "score_query_intent_risk": "enterprise_search_vector.policy.write",
            "forecast_index_freshness": "enterprise_search_vector.intelligence.write",
            "generate_index_proof": "enterprise_search_vector.audit",
            "register_governed_model": "enterprise_search_vector.configure",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_locale",
                "ranking_mode",
            ),
            "allowed_database_backends": ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "runtime_profile_badge": "read_only",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "semantic_weight",
                "keyword_weight",
                "freshness_weight",
                "authority_weight",
                "feedback_weight",
                "relevance_threshold",
                "chunk_size_tokens",
                "embedding_batch_limit",
                "max_results",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("configuration", "parameter", "release_gate", "domain_policy"),
            "required_fields": ("rule_id", "tenant", "rule_type", "status"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "event_surfaces": {
            "contract": "appgen_event_contract",
            "emits": ("SearchIndexUpdated", "DiscoveryInsightGenerated"),
            "consumes": ("ProductPublished", "CustomerUpdated", "AuditEventSealed"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "workflow_board": blueprint["workflow_board"],
        "search_control_contract": improve1_search_control_contract(),
        "full_capability_surface": {
            "search_control_panels": tuple(item["evidence"]["ui_surface"] for item in improve1_search_control_contract()["capabilities"]),
        },
    }


def enterprise_search_vector_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = enterprise_search_vector_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, permission in contract["action_permissions"].items()
        if permission in permissions
    )
    view = _view_counts(state, tenant)
    blueprint = enterprise_search_vector_ui_blueprint()
    return {
        "format": "appgen.enterprise-search-vector-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/enterprise_search_vector",
        "fragments": contract["fragments"],
        "cards": (
            {"key": "indexes", "value": view["index_count"], "fragment": "SearchIndexRegistry"},
            {"key": "documents", "value": view["document_count"], "fragment": "VectorDocumentExplorer"},
            {"key": "jobs", "value": view["embedding_job_count"], "fragment": "EmbeddingJobConsole"},
            {"key": "queries", "value": view["query_count"], "fragment": "QueryTraceExplorer"},
            {"key": "feedback", "value": view["feedback_count"], "fragment": "RelevanceFeedbackPanel"},
            {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "SearchDeadLetterQueue"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "forms": tuple(item for item in blueprint["forms"] if item["permission"] in permissions),
        "wizards": tuple(item for item in blueprint["wizards"] if item["permission"] in permissions),
        "controls": tuple(item for item in blueprint["controls"] if item["permission"] in permissions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    indexes = tuple(item for item in state.get("search_indexes", {}).values() if item["tenant"] == tenant)
    jobs = tuple(item for item in state.get("embedding_jobs", {}).values() if item["tenant"] == tenant)
    docs = tuple(
        item
        for item in state.get("vector_documents", {}).values()
        if item["tenant"] == tenant and item.get("status", "active") != "deleted"
    )
    queries = tuple(item for item in state.get("query_traces", {}).values() if item["tenant"] == tenant)
    return {
        "index_count": len(indexes),
        "embedding_job_count": len(jobs),
        "document_count": len(docs),
        "query_count": len(queries),
        "feedback_count": sum(int(item.get("feedback_count", 0)) for item in docs),
        "ready_document_count": sum(1 for item in docs if item.get("embedding_job_id")),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "search_control_contract": improve1_search_control_contract(),
        "full_capability_surface": {
            "search_control_panels": tuple(item["evidence"]["ui_surface"] for item in improve1_search_control_contract()["capabilities"]),
        },
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
            "event_contract": "appgen_event_contract",
        },
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
            "events": (),
        }
    )


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = enterprise_search_vector_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = enterprise_search_vector_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
        "forms": contract.get("forms", ()),
        "wizards": contract.get("wizards", ()),
        "controls": contract.get("controls", ()),
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v2",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get(
            "stream_engine_picker_visible",
            configuration_editor.get("user_facing_stream_engine_picker", False),
        )
        is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(rendered.get("forms"))
        and bool(rendered.get("wizards"))
        and bool(rendered.get("controls"))
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
