"""Wizards for the land_real_estate_development standalone app."""

from __future__ import annotations

from .standalone import land_real_estate_development_build_wizards_contract


def wizard_contracts() -> dict:
    return land_real_estate_development_build_wizards_contract()


def smoke_test() -> dict:
    return {"ok": wizard_contracts()["ok"], "side_effects": ()}
