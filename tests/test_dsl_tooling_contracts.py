import json
import subprocess
import sys
from pathlib import Path

from pyAppGen.dsl import format_report_dsl
from pyAppGen.dsl import designer_sync_report_dsl
from pyAppGen.dsl import diagnostic_catalog_dsl
from pyAppGen.dsl import diagnostic_fixture_audit_dsl
from pyAppGen.dsl import doctor_report_dsl
from pyAppGen.dsl import graph_report_dsl
from pyAppGen.dsl import graph_suite_report_dsl
from pyAppGen.dsl import generate_report_dsl
from pyAppGen.dsl import lint_report_dsl
from pyAppGen.dsl import lsp_service_dsl
from pyAppGen.dsl import migration_plan_dsl
from pyAppGen.dsl import nl_plan_dsl
from pyAppGen.dsl import pbc_publish_report
from pyAppGen.dsl import pbc_verifier_report
from pyAppGen.dsl import release_verifier_report_dsl
from pyAppGen.dsl import semantic_drift_audit_dsl
from pyAppGen.dsl import semantic_model_dsl
from pyAppGen.dsl import validate_report_dsl


TOOLING_SAMPLE = """
app FinanceOps { targets: web, mobile, desktop }

table Customer {
  id: int pk
  name: string required search
}

table Invoice {
  id: int pk
  customer_id: int -> Customer.id [many-to-one]
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
  lookup customer_name (customer.name)
}

view InvoiceForm for Invoice {
  Main: customer.name, total
  @ customer.name Lookup 0 0 6 1
  on Save -> SubmitInvoice
}

flow SubmitInvoice {
  draft -> reviewed
  reviewed -> posted
  human Review assigned Accountant -> reviewed
  timer reviewed "P2D" -> escalated
  compensate posted -> ReverseInvoice
}

composition FinanceSuite {
  include pbc gl_core version 1.0.0
  require database postgresql
}
"""

RELEASE_SAMPLE = """
app ReleaseDemo { targets: web, mobile, desktop }

table Invoice {
  id: int pk
  total: decimal
}

view InvoiceForm for Invoice {
  Main: id, total
}

operation SubmitInvoice {
  draft -> done
}

menu MainMenu {
  on Open -> SubmitInvoice
}

package ReleaseMobile {
  target: mobile
  signing: yes
  offline: yes
  permission: camera, explained
  smoke: launch
}

package ReleaseDesktop {
  target: desktop
  format: installer
  splash: declared
  menu_ref: MainMenu
  smoke: launch
}

test ReleaseSmoke {
  run happy_path -> SubmitInvoice
}

composition FinanceSuite {
  include pbc gl_core version 1.0.0
}

deploy Production {
  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
  resource SubmitInvoice cpu 1
  env SubmitInvoice DATABASE_URL
}
"""


def _position_of(source: str, token: str) -> dict:
    index = source.index(token)
    line = source.count("\n", 0, index)
    previous_newline = source.rfind("\n", 0, index)
    character = index if previous_newline < 0 else index - previous_newline - 1
    return {"line": line, "character": character}


def test_semantic_model_exposes_spec_contract_for_tables_views_flows_and_pbcs() -> None:
    model = semantic_model_dsl(TOOLING_SAMPLE, source_name="finance.appgen")

    assert model["format"] == "appgen.semantic-model.v1"
    assert model["ok"] is True
    assert model["app"]["targets"] == ("web", "mobile", "desktop")
    assert model["tables"]["Invoice"]["fields"]["customer_id"]["relationship"]["alias"] == "customer"
    assert model["tables"]["Invoice"]["lookup_paths"]["customer.name"]["valid"] is True
    assert model["views"]["InvoiceForm"]["components"][0]["binding"] == "customer.name"
    assert model["flows"]["SubmitInvoice"]["human_tasks"][0]["assignee"] == "Accountant"
    assert model["composition"]["FinanceSuite"]["includes"][0]["pbc"] == "gl_core"
    assert model["pbcs"]["gl_core"]["catalog_resolved"] is True
    assert "table.Invoice.customer_id" in model["symbols"]


def test_lint_report_maps_existing_linter_errors_to_stable_agx_diagnostics() -> None:
    source = """
    app Bad { targets: web }
    table Customer { id: int pk; name: string }
    table Invoice { id: int pk; customer_id: int -> Customer.id }
    view InvoiceForm for Invoice { Main: customer.missing_name }
    """

    report = lint_report_dsl(source, source_name="bad.appgen")

    assert report["format"] == "appgen.lint-report.v1"
    assert report["ok"] is False
    assert report["severity_counts"]["error"] >= 1
    assert any(item["code"] == "AGX0303" for item in report["diagnostics"])
    assert any(item["legacy_code"] == "unresolved_lookup_path" for item in report["diagnostics"])


def test_format_validate_and_graph_reports_follow_tooling_contracts() -> None:
    formatted = format_report_dsl(TOOLING_SAMPLE, source_name="finance.appgen")
    validation = validate_report_dsl(formatted["text"], source_name="finance.appgen")
    graph = graph_report_dsl(formatted["text"], source_name="finance.appgen", kind="er")

    assert formatted["format"] == "appgen.format-result.v1"
    assert formatted["idempotent"] is True
    assert validation["format"] == "appgen.validate-report.v1"
    assert validation["ok"] is True
    assert graph["format"] == "appgen.graph-report.v1"
    assert graph["graph"]["edges"][0]["from"] == "Invoice"


def test_formatter_preserves_comments_and_orders_field_modifiers() -> None:
    source = """
// file header
app FormatDemo { targets: web }

// customer table
table Customer {
  // identity comment
  id: int search default 0 required pk unique hidden // inline identity
  name: string search unique required
  parent_id: int search default 0 required -> Customer.id [many-to-one]
}

view CustomerForm for Customer { Main: name, parent.name }
"""

    report = format_report_dsl(source, source_name="format.appgen")
    second = format_report_dsl(report["text"], source_name="format.appgen")

    assert report["format"] == "appgen.format-result.v1"
    assert report["idempotent"] is True
    assert second["text"] == report["text"]
    assert report["text"].startswith("// file header\napp FormatDemo")
    assert "\n// customer table\ntable Customer" in report["text"]
    assert "  // identity comment\n  id: int pk required unique hidden search default 0 // inline identity" in report["text"]
    assert "  name: string required unique search" in report["text"]
    assert "  parent_id: int required search default 0 -> Customer.id [many-to-one]" in report["text"]


def test_graph_suite_report_covers_required_kinds_and_formats() -> None:
    report = graph_suite_report_dsl(RELEASE_SAMPLE, source_name="release.appgen")

    assert report["format"] == "appgen.graph-suite-report.v1"
    assert report["ok"] is True
    assert set(report["graph_reports"]) == {
        "er",
        "lookup",
        "workflow",
        "handler",
        "pbc",
        "security",
        "agent",
        "deployment",
        "package",
    }
    assert all(set(outputs) == {"json", "mermaid", "dot"} for outputs in report["renderings"].values())
    assert report["renderings"]["er"]["json"].startswith("{")
    assert report["renderings"]["workflow"]["mermaid"].startswith("graph TD")
    assert report["renderings"]["deployment"]["dot"].startswith("digraph appgen")


def test_appgen_lint_subcommand_emits_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "finance.appgen"
    path.write_text(TOOLING_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lint", str(path), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.lint-report.v1"
    assert payload["ok"] is True


def test_appgen_graph_suite_subcommand_emits_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "release.appgen"
    path.write_text(RELEASE_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "graph-suite", str(path), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.graph-suite-report.v1"
    assert payload["formats"] == ["json", "mermaid", "dot"]
    assert payload["renderings"]["package"]["dot"].startswith("digraph appgen")


def test_migration_plan_detects_add_drop_type_and_backfill_changes() -> None:
    previous = """
    app FinanceOps { targets: web }
    table Customer { id: int pk; name: string required }
    table Invoice { id: int pk; total: decimal default 0; note: string }
    """
    current = """
    app FinanceOps { targets: web }
    table Customer { id: int pk; name: string required; segment: string required }
    table Invoice { id: int pk; total: string default 0 }
    table CreditMemo { id: int pk; amount: decimal default 0 }
    """

    plan = migration_plan_dsl(previous, current, backend="postgresql")

    assert plan["format"] == "appgen.migration-plan.v1"
    assert plan["ok"] is True
    assert plan["destructive"] is True
    assert plan["requires_approval"] is True
    assert {change["kind"] for change in plan["changes"]} >= {
        "add_table",
        "add_field",
        "drop_field",
        "type_change",
    }
    assert any(change.get("requires_backfill") for change in plan["changes"])
    assert any(item["code"] == "AGX1101" for item in plan["diagnostics"])


def test_migration_plan_detects_index_check_and_pbc_ownership_transfer_changes() -> None:
    previous = """
    app FinanceOps { targets: web }
    table Invoice {
      id: int pk
      total: decimal
      index(total)
      constraint(total_positive, total)
    }
    pbc Billing { owns: Invoice }
    """
    current = """
    app FinanceOps { targets: web }
    table Invoice {
      id: int pk
      total: decimal
      unique(total)
      index(id)
      constraint(non_negative_total, total)
    }
    pbc Finance { owns: Invoice }
    """

    plan = migration_plan_dsl(previous, current, backend="postgresql")
    changes = {change["kind"]: change for change in plan["changes"]}

    assert plan["format"] == "appgen.migration-plan.v1"
    assert plan["ok"] is True
    assert plan["destructive"] is True
    assert {
        "add_index",
        "drop_index",
        "add_check",
        "drop_check",
        "add_unique_constraint",
        "pbc_ownership_transfer",
    } <= set(changes)
    assert changes["pbc_ownership_transfer"]["from"] == "Billing"
    assert changes["pbc_ownership_transfer"]["to"] == "Finance"
    assert changes["pbc_ownership_transfer"]["requires_approval"] is True


def test_nl_plan_returns_linted_dsl_patch_and_migration_preview() -> None:
    plan = nl_plan_dsl(
        TOOLING_SAMPLE,
        prompt="Add credit memos to accounts receivable",
        source_name="finance.appgen",
    )

    assert plan["format"] == "appgen.nl-plan.v1"
    assert plan["ok"] is True
    assert plan["intent"] == "domain_feature"
    assert "table CreditMemo" in plan["dsl_patch"]
    assert plan["lint"]["ok"] is True
    assert plan["migration_preview"]["format"] == "appgen.migration-plan.v1"
    assert any(change["kind"] == "add_table" and change["table"] == "CreditMemo" for change in plan["migration_preview"]["changes"])
    assert plan["token_budget_notes"]


def test_appgen_nl_plan_subcommand_emits_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "finance.appgen"
    path.write_text(TOOLING_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "nl-plan",
            str(path),
            "--prompt",
            "Add credit memos to accounts receivable",
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.nl-plan.v1"
    assert payload["migration_preview"]["format"] == "appgen.migration-plan.v1"


def test_appgen_migration_plan_subcommand_emits_json_contract(tmp_path: Path) -> None:
    previous = tmp_path / "previous.appgen"
    current = tmp_path / "current.appgen"
    previous.write_text(TOOLING_SAMPLE, encoding="utf-8")
    current.write_text(
        TOOLING_SAMPLE
        + """

table Payment {
  id: int pk
  invoice_id: int -> Invoice.id
  amount: decimal default 0
}
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "migration-plan",
            str(previous),
            str(current),
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.migration-plan.v1"
    assert any(change["kind"] == "add_table" and change["table"] == "Payment" for change in payload["changes"])


def test_lsp_service_uses_shared_semantic_model_for_core_editor_features() -> None:
    report = lsp_service_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        position=_position_of(TOOLING_SAMPLE, "Invoice"),
        prefix="In",
        rename_to="SalesInvoice",
    )

    assert report["format"] == "appgen.lsp-service.v1"
    assert report["ok"] is True
    assert report["semantic_model_format"] == "appgen.semantic-model.v1"
    assert report["capabilities"]["features"]["textDocument/completion"] is True
    assert not any(item["severity"] == 1 for item in report["publishDiagnostics"]["diagnostics"])
    assert any(item["label"] == "Invoice" for item in report["completion"]["items"])
    assert report["hover"]["ok"] is True
    assert report["definition"]["ok"] is True
    assert len(report["references"]["locations"]) >= 2
    assert any(symbol["name"] == "Invoice" for symbol in report["documentSymbol"]["symbols"])
    assert report["formatting"]["format"] == "appgen.lsp-formatting.v1"
    assert report["rename"]["ok"] is True
    assert "SalesInvoice" in report["rename"]["workspace_edit"]["changes"]["finance.appgen"][0]["newText"]
    assert any(symbol["name"] == "Invoice" for symbol in report["workspaceSymbol"]["symbols"])


def test_lsp_service_exposes_code_action_for_missing_handler_target() -> None:
    source = """
    app Bad { targets: web }
    table Invoice { id: int pk }
    view InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }
    """

    report = lsp_service_dsl(source, source_name="bad.appgen", position=_position_of(source, "SubmitInvoice"))

    assert report["ok"] is False
    assert any(item["code"] == "AGX0403" for item in report["publishDiagnostics"]["source_report"]["diagnostics"])
    assert any(action["data"]["id"] == "create_operation_from_handler" for action in report["codeAction"]["actions"])


def test_lsp_code_actions_cover_required_tooling_quick_fixes() -> None:
    source = """
    app Bad { targets: web, mobile }
    table Customer { id: int pk; name: string }
    table Invoice {
      id: int pk
      total: decimal
      customer_id: int -> Customer.missing_id
    }
    view MissingForm for Missing { Main: id }
    view InvoiceForm for Invoice {
      Main: totl, customer.missing_name
      on Save -> SubmitInvoice
    }
    rule InvoicePolicy for Invoice { missing_status == active }
    composition Suite {
      include pbc missing_pbc version 1.0.0
      include pbc gl_core version 1.0.0
      include pbc ap_automation version 1.0.0
      connect ap_automation domain_event MissingEvent -> gl_core domain_event MissingCommand
    }
    llm ApiModel { provider: openai; api_key: "sk-secret" }
    agent Writer {
      provider: ApiModel
      tools: write
    }
    """

    report = lsp_service_dsl(source, source_name="bad.appgen")
    action_ids = {action["data"]["id"] for action in report["codeAction"]["actions"]}

    assert {
        "create_missing_table",
        "create_missing_field",
        "create_calculated_field_for_binding",
        "create_operation_from_handler",
        "create_flow_from_handler",
        "add_lookup_directive",
        "replace_typo_with_nearest_symbol",
        "replace_secret_literal_with_env",
    } <= action_ids


def test_lsp_code_actions_cover_pbc_and_agent_quick_fixes_on_parseable_sources() -> None:
    pbc_source = """
    app BadPbc { targets: web }
    table Thing { id: int pk }
    view ThingForm for Thing { Main: id }
    composition Suite {
      include pbc missing_pbc version 1.0.0
      include pbc gl_core version 1.0.0
      include pbc ap_automation version 1.0.0
      connect ap_automation domain_event MissingEvent -> gl_core domain_event MissingCommand
    }
    """
    agent_source = """
    app BadAgent { targets: web }
    table Thing { id: int pk }
    view ThingForm for Thing { Main: id }
    llm LocalModel { provider: ollama; mode: local }
    agent Writer {
      provider: LocalModel
      tools: write
    }
    """

    pbc_actions = {action["data"]["id"] for action in lsp_service_dsl(pbc_source, source_name="pbc.appgen")["codeAction"]["actions"]}
    agent_actions = {action["data"]["id"] for action in lsp_service_dsl(agent_source, source_name="agent.appgen")["codeAction"]["actions"]}

    assert {"create_event_contract", "register_or_import_pbc_manifest"} <= pbc_actions
    assert "add_missing_permission_for_agent_skill" in agent_actions


def test_lsp_code_actions_add_package_and_smoke_test_for_valid_sources() -> None:
    source = """
    app Packaged { targets: web, mobile }
    table Book { id: int pk; title: string }
    view BookForm for Book { Main: title }
    flow PublishBook { draft -> live }
    """

    report = lsp_service_dsl(source, source_name="packaged.appgen")
    action_ids = {action["data"]["id"] for action in report["codeAction"]["actions"]}

    assert "add_package_for_app_target" in action_ids
    assert "create_smoke_test_declaration" in action_ids


def test_appgen_lsp_subcommand_emits_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "finance.appgen"
    path.write_text(TOOLING_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lsp",
            str(path),
            "--position",
            "9:6",
            "--prefix",
            "In",
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.lsp-service.v1"
    assert payload["capabilities"]["source_of_truth"] == "appgen.semantic-model.v1"


def test_release_verifier_report_covers_package_pbc_and_deployment_evidence() -> None:
    report = release_verifier_report_dsl(RELEASE_SAMPLE, source_name="release.appgen", targets=("all",))

    assert report["format"] == "appgen.release-verifier-report.v1"
    assert report["ok"] is True
    assert set(report["reports"]) == {"web", "mobile", "desktop", "pbc", "deployment"}
    assert report["reports"]["web"]["format"] == "appgen.web-verifier.v1"
    assert report["reports"]["mobile"]["format"] == "appgen.mobile-verifier.v1"
    assert report["reports"]["desktop"]["format"] == "appgen.desktop-verifier.v1"
    assert report["reports"]["pbc"]["format"] == "appgen.pbc-verifier.v1"
    assert report["reports"]["deployment"]["format"] == "appgen.deployment-verifier.v1"
    assert report["evidence_bundle"]["format"] == "appgen.release-evidence-bundle.v1"


def test_release_verifier_reports_blocking_gaps_for_missing_mobile_package_metadata() -> None:
    report = release_verifier_report_dsl(TOOLING_SAMPLE, source_name="finance.appgen", targets=("mobile",))

    assert report["ok"] is False
    assert "package_metadata_exists" in report["reports"]["mobile"]["blocking_gaps"]
    assert "smoke_launch_not_declared" in report["reports"]["mobile"]["blocking_gaps"]


def test_pbc_verifier_accepts_catalog_package_with_release_evidence() -> None:
    report = pbc_verifier_report("gl_core")

    assert report["format"] == "appgen.pbc-package-verifier.v1"
    assert report["ok"] is True
    assert report["catalog"]["pbc"] == "gl_core"


def test_pbc_publish_report_returns_side_effect_free_catalog_patch() -> None:
    report = pbc_publish_report("src/pyAppGen/pbcs/gl_core", catalog="local")

    assert report["format"] == "appgen.pbc-publish-report.v1"
    assert report["ok"] is True
    assert report["pbc"] == "gl_core"
    assert report["target"]["side_effect_free"] is True
    assert report["target"]["write_performed"] is False
    assert "gl_core" in report["catalog_patch"]
    assert report["registration"]["decision"] == "approved"
    assert report["release_evidence"]["format"] == "appgen.pbc-package-verifier.v1"


def test_appgen_verify_and_pbc_subcommands_emit_json_contracts(tmp_path: Path) -> None:
    path = tmp_path / "release.appgen"
    path.write_text(RELEASE_SAMPLE, encoding="utf-8")

    verify = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "verify", str(path), "--target", "all", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    pbc = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "pbc", "verify", "gl_core", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    publish = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "pbc",
            "publish",
            "src/pyAppGen/pbcs/gl_core",
            "--catalog",
            "local",
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert verify.returncode == 0, verify.stderr
    assert pbc.returncode == 0, pbc.stderr
    assert publish.returncode == 0, publish.stderr
    verify_payload = json.loads(verify.stdout)
    pbc_payload = json.loads(pbc.stdout)
    publish_payload = json.loads(publish.stdout)
    assert verify_payload["format"] == "appgen.release-verifier-report.v1"
    assert pbc_payload["format"] == "appgen.pbc-package-verifier.v1"
    assert publish_payload["format"] == "appgen.pbc-publish-report.v1"
    assert publish_payload["catalog_patch"]["gl_core"]["datastore_backend"] == "postgresql"


def test_designer_sync_projects_all_required_ide_surfaces_from_semantic_model() -> None:
    report = designer_sync_report_dsl(TOOLING_SAMPLE, source_name="finance.appgen")

    assert report["format"] == "appgen.designer-sync-report.v1"
    assert report["ok"] is True
    assert report["semantic_model_format"] == "appgen.semantic-model.v1"
    assert set(report["surfaces"]) >= {
        "dsl_editor",
        "component_palette",
        "form_designer",
        "database_designer",
        "workflow_designer",
        "pbc_composition_designer",
        "package_deployment_designer",
        "diagnostics_panel",
        "graph_explain_panel",
        "natural_language_planner",
    }
    assert report["projections"]["form_designer"]["views"][0]["valid_bindings"]
    assert report["projections"]["database_designer"]["er_graph"]["format"] == "appgen.graph.er.v1"
    assert report["projections"]["workflow_designer"]["workflow_graph"]["format"] == "appgen.graph.workflow.v1"


def test_designer_sync_accepts_round_trippable_visual_edit_and_rejects_invalid_binding() -> None:
    valid = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "add_component",
            "view": "InvoiceForm",
            "binding": "customer.name",
            "component": "Lookup",
            "x": 1,
            "y": 2,
            "w": 4,
            "h": 1,
        },
    )
    invalid = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "add_component",
            "view": "InvoiceForm",
            "binding": "missing.field",
            "component": "Lookup",
            "x": 1,
            "y": 2,
            "w": 4,
            "h": 1,
        },
    )

    assert valid["visual_edit"]["accepted"] is True
    assert valid["visual_edit"]["round_trip_ok"] is True
    assert invalid["visual_edit"]["accepted"] is False
    assert invalid["ok"] is False
    assert any(item["code"] == "AGX0402" for item in invalid["visual_edit"]["diagnostics"])


def test_appgen_designer_sync_subcommand_emits_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "finance.appgen"
    path.write_text(TOOLING_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.designer-sync-report.v1"
    assert payload["projections"]["dsl_editor"]["semantic_model_format"] == "appgen.semantic-model.v1"


def test_diagnostic_catalog_and_fixture_audit_cover_required_agx_codes() -> None:
    catalog = diagnostic_catalog_dsl()
    audit = diagnostic_fixture_audit_dsl()

    assert catalog["format"] == "appgen.diagnostic-catalog.v1"
    assert audit["format"] == "appgen.diagnostic-fixture-audit.v1"
    assert catalog["ok"] is True
    assert audit["ok"] is True
    assert set(catalog["required_codes"]) <= set(audit["covered_codes"])
    assert {
        "AGX0201",
        "AGX0304",
        "AGX0404",
        "AGX0602",
        "AGX0903",
        "AGX1002",
        "AGX1101",
        "AGX1201",
    } <= set(audit["covered_codes"])


def test_appgen_diagnostics_subcommand_emits_catalog_and_fixture_audit() -> None:
    base_command = [sys.executable, "-m", "pyAppGen", "diagnostics", "--json"]
    catalog_result = subprocess.run(
        base_command,
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    audit_result = subprocess.run(
        [*base_command[:-1], "--audit-fixtures", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert catalog_result.returncode == 0, catalog_result.stderr
    assert audit_result.returncode == 0, audit_result.stderr
    assert json.loads(catalog_result.stdout)["format"] == "appgen.diagnostic-catalog.v1"
    assert json.loads(audit_result.stdout)["format"] == "appgen.diagnostic-fixture-audit.v1"


def test_semantic_drift_audit_proves_tooling_surfaces_share_one_model() -> None:
    report = semantic_drift_audit_dsl(RELEASE_SAMPLE, source_name="release.appgen")

    assert report["format"] == "appgen.semantic-drift-audit.v1"
    assert report["ok"] is True
    assert report["semantic_model_format"] == "appgen.semantic-model.v1"
    assert {
        "cli",
        "lsp",
        "studio",
        "graph",
        "generator_readiness",
        "release_verifier",
        "tests",
    } <= set(report["surfaces"])
    assert all(check["ok"] for check in report["checks"])
    assert any(check["check"] == "designer_graphs_match_semantic_graphs" for check in report["checks"])


def test_appgen_drift_subcommand_emits_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "release.appgen"
    path.write_text(RELEASE_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "drift", str(path), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.semantic-drift-audit.v1"
    assert payload["surface_evidence"]["lsp_service"] == "appgen.lsp-service.v1"


def test_doctor_report_checks_parser_catalog_generator_and_ide_hooks() -> None:
    report = doctor_report_dsl()

    assert report["format"] == "appgen.doctor-report.v1"
    assert report["ok"] is True
    assert {
        "grammar_file",
        "generated_parser",
        "parser_sync",
        "pbc_catalog",
        "template_writers",
        "generator_backends",
        "lsp_semantic_service",
        "studio_semantic_service",
    } <= {check["check"] for check in report["checks"]}


def test_generate_report_writes_validated_dsl_app_and_blocks_lint_errors(tmp_path: Path) -> None:
    output_dir = tmp_path / "generated_app"
    report = generate_report_dsl(RELEASE_SAMPLE, source_name="release.appgen", output_dir=output_dir, targets=("web",))
    blocked = generate_report_dsl(
        "app Bad { targets: web } table Invoice { total: galaxy }",
        source_name="bad.appgen",
        output_dir=tmp_path / "blocked_app",
    )

    assert report["format"] == "appgen.generate-report.v1"
    assert report["ok"] is True
    assert report["generated"] is True
    assert (output_dir / "appgen.json").exists()
    assert {"appgen.json", "models.py", "views.py"} <= {item["path"] for item in report["artifacts"]}
    assert blocked["ok"] is False
    assert blocked["generated"] is False
    assert "lint_errors" in blocked["blocking_gaps"]


def test_appgen_doctor_and_generate_subcommands_emit_json_contracts(tmp_path: Path) -> None:
    source_path = tmp_path / "release.appgen"
    output_dir = tmp_path / "app"
    source_path.write_text(RELEASE_SAMPLE, encoding="utf-8")

    doctor_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "doctor", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    generate_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "generate",
            str(source_path),
            "--target",
            "web",
            "--out",
            str(output_dir),
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert doctor_result.returncode == 0, doctor_result.stderr
    assert generate_result.returncode == 0, generate_result.stderr
    assert json.loads(doctor_result.stdout)["format"] == "appgen.doctor-report.v1"
    assert json.loads(generate_result.stdout)["format"] == "appgen.generate-report.v1"
    assert (output_dir / "appgen.json").exists()


def test_cli_contracts_cover_text_summaries_exit_codes_and_bad_arguments(tmp_path: Path) -> None:
    source_path = tmp_path / "release.appgen"
    output_dir = tmp_path / "generated"
    source_path.write_text(RELEASE_SAMPLE, encoding="utf-8")
    root = Path(__file__).resolve().parents[1]

    lint_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lint", str(source_path)],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    format_check = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "format", str(source_path), "--check"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    graph_suite_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "graph-suite", str(source_path)],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    doctor_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "doctor"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    generate_text = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "generate",
            str(source_path),
            "--target",
            "web",
            "--out",
            str(output_dir),
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    invalid_graph_format = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "graph", str(source_path), "--format", "svg"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    missing_required_arg = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "generate", str(source_path)],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )

    assert lint_text.returncode == 0, lint_text.stderr
    assert "lint ok:" in lint_text.stdout
    assert format_check.returncode == 1
    assert "format changed: idempotent" in format_check.stdout
    assert graph_suite_text.returncode == 0, graph_suite_text.stderr
    assert "graph-suite ok: 9 kinds, 3 formats" in graph_suite_text.stdout
    assert doctor_text.returncode == 0, doctor_text.stderr
    assert doctor_text.stdout.startswith("doctor ok")
    assert generate_text.returncode == 0, generate_text.stderr
    assert "generate ok: generated=True" in generate_text.stdout
    assert "artifact appgen.json" in generate_text.stdout
    assert invalid_graph_format.returncode == 2
    assert "invalid choice" in invalid_graph_format.stderr
    assert missing_required_arg.returncode == 2
    assert "--out" in missing_required_arg.stderr
