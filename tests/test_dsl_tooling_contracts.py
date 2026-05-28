import json
import subprocess
import sys
from pathlib import Path

from pyAppGen.dsl import format_report_dsl
from pyAppGen.dsl import designer_sync_report_dsl
from pyAppGen.dsl import graph_report_dsl
from pyAppGen.dsl import lint_report_dsl
from pyAppGen.dsl import lsp_service_dsl
from pyAppGen.dsl import migration_plan_dsl
from pyAppGen.dsl import nl_plan_dsl
from pyAppGen.dsl import pbc_verifier_report
from pyAppGen.dsl import release_verifier_report_dsl
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
    assert any(item["code"] == "AGX0402" for item in report["diagnostics"])
    assert any(item["legacy_code"] == "unknown_view_field" for item in report["diagnostics"])


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

    assert verify.returncode == 0, verify.stderr
    assert pbc.returncode == 0, pbc.stderr
    verify_payload = json.loads(verify.stdout)
    pbc_payload = json.loads(pbc.stdout)
    assert verify_payload["format"] == "appgen.release-verifier-report.v1"
    assert pbc_payload["format"] == "appgen.pbc-package-verifier.v1"


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
