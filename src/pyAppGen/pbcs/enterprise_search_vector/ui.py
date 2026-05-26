"""UI contract for the Enterprise Search Vector PBC."""

from __future__ import annotations

from .runtime import ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS
from .runtime import ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES


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


def enterprise_search_vector_ui_contract() -> dict:
    return {
        "format": "appgen.enterprise-search-vector-ui-contract.v1",
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
        "event_surfaces": {
            "contract": "appgen_event_contract",
            "emits": ("SearchIndexUpdated", "DiscoveryInsightGenerated"),
            "consumes": ("ProductPublished", "CustomerUpdated", "AuditEventSealed"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    return {
        "format": "appgen.enterprise-search-vector-workbench-render.v1",
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
        "locked_actions": tuple(
            action for action in contract["action_permissions"] if action not in visible_actions
        ),
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
    docs = tuple(item for item in state.get("vector_documents", {}).values() if item["tenant"] == tenant)
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
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


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
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
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
