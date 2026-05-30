"""UI fragments for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import (
    CONTROL_BLUEPRINTS,
    FORM_BLUEPRINTS,
    NAVIGATION_SECTIONS,
    PBC_KEY,
    PERMISSIONS,
    UI_FRAGMENTS,
    WIZARD_BLUEPRINTS,
    WORKBENCH_VIEWS,
)
from .domain_depth import ui_capability_surface_contract


def data_product_catalog_ui_contract() -> dict:
    capability_surface = ui_capability_surface_contract()
    return {
        "ok": capability_surface["ok"],
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENTS,
        "workbench_view": UI_FRAGMENTS[0],
        "workbench_views": WORKBENCH_VIEWS,
        "forms": FORM_BLUEPRINTS,
        "wizards": WIZARD_BLUEPRINTS,
        "controls": CONTROL_BLUEPRINTS,
        "navigation_sections": NAVIGATION_SECTIONS,
        "configuration_editor": True,
        "action_permissions": PERMISSIONS,
        "stream_engine_picker_visible": False,
        "full_capability_surface": capability_surface,
        "side_effects": (),
    }


def data_product_catalog_render_workbench(state: dict | None = None) -> dict:
    state = dict(state or {})
    records = state.get("records", {})
    table_counts = {table: len(items) for table, items in records.items()} if isinstance(records, dict) else {}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "view": UI_FRAGMENTS[0],
        "panels": NAVIGATION_SECTIONS,
        "forms": FORM_BLUEPRINTS,
        "wizards": WIZARD_BLUEPRINTS,
        "controls": CONTROL_BLUEPRINTS,
        "table_counts": table_counts,
        "configuration_editor": True,
        "action_permissions": PERMISSIONS,
        "side_effects": (),
    }


def smoke_test() -> dict:
    contract = data_product_catalog_ui_contract()
    rendered = data_product_catalog_render_workbench()
    return {"ok": contract["ok"] and rendered["ok"], "contract": contract, "rendered": rendered, "side_effects": ()}
