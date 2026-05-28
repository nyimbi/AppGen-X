"""Workbench UI surface for the chemical_batch_compliance PBC."""

from __future__ import annotations

from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .slice_app import PBC_KEY
from .slice_app import build_app_surface
from .slice_app import build_workbench_view


def chemical_batch_compliance_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    app_surface = build_app_surface()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": (
            "ChemicalBatchComplianceWorkbench",
            "ChemicalBatchComplianceDetail",
            "ChemicalBatchComplianceAssistantPanel",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            f"{PBC_KEY}.read",
            f"{PBC_KEY}.create",
            f"{PBC_KEY}.update",
            f"{PBC_KEY}.approve",
            f"{PBC_KEY}.admin",
        ),
        "full_capability_surface": {
            "operation_actions": DOMAIN_OPERATIONS,
            "rule_editors": DOMAIN_RULES,
            "parameter_editors": DOMAIN_PARAMETERS,
            "advanced_panels": DOMAIN_ADVANCED_CAPABILITIES,
            "table_browsers": DOMAIN_OWNED_TABLES,
            "edge_case_queues": DOMAIN_EDGE_CASES,
            "agent_tools": tuple(f"{PBC_KEY}_skills.{op}" for op in DOMAIN_OPERATIONS),
            "navigation_sections": (
                "overview",
                "formula_release",
                "batch_execution",
                "quality_and_holds",
                "regulatory_dossiers",
                "assistant_governance",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
            "forms": app_surface["forms"],
            "wizards": app_surface["wizards"],
            "controls": app_surface["controls"],
            "views": app_surface["views"],
            "assistant_cards": app_surface["assistant_cards"],
        },
        "side_effects": (),
    }


def chemical_batch_compliance_render_workbench(tenant: str = "default") -> dict:
    return build_workbench_view(tenant=tenant)


def smoke_test() -> dict:
    return {
        "ok": chemical_batch_compliance_ui_contract()["ok"]
        and chemical_batch_compliance_render_workbench()["ok"],
        "side_effects": (),
    }
