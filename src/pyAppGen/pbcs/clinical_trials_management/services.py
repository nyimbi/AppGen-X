"""Command and query service layer for the clinical_trials_management PBC."""

from __future__ import annotations

from .agent import clinical_trials_management_assistant_preview
from .controls import clinical_trials_management_control_center
from .events import EVENT_CONTRACT
from .forms import clinical_trials_management_form_catalog
from .runtime import clinical_trials_management_build_workbench_view
from .runtime import clinical_trials_management_runtime_smoke
from .wizards import clinical_trials_management_wizard_catalog


OPERATION_CONTRACTS = (
    {
        "operation": "command_trial_protocols",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/trial-protocols",
        "permission": "clinical_trials_management.protocol_admin",
        "owned_tables": ("clinical_trials_management_trial_protocol",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialProtocolRegistered",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_study_sites",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/study-sites",
        "permission": "clinical_trials_management.site_activation",
        "owned_tables": ("clinical_trials_management_study_site",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialSiteActivated",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_subjects",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/subjects",
        "permission": "clinical_trials_management.subject_enrollment",
        "owned_tables": ("clinical_trials_management_subject",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialSubjectEnrollmentReviewed",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_consent_records",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/consent-records",
        "permission": "clinical_trials_management.consent_manage",
        "owned_tables": ("clinical_trials_management_consent_record",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialConsentRecorded",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_visit_schedules",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/visit-schedules",
        "permission": "clinical_trials_management.visit_manage",
        "owned_tables": ("clinical_trials_management_visit_schedule",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialVisitScheduled",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_adverse_events",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/adverse-events",
        "permission": "clinical_trials_management.safety_review",
        "owned_tables": ("clinical_trials_management_adverse_event",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialSeriousAdverseEventReported",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_monitoring_findings",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/monitoring-findings",
        "permission": "clinical_trials_management.monitoring_manage",
        "owned_tables": ("clinical_trials_management_monitoring_finding",),
        "read_tables": (),
        "emitted_event": "ClinicalTrialMonitoringFindingOpened",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_policy_rules",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/policy-rules",
        "permission": "clinical_trials_management.configure",
        "owned_tables": ("clinical_trials_management_clinical_trials_management_policy_rule",),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "command_runtime_parameters",
        "operation_kind": "command",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/runtime-parameters",
        "permission": "clinical_trials_management.configure",
        "owned_tables": ("clinical_trials_management_clinical_trials_management_runtime_parameter",),
        "read_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_clinical_trials_management_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/clinical_trials_management/clinical-trials-workbench",
        "permission": "clinical_trials_management.read",
        "owned_tables": (),
        "read_tables": (
            "clinical_trials_management_trial_protocol",
            "clinical_trials_management_study_site",
            "clinical_trials_management_subject",
            "clinical_trials_management_visit_schedule",
            "clinical_trials_management_adverse_event",
            "clinical_trials_management_monitoring_finding",
        ),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_clinical_trials_management_controls",
        "operation_kind": "query",
        "method": "GET",
        "path": "/api/pbc/clinical_trials_management/controls",
        "permission": "clinical_trials_management.audit",
        "owned_tables": (),
        "read_tables": (
            "clinical_trials_management_clinical_trials_management_control_assertion",
            "clinical_trials_management_adverse_event",
            "clinical_trials_management_monitoring_finding",
            "clinical_trials_management_appgen_dead_letter_event",
        ),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
        "event_contract": "AppGen-X",
    },
    {
        "operation": "query_clinical_trials_management_assistant_preview",
        "operation_kind": "query",
        "method": "POST",
        "path": "/api/pbc/clinical_trials_management/assistant/document-preview",
        "permission": "clinical_trials_management.audit",
        "owned_tables": (),
        "read_tables": (
            "clinical_trials_management_trial_protocol",
            "clinical_trials_management_study_site",
            "clinical_trials_management_subject",
            "clinical_trials_management_consent_record",
            "clinical_trials_management_visit_schedule",
            "clinical_trials_management_adverse_event",
            "clinical_trials_management_monitoring_finding",
            "clinical_trials_management_clinical_trials_management_policy_rule",
            "clinical_trials_management_clinical_trials_management_runtime_parameter",
        ),
        "emitted_event": None,
        "transaction_boundary": "read_only_projection",
        "event_contract": "AppGen-X",
    },
)


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item["operation"] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": "clinical_trials_management",
        "operations": operations,
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
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
        "pbc": "clinical_trials_management",
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


class ClinicalTrialsManagementService:
    """Side-effect-free package-local service facade."""

    def _execute(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "clinical_trials_management",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
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
        else:
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        return result

    def command_trial_protocols(self, payload: dict | None = None) -> dict:
        return self._execute("command_trial_protocols", payload or {})

    def command_study_sites(self, payload: dict | None = None) -> dict:
        return self._execute("command_study_sites", payload or {})

    def command_subjects(self, payload: dict | None = None) -> dict:
        return self._execute("command_subjects", payload or {})

    def command_consent_records(self, payload: dict | None = None) -> dict:
        return self._execute("command_consent_records", payload or {})

    def command_visit_schedules(self, payload: dict | None = None) -> dict:
        return self._execute("command_visit_schedules", payload or {})

    def command_adverse_events(self, payload: dict | None = None) -> dict:
        return self._execute("command_adverse_events", payload or {})

    def command_monitoring_findings(self, payload: dict | None = None) -> dict:
        return self._execute("command_monitoring_findings", payload or {})

    def command_policy_rules(self, payload: dict | None = None) -> dict:
        return self._execute("command_policy_rules", payload or {})

    def command_runtime_parameters(self, payload: dict | None = None) -> dict:
        return self._execute("command_runtime_parameters", payload or {})

    def query_clinical_trials_management_workbench(self, payload: dict | None = None) -> dict:
        base = self._execute("query_clinical_trials_management_workbench", payload or {})
        workbench = clinical_trials_management_build_workbench_view("tenant-smoke", clinical_trials_management_runtime_smoke()["state"])
        return {
            **base,
            "workbench": workbench,
            "app_surface": {
                "form_count": len(clinical_trials_management_form_catalog()["forms"]),
                "wizard_count": len(clinical_trials_management_wizard_catalog()["wizards"]),
            },
        }

    def query_clinical_trials_management_controls(self, payload: dict | None = None) -> dict:
        base = self._execute("query_clinical_trials_management_controls", payload or {})
        control_center = clinical_trials_management_control_center()
        return {
            **base,
            "control_center": {
                "ok": control_center["ok"],
                "lock_readiness": control_center["lock_readiness"],
                "assistant_guardrails": control_center["assistant_guardrails"],
            },
        }

    def query_clinical_trials_management_assistant_preview(self, payload: dict | None = None) -> dict:
        base = self._execute("query_clinical_trials_management_assistant_preview", payload or {})
        preview = clinical_trials_management_assistant_preview(payload or {})
        return {**base, "preview": preview}


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    service = ClinicalTrialsManagementService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith("command_") or name.startswith("query_")) and callable(getattr(service, name))
    )
    return {
        "ok": bool(operations) and service_operation_contracts()["ok"],
        "pbc": "clinical_trials_management",
        "service_class": service.__class__.__name__,
        "operations": operations,
        "command_operations": service_operation_contracts()["command_operations"],
        "query_operations": service_operation_contracts()["query_operations"],
        "operation_contracts": service_operation_contracts()["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ClinicalTrialsManagementService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = getattr(service, operation)({"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }
