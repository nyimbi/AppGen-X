"""UI contracts for the oil_gas_field_operations PBC."""

from __future__ import annotations

from .controls import oil_gas_field_operations_control_catalog
from .domain_depth import DOMAIN_ADVANCED_CAPABILITIES
from .domain_depth import DOMAIN_EDGE_CASES
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import domain_capability_surface_contract
from .forms import oil_gas_field_operations_form_catalog
from .wizards import oil_gas_field_operations_wizard_catalog

PBC_KEY = "oil_gas_field_operations"


def oil_gas_field_operations_standalone_workbench_blueprint() -> dict:
    forms = oil_gas_field_operations_form_catalog()
    wizards = oil_gas_field_operations_wizard_catalog()
    controls = oil_gas_field_operations_control_catalog()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "route": "/app/oil-gas-field-operations/workbench",
        "panels": (
            "route_surveillance",
            "allocation_exceptions",
            "workover_candidates",
            "hse_boundary_monitor",
            "assistant_panel",
        ),
        "forms": forms["form_ids"],
        "wizards": wizards["wizard_ids"],
        "controls": controls["control_ids"],
        "side_effects": (),
    }


def oil_gas_field_operations_ui_contract() -> dict:
    surface = domain_capability_surface_contract()
    forms = oil_gas_field_operations_form_catalog()
    wizards = oil_gas_field_operations_wizard_catalog()
    controls = oil_gas_field_operations_control_catalog()
    standalone = oil_gas_field_operations_standalone_workbench_blueprint()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and standalone["ok"],
        "pbc": PBC_KEY,
        "fragments": (
            "OilGasFieldOperationsWorkbench",
            "OilGasFieldOperationsDetail",
            "OilGasFieldOperationsAssistantPanel",
            "OilGasFieldOperationsMorningReview",
            "OilGasFieldOperationsControlCenter",
        ),
        "configuration_editor": True,
        "stream_engine_picker_visible": False,
        "action_permissions": (
            "oil_gas_field_operations.read",
            "oil_gas_field_operations.create",
            "oil_gas_field_operations.update",
            "oil_gas_field_operations.approve",
            "oil_gas_field_operations.admin",
        ),
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "standalone_workbench": standalone,
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
                "routes_and_pads",
                "production_surveillance",
                "allocation_and_reconciliation",
                "workover_readiness",
                "hse_boundary_monitor",
                "assistant_preview",
                "release_evidence",
            ),
            "coverage": surface["coverage"],
        },
        "side_effects": (),
    }


def oil_gas_field_operations_render_workbench() -> dict:
    ui = oil_gas_field_operations_ui_contract()
    full = ui["full_capability_surface"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "operation_actions": full["operation_actions"],
        "table_browsers": full["table_browsers"],
        "forms": ui["forms"]["form_ids"],
        "wizards": ui["wizards"]["wizard_ids"],
        "controls": ui["controls"]["control_ids"],
        "side_effects": (),
    }


def oil_gas_field_operations_render_standalone_workbench(workbench: dict | None = None) -> dict:
    payload = dict(workbench or {})
    summary = dict(payload.get("summary", {}))
    cards = (
        {"card_id": "producing_wells", "label": "Producing wells", "value": summary.get("producing_wells", 0)},
        {"card_id": "surveillance_wells", "label": "Surveillance wells", "value": summary.get("surveillance_wells", 0)},
        {"card_id": "allocation_exceptions", "label": "Allocation exceptions", "value": summary.get("allocation_exceptions", 0)},
        {"card_id": "open_field_tickets", "label": "Open field tickets", "value": summary.get("open_field_tickets", 0)},
        {"card_id": "reportable_hse", "label": "Reportable HSE", "value": summary.get("reportable_hse", 0)},
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "route": "/app/oil-gas-field-operations/workbench",
        "cards": cards,
        "records": tuple(payload.get("records", ())),
        "forms": oil_gas_field_operations_form_catalog()["form_ids"],
        "wizards": oil_gas_field_operations_wizard_catalog()["wizard_ids"],
        "controls": oil_gas_field_operations_control_catalog()["control_ids"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    rendered = oil_gas_field_operations_render_standalone_workbench(
        {
            "summary": {
                "producing_wells": 3,
                "surveillance_wells": 1,
                "allocation_exceptions": 1,
                "open_field_tickets": 2,
                "reportable_hse": 0,
            }
        }
    )
    return {
        "ok": oil_gas_field_operations_ui_contract()["ok"] and oil_gas_field_operations_render_workbench()["ok"] and rendered["ok"],
        "side_effects": (),
    }
