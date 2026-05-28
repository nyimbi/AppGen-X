"""Forms for the construction_project_controls one-PBC app."""
from __future__ import annotations

from .runtime import construction_project_controls_build_forms_contract


def form_contracts():
    return construction_project_controls_build_forms_contract()


def smoke_test():
    return {"ok": form_contracts()["ok"], "side_effects": ()}
