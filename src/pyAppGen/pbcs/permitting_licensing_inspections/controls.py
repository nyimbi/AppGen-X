"""Controls for the permitting_licensing_inspections standalone app."""
from __future__ import annotations

from .runtime import permitting_licensing_inspections_build_controls_contract


def control_contracts():
    return permitting_licensing_inspections_build_controls_contract()


def smoke_test():
    return {"ok": control_contracts()["ok"], "side_effects": ()}
