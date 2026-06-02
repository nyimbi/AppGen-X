"""Command/query services for the audit_ledger PBC."""

from __future__ import annotations

from .ledger_proofs import build_evidence_envelope
from .ledger_proofs import plan_disclosure_minimization
from .repository import AuditLedgerRepository
from .runtime import audit_ledger_build_api_contract
from .runtime import audit_ledger_build_service_contract

EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "adapter": "appgen_event_adapter",
    "topic": "appgen.audit.events",
    "inbox_topic": "appgen.audit.events",
    "outbox_table": "audit_ledger_appgen_outbox_event",
    "inbox_table": "audit_ledger_appgen_inbox_event",
    "dead_letter_table": "audit_ledger_dead_letter_event",
    "retry_policy": {"name": "audit_ledger_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "audit_ledger_appgen_inbox_event"},
}


def _path_for(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, f"/api/pbc/audit_ledger{path}"


def _operation_contracts() -> tuple[dict, ...]:
    api = audit_ledger_build_api_contract()
    contracts = []
    for route in api["routes"]:
        method, path = _path_for(route["route"])
        operation = route.get("command") or route.get("query")
        operation_kind = "command" if route.get("command") else "query"
        contracts.append(
            {
                "operation": operation,
                "operation_kind": operation_kind,
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": tuple(route.get("owned_tables", ())) if operation_kind == "command" else (),
                "read_tables": tuple(route.get("owned_tables", ())) if operation_kind == "query" else (),
                "emitted_event": tuple(route.get("emits", ()))[0] if operation_kind == "command" and route.get("emits") else None,
                "consumed_events": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _operation_contracts()


def preview_audit_event_envelope(payload: dict | None = None) -> dict:
    """Preview sealing evidence for one audit event without mutating state."""
    supplied = dict(payload or {})
    preview = build_evidence_envelope(supplied, sequence=1, previous_hash="genesis")
    return {
        "ok": preview["ok"],
        "operation": "record_audit_event",
        "event_contract": "AppGen-X",
        "preview": preview,
        "side_effects": (),
    }


def preview_forensic_export(payload: dict | None = None) -> dict:
    """Preview disclosure minimization for one export request without mutating state."""
    supplied = dict(payload or {})
    sample_events = tuple(supplied.get("sample_events", ()))
    if not sample_events and supplied.get("sample_event"):
        sample_events = (dict(supplied["sample_event"]),)
    plan = plan_disclosure_minimization(
        sample_events,
        classification=str(supplied.get("classification", "regulated")),
        requested_fields=tuple(supplied.get("disclosure", ())),
        purpose=str(supplied.get("purpose", "forensic_export")),
        approval_required=bool(supplied.get("approval_required", False)),
    )
    return {
        "ok": plan["ok"],
        "operation": "prepare_forensic_export",
        "event_contract": "AppGen-X",
        "preview": plan,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    service = audit_ledger_build_service_contract()
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "audit_ledger",
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "runtime_service": service,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"]
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "audit_ledger",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_events": contract["consumed_events"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "side_effects": (),
    }


class AuditLedgerService:
    """Side-effect-free command/query facade."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "audit_ledger",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_name == "record_audit_event":
            result["preview"] = preview_audit_event_envelope(payload)
        elif operation_name == "prepare_forensic_export":
            result["preview"] = preview_forensic_export(payload)
        if operation_kind == "command":
            event_type = plan.get("emitted_event")
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (event_type,) if event_type else (),
                }
            )
        elif operation_kind == "query":
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        return result

    def __getattr__(self, name: str):
        if name in {item["operation"] for item in OPERATION_CONTRACTS}:
            return lambda payload=None: self._execute(name, payload or {})
        raise AttributeError(name)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "audit_ledger",
        "service_class": "AuditLedgerService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "preview_operations": ("record_audit_event", "prepare_forensic_export"),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


STANDALONE_OPERATION_CONTRACTS = (
    {"operation": "configure_runtime", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/runtime/configuration", "handler": "configure_runtime", "permission": "audit_ledger.configure", "table": "audit_ledger_configuration", "form": "AuditLedgerConfigurationForm", "wizard": "AuditLedgerRuntimeSetupWizard"},
    {"operation": "set_parameter", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/runtime/parameters", "handler": "set_parameter", "permission": "audit_ledger.configure", "table": "audit_ledger_parameter", "form": "AuditLedgerParameterForm", "wizard": "AuditLedgerRuntimeSetupWizard"},
    {"operation": "register_rule", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/runtime/rules", "handler": "register_rule", "permission": "audit_ledger.configure", "table": "audit_ledger_rule", "form": "AuditLedgerRuleForm", "wizard": "AuditLedgerRetentionGovernanceWizard"},
    {"operation": "receive_event", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/events/inbox", "handler": "receive_event", "permission": "audit_ledger.event", "table": "audit_ledger_appgen_inbox_event", "form": "AuditLedgerInboxEventForm", "wizard": "AuditLedgerRuntimeSetupWizard"},
    {"operation": "record_audit_event", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/audit-events", "handler": "record_audit_event", "permission": "audit_ledger.seal", "table": "audit_ledger_audit_event", "form": "AuditLedgerAuditEventForm", "wizard": "AuditLedgerEventCaptureWizard"},
    {"operation": "record_access_evidence", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/access-evidence", "handler": "record_access_evidence", "permission": "audit_ledger.seal", "table": "audit_ledger_access_evidence", "form": "AuditLedgerAccessEvidenceForm", "wizard": "AuditLedgerEventCaptureWizard"},
    {"operation": "define_retention_policy", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/retention-policies", "handler": "define_retention_policy", "permission": "audit_ledger.configure", "table": "audit_ledger_retention_policy", "form": "AuditLedgerRetentionPolicyForm", "wizard": "AuditLedgerRetentionGovernanceWizard"},
    {"operation": "assert_control", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/control-assertions", "handler": "assert_control", "permission": "audit_ledger.audit", "table": "audit_ledger_control_assertion", "form": "AuditLedgerControlAssertionForm", "wizard": "AuditLedgerReleaseEvidenceWizard"},
    {"operation": "prepare_forensic_export", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/forensic-exports", "handler": "prepare_forensic_export", "permission": "audit_ledger.export", "table": "audit_ledger_forensic_export", "form": "AuditLedgerForensicExportForm", "wizard": "AuditLedgerForensicExportWizard"},
    {"operation": "verify_signature_chain", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/signature-chain/verify", "handler": "verify_signature_chain", "permission": "audit_ledger.verify", "table": "audit_ledger_signature_chain", "form": "AuditLedgerSignatureVerificationForm", "wizard": "AuditLedgerReleaseEvidenceWizard"},
    {"operation": "publish_audit_projection", "operation_kind": "command", "method": "POST", "path": "/app/audit-ledger/projections", "handler": "publish_audit_projection", "permission": "audit_ledger.publish", "table": "audit_ledger_projection_link", "form": "AuditLedgerProjectionForm", "wizard": "AuditLedgerReleaseEvidenceWizard"},
    {"operation": "build_workbench", "operation_kind": "query", "method": "GET", "path": "/app/audit-ledger/workbench", "handler": "build_workbench", "permission": "audit_ledger.read", "table": "audit_ledger_audit_event", "form": None, "wizard": None},
    {"operation": "ledger_summary", "operation_kind": "query", "method": "GET", "path": "/app/audit-ledger/summary", "handler": "ledger_summary", "permission": "audit_ledger.read", "table": "audit_ledger_audit_event", "form": None, "wizard": None},
    {"operation": "release_snapshot", "operation_kind": "query", "method": "GET", "path": "/app/audit-ledger/release-snapshot", "handler": "release_snapshot", "permission": "audit_ledger.read", "table": "audit_ledger_control_assertion", "form": None, "wizard": None},
)


def standalone_service_operation_contracts() -> dict:
    """Return the service operation surface for the standalone app."""
    return {
        "format": "appgen.audit-ledger-standalone-service-contract.v1",
        "ok": bool(STANDALONE_OPERATION_CONTRACTS),
        "pbc": "audit_ledger",
        "contracts": STANDALONE_OPERATION_CONTRACTS,
        "routes": tuple(f"{item['method']} {item['path']}" for item in STANDALONE_OPERATION_CONTRACTS),
        "tables": tuple(dict.fromkeys(item["table"] for item in STANDALONE_OPERATION_CONTRACTS)),
        "side_effects": (),
    }


class AuditLedgerStandaloneService:
    """Stateful service facade over the SQLite-backed standalone repository."""

    def __init__(self, repository: AuditLedgerRepository | None = None):
        self.repository = repository or AuditLedgerRepository()

    def close(self) -> None:
        self.repository.close()

    def standalone_service_manifest(self) -> dict:
        return standalone_service_operation_contracts()

    def _wrap(self, operation: str, result: dict) -> dict:
        contract = next(item for item in STANDALONE_OPERATION_CONTRACTS if item["operation"] == operation)
        return {
            "ok": result.get("ok") is True,
            "operation": operation,
            "operation_kind": contract["operation_kind"],
            "route": {"method": contract["method"], "path": contract["path"]},
            "permission": contract["permission"],
            "table": contract["table"],
            "form": contract["form"],
            "wizard": contract["wizard"],
            "result": result,
            "side_effects": (),
        }

    def configure_runtime(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("configure_runtime", self.repository.configure_runtime(supplied.get("configuration", supplied)))

    def set_parameter(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("set_parameter", self.repository.set_parameter(str(supplied.get("name", "")), supplied.get("value")))

    def register_rule(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("register_rule", self.repository.register_rule(dict(supplied.get("rule", supplied))))

    def receive_event(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap(
            "receive_event",
            self.repository.receive_event(
                dict(supplied.get("envelope", supplied)),
                simulate_failure=bool(supplied.get("simulate_failure", False)),
            ),
        )

    def record_audit_event(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("record_audit_event", self.repository.record_audit_event(dict(supplied.get("audit_event", supplied))))

    def record_access_evidence(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("record_access_evidence", self.repository.record_access_evidence(dict(supplied.get("evidence", supplied))))

    def define_retention_policy(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("define_retention_policy", self.repository.define_retention_policy(dict(supplied.get("policy", supplied))))

    def assert_control(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("assert_control", self.repository.assert_control(dict(supplied.get("assertion", supplied))))

    def prepare_forensic_export(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("prepare_forensic_export", self.repository.prepare_forensic_export(dict(supplied.get("export", supplied))))

    def verify_signature_chain(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("verify_signature_chain", self.repository.verify_signature_chain(tenant=str(supplied.get("tenant", ""))))

    def publish_audit_projection(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap(
            "publish_audit_projection",
            self.repository.publish_audit_projection(
                str(supplied.get("audit_id", "")),
                systems=tuple(supplied.get("systems", ())),
            ),
        )

    def build_workbench(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("build_workbench", self.repository.build_workbench(tenant=str(supplied.get("tenant", ""))))

    def ledger_summary(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("ledger_summary", self.repository.ledger_summary(tenant=str(supplied.get("tenant", ""))))

    def release_snapshot(self, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        return self._wrap("release_snapshot", self.repository.release_snapshot(tenant=str(supplied.get("tenant", ""))))


def smoke_test() -> dict:
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = AuditLedgerService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }


def standalone_service_smoke_test() -> dict:
    service = AuditLedgerStandaloneService()
    try:
        configured = service.configure_runtime(
            {
                "configuration": {
                    "database_backend": "postgresql",
                    "event_topic": "appgen.audit.events",
                    "retry_limit": 3,
                    "signature_algorithm": "dilithium3_simulated",
                    "allowed_classifications": ("public", "internal", "regulated"),
                    "export_modes": ("proof_bundle",),
                    "default_timezone": "UTC",
                    "workbench_limit": 100,
                }
            }
        )
        event = service.record_audit_event(
            {
                "audit_event": {
                    "audit_id": "audit_service",
                    "tenant": "tenant_service",
                    "source_pbc": "workflow_orchestration",
                    "aggregate_id": "wf_service",
                    "actor": "operator",
                    "action": "complete_workflow",
                    "classification": "regulated",
                    "payload": {"workflow_id": "wf_service"},
                }
            }
        )
        summary = service.ledger_summary({"tenant": "tenant_service"})
        return {
            "ok": configured["ok"] and event["ok"] and summary["ok"],
            "service_contract": standalone_service_operation_contracts(),
            "configured": configured,
            "event": event,
            "summary": summary,
            "side_effects": (),
        }
    finally:
        service.close()
