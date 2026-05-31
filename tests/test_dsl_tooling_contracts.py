import json
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from pyAppGen import dsl as appgen_dsl
from pyAppGen.dsl import format_report_dsl
from pyAppGen.dsl import formatter_contract_audit_dsl
from pyAppGen.dsl import designer_visual_edit_matrix_dsl
from pyAppGen.dsl import designer_sync_report_dsl
from pyAppGen.dsl import diagnostic_catalog_dsl
from pyAppGen.dsl import diagnostic_fixture_audit_dsl
from pyAppGen.dsl import doctor_report_dsl
from pyAppGen.dsl import graph_report_dsl
from pyAppGen.dsl import graph_suite_report_dsl
from pyAppGen.dsl import generate_report_dsl
from pyAppGen.dsl import lint_report_dsl
from pyAppGen.dsl import lint_report_dsl_path
from pyAppGen.dsl import lint_report_dsl_sources
from pyAppGen.dsl import lsp_server_handle_message
from pyAppGen.dsl import lsp_service_dsl
from pyAppGen.dsl import migration_plan_dsl
from pyAppGen.dsl import nl_plan_dsl
from pyAppGen.dsl import nl_plan_contract_audit_dsl
from pyAppGen.dsl import parser_golden_audit_dsl
from pyAppGen.dsl import pbc_publish_report
from pyAppGen.dsl import pbc_verifier_report
from pyAppGen.dsl import release_verifier_report_dsl
from pyAppGen.dsl import semantic_drift_audit_dsl
from pyAppGen.dsl import semantic_model_dsl
from pyAppGen.dsl import semantic_model_dsl_path
from pyAppGen.dsl import semantic_model_dsl_sources
from pyAppGen.dsl import symbol_coverage_dsl
from pyAppGen.dsl import tooling_audit_report_dsl
from pyAppGen.dsl import validate_report_dsl
from pyAppGen.dsl import completion_coverage_dsl
from pyAppGen.dsl import apply_lsp_code_action_dsl
from pyAppGen.dsl import lsp_code_action_apply_audit_dsl


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


def _rpc_frame(message: dict) -> bytes:
    body = json.dumps(message, separators=(",", ":")).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def _read_rpc_frames(payload: bytes) -> tuple[dict, ...]:
    offset = 0
    messages = []
    separator = b"\r\n\r\n"
    while offset < len(payload):
        header_end = payload.find(separator, offset)
        if header_end < 0:
            break
        headers = payload[offset:header_end].decode("ascii")
        length = 0
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                length = int(line.split(":", 1)[1].strip())
        body_start = header_end + len(separator)
        body_end = body_start + length
        messages.append(json.loads(payload[body_start:body_end].decode("utf-8")))
        offset = body_end
    return tuple(messages)


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
    assert model["symbol_coverage"]["format"] == "appgen.symbol-coverage.v1"
    assert model["contract_counts"]["required_top_level_field_count"] == 20
    assert model["contract_counts"]["present_top_level_field_count"] == 20
    assert model["contract_counts"]["missing_top_level_field_count"] == 0
    assert model["contract_counts"]["symbol_count"] == len(model["symbols"])
    assert model["contract_counts"]["symbol_kind_count"] > 0
    assert model["missing_top_level_fields"] == ()


def test_semantic_model_sources_resolve_workspace_files_and_symbol_attribution(tmp_path: Path) -> None:
    app_path = tmp_path / "app.appgen"
    data_dir = tmp_path / "data"
    ui_dir = tmp_path / "ui"
    workflow_dir = tmp_path / "workflow"
    data_dir.mkdir()
    ui_dir.mkdir()
    workflow_dir.mkdir()
    customer_path = data_dir / "customer.appgen"
    invoice_path = data_dir / "invoice.appgen"
    form_path = ui_dir / "invoice-form.appgen"
    flow_path = workflow_dir / "submit-invoice.appgen"
    app_path.write_text("app SourceSet { targets: web, mobile, desktop }\n", encoding="utf-8")
    customer_path.write_text("table Customer { id: int pk; name: string required search }\n", encoding="utf-8")
    invoice_path.write_text(
        """
table Invoice {
  id: int pk
  customer_id: int -> Customer.id [many-to-one]
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
  lookup customer_name (customer.name)
}
""".strip()
        + "\n",
        encoding="utf-8",
    )
    form_path.write_text(
        """
view InvoiceForm for Invoice {
  Main: customer.name, total
  @ customer.name Lookup 0 0 6 1
  on Save -> SubmitInvoice
}
""".strip()
        + "\n",
        encoding="utf-8",
    )
    flow_path.write_text("flow SubmitInvoice { draft -> reviewed; reviewed -> posted }\n", encoding="utf-8")

    model = semantic_model_dsl_path(tmp_path)

    assert model["format"] == "appgen.semantic-model.v1"
    assert model["ok"] is True
    assert model["source_set"]["format"] == "appgen.semantic-source-set.v1"
    assert {report["format"] for report in model["file_reports"]} == {"appgen.semantic-file-report.v1"}
    assert model["source_mode"] == "directory"
    assert model["file_count"] == 5
    assert set(model["source_files"]) == {str(app_path), str(customer_path), str(invoice_path), str(form_path), str(flow_path)}
    assert model["tables"]["Invoice"]["fields"]["customer_id"]["relationship"]["target_table"] == "Customer"
    assert model["tables"]["Invoice"]["lookup_paths"]["customer.name"]["valid"] is True
    assert model["views"]["InvoiceForm"]["table"] == "Invoice"
    assert "SubmitInvoice" in model["flows"]
    assert model["symbols"]["table.Customer"]["file"] == str(customer_path)
    assert model["symbols"]["table.Invoice"]["file"] == str(invoice_path)
    assert model["symbols"]["view.InvoiceForm"]["file"] == str(form_path)
    assert model["symbols"]["flow.SubmitInvoice"]["file"] == str(flow_path)
    assert model["source_file_symbol_counts"][str(app_path)] >= 1
    assert model["source_file_symbol_counts"][str(customer_path)] >= 1
    assert model["source_file_symbol_counts"][str(invoice_path)] >= 1
    assert model["source_file_symbol_counts"][str(form_path)] >= 1
    assert model["source_file_symbol_counts"][str(flow_path)] >= 1
    assert model["contract_counts"]["source_file_count"] == 5
    assert model["contract_counts"]["source_file_symbol_file_count"] == 5


def test_semantic_model_sources_empty_source_set_reports_contract_error() -> None:
    model = semantic_model_dsl_sources({}, source_name="empty-workspace")

    assert model["format"] == "appgen.semantic-model.v1"
    assert model["ok"] is False
    assert model["source_set"]["format"] == "appgen.semantic-source-set.v1"
    assert model["source_mode"] == "directory"
    assert model["file_count"] == 0
    assert model["diagnostics"][0]["code"] == "AGX0001"


def test_semantic_symbol_coverage_proves_required_nested_symbol_kinds() -> None:
    source = """
    app SymbolDemo { targets: web, mobile, desktop }
    AddressFields { street: string }
    table Customer { id: int pk; name: string; ... AddressFields }
    table Invoice { id: int pk; customer_id: int -> Customer.id; total: decimal = id }
    enum Status { draft posted }
    view InvoiceForm for Invoice {
      Main: customer.name, total
      @ customer.name Lookup 0 0 6 1
      on Save -> SubmitInvoice
    }
    flow SubmitInvoice { draft -> reviewed; reviewed -> posted }
    role Clerk { Invoice: read, write }
    rule InvoicePolicy for Invoice { id == 1 }
    llm LocalModel { provider: ollama; mode: local }
    agent Builder { provider: LocalModel; tools: write, schema; Invoice: write; on Run -> SubmitInvoice }
    pbc Billing { owns: Invoice; Invoice: read, write }
    composition Suite { include pbc gl_core version 1.0.0 }
    audit ReleaseAudit { evidence: tests }
    version Release2026 { number: 1.0.0 }
    operation ReverseInvoice { posted -> reversed }
    security TenantSecurity { Invoice: read, write; tenancy: org }
    api InvoiceApi { on Create -> SubmitInvoice; Invoice: read }
    event InvoicePosted { topic: invoices }
    job InvoiceJob { run nightly -> SubmitInvoice }
    report InvoiceReport { source Invoice -> InvoiceApi }
    menu MainMenu { on Open -> SubmitInvoice }
    component CustomerLookup { on Select -> SubmitInvoice }
    package MobileRelease { target: mobile; smoke: launch }
    test Smoke { run happy -> SubmitInvoice }
    deploy Production { unit SubmitInvoice as worker; health SubmitInvoice "/health" }
    """

    model = semantic_model_dsl(source, source_name="symbols.appgen")
    coverage = symbol_coverage_dsl(source, source_name="symbols.appgen")

    assert model["ok"] is True
    assert coverage["format"] == "appgen.symbol-coverage.v1"
    assert model["symbol_coverage"]["missing"] == ()
    assert coverage["missing"] == ()
    assert coverage["required_kind_count"] == len(coverage["required"])
    assert coverage["detected_kind_count"] == len(coverage["detected"])
    assert coverage["missing_kind_count"] == len(coverage["missing"])
    assert coverage["detected_kind_count"] == coverage["required_kind_count"]
    assert set(coverage["required"]) <= set(coverage["detected"])
    assert coverage["counts"]["group"] == 1
    assert coverage["counts"]["component_binding"] == 1
    assert coverage["counts"]["permission"] >= 3
    assert coverage["counts"]["agent_skill"] >= 2
    assert coverage["counts"]["deployment_unit"] == 1
    assert any(symbol["kind"] == "component_binding" and symbol["name"] == "customer.name" for symbol in model["symbols"].values())
    assert any(symbol["kind"] == "deployment_unit" and symbol["name"] == "SubmitInvoice" for symbol in model["symbols"].values())


def test_lsp_symbol_coverage_projects_required_symbol_kinds_to_editor_surfaces() -> None:
    source = appgen_dsl._symbol_coverage_sample()
    coverage = appgen_dsl.lsp_symbol_coverage_dsl(source, source_name="lsp-symbols.appgen")

    assert coverage["format"] == "appgen.lsp-symbol-coverage.v1"
    assert coverage["ok"] is True
    assert coverage["required_kind_count"] == len(coverage["required"])
    assert coverage["document_detected_kind_count"] == coverage["required_kind_count"]
    assert coverage["workspace_detected_kind_count"] == coverage["required_kind_count"]
    assert coverage["document_missing_kind_count"] == 0
    assert coverage["workspace_missing_kind_count"] == 0
    assert coverage["document_missing"] == ()
    assert coverage["workspace_missing"] == ()
    assert coverage["document_symbol_count"] >= coverage["required_kind_count"]
    assert coverage["workspace_symbol_count"] >= coverage["required_kind_count"]
    assert coverage["document_kind_counts"]["deployment_unit"] >= 1
    assert coverage["workspace_kind_counts"]["agent_skill"] >= 1


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
    assert report["stage_count"] == len(report["stage_names"]) == 3
    assert report["severity_count"] == len(report["severity_names"]) == 4
    assert report["file_count"] == 1
    assert report["diagnostic_count"] == len(report["diagnostics"])
    assert report["fix_count"] == sum(len(item.get("fixes", ())) for item in report["diagnostics"])
    assert report["fixes_available"] is (report["fix_count"] > 0)
    assert report["severity_counts"]["error"] >= 1
    assert any(item["code"] == "AGX0303" for item in report["diagnostics"])
    assert any(item["legacy_code"] == "unresolved_lookup_path" for item in report["diagnostics"])


def test_lint_report_accepts_directory_source_sets(tmp_path: Path) -> None:
    source_dir = tmp_path / "src" / "appgen"
    source_dir.mkdir(parents=True)
    finance = source_dir / "finance.appgen"
    broken = source_dir / "broken.appgen"
    finance.write_text(TOOLING_SAMPLE, encoding="utf-8")
    broken.write_text("app Broken { targets: web }\n\ntable BrokenThing { id: int pk; name: galaxy }\n", encoding="utf-8")

    report = lint_report_dsl_path(source_dir)
    memory_report = lint_report_dsl_sources(
        {
            "memory/finance.appgen": TOOLING_SAMPLE,
            "memory/broken.appgen": broken.read_text(encoding="utf-8"),
        }
    )

    assert report["format"] == "appgen.lint-report.v1"
    assert report["source_mode"] == "directory"
    assert report["ok"] is False
    assert report["stage_count"] == len(report["stage_names"]) == 3
    assert report["severity_count"] == len(report["severity_names"]) == 4
    assert report["file_count"] == len(report["files"]) == 2
    assert report["diagnostic_count"] == len(report["diagnostics"])
    assert report["fix_count"] == sum(len(item.get("fixes", ())) for item in report["diagnostics"])
    assert report["fixes_available"] is (report["fix_count"] > 0)
    assert {Path(item).name for item in report["files"]} == {"finance.appgen", "broken.appgen"}
    assert len(report["file_reports"]) == 2
    assert any(item["code"] == "AGX0201" and Path(item["file"]).name == "broken.appgen" for item in report["diagnostics"])
    assert memory_report["source_mode"] == "directory"
    assert memory_report["file_count"] == len(memory_report["files"]) == 2
    assert memory_report["diagnostic_count"] == len(memory_report["diagnostics"])


def test_lint_report_strict_mode_promotes_unknown_components_to_errors() -> None:
    source = """
    app StrictDemo { targets: web }
    table Customer { id: int pk; name: string }
    view CustomerForm for Customer {
      Main: name
      @ name UnknownWidget 0 0 4 1
    }
    """

    normal = lint_report_dsl(source, source_name="strict.appgen")
    strict = lint_report_dsl(source, source_name="strict.appgen", strict=True)

    assert normal["strict"] is False
    assert strict["strict"] is True
    assert normal["ok"] is True
    assert strict["ok"] is False
    assert any(item["code"] == "AGX0404" and item["severity"] == "warning" for item in normal["diagnostics"])
    assert any(item["code"] == "AGX0404" and item["severity"] == "error" for item in strict["diagnostics"])


def test_lint_report_uses_component_catalog_to_register_visual_components() -> None:
    source = """
    app CatalogDemo { targets: web }
    table Customer { id: int pk; name: string }
    view CustomerForm for Customer {
      Main: name
      @ name CustomGauge 0 0 4 1
    }
    """

    strict = lint_report_dsl(source, source_name="catalog.appgen", strict=True)
    cataloged = lint_report_dsl(
        source,
        source_name="catalog.appgen",
        strict=True,
        component_catalog=("CustomGauge",),
        component_catalog_source="components.json",
    )

    assert strict["ok"] is False
    assert any(item["code"] == "AGX0404" for item in strict["diagnostics"])
    assert cataloged["ok"] is True
    assert not any(item["code"] == "AGX0404" for item in cataloged["diagnostics"])
    assert cataloged["component_catalog"]["source"] == "components.json"
    assert cataloged["component_catalog"]["components"] == ("CustomGauge",)


def test_appgen_lint_subcommand_accepts_directory_input(tmp_path: Path) -> None:
    source_dir = tmp_path / "appgen"
    source_dir.mkdir()
    (source_dir / "one.appgen").write_text("app One { targets: web }\n\ntable OneThing { id: int pk }\n", encoding="utf-8")
    (source_dir / "two.appgen").write_text("app Two { targets: web }\n\ntable TwoThing { id: int pk }\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lint", str(source_dir), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lint", str(source_dir)],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert text_result.returncode == 0, text_result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.lint-report.v1"
    assert payload["source_mode"] == "directory"
    assert {Path(item).name for item in payload["files"]} == {"one.appgen", "two.appgen"}
    assert "source directory: files=2" in text_result.stdout


def test_appgen_lint_subcommand_enforces_strict_component_mode(tmp_path: Path) -> None:
    source_path = tmp_path / "strict.appgen"
    source_path.write_text(
        """
app StrictDemo { targets: web }
table Customer { id: int pk; name: string }
view CustomerForm for Customer {
  Main: name
  @ name UnknownWidget 0 0 4 1
}
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lint", str(source_path), "--strict", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1, result.stderr
    payload = json.loads(result.stdout)
    assert payload["strict"] is True
    assert payload["severity_counts"]["error"] == 1
    assert any(item["code"] == "AGX0404" and item["severity"] == "error" for item in payload["diagnostics"])


def test_appgen_lint_subcommand_applies_component_catalog(tmp_path: Path) -> None:
    source_path = tmp_path / "catalog.appgen"
    catalog_path = tmp_path / "components.json"
    source_path.write_text(
        """
app CatalogDemo { targets: web }
table Customer { id: int pk; name: string }
view CustomerForm for Customer {
  Main: name
  @ name CustomGauge 0 0 4 1
}
""",
        encoding="utf-8",
    )
    catalog_path.write_text(
        json.dumps({"components": [{"name": "CustomGauge", "icon": "gauge"}]}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lint",
            str(source_path),
            "--strict",
            "--catalog",
            str(catalog_path),
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["strict"] is True
    assert payload["component_catalog"]["source"] == str(catalog_path)
    assert payload["component_catalog"]["components"] == ["CustomGauge"]
    assert not any(item["code"] == "AGX0404" for item in payload["diagnostics"])


def test_appgen_component_publish_subcommand_emits_side_effect_free_catalog_patch(tmp_path: Path) -> None:
    catalog_path = tmp_path / "components.json"
    catalog_path.write_text(json.dumps({"components": [{"name": "ExistingBox"}]}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "component-publish",
            "--component",
            "CustomGauge",
            "--catalog",
            str(catalog_path),
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "component-publish",
            "--component",
            "CustomGauge",
            "--catalog",
            str(catalog_path),
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert payload["format"] == "appgen.component-publish-report.v1"
    assert payload["ok"] is True
    assert payload["component"] == "CustomGauge"
    assert payload["catalog"]["components"] == ["ExistingBox"]
    assert payload["catalog_patch"]["format"] == "appgen.component-catalog-patch.v1"
    assert payload["catalog_patch"]["component"]["name"] == "CustomGauge"
    assert payload["catalog_patch"]["component"]["icon"] == "custom-gauge"
    assert payload["catalog_patch"]["catalog_path"] == str(catalog_path)
    assert payload["catalog_patch"]["before_count"] == 1
    assert payload["catalog_patch"]["after_count"] == 2
    assert payload["catalog_patch"]["already_registered"] is False
    assert payload["catalog_patch"]["side_effect_free"] is True
    assert payload["catalog_patch"]["write_performed"] is False
    assert text_result.returncode == 0, text_result.stderr
    assert text_result.stdout.startswith("component-publish ok: format=appgen.component-publish-report.v1 component=CustomGauge")
    assert f"catalog={catalog_path}" in text_result.stdout
    assert "already_registered=False" in text_result.stdout
    assert "side_effect_free=True" in text_result.stdout
    assert "write_performed=False" in text_result.stdout
    assert "patch_format=appgen.component-catalog-patch.v1" in text_result.stdout
    assert "catalog-count before=1 after=2 existing=1" in text_result.stdout


def test_component_publish_cli_audit_covers_patch_text_and_missing_catalog(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_component_publish_cli(tmp_path)

    assert audit["format"] == "appgen.component-publish-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 3
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["failing_cases"] == ()
    assert audit["case_ids"] == ("json_publish_patch", "text_publish_markers", "missing_catalog_rejected")
    assert audit["required_case_ids"] == ("json_publish_patch", "text_publish_markers", "missing_catalog_rejected")
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["expected_exit_codes_by_case"] == {
        "json_publish_patch": 0,
        "text_publish_markers": 0,
        "missing_catalog_rejected": 1,
    }
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {case_id: True for case_id in audit["required_case_ids"]}
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["patch_format"] == "appgen.component-catalog-patch.v1"
    assert audit["operation"] == "upsert_component"
    assert audit["component"] == "CustomGauge"
    assert audit["component_icon"] == "custom-gauge"
    assert audit["before_count"] == 1
    assert audit["after_count"] == 2
    assert audit["existing_catalog_count"] == 1
    assert audit["side_effect_free"] is True
    assert audit["write_performed"] is False
    assert audit["text_has_report_format"] is True
    assert audit["text_has_patch_format"] is True
    assert audit["text_has_side_effect_markers"] is True
    assert audit["text_has_existing_catalog"] is True
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_markers"] == ()
    assert {
        "component-publish ok: format=appgen.component-publish-report.v1",
        "patch_format=appgen.component-catalog-patch.v1",
        "side_effect_free=True",
        "write_performed=False",
        "catalog-existing ExistingBox",
    } <= set(audit["required_text_markers"])
    assert audit["missing_catalog_exit_code"] == 1
    assert audit["required_missing_catalog_blocking_gaps"] == ("catalog_path_readable",)
    assert "catalog_path_readable" in audit["missing_catalog_blocking_gaps"]
    assert audit["missing_catalog_blocking_gap_miss_count"] == 0
    assert audit["missing_catalog_blocking_gap_misses"] == ()
    assert audit["missing_catalog_side_effect_free"] is True
    assert audit["missing_catalog_write_performed"] is False


def test_lint_directory_audit_covers_strict_component_cli_gate(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_lint_directory_cli(tmp_path, TOOLING_SAMPLE)

    assert report["format"] == "appgen.lint-directory-cli-audit.v1"
    assert report["ok"] is True
    assert report["scenario_count"] == 8
    assert report["passing_scenario_count"] == report["scenario_count"]
    assert report["failing_scenario_count"] == 0
    assert report["failing_scenarios"] == ()
    assert report["scenario_ids"] == (
        "strict_directory_json",
        "warning_directory_files",
        "normal_unknown_component_warning",
        "strict_unknown_component_error",
        "strict_catalog_component_success",
        "previous_semantic_migration_preview",
        "stage_separation_profiles",
        "directory_file_order_and_reports",
    )
    assert report["required_scenario_ids"] == report["scenario_ids"]
    assert report["exit_codes_by_scenario"] == report["expected_exit_codes_by_scenario"]
    assert report["expected_exit_codes_by_scenario"] == {
        "strict_directory_json": 0,
        "warning_directory_files": 0,
        "normal_unknown_component_warning": 0,
        "strict_unknown_component_error": 1,
        "strict_catalog_component_success": 0,
        "previous_semantic_migration_preview": 0,
        "stage_separation_profiles": 0,
        "directory_file_order_and_reports": 0,
    }
    assert report["missing_exit_code_scenario_count"] == 0
    assert report["missing_exit_code_scenarios"] == ()
    assert report["payload_formats_by_scenario"] == report["expected_payload_formats_by_scenario"]
    assert set(report["expected_payload_formats_by_scenario"].values()) == {"appgen.lint-report.v1"}
    assert "stage_separation_profiles" not in report["expected_payload_formats_by_scenario"]
    assert report["missing_payload_format_scenario_count"] == 0
    assert report["missing_payload_format_scenarios"] == ()
    assert report["ok_by_scenario"] == {scenario: True for scenario in report["required_scenario_ids"]}
    assert report["missing_ok_scenario_count"] == 0
    assert report["missing_ok_scenarios"] == ()
    assert report["stage_profile_count"] == 3
    assert report["passing_stage_profile_count"] == report["stage_profile_count"]
    assert report["failing_stage_profile_count"] == 0
    assert report["stage_profile_ids"] == ("syntax", "semantic", "policy")
    assert report["exit_codes_by_stage_profile"] == report["expected_exit_codes_by_stage_profile"]
    assert report["expected_exit_codes_by_stage_profile"] == {"syntax": 1, "semantic": 1, "policy": 0}
    assert report["missing_stage_profile_exit_code_count"] == 0
    assert report["missing_stage_profile_exit_code_profiles"] == ()
    assert report["ok_by_stage_profile"] == {"syntax": True, "semantic": True, "policy": True}
    assert report["missing_ok_stage_profile_count"] == 0
    assert report["missing_ok_stage_profiles"] == ()
    assert report["missing_stage_name_count"] == 0
    assert report["missing_stage_names"] == ()
    assert report["missing_severity_name_count"] == 0
    assert report["missing_severity_names"] == ()
    assert report["file_order_sorted"] is True
    assert report["file_relative_order"] == ("a.appgen", "nested/b.appgen")
    assert report["normal_unknown_component_warning"]["ok"] is True
    assert report["normal_unknown_component_warning"]["exit_code"] == 0
    assert report["normal_unknown_component_warning"]["strict"] is False
    assert report["strict_unknown_component_error"]["ok"] is True
    assert report["strict_unknown_component_error"]["exit_code"] == 1
    assert report["strict_unknown_component_error"]["strict"] is True
    assert report["strict_catalog_component_success"]["ok"] is True
    assert report["strict_catalog_component_success"]["exit_code"] == 0
    assert report["strict_catalog_component_success"]["component_catalog"]["components"] == ["CustomGauge"]
    assert report["previous_semantic_migration_preview"]["ok"] is True
    assert report["previous_semantic_migration_preview"]["format"] == "appgen.migration-plan.v1"
    assert "added_field" in report["previous_semantic_migration_preview"]["detected"]
    assert report["stage_separation"]["ok"] is True
    assert report["stage_separation"]["stages"] == {"syntax": True, "semantic": True, "policy": True}
    assert tuple(report["stage_separation"]["stage_names"]) == ("syntax", "semantic", "policy")
    assert tuple(report["stage_separation"]["severity_names"]) == ("error", "warning", "info", "hint")
    assert report["stage_separation"]["syntax"]["syntax"]["error"] >= 1
    assert report["stage_separation"]["semantic"]["semantic"]["error"] >= 1
    assert report["stage_separation"]["policy"]["policy"]["warning"] >= 1


def test_format_validate_and_graph_reports_follow_tooling_contracts() -> None:
    formatted = format_report_dsl(TOOLING_SAMPLE, source_name="finance.appgen")
    validation = validate_report_dsl(formatted["text"], source_name="finance.appgen", targets=("web", "mobile"))
    graph = graph_report_dsl(formatted["text"], source_name="finance.appgen", kind="er")

    assert formatted["format"] == "appgen.format-result.v1"
    assert formatted["idempotent"] is True
    assert validation["format"] == "appgen.validate-report.v1"
    assert validation["ok"] is True
    assert validation["requested_targets"] == ("web", "mobile")
    assert validation["requested_target_count"] == 2
    assert validation["app_target_count"] == len(validation["app_targets"])
    assert validation["check_count"] == len(validation["checks"])
    assert validation["passing_check_count"] == validation["check_count"]
    assert validation["blocking_check_count"] == 0
    assert validation["blocking_checks"] == ()
    assert validation["diagnostic_count"] == len(validation["diagnostics"])
    assert validation["target_diagnostic_count"] == 0
    assert any(check["check"] == "target_compatibility" and check["ok"] for check in validation["checks"])
    assert graph["format"] == "appgen.graph-report.v1"
    assert graph["graph"]["edges"][0]["from"] == "Invoice"


def test_validate_report_rejects_unknown_or_undeclared_targets() -> None:
    source = "app WebOnly { targets: web }\n\ntable Thing { id: int pk }\n"

    missing = validate_report_dsl(source, source_name="web.appgen", targets=("mobile",))
    unknown = validate_report_dsl(source, source_name="web.appgen", targets=("satellite",))

    assert missing["ok"] is False
    assert missing["checks"][-1]["missing_targets"] == ("mobile",)
    assert missing["requested_target_count"] == 1
    assert missing["blocking_check_count"] >= 1
    assert "target_compatibility" in missing["blocking_checks"]
    assert missing["diagnostic_count"] == len(missing["diagnostics"])
    assert missing["target_diagnostic_count"] >= 1
    assert any(item["code"] == "AGX0802" for item in missing["diagnostics"])
    assert unknown["ok"] is False
    assert unknown["checks"][-1]["unknown_targets"] == ("satellite",)
    assert unknown["target_diagnostic_count"] >= 1
    assert any("Unknown validation targets" in item["message"] for item in unknown["diagnostics"])


def test_appgen_validate_subcommand_enforces_requested_targets(tmp_path: Path) -> None:
    source_path = tmp_path / "web.appgen"
    source_path.write_text("app WebOnly { targets: web }\n\ntable Thing { id: int pk }\n", encoding="utf-8")

    ok_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "validate", str(source_path), "--targets", "web", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    bad_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "validate", str(source_path), "--targets", "web,mobile", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    bad_text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "validate", str(source_path), "--targets", "web,mobile"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert ok_result.returncode == 0, ok_result.stderr
    assert bad_result.returncode == 1, bad_result.stderr
    ok_payload = json.loads(ok_result.stdout)
    bad_payload = json.loads(bad_result.stdout)
    assert ok_payload["requested_targets"] == ["web"]
    assert bad_payload["requested_targets"] == ["web", "mobile"]
    assert bad_payload["checks"][-1]["missing_targets"] == ["mobile"]
    assert bad_text_result.returncode == 1
    assert bad_text_result.stdout.startswith("validate failed: format=appgen.validate-report.v1 requested=web,mobile")
    assert f"app_targets={','.join(bad_payload['app_targets'])}" in bad_text_result.stdout
    assert f"semantic_format={bad_payload['semantic_model']['format']}" in bad_text_result.stdout
    assert "fail target_compatibility" in bad_text_result.stdout
    assert "missing-targets mobile" in bad_text_result.stdout
    assert "error AGX0802:" in bad_text_result.stdout


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


def test_formatter_organize_orders_table_fields_without_reordering_top_level_declarations(tmp_path: Path) -> None:
    source = """
app OrganizeDemo { targets: web }

table Invoice {
  total: decimal = subtotal + tax
  description: string
  // customer link
  customer_id: int -> Customer.id
  updated_at: string
  invoice_number: string unique
  subtotal: decimal
  tax: decimal
  id: int pk
  index(total)
}

table Customer {
  name: string
  id: int pk
}
"""
    source_path = tmp_path / "organize.appgen"
    source_path.write_text(source, encoding="utf-8")

    report = format_report_dsl(source, source_name="organize.appgen", organize=True)
    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "format", str(source_path), "--organize", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert report["format"] == "appgen.format-result.v1"
    assert report["organize"] is True
    assert report["idempotent"] is True
    assert report["text"].index("table Invoice") < report["text"].index("table Customer")
    assert (
        "table Invoice {\n"
        "  id: int pk\n"
        "  invoice_number: string unique\n"
        "  // customer link\n"
        "  customer_id: int -> Customer.id\n"
        "  description: string\n"
        "  subtotal: decimal\n"
        "  tax: decimal\n"
        "  total: decimal = subtotal + tax\n"
        "  updated_at: string\n"
        "  index(total)\n"
        "}"
    ) in report["text"]
    assert result.returncode == 0, result.stderr
    assert payload["organize"] is True
    assert "  id: int pk" in payload["text"]


def test_formatter_contract_audit_proves_documented_formatter_guarantees() -> None:
    audit = formatter_contract_audit_dsl()
    check_ids = {check["check"] for check in audit["checks"]}

    assert audit["format"] == "appgen.formatter-contract-audit.v1"
    assert audit["ok"] is True
    assert audit["check_count"] == len(audit["checks"])
    assert audit["passing_check_count"] == audit["check_count"]
    assert audit["failed_check_count"] == 0
    assert audit["comment_check_count"] >= 3
    assert audit["ordering_check_count"] >= 3
    assert audit["report_count"] == 2
    assert audit["idempotent_report_count"] == audit["report_count"]
    assert audit["changed_report_count"] == audit["report_count"]
    assert audit["diagnostic_count"] >= 0
    assert audit["diagnostic_error_count"] == 0
    assert audit["diagnostic_severity_counts"]["hint"] == audit["diagnostic_count"]
    assert audit["text_byte_count"] > 0
    assert {
        "idempotent",
        "file_level_comments_preserved",
        "declaration_comments_preserved",
        "inline_comments_preserved",
        "modifier_ordering",
        "relationship_modifier_ordering",
        "organize_requested",
        "top_level_order_preserved",
        "organize_table_body_ordering",
    } <= check_ids
    assert audit["blocking_gaps"] == ()


def test_graph_suite_report_covers_required_kinds_and_formats() -> None:
    report = graph_suite_report_dsl(RELEASE_SAMPLE, source_name="release.appgen")

    assert report["format"] == "appgen.graph-suite-report.v1"
    assert report["ok"] is True
    assert report["required_kind_count"] == len(report["required_kinds"])
    assert report["present_kind_count"] == len(report["graph_reports"])
    assert report["missing_kind_count"] == 0
    assert report["missing_kinds"] == ()
    assert report["format_count"] == len(report["formats"]) == 3
    assert report["graph_report_count"] == len(report["graph_reports"])
    assert report["rendering_count"] == report["expected_rendering_count"]
    assert report["missing_rendering_count"] == 0
    assert report["missing_renderings"] == ()
    assert report["diagnostic_count"] == len(report["diagnostics"])
    assert report["check_count"] == len(report["checks"])
    assert report["passing_check_count"] == report["check_count"]
    assert report["blocking_gap_count"] == 0
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


def test_lint_text_output_uses_report_stage_order() -> None:
    payload = {
        "format": "appgen.lint-report.v1",
        "ok": True,
        "severity_counts": {"error": 0, "warning": 1, "info": 0, "hint": 0},
        "stage_names": ("policy", "syntax", "semantic"),
        "stages": {
            "syntax": {"diagnostic_count": 0},
            "semantic": {"diagnostic_count": 1},
            "policy": {"diagnostic_count": 2},
        },
        "diagnostics": (),
    }
    output = StringIO()

    with redirect_stdout(output):
        appgen_dsl._emit_tooling_payload(payload, as_json=False)

    assert "stages policy=2 syntax=0 semantic=1" in output.getvalue()


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
    assert plan["allowed_backend_count"] == len(plan["allowed_backends"])
    assert plan["change_count"] == len(plan["changes"])
    assert plan["destructive_change_count"] == sum(1 for change in plan["changes"] if change.get("destructive"))
    assert plan["diagnostic_count"] == len(plan["diagnostics"])
    assert plan["rename_hint_count"] == len(plan["rename_hints"])
    assert {change["kind"] for change in plan["changes"]} >= {
        "add_table",
        "add_field",
        "drop_field",
        "type_change",
    }
    assert any(change.get("requires_backfill") for change in plan["changes"])
    assert any(item["code"] == "AGX1101" for item in plan["diagnostics"])
    assert plan["coverage"]["format"] == "appgen.migration-coverage.v1"
    assert {"added_table", "added_field", "dropped_field", "type_change", "data_backfill_requirement"} <= set(
        plan["coverage"]["detected"]
    )


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
    assert {"unique_index_check_change", "pbc_ownership_transfer"} <= set(plan["coverage"]["detected"])


def test_migration_plan_coverage_tracks_required_detection_families() -> None:
    previous = """
    app Coverage { targets: web }
    table Customer { id: int pk; name: string required }
    table Invoice {
      id: int pk
      customer_id: int -> Customer.id
      subtotal: decimal default 0
      total: decimal = subtotal
      index(customer_id)
    }
    pbc Billing { owns: Invoice }
    """
    current = """
    app Coverage { targets: web }
    table Account { id: int pk; name: string required }
    table Invoice {
      id: int pk
      account_id: int -> Account.id
      subtotal: string
      tax: decimal required
      total: decimal = subtotal + tax
      unique(account_id)
    }
    pbc Finance { owns: Invoice }
    """

    plan = migration_plan_dsl(
        previous,
        current,
        backend="postgresql",
        rename_hints=("table:Customer=Account", "field:Invoice.customer_id=Invoice.account_id"),
    )
    detected = set(plan["coverage"]["detected"])

    assert plan["allowed_backend_count"] == len(plan["allowed_backends"])
    assert plan["change_count"] == len(plan["changes"])
    assert plan["destructive_change_count"] == sum(1 for change in plan["changes"] if change.get("destructive"))
    assert plan["diagnostic_count"] == len(plan["diagnostics"])
    assert plan["rename_hint_count"] == 2
    assert plan["coverage"]["required"] == (
        "added_table",
        "dropped_table",
        "renamed_table",
        "added_field",
        "dropped_field",
        "renamed_field",
        "type_change",
        "nullability_change",
        "default_change",
        "relationship_change",
        "unique_index_check_change",
        "calculated_field_change",
        "pbc_ownership_transfer",
        "data_backfill_requirement",
    )
    assert {
        "renamed_table",
        "renamed_field",
        "added_field",
        "type_change",
        "default_change",
        "relationship_change",
        "unique_index_check_change",
        "calculated_field_change",
        "pbc_ownership_transfer",
        "data_backfill_requirement",
    } <= detected


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


def test_appgen_nl_plan_subcommand_emits_json_and_text_contracts(tmp_path: Path) -> None:
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
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "nl-plan",
            str(path),
            "--prompt",
            "Add credit memos to accounts receivable",
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
    assert text_result.returncode == 0, text_result.stderr
    assert text_result.stdout.startswith("nl-plan ok: format=appgen.nl-plan.v1")
    assert f"intent={payload['intent']}" in text_result.stdout
    assert f"operations={len(payload['edit_operations'])}" in text_result.stdout
    assert f"patch_bytes={len(payload['dsl_patch'])}" in text_result.stdout
    assert f"tests={len(payload['test_plan'])}" in text_result.stdout
    assert f"token_notes={len(payload['token_budget_notes'])}" in text_result.stdout
    assert f"token-budget-notes {len(payload['token_budget_notes'])}" in text_result.stdout
    assert "operation-kinds add_table" in text_result.stdout
    assert f"lint format={payload['lint']['format']}: ok={payload['lint']['ok']}" in text_result.stdout
    assert (
        f"migration-preview format={payload['migration_preview']['format']} backend=postgresql: "
        f"changes={len(payload['migration_preview']['changes'])} "
        f"requires_approval={payload['migration_preview']['requires_approval']}"
    ) in text_result.stdout


def test_nl_plan_contract_audit_covers_supported_edit_operations_and_rejections() -> None:
    audit = nl_plan_contract_audit_dsl(TOOLING_SAMPLE, source_name="finance.appgen")
    case_ids = {case["id"] for case in audit["cases"]}

    assert audit["format"] == "appgen.nl-plan-contract-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["accepted_case_count"] == len(audit["required_edit_operations"])
    assert audit["rejected_case_count"] == 1
    assert audit["required_operation_count"] == len(audit["required_edit_operations"])
    assert set(audit["observed_operation_kinds"]) >= set(audit["required_edit_operations"])
    assert audit["observed_operation_kind_count"] >= audit["required_operation_count"]
    assert audit["observed_operation_kind_count"] == len(audit["observed_operation_kinds"])
    assert audit["missing_required_operation_kinds"] == ()
    assert audit["missing_required_operation_kind_count"] == 0
    assert audit["token_budget_case_count"] == audit["case_count"]
    assert set(audit["required_edit_operations"]) <= {
        "add_table",
        "add_field",
        "add_relationship",
        "add_view_section",
        "add_component_placement",
        "add_handler",
        "add_operation",
        "add_rule",
        "add_flow_transition",
        "add_pbc_include",
        "add_api_event_contract",
        "add_package_deployment_unit",
        "add_agent_skill_permission",
    }
    assert {
        "add_table",
        "add_field",
        "add_relationship",
        "add_view_section",
        "add_component_placement",
        "add_handler",
        "add_operation",
        "add_rule",
        "add_flow_transition",
        "add_pbc_include",
        "add_api_event_contract",
        "add_package_deployment_unit",
        "add_agent_skill_permission",
        "reject_unsupported",
    } <= case_ids
    assert audit["blocking_gap_count"] == 0
    assert audit["blocking_gaps"] == ()


def test_nl_plan_cli_audit_covers_all_supported_edit_operations(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_nl_plan_cli(tmp_path, TOOLING_SAMPLE)
    contract = nl_plan_contract_audit_dsl(TOOLING_SAMPLE, source_name="finance.appgen")

    assert audit["format"] == "appgen.nl-plan-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == audit["accepted_case_count"] + audit["rejected_case_count"] + audit["text_case_count"]
    assert audit["accepted_passing_case_count"] == audit["accepted_case_count"]
    assert audit["accepted_failing_case_count"] == 0
    assert audit["rejected_case_count"] == 1
    assert audit["text_case_count"] == 1
    assert tuple(audit["required_operation_kinds"]) == tuple(contract["required_edit_operations"])
    expected_case_ids = tuple(f"{kind}_json" for kind in contract["required_edit_operations"])
    assert audit["required_accepted_case_ids"] == expected_case_ids
    assert audit["observed_accepted_case_ids"] == expected_case_ids
    assert audit["missing_accepted_case_count"] == 0
    assert audit["missing_accepted_case_ids"] == ()
    assert audit["expected_operation_kind_by_case"] == {f"{kind}_json": kind for kind in contract["required_edit_operations"]}
    assert all(
        audit["expected_operation_kind_by_case"][case_id] in audit["operation_kinds_by_case"][case_id]
        for case_id in expected_case_ids
    )
    assert audit["missing_expected_operation_kind_case_count"] == 0
    assert audit["missing_expected_operation_kind_cases"] == ()
    assert set(audit["accepted_operation_kinds"]) >= set(contract["required_edit_operations"])
    assert audit["accepted_operation_kind_count"] == len(audit["accepted_operation_kinds"])
    assert audit["missing_accepted_operation_kind_count"] == 0
    assert audit["missing_accepted_operation_kinds"] == ()
    assert audit["accepted_case_count"] == len(contract["required_edit_operations"])
    assert audit["expected_payload_formats_by_case"] == {case_id: "appgen.nl-plan.v1" for case_id in expected_case_ids}
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["expected_exit_codes_by_case"] == {case_id: 0 for case_id in expected_case_ids}
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_cases"] == expected_case_ids
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["lint_ok_cases"] == expected_case_ids
    assert audit["missing_lint_ok_case_count"] == 0
    assert audit["missing_lint_ok_cases"] == ()
    assert audit["migration_format_cases"] == expected_case_ids
    assert audit["missing_migration_format_case_count"] == 0
    assert audit["missing_migration_format_cases"] == ()
    assert audit["test_plan_cases"] == expected_case_ids
    assert audit["missing_test_plan_case_count"] == 0
    assert audit["missing_test_plan_cases"] == ()
    assert audit["token_budget_cases"] == expected_case_ids
    assert audit["missing_token_budget_case_count"] == 0
    assert audit["missing_token_budget_cases"] == ()
    assert audit["blocking_cases"] == ()
    assert audit["blocking_case_count"] == 0
    assert audit["accepted_patch_bytes"] > 0
    assert audit["accepted_test_count"] >= len(contract["required_edit_operations"])
    assert audit["accepted_token_budget_notes"] >= len(contract["required_edit_operations"])
    assert audit["accepted_text_exit_code"] == 0
    assert audit["accepted_text_prefix"].startswith("nl-plan ok: format=appgen.nl-plan.v1")
    assert audit["required_text_markers"] == (
        "report_format",
        "lint_format",
        "migration_format",
        "test_plan",
        "token_budget_notes",
        "token_budget_note",
    )
    assert all(audit["text_markers"][marker] is True for marker in audit["required_text_markers"])
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_markers"] == ()
    assert audit["accepted_text_marker_count"] >= 6
    assert audit["accepted_text_has_report_format"] is True
    assert audit["accepted_text_has_lint_format"] is True
    assert audit["accepted_text_has_migration_format"] is True
    assert audit["accepted_text_test_plan_lines"]
    assert audit["accepted_text_test_plan_line_count"] == len(audit["accepted_text_test_plan_lines"])
    assert all(line.startswith("test-plan ") for line in audit["accepted_text_test_plan_lines"])
    assert any("lint_patched_dsl" in line for line in audit["accepted_text_test_plan_lines"])
    assert audit["accepted_text_has_token_notes"] is True
    assert audit["accepted_text_token_note_lines"]
    assert audit["accepted_text_token_note_line_count"] == len(audit["accepted_text_token_note_lines"])
    assert all(line.startswith("token-budget-note ") for line in audit["accepted_text_token_note_lines"])
    assert audit["rejected_ok"] is True
    assert audit["rejected_case_id"] == "reject_out_of_dsl_generated_code"
    assert audit["rejected_exit_code"] == 1
    assert audit["expected_rejected_exit_codes_by_case"] == {"reject_out_of_dsl_generated_code": 1}
    assert audit["rejected_exit_codes_by_case"] == audit["expected_rejected_exit_codes_by_case"]
    assert audit["missing_rejected_exit_code_case_count"] == 0
    assert audit["missing_rejected_exit_code_cases"] == ()
    assert audit["rejected_payload_format"] == "appgen.nl-plan.v1"
    assert audit["expected_rejected_payload_formats_by_case"] == {
        "reject_out_of_dsl_generated_code": "appgen.nl-plan.v1"
    }
    assert audit["rejected_payload_formats_by_case"] == audit["expected_rejected_payload_formats_by_case"]
    assert audit["missing_rejected_payload_format_case_count"] == 0
    assert audit["missing_rejected_payload_format_cases"] == ()
    assert "AGX1201" in audit["rejected_diagnostic_codes"]
    assert audit["required_rejected_diagnostic_codes_by_case"] == {
        "reject_out_of_dsl_generated_code": ("AGX1201",)
    }
    assert audit["rejected_diagnostic_codes_by_case"]["reject_out_of_dsl_generated_code"] == ("AGX1201",)
    assert audit["missing_rejected_diagnostic_code_case_count"] == 0
    assert audit["missing_rejected_diagnostic_codes_by_case"] == {}
    assert audit["rejected_patch_empty_cases"] == ("reject_out_of_dsl_generated_code",)
    assert audit["missing_rejected_patch_empty_case_count"] == 0
    assert audit["missing_rejected_patch_empty_cases"] == ()


def test_appgen_migration_plan_subcommand_emits_json_and_text_contracts(tmp_path: Path) -> None:
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
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "migration-plan",
            str(previous),
            str(current),
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
    assert text_result.returncode == 0, text_result.stderr
    assert text_result.stdout.startswith("migration-plan ok: format=appgen.migration-plan.v1 backend=postgresql")
    assert "changes=2" in text_result.stdout
    assert f"migration-coverage format={payload['coverage']['format']}" in text_result.stdout
    assert f"detected={len(payload['coverage']['detected'])}" in text_result.stdout
    assert f"missing={len(payload['coverage']['missing'])}" in text_result.stdout
    assert "migration-detected added_table, relationship_change" in text_result.stdout
    assert "change add_table: Payment" in text_result.stdout
    assert "change add_relationship: Payment" in text_result.stdout


def test_migration_plan_text_reports_safe_alternatives_for_destructive_changes(tmp_path: Path) -> None:
    previous = tmp_path / "previous.appgen"
    current = tmp_path / "current.appgen"
    previous.write_text(
        """
app FinanceOps { targets: web }
table Customer { id: int pk; name: string required }
table Invoice { id: int pk; total: decimal default 0; note: string }
""",
        encoding="utf-8",
    )
    current.write_text(
        """
app FinanceOps { targets: web }
table Customer { id: int pk; name: string required; segment: string required }
table Invoice { id: int pk; total: string default 0 }
table CreditMemo { id: int pk; amount: decimal default 0 }
""",
        encoding="utf-8",
    )

    text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "migration-plan", str(previous), str(current)],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert text_result.returncode == 0, text_result.stderr
    assert "requires_approval=True" in text_result.stdout
    assert "safe-alternative drop_field" in text_result.stdout
    assert "safe-alternative type_change" in text_result.stdout


def test_lsp_service_uses_shared_semantic_model_for_core_editor_features() -> None:
    report = lsp_service_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        position=_position_of(TOOLING_SAMPLE, "SubmitInvoice"),
        prefix="In",
        rename_to="PostInvoice",
    )

    assert report["format"] == "appgen.lsp-service.v1"
    assert report["ok"] is True
    assert report["semantic_model_format"] == "appgen.semantic-model.v1"
    assert report["capabilities"]["features"]["textDocument/completion"] is True
    assert report["service_counts"]["diagnostic_count"] == len(report["publishDiagnostics"]["diagnostics"])
    assert report["service_counts"]["completion_count"] == len(report["completion"]["items"])
    assert report["service_counts"]["completion_missing_source_count"] == report["completionCoverage"]["missing_source_count"]
    assert report["service_counts"]["reference_count"] == len(report["references"]["locations"])
    assert report["service_counts"]["document_symbol_count"] == len(report["documentSymbol"]["symbols"])
    assert report["symbolCoverage"]["format"] == "appgen.lsp-symbol-coverage.v1"
    assert report["service_counts"]["symbol_required_kind_count"] == report["symbolCoverage"]["required_kind_count"]
    assert report["service_counts"]["document_symbol_missing_kind_count"] == len(report["symbolCoverage"]["document_missing"])
    assert report["service_counts"]["workspace_symbol_missing_kind_count"] == len(report["symbolCoverage"]["workspace_missing"])
    assert report["service_counts"]["code_action_count"] == len(report["codeAction"]["actions"])
    assert report["service_counts"]["workspace_symbol_count"] == len(report["workspaceSymbol"]["symbols"])
    assert report["service_counts"]["rename_edit_count"] >= 1
    assert not any(item["severity"] == 1 for item in report["publishDiagnostics"]["diagnostics"])
    assert any(item["label"] == "Invoice" for item in report["completion"]["items"])
    assert report["hover"]["ok"] is True
    assert report["definition"]["ok"] is True
    assert len(report["references"]["locations"]) >= 2
    assert any(symbol["name"] == "Invoice" for symbol in report["documentSymbol"]["symbols"])
    assert report["formatting"]["format"] == "appgen.lsp-formatting.v1"
    assert report["rename"]["ok"] is True
    assert "PostInvoice" in report["rename"]["workspace_edit"]["changes"]["finance.appgen"][0]["newText"]


def test_lsp_document_symbols_include_view_sections_components_and_handlers() -> None:
    source = """
    app OutlineDemo { targets: web }
    table Invoice { id: int pk; customer_id: int }
    view InvoiceForm for Invoice {
      Header: id, customer_id
      @ customer_id Lookup 0 0 4 1
      on Save -> SubmitInvoice
    }
    operation SubmitInvoice { draft -> done }
    """
    report = appgen_dsl.lsp_document_symbols_dsl(source, source_name="outline.appgen")
    view_symbol = next(symbol for symbol in report["symbols"] if symbol["name"] == "InvoiceForm")
    child_details = {(child["name"], child["detail"]) for child in view_symbol["children"]}

    assert report["format"] == "appgen.lsp-document-symbols.v1"
    assert report["ok"] is True
    assert ("Header", "view_section") in child_details
    assert ("customer_id", "component_binding") in child_details
    assert ("Save", "handler") in child_details


def test_lsp_hover_exposes_pbc_catalog_metadata_and_diagnostic_explanation() -> None:
    pbc_source = """
    app HoverDemo { targets: web }
    composition Suite { include pbc gl_core version 1.0.0 }
    """
    pbc_hover = appgen_dsl.lsp_hover_dsl(
        pbc_source,
        source_name="hover-pbc.appgen",
        position=_position_of(pbc_source, "gl_core"),
    )

    assert pbc_hover["format"] == "appgen.lsp-hover.v1"
    assert pbc_hover["ok"] is True
    assert any("PBC `gl_core`: General Ledger Core" in item for item in pbc_hover["contents"])
    assert any('"format": "appgen.lsp-pbc-hover.v1"' in item for item in pbc_hover["contents"])
    assert any('"api_count":' in item and '"event_count":' in item for item in pbc_hover["contents"])

    diagnostic_source = """
    app BadHover { targets: web }
    table Customer { id: int pk }
    view CustomerForm for Customer { Main: missing }
    """
    diagnostic_hover = appgen_dsl.lsp_hover_dsl(
        diagnostic_source,
        source_name="hover-diagnostic.appgen",
        position=_position_of(diagnostic_source, "missing"),
    )

    assert diagnostic_hover["ok"] is True
    assert any("AGX0402:" in item for item in diagnostic_hover["contents"])
    assert any('"code": "AGX0402"' in item for item in diagnostic_hover["contents"])
    assert any("database-backed form binding" in item for item in diagnostic_hover["contents"])


def test_lsp_hover_exposes_relationship_targets_and_lookup_resolution() -> None:
    source = """
app HoverDetails { targets: web }
table Customer { id: int pk; name: string }
table Invoice {
  id: int pk
  customer_id: int -> Customer.id [many-to-one]
  lookup customer_name (customer.name)
}
view InvoiceForm for Invoice {
  Main: customer.name, customer_id
  on Save -> SubmitInvoice
}
operation SubmitInvoice { draft -> posted }
"""

    relationship_hover = appgen_dsl.lsp_hover_dsl(
        source,
        source_name="hover-details.appgen",
        position=_position_of(source, "customer_id: int"),
    )
    lookup_hover = appgen_dsl.lsp_hover_dsl(
        source,
        source_name="hover-details.appgen",
        position=_position_of(source, "customer.name, customer_id"),
    )
    handler_hover = appgen_dsl.lsp_hover_dsl(
        source,
        source_name="hover-details.appgen",
        position=_position_of(source, "SubmitInvoice\n}"),
    )

    assert relationship_hover["format"] == "appgen.lsp-hover.v1"
    assert relationship_hover["ok"] is True
    assert any("relationship `Invoice.customer_id` -> `Customer.id`" in item for item in relationship_hover["contents"])
    assert any('"format": "appgen.lsp-relationship-hover.v1"' in item for item in relationship_hover["contents"])
    assert any('"cardinality": "many-to-one"' in item and '"alias": "customer"' in item for item in relationship_hover["contents"])
    assert lookup_hover["ok"] is True
    assert any("lookup `customer.name`" in item for item in lookup_hover["contents"])
    assert any('"format": "appgen.lsp-lookup-hover.v1"' in item for item in lookup_hover["contents"])
    assert any('"chain": ["Invoice.customer_id", "Customer.name"]' in item for item in lookup_hover["contents"])
    assert handler_hover["ok"] is True
    assert any("handler `InvoiceForm.Save` targets `SubmitInvoice` (operation)" in item for item in handler_hover["contents"])
    assert any('"format": "appgen.lsp-handler-target-hover.v1"' in item for item in handler_hover["contents"])
    assert any('"owner_kind": "view"' in item and '"target_kind": "operation"' in item for item in handler_hover["contents"])


def test_lsp_workspace_symbols_include_pbc_catalog_metadata_and_contracts() -> None:
    direct = appgen_dsl.lsp_workspace_symbols_dsl(
        "app WorkspaceCatalog { targets: web }\ntable CatalogProbe { id: int pk }\n",
        source_name="workspace-catalog.appgen",
        query="ledger",
    )
    pbc_symbols = [symbol for symbol in direct["symbols"] if symbol["data"].get("id") == "catalog.pbc.gl_core"]

    assert direct["format"] == "appgen.lsp-workspace-symbols.v1"
    assert direct["ok"] is True
    assert pbc_symbols
    assert pbc_symbols[0]["location"]["uri"] == "catalog://pbc/gl_core"
    assert pbc_symbols[0]["data"]["catalog_resolved"] is True
    assert pbc_symbols[0]["data"]["label"] == "General Ledger Core"

    documents = {"memory://app.appgen": "app WorkspaceCatalog { targets: web }\ntable CatalogProbe { id: int pk }\n"}
    rpc_responses, _ = appgen_dsl.lsp_server_handle_message(
        {"jsonrpc": "2.0", "id": 11, "method": "workspace/symbol", "params": {"query": "JournalPosted"}},
        documents,
    )
    contract_symbols = [
        symbol
        for symbol in rpc_responses[0]["result"]
        if symbol["name"] == "JournalPosted" and symbol["data"].get("pbc") == "gl_core"
    ]

    assert contract_symbols
    assert contract_symbols[0]["containerName"] == "gl_core"
    assert contract_symbols[0]["data"]["kind"] == "event"
    assert contract_symbols[0]["location"]["uri"].startswith("catalog://pbc/gl_core/event/")


def test_lsp_definition_resolves_pbc_catalog_keys_and_contracts() -> None:
    pbc_source = """
    app DefinitionCatalog { targets: web }
    composition Suite {
      include pbc gl_core version 1.0.0
      connect ap_automation event InvoiceApproved -> gl_core event JournalPosted
    }
    """
    pbc_definition = appgen_dsl.lsp_definition_dsl(
        pbc_source,
        source_name="definition-catalog.appgen",
        position=_position_of(pbc_source, "gl_core"),
    )
    event_definition = appgen_dsl.lsp_definition_dsl(
        pbc_source,
        source_name="definition-catalog.appgen",
        position=_position_of(pbc_source, "JournalPosted"),
    )
    documents = {"memory://definition-catalog.appgen": pbc_source}
    rpc_responses, _ = appgen_dsl.lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 12,
            "method": "textDocument/definition",
            "params": {
                "textDocument": {"uri": "memory://definition-catalog.appgen"},
                "position": _position_of(pbc_source, "JournalPosted"),
            },
        },
        documents,
    )

    assert pbc_definition["ok"] is True
    assert pbc_definition["location"]["uri"] == "catalog://pbc/gl_core"
    assert event_definition["ok"] is True
    assert event_definition["location"]["uri"] == "catalog://pbc/gl_core/event/JournalPosted"
    assert rpc_responses[0]["result"]["uri"] == "catalog://pbc/gl_core/event/JournalPosted"


def test_lsp_definition_uses_reference_context_for_enterprise_symbols() -> None:
    source = """
app DefinitionContext { targets: web }
table Ledger { id: int pk; gl_core: string }
pbc gl_core { datastore: postgresql }
event JournalPosted { topic: finance.journal }
api LedgerApi { POST "/journal" -> JournalPosted }
operation JournalPosted { draft -> done }
operation SubmitInvoice { draft -> done }
composition Suite {
  include pbc gl_core version 1.0.0
}
deploy Production {
  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
  resource SubmitInvoice cpu "500m"
  env SubmitInvoice QUEUE_URL
}
"""

    def position_at(index: int) -> dict:
        line = source.count("\n", 0, index)
        previous_newline = source.rfind("\n", 0, index)
        return {"line": line, "character": index if previous_newline < 0 else index - previous_newline - 1}

    pbc_ref = source.index("include pbc gl_core") + len("include pbc ")
    event_ref = source.index("-> JournalPosted") + len("-> ")
    unit_ref = source.index("health SubmitInvoice") + len("health ")
    pbc_decl_line = source.count("\n", 0, source.index("pbc gl_core"))
    event_decl_line = source.count("\n", 0, source.index("event JournalPosted"))
    unit_decl_line = source.count("\n", 0, source.index("unit SubmitInvoice"))

    pbc_definition = appgen_dsl.lsp_definition_dsl(
        source,
        source_name="definition-context.appgen",
        position=position_at(pbc_ref),
    )
    event_definition = appgen_dsl.lsp_definition_dsl(
        source,
        source_name="definition-context.appgen",
        position=position_at(event_ref),
    )
    deployment_definition = appgen_dsl.lsp_definition_dsl(
        source,
        source_name="definition-context.appgen",
        position=position_at(unit_ref),
    )

    assert pbc_definition["ok"] is True
    assert pbc_definition["location"]["uri"] == "definition-context.appgen"
    assert pbc_definition["location"]["range"]["start"]["line"] == pbc_decl_line
    assert event_definition["ok"] is True
    assert event_definition["location"]["range"]["start"]["line"] == event_decl_line
    assert deployment_definition["ok"] is True
    assert deployment_definition["location"]["range"]["start"]["line"] == unit_decl_line


def test_lsp_references_preserve_lexical_code_scope() -> None:
    source = """
app ReferenceScope { targets: web }
table Invoice { id: int pk }
view InvoiceForm for Invoice {
  Main: id
  on Save -> SubmitInvoice
}
operation SubmitInvoice { draft -> done }
audit ReferenceAudit {
  evidence: "SubmitInvoice"
}
// SubmitInvoice remains in this comment
/* SubmitInvoice remains in this block comment */
"""

    references = appgen_dsl.lsp_references_dsl(
        source,
        source_name="reference-scope.appgen",
        position=_position_of(source, "SubmitInvoice {"),
    )

    assert references["format"] == "appgen.lsp-references.v1"
    assert references["ok"] is True
    assert len(references["locations"]) == 2
    assert all(location["uri"] == "reference-scope.appgen" for location in references["locations"])
    assert {location["range"]["start"]["line"] for location in references["locations"]} == {
        source.count("\n", 0, source.index("on Save -> SubmitInvoice")),
        source.count("\n", 0, source.index("operation SubmitInvoice")),
    }


def test_lsp_references_include_pbc_catalog_contract_indexes() -> None:
    pbc_source = """
    app ReferenceCatalog { targets: web }
    composition Suite {
      include pbc gl_core version 1.0.0
      connect ap_automation event InvoiceApproved -> gl_core event JournalPosted
    }
    """
    pbc_references = appgen_dsl.lsp_references_dsl(
        pbc_source,
        source_name="references-catalog.appgen",
        position=_position_of(pbc_source, "gl_core"),
    )
    event_references = appgen_dsl.lsp_references_dsl(
        pbc_source,
        source_name="references-catalog.appgen",
        position=_position_of(pbc_source, "JournalPosted"),
    )
    documents = {"memory://references-catalog.appgen": pbc_source}
    rpc_responses, _ = appgen_dsl.lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 13,
            "method": "textDocument/references",
            "params": {
                "textDocument": {"uri": "memory://references-catalog.appgen"},
                "position": _position_of(pbc_source, "JournalPosted"),
            },
        },
        documents,
    )

    assert pbc_references["ok"] is True
    assert any(location["uri"] == "catalog://pbc/gl_core" for location in pbc_references["locations"])
    assert event_references["ok"] is True
    assert any(
        location["uri"] == "catalog://pbc/gl_core/event/JournalPosted"
        for location in event_references["locations"]
    )
    assert any(
        location["uri"] == "catalog://pbc/gl_core/event/JournalPosted"
        for location in rpc_responses[0]["result"]
    )


def test_lsp_json_rpc_audit_proves_advertised_provider_capabilities() -> None:
    broken_handler_source = """
app Bad { targets: web }
table Invoice { id: int pk }
view InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }
"""
    audit = appgen_dsl._tooling_audit_lsp_json_rpc(TOOLING_SAMPLE, broken_handler_source=broken_handler_source)
    capabilities = audit["initialize_capabilities"]

    assert audit["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert audit["ok"] is True
    assert audit["check_count"] == len(audit["checks"])
    assert audit["passing_check_count"] == audit["check_count"]
    assert audit["failing_check_count"] == 0
    assert audit["provider_count"] == 9
    assert audit["enabled_provider_count"] == audit["provider_count"]
    assert audit["missing_provider_count"] == 0
    assert audit["missing_providers"] == ()
    assert audit["provider_count"] == len(audit["provider_names"])
    assert audit["request_check_count"] == 8
    assert audit["passing_request_check_count"] == audit["request_check_count"]
    assert audit["request_check_ids"] == (
        "completion",
        "hover",
        "definition",
        "references",
        "document_symbols",
        "rename",
        "workspace_symbol",
        "workspace_symbol_catalog_metadata",
    )
    assert audit["code_action_count"] >= 1
    assert audit["formatting_edit_count"] >= 1
    assert audit["blocking_gap_count"] == 0
    assert audit["blocking_gaps"] == ()
    assert audit["method_contract_count"] == 11
    assert audit["passing_method_contract_count"] == audit["method_contract_count"]
    assert audit["missing_method_contract_count"] == 0
    assert audit["missing_method_contracts"] == ()
    assert set(audit["method_contract_names"]) == {
        "textDocument/didOpen",
        "textDocument/didChange",
        "textDocument/completion",
        "textDocument/hover",
        "textDocument/definition",
        "textDocument/references",
        "textDocument/documentSymbol",
        "textDocument/rename",
        "textDocument/codeAction",
        "textDocument/formatting",
        "workspace/symbol",
    }
    assert all(detail["advertised"] for detail in audit["method_contracts"].values())
    assert all(detail["exercised"] for detail in audit["method_contracts"].values())
    assert audit["method_contracts"]["textDocument/didOpen"]["provider"] == "notification"
    assert audit["method_contracts"]["textDocument/didChange"]["provider"] == "notification"
    assert audit["method_contracts"]["textDocument/codeAction"]["check"] == "code_action_request"
    assert audit["method_contracts"]["textDocument/formatting"]["check"] == "formatting_request"
    assert audit["editor_workflow_case_count"] == 14
    assert audit["editor_workflow_passing_case_count"] == audit["editor_workflow_case_count"]
    assert audit["editor_workflow_failing_case_count"] == 0
    assert audit["editor_workflow_failing_cases"] == ()
    assert audit["required_editor_workflow_case_ids"] == (
        "initialize",
        "open_diagnostics",
        "completion",
        "hover",
        "definition",
        "references",
        "document_symbols",
        "rename",
        "workspace_symbol",
        "change_diagnostics",
        "code_action",
        "formatting",
        "shutdown",
        "exit",
    )
    assert audit["editor_workflow_case_ids"] == audit["required_editor_workflow_case_ids"]
    assert audit["missing_editor_workflow_case_count"] == 0
    assert audit["missing_editor_workflow_cases"] == ()
    assert audit["editor_workflow_methods_by_case"] == audit["expected_editor_workflow_methods_by_case"]
    assert audit["missing_editor_workflow_method_case_count"] == 0
    assert audit["missing_editor_workflow_method_cases"] == ()
    assert audit["editor_workflow_result_shapes_by_case"] == audit["expected_editor_workflow_result_shapes_by_case"]
    assert audit["missing_editor_workflow_shape_case_count"] == 0
    assert audit["missing_editor_workflow_shape_cases"] == ()
    assert audit["editor_workflow_diagnostic_transition_ok"] is True
    assert audit["editor_workflow_shutdown_exit_ok"] is True
    workflow_cases = {case["id"]: case for case in audit["editor_workflow_results"]}
    assert workflow_cases["open_diagnostics"]["notification_method"] == "textDocument/publishDiagnostics"
    assert workflow_cases["change_diagnostics"]["notification_method"] == "textDocument/publishDiagnostics"
    assert workflow_cases["rename"]["result_shape"] == "workspace_edit"
    assert workflow_cases["exit"]["should_exit"] is True
    assert "enterprise_definition_context" in {check["check"] for check in audit["checks"]}
    assert "lexical_reference_scope" in {check["check"] for check in audit["checks"]}
    assert audit["lexical_reference_scope_ok"] is True
    assert audit["reference_scope_location_count"] == 2
    assert audit["reference_scope_expected_line_count"] == 2
    assert audit["reference_scope_matched_line_count"] == audit["reference_scope_expected_line_count"]
    assert audit["reference_scope_excluded_match_count"] == 0
    assert set(audit["reference_scope_lines"]) == set(audit["reference_scope_expected_lines"])
    assert not (set(audit["reference_scope_lines"]) & set(audit["reference_scope_excluded_lines"]))
    lexical_check = next(check for check in audit["checks"] if check["check"] == "lexical_reference_scope")
    assert lexical_check["detail"]["reference_scope_location_count"] == 2
    assert lexical_check["detail"]["reference_scope_excluded_match_count"] == 0
    assert "completion_context_filtering" in {check["check"] for check in audit["checks"]}
    assert audit["completion_context_count"] == 8
    assert audit["passing_completion_context_count"] == audit["completion_context_count"]
    assert audit["missing_completion_context_count"] == 0
    assert audit["missing_completion_contexts"] == ()
    assert audit["completion_context_missing_label_count"] == 0
    assert audit["completion_context_forbidden_label_count"] == 0
    assert set(audit["completion_context_names"]) == {
        "top_level",
        "table",
        "view",
        "flow",
        "composition",
        "deploy",
        "package",
        "agent",
    }
    assert audit["completion_context_missing_labels"] == {}
    assert audit["completion_context_forbidden_labels"] == {}
    assert all(result["ok"] for result in audit["completion_context_results"])
    assert all(not result["missing_labels"] for result in audit["completion_context_results"])
    assert all(not result["forbidden_labels"] for result in audit["completion_context_results"])
    assert "hover_relationship_lookup_depth" in {check["check"] for check in audit["checks"]}
    assert "hover_handler_target_depth" in {check["check"] for check in audit["checks"]}
    assert "hover_catalog_diagnostic_depth" in {check["check"] for check in audit["checks"]}
    assert "workspace_symbol_catalog_result_depth" in {check["check"] for check in audit["checks"]}
    assert "reference_catalog_index_depth" in {check["check"] for check in audit["checks"]}
    assert audit["missing_catalog_reference_context_count"] == 0
    assert audit["missing_catalog_reference_contexts"] == ()
    assert audit["catalog_reference_pbc_workspace_count"] >= 1
    assert audit["catalog_reference_pbc_catalog_count"] >= 1
    assert audit["catalog_reference_event_workspace_count"] >= 1
    assert audit["catalog_reference_event_catalog_count"] >= 1
    assert all(audit["catalog_reference_checks"].values())
    assert audit["catalog_reference_counts"]["pbc_catalog"] >= 1
    assert audit["catalog_reference_counts"]["event_catalog"] >= 1
    assert audit["definition_context_count"] == 5
    assert audit["passing_definition_context_count"] == audit["definition_context_count"]
    assert audit["missing_definition_context_count"] == 0
    assert audit["missing_definition_contexts"] == ()
    assert set(audit["definition_context_names"]) == {
        "pbc_include",
        "api_event_target",
        "deployment_health_target",
        "deployment_resource_target",
        "deployment_env_target",
    }
    assert all(audit["definition_context_matches"].values())
    assert audit["definition_context_expected_lines"] == audit["definition_context_observed_lines"]
    definition_check = next(check for check in audit["checks"] if check["check"] == "enterprise_definition_context")
    assert definition_check["detail"]["missing_definition_contexts"] == ()
    assert definition_check["detail"]["expected_lines"] == definition_check["detail"]["observed_lines"]
    assert audit["workspace_symbol_catalog_query_count"] == 2
    assert audit["workspace_symbol_catalog_passing_query_count"] == audit["workspace_symbol_catalog_query_count"]
    assert audit["workspace_symbol_catalog_missing_query_count"] == 0
    assert audit["workspace_symbol_catalog_missing_queries"] == ()
    assert audit["workspace_symbol_catalog_pbc_result_count"] >= 1
    assert audit["workspace_symbol_catalog_contract_result_count"] >= 1
    assert "catalog://pbc/gl_core" in audit["workspace_symbol_catalog_pbc_uris"]
    assert any(
        uri.startswith("catalog://pbc/gl_core/event/")
        for uri in audit["workspace_symbol_catalog_contract_uris"]
    )
    assert "gl_core" in audit["workspace_symbol_catalog_pbc_keys"]
    assert "JournalPosted" in audit["workspace_symbol_catalog_contract_names"]
    assert audit["required_hover_surface_count"] == 5
    assert audit["observed_hover_surface_count"] == audit["required_hover_surface_count"]
    assert audit["missing_hover_surface_count"] == 0
    assert audit["missing_hover_surfaces"] == ()
    assert set(audit["required_hover_surfaces"]) == {
        "pbc_catalog",
        "diagnostic_explanation",
        "relationship",
        "lookup",
        "handler_target",
    }
    assert set(audit["observed_hover_surfaces"]) == set(audit["required_hover_surfaces"])
    assert all(audit["hover_surface_checks"].values())
    assert "workspace_document_scan_and_rename" in {check["check"] for check in audit["checks"]}
    assert capabilities["completionProvider"]["triggerCharacters"]
    assert capabilities["hoverProvider"] is True
    assert capabilities["definitionProvider"] is True
    assert capabilities["referencesProvider"] is True
    assert capabilities["documentSymbolProvider"] is True
    assert capabilities["renameProvider"]["prepareProvider"] is False
    assert capabilities["codeActionProvider"] is True
    assert capabilities["documentFormattingProvider"] is True
    assert capabilities["workspaceSymbolProvider"] is True


def test_lsp_completion_coverage_proves_required_context_sources() -> None:
    source = """
    app CompletionDemo { targets: web, mobile, desktop }
    table Customer { id: int pk; name: string }
    table Invoice {
      id: int pk
      customer_id: int -> Customer.id
      lookup customer_name (customer.name)
    }
    view InvoiceForm for Invoice {
      Main: customer.name
      @ customer.name Lookup 0 0 6 1
      on Save -> SubmitInvoice
    }
    flow SubmitInvoice { draft -> reviewed; reviewed -> posted }
    operation ReverseInvoice { posted -> reversed }
    component CustomerLookup { on Select -> SubmitInvoice }
    composition Suite { include pbc gl_core version 1.0.0 }
    package MobileRelease { target: mobile; smoke: launch }
    deploy Production { unit SubmitInvoice as worker; health SubmitInvoice "/health" }
    llm LocalModel { provider: ollama; mode: local }
    agent Builder { provider: LocalModel; tools: write, schema }
    """

    coverage = completion_coverage_dsl(source, source_name="completion.appgen")
    service = lsp_service_dsl(source, source_name="completion.appgen")

    assert coverage["format"] == "appgen.completion-coverage.v1"
    assert coverage["missing"] == ()
    assert service["completionCoverage"]["missing"] == ()
    assert set(coverage["required"]) <= set(coverage["detected"])
    assert coverage["required_source_count"] == len(coverage["required"])
    assert coverage["detected_source_count"] == len(coverage["detected"])
    assert coverage["missing_source_count"] == 0
    assert coverage["label_count"] >= coverage["detected_source_count"]
    assert service["service_counts"]["completion_required_source_count"] == coverage["required_source_count"]
    assert service["service_counts"]["completion_detected_source_count"] == coverage["detected_source_count"]
    assert service["service_counts"]["completion_missing_source_count"] == 0
    assert coverage["source_label_counts"]["operation_targets"] >= 1
    assert coverage["source_label_counts"]["lookup_paths"] >= 1
    assert coverage["source_label_counts"]["pbc_apis"] >= 1
    assert coverage["source_label_counts"]["agent_skills"] >= 1
    assert "SubmitInvoice" in coverage["labels_by_source"]["operation_targets"]
    assert "customer.name" in coverage["labels_by_source"]["lookup_paths"]
    assert "Lookup" in coverage["labels_by_source"]["components"]
    assert "gl_core" in coverage["labels_by_source"]["pbc_keys"]
    assert "POST /journals" in coverage["labels_by_source"]["pbc_apis"]
    assert "POST /journals" in coverage["labels_by_source"]["pbc_commands"]
    assert "JournalPosted" in coverage["labels_by_source"]["pbc_events"]
    assert "mobile" in coverage["labels_by_source"]["package_targets"]
    assert "LocalModel" in coverage["labels_by_source"]["llm_providers"]
    assert "write" in coverage["labels_by_source"]["agent_skills"]
    assert any(symbol["name"] == "Invoice" for symbol in service["workspaceSymbol"]["symbols"])


def test_lsp_completion_filters_items_by_cursor_context() -> None:
    source = """
app CompletionContext { targets: web, mobile, desktop }
table Customer { id: int pk; name: string }
AuditFields { created_at: string }
table Invoice {

  id: int pk
  ... AuditFields
  customer_id: int -> Customer.id
  lookup customer_name (customer.name)
}
view InvoiceForm for Invoice {

  Main: customer.name
  @ customer.name Lookup 0 0 6 1
  on Save -> SubmitInvoice
}
flow SubmitInvoice {

  draft -> posted
}
operation ReverseInvoice { posted -> reversed }
composition Suite { include pbc gl_core version 1.0.0 }
deploy Production {

  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
}
package MobileRelease {

  target: mobile
  smoke: launch
}
llm LocalModel { provider: ollama; mode: local }
agent Builder { provider: LocalModel; tools: read, schema }
"""

    def labels_at(marker: str, offset: int, expected_context: str) -> set[str]:
        result = appgen_dsl.lsp_completion_dsl(
            source,
            source_name="completion-context.appgen",
            position=_position_of(source, marker) | {"character": _position_of(source, marker)["character"] + offset},
        )
        assert result["context"] == expected_context
        return {item["label"] for item in result["items"]}

    top_level = appgen_dsl.lsp_completion_dsl(
        source,
        source_name="completion-context.appgen",
        position={"line": 0, "character": 0},
    )
    assert top_level["context"] == "top_level"
    top_level_labels = {item["label"] for item in top_level["items"]}
    assert {"table", "view", "flow"} <= top_level_labels
    assert not {"Invoice", "gl_core", "LocalModel"} & top_level_labels

    table_labels = labels_at("table Invoice {\n\n", len("table Invoice {\n\n"), "table")
    assert {"id", "Customer", "lookup", "... AuditFields"} <= table_labels
    assert not {"gl_core", "LocalModel", "table"} & table_labels

    view_labels = labels_at("view InvoiceForm for Invoice {\n\n", len("view InvoiceForm for Invoice {\n\n"), "view")
    assert {"customer.name", "Lookup", "Save", "SubmitInvoice"} <= view_labels
    assert not {"gl_core", "LocalModel", "table"} & view_labels

    flow_labels = labels_at("flow SubmitInvoice {\n\n", len("flow SubmitInvoice {\n\n"), "flow")
    assert {"draft", "posted", "ReverseInvoice"} <= flow_labels
    assert not {"gl_core", "LocalModel", "Invoice"} & flow_labels

    composition_labels = labels_at("include pbc gl_core", len("include pbc "), "composition")
    assert {"gl_core", "JournalPosted", "POST /journals"} <= composition_labels
    assert not {"Invoice", "LocalModel", "table"} & composition_labels

    deploy_labels = labels_at("deploy Production {\n\n", len("deploy Production {\n\n"), "deploy")
    assert {"SubmitInvoice", "worker"} <= deploy_labels
    assert not {"gl_core", "LocalModel", "Invoice"} & deploy_labels

    package_labels = labels_at("package MobileRelease {\n\n", len("package MobileRelease {\n\n"), "package")
    assert {"mobile", "SubmitInvoice", "Package"} <= package_labels
    assert not {"gl_core", "LocalModel", "Invoice"} & package_labels

    agent_labels = labels_at("provider: LocalModel", len("provider: "), "agent")
    assert {"LocalModel", "read", "schema"} <= agent_labels
    assert not {"gl_core", "Invoice", "table"} & agent_labels


def test_lsp_rename_blocks_destructive_migration_impact() -> None:
    source = """
app RenameRisk { targets: web }

table Customer {
  id: int pk
  name: string
}

table Invoice {
  id: int pk
  customer_id: int -> Customer.id
}

view InvoiceForm for Invoice {
  Main: id, customer.name
}
"""

    report = lsp_service_dsl(
        source,
        source_name="rename-risk.appgen",
        position=_position_of(source, "id: int pk"),
        rename_to="identifier",
    )

    assert report["rename"]["ok"] is False
    assert report["rename"]["blocked"] is True
    assert report["rename"]["migration_preview"]["requires_approval"] is True
    assert any(item["code"] == "AGX1101" and item["severity"] == "error" for item in report["rename"]["blockers"])
    assert "add_rename_hint" in {fix["id"] for item in report["rename"]["blockers"] for fix in item["fixes"]}


def test_lsp_rename_preserves_comments_and_string_literals() -> None:
    source = """
app RenameScope { targets: web }
table Invoice { id: int pk; SubmitInvoice: string }
view InvoiceForm for Invoice {
  Main: id
  on Save -> SubmitInvoice
}
operation SubmitInvoice {
  draft -> done
}
audit RenameAudit {
  evidence: "SubmitInvoice"
}
deploy Production {
  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
}
// SubmitInvoice should remain in this comment
"""

    report = lsp_service_dsl(
        source,
        source_name="rename-scope.appgen",
        position=_position_of(source, "SubmitInvoice {\n"),
        rename_to="PostInvoice",
    )
    change = report["rename"]["workspace_edit"]["changes"]["rename-scope.appgen"][0]["newText"]

    assert report["rename"]["ok"] is True
    assert report["rename"]["lexical_scope"] == "operation_declarations_and_targets"
    assert report["rename"]["occurrence_count"] == 4
    assert "on Save -> PostInvoice" in change
    assert "operation PostInvoice" in change
    assert "unit PostInvoice as worker" in change
    assert 'health PostInvoice "/health"' in change
    assert "SubmitInvoice: string" in change
    assert 'evidence: "SubmitInvoice"' in change
    assert "// SubmitInvoice should remain in this comment" in change


def test_lsp_table_rename_candidate_scopes_references_and_preserves_fields() -> None:
    source = """
app RenameTables { targets: web }
table Customer { id: int pk; name: string }
table Invoice { id: int pk; Customer: string; customer_id: int -> Customer.id }
view CustomerForm for Customer { Main: id }
operation SubmitCustomer { draft -> done }
api CustomerApi { on Create -> SubmitCustomer }
report CustomerReport { source Customer -> CustomerApi }
audit RenameAudit { evidence: "Customer" }
// Customer remains in this comment
"""

    report = lsp_service_dsl(
        source,
        source_name="table-rename.appgen",
        position=_position_of(source, "Customer {"),
        rename_to="Account",
    )
    rename = report["rename"]
    change = rename["workspace_edit"]["changes"]["table-rename.appgen"][0]["newText"]

    assert rename["ok"] is False
    assert rename["blocked"] is True
    assert rename["lexical_scope"] == "table_declarations_and_targets"
    assert rename["occurrence_count"] == 4
    assert "table Account" in change
    assert "customer_id: int -> Account.id" in change
    assert "view CustomerForm for Account" in change
    assert "source Account -> CustomerApi" in change
    assert "Customer: string" in change
    assert 'evidence: "Customer"' in change
    assert "// Customer remains in this comment" in change
    assert any(item["code"] == "AGX1101" for item in rename["blockers"])


def test_lsp_view_rename_candidate_scopes_menu_targets_and_preserves_operation() -> None:
    source = """
app RenameViews { targets: web }
table Invoice { id: int pk; InvoiceForm: string }
view InvoiceForm for Invoice { Main: id }
operation InvoiceForm { draft -> done }
menu MainMenu { item invoices -> InvoiceForm; on Open -> InvoiceForm }
audit RenameAudit { evidence: "InvoiceForm" }
// InvoiceForm remains in this comment
"""

    report = lsp_service_dsl(
        source,
        source_name="view-rename.appgen",
        position=_position_of(source, "InvoiceForm for"),
        rename_to="InvoiceReviewForm",
    )
    rename = report["rename"]
    change = rename["workspace_edit"]["changes"]["view-rename.appgen"][0]["newText"]

    assert rename["ok"] is False
    assert rename["blocked"] is True
    assert rename["lexical_scope"] == "view_declarations_and_targets"
    assert rename["occurrence_count"] == 2
    assert "view InvoiceReviewForm for Invoice" in change
    assert "item invoices -> InvoiceReviewForm" in change
    assert "InvoiceForm: string" in change
    assert "operation InvoiceForm" in change
    assert "on Open -> InvoiceForm" in change
    assert 'evidence: "InvoiceForm"' in change
    assert "// InvoiceForm remains in this comment" in change
    assert any(item["code"] == "AGX1101" for item in rename["blockers"])


def test_lsp_field_rename_candidate_scopes_table_and_views() -> None:
    source = """
app RenameFields { targets: web }
table Invoice {
  id: int pk
  total: decimal
  tax: decimal
  customer_id: int -> Customer.id
  balance: decimal = total + tax
}
table Customer { id: int pk; total: decimal }
view InvoiceForm for Invoice {
  Main: total, balance
  @ total NumberEdit 0 0 4 1
  on Save -> total
  Extra: customer.total
}
operation total { draft -> done }
audit RenameAudit { evidence: "total" }
// total remains in this comment
"""

    report = lsp_service_dsl(
        source,
        source_name="field-rename.appgen",
        position=_position_of(source, "total: decimal"),
        rename_to="amount",
    )
    rename = report["rename"]
    change = rename["workspace_edit"]["changes"]["field-rename.appgen"][0]["newText"]

    assert rename["ok"] is False
    assert rename["blocked"] is True
    assert rename["lexical_scope"] == "field_declarations_and_bindings"
    assert rename["occurrence_count"] == 4
    assert "amount: decimal" in change
    assert "balance: decimal = amount + tax" in change
    assert "Main: amount, balance" in change
    assert "@ amount NumberEdit" in change
    assert "table Customer { id: int pk; total: decimal }" in change
    assert "on Save -> total" in change
    assert "Extra: customer.total" in change
    assert "operation total" in change
    assert 'evidence: "total"' in change
    assert "// total remains in this comment" in change
    assert any(item["code"] == "AGX1101" for item in rename["blockers"])


def test_lsp_enterprise_rename_candidates_scope_pbc_contract_package_and_deployment_units() -> None:
    source = """
app EnterpriseRefactors { targets: web }
table Ledger { id: int pk; gl_core: string }
view LedgerForm for Ledger {
  Main: id
  on Save -> JournalPosted
}
pbc gl_core { datastore: postgresql }
pbc ap_automation { datastore: postgresql }
event InvoiceApproved { topic: ap.invoice }
event JournalPosted { topic: finance.journal }
api LedgerApi { POST "/journal" -> JournalPosted }
operation JournalPosted { draft -> done }
operation SubmitInvoice { draft -> done }
operation PostInvoice { draft -> done }
composition Suite {
  include pbc gl_core version 1.0.0
  include pbc ap_automation version 1.0.0
  connect ap_automation domain_event InvoiceApproved -> gl_core domain_event JournalPosted
}
package FinanceRelease { target: web; smoke: launch }
deploy Production {
  unit gl_core as microservice
  unit SubmitInvoice as worker
  health gl_core "/healthz"
  health SubmitInvoice "/worker-health"
  resource gl_core cpu "500m"
  resource SubmitInvoice cpu "250m"
  env gl_core DATABASE_URL
  env SubmitInvoice QUEUE_URL
}
llm LocalModel { provider: ollama; mode: local }
agent Assistant { provider: LocalModel; tools: read }
audit RenameAudit { evidence: "gl_core JournalPosted FinanceRelease SubmitInvoice" }
// gl_core JournalPosted FinanceRelease SubmitInvoice remain in this comment
"""

    pbc_report = lsp_service_dsl(
        source,
        source_name="enterprise-rename.appgen",
        position=_position_of(source, "gl_core {"),
        rename_to="ledger_core",
    )["rename"]
    pbc_change = pbc_report["workspace_edit"]["changes"]["enterprise-rename.appgen"][0]["newText"]
    assert pbc_report["blocked"] is True
    assert pbc_report["lexical_scope"] == "pbc_declarations_and_targets"
    assert pbc_report["occurrence_count"] == 7
    assert "pbc ledger_core" in pbc_change
    assert "include pbc ledger_core" in pbc_change
    assert "-> ledger_core domain_event JournalPosted" in pbc_change
    assert "unit ledger_core as microservice" in pbc_change
    assert 'health ledger_core "/healthz"' in pbc_change
    assert "resource ledger_core cpu" in pbc_change
    assert "env ledger_core DATABASE_URL" in pbc_change
    assert "gl_core: string" in pbc_change
    assert 'evidence: "gl_core JournalPosted FinanceRelease SubmitInvoice"' in pbc_change

    event_report = lsp_service_dsl(
        source,
        source_name="enterprise-rename.appgen",
        position=_position_of(source, "JournalPosted {"),
        rename_to="LedgerPosted",
    )["rename"]
    event_change = event_report["workspace_edit"]["changes"]["enterprise-rename.appgen"][0]["newText"]
    assert event_report["ok"] is True
    assert event_report["lexical_scope"] == "event_declarations_and_targets"
    assert event_report["occurrence_count"] == 3
    assert "event LedgerPosted" in event_change
    assert 'POST "/journal" -> LedgerPosted' in event_change
    assert "domain_event LedgerPosted" in event_change
    assert "operation JournalPosted" in event_change
    assert "on Save -> JournalPosted" in event_change

    package_report = lsp_service_dsl(
        source,
        source_name="enterprise-rename.appgen",
        position=_position_of(source, "FinanceRelease {"),
        rename_to="WebRelease",
    )["rename"]
    package_change = package_report["workspace_edit"]["changes"]["enterprise-rename.appgen"][0]["newText"]
    assert package_report["ok"] is True
    assert package_report["lexical_scope"] == "package_declarations_and_targets"
    assert package_report["occurrence_count"] == 1
    assert "package WebRelease" in package_change
    assert 'evidence: "gl_core JournalPosted FinanceRelease SubmitInvoice"' in package_change

    unit_report = lsp_service_dsl(
        source,
        source_name="enterprise-rename.appgen",
        position=_position_of(source, "SubmitInvoice as worker"),
        rename_to="PostInvoice",
    )["rename"]
    unit_change = unit_report["workspace_edit"]["changes"]["enterprise-rename.appgen"][0]["newText"]
    assert unit_report["ok"] is True
    assert unit_report["lexical_scope"] == "deployment_unit_declarations_and_targets"
    assert unit_report["occurrence_count"] == 4
    assert "unit PostInvoice as worker" in unit_change
    assert 'health PostInvoice "/worker-health"' in unit_change
    assert "resource PostInvoice cpu" in unit_change
    assert "env PostInvoice QUEUE_URL" in unit_change
    assert "operation SubmitInvoice" in unit_change
    assert "operation PostInvoice" in unit_change
    assert "// gl_core JournalPosted FinanceRelease SubmitInvoice remain in this comment" in unit_change


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


def test_lsp_code_action_apply_patches_missing_operation_and_lookup_directive(tmp_path: Path) -> None:
    missing_operation = """
    app Bad { targets: web }
    table Invoice { id: int pk }
    view InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }
    """
    operation = apply_lsp_code_action_dsl(
        missing_operation,
        source_name="bad.appgen",
        action_id="create_operation_from_handler",
    )

    assert operation["format"] == "appgen.lsp-code-action-apply.v1"
    assert operation["ok"] is True
    assert operation["changed"] is True
    assert "operation SubmitInvoice" in operation["patched_source"]
    assert operation["lint"]["ok"] is True

    missing_lookup = """
    app BadLookup { targets: web }
    table Customer { id: int pk; name: string }
    table Invoice { id: int pk; customer_id: int -> Customer.id }
    view InvoiceForm for Invoice { Main: customer_name }
    """
    lookup = apply_lsp_code_action_dsl(
        missing_lookup,
        source_name="lookup.appgen",
        action_id="add_lookup_directive",
    )

    assert lookup["changed"] is True
    assert "lookup customer_name (customer.name)" in lookup["patched_source"]
    assert lookup["lint"]["ok"] is True
    assert lookup["applied_edits"]

    missing_relationship = """
    app MissingLookupRelationship { targets: web }
    table Customer { id: int pk; name: string }
    table Invoice { id: int pk }
    view InvoiceForm for Invoice { Main: customer.name }
    """
    relationship = apply_lsp_code_action_dsl(
        missing_relationship,
        source_name="relationship.appgen",
        action_id="add_relationship_for_lookup_path",
    )

    assert relationship["changed"] is True
    assert "customer_id: int -> Customer.id" in relationship["patched_source"]
    assert relationship["lint"]["ok"] is True

    source_path = tmp_path / "bad.appgen"
    source_path.write_text(missing_operation, encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lsp",
            str(source_path),
            "--apply-code-action",
            "create_operation_from_handler",
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lsp",
            str(source_path),
            "--apply-code-action",
            "create_operation_from_handler",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    unknown_text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lsp",
            str(source_path),
            "--apply-code-action",
            "missing_action",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert text_result.returncode == 0, text_result.stderr
    assert payload["format"] == "appgen.lsp-code-action-apply.v1"
    assert "operation SubmitInvoice" in payload["patched_source"]
    assert text_result.stdout.startswith(
        "lsp-code-action ok: format=appgen.lsp-code-action-apply.v1 action=create_operation_from_handler"
    )
    assert "changed=True" in text_result.stdout
    assert "lint_ok=True" in text_result.stdout
    assert unknown_text_result.returncode == 1
    assert unknown_text_result.stdout.startswith(
        "lsp-code-action failed: format=appgen.lsp-code-action-apply.v1 action=missing_action"
    )
    assert "available-actions " in unknown_text_result.stdout
    assert "create_operation_from_handler" in unknown_text_result.stdout
    assert "error AGX0100: Unknown code action: missing_action" in unknown_text_result.stdout


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

    missing_relationship_source = """
    app BadRelationship { targets: web }
    table Customer { id: int pk; name: string }
    table Invoice { id: int pk }
    view InvoiceForm for Invoice { Main: customer.name }
    """
    relationship_action_ids = {
        action["data"]["id"]
        for action in lsp_service_dsl(missing_relationship_source, source_name="relationship.appgen")["codeAction"]["actions"]
    }
    assert "add_relationship_for_lookup_path" in relationship_action_ids


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
    pbc_contract_source = """
    app BadPbcContract { targets: web }
    table Thing { id: int pk }
    view ThingForm for Thing { Main: id }
    composition Suite {
      include pbc gl_core version 1.0.0
      include pbc ap_automation version 1.0.0
      connect ap_automation domain_event MissingEvent -> gl_core domain_event MissingCommand
    }
    """

    pbc_actions = {action["data"]["id"] for action in lsp_service_dsl(pbc_source, source_name="pbc.appgen")["codeAction"]["actions"]}
    agent_actions = {action["data"]["id"] for action in lsp_service_dsl(agent_source, source_name="agent.appgen")["codeAction"]["actions"]}
    pbc_event_contract = apply_lsp_code_action_dsl(
        pbc_contract_source,
        source_name="pbc.appgen",
        action_id="create_event_contract",
    )
    agent_permission = apply_lsp_code_action_dsl(
        agent_source,
        source_name="agent.appgen",
        action_id="add_missing_permission_for_agent_skill",
    )

    assert {"create_event_contract", "register_or_import_pbc_manifest"} <= pbc_actions
    assert "add_missing_permission_for_agent_skill" in agent_actions
    assert pbc_event_contract["ok"] is True
    assert "event MissingEvent" in pbc_event_contract["patched_source"]
    assert "event MissingCommand" in pbc_event_contract["patched_source"]
    assert agent_permission["ok"] is True
    assert "GeneratedResource: write" in agent_permission["patched_source"]


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


def test_lsp_code_action_apply_audit_proves_required_quick_fixes() -> None:
    audit = lsp_code_action_apply_audit_dsl()

    assert audit["format"] == "appgen.lsp-code-action-apply-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["required_case_ids"] == audit["required_action_ids"]
    assert audit["observed_case_ids"] == audit["observed_action_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["required_action_count"] == len(audit["required_action_ids"])
    assert audit["observed_action_count"] == len(audit["observed_action_ids"])
    assert audit["missing_required_action_count"] == 0
    assert audit["applied_edit_count"] >= audit["case_count"]
    assert audit["applied_edit_cases"] == audit["required_case_ids"]
    assert audit["missing_applied_edit_case_count"] == 0
    assert audit["missing_applied_edit_cases"] == ()
    assert audit["expected_text_by_case"]["create_missing_table"] == "table Missing"
    assert audit["expected_text_by_case"]["remove_invalid_runtime_picker_fields"] == "targets: web"
    assert audit["expected_text_matched_cases"] == audit["required_case_ids"]
    assert audit["missing_expected_text_case_count"] == 0
    assert audit["missing_expected_text_cases"] == ()
    assert audit["lint_passing_case_count"] == audit["case_count"]
    assert audit["lint_passing_cases"] == audit["required_case_ids"]
    assert audit["missing_lint_passing_case_count"] == 0
    assert audit["missing_lint_passing_cases"] == ()
    assert audit["lint_failing_case_count"] == 0
    assert audit["changed_case_count"] == audit["case_count"]
    assert audit["changed_cases"] == audit["required_case_ids"]
    assert audit["missing_changed_case_count"] == 0
    assert audit["missing_changed_cases"] == ()
    assert audit["cleanup_case_count"] == audit["case_count"]
    assert audit["cleanup_cases"] == audit["required_case_ids"]
    assert audit["missing_cleanup_case_count"] == 0
    assert audit["missing_cleanup_cases"] == ()
    assert audit["diagnostic_code_count"] == len(audit["diagnostic_codes"])
    assert audit["diagnostic_code_count"] >= audit["case_count"] - 2
    assert audit["blocking_gap_count"] == 0
    assert audit["blocking_gaps"] == ()
    assert audit["missing_required_action_ids"] == ()
    assert set(audit["required_action_ids"]) == set(audit["observed_action_ids"])
    assert {
        "create_missing_table",
        "create_missing_field",
        "create_calculated_field_for_binding",
        "create_operation_from_handler",
        "create_flow_from_handler",
        "add_lookup_directive",
        "add_relationship_for_lookup_path",
        "replace_typo_with_nearest_symbol",
        "replace_secret_literal_with_env",
        "remove_invalid_runtime_picker_fields",
        "create_event_contract",
        "register_or_import_pbc_manifest",
        "add_missing_permission_for_agent_skill",
        "add_package_for_app_target",
        "create_smoke_test_declaration",
    } <= set(audit["required_actions"])


def test_lsp_code_action_cli_audit_covers_required_agent_facing_quick_fixes(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_lsp_apply_code_action_cli(tmp_path)
    cases = {case["case"]: case for case in report["cases"]}

    assert report["format"] == "appgen.lsp-code-action-cli-audit.v1"
    assert report["ok"] is True
    assert report["case_count"] == len(report["cases"])
    assert report["passing_case_count"] == report["case_count"]
    assert report["failing_case_count"] == 0
    assert report["failing_cases"] == ()
    assert report["case_ids"] == report["observed_action_ids"]
    assert report["required_case_ids"] == report["required_action_ids"]
    assert report["observed_case_ids"] == report["observed_action_ids"]
    assert report["missing_case_count"] == 0
    assert report["missing_case_ids"] == ()
    assert report["exit_codes_by_case"] == report["expected_exit_codes_by_case"]
    assert set(report["expected_exit_codes_by_case"].values()) == {0}
    assert report["missing_exit_code_case_count"] == 0
    assert report["missing_exit_code_cases"] == ()
    assert report["payload_formats_by_case"] == report["expected_payload_formats_by_case"]
    assert set(report["expected_payload_formats_by_case"].values()) == {"appgen.lsp-code-action-apply.v1"}
    assert report["missing_payload_format_case_count"] == 0
    assert report["missing_payload_format_cases"] == ()
    assert report["ok_by_case"] == {case_id: True for case_id in report["required_case_ids"]}
    assert report["missing_ok_case_count"] == 0
    assert report["missing_ok_cases"] == ()
    assert report["required_action_count"] == len(report["required_action_ids"])
    assert report["observed_action_count"] == len(report["observed_action_ids"])
    assert report["missing_required_action_count"] == 0
    assert report["applied_edit_count"] >= report["case_count"]
    assert report["applied_edit_cases"] == report["required_case_ids"]
    assert report["missing_applied_edit_case_count"] == 0
    assert report["missing_applied_edit_cases"] == ()
    assert report["expected_text_case_count"] == report["case_count"]
    assert report["expected_text_matched_cases"] == report["required_case_ids"]
    assert report["missing_expected_text_case_count"] == 0
    assert report["missing_expected_text_cases"] == ()
    assert report["expected_text_by_case"]["create_missing_table"] == "table Missing"
    assert report["expected_text_by_case"]["replace_secret_literal_with_env"] == "api_key: OPENAI_API_KEY"
    assert report["forbidden_removed_case_count"] == report["case_count"]
    assert report["forbidden_removed_cases"] == report["required_case_ids"]
    assert report["missing_forbidden_removed_case_count"] == 0
    assert report["missing_forbidden_removed_cases"] == ()
    assert report["forbidden_text_by_case"]["replace_secret_literal_with_env"] == ('api_key: "sk-secret"',)
    assert report["forbidden_text_by_case"]["remove_invalid_runtime_picker_fields"] == (
        "runtime:",
        "stream:",
        "backend:",
    )
    assert report["lint_format_case_count"] == report["case_count"]
    assert report["lint_format_cases"] == report["required_case_ids"]
    assert report["missing_lint_format_case_count"] == 0
    assert report["missing_lint_format_cases"] == ()
    assert report["lint_passing_case_count"] == report["case_count"]
    assert report["lint_passing_cases"] == report["required_case_ids"]
    assert report["missing_lint_passing_case_count"] == 0
    assert report["missing_lint_passing_cases"] == ()
    assert report["lint_failing_case_count"] == 0
    assert report["changed_case_count"] == report["case_count"]
    assert report["changed_cases"] == report["required_case_ids"]
    assert report["missing_changed_case_count"] == 0
    assert report["missing_changed_cases"] == ()
    assert report["unchanged_case_count"] == 0
    assert report["blocking_gap_count"] == 0
    assert report["blocking_gaps"] == ()
    assert report["missing_required_action_ids"] == ()
    assert tuple(report["required_action_ids"]) == tuple(report["required_cli_actions"])
    assert set(report["required_action_ids"]) == set(report["observed_action_ids"])
    assert tuple(report["required_action_ids"]) == tuple(lsp_code_action_apply_audit_dsl()["required_action_ids"])
    assert {
        "create_missing_table",
        "create_missing_field",
        "create_calculated_field_for_binding",
        "create_operation_from_handler",
        "create_flow_from_handler",
        "add_lookup_directive",
        "add_relationship_for_lookup_path",
        "replace_typo_with_nearest_symbol",
        "replace_secret_literal_with_env",
        "remove_invalid_runtime_picker_fields",
        "create_event_contract",
        "register_or_import_pbc_manifest",
        "add_missing_permission_for_agent_skill",
        "add_package_for_app_target",
        "create_smoke_test_declaration",
    } <= set(report["required_cli_actions"])
    assert cases["create_missing_table"]["ok"] is True
    assert cases["create_missing_field"]["ok"] is True
    assert cases["create_calculated_field_for_binding"]["ok"] is True
    assert cases["create_operation_from_handler"]["ok"] is True
    assert cases["create_operation_from_handler"]["changed"] is True
    assert cases["create_operation_from_handler"]["applied_edit_count"] > 0
    assert cases["create_operation_from_handler"]["lint_ok"] is True
    assert cases["create_flow_from_handler"]["ok"] is True
    assert cases["add_lookup_directive"]["ok"] is True
    assert cases["add_lookup_directive"]["changed"] is True
    assert cases["add_lookup_directive"]["applied_edit_count"] > 0
    assert cases["add_relationship_for_lookup_path"]["ok"] is True
    assert cases["replace_typo_with_nearest_symbol"]["ok"] is True
    assert cases["add_package_for_app_target"]["ok"] is True
    assert cases["add_package_for_app_target"]["expected_text"] == "package WebPackage"
    assert cases["create_smoke_test_declaration"]["ok"] is True
    assert cases["create_smoke_test_declaration"]["expected_text"] == "test PublishSmoke"
    assert cases["add_lookup_directive"]["lint_ok"] is True
    assert cases["replace_secret_literal_with_env"]["ok"] is True
    assert cases["replace_secret_literal_with_env"]["forbidden_removed"] is True
    assert cases["replace_secret_literal_with_env"]["expected_text"] == "api_key: OPENAI_API_KEY"
    assert cases["remove_invalid_runtime_picker_fields"]["ok"] is True
    assert cases["remove_invalid_runtime_picker_fields"]["forbidden_removed"] is True
    assert cases["remove_invalid_runtime_picker_fields"]["expected_text"] == "targets: web"
    assert cases["create_event_contract"]["ok"] is True
    assert cases["register_or_import_pbc_manifest"]["ok"] is True
    assert cases["add_missing_permission_for_agent_skill"]["ok"] is True


def test_lsp_rename_cli_audit_covers_safe_and_blocked_renames(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_lsp_rename_cli(tmp_path, appgen_dsl._tooling_audit_sample_dsl())

    assert report["format"] == "appgen.lsp-rename-cli-audit.v1"
    assert report["ok"] is True
    assert report["scenario_count"] == 11
    assert report["passing_scenario_count"] == 11
    assert report["failing_scenario_count"] == 0
    assert report["failing_scenarios"] == ()
    assert report["scenario_ids"] == (
        "safe_flow_rename",
        "lexical_operation_scope",
        "blocked_table_scope",
        "blocked_view_scope",
        "blocked_pbc_scope",
        "event_scope",
        "package_scope",
        "deployment_unit_scope",
        "blocked_field_scope",
        "approval_blocker_json",
        "approval_blocker_text",
    )
    assert report["observed_scenario_ids"] == report["required_scenario_ids"]
    assert report["missing_scenario_count"] == 0
    assert report["missing_scenario_ids"] == ()
    assert report["observed_modes_by_scenario"] == report["required_modes_by_scenario"]
    assert report["missing_mode_scenario_count"] == 0
    assert report["missing_mode_scenarios"] == ()
    assert report["observed_scopes_by_scenario"] == report["required_scopes_by_scenario"]
    assert report["missing_scope_scenario_count"] == 0
    assert report["missing_scope_scenarios"] == ()
    assert report["exit_codes_by_scenario"] == report["expected_exit_codes_by_scenario"]
    assert set(report["expected_exit_codes_by_scenario"].values()) == {0}
    assert report["missing_exit_code_scenario_count"] == 0
    assert report["missing_exit_code_scenarios"] == ()
    assert report["payload_formats_by_scenario"] == report["expected_payload_formats_by_scenario"]
    assert set(report["expected_payload_formats_by_scenario"].values()) == {"appgen.lsp-service.v1"}
    assert "approval_blocker_text" not in report["expected_payload_formats_by_scenario"]
    assert report["missing_payload_format_scenario_count"] == 0
    assert report["missing_payload_format_scenarios"] == ()
    assert report["ok_by_scenario"] == {scenario: True for scenario in report["required_scenario_ids"]}
    assert report["missing_ok_scenario_count"] == 0
    assert report["missing_ok_scenarios"] == ()
    assert report["safe_json_scenario_count"] == 5
    assert report["blocked_json_scenario_count"] == 5
    assert report["blocked_text_scenario_count"] == 1
    assert report["blocked_code_count"] >= 1
    assert report["blocked_fix_count"] >= 1
    assert report["safe_ok"] is True
    assert report["rename_format"] == "appgen.lsp-rename.v1"
    assert report["token"] == "SubmitInvoice"
    assert report["new_name"] == "PostInvoice"
    assert report["lexical_scope"] == "flow_declarations_and_targets"
    assert report["occurrence_count"] >= 2
    assert report["changed"] is True
    assert report["migration_format"] == "appgen.migration-plan.v1"
    assert report["lexical_scope_ok"] is True
    assert report["lexical_occurrence_count"] == 4
    assert report["lexical_symbol_scope"] == "operation_declarations_and_targets"
    assert report["lexical_field_preserved"] is True
    assert report["lexical_string_preserved"] is True
    assert report["lexical_comment_preserved"] is True
    assert report["table_scope_ok"] is True
    assert report["table_scope"] == "table_declarations_and_targets"
    assert report["table_occurrence_count"] == 4
    assert report["table_blocked"] is True
    assert report["table_field_preserved"] is True
    assert report["table_string_preserved"] is True
    assert report["table_comment_preserved"] is True
    assert report["view_scope_ok"] is True
    assert report["view_scope"] == "view_declarations_and_targets"
    assert report["view_occurrence_count"] == 2
    assert report["view_blocked"] is True
    assert report["view_field_preserved"] is True
    assert report["view_operation_preserved"] is True
    assert report["view_string_preserved"] is True
    assert report["view_comment_preserved"] is True
    assert report["pbc_scope_ok"] is True
    assert report["pbc_scope"] == "pbc_declarations_and_targets"
    assert report["pbc_occurrence_count"] == 7
    assert report["pbc_blocked"] is True
    assert report["pbc_field_preserved"] is True
    assert report["pbc_deployment_unit_updated"] is True
    assert report["pbc_string_preserved"] is True
    assert report["event_scope_ok"] is True
    assert report["event_scope"] == "event_declarations_and_targets"
    assert report["event_occurrence_count"] == 3
    assert report["event_operation_preserved"] is True
    assert report["event_handler_preserved"] is True
    assert report["package_scope_ok"] is True
    assert report["package_scope"] == "package_declarations_and_targets"
    assert report["package_occurrence_count"] == 1
    assert report["package_string_preserved"] is True
    assert report["deployment_scope_ok"] is True
    assert report["deployment_scope"] == "deployment_unit_declarations_and_targets"
    assert report["deployment_occurrence_count"] == 4
    assert report["deployment_operation_preserved"] is True
    assert report["field_scope_ok"] is True
    assert report["field_scope"] == "field_declarations_and_bindings"
    assert report["field_occurrence_count"] == 4
    assert report["field_blocked"] is True
    assert report["field_other_table_preserved"] is True
    assert report["field_handler_target_preserved"] is True
    assert report["field_lookup_path_preserved"] is True
    assert report["field_operation_preserved"] is True
    assert report["field_string_preserved"] is True
    assert report["field_comment_preserved"] is True
    assert report["blocked_ok"] is True
    assert report["blocked_exit_code"] == 0
    assert report["blocked_rename_format"] == "appgen.lsp-rename.v1"
    assert report["blocked_rename_ok"] is False
    assert report["blocked"] is True
    assert report["blocked_text_ok"] is True
    assert "rename ok=False" in report["blocked_text"]
    assert "format=appgen.lsp-rename.v1" in report["blocked_text"]
    assert "blocked=True" in report["blocked_text"]
    assert "blockers=1" in report["blocked_text"]
    assert "migration_format=appgen.migration-plan.v1" in report["blocked_text"]
    assert "requires_approval=True" in report["blocked_text"]
    assert report["blocked_code"] == "AGX1101"
    assert report["blocked_fix"] == "add_rename_hint"
    assert report["blocked_migration_format"] == "appgen.migration-plan.v1"
    assert report["blocked_requires_approval"] is True


def test_appgen_lsp_subcommand_emits_json_and_text_contracts(tmp_path: Path) -> None:
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
    text_result = subprocess.run(
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
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert text_result.returncode == 0, text_result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.lsp-service.v1"
    assert payload["capabilities"]["source_of_truth"] == "appgen.semantic-model.v1"
    assert text_result.stdout.startswith("lsp ok: format=appgen.lsp-service.v1 semantic_format=appgen.semantic-model.v1")
    assert f"diagnostics={len(payload['publishDiagnostics']['diagnostics'])}" in text_result.stdout
    assert f"completions={len(payload['completion']['items'])}" in text_result.stdout
    assert f"actions={len(payload['codeAction']['actions'])}" in text_result.stdout
    assert f"symbols={len(payload['documentSymbol']['symbols'])}" in text_result.stdout
    assert f"workspace_symbols={len(payload['workspaceSymbol']['symbols'])}" in text_result.stdout
    assert "source_of_truth=appgen.semantic-model.v1" in text_result.stdout
    assert f"completion_coverage format={payload['completionCoverage']['format']}" in text_result.stdout
    assert f"missing={len(payload['completionCoverage']['missing'])}" in text_result.stdout
    assert f"definition format={payload['definition']['format']} ok={payload['definition']['ok']}" in text_result.stdout
    assert f"references format={payload['references']['format']} locations={len(payload['references']['locations'])}" in text_result.stdout
    assert f"formatting format={payload['formatting']['format']} edits={len(payload['formatting']['edits'])}" in text_result.stdout
    assert f"hover_items={len(payload['hover']['contents'])}" in text_result.stdout


def test_lsp_json_rpc_server_handles_editor_lifecycle_from_shared_semantics() -> None:
    uri = "memory://finance.appgen"
    documents: dict[str, str] = {}

    init_responses, should_exit = lsp_server_handle_message(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        documents,
    )
    open_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": uri,
                    "languageId": "appgen",
                    "version": 1,
                    "text": TOOLING_SAMPLE,
                }
            },
        },
        documents,
    )
    completion_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/completion",
            "params": {"textDocument": {"uri": uri}, "position": _position_of(TOOLING_SAMPLE, "Invoice")},
        },
        documents,
    )
    symbols_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "textDocument/documentSymbol",
            "params": {"textDocument": {"uri": uri}},
        },
        documents,
    )
    rename_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "textDocument/rename",
            "params": {
                "textDocument": {"uri": uri},
                "position": _position_of(TOOLING_SAMPLE, "SubmitInvoice"),
                "newName": "PostInvoice",
            },
        },
        documents,
    )
    workspace_responses, _ = lsp_server_handle_message(
        {"jsonrpc": "2.0", "id": 5, "method": "workspace/symbol", "params": {"query": "Invoice"}},
        documents,
    )
    shutdown_responses, _ = lsp_server_handle_message(
        {"jsonrpc": "2.0", "id": 6, "method": "shutdown"},
        documents,
    )
    exit_responses, should_exit_after_exit = lsp_server_handle_message(
        {"jsonrpc": "2.0", "method": "exit"},
        documents,
    )

    assert should_exit is False
    assert init_responses[0]["result"]["capabilities"]["completionProvider"]["triggerCharacters"]
    assert open_responses[0]["method"] == "textDocument/publishDiagnostics"
    assert not any(item["severity"] == 1 for item in open_responses[0]["params"]["diagnostics"])
    assert any(item["label"] == "Invoice" for item in completion_responses[0]["result"]["items"])
    assert any(symbol["name"] == "Invoice" for symbol in symbols_responses[0]["result"])
    assert "PostInvoice" in rename_responses[0]["result"]["changes"][uri][0]["newText"]
    assert any(symbol["name"] == "Invoice" for symbol in workspace_responses[0]["result"])
    assert shutdown_responses[0]["result"] is None
    assert exit_responses == ()
    assert should_exit_after_exit is True


def test_appgen_lsp_stdio_subcommand_speaks_json_rpc_frames() -> None:
    uri = "memory://stdio-finance.appgen"
    payload = b"".join(
        (
            _rpc_frame({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
            _rpc_frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "appgen",
                            "version": 1,
                            "text": TOOLING_SAMPLE,
                        }
                    },
                }
            ),
            _rpc_frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}),
            _rpc_frame({"jsonrpc": "2.0", "method": "exit"}),
        )
    )
    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lsp", "--stdio"],
        input=payload,
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
    )
    responses = _read_rpc_frames(result.stdout)

    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert any(response.get("id") == 1 and response["result"]["capabilities"]["completionProvider"] for response in responses)
    assert any(response.get("method") == "textDocument/publishDiagnostics" for response in responses)
    assert any(response.get("id") == 2 and response.get("result") is None for response in responses)


def test_lsp_stdio_transport_audit_exercises_editor_requests() -> None:
    audit = appgen_dsl._tooling_audit_lsp_stdio_transport(TOOLING_SAMPLE)

    assert audit["format"] == "appgen.lsp-stdio-transport-audit.v1"
    assert audit["ok"] is True
    assert audit["exit_code"] == 0
    assert audit["total_message_count"] == 7
    assert audit["request_message_count"] == 4
    assert audit["notification_message_count"] == 3
    assert audit["response_count"] >= audit["request_message_count"]
    assert audit["id_response_count"] >= audit["request_message_count"]
    assert audit["expected_id_count"] == len(audit["expected_ids"]) == 4
    assert audit["missing_response_id_count"] == 0
    assert audit["missing_response_ids"] == ()
    assert audit["expected_response_ids_by_method"] == {
        "initialize": 1,
        "textDocument/completion": 2,
        "workspace/symbol": 3,
        "shutdown": 4,
    }
    assert audit["response_ids_by_method"] == audit["expected_response_ids_by_method"]
    assert audit["missing_response_method_count"] == 0
    assert audit["missing_response_methods"] == ()
    assert audit["notification_count"] >= 2
    assert audit["method_count"] >= 1
    assert audit["required_notification_methods"] == ("textDocument/publishDiagnostics",)
    assert "textDocument/publishDiagnostics" in audit["observed_notification_methods"]
    assert audit["missing_notification_method_count"] == 0
    assert audit["missing_notification_methods"] == ()
    assert audit["diagnostic_publication_count"] >= 2
    assert audit["changed_source_differs"] is True
    assert audit["changed_diagnostic_count"] >= 1
    assert audit["changed_error_count"] >= 1
    assert {"AGX0401", "AGX0402"} & set(audit["changed_diagnostic_codes"])
    assert audit["required_changed_diagnostic_code_families"] == {
        "unresolved_binding_or_table": ("AGX0401", "AGX0402"),
    }
    assert audit["changed_diagnostic_code_families"]["unresolved_binding_or_table"]
    assert audit["missing_changed_diagnostic_code_family_count"] == 0
    assert audit["missing_changed_diagnostic_code_families"] == ()
    assert audit["completion_response_count"] >= 1
    assert audit["workspace_symbol_response_count"] >= 1
    assert audit["shutdown_response_count"] >= 1
    assert {1, 2, 3, 4} <= set(audit["ids"])
    assert "textDocument/publishDiagnostics" in audit["methods"]


def test_lsp_json_rpc_server_serves_code_actions_formatting_and_did_change() -> None:
    bad_uri = "memory://bad-handler.appgen"
    format_uri = "memory://format.appgen"
    bad_source = """
app Bad { targets: web }
table Invoice { id: int pk }
view InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }
"""
    changed_source = bad_source.replace("Main: id", "Main: missing")
    format_source = "app FormatDemo { targets: web }\ntable Invoice { id: int pk }\n"
    documents: dict[str, str] = {}

    lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": bad_uri,
                    "languageId": "appgen",
                    "version": 1,
                    "text": bad_source,
                }
            },
        },
        documents,
    )
    change_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {"uri": bad_uri, "version": 2},
                "contentChanges": [{"text": changed_source}],
            },
        },
        documents,
    )
    code_action_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 12,
            "method": "textDocument/codeAction",
            "params": {
                "textDocument": {"uri": bad_uri},
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 4, "character": 0}},
            },
        },
        documents,
    )
    lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": format_uri,
                    "languageId": "appgen",
                    "version": 1,
                    "text": format_source,
                }
            },
        },
        documents,
    )
    formatting_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 13,
            "method": "textDocument/formatting",
            "params": {"textDocument": {"uri": format_uri}, "options": {"tabSize": 2, "insertSpaces": True}},
        },
        documents,
    )

    assert documents[bad_uri] == changed_source
    assert change_responses[0]["method"] == "textDocument/publishDiagnostics"
    assert any(item["severity"] == 1 for item in change_responses[0]["params"]["diagnostics"])
    action_ids = {item["data"]["id"] for item in code_action_responses[0]["result"]}
    assert {"create_operation_from_handler", "create_missing_field"} <= action_ids
    assert formatting_responses[0]["result"]
    assert "table Invoice" in formatting_responses[0]["result"][0]["newText"]


def test_lsp_json_rpc_server_resolves_symbols_across_open_workspace_documents() -> None:
    customer_uri = "memory://customer.appgen"
    invoice_uri = "memory://invoice.appgen"
    customer_source = """
app CustomerWorkspace { targets: web }
table Customer {
  id: int pk
  name: string
}
"""
    invoice_source = """
app InvoiceWorkspace { targets: web }
table Invoice {
  id: int pk
  customer_id: int -> Customer.id
}
view InvoiceForm for Invoice { Main: customer_id }
"""
    documents: dict[str, str] = {}
    for uri, source in ((customer_uri, customer_source), (invoice_uri, invoice_source)):
        lsp_server_handle_message(
            {
                "jsonrpc": "2.0",
                "method": "textDocument/didOpen",
                "params": {
                    "textDocument": {
                        "uri": uri,
                        "languageId": "appgen",
                        "version": 1,
                        "text": source,
                    }
                },
            },
            documents,
        )

    definition_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "textDocument/definition",
            "params": {
                "textDocument": {"uri": invoice_uri},
                "position": _position_of(invoice_source, "Customer.id"),
            },
        },
        documents,
    )
    reference_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "textDocument/references",
            "params": {
                "textDocument": {"uri": invoice_uri},
                "position": _position_of(invoice_source, "Customer.id"),
            },
        },
        documents,
    )
    completion_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": invoice_uri},
                "position": _position_of(invoice_source, "Customer.id"),
            },
        },
        documents,
    )
    workspace_responses, _ = lsp_server_handle_message(
        {"jsonrpc": "2.0", "id": 10, "method": "workspace/symbol", "params": {"query": "Customer"}},
        documents,
    )

    assert definition_responses[0]["result"]["uri"] == customer_uri
    assert {item["uri"] for item in reference_responses[0]["result"]} == {customer_uri, invoice_uri}
    assert any(
        item["label"] == "Customer" and item["data"]["source"] == "workspace_symbols"
        for item in completion_responses[0]["result"]["items"]
    )
    assert any(
        item["location"]["uri"] == customer_uri and item["name"] == "Customer"
        for item in workspace_responses[0]["result"]
    )


def test_lsp_json_rpc_server_renames_identifier_across_open_workspace_documents() -> None:
    operation_uri = "memory://operation.appgen"
    form_uri = "memory://form.appgen"
    operation_source = """
app OperationWorkspace { targets: web }
table Invoice { id: int pk }
operation SubmitInvoice {
  draft -> done
}
"""
    form_source = """
app FormWorkspace { targets: web }
table Invoice { id: int pk }
view InvoiceForm for Invoice {
  Main: id
  on Save -> SubmitInvoice
}
"""
    documents: dict[str, str] = {}
    for uri, source in ((operation_uri, operation_source), (form_uri, form_source)):
        lsp_server_handle_message(
            {
                "jsonrpc": "2.0",
                "method": "textDocument/didOpen",
                "params": {
                    "textDocument": {
                        "uri": uri,
                        "languageId": "appgen",
                        "version": 1,
                        "text": source,
                    }
                },
            },
            documents,
        )

    rename_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "textDocument/rename",
            "params": {
                "textDocument": {"uri": operation_uri},
                "position": _position_of(operation_source, "SubmitInvoice"),
                "newName": "PostInvoice",
            },
        },
        documents,
    )

    changes = rename_responses[0]["result"]["changes"]
    assert set(changes) == {operation_uri, form_uri}
    assert "operation PostInvoice" in changes[operation_uri][0]["newText"]
    assert "on Save -> PostInvoice" in changes[form_uri][0]["newText"]


def test_vscode_extension_contract_wires_appgen_language_server_and_commands() -> None:
    extension_dir = Path(__file__).resolve().parents[1] / "extensions" / "vscode-appgen-x"
    package = json.loads((extension_dir / "package.json").read_text(encoding="utf-8"))
    language_config = json.loads((extension_dir / "language-configuration.json").read_text(encoding="utf-8"))
    grammar = json.loads((extension_dir / "syntaxes" / "appgen.tmLanguage.json").read_text(encoding="utf-8"))
    source = (extension_dir / "src" / "extension.js").read_text(encoding="utf-8")

    commands = {item["command"] for item in package["contributes"]["commands"]}
    languages = package["contributes"]["languages"]

    assert package["main"] == "./src/extension.js"
    assert package["activationEvents"][0] == "onLanguage:appgen"
    assert {f"onCommand:{command}" for command in commands} <= set(package["activationEvents"])
    assert languages[0]["id"] == "appgen"
    assert {".appgen", ".ag", ".ags"} <= set(languages[0]["extensions"])
    assert package["contributes"]["grammars"][0]["path"] == "./syntaxes/appgen.tmLanguage.json"
    assert {
        "appgen.lint",
        "appgen.semantic",
        "appgen.previewSemantic",
        "appgen.format",
        "appgen.graph",
        "appgen.previewGraph",
        "appgen.explain",
        "appgen.generate",
        "appgen.previewArtifacts",
        "appgen.package",
        "appgen.pbcCatalog",
        "appgen.restartLanguageServer",
    } <= commands
    command_palette = {item["command"] for item in package["contributes"]["menus"]["commandPalette"]}
    assert commands <= command_palette
    assert package["contributes"]["configuration"]["properties"]["appgen.command"]["default"] == "appgen"
    assert language_config["comments"]["lineComment"] == "//"
    assert grammar["scopeName"] == "source.appgen"
    assert '["lsp", "--stdio"]' in source
    assert '["semantic", activeFile(), "--json"]' in source
    assert '["semantic", file, "--json"]' in source
    assert "renderSemanticModel" in source
    assert "registerCompletionItemProvider" in source
    assert "registerHoverProvider" in source
    assert "registerDefinitionProvider" in source
    assert "registerReferenceProvider" in source
    assert "registerDocumentSymbolProvider" in source
    assert "registerWorkspaceSymbolProvider" in source
    assert "registerRenameProvider" in source
    assert "asRenameWorkspaceEdit" in source
    assert "AppGen-X rename blocked" in source
    assert "registerCodeActionsProvider" in source
    assert "registerDocumentFormattingEditProvider" in source
    assert '["pbc", "list", "--json"]' in source
    assert "renderPbcCatalog" in source
    assert "renderGraphPreview" in source
    assert "renderArtifactPreview" in source
    assert "createWebviewPanel" in source
    audit = appgen_dsl._tooling_audit_vscode_extension(Path(__file__).resolve().parents[1])
    assert audit["format"] == "appgen.vscode-extension-audit.v1"
    assert audit["ok"] is True
    assert audit["checks"]["language_metadata"] is True
    assert audit["checks"]["command_activation_events"] is True
    assert audit["checks"]["command_palette"] is True
    assert audit["checks"]["cli_command_configuration"] is True
    assert {".appgen", ".ag", ".ags"} <= set(audit["language_extensions"])
    assert audit["language_extension_count"] == len(audit["language_extensions"])
    assert audit["command_count"] == len(audit["commands"])
    assert audit["required_command_count"] == len(audit["required_commands"])
    assert audit["required_command_count"] >= 12
    assert audit["missing_command_count"] == 0
    assert audit["missing_commands"] == ()
    assert audit["command_palette_count"] >= audit["required_command_count"]
    assert audit["missing_command_palette_count"] == 0
    assert audit["missing_command_palette"] == ()
    assert audit["activation_event_count"] == len(audit["activation_events"])
    assert audit["required_activation_event_count"] == len(audit["required_activation_events"])
    assert audit["missing_activation_event_count"] == 0
    assert audit["missing_activation_events"] == ()
    assert "onLanguage:appgen" in audit["activation_events"]
    assert {f"onCommand:{command}" for command in audit["required_commands"]} <= set(audit["activation_events"])
    assert set(audit["required_commands"]) <= set(audit["command_palette"])
    assert "appgen.command" in audit["configuration_properties"]
    assert audit["configuration_property_count"] == len(audit["configuration_properties"])
    assert audit["checks"]["diagnostics_collection"] is True
    assert audit["checks"]["cli_command_contracts"] is True
    assert audit["checks"]["webview_renderers"] is True
    assert audit["provider_marker_count"] == len(audit["provider_markers"])
    assert audit["provider_marker_count"] >= 10
    assert audit["missing_provider_marker_count"] == 0
    assert audit["missing_provider_markers"] == ()
    assert audit["command_cli_marker_count"] == len(audit["command_cli_markers"])
    assert audit["missing_command_cli_marker_count"] == 0
    assert audit["missing_command_cli_markers"] == ()
    assert audit["webview_marker_count"] == len(audit["webview_markers"])
    assert audit["missing_webview_marker_count"] == 0
    assert audit["missing_webview_markers"] == ()
    assert '["generate", file, "--out", out, "--allow-warnings", "--json"]' in audit["command_cli_markers"]
    assert '["semantic", activeFile(), "--json"]' in audit["command_cli_markers"]
    assert '["semantic", file, "--json"]' in audit["command_cli_markers"]


def test_release_verifier_report_covers_package_pbc_and_deployment_evidence() -> None:
    report = release_verifier_report_dsl(RELEASE_SAMPLE, source_name="release.appgen", targets=("all",))

    assert report["format"] == "appgen.release-verifier-report.v1"
    assert report["ok"] is True
    assert set(report["reports"]) == {"web", "mobile", "desktop", "pbc", "deployment"}
    assert report["target_count"] == len(report["targets"]) == 5
    assert report["report_count"] == len(report["reports"]) == 5
    assert report["check_count"] == len(report["checks"]) == 5
    assert report["passing_check_count"] == report["check_count"]
    assert report["failing_check_count"] == 0
    assert report["diagnostic_count"] == len(report["diagnostics"])
    assert report["evidence_artifact_count"] == len(report["evidence_bundle"]["artifacts"])
    assert report["written_artifact_count"] == 0
    assert report["reports"]["web"]["format"] == "appgen.web-verifier.v1"
    assert report["reports"]["mobile"]["format"] == "appgen.mobile-verifier.v1"
    assert report["reports"]["desktop"]["format"] == "appgen.desktop-verifier.v1"
    assert report["reports"]["pbc"]["format"] == "appgen.pbc-verifier.v1"
    assert report["reports"]["deployment"]["format"] == "appgen.deployment-verifier.v1"
    assert all(item["check_count"] == len(item["checks"]) for item in report["reports"].values())
    assert all(item["passing_check_count"] == item["check_count"] for item in report["reports"].values())
    assert all(item["blocking_gap_count"] == len(item["blocking_gaps"]) == 0 for item in report["reports"].values())
    assert report["evidence_bundle"]["format"] == "appgen.release-evidence-bundle.v1"
    assert report["evidence_bundle"]["graph_suite"]["format"] == "appgen.graph-suite-report.v1"
    assert set(report["evidence_bundle"]["graph_suite"]["required_kinds"]) == {
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
    assert set(report["evidence_bundle"]["graph_suite"]["formats"]) == {"json", "mermaid", "dot"}
    assert report["graph_kind_count"] == len(report["evidence_bundle"]["graph_suite"]["required_kinds"]) == 9
    assert report["graph_format_count"] == len(report["evidence_bundle"]["graph_suite"]["formats"]) == 3
    assert report["graph_evidence"]["format"] == "appgen.graph-suite-report.v1"


def test_package_report_writes_release_evidence_bundle_when_output_dir_is_given(tmp_path: Path) -> None:
    output_dir = tmp_path / "dist"
    report = release_verifier_report_dsl(
        RELEASE_SAMPLE,
        source_name="release.appgen",
        targets=("mobile", "desktop"),
        output_dir=str(output_dir),
    )
    evidence_path = output_dir / "appgen-release-evidence.json"
    mobile_manifest_path = output_dir / "appgen-package-mobile.json"
    desktop_manifest_path = output_dir / "appgen-package-desktop.json"
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    mobile_manifest = json.loads(mobile_manifest_path.read_text(encoding="utf-8"))
    desktop_manifest = json.loads(desktop_manifest_path.read_text(encoding="utf-8"))

    assert report["format"] == "appgen.release-verifier-report.v1"
    assert report["ok"] is True
    assert report["target_count"] == 2
    assert report["written_artifact_count"] == len(report["written_artifacts"]) == 3
    assert evidence_path.exists()
    assert mobile_manifest_path.exists()
    assert desktop_manifest_path.exists()
    assert report["written_artifacts"][0]["path"] == str(evidence_path)
    assert {artifact["kind"] for artifact in report["written_artifacts"]} == {
        "release_evidence",
        "mobile_package_manifest",
        "desktop_package_manifest",
    }
    assert payload["format"] == "appgen.release-evidence-file.v1"
    assert payload["evidence_bundle"]["format"] == "appgen.release-evidence-bundle.v1"
    assert payload["evidence_bundle"]["graph_suite"]["format"] == "appgen.graph-suite-report.v1"
    assert set(payload["evidence_bundle"]["graph_suite"]["formats"]) == {"json", "mermaid", "dot"}
    assert set(payload["reports"]) == {"mobile", "desktop"}
    assert mobile_manifest["format"] == "appgen.package-manifest.v1"
    assert mobile_manifest["target"] == "mobile"
    assert mobile_manifest["artifact_class"] == "mobile_application"
    assert mobile_manifest["signing_posture_declared"] is True
    assert mobile_manifest["offline_policy_declared"] is True
    assert mobile_manifest["permissions_explained"] is True
    assert mobile_manifest["screens_fit_target_density"] is True
    assert desktop_manifest["target"] == "desktop"
    assert desktop_manifest["artifact_class"] == "desktop_application"
    assert desktop_manifest["installer_posture_declared"] is True
    assert desktop_manifest["startup_assets_declared"] is True
    assert desktop_manifest["menus_bind_to_handlers"] is True


def test_package_cli_audit_proves_all_target_handoff_contracts(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_package_verify_cli(tmp_path, TOOLING_SAMPLE)
    manifest_case = next(case for case in report["cases"] if case["case"] == "package_writes_target_manifests")

    assert report["format"] == "appgen.package-verify-cli-audit.v1"
    assert report["ok"] is True
    assert report["failing_case_count"] == 0
    assert report["failing_cases"] == ()
    assert report["case_ids"] == ("verify_all_targets", "package_writes_target_manifests")
    assert report["required_case_ids"] == ("verify_all_targets", "package_writes_target_manifests")
    assert report["observed_case_ids"] == report["required_case_ids"]
    assert report["missing_case_count"] == 0
    assert report["missing_case_ids"] == ()
    assert report["expected_exit_codes_by_case"] == {
        "verify_all_targets": 0,
        "package_writes_target_manifests": 0,
    }
    assert report["exit_codes_by_case"] == report["expected_exit_codes_by_case"]
    assert report["missing_exit_code_case_count"] == 0
    assert report["missing_exit_code_cases"] == ()
    assert report["expected_payload_formats_by_case"] == {
        "verify_all_targets": "appgen.release-verifier-report.v1",
        "package_writes_target_manifests": "appgen.release-verifier-report.v1",
    }
    assert report["payload_formats_by_case"] == report["expected_payload_formats_by_case"]
    assert report["missing_payload_format_case_count"] == 0
    assert report["missing_payload_format_cases"] == ()
    assert report["ok_by_case"] == {case_id: True for case_id in report["required_case_ids"]}
    assert report["missing_ok_case_count"] == 0
    assert report["missing_ok_cases"] == ()
    assert report["expected_targets"] == ("web", "mobile", "desktop", "pbc", "deployment")
    assert report["manifest_target_count"] == 5
    assert report["manifest_targets"] == report["expected_targets"]
    assert report["missing_manifest_target_count"] == 0
    assert report["missing_manifest_targets"] == ()
    assert report["required_manifest_formats_by_target"] == {
        target: "appgen.package-manifest.v1" for target in report["expected_targets"]
    }
    assert report["missing_manifest_format_target_count"] == 0
    assert report["missing_manifest_format_targets"] == ()
    assert report["required_artifact_classes_by_target"] == {
        "web": "web_application",
        "mobile": "mobile_application",
        "desktop": "desktop_application",
        "pbc": "packaged_business_capability",
        "deployment": "deployment_plan",
    }
    assert report["artifact_classes_by_target"] == report["required_artifact_classes_by_target"]
    assert report["missing_artifact_class_target_count"] == 0
    assert report["missing_artifact_class_targets"] == ()
    assert report["required_smoke_entrypoints_by_target"] == {
        "web": "web.smoke",
        "mobile": "mobile.launch",
        "desktop": "desktop.launch",
    }
    assert report["smoke_entrypoints_by_target"] == report["required_smoke_entrypoints_by_target"]
    assert report["missing_smoke_entrypoint_target_count"] == 0
    assert report["missing_smoke_entrypoint_targets"] == ()
    assert report["release_evidence_report_count"] == 5
    assert set(report["release_evidence_reports"]) == set(report["expected_targets"])
    assert report["missing_release_report_count"] == 0
    assert report["missing_release_reports"] == ()
    assert report["required_release_report_formats_by_target"] == {
        "web": "appgen.web-verifier.v1",
        "mobile": "appgen.mobile-verifier.v1",
        "desktop": "appgen.desktop-verifier.v1",
        "pbc": "appgen.pbc-verifier.v1",
        "deployment": "appgen.deployment-verifier.v1",
    }
    assert report["release_report_formats_by_target"] == report["required_release_report_formats_by_target"]
    assert report["missing_release_report_format_target_count"] == 0
    assert report["missing_release_report_format_targets"] == ()
    assert report["release_report_kinds_by_target"] == {
        target: target for target in report["expected_targets"]
    }
    assert report["missing_release_report_kind_target_count"] == 0
    assert report["missing_release_report_kind_targets"] == ()
    assert report["release_report_ok_by_target"] == {
        target: True for target in report["expected_targets"]
    }
    assert report["failing_release_report_target_count"] == 0
    assert report["failing_release_report_targets"] == ()
    assert report["release_report_blocking_gap_counts_by_target"] == {
        target: 0 for target in report["expected_targets"]
    }
    assert report["release_report_blocking_gap_target_count"] == 0
    assert report["release_report_blocking_gap_targets"] == ()
    assert report["missing_release_graph_kind_count"] == 0
    assert report["missing_release_graph_kinds"] == ()
    assert report["missing_release_graph_format_count"] == 0
    assert report["missing_release_graph_formats"] == ()
    assert report["readiness_check_count"] == 29
    assert report["passing_readiness_check_count"] == report["readiness_check_count"]
    assert report["missing_readiness_check_count"] == 0
    assert report["missing_readiness_checks"] == ()
    assert report["missing_readiness_checks_by_target"] == {
        "web": (),
        "mobile": (),
        "desktop": (),
        "pbc": (),
        "deployment": (),
    }
    assert set(report["readiness_matrix"]) == {"web", "mobile", "desktop", "pbc", "deployment"}
    assert all(all(checks.values()) for checks in report["readiness_matrix"].values())
    assert report["readiness_matrix"]["web"]["smoke_entrypoint"] is True
    assert report["readiness_matrix"]["mobile"]["smoke_entrypoint"] is True
    assert report["readiness_matrix"]["desktop"]["smoke_entrypoint"] is True
    assert report["readiness_matrix"]["pbc"]["handoff_contracts_present"] is True
    assert report["readiness_matrix"]["deployment"]["topology_declared"] is True
    assert report["missing_handoff_artifact_count"] == 0
    assert report["missing_handoff_artifacts"] == ()
    assert report["missing_handoff_artifacts_by_target"] == {
        "web": (),
        "mobile": (),
        "desktop": (),
        "pbc": (),
        "deployment": (),
    }
    assert report["required_handoff_artifacts_by_target"]["web"] == ("routes", "forms", "handlers", "smoke_tests")
    assert report["required_handoff_artifacts_by_target"]["mobile"] == (
        "mobile_metadata",
        "signing_posture",
        "offline_policy",
        "permissions",
        "screen_density",
        "smoke_launch",
    )
    assert report["required_handoff_artifacts_by_target"]["desktop"] == (
        "desktop_metadata",
        "installer_profile",
        "startup_assets",
        "menus",
        "context_menus",
        "smoke_launch",
    )
    assert report["required_handoff_artifacts_by_target"]["pbc"] == (
        "manifest",
        "contracts",
        "owned_schema",
        "registration",
        "release_evidence",
    )
    assert report["required_handoff_artifacts_by_target"]["deployment"] == (
        "units",
        "health_checks",
        "environment",
        "resource_hints",
        "topology_graph",
    )
    assert set(report["required_handoff_artifacts_by_target"]["desktop"]) <= set(
        report["handoff_artifacts_by_target"]["desktop"]
    )
    assert set(manifest_case["release_evidence_reports"]) == {"web", "mobile", "desktop", "pbc", "deployment"}
    assert manifest_case["web_artifact_class"] == "web_application"
    assert manifest_case["release_graph_suite_format"] == "appgen.graph-suite-report.v1"
    assert set(manifest_case["release_graph_formats"]) == {"json", "mermaid", "dot"}
    assert {"er", "lookup", "workflow", "handler", "security", "agent", "deployment", "package"} <= set(
        manifest_case["release_graph_kinds"]
    )
    assert {"routes", "forms", "handlers", "smoke_tests"} <= set(manifest_case["web_handoff_artifacts"])
    assert manifest_case["mobile_artifact_class"] == "mobile_application"
    assert {
        "mobile_metadata",
        "signing_posture",
        "offline_policy",
        "permissions",
        "screen_density",
        "smoke_launch",
    } <= set(manifest_case["mobile_handoff_artifacts"])
    assert manifest_case["mobile_package_metadata_exists"] is True
    assert manifest_case["mobile_signing_posture_declared"] is True
    assert manifest_case["mobile_offline_policy_declared"] is True
    assert manifest_case["mobile_permissions_explained"] is True
    assert manifest_case["mobile_screens_fit_target_density"] is True
    assert manifest_case["mobile_smoke_launch_path_exists"] is True
    assert manifest_case["mobile_smoke_entrypoint"] == "mobile.launch"
    assert manifest_case["desktop_artifact_class"] == "desktop_application"
    assert {
        "desktop_metadata",
        "installer_profile",
        "startup_assets",
        "menus",
        "context_menus",
        "smoke_launch",
    } <= set(manifest_case["desktop_handoff_artifacts"])
    assert manifest_case["desktop_package_metadata_exists"] is True
    assert manifest_case["desktop_installer_posture_declared"] is True
    assert manifest_case["desktop_startup_assets_declared"] is True
    assert manifest_case["desktop_menus_bind_to_handlers"] is True
    assert manifest_case["desktop_smoke_launch_path_exists"] is True
    assert manifest_case["desktop_smoke_entrypoint"] == "desktop.launch"
    assert manifest_case["pbc_artifact_class"] == "packaged_business_capability"
    assert {"manifest", "contracts", "owned_schema", "registration", "release_evidence"} <= set(
        manifest_case["pbc_handoff_artifacts"]
    )
    assert manifest_case["pbc_side_effect_free_registration"] is True
    assert manifest_case["deployment_artifact_class"] == "deployment_plan"
    assert {"units", "health_checks", "environment", "resource_hints", "topology_graph"} <= set(
        manifest_case["deployment_handoff_artifacts"]
    )
    assert manifest_case["deployment_units_declared"] is True
    assert manifest_case["deployment_health_checks_declared"] is True
    assert manifest_case["deployment_environment_variables_named"] is True
    assert manifest_case["deployment_secret_values_absent"] is True
    assert manifest_case["deployment_resource_hints_present"] is True
    assert manifest_case["deployment_topology_graph_connected"] is True
    assert manifest_case["deployment_topology_declared"] is True


def test_appgen_package_subcommand_materializes_release_evidence(tmp_path: Path) -> None:
    source_path = tmp_path / "release.appgen"
    output_dir = tmp_path / "dist"
    source_path.write_text(RELEASE_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "package",
            str(source_path),
            "--target",
            "mobile",
            "--out",
            str(output_dir),
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "package",
            str(source_path),
            "--target",
            "mobile",
            "--out",
            str(output_dir / "text"),
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    verify_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "verify", str(source_path), "--target", "mobile"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    invalid_target = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "package",
            str(source_path),
            "--target",
            "banana",
            "--json",
        ],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    evidence_path = output_dir / "appgen-release-evidence.json"
    mobile_manifest_path = output_dir / "appgen-package-mobile.json"
    assert payload["format"] == "appgen.release-verifier-report.v1"
    assert payload["targets"] == ["mobile"]
    assert evidence_path.exists()
    assert mobile_manifest_path.exists()
    assert json.loads(evidence_path.read_text(encoding="utf-8"))["reports"]["mobile"]["format"] == "appgen.mobile-verifier.v1"
    assert json.loads(mobile_manifest_path.read_text(encoding="utf-8"))["smoke_entrypoint"] == "mobile.launch"
    assert text_result.returncode == 0, text_result.stderr
    assert text_result.stdout.startswith("release-verify ok: format=appgen.release-verifier-report.v1 targets=mobile")
    assert "written=2" in text_result.stdout
    assert "release-evidence format=appgen.release-evidence-bundle.v1: artifacts=1" in text_result.stdout
    assert "graph-suite format=appgen.graph-suite-report.v1: kinds=9 formats=3" in text_result.stdout
    assert "ok mobile" in text_result.stdout
    assert f"artifact release_evidence: {output_dir / 'text' / 'appgen-release-evidence.json'}" in text_result.stdout
    assert f"artifact mobile_package_manifest: {output_dir / 'text' / 'appgen-package-mobile.json'}" in text_result.stdout
    assert verify_text.returncode == 0, verify_text.stderr
    assert verify_text.stdout.startswith("release-verify ok: format=appgen.release-verifier-report.v1 targets=mobile written=0")
    assert "release-evidence format=appgen.release-evidence-bundle.v1: artifacts=1" in verify_text.stdout
    assert "graph-suite format=appgen.graph-suite-report.v1: kinds=9 formats=3" in verify_text.stdout
    assert "ok mobile" in verify_text.stdout
    assert "artifact " not in verify_text.stdout
    assert invalid_target.returncode == 2
    assert "invalid choice" in invalid_target.stderr
    assert "Traceback" not in invalid_target.stderr


def test_release_verifier_reports_blocking_gaps_for_missing_mobile_package_metadata() -> None:
    report = release_verifier_report_dsl(TOOLING_SAMPLE, source_name="finance.appgen", targets=("mobile",))

    assert report["ok"] is False
    assert "package_metadata_exists" in report["reports"]["mobile"]["blocking_gaps"]
    assert "smoke_launch_not_declared" in report["reports"]["mobile"]["blocking_gaps"]


def test_appgen_verify_text_reports_target_blocking_gaps(tmp_path: Path) -> None:
    source_path = tmp_path / "missing-mobile-package.appgen"
    source_path.write_text(TOOLING_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "verify", str(source_path), "--target", "mobile"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1, result.stderr
    assert result.stdout.startswith("release-verify failed: format=appgen.release-verifier-report.v1 targets=mobile written=0")
    assert "release-evidence format=appgen.release-evidence-bundle.v1" in result.stdout
    assert "graph-suite format=appgen.graph-suite-report.v1: kinds=9 formats=3" in result.stdout
    assert "fail mobile gaps=" in result.stdout
    assert "package_metadata_exists" in result.stdout
    assert "smoke_launch_not_declared" in result.stdout


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


def test_appgen_pbc_list_and_verify_text_outputs_are_human_readable() -> None:
    root = Path(__file__).resolve().parents[1]
    audit = appgen_dsl._tooling_audit_pbc_cli_text()

    pbc_list = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "pbc", "list"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    pbc_verify = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "pbc", "verify", "gl_core"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )

    assert pbc_list.returncode == 0, pbc_list.stderr
    assert pbc_verify.returncode == 0, pbc_verify.stderr
    assert pbc_list.stdout.startswith("pbc list ok: count=")
    assert "format=appgen.pbc-verifier-catalog.v1" in pbc_list.stdout
    assert "mesh " in pbc_list.stdout
    assert "pbc gl_core: ok=True" in pbc_list.stdout
    assert "datastore=postgresql" in pbc_list.stdout
    assert not pbc_list.stdout.lstrip().startswith("{")
    assert pbc_verify.stdout.startswith("pbc verify ok: pbc=gl_core")
    assert "format=appgen.pbc-package-verifier.v1" in pbc_verify.stdout
    assert "checks=7 gaps=0" in pbc_verify.stdout
    assert "ok manifest_validates" in pbc_verify.stdout
    assert "catalog label=" in pbc_verify.stdout
    assert not pbc_verify.stdout.lstrip().startswith("{")
    assert audit["format"] == "appgen.pbc-cli-text-audit.v1"
    assert audit["ok"] is True
    assert {case["case"] for case in audit["cases"]} == {"pbc_list_text", "pbc_verify_text"}


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


def test_designer_sync_visual_edits_apply_real_dsl_mutations_and_diff_previews() -> None:
    field = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "add_field",
            "table": "Invoice",
            "field": "due_date",
            "type": "date",
            "required": True,
        },
    )
    transition = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "add_flow_transition",
            "flow": "SubmitInvoice",
            "from": "posted",
            "to": "archived",
        },
    )
    pbc = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "add_pbc_include",
            "composition": "FinanceSuite",
            "pbc": "ap_automation",
            "version": "1.0.0",
        },
    )

    assert field["visual_edit"]["accepted"] is True
    assert "  due_date: date required" in field["visual_edit"]["patched_source"]
    assert "due_date" in field["visual_edit"]["semantic_after"]["tables"]["Invoice"]["fields"]
    assert "database_designer" in field["visual_edit"]["changed_surfaces"]
    assert any(line.startswith("+  due_date: date required") for line in field["visual_edit"]["dsl_diff"])
    assert transition["visual_edit"]["accepted"] is True
    assert "  posted -> archived" in transition["visual_edit"]["patched_source"]
    assert "workflow_designer" in transition["visual_edit"]["changed_surfaces"]
    assert pbc["visual_edit"]["accepted"] is True
    assert "  include pbc ap_automation version 1.0.0" in pbc["visual_edit"]["patched_source"]
    assert "pbc_composition_designer" in pbc["visual_edit"]["changed_surfaces"]


def test_designer_sync_applies_multi_surface_transactions_atomically() -> None:
    transaction = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "transaction",
            "edits": [
                {"kind": "add_field", "table": "Invoice", "field": "bulk_note", "type": "string"},
                {
                    "kind": "add_component",
                    "view": "InvoiceForm",
                    "binding": "bulk_note",
                    "component": "TextBox",
                    "x": 2,
                    "y": 3,
                    "w": 5,
                    "h": 1,
                },
                {"kind": "add_flow_transition", "flow": "SubmitInvoice", "from": "posted", "to": "archived"},
                {"kind": "add_package", "name": "WebBulkRelease", "target": "web"},
                {"kind": "add_deployment_unit", "deployment": "Production", "target": "SubmitInvoice", "pattern": "worker"},
            ],
        },
    )
    rejected = designer_sync_report_dsl(
        TOOLING_SAMPLE,
        source_name="finance.appgen",
        visual_edit={
            "kind": "transaction",
            "edits": [
                {"kind": "add_field", "table": "Invoice", "field": "rolled_back_note", "type": "string"},
                {
                    "kind": "add_component",
                    "view": "InvoiceForm",
                    "binding": "missing.field",
                    "component": "Lookup",
                    "x": 1,
                    "y": 2,
                    "w": 4,
                    "h": 1,
                },
            ],
        },
    )

    visual = transaction["visual_edit"]
    assert transaction["ok"] is True
    assert visual["format"] == "appgen.designer-visual-transaction-result.v1"
    assert visual["accepted"] is True
    assert visual["atomic"] is True
    assert visual["operation_count"] == 5
    assert visual["operations"] == (
        "add_field",
        "add_component",
        "add_flow_transition",
        "add_package",
        "add_deployment_unit",
    )
    assert {"database_designer", "form_designer", "workflow_designer", "package_deployment_designer"} <= set(
        visual["changed_surfaces"]
    )
    assert "bulk_note" in visual["semantic_after"]["tables"]["Invoice"]["fields"]
    assert "@ bulk_note TextBox 2 3 5 1" in visual["patched_source"]
    assert "posted -> archived" in visual["patched_source"]
    assert "package WebBulkRelease" in visual["patched_source"]
    assert "unit SubmitInvoice as worker" in visual["patched_source"]

    rejected_visual = rejected["visual_edit"]
    assert rejected["ok"] is False
    assert rejected_visual["accepted"] is False
    assert rejected_visual["atomic"] is True
    assert "rolled_back_note" not in rejected_visual["patched_source"]
    assert "rolled_back_note" in rejected_visual["attempted_source"]
    assert any(item["code"] == "AGX0402" for item in rejected_visual["diagnostics"])


def test_designer_visual_edit_matrix_covers_required_studio_edit_paths() -> None:
    matrix = designer_visual_edit_matrix_dsl(TOOLING_SAMPLE, source_name="finance.appgen")
    case_ids = {case["id"] for case in matrix["cases"]}

    assert matrix["format"] == "appgen.designer-visual-edit-matrix.v1"
    assert matrix["ok"] is True
    assert {
        "database_designer_add_field",
        "form_designer_add_component",
        "workflow_designer_add_transition",
        "pbc_composition_designer_add_include",
        "package_designer_add_package",
        "deployment_designer_add_unit",
        "multi_surface_transaction_round_trip",
        "multi_surface_transaction_rejects_invalid_binding_atomically",
        "form_designer_reject_invalid_binding",
    } <= case_ids
    assert matrix["blocking_gaps"] == ()


def test_appgen_designer_sync_subcommand_emits_json_and_text_contracts(tmp_path: Path) -> None:
    path = tmp_path / "finance.appgen"
    path.write_text(TOOLING_SAMPLE, encoding="utf-8")
    edit = {
        "kind": "add_field",
        "table": "Invoice",
        "field": "sync_note",
        "type": "string",
    }
    bulk_edit = {
        "kind": "transaction",
        "edits": [
            {"kind": "add_field", "table": "Invoice", "field": "bulk_sync_note", "type": "string"},
            {
                "kind": "add_component",
                "view": "InvoiceForm",
                "binding": "bulk_sync_note",
                "component": "TextBox",
                "x": 2,
                "y": 3,
                "w": 5,
                "h": 1,
            },
            {"kind": "add_flow_transition", "flow": "SubmitInvoice", "from": "posted", "to": "archived"},
            {"kind": "add_package", "name": "WebBulkRelease", "target": "web"},
            {"kind": "add_deployment_unit", "deployment": "Production", "target": "SubmitInvoice", "pattern": "worker"},
        ],
    }

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path)],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    edit_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--edit-json", json.dumps(edit), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    edit_text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--edit-json", json.dumps(edit)],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    bulk_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--edit-json", json.dumps(bulk_edit), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    invalid_edit_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--edit-json", "{bad", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    non_object_edit_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "designer-sync", str(path), "--edit-json", "[]", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.designer-sync-report.v1"
    assert payload["projections"]["dsl_editor"]["semantic_model_format"] == "appgen.semantic-model.v1"
    assert text_result.returncode == 0, text_result.stderr
    assert text_result.stdout.startswith(
        "designer-sync ok: format=appgen.designer-sync-report.v1 semantic_format=appgen.semantic-model.v1"
    )
    assert "surfaces=10" in text_result.stdout
    assert "form_designer" in text_result.stdout
    assert "visual-edit-matrix ok=True" in text_result.stdout
    assert "visual-edit-operations add_field, add_component, add_flow_transition" in text_result.stdout
    assert "add_pbc_include" in text_result.stdout
    assert "add_package" in text_result.stdout
    assert "add_deployment_unit" in text_result.stdout
    assert edit_result.returncode == 0, edit_result.stderr
    edit_payload = json.loads(edit_result.stdout)
    assert edit_payload["visual_edit"]["accepted"] is True
    assert "sync_note" in edit_payload["visual_edit"]["patched_source"]
    assert edit_text_result.returncode == 0, edit_text_result.stderr
    assert "visual-edit accepted=True round_trip=True" in edit_text_result.stdout
    assert "changed=database_designer" in edit_text_result.stdout
    assert bulk_result.returncode == 0, bulk_result.stderr
    bulk_payload = json.loads(bulk_result.stdout)
    assert bulk_payload["visual_edit"]["format"] == "appgen.designer-visual-transaction-result.v1"
    assert bulk_payload["visual_edit"]["accepted"] is True
    assert bulk_payload["visual_edit"]["operation_count"] == 5
    assert "bulk_sync_note" in bulk_payload["visual_edit"]["patched_source"]
    assert invalid_edit_result.returncode == 2
    assert "invalid JSON for --edit-json" in invalid_edit_result.stderr
    assert non_object_edit_result.returncode == 2
    assert "--edit-json must be a JSON object" in non_object_edit_result.stderr
    assert "Traceback" not in invalid_edit_result.stderr
    assert "Traceback" not in non_object_edit_result.stderr


def test_designer_sync_cli_audit_proves_diff_semantic_and_projection_refresh(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_designer_sync_cli(tmp_path, TOOLING_SAMPLE)

    assert report["format"] == "appgen.designer-sync-cli-audit.v1"
    assert report["ok"] is True
    assert report["scenario_count"] == 4
    assert report["passing_scenario_count"] == report["scenario_count"]
    assert report["required_scenario_ids"] == (
        "valid_add_field_round_trip",
        "bulk_transaction_round_trip",
        "invalid_json_rejected",
        "non_object_edit_rejected",
    )
    assert report["observed_scenario_ids"] == report["required_scenario_ids"]
    assert report["missing_scenario_count"] == 0
    assert report["missing_scenario_ids"] == ()
    assert report["failing_scenario_count"] == 0
    assert report["failing_scenario_ids"] == ()
    assert report["expected_exit_codes_by_scenario"] == {
        "valid_add_field_round_trip": 0,
        "bulk_transaction_round_trip": 0,
        "invalid_json_rejected": 2,
        "non_object_edit_rejected": 2,
    }
    assert report["exit_codes_by_scenario"] == report["expected_exit_codes_by_scenario"]
    assert report["missing_exit_code_scenario_count"] == 0
    assert report["missing_exit_code_scenarios"] == ()
    assert report["expected_payload_formats_by_scenario"] == {
        "valid_add_field_round_trip": "appgen.designer-sync-report.v1",
        "bulk_transaction_round_trip": "appgen.designer-sync-report.v1",
    }
    assert report["payload_formats_by_scenario"] == report["expected_payload_formats_by_scenario"]
    assert report["missing_payload_format_scenario_count"] == 0
    assert report["missing_payload_format_scenarios"] == ()
    assert report["ok_by_scenario"] == {scenario: True for scenario in report["required_scenario_ids"]}
    assert report["missing_ok_scenario_count"] == 0
    assert report["missing_ok_scenarios"] == ()
    assert report["valid_changed_surface_count"] >= 1
    assert report["required_changed_surfaces"] == ("database_designer",)
    assert report["missing_changed_surface_count"] == 0
    assert report["missing_changed_surfaces"] == ()
    assert report["projection_count"] >= 1
    assert report["required_projection_ids"] == (
        "form_designer",
        "database_designer",
        "workflow_designer",
        "pbc_composition_designer",
        "package_deployment_designer",
    )
    assert set(report["projection_ids"]) == set(report["required_projection_ids"])
    assert report["missing_projection_count"] == 0
    assert report["missing_projection_ids"] == ()
    assert report["invalid_case_count"] == 2
    assert report["invalid_case_ids"] == ("invalid_json_rejected", "non_object_edit_rejected")
    assert report["traceback_free_count"] == report["invalid_case_count"]
    assert report["traceback_free_case_ids"] == report["invalid_case_ids"]
    assert report["missing_traceback_free_case_count"] == 0
    assert report["missing_traceback_free_case_ids"] == ()
    assert report["valid_exit"] == 0
    assert report["valid_payload_format"] == "appgen.designer-sync-report.v1"
    assert report["valid_round_trip"] is True
    assert "database_designer" in report["valid_changed_surfaces"]
    assert report["valid_diff_lines"] > 0
    assert report["required_diff_fragments"] == ("+  sync_note: string",)
    assert report["missing_diff_fragment_count"] == 0
    assert report["missing_diff_fragments"] == ()
    assert report["valid_semantic_model_format"] == "appgen.semantic-model.v1"
    assert report["valid_projection_format"] == "appgen.designer-database-projection.v1"
    assert report["valid_projection_semantic_model_format"] == "appgen.semantic-model.v1"
    assert report["bulk_exit"] == 0
    assert report["bulk_payload_format"] == "appgen.designer-sync-report.v1"
    assert report["bulk_result_format"] == "appgen.designer-visual-transaction-result.v1"
    assert report["bulk_atomic"] is True
    assert report["bulk_round_trip"] is True
    assert report["bulk_operation_count"] == 5
    assert report["bulk_operations"] == (
        "add_field",
        "add_component",
        "add_flow_transition",
        "add_package",
        "add_deployment_unit",
    )
    assert set(report["required_bulk_changed_surfaces"]) <= set(report["bulk_changed_surfaces"])
    assert report["missing_bulk_changed_surfaces"] == ()
    assert report["bulk_diff_lines"] > 0
    assert report["bulk_patch_count"] == 5
    assert report["bulk_semantic_model_format"] == "appgen.semantic-model.v1"


def test_diagnostic_catalog_and_fixture_audit_cover_required_agx_codes() -> None:
    catalog = diagnostic_catalog_dsl()
    audit = diagnostic_fixture_audit_dsl()

    assert catalog["format"] == "appgen.diagnostic-catalog.v1"
    assert audit["format"] == "appgen.diagnostic-fixture-audit.v1"
    assert catalog["ok"] is True
    assert audit["ok"] is True
    assert catalog["range_count"] == len(catalog["ranges"])
    assert catalog["diagnostic_count"] == len(catalog["diagnostics"])
    assert catalog["required_code_count"] == len(catalog["required_codes"])
    assert catalog["covered_fixture_code_count"] == len(catalog["covered_fixture_codes"])
    assert catalog["missing_fixture_count"] == 0
    assert catalog["catalog_shape_gaps"] == ()
    assert catalog["catalog_shape_gap_count"] == 0
    assert catalog["runtime_shape_enforced_by"] == "appgen.diagnostic-fixture-audit.v1"
    assert set(catalog["diagnostic_shape_fields"]) == {
        "code",
        "title",
        "severity",
        "message",
        "range",
        "related_locations",
        "fixes",
        "docs_url",
    }
    assert catalog["diagnostic_shape_field_count"] == len(catalog["diagnostic_shape_fields"])
    assert set(catalog["catalog_fields"]) == {
        "code",
        "severity",
        "title",
        "trigger",
        "example_fix",
        "docs_url",
        "fixture",
    }
    assert catalog["catalog_field_count"] == len(catalog["catalog_fields"])
    assert all(set(catalog["catalog_fields"]) <= set(item) for item in catalog["diagnostics"])
    assert set(catalog["required_codes"]) == set(catalog["covered_fixture_codes"])
    assert set(catalog["required_codes"]) <= set(audit["covered_codes"])
    assert audit["required_code_count"] == len(audit["required_codes"])
    assert audit["covered_code_count"] == len(audit["covered_codes"])
    assert audit["missing_code_count"] == 0
    assert audit["fixture_count"] == len(audit["fixtures"])
    assert audit["passing_fixture_count"] == audit["fixture_count"]
    assert audit["blocking_gap_count"] == 0
    assert audit["shape_gap_count"] == 0
    assert audit["severity_gap_count"] == 0
    assert audit["report_format_count"] == len(audit["report_formats"])
    assert {
        "appgen.lint-report.v1",
        "appgen.migration-plan.v1",
        "appgen.nl-plan.v1",
        "appgen.internal-error.v1",
    } <= set(audit["report_formats"])
    assert "docs/tooling.md#linter-rules-by-domain" in appgen_dsl._tooling_audit_doc_refs(catalog["diagnostics"])
    assert all(not fixture["shape_gaps"] for fixture in audit["fixtures"])
    assert all(not fixture["severity_gaps"] for fixture in audit["fixtures"])
    assert {
        "AGX0201",
        "AGX0304",
        "AGX0404",
        "AGX0602",
        "AGX0903",
        "AGX1002",
        "AGX1101",
        "AGX1201",
        "AGX9000",
    } <= set(audit["covered_codes"])


def test_appgen_diagnostics_subcommand_emits_catalog_fixture_audit_and_text() -> None:
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
    catalog_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "diagnostics"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    audit_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "diagnostics", "--audit-fixtures"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert catalog_result.returncode == 0, catalog_result.stderr
    assert audit_result.returncode == 0, audit_result.stderr
    assert catalog_text.returncode == 0, catalog_text.stderr
    assert audit_text.returncode == 0, audit_text.stderr
    catalog_payload = json.loads(catalog_result.stdout)
    audit_payload = json.loads(audit_result.stdout)
    assert catalog_payload["format"] == "appgen.diagnostic-catalog.v1"
    assert audit_payload["format"] == "appgen.diagnostic-fixture-audit.v1"
    assert catalog_text.stdout.startswith("diagnostics ok: format=appgen.diagnostic-catalog.v1")
    assert f"format={catalog_payload['format']}" in catalog_text.stdout
    assert f"covered={len(catalog_payload['covered_fixture_codes'])}" in catalog_text.stdout
    assert f"required={len(catalog_payload['required_codes'])}" in catalog_text.stdout
    assert f"fixtures={catalog_payload['fixture_count']}" in catalog_text.stdout
    assert "missing=0" in catalog_text.stdout
    assert "missing-fixture " not in catalog_text.stdout
    assert audit_text.stdout.startswith("diagnostics-audit ok: format=appgen.diagnostic-fixture-audit.v1")
    assert f"format={audit_payload['format']}" in audit_text.stdout
    assert f"covered={len(audit_payload['covered_codes'])}" in audit_text.stdout
    assert f"required={len(audit_payload['required_codes'])}" in audit_text.stdout
    assert "missing=0" in audit_text.stdout
    assert "missing-code " not in audit_text.stdout


def test_parser_golden_audit_covers_required_grammar_constructs() -> None:
    audit = parser_golden_audit_dsl()

    assert audit["format"] == "appgen.parser-golden-audit.v1"
    assert audit["ok"] is True
    assert audit["missing_constructs"] == ()
    assert audit["required_construct_count"] == len(audit["constructs_required"])
    assert audit["covered_construct_count"] == len(audit["constructs_covered"])
    assert audit["missing_construct_count"] == 0
    assert audit["fixture_count"] == len(audit["fixtures"])
    assert audit["valid_fixture_count"] >= 1
    assert audit["invalid_fixture_count"] >= 1
    assert audit["passing_fixture_count"] == audit["fixture_count"]
    assert audit["failing_fixture_count"] == 0
    assert audit["blocking_gap_count"] == 0
    assert audit["parsed_fixture_count"] >= audit["valid_fixture_count"]
    assert audit["valid_parsed_fixture_count"] == audit["valid_fixture_count"]
    assert audit["invalid_rejected_fixture_count"] == audit["invalid_fixture_count"]
    assert set(audit["constructs_required"]) <= set(audit["constructs_covered"])
    assert {
        "composition_connect",
        "deploy_unit",
        "llm",
        "agent",
        "package",
        "test",
    } <= set(audit["constructs_covered"])


def test_appgen_parser_golden_subcommand_emits_json_and_text_contracts() -> None:
    json_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "parser-golden", "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "parser-golden"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert json_result.returncode == 0, json_result.stderr
    assert text_result.returncode == 0, text_result.stderr
    payload = json.loads(json_result.stdout)
    assert payload["format"] == "appgen.parser-golden-audit.v1"
    assert text_result.stdout.startswith("parser-golden ok: format=appgen.parser-golden-audit.v1")
    assert f"fixtures={payload['fixture_count']}" in text_result.stdout
    assert f"valid={payload['valid_fixture_count']}" in text_result.stdout
    assert f"invalid={payload['invalid_fixture_count']}" in text_result.stdout
    assert f"format={payload['format']}" in text_result.stdout
    assert f"required={payload['required_construct_count']}" in text_result.stdout
    assert f"constructs={payload['covered_construct_count']}" in text_result.stdout
    assert f"missing={payload['missing_construct_count']}" in text_result.stdout
    assert "missing-constructs " not in text_result.stdout
    assert "fail " not in text_result.stdout


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
        "generator",
        "generator_readiness",
        "release_verifier",
        "tests",
    } <= set(report["surfaces"])
    assert all(check["ok"] for check in report["checks"])
    assert any(check["check"] == "designer_graphs_match_semantic_graphs" for check in report["checks"])
    assert any(check["check"] == "generator_validation_uses_semantic_model" for check in report["checks"])
    assert report["surface_evidence"]["generate_report"] == "appgen.generate-report.v1"


def test_appgen_drift_subcommand_emits_json_and_text_contracts(tmp_path: Path) -> None:
    path = tmp_path / "release.appgen"
    path.write_text(RELEASE_SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "drift", str(path), "--json"],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "drift", str(path)],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert text_result.returncode == 0, text_result.stderr
    payload = json.loads(result.stdout)
    assert payload["format"] == "appgen.semantic-drift-audit.v1"
    assert payload["surface_evidence"]["lsp_service"] == "appgen.lsp-service.v1"
    assert payload["surface_evidence"]["generate_report"] == "appgen.generate-report.v1"
    assert text_result.stdout.startswith("drift ok: format=appgen.semantic-drift-audit.v1 semantic_format=appgen.semantic-model.v1")
    assert "surfaces=8" in text_result.stdout
    assert "blocking_gaps=0" in text_result.stdout
    assert "evidence lsp_service: appgen.lsp-service.v1" in text_result.stdout
    assert "evidence generate_report: appgen.generate-report.v1" in text_result.stdout
    assert "ok generator_validation_uses_semantic_model" in text_result.stdout


def test_test_strategy_cli_audit_requires_generator_drift_surface(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_test_strategy_cli(tmp_path, TOOLING_SAMPLE)
    catalog_case = next(case for case in report["cases"] if case["case"] == "diagnostics_catalog")
    drift_case = next(case for case in report["cases"] if case["case"] == "semantic_drift")

    assert report["format"] == "appgen.test-strategy-cli-audit.v1"
    assert report["ok"] is True
    assert report["case_count"] == len(report["cases"])
    assert report["passing_case_count"] == report["case_count"]
    assert report["failing_case_count"] == 0
    assert report["required_case_ids"] == (
        "diagnostics_catalog",
        "diagnostics_audit_fixtures",
        "parser_golden",
        "semantic_drift",
        "doctor",
    )
    assert report["observed_case_ids"] == report["required_case_ids"]
    assert report["missing_case_count"] == 0
    assert report["missing_case_ids"] == ()
    assert report["case_ids"] == tuple(case["case"] for case in report["cases"])
    assert report["failing_cases"] == ()
    assert report["required_surface_count"] == 6
    assert report["observed_surface_count"] >= report["required_surface_count"]
    assert report["missing_surface_count"] == 0
    assert report["missing_surfaces"] == ()
    assert set(report["required_surfaces"]) <= set(report["observed_surfaces"])
    assert report["payload_format_count"] == len(report["payload_formats"])
    assert report["expected_payload_formats_by_case"] == {
        "diagnostics_catalog": "appgen.diagnostic-catalog.v1",
        "diagnostics_audit_fixtures": "appgen.diagnostic-fixture-audit.v1",
        "parser_golden": "appgen.parser-golden-audit.v1",
        "semantic_drift": "appgen.semantic-drift-audit.v1",
        "doctor": "appgen.doctor-report.v1",
    }
    assert report["payload_formats_by_case"] == report["expected_payload_formats_by_case"]
    assert report["missing_payload_format_case_count"] == 0
    assert report["missing_payload_format_cases"] == ()
    assert report["expected_exit_codes_by_case"] == {
        "diagnostics_catalog": 0,
        "diagnostics_audit_fixtures": 0,
        "parser_golden": 0,
        "semantic_drift": 0,
        "doctor": 0,
    }
    assert report["exit_codes_by_case"] == report["expected_exit_codes_by_case"]
    assert report["missing_exit_code_case_count"] == 0
    assert report["missing_exit_code_cases"] == ()
    assert report["ok_by_case"] == {
        "diagnostics_catalog": True,
        "diagnostics_audit_fixtures": True,
        "parser_golden": True,
        "semantic_drift": True,
        "doctor": True,
    }
    assert report["missing_ok_case_count"] == 0
    assert report["missing_ok_cases"] == ()
    assert report["expected_text_markers_by_case"] == {
        "diagnostics_catalog": "diagnostics ok: format=appgen.diagnostic-catalog.v1",
        "diagnostics_audit_fixtures": "diagnostics-audit ok: format=appgen.diagnostic-fixture-audit.v1",
        "parser_golden": "parser-golden ok: format=appgen.parser-golden-audit.v1",
        "semantic_drift": "drift ok: format=appgen.semantic-drift-audit.v1",
        "doctor": "doctor ok: format=appgen.doctor-report.v1",
    }
    assert report["text_exit_codes_by_case"] == report["expected_exit_codes_by_case"]
    assert report["missing_text_exit_code_case_count"] == 0
    assert report["missing_text_exit_code_cases"] == ()
    assert report["text_marker_present_by_case"] == {
        "diagnostics_catalog": True,
        "diagnostics_audit_fixtures": True,
        "parser_golden": True,
        "semantic_drift": True,
        "doctor": True,
    }
    assert report["missing_text_marker_case_count"] == 0
    assert report["missing_text_marker_cases"] == ()
    assert report["text_json_fallback_by_case"] == {
        "diagnostics_catalog": False,
        "diagnostics_audit_fixtures": False,
        "parser_golden": False,
        "semantic_drift": False,
        "doctor": False,
    }
    assert report["text_json_fallback_case_count"] == 0
    assert report["text_json_fallback_cases"] == ()
    assert set(report["payload_formats"]) >= {
        "appgen.diagnostic-catalog.v1",
        "appgen.diagnostic-fixture-audit.v1",
        "appgen.parser-golden-audit.v1",
        "appgen.semantic-drift-audit.v1",
        "appgen.doctor-report.v1",
    }
    assert report["doctor_check_count"] > 0
    assert catalog_case["payload_format"] == "appgen.diagnostic-catalog.v1"
    assert catalog_case["required_count"] == catalog_case["covered_count"]
    assert catalog_case["fixture_count"] >= catalog_case["required_count"]
    assert {"cli", "lsp", "studio", "graph", "generator", "release_verifier"} <= set(
        drift_case["required_surfaces"]
    )
    assert set(drift_case["required_surfaces"]) <= set(drift_case["surfaces"])
    assert drift_case["generate_report"] == "appgen.generate-report.v1"


def test_test_strategy_diagnostic_catalog_case_proves_registry_coverage_without_pbc_imports() -> None:
    catalog_case = appgen_dsl._tooling_audit_diagnostics_catalog_cli()

    assert catalog_case["ok"] is True
    assert catalog_case["payload_format"] == "appgen.diagnostic-catalog.v1"
    assert catalog_case["required_count"] == catalog_case["covered_count"]
    assert catalog_case["fixture_count"] >= catalog_case["required_count"]


def test_module_boundary_audit_proves_documented_tooling_surfaces() -> None:
    audit = appgen_dsl.module_boundary_audit_dsl()

    assert audit["format"] == "appgen.module-boundary-audit.v1"
    assert audit["ok"] is True
    assert audit["boundary_count"] == len(audit["boundaries"])
    assert audit["boundary_count"] >= 12
    assert audit["passing_boundary_count"] == audit["boundary_count"]
    assert audit["missing_boundary_count"] == 0
    assert audit["callable_count"] == sum(len(boundary["callables"]) for boundary in audit["boundaries"])
    assert audit["callable_count"] >= 20
    assert audit["missing_callable_count"] == 0
    assert audit["missing_boundaries"] == ()
    assert audit["core_runtime_gaps"] == ()
    assert audit["core_runtime_count"] == len(audit["core_runtime"])
    assert audit["passing_core_runtime_count"] == audit["core_runtime_count"]
    assert audit["core_runtime_gap_count"] == 0
    assert audit["layout_policy"] == "boundaries_visible_without_requiring_subpackage_layout"
    assert {
        "parser",
        "ast",
        "symbols",
        "semantic",
        "diagnostics",
        "formatter",
        "lsp",
        "cli",
        "graphs",
        "migrations",
        "nl_plan",
        "release",
    } <= {boundary["boundary"] for boundary in audit["boundaries"]}
    assert all(boundary["callable_count"] == len(boundary["callables"]) for boundary in audit["boundaries"])
    assert all(boundary["missing_callables"] == () for boundary in audit["boundaries"])
    assert all(boundary["missing_callable_count"] == 0 for boundary in audit["boundaries"])
    assert {item["boundary"] for item in audit["core_runtime"]} == {"parser", "semantic", "diagnostics", "formatter"}
    assert all(item["ok"] for item in audit["core_runtime"])


def test_doctor_report_checks_parser_catalog_generator_and_ide_hooks() -> None:
    report = doctor_report_dsl()

    assert report["format"] == "appgen.doctor-report.v1"
    assert report["ok"] is True
    assert report["required_check_ids"] == (
        "grammar_file",
        "generated_parser",
        "parser_sync",
        "parser_golden_fixtures",
        "directory_lint_input",
        "python_package_import",
        "sqlalchemy_import",
        "pbc_catalog",
        "template_writers",
        "generator_backends",
        "lsp_semantic_service",
        "cli_alias_contract",
        "lsp_completion_coverage",
        "semantic_symbol_coverage",
        "lsp_symbol_coverage",
        "module_boundaries",
        "studio_semantic_service",
        "vscode_extension_surface",
    )
    assert report["observed_check_ids"] == report["required_check_ids"]
    assert report["missing_required_check_count"] == 0
    assert report["missing_required_check_ids"] == ()
    assert report["missing_detail_format_check_count"] == 0
    assert report["missing_detail_format_checks"] == ()
    assert {
        "grammar_file",
        "generated_parser",
        "parser_sync",
        "parser_golden_fixtures",
        "directory_lint_input",
        "pbc_catalog",
        "template_writers",
        "generator_backends",
        "lsp_semantic_service",
        "cli_alias_contract",
        "lsp_completion_coverage",
        "semantic_symbol_coverage",
        "module_boundaries",
        "studio_semantic_service",
        "vscode_extension_surface",
    } <= {check["check"] for check in report["checks"]}
    alias_check = next(check for check in report["checks"] if check["check"] == "cli_alias_contract")
    assert alias_check["detail"]["report_format"] == "appgen.cli-alias-contract.v1"
    assert report["required_detail_formats_by_check"]["cli_alias_contract"] == "appgen.cli-alias-contract.v1"
    assert report["required_detail_formats_by_check"]["parser_golden_fixtures"] == "appgen.parser-golden-audit.v1"
    assert report["required_detail_formats_by_check"]["vscode_extension_surface"] == "appgen.vscode-extension-audit.v1"
    assert alias_check["detail"]["commands"] == ("appgen", "apg")
    assert alias_check["detail"]["shared_target"] == "pyAppGen.__main__:main"
    assert alias_check["detail"]["module_dispatches_tooling"] is True


def test_doctor_cli_audit_proves_json_and_text_modes() -> None:
    audit = appgen_dsl._tooling_audit_doctor_cli_modes()

    assert audit["format"] == "appgen.doctor-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 2
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["failing_cases"] == ()
    assert audit["required_case_ids"] == ("doctor_json", "doctor_text")
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["modes_by_case"] == audit["expected_modes_by_case"]
    assert audit["missing_mode_case_count"] == 0
    assert audit["missing_mode_cases"] == ()
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {"doctor_json": True, "doctor_text": True}
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["doctor_check_count"] >= 18
    assert audit["blocking_gap_count"] == 0
    assert audit["observed_check_ids"] == audit["required_check_ids"]
    assert audit["missing_required_check_count"] == 0
    assert audit["missing_required_check_ids"] == ()
    assert audit["detail_formats_by_check"] == audit["required_detail_formats_by_check"]
    assert audit["missing_detail_format_check_count"] == 0
    assert audit["missing_detail_format_checks"] == ()
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_marker_case_count"] == 0
    assert audit["missing_text_marker_cases"] == ()
    assert all(markers == () for markers in audit["missing_text_markers_by_case"].values())
    assert audit["text_json_fallback_by_case"] == {"doctor_text": False}
    assert audit["text_json_fallback_case_count"] == 0
    assert audit["text_json_fallback_cases"] == ()


def test_studio_semantic_service_audit_proves_panel_contracts() -> None:
    report = appgen_dsl._tooling_audit_studio_semantic_service(TOOLING_SAMPLE)

    assert report["format"] == "appgen.studio-semantic-service-audit.v1"
    assert report["ok"] is True
    assert report["check_count"] == len(report["checks"])
    assert report["passing_check_count"] == report["check_count"]
    assert report["failing_check_count"] == 0
    assert report["blocking_gap_count"] == 0
    assert report["blocking_gaps"] == ()
    assert report["service_format"] == "appgen.studio-semantic-service.v1"
    assert report["missing_service_formats"] == ()
    assert {
        "appgen.studio-semantic-service.v1",
        "appgen.lsp-service.v1",
        "appgen.designer-sync-report.v1",
        "appgen.graph-suite-report.v1",
        "appgen.nl-plan.v1",
    } <= set(report["observed_service_formats"])
    assert report["service_count"] == len(report["services"])
    assert report["required_service_format_count"] == len(report["required_service_formats"])
    assert report["observed_service_format_count"] == len(report["observed_service_formats"])
    assert report["missing_service_format_count"] == 0
    assert tuple(report["required_service_formats"]) == (
        "appgen.studio-semantic-service.v1",
        "appgen.lsp-service.v1",
        "appgen.designer-sync-report.v1",
        "appgen.graph-suite-report.v1",
        "appgen.nl-plan.v1",
    )
    assert all(report["checks"].values())
    assert report["checks"]["service_format_contracts"] is True
    assert report["services"] == {
        "lsp": "appgen.lsp-service.v1",
        "designer_sync": "appgen.designer-sync-report.v1",
        "graph_suite": "appgen.graph-suite-report.v1",
        "natural_language_planner": "appgen.nl-plan.v1",
    }
    assert report["surface_count"] == len(report["surfaces"])
    assert report["required_surface_count"] == len(report["required_surfaces"])
    assert report["missing_required_surface_count"] == 0
    assert report["missing_required_surfaces"] == ()
    assert report["surface_format_count"] == len(report["surface_formats"])
    assert report["surface_format_gap_count"] == 0
    assert report["surface_format_gaps"] == ()
    assert report["semantic_surface_format_count"] == len(report["semantic_surface_formats"])
    assert report["semantic_surface_format_gap_count"] == 0
    assert report["semantic_surface_format_gaps"] == ()
    assert report["panel_count"] == len(report["panel_counts"])
    assert set(report["required_surfaces"]) <= set(report["surfaces"])
    assert report["surface_formats"]["diagnostics_panel"] == "appgen.lsp-diagnostics.v1"
    assert report["surface_formats"]["graph_explain_panel"] == "appgen.designer-graph-explain-panel.v1"
    assert report["surface_formats"]["natural_language_planner"] == "appgen.designer-nl-planner-panel.v1"
    assert all(value == "appgen.semantic-model.v1" for value in report["semantic_surface_formats"].values())
    assert report["checks"]["panel_payload_depth"] is True
    assert report["panel_counts"]["component_palette_components"] > 0
    assert report["panel_counts"]["form_designer_views"] > 0
    assert report["panel_counts"]["database_designer_tables"] > 0
    assert report["panel_counts"]["workflow_designer_flows"] > 0
    assert report["panel_counts"]["pbc_composition_designer_pbcs"] > 0
    assert report["panel_counts"]["package_deployment_designer_packages"] >= 0
    assert report["panel_counts"]["diagnostics_panel_diagnostics"] > 0
    assert report["panel_counts"]["graph_explain_panel_graphs"] >= len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert report["panel_counts"]["graph_suite_reports"] >= len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert report["panel_counts"]["natural_language_operations"] > 0
    assert report["panel_counts"]["natural_language_patch_bytes"] > 0
    assert report["checks"]["frontend_browser_smoke_bridge"] is True
    assert report["browser_smoke_format"] == "appgen.studio-browser-smoke-ci-contract.v1"
    assert "semantic_service_bridge" in report["browser_smoke_scenarios"]
    assert "interaction_audit_bridge" in report["browser_smoke_scenarios"]
    assert report["browser_smoke_checks"]["frontend_semantic_service_bridge"] is True
    assert report["browser_smoke_checks"]["frontend_interaction_audit_bridge"] is True
    assert report["frontend_semantic_service_format"] == "appgen.frontend-semantic-service-audit.v1"
    assert report["frontend_semantic_service_audit"]["ok"] is True
    assert report["frontend_semantic_service_count"] == 4
    assert report["frontend_semantic_required_service_count"] == 4
    assert set(report["frontend_semantic_required_services"]) <= set(report["frontend_semantic_services"])
    assert report["frontend_semantic_missing_services"] == ()
    assert report["frontend_semantic_surface_count"] == len(report["required_surfaces"])
    assert report["frontend_semantic_required_surface_count"] == len(report["required_surfaces"])
    assert set(report["frontend_semantic_required_surfaces"]) <= set(report["frontend_semantic_surfaces"])
    assert report["frontend_semantic_missing_surfaces"] == ()
    assert report["frontend_semantic_surface_contract_count"] == len(report["frontend_semantic_required_surface_contracts"])
    assert report["frontend_semantic_required_surface_contract_count"] == len(
        report["frontend_semantic_required_surface_contracts"]
    )
    assert set(report["frontend_semantic_required_surface_contracts"]) <= set(
        report["frontend_semantic_surface_contracts"]
    )
    assert report["frontend_semantic_missing_surface_contracts"] == ()
    assert report["frontend_semantic_missing_service_count"] == 0
    assert report["frontend_semantic_missing_surface_count"] == 0
    assert report["frontend_semantic_missing_surface_contract_count"] == 0
    assert report["frontend_semantic_service_audit"]["checks"]["panel_renders_services"] is True
    assert report["frontend_semantic_service_audit"]["checks"]["panel_renders_surfaces"] is True
    assert report["frontend_interaction_format"] == "appgen.frontend-interaction-audit.v1"
    assert report["frontend_interaction_audit"]["ok"] is True
    assert report["frontend_interaction_scenario_count"] == 9
    assert report["frontend_interaction_required_scenario_count"] == 9
    assert "actionable_drag_drop_wiring_operations" in report["frontend_interaction_scenarios"]
    assert set(report["frontend_interaction_required_scenarios"]) <= set(report["frontend_interaction_scenarios"])
    assert report["frontend_interaction_missing_scenarios"] == ()
    assert report["frontend_interaction_audit_input_count"] == len(
        report["frontend_interaction_required_audit_inputs"]
    )
    assert report["frontend_interaction_required_audit_input_count"] == len(
        report["frontend_interaction_required_audit_inputs"]
    )
    assert set(report["frontend_interaction_required_audit_inputs"]) <= set(
        report["frontend_interaction_audit_inputs"]
    )
    assert report["frontend_interaction_missing_audit_inputs"] == ()
    assert report["frontend_interaction_helper_count"] == len(report["frontend_interaction_required_helpers"])
    assert report["frontend_interaction_required_helper_count"] == len(report["frontend_interaction_required_helpers"])
    assert set(report["frontend_interaction_required_helpers"]) <= set(report["frontend_interaction_helpers"])
    assert report["frontend_interaction_missing_helpers"] == ()
    assert report["frontend_interaction_missing_scenario_count"] == 0
    assert report["frontend_interaction_missing_audit_input_count"] == 0
    assert report["frontend_interaction_missing_helper_count"] == 0
    assert report["frontend_interaction_audit"]["checks"]["status_rail_inputs"] is True
    assert report["frontend_interaction_audit"]["checks"]["palette_helpers"] is True


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
    assert report["artifact_count"] == len(report["artifacts"])
    assert report["artifact_count"] > 0
    assert report["manifest_exists"] is True
    assert report["diagnostic_count"] == len(report["diagnostics"])
    assert report["blocking_gap_count"] == 0
    assert (output_dir / "appgen.json").exists()
    assert {"appgen.json", "models.py", "views.py"} <= {item["path"] for item in report["artifacts"]}
    assert blocked["ok"] is False
    assert blocked["generated"] is False
    assert blocked["artifact_count"] == 0
    assert blocked["diagnostic_count"] == len(blocked["diagnostics"])
    assert blocked["blocking_gap_count"] == len(blocked["blocking_gaps"]) == 1
    assert "lint_errors" in blocked["blocking_gaps"]


def test_generate_report_blocks_warnings_unless_allow_warnings_is_set(tmp_path: Path) -> None:
    warning_source = """
app WarningDemo { targets: web }
table Customer { id: int pk; name: string }
view CustomerForm for Customer {
  Main: name
  @ name UnknownWidget 0 0 4 1
}
"""
    blocked = generate_report_dsl(
        warning_source,
        source_name="warning.appgen",
        output_dir=tmp_path / "blocked",
    )
    allowed = generate_report_dsl(
        warning_source,
        source_name="warning.appgen",
        output_dir=tmp_path / "allowed",
        allow_warnings=True,
    )
    error_blocked = generate_report_dsl(
        "app Bad { targets: web } table Invoice { total: galaxy }",
        source_name="bad.appgen",
        output_dir=tmp_path / "error-blocked",
        allow_warnings=True,
    )

    assert blocked["ok"] is False
    assert blocked["generated"] is False
    assert "lint_warnings" in blocked["blocking_gaps"]
    assert any(item["severity"] == "warning" for item in blocked["diagnostics"])
    assert allowed["ok"] is True
    assert allowed["generated"] is True
    assert (tmp_path / "allowed" / "appgen.json").exists()
    assert error_blocked["ok"] is False
    assert error_blocked["generated"] is False
    assert "lint_errors" in error_blocked["blocking_gaps"]


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
    doctor_payload = json.loads(doctor_result.stdout)
    doctor_checks = {check["check"]: check for check in doctor_payload["checks"]}
    assert doctor_payload["format"] == "appgen.doctor-report.v1"
    assert doctor_checks["lsp_symbol_coverage"]["ok"] is True
    assert doctor_checks["lsp_symbol_coverage"]["detail"]["report_format"] == "appgen.lsp-symbol-coverage.v1"
    assert json.loads(generate_result.stdout)["format"] == "appgen.generate-report.v1"
    assert (output_dir / "appgen.json").exists()


def test_appgen_generate_subcommand_requires_allow_warnings_for_lint_warnings(tmp_path: Path) -> None:
    source_path = tmp_path / "warning.appgen"
    blocked_dir = tmp_path / "blocked"
    allowed_dir = tmp_path / "allowed"
    source_path.write_text(
        """
app WarningDemo { targets: web }
table Customer { id: int pk; name: string }
view CustomerForm for Customer {
  Main: name
  @ name UnknownWidget 0 0 4 1
}
""",
        encoding="utf-8",
    )
    root = Path(__file__).resolve().parents[1]

    blocked = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "generate",
            str(source_path),
            "--out",
            str(blocked_dir),
            "--json",
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    blocked_text = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "generate",
            str(source_path),
            "--out",
            str(tmp_path / "blocked-text"),
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    allowed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "generate",
            str(source_path),
            "--out",
            str(allowed_dir),
            "--allow-warnings",
            "--json",
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )

    assert blocked.returncode == 1, blocked.stderr
    blocked_payload = json.loads(blocked.stdout)
    assert "lint_warnings" in blocked_payload["blocking_gaps"]
    assert blocked_text.returncode == 1, blocked_text.stderr
    assert blocked_text.stdout.startswith("generate failed: format=appgen.generate-report.v1 generated=False")
    assert f"targets={','.join(blocked_payload['targets'])}" in blocked_text.stdout
    assert f"artifacts={len(blocked_payload['artifacts'])}" in blocked_text.stdout
    assert f"semantic_format={blocked_payload['validation']['semantic_model']['format']}" in blocked_text.stdout
    assert f"output_dir {tmp_path / 'blocked-text'}" in blocked_text.stdout
    assert "gap lint_warnings" in blocked_text.stdout
    assert "warning AGX0404:" in blocked_text.stdout
    assert allowed.returncode == 0, allowed.stderr
    assert json.loads(allowed.stdout)["allow_warnings"] is True
    assert (allowed_dir / "appgen.json").exists()


def test_validate_generate_cli_audit_proves_generated_artifact_handoff(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_validate_generate_cli(tmp_path, TOOLING_SAMPLE)
    cases = {case["case"]: case for case in audit["cases"]}
    generated = cases["generate_writes_artifacts"]

    assert audit["format"] == "appgen.validate-generate-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["required_case_ids"] == (
        "validate_targets",
        "validate_rejects_undeclared_targets",
        "validate_rejects_unknown_targets",
        "generate_writes_artifacts",
        "generate_blocks_warnings",
        "generate_allows_warnings_when_requested",
        "generate_blocks_errors_even_when_warnings_allowed",
    )
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["case_ids"] == tuple(case["case"] for case in audit["cases"])
    assert audit["failing_cases"] == ()
    assert audit["generated_case_count"] == 4
    assert audit["validation_case_count"] == 3
    assert audit["generated_success_case_count"] == 2
    assert audit["generated_success_cases"] == ("generate_writes_artifacts", "generate_allows_warnings_when_requested")
    assert audit["generated_blocked_case_count"] == 2
    assert audit["generated_blocked_cases"] == (
        "generate_blocks_warnings",
        "generate_blocks_errors_even_when_warnings_allowed",
    )
    assert audit["validation_rejection_case_count"] == 2
    assert audit["validation_rejection_cases"] == (
        "validate_rejects_undeclared_targets",
        "validate_rejects_unknown_targets",
    )
    assert audit["manifest_case_count"] == 2
    assert audit["manifest_existing_case_count"] == 2
    assert set(audit["manifest_existing_cases"]) == {
        "generate_writes_artifacts",
        "generate_allows_warnings_when_requested",
    }
    assert audit["artifact_handoff_case_count"] == 1
    assert audit["artifact_path_case_count"] == 1
    assert audit["artifact_path_missing_case_count"] == 0
    assert audit["blocking_gap_case_count"] == 2
    assert audit["generated_blocked_output_absent_case_count"] == 1
    assert audit["generated_blocked_output_absent_cases"] == ("generate_blocks_errors_even_when_warnings_allowed",)
    assert {"lint_warnings", "lint_errors"} <= set(audit["generated_blocking_gap_names"])
    assert audit["expected_payload_formats_by_case"] == {
        "validate_targets": "appgen.validate-report.v1",
        "validate_rejects_undeclared_targets": "appgen.validate-report.v1",
        "validate_rejects_unknown_targets": "appgen.validate-report.v1",
        "generate_writes_artifacts": "appgen.generate-report.v1",
        "generate_blocks_warnings": "appgen.generate-report.v1",
        "generate_allows_warnings_when_requested": "appgen.generate-report.v1",
        "generate_blocks_errors_even_when_warnings_allowed": "appgen.generate-report.v1",
    }
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["expected_exit_codes_by_case"] == {
        "validate_targets": 0,
        "validate_rejects_undeclared_targets": 1,
        "validate_rejects_unknown_targets": 1,
        "generate_writes_artifacts": 0,
        "generate_blocks_warnings": 1,
        "generate_allows_warnings_when_requested": 0,
        "generate_blocks_errors_even_when_warnings_allowed": 1,
    }
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {case_id: True for case_id in audit["required_case_ids"]}
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["payload_format_count"] == len(audit["payload_formats"])
    assert set(audit["payload_formats"]) == {"appgen.validate-report.v1", "appgen.generate-report.v1"}
    assert generated["ok"] is True
    assert generated["targets"] == ("web",)
    assert generated["semantic_model_format"] == "appgen.semantic-model.v1"
    assert generated["validation_format"] == "appgen.validate-report.v1"
    assert generated["artifact_count"] > 0
    assert generated["artifact_paths_exist"] is True
    assert generated["manifest_exists"] is True
    assert generated["manifest_app_name"] == "FinanceOps"


def test_tooling_implementation_phase_audit_maps_phase_exit_criteria_to_evidence() -> None:
    def ok(format_name: str) -> dict:
        return {"ok": True, "format": format_name}

    report = appgen_dsl._tooling_audit_implementation_phases(
        semantic={
            "ok": True,
            "format": "appgen.semantic-model.v1",
            **{key: {} for key in (
                "source_files",
                "app",
                "symbols",
                "tables",
                "views",
                "flows",
                "operations",
                "rules",
                "roles",
                "security",
                "agents",
                "llms",
                "pbcs",
                "composition",
                "contracts",
                "deployment",
                "packages",
                "graphs",
                "diagnostics",
            )},
        },
        symbol_coverage={"format": "appgen.symbol-coverage.v1", "missing": ()},
        language_quality={
            "format": "appgen.dsl-language-quality.v1",
            "ok": True,
            "antlr_integrity": {"format": "appgen.dsl-antlr-integrity.v1", "ok": True},
            "budget": {"format": "appgen.dsl-keyword-budget.v1", "ok": True},
        },
        diagnostics={
            **ok("appgen.diagnostic-catalog.v1"),
            "missing_fixture_count": 0,
            "catalog_shape_gap_count": 0,
        },
        diagnostic_fixtures={
            **ok("appgen.diagnostic-fixture-audit.v1"),
            "fixture_count": 9,
            "passing_fixture_count": 9,
            "missing_code_count": 0,
            "blocking_gap_count": 0,
            "shape_gap_count": 0,
            "severity_gap_count": 0,
        },
        parser_golden={
            **ok("appgen.parser-golden-audit.v1"),
            "fixture_count": 4,
            "passing_fixture_count": 4,
            "failing_fixture_count": 0,
            "missing_construct_count": 0,
            "blocking_gap_count": 0,
        },
        parser_golden_text_renderer=ok("appgen.parser-golden-text-renderer.v1"),
        drift={
            **ok("appgen.semantic-drift-audit.v1"),
            "semantic_model_format": "appgen.semantic-model.v1",
            "surfaces": ("cli", "lsp", "studio", "graph", "generator", "release_verifier"),
            "blocking_gaps": (),
        },
        drift_text_renderer=ok("appgen.semantic-drift-text-renderer.v1"),
        doctor={
            **ok("appgen.doctor-report.v1"),
            "checks": tuple({"check": f"check_{index}", "ok": True} for index in range(15)),
            "blocking_gaps": (),
        },
        doctor_text_renderer=ok("appgen.doctor-text-renderer.v1"),
        test_strategy_cli={**ok("appgen.test-strategy-cli-audit.v1"), "doctor_check_count": 15},
        test_family_contracts={
            **ok("appgen.test-family-contract-audit.v1"),
            "family_count": 11,
            "passing_family_count": 11,
            "missing_family_count": 0,
        },
        contributor_task_contracts={
            **ok("appgen.contributor-task-contract-audit.v1"),
            "task_count": 22,
            "passing_task_count": 22,
            "missing_task_count": 0,
        },
        priority_order_contracts={
            **ok("appgen.priority-order-contract-audit.v1"),
            "priority_count": 10,
            "passing_priority_count": 10,
            "missing_priority_count": 0,
            "document_order_matches": True,
        },
        module_boundaries=ok("appgen.module-boundary-audit.v1"),
        lint=ok("appgen.lint-report.v1"),
        strict_lint={**ok("appgen.lint-report.v1"), "strict": True},
        catalog_lint=ok("appgen.lint-report.v1"),
        lint_directory_cli={
            **ok("appgen.lint-directory-cli-audit.v1"),
            "scenario_count": 8,
            "passing_scenario_count": 8,
            "failing_scenario_count": 0,
            "stage_profile_count": 3,
            "passing_stage_profile_count": 3,
            "failing_stage_profile_count": 0,
            "missing_exit_code_scenario_count": 0,
            "missing_payload_format_scenario_count": 0,
            "missing_ok_scenario_count": 0,
            "missing_stage_profile_exit_code_count": 0,
            "missing_ok_stage_profile_count": 0,
            "missing_stage_name_count": 0,
            "missing_severity_name_count": 0,
            "file_order_sorted": True,
            "diagnostics_have_files": True,
            "stage_separation": {"ok": True},
        },
        semantic_source_set_cli={
            **ok("appgen.semantic-source-set-cli-audit.v1"),
            "source_set_format": "appgen.semantic-source-set.v1",
            "missing_symbol_file_count": 0,
            "missing_text_marker_count": 0,
        },
        component_publish_cli={
            **ok("appgen.component-publish-cli-audit.v1"),
            "case_count": 3,
            "passing_case_count": 3,
            "failing_case_count": 0,
            "missing_exit_code_case_count": 0,
            "missing_ok_case_count": 0,
            "patch_format": "appgen.component-catalog-patch.v1",
            "side_effect_free": True,
            "write_performed": False,
            "missing_catalog_exit_code": 1,
            "missing_catalog_blocking_gaps": ("catalog_path_readable",),
            "missing_catalog_side_effect_free": True,
            "missing_catalog_write_performed": False,
        },
        formatted={"ok": True, "format": "appgen.format-result.v1", "idempotent": True},
        formatter_contract={
            **ok("appgen.formatter-contract-audit.v1"),
            "check_count": 9,
            "passing_check_count": 9,
        },
        format_write={
            **ok("appgen.format-write-audit.v1"),
            "scenario_count": 5,
            "passing_scenario_count": 5,
            "organize_category_count": 7,
        },
        validation=ok("appgen.validate-report.v1"),
        validate_generate_cli={
            **ok("appgen.validate-generate-cli-audit.v1"),
            "validation_case_count": 3,
            "validation_rejection_case_count": 2,
            "generated_case_count": 4,
            "generated_success_case_count": 2,
            "generated_blocked_case_count": 2,
            "artifact_handoff_case_count": 1,
        },
        dsl_language_cli=ok("appgen.dsl-language-cli-audit.v1"),
        contract_schema_cli={
            **ok("appgen.contract-schema-cli-audit.v1"),
            "missing_required_schema_count": 0,
            "missing_case_count": 0,
            "missing_exit_code_case_count": 0,
            "missing_payload_format_case_count": 0,
            "missing_text_marker_count": 0,
            "semantic_required_fields": ("format", "ok", "app", "symbols", "tables", "views", "diagnostics"),
            "text_json_fallback": False,
        },
        contract_validation_cli={
            **ok("appgen.contract-validation-cli-audit.v1"),
            "missing_case_count": 0,
            "missing_exit_code_case_count": 0,
            "missing_payload_format_case_count": 0,
            "missing_text_marker_count": 0,
            "text_json_fallback": False,
            "valid_report_format": "appgen.contract-validation-report.v1",
            "valid_payload_format": "appgen.semantic-model.v1",
            "valid_schema_format": "appgen.semantic-model.v1",
            "self_report_payload_format": "appgen.contract-validation-report.v1",
            "self_report_schema_format": "appgen.contract-validation-report.v1",
            "missing_required_error_count": 1,
            "unknown_schema_available": False,
            "malformed_diagnostic_count": 1,
        },
        internal_error_exit=ok("appgen.internal-error-exit-audit.v1"),
        missing_input_exit=ok("appgen.missing-input-exit-audit.v1"),
        missing_required_option_exit=ok("appgen.missing-required-option-exit-audit.v1"),
        invalid_choice_exit=ok("appgen.invalid-choice-exit-audit.v1"),
        cli_help_surface={
            **ok("appgen.cli-help-surface-audit.v1"),
            "documented_missing_subcommand_count": 0,
            "help_missing_subcommand_count": 0,
            "subcommand_option_surface_count": 26,
            "passing_option_surface_count": 26,
            "failing_option_surface_count": 0,
            "missing_option_count": 0,
            "command_alias_count": 2,
            "entrypoint_dispatch_count": 2,
            "alias_contract": {"ok": True},
        },
        graphs={
            **ok("appgen.graph-suite-report.v1"),
            "missing_kind_count": 0,
            "missing_rendering_count": 0,
        },
        graph_cli={
            **ok("appgen.graph-cli-audit.v1"),
            "missing_required_kind_count": 0,
            "failing_case_count": 0,
        },
        graph_suite_cli={
            **ok("appgen.graph-suite-cli-audit.v1"),
            "missing_rendering_count": 0,
            "missing_text_fragment_count": 0,
        },
        explain_cli={
            **ok("appgen.explain-cli-audit.v1"),
            "case_count": 6,
            "passing_case_count": 6,
            "missing_report_format_count": 0,
        },
        graph_explain_text_renderer=ok("appgen.graph-explain-text-renderer.v1"),
        lsp={
            **ok("appgen.lsp-service.v1"),
            "completionCoverage": {
                "format": "appgen.completion-coverage.v1",
                "missing": (),
                "missing_source_count": 0,
            },
        },
        lsp_rpc={
            **ok("appgen.lsp-json-rpc-audit.v1"),
                "provider_count": 9,
                "enabled_provider_count": 9,
                "request_check_count": 8,
                "passing_request_check_count": 8,
                "editor_workflow_case_count": 8,
                "editor_workflow_passing_case_count": 8,
                "editor_workflow_failing_case_count": 0,
                "missing_editor_workflow_case_count": 0,
                "missing_editor_workflow_method_case_count": 0,
                "missing_editor_workflow_shape_case_count": 0,
                "editor_workflow_diagnostic_transition_ok": True,
                "editor_workflow_shutdown_exit_ok": True,
            },
        lsp_stdio={
            **ok("appgen.lsp-stdio-transport-audit.v1"),
            "missing_response_ids": (),
        },
        lsp_text_renderer={
            **ok("appgen.lsp-service-text-renderer.v1"),
            "navigation_line_count": 2,
            "completion_line_count": 2,
            "missing_text_surface_count": 0,
            "missing_editor_contract_format_count": 0,
            "missing_navigation_surface_count": 0,
            "missing_completion_gap_count": 0,
            "missing_hover_item_count": 0,
            "missing_rename_blocker_code_count": 0,
            "missing_rename_fix_id_count": 0,
        },
        lsp_rename_cli={
            **ok("appgen.lsp-rename-cli-audit.v1"),
            "missing_exit_code_scenario_count": 0,
            "missing_payload_format_scenario_count": 0,
            "missing_ok_scenario_count": 0,
        },
        quick_fix=ok("appgen.lsp-code-action-apply.v1"),
        code_action_apply_audit={
            **ok("appgen.lsp-code-action-apply-audit.v1"),
            "case_count": 15,
            "passing_case_count": 15,
            "required_action_count": 15,
            "observed_action_count": 15,
            "required_action_ids": tuple(f"action_{index}" for index in range(15)),
            "observed_action_ids": tuple(f"action_{index}" for index in range(15)),
            "missing_required_action_count": 0,
            "applied_edit_count": 15,
            "lint_passing_case_count": 15,
            "lint_failing_case_count": 0,
            "blocking_gap_count": 0,
        },
        lsp_apply_cli={
            **ok("appgen.lsp-code-action-cli-audit.v1"),
            "case_count": 15,
            "passing_case_count": 15,
            "required_action_ids": tuple(f"action_{index}" for index in range(15)),
            "missing_required_action_count": 0,
            "applied_edit_count": 15,
            "lint_passing_case_count": 15,
            "lint_failing_case_count": 0,
            "changed_case_count": 15,
            "unchanged_case_count": 0,
            "blocking_gap_count": 0,
        },
        code_action_text_renderer={
            **ok("appgen.lsp-code-action-text-renderer.v1"),
            "json_fallback": False,
            "edit_line_count": 1,
            "available_action_line_count": 1,
            "missing_text_surface_count": 0,
            "missing_action_id_count": 0,
            "missing_edit_snippet_count": 0,
            "missing_available_action_count": 0,
            "missing_diagnostic_code_count": 0,
            "missing_status_count": 0,
        },
        vscode=ok("appgen.vscode-extension-audit.v1"),
        studio={
            **ok("appgen.studio-semantic-service-audit.v1"),
            "browser_smoke_format": "appgen.studio-browser-smoke-ci-contract.v1",
            "browser_smoke_checks": {
                "frontend_semantic_service_bridge": True,
                "frontend_interaction_audit_bridge": True,
            },
            "frontend_semantic_service_format": "appgen.frontend-semantic-service-audit.v1",
            "frontend_semantic_service_audit": {"format": "appgen.frontend-semantic-service-audit.v1", "ok": True},
            "frontend_semantic_missing_services": (),
            "frontend_semantic_missing_surfaces": (),
            "frontend_semantic_missing_surface_contracts": (),
            "frontend_interaction_format": "appgen.frontend-interaction-audit.v1",
            "frontend_interaction_audit": {"format": "appgen.frontend-interaction-audit.v1", "ok": True},
            "frontend_interaction_missing_scenarios": (),
            "frontend_interaction_missing_audit_inputs": (),
            "frontend_interaction_missing_helpers": (),
        },
        designer=ok("appgen.designer-sync-report.v1"),
        designer_visual_edit_matrix=ok("appgen.designer-visual-edit-matrix.v1"),
        designer_sync_cli={
            **ok("appgen.designer-sync-cli-audit.v1"),
            "missing_ok_scenario_count": 0,
            "bulk_atomic": True,
            "bulk_round_trip": True,
            "bulk_operation_count": 5,
            "missing_bulk_changed_surfaces": (),
        },
        migration_detected=appgen_dsl.REQUIRED_MIGRATION_DETECTIONS,
        migration_cli={
            **ok("appgen.migration-cli-audit.v1"),
            "case_count": 2,
            "passing_case_count": 2,
            "allowed_backend_count": 2,
        },
        migration_semantic_input_cli={
            **ok("appgen.migration-semantic-input-cli-audit.v1"),
            "semantic_input_count": 2,
            "missing_source_file_count": 0,
            "missing_change_kind_count": 0,
            "missing_text_fragment_count": 0,
        },
        migration_text_renderer={
            **ok("appgen.migration-plan-text-renderer.v1"),
            "approval_line_count": 1,
            "safe_alternative_line_count": 2,
            "missing_text_surface_count": 0,
            "missing_detected_family_count": 0,
            "missing_missing_family_count": 0,
            "missing_change_target_count": 0,
            "missing_safe_alternative_count": 0,
            "missing_diagnostic_code_count": 0,
            "missing_contract_format_count": 0,
        },
        nl_plan={"ok": True, "format": "appgen.nl-plan.v1", "dsl_patch": "--- before\n+++ after"},
        nl_plan_contract={
            **ok("appgen.nl-plan-contract-audit.v1"),
            "case_count": 14,
            "passing_case_count": 14,
            "accepted_case_count": 13,
            "rejected_case_count": 1,
            "required_operation_count": 13,
            "observed_operation_kind_count": 13,
            "token_budget_case_count": 14,
            "blocking_gaps": (),
        },
        nl_plan_cli={
            **ok("appgen.nl-plan-cli-audit.v1"),
            "accepted_case_count": 13,
            "accepted_passing_case_count": 13,
            "accepted_operation_kind_count": 13,
            "accepted_patch_bytes": 100,
            "accepted_test_count": 13,
            "accepted_token_budget_notes": 13,
            "accepted_text_has_report_format": True,
            "accepted_text_has_lint_format": True,
            "accepted_text_has_migration_format": True,
            "accepted_text_has_token_notes": True,
            "rejected_diagnostic_codes": ("AGX1201",),
            "blocking_cases": (),
        },
        release=ok("appgen.release-verifier-report.v1"),
        package=ok("appgen.release-verifier-report.v1"),
        package_verify_cli={
            **ok("appgen.package-verify-cli-audit.v1"),
            "target_count": 5,
            "manifest_count": 5,
            "handoff_artifact_count": 25,
            "missing_case_count": 0,
            "missing_exit_code_case_count": 0,
            "missing_payload_format_case_count": 0,
            "missing_ok_case_count": 0,
        },
        release_text_renderer={
            **ok("appgen.release-verifier-text-renderer.v1"),
            "release_line_count": 2,
            "graph_line_count": 3,
            "target_status_line_count": 2,
            "artifact_line_count": 2,
            "missing_release_marker_count": 0,
            "missing_graph_marker_count": 0,
            "missing_target_status_count": 0,
            "missing_blocking_gap_count": 0,
            "missing_artifact_marker_count": 0,
            "missing_text_surface_count": 0,
            "missing_contract_format_count": 0,
            "missing_graph_kind_count": 0,
            "missing_graph_format_count": 0,
            "missing_target_outcome_count": 0,
            "missing_artifact_path_count": 0,
        },
        pbc_publish_cli={
            **ok("appgen.pbc-publish-cli-audit.v1"),
            "case_count": 2,
            "passing_case_count": 2,
            "side_effect_free": True,
            "write_performed": False,
            "release_evidence_ok": True,
        },
    )

    assert report["format"] == "appgen.tooling-implementation-phase-audit.v1"
    assert report["ok"] is True
    assert report["phase_count"] == len(report["phases"])
    assert report["passing_phase_count"] == report["phase_count"]
    assert report["phase_ids"] == tuple(phase["id"] for phase in report["phases"])
    assert report["required_phase_ids"] == report["phase_ids"]
    assert report["missing_required_phase_count"] == 0
    assert report["missing_required_phase_ids"] == ()
    assert report["observed_exit_criteria_by_phase"] == {
        phase["id"]: tuple(criterion["id"] for criterion in phase["exit_criteria"])
        for phase in report["phases"]
    }
    assert report["required_exit_criteria_by_phase"] == report["observed_exit_criteria_by_phase"]
    assert report["missing_required_exit_criteria_phase_count"] == 0
    assert report["missing_required_exit_criteria_by_phase"] == {}
    assert report["exit_criterion_counts_by_phase"] == {
        phase["id"]: len(phase["exit_criteria"])
        for phase in report["phases"]
    }
    assert report["passing_exit_criterion_counts_by_phase"] == {
        phase["id"]: sum(1 for criterion in phase["exit_criteria"] if criterion["ok"])
        for phase in report["phases"]
    }
    assert report["missing_exit_criterion_counts_by_phase"] == {
        phase["id"]: len(phase["missing_exit_criteria"])
        for phase in report["phases"]
    }
    assert report["passing_exit_criteria_by_phase"] == {
        phase["id"]: phase["passing_exit_criteria"]
        for phase in report["phases"]
    }
    assert report["exit_criterion_evidence_formats_by_phase"] == {
        phase["id"]: phase["evidence_formats_by_criterion"]
        for phase in report["phases"]
    }
    assert set(report["exit_criterion_counts_by_phase"]) == set(report["phase_ids"])
    assert report["exit_criterion_count"] == sum(len(phase["exit_criteria"]) for phase in report["phases"])
    assert report["passing_exit_criterion_count"] == report["exit_criterion_count"]
    assert sum(report["exit_criterion_counts_by_phase"].values()) == report["exit_criterion_count"]
    assert sum(report["passing_exit_criterion_counts_by_phase"].values()) == report["passing_exit_criterion_count"]
    assert sum(report["missing_exit_criterion_counts_by_phase"].values()) == report["missing_exit_criterion_count"]
    assert report["exit_criterion_ids"] == tuple(
        criterion["id"] for phase in report["phases"] for criterion in phase["exit_criteria"]
    )
    assert report["passing_exit_criteria"] == report["exit_criterion_ids"]
    assert report["missing_exit_criterion_count"] == 0
    assert report["missing_exit_criteria"] == ()
    assert report["missing_exit_criteria_by_phase"] == {}
    assert report["missing_phase_count"] == 0
    assert report["missing_phases"] == ()
    assert len(report["phases"]) == 7
    assert all(phase["passing_exit_criteria"] for phase in report["phases"])
    assert all(
        set(phase["passing_exit_criteria"]) == {criterion["id"] for criterion in phase["exit_criteria"]}
        for phase in report["phases"]
    )
    assert all(phase["missing_exit_criteria"] == () for phase in report["phases"])
    assert all(phase["evidence_formats_by_criterion"] for phase in report["phases"])
    assert report["exit_criterion_evidence_formats_by_phase"]["phase_5_ide_and_visual_designer_integration"][
        "frontend_browser_smoke_bridges"
    ] == (
        "appgen.studio-browser-smoke-ci-contract.v1",
        "appgen.frontend-semantic-service-audit.v1",
        "appgen.frontend-interaction-audit.v1",
    )
    assert {
        criterion["id"]
        for phase in report["phases"]
        for criterion in phase["exit_criteria"]
    } >= {
        "current_behavior_documented",
        "json_schema_contracts",
        "parser_golden_fixture_contracts",
        "semantic_drift_surface_contracts",
        "doctor_cli_text_contracts",
        "grammar_parser_sync_and_keyword_budget",
        "test_strategy_family_contracts",
        "contributor_task_breakdown_contracts",
        "priority_order_contracts",
        "semantic_model_contract",
        "diagnostic_catalog_fixture_contracts",
        "lint_cli_directory_contracts",
        "component_publish_catalog_contracts",
        "formatter_idempotency",
        "formatter_write_organize_contracts",
        "validate_target_contracts",
        "generate_artifact_policy_contracts",
        "cli_usage_failure_modes",
        "cli_help_alias_contracts",
        "graph_json_mermaid_and_dot",
        "graph_rendering_contracts",
        "explain_cli_contracts",
        "lsp_transport_rpc_contracts",
        "lsp_navigation_completion_contracts",
        "rename_and_code_actions",
        "quick_fix_family_coverage",
        "quick_fix_cli_and_text_contracts",
        "studio_semantic_bridge",
        "frontend_browser_smoke_bridges",
        "migration_safety_text_contracts",
        "natural_language_operation_contracts",
        "natural_language_cli_agent_contracts",
        "release_and_package_verifiers",
        "package_manifest_handoff_contracts",
        "release_text_evidence_contracts",
        "pbc_publish_side_effect_contracts",
    }


def test_non_goal_policy_audit_reports_guard_counts() -> None:
    report = appgen_dsl._tooling_audit_non_goal_policy()

    assert report["format"] == "appgen.non-goal-policy-audit.v1"
    assert report["ok"] is True
    assert report["case_count"] == len(report["cases"])
    assert report["passing_case_count"] == report["case_count"]
    assert report["diagnostic_code_count"] >= 3
    assert report["fix_count"] >= 2
    assert report["rejected_prompt_count"] == 3
    assert report["zero_patch_rejection_count"] == 3


def test_package_verify_cli_audit_exposes_web_manifest_readiness_metadata(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_package_verify_cli(tmp_path, TOOLING_SAMPLE)
    manifest_case = next(case for case in report["cases"] if case["case"] == "package_writes_target_manifests")

    assert report["format"] == "appgen.package-verify-cli-audit.v1"
    assert report["ok"] is True
    assert report["case_count"] == len(report["cases"])
    assert report["passing_case_count"] == report["case_count"]
    assert report["failing_case_count"] == 0
    assert report["target_count"] == 5
    assert report["manifest_target_count"] == 5
    assert report["missing_manifest_target_count"] == 0
    assert report["manifest_count"] == 5
    assert report["handoff_artifact_count"] >= 25
    assert report["handoff_counts_by_target"]["web"] >= 4
    assert report["manifest_formats"]["web"] == "appgen.package-manifest.v1"
    assert manifest_case["web_artifact_class"] == "web_application"
    assert {"routes", "forms", "handlers", "smoke_tests"} <= set(manifest_case["web_handoff_artifacts"])
    assert manifest_case["web_app_build_contract"] is True
    assert manifest_case["web_routes_declared"] is True
    assert manifest_case["web_forms_bind_valid_fields"] is True
    assert manifest_case["web_handler_targets_resolve"] is True
    assert manifest_case["web_smoke_tests_declared"] is True
    assert manifest_case["web_smoke_entrypoint"] == "web.smoke"


def test_package_invalid_target_audit_reports_failure_counts(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_package_invalid_target(tmp_path, TOOLING_SAMPLE)

    assert report["format"] == "appgen.package-invalid-target-audit.v1"
    assert report["ok"] is True
    assert report["case_count"] == 2
    assert report["passing_case_count"] == 2
    assert report["failing_case_count"] == 0
    assert report["required_case_ids"] == ("package_invalid_target", "verify_invalid_target")
    assert report["observed_case_ids"] == report["required_case_ids"]
    assert report["missing_case_count"] == 0
    assert report["missing_case_ids"] == ()
    assert report["invalid_choice_message_count"] == 2
    assert report["invalid_choice_message_cases"] == report["required_case_ids"]
    assert report["missing_invalid_choice_message_count"] == 0
    assert report["missing_invalid_choice_message_cases"] == ()
    assert report["traceback_free_count"] == 2
    assert report["traceback_free_cases"] == report["required_case_ids"]
    assert report["missing_traceback_free_count"] == 0
    assert report["missing_traceback_free_cases"] == ()
    assert report["expected_exit_code_by_case"] == {
        "package_invalid_target": 2,
        "verify_invalid_target": 2,
    }
    assert report["exit_codes_by_case"] == report["expected_exit_code_by_case"]
    assert report["missing_expected_exit_code_count"] == 0
    assert report["missing_expected_exit_code_cases"] == ()
    assert report["case_ids"] == ("package_invalid_target", "verify_invalid_target")
    assert all(case["exit_code"] == 2 for case in report["cases"])


def test_package_verify_cli_audit_exposes_deployment_manifest_readiness_metadata(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_package_verify_cli(tmp_path, TOOLING_SAMPLE)
    manifest_case = next(case for case in report["cases"] if case["case"] == "package_writes_target_manifests")

    assert report["format"] == "appgen.package-verify-cli-audit.v1"
    assert report["ok"] is True
    assert manifest_case["deployment_artifact_class"] == "deployment_plan"
    assert {"units", "health_checks", "environment", "resource_hints", "topology_graph"} <= set(
        manifest_case["deployment_handoff_artifacts"]
    )
    assert manifest_case["deployment_units_declared"] is True
    assert manifest_case["deployment_health_checks_declared"] is True
    assert manifest_case["deployment_environment_variables_named"] is True
    assert manifest_case["deployment_secret_values_absent"] is True
    assert manifest_case["deployment_resource_hints_present"] is True
    assert manifest_case["deployment_topology_graph_connected"] is True
    assert manifest_case["deployment_topology_declared"] is True


def test_package_verify_cli_audit_exposes_native_package_metadata_and_smoke_readiness(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_package_verify_cli(tmp_path, TOOLING_SAMPLE)
    manifest_case = next(case for case in report["cases"] if case["case"] == "package_writes_target_manifests")

    assert report["format"] == "appgen.package-verify-cli-audit.v1"
    assert report["ok"] is True
    assert manifest_case["mobile_package_metadata_exists"] is True
    assert manifest_case["mobile_smoke_launch_path_exists"] is True
    assert manifest_case["mobile_smoke_entrypoint"] == "mobile.launch"
    assert manifest_case["desktop_package_metadata_exists"] is True
    assert manifest_case["desktop_smoke_launch_path_exists"] is True
    assert manifest_case["desktop_smoke_entrypoint"] == "desktop.launch"


def test_tooling_audit_proves_docs_tooling_surface_and_cli_contract() -> None:
    report = tooling_audit_report_dsl()
    root = Path(__file__).resolve().parents[1]
    cli_json = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "tooling-audit", "--json"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    cli_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "tooling-audit"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )

    assert report["format"] == "appgen.tooling-audit.v1"
    assert report["ok"] is True
    assert report["passed"] == report["required"] >= 16
    assert report["blocking_gaps"] == ()
    assert {
        "shared_semantic_model",
        "module_boundaries",
        "dsl_language_quality",
        "dsl_language_cli_contracts",
        "contract_schema_cli_contracts",
        "contract_validation_cli_contracts",
        "implementation_phase_exit_criteria",
        "language_server_core_features",
        "lsp_transport_rpc_contracts",
        "lsp_navigation_completion_contracts",
        "ide_visual_designer_round_trip",
        "vscode_extension_surface",
        "studio_semantic_service",
        "frontend_semantic_service_bridge",
        "frontend_interaction_audit_bridge",
        "cli_usage_failure_contracts",
        "validate_target_contracts",
        "generate_artifact_policy_contracts",
        "formatter_write_organize_contracts",
        "package_and_release_verifiers",
        "package_manifest_handoff_contracts",
        "release_text_evidence_contracts",
        "graph_rendering_contracts",
        "explain_cli_contracts",
        "migration_safety_text_contracts",
        "parser_golden_and_drift_gates",
        "parser_golden_fixture_contracts",
        "semantic_drift_surface_contracts",
        "doctor_cli_text_contracts",
        "tooling_doc_anchor_integrity",
        "non_goal_policy_guards",
        "tooling_audit_text_renderer",
        "component_publish_catalog_contracts",
        "pbc_publish_side_effect_contracts",
    } <= {check["id"] for check in report["checks"]}
    tooling_text_check = next(check for check in report["checks"] if check["id"] == "tooling_audit_text_renderer")
    assert tooling_text_check["detail"]["format"] == "appgen.tooling-audit-text-renderer.v1"
    assert tooling_text_check["detail"]["ok"] is True
    assert tooling_text_check["detail"]["missing_check_id_count"] == 0
    assert tooling_text_check["detail"]["missing_check_ids"] == ()
    assert tooling_text_check["detail"]["missing_section_count"] == 0
    assert tooling_text_check["detail"]["missing_sections"] == ()
    assert tooling_text_check["detail"]["missing_detail_format_count"] == 0
    assert tooling_text_check["detail"]["missing_detail_formats"] == ()
    assert tooling_text_check["detail"]["missing_blocking_gap_id_count"] == 0
    assert tooling_text_check["detail"]["missing_blocking_gap_ids"] == ()
    assert "tooling_doc_anchor_integrity" in tooling_text_check["detail"]["emitted_check_ids"]
    assert "docs/tooling.md#appgen-tooling-audit" in tooling_text_check["detail"]["emitted_sections"]
    assert "appgen.tooling-doc-anchor-audit.v1" in tooling_text_check["detail"]["emitted_detail_formats"]
    assert "studio_semantic_service" in tooling_text_check["detail"]["emitted_blocking_gap_ids"]
    assert tooling_text_check["detail"]["emitted_text_surfaces"] == tooling_text_check["detail"][
        "required_text_surfaces"
    ]
    assert tooling_text_check["detail"]["missing_text_surface_count"] == 0
    assert tooling_text_check["detail"]["missing_text_surfaces"] == ()
    assert tooling_text_check["detail"]["emitted_status_markers"] == tooling_text_check["detail"][
        "required_status_markers"
    ]
    assert tooling_text_check["detail"]["missing_status_marker_count"] == 0
    assert tooling_text_check["detail"]["missing_status_markers"] == ()
    assert tooling_text_check["detail"]["emitted_top_level_formats"] == tooling_text_check["detail"][
        "required_top_level_formats"
    ]
    assert tooling_text_check["detail"]["missing_top_level_format_count"] == 0
    assert tooling_text_check["detail"]["missing_top_level_formats"] == ()
    assert tooling_text_check["detail"]["emitted_source_documents"] == tooling_text_check["detail"][
        "required_source_documents"
    ]
    assert tooling_text_check["detail"]["missing_source_document_count"] == 0
    assert tooling_text_check["detail"]["missing_source_documents"] == ()
    assert tooling_text_check["detail"]["emitted_implementation_phase_markers"] == tooling_text_check["detail"][
        "required_implementation_phase_markers"
    ]
    assert tooling_text_check["detail"]["missing_implementation_phase_marker_count"] == 0
    assert tooling_text_check["detail"]["missing_implementation_phase_markers"] == ()
    semantic_check = next(check for check in report["checks"] if check["id"] == "shared_semantic_model")
    assert semantic_check["detail"]["contract_counts"]["required_top_level_field_count"] == 20
    assert semantic_check["detail"]["contract_counts"]["missing_top_level_field_count"] == 0
    assert semantic_check["detail"]["missing_top_level_fields"] == ()
    assert semantic_check["detail"]["symbol_coverage_counts"]["required_kind_count"] == (
        semantic_check["detail"]["symbol_coverage_counts"]["detected_kind_count"]
    )
    assert semantic_check["detail"]["symbol_coverage_counts"]["missing_kind_count"] == 0
    assert semantic_check["detail"]["symbol_coverage_counts"]["symbol_count"] > 0
    assert semantic_check["detail"]["source_set_cli"]["format"] == "appgen.semantic-source-set-cli-audit.v1"
    assert semantic_check["detail"]["source_set_cli"]["ok"] is True
    assert semantic_check["detail"]["source_set_cli"]["source_set_format"] == "appgen.semantic-source-set.v1"
    assert semantic_check["detail"]["source_set_cli"]["missing_symbol_file_count"] == 0
    assert semantic_check["detail"]["source_set_cli"]["missing_text_marker_count"] == 0
    language_check = next(check for check in report["checks"] if check["id"] == "dsl_language_quality")
    assert language_check["detail"]["format"] == "appgen.dsl-language-quality.v1"
    assert language_check["detail"]["ok"] is True
    assert language_check["detail"]["antlr_integrity"]["format"] == "appgen.dsl-antlr-integrity.v1"
    assert language_check["detail"]["antlr_integrity"]["ok"] is True
    assert language_check["detail"]["budget"]["format"] == "appgen.dsl-keyword-budget.v1"
    assert language_check["detail"]["budget"]["ok"] is True
    assert language_check["detail"]["canonical_keyword_count"] <= language_check["detail"]["budget"]["limit"]
    language_cli_check = next(check for check in report["checks"] if check["id"] == "dsl_language_cli_contracts")
    assert language_cli_check["detail"]["format"] == "appgen.dsl-language-cli-audit.v1"
    assert language_cli_check["detail"]["ok"] is True
    assert language_cli_check["detail"]["json_case_count"] == 4
    assert language_cli_check["detail"]["text_case_count"] == 4
    assert language_cli_check["detail"]["missing_case_count"] == 0
    assert language_cli_check["detail"]["missing_case_ids"] == ()
    assert language_cli_check["detail"]["failing_cases"] == ()
    assert language_cli_check["detail"]["missing_payload_format_case_count"] == 0
    assert language_cli_check["detail"]["missing_payload_format_cases"] == ()
    assert language_cli_check["detail"]["exit_codes_by_case"] == language_cli_check["detail"]["expected_exit_codes_by_case"]
    assert language_cli_check["detail"]["missing_exit_code_case_count"] == 0
    assert language_cli_check["detail"]["missing_exit_code_cases"] == ()
    assert language_cli_check["detail"]["ok_by_case"] == {
        "dsl_quality_json": True,
        "dsl_antlr_json": True,
        "dsl_authoring_gate_json": True,
        "dsl_language_service_json": True,
        "dsl_quality_text": True,
        "dsl_antlr_text": True,
        "dsl_authoring_gate_text": True,
        "dsl_language_service_text": True,
    }
    assert language_cli_check["detail"]["missing_ok_case_count"] == 0
    assert language_cli_check["detail"]["missing_ok_cases"] == ()
    assert language_cli_check["detail"]["text_exit_codes_by_case"] == (
        language_cli_check["detail"]["expected_text_exit_codes_by_case"]
    )
    assert language_cli_check["detail"]["missing_text_exit_code_case_count"] == 0
    assert language_cli_check["detail"]["missing_text_exit_code_cases"] == ()
    assert language_cli_check["detail"]["missing_text_marker_count"] == 0
    assert language_cli_check["detail"]["missing_text_marker_cases"] == ()
    assert language_cli_check["detail"]["text_json_fallback_by_case"] == {
        "dsl_quality_text": False,
        "dsl_antlr_text": False,
        "dsl_authoring_gate_text": False,
        "dsl_language_service_text": False,
    }
    assert language_cli_check["detail"]["text_json_fallback_case_count"] == 0
    assert language_cli_check["detail"]["text_json_fallback_cases"] == ()
    assert language_cli_check["detail"]["observed_case_ids"] == language_cli_check["detail"]["required_case_ids"]
    assert language_cli_check["detail"]["payload_formats_by_case"] == (
        language_cli_check["detail"]["expected_payload_formats_by_case"]
    )
    assert language_cli_check["detail"]["language_quality_format"] == "appgen.dsl-language-quality.v1"
    assert language_cli_check["detail"]["antlr_integrity_format"] == "appgen.dsl-antlr-integrity.v1"
    assert language_cli_check["detail"]["authoring_gate_format"] == "appgen.dsl-authoring-release-gate.v1"
    assert language_cli_check["detail"]["language_service_format"] == "appgen.dsl-language-service.v1"
    contract_schema_check = next(check for check in report["checks"] if check["id"] == "contract_schema_cli_contracts")
    assert contract_schema_check["detail"]["format"] == "appgen.contract-schema-cli-audit.v1"
    assert contract_schema_check["detail"]["ok"] is True
    assert contract_schema_check["detail"]["required_schema_count"] == len(appgen_dsl.CONTRACT_SCHEMA_REQUIRED_FORMATS)
    assert contract_schema_check["detail"]["missing_required_schema_count"] == 0
    assert contract_schema_check["detail"]["missing_required_schema_formats"] == ()
    assert contract_schema_check["detail"]["missing_case_count"] == 0
    assert contract_schema_check["detail"]["missing_exit_code_case_count"] == 0
    assert contract_schema_check["detail"]["missing_payload_format_case_count"] == 0
    assert contract_schema_check["detail"]["sample_validation_case_count"] == len(
        appgen_dsl.CONTRACT_SCHEMA_REQUIRED_FORMATS
    )
    assert contract_schema_check["detail"]["sample_validation_passing_count"] == contract_schema_check["detail"][
        "sample_validation_case_count"
    ]
    assert contract_schema_check["detail"]["sample_validation_failing_count"] == 0
    assert contract_schema_check["detail"]["sample_validation_missing_count"] == 0
    assert contract_schema_check["detail"]["missing_text_marker_count"] == 0
    assert contract_schema_check["detail"]["text_json_fallback"] is False
    assert {"format", "ok", "app", "symbols", "tables", "views", "diagnostics"} <= set(
        contract_schema_check["detail"]["semantic_required_fields"]
    )
    contract_validation_check = next(
        check for check in report["checks"] if check["id"] == "contract_validation_cli_contracts"
    )
    assert contract_validation_check["detail"]["format"] == "appgen.contract-validation-cli-audit.v1"
    assert contract_validation_check["detail"]["ok"] is True
    assert contract_validation_check["detail"]["case_count"] == 7
    assert contract_validation_check["detail"]["passing_case_count"] == contract_validation_check["detail"]["case_count"]
    assert contract_validation_check["detail"]["missing_case_count"] == 0
    assert contract_validation_check["detail"]["missing_exit_code_case_count"] == 0
    assert contract_validation_check["detail"]["missing_payload_format_case_count"] == 0
    assert contract_validation_check["detail"]["missing_text_marker_count"] == 0
    assert contract_validation_check["detail"]["text_json_fallback"] is False
    assert contract_validation_check["detail"]["valid_report_format"] == "appgen.contract-validation-report.v1"
    assert contract_validation_check["detail"]["valid_payload_format"] == "appgen.semantic-model.v1"
    assert contract_validation_check["detail"]["valid_schema_format"] == "appgen.semantic-model.v1"
    assert contract_validation_check["detail"]["self_report_payload_format"] == "appgen.contract-validation-report.v1"
    assert contract_validation_check["detail"]["self_report_schema_format"] == "appgen.contract-validation-report.v1"
    assert contract_validation_check["detail"]["missing_required_error_count"] >= 1
    assert contract_validation_check["detail"]["unknown_schema_available"] is False
    assert contract_validation_check["detail"]["malformed_diagnostic_count"] >= 1
    non_goal_check = next(check for check in report["checks"] if check["id"] == "non_goal_policy_guards")
    assert non_goal_check["detail"]["format"] == "appgen.non-goal-policy-audit.v1"
    assert non_goal_check["detail"]["ok"] is True
    assert non_goal_check["detail"]["case_count"] == len(non_goal_check["detail"]["cases"])
    assert non_goal_check["detail"]["passing_case_count"] == non_goal_check["detail"]["case_count"]
    assert non_goal_check["detail"]["diagnostic_code_count"] >= 3
    assert non_goal_check["detail"]["fix_count"] >= 2
    assert non_goal_check["detail"]["rejected_prompt_count"] == 3
    assert non_goal_check["detail"]["zero_patch_rejection_count"] == 3
    non_goal_cases = {case["case"]: case for case in non_goal_check["detail"]["cases"]}
    assert non_goal_cases["reject_secret_literal"]["secret_removed"] is True
    assert non_goal_cases["reject_secret_literal"]["fixed_contains_env_binding"] is True
    assert non_goal_cases["reject_runtime_picker_fields"]["picker_fields_removed"] is True
    assert non_goal_cases["reject_generated_code_bypass_prompt"]["accepted"] is False
    assert non_goal_cases["reject_generated_code_bypass_prompt"]["patch_bytes"] == 0
    assert non_goal_cases["reject_lint_semantic_bypass_prompt"]["patch_bytes"] == 0
    assert "AGX1201" in non_goal_cases["reject_lint_semantic_bypass_prompt"]["diagnostic_codes"]
    assert non_goal_cases["reject_release_evidence_bypass_prompt"]["patch_bytes"] == 0
    assert "AGX1201" in non_goal_cases["reject_release_evidence_bypass_prompt"]["diagnostic_codes"]
    assert report["doc_anchor_integrity"]["format"] == "appgen.tooling-doc-anchor-audit.v1"
    assert report["doc_anchor_integrity"]["ok"] is True
    assert report["doc_anchor_integrity"]["missing_sections"] == ()
    assert report["doc_anchor_integrity"]["documented_contract_format_count"] >= 50
    assert report["doc_anchor_integrity"]["runtime_covered_format_count"] == (
        report["doc_anchor_integrity"]["documented_contract_format_count"]
    )
    assert report["doc_anchor_integrity"]["test_covered_format_count"] == (
        report["doc_anchor_integrity"]["documented_contract_format_count"]
    )
    assert report["doc_anchor_integrity"]["missing_runtime_formats"] == ()
    assert report["doc_anchor_integrity"]["runtime_reference_gap_count"] == 0
    assert report["doc_anchor_integrity"]["missing_test_formats"] == ()
    assert report["doc_anchor_integrity"]["test_reference_gap_count"] == 0
    assert report["doc_anchor_integrity"]["minimum_runtime_format_reference_count"] >= 1
    assert report["doc_anchor_integrity"]["minimum_test_format_reference_count"] >= 1
    assert "appgen.studio-semantic-service.v1" in report["doc_anchor_integrity"]["documented_contract_formats"]
    assert report["doc_anchor_integrity"]["format_reference_matrix"]["appgen.studio-semantic-service.v1"][
        "docs"
    ] >= 1
    assert report["doc_anchor_integrity"]["format_reference_matrix"]["appgen.studio-semantic-service.v1"][
        "runtime"
    ] >= 1
    assert report["doc_anchor_integrity"]["format_reference_matrix"]["appgen.studio-semantic-service.v1"][
        "tests"
    ] >= 1
    assert "docs/tooling.md#cli-contracts" in report["doc_anchor_integrity"]["referenced_sections"]
    assert "docs/tooling.md#diagnostic-specification" in report["doc_anchor_integrity"]["referenced_sections"]
    assert "docs/tooling.md#linter-rules-by-domain" in report["doc_anchor_integrity"]["referenced_sections"]
    assert "docs/tooling.md#command-line-interface" not in report["doc_anchor_integrity"]["referenced_sections"]
    assert appgen_dsl._tooling_audit_doc_refs(
        {
            "section": "docs/tooling.md#cli-contracts",
            "detail": {"docs_url": "docs/tooling.md#diagnostic-specification"},
        }
    ) == ("docs/tooling.md#cli-contracts", "docs/tooling.md#diagnostic-specification")
    anchor_check = next(check for check in report["checks"] if check["id"] == "tooling_doc_anchor_integrity")
    assert anchor_check["detail"]["ok"] is True
    assert anchor_check["detail"]["missing_sections"] == ()
    assert anchor_check["detail"]["missing_runtime_formats"] == ()
    assert anchor_check["detail"]["missing_test_formats"] == ()
    assert anchor_check["detail"]["runtime_covered_format_count"] == (
        anchor_check["detail"]["documented_contract_format_count"]
    )
    assert anchor_check["detail"]["test_covered_format_count"] == anchor_check["detail"]["documented_contract_format_count"]
    assert anchor_check["detail"]["runtime_reference_gap_count"] == 0
    assert anchor_check["detail"]["test_reference_gap_count"] == 0
    module_check = next(check for check in report["checks"] if check["id"] == "module_boundaries")
    assert module_check["detail"]["format"] == "appgen.module-boundary-audit.v1"
    assert module_check["detail"]["ok"] is True
    assert module_check["detail"]["missing_boundaries"] == ()
    assert module_check["detail"]["core_runtime_gaps"] == ()
    phase_check = next(check for check in report["checks"] if check["id"] == "implementation_phase_exit_criteria")
    assert phase_check["detail"]["format"] == "appgen.tooling-implementation-phase-audit.v1"
    assert phase_check["detail"]["ok"] is True
    assert phase_check["detail"]["required_phase_ids"] == phase_check["detail"]["phase_ids"]
    assert phase_check["detail"]["missing_required_phase_count"] == 0
    assert phase_check["detail"]["missing_required_phase_ids"] == ()
    assert phase_check["detail"]["required_exit_criteria_by_phase"] == phase_check["detail"][
        "observed_exit_criteria_by_phase"
    ]
    assert phase_check["detail"]["missing_required_exit_criteria_phase_count"] == 0
    assert phase_check["detail"]["missing_required_exit_criteria_by_phase"] == {}
    assert phase_check["detail"]["missing_phases"] == ()
    assert {phase["id"] for phase in phase_check["detail"]["phases"]} == {
        "phase_0_inventory_and_stabilization",
        "phase_1_shared_semantic_model_mvp",
        "phase_2_linter_and_formatter",
        "phase_3_cli_and_graph_tooling",
        "phase_4_language_server",
        "phase_5_ide_and_visual_designer_integration",
        "phase_6_migration_natural_language_and_release_verifiers",
    }
    assert all(phase["missing_exit_criteria"] == () for phase in phase_check["detail"]["phases"])
    assert all(phase["passing_exit_criteria"] for phase in phase_check["detail"]["phases"])
    assert phase_check["detail"]["passing_exit_criteria"] == phase_check["detail"]["exit_criterion_ids"]
    assert phase_check["detail"]["missing_exit_criteria_by_phase"] == {}
    assert phase_check["detail"]["exit_criterion_evidence_formats_by_phase"][
        "phase_5_ide_and_visual_designer_integration"
    ]["frontend_browser_smoke_bridges"] == (
        "appgen.studio-browser-smoke-ci-contract.v1",
        "appgen.frontend-semantic-service-audit.v1",
        "appgen.frontend-interaction-audit.v1",
    )
    phase_doc_check = next(
        check for check in report["checks"] if check["id"] == "implementation_phase_doc_alignment_contracts"
    )
    assert phase_doc_check["detail"]["format"] == "appgen.implementation-phase-doc-alignment.v1"
    assert phase_doc_check["detail"]["ok"] is True
    assert phase_doc_check["detail"]["phase_heading_count"] == phase_check["detail"]["phase_count"]
    assert phase_doc_check["detail"]["runtime_phase_count"] == phase_check["detail"]["phase_count"]
    assert phase_doc_check["detail"]["documented_phase_ids"] == phase_check["detail"]["phase_ids"]
    assert phase_doc_check["detail"]["missing_phase_heading_count"] == 0
    assert phase_doc_check["detail"]["extra_phase_heading_count"] == 0
    assert phase_doc_check["detail"]["title_mismatch_count"] == 0
    assert phase_doc_check["detail"]["exit_criteria_label_count"] == phase_check["detail"]["phase_count"]
    assert phase_doc_check["detail"]["missing_exit_phrase_count"] == 0
    contributor_check = next(check for check in report["checks"] if check["id"] == "contributor_task_breakdown_contracts")
    assert contributor_check["detail"]["format"] == "appgen.contributor-task-contract-audit.v1"
    assert contributor_check["detail"]["ok"] is True
    assert contributor_check["detail"]["group_count"] == 3
    assert contributor_check["detail"]["required_groups"] == ("good_first", "intermediate", "advanced")
    assert contributor_check["detail"]["groups"] == ("good_first", "intermediate", "advanced")
    assert contributor_check["detail"]["missing_required_group_count"] == 0
    assert contributor_check["detail"]["missing_required_groups"] == ()
    assert contributor_check["detail"]["task_count"] == 22
    assert contributor_check["detail"]["passing_task_count"] == contributor_check["detail"]["task_count"]
    assert contributor_check["detail"]["missing_task_count"] == 0
    assert contributor_check["detail"]["missing_tasks"] == ()
    assert contributor_check["detail"]["required_task_names"] == contributor_check["detail"]["task_names"]
    assert contributor_check["detail"]["missing_required_task_count"] == 0
    assert contributor_check["detail"]["missing_required_task_names"] == ()
    assert {
        "define_diagnostic_dataclasses_and_json_schema",
        "pbc_catalog_binding_in_semantic_model",
        "safe_rename_across_workspace",
        "cross_tool_drift_tests",
    } <= set(contributor_check["detail"]["task_names"])
    assert all(task["evidence_format"] for task in contributor_check["detail"]["tasks"])
    priority_check = next(check for check in report["checks"] if check["id"] == "priority_order_contracts")
    assert priority_check["detail"]["format"] == "appgen.priority-order-contract-audit.v1"
    assert priority_check["detail"]["ok"] is True
    assert priority_check["detail"]["priority_count"] == 10
    assert priority_check["detail"]["passing_priority_count"] == priority_check["detail"]["priority_count"]
    assert priority_check["detail"]["missing_priority_count"] == 0
    assert priority_check["detail"]["missing_priorities"] == ()
    assert priority_check["detail"]["required_priority_ids"] == priority_check["detail"]["priority_ids"]
    assert priority_check["detail"]["missing_required_priority_count"] == 0
    assert priority_check["detail"]["missing_required_priority_ids"] == ()
    assert priority_check["detail"]["documented_item_count"] == 10
    assert priority_check["detail"]["document_order_matches"] is True
    assert priority_check["detail"]["documented_items"] == priority_check["detail"]["expected_items"]
    assert priority_check["detail"]["priority_ids"] == (
        "shared_parser_and_semantic_model",
        "diagnostic_registry_and_linter",
        "formatter",
        "cli_json_contracts",
        "graph_and_explain_tooling",
        "language_server",
        "vscode_and_monaco_integration",
        "migration_planner",
        "natural_language_dsl_diff_planner",
        "package_and_release_verifiers",
    )
    assert all(item["evidence_format"] for item in priority_check["detail"]["priorities"])
    section_coverage_check = next(check for check in report["checks"] if check["id"] == "tooling_section_coverage_contracts")
    assert section_coverage_check["detail"]["format"] == "appgen.tooling-section-coverage-audit.v1"
    assert section_coverage_check["detail"]["ok"] is True
    assert section_coverage_check["detail"]["required_section_count"] == 18
    assert section_coverage_check["detail"]["covered_section_count"] == (
        section_coverage_check["detail"]["required_section_count"]
    )
    assert section_coverage_check["detail"]["missing_section_count"] == 0
    assert section_coverage_check["detail"]["missing_sections"] == ()
    assert section_coverage_check["detail"]["required_subsection_count"] == 42
    assert section_coverage_check["detail"]["covered_subsection_count"] == (
        section_coverage_check["detail"]["required_subsection_count"]
    )
    assert section_coverage_check["detail"]["missing_subsection_count"] == 0
    assert section_coverage_check["detail"]["missing_subsections"] == ()
    assert section_coverage_check["detail"]["stale_mapping_count"] == 0
    assert section_coverage_check["detail"]["stale_subsection_mapping_count"] == 0
    assert {
        "goals",
        "core-architecture",
        "cli-contracts",
        "implementation-phases",
        "priority-order",
    } <= set(section_coverage_check["detail"]["covered_sections"])
    assert {
        "appgen-lint",
        "appgen-contract-schema",
        "appgen-contract-validate",
        "code-actions",
        "parser-golden-audit",
        "phase-6-migration-natural-language-and-release-verifiers",
    } <= set(section_coverage_check["detail"]["covered_subsections"])
    vscode_check = next(check for check in report["checks"] if check["id"] == "vscode_extension_surface")
    assert vscode_check["detail"]["checks"]["diagnostics_collection"] is True
    assert vscode_check["detail"]["checks"]["cli_command_contracts"] is True
    assert vscode_check["detail"]["checks"]["webview_renderers"] is True
    designer_check = next(check for check in report["checks"] if check["id"] == "ide_visual_designer_round_trip")
    assert designer_check["detail"]["cli"]["format"] == "appgen.designer-sync-cli-audit.v1"
    assert designer_check["detail"]["cli"]["ok"] is True
    assert designer_check["detail"]["cli"]["scenario_count"] == 4
    assert designer_check["detail"]["cli"]["passing_scenario_count"] == 4
    assert designer_check["detail"]["cli"]["missing_scenario_count"] == 0
    assert designer_check["detail"]["cli"]["failing_scenario_count"] == 0
    assert designer_check["detail"]["cli"]["exit_codes_by_scenario"] == designer_check["detail"]["cli"][
        "expected_exit_codes_by_scenario"
    ]
    assert designer_check["detail"]["cli"]["missing_exit_code_scenario_count"] == 0
    assert designer_check["detail"]["cli"]["missing_exit_code_scenarios"] == ()
    assert designer_check["detail"]["cli"]["payload_formats_by_scenario"] == designer_check["detail"]["cli"][
        "expected_payload_formats_by_scenario"
    ]
    assert designer_check["detail"]["cli"]["missing_payload_format_scenario_count"] == 0
    assert designer_check["detail"]["cli"]["missing_payload_format_scenarios"] == ()
    assert designer_check["detail"]["cli"]["ok_by_scenario"] == {
        scenario: True for scenario in designer_check["detail"]["cli"]["required_scenario_ids"]
    }
    assert designer_check["detail"]["cli"]["missing_ok_scenario_count"] == 0
    assert designer_check["detail"]["cli"]["missing_ok_scenarios"] == ()
    assert designer_check["detail"]["cli"]["valid_changed_surface_count"] >= 1
    assert designer_check["detail"]["cli"]["missing_changed_surface_count"] == 0
    assert designer_check["detail"]["cli"]["projection_count"] >= 1
    assert set(designer_check["detail"]["cli"]["projection_ids"]) == set(
        designer_check["detail"]["cli"]["required_projection_ids"]
    )
    assert designer_check["detail"]["cli"]["missing_projection_count"] == 0
    assert designer_check["detail"]["cli"]["invalid_case_count"] == 2
    assert designer_check["detail"]["cli"]["traceback_free_count"] == 2
    assert designer_check["detail"]["cli"]["traceback_free_case_ids"] == designer_check["detail"]["cli"]["invalid_case_ids"]
    assert designer_check["detail"]["cli"]["missing_traceback_free_case_count"] == 0
    assert designer_check["detail"]["cli"]["valid_round_trip"] is True
    assert "database_designer" in designer_check["detail"]["cli"]["valid_changed_surfaces"]
    assert designer_check["detail"]["cli"]["valid_diff_lines"] > 0
    assert designer_check["detail"]["cli"]["missing_diff_fragment_count"] == 0
    assert designer_check["detail"]["cli"]["valid_semantic_model_format"] == "appgen.semantic-model.v1"
    assert designer_check["detail"]["cli"]["valid_projection_semantic_model_format"] == "appgen.semantic-model.v1"
    assert designer_check["detail"]["cli"]["bulk_result_format"] == "appgen.designer-visual-transaction-result.v1"
    assert designer_check["detail"]["cli"]["bulk_atomic"] is True
    assert designer_check["detail"]["cli"]["bulk_round_trip"] is True
    assert designer_check["detail"]["cli"]["bulk_operation_count"] == 5
    assert set(designer_check["detail"]["cli"]["required_bulk_changed_surfaces"]) <= set(
        designer_check["detail"]["cli"]["bulk_changed_surfaces"]
    )
    assert designer_check["detail"]["cli"]["missing_bulk_changed_surfaces"] == ()
    assert designer_check["detail"]["cli"]["bulk_patch_count"] == 5
    assert designer_check["detail"]["cli"]["bulk_semantic_model_format"] == "appgen.semantic-model.v1"
    assert designer_check["detail"]["cli"]["non_object_exit"] == 2
    assert "--edit-json must be a JSON object" in designer_check["detail"]["cli"]["non_object_stderr"]
    assert designer_check["detail"]["text_renderer"]["emitted_surfaces"] == designer_check["detail"]["text_renderer"][
        "required_surfaces"
    ]
    assert designer_check["detail"]["text_renderer"]["missing_surface_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_surfaces"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_changed_surfaces"] == designer_check["detail"][
        "text_renderer"
    ]["required_changed_surfaces"]
    assert designer_check["detail"]["text_renderer"]["missing_changed_surface_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_changed_surfaces"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_operations"] == designer_check["detail"]["text_renderer"][
        "required_operations"
    ]
    assert designer_check["detail"]["text_renderer"]["missing_operation_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_operations"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_case_ids"] == designer_check["detail"]["text_renderer"][
        "required_case_ids"
    ]
    assert designer_check["detail"]["text_renderer"]["missing_case_id_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_case_ids"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_check_ids"] == designer_check["detail"]["text_renderer"][
        "required_check_ids"
    ]
    assert designer_check["detail"]["text_renderer"]["missing_check_id_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_check_ids"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_diff_snippets"] == designer_check["detail"][
        "text_renderer"
    ]["required_diff_snippets"]
    assert designer_check["detail"]["text_renderer"]["missing_diff_snippet_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_diff_snippets"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_text_surfaces"] == designer_check["detail"][
        "text_renderer"
    ]["required_text_surfaces"]
    assert designer_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_contract_formats"] == designer_check["detail"][
        "text_renderer"
    ]["required_contract_formats"]
    assert designer_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert designer_check["detail"]["text_renderer"]["emitted_status_markers"] == designer_check["detail"][
        "text_renderer"
    ]["required_status_markers"]
    assert designer_check["detail"]["text_renderer"]["missing_status_marker_count"] == 0
    assert designer_check["detail"]["text_renderer"]["missing_status_markers"] == ()
    studio_check = next(check for check in report["checks"] if check["id"] == "studio_semantic_service")
    assert studio_check["detail"]["format"] == "appgen.studio-semantic-service-audit.v1"
    assert studio_check["detail"]["ok"] is True
    assert studio_check["detail"]["blocking_gaps"] == ()
    assert studio_check["detail"]["checks"]["surface_formats"] is True
    assert studio_check["detail"]["checks"]["semantic_surface_formats"] is True
    assert studio_check["detail"]["checks"]["diagnostics_quick_fixes"] is True
    assert studio_check["detail"]["checks"]["graph_explain"] is True
    assert studio_check["detail"]["checks"]["natural_language_evolution"] is True
    assert set(studio_check["detail"]["required_surfaces"]) <= set(studio_check["detail"]["surfaces"])
    assert studio_check["detail"]["surface_formats"]["diagnostics_panel"] == "appgen.lsp-diagnostics.v1"
    assert studio_check["detail"]["surface_formats"]["graph_explain_panel"] == "appgen.designer-graph-explain-panel.v1"
    assert studio_check["detail"]["surface_formats"]["natural_language_planner"] == "appgen.designer-nl-planner-panel.v1"
    frontend_semantic_check = next(check for check in report["checks"] if check["id"] == "frontend_semantic_service_bridge")
    assert frontend_semantic_check["detail"]["format"] == "appgen.frontend-semantic-service-audit.v1"
    assert frontend_semantic_check["detail"]["audit"]["ok"] is True
    assert set(frontend_semantic_check["detail"]["required_services"]) <= set(frontend_semantic_check["detail"]["services"])
    assert frontend_semantic_check["detail"]["missing_services"] == ()
    assert set(frontend_semantic_check["detail"]["required_surfaces"]) <= set(frontend_semantic_check["detail"]["surfaces"])
    assert frontend_semantic_check["detail"]["missing_surfaces"] == ()
    assert set(frontend_semantic_check["detail"]["required_surface_contracts"]) <= set(
        frontend_semantic_check["detail"]["surface_contracts"]
    )
    assert frontend_semantic_check["detail"]["missing_surface_contracts"] == ()
    assert frontend_semantic_check["detail"]["service_count"] == frontend_semantic_check["detail"]["required_service_count"]
    assert frontend_semantic_check["detail"]["surface_count"] == frontend_semantic_check["detail"]["required_surface_count"]
    assert (
        frontend_semantic_check["detail"]["surface_contract_count"]
        == frontend_semantic_check["detail"]["required_surface_contract_count"]
    )
    assert frontend_semantic_check["detail"]["missing_service_count"] == 0
    assert frontend_semantic_check["detail"]["missing_surface_count"] == 0
    assert frontend_semantic_check["detail"]["missing_surface_contract_count"] == 0
    frontend_interaction_check = next(check for check in report["checks"] if check["id"] == "frontend_interaction_audit_bridge")
    assert frontend_interaction_check["detail"]["format"] == "appgen.frontend-interaction-audit.v1"
    assert frontend_interaction_check["detail"]["audit"]["ok"] is True
    assert frontend_interaction_check["detail"]["scenario_count"] == 9
    assert "actionable_drag_drop_wiring_operations" in frontend_interaction_check["detail"]["scenarios"]
    assert set(frontend_interaction_check["detail"]["required_scenarios"]) <= set(
        frontend_interaction_check["detail"]["scenarios"]
    )
    assert frontend_interaction_check["detail"]["missing_scenarios"] == ()
    assert set(frontend_interaction_check["detail"]["required_audit_inputs"]) <= set(
        frontend_interaction_check["detail"]["audit_inputs"]
    )
    assert frontend_interaction_check["detail"]["missing_audit_inputs"] == ()
    assert set(frontend_interaction_check["detail"]["required_helpers"]) <= set(
        frontend_interaction_check["detail"]["helpers"]
    )
    assert frontend_interaction_check["detail"]["missing_helpers"] == ()
    assert (
        frontend_interaction_check["detail"]["scenario_count"]
        == frontend_interaction_check["detail"]["required_scenario_count"]
    )
    assert (
        frontend_interaction_check["detail"]["audit_input_count"]
        == frontend_interaction_check["detail"]["required_audit_input_count"]
    )
    assert frontend_interaction_check["detail"]["helper_count"] == frontend_interaction_check["detail"]["required_helper_count"]
    assert frontend_interaction_check["detail"]["missing_scenario_count"] == 0
    assert frontend_interaction_check["detail"]["missing_audit_input_count"] == 0
    assert frontend_interaction_check["detail"]["missing_helper_count"] == 0
    lsp_check = next(check for check in report["checks"] if check["id"] == "language_server_core_features")
    assert lsp_check["detail"]["symbol_coverage"]["format"] == "appgen.lsp-symbol-coverage.v1"
    assert lsp_check["detail"]["symbol_coverage"]["ok"] is True
    assert lsp_check["detail"]["symbol_coverage"]["document_missing_kind_count"] == 0
    assert lsp_check["detail"]["symbol_coverage"]["workspace_missing_kind_count"] == 0
    assert lsp_check["detail"]["rpc"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_check["detail"]["rpc"]["blocking_gaps"] == ()
    assert lsp_check["detail"]["rpc"]["check_count"] == len(lsp_check["detail"]["rpc"]["checks"])
    assert lsp_check["detail"]["rpc"]["passing_check_count"] == lsp_check["detail"]["rpc"]["check_count"]
    assert lsp_check["detail"]["rpc"]["provider_count"] == 9
    assert lsp_check["detail"]["rpc"]["enabled_provider_count"] == 9
    assert lsp_check["detail"]["rpc"]["request_check_count"] == 8
    assert lsp_check["detail"]["rpc"]["code_action_count"] >= 1
    assert lsp_check["detail"]["rpc"]["formatting_edit_count"] >= 1
    assert lsp_check["detail"]["stdio"]["format"] == "appgen.lsp-stdio-transport-audit.v1"
    assert lsp_check["detail"]["stdio"]["request_message_count"] == 4
    assert lsp_check["detail"]["stdio"]["response_count"] >= lsp_check["detail"]["stdio"]["request_message_count"]
    assert lsp_check["detail"]["stdio"]["id_response_count"] >= lsp_check["detail"]["stdio"]["request_message_count"]
    assert lsp_check["detail"]["stdio"]["notification_count"] >= 2
    assert lsp_check["detail"]["stdio"]["method_count"] >= 1
    assert lsp_check["detail"]["rename_cli"]["format"] == "appgen.lsp-rename-cli-audit.v1"
    assert lsp_check["detail"]["rename_cli"]["ok"] is True
    assert lsp_check["detail"]["rename_cli"]["passing_scenario_count"] == (
        lsp_check["detail"]["rename_cli"]["scenario_count"]
    )
    assert lsp_check["detail"]["rename_cli"]["failing_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["failing_scenarios"] == ()
    assert lsp_check["detail"]["rename_cli"]["observed_scenario_ids"] == (
        lsp_check["detail"]["rename_cli"]["required_scenario_ids"]
    )
    assert lsp_check["detail"]["rename_cli"]["missing_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["missing_scenario_ids"] == ()
    assert lsp_check["detail"]["rename_cli"]["observed_modes_by_scenario"] == (
        lsp_check["detail"]["rename_cli"]["required_modes_by_scenario"]
    )
    assert lsp_check["detail"]["rename_cli"]["missing_mode_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["missing_mode_scenarios"] == ()
    assert lsp_check["detail"]["rename_cli"]["observed_scopes_by_scenario"] == (
        lsp_check["detail"]["rename_cli"]["required_scopes_by_scenario"]
    )
    assert lsp_check["detail"]["rename_cli"]["missing_scope_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["missing_scope_scenarios"] == ()
    assert lsp_check["detail"]["rename_cli"]["exit_codes_by_scenario"] == (
        lsp_check["detail"]["rename_cli"]["expected_exit_codes_by_scenario"]
    )
    assert lsp_check["detail"]["rename_cli"]["missing_exit_code_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["missing_exit_code_scenarios"] == ()
    assert lsp_check["detail"]["rename_cli"]["payload_formats_by_scenario"] == (
        lsp_check["detail"]["rename_cli"]["expected_payload_formats_by_scenario"]
    )
    assert lsp_check["detail"]["rename_cli"]["missing_payload_format_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["missing_payload_format_scenarios"] == ()
    assert lsp_check["detail"]["rename_cli"]["ok_by_scenario"] == {
        scenario: True for scenario in lsp_check["detail"]["rename_cli"]["required_scenario_ids"]
    }
    assert lsp_check["detail"]["rename_cli"]["missing_ok_scenario_count"] == 0
    assert lsp_check["detail"]["rename_cli"]["missing_ok_scenarios"] == ()
    assert lsp_check["detail"]["rename_cli"]["safe_json_scenario_count"] == 5
    assert lsp_check["detail"]["rename_cli"]["blocked_json_scenario_count"] == 5
    assert lsp_check["detail"]["rename_cli"]["blocked_text_scenario_count"] == 1
    assert lsp_check["detail"]["rename_cli"]["rename_format"] == "appgen.lsp-rename.v1"
    assert lsp_check["detail"]["rename_cli"]["token"] == "SubmitInvoice"
    assert lsp_check["detail"]["rename_cli"]["new_name"] == "PostInvoice"
    assert lsp_check["detail"]["rename_cli"]["lexical_scope"] == "flow_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["lexical_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["lexical_occurrence_count"] == 4
    assert lsp_check["detail"]["rename_cli"]["lexical_symbol_scope"] == "operation_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["lexical_field_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["lexical_string_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["lexical_comment_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["table_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["table_scope"] == "table_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["table_occurrence_count"] == 4
    assert lsp_check["detail"]["rename_cli"]["table_field_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["view_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["view_scope"] == "view_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["view_occurrence_count"] == 2
    assert lsp_check["detail"]["rename_cli"]["view_field_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["view_operation_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["pbc_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["pbc_scope"] == "pbc_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["pbc_occurrence_count"] == 7
    assert lsp_check["detail"]["rename_cli"]["event_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["event_scope"] == "event_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["package_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["package_scope"] == "package_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["deployment_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["deployment_scope"] == "deployment_unit_declarations_and_targets"
    assert lsp_check["detail"]["rename_cli"]["field_scope_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["field_scope"] == "field_declarations_and_bindings"
    assert lsp_check["detail"]["rename_cli"]["field_occurrence_count"] == 4
    assert lsp_check["detail"]["rename_cli"]["field_other_table_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["field_operation_preserved"] is True
    assert lsp_check["detail"]["rename_cli"]["changed"] is True
    assert lsp_check["detail"]["rename_cli"]["migration_format"] == "appgen.migration-plan.v1"
    assert lsp_check["detail"]["rename_cli"]["safe_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["blocked_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["blocked_rename_ok"] is False
    assert lsp_check["detail"]["rename_cli"]["blocked"] is True
    assert lsp_check["detail"]["rename_cli"]["blocked_text_ok"] is True
    assert "requires_approval=True" in lsp_check["detail"]["rename_cli"]["blocked_text"]
    assert "rename-blocker AGX1101:" in lsp_check["detail"]["rename_cli"]["blocked_text"]
    assert "fixes=add_rename_hint" in lsp_check["detail"]["rename_cli"]["blocked_text"]
    assert lsp_check["detail"]["rename_cli"]["blocked_code"] == "AGX1101"
    assert lsp_check["detail"]["rename_cli"]["blocked_fix"] == "add_rename_hint"
    assert lsp_check["detail"]["rename_cli"]["blocked_requires_approval"] is True
    assert {
        "did_change_diagnostics",
        "completion_context_filtering",
        "hover_relationship_lookup_depth",
        "hover_handler_target_depth",
        "hover_catalog_diagnostic_depth",
        "workspace_symbol_catalog_result_depth",
        "reference_catalog_index_depth",
        "workspace_document_scan_and_rename",
        "editor_lifecycle_workflow",
        "enterprise_definition_context",
        "lexical_reference_scope",
        "code_action_request",
        "formatting_request",
    } <= {check["check"] for check in lsp_check["detail"]["rpc"]["checks"]}
    lsp_transport_check = next(check for check in report["checks"] if check["id"] == "lsp_transport_rpc_contracts")
    assert lsp_transport_check["detail"]["rpc"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_transport_check["detail"]["rpc"]["provider_count"] == 9
    assert lsp_transport_check["detail"]["rpc"]["enabled_provider_count"] == 9
    assert lsp_transport_check["detail"]["rpc"]["request_check_count"] == 8
    assert lsp_transport_check["detail"]["rpc"]["passing_request_check_count"] == 8
    assert lsp_transport_check["detail"]["rpc"]["method_contract_count"] == 11
    assert lsp_transport_check["detail"]["rpc"]["passing_method_contract_count"] == (
        lsp_transport_check["detail"]["rpc"]["method_contract_count"]
    )
    assert lsp_transport_check["detail"]["rpc"]["missing_method_contract_count"] == 0
    assert lsp_transport_check["detail"]["rpc"]["missing_method_contracts"] == ()
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_case_count"] == 14
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_passing_case_count"] == (
        lsp_transport_check["detail"]["rpc"]["editor_workflow_case_count"]
    )
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_failing_case_count"] == 0
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_failing_cases"] == ()
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_case_ids"] == (
        lsp_transport_check["detail"]["rpc"]["required_editor_workflow_case_ids"]
    )
    assert lsp_transport_check["detail"]["rpc"]["missing_editor_workflow_case_count"] == 0
    assert lsp_transport_check["detail"]["rpc"]["missing_editor_workflow_cases"] == ()
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_methods_by_case"] == (
        lsp_transport_check["detail"]["rpc"]["expected_editor_workflow_methods_by_case"]
    )
    assert lsp_transport_check["detail"]["rpc"]["missing_editor_workflow_method_case_count"] == 0
    assert lsp_transport_check["detail"]["rpc"]["missing_editor_workflow_method_cases"] == ()
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_result_shapes_by_case"] == (
        lsp_transport_check["detail"]["rpc"]["expected_editor_workflow_result_shapes_by_case"]
    )
    assert lsp_transport_check["detail"]["rpc"]["missing_editor_workflow_shape_case_count"] == 0
    assert lsp_transport_check["detail"]["rpc"]["missing_editor_workflow_shape_cases"] == ()
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_diagnostic_transition_ok"] is True
    assert lsp_transport_check["detail"]["rpc"]["editor_workflow_shutdown_exit_ok"] is True
    assert set(lsp_transport_check["detail"]["rpc"]["method_contracts"]) == {
        "textDocument/didOpen",
        "textDocument/didChange",
        "textDocument/completion",
        "textDocument/hover",
        "textDocument/definition",
        "textDocument/references",
        "textDocument/documentSymbol",
        "textDocument/rename",
        "textDocument/codeAction",
        "textDocument/formatting",
        "workspace/symbol",
    }
    assert all(
        detail["advertised"] and detail["exercised"]
        for detail in lsp_transport_check["detail"]["rpc"]["method_contracts"].values()
    )
    assert lsp_transport_check["detail"]["rpc"]["blocking_gap_count"] == 0
    assert lsp_transport_check["detail"]["stdio"]["format"] == "appgen.lsp-stdio-transport-audit.v1"
    assert lsp_transport_check["detail"]["stdio"]["request_message_count"] == 4
    assert lsp_transport_check["detail"]["stdio"]["missing_response_ids"] == ()
    assert lsp_transport_check["detail"]["stdio"]["response_ids_by_method"] == lsp_transport_check["detail"]["stdio"][
        "expected_response_ids_by_method"
    ]
    assert lsp_transport_check["detail"]["stdio"]["missing_response_method_count"] == 0
    assert lsp_transport_check["detail"]["stdio"]["missing_response_methods"] == ()
    assert lsp_transport_check["detail"]["stdio"]["required_notification_methods"] == ("textDocument/publishDiagnostics",)
    assert "textDocument/publishDiagnostics" in lsp_transport_check["detail"]["stdio"]["observed_notification_methods"]
    assert lsp_transport_check["detail"]["stdio"]["missing_notification_method_count"] == 0
    assert lsp_transport_check["detail"]["stdio"]["missing_notification_methods"] == ()
    assert lsp_transport_check["detail"]["stdio"]["changed_diagnostic_code_families"]["unresolved_binding_or_table"]
    assert lsp_transport_check["detail"]["stdio"]["missing_changed_diagnostic_code_family_count"] == 0
    assert lsp_transport_check["detail"]["stdio"]["missing_changed_diagnostic_code_families"] == ()
    assert lsp_transport_check["detail"]["stdio"]["completion_response_count"] == 1
    assert lsp_transport_check["detail"]["stdio"]["workspace_symbol_response_count"] == 1
    assert lsp_transport_check["detail"]["stdio"]["shutdown_response_count"] == 1
    lsp_navigation_check = next(check for check in report["checks"] if check["id"] == "lsp_navigation_completion_contracts")
    assert lsp_navigation_check["detail"]["completion_coverage"]["format"] == "appgen.completion-coverage.v1"
    assert lsp_navigation_check["detail"]["completion_coverage"]["missing_source_count"] == 0
    assert lsp_navigation_check["detail"]["completion_coverage"]["required_source_count"] == (
        lsp_navigation_check["detail"]["completion_coverage"]["detected_source_count"]
    )
    assert lsp_navigation_check["detail"]["symbol_coverage"]["format"] == "appgen.lsp-symbol-coverage.v1"
    assert lsp_navigation_check["detail"]["symbol_coverage"]["document_missing_kind_count"] == 0
    assert lsp_navigation_check["detail"]["symbol_coverage"]["workspace_missing_kind_count"] == 0
    assert lsp_navigation_check["detail"]["reference_scope"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_navigation_check["detail"]["reference_scope"]["lexical_reference_scope_ok"] is True
    assert lsp_navigation_check["detail"]["reference_scope"]["location_count"] == 2
    assert lsp_navigation_check["detail"]["reference_scope"]["matched_line_count"] == (
        lsp_navigation_check["detail"]["reference_scope"]["expected_line_count"]
    )
    assert lsp_navigation_check["detail"]["reference_scope"]["excluded_match_count"] == 0
    assert set(lsp_navigation_check["detail"]["reference_scope"]["lines"]) == set(
        lsp_navigation_check["detail"]["reference_scope"]["expected_lines"]
    )
    assert not (
        set(lsp_navigation_check["detail"]["reference_scope"]["lines"])
        & set(lsp_navigation_check["detail"]["reference_scope"]["excluded_lines"])
    )
    assert lsp_navigation_check["detail"]["hover_depth"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_navigation_check["detail"]["hover_depth"]["required_surface_count"] == 5
    assert lsp_navigation_check["detail"]["hover_depth"]["observed_surface_count"] == (
        lsp_navigation_check["detail"]["hover_depth"]["required_surface_count"]
    )
    assert lsp_navigation_check["detail"]["hover_depth"]["missing_surface_count"] == 0
    assert lsp_navigation_check["detail"]["hover_depth"]["missing_surfaces"] == ()
    assert set(lsp_navigation_check["detail"]["hover_depth"]["required_surfaces"]) == {
        "pbc_catalog",
        "diagnostic_explanation",
        "relationship",
        "lookup",
        "handler_target",
    }
    assert set(lsp_navigation_check["detail"]["hover_depth"]["observed_surfaces"]) == set(
        lsp_navigation_check["detail"]["hover_depth"]["required_surfaces"]
    )
    assert all(lsp_navigation_check["detail"]["hover_depth"]["surface_checks"].values())
    assert lsp_navigation_check["detail"]["completion_contexts"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_navigation_check["detail"]["completion_contexts"]["context_count"] == 8
    assert lsp_navigation_check["detail"]["completion_contexts"]["passing_context_count"] == (
        lsp_navigation_check["detail"]["completion_contexts"]["context_count"]
    )
    assert lsp_navigation_check["detail"]["completion_contexts"]["missing_context_count"] == 0
    assert lsp_navigation_check["detail"]["completion_contexts"]["missing_contexts"] == ()
    assert lsp_navigation_check["detail"]["completion_contexts"]["missing_label_count"] == 0
    assert lsp_navigation_check["detail"]["completion_contexts"]["forbidden_label_count"] == 0
    assert set(lsp_navigation_check["detail"]["completion_contexts"]["context_names"]) == {
        "top_level",
        "table",
        "view",
        "flow",
        "composition",
        "deploy",
        "package",
        "agent",
    }
    assert lsp_navigation_check["detail"]["completion_contexts"]["missing_labels"] == {}
    assert lsp_navigation_check["detail"]["completion_contexts"]["forbidden_labels"] == {}
    assert all(result["ok"] for result in lsp_navigation_check["detail"]["completion_contexts"]["results"])
    assert all(
        not result["missing_labels"] for result in lsp_navigation_check["detail"]["completion_contexts"]["results"]
    )
    assert all(
        not result["forbidden_labels"] for result in lsp_navigation_check["detail"]["completion_contexts"]["results"]
    )
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["query_count"] == 2
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["passing_query_count"] == (
        lsp_navigation_check["detail"]["workspace_symbol_catalog"]["query_count"]
    )
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["missing_query_count"] == 0
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["missing_queries"] == ()
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["pbc_result_count"] >= 1
    assert lsp_navigation_check["detail"]["workspace_symbol_catalog"]["contract_result_count"] >= 1
    assert "catalog://pbc/gl_core" in lsp_navigation_check["detail"]["workspace_symbol_catalog"]["pbc_uris"]
    assert any(
        uri.startswith("catalog://pbc/gl_core/event/")
        for uri in lsp_navigation_check["detail"]["workspace_symbol_catalog"]["contract_uris"]
    )
    assert "gl_core" in lsp_navigation_check["detail"]["workspace_symbol_catalog"]["pbc_keys"]
    assert "JournalPosted" in lsp_navigation_check["detail"]["workspace_symbol_catalog"]["contract_names"]
    assert lsp_navigation_check["detail"]["definition_context"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_navigation_check["detail"]["definition_context"]["context_count"] == 5
    assert lsp_navigation_check["detail"]["definition_context"]["passing_context_count"] == (
        lsp_navigation_check["detail"]["definition_context"]["context_count"]
    )
    assert lsp_navigation_check["detail"]["definition_context"]["missing_context_count"] == 0
    assert lsp_navigation_check["detail"]["definition_context"]["missing_contexts"] == ()
    assert set(lsp_navigation_check["detail"]["definition_context"]["context_names"]) == {
        "pbc_include",
        "api_event_target",
        "deployment_health_target",
        "deployment_resource_target",
        "deployment_env_target",
    }
    assert all(lsp_navigation_check["detail"]["definition_context"]["matches"].values())
    assert lsp_navigation_check["detail"]["definition_context"]["expected_lines"] == (
        lsp_navigation_check["detail"]["definition_context"]["observed_lines"]
    )
    assert lsp_navigation_check["detail"]["catalog_references"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_navigation_check["detail"]["catalog_references"]["missing_context_count"] == 0
    assert lsp_navigation_check["detail"]["catalog_references"]["missing_contexts"] == ()
    assert lsp_navigation_check["detail"]["catalog_references"]["pbc_workspace_count"] >= 1
    assert lsp_navigation_check["detail"]["catalog_references"]["pbc_catalog_count"] >= 1
    assert lsp_navigation_check["detail"]["catalog_references"]["event_workspace_count"] >= 1
    assert lsp_navigation_check["detail"]["catalog_references"]["event_catalog_count"] >= 1
    assert all(lsp_navigation_check["detail"]["catalog_references"]["checks"].values())
    assert lsp_navigation_check["detail"]["catalog_references"]["counts"]["pbc_catalog"] >= 1
    assert lsp_navigation_check["detail"]["catalog_references"]["counts"]["event_catalog"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["format"] == "appgen.lsp-service-text-renderer.v1"
    assert lsp_navigation_check["detail"]["text_renderer"]["service_count_line_count"] == 1
    assert lsp_navigation_check["detail"]["text_renderer"]["completion_line_count"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["navigation_line_count"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["definition_line_count"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["reference_line_count"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["formatting_line_count"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["hover_line_count"] >= 1
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        "service_counts",
        "source_of_truth",
        "completion_coverage",
        "completion_missing",
        "definition",
        "references",
        "formatting",
        "rename",
        "rename_blocker",
        "hover_summary",
        "hover_content",
    )
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_editor_contract_format_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_editor_contract_formats"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["emitted_editor_contract_formats"] == (
        "appgen.lsp-service.v1",
        "appgen.semantic-model.v1",
        "appgen.completion-coverage.v1",
        "appgen.lsp-definition.v1",
        "appgen.lsp-references.v1",
        "appgen.lsp-formatting.v1",
        "appgen.lsp-rename.v1",
        "appgen.migration-plan.v1",
    )
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_navigation_surface_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_navigation_surfaces"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_completion_gap_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_completion_gaps"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_hover_item_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_hover_items"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_rename_blocker_code_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_rename_blocker_codes"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_rename_fix_id_count"] == 0
    assert lsp_navigation_check["detail"]["text_renderer"]["missing_rename_fix_ids"] == ()
    assert lsp_navigation_check["detail"]["text_renderer"]["json_fallback"] is False
    quick_fix_check = next(check for check in report["checks"] if check["id"] == "lsp_quick_fix_application")
    assert quick_fix_check["detail"]["cli"]["format"] == "appgen.lsp-code-action-cli-audit.v1"
    assert quick_fix_check["detail"]["cli"]["ok"] is True
    assert quick_fix_check["detail"]["application_audit"]["case_count"] == len(
        quick_fix_check["detail"]["application_audit"]["cases"]
    )
    assert quick_fix_check["detail"]["application_audit"]["passing_case_count"] == (
        quick_fix_check["detail"]["application_audit"]["case_count"]
    )
    assert quick_fix_check["detail"]["application_audit"]["required_action_count"] == len(
        quick_fix_check["detail"]["application_audit"]["required_action_ids"]
    )
    assert quick_fix_check["detail"]["application_audit"]["observed_action_count"] == len(
        quick_fix_check["detail"]["application_audit"]["observed_action_ids"]
    )
    assert quick_fix_check["detail"]["application_audit"]["missing_required_action_count"] == 0
    assert quick_fix_check["detail"]["application_audit"]["applied_edit_count"] >= (
        quick_fix_check["detail"]["application_audit"]["case_count"]
    )
    assert quick_fix_check["detail"]["application_audit"]["lint_passing_case_count"] == (
        quick_fix_check["detail"]["application_audit"]["case_count"]
    )
    assert quick_fix_check["detail"]["cli"]["missing_required_action_ids"] == ()
    assert quick_fix_check["detail"]["cli"]["exit_codes_by_case"] == (
        quick_fix_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert quick_fix_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert quick_fix_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert quick_fix_check["detail"]["cli"]["payload_formats_by_case"] == (
        quick_fix_check["detail"]["cli"]["expected_payload_formats_by_case"]
    )
    assert quick_fix_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert quick_fix_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert quick_fix_check["detail"]["cli"]["ok_by_case"] == {
        case_id: True for case_id in quick_fix_check["detail"]["cli"]["required_case_ids"]
    }
    assert quick_fix_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert quick_fix_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert tuple(quick_fix_check["detail"]["cli"]["required_action_ids"]) == tuple(
        quick_fix_check["detail"]["application_audit"]["required_action_ids"]
    )
    assert {
        "create_missing_table",
        "create_missing_field",
        "create_calculated_field_for_binding",
        "create_operation_from_handler",
        "create_flow_from_handler",
        "add_lookup_directive",
        "add_relationship_for_lookup_path",
        "replace_typo_with_nearest_symbol",
        "replace_secret_literal_with_env",
        "remove_invalid_runtime_picker_fields",
        "create_event_contract",
        "register_or_import_pbc_manifest",
        "add_missing_permission_for_agent_skill",
        "add_package_for_app_target",
        "create_smoke_test_declaration",
    } <= set(quick_fix_check["detail"]["cli"]["required_cli_actions"])
    assert all(case["changed"] for case in quick_fix_check["detail"]["cli"]["cases"])
    assert all(case["applied_edit_count"] > 0 for case in quick_fix_check["detail"]["cli"]["cases"])
    assert all(case["lint_format"] == "appgen.lint-report.v1" for case in quick_fix_check["detail"]["cli"]["cases"])
    assert all(case["lint_ok"] is True for case in quick_fix_check["detail"]["cli"]["cases"])
    assert all(case["forbidden_removed"] for case in quick_fix_check["detail"]["cli"]["cases"])
    quick_fix_coverage = next(check for check in report["checks"] if check["id"] == "lsp_quick_fix_coverage_contracts")
    assert quick_fix_coverage["ok"] is True
    assert quick_fix_coverage["detail"]["format"] == "appgen.lsp-code-action-apply-audit.v1"
    assert quick_fix_coverage["detail"]["required_action_count"] >= 15
    assert quick_fix_coverage["detail"]["passing_case_count"] == quick_fix_coverage["detail"]["case_count"]
    assert quick_fix_coverage["detail"]["missing_case_count"] == 0
    assert quick_fix_coverage["detail"]["missing_required_action_count"] == 0
    assert quick_fix_coverage["detail"]["applied_edit_cases"] == quick_fix_coverage["detail"]["required_case_ids"]
    assert quick_fix_coverage["detail"]["missing_applied_edit_case_count"] == 0
    assert quick_fix_coverage["detail"]["expected_text_matched_cases"] == quick_fix_coverage["detail"][
        "required_case_ids"
    ]
    assert quick_fix_coverage["detail"]["missing_expected_text_case_count"] == 0
    assert quick_fix_coverage["detail"]["lint_passing_cases"] == quick_fix_coverage["detail"]["required_case_ids"]
    assert quick_fix_coverage["detail"]["missing_lint_passing_case_count"] == 0
    assert quick_fix_coverage["detail"]["changed_cases"] == quick_fix_coverage["detail"]["required_case_ids"]
    assert quick_fix_coverage["detail"]["missing_changed_case_count"] == 0
    assert quick_fix_coverage["detail"]["cleanup_cases"] == quick_fix_coverage["detail"]["required_case_ids"]
    assert quick_fix_coverage["detail"]["missing_cleanup_case_count"] == 0
    assert quick_fix_coverage["detail"]["blocking_gap_count"] == 0
    quick_fix_cli = next(check for check in report["checks"] if check["id"] == "lsp_quick_fix_cli_contracts")
    assert quick_fix_cli["ok"] is True
    assert quick_fix_cli["detail"]["cli"]["format"] == "appgen.lsp-code-action-cli-audit.v1"
    assert tuple(quick_fix_cli["detail"]["cli"]["required_action_ids"]) == tuple(
        quick_fix_cli["detail"]["application_required_action_ids"]
    )
    assert quick_fix_cli["detail"]["cli"]["missing_required_action_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["missing_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["failing_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["failing_cases"] == ()
    assert quick_fix_cli["detail"]["cli"]["required_case_ids"] == quick_fix_cli["detail"]["cli"]["required_action_ids"]
    assert quick_fix_cli["detail"]["cli"]["observed_case_ids"] == quick_fix_cli["detail"]["cli"]["observed_action_ids"]
    assert quick_fix_cli["detail"]["cli"]["exit_codes_by_case"] == (
        quick_fix_cli["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert quick_fix_cli["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert quick_fix_cli["detail"]["cli"]["payload_formats_by_case"] == (
        quick_fix_cli["detail"]["cli"]["expected_payload_formats_by_case"]
    )
    assert quick_fix_cli["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert quick_fix_cli["detail"]["cli"]["ok_by_case"] == {
        case_id: True for case_id in quick_fix_cli["detail"]["cli"]["required_case_ids"]
    }
    assert quick_fix_cli["detail"]["cli"]["missing_ok_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["missing_ok_cases"] == ()
    assert quick_fix_cli["detail"]["cli"]["changed_case_count"] == quick_fix_cli["detail"]["cli"]["case_count"]
    assert quick_fix_cli["detail"]["cli"]["changed_cases"] == quick_fix_cli["detail"]["cli"]["required_case_ids"]
    assert quick_fix_cli["detail"]["cli"]["missing_changed_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["expected_text_case_count"] == quick_fix_cli["detail"]["cli"]["case_count"]
    assert quick_fix_cli["detail"]["cli"]["expected_text_matched_cases"] == quick_fix_cli["detail"]["cli"][
        "required_case_ids"
    ]
    assert quick_fix_cli["detail"]["cli"]["missing_expected_text_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["forbidden_removed_case_count"] == quick_fix_cli["detail"]["cli"]["case_count"]
    assert quick_fix_cli["detail"]["cli"]["forbidden_removed_cases"] == quick_fix_cli["detail"]["cli"][
        "required_case_ids"
    ]
    assert quick_fix_cli["detail"]["cli"]["missing_forbidden_removed_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["lint_format_case_count"] == quick_fix_cli["detail"]["cli"]["case_count"]
    assert quick_fix_cli["detail"]["cli"]["lint_format_cases"] == quick_fix_cli["detail"]["cli"]["required_case_ids"]
    assert quick_fix_cli["detail"]["cli"]["missing_lint_format_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["lint_passing_cases"] == quick_fix_cli["detail"]["cli"]["required_case_ids"]
    assert quick_fix_cli["detail"]["cli"]["missing_lint_passing_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["applied_edit_cases"] == quick_fix_cli["detail"]["cli"]["required_case_ids"]
    assert quick_fix_cli["detail"]["cli"]["missing_applied_edit_case_count"] == 0
    assert quick_fix_cli["detail"]["cli"]["blocking_gap_count"] == 0
    quick_fix_text = next(check for check in report["checks"] if check["id"] == "lsp_quick_fix_text_contracts")
    assert quick_fix_text["ok"] is True
    assert quick_fix_text["detail"]["format"] == "appgen.lsp-code-action-text-renderer.v1"
    assert quick_fix_text["detail"]["success_summary_line_count"] >= 1
    assert quick_fix_text["detail"]["failure_summary_line_count"] >= 1
    assert quick_fix_text["detail"]["edit_line_count"] >= 1
    assert quick_fix_text["detail"]["available_action_line_count"] >= 1
    assert quick_fix_text["detail"]["diagnostic_line_count"] >= 1
    assert quick_fix_text["detail"]["missing_text_surface_count"] == 0
    assert quick_fix_text["detail"]["missing_text_surfaces"] == ()
    assert quick_fix_text["detail"]["emitted_text_surfaces"] == (
        "success_summary",
        "failure_summary",
        "title",
        "edit",
        "available_actions",
        "diagnostic",
        "lint_status",
        "changed_status",
    )
    assert quick_fix_text["detail"]["missing_action_id_count"] == 0
    assert quick_fix_text["detail"]["missing_action_ids"] == ()
    assert quick_fix_text["detail"]["emitted_action_ids"] == (
        "create_operation_from_handler",
        "missing_action",
    )
    assert quick_fix_text["detail"]["missing_edit_snippet_count"] == 0
    assert quick_fix_text["detail"]["missing_edit_snippets"] == ()
    assert quick_fix_text["detail"]["missing_available_action_count"] == 0
    assert quick_fix_text["detail"]["missing_available_actions"] == ()
    assert quick_fix_text["detail"]["missing_diagnostic_code_count"] == 0
    assert quick_fix_text["detail"]["missing_diagnostic_codes"] == ()
    assert quick_fix_text["detail"]["missing_status_count"] == 0
    assert quick_fix_text["detail"]["missing_statuses"] == ()
    assert quick_fix_text["detail"]["json_fallback"] is False
    cli_check = next(check for check in report["checks"] if check["id"] == "cli_validation_and_generation_contracts")
    assert cli_check["detail"]["validate_generate_cli"]["format"] == "appgen.validate-generate-cli-audit.v1"
    assert cli_check["detail"]["validate_generate_cli"]["ok"] is True
    assert cli_check["detail"]["validate_generate_cli"]["observed_case_ids"] == (
        cli_check["detail"]["validate_generate_cli"]["required_case_ids"]
    )
    assert cli_check["detail"]["validate_generate_cli"]["missing_case_count"] == 0
    assert cli_check["detail"]["validate_generate_cli"]["missing_case_ids"] == ()
    assert cli_check["detail"]["validate_generate_cli"]["payload_formats_by_case"] == (
        cli_check["detail"]["validate_generate_cli"]["expected_payload_formats_by_case"]
    )
    assert cli_check["detail"]["validate_generate_cli"]["missing_payload_format_case_count"] == 0
    assert cli_check["detail"]["validate_generate_cli"]["missing_payload_format_cases"] == ()
    assert cli_check["detail"]["validate_generate_cli"]["exit_codes_by_case"] == (
        cli_check["detail"]["validate_generate_cli"]["expected_exit_codes_by_case"]
    )
    assert cli_check["detail"]["validate_generate_cli"]["missing_exit_code_case_count"] == 0
    assert cli_check["detail"]["validate_generate_cli"]["missing_exit_code_cases"] == ()
    assert cli_check["detail"]["validate_generate_cli"]["ok_by_case"] == {
        case_id: True for case_id in cli_check["detail"]["validate_generate_cli"]["required_case_ids"]
    }
    assert cli_check["detail"]["validate_generate_cli"]["missing_ok_case_count"] == 0
    assert cli_check["detail"]["validate_generate_cli"]["missing_ok_cases"] == ()
    assert {
        "validate_targets",
        "validate_rejects_undeclared_targets",
        "validate_rejects_unknown_targets",
        "generate_writes_artifacts",
        "generate_blocks_warnings",
        "generate_allows_warnings_when_requested",
        "generate_blocks_errors_even_when_warnings_allowed",
    } <= {case["case"] for case in cli_check["detail"]["validate_generate_cli"]["cases"]}
    validate_cases = {case["case"]: case for case in cli_check["detail"]["validate_generate_cli"]["cases"]}
    assert validate_cases["validate_rejects_undeclared_targets"]["exit_code"] == 1
    assert validate_cases["validate_rejects_undeclared_targets"]["requested_targets"] == ("web", "mobile")
    assert validate_cases["validate_rejects_undeclared_targets"]["app_targets"] == ("web",)
    assert "AGX0802" in validate_cases["validate_rejects_undeclared_targets"]["diagnostic_codes"]
    assert validate_cases["validate_rejects_unknown_targets"]["exit_code"] == 1
    assert "AGX0802" in validate_cases["validate_rejects_unknown_targets"]["diagnostic_codes"]
    assert validate_cases["generate_blocks_errors_even_when_warnings_allowed"]["exit_code"] == 1
    assert validate_cases["generate_blocks_errors_even_when_warnings_allowed"]["allow_warnings"] is True
    assert "lint_errors" in validate_cases["generate_blocks_errors_even_when_warnings_allowed"]["blocking_gaps"]
    assert validate_cases["generate_blocks_errors_even_when_warnings_allowed"]["output_exists"] is False
    assert validate_cases["generate_writes_artifacts"]["targets"] == ("web",)
    assert validate_cases["generate_writes_artifacts"]["semantic_model_format"] == "appgen.semantic-model.v1"
    assert validate_cases["generate_writes_artifacts"]["validation_format"] == "appgen.validate-report.v1"
    assert validate_cases["generate_writes_artifacts"]["artifact_count"] > 0
    assert validate_cases["generate_writes_artifacts"]["artifact_paths_exist"] is True
    assert validate_cases["generate_writes_artifacts"]["manifest_exists"] is True
    assert validate_cases["generate_writes_artifacts"]["manifest_app_name"] == "ToolingAudit"
    validate_target_check = next(check for check in report["checks"] if check["id"] == "validate_target_contracts")
    assert validate_target_check["detail"]["validate"] == "appgen.validate-report.v1"
    assert validate_target_check["detail"]["cli"]["format"] == "appgen.validate-generate-cli-audit.v1"
    assert validate_target_check["detail"]["cli"]["validation_case_count"] == 3
    assert validate_target_check["detail"]["cli"]["validation_rejection_case_count"] == 2
    assert validate_target_check["detail"]["cli"]["observed_case_ids"] == (
        validate_target_check["detail"]["cli"]["required_case_ids"]
    )
    assert validate_target_check["detail"]["cli"]["missing_case_count"] == 0
    assert validate_target_check["detail"]["cli"]["missing_case_ids"] == ()
    assert validate_target_check["detail"]["cli"]["payload_formats_by_case"] == (
        validate_target_check["detail"]["cli"]["expected_payload_formats_by_case"]
    )
    assert validate_target_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert validate_target_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert validate_target_check["detail"]["cli"]["exit_codes_by_case"] == (
        validate_target_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert validate_target_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert validate_target_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert validate_target_check["detail"]["cli"]["ok_by_case"] == {
        case_id: True for case_id in validate_target_check["detail"]["cli"]["required_case_ids"]
    }
    assert validate_target_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert validate_target_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert set(validate_target_check["detail"]["cli"]["validation_rejection_cases"]) == {
        "validate_rejects_undeclared_targets",
        "validate_rejects_unknown_targets",
    }
    assert validate_target_check["detail"]["text_renderer"]["format"] == "appgen.validate-generate-text-renderer.v1"
    assert validate_target_check["detail"]["text_renderer"]["summary_line_count"] == 2
    assert validate_target_check["detail"]["text_renderer"]["check_line_count"] == 2
    assert validate_target_check["detail"]["text_renderer"]["passing_check_line_count"] == 1
    assert validate_target_check["detail"]["text_renderer"]["failing_check_line_count"] == 1
    assert validate_target_check["detail"]["text_renderer"]["target_detail_line_count"] == 2
    assert validate_target_check["detail"]["text_renderer"]["error_line_count"] == 1
    assert validate_target_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        validate_target_check["detail"]["text_renderer"]["required_text_surfaces"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_contract_formats"] == (
        validate_target_check["detail"]["text_renderer"]["required_contract_formats"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_semantic_formats"] == (
        validate_target_check["detail"]["text_renderer"]["required_semantic_formats"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_semantic_format_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_semantic_formats"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_validate_statuses"] == (
        validate_target_check["detail"]["text_renderer"]["required_validate_statuses"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_validate_status_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_validate_statuses"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_requested_targets"] == (
        validate_target_check["detail"]["text_renderer"]["required_requested_targets"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_requested_target_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_requested_targets"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_app_targets"] == (
        validate_target_check["detail"]["text_renderer"]["required_app_targets"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_app_target_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_app_targets"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_check_ids"] == (
        validate_target_check["detail"]["text_renderer"]["required_check_ids"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_check_id_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_check_ids"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_passing_check_ids"] == (
        validate_target_check["detail"]["text_renderer"]["required_passing_check_ids"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_passing_check_id_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_passing_check_ids"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_failing_check_ids"] == (
        validate_target_check["detail"]["text_renderer"]["required_failing_check_ids"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_failing_check_id_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_failing_check_ids"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_unknown_targets"] == (
        validate_target_check["detail"]["text_renderer"]["required_unknown_targets"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_unknown_target_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_unknown_targets"] == ()
    assert validate_target_check["detail"]["text_renderer"]["emitted_missing_targets"] == (
        validate_target_check["detail"]["text_renderer"]["required_missing_targets"]
    )
    assert validate_target_check["detail"]["text_renderer"]["missing_missing_target_count"] == 0
    assert validate_target_check["detail"]["text_renderer"]["missing_missing_targets"] == ()
    assert validate_target_check["detail"]["text_renderer"]["json_fallback"] is False
    generate_policy_check = next(check for check in report["checks"] if check["id"] == "generate_artifact_policy_contracts")
    assert generate_policy_check["detail"]["generate"]["format"] == "appgen.generate-report.v1"
    assert generate_policy_check["detail"]["generate"]["generated"] is True
    assert generate_policy_check["detail"]["generate"]["artifact_count"] > 0
    assert generate_policy_check["detail"]["generate"]["manifest_exists"] is True
    assert generate_policy_check["detail"]["cli"]["format"] == "appgen.validate-generate-cli-audit.v1"
    assert generate_policy_check["detail"]["cli"]["observed_case_ids"] == (
        generate_policy_check["detail"]["cli"]["required_case_ids"]
    )
    assert generate_policy_check["detail"]["cli"]["missing_case_count"] == 0
    assert generate_policy_check["detail"]["cli"]["missing_case_ids"] == ()
    assert generate_policy_check["detail"]["cli"]["generated_case_count"] == 4
    assert generate_policy_check["detail"]["cli"]["generated_success_case_count"] == 2
    assert set(generate_policy_check["detail"]["cli"]["generated_success_cases"]) == {
        "generate_writes_artifacts",
        "generate_allows_warnings_when_requested",
    }
    assert generate_policy_check["detail"]["cli"]["generated_blocked_case_count"] == 2
    assert set(generate_policy_check["detail"]["cli"]["generated_blocked_cases"]) == {
        "generate_blocks_warnings",
        "generate_blocks_errors_even_when_warnings_allowed",
    }
    assert generate_policy_check["detail"]["cli"]["manifest_case_count"] >= 2
    assert generate_policy_check["detail"]["cli"]["manifest_existing_case_count"] >= 2
    assert generate_policy_check["detail"]["cli"]["artifact_handoff_case_count"] >= 1
    assert generate_policy_check["detail"]["cli"]["artifact_path_case_count"] >= 1
    assert generate_policy_check["detail"]["cli"]["artifact_path_missing_case_count"] == 0
    assert generate_policy_check["detail"]["cli"]["blocking_gap_case_count"] >= 2
    assert generate_policy_check["detail"]["cli"]["generated_blocked_output_absent_case_count"] >= 1
    assert "generate_blocks_errors_even_when_warnings_allowed" in (
        generate_policy_check["detail"]["cli"]["generated_blocked_output_absent_cases"]
    )
    assert {"lint_warnings", "lint_errors"} <= set(generate_policy_check["detail"]["cli"]["generated_blocking_gap_names"])
    assert generate_policy_check["detail"]["cli"]["payload_formats_by_case"] == (
        generate_policy_check["detail"]["cli"]["expected_payload_formats_by_case"]
    )
    assert generate_policy_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert generate_policy_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert generate_policy_check["detail"]["cli"]["exit_codes_by_case"] == (
        generate_policy_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert generate_policy_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert generate_policy_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert generate_policy_check["detail"]["cli"]["ok_by_case"] == {
        case_id: True for case_id in generate_policy_check["detail"]["cli"]["required_case_ids"]
    }
    assert generate_policy_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert generate_policy_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert generate_policy_check["detail"]["cli"]["payload_format_count"] == len(
        generate_policy_check["detail"]["cli"]["payload_formats"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["format"] == "appgen.validate-generate-text-renderer.v1"
    assert generate_policy_check["detail"]["text_renderer"]["artifact_line_count"] >= 1
    assert generate_policy_check["detail"]["text_renderer"]["manifest_line_count"] >= 1
    assert generate_policy_check["detail"]["text_renderer"]["gap_line_count"] >= 1
    assert generate_policy_check["detail"]["text_renderer"]["warning_line_count"] >= 1
    assert generate_policy_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        generate_policy_check["detail"]["text_renderer"]["required_text_surfaces"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_contract_formats"] == (
        generate_policy_check["detail"]["text_renderer"]["required_contract_formats"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_semantic_formats"] == (
        generate_policy_check["detail"]["text_renderer"]["required_semantic_formats"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_semantic_format_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_semantic_formats"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_generate_statuses"] == (
        generate_policy_check["detail"]["text_renderer"]["required_generate_statuses"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_generate_status_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_generate_statuses"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_generated_values"] == (
        generate_policy_check["detail"]["text_renderer"]["required_generated_values"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_generated_value_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_generated_values"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_output_dirs"] == (
        generate_policy_check["detail"]["text_renderer"]["required_output_dirs"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_output_dir_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_output_dirs"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_artifact_sizes"] == (
        generate_policy_check["detail"]["text_renderer"]["required_artifact_sizes"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_artifact_size_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_artifact_sizes"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_generate_targets"] == (
        generate_policy_check["detail"]["text_renderer"]["required_generate_targets"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_generate_target_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_generate_targets"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_artifact_paths"] == (
        generate_policy_check["detail"]["text_renderer"]["required_artifact_paths"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_artifact_path_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_artifact_paths"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_manifest_paths"] == (
        generate_policy_check["detail"]["text_renderer"]["required_manifest_paths"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_manifest_path_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_manifest_paths"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_gap_ids"] == (
        generate_policy_check["detail"]["text_renderer"]["required_gap_ids"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_gap_id_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_gap_ids"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_diagnostic_codes"] == (
        generate_policy_check["detail"]["text_renderer"]["required_diagnostic_codes"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_diagnostic_code_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_diagnostic_codes"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["emitted_diagnostic_severities"] == (
        generate_policy_check["detail"]["text_renderer"]["required_diagnostic_severities"]
    )
    assert generate_policy_check["detail"]["text_renderer"]["missing_diagnostic_severity_count"] == 0
    assert generate_policy_check["detail"]["text_renderer"]["missing_diagnostic_severities"] == ()
    assert generate_policy_check["detail"]["text_renderer"]["json_fallback"] is False
    assert cli_check["detail"]["format_write"]["format"] == "appgen.format-write-audit.v1"
    assert cli_check["detail"]["format_write"]["ok"] is True
    assert cli_check["detail"]["format_write"]["scenario_count"] == 5
    assert cli_check["detail"]["format_write"]["passing_scenario_count"] == 5
    assert cli_check["detail"]["format_write"]["write_mode_count"] == 2
    assert cli_check["detail"]["format_write"]["check_mode_count"] == 2
    assert cli_check["detail"]["format_write"]["organize_category_count"] == 7
    assert cli_check["detail"]["format_write"]["check_exit_code"] == 1
    assert cli_check["detail"]["format_write"]["check_changed"] is True
    assert cli_check["detail"]["format_write"]["check_write_requested"] is False
    assert cli_check["detail"]["format_write"]["check_written"] is False
    assert cli_check["detail"]["format_write"]["text_exit_code"] == 0
    assert cli_check["detail"]["format_write"]["text_has_report_format"] is True
    assert cli_check["detail"]["format_write"]["text_has_write_metadata"] is True
    assert cli_check["detail"]["format_write"]["clean_check_exit_code"] == 0
    assert cli_check["detail"]["format_write"]["clean_check_changed"] is False
    assert cli_check["detail"]["format_write"]["organize_exit_code"] == 0
    assert cli_check["detail"]["format_write"]["organize"] is True
    assert cli_check["detail"]["format_write"]["organize_idempotent"] is True
    assert cli_check["detail"]["format_write"]["organize_order"] == tuple(
        sorted(cli_check["detail"]["format_write"]["organize_order"])
    )
    formatter_gate = next(check for check in report["checks"] if check["id"] == "formatter_write_organize_contracts")
    assert formatter_gate["detail"]["formatted"]["format"] == "appgen.format-result.v1"
    assert formatter_gate["detail"]["formatted"]["idempotent"] is True
    assert formatter_gate["detail"]["formatter_contract"]["format"] == "appgen.formatter-contract-audit.v1"
    assert formatter_gate["detail"]["formatter_contract"]["passing_check_count"] == (
        formatter_gate["detail"]["formatter_contract"]["check_count"]
    )
    assert formatter_gate["detail"]["formatter_contract"]["failed_check_count"] == 0
    assert formatter_gate["detail"]["formatter_contract"]["diagnostic_error_count"] == 0
    assert formatter_gate["detail"]["formatter_contract"]["blocking_gaps"] == ()
    assert formatter_gate["detail"]["format_write"]["format"] == "appgen.format-write-audit.v1"
    assert formatter_gate["detail"]["format_write"]["passing_scenario_count"] == (
        formatter_gate["detail"]["format_write"]["scenario_count"]
    )
    assert formatter_gate["detail"]["format_write"]["failing_scenario_count"] == 0
    assert formatter_gate["detail"]["format_write"]["blocking_gap_count"] == 0
    assert formatter_gate["detail"]["format_write"]["write_mode_count"] == 2
    assert formatter_gate["detail"]["format_write"]["check_mode_count"] == 2
    assert formatter_gate["detail"]["format_write"]["organize_category_count"] == 7
    assert formatter_gate["detail"]["format_write"]["text_has_report_format"] is True
    assert formatter_gate["detail"]["format_write"]["text_has_write_metadata"] is True
    assert formatter_gate["detail"]["text_renderer"]["format"] == "appgen.format-text-renderer.v1"
    assert formatter_gate["detail"]["text_renderer"]["summary_line_count"] == 1
    assert formatter_gate["detail"]["text_renderer"]["write_path_line_count"] == 1
    assert formatter_gate["detail"]["text_renderer"]["write_flag_line_count"] == 1
    assert formatter_gate["detail"]["text_renderer"]["idempotence_line_count"] == 1
    assert formatter_gate["detail"]["text_renderer"]["organize_line_count"] == 1
    assert formatter_gate["detail"]["text_renderer"]["emitted_text_surfaces"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_text_surfaces"]
    assert formatter_gate["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_contract_formats"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_contract_formats"]
    assert formatter_gate["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_mutation_states"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_mutation_states"]
    assert formatter_gate["detail"]["text_renderer"]["missing_mutation_state_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_mutation_states"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_write_paths"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_write_paths"]
    assert formatter_gate["detail"]["text_renderer"]["missing_write_path_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_write_paths"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_write_requested_values"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_write_requested_values"]
    assert formatter_gate["detail"]["text_renderer"]["missing_write_requested_value_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_write_requested_values"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_written_values"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_written_values"]
    assert formatter_gate["detail"]["text_renderer"]["missing_written_value_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_written_values"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_organize_values"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_organize_values"]
    assert formatter_gate["detail"]["text_renderer"]["missing_organize_value_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_organize_values"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_idempotence_states"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_idempotence_states"]
    assert formatter_gate["detail"]["text_renderer"]["missing_idempotence_state_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_idempotence_states"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_diagnostic_codes"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_diagnostic_codes"]
    assert formatter_gate["detail"]["text_renderer"]["missing_diagnostic_code_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_diagnostic_codes"] == ()
    assert formatter_gate["detail"]["text_renderer"]["emitted_diagnostic_severities"] == formatter_gate["detail"][
        "text_renderer"
    ]["required_diagnostic_severities"]
    assert formatter_gate["detail"]["text_renderer"]["missing_diagnostic_severity_count"] == 0
    assert formatter_gate["detail"]["text_renderer"]["missing_diagnostic_severities"] == ()
    assert formatter_gate["detail"]["text_renderer"]["json_fallback"] is False
    assert cli_check["detail"]["internal_error_exit"]["format"] == "appgen.internal-error-exit-audit.v1"
    assert cli_check["detail"]["internal_error_exit"]["ok"] is True
    assert cli_check["detail"]["internal_error_exit"]["mode_count"] == 2
    assert cli_check["detail"]["internal_error_exit"]["passing_mode_count"] == 2
    assert cli_check["detail"]["internal_error_exit"]["traceback_free_mode_count"] == 2
    assert cli_check["detail"]["internal_error_exit"]["json_exit_code"] == 3
    assert cli_check["detail"]["internal_error_exit"]["text_exit_code"] == 3
    assert cli_check["detail"]["internal_error_exit"]["json_traceback_free"] is True
    assert cli_check["detail"]["internal_error_exit"]["text_traceback_free"] is True
    cli_usage_check = next(check for check in report["checks"] if check["id"] == "cli_usage_failure_contracts")
    assert cli_usage_check["detail"]["internal_error_exit"]["format"] == "appgen.internal-error-exit-audit.v1"
    assert cli_usage_check["detail"]["internal_error_exit"]["passing_mode_count"] == 2
    assert cli_usage_check["detail"]["internal_error_exit"]["traceback_free_mode_count"] == 2
    assert cli_usage_check["detail"]["missing_input_exit"]["format"] == "appgen.missing-input-exit-audit.v1"
    assert cli_usage_check["detail"]["missing_input_exit"]["failing_case_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["missing_case_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["missing_case_ids"] == ()
    assert cli_usage_check["detail"]["missing_input_exit"]["missing_command_family_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["missing_command_families"] == ()
    assert cli_usage_check["detail"]["missing_input_exit"]["missing_path_message_missing_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["missing_path_message_missing_cases"] == ()
    assert cli_usage_check["detail"]["missing_input_exit"]["stdout_empty_count"] == (
        cli_usage_check["detail"]["missing_input_exit"]["case_count"]
    )
    assert cli_usage_check["detail"]["missing_input_exit"]["stdout_non_empty_case_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["stdout_non_empty_cases"] == ()
    assert cli_usage_check["detail"]["missing_input_exit"]["traceback_case_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["traceback_cases"] == ()
    assert cli_usage_check["detail"]["missing_input_exit"]["expected_exit_code"] == 2
    assert cli_usage_check["detail"]["missing_input_exit"]["unexpected_exit_code_case_count"] == 0
    assert cli_usage_check["detail"]["missing_input_exit"]["unexpected_exit_code_cases"] == ()
    assert cli_usage_check["detail"]["missing_required_option_exit"]["format"] == (
        "appgen.missing-required-option-exit-audit.v1"
    )
    assert cli_usage_check["detail"]["missing_required_option_exit"]["failing_case_count"] == 0
    assert cli_usage_check["detail"]["missing_required_option_exit"]["missing_case_count"] == 0
    assert cli_usage_check["detail"]["missing_required_option_exit"]["missing_case_ids"] == ()
    assert cli_usage_check["detail"]["missing_required_option_exit"]["missing_expected_message_count"] == 0
    assert cli_usage_check["detail"]["missing_required_option_exit"]["missing_expected_message_cases"] == ()
    assert cli_usage_check["detail"]["missing_required_option_exit"]["stdout_empty_count"] == (
        cli_usage_check["detail"]["missing_required_option_exit"]["case_count"]
    )
    assert cli_usage_check["detail"]["missing_required_option_exit"]["stdout_non_empty_case_count"] == 0
    assert cli_usage_check["detail"]["missing_required_option_exit"]["stdout_non_empty_cases"] == ()
    assert cli_usage_check["detail"]["missing_required_option_exit"]["traceback_case_count"] == 0
    assert cli_usage_check["detail"]["missing_required_option_exit"]["traceback_cases"] == ()
    assert cli_usage_check["detail"]["missing_required_option_exit"]["expected_exit_code"] == 2
    assert cli_usage_check["detail"]["missing_required_option_exit"]["unexpected_exit_code_case_count"] == 0
    assert cli_usage_check["detail"]["missing_required_option_exit"]["unexpected_exit_code_cases"] == ()
    assert cli_usage_check["detail"]["invalid_choice_exit"]["format"] == "appgen.invalid-choice-exit-audit.v1"
    assert cli_usage_check["detail"]["invalid_choice_exit"]["failing_case_count"] == 0
    assert cli_usage_check["detail"]["invalid_choice_exit"]["missing_case_count"] == 0
    assert cli_usage_check["detail"]["invalid_choice_exit"]["missing_case_ids"] == ()
    assert cli_usage_check["detail"]["invalid_choice_exit"]["invalid_choice_message_count"] == (
        cli_usage_check["detail"]["invalid_choice_exit"]["case_count"]
    )
    assert cli_usage_check["detail"]["invalid_choice_exit"]["missing_invalid_choice_message_count"] == 0
    assert cli_usage_check["detail"]["invalid_choice_exit"]["missing_invalid_choice_message_cases"] == ()
    assert cli_usage_check["detail"]["invalid_choice_exit"]["stdout_empty_count"] == (
        cli_usage_check["detail"]["invalid_choice_exit"]["case_count"]
    )
    assert cli_usage_check["detail"]["invalid_choice_exit"]["stdout_non_empty_case_count"] == 0
    assert cli_usage_check["detail"]["invalid_choice_exit"]["stdout_non_empty_cases"] == ()
    assert cli_usage_check["detail"]["invalid_choice_exit"]["traceback_case_count"] == 0
    assert cli_usage_check["detail"]["invalid_choice_exit"]["traceback_cases"] == ()
    assert cli_usage_check["detail"]["invalid_choice_exit"]["expected_exit_code"] == 2
    assert cli_usage_check["detail"]["invalid_choice_exit"]["unexpected_exit_code_case_count"] == 0
    assert cli_usage_check["detail"]["invalid_choice_exit"]["unexpected_exit_code_cases"] == ()
    assert cli_usage_check["detail"]["cli_help_surface"]["format"] == "appgen.cli-help-surface-audit.v1"
    assert cli_usage_check["detail"]["cli_help_surface"]["documented_missing_subcommands"] == ()
    assert cli_usage_check["detail"]["cli_help_surface"]["help_missing_subcommands"] == ()
    assert cli_usage_check["detail"]["cli_help_surface"]["listed_subcommand_count"] == (
        cli_usage_check["detail"]["cli_help_surface"]["help_listed_subcommand_count"]
    )
    assert cli_usage_check["detail"]["cli_help_surface"]["failing_option_surface_count"] == 0
    assert cli_usage_check["detail"]["cli_help_surface"]["missing_option_count"] == 0
    cli_help_gate = next(check for check in report["checks"] if check["id"] == "cli_help_alias_contracts")
    assert cli_help_gate["ok"] is True
    assert cli_help_gate["detail"]["format"] == "appgen.cli-help-surface-audit.v1"
    assert cli_help_gate["detail"]["help_exit_code"] == 0
    assert cli_help_gate["detail"]["listed_subcommand_count"] == (
        cli_help_gate["detail"]["required_subcommand_count"]
    )
    assert cli_help_gate["detail"]["documented_missing_subcommand_count"] == 0
    assert cli_help_gate["detail"]["help_missing_subcommand_count"] == 0
    assert cli_help_gate["detail"]["passing_option_surface_count"] == (
        cli_help_gate["detail"]["subcommand_option_surface_count"]
    )
    assert cli_help_gate["detail"]["failing_option_surface_count"] == 0
    assert cli_help_gate["detail"]["option_help_exit_failure_count"] == 0
    assert cli_help_gate["detail"]["missing_option_count"] == 0
    assert cli_help_gate["detail"]["command_alias_count"] == 2
    assert cli_help_gate["detail"]["entrypoint_dispatch_count"] == 2
    assert cli_help_gate["detail"]["failing_entrypoint_dispatch_count"] == 0
    assert cli_help_gate["detail"]["required_entrypoint_ids"] == ("python_module", "repo_alias")
    assert cli_help_gate["detail"]["observed_entrypoint_ids"] == cli_help_gate["detail"]["required_entrypoint_ids"]
    assert cli_help_gate["detail"]["missing_entrypoint_ids"] == ()
    assert cli_help_gate["detail"]["missing_entrypoint_id_count"] == 0
    assert cli_help_gate["detail"]["entrypoint_dispatch_ok_by_id"] == {"python_module": True, "repo_alias": True}
    assert cli_help_gate["detail"]["missing_entrypoint_dispatch_ids"] == ()
    assert cli_help_gate["detail"]["missing_entrypoint_dispatch_count"] == 0
    assert cli_help_gate["detail"]["entrypoint_exit_codes_by_id"] == (
        cli_help_gate["detail"]["expected_entrypoint_exit_codes_by_id"]
    )
    assert cli_help_gate["detail"]["missing_entrypoint_exit_code_ids"] == ()
    assert cli_help_gate["detail"]["missing_entrypoint_exit_code_count"] == 0
    assert cli_help_gate["detail"]["entrypoint_payload_formats_by_id"] == (
        cli_help_gate["detail"]["expected_entrypoint_payload_formats_by_id"]
    )
    assert cli_help_gate["detail"]["missing_entrypoint_payload_format_ids"] == ()
    assert cli_help_gate["detail"]["missing_entrypoint_payload_format_count"] == 0
    assert cli_help_gate["detail"]["entrypoint_traceback_free_by_id"] == {"python_module": True, "repo_alias": True}
    assert cli_help_gate["detail"]["missing_entrypoint_traceback_free_ids"] == ()
    assert cli_help_gate["detail"]["missing_entrypoint_traceback_free_count"] == 0
    assert cli_help_gate["detail"]["alias_contract"]["format"] == "appgen.cli-alias-contract.v1"
    assert cli_help_gate["detail"]["alias_contract"]["shared_target"] == "pyAppGen.__main__:main"
    assert cli_help_gate["detail"]["module_entrypoint"]["ok"] is True
    assert cli_help_gate["detail"]["repo_alias_command"]["ok"] is True
    assert cli_check["detail"]["missing_input_exit"]["format"] == "appgen.missing-input-exit-audit.v1"
    assert cli_check["detail"]["missing_input_exit"]["ok"] is True
    assert cli_check["detail"]["missing_input_exit"]["case_count"] == len(
        cli_check["detail"]["missing_input_exit"]["cases"]
    )
    assert cli_check["detail"]["missing_input_exit"]["passing_case_count"] == (
        cli_check["detail"]["missing_input_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_input_exit"]["failing_case_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["failing_cases"] == ()
    assert cli_check["detail"]["missing_input_exit"]["observed_case_ids"] == (
        cli_check["detail"]["missing_input_exit"]["required_case_ids"]
    )
    assert cli_check["detail"]["missing_input_exit"]["missing_case_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["missing_case_ids"] == ()
    assert cli_check["detail"]["missing_input_exit"]["case_ids"] == tuple(
        case["name"] for case in cli_check["detail"]["missing_input_exit"]["cases"]
    )
    assert cli_check["detail"]["missing_input_exit"]["command_family_count"] >= 14
    assert set(cli_check["detail"]["missing_input_exit"]["required_command_families"]) <= set(
        cli_check["detail"]["missing_input_exit"]["command_families"]
    )
    assert cli_check["detail"]["missing_input_exit"]["missing_command_family_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["missing_command_families"] == ()
    assert cli_check["detail"]["missing_input_exit"]["missing_path_message_count"] == (
        cli_check["detail"]["missing_input_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_input_exit"]["stdout_empty_count"] == (
        cli_check["detail"]["missing_input_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_input_exit"]["traceback_free_count"] == (
        cli_check["detail"]["missing_input_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_input_exit"]["stdout_non_empty_case_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["stdout_non_empty_cases"] == ()
    assert cli_check["detail"]["missing_input_exit"]["traceback_case_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["traceback_cases"] == ()
    assert cli_check["detail"]["missing_input_exit"]["expected_exit_code"] == 2
    assert cli_check["detail"]["missing_input_exit"]["unexpected_exit_code_case_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["unexpected_exit_code_cases"] == ()
    assert cli_check["detail"]["missing_input_exit"]["missing_path_message_missing_count"] == 0
    assert cli_check["detail"]["missing_input_exit"]["missing_path_message_missing_cases"] == ()
    assert cli_check["detail"]["missing_required_option_exit"]["format"] == (
        "appgen.missing-required-option-exit-audit.v1"
    )
    assert cli_check["detail"]["missing_required_option_exit"]["ok"] is True
    assert cli_check["detail"]["missing_required_option_exit"]["case_count"] == len(
        cli_check["detail"]["missing_required_option_exit"]["cases"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["passing_case_count"] == (
        cli_check["detail"]["missing_required_option_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["failing_case_count"] == 0
    assert cli_check["detail"]["missing_required_option_exit"]["failing_cases"] == ()
    assert cli_check["detail"]["missing_required_option_exit"]["observed_case_ids"] == (
        cli_check["detail"]["missing_required_option_exit"]["required_case_ids"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["missing_case_count"] == 0
    assert cli_check["detail"]["missing_required_option_exit"]["missing_case_ids"] == ()
    assert cli_check["detail"]["missing_required_option_exit"]["case_ids"] == tuple(
        case["name"] for case in cli_check["detail"]["missing_required_option_exit"]["cases"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["expected_message_count"] == (
        cli_check["detail"]["missing_required_option_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["stdout_empty_count"] == (
        cli_check["detail"]["missing_required_option_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["traceback_free_count"] == (
        cli_check["detail"]["missing_required_option_exit"]["case_count"]
    )
    assert cli_check["detail"]["missing_required_option_exit"]["stdout_non_empty_case_count"] == 0
    assert cli_check["detail"]["missing_required_option_exit"]["stdout_non_empty_cases"] == ()
    assert cli_check["detail"]["missing_required_option_exit"]["traceback_case_count"] == 0
    assert cli_check["detail"]["missing_required_option_exit"]["traceback_cases"] == ()
    assert cli_check["detail"]["missing_required_option_exit"]["expected_exit_code"] == 2
    assert cli_check["detail"]["missing_required_option_exit"]["unexpected_exit_code_case_count"] == 0
    assert cli_check["detail"]["missing_required_option_exit"]["unexpected_exit_code_cases"] == ()
    assert cli_check["detail"]["missing_required_option_exit"]["missing_expected_message_count"] == 0
    assert cli_check["detail"]["missing_required_option_exit"]["missing_expected_message_cases"] == ()
    assert {
        "generate_missing_out",
        "nl_plan_missing_prompt",
        "component_publish_missing_component",
    } <= {case["name"] for case in cli_check["detail"]["missing_required_option_exit"]["cases"]}
    assert {
        "lint_backend",
        "graph_kind",
        "graph_format",
        "migration_backend",
        "nl_backend",
        "verify_target",
        "package_target",
        "pbc_publish_catalog",
    } <= {case["name"] for case in cli_check["detail"]["invalid_choice_exit"]["cases"]}
    assert cli_check["detail"]["invalid_choice_exit"]["case_count"] == len(
        cli_check["detail"]["invalid_choice_exit"]["cases"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["passing_case_count"] == (
        cli_check["detail"]["invalid_choice_exit"]["case_count"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["failing_case_count"] == 0
    assert cli_check["detail"]["invalid_choice_exit"]["failing_cases"] == ()
    assert cli_check["detail"]["invalid_choice_exit"]["observed_case_ids"] == (
        cli_check["detail"]["invalid_choice_exit"]["required_case_ids"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["missing_case_count"] == 0
    assert cli_check["detail"]["invalid_choice_exit"]["missing_case_ids"] == ()
    assert cli_check["detail"]["invalid_choice_exit"]["case_ids"] == tuple(
        case["name"] for case in cli_check["detail"]["invalid_choice_exit"]["cases"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["invalid_choice_message_count"] == (
        cli_check["detail"]["invalid_choice_exit"]["case_count"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["stdout_empty_count"] == (
        cli_check["detail"]["invalid_choice_exit"]["case_count"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["traceback_free_count"] == (
        cli_check["detail"]["invalid_choice_exit"]["case_count"]
    )
    assert cli_check["detail"]["invalid_choice_exit"]["stdout_non_empty_case_count"] == 0
    assert cli_check["detail"]["invalid_choice_exit"]["stdout_non_empty_cases"] == ()
    assert cli_check["detail"]["invalid_choice_exit"]["traceback_case_count"] == 0
    assert cli_check["detail"]["invalid_choice_exit"]["traceback_cases"] == ()
    assert cli_check["detail"]["invalid_choice_exit"]["expected_exit_code"] == 2
    assert cli_check["detail"]["invalid_choice_exit"]["unexpected_exit_code_case_count"] == 0
    assert cli_check["detail"]["invalid_choice_exit"]["unexpected_exit_code_cases"] == ()
    assert cli_check["detail"]["invalid_choice_exit"]["missing_invalid_choice_message_count"] == 0
    assert cli_check["detail"]["invalid_choice_exit"]["missing_invalid_choice_message_cases"] == ()
    diagnostic_contract_check = next(
        check for check in report["checks"] if check["id"] == "diagnostic_catalog_fixture_contracts"
    )
    assert diagnostic_contract_check["detail"]["catalog_format"] == "appgen.diagnostic-catalog.v1"
    assert diagnostic_contract_check["detail"]["fixture_format"] == "appgen.diagnostic-fixture-audit.v1"
    assert diagnostic_contract_check["detail"]["required_code_count"] == (
        diagnostic_contract_check["detail"]["covered_fixture_code_count"]
    )
    assert diagnostic_contract_check["detail"]["missing_fixture_count"] == 0
    assert diagnostic_contract_check["detail"]["catalog_shape_gap_count"] == 0
    assert diagnostic_contract_check["detail"]["diagnostic_shape_field_count"] >= 8
    assert diagnostic_contract_check["detail"]["catalog_field_count"] >= 7
    assert diagnostic_contract_check["detail"]["passing_fixture_count"] == diagnostic_contract_check["detail"]["fixture_count"]
    assert diagnostic_contract_check["detail"]["missing_code_count"] == 0
    assert diagnostic_contract_check["detail"]["blocking_gap_count"] == 0
    assert diagnostic_contract_check["detail"]["shape_gap_count"] == 0
    assert diagnostic_contract_check["detail"]["severity_gap_count"] == 0
    assert diagnostic_contract_check["detail"]["report_format_count"] >= 4
    assert diagnostic_contract_check["detail"]["docs_urls"]
    assert diagnostic_contract_check["detail"]["text_renderer"]["format"] == "appgen.diagnostics-text-renderer.v1"
    assert diagnostic_contract_check["detail"]["text_renderer"]["summary_line_count"] == 2
    assert diagnostic_contract_check["detail"]["text_renderer"]["required_code_line_count"] >= 3
    assert diagnostic_contract_check["detail"]["text_renderer"]["covered_fixture_line_count"] >= 3
    assert diagnostic_contract_check["detail"]["text_renderer"]["covered_code_line_count"] >= 2
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_code_line_count"] >= 1
    assert diagnostic_contract_check["detail"]["text_renderer"]["blocking_gap_line_count"] >= 1
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_required_codes"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_codes"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_required_code_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_required_codes"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_covered_fixture_codes"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_covered_fixture_codes"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_covered_fixture_code_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_covered_fixture_codes"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_covered_codes"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_covered_codes"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_covered_code_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_covered_codes"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_missing_codes"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_missing_codes"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_missing_code_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_missing_codes"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_blocking_gap_ids"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_blocking_gap_ids"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_blocking_gap_id_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_blocking_gap_ids"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_text_surfaces"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["emitted_contract_formats"] == (
        diagnostic_contract_check["detail"]["text_renderer"]["required_contract_formats"]
    )
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert diagnostic_contract_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert diagnostic_contract_check["detail"]["text_renderer"]["json_fallback"] is False
    lint_check = next(check for check in report["checks"] if check["id"] == "lint_directory_and_strict_profiles")
    assert lint_check["detail"]["directory_cli"]["format"] == "appgen.lint-directory-cli-audit.v1"
    assert lint_check["detail"]["directory_cli"]["ok"] is True
    assert lint_check["detail"]["directory_cli"]["source_mode"] == "directory"
    assert lint_check["detail"]["directory_cli"]["file_report_count"] == 2
    assert lint_check["detail"]["directory_cli"]["warning_count"] >= 1
    assert lint_check["detail"]["directory_cli"]["diagnostics_have_files"] is True
    assert lint_check["detail"]["directory_cli"]["normal_unknown_component_warning"]["ok"] is True
    assert lint_check["detail"]["directory_cli"]["strict_unknown_component_error"]["ok"] is True
    assert lint_check["detail"]["directory_cli"]["strict_catalog_component_success"]["ok"] is True
    lint_contract_check = next(check for check in report["checks"] if check["id"] == "lint_cli_directory_contracts")
    assert lint_contract_check["detail"]["lint_format"] == "appgen.lint-report.v1"
    assert lint_contract_check["detail"]["strict"] is True
    assert tuple(lint_contract_check["detail"]["catalog_components"]) == ("CustomGauge",)
    assert lint_contract_check["detail"]["directory_cli"]["format"] == "appgen.lint-directory-cli-audit.v1"
    assert lint_contract_check["detail"]["directory_cli"]["passing_scenario_count"] == (
        lint_contract_check["detail"]["directory_cli"]["scenario_count"]
    )
    assert lint_contract_check["detail"]["directory_cli"]["failing_scenario_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["failing_scenarios"] == ()
    assert lint_contract_check["detail"]["directory_cli"]["exit_codes_by_scenario"] == (
        lint_contract_check["detail"]["directory_cli"]["expected_exit_codes_by_scenario"]
    )
    assert lint_contract_check["detail"]["directory_cli"]["missing_exit_code_scenario_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["missing_exit_code_scenarios"] == ()
    assert lint_contract_check["detail"]["directory_cli"]["payload_formats_by_scenario"] == (
        lint_contract_check["detail"]["directory_cli"]["expected_payload_formats_by_scenario"]
    )
    assert lint_contract_check["detail"]["directory_cli"]["missing_payload_format_scenario_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["missing_payload_format_scenarios"] == ()
    assert lint_contract_check["detail"]["directory_cli"]["ok_by_scenario"] == {
        scenario: True for scenario in lint_contract_check["detail"]["directory_cli"]["required_scenario_ids"]
    }
    assert lint_contract_check["detail"]["directory_cli"]["missing_ok_scenario_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["missing_ok_scenarios"] == ()
    assert lint_contract_check["detail"]["directory_cli"]["stage_profile_count"] == 3
    assert lint_contract_check["detail"]["directory_cli"]["passing_stage_profile_count"] == 3
    assert lint_contract_check["detail"]["directory_cli"]["failing_stage_profile_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["stage_profile_ids"] == ("syntax", "semantic", "policy")
    assert lint_contract_check["detail"]["directory_cli"]["exit_codes_by_stage_profile"] == (
        lint_contract_check["detail"]["directory_cli"]["expected_exit_codes_by_stage_profile"]
    )
    assert lint_contract_check["detail"]["directory_cli"]["missing_stage_profile_exit_code_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["missing_stage_profile_exit_code_profiles"] == ()
    assert lint_contract_check["detail"]["directory_cli"]["ok_by_stage_profile"] == {
        "syntax": True,
        "semantic": True,
        "policy": True,
    }
    assert lint_contract_check["detail"]["directory_cli"]["missing_ok_stage_profile_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["missing_ok_stage_profiles"] == ()
    assert lint_contract_check["detail"]["directory_cli"]["missing_stage_name_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["missing_severity_name_count"] == 0
    assert lint_contract_check["detail"]["directory_cli"]["source_mode"] == "directory"
    assert lint_contract_check["detail"]["directory_cli"]["file_order_sorted"] is True
    assert lint_contract_check["detail"]["directory_cli"]["file_relative_order"] == ("a.appgen", "nested/b.appgen")
    assert lint_contract_check["detail"]["directory_cli"]["file_report_count"] == 2
    assert lint_contract_check["detail"]["directory_cli"]["diagnostics_have_files"] is True
    assert lint_contract_check["detail"]["directory_cli"]["warning_count"] >= 1
    assert lint_contract_check["detail"]["directory_cli"]["normal_unknown_component_warning"]["ok"] is True
    assert lint_contract_check["detail"]["directory_cli"]["strict_unknown_component_error"]["ok"] is True
    assert lint_contract_check["detail"]["directory_cli"]["strict_catalog_component_success"]["ok"] is True
    assert lint_contract_check["detail"]["directory_cli"]["previous_semantic_migration_preview"]["ok"] is True
    assert lint_contract_check["detail"]["directory_cli"]["stage_separation"]["ok"] is True
    assert lint_contract_check["detail"]["text_renderer"]["format"] == "appgen.lint-text-renderer.v1"
    assert lint_contract_check["detail"]["text_renderer"]["source_file_line_count"] >= 1
    assert lint_contract_check["detail"]["text_renderer"]["stage_line_count"] >= 1
    assert lint_contract_check["detail"]["text_renderer"]["migration_preview_line_count"] >= 1
    assert lint_contract_check["detail"]["text_renderer"]["diagnostic_line_count"] >= 1
    assert lint_contract_check["detail"]["text_renderer"]["emitted_source_files"] == (
        lint_contract_check["detail"]["text_renderer"]["required_source_files"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_source_file_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_source_files"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        lint_contract_check["detail"]["text_renderer"]["required_text_surfaces"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_contract_formats"] == (
        lint_contract_check["detail"]["text_renderer"]["required_contract_formats"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_source_modes"] == (
        lint_contract_check["detail"]["text_renderer"]["required_source_modes"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_source_mode_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_source_modes"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_migration_backends"] == (
        lint_contract_check["detail"]["text_renderer"]["required_migration_backends"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_migration_backend_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_migration_backends"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_approval_values"] == (
        lint_contract_check["detail"]["text_renderer"]["required_approval_values"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_approval_value_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_approval_values"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_stage_counts"] == (
        lint_contract_check["detail"]["text_renderer"]["required_stage_counts"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_stage_count_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_stage_counts"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_stage_names"] == (
        lint_contract_check["detail"]["text_renderer"]["required_stage_names"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_stage_name_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_stage_names"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_migration_families"] == (
        lint_contract_check["detail"]["text_renderer"]["required_migration_families"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_migration_family_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_migration_families"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_diagnostic_codes"] == (
        lint_contract_check["detail"]["text_renderer"]["required_diagnostic_codes"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_diagnostic_code_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_diagnostic_codes"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["emitted_diagnostic_severities"] == (
        lint_contract_check["detail"]["text_renderer"]["required_diagnostic_severities"]
    )
    assert lint_contract_check["detail"]["text_renderer"]["missing_diagnostic_severity_count"] == 0
    assert lint_contract_check["detail"]["text_renderer"]["missing_diagnostic_severities"] == ()
    assert lint_contract_check["detail"]["text_renderer"]["json_fallback"] is False
    component_publish_check = next(check for check in report["checks"] if check["id"] == "component_publish_catalog_contracts")
    assert component_publish_check["detail"]["cli"]["format"] == "appgen.component-publish-cli-audit.v1"
    assert component_publish_check["detail"]["cli"]["passing_case_count"] == component_publish_check["detail"]["cli"]["case_count"]
    assert component_publish_check["detail"]["cli"]["failing_case_count"] == 0
    assert component_publish_check["detail"]["cli"]["case_ids"] == (
        "json_publish_patch",
        "text_publish_markers",
        "missing_catalog_rejected",
    )
    assert component_publish_check["detail"]["cli"]["required_case_ids"] == (
        "json_publish_patch",
        "text_publish_markers",
        "missing_catalog_rejected",
    )
    assert component_publish_check["detail"]["cli"]["observed_case_ids"] == (
        component_publish_check["detail"]["cli"]["required_case_ids"]
    )
    assert component_publish_check["detail"]["cli"]["missing_case_count"] == 0
    assert component_publish_check["detail"]["cli"]["missing_case_ids"] == ()
    assert component_publish_check["detail"]["cli"]["exit_codes_by_case"] == (
        component_publish_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert component_publish_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert component_publish_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert component_publish_check["detail"]["cli"]["ok_by_case"] == {
        case_id: True for case_id in component_publish_check["detail"]["cli"]["required_case_ids"]
    }
    assert component_publish_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert component_publish_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert component_publish_check["detail"]["cli"]["patch_format"] == "appgen.component-catalog-patch.v1"
    assert component_publish_check["detail"]["cli"]["operation"] == "upsert_component"
    assert component_publish_check["detail"]["cli"]["component"] == "CustomGauge"
    assert component_publish_check["detail"]["cli"]["component_icon"] == "custom-gauge"
    assert component_publish_check["detail"]["cli"]["before_count"] == 1
    assert component_publish_check["detail"]["cli"]["after_count"] == 2
    assert component_publish_check["detail"]["cli"]["side_effect_free"] is True
    assert component_publish_check["detail"]["cli"]["write_performed"] is False
    assert component_publish_check["detail"]["cli"]["text_has_report_format"] is True
    assert component_publish_check["detail"]["cli"]["text_has_patch_format"] is True
    assert component_publish_check["detail"]["cli"]["text_has_side_effect_markers"] is True
    assert component_publish_check["detail"]["cli"]["text_has_existing_catalog"] is True
    assert component_publish_check["detail"]["cli"]["missing_text_marker_count"] == 0
    assert component_publish_check["detail"]["cli"]["missing_text_markers"] == ()
    assert component_publish_check["detail"]["cli"]["missing_catalog_exit_code"] == 1
    assert component_publish_check["detail"]["cli"]["required_missing_catalog_blocking_gaps"] == (
        "catalog_path_readable",
    )
    assert "catalog_path_readable" in component_publish_check["detail"]["cli"]["missing_catalog_blocking_gaps"]
    assert component_publish_check["detail"]["cli"]["missing_catalog_blocking_gap_miss_count"] == 0
    assert component_publish_check["detail"]["cli"]["missing_catalog_blocking_gap_misses"] == ()
    assert component_publish_check["detail"]["cli"]["missing_catalog_side_effect_free"] is True
    assert component_publish_check["detail"]["cli"]["missing_catalog_write_performed"] is False
    assert component_publish_check["detail"]["text_renderer"]["format"] == "appgen.component-publish-text-renderer.v1"
    assert component_publish_check["detail"]["text_renderer"]["summary_line_count"] == 1
    assert component_publish_check["detail"]["text_renderer"]["catalog_line_count"] >= 2
    assert component_publish_check["detail"]["text_renderer"]["side_effect_line_count"] == 1
    assert component_publish_check["detail"]["text_renderer"]["patch_contract_line_count"] == 1
    assert component_publish_check["detail"]["text_renderer"]["existing_catalog_line_count"] == 1
    assert component_publish_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        component_publish_check["detail"]["text_renderer"]["required_text_surfaces"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_contract_formats"] == (
        component_publish_check["detail"]["text_renderer"]["required_contract_formats"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_registration_values"] == (
        component_publish_check["detail"]["text_renderer"]["required_registration_values"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_registration_value_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_registration_values"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_catalog_count_markers"] == (
        component_publish_check["detail"]["text_renderer"]["required_catalog_count_markers"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_catalog_count_marker_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_catalog_count_markers"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_catalog_sources"] == (
        component_publish_check["detail"]["text_renderer"]["required_catalog_sources"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_catalog_source_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_catalog_sources"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_side_effect_values"] == (
        component_publish_check["detail"]["text_renderer"]["required_side_effect_values"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_side_effect_value_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_side_effect_values"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_write_values"] == (
        component_publish_check["detail"]["text_renderer"]["required_write_values"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_write_value_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_write_values"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_patch_formats"] == (
        component_publish_check["detail"]["text_renderer"]["required_patch_formats"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_patch_format_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_patch_formats"] == ()
    assert component_publish_check["detail"]["text_renderer"]["emitted_existing_components"] == (
        component_publish_check["detail"]["text_renderer"]["required_existing_components"]
    )
    assert component_publish_check["detail"]["text_renderer"]["missing_existing_component_count"] == 0
    assert component_publish_check["detail"]["text_renderer"]["missing_existing_components"] == ()
    assert component_publish_check["detail"]["text_renderer"]["json_fallback"] is False
    test_strategy_check = next(check for check in report["checks"] if check["id"] == "parser_golden_and_drift_gates")
    assert test_strategy_check["detail"]["cli"]["format"] == "appgen.test-strategy-cli-audit.v1"
    assert test_strategy_check["detail"]["cli"]["ok"] is True
    assert test_strategy_check["detail"]["cli"]["case_count"] == len(test_strategy_check["detail"]["cli"]["cases"])
    assert test_strategy_check["detail"]["cli"]["passing_case_count"] == test_strategy_check["detail"]["cli"]["case_count"]
    assert test_strategy_check["detail"]["cli"]["failing_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["observed_case_ids"] == (
        test_strategy_check["detail"]["cli"]["required_case_ids"]
    )
    assert test_strategy_check["detail"]["cli"]["missing_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_case_ids"] == ()
    assert test_strategy_check["detail"]["cli"]["case_ids"] == tuple(
        case["case"] for case in test_strategy_check["detail"]["cli"]["cases"]
    )
    assert test_strategy_check["detail"]["cli"]["required_surface_count"] == 6
    assert test_strategy_check["detail"]["cli"]["observed_surface_count"] >= 6
    assert test_strategy_check["detail"]["cli"]["missing_surface_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_surfaces"] == ()
    assert set(test_strategy_check["detail"]["cli"]["required_surfaces"]) <= set(
        test_strategy_check["detail"]["cli"]["observed_surfaces"]
    )
    assert test_strategy_check["detail"]["cli"]["payload_format_count"] == len(
        test_strategy_check["detail"]["cli"]["payload_formats"]
    )
    assert test_strategy_check["detail"]["cli"]["payload_formats_by_case"] == (
        test_strategy_check["detail"]["cli"]["expected_payload_formats_by_case"]
    )
    assert test_strategy_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert test_strategy_check["detail"]["cli"]["exit_codes_by_case"] == (
        test_strategy_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert test_strategy_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert test_strategy_check["detail"]["cli"]["ok_by_case"] == {
        "diagnostics_catalog": True,
        "diagnostics_audit_fixtures": True,
        "parser_golden": True,
        "semantic_drift": True,
        "doctor": True,
    }
    assert test_strategy_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert test_strategy_check["detail"]["cli"]["text_exit_codes_by_case"] == (
        test_strategy_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert test_strategy_check["detail"]["cli"]["missing_text_exit_code_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_text_exit_code_cases"] == ()
    assert test_strategy_check["detail"]["cli"]["text_marker_present_by_case"] == {
        "diagnostics_catalog": True,
        "diagnostics_audit_fixtures": True,
        "parser_golden": True,
        "semantic_drift": True,
        "doctor": True,
    }
    assert test_strategy_check["detail"]["cli"]["missing_text_marker_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["missing_text_marker_cases"] == ()
    assert test_strategy_check["detail"]["cli"]["text_json_fallback_by_case"] == {
        "diagnostics_catalog": False,
        "diagnostics_audit_fixtures": False,
        "parser_golden": False,
        "semantic_drift": False,
        "doctor": False,
    }
    assert test_strategy_check["detail"]["cli"]["text_json_fallback_case_count"] == 0
    assert test_strategy_check["detail"]["cli"]["text_json_fallback_cases"] == ()
    assert test_strategy_check["detail"]["cli"]["doctor_check_count"] > 0
    assert {
        "diagnostics_catalog",
        "diagnostics_audit_fixtures",
        "parser_golden",
        "semantic_drift",
        "doctor",
    } <= {case["case"] for case in test_strategy_check["detail"]["cli"]["cases"]}
    drift_case = next(case for case in test_strategy_check["detail"]["cli"]["cases"] if case["case"] == "semantic_drift")
    assert {"cli", "lsp", "studio", "graph", "generator", "release_verifier"} <= set(
        drift_case["required_surfaces"]
    )
    assert drift_case["generate_report"] == "appgen.generate-report.v1"
    family_gate = next(check for check in report["checks"] if check["id"] == "test_strategy_family_contracts")
    assert family_gate["ok"] is True
    assert family_gate["detail"]["format"] == "appgen.test-family-contract-audit.v1"
    assert family_gate["detail"]["family_count"] == 11
    assert family_gate["detail"]["passing_family_count"] == family_gate["detail"]["family_count"]
    assert family_gate["detail"]["missing_family_count"] == 0
    assert family_gate["detail"]["missing_families"] == ()
    assert {
        "parser_golden_tests",
        "semantic_tests",
        "diagnostic_golden_tests",
        "formatter_tests",
        "cli_contract_tests",
        "lsp_tests",
        "graph_tests",
        "migration_tests",
        "natural_language_planner_tests",
        "verifier_tests",
        "drift_tests",
    } == set(family_gate["detail"]["family_names"])
    assert all(family["ok"] for family in family_gate["detail"]["families"])
    parser_gate = next(check for check in report["checks"] if check["id"] == "parser_golden_fixture_contracts")
    assert parser_gate["detail"]["parser"]["format"] == "appgen.parser-golden-audit.v1"
    assert parser_gate["detail"]["parser"]["required_construct_count"] == (
        parser_gate["detail"]["parser"]["covered_construct_count"]
    )
    assert parser_gate["detail"]["parser"]["missing_construct_count"] == 0
    assert parser_gate["detail"]["parser"]["passing_fixture_count"] == parser_gate["detail"]["parser"]["fixture_count"]
    assert parser_gate["detail"]["parser"]["failing_fixture_count"] == 0
    assert parser_gate["detail"]["parser"]["blocking_gap_count"] == 0
    assert parser_gate["detail"]["parser"]["valid_fixture_count"] >= 1
    assert parser_gate["detail"]["parser"]["invalid_fixture_count"] >= 1
    assert parser_gate["detail"]["text_renderer"]["format"] == "appgen.parser-golden-text-renderer.v1"
    assert parser_gate["detail"]["text_renderer"]["missing_fragment_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["marker_line_count"] >= 4
    assert parser_gate["detail"]["text_renderer"]["emitted_covered_constructs"] == parser_gate["detail"][
        "text_renderer"
    ]["required_covered_constructs"]
    assert parser_gate["detail"]["text_renderer"]["missing_covered_construct_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["missing_covered_constructs"] == ()
    assert parser_gate["detail"]["text_renderer"]["emitted_missing_constructs"] == parser_gate["detail"][
        "text_renderer"
    ]["required_missing_constructs"]
    assert parser_gate["detail"]["text_renderer"]["missing_missing_construct_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["missing_missing_constructs"] == ()
    assert parser_gate["detail"]["text_renderer"]["emitted_gap_ids"] == parser_gate["detail"]["text_renderer"][
        "required_gap_ids"
    ]
    assert parser_gate["detail"]["text_renderer"]["missing_gap_id_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["missing_gap_ids"] == ()
    assert parser_gate["detail"]["text_renderer"]["emitted_text_surfaces"] == parser_gate["detail"][
        "text_renderer"
    ]["required_text_surfaces"]
    assert parser_gate["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert parser_gate["detail"]["text_renderer"]["emitted_report_formats"] == parser_gate["detail"][
        "text_renderer"
    ]["required_report_formats"]
    assert parser_gate["detail"]["text_renderer"]["missing_report_format_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["missing_report_formats"] == ()
    assert parser_gate["detail"]["text_renderer"]["emitted_count_markers"] == parser_gate["detail"][
        "text_renderer"
    ]["required_count_markers"]
    assert parser_gate["detail"]["text_renderer"]["missing_count_marker_count"] == 0
    assert parser_gate["detail"]["text_renderer"]["missing_count_markers"] == ()
    assert parser_gate["detail"]["text_renderer"]["json_fallback"] is False
    drift_gate = next(check for check in report["checks"] if check["id"] == "semantic_drift_surface_contracts")
    assert drift_gate["detail"]["drift"]["format"] == "appgen.semantic-drift-audit.v1"
    assert drift_gate["detail"]["drift"]["semantic_model_format"] == "appgen.semantic-model.v1"
    assert drift_gate["detail"]["drift"]["surface_count"] >= 8
    assert drift_gate["detail"]["drift"]["blocking_gap_count"] == 0
    assert drift_gate["detail"]["drift"]["surface_evidence"]["generate_report"] == "appgen.generate-report.v1"
    assert drift_gate["detail"]["text_renderer"]["format"] == "appgen.semantic-drift-text-renderer.v1"
    assert drift_gate["detail"]["text_renderer"]["surface_line_count"] >= 1
    assert drift_gate["detail"]["text_renderer"]["evidence_line_count"] >= 3
    assert drift_gate["detail"]["text_renderer"]["check_line_count"] >= 2
    assert drift_gate["detail"]["text_renderer"]["digest_line_count"] >= 1
    assert drift_gate["detail"]["text_renderer"]["emitted_surfaces"] == drift_gate["detail"]["text_renderer"][
        "required_surfaces"
    ]
    assert drift_gate["detail"]["text_renderer"]["missing_surface_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_surfaces"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_gap_ids"] == drift_gate["detail"]["text_renderer"][
        "required_gap_ids"
    ]
    assert drift_gate["detail"]["text_renderer"]["missing_gap_id_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_gap_ids"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_evidence_keys"] == drift_gate["detail"]["text_renderer"][
        "required_evidence_keys"
    ]
    assert drift_gate["detail"]["text_renderer"]["missing_evidence_key_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_evidence_keys"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_check_ids"] == drift_gate["detail"]["text_renderer"][
        "required_check_ids"
    ]
    assert drift_gate["detail"]["text_renderer"]["missing_check_id_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_check_ids"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_passing_check_ids"] == drift_gate["detail"][
        "text_renderer"
    ]["required_passing_check_ids"]
    assert drift_gate["detail"]["text_renderer"]["missing_passing_check_id_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_passing_check_ids"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_failing_check_ids"] == drift_gate["detail"][
        "text_renderer"
    ]["required_failing_check_ids"]
    assert drift_gate["detail"]["text_renderer"]["missing_failing_check_id_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_failing_check_ids"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_text_surfaces"] == drift_gate["detail"][
        "text_renderer"
    ]["required_text_surfaces"]
    assert drift_gate["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_contract_formats"] == drift_gate["detail"][
        "text_renderer"
    ]["required_contract_formats"]
    assert drift_gate["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert drift_gate["detail"]["text_renderer"]["emitted_semantic_digests"] == drift_gate["detail"][
        "text_renderer"
    ]["required_semantic_digests"]
    assert drift_gate["detail"]["text_renderer"]["missing_semantic_digest_count"] == 0
    assert drift_gate["detail"]["text_renderer"]["missing_semantic_digests"] == ()
    assert drift_gate["detail"]["text_renderer"]["json_fallback"] is False
    assert drift_gate["detail"]["cli"]["observed_surface_count"] >= drift_gate["detail"]["cli"]["required_surface_count"]
    assert drift_gate["detail"]["cli"]["missing_surface_count"] == 0
    assert drift_gate["detail"]["cli"]["failing_case_count"] == 0
    assert drift_gate["detail"]["cli"]["missing_surfaces"] == ()
    assert set(drift_gate["detail"]["cli"]["required_surfaces"]) <= set(drift_gate["detail"]["cli"]["observed_surfaces"])
    assert drift_gate["detail"]["cli"]["payload_format_count"] == len(drift_gate["detail"]["cli"]["payload_formats"])
    doctor_gate = next(check for check in report["checks"] if check["id"] == "doctor_cli_text_contracts")
    assert doctor_gate["detail"]["doctor"]["format"] == "appgen.doctor-report.v1"
    assert doctor_gate["detail"]["doctor"]["check_count"] >= 15
    assert doctor_gate["detail"]["doctor"]["blocking_gap_count"] == 0
    assert doctor_gate["detail"]["doctor"]["observed_check_ids"] == doctor_gate["detail"]["doctor"]["required_check_ids"]
    assert doctor_gate["detail"]["doctor"]["missing_required_check_count"] == 0
    assert doctor_gate["detail"]["doctor"]["missing_required_check_ids"] == ()
    assert doctor_gate["detail"]["doctor"]["missing_detail_format_check_count"] == 0
    assert doctor_gate["detail"]["doctor"]["missing_detail_format_checks"] == ()
    assert {
        "parser_golden_fixtures",
        "directory_lint_input",
        "cli_alias_contract",
        "module_boundaries",
        "studio_semantic_service",
        "vscode_extension_surface",
    } <= set(doctor_gate["detail"]["doctor"]["check_ids"])
    assert doctor_gate["detail"]["text_renderer"]["format"] == "appgen.doctor-text-renderer.v1"
    assert doctor_gate["detail"]["text_renderer"]["check_line_count"] >= 8
    assert doctor_gate["detail"]["text_renderer"]["detail_format_line_count"] >= 8
    assert doctor_gate["detail"]["text_renderer"]["emitted_check_ids"] == doctor_gate["detail"]["text_renderer"][
        "required_check_ids"
    ]
    assert doctor_gate["detail"]["text_renderer"]["missing_check_id_count"] == 0
    assert doctor_gate["detail"]["text_renderer"]["missing_check_ids"] == ()
    assert doctor_gate["detail"]["text_renderer"]["emitted_detail_formats_by_check"] == doctor_gate["detail"][
        "text_renderer"
    ]["required_detail_formats_by_check"]
    assert doctor_gate["detail"]["text_renderer"]["missing_detail_format_check_count"] == 0
    assert doctor_gate["detail"]["text_renderer"]["missing_detail_format_checks"] == ()
    assert doctor_gate["detail"]["text_renderer"]["emitted_check_outcomes"] == doctor_gate["detail"][
        "text_renderer"
    ]["required_check_outcomes"]
    assert doctor_gate["detail"]["text_renderer"]["missing_check_outcome_count"] == 0
    assert doctor_gate["detail"]["text_renderer"]["missing_check_outcomes"] == ()
    assert doctor_gate["detail"]["text_renderer"]["emitted_text_surfaces"] == doctor_gate["detail"][
        "text_renderer"
    ]["required_text_surfaces"]
    assert doctor_gate["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert doctor_gate["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert doctor_gate["detail"]["text_renderer"]["emitted_report_formats"] == doctor_gate["detail"][
        "text_renderer"
    ]["required_report_formats"]
    assert doctor_gate["detail"]["text_renderer"]["missing_report_format_count"] == 0
    assert doctor_gate["detail"]["text_renderer"]["missing_report_formats"] == ()
    assert doctor_gate["detail"]["text_renderer"]["json_fallback"] is False
    assert doctor_gate["detail"]["cli"]["format"] == "appgen.doctor-cli-audit.v1"
    assert doctor_gate["detail"]["cli"]["case_count"] == 2
    assert doctor_gate["detail"]["cli"]["passing_case_count"] == doctor_gate["detail"]["cli"]["case_count"]
    assert doctor_gate["detail"]["cli"]["failing_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["failing_cases"] == ()
    assert doctor_gate["detail"]["cli"]["observed_case_ids"] == doctor_gate["detail"]["cli"]["required_case_ids"]
    assert doctor_gate["detail"]["cli"]["missing_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_case_ids"] == ()
    assert doctor_gate["detail"]["cli"]["modes_by_case"] == doctor_gate["detail"]["cli"]["expected_modes_by_case"]
    assert doctor_gate["detail"]["cli"]["missing_mode_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_mode_cases"] == ()
    assert doctor_gate["detail"]["cli"]["exit_codes_by_case"] == doctor_gate["detail"]["cli"][
        "expected_exit_codes_by_case"
    ]
    assert doctor_gate["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert doctor_gate["detail"]["cli"]["ok_by_case"] == {"doctor_json": True, "doctor_text": True}
    assert doctor_gate["detail"]["cli"]["missing_ok_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_ok_cases"] == ()
    assert doctor_gate["detail"]["cli"]["payload_formats_by_case"] == doctor_gate["detail"]["cli"][
        "expected_payload_formats_by_case"
    ]
    assert doctor_gate["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert doctor_gate["detail"]["cli"]["observed_check_ids"] == doctor_gate["detail"]["cli"]["required_check_ids"]
    assert doctor_gate["detail"]["cli"]["missing_required_check_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_required_check_ids"] == ()
    assert doctor_gate["detail"]["cli"]["detail_formats_by_check"] == doctor_gate["detail"]["cli"][
        "required_detail_formats_by_check"
    ]
    assert doctor_gate["detail"]["cli"]["missing_detail_format_check_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_detail_format_checks"] == ()
    assert doctor_gate["detail"]["cli"]["missing_text_marker_count"] == 0
    assert doctor_gate["detail"]["cli"]["missing_text_marker_cases"] == ()
    assert doctor_gate["detail"]["cli"]["text_json_fallback_by_case"] == {"doctor_text": False}
    assert doctor_gate["detail"]["cli"]["text_json_fallback_case_count"] == 0
    assert doctor_gate["detail"]["cli"]["text_json_fallback_cases"] == ()
    assert doctor_gate["detail"]["cli"]["doctor_check_count"] >= 15
    assert doctor_gate["detail"]["cli"]["strategy_doctor_check_count"] >= 15
    package_check = next(check for check in report["checks"] if check["id"] == "package_and_release_verifiers")
    assert package_check["detail"]["cli"]["format"] == "appgen.package-verify-cli-audit.v1"
    assert package_check["detail"]["cli"]["ok"] is True
    assert package_check["detail"]["invalid_target"]["format"] == "appgen.package-invalid-target-audit.v1"
    assert package_check["detail"]["invalid_target"]["ok"] is True
    assert package_check["detail"]["invalid_target"]["case_count"] == 2
    assert package_check["detail"]["invalid_target"]["passing_case_count"] == 2
    assert package_check["detail"]["invalid_target"]["failing_case_count"] == 0
    assert package_check["detail"]["invalid_target"]["missing_case_count"] == 0
    assert package_check["detail"]["invalid_target"]["invalid_choice_message_count"] == 2
    assert package_check["detail"]["invalid_target"]["missing_invalid_choice_message_count"] == 0
    assert package_check["detail"]["invalid_target"]["traceback_free_count"] == 2
    assert package_check["detail"]["invalid_target"]["missing_traceback_free_count"] == 0
    assert package_check["detail"]["invalid_target"]["missing_expected_exit_code_count"] == 0
    assert set(package_check["detail"]["invalid_target"]["case_ids"]) == {
        "package_invalid_target",
        "verify_invalid_target",
    }
    assert package_check["detail"]["cli"]["case_count"] == 2
    assert package_check["detail"]["cli"]["passing_case_count"] == 2
    assert package_check["detail"]["cli"]["failing_case_count"] == 0
    assert package_check["detail"]["cli"]["observed_case_ids"] == package_check["detail"]["cli"]["required_case_ids"]
    assert package_check["detail"]["cli"]["missing_case_count"] == 0
    assert package_check["detail"]["cli"]["missing_case_ids"] == ()
    assert package_check["detail"]["cli"]["exit_codes_by_case"] == (
        package_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert package_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert package_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert package_check["detail"]["cli"]["payload_formats_by_case"] == (
        package_check["detail"]["cli"]["expected_payload_formats_by_case"]
    )
    assert package_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert package_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert package_check["detail"]["cli"]["ok_by_case"] == {
        case_id: True for case_id in package_check["detail"]["cli"]["required_case_ids"]
    }
    assert package_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert package_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert package_check["detail"]["cli"]["missing_manifest_target_count"] == 0
    assert package_check["detail"]["cli"]["missing_release_report_count"] == 0
    assert package_check["detail"]["cli"]["target_count"] == 5
    assert package_check["detail"]["cli"]["manifest_count"] == 5
    assert package_check["detail"]["cli"]["handoff_artifact_count"] >= 25
    assert {
        "verify_all_targets",
        "package_writes_target_manifests",
    } <= {case["case"] for case in package_check["detail"]["cli"]["cases"]}
    manifest_case = next(
        case for case in package_check["detail"]["cli"]["cases"] if case["case"] == "package_writes_target_manifests"
    )
    assert set(manifest_case["release_evidence_reports"]) == {"web", "mobile", "desktop", "pbc", "deployment"}
    assert manifest_case["release_graph_suite_format"] == "appgen.graph-suite-report.v1"
    assert set(manifest_case["release_graph_formats"]) == {"json", "mermaid", "dot"}
    assert manifest_case["web_artifact_class"] == "web_application"
    assert {"routes", "forms", "handlers", "smoke_tests"} <= set(manifest_case["web_handoff_artifacts"])
    assert manifest_case["web_app_build_contract"] is True
    assert manifest_case["web_routes_declared"] is True
    assert manifest_case["web_forms_bind_valid_fields"] is True
    assert manifest_case["web_handler_targets_resolve"] is True
    assert manifest_case["web_smoke_tests_declared"] is True
    assert manifest_case["web_smoke_entrypoint"] == "web.smoke"
    assert manifest_case["mobile_artifact_class"] == "mobile_application"
    assert {"signing_posture", "offline_policy", "permissions", "screen_density", "smoke_launch"} <= set(
        manifest_case["mobile_handoff_artifacts"]
    )
    assert manifest_case["mobile_signing_posture_declared"] is True
    assert manifest_case["mobile_offline_policy_declared"] is True
    assert manifest_case["mobile_permissions_explained"] is True
    assert manifest_case["mobile_screens_fit_target_density"] is True
    assert manifest_case["mobile_smoke_entrypoint"] == "mobile.launch"
    assert manifest_case["desktop_artifact_class"] == "desktop_application"
    assert {"installer_profile", "startup_assets", "menus", "context_menus", "smoke_launch"} <= set(
        manifest_case["desktop_handoff_artifacts"]
    )
    assert manifest_case["desktop_installer_posture_declared"] is True
    assert manifest_case["desktop_startup_assets_declared"] is True
    assert manifest_case["desktop_menus_bind_to_handlers"] is True
    assert manifest_case["desktop_smoke_entrypoint"] == "desktop.launch"
    assert manifest_case["pbc_artifact_class"] == "packaged_business_capability"
    assert manifest_case["deployment_artifact_class"] == "deployment_plan"
    package_manifest_check = next(check for check in report["checks"] if check["id"] == "package_manifest_handoff_contracts")
    assert package_manifest_check["detail"]["format"] == "appgen.package-verify-cli-audit.v1"
    assert package_manifest_check["detail"]["target_count"] == 5
    assert package_manifest_check["detail"]["expected_targets"] == ("web", "mobile", "desktop", "pbc", "deployment")
    assert package_manifest_check["detail"]["failing_case_count"] == 0
    assert package_manifest_check["detail"]["failing_cases"] == ()
    assert package_manifest_check["detail"]["case_ids"] == ("verify_all_targets", "package_writes_target_manifests")
    assert package_manifest_check["detail"]["observed_case_ids"] == package_manifest_check["detail"]["required_case_ids"]
    assert package_manifest_check["detail"]["missing_case_count"] == 0
    assert package_manifest_check["detail"]["missing_case_ids"] == ()
    assert package_manifest_check["detail"]["exit_codes_by_case"] == (
        package_manifest_check["detail"]["expected_exit_codes_by_case"]
    )
    assert package_manifest_check["detail"]["missing_exit_code_case_count"] == 0
    assert package_manifest_check["detail"]["missing_exit_code_cases"] == ()
    assert package_manifest_check["detail"]["payload_formats_by_case"] == (
        package_manifest_check["detail"]["expected_payload_formats_by_case"]
    )
    assert package_manifest_check["detail"]["missing_payload_format_case_count"] == 0
    assert package_manifest_check["detail"]["missing_payload_format_cases"] == ()
    assert package_manifest_check["detail"]["ok_by_case"] == {
        case_id: True for case_id in package_manifest_check["detail"]["required_case_ids"]
    }
    assert package_manifest_check["detail"]["missing_ok_case_count"] == 0
    assert package_manifest_check["detail"]["missing_ok_cases"] == ()
    assert package_manifest_check["detail"]["manifest_count"] == 5
    assert package_manifest_check["detail"]["manifest_target_count"] == 5
    assert package_manifest_check["detail"]["manifest_targets"] == ("web", "mobile", "desktop", "pbc", "deployment")
    assert package_manifest_check["detail"]["missing_manifest_target_count"] == 0
    assert package_manifest_check["detail"]["missing_manifest_targets"] == ()
    assert package_manifest_check["detail"]["manifest_formats"]["web"] == "appgen.package-manifest.v1"
    assert package_manifest_check["detail"]["required_manifest_formats_by_target"] == {
        target: "appgen.package-manifest.v1"
        for target in package_manifest_check["detail"]["expected_targets"]
    }
    assert package_manifest_check["detail"]["missing_manifest_format_target_count"] == 0
    assert package_manifest_check["detail"]["missing_manifest_format_targets"] == ()
    assert package_manifest_check["detail"]["artifact_classes_by_target"] == (
        package_manifest_check["detail"]["required_artifact_classes_by_target"]
    )
    assert package_manifest_check["detail"]["missing_artifact_class_target_count"] == 0
    assert package_manifest_check["detail"]["missing_artifact_class_targets"] == ()
    assert package_manifest_check["detail"]["smoke_entrypoints_by_target"] == (
        package_manifest_check["detail"]["required_smoke_entrypoints_by_target"]
    )
    assert package_manifest_check["detail"]["missing_smoke_entrypoint_target_count"] == 0
    assert package_manifest_check["detail"]["missing_smoke_entrypoint_targets"] == ()
    assert package_manifest_check["detail"]["handoff_artifact_count"] >= 25
    assert package_manifest_check["detail"]["handoff_counts_by_target"]["mobile"] >= 6
    assert package_manifest_check["detail"]["missing_handoff_artifact_count"] == 0
    assert package_manifest_check["detail"]["missing_handoff_artifacts"] == ()
    assert package_manifest_check["detail"]["missing_handoff_artifacts_by_target"] == {
        "web": (),
        "mobile": (),
        "desktop": (),
        "pbc": (),
        "deployment": (),
    }
    assert package_manifest_check["detail"]["required_handoff_artifacts_by_target"]["web"] == (
        "routes",
        "forms",
        "handlers",
        "smoke_tests",
    )
    assert package_manifest_check["detail"]["required_handoff_artifacts_by_target"]["desktop"] == (
        "desktop_metadata",
        "installer_profile",
        "startup_assets",
        "menus",
        "context_menus",
        "smoke_launch",
    )
    assert set(package_manifest_check["detail"]["required_handoff_artifacts_by_target"]["deployment"]) <= set(
        package_manifest_check["detail"]["handoff_artifacts_by_target"]["deployment"]
    )
    assert package_manifest_check["detail"]["readiness_check_count"] == 29
    assert package_manifest_check["detail"]["passing_readiness_check_count"] == (
        package_manifest_check["detail"]["readiness_check_count"]
    )
    assert package_manifest_check["detail"]["missing_readiness_check_count"] == 0
    assert package_manifest_check["detail"]["missing_readiness_checks"] == ()
    assert package_manifest_check["detail"]["missing_readiness_checks_by_target"] == {
        "web": (),
        "mobile": (),
        "desktop": (),
        "pbc": (),
        "deployment": (),
    }
    assert set(package_manifest_check["detail"]["readiness_matrix"]) == {
        "web",
        "mobile",
        "desktop",
        "pbc",
        "deployment",
    }
    assert all(all(checks.values()) for checks in package_manifest_check["detail"]["readiness_matrix"].values())
    assert package_manifest_check["detail"]["readiness_matrix"]["web"]["smoke_entrypoint"] is True
    assert package_manifest_check["detail"]["readiness_matrix"]["mobile"]["smoke_entrypoint"] is True
    assert package_manifest_check["detail"]["readiness_matrix"]["desktop"]["smoke_entrypoint"] is True
    assert package_manifest_check["detail"]["readiness_matrix"]["pbc"]["handoff_contracts_present"] is True
    assert package_manifest_check["detail"]["readiness_matrix"]["deployment"]["topology_declared"] is True
    assert package_manifest_check["detail"]["release_evidence_report_count"] == 5
    assert package_manifest_check["detail"]["missing_release_report_count"] == 0
    assert package_manifest_check["detail"]["missing_release_reports"] == ()
    assert package_manifest_check["detail"]["release_report_formats_by_target"] == (
        package_manifest_check["detail"]["required_release_report_formats_by_target"]
    )
    assert package_manifest_check["detail"]["missing_release_report_format_target_count"] == 0
    assert package_manifest_check["detail"]["missing_release_report_format_targets"] == ()
    assert package_manifest_check["detail"]["release_report_kinds_by_target"] == {
        target: target
        for target in package_manifest_check["detail"]["expected_targets"]
    }
    assert package_manifest_check["detail"]["missing_release_report_kind_target_count"] == 0
    assert package_manifest_check["detail"]["missing_release_report_kind_targets"] == ()
    assert package_manifest_check["detail"]["release_report_ok_by_target"] == {
        target: True
        for target in package_manifest_check["detail"]["expected_targets"]
    }
    assert package_manifest_check["detail"]["failing_release_report_target_count"] == 0
    assert package_manifest_check["detail"]["failing_release_report_targets"] == ()
    assert package_manifest_check["detail"]["release_report_blocking_gap_counts_by_target"] == {
        target: 0
        for target in package_manifest_check["detail"]["expected_targets"]
    }
    assert package_manifest_check["detail"]["release_report_blocking_gap_target_count"] == 0
    assert package_manifest_check["detail"]["release_report_blocking_gap_targets"] == ()
    assert set(package_manifest_check["detail"]["release_evidence_reports"]) == {
        "web",
        "mobile",
        "desktop",
        "pbc",
        "deployment",
    }
    assert package_manifest_check["detail"]["release_graph_suite_format"] == "appgen.graph-suite-report.v1"
    assert package_manifest_check["detail"]["release_graph_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert package_manifest_check["detail"]["missing_release_graph_kind_count"] == 0
    assert package_manifest_check["detail"]["missing_release_graph_kinds"] == ()
    assert package_manifest_check["detail"]["release_graph_format_count"] == len(appgen_dsl.GRAPH_TEXT_FORMATS)
    assert package_manifest_check["detail"]["missing_release_graph_format_count"] == 0
    assert package_manifest_check["detail"]["missing_release_graph_formats"] == ()
    assert set(package_manifest_check["detail"]["release_graph_formats"]) == {"json", "mermaid", "dot"}
    assert package_manifest_check["detail"]["web"]["artifact_class"] == "web_application"
    assert package_manifest_check["detail"]["web"]["app_build_contract"] is True
    assert package_manifest_check["detail"]["web"]["forms_bind_valid_fields"] is True
    assert package_manifest_check["detail"]["mobile"]["artifact_class"] == "mobile_application"
    assert package_manifest_check["detail"]["mobile"]["signing_posture_declared"] is True
    assert package_manifest_check["detail"]["mobile"]["offline_policy_declared"] is True
    assert package_manifest_check["detail"]["desktop"]["artifact_class"] == "desktop_application"
    assert package_manifest_check["detail"]["desktop"]["installer_posture_declared"] is True
    assert package_manifest_check["detail"]["desktop"]["menus_bind_to_handlers"] is True
    assert package_manifest_check["detail"]["pbc"]["artifact_class"] == "packaged_business_capability"
    assert package_manifest_check["detail"]["pbc"]["side_effect_free_registration"] is True
    assert package_manifest_check["detail"]["deployment"]["artifact_class"] == "deployment_plan"
    assert package_manifest_check["detail"]["deployment"]["secret_values_absent"] is True
    assert package_manifest_check["detail"]["deployment"]["topology_graph_connected"] is True
    release_text_check = next(check for check in report["checks"] if check["id"] == "release_text_evidence_contracts")
    assert release_text_check["detail"]["format"] == "appgen.release-verifier-text-renderer.v1"
    assert release_text_check["detail"]["release_line_count"] == 2
    assert release_text_check["detail"]["graph_line_count"] == 3
    assert release_text_check["detail"]["target_status_line_count"] == 2
    assert release_text_check["detail"]["passing_target_line_count"] == 1
    assert release_text_check["detail"]["failing_target_line_count"] == 1
    assert release_text_check["detail"]["blocking_gap_line_count"] == 1
    assert release_text_check["detail"]["artifact_line_count"] == 2
    assert release_text_check["detail"]["missing_release_marker_count"] == 0
    assert release_text_check["detail"]["missing_graph_marker_count"] == 0
    assert release_text_check["detail"]["missing_target_status_count"] == 0
    assert release_text_check["detail"]["missing_blocking_gap_count"] == 0
    assert release_text_check["detail"]["missing_artifact_marker_count"] == 0
    assert release_text_check["detail"]["missing_text_surface_count"] == 0
    assert release_text_check["detail"]["missing_text_surfaces"] == ()
    assert release_text_check["detail"]["emitted_text_surfaces"] == (
        "release_summary",
        "release_evidence",
        "graph_suite",
        "graph_kinds",
        "graph_formats",
        "target_statuses",
        "blocking_gaps",
        "artifacts",
    )
    assert release_text_check["detail"]["missing_contract_format_count"] == 0
    assert release_text_check["detail"]["missing_contract_formats"] == ()
    assert release_text_check["detail"]["missing_graph_kind_count"] == 0
    assert release_text_check["detail"]["missing_graph_kinds"] == ()
    assert release_text_check["detail"]["missing_graph_format_count"] == 0
    assert release_text_check["detail"]["missing_graph_formats"] == ()
    assert release_text_check["detail"]["missing_target_outcome_count"] == 0
    assert release_text_check["detail"]["missing_target_outcomes"] == ()
    assert release_text_check["detail"]["missing_artifact_path_count"] == 0
    assert release_text_check["detail"]["missing_artifact_paths"] == ()
    assert release_text_check["detail"]["required_release_markers"] == ("release-verify", "release-evidence")
    assert release_text_check["detail"]["required_graph_markers"] == ("graph-suite", "graph-kinds", "graph-formats")
    assert release_text_check["detail"]["required_target_statuses"] == ("mobile", "desktop")
    assert release_text_check["detail"]["required_blocking_gaps"] == (
        "package_metadata_exists",
        "smoke_launch_not_declared",
    )
    assert release_text_check["detail"]["required_artifact_markers"] == (
        "release_evidence",
        "mobile_package_manifest",
    )
    assert release_text_check["detail"]["json_fallback"] is False
    pbc_publish_check = next(check for check in report["checks"] if check["id"] == "pbc_publish_side_effect_contracts")
    assert pbc_publish_check["detail"]["catalog"]["format"] == "appgen.pbc-verifier-catalog.v1"
    assert pbc_publish_check["detail"]["catalog"]["count"] > 0
    assert pbc_publish_check["detail"]["text_cli"]["format"] == "appgen.pbc-cli-text-audit.v1"
    assert pbc_publish_check["detail"]["text_cli"]["passing_case_count"] == pbc_publish_check["detail"]["text_cli"]["case_count"]
    assert pbc_publish_check["detail"]["text_cli"]["json_fallback_count"] == 0
    assert pbc_publish_check["detail"]["publish_cli"]["format"] == "appgen.pbc-publish-cli-audit.v1"
    assert pbc_publish_check["detail"]["publish_cli"]["passing_case_count"] == (
        pbc_publish_check["detail"]["publish_cli"]["case_count"]
    )
    assert pbc_publish_check["detail"]["publish_cli"]["payload_format"] == "appgen.pbc-publish-report.v1"
    assert pbc_publish_check["detail"]["publish_cli"]["pbc"] == "gl_core"
    assert pbc_publish_check["detail"]["publish_cli"]["target_mode"] == "file"
    assert pbc_publish_check["detail"]["publish_cli"]["side_effect_free"] is True
    assert pbc_publish_check["detail"]["publish_cli"]["write_performed"] is False
    assert pbc_publish_check["detail"]["publish_cli"]["catalog_patch_count"] >= 1
    assert pbc_publish_check["detail"]["publish_cli"]["release_evidence_format"] == "appgen.pbc-package-verifier.v1"
    assert pbc_publish_check["detail"]["publish_cli"]["release_evidence_ok"] is True
    assert pbc_publish_check["detail"]["publish_cli"]["passing_check_count"] == (
        pbc_publish_check["detail"]["publish_cli"]["check_count"]
    )
    assert pbc_publish_check["detail"]["publish_cli"]["blocking_gap_count"] == 0
    assert pbc_publish_check["detail"]["publish_cli"]["text_has_catalog_path"] is True
    assert pbc_publish_check["detail"]["publish_cli"]["text_has_side_effect_markers"] is True
    assert pbc_publish_check["detail"]["publish_cli"]["text_has_catalog_patch"] is True
    assert pbc_publish_check["detail"]["publish_cli"]["text_has_check_status"] is True
    assert pbc_publish_check["detail"]["publish_cli"]["text_json_fallback"] is False
    assert pbc_publish_check["detail"]["publish_text_renderer"]["format"] == "appgen.pbc-publish-text-renderer.v1"
    assert pbc_publish_check["detail"]["publish_text_renderer"]["summary_line_count"] == 1
    assert pbc_publish_check["detail"]["publish_text_renderer"]["catalog_path_line_count"] == 1
    assert pbc_publish_check["detail"]["publish_text_renderer"]["side_effect_line_count"] == 1
    assert pbc_publish_check["detail"]["publish_text_renderer"]["catalog_patch_line_count"] >= 1
    assert pbc_publish_check["detail"]["publish_text_renderer"]["passing_check_line_count"] >= 4
    assert pbc_publish_check["detail"]["publish_text_renderer"]["failing_check_line_count"] == 0
    assert pbc_publish_check["detail"]["publish_text_renderer"]["json_fallback"] is False
    migration_check = next(check for check in report["checks"] if check["id"] == "migration_detection_coverage")
    assert migration_check["detail"]["cli"]["format"] == "appgen.migration-cli-audit.v1"
    assert migration_check["detail"]["cli"]["ok"] is True
    assert migration_check["detail"]["cli"]["case_count"] == migration_check["detail"]["cli"]["allowed_backend_count"]
    assert migration_check["detail"]["cli"]["passing_case_count"] == migration_check["detail"]["cli"]["case_count"]
    assert migration_check["detail"]["cli"]["failing_case_count"] == 0
    assert migration_check["detail"]["cli"]["missing_allowed_backend_count"] == 0
    assert migration_check["detail"]["cli"]["change_kind_count"] >= 3
    assert migration_check["detail"]["cli"]["required_change_kind_count"] == 3
    assert migration_check["detail"]["cli"]["missing_required_change_kind_count"] == 0
    assert migration_check["detail"]["cli"]["approval_required_count"] == migration_check["detail"]["cli"]["case_count"]
    assert migration_check["detail"]["cli"]["rename_hint_case_count"] == migration_check["detail"]["cli"]["case_count"]
    assert migration_check["detail"]["semantic_input_cli"]["format"] == "appgen.migration-semantic-input-cli-audit.v1"
    assert migration_check["detail"]["semantic_input_cli"]["ok"] is True
    assert migration_check["detail"]["semantic_input_cli"]["semantic_input_count"] == 2
    assert migration_check["detail"]["semantic_input_cli"]["missing_source_file_count"] == 0
    assert migration_check["detail"]["semantic_input_cli"]["missing_change_kind_count"] == 0
    migration_safety_check = next(check for check in report["checks"] if check["id"] == "migration_safety_text_contracts")
    assert migration_safety_check["detail"]["required_detection_count"] == len(appgen_dsl.REQUIRED_MIGRATION_DETECTIONS)
    assert migration_safety_check["detail"]["detected_detection_count"] >= len(appgen_dsl.REQUIRED_MIGRATION_DETECTIONS)
    assert migration_safety_check["detail"]["missing_detections"] == ()
    assert migration_safety_check["detail"]["cli"]["format"] == "appgen.migration-cli-audit.v1"
    assert migration_safety_check["detail"]["cli"]["case_count"] == migration_safety_check["detail"]["cli"]["allowed_backend_count"]
    assert migration_safety_check["detail"]["cli"]["passing_case_count"] == migration_safety_check["detail"]["cli"]["case_count"]
    assert migration_safety_check["detail"]["cli"]["required_case_ids"] == tuple(
        f"{backend}_json_rename_hints" for backend in appgen_dsl.SUPPORTED_DATABASE_BACKENDS
    )
    assert migration_safety_check["detail"]["cli"]["observed_case_ids"] == migration_safety_check["detail"]["cli"][
        "required_case_ids"
    ]
    assert migration_safety_check["detail"]["cli"]["missing_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_case_ids"] == ()
    assert migration_safety_check["detail"]["cli"]["missing_allowed_backend_count"] == 0
    assert migration_safety_check["detail"]["cli"]["backends_by_case"] == migration_safety_check["detail"]["cli"][
        "expected_backends_by_case"
    ]
    assert migration_safety_check["detail"]["cli"]["missing_backend_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_backend_case_ids"] == ()
    assert migration_safety_check["detail"]["cli"]["change_kind_count"] >= 3
    assert migration_safety_check["detail"]["cli"]["missing_required_change_kind_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_change_kind_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_change_kinds_by_case"] == {}
    assert migration_safety_check["detail"]["cli"]["approval_required_cases"] == migration_safety_check["detail"]["cli"][
        "required_case_ids"
    ]
    assert migration_safety_check["detail"]["cli"]["missing_approval_required_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_approval_required_cases"] == ()
    assert migration_safety_check["detail"]["cli"]["exit_codes_by_case"] == migration_safety_check["detail"]["cli"][
        "expected_exit_codes_by_case"
    ]
    assert migration_safety_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert migration_safety_check["detail"]["cli"]["missing_destructive_change_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_destructive_change_cases"] == ()
    assert migration_safety_check["detail"]["cli"]["missing_safe_alternative_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_safe_alternative_cases"] == ()
    assert migration_safety_check["detail"]["semantic_input_cli"]["format"] == (
        "appgen.migration-semantic-input-cli-audit.v1"
    )
    assert migration_safety_check["detail"]["semantic_input_cli"]["ok"] is True
    assert migration_safety_check["detail"]["semantic_input_cli"]["previous_input_format"] == "appgen.semantic-model.v1"
    assert migration_safety_check["detail"]["semantic_input_cli"]["current_input_format"] == "appgen.semantic-model.v1"
    assert migration_safety_check["detail"]["semantic_input_cli"]["semantic_input_count"] == 2
    assert migration_safety_check["detail"]["semantic_input_cli"]["missing_source_file_count"] == 0
    assert migration_safety_check["detail"]["semantic_input_cli"]["missing_change_kind_count"] == 0
    assert migration_safety_check["detail"]["semantic_input_cli"]["missing_text_fragment_count"] == 0
    assert migration_safety_check["detail"]["semantic_input_cli"]["text_json_fallback"] is False
    assert migration_safety_check["detail"]["cli"]["required_diagnostic_codes_by_case"] == {
        case_id: ("AGX1101",)
        for case_id in migration_safety_check["detail"]["cli"]["required_case_ids"]
    }
    assert migration_safety_check["detail"]["cli"]["missing_diagnostic_code_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_diagnostic_codes_by_case"] == {}
    assert migration_safety_check["detail"]["cli"]["rename_hint_cases"] == migration_safety_check["detail"]["cli"][
        "required_case_ids"
    ]
    assert migration_safety_check["detail"]["cli"]["missing_rename_hint_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_rename_hint_cases"] == ()
    assert migration_safety_check["detail"]["cli"]["payload_formats_by_case"] == migration_safety_check["detail"][
        "cli"
    ]["expected_payload_formats_by_case"]
    assert migration_safety_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert migration_safety_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["format"] == "appgen.migration-plan-text-renderer.v1"
    assert migration_safety_check["detail"]["text_renderer"]["summary_line_count"] == 1
    assert migration_safety_check["detail"]["text_renderer"]["coverage_line_count"] == 1
    assert migration_safety_check["detail"]["text_renderer"]["change_line_count"] == 3
    assert migration_safety_check["detail"]["text_renderer"]["safe_alternative_line_count"] == 2
    assert migration_safety_check["detail"]["text_renderer"]["approval_line_count"] == 1
    assert migration_safety_check["detail"]["text_renderer"]["destructive_summary_line_count"] == 1
    assert migration_safety_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        "summary",
        "input_formats",
        "coverage",
        "detected_families",
        "missing_families",
        "changes",
        "safe_alternatives",
        "diagnostics",
        "approval_required",
        "destructive_summary",
    )
    assert migration_safety_check["detail"]["text_renderer"]["missing_detected_family_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_detected_families"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["missing_missing_family_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_missing_families"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["missing_change_target_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_change_targets"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["missing_safe_alternative_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_safe_alternatives"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["missing_diagnostic_code_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_diagnostic_codes"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["missing_contract_format_count"] == 0
    assert migration_safety_check["detail"]["text_renderer"]["missing_contract_formats"] == ()
    assert migration_safety_check["detail"]["text_renderer"]["json_fallback"] is False
    graph_check = next(check for check in report["checks"] if check["id"] == "graph_and_explain_tooling")
    assert graph_check["detail"]["cli"]["format"] == "appgen.graph-cli-format-audit.v1"
    assert graph_check["detail"]["cli"]["ok"] is True
    assert graph_check["detail"]["cli"]["case_count"] == 10
    assert graph_check["detail"]["cli"]["passing_case_count"] == 10
    assert graph_check["detail"]["cli"]["failing_case_count"] == 0
    assert graph_check["detail"]["cli"]["graph_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert graph_check["detail"]["cli"]["missing_required_kind_count"] == 0
    assert graph_check["detail"]["cli"]["output_format_count"] == 3
    assert {
        "er_mermaid",
        "lookup_json",
        "workflow_json",
        "workflow_mermaid",
        "handler_mermaid",
        "pbc_dot",
        "security_dot",
        "agent_json",
        "deployment_dot",
        "package_mermaid",
    } <= {case["case"] for case in graph_check["detail"]["cli"]["cases"]}
    assert graph_check["detail"]["suite_cli"]["format"] == "appgen.graph-suite-cli-audit.v1"
    assert graph_check["detail"]["suite_cli"]["ok"] is True
    assert graph_check["detail"]["suite_cli"]["required_kind_count"] == len(graph_check["detail"]["suite_cli"]["required_kinds"])
    assert graph_check["detail"]["suite_cli"]["missing_required_kind_count"] == 0
    assert graph_check["detail"]["suite_cli"]["output_format_count"] == len(graph_check["detail"]["suite_cli"]["formats"])
    assert graph_check["detail"]["suite_cli"]["missing_rendering_count"] == 0
    assert graph_check["detail"]["suite_cli"]["missing_text_fragment_count"] == 0
    assert set(graph_check["detail"]["suite_cli"]["required_kinds"]) >= {
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
    assert tuple(graph_check["detail"]["suite_cli"]["formats"]) == ("json", "mermaid", "dot")
    assert graph_check["detail"]["suite_cli"]["rendering_kind_count"] == 9
    assert graph_check["detail"]["suite_cli"]["missing_renderings"] == ()
    assert all(
        set(formats) == {"json", "mermaid", "dot"}
        for formats in graph_check["detail"]["suite_cli"]["rendering_formats_by_kind"].values()
    )
    assert graph_check["detail"]["suite_cli"]["text_has_report_format"] is True
    assert graph_check["detail"]["suite_cli"]["text_has_kinds"] is True
    assert graph_check["detail"]["suite_cli"]["text_has_formats"] is True
    assert graph_check["detail"]["explain_cli"]["format"] == "appgen.explain-cli-audit.v1"
    assert graph_check["detail"]["explain_cli"]["ok"] is True
    assert all(case["has_report_format"] is True for case in graph_check["detail"]["explain_cli"]["cases"])
    explain_cases = {case["case"]: case for case in graph_check["detail"]["explain_cli"]["cases"]}
    assert explain_cases["field_symbol_json"]["symbol_id"] == "table.Invoice.customer_id"
    assert explain_cases["diagnostic_json"]["diagnostic_docs_url"] == "docs/tooling.md#diagnostic-specification"
    assert explain_cases["qualified_handler_json"]["handler_edges"] == ("InvoiceForm.Save->SubmitInvoice",)
    assert {
        "field_symbol_text",
        "field_symbol_json",
        "diagnostic_json",
        "qualified_handler_text",
        "qualified_handler_json",
    } <= {case["case"] for case in graph_check["detail"]["explain_cli"]["cases"]}
    graph_rendering_check = next(check for check in report["checks"] if check["id"] == "graph_rendering_contracts")
    assert graph_rendering_check["detail"]["suite_format"] == "appgen.graph-suite-report.v1"
    assert graph_rendering_check["detail"]["required_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert graph_rendering_check["detail"]["missing_kind_count"] == 0
    assert graph_rendering_check["detail"]["missing_rendering_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["format"] == "appgen.graph-cli-format-audit.v1"
    assert graph_rendering_check["detail"]["cli"]["case_count"] == 10
    assert graph_rendering_check["detail"]["cli"]["failing_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["required_case_ids"] == (
        "er_mermaid",
        "lookup_json",
        "workflow_json",
        "workflow_mermaid",
        "handler_mermaid",
        "pbc_dot",
        "security_dot",
        "agent_json",
        "deployment_dot",
        "package_mermaid",
    )
    assert graph_rendering_check["detail"]["cli"]["observed_case_ids"] == graph_rendering_check["detail"]["cli"][
        "required_case_ids"
    ]
    assert graph_rendering_check["detail"]["cli"]["missing_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["missing_case_ids"] == ()
    assert graph_rendering_check["detail"]["cli"]["exit_codes_by_case"] == (
        graph_rendering_check["detail"]["cli"]["expected_exit_codes_by_case"]
    )
    assert graph_rendering_check["detail"]["cli"]["missing_exit_code_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["missing_exit_code_cases"] == ()
    assert graph_rendering_check["detail"]["cli"]["ok_by_case"] == {
        "er_mermaid": True,
        "lookup_json": True,
        "workflow_json": True,
        "workflow_mermaid": True,
        "handler_mermaid": True,
        "pbc_dot": True,
        "security_dot": True,
        "agent_json": True,
        "deployment_dot": True,
        "package_mermaid": True,
    }
    assert graph_rendering_check["detail"]["cli"]["missing_ok_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["missing_ok_cases"] == ()
    assert graph_rendering_check["detail"]["cli"]["formats_by_case"] == graph_rendering_check["detail"]["cli"][
        "expected_formats_by_case"
    ]
    assert graph_rendering_check["detail"]["cli"]["missing_format_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["missing_format_cases"] == ()
    assert graph_rendering_check["detail"]["cli"]["graph_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert graph_rendering_check["detail"]["cli"]["missing_required_kind_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["payload_format_case_count"] == graph_rendering_check["detail"]["cli"]["json_case_count"]
    assert graph_rendering_check["detail"]["cli"]["payload_formats_by_case"] == graph_rendering_check["detail"]["cli"][
        "expected_payload_formats_by_case"
    ]
    assert graph_rendering_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert graph_rendering_check["detail"]["cli"]["text_marker_case_count"] == (
        graph_rendering_check["detail"]["cli"]["mermaid_case_count"] + graph_rendering_check["detail"]["cli"]["dot_case_count"]
    )
    assert graph_rendering_check["detail"]["cli"]["required_text_markers_by_case"]["package_mermaid"] == "graph TD"
    assert graph_rendering_check["detail"]["cli"]["required_text_markers_by_case"]["security_dot"] == "digraph appgen"
    assert graph_rendering_check["detail"]["cli"]["missing_text_marker_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["missing_text_marker_cases"] == ()
    assert graph_rendering_check["detail"]["cli"]["missing_text_markers_by_case"] == {}
    assert graph_rendering_check["detail"]["cli"]["text_json_fallback_case_count"] == 0
    assert graph_rendering_check["detail"]["cli"]["text_json_fallback_cases"] == ()
    assert all(value is False for value in graph_rendering_check["detail"]["cli"]["text_json_fallback_by_case"].values())
    assert graph_rendering_check["detail"]["suite_cli"]["format"] == "appgen.graph-suite-cli-audit.v1"
    assert graph_rendering_check["detail"]["suite_cli"]["case_count"] == 2
    assert graph_rendering_check["detail"]["suite_cli"]["passing_case_count"] == 2
    assert graph_rendering_check["detail"]["suite_cli"]["failing_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["failing_cases"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["observed_case_ids"] == (
        graph_rendering_check["detail"]["suite_cli"]["required_case_ids"]
    )
    assert graph_rendering_check["detail"]["suite_cli"]["missing_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_case_ids"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["modes_by_case"] == (
        graph_rendering_check["detail"]["suite_cli"]["expected_modes_by_case"]
    )
    assert graph_rendering_check["detail"]["suite_cli"]["missing_mode_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_mode_cases"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["exit_codes_by_case"] == (
        graph_rendering_check["detail"]["suite_cli"]["expected_exit_codes_by_case"]
    )
    assert graph_rendering_check["detail"]["suite_cli"]["missing_exit_code_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_exit_code_cases"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["ok_by_case"] == {
        "graph_suite_json": True,
        "graph_suite_text": True,
    }
    assert graph_rendering_check["detail"]["suite_cli"]["missing_ok_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_ok_cases"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["payload_formats_by_case"] == (
        graph_rendering_check["detail"]["suite_cli"]["expected_payload_formats_by_case"]
    )
    assert graph_rendering_check["detail"]["suite_cli"]["missing_payload_format_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_payload_format_cases"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["text_json_fallback_by_case"] == {"graph_suite_text": False}
    assert graph_rendering_check["detail"]["suite_cli"]["text_json_fallback_case_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["text_json_fallback_cases"] == ()
    assert graph_rendering_check["detail"]["suite_cli"]["missing_required_kind_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["present_rendering_count"] == (
        graph_rendering_check["detail"]["suite_cli"]["expected_rendering_count"]
    )
    assert graph_rendering_check["detail"]["suite_cli"]["complete_rendering_kind_count"] == len(
        appgen_dsl.REQUIRED_GRAPH_KINDS
    )
    assert graph_rendering_check["detail"]["suite_cli"]["missing_rendering_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_format_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["missing_text_fragment_count"] == 0
    assert graph_rendering_check["detail"]["suite_cli"]["text_fragment_ids"] == (
        "summary_format",
        "graph_kinds",
        "graph_formats",
    )
    assert graph_rendering_check["detail"]["suite_cli"]["rendering_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    explain_contract_check = next(check for check in report["checks"] if check["id"] == "explain_cli_contracts")
    assert explain_contract_check["detail"]["format"] == "appgen.explain-cli-audit.v1"
    assert explain_contract_check["detail"]["case_count"] == 6
    assert explain_contract_check["detail"]["passing_case_count"] == 6
    assert explain_contract_check["detail"]["failing_case_count"] == 0
    assert explain_contract_check["detail"]["failing_cases"] == ()
    assert explain_contract_check["detail"]["case_ids"] == (
        "field_symbol_text",
        "field_symbol_json",
        "diagnostic_text",
        "diagnostic_json",
        "qualified_handler_text",
        "qualified_handler_json",
    )
    assert explain_contract_check["detail"]["required_case_ids"] == explain_contract_check["detail"]["case_ids"]
    assert explain_contract_check["detail"]["observed_case_ids"] == explain_contract_check["detail"]["case_ids"]
    assert explain_contract_check["detail"]["missing_case_count"] == 0
    assert explain_contract_check["detail"]["missing_case_ids"] == ()
    assert explain_contract_check["detail"]["output_modes_by_case"] == explain_contract_check["detail"][
        "expected_output_modes_by_case"
    ]
    assert explain_contract_check["detail"]["missing_output_mode_case_count"] == 0
    assert explain_contract_check["detail"]["missing_output_mode_cases"] == ()
    assert explain_contract_check["detail"]["exit_codes_by_case"] == explain_contract_check["detail"][
        "expected_exit_codes_by_case"
    ]
    assert explain_contract_check["detail"]["missing_exit_code_case_count"] == 0
    assert explain_contract_check["detail"]["missing_exit_code_cases"] == ()
    assert explain_contract_check["detail"]["ok_by_case"] == {
        "field_symbol_text": True,
        "field_symbol_json": True,
        "diagnostic_text": True,
        "diagnostic_json": True,
        "qualified_handler_text": True,
        "qualified_handler_json": True,
    }
    assert explain_contract_check["detail"]["missing_ok_case_count"] == 0
    assert explain_contract_check["detail"]["missing_ok_cases"] == ()
    assert explain_contract_check["detail"]["payload_formats_by_case"] == explain_contract_check["detail"][
        "expected_payload_formats_by_case"
    ]
    assert explain_contract_check["detail"]["missing_payload_format_case_count"] == 0
    assert explain_contract_check["detail"]["missing_payload_format_cases"] == ()
    assert explain_contract_check["detail"]["exit_failure_count"] == 0
    assert explain_contract_check["detail"]["text_case_count"] == 3
    assert explain_contract_check["detail"]["json_case_count"] == 3
    assert explain_contract_check["detail"]["missing_report_format_count"] == 0
    assert explain_contract_check["detail"]["required_report_format_cases"] == explain_contract_check["detail"][
        "case_ids"
    ]
    assert explain_contract_check["detail"]["report_format_cases"] == explain_contract_check["detail"]["case_ids"]
    assert explain_contract_check["detail"]["missing_report_format_cases"] == ()
    assert explain_contract_check["detail"]["text_report_format_case_count"] == 3
    assert explain_contract_check["detail"]["json_report_format_case_count"] == 3
    assert explain_contract_check["detail"]["required_text_markers_by_case"]["field_symbol_text"].startswith(
        "explain symbol ok: format=appgen.explain-report.v1"
    )
    assert explain_contract_check["detail"]["missing_text_marker_count"] == 0
    assert explain_contract_check["detail"]["missing_text_marker_cases"] == ()
    assert explain_contract_check["detail"]["missing_text_markers_by_case"] == {}
    assert explain_contract_check["detail"]["text_json_fallback_case_count"] == 0
    assert explain_contract_check["detail"]["text_json_fallback_cases"] == ()
    assert all(value is False for value in explain_contract_check["detail"]["text_json_fallback_by_case"].values())
    assert explain_contract_check["detail"]["navigation_detail_case_count"] == 3
    assert explain_contract_check["detail"]["navigation_detail_cases"] == (
        "field_symbol_json",
        "diagnostic_json",
        "qualified_handler_json",
    )
    assert explain_contract_check["detail"]["required_navigation_detail_cases"] == explain_contract_check["detail"][
        "navigation_detail_cases"
    ]
    assert explain_contract_check["detail"]["missing_navigation_detail_case_count"] == 0
    assert explain_contract_check["detail"]["missing_navigation_detail_cases"] == ()
    assert explain_contract_check["detail"]["symbol_navigation_detail_count"] == 1
    assert explain_contract_check["detail"]["diagnostic_navigation_detail_count"] == 1
    assert explain_contract_check["detail"]["handler_navigation_detail_count"] == 1
    assert explain_contract_check["detail"]["symbol_case_count"] == 2
    assert explain_contract_check["detail"]["diagnostic_case_count"] == 2
    assert explain_contract_check["detail"]["handler_case_count"] == 2
    assert explain_contract_check["detail"]["text_renderer"]["format"] == "appgen.graph-explain-text-renderer.v1"
    assert explain_contract_check["detail"]["text_renderer"]["missing_fragment_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["emitted_graph_kinds"] == (
        explain_contract_check["detail"]["text_renderer"]["required_graph_kinds"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_graph_kind_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_graph_kinds"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_graph_formats"] == (
        explain_contract_check["detail"]["text_renderer"]["required_graph_formats"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_graph_format_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_graph_formats"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_check_ids"] == (
        explain_contract_check["detail"]["text_renderer"]["required_check_ids"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_check_id_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_check_ids"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_explain_kinds"] == (
        explain_contract_check["detail"]["text_renderer"]["required_explain_kinds"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_explain_kind_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_explain_kinds"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_symbol_ids"] == (
        explain_contract_check["detail"]["text_renderer"]["required_symbol_ids"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_symbol_id_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_symbol_ids"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_diagnostic_codes"] == (
        explain_contract_check["detail"]["text_renderer"]["required_diagnostic_codes"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_diagnostic_code_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_diagnostic_codes"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_docs_urls"] == (
        explain_contract_check["detail"]["text_renderer"]["required_docs_urls"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_docs_url_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_docs_urls"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_handler_edges"] == (
        explain_contract_check["detail"]["text_renderer"]["required_handler_edges"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_handler_edge_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_handler_edges"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_text_surfaces"] == (
        explain_contract_check["detail"]["text_renderer"]["required_text_surfaces"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_text_surface_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_text_surfaces"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_report_formats"] == (
        explain_contract_check["detail"]["text_renderer"]["required_report_formats"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_report_format_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_report_formats"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_reference_counts"] == (
        explain_contract_check["detail"]["text_renderer"]["required_reference_counts"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_reference_count_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_reference_counts"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["emitted_match_counts"] == (
        explain_contract_check["detail"]["text_renderer"]["required_match_counts"]
    )
    assert explain_contract_check["detail"]["text_renderer"]["missing_match_count_count"] == 0
    assert explain_contract_check["detail"]["text_renderer"]["missing_match_counts"] == ()
    assert explain_contract_check["detail"]["text_renderer"]["json_fallback"] is False
    nl_check = next(check for check in report["checks"] if check["id"] == "natural_language_patch_planner")
    assert nl_check["detail"]["cli"]["format"] == "appgen.nl-plan-cli-audit.v1"
    assert nl_check["detail"]["cli"]["ok"] is True
    assert nl_check["detail"]["contract"]["case_count"] == len(nl_check["detail"]["contract"]["cases"])
    assert nl_check["detail"]["contract"]["passing_case_count"] == nl_check["detail"]["contract"]["case_count"]
    assert nl_check["detail"]["contract"]["accepted_case_count"] == len(
        nl_check["detail"]["contract"]["required_edit_operations"]
    )
    assert nl_check["detail"]["contract"]["rejected_case_count"] == 1
    assert nl_check["detail"]["contract"]["required_operation_count"] == len(
        nl_check["detail"]["contract"]["required_edit_operations"]
    )
    assert nl_check["detail"]["contract"]["observed_operation_kind_count"] >= (
        nl_check["detail"]["contract"]["required_operation_count"]
    )
    assert nl_check["detail"]["contract"]["token_budget_case_count"] == nl_check["detail"]["contract"]["case_count"]
    assert nl_check["detail"]["cli"]["case_count"] == (
        nl_check["detail"]["cli"]["accepted_case_count"]
        + nl_check["detail"]["cli"]["rejected_case_count"]
        + nl_check["detail"]["cli"]["text_case_count"]
    )
    assert nl_check["detail"]["cli"]["accepted_passing_case_count"] == nl_check["detail"]["cli"]["accepted_case_count"]
    assert nl_check["detail"]["cli"]["accepted_failing_case_count"] == 0
    assert nl_check["detail"]["cli"]["accepted_operation_kind_count"] == len(
        nl_check["detail"]["cli"]["accepted_operation_kinds"]
    )
    assert tuple(nl_check["detail"]["cli"]["required_operation_kinds"]) == tuple(
        nl_check["detail"]["contract"]["required_edit_operations"]
    )
    assert nl_check["detail"]["cli"]["required_accepted_case_ids"] == tuple(
        f"{kind}_json" for kind in nl_check["detail"]["contract"]["required_edit_operations"]
    )
    assert nl_check["detail"]["cli"]["observed_accepted_case_ids"] == nl_check["detail"]["cli"][
        "required_accepted_case_ids"
    ]
    assert nl_check["detail"]["cli"]["missing_accepted_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_accepted_case_ids"] == ()
    assert nl_check["detail"]["cli"]["missing_expected_operation_kind_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_expected_operation_kind_cases"] == ()
    assert set(nl_check["detail"]["cli"]["accepted_operation_kinds"]) >= set(
        nl_check["detail"]["contract"]["required_edit_operations"]
    )
    assert nl_check["detail"]["cli"]["missing_accepted_operation_kind_count"] == 0
    assert nl_check["detail"]["cli"]["missing_accepted_operation_kinds"] == ()
    assert nl_check["detail"]["cli"]["payload_formats_by_case"] == nl_check["detail"]["cli"][
        "expected_payload_formats_by_case"
    ]
    assert nl_check["detail"]["cli"]["missing_payload_format_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_payload_format_cases"] == ()
    assert nl_check["detail"]["cli"]["lint_ok_cases"] == nl_check["detail"]["cli"]["required_accepted_case_ids"]
    assert nl_check["detail"]["cli"]["missing_lint_ok_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_lint_ok_cases"] == ()
    assert nl_check["detail"]["cli"]["migration_format_cases"] == nl_check["detail"]["cli"][
        "required_accepted_case_ids"
    ]
    assert nl_check["detail"]["cli"]["missing_migration_format_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_migration_format_cases"] == ()
    assert nl_check["detail"]["cli"]["test_plan_cases"] == nl_check["detail"]["cli"]["required_accepted_case_ids"]
    assert nl_check["detail"]["cli"]["missing_test_plan_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_test_plan_cases"] == ()
    assert nl_check["detail"]["cli"]["token_budget_cases"] == nl_check["detail"]["cli"]["required_accepted_case_ids"]
    assert nl_check["detail"]["cli"]["missing_token_budget_case_count"] == 0
    assert nl_check["detail"]["cli"]["missing_token_budget_cases"] == ()
    assert nl_check["detail"]["cli"]["accepted_case_count"] == len(nl_check["detail"]["contract"]["required_edit_operations"])
    assert nl_check["detail"]["cli"]["blocking_cases"] == ()
    assert nl_check["detail"]["cli"]["blocking_case_count"] == 0
    assert nl_check["detail"]["cli"]["accepted_patch_bytes"] > 0
    assert nl_check["detail"]["cli"]["migration_format"] == "appgen.migration-plan.v1"
    assert nl_check["detail"]["cli"]["accepted_test_count"] > 0
    assert nl_check["detail"]["cli"]["accepted_token_budget_notes"] > 0
    assert "AGX1201" in nl_check["detail"]["cli"]["rejected_diagnostic_codes"]
    nl_operation_check = next(check for check in report["checks"] if check["id"] == "natural_language_operation_contracts")
    assert nl_operation_check["detail"]["format"] == "appgen.nl-plan-contract-audit.v1"
    assert nl_operation_check["detail"]["passing_case_count"] == nl_operation_check["detail"]["case_count"]
    assert nl_operation_check["detail"]["accepted_case_count"] == nl_operation_check["detail"]["required_operation_count"]
    assert nl_operation_check["detail"]["accepted_case_count"] == len(
        nl_operation_check["detail"]["required_edit_operations"]
    )
    assert nl_operation_check["detail"]["rejected_case_count"] == 1
    assert set(nl_operation_check["detail"]["observed_operation_kinds"]) >= set(
        nl_operation_check["detail"]["required_edit_operations"]
    )
    assert nl_operation_check["detail"]["observed_operation_kind_count"] >= (
        nl_operation_check["detail"]["required_operation_count"]
    )
    assert nl_operation_check["detail"]["observed_operation_kind_count"] == len(
        nl_operation_check["detail"]["observed_operation_kinds"]
    )
    assert nl_operation_check["detail"]["missing_required_operation_kinds"] == ()
    assert nl_operation_check["detail"]["missing_required_operation_kind_count"] == 0
    assert nl_operation_check["detail"]["token_budget_case_count"] == nl_operation_check["detail"]["case_count"]
    assert nl_operation_check["detail"]["blocking_gap_count"] == 0
    assert nl_operation_check["detail"]["blocking_gaps"] == ()
    nl_cli_agent_check = next(check for check in report["checks"] if check["id"] == "natural_language_cli_agent_contracts")
    assert nl_cli_agent_check["detail"]["format"] == "appgen.nl-plan-cli-audit.v1"
    assert nl_cli_agent_check["detail"]["accepted_case_count"] == nl_operation_check["detail"]["required_operation_count"]
    assert nl_cli_agent_check["detail"]["accepted_passing_case_count"] == (
        nl_cli_agent_check["detail"]["accepted_case_count"]
    )
    assert nl_cli_agent_check["detail"]["accepted_failing_case_count"] == 0
    assert nl_cli_agent_check["detail"]["accepted_operation_kind_count"] >= (
        nl_operation_check["detail"]["required_operation_count"]
    )
    assert nl_cli_agent_check["detail"]["missing_accepted_operation_kind_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_accepted_operation_kinds"] == ()
    assert nl_cli_agent_check["detail"]["missing_accepted_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_expected_operation_kind_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_payload_format_case_count"] == 0
    assert nl_cli_agent_check["detail"]["exit_codes_by_case"] == nl_cli_agent_check["detail"][
        "expected_exit_codes_by_case"
    ]
    assert nl_cli_agent_check["detail"]["missing_exit_code_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_exit_code_cases"] == ()
    assert nl_cli_agent_check["detail"]["ok_cases"] == nl_cli_agent_check["detail"]["required_accepted_case_ids"]
    assert nl_cli_agent_check["detail"]["missing_ok_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_ok_cases"] == ()
    assert nl_cli_agent_check["detail"]["missing_lint_ok_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_migration_format_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_test_plan_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_token_budget_case_count"] == 0
    assert nl_cli_agent_check["detail"]["accepted_patch_bytes"] > 0
    assert nl_cli_agent_check["detail"]["accepted_test_count"] >= nl_cli_agent_check["detail"]["accepted_case_count"]
    assert nl_cli_agent_check["detail"]["accepted_token_budget_notes"] >= (
        nl_cli_agent_check["detail"]["accepted_case_count"]
    )
    assert nl_cli_agent_check["detail"]["migration_format"] == "appgen.migration-plan.v1"
    assert nl_cli_agent_check["detail"]["accepted_text_marker_count"] >= 6
    assert nl_cli_agent_check["detail"]["missing_text_marker_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_text_markers"] == ()
    assert nl_cli_agent_check["detail"]["accepted_text_has_report_format"] is True
    assert nl_cli_agent_check["detail"]["accepted_text_has_lint_format"] is True
    assert nl_cli_agent_check["detail"]["accepted_text_has_migration_format"] is True
    assert nl_cli_agent_check["detail"]["accepted_text_test_plan_line_count"] > 0
    assert nl_cli_agent_check["detail"]["accepted_text_has_token_notes"] is True
    assert nl_cli_agent_check["detail"]["accepted_text_token_note_line_count"] > 0
    assert nl_cli_agent_check["detail"]["rejected_ok"] is True
    assert nl_cli_agent_check["detail"]["rejected_case_id"] == "reject_out_of_dsl_generated_code"
    assert nl_cli_agent_check["detail"]["rejected_exit_codes_by_case"] == nl_cli_agent_check["detail"][
        "expected_rejected_exit_codes_by_case"
    ]
    assert nl_cli_agent_check["detail"]["missing_rejected_exit_code_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_rejected_exit_code_cases"] == ()
    assert nl_cli_agent_check["detail"]["rejected_payload_formats_by_case"] == nl_cli_agent_check["detail"][
        "expected_rejected_payload_formats_by_case"
    ]
    assert nl_cli_agent_check["detail"]["missing_rejected_payload_format_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_rejected_payload_format_cases"] == ()
    assert nl_cli_agent_check["detail"]["required_rejected_diagnostic_codes_by_case"] == {
        "reject_out_of_dsl_generated_code": ("AGX1201",)
    }
    assert nl_cli_agent_check["detail"]["missing_rejected_diagnostic_code_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_rejected_diagnostic_codes_by_case"] == {}
    assert nl_cli_agent_check["detail"]["rejected_patch_empty_cases"] == ("reject_out_of_dsl_generated_code",)
    assert nl_cli_agent_check["detail"]["missing_rejected_patch_empty_case_count"] == 0
    assert nl_cli_agent_check["detail"]["missing_rejected_patch_empty_cases"] == ()
    assert "AGX1201" in nl_cli_agent_check["detail"]["rejected_diagnostic_codes"]
    assert nl_cli_agent_check["detail"]["blocking_case_count"] == 0
    assert nl_cli_agent_check["detail"]["blocking_cases"] == ()
    assert all(check["section"].startswith("docs/tooling.md#") for check in report["checks"])
    assert cli_json.returncode == 0, cli_json.stderr
    assert json.loads(cli_json.stdout)["format"] == "appgen.tooling-audit.v1"
    assert cli_text.returncode == 0, cli_text.stderr
    assert cli_text.stdout.startswith("tooling-audit ok:")
    assert "blocking_gaps=0 sections=" in cli_text.stdout
    assert "source=docs/tooling.md" in cli_text.stdout
    assert "section docs/tooling.md#language-server-specification" in cli_text.stdout
    assert "section docs/tooling.md#package-and-verifier-tooling" in cli_text.stdout
    assert "formats=appgen.cli-alias-contract.v1" in cli_text.stdout
    assert "appgen.lsp-json-rpc-audit.v1" in cli_text.stdout
    assert "appgen.lsp-code-action-cli-audit.v1" in cli_text.stdout
    assert "appgen.designer-sync-cli-audit.v1" in cli_text.stdout
    assert "appgen.studio-semantic-service-audit.v1" in cli_text.stdout
    assert "appgen.tooling-implementation-phase-audit.v1" in cli_text.stdout


def test_tooling_audit_text_renderer_contract_proves_human_log_markers() -> None:
    report = appgen_dsl._tooling_audit_text_renderer_contract()

    assert report["format"] == "appgen.tooling-audit-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 20
    assert report["check_line_count"] == 10
    assert report["passing_check_line_count"] == 10
    assert report["failing_check_line_count"] == 0
    assert report["detail_format_line_count"] >= 5
    assert report["section_line_count"] >= 4
    assert report["blocking_gap_line_count"] == 1
    assert report["implementation_phase_line_count"] == 2
    assert report["missing_fragments"] == ()
    assert report["missing_check_id_count"] == 0
    assert report["missing_check_ids"] == ()
    assert set(report["required_check_ids"]) <= set(report["emitted_check_ids"])
    assert "tooling_doc_anchor_integrity" in report["emitted_check_ids"]
    assert report["missing_section_count"] == 0
    assert report["missing_sections"] == ()
    assert set(report["required_sections"]) <= set(report["emitted_sections"])
    assert "docs/tooling.md#appgen-tooling-audit" in report["emitted_sections"]
    assert report["missing_detail_format_count"] == 0
    assert report["missing_detail_formats"] == ()
    assert set(report["required_detail_formats"]) <= set(report["emitted_detail_formats"])
    assert "appgen.tooling-doc-anchor-audit.v1" in report["emitted_detail_formats"]
    assert report["missing_blocking_gap_id_count"] == 0
    assert report["missing_blocking_gap_ids"] == ()
    assert report["required_blocking_gap_ids"] == ("studio_semantic_service",)
    assert "studio_semantic_service" in report["emitted_blocking_gap_ids"]
    assert report["required_text_surfaces"] == (
        "success_summary",
        "failure_summary",
        "source",
        "sections",
        "check_statuses",
        "detail_formats",
        "blocking_gaps",
        "implementation_phases",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_status_markers"] == (
        "tooling-audit ok",
        "tooling-audit failed",
        "blocking_gaps=0",
    )
    assert report["emitted_status_markers"] == report["required_status_markers"]
    assert report["missing_status_marker_count"] == 0
    assert report["missing_status_markers"] == ()
    assert report["required_top_level_formats"] == ("appgen.tooling-audit.v1",)
    assert report["emitted_top_level_formats"] == report["required_top_level_formats"]
    assert report["missing_top_level_format_count"] == 0
    assert report["missing_top_level_formats"] == ()
    assert report["required_source_documents"] == ("docs/tooling.md",)
    assert report["emitted_source_documents"] == report["required_source_documents"]
    assert report["missing_source_document_count"] == 0
    assert report["missing_source_documents"] == ()
    assert report["required_implementation_phase_markers"] == (
        "format=appgen.tooling-implementation-phase-audit.v1",
        "criteria=3/3",
        "missing_criteria=0",
    )
    assert report["emitted_implementation_phase_markers"] == report["required_implementation_phase_markers"]
    assert report["missing_implementation_phase_marker_count"] == 0
    assert report["missing_implementation_phase_markers"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith("tooling-audit ok: format=appgen.tooling-audit.v1")
    assert {
        "tooling-audit failed: format=appgen.tooling-audit.v1",
        "blocking-gap studio_semantic_service section=docs/tooling.md#appgen-x-studio-monaco",
        "formats=appgen.cli-help-surface-audit.v1",
        "formats=appgen.lsp-json-rpc-audit.v1",
        "formats=appgen.non-goal-policy-audit.v1",
        "formats=appgen.tooling-doc-anchor-audit.v1",
        "implementation-phases 1 missing=0 format=appgen.tooling-implementation-phase-audit.v1 criteria=3/3 missing_criteria=0",
    } <= set(report["required_fragments"])


def test_release_verifier_text_renderer_contract_proves_handoff_log_markers() -> None:
    report = appgen_dsl._release_verifier_text_renderer_contract()

    assert report["format"] == "appgen.release-verifier-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 9
    assert report["release_line_count"] == 2
    assert report["graph_line_count"] == 3
    assert report["target_status_line_count"] == 2
    assert report["passing_target_line_count"] == 1
    assert report["failing_target_line_count"] == 1
    assert report["blocking_gap_line_count"] == 1
    assert report["artifact_line_count"] == 2
    assert report["missing_fragments"] == ()
    assert report["missing_release_marker_count"] == 0
    assert report["missing_release_markers"] == ()
    assert report["required_release_markers"] == ("release-verify", "release-evidence")
    assert set(report["required_release_markers"]) <= set(report["emitted_release_markers"])
    assert report["missing_graph_marker_count"] == 0
    assert report["missing_graph_markers"] == ()
    assert report["required_graph_markers"] == ("graph-suite", "graph-kinds", "graph-formats")
    assert set(report["required_graph_markers"]) <= set(report["emitted_graph_markers"])
    assert report["missing_target_status_count"] == 0
    assert report["missing_target_statuses"] == ()
    assert report["required_target_statuses"] == ("mobile", "desktop")
    assert set(report["required_target_statuses"]) <= set(report["emitted_target_statuses"])
    assert report["missing_blocking_gap_count"] == 0
    assert report["missing_blocking_gaps"] == ()
    assert report["required_blocking_gaps"] == ("package_metadata_exists", "smoke_launch_not_declared")
    assert set(report["required_blocking_gaps"]) <= set(report["emitted_blocking_gaps"])
    assert report["missing_artifact_marker_count"] == 0
    assert report["missing_artifact_markers"] == ()
    assert report["required_artifact_markers"] == ("release_evidence", "mobile_package_manifest")
    assert set(report["required_artifact_markers"]) <= set(report["emitted_artifact_markers"])
    assert report["required_text_surfaces"] == (
        "release_summary",
        "release_evidence",
        "graph_suite",
        "graph_kinds",
        "graph_formats",
        "target_statuses",
        "blocking_gaps",
        "artifacts",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == (
        "appgen.release-verifier-report.v1",
        "appgen.release-evidence-bundle.v1",
        "appgen.graph-suite-report.v1",
    )
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_graph_kinds"] == ("workflow", "package")
    assert report["emitted_graph_kinds"] == report["required_graph_kinds"]
    assert report["missing_graph_kind_count"] == 0
    assert report["missing_graph_kinds"] == ()
    assert report["required_graph_formats"] == ("json", "mermaid", "dot")
    assert report["emitted_graph_formats"] == report["required_graph_formats"]
    assert report["missing_graph_format_count"] == 0
    assert report["missing_graph_formats"] == ()
    assert report["required_target_outcomes"] == ("mobile:fail", "desktop:ok")
    assert report["emitted_target_outcomes"] == report["required_target_outcomes"]
    assert report["missing_target_outcome_count"] == 0
    assert report["missing_target_outcomes"] == ()
    assert report["required_artifact_paths"] == (
        "dist/appgen-release-evidence.json",
        "dist/appgen-package-mobile.json",
    )
    assert report["emitted_artifact_paths"] == report["required_artifact_paths"]
    assert report["missing_artifact_path_count"] == 0
    assert report["missing_artifact_paths"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "release-verify failed: format=appgen.release-verifier-report.v1 targets=mobile,desktop"
    )
    assert {
        "release-evidence format=appgen.release-evidence-bundle.v1: artifacts=1",
        "graph-suite format=appgen.graph-suite-report.v1: kinds=2 formats=3",
        "graph-kinds workflow, package",
        "graph-formats json, mermaid, dot",
        "fail mobile gaps=package_metadata_exists,smoke_launch_not_declared",
        "artifact mobile_package_manifest: dist/appgen-package-mobile.json",
    } <= set(report["required_fragments"])


def test_component_publish_text_renderer_contract_proves_catalog_log_markers() -> None:
    report = appgen_dsl._component_publish_text_renderer_contract()

    assert report["format"] == "appgen.component-publish-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] == report["output_line_count"] == 3
    assert report["summary_line_count"] == 1
    assert report["catalog_line_count"] == 2
    assert report["side_effect_line_count"] == 1
    assert report["patch_contract_line_count"] == 1
    assert report["existing_catalog_line_count"] == 1
    assert report["required_text_surfaces"] == (
        "summary",
        "catalog_source",
        "catalog_counts",
        "existing_catalog",
        "side_effect_free",
        "write_performed",
        "patch_format",
        "registration_state",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == (
        "appgen.component-publish-report.v1",
        "appgen.component-catalog-patch.v1",
    )
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_registration_values"] == ("False",)
    assert report["emitted_registration_values"] == report["required_registration_values"]
    assert report["missing_registration_value_count"] == 0
    assert report["missing_registration_values"] == ()
    assert report["required_catalog_count_markers"] == ("before=1", "after=2", "existing=1")
    assert report["emitted_catalog_count_markers"] == report["required_catalog_count_markers"]
    assert report["missing_catalog_count_marker_count"] == 0
    assert report["missing_catalog_count_markers"] == ()
    assert report["required_catalog_sources"] == ("components.json",)
    assert report["emitted_catalog_sources"] == report["required_catalog_sources"]
    assert report["missing_catalog_source_count"] == 0
    assert report["missing_catalog_sources"] == ()
    assert report["required_side_effect_values"] == ("True",)
    assert report["emitted_side_effect_values"] == report["required_side_effect_values"]
    assert report["missing_side_effect_value_count"] == 0
    assert report["missing_side_effect_values"] == ()
    assert report["required_write_values"] == ("False",)
    assert report["emitted_write_values"] == report["required_write_values"]
    assert report["missing_write_value_count"] == 0
    assert report["missing_write_values"] == ()
    assert report["required_patch_formats"] == ("appgen.component-catalog-patch.v1",)
    assert report["emitted_patch_formats"] == report["required_patch_formats"]
    assert report["missing_patch_format_count"] == 0
    assert report["missing_patch_formats"] == ()
    assert report["required_existing_components"] == ("ExistingBox",)
    assert report["emitted_existing_components"] == report["required_existing_components"]
    assert report["missing_existing_component_count"] == 0
    assert report["missing_existing_components"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "component-publish ok: format=appgen.component-publish-report.v1 component=CustomGauge"
    )
    assert {
        "already_registered=False",
        "side_effect_free=True",
        "write_performed=False",
        "patch_format=appgen.component-catalog-patch.v1",
        "catalog-count before=1 after=2 existing=1",
        "catalog-existing ExistingBox",
    } <= set(report["required_fragments"])


def test_pbc_publish_text_renderer_contract_proves_side_effect_free_log_markers() -> None:
    report = appgen_dsl._pbc_publish_text_renderer_contract()

    assert report["format"] == "appgen.pbc-publish-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 8
    assert report["summary_line_count"] == 1
    assert report["catalog_path_line_count"] == 1
    assert report["side_effect_line_count"] == 1
    assert report["catalog_patch_line_count"] == 1
    assert report["check_line_count"] == 4
    assert report["passing_check_line_count"] == 4
    assert report["failing_check_line_count"] == 0
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith("pbc publish ok: gl_core -> local")
    assert {
        "catalog_path catalog/pbcs.json",
        "side_effect_free=True write_performed=False",
        "catalog-patch gl_core: General Ledger Core",
        "ok package_loads",
        "ok manifest_validates",
        "ok catalog_patch_available",
        "ok publish_is_side_effect_free",
    } <= set(report["required_fragments"])


def test_pbc_publish_cli_audit_covers_side_effect_free_file_catalog(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_pbc_publish_cli(tmp_path)

    assert audit["format"] == "appgen.pbc-publish-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 2
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["failing_cases"] == ()
    assert audit["payload_format"] == "appgen.pbc-publish-report.v1"
    assert audit["pbc"] == "gl_core"
    assert audit["target_mode"] == "file"
    assert audit["side_effect_free"] is True
    assert audit["write_performed"] is False
    assert audit["catalog_patch_count"] >= 1
    assert audit["release_evidence_format"] == "appgen.pbc-package-verifier.v1"
    assert audit["release_evidence_ok"] is True
    assert audit["passing_check_count"] == audit["check_count"]
    assert audit["blocking_gap_count"] == 0
    assert audit["text_has_catalog_path"] is True
    assert audit["text_has_side_effect_markers"] is True
    assert audit["text_has_catalog_patch"] is True
    assert audit["text_has_check_status"] is True
    assert audit["text_json_fallback"] is False


def test_diagnostics_text_renderer_contract_proves_catalog_and_fixture_log_markers() -> None:
    report = appgen_dsl._diagnostics_text_renderer_contract()

    assert report["format"] == "appgen.diagnostics-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 8
    assert report["summary_line_count"] == 2
    assert report["required_code_line_count"] == 3
    assert report["covered_fixture_line_count"] == 3
    assert report["covered_code_line_count"] == 2
    assert report["missing_code_line_count"] == 1
    assert report["blocking_gap_line_count"] == 1
    assert report["required_codes"] == ("AGX0201", "AGX0303", "AGX9000")
    assert report["emitted_required_codes"] == report["required_codes"]
    assert report["missing_required_code_count"] == 0
    assert report["missing_required_codes"] == ()
    assert report["required_covered_fixture_codes"] == ("AGX0201", "AGX0303", "AGX9000")
    assert report["emitted_covered_fixture_codes"] == report["required_covered_fixture_codes"]
    assert report["missing_covered_fixture_code_count"] == 0
    assert report["missing_covered_fixture_codes"] == ()
    assert report["required_covered_codes"] == ("AGX0201", "AGX0303")
    assert report["emitted_covered_codes"] == report["required_covered_codes"]
    assert report["missing_covered_code_count"] == 0
    assert report["missing_covered_codes"] == ()
    assert report["required_missing_codes"] == ("AGX9000",)
    assert report["emitted_missing_codes"] == report["required_missing_codes"]
    assert report["missing_missing_code_count"] == 0
    assert report["missing_missing_codes"] == ()
    assert report["required_blocking_gap_ids"] == ("AGX9000",)
    assert report["emitted_blocking_gap_ids"] == report["required_blocking_gap_ids"]
    assert report["missing_blocking_gap_id_count"] == 0
    assert report["missing_blocking_gap_ids"] == ()
    assert report["required_text_surfaces"] == (
        "catalog_summary",
        "fixture_summary",
        "required_codes",
        "covered_fixture_codes",
        "covered_codes",
        "missing_codes",
        "blocking_gaps",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == (
        "appgen.diagnostic-catalog.v1",
        "appgen.diagnostic-fixture-audit.v1",
    )
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "diagnostics ok: format=appgen.diagnostic-catalog.v1 covered=3 required=3"
    )
    assert {
        "diagnostics-audit failed: format=appgen.diagnostic-fixture-audit.v1 covered=2 required=3 missing=1",
        "required-code AGX9000",
        "covered-fixture-code AGX0303",
        "covered-code AGX0201",
        "covered-code AGX0303",
        "missing-code AGX9000",
        "fail AGX9000: missing fixture",
    } <= set(report["required_fragments"])


def test_lint_text_renderer_contract_proves_stage_and_migration_log_markers() -> None:
    report = appgen_dsl._lint_text_renderer_contract()

    assert report["format"] == "appgen.lint-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 7
    assert report["source_file_line_count"] == 2
    assert report["stage_line_count"] == 1
    assert report["migration_line_count"] == 2
    assert report["migration_preview_line_count"] == 1
    assert report["migration_detected_line_count"] == 1
    assert report["diagnostic_line_count"] == 2
    assert report["error_line_count"] == 1
    assert report["warning_line_count"] == 1
    assert report["required_source_files"] == ("apps/sales.appgen", "apps/inventory.appgen")
    assert report["emitted_source_files"] == report["required_source_files"]
    assert report["missing_source_file_count"] == 0
    assert report["missing_source_files"] == ()
    assert report["required_text_surfaces"] == (
        "source_summary",
        "source_files",
        "stage_counts",
        "migration_preview",
        "migration_detected",
        "diagnostics",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == ("appgen.lint-report.v1", "appgen.migration-plan.v1")
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_source_modes"] == ("directory",)
    assert report["emitted_source_modes"] == report["required_source_modes"]
    assert report["missing_source_mode_count"] == 0
    assert report["missing_source_modes"] == ()
    assert report["required_migration_backends"] == ("postgresql",)
    assert report["emitted_migration_backends"] == report["required_migration_backends"]
    assert report["missing_migration_backend_count"] == 0
    assert report["missing_migration_backends"] == ()
    assert report["required_approval_values"] == ("requires_approval=True",)
    assert report["emitted_approval_values"] == report["required_approval_values"]
    assert report["missing_approval_value_count"] == 0
    assert report["missing_approval_values"] == ()
    assert report["required_stage_counts"] == ("syntax=0", "semantic=1", "policy=1")
    assert report["emitted_stage_counts"] == report["required_stage_counts"]
    assert report["missing_stage_count_count"] == 0
    assert report["missing_stage_counts"] == ()
    assert report["required_stage_names"] == ("syntax", "semantic", "policy")
    assert report["emitted_stage_names"] == report["required_stage_names"]
    assert report["missing_stage_name_count"] == 0
    assert report["missing_stage_names"] == ()
    assert report["required_migration_families"] == ("relationships", "tables")
    assert report["emitted_migration_families"] == report["required_migration_families"]
    assert report["missing_migration_family_count"] == 0
    assert report["missing_migration_families"] == ()
    assert report["required_diagnostic_codes"] == ("AGX0402", "AGX0701")
    assert report["emitted_diagnostic_codes"] == report["required_diagnostic_codes"]
    assert report["missing_diagnostic_code_count"] == 0
    assert report["missing_diagnostic_codes"] == ()
    assert report["required_diagnostic_severities"] == ("error", "warning")
    assert report["emitted_diagnostic_severities"] == report["required_diagnostic_severities"]
    assert report["missing_diagnostic_severity_count"] == 0
    assert report["missing_diagnostic_severities"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith("lint failed: format=appgen.lint-report.v1")
    assert {
        "source directory: files=2",
        "source-file apps/sales.appgen",
        "source-file apps/inventory.appgen",
        "stages syntax=0 semantic=1 policy=1",
        "migration-preview format=appgen.migration-plan.v1 backend=postgresql: changes=1 requires_approval=True",
        "migration-detected relationships, tables",
        "error AGX0402: A database-backed form binding must resolve to a field.",
    } <= set(report["required_fragments"])


def test_semantic_drift_text_renderer_contract_proves_shared_model_log_markers() -> None:
    report = appgen_dsl._semantic_drift_text_renderer_contract()

    assert report["format"] == "appgen.semantic-drift-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 8
    assert report["summary_line_count"] == 1
    assert report["surface_line_count"] == 1
    assert report["gap_line_count"] == 1
    assert report["evidence_line_count"] == 3
    assert report["check_line_count"] == 2
    assert report["passing_check_line_count"] == 1
    assert report["failing_check_line_count"] == 1
    assert report["digest_line_count"] == 1
    assert report["required_surfaces"] == ("cli", "lsp", "studio", "generator")
    assert report["emitted_surfaces"] == report["required_surfaces"]
    assert report["missing_surface_count"] == 0
    assert report["missing_surfaces"] == ()
    assert report["required_gap_ids"] == ("studio_missing_surface",)
    assert report["emitted_gap_ids"] == report["required_gap_ids"]
    assert report["missing_gap_id_count"] == 0
    assert report["missing_gap_ids"] == ()
    assert report["required_evidence_keys"] == ("generate_report", "lsp_service", "studio_surfaces")
    assert report["emitted_evidence_keys"] == report["required_evidence_keys"]
    assert report["missing_evidence_key_count"] == 0
    assert report["missing_evidence_keys"] == ()
    assert report["required_check_ids"] == ("cli_uses_semantic_model", "studio_uses_semantic_model")
    assert report["emitted_check_ids"] == report["required_check_ids"]
    assert report["missing_check_id_count"] == 0
    assert report["missing_check_ids"] == ()
    assert report["required_passing_check_ids"] == ("cli_uses_semantic_model",)
    assert report["emitted_passing_check_ids"] == report["required_passing_check_ids"]
    assert report["missing_passing_check_id_count"] == 0
    assert report["missing_passing_check_ids"] == ()
    assert report["required_failing_check_ids"] == ("studio_uses_semantic_model",)
    assert report["emitted_failing_check_ids"] == report["required_failing_check_ids"]
    assert report["missing_failing_check_id_count"] == 0
    assert report["missing_failing_check_ids"] == ()
    assert report["required_text_surfaces"] == (
        "summary",
        "surface_list",
        "blocking_gaps",
        "surface_evidence",
        "check_results",
        "semantic_digest",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == (
        "appgen.semantic-drift-audit.v1",
        "appgen.semantic-model.v1",
        "appgen.generate-report.v1",
        "appgen.lsp-service.v1",
    )
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_semantic_digests"] == ("sha256:semantic-fixture",)
    assert report["emitted_semantic_digests"] == report["required_semantic_digests"]
    assert report["missing_semantic_digest_count"] == 0
    assert report["missing_semantic_digests"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "drift failed: format=appgen.semantic-drift-audit.v1 semantic_format=appgen.semantic-model.v1"
    )
    assert {
        "surfaces cli, lsp, studio, generator",
        "gap studio_missing_surface",
        "evidence generate_report: appgen.generate-report.v1",
        "evidence studio_surfaces: database_designer,form_designer",
        "fail studio_uses_semantic_model",
    } <= set(report["required_fragments"])


def test_doctor_text_renderer_contract_proves_check_and_detail_format_markers() -> None:
    report = appgen_dsl._doctor_text_renderer_contract()

    assert report["format"] == "appgen.doctor-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["required_fragment_count"] == 9
    assert report["missing_fragment_count"] == 0
    assert report["check_line_count"] == 8
    assert report["detail_format_line_count"] == 8
    assert report["required_check_ids"] == (
        "parser_golden_fixtures",
        "lsp_completion_coverage",
        "semantic_symbol_coverage",
        "lsp_symbol_coverage",
        "cli_alias_contract",
        "module_boundaries",
        "studio_semantic_service",
        "vscode_extension_surface",
    )
    assert report["emitted_check_ids"] == report["required_check_ids"]
    assert report["missing_check_id_count"] == 0
    assert report["missing_check_ids"] == ()
    assert report["required_detail_formats_by_check"]["module_boundaries"] == "appgen.module-boundary-audit.v1"
    assert report["emitted_detail_formats_by_check"] == report["required_detail_formats_by_check"]
    assert report["missing_detail_format_check_count"] == 0
    assert report["missing_detail_format_checks"] == ()
    assert report["required_check_outcomes"] == (
        "parser_golden_fixtures:ok",
        "lsp_completion_coverage:ok",
        "semantic_symbol_coverage:ok",
        "lsp_symbol_coverage:ok",
        "cli_alias_contract:ok",
        "module_boundaries:fail",
        "studio_semantic_service:ok",
        "vscode_extension_surface:ok",
    )
    assert report["emitted_check_outcomes"] == report["required_check_outcomes"]
    assert report["missing_check_outcome_count"] == 0
    assert report["missing_check_outcomes"] == ()
    assert report["required_text_surfaces"] == ("summary", "check_statuses", "detail_formats", "blocking_gaps")
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_report_formats"] == (
        "appgen.doctor-report.v1",
        "appgen.parser-golden-audit.v1",
        "appgen.completion-coverage.v1",
        "appgen.symbol-coverage.v1",
        "appgen.lsp-symbol-coverage.v1",
        "appgen.cli-alias-contract.v1",
        "appgen.module-boundary-audit.v1",
        "appgen.designer-sync-report.v1",
        "appgen.vscode-extension-audit.v1",
    )
    assert report["emitted_report_formats"] == report["required_report_formats"]
    assert report["missing_report_format_count"] == 0
    assert report["missing_report_formats"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith("doctor failed: format=appgen.doctor-report.v1 checks=8")
    assert {
        "ok parser_golden_fixtures detail_format=appgen.parser-golden-audit.v1: Parser golden fixtures cover valid and invalid DSL grammar constructs.",
        "ok lsp_completion_coverage detail_format=appgen.completion-coverage.v1: Language-server completion sources cover docs/tooling.md contexts.",
        "ok semantic_symbol_coverage detail_format=appgen.symbol-coverage.v1: Semantic model emits all required symbol kinds for CLI, IDE, tests, and agents.",
        "ok lsp_symbol_coverage detail_format=appgen.lsp-symbol-coverage.v1: Language-server document and workspace symbol surfaces expose every required semantic symbol kind.",
        "ok cli_alias_contract detail_format=appgen.cli-alias-contract.v1: appgen and apg resolve to the same tooling entrypoint.",
        "fail module_boundaries detail_format=appgen.module-boundary-audit.v1: Documented DSL tooling boundaries are incomplete.",
        "ok studio_semantic_service detail_format=appgen.designer-sync-report.v1: Studio designer service is bound to the shared semantic model.",
        "ok vscode_extension_surface detail_format=appgen.vscode-extension-audit.v1: VS Code extension scaffold declares the AppGen-X language, commands, and LSP providers.",
    } <= set(report["required_fragments"])


def test_validate_generate_text_renderer_contract_proves_readiness_log_markers() -> None:
    report = appgen_dsl._validate_generate_text_renderer_contract()

    assert report["format"] == "appgen.validate-generate-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 10
    assert report["summary_line_count"] == 2
    assert report["check_line_count"] == 2
    assert report["passing_check_line_count"] == 1
    assert report["failing_check_line_count"] == 1
    assert report["target_detail_line_count"] == 2
    assert report["artifact_line_count"] == 1
    assert report["manifest_line_count"] == 1
    assert report["gap_line_count"] == 1
    assert report["diagnostic_line_count"] == 2
    assert report["warning_line_count"] == 1
    assert report["error_line_count"] == 1
    assert report["required_text_surfaces"] == (
        "validate_summary",
        "generate_summary",
        "checks",
        "target_details",
        "output_dir",
        "manifest",
        "artifacts",
        "gaps",
        "diagnostics",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == ("appgen.validate-report.v1", "appgen.generate-report.v1")
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_semantic_formats"] == ("appgen.semantic-model.v1",)
    assert report["emitted_semantic_formats"] == report["required_semantic_formats"]
    assert report["missing_semantic_format_count"] == 0
    assert report["missing_semantic_formats"] == ()
    assert report["required_validate_statuses"] == ("failed",)
    assert report["emitted_validate_statuses"] == report["required_validate_statuses"]
    assert report["missing_validate_status_count"] == 0
    assert report["missing_validate_statuses"] == ()
    assert report["required_generate_statuses"] == ("failed",)
    assert report["emitted_generate_statuses"] == report["required_generate_statuses"]
    assert report["missing_generate_status_count"] == 0
    assert report["missing_generate_statuses"] == ()
    assert report["required_generated_values"] == ("False",)
    assert report["emitted_generated_values"] == report["required_generated_values"]
    assert report["missing_generated_value_count"] == 0
    assert report["missing_generated_values"] == ()
    assert report["required_output_dirs"] == ("generated/app",)
    assert report["emitted_output_dirs"] == report["required_output_dirs"]
    assert report["missing_output_dir_count"] == 0
    assert report["missing_output_dirs"] == ()
    assert report["required_artifact_sizes"] == ("generated/app/web/routes.json=512",)
    assert report["emitted_artifact_sizes"] == report["required_artifact_sizes"]
    assert report["missing_artifact_size_count"] == 0
    assert report["missing_artifact_sizes"] == ()
    assert report["required_requested_targets"] == ("web", "mobile")
    assert report["emitted_requested_targets"] == report["required_requested_targets"]
    assert report["missing_requested_target_count"] == 0
    assert report["missing_requested_targets"] == ()
    assert report["required_app_targets"] == ("web",)
    assert report["emitted_app_targets"] == report["required_app_targets"]
    assert report["missing_app_target_count"] == 0
    assert report["missing_app_targets"] == ()
    assert report["required_generate_targets"] == ("web",)
    assert report["emitted_generate_targets"] == report["required_generate_targets"]
    assert report["missing_generate_target_count"] == 0
    assert report["missing_generate_targets"] == ()
    assert report["required_check_ids"] == ("syntax", "target_compatibility")
    assert report["emitted_check_ids"] == report["required_check_ids"]
    assert report["missing_check_id_count"] == 0
    assert report["missing_check_ids"] == ()
    assert report["required_passing_check_ids"] == ("syntax",)
    assert report["emitted_passing_check_ids"] == report["required_passing_check_ids"]
    assert report["missing_passing_check_id_count"] == 0
    assert report["missing_passing_check_ids"] == ()
    assert report["required_failing_check_ids"] == ("target_compatibility",)
    assert report["emitted_failing_check_ids"] == report["required_failing_check_ids"]
    assert report["missing_failing_check_id_count"] == 0
    assert report["missing_failing_check_ids"] == ()
    assert report["required_unknown_targets"] == ("mobile",)
    assert report["emitted_unknown_targets"] == report["required_unknown_targets"]
    assert report["missing_unknown_target_count"] == 0
    assert report["missing_unknown_targets"] == ()
    assert report["required_missing_targets"] == ("mobile",)
    assert report["emitted_missing_targets"] == report["required_missing_targets"]
    assert report["missing_missing_target_count"] == 0
    assert report["missing_missing_targets"] == ()
    assert report["required_artifact_paths"] == ("generated/app/web/routes.json",)
    assert report["emitted_artifact_paths"] == report["required_artifact_paths"]
    assert report["missing_artifact_path_count"] == 0
    assert report["missing_artifact_paths"] == ()
    assert report["required_manifest_paths"] == ("generated/app/appgen-manifest.json",)
    assert report["emitted_manifest_paths"] == report["required_manifest_paths"]
    assert report["missing_manifest_path_count"] == 0
    assert report["missing_manifest_paths"] == ()
    assert report["required_gap_ids"] == ("lint_warnings",)
    assert report["emitted_gap_ids"] == report["required_gap_ids"]
    assert report["missing_gap_id_count"] == 0
    assert report["missing_gap_ids"] == ()
    assert report["required_diagnostic_codes"] == ("AGX0802", "AGX0404")
    assert report["emitted_diagnostic_codes"] == report["required_diagnostic_codes"]
    assert report["missing_diagnostic_code_count"] == 0
    assert report["missing_diagnostic_codes"] == ()
    assert report["required_diagnostic_severities"] == ("error", "warning")
    assert report["emitted_diagnostic_severities"] == report["required_diagnostic_severities"]
    assert report["missing_diagnostic_severity_count"] == 0
    assert report["missing_diagnostic_severities"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "validate failed: format=appgen.validate-report.v1 requested=web,mobile"
    )
    assert {
        "unknown-targets mobile",
        "missing-targets mobile",
        "generate failed: format=appgen.generate-report.v1 generated=False targets=web artifacts=1 semantic_format=appgen.semantic-model.v1",
        "artifact generated/app/web/routes.json bytes=512",
        "gap lint_warnings",
    } <= set(report["required_fragments"])


def test_format_text_renderer_contract_proves_write_and_idempotence_log_markers() -> None:
    report = appgen_dsl._format_text_renderer_contract()

    assert report["format"] == "appgen.format-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 3
    assert report["summary_line_count"] == 1
    assert report["write_path_line_count"] == 1
    assert report["diagnostic_line_count"] == 1
    assert report["warning_line_count"] == 1
    assert report["error_line_count"] == 0
    assert report["write_flag_line_count"] == 1
    assert report["idempotence_line_count"] == 1
    assert report["organize_line_count"] == 1
    assert report["required_text_surfaces"] == (
        "summary",
        "write_path",
        "diagnostics",
        "write_requested",
        "written",
        "organize",
        "idempotence",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == ("appgen.format-result.v1",)
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_mutation_states"] == ("changed",)
    assert report["emitted_mutation_states"] == report["required_mutation_states"]
    assert report["missing_mutation_state_count"] == 0
    assert report["missing_mutation_states"] == ()
    assert report["required_write_paths"] == ("apps/sales.appgen",)
    assert report["emitted_write_paths"] == report["required_write_paths"]
    assert report["missing_write_path_count"] == 0
    assert report["missing_write_paths"] == ()
    assert report["required_write_requested_values"] == ("True",)
    assert report["emitted_write_requested_values"] == report["required_write_requested_values"]
    assert report["missing_write_requested_value_count"] == 0
    assert report["missing_write_requested_values"] == ()
    assert report["required_written_values"] == ("True",)
    assert report["emitted_written_values"] == report["required_written_values"]
    assert report["missing_written_value_count"] == 0
    assert report["missing_written_values"] == ()
    assert report["required_organize_values"] == ("True",)
    assert report["emitted_organize_values"] == report["required_organize_values"]
    assert report["missing_organize_value_count"] == 0
    assert report["missing_organize_values"] == ()
    assert report["required_idempotence_states"] == ("not-idempotent",)
    assert report["emitted_idempotence_states"] == report["required_idempotence_states"]
    assert report["missing_idempotence_state_count"] == 0
    assert report["missing_idempotence_states"] == ()
    assert report["required_diagnostic_codes"] == ("AGX0201",)
    assert report["emitted_diagnostic_codes"] == report["required_diagnostic_codes"]
    assert report["missing_diagnostic_code_count"] == 0
    assert report["missing_diagnostic_codes"] == ()
    assert report["required_diagnostic_severities"] == ("warning",)
    assert report["emitted_diagnostic_severities"] == report["required_diagnostic_severities"]
    assert report["missing_diagnostic_severity_count"] == 0
    assert report["missing_diagnostic_severities"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith("format changed: format=appgen.format-result.v1")
    assert {
        "format changed: format=appgen.format-result.v1 not-idempotent written organize=True write_requested=True written=True",
        "write_path apps/sales.appgen",
        "warning AGX0201: Formatter normalized field modifier order.",
    } <= set(report["required_fragments"])


def test_designer_sync_text_renderer_contract_proves_round_trip_log_markers() -> None:
    report = appgen_dsl._designer_sync_text_renderer_contract()

    assert report["format"] == "appgen.designer-sync-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 10
    assert report["summary_line_count"] == 1
    assert report["surface_line_count"] == 1
    assert report["visual_edit_line_count"] == 1
    assert report["dsl_diff_line_count"] == 2
    assert report["matrix_line_count"] == 1
    assert report["operation_line_count"] == 1
    assert report["case_line_count"] == 7
    assert report["check_line_count"] == 2
    assert report["passing_check_line_count"] == 2
    assert report["failing_check_line_count"] == 0
    assert report["required_surfaces"] == (
        "form_designer",
        "database_designer",
        "workflow_designer",
        "package_designer",
    )
    assert report["emitted_surfaces"] == report["required_surfaces"]
    assert report["missing_surface_count"] == 0
    assert report["missing_surfaces"] == ()
    assert report["required_changed_surfaces"] == ("database_designer", "form_designer")
    assert report["emitted_changed_surfaces"] == report["required_changed_surfaces"]
    assert report["missing_changed_surface_count"] == 0
    assert report["missing_changed_surfaces"] == ()
    assert report["required_operations"] == (
        "add_field",
        "add_component",
        "add_flow_transition",
        "add_pbc_include",
        "add_package",
        "add_deployment_unit",
    )
    assert report["emitted_operations"] == report["required_operations"]
    assert report["missing_operation_count"] == 0
    assert report["missing_operations"] == ()
    assert report["required_case_ids"] == (
        "database_designer_add_field",
        "form_designer_add_component",
        "workflow_designer_add_transition",
        "pbc_composition_designer_add_include",
        "package_designer_add_package",
        "deployment_designer_add_unit",
        "form_designer_reject_invalid_binding",
    )
    assert report["emitted_case_ids"] == report["required_case_ids"]
    assert report["missing_case_id_count"] == 0
    assert report["missing_case_ids"] == ()
    assert report["required_check_ids"] == ("semantic_round_trip", "projection_refresh")
    assert report["emitted_check_ids"] == report["required_check_ids"]
    assert report["missing_check_id_count"] == 0
    assert report["missing_check_ids"] == ()
    assert report["required_diff_snippets"] == ("+  sync_note: string", "+  Main: sync_note")
    assert report["emitted_diff_snippets"] == report["required_diff_snippets"]
    assert report["missing_diff_snippet_count"] == 0
    assert report["missing_diff_snippets"] == ()
    assert report["required_text_surfaces"] == (
        "summary",
        "surfaces",
        "visual_edit",
        "dsl_diff",
        "visual_edit_matrix",
        "operations",
        "cases",
        "checks",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_contract_formats"] == (
        "appgen.designer-sync-report.v1",
        "appgen.semantic-model.v1",
        "appgen.designer-visual-edit-matrix.v1",
    )
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["required_status_markers"] == (
        "designer-sync ok",
        "accepted=True",
        "round_trip=True",
        "ok=True",
        "gaps=0",
    )
    assert report["emitted_status_markers"] == report["required_status_markers"]
    assert report["missing_status_marker_count"] == 0
    assert report["missing_status_markers"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "designer-sync ok: format=appgen.designer-sync-report.v1 semantic_format=appgen.semantic-model.v1"
    )
    assert {
        "visual-edit accepted=True round_trip=True changed=database_designer,form_designer diff_lines=2",
        "dsl-diff +  sync_note: string",
        "dsl-diff +  Main: sync_note",
        "visual-edit-matrix ok=True format=appgen.designer-visual-edit-matrix.v1 cases=7 gaps=0",
        "visual-edit-operations add_field, add_component, add_flow_transition, add_pbc_include, add_package, add_deployment_unit",
        "visual-edit-case database_designer_add_field",
        "visual-edit-case form_designer_add_component",
        "visual-edit-case workflow_designer_add_transition",
        "visual-edit-case pbc_composition_designer_add_include",
        "visual-edit-case package_designer_add_package",
        "visual-edit-case deployment_designer_add_unit",
        "visual-edit-case form_designer_reject_invalid_binding",
        "ok projection_refresh",
    } <= set(report["required_fragments"])


def test_migration_plan_text_renderer_contract_proves_safety_log_markers() -> None:
    report = appgen_dsl._migration_plan_text_renderer_contract()

    assert report["format"] == "appgen.migration-plan-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 10
    assert report["summary_line_count"] == 1
    assert report["input_line_count"] == 1
    assert report["coverage_line_count"] == 1
    assert report["detected_family_line_count"] == 1
    assert report["missing_family_line_count"] == 1
    assert report["change_line_count"] == 3
    assert report["safe_alternative_line_count"] == 2
    assert report["diagnostic_line_count"] == 1
    assert report["warning_line_count"] == 1
    assert report["error_line_count"] == 0
    assert report["approval_line_count"] == 1
    assert report["destructive_summary_line_count"] == 1
    assert report["required_text_surfaces"] == (
        "summary",
        "input_formats",
        "coverage",
        "detected_families",
        "missing_families",
        "changes",
        "safe_alternatives",
        "diagnostics",
        "approval_required",
        "destructive_summary",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_detected_families"] == ("added_table", "dropped_field", "type_change")
    assert report["emitted_detected_families"] == report["required_detected_families"]
    assert report["missing_detected_family_count"] == 0
    assert report["missing_detected_families"] == ()
    assert report["required_missing_families"] == ("relationship_change",)
    assert report["emitted_missing_families"] == report["required_missing_families"]
    assert report["missing_missing_family_count"] == 0
    assert report["missing_missing_families"] == ()
    assert report["required_change_targets"] == (
        "add_table: CreditMemo",
        "drop_field: Invoice.legacy_code",
        "type_change: Invoice.total",
    )
    assert report["emitted_change_targets"] == report["required_change_targets"]
    assert report["missing_change_target_count"] == 0
    assert report["missing_change_targets"] == ()
    assert report["required_safe_alternatives"] == ("drop_field", "type_change")
    assert report["emitted_safe_alternatives"] == report["required_safe_alternatives"]
    assert report["missing_safe_alternative_count"] == 0
    assert report["missing_safe_alternatives"] == ()
    assert report["required_diagnostic_codes"] == ("AGX1101",)
    assert report["emitted_diagnostic_codes"] == report["required_diagnostic_codes"]
    assert report["missing_diagnostic_code_count"] == 0
    assert report["missing_diagnostic_codes"] == ()
    assert report["required_contract_formats"] == (
        "appgen.migration-plan.v1",
        "appgen.migration-coverage.v1",
    )
    assert report["emitted_contract_formats"] == report["required_contract_formats"]
    assert report["missing_contract_format_count"] == 0
    assert report["missing_contract_formats"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "migration-plan failed: format=appgen.migration-plan.v1 backend=postgresql"
    )
    assert {
        "migration-inputs previous=appgen.semantic-model.v1 current=appgen.semantic-model.v1 semantic_inputs=2",
        "migration-coverage format=appgen.migration-coverage.v1: detected=3 missing=1",
        "migration-detected added_table, dropped_field, type_change",
        "migration-missing relationship_change",
        "safe-alternative drop_field: Mark Invoice.legacy_code deprecated before dropping it.",
        "warning AGX1101: Destructive migration changes require approval.",
    } <= set(report["required_fragments"])


def test_migration_plan_accepts_semantic_model_json_inputs(tmp_path: Path) -> None:
    previous_source = """
app MigrationDemo { targets: web }

table Customer {
  id: int pk
  name: string
}

table Invoice {
  id: int pk
  customer_id: int -> Customer.id
  total: decimal default 0
}
"""
    current_source = """
app MigrationDemo { targets: web }

table Account {
  id: int pk
  name: string
}

table Invoice {
  id: int pk
  account_id: int -> Account.id
  total: decimal default 0
  due_date: date required
}
"""
    previous_path = tmp_path / "previous.semantic.json"
    current_path = tmp_path / "current.semantic.json"
    previous_path.write_text(
        json.dumps(appgen_dsl.semantic_model_dsl(previous_source), indent=2, sort_keys=True, default=list),
        encoding="utf-8",
    )
    current_path.write_text(
        json.dumps(appgen_dsl.semantic_model_dsl(current_source), indent=2, sort_keys=True, default=list),
        encoding="utf-8",
    )

    report = appgen_dsl.migration_plan_dsl_files(
        previous_path,
        current_path,
        backend="postgresql",
        rename_hints=("table:Customer=Account", "field:Invoice.customer_id=Invoice.account_id"),
    )

    assert report["format"] == "appgen.migration-plan.v1"
    assert report["ok"] is True
    assert report["previous_input_format"] == "appgen.semantic-model.v1"
    assert report["current_input_format"] == "appgen.semantic-model.v1"
    assert report["input_formats"] == ("appgen.semantic-model.v1",)
    assert report["semantic_input_count"] == 2
    assert report["source_files"] == (str(previous_path), str(current_path))
    assert {"rename_table", "rename_field", "add_field"} <= {change["kind"] for change in report["changes"]}
    assert report["coverage"]["format"] == "appgen.migration-coverage.v1"


def test_migration_semantic_input_cli_audit_proves_json_baselines(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_migration_semantic_input_cli(tmp_path)

    assert report["format"] == "appgen.migration-semantic-input-cli-audit.v1"
    assert report["ok"] is True
    assert report["json_exit_code"] == 0
    assert report["text_exit_code"] == 0
    assert report["payload_format"] == "appgen.migration-plan.v1"
    assert report["payload_ok"] is True
    assert report["backend"] == "postgresql"
    assert report["previous_input_format"] == "appgen.semantic-model.v1"
    assert report["current_input_format"] == "appgen.semantic-model.v1"
    assert report["input_formats"] == ("appgen.semantic-model.v1",)
    assert report["semantic_input_count"] == 2
    assert report["missing_source_file_count"] == 0
    assert report["missing_source_files"] == ()
    assert report["required_change_kinds"] == ("rename_table", "rename_field", "add_field")
    assert report["missing_change_kind_count"] == 0
    assert report["missing_change_kinds"] == ()
    assert report["coverage_format"] == "appgen.migration-coverage.v1"
    assert report["missing_text_fragment_count"] == 0
    assert report["missing_text_fragments"] == ()
    assert report["text_json_fallback"] is False
    assert report["text_prefix"].startswith("migration-plan ok: format=appgen.migration-plan.v1")


def test_migration_cli_audit_covers_supported_backends_and_rename_hints(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_migration_cli(tmp_path)

    assert report["format"] == "appgen.migration-cli-audit.v1"
    assert report["ok"] is True
    assert report["case_count"] == report["allowed_backend_count"]
    assert report["passing_case_count"] == report["case_count"]
    assert report["failing_case_count"] == 0
    expected_case_ids = tuple(f"{backend}_json_rename_hints" for backend in appgen_dsl.SUPPORTED_DATABASE_BACKENDS)
    assert report["required_case_ids"] == expected_case_ids
    assert report["observed_case_ids"] == expected_case_ids
    assert report["missing_case_count"] == 0
    assert report["missing_case_ids"] == ()
    assert report["allowed_backends"] == appgen_dsl.SUPPORTED_DATABASE_BACKENDS
    assert report["observed_backends"] == appgen_dsl.SUPPORTED_DATABASE_BACKENDS
    assert report["missing_allowed_backend_count"] == 0
    assert report["missing_allowed_backends"] == ()
    assert report["expected_backends_by_case"] == {
        f"{backend}_json_rename_hints": backend for backend in appgen_dsl.SUPPORTED_DATABASE_BACKENDS
    }
    assert report["backends_by_case"] == report["expected_backends_by_case"]
    assert report["missing_backend_case_count"] == 0
    assert report["missing_backend_case_ids"] == ()
    assert report["change_kind_count"] >= 3
    assert report["required_change_kind_count"] == 3
    assert report["missing_required_change_kind_count"] == 0
    assert report["missing_required_change_kinds"] == ()
    assert set(report["required_change_kinds"]) == {"rename_table", "rename_field", "add_field"}
    assert set(report["required_change_kinds"]) <= set(report["observed_change_kinds"])
    assert report["required_change_kinds_by_case"] == {
        case_id: ("rename_table", "rename_field", "add_field") for case_id in expected_case_ids
    }
    assert all(
        set(report["required_change_kinds_by_case"][case_id]) <= set(report["change_kinds_by_case"][case_id])
        for case_id in expected_case_ids
    )
    assert report["missing_change_kind_case_count"] == 0
    assert report["missing_change_kinds_by_case"] == {}
    assert report["approval_required_count"] == report["case_count"]
    assert report["approval_required_cases"] == expected_case_ids
    assert report["missing_approval_required_case_count"] == 0
    assert report["missing_approval_required_cases"] == ()
    assert report["rename_hint_case_count"] == report["case_count"]
    assert report["expected_rename_hint_count_by_case"] == {case_id: 2 for case_id in expected_case_ids}
    assert report["rename_hint_cases"] == expected_case_ids
    assert report["missing_rename_hint_case_count"] == 0
    assert report["missing_rename_hint_cases"] == ()
    assert all(report["rename_hint_counts_by_case"][case_id] >= 2 for case_id in expected_case_ids)
    assert report["expected_payload_formats_by_case"] == {
        case_id: "appgen.migration-plan.v1" for case_id in expected_case_ids
    }
    assert report["payload_formats_by_case"] == report["expected_payload_formats_by_case"]
    assert report["missing_payload_format_case_count"] == 0
    assert report["missing_payload_format_cases"] == ()
    assert report["expected_exit_codes_by_case"] == {case_id: 0 for case_id in expected_case_ids}
    assert report["exit_codes_by_case"] == report["expected_exit_codes_by_case"]
    assert report["missing_exit_code_case_count"] == 0
    assert report["missing_exit_code_cases"] == ()
    assert all(report["destructive_change_counts_by_case"][case_id] >= 1 for case_id in expected_case_ids)
    assert report["destructive_change_cases"] == expected_case_ids
    assert report["missing_destructive_change_case_count"] == 0
    assert report["missing_destructive_change_cases"] == ()
    assert all(report["safe_alternative_counts_by_case"][case_id] >= 1 for case_id in expected_case_ids)
    assert report["safe_alternative_cases"] == expected_case_ids
    assert report["missing_safe_alternative_case_count"] == 0
    assert report["missing_safe_alternative_cases"] == ()
    assert report["required_diagnostic_codes_by_case"] == {case_id: ("AGX1101",) for case_id in expected_case_ids}
    assert all("AGX1101" in report["diagnostic_codes_by_case"][case_id] for case_id in expected_case_ids)
    assert report["missing_diagnostic_code_case_count"] == 0
    assert report["missing_diagnostic_codes_by_case"] == {}
    assert all(case["exit_code"] == 0 for case in report["cases"])
    assert all(case["payload_format"] == "appgen.migration-plan.v1" for case in report["cases"])
    assert all(case["requires_approval"] is True for case in report["cases"])
    assert all(case["rename_hint_count"] >= 2 for case in report["cases"])
    assert all({"rename_table", "rename_field", "add_field"} <= set(case["change_kinds"]) for case in report["cases"])


def test_lsp_service_text_renderer_contract_proves_editor_log_markers() -> None:
    report = appgen_dsl._lsp_service_text_renderer_contract()

    assert report["format"] == "appgen.lsp-service-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 11
    assert report["required_text_surfaces"] == (
        "service_counts",
        "source_of_truth",
        "completion_coverage",
        "completion_missing",
        "definition",
        "references",
        "formatting",
        "rename",
        "rename_blocker",
        "hover_summary",
        "hover_content",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_editor_contract_formats"] == (
        "appgen.lsp-service.v1",
        "appgen.semantic-model.v1",
        "appgen.completion-coverage.v1",
        "appgen.lsp-definition.v1",
        "appgen.lsp-references.v1",
        "appgen.lsp-formatting.v1",
        "appgen.lsp-rename.v1",
        "appgen.migration-plan.v1",
    )
    assert report["emitted_editor_contract_formats"] == report["required_editor_contract_formats"]
    assert report["missing_editor_contract_format_count"] == 0
    assert report["missing_editor_contract_formats"] == ()
    assert report["required_navigation_surfaces"] == ("definition", "references")
    assert report["emitted_navigation_surfaces"] == report["required_navigation_surfaces"]
    assert report["missing_navigation_surface_count"] == 0
    assert report["missing_navigation_surfaces"] == ()
    assert report["required_completion_gaps"] == ("agent_actions",)
    assert report["emitted_completion_gaps"] == report["required_completion_gaps"]
    assert report["missing_completion_gap_count"] == 0
    assert report["missing_completion_gaps"] == ()
    assert report["required_hover_items"] == ("table Invoice", "field total")
    assert report["emitted_hover_items"] == report["required_hover_items"]
    assert report["missing_hover_item_count"] == 0
    assert report["missing_hover_items"] == ()
    assert report["required_rename_blocker_codes"] == ("AGX1101",)
    assert report["emitted_rename_blocker_codes"] == report["required_rename_blocker_codes"]
    assert report["missing_rename_blocker_code_count"] == 0
    assert report["missing_rename_blocker_codes"] == ()
    assert report["required_rename_fix_ids"] == ("add_rename_hint",)
    assert report["emitted_rename_fix_ids"] == report["required_rename_fix_ids"]
    assert report["missing_rename_fix_id_count"] == 0
    assert report["missing_rename_fix_ids"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["summary_line_count"] == 1
    assert report["service_count_line_count"] == 1
    assert report["source_line_count"] == 1
    assert report["completion_line_count"] == 2
    assert report["completion_missing_line_count"] == 1
    assert report["navigation_line_count"] == 2
    assert report["definition_line_count"] == 1
    assert report["reference_line_count"] == 1
    assert report["formatting_line_count"] == 1
    assert report["rename_line_count"] == 1
    assert report["rename_blocker_line_count"] == 1
    assert report["hover_summary_line_count"] == 1
    assert report["hover_line_count"] == 2
    assert report["text_prefix"].startswith(
        "lsp ok: format=appgen.lsp-service.v1 semantic_format=appgen.semantic-model.v1"
    )
    assert {
        "service_counts completion_sources=5/6 missing_completion_sources=1 references=2 document_symbols=2 workspace_symbols=1 code_actions=1 formatting_edits=1 rename_edits=0",
        "source_of_truth=appgen.semantic-model.v1",
        "completion_coverage format=appgen.completion-coverage.v1 missing=1",
        "completion-missing agent_actions",
        "definition format=appgen.lsp-definition.v1 ok=True",
        "references format=appgen.lsp-references.v1 locations=2",
        "rename ok=False format=appgen.lsp-rename.v1 changed=False blocked=True diagnostics=1 blockers=1 migration_format=appgen.migration-plan.v1 requires_approval=True",
        "rename-blocker AGX1101: Destructive migration changes require approval. fixes=add_rename_hint",
        "hover table Invoice",
        "hover field total",
    } <= set(report["required_fragments"])


def test_lsp_code_action_text_renderer_contract_proves_quick_fix_log_markers() -> None:
    report = appgen_dsl._lsp_code_action_text_renderer_contract()

    assert report["format"] == "appgen.lsp-code-action-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 6
    assert report["success_summary_line_count"] == 1
    assert report["failure_summary_line_count"] == 1
    assert report["title_line_count"] == 1
    assert report["edit_line_count"] == 1
    assert report["available_action_line_count"] == 1
    assert report["diagnostic_line_count"] == 1
    assert report["lint_status_line_count"] == 2
    assert report["changed_status_line_count"] == 2
    assert report["required_text_surfaces"] == (
        "success_summary",
        "failure_summary",
        "title",
        "edit",
        "available_actions",
        "diagnostic",
        "lint_status",
        "changed_status",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_action_ids"] == ("create_operation_from_handler", "missing_action")
    assert report["emitted_action_ids"] == report["required_action_ids"]
    assert report["missing_action_id_count"] == 0
    assert report["missing_action_ids"] == ()
    assert report["required_edit_snippets"] == ("operation SubmitInvoice {}",)
    assert report["emitted_edit_snippets"] == report["required_edit_snippets"]
    assert report["missing_edit_snippet_count"] == 0
    assert report["missing_edit_snippets"] == ()
    assert report["required_available_actions"] == (
        "create_operation_from_handler",
        "create_flow_from_handler",
    )
    assert report["emitted_available_actions"] == report["required_available_actions"]
    assert report["missing_available_action_count"] == 0
    assert report["missing_available_actions"] == ()
    assert report["required_diagnostic_codes"] == ("AGX1002",)
    assert report["emitted_diagnostic_codes"] == report["required_diagnostic_codes"]
    assert report["missing_diagnostic_code_count"] == 0
    assert report["missing_diagnostic_codes"] == ()
    assert report["required_statuses"] == (
        "ok",
        "failed",
        "lint_ok=True",
        "lint_ok=False",
        "changed=True",
        "changed=False",
    )
    assert report["emitted_statuses"] == report["required_statuses"]
    assert report["missing_status_count"] == 0
    assert report["missing_statuses"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "lsp-code-action ok: format=appgen.lsp-code-action-apply.v1 action=create_operation_from_handler"
    )
    assert {
        "title Create operation SubmitInvoice",
        "edit operation SubmitInvoice {}",
        "lsp-code-action failed: format=appgen.lsp-code-action-apply.v1 action=missing_action changed=False edits=0 lint_ok=False",
        "available-actions create_operation_from_handler, create_flow_from_handler",
        "error AGX1002: Unknown code action: missing_action",
    } <= set(report["required_fragments"])


def test_graph_explain_text_renderer_contract_proves_review_log_markers() -> None:
    report = appgen_dsl._graph_explain_text_renderer_contract()

    assert report["format"] == "appgen.graph-explain-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 11
    assert report["required_graph_kinds"] == ("er", "lookup", "workflow")
    assert report["emitted_graph_kinds"] == report["required_graph_kinds"]
    assert report["missing_graph_kind_count"] == 0
    assert report["missing_graph_kinds"] == ()
    assert report["required_graph_formats"] == ("json", "mermaid", "dot")
    assert report["emitted_graph_formats"] == report["required_graph_formats"]
    assert report["missing_graph_format_count"] == 0
    assert report["missing_graph_formats"] == ()
    assert report["required_check_ids"] == ("er_graph", "workflow_graph")
    assert report["emitted_check_ids"] == report["required_check_ids"]
    assert report["missing_check_id_count"] == 0
    assert report["missing_check_ids"] == ()
    assert report["required_explain_kinds"] == ("symbol", "diagnostic", "handler")
    assert report["emitted_explain_kinds"] == report["required_explain_kinds"]
    assert report["missing_explain_kind_count"] == 0
    assert report["missing_explain_kinds"] == ()
    assert report["required_symbol_ids"] == ("table.Invoice",)
    assert report["emitted_symbol_ids"] == report["required_symbol_ids"]
    assert report["missing_symbol_id_count"] == 0
    assert report["missing_symbol_ids"] == ()
    assert report["required_diagnostic_codes"] == ("AGX0303",)
    assert report["emitted_diagnostic_codes"] == report["required_diagnostic_codes"]
    assert report["missing_diagnostic_code_count"] == 0
    assert report["missing_diagnostic_codes"] == ()
    assert report["required_docs_urls"] == ("docs/tooling.md#linter-rules-by-domain",)
    assert report["emitted_docs_urls"] == report["required_docs_urls"]
    assert report["missing_docs_url_count"] == 0
    assert report["missing_docs_urls"] == ()
    assert report["emitted_handler_edges"] == report["required_handler_edges"]
    assert report["missing_handler_edge_count"] == 0
    assert report["missing_handler_edges"] == ()
    assert report["required_text_surfaces"] == (
        "graph_summary",
        "graph_kinds",
        "graph_formats",
        "graph_checks",
        "explain_summaries",
        "symbol_detail",
        "symbol_parent",
        "symbol_references",
        "diagnostic_detail",
        "diagnostic_docs",
        "handler_match_count",
        "handler_edges",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_report_formats"] == ("appgen.graph-suite-report.v1", "appgen.explain-report.v1")
    assert report["emitted_report_formats"] == report["required_report_formats"]
    assert report["missing_report_format_count"] == 0
    assert report["missing_report_formats"] == ()
    assert report["required_reference_counts"] == ("references: 2",)
    assert report["emitted_reference_counts"] == report["required_reference_counts"]
    assert report["missing_reference_count_count"] == 0
    assert report["missing_reference_counts"] == ()
    assert report["required_match_counts"] == ("matches: 2",)
    assert report["emitted_match_counts"] == report["required_match_counts"]
    assert report["missing_match_count_count"] == 0
    assert report["missing_match_counts"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "graph-suite ok: format=appgen.graph-suite-report.v1 3 kinds, 3 formats"
    )
    assert {
        "graph-kinds er, lookup, workflow",
        "graph-formats json, mermaid, dot",
        "explain symbol ok: format=appgen.explain-report.v1 table.Invoice",
        "docs: docs/tooling.md#linter-rules-by-domain",
        "InvoiceForm.Save -> SubmitInvoice [operation]",
    } <= set(report["required_fragments"])


def test_parser_golden_text_renderer_contract_proves_fixture_log_markers() -> None:
    report = appgen_dsl._parser_golden_text_renderer_contract()

    assert report["format"] == "appgen.parser-golden-text-renderer.v1"
    assert report["ok"] is True
    assert report["required_fragment_count"] == len(report["required_fragments"])
    assert report["missing_fragment_count"] == 0
    assert report["marker_line_count"] >= 4
    assert report["summary_line_count"] == 1
    assert report["covered_construct_line_count"] == 1
    assert report["missing_construct_line_count"] == 1
    assert report["blocking_gap_line_count"] == 1
    assert report["required_covered_constructs"] == ("apps", "tables", "agents")
    assert report["emitted_covered_constructs"] == report["required_covered_constructs"]
    assert report["missing_covered_construct_count"] == 0
    assert report["missing_covered_constructs"] == ()
    assert report["required_missing_constructs"] == ("packages",)
    assert report["emitted_missing_constructs"] == report["required_missing_constructs"]
    assert report["missing_missing_construct_count"] == 0
    assert report["missing_missing_constructs"] == ()
    assert report["required_gap_ids"] == ("packages_valid_fixture",)
    assert report["emitted_gap_ids"] == report["required_gap_ids"]
    assert report["missing_gap_id_count"] == 0
    assert report["missing_gap_ids"] == ()
    assert report["required_text_surfaces"] == (
        "summary",
        "covered_constructs",
        "missing_constructs",
        "blocking_gaps",
    )
    assert report["emitted_text_surfaces"] == report["required_text_surfaces"]
    assert report["missing_text_surface_count"] == 0
    assert report["missing_text_surfaces"] == ()
    assert report["required_report_formats"] == ("appgen.parser-golden-audit.v1",)
    assert report["emitted_report_formats"] == report["required_report_formats"]
    assert report["missing_report_format_count"] == 0
    assert report["missing_report_formats"] == ()
    assert report["required_count_markers"] == (
        "fixtures=4",
        "valid=3",
        "invalid=1",
        "required=4",
        "constructs=3",
        "missing=1",
    )
    assert report["emitted_count_markers"] == report["required_count_markers"]
    assert report["missing_count_marker_count"] == 0
    assert report["missing_count_markers"] == ()
    assert report["missing_fragments"] == ()
    assert report["json_fallback"] is False
    assert report["text_prefix"].startswith(
        "parser-golden failed: format=appgen.parser-golden-audit.v1 fixtures=4"
    )
    assert {
        "covered-constructs apps, tables, agents",
        "missing-constructs packages",
        "fail packages_valid_fixture: Missing valid fixture for package declarations.",
    } <= set(report["required_fragments"])


def test_tooling_audit_text_summary_exposes_sections_gaps_and_formats() -> None:
    payload = {
        "format": "appgen.tooling-audit.v1",
        "ok": True,
        "passed": 5,
        "required": 5,
        "sections": (
            "docs/tooling.md#cli-contracts",
            "docs/tooling.md#implementation-phases",
            "docs/tooling.md#language-server-specification",
            "docs/tooling.md#non-goals",
            "docs/tooling.md#appgen-tooling-audit",
        ),
        "source_of_truth": "docs/tooling.md",
        "blocking_gaps": (),
        "checks": (
            {
                "id": "cli_contracts",
                "ok": True,
                "section": "docs/tooling.md#cli-contracts",
                "evidence": "CLI contracts are executable.",
                "detail": {"format": "appgen.cli-help-surface-audit.v1"},
            },
            {
                "id": "language_server_core_features",
                "ok": True,
                "section": "docs/tooling.md#language-server-specification",
                "evidence": "LSP features are executable.",
                "detail": {"rpc": {"format": "appgen.lsp-json-rpc-audit.v1"}},
            },
            {
                "id": "implementation_phase_exit_criteria",
                "ok": True,
                "section": "docs/tooling.md#implementation-phases",
                "evidence": "Implementation phases are executable.",
                "detail": {
                    "format": "appgen.tooling-implementation-phase-audit.v1",
                    "phases": ({"id": "phase_0_inventory_and_stabilization"},),
                    "missing_phases": (),
                },
            },
            {
                "id": "non_goal_policy_guards",
                "ok": True,
                "section": "docs/tooling.md#non-goals",
                "evidence": "Non-goal policy guards are executable.",
                "detail": {"format": "appgen.non-goal-policy-audit.v1"},
            },
            {
                "id": "tooling_doc_anchor_integrity",
                "ok": True,
                "section": "docs/tooling.md#appgen-tooling-audit",
                "evidence": "Tooling audit section references resolve.",
                "detail": {"format": "appgen.tooling-doc-anchor-audit.v1"},
            },
        ),
    }
    output = StringIO()

    with redirect_stdout(output):
        appgen_dsl._emit_tooling_payload(payload, as_json=False)

    text = output.getvalue()
    assert text.startswith("tooling-audit ok: format=appgen.tooling-audit.v1 5/5 checks blocking_gaps=0 sections=5 source=docs/tooling.md")
    assert "implementation-phases 1 missing=0 format=appgen.tooling-implementation-phase-audit.v1" in text
    assert "section docs/tooling.md#cli-contracts" in text
    assert "section docs/tooling.md#non-goals" in text
    assert "section docs/tooling.md#appgen-tooling-audit" in text
    assert "formats=appgen.cli-help-surface-audit.v1" in text
    assert "formats=appgen.lsp-json-rpc-audit.v1" in text
    assert "formats=appgen.tooling-implementation-phase-audit.v1" in text
    assert "formats=appgen.non-goal-policy-audit.v1" in text
    assert "formats=appgen.tooling-doc-anchor-audit.v1" in text


def test_tooling_doc_anchor_audit_proves_documented_contract_formats() -> None:
    root = Path(__file__).resolve().parents[1]
    report = appgen_dsl._tooling_audit_doc_anchor_integrity(
        root,
        (
            "docs/tooling.md#appgen-tooling-audit",
            "docs/tooling.md#cli-contracts",
        ),
    )

    assert report["format"] == "appgen.tooling-doc-anchor-audit.v1"
    assert report["ok"] is True
    assert report["missing_sections"] == ()
    assert report["documented_contract_format_count"] >= 50
    assert report["runtime_covered_format_count"] == report["documented_contract_format_count"]
    assert report["test_covered_format_count"] == report["documented_contract_format_count"]
    assert report["missing_runtime_formats"] == ()
    assert report["runtime_reference_gap_count"] == 0
    assert report["missing_test_formats"] == ()
    assert report["test_reference_gap_count"] == 0
    assert report["minimum_runtime_format_reference_count"] >= 1
    assert report["minimum_test_format_reference_count"] >= 1
    assert {
        "appgen.tooling-audit.v1",
        "appgen.tooling-doc-anchor-audit.v1",
        "appgen.studio-semantic-service.v1",
    } <= set(report["documented_contract_formats"])
    for format_name in (
        "appgen.tooling-audit.v1",
        "appgen.tooling-doc-anchor-audit.v1",
        "appgen.studio-semantic-service.v1",
    ):
        assert report["format_reference_matrix"][format_name]["docs"] >= 1
        assert report["format_reference_matrix"][format_name]["runtime"] >= 1
        assert report["format_reference_matrix"][format_name]["tests"] >= 1


def test_top_level_help_exposes_tooling_subcommands_and_apg_alias() -> None:
    root = Path(__file__).resolve().parents[1]
    audit = appgen_dsl._tooling_audit_cli_help_surface(root)
    help_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "--help"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    normalized_help = " ".join(help_result.stdout.split())

    assert help_result.returncode == 0, help_result.stderr
    assert "Tooling subcommands are also available" in normalized_help
    assert "lint, semantic, format, validate, generate, graph, graph-suite" in normalized_help
    assert "component-publish, pbc, designer-sync" in normalized_help
    assert "diagnostics, parser-golden, dsl-quality, dsl-antlr" in normalized_help
    assert "dsl-authoring-gate, dsl-language-service, drift, doctor, and tooling-audit" in normalized_help
    assert "apg =" in pyproject
    assert "visual drag-and-drop form design" in normalized_help
    assert audit["format"] == "appgen.cli-help-surface-audit.v1"
    assert audit["ok"] is True
    assert audit["script_targets"]["appgen"] == "pyAppGen.__main__:main"
    assert audit["script_targets"]["apg"] == audit["script_targets"]["appgen"]
    assert audit["command_alias_count"] == 2
    assert audit["entrypoint_dispatch_count"] == 2
    assert audit["failing_entrypoint_dispatch_count"] == 0
    assert audit["required_entrypoint_ids"] == ("python_module", "repo_alias")
    assert audit["observed_entrypoint_ids"] == audit["required_entrypoint_ids"]
    assert audit["missing_entrypoint_ids"] == ()
    assert audit["missing_entrypoint_id_count"] == 0
    assert audit["entrypoint_dispatch_ok_by_id"] == {"python_module": True, "repo_alias": True}
    assert audit["missing_entrypoint_dispatch_ids"] == ()
    assert audit["missing_entrypoint_dispatch_count"] == 0
    assert audit["expected_entrypoint_exit_codes_by_id"] == {"python_module": 0, "repo_alias": 0}
    assert audit["entrypoint_exit_codes_by_id"] == audit["expected_entrypoint_exit_codes_by_id"]
    assert audit["missing_entrypoint_exit_code_ids"] == ()
    assert audit["missing_entrypoint_exit_code_count"] == 0
    assert audit["expected_entrypoint_payload_formats_by_id"] == {
        "python_module": "appgen.lint-report.v1",
        "repo_alias": "appgen.lint-report.v1",
    }
    assert audit["entrypoint_payload_formats_by_id"] == audit["expected_entrypoint_payload_formats_by_id"]
    assert audit["missing_entrypoint_payload_format_ids"] == ()
    assert audit["missing_entrypoint_payload_format_count"] == 0
    assert audit["entrypoint_traceback_free_by_id"] == {"python_module": True, "repo_alias": True}
    assert audit["missing_entrypoint_traceback_free_ids"] == ()
    assert audit["missing_entrypoint_traceback_free_count"] == 0
    assert audit["alias_contract"]["format"] == "appgen.cli-alias-contract.v1"
    assert audit["alias_contract"]["ok"] is True
    assert audit["alias_contract"]["commands"] == ("appgen", "apg")
    assert audit["alias_contract"]["shared_target"] == "pyAppGen.__main__:main"
    assert audit["alias_contract"]["required_entrypoint_ids"] == audit["required_entrypoint_ids"]
    assert audit["alias_contract"]["observed_entrypoint_ids"] == audit["required_entrypoint_ids"]
    assert audit["alias_contract"]["missing_entrypoint_ids"] == ()
    assert audit["alias_contract"]["entrypoint_dispatch_ok_by_id"] == audit["entrypoint_dispatch_ok_by_id"]
    assert audit["alias_contract"]["missing_entrypoint_dispatch_ids"] == ()
    assert audit["alias_contract"]["entrypoint_exit_codes_by_id"] == audit["expected_entrypoint_exit_codes_by_id"]
    assert audit["alias_contract"]["missing_entrypoint_exit_code_ids"] == ()
    assert audit["alias_contract"]["entrypoint_payload_formats_by_id"] == (
        audit["expected_entrypoint_payload_formats_by_id"]
    )
    assert audit["alias_contract"]["missing_entrypoint_payload_format_ids"] == ()
    assert audit["alias_contract"]["entrypoint_traceback_free_by_id"] == audit["entrypoint_traceback_free_by_id"]
    assert audit["alias_contract"]["missing_entrypoint_traceback_free_ids"] == ()
    assert audit["alias_contract"]["module_dispatches_tooling"] is True
    assert audit["alias_contract"]["module_payload_format"] == "appgen.lint-report.v1"
    assert audit["alias_contract"]["repo_alias_dispatches_tooling"] is True
    assert audit["alias_contract"]["repo_alias_payload_format"] == "appgen.lint-report.v1"
    assert audit["repo_alias_command"]["ok"] is True
    assert audit["repo_alias_command"]["exists"] is True
    assert audit["repo_alias_command"]["path"] == "apg"
    assert audit["repo_alias_command"]["exit_code"] == 0
    assert audit["repo_alias_command"]["payload_format"] == "appgen.lint-report.v1"
    assert audit["repo_alias_command"]["traceback_free"] is True
    assert audit["help_exit_code"] == 0
    assert audit["help_lists_subcommands"] is True
    assert audit["required_subcommand_count"] == len(audit["required_subcommands"])
    assert audit["required_subcommand_count"] >= 20
    assert audit["documented_subcommand_count"] == audit["required_subcommand_count"]
    assert audit["documented_missing_subcommand_count"] == 0
    assert audit["documented_missing_subcommands"] == ()
    assert audit["help_listed_subcommand_count"] == audit["required_subcommand_count"]
    assert audit["listed_subcommand_count"] == audit["required_subcommand_count"]
    assert audit["help_missing_subcommand_count"] == 0
    assert audit["help_missing_subcommands"] == ()
    assert audit["subcommand_option_help_ok"] is True
    assert audit["subcommand_option_surface_count"] == len(audit["subcommand_option_help"])
    assert audit["subcommand_option_surface_count"] == len(audit["subcommand_option_surfaces"])
    assert audit["passing_option_surface_count"] == audit["subcommand_option_surface_count"]
    assert audit["failing_option_surface_count"] == 0
    assert audit["failing_option_surfaces"] == ()
    assert audit["option_help_exit_failure_count"] == 0
    assert audit["option_help_exit_failures"] == ()
    assert audit["required_option_count"] >= 50
    assert audit["missing_option_count"] == 0
    assert audit["top_level_help_byte_count"] > 400
    assert audit["subcommand_option_missing_details"] == ()
    assert audit["subcommand_option_help"]["component-publish"]["missing"] == ()
    assert audit["subcommand_option_help"]["lint"]["missing"] == ()
    assert audit["subcommand_option_help"]["lint"]["exit_code"] == 0
    assert audit["subcommand_option_help"]["lint"]["required_option_count"] >= 5
    assert audit["subcommand_option_help"]["semantic"]["missing"] == ()
    assert audit["subcommand_option_help"]["semantic"]["exit_code"] == 0
    assert audit["subcommand_option_help"]["migration-plan"]["missing"] == ()
    assert audit["subcommand_option_help"]["lsp"]["missing"] == ()
    assert audit["subcommand_option_help"]["dsl-quality"]["missing"] == ()
    assert audit["subcommand_option_help"]["dsl-antlr"]["missing"] == ()
    assert audit["subcommand_option_help"]["dsl-authoring-gate"]["missing"] == ()
    assert audit["subcommand_option_help"]["dsl-language-service"]["missing"] == ()
    assert audit["subcommand_option_help"]["pbc publish"]["missing"] == ()
    assert audit["subcommand_option_help"]["designer-sync"]["missing"] == ()
    assert audit["module_entrypoint"]["ok"] is True
    assert audit["module_entrypoint"]["exit_code"] == 0
    assert audit["module_entrypoint"]["payload_format"] == "appgen.lint-report.v1"
    assert audit["module_entrypoint"]["traceback_free"] is True


def test_semantic_cli_audit_proves_directory_json_and_text_contracts(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_semantic_source_set_cli(tmp_path)

    assert audit["format"] == "appgen.semantic-source-set-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["json_exit_code"] == 0
    assert audit["text_exit_code"] == 0
    assert audit["payload_format"] == "appgen.semantic-model.v1"
    assert audit["source_set_format"] == "appgen.semantic-source-set.v1"
    assert audit["source_mode"] == "directory"
    assert audit["file_count"] == audit["expected_file_count"] == 5
    assert audit["missing_file_count"] == 0
    assert audit["missing_table_count"] == 0
    assert audit["missing_view_count"] == 0
    assert audit["missing_flow_count"] == 0
    assert audit["missing_symbol_file_count"] == 0
    assert audit["files_without_symbols_count"] == 0
    assert audit["error_diagnostic_count"] == 0
    assert audit["missing_text_marker_count"] == 0
    assert audit["text_json_fallback"] is False


def test_dsl_language_cli_audit_proves_quality_authoring_and_service_commands(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_dsl_language_cli(tmp_path, TOOLING_SAMPLE)

    assert audit["format"] == "appgen.dsl-language-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 8
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["failing_cases"] == ()
    assert audit["required_case_ids"] == (
        "dsl_quality_json",
        "dsl_antlr_json",
        "dsl_authoring_gate_json",
        "dsl_language_service_json",
        "dsl_quality_text",
        "dsl_antlr_text",
        "dsl_authoring_gate_text",
        "dsl_language_service_text",
    )
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["json_case_count"] == 4
    assert audit["text_case_count"] == 4
    assert audit["expected_payload_formats_by_case"] == {
        "dsl_quality_json": "appgen.dsl-language-quality.v1",
        "dsl_antlr_json": "appgen.dsl-antlr-integrity.v1",
        "dsl_authoring_gate_json": "appgen.dsl-authoring-release-gate.v1",
        "dsl_language_service_json": "appgen.dsl-language-service.v1",
    }
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["expected_exit_codes_by_case"] == {
        "dsl_quality_json": 0,
        "dsl_antlr_json": 0,
        "dsl_authoring_gate_json": 0,
        "dsl_language_service_json": 0,
        "dsl_quality_text": 0,
        "dsl_antlr_text": 0,
        "dsl_authoring_gate_text": 0,
        "dsl_language_service_text": 0,
    }
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {
        "dsl_quality_json": True,
        "dsl_antlr_json": True,
        "dsl_authoring_gate_json": True,
        "dsl_language_service_json": True,
        "dsl_quality_text": True,
        "dsl_antlr_text": True,
        "dsl_authoring_gate_text": True,
        "dsl_language_service_text": True,
    }
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["expected_text_exit_codes_by_case"] == {
        "dsl_quality_text": 0,
        "dsl_antlr_text": 0,
        "dsl_authoring_gate_text": 0,
        "dsl_language_service_text": 0,
    }
    assert audit["text_exit_codes_by_case"] == audit["expected_text_exit_codes_by_case"]
    assert audit["missing_text_exit_code_case_count"] == 0
    assert audit["missing_text_exit_code_cases"] == ()
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_marker_cases"] == ()
    assert all(markers == () for markers in audit["missing_text_markers_by_case"].values())
    assert audit["text_marker_count"] == sum(
        len(markers) for markers in audit["required_text_markers_by_case"].values()
    )
    assert audit["text_json_fallback_by_case"] == {
        "dsl_quality_text": False,
        "dsl_antlr_text": False,
        "dsl_authoring_gate_text": False,
        "dsl_language_service_text": False,
    }
    assert audit["text_json_fallback_case_count"] == 0
    assert audit["text_json_fallback_cases"] == ()
    assert audit["language_quality_format"] == "appgen.dsl-language-quality.v1"
    assert audit["antlr_integrity_format"] == "appgen.dsl-antlr-integrity.v1"
    assert audit["authoring_gate_format"] == "appgen.dsl-authoring-release-gate.v1"
    assert audit["language_service_format"] == "appgen.dsl-language-service.v1"
    assert audit["completion_count"] > 0
    assert {
        "dsl_quality_json",
        "dsl_antlr_json",
        "dsl_authoring_gate_json",
        "dsl_language_service_json",
        "dsl_quality_text",
        "dsl_antlr_text",
        "dsl_authoring_gate_text",
        "dsl_language_service_text",
    } == {case["case"] for case in audit["cases"]}


def test_contract_schema_catalog_exposes_core_json_schemas() -> None:
    catalog = appgen_dsl.contract_schema_catalog_dsl()
    semantic = appgen_dsl.contract_schema_catalog_dsl("appgen.semantic-model.v1")
    missing = appgen_dsl.contract_schema_catalog_dsl("appgen.missing-contract.v1")

    assert catalog["format"] == "appgen.contract-schema-catalog.v1"
    assert catalog["ok"] is True
    assert catalog["schema_dialect"] == "https://json-schema.org/draft/2020-12/schema"
    assert catalog["required_schema_count"] == len(appgen_dsl.CONTRACT_SCHEMA_REQUIRED_FORMATS)
    assert set(catalog["required_schema_formats"]) == set(appgen_dsl.CONTRACT_SCHEMA_REQUIRED_FORMATS)
    assert {
        "appgen.format-result.v1",
        "appgen.validate-report.v1",
        "appgen.generate-report.v1",
        "appgen.graph-suite-report.v1",
        "appgen.explain-report.v1",
        "appgen.symbol-coverage.v1",
        "appgen.semantic-source-set.v1",
        "appgen.semantic-file-report.v1",
        "appgen.semantic-source-set-cli-audit.v1",
        "appgen.module-boundary-audit.v1",
        "appgen.non-goal-policy-audit.v1",
        "appgen.dsl-keyword-budget.v1",
        "appgen.dsl-antlr-integrity.v1",
        "appgen.dsl-language-quality.v1",
        "appgen.dsl-language-cli-audit.v1",
        "appgen.lint-directory-cli-audit.v1",
        "appgen.lint-text-renderer.v1",
        "appgen.format-text-renderer.v1",
        "appgen.formatter-contract-audit.v1",
        "appgen.validate-generate-text-renderer.v1",
        "appgen.validate-generate-cli-audit.v1",
        "appgen.graph-explain-text-renderer.v1",
        "appgen.graph-cli-format-audit.v1",
        "appgen.graph-suite-cli-audit.v1",
        "appgen.explain-cli-audit.v1",
        "appgen.lsp-service.v1",
        "appgen.lsp-capabilities.v1",
        "appgen.lsp-diagnostics.v1",
        "appgen.lsp-completion.v1",
        "appgen.completion-coverage.v1",
        "appgen.lsp-hover.v1",
        "appgen.lsp-lookup-hover.v1",
        "appgen.lsp-relationship-hover.v1",
        "appgen.lsp-handler-target-hover.v1",
        "appgen.lsp-pbc-hover.v1",
        "appgen.lsp-definition.v1",
        "appgen.lsp-references.v1",
        "appgen.lsp-document-symbols.v1",
        "appgen.lsp-workspace-symbols.v1",
        "appgen.lsp-symbol-coverage.v1",
        "appgen.lsp-code-actions.v1",
        "appgen.lsp-code-action-apply.v1",
        "appgen.lsp-code-action-apply-audit.v1",
        "appgen.lsp-code-action-cli-audit.v1",
        "appgen.lsp-formatting.v1",
        "appgen.lsp-rename.v1",
        "appgen.lsp-rename-cli-audit.v1",
        "appgen.lsp-json-rpc-audit.v1",
        "appgen.lsp-stdio-transport-audit.v1",
        "appgen.lsp-service-text-renderer.v1",
        "appgen.lsp-code-action-text-renderer.v1",
        "appgen.internal-error.v1",
        "appgen.internal-error-exit-audit.v1",
        "appgen.missing-input-exit-audit.v1",
        "appgen.missing-required-option-exit-audit.v1",
        "appgen.invalid-choice-exit-audit.v1",
        "appgen.cli-alias-contract.v1",
        "appgen.cli-help-surface-audit.v1",
        "appgen.designer-sync-report.v1",
        "appgen.designer-sync-text-renderer.v1",
        "appgen.designer-visual-transaction-result.v1",
        "appgen.designer-visual-edit-matrix.v1",
        "appgen.studio-semantic-service.v1",
        "appgen.studio-semantic-service-audit.v1",
        "appgen.frontend-semantic-service-audit.v1",
        "appgen.frontend-interaction-audit.v1",
        "appgen.vscode-extension-audit.v1",
        "appgen.diagnostic-catalog.v1",
        "appgen.diagnostic-fixture-audit.v1",
        "appgen.diagnostics-text-renderer.v1",
        "appgen.parser-golden-audit.v1",
        "appgen.parser-golden-text-renderer.v1",
        "appgen.semantic-drift-audit.v1",
        "appgen.semantic-drift-text-renderer.v1",
        "appgen.migration-plan.v1",
        "appgen.migration-coverage.v1",
        "appgen.migration-plan-text-renderer.v1",
        "appgen.migration-cli-audit.v1",
        "appgen.migration-semantic-input-cli-audit.v1",
        "appgen.nl-plan.v1",
        "appgen.nl-plan-contract-audit.v1",
        "appgen.nl-plan-cli-audit.v1",
        "appgen.release-verifier-report.v1",
        "appgen.release-evidence-bundle.v1",
        "appgen.release-verifier-text-renderer.v1",
        "appgen.package-manifest.v1",
        "appgen.package-verify-cli-audit.v1",
        "appgen.component-publish-report.v1",
        "appgen.component-catalog-patch.v1",
        "appgen.component-publish-text-renderer.v1",
        "appgen.pbc-package-verifier.v1",
        "appgen.pbc-publish-report.v1",
        "appgen.pbc-publish-text-renderer.v1",
        "appgen.pbc-cli-text-audit.v1",
        "appgen.doctor-report.v1",
        "appgen.doctor-cli-audit.v1",
        "appgen.doctor-text-renderer.v1",
        "appgen.tooling-audit-text-renderer.v1",
        "appgen.tooling-doc-anchor-audit.v1",
        "appgen.tooling-section-coverage-audit.v1",
        "appgen.tooling-implementation-phase-audit.v1",
        "appgen.implementation-phase-doc-alignment.v1",
        "appgen.test-family-contract-audit.v1",
        "appgen.contributor-task-contract-audit.v1",
        "appgen.priority-order-contract-audit.v1",
        "appgen.contract-schema-cli-audit.v1",
        "appgen.contract-validation-cli-audit.v1",
    } <= set(catalog["required_schema_formats"])
    assert catalog["missing_required_schema_count"] == 0
    assert catalog["missing_required_schema_formats"] == ()
    assert catalog["schema_count"] == catalog["required_schema_count"]
    assert all(schema["$schema"] == catalog["schema_dialect"] for schema in catalog["schemas"].values())
    assert semantic["ok"] is True
    assert semantic["selected_formats"] == ("appgen.semantic-model.v1",)
    semantic_schema = semantic["schemas"]["appgen.semantic-model.v1"]
    assert semantic_schema["title"] == "appgen.semantic-model.v1"
    assert {"format", "ok", "app", "symbols", "tables", "views", "diagnostics"} <= set(
        semantic_schema["required"]
    )
    diagnostic_schema = catalog["schemas"]["appgen.diagnostic.v1"]
    assert diagnostic_schema["title"] == "appgen.diagnostic.v1"
    assert {"code", "severity", "message"} <= set(diagnostic_schema["required"])
    assert missing["ok"] is False
    assert missing["missing_requested_schema_formats"] == ("appgen.missing-contract.v1",)


def test_contract_schema_cli_audit_proves_schema_command_modes() -> None:
    audit = appgen_dsl._tooling_audit_contract_schema_cli()

    assert audit["format"] == "appgen.contract-schema-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 4
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["required_case_ids"] == (
        "catalog_json",
        "single_semantic_json",
        "missing_schema_json",
        "catalog_text",
    )
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["required_schema_count"] == len(appgen_dsl.CONTRACT_SCHEMA_REQUIRED_FORMATS)
    assert audit["missing_required_schema_count"] == 0
    assert audit["missing_required_schema_formats"] == ()
    assert audit["sample_validation_case_count"] == len(appgen_dsl.CONTRACT_SCHEMA_REQUIRED_FORMATS)
    assert audit["sample_validation_passing_count"] == audit["sample_validation_case_count"]
    assert audit["sample_validation_failing_count"] == 0
    assert audit["sample_validation_failing_formats"] == ()
    assert audit["sample_validation_missing_count"] == 0
    assert audit["sample_validation_missing_formats"] == ()
    assert {"format", "ok", "app", "symbols", "tables", "views", "diagnostics"} <= set(
        audit["semantic_required_fields"]
    )
    assert audit["expected_exit_codes_by_case"] == {
        "catalog_json": 0,
        "single_semantic_json": 0,
        "missing_schema_json": 1,
        "catalog_text": 0,
    }
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_markers"] == ()
    assert audit["text_json_fallback"] is False
    assert audit["text_prefix"].startswith("contract-schema ok: format=appgen.contract-schema-catalog.v1")


def test_contract_validation_cli_audit_proves_payload_validation_modes(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_contract_validation_cli(tmp_path)

    assert audit["format"] == "appgen.contract-validation-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 7
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["required_case_ids"] == (
        "valid_inferred_json",
        "self_report_json",
        "valid_explicit_json",
        "missing_required_json",
        "unknown_schema_json",
        "malformed_json",
        "valid_text",
    )
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["expected_exit_codes_by_case"] == {
        "valid_inferred_json": 0,
        "self_report_json": 0,
        "valid_explicit_json": 0,
        "missing_required_json": 1,
        "unknown_schema_json": 1,
        "malformed_json": 1,
        "valid_text": 0,
    }
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_markers"] == ()
    assert audit["text_json_fallback"] is False
    assert audit["valid_report_format"] == "appgen.contract-validation-report.v1"
    assert audit["valid_payload_format"] == "appgen.semantic-model.v1"
    assert audit["valid_schema_format"] == "appgen.semantic-model.v1"
    assert audit["self_report_payload_format"] == "appgen.contract-validation-report.v1"
    assert audit["self_report_schema_format"] == "appgen.contract-validation-report.v1"
    assert audit["missing_required_error_count"] >= 1
    assert audit["unknown_schema_available"] is False
    assert audit["malformed_diagnostic_count"] >= 1
    assert audit["text_prefix"].startswith("contract-validate ok: format=appgen.contract-validation-report.v1")


def test_cli_contracts_cover_text_summaries_exit_codes_and_bad_arguments(tmp_path: Path) -> None:
    source_path = tmp_path / "release.appgen"
    output_dir = tmp_path / "generated"
    source_path.write_text(RELEASE_SAMPLE, encoding="utf-8")
    lint_current_path = tmp_path / "lint-current.appgen"
    lint_previous_path = tmp_path / "lint-previous-semantic.json"
    lint_previous_source = "app LintText { targets: web }\ntable Customer { id: int pk }\n"
    lint_current_path.write_text(
        "app LintText { targets: web }\ntable Customer { id: int pk; name: string }\n",
        encoding="utf-8",
    )
    lint_previous_path.write_text(
        json.dumps(semantic_model_dsl(lint_previous_source, source_name="lint-previous.appgen"), indent=2, default=list),
        encoding="utf-8",
    )
    root = Path(__file__).resolve().parents[1]

    lint_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "lint", str(source_path)],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    lint_migration_text = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lint",
            str(lint_current_path),
            "--previous-semantic",
            str(lint_previous_path),
        ],
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
    validate_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "validate", str(source_path), "--targets", "web"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    explain_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "explain", str(source_path), "--symbol", "table.Invoice"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    explain_json = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "explain", str(source_path), "--diagnostic", "AGX0303", "--json"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    explain_diagnostic_text = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "explain", str(source_path), "--diagnostic", "AGX0303"],
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
    invalid_graph_kind = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "graph", str(source_path), "--kind", "unknown", "--format", "json"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    invalid_migration_backend = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "migration-plan",
            str(source_path),
            str(source_path),
            "--backend",
            "oracle",
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    missing_input_path = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "graph", str(tmp_path / "missing.appgen"), "--format", "json"],
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
    assert "format=appgen.lint-report.v1" in lint_text.stdout
    assert "stages syntax=0 semantic=1 policy=0" in lint_text.stdout
    assert lint_migration_text.returncode == 0, lint_migration_text.stderr
    assert "migration-preview format=appgen.migration-plan.v1 backend=postgresql: changes=1 requires_approval=False" in lint_migration_text.stdout
    assert "migration-detected added_field" in lint_migration_text.stdout
    assert format_check.returncode == 1
    assert "format changed: format=appgen.format-result.v1 idempotent" in format_check.stdout
    assert "format=appgen.format-result.v1" in format_check.stdout
    assert "organize=False write_requested=False written=False" in format_check.stdout
    assert graph_suite_text.returncode == 0, graph_suite_text.stderr
    assert "graph-suite ok: format=appgen.graph-suite-report.v1 9 kinds, 3 formats" in graph_suite_text.stdout
    assert "graph-kinds er, lookup, workflow, handler, pbc, security, agent, deployment, package" in graph_suite_text.stdout
    assert "graph-formats json, mermaid, dot" in graph_suite_text.stdout
    assert validate_text.returncode == 0, validate_text.stderr
    assert validate_text.stdout.startswith("validate ok: format=appgen.validate-report.v1 requested=web")
    assert "app_targets=web,mobile,desktop" in validate_text.stdout
    assert "format=appgen.validate-report.v1" in validate_text.stdout
    assert "semantic_format=appgen.semantic-model.v1" in validate_text.stdout
    assert explain_text.returncode == 0, explain_text.stderr
    assert explain_text.stdout.startswith("explain symbol ok: format=appgen.explain-report.v1 table.Invoice")
    assert "table.Invoice: table Invoice" in explain_text.stdout
    assert not explain_text.stdout.lstrip().startswith("{")
    assert explain_json.returncode == 0, explain_json.stderr
    assert json.loads(explain_json.stdout)["format"] == "appgen.explain-report.v1"
    assert explain_diagnostic_text.returncode == 0, explain_diagnostic_text.stderr
    assert explain_diagnostic_text.stdout.startswith("explain diagnostic ok: format=appgen.explain-report.v1 AGX0303")
    assert "AGX0303: Unresolved lookup path" in explain_diagnostic_text.stdout
    assert "docs: docs/tooling.md#diagnostic-specification" in explain_diagnostic_text.stdout
    assert doctor_text.returncode == 0, doctor_text.stderr
    assert doctor_text.stdout.startswith("doctor ok: format=appgen.doctor-report.v1 checks=")
    assert "blocking_gaps=0" in doctor_text.stdout
    assert "detail_format=appgen.parser-golden-audit.v1" in doctor_text.stdout
    assert "detail_format=appgen.cli-alias-contract.v1" in doctor_text.stdout
    assert "detail_format=appgen.completion-coverage.v1" in doctor_text.stdout
    assert "detail_format=appgen.symbol-coverage.v1" in doctor_text.stdout
    assert "detail_format=appgen.module-boundary-audit.v1" in doctor_text.stdout
    assert "detail_format=appgen.designer-sync-report.v1" in doctor_text.stdout
    assert "detail_format=appgen.vscode-extension-audit.v1" in doctor_text.stdout
    assert generate_text.returncode == 0, generate_text.stderr
    assert "generate ok: format=appgen.generate-report.v1 generated=True" in generate_text.stdout
    assert "targets=web" in generate_text.stdout
    assert "format=appgen.generate-report.v1" in generate_text.stdout
    assert "semantic_format=appgen.semantic-model.v1" in generate_text.stdout
    assert "output_dir " in generate_text.stdout
    assert "manifest " in generate_text.stdout
    assert "artifact appgen.json" in generate_text.stdout
    assert invalid_graph_format.returncode == 2
    assert "invalid choice" in invalid_graph_format.stderr
    assert invalid_graph_kind.returncode == 2
    assert "invalid choice" in invalid_graph_kind.stderr
    assert invalid_migration_backend.returncode == 2
    assert "invalid choice" in invalid_migration_backend.stderr
    assert missing_input_path.returncode == 2
    assert "path does not exist" in missing_input_path.stderr
    assert "Traceback" not in missing_input_path.stderr
    assert missing_required_arg.returncode == 2
    assert "--out" in missing_required_arg.stderr


def test_missing_input_audit_covers_file_based_commands(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_missing_input_exit(tmp_path)
    cases = {case["name"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.missing-input-exit-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["case_ids"] == tuple(case["name"] for case in audit["cases"])
    assert audit["failing_cases"] == ()
    assert audit["command_family_count"] == len(audit["command_families"])
    assert set(audit["required_command_families"]) <= set(audit["command_families"])
    assert audit["missing_command_family_count"] == 0
    assert audit["missing_command_families"] == ()
    assert {
        "lint",
        "semantic",
        "format",
        "validate",
        "graph",
        "graph-suite",
        "explain",
        "generate",
        "migration-plan",
        "nl-plan",
        "lsp",
        "verify",
        "package",
        "designer-sync",
        "dsl-authoring-gate",
        "dsl-language-service",
        "drift",
    } <= set(audit["command_families"])
    assert audit["missing_path_message_count"] == audit["case_count"]
    assert audit["missing_path_message_missing_count"] == 0
    assert audit["missing_path_message_missing_cases"] == ()
    assert audit["stdout_empty_count"] == audit["case_count"]
    assert audit["traceback_free_count"] == audit["case_count"]
    assert audit["stdout_non_empty_case_count"] == 0
    assert audit["stdout_non_empty_cases"] == ()
    assert audit["traceback_case_count"] == 0
    assert audit["traceback_cases"] == ()
    assert audit["expected_exit_code"] == 2
    assert audit["unexpected_exit_code_case_count"] == 0
    assert audit["unexpected_exit_code_cases"] == ()
    assert {
        "lint_missing_path",
        "lint_missing_previous_semantic",
        "lint_missing_catalog",
        "semantic_missing_path",
        "format_missing_path",
        "validate_missing_path",
        "graph_missing_path",
        "graph_suite_missing_path",
        "explain_missing_path",
        "generate_missing_path",
        "migration_missing_previous",
        "migration_missing_current",
        "nl_plan_missing_path",
        "lsp_missing_path",
        "verify_missing_path",
        "package_missing_path",
        "designer_sync_missing_path",
        "dsl_authoring_gate_missing_path",
        "dsl_language_service_missing_path",
        "drift_missing_path",
    } <= set(cases)
    assert all(case["exit_code"] == 2 for case in cases.values())
    assert all("path does not exist" in case["stderr"] for case in cases.values())
    assert all("Traceback" not in case["stderr"] for case in cases.values())
    assert all(case["stdout_empty"] is True for case in cases.values())


def test_explain_cli_audit_covers_text_and_json_modes(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_explain_cli_formats(tmp_path, TOOLING_SAMPLE)
    cases = {case["case"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.explain-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["case_count"] == 6
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["failing_cases"] == ()
    assert audit["case_ids"] == tuple(case["case"] for case in audit["cases"])
    expected_case_ids = (
        "field_symbol_text",
        "field_symbol_json",
        "diagnostic_text",
        "diagnostic_json",
        "qualified_handler_text",
        "qualified_handler_json",
    )
    assert audit["required_case_ids"] == expected_case_ids
    assert audit["observed_case_ids"] == expected_case_ids
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["expected_output_modes_by_case"] == {
        "field_symbol_text": "text",
        "field_symbol_json": "json",
        "diagnostic_text": "text",
        "diagnostic_json": "json",
        "qualified_handler_text": "text",
        "qualified_handler_json": "json",
    }
    assert audit["output_modes_by_case"] == audit["expected_output_modes_by_case"]
    assert audit["missing_output_mode_case_count"] == 0
    assert audit["missing_output_mode_cases"] == ()
    assert audit["expected_exit_codes_by_case"] == {case_id: 0 for case_id in expected_case_ids}
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {case_id: True for case_id in expected_case_ids}
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["expected_payload_formats_by_case"] == {
        "field_symbol_json": "appgen.explain-report.v1",
        "diagnostic_json": "appgen.explain-report.v1",
        "qualified_handler_json": "appgen.explain-report.v1",
    }
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["exit_failure_count"] == 0
    assert audit["text_case_count"] == 3
    assert audit["json_case_count"] == 3
    assert audit["report_format_case_count"] == audit["case_count"]
    assert audit["missing_report_format_count"] == 0
    assert audit["required_report_format_cases"] == expected_case_ids
    assert audit["report_format_cases"] == expected_case_ids
    assert audit["missing_report_format_cases"] == ()
    assert audit["text_report_format_case_count"] == audit["text_case_count"]
    assert audit["json_report_format_case_count"] == audit["json_case_count"]
    assert audit["required_text_markers_by_case"] == {
        "field_symbol_text": "explain symbol ok: format=appgen.explain-report.v1 Invoice.customer_id",
        "diagnostic_text": "explain diagnostic ok: format=appgen.explain-report.v1 AGX0303",
        "qualified_handler_text": "explain handler ok: format=appgen.explain-report.v1 InvoiceForm.Save",
    }
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_marker_cases"] == ()
    assert audit["missing_text_markers_by_case"] == {}
    assert audit["text_json_fallback_by_case"] == {
        "field_symbol_text": False,
        "diagnostic_text": False,
        "qualified_handler_text": False,
    }
    assert audit["text_json_fallback_case_count"] == 0
    assert audit["text_json_fallback_cases"] == ()
    assert audit["symbol_case_count"] == 2
    assert audit["diagnostic_case_count"] == 2
    assert audit["handler_case_count"] == 2
    assert audit["navigation_detail_case_count"] == 3
    assert audit["navigation_detail_cases"] == (
        "field_symbol_json",
        "diagnostic_json",
        "qualified_handler_json",
    )
    assert audit["required_navigation_detail_cases"] == audit["navigation_detail_cases"]
    assert audit["missing_navigation_detail_case_count"] == 0
    assert audit["missing_navigation_detail_cases"] == ()
    assert audit["symbol_navigation_detail_count"] == 1
    assert audit["diagnostic_navigation_detail_count"] == 1
    assert audit["handler_navigation_detail_count"] == 1
    assert set(expected_case_ids) <= set(cases)
    assert all(case["exit_code"] == 0 for case in cases.values())
    assert all(case["has_report_format"] is True for case in cases.values())
    assert cases["field_symbol_text"]["stdout_prefix"].startswith(
        "explain symbol ok: format=appgen.explain-report.v1 Invoice.customer_id"
    )
    assert cases["diagnostic_text"]["stdout_prefix"].startswith(
        "explain diagnostic ok: format=appgen.explain-report.v1 AGX0303"
    )
    assert cases["qualified_handler_text"]["stdout_prefix"].startswith(
        "explain handler ok: format=appgen.explain-report.v1 InvoiceForm.Save"
    )
    assert cases["field_symbol_json"]["symbol_id"] == "table.Invoice.customer_id"
    assert cases["field_symbol_json"]["symbol_kind"] == "field"
    assert cases["field_symbol_json"]["symbol_parent"] == "table.Invoice"
    assert cases["field_symbol_json"]["symbol_reference_count"] == 0
    assert cases["diagnostic_json"]["diagnostic_title"] == "Unresolved lookup path"
    assert cases["diagnostic_json"]["diagnostic_docs_url"] == "docs/tooling.md#diagnostic-specification"
    assert cases["qualified_handler_json"]["handler_match_count"] == 1
    assert cases["qualified_handler_json"]["handler_edges"] == ("InvoiceForm.Save->SubmitInvoice",)


def test_graph_cli_audit_covers_documented_graph_examples(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_graph_cli_formats(tmp_path, TOOLING_SAMPLE)
    cases = {case["case"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.graph-cli-format-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["case_ids"] == tuple(case["case"] for case in audit["cases"])
    expected_case_ids = (
        "er_mermaid",
        "lookup_json",
        "workflow_json",
        "workflow_mermaid",
        "handler_mermaid",
        "pbc_dot",
        "security_dot",
        "agent_json",
        "deployment_dot",
        "package_mermaid",
    )
    assert audit["required_case_ids"] == expected_case_ids
    assert audit["observed_case_ids"] == expected_case_ids
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["failing_cases"] == ()
    assert audit["expected_exit_codes_by_case"] == {case_id: 0 for case_id in expected_case_ids}
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {case_id: True for case_id in expected_case_ids}
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["expected_formats_by_case"] == {
        "er_mermaid": "mermaid",
        "lookup_json": "json",
        "workflow_json": "json",
        "workflow_mermaid": "mermaid",
        "handler_mermaid": "mermaid",
        "pbc_dot": "dot",
        "security_dot": "dot",
        "agent_json": "json",
        "deployment_dot": "dot",
        "package_mermaid": "mermaid",
    }
    assert audit["formats_by_case"] == audit["expected_formats_by_case"]
    assert audit["missing_format_case_count"] == 0
    assert audit["missing_format_cases"] == ()
    assert audit["graph_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert set(audit["covered_graph_kinds"]) == set(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert audit["missing_required_kind_count"] == 0
    assert audit["missing_required_kinds"] == ()
    assert audit["output_format_count"] == 3
    assert set(audit["covered_output_formats"]) == {"mermaid", "json", "dot"}
    assert audit["json_case_count"] == 3
    assert audit["mermaid_case_count"] == 4
    assert audit["dot_case_count"] == 3
    assert audit["payload_format_case_count"] == audit["json_case_count"]
    assert audit["expected_payload_formats_by_case"] == {
        "lookup_json": "appgen.graph-report.v1",
        "workflow_json": "appgen.graph-report.v1",
        "agent_json": "appgen.graph-report.v1",
    }
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["text_marker_case_count"] == audit["mermaid_case_count"] + audit["dot_case_count"]
    assert audit["required_text_markers_by_case"]["er_mermaid"] == "graph TD"
    assert audit["required_text_markers_by_case"]["pbc_dot"] == "digraph appgen"
    assert audit["missing_text_marker_count"] == 0
    assert audit["missing_text_marker_cases"] == ()
    assert audit["missing_text_markers_by_case"] == {}
    assert audit["text_json_fallback_case_count"] == 0
    assert audit["text_json_fallback_cases"] == ()
    assert audit["text_json_fallback_by_case"] == {
        "er_mermaid": False,
        "workflow_mermaid": False,
        "handler_mermaid": False,
        "pbc_dot": False,
        "security_dot": False,
        "deployment_dot": False,
        "package_mermaid": False,
    }
    assert set(expected_case_ids) <= set(cases)
    assert cases["er_mermaid"]["kind"] == "er"
    assert cases["er_mermaid"]["format"] == "mermaid"
    assert cases["lookup_json"]["kind"] == "lookup"
    assert cases["lookup_json"]["payload_format"] == "appgen.graph-report.v1"
    assert cases["workflow_json"]["kind"] == "workflow"
    assert cases["workflow_json"]["format"] == "json"
    assert cases["workflow_json"]["payload_format"] == "appgen.graph-report.v1"
    assert cases["handler_mermaid"]["stdout_prefix"].startswith("graph TD")
    assert cases["workflow_mermaid"]["stdout_prefix"].startswith("graph TD")
    assert cases["pbc_dot"]["kind"] == "pbc"
    assert cases["pbc_dot"]["format"] == "dot"
    assert cases["pbc_dot"]["stdout_prefix"].startswith("digraph appgen")
    assert cases["security_dot"]["stdout_prefix"].startswith("digraph appgen")
    assert cases["agent_json"]["payload_format"] == "appgen.graph-report.v1"
    assert cases["deployment_dot"]["stdout_prefix"].startswith("digraph appgen")
    assert cases["package_mermaid"]["stdout_prefix"].startswith("graph TD")
    assert all(case["exit_code"] == 0 for case in cases.values())


def test_graph_suite_cli_audit_proves_all_required_renderings(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_graph_suite_cli(tmp_path, TOOLING_SAMPLE)

    assert audit["format"] == "appgen.graph-suite-cli-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == 2
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["failing_cases"] == ()
    assert audit["required_case_ids"] == ("graph_suite_json", "graph_suite_text")
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["modes_by_case"] == audit["expected_modes_by_case"]
    assert audit["missing_mode_case_count"] == 0
    assert audit["missing_mode_cases"] == ()
    assert audit["exit_codes_by_case"] == audit["expected_exit_codes_by_case"]
    assert audit["missing_exit_code_case_count"] == 0
    assert audit["missing_exit_code_cases"] == ()
    assert audit["ok_by_case"] == {"graph_suite_json": True, "graph_suite_text": True}
    assert audit["missing_ok_case_count"] == 0
    assert audit["missing_ok_cases"] == ()
    assert audit["payload_formats_by_case"] == audit["expected_payload_formats_by_case"]
    assert audit["missing_payload_format_case_count"] == 0
    assert audit["missing_payload_format_cases"] == ()
    assert audit["text_json_fallback_by_case"] == {"graph_suite_text": False}
    assert audit["text_json_fallback_case_count"] == 0
    assert audit["text_json_fallback_cases"] == ()
    assert audit["required_kind_count"] == len(audit["required_kinds"])
    assert audit["missing_required_kind_count"] == 0
    assert audit["missing_required_kinds"] == ()
    assert audit["output_format_count"] == len(audit["formats"])
    assert audit["expected_rendering_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS) * len(appgen_dsl.GRAPH_TEXT_FORMATS)
    assert audit["present_rendering_count"] == audit["expected_rendering_count"]
    assert audit["complete_rendering_kind_count"] == len(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert set(audit["complete_rendering_kinds"]) == set(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert audit["missing_rendering_count"] == 0
    assert audit["missing_format_count"] == 0
    assert set(audit["required_kinds"]) == set(appgen_dsl.REQUIRED_GRAPH_KINDS)
    assert tuple(audit["formats"]) == ("json", "mermaid", "dot")
    assert audit["missing_renderings"] == ()
    assert all(
        set(formats) == {"json", "mermaid", "dot"}
        for formats in audit["rendering_formats_by_kind"].values()
    )
    assert audit["text_fragment_count"] == 3
    assert audit["text_fragment_ids"] == ("summary_format", "graph_kinds", "graph_formats")
    assert audit["missing_text_fragment_count"] == 0
    assert audit["missing_text_fragments"] == ()
    assert audit["text_has_report_format"] is True
    assert audit["text_has_kinds"] is True
    assert audit["text_has_formats"] is True


def test_invalid_choice_audit_covers_graph_formats_and_backend_choices(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_invalid_choice_exit(tmp_path)
    cases = {case["name"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.invalid-choice-exit-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["case_ids"] == tuple(case["name"] for case in audit["cases"])
    assert audit["failing_cases"] == ()
    assert audit["invalid_choice_message_count"] == audit["case_count"]
    assert audit["missing_invalid_choice_message_count"] == 0
    assert audit["missing_invalid_choice_message_cases"] == ()
    assert audit["stdout_empty_count"] == audit["case_count"]
    assert audit["traceback_free_count"] == audit["case_count"]
    assert audit["stdout_non_empty_case_count"] == 0
    assert audit["stdout_non_empty_cases"] == ()
    assert audit["traceback_case_count"] == 0
    assert audit["traceback_cases"] == ()
    assert audit["expected_exit_code"] == 2
    assert audit["unexpected_exit_code_case_count"] == 0
    assert audit["unexpected_exit_code_cases"] == ()
    assert {
        "lint_backend",
        "graph_kind",
        "graph_format",
        "migration_backend",
        "nl_backend",
        "verify_target",
        "package_target",
        "pbc_publish_catalog",
    } <= set(cases)
    assert all(case["exit_code"] == 2 for case in cases.values())
    assert all("invalid choice" in case["stderr"] for case in cases.values())
    assert all("Traceback" not in case["stderr"] for case in cases.values())


def test_missing_required_option_audit_covers_required_cli_options(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_missing_required_option_exit(tmp_path)
    cases = {case["name"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.missing-required-option-exit-audit.v1"
    assert audit["ok"] is True
    assert audit["case_count"] == len(audit["cases"])
    assert audit["passing_case_count"] == audit["case_count"]
    assert audit["failing_case_count"] == 0
    assert audit["observed_case_ids"] == audit["required_case_ids"]
    assert audit["missing_case_count"] == 0
    assert audit["missing_case_ids"] == ()
    assert audit["case_ids"] == tuple(case["name"] for case in audit["cases"])
    assert audit["failing_cases"] == ()
    assert audit["expected_message_count"] == audit["case_count"]
    assert audit["missing_expected_message_count"] == 0
    assert audit["missing_expected_message_cases"] == ()
    assert audit["expected_messages_by_case"]["explain_missing_selector"] == "one of the arguments"
    assert audit["stdout_empty_count"] == audit["case_count"]
    assert audit["traceback_free_count"] == audit["case_count"]
    assert audit["stdout_non_empty_case_count"] == 0
    assert audit["stdout_non_empty_cases"] == ()
    assert audit["traceback_case_count"] == 0
    assert audit["traceback_cases"] == ()
    assert audit["expected_exit_code"] == 2
    assert audit["unexpected_exit_code_case_count"] == 0
    assert audit["unexpected_exit_code_cases"] == ()
    assert {
        "generate_missing_out",
        "nl_plan_missing_prompt",
        "component_publish_missing_component",
        "explain_missing_selector",
    } <= set(cases)
    assert all(case["exit_code"] == 2 for case in cases.values())
    assert all(case["expected_message"] in case["stderr"] for case in cases.values())
    assert all("Traceback" not in case["stderr"] for case in cases.values())


def test_format_write_audit_covers_json_check_and_text_write_contracts(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_format_write(tmp_path)

    assert audit["format"] == "appgen.format-write-audit.v1"
    assert audit["ok"] is True
    assert audit["scenario_count"] == 5
    assert audit["passing_scenario_count"] == audit["scenario_count"]
    assert audit["failing_scenario_count"] == 0
    assert audit["scenario_ids"] == (
        "dirty_check_json",
        "clean_check_json",
        "organize_json",
        "write_json",
        "write_text",
    )
    assert audit["failing_scenarios"] == ()
    assert audit["blocking_gap_count"] == 0
    assert audit["blocking_gaps"] == ()
    assert audit["write_mode_count"] == 2
    assert audit["check_mode_count"] == 2
    assert audit["organize_category_count"] == 7
    assert audit["payload_format"] == "appgen.format-result.v1"
    assert audit["check_exit_code"] == 1
    assert audit["check_changed"] is True
    assert audit["check_write_requested"] is False
    assert audit["check_written"] is False
    assert audit["text_exit_code"] == 0
    assert audit["text_has_report_format"] is True
    assert audit["text_has_write_metadata"] is True
    assert audit["text_stdout_prefix"].startswith("format changed: format=appgen.format-result.v1")
    assert audit["organize_table_body_order"] == (
        "identity:id",
        "business_key:invoice_number",
        "relationship:customer_id",
        "editable:subtotal",
        "calculated:total",
        "audit:updated_at",
        "directive:index",
    )


def test_appgen_format_write_rewrites_file_and_reports_write_metadata(tmp_path: Path) -> None:
    source_path = tmp_path / "format.appgen"
    text_source_path = tmp_path / "format-text.appgen"
    unformatted = "app FormatWrite { targets: web }\ntable Invoice { total: decimal; id: int pk }\n"
    source_path.write_text(
        unformatted,
        encoding="utf-8",
    )
    text_source_path.write_text(unformatted, encoding="utf-8")
    root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "format", str(source_path), "--write", "--json"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [sys.executable, "-m", "pyAppGen", "format", str(text_source_path), "--write"],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert payload["format"] == "appgen.format-result.v1"
    assert payload["write_requested"] is True
    assert payload["written"] is True
    assert payload["write_path"] == str(source_path)
    assert source_path.read_text(encoding="utf-8") == payload["text"]
    assert source_path.read_text(encoding="utf-8") != unformatted
    assert text_result.returncode == 0, text_result.stderr
    assert text_result.stdout.startswith("format changed: format=appgen.format-result.v1 idempotent written")
    assert "organize=False write_requested=True written=True" in text_result.stdout
    assert f"write_path {text_source_path}" in text_result.stdout
    assert text_source_path.read_text(encoding="utf-8") != unformatted


def test_appgen_tooling_cli_returns_code_3_for_internal_errors(tmp_path: Path) -> None:
    source_path = tmp_path / "internal.appgen"
    malformed_catalog = tmp_path / "malformed-components.json"
    source_path.write_text("app Internal { targets: web }\ntable Thing { id: int pk }\n", encoding="utf-8")
    malformed_catalog.write_text("{not-json", encoding="utf-8")
    root = Path(__file__).resolve().parents[1]

    json_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lint",
            str(source_path),
            "--catalog",
            str(malformed_catalog),
            "--json",
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )
    text_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyAppGen",
            "lint",
            str(source_path),
            "--catalog",
            str(malformed_catalog),
        ],
        check=False,
        cwd=root,
        text=True,
        capture_output=True,
    )

    assert json_result.returncode == 3
    payload = json.loads(json_result.stdout)
    assert payload["format"] == "appgen.internal-error.v1"
    assert payload["code"] == "AGX9000"
    assert payload["ok"] is False
    assert "Traceback" not in json_result.stderr
    assert text_result.returncode == 3
    assert text_result.stdout.startswith("internal-error failed: format=appgen.internal-error.v1")
    assert "code=AGX9000" in text_result.stdout
    assert "Traceback" not in text_result.stderr


def test_internal_error_audit_covers_json_and_text_modes(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_internal_error_exit(tmp_path)

    assert report["format"] == "appgen.internal-error-exit-audit.v1"
    assert report["ok"] is True
    assert report["mode_count"] == 2
    assert report["passing_mode_count"] == report["mode_count"]
    assert report["traceback_free_mode_count"] == report["mode_count"]
    assert report["json_exit_code"] == 3
    assert report["text_exit_code"] == 3
    assert report["payload_format"] == "appgen.internal-error.v1"
    assert report["code"] == "AGX9000"
    assert report["json_traceback_free"] is True
    assert report["text_traceback_free"] is True
    assert report["text_stdout"].startswith("internal-error failed: format=appgen.internal-error.v1")
    assert "code=AGX9000" in report["text_stdout"]
