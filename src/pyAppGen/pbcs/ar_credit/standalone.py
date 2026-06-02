"""Standalone one-PBC application surface for ar_credit."""

from __future__ import annotations

from . import routes
from . import ui
from .controls import ar_credit_control_center
from .forms import ar_credit_prepare_form_submission
from .repository import ArCreditRepository
from .repository import REPOSITORY_TABLES
from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC
from .seed_data import DEFAULT_CONFIGURATION
from .seed_data import DEFAULT_PARAMETERS
from .seed_data import DEFAULT_RULE
from .seed_data import load_demo_state
from .services import ArCreditService
from .wizards import ar_credit_plan_wizard


def standalone_app_manifest() -> dict:
    service = ArCreditService(state=load_demo_state()["state"])
    return {
        "ok": True,
        "pbc": "ar_credit",
        "app": ui.ar_credit_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service.service_operation_manifest() if hasattr(service, "service_operation_manifest") else None,
        "repository_tables": REPOSITORY_TABLES,
        "side_effects": (),
    }


class ArCreditStandaloneApp:
    """Package-local standalone app that owns the AR runtime state and snapshot store."""

    def __init__(self, *, database_path: str = ":memory:", state: dict | None = None, tenant: str = "tenant_demo"):
        self.tenant = tenant
        self.repository = ArCreditRepository(database_path=database_path)
        self.repository.apply_migrations()
        loaded_state = self.repository.load_state(tenant, snapshot_kind="latest") if state is None else state
        self.service = ArCreditService(state=loaded_state)

    @property
    def state(self) -> dict | None:
        return self.service.state

    def close(self) -> None:
        self.repository.close()

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        result = routes.dispatch_route(method, path, payload, service=self.service)
        self._persist_route_result(method=method, path=path, payload=payload or {}, result=result)
        return result

    def bootstrap(self, *, tenant: str | None = None) -> dict:
        tenant = tenant or self.tenant
        if self.service.state is None:
            self.service.state = {}
        self.service.state = self.service.state or {}
        if not self.service.state.get("configuration"):
            self.service.state = load_demo_state(tenant=tenant, include_transactions=False)["state"]
        self.repository.save_state(tenant, self.service.state, snapshot_kind="latest", captured_at="2026-05-29T00:00:00Z")
        self.repository.record_workflow_run(
            run_id=f"{tenant}-bootstrap",
            tenant=tenant,
            workflow_name="bootstrap",
            status="completed",
            summary={
                "configuration": DEFAULT_CONFIGURATION,
                "parameters": DEFAULT_PARAMETERS,
                "rule": {**DEFAULT_RULE, "tenant": tenant, "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC},
            },
            created_at="2026-05-29T00:00:00Z",
        )
        return {"ok": True, "tenant": tenant, "state": self.service.state, "side_effects": ()}

    def submit_form(self, form_id: str, payload: dict | None = None) -> dict:
        prepared = ar_credit_prepare_form_submission(form_id, payload)
        if prepared["ok"] is not True:
            return prepared
        dispatch_payload = dict(prepared["payload"])
        dispatch_payload["state"] = self.service.state
        result = self.dispatch(prepared["method"], prepared["path"], dispatch_payload)
        self.repository.record_workflow_run(
            run_id=f"{form_id}-{len(self.repository.list_workflow_runs(tenant=self.tenant)) + 1}",
            tenant=self.tenant,
            workflow_name=form_id,
            status="completed" if result.get("ok") else "failed",
            summary={
                "route": prepared["path"],
                "operation": prepared["form"]["operation"],
                "payload_keys": tuple(sorted(dict(payload or {}))),
            },
            created_at="2026-05-29T00:00:00Z",
        )
        return {
            "ok": result.get("ok") is True,
            "form": prepared["form"],
            "result": result,
            "side_effects": (),
        }

    def plan_wizard(self, wizard_id: str, context: dict | None = None) -> dict:
        return ar_credit_plan_wizard(wizard_id, context)

    def load_demo_workspace(self, *, tenant: str | None = None) -> dict:
        tenant = tenant or self.tenant
        seeded = load_demo_state(tenant=tenant)
        self.service.state = seeded["state"]
        self.repository.save_state(tenant, self.service.state, snapshot_kind="latest", captured_at="2026-05-29T00:00:00Z")
        self.repository.record_workflow_run(
            run_id=f"{tenant}-seed-demo",
            tenant=tenant,
            workflow_name="load_demo_workspace",
            status="completed",
            summary={
                "customer_id": seeded["customer"]["customer_id"],
                "invoice_id": seeded["invoice"]["invoice_id"],
                "receipt_id": seeded["receipt"]["receipt_id"],
            },
            created_at="2026-05-29T00:00:00Z",
        )
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str | None = None, principal_permissions: tuple[str, ...] | None = None) -> dict:
        tenant = tenant or self.tenant
        permissions = principal_permissions or tuple(sorted(set(ui.ar_credit_ui_contract()["action_permissions"].values())))
        return ui.ar_credit_render_standalone_app(self.state or {}, tenant=tenant, principal_permissions=permissions)

    def control_center(self, *, tenant: str | None = None, as_of: str = "2026-06-30") -> dict:
        return ar_credit_control_center(self.state or {}, tenant=tenant or self.tenant, as_of=as_of)

    def release_snapshot(self, *, tenant: str | None = None) -> dict:
        from . import release_evidence

        tenant = tenant or self.tenant
        evidence = release_evidence.build_release_evidence()
        self.repository.save_release_snapshot(
            snapshot_id=f"{tenant}-release",
            tenant=tenant,
            evidence=evidence,
            created_at="2026-05-29T00:00:00Z",
        )
        return evidence

    def _persist_route_result(self, *, method: str, path: str, payload: dict, result: dict) -> None:
        if self.state is None:
            return
        self.repository.save_state(self.tenant, self.state, snapshot_kind="latest", captured_at="2026-05-29T00:00:00Z")
        self.repository.record_workflow_run(
            run_id=f"{method.lower()}-{len(self.repository.list_workflow_runs(tenant=self.tenant)) + 1}",
            tenant=self.tenant,
            workflow_name=f"{method} {path}",
            status="completed" if result.get("ok") else "failed",
            summary={
                "path": path,
                "payload_keys": tuple(sorted(payload)),
                "handled": result.get("handled"),
            },
            created_at="2026-05-29T00:00:00Z",
        )


def workbench_smoke_test() -> dict:
    app = ArCreditStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    controls = app.control_center(tenant="tenant_demo")
    latest_state = app.repository.load_state("tenant_demo")
    workflow_runs = app.repository.list_workflow_runs(tenant="tenant_demo")
    manifest = app.repository.database_manifest()
    app.close()
    return {
        "ok": loaded["ok"] and rendered["ok"] and controls["ok"] and latest_state is not None and bool(workflow_runs),
        "loaded": loaded,
        "rendered": rendered,
        "controls": controls,
        "workflow_runs": workflow_runs,
        "repository": manifest,
        "side_effects": (),
    }


def smoke_test() -> dict:
    app = ArCreditStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot(tenant="tenant_demo")
    latest_release = app.repository.latest_release_snapshot(tenant="tenant_demo")
    app.close()
    return {
        "ok": loaded["ok"] and rendered["ok"] and release_snapshot["ok"] and latest_release is not None,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "latest_release": latest_release,
        "side_effects": (),
    }
