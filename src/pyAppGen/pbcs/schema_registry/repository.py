"""Stateful repository facade for the schema_registry standalone PBC."""

from __future__ import annotations

from copy import deepcopy

from . import runtime


PBC_KEY = "schema_registry"

REPOSITORY_BINDINGS = (
    {
        "resource": "runtime_configuration",
        "table": "schema_registry_schema_configuration",
        "operation": "configure_runtime",
        "mode": "command",
    },
    {
        "resource": "runtime_parameter",
        "table": "schema_registry_schema_parameter",
        "operation": "set_parameter",
        "mode": "command",
    },
    {
        "resource": "governance_rule",
        "table": "schema_registry_schema_rule",
        "operation": "register_rule",
        "mode": "command",
    },
    {
        "resource": "inbox_event",
        "table": "schema_registry_appgen_inbox_event",
        "operation": "receive_event",
        "mode": "command",
    },
    {
        "resource": "schema_subject",
        "table": "schema_registry_schema_subject",
        "operation": "register_subject",
        "mode": "command",
    },
    {
        "resource": "compatibility_rule",
        "table": "schema_registry_compatibility_rule",
        "operation": "define_compatibility_rule",
        "mode": "command",
    },
    {
        "resource": "consumer_binding",
        "table": "schema_registry_consumer_binding",
        "operation": "register_consumer_binding",
        "mode": "command",
    },
    {
        "resource": "schema_version",
        "table": "schema_registry_schema_version",
        "operation": "submit_schema_version",
        "mode": "command",
    },
    {
        "resource": "validation_run",
        "table": "schema_registry_validation_run",
        "operation": "run_compatibility_check",
        "mode": "command",
    },
    {
        "resource": "payload_validation",
        "table": "schema_registry_validation_run",
        "operation": "validate_payload",
        "mode": "command",
    },
    {
        "resource": "contract_violation",
        "table": "schema_registry_contract_violation",
        "operation": "record_contract_violation",
        "mode": "command",
    },
    {
        "resource": "contract_projection",
        "table": "schema_registry_contract_projection",
        "operation": "publish_contract_projection",
        "mode": "command",
    },
    {
        "resource": "subject_catalog",
        "table": "schema_registry_schema_subject",
        "operation": "list_subjects",
        "mode": "query",
    },
    {
        "resource": "workbench",
        "table": "schema_registry_schema_subject",
        "operation": "build_workbench",
        "mode": "query",
    },
)


def _copy_payload(payload: dict | None) -> dict:
    return deepcopy(dict(payload or {}))


class SchemaRegistryRepository:
    """Own the standalone state and persist only inside the PBC boundary."""

    def __init__(self, state: dict | None = None):
        self._state = deepcopy(state) if state is not None else runtime.schema_registry_empty_state()

    @property
    def state(self) -> dict:
        return deepcopy(self._state)

    def _apply(self, result: dict) -> dict:
        if result.get("state") is not None:
            self._state = result["state"]
        return result

    def configure_runtime(self, configuration: dict) -> dict:
        return self._apply(runtime.schema_registry_configure_runtime(self._state, _copy_payload(configuration)))

    def set_parameter(self, key: str, value: int | float | str) -> dict:
        return self._apply(runtime.schema_registry_set_parameter(self._state, key, value))

    def register_rule(self, rule: dict) -> dict:
        return self._apply(runtime.schema_registry_register_rule(self._state, _copy_payload(rule)))

    def receive_event(self, envelope: dict) -> dict:
        return self._apply(runtime.schema_registry_receive_event(self._state, _copy_payload(envelope)))

    def register_subject(self, subject: dict) -> dict:
        return self._apply(runtime.schema_registry_register_subject(self._state, _copy_payload(subject)))

    def define_compatibility_rule(self, rule: dict) -> dict:
        return self._apply(runtime.schema_registry_define_compatibility_rule(self._state, _copy_payload(rule)))

    def register_consumer_binding(self, binding: dict) -> dict:
        return self._apply(runtime.schema_registry_register_consumer_binding(self._state, _copy_payload(binding)))

    def submit_schema_version(self, version: dict) -> dict:
        return self._apply(runtime.schema_registry_submit_schema_version(self._state, _copy_payload(version)))

    def run_compatibility_check(self, subject_id: str, proposed_schema: dict) -> dict:
        return self._apply(
            runtime.schema_registry_run_compatibility_check(self._state, subject_id, _copy_payload(proposed_schema))
        )

    def validate_payload(self, subject_id: str, payload: dict) -> dict:
        return self._apply(runtime.schema_registry_validate_payload(self._state, subject_id, _copy_payload(payload)))

    def record_contract_violation(self, violation: dict) -> dict:
        return self._apply(runtime.schema_registry_record_contract_violation(self._state, _copy_payload(violation)))

    def publish_contract_projection(self, subject_id: str, systems: tuple[str, ...]) -> dict:
        return self._apply(runtime.schema_registry_publish_contract_projection(self._state, subject_id, tuple(systems)))

    def list_subjects(self, *, tenant: str | None = None) -> dict:
        subjects = tuple(self._state["subjects"].values())
        filtered = tuple(subject for subject in subjects if tenant is None or subject.get("tenant") == tenant)
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "subjects": filtered,
            "count": len(filtered),
            "side_effects": (),
        }

    def build_workbench(self, *, tenant: str) -> dict:
        view = runtime.schema_registry_build_workbench_view(self._state, tenant=tenant)
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "view": view,
            "side_effects": (),
        }

    def persistence_plan(self, operation: str, payload: dict | None = None) -> dict:
        binding = next((item for item in REPOSITORY_BINDINGS if item["operation"] == operation), None)
        if binding is None:
            return {
                "ok": False,
                "pbc": PBC_KEY,
                "operation": operation,
                "reason": "unknown_repository_operation",
                "side_effects": (),
            }
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "operation": operation,
            "mode": binding["mode"],
            "resource": binding["resource"],
            "table": binding["table"],
            "payload_keys": tuple(sorted((payload or {}).keys())),
            "database_backends": runtime.SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS,
            "side_effects": (),
        }


def schema_registry_repository_manifest() -> dict:
    """Return the standalone repository contract for this PBC."""
    operations = tuple(binding["operation"] for binding in REPOSITORY_BINDINGS)
    command_operations = tuple(binding["operation"] for binding in REPOSITORY_BINDINGS if binding["mode"] == "command")
    query_operations = tuple(binding["operation"] for binding in REPOSITORY_BINDINGS if binding["mode"] == "query")
    return {
        "format": "appgen.schema-registry-repository.v1",
        "ok": bool(REPOSITORY_BINDINGS),
        "pbc": PBC_KEY,
        "backing_store": "owned_relational_tables_plus_runtime_state",
        "allowed_database_backends": runtime.SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS,
        "bindings": REPOSITORY_BINDINGS,
        "operations": operations,
        "command_operations": command_operations,
        "query_operations": query_operations,
        "shared_table_access": False,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the repository with a minimal subject lifecycle."""
    repository = SchemaRegistryRepository()
    configured = repository.configure_runtime(
        {
            "database_backend": "postgresql",
            "event_topic": runtime.SCHEMA_REGISTRY_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_formats": ("json", "avro", "event"),
            "default_compatibility": "backward_forward",
            "namespace_policy": "tenant_scoped",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        }
    )
    repository.set_parameter("compatibility_threshold", 0.8)
    subject = repository.register_subject(
        {
            "subject_id": "subject_smoke",
            "tenant": "tenant_smoke",
            "owner_pbc": "schema_registry",
            "name": "tenant_smoke.order.created",
            "channel": "event",
            "format": "json",
            "namespace": "tenant_smoke.orders",
        }
    )
    listing = repository.list_subjects(tenant="tenant_smoke")
    plan = repository.persistence_plan("register_subject", {"subject_id": "subject_smoke"})
    return {
        "ok": configured["ok"] and subject["ok"] and listing["count"] == 1 and plan["ok"],
        "manifest": schema_registry_repository_manifest(),
        "configured": configured,
        "subject": subject,
        "listing": listing,
        "plan": plan,
        "side_effects": (),
    }
