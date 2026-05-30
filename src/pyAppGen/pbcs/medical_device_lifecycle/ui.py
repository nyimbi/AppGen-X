"""UI contract for the Medical Device Lifecycle PBC."""

from __future__ import annotations

from .controls import medical_device_lifecycle_control_catalog
from .forms import medical_device_lifecycle_form_catalog
from .permissions import permission_manifest
from .runtime import MEDICAL_DEVICE_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
from .runtime import MEDICAL_DEVICE_LIFECYCLE_CONSUMED_EVENT_TYPES
from .runtime import MEDICAL_DEVICE_LIFECYCLE_EMITTED_EVENT_TYPES
from .runtime import MEDICAL_DEVICE_LIFECYCLE_OWNED_TABLES
from .runtime import MEDICAL_DEVICE_LIFECYCLE_REQUIRED_EVENT_TOPIC
from .runtime import medical_device_lifecycle_build_workbench_view
from .wizards import medical_device_lifecycle_wizard_catalog

PBC_KEY = "medical_device_lifecycle"

MEDICAL_DEVICE_LIFECYCLE_UI_FRAGMENT_KEYS = (
    "MedicalDeviceLifecycleWorkbench",
    "DeviceRegistryBoard",
    "AssignmentConsole",
    "CalibrationAndMaintenanceBoard",
    "RecallCommandCenter",
    "UsageTraceConsole",
    "RegulatoryEvidencePanel",
    "MedicalDeviceLifecycleRuleStudio",
    "MedicalDeviceLifecycleAssistantPanel",
    "MedicalDeviceLifecycleControlCenter",
)


def medical_device_lifecycle_ui_contract() -> dict:
    """Return workbench metadata for the standalone medical device slice."""
    forms = medical_device_lifecycle_form_catalog()
    wizards = medical_device_lifecycle_wizard_catalog()
    controls = medical_device_lifecycle_control_catalog()
    permissions = permission_manifest()
    return {
        "format": "appgen.medical-device-lifecycle-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and permissions["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/medical_device_lifecycle",
        "fragments": MEDICAL_DEVICE_LIFECYCLE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/medical_device_lifecycle",
            "/workbench/pbcs/medical_device_lifecycle/registry",
            "/workbench/pbcs/medical_device_lifecycle/assignments",
            "/workbench/pbcs/medical_device_lifecycle/calibration-maintenance",
            "/workbench/pbcs/medical_device_lifecycle/recalls",
            "/workbench/pbcs/medical_device_lifecycle/usage-traceability",
            "/workbench/pbcs/medical_device_lifecycle/evidence",
            "/workbench/pbcs/medical_device_lifecycle/governance",
            "/workbench/pbcs/medical_device_lifecycle/assistant",
            "/workbench/pbcs/medical_device_lifecycle/controls",
        ),
        "panels": (
            {
                "key": "registry",
                "fragment": "DeviceRegistryBoard",
                "binds_to": ("medical_device",),
                "commands": ("register_device", "upsert_policy_rule", "update_runtime_parameter"),
            },
            {
                "key": "assignment",
                "fragment": "AssignmentConsole",
                "binds_to": ("medical_device", "device_assignment"),
                "commands": ("assign_device", "record_usage_trace"),
            },
            {
                "key": "serviceability",
                "fragment": "CalibrationAndMaintenanceBoard",
                "binds_to": ("calibration", "maintenance_event"),
                "commands": ("record_calibration", "record_maintenance"),
            },
            {
                "key": "recalls",
                "fragment": "RecallCommandCenter",
                "binds_to": ("recall_notice", "device_assignment"),
                "commands": ("launch_recall", "attach_regulatory_evidence"),
            },
            {
                "key": "usage",
                "fragment": "UsageTraceConsole",
                "binds_to": ("usage_trace",),
                "commands": ("record_usage_trace",),
            },
            {
                "key": "evidence",
                "fragment": "RegulatoryEvidencePanel",
                "binds_to": ("regulatory_evidence",),
                "commands": ("attach_regulatory_evidence",),
            },
            {
                "key": "assistant",
                "fragment": "MedicalDeviceLifecycleAssistantPanel",
                "binds_to": ("medical_device", "recall_notice", "regulatory_evidence"),
                "commands": ("preview_document_change",),
            },
            {
                "key": "controls",
                "fragment": "MedicalDeviceLifecycleControlCenter",
                "binds_to": ("medical_device_lifecycle_control_assertion",),
                "commands": ("build_control_center",),
            },
        ),
        "action_permissions": permissions["action_permissions"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "quality_score_floor", "workbench_limit"),
            "allowed_database_backends": MEDICAL_DEVICE_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": MEDICAL_DEVICE_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "quality_score_floor",
                "materiality_threshold",
                "approval_sla_hours",
                "risk_threshold",
                "forecast_horizon_days",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("qualification", "assignment", "calibration", "maintenance", "recall", "privacy"),
            "required_fields": ("rule_id", "rule_type", "condition", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": MEDICAL_DEVICE_LIFECYCLE_EMITTED_EVENT_TYPES,
            "consumes": MEDICAL_DEVICE_LIFECYCLE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": MEDICAL_DEVICE_LIFECYCLE_OWNED_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": MEDICAL_DEVICE_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def medical_device_lifecycle_render_workbench(
    summary: dict | None = None,
    *,
    tenant: str = "default",
    principal_permissions: tuple[str, ...] = (),
) -> dict:
    """Render high-level workbench cards for the medical device slice."""
    contract = medical_device_lifecycle_ui_contract()
    visible_permission_set = set(principal_permissions or tuple(dict.fromkeys(contract["action_permissions"].values())))
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in visible_permission_set
    )
    if summary is None:
        from .standalone import medical_device_lifecycle_standalone_app_smoke

        summary = medical_device_lifecycle_standalone_app_smoke()["workbench"]
    baseline_workbench = medical_device_lifecycle_build_workbench_view(tenant)
    cards = (
        {"key": "devices", "value": summary.get("device_count", 0), "fragment": "DeviceRegistryBoard"},
        {"key": "available", "value": summary.get("available_device_count", 0), "fragment": "AssignmentConsole"},
        {"key": "calibration_due", "value": summary.get("calibration_due_count", 0), "fragment": "CalibrationAndMaintenanceBoard"},
        {"key": "recall_hold", "value": summary.get("recall_hold_count", 0), "fragment": "RecallCommandCenter"},
        {"key": "missing_evidence", "value": summary.get("missing_evidence_count", 0), "fragment": "RegulatoryEvidencePanel"},
        {"key": "outbox", "value": summary.get("outbox_count", 0), "fragment": "MedicalDeviceLifecycleAssistantPanel"},
    )
    return {
        "format": "appgen.medical-device-lifecycle-workbench-render.v1",
        "ok": True,
        "tenant": summary.get("tenant", tenant),
        "route": "/workbench/pbcs/medical_device_lifecycle",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "queues": summary.get("queues", {}),
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "binding_evidence": {
            **contract["workbench_binding_evidence"],
            "baseline_workbench": baseline_workbench,
        },
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = medical_device_lifecycle_ui_contract()
    rendered = medical_device_lifecycle_render_workbench()
    return {
        "ok": contract["ok"]
        and rendered["ok"]
        and bool(contract["forms"])
        and bool(contract["wizards"])
        and bool(contract["controls"])
        and contract["configuration_editor"]["stream_engine_picker_visible"] is False,
        "contract": contract,
        "rendered": rendered,
        "side_effects": (),
    }
