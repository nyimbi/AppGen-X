"""Wizards for the permitting_licensing_inspections standalone app."""
from __future__ import annotations

from .runtime import permitting_licensing_inspections_build_wizards_contract


def wizard_contracts():
    return permitting_licensing_inspections_build_wizards_contract()


def smoke_test():
    return {"ok": wizard_contracts()["ok"], "side_effects": ()}
