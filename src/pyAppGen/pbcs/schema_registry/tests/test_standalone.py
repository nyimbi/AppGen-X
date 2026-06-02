"""Standalone app smoke tests for schema_registry."""

from __future__ import annotations

from ..forms import schema_registry_form_catalog
from ..repository import schema_registry_repository_manifest
from ..standalone import SchemaRegistryStandaloneApp
from ..standalone import smoke_test
from ..ui import schema_registry_standalone_app_contract
from ..wizards import schema_registry_wizard_catalog


def test_standalone_manifest_and_smoke():
    contract = schema_registry_standalone_app_contract()
    app_smoke = smoke_test()
    repository = schema_registry_repository_manifest()
    forms = schema_registry_form_catalog()
    wizards = schema_registry_wizard_catalog()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert repository["ok"] is True
    assert forms
    assert wizards
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = SchemaRegistryStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assistant = app.assistant_workspace()
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "schema_registry_one_pbc_app"
    assert assistant["ok"] is True
    assert assistant["forms"]
    assert assistant["wizards"]
