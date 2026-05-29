"""Standalone one-PBC application surface for schema_registry."""

from __future__ import annotations

from . import agent
from . import release_evidence
from . import routes
from . import ui
from .repository import SchemaRegistryRepository
from .runtime import SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC
from .services import SchemaRegistryService


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "allowed_formats": ("json", "avro", "event", "api", "projection"),
    "default_compatibility": "backward_forward",
    "namespace_policy": "tenant_scoped",
    "default_timezone": "UTC",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "compatibility_threshold": 0.9,
    "max_schema_fields": 64,
    "semantic_similarity_floor": 0.82,
    "violation_risk_threshold": 0.45,
    "review_sla_hours": 24,
    "retention_days": 365,
}
DEFAULT_RULE = {
    "rule_id": "schema_registry.release_readiness",
    "tenant": "tenant_demo",
    "scope": "event",
    "mode": "backward_forward",
    "classification": "internal",
    "severity": "high",
    "status": "active",
}
DEFAULT_COMPATIBILITY_RULE = {
    "rule_id": "compatibility_rule.default",
    "tenant": "tenant_demo",
    "subject_id": "subject_demo_order_created",
    "mode": "backward_forward",
    "status": "active",
    "transitive": True,
}
DEFAULT_SUBJECT = {
    "subject_id": "subject_demo_order_created",
    "tenant": "tenant_demo",
    "owner_pbc": "schema_registry",
    "name": "tenant_demo.order.created",
    "channel": "event",
    "format": "json",
    "namespace": "tenant_demo.orders",
}
DEFAULT_SCHEMA_VERSION = {
    "version_id": "version_demo_order_created_v1",
    "tenant": "tenant_demo",
    "subject_id": "subject_demo_order_created",
    "semantic_version": "1.0.0",
    "schema": {
        "fields": {
            "order_id": {"type": "string", "required": True},
            "total_amount": {"type": "number", "required": True},
            "currency": {"type": "string", "required": True},
        }
    },
}
DEFAULT_CONSUMER_BINDING = {
    "binding_id": "binding_demo_order_created_gateway",
    "tenant": "tenant_demo",
    "subject_id": "subject_demo_order_created",
    "consumer_pbc": "api_gateway_mesh",
    "consumer_type": "projection",
    "min_version": "1.0.0",
}
DEFAULT_VIOLATION = {
    "violation_id": "violation_demo_order_created",
    "tenant": "tenant_demo",
    "subject_id": "subject_demo_order_created",
    "producer_pbc": "schema_registry",
    "consumer_pbc": "api_gateway_mesh",
    "severity": "high",
    "reason": "consumer rollout pending for additive field adoption",
    "status": "open",
}
DEFAULT_EVENT = {
    "event_type": "PbcDeployed",
    "event_id": "event_demo_deployment",
    "payload": {
        "tenant": "tenant_demo",
        "pbc": "schema_registry",
        "version": "1.0.0",
    },
}


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    return {
        "ok": True,
        "pbc": "schema_registry",
        "app": ui.schema_registry_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": SchemaRegistryService().query_release_evidence({})["operation_contract"],
        "repository": {
            "format": "appgen.schema-registry-standalone-app.v1",
            "backing_store": "owned_relational_tables_plus_runtime_state",
        },
        "agent": agent.standalone_agent_workspace_contract(),
        "side_effects": (),
    }


class SchemaRegistryStandaloneApp:
    """Package-local standalone app that owns the Schema Registry runtime state."""

    def __init__(self, state: dict | None = None):
        self.repository = SchemaRegistryRepository(state=state)
        self.service = SchemaRegistryService(repository=self.repository)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        configuration = dict(DEFAULT_CONFIGURATION)
        self.dispatch("POST", "/api/pbc/schema_registry/runtime/configuration", {"configuration": configuration})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch("POST", "/api/pbc/schema_registry/runtime/parameters", {"name": name, "value": value})
        runtime_rule = {**DEFAULT_RULE, "tenant": tenant}
        self.dispatch("POST", "/api/pbc/schema_registry/runtime/rules", {"rule": runtime_rule})
        self.dispatch("POST", "/api/pbc/schema_registry/events/inbox", {"envelope": {**DEFAULT_EVENT, "payload": {**DEFAULT_EVENT["payload"], "tenant": tenant}}})
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        subject = {**DEFAULT_SUBJECT, "tenant": tenant, "name": f"{tenant}.order.created", "namespace": f"{tenant}.orders"}
        version = {**DEFAULT_SCHEMA_VERSION, "tenant": tenant, "subject_id": subject["subject_id"]}
        consumer_binding = {**DEFAULT_CONSUMER_BINDING, "tenant": tenant, "subject_id": subject["subject_id"]}
        compatibility_rule = {**DEFAULT_COMPATIBILITY_RULE, "tenant": tenant, "subject_id": subject["subject_id"]}
        violation = {**DEFAULT_VIOLATION, "tenant": tenant, "subject_id": subject["subject_id"]}
        self.dispatch("POST", "/api/pbc/schema_registry/subjects", {"subject": subject})
        self.dispatch("POST", "/api/pbc/schema_registry/compatibility-rules", {"rule": compatibility_rule})
        self.dispatch("POST", "/api/pbc/schema_registry/versions", {"version": version})
        self.dispatch("POST", "/api/pbc/schema_registry/consumer-bindings", {"binding": consumer_binding})
        self.dispatch("POST", "/api/pbc/schema_registry/compatibility-checks", {"subject_id": subject["subject_id"], "proposed_schema": {"fields": {"order_id": {"type": "string", "required": True}, "total_amount": {"type": "number", "required": True}, "currency": {"type": "string", "required": True}, "order_source": {"type": "string", "required": False}}}})
        self.dispatch("POST", "/api/pbc/schema_registry/payload-validations", {"subject_id": subject["subject_id"], "payload": {"order_id": "ORD-100", "total_amount": 125.0, "currency": "USD"}})
        self.dispatch("POST", "/api/pbc/schema_registry/violations", {"violation": violation})
        self.dispatch("POST", "/api/pbc/schema_registry/projections", {"subject_id": subject["subject_id"], "systems": ("gateway", "audit", "composition", "workflow")})
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "assistant": self.assistant_workspace(),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.schema_registry_ui_contract()["action_permissions"].values())))
        return ui.schema_registry_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def assistant_workspace(self) -> dict:
        return agent.standalone_agent_workspace_contract()

    def release_snapshot(self) -> dict:
        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = SchemaRegistryStandaloneApp()
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
