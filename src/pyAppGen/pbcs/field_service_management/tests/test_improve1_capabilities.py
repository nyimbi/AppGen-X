"""Executable improve1 capability registry checks."""

from pathlib import Path
import re

from ..improve1_capabilities import capability_registry, plan_feature_execution, validate_improve1_capabilities


def _titles() -> tuple[str, ...]:
    improve = (Path(__file__).resolve().parents[1] / "improve1.md").read_text()
    return tuple(title for _, title in re.findall(r"^###\s+(\d+)\.\s+(.+)$", improve, re.M))


def test_improve1_capability_registry_matches_backlog_and_surfaces():
    titles = _titles()
    validation = validate_improve1_capabilities(titles)
    registry = capability_registry()
    assert validation["ok"] is True
    assert registry["ok"] is True
    assert registry["capability_count"] == 50
    for capability in registry["capabilities"]:
        assert capability["code_artifact_model"]
        assert capability["ui_surface"]
        assert capability["service_api"]
        assert capability["test"]
        assert capability["evidence"]
        assert capability["configurable"] is True
        assert capability["agent_assisted"] is True


def test_improve1_feature_execution_plans_are_side_effect_free():
    for feature_number in (1, 25, 50):
        plan = plan_feature_execution(feature_number)
        assert plan["ok"] is True
        assert plan["feature_number"] == feature_number
        assert plan["side_effects"] == ()
        assert plan["model_artifacts"]
        assert plan["ui_artifacts"]
        assert plan["service_artifacts"]
