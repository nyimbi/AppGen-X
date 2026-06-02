"""Single-PBC app UI surfaces for the BIM operations slice."""
from __future__ import annotations

from .bim_control import BIM_CONTROL_CAPABILITIES, improve1_bim_control_contract
from .federation_governance import DISCIPLINES, ISSUE_PURPOSES

PBC_KEY = "building_information_modeling_ops"


def building_information_modeling_ops_forms_contract() -> dict:
    forms = (
        {
            "form_id": "project_coordinate_baseline_form",
            "title": "Project Coordinate Baseline",
            "table": f"{PBC_KEY}_model_version",
            "fields": (
                "coordinate_basis",
                "survey_point",
                "project_base_point",
                "true_north_degrees",
                "elevation_datum",
                "unit_scale",
            ),
            "submit_action": "configure_project_coordinates",
            "database_backed": True,
        },
        {
            "form_id": "model_package_registration_form",
            "title": "Model Package Registration",
            "table": f"{PBC_KEY}_model_version",
            "fields": (
                "model_id",
                "version_id",
                "discipline",
                "authoring_party",
                "issue_purpose",
                "approval_state",
                "spatial_coverage",
                "lod_target",
                "checksum",
            ),
            "submit_action": "register_model_package",
            "choices": {
                "discipline": DISCIPLINES,
                "issue_purpose": ISSUE_PURPOSES,
            },
            "database_backed": True,
        },
        {
            "form_id": "federation_assembly_form",
            "title": "Federation Assembly",
            "table": f"{PBC_KEY}_building_information_modeling_ops_governed_model",
            "fields": ("federation_id", "intended_use", "version_ids"),
            "submit_action": "assemble_federation",
            "database_backed": True,
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "forms": forms,
        "single_pbc_app": True,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def building_information_modeling_ops_wizard_contract() -> dict:
    wizards = (
        {
            "wizard_id": "federation_setup_wizard",
            "title": "Federation Setup Wizard",
            "steps": (
                "configure_project_coordinates",
                "register_model_package",
                "validate_coordinate_alignment",
                "assemble_federation",
                "seal_release_evidence",
            ),
            "entry_form": "project_coordinate_baseline_form",
            "completion_view": "federation_operations_workbench",
        },
        {
            "wizard_id": "release_readiness_wizard",
            "title": "Release Readiness Wizard",
            "steps": (
                "review_blocked_packages",
                "check_issue_purpose_gate",
                "preview_release_evidence",
                "confirm_approval_lineage",
            ),
            "entry_form": "federation_assembly_form",
            "completion_view": "release_evidence_desk",
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizards": wizards,
        "single_pbc_app": True,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def building_information_modeling_ops_controls_contract() -> dict:
    controls = (
        {
            "control_id": "coordinate_alignment_control",
            "control_type": "validation",
            "checks": (
                "coordinate_basis_mismatch",
                "survey_point_out_of_tolerance",
                "project_base_point_out_of_tolerance",
                "true_north_out_of_tolerance",
                "elevation_datum_mismatch",
                "unit_scale_mismatch",
            ),
            "blocks_release": True,
        },
        {
            "control_id": "issue_purpose_gate_control",
            "control_type": "lifecycle_gate",
            "allowed_issue_purposes": ("shared", "construction", "record", "handover"),
            "blocks_release": True,
        },
        {
            "control_id": "approval_lineage_control",
            "control_type": "approval_gate",
            "required_state": "approved",
            "blocks_release": True,
        },
        {
            "control_id": "owned_table_boundary_control",
            "control_type": "boundary_guard",
            "shared_table_access": False,
            "blocks_release": True,
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "controls": controls,
        "single_pbc_app": True,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def building_information_modeling_ops_ui_contract() -> dict:
    forms = building_information_modeling_ops_forms_contract()
    wizards = building_information_modeling_ops_wizard_contract()
    controls = building_information_modeling_ops_controls_contract()
    workbench_views = (
        {
            "view_id": "federation_operations_workbench",
            "route": f"/workbench/pbcs/{PBC_KEY}",
            "focus": "active federations by discipline",
        },
        {
            "view_id": "package_readiness_board",
            "route": f"/workbench/pbcs/{PBC_KEY}/packages",
            "focus": "blocked packages and coordinate issues",
        },
        {
            "view_id": "release_evidence_desk",
            "route": f"/workbench/pbcs/{PBC_KEY}/release-evidence",
            "focus": "checksums, approvals, and audit seals",
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "BuildingInformationModelingOpsWorkbench",
            "BuildingInformationModelingOpsDetail",
            "BuildingInformationModelingOpsAssistantPanel",
            "BuildingInformationModelingOpsFederationWizard",
        ),
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workbench_views": workbench_views,
        "bim_control_panels": tuple(f"bim_control_{capability}" for capability in BIM_CONTROL_CAPABILITIES),
        "bim_control_contract": improve1_bim_control_contract(),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "single_pbc_app": True,
        "action_permissions": (
            "building_information_modeling_ops.read",
            "building_information_modeling_ops.create",
            "building_information_modeling_ops.update",
            "building_information_modeling_ops.approve",
            "building_information_modeling_ops.admin",
        ),
        "side_effects": (),
    }


def building_information_modeling_ops_render_workbench(state: dict | None = None) -> dict:
    ui = building_information_modeling_ops_ui_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "workbench_views": ui["workbench_views"],
        "state": dict(state or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    ui = building_information_modeling_ops_ui_contract()
    rendered = building_information_modeling_ops_render_workbench()
    return {
        "ok": ui["ok"] and rendered["ok"] and bool(ui["forms"]) and bool(ui["wizards"]) and bool(ui["controls"]),
        "side_effects": (),
    }
