"""Executable runtime capability proofs for the workflow_orchestration PBC."""

import pytest

from .. import config, runtime, ui


PBC_KEY = "workflow_orchestration"
ALLOWED_BACKENDS = ("postgresql", "mysql", "mariadb")


def _call(name, *args, **kwargs):
    return getattr(runtime, f"{PBC_KEY}_{name}")(*args, **kwargs)


def test_runtime_smoke_covers_standard_and_advanced_capabilities():
    smoke = _call("runtime_smoke")
    capabilities = _call("runtime_capabilities")
    check_ids = {check["id"] for check in smoke["checks"]}

    assert smoke["ok"] is True
    assert len(smoke["checks"]) >= 30
    assert not smoke["blocking_gaps"]
    assert capabilities["ok"] is True
    assert len(capabilities["standard_features"]) >= 10
    declared = set(capabilities["capabilities"]) | set(capabilities["standard_features"])
    assert declared >= {
        "configuration_schema",
        "rule_engine",
        "parameter_engine",
        "workbench",
    }
    assert {"retry_dead_letter", "retry_dead_letter_evidence"} & declared
    assert any("event_sourced" in item for item in check_ids)
    assert any("graph_relational" in item for item in check_ids)
    assert any("multi_tenant" in item for item in check_ids)
    assert any("probabilistic" in item for item in check_ids)
    assert any("zero_knowledge" in item for item in check_ids)
    assert any("carbon_aware" in item for item in check_ids)
    assert any("stochastic" in item for item in check_ids)


def test_contracts_enforce_owned_boundary_appgen_eventing_and_backend_allowlist():
    schema = _call("build_schema_contract")
    service = _call("build_service_contract")
    api = _call("build_api_contract")
    release = _call("build_release_evidence")
    boundary = _call("verify_owned_table_boundary", ("foreign_operational_table",))

    assert schema["ok"] is True
    assert tuple(schema["datastore_backends"]) == ALLOWED_BACKENDS
    assert schema["shared_table_access"] is False
    assert service["ok"] is True
    assert service["command_methods"]
    assert service["query_methods"]
    if service.get("eventing"):
        assert service["eventing"]["contract"] == "AppGen-X"
        assert service["eventing"]["stream_engine_picker_visible"] is False
    if service.get("rules_parameters_configuration"):
        assert {"register_rule", "set_parameter", "configure_runtime"} <= set(service["rules_parameters_configuration"])
    assert service["retry_dead_letter_evidence"]["dead_letter_table"].startswith(f"{PBC_KEY}_")
    assert api["ok"] is True
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert api["shared_table_access"] is False
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_operational_table",)


def test_configuration_rules_parameters_and_ui_are_executable():
    state = _call("empty_state")
    configured = _call(
        "configure_runtime",
        state,
        {
            "database_backend": "postgresql",
            "event_topic": getattr(runtime, "WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC"),
            "retry_limit": 3,
        },
    )
    parameter = _call("set_parameter", configured["state"], "default_retry_limit", 4)
    compiled_rule = config.compile_rule(config.RULE_SCHEMA[0])
    rule_decision = config.evaluate_rule(
        compiled_rule,
        {"tenant": "tenant_alpha", "database_backend": "postgresql", "event_contract": "AppGen-X"},
    )
    ui_smoke = ui.smoke_test()
    ui_contract = ui.workflow_orchestration_ui_contract()

    assert configured["configuration"]["event_contract"] == "AppGen-X"
    assert configured["configuration"]["stream_engine_picker_visible"] is False
    assert configured["configuration"]["allowed_database_backends"] == ALLOWED_BACKENDS
    assert parameter["ok"] is True
    assert compiled_rule["compiled"] is True
    assert rule_decision["allowed"] is True
    assert config.set_parameter({}, "retry_limit", 3)["accepted"] is True
    assert config.compile_rule({"rule_id": "bad", "condition": "tenant_present", "effect": "allow_when_true", "stream_engine": "picker"})["ok"] is False
    assert ui_smoke["ok"] is True
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["parameter_editor"]
    assert ui_contract["rule_editor"]

    with pytest.raises(ValueError):
        _call(
            "configure_runtime",
            state,
            {
                "database_backend": "postgresql",
                "event_topic": getattr(runtime, "WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC"),
                "stream_engine": "picker",
            },
        )
