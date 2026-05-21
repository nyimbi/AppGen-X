"""Test cases for the __main__ module."""
import json
import py_compile
import importlib.util
import re
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
import pytest

from click.testing import CliRunner
from sqlalchemy import Column
from sqlalchemy import Computed
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy import text

from pyAppGen import __main__
from pyAppGen.gen import generate_app_from_database
from pyAppGen.gen import generate_app_from_schema
from pyAppGen.dsl import apply_lint_fixes
from pyAppGen.dsl import dsl_code_actions
from pyAppGen.dsl import dsl_completion_items
from pyAppGen.dsl import dsl_language_service
from pyAppGen.dsl import dsl_language_quality_contract
from pyAppGen.dsl import dsl_keyword_budget
from pyAppGen.dsl import dsl_outline
from pyAppGen.dsl import format_dsl
from pyAppGen.dsl import lint_dsl
from pyAppGen.schema import load_schema
from pyAppGen.schema import RelationSchema
from pyAppGen.schema import schema_from_metadata
from pyAppGen.schema import schema_source_contract
from pyAppGen.schema import schema_source_kind


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_dsl_linter_reports_semantic_feedback(runner: CliRunner, tmp_path) -> None:
    """The DSL linter validates syntax, semantics, and CLI JSON output."""
    source = """
    app LintDemo { targets: web, mobile }
    table Author { id: int pk; name: string required; }
    table Book { id: int pk; title: string required; author_id: int -> Author.id [many-to-one]; }
    view BookForm for Book { Main: title, author_id; @ title TextBox 0 0 6 1; }
    """
    report = lint_dsl(source, source_name="inline")
    assert report["ok"] is True
    assert report["summary"]["tables"] == 2
    assert report["summary"]["targets"] == ("web", "mobile")
    assert report["language_quality"]["format"] == "appgen.dsl-language-quality.v1"
    assert report["language_quality"]["ok"] is True
    assert report["language_quality"]["canonical_keyword_count"] == 17
    assert "ref" not in report["language_quality"]["keywords"]
    assert report["language_quality"]["legacy_contextual_tokens"] == ("ref",)
    assert dsl_keyword_budget()["count"] <= dsl_keyword_budget()["limit"]
    assert dsl_keyword_budget()["canonical_keyword_count"] == 17
    assert dsl_keyword_budget()["legacy_contextual_tokens"] == ("ref",)
    assert dsl_keyword_budget()["modifier_aliases"] == {"hide": "hidden", "searchable": "search"}
    assert dsl_language_quality_contract()["grammar"] == "lang/appgen.g4"
    assert dsl_language_quality_contract()["ok"] is True
    broken = lint_dsl("app Bad { targets: web, toaster } table Book { title: string }")
    assert broken["ok"] is False
    assert any("Unknown app targets" in error for error in broken["errors"])
    semantic = lint_dsl(
        """
        app Broken { targets: web }
        table Book { id: int pk; title: string; }
        view BookForm for Book { Main: missing; @ other TextBox 0 0 6 1; }
        llm Local { provider: ollama; mode: local; model: llama3; }
        agent Helper { provider: MissingProvider; goal: "Help"; }
        """
    )
    assert semantic["ok"] is False
    assert any("Unknown view field: BookForm.missing" in error for error in semantic["errors"])
    assert any("Unknown component field: BookForm.other" in error for error in semantic["errors"])
    assert any("Unknown agent provider: Helper.MissingProvider" in error for error in semantic["errors"])
    typo = lint_dsl(
        """
        app Typo { targets: web }
        table Book { id: int pk; title: string; summary: string; }
        view BookForm for Book { Main: titel; @ summry TextArea 0 0 6 2; }
        llm LocalModel { provider: ollama; mode: local; }
        agent Helper { provider: LocalModl; goal: "Help"; }
        """
    )
    assert typo["ok"] is False
    assert "diagnostics" in typo
    assert any(item["code"] == "unknown_view_field" for item in typo["diagnostics"])
    assert any(item.get("hint") == "title" for item in typo["diagnostics"])
    assert any(item.get("hint") == "summary" for item in typo["diagnostics"])
    assert any(item.get("hint") == "LocalModel" for item in typo["diagnostics"])
    assert all("severity" in item and "message" in item for item in typo["diagnostics"])
    style = lint_dsl(
        "app Style { targets: web } table Book { id: int pk; author_id: int ref Author.id } "
        "llm Cloud { provider: openai; mode: api; model: gpt; api_key: \"secret\" }"
    )
    assert any("Prefer arrow references" in warning for warning in style["warnings"])
    assert any("environment variable" in warning for warning in style["warnings"])
    assert any(item["code"] == "prefer_arrow_reference" for item in style["diagnostics"])
    assert any("replace_ref_with_arrow" in item["fix_ids"] for item in style["diagnostics"])
    assert style["severity_counts"]["warning"] >= 2
    assert {"replace_ref_with_arrow", "use_api_key_env"}.issubset(
        {fix["id"] for fix in style["fixes"]}
    )
    actions = dsl_code_actions(
        "app Bad { targets: web, toaster } table Book { id: int pk; author_id: int ref Author.id }",
        source_name="inline",
    )
    assert {action["id"] for action in actions} >= {"replace_ref_with_arrow", "normalize_targets"}
    target_action = next(action for action in actions if action["id"] == "normalize_targets")
    assert target_action["format"] == "appgen.dsl-code-action.v1"
    assert target_action["diagnostic_codes"] == ("unknown_app_target",)
    assert target_action["edits"][0]["replacement"] == "web"
    ref_action = next(action for action in actions if action["id"] == "replace_ref_with_arrow")
    assert "author_id: int -> Author.id" in ref_action["fixed_preview"]
    assert any(fix["id"] == "normalize_targets" for fix in broken["fixes"])
    fixed = apply_lint_fixes(
        "app Bad { targets: web, toaster } table Author { id: int pk } table Book { id: int pk; author_id: int ref Author.id } "
        "llm Cloud { provider: openai; mode: api; model: gpt; api_key: \"secret\" }"
    )
    assert fixed["format"] == "appgen.dsl-fix-result.v1"
    assert fixed["changed"] is True
    assert {"replace_ref_with_arrow", "use_api_key_env", "normalize_targets"}.issubset(
        set(fixed["applied"])
    )
    assert "author_id: int -> Author.id" in fixed["fixed"]
    assert "api_key: OPENAI_API_KEY" in fixed["fixed"]
    assert "toaster" not in fixed["fixed"]
    assert fixed["after"]["summary"]["targets"] == ("web",)
    alias_source = """
    app AliasDemo { targets: web }
    entity Author { id: int pk; name: string required }
    entity Book { id: int pk; author_id: int -> Author.id }
    form BookForm for Book { Main: author_id; }
    workflow Publish { draft -> live }
    """
    alias_report = lint_dsl(alias_source)
    assert alias_report["ok"] is True
    assert any("canonical DSL words" in warning for warning in alias_report["warnings"])
    assert "normalize_authoring_aliases" in {fix["id"] for fix in alias_report["fixes"]}
    alias_fixed = apply_lint_fixes(alias_source)
    assert "table Author" in alias_fixed["fixed"]
    assert "view BookForm for Book" in alias_fixed["fixed"]
    assert "flow Publish" in alias_fixed["fixed"]
    assert alias_fixed["after"]["ok"] is True
    modifier_alias_source = """
    app ModifierAliasDemo { targets: web }
    table Book { id: int pk; title: string required searchable; secret: string hide }
    """
    modifier_alias_report = lint_dsl(modifier_alias_source)
    assert modifier_alias_report["ok"] is True
    assert any("canonical DSL modifier words" in warning for warning in modifier_alias_report["warnings"])
    assert "normalize_modifier_aliases" in {fix["id"] for fix in modifier_alias_report["fixes"]}
    modifier_alias_fixed = apply_lint_fixes(modifier_alias_source)
    assert "title: string required search" in modifier_alias_fixed["fixed"]
    assert "secret: string hidden" in modifier_alias_fixed["fixed"]
    assert "searchable" not in modifier_alias_fixed["fixed"]
    assert " hide" not in modifier_alias_fixed["fixed"]
    assert modifier_alias_fixed["after"]["ok"] is True
    formatted = format_dsl(
        "app Library{targets:web,mobile} table Author{id:int pk} table Book{id:int pk; title:string required; author_id:int -> Author.id[many-to-one]}"
    )
    assert formatted["format"] == "appgen.dsl-format-result.v1"
    assert formatted["after"]["ok"] is True
    assert formatted["formatted"] == (
        "app Library {\n"
        "  targets: web, mobile\n"
        "}\n"
        "\n"
        "table Author {\n"
        "  id: int pk\n"
        "}\n"
        "\n"
        "table Book {\n"
        "  id: int pk\n"
        "  title: string required\n"
        "  author_id: int -> Author.id [many-to-one]\n"
        "}\n"
    )
    outline = dsl_outline(source, source_name="inline")
    assert outline["format"] == "appgen.dsl-outline.v1"
    assert outline["ok"] is True
    assert outline["app"] == "LintDemo"
    assert {block["kind"] for block in outline["blocks"]} >= {"app", "table", "view"}
    assert next(table for table in outline["tables"] if table["name"] == "Book")["fields"] == (
        "id",
        "title",
        "author_id",
    )
    draft_outline = dsl_outline("app Draft { targets: web }\ntable Book { title: string")
    assert draft_outline["ok"] is False
    assert draft_outline["app"] == "Draft"
    assert draft_outline["parse_error"]
    completions = dsl_completion_items("tit", source=source)
    assert any(item["label"] == "title" and item["kind"] == "field" for item in completions)
    assert any(item["label"] == "Delphi Component" for item in dsl_completion_items("Del"))
    service = dsl_language_service(source, source_name="inline", prefix="Book")
    assert service["format"] == "appgen.dsl-language-service.v1"
    assert service["lint"]["ok"] is True
    assert service["outline"]["summary"]["tables"] == 2
    assert any(item["label"] == "Book" and item["kind"] == "table" for item in service["completions"])
    assert "code_actions" in service
    assert service["formatting"]["format"] == "appgen.dsl-format-result.v1"

    dsl_path = tmp_path / "lint.appgen"
    dsl_path.write_text(source)
    result = runner.invoke(__main__.main, ["--lint-dsl", str(dsl_path)])
    payload = json.loads(result.output)
    assert result.exit_code == 0
    assert payload["ok"] is True
    assert payload["summary"]["tables"] == 2
    bad_path = tmp_path / "bad.appgen"
    bad_path.write_text("app Bad { targets: web, toaster } table Book { title: string }")
    bad_result = runner.invoke(__main__.main, ["--lint-dsl", str(bad_path)])
    bad_payload = json.loads(bad_result.output)
    assert bad_result.exit_code == 1
    assert bad_payload["ok"] is False
    fix_path = tmp_path / "fix.appgen"
    fix_path.write_text("app Bad { targets: web, toaster } table Book { title: string ref Author.id }")
    fix_result = runner.invoke(__main__.main, ["--fix-dsl", str(fix_path)])
    fix_payload = json.loads(fix_result.output)
    assert fix_result.exit_code == 1
    assert fix_payload["changed"] is True
    assert "toaster" not in fix_path.read_text()
    assert "title: string -> Author.id" in fix_path.read_text()
    format_path = tmp_path / "format.appgen"
    format_path.write_text("app Library{targets:web,mobile} table Author{id:int pk} table Book{id:int pk; author_id:int -> Author.id}")
    format_result = runner.invoke(__main__.main, ["--format-dsl", str(format_path)])
    format_payload = json.loads(format_result.output)
    assert format_result.exit_code == 0
    assert format_payload["format"] == "appgen.dsl-format-result.v1"
    assert format_payload["changed"] is True
    assert format_path.read_text() == (
        "app Library {\n"
        "  targets: web, mobile\n"
        "}\n"
        "\n"
        "table Author {\n"
        "  id: int pk\n"
        "}\n"
        "\n"
        "table Book {\n"
        "  id: int pk\n"
        "  author_id: int -> Author.id\n"
        "}\n"
    )


def test_dsl_documentation_suite_exists() -> None:
    """The DSL has grammar, guide, tutorial, and linter documentation."""
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    expected = {
        "dsl.md": "AppGen DSL",
        "dsl-grammar.md": "AppGen DSL Grammar",
        "dsl-user-guide.md": "AppGen DSL User Guide",
        "dsl-tutorial.md": "AppGen DSL Tutorial",
        "dsl-linter.md": "AppGen DSL Linter",
    }
    for filename, heading in expected.items():
        text = (docs_dir / filename).read_text()
        assert heading in text
    index_text = (docs_dir / "index.md").read_text()
    assert "dsl-grammar" in index_text
    assert "dsl-linter" in index_text
    grammar = (docs_dir / "dsl-grammar.md").read_text()
    guide = (docs_dir / "dsl-user-guide.md").read_text()
    tutorial = (docs_dir / "dsl-tutorial.md").read_text()
    linter = (docs_dir / "dsl-linter.md").read_text()
    assert "Complete Grammar" in grammar
    assert "Lexical Rules" in grammar
    assert "dsl_language_quality_contract" in grammar
    assert "Delphi-style component placement" in grammar
    assert "Schema Design Checklist" in guide
    assert "Natural Language Evolution" in guide
    assert "9. Add API-Backed LLM Provider" in tutorial
    assert "Output Contract" in linter
    assert "structured quick fixes" in linter
    assert "language_quality" in linter
    assert "CI Gate" in linter


def test_generate_app_from_sqlite_schema_compiles(tmp_path) -> None:
    """Generate FAB app files from a small schema and compile the result."""
    db_path = tmp_path / "source.db"
    database_url = f"sqlite:///{db_path}"

    engine = create_engine(database_url)
    metadata = MetaData()
    Table(
        "author",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(80), nullable=False),
        Column("email", String(120), nullable=False),
        Column(
            "status",
            Enum("active", "blocked", name="author_status"),
            nullable=False,
            server_default=text("'active'"),
        ),
        UniqueConstraint("email", name="uq_author_email"),
    )
    Table(
        "book",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String(120), nullable=False, server_default=text("'Untitled'")),
        Column("isbn", String(32), nullable=True),
        Column("author_id", Integer, ForeignKey("author.id")),
        Index("ix_book_isbn_unique", "isbn", unique=True),
    )
    metadata.create_all(engine)

    output_dir = tmp_path / "app"
    generate_app_from_database(database_url, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_author = next(table for table in manifest["tables"] if table["name"] == "author")
    manifest_book = next(table for table in manifest["tables"] if table["name"] == "book")
    author_columns = {column["name"]: column for column in manifest_author["columns"]}
    book_columns = {column["name"]: column for column in manifest_book["columns"]}
    assert manifest["source_profile"]["source_kind"] == "database"
    assert manifest["source_profile"]["counts"]["relations"] == 1
    assert manifest["source_profile"]["fingerprint"]
    assert author_columns["email"]["unique"] is True
    assert author_columns["status"]["default"] == "active"
    assert book_columns["title"]["default"] == "Untitled"
    assert book_columns["isbn"]["unique"] is True

    generated_files = [
        output_dir / "models.py",
        output_dir / "views.py",
        output_dir / "api.py",
        output_dir / "openapi.py",
        output_dir / "gql.py",
        output_dir / "security.py",
        output_dir / "runtime_security.py",
        output_dir / "workflow.py",
        output_dir / "rules.py",
        output_dir / "validation.py",
        output_dir / "health.py",
        output_dir / "monitoring.py",
        output_dir / "resilience.py",
        output_dir / "performance.py",
        output_dir / "runtime_assurance.py",
        output_dir / "reports.py",
        output_dir / "report_delivery.py",
        output_dir / "dashboards.py",
        output_dir / "usage_analytics.py",
        output_dir / "search.py",
        output_dir / "media.py",
        output_dir / "documents.py",
        output_dir / "inventory_ops.py",
        output_dir / "finance_ops.py",
        output_dir / "manufacturing_ops.py",
        output_dir / "backup.py",
        output_dir / "data_access.py",
        output_dir / "data_exchange.py",
        output_dir / "database_ops.py",
        output_dir / "schema_import.py",
        output_dir / "designer.py",
        output_dir / "form_designer.py",
        output_dir / "nl_evolution.py",
        output_dir / "dsl_reference.py",
        output_dir / "view_experience.py",
        output_dir / "support_center.py",
        output_dir / "low_code_features.py",
        output_dir / "config_admin.py",
        output_dir / "integrations.py",
        output_dir / "productivity.py",
        output_dir / "lifecycle.py",
        output_dir / "tenancy.py",
        output_dir / "rls.py",
        output_dir / "identity.py",
        output_dir / "compliance.py",
        output_dir / "assistant.py",
        output_dir / "intelligence.py",
        output_dir / "chatbot.py",
        output_dir / "voice.py",
        output_dir / "agents.py",
        output_dir / "i18n.py",
        output_dir / "text_quality.py",
        output_dir / "notifications.py",
        output_dir / "platforms.py",
        output_dir / "microservices.py",
        output_dir / "collaboration.py",
        output_dir / "version_control.py",
        output_dir / "realtime.py",
        output_dir / "events.py",
        output_dir / "rpa.py",
        output_dir / "diagnostics.py",
        output_dir / "api_testing.py",
        output_dir / "code_review.py",
        output_dir / "components.py",
        output_dir / "view_composition.py",
        output_dir / "tabbed_views.py",
        output_dir / "prototyping.py",
        output_dir / "erp_templates.py",
        output_dir / "project_management.py",
        output_dir / "devtools.py",
        output_dir / "studio.py",
        output_dir / "wizards.py",
        output_dir / "branding.py",
        output_dir / "extensions.py",
        tmp_path / "config.py",
        tmp_path / "seed.py",
    ]
    for generated_file in generated_files:
        assert generated_file.exists()
        py_compile.compile(str(generated_file), doraise=True)

    assert (output_dir / "__init__.py").exists()
    assert (output_dir / "templates" / "my_index.html").exists()
    assert (output_dir / "templates" / "appgen_runtime_security.html").exists()
    assert (output_dir / "templates" / "appgen_openapi.html").exists()
    assert (output_dir / "static" / "appgen.webmanifest").exists()
    assert (output_dir / "static" / "appgen-sw.js").exists()
    assert (output_dir / "static" / "appgen-offline.html").exists()
    assert (output_dir / "static" / "appgen-icon.svg").exists()
    assert (output_dir / "static" / "appgen-theme.css").exists()
    assert (output_dir / "static" / "appgen-view-experience.js").exists()
    assert (output_dir / "templates" / "appgen_designer.html").exists()
    assert (output_dir / "templates" / "appgen_form_designer.html").exists()
    assert (output_dir / "templates" / "appgen_nl_evolution.html").exists()
    assert (output_dir / "templates" / "appgen_dsl_reference.html").exists()
    assert (output_dir / "templates" / "appgen_view_experience.html").exists()
    assert (output_dir / "templates" / "appgen_support_center.html").exists()
    assert (output_dir / "templates" / "appgen_low_code_features.html").exists()
    assert (output_dir / "templates" / "appgen_monitoring.html").exists()
    assert (output_dir / "templates" / "appgen_resilience.html").exists()
    assert (output_dir / "templates" / "appgen_rules.html").exists()
    assert (output_dir / "templates" / "appgen_performance.html").exists()
    assert (output_dir / "templates" / "appgen_runtime_assurance.html").exists()
    assert (output_dir / "templates" / "appgen_workflows.html").exists()
    assert (output_dir / "templates" / "appgen_reports.html").exists()
    assert (output_dir / "templates" / "appgen_report_delivery.html").exists()
    assert (output_dir / "templates" / "appgen_dashboards.html").exists()
    assert (output_dir / "templates" / "appgen_usage_analytics.html").exists()
    assert (output_dir / "templates" / "appgen_search.html").exists()
    assert (output_dir / "templates" / "appgen_media.html").exists()
    assert (output_dir / "templates" / "appgen_documents.html").exists()
    assert (output_dir / "templates" / "appgen_inventory_ops.html").exists()
    assert (output_dir / "templates" / "appgen_finance_ops.html").exists()
    assert (output_dir / "templates" / "appgen_manufacturing_ops.html").exists()
    assert (output_dir / "templates" / "appgen_data_access.html").exists()
    assert (output_dir / "templates" / "appgen_backup.html").exists()
    assert (output_dir / "templates" / "appgen_data_exchange.html").exists()
    assert (output_dir / "templates" / "appgen_database_ops.html").exists()
    assert (output_dir / "templates" / "appgen_schema_import.html").exists()
    assert (output_dir / "templates" / "appgen_config.html").exists()
    assert (output_dir / "templates" / "appgen_integrations.html").exists()
    assert (output_dir / "templates" / "appgen_productivity.html").exists()
    assert (output_dir / "templates" / "appgen_lifecycle.html").exists()
    assert (output_dir / "templates" / "appgen_tenancy.html").exists()
    assert (output_dir / "templates" / "appgen_rls.html").exists()
    assert (output_dir / "templates" / "appgen_identity.html").exists()
    assert (output_dir / "templates" / "appgen_compliance.html").exists()
    assert (output_dir / "templates" / "appgen_assistant.html").exists()
    assert (output_dir / "templates" / "appgen_intelligence.html").exists()
    assert (output_dir / "templates" / "appgen_chatbot.html").exists()
    assert (output_dir / "templates" / "appgen_voice.html").exists()
    assert (output_dir / "templates" / "appgen_agents.html").exists()
    assert (output_dir / "templates" / "appgen_i18n.html").exists()
    assert (output_dir / "templates" / "appgen_text_quality.html").exists()
    assert (output_dir / "templates" / "appgen_notifications.html").exists()
    assert (output_dir / "templates" / "appgen_platforms.html").exists()
    assert (output_dir / "templates" / "appgen_microservices.html").exists()
    assert (output_dir / "templates" / "appgen_collaboration.html").exists()
    assert (output_dir / "templates" / "appgen_version_control.html").exists()
    assert (output_dir / "templates" / "appgen_realtime.html").exists()
    assert (output_dir / "templates" / "appgen_events.html").exists()
    assert (output_dir / "templates" / "appgen_rpa.html").exists()
    assert (output_dir / "templates" / "appgen_diagnostics.html").exists()
    assert (output_dir / "templates" / "appgen_api_testing.html").exists()
    assert (output_dir / "templates" / "appgen_code_review.html").exists()
    assert (output_dir / "templates" / "appgen_components.html").exists()
    assert (output_dir / "templates" / "appgen_view_composition.html").exists()
    assert (output_dir / "templates" / "appgen_tabbed_views.html").exists()
    assert (output_dir / "templates" / "appgen_prototyping.html").exists()
    assert (output_dir / "templates" / "appgen_erp_templates.html").exists()
    assert (output_dir / "templates" / "appgen_project_management.html").exists()
    assert (output_dir / "templates" / "appgen_devtools.html").exists()
    assert (output_dir / "templates" / "appgen_studio.html").exists()
    assert (output_dir / "templates" / "appgen_wizards.html").exists()
    assert (output_dir / "templates" / "appgen_branding.html").exists()
    assert (output_dir / "templates" / "appgen_extensions.html").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "app_custom" / "__init__.py").exists()
    assert (tmp_path / "app_custom" / "extensions.py").exists()
    assert (tmp_path / "pyproject.toml").exists()
    assert (tmp_path / "MANIFEST.in").exists()
    assert (tmp_path / "appgen_package.py").exists()
    assert (tmp_path / "cookiecutter" / "cookiecutter.json").exists()
    assert (tmp_path / "cookiecutter" / "{{cookiecutter.project_slug}}" / "pyproject.toml").exists()
    assert (tmp_path / "cookiecutter" / "{{cookiecutter.project_slug}}" / "app" / "__init__.py").exists()
    assert (tmp_path / "babel.cfg").exists()
    assert (output_dir / "translations" / "en" / "LC_MESSAGES" / "messages.po").exists()
    assert (tmp_path / "docs" / "schema.md").exists()
    assert (tmp_path / "docs" / "data-dictionary.json").exists()
    assert (tmp_path / "docs" / "data-dictionary.md").exists()
    assert (tmp_path / "docs" / "openapi.json").exists()
    assert (tmp_path / "docs" / "accessibility.md").exists()
    assert (tmp_path / "Dockerfile").exists()
    assert (tmp_path / "docker-compose.yml").exists()
    assert (tmp_path / "deploy" / "appgen_deploy.py").exists()
    assert (tmp_path / "deploy" / "appgen_https.py").exists()
    assert (tmp_path / "deploy" / "Caddyfile").exists()
    assert (tmp_path / "deploy" / "k8s.yaml").exists()
    assert (tmp_path / "deploy" / "k8s-autoscale.yaml").exists()
    assert (tmp_path / "deploy" / "terraform-aws.tf").exists()
    assert (tmp_path / "deploy" / "terraform-gcp.tf").exists()
    assert (tmp_path / "deploy" / "terraform-azure.tf").exists()
    assert (tmp_path / "frontends" / "appgen_frontends.py").exists()
    assert (tmp_path / "frontends" / "react" / "src" / "App.jsx").exists()
    assert (tmp_path / "frontends" / "vue" / "src" / "App.vue").exists()
    assert (tmp_path / "frontends" / "angular" / "src" / "app.component.ts").exists()
    assert (tmp_path / "frontends" / "svelte" / "src" / "App.svelte").exists()
    assert (tmp_path / "frontends" / "htmx" / "src" / "server.js").exists()
    assert (tmp_path / "frontends" / "express" / "src" / "server.js").exists()
    assert (tmp_path / "sdks" / "appgen_sdks.py").exists()
    assert (tmp_path / "sdks" / "python" / "client.py").exists()
    assert (tmp_path / "sdks" / "javascript" / "client.js").exists()
    assert (tmp_path / "sdks" / "java" / "AppGenClient.java").exists()
    assert (tmp_path / "sdks" / "csharp" / "AppGenClient.cs").exists()
    assert (tmp_path / "native" / "appgen_native.py").exists()
    assert (tmp_path / "native" / "mobile" / "app.py").exists()
    assert (tmp_path / "native" / "desktop" / "app.py").exists()
    assert (tmp_path / "jhipster" / "appgen_jhipster.py").exists()
    assert (tmp_path / "jhipster" / "app.jdl").exists()
    assert (tmp_path / "chatbots" / "appgen_chatbots.py").exists()
    assert (tmp_path / "chatbots" / "dialogflow" / "intents.json").exists()
    assert (tmp_path / "chatbots" / "botframework" / "manifest.json").exists()
    assert (tmp_path / "automation" / "appgen_node_red.py").exists()
    assert (tmp_path / "automation" / "node-red" / "flows.json").exists()
    assert (tmp_path / ".env.example").exists()
    assert (tmp_path / ".github" / "workflows" / "appgen-ci.yml").exists()
    assert (tmp_path / ".vscode" / "launch.json").exists()
    assert (tmp_path / ".vscode" / "tasks.json").exists()
    assert (tmp_path / ".vscode" / "extensions.json").exists()
    assert (tmp_path / ".idea" / "misc.xml").exists()
    assert (tmp_path / ".idea" / "modules.xml").exists()
    assert (tmp_path / ".idea" / "runConfigurations" / "AppGen_Flask.xml").exists()
    assert (tmp_path / ".project").exists()
    assert (tmp_path / ".pydevproject").exists()
    assert (tmp_path / "scripts" / "appgen_quality.py").exists()
    assert (tmp_path / "migrations" / "README.md").exists()
    assert (tmp_path / "alembic.ini").exists()
    assert (tmp_path / "migrations" / "script.py.mako").exists()
    assert (tmp_path / "migrations" / "versions" / ".gitkeep").exists()
    assert (tmp_path / "tests" / "test_generated_coverage.py").exists()
    py_compile.compile(str(tmp_path / "migrations" / "env.py"), doraise=True)
    py_compile.compile(str(tmp_path / "deploy" / "appgen_deploy.py"), doraise=True)
    py_compile.compile(str(tmp_path / "deploy" / "appgen_https.py"), doraise=True)
    py_compile.compile(str(tmp_path / "frontends" / "appgen_frontends.py"), doraise=True)
    py_compile.compile(str(tmp_path / "sdks" / "appgen_sdks.py"), doraise=True)
    py_compile.compile(str(tmp_path / "sdks" / "python" / "client.py"), doraise=True)
    py_compile.compile(str(tmp_path / "native" / "appgen_native.py"), doraise=True)
    py_compile.compile(str(tmp_path / "native" / "mobile" / "app.py"), doraise=True)
    py_compile.compile(str(tmp_path / "native" / "desktop" / "app.py"), doraise=True)
    py_compile.compile(str(tmp_path / "jhipster" / "appgen_jhipster.py"), doraise=True)
    py_compile.compile(str(tmp_path / "chatbots" / "appgen_chatbots.py"), doraise=True)
    py_compile.compile(str(tmp_path / "automation" / "appgen_node_red.py"), doraise=True)
    py_compile.compile(str(tmp_path / "scripts" / "appgen_quality.py"), doraise=True)
    py_compile.compile(str(tmp_path / "appgen_package.py"), doraise=True)
    py_compile.compile(str(tmp_path / "tests" / "test_generated_contract.py"), doraise=True)
    py_compile.compile(str(tmp_path / "tests" / "test_generated_coverage.py"), doraise=True)
    ci_text = (tmp_path / ".github" / "workflows" / "appgen-ci.yml").read_text()
    assert "python scripts/appgen_quality.py" in ci_text
    assert "pytest" in ci_text
    quality_script = (tmp_path / "scripts" / "appgen_quality.py").read_text()
    assert "workflow_webhook_plan" in quality_script
    quality = subprocess.run(
        [sys.executable, str(tmp_path / "scripts" / "appgen_quality.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "appgen quality passed" in quality.stdout
    schema_docs = (tmp_path / "docs" / "schema.md").read_text()
    assert "author_id" in schema_docs
    assert "`book.author_id` -> `author.id`" in schema_docs
    data_dictionary = json.loads((tmp_path / "docs" / "data-dictionary.json").read_text())
    book_dictionary = next(table for table in data_dictionary["tables"] if table["name"] == "book")
    book_fields = {column["name"]: column for column in book_dictionary["columns"]}
    assert data_dictionary["format"] == "appgen.data-dictionary.v1"
    assert book_fields["title"]["content_kind"] == "descriptor"
    assert book_fields["title"]["sample_value"] == "Sample Title"
    assert book_fields["author_id"]["content_kind"] == "relationship"
    assert book_fields["author_id"]["reference"] == {"table": "author", "column": "id"}
    assert "title" in book_dictionary["display_fields"]
    assert "title" in book_dictionary["writable_fields"]
    data_dictionary_md = (tmp_path / "docs" / "data-dictionary.md").read_text()
    assert "Data Dictionary" in data_dictionary_md
    assert "Writable fields" in data_dictionary_md
    k8s_text = (tmp_path / "deploy" / "k8s.yaml").read_text()
    assert "kind: Deployment" in k8s_text
    assert "readinessProbe" in k8s_text
    assert "secret-key" in k8s_text
    autoscale_text = (tmp_path / "deploy" / "k8s-autoscale.yaml").read_text()
    assert "HorizontalPodAutoscaler" in autoscale_text
    assert "appgen_http_p95_ms" in autoscale_text
    compose_text = (tmp_path / "docker-compose.yml").read_text()
    assert "caddy:2" in compose_text
    assert "443:443" in compose_text
    assert "nodered/node-red:3.1" in compose_text
    assert "1880:1880" in compose_text
    caddy_text = (tmp_path / "deploy" / "Caddyfile").read_text()
    assert "reverse_proxy web:8080" in caddy_text
    assert "Strict-Transport-Security" in caddy_text
    assert 'target   = "aws"' in (tmp_path / "deploy" / "terraform-aws.tf").read_text()
    assert 'target   = "gcp"' in (tmp_path / "deploy" / "terraform-gcp.tf").read_text()
    assert 'target   = "azure"' in (tmp_path / "deploy" / "terraform-azure.tf").read_text()
    deployment = _load_module(tmp_path / "deploy" / "appgen_deploy.py", "generated_deployment")
    https = _load_module(tmp_path / "deploy" / "appgen_https.py", "generated_https")
    assert "kubernetes" in deployment.deployment_targets()
    assert "onprem" in deployment.deployment_targets()
    assert "https" in deployment.deployment_targets()
    assert deployment.artifact_plan("aws") == ("deploy/terraform-aws.tf",)
    assert deployment.artifact_plan("https") == ("deploy/Caddyfile", "deploy/appgen_https.py")
    assert "automation/node-red/flows.json" in deployment.artifact_plan("compose")
    assert deployment.environment_status({"SECRET_KEY": "s", "SQLALCHEMY_DATABASE_URI": "sqlite://"})["configured"] is True
    assert deployment.secret_plan("aws")["cloud_secret_store"] == "AWS Secrets Manager"
    runbook = deployment.deployment_runbook("kubernetes", image_tag="app:v1", base_url="https://app.example")
    assert runbook["review_required"] is True
    assert runbook["image_tag"] == "app:v1"
    assert runbook["smoke_checks"][0]["url"] == "https://app.example/health"
    rollback_plan = deployment.rollback_plan("kubernetes", previous_image_tag="app:v0")
    assert rollback_plan["previous_image_tag"] == "app:v0"
    assert rollback_plan["review_required"] is True
    assert deployment.deployment_topology("onprem")["network"] == "private-datacenter"
    scaling = deployment.scaling_profile("kubernetes", {"replicas": 2, "cpu_percent": 91})
    assert scaling["desired_replicas"] == 4
    assert scaling["hpa_artifact"] == "deploy/k8s-autoscale.yaml"
    infra_scaling = deployment.infrastructure_scaling_plan("kubernetes", {"p95_ms": 900})
    assert infra_scaling["profile"]["review_required"] is True
    readiness = deployment.cloud_readiness_matrix({"SECRET_KEY": "s", "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    assert {item["target"] for item in readiness} >= {"kubernetes", "onprem", "aws", "gcp", "azure"}
    assert deployment.onprem_readiness(
        {"SECRET_KEY": "s", "SQLALCHEMY_DATABASE_URI": "sqlite://"},
        {"Dockerfile", "docker-compose.yml", "deploy/Caddyfile"},
    )["ok"] is True
    promotion = deployment.release_promotion_plan("compose", "kubernetes", image_tag="app:v2")
    assert promotion["format"] == "appgen.release-promotion-plan.v1"
    assert promotion["scaling"]["target"] == "kubernetes"
    all_artifacts = {
        "Dockerfile",
        "docker-compose.yml",
        "deploy/Caddyfile",
        "deploy/appgen_https.py",
        "deploy/k8s.yaml",
        "deploy/k8s-autoscale.yaml",
        "deploy/terraform-aws.tf",
        "deploy/terraform-gcp.tf",
        "deploy/terraform-azure.tf",
        "automation/node-red/flows.json",
    }
    assert deployment.deployment_check(
        {"SECRET_KEY": "s", "SQLALCHEMY_DATABASE_URI": "sqlite://"},
        all_artifacts,
    )["ok"] is True
    assert https.https_readiness(
        {"APPGEN_DOMAIN": "example.test", "APPGEN_TLS_EMAIL": "admin@example.test"},
        all_artifacts,
    )["ok"] is True
    assert https.public_base_url({"APPGEN_DOMAIN": "example.test"}) == "https://example.test"
    frontends = _load_module(tmp_path / "frontends" / "appgen_frontends.py", "generated_frontends")
    assert set(frontends.frontend_targets()) == {"react", "vue", "angular", "svelte", "htmx", "express"}
    assert frontends.frontend_plan("react")["entry"] == "src/App.jsx"
    assert ("book", "/api/v1/book/") in frontends.api_routes()
    frontend_artifacts = {
        "frontends/react/package.json",
        "frontends/react/src/App.jsx",
        "frontends/vue/package.json",
        "frontends/vue/src/App.vue",
        "frontends/angular/package.json",
        "frontends/angular/src/app.component.ts",
        "frontends/svelte/package.json",
        "frontends/svelte/src/App.svelte",
        "frontends/htmx/package.json",
        "frontends/htmx/src/server.js",
        "frontends/express/package.json",
        "frontends/express/src/server.js",
    }
    assert frontends.scaffold_check(frontend_artifacts)["ok"] is True
    assert "/api/v1/book/" in (tmp_path / "frontends" / "react" / "src" / "App.jsx").read_text()
    assert "<template>" in (tmp_path / "frontends" / "vue" / "src" / "App.vue").read_text()
    assert "AppComponent" in (tmp_path / "frontends" / "angular" / "src" / "app.component.ts").read_text()
    assert "{#each tables as table}" in (tmp_path / "frontends" / "svelte" / "src" / "App.svelte").read_text()
    assert "hx-get" in (tmp_path / "frontends" / "htmx" / "src" / "server.js").read_text()
    assert "http.createServer" in (tmp_path / "frontends" / "express" / "src" / "server.js").read_text()
    native = _load_module(tmp_path / "native" / "appgen_native.py", "generated_native")
    mobile = _load_module(tmp_path / "native" / "mobile" / "app.py", "generated_mobile")
    desktop = _load_module(tmp_path / "native" / "desktop" / "app.py", "generated_desktop")
    assert set(native.native_targets()) == {"mobile", "desktop"}
    assert native.native_plan("mobile")["framework"] == "kivy"
    assert ("book", "/api/v1/book/") in native.native_api_routes()
    native_artifacts = {
        "native/appgen_native.py",
        "native/mobile/pyproject.toml",
        "native/mobile/app.py",
        "native/desktop/pyproject.toml",
        "native/desktop/app.py",
    }
    assert native.scaffold_check(native_artifacts)["ok"] is True
    assert "android.permission.CAMERA" in native.native_permission_manifest("mobile")["android"]
    assert native.native_capability_plan("desktop")["offline_storage"] == "json-cache"
    assert mobile.mobile_contract()["framework"] == "kivy"
    assert "android.permission.ACCESS_FINE_LOCATION" in mobile.permission_manifest()["android"]
    assert mobile.camera_capture_plan("book", "cover_image")["permission"] == "android.permission.CAMERA"
    assert mobile.location_capture_plan("book")["status"] == "planned"
    assert mobile.push_notification_payload("Ready", "Book synced")["permission"] == "android.permission.POST_NOTIFICATIONS"
    offline_book = mobile.offline_record("Book", {"id": 1, "title": "Dune"})
    assert offline_book["status"] == "queued"
    assert offline_book["sync_key"] == "book:1"
    sync_batch = mobile.offline_sync_batch((offline_book,))
    assert sync_batch["format"] == "appgen.mobile-offline-sync-batch.v1"
    assert sync_batch["tables"][0]["endpoint"] == "/api/v1/book/"
    conflict = mobile.sync_conflict(offline_book, {"values": {"id": 1, "title": "Dune Messiah"}})
    assert conflict["format"] == "appgen.mobile-sync-conflict.v1"
    assert conflict["requires_review"] is True
    replay = mobile.offline_replay_plan("https://api.example.test", (offline_book,))
    assert replay["format"] == "appgen.mobile-offline-replay.v1"
    assert replay["steps"][0]["conflict_policy"] == "manual_review"
    assert desktop.desktop_contract()["framework"] == "beeware"
    assert desktop.desktop_file_action("/tmp/book.json", table_name="Book")["review_required"] is True
    assert desktop.desktop_notification_payload("Ready", "Book synced")["title"] == "Ready"
    assert desktop.local_cache_plan("/tmp/cache")[1]["path"].endswith("/book.json")
    cache_snapshot = desktop.desktop_cache_snapshot("/tmp/cache", {"book": [{"id": 1}]})
    assert cache_snapshot["format"] == "appgen.desktop-cache-snapshot.v1"
    assert cache_snapshot["files"][1]["record_count"] == 1
    change_set = desktop.desktop_change_set("book", ({"values": {"id": 1, "title": "Dune"}},))
    assert change_set["format"] == "appgen.desktop-change-set.v1"
    assert change_set["requires_review"] is True
    desktop_sync = desktop.desktop_sync_plan("https://api.example.test", (change_set,))
    assert desktop_sync["format"] == "appgen.desktop-sync-plan.v1"
    assert desktop_sync["steps"][0]["conflict_policy"] == "manual_review"
    jhipster = _load_module(tmp_path / "jhipster" / "appgen_jhipster.py", "generated_jhipster")
    assert jhipster.jhipster_import_command() == ("jhipster", "jdl", "jhipster/app.jdl")
    assert jhipster.export_check({"jhipster/app.jdl", "jhipster/appgen_jhipster.py"})["ok"] is True
    assert "agentic-systems" in {item["key"] for item in jhipster.appgen_upgrade_targets()}
    gap_analysis = jhipster.jhipster_gap_analysis()
    assert gap_analysis["position"] == "appgen-is-broader-than-jhipster"
    assert "visual-builders" in gap_analysis["appgen_only"]
    adoption_plan = jhipster.jhipster_adoption_plan({"jhipster/app.jdl", "jhipster/appgen_jhipster.py"})
    assert adoption_plan["format"] == "appgen.jhipster-adoption-plan.v1"
    assert adoption_plan["steps"][1]["side_effect"] == "external_code_generation"
    jdl_text = (tmp_path / "jhipster" / "app.jdl").read_text()
    assert "entity Book" in jdl_text
    assert "relationship ManyToOne" in jdl_text
    assert "Book{author} to Author" in jdl_text
    assert "dto * with mapstruct" in jdl_text
    chatbots = _load_module(tmp_path / "chatbots" / "appgen_chatbots.py", "generated_chatbots")
    assert set(chatbots.chatbot_targets()) == {"dialogflow", "botframework"}
    assert "create_book" in {intent["intent"] for intent in chatbots.chatbot_intents()}
    book_plan = chatbots.conversation_plan("create_book", {})
    assert book_plan["ready"] is False
    assert book_plan["missing_fields"] == ("title",)
    assert book_plan["next_prompt"] == "What should title be?"
    chatbot_artifacts = {
        "chatbots/appgen_chatbots.py",
        "chatbots/dialogflow/intents.json",
        "chatbots/botframework/manifest.json",
    }
    assert chatbots.export_check(chatbot_artifacts)["ok"] is True
    dialogflow_export = json.loads((tmp_path / "chatbots" / "dialogflow" / "intents.json").read_text())
    assert "create_book" in {intent["displayName"] for intent in dialogflow_export["intents"]}
    bot_manifest = json.loads((tmp_path / "chatbots" / "botframework" / "manifest.json").read_text())
    commands = bot_manifest["bots"][0]["commandLists"][0]["commands"]
    assert "create_book" in {command["title"] for command in commands}
    node_red = _load_module(tmp_path / "automation" / "appgen_node_red.py", "generated_node_red")
    assert "book.created" in {event["topic"] for event in node_red.node_red_events()}
    assert node_red.event_topic("book", "created") == "book.created"
    assert node_red.webhook_plan("book", "created")["path"] == "/appgen/book/created"
    assert node_red.node_red_runtime_service()["service"] == "node-red"
    assert node_red.compose_service_plan()["image"] == "nodered/node-red:3.1"
    assert node_red.runtime_readiness({"automation/node-red/flows.json", "docker-compose.yml"})["ok"] is True
    flow_export = json.loads((tmp_path / "automation" / "node-red" / "flows.json").read_text())
    assert node_red.validate_flow_export(flow_export)["ok"] is True
    assert node_red.validate_flow_export(flow_export)["runtime"]["port"] == 1880
    assert node_red.workflow_events() == ()
    assert any(node.get("type") == "http in" and node.get("name") == "book.created" for node in flow_export)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    config_text = (tmp_path / "config.py").read_text()
    assert f"SQLALCHEMY_DATABASE_URI = '{database_url}'" in config_text
    assert "FAB_API_SHOW_STACKTRACE = True" in config_text
    assert "FAB_API_SWAGGER_UI = True" in config_text
    assert manifest["source"] == database_url
    assert {table["name"] for table in manifest["tables"]} == {"author", "book"}
    assert "schema.import" in {item["key"] for item in manifest["capabilities"]}
    assert "api.rest" in {item["key"] for item in manifest["capabilities"]}
    assert "api.graphql" in {item["key"] for item in manifest["capabilities"]}
    assert "api.documentation" in {item["key"] for item in manifest["capabilities"]}
    assert "api.openapi" in {item["key"] for item in manifest["capabilities"]}
    assert "api.sdks" in {item["key"] for item in manifest["capabilities"]}
    assert "reports.analytics" in {item["key"] for item in manifest["capabilities"]}
    assert "reports.usage-analytics" in {item["key"] for item in manifest["capabilities"]}
    assert "data.visualization" in {item["key"] for item in manifest["capabilities"]}
    assert "data.search" in {item["key"] for item in manifest["capabilities"]}
    assert "data.exchange" in {item["key"] for item in manifest["capabilities"]}
    assert "data.database-ops" in {item["key"] for item in manifest["capabilities"]}
    assert "data.migrations" in {item["key"] for item in manifest["capabilities"]}
    assert "devops.cicd" in {item["key"] for item in manifest["capabilities"]}
    assert "devops.ide-integration" in {item["key"] for item in manifest["capabilities"]}
    assert "devops.studio" in {item["key"] for item in manifest["capabilities"]}
    assert "devops.project-management" in {item["key"] for item in manifest["capabilities"]}
    assert "support.training" in {item["key"] for item in manifest["capabilities"]}
    assert "integration.enterprise" in {item["key"] for item in manifest["capabilities"]}
    assert "dsl.language-design" in {item["key"] for item in manifest["capabilities"]}
    assert "integration.productivity" in {item["key"] for item in manifest["capabilities"]}
    assert "scale.multi-tenancy" in {item["key"] for item in manifest["capabilities"]}
    assert "security.sso" in {item["key"] for item in manifest["capabilities"]}
    assert "security.session" in {item["key"] for item in manifest["capabilities"]}
    assert "security.https" in {item["key"] for item in manifest["capabilities"]}
    assert "security.rls" in {item["key"] for item in manifest["capabilities"]}
    assert "security.compliance" in {item["key"] for item in manifest["capabilities"]}
    assert "ai.assistance" in {item["key"] for item in manifest["capabilities"]}
    assert "ai.intelligence" in {item["key"] for item in manifest["capabilities"]}
    assert "ai.voice-assistant" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.notifications" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.targets" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.frontends" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.form-designer" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.view-composition" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.tabbed-views" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.nl-evolution" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.rapid-prototyping" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.view-experience" in {item["key"] for item in manifest["capabilities"]}
    assert "ai.agentic-systems" in {item["key"] for item in manifest["capabilities"]}
    assert "components.erp-templates" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.microservices" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.native" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.jhipster" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.competitive-benchmark" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.jhipster-superiority" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.chatbots" in {item["key"] for item in manifest["capabilities"]}
    assert "ai.guided-chatbot" in {item["key"] for item in manifest["capabilities"]}
    assert "automation.node-red" in {item["key"] for item in manifest["capabilities"]}
    assert "automation.cep" in {item["key"] for item in manifest["capabilities"]}
    assert "automation.rpa-bpa" in {item["key"] for item in manifest["capabilities"]}
    assert "team.collaboration" in {item["key"] for item in manifest["capabilities"]}
    assert "team.version-control" in {item["key"] for item in manifest["capabilities"]}
    assert "team.realtime" in {item["key"] for item in manifest["capabilities"]}
    assert "quality.diagnostics" in {item["key"] for item in manifest["capabilities"]}
    assert "quality.api-testing" in {item["key"] for item in manifest["capabilities"]}
    assert "quality.code-review" in {item["key"] for item in manifest["capabilities"]}
    assert "quality.test-coverage" in {item["key"] for item in manifest["capabilities"]}
    assert "components.templates" in {item["key"] for item in manifest["capabilities"]}
    assert "components.lookups" in {item["key"] for item in manifest["capabilities"]}
    assert "components.text-quality" in {item["key"] for item in manifest["capabilities"]}
    assert "components.media" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.wizards" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.layout" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.branding" in {item["key"] for item in manifest["capabilities"]}
    assert "platform.extensibility" in {item["key"] for item in manifest["capabilities"]}
    assert "devops.packaging" in {item["key"] for item in manifest["capabilities"]}
    assert "data.seed" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.visual-modeling" in {item["key"] for item in manifest["capabilities"]}
    assert "ui.pwa" in {item["key"] for item in manifest["capabilities"]}
    assert "i18n.localization" in {item["key"] for item in manifest["capabilities"]}
    assert "a11y.compliance" in {item["key"] for item in manifest["capabilities"]}
    assert "workflow.automation" in {item["key"] for item in manifest["capabilities"]}
    assert "workflow.statecharts" in {item["key"] for item in manifest["capabilities"]}
    assert "logic.business-rules" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.monitoring" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.resilience" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.performance" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.assurance" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.configuration" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.lifecycle" in {item["key"] for item in manifest["capabilities"]}
    assert "ops.backup" in {item["key"] for item in manifest["capabilities"]}


def test_metadata_defaults_are_portable() -> None:
    """Reflected SQL defaults normalize away dialect-only literal casts."""
    metadata = MetaData()
    Table(
        "event",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("status", String(20), server_default=text("'active'::character varying")),
        Column("created_at", String(40), server_default=text("(CURRENT_TIMESTAMP)")),
    )

    schema = schema_from_metadata(metadata)
    columns = {column.name: column for column in schema.table("event").columns}

    assert columns["status"].default == "active"
    assert columns["created_at"].default == "CURRENT_TIMESTAMP"


def test_metadata_primary_keys_normalize_non_nullable() -> None:
    """Reflected database imports treat primary keys as required fields."""
    metadata = MetaData()
    Table(
        "legacy_order_line",
        metadata,
        Column("order_id", Integer, primary_key=True, nullable=True),
        Column("line_no", Integer, primary_key=True, nullable=True),
        Column("sku", String(40), nullable=True),
    )

    schema = schema_from_metadata(metadata, source="sqlite:///legacy.db")
    columns = {column.name: column for column in schema.table("legacy_order_line").columns}
    profile = schema.source_profile()

    assert columns["order_id"].primary_key is True
    assert columns["order_id"].nullable is False
    assert columns["line_no"].primary_key is True
    assert columns["line_no"].nullable is False
    assert columns["sku"].nullable is True
    assert profile["source_kind"] == "database"
    assert profile["table_signatures"][0]["primary_keys"] == ("order_id", "line_no")


def test_metadata_reflection_preserves_indexes_and_computed_columns(tmp_path) -> None:
    """Existing database imports preserve search indexes and computed fields."""
    metadata = MetaData()
    Table(
        "invoice_line",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("invoice_number", String(40), nullable=False),
        Column("sku", String(40), nullable=False),
        Column("quantity", Integer, nullable=False),
        Column("unit_price", Integer, nullable=False),
        Column("line_total", Integer, Computed("quantity * unit_price")),
        Index("ix_invoice_line_invoice_number", "invoice_number"),
        Index("ix_invoice_line_sku_quantity", "sku", "quantity"),
    )

    schema = schema_from_metadata(metadata, source="sqlite:///billing.db")
    columns = {column.name: column for column in schema.table("invoice_line").columns}

    assert columns["invoice_number"].searchable is True
    assert columns["sku"].searchable is True
    assert columns["quantity"].searchable is True
    assert columns["unit_price"].searchable is False
    assert columns["line_total"].derived is True
    assert columns["line_total"].expression == "quantity * unit_price"

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    line_manifest = next(table for table in manifest["tables"] if table["name"] == "invoice_line")
    manifest_columns = {column["name"]: column for column in line_manifest["columns"]}
    assert manifest_columns["invoice_number"]["searchable"] is True
    assert manifest_columns["sku"]["searchable"] is True
    assert manifest_columns["line_total"]["derived"] is True
    assert manifest_columns["line_total"]["expression"] == "quantity * unit_price"
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_schema_source_profile_fingerprints_imports(tmp_path) -> None:
    """Every supported schema source reports stable provenance for generated manifests."""
    dbml_path = tmp_path / "library.dbml"
    dbml_path.write_text(
        """
        Table author {
          id int [pk]
          name varchar [not null]
        }
        """
    )
    dbml_schema = load_schema(dbml_path, source_type="dbml")
    dbml_profile = dbml_schema.source_profile()
    assert dbml_profile["format"] == "appgen.schema-source-profile.v1"
    assert dbml_profile["source_kind"] == "dbml"
    assert dbml_profile["counts"]["tables"] == 1
    assert dbml_profile["table_signatures"][0]["primary_keys"] == ("id",)
    assert len(dbml_profile["fingerprint"]) == 16
    dbml_fidelity = dbml_schema.source_fidelity_report()
    assert dbml_fidelity["format"] == "appgen.schema-source-fidelity.v1"
    assert dbml_fidelity["source_kind"] == "dbml"
    assert dbml_fidelity["ok"] is True
    assert dbml_fidelity["import_command"] == "appgen --dbml schema.dbml --writedir app"
    assert "dbml" in dbml_fidelity["roundtrip_targets"]
    assert dbml_fidelity["checks"]["relations_normalized"] is True
    assert schema_source_kind(str(dbml_path)) == "dbml"

    sql_path = tmp_path / "library.sql"
    sql_path.write_text("CREATE TABLE book (id INTEGER PRIMARY KEY, title TEXT NOT NULL);")
    sql_schema = load_schema(sql_path, source_type="sql")
    assert sql_schema.source_profile()["source_kind"] == "sql"
    assert sql_schema.source_fidelity_report()["import_command"] == "appgen --sql schema.sql --writedir app"

    pony_path = tmp_path / "entities.py"
    pony_path.write_text(
        """
        from pony.orm import Database, PrimaryKey, Required
        db = Database()
        class Book(db.Entity):
            id = PrimaryKey(int)
            title = Required(str)
        """
    )
    pony_schema = load_schema(pony_path, source_type="pony")
    assert pony_schema.source_profile()["source_kind"] == "ponyorm"
    assert "ponyorm" in pony_schema.source_fidelity_report()["roundtrip_targets"]

    metadata = MetaData()
    Table("live_book", metadata, Column("id", Integer, primary_key=True))
    database_schema = schema_from_metadata(metadata, source="sqlite:///live.db")
    source_contract = schema_source_contract()
    assert database_schema.source_profile()["source_kind"] == "database"
    database_fidelity = database_schema.source_fidelity_report()
    assert database_fidelity["database_url_dialects"] == source_contract["database_url_dialects"]
    assert database_fidelity["sqlalchemy_driver_urls"] is True
    assert schema_source_kind("postgresql+psycopg2://user@host/db") == "database"
    assert schema_source_kind("mysql+pymysql://user@host/db") == "database"
    assert source_contract["format"] == "appgen.schema-source-contract.v1"
    assert {"dbml", "sql", "ponyorm", "database"} <= set(source_contract["source_kinds"])
    assert source_contract["sqlalchemy_driver_urls"] is True


def test_dbml_source_normalizes_and_generates(tmp_path) -> None:
    """DBML imports feed the canonical schema and existing generator."""
    dbml_path = tmp_path / "library.dbml"
    dbml_path.write_text(
        """
        Enum Status {
          draft
          published
          archived
        }

        Table author {
          id int [pk]
          name varchar [not null]
          email varchar [unique]
        }

        Table book {
          id int [pk]
          title varchar [not null, default: 'Untitled']
          isbn varchar
          status Status [default: 'draft']
          author_id int [ref: > author.id]

          indexes {
            isbn [unique]
            (title, author_id) [unique]
          }
        }
        """
    )

    schema = load_schema(dbml_path)
    author = schema.table("author")
    book = schema.table("book")
    author_columns = {column.name: column for column in author.columns}
    book_columns = {column.name: column for column in book.columns}
    assert schema.enums[0].name == "Status"
    assert schema.enums[0].values == ("draft", "published", "archived")
    assert author_columns["id"].nullable is False
    assert author_columns["email"].unique is True
    assert book_columns["title"].default == "Untitled"
    assert book_columns["isbn"].unique is True
    assert book_columns["title"].unique is False
    assert book_columns["status"].type_name == "Status"
    assert book_columns["status"].default == "draft"
    assert book_columns["author_id"].references == ("author", "id")

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "views.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)
    py_compile.compile(str(output_dir / "openapi.py"), doraise=True)
    py_compile.compile(str(output_dir / "gql.py"), doraise=True)
    py_compile.compile(str(output_dir / "workflow.py"), doraise=True)
    py_compile.compile(str(output_dir / "health.py"), doraise=True)
    py_compile.compile(str(output_dir / "monitoring.py"), doraise=True)
    py_compile.compile(str(output_dir / "resilience.py"), doraise=True)
    py_compile.compile(str(output_dir / "runtime_assurance.py"), doraise=True)
    py_compile.compile(str(output_dir / "reports.py"), doraise=True)
    py_compile.compile(str(output_dir / "report_delivery.py"), doraise=True)
    py_compile.compile(str(output_dir / "dashboards.py"), doraise=True)
    py_compile.compile(str(output_dir / "search.py"), doraise=True)
    py_compile.compile(str(output_dir / "media.py"), doraise=True)
    py_compile.compile(str(output_dir / "documents.py"), doraise=True)
    py_compile.compile(str(output_dir / "inventory_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "finance_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "manufacturing_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "backup.py"), doraise=True)
    py_compile.compile(str(output_dir / "designer.py"), doraise=True)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_book = next(table for table in manifest["tables"] if table["name"] == "book")
    manifest_book_columns = {column["name"]: column for column in manifest_book["columns"]}
    assert manifest["source_profile"]["source_kind"] == "dbml"
    assert manifest["source_profile"]["counts"]["enums"] == 1
    assert manifest["source_profile"]["fingerprint"] == schema.source_profile()["fingerprint"]
    assert manifest["source_fidelity"]["format"] == "appgen.schema-source-fidelity.v1"
    assert manifest["source_fidelity"]["ok"] is True
    assert manifest["source_fidelity"]["fingerprint"] == manifest["source_profile"]["fingerprint"]
    assert manifest["enums"][0]["name"] == "Status"
    assert manifest_book_columns["title"]["default"] == "Untitled"
    assert manifest_book_columns["isbn"]["unique"] is True
    assert manifest_book_columns["title"]["unique"] is False
    assert manifest_book_columns["status"]["default"] == "draft"
    assert manifest["relations"][0]["target_table"] == "author"


def test_dbml_source_preserves_composite_ref_pairs(tmp_path) -> None:
    """DBML composite refs preserve each source/target column pairing."""
    dbml_path = tmp_path / "fulfillment.dbml"
    dbml_path.write_text(
        """
        Table order_line {
          order_id int [pk]
          line_no int [pk]
          sku varchar
        }

        Table shipment_line {
          order_id int
          line_no int
          package_no int

          indexes {
            (order_id, line_no, package_no) [pk]
          }
        }

        Ref: shipment_line.(order_id, line_no) > order_line.(order_id, line_no)
        """
    )

    schema = load_schema(dbml_path, source_type="dbml")
    shipment = schema.table("shipment_line")
    columns = {column.name: column for column in shipment.columns}

    assert columns["order_id"].references == ("order_line", "order_id")
    assert columns["line_no"].references == ("order_line", "line_no")
    assert {
        (relation.source_column, relation.target_column)
        for relation in schema.relations
        if relation.source_table == "shipment_line"
    } == {("order_id", "order_id"), ("line_no", "line_no")}

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_shipment = next(table for table in manifest["tables"] if table["name"] == "shipment_line")
    manifest_columns = {column["name"]: column for column in manifest_shipment["columns"]}
    assert manifest_columns["order_id"]["references"] == ["order_line", "order_id"]
    assert manifest_columns["line_no"]["references"] == ["order_line", "line_no"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_dbml_source_preserves_ref_direction_and_cardinality(tmp_path) -> None:
    """DBML '<' and '-' refs normalize to source-column references and cardinality."""
    dbml_path = tmp_path / "profiles.dbml"
    dbml_path.write_text(
        """
        Table author {
          id int [pk]
          name varchar
        }

        Table book {
          id int [pk]
          author_id int
          title varchar
        }

        Table author_profile {
          id int [pk]
          author_id int [unique]
          bio text
        }

        Ref: author.id < book.author_id
        Ref: author_profile.author_id - author.id
        """
    )

    schema = load_schema(dbml_path, source_type="dbml")
    book_columns = {column.name: column for column in schema.table("book").columns}
    profile_columns = {column.name: column for column in schema.table("author_profile").columns}
    relation_cardinality = {
        (relation.source_table, relation.source_column): relation.cardinality
        for relation in schema.relations
    }

    assert book_columns["author_id"].references == ("author", "id")
    assert profile_columns["author_id"].references == ("author", "id")
    assert relation_cardinality[("book", "author_id")] == "many-to-one"
    assert relation_cardinality[("author_profile", "author_id")] == "one-to-one"

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_relations = {
        (relation["source_table"], relation["source_column"]): relation
        for relation in manifest["relations"]
    }
    assert manifest_relations[("book", "author_id")]["target_table"] == "author"
    assert manifest_relations[("book", "author_id")]["cardinality"] == "many-to-one"
    assert manifest_relations[("author_profile", "author_id")]["cardinality"] == "one-to-one"
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_dbml_source_preserves_table_group_metadata(tmp_path) -> None:
    """DBML TableGroup membership is retained for designer/source fidelity."""
    dbml_path = tmp_path / "operations.dbml"
    dbml_path.write_text(
        """
        Table customer {
          id int [pk]
          email varchar [not null]
        }

        Table invoice {
          id int [pk]
          customer_id int [ref: > customer.id]
          total decimal
        }

        TableGroup Revenue {
          customer
          invoice
        }
        """
    )

    schema = load_schema(dbml_path, source_type="dbml")
    customer_columns = {column.name: column for column in schema.table("customer").columns}
    invoice_columns = {column.name: column for column in schema.table("invoice").columns}

    assert customer_columns["id"].source_group == "Revenue"
    assert customer_columns["email"].source_group == "Revenue"
    assert invoice_columns["customer_id"].source_group == "Revenue"
    assert schema.source_fidelity_report()["lossy_features"] == (
        "DBML notes, colors, and project metadata require review outside AppSchema",
    )

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    invoice_manifest = next(table for table in manifest["tables"] if table["name"] == "invoice")
    manifest_columns = {column["name"]: column for column in invoice_manifest["columns"]}
    assert manifest_columns["customer_id"]["source_group"] == "Revenue"
    assert manifest_columns["customer_id"]["references"] == ["customer", "id"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_sql_source_normalizes_relationships(tmp_path) -> None:
    """SQL DDL imports capture columns, defaults, constraints, domains, and FKs."""
    sql_path = tmp_path / "library.sql"
    sql_path.write_text(
        """
        CREATE TYPE "public"."book_kind" AS ENUM ('paperback', 'ebook');

        CREATE TABLE "public"."author" (
          id INTEGER PRIMARY KEY,
          email VARCHAR(255) NOT NULL,
          status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'blocked')),
          CONSTRAINT uq_author_email UNIQUE (email)
        );

        CREATE TABLE book (
          id INTEGER PRIMARY KEY,
          title TEXT NOT NULL DEFAULT 'Untitled',
          kind "public"."book_kind" DEFAULT 'paperback',
          isbn TEXT,
          subtitle TEXT,
          author_id INTEGER
        );

        CREATE UNIQUE INDEX ix_book_isbn_unique ON book (isbn);
        CREATE UNIQUE INDEX ix_book_title_subtitle_unique ON book (title, subtitle);
        ALTER TABLE book ADD CONSTRAINT fk_book_author FOREIGN KEY (author_id) REFERENCES "public"."author"(id);
        ALTER TABLE book ADD CONSTRAINT uq_book_title UNIQUE (title);
        """
    )

    schema = load_schema(sql_path)
    author = schema.table("author")
    book = schema.table("book")
    author_columns = {column.name: column for column in author.columns}
    book_columns = {column.name: column for column in book.columns}

    assert author.columns[0].primary_key is True
    assert author_columns["email"].unique is True
    assert author_columns["status"].type_name == "AuthorStatus"
    assert author_columns["status"].default == "active"
    assert book_columns["title"].default == "Untitled"
    assert book_columns["title"].unique is True
    assert book_columns["isbn"].unique is True
    assert book_columns["subtitle"].unique is False
    assert book_columns["kind"].type_name == "book_kind"
    assert book_columns["kind"].default == "paperback"
    assert book_columns["author_id"].references == ("author", "id")
    assert schema.relations[0].source_column == "author_id"
    enum_values = {enum.name: enum.values for enum in schema.enums}
    assert enum_values["AuthorStatus"] == ("active", "blocked")
    assert enum_values["book_kind"] == ("paperback", "ebook")

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_author = next(table for table in manifest["tables"] if table["name"] == "author")
    manifest_status = next(column for column in manifest_author["columns"] if column["name"] == "status")
    manifest_enums = {enum["name"]: enum["values"] for enum in manifest["enums"]}
    assert manifest["source_profile"]["source_kind"] == "sql"
    assert manifest["source_profile"]["counts"]["relations"] == 1
    assert manifest_enums["AuthorStatus"] == ["active", "blocked"]
    assert manifest_enums["book_kind"] == ["paperback", "ebook"]
    assert manifest_status["type"] == "AuthorStatus"
    assert manifest_status["default"] == "active"
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_sql_source_preserves_composite_foreign_key_pairs(tmp_path) -> None:
    """Composite SQL foreign keys preserve source/target column pairings."""
    sql_path = tmp_path / "fulfillment.sql"
    sql_path.write_text(
        """
        CREATE TABLE order_line (
          order_id INTEGER NOT NULL,
          line_no INTEGER NOT NULL,
          sku TEXT NOT NULL,
          PRIMARY KEY (order_id, line_no)
        );

        CREATE TABLE shipment_line (
          order_id INTEGER NOT NULL,
          line_no INTEGER NOT NULL,
          package_no INTEGER NOT NULL,
          PRIMARY KEY (order_id, line_no, package_no),
          CONSTRAINT fk_shipment_order_line
            FOREIGN KEY (order_id, line_no)
            REFERENCES order_line(order_id, line_no)
        );

        CREATE TABLE return_line (
          order_id INTEGER NOT NULL,
          line_no INTEGER NOT NULL,
          reason TEXT,
          PRIMARY KEY (order_id, line_no)
        );

        ALTER TABLE return_line
          ADD CONSTRAINT fk_return_order_line
          FOREIGN KEY (order_id, line_no)
          REFERENCES order_line(order_id, line_no);
        """
    )

    schema = load_schema(sql_path, source_type="sql")
    shipment = schema.table("shipment_line")
    return_line = schema.table("return_line")
    shipment_columns = {column.name: column for column in shipment.columns}
    return_columns = {column.name: column for column in return_line.columns}

    assert shipment_columns["order_id"].references == ("order_line", "order_id")
    assert shipment_columns["line_no"].references == ("order_line", "line_no")
    assert return_columns["order_id"].references == ("order_line", "order_id")
    assert return_columns["line_no"].references == ("order_line", "line_no")
    assert {
        (relation.source_table, relation.source_column, relation.target_table, relation.target_column)
        for relation in schema.relations
        if relation.target_table == "order_line"
    } == {
        ("shipment_line", "order_id", "order_line", "order_id"),
        ("shipment_line", "line_no", "order_line", "line_no"),
        ("return_line", "order_id", "order_line", "order_id"),
        ("return_line", "line_no", "order_line", "line_no"),
    }

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_shipment = next(table for table in manifest["tables"] if table["name"] == "shipment_line")
    manifest_columns = {column["name"]: column for column in manifest_shipment["columns"]}
    assert manifest_columns["order_id"]["references"] == ["order_line", "order_id"]
    assert manifest_columns["line_no"]["references"] == ["order_line", "line_no"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_sql_source_resolves_implicit_primary_key_references(tmp_path) -> None:
    """SQL REFERENCES without a column list points at the target primary key."""
    sql_path = tmp_path / "implicit_refs.sql"
    sql_path.write_text(
        """
        CREATE TABLE publisher (
          code TEXT PRIMARY KEY,
          name TEXT NOT NULL
        );

        CREATE TABLE book (
          isbn TEXT PRIMARY KEY,
          publisher_code TEXT REFERENCES publisher,
          title TEXT NOT NULL
        );

        CREATE TABLE review (
          id INTEGER PRIMARY KEY,
          book_isbn TEXT
        );

        ALTER TABLE review
          ADD CONSTRAINT fk_review_book
          FOREIGN KEY (book_isbn)
          REFERENCES book;
        """
    )

    schema = load_schema(sql_path, source_type="sql")
    book_columns = {column.name: column for column in schema.table("book").columns}
    review_columns = {column.name: column for column in schema.table("review").columns}

    assert book_columns["publisher_code"].references == ("publisher", "code")
    assert review_columns["book_isbn"].references == ("book", "isbn")
    assert {
        (relation.source_table, relation.source_column, relation.target_table, relation.target_column)
        for relation in schema.relations
    } == {
        ("book", "publisher_code", "publisher", "code"),
        ("review", "book_isbn", "book", "isbn"),
    }

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_book = next(table for table in manifest["tables"] if table["name"] == "book")
    manifest_review = next(table for table in manifest["tables"] if table["name"] == "review")
    book_manifest_columns = {column["name"]: column for column in manifest_book["columns"]}
    review_manifest_columns = {column["name"]: column for column in manifest_review["columns"]}
    assert book_manifest_columns["publisher_code"]["references"] == ["publisher", "code"]
    assert review_manifest_columns["book_isbn"]["references"] == ["book", "isbn"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_sql_source_handles_comments_identity_and_generated_columns(tmp_path) -> None:
    """SQL DDL imports tolerate comments, identity syntax, and generated fields."""
    sql_path = tmp_path / "orders.sql"
    sql_path.write_text(
        """
        -- AppGen should ignore comment-only DDL noise.
        CREATE TABLE customer (
          id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
          email TEXT NOT NULL UNIQUE,
          note TEXT DEFAULT 'not -- a comment'
        );

        /*
          Common production DDL contains block comments between statements.
        */
        CREATE TABLE order_header (
          id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          customer_id INTEGER REFERENCES customer,
          quantity NUMERIC(12, 2) NOT NULL DEFAULT 0,
          unit_price NUMERIC(12, 2) NOT NULL DEFAULT 0,
          total NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
          status TEXT CHECK (status IN ('draft', 'posted'))
        );
        """
    )

    schema = load_schema(sql_path, source_type="sql")
    customer_columns = {column.name: column for column in schema.table("customer").columns}
    order_columns = {column.name: column for column in schema.table("order_header").columns}

    assert customer_columns["id"].type_name == "INTEGER"
    assert customer_columns["id"].primary_key is True
    assert customer_columns["email"].unique is True
    assert customer_columns["note"].default == "not -- a comment"
    assert order_columns["id"].type_name == "INTEGER"
    assert order_columns["id"].primary_key is True
    assert order_columns["customer_id"].references == ("customer", "id")
    assert order_columns["quantity"].type_name == "NUMERIC(12, 2)"
    assert order_columns["total"].type_name == "NUMERIC(12, 2)"
    assert order_columns["total"].derived is True
    assert order_columns["total"].expression == "quantity * unit_price"
    assert order_columns["status"].type_name == "OrderHeaderStatus"
    assert {enum.name: enum.values for enum in schema.enums}["OrderHeaderStatus"] == ("draft", "posted")

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_order = next(table for table in manifest["tables"] if table["name"] == "order_header")
    manifest_columns = {column["name"]: column for column in manifest_order["columns"]}
    assert manifest_columns["total"]["derived"] is True
    assert manifest_columns["total"]["expression"] == "quantity * unit_price"
    assert manifest_columns["customer_id"]["references"] == ["customer", "id"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_ponyorm_source_normalizes_entities(tmp_path) -> None:
    """PonyORM-style scripts can become the same canonical schema."""
    pony_path = tmp_path / "entities.py"
    pony_path.write_text(
        """
        import datetime
        from decimal import Decimal
        from enum import Enum
        from pony.orm import Database, PrimaryKey, Required, Optional, Set
        from pony.orm import Json, LongStr


        class Status(Enum):
            draft = "draft"
            published = "published"

        db = Database()

        class Author(db.Entity):
            id = PrimaryKey(int)
            email = Required(str, unique=True)
            display_name = Optional(str, default="Anonymous")
            bio = Optional(LongStr)
            metadata = Optional(Json)
            books = Set('Book')

        class Book(db.Entity):
            id = PrimaryKey(int, auto=True)
            title = Required(str)
            status = Required(Status, default=Status.draft)
            rating = Optional(float, default=0.0)
            price = Optional(Decimal, default=0)
            published_at = Optional(datetime.datetime)
            publication_date = Optional(datetime.date)
            author = Required("Author", reverse="books")
            subtitle = Optional(str)
        """
    )

    schema = load_schema(pony_path, source_type="pony")
    author = schema.table("Author")
    book = schema.table("Book")
    author_columns = {column.name: column for column in author.columns}
    book_columns = {column.name: column for column in book.columns}

    assert book.columns[0].name == "id"
    assert book.columns[1].name == "title"
    assert book_columns["author_id"].references == ("Author", "id")
    assert book_columns["author_id"].nullable is False
    assert book_columns["status"].type_name == "Status"
    assert book_columns["rating"].type_name == "float"
    assert book_columns["rating"].default == "0.0"
    assert book_columns["price"].type_name == "decimal"
    assert book_columns["published_at"].type_name == "datetime"
    assert book_columns["publication_date"].type_name == "date"
    assert author_columns["email"].unique is True
    assert author_columns["display_name"].default == "Anonymous"
    assert author_columns["bio"].type_name == "text"
    assert author_columns["metadata"].type_name == "json"
    assert "books" not in author_columns
    assert schema.enums[0].name == "Status"
    assert schema.enums[0].values == ("draft", "published")
    assert schema.relations[0].source_table == "Book"

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_enums = {enum["name"]: enum["values"] for enum in manifest["enums"]}
    assert manifest["source_profile"]["source_kind"] == "ponyorm"
    assert manifest["source_profile"]["counts"]["relations"] == 1
    assert manifest_enums["Status"] == ["draft", "published"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_ponyorm_source_preserves_many_to_many_sets(tmp_path) -> None:
    """Reciprocal PonyORM Set declarations become a generated association table."""
    pony_path = tmp_path / "learning.py"
    pony_path.write_text(
        """
        from pony.orm import Database, PrimaryKey, Required, Set

        db = Database()

        class Student(db.Entity):
            id = PrimaryKey(int)
            name = Required(str)
            courses = Set("Course")

        class Course(db.Entity):
            id = PrimaryKey(int)
            title = Required(str)
            students = Set(Student)
        """
    )

    schema = load_schema(pony_path, source_type="pony")
    association = schema.table("course_student")
    columns = {column.name: column for column in association.columns}

    assert columns["course_id"].primary_key is True
    assert columns["course_id"].references == ("Course", "id")
    assert columns["student_id"].primary_key is True
    assert columns["student_id"].references == ("Student", "id")
    assert {relation.target_table for relation in schema.relations if relation.source_table == "course_student"} == {
        "Course",
        "Student",
    }
    assert {
        relation.cardinality for relation in schema.relations if relation.source_table == "course_student"
    } == {"many-to-many"}

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    association_manifest = next(table for table in manifest["tables"] if table["name"] == "course_student")
    manifest_columns = {column["name"]: column for column in association_manifest["columns"]}
    assert manifest_columns["course_id"]["references"] == ["Course", "id"]
    assert manifest_columns["student_id"]["references"] == ["Student", "id"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "views.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_ponyorm_source_preserves_non_id_primary_key_relationships(tmp_path) -> None:
    """PonyORM imports point relations at the target entity's declared primary key."""
    pony_path = tmp_path / "catalog.py"
    pony_path.write_text(
        """
        from pony.orm import Database, PrimaryKey, Required, Set

        db = Database()

        class Publisher(db.Entity):
            code = PrimaryKey(str)
            name = Required(str)
            books = Set("Book")

        class Book(db.Entity):
            isbn = PrimaryKey(str)
            title = Required(str)
            publisher = Required(Publisher, reverse="books")
            categories = Set("Category")

        class Category(db.Entity):
            slug = PrimaryKey(str)
            title = Required(str)
            books = Set(Book)
        """
    )

    schema = load_schema(pony_path, source_type="pony")
    book_columns = {column.name: column for column in schema.table("Book").columns}
    association = schema.table("book_category")
    association_columns = {column.name: column for column in association.columns}

    assert "publisher_id" not in book_columns
    assert book_columns["publisher_code"].type_name == "string"
    assert book_columns["publisher_code"].references == ("Publisher", "code")
    assert association_columns["book_isbn"].type_name == "string"
    assert association_columns["book_isbn"].references == ("Book", "isbn")
    assert association_columns["category_slug"].type_name == "string"
    assert association_columns["category_slug"].references == ("Category", "slug")
    assert {relation.target_column for relation in schema.relations if relation.source_table == "book_category"} == {
        "isbn",
        "slug",
    }

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    book_manifest = next(table for table in manifest["tables"] if table["name"] == "Book")
    manifest_columns = {column["name"]: column for column in book_manifest["columns"]}
    assert manifest_columns["publisher_code"]["references"] == ["Publisher", "code"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "views.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_ponyorm_source_preserves_composite_primary_keys(tmp_path) -> None:
    """Class-level PonyORM PrimaryKey calls map to canonical composite keys."""
    pony_path = tmp_path / "orders.py"
    pony_path.write_text(
        """
        from pony.orm import Database, Required, PrimaryKey, Set

        db = Database()

        class Order(db.Entity):
            id = PrimaryKey(int)
            number = Required(str, unique=True)
            lines = Set("OrderLine")

        class OrderLine(db.Entity):
            order = Required(Order)
            line_no = Required(int)
            sku = Required(str)
            PrimaryKey(order, line_no)
        """
    )

    schema = load_schema(pony_path, source_type="pony")
    line = schema.table("OrderLine")
    columns = {column.name: column for column in line.columns}

    assert "id" not in columns
    assert columns["order_id"].primary_key is True
    assert columns["order_id"].references == ("Order", "id")
    assert columns["line_no"].primary_key is True
    assert columns["sku"].primary_key is False

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    line_manifest = next(table for table in manifest["tables"] if table["name"] == "OrderLine")
    manifest_columns = {column["name"]: column for column in line_manifest["columns"]}
    assert manifest_columns["order_id"]["primary_key"] is True
    assert manifest_columns["line_no"]["primary_key"] is True
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_ponyorm_source_preserves_indexes_and_alternate_keys(tmp_path) -> None:
    """PonyORM index metadata becomes canonical unique/searchable hints."""
    pony_path = tmp_path / "crm.py"
    pony_path.write_text(
        """
        from pony.orm import Database, PrimaryKey, Required, Optional, composite_key, composite_index

        db = Database()

        class Contact(db.Entity):
            id = PrimaryKey(int)
            email = Required(str)
            tenant_id = Required(int)
            external_id = Required(str)
            display_name = Required(str, index=True)
            phone = Optional(str)
            composite_key(email)
            composite_key(tenant_id, external_id)
            composite_index(display_name, phone)
        """
    )

    schema = load_schema(pony_path, source_type="pony")
    columns = {column.name: column for column in schema.table("Contact").columns}

    assert columns["email"].unique is True
    assert columns["tenant_id"].unique is False
    assert columns["external_id"].unique is False
    assert columns["display_name"].searchable is True
    assert columns["phone"].searchable is True

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    contact = next(table for table in manifest["tables"] if table["name"] == "Contact")
    manifest_columns = {column["name"]: column for column in contact["columns"]}
    assert manifest_columns["email"]["unique"] is True
    assert manifest_columns["display_name"]["searchable"] is True
    assert manifest_columns["phone"]["searchable"] is True
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)


def test_appgen_cli_generates_from_ponyorm(tmp_path, runner: CliRunner) -> None:
    """The public CLI accepts PonyORM entity scripts as a first-class source."""
    pony_path = tmp_path / "entities.py"
    pony_path.write_text(
        """
        from pony.orm import Database, PrimaryKey, Required, Optional, Set

        db = Database()

        class Customer(db.Entity):
            id = PrimaryKey(int)
            name = Required(str, unique=True)
            invoices = Set("Invoice")

        class Invoice(db.Entity):
            id = PrimaryKey(int)
            total = Required(float, default=0.0)
            customer = Required(Customer)
            note = Optional(str)
        """
    )
    output_dir = tmp_path / "app"

    result = runner.invoke(__main__.main, ["--pony", str(pony_path), "-w", str(output_dir)])

    assert result.exit_code == 0, result.output
    manifest = json.loads((output_dir / "appgen.json").read_text())
    invoice = next(table for table in manifest["tables"] if table["name"] == "Invoice")
    invoice_columns = {column["name"]: column for column in invoice["columns"]}
    assert invoice_columns["total"]["default"] == "0.0"
    assert invoice_columns["customer_id"]["references"] == ["Customer", "id"]
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_access.py"), doraise=True)
    py_compile.compile(str(output_dir / "database_ops.py"), doraise=True)
    assert (output_dir / "templates" / "appgen_database_ops.html").exists()


def test_appgen_dsl_normalizes_low_code_model_and_generates(tmp_path) -> None:
    """The compact ANTLR DSL feeds schema, UI, workflow, and role metadata."""
    dsl_path = tmp_path / "library.ags"
    dsl_path.write_text(
        """
        app Library { theme: "sage" }

        enum Status { draft published archived }

        table Author {
          id: int pk
          name: string required search
          email: email unique
          birth_date: date
          last_seen_at: datetime
          appointment_time: time
        }

        table Book {
          id: int pk
          title: string required search
          status: Status default draft
          summary: text
          cover_image: image
          manuscript_file: file
          internal_code: string hidden
          author_id: int -> Author.id
        }

        view BookList for Book {
          Overview: title, status;
          Assets: cover_image, manuscript_file;
          @ title TextBox 0 0 6 1;
          @ summary TextArea 0 2 8 3;
          @ cover_image ImageUpload 0 6 4 2;
        }

        flow Publish {
          draft -> published;
          published -> archived;
        }

        role Editor {
          Book: read, create, update;
        }

        rule PublishPolicy for Book {
          title required "Title is required";
          status in draft, published, archived;
          status == published -> review;
        }

        llm LocalModel {
          provider: ollama
          mode: local
          model: llama3
          endpoint: "http://localhost:11434"
        }

        llm CloudModel {
          provider: openai
          mode: api
          model: gpt-4.1-mini
          api_key: OPENAI_API_KEY
        }

        agent Publisher {
          provider: LocalModel
          goal: "Review and publish books"
          tools: schema, forms, chatbots
          memory: project
          max_steps: 6
        }
        """
    )

    schema = load_schema(dsl_path, source_type="dsl")
    author = schema.table("Author")
    book = schema.table("Book")
    author_columns = {column.name: column for column in author.columns}
    book_columns = {column.name: column for column in book.columns}

    assert schema.app_name == "Library"
    assert schema.app_options["theme"] == "sage"
    assert schema.enums[0].name == "Status"
    assert schema.enums[0].values == ("draft", "published", "archived")
    assert author_columns["birth_date"].type_name == "date"
    assert author_columns["last_seen_at"].type_name == "datetime"
    assert author_columns["appointment_time"].type_name == "time"
    assert book_columns["status"].default == "draft"
    assert book_columns["summary"].type_name == "text"
    assert book_columns["cover_image"].type_name == "image"
    assert book_columns["manuscript_file"].type_name == "file"
    assert book_columns["author_id"].references == ("Author", "id")
    assert book_columns["title"].searchable is True
    assert book_columns["internal_code"].hidden is True
    assert schema.views[0].fields == ("title", "status", "cover_image", "manuscript_file")
    assert schema.views[0].sections[0].name == "Overview"
    assert schema.views[0].sections[0].fields == ("title", "status")
    assert schema.views[0].components[0].component == "TextBox"
    assert schema.views[0].components[1].field == "summary"
    assert schema.views[0].components[1].w == 8
    assert schema.flows[0].steps[0].source == "draft"
    assert schema.roles[0].permissions[0].actions == ("read", "create", "update")
    assert schema.rules[0].conditions[0].operator == "required"
    assert schema.rules[0].conditions[1].operator == "in"
    assert schema.rules[0].conditions[2].action == "review"
    assert schema.llm_providers[0].name == "LocalModel"
    assert schema.llm_providers[0].mode == "local"
    assert schema.llm_providers[0].endpoint == "http://localhost:11434"
    assert schema.llm_providers[1].model == "gpt-4.1-mini"
    assert schema.llm_providers[1].api_key == "OPENAI_API_KEY"
    assert schema.agents[0].provider == "LocalModel"
    assert schema.agents[0].goal == "Review and publish books"
    assert schema.agents[0].tools == ("schema", "forms", "chatbots")
    assert schema.agents[0].max_steps == 6

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "views.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)
    py_compile.compile(str(output_dir / "gql.py"), doraise=True)
    py_compile.compile(str(output_dir / "security.py"), doraise=True)
    py_compile.compile(str(output_dir / "runtime_security.py"), doraise=True)
    py_compile.compile(str(output_dir / "workflow.py"), doraise=True)
    py_compile.compile(str(output_dir / "rules.py"), doraise=True)
    py_compile.compile(str(output_dir / "health.py"), doraise=True)
    py_compile.compile(str(output_dir / "resilience.py"), doraise=True)
    py_compile.compile(str(output_dir / "performance.py"), doraise=True)
    py_compile.compile(str(output_dir / "runtime_assurance.py"), doraise=True)
    py_compile.compile(str(output_dir / "designer.py"), doraise=True)
    py_compile.compile(str(output_dir / "config_admin.py"), doraise=True)
    py_compile.compile(str(output_dir / "integrations.py"), doraise=True)
    py_compile.compile(str(output_dir / "productivity.py"), doraise=True)
    py_compile.compile(str(output_dir / "lifecycle.py"), doraise=True)
    py_compile.compile(str(output_dir / "tenancy.py"), doraise=True)
    py_compile.compile(str(output_dir / "rls.py"), doraise=True)
    py_compile.compile(str(output_dir / "identity.py"), doraise=True)
    py_compile.compile(str(output_dir / "compliance.py"), doraise=True)
    py_compile.compile(str(output_dir / "assistant.py"), doraise=True)
    py_compile.compile(str(output_dir / "intelligence.py"), doraise=True)
    py_compile.compile(str(output_dir / "chatbot.py"), doraise=True)
    py_compile.compile(str(output_dir / "voice.py"), doraise=True)
    py_compile.compile(str(output_dir / "agents.py"), doraise=True)
    py_compile.compile(str(output_dir / "i18n.py"), doraise=True)
    py_compile.compile(str(output_dir / "text_quality.py"), doraise=True)
    py_compile.compile(str(output_dir / "notifications.py"), doraise=True)
    py_compile.compile(str(output_dir / "platforms.py"), doraise=True)
    py_compile.compile(str(output_dir / "microservices.py"), doraise=True)
    py_compile.compile(str(tmp_path / "sdks" / "appgen_sdks.py"), doraise=True)
    py_compile.compile(str(tmp_path / "sdks" / "python" / "client.py"), doraise=True)
    py_compile.compile(str(output_dir / "collaboration.py"), doraise=True)
    py_compile.compile(str(output_dir / "version_control.py"), doraise=True)
    py_compile.compile(str(output_dir / "realtime.py"), doraise=True)
    py_compile.compile(str(output_dir / "events.py"), doraise=True)
    py_compile.compile(str(output_dir / "rpa.py"), doraise=True)
    py_compile.compile(str(output_dir / "diagnostics.py"), doraise=True)
    py_compile.compile(str(output_dir / "api_testing.py"), doraise=True)
    py_compile.compile(str(output_dir / "code_review.py"), doraise=True)
    py_compile.compile(str(output_dir / "components.py"), doraise=True)
    py_compile.compile(str(output_dir / "view_composition.py"), doraise=True)
    py_compile.compile(str(output_dir / "tabbed_views.py"), doraise=True)
    py_compile.compile(str(output_dir / "form_designer.py"), doraise=True)
    py_compile.compile(str(output_dir / "nl_evolution.py"), doraise=True)
    py_compile.compile(str(output_dir / "dsl_reference.py"), doraise=True)
    py_compile.compile(str(output_dir / "view_experience.py"), doraise=True)
    py_compile.compile(str(output_dir / "support_center.py"), doraise=True)
    py_compile.compile(str(output_dir / "prototyping.py"), doraise=True)
    py_compile.compile(str(output_dir / "erp_templates.py"), doraise=True)
    py_compile.compile(str(output_dir / "project_management.py"), doraise=True)
    py_compile.compile(str(output_dir / "devtools.py"), doraise=True)
    py_compile.compile(str(output_dir / "studio.py"), doraise=True)
    py_compile.compile(str(output_dir / "wizards.py"), doraise=True)
    py_compile.compile(str(output_dir / "branding.py"), doraise=True)
    py_compile.compile(str(output_dir / "extensions.py"), doraise=True)
    py_compile.compile(str(output_dir / "dashboards.py"), doraise=True)
    py_compile.compile(str(output_dir / "usage_analytics.py"), doraise=True)
    py_compile.compile(str(output_dir / "search.py"), doraise=True)
    py_compile.compile(str(output_dir / "media.py"), doraise=True)
    py_compile.compile(str(output_dir / "documents.py"), doraise=True)
    py_compile.compile(str(output_dir / "inventory_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "finance_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "manufacturing_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_access.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_exchange.py"), doraise=True)
    py_compile.compile(str(output_dir / "database_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "schema_import.py"), doraise=True)
    py_compile.compile(str(tmp_path / "config.py"), doraise=True)
    py_compile.compile(str(tmp_path / "seed.py"), doraise=True)
    py_compile.compile(str(tmp_path / "app_custom" / "extensions.py"), doraise=True)
    py_compile.compile(str(tmp_path / "automation" / "appgen_node_red.py"), doraise=True)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    assert manifest["app_name"] == "Library"
    assert manifest["app_options"]["theme"] == "sage"
    assert manifest["enums"][0]["name"] == "Status"
    assert manifest["enums"][0]["values"] == ["draft", "published", "archived"]
    assert manifest["views"][0]["name"] == "BookList"
    assert manifest["views"][0]["sections"][0]["name"] == "Overview"
    assert manifest["views"][0]["sections"][1]["fields"] == ["cover_image", "manuscript_file"]
    assert manifest["views"][0]["components"][0]["component"] == "TextBox"
    assert manifest["views"][0]["components"][1]["field"] == "summary"
    assert manifest["flows"][0]["steps"][1]["target"] == "archived"
    assert manifest["roles"][0]["permissions"][0]["resource"] == "Book"
    assert manifest["rules"][0]["conditions"][0]["message"] == "Title is required"
    manifest_book = next(table for table in manifest["tables"] if table["name"] == "Book")
    manifest_columns = {column["name"]: column for column in manifest_book["columns"]}
    assert manifest_columns["title"]["searchable"] is True
    assert manifest_columns["internal_code"]["hidden"] is True
    assert manifest_columns["status"]["type"] == "Status"
    api_text = (output_dir / "api.py").read_text()
    gql_text = (output_dir / "gql.py").read_text()
    models_text = (output_dir / "models.py").read_text()
    views_text = (output_dir / "views.py").read_text()
    assert "status = Column(Enum('draft', 'published', 'archived', name='status_enum')" in models_text
    assert "class BookRestApi" in api_text
    assert "OpenAPIView" in (output_dir / "openapi.py").read_text()
    assert "method_permission_name = API_PERMISSION_MAP" in api_text
    assert "'post': 'create'" in api_text
    assert "include_columns = ['id', 'title', 'status', 'summary', 'cover_image', 'manuscript_file', 'author']" in api_text
    assert "def pre_add(self, item):" in api_text
    assert "before_save_row('Book'" in api_text
    assert "after_save_row('Book'" in api_text
    assert "internal_code" not in api_text
    assert "class BookObject" in gql_text
    assert "internal_code" not in gql_text
    assert (
        "list_columns = ['title', 'status', 'cover_image', 'manuscript_file'] + "
        "['name', 'code', 'description', 'notes']"
    ) in views_text
    assert "appgen_view_sections = [{'name': 'overview'" in views_text
    assert "'fields': ['cover_image', 'manuscript_file']" in views_text
    assert "appgen_lookup_fields = {'author':" in views_text
    assert "'source_column': 'author_id'" in views_text
    assert "'target_table': 'Author'" in views_text
    assert "'label_fields': ('name', 'email')" in views_text
    assert "search_columns = ['name', 'code', 'description', 'notes'] + ['title']" in views_text
    assert "def pre_add(self, item):" in views_text
    assert "before_save_row('Book'" in views_text
    assert "after_save_row('Book'" in views_text
    assert "ROLE_POLICIES" in (output_dir / "security.py").read_text()
    assert "RuntimeSecurityView" in (output_dir / "runtime_security.py").read_text()
    assert "WorkflowView" in (output_dir / "workflow.py").read_text()
    assert "RulesView" in (output_dir / "rules.py").read_text()
    assert "MonitoringView" in (output_dir / "monitoring.py").read_text()
    assert "ResilienceView" in (output_dir / "resilience.py").read_text()
    assert "PerformanceView" in (output_dir / "performance.py").read_text()
    assert "RuntimeAssuranceView" in (output_dir / "runtime_assurance.py").read_text()
    assert "ReportsView" in (output_dir / "reports.py").read_text()
    assert "DashboardView" in (output_dir / "dashboards.py").read_text()
    assert "UsageAnalyticsView" in (output_dir / "usage_analytics.py").read_text()
    assert "SearchView" in (output_dir / "search.py").read_text()
    assert "MediaView" in (output_dir / "media.py").read_text()
    assert "DocumentManagementView" in (output_dir / "documents.py").read_text()
    assert "InventoryOpsView" in (output_dir / "inventory_ops.py").read_text()
    assert "FinanceOpsView" in (output_dir / "finance_ops.py").read_text()
    assert "ManufacturingOpsView" in (output_dir / "manufacturing_ops.py").read_text()
    assert "DataAccessView" in (output_dir / "data_access.py").read_text()
    assert "DataExchangeView" in (output_dir / "data_exchange.py").read_text()
    assert "DatabaseOpsView" in (output_dir / "database_ops.py").read_text()
    assert "internal_code" not in (output_dir / "reports.py").read_text()
    assert "BackupView" in (output_dir / "backup.py").read_text()
    assert "internal_code" in (output_dir / "backup.py").read_text()
    assert "AppGenDesignerView" in (output_dir / "designer.py").read_text()
    assert "visual_model" in (output_dir / "designer.py").read_text()
    assert "apply_proposal" in (output_dir / "designer.py").read_text()
    assert "proposal_from_payload" in (output_dir / "designer.py").read_text()
    assert "@expose('/proposal'" in (output_dir / "designer.py").read_text()
    assert "ConfigAdminView" in (output_dir / "config_admin.py").read_text()
    assert "IntegrationView" in (output_dir / "integrations.py").read_text()
    assert "TenancyView" in (output_dir / "tenancy.py").read_text()
    assert "RowLevelSecurityView" in (output_dir / "rls.py").read_text()
    assert "IdentityView" in (output_dir / "identity.py").read_text()
    assert "ComplianceView" in (output_dir / "compliance.py").read_text()
    assert "AssistantView" in (output_dir / "assistant.py").read_text()
    assert "GuidedChatbotView" in (output_dir / "chatbot.py").read_text()
    assert "VoiceAssistantView" in (output_dir / "voice.py").read_text()
    assert "LocalizationView" in (output_dir / "i18n.py").read_text()
    assert "DSLReferenceView" in (output_dir / "dsl_reference.py").read_text()
    assert "ViewExperienceView" in (output_dir / "view_experience.py").read_text()
    assert "SupportCenterView" in (output_dir / "support_center.py").read_text()
    assert "PrototypingView" in (output_dir / "prototyping.py").read_text()
    assert "TextQualityView" in (output_dir / "text_quality.py").read_text()
    assert "NotificationView" in (output_dir / "notifications.py").read_text()
    assert "PlatformView" in (output_dir / "platforms.py").read_text()
    assert "MicroserviceView" in (output_dir / "microservices.py").read_text()
    assert "CollaborationView" in (output_dir / "collaboration.py").read_text()
    assert "EventProcessingView" in (output_dir / "events.py").read_text()
    assert "DiagnosticsView" in (output_dir / "diagnostics.py").read_text()
    assert "APITestingView" in (output_dir / "api_testing.py").read_text()
    assert "CodeReviewView" in (output_dir / "code_review.py").read_text()
    assert "ComponentView" in (output_dir / "components.py").read_text()
    assert "WizardView" in (output_dir / "wizards.py").read_text()
    assert "BrandingView" in (output_dir / "branding.py").read_text()
    assert "ExtensionView" in (output_dir / "extensions.py").read_text()
    assert "DSL Draft" in (output_dir / "templates" / "appgen_designer.html").read_text()
    assert "Visual Graph" in (output_dir / "templates" / "appgen_designer.html").read_text()
    assert "Model JSON" in (output_dir / "templates" / "appgen_designer.html").read_text()
    assert "Preview DSL" in (output_dir / "templates" / "appgen_designer.html").read_text()
    assert "Health JSON" in (output_dir / "templates" / "appgen_monitoring.html").read_text()
    assert "Error Handling JSON" in (output_dir / "templates" / "appgen_resilience.html").read_text()
    assert "Business Rules" in (output_dir / "templates" / "appgen_rules.html").read_text()
    assert "OpenAPI JSON" in (output_dir / "templates" / "appgen_openapi.html").read_text()
    assert "Generated performance budgets" in (
        output_dir / "templates" / "appgen_performance.html"
    ).read_text()
    assert "Generated operational assurance" in (
        output_dir / "templates" / "appgen_runtime_assurance.html"
    ).read_text()
    assert "Generated transition cockpit" in (output_dir / "templates" / "appgen_workflows.html").read_text()
    assert "FSM JSON" in (output_dir / "templates" / "appgen_workflows.html").read_text()
    assert "SCXML" in (output_dir / "templates" / "appgen_workflows.html").read_text()
    assert "Workbench JSON" in (output_dir / "templates" / "appgen_workflows.html").read_text()
    assert "Export CSV" in (output_dir / "templates" / "appgen_reports.html").read_text()
    assert "Generated PDF export and email delivery contracts" in (
        output_dir / "templates" / "appgen_report_delivery.html"
    ).read_text()
    assert "Generated dashboard, KPI, and chart contracts" in (
        output_dir / "templates" / "appgen_dashboards.html"
    ).read_text()
    assert "Workbench JSON" in (output_dir / "templates" / "appgen_dashboards.html").read_text()
    usage_template = (output_dir / "templates" / "appgen_usage_analytics.html").read_text()
    assert "app usage analytics" in usage_template
    assert "Release Gate JSON" in usage_template
    assert "Generated search indexes" in (output_dir / "templates" / "appgen_search.html").read_text()
    assert "Generated image and upload field contracts" in (
        output_dir / "templates" / "appgen_media.html"
    ).read_text()
    assert "Document Management" in (
        output_dir / "templates" / "appgen_documents.html"
    ).read_text()
    assert "Inventory Traceability" in (
        output_dir / "templates" / "appgen_inventory_ops.html"
    ).read_text()
    assert "Finance Operations" in (
        output_dir / "templates" / "appgen_finance_ops.html"
    ).read_text()
    assert "Manufacturing Operations" in (
        output_dir / "templates" / "appgen_manufacturing_ops.html"
    ).read_text()
    assert "Data Access" in (
        output_dir / "templates" / "appgen_data_access.html"
    ).read_text()
    assert "Workbench JSON" in (output_dir / "templates" / "appgen_data_access.html").read_text()
    assert "Schema-aware CSV and JSON import/export" in (
        output_dir / "templates" / "appgen_data_exchange.html"
    ).read_text()
    assert "Migration batch planning" in (
        output_dir / "templates" / "appgen_data_exchange.html"
    ).read_text()
    assert "Database Operations" in (
        output_dir / "templates" / "appgen_database_ops.html"
    ).read_text()
    schema_import_template = (output_dir / "templates" / "appgen_schema_import.html").read_text()
    assert "Schema Import" in schema_import_template
    assert "Normalization JSON" in schema_import_template
    assert "Validation JSON" in schema_import_template
    assert "Commands JSON" in schema_import_template
    assert "Release Gate JSON" in schema_import_template
    backup_template = (output_dir / "templates" / "appgen_backup.html").read_text()
    assert "Export all JSON" in backup_template
    assert "Autobackup Schedule JSON" in backup_template
    assert "DR Plan JSON" in backup_template
    assert "Release Gate JSON" in backup_template
    assert "Configuration" in (output_dir / "templates" / "appgen_config.html").read_text()
    assert "Salesforce" in (output_dir / "templates" / "appgen_integrations.html").read_text()
    assert "Entando" in (output_dir / "templates" / "appgen_integrations.html").read_text()
    assert "Invenio" in (output_dir / "templates" / "appgen_integrations.html").read_text()
    assert "Productivity Integrations" in (output_dir / "templates" / "appgen_productivity.html").read_text()
    assert "Lifecycle JSON" in (output_dir / "templates" / "appgen_lifecycle.html").read_text()
    assert "tenant_id" in (output_dir / "templates" / "appgen_tenancy.html").read_text()
    assert "row-level security contracts" in (output_dir / "templates" / "appgen_rls.html").read_text()
    identity_template = (output_dir / "templates" / "appgen_identity.html").read_text()
    assert "OpenID Connect" in identity_template
    assert "Release Gate JSON" in identity_template
    compliance_template = (output_dir / "templates" / "appgen_compliance.html").read_text()
    assert "protected-field" in compliance_template
    assert "Release Gate JSON" in compliance_template
    assert "prediction features" in (output_dir / "templates" / "appgen_assistant.html").read_text()
    assert "Intelligence JSON" in (output_dir / "templates" / "appgen_intelligence.html").read_text()
    assert "Guided Chatbot" in (output_dir / "templates" / "appgen_chatbot.html").read_text()
    assert "Voice JSON" in (output_dir / "templates" / "appgen_voice.html").read_text()
    assert "Generated spell, grammar, and character-count contracts" in (
        output_dir / "templates" / "appgen_text_quality.html"
    ).read_text()
    assert "Generated notification channels" in (output_dir / "templates" / "appgen_notifications.html").read_text()
    platforms_template = (output_dir / "templates" / "appgen_platforms.html").read_text()
    assert "web, PWA, mobile, desktop, and chatbot" in platforms_template
    assert "Generation Matrix JSON" in platforms_template
    assert "Release Gate JSON" in platforms_template
    assert "microservices architecture contract" in (output_dir / "templates" / "appgen_microservices.html").read_text()
    assert "class AppGenClient" in (tmp_path / "sdks" / "python" / "client.py").read_text()
    assert "export class AppGenClient" in (tmp_path / "sdks" / "javascript" / "client.js").read_text()
    assert "change proposals" in (output_dir / "templates" / "appgen_collaboration.html").read_text()
    assert "rollback" in (output_dir / "templates" / "appgen_version_control.html").read_text()
    assert "Visual Studio Code" in (output_dir / "templates" / "appgen_devtools.html").read_text()
    assert "JetBrains" in (output_dir / "templates" / "appgen_devtools.html").read_text()
    studio_template = (output_dir / "templates" / "appgen_studio.html").read_text()
    assert "Developer Studio" in studio_template
    assert "Project Tree JSON" in studio_template
    assert "Capability Matrix JSON" in studio_template
    assert "Diagnostics JSON" in studio_template
    assert "Release Gate JSON" in studio_template
    assert "DSL Editor" in studio_template
    assert "Database Designer" in studio_template
    assert "DBML" in studio_template
    assert "SQL Builder JSON" in studio_template
    assert "parameterized query builder" in studio_template
    assert "SQL DDL" in studio_template
    assert "Workspace JSON" in studio_template
    assert "event-stream contracts" in (output_dir / "templates" / "appgen_realtime.html").read_text()
    assert "permissions per tab" in (output_dir / "templates" / "appgen_tabbed_views.html").read_text()
    assert "complex event processing" in (output_dir / "templates" / "appgen_events.html").read_text()
    assert "RPA &amp; BPA" in (output_dir / "templates" / "appgen_rpa.html").read_text()
    assert "runtime self-tests" in (output_dir / "templates" / "appgen_diagnostics.html").read_text()
    assert "automated API testing" in (output_dir / "templates" / "appgen_api_testing.html").read_text()
    assert "Release Gate JSON" in (output_dir / "templates" / "appgen_api_testing.html").read_text()
    assert "Generated automated code-review findings" in (
        output_dir / "templates" / "appgen_code_review.html"
    ).read_text()
    assert "Generated component and widget contracts" in (
        output_dir / "templates" / "appgen_components.html"
    ).read_text()
    assert "Keyword Budget" in (output_dir / "templates" / "appgen_dsl_reference.html").read_text()
    assert "Reference JSON" in (output_dir / "templates" / "appgen_dsl_reference.html").read_text()
    assert "Language Quality JSON" in (output_dir / "templates" / "appgen_dsl_reference.html").read_text()
    assert "View Experience" in (output_dir / "templates" / "appgen_view_experience.html").read_text()
    assert "Presence JSON" in (output_dir / "templates" / "appgen_view_experience.html").read_text()
    assert "data-appgen-time-on-page" in (output_dir / "static" / "appgen-view-experience.js").read_text()
    assert "Support Center" in (output_dir / "templates" / "appgen_support_center.html").read_text()
    assert "Tutorials JSON" in (output_dir / "templates" / "appgen_support_center.html").read_text()
    assert "Low-Code Feature Matrix" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Feature Matrix JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Roadmap Sources JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "JHipster Comparison JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Superset Certification JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Superset Scorecard JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Superset Evidence JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Superset Blueprint JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Capability Depth JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    assert "Superiority Tiers JSON" in (output_dir / "templates" / "appgen_low_code_features.html").read_text()
    erp_template_text = (output_dir / "templates" / "appgen_erp_templates.html").read_text()
    assert "Roadmap JSON" in erp_template_text
    assert "Release Gate JSON" in erp_template_text
    assert "Prototype JSON" in (output_dir / "templates" / "appgen_prototyping.html").read_text()
    assert "Generated sequential user-input" in (output_dir / "templates" / "appgen_wizards.html").read_text()
    branding_template = (output_dir / "templates" / "appgen_branding.html").read_text()
    assert "Generated branding contract" in branding_template
    assert "Design System JSON" in branding_template
    assert "Quality JSON" in branding_template
    assert "Visual Quality JSON" in branding_template
    assert "Responsive Layouts" in branding_template
    assert "Visual Regression JSON" in branding_template
    assert "UI Release Gate JSON" in branding_template
    assert "Viewport Contracts" in branding_template
    assert "contrast, palette balance, no-overlap" in branding_template
    assert "Component States" in branding_template
    assert "app_custom/extensions.py" in (output_dir / "templates" / "appgen_extensions.html").read_text()
    assert "Library" in (tmp_path / "README.md").read_text()
    accessibility_text = (tmp_path / "docs" / "accessibility.md").read_text()
    assert "skip-to-content" in accessibility_text
    assert "Run an automated WCAG scan" in accessibility_text
    assert "BABEL_DEFAULT_LOCALE = \"en\"" in (tmp_path / "config.py").read_text()
    assert "[jinja2: app/templates/**.html]" in (tmp_path / "babel.cfg").read_text()
    messages_text = (output_dir / "translations" / "en" / "LC_MESSAGES" / "messages.po").read_text()
    assert 'msgid "Library"' in messages_text
    assert 'msgid "Book"' in messages_text
    assert 'msgid "Internal Code"' in messages_text
    pwa_manifest = json.loads((output_dir / "static" / "appgen.webmanifest").read_text())
    assert pwa_manifest["display"] == "standalone"
    assert pwa_manifest["name"] == "Library"
    assert pwa_manifest["theme_color"] == "#2f6f5e"
    assert "APPGEN_CACHE" in (output_dir / "static" / "appgen-sw.js").read_text()
    theme_css = (output_dir / "static" / "appgen-theme.css").read_text()
    assert "--appgen-primary: #2f6f5e;" in theme_css
    assert "--appgen-accent: #9a6b2f;" in theme_css
    assert "--appgen-focus-ring:" in theme_css
    assert "--appgen-state-hover:" in theme_css
    assert "--appgen-state-selected:" in theme_css
    assert "--appgen-state-invalid:" in theme_css
    assert "--appgen-touch-target: 44px;" in theme_css
    assert "--appgen-content-max: 1180px;" in theme_css
    assert ".appgen-page-header" in theme_css
    assert "fill=\"#2f6f5e\"" in (output_dir / "static" / "appgen-icon.svg").read_text()
    assert "Library is offline" in (output_dir / "static" / "appgen-offline.html").read_text()
    assert "Book Schema" not in (tmp_path / "docs" / "schema.md").read_text()
    assert "internal_code | string" in (tmp_path / "docs" / "schema.md").read_text()
    assert "```mermaid" in (tmp_path / "docs" / "schema.md").read_text()
    assert "Author ||--o{ Book : author_id" in (tmp_path / "docs" / "schema.md").read_text()
    home_text = (output_dir / "templates" / "my_index.html").read_text()
    assert "Generated by AppGen" in home_text
    assert "Skip to content" in home_text
    assert 'id="appgen-main"' in home_text
    assert 'aria-labelledby="appgen-title"' in home_text
    assert "/static/appgen.webmanifest" in home_text
    assert "/static/appgen-theme.css" in home_text
    assert "navigator.serviceWorker.register" in home_text
    security = _load_module(output_dir / "security.py", "generated_security")
    runtime_security = _load_module(output_dir / "runtime_security.py", "generated_runtime_security")
    workflow = _load_module(output_dir / "workflow.py", "generated_workflow")
    openapi = _load_module(output_dir / "openapi.py", "generated_openapi")
    rules = _load_module(output_dir / "rules.py", "generated_rules")
    validation = _load_module(output_dir / "validation.py", "generated_validation")
    health = _load_module(output_dir / "health.py", "generated_health")
    monitoring = _load_module(output_dir / "monitoring.py", "generated_monitoring")
    resilience = _load_module(output_dir / "resilience.py", "generated_resilience")
    performance = _load_module(output_dir / "performance.py", "generated_performance")
    reports = _load_module(output_dir / "reports.py", "generated_reports")
    report_delivery = _load_module(output_dir / "report_delivery.py", "generated_report_delivery")
    dashboards = _load_module(output_dir / "dashboards.py", "generated_dashboards")
    usage_analytics = _load_module(output_dir / "usage_analytics.py", "generated_usage_analytics")
    search = _load_module(output_dir / "search.py", "generated_search")
    media = _load_module(output_dir / "media.py", "generated_media")
    documents = _load_module(output_dir / "documents.py", "generated_documents")
    inventory_ops = _load_module(output_dir / "inventory_ops.py", "generated_inventory_ops")
    finance_ops = _load_module(output_dir / "finance_ops.py", "generated_finance_ops")
    manufacturing_ops = _load_module(output_dir / "manufacturing_ops.py", "generated_manufacturing_ops")
    data_access = _load_module(output_dir / "data_access.py", "generated_data_access")
    data_exchange = _load_module(output_dir / "data_exchange.py", "generated_data_exchange")
    database_ops = _load_module(output_dir / "database_ops.py", "generated_database_ops")
    schema_import = _load_module(output_dir / "schema_import.py", "generated_schema_import")
    backup = _load_module(output_dir / "backup.py", "generated_backup")
    designer = _load_module(output_dir / "designer.py", "generated_designer")
    form_designer = _load_module(output_dir / "form_designer.py", "generated_form_designer")
    nl_evolution = _load_module(output_dir / "nl_evolution.py", "generated_nl_evolution")
    dsl_reference = _load_module(output_dir / "dsl_reference.py", "generated_dsl_reference")
    view_experience = _load_module(output_dir / "view_experience.py", "generated_view_experience")
    support_center = _load_module(output_dir / "support_center.py", "generated_support_center")
    prototyping = _load_module(output_dir / "prototyping.py", "generated_prototyping")
    config_admin = _load_module(output_dir / "config_admin.py", "generated_config_admin")
    integrations = _load_module(output_dir / "integrations.py", "generated_integrations")
    productivity = _load_module(output_dir / "productivity.py", "generated_productivity")
    lifecycle = _load_module(output_dir / "lifecycle.py", "generated_lifecycle")
    tenancy = _load_module(output_dir / "tenancy.py", "generated_tenancy")
    rls = _load_module(output_dir / "rls.py", "generated_rls")
    identity = _load_module(output_dir / "identity.py", "generated_identity")
    compliance = _load_module(output_dir / "compliance.py", "generated_compliance")
    assistant = _load_module(output_dir / "assistant.py", "generated_assistant")
    intelligence = _load_module(output_dir / "intelligence.py", "generated_intelligence")
    chatbot = _load_module(output_dir / "chatbot.py", "generated_chatbot")
    voice = _load_module(output_dir / "voice.py", "generated_voice")
    agents = _load_module(output_dir / "agents.py", "generated_agents")
    i18n = _load_module(output_dir / "i18n.py", "generated_i18n")
    text_quality = _load_module(output_dir / "text_quality.py", "generated_text_quality")
    notifications = _load_module(output_dir / "notifications.py", "generated_notifications")
    platforms = _load_module(output_dir / "platforms.py", "generated_platforms")
    microservices = _load_module(output_dir / "microservices.py", "generated_microservices")
    sdks = _load_module(tmp_path / "sdks" / "appgen_sdks.py", "generated_sdks")
    collaboration = _load_module(output_dir / "collaboration.py", "generated_collaboration")
    version_control = _load_module(output_dir / "version_control.py", "generated_version_control")
    realtime = _load_module(output_dir / "realtime.py", "generated_realtime")
    events = _load_module(output_dir / "events.py", "generated_events")
    rpa = _load_module(output_dir / "rpa.py", "generated_rpa")
    diagnostics = _load_module(output_dir / "diagnostics.py", "generated_diagnostics")
    api_testing = _load_module(output_dir / "api_testing.py", "generated_api_testing")
    code_review = _load_module(output_dir / "code_review.py", "generated_code_review")
    components = _load_module(output_dir / "components.py", "generated_components")
    view_composition = _load_module(output_dir / "view_composition.py", "generated_view_composition")
    tabbed_views = _load_module(output_dir / "tabbed_views.py", "generated_tabbed_views")
    erp_templates = _load_module(output_dir / "erp_templates.py", "generated_erp_templates")
    project_management = _load_module(output_dir / "project_management.py", "generated_project_management")
    devtools = _load_module(output_dir / "devtools.py", "generated_devtools")
    studio = _load_module(output_dir / "studio.py", "generated_studio")
    wizards = _load_module(output_dir / "wizards.py", "generated_wizards")
    branding = _load_module(output_dir / "branding.py", "generated_branding")
    low_code_features = _load_module(output_dir / "low_code_features.py", "generated_low_code_features")
    extensions = _load_module(output_dir / "extensions.py", "generated_extensions")
    appgen_package = _load_module(tmp_path / "appgen_package.py", "generated_appgen_package")
    generated_coverage = _load_module(tmp_path / "tests" / "test_generated_coverage.py", "generated_test_coverage")
    node_red = _load_module(tmp_path / "automation" / "appgen_node_red.py", "generated_node_red_dsl")
    seed = _load_module(tmp_path / "seed.py", "generated_seed")
    assert security.can("Editor", "Book", "update") is True
    assert security.can("Editor", "Book", "delete") is False
    principal = security.normalize_principal({"sub": "u1", "roles": ["Editor"], "tenant_id": "acme"})
    assert principal["id"] == "u1"
    assert principal["roles"] == ("Editor",)
    assert security.principal_allowed_actions(principal, "Book") == ("read", "create", "update")
    allow_decision = security.authorize(principal, "Book", "update")
    assert allow_decision["ok"] is True
    deny_decision = security.authorize(principal, "Book", "delete")
    assert deny_decision["reason"] == "missing_permission"
    assert security.authorization_audit_event(deny_decision, request_id="req-1")["event"] == "security.authorization.denied"
    assert any(row["role"] == "Editor" and row["resource"] == "Book" for row in security.policy_matrix())
    proposal = security.access_change_proposal("Editor", "Book", ("read", "delete"), actor="ada")
    assert proposal["review_required"] is True
    assert proposal["dsl"] == "role Editor {\n  Book: read, delete;\n}\n"
    threat_model = security.threat_model()
    assert threat_model["format"] == "appgen.security-threat-model.v1"
    assert ("Book", "cover_image") in threat_model["protected_fields"]
    assert any(item["id"] == "secret-exposure" for item in threat_model["threats"])
    assert security.secret_exposure_scan({"SECRET_KEY": "change-me-before-deploy"})["ok"] is False
    assert security.dependency_security_plan()["commands"][0] == "python -m pip-audit -r requirements.txt"
    assert security.api_security_test_plan()["cases"]
    security_gate = security.security_gate_plan(
        {"SECRET_KEY": "x" * 32},
        {"app/security.py", "app/runtime_security.py", "app/identity.py", "app/rls.py", "app/compliance.py"},
    )
    assert security_gate["format"] == "appgen.security-gate-plan.v1"
    assert security_gate["ok"] is True
    assert security.security_signoff(
        {"SECRET_KEY": "x" * 32},
        {"app/security.py", "app/runtime_security.py", "app/identity.py", "app/rls.py", "app/compliance.py"},
        actor="ada",
    )["decision"] == "approved"
    assert runtime_security.security_policy()["idle_timeout_seconds"] == 1800
    assert runtime_security.is_public_path("/static/app.css") is True
    assert runtime_security.is_public_path("/book/list/") is False
    assert runtime_security.should_logout(1000, now=runtime_security.datetime.fromtimestamp(1000 + 1801, runtime_security.timezone.utc)) is True
    session_data = {}
    runtime_security.mark_activity(session_data, now=runtime_security.datetime.fromtimestamp(2000, runtime_security.timezone.utc))
    assert session_data["_appgen_last_seen"] == 2000
    assert runtime_security.session_state(session_data, now=runtime_security.datetime.fromtimestamp(2100, runtime_security.timezone.utc))["remaining_seconds"] == 1700
    headers = runtime_security.security_headers({"X-Frame-Options": "DENY"})
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["X-Content-Type-Options"] == "nosniff"
    openapi_spec = openapi.openapi_spec()
    assert openapi_spec["openapi"] == "3.1.0"
    assert "/api/v1/book/" in openapi_spec["paths"]
    assert openapi_spec["components"]["schemas"]["Book"]["properties"]["status"]["enum"] == [
        "draft",
        "published",
        "archived",
    ]
    assert openapi.openapi_check(
        {"app/openapi.py", "docs/openapi.json", "app/templates/appgen_openapi.html"}
    )["ok"] is True
    docs_openapi = json.loads((tmp_path / "docs" / "openapi.json").read_text())
    assert docs_openapi["openapi"] == "3.1.0"
    assert workflow.next_states("Publish", "draft") == ("published",)
    assert workflow.can_transition("Publish", "published", "archived") is True
    assert workflow.transition("Publish", "published", "archived") == "archived"
    assert workflow.start_states("Publish") == ("draft",)
    assert workflow.terminal_states("Publish") == ("archived",)
    assert workflow.advance_plan("Publish", "draft") == ("draft", "published", "archived")
    assert workflow.workflow_catalog()[0]["name"] == "Publish"
    assert workflow.workflow_catalog()[0]["authorization"]["format"] == "appgen.workflow-authorization.v1"
    assert workflow.workflow_authorization_policy("Publish")["roles"] == ("Editor",)
    assert workflow.can_transition_as("Publish", "draft", "published", {"roles": ["Editor"]}) is True
    assert workflow.can_transition_as("Publish", "draft", "published", {"roles": ["Viewer"]}) is False
    auth_plan = workflow.transition_authorization_plan("Publish", "draft", "published", {"role": "Editor"})
    assert auth_plan["allowed"] is True
    assert auth_plan["required_roles"] == ("Editor",)
    assert workflow.transition_graph("Publish") == {
        "draft": ("published",),
        "published": ("archived",),
        "archived": (),
    }
    assert workflow.statechart_mermaid("Publish").startswith("stateDiagram-v2\n  [*] --> draft")
    fsm = workflow.fsm_export("Publish")
    assert fsm["initial"] == ("draft",)
    assert fsm["final"] == ("archived",)
    assert fsm["transitions"][0]["event"] == "draft_to_published"
    assert workflow.workflow_graph_check("Publish")["ok"] is True
    auth_flow = workflow.authorization_flow("Publish")
    assert auth_flow["format"] == "appgen.workflow-authorization-flow.v1"
    assert auth_flow["transitions"][0]["roles"] == ("Editor",)
    approval_route = workflow.workflow_approval_route("Publish")
    assert approval_route["format"] == "appgen.workflow-approval-route.v1"
    assert approval_route["steps"][0]["approval_roles"] == ("Editor",)
    sla_plan = workflow.workflow_sla_plan("Publish", hours=8)
    assert sla_plan["target_hours"] == 8
    assert sla_plan["escalation_after_hours"] == 16
    audit_event = workflow.workflow_audit_event("Publish", "draft", "published", actor="Editor")
    assert audit_event["format"] == "appgen.workflow-audit-event.v1"
    assert audit_event["allowed"] is True
    runbook = workflow.transition_runbook("Publish", "draft", "published", {"roles": ["Editor"]})
    assert runbook["format"] == "appgen.workflow-transition-runbook.v1"
    assert runbook["approval_route"]["workflow"] == "Publish"
    scxml = workflow.scxml_export("Publish")
    assert scxml.startswith("<scxml")
    assert '<transition event="draft_to_published" target="published" />' in scxml
    workbench = workflow.statechart_workbench("Publish")
    assert workbench["exports"]["scxml"].startswith("<scxml")
    assert workbench["authorization"]["roles"] == ("Editor",)
    assert workbench["approval_route"]["steps"][0]["audit_required"] is True
    assert workbench["sla"]["metrics"][0] == "age_hours"
    assert workbench["diagnostics"]["ok"] is True
    proposal = workflow.transition_proposal("Publish", "review", "approved", actor="ada")
    assert proposal["requires_review"] is True
    assert proposal["dsl"] == "flow Publish {\n  review -> approved;\n}\n"
    assert "New source state: review" in proposal["warnings"]
    assert rules.rules_for_table("Book")[0]["name"] == "PublishPolicy"
    assert rules.validate_row("Book", {"status": "draft"})["errors"][0]["message"] == "Title is required"
    assert rules.validate_row("Book", {"title": "Dune", "status": "draft"})["ok"] is True
    assert rules.decision_plan("Book", {"title": "Dune", "status": "published"})["decisions"] == ("review",)
    decision_tree = rules.rule_decision_tree("PublishPolicy")
    assert decision_tree["format"] == "appgen.decision-tree.v1"
    assert any(node["type"] == "action" and node["action"] == "review" for node in decision_tree["nodes"])
    assert rules.decision_tree_catalog("Book")[0]["rule"] == "PublishPolicy"
    decision_trace = rules.decision_trace("Book", {"title": "Dune", "status": "published"})
    assert decision_trace["format"] == "appgen.decision-trace.v1"
    assert decision_trace["decisions"] == ("review",)
    assert rules.rules_check({"app/rules.py", "app/templates/appgen_rules.html"})["ok"] is True
    assert validation.table_validation_contract("Book")["name"] == "Book"
    assert validation.field_validation_contract("Book", "status")["enum_values"] == ("draft", "published", "archived")
    assert validation.validate_payload("Book", {"status": "draft"})["errors"][0]["code"] == "required"
    assert validation.validate_payload("Book", {"title": "Dune", "status": "missing"})["errors"][0]["code"] == "enum"
    assert validation.validate_payload("Book", {"title": "Dune", "status": "draft"})["ok"] is True
    assert validation.validate_payload("Book", {"title": "Dune"}, partial=True)["ok"] is True
    assert validation.ui_validation_schema("Book")["format"] == "appgen.ui-validation.v1"
    assert validation.validation_check({"app/validation.py"})["ok"] is True
    assert branding.theme_contract()["theme"] == "sage"
    assert branding.css_variables()["--appgen-primary"] == "#2f6f5e"
    assert branding.css_variables()["--appgen-content-max"] == "1180px"
    assert branding.typography_scale()["sizes"]["page"] == "1.5rem"
    assert branding.density_modes()["touch"]["control_height"] == "48px"
    assert branding.design_tokens()["radius"]["panel"] == "8px"
    assert branding.layout_contract("record-form")["validation"] == "summary + field messages"
    assert branding.design_system_report()["format"] == "appgen.design-system.v1"
    assert branding.theme_quality_report()["ok"] is True
    assert branding.viewport_contract("mobile")["density"] == "touch"
    assert branding.viewport_contract("desktop")["page_header"] == "title + actions"
    assert branding.component_state_matrix("form-control")["invalid"]["message_required"] is True
    assert branding.component_state_matrix("table-row")["selected"]["aria_selected"] is True
    assert branding.visual_regression_plan()["format"] == "appgen.visual-regression.v1"
    assert branding.visual_test_matrix()["format"] == "appgen.visual-test-matrix.v1"
    assert {"mobile", "tablet", "desktop"} <= {row["viewport"] for row in branding.visual_test_matrix()["rows"]}
    assert "invalid" in branding.visual_test_matrix("record-form")["states"]
    assert branding.contrast_ratio("#14213d", "#f8fafc") >= 4.5
    assert branding.palette_balance_report()["ok"] is True
    assert branding.visual_experience_quality_report()["format"] == "appgen.visual-experience-quality.v1"
    assert branding.visual_experience_quality_report()["ok"] is True
    assert any(item["check"] == "no_overlap_review" for item in branding.visual_experience_quality_report()["checks"])
    assert "mobile" in branding.design_system_report()["viewports"]
    assert branding.component_style_contract("button")["min_height"] == "44px"
    assert branding.component_style_contract("page-header")["responsive_behavior"] == "actions wrap below title on mobile"
    assert branding.component_style_contract("dashboard-card")["accent_border"] == "4px"
    assert branding.accessibility_theme_check()["ok"] is True
    assert any(item["wcag"] == "2.4.1" for item in branding.accessibility_checklist())
    assert branding.accessibility_audit_plan()["format"] == "appgen.accessibility-audit.v1"
    assert branding.accessibility_audit_plan("home")["ok"] is True
    assert branding.keyboard_navigation_plan("home")[0]["escape_hatch"] == "skip_to_content"
    assert branding.aria_landmark_contract("home")[0]["requires_main"] is True
    assert branding.asset_check(
        {"app/branding.py", "app/static/appgen-theme.css", "app/templates/appgen_branding.html"}
    )["ok"] is True
    assert branding.asset_check(
        {"app/branding.py", "app/static/appgen-theme.css", "app/templates/appgen_branding.html"}
    )["quality"]["format"] == "appgen.theme-quality.v1"
    assert branding.asset_check(
        {"app/branding.py", "app/static/appgen-theme.css", "app/templates/appgen_branding.html"}
    )["visual_regression"]["format"] == "appgen.visual-regression.v1"
    ui_gate = branding.ui_experience_release_gate(
        {"app/branding.py", "app/static/appgen-theme.css", "app/templates/appgen_branding.html"}
    )
    assert ui_gate["format"] == "appgen.ui-experience-release-gate.v1"
    assert ui_gate["ok"] is True
    assert {"theme_quality", "visual_quality", "accessibility", "visual_regression", "assets"} <= {
        item["gate"] for item in ui_gate["gates"]
    }
    assert branding.ui_experience_release_gate({"app/branding.py"})["ok"] is False
    assert low_code_features.readiness_report()["source"]["document"] == "docs/Lo-code features.md"
    assert {"docs/ideas.md", "docs/base_features.md", "docs/Lo-code features.md"} == {
        item["document"] for item in low_code_features.source_document_contracts()
    }
    assert low_code_features.roadmap_source_report()["format"] == "appgen.roadmap-source-report.v1"
    assert low_code_features.roadmap_source_report()["ok"] is True
    assert low_code_features.roadmap_source_report()["base_features_complete"] is True
    assert low_code_features.roadmap_source_report()["ideas_roadmap_complete"] is True
    assert "schema-sources" in {item["id"] for item in low_code_features.ideas_roadmap_alignment()}
    assert "deployment" in {item["id"] for item in low_code_features.base_feature_alignment()}
    assert low_code_features.readiness_report()["alignment_complete"] is True
    assert low_code_features.readiness_report()["roadmap_sources_ok"] is True
    assert low_code_features.readiness_report()["competitive_position"] == "broader-than-jhipster"
    assert low_code_features.readiness_report()["competitive_advantage_count"] >= 7
    assert low_code_features.readiness_report()["jhipster_superset_ok"] is True
    assert low_code_features.jhipster_competitive_report()["ok"] is True
    assert low_code_features.jhipster_competitive_report()["superset_scorecard"]["ok"] is True
    assert low_code_features.jhipster_capability_benchmark()["ok"] is True
    assert low_code_features.jhipster_superset_scorecard()["position"] == "more-capable-than-jhipster"
    assert low_code_features.jhipster_superset_scorecard()["minimum_appgen_only_advantages"] == 10
    assert low_code_features.jhipster_superset_scorecard()["blocking_gaps"] == ()
    assert low_code_features.jhipster_superset_evidence()["ok"] is True
    assert low_code_features.jhipster_superset_evidence({"app/designer.py"})["ok"] is False
    depth = low_code_features.jhipster_capability_depth_index()
    assert depth["format"] == "appgen.jhipster-capability-depth-index.v1"
    assert depth["ok"] is True
    assert depth["minimum_dimensions_per_area"] == 4
    assert {item["area"] for item in depth["areas"]} >= {"visual_builders", "agentic_systems", "database_ide"}
    assert low_code_features.jhipster_capability_depth_index({"app/designer.py"})["ok"] is False
    certification = low_code_features.jhipster_superset_certification()
    assert certification["format"] == "appgen.jhipster-superset-certification.v1"
    assert certification["certification"] == "appgen-more-capable-than-jhipster"
    assert certification["ok"] is True
    assert certification["blocking_gaps"] == ()
    assert certification["advantage_ratio"] >= 2.0
    assert certification["capability_depth"]["ok"] is True
    assert "jhipster/app.jdl" in certification["generated_contracts"]
    assert "app/form_designer.py" in certification["generated_contracts"]
    assert low_code_features.jhipster_superset_certification({"app/designer.py"})["ok"] is False
    blueprint = low_code_features.jhipster_superset_blueprint()
    assert blueprint["format"] == "appgen.jhipster-superset-blueprint.v1"
    assert blueprint["ok"] is True
    assert "/form-designer/" in {item["route"] for item in blueprint["route_map"]}
    assert {"design", "generate", "operate", "evolve", "compose"} == {item["pillar"] for item in blueprint["pillars"]}
    superiority = low_code_features.jhipster_superiority_tiers()
    assert superiority["format"] == "appgen.jhipster-superiority-tiers.v1"
    assert superiority["ok"] is True
    assert superiority["minimum_appgen_only_advantages"] == 10
    assert superiority["stop_condition"] == "do-not-claim-jhipster-superiority-unless-ok-is-true"
    assert {"preserve-baseline", "outperform-baseline", "product-platform"} == {
        item["tier"] for item in superiority["tiers"]
    }
    assert "/studio/" in next(item for item in superiority["tiers"] if item["tier"] == "product-platform")[
        "present_routes"
    ]
    assert low_code_features.readiness_report()["jhipster_superset_blueprint_ok"] is True
    assert low_code_features.readiness_report()["jhipster_superiority_ok"] is True
    assert low_code_features.readiness_report()["jhipster_capability_depth_ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["jhipster_superset_blueprint_ok"] is True
    assert low_code_features.jhipster_superset_blueprint({"app/form_designer.py"})["ok"] is False
    assert {
        gate["area"] for gate in low_code_features.jhipster_superset_scorecard()["required_gates"]
    } >= {
        "visual_builders",
        "schema_import",
        "native_targets",
        "agentic_systems",
        "erp_templates",
        "runtime_assurance",
        "database_ide",
    }
    assert len(low_code_features.jhipster_competitive_report()["appgen_differentiators"]) >= 7
    assert "agentic_systems" in {item["area"] for item in low_code_features.jhipster_competitive_report()["appgen_only_capabilities"]}
    assert "runtime_assurance" in {item["area"] for item in low_code_features.jhipster_competitive_report()["appgen_only_capabilities"]}
    assert "database_ide" in {item["area"] for item in low_code_features.jhipster_competitive_report()["appgen_only_capabilities"]}
    assert "application_composition" in {
        item["area"] for item in low_code_features.jhipster_competitive_report()["appgen_only_capabilities"]
    }
    assert "ui.form-designer" in {item["key"] for item in low_code_features.capability_matrix()}
    assert "components.application-composition" in {item["key"] for item in low_code_features.capability_matrix()}
    assert "platform.jhipster-superiority" in {item["key"] for item in low_code_features.capability_matrix()}
    assert "ai.agentic-systems" in {item["key"] for item in low_code_features.grouped_capabilities()["ai"]}
    composition_plan = low_code_features.composition_install_plan(("agentic-suite", "erp-suite"))
    assert composition_plan["format"] == "appgen.composition-install-plan.v1"
    assert "schema-core" in composition_plan["blocks"]
    assert low_code_features.composition_package("builder-suite", ("visual-builder",))["publish_targets"] == (
        "studio",
        "entando",
        "invenio",
        "cookiecutter",
    )
    assert low_code_features.composition_preview(("native-targets",))["destructive"] is False
    assert low_code_features.composition_marketplace_readiness(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["jhipster_superset_ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["jhipster_certification_ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["jhipster_superiority_ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["jhipster_capability_depth_ok"] is True
    assert low_code_features.low_code_features_check(
        {"app/low_code_features.py", "app/templates/appgen_low_code_features.html", "app/appgen.json"}
    )["roadmap_sources_ok"] is True
    hook_names = {hook["hook"] for hook in extensions.extension_points()}
    assert {"startup", "validate_book", "before_save_book", "after_save_book"} <= hook_names
    assert extensions.dispatch("missing_hook", {"ok": True}) == {"ok": True}
    generated_validation = extensions.validate_row("Book", {"status": "draft"})
    assert generated_validation["ok"] is False
    assert generated_validation["errors"][0]["message"] == "Title is required"
    assert extensions.validate_row("Book", {"title": "Dune", "status": "draft"})["ok"] is True
    assert extensions.validate_row("Book", {"title": "Dune", "status": "published"})["decisions"] == ("review",)
    assert extensions.before_save_row("Book", {"title": "Dune", "status": "draft"}) == {
        "title": "Dune",
        "status": "draft",
    }
    with pytest.raises(ValueError, match="Title is required"):
        extensions.before_save_row("Book", {"status": "draft"})
    assert extensions.after_save_row("Book", {"title": "Dune"}) == {"title": "Dune"}
    assert extensions.extension_check(
        {
            "app/extensions.py",
            "app/templates/appgen_extensions.html",
            "app_custom/__init__.py",
            "app_custom/extensions.py",
        }
    )["ok"] is True
    assert appgen_package.package_metadata()["package_name"] == "appgen-library"
    assert appgen_package.fab_extension_contract()["custom_hooks"] == "app_custom.extensions"
    assert appgen_package.cookiecutter_context()["project_slug"] == "appgen_library"
    assert appgen_package.packaging_check(
        {
            "pyproject.toml",
            "MANIFEST.in",
            "README.md",
            "requirements.txt",
            "app/__init__.py",
            "app/appgen.json",
            "app/templates/my_index.html",
            "app_custom/extensions.py",
            "cookiecutter/cookiecutter.json",
            "cookiecutter/{{cookiecutter.project_slug}}/pyproject.toml",
            "cookiecutter/{{cookiecutter.project_slug}}/app/__init__.py",
        }
    )["ok"] is True
    assert set(generated_coverage.coverage_matrix()) == {"Author", "Book"}
    assert set(generated_coverage.workflow_coverage_matrix()) == {"Publish"}
    publish_coverage = generated_coverage.workflow_coverage_matrix()["Publish"]
    assert publish_coverage["automation"]["node_red"] == (
        "workflow.Publish.draft.published",
        "workflow.Publish.published.archived",
    )
    assert generated_coverage.coverage_summary()["ok"] is True
    assert generated_coverage.coverage_summary()["workflows"] == 1
    assert generated_coverage.uncovered_requirements() == {}
    assert generated_coverage.uncovered_workflow_requirements() == {}
    assert health.status()["tables"] == 2
    assert monitoring.liveness()["live"] is True
    assert monitoring.readiness()["ready"] is True
    assert monitoring.error_payload(ValueError("bad"), status_code=400)["status"] == 400
    assert resilience.classify_exception(ValueError("bad"))["category"] == "validation"
    assert resilience.safe_error_response(TimeoutError("slow"))["retryable"] is True
    assert "preserve_user_input" in resilience.safe_error_response(ValueError("bad"))["actions"]
    assert resilience.retry_policy("sync", attempt=1)["delay_seconds"] == 1
    assert resilience.circuit_breaker_state(5)["state"] == "open"
    assert resilience.incident_report(RuntimeError("boom"))["id"].startswith("inc-")
    assert resilience.exception_management_plan()["redact_internal_errors"] is True
    assert resilience.resilience_check({"app/resilience.py", "app/templates/appgen_resilience.html"})["ok"] is True
    assert performance.table_budget("Book")["route"] == "/api/v1/book/"
    assert performance.pagination_plan("Book", requested=999)["page_size"] == (
        performance.table_budget("Book")["page_size"] * 2
    )
    assert performance.cache_policy("Book")["cache_key"] == "appgen:book:list"
    assert performance.load_profile_plan(users=3, duration_seconds=5)["users"] == 3
    matrix = performance.load_test_matrix(users=3, duration_seconds=5)
    assert matrix["format"] == "appgen.load-test-matrix.v1"
    assert matrix["scenarios"][0]["executor"] == "constant-vus"
    k6_script = performance.k6_script(users=3, duration_seconds=5)
    assert "export const options" in k6_script
    assert "http.get" in k6_script
    locustfile = performance.locustfile_text()
    assert "class AppGenUser" in locustfile
    runbook = performance.load_test_runbook(users=3, duration_seconds=5)
    assert runbook["format"] == "appgen.load-test-runbook.v1"
    assert "k6 run performance.k6.js" in runbook["commands"][0]
    assert performance.slo_report({"p95_ms": 200, "error_rate": 0})["ok"] is True
    scale_plan = performance.autoscale_plan(
        {"cpu_percent": 90, "queue_depth": 150, "p95_ms": 700},
        current_replicas=2,
    )
    assert scale_plan["desired_replicas"] == 3
    assert "cpu" in scale_plan["reasons"]
    assert performance.performance_check(
        {"app/performance.py", "app/templates/appgen_performance.html"}
    )["ok"] is True
    runtime_assurance = _load_module(output_dir / "runtime_assurance.py", "generated_runtime_assurance")
    assurance_report = runtime_assurance.runtime_assurance_report({"p95_ms": 200, "error_rate": 0})
    assert assurance_report["format"] == "appgen.runtime-assurance.v1"
    assert assurance_report["ok"] is True
    assert "performance" in {area["id"] for area in assurance_report["areas"]}
    assert runtime_assurance.runtime_assurance_report({"p95_ms": 999})["ok"] is False
    assert runtime_assurance.runtime_assurance_check(
        {
            "app/runtime_assurance.py",
            "app/templates/appgen_runtime_assurance.html",
            "app/runtime_security.py",
            "app/security.py",
            "app/monitoring.py",
            "app/health.py",
            "app/resilience.py",
            "app/templates/appgen_resilience.html",
            "app/performance.py",
            "app/templates/appgen_performance.html",
            "app/backup.py",
            "app/templates/appgen_backup.html",
            "app/branding.py",
            "app/static/appgen-theme.css",
            "app/templates/appgen_branding.html",
            "scripts/appgen_quality.py",
            "tests/test_generated_contract.py",
        }
    )["ok"] is True
    release_gate = runtime_assurance.application_release_gate(
        {"p95_ms": 200, "error_rate": 0},
        runtime_assurance.REQUIRED_RELEASE_ARTIFACTS,
    )
    assert release_gate["format"] == "appgen.application-release-gate.v1"
    assert release_gate["ok"] is True
    assert release_gate["decision"] == "approved"
    assert {"security", "operations", "experience", "delivery"} == {area["id"] for area in release_gate["areas"]}
    assert runtime_assurance.application_release_gate(
        {"visual_quality": False},
        runtime_assurance.REQUIRED_RELEASE_ARTIFACTS,
    )["decision"] == "blocked"
    assert runtime_assurance.application_release_gate(
        existing_paths={"app/runtime_assurance.py"}
    )["ok"] is False
    assert reports.visible_columns("Book") == ("id", "title", "status", "summary", "cover_image", "manuscript_file", "author")
    assert "title,status" in reports.rows_to_csv(("title", "status"), [{"title": "Dune", "status": "draft"}])
    assert reports.join_report_catalog()
    first_join = reports.join_report_catalog()[0]
    assert reports.report_query_plan(first_join["key"])["requires_join"] is True
    assert report_delivery.delivery_plan("Book", channels=("download", "email"), formats=("csv", "pdf"))["ok"] is True
    assert report_delivery.rows_to_html("Book", [{"title": "Dune", "status": "draft"}]).startswith("<!doctype html>")
    assert report_delivery.rows_to_pdf_bytes("Book", [{"title": "Dune", "status": "draft"}]).startswith(b"%PDF")
    email_report = report_delivery.email_report_payload(
        "Book",
        [{"title": "Dune", "status": "draft"}],
        recipients=("ada@example.test",),
    )
    assert email_report["channel"] == "email"
    assert email_report["attachments"][0]["content_type"] == "application/pdf"
    dashboard_catalog = dashboards.dashboard_catalog()
    assert any(item["table"] == "Book" for item in dashboard_catalog)
    book_dashboard = dashboards.dashboard_spec("Book")
    assert book_dashboard["charts"][0]["metric"] == "count"
    assert any(chart["metric"] == "count_by" and chart["field"] == "title" for chart in book_dashboard["charts"])
    count_chart = dashboards.chart_spec("BookRecordCount")
    assert dashboards.chart_data(count_chart, [{"title": "Dune"}, {"title": "Dune Messiah"}])["values"] == (2,)
    bar_chart = next(chart for chart in book_dashboard["charts"] if chart["metric"] == "count_by")
    bar_data = dashboards.chart_data(bar_chart, [{"title": "Dune"}, {"title": "Dune"}, {"title": "Foundation"}])
    assert bar_data["labels"] == ("Dune", "Foundation")
    assert bar_data["values"] == (2, 1)
    bar_dataset = dashboards.chart_dataset(bar_chart, [{"title": "Dune"}, {"title": "Dune"}, {"title": "Foundation"}])
    assert bar_dataset == ({"label": "Dune", "value": 2}, {"label": "Foundation", "value": 1})
    assert dashboards.vega_lite_spec(bar_chart)["$schema"].endswith("/vega-lite/v5.json")
    assert dashboards.chart_render_contract(bar_chart, [{"title": "Dune"}])["vega_lite"]["mark"] == "bar"
    assert "highest Dune at 1" in dashboards.chart_accessibility_summary(bar_chart, [{"title": "Dune"}])
    dashboard_payload = dashboards.dashboard_payload("Book", [{"title": "Dune"}])
    assert dashboard_payload["charts"][0]["data"]["values"] == (1,)
    assert dashboard_payload["charts"][0]["render"]["dataset"] == ({"label": "records", "value": 1},)
    assert dashboards.dashboard_workbench("Book", [{"title": "Dune"}])["renderer_targets"] == (
        "web:vega-lite",
        "mobile:native-chart",
        "desktop:native-chart",
    )
    usage_events = (
        usage_analytics.usage_event("Book", "viewed", actor="ada", occurred_at="2026-01-01T10:00:00Z"),
        usage_analytics.usage_event("Book", "created", actor="ada", occurred_at="2026-01-01T10:01:00Z"),
        usage_analytics.usage_event("Author", "viewed", actor="grace", occurred_at="2026-01-02T10:00:00Z"),
    )
    assert usage_analytics.activity_summary(usage_events)["active_users"] == 2
    assert usage_analytics.adoption_report(usage_events)["active_resources"] == 2
    assert usage_analytics.funnel_report("Book", usage_events)["steps"][0]["count"] == 1
    assert usage_analytics.retention_report(usage_events)["latest_active_users"] == 1
    assert usage_analytics.realtime_usage_snapshot(usage_events, limit=2)["summary"]["events"] == 3
    assert usage_analytics.usage_dashboard(usage_events)["summary"]["events"] == 3
    sample_usage = usage_analytics.sample_usage_events()
    assert len(sample_usage) == len(usage_analytics.USAGE_RESOURCES) * 2
    usage_gate = usage_analytics.usage_analytics_release_gate(
        {"app/usage_analytics.py", "app/templates/appgen_usage_analytics.html"},
        sample_usage,
    )
    assert usage_gate["format"] == "appgen.usage-analytics-release-gate.v1"
    assert usage_gate["ok"] is True
    assert {"event_catalog", "activity_summary", "adoption", "funnels", "retention", "realtime"} <= {
        gate["gate"] for gate in usage_gate["gates"]
    }
    assert usage_analytics.usage_analytics_release_gate({"app/usage_analytics.py"}, sample_usage)["ok"] is False
    assert usage_analytics.usage_analytics_check(
        {"app/usage_analytics.py", "app/templates/appgen_usage_analytics.html"}
    )["ok"] is True
    search_catalog = search.search_catalog()
    assert any(item["table"] == "Book" and item["fields"] == ("title",) for item in search_catalog)
    assert search.search_index("Author")["fields"] == ("name",)
    assert search.provider_plan("elasticsearch", {})["missing"] == ("ELASTICSEARCH_URL",)
    assert search.provider_plan("whoosh", {"WHOOSH_INDEX_DIR": "/tmp/index"})["configured"] is True
    assert search.elasticsearch_mapping("Book")["mappings"]["properties"]["title"]["type"] == "text"
    assert search.whoosh_schema("Book")["fields"][1]["name"] == "title"
    assert search.provider_index_plan("elasticsearch", "Book")["mapping"]["index"] == "book-search"
    assert search.provider_index_plan("whoosh", "Book")["schema"]["index_dir"] == "whoosh/book"
    reindex = search.reindex_plan("elasticsearch", ("Book",))
    assert reindex["requires_review"] is True
    assert reindex["indexes"][0]["bulk_endpoint"] == "/_bulk"
    assert search.row_matches("Book", {"id": 1, "title": "Dune", "internal_code": "B-1"}, "dune") is True
    assert search.search_document("Book", {"id": 1, "title": "Dune", "internal_code": "B-1"})["fields"] == {
        "title": "Dune"
    }
    search_results = search.search_rows(
        "Book",
        [{"id": 1, "title": "Dune"}, {"id": 2, "title": "Foundation"}],
        "dune",
    )
    assert search_results[0]["id"] == 1
    assert search.search_payload({"Book": [{"id": 1, "title": "Dune"}]}, "dune")["results"][1]["matches"][0]["id"] == 1
    media_catalog = media.media_catalog()
    assert any(item["table"] == "Book" and item["field"] == "cover_image" and item["kind"] == "image" for item in media_catalog)
    assert any(item["table"] == "Book" and item["field"] == "manuscript_file" and item["kind"] == "file" for item in media_catalog)
    assert media.media_field("Book", "cover_image")["allowed_extensions"][0] == ".jpg"
    assert media.preview_contract("Book", "cover_image")["preview"] == "thumbnail"
    assert media.preview_contract("Book", "manuscript_file")["preview"] == "filename"
    assert media.sanitize_filename("../Cover Draft.png") == "Cover_Draft.png"
    assert media.storage_plan("Book", "cover_image", filename="../Cover Draft.png")["path"].endswith("Cover_Draft.png")
    assert media.validate_upload(
        "Book",
        "cover_image",
        filename="cover.png",
        content_type="image/png",
        size=1024,
    )["ok"] is True
    assert media.validate_upload(
        "Book",
        "cover_image",
        filename="cover.exe",
        content_type="application/octet-stream",
        size=99 * 1024 * 1024,
    )["errors"] == ("extension", "content_type", "size")
    document_catalog = documents.document_catalog()
    assert any(item["id"] == "book.manuscript_file" and item["approval_required"] for item in document_catalog)
    version = documents.document_version(
        "book.manuscript_file",
        record_id=1,
        filename="manuscript.pdf",
        author="ada",
    )
    assert version["library"] == "book_documents"
    assert version["version"] == 1
    assert documents.approval_workflow("book.manuscript_file")["steps"][1]["target"] == "approved"
    assert documents.retention_policy("book.manuscript_file")["retention_days"] == 2555
    esign = documents.esignature_payload("book.manuscript_file", signer="ada@example.test", record_id=1)
    assert esign["signer"] == "ada@example.test"
    audit = documents.document_audit_event("book.manuscript_file", "approved", actor="grace", record_id=1)
    assert audit["action"] == "approved"
    assert documents.document_management_check({"app/documents.py", "app/templates/appgen_documents.html"})["ok"] is True
    inventory_catalog = inventory_ops.inventory_catalog()
    assert any(item["table"] == "Book" and "title" in item["identifiers"] for item in inventory_catalog)
    barcode = inventory_ops.barcode_label("Book", {"title": "Dune"})
    assert barcode["value"] == "Book:Dune"
    assert inventory_ops.rfid_tag_payload("Book", {"title": "Dune"})["epc"].startswith("urn:epc:id:sgtin:")
    scan_event = inventory_ops.scan_event("Book", "Dune", mode="barcode", device_id="scanner-1")
    assert scan_event["candidate_fields"] == ("title",)
    movement = inventory_ops.stock_movement("Book", sku="Dune", quantity=2, from_location="A", to_location="B")
    assert movement["quantity"] == 2.0
    assert inventory_ops.cycle_count_plan("Book")[0]["scan_modes"] == ("barcode", "qr", "rfid")
    assert inventory_ops.reconcile_count("Book", expected=2, counted=3)["requires_review"] is True
    assert inventory_ops.traceability_chain("Book", ("Dune", "copy-1"))["events"][1]["identifier"] == "copy-1"
    assert inventory_ops.inventory_ops_check({"app/inventory_ops.py", "app/templates/appgen_inventory_ops.html"})["ok"] is True
    assert finance_ops.tax_calculation(100, category="standard")["tax_amount"] == 16.0
    assert finance_ops.tax_calculation(116, inclusive=True)["taxable_amount"] == 100.0
    assert finance_ops.exchange_rate_plan("USD", "KES")["rate"] == 129.0
    assert finance_ops.convert_amount(2, base="USD", target="KES")["converted"] == 258.0
    first_finance_table = finance_ops.finance_catalog()[0]["table"]
    assert finance_ops.budget_forecast(first_finance_table, (100, 200), periods=2, growth_rate=0.1)["forecast"] == (
        165.0,
        181.5,
    )
    revenue = finance_ops.revenue_recognition_schedule(120, periods=3)
    assert revenue["schedule"][0]["amount"] == 40.0
    batch = finance_ops.batch_process(first_finance_table, ({"title": "Dune"},), action="post", actor="ada")
    assert batch["row_count"] == 1
    assert finance_ops.finance_ops_check({"app/finance_ops.py", "app/templates/appgen_finance_ops.html"})["ok"] is True
    first_manufacturing_table = manufacturing_ops.manufacturing_catalog()[0]["table"]
    bom = manufacturing_ops.bill_of_material_plan(
        first_manufacturing_table,
        "FG-1",
        ({"component": "COMP-1", "quantity_per": 2},),
    )
    requirements = manufacturing_ops.material_requirements(3, bom["components"], on_hand={"COMP-1": 1})
    assert requirements[0]["net_required"] == 5.0
    assert manufacturing_ops.capacity_plan(({"work_order": "WO-1", "standard_hours": 4},), available_hours=8)[
        "overloaded"
    ] is False
    schedule = manufacturing_ops.production_schedule(
        ({"work_order": "WO-1", "standard_hours": 4},),
        capacity_hours_per_period=8,
    )
    assert schedule[0]["period"] == 1
    assert manufacturing_ops.purchase_requisition_plan(requirements)["line_count"] == 1
    assert manufacturing_ops.kanban_signal("COMP-1", on_hand=1, reorder_point=2, lot_size=10)["quantity"] == 10.0
    assert manufacturing_ops.manufacturing_ops_check(
        {"app/manufacturing_ops.py", "app/templates/appgen_manufacturing_ops.html"}
    )["ok"] is True
    access_book = data_access.resource_contract("Book")
    assert "title" in access_book["readable_fields"]
    assert "title" in access_book["writable_fields"]
    assert "internal_code" not in access_book["readable_fields"]
    assert "internal_code" not in access_book["writable_fields"]
    query_spec = data_access.normalize_query(
        "Book",
        filters={"title": {"contains": "dun"}},
        sort="-title",
        limit=999,
        fields=("title",),
    )
    assert query_spec["limit"] == 500
    assert query_spec["direction"] == "desc"
    query_result = data_access.query_rows(
        "Book",
        [{"id": 1, "title": "Dune", "status": "draft"}, {"id": 2, "title": "Foundation"}],
        filters={"title": {"contains": "dun"}},
        fields=("title",),
    )
    assert query_result["total"] == 1
    assert query_result["rows"] == ({"title": "Dune"},)
    saved = data_access.saved_query(
        "Book",
        "Published Books",
        filters={"title": {"contains": "dun"}},
        fields=("title",),
        actor="ada",
    )
    assert saved["key"] == "Book:published_books"
    export = data_access.query_export(saved)
    assert ("fields", "title") in export["url_params"]
    assert export["automation_payload"]["filters"] == {"title": {"contains": "dun"}}
    assert data_access.sanitize_write_payload("Book", {"title": "Dune"})["ok"] is True
    blocked_payload = data_access.sanitize_write_payload("Book", {"title": "Dune", "internal_code": "B-1"})
    assert blocked_payload["ok"] is False
    assert blocked_payload["unknown_fields"] == ("internal_code",)
    update_plan = data_access.mutation_plan("Book", "update", {"id": 1, "title": "Dune Messiah"}, actor="ada")
    assert update_plan["ok"] is True
    assert update_plan["identity"] == {"id": 1}
    bulk_plan = data_access.bulk_mutation_plan(
        "Book",
        "update",
        ({"id": 1, "title": "Dune"}, {"id": 2, "title": "Foundation"}),
        actor="ada",
    )
    assert bulk_plan["count"] == 2
    assert bulk_plan["review_required"] is True
    audit_event = data_access.mutation_audit_event(update_plan, request_id="req-1")
    assert audit_event["event"] == "data_access.Book.update"
    assert audit_event["payload_fields"] == ("title",)
    workbench = data_access.data_access_workbench("Book")
    assert workbench["query_builder"]["operators"] == ("eq", "contains", "startswith", "in", "gte", "lte")
    assert workbench["mutations"]["bulk_supported"] is True
    delete_plan = data_access.mutation_plan("Book", "delete", {"id": 1})
    assert delete_plan["review_required"] is True
    assert data_access.data_access_check({"app/data_access.py", "app/templates/appgen_data_access.html"})["ok"] is True
    exchange_contract = data_exchange.table_contract("Book")
    assert exchange_contract["fields"] == (
        "title",
        "status",
        "summary",
        "cover_image",
        "manuscript_file",
        "author",
    )
    assert exchange_contract["hidden_fields"] == ("internal_code",)
    assert data_exchange.csv_template("Book").startswith("title,status,summary")
    csv_rows = data_exchange.rows_from_csv("Book", "title,status\nDune,draft\n")
    assert csv_rows == ({"title": "Dune", "status": "draft"},)
    assert data_exchange.import_plan("Book", "title,status\nDune,draft\n")["ready"] is True
    assert data_exchange.import_plan("Book", "status\ndraft\n")["errors"][0]["missing"] == ("title",)
    migration_batch = data_exchange.migration_batch_plan(
        "Book",
        "title,status\nDune,draft\n,published\nMessiah,published\n",
        batch_size=1,
    )
    assert migration_batch["format"] == "appgen.migration-batch.v1"
    assert migration_batch["accepted_count"] == 2
    assert migration_batch["rejected_count"] == 1
    assert migration_batch["requires_review"] is True
    assert [batch["row_count"] for batch in migration_batch["batches"]] == [1, 1]
    assert data_exchange.migration_batch_summary(migration_batch)["batch_count"] == 2
    response_body, response_status = data_exchange.migration_batch_request_plan(
        "Book",
        {"content": "title,status\nDune,draft\n", "batch_size": 10},
    )
    assert response_status == 200
    assert response_body["accepted_count"] == 1
    invalid_body, invalid_status = data_exchange.migration_batch_request_plan("Book", {"batch_size": "bad"})
    assert invalid_status == 400
    assert invalid_body["error"] == "invalid_migration_batch_request"
    missing_body, missing_status = data_exchange.migration_batch_request_plan("Missing", {})
    assert missing_status == 404
    assert missing_body["error"] == "unknown_table"
    assert "migration_batch_json" in (output_dir / "data_exchange.py").read_text()
    assert "migration_batch_request_plan" in (output_dir / "data_exchange.py").read_text()
    assert "request.get_json" in (output_dir / "data_exchange.py").read_text()
    json_exchange = data_exchange.rows_to_json("Book", [{"title": "Dune", "internal_code": "B-1"}])
    assert "internal_code" not in json_exchange
    assert data_exchange.rows_from_json("Book", json_exchange)[0]["title"] == "Dune"
    assert data_exchange.exchange_check(
        {"app/data_exchange.py", "app/templates/appgen_data_exchange.html"}
    )["ok"] is True
    assert {item["provider"] for item in database_ops.database_provider_catalog()} == {
        "postgresql",
        "mysql",
        "sqlite",
        "mongodb",
        "dynamodb",
        "cassandra",
        "redis",
    }
    assert {item["provider"] for item in database_ops.relational_provider_catalog()} == {
        "postgresql",
        "mysql",
        "sqlite",
    }
    assert {item["provider"] for item in database_ops.nosql_provider_catalog()} == {
        "mongodb",
        "dynamodb",
        "cassandra",
        "redis",
    }
    assert {item["addon"] for item in database_ops.database_addon_catalog()} == {
        "patroni",
        "postgraphile",
        "zombodb",
        "elasticsearch",
    }
    assert database_ops.compose_service_plan("postgresql")["image"] == "postgres:16"
    assert database_ops.compose_service_plan("mysql")["image"] == "mysql:8"
    assert database_ops.compose_service_plan("mongodb")["image"] == "mongo:7"
    assert database_ops.nosql_provider_plan("mongodb", {"MONGODB_URI": "mongodb://db", "MONGODB_DATABASE": "app"})[
        "configured"
    ] is True
    assert database_ops.kubernetes_statefulset_plan("postgresql")["kind"] == "StatefulSet"
    assert database_ops.kubernetes_statefulset_plan("mongodb")["kind"] == "StatefulSet"
    assert {item["provider"] for item in database_ops.migration_target_matrix()} == {
        "postgresql",
        "mysql",
        "sqlite",
        "mongodb",
        "dynamodb",
        "cassandra",
        "redis",
    }
    assert {item["provider"] for item in database_ops.migration_target_matrix() if item["alembic"] is False} == {
        "mongodb",
        "dynamodb",
        "cassandra",
        "redis",
    }
    inventory = {item["table"]: item for item in database_ops.schema_inventory()}
    assert inventory["Book"]["required_fields"] == ("title",)
    assert inventory["Book"]["references"][0]["target_table"] == "Author"
    profile = database_ops.migration_source_profile(
        {"provider": "postgresql", "tables": ("Author",), "row_counts": {"Author": 2}}
    )
    assert profile["missing_tables"] == ("Book",)
    risk = database_ops.migration_risk_assessment(
        {"provider": "postgresql", "tables": ("Author",), "row_counts": {"Author": 2}}
    )
    assert risk["format"] == "appgen.database-migration-risk.v1"
    assert risk["risk_level"] == "high"
    assert any(item["kind"] == "missing_tables" for item in risk["risks"])
    cutover = database_ops.migration_cutover_plan({"provider": "postgresql", "tables": ("Author",)}, "postgresql")
    assert cutover["format"] == "appgen.database-cutover-plan.v1"
    assert cutover["requires_review"] is True
    assert "remediate" in [step["name"] for step in cutover["steps"]]
    assert database_ops.document_projection("Book")["collection"] == "book"
    assert {item["table"] for item in database_ops.document_projection_matrix()} >= {"Book", "Author"}
    assert database_ops.database_ops_check(
        {
            "app/database_ops.py",
            "app/templates/appgen_database_ops.html",
            "docker-compose.yml",
            "deploy/k8s.yaml",
        }
    )["ok"] is True
    assert {item["kind"] for item in schema_import.schema_source_catalog()} == {
        "dbml",
        "sql",
        "ponyorm",
        "database",
    }
    assert schema_import.schema_source_profile()["counts"]["tables"] == 2
    assert schema_import.schema_source_profile()["fingerprint"] == manifest["source_profile"]["fingerprint"]
    generated_source_contract = schema_import.schema_source_contract()
    assert generated_source_contract["format"] == "appgen.schema-source-contract.v1"
    assert generated_source_contract["sqlalchemy_driver_urls"] is True
    assert "postgresql" in generated_source_contract["database_url_dialects"]
    normalization = schema_import.normalization_report()
    assert normalization["format"] == "appgen.schema-normalization.v1"
    assert normalization["canonical_contract"] == "AppSchema"
    assert normalization["source_contract"]["ok"] is True
    assert normalization["fingerprint"] == manifest["source_profile"]["fingerprint"]
    assert normalization["table_signatures"][0]["table"] == "Author"
    fidelity = schema_import.source_fidelity_report()
    assert fidelity["format"] == "appgen.schema-source-fidelity.v1"
    assert fidelity["fingerprint"] == manifest["source_profile"]["fingerprint"]
    assert fidelity["source_contract"]["ok"] is True
    assert "dsl" in fidelity["roundtrip_targets"]
    sql_validation = schema_import.source_validation_plan("sql")
    assert sql_validation["format"] == "appgen.schema-source-validation.v1"
    assert "preserve_composite_foreign_keys" in sql_validation["checks"]
    assert {item["source_kind"] for item in schema_import.all_source_validation_plans()} == {
        "dbml",
        "sql",
        "ponyorm",
        "database",
    }
    assert schema_import.import_command_plan("dbml", "schema.dbml")["command"] == "appgen --dbml schema.dbml --writedir app"
    assert schema_import.import_command_plan("ponyorm", "entities.py")["command"] == "appgen --pony entities.py --writedir app"
    assert schema_import.source_roundtrip_plan("sql")["to"] == "sql"
    diff = schema_import.schema_roundtrip_diff("dbml", current_manifest={"tables": ["Book", "LegacyBook"]})
    assert diff["format"] == "appgen.schema-roundtrip-diff.v1"
    assert diff["destructive"] is True
    assert {"op": "review_extra_table", "table": "LegacyBook", "destructive": True} in diff["operations"]
    assert len(schema_import.all_schema_roundtrip_diffs()) == 4
    apply_plan = schema_import.import_apply_plan("sql", "schema.sql")
    assert apply_plan["format"] == "appgen.schema-import-apply-plan.v1"
    assert apply_plan["requires_review"] is True
    assert apply_plan["diff"]["source_kind"] == "sql"
    assert "app/models.py" in apply_plan["writes"]
    assert len(schema_import.all_import_apply_plans()) == 4
    assert schema_import.schema_import_check(
        {"app/schema_import.py", "app/templates/appgen_schema_import.html", "app/appgen.json"}
    )["ok"] is True
    import_gate = schema_import.schema_import_release_gate(
        {"app/schema_import.py", "app/templates/appgen_schema_import.html", "app/appgen.json"}
    )
    assert import_gate["format"] == "appgen.schema-import-release-gate.v1"
    assert import_gate["ok"] is True
    assert import_gate["blocking_gaps"] == ()
    assert {item["source_kind"] for item in import_gate["sources"]} == {"dbml", "sql", "ponyorm", "database"}
    assert schema_import.schema_import_release_gate({"app/schema_import.py"})["ok"] is False
    assert backup.BACKUP_TABLES["Book"]["columns"] == [
        "id",
        "title",
        "status",
        "summary",
        "cover_image",
        "manuscript_file",
        "internal_code",
        "author",
    ]
    backup_json = backup.backup_json(
        {"Book": [{"id": 1, "title": "Dune", "status": "draft", "internal_code": "B-1", "author": 1}]}
    )
    assert '"format": "appgen.backup.v1"' in backup_json
    assert '"internal_code": "B-1"' in backup_json
    assert backup.restore_plan(backup_json)["Book"] == 1
    assert backup.load_backup_payload(backup_json)["format"] == "appgen.backup.v1"
    manifest_record = backup.backup_manifest(backup_json, created_at="2026-01-01T02:00:00+00:00", actor="ada")
    assert manifest_record["format"] == "appgen.backup.manifest.v1"
    assert manifest_record["tables"]["Book"] == 1
    assert backup.backup_integrity_check(backup_json, manifest_record)["ok"] is True
    tampered = backup.load_backup_payload(backup_json)
    tampered["tables"][1]["rows"][0]["title"] = "Changed"
    assert backup.backup_integrity_check(tampered, manifest_record)["ok"] is False
    schedule = backup.backup_schedule_plan("2026-01-01T03:00:00+00:00")
    assert schedule["job_id"] == "appgen.autobackup.daily"
    assert schedule["next_run"].startswith("2026-01-02T02:00:00")
    retention = backup.retention_plan((manifest_record,) * 30)
    assert retention["review_required"] is True
    runbook = backup.recovery_runbook(backup_json, manifest_record)
    assert runbook["review_required"] is True
    assert runbook["can_restore"] is True
    assert runbook["steps"][0] == "verify backup manifest and SHA-256 digest"
    dr_plan = backup.disaster_recovery_plan(backup_json, manifest_record)
    assert dr_plan["format"] == "appgen.disaster-recovery-plan.v1"
    assert dr_plan["ok"] is True
    assert dr_plan["operator_approval_required"] is True
    backup_gate = backup.backup_release_gate(
        {"app/backup.py", "app/templates/appgen_backup.html"},
        backup_json,
        manifest_record,
    )
    assert backup_gate["format"] == "appgen.backup-release-gate.v1"
    assert backup_gate["ok"] is True
    assert {"integrity_manifest", "autobackup_schedule", "recovery_runbook", "disaster_recovery"} <= {
        gate["gate"] for gate in backup_gate["gates"]
    }
    assert backup.backup_release_gate({"app/backup.py"}, backup_json, manifest_record)["ok"] is False
    bad_payload = {
        "format": "appgen.backup.v1",
        "tables": [{"table": "Book", "columns": ["id"], "rows": []}],
    }
    with pytest.raises(ValueError, match="Column mismatch"):
        backup.validate_backup_payload(bad_payload)
    assert seed.SEED_DATA["Book"][0]["title"] == "Sample Title"
    assert seed.SEED_DATA["Book"][0]["author_id"] == 1
    assert "internal_code" not in seed.SEED_DATA["Book"][0]
    seed_plan = seed.seed_plan()
    assert seed_plan["format"] == "appgen.seed-plan.v1"
    assert {"demo", "smoke", "load"} == {scenario["name"] for scenario in seed_plan["scenarios"]}
    assert seed.seed_insert_order().index("Author") < seed.seed_insert_order().index("Book")
    book_seed_plan = next(item for item in seed_plan["tables"] if item["table"] == "Book")
    assert book_seed_plan["dependencies"] == ("Author",)
    assert "author_id" in book_seed_plan["fields"]
    assert len(seed.table_seed_factory("Book", count=3)) == 3
    assert seed.table_seed_factory("Book", count=3)[2]["id"] == 3
    assert len(seed.scenario_seed_data("load")["Book"]) == 25
    fixture_export = seed.seed_fixture_export("smoke")
    assert fixture_export["format"] == "appgen.seed-fixture.v1"
    assert fixture_export["validation"]["ok"] is True
    assert "def appgen_seed_data" in fixture_export["pytest"]
    assert 'INSERT INTO "Author"' in fixture_export["sql"]
    assert seed.validate_seed_data()["ok"] is True
    assert seed.validate_seed_data({"Book": [{"status": "draft"}]})["errors"][0]["missing"] == ("title",)
    assert seed.anonymized_seed_data({"User": [{"email": "ada@example.test", "name": "Ada"}]})["User"][0]["email"] == "[redacted]"
    assert '"format": "appgen.seed.v1"' in seed.seed_json()
    seed_sql = seed.seed_sql()
    assert 'INSERT INTO "Author"' in seed_sql
    assert 'INSERT INTO "Book"' in seed_sql
    assert seed_sql.index('INSERT INTO "Author"') < seed_sql.index('INSERT INTO "Book"')
    catalog = integrations.integration_catalog({})
    assert {item["name"] for item in catalog} == {
        "rest",
        "webhook",
        "salesforce",
        "sap",
        "entando",
        "invenio",
        "stripe",
        "mpesa",
        "twilio_sms",
        "sendgrid_email",
    }
    assert {item["name"] for item in integrations.integrations_by_kind("payment", {})} == {"stripe", "mpesa"}
    assert integrations.integration_config("salesforce", {})["configured"] is False
    configured_env = {
        "APPGEN_REST_BASE_URL": "https://api.example.test",
        "APPGEN_REST_TOKEN": "token",
    }
    assert integrations.outbound_request_plan("rest", "sync", {"id": 1}, configured_env)["operation"] == "sync"
    webhook_env = {
        "APPGEN_WEBHOOK_URL": "https://hooks.example.test/appgen",
        "APPGEN_WEBHOOK_SECRET": "secret",
    }
    webhook_plan = integrations.signed_webhook_plan("Book.created", {"id": 1}, environ=webhook_env)
    assert webhook_plan["headers"]["X-AppGen-Event"] == "Book.created"
    assert webhook_plan["headers"]["Idempotency-Key"] == webhook_plan["idempotency_key"]
    assert integrations.validate_webhook_signature({"id": 1}, webhook_plan["signature"], "secret") is True
    assert integrations.integration_idempotency_key("webhook", "webhook.Book.created", {"id": 1}) == webhook_plan["idempotency_key"]
    outbox_entry = integrations.integration_outbox_entry(webhook_plan)
    assert outbox_entry["id"].startswith("outbox-")
    assert outbox_entry["status"] == "pending"
    assert integrations.delivery_audit_event(outbox_entry, status="queued")["event"] == "integration.delivery.queued"
    payment_env = {"STRIPE_API_KEY": "sk_test", "STRIPE_WEBHOOK_SECRET": "whsec"}
    payment_plan = integrations.payment_request_plan("stripe", amount=42, currency="usd", reference="INV-1", environ=payment_env)
    assert payment_plan["operation"] == "payment.authorize"
    assert payment_plan["payload"]["currency"] == "USD"
    assert payment_plan["side_effect"] == "external_payment"
    sms_env = {
        "TWILIO_ACCOUNT_SID": "sid",
        "TWILIO_AUTH_TOKEN": "token",
        "TWILIO_FROM_NUMBER": "+10000000000",
    }
    sms_plan = integrations.sms_request_plan("twilio_sms", to="+15551234567", body="Ready", environ=sms_env)
    assert sms_plan["operation"] == "sms.send"
    email_env = {"SENDGRID_API_KEY": "key", "APPGEN_EMAIL_FROM": "noreply@example.test"}
    email_plan = integrations.email_request_plan(
        "sendgrid_email",
        to=["ada@example.test"],
        subject="Ready",
        body="Your report is ready.",
        environ=email_env,
    )
    assert email_plan["payload"]["to"] == ("ada@example.test",)
    entando_env = {
        "ENTANDO_BASE_URL": "https://portal.example.test",
        "ENTANDO_CLIENT_ID": "client",
        "ENTANDO_CLIENT_SECRET": "secret",
    }
    portal_plan = integrations.low_code_portal_plan(
        microfrontend="book-list",
        route="/books",
        environ=entando_env,
    )
    entando_contract = integrations.integration_contract("entando")
    assert entando_contract["version"] == "appgen.integration.entando.v1"
    assert "microfrontend" in entando_contract["surfaces"]
    assert "portal.microfrontend.publish" in entando_contract["events"]
    assert portal_plan["operation"] == "portal.microfrontend.publish"
    assert portal_plan["contract"] == entando_contract["version"]
    assert portal_plan["side_effect"] == "external_portal_publish"
    invenio_env = {"INVENIO_BASE_URL": "https://repo.example.test", "INVENIO_ACCESS_TOKEN": "token"}
    deposit_plan = integrations.repository_deposit_plan(
        record={"title": "Dune"},
        files=("dune.pdf",),
        environ=invenio_env,
    )
    invenio_contract = integrations.integration_contract("invenio")
    assert invenio_contract["version"] == "appgen.integration.invenio.v1"
    assert "deposit" in invenio_contract["surfaces"]
    assert "repository.record.publish" in invenio_contract["events"]
    assert deposit_plan["operation"] == "repository.deposit.create"
    assert deposit_plan["contract"] == invenio_contract["version"]
    assert deposit_plan["payload"]["files"] == ("dune.pdf",)
    assert {item["integration"] for item in integrations.generated_integration_contracts()} == {"entando", "invenio"}
    assert integrations.integration_check({"app/integrations.py", "app/templates/appgen_integrations.html"})["ok"] is True
    productivity_providers = {item["provider"]: item for item in productivity.provider_catalog({})}
    assert set(productivity_providers) == {"microsoft365", "google_workspace"}
    assert productivity_providers["microsoft365"]["configured"] is False
    doc_payload = productivity.document_merge_payload("Book", {"title": "Dune"})
    assert doc_payload["target"] == "docs"
    assert doc_payload["fields"]["title"] == "Dune"
    sheet_payload = productivity.spreadsheet_export_payload("Book", ({"title": "Dune"},), provider="microsoft365")
    assert sheet_payload["target"] == "excel"
    assert sheet_payload["row_count"] == 1
    assert productivity.calendar_event_payload("Book")["target"] == "calendar"
    task_payload = productivity.task_sync_payload("Book", {"status": "draft"})
    assert "title" in task_payload["missing_required_fields"]
    assert productivity.productivity_check({"app/productivity.py", "app/templates/appgen_productivity.html"})["ok"] is True
    assert {item["name"] for item in lifecycle.environment_catalog()} == {
        "development",
        "testing",
        "staging",
        "production",
    }
    assert lifecycle.environment_status("production", {})["ready"] is False
    assert lifecycle.custom_domain_plan("production", "app.example.test")["domain"] == "app.example.test"
    assert lifecycle.release_checklist("production")["gates"]
    assert lifecycle.promotion_plan("staging")["target"] == "production"
    assert lifecycle.maintenance_window(duration_minutes=45)["duration_minutes"] == 45
    assert "deploy" in lifecycle.update_plan("1.2.3", migration_required=True)["steps"]
    assert lifecycle.feedback_item("Needs work", rating=2)["id"].startswith("fb-")
    assert lifecycle.user_test_session("Onboarding")["metrics"] == (
        "completion_rate",
        "time_on_task",
        "user_satisfaction",
    )
    assert lifecycle.issue_report("Broken form", severity="high")["status"] == "open"
    assert lifecycle.lifecycle_check({"app/lifecycle.py", "app/templates/appgen_lifecycle.html"})["ok"] is True
    assert tenancy.is_tenant_scoped("Book") is False
    assert tenancy.tenant_filter_kwargs("Book", "acme") == {}
    assert tenancy.tenant_context({"X-AppGen-Tenant": "acme"}, {}, {}) == {"tenant_id": "acme"}
    assert rls.table_policy("Book")["scoped"] is False
    assert rls.rls_filter_kwargs("Book", {"tenant_id": "acme"}) == {}
    assert rls.can_access_row("Book", {"title": "Dune"}, {}) is True
    assert rls.postgres_policy_sql("Book").startswith("-- Book is not tenant scoped")
    assert {item["name"] for item in identity.provider_catalog({})} == {
        "oidc",
        "saml",
        "ldap",
        "active_directory",
        "headers",
        "cognito",
    }
    assert identity.provider_config("oidc", {})["configured"] is False
    ldap_env = {
        "LDAP_URI": "ldaps://ldap.example.test",
        "LDAP_BIND_DN": "cn=app,dc=example,dc=test",
        "LDAP_BIND_PASSWORD": "secret",
        "LDAP_USER_BASE_DN": "ou=people,dc=example,dc=test",
    }
    ldap_plan = identity.ldap_bind_plan("ldap", "ada", environ=ldap_env)
    assert ldap_plan["server"] == "ldaps://ldap.example.test"
    assert ldap_plan["user_filter"] == "(&(objectClass=person)(uid=ada))"
    assert identity.directory_search_plan("ldap", "ada", environ=ldap_env)["filter"] == (
        "(|(cn=*ada*)(mail=*ada*)(uid=*ada*))"
    )
    ad_env = {
        "AD_SERVER": "ldaps://ad.example.test",
        "AD_DOMAIN": "example.test",
        "AD_BIND_USER": "svc-app",
        "AD_BIND_PASSWORD": "secret",
        "AD_USER_BASE_DN": "dc=example,dc=test",
    }
    ad_plan = identity.ldap_bind_plan("active_directory", "ada", environ=ad_env)
    assert ad_plan["bind_identity"] == "ada@example.test"
    assert "sAMAccountName=ada" in ad_plan["user_filter"]
    oidc_env = {
        "OIDC_ISSUER": "https://issuer.example.test",
        "OIDC_CLIENT_ID": "client",
        "OIDC_CLIENT_SECRET": "secret",
    }
    assert identity.login_request_plan("oidc", "/next", oidc_env)["next_url"] == "/next"
    cognito_env = {
        "COGNITO_REGION": "us-east-1",
        "COGNITO_USER_POOL_ID": "us-east-1_abc",
        "COGNITO_CLIENT_ID": "client",
        "COGNITO_CLIENT_SECRET": "secret",
        "COGNITO_DOMAIN": "https://auth.example.test",
    }
    assert identity.provider_config("cognito", cognito_env)["configured"] is True
    assert identity.cognito_issuer(cognito_env) == "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_abc"
    assert identity.cognito_jwks_url(cognito_env).endswith("/.well-known/jwks.json")
    assert identity.cognito_authorize_url("https://app.example.test/callback", cognito_env).startswith(
        "https://auth.example.test/oauth2/authorize"
    )
    oauth = identity.cognito_oauth_metadata(cognito_env)
    assert oauth["token_url"] == "https://auth.example.test/oauth2/token"
    assert oauth["client_secret_env"] == "COGNITO_CLIENT_SECRET"
    token_plan = identity.cognito_token_exchange_plan("auth-code", "https://app.example.test/callback", environ=cognito_env)
    assert token_plan["auth"] == "client_secret_basic"
    assert token_plan["body"]["grant_type"] == "authorization_code"
    assert identity.cognito_logout_url("https://app.example.test/logout", cognito_env).startswith(
        "https://auth.example.test/logout"
    )
    assert identity.cognito_group_role_mapping({"cognito:groups": ["appgen:Editor", "Admins"]}, prefix="appgen:") == (
        "Editor",
    )
    assert identity.cognito_readiness(cognito_env)["oauth"]["userinfo_url"].endswith("/oauth2/userInfo")
    identity_gate = identity.identity_release_gate(
        {"app/identity.py", "app/templates/appgen_identity.html"},
        identity.sample_identity_environment(),
    )
    assert identity_gate["format"] == "appgen.identity-release-gate.v1"
    assert identity_gate["ok"] is True
    assert {"provider_catalog", "provider_configuration", "directory_plans", "cognito_oauth", "token_exchange_review"} <= {
        gate["gate"] for gate in identity_gate["gates"]
    }
    assert identity.identity_release_gate({"app/identity.py"}, identity.sample_identity_environment())["ok"] is False
    principal = identity.normalize_principal({"sub": "u1", "email": "ada@example.test", "roles": ["Editor"]})
    assert principal["username"] == "ada@example.test"
    assert principal["roles"] == ("Editor",)
    ad_principal = identity.normalize_principal({"sAMAccountName": "ada", "mail": "ada@example.test", "groups": ["ERP"]})
    assert ad_principal["username"] == "ada"
    assert ad_principal["email"] == "ada@example.test"
    assert ad_principal["roles"] == ("ERP",)
    cognito_principal = identity.normalize_principal(
        {"sub": "u2", "email": "bo@example.test", "cognito:groups": ["Editor"]}
    )
    assert cognito_principal["roles"] == ("Editor",)
    assert compliance.protected_fields("Book") == ("internal_code",)
    assert compliance.redact_row("Book", {"title": "Dune", "internal_code": "B-1"})["internal_code"] == "[redacted]"
    audit = compliance.audit_event("read", "Book", actor="ada", tenant_id="acme")
    assert audit["action"] == "read"
    assert audit["tenant_id"] == "acme"
    assert compliance.retention_policy("Book")["retention_days"] == 365
    privacy = compliance.privacy_request("erase", "subject-1", tables=("Book",), actor="dpo")
    assert privacy["format"] == "appgen.privacy-request.v1"
    assert privacy["requires_review"] is True
    export = compliance.subject_export_package(
        "subject-1",
        {"Book": [{"id": 1, "title": "Dune", "internal_code": "B-1"}]},
        actor="dpo",
    )
    assert export["data"]["Book"][0]["internal_code"] == "[redacted]"
    erasure = compliance.erasure_plan("subject-1", {"Book": [{"id": 1}]}, actor="dpo")
    assert erasure["format"] == "appgen.erasure-plan.v1"
    assert erasure["actions"][0]["table"] == "Book"
    record = type("Record", (), {"id": 1, "age_days": 400})()
    disposition = compliance.retention_disposition_review("Book", [record])
    assert disposition["requires_review"] is True
    assert disposition["due"][0]["action"] == "archive_or_delete_review"
    compliance_gate = compliance.compliance_release_gate(
        {"app/compliance.py", "app/templates/appgen_compliance.html"},
        {"Book": [{"id": 1, "internal_code": "B-1", "age_days": 400}]},
    )
    assert compliance_gate["format"] == "appgen.compliance-release-gate.v1"
    assert compliance_gate["ok"] is True
    assert {"redaction", "privacy_requests", "erasure_review", "retention_disposition", "audit_events"} <= {
        gate["gate"] for gate in compliance_gate["gates"]
    }
    assert compliance.compliance_release_gate({"app/compliance.py"}, {"Book": [{"id": 1, "age_days": 400}]})[
        "ok"
    ] is False
    context = assistant.prompt_context("Book", {"title": "Dune", "internal_code": "B-1"})
    assert context["values"] == {"title": "Dune"}
    assert "internal_code" not in context["fields"]
    questions = assistant.chatbot_questions("Book")
    assert any(question["field"] == "title" and question["required"] for question in questions)
    intelligence_catalog = {item["table"]: item for item in intelligence.intelligence_catalog()}
    assert "Book" in intelligence_catalog
    book_features = intelligence.preprocess_row("Book", {"title": "Dune", "summary": "Good success"})
    assert book_features["title__tokens"] == 1
    anomaly = intelligence.anomaly_score("Book", {"title": ""})
    assert anomaly["anomalous"] is True
    assert intelligence.sentiment("good success")["label"] == "positive"
    assert "Ada Lovelace" in intelligence.extract_entities("Ada Lovelace approved the plan")
    assert intelligence.classify_text("invoice payment failed")["label"] == "finance"
    vision_providers = {item["provider"]: item for item in intelligence.vision_provider_catalog({})}
    assert set(vision_providers) == {"opencv", "tensorflow", "pytorch", "google_vision"}
    assert vision_providers["google_vision"]["configured"] is False
    assert any(
        item["table"] == "Book" and item["field"] == "cover_image" and item["kind"] == "image"
        for item in intelligence.media_intelligence_catalog()
    )
    assert intelligence.ocr_plan("Book", "cover_image", provider="opencv")["task"] == "ocr"
    object_plan = intelligence.object_detection_plan("Book", "cover_image", provider="google_vision", environ={})
    assert object_plan["review_required"] is True
    assert object_plan["missing"] == ("GOOGLE_APPLICATION_CREDENTIALS",)
    assert intelligence.classification_plan("Book", "cover_image", source="uploads/book/cover.png")["source"].endswith(
        "cover.png"
    )
    assert any(item["kind"] == "run_nlp_review" for item in intelligence.recommendation_plan("Book", {}))
    experiment_id = intelligence.experiment_catalog()[0]["id"]
    assert intelligence.assign_variant(experiment_id, "ada") in {"control", "compact", "guided"}
    assert intelligence.predictive_maintenance({"p95_ms": 900, "error_rate": 0.03})["healthy"] is False
    assert intelligence.intelligence_check({"app/intelligence.py", "app/templates/appgen_intelligence.html"})["ok"] is True
    chatbot_intents = {item["intent"]: item for item in chatbot.chatbot_catalog()}
    assert "create_book" in chatbot_intents
    book_chat = chatbot.start_conversation("create_book")
    assert book_chat["next_field"] == "title"
    answered_book_chat = chatbot.answer_conversation(book_chat, "Dune")
    assert answered_book_chat["ready"] is True
    assert answered_book_chat["values"]["title"] == "Dune"
    payload = chatbot.create_payload("create_book", answered_book_chat["values"])
    assert payload["table"] == "Book"
    assert payload["ready"] is True
    assert payload["payload"]["title"] == "Dune"
    assert chatbot.chatbot_check({"app/chatbot.py", "app/templates/appgen_chatbot.html"})["ok"] is True
    assert {item["provider"] for item in voice.voice_provider_catalog()} == {"alexa", "google_assistant", "web_speech"}
    first_voice_intent = voice.voice_intent_catalog()[0]["intent"]
    assert voice.utterance_training_phrases(first_voice_intent)
    assert voice.slot_schema(first_voice_intent)
    assert voice.match_utterance("please create book")["matched"] is True
    assert voice.slot_fill_plan(first_voice_intent, {})["ready"] in {True, False}
    assert voice.voice_response(first_voice_intent, {})["ssml"].startswith("<speak>")
    assert voice.alexa_interaction_model()["interactionModel"]["languageModel"]["intents"]
    assert voice.google_actions_model()["actions"]
    assert voice.voice_check({"app/voice.py", "app/templates/appgen_voice.html"})["ok"] is True
    assert i18n.translate("Book", locale="en") == "Book"
    assert i18n.translate("Book", locale="es") == "Book"
    assert i18n.negotiate_locale("fr-CA,fr;q=0.9,en;q=0.8") == "fr"
    missing_report = i18n.missing_translation_report(("en", "es"))
    assert missing_report["format"] == "appgen.i18n-missing.v1"
    assert "Book" in missing_report["missing"]["es"]
    assert i18n.translation_payload("es")["fallback_locale"] == "en"
    assert i18n.i18n_check(
        {"babel.cfg", "app/i18n.py", "app/templates/appgen_i18n.html", "app/translations/en/LC_MESSAGES/messages.po"}
    )["ok"] is True
    features = assistant.prediction_features("Book", {"title": "Dune", "internal_code": "B-1"})
    assert features == {"title": "Dune"}
    text_catalog = text_quality.text_quality_catalog()
    assert any(item["table"] == "Book" and item["field"] == "summary" for item in text_catalog)
    assert text_quality.character_count("hello world") == {"characters": 11, "words": 2}
    assert text_quality.repeated_words("This is is clear.") == ("is",)
    quality = text_quality.quality_report("Book", "summary", "bad  grammar grammar")
    assert quality["counts"]["characters"] == 20
    assert "double_space" in quality["warnings"]
    assert "capitalization" in quality["warnings"]
    assert "terminal_punctuation" in quality["warnings"]
    assert quality["repeated_words"] == ("grammar",)
    assert text_quality.form_text_quality("Book", {"summary": "Fine."})[0]["remaining"] == 1995
    suggestions = assistant.recommendations("Book", {"status": "draft"})
    assert any(item["type"] == "missing_required_field" and item["field"] == "title" for item in suggestions)
    review = assistant.review_task("Book", {"status": "draft"})
    assert review["table"] == "Book"
    assert review["recommendations"] == suggestions
    assert {item["channel"] for item in notifications.channel_catalog()} == {"in_app", "email", "webhook", "push"}
    event_catalog = notifications.event_catalog()
    assert any(item["table"] == "Book" and "Book.created" in item["events"] for item in event_catalog)
    payload = notifications.notification_payload(
        "email",
        "Book created",
        "A record was created",
        recipients=("ada@example.test",),
        event="Book.created",
    )
    assert payload["channel"] == "email"
    assert payload["recipients"] == ("ada@example.test",)
    queued = notifications.queue_event("Book", "created", {"title": "Dune"}, channels=("in_app", "webhook"))
    assert [item["channel"] for item in queued] == ["in_app", "webhook"]
    assert queued[0]["event"] == "Book.created"
    assert queued[0]["metadata"]["row"] == {"title": "Dune"}
    agent_providers = agents.provider_catalog({})
    assert {provider["mode"] for provider in agent_providers} == {"local", "api"}
    assert agents.agent_plan(agents.agent_catalog()[0]["name"], "inspect")["model"]
    provider_matrix = agents.provider_connection_matrix({"OPENAI_API_KEY": "test"})
    assert provider_matrix["format"] == "appgen.agent-provider-matrix.v1"
    assert provider_matrix["ok"] is True
    assert {"local", "api"} <= set(provider_matrix["modes"])
    tool_policy = agents.agent_tool_policy("Publisher")
    assert tool_policy["format"] == "appgen.agent-tool-policy.v1"
    assert tool_policy["ok"] is True
    execution_matrix = agents.agent_execution_matrix(environ={"OPENAI_API_KEY": "test"})
    assert execution_matrix["format"] == "appgen.agent-execution-matrix.v1"
    assert execution_matrix["ok"] is True
    agent_gate = agents.agentic_release_gate(
        {"app/agents.py", "app/templates/appgen_agents.html"},
        environ={"OPENAI_API_KEY": "test"},
    )
    assert agent_gate["format"] == "appgen.agentic-release-gate.v1"
    assert agent_gate["ok"] is True
    assert {"provider_modes", "provider_secret_policy", "agent_provider_links", "tool_policy"} <= {
        gate["gate"] for gate in agent_gate["gates"]
    }
    assert agents.agentic_release_gate({"app/agents.py"}, environ={"OPENAI_API_KEY": "test"})["ok"] is False
    assert {item["target"] for item in platforms.platform_catalog()} == {"web", "pwa", "mobile", "desktop", "chatbot"}
    mobile_contract = platforms.platform_contract("mobile")
    assert "camera" in mobile_contract["capabilities"]
    assert {"web", "mobile", "desktop"} == set(platforms.generation_matrix())
    package_matrix = platforms.target_package_matrix()
    assert package_matrix["format"] == "appgen.target-package-matrix.v1"
    assert package_matrix["ok"] is True
    assert {"web", "mobile", "desktop"} <= {row["target"] for row in package_matrix["rows"]}
    platform_gate = platforms.platform_release_gate(
        {
            "app/",
            "frontends/react",
            "frontends/vue",
            "frontends/angular",
            "frontends/svelte",
            "frontends/htmx",
            "frontends/express",
            "app/static/appgen.webmanifest",
            "app/static/appgen-sw.js",
            "app/static/appgen-offline.html",
            "native/mobile/app.py",
            "native/mobile/pyproject.toml",
            "native/desktop/app.py",
            "native/desktop/pyproject.toml",
        }
    )
    assert platform_gate["format"] == "appgen.platform-release-gate.v1"
    assert platform_gate["ok"] is True
    assert {"target_selection", "package_matrix", "web_contract", "mobile_contract", "desktop_contract"} <= {
        gate["gate"] for gate in platform_gate["gates"]
    }
    assert platforms.platform_release_gate({"app/"})["ok"] is False
    assert mobile_contract["tables"][1]["table"] == "Book"
    assert "internal_code" not in mobile_contract["tables"][1]["fields"]
    assert platforms.mobile_capabilities()["location"] is True
    assert "api-gateway" in microservices.service_names()
    assert microservices.service_for_table("Book")["name"] == "book-service"
    assert any(route["path"] == "/api/v1/book/" and route["service"] == "book-service" for route in microservices.api_gateway_routes())
    assert any(route["topic"] == "Book.created" and route["service"] == "book-service" for route in microservices.event_routes())
    assert "workflow-service" in microservices.dependency_graph()["book-service"]
    assert microservices.deployment_units()[0]["name"] == "api-gateway"
    assert microservices.health_check_plan()[0]["liveness"].endswith("/live")
    assert microservices.scaling_policy("book-service", cpu_percent=90)["desired_replicas"] == 3
    relationships = microservices.cross_service_relationships()
    assert relationships[0]["source_table"] == "Book"
    assert relationships[0]["source_column"] == "author_id"
    assert relationships[0]["target_table"] == "Author"
    assert relationships[0]["cross_service"] is True
    resolver = microservices.relationship_resolver_plan("Book", "author_id", 1)
    assert resolver["format"] == "appgen.cross-service-relationship-resolver.v1"
    assert resolver["request"]["upstream"].endswith("/api/v1/author/1")
    consistency = microservices.relationship_consistency_plan()
    assert consistency[0]["requires_review"] is True
    event_contracts = microservices.relationship_event_contracts()
    assert event_contracts[0]["publisher"] == "author-service"
    check = microservices.microservice_check(
        {"app/microservices.py", "app/templates/appgen_microservices.html", "deploy/k8s.yaml"}
    )
    assert check["ok"] is True
    assert check["cross_service_relationships"]
    intents = platforms.chatbot_intents()
    assert any(intent["intent"] == "create_book" for intent in intents)
    assert set(sdks.sdk_targets()) == {"python", "javascript", "java", "csharp"}
    assert sdks.sdk_plan("python")["path"] == "sdks/python/client.py"
    assert sdks.client_method_names("Book")["create"] == "create_book"
    assert sdks.scaffold_check(
        {
            "sdks/appgen_sdks.py",
            "sdks/python/client.py",
            "sdks/javascript/client.js",
            "sdks/java/AppGenClient.java",
            "sdks/csharp/AppGenClient.cs",
        }
    )["ok"] is True
    collaboration_catalog = collaboration.collaboration_catalog()
    assert any(item["table"] == "Book" and "Book.proposal.created" in item["events"] for item in collaboration_catalog)
    realtime_topics = realtime.realtime_topics()
    assert any(item["table"] == "Book" and "Book.message" in item["topics"] for item in realtime_topics)
    event = realtime.event_payload("Book.updated", {"title": "Dune"}, actor="ada", event_id="evt-1")
    assert realtime.sse_frame(event).startswith("id: evt-1\nevent: Book_updated\n")
    assert realtime.collaboration_message("Book", "ada", "Ready")["body"] == "Ready"
    assert "Book.updated" in realtime.replay_plan(limit=10)["topics"]
    event_catalog = events.event_catalog()
    assert any("Book.created" in item["topics"] for item in event_catalog["tables"])
    workflow_topic = "workflow.Publish.draft.published"
    assert workflow_topic in events.all_topics()
    table_event = events.normalize_event("Book.created", {"title": "Dune"}, actor="ada", tenant_id="acme")
    assert events.match_event_rules(table_event) == ("audit", "notify", "realtime")
    plan = events.process_event(table_event)
    assert plan["audit"] is True
    assert plan["notify"] is True
    failed_event = events.normalize_event("Book.failed", {"title": "Dune"}, severity="error")
    failed_plan = events.process_event(failed_event)
    assert failed_plan["dead_letter"] is True
    assert failed_plan["alert"]["severity"] == "error"
    assert events.retry_plan(table_event, attempt=1)["delay_seconds"] == 5
    assert events.dead_letter_event(table_event, "boom")["error"] == "boom"
    assert events.cep_check({"app/events.py", "app/templates/appgen_events.html"})["ok"] is True
    rpa_tasks = {task["id"]: task for task in rpa.rpa_task_catalog()}
    assert "book.create_record" in rpa_tasks
    book_task_plan = rpa.task_plan("book.create_record", {"title": "Dune"})
    assert book_task_plan["surface"] == "browser"
    assert book_task_plan["actions"][1]["values"]["title"] == "Dune"
    assert rpa.credential_readiness({})["missing"] == ("APPGEN_API_TOKEN", "APPGEN_BROWSER_SESSION")
    assert rpa.automation_audit_event("book.create_record", actor="ada")["task_id"] == "book.create_record"
    process_model = rpa.process_model("book.create_record")
    assert process_model["flows"][0]["source"] == "start"
    assert process_model["flows"][-1]["target"] == "end"
    assert "<bpmn:process" in rpa.bpmn_xml("book.create_record")
    assert rpa.uml_activity("book.create_record").startswith("@startuml")
    assert rpa.validate_process_model("book.create_record")["ok"] is True
    simulation = rpa.simulate_process("book.create_record", runs=3, base_duration_seconds=10)
    assert simulation["runs"] == 3
    assert simulation["valid"] is True
    assert simulation["bottlenecks"]
    platforms = {item["platform"]: item for item in rpa.rpa_platform_catalog({})}
    assert set(platforms) == {"uipath", "blue_prism", "automation_anywhere"}
    assert platforms["uipath"]["ready"] is False
    platform_plan = rpa.rpa_platform_plan("uipath", "book.create_record")
    assert platform_plan["artifact"] == "process-package"
    assert platform_plan["task_id"] == "book.create_record"
    export_package = rpa.rpa_export_package("blue_prism", "book.create_record")
    assert export_package["artifact"] == "release-package"
    assert "<bpmn:process" in export_package["bpmn"]
    queue_payload = rpa.rpa_queue_payload("automation_anywhere", "book.create_record", {"title": "Dune"})
    assert queue_payload["work_item_queue"] == "appgen_book_create_record"
    assert queue_payload["inputs"]["title"] == "Dune"
    slow_observation = rpa.process_observation("book.create_record", duration_seconds=45, success=False, errors=1)
    assert rpa.process_summary((slow_observation,))["bottlenecks"] == ("book.create_record",)
    assert rpa.rpa_check({"app/rpa.py", "app/templates/appgen_rpa.html"})["platforms"] == (
        "uipath",
        "blue_prism",
        "automation_anywhere",
    )
    assert rpa.rpa_check({"app/rpa.py", "app/templates/appgen_rpa.html"})["ok"] is True
    proposal = collaboration.change_proposal(
        "Book",
        {"title": "Dune"},
        {"title": "Dune Messiah"},
        author="ada",
        message="Rename sample",
    )
    assert proposal["changed_fields"] == ("title",)
    decision = collaboration.review_decision(proposal, "grace", "approved", comment="ship it")
    assert decision["decision"] == "approved"
    assert collaboration.merge_plan(proposal, decision)["applied"] is True
    rejected = collaboration.review_decision(proposal, "grace", "changes_requested")
    assert collaboration.merge_plan(proposal, rejected)["applied"] is False
    conflict_left = collaboration.change_proposal(
        "Book",
        {"title": "Dune"},
        {"title": "Dune Messiah"},
        author="ada",
    )
    conflict_right = collaboration.change_proposal(
        "Book",
        {"title": "Dune"},
        {"title": "Children of Dune"},
        author="grace",
    )
    conflict_report = collaboration.proposal_conflict_report((conflict_left, conflict_right))
    assert conflict_report["ok"] is False
    assert conflict_report["conflicts"][0]["fields"] == ("title",)
    queue = collaboration.merge_queue(
        (conflict_left, conflict_right),
        (collaboration.review_decision(conflict_left, "bo", "approved"),),
    )
    assert queue["blocked"]
    resolution = collaboration.conflict_resolution_plan(conflict_report["conflicts"][0], actor="bo")
    assert resolution["format"] == "appgen.conflict-resolution-plan.v1"
    assert any(item["resource"] == "manifest" for item in version_control.version_resource_catalog())
    before_snapshot = version_control.snapshot_manifest(manifest, author="ada", message="baseline")
    changed_manifest = json.loads(json.dumps(manifest))
    changed_manifest["tables"][0]["columns"].append({"name": "edition", "type": "string"})
    after_snapshot = version_control.snapshot_manifest(changed_manifest, author="ada", message="add edition")
    diff = version_control.diff_snapshots(before_snapshot, after_snapshot)
    assert diff["change_count"] == 1
    assert diff["changes"][0]["kind"] == "field_added"
    assert version_control.branch_plan(before_snapshot, "feature/edition")["base_revision"] == before_snapshot["revision_id"]
    rollback = version_control.rollback_plan((before_snapshot, after_snapshot), before_snapshot["revision_id"])
    assert rollback["requires_review"] is True
    assert rollback["discarded_revisions"] == (after_snapshot["revision_id"],)
    assert version_control.version_control_check(
        {"app/version_control.py", "app/templates/appgen_version_control.html"}
    )["ok"] is True
    assert {item["tool"] for item in devtools.devtool_catalog()} == {"vscode", "eclipse", "jetbrains"}
    assert devtools.vscode_launch_profile()["module"] == "flask"
    assert any(task["label"] == "AppGen quality" for task in devtools.vscode_tasks())
    assert devtools.jetbrains_run_config()["type"] == "Python.FlaskServer"
    assert any(task["name"] == "AppGen quality" for task in devtools.jetbrains_tasks())
    assert devtools.eclipse_project()["nature"] == "org.python.pydev.pythonNature"
    assert any(item["table"] == "Book" for item in devtools.source_map())
    assert devtools.devtools_check(
        {
            "app/devtools.py",
            "app/templates/appgen_devtools.html",
            ".vscode/launch.json",
            ".vscode/tasks.json",
            ".vscode/extensions.json",
            ".idea/misc.xml",
            ".idea/modules.xml",
            ".idea/runConfigurations/AppGen_Flask.xml",
            ".project",
            ".pydevproject",
        }
    )["ok"] is True
    assert studio.editable_files()
    assert {"web", "mobile", "desktop"} <= set(studio.ide_workspace()["generation"]["targets"])
    assert "open_dsl" in {item["command"] for item in studio.ide_command_palette()}
    capability_matrix = studio.ide_capability_matrix()
    assert capability_matrix["format"] == "appgen.ide-capability-matrix.v1"
    assert capability_matrix["ok"] is True
    assert {
        "dsl_authoring",
        "database_design",
        "application_generation",
        "application_management",
        "natural_language_evolution",
    } <= {item["capability"] for item in capability_matrix["capabilities"]}
    workflow_blueprint = studio.ide_workflow_blueprint()
    assert workflow_blueprint["format"] == "appgen.ide-workflow-blueprint.v1"
    assert studio.ide_workflow_blueprint("design_database")["steps"][0] == "edit table/field design"
    assert "Application" in {item["name"] for item in studio.project_tree()}
    assert {item["command"] for item in studio.command_palette_search("database")} >= {"design_database"}
    editor_state = studio.dsl_editor_state(text="app Library")
    assert editor_state["lint"]["warnings"]
    assert "code_actions" in editor_state["panels"]
    action_state = studio.dsl_editor_state(text="app Bad { targets: web, toaster } table Book { title: string ref Author.id }")
    assert {action["id"] for action in action_state["code_actions"]} >= {"normalize_targets", "replace_ref_with_arrow"}
    assert {action["id"] for action in studio.dsl_code_actions("table Book { title: string ref Author.id }")} >= {
        "add_app_declaration",
        "replace_ref_with_arrow",
    }
    assert studio.dsl_keyword_budget()["ok"] is True
    assert studio.dsl_keyword_budget()["canonical_keyword_count"] == 17
    assert studio.dsl_keyword_budget()["legacy_contextual_tokens"] == ("ref",)
    authoring = studio.dsl_authoring_surface(
        "app Library { targets: web, mobile, toaster } table Book { id: int pk }"
    )
    assert authoring["outline"]["tables"] == ("Book",)
    assert any("Unknown app targets: toaster" in error for error in authoring["lint"]["errors"])
    assert any(fix["id"] == "normalize_targets" for fix in authoring["lint"]["fixes"])
    assert studio.dsl_quick_fixes("table Book { id: int pk }")[0]["id"] == "add_app_declaration"
    assert any(item["label"] == "Delphi Component" for item in studio.dsl_completion_items("Delphi"))
    assert studio.dsl_schema_preview("table Book { id: int pk }")["exports"] == ("dbml", "sql", "ponyorm")
    dsl_editor = studio.editor_session("appgen.dsl", "app Library { targets: web }")
    assert dsl_editor["language"] == "appgen-dsl"
    assert "schema_preview" in dsl_editor["checks"]
    assert studio.dsl_change_plan("add invoice table")["can_create"] == (
        "tables",
        "fields",
        "forms",
        "chatbots",
        "agents",
        "platform_targets",
    )
    assert studio.database_design_catalog()[1]["table"] == "Book"
    assert studio.table_design("Book")["model"] == "Book"
    assert studio.field_design("Book", "title")["required"] is True
    workbench = studio.database_design_workspace()
    assert workbench["erd"].startswith("erDiagram\n")
    assert "relationship" in workbench["proposal_kinds"]
    assert "Table Book" in workbench["exports"]["dbml"]
    assert "CREATE TABLE Book" in workbench["exports"]["sql"]
    assert "class Book(db.Entity)" in workbench["exports"]["ponyorm"]
    assert workbench["sql_workbench"]["format"] == "appgen.sql-workbench.v1"
    assert studio.sql_referenced_tables("select * from Book join Author on Book.author_id = Author.id") == (
        "Book",
        "Author",
    )
    assert studio.sql_statement_guard("delete from Book")["ok"] is False
    sql_session = studio.sql_workbench_session("select * from Book", dialect="sqlite")
    assert sql_session["guard"]["read_only"] is True
    assert sql_session["side_effects"] == ()
    assert sql_session["explain"]["tables"] == ("Book",)
    assert sql_session["builder"]["format"] == "appgen.sql-select-builder.v1"
    assert "build_select" in sql_session["commands"]
    assert any(item["label"] == "Book.title" for item in studio.sql_completion_items("Book.", table_name="Book"))
    query = studio.sql_select_builder(
        "Book",
        fields=("title",),
        filters=({"field": "title", "operator": "like", "parameter": "title", "value": "D%"},),
        limit=25,
        order_by="title",
    )
    assert query["ok"] is True
    assert query["statement"] == "SELECT title FROM Book WHERE title LIKE :title ORDER BY title LIMIT 25"
    assert query["params"] == {"title": "D%"}
    assert query["guard"]["read_only"] is True
    assert studio.sql_filter_plan("Book", ({"field": "missing", "operator": "="},))["ok"] is False
    assert studio.sql_select_builder("Book", fields=("missing",))["ok"] is False
    assert studio.schema_erd_mermaid().startswith("erDiagram\n")
    assert "Ref: Book.author_id > Author.id" in studio.schema_dbml()
    assert "author_id INTEGER REFERENCES Author(id)" in studio.schema_sql_ddl()
    assert "author_id = Optional('Author')" in studio.schema_ponyorm()
    table_proposal = studio.database_table_proposal(
        "Invoice", ({"name": "number", "type": "string", "required": True},)
    )
    assert table_proposal["migration"]["requires_review"] is True
    assert "Table Invoice" in table_proposal["preview"]["dbml"]
    relationship_proposal = studio.database_relationship_proposal("Book", "publisher_id", "Publisher")
    assert relationship_proposal["preview"]["dsl"] == "  publisher_id: int -> Publisher.id [many-to-one]"
    assert relationship_proposal["migration"]["change"]["action"] == "add_relationship"
    assert studio.schema_change_preview({"add_field": "Book.edition"})["review_required"] is True
    assert studio.database_migration_plan({"add_field": "Book.edition"})["requires_review"] is True
    assert studio.app_generation_plan(targets=("web", "desktop"))["targets"] == ("web", "desktop")
    job = studio.generation_job_plan(targets=("web", "mobile"), changed_paths=("appgen.dsl",))
    assert [stage["name"] for stage in job["stages"]] == ["lint_dsl", "schema_diff", "generate", "quality"]
    job_manifest = studio.generation_job_manifest(targets=("web", "mobile"), changed_paths=("appgen.dsl",))
    assert job_manifest["format"] == "appgen.generation-job.v1"
    assert job_manifest["job_id"] == studio.generation_job_id(targets=("web", "mobile"), changed_paths=("appgen.dsl",))
    assert studio.generation_job_status(job_manifest)["remaining_stages"] == ("lint_dsl", "schema_diff", "generate", "quality")
    assert studio.generation_job_log(job_manifest)["entries"][0]["stage"] == "lint_dsl"
    assert studio.generation_job_queue((job_manifest,))["jobs"][0]["job_id"] == job_manifest["job_id"]
    artifacts = studio.generation_artifact_manifest(("web", "mobile"))
    assert artifacts["format"] == "appgen.generation-artifacts.v1"
    assert {item["target"] for item in artifacts["artifacts"]} == {"web", "mobile"}
    applications = studio.application_registry()
    assert applications["format"] == "appgen.application-registry.v1"
    assert applications["active"] == "Library"
    assert {"dsl", "dbml", "sql", "ponyorm", "database"} <= set(applications["source_kinds"])
    creation = studio.application_creation_plan(
        "InvoiceApp", source_kind="dbml", source_path="invoice.dbml", targets=("web", "mobile")
    )
    assert creation["command"] == "appgen --dbml invoice.dbml --writedir apps/invoiceapp"
    assert creation["stages"][0] == "source_fidelity"
    assert studio.application_import_plan("database", "sqlite:///legacy.db")["source_kind"] == "database"
    assert studio.application_open_plan("Library")["format"] == "appgen.application-open-plan.v1"
    assert studio.application_export_package("Library")["bundle"]
    assert studio.application_portfolio_check()["ok"] is True
    assert studio.app_management_plan("deploy")["requires_review"] is True
    assert studio.file_edit_plan("app/models.py", "add comment")["requires_review"] is True
    debug = studio.debug_session()
    assert debug["breakpoints"]
    assert studio.breakpoint_plan("app/views.py", symbol="init_views")["symbol"] == "init_views"
    inspected = studio.variable_inspection("request", {"SECRET_KEY": "x", "title": "Dune"})
    assert inspected["variables"]["SECRET_KEY"] == "[redacted]"
    assert studio.dependency_update_plan("flask", "3.0")["package"] == "flask"
    component = studio.component_repository()[0]
    assert studio.component_share_package(component["id"])["component"]["id"] == component["id"]
    assert studio.clone_plan("LibraryCopy")["new_app_name"] == "LibraryCopy"
    ide_report = studio.ide_diagnostics(
        {"app/studio.py", "app/templates/appgen_studio.html", "app/dsl_reference.py", "app/models.py", "migrations/README.md", "scripts/appgen_quality.py"},
        {"DATABASE_URL": "sqlite:///app.db", "SECRET_KEY": "x"},
    )
    assert ide_report["format"] == "appgen.ide-diagnostics.v1"
    assert ide_report["ok"] is True
    studio_ready = studio.studio_check({"app/studio.py", "app/templates/appgen_studio.html"})
    assert studio_ready["ok"] is True
    assert "design_database" in studio_ready["commands"]
    studio_gate = studio.studio_release_gate(
        {
            "app/studio.py",
            "app/templates/appgen_studio.html",
            "app/dsl_reference.py",
            "app/models.py",
            "migrations/README.md",
            "scripts/appgen_quality.py",
        }
    )
    assert studio_gate["format"] == "appgen.studio-release-gate.v1"
    assert studio_gate["ok"] is True
    assert studio_gate["blocking_gaps"] == ()
    assert {
        gate["gate"] for gate in studio_gate["gates"]
    } >= {"capability_matrix", "dsl_lint", "database_workbench", "safe_sql", "query_builder", "generation_pipeline", "component_sharing"}
    assert studio.studio_release_gate({"app/studio.py"})["ok"] is False
    book_tabs = tabbed_views.tabbed_view("BookList")
    assert [tab["id"] for tab in book_tabs["tabs"]] == ["overview", "assets"]
    overview_policy = tabbed_views.tab_policy("BookList", "overview")
    assert overview_policy["required_action"] == "read"
    assert overview_policy["allowed_roles"] == ("Editor",)
    assert tabbed_views.can_access_tab("BookList", "overview", ("Editor",)) is True
    assert tabbed_views.can_access_tab("BookList", "overview", ("Viewer",)) is False
    assert [tab["id"] for tab in tabbed_views.visible_tabs("BookList", ("Editor",))] == ["overview", "assets"]
    assert tabbed_views.tabbed_views_check(
        {"app/tabbed_views.py", "app/templates/appgen_tabbed_views.html"}
    )["ok"] is True
    assert diagnostics.selftest()["ok"] is True
    assert diagnostics.selftest()["summary"]["fail"] == 0
    assert diagnostics.validate_row("Book", {"status": "draft"})["missing"] == ("title",)
    snapshot = diagnostics.debug_snapshot(
        {"SECRET_KEY": "secret", "APP_NAME": "Library"},
        {"PATH": "/usr/bin"},
    )
    assert snapshot["config"]["SECRET_KEY"] == "[redacted]"
    assert snapshot["config"]["APP_NAME"] == "Library"
    remediation = diagnostics.remediation_plan(({"name": "Book has primary key", "status": "warn", "details": ()},))
    assert remediation["format"] == "appgen.diagnostics-remediation.v1"
    assert remediation["actions"][0]["severity"] == "warning"
    support_bundle = diagnostics.support_bundle({"SECRET_KEY": "secret"}, {"PATH": "/usr/bin"})
    assert support_bundle["format"] == "appgen.support-bundle.v1"
    assert support_bundle["snapshot"]["config"]["SECRET_KEY"] == "[redacted]"
    assert diagnostics.api_smoke_plan()[1]["path"] == "/api/v1/book/"
    assert diagnostics.load_test_plan(users=3, duration_seconds=5)["users"] == 3
    api_requests = api_testing.request_plan()
    assert any(request["name"] == "list_book" and request["path"] == "/api/v1/book/" for request in api_requests)
    assert api_testing.sample_payload("Book")["title"] == "sample_title"
    assert api_testing.sample_payload("Book")["status"] == "draft"
    assert api_testing.validate_response("list_book", 200)["ok"] is True
    assert api_testing.validate_response("create_book", 201)["ok"] is True
    assert api_testing.synthetic_check_results({"list_book": 200})["ok"] is True
    assert api_testing.synthetic_monitor_plan(interval_seconds=1)["interval_seconds"] == 15
    fixture_strategy = api_testing.fixture_strategy()
    assert fixture_strategy["format"] == "appgen.api-test-fixture-strategy.v1"
    assert fixture_strategy["default_scenario"] == "smoke"
    assert "get_book" in fixture_strategy["requires_fixture_cases"]
    ui_smoke = api_testing.ui_smoke_plan(base_url="https://app.example.test")
    assert any(item["name"] == "book_list_view" for item in ui_smoke)
    assert ui_smoke[0]["url"].startswith("https://app.example.test/")
    ui_result = api_testing.ui_smoke_result(
        "home",
        status_code=200,
        text="Library",
        selectors=("body",),
        accessibility=("has_title", "has_main_or_body"),
    )
    assert ui_result["ok"] is True
    assert api_testing.ui_smoke_results({"home": {"status_code": 500}})["ok"] is False
    assert "def test_generated_ui_smoke(page, case):" in api_testing.render_playwright_smoke_module()
    pytest_cases = api_testing.pytest_case_matrix()
    assert pytest_cases[0]["id"] == api_requests[0]["name"]
    assert next(case for case in pytest_cases if case["requires_fixture"])["fixture_scenario"] == "smoke"
    rendered_pytest = api_testing.render_pytest_module()
    assert "@pytest.mark.parametrize" in rendered_pytest
    assert "FIXTURE_STRATEGY" in rendered_pytest
    assert "def test_generated_api_contracts(client, appgen_seed_data, case):" in rendered_pytest
    assert api_testing.test_execution_plan()["case_count"] == len(pytest_cases)
    assert api_testing.test_execution_plan()["ui_case_count"] == len(api_testing.ui_smoke_plan())
    assert api_testing.test_execution_plan()["fixture_source"] == "seed.py"
    assert api_testing.contract_coverage(openapi.openapi_spec()["paths"].keys())["ok"] is True
    api_testing_gate = api_testing.api_testing_release_gate(
        {"app/api_testing.py", "app/templates/appgen_api_testing.html", "docs/openapi.json"},
        openapi.openapi_spec()["paths"].keys(),
    )
    assert api_testing_gate["format"] == "appgen.api-testing-release-gate.v1"
    assert api_testing_gate["ok"] is True
    assert {"api_request_matrix", "ui_smoke", "synthetic_monitoring", "contract_coverage"} <= {
        gate["gate"] for gate in api_testing_gate["gates"]
    }
    assert api_testing.api_testing_release_gate({"app/api_testing.py"}, openapi.openapi_spec()["paths"].keys())[
        "ok"
    ] is False
    assert api_testing.api_testing_check(
        {"app/api_testing.py", "app/templates/appgen_api_testing.html", "docs/openapi.json"}
    )["ok"] is True
    review_findings = code_review.schema_review()
    assert any(item["rule"] == "primary-key" and item["table"] == "Book" for item in review_findings)
    assert any(item["rule"] == "protected-hidden-fields" and item["table"] == "Book" for item in review_findings)
    assert code_review.review_summary()["ok"] is True
    assert code_review.artifact_review({"app/models.py"})["missing"]
    component_catalog = components.component_catalog()
    assert any(item["table"] == "Book" and "form" in item["components"] for item in component_catalog)
    assert components.field_widget("Author", "email")["widget"] == "email-input"
    assert components.field_widget("Author", "birth_date")["widget"] == "calendar-date"
    assert components.field_widget("Author", "birth_date")["component"] == "DatePicker"
    assert components.field_widget("Author", "birth_date")["input_type"] == "date"
    assert components.field_widget("Author", "last_seen_at")["widget"] == "calendar-datetime"
    assert components.field_widget("Author", "last_seen_at")["input_type"] == "datetime-local"
    assert components.field_widget("Author", "appointment_time")["widget"] == "time-input"
    assert {item["field"] for item in components.calendar_fields("Author")} == {
        "birth_date",
        "last_seen_at",
        "appointment_time",
    }
    assert components.platform_widget("Author", "birth_date", "mobile")["renderer"] == "native-date-picker"
    assert any(item["widget"] == "calendar-datetime" for item in components.widget_registry())
    assert any(item["type"] == "DateTimePicker" for item in components.component_palette())
    assert components.field_widget("Book", "author")["widget"] == "relationship-picker"
    assert components.lookup_contract("Book", "author")["target_table"] == "Author"
    assert components.lookup_contract("Book", "author")["source_column"] == "author_id"
    assert components.lookup_contract("Book", "author")["label_fields"] == ("name", "email")
    assert components.lookup_options("Book", "author", [{"id": 1, "name": "Ada", "email": "ada@example.test"}]) == (
        {"value": 1, "label": "Ada ada@example.test"},
    )
    assert components.field_widget("Book", "status")["widget"] == "select"
    assert components.field_widget("Book", "status")["choices"] == ("draft", "published", "archived")
    assert components.field_widget("Book", "summary")["widget"] == "textarea"
    assert components.field_widget("Book", "cover_image")["widget"] == "image-upload"
    assert components.field_widget("Book", "manuscript_file")["widget"] == "file-upload"
    form_layout = components.form_layout("Book")
    assert [section["name"] for section in form_layout["sections"]] == ["overview", "assets"]
    assert form_layout["sections"][0]["fields"][0]["field"] == "title"
    assert form_layout["sections"][1]["fields"][0]["widget"] == "image-upload"
    assert "internal_code" not in components.list_layout("Book")["columns"]
    contract = components.component_contract("Book")
    assert contract["table"] == "Book"
    assert "detail" in contract
    custom_widget = components.custom_widget_contract("Signature Pad", props=("value", "penColor"))
    assert custom_widget["format"] == "appgen.custom-widget.v1"
    assert custom_widget["renderer"]["mobile"] == "mobile-custom-signature-pad"
    custom_plan = components.custom_widget_registration_plan(custom_widget, package="app_custom/widgets/signature")
    assert custom_plan["format"] == "appgen.custom-widget-registration.v1"
    assert custom_plan["side_effects"] == ()
    custom_preview = components.custom_widget_preview(custom_widget, {"penColor": "#111111"})
    assert custom_preview["props"]["penColor"] == "#111111"
    assert components.custom_widget_palette_entry(custom_widget)["custom"] is True
    assert "custom_widget_extension_points" in components.visual_builder_payload()
    assert any(item["master"] == "Book" and item["detail"] == "Author" for item in view_composition.master_detail_catalog())
    assert view_composition.chart_view_catalog()
    assert view_composition.view_composition_check(
        {"app/views.py", "app/view_composition.py", "app/templates/appgen_view_composition.html"}
    )["ok"] is True
    assert any(item["type"] == "TextBox" for item in form_designer.component_palette())
    assert any(item["type"] == "DateTimePicker" for item in form_designer.component_palette())
    assert form_designer.field_component("Author", "birth_date")["type"] == "DatePicker"
    assert form_designer.field_component("Author", "last_seen_at")["type"] == "DateTimePicker"
    assert form_designer.field_component("Author", "appointment_time")["type"] == "TimePicker"
    design = form_designer.form_design("Book")
    assert design["source_view"] == "BookList"
    assert any(component["field"] == "summary" and component["type"] == "TextArea" for component in design["components"])
    proposal = form_designer.proposal_from_drop({"table": "Book", "component": "TextBox", "field": "title", "x": 1, "y": 1})
    updated_design = form_designer.apply_form_proposal(design, proposal)
    assert form_designer.validate_form_design(updated_design)["ok"] is True
    assert proposal["component"]["x"] == 1
    assert proposal["component"]["y"] == 1
    assert any(item["name"] == "field" for item in proposal["properties"])
    overflow = form_designer.drop_component("Book", "TextBox", x=99, y=2, w=4)
    assert overflow["x"] == 8
    assert form_designer.component_bounds(overflow)["right"] == 12
    overlapping = form_designer.apply_form_proposal(
        design,
        form_designer.proposal_from_drop({"table": "Book", "component": "TextBox", "field": "title", "x": 0, "y": 0}),
    )
    validation = form_designer.validate_form_design(overlapping)
    assert validation["ok"] is False
    assert validation["conflicts"]
    suggestion = form_designer.placement_suggestion(design, "TextBox", "title")
    assert suggestion["component"]["y"] > max(component["y"] for component in design["components"])
    assert "getBoundingClientRect" in (output_dir / "templates" / "appgen_form_designer.html").read_text()
    assert "Inspector" in (output_dir / "templates" / "appgen_form_designer.html").read_text()
    nl_plan = nl_evolution.evolution_plan(
        "create table Ticket with fields title, email unique, amount decimal, author_id references Author required "
        "and form TicketForm workflow Triage "
        "from open to closed rule TicketPolicy chatbot SupportBot agent SupportAgent "
        "targets web mobile desktop"
    )
    assert {
        "add_table",
        "add_field",
        "add_form",
        "add_workflow",
        "add_rule",
        "add_chatbot",
        "add_agent",
        "set_targets",
    }.issubset({item["kind"] for item in nl_plan["proposals"]})
    field_proposals = [item for item in nl_plan["proposals"] if item["kind"] == "add_field"]
    assert [item["name"] for item in field_proposals] == ["title", "email", "amount", "author_id"]
    assert field_proposals[0]["modifiers"] == ("required", "search")
    assert field_proposals[1]["type"] == "email"
    assert {"unique", "search"}.issubset(set(field_proposals[1]["modifiers"]))
    assert field_proposals[2]["type"] == "decimal"
    assert field_proposals[3]["type"] == "int"
    assert field_proposals[3]["references"] == {"table": "Author", "column": "id"}
    assert field_proposals[3]["cardinality"] == "many-to-one"
    nl_dsl = nl_evolution.proposals_to_dsl(nl_plan)
    assert "agent SupportAgent" in nl_dsl
    assert "table Ticket {" in nl_dsl
    assert "title: string required search" in nl_dsl
    assert "email: email unique search" in nl_dsl
    assert "amount: decimal" in nl_dsl
    assert "author_id: int -> Author.id [many-to-one] required" in nl_dsl
    assert "flow Triage" in nl_dsl
    assert "open -> closed" in nl_dsl
    assert "rule TicketPolicy for Ticket" in nl_dsl
    assert "targets: web, mobile, desktop" in nl_dsl
    erp_nl_plan = nl_evolution.evolution_plan(
        "generate ERP accounts payable and inventory for targets web desktop"
    )
    erp_modules = {
        item["module"] for item in erp_nl_plan["proposals"] if item["kind"] == "add_erp_module"
    }
    assert {"accounts_payable", "inventory"} <= erp_modules
    assert "erp_templates.erp_module_dsl('accounts_payable')" in nl_evolution.proposals_to_dsl(erp_nl_plan)
    erp_impact = nl_evolution.migration_impact(erp_nl_plan)
    assert any(item.get("action") == "add_erp_module" for item in erp_impact["review"])
    changeset = nl_evolution.evolution_changeset(
        "create table Ticket with fields title and form TicketForm chatbot SupportBot agent SupportAgent targets web mobile desktop",
        "app Library\n\ntable Author {\n  id: int pk\n  name: string\n}\n",
    )
    assert changeset["format"] == "appgen.nl-changeset.v1"
    assert changeset["id"].startswith("nlchg-")
    assert changeset["summary"]["kinds"]["add_table"] == 1
    assert changeset["migration_impact"]["format"] == "appgen.nl-migration-impact.v1"
    assert {"action": "create_table", "table": "Ticket", "destructive": False} in changeset["migration_impact"]["ddl"]
    assert changeset["test_plan"]["format"] == "appgen.nl-test-plan.v1"
    assert {"dsl_lint", "schema_diff", "ui_smoke", "agent_provider_readiness"} <= set(changeset["test_plan"]["checks"])
    assert changeset["rollback"]["format"] == "appgen.nl-rollback-plan.v1"
    assert changeset["rollback"]["review_required"] is True
    assert changeset["requires_approval"] is True
    assert changeset["app_patch"] == {"targets": ("web", "mobile", "desktop")}
    assert "app Library { targets: web, mobile, desktop }" in changeset["applied_preview"]
    assert "table Ticket {" in changeset["applied_preview"]
    approval = nl_evolution.approval_workflow(changeset, actor="ada")
    assert approval["current"] == "review"
    assert approval["actor"] == "ada"
    assert "rollback_plan" in approval["required_checks"]
    patched_dsl = nl_evolution.apply_changeset("app Existing { theme: sage }\n", changeset)
    assert "app Existing { theme: sage; targets: web, mobile, desktop }" in patched_dsl
    assert "agent SupportAgent" in patched_dsl
    destructive_report = nl_evolution.destructive_intent_report("remove field title from Ticket and drop table OldTicket")
    assert destructive_report["destructive"] is True
    destructive_changeset = nl_evolution.evolution_changeset(
        "remove field title from Ticket and drop table OldTicket",
        "app Library { targets: web }\n\ntable Ticket {\n  id: int pk\n  title: string\n}\n",
    )
    assert destructive_changeset["migration_impact"]["destructive"] is True
    assert {"action": "drop_column", "table": "Ticket", "field": "title", "destructive": True, "requires_backup": True} in destructive_changeset["migration_impact"]["ddl"]
    assert {"action": "drop_table", "table": "OldTicket", "destructive": True, "requires_backup": True} in destructive_changeset["migration_impact"]["ddl"]
    assert destructive_changeset["rollback"]["requires_backup"] is True
    assert destructive_changeset["test_plan"]["destructive"] is True
    assert "data_backup_review" in destructive_changeset["test_plan"]["checks"]
    assert "// destructive: remove field Ticket.title" in destructive_changeset["applied_preview"]
    assert dsl_reference.dsl_keyword_budget()["count"] <= dsl_reference.dsl_keyword_budget()["limit"]
    assert dsl_reference.dsl_keyword_budget()["format"] == "appgen.dsl-keyword-budget.v1"
    assert dsl_reference.dsl_keyword_budget()["legacy_contextual_tokens"] == ("ref",)
    assert dsl_reference.dsl_language_quality_contract()["format"] == "appgen.dsl-language-quality.v1"
    assert dsl_reference.dsl_language_quality_contract()["ok"] is True
    assert dsl_reference.dsl_language_quality_contract()["canonical_keyword_count"] == 17
    assert "ref" not in dsl_reference.dsl_language_quality_contract()["keywords"]
    assert dsl_reference.dsl_reference_check(
        {"app/dsl_reference.py", "app/templates/appgen_dsl_reference.html"}
    )["language_quality"]["ok"] is True
    assert "[cardinality] relation metadata" in dsl_reference.dsl_keyword_budget()["keyword_free_syntax"]
    assert "entity/model/form/screen/workflow authoring aliases" in dsl_reference.dsl_keyword_budget()["keyword_free_syntax"]
    assert "hide/searchable modifier aliases" in dsl_reference.dsl_keyword_budget()["keyword_free_syntax"]
    assert dsl_reference.dsl_keyword_budget()["modifier_aliases"] == {"hide": "hidden", "searchable": "search"}
    assert "Reference" in {item["name"] for item in dsl_reference.dsl_construct_catalog()}
    assert "author_id: int -> Author.id [many-to-one]" in dsl_reference.dsl_example("relation")
    assert dsl_reference.dsl_lint(dsl_reference.dsl_example("full"))["ok"] is True
    assert dsl_reference.dsl_lint(
        "table Book { author_id: int -> Author.id [one2one] }"
    )["errors"]
    assert dsl_reference.dsl_lint("table Book { author_id: int ref Author.id }")["warnings"]
    ref_lint = dsl_reference.dsl_lint("table Book { author_id: int ref Author.id }")
    assert {"add_app_declaration", "replace_ref_with_arrow"}.issubset(
        {fix["id"] for fix in ref_lint["fixes"]}
    )
    assert dsl_reference.dsl_lint("app Bad { targets: web, toaster } table Book { title: string }")["errors"]
    generated_fix = dsl_reference.apply_dsl_fixes(
        "app Bad { targets: web, toaster } table Book { title: string ref Author.id }"
    )
    assert generated_fix["format"] == "appgen.dsl-fix-result.v1"
    assert {"replace_ref_with_arrow", "normalize_targets"} <= set(generated_fix["applied"])
    assert "title: string -> Author.id" in generated_fix["fixed"]
    assert "toaster" not in generated_fix["fixed"]
    generated_actions = dsl_reference.dsl_code_actions(
        "app Bad { targets: web, toaster } table Book { title: string ref Author.id }"
    )
    assert {action["id"] for action in generated_actions} >= {"normalize_targets", "replace_ref_with_arrow"}
    assert all(action["format"] == "appgen.dsl-code-action.v1" for action in generated_actions)
    generated_format = dsl_reference.format_dsl(
        "app Library{targets:web,desktop} table Book{id:int pk; title:string required}"
    )
    assert generated_format["format"] == "appgen.dsl-format-result.v1"
    assert generated_format["after"]["ok"] is True
    assert "app Library {\n  targets: web, desktop\n}" in generated_format["formatted"]
    assert "table Book {\n  id: int pk\n  title: string required\n}" in generated_format["formatted"]
    generated_alias_lint = dsl_reference.dsl_lint("entity Book { title: string } form BookForm for Book { Main: title }")
    assert generated_alias_lint["ok"] is True
    assert "normalize_authoring_aliases" in {fix["id"] for fix in generated_alias_lint["fixes"]}
    generated_alias_fix = dsl_reference.apply_dsl_fixes(
        "entity Book { title: string } form BookForm for Book { Main: title }"
    )
    assert "table Book" in generated_alias_fix["fixed"]
    assert "view BookForm for Book" in generated_alias_fix["fixed"]
    generated_modifier_lint = dsl_reference.dsl_lint(
        "app Alias { targets: web } table Book { title: string searchable; secret: string hide }"
    )
    assert generated_modifier_lint["ok"] is True
    assert "normalize_modifier_aliases" in {fix["id"] for fix in generated_modifier_lint["fixes"]}
    generated_modifier_fix = dsl_reference.apply_dsl_fixes(
        "app Alias { targets: web } table Book { title: string searchable; secret: string hide }"
    )
    assert "title: string search" in generated_modifier_fix["fixed"]
    assert "secret: string hidden" in generated_modifier_fix["fixed"]
    assert dsl_reference.dsl_lint(
        "table Book { title: string title: text } table Book { title: string }"
    )["errors"]
    view_lint = dsl_reference.dsl_lint(
        "table Book { title: string } view BookForm for Book { Main: missing; @ other TextBox 0 0 4 1; }"
    )
    assert "Unknown view field: BookForm.missing" in view_lint["errors"]
    assert "Unknown component field: BookForm.other" in view_lint["errors"]
    assert dsl_reference.dsl_lint(
        "llm Local { mode: local } agent Helper { provider: Cloud } table Book { title: string }"
    )["errors"]
    assert dsl_reference.dsl_reference_check(
        {"app/dsl_reference.py", "app/templates/appgen_dsl_reference.html"}
    )["ok"] is True
    offline_states = view_experience.offline_field_state("Book", {"title": "Dune"})
    assert offline_states[0]["status"] == "queued"
    presence = view_experience.presence_event("/Book/list/", "ada")
    assert presence["resource"] == "Book"
    assert view_experience.active_viewers("/Book/list/", (presence,))
    access = view_experience.access_log_event("/Book/list/", "ada", duration_ms=25)
    assert access["resource"] == "Book"
    assert view_experience.access_log_summary((access,))["unique_users"] == 1
    footer = view_experience.view_footer_context("ada", "/Book/list/")
    assert footer["version"] == "0.1.0"
    assert footer["offline_ready"] is True
    assert footer["help"]["href"] == "/chatbot/"
    assert view_experience.baseview_experience_check(
        {
            "app/view_experience.py",
            "app/templates/appgen_view_experience.html",
            "app/static/appgen-view-experience.js",
        }
    )["ok"] is True
    assert "getting-started" in {item["key"] for item in support_center.support_topic_catalog()}
    assert support_center.tutorial_catalog()[0]["key"] == "first-app"
    sample_dsl = support_center.sample_application_catalog()[0]["dsl"]
    assert "table " in sample_dsl and "view " in sample_dsl
    assert "id: string required search" not in sample_dsl
    assert any(item["key"] == "read-dsl" for item in support_center.onboarding_checklist())
    assert support_center.search_support("security")
    ticket = support_center.support_ticket_payload("security setup", user="ada", path="/identity/")
    assert ticket["id"].startswith("support-")
    assert ticket["status"] == "open"
    assert support_center.support_center_check(
        {"app/support_center.py", "app/templates/appgen_support_center.html"}
    )["ok"] is True
    first_prototype = prototyping.prototype_catalog()[0]["resource"]
    assert prototyping.sample_row(first_prototype)
    assert prototyping.screen_mockup(first_prototype, "create")["layout"] == "form"
    assert prototyping.prototype_plan(first_prototype)["screens"]
    assert prototyping.experiment_hypothesis(first_prototype, "shorter form")["id"].startswith("proto-")
    assert prototyping.preview_package(first_prototype)["format"] == "appgen-prototype-v1"
    assert prototyping.promote_to_backlog(first_prototype)[0]["key"].startswith("PROTO-")
    assert prototyping.prototyping_check({"app/prototyping.py", "app/templates/appgen_prototyping.html"})["ok"] is True
    erp_modules = {item["module"] for item in erp_templates.erp_template_catalog()}
    assert {
        "general_ledger",
        "chart_of_accounts",
        "invoicing",
        "accounts_payable",
        "accounts_receivable",
        "inventory",
        "human_resources",
        "payroll",
        "purchasing",
        "procurement",
        "supply_chain",
        "warehouse_management",
        "manufacturing",
        "sales",
        "crm",
        "ecommerce",
        "fixed_assets",
        "maintenance",
        "quality_management",
        "document_management",
        "compliance_management",
        "projects",
        "reporting",
    }.issubset(erp_modules)
    gl_dsl = erp_templates.erp_module_dsl("general_ledger")
    assert "table ledger_account" in gl_dsl
    assert "ledger_account_id: int required -> ledger_account.id" in gl_dsl
    assert "debit_amount: decimal default 0" in gl_dsl
    invoicing_dsl = erp_templates.erp_module_dsl("invoicing")
    assert "invoice_id: int required -> invoice.id" in invoicing_dsl
    assert "line_total: decimal = quantity * unit_price" in invoicing_dsl
    inventory_dsl = erp_templates.erp_module_dsl("inventory")
    assert "sku: string required unique search" in inventory_dsl
    manufacturing_dsl = erp_templates.erp_module_dsl("manufacturing")
    assert "table work_order" in manufacturing_dsl
    assert "bill_of_material_id: int required -> bill_of_material.id" in manufacturing_dsl
    crm_dsl = erp_templates.erp_module_dsl("crm")
    assert "table opportunity" in crm_dsl
    assert "lead_id: int -> lead.id" in crm_dsl
    warehouse_dsl = erp_templates.erp_module_dsl("warehouse_management")
    assert "bin_location_id: int -> bin_location.id" in warehouse_dsl
    quality_dsl = erp_templates.erp_module_dsl("quality_management")
    assert "nonconformance_id: int required -> nonconformance.id" in quality_dsl
    hr_dsl = erp_templates.erp_module_dsl("human_resources")
    assert "employee_number: string required unique search" in hr_dsl
    ap_blueprints = erp_templates.erp_table_blueprints("accounts_payable")
    assert any(item["table"] == "vendor_bill" and "vendor_id: int required -> vendor.id" in item["fields"] for item in ap_blueprints)
    ar_package = erp_templates.erp_module_package("accounts_receivable")
    assert "dsl" in ar_package and "customer_invoice" in ar_package["dsl"]
    stacks = {item["stack"]: item for item in erp_templates.erp_recommended_stacks()}
    assert {"finance_core", "distribution_core", "people_core", "manufacturing_core", "full_erp"} <= set(stacks)
    assert "general_ledger" in stacks["finance_core"]["modules"]
    composite_dsl = erp_templates.erp_composite_dsl(("general_ledger", "invoicing"), app_name="FinanceDesk")
    assert "app FinanceDesk" in composite_dsl
    assert "flow journal_entry_approval" in composite_dsl
    assert "table invoice_line" in composite_dsl
    starter = erp_templates.erp_starter_manifest(("accounts_receivable", "accounts_payable"), app_name="BackOffice")
    assert starter["format"] == "appgen.erp-starter.v1"
    assert "customer_invoice" in starter["tables"]
    assert "vendor_bill" in starter["tables"]
    generation_plan = erp_templates.erp_starter_generation_plan(("inventory",), app_name="StockDesk")
    assert [step["name"] for step in generation_plan["steps"]] == ["compose_dsl", "lint_dsl", "generate", "verify"]
    coverage = erp_templates.erp_domain_coverage_report(erp_templates.ERP_MODULE_RECOMMENDATIONS["full_erp"])
    assert coverage["format"] == "appgen.erp-domain-coverage.v1"
    assert {"finance", "distribution", "people", "manufacturing", "governance"} <= set(coverage["covered_domains"])
    roadmap = erp_templates.erp_implementation_roadmap(("general_ledger", "invoicing"), app_name="FinanceDesk")
    assert roadmap["format"] == "appgen.erp-implementation-roadmap.v1"
    assert roadmap["phases"][-1]["exit_gate"] == "erp_starter_release_gate ok"
    erp_gate = erp_templates.erp_starter_release_gate(
        erp_templates.ERP_MODULE_RECOMMENDATIONS["finance_core"],
        existing_paths={"app/erp_templates.py", "app/templates/appgen_erp_templates.html"},
    )
    assert erp_gate["format"] == "appgen.erp-release-gate.v1"
    assert erp_gate["ok"] is True
    assert {"domain_coverage", "generation_plan", "migration_plan", "artifacts"} <= {
        item["gate"] for item in erp_gate["gates"]
    }
    assert erp_templates.erp_starter_release_gate(("inventory",), existing_paths={"app/erp_templates.py"})["ok"] is False
    migration_plan = erp_templates.erp_data_migration_plan(("inventory",), source="legacy")
    assert migration_plan["format"] == "appgen.erp-migration-plan.v1"
    assert migration_plan["batches"][0]["source"].startswith("legacy.")
    assert erp_templates.erp_templates_check(
        {"app/erp_templates.py", "app/templates/appgen_erp_templates.html"}
    )["ok"] is True
    assert "finance_core" in erp_templates.erp_templates_check(
        {"app/erp_templates.py", "app/templates/appgen_erp_templates.html"}
    )["stacks"]
    assert {"jira", "github", "azure_boards", "gitlab"} == {item["provider"] for item in project_management.provider_catalog({})}
    assert any(item["key"] == "DATA-BOOK" for item in project_management.backlog_templates())
    assert project_management.sprint_plan(capacity=6)["items"]
    assert "appgen_quality" in project_management.release_plan()["gates"]
    assert project_management.traceability_matrix()[0]["story"].startswith("DATA-")
    assert project_management.export_plan("github")[0]["provider"] == "github"
    wizard_catalog = wizards.wizard_catalog()
    assert any(item["name"] == "BookCreate" and item["kind"] == "table" for item in wizard_catalog)
    assert any(item["name"] == "PublishWorkflow" and item["kind"] == "workflow" for item in wizard_catalog)
    book_wizard = wizards.wizard_plan("BookCreate")
    assert book_wizard["steps"][0]["name"] == "required"
    assert any(field["field"] == "title" and field["required"] for field in book_wizard["steps"][0]["fields"])
    assert all(field["field"] != "internal_code" for step in book_wizard["steps"] for field in step["fields"])
    assert wizards.field_questions("BookCreate")[0]["field"] == "title"
    assert next(question for question in wizards.field_questions("BookCreate") if question["field"] == "status")[
        "choices"
    ] == ("draft", "published", "archived")
    assert wizards.validate_step("BookCreate", "required", {"status": "draft"})["missing"] == ("title",)
    assert wizards.validate_step("BookCreate", "optional", {"status": "bad"})["invalid_choices"] == ("status",)
    assert wizards.wizard_progress("BookCreate", ("required",))["current"]["name"] == "optional"
    publish_wizard = wizards.wizard_plan("PublishWorkflow")
    assert publish_wizard["steps"][0]["source"] == "draft"
    assert publish_wizard["steps"][-1]["name"] == "complete"
    flow_export = json.loads((tmp_path / "automation" / "node-red" / "flows.json").read_text())
    assert node_red.event_topic("Book", "updated") == "Book.updated"
    assert node_red.webhook_plan("Book", "updated", "https://example.test")["url"] == (
        "https://example.test/appgen/book/updated"
    )
    assert node_red.workflow_event_topic("Publish", "draft", "published") == "workflow.Publish.draft.published"
    assert node_red.workflow_webhook_plan("Publish", "published", "archived", "https://example.test")["url"] == (
        "https://example.test/appgen/workflow/publish/published/archived"
    )
    validation = node_red.validate_flow_export(flow_export)
    assert validation["http_inputs"] == 8
    assert validation["runtime"]["service"] == "node-red"
    assert node_red.compose_service_plan()["ports"] == ("1880:1880",)
    assert node_red.runtime_readiness({"automation/node-red/flows.json", "docker-compose.yml"})["run"] == (
        "docker compose up node-red"
    )
    assert validation["workflow_events"] == (
        "workflow.Publish.draft.published",
        "workflow.Publish.published.archived",
    )
    quality = subprocess.run(
        [sys.executable, str(tmp_path / "scripts" / "appgen_quality.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "appgen quality passed" in quality.stdout
    config_values = config_admin.parse_config_assignments((tmp_path / "config.py").read_text())
    assert config_values["FAB_API_SHOW_STACKTRACE"] is True
    assert config_values["FAB_API_SWAGGER_UI"] is True
    assert set(config_admin.EDITABLE_CONFIG) == {
        "APP_NAME",
        "SECRET_KEY",
        "SQLALCHEMY_DATABASE_URI",
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        "FAB_API_SHOW_STACKTRACE",
        "FAB_API_SWAGGER_UI",
        "WTF_CSRF_ENABLED",
        "AUTH_ROLE_ADMIN",
        "AUTH_ROLE_PUBLIC",
        "SESSION_COOKIE_HTTPONLY",
        "SESSION_COOKIE_SAMESITE",
        "BABEL_DEFAULT_LOCALE",
        "BABEL_DEFAULT_TIMEZONE",
        "LANGUAGES",
    }
    assert config_admin.config_schema()["editable_count"] == len(config_admin.EDITABLE_CONFIG)
    assert {section["name"] for section in config_admin.config_sections(config_values)} == {
        "Application",
        "Database",
        "Security",
        "API",
        "Localization",
    }
    setup = config_admin.setup_checklist(config_values)
    assert any(task["key"] == "LANGUAGES" for task in setup["tasks"])
    assert config_admin.config_readiness(config_values)["ready"] is False
    assert "SECRET_KEY must be replaced before production." in config_admin.config_readiness(config_values)["blockers"]
    assert "APP_NAME=Library" in config_admin.env_template(config_values)
    updated_config = config_admin.replace_config_assignment(
        (tmp_path / "config.py").read_text(),
        "APP_NAME",
        "Library Admin",
    )
    assert "APP_NAME = 'Library Admin'" in updated_config
    updated_languages = config_admin.replace_config_assignment(
        (tmp_path / "config.py").read_text(),
        "LANGUAGES",
        {"en": {"flag": "us", "name": "English"}, "fr": {"flag": "fr", "name": "French"}},
    )
    compile(updated_languages, "config.py", "exec")
    assert "'fr': {'flag': 'fr', 'name': 'French'}" in updated_languages
    assert "enum Status { draft published archived }" in designer.dsl_from_manifest(manifest)
    assert "table Book" in designer.dsl_from_manifest(manifest)
    assert "internal_code: string hidden" in designer.dsl_from_manifest(manifest)
    assert "title: string required search" in designer.dsl_from_manifest(manifest)
    assert "Overview: title, status;" in designer.dsl_from_manifest(manifest)
    assert "@ summary TextArea 0 2 8 3;" in designer.dsl_from_manifest(manifest)
    assert "flow Publish" in designer.dsl_from_manifest(manifest)
    assert "rule PublishPolicy for Book" in designer.dsl_from_manifest(manifest)
    graph = designer.visual_model(manifest)
    assert any(node["id"] == "enum:Status" and node["kind"] == "enum" for node in graph["nodes"])
    assert any(edge["target"] == "enum:Status" and edge["kind"] == "choice" for edge in graph["edges"])
    assert any(node["id"] == "Book" and node["kind"] == "table" for node in graph["nodes"])
    assert any(edge["source"] == "Book" and edge["target"] == "Author" for edge in graph["edges"])
    erd = designer.erd_mermaid(manifest)
    assert erd.startswith("erDiagram\n")
    assert "Author ||--o{ Book : author" in erd
    relationships = designer.relationship_matrix(manifest)
    assert relationships[0]["source_table"] == "Book"
    assert relationships[0]["target_table"] == "Author"
    assert designer.schema_diagram_check(manifest)["ok"] is True
    table_patch = designer.table_proposal("Publisher")
    assert "table Publisher" in designer.proposal_to_dsl(manifest, table_patch)
    field_patch = designer.field_proposal("Book", "isbn", required=True, searchable=True)
    field_dsl = designer.proposal_to_dsl(manifest, field_patch)
    assert "isbn: string required search" in field_dsl
    diff = designer.schema_diff(manifest, designer.apply_proposal(manifest, field_patch))
    assert diff["format"] == "appgen.schema-diff.v1"
    assert diff["added_fields"][0]["field"] == "isbn"
    assert diff["destructive"] is False
    preview = designer.migration_preview(manifest, field_patch)
    assert preview["format"] == "appgen.migration-preview.v1"
    assert preview["operations"][0]["op"] == "add_column"
    assert "data_loss_check" in preview["checks"]
    relation_patch = designer.relationship_proposal("Book", "publisher_id", "Publisher", cardinality="many-to-one")
    assert relation_patch["preview"]["dbml"] == "Ref: Book.publisher_id > Publisher.id"
    relation_dsl = designer.proposal_to_dsl(manifest, relation_patch)
    assert "publisher_id: int -> Publisher.id [many-to-one]" in relation_dsl
    assert designer.migration_preview(manifest, relation_patch)["operations"][0]["op"] == "add_column"
    browser_patch = designer.proposal_from_payload(
        {"kind": "add_field", "table": "Book", "name": "subtitle", "type": "string", "searchable": True}
    )
    assert "subtitle: string search" in designer.proposal_to_dsl(manifest, browser_patch)
    browser_relation = designer.proposal_from_payload(
        {"kind": "add_relationship", "source_table": "Book", "source_field": "editor_id", "target_table": "Author"}
    )
    assert browser_relation["relation"]["target_column"] == "id"
    flow_patch = designer.flow_step_proposal("Publish", "review", "approved")
    assert "review -> approved;" in designer.proposal_to_dsl(manifest, flow_patch)
    state = designer.designer_state(manifest)
    assert state["graph"]["nodes"]
    assert state["dsl"].startswith("app Library")
    assert "script_location = migrations" in (tmp_path / "alembic.ini").read_text()


def test_appgen_dsl_supports_groups_arrays_and_derived_fields(tmp_path) -> None:
    """The compact DSL supports reusable field groups, arrays, and derived fields."""
    dsl_path = tmp_path / "orders.ags"
    dsl_path.write_text(
        """
        app Orders

        AuditFields {
          created_at: datetime
          tags: string[]
        }

        table Order {
          id: int pk
          ...AuditFields
          subtotal: decimal required
          tax: decimal default 0
          total: decimal = subtotal + tax
        }
        """
    )

    schema = load_schema(dsl_path, source_type="dsl")
    order = schema.table("Order")
    columns = {column.name: column for column in order.columns}

    assert columns["created_at"].source_group == "AuditFields"
    assert columns["tags"].type_name == "string[]"
    assert columns["tags"].source_group == "AuditFields"
    assert columns["total"].derived is True
    assert columns["total"].hidden is True
    assert columns["total"].expression == "subtotal+tax"

    output_dir = tmp_path / "app"
    generate_app_from_schema(schema, output_dir)

    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)
    py_compile.compile(str(output_dir / "gql.py"), doraise=True)
    py_compile.compile(str(output_dir / "reports.py"), doraise=True)
    py_compile.compile(str(output_dir / "report_delivery.py"), doraise=True)
    py_compile.compile(str(output_dir / "backup.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_access.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_exchange.py"), doraise=True)
    py_compile.compile(str(output_dir / "designer.py"), doraise=True)

    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_order = next(table for table in manifest["tables"] if table["name"] == "Order")
    manifest_columns = {column["name"]: column for column in manifest_order["columns"]}
    assert manifest_columns["tags"]["source_group"] == "AuditFields"
    assert manifest_columns["total"]["derived"] is True
    assert manifest_columns["total"]["expression"] == "subtotal+tax"
    model_lines = (output_dir / "models.py").read_text().splitlines()
    assert any(line.strip().startswith("tags = Column(Text") for line in model_lines)
    assert not any(line.strip().startswith("total = Column") for line in model_lines)
    assert "include_columns = ['id', 'created_at', 'tags', 'subtotal', 'tax']" in (
        output_dir / "api.py"
    ).read_text()
    assert "subtotal+tax" in (tmp_path / "docs" / "schema.md").read_text()
    designer = _load_module(output_dir / "designer.py", "orders_designer")
    assert "total: decimal = subtotal+tax hidden" in designer.dsl_from_manifest(manifest)


def test_appgen_dsl_prefers_arrow_references_and_keeps_keyword_budget(tmp_path) -> None:
    """References use arrow syntax so the core DSL keyword list stays small."""
    dsl_path = tmp_path / "relations.ags"
    dsl_path.write_text(
        """
        # App-level notes are ignored by the parser.
        app Relations

        table Author {
          id: int pk
          name: string required
        }

        /* Field comments can explain relationship intent without changing output. */
        table Book {
          id: int pk
          title: string required
          author_id: int -> Author.id [many-to-one]
        }

        table AuthorProfile {
          id: int pk
          author_id: int -> Author.id [one-to-one]
        }

        table Review {
          id: int pk
          book_id: int required
          rating: int
        }

        // External relations can be documented inline too.
        Review.book_id -> Book.id [many-to-one]
        """
    )

    schema = load_schema(dsl_path, source_type="dsl")
    book = schema.table("Book")
    profile = schema.table("AuthorProfile")
    review = schema.table("Review")
    book_columns = {column.name: column for column in book.columns}
    profile_columns = {column.name: column for column in profile.columns}
    review_columns = {column.name: column for column in review.columns}
    relation_cardinality = {
        (relation.source_table, relation.source_column): relation.cardinality
        for relation in schema.relations
    }

    assert book_columns["author_id"].references == ("Author", "id")
    assert profile_columns["author_id"].references == ("Author", "id")
    assert review_columns["book_id"].references == ("Book", "id")
    assert {relation.source_table for relation in schema.relations} == {"Book", "AuthorProfile", "Review"}
    assert relation_cardinality[("Book", "author_id")] == "many-to-one"
    assert relation_cardinality[("AuthorProfile", "author_id")] == "one-to-one"
    assert relation_cardinality[("Review", "book_id")] == "many-to-one"

    schema_for_export = replace(
        schema,
        relations=(
            *schema.relations,
            RelationSchema(
                source_table="Book",
                source_column="id",
                target_table="Review",
                target_column="book_id",
                cardinality="one-to-many",
            ),
        ),
    )
    output_dir = tmp_path / "app"
    generate_app_from_schema(schema_for_export, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())
    manifest_cardinality = {
        (relation["source_table"], relation["source_column"]): relation["cardinality"]
        for relation in manifest["relations"]
    }
    assert manifest_cardinality[("AuthorProfile", "author_id")] == "one-to-one"
    jhipster = _load_module(tmp_path / "jhipster" / "appgen_jhipster.py", "cardinality_jhipster")
    jdl_text = (tmp_path / "jhipster" / "app.jdl").read_text()
    assert "relationship ManyToOne" in jdl_text
    assert "relationship OneToOne" in jdl_text
    assert "relationship OneToMany" in jdl_text
    assert "AuthorProfile{author} to Author" in jdl_text
    assert "Book{reviews} to Review{book}" in jdl_text
    jhipster_relationships = {
        (relationship["source"], relationship["field"]): relationship
        for relationship in jhipster.jhipster_relationships()
    }
    assert jhipster_relationships[("AuthorProfile", "author")]["type"] == "OneToOne"
    assert jhipster_relationships[("AuthorProfile", "author")]["cardinality"] == "one-to-one"
    assert any(
        relationship["type"] == "OneToMany" and relationship["target_column"] == "book_id"
        for relationship in jhipster.jhipster_relationships()
    )

    grammar = (Path(__file__).resolve().parents[1] / "lang" / "appgen.g4").read_text()
    keyword_tokens = set(re.findall(r"^([A-Z_]+)\s+:\s+'[a-z_][a-z0-9_]*'", grammar, flags=re.M))
    core_keywords = {
        "APP",
        "TABLE",
        "ENUM",
        "VIEW",
        "FOR",
        "FLOW",
        "ROLE",
        "RULE",
        "LLM",
        "AGENT",
        "PK",
        "REQUIRED",
        "UNIQUE",
        "HIDE",
        "SEARCH",
        "DEFAULT",
        "IN",
    }
    assert core_keywords <= keyword_tokens
    assert len(core_keywords) <= 17
    assert "| ARROW target relationCardinality?" in grammar
    assert "relationCardinality" in grammar
    assert "componentPlacement" in grammar
    assert "AT IDENT IDENT INT INT INT INT" in grammar
    assert "agenticOption" in grammar
    assert "IDENT COLON agenticValue" in grammar
    assert "agenticValue" in grammar


def test_appgen_dsl_accepts_authoring_aliases_without_new_keywords(tmp_path) -> None:
    """Beginner-friendly aliases normalize before ANTLR while the grammar stays compact."""
    dsl_path = tmp_path / "aliases.ags"
    dsl_path.write_text(
        """
        app AliasDemo { targets: web, mobile }

        entity Customer {
          id: int pk
          name: string required search
        }

        model Invoice {
          id: int pk
          customer_id: int required -> Customer.id [many-to-one]
          total: decimal required searchable
          internal_note: string hide
        }

        form InvoiceForm for Invoice {
          Main: customer_id, total;
          @ customer_id Lookup 0 0 6 1;
        }

        workflow Collect {
          draft -> sent
          sent -> paid
        }
        """
    )

    schema = load_schema(dsl_path, source_type="dsl")
    invoice_columns = {column.name: column for column in schema.table("Invoice").columns}
    assert schema.table("Customer").columns[1].name == "name"
    assert invoice_columns["customer_id"].references == ("Customer", "id")
    assert invoice_columns["total"].searchable is True
    assert invoice_columns["internal_note"].hidden is True
    assert schema.views[0].name == "InvoiceForm"
    assert schema.flows[0].name == "Collect"

    report = lint_dsl(dsl_path.read_text())
    assert report["ok"] is True
    assert any("canonical DSL words" in warning for warning in report["warnings"])
    fixed = apply_lint_fixes(dsl_path.read_text())
    assert "entity " not in fixed["fixed"]
    assert "model " not in fixed["fixed"]
    assert "form " not in fixed["fixed"]
    assert "workflow " not in fixed["fixed"]
    assert "searchable" not in fixed["fixed"]
    assert " hide" not in fixed["fixed"]
    assert "total: decimal required search" in fixed["fixed"]
    assert "internal_note: string hidden" in fixed["fixed"]
    assert "table Customer" in fixed["fixed"]
    assert "table Invoice" in fixed["fixed"]
    assert "view InvoiceForm for Invoice" in fixed["fixed"]
    assert "flow Collect" in fixed["fixed"]

    grammar = (Path(__file__).resolve().parents[1] / "lang" / "appgen.g4").read_text()
    assert "ENTITY" not in grammar
    assert "FORM" not in grammar
    assert "WORKFLOW" not in grammar


def test_generated_reports_cover_join_and_three_way_table_sets(tmp_path) -> None:
    """Report generation includes table, join, and three-table relation reports."""
    dsl_path = tmp_path / "reporting.ags"
    dsl_path.write_text(
        """
        app Reporting

        table Author {
          id: int pk
          name: string required search
        }

        table Book {
          id: int pk
          title: string required search
          author_id: int required -> Author.id
        }

        table Review {
          id: int pk
          book_id: int required -> Book.id
          rating: int required
        }
        """
    )
    schema = load_schema(dsl_path, source_type="dsl")
    output_dir = tmp_path / "app"

    generate_app_from_schema(schema, output_dir)

    py_compile.compile(str(output_dir / "reports.py"), doraise=True)
    reports = _load_module(output_dir / "reports.py", "generated_relationship_reports")
    assert {item["kind"] for item in reports.all_report_catalog()} == {"table", "join", "three_way"}
    join_keys = reports.relationship_report_keys()
    assert any(key.endswith("__join") for key in join_keys)
    assert any(key.endswith("__three_way") for key in join_keys)
    join_report = next(report for report in reports.join_report_catalog() if report["tables"] == ("Book", "Author"))
    assert "Book.title" in join_report["columns"]
    assert "Author.name" in join_report["columns"]
    three_way = reports.three_way_report_catalog()[0]
    plan = reports.report_query_plan(three_way["key"])
    assert plan["kind"] == "three_way"
    assert plan["requires_join"] is True
    assert len(plan["tables"]) == 3
    csv_text = reports.relationship_rows_to_csv(
        join_report["key"],
        [{"Book": {"title": "Dune"}, "Author": {"name": "Frank Herbert"}}],
    )
    assert "Book.title" in csv_text
    assert "Author.name" in csv_text
    assert "Dune" in csv_text
    assert "Frank Herbert" in csv_text


def test_appgen_cli_generates_from_dsl(tmp_path, runner: CliRunner) -> None:
    """The public CLI accepts the AppGen DSL as a first-class source."""
    dsl_path = tmp_path / "tiny.ags"
    dsl_path.write_text(
        """
        app Tiny
        table Thing {
          id: int pk
          name: string required
        }
        """
    )
    output_dir = tmp_path / "app"

    result = runner.invoke(__main__.main, ["--dsl", str(dsl_path), "-w", str(output_dir)])

    assert result.exit_code == 0, result.output
    assert (output_dir / "appgen.json").exists()
    py_compile.compile(str(output_dir / "models.py"), doraise=True)
    py_compile.compile(str(output_dir / "api.py"), doraise=True)
    py_compile.compile(str(output_dir / "runtime_security.py"), doraise=True)
    py_compile.compile(str(output_dir / "reports.py"), doraise=True)
    py_compile.compile(str(output_dir / "dashboards.py"), doraise=True)
    py_compile.compile(str(output_dir / "search.py"), doraise=True)
    py_compile.compile(str(output_dir / "media.py"), doraise=True)
    py_compile.compile(str(output_dir / "documents.py"), doraise=True)
    py_compile.compile(str(output_dir / "inventory_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "finance_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "manufacturing_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "backup.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_access.py"), doraise=True)
    py_compile.compile(str(output_dir / "data_exchange.py"), doraise=True)
    py_compile.compile(str(output_dir / "monitoring.py"), doraise=True)
    py_compile.compile(str(output_dir / "resilience.py"), doraise=True)
    py_compile.compile(str(output_dir / "performance.py"), doraise=True)
    py_compile.compile(str(output_dir / "runtime_assurance.py"), doraise=True)
    py_compile.compile(str(output_dir / "rules.py"), doraise=True)
    py_compile.compile(str(output_dir / "config_admin.py"), doraise=True)
    py_compile.compile(str(output_dir / "integrations.py"), doraise=True)
    py_compile.compile(str(output_dir / "productivity.py"), doraise=True)
    py_compile.compile(str(output_dir / "lifecycle.py"), doraise=True)
    py_compile.compile(str(output_dir / "tenancy.py"), doraise=True)
    py_compile.compile(str(output_dir / "rls.py"), doraise=True)
    py_compile.compile(str(output_dir / "identity.py"), doraise=True)
    py_compile.compile(str(output_dir / "compliance.py"), doraise=True)
    py_compile.compile(str(output_dir / "assistant.py"), doraise=True)
    py_compile.compile(str(output_dir / "intelligence.py"), doraise=True)
    py_compile.compile(str(output_dir / "chatbot.py"), doraise=True)
    py_compile.compile(str(output_dir / "voice.py"), doraise=True)
    py_compile.compile(str(output_dir / "i18n.py"), doraise=True)
    py_compile.compile(str(output_dir / "text_quality.py"), doraise=True)
    py_compile.compile(str(output_dir / "notifications.py"), doraise=True)
    py_compile.compile(str(output_dir / "platforms.py"), doraise=True)
    py_compile.compile(str(output_dir / "microservices.py"), doraise=True)
    py_compile.compile(str(tmp_path / "sdks" / "appgen_sdks.py"), doraise=True)
    py_compile.compile(str(tmp_path / "sdks" / "python" / "client.py"), doraise=True)
    py_compile.compile(str(output_dir / "collaboration.py"), doraise=True)
    py_compile.compile(str(output_dir / "realtime.py"), doraise=True)
    py_compile.compile(str(output_dir / "events.py"), doraise=True)
    py_compile.compile(str(output_dir / "rpa.py"), doraise=True)
    py_compile.compile(str(output_dir / "diagnostics.py"), doraise=True)
    py_compile.compile(str(output_dir / "api_testing.py"), doraise=True)
    py_compile.compile(str(output_dir / "code_review.py"), doraise=True)
    py_compile.compile(str(output_dir / "report_delivery.py"), doraise=True)
    py_compile.compile(str(output_dir / "components.py"), doraise=True)
    py_compile.compile(str(output_dir / "wizards.py"), doraise=True)
    py_compile.compile(str(output_dir / "search.py"), doraise=True)
    py_compile.compile(str(output_dir / "usage_analytics.py"), doraise=True)
    py_compile.compile(str(output_dir / "media.py"), doraise=True)
    py_compile.compile(str(output_dir / "documents.py"), doraise=True)
    py_compile.compile(str(output_dir / "inventory_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "finance_ops.py"), doraise=True)
    py_compile.compile(str(output_dir / "manufacturing_ops.py"), doraise=True)
    py_compile.compile(str(tmp_path / "seed.py"), doraise=True)
    assert (tmp_path / "docs" / "schema.md").exists()
    assert (tmp_path / "config.py").exists()
    assert (tmp_path / "README.md").exists()


def test_appgen_dsl_targets_select_generated_platform_contracts(tmp_path) -> None:
    """The DSL can select generated web, mobile, and desktop application targets."""
    dsl_path = tmp_path / "targets.ags"
    dsl_path.write_text(
        """
        app Targeted { targets: web, mobile, desktop }

        table Task {
          id: int pk
          title: string required search
        }
        """
    )
    schema = load_schema(dsl_path, source_type="dsl")
    output_dir = tmp_path / "app"

    assert schema.app_options["targets"] == "web,mobile,desktop"

    generate_app_from_schema(schema, output_dir)
    manifest = json.loads((output_dir / "appgen.json").read_text())

    py_compile.compile(str(output_dir / "platforms.py"), doraise=True)
    py_compile.compile(str(tmp_path / "frontends" / "appgen_frontends.py"), doraise=True)
    py_compile.compile(str(tmp_path / "native" / "appgen_native.py"), doraise=True)
    py_compile.compile(str(tmp_path / "chatbots" / "appgen_chatbots.py"), doraise=True)
    platforms = _load_module(output_dir / "platforms.py", "targeted_platforms")
    frontends = _load_module(tmp_path / "frontends" / "appgen_frontends.py", "targeted_frontends")
    native = _load_module(tmp_path / "native" / "appgen_native.py", "targeted_native")
    chatbots = _load_module(tmp_path / "chatbots" / "appgen_chatbots.py", "targeted_chatbots")

    assert platforms.selected_platform_targets() == ("web", "mobile", "desktop")
    assert manifest["platform_targets"] == ["web", "mobile", "desktop"]
    assert manifest["unknown_platform_targets"] == []
    assert {item["target"] for item in platforms.platform_catalog()} == {"web", "mobile", "desktop"}
    assert set(platforms.generation_matrix()) == {"web", "mobile", "desktop"}
    assert platforms.platform_contract("pwa")["selected"] is False
    assert set(frontends.frontend_targets()) == {"react", "vue", "angular", "svelte", "htmx", "express"}
    assert frontends.frontend_plan("react")["selected"] is True
    assert set(native.native_targets()) == {"mobile", "desktop"}
    assert native.native_plan("mobile")["selected"] is True
    assert chatbots.chatbot_targets() == ()


def test_appgen_dsl_rejects_unknown_platform_targets(tmp_path) -> None:
    """Invalid target names fail at parse time instead of being silently ignored."""
    dsl_path = tmp_path / "bad-target.ags"
    dsl_path.write_text(
        """
        app BadTarget { targets: web, toaster }

        table Task {
          id: int pk
          title: string required
        }
        """
    )

    with pytest.raises(ValueError, match="Unknown app targets: toaster"):
        load_schema(dsl_path, source_type="dsl")


def test_appgen_dsl_rejects_broken_semantic_references(tmp_path) -> None:
    """The DSL reports broken references before generating inconsistent apps."""
    dsl_path = tmp_path / "broken.ags"
    dsl_path.write_text(
        """
        app Broken

        table Book {
          id: int pk
          title: string required
          author_id: int -> Author.id
          label: string = title + missing_label
        }

        view BookForm for Book {
          Main: title, missing_field;
          @ missing_field TextBox 0 0 4 1;
        }

        role Editor {
          Missing: read;
        }

        rule BrokenRule for Book {
          missing_field required;
        }

        llm LocalModel {
          provider: ollama
          mode: local
        }

        agent Publisher {
          provider: CloudModel
        }
        """
    )

    with pytest.raises(ValueError) as excinfo:
        load_schema(dsl_path, source_type="dsl")

    message = str(excinfo.value)
    assert "Unknown reference target table: Author" in message
    assert "Unknown derived-field reference: Book.label uses missing_label" in message
    assert "Unknown view field: BookForm.missing_field" in message
    assert "Unknown role resource: Editor.Missing" in message
    assert "Unknown rule field: BrokenRule.missing_field" in message
    assert "Unknown agent provider: Publisher.CloudModel" in message


def test_appgen_dsl_rejects_duplicate_declarations_but_allows_group_overrides(tmp_path) -> None:
    """Duplicate DSL declarations fail unless a local field overrides a spread group field."""
    override_path = tmp_path / "override.ags"
    override_path.write_text(
        """
        app Override

        AuditFields {
          status: string
          created_at: datetime
        }

        table Task {
          id: int pk
          ...AuditFields
          status: string required search
        }
        """
    )
    schema = load_schema(override_path, source_type="dsl")
    task_columns = {column.name: column for column in schema.table("Task").columns}
    assert task_columns["status"].source_group is None
    assert task_columns["status"].nullable is False
    assert task_columns["created_at"].source_group == "AuditFields"

    duplicate_field_path = tmp_path / "duplicate-field.ags"
    duplicate_field_path.write_text(
        """
        app DuplicateField

        table Task {
          id: int pk
          title: string
          title: text
        }
        """
    )

    with pytest.raises(ValueError, match="Duplicate field declaration: Task.title"):
        load_schema(duplicate_field_path, source_type="dsl")

    duplicate_decl_path = tmp_path / "duplicate-declarations.ags"
    duplicate_decl_path.write_text(
        """
        app DuplicateDeclarations

        table Task {
          id: int pk
          title: string
        }

        table Task {
          id: int pk
          title: string
        }

        view TaskForm for Task {
          title;
        }

        view TaskForm for Task {
          title;
        }
        """
    )

    with pytest.raises(ValueError) as excinfo:
        load_schema(duplicate_decl_path, source_type="dsl")

    message = str(excinfo.value)
    assert "Duplicate table declaration: Task" in message
    assert "Duplicate view declaration: TaskForm" in message


def test_generated_tenancy_helpers_detect_tenant_columns(tmp_path) -> None:
    """Generated tenancy helpers expose scoped tables and filter kwargs."""
    dsl_path = tmp_path / "tenant.ags"
    dsl_path.write_text(
        """
        app TenantApp

        table Project {
          id: int pk
          tenant_id: string required search
          name: string required
        }

        role ProjectManager {
          Project: read, update;
        }
        """
    )
    schema = load_schema(dsl_path, source_type="dsl")
    output_dir = tmp_path / "app"

    generate_app_from_schema(schema, output_dir)

    py_compile.compile(str(output_dir / "tenancy.py"), doraise=True)
    py_compile.compile(str(output_dir / "rls.py"), doraise=True)
    tenancy = _load_module(output_dir / "tenancy.py", "tenant_helpers")
    rls = _load_module(output_dir / "rls.py", "tenant_rls_helpers")
    catalog = tenancy.tenant_catalog()
    assert catalog[0]["table"] == "Project"
    assert catalog[0]["scoped"] is True
    assert catalog[0]["tenant_columns"] == ("tenant_id",)
    assert tenancy.is_tenant_scoped("Project") is True
    assert tenancy.tenant_filter_kwargs("Project", "acme") == {"tenant_id": "acme"}
    assert rls.table_policy("Project")["tenant_column"] == "tenant_id"
    assert rls.rls_filter_kwargs("Project", {"tenant_id": "acme"}) == {"tenant_id": "acme"}
    assert rls.can_access_row("Project", {"tenant_id": "acme", "name": "A"}, {"tenant_id": "acme"}) is True
    assert rls.can_access_row("Project", {"tenant_id": "other", "name": "B"}, {"tenant_id": "acme"}) is False
    assert rls.bypasses_rls("Project", {"roles": ["Admin"]}) is True
    assert rls.filter_rows(
        "Project",
        [{"tenant_id": "acme", "name": "A"}, {"tenant_id": "other", "name": "B"}],
        {"tenant_id": "acme"},
    ) == ({"tenant_id": "acme", "name": "A"},)
    sql = rls.postgres_policy_sql("Project")
    assert "ALTER TABLE \"Project\" ENABLE ROW LEVEL SECURITY;" in sql
    assert "current_setting('appgen.tenant_id', true)" in sql
    assert "Project" in rls.postgres_all_policy_sql()
    assert rls.postgres_role_name("ProjectManager") == "appgen_projectmanager"
    assert rls.postgres_set_tenant_sql("acme") == "SELECT set_config('appgen.tenant_id', 'acme', true);"
    sync_plan = rls.postgres_role_sync_plan(
        ({"username": "ada", "roles": ["ProjectManager"], "tenant_id": "acme"},)
    )
    assert sync_plan["roles"][0]["database_role"] == "appgen_projectmanager"
    assert sync_plan["users"][0]["grants"] == ("appgen_projectmanager",)
    sync_sql = rls.postgres_role_sync_sql(
        ({"username": "ada", "roles": ["ProjectManager"], "tenant_id": "acme"},),
        create_login_roles=True,
    )
    assert 'CREATE ROLE "appgen_projectmanager" NOLOGIN;' in sync_sql
    assert 'CREATE ROLE "ada" LOGIN;' in sync_sql
    assert 'GRANT "appgen_projectmanager" TO "ada";' in sync_sql
    with pytest.raises(PermissionError, match="Tenant context required"):
        tenancy.require_tenant("Project", None)
    with pytest.raises(PermissionError, match="Tenant context required"):
        rls.rls_filter_kwargs("Project", {})
    with pytest.raises(ValueError, match="Tenant id is required"):
        rls.postgres_set_tenant_sql("")


def test_appgen_dsl_supports_explicit_rls_targets_without_new_keywords(tmp_path) -> None:
    """App options can declare RLS fields even when names do not match tenant conventions."""
    dsl_path = tmp_path / "explicit_rls.ags"
    dsl_path.write_text(
        """
        app TenantApp { rls: Project.org_id; targets: web, mobile, desktop }

        table Project {
          id: int pk
          org_id: string required search
          name: string required
        }

        table Task {
          id: int pk
          project_id: int required -> Project.id
          title: string required
        }
        """
    )

    lint = lint_dsl(dsl_path.read_text(), source_name=str(dsl_path))
    assert lint["ok"] is True
    schema = load_schema(dsl_path, source_type="dsl")
    assert schema.app_options["rls"] == "Project.org_id"
    output_dir = tmp_path / "app"

    generate_app_from_schema(schema, output_dir)

    py_compile.compile(str(output_dir / "tenancy.py"), doraise=True)
    py_compile.compile(str(output_dir / "rls.py"), doraise=True)
    tenancy = _load_module(output_dir / "tenancy.py", "explicit_tenant_helpers")
    rls = _load_module(output_dir / "rls.py", "explicit_rls_helpers")
    catalog = {item["table"]: item for item in tenancy.tenant_catalog()}
    assert catalog["Project"]["scoped"] is True
    assert catalog["Project"]["tenant_columns"] == ("org_id",)
    assert catalog["Project"]["tenant_source"] == "explicit"
    assert catalog["Task"]["scoped"] is False
    assert rls.table_policy("Project")["tenant_column"] == "org_id"
    assert rls.table_policy("Project")["tenant_source"] == "explicit"
    assert rls.rls_filter_kwargs("Project", {"tenant_id": "acme"}) == {"org_id": "acme"}
    assert rls.can_access_row("Project", {"org_id": "acme"}, {"tenant_id": "acme"}) is True
    assert rls.can_access_row("Project", {"org_id": "other"}, {"tenant_id": "acme"}) is False
    assert "org_id" in rls.postgres_policy_sql("Project")


def test_appgen_dsl_rejects_unknown_explicit_rls_targets(tmp_path) -> None:
    """Explicit RLS targets are validated against generated schema fields."""
    dsl_path = tmp_path / "broken_rls.ags"
    dsl_path.write_text(
        """
        app TenantApp { rls: Project.organization_id }

        table Project {
          id: int pk
          org_id: string required
        }
        """
    )

    with pytest.raises(ValueError, match="Unknown RLS target field: Project.organization_id"):
        load_schema(dsl_path, source_type="dsl")


def _load_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
