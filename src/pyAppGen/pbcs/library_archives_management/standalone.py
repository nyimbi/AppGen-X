"""Standalone one-PBC app composition for the Library and Archives Management package."""

from __future__ import annotations

from .agent import agent_skill_manifest
from .agent import chatbot_interface_contract
from .controls import library_archives_management_assistant_crud_preview
from .controls import library_archives_management_control_center
from .controls import library_archives_management_control_catalog
from .forms import library_archives_management_form_catalog
from .forms import library_archives_management_form_examples
from .forms import library_archives_management_validate_form_payload
from .manifest import PBC_MANIFEST
from .routes import ROUTES
from .routes import api_route_contracts
from .routes import dispatch_route
from .services import LibraryArchivesManagementService
from .services import service_operation_manifest
from .ui import library_archives_management_render_workbench
from .ui import library_archives_management_ui_contract
from .wizards import library_archives_management_plan_wizard
from .wizards import library_archives_management_wizard_catalog

PBC_KEY = "library_archives_management"
REQUIRED_DOMAIN_AREAS = (
    "accessioning",
    "cataloging",
    "authority control",
    "circulation/loans",
    "holds",
    "acquisitions",
    "preservation",
    "digitization",
    "rights/access restrictions",
    "finding aids",
    "reading-room requests",
    "deaccessioning",
    "provenance",
    "conservation",
    "audits",
    "assistant CRUD previews",
)



def library_archives_management_standalone_app_contract() -> dict:
    """Return the composed standalone-app surface for this one-PBC package."""
    forms = library_archives_management_form_catalog()
    wizards = library_archives_management_wizard_catalog()
    controls = library_archives_management_control_catalog()
    ui = library_archives_management_ui_contract()
    routes = api_route_contracts()
    services = service_operation_manifest()
    agent = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    supported_domain_areas = tuple(
        dict.fromkeys(forms["domain_areas"] + wizards["domain_areas"] + controls["domain_areas"])
    )
    missing_domain_areas = tuple(area for area in REQUIRED_DOMAIN_AREAS if area not in supported_domain_areas)
    return {
        "format": "appgen.library-archives-management-standalone-app.v1",
        "ok": all(
            item.get("ok") is True
            for item in (forms, wizards, controls, ui, routes, services, agent, chatbot)
        ) and not missing_domain_areas,
        "pbc": PBC_KEY,
        "manifest": dict(PBC_MANIFEST),
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "ui": ui,
        "routes": routes,
        "services": services,
        "agent": agent,
        "chatbot": chatbot,
        "supported_domain_areas": supported_domain_areas,
        "missing_domain_areas": missing_domain_areas,
        "side_effects": (),
    }



def library_archives_management_bootstrap_standalone_app() -> dict:
    """Create a standalone service bundle for local package use."""
    service = LibraryArchivesManagementService()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service": service,
        "contract": library_archives_management_standalone_app_contract(),
        "side_effects": (),
    }



def library_archives_management_standalone_domain_walkthrough() -> dict:
    """Exercise the standalone surface across the core library and archives domains."""
    bundle = library_archives_management_bootstrap_standalone_app()
    service = bundle["service"]
    examples = library_archives_management_form_examples()["examples"]
    validations = tuple(
        library_archives_management_validate_form_payload(form_id, payload)
        for form_id, payload in examples.items()
    )
    wizard_contexts = {
        "acquisition_to_accession": {"decision_id": "ACQ-2026-014", "accession_number": "2026-045", "provenance_id": "PROV-884"},
        "catalog_authority_and_finding_aid": {"record_id": "CAT-00045", "heading_id": "AUTH-119"},
        "circulation_and_holds": {"item_id": "ITEM-BOOK-778"},
        "preservation_digitization_access": {"item_id": "ITEM-OH-44", "job_id": "DIG-6001", "rights_id": "RIGHTS-204"},
        "reading_room_service": {"request_id": "RR-0091", "researcher_id": "RES-771", "item_ids": ["ITEM-OH-44", "ITEM-MS-12"]},
        "deaccession_and_audit": {"audit_id": "AUD-330", "provenance_id": "PROV-884", "rights_id": "RIGHTS-204"},
        "assistant_curator_preview": {"target_table": "library_archives_management_rights_statement", "requested_action": "update"},
    }
    plans = tuple(
        library_archives_management_plan_wizard(wizard_id, wizard_contexts[wizard_id])
        for wizard_id in wizard_contexts
    )
    service_calls = {
        "accession": service.record_archive_request(examples["accession_register_intake"]),
        "catalog": service.record_catalog_record(examples["catalog_recording"]),
        "loan": service.review_circulation_loan(examples["circulation_loan_checkout"]),
        "rights": service.simulate_rights_statement(examples["rights_access_restriction"]),
        "preservation": service.create_preservation_action(examples["preservation_treatment"]),
        "digitization": service.approve_digitization_job(examples["digitization_triage"]),
        "audit": service.create_library_archives_management_control_assertion(examples["inventory_audit"]),
        "assistant": service.record_library_archives_management_governed_model(examples["assistant_crud_preview"]),
    }
    route_results = tuple(
        dispatch_route(route, {"route": route, "tenant": "archives-east"})
        for route in ROUTES
    )
    workbench = library_archives_management_render_workbench()
    controls = library_archives_management_control_center({"tenant": "archives-east"})
    assistant_preview = library_archives_management_assistant_crud_preview(
        examples["assistant_crud_preview"]["document_text"],
        examples["assistant_crud_preview"]["instructions"],
        action=examples["assistant_crud_preview"]["requested_action"],
        target_table=examples["assistant_crud_preview"]["target_table"],
        payload={"rights_id": "RIGHTS-204", "access_level": "onsite_only"},
    )
    covered_domains = tuple(
        dict.fromkeys(
            library_archives_management_standalone_app_contract()["supported_domain_areas"]
        )
    )
    missing_domain_areas = tuple(area for area in REQUIRED_DOMAIN_AREAS if area not in covered_domains)
    return {
        "ok": bundle["contract"]["ok"]
        and all(item["ok"] for item in validations)
        and all(plan["ok"] for plan in plans)
        and all(result["ok"] for result in service_calls.values())
        and all(route["ok"] for route in route_results)
        and workbench["ok"]
        and controls["ok"]
        and assistant_preview["ok"]
        and not missing_domain_areas,
        "contract": bundle["contract"],
        "validations": validations,
        "plans": plans,
        "service_calls": service_calls,
        "route_results": route_results,
        "workbench": workbench,
        "controls": controls,
        "assistant_preview": assistant_preview,
        "covered_domains": covered_domains,
        "missing_domain_areas": missing_domain_areas,
        "side_effects": (),
    }



def library_archives_management_standalone_app_smoke() -> dict:
    """Exercise the standalone app through its domain walkthrough."""
    return library_archives_management_standalone_domain_walkthrough()
