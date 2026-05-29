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
    assert set(coverage["required"]) <= set(coverage["detected"])
    assert coverage["counts"]["group"] == 1
    assert coverage["counts"]["component_binding"] == 1
    assert coverage["counts"]["permission"] >= 3
    assert coverage["counts"]["agent_skill"] >= 2
    assert coverage["counts"]["deployment_unit"] == 1
    assert any(symbol["kind"] == "component_binding" and symbol["name"] == "customer.name" for symbol in model["symbols"].values())
    assert any(symbol["kind"] == "deployment_unit" and symbol["name"] == "SubmitInvoice" for symbol in model["symbols"].values())


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
    assert {Path(item).name for item in report["files"]} == {"finance.appgen", "broken.appgen"}
    assert len(report["file_reports"]) == 2
    assert any(item["code"] == "AGX0201" and Path(item["file"]).name == "broken.appgen" for item in report["diagnostics"])
    assert memory_report["source_mode"] == "directory"


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


def test_lint_directory_audit_covers_strict_component_cli_gate(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_lint_directory_cli(tmp_path, TOOLING_SAMPLE)

    assert report["format"] == "appgen.lint-directory-cli-audit.v1"
    assert report["ok"] is True
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
    assert any(check["check"] == "target_compatibility" and check["ok"] for check in validation["checks"])
    assert graph["format"] == "appgen.graph-report.v1"
    assert graph["graph"]["edges"][0]["from"] == "Invoice"


def test_validate_report_rejects_unknown_or_undeclared_targets() -> None:
    source = "app WebOnly { targets: web }\n\ntable Thing { id: int pk }\n"

    missing = validate_report_dsl(source, source_name="web.appgen", targets=("mobile",))
    unknown = validate_report_dsl(source, source_name="web.appgen", targets=("satellite",))

    assert missing["ok"] is False
    assert missing["checks"][-1]["missing_targets"] == ("mobile",)
    assert any(item["code"] == "AGX0802" for item in missing["diagnostics"])
    assert unknown["ok"] is False
    assert unknown["checks"][-1]["unknown_targets"] == ("satellite",)
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
    assert f"semantic={bad_payload['semantic_model']['format']}" in bad_text_result.stdout
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
    assert f"lint {payload['lint']['format']}: ok={payload['lint']['ok']}" in text_result.stdout
    assert (
        f"migration-preview {payload['migration_preview']['format']} postgresql: "
        f"changes={len(payload['migration_preview']['changes'])} "
        f"requires_approval={payload['migration_preview']['requires_approval']}"
    ) in text_result.stdout


def test_nl_plan_contract_audit_covers_supported_edit_operations_and_rejections() -> None:
    audit = nl_plan_contract_audit_dsl(TOOLING_SAMPLE, source_name="finance.appgen")
    case_ids = {case["id"] for case in audit["cases"]}

    assert audit["format"] == "appgen.nl-plan-contract-audit.v1"
    assert audit["ok"] is True
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
    assert audit["blocking_gaps"] == ()


def test_nl_plan_cli_audit_covers_all_supported_edit_operations(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_nl_plan_cli(tmp_path, TOOLING_SAMPLE)
    contract = nl_plan_contract_audit_dsl(TOOLING_SAMPLE, source_name="finance.appgen")

    assert audit["format"] == "appgen.nl-plan-cli-audit.v1"
    assert audit["ok"] is True
    assert set(audit["accepted_operation_kinds"]) >= set(contract["required_edit_operations"])
    assert audit["accepted_case_count"] == len(contract["required_edit_operations"])
    assert audit["blocking_cases"] == ()
    assert audit["accepted_patch_bytes"] > 0
    assert audit["accepted_test_count"] >= len(contract["required_edit_operations"])
    assert audit["accepted_token_budget_notes"] >= len(contract["required_edit_operations"])
    assert "AGX1201" in audit["rejected_diagnostic_codes"]


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
    assert f"migration-coverage {payload['coverage']['format']}" in text_result.stdout
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
    assert audit["blocking_gaps"] == ()
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
    assert audit["blocking_gaps"] == ()
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
    assert report["safe_ok"] is True
    assert report["rename_format"] == "appgen.lsp-rename.v1"
    assert report["token"] == "SubmitInvoice"
    assert report["new_name"] == "PostInvoice"
    assert report["changed"] is True
    assert report["migration_format"] == "appgen.migration-plan.v1"
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
    assert "migration=appgen.migration-plan.v1" in report["blocked_text"]
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
    assert text_result.stdout.startswith("lsp ok: format=appgen.lsp-service.v1 semantic=appgen.semantic-model.v1")
    assert f"diagnostics={len(payload['publishDiagnostics']['diagnostics'])}" in text_result.stdout
    assert f"completions={len(payload['completion']['items'])}" in text_result.stdout
    assert f"actions={len(payload['codeAction']['actions'])}" in text_result.stdout
    assert f"symbols={len(payload['documentSymbol']['symbols'])}" in text_result.stdout
    assert f"workspace_symbols={len(payload['workspaceSymbol']['symbols'])}" in text_result.stdout
    assert "source_of_truth=appgen.semantic-model.v1" in text_result.stdout
    assert f"completion_coverage={payload['completionCoverage']['format']}" in text_result.stdout
    assert f"missing={len(payload['completionCoverage']['missing'])}" in text_result.stdout
    assert f"definition={payload['definition']['format']} ok={payload['definition']['ok']}" in text_result.stdout
    assert f"references={payload['references']['format']} locations={len(payload['references']['locations'])}" in text_result.stdout
    assert f"formatting={payload['formatting']['format']} edits={len(payload['formatting']['edits'])}" in text_result.stdout
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
    assert audit["diagnostic_publication_count"] >= 2
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
    assert languages[0]["id"] == "appgen"
    assert {".appgen", ".ag", ".ags"} <= set(languages[0]["extensions"])
    assert package["contributes"]["grammars"][0]["path"] == "./syntaxes/appgen.tmLanguage.json"
    assert {
        "appgen.lint",
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
    assert language_config["comments"]["lineComment"] == "//"
    assert grammar["scopeName"] == "source.appgen"
    assert '["lsp", "--stdio"]' in source
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
    assert {".appgen", ".ag", ".ags"} <= set(audit["language_extensions"])
    assert "onLanguage:appgen" in audit["activation_events"]
    assert audit["checks"]["diagnostics_collection"] is True
    assert audit["checks"]["cli_command_contracts"] is True
    assert audit["checks"]["webview_renderers"] is True
    assert '["generate", file, "--out", out, "--allow-warnings", "--json"]' in audit["command_cli_markers"]


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
    assert "release-evidence appgen.release-evidence-bundle.v1: artifacts=1" in text_result.stdout
    assert "graph-suite appgen.graph-suite-report.v1: kinds=9 formats=3" in text_result.stdout
    assert "ok mobile" in text_result.stdout
    assert f"artifact release_evidence: {output_dir / 'text' / 'appgen-release-evidence.json'}" in text_result.stdout
    assert f"artifact mobile_package_manifest: {output_dir / 'text' / 'appgen-package-mobile.json'}" in text_result.stdout
    assert verify_text.returncode == 0, verify_text.stderr
    assert verify_text.stdout.startswith("release-verify ok: format=appgen.release-verifier-report.v1 targets=mobile written=0")
    assert "release-evidence appgen.release-evidence-bundle.v1: artifacts=1" in verify_text.stdout
    assert "graph-suite appgen.graph-suite-report.v1: kinds=9 formats=3" in verify_text.stdout
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
    assert "release-evidence appgen.release-evidence-bundle.v1" in result.stdout
    assert "graph-suite appgen.graph-suite-report.v1: kinds=9 formats=3" in result.stdout
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
        "designer-sync ok: format=appgen.designer-sync-report.v1 semantic=appgen.semantic-model.v1"
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
    assert report["valid_exit"] == 0
    assert report["valid_payload_format"] == "appgen.designer-sync-report.v1"
    assert report["valid_round_trip"] is True
    assert "database_designer" in report["valid_changed_surfaces"]
    assert report["valid_diff_lines"] > 0
    assert report["valid_semantic_model_format"] == "appgen.semantic-model.v1"
    assert report["valid_projection_format"] == "appgen.designer-database-projection.v1"
    assert report["valid_projection_semantic_model_format"] == "appgen.semantic-model.v1"


def test_diagnostic_catalog_and_fixture_audit_cover_required_agx_codes() -> None:
    catalog = diagnostic_catalog_dsl()
    audit = diagnostic_fixture_audit_dsl()

    assert catalog["format"] == "appgen.diagnostic-catalog.v1"
    assert audit["format"] == "appgen.diagnostic-fixture-audit.v1"
    assert catalog["ok"] is True
    assert audit["ok"] is True
    assert catalog["catalog_shape_gaps"] == ()
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
    assert set(catalog["catalog_fields"]) == {
        "code",
        "severity",
        "title",
        "trigger",
        "example_fix",
        "docs_url",
        "fixture",
    }
    assert all(set(catalog["catalog_fields"]) <= set(item) for item in catalog["diagnostics"])
    assert set(catalog["required_codes"]) == set(catalog["covered_fixture_codes"])
    assert set(catalog["required_codes"]) <= set(audit["covered_codes"])
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
    assert catalog_text.stdout.startswith("diagnostics ok:")
    assert f"format={catalog_payload['format']}" in catalog_text.stdout
    assert f"covered={len(catalog_payload['covered_fixture_codes'])}" in catalog_text.stdout
    assert f"required={len(catalog_payload['required_codes'])}" in catalog_text.stdout
    assert f"fixtures={catalog_payload['fixture_count']}" in catalog_text.stdout
    assert "missing=0" in catalog_text.stdout
    assert "missing-fixture " not in catalog_text.stdout
    assert audit_text.stdout.startswith("diagnostics-audit ok:")
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
    assert audit["valid_fixture_count"] >= 1
    assert audit["invalid_fixture_count"] >= 1
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
    assert text_result.stdout.startswith("parser-golden ok:")
    assert f"{payload['fixture_count']} fixtures" in text_result.stdout
    assert f"valid={payload['valid_fixture_count']}" in text_result.stdout
    assert f"invalid={payload['invalid_fixture_count']}" in text_result.stdout
    assert f"format={payload['format']}" in text_result.stdout
    assert f"required={len(payload['constructs_required'])}" in text_result.stdout
    assert f"constructs={len(payload['constructs_covered'])}" in text_result.stdout
    assert "missing=0" in text_result.stdout
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
    assert text_result.stdout.startswith("drift ok: format=appgen.semantic-drift-audit.v1 semantic=appgen.semantic-model.v1")
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
    assert audit["missing_boundaries"] == ()
    assert audit["core_runtime_gaps"] == ()
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
    assert all(boundary["missing_callables"] == () for boundary in audit["boundaries"])
    assert {item["boundary"] for item in audit["core_runtime"]} == {"parser", "semantic", "diagnostics", "formatter"}
    assert all(item["ok"] for item in audit["core_runtime"])


def test_doctor_report_checks_parser_catalog_generator_and_ide_hooks() -> None:
    report = doctor_report_dsl()

    assert report["format"] == "appgen.doctor-report.v1"
    assert report["ok"] is True
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
    assert alias_check["detail"]["commands"] == ("appgen", "apg")
    assert alias_check["detail"]["shared_target"] == "pyAppGen.__main__:main"
    assert alias_check["detail"]["module_dispatches_tooling"] is True


def test_studio_semantic_service_audit_proves_panel_contracts() -> None:
    report = appgen_dsl._tooling_audit_studio_semantic_service(TOOLING_SAMPLE)

    assert report["format"] == "appgen.studio-semantic-service-audit.v1"
    assert report["ok"] is True
    assert report["blocking_gaps"] == ()
    assert all(report["checks"].values())
    assert report["services"] == {
        "lsp": "appgen.lsp-service.v1",
        "designer_sync": "appgen.designer-sync-report.v1",
        "graph_suite": "appgen.graph-suite-report.v1",
        "natural_language_planner": "appgen.nl-plan.v1",
    }
    assert set(report["required_surfaces"]) <= set(report["surfaces"])
    assert report["surface_formats"]["diagnostics_panel"] == "appgen.lsp-diagnostics.v1"
    assert report["surface_formats"]["graph_explain_panel"] == "appgen.designer-graph-explain-panel.v1"
    assert report["surface_formats"]["natural_language_planner"] == "appgen.designer-nl-planner-panel.v1"
    assert all(value == "appgen.semantic-model.v1" for value in report["semantic_surface_formats"].values())
    assert report["checks"]["frontend_browser_smoke_bridge"] is True
    assert report["browser_smoke_format"] == "appgen.studio-browser-smoke-ci-contract.v1"
    assert "semantic_service_bridge" in report["browser_smoke_scenarios"]
    assert report["browser_smoke_checks"]["frontend_semantic_service_bridge"] is True


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
    assert json.loads(doctor_result.stdout)["format"] == "appgen.doctor-report.v1"
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
    assert f"semantic={blocked_payload['validation']['semantic_model']['format']}" in blocked_text.stdout
    assert f"output_dir {tmp_path / 'blocked-text'}" in blocked_text.stdout
    assert "gap lint_warnings" in blocked_text.stdout
    assert "warning AGX0404:" in blocked_text.stdout
    assert allowed.returncode == 0, allowed.stderr
    assert json.loads(allowed.stdout)["allow_warnings"] is True
    assert (allowed_dir / "appgen.json").exists()


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
        diagnostics=ok("appgen.diagnostic-catalog.v1"),
        diagnostic_fixtures=ok("appgen.diagnostic-fixture-audit.v1"),
        parser_golden=ok("appgen.parser-golden-audit.v1"),
        drift=ok("appgen.semantic-drift-audit.v1"),
        test_strategy_cli=ok("appgen.test-strategy-cli-audit.v1"),
        module_boundaries=ok("appgen.module-boundary-audit.v1"),
        lint=ok("appgen.lint-report.v1"),
        strict_lint=ok("appgen.lint-report.v1"),
        catalog_lint=ok("appgen.lint-report.v1"),
        lint_directory_cli=ok("appgen.lint-directory-cli-audit.v1"),
        formatted={"ok": True, "format": "appgen.format-result.v1", "idempotent": True},
        formatter_contract=ok("appgen.formatter-contract-audit.v1"),
        validation=ok("appgen.validate-report.v1"),
        validate_generate_cli=ok("appgen.validate-generate-cli-audit.v1"),
        cli_help_surface=ok("appgen.cli-help-surface-audit.v1"),
        graphs=ok("appgen.graph-suite-report.v1"),
        graph_cli=ok("appgen.graph-cli-audit.v1"),
        graph_suite_cli=ok("appgen.graph-suite-cli-audit.v1"),
        explain_cli=ok("appgen.explain-cli-audit.v1"),
        lsp=ok("appgen.lsp-service.v1"),
        lsp_rpc=ok("appgen.lsp-json-rpc-audit.v1"),
        lsp_stdio=ok("appgen.lsp-stdio-transport-audit.v1"),
        lsp_rename_cli=ok("appgen.lsp-rename-cli-audit.v1"),
        quick_fix=ok("appgen.lsp-code-action-apply.v1"),
        code_action_apply_audit=ok("appgen.lsp-code-action-apply-audit.v1"),
        lsp_apply_cli=ok("appgen.lsp-code-action-cli-audit.v1"),
        vscode=ok("appgen.vscode-extension-audit.v1"),
        studio=ok("appgen.studio-semantic-service-audit.v1"),
        designer=ok("appgen.designer-sync-report.v1"),
        designer_visual_edit_matrix=ok("appgen.designer-visual-edit-matrix.v1"),
        designer_sync_cli=ok("appgen.designer-sync-cli-audit.v1"),
        migration_detected=appgen_dsl.REQUIRED_MIGRATION_DETECTIONS,
        migration_cli=ok("appgen.migration-cli-audit.v1"),
        nl_plan={"ok": True, "format": "appgen.nl-plan.v1", "dsl_patch": "--- before\n+++ after"},
        nl_plan_contract=ok("appgen.nl-plan-contract-audit.v1"),
        nl_plan_cli=ok("appgen.nl-plan-cli-audit.v1"),
        release=ok("appgen.release-verifier-report.v1"),
        package=ok("appgen.release-verifier-report.v1"),
        package_verify_cli=ok("appgen.package-verify-cli-audit.v1"),
    )

    assert report["format"] == "appgen.tooling-implementation-phase-audit.v1"
    assert report["ok"] is True
    assert report["missing_phases"] == ()
    assert len(report["phases"]) == 7
    assert all(phase["missing_exit_criteria"] == () for phase in report["phases"])
    assert {
        criterion["id"]
        for phase in report["phases"]
        for criterion in phase["exit_criteria"]
    } >= {
        "current_behavior_documented",
        "semantic_model_contract",
        "formatter_idempotency",
        "graph_json_mermaid_and_dot",
        "rename_and_code_actions",
        "studio_semantic_bridge",
        "release_and_package_verifiers",
    }


def test_package_verify_cli_audit_exposes_web_manifest_readiness_metadata(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_package_verify_cli(tmp_path, TOOLING_SAMPLE)
    manifest_case = next(case for case in report["cases"] if case["case"] == "package_writes_target_manifests")

    assert report["format"] == "appgen.package-verify-cli-audit.v1"
    assert report["ok"] is True
    assert manifest_case["web_artifact_class"] == "web_application"
    assert {"routes", "forms", "handlers", "smoke_tests"} <= set(manifest_case["web_handoff_artifacts"])
    assert manifest_case["web_app_build_contract"] is True
    assert manifest_case["web_routes_declared"] is True
    assert manifest_case["web_forms_bind_valid_fields"] is True
    assert manifest_case["web_handler_targets_resolve"] is True
    assert manifest_case["web_smoke_tests_declared"] is True
    assert manifest_case["web_smoke_entrypoint"] == "web.smoke"


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
        "implementation_phase_exit_criteria",
        "language_server_core_features",
        "ide_visual_designer_round_trip",
        "vscode_extension_surface",
        "studio_semantic_service",
        "package_and_release_verifiers",
        "parser_golden_and_drift_gates",
        "tooling_doc_anchor_integrity",
        "non_goal_policy_guards",
    } <= {check["id"] for check in report["checks"]}
    non_goal_check = next(check for check in report["checks"] if check["id"] == "non_goal_policy_guards")
    assert non_goal_check["detail"]["format"] == "appgen.non-goal-policy-audit.v1"
    assert non_goal_check["detail"]["ok"] is True
    non_goal_cases = {case["case"]: case for case in non_goal_check["detail"]["cases"]}
    assert non_goal_cases["reject_secret_literal"]["secret_removed"] is True
    assert non_goal_cases["reject_secret_literal"]["fixed_contains_env_binding"] is True
    assert non_goal_cases["reject_runtime_picker_fields"]["picker_fields_removed"] is True
    assert non_goal_cases["reject_generated_code_bypass_prompt"]["accepted"] is False
    assert non_goal_cases["reject_generated_code_bypass_prompt"]["patch_bytes"] == 0
    assert report["doc_anchor_integrity"]["format"] == "appgen.tooling-doc-anchor-audit.v1"
    assert report["doc_anchor_integrity"]["ok"] is True
    assert report["doc_anchor_integrity"]["missing_sections"] == ()
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
    module_check = next(check for check in report["checks"] if check["id"] == "module_boundaries")
    assert module_check["detail"]["format"] == "appgen.module-boundary-audit.v1"
    assert module_check["detail"]["ok"] is True
    assert module_check["detail"]["missing_boundaries"] == ()
    assert module_check["detail"]["core_runtime_gaps"] == ()
    phase_check = next(check for check in report["checks"] if check["id"] == "implementation_phase_exit_criteria")
    assert phase_check["detail"]["format"] == "appgen.tooling-implementation-phase-audit.v1"
    assert phase_check["detail"]["ok"] is True
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
    vscode_check = next(check for check in report["checks"] if check["id"] == "vscode_extension_surface")
    assert vscode_check["detail"]["checks"]["diagnostics_collection"] is True
    assert vscode_check["detail"]["checks"]["cli_command_contracts"] is True
    assert vscode_check["detail"]["checks"]["webview_renderers"] is True
    designer_check = next(check for check in report["checks"] if check["id"] == "ide_visual_designer_round_trip")
    assert designer_check["detail"]["cli"]["format"] == "appgen.designer-sync-cli-audit.v1"
    assert designer_check["detail"]["cli"]["ok"] is True
    assert designer_check["detail"]["cli"]["valid_round_trip"] is True
    assert "database_designer" in designer_check["detail"]["cli"]["valid_changed_surfaces"]
    assert designer_check["detail"]["cli"]["valid_diff_lines"] > 0
    assert designer_check["detail"]["cli"]["valid_semantic_model_format"] == "appgen.semantic-model.v1"
    assert designer_check["detail"]["cli"]["valid_projection_semantic_model_format"] == "appgen.semantic-model.v1"
    assert designer_check["detail"]["cli"]["non_object_exit"] == 2
    assert "--edit-json must be a JSON object" in designer_check["detail"]["cli"]["non_object_stderr"]
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
    lsp_check = next(check for check in report["checks"] if check["id"] == "language_server_core_features")
    assert lsp_check["detail"]["rpc"]["format"] == "appgen.lsp-json-rpc-audit.v1"
    assert lsp_check["detail"]["rpc"]["blocking_gaps"] == ()
    assert lsp_check["detail"]["rename_cli"]["format"] == "appgen.lsp-rename-cli-audit.v1"
    assert lsp_check["detail"]["rename_cli"]["ok"] is True
    assert lsp_check["detail"]["rename_cli"]["rename_format"] == "appgen.lsp-rename.v1"
    assert lsp_check["detail"]["rename_cli"]["token"] == "SubmitInvoice"
    assert lsp_check["detail"]["rename_cli"]["new_name"] == "PostInvoice"
    assert lsp_check["detail"]["rename_cli"]["changed"] is True
    assert lsp_check["detail"]["rename_cli"]["migration_format"] == "appgen.migration-plan.v1"
    assert lsp_check["detail"]["rename_cli"]["safe_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["blocked_ok"] is True
    assert lsp_check["detail"]["rename_cli"]["blocked_rename_ok"] is False
    assert lsp_check["detail"]["rename_cli"]["blocked"] is True
    assert lsp_check["detail"]["rename_cli"]["blocked_text_ok"] is True
    assert "requires_approval=True" in lsp_check["detail"]["rename_cli"]["blocked_text"]
    assert lsp_check["detail"]["rename_cli"]["blocked_code"] == "AGX1101"
    assert lsp_check["detail"]["rename_cli"]["blocked_fix"] == "add_rename_hint"
    assert lsp_check["detail"]["rename_cli"]["blocked_requires_approval"] is True
    assert {
        "did_change_diagnostics",
        "code_action_request",
        "formatting_request",
    } <= {check["check"] for check in lsp_check["detail"]["rpc"]["checks"]}
    quick_fix_check = next(check for check in report["checks"] if check["id"] == "lsp_quick_fix_application")
    assert quick_fix_check["detail"]["cli"]["format"] == "appgen.lsp-code-action-cli-audit.v1"
    assert quick_fix_check["detail"]["cli"]["ok"] is True
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
    cli_check = next(check for check in report["checks"] if check["id"] == "cli_validation_and_generation_contracts")
    assert cli_check["detail"]["validate_generate_cli"]["format"] == "appgen.validate-generate-cli-audit.v1"
    assert cli_check["detail"]["validate_generate_cli"]["ok"] is True
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
    assert cli_check["detail"]["format_write"]["format"] == "appgen.format-write-audit.v1"
    assert cli_check["detail"]["format_write"]["ok"] is True
    assert cli_check["detail"]["format_write"]["check_exit_code"] == 1
    assert cli_check["detail"]["format_write"]["check_changed"] is True
    assert cli_check["detail"]["format_write"]["check_write_requested"] is False
    assert cli_check["detail"]["format_write"]["check_written"] is False
    assert cli_check["detail"]["format_write"]["clean_check_exit_code"] == 0
    assert cli_check["detail"]["format_write"]["clean_check_changed"] is False
    assert cli_check["detail"]["format_write"]["organize_exit_code"] == 0
    assert cli_check["detail"]["format_write"]["organize"] is True
    assert cli_check["detail"]["format_write"]["organize_idempotent"] is True
    assert cli_check["detail"]["format_write"]["organize_order"] == tuple(
        sorted(cli_check["detail"]["format_write"]["organize_order"])
    )
    assert cli_check["detail"]["internal_error_exit"]["format"] == "appgen.internal-error-exit-audit.v1"
    assert cli_check["detail"]["internal_error_exit"]["ok"] is True
    assert cli_check["detail"]["internal_error_exit"]["json_exit_code"] == 3
    assert cli_check["detail"]["internal_error_exit"]["text_exit_code"] == 3
    assert cli_check["detail"]["internal_error_exit"]["json_traceback_free"] is True
    assert cli_check["detail"]["internal_error_exit"]["text_traceback_free"] is True
    assert cli_check["detail"]["missing_required_option_exit"]["format"] == (
        "appgen.missing-required-option-exit-audit.v1"
    )
    assert cli_check["detail"]["missing_required_option_exit"]["ok"] is True
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
    } <= {case["name"] for case in cli_check["detail"]["invalid_choice_exit"]["cases"]}
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
    test_strategy_check = next(check for check in report["checks"] if check["id"] == "parser_golden_and_drift_gates")
    assert test_strategy_check["detail"]["cli"]["format"] == "appgen.test-strategy-cli-audit.v1"
    assert test_strategy_check["detail"]["cli"]["ok"] is True
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
    package_check = next(check for check in report["checks"] if check["id"] == "package_and_release_verifiers")
    assert package_check["detail"]["cli"]["format"] == "appgen.package-verify-cli-audit.v1"
    assert package_check["detail"]["cli"]["ok"] is True
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
    graph_check = next(check for check in report["checks"] if check["id"] == "graph_and_explain_tooling")
    assert graph_check["detail"]["cli"]["format"] == "appgen.graph-cli-format-audit.v1"
    assert graph_check["detail"]["cli"]["ok"] is True
    assert {
        "er_mermaid",
        "workflow_json",
        "workflow_mermaid",
        "pbc_dot",
    } <= {case["case"] for case in graph_check["detail"]["cli"]["cases"]}
    assert graph_check["detail"]["suite_cli"]["format"] == "appgen.graph-suite-cli-audit.v1"
    assert graph_check["detail"]["suite_cli"]["ok"] is True
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
    assert graph_check["detail"]["suite_cli"]["text_has_kinds"] is True
    assert graph_check["detail"]["suite_cli"]["text_has_formats"] is True
    assert graph_check["detail"]["explain_cli"]["format"] == "appgen.explain-cli-audit.v1"
    assert graph_check["detail"]["explain_cli"]["ok"] is True
    assert {
        "field_symbol_text",
        "field_symbol_json",
        "diagnostic_json",
        "qualified_handler_text",
        "qualified_handler_json",
    } <= {case["case"] for case in graph_check["detail"]["explain_cli"]["cases"]}
    nl_check = next(check for check in report["checks"] if check["id"] == "natural_language_patch_planner")
    assert nl_check["detail"]["cli"]["format"] == "appgen.nl-plan-cli-audit.v1"
    assert nl_check["detail"]["cli"]["ok"] is True
    assert set(nl_check["detail"]["cli"]["accepted_operation_kinds"]) >= set(
        nl_check["detail"]["contract"]["required_edit_operations"]
    )
    assert nl_check["detail"]["cli"]["accepted_case_count"] == len(nl_check["detail"]["contract"]["required_edit_operations"])
    assert nl_check["detail"]["cli"]["blocking_cases"] == ()
    assert nl_check["detail"]["cli"]["accepted_patch_bytes"] > 0
    assert nl_check["detail"]["cli"]["migration_format"] == "appgen.migration-plan.v1"
    assert nl_check["detail"]["cli"]["accepted_test_count"] > 0
    assert nl_check["detail"]["cli"]["accepted_token_budget_notes"] > 0
    assert "AGX1201" in nl_check["detail"]["cli"]["rejected_diagnostic_codes"]
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
    assert "lint, format, validate, generate, graph, graph-suite" in normalized_help
    assert "component-publish, pbc, designer-sync" in normalized_help
    assert "diagnostics, parser-golden, drift, doctor, and tooling-audit" in normalized_help
    assert "apg =" in pyproject
    assert "visual drag-and-drop form design" in normalized_help
    assert audit["format"] == "appgen.cli-help-surface-audit.v1"
    assert audit["ok"] is True
    assert audit["script_targets"]["appgen"] == "pyAppGen.__main__:main"
    assert audit["script_targets"]["apg"] == audit["script_targets"]["appgen"]
    assert audit["alias_contract"]["format"] == "appgen.cli-alias-contract.v1"
    assert audit["alias_contract"]["ok"] is True
    assert audit["alias_contract"]["commands"] == ("appgen", "apg")
    assert audit["alias_contract"]["shared_target"] == "pyAppGen.__main__:main"
    assert audit["alias_contract"]["module_dispatches_tooling"] is True
    assert audit["alias_contract"]["module_payload_format"] == "appgen.lint-report.v1"
    assert audit["help_exit_code"] == 0
    assert audit["help_lists_subcommands"] is True
    assert audit["help_missing_subcommands"] == ()
    assert audit["subcommand_option_help_ok"] is True
    assert audit["subcommand_option_help"]["component-publish"]["missing"] == ()
    assert audit["subcommand_option_help"]["lint"]["missing"] == ()
    assert audit["subcommand_option_help"]["lint"]["exit_code"] == 0
    assert audit["subcommand_option_help"]["migration-plan"]["missing"] == ()
    assert audit["subcommand_option_help"]["lsp"]["missing"] == ()
    assert audit["subcommand_option_help"]["pbc publish"]["missing"] == ()
    assert audit["subcommand_option_help"]["designer-sync"]["missing"] == ()
    assert audit["module_entrypoint"]["ok"] is True
    assert audit["module_entrypoint"]["exit_code"] == 0
    assert audit["module_entrypoint"]["payload_format"] == "appgen.lint-report.v1"
    assert audit["module_entrypoint"]["traceback_free"] is True


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
    assert "migration-preview appgen.migration-plan.v1 postgresql: changes=1 requires_approval=False" in lint_migration_text.stdout
    assert "migration-detected added_field" in lint_migration_text.stdout
    assert format_check.returncode == 1
    assert "format changed: idempotent" in format_check.stdout
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
    assert "semantic=appgen.semantic-model.v1" in validate_text.stdout
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
    assert "semantic=appgen.semantic-model.v1" in generate_text.stdout
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
    assert {
        "lint_missing_path",
        "lint_missing_previous_semantic",
        "lint_missing_catalog",
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
        "drift_missing_path",
    } <= set(cases)
    assert all(case["exit_code"] == 2 for case in cases.values())
    assert all("path does not exist" in case["stderr"] for case in cases.values())
    assert all("Traceback" not in case["stderr"] for case in cases.values())


def test_explain_cli_audit_covers_text_and_json_modes(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_explain_cli_formats(tmp_path, TOOLING_SAMPLE)
    cases = {case["case"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.explain-cli-audit.v1"
    assert audit["ok"] is True
    assert {
        "field_symbol_text",
        "field_symbol_json",
        "diagnostic_text",
        "diagnostic_json",
        "qualified_handler_text",
        "qualified_handler_json",
    } <= set(cases)
    assert all(case["exit_code"] == 0 for case in cases.values())


def test_graph_cli_audit_covers_documented_graph_examples(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_graph_cli_formats(tmp_path, TOOLING_SAMPLE)
    cases = {case["case"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.graph-cli-format-audit.v1"
    assert audit["ok"] is True
    assert {"er_mermaid", "workflow_json", "workflow_mermaid", "pbc_dot"} <= set(cases)
    assert cases["er_mermaid"]["kind"] == "er"
    assert cases["er_mermaid"]["format"] == "mermaid"
    assert cases["workflow_json"]["kind"] == "workflow"
    assert cases["workflow_json"]["format"] == "json"
    assert cases["workflow_json"]["payload_format"] == "appgen.graph-report.v1"
    assert cases["workflow_mermaid"]["stdout_prefix"].startswith("graph TD")
    assert cases["pbc_dot"]["kind"] == "pbc"
    assert cases["pbc_dot"]["format"] == "dot"
    assert cases["pbc_dot"]["stdout_prefix"].startswith("digraph appgen")
    assert all(case["exit_code"] == 0 for case in cases.values())


def test_invalid_choice_audit_covers_graph_formats_and_backend_choices(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_invalid_choice_exit(tmp_path)
    cases = {case["name"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.invalid-choice-exit-audit.v1"
    assert audit["ok"] is True
    assert {"lint_backend", "graph_kind", "graph_format", "migration_backend", "nl_backend"} <= set(cases)
    assert all(case["exit_code"] == 2 for case in cases.values())
    assert all("invalid choice" in case["stderr"] for case in cases.values())
    assert all("Traceback" not in case["stderr"] for case in cases.values())


def test_missing_required_option_audit_covers_required_cli_options(tmp_path: Path) -> None:
    audit = appgen_dsl._tooling_audit_missing_required_option_exit(tmp_path)
    cases = {case["name"]: case for case in audit["cases"]}

    assert audit["format"] == "appgen.missing-required-option-exit-audit.v1"
    assert audit["ok"] is True
    assert {"generate_missing_out", "nl_plan_missing_prompt", "component_publish_missing_component"} <= set(cases)
    assert all(case["exit_code"] == 2 for case in cases.values())
    assert all("the following arguments are required" in case["stderr"] for case in cases.values())
    assert all("Traceback" not in case["stderr"] for case in cases.values())


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
    assert text_result.stdout.startswith("format changed: idempotent written")
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
    assert text_result.stdout.startswith("internal-error format=appgen.internal-error.v1")
    assert "Traceback" not in text_result.stderr


def test_internal_error_audit_covers_json_and_text_modes(tmp_path: Path) -> None:
    report = appgen_dsl._tooling_audit_internal_error_exit(tmp_path)

    assert report["format"] == "appgen.internal-error-exit-audit.v1"
    assert report["ok"] is True
    assert report["json_exit_code"] == 3
    assert report["text_exit_code"] == 3
    assert report["payload_format"] == "appgen.internal-error.v1"
    assert report["code"] == "AGX9000"
    assert report["json_traceback_free"] is True
    assert report["text_traceback_free"] is True
    assert report["text_stdout"].startswith("internal-error format=appgen.internal-error.v1")
