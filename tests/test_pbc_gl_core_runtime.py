import pytest

from pyAppGen.pbc import GL_CORE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import gl_core_append_ledger_event
from pyAppGen.pbc import gl_core_build_projection
from pyAppGen.pbc import gl_core_build_release_evidence
from pyAppGen.pbc import gl_core_build_schema_contract
from pyAppGen.pbc import gl_core_build_service_contract
from pyAppGen.pbc import gl_core_build_workbench_view
from pyAppGen.pbc import gl_core_chart_governance_contract
from pyAppGen.pbc import gl_core_configure_runtime
from pyAppGen.pbc import gl_core_empty_state
from pyAppGen.pbc import gl_core_open_accounting_period
from pyAppGen.pbc import gl_core_register_account
from pyAppGen.pbc import gl_core_register_journal
from pyAppGen.pbc import gl_core_register_rule
from pyAppGen.pbc import gl_core_register_schema_extension
from pyAppGen.pbc import gl_core_render_workbench
from pyAppGen.pbc import gl_core_runtime_capabilities
from pyAppGen.pbc import gl_core_runtime_smoke
from pyAppGen.pbc import gl_core_set_parameter
from pyAppGen.pbc import gl_core_transition_account_state
from pyAppGen.pbc import gl_core_transition_journal_state
from pyAppGen.pbc import gl_core_transition_period_state
from pyAppGen.pbc import gl_core_ui_contract
from pyAppGen.pbc import gl_core_verify_journal_invariants
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit
from pyAppGen.pbcs.gl_core import GL_CORE_ACCOUNT_LIFECYCLE_TRANSITIONS
from pyAppGen.pbcs.gl_core import GL_CORE_ACCOUNT_POSTABLE_STATES
from pyAppGen.pbcs.gl_core import GL_CORE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.gl_core import GL_CORE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.gl_core import GL_CORE_JOURNAL_LIFECYCLE_TRANSITIONS
from pyAppGen.pbcs.gl_core import GL_CORE_JOURNAL_SEALED_STATES
from pyAppGen.pbcs.gl_core import GL_CORE_OWNED_TABLES
from pyAppGen.pbcs.gl_core import GL_CORE_PERIOD_LIFECYCLE_TRANSITIONS
from pyAppGen.pbcs.gl_core import GL_CORE_PERIOD_TERMINAL_STATES
from pyAppGen.pbcs.gl_core import GL_CORE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.gl_core import gl_core_build_api_contract
from pyAppGen.pbcs.gl_core import gl_core_permissions_contract
from pyAppGen.pbcs.gl_core import gl_core_receive_event
from pyAppGen.pbcs.gl_core import gl_core_verify_owned_table_boundary
from pyAppGen.pbcs.gl_core import implementation_contract as gl_core_package_contract


def test_gl_core_runtime_executes_all_documented_advanced_capabilities() -> None:
    runtime = gl_core_runtime_capabilities()
    smoke = gl_core_runtime_smoke()
    package_contract = gl_core_package_contract()
    contract = pbc_implementation_contract("gl_core")
    api = gl_core_build_api_contract()
    schema = gl_core_build_schema_contract()
    service = gl_core_build_service_contract()
    release = gl_core_build_release_evidence()
    permissions = gl_core_permissions_contract()

    assert runtime["format"] == "appgen.gl-core-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/gl_core"
    assert runtime["owned_tables"] == GL_CORE_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 30
    assert runtime["allowed_database_backends"] == GL_CORE_ALLOWED_DATABASE_BACKENDS
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert "recurring_journals" in runtime["standard_features"]
    assert "currency_translation" in runtime["standard_features"]
    assert "electronic_audit_file" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(GL_CORE_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    assert package_contract["api_contract"]["event_contract"] == "AppGen-X"
    assert package_contract["permissions_contract"]["action_permissions"]["receive_event"] == "gl_core.event"
    assert package_contract["owned_tables"] == GL_CORE_OWNED_TABLES
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["allowed_database_backends"] == GL_CORE_ALLOWED_DATABASE_BACKENDS
    assert package_contract["required_event_topic"] == GL_CORE_REQUIRED_EVENT_TOPIC

    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "gl_core.event"
    assert contract["source_package"]["owned_tables"] == GL_CORE_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == GL_CORE_ALLOWED_DATABASE_BACKENDS
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "LedgerConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(GL_CORE_ADVANCED_CAPABILITY_KEYS)

    assert schema["ok"] is True
    assert len(schema["tables"]) == len(GL_CORE_OWNED_TABLES)
    assert len(schema["migrations"]) == len(GL_CORE_OWNED_TABLES)
    assert {"gl_core_ledger_account", "gl_core_accounting_period", "gl_core_audit_proof"} <= {
        item["table"] for item in schema["tables"]
    }
    assert all(item["table"].startswith("gl_core_") for item in schema["tables"])
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 20
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["ok"] is True
    assert not release["blocking_gaps"]

    assert api["owned_tables"] == GL_CORE_OWNED_TABLES
    assert api["shared_table_access"] is False
    assert api["event_contract"] == "AppGen-X"
    assert api["stream_engine_picker_visible"] is False
    assert any(route.get("command") == "receive_event" for route in api["routes"])
    assert set(api["consumes"]) == set(GL_CORE_CONSUMED_EVENT_TYPES)

    assert permissions["ok"] is True
    assert permissions["action_permissions"]["receive_event"] == "gl_core.event"

    assert pbc_implementation_release_audit(("gl_core",))["ok"] is True
    assert pbc_implemented_capability_audit(("gl_core",))["ok"] is True
    assert pbc_release_audit()["ok"] is True


def test_gl_core_runtime_handles_configuration_rules_parameters_and_idempotent_events() -> None:
    configured = gl_core_configure_runtime(
        gl_core_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_account_types": ("asset", "liability", "equity", "revenue", "expense"),
            "workbench_limit": 50,
        },
    )
    state = configured["state"]
    assert configured["configuration"]["event_contract"] == "AppGen-X"
    assert configured["configuration"]["allowed_database_backends"] == GL_CORE_ALLOWED_DATABASE_BACKENDS
    assert configured["configuration"]["stream_engine_picker_visible"] is False
    assert configured["configuration"]["user_selectable_event_contract"] is False
    assert configured["configuration"]["owned_tables"] == GL_CORE_OWNED_TABLES

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
    extension = gl_core_register_schema_extension(
        state,
        "gl_core_journal_event",
        {"confidence": "decimal", "valid_time": "datetime"},
    )
    assert extension["ok"] is True
    state = extension["state"]

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
    assert gl_core_build_projection(state, tenant="tenant_alpha")["source_event_count"] == 0

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
            "source_text": "customer invoice revenue cash",
        },
    )
    assert good["ok"] is True
    assert good["event"]["previous_hash"] == "GENESIS"
    assert good["outbox_event"]["topic"] == GL_CORE_REQUIRED_EVENT_TOPIC
    assert good["outbox_event"]["idempotency_key"] == "gl_core:JournalPosted:gl_evt_000001"

    source_event = {
        "event_id": "evt_invoice_1",
        "event_type": "InvoiceApproved",
        "payload": {"tenant": "tenant_alpha", "invoice_id": "inv_100", "amount": 100},
    }
    received = gl_core_receive_event(good["state"], source_event)
    assert received["ok"] is True
    assert received["duplicate"] is False
    assert received["handler"]["status"] == "processed"
    assert received["projection"]["invoice_id"] == "inv_100"
    assert len(received["state"]["inbox"]) == 1

    duplicate = gl_core_receive_event(received["state"], source_event)
    assert duplicate["ok"] is True
    assert duplicate["duplicate"] is True
    assert len(duplicate["state"]["inbox"]) == 1

    failing_event = {
        "event_id": "evt_tax_1",
        "event_type": "TaxCalculated",
        "payload": {"tenant": "tenant_alpha", "tax_record_id": "tax_100", "amount": 8},
    }
    retrying = gl_core_receive_event(received["state"], failing_event, simulate_failure=True)
    assert retrying["ok"] is False
    assert retrying["handler"]["status"] == "retrying"
    assert len(retrying["state"]["retry_evidence"]) == 1
    assert len(retrying["state"]["dead_letter"]) == 0

    dead_letter = gl_core_receive_event(retrying["state"], failing_event, simulate_failure=True)
    assert dead_letter["ok"] is False
    assert dead_letter["dead_lettered"] is True
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["retry_evidence"]) == 2
    assert len(dead_letter["state"]["dead_letter"]) == 1
    assert dead_letter["state"]["dead_letter"][0]["reason"] == "unsupported_or_failed_gl_core_event"

    projection = gl_core_build_projection(dead_letter["state"], tenant="tenant_alpha")
    assert projection["trial_balance"] == 0
    assert projection["balances"] == {"cash": 100.0, "revenue": -100.0}

    workbench = gl_core_build_workbench_view(dead_letter["state"], tenant="tenant_alpha")
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2
    assert workbench["outbox_count"] == 1
    assert workbench["inbox_count"] == 3
    assert workbench["dead_letter_count"] == 1
    assert workbench["retry_evidence_count"] == 2
    assert workbench["binding_evidence"]["owned_tables"] == GL_CORE_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False
    assert workbench["binding_evidence"]["configuration"]["user_selectable_event_contract"] is False

    ui_contract = gl_core_ui_contract()
    permissions = gl_core_permissions_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == GL_CORE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == GL_CORE_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["event_contract"] == "AppGen-X"
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == GL_CORE_OWNED_TABLES
    assert ui_contract["binding_evidence"]["shared_table_access"] is False

    rendered = gl_core_render_workbench(
        dead_letter["state"],
        tenant="tenant_alpha",
        principal_permissions=permissions["permissions"],
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 1
    assert rendered["inbox_count"] == 3
    assert rendered["dead_letter_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == GL_CORE_OWNED_TABLES
    assert rendered["binding_evidence"]["dead_letter_table"] == "gl_core_dead_letter_event"


def test_gl_core_chart_period_and_journal_lifecycles_gate_posting() -> None:
    state = _governed_state()

    # A new account is proposed, and proposed is not a posting target: the chart
    # cannot become a posting surface as a side effect of someone creating it.
    assert state["accounts"]["acct_cash"]["lifecycle_state"] == "proposed"
    assert state["accounts"]["acct_cash"]["normal_balance"] == "debit"
    assert state["accounts"]["acct_revenue"]["normal_balance"] == "credit"
    assert state["accounts"]["acct_deferred"]["lifecycle_state"] == "proposed"
    assert state["accounts"]["acct_deferred"]["hierarchy_depth"] == 0

    # `posting_blocked` is reachable from `active`, never from `proposed`, and the
    # refusal names the graph rather than only the target.
    guard = gl_core_transition_account_state(state, "acct_deferred", {"to_state": "posting_blocked"})
    assert guard["ok"] is False
    assert guard["reason"] == "invalid_transition"
    assert guard["allowed_transitions"] == ("active", "retired")

    assert gl_core_transition_account_state(state, "acct_missing", {"to_state": "active"})["reason"] == "unknown_account"

    state = gl_core_transition_account_state(state, "acct_cash", {"to_state": "active", "actor": "controller"})["state"]
    state = gl_core_transition_account_state(state, "acct_revenue", {"to_state": "active", "actor": "controller"})["state"]
    assert state["accounts"]["acct_cash"]["lifecycle_state"] in GL_CORE_ACCOUNT_POSTABLE_STATES
    assert len(state["account_lifecycle_transitions"]) == 2

    # The invariant engine reports every failure, not the first one. This journal
    # is unbalanced, names an account that does not exist, and lands in a period
    # nobody opened, so all three are named at once.
    everything_wrong = gl_core_verify_journal_invariants(
        state,
        {
            "journal_id": "jrn_everything_wrong",
            "tenant": "tenant_alpha",
            "period_id": "period_never_opened",
            "currency": "USD",
            "source_document_hash": "sha3:invoice-999",
            "lines": (
                {"account": "acct_cash", "debit": 500, "credit": 0},
                {"account": "acct_ghost", "debit": 0, "credit": 400},
            ),
        },
    )
    assert everything_wrong["ok"] is False
    assert everything_wrong["failed_invariants"] == ("balanced", "accounts_valid", "period_admissible")
    assert len(everything_wrong["invariants"]) == 6
    assert everything_wrong["proof_hash"]

    # A journal is not the ledger event it produces: drafting is mutable, posting
    # is not. `draft` cannot jump to `posted` at all.
    jump = gl_core_transition_journal_state(state, "jrn_1000", {"to_state": "posted", "actor": "controller"})
    assert jump["ok"] is False
    assert jump["reason"] == "invalid_transition"
    assert jump["allowed_transitions"] == ("validated", "rejected", "superseded")
    assert "remediation" not in jump

    state = gl_core_transition_journal_state(state, "jrn_1000", {"to_state": "validated", "actor": "preparer"})["state"]
    state = gl_core_transition_journal_state(state, "jrn_1000", {"to_state": "pending_approval", "actor": "preparer"})["state"]
    posting = gl_core_transition_journal_state(
        state, "jrn_1000", {"to_state": "posted", "actor": "controller", "reason": "month-end close"}
    )
    assert posting["ok"] is True, posting
    state = posting["state"]
    assert state["journals"]["jrn_1000"]["lifecycle_state"] == "posted"
    assert len(state["journals"]["jrn_1000"]["lifecycle_history"]) == 3
    # Posting is the only transition that writes a ledger event, and the proof
    # hash travels with it so a downstream projection can re-verify the fact.
    assert len(state["events"]) == 1
    assert posting["ledger_event"]["payload"]["invariant_proof"] == state["journals"]["jrn_1000"]["invariant_proof"]
    assert state["outbox"][-1]["event_type"] == "JournalPosted"

    # An unbalanced journal is refused at the posting edge, and the refusal names
    # the invariant that failed rather than the fact that something did.
    state = gl_core_transition_journal_state(state, "jrn_unbalanced", {"to_state": "validated", "actor": "preparer"})["state"]
    unbalanced = gl_core_transition_journal_state(state, "jrn_unbalanced", {"to_state": "posted", "actor": "controller"})
    assert unbalanced["ok"] is False
    assert unbalanced["reason"] == "invariant_violation"
    assert unbalanced["failed_invariants"] == ("balanced",)
    assert len(state["events"]) == 1

    # A journal that touches a proposed account fails the same way, for the other
    # half of `accounts_valid`.
    state = gl_core_transition_journal_state(state, "jrn_blocked_account", {"to_state": "validated", "actor": "preparer"})["state"]
    unpostable = gl_core_transition_journal_state(state, "jrn_blocked_account", {"to_state": "posted", "actor": "controller"})
    assert unpostable["ok"] is False
    assert unpostable["failed_invariants"] == ("accounts_valid",)
    assert unpostable["invariants"][1]["detail"]["not_postable"] == ("acct_deferred",)

    # A posted journal is sealed. Editing it is refused, and the refusal carries
    # the remediation rather than leaving the operator to guess.
    sealed = gl_core_transition_journal_state(state, "jrn_1000", {"to_state": "draft", "actor": "preparer"})
    assert sealed["ok"] is False
    assert sealed["allowed_transitions"] == ("reversed", "correcting")
    assert sealed["remediation"] == "post a correcting journal rather than editing a sealed one"

    # A correction is a new journal linked to the original, not a rewrite.
    correction = gl_core_transition_journal_state(
        state, "jrn_1000", {"to_state": "correcting", "actor": "controller", "reason": "restate revenue"}
    )
    assert correction["ok"] is True
    state = correction["state"]
    assert state["journals"]["jrn_1000"]["correction_of"] == "jrn_1000"
    assert state["journals"]["jrn_1000"]["lifecycle_state"] == "correcting"

    # Closing a period is gated on every journal in it being sealed. The refusal
    # names the journals, so the operator knows what to work, not just that work remains.
    blocked_close = gl_core_transition_period_state(
        state, "period_2026_05", {"to_state": "closed", "actor": "controller"}
    )
    assert blocked_close["ok"] is False
    assert blocked_close["reason"] == "unposted_journals"
    assert set(blocked_close["unposted_journals"]) == {"jrn_unbalanced", "jrn_blocked_account"}
    assert blocked_close["remediation"] == "post or reject every journal in the period before closing it"

    # `locked` is the state a controller freezes a period in while the close is
    # prepared. The same journal that passed `period_admissible` before now fails
    # it, which is what proves the lock bites.
    assert gl_core_verify_journal_invariants(state, state["journals"]["jrn_1000"])["failed_invariants"] == ()
    state = gl_core_transition_period_state(
        state, "period_2026_05", {"to_state": "locked", "actor": "controller", "reason": "prepare close"}
    )["state"]
    assert gl_core_verify_journal_invariants(state, state["journals"]["jrn_1000"])["failed_invariants"] == (
        "period_admissible",
    )

    # `closed` is terminal, so nothing leaves it.
    assert GL_CORE_PERIOD_LIFECYCLE_TRANSITIONS["closed"] == ()
    assert GL_CORE_PERIOD_TERMINAL_STATES == ("closed",)

    workbench = gl_core_build_workbench_view(state, tenant="tenant_alpha")
    assert workbench["chart_account_count"] == 3
    assert workbench["postable_account_count"] == 2
    assert dict(workbench["account_lifecycle_state_counts"])["proposed"] == 1
    assert workbench["journal_count"] == 3
    assert workbench["journal_lifecycle_state_counts"] == (
        ("correcting", 1),
        ("draft", 0),
        ("pending_approval", 0),
        ("posted", 0),
        ("rejected", 0),
        ("reversed", 0),
        ("superseded", 0),
        ("validated", 2),
    )
    assert workbench["unposted_journal_count"] == 2
    assert workbench["posted_journal_count"] == 0
    assert workbench["period_count"] == 1
    assert workbench["open_period_count"] == 0

    contract = gl_core_chart_governance_contract()
    assert contract["account_transitions"] == {
        state_name: targets for state_name, targets in GL_CORE_ACCOUNT_LIFECYCLE_TRANSITIONS.items()
    }
    assert contract["period_states"] == tuple(GL_CORE_PERIOD_LIFECYCLE_TRANSITIONS)
    assert contract["period_admissible_states"] == ("open",)
    assert contract["journal_sealed_states"] == GL_CORE_JOURNAL_SEALED_STATES
    assert contract["journal_transitions"] == {
        state_name: targets for state_name, targets in GL_CORE_JOURNAL_LIFECYCLE_TRANSITIONS.items()
    }
    assert len(contract["journal_invariants"]) == 6

    # The UI contract surfaces the same governance, so a screen can render the
    # lifecycle without reaching into the runtime module.
    ui = gl_core_ui_contract()
    assert ui["chart_governance"] == contract
    lifecycle_panels = tuple(panel for panel in ui["panels"] if panel["fragment"] == "JournalLifecycleConsole")
    assert len(lifecycle_panels) == 1
    assert "JournalLifecycleConsole" in ui["fragments"]
    assert "ChartOfAccountsConsole" in ui["fragments"]
    assert "/workbench/pbcs/gl_core/journals/lifecycle" in ui["routes"]
    assert "/workbench/pbcs/gl_core/chart-of-accounts" in ui["routes"]
    assert "/workbench/pbcs/gl_core/periods" in ui["routes"]
    assert ui["action_permissions"]["transition_journal_state"] == "gl_core.post"
    assert ui["action_permissions"]["transition_period_state"] == "gl_core.close"


def test_gl_core_rejects_invalid_chart_period_and_journal_inputs() -> None:
    state = gl_core_configure_runtime(
        gl_core_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
        },
    )["state"]

    with pytest.raises(ValueError, match="Missing GL account fields"):
        gl_core_register_account(state, {"account_id": "acct_partial", "tenant": "tenant_alpha"})

    with pytest.raises(ValueError, match="Unsupported GL account type"):
        gl_core_register_account(
            state,
            {"account_id": "acct_bad", "tenant": "tenant_alpha", "account_code": "9999", "account_type": "memo"},
        )

    with pytest.raises(ValueError, match="Missing GL period fields"):
        gl_core_open_accounting_period(state, {"period_id": "period_partial", "tenant": "tenant_alpha"})

    with pytest.raises(ValueError, match="GL period start must precede its end"):
        gl_core_open_accounting_period(
            state,
            {
                "period_id": "period_backwards",
                "tenant": "tenant_alpha",
                "fiscal_year": 2026,
                "starts_at": "2026-05-31T00:00:00Z",
                "ends_at": "2026-05-01T00:00:00Z",
            },
        )

    with pytest.raises(ValueError, match="Missing GL journal fields"):
        gl_core_register_journal(state, {"journal_id": "jrn_partial", "tenant": "tenant_alpha"})

    state = _governed_state()

    with pytest.raises(ValueError, match="GL account already exists"):
        gl_core_register_account(
            state,
            {"account_id": "acct_cash", "tenant": "tenant_alpha", "account_code": "1100", "account_type": "asset"},
        )

    with pytest.raises(ValueError, match="is already in use"):
        gl_core_register_account(
            state,
            {"account_id": "acct_cash_2", "tenant": "tenant_alpha", "account_code": "1000", "account_type": "asset"},
        )

    with pytest.raises(ValueError, match="GL account parent does not exist"):
        gl_core_register_account(
            state,
            {
                "account_id": "acct_orphan",
                "tenant": "tenant_alpha",
                "account_code": "1200",
                "account_type": "asset",
                "parent_account_id": "acct_nowhere",
            },
        )

    with pytest.raises(ValueError, match="GL period already exists"):
        gl_core_open_accounting_period(
            state,
            {
                "period_id": "period_2026_05",
                "tenant": "tenant_alpha",
                "fiscal_year": 2026,
                "starts_at": "2026-05-01T00:00:00Z",
                "ends_at": "2026-05-31T23:59:59Z",
            },
        )

    # A tenant cannot hold two open periods covering the same day: a journal would
    # then have two admissible windows and `period_admissible` would be ambiguous.
    with pytest.raises(ValueError, match="overlaps an existing period"):
        gl_core_open_accounting_period(
            state,
            {
                "period_id": "period_2026_05b",
                "tenant": "tenant_alpha",
                "fiscal_year": 2026,
                "starts_at": "2026-05-15T00:00:00Z",
                "ends_at": "2026-06-15T00:00:00Z",
            },
        )

    with pytest.raises(ValueError, match="GL journal already exists"):
        gl_core_register_journal(
            state,
            {
                "journal_id": "jrn_1000",
                "tenant": "tenant_alpha",
                "period_id": "period_2026_05",
                "lines": ({"account": "acct_cash", "debit": 1, "credit": 0},),
            },
        )

    assert gl_core_transition_journal_state(state, "jrn_missing", {"to_state": "validated"})["reason"] == "unknown_journal"
    assert gl_core_transition_period_state(state, "period_missing", {"to_state": "locked"})["reason"] == "unknown_period"
    assert (
        gl_core_transition_period_state(state, "period_2026_05", {"to_state": "reopened"})["reason"]
        == "invalid_transition"
    )


def _governed_state() -> dict:
    state = gl_core_configure_runtime(
        gl_core_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_account_types": ("asset", "liability", "equity", "revenue", "expense"),
            "workbench_limit": 50,
        },
    )["state"]
    for account in (
        {"account_id": "acct_cash", "tenant": "tenant_alpha", "account_code": "1000", "account_type": "asset"},
        {"account_id": "acct_revenue", "tenant": "tenant_alpha", "account_code": "4000", "account_type": "revenue"},
        {"account_id": "acct_deferred", "tenant": "tenant_alpha", "account_code": "2100", "account_type": "liability"},
    ):
        state = gl_core_register_account(state, account)["state"]
    state = gl_core_open_accounting_period(
        state,
        {
            "period_id": "period_2026_05",
            "tenant": "tenant_alpha",
            "fiscal_year": 2026,
            "starts_at": "2026-05-01T00:00:00Z",
            "ends_at": "2026-05-31T23:59:59Z",
        },
    )["state"]
    for journal in (
        {
            "journal_id": "jrn_1000",
            "tenant": "tenant_alpha",
            "period_id": "period_2026_05",
            "valid_at": "2026-05-25T00:00:00Z",
            "source_document_hash": "sha3:invoice-100",
            "lines": (
                {"account": "acct_cash", "debit": 1200, "credit": 0},
                {"account": "acct_revenue", "debit": 0, "credit": 1200},
            ),
        },
        {
            "journal_id": "jrn_unbalanced",
            "tenant": "tenant_alpha",
            "period_id": "period_2026_05",
            "source_document_hash": "sha3:invoice-101",
            "lines": (
                {"account": "acct_cash", "debit": 500, "credit": 0},
                {"account": "acct_revenue", "debit": 0, "credit": 400},
            ),
        },
        {
            "journal_id": "jrn_blocked_account",
            "tenant": "tenant_alpha",
            "period_id": "period_2026_05",
            "source_document_hash": "sha3:invoice-102",
            "lines": (
                {"account": "acct_cash", "debit": 10, "credit": 0},
                {"account": "acct_deferred", "debit": 0, "credit": 10},
            ),
        },
    ):
        state = gl_core_register_journal(state, journal)["state"]
    return state


def test_gl_core_rejects_invalid_runtime_inputs_and_proves_owned_table_boundary() -> None:
    with pytest.raises(ValueError, match="GL Core supports only PostgreSQL, MySQL, or MariaDB backends"):
        gl_core_configure_runtime(
            gl_core_empty_state(),
            {
                "database_backend": "sqlite",
                "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="GL Core uses the AppGen-X event contract"):
        gl_core_configure_runtime(
            gl_core_empty_state(),
            {
                "database_backend": "postgresql",
                "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "stream_engine": "nats",
            },
        )

    with pytest.raises(ValueError, match="GL Core requires AppGen-X event topic"):
        gl_core_configure_runtime(
            gl_core_empty_state(),
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.gl.other",
                "retry_limit": 2,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    state = gl_core_configure_runtime(
        gl_core_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "default_timezone": "UTC",
        },
    )["state"]

    with pytest.raises(ValueError, match="Unsupported GL Core parameter"):
        gl_core_set_parameter(state, "unexpected_limit", 1)

    with pytest.raises(ValueError, match="Missing required GL rule fields"):
        gl_core_register_rule(state, {"rule_id": "rule_bad", "tenant": "tenant_alpha"})

    with pytest.raises(ValueError, match="GL Core schema extensions must target owned tables"):
        gl_core_register_schema_extension(state, "customer_profile", {"risk_score": "decimal"})

    invalid_extension = gl_core_register_schema_extension(
        state,
        "gl_core_journal_event",
        {"Confidence": "decimal"},
    )
    assert invalid_extension["ok"] is False
    assert invalid_extension["error"] == "invalid_extension_field"

    boundary = gl_core_verify_owned_table_boundary(
        (
            "gl_core_journal_event",
            "gl_core_journal_line",
            "gl_core_account_projection",
            "gl_core_appgen_outbox_event",
            "gl_core_appgen_inbox_event",
            "gl_core_dead_letter_event",
            "invoice_approval_projection",
            "InvoiceApproved",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == GL_CORE_OWNED_TABLES
    assert boundary["shared_table_access"] is False
    assert boundary["declared_dependencies"]["shared_tables"] == ()

    bad_boundary = gl_core_verify_owned_table_boundary(("gl_core_journal_event", "shared_customer"))
    assert bad_boundary["ok"] is False
    assert bad_boundary["violations"] == ("shared_customer",)

    api = gl_core_build_api_contract()
    assert api["shared_table_access"] is False
    assert api["owned_tables"] == GL_CORE_OWNED_TABLES
    assert api["event_contract"] == "AppGen-X"
    assert any(route.get("command") == "receive_event" for route in api["routes"])
    assert all(
        set(route.get("owned_tables", ())).issubset(set(GL_CORE_OWNED_TABLES))
        for route in api["routes"]
        if route.get("command") != "receive_event"
    )
