"""Controls for the construction_project_controls one-PBC app."""
from __future__ import annotations

from .runtime import construction_project_controls_build_controls_contract


def control_contracts():
    return construction_project_controls_build_controls_contract()


def smoke_test():
    return {"ok": control_contracts()["ok"], "side_effects": ()}
