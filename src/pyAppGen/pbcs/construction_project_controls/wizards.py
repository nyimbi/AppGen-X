"""Wizards for the construction_project_controls one-PBC app."""
from __future__ import annotations

from .runtime import construction_project_controls_build_wizards_contract


def wizard_contracts():
    return construction_project_controls_build_wizards_contract()


def smoke_test():
    return {"ok": wizard_contracts()["ok"], "side_effects": ()}
