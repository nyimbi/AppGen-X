"""Standalone one-PBC app composition for the medical_device_lifecycle package."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import hashlib

from .controls import medical_device_lifecycle_control_catalog
from .forms import medical_device_lifecycle_form_catalog
from .runtime import MEDICAL_DEVICE_LIFECYCLE_REQUIRED_EVENT_TOPIC
from .runtime import medical_device_lifecycle_verify_owned_table_boundary
from .wizards import medical_device_lifecycle_wizard_catalog

PBC_KEY = "medical_device_lifecycle"


STANDALONE_ROUTE_CONTRACTS = (
    {
        "operation": "register_device",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/devices",
        "handler": "register_device",
        "permission": "medical_device_lifecycle.create",
        "table": "medical_device_lifecycle_medical_device",
        "form": "medical_device_registry_intake",
        "wizard": "device_onboarding_and_qualification",
    },
    {
        "operation": "assign_device",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/assignments",
        "handler": "assign_device",
        "permission": "medical_device_lifecycle.update",
        "table": "medical_device_lifecycle_device_assignment",
        "form": "device_assignment_governance",
        "wizard": "point_of_care_assignment",
    },
    {
        "operation": "record_calibration",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/calibrations",
        "handler": "record_calibration",
        "permission": "medical_device_lifecycle.approve",
        "table": "medical_device_lifecycle_calibration",
        "form": "calibration_review",
        "wizard": "calibration_and_return_to_service",
    },
    {
        "operation": "record_maintenance",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/maintenance-events",
        "handler": "record_maintenance",
        "permission": "medical_device_lifecycle.approve",
        "table": "medical_device_lifecycle_maintenance_event",
        "form": "maintenance_return_to_service",
        "wizard": "calibration_and_return_to_service",
    },
    {
        "operation": "launch_recall",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/recalls",
        "handler": "launch_recall",
        "permission": "medical_device_lifecycle.admin",
        "table": "medical_device_lifecycle_recall_notice",
        "form": "recall_containment",
        "wizard": "recall_containment_and_notification",
    },
    {
        "operation": "record_usage_trace",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/usage-traces",
        "handler": "record_usage_trace",
        "permission": "medical_device_lifecycle.update",
        "table": "medical_device_lifecycle_usage_trace",
        "form": "usage_trace_capture",
        "wizard": "point_of_care_assignment",
    },
    {
        "operation": "attach_regulatory_evidence",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/regulatory-evidence",
        "handler": "attach_regulatory_evidence",
        "permission": "medical_device_lifecycle.approve",
        "table": "medical_device_lifecycle_regulatory_evidence",
        "form": "regulatory_evidence_packet",
        "wizard": "recall_containment_and_notification",
    },
    {
        "operation": "upsert_policy_rule",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/policy-rules",
        "handler": "upsert_policy_rule",
        "permission": "medical_device_lifecycle.admin",
        "table": "medical_device_lifecycle_medical_device_lifecycle_policy_rule",
        "form": "policy_rule_editor",
        "wizard": "device_onboarding_and_qualification",
    },
    {
        "operation": "update_runtime_parameter",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/runtime-parameters",
        "handler": "update_runtime_parameter",
        "permission": "medical_device_lifecycle.admin",
        "table": "medical_device_lifecycle_medical_device_lifecycle_runtime_parameter",
        "form": "runtime_parameter_editor",
        "wizard": "device_onboarding_and_qualification",
    },
    {
        "operation": "preview_document_change",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/medical-device-lifecycle/assistant/document-preview",
        "handler": "preview_document_change",
        "permission": "medical_device_lifecycle.read",
        "table": "medical_device_lifecycle_regulatory_evidence",
        "form": "assistant_document_intake",
        "wizard": "assistant_change_preview",
    },
    {
        "operation": "get_device",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/medical-device-lifecycle/devices/detail",
        "handler": "get_device",
        "permission": "medical_device_lifecycle.read",
        "table": "medical_device_lifecycle_medical_device",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/medical-device-lifecycle/workbench",
        "handler": "build_workbench",
        "permission": "medical_device_lifecycle.read",
        "table": "medical_device_lifecycle_medical_device",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "build_control_center",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/medical-device-lifecycle/controls",
        "handler": "build_control_center",
        "permission": "medical_device_lifecycle.read",
        "table": "medical_device_lifecycle_medical_device_lifecycle_control_assertion",
        "form": None,
        "wizard": None,
    },
)


def standalone_route_contracts() -> dict:
    """Return executable standalone-app routes for the one-PBC package slice."""
    contracts = tuple({**item, "route_id": f"{item['method']} {item['path']}"} for item in STANDALONE_ROUTE_CONTRACTS)
    return {
        "format": "appgen.medical-device-lifecycle-standalone-route-contract.v1",
        "ok": bool(contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _today() -> str:
    return date.today().isoformat()


def _is_due(due_at: str | None, today: str | None = None) -> bool:
    if not due_at:
        return False
    return str(due_at) <= str(today or _today())


def _empty_state() -> dict:
    return {
        "devices": {},
        "assignments": {},
        "calibrations": {},
        "maintenance_events": {},
        "recall_notices": {},
        "usage_traces": {},
        "regulatory_evidence": {},
        "policy_rules": {},
        "runtime_parameters": {
            "quality_score_floor": 0.9,
            "materiality_threshold": 0.8,
            "approval_sla_hours": 24,
            "risk_threshold": 0.75,
            "forecast_horizon_days": 30,
            "workbench_limit": 50,
        },
        "control_assertions": {},
        "governed_models": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "handled_events": set(),
    }


class MedicalDeviceLifecycleStandaloneApp:
    """Mutable package-local standalone app for medical device lifecycle operations."""

    def __init__(self, state: dict | None = None):
        self.state = deepcopy(state) if state is not None else _empty_state()
        self.state["handled_events"] = set(self.state.get("handled_events", set()))

    def close(self) -> None:
        """No-op close hook for API symmetry with persistent standalone stores."""

    def _emit(self, event_type: str, payload: dict) -> None:
        self.state["outbox"].append(
            {
                "event_type": event_type,
                "topic": MEDICAL_DEVICE_LIFECYCLE_REQUIRED_EVENT_TOPIC,
                "payload": dict(payload),
                "idempotency_key": _digest((event_type, payload)),
            }
        )

    def _device(self, device_id: str) -> dict | None:
        return self.state["devices"].get(device_id)

    def _required_documents(self, device: dict) -> tuple[str, ...]:
        required = ["manual", "service_record", "calibration_certificate"]
        if device.get("active_recall"):
            required.append("recall_letter")
        return tuple(required)

    def _document_types_for_device(self, device_id: str) -> set[str]:
        return {
            item["document_type"]
            for item in self.state["regulatory_evidence"].values()
            if item["device_id"] == device_id and item.get("approved")
        }

    def _assignment_blockers(self, device: dict, payload: dict) -> tuple[str, ...]:
        blockers = []
        today = payload.get("today") or _today()
        if device.get("qualification_status") != "qualified":
            blockers.append("device_not_qualified")
        if device.get("current_state") in {"quarantined", "maintenance", "retired", "disposed", "recall_hold"}:
            blockers.append(f"state_{device.get('current_state')}")
        if device.get("active_recall"):
            blockers.append("active_recall")
        if device.get("open_assignment_id"):
            blockers.append("already_assigned")
        if _is_due(device.get("calibration_due_at"), today):
            blockers.append("calibration_overdue")
        if _is_due(device.get("maintenance_due_at"), today):
            blockers.append("maintenance_due")
        if payload.get("assignment_type") == "patient" and device.get("implantable") and not payload.get("procedure_ref"):
            blockers.append("implant_requires_procedure_ref")
        return tuple(blockers)

    def register_device(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        device_id = payload.get("device_id")
        if not device_id:
            return {"ok": False, "reason": "device_id_required", "side_effects": ()}
        device = {
            "device_id": device_id,
            "tenant": payload.get("tenant", "default"),
            "udi": payload.get("udi", device_id),
            "manufacturer": payload.get("manufacturer", "unknown"),
            "model": payload.get("model", "unknown-model"),
            "serial_number": payload.get("serial_number", device_id),
            "lot_number": payload.get("lot_number"),
            "firmware_version": payload.get("firmware_version"),
            "risk_class": payload.get("risk_class", "II"),
            "implantable": bool(payload.get("implantable", False)),
            "department": payload.get("department", "biomed"),
            "location": payload.get("location", "warehouse"),
            "qualification_status": payload.get("qualification_status", "qualified"),
            "current_state": payload.get(
                "current_state",
                "available" if payload.get("qualification_status", "qualified") == "qualified" else "qualification_hold",
            ),
            "calibration_due_at": payload.get("calibration_due_at"),
            "maintenance_due_at": payload.get("maintenance_due_at"),
            "active_recall": False,
            "open_assignment_id": None,
            "usage_count": int(payload.get("usage_count", 0)),
            "last_used_at": payload.get("last_used_at"),
        }
        self.state["devices"][device_id] = device
        self._emit("MedicalDeviceLifecycleCreated", {"device_id": device_id, "tenant": device["tenant"]})
        return {"ok": True, "result": device, "side_effects": ()}

    def assign_device(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        device = self._device(payload.get("device_id", ""))
        if device is None:
            return {"ok": False, "reason": "device_not_found", "side_effects": ()}
        blockers = self._assignment_blockers(device, payload)
        if blockers:
            return {
                "ok": False,
                "reason": "assignment_blocked",
                "device_id": device["device_id"],
                "blocked_by": blockers,
                "side_effects": (),
            }
        assignment_id = payload.get("assignment_id") or f"{device['device_id']}-assignment"
        assignment = {
            "assignment_id": assignment_id,
            "tenant": payload.get("tenant", device["tenant"]),
            "device_id": device["device_id"],
            "assignment_type": payload.get("assignment_type", "department"),
            "assignee_ref": payload.get("assignee_ref", device.get("department")),
            "responsible_role": payload.get("responsible_role", "biomed"),
            "privacy_scope": payload.get("privacy_scope", "operational"),
            "intended_use": payload.get("intended_use"),
            "procedure_ref": payload.get("procedure_ref"),
            "status": "active",
            "started_at": payload.get("started_at", _today()),
        }
        self.state["assignments"][assignment_id] = assignment
        device["open_assignment_id"] = assignment_id
        device["current_state"] = "assigned"
        device["location"] = payload.get("location", device["location"])
        self._emit("MedicalDeviceLifecycleUpdated", {"device_id": device["device_id"], "assignment_id": assignment_id})
        return {"ok": True, "result": assignment, "side_effects": ()}

    def record_calibration(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        device = self._device(payload.get("device_id", ""))
        if device is None:
            return {"ok": False, "reason": "device_not_found", "side_effects": ()}
        calibration_id = payload.get("calibration_id") or f"{device['device_id']}-calibration"
        record = {
            "calibration_id": calibration_id,
            "tenant": payload.get("tenant", device["tenant"]),
            "device_id": device["device_id"],
            "completed_at": payload.get("completed_at", _today()),
            "outcome": payload.get("outcome", "pass"),
            "technician": payload.get("technician", "tech"),
            "standard_used": payload.get("standard_used", "reference-standard"),
            "next_due_at": payload.get("next_due_at"),
            "impact_summary": payload.get("impact_summary"),
        }
        self.state["calibrations"][calibration_id] = record
        device["calibration_due_at"] = record["next_due_at"]
        if record["outcome"] == "pass":
            if device.get("active_recall"):
                device["current_state"] = "recall_hold"
            elif device.get("open_assignment_id"):
                device["current_state"] = "assigned"
            else:
                device["current_state"] = "available"
            event_type = "MedicalDeviceLifecycleApproved"
        else:
            device["current_state"] = "quarantined"
            event_type = "MedicalDeviceLifecycleExceptionOpened"
        self._emit(event_type, {"device_id": device["device_id"], "calibration_id": calibration_id})
        return {"ok": True, "result": record, "side_effects": ()}

    def record_maintenance(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        device = self._device(payload.get("device_id", ""))
        if device is None:
            return {"ok": False, "reason": "device_not_found", "side_effects": ()}
        maintenance_id = payload.get("maintenance_id") or f"{device['device_id']}-maintenance"
        record = {
            "maintenance_id": maintenance_id,
            "tenant": payload.get("tenant", device["tenant"]),
            "device_id": device["device_id"],
            "failure_mode": payload.get("failure_mode", "preventive"),
            "severity": payload.get("severity", "medium"),
            "qualification_result": payload.get("qualification_result", "pass"),
            "resolved_status": payload.get("resolved_status", "returned_to_service"),
            "vendor": payload.get("vendor"),
            "next_due_at": payload.get("next_due_at"),
        }
        self.state["maintenance_events"][maintenance_id] = record
        device["maintenance_due_at"] = record["next_due_at"]
        if record["qualification_result"] == "pass" and record["resolved_status"] in {"complete", "returned_to_service"}:
            device["current_state"] = "recall_hold" if device.get("active_recall") else "available"
            event_type = "MedicalDeviceLifecycleApproved"
        else:
            device["current_state"] = "maintenance"
            event_type = "MedicalDeviceLifecycleExceptionOpened"
        self._emit(event_type, {"device_id": device["device_id"], "maintenance_id": maintenance_id})
        return {"ok": True, "result": record, "side_effects": ()}

    def launch_recall(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        recall_id = payload.get("recall_id") or "recall-1"
        tenant = payload.get("tenant", "default")
        explicit_ids = set(payload.get("device_ids") or ())
        matched_devices = []
        for device in self.state["devices"].values():
            if device["tenant"] != tenant:
                continue
            if explicit_ids and device["device_id"] in explicit_ids:
                matched_devices.append(device)
                continue
            if payload.get("model") and device.get("model") == payload["model"]:
                matched_devices.append(device)
                continue
            if payload.get("lot_number") and device.get("lot_number") == payload["lot_number"]:
                matched_devices.append(device)
                continue
            if payload.get("firmware_version") and device.get("firmware_version") == payload["firmware_version"]:
                matched_devices.append(device)
        recall = {
            "recall_id": recall_id,
            "tenant": tenant,
            "manufacturer_notice": payload.get("manufacturer_notice", "notice"),
            "recall_class": payload.get("recall_class", "II"),
            "required_action": payload.get("required_action", "quarantine"),
            "deadline": payload.get("deadline"),
            "matched_device_ids": tuple(device["device_id"] for device in matched_devices),
            "status": "open",
        }
        self.state["recall_notices"][recall_id] = recall
        for device in matched_devices:
            device["active_recall"] = True
            device["current_state"] = "recall_hold"
        self._emit("MedicalDeviceLifecycleExceptionOpened", {"recall_id": recall_id, "matched_device_count": len(matched_devices)})
        return {"ok": True, "result": recall, "side_effects": ()}

    def record_usage_trace(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        device = self._device(payload.get("device_id", ""))
        if device is None:
            return {"ok": False, "reason": "device_not_found", "side_effects": ()}
        if device.get("active_recall") or _is_due(device.get("calibration_due_at"), payload.get("today")):
            return {
                "ok": False,
                "reason": "device_not_ready_for_use",
                "device_id": device["device_id"],
                "current_state": device.get("current_state"),
                "side_effects": (),
            }
        usage_id = payload.get("usage_id") or f"{device['device_id']}-usage"
        record = {
            "usage_id": usage_id,
            "tenant": payload.get("tenant", device["tenant"]),
            "device_id": device["device_id"],
            "assignment_id": payload.get("assignment_id", device.get("open_assignment_id")),
            "operator_ref": payload.get("operator_ref", "operator"),
            "location": payload.get("location", device["location"]),
            "procedure_ref": payload.get("procedure_ref"),
            "started_at": payload.get("started_at", f"{_today()}T08:00:00"),
            "ended_at": payload.get("ended_at"),
            "event_type": payload.get("event_type", "in_use"),
        }
        self.state["usage_traces"][usage_id] = record
        device["usage_count"] = int(device.get("usage_count", 0)) + 1
        device["last_used_at"] = record["started_at"]
        self._emit("MedicalDeviceLifecycleUpdated", {"device_id": device["device_id"], "usage_id": usage_id})
        return {"ok": True, "result": record, "side_effects": ()}

    def attach_regulatory_evidence(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        evidence_id = payload.get("evidence_id")
        device_id = payload.get("device_id")
        if not evidence_id or not device_id:
            return {"ok": False, "reason": "evidence_id_and_device_id_required", "side_effects": ()}
        if self._device(device_id) is None:
            return {"ok": False, "reason": "device_not_found", "side_effects": ()}
        record = {
            "evidence_id": evidence_id,
            "tenant": payload.get("tenant", "default"),
            "device_id": device_id,
            "document_type": payload.get("document_type", "service_record"),
            "effective_date": payload.get("effective_date"),
            "retention_class": payload.get("retention_class", "regulated"),
            "checksum": payload.get("checksum", _digest((evidence_id, device_id))),
            "approved": bool(payload.get("approved", True)),
        }
        self.state["regulatory_evidence"][evidence_id] = record
        self._emit("MedicalDeviceLifecycleApproved", {"device_id": device_id, "evidence_id": evidence_id})
        return {"ok": True, "result": record, "side_effects": ()}

    def upsert_policy_rule(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        rule_id = payload.get("rule_id")
        if not rule_id:
            return {"ok": False, "reason": "rule_id_required", "side_effects": ()}
        record = {
            "tenant": payload.get("tenant", "default"),
            "rule_id": rule_id,
            "rule_type": payload.get("rule_type", "assignment"),
            "condition": payload.get("condition", "device must be qualified"),
            "status": payload.get("status", "active"),
        }
        self.state["policy_rules"][rule_id] = record
        return {"ok": True, "result": record, "side_effects": ()}

    def update_runtime_parameter(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        name = payload.get("name")
        if not name:
            return {"ok": False, "reason": "parameter_name_required", "side_effects": ()}
        record = {
            "tenant": payload.get("tenant", "default"),
            "name": name,
            "value": payload.get("value"),
        }
        self.state["runtime_parameters"][name] = record["value"]
        return {"ok": True, "result": record, "side_effects": ()}

    def get_device(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        device = self._device(payload.get("device_id", ""))
        if device is None:
            return {"ok": False, "reason": "device_not_found", "side_effects": ()}
        assignments = tuple(item for item in self.state["assignments"].values() if item["device_id"] == device["device_id"])
        calibrations = tuple(item for item in self.state["calibrations"].values() if item["device_id"] == device["device_id"])
        maintenance = tuple(item for item in self.state["maintenance_events"].values() if item["device_id"] == device["device_id"])
        evidence = tuple(item for item in self.state["regulatory_evidence"].values() if item["device_id"] == device["device_id"])
        return {
            "ok": True,
            "result": {
                "device": device,
                "assignments": assignments,
                "calibrations": calibrations,
                "maintenance_events": maintenance,
                "regulatory_evidence": evidence,
            },
            "side_effects": (),
        }

    def build_workbench(self, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        tenant = payload.get("tenant", "default")
        today = payload.get("today") or _today()
        devices = tuple(item for item in self.state["devices"].values() if item["tenant"] == tenant)
        assignments = tuple(item for item in self.state["assignments"].values() if item["tenant"] == tenant and item["status"] == "active")
        calibration_due = tuple(item["device_id"] for item in devices if _is_due(item.get("calibration_due_at"), today))
        maintenance_due = tuple(item["device_id"] for item in devices if _is_due(item.get("maintenance_due_at"), today))
        recall_hold = tuple(item["device_id"] for item in devices if item.get("active_recall"))
        missing_evidence = tuple(
            item["device_id"]
            for item in devices
            if not set(self._required_documents(item)).issubset(self._document_types_for_device(item["device_id"]))
        )
        available = tuple(
            item["device_id"]
            for item in devices
            if item.get("current_state") == "available" and item["device_id"] not in recall_hold
        )
        return {
            "ok": True,
            "tenant": tenant,
            "device_count": len(devices),
            "available_device_count": len(available),
            "open_assignment_count": len(assignments),
            "calibration_due_count": len(calibration_due),
            "maintenance_due_count": len(maintenance_due),
            "recall_hold_count": len(recall_hold),
            "missing_evidence_count": len(missing_evidence),
            "outbox_count": len(self.state["outbox"]),
            "queues": {
                "calibration_due": calibration_due,
                "maintenance_due": maintenance_due,
                "recall_hold": recall_hold,
                "missing_evidence": missing_evidence,
            },
            "devices": tuple(
                {
                    "device_id": item["device_id"],
                    "state": item["current_state"],
                    "location": item["location"],
                    "department": item["department"],
                    "risk_class": item["risk_class"],
                    "active_recall": item["active_recall"],
                }
                for item in devices[: int(self.state["runtime_parameters"].get("workbench_limit", 50))]
            ),
            "side_effects": (),
        }

    def build_control_center(self, payload: dict | None = None) -> dict:
        from .controls import medical_device_lifecycle_control_center

        summary = self.build_workbench(payload)
        return {
            "ok": True,
            "result": medical_device_lifecycle_control_center(summary),
            "side_effects": (),
        }

    def preview_document_change(self, payload: dict | None = None) -> dict:
        from .agent import datastore_crud_plan, document_instruction_plan

        payload = dict(payload or {})
        plan = document_instruction_plan(payload.get("document_text"), payload.get("instructions"))
        preview_action = payload.get("action", "update")
        target_table = payload.get("target_hint") or (plan.get("candidate_tables") or ("medical_device_lifecycle_medical_device",))[0]
        crud_plan = datastore_crud_plan(preview_action, target_table, {"target_hint": payload.get("target_hint")})
        return {
            "ok": plan["ok"] and crud_plan["ok"],
            "result": {
                "document_plan": plan,
                "crud_plan": crud_plan,
                "preview_only": True,
            },
            "side_effects": (),
        }


def standalone_service_operation_contracts() -> dict:
    """Return the standalone operation surface."""
    contracts = standalone_route_contracts()["contracts"]
    return {
        "ok": bool(contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in contracts),
        "command_operations": tuple(item["operation"] for item in contracts if item["operation_kind"] == "command"),
        "query_operations": tuple(item["operation"] for item in contracts if item["operation_kind"] == "query"),
        "contracts": contracts,
        "side_effects": (),
    }


def medical_device_lifecycle_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this one-PBC package."""
    from .agent import standalone_agent_workspace_contract

    forms = medical_device_lifecycle_form_catalog()
    wizards = medical_device_lifecycle_wizard_catalog()
    controls = medical_device_lifecycle_control_catalog()
    routes = standalone_route_contracts()
    workspace = standalone_agent_workspace_contract()
    return {
        "format": "appgen.medical-device-lifecycle-standalone-app.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and routes["ok"] and workspace["ok"],
        "pbc": PBC_KEY,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "routes": routes,
        "agent": workspace,
        "owned_boundary": medical_device_lifecycle_verify_owned_table_boundary(
            (
                "medical_device_lifecycle_medical_device",
                "medical_device_lifecycle_device_assignment",
                "medical_device_lifecycle_recall_notice",
            )
        ),
        "side_effects": (),
    }


def medical_device_lifecycle_bootstrap_standalone_app(initial_state: dict | None = None) -> dict:
    """Create a live standalone app instance for local package use."""
    app = MedicalDeviceLifecycleStandaloneApp(initial_state)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app": app,
        "contract": medical_device_lifecycle_standalone_app_contract(),
        "side_effects": (),
    }


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    app: MedicalDeviceLifecycleStandaloneApp | None = None,
) -> dict:
    """Dispatch one standalone-app route to the package-local standalone app."""
    route = next(
        (item for item in standalone_route_contracts()["contracts"] if item["method"] == method and item["path"] == path),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    local_app = app or MedicalDeviceLifecycleStandaloneApp()
    try:
        result = getattr(local_app, route["handler"])(payload or {})
        return {
            "ok": result.get("ok") is True,
            "handled": True,
            "route": route,
            "result": result,
            "side_effects": (),
        }
    finally:
        if app is None:
            local_app.close()


def medical_device_lifecycle_standalone_app_smoke() -> dict:
    """Exercise the standalone app through its route surface."""
    bundle = medical_device_lifecycle_bootstrap_standalone_app()
    app = bundle["app"]
    try:
        device = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/devices",
            {
                "tenant": "tenant-standalone",
                "device_id": "MD-100",
                "udi": "UDI-100",
                "manufacturer": "Acme Devices",
                "model": "InfusionPro",
                "serial_number": "SN-100",
                "lot_number": "LOT-01",
                "firmware_version": "1.0.0",
                "risk_class": "II",
                "implantable": False,
                "department": "ICU",
                "location": "ICU-STORE",
                "qualification_status": "qualified",
                "calibration_due_at": "2099-01-01",
                "maintenance_due_at": "2099-02-01",
            },
            app=app,
        )
        calibration = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/calibrations",
            {
                "tenant": "tenant-standalone",
                "calibration_id": "CAL-100",
                "device_id": "MD-100",
                "completed_at": "2026-01-02",
                "outcome": "pass",
                "technician": "tech-01",
                "standard_used": "NIST",
                "next_due_at": "2099-03-01",
            },
            app=app,
        )
        assignment = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/assignments",
            {
                "tenant": "tenant-standalone",
                "assignment_id": "ASN-100",
                "device_id": "MD-100",
                "assignment_type": "room",
                "assignee_ref": "ICU-RM1",
                "responsible_role": "nurse_manager",
                "privacy_scope": "operational",
            },
            app=app,
        )
        usage = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/usage-traces",
            {
                "tenant": "tenant-standalone",
                "usage_id": "USE-100",
                "device_id": "MD-100",
                "assignment_id": "ASN-100",
                "operator_ref": "nurse-1",
                "location": "ICU-RM1",
                "event_type": "in_use",
            },
            app=app,
        )
        evidence_manual = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/regulatory-evidence",
            {
                "tenant": "tenant-standalone",
                "evidence_id": "DOC-100",
                "device_id": "MD-100",
                "document_type": "manual",
                "approved": True,
            },
            app=app,
        )
        evidence_service = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/regulatory-evidence",
            {
                "tenant": "tenant-standalone",
                "evidence_id": "DOC-101",
                "device_id": "MD-100",
                "document_type": "service_record",
                "approved": True,
            },
            app=app,
        )
        evidence_calibration = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/regulatory-evidence",
            {
                "tenant": "tenant-standalone",
                "evidence_id": "DOC-102",
                "device_id": "MD-100",
                "document_type": "calibration_certificate",
                "approved": True,
            },
            app=app,
        )
        recall = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/recalls",
            {
                "tenant": "tenant-standalone",
                "recall_id": "REC-100",
                "manufacturer_notice": "FSN-100",
                "recall_class": "II",
                "device_ids": ["MD-100"],
                "required_action": "quarantine and inspect",
            },
            app=app,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/medical-device-lifecycle/workbench",
            {"tenant": "tenant-standalone"},
            app=app,
        )
        controls = dispatch_standalone_route(
            "GET",
            "/app/medical-device-lifecycle/controls",
            {"tenant": "tenant-standalone"},
            app=app,
        )
        preview = dispatch_standalone_route(
            "POST",
            "/app/medical-device-lifecycle/assistant/document-preview",
            {
                "document_text": "Field safety notice for InfusionPro",
                "instructions": "quarantine the recalled infusion device and attach recall evidence",
                "action": "update",
            },
            app=app,
        )
        return {
            "ok": bundle["contract"]["ok"]
            and device["ok"]
            and calibration["ok"]
            and assignment["ok"]
            and usage["ok"]
            and evidence_manual["ok"]
            and evidence_service["ok"]
            and evidence_calibration["ok"]
            and recall["ok"]
            and workbench["ok"]
            and controls["ok"]
            and preview["ok"]
            and workbench["result"]["recall_hold_count"] == 1,
            "contract": bundle["contract"],
            "device": device,
            "calibration": calibration,
            "assignment": assignment,
            "usage": usage,
            "recall": recall,
            "workbench": workbench["result"],
            "controls": controls["result"]["result"],
            "preview": preview["result"]["result"],
            "side_effects": (),
        }
    finally:
        app.close()
