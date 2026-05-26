import importlib

from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS


def test_every_pbc_has_domain_specific_rules_parameters_and_configuration() -> None:
    for key in IMPLEMENTED_PBC_KEYS:
        config = importlib.import_module(f"pyAppGen.pbcs.{key}.config")

        configuration = config.configuration_manifest()
        parameters = config.parameter_manifest()
        rules = config.rule_manifest()
        governance = config.governance_smoke_test()

        assert configuration["ok"] is True
        assert parameters["ok"] is True
        assert rules["ok"] is True
        assert governance["ok"] is True
        assert len(configuration["domain_parameter_schema"]) >= 4
        assert len(configuration["domain_rule_schema"]) >= 4
        assert {item["scope"] for item in configuration["domain_parameter_schema"]} >= {
            "domain",
            "advanced",
            "workflow",
            "data_boundary",
        }
        assert {item["condition"] for item in configuration["domain_rule_schema"]} >= {
            "capability_available",
            "workflow_declared",
            "owned_table_boundary",
        }

        for parameter in configuration["domain_parameter_schema"]:
            accepted = config.set_parameter({}, parameter["key"], parameter["default"])
            assert accepted["ok"] is True
            assert accepted["parameter_scope"] == parameter["scope"]

        for rule in configuration["domain_rule_schema"]:
            compiled = config.compile_rule(rule)
            decision = config.evaluate_rule(compiled, {"tenant": "tenant-smoke"})
            assert compiled["ok"] is True
            assert decision["ok"] is True
            assert decision["allowed"] is True
            assert decision["scope"] == rule["scope"]


def test_pbc_rule_compilers_reject_stream_engine_pickers() -> None:
    for key in IMPLEMENTED_PBC_KEYS:
        config = importlib.import_module(f"pyAppGen.pbcs.{key}.config")
        rule = dict(config.configuration_manifest()["domain_rule_schema"][0])
        rule["stream_engine"] = "user_selected_stream_runtime"

        rejected = config.compile_rule(rule)

        assert rejected == {
            "ok": False,
            "compiled": False,
            "reason": "stream_engine_picker_disallowed",
            "side_effects": (),
        }
