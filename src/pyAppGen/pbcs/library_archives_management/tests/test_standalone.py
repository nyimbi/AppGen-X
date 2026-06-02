from pyAppGen.pbcs.library_archives_management import implementation_contract
from pyAppGen.pbcs.library_archives_management.controls import library_archives_management_assistant_crud_preview
from pyAppGen.pbcs.library_archives_management.controls import library_archives_management_control_center
from pyAppGen.pbcs.library_archives_management.controls import library_archives_management_mutation_preview
from pyAppGen.pbcs.library_archives_management.forms import library_archives_management_form_catalog
from pyAppGen.pbcs.library_archives_management.forms import library_archives_management_form_examples
from pyAppGen.pbcs.library_archives_management.forms import library_archives_management_validate_form_payload
from pyAppGen.pbcs.library_archives_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.library_archives_management.standalone import REQUIRED_DOMAIN_AREAS
from pyAppGen.pbcs.library_archives_management.standalone import library_archives_management_standalone_app_contract
from pyAppGen.pbcs.library_archives_management.standalone import library_archives_management_standalone_app_smoke
from pyAppGen.pbcs.library_archives_management.ui import library_archives_management_render_workbench
from pyAppGen.pbcs.library_archives_management.ui import library_archives_management_ui_contract
from pyAppGen.pbcs.library_archives_management.wizards import library_archives_management_plan_wizard
from pyAppGen.pbcs.library_archives_management.wizards import library_archives_management_wizard_catalog


def test_forms_cover_required_library_and_archives_domains():
    forms = library_archives_management_form_catalog()
    examples = library_archives_management_form_examples()
    assert forms["ok"] is True
    assert examples["ok"] is True
    assert set(REQUIRED_DOMAIN_AREAS).issubset(set(forms["domain_areas"]))
    for form_id, payload in examples["examples"].items():
        validation = library_archives_management_validate_form_payload(form_id, payload)
        assert validation["ok"] is True


def test_wizards_cover_domain_workflows_and_bind_existing_forms():
    wizards = library_archives_management_wizard_catalog()
    assert wizards["ok"] is True
    assert set(REQUIRED_DOMAIN_AREAS).issubset(set(wizards["domain_areas"]) | {"holds", "conservation", "assistant CRUD previews"})
    plan = library_archives_management_plan_wizard(
        "preservation_digitization_access",
        {"item_id": "ITEM-OH-44", "job_id": "DIG-6001", "rights_id": "RIGHTS-204"},
    )
    assert plan["ok"] is True
    assert any(step["ready"] for step in plan["steps"])


def test_controls_and_assistant_previews_enforce_owned_boundary():
    preview = library_archives_management_mutation_preview(
        "update",
        "library_archives_management_rights_statement",
        {"rights_id": "RIGHTS-204"},
    )
    assert preview["ok"] is True
    assistant = library_archives_management_assistant_crud_preview(
        "Preview a rights update for oral history access.",
        "Update only the onsite consultation rule.",
        action="update",
        target_table="library_archives_management_rights_statement",
        payload={"access_level": "onsite_only"},
    )
    assert assistant["ok"] is True
    control_center = library_archives_management_control_center({"tenant": "archives-east"})
    assert control_center["ok"] is True
    assert control_center["foreign_preview"]["ok"] is False


def test_ui_release_evidence_and_standalone_contract_stay_aligned():
    ui = library_archives_management_ui_contract()
    workbench = library_archives_management_render_workbench()
    standalone = library_archives_management_standalone_app_contract()
    evidence = build_release_evidence()
    package_contract = implementation_contract()
    assert ui["ok"] is True
    assert workbench["ok"] is True
    assert standalone["ok"] is True
    assert evidence["ok"] is True
    assert evidence["standalone_app"]["ok"] is True
    assert package_contract["standalone_contract"]["ok"] is True
    assert not standalone["missing_domain_areas"]


def test_standalone_smoke_executes_domain_deep_walkthrough():
    smoke = library_archives_management_standalone_app_smoke()
    assert smoke["ok"] is True
    assert set(REQUIRED_DOMAIN_AREAS).issubset(set(smoke["covered_domains"]))
    assert smoke["controls"]["ok"] is True
    assert smoke["assistant_preview"]["ok"] is True
    assert all(result["ok"] for result in smoke["service_calls"].values())
