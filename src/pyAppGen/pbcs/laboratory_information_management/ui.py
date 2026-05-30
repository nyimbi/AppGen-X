"""UI contract for the laboratory_information_management PBC."""

from __future__ import annotations

from .controls import laboratory_information_management_control_center
from .controls import laboratory_information_management_control_catalog
from .forms import laboratory_information_management_form_catalog
from .runtime import LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES
from .runtime import laboratory_information_management_permissions_contract
from .standalone import standalone_manifest
from .wizards import laboratory_information_management_wizard_catalog

PBC_KEY = "laboratory_information_management"


def laboratory_information_management_ui_contract() -> dict:
    forms = laboratory_information_management_form_catalog()
    wizards = laboratory_information_management_wizard_catalog()
    controls = laboratory_information_management_control_catalog()
    permissions = laboratory_information_management_permissions_contract()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/laboratory_information_management",
        "fragments": (
            "LaboratoryInformationManagementWorkbench",
            "LaboratoryInformationManagementDetail",
            "LaboratoryInformationManagementAssistantPanel",
            "LaboratoryInformationManagementStandaloneWorkbench",
            "LaboratoryInformationManagementQcGate",
            "LaboratoryInformationManagementAuditTrailPanel",
        ),
        "forms": forms["form_ids"],
        "wizards": wizards["wizard_ids"],
        "controls": controls["control_ids"],
        "routes": (
            "/workbench/pbcs/laboratory_information_management",
            "/workbench/pbcs/laboratory_information_management/accessioning",
            "/workbench/pbcs/laboratory_information_management/qc",
            "/workbench/pbcs/laboratory_information_management/results",
            "/workbench/pbcs/laboratory_information_management/oos",
            "/workbench/pbcs/laboratory_information_management/stability",
            "/workbench/pbcs/laboratory_information_management/audit",
        ),
        "action_permissions": permissions["permissions"],
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "binding_evidence": {
            "owned_tables": LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES,
            "shared_table_access": False,
            "standalone_surface": standalone_manifest(),
        },
        "side_effects": (),
    }


def laboratory_information_management_standalone_workbench_blueprint() -> dict:
    forms = laboratory_information_management_form_catalog()
    wizards = laboratory_information_management_wizard_catalog()
    controls = laboratory_information_management_control_catalog()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "route": "/app/laboratory-information-management/workbench",
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "assistant_panel": {
            "preview_only": True,
            "requires_confirmation": True,
            "citations_required": True,
        },
        "side_effects": (),
    }


def laboratory_information_management_render_workbench() -> dict:
    ui = laboratory_information_management_ui_contract()
    return {
        "ok": ui["ok"],
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "fragments": ui["fragments"],
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "side_effects": (),
    }


def laboratory_information_management_render_standalone_workbench(summary: dict) -> dict:
    blueprint = laboratory_information_management_standalone_workbench_blueprint()
    control_center = laboratory_information_management_control_center(summary)
    queue_counts = dict(summary.get("queue_counts", {}))
    cards = (
        {"key": "accessioning", "value": queue_counts.get("accessioning", 0), "fragment": "LaboratoryInformationManagementWorkbench"},
        {"key": "pending_runs", "value": queue_counts.get("pending_runs", 0), "fragment": "LaboratoryInformationManagementQcGate"},
        {"key": "results_review", "value": queue_counts.get("results_review", 0), "fragment": "LaboratoryInformationManagementDetail"},
        {"key": "oos_open", "value": queue_counts.get("oos_open", 0), "fragment": "LaboratoryInformationManagementAuditTrailPanel"},
        {"key": "stability_due", "value": queue_counts.get("stability_due", 0), "fragment": "LaboratoryInformationManagementAssistantPanel"},
        {"key": "coa_ready", "value": queue_counts.get("coa_ready", 0), "fragment": "LaboratoryInformationManagementStandaloneWorkbench"},
    )
    return {
        "ok": blueprint["ok"] and control_center["ok"],
        "pbc": PBC_KEY,
        "route": blueprint["route"],
        "cards": cards,
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "control_center": control_center,
        "assistant_guardrails": summary.get("assistant_guardrails", {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    rendered = laboratory_information_management_render_standalone_workbench(
        {
            "queue_counts": {"accessioning": 1, "pending_runs": 1, "results_review": 1, "oos_open": 0, "stability_due": 1, "coa_ready": 1},
            "assistant_guardrails": {"preview_only": True, "requires_confirmation_for_mutation": True, "citations_required": True},
            "audit": {"ok": True},
        }
    )
    return {
        "ok": laboratory_information_management_ui_contract()["ok"] and laboratory_information_management_render_workbench()["ok"] and rendered["ok"],
        "rendered": rendered,
        "side_effects": (),
    }
