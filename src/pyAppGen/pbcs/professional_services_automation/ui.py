"""UI fragments for the professional_services_automation PBC."""

from __future__ import annotations

from .controls import professional_services_automation_control_catalog
from .forms import professional_services_automation_form_catalog
from .permissions import permission_manifest
from .wizards import professional_services_automation_wizard_catalog
from .domain_depth import domain_capability_surface_contract as professional_services_automation_domain_capability_surface_contract
from .domain_depth import ui_capability_surface_contract as professional_services_automation_ui_capability_surface_contract


PBC_KEY = "professional_services_automation"
UI_FRAGMENTS = (
    "ProfessionalServicesAutomationWorkbench",
    "ProfessionalServicesAutomationDetail",
    "ProfessionalServicesAutomationAssistantPanel",
)



def professional_services_automation_standalone_app_contract() -> dict:
    """Return the package-local standalone app shell contract."""
    forms = professional_services_automation_form_catalog()
    wizards = professional_services_automation_wizard_catalog()
    controls = professional_services_automation_control_catalog()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "app_id": "professional_services_automation_one_pbc_app",
        "workbench_route": "/workbench/pbcs/professional_services_automation",
        "navigation": (
            {"key": "engagements", "route": "/workbench/pbcs/professional_services_automation/engagements"},
            {"key": "staffing", "route": "/workbench/pbcs/professional_services_automation/staffing"},
            {"key": "delivery", "route": "/workbench/pbcs/professional_services_automation/delivery"},
            {"key": "billing", "route": "/workbench/pbcs/professional_services_automation/billing"},
            {"key": "release", "route": "/workbench/pbcs/professional_services_automation/release"},
        ),
        "forms": forms["form_ids"],
        "wizards": wizards["wizard_ids"],
        "controls": controls["control_ids"],
        "single_agent_namespace": f"{PBC_KEY}_skills",
        "side_effects": (),
    }



def professional_services_automation_ui_contract() -> dict:
    """Return the composed UI contract for the PSA workbench."""
    full = professional_services_automation_ui_capability_surface_contract()
    forms = professional_services_automation_form_catalog()
    wizards = professional_services_automation_wizard_catalog()
    controls = professional_services_automation_control_catalog()
    permissions = permission_manifest()
    return {
        "format": "appgen.professional-services-automation-ui-contract.v2",
        "ok": full["ok"] and forms["ok"] and wizards["ok"] and controls["ok"] and permissions["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/professional_services_automation",
        "fragments": UI_FRAGMENTS,
        "workbench_view": UI_FRAGMENTS[0],
        "configuration_editor": True,
        "action_permissions": permissions["permissions"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "standalone_app": professional_services_automation_standalone_app_contract(),
        "full_capability_surface": full,
        "operation_actions": full["operation_actions"],
        "rule_editors": full["rule_editors"],
        "parameter_editors": full["parameter_editors"],
        "advanced_panels": full["advanced_panels"],
        "edge_case_queues": full["edge_case_queues"],
        "table_browsers": full["table_browsers"],
        "navigation_sections": full["navigation_sections"],
        "domain_surface": professional_services_automation_domain_capability_surface_contract(),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def professional_services_automation_render_workbench(state: dict | None = None) -> dict:
    """Return a package-local rendered workbench view."""
    contract = professional_services_automation_ui_contract()
    records = tuple((state or {}).get("records", {}).values())
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "view": UI_FRAGMENTS[0],
        "panels": tuple(dict.fromkeys(("overview", "records", "rules", "agent") + contract["navigation_sections"])),
        "record_count": len(records),
        "operation_actions": contract["operation_actions"],
        "advanced_panels": contract["advanced_panels"],
        "edge_case_queues": contract["edge_case_queues"],
        "table_browsers": contract["table_browsers"],
        "agent_tools": contract["full_capability_surface"]["agent_tools"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "side_effects": (),
    }



def professional_services_automation_render_standalone_app(
    state: dict | None = None,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...] | None = None,
) -> dict:
    """Render the standalone app shell with permission-filtered affordances."""
    contract = professional_services_automation_ui_contract()
    shell = professional_services_automation_standalone_app_contract()
    granted = set(principal_permissions or contract["action_permissions"])
    forms = tuple(item for item in contract["forms"] if item["permission"] in granted)
    wizards = tuple(item for item in contract["wizards"] if item["permission"] in granted)
    controls = tuple(item for item in contract["controls"] if item["permission"] in granted)
    records = tuple((state or {}).get("records", {}).values())
    cards = (
        {"key": "engagements", "label": "Engagements", "value": len(records)},
        {"key": "rules", "label": "Rules", "value": len((state or {}).get("rules", {}))},
        {"key": "outbox", "label": "Outbox Events", "value": len((state or {}).get("outbox", ()))},
        {"key": "exceptions", "label": "Dead Letters", "value": len((state or {}).get("dead_letter", ()))},
    )
    return {
        "ok": contract["ok"] and shell["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "shell": shell,
        "workbench": {
            "view": contract["workbench_view"],
            "fragments": contract["fragments"],
            "navigation": shell["navigation"],
            "cards": cards,
            "record_ids": tuple(item.get("id") for item in records),
        },
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "configuration_bound": bool((state or {}).get("configuration")),
        "binding_evidence": {
            "owned_tables": contract["table_browsers"],
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise package-local UI and standalone shell evidence."""
    contract = professional_services_automation_ui_contract()
    rendered = professional_services_automation_render_workbench({"records": {"eng_1": {"id": "eng_1"}}})
    standalone = professional_services_automation_render_standalone_app(
        {
            "configuration": {"database_backend": "postgresql"},
            "records": {"eng_1": {"id": "eng_1"}},
            "rules": {"rule_1": {"rule_id": "rule_1"}},
            "outbox": ({"event_type": "EngagementCreated"},),
            "dead_letter": (),
        },
        tenant="tenant_smoke",
    )
    return {
        "ok": contract["ok"]
        and rendered["ok"]
        and standalone["ok"]
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls")),
        "contract": contract,
        "rendered": rendered,
        "standalone": standalone,
        "side_effects": (),
    }
