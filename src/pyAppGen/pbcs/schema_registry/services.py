"""Command/query service layer for the schema_registry standalone PBC."""

from __future__ import annotations

from .repository import SchemaRegistryRepository


PBC_KEY = "schema_registry"
EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": "pbc.schema_registry.events",
    "inbox_topic": "pbc.schema_registry.inbox",
    "outbox_table": "schema_registry_appgen_outbox_event",
    "inbox_table": "schema_registry_appgen_inbox_event",
    "dead_letter_table": "schema_registry_dead_letter_event",
    "retry_policy": {"name": "schema_registry_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "schema_registry_appgen_inbox_event"},
}

OPERATION_CONTRACTS = (
    {
        "operation": "configure_runtime",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/runtime/configuration",
        "permission": "schema_registry.configure",
        "owned_tables": ("schema_registry_schema_configuration",),
        "read_tables": (),
        "emitted_event": None,
        "idempotency_required": True,
        "idempotency_key": "schema_registry:configure_runtime:tenant",
    },
    {
        "operation": "set_parameter",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/runtime/parameters",
        "permission": "schema_registry.configure",
        "owned_tables": ("schema_registry_schema_parameter",),
        "read_tables": (),
        "emitted_event": None,
        "idempotency_required": True,
        "idempotency_key": "schema_registry:set_parameter:key",
    },
    {
        "operation": "register_rule",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/runtime/rules",
        "permission": "schema_registry.configure",
        "owned_tables": ("schema_registry_schema_rule",),
        "read_tables": (),
        "emitted_event": None,
        "idempotency_required": True,
        "idempotency_key": "schema_registry:register_rule:rule_id",
    },
    {
        "operation": "receive_event",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/events/inbox",
        "permission": "schema_registry.event",
        "owned_tables": (
            "schema_registry_appgen_inbox_event",
            "schema_registry_appgen_outbox_event",
            "schema_registry_dead_letter_event",
        ),
        "read_tables": (),
        "emitted_event": None,
        "idempotency_required": True,
        "idempotency_key": "schema_registry:receive_event:event_id",
    },
    {
        "operation": "register_subject",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/subjects",
        "permission": "schema_registry.register",
        "owned_tables": ("schema_registry_schema_subject", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "SchemaSubjectRegistered",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:register_subject:subject_id",
    },
    {
        "operation": "define_compatibility_rule",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/compatibility-rules",
        "permission": "schema_registry.approve",
        "owned_tables": ("schema_registry_compatibility_rule", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "CompatibilityRuleChanged",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:define_compatibility_rule:rule_id",
    },
    {
        "operation": "register_consumer_binding",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/consumer-bindings",
        "permission": "schema_registry.register",
        "owned_tables": ("schema_registry_consumer_binding",),
        "read_tables": (),
        "emitted_event": None,
        "idempotency_required": True,
        "idempotency_key": "schema_registry:register_consumer_binding:binding_id",
    },
    {
        "operation": "submit_schema_version",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/versions",
        "permission": "schema_registry.register",
        "owned_tables": ("schema_registry_schema_version", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "SchemaAccepted",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:submit_schema_version:version_id",
    },
    {
        "operation": "run_compatibility_check",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/compatibility-checks",
        "permission": "schema_registry.validate",
        "owned_tables": ("schema_registry_validation_run", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "BreakingSchemaBlocked",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:run_compatibility_check:subject_id",
    },
    {
        "operation": "validate_payload",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/payload-validations",
        "permission": "schema_registry.validate",
        "owned_tables": ("schema_registry_validation_run", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "PayloadValidated",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:validate_payload:subject_id",
    },
    {
        "operation": "record_contract_violation",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/violations",
        "permission": "schema_registry.triage",
        "owned_tables": ("schema_registry_contract_violation", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "ContractViolationRecorded",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:record_contract_violation:violation_id",
    },
    {
        "operation": "publish_contract_projection",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/schema_registry/projections",
        "permission": "schema_registry.publish",
        "owned_tables": ("schema_registry_contract_projection", "schema_registry_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "ContractProjectionPublished",
        "idempotency_required": True,
        "idempotency_key": "schema_registry:publish_contract_projection:subject_id",
    },
    {
        "operation": "query_subjects",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/schema_registry/subjects",
        "permission": "schema_registry.read",
        "owned_tables": (),
        "read_tables": (
            "schema_registry_schema_subject",
            "schema_registry_schema_version",
            "schema_registry_consumer_binding",
        ),
        "emitted_event": None,
        "idempotency_required": False,
        "idempotency_key": None,
    },
    {
        "operation": "query_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/schema_registry/workbench",
        "permission": "schema_registry.audit",
        "owned_tables": (),
        "read_tables": (
            "schema_registry_schema_subject",
            "schema_registry_schema_version",
            "schema_registry_validation_run",
            "schema_registry_contract_violation",
            "schema_registry_consumer_binding",
            "schema_registry_appgen_outbox_event",
            "schema_registry_appgen_inbox_event",
            "schema_registry_dead_letter_event",
        ),
        "emitted_event": None,
        "idempotency_required": False,
        "idempotency_key": None,
    },
    {
        "operation": "query_release_evidence",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/schema_registry/release-evidence",
        "permission": "schema_registry.audit",
        "owned_tables": (),
        "read_tables": (
            "schema_registry_schema_subject",
            "schema_registry_schema_version",
            "schema_registry_contract_violation",
        ),
        "emitted_event": None,
        "idempotency_required": False,
        "idempotency_key": None,
    },
)


def _contract_with_defaults(contract: dict) -> dict:
    return {
        **contract,
        "event_contract": "AppGen-X",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    contracts = tuple(_contract_with_defaults(item) for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in contracts if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in contracts if item["operation_kind"] == "query")
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in contracts),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": contracts,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in service_operation_contracts()["contracts"] if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "idempotency_required": contract["idempotency_required"],
        "idempotency_key": contract["idempotency_key"],
        "side_effects": (),
    }


class SchemaRegistryService:
    """Stateful standalone service that delegates to the package repository."""

    def __init__(self, state: dict | None = None, repository: SchemaRegistryRepository | None = None):
        self.repository = repository or SchemaRegistryRepository(state=state)

    @property
    def state(self) -> dict:
        return self.repository.state

    def _dispatch(self, operation_name: str, payload: dict | None) -> dict:
        body = dict(payload or {})
        if operation_name == "configure_runtime":
            return self.repository.configure_runtime(body.get("configuration", body))
        if operation_name == "set_parameter":
            return self.repository.set_parameter(body["name"], body["value"])
        if operation_name == "register_rule":
            return self.repository.register_rule(body.get("rule", body))
        if operation_name == "receive_event":
            return self.repository.receive_event(body.get("envelope", body))
        if operation_name == "register_subject":
            return self.repository.register_subject(body.get("subject", body))
        if operation_name == "define_compatibility_rule":
            return self.repository.define_compatibility_rule(body.get("rule", body))
        if operation_name == "register_consumer_binding":
            return self.repository.register_consumer_binding(body.get("binding", body))
        if operation_name == "submit_schema_version":
            return self.repository.submit_schema_version(body.get("version", body))
        if operation_name == "run_compatibility_check":
            return self.repository.run_compatibility_check(body["subject_id"], body["proposed_schema"])
        if operation_name == "validate_payload":
            return self.repository.validate_payload(body["subject_id"], body["payload"])
        if operation_name == "record_contract_violation":
            return self.repository.record_contract_violation(body.get("violation", body))
        if operation_name == "publish_contract_projection":
            return self.repository.publish_contract_projection(body["subject_id"], tuple(body["systems"]))
        if operation_name == "query_subjects":
            return self.repository.list_subjects(tenant=body.get("tenant"))
        if operation_name == "query_workbench":
            return self.repository.build_workbench(tenant=body["tenant"])
        if operation_name == "query_release_evidence":
            from . import release_evidence

            evidence = release_evidence.build_release_evidence()
            return {
                "ok": evidence.get("ok") is True,
                "pbc": PBC_KEY,
                "release_evidence": evidence,
                "side_effects": (),
            }
        return {
            "ok": False,
            "pbc": PBC_KEY,
            "reason": "unknown_operation",
            "operation": operation_name,
            "side_effects": (),
        }

    def _execute(self, operation_name: str, payload: dict | None) -> dict:
        plan = operation_plan(operation_name, payload)
        execution = self._dispatch(operation_name, payload)
        result = {
            "ok": plan["ok"] and execution.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": plan.get("operation_kind"),
            "payload": dict(payload or {}),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "result": execution,
            "side_effects": (),
        }
        if plan.get("operation_kind") == "command":
            event_type = plan.get("emitted_event")
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (event_type,) if event_type else (),
                }
            )
        elif plan.get("operation_kind") == "query":
            result.update(
                {
                    "query": operation_name,
                    "read_only": True,
                    "outbox_table": None,
                    "emits": (),
                }
            )
        return result

    def configure_runtime(self, payload: dict | None = None) -> dict:
        return self._execute("configure_runtime", payload)

    def set_parameter(self, payload: dict | None = None) -> dict:
        return self._execute("set_parameter", payload)

    def register_rule(self, payload: dict | None = None) -> dict:
        return self._execute("register_rule", payload)

    def receive_event(self, payload: dict | None = None) -> dict:
        return self._execute("receive_event", payload)

    def register_subject(self, payload: dict | None = None) -> dict:
        return self._execute("register_subject", payload)

    def define_compatibility_rule(self, payload: dict | None = None) -> dict:
        return self._execute("define_compatibility_rule", payload)

    def register_consumer_binding(self, payload: dict | None = None) -> dict:
        return self._execute("register_consumer_binding", payload)

    def submit_schema_version(self, payload: dict | None = None) -> dict:
        return self._execute("submit_schema_version", payload)

    def run_compatibility_check(self, payload: dict | None = None) -> dict:
        return self._execute("run_compatibility_check", payload)

    def validate_payload(self, payload: dict | None = None) -> dict:
        return self._execute("validate_payload", payload)

    def record_contract_violation(self, payload: dict | None = None) -> dict:
        return self._execute("record_contract_violation", payload)

    def publish_contract_projection(self, payload: dict | None = None) -> dict:
        return self._execute("publish_contract_projection", payload)

    def query_subjects(self, payload: dict | None = None) -> dict:
        return self._execute("query_subjects", payload)

    def query_workbench(self, payload: dict | None = None) -> dict:
        return self._execute("query_workbench", payload)

    def query_release_evidence(self, payload: dict | None = None) -> dict:
        return self._execute("query_release_evidence", payload)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "SchemaRegistryService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute a subject-registration lifecycle through the standalone service."""
    service = SchemaRegistryService()
    service.configure_runtime(
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "appgen.schema.events",
                "retry_limit": 3,
                "allowed_formats": ("json", "avro", "event"),
                "default_compatibility": "backward_forward",
                "namespace_policy": "tenant_scoped",
                "default_timezone": "UTC",
                "workbench_limit": 100,
            }
        }
    )
    result = service.register_subject(
        {
            "subject": {
                "subject_id": "subject_smoke",
                "tenant": "tenant_smoke",
                "owner_pbc": "schema_registry",
                "name": "tenant_smoke.order.created",
                "channel": "event",
                "format": "json",
                "namespace": "tenant_smoke.orders",
            }
        }
    )
    return {
        "ok": service_operation_manifest()["ok"] and result.get("ok") is True and result["operation_contract"]["ok"],
        "manifest": service_operation_manifest(),
        "result": result,
        "side_effects": (),
    }
