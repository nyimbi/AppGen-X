"""Standalone application surface evidence for the tax_localization PBC."""

from __future__ import annotations

from . import agent
from .controls import tax_localization_control_catalog
from .forms import tax_localization_form_catalog
from .repository import smoke_test as repository_smoke_test
from .repository import TaxLocalizationRepository
from .runtime import TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS
from .wizards import tax_localization_wizard_catalog


PBC_KEY = "tax_localization"


def single_pbc_tax_localization_contract() -> dict:
    forms = tax_localization_form_catalog()
    wizards = tax_localization_wizard_catalog()
    controls = tax_localization_control_catalog()
    repo = TaxLocalizationRepository()
    try:
        repository_manifest = repo.database_manifest()
    finally:
        repo.close()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"] and repository_manifest["ok"],
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": TAX_LOCALIZATION_ALLOWED_DATABASE_BACKENDS,
        "local_repository_backend": repository_manifest["local_repository_backend"],
        "owned_tables": repository_manifest["owned_tables"],
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "workbench": "TaxLocalizationWorkbench",
        "assistant_panel": "TaxLocalizationAgent",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_tax_plan(document: str, instructions: str, *, target_entity: str | None = None, requested_action: str | None = None) -> dict:
    plan = agent.document_instruction_plan(
        document,
        instructions,
        target_entity=target_entity,
        requested_action=requested_action,
    )
    preview = agent.tax_localization_assistant_preview(
        {
            "document_text": document,
            "instructions": instructions,
            "target_entity": plan["target_entity"],
            "requested_action": plan["requested_action"],
            "payload": {"document_digest": plan["document_digest"]},
        }
    )
    return {
        "ok": plan["ok"] and preview["ok"],
        "pbc": PBC_KEY,
        "domain_plan": plan,
        "crud_preview": preview["mutation_preview"],
        "requires_human_confirmation": plan["requires_human_confirmation"],
        "side_effects": (),
    }


def app_surface_smoke_test() -> dict:
    app = single_pbc_tax_localization_contract()
    repository = repository_smoke_test()
    quote_plan = document_instruction_tax_plan(
        "California local sales tax memo for bottled goods.",
        "Update the tax rule and review the filing implication.",
        target_entity="tax_rule",
        requested_action="update",
    )
    return {
        "ok": app["ok"] and repository["ok"] and quote_plan["ok"],
        "single_pbc_app": app,
        "repository": repository,
        "document_plan": quote_plan,
        "side_effects": (),
    }
