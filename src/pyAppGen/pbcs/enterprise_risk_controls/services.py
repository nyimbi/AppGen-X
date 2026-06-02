"""Command and query service layer for the enterprise_risk_controls PBC."""

from __future__ import annotations

from .agent import enterprise_risk_controls_assistant_preview
from .controls import enterprise_risk_controls_control_center
from .events import EVENT_CONTRACT
from .forms import enterprise_risk_controls_form_catalog
from .wizards import enterprise_risk_controls_wizard_catalog

OPERATION_CONTRACTS = (
    {
        "operation": "register_risk",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/risks",
        "permission": "enterprise_risk_controls.register_risk",
        "owned_tables": (
            "enterprise_risk_controls_risk_register",
            "enterprise_risk_controls_risk_taxonomy",
        ),
        "read_tables": (),
        "emitted_event": "RiskRegistered",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "assess_inherent_risk",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/risk-assessments",
        "permission": "enterprise_risk_controls.assess_risk",
        "owned_tables": (
            "enterprise_risk_controls_risk_assessment",
            "enterprise_risk_controls_risk_indicator_observation",
        ),
        "read_tables": (),
        "emitted_event": "RiskAssessed",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "define_control",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/controls",
        "permission": "enterprise_risk_controls.manage_controls",
        "owned_tables": (
            "enterprise_risk_controls_control_library",
            "enterprise_risk_controls_control_objective",
        ),
        "read_tables": (),
        "emitted_event": "ControlDefined",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "schedule_control_test",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/control-tests",
        "permission": "enterprise_risk_controls.manage_controls",
        "owned_tables": (
            "enterprise_risk_controls_control_test",
            "enterprise_risk_controls_control_test_evidence",
        ),
        "read_tables": (),
        "emitted_event": "ControlTestScheduled",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "record_attestation",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/attestations",
        "permission": "enterprise_risk_controls.attest_controls",
        "owned_tables": (
            "enterprise_risk_controls_control_attestation",
            "enterprise_risk_controls_control_owner_assignment",
        ),
        "read_tables": (),
        "emitted_event": "ControlAttested",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "open_remediation",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/remediations",
        "permission": "enterprise_risk_controls.manage_remediation",
        "owned_tables": (
            "enterprise_risk_controls_remediation_issue",
            "enterprise_risk_controls_remediation_action",
        ),
        "read_tables": (),
        "emitted_event": "RemediationOpened",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "generate_assurance_packet",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/assurance-packets",
        "permission": "enterprise_risk_controls.compile_assurance",
        "owned_tables": (
            "enterprise_risk_controls_audit_evidence_packet",
            "enterprise_risk_controls_risk_committee_packet",
        ),
        "read_tables": (),
        "emitted_event": "AssurancePacketGenerated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_enterprise_risk_controls_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/enterprise_risk_controls/workbench",
        "permission": "enterprise_risk_controls.read",
        "owned_tables": (),
        "read_tables": (
            "enterprise_risk_controls_risk_register",
            "enterprise_risk_controls_risk_assessment",
            "enterprise_risk_controls_control_library",
            "enterprise_risk_controls_remediation_issue",
            "enterprise_risk_controls_audit_evidence_packet",
            "enterprise_risk_controls_appgen_inbox_event",
            "enterprise_risk_controls_appgen_outbox_event",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_enterprise_risk_controls_controls",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/enterprise_risk_controls/controls",
        "permission": "enterprise_risk_controls.audit",
        "owned_tables": (),
        "read_tables": (
            "enterprise_risk_controls_control_exception",
            "enterprise_risk_controls_risk_indicator_observation",
            "enterprise_risk_controls_risk_appetite_statement",
            "enterprise_risk_controls_audit_evidence_packet",
            "enterprise_risk_controls_appgen_dead_letter_event",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_enterprise_risk_controls_assistant_preview",
        "operation_kind": "query",
        "method": "POST",
        "path": "/api/pbc/enterprise_risk_controls/assistant/document-preview",
        "permission": "enterprise_risk_controls.audit",
        "owned_tables": (),
        "read_tables": (
            "enterprise_risk_controls_risk_policy_rule",
            "enterprise_risk_controls_risk_runtime_parameter",
            "enterprise_risk_controls_risk_schema_extension",
            "enterprise_risk_controls_risk_register",
            "enterprise_risk_controls_control_library",
            "enterprise_risk_controls_remediation_issue",
        ),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
)


def service_operation_contracts() -> dict:
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["emitted_event"] for item in command_contracts)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["emitted_event"] is None for item in query_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "enterprise_risk_controls",
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "enterprise_risk_controls",
        "service_class": "EnterpriseRiskControlsService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": "enterprise_risk_controls",
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
        "side_effects": (),
    }


class EnterpriseRiskControlsService:
    """Side-effect-free package-local service facade."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        result = {
            "ok": plan.get("ok") is True,
            "pbc": "enterprise_risk_controls",
            "operation": operation_name,
            "operation_kind": plan.get("operation_kind"),
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
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
        else:
            result.update(
                {
                    "query": operation_name,
                    "read_only": True,
                    "outbox_table": None,
                    "emits": (),
                }
            )
        return result

    def register_risk(self, payload: dict | None = None) -> dict:
        return self._execute("register_risk", payload or {})

    def assess_inherent_risk(self, payload: dict | None = None) -> dict:
        return self._execute("assess_inherent_risk", payload or {})

    def define_control(self, payload: dict | None = None) -> dict:
        return self._execute("define_control", payload or {})

    def schedule_control_test(self, payload: dict | None = None) -> dict:
        return self._execute("schedule_control_test", payload or {})

    def record_attestation(self, payload: dict | None = None) -> dict:
        return self._execute("record_attestation", payload or {})

    def open_remediation(self, payload: dict | None = None) -> dict:
        return self._execute("open_remediation", payload or {})

    def generate_assurance_packet(self, payload: dict | None = None) -> dict:
        return self._execute("generate_assurance_packet", payload or {})

    def query_enterprise_risk_controls_workbench(self, payload: dict | None = None) -> dict:
        base = self._execute("query_enterprise_risk_controls_workbench", payload or {})
        return {
            **base,
            "app_surface": {
                "form_count": len(enterprise_risk_controls_form_catalog()["forms"]),
                "wizard_count": len(enterprise_risk_controls_wizard_catalog()["wizards"]),
            },
        }

    def query_enterprise_risk_controls_controls(self, payload: dict | None = None) -> dict:
        base = self._execute("query_enterprise_risk_controls_controls", payload or {})
        return {**base, "control_center": enterprise_risk_controls_control_center()}

    def query_enterprise_risk_controls_assistant_preview(self, payload: dict | None = None) -> dict:
        base = self._execute("query_enterprise_risk_controls_assistant_preview", payload or {})
        return {**base, "assistant_preview": enterprise_risk_controls_assistant_preview(payload or {})}


def smoke_test():
    service = EnterpriseRiskControlsService()
    command = service.register_risk({"tenant": "tenant-smoke", "risk_code": "RISK-001"})
    query = service.query_enterprise_risk_controls_workbench({"tenant": "tenant-smoke"})
    preview = service.query_enterprise_risk_controls_assistant_preview(
        {
            "document_text": "Critical issues need a 30-day remediation SLA.",
            "instructions": "Update the remediation parameter to 30 days.",
            "target_entity": "risk_runtime_parameter",
            "requested_action": "update",
        }
    )
    return {
        "ok": command["ok"] and query["ok"] and preview["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "preview": preview,
        "side_effects": (),
    }
