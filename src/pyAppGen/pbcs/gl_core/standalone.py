"""Standalone one-PBC application surface for gl_core."""

from __future__ import annotations

from . import routes
from . import ui
from .repository import GlCoreRepository
from .repository import gl_core_repository_manifest
from .runtime import GL_CORE_REQUIRED_EVENT_TOPIC
from .runtime import gl_core_configure_runtime
from .runtime import gl_core_register_rule
from .runtime import gl_core_set_parameter
from .services import GlCoreService


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "allowed_account_types": ("asset", "liability", "equity", "revenue", "expense"),
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "approval_threshold": 1000.0,
    "materiality_threshold": 0.05,
    "close_tolerance": 0.0,
    "revaluation_threshold": 5000.0,
    "retention_days": 2555,
    "workbench_limit": 100,
}
DEFAULT_RULE = {
    "rule_id": "gl_core.default_posting_policy",
    "tenant": "tenant_demo",
    "scope": "journal_posting",
    "status": "active",
    "requires_balance": True,
    "requires_approval_over": 1000.0,
}


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    return {
        "ok": True,
        "pbc": "gl_core",
        "app": ui.gl_core_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "repository": gl_core_repository_manifest(),
        "side_effects": (),
    }


class GlCoreStandaloneApp:
    """Package-local standalone app that owns GL runtime and repository state."""

    def __init__(self, state: dict | None = None):
        self.service = GlCoreService(state=state)
        self.repository = GlCoreRepository(state=self.service.state)
        self.service.state = self.repository.state


    def _sync_state(self) -> None:
        self.repository = GlCoreRepository(state=self.service.state)
        self.service.state = self.repository.state

    def _adopt_state(self, state: dict) -> None:
        self.repository = GlCoreRepository(state=state)
        self.service.state = self.repository.state

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        result = routes.dispatch_route(method, path, payload, service=self.service)
        self._sync_state()
        return result

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        state = gl_core_configure_runtime(self.state, DEFAULT_CONFIGURATION)["state"]
        for name, value in DEFAULT_PARAMETERS.items():
            state = gl_core_set_parameter(state, name, value)["state"]
        state = gl_core_register_rule(state, {**DEFAULT_RULE, "tenant": tenant})["state"]
        self._adopt_state(state)
        seeded = self.repository.seed_defaults(tenant=tenant)
        self._adopt_state(seeded["state"])
        consumed = self.dispatch(
            "POST",
            "/api/pbc/gl_core/gl/events/inbox",
            {
                "envelope": {
                    "event_id": f"invoice-{tenant}",
                    "event_type": "InvoiceApproved",
                    "payload": {
                        "tenant": tenant,
                        "invoice_id": f"inv-{tenant}",
                        "amount": 1250.0,
                    },
                }
            },
        )
        return {
            "ok": seeded["ok"] and consumed["ok"],
            "tenant": tenant,
            "repository_seed": seeded,
            "consumed": consumed,
            "state": self.state,
            "side_effects": (),
        }

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        source_document = self.repository.save_source_document(
            {
                "tenant": tenant,
                "document_id": f"doc-{tenant}",
                "source_hash": f"hash-{tenant}",
                "derived_account": "product_revenue",
                "confidence": 0.94,
                "audit_trace": "semantic derivation from approved invoice and controller note",
            }
        )
        self._adopt_state(source_document["state"])
        draft = self.repository.save_journal_draft(
            {
                "tenant": tenant,
                "journal_id": f"je-{tenant}",
                "period_id": "2026-05",
                "source_document_hash": f"hash-{tenant}",
            },
            (
                {"account_id": "cash_main", "debit": 1250.0, "credit": 0.0, "currency": "USD", "dimensions": {"entity": "hq", "source": "invoice"}},
                {"account_id": "product_revenue", "debit": 0.0, "credit": 1250.0, "currency": "USD", "dimensions": {"entity": "hq", "source": "invoice"}},
            ),
        )
        self._adopt_state(draft["state"])
        posted = self.dispatch(
            "POST",
            "/api/pbc/gl_core/gl/journal-events",
            {
                "event_type": "JournalPosted",
                "payload": {
                    "tenant": tenant,
                    "valid_at": "2026-05-31T00:00:00Z",
                    "lines": (
                        {"account": "cash_main", "debit": 1250.0, "credit": 0.0},
                        {"account": "product_revenue", "debit": 0.0, "credit": 1250.0},
                    ),
                    "source_text": "customer invoice revenue cash",
                },
            },
        )
        close = self.dispatch(
            "POST",
            "/api/pbc/gl_core/gl/close-snapshots",
            {"tenant": tenant},
        )
        reconciliation = self.dispatch(
            "POST",
            "/api/pbc/gl_core/gl/reconciliations",
            {"source_items": ({"source_id": f"bank-{tenant}", "amount": 1250.0},)},
        )
        return {
            "ok": draft["ok"] and posted["ok"] and close["ok"] and reconciliation["ok"],
            "tenant": tenant,
            "source_document": source_document,
            "draft": draft,
            "posted": posted,
            "close": close,
            "reconciliation": reconciliation,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.gl_core_ui_contract()["action_permissions"].values())))
        return ui.gl_core_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = GlCoreStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and rendered["ok"]
        and rendered["workbench"]["cards"][0]["value"] >= 1
        and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }


def workbench_smoke_test() -> dict:
    """Exercise bootstrap, route dispatch, and rendering without release recursion."""
    app = GlCoreStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
