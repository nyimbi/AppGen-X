"""Repository tests for the standalone Composition Engine slice."""

from __future__ import annotations

from .. import runtime
from ..repository import CompositionEngineRepository
from ..repository import repository_manifest


def _build_state():
    state = runtime.composition_engine_empty_state()
    state = runtime.composition_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_targets": ("web", "admin"),
            "allowed_layout_modes": ("grid", "flow"),
            "publication_mode": "side_effect_free_plan",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = runtime.composition_engine_set_parameter(state, "route_budget", 24)["state"]
    state = runtime.composition_engine_register_rule(
        state,
        {
            "rule_id": "repo_rule",
            "tenant": "tenant_repo",
            "scope": "workspace",
            "required_fragments": ("CompositionWorkbench",),
            "allowed_meshes": ("platform", "relationship"),
            "route_policy": "balanced",
            "requires_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    state = runtime.composition_engine_receive_event(
        state,
        {
            "event_id": "evt_repo_schema",
            "event_type": "SchemaAccepted",
            "payload": {"tenant": "tenant_repo", "schema_id": "CustomerProfile", "owner_pbc": "customer_360"},
        },
    )["state"]
    state = runtime.composition_engine_create_workspace(
        state,
        {
            "workspace_id": "ws_repo",
            "tenant": "tenant_repo",
            "name": "Repository Workspace",
            "owner": "repo_owner",
            "target": "web",
        },
    )["state"]
    state = runtime.composition_engine_select_pbc(
        state,
        "ws_repo",
        {"pbc": "customer_360", "mesh": "relationship", "reason": "repository-backed workspace"},
    )["state"]
    state = runtime.composition_engine_register_component(
        state,
        {
            "component_id": "cmp_repo",
            "tenant": "tenant_repo",
            "pbc": "customer_360",
            "fragment": "CompositionWorkbench",
            "permissions": ("composition_engine.compose",),
            "schemas": ("CustomerProfile",),
        },
    )["state"]
    state = runtime.composition_engine_register_ui_fragment(
        state,
        {
            "fragment_id": "frag_repo",
            "tenant": "tenant_repo",
            "component_id": "cmp_repo",
            "route": "/customers/repository",
            "slots": ("main",),
            "events": ("CustomerProfile",),
        },
    )["state"]
    state = runtime.composition_engine_bind_layout(
        state,
        {
            "binding_id": "bind_repo",
            "tenant": "tenant_repo",
            "workspace_id": "ws_repo",
            "page": "home",
            "slot": "main",
            "fragment_id": "frag_repo",
            "projection": "customer_profile_projection",
        },
    )["state"]
    state = runtime.composition_engine_validate_composition_plan(state, "ws_repo")["state"]
    state = runtime.composition_engine_generate_composition_dsl(state, "ws_repo")["state"]
    state = runtime.composition_engine_publish_composition(state, "ws_repo")["state"]
    return state


def test_repository_manifest_and_smoke() -> None:
    manifest = repository_manifest()
    from ..repository import smoke_test

    smoke = smoke_test()
    assert manifest["ok"] is True
    assert manifest["repository_class"] == "CompositionEngineRepository"
    assert manifest["runtime_tables"]
    assert smoke["ok"] is True


def test_repository_applies_migrations_and_syncs_runtime_state() -> None:
    repository = CompositionEngineRepository()
    applied = repository.apply_migrations()
    state = _build_state()
    repository.sync_state(state)

    workspace = repository.fetch_workspace("ws_repo")
    summary = repository.workspace_summary(tenant="tenant_repo")
    outbox_rows = repository.list_rows(runtime.COMPOSITION_ENGINE_RUNTIME_TABLES[0])
    release_rows = repository.list_rows("composition_engine_release_evidence", tenant="tenant_repo")

    assert applied == ("001_initial.sql",)
    assert workspace is not None
    assert workspace["workspace_id"] == "ws_repo"
    assert tuple(workspace["selected_pbcs"]) == ("customer_360",)
    assert summary["workspace_count"] == 1
    assert summary["published_count"] == 1
    assert summary["binding_count"] == 1
    assert summary["package_plan_count"] == 1
    assert summary["release_evidence_count"] == 1
    assert len(outbox_rows) >= 3
    assert release_rows[0]["status"] == "published"

    repository.close()
