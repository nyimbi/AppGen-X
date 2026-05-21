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
from pyAppGen.schema import load_schema
from pyAppGen.schema import RelationSchema
from pyAppGen.schema import schema_from_metadata


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


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
        output_dir / "health.py",
        output_dir / "monitoring.py",
        output_dir / "resilience.py",
        output_dir / "performance.py",
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
        output_dir / "designer.py",
        output_dir / "form_designer.py",
        output_dir / "nl_evolution.py",
        output_dir / "dsl_reference.py",
        output_dir / "view_experience.py",
        output_dir / "support_center.py",
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
    assert (output_dir / "templates" / "appgen_monitoring.html").exists()
    assert (output_dir / "templates" / "appgen_resilience.html").exists()
    assert (output_dir / "templates" / "appgen_rules.html").exists()
    assert (output_dir / "templates" / "appgen_performance.html").exists()
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
    assert (tmp_path / "deploy" / "terraform-aws.tf").exists()
    assert (tmp_path / "deploy" / "terraform-gcp.tf").exists()
    assert (tmp_path / "deploy" / "terraform-azure.tf").exists()
    assert (tmp_path / "frontends" / "appgen_frontends.py").exists()
    assert (tmp_path / "frontends" / "react" / "src" / "App.jsx").exists()
    assert (tmp_path / "frontends" / "vue" / "src" / "App.vue").exists()
    assert (tmp_path / "frontends" / "angular" / "src" / "app.component.ts").exists()
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
    compose_text = (tmp_path / "docker-compose.yml").read_text()
    assert "caddy:2" in compose_text
    assert "443:443" in compose_text
    caddy_text = (tmp_path / "deploy" / "Caddyfile").read_text()
    assert "reverse_proxy web:8080" in caddy_text
    assert "Strict-Transport-Security" in caddy_text
    assert 'target   = "aws"' in (tmp_path / "deploy" / "terraform-aws.tf").read_text()
    assert 'target   = "gcp"' in (tmp_path / "deploy" / "terraform-gcp.tf").read_text()
    assert 'target   = "azure"' in (tmp_path / "deploy" / "terraform-azure.tf").read_text()
    deployment = _load_module(tmp_path / "deploy" / "appgen_deploy.py", "generated_deployment")
    https = _load_module(tmp_path / "deploy" / "appgen_https.py", "generated_https")
    assert "kubernetes" in deployment.deployment_targets()
    assert "https" in deployment.deployment_targets()
    assert deployment.artifact_plan("aws") == ("deploy/terraform-aws.tf",)
    assert deployment.artifact_plan("https") == ("deploy/Caddyfile", "deploy/appgen_https.py")
    assert deployment.environment_status({"SECRET_KEY": "s", "SQLALCHEMY_DATABASE_URI": "sqlite://"})["configured"] is True
    all_artifacts = {
        "Dockerfile",
        "docker-compose.yml",
        "deploy/Caddyfile",
        "deploy/appgen_https.py",
        "deploy/k8s.yaml",
        "deploy/terraform-aws.tf",
        "deploy/terraform-gcp.tf",
        "deploy/terraform-azure.tf",
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
    assert set(frontends.frontend_targets()) == {"react", "vue", "angular", "express"}
    assert frontends.frontend_plan("react")["entry"] == "src/App.jsx"
    assert ("book", "/api/v1/book/") in frontends.api_routes()
    frontend_artifacts = {
        "frontends/react/package.json",
        "frontends/react/src/App.jsx",
        "frontends/vue/package.json",
        "frontends/vue/src/App.vue",
        "frontends/angular/package.json",
        "frontends/angular/src/app.component.ts",
        "frontends/express/package.json",
        "frontends/express/src/server.js",
    }
    assert frontends.scaffold_check(frontend_artifacts)["ok"] is True
    assert "/api/v1/book/" in (tmp_path / "frontends" / "react" / "src" / "App.jsx").read_text()
    assert "<template>" in (tmp_path / "frontends" / "vue" / "src" / "App.vue").read_text()
    assert "AppComponent" in (tmp_path / "frontends" / "angular" / "src" / "app.component.ts").read_text()
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
    assert mobile.mobile_contract()["framework"] == "kivy"
    assert mobile.offline_record("Book", {"title": "Dune"})["status"] == "queued"
    assert desktop.desktop_contract()["framework"] == "beeware"
    assert desktop.local_cache_plan("/tmp/cache")[1]["path"].endswith("/book.json")
    jhipster = _load_module(tmp_path / "jhipster" / "appgen_jhipster.py", "generated_jhipster")
    assert jhipster.jhipster_import_command() == ("jhipster", "jdl", "jhipster/app.jdl")
    assert jhipster.export_check({"jhipster/app.jdl", "jhipster/appgen_jhipster.py"})["ok"] is True
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
    flow_export = json.loads((tmp_path / "automation" / "node-red" / "flows.json").read_text())
    assert node_red.validate_flow_export(flow_export)["ok"] is True
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
    assert "Generated transition cockpit" in (output_dir / "templates" / "appgen_workflows.html").read_text()
    assert "FSM JSON" in (output_dir / "templates" / "appgen_workflows.html").read_text()
    assert "Export CSV" in (output_dir / "templates" / "appgen_reports.html").read_text()
    assert "Generated PDF export and email delivery contracts" in (
        output_dir / "templates" / "appgen_report_delivery.html"
    ).read_text()
    assert "Generated dashboard, KPI, and chart contracts" in (
        output_dir / "templates" / "appgen_dashboards.html"
    ).read_text()
    assert "app usage analytics" in (output_dir / "templates" / "appgen_usage_analytics.html").read_text()
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
    assert "Schema-aware CSV and JSON import/export" in (
        output_dir / "templates" / "appgen_data_exchange.html"
    ).read_text()
    assert "Migration batch planning" in (
        output_dir / "templates" / "appgen_data_exchange.html"
    ).read_text()
    assert "Database Operations" in (
        output_dir / "templates" / "appgen_database_ops.html"
    ).read_text()
    assert "Export all JSON" in (output_dir / "templates" / "appgen_backup.html").read_text()
    assert "Configuration" in (output_dir / "templates" / "appgen_config.html").read_text()
    assert "Salesforce" in (output_dir / "templates" / "appgen_integrations.html").read_text()
    assert "Entando" in (output_dir / "templates" / "appgen_integrations.html").read_text()
    assert "Invenio" in (output_dir / "templates" / "appgen_integrations.html").read_text()
    assert "Productivity Integrations" in (output_dir / "templates" / "appgen_productivity.html").read_text()
    assert "Lifecycle JSON" in (output_dir / "templates" / "appgen_lifecycle.html").read_text()
    assert "tenant_id" in (output_dir / "templates" / "appgen_tenancy.html").read_text()
    assert "row-level security contracts" in (output_dir / "templates" / "appgen_rls.html").read_text()
    assert "OpenID Connect" in (output_dir / "templates" / "appgen_identity.html").read_text()
    assert "protected-field" in (output_dir / "templates" / "appgen_compliance.html").read_text()
    assert "prediction features" in (output_dir / "templates" / "appgen_assistant.html").read_text()
    assert "Intelligence JSON" in (output_dir / "templates" / "appgen_intelligence.html").read_text()
    assert "Guided Chatbot" in (output_dir / "templates" / "appgen_chatbot.html").read_text()
    assert "Voice JSON" in (output_dir / "templates" / "appgen_voice.html").read_text()
    assert "Generated spell, grammar, and character-count contracts" in (
        output_dir / "templates" / "appgen_text_quality.html"
    ).read_text()
    assert "Generated notification channels" in (output_dir / "templates" / "appgen_notifications.html").read_text()
    assert "web, PWA, mobile, desktop, and chatbot" in (output_dir / "templates" / "appgen_platforms.html").read_text()
    assert "microservices architecture contract" in (output_dir / "templates" / "appgen_microservices.html").read_text()
    assert "class AppGenClient" in (tmp_path / "sdks" / "python" / "client.py").read_text()
    assert "export class AppGenClient" in (tmp_path / "sdks" / "javascript" / "client.js").read_text()
    assert "change proposals" in (output_dir / "templates" / "appgen_collaboration.html").read_text()
    assert "rollback" in (output_dir / "templates" / "appgen_version_control.html").read_text()
    assert "Visual Studio Code" in (output_dir / "templates" / "appgen_devtools.html").read_text()
    assert "JetBrains" in (output_dir / "templates" / "appgen_devtools.html").read_text()
    assert "Developer Studio" in (output_dir / "templates" / "appgen_studio.html").read_text()
    assert "event-stream contracts" in (output_dir / "templates" / "appgen_realtime.html").read_text()
    assert "permissions per tab" in (output_dir / "templates" / "appgen_tabbed_views.html").read_text()
    assert "complex event processing" in (output_dir / "templates" / "appgen_events.html").read_text()
    assert "RPA &amp; BPA" in (output_dir / "templates" / "appgen_rpa.html").read_text()
    assert "runtime self-tests" in (output_dir / "templates" / "appgen_diagnostics.html").read_text()
    assert "automated API testing" in (output_dir / "templates" / "appgen_api_testing.html").read_text()
    assert "Generated automated code-review findings" in (
        output_dir / "templates" / "appgen_code_review.html"
    ).read_text()
    assert "Generated component and widget contracts" in (
        output_dir / "templates" / "appgen_components.html"
    ).read_text()
    assert "Keyword Budget" in (output_dir / "templates" / "appgen_dsl_reference.html").read_text()
    assert "Reference JSON" in (output_dir / "templates" / "appgen_dsl_reference.html").read_text()
    assert "View Experience" in (output_dir / "templates" / "appgen_view_experience.html").read_text()
    assert "Presence JSON" in (output_dir / "templates" / "appgen_view_experience.html").read_text()
    assert "data-appgen-time-on-page" in (output_dir / "static" / "appgen-view-experience.js").read_text()
    assert "Support Center" in (output_dir / "templates" / "appgen_support_center.html").read_text()
    assert "Tutorials JSON" in (output_dir / "templates" / "appgen_support_center.html").read_text()
    assert "Prototype JSON" in (output_dir / "templates" / "appgen_prototyping.html").read_text()
    assert "Generated sequential user-input" in (output_dir / "templates" / "appgen_wizards.html").read_text()
    assert "Generated branding contract" in (output_dir / "templates" / "appgen_branding.html").read_text()
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
    extensions = _load_module(output_dir / "extensions.py", "generated_extensions")
    appgen_package = _load_module(tmp_path / "appgen_package.py", "generated_appgen_package")
    generated_coverage = _load_module(tmp_path / "tests" / "test_generated_coverage.py", "generated_test_coverage")
    node_red = _load_module(tmp_path / "automation" / "appgen_node_red.py", "generated_node_red_dsl")
    seed = _load_module(tmp_path / "seed.py", "generated_seed")
    assert security.can("Editor", "Book", "update") is True
    assert security.can("Editor", "Book", "delete") is False
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
    assert rules.rules_for_table("Book")[0]["name"] == "PublishPolicy"
    assert rules.validate_row("Book", {"status": "draft"})["errors"][0]["message"] == "Title is required"
    assert rules.validate_row("Book", {"title": "Dune", "status": "draft"})["ok"] is True
    assert rules.decision_plan("Book", {"title": "Dune", "status": "published"})["decisions"] == ("review",)
    assert rules.rules_check({"app/rules.py", "app/templates/appgen_rules.html"})["ok"] is True
    assert branding.theme_contract()["theme"] == "sage"
    assert branding.css_variables()["--appgen-primary"] == "#2f6f5e"
    assert branding.asset_check(
        {"app/branding.py", "app/static/appgen-theme.css", "app/templates/appgen_branding.html"}
    )["ok"] is True
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
    assert dashboards.dashboard_payload("Book", [{"title": "Dune"}])["charts"][0]["data"]["values"] == (1,)
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
    assert usage_analytics.usage_analytics_check(
        {"app/usage_analytics.py", "app/templates/appgen_usage_analytics.html"}
    )["ok"] is True
    search_catalog = search.search_catalog()
    assert any(item["table"] == "Book" and item["fields"] == ("title",) for item in search_catalog)
    assert search.search_index("Author")["fields"] == ("name",)
    assert search.provider_plan("elasticsearch", {})["missing"] == ("ELASTICSEARCH_URL",)
    assert search.provider_plan("whoosh", {"WHOOSH_INDEX_DIR": "/tmp/index"})["configured"] is True
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
    assert data_access.sanitize_write_payload("Book", {"title": "Dune"})["ok"] is True
    blocked_payload = data_access.sanitize_write_payload("Book", {"title": "Dune", "internal_code": "B-1"})
    assert blocked_payload["ok"] is False
    assert blocked_payload["unknown_fields"] == ("internal_code",)
    update_plan = data_access.mutation_plan("Book", "update", {"id": 1, "title": "Dune Messiah"}, actor="ada")
    assert update_plan["ok"] is True
    assert update_plan["identity"] == {"id": 1}
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
    bad_payload = {
        "format": "appgen.backup.v1",
        "tables": [{"table": "Book", "columns": ["id"], "rows": []}],
    }
    with pytest.raises(ValueError, match="Column mismatch"):
        backup.validate_backup_payload(bad_payload)
    assert seed.SEED_DATA["Book"][0]["title"] == "Sample Title"
    assert "internal_code" not in seed.SEED_DATA["Book"][0]
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
    principal = identity.normalize_principal({"sub": "u1", "email": "ada@example.test", "roles": ["Editor"]})
    assert principal["username"] == "ada@example.test"
    assert principal["roles"] == ("Editor",)
    ad_principal = identity.normalize_principal({"sAMAccountName": "ada", "mail": "ada@example.test", "groups": ["ERP"]})
    assert ad_principal["username"] == "ada"
    assert ad_principal["email"] == "ada@example.test"
    assert ad_principal["roles"] == ("ERP",)
    assert compliance.protected_fields("Book") == ("internal_code",)
    assert compliance.redact_row("Book", {"title": "Dune", "internal_code": "B-1"})["internal_code"] == "[redacted]"
    audit = compliance.audit_event("read", "Book", actor="ada", tenant_id="acme")
    assert audit["action"] == "read"
    assert audit["tenant_id"] == "acme"
    assert compliance.retention_policy("Book")["retention_days"] == 365
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
    assert {item["target"] for item in platforms.platform_catalog()} == {"web", "pwa", "mobile", "desktop", "chatbot"}
    mobile_contract = platforms.platform_contract("mobile")
    assert "camera" in mobile_contract["capabilities"]
    assert {"web", "mobile", "desktop"} == set(platforms.generation_matrix())
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
    assert microservices.microservice_check(
        {"app/microservices.py", "app/templates/appgen_microservices.html", "deploy/k8s.yaml"}
    )["ok"] is True
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
    assert studio.studio_check({"app/studio.py", "app/templates/appgen_studio.html"})["ok"] is True
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
    assert diagnostics.validate_row("Book", {"status": "draft"})["missing"] == ("title",)
    snapshot = diagnostics.debug_snapshot(
        {"SECRET_KEY": "secret", "APP_NAME": "Library"},
        {"PATH": "/usr/bin"},
    )
    assert snapshot["config"]["SECRET_KEY"] == "[redacted]"
    assert snapshot["config"]["APP_NAME"] == "Library"
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
    assert api_testing.contract_coverage(openapi.openapi_spec()["paths"].keys())["ok"] is True
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
    assert dsl_reference.dsl_keyword_budget()["count"] <= dsl_reference.dsl_keyword_budget()["limit"]
    assert "[cardinality] relation metadata" in dsl_reference.dsl_keyword_budget()["keyword_free_syntax"]
    assert "Reference" in {item["name"] for item in dsl_reference.dsl_construct_catalog()}
    assert "author_id: int -> Author.id [many-to-one]" in dsl_reference.dsl_example("relation")
    assert dsl_reference.dsl_lint(dsl_reference.dsl_example("full"))["ok"] is True
    assert dsl_reference.dsl_lint(
        "table Book { author_id: int -> Author.id [one2one] }"
    )["errors"]
    assert dsl_reference.dsl_lint("table Book { author_id: int ref Author.id }")["warnings"]
    assert dsl_reference.dsl_lint("app Bad { targets: web, toaster } table Book { title: string }")["errors"]
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
    assert erp_templates.erp_templates_check(
        {"app/erp_templates.py", "app/templates/appgen_erp_templates.html"}
    )["ok"] is True
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
    browser_patch = designer.proposal_from_payload(
        {"kind": "add_field", "table": "Book", "name": "subtitle", "type": "string", "searchable": True}
    )
    assert "subtitle: string search" in designer.proposal_to_dsl(manifest, browser_patch)
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
    assert set(frontends.frontend_targets()) == {"react", "vue", "angular", "express"}
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
    with pytest.raises(PermissionError, match="Tenant context required"):
        tenancy.require_tenant("Project", None)
    with pytest.raises(PermissionError, match="Tenant context required"):
        rls.rls_filter_kwargs("Project", {})


def _load_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
