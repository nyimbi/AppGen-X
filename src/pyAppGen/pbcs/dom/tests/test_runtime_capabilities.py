"""Executable runtime capability proofs for the dom PBC."""

import pytest

from .. import config, runtime, ui


PBC_KEY = "dom"
ALLOWED_BACKENDS = ("postgresql", "mysql", "mariadb")
CORE_STANDARD_FEATURES = {
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "workbench",
    "retry_dead_letter_evidence",
    "idempotent_handlers",
}
ADVANCED_TERMS = (
    "event_sourced",
    "graph_relational",
    "multi_tenant",
    "probabilistic",
    "carbon_aware",
    "stochastic",
)


def _call(name, *args, **kwargs):
    return getattr(runtime, f"{PBC_KEY}_{name}")(*args, **kwargs)


def _configuration():
    return {
        "database_backend": "postgresql",
        "event_topic": getattr(runtime, "DOM_REQUIRED_EVENT_TOPIC"),
        "retry_limit": 3,
    }


def test_runtime_smoke_covers_standard_and_advanced_capabilities():
    smoke = _call("runtime_smoke")
    capabilities = _call("runtime_capabilities")
    capability_ids = set(capabilities["capabilities"])

    assert smoke["ok"] is True
    assert len(smoke["checks"]) >= 25
    assert not smoke["blocking_gaps"]
    assert capabilities["ok"] is True
    assert CORE_STANDARD_FEATURES <= set(capabilities["standard_features"])
    assert all(any(term in item for item in capability_ids) for term in ADVANCED_TERMS)


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
    assert service["transaction_boundary"].endswith("owned_datastore_plus_appgen_outbox")
    assert not service["external_dependencies"]["shared_tables"]
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
    configured = _call("configure_runtime", state, _configuration())
    parameter = _call("set_parameter", configured["state"], "workbench_limit", 25)
    compiled_rule = config.compile_rule(config.RULE_SCHEMA[0])
    rule_decision = config.evaluate_rule(
        compiled_rule,
        {"tenant": "tenant_alpha", "database_backend": "postgresql", "event_contract": "AppGen-X"},
    )
    ui_smoke = ui.smoke_test()

    assert configured["configuration"]["event_contract"] == "AppGen-X"
    assert configured["configuration"]["stream_engine_picker_visible"] is False
    assert configured["configuration"]["allowed_database_backends"] == ALLOWED_BACKENDS
    assert parameter["ok"] is True
    assert config.set_parameter({}, "retry_limit", 3)["accepted"] is True
    assert config.compile_rule({"rule_id": "bad", "condition": "tenant_present", "effect": "allow_when_true", "stream_engine": "picker"})["ok"] is False
    assert compiled_rule["compiled"] is True
    assert rule_decision["allowed"] is True
    assert ui_smoke["ok"] is True
    assert ui_smoke["manifest"]["fragments"]
    assert ui_smoke["manifest"]["routes"]
    assert ui_smoke["rendered"]["cards"]
    assert ui_smoke["rendered"]["configuration_bound"] is True
    assert ui_smoke["rendered"]["binding_evidence"]["owned_tables"]

    with pytest.raises(ValueError):
        _call("configure_runtime", state, {**_configuration(), "stream_engine": "picker"})
