from pyAppGen.pbc import GL_CORE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import gl_core_append_ledger_event
from pyAppGen.pbc import gl_core_build_projection
from pyAppGen.pbc import gl_core_build_workbench_view
from pyAppGen.pbc import gl_core_configure_runtime
from pyAppGen.pbc import gl_core_empty_state
from pyAppGen.pbc import gl_core_register_rule
from pyAppGen.pbc import gl_core_render_workbench
from pyAppGen.pbc import gl_core_runtime_capabilities
from pyAppGen.pbc import gl_core_runtime_smoke
from pyAppGen.pbc import gl_core_set_parameter
from pyAppGen.pbc import gl_core_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit


def test_gl_core_runtime_executes_all_documented_advanced_capabilities() -> None:
    runtime = gl_core_runtime_capabilities()
    smoke = gl_core_runtime_smoke()

    assert runtime["format"] == "appgen.gl-core-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/gl_core"
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(GL_CORE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("gl_core")
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "LedgerConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(GL_CORE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("gl_core",))["ok"] is True
    assert pbc_implemented_capability_audit(("gl_core",))["ok"] is True
    assert pbc_release_audit()["ok"] is True


def test_gl_core_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = gl_core_empty_state()
    state = gl_core_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.gl.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_account_types": ("asset", "liability", "equity", "revenue", "expense"),
            "workbench_limit": 50,
        },
    )["state"]
    state = gl_core_set_parameter(state, "approval_threshold", 1000)["state"]
    state = gl_core_set_parameter(state, "materiality_threshold", 0.05)["state"]
    state = gl_core_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_alpha",
            "scope": "journal_posting",
            "requires_balance": True,
            "requires_approval_over": 1000,
            "status": "active",
        },
    )["state"]
    bad = gl_core_append_ledger_event(
        state,
        "JournalPosted",
        {
            "tenant": "tenant_alpha",
            "lines": (
                {"account": "cash", "debit": 100, "credit": 0},
                {"account": "revenue", "debit": 0, "credit": 90},
            ),
        },
    )
    assert bad["ok"] is False
    assert gl_core_build_projection(state)["source_event_count"] == 0

    good = gl_core_append_ledger_event(
        state,
        "JournalPosted",
        {
            "tenant": "tenant_alpha",
            "valid_at": "2026-05-25T00:00:00Z",
            "lines": (
                {"account": "cash", "debit": 100, "credit": 0},
                {"account": "revenue", "debit": 0, "credit": 100},
            ),
        },
    )
    assert good["ok"] is True
    assert good["event"]["previous_hash"] == "GENESIS"
    assert good["outbox_event"]["idempotency_key"] == "gl_core:JournalPosted:gl_evt_000001"

    projection = gl_core_build_projection(good["state"], tenant="tenant_alpha")
    assert projection["trial_balance"] == 0
    assert projection["balances"] == {"cash": 100.0, "revenue": -100.0}

    workbench = gl_core_build_workbench_view(good["state"], tenant="tenant_alpha")
    assert workbench["event_count"] == 1
    assert workbench["account_count"] == 2
    assert workbench["trial_balance"] == 0
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2

    ui_contract = gl_core_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "approval_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = gl_core_render_workbench(
        good["state"],
        tenant="tenant_alpha",
        principal_permissions=(
            "gl_core.post",
            "gl_core.read",
            "gl_core.close",
            "gl_core.reconcile",
            "gl_core.audit",
            "gl_core.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
