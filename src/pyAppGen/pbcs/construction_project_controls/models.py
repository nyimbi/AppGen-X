"""Model contracts for construction project controls."""
from __future__ import annotations

from dataclasses import dataclass

from .runtime import construction_project_controls_build_schema_contract


@dataclass(frozen=True)
class ConstructionProjectModel:
    table: str = "construction_project_controls_construction_project"


@dataclass(frozen=True)
class WorkPackageModel:
    table: str = "construction_project_controls_work_package"


@dataclass(frozen=True)
class SiteProgressModel:
    table: str = "construction_project_controls_site_progress"


def model_contracts():
    return construction_project_controls_build_schema_contract()["models"]


def model_catalog():
    return {
        "ok": True,
        "models": (
            ConstructionProjectModel.table,
            WorkPackageModel.table,
            SiteProgressModel.table,
        ),
        "side_effects": (),
    }
