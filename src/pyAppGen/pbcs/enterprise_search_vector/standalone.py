"""Standalone one-PBC application composition for enterprise_search_vector."""

from __future__ import annotations

from . import agent
from . import events
from . import permissions
from . import routes
from . import seed_data
from . import services
from . import ui
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence
from .runtime import enterprise_search_vector_build_workbench_view
from .runtime import enterprise_search_vector_configure_runtime
from .runtime import enterprise_search_vector_create_index
from .runtime import enterprise_search_vector_empty_state
from .runtime import enterprise_search_vector_ingest_document
from .runtime import enterprise_search_vector_query
from .runtime import enterprise_search_vector_register_governed_model
from .runtime import enterprise_search_vector_register_rule
from .runtime import enterprise_search_vector_run_embedding_job
from .runtime import enterprise_search_vector_set_parameter


PBC_KEY = "enterprise_search_vector"


def standalone_workflow_catalog() -> tuple[dict, ...]:
    """Return executable standalone workflow definitions for this PBC app."""
    return (
        {
            "workflow_id": "bootstrap_search_app",
            "label": "Bootstrap Search App",
            "steps": ("configure_runtime", "set_parameter", "register_rule", "create_index"),
            "outcome": "runtime_ready",
        },
        {
            "workflow_id": "ingest_and_embed",
            "label": "Ingest and Embed",
            "steps": ("ingest_document", "run_embedding_job", "generate_index_proof"),
            "outcome": "document_searchable",
        },
        {
            "workflow_id": "governed_search",
            "label": "Governed Search",
            "steps": ("query", "score_query_intent_risk", "run_relevance_controls"),
            "outcome": "grounded_discovery_trace",
        },
        {
            "workflow_id": "governance_review",
            "label": "Governance Review",
            "steps": (
                "screen_search_policy",
                "forecast_index_freshness",
                "record_retention_deletion",
                "register_governed_model",
            ),
            "outcome": "operational_governance_evidence",
        },
    )


def bootstrap_standalone_state() -> dict:
    """Build a deterministic standalone app state using package-local seeds."""
    state = enterprise_search_vector_empty_state()
    state = enterprise_search_vector_configure_runtime(state, seed_data.default_configuration())["state"]
    for key, value in seed_data.default_parameter_values().items():
        state = enterprise_search_vector_set_parameter(state, key, value)["state"]
    for rule in seed_data.default_rules():
        state = enterprise_search_vector_register_rule(state, rule)["state"]
    for index in seed_data.default_indexes():
        state = enterprise_search_vector_create_index(state, index)["state"]
    for document in seed_data.default_document_commands():
        state = enterprise_search_vector_ingest_document(state, document)["state"]
    state = enterprise_search_vector_run_embedding_job(
        state,
        {
            "job_id": "job_bootstrap_alpha",
            "tenant": "tenant_alpha",
            "index_id": "idx_product",
            "document_ids": ("doc_product_alpha",),
            "status": "completed",
        },
    )["state"]
    for model in seed_data.default_governed_models():
        state = enterprise_search_vector_register_governed_model(state, model)["state"]
    return state


def standalone_application_manifest() -> dict:
    """Return the standalone one-PBC app composition contract."""
    runtime_state = bootstrap_standalone_state()
    query = enterprise_search_vector_query(
        runtime_state,
        {
            "query_id": "query_bootstrap_alpha",
            "tenant": "tenant_alpha",
            "text": "optical camera",
            "principal_permissions": ("search.read",),
            "locale": "en-US",
        },
    )
    runtime_state = query["state"]
    workbench = enterprise_search_vector_build_workbench_view(runtime_state, tenant="tenant_alpha")
    return {
        "format": "appgen.enterprise-search-vector-standalone-app.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "mode": "standalone_one_pbc_app",
        "manifest": PBC_MANIFEST,
        "routes": routes.api_route_contracts(),
        "services": services.service_operation_manifest(),
        "permissions": permissions.permission_manifest(),
        "events": events.event_contract_manifest(),
        "ui": ui.enterprise_search_vector_ui_contract(),
        "agent": agent.composed_agent_contribution(),
        "release": build_release_evidence(),
        "seed": seed_data.seed_plan(),
        "workflows": standalone_workflow_catalog(),
        "bootstrap": {
            "state_digest": query["query_trace"]["audit_proof"],
            "query_result_count": query["query_trace"]["result_count"],
            "workbench": workbench,
        },
        "side_effects": (),
    }


def validate_standalone_application() -> dict:
    """Validate standalone app completeness and bootstrap evidence."""
    app = standalone_application_manifest()
    bootstrap = app["bootstrap"]
    workflow_ids = tuple(item["workflow_id"] for item in app["workflows"])
    missing_workflows = tuple(
        workflow
        for workflow in ("bootstrap_search_app", "ingest_and_embed", "governed_search", "governance_review")
        if workflow not in workflow_ids
    )
    missing_sections = tuple(
        section
        for section in ("routes", "services", "permissions", "events", "ui", "agent", "release", "seed")
        if not app.get(section)
    )
    return {
        "ok": app["ok"]
        and not missing_workflows
        and not missing_sections
        and bootstrap["query_result_count"] >= 1
        and bootstrap["workbench"]["configuration_bound"] is True,
        "pbc": PBC_KEY,
        "missing_workflows": missing_workflows,
        "missing_sections": missing_sections,
        "app": app,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the standalone app composition contract."""
    validation = validate_standalone_application()
    app = validation["app"]
    return {
        "ok": validation["ok"]
        and app["agent"]["ok"]
        and bool(app["ui"]["forms"])
        and bool(app["workflows"])
        and bool(app["bootstrap"]["workbench"]["binding_evidence"]["owned_tables"]),
        "validation": validation,
        "side_effects": (),
    }
