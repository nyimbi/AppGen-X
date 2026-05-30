"""Runtime semantic checks for improve1 capability coverage."""

from importlib import import_module

from ..improve1_capabilities import capability_registry, plan_feature_execution

PBC_PACKAGE = __package__.rsplit(".", 1)[0]
agent = import_module(f"{PBC_PACKAGE}.agent")
release_evidence = import_module(f"{PBC_PACKAGE}.release_evidence")
services = import_module(f"{PBC_PACKAGE}.services")
ui = import_module(f"{PBC_PACKAGE}.ui")


def _call_first(module, names):
    for name in names:
        fn = getattr(module, name, None)
        if callable(fn):
            try:
                return name, fn()
            except TypeError:
                continue
    raise AssertionError(f"no callable smoke surface found on {module.__name__}")


def _assert_ok_result(surface, result):
    assert isinstance(result, dict), surface
    assert result.get("ok") is True, surface
    assert result.get("side_effects", ()) in ((), [], None)


def test_improve1_registry_is_bound_to_executable_pbc_surfaces():
    registry = capability_registry()
    assert registry["ok"] is True
    service_name, service_result = _call_first(services, ("smoke_test", "service_operation_manifest", "service_operation_contracts"))
    ui_name, ui_result = _call_first(ui, ("smoke_test",))
    release_name, release_result = _call_first(release_evidence, ("smoke_test", "release_readiness_manifest", "validate_release_evidence", "build_release_evidence"))
    agent_name, agent_result = _call_first(agent, ("smoke_test", "composed_agent_contribution", "agent_skill_manifest"))

    _assert_ok_result(f"services.{service_name}", service_result)
    _assert_ok_result(f"ui.{ui_name}", ui_result)
    _assert_ok_result(f"release_evidence.{release_name}", release_result)
    _assert_ok_result(f"agent.{agent_name}", agent_result)

    for feature_number in (1, 10, 25, 40, 50):
        plan = plan_feature_execution(feature_number)
        assert plan["ok"] is True
        assert plan["side_effects"] == ()
        assert "services.py" in plan["service_artifacts"] or "routes.py" in plan["service_artifacts"]
        assert "ui.py" in plan["ui_artifacts"]
        assert "release_evidence.py" in plan["evidence_artifacts"]


def test_all_improve1_capabilities_expose_runtime_surface_classes():
    registry = capability_registry()
    assert registry["capability_count"] == 50
    for capability in registry["capabilities"]:
        assert capability["code_artifact_model"]
        assert capability["ui_surface"]
        assert capability["service_api"]
        assert capability["test"]
        assert capability["evidence"]
        assert capability["side_effect_free_plan"] is True
