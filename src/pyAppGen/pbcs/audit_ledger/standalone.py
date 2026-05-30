"""Standalone one-PBC app surface for audit_ledger."""

from __future__ import annotations

from . import routes
from . import ui
from .repository import AuditLedgerRepository
from .repository import repository_smoke_test
from .runtime import AUDIT_LEDGER_REQUIRED_EVENT_TOPIC
from .services import AuditLedgerStandaloneService


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "signature_algorithm": "dilithium3_simulated",
    "allowed_classifications": ("public", "internal", "regulated"),
    "export_modes": ("proof_bundle", "forensic_archive"),
    "default_timezone": "UTC",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "retention_days": 2555,
    "export_batch_limit": 500,
    "tamper_risk_threshold": 0.35,
    "control_failure_threshold": 0.2,
    "proof_disclosure_limit": 4,
    "review_sla_hours": 24,
}
DEFAULT_RULE = {
    "rule_id": "audit_ledger.release_readiness",
    "tenant": "tenant_demo",
    "scope": "release_gate",
    "classification": "regulated",
    "minimum_retention_days": 2555,
    "requires_legal_hold_review": True,
    "requires_export_approval": True,
    "severity": "blocking",
    "status": "active",
}


def standalone_app_manifest() -> dict:
    """Return the composed standalone-app contribution from this package."""
    repository = AuditLedgerRepository()
    try:
        service_contract = AuditLedgerStandaloneService(repository=repository).standalone_service_manifest()
        return {
            "ok": True,
            "pbc": "audit_ledger",
            "app": ui.audit_ledger_standalone_app_contract(),
            "routes": routes.standalone_route_contracts()["routes"],
            "service": service_contract,
            "repository": repository.repository_contract(),
            "side_effects": (),
        }
    finally:
        repository.close()


class AuditLedgerStandaloneApp:
    """Package-local standalone app that owns audit-ledger runtime state."""

    def __init__(self, database_path: str = ":memory:", repository: AuditLedgerRepository | None = None):
        self.repository = repository or AuditLedgerRepository(database_path=database_path)
        self.service = AuditLedgerStandaloneService(repository=self.repository)

    @property
    def state(self) -> dict:
        return self.repository.load_state()

    def close(self) -> None:
        self.service.close()

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_standalone_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.dispatch(
            "POST",
            "/app/audit-ledger/runtime/configuration",
            {"configuration": DEFAULT_CONFIGURATION},
        )
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch(
                "POST",
                "/app/audit-ledger/runtime/parameters",
                {"name": name, "value": value},
            )
        self.dispatch(
            "POST",
            "/app/audit-ledger/runtime/rules",
            {"rule": {**DEFAULT_RULE, "tenant": tenant}},
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/events/inbox",
            {
                "envelope": {
                    "event_id": f"route-{tenant}",
                    "event_type": "RoutePublished",
                    "payload": {
                        "tenant": tenant,
                        "route_id": f"route-{tenant}",
                        "service_id": f"svc-{tenant}",
                    },
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST",
            "/app/audit-ledger/audit-events",
            {
                "audit_event": {
                    "audit_id": f"audit-{tenant}",
                    "tenant": tenant,
                    "source_pbc": "api_gateway_mesh",
                    "aggregate_id": f"route-{tenant}",
                    "actor": "standalone_operator",
                    "action": "publish_route",
                    "classification": "regulated",
                    "payload": {"route_id": f"route-{tenant}", "method": "POST"},
                    "occurred_at": "2026-05-29T09:00:00Z",
                }
            },
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/access-evidence",
            {
                "evidence": {
                    "evidence_id": f"access-{tenant}",
                    "tenant": tenant,
                    "principal": "standalone_operator",
                    "resource": f"route-{tenant}",
                    "action": "publish_route",
                    "decision": "allow",
                    "context": {"risk": "low", "channel": "standalone"},
                    "policy_source": "identity_access_projection",
                }
            },
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/retention-policies",
            {
                "policy": {
                    "policy_id": f"retention-{tenant}",
                    "tenant": tenant,
                    "classification": "regulated",
                    "retention_days": 2555,
                    "legal_hold": False,
                    "disposal_action": "review",
                }
            },
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/control-assertions",
            {
                "assertion": {
                    "control_id": f"control-{tenant}",
                    "tenant": tenant,
                    "control": "signature_chain_complete",
                    "status": "pass",
                    "severity": "blocking",
                    "evidence": (f"audit-{tenant}",),
                }
            },
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/forensic-exports",
            {
                "export": {
                    "export_id": f"export-{tenant}",
                    "tenant": tenant,
                    "classification": "regulated",
                    "requested_by": "auditor",
                    "purpose": "incident_review",
                    "disclosure": ("audit_id", "actor", "action", "payload_hash"),
                }
            },
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/signature-chain/verify",
            {"tenant": tenant},
        )
        self.dispatch(
            "POST",
            "/app/audit-ledger/projections",
            {"audit_id": f"audit-{tenant}", "systems": ("identity", "gateway", "workflow")},
        )
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(
            sorted(set(ui.audit_ledger_ui_contract()["action_permissions"].values()))
        )
        return ui.audit_ledger_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions,
        )

    def release_snapshot(self, *, tenant: str) -> dict:
        return self.repository.release_snapshot(tenant=tenant)


def smoke_test() -> dict:
    """Exercise the standalone app end-to-end."""
    app = AuditLedgerStandaloneApp()
    try:
        loaded = app.load_demo_workspace()
        rendered = app.render_workbench(tenant="tenant_demo")
        release_snapshot = app.release_snapshot(tenant="tenant_demo")
        return {
            "ok": loaded["ok"]
            and rendered["ok"]
            and rendered["workbench"]["cards"][0]["value"] >= 1
            and release_snapshot["ok"]
            and repository_smoke_test()["ok"],
            "manifest": standalone_app_manifest(),
            "loaded": loaded,
            "rendered": rendered,
            "release_snapshot": release_snapshot,
            "side_effects": (),
        }
    finally:
        app.close()
