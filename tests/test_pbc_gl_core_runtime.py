from pyAppGen.pbc import GL_CORE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import gl_core_append_ledger_event
from pyAppGen.pbc import gl_core_build_projection
from pyAppGen.pbc import gl_core_empty_state
from pyAppGen.pbc import gl_core_runtime_capabilities
from pyAppGen.pbc import gl_core_runtime_smoke
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit


def test_gl_core_runtime_executes_all_documented_advanced_capabilities() -> None:
    runtime = gl_core_runtime_capabilities()
    smoke = gl_core_runtime_smoke()

    assert runtime["format"] == "appgen.gl-core-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/gl_core"
    assert smoke["ok"] is True
    assert set(GL_CORE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("gl_core")
    assert contract["advanced_runtime"]["ok"] is True
    assert set(contract["advanced_runtime"]["capabilities"]) == set(GL_CORE_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("gl_core",))["ok"] is True
    assert pbc_release_audit()["ok"] is True


def test_gl_core_runtime_is_event_sourced_and_rejects_unbalanced_journals() -> None:
    state = gl_core_empty_state()
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
