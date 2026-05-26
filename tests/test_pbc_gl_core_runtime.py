import pytest

from pyAppGen.pbc import GL_CORE_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import gl_core_append_ledger_event
from pyAppGen.pbc import gl_core_build_projection
from pyAppGen.pbc import gl_core_build_release_evidence
from pyAppGen.pbc import gl_core_build_schema_contract
from pyAppGen.pbc import gl_core_build_service_contract
from pyAppGen.pbc import gl_core_build_workbench_view
from pyAppGen.pbc import gl_core_configure_runtime
from pyAppGen.pbc import gl_core_empty_state
from pyAppGen.pbc import gl_core_register_rule
from pyAppGen.pbc import gl_core_register_schema_extension
from pyAppGen.pbc import gl_core_render_workbench
from pyAppGen.pbc import gl_core_runtime_capabilities
from pyAppGen.pbc import gl_core_runtime_smoke
from pyAppGen.pbc import gl_core_set_parameter
from pyAppGen.pbc import gl_core_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import pbc_release_audit
from pyAppGen.pbcs.gl_core import GL_CORE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.gl_core import GL_CORE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.gl_core import GL_CORE_OWNED_TABLES
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
