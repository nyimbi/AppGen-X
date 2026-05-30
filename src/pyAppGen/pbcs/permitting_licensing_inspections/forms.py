"""Forms for the permitting_licensing_inspections standalone app."""
from __future__ import annotations

from .runtime import permitting_licensing_inspections_build_forms_contract


def form_contracts():
    return permitting_licensing_inspections_build_forms_contract()


def smoke_test():
    return {"ok": form_contracts()["ok"], "side_effects": ()}
