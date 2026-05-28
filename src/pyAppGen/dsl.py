"""ANTLR-backed parser for the AppGen low-code DSL."""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable

from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from .schema import AppSchema
from .schema import AgentSchema
from .schema import ColumnSchema
from .schema import DeploymentHealthSchema
from .schema import DeploymentScaleSchema
from .schema import DeploymentUnitSchema
from .schema import EnumSchema
from .schema import EnterpriseContractSchema
from .schema import EnterpriseStatementSchema
from .schema import FormComponentSchema
from .schema import FlowSchema
from .schema import FlowStepSchema
from .schema import HandlerSchema
from .schema import LLMProviderSchema
from .schema import PermissionSchema
from .schema import PlatformBlockSchema
from .schema import RelationSchema
from .schema import RuleConditionSchema
from .schema import RuleSchema
from .schema import RoleSchema
from .schema import SUPPORTED_SCHEMA_SOURCES
from .schema import TableSchema
from .schema import TableDirectiveSchema
from .schema import ViewSchema
from .schema import ViewSectionSchema
from .schema import normalize_platform_targets


_GENERATED_DIR = Path(__file__).resolve().parent / "dsl_generated" / "lang"
if str(_GENERATED_DIR) not in sys.path:
    sys.path.insert(0, str(_GENERATED_DIR))

from appgenLexer import appgenLexer  # type: ignore  # noqa: E402
from appgenParser import appgenParser  # type: ignore  # noqa: E402


REQUIRED_GRAPH_KINDS = (
    "er",
    "lookup",
    "workflow",
    "handler",
    "pbc",
    "security",
    "agent",
    "deployment",
    "package",
)
GRAPH_TEXT_FORMATS = ("json", "mermaid", "dot")


class AppGenSyntaxError(ValueError):
    """Raised when AppGen DSL parsing fails."""


class _CollectingErrorListener(ErrorListener):
    def __init__(self) -> None:
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # noqa: N802
        self.errors.append(f"{line}:{column}: {msg}")


def schema_from_dsl_file(path: str | Path) -> AppSchema:
    path = Path(path)
    return schema_from_dsl(path.read_text(), source_name=str(path))


def lint_dsl_file(path: str | Path) -> dict:
    """Lint an AppGen DSL file without generating an application."""
    path = Path(path)
    return lint_dsl(path.read_text(), source_name=str(path))


def fix_dsl_file(path: str | Path, *, fix_ids: Iterable[str] | None = None) -> dict:
    """Apply safe linter quick fixes to an AppGen DSL file."""
    path = Path(path)
    result = apply_lint_fixes(path.read_text(), fix_ids=fix_ids, source_name=str(path))
    if result["changed"]:
        path.write_text(result["fixed"])
    return result


def format_dsl_file(path: str | Path) -> dict:
    """Format an AppGen DSL file in place and return before/after metadata."""
    path = Path(path)
    result = format_dsl(path.read_text(), source_name=str(path))
    if result["changed"]:
        path.write_text(result["formatted"])
    return result


def lint_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return syntax, semantic, and style feedback for AppGen DSL source."""
    source = text or ""
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []
    schema: AppSchema | None = None

    if not source.strip():
        errors.append("DSL source is empty.")
    if source.count("{") != source.count("}"):
        errors.append("Unbalanced braces: every block opened with { must close with }.")
    if re.search(r"\bref\b", source):
        warnings.append("Prefer arrow references, for example author_id: int -> Author.id.")
    if re.search(r"api_key\s*:\s*['\"]", source):
        warnings.append("Use an environment variable name for api_key, not a literal secret.")
    if _uses_authoring_aliases(source):
        warnings.append("Use canonical DSL words in committed source: table, view, and flow.")
    if _uses_modifier_aliases(source):
        warnings.append("Use canonical DSL modifier words in committed source: hidden and search.")
    if re.search(r"\brelationship\b|\bcomponent\b", source, re.I) or (
        re.search(r"\bentity\b", source, re.I) and not _uses_authoring_aliases(source)
    ):
        suggestions.append(
            "Use compact DSL constructs such as table, view, flow, rule, llm, and agent."
        )
    errors.extend(_preparse_tooling_errors(source))

    if not errors:
        try:
            schema = schema_from_dsl(source, source_name=source_name)
        except AppGenSyntaxError as exc:
            errors.extend(part.strip() for part in str(exc).split(";") if part.strip())
            suggestions.extend(_semantic_suggestions(source, errors))

    if schema is not None:
        policy_errors, policy_warnings = _tooling_policy_diagnostics(schema)
        errors.extend(policy_errors)
        warnings.extend(policy_warnings)
        if not schema.tables:
            errors.append("Add at least one table block so the generator has a data model.")
        if not schema.app_name:
            warnings.append("Add an app declaration to name generated applications and targets.")
        if not schema.views:
            suggestions.append("Add view blocks to design forms and visual component layouts.")
        if not schema.llm_providers and not schema.agents:
            suggestions.append("Add llm and agent blocks when the app needs agentic behavior.")

    return {
        "ok": not errors,
        "source": source_name,
        "errors": tuple(errors),
        "warnings": tuple(warnings),
        "suggestions": tuple(suggestions),
        "diagnostics": _lint_diagnostics(source, errors, warnings, suggestions),
        "fixes": _lint_quick_fixes(source, errors, warnings),
        "severity_counts": _diagnostic_severity_counts(errors, warnings, suggestions),
        "summary": _lint_summary(schema),
        "language_quality": dsl_language_quality_contract(),
    }


def apply_lint_fixes(
    text: str,
    *,
    fix_ids: Iterable[str] | None = None,
    source_name: str | None = None,
) -> dict:
    """Apply deterministic quick fixes and return before/after lint metadata."""
    original = text or ""
    report = lint_dsl(original, source_name=source_name)
    selected = set(fix_ids or ())
    fixed = original
    applied: list[str] = []
    skipped: list[dict] = []

    for fix in report["fixes"]:
        fix_id = fix["id"]
        if selected and fix_id not in selected:
            skipped.append({"id": fix_id, "reason": "not_selected"})
            continue
        updated = _apply_lint_fix(fixed, fix)
        if updated == fixed:
            skipped.append({"id": fix_id, "reason": "no_change"})
            continue
        fixed = updated
        applied.append(fix_id)

    after = lint_dsl(fixed, source_name=source_name)
    return {
        "format": "appgen.dsl-fix-result.v1",
        "source": source_name,
        "changed": fixed != original,
        "applied": tuple(applied),
        "skipped": tuple(skipped),
        "original": original,
        "fixed": fixed,
        "before": report,
        "after": after,
    }


def format_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return deterministic DSL formatting plus before/after lint metadata."""
    original = text or ""
    formatted = _format_dsl_source(original)
    return {
        "format": "appgen.dsl-format-result.v1",
        "source": source_name,
        "changed": formatted != original,
        "original": original,
        "formatted": formatted,
        "before": lint_dsl(original, source_name=source_name),
        "after": lint_dsl(formatted, source_name=source_name),
    }


def dsl_outline(text: str, *, source_name: str | None = None) -> dict:
    """Return an IDE-ready outline for AppGen DSL source."""
    source = text or ""
    try:
        schema = schema_from_dsl(source, source_name=source_name)
    except AppGenSyntaxError as exc:
        return _regex_outline(source, source_name=source_name, error=str(exc))
    except Exception as exc:
        return _regex_outline(source, source_name=source_name, error=str(exc))
    return {
        "format": "appgen.dsl-outline.v1",
        "source": source_name,
        "ok": True,
        "app": schema.app_name,
        "targets": _lint_summary(schema)["targets"],
        "blocks": _outline_blocks(source, schema),
        "tables": tuple(
            {
                "name": table.name,
                "fields": tuple(column.name for column in table.columns),
                "search_fields": tuple(column.name for column in table.columns if column.searchable),
                "hidden_fields": tuple(column.name for column in table.columns if column.hidden),
                "relations": tuple(
                    {"field": column.name, "target": ".".join(column.references)}
                    for column in table.columns
                    if column.references
                ),
                "directives": tuple(
                    {
                        "verb": directive.verb,
                        "name": directive.name,
                        "values": directive.values,
                        "targets": directive.targets,
                    }
                    for directive in table.directives
                ),
            }
            for table in schema.tables
        ),
        "views": tuple(
            {
                "name": view.name,
                "table": view.table,
                "fields": view.fields,
                "sections": tuple(section.name for section in view.sections),
                "components": tuple(
                    {
                        "field": component.field,
                        "component": component.component,
                        "bounds": (component.x, component.y, component.w, component.h),
                    }
                    for component in view.components
                ),
                "handlers": tuple(
                    {
                        "trigger": handler.trigger,
                        "event": handler.event,
                        "target": handler.target,
                    }
                    for handler in view.handlers
                ),
            }
            for view in schema.views
        ),
        "flows": tuple(
            {
                "name": flow.name,
                "steps": tuple({"source": step.source, "target": step.target} for step in flow.steps),
                "directives": tuple(
                    {
                        "verb": directive.verb,
                        "values": directive.values,
                        "target": directive.target,
                    }
                    for directive in flow.directives
                ),
            }
            for flow in schema.flows
        ),
        "roles": tuple(role.name for role in schema.roles),
        "rules": tuple(rule.name for rule in schema.rules),
        "llms": tuple(provider.name for provider in schema.llm_providers),
        "agents": tuple(agent.name for agent in schema.agents),
        "platform_blocks": tuple(
            {"kind": block.kind, "name": block.name}
            for block in schema.platform_blocks
        ),
        "enterprise_contracts": tuple(
            {"kind": contract.kind, "name": contract.name}
            for contract in _enterprise_contracts(schema)
        ),
        "summary": _lint_summary(schema),
    }


def dsl_completion_items(prefix: str = "", *, source: str | None = None) -> tuple[dict, ...]:
    """Return keyword, snippet, and schema-aware completions for DSL editors."""
    needle = str(prefix or "").strip().lower()
    items: list[dict] = [
        {"label": keyword, "insert": keyword, "kind": "keyword"}
        for keyword in CORE_KEYWORDS
    ]
    items.extend(_dsl_snippets())
    if source:
        outline = dsl_outline(source)
        for table in outline.get("tables", ()):
            table_name = table["name"]
            items.append({"label": table_name, "insert": table_name, "kind": "table"})
            for field_name in table.get("fields", ()):
                items.append(
                    {
                        "label": field_name,
                        "insert": field_name,
                        "kind": "field",
                        "detail": table_name,
                    }
                )
                items.append(
                    {
                        "label": f"{table_name}.{field_name}",
                        "insert": f"{table_name}.{field_name}",
                        "kind": "reference",
                    }
                )
        for provider_name in outline.get("llms", ()):
            items.append({"label": provider_name, "insert": provider_name, "kind": "llm"})
    deduped = tuple({(item["kind"], item["label"]): item for item in items}.values())
    if not needle:
        return deduped
    return tuple(item for item in deduped if item["label"].lower().startswith(needle))


def dsl_language_service(
    text: str,
    *,
    source_name: str | None = None,
    prefix: str = "",
) -> dict:
    """Return the package-level DSL language-service payload for IDEs."""
    source = text or ""
    return {
        "format": "appgen.dsl-language-service.v1",
        "source": source_name,
        "language": "appgen-dsl",
        "lint": lint_dsl(source, source_name=source_name),
        "outline": dsl_outline(source, source_name=source_name),
        "completions": dsl_completion_items(prefix, source=source),
        "code_actions": dsl_code_actions(source, source_name=source_name),
        "formatting": format_dsl(source, source_name=source_name),
        "authoring_score": dsl_authoring_score(source, source_name=source_name),
        "language_quality": dsl_language_quality_contract(),
    }


def semantic_model_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return the shared JSON semantic model required by docs/tooling.md."""
    source = text or ""
    lint = lint_dsl(source, source_name=source_name)
    try:
        schema = schema_from_dsl(source, source_name=source_name)
    except AppGenSyntaxError:
        schema = None
    except Exception as exc:  # pragma: no cover - defensive tooling boundary
        return {
            "format": "appgen.semantic-model.v1",
            "source_files": (source_name,) if source_name else (),
            "app": {},
            "symbols": {},
            "tables": {},
            "views": {},
            "flows": {},
            "operations": {},
            "rules": {},
            "roles": {},
            "security": {},
            "agents": {},
            "llms": {},
            "pbcs": {},
            "composition": {},
            "contracts": {},
            "deployment": {},
            "packages": {},
            "graphs": {},
            "diagnostics": (
                _spec_diagnostic(
                    source,
                    "AGX9000",
                    "error",
                    f"Internal semantic model error: {exc}",
                ),
            ),
            "ok": False,
        }

    if schema is None:
        return {
            "format": "appgen.semantic-model.v1",
            "source_files": (source_name,) if source_name else (),
            "app": {},
            "symbols": {},
            "tables": {},
            "views": {},
            "flows": {},
            "operations": {},
            "rules": {},
            "roles": {},
            "security": {},
            "agents": {},
            "llms": {},
            "pbcs": {},
            "composition": {},
            "contracts": {},
            "deployment": {},
            "packages": {},
            "graphs": {},
            "diagnostics": tuple(_spec_diagnostic_from_legacy(source, item) for item in lint["diagnostics"]),
            "ok": False,
        }

    tables = _semantic_tables(schema)
    views = _semantic_views(schema)
    flows = _semantic_flows(schema)
    platform = {block.name: block for block in schema.platform_blocks}
    contracts = _semantic_contracts(schema)
    model = {
        "format": "appgen.semantic-model.v1",
        "source_files": (source_name,) if source_name else (),
        "app": {
            "name": schema.app_name,
            "options": dict(schema.app_options),
            "targets": _lint_summary(schema)["targets"],
        },
        "symbols": _semantic_symbols(source, schema),
        "tables": tables,
        "views": views,
        "flows": flows,
        "operations": {
            name: _semantic_platform_block(block)
            for name, block in platform.items()
            if block.kind == "operation"
        },
        "rules": {
            rule.name: {
                "name": rule.name,
                "table": rule.table,
                "conditions": tuple(
                    {
                        "field": condition.field,
                        "operator": condition.operator,
                        "values": condition.values,
                        "message": condition.message,
                        "action": condition.action,
                    }
                    for condition in rule.conditions
                ),
            }
            for rule in schema.rules
        },
        "roles": {
            role.name: {
                "name": role.name,
                "permissions": tuple(_semantic_permission(permission) for permission in role.permissions),
            }
            for role in schema.roles
        },
        "security": {
            name: _semantic_platform_block(block)
            for name, block in platform.items()
            if block.kind == "security"
        },
        "agents": {
            agent.name: {
                "name": agent.name,
                "provider": agent.provider,
                "goal": agent.goal,
                "tools": agent.tools,
                "memory": agent.memory,
                "max_steps": agent.max_steps,
                "skills": tuple(_semantic_statement(item) for item in agent.competencies),
                "handlers": tuple(_semantic_handler(handler) for handler in agent.handlers),
                "permissions": tuple(_semantic_permission(permission) for permission in agent.permissions),
            }
            for agent in schema.agents
        },
        "llms": {
            provider.name: {
                "name": provider.name,
                "provider": provider.provider,
                "mode": provider.mode,
                "model": provider.model,
                "endpoint": provider.endpoint,
                "api_key": provider.api_key,
            }
            for provider in schema.llm_providers
        },
        "pbcs": _semantic_pbcs(schema),
        "composition": _semantic_compositions(schema),
        "contracts": contracts,
        "deployment": {
            name: _semantic_deployment(block)
            for name, block in platform.items()
            if block.kind == "deploy"
        },
        "packages": contracts.get("package", {}),
        "graphs": _semantic_graphs(schema),
        "diagnostics": tuple(_spec_diagnostic_from_legacy(source, item) for item in lint["diagnostics"]),
        "ok": lint["ok"],
    }
    return model


def semantic_model_dsl_file(path: str | Path) -> dict:
    path = Path(path)
    return semantic_model_dsl(path.read_text(encoding="utf-8"), source_name=str(path))


def lint_report_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return the docs/tooling.md appgen.lint-report.v1 contract."""
    source = text or ""
    legacy = lint_dsl(source, source_name=source_name)
    diagnostics = tuple(_spec_diagnostic_from_legacy(source, item) for item in legacy["diagnostics"])
    counts = {
        "error": sum(1 for item in diagnostics if item["severity"] == "error"),
        "warning": sum(1 for item in diagnostics if item["severity"] == "warning"),
        "info": sum(1 for item in diagnostics if item["severity"] == "info"),
        "hint": sum(1 for item in diagnostics if item["severity"] == "hint"),
    }
    return {
        "format": "appgen.lint-report.v1",
        "ok": not counts["error"],
        "files": (source_name,) if source_name else (),
        "severity_counts": counts,
        "diagnostics": diagnostics,
        "fixes_available": any(item.get("fixes") for item in diagnostics),
        "semantic_model_available": legacy["ok"],
        "legacy_report": legacy,
    }


def lint_report_dsl_sources(sources: dict[str, str]) -> dict:
    """Aggregate linter output for a multi-file AppGen-X source set."""
    if not sources:
        diagnostic = _spec_diagnostic("", "AGX0001", "error", "No .appgen files found in directory input.")
        return {
            "format": "appgen.lint-report.v1",
            "ok": False,
            "files": (),
            "severity_counts": {"error": 1, "warning": 0, "info": 0, "hint": 0},
            "diagnostics": (diagnostic,),
            "fixes_available": False,
            "semantic_model_available": False,
            "source_mode": "directory",
            "file_reports": (),
        }
    reports = tuple(
        lint_report_dsl(source, source_name=name)
        for name, source in sorted(sources.items())
    )
    diagnostics = tuple(
        {**diagnostic, "file": report["files"][0] if report.get("files") else None}
        for report in reports
        for diagnostic in report["diagnostics"]
    )
    counts = {
        "error": sum(1 for item in diagnostics if item["severity"] == "error"),
        "warning": sum(1 for item in diagnostics if item["severity"] == "warning"),
        "info": sum(1 for item in diagnostics if item["severity"] == "info"),
        "hint": sum(1 for item in diagnostics if item["severity"] == "hint"),
    }
    return {
        "format": "appgen.lint-report.v1",
        "ok": not counts["error"],
        "files": tuple(report["files"][0] for report in reports if report.get("files")),
        "severity_counts": counts,
        "diagnostics": diagnostics,
        "fixes_available": any(report["fixes_available"] for report in reports),
        "semantic_model_available": all(report["semantic_model_available"] for report in reports),
        "source_mode": "directory" if len(reports) != 1 else "multi-source",
        "file_reports": reports,
    }


def lint_report_dsl_file(path: str | Path) -> dict:
    path = Path(path)
    return lint_report_dsl(path.read_text(encoding="utf-8"), source_name=str(path))


def lint_report_dsl_path(path: str | Path) -> dict:
    path = Path(path)
    if path.is_dir():
        sources = {
            str(item): item.read_text(encoding="utf-8")
            for item in sorted(path.rglob("*.appgen"))
            if item.is_file()
        }
        return lint_report_dsl_sources(sources)
    return lint_report_dsl_file(path)


def diagnostic_catalog_dsl() -> dict:
    """Return the stable diagnostic registry required by docs/tooling.md."""
    specs = tuple(
        {
            "code": spec["code"],
            "severity": spec["severity"],
            "title": spec["title"],
            "trigger": spec["trigger"],
            "example_fix": spec["example_fix"],
            "docs_url": _spec_docs_url(spec["code"]),
            "fixture": _diagnostic_fixture_for_code(spec["code"]) is not None,
        }
        for spec in DIAGNOSTIC_SPECS
    )
    ranges = tuple(
        {
            "range": item[0],
            "area": item[1],
        }
        for item in DIAGNOSTIC_RANGES
    )
    return {
        "format": "appgen.diagnostic-catalog.v1",
        "ok": all(item["fixture"] for item in specs),
        "ranges": ranges,
        "diagnostics": specs,
        "required_codes": tuple(item["code"] for item in specs),
        "fixture_count": len(DIAGNOSTIC_FIXTURES),
        "missing_fixtures": tuple(item["code"] for item in specs if not item["fixture"]),
    }


def diagnostic_fixture_audit_dsl() -> dict:
    """Run diagnostic golden fixtures through their authoritative tooling path."""
    results = tuple(_run_diagnostic_fixture(fixture) for fixture in DIAGNOSTIC_FIXTURES)
    covered = {code for result in results for code in result["observed_codes"]}
    required = tuple(item["code"] for item in DIAGNOSTIC_SPECS)
    missing = tuple(code for code in required if code not in covered)
    return {
        "format": "appgen.diagnostic-fixture-audit.v1",
        "ok": not missing and all(result["ok"] for result in results),
        "required_codes": required,
        "covered_codes": tuple(sorted(covered)),
        "missing_codes": missing,
        "fixtures": results,
        "blocking_gaps": tuple(result for result in results if not result["ok"]),
    }


def parser_golden_audit_dsl() -> dict:
    """Run parser golden fixtures for the grammar surface required by docs/tooling.md."""
    results = tuple(_run_parser_golden_fixture(fixture) for fixture in PARSER_GOLDEN_FIXTURES)
    covered = {
        construct
        for result in results
        if result["valid"]
        for construct in result["constructs"]
    }
    required = tuple(PARSER_GOLDEN_REQUIRED_CONSTRUCTS)
    missing = tuple(construct for construct in required if construct not in covered)
    return {
        "format": "appgen.parser-golden-audit.v1",
        "ok": not missing and all(result["ok"] for result in results),
        "constructs_required": required,
        "constructs_covered": tuple(sorted(covered)),
        "missing_constructs": missing,
        "fixture_count": len(results),
        "valid_fixture_count": sum(1 for result in results if result["valid"]),
        "invalid_fixture_count": sum(1 for result in results if not result["valid"]),
        "fixtures": results,
        "blocking_gaps": tuple(result for result in results if not result["ok"]),
    }


def semantic_drift_audit_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Prove CLI, LSP, IDE, verifier, and tests consume one semantic model."""
    source = text or ""
    semantic = semantic_model_dsl(source, source_name=source_name)
    lint = lint_report_dsl(source, source_name=source_name)
    validate = validate_report_dsl(source, source_name=source_name)
    lsp = lsp_service_dsl(source, source_name=source_name)
    designer = designer_sync_report_dsl(source, source_name=source_name)
    release = release_verifier_report_dsl(source, source_name=source_name, targets=("all",))
    graph_reports = {
        kind: graph_report_dsl(source, source_name=source_name, kind=kind)
        for kind in sorted(semantic.get("graphs", {}))
    }
    canonical = _semantic_drift_digest(semantic)
    checks = (
        _drift_check(
            "cli_validate_uses_semantic_model",
            _semantic_drift_digest(validate.get("semantic_model", {})) == canonical,
            "appgen validate embeds the same semantic model digest as the canonical parser output.",
            {"surface": "CLI validate", "format": validate.get("format")},
        ),
        _drift_check(
            "lsp_diagnostics_match_lint_report",
            _diagnostic_codes(lsp["publishDiagnostics"]["source_report"]) == _diagnostic_codes(lint),
            "LSP diagnostics are a projection of appgen.lint-report.v1.",
            {"surface": "LSP", "format": lsp.get("format")},
        ),
        _drift_check(
            "lsp_symbols_match_semantic_symbols",
            _lsp_symbol_ids(lsp["documentSymbol"]) == _top_level_symbol_ids(semantic),
            "LSP document symbols are projected from semantic symbols.",
            {"surface": "LSP document symbols"},
        ),
        _drift_check(
            "designer_forms_match_semantic_views",
            _designer_view_names(designer) == tuple(semantic.get("views", {}).keys()),
            "Studio form designer views are projected from semantic views.",
            {"surface": "AppGen-X Studio form designer"},
        ),
        _drift_check(
            "designer_database_matches_semantic_tables",
            _designer_table_names(designer) == tuple(semantic.get("tables", {}).keys()),
            "Studio database designer tables are projected from semantic tables.",
            {"surface": "AppGen-X Studio database designer"},
        ),
        _drift_check(
            "designer_graphs_match_semantic_graphs",
            _semantic_drift_digest(designer["projections"]["graph_explain_panel"]["graphs"]) == _semantic_drift_digest(semantic.get("graphs", {})),
            "Studio graph/explain panel reuses semantic graphs.",
            {"surface": "AppGen-X Studio graph panel"},
        ),
        _drift_check(
            "graph_reports_match_semantic_graphs",
            all(report.get("graph") == semantic.get("graphs", {}).get(kind) for kind, report in graph_reports.items()),
            "appgen graph reports emit graph projections from the semantic model.",
            {"surface": "CLI graph", "kinds": tuple(graph_reports)},
        ),
        _drift_check(
            "release_verifier_uses_semantic_model",
            release.get("semantic_model_format") == semantic.get("format")
            and _diagnostic_codes(release) == _diagnostic_codes(semantic),
            "Release verifier carries semantic-model format and diagnostics without reparsing drift.",
            {"surface": "release verifier", "format": release.get("format")},
        ),
        _drift_check(
            "tests_share_canonical_fixture_contract",
            bool(semantic.get("symbols")) and bool(semantic.get("tables")) and bool(semantic.get("graphs")),
            "Fixture-driven tests can assert symbols, tables, and graphs from the same model.",
            {"surface": "tests", "semantic_digest": canonical},
        ),
    )
    return {
        "format": "appgen.semantic-drift-audit.v1",
        "ok": semantic["ok"] and all(check["ok"] for check in checks),
        "source": source_name,
        "semantic_model_format": semantic.get("format"),
        "semantic_digest": canonical,
        "surfaces": (
            "cli",
            "lsp",
            "studio",
            "graph",
            "generator_readiness",
            "release_verifier",
            "tests",
        ),
        "checks": checks,
        "surface_evidence": {
            "lint_report": lint.get("format"),
            "validate_report": validate.get("format"),
            "lsp_service": lsp.get("format"),
            "designer_sync": designer.get("format"),
            "release_verifier": release.get("format"),
            "graph_reports": tuple(report.get("format") for report in graph_reports.values()),
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def _semantic_drift_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=list)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _drift_check(check: str, ok: bool, evidence: str, detail: dict | None = None) -> dict:
    return {
        "check": check,
        "ok": bool(ok),
        "evidence": evidence,
        "detail": detail or {},
    }


def _diagnostic_codes(report: dict) -> tuple[str, ...]:
    return tuple(item.get("code") for item in report.get("diagnostics", ()))


def _lsp_symbol_ids(document_symbols: dict) -> tuple[str, ...]:
    ids: list[str] = []
    for symbol in document_symbols.get("symbols", ()):
        data = symbol.get("data", {})
        if data.get("id"):
            ids.append(data["id"])
    return tuple(ids)


def _top_level_symbol_ids(semantic: dict) -> tuple[str, ...]:
    return tuple(
        symbol["id"]
        for symbol in semantic.get("symbols", {}).values()
        if not symbol.get("parent")
    )


def _designer_view_names(designer: dict) -> tuple[str, ...]:
    return tuple(
        view.get("view")
        for view in designer.get("projections", {}).get("form_designer", {}).get("views", ())
    )


def _designer_table_names(designer: dict) -> tuple[str, ...]:
    return tuple(
        table.get("name")
        for table in designer.get("projections", {}).get("database_designer", {}).get("tables", ())
    )


def _diagnostic_fixture_for_code(code: str) -> dict | None:
    for fixture in DIAGNOSTIC_FIXTURES:
        if code in fixture["expected_codes"]:
            return fixture
    return None


def _run_diagnostic_fixture(fixture: dict) -> dict:
    runner = fixture["runner"]
    if runner == "lint":
        report = lint_report_dsl(fixture["source"], source_name=fixture["name"])
        diagnostics = report["diagnostics"]
    elif runner == "migration":
        report = migration_plan_dsl(
            fixture["previous_source"],
            fixture["source"],
            previous_name=f"{fixture['name']}.previous",
            current_name=fixture["name"],
        )
        diagnostics = report["diagnostics"]
    elif runner == "nl-plan":
        report = nl_plan_dsl(
            fixture["source"],
            source_name=fixture["name"],
            prompt=fixture["prompt"],
        )
        diagnostics = report["diagnostics"]
    else:
        report = {"format": "appgen.unknown-diagnostic-fixture.v1", "ok": False}
        diagnostics = ()
    observed = tuple(dict.fromkeys(item["code"] for item in diagnostics))
    expected = tuple(fixture["expected_codes"])
    missing = tuple(code for code in expected if code not in observed)
    return {
        "name": fixture["name"],
        "runner": runner,
        "expected_codes": expected,
        "observed_codes": observed,
        "ok": not missing,
        "missing_codes": missing,
        "report_format": report.get("format"),
    }


def _run_parser_golden_fixture(fixture: dict) -> dict:
    valid = bool(fixture["valid"])
    error = ""
    parsed = False
    try:
        _parse(fixture["source"])
        parsed = True
    except AppGenSyntaxError as exc:
        error = str(exc)
    ok = parsed if valid else not parsed
    return {
        "name": fixture["name"],
        "valid": valid,
        "constructs": tuple(fixture["constructs"]),
        "ok": ok,
        "parsed": parsed,
        "error": error,
        "source_lines": len(fixture["source"].splitlines()),
    }


def dsl_tooling_cli(argv: Iterable[str] | None = None) -> int:
    """Run docs/tooling.md subcommands without disturbing legacy flags."""
    parser = argparse.ArgumentParser(prog="appgen")
    subparsers = parser.add_subparsers(dest="command", required=True)

    lint_parser = subparsers.add_parser("lint")
    lint_parser.add_argument("path")
    lint_parser.add_argument("--json", action="store_true")
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.add_argument("--catalog")

    format_parser = subparsers.add_parser("format")
    format_parser.add_argument("path")
    format_parser.add_argument("--check", action="store_true")
    format_parser.add_argument("--write", action="store_true")
    format_parser.add_argument("--json", action="store_true")

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path")
    validate_parser.add_argument("--targets")
    validate_parser.add_argument("--json", action="store_true")

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("path")
    generate_parser.add_argument("--out", required=True)
    generate_parser.add_argument("--target", action="append", default=[])
    generate_parser.add_argument("--allow-warnings", action="store_true")
    generate_parser.add_argument("--json", action="store_true")

    graph_parser = subparsers.add_parser("graph")
    graph_parser.add_argument("path")
    graph_parser.add_argument("--kind", default="er")
    graph_parser.add_argument("--format", default="json", choices=("json", "mermaid", "dot"))

    graph_suite_parser = subparsers.add_parser("graph-suite")
    graph_suite_parser.add_argument("path")
    graph_suite_parser.add_argument("--json", action="store_true")

    explain_parser = subparsers.add_parser("explain")
    explain_parser.add_argument("path")
    explain_group = explain_parser.add_mutually_exclusive_group(required=True)
    explain_group.add_argument("--symbol")
    explain_group.add_argument("--diagnostic")
    explain_group.add_argument("--handler")
    explain_parser.add_argument("--json", action="store_true")

    migration_parser = subparsers.add_parser("migration-plan")
    migration_parser.add_argument("previous")
    migration_parser.add_argument("current")
    migration_parser.add_argument("--backend", default="postgresql")
    migration_parser.add_argument("--rename-hint", action="append", default=[])
    migration_parser.add_argument("--json", action="store_true")

    nl_parser = subparsers.add_parser("nl-plan")
    nl_parser.add_argument("path")
    nl_parser.add_argument("--prompt", required=True)
    nl_parser.add_argument("--backend", default="postgresql")
    nl_parser.add_argument("--json", action="store_true")

    lsp_parser = subparsers.add_parser("lsp")
    lsp_parser.add_argument("path")
    lsp_parser.add_argument("--position")
    lsp_parser.add_argument("--prefix", default="")
    lsp_parser.add_argument("--rename")
    lsp_parser.add_argument("--json", action="store_true")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("path")
    verify_parser.add_argument("--target", action="append", default=[])
    verify_parser.add_argument("--json", action="store_true")

    package_parser = subparsers.add_parser("package")
    package_parser.add_argument("path")
    package_parser.add_argument("--target", action="append", default=[])
    package_parser.add_argument("--out")
    package_parser.add_argument("--json", action="store_true")

    pbc_parser = subparsers.add_parser("pbc")
    pbc_subparsers = pbc_parser.add_subparsers(dest="pbc_command", required=True)
    pbc_list_parser = pbc_subparsers.add_parser("list")
    pbc_list_parser.add_argument("--json", action="store_true")
    pbc_verify_parser = pbc_subparsers.add_parser("verify")
    pbc_verify_parser.add_argument("pbc")
    pbc_verify_parser.add_argument("--json", action="store_true")
    pbc_publish_parser = pbc_subparsers.add_parser("publish")
    pbc_publish_parser.add_argument("pbc")
    pbc_publish_parser.add_argument("--catalog", default="local", choices=("local", "file", "registry"))
    pbc_publish_parser.add_argument("--catalog-path")
    pbc_publish_parser.add_argument("--json", action="store_true")

    designer_parser = subparsers.add_parser("designer-sync")
    designer_parser.add_argument("path")
    designer_parser.add_argument("--edit-json")
    designer_parser.add_argument("--json", action="store_true")

    diagnostics_parser = subparsers.add_parser("diagnostics")
    diagnostics_parser.add_argument("--audit-fixtures", action="store_true")
    diagnostics_parser.add_argument("--json", action="store_true")

    parser_golden_parser = subparsers.add_parser("parser-golden")
    parser_golden_parser.add_argument("--json", action="store_true")

    drift_parser = subparsers.add_parser("drift")
    drift_parser.add_argument("path")
    drift_parser.add_argument("--json", action="store_true")

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(tuple(argv or ()))
    path = Path(args.path) if hasattr(args, "path") else None
    source = "" if path is None or path.is_dir() else path.read_text(encoding="utf-8")

    if args.command == "lint":
        report = lint_report_dsl_path(path) if path is not None else lint_report_dsl(source)
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "format":
        report = format_report_dsl(source, source_name=str(path), include_text=True)
        if args.write and report["changed"]:
            path.write_text(report["text"], encoding="utf-8")
        printable = report if args.json else {key: value for key, value in report.items() if key != "text"}
        _emit_tooling_payload(printable, as_json=args.json)
        if args.check and report["changed"]:
            return 1
        return 0 if not any(item["severity"] == "error" for item in report["diagnostics"]) else 1
    if args.command == "validate":
        report = validate_report_dsl(source, source_name=str(path))
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "generate":
        report = generate_report_dsl(
            source,
            source_name=str(path),
            output_dir=args.out,
            targets=args.target,
            allow_warnings=args.allow_warnings,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "graph":
        report = graph_report_dsl(source, source_name=str(path), kind=args.kind)
        if args.format == "json":
            _emit_tooling_payload(report, as_json=True)
        else:
            print(_graph_as_text(report.get("graph", {}), args.format))
        return 0 if report["ok"] else 1
    if args.command == "graph-suite":
        report = graph_suite_report_dsl(source, source_name=str(path))
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "explain":
        report = explain_report_dsl(
            source,
            source_name=str(path),
            symbol=args.symbol,
            diagnostic=args.diagnostic,
            handler=args.handler,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "migration-plan":
        previous_path = Path(args.previous)
        current_path = Path(args.current)
        report = migration_plan_dsl(
            previous_path.read_text(encoding="utf-8"),
            current_path.read_text(encoding="utf-8"),
            previous_name=str(previous_path),
            current_name=str(current_path),
            backend=args.backend,
            rename_hints=args.rename_hint,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "nl-plan":
        report = nl_plan_dsl(
            source,
            prompt=args.prompt,
            source_name=str(path),
            backend=args.backend,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "lsp":
        report = lsp_service_dsl(
            source,
            source_name=str(path),
            position=_parse_lsp_position(args.position),
            prefix=args.prefix,
            rename_to=args.rename,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "verify":
        report = release_verifier_report_dsl(
            source,
            source_name=str(path),
            targets=args.target,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "package":
        report = release_verifier_report_dsl(
            source,
            source_name=str(path),
            targets=args.target or ("web", "mobile", "desktop"),
            output_dir=args.out,
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "pbc":
        if args.pbc_command == "list":
            report = pbc_verifier_catalog_report()
            _emit_tooling_payload(report, as_json=args.json)
            return 0 if report["ok"] else 1
        if args.pbc_command == "publish":
            report = pbc_publish_report(
                args.pbc,
                catalog=args.catalog,
                catalog_path=args.catalog_path,
            )
            _emit_tooling_payload(report, as_json=args.json)
            return 0 if report["ok"] else 1
        report = pbc_verifier_report(args.pbc)
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "designer-sync":
        edit = json.loads(args.edit_json) if args.edit_json else None
        report = designer_sync_report_dsl(source, source_name=str(path), visual_edit=edit)
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "diagnostics":
        report = diagnostic_fixture_audit_dsl() if args.audit_fixtures else diagnostic_catalog_dsl()
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "parser-golden":
        report = parser_golden_audit_dsl()
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "drift":
        report = semantic_drift_audit_dsl(source, source_name=str(path))
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "doctor":
        report = doctor_report_dsl()
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    return 2


def _emit_tooling_payload(payload: dict, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True, default=list))
        return
    if payload.get("format") == "appgen.lint-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        counts = payload.get("severity_counts", {})
        print(f"lint {status}: {counts}")
        for diagnostic in payload.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
        return
    if payload.get("format") == "appgen.format-result.v1":
        status = "changed" if payload.get("changed") else "ok"
        idempotent = "idempotent" if payload.get("idempotent") else "not-idempotent"
        print(f"format {status}: {idempotent}")
        for diagnostic in payload.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
        return
    if payload.get("format") == "appgen.validate-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        print(f"validate {status}")
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
        return
    if payload.get("format") == "appgen.generate-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        print(f"generate {status}: generated={payload.get('generated', False)}")
        for artifact in payload.get("artifacts", ()):
            print(f"artifact {artifact['path']}")
        for gap in payload.get("blocking_gaps", ()):
            print(f"gap {gap}")
        return
    if payload.get("format") == "appgen.graph-suite-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        kind_count = len(payload.get("required_kinds", ()))
        format_count = len(payload.get("formats", ()))
        print(f"graph-suite {status}: {kind_count} kinds, {format_count} formats")
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
        return
    if payload.get("format") == "appgen.parser-golden-audit.v1":
        status = "ok" if payload.get("ok") else "failed"
        print(
            f"parser-golden {status}: "
            f"{payload.get('fixture_count', 0)} fixtures, "
            f"{len(payload.get('constructs_covered', ()))} constructs"
        )
        for gap in payload.get("blocking_gaps", ()):
            print(f"fail {gap['name']}: {gap.get('error', '')}")
        return
    if payload.get("format") == "appgen.explain-report.v1":
        print(json.dumps(payload, indent=2, sort_keys=True, default=list))
        return
    if payload.get("format") == "appgen.doctor-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        print(f"doctor {status}")
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}: {check.get('message', '')}")
        return
    if payload.get("format") == "appgen.pbc-publish-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        target = payload.get("target", {})
        print(f"pbc publish {status}: {payload.get('pbc')} -> {target.get('mode')}")
        print(f"side_effect_free={target.get('side_effect_free')} write_performed={target.get('write_performed')}")
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
        return
    print(json.dumps(payload, indent=2, sort_keys=True, default=list))


def _graph_as_text(graph: dict, output_format: str) -> str:
    nodes = graph.get("nodes", ())
    edges = graph.get("edges", ())
    if output_format == "mermaid":
        lines = ["graph TD"]
        for node in nodes:
            lines.append(f"  {node['id'].replace('.', '_')}[{node['id']}]")
        for edge in edges:
            source = str(edge.get("from", "")).replace(".", "_").replace("/", "_")
            target = str(edge.get("to", "")).replace(".", "_").replace("/", "_")
            label = edge.get("label", "")
            lines.append(f"  {source} -->|{label}| {target}")
        return "\n".join(lines)
    if output_format == "dot":
        lines = ["digraph appgen {"]
        for node in nodes:
            lines.append(f'  "{node["id"]}";')
        for edge in edges:
            lines.append(f'  "{edge.get("from")}" -> "{edge.get("to")}" [label="{edge.get("label", "")}"];')
        lines.append("}")
        return "\n".join(lines)
    return json.dumps(graph, indent=2, sort_keys=True, default=list)


def format_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    include_text: bool = True,
) -> dict:
    """Return the docs/tooling.md appgen.format-result.v1 contract."""
    result = format_dsl(text, source_name=source_name)
    second = format_dsl(result["formatted"], source_name=source_name)
    payload = {
        "format": "appgen.format-result.v1",
        "source": source_name,
        "changed": result["changed"],
        "idempotent": second["formatted"] == result["formatted"],
        "diagnostics": lint_report_dsl(result["formatted"], source_name=source_name)["diagnostics"],
    }
    if include_text:
        payload["text"] = result["formatted"]
    return payload


def validate_report_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return a generator-readiness validation contract without writing files."""
    lint = lint_report_dsl(text, source_name=source_name)
    semantic = semantic_model_dsl(text, source_name=source_name)
    checks = (
        {"check": "lint", "ok": lint["ok"]},
        {"check": "semantic_model", "ok": semantic["ok"]},
        {"check": "has_tables", "ok": bool(semantic.get("tables"))},
        {"check": "view_bindings", "ok": not any(item["code"] in {"AGX0303", "AGX0402"} for item in lint["diagnostics"])},
        {"check": "handler_targets", "ok": not any(item["code"] == "AGX0403" for item in lint["diagnostics"])},
    )
    return {
        "format": "appgen.validate-report.v1",
        "source": source_name,
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "lint": lint,
        "semantic_model": semantic,
    }


def generate_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    output_dir: str | Path,
    targets: Iterable[str] | None = None,
    allow_warnings: bool = False,
) -> dict:
    """Validate and generate an app from DSL with machine-readable evidence."""
    source = text or ""
    output_path = Path(output_dir)
    requested_targets = tuple(targets or ())
    validation = validate_report_dsl(source, source_name=source_name)
    lint = validation["lint"]
    errors = tuple(item for item in lint["diagnostics"] if item["severity"] == "error")
    warnings = tuple(item for item in lint["diagnostics"] if item["severity"] == "warning")
    if errors:
        return {
            "format": "appgen.generate-report.v1",
            "ok": False,
            "source": source_name,
            "output_dir": str(output_path),
            "targets": requested_targets,
            "allow_warnings": allow_warnings,
            "validation": validation,
            "generated": False,
            "artifacts": (),
            "diagnostics": tuple(lint["diagnostics"]),
            "blocking_gaps": ("lint_errors",),
        }
    try:
        from .gen import generate_app_from_schema

        schema = schema_from_dsl(source, source_name=source_name)
        generated_path = generate_app_from_schema(schema, output_path)
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        diagnostic = _spec_diagnostic(
            source,
            "AGX9000",
            "error",
            f"Internal generation error: {exc}",
        )
        return {
            "format": "appgen.generate-report.v1",
            "ok": False,
            "source": source_name,
            "output_dir": str(output_path),
            "targets": requested_targets,
            "validation": validation,
            "generated": False,
            "artifacts": (),
            "diagnostics": (diagnostic,),
            "blocking_gaps": ("generation_error",),
        }
    artifacts = _generated_artifact_summary(generated_path)
    manifest_path = generated_path / "appgen.json"
    return {
        "format": "appgen.generate-report.v1",
        "ok": validation["ok"] and bool(artifacts) and manifest_path.exists(),
        "source": source_name,
        "output_dir": str(generated_path),
        "targets": requested_targets or validation["semantic_model"]["app"].get("targets", ()),
        "allow_warnings": allow_warnings,
        "validation": validation,
        "semantic_model_format": validation["semantic_model"].get("format"),
        "generated": True,
        "artifacts": artifacts,
        "manifest": str(manifest_path) if manifest_path.exists() else None,
        "diagnostics": tuple(lint["diagnostics"]),
        "blocking_gaps": () if manifest_path.exists() else ("manifest_missing",),
    }


def doctor_report_dsl() -> dict:
    """Check parser generation, imports, catalog, templates, backends, and IDE hooks."""
    root = Path(__file__).resolve().parents[2]
    checks = (
        _doctor_check(
            "grammar_file",
            (root / "lang" / "appgen.g4").exists(),
            "ANTLR grammar exists at lang/appgen.g4.",
            {"path": "lang/appgen.g4"},
        ),
        _doctor_check(
            "generated_parser",
            (_GENERATED_DIR / "appgenParser.py").exists() and (_GENERATED_DIR / "appgenLexer.py").exists(),
            "Generated parser and lexer are present.",
            {"path": str(_GENERATED_DIR)},
        ),
        _doctor_check(
            "parser_sync",
            dsl_antlr_integrity_report()["ok"],
            "Generated ANTLR artifacts are synchronized with the grammar contract.",
            {"report_format": "appgen.dsl-antlr-integrity.v1"},
        ),
        _doctor_check(
            "parser_golden_fixtures",
            parser_golden_audit_dsl()["ok"],
            "Parser golden fixtures cover valid and invalid DSL grammar constructs.",
            {"report_format": "appgen.parser-golden-audit.v1"},
        ),
        _doctor_check(
            "directory_lint_input",
            lint_report_dsl_sources(
                {
                    "doctor/app.appgen": _doctor_sample_dsl(),
                    "doctor/agent.appgen": "app DoctorAgent { targets: web }\n\ntable AgentThing { id: int pk }\n",
                }
            )["ok"],
            "Linter accepts multi-file directory-style source sets.",
            {"report_format": "appgen.lint-report.v1"},
        ),
        _doctor_import_check("python_package_import", "pyAppGen"),
        _doctor_import_check("sqlalchemy_import", "sqlalchemy"),
        _doctor_check(
            "pbc_catalog",
            bool(_pbc_catalog_by_key()),
            "Registered PBC catalog is available.",
            {"count": len(_pbc_catalog_by_key())},
        ),
        _doctor_check(
            "template_writers",
            _doctor_template_writers_available(),
            "Generator template writer functions are importable.",
            {"writers": ("write_generated_home", "write_studio_template", "write_form_designer_template")},
        ),
        _doctor_check(
            "generator_backends",
            {"postgresql", "mysql", "mariadb"} <= set(migration_plan_dsl("", "", backend="postgresql")["allowed_backends"]),
            "Migration/generation backend policy is constrained to PostgreSQL and MySQL-compatible profiles.",
            {"allowed": ("postgresql", "mysql", "mariadb")},
        ),
        _doctor_check(
            "lsp_semantic_service",
            lsp_capabilities_dsl()["source_of_truth"] == "appgen.semantic-model.v1",
            "Language-server adapter is bound to the shared semantic model.",
            {"report_format": "appgen.lsp-capabilities.v1"},
        ),
        _doctor_check(
            "studio_semantic_service",
            designer_sync_report_dsl(_doctor_sample_dsl(), source_name="doctor.appgen")["semantic_model_format"] == "appgen.semantic-model.v1",
            "Studio designer service is bound to the shared semantic model.",
            {"report_format": "appgen.designer-sync-report.v1"},
        ),
    )
    return {
        "format": "appgen.doctor-report.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def _generated_artifact_summary(output_path: Path) -> tuple[dict, ...]:
    if not output_path.exists():
        return ()
    artifacts = []
    for path in sorted(item for item in output_path.rglob("*") if item.is_file()):
        rel = path.relative_to(output_path).as_posix()
        if rel.startswith("__pycache__/"):
            continue
        artifacts.append({"path": rel, "bytes": path.stat().st_size})
    return tuple(artifacts)


def _doctor_check(check: str, ok: bool, message: str, detail: dict | None = None) -> dict:
    return {
        "check": check,
        "ok": bool(ok),
        "message": message,
        "detail": detail or {},
    }


def _doctor_import_check(check: str, module: str) -> dict:
    try:
        __import__(module)
    except Exception as exc:  # pragma: no cover - environment-dependent
        return _doctor_check(check, False, f"Cannot import {module}: {exc}", {"module": module})
    return _doctor_check(check, True, f"Imported {module}.", {"module": module})


def _doctor_template_writers_available() -> bool:
    try:
        from . import gen
    except Exception:
        return False
    return all(
        callable(getattr(gen, name, None))
        for name in ("write_generated_home", "write_studio_template", "write_form_designer_template")
    )


def _doctor_sample_dsl() -> str:
    return "app Doctor { targets: web }\n\ntable Thing { id: int pk; name: string }\n\nview ThingForm for Thing { Main: name }\n"


def graph_report_dsl(text: str, *, source_name: str | None = None, kind: str = "er") -> dict:
    """Return one semantic graph in JSON form."""
    model = semantic_model_dsl(text, source_name=source_name)
    graphs = model.get("graphs", {})
    if kind not in graphs:
        return {
            "format": "appgen.graph-report.v1",
            "source": source_name,
            "kind": kind,
            "ok": False,
            "diagnostics": (
                {
                    "code": "AGX9001",
                    "severity": "error",
                    "title": "Unknown graph kind",
                    "message": f"Unknown graph kind: {kind}",
                    "range": None,
                    "related_locations": (),
                    "fixes": (),
                    "docs_url": "docs/tooling.md#graph-tooling",
                },
            ),
            "available_kinds": tuple(sorted(graphs)),
        }
    return {
        "format": "appgen.graph-report.v1",
        "source": source_name,
        "kind": kind,
        "ok": model["ok"],
        "graph": graphs[kind],
        "diagnostics": model["diagnostics"],
    }


def graph_suite_report_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return release evidence for every required semantic graph and format."""
    model = semantic_model_dsl(text, source_name=source_name)
    graphs = model.get("graphs", {})
    missing_kinds = tuple(kind for kind in REQUIRED_GRAPH_KINDS if kind not in graphs)
    graph_reports = {
        kind: graph_report_dsl(text, source_name=source_name, kind=kind)
        for kind in REQUIRED_GRAPH_KINDS
        if kind in graphs
    }
    renderings = {
        kind: {
            output_format: _graph_as_text(report.get("graph", {}), output_format)
            for output_format in GRAPH_TEXT_FORMATS
        }
        for kind, report in graph_reports.items()
    }
    rendering_gaps = tuple(
        {
            "kind": kind,
            "format": output_format,
        }
        for kind, outputs in renderings.items()
        for output_format, rendered in outputs.items()
        if not rendered.strip()
    )
    checks = (
        _release_check(
            "all_required_graph_kinds",
            not missing_kinds,
            detail={"required": REQUIRED_GRAPH_KINDS, "missing": missing_kinds},
        ),
        _release_check(
            "json_mermaid_dot_renderings",
            not rendering_gaps
            and all(set(outputs) == set(GRAPH_TEXT_FORMATS) for outputs in renderings.values()),
            detail={"formats": GRAPH_TEXT_FORMATS, "gaps": rendering_gaps},
        ),
        _release_check(
            "graphs_share_semantic_model",
            all(report.get("graph") == graphs.get(kind) for kind, report in graph_reports.items()),
            detail={"semantic_model_format": model.get("format")},
        ),
    )
    return {
        "format": "appgen.graph-suite-report.v1",
        "source": source_name,
        "ok": model["ok"] and all(check["ok"] for check in checks),
        "semantic_model_format": model.get("format"),
        "required_kinds": REQUIRED_GRAPH_KINDS,
        "formats": GRAPH_TEXT_FORMATS,
        "graph_reports": graph_reports,
        "renderings": renderings,
        "diagnostics": model["diagnostics"],
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def explain_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    symbol: str | None = None,
    diagnostic: str | None = None,
    handler: str | None = None,
) -> dict:
    """Explain a symbol, diagnostic, or handler using the semantic model."""
    model = semantic_model_dsl(text, source_name=source_name)
    if diagnostic:
        return {
            "format": "appgen.explain-report.v1",
            "source": source_name,
            "ok": True,
            "kind": "diagnostic",
            "query": diagnostic,
            "explanation": _diagnostic_explanation(diagnostic),
        }
    if handler:
        handlers = model.get("graphs", {}).get("handler", {}).get("edges", ())
        matches = tuple(edge for edge in handlers if edge.get("from") == handler or edge.get("label") == handler)
        return {
            "format": "appgen.explain-report.v1",
            "source": source_name,
            "ok": bool(matches),
            "kind": "handler",
            "query": handler,
            "matches": matches,
        }
    if symbol:
        symbols = model.get("symbols", {})
        match = symbols.get(symbol) or symbols.get(_symbol_query_to_id(symbol))
        return {
            "format": "appgen.explain-report.v1",
            "source": source_name,
            "ok": bool(match),
            "kind": "symbol",
            "query": symbol,
            "symbol": match,
        }
    return {
        "format": "appgen.explain-report.v1",
        "source": source_name,
        "ok": False,
        "kind": "none",
        "message": "Provide symbol, diagnostic, or handler.",
    }


def migration_plan_dsl(
    previous_text: str,
    current_text: str,
    *,
    previous_name: str | None = None,
    current_name: str | None = None,
    backend: str = "postgresql",
    rename_hints: Iterable[str] | None = None,
) -> dict:
    """Compare two DSL semantic models and return appgen.migration-plan.v1."""
    normalized_backend = backend.strip().lower().replace("-", "_")
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    previous = semantic_model_dsl(previous_text, source_name=previous_name)
    current = semantic_model_dsl(current_text, source_name=current_name)
    hints = _parse_rename_hints(rename_hints or ())
    diagnostics: list[dict] = []
    changes: list[dict] = []

    if normalized_backend not in allowed_backends:
        diagnostics.append(
            _spec_diagnostic(
                current_text,
                "AGX1102",
                "error",
                f"Unsupported migration backend: {backend}",
            )
        )
    if not previous.get("ok"):
        diagnostics.append(
            _spec_diagnostic(
                previous_text,
                "AGX1100",
                "error",
                "Previous semantic model has diagnostics and cannot be used as a migration baseline.",
            )
        )
    if not current.get("ok"):
        diagnostics.append(
            _spec_diagnostic(
                current_text,
                "AGX1100",
                "error",
                "Current semantic model has diagnostics and cannot produce a safe migration plan.",
            )
        )

    previous_tables = previous.get("tables", {})
    current_tables = current.get("tables", {})
    previous_names = set(previous_tables)
    current_names = set(current_tables)
    added_tables = current_names - previous_names
    dropped_tables = previous_names - current_names

    table_renames = _table_rename_candidates(previous_tables, current_tables, dropped_tables, added_tables, hints)
    renamed_old = {item["from"] for item in table_renames}
    renamed_new = {item["to"] for item in table_renames}
    changes.extend(table_renames)

    for table_name in sorted(added_tables - renamed_new):
        changes.append(_migration_change("add_table", table=table_name, destructive=False))
    for table_name in sorted(dropped_tables - renamed_old):
        changes.append(
            _migration_change(
                "drop_table",
                table=table_name,
                destructive=True,
                safe_alternative="Retain the table and mark it archived until data retention is approved.",
            )
        )

    for table_name in sorted(previous_names & current_names):
        changes.extend(
            _field_migration_changes(
                table_name,
                previous_tables[table_name],
                current_tables[table_name],
                hints,
            )
        )
        changes.extend(_directive_migration_changes(table_name, previous_tables[table_name], current_tables[table_name]))

    changes.extend(_relationship_migration_changes(previous, current))
    changes.extend(_calculated_field_migration_changes(previous_tables, current_tables))
    changes.extend(_pbc_migration_changes(previous, current))

    destructive = any(change.get("destructive") for change in changes)
    if destructive:
        diagnostics.append(
            _spec_diagnostic(
                current_text,
                "AGX1101",
                "warning",
                "Migration plan contains destructive changes and requires explicit approval.",
            )
        )

    return {
        "format": "appgen.migration-plan.v1",
        "ok": not any(item["severity"] == "error" for item in diagnostics),
        "backend": normalized_backend,
        "allowed_backends": tuple(sorted(allowed_backends)),
        "source_files": tuple(item for item in (previous_name, current_name) if item),
        "changes": tuple(changes),
        "destructive": destructive,
        "requires_approval": destructive,
        "diagnostics": tuple(diagnostics),
        "rename_hints": tuple(hints.values()),
    }


def migration_plan_dsl_files(
    previous_path: str | Path,
    current_path: str | Path,
    *,
    backend: str = "postgresql",
    rename_hints: Iterable[str] | None = None,
) -> dict:
    previous = Path(previous_path)
    current = Path(current_path)
    return migration_plan_dsl(
        previous.read_text(encoding="utf-8"),
        current.read_text(encoding="utf-8"),
        previous_name=str(previous),
        current_name=str(current),
        backend=backend,
        rename_hints=rename_hints,
    )


def nl_plan_dsl(
    text: str,
    *,
    prompt: str,
    source_name: str | None = None,
    backend: str = "postgresql",
) -> dict:
    """Return a constrained natural-language-to-DSL edit plan."""
    source = text or ""
    semantic = semantic_model_dsl(source, source_name=source_name)
    operation = _classify_nl_operation(prompt, semantic)
    if operation["kind"] == "unsupported":
        diagnostic = _spec_diagnostic(
            source,
            "AGX1201",
            "error",
            "Natural-language plan cannot be represented as a constrained DSL diff.",
        )
        return {
            "format": "appgen.nl-plan.v1",
            "ok": False,
            "prompt": prompt,
            "intent": "unsupported",
            "edit_operations": (),
            "dsl_patch": "",
            "patched_source": source,
            "affected_symbols": (),
            "lint": lint_report_dsl(source, source_name=source_name),
            "migration_preview": migration_plan_dsl(source, source, previous_name=source_name, current_name=source_name, backend=backend),
            "test_plan": (),
            "token_budget_notes": _nl_token_budget_notes(),
            "diagnostics": (diagnostic,),
        }

    patch = _render_nl_dsl_patch(operation)
    patched_source = _append_dsl_patch(source, patch)
    lint = lint_report_dsl(patched_source, source_name=source_name)
    migration = migration_plan_dsl(
        source,
        patched_source,
        previous_name=source_name,
        current_name=source_name,
        backend=backend,
    )
    diagnostics = tuple(lint["diagnostics"]) + tuple(migration["diagnostics"])
    return {
        "format": "appgen.nl-plan.v1",
        "ok": lint["ok"] and not any(item["severity"] == "error" for item in migration["diagnostics"]),
        "prompt": prompt,
        "intent": operation["intent"],
        "edit_operations": (operation,),
        "dsl_patch": patch,
        "patched_source": patched_source,
        "affected_symbols": tuple(operation.get("affected_symbols", ())),
        "lint": lint,
        "migration_preview": migration,
        "test_plan": _nl_test_plan(operation),
        "token_budget_notes": _nl_token_budget_notes(),
        "diagnostics": diagnostics,
    }


def lsp_capabilities_dsl() -> dict:
    """Return the AppGen-X language-server capability contract."""
    return {
        "format": "appgen.lsp-capabilities.v1",
        "language_id": "appgen",
        "extensions": (".appgen", ".ag", ".ags"),
        "features": {
            "textDocument/didOpen": True,
            "textDocument/didChange": True,
            "textDocument/completion": True,
            "textDocument/hover": True,
            "textDocument/definition": True,
            "textDocument/references": True,
            "textDocument/documentSymbol": True,
            "textDocument/rename": True,
            "textDocument/codeAction": True,
            "textDocument/formatting": True,
            "workspace/symbol": True,
        },
        "sync": "full-document-with-semantic-cache",
        "source_of_truth": "appgen.semantic-model.v1",
    }


def lsp_service_dsl(
    text: str,
    *,
    source_name: str | None = None,
    position: dict | None = None,
    prefix: str = "",
    rename_to: str | None = None,
) -> dict:
    """Return LSP-shaped data built from the shared semantic model."""
    source = text or ""
    semantic = semantic_model_dsl(source, source_name=source_name)
    active_position = position or {"line": 0, "character": 0}
    return {
        "format": "appgen.lsp-service.v1",
        "ok": semantic["ok"],
        "source": source_name,
        "capabilities": lsp_capabilities_dsl(),
        "semantic_model_format": semantic["format"],
        "publishDiagnostics": lsp_diagnostics_dsl(source, source_name=source_name),
        "completion": lsp_completion_dsl(source, source_name=source_name, position=active_position, prefix=prefix),
        "hover": lsp_hover_dsl(source, source_name=source_name, position=active_position),
        "definition": lsp_definition_dsl(source, source_name=source_name, position=active_position),
        "references": lsp_references_dsl(source, source_name=source_name, position=active_position),
        "documentSymbol": lsp_document_symbols_dsl(source, source_name=source_name),
        "codeAction": lsp_code_actions_dsl(source, source_name=source_name),
        "formatting": lsp_formatting_dsl(source, source_name=source_name),
        "rename": lsp_rename_dsl(source, source_name=source_name, position=active_position, new_name=rename_to)
        if rename_to
        else None,
        "workspaceSymbol": lsp_workspace_symbols_dsl(source, source_name=source_name, query=prefix),
    }


def lsp_diagnostics_dsl(text: str, *, source_name: str | None = None) -> dict:
    lint = lint_report_dsl(text, source_name=source_name)
    return {
        "format": "appgen.lsp-diagnostics.v1",
        "uri": source_name,
        "diagnostics": tuple(_lsp_diagnostic(item) for item in lint["diagnostics"]),
        "source_report": lint,
    }


def lsp_completion_dsl(
    text: str,
    *,
    source_name: str | None = None,
    position: dict | None = None,
    prefix: str = "",
) -> dict:
    del source_name
    semantic = semantic_model_dsl(text)
    items: list[dict] = []
    for item in dsl_completion_items(prefix, source=text):
        items.append(
            {
                "label": item["label"],
                "kind": _lsp_completion_kind(item.get("kind", "")),
                "detail": item.get("detail") or item.get("kind"),
                "insertText": item.get("insert", item["label"]),
                "data": {"source": "dsl_completion_items", "kind": item.get("kind")},
            }
        )
    for key, pbc in semantic.get("pbcs", {}).items():
        items.append(
            {
                "label": key,
                "kind": 9,
                "detail": "PBC catalog entry" if pbc.get("catalog_resolved") else "PBC declaration",
                "insertText": key,
                "data": {"source": "pbc_catalog", "catalog_resolved": pbc.get("catalog_resolved", False)},
            }
        )
    for flow_name in semantic.get("flows", {}):
        items.append(
            {
                "label": flow_name,
                "kind": 3,
                "detail": "workflow target",
                "insertText": flow_name,
                "data": {"source": "semantic_model", "kind": "flow"},
            }
        )
    deduped = tuple({(item["label"], item["detail"]): item for item in items}.values())
    return {
        "format": "appgen.lsp-completion.v1",
        "position": position,
        "isIncomplete": False,
        "items": deduped,
    }


def lsp_hover_dsl(text: str, *, source_name: str | None = None, position: dict | None = None) -> dict:
    token = _lsp_token_at_position(text, position)
    symbol = _lsp_symbol_for_token(text, token, source_name=source_name)
    diagnostic = _lsp_diagnostic_for_token(text, token, source_name=source_name)
    contents: list[str] = []
    if symbol:
        contents.append(f"{symbol['kind']} `{symbol['name']}`")
        if symbol.get("detail"):
            contents.append(json.dumps(symbol["detail"], sort_keys=True, default=list))
    if diagnostic:
        contents.append(f"{diagnostic['code']}: {diagnostic['message']}")
    if token in CORE_KEYWORDS:
        contents.append(f"AppGen-X keyword `{token}`")
    return {
        "format": "appgen.lsp-hover.v1",
        "ok": bool(contents),
        "token": token,
        "contents": tuple(contents),
        "range": _lsp_token_range(text, position, token),
    }


def lsp_definition_dsl(text: str, *, source_name: str | None = None, position: dict | None = None) -> dict:
    token = _lsp_token_at_position(text, position)
    symbol = _lsp_symbol_for_token(text, token, source_name=source_name)
    location = _lsp_location(source_name, symbol.get("range")) if symbol else None
    return {
        "format": "appgen.lsp-definition.v1",
        "ok": location is not None,
        "token": token,
        "location": location,
    }


def lsp_references_dsl(text: str, *, source_name: str | None = None, position: dict | None = None) -> dict:
    token = _lsp_token_at_position(text, position)
    locations = tuple(_lsp_location(source_name, item) for item in _lsp_occurrence_ranges(text, token))
    return {
        "format": "appgen.lsp-references.v1",
        "ok": bool(locations),
        "token": token,
        "locations": locations,
    }


def lsp_document_symbols_dsl(text: str, *, source_name: str | None = None) -> dict:
    semantic = semantic_model_dsl(text, source_name=source_name)
    symbols = []
    for symbol in semantic.get("symbols", {}).values():
        parent = symbol.get("parent")
        if parent:
            continue
        children = tuple(
            _lsp_document_symbol(child)
            for child in semantic.get("symbols", {}).values()
            if child.get("parent") == symbol["id"]
        )
        symbols.append({**_lsp_document_symbol(symbol), "children": children})
    return {
        "format": "appgen.lsp-document-symbols.v1",
        "ok": semantic["ok"],
        "symbols": tuple(symbols),
    }


def lsp_workspace_symbols_dsl(text: str, *, source_name: str | None = None, query: str = "") -> dict:
    semantic = semantic_model_dsl(text, source_name=source_name)
    needle = (query or "").lower()
    symbols = tuple(
        {
            "name": symbol["name"],
            "kind": _lsp_symbol_kind(symbol["kind"]),
            "location": _lsp_location(source_name, symbol.get("range")),
            "containerName": symbol.get("parent"),
            "data": {"id": symbol["id"], "kind": symbol["kind"]},
        }
        for symbol in semantic.get("symbols", {}).values()
        if not needle or needle in symbol["name"].lower() or needle in symbol["id"].lower()
    )
    return {"format": "appgen.lsp-workspace-symbols.v1", "ok": semantic["ok"], "symbols": symbols}


def lsp_code_actions_dsl(text: str, *, source_name: str | None = None) -> dict:
    actions = []
    for action in dsl_code_actions(text, source_name=source_name):
        actions.append(
            {
                "title": action["title"],
                "kind": "quickfix",
                "diagnostics": tuple(_lsp_diagnostic(item) for item in action.get("diagnostics", ())),
                "edit": {"changes": {source_name or "memory://appgen": action.get("edits", ())}},
                "command": action.get("command"),
                "data": {"id": action["id"], "changed": action["changed"]},
            }
        )
    actions.extend(_lsp_required_quick_actions(text, source_name=source_name))
    return {"format": "appgen.lsp-code-actions.v1", "ok": True, "actions": tuple(actions)}


def lsp_formatting_dsl(text: str, *, source_name: str | None = None) -> dict:
    formatted = format_report_dsl(text, source_name=source_name, include_text=True)
    full_range = {
        "start": {"line": 0, "character": 0},
        "end": {"line": len((text or "").splitlines()), "character": 0},
    }
    return {
        "format": "appgen.lsp-formatting.v1",
        "ok": not any(item["severity"] == "error" for item in formatted["diagnostics"]),
        "edits": (
            {
                "range": full_range,
                "newText": formatted["text"],
            },
        )
        if formatted["changed"]
        else (),
        "format_report": formatted,
    }


def lsp_rename_dsl(
    text: str,
    *,
    source_name: str | None = None,
    position: dict | None = None,
    new_name: str | None = None,
) -> dict:
    source = text or ""
    token = _lsp_token_at_position(source, position)
    if not token or not new_name or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", new_name):
        return {
            "format": "appgen.lsp-rename.v1",
            "ok": False,
            "token": token,
            "diagnostics": (
                _spec_diagnostic(source, "AGX0100", "error", "Rename requires a valid identifier."),
            ),
        }
    symbol = _lsp_symbol_for_token(source, token, source_name=source_name)
    if not symbol:
        return {
            "format": "appgen.lsp-rename.v1",
            "ok": False,
            "token": token,
            "diagnostics": (
                _spec_diagnostic(source, "AGX0100", "error", f"Cannot rename unknown symbol: {token}"),
            ),
        }
    new_text = re.sub(rf"\b{re.escape(token)}\b", new_name, source)
    lint = lint_report_dsl(new_text, source_name=source_name)
    migration = migration_plan_dsl(source, new_text, previous_name=source_name, current_name=source_name)
    return {
        "format": "appgen.lsp-rename.v1",
        "ok": lint["ok"],
        "token": token,
        "new_name": new_name,
        "symbol": symbol,
        "workspace_edit": {
            "changes": {
                source_name or "memory://appgen": (
                    {
                        "range": {
                            "start": {"line": 0, "character": 0},
                            "end": {"line": len(source.splitlines()), "character": 0},
                        },
                        "newText": new_text,
                    },
                )
            }
        },
        "lint": lint,
        "migration_preview": migration,
    }


def _parse_lsp_position(value: str | None) -> dict | None:
    if not value:
        return None
    match = re.match(r"(?P<line>\d+):(?P<char>\d+)$", value.strip())
    if not match:
        return None
    return {"line": int(match.group("line")), "character": int(match.group("char"))}


def _lsp_diagnostic(diagnostic: dict) -> dict:
    return {
        "range": _lsp_range(diagnostic.get("range")),
        "severity": {"error": 1, "warning": 2, "info": 3, "hint": 4}.get(diagnostic.get("severity"), 3),
        "code": diagnostic.get("code"),
        "source": "appgen",
        "message": diagnostic.get("message"),
        "data": {
            "title": diagnostic.get("title"),
            "docs_url": diagnostic.get("docs_url"),
            "fixes": diagnostic.get("fixes", ()),
        },
    }


def _lsp_completion_kind(kind: str) -> int:
    return {
        "keyword": 14,
        "snippet": 15,
        "table": 7,
        "field": 5,
        "reference": 18,
        "llm": 9,
        "flow": 3,
    }.get(kind, 12)


def _lsp_symbol_kind(kind: str) -> int:
    return {
        "app": 2,
        "table": 5,
        "field": 8,
        "enum": 10,
        "enum_value": 22,
        "view": 5,
        "handler": 12,
        "flow": 12,
        "flow_state": 13,
        "operation": 12,
        "role": 5,
        "rule": 12,
        "llm": 13,
        "agent": 5,
        "pbc": 5,
        "composition": 5,
        "api": 12,
        "event": 12,
        "package": 5,
    }.get(kind, 13)


def _lsp_document_symbol(symbol: dict) -> dict:
    symbol_range = _lsp_range(symbol.get("range"))
    return {
        "name": symbol["name"],
        "kind": _lsp_symbol_kind(symbol["kind"]),
        "range": symbol_range,
        "selectionRange": symbol_range,
        "detail": symbol["kind"],
        "data": {"id": symbol["id"]},
    }


def _lsp_range(range_value: dict | None) -> dict:
    if not range_value:
        return {
            "start": {"line": 0, "character": 0},
            "end": {"line": 0, "character": 0},
        }
    return {
        "start": {
            "line": max(int(range_value["start"]["line"]) - 1, 0),
            "character": int(range_value["start"]["character"]),
        },
        "end": {
            "line": max(int(range_value["end"]["line"]) - 1, 0),
            "character": int(range_value["end"]["character"]),
        },
    }


def _lsp_location(source_name: str | None, range_value: dict | None) -> dict:
    return {"uri": source_name or "memory://appgen", "range": _lsp_range(range_value)}


def _lsp_token_at_position(source: str, position: dict | None) -> str:
    if not source:
        return ""
    if not position:
        match = re.search(r"[A-Za-z_][A-Za-z0-9_]*", source)
        return match.group(0) if match else ""
    lines = source.splitlines()
    line_index = int(position.get("line", 0))
    if line_index < 0 or line_index >= len(lines):
        return ""
    line = lines[line_index]
    character = max(min(int(position.get("character", 0)), len(line)), 0)
    for match in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*", line):
        if match.start() <= character <= match.end():
            return match.group(0)
    return ""


def _lsp_token_range(source: str, position: dict | None, token: str) -> dict:
    if not token:
        return _lsp_range(None)
    lines = source.splitlines()
    line_index = int((position or {}).get("line", 0))
    if 0 <= line_index < len(lines):
        index = lines[line_index].find(token)
        if index >= 0:
            return {
                "start": {"line": line_index, "character": index},
                "end": {"line": line_index, "character": index + len(token)},
            }
    line, column = _locate_token(source, token)
    return _lsp_range(_semantic_range(line, column, token))


def _lsp_symbol_for_token(source: str, token: str, *, source_name: str | None = None) -> dict | None:
    if not token:
        return None
    semantic = semantic_model_dsl(source, source_name=source_name)
    exact_candidates = [
        symbol
        for symbol in semantic.get("symbols", {}).values()
        if symbol.get("name") == token or symbol.get("id") == token
    ]
    if exact_candidates:
        return sorted(exact_candidates, key=lambda item: 0 if item["kind"] in {"table", "view", "flow", "operation"} else 1)[0]
    return semantic.get("symbols", {}).get(_symbol_query_to_id(token))


def _lsp_diagnostic_for_token(source: str, token: str, *, source_name: str | None = None) -> dict | None:
    if not token:
        return None
    for diagnostic in lint_report_dsl(source, source_name=source_name)["diagnostics"]:
        if token in diagnostic.get("message", ""):
            return diagnostic
    return None


def _lsp_occurrence_ranges(source: str, token: str) -> tuple[dict, ...]:
    if not token:
        return ()
    ranges = []
    for line_index, line in enumerate(source.splitlines()):
        for match in re.finditer(rf"\b{re.escape(token)}\b", line):
            ranges.append(
                {
                    "start": {"line": line_index + 1, "character": match.start()},
                    "end": {"line": line_index + 1, "character": match.end()},
                }
            )
    return tuple(ranges)


def _lsp_required_quick_actions(text: str, *, source_name: str | None = None) -> tuple[dict, ...]:
    actions = []
    report = lint_report_dsl(text, source_name=source_name)
    for diagnostic in report["diagnostics"]:
        actions.extend(_lsp_required_actions_for_diagnostic(text or "", diagnostic, source_name=source_name))
    actions.extend(_lsp_missing_package_actions(text or "", source_name=source_name))
    return tuple({action["data"]["id"] + ":" + action["title"]: action for action in actions}.values())


def _lsp_required_actions_for_diagnostic(source: str, diagnostic: dict, *, source_name: str | None = None) -> tuple[dict, ...]:
    code = diagnostic.get("code")
    message = diagnostic.get("message", "")
    actions: list[dict] = []
    if code in {"AGX0301", "AGX0401"}:
        table = _missing_table_name(message)
        if table:
            actions.append(_lsp_append_action(source, source_name, diagnostic, "create_missing_table", f"Create table {table}", f"\ntable {table} {{\n  id: int pk\n  name: string\n}}\n"))
    if code in {"AGX0302", "AGX0402", "AGX0502"}:
        table, field = _missing_field_target(message, source)
        if table and field and "." not in field:
            actions.append(_lsp_insert_in_block_action(source, source_name, diagnostic, "create_missing_field", f"Create field {table}.{field}", "table", table, f"  {field}: string\n"))
    if code == "AGX0303":
        view, binding = _view_binding_from_message(message)
        table = _view_table_for_view(source, view)
        field = binding.rsplit(".", 1)[-1] if binding else "display_value"
        if table:
            actions.append(_lsp_insert_in_block_action(source, source_name, diagnostic, "create_calculated_field_for_binding", f"Create calculated field {table}.{field}", "table", table, f"  {field}: string = \"TODO\"\n"))
            actions.append(_lsp_insert_in_block_action(source, source_name, diagnostic, "add_lookup_directive", f"Add lookup directive for {binding}", "table", table, f"  lookup {field} ({binding})\n"))
    if code == "AGX0403":
        target = _handler_target_from_message(message)
        if target:
            actions.append(_lsp_append_action(source, source_name, diagnostic, "create_operation_from_handler", f"Create operation {target}", f"\noperation {target} {{\n  step validate -> complete\n}}\n"))
            actions.append(_lsp_append_action(source, source_name, diagnostic, "create_flow_from_handler", f"Create flow {target}", f"\nflow {target} {{\n  draft -> complete\n}}\n"))
    if code == "AGX0901":
        pbc = _diagnostic_token(message)
        if pbc:
            actions.append(_lsp_append_action(source, source_name, diagnostic, "register_or_import_pbc_manifest", f"Declare PBC {pbc}", f"\npbc {pbc} {{\n  label: \"{pbc}\"\n  datastore: postgresql\n}}\n"))
    if code == "AGX0902":
        contract = _missing_contract_name(message)
        if contract:
            actions.append(_lsp_append_action(source, source_name, diagnostic, "create_event_contract", f"Create event contract {contract}", f"\nevent {contract} {{\n  topic: pbc.events\n}}\n"))
    if code == "AGX1002":
        agent = _agent_name_from_message(message)
        if agent:
            actions.append(_lsp_insert_in_block_action(source, source_name, diagnostic, "add_missing_permission_for_agent_skill", f"Add permission for {agent}", "agent", agent, "  GeneratedResource: write\n"))
    if code == "AGX0702":
        actions.append(_lsp_replace_action(source, source_name, diagnostic, "replace_secret_literal_with_env", "Replace secret literal with env binding", r"api_key\s*:\s*['\"][^'\"]+['\"]", "api_key: OPENAI_API_KEY"))
    if diagnostic.get("legacy_code") in {"unknown_view_field", "unknown_component_field", "unknown_rule_field"} or diagnostic.get("hint"):
        token = _diagnostic_token(message)
        hint = diagnostic.get("hint") or _nearest_symbol_hint(source, token)
        if token and hint:
            actions.append(_lsp_replace_action(source, source_name, diagnostic, "replace_typo_with_nearest_symbol", f"Replace {token} with {hint}", rf"\b{re.escape(token)}\b", hint, first_only=True))
    return tuple(actions)


def _lsp_missing_package_actions(source: str, *, source_name: str | None = None) -> tuple[dict, ...]:
    semantic = semantic_model_dsl(source, source_name=source_name)
    targets = set(semantic.get("app", {}).get("targets", ()))
    packages = semantic.get("packages", {})
    declared_targets = {
        target
        for package in packages.values()
        for target in package.get("options", {}).get("target", ()) + package.get("options", {}).get("targets", ())
    }
    missing = tuple(sorted(targets - declared_targets))
    actions = []
    for target in missing:
        package_name = f"{_pascal_case(target)}Package"
        actions.append(_lsp_append_action(source, source_name, None, "add_package_for_app_target", f"Add package for {target}", f"\npackage {package_name} {{\n  target: {target}\n  smoke: launch\n}}\n"))
    if semantic.get("flows") and not semantic.get("contracts", {}).get("test"):
        first_flow = next(iter(semantic["flows"]))
        actions.append(_lsp_append_action(source, source_name, None, "create_smoke_test_declaration", f"Create smoke test for {first_flow}", f"\ntest {first_flow}Smoke {{\n  run happy_path -> {first_flow}\n}}\n"))
    return tuple(actions)


def _lsp_append_action(source: str, source_name: str | None, diagnostic: dict | None, action_id: str, title: str, new_text: str) -> dict:
    line_count = len(source.splitlines())
    return _lsp_edit_action(source_name, diagnostic, action_id, title, ({"range": {"start": {"line": line_count, "character": 0}, "end": {"line": line_count, "character": 0}}, "newText": new_text},))


def _lsp_insert_in_block_action(source: str, source_name: str | None, diagnostic: dict | None, action_id: str, title: str, kind: str, name: str, new_text: str) -> dict:
    line = _closing_line_for_block(source, kind, name)
    if line is None:
        return _lsp_append_action(source, source_name, diagnostic, action_id, title, f"\n{kind} {name} {{\n{new_text}}}\n")
    return _lsp_edit_action(source_name, diagnostic, action_id, title, ({"range": {"start": {"line": line, "character": 0}, "end": {"line": line, "character": 0}}, "newText": new_text},))


def _lsp_replace_action(
    source: str,
    source_name: str | None,
    diagnostic: dict | None,
    action_id: str,
    title: str,
    pattern: str,
    replacement: str,
    *,
    first_only: bool = False,
) -> dict:
    regex = re.compile(pattern)
    matches = tuple(regex.finditer(source))
    selected = matches[:1] if first_only else matches
    edits = tuple(
        {"range": _source_range(source, match.start(), match.end()), "newText": match.expand(replacement)}
        for match in selected
    )
    return _lsp_edit_action(source_name, diagnostic, action_id, title, edits)


def _lsp_edit_action(source_name: str | None, diagnostic: dict | None, action_id: str, title: str, edits: tuple[dict, ...]) -> dict:
    return {
        "title": title,
        "kind": "quickfix",
        "diagnostics": (_lsp_diagnostic(diagnostic),) if diagnostic else (),
        "edit": {"changes": {source_name or "memory://appgen": edits}},
        "data": {"id": action_id, "changed": bool(edits)},
    }


def _missing_table_name(message: str) -> str | None:
    for pattern in (r"Unknown view table: [^.]+ for ([A-Za-z_][A-Za-z0-9_]*)", r"Unknown (?:relation|reference) target table: ([A-Za-z_][A-Za-z0-9_]*)"):
        match = re.search(pattern, message)
        if match:
            return match.group(1)
    return None


def _missing_field_target(message: str, source: str) -> tuple[str | None, str | None]:
    for pattern in (
        r"Unknown (?:relation|reference) target field: ([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown rule field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown (?:view|component) field: ([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)",
    ):
        match = re.search(pattern, message)
        if match and len(match.groups()) == 2:
            left, right = match.groups()
            return (_view_table_for_view(source, left) or left, right)
        if match and len(match.groups()) == 1:
            table = _rule_table_from_message(message, source)
            return (table, match.group(1))
    return None, None


def _view_binding_from_message(message: str) -> tuple[str | None, str | None]:
    match = re.search(r"(?:Unresolved lookup path|Multi-hop lookup chain breaks): ([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_.]*)", message)
    return (match.group(1), match.group(2)) if match else (None, None)


def _handler_target_from_message(message: str) -> str | None:
    match = re.search(r"Unknown handler target:\s+[A-Za-z_][A-Za-z0-9_]*\.([A-Za-z_][A-Za-z0-9_]*)", message)
    return match.group(1) if match else _diagnostic_token(message)


def _missing_contract_name(message: str) -> str | None:
    match = re.search(r"Unknown cross-PBC contract: .*?(?:event|domain_event|command|api)\s+([A-Za-z_][A-Za-z0-9_]*)", message)
    return match.group(1) if match else None


def _agent_name_from_message(message: str) -> str | None:
    match = re.search(r"Agent write-capable skill has no permission: ([A-Za-z_][A-Za-z0-9_]*)\.", message)
    return match.group(1) if match else None


def _view_table_for_view(source: str, view_name: str | None) -> str | None:
    if not view_name:
        return None
    match = re.search(rf"\bview\s+{re.escape(view_name)}\s+for\s+([A-Za-z_][A-Za-z0-9_]*)", source)
    return match.group(1) if match else None


def _rule_table_from_message(message: str, source: str) -> str | None:
    match = re.search(r"Unknown rule field: ([A-Za-z_][A-Za-z0-9_]*)\.", message)
    if not match:
        return None
    rule = match.group(1)
    rule_match = re.search(rf"\brule\s+{re.escape(rule)}\s+for\s+([A-Za-z_][A-Za-z0-9_]*)", source)
    return rule_match.group(1) if rule_match else None


def _closing_line_for_block(source: str, kind: str, name: str) -> int | None:
    pattern = re.compile(rf"\b{kind}\s+{re.escape(name)}\b[^\{{]*\{{")
    match = pattern.search(source)
    if not match:
        return None
    depth = 1
    for index in range(match.end(), len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source.count("\n", 0, index)
    return None


def _nearest_symbol_hint(source: str, token: str | None) -> str | None:
    if not token:
        return None
    semantic = semantic_model_dsl(source)
    candidates = [symbol["name"] for symbol in semantic.get("symbols", {}).values()]
    if not candidates:
        candidates = [
            field
            for fields in _declared_table_fields_for_suggestions(source).values()
            for field in fields
        ]
    matches = difflib.get_close_matches(token, candidates, n=1)
    return matches[0] if matches else None


def designer_sync_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    visual_edit: dict | None = None,
) -> dict:
    """Return Studio/visual-designer state synchronized with the DSL model."""
    source = text or ""
    semantic = semantic_model_dsl(source, source_name=source_name)
    lsp = lsp_service_dsl(source, source_name=source_name)
    projections = {
        "dsl_editor": {
            "format": "appgen.designer-dsl-editor.v1",
            "semantic_model_format": semantic.get("format"),
            "diagnostics": lsp["publishDiagnostics"],
            "outline": lsp["documentSymbol"],
            "code_actions": lsp["codeAction"],
            "formatting": lsp["formatting"],
        },
        "component_palette": _designer_component_palette(semantic),
        "form_designer": _designer_form_projection(semantic),
        "database_designer": _designer_database_projection(semantic),
        "workflow_designer": _designer_workflow_projection(semantic),
        "pbc_composition_designer": _designer_pbc_projection(semantic),
        "package_deployment_designer": _designer_package_deployment_projection(semantic),
        "diagnostics_panel": lsp["publishDiagnostics"],
        "graph_explain_panel": {
            "format": "appgen.designer-graph-explain-panel.v1",
            "graphs": semantic.get("graphs", {}),
            "available_explain_queries": tuple(semantic.get("symbols", {}).keys()),
        },
        "natural_language_planner": {
            "format": "appgen.designer-nl-planner-panel.v1",
            "command": "appgen nl-plan",
            "requires_dsl_diff_preview": True,
            "token_budget_notes": _nl_token_budget_notes(),
        },
    }
    edit_result = _designer_visual_edit_result(source, visual_edit, source_name=source_name) if visual_edit else None
    checks = (
        _release_check("dsl_editor_bound_to_lsp", projections["dsl_editor"]["semantic_model_format"] == "appgen.semantic-model.v1"),
        _release_check("form_designer_bound_to_semantic_model", projections["form_designer"]["semantic_model_format"] == "appgen.semantic-model.v1"),
        _release_check("database_designer_bound_to_semantic_model", projections["database_designer"]["semantic_model_format"] == "appgen.semantic-model.v1"),
        _release_check("workflow_designer_bound_to_semantic_model", projections["workflow_designer"]["semantic_model_format"] == "appgen.semantic-model.v1"),
        _release_check("pbc_designer_bound_to_semantic_model", projections["pbc_composition_designer"]["semantic_model_format"] == "appgen.semantic-model.v1"),
        _release_check("package_deployment_designer_bound_to_semantic_model", projections["package_deployment_designer"]["semantic_model_format"] == "appgen.semantic-model.v1"),
        _release_check("visual_edit_round_trips", edit_result is None or edit_result["round_trip_ok"]),
        _release_check("invalid_visual_edits_rejected", edit_result is None or edit_result["accepted"] or bool(edit_result["diagnostics"])),
    )
    return {
        "format": "appgen.designer-sync-report.v1",
        "ok": semantic["ok"] and all(check["ok"] for check in checks),
        "source": source_name,
        "semantic_model_format": semantic.get("format"),
        "surfaces": tuple(projections.keys()),
        "projections": projections,
        "visual_edit": edit_result,
        "checks": checks,
        "blocking_gaps": tuple(check["check"] for check in checks if not check["ok"]),
    }


def _designer_component_palette(semantic: dict) -> dict:
    field_types = {
        field.get("type")
        for table in semantic.get("tables", {}).values()
        for field in table.get("fields", {}).values()
    }
    return {
        "format": "appgen.designer-component-palette.v1",
        "semantic_model_format": semantic.get("format"),
        "components": (
            {"component": "TextBox", "binds": ("string", "email", "text"), "icon": "type"},
            {"component": "NumberInput", "binds": ("int", "decimal", "float"), "icon": "hash"},
            {"component": "CheckBox", "binds": ("bool",), "icon": "check-square"},
            {"component": "DatePicker", "binds": ("date", "datetime", "time"), "icon": "calendar"},
            {"component": "Lookup", "binds": ("relationship", "lookup_path"), "icon": "list-search"},
            {"component": "Button", "binds": ("handler",), "icon": "square-mouse-pointer"},
        ),
        "field_types": tuple(sorted(item for item in field_types if item)),
    }


def _designer_form_projection(semantic: dict) -> dict:
    return {
        "format": "appgen.designer-form-projection.v1",
        "semantic_model_format": semantic.get("format"),
        "views": tuple(
            {
                "view": name,
                "table": view.get("table"),
                "sections": view.get("sections", ()),
                "components": view.get("components", ()),
                "handlers": view.get("handlers", ()),
                "valid_bindings": tuple(_valid_bindings_for_table(semantic, view.get("table"))),
            }
            for name, view in semantic.get("views", {}).items()
        ),
    }


def _designer_database_projection(semantic: dict) -> dict:
    return {
        "format": "appgen.designer-database-projection.v1",
        "semantic_model_format": semantic.get("format"),
        "tables": tuple(semantic.get("tables", {}).values()),
        "er_graph": semantic.get("graphs", {}).get("er", {}),
        "lookup_graph": semantic.get("graphs", {}).get("lookup", {}),
    }


def _designer_workflow_projection(semantic: dict) -> dict:
    return {
        "format": "appgen.designer-workflow-projection.v1",
        "semantic_model_format": semantic.get("format"),
        "flows": tuple(semantic.get("flows", {}).values()),
        "workflow_graph": semantic.get("graphs", {}).get("workflow", {}),
        "handler_graph": semantic.get("graphs", {}).get("handler", {}),
    }


def _designer_pbc_projection(semantic: dict) -> dict:
    return {
        "format": "appgen.designer-pbc-composition-projection.v1",
        "semantic_model_format": semantic.get("format"),
        "pbcs": semantic.get("pbcs", {}),
        "composition": semantic.get("composition", {}),
        "pbc_graph": semantic.get("graphs", {}).get("pbc", {}),
    }


def _designer_package_deployment_projection(semantic: dict) -> dict:
    return {
        "format": "appgen.designer-package-deployment-projection.v1",
        "semantic_model_format": semantic.get("format"),
        "packages": semantic.get("packages", {}),
        "deployment": semantic.get("deployment", {}),
        "package_graph": semantic.get("graphs", {}).get("package", {}),
        "deployment_graph": semantic.get("graphs", {}).get("deployment", {}),
    }


def _valid_bindings_for_table(semantic: dict, table_name: str | None) -> tuple[str, ...]:
    table = semantic.get("tables", {}).get(table_name or "")
    if not table:
        return ()
    fields = tuple(table.get("fields", {}).keys())
    lookups = tuple(path for path, detail in table.get("lookup_paths", {}).items() if detail.get("valid"))
    return fields + lookups


def _designer_visual_edit_result(source: str, visual_edit: dict | None, *, source_name: str | None = None) -> dict:
    patch = _designer_edit_to_patch(source, visual_edit or {})
    patched_source = _append_dsl_patch(source, patch) if patch else source
    lint = lint_report_dsl(patched_source, source_name=source_name)
    semantic = semantic_model_dsl(patched_source, source_name=source_name)
    accepted = bool(patch) and lint["ok"]
    return {
        "format": "appgen.designer-visual-edit-result.v1",
        "operation": (visual_edit or {}).get("kind"),
        "accepted": accepted,
        "dsl_patch": patch,
        "patched_source": patched_source,
        "lint": lint,
        "diagnostics": tuple(lint["diagnostics"]),
        "round_trip_ok": accepted and semantic["ok"],
        "semantic_model_format": semantic.get("format"),
    }


def _designer_edit_to_patch(source: str, edit: dict) -> str:
    kind = edit.get("kind")
    if kind == "add_table":
        fields = tuple(edit.get("fields") or ({"name": "name", "type": "string", "required": True},))
        lines = [f"table {_pascal_case(str(edit.get('table') or edit.get('name') or 'NewTable'))} {{", "  id: int pk"]
        for field in fields:
            field_name = _snake_case(str(field.get("name", "field")))
            type_name = str(field.get("type") or field.get("type_name") or "string")
            required = " required" if field.get("required") else ""
            lines.append(f"  {field_name}: {type_name}{required}")
        lines.append("}")
        return "\n".join(lines)
    if kind == "add_field":
        table = _pascal_case(str(edit.get("table", "")))
        field = _snake_case(str(edit.get("field") or edit.get("name") or "field"))
        type_name = str(edit.get("type") or edit.get("type_name") or "string")
        return f"// edit table {table}: add {field}: {type_name}"
    if kind == "add_component":
        return _designer_component_patch(edit)
    if kind == "add_flow_transition":
        flow = _pascal_case(str(edit.get("flow", "")))
        source_state = _snake_case(str(edit.get("from", "draft")))
        target_state = _snake_case(str(edit.get("to", "done")))
        if re.search(rf"\bflow\s+{re.escape(flow)}\s*\{{", source):
            return f"// edit flow {flow}: add transition {source_state} -> {target_state}"
        return f"flow {flow} {{\n  {source_state} -> {target_state}\n}}"
    if kind == "add_pbc_include":
        pbc = str(edit.get("pbc", "")).strip()
        composition = _pascal_case(str(edit.get("composition") or "AppComposition"))
        return f"composition {composition} {{\n  include pbc {pbc} version {edit.get('version', '1.0.0')}\n}}"
    if kind == "add_package":
        name = _pascal_case(str(edit.get("name") or f"{edit.get('target', 'web')}Package"))
        target = str(edit.get("target", "web")).lower()
        return f"package {name} {{\n  target: {target}\n  smoke: launch\n}}"
    if kind == "add_deployment_unit":
        deploy = _pascal_case(str(edit.get("deployment") or "Production"))
        target = str(edit.get("target") or edit.get("unit") or "app")
        pattern = str(edit.get("pattern") or "service")
        return f"deploy {deploy} {{\n  unit {target} as {pattern}\n  health {target} \"/health\"\n}}"
    return ""


def _designer_component_patch(edit: dict) -> str:
    view = _pascal_case(str(edit.get("view", "")))
    binding = str(edit.get("binding") or edit.get("field") or "")
    component = str(edit.get("component") or "TextBox")
    x = int(edit.get("x", 0))
    y = int(edit.get("y", 0))
    w = int(edit.get("w", 4))
    h = int(edit.get("h", 1))
    return f"// edit view {view}: add component {binding} {component} {x} {y} {w} {h}"


def _append_to_existing_block(source: str, kind: str, name: str, line: str) -> str:
    if not name:
        return ""
    pattern = re.compile(rf"({kind}\s+{re.escape(name)}\b[^\{{]*\{{)(?P<body>.*?)(\n\}})", re.S)
    match = pattern.search(source)
    if match is None:
        return ""
    body = match.group("body").rstrip()
    return source[: match.start()] + f"{match.group(1)}{body}\n{line}{match.group(3)}" + source[match.end() :]


def release_verifier_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    targets: Iterable[str] | None = None,
    output_dir: str | None = None,
) -> dict:
    """Return machine-readable release verifier evidence for DSL tooling."""
    source = text or ""
    semantic = semantic_model_dsl(source, source_name=source_name)
    requested_targets = _release_requested_targets(targets, semantic)
    reports = {
        "web": web_verifier_report_dsl(source, source_name=source_name, semantic=semantic),
        "mobile": mobile_verifier_report_dsl(source, source_name=source_name, semantic=semantic),
        "desktop": desktop_verifier_report_dsl(source, source_name=source_name, semantic=semantic),
        "pbc": pbc_composition_verifier_report_dsl(source, source_name=source_name, semantic=semantic),
        "deployment": deployment_verifier_report_dsl(source, source_name=source_name, semantic=semantic),
    }
    selected_keys = tuple(key for key in ("web", "mobile", "desktop", "pbc", "deployment") if key in requested_targets)
    if not selected_keys:
        selected_keys = ("web", "mobile", "desktop", "pbc", "deployment")
    selected_reports = {key: reports[key] for key in selected_keys}
    checks = tuple(
        {
            "verifier": key,
            "ok": report["ok"],
            "blocking_gaps": report.get("blocking_gaps", ()),
        }
        for key, report in selected_reports.items()
    )
    return {
        "format": "appgen.release-verifier-report.v1",
        "ok": semantic["ok"] and all(check["ok"] for check in checks),
        "source": source_name,
        "output_dir": output_dir,
        "semantic_model_format": semantic["format"],
        "targets": selected_keys,
        "checks": checks,
        "reports": selected_reports,
        "diagnostics": semantic["diagnostics"],
        "evidence_bundle": {
            "format": "appgen.release-evidence-bundle.v1",
            "source": source_name,
            "artifacts": tuple(f"{key}:{report['format']}" for key, report in selected_reports.items()),
            "requires_generation": any(
                gap in {"app_build_not_observed", "smoke_tests_not_declared", "smoke_launch_not_declared"}
                for report in selected_reports.values()
                for gap in report.get("blocking_gaps", ())
            ),
        },
    }


def web_verifier_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    semantic: dict | None = None,
) -> dict:
    semantic = semantic or semantic_model_dsl(text, source_name=source_name)
    lint = lint_report_dsl(text, source_name=source_name)
    app_targets = semantic.get("app", {}).get("targets", ())
    route_sources = _release_route_sources(semantic)
    checks = (
        _release_check("target_declared", "web" in app_targets or "pwa" in app_targets),
        _release_check("app_build_contract", bool(semantic.get("packages")) or bool(semantic.get("app"))),
        _release_check("routes_exist", bool(route_sources) or bool(semantic.get("views"))),
        _release_check("generated_forms_bind_valid_fields", not _has_diagnostic(lint, {"AGX0401", "AGX0402", "AGX0303"})),
        _release_check("handler_targets_resolve", not _has_diagnostic(lint, {"AGX0403"})),
        _release_check("smoke_tests_declared", bool(semantic.get("contracts", {}).get("test")) or _package_option_present(semantic, "smoke")),
    )
    return _release_verifier_payload("web", "appgen.web-verifier.v1", checks, semantic)


def mobile_verifier_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    semantic: dict | None = None,
) -> dict:
    semantic = semantic or semantic_model_dsl(text, source_name=source_name)
    mobile_packages = _packages_for_target(semantic, "mobile")
    checks = (
        _release_check("target_declared", "mobile" in semantic.get("app", {}).get("targets", ())),
        _release_check("package_metadata_exists", bool(mobile_packages)),
        _release_check("signing_posture_declared", any(_contract_option_present(package, "signing", "signature") for package in mobile_packages)),
        _release_check("offline_policy_declared", any(_contract_option_present(package, "offline", "cache", "sync") for package in mobile_packages)),
        _release_check("permissions_explained", any(_contract_option_present(package, "permission", "permissions") for package in mobile_packages) or bool(semantic.get("roles"))),
        _release_check("screens_fit_target_density", _components_fit_density(semantic, max_width=12, max_height=24)),
        _release_check("smoke_launch_path_exists", any(_contract_option_present(package, "smoke", "launch") for package in mobile_packages)),
    )
    return _release_verifier_payload("mobile", "appgen.mobile-verifier.v1", checks, semantic)


def desktop_verifier_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    semantic: dict | None = None,
) -> dict:
    semantic = semantic or semantic_model_dsl(text, source_name=source_name)
    desktop_packages = _packages_for_target(semantic, "desktop")
    checks = (
        _release_check("target_declared", "desktop" in semantic.get("app", {}).get("targets", ())),
        _release_check("package_metadata_exists", bool(desktop_packages)),
        _release_check("installer_or_update_posture_declared", any(_contract_option_present(package, "installer", "update", "format") for package in desktop_packages)),
        _release_check("splash_or_startup_assets_declared_when_used", any(_contract_option_present(package, "splash", "startup", "asset", "assets") for package in desktop_packages)),
        _release_check("menus_and_context_menus_bind_to_handlers", _menus_bind_to_handlers(semantic)),
        _release_check("smoke_launch_path_exists", any(_contract_option_present(package, "smoke", "launch") for package in desktop_packages)),
    )
    return _release_verifier_payload("desktop", "appgen.desktop-verifier.v1", checks, semantic)


def pbc_composition_verifier_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    semantic: dict | None = None,
) -> dict:
    del text, source_name
    semantic = semantic or {}
    pbcs = semantic.get("pbcs", {})
    composition = semantic.get("composition", {})
    checks = (
        _release_check("manifest_validates", all(pbc.get("catalog_resolved") for pbc in pbcs.values()) if pbcs else True),
        _release_check("package_artifacts_exist", all(_pbc_catalog_has_artifacts(pbc.get("catalog")) for pbc in pbcs.values()) if pbcs else True),
        _release_check("owned_tables_have_migrations_models", all(_pbc_catalog_has_schema_artifacts(pbc.get("catalog")) for pbc in pbcs.values()) if pbcs else True),
        _release_check("apis_events_handlers_declared", all(_pbc_catalog_has_contracts(pbc.get("catalog")) for pbc in pbcs.values()) if pbcs else True),
        _release_check("no_private_cross_pbc_table_mutation", not _composition_uses_private_tables(composition)),
        _release_check("self_registration_side_effect_free", all(_pbc_catalog_side_effect_free(pbc.get("catalog")) for pbc in pbcs.values()) if pbcs else True),
        _release_check("release_evidence_exists", all(_pbc_catalog_has_release_evidence(pbc.get("catalog")) for pbc in pbcs.values()) if pbcs else True),
    )
    return _release_verifier_payload("pbc", "appgen.pbc-verifier.v1", checks, semantic, {"pbcs": tuple(pbcs)})


def deployment_verifier_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    semantic: dict | None = None,
) -> dict:
    del text, source_name
    semantic = semantic or {}
    deployments = semantic.get("deployment", {})
    checks_by_deployment = {
        name: _deployment_verifier_checks(name, deployment)
        for name, deployment in deployments.items()
    }
    checks = tuple(
        check
        for deployment_checks in checks_by_deployment.values()
        for check in deployment_checks
    )
    if not checks:
        checks = (_release_check("units_declared", True),)
    return _release_verifier_payload(
        "deployment",
        "appgen.deployment-verifier.v1",
        checks,
        semantic,
        {"deployments": checks_by_deployment},
    )


def pbc_verifier_catalog_report() -> dict:
    catalog = _pbc_catalog_by_key()
    items = tuple(
        {
            "pbc": key,
            "ok": pbc_verifier_report(key)["ok"],
            "label": item.get("label"),
            "mesh": item.get("mesh"),
            "datastore_backend": item.get("datastore_backend"),
        }
        for key, item in sorted(catalog.items())
    )
    return {
        "format": "appgen.pbc-verifier-catalog.v1",
        "ok": all(item["ok"] for item in items),
        "count": len(items),
        "pbcs": items,
    }


def pbc_verifier_report(pbc_key_or_path: str) -> dict:
    key = Path(pbc_key_or_path).name
    catalog = _pbc_catalog_by_key()
    item = catalog.get(key) or catalog.get(str(pbc_key_or_path))
    checks = (
        _release_check("manifest_validates", item is not None),
        _release_check("package_artifacts_exist", _pbc_catalog_has_artifacts(item)),
        _release_check("owned_tables_have_migrations_models", _pbc_catalog_has_schema_artifacts(item)),
        _release_check("apis_events_handlers_declared", _pbc_catalog_has_contracts(item)),
        _release_check("no_private_cross_pbc_table_mutation", item is not None and not item.get("shared_table_access", False)),
        _release_check("self_registration_side_effect_free", _pbc_catalog_side_effect_free(item)),
        _release_check("release_evidence_exists", _pbc_catalog_has_release_evidence(item)),
    )
    payload = _release_verifier_payload(
        "pbc",
        "appgen.pbc-package-verifier.v1",
        checks,
        {},
        {"pbc": key, "catalog": item or {}},
    )
    return payload


def pbc_publish_report(pbc_key_or_path: str, *, catalog: str = "local", catalog_path: str | None = None) -> dict:
    """Return a side-effect-free PBC publish plan and catalog patch evidence."""
    package_ref = _pbc_publish_ref(pbc_key_or_path)
    load_report = _load_pbc_publish_package(package_ref)
    manifest = load_report.get("manifest") if load_report.get("ok") else None
    registration = load_report.get("registration", {})
    validation = registration.get("validation", {})
    catalog_patch = registration.get("catalog_patch")
    key = (manifest or {}).get("pbc") or Path(str(pbc_key_or_path)).name
    release_evidence = _pbc_publish_release_evidence(key)
    target = {
        "mode": catalog,
        "catalog_path": catalog_path,
        "side_effect_free": True,
        "write_performed": False,
    }
    checks = (
        _release_check(
            "package_loads",
            load_report.get("ok", False),
            detail={"source": str(package_ref), "error": load_report.get("error")},
        ),
        _release_check(
            "manifest_validates",
            validation.get("ok", False),
            detail={"invalid": validation.get("invalid", ())},
        ),
        _release_check(
            "manifest_publishable",
            validation.get("publishable", False),
            detail={"missing_publish_artifacts": validation.get("missing_publish_artifacts", ())},
        ),
        _release_check("catalog_patch_available", bool(catalog_patch), detail={"catalog": catalog}),
        _release_check(
            "release_evidence_exists",
            bool(release_evidence.get("ok")),
            detail={"format": release_evidence.get("format")},
        ),
        _release_check("publish_is_side_effect_free", True, detail=target),
    )
    return {
        "format": "appgen.pbc-publish-report.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": key,
        "source": str(pbc_key_or_path),
        "package_ref": str(package_ref),
        "target": target,
        "load_report": load_report,
        "registration": registration,
        "catalog_patch": catalog_patch,
        "release_evidence": release_evidence,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "next_actions": registration.get("next_actions", ()),
    }


def _load_pbc_publish_package(package_ref: str | Path) -> dict:
    try:
        from .pbc import load_pbc_package
    except Exception as exc:  # pragma: no cover - optional package boundary
        return {
            "format": "appgen.pbc-package-load-report.v1",
            "ok": False,
            "source": str(package_ref),
            "error": str(exc),
        }
    return load_pbc_package(package_ref, existing_catalog={})


def _pbc_publish_ref(pbc_key_or_path: str) -> str | Path:
    raw = Path(str(pbc_key_or_path))
    if raw.exists():
        module_ref = _pbc_source_path_to_module(raw)
        return module_ref or raw
    return str(pbc_key_or_path)


def _pbc_source_path_to_module(path: Path) -> str | None:
    parts = path.resolve().parts
    try:
        index = parts.index("pyAppGen")
    except ValueError:
        return None
    if len(parts) >= index + 3 and parts[index + 1] == "pbcs":
        return ".".join(parts[index : index + 3])
    return None


def _pbc_publish_release_evidence(key: str) -> dict:
    catalog = _pbc_catalog_by_key()
    if key in catalog:
        return pbc_verifier_report(key)
    return {
        "format": "appgen.pbc-package-verifier.v1",
        "ok": False,
        "kind": "pbc",
        "pbc": key,
        "blocking_gaps": ("release_evidence_not_registered",),
        "checks": (_release_check("release_evidence_exists", False),),
    }


def _release_requested_targets(targets: Iterable[str] | None, semantic: dict) -> tuple[str, ...]:
    explicit = tuple(str(target).strip().lower() for target in (targets or ()) if str(target).strip())
    if explicit:
        if "all" in explicit:
            return ("web", "mobile", "desktop", "pbc", "deployment")
        return tuple(dict.fromkeys(explicit))
    app_targets = tuple(semantic.get("app", {}).get("targets", ()))
    requested = [target for target in ("web", "mobile", "desktop") if target in app_targets or (target == "web" and "pwa" in app_targets)]
    if semantic.get("pbcs") or semantic.get("composition"):
        requested.append("pbc")
    if semantic.get("deployment"):
        requested.append("deployment")
    return tuple(dict.fromkeys(requested or ("web", "mobile", "desktop", "pbc", "deployment")))


def _release_check(check: str, ok: bool, *, detail: dict | None = None) -> dict:
    return {"check": check, "ok": bool(ok), "detail": detail or {}}


def _release_verifier_payload(kind: str, payload_format: str, checks: tuple[dict, ...], semantic: dict, extra: dict | None = None) -> dict:
    blocking = tuple(_release_gap_name(check["check"]) for check in checks if not check["ok"])
    payload = {
        "format": payload_format,
        "kind": kind,
        "ok": not blocking and semantic.get("ok", True),
        "checks": checks,
        "blocking_gaps": blocking,
    }
    if extra:
        payload.update(extra)
    return payload


def _release_gap_name(check: str) -> str:
    mapping = {
        "app_build_contract": "app_build_not_observed",
        "smoke_tests_declared": "smoke_tests_not_declared",
        "smoke_launch_path_exists": "smoke_launch_not_declared",
    }
    return mapping.get(check, check)


def _has_diagnostic(report: dict, codes: set[str]) -> bool:
    return any(item.get("code") in codes for item in report.get("diagnostics", ()))


def _release_route_sources(semantic: dict) -> tuple[str, ...]:
    contracts = semantic.get("contracts", {})
    route_sources = []
    route_sources.extend(contracts.get("api", {}).keys())
    route_sources.extend(semantic.get("views", {}).keys())
    return tuple(route_sources)


def _packages_for_target(semantic: dict, target: str) -> tuple[dict, ...]:
    packages = semantic.get("contracts", {}).get("package", {})
    matched = []
    for package in packages.values():
        raw_targets = package.get("options", {}).get("target", ()) or package.get("options", {}).get("targets", ())
        normalized, _unknown = normalize_platform_targets(raw_targets, default=())
        if target in normalized:
            matched.append(package)
    return tuple(matched)


def _package_option_present(semantic: dict, *names: str) -> bool:
    packages = semantic.get("contracts", {}).get("package", {})
    return any(_contract_option_present(package, *names) for package in packages.values())


def _contract_option_present(contract: dict, *names: str) -> bool:
    options = contract.get("options", {})
    lowered = {key.lower(): value for key, value in options.items()}
    for name in names:
        if name.lower() in lowered and lowered[name.lower()]:
            return True
        if any(name.lower() in str(value).lower() for values in lowered.values() for value in values):
            return True
    statements = contract.get("statements", ())
    return any(name.lower() in statement.get("verb", "").lower() for name in names for statement in statements)


def _components_fit_density(semantic: dict, *, max_width: int, max_height: int) -> bool:
    for view in semantic.get("views", {}).values():
        for component in view.get("components", ()):
            if component.get("x", 0) < 0 or component.get("y", 0) < 0:
                return False
            if component.get("w", 1) <= 0 or component.get("h", 1) <= 0:
                return False
            if component.get("x", 0) + component.get("w", 1) > max_width:
                return False
            if component.get("y", 0) + component.get("h", 1) > max_height:
                return False
    return True


def _menus_bind_to_handlers(semantic: dict) -> bool:
    contracts = semantic.get("contracts", {})
    menus = contracts.get("menu", {})
    if not menus:
        return True
    targets = _handler_targets(semantic)
    for menu in menus.values():
        for handler in menu.get("handlers", ()):
            if handler.get("target") not in targets:
                return False
    return True


def _handler_targets(semantic: dict) -> set[str]:
    targets = set(semantic.get("operations", {}))
    targets.update(semantic.get("flows", {}))
    for contracts in semantic.get("contracts", {}).values():
        targets.update(contracts.keys())
    targets.update(semantic.get("agents", {}))
    return targets


def _pbc_catalog_has_artifacts(item: dict | None) -> bool:
    if not item:
        return False
    return bool(item.get("package_dir") or item.get("package_directory") or item.get("template") or _pbc_package_dir(item).exists())


def _pbc_catalog_has_schema_artifacts(item: dict | None) -> bool:
    if not item:
        return False
    package_dir = _pbc_package_dir(item)
    has_files = (package_dir / "migrations").exists() and (
        (package_dir / "models.py").exists() or (package_dir / "schema_contract.py").exists()
    )
    return bool(item.get("tables")) and item.get("datastore_backend") in {"postgresql", "mysql", "mariadb"} and (has_files or not package_dir.exists())


def _pbc_catalog_has_contracts(item: dict | None) -> bool:
    if not item:
        return False
    return bool(item.get("apis") or item.get("emits") or item.get("consumes"))


def _pbc_catalog_side_effect_free(item: dict | None) -> bool:
    if not item:
        return False
    return item.get("self_registration_side_effect_free", True) is not False


def _pbc_catalog_has_release_evidence(item: dict | None) -> bool:
    if not item:
        return False
    package_dir = _pbc_package_dir(item)
    evidence_files = ("RELEASE_EVIDENCE.md", "release_evidence.py", "capability_assurance.py")
    return bool(item.get("implemented") or item.get("release_evidence") or item.get("tests") or item.get("capabilities")) or any(
        (package_dir / name).exists() for name in evidence_files
    )


def _pbc_package_dir(item: dict | None) -> Path:
    if not item:
        return Path("__missing_pbc__")
    raw = item.get("package_directory") or item.get("package_dir") or item.get("pbc")
    path = Path(str(raw))
    if path.is_absolute():
        return path
    if str(path).startswith("pbcs/"):
        return Path(__file__).resolve().parent / path
    return Path(__file__).resolve().parent / "pbcs" / item.get("pbc", str(path))


def _composition_uses_private_tables(composition: dict) -> bool:
    for block in composition.values():
        for connection in block.get("connections", ()):
            if connection.get("from_kind") == "table" or connection.get("to_kind") == "table":
                return True
    return False


def _deployment_verifier_checks(name: str, deployment: dict) -> tuple[dict, ...]:
    units = tuple(deployment.get("units", ()))
    health = tuple(deployment.get("health", ()))
    statements = tuple(deployment.get("statements", ()))
    unit_targets = {unit.get("target") for unit in units}
    health_targets = {item.get("target") for item in health}
    env_statements = tuple(item for item in statements if item.get("verb") == "env")
    resource_statements = tuple(item for item in statements if item.get("verb") == "resource")
    production_like = name.lower() in {"prod", "production", "live"} or deployment.get("options", {}).get("environment") == ("production",)
    return (
        _release_check("units_declared", bool(units), detail={"deployment": name}),
        _release_check("health_checks_declared", bool(health) and unit_targets <= health_targets, detail={"deployment": name}),
        _release_check("environment_variables_named", all(_valid_env_binding(item) for item in env_statements), detail={"deployment": name}),
        _release_check("secret_values_absent", not any(_looks_like_secret_literal(value) for item in statements for value in item.get("values", ())), detail={"deployment": name}),
        _release_check("resource_hints_present_for_production_units", bool(resource_statements) or not production_like, detail={"deployment": name}),
        _release_check("topology_graph_connected_and_explainable", _deployment_topology_connected(units, health), detail={"deployment": name}),
    )


def _valid_env_binding(statement: dict) -> bool:
    values = statement.get("values", ())
    return bool(values) and all(re.fullmatch(r"[A-Z][A-Z0-9_]*", value or "") for value in values)


def _looks_like_secret_literal(value: str) -> bool:
    text = str(value or "")
    lowered = text.lower()
    return (
        any(marker in lowered for marker in ("secret=", "password=", "token=", "apikey=", "api_key="))
        or bool(re.match(r"(sk|pk|whsec|xoxb|ghp)_[A-Za-z0-9_\\-]{8,}", text))
    )


def _deployment_topology_connected(units: tuple[dict, ...], health: tuple[dict, ...]) -> bool:
    if not units:
        return False
    if len(units) == 1:
        return True
    health_targets = {item.get("target") for item in health}
    unit_targets = {unit.get("target") for unit in units}
    return bool(unit_targets & health_targets)


def _parse_rename_hints(rename_hints: Iterable[str]) -> dict[tuple[str, str], dict]:
    parsed: dict[tuple[str, str], dict] = {}
    for raw_hint in rename_hints:
        raw = str(raw_hint).strip()
        match = re.match(r"(?P<kind>table|field):(?P<old>[A-Za-z_][A-Za-z0-9_.]*)=(?P<new>[A-Za-z_][A-Za-z0-9_.]*)$", raw)
        if not match:
            continue
        key = (match.group("kind"), match.group("old"))
        parsed[key] = {
            "kind": match.group("kind"),
            "from": match.group("old"),
            "to": match.group("new"),
            "source": raw,
        }
    return parsed


def _migration_change(kind: str, **kwargs) -> dict:
    destructive = bool(kwargs.pop("destructive", False))
    change = {"kind": kind, "destructive": destructive}
    change.update(kwargs)
    if destructive:
        change.setdefault("requires_approval", True)
    return change


def _table_rename_candidates(
    previous_tables: dict,
    current_tables: dict,
    dropped_tables: set[str],
    added_tables: set[str],
    hints: dict[tuple[str, str], dict],
) -> list[dict]:
    changes: list[dict] = []
    for table_name in sorted(dropped_tables):
        hint = hints.get(("table", table_name))
        if hint and hint["to"] in added_tables:
            changes.append(
                _migration_change(
                    "rename_table",
                    table=table_name,
                    **{"from": table_name, "to": hint["to"]},
                    confidence="hinted",
                )
            )
            continue
        previous_fields = set(previous_tables[table_name].get("fields", {}))
        best_name = None
        best_score = 0.0
        for added_name in added_tables:
            current_fields = set(current_tables[added_name].get("fields", {}))
            if not previous_fields and not current_fields:
                continue
            score = len(previous_fields & current_fields) / max(len(previous_fields | current_fields), 1)
            if score > best_score:
                best_name = added_name
                best_score = score
        if best_name and best_score >= 0.6:
            changes.append(
                _migration_change(
                    "renamed_table_candidate",
                    table=table_name,
                    **{"from": table_name, "to": best_name},
                    confidence=round(best_score, 2),
                    requires_approval=True,
                    safe_alternative="Add an explicit table rename hint before applying the migration.",
                )
            )
    return changes


def _field_migration_changes(
    table_name: str,
    previous_table: dict,
    current_table: dict,
    hints: dict[tuple[str, str], dict],
) -> tuple[dict, ...]:
    changes: list[dict] = []
    previous_fields = previous_table.get("fields", {})
    current_fields = current_table.get("fields", {})
    previous_names = set(previous_fields)
    current_names = set(current_fields)
    added_fields = current_names - previous_names
    dropped_fields = previous_names - current_names
    field_renames = _field_rename_candidates(table_name, previous_fields, current_fields, dropped_fields, added_fields, hints)
    renamed_old = {item["from"].split(".", 1)[1] for item in field_renames}
    renamed_new = {item["to"].split(".", 1)[1] for item in field_renames}
    changes.extend(field_renames)

    for field_name in sorted(added_fields - renamed_new):
        field = current_fields[field_name]
        requires_backfill = field.get("required") and field.get("default") is None and not field.get("primary_key")
        changes.append(
            _migration_change(
                "add_field",
                table=table_name,
                field=field_name,
                field_type=field.get("type"),
                destructive=False,
                requires_backfill=bool(requires_backfill),
                safe_alternative="Add a default or nullable rollout field before enforcing required data." if requires_backfill else None,
            )
        )
    for field_name in sorted(dropped_fields - renamed_old):
        changes.append(
            _migration_change(
                "drop_field",
                table=table_name,
                field=field_name,
                destructive=True,
                safe_alternative="Keep the field hidden until retention and exports are complete.",
            )
        )

    for field_name in sorted(previous_names & current_names):
        before = previous_fields[field_name]
        after = current_fields[field_name]
        for attr, kind in (
            ("type", "type_change"),
            ("required", "nullability_change"),
            ("default", "default_change"),
            ("unique", "unique_change"),
        ):
            if before.get(attr) != after.get(attr):
                destructive = kind in {"type_change", "nullability_change"} and after.get(attr) not in (False, None)
                changes.append(
                    _migration_change(
                        kind,
                        table=table_name,
                        field=field_name,
                        before=before.get(attr),
                        after=after.get(attr),
                        destructive=destructive,
                        requires_backfill=kind in {"type_change", "nullability_change"},
                    )
                )
        if before.get("relationship") != after.get("relationship"):
            changes.append(
                _migration_change(
                    "relationship_change",
                    table=table_name,
                    field=field_name,
                    before=before.get("relationship"),
                    after=after.get("relationship"),
                    destructive=True,
                    safe_alternative="Create a new relationship field, backfill it, then retire the old relationship.",
                )
            )
    return tuple(changes)


def _field_rename_candidates(
    table_name: str,
    previous_fields: dict,
    current_fields: dict,
    dropped_fields: set[str],
    added_fields: set[str],
    hints: dict[tuple[str, str], dict],
) -> list[dict]:
    changes: list[dict] = []
    for field_name in sorted(dropped_fields):
        qualified = f"{table_name}.{field_name}"
        hint = hints.get(("field", qualified)) or hints.get(("field", field_name))
        if hint:
            new_name = hint["to"].split(".")[-1]
            if new_name in added_fields:
                changes.append(
                    _migration_change(
                        "rename_field",
                        table=table_name,
                        field=field_name,
                        **{"from": qualified, "to": f"{table_name}.{new_name}"},
                        confidence="hinted",
                    )
                )
                continue
        before = previous_fields[field_name]
        for added_name in sorted(added_fields):
            after = current_fields[added_name]
            if before.get("type") == after.get("type") and before.get("relationship") == after.get("relationship"):
                changes.append(
                    _migration_change(
                        "renamed_field_candidate",
                        table=table_name,
                        field=field_name,
                        **{"from": qualified, "to": f"{table_name}.{added_name}"},
                        confidence="type-and-relationship-match",
                        requires_approval=True,
                        safe_alternative="Add an explicit field rename hint before applying the migration.",
                    )
                )
                break
    return changes


def _directive_migration_changes(table_name: str, previous_table: dict, current_table: dict) -> tuple[dict, ...]:
    before = {_directive_signature(item): item for item in previous_table.get("directives", ())}
    after = {_directive_signature(item): item for item in current_table.get("directives", ())}
    changes: list[dict] = []
    for signature in sorted(set(after) - set(before)):
        changes.append(_directive_change("add", table_name, after[signature]))
    for signature in sorted(set(before) - set(after)):
        changes.append(_directive_change("drop", table_name, before[signature]))
    return tuple(changes)


def _directive_change(action: str, table_name: str, directive: dict) -> dict:
    family = _directive_migration_family(directive)
    destructive = action == "drop"
    kind = f"{action}_{family}" if family else f"{action}_table_directive"
    detail = {
        "table": table_name,
        "directive": _directive_signature(directive),
        "directive_detail": directive,
        "destructive": destructive,
    }
    if family == "index":
        detail["index"] = directive.get("name") or "_".join(directive.get("values", ()))
        detail["fields"] = tuple(directive.get("values", ()))
    if family == "check":
        detail["check"] = directive.get("name") or "_".join(directive.get("values", ()))
        detail["expression"] = tuple(directive.get("values", ()))
    if destructive:
        detail["safe_alternative"] = (
            "Retain the table directive until dependent queries, reports, and generated validations are migrated."
        )
    return _migration_change(kind, **detail)


def _directive_migration_family(directive: dict) -> str | None:
    verb = str(directive.get("verb") or "").lower()
    if verb in {"index", "key"}:
        return "index"
    if verb == "unique":
        return "unique_constraint"
    if verb in {"constraint", "check"}:
        return "check"
    return None


def _directive_signature(directive: dict) -> str:
    return json.dumps(directive, sort_keys=True, default=list)


def _relationship_migration_changes(previous: dict, current: dict) -> tuple[dict, ...]:
    before = {
        (edge["from"], edge["to"], edge.get("label"), edge.get("cardinality"))
        for edge in previous.get("graphs", {}).get("er", {}).get("edges", ())
    }
    after = {
        (edge["from"], edge["to"], edge.get("label"), edge.get("cardinality"))
        for edge in current.get("graphs", {}).get("er", {}).get("edges", ())
    }
    changes = [
        _migration_change(
            "add_relationship",
            table=item[0],
            target_table=item[1],
            field=item[2],
            cardinality=item[3],
            destructive=False,
        )
        for item in sorted(after - before)
    ]
    changes.extend(
        _migration_change(
            "drop_relationship",
            table=item[0],
            target_table=item[1],
            field=item[2],
            cardinality=item[3],
            destructive=True,
            safe_alternative="Retain the existing relationship until dependent forms and reports are migrated.",
        )
        for item in sorted(before - after)
    )
    return tuple(changes)


def _calculated_field_migration_changes(previous_tables: dict, current_tables: dict) -> tuple[dict, ...]:
    changes: list[dict] = []
    for table_name in sorted(set(previous_tables) & set(current_tables)):
        previous_fields = previous_tables[table_name].get("fields", {})
        current_fields = current_tables[table_name].get("fields", {})
        for field_name in sorted(set(previous_fields) & set(current_fields)):
            before = previous_fields[field_name]
            after = current_fields[field_name]
            if before.get("calculated") != after.get("calculated") or before.get("expression") != after.get("expression"):
                changes.append(
                    _migration_change(
                        "calculated_field_change",
                        table=table_name,
                        field=field_name,
                        before=before.get("expression"),
                        after=after.get("expression"),
                        destructive=False,
                    )
                )
    return tuple(changes)


def _pbc_migration_changes(previous: dict, current: dict) -> tuple[dict, ...]:
    previous_pbcs = set(previous.get("pbcs", {}))
    current_pbcs = set(current.get("pbcs", {}))
    changes = [
        _migration_change("add_pbc_include", pbc=pbc, destructive=False)
        for pbc in sorted(current_pbcs - previous_pbcs)
    ]
    changes.extend(
        _migration_change(
            "drop_pbc_include",
            pbc=pbc,
            destructive=True,
            safe_alternative="Deprecate the PBC contract and preserve projections before removal.",
        )
        for pbc in sorted(previous_pbcs - current_pbcs)
    )
    changes.extend(_pbc_ownership_transfer_changes(previous, current))
    return tuple(changes)


def _pbc_ownership_transfer_changes(previous: dict, current: dict) -> tuple[dict, ...]:
    before = _pbc_table_ownership(previous)
    after = _pbc_table_ownership(current)
    changes: list[dict] = []
    for table in sorted(set(before) & set(after)):
        if before[table] == after[table]:
            continue
        changes.append(
            _migration_change(
                "pbc_ownership_transfer",
                table=table,
                **{"from": before[table], "to": after[table]},
                destructive=True,
                safe_alternative="Publish a projection contract and backfill the receiving PBC before changing table ownership.",
            )
        )
    return tuple(changes)


def _pbc_table_ownership(semantic: dict) -> dict[str, str]:
    owners: dict[str, str] = {}
    for pbc, detail in semantic.get("pbcs", {}).items():
        options = detail.get("options", {}) or {}
        for key in ("owns", "tables", "owned_tables"):
            for table in options.get(key, ()):
                owners[str(table)] = pbc
        catalog = detail.get("catalog") or {}
        for table in catalog.get("tables", ()):
            owners.setdefault(str(table), pbc)
    return owners


def _classify_nl_operation(prompt: str, semantic: dict) -> dict:
    normalized = " ".join((prompt or "").strip().split())
    lower = normalized.lower()
    if not normalized:
        return {"kind": "unsupported", "intent": "empty"}

    pbc_match = re.search(r"\b(?:include|add|compose)\s+(?:pbc\s+)?(?P<pbc>[a-z][a-z0-9_]+)\b", lower)
    if pbc_match and pbc_match.group("pbc") in _pbc_catalog_by_key():
        pbc = pbc_match.group("pbc")
        return {
            "kind": "add_pbc_include",
            "intent": "composition_change",
            "pbc": pbc,
            "composition": _default_composition_name(semantic),
            "affected_symbols": (f"pbc.{pbc}",),
        }

    field_match = re.search(r"\badd\s+(?P<field>[A-Za-z][A-Za-z0-9_ ]+?)\s+to\s+(?P<table>[A-Za-z][A-Za-z0-9_ ]+)\b", normalized, re.I)
    if field_match:
        table_name = _resolve_nl_table_name(field_match.group("table"), semantic)
        field_name = _snake_case(field_match.group("field"))
        if table_name and field_name:
            return {
                "kind": "add_field",
                "intent": "schema_change",
                "table": table_name,
                "field": field_name,
                "field_type": _infer_nl_field_type(field_name),
                "affected_symbols": (f"table.{table_name}.{field_name}",),
            }

    table_match = re.search(r"\b(?:add|create)\s+(?P<table>[A-Za-z][A-Za-z0-9_ ]+?)(?:\s+(?:table|record|entity|feature|module))?(?:\s+to\b|$)", normalized, re.I)
    if table_match:
        raw_table = table_match.group("table")
        table_name = _pascal_case(_strip_domain_suffix(raw_table))
        if table_name:
            return {
                "kind": "add_table",
                "intent": "domain_feature",
                "table": table_name,
                "affected_symbols": (f"table.{table_name}",),
            }

    flow_match = re.search(r"\b(?:add|create)\s+(?P<flow>[A-Za-z][A-Za-z0-9_ ]+?)\s+(?:workflow|flow)\b", normalized, re.I)
    if flow_match:
        flow_name = _pascal_case(flow_match.group("flow"))
        return {
            "kind": "add_flow",
            "intent": "workflow_change",
            "flow": flow_name,
            "affected_symbols": (f"flow.{flow_name}",),
        }

    return {"kind": "unsupported", "intent": "unclassified"}


def _render_nl_dsl_patch(operation: dict) -> str:
    if operation["kind"] == "add_table":
        table = operation["table"]
        return f"""
table {table} {{
  id: int pk
  name: string required search
  status: string default draft
  created_at: datetime
}}

view {table}Form for {table} {{
  Main: name, status
}}
""".strip()
    if operation["kind"] == "add_field":
        return f"// edit table {operation['table']}: add {operation['field']}: {operation['field_type']}"
    if operation["kind"] == "add_pbc_include":
        composition = operation["composition"]
        return f"""
composition {composition} {{
  include pbc {operation['pbc']} version 1.0.0
}}
""".strip()
    if operation["kind"] == "add_flow":
        flow = operation["flow"]
        return f"""
flow {flow} {{
  draft -> review
  review -> approved
}}
""".strip()
    return ""


def _append_dsl_patch(source: str, patch: str) -> str:
    if not patch:
        return source
    if patch.startswith("// edit table "):
        return _apply_table_field_patch(source, patch)
    if patch.startswith("// edit view "):
        return _apply_view_component_patch(source, patch)
    if patch.startswith("// edit flow "):
        return _apply_flow_transition_patch(source, patch)
    stripped = source.rstrip()
    return f"{stripped}\n\n{patch}\n" if stripped else f"{patch}\n"


def _apply_table_field_patch(source: str, patch: str) -> str:
    match = re.match(r"// edit table (?P<table>[A-Za-z_][A-Za-z0-9_]*): add (?P<field>[a-z][a-z0-9_]*): (?P<type>[A-Za-z_][A-Za-z0-9_]*)", patch)
    if not match:
        return source
    table = match.group("table")
    field = match.group("field")
    field_type = match.group("type")
    pattern = re.compile(rf"(table\s+{re.escape(table)}\s*\{{)(?P<body>.*?)(\n\}})", re.S)
    table_match = pattern.search(source)
    if table_match is None:
        return _append_dsl_patch(
            source,
            f"table {table} {{\n  id: int pk\n  {field}: {field_type}\n}}",
        )
    body = table_match.group("body").rstrip()
    replacement = f"{table_match.group(1)}{body}\n  {field}: {field_type}{table_match.group(3)}"
    return source[: table_match.start()] + replacement + source[table_match.end() :]


def _apply_view_component_patch(source: str, patch: str) -> str:
    match = re.match(
        r"// edit view (?P<view>[A-Za-z_][A-Za-z0-9_]*): add component (?P<binding>[A-Za-z_][A-Za-z0-9_.]*) (?P<component>[A-Za-z_][A-Za-z0-9_]*) (?P<x>-?\d+) (?P<y>-?\d+) (?P<w>-?\d+) (?P<h>-?\d+)",
        patch,
    )
    if not match:
        return source
    view = match.group("view")
    line = f"  @ {match.group('binding')} {match.group('component')} {match.group('x')} {match.group('y')} {match.group('w')} {match.group('h')}"
    return _append_to_existing_block(source, "view", view, line) or source


def _apply_flow_transition_patch(source: str, patch: str) -> str:
    match = re.match(
        r"// edit flow (?P<flow>[A-Za-z_][A-Za-z0-9_]*): add transition (?P<source>[A-Za-z_][A-Za-z0-9_]*) -> (?P<target>[A-Za-z_][A-Za-z0-9_]*)",
        patch,
    )
    if not match:
        return source
    line = f"  {match.group('source')} -> {match.group('target')}"
    return _append_to_existing_block(source, "flow", match.group("flow"), line) or source


def _default_composition_name(semantic: dict) -> str:
    compositions = semantic.get("composition", {})
    if compositions:
        return next(iter(compositions))
    app_name = semantic.get("app", {}).get("name")
    return f"{app_name or 'App'}Composition"


def _resolve_nl_table_name(raw: str, semantic: dict) -> str | None:
    candidate = _pascal_case(_strip_domain_suffix(raw))
    if candidate in semantic.get("tables", {}):
        return candidate
    normalized = _snake_case(raw).replace("_", "")
    for table_name in semantic.get("tables", {}):
        if table_name.lower() == candidate.lower() or table_name.lower() == normalized:
            return table_name
    return candidate if candidate else None


def _strip_domain_suffix(raw: str) -> str:
    value = re.sub(r"\b(accounts receivable|accounts payable|erp|module|feature)\b", "", raw, flags=re.I)
    value = re.sub(r"\bto\b.*$", "", value, flags=re.I)
    return value.strip()


def _snake_case(raw: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", raw or "")
    return "_".join(word.lower() for word in words)


def _pascal_case(raw: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", raw or "")
    if len(words) == 2 and words[-1].lower() == "memos":
        words[-1] = "memo"
    elif len(words) == 1 and words[0].lower().endswith("memos"):
        words[0] = words[0][:-1]
    elif len(words) > 1 and words[-1].lower().endswith("s") and not words[-1].lower().endswith("ss"):
        words[-1] = words[-1][:-1]
    return "".join(word[:1].upper() + word[1:] for word in words if word)


def _infer_nl_field_type(field_name: str) -> str:
    if field_name.endswith("_id"):
        return "int"
    if any(token in field_name for token in ("amount", "total", "balance", "price", "cost")):
        return "decimal"
    if any(token in field_name for token in ("date", "at", "time")):
        return "datetime"
    if field_name.startswith(("is_", "has_", "can_")):
        return "bool"
    return "string"


def _nl_test_plan(operation: dict) -> tuple[dict, ...]:
    return (
        {"id": "lint_patched_dsl", "command": "appgen lint app.appgen --json"},
        {"id": "validate_patched_dsl", "command": "appgen validate app.appgen --json"},
        {"id": f"assert_{operation['kind']}", "assertion": "Generated semantic model includes the affected symbols."},
    )


def _nl_token_budget_notes() -> tuple[str, ...]:
    return (
        "Send the semantic symbols and the requested edit operation, not the whole generated project.",
        "Return a DSL patch and let AppGen-X run lint, migration preview, and generation.",
        "Reject requests that cannot be represented as a bounded DSL operation.",
    )


def _semantic_symbols(source: str, schema: AppSchema) -> dict:
    symbols: dict[str, dict] = {}

    def add(kind: str, name: str, *, parent: str | None = None, detail: dict | None = None) -> None:
        symbol_id = f"{kind}.{name}" if parent is None else f"{parent}.{name}"
        line, column = _locate_token(source, name)
        symbols[symbol_id] = {
            "id": symbol_id,
            "kind": kind,
            "name": name,
            "parent": parent,
            "file": schema.source,
            "range": _semantic_range(line, column, name),
            "references": (),
            "detail": detail or {},
        }

    if schema.app_name:
        add("app", schema.app_name, detail={"targets": _lint_summary(schema)["targets"]})
    for table in schema.tables:
        add("table", table.name)
        for column in table.columns:
            add("field", column.name, parent=f"table.{table.name}", detail={"type": column.type_name})
    for enum in schema.enums:
        add("enum", enum.name)
        for value in enum.values:
            add("enum_value", value, parent=f"enum.{enum.name}")
    for view in schema.views:
        add("view", view.name, detail={"table": view.table})
        for handler in view.handlers:
            add("handler", handler.event, parent=f"view.{view.name}", detail={"target": handler.target})
    for flow in schema.flows:
        add("flow", flow.name)
        for state in _flow_states(flow):
            add("flow_state", state, parent=f"flow.{flow.name}")
    for role in schema.roles:
        add("role", role.name)
    for rule in schema.rules:
        add("rule", rule.name, detail={"table": rule.table})
    for provider in schema.llm_providers:
        add("llm", provider.name, detail={"provider": provider.provider})
    for agent in schema.agents:
        add("agent", agent.name, detail={"provider": agent.provider})
    for block in schema.platform_blocks:
        add(block.kind, block.name)
    for contract in _enterprise_contracts(schema):
        add(contract.kind, contract.name)
    return symbols


def _semantic_range(line: int | None, column: int | None, token: str) -> dict | None:
    if line is None or column is None:
        return None
    return {
        "start": {"line": line, "character": column},
        "end": {"line": line, "character": column + len(token)},
    }


def _semantic_tables(schema: AppSchema) -> dict:
    table_map = {table.name: table for table in schema.tables}
    field_map = {table.name: _field_names(table) for table in schema.tables}
    return {
        table.name: {
            "name": table.name,
            "fields": {
                column.name: {
                    "name": column.name,
                    "type": column.type_name,
                    "required": not column.nullable,
                    "primary_key": column.primary_key,
                    "unique": column.unique,
                    "hidden": column.hidden,
                    "search": column.searchable,
                    "default": column.default,
                    "calculated": column.derived,
                    "expression": column.expression,
                    "relationship": _semantic_relationship(column),
                }
                for column in table.columns
            },
            "directives": tuple(_semantic_table_directive(item) for item in table.directives),
            "lookup_paths": _semantic_lookup_paths(table, table_map, field_map),
        }
        for table in schema.tables
    }


def _semantic_relationship(column: ColumnSchema) -> dict | None:
    if not column.references:
        return None
    target_table, target_field = column.references
    alias = column.name[:-3] if column.name.endswith("_id") else column.name
    return {
        "target_table": target_table,
        "target_field": target_field,
        "cardinality": "many-to-one",
        "alias": alias,
    }


def _semantic_table_directive(directive: TableDirectiveSchema) -> dict:
    return {
        "verb": directive.verb,
        "name": directive.name,
        "values": directive.values,
        "targets": directive.targets,
    }


def _semantic_lookup_paths(
    table: TableSchema,
    table_map: dict[str, TableSchema],
    field_map: dict[str, set[str]],
) -> dict:
    paths: dict[str, dict] = {}
    for column in table.columns:
        if not column.references:
            continue
        alias = column.name[:-3] if column.name.endswith("_id") else column.name
        target_table, _target_field = column.references
        target = table_map.get(target_table)
        if target is None:
            continue
        for target_column in target.columns:
            path = f"{alias}.{target_column.name}"
            paths[path] = {
                "chain": (f"{table.name}.{column.name}", f"{target_table}.{target_column.name}"),
                "valid": _valid_lookup_path(table.name, path, table_map, field_map),
            }
    for directive in table.directives:
        if directive.verb.lower() == "lookup":
            for value in directive.values:
                paths.setdefault(
                    value,
                    {
                        "chain": (value,),
                        "valid": _valid_lookup_path(table.name, value, table_map, field_map),
                    },
                )
    return paths


def _semantic_views(schema: AppSchema) -> dict:
    return {
        view.name: {
            "name": view.name,
            "table": view.table,
            "sections": tuple(
                {"name": section.name, "fields": section.fields}
                for section in view.sections
            ),
            "fields": view.fields,
            "components": tuple(
                {
                    "binding": component.field,
                    "component": component.component,
                    "x": component.x,
                    "y": component.y,
                    "w": component.w,
                    "h": component.h,
                }
                for component in view.components
            ),
            "handlers": tuple(_semantic_handler(handler) for handler in view.handlers),
        }
        for view in schema.views
    }


def _semantic_flows(schema: AppSchema) -> dict:
    return {
        flow.name: {
            "name": flow.name,
            "states": _flow_states(flow),
            "transitions": tuple(
                {"from": step.source, "to": step.target}
                for step in flow.steps
            ),
            "directives": tuple(_semantic_statement(item) for item in flow.directives),
            "human_tasks": tuple(_semantic_human_task(item) for item in flow.directives if item.verb == "human"),
            "timers": tuple(_semantic_timer(item) for item in flow.directives if item.verb == "timer"),
            "compensations": tuple(
                {"state": item.values[0] if item.values else None, "operation": item.target}
                for item in flow.directives
                if item.verb == "compensate"
            ),
        }
        for flow in schema.flows
    }


def _flow_states(flow: FlowSchema) -> tuple[str, ...]:
    states: list[str] = []
    for step in flow.steps:
        states.extend((step.source, step.target))
    for directive in flow.directives:
        states.extend(value for value in directive.values if _looks_like_identifier(value))
        if directive.target:
            states.append(directive.target)
    return tuple(dict.fromkeys(states))


def _semantic_human_task(statement: EnterpriseStatementSchema) -> dict:
    values = statement.values
    return {
        "name": values[0] if values else None,
        "assignee": values[2] if len(values) >= 3 and values[1] == "assigned" else None,
        "to": statement.target,
    }


def _semantic_timer(statement: EnterpriseStatementSchema) -> dict:
    values = statement.values
    return {
        "state": values[0] if values else None,
        "duration": values[1] if len(values) > 1 else None,
        "to": statement.target,
    }


def _semantic_pbcs(schema: AppSchema) -> dict:
    catalog = _pbc_catalog_by_key()
    pbcs = {
        block.name: {
            **_semantic_platform_block(block),
            "catalog_resolved": block.name in catalog,
            "catalog": catalog.get(block.name),
        }
        for block in schema.platform_blocks
        if block.kind == "pbc"
    }
    for block in schema.platform_blocks:
        if block.kind != "composition":
            continue
        for include in block.options.get("include", ()):
            key = _composition_include_key(include)
            if key and key not in pbcs:
                pbcs[key] = {
                    "name": key,
                    "kind": "pbc",
                    "catalog_resolved": key in catalog,
                    "catalog": catalog.get(key),
                    "declared_inline": False,
                }
    return pbcs


def _semantic_compositions(schema: AppSchema) -> dict:
    catalog = _pbc_catalog_by_key()
    return {
        block.name: {
            "name": block.name,
            "includes": tuple(
                {
                    "pbc": _composition_include_key(include),
                    "version": _composition_include_version(include),
                    "catalog_resolved": _composition_include_key(include) in catalog,
                }
                for include in block.options.get("include", ())
            ),
            "requires": block.options.get("require", ()),
            "exposes": block.options.get("expose", ()),
            "connections": tuple(_semantic_composition_connection(item) for item in block.options.get("connect", ())),
            "options": dict(block.options),
        }
        for block in schema.platform_blocks
        if block.kind == "composition"
    }


def _composition_include_key(value: str) -> str | None:
    match = re.match(r"(?P<key>[A-Za-z_][A-Za-z0-9_]*)(?:\s*version\s*(?P<version>.+))?$", value or "")
    return match.group("key") if match else None


def _composition_include_version(value: str) -> str | None:
    match = re.match(r"(?P<key>[A-Za-z_][A-Za-z0-9_]*)(?:\s*version\s*(?P<version>.+))?$", value or "")
    if not match:
        return None
    version = match.group("version")
    return version.strip("'\"") if version else None


def _semantic_composition_connection(value: str) -> dict:
    parts = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", value or "")
    return {
        "raw": value,
        "from_pbc": parts[0] if len(parts) > 0 else None,
        "from_kind": parts[1] if len(parts) > 1 else None,
        "from_contract": parts[2] if len(parts) > 2 else None,
        "to_pbc": parts[3] if len(parts) > 3 else None,
        "to_kind": parts[4] if len(parts) > 4 else None,
        "to_contract": parts[5] if len(parts) > 5 else None,
    }


def _pbc_catalog_by_key() -> dict[str, dict]:
    try:
        from .pbc import pbc_catalog
    except Exception:  # pragma: no cover - optional catalog boundary
        return {}
    return {item["pbc"]: item for item in pbc_catalog()}


def _semantic_contracts(schema: AppSchema) -> dict:
    return {
        kind: {contract.name: _semantic_contract(contract) for contract in contracts}
        for kind, contracts in _enterprise_contract_groups(schema).items()
    }


def _semantic_contract(contract: EnterpriseContractSchema) -> dict:
    return {
        "kind": contract.kind,
        "name": contract.name,
        "options": dict(contract.options),
        "statements": tuple(_semantic_statement(item) for item in contract.statements),
        "handlers": tuple(_semantic_handler(item) for item in contract.handlers),
        "permissions": tuple(_semantic_permission(item) for item in contract.permissions),
    }


def _semantic_platform_block(block: PlatformBlockSchema) -> dict:
    return {
        "kind": block.kind,
        "name": block.name,
        "options": dict(block.options),
        "steps": tuple({"from": step.source, "to": step.target} for step in block.steps),
        "statements": tuple(_semantic_statement(item) for item in block.statements),
        "handlers": tuple(_semantic_handler(item) for item in block.handlers),
        "permissions": tuple(_semantic_permission(item) for item in block.permissions),
    }


def _semantic_deployment(block: PlatformBlockSchema) -> dict:
    return {
        **_semantic_platform_block(block),
        "units": tuple(
            {"target": unit.target, "pattern": unit.pattern}
            for unit in block.deployment_units
        ),
        "scales": tuple(
            {"target": scale.target, "min": scale.minimum, "max": scale.maximum}
            for scale in block.deployment_scales
        ),
        "health": tuple(
            {"target": health.target, "kind": health.kind, "path": health.path}
            for health in block.deployment_health
        ),
    }


def _semantic_statement(statement: EnterpriseStatementSchema) -> dict:
    return {"verb": statement.verb, "values": statement.values, "target": statement.target}


def _semantic_handler(handler: HandlerSchema) -> dict:
    return {"trigger": handler.trigger, "event": handler.event, "target": handler.target}


def _semantic_permission(permission: PermissionSchema) -> dict:
    return {"resource": permission.resource, "actions": permission.actions}


def _semantic_graphs(schema: AppSchema) -> dict:
    return {
        "er": _er_graph(schema),
        "lookup": _lookup_graph(schema),
        "workflow": _workflow_graph(schema),
        "handler": _handler_graph(schema),
        "pbc": _pbc_graph(schema),
        "security": _security_graph(schema),
        "agent": _agent_graph(schema),
        "deployment": _deployment_graph(schema),
        "package": _package_graph(schema),
    }


def _er_graph(schema: AppSchema) -> dict:
    nodes = tuple({"id": table.name, "kind": "table"} for table in schema.tables)
    edges = tuple(
        {
            "from": relation.source_table,
            "to": relation.target_table,
            "label": relation.source_column,
            "cardinality": relation.cardinality,
        }
        for relation in schema.relations
    )
    return {"format": "appgen.graph.er.v1", "nodes": nodes, "edges": edges}


def _lookup_graph(schema: AppSchema) -> dict:
    nodes: list[dict] = []
    edges: list[dict] = []
    table_map = {table.name: table for table in schema.tables}
    field_map = {table.name: _field_names(table) for table in schema.tables}
    for table in schema.tables:
        nodes.append({"id": table.name, "kind": "table"})
        for path, detail in _semantic_lookup_paths(table, table_map, field_map).items():
            node_id = f"{table.name}.{path}"
            nodes.append({"id": node_id, "kind": "lookup_path", "valid": detail["valid"]})
            edges.append({"from": table.name, "to": node_id, "label": path})
    return {"format": "appgen.graph.lookup.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _workflow_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for flow in schema.flows:
        nodes.append({"id": flow.name, "kind": "flow"})
        for state in _flow_states(flow):
            state_id = f"{flow.name}.{state}"
            nodes.append({"id": state_id, "kind": "state"})
        for step in flow.steps:
            edges.append({"from": f"{flow.name}.{step.source}", "to": f"{flow.name}.{step.target}", "label": "transition"})
        for directive in flow.directives:
            if directive.target:
                edges.append({"from": flow.name, "to": f"{flow.name}.{directive.target}", "label": directive.verb})
    return {"format": "appgen.graph.workflow.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _handler_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for view in schema.views:
        nodes.append({"id": view.name, "kind": "view"})
        for handler in view.handlers:
            event_id = f"{view.name}.{handler.event}"
            nodes.append({"id": event_id, "kind": "handler"})
            edges.append({"from": event_id, "to": handler.target, "label": handler.event})
    for contract in _enterprise_contracts(schema):
        nodes.append({"id": contract.name, "kind": contract.kind})
        for handler in contract.handlers:
            event_id = f"{contract.name}.{handler.event}"
            nodes.append({"id": event_id, "kind": "handler"})
            edges.append({"from": event_id, "to": handler.target, "label": handler.event})
    return {"format": "appgen.graph.handler.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _pbc_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for key, pbc in _semantic_pbcs(schema).items():
        nodes.append({"id": key, "kind": "pbc", "catalog_resolved": pbc.get("catalog_resolved", False)})
    for composition in _semantic_compositions(schema).values():
        nodes.append({"id": composition["name"], "kind": "composition"})
        for include in composition["includes"]:
            if include["pbc"]:
                edges.append({"from": composition["name"], "to": include["pbc"], "label": "include"})
        for connection in composition["connections"]:
            if connection["from_pbc"] and connection["to_pbc"]:
                edges.append(
                    {
                        "from": connection["from_pbc"],
                        "to": connection["to_pbc"],
                        "label": connection["from_contract"],
                    }
                )
    return {"format": "appgen.graph.pbc.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _security_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for role in schema.roles:
        nodes.append({"id": role.name, "kind": "role"})
        for permission in role.permissions:
            nodes.append({"id": permission.resource, "kind": "resource"})
            for action in permission.actions:
                edges.append({"from": role.name, "to": permission.resource, "label": action})
    for agent in schema.agents:
        nodes.append({"id": agent.name, "kind": "agent"})
        for permission in agent.permissions:
            nodes.append({"id": permission.resource, "kind": "resource"})
            for action in permission.actions:
                edges.append({"from": agent.name, "to": permission.resource, "label": action})
    return {"format": "appgen.graph.security.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _agent_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for provider in schema.llm_providers:
        nodes.append({"id": provider.name, "kind": "llm"})
    for agent in schema.agents:
        nodes.append({"id": agent.name, "kind": "agent"})
        if agent.provider:
            edges.append({"from": agent.name, "to": agent.provider, "label": "uses"})
        for skill in agent.competencies:
            skill_id = f"{agent.name}.{skill.verb}"
            nodes.append({"id": skill_id, "kind": "skill"})
            edges.append({"from": agent.name, "to": skill_id, "label": skill.verb})
            if skill.target:
                edges.append({"from": skill_id, "to": skill.target, "label": "target"})
    return {"format": "appgen.graph.agent.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _deployment_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for block in schema.platform_blocks:
        if block.kind != "deploy":
            continue
        nodes.append({"id": block.name, "kind": "deployment"})
        for unit in block.deployment_units:
            unit_id = f"{block.name}.{unit.target}"
            nodes.append({"id": unit_id, "kind": unit.pattern})
            edges.append({"from": block.name, "to": unit_id, "label": "unit"})
        for health in block.deployment_health:
            edges.append({"from": f"{block.name}.{health.target}", "to": health.path, "label": health.kind})
    return {"format": "appgen.graph.deployment.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _package_graph(schema: AppSchema) -> dict:
    nodes = []
    edges = []
    for contract in schema.package_contracts:
        nodes.append({"id": contract.name, "kind": "package"})
        for target in contract.options.get("target", ()) or contract.options.get("targets", ()):
            nodes.append({"id": target, "kind": "target"})
            edges.append({"from": contract.name, "to": target, "label": "builds"})
    return {"format": "appgen.graph.package.v1", "nodes": tuple(nodes), "edges": tuple(edges)}


def _looks_like_identifier(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value or ""))


def _spec_diagnostic_from_legacy(source: str, diagnostic: dict) -> dict:
    legacy_code = diagnostic.get("code", "dsl_feedback")
    code = _spec_diagnostic_code(legacy_code, diagnostic.get("message", ""))
    line = diagnostic.get("line")
    column = diagnostic.get("column")
    message = diagnostic.get("message", "")
    return {
        "code": code,
        "legacy_code": legacy_code,
        "severity": _spec_severity(diagnostic.get("severity", "info")),
        "title": _spec_diagnostic_title(code),
        "message": message,
        "range": _semantic_range(line, column, _diagnostic_token(message) or ""),
        "related_locations": (),
        "fixes": tuple(
            {"id": fix_id, "title": fix_id.replace("_", " ")}
            for fix_id in diagnostic.get("fix_ids", ())
        ),
        "docs_url": _spec_docs_url(code),
    }


def _spec_diagnostic(source: str, code: str, severity: str, message: str) -> dict:
    line, column = _locate_token(source, _diagnostic_token(message))
    return {
        "code": code,
        "severity": severity,
        "title": _spec_diagnostic_title(code),
        "message": message,
        "range": _semantic_range(line, column, _diagnostic_token(message) or ""),
        "related_locations": (),
        "fixes": (),
        "docs_url": _spec_docs_url(code),
    }


def _spec_severity(value: str) -> str:
    return {"suggestion": "hint"}.get(value, value if value in {"error", "warning", "info", "hint"} else "info")


def _spec_diagnostic_code(legacy_code: str, message: str) -> str:
    mapping = {
        "empty_source": "AGX0001",
        "unbalanced_braces": "AGX0001",
        "duplicate_declaration": "AGX0101",
        "unknown_derived_field": "AGX0202",
        "unknown_field_type": "AGX0201",
        "unknown_relation_target_table": "AGX0301",
        "unknown_reference_target_table": "AGX0301",
        "unknown_relation_target_field": "AGX0302",
        "unknown_reference_target_field": "AGX0302",
        "unknown_view_table": "AGX0401",
        "unknown_view_field": "AGX0402",
        "unknown_component_field": "AGX0402",
        "unknown_visual_component": "AGX0404",
        "rule_single_equals": "AGX0501",
        "strict_flow_state": "AGX0601",
        "unassigned_human_task": "AGX0602",
        "unknown_pbc_catalog_entry": "AGX0901",
        "unknown_cross_pbc_contract": "AGX0902",
        "private_pbc_table_access": "AGX0903",
        "unknown_agent_provider": "AGX1001",
        "unknown_agent_skill_target": "AGX1001",
        "agent_write_skill_permission": "AGX1002",
        "literal_api_key": "AGX0702",
        "unknown_app_target": "AGX0802",
    }
    if message.startswith("Unresolved lookup path"):
        return "AGX0303"
    if message.startswith("Unknown field type"):
        return "AGX0201"
    if message.startswith("Multi-hop lookup chain breaks"):
        return "AGX0304"
    if message.startswith("Unknown view table"):
        return "AGX0401"
    if message.startswith("Unknown table directive field"):
        return "AGX0303"
    if message.startswith("Unknown table directive target"):
        return "AGX0302"
    if message.startswith("Unknown handler target"):
        return "AGX0403"
    if message.startswith("Unknown contract target"):
        return "AGX0801"
    if message.startswith("Unknown package target"):
        return "AGX0802"
    if message.startswith("Unknown deployment"):
        return "AGX0801"
    if message.startswith("Invalid deployment"):
        return "AGX0801"
    if message.startswith("Unknown role resource"):
        return "AGX0701"
    if message.startswith("Unknown rule"):
        return "AGX0502"
    if message.startswith("Rule expression uses single ="):
        return "AGX0501"
    if message.startswith("Flow strict state"):
        return "AGX0601"
    if message.startswith("Human task has no assignee"):
        return "AGX0602"
    if message.startswith("Unknown PBC catalog entry"):
        return "AGX0901"
    if message.startswith("Unknown cross-PBC contract"):
        return "AGX0902"
    if message.startswith("Private PBC table access"):
        return "AGX0903"
    if message.startswith("Unknown agent skill target"):
        return "AGX1001"
    if message.startswith("Agent write-capable skill"):
        return "AGX1002"
    return mapping.get(legacy_code, "AGX0000" if legacy_code == "dsl_feedback" else "AGX0100")


def _spec_diagnostic_title(code: str) -> str:
    titles = {
        "AGX0001": "Source cannot be parsed",
        "AGX0101": "Duplicate declaration",
        "AGX0201": "Unknown field type",
        "AGX0202": "Unknown calculated-field reference",
        "AGX0301": "Unknown relationship table",
        "AGX0302": "Unknown relationship field",
        "AGX0303": "Unresolved lookup path",
        "AGX0304": "Broken multi-hop lookup chain",
        "AGX0401": "Unknown view table",
        "AGX0402": "Invalid database-backed view binding",
        "AGX0403": "Unknown handler target",
        "AGX0404": "Unknown visual component",
        "AGX0501": "Invalid rule equality operator",
        "AGX0502": "Unknown rule field",
        "AGX0601": "Invalid strict workflow state",
        "AGX0602": "Unassigned human task",
        "AGX0701": "Unknown permission resource",
        "AGX0702": "Secret literal in source",
        "AGX0801": "Invalid deployment or contract reference",
        "AGX0802": "Invalid package or target reference",
        "AGX0901": "Unknown PBC catalog entry",
        "AGX0902": "Unknown cross-PBC contract",
        "AGX0903": "Private PBC table access",
        "AGX1001": "Unknown agent reference",
        "AGX1002": "Write-capable agent skill lacks permission",
        "AGX1101": "Destructive migration",
        "AGX1201": "Unsupported natural-language plan",
        "AGX9000": "Internal tooling error",
        "AGX9001": "Unknown graph kind",
    }
    return titles.get(code, "DSL diagnostic")


def _spec_docs_url(code: str) -> str:
    if code.startswith("AGX03"):
        return "docs/tooling.md#diagnostic-specification"
    if code.startswith("AGX04"):
        return "docs/tooling.md#linter-rules-by-domain"
    if code.startswith("AGX09"):
        return "docs/pbc-catalog.md"
    return "docs/tooling.md#diagnostic-specification"


def _diagnostic_explanation(code: str) -> dict:
    return {
        "code": code,
        "title": _spec_diagnostic_title(code),
        "docs_url": _spec_docs_url(code),
        "summary": {
            "AGX0303": "A lookup path must resolve through declared relationships.",
            "AGX0402": "A database-backed form binding must resolve to a field, calculated field, or lookup path.",
            "AGX0403": "A handler must target a declared operation, flow, agent, or contract.",
            "AGX0901": "A composition can include only locally declared or registered PBC keys.",
            "AGX0902": "Cross-PBC links must reference exposed catalog APIs, events, or commands.",
            "AGX0903": "PBC composition cannot read or mutate another PBC's private tables.",
            "AGX1002": "Write-capable agent skills require an explicit permission grant.",
        }.get(code, "See the tooling diagnostic specification for this code."),
    }


def _symbol_query_to_id(symbol: str) -> str:
    if symbol.startswith(("table.", "view.", "flow.", "operation.", "pbc.", "agent.")):
        return symbol
    parts = symbol.split(".")
    if len(parts) == 2:
        return f"table.{parts[0]}.{parts[1]}"
    return symbol


def dsl_language_ergonomics_contract(text: str | None = None, *, source_name: str | None = None) -> dict:
    """Return evidence that the DSL stays learnable, compact, and pleasant to edit."""
    sample = text if text is not None else DSL_ERGONOMICS_SAMPLE
    formatted = format_dsl(sample, source_name=source_name)
    lint = lint_dsl(formatted["formatted"], source_name=source_name)
    score = dsl_authoring_score(formatted["formatted"], source_name=source_name)
    quality = dsl_language_quality_contract()
    alias_source = (
        "app AliasDemo { targets: web } "
        "entity Book { title: string searchable; secret: string hide } "
        "form BookForm for Book { Main: title } workflow Publish { draft -> live }"
    )
    alias_fix = apply_lint_fixes(alias_source, source_name=source_name)
    ref_source = "app RefDemo { targets: web } table Author { id: int pk } table Book { author_id: int ref Author.id }"
    ref_actions = dsl_code_actions(ref_source, source_name=source_name)
    source_kinds = {item["kind"] for item in SUPPORTED_SCHEMA_SOURCES}
    checks = (
        {
            "check": "compact_keyword_budget",
            "ok": quality["budget"]["ok"] and quality["canonical_keyword_count"] <= KEYWORD_LIMIT,
            "evidence": quality["budget"],
        },
        {
            "check": "keyword_free_expressiveness",
            "ok": {"-> references", "@ component placements", "... field groups", "= derived fields"} <= set(KEYWORD_FREE_SYNTAX),
            "syntax": KEYWORD_FREE_SYNTAX,
        },
        {
            "check": "friendly_aliases",
            "ok": alias_fix["after"]["ok"]
            and {"normalize_authoring_aliases", "normalize_modifier_aliases"} <= set(alias_fix["applied"]),
            "applied": alias_fix["applied"],
        },
        {
            "check": "legacy_ref_guidance",
            "ok": "ref" in LEGACY_CONTEXTUAL_TOKENS and any(action["id"] == "replace_ref_with_arrow" for action in ref_actions),
            "actions": tuple(action["id"] for action in ref_actions),
        },
        {
            "check": "formatter_stability",
            "ok": formatted["after"]["ok"] and format_dsl(formatted["formatted"])["formatted"] == formatted["formatted"],
            "changed": formatted["changed"],
        },
        {
            "check": "progressive_learning_path",
            "ok": len(LEARNING_PATH) == 4
            and LEARNING_PATH[0]["constructs"][0] == "app"
            and {"llm", "agent"} <= set(LEARNING_PATH[-1]["constructs"]),
            "learning_path": LEARNING_PATH,
        },
        {
            "check": "authoring_completion",
            "ok": lint["ok"] and score["ok"] and not score["next_actions"],
            "score": score["score"],
            "next_actions": score["next_actions"],
        },
        {
            "check": "source_family_guidance",
            "ok": {"dbml", "sql", "ponyorm", "database", "dsl"} <= source_kinds,
            "source_families": tuple(sorted(source_kinds)),
        },
    )
    return {
        "format": "appgen.dsl-language-ergonomics.v1",
        "source": source_name,
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "sample": formatted["formatted"],
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def dsl_language_experience_gate(text: str | None = None, *, source_name: str | None = None) -> dict:
    """Return outcome evidence for a delightful, intuitive, functional DSL."""
    source = text if text is not None else DSL_ERGONOMICS_SAMPLE
    formatted = format_dsl(source, source_name=source_name)
    canonical = formatted["formatted"]
    lint = lint_dsl(canonical, source_name=source_name)
    outline = dsl_outline(canonical, source_name=source_name)
    score = dsl_authoring_score(canonical, source_name=source_name)
    quality = dsl_language_quality_contract()
    ergonomics = dsl_language_ergonomics_contract(canonical, source_name=source_name)
    completions = dsl_completion_items(source=canonical)
    actions = dsl_code_actions("table Book { author_id: int ref Author.id }", source_name=source_name)
    summary = lint["summary"]
    source_kinds = {item["kind"] for item in SUPPORTED_SCHEMA_SOURCES}
    checks = (
        {
            "outcome": "delightful",
            "ok": ergonomics["ok"] and formatted["after"]["ok"] and len(completions) >= len(CORE_KEYWORDS),
            "evidence": ("language_ergonomics", "deterministic_formatter", "completion_catalog"),
        },
        {
            "outcome": "intuitive",
            "ok": score["ok"]
            and not score["next_actions"]
            and len(LEARNING_PATH) == 4
            and any(action["id"] == "replace_ref_with_arrow" for action in actions),
            "evidence": ("authoring_score", "progressive_learning_path", "code_actions"),
        },
        {
            "outcome": "functional",
            "ok": lint["ok"]
            and outline.get("ok") is True
            and summary["tables"] >= 2
            and summary["views"] >= 1
            and summary["flows"] >= 1
            and summary["llm_providers"] >= 1
            and summary["agents"] >= 1,
            "summary": summary,
        },
        {
            "outcome": "antlr_backed",
            "ok": quality["antlr_integrity"]["ok"],
            "evidence": quality["antlr_integrity"],
        },
        {
            "outcome": "keyword_limited",
            "ok": quality["budget"]["ok"] and quality["canonical_keyword_count"] <= KEYWORD_LIMIT,
            "evidence": quality["budget"],
        },
        {
            "outcome": "multi_source_ready",
            "ok": {"dbml", "sql", "ponyorm", "database", "dsl"} <= source_kinds,
            "source_families": tuple(sorted(source_kinds)),
        },
    )
    return {
        "format": "appgen.dsl-language-experience-gate.v1",
        "source": source_name,
        "ok": all(check["ok"] for check in checks),
        "language": "appgen-dsl",
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "sample": canonical,
    }


def dsl_authoring_release_gate(
    text: str,
    *,
    source_name: str | None = None,
    expected_sources: Iterable[str] = ("dbml", "sql", "ponyorm", "database", "dsl"),
) -> dict:
    """Return release evidence for the full DSL authoring experience."""
    source = text or ""
    lint = lint_dsl(source, source_name=source_name)
    outline = dsl_outline(source, source_name=source_name)
    formatting = format_dsl(source, source_name=source_name)
    score = dsl_authoring_score(source, source_name=source_name)
    quality = dsl_language_quality_contract()
    ergonomics = dsl_language_ergonomics_contract(source, source_name=source_name)
    experience = dsl_language_experience_gate(source_name=source_name)
    completions = dsl_completion_items(source=source)
    actions = dsl_code_actions(source, source_name=source_name)
    source_catalog = tuple(
        {
            "kind": item["kind"],
            "entrypoint": item["entrypoint"],
            "command": item["command"],
        }
        for item in SUPPORTED_SCHEMA_SOURCES
    )
    supported_sources = {item["kind"] for item in source_catalog}
    required_sources = tuple(expected_sources)
    summary = lint["summary"]
    gates = (
        {
            "gate": "language_quality",
            "ok": quality["ok"],
            "evidence": quality["checks"],
        },
        {
            "gate": "keyword_budget",
            "ok": quality["budget"]["ok"] and quality["canonical_keyword_count"] <= quality["budget"]["limit"],
            "evidence": quality["budget"],
        },
        {
            "gate": "syntax_semantics",
            "ok": lint["ok"],
            "errors": lint["errors"],
            "warnings": lint["warnings"],
        },
        {
            "gate": "formatter_stability",
            "ok": formatting["after"]["ok"] and source.strip() == formatting["formatted"].strip(),
            "changed": formatting["changed"],
        },
        {
            "gate": "outline_and_navigation",
            "ok": outline.get("ok") is True and bool(outline.get("blocks")) and summary["tables"] > 0,
            "block_count": len(outline.get("blocks", ())),
        },
        {
            "gate": "source_family_coverage",
            "ok": set(required_sources) <= supported_sources,
            "required": required_sources,
            "supported": tuple(item["kind"] for item in source_catalog),
        },
        {
            "gate": "authoring_guidance",
            "ok": score["ok"] and not score["next_actions"],
            "score": score["score"],
            "next_actions": score["next_actions"],
        },
        {
            "gate": "language_ergonomics",
            "ok": ergonomics["ok"],
            "evidence": ergonomics["checks"],
        },
        {
            "gate": "language_experience",
            "ok": experience["ok"],
            "evidence": experience["checks"],
        },
        {
            "gate": "ide_contract",
            "ok": bool(completions) and all(action.get("format") == "appgen.dsl-code-action.v1" for action in actions),
            "completion_count": len(completions),
            "code_action_count": len(actions),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.dsl-authoring-release-gate.v1",
        "source": source_name,
        "language": "appgen-dsl",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "gates": gates,
        "source_families": source_catalog,
        "summary": summary,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }


def dsl_authoring_score(text: str, *, source_name: str | None = None) -> dict:
    """Return IDE-ready guidance for making a DSL source complete and approachable."""
    source = text or ""
    lint = lint_dsl(source, source_name=source_name)
    outline = dsl_outline(source, source_name=source_name)
    summary = lint["summary"]
    formatted = _format_dsl_source(source)
    checks = (
        {
            "check": "syntax_and_semantics",
            "ok": lint["ok"],
            "weight": 30,
            "next_action": "Fix parser or semantic diagnostics before generation.",
        },
        {
            "check": "named_application",
            "ok": bool(outline.get("app")),
            "weight": 10,
            "next_action": "Add an app declaration with generation targets.",
        },
        {
            "check": "data_model",
            "ok": summary["tables"] > 0 and summary["fields"] > 0,
            "weight": 15,
            "next_action": "Add at least one table with fields.",
        },
        {
            "check": "form_design",
            "ok": summary["views"] > 0,
            "weight": 10,
            "next_action": "Add a view block or visual component placement.",
        },
        {
            "check": "target_selection",
            "ok": bool(summary["targets"]) and not summary["unknown_targets"],
            "weight": 10,
            "next_action": "Choose supported targets: web, pwa, mobile, desktop, or chatbot.",
        },
        {
            "check": "keyword_budget",
            "ok": dsl_keyword_budget()["ok"],
            "weight": 10,
            "next_action": "Keep new concepts as options, aliases, or symbols instead of new keywords.",
        },
        {
            "check": "canonical_style",
            "ok": not lint["warnings"],
            "weight": 10,
            "next_action": "Apply quick fixes for aliases, legacy refs, or literal API keys.",
        },
        {
            "check": "formatted",
            "ok": source.strip() == formatted.strip(),
            "weight": 5,
            "next_action": "Run the deterministic formatter.",
        },
    )
    earned = sum(item["weight"] for item in checks if item["ok"])
    total = sum(item["weight"] for item in checks)
    blocking = tuple(item for item in checks if not item["ok"])
    return {
        "format": "appgen.dsl-authoring-score.v1",
        "source": source_name,
        "score": round((earned / total) * 100),
        "ok": lint["ok"] and earned >= 80,
        "checks": checks,
        "next_actions": tuple(item["next_action"] for item in blocking),
        "quick_fix_ids": tuple(fix["id"] for fix in lint["fixes"]),
        "summary": summary,
    }


def dsl_code_actions(text: str, *, source_name: str | None = None) -> tuple[dict, ...]:
    """Return IDE-ready code actions for deterministic DSL quick fixes."""
    source = text or ""
    report = lint_dsl(source, source_name=source_name)
    diagnostics = report["diagnostics"]
    actions = []
    for fix in report["fixes"]:
        related = tuple(
            diagnostic
            for diagnostic in diagnostics
            if fix["id"] in diagnostic.get("fix_ids", ())
        )
        fixed_preview = _apply_lint_fix(source, fix)
        actions.append(
            {
                "format": "appgen.dsl-code-action.v1",
                "id": fix["id"],
                "title": fix["title"],
                "kind": "quickfix",
                "source": source_name,
                "diagnostic_codes": tuple(diagnostic["code"] for diagnostic in related),
                "diagnostics": related,
                "edits": _fix_edits(source, fix),
                "command": {
                    "name": "appgen.applyDslFix",
                    "arguments": (fix["id"],),
                },
                "changed": fixed_preview != source,
                "fixed_preview": fixed_preview,
            }
        )
    return tuple(actions)


def _format_dsl_source(source: str) -> str:
    units = _dsl_format_units(source)
    lines: list[str] = []
    indent = 0
    previous_closed_top_level = False

    for unit in units:
        if unit == "}":
            indent = max(indent - 1, 0)
            lines.append("  " * indent + "}")
            previous_closed_top_level = indent == 0
            continue
        if unit == "{":
            if lines and lines[-1].strip():
                lines[-1] = lines[-1].rstrip() + " {"
            else:
                lines.append("  " * indent + "{")
            indent += 1
            previous_closed_top_level = False
            continue
        if previous_closed_top_level and lines and lines[-1] != "":
            lines.append("")
        lines.append("  " * indent + _normalize_dsl_spacing(unit))
        previous_closed_top_level = False

    return "\n".join(lines).rstrip() + ("\n" if lines else "")


def _dsl_format_units(source: str) -> tuple[str, ...]:
    units: list[str] = []
    buffer: list[str] = []
    quote: str | None = None
    escape = False

    def flush() -> None:
        value = "".join(buffer).strip()
        buffer.clear()
        if value:
            units.append(value)

    for char in source:
        if quote:
            buffer.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            buffer.append(char)
            continue
        if char in "{};":
            flush()
            if char in "{}":
                units.append(char)
            continue
        if char in "\r\n":
            flush()
            continue
        buffer.append(char)
    flush()
    return tuple(units)


def _normalize_dsl_spacing(unit: str) -> str:
    value = re.sub(r"\s+", " ", unit.strip())
    value = re.sub(r"\s*,\s*", ", ", value)
    value = re.sub(r"\s*:\s*", ": ", value)
    value = re.sub(r"\s*->\s*", " -> ", value)
    value = re.sub(r"\s*=\s*", " = ", value)
    value = re.sub(r"\s*\[\s*", " [", value)
    value = re.sub(r"\s*\]\s*", "]", value)
    return _normalize_field_modifier_order(value.strip())


def _normalize_field_modifier_order(value: str) -> str:
    if value.startswith("//") or ":" not in value:
        return value
    code, comment = _split_inline_comment(value)
    match = re.match(r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?P<rest>.+)$", code)
    if match is None:
        return value
    tokens = _tokenize_formatter_unit(match.group("rest"))
    if len(tokens) < 2:
        return value
    type_name = tokens[0]
    if tokens[1] == "=":
        return value
    ordered_flags = {"pk": False, "required": False, "unique": False, "hidden": False, "search": False}
    default_tokens: list[str] = []
    relation_tokens: list[str] = []
    other_tokens: list[str] = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token in ordered_flags:
            ordered_flags[token] = True
            index += 1
            continue
        if token == "default":
            default_tokens = [token]
            index += 1
            if index < len(tokens):
                default_tokens.append(tokens[index])
                index += 1
            continue
        if token == "->":
            relation_tokens = [token]
            index += 1
            if index < len(tokens):
                relation_tokens.append(tokens[index])
                index += 1
            if index < len(tokens) and re.fullmatch(r"\[[^\]]+\]", tokens[index]):
                relation_tokens.append(tokens[index])
                index += 1
            continue
        other_tokens.append(token)
        index += 1
    modifiers = [name for name in ("pk", "required", "unique", "hidden", "search") if ordered_flags[name]]
    modifiers.extend(default_tokens)
    modifiers.extend(relation_tokens)
    modifiers.extend(other_tokens)
    formatted = f"{match.group('name')}: {' '.join((type_name, *modifiers)).strip()}"
    return f"{formatted} {comment}" if comment else formatted


def _split_inline_comment(value: str) -> tuple[str, str]:
    quote: str | None = None
    escape = False
    for index in range(len(value) - 1):
        char = value[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "/" and value[index + 1] == "/":
            return value[:index].rstrip(), value[index:].strip()
    return value, ""


def _tokenize_formatter_unit(value: str) -> list[str]:
    tokens: list[str] = []
    buffer: list[str] = []
    quote: str | None = None
    bracket_depth = 0
    escape = False

    def flush() -> None:
        token = "".join(buffer).strip()
        buffer.clear()
        if token:
            tokens.append(token)

    for char in value:
        if quote:
            buffer.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            buffer.append(char)
            continue
        if char == "[":
            bracket_depth += 1
            buffer.append(char)
            continue
        if char == "]":
            bracket_depth = max(bracket_depth - 1, 0)
            buffer.append(char)
            continue
        if char.isspace() and bracket_depth == 0:
            flush()
            continue
        buffer.append(char)
    flush()
    return tokens


def _apply_lint_fix(source: str, fix: dict) -> str:
    kind = fix.get("kind")
    if kind == "replace_all":
        return str(fix["replacement"])
    if kind == "insert" and fix.get("position") == "start":
        return str(fix["insert"]) + source
    if kind == "regex_replace":
        return re.sub(str(fix["pattern"]), str(fix["replacement"]), source)
    if kind == "replace_targets":
        return _apply_target_normalization(source, tuple(fix["supported"]))
    if kind == "normalize_aliases":
        return _normalize_authoring_aliases(source)
    if kind == "normalize_modifier_aliases":
        return _normalize_modifier_aliases(source)
    return source


def _apply_target_normalization(source: str, supported: tuple[str, ...]) -> str:
    def repl(match: re.Match[str]) -> str:
        prefix, raw_values = match.groups()
        kept = []
        for value in raw_values.split(","):
            target = value.strip().strip("'\"").lower().replace("-", "_")
            if target in supported and target not in kept:
                kept.append(target)
        if not kept:
            kept.append("web")
        return prefix + ", ".join(kept)

    return re.sub(r"(\btargets\s*:\s*)([^;\n}]+)", repl, source)


def _fix_edits(source: str, fix: dict) -> tuple[dict, ...]:
    kind = fix.get("kind")
    if kind == "replace_all":
        return (
            {
                "range": _source_range(source, 0, len(source)),
                "replacement": str(fix["replacement"]),
            },
        )
    if kind == "insert" and fix.get("position") == "start":
        return (
            {
                "range": _source_range(source, 0, 0),
                "replacement": str(fix["insert"]),
            },
        )
    if kind == "regex_replace":
        pattern = re.compile(str(fix["pattern"]))
        replacement = str(fix["replacement"])
        return tuple(
            {
                "range": _source_range(source, match.start(), match.end()),
                "replacement": match.expand(replacement),
            }
            for match in pattern.finditer(source)
        )
    if kind == "replace_targets":
        match = re.search(r"(\btargets\s*:\s*)([^;\n}]+)", source)
        if match:
            fixed = _apply_target_normalization(source, tuple(fix["supported"]))
            fixed_match = re.search(r"(\btargets\s*:\s*)([^;\n}]+)", fixed)
            if fixed_match:
                return (
                    {
                        "range": _source_range(source, match.start(2), match.end(2)),
                        "replacement": fixed_match.group(2),
                    },
                )
    if kind == "normalize_aliases":
        fixed = _normalize_authoring_aliases(source)
        if fixed != source:
            return (
                {
                    "range": _source_range(source, 0, len(source)),
                    "replacement": fixed,
                },
            )
    if kind == "normalize_modifier_aliases":
        fixed = _normalize_modifier_aliases(source)
        if fixed != source:
            return (
                {
                    "range": _source_range(source, 0, len(source)),
                    "replacement": fixed,
                },
            )
    return ()


def _source_range(source: str, start: int, end: int) -> dict:
    start_line, start_character = _line_column_for_index(source, start)
    end_line, end_character = _line_column_for_index(source, end)
    return {
        "start": {"line": start_line, "character": start_character},
        "end": {"line": end_line, "character": end_character},
    }


def _line_column_for_index(source: str, index: int) -> tuple[int, int]:
    bounded = max(0, min(index, len(source)))
    line = source.count("\n", 0, bounded)
    previous_newline = source.rfind("\n", 0, bounded)
    character = bounded if previous_newline < 0 else bounded - previous_newline - 1
    return line, character


def _lint_quick_fixes(source: str, errors: Iterable[str], warnings: Iterable[str]) -> tuple[dict, ...]:
    """Return deterministic quick fixes for common DSL authoring feedback."""
    fixes: list[dict] = []
    if source.strip() and not re.search(r"\bapp\s+", source):
        fixes.append(
            {
                "id": "add_app_declaration",
                "title": "Add an app declaration",
                "kind": "insert",
                "insert": "app Generated { targets: web }\n\n",
                "position": "start",
            }
        )
    if "DSL source is empty." in errors:
        fixes.append(
            {
                "id": "insert_minimal_app",
                "title": "Insert a minimal app and table",
                "kind": "replace_all",
                "replacement": "app Generated { targets: web }\n\ntable Thing {\n  id: int pk\n  name: string required search\n}\n",
            }
        )
    if re.search(r"\bref\s+([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)", source):
        fixes.append(
            {
                "id": "replace_ref_with_arrow",
                "title": "Use arrow reference syntax",
                "kind": "regex_replace",
                "pattern": r"\bref\s+([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)",
                "replacement": r"-> \1.\2",
            }
        )
    if re.search(r"api_key\s*:\s*['\"]", source):
        fixes.append(
            {
                "id": "use_api_key_env",
                "title": "Use an environment variable for api_key",
                "kind": "regex_replace",
                "pattern": r"api_key\s*:\s*['\"][^'\"]+['\"]",
                "replacement": "api_key: OPENAI_API_KEY",
            }
        )
    if _preparse_tooling_errors(source):
        fixes.append(
            {
                "id": "replace_rule_equals_with_eqeq",
                "title": "Use == for rule equality",
                "kind": "regex_replace",
                "pattern": r"(?<![!<>=])=(?!=)",
                "replacement": "==",
            }
        )
    if _uses_authoring_aliases(source):
        fixes.append(
            {
                "id": "normalize_authoring_aliases",
                "title": "Normalize authoring aliases to canonical DSL words",
                "kind": "normalize_aliases",
                "aliases": dict(AUTHORING_ALIASES),
            }
        )
    if _uses_modifier_aliases(source):
        fixes.append(
            {
                "id": "normalize_modifier_aliases",
                "title": "Normalize modifier aliases to canonical DSL words",
                "kind": "normalize_modifier_aliases",
                "aliases": dict(MODIFIER_ALIASES),
            }
        )
    for error in errors:
        if error.startswith("Unknown app targets"):
            fixes.append(
                {
                    "id": "normalize_targets",
                    "title": "Keep only supported app targets",
                    "kind": "replace_targets",
                    "supported": ("web", "pwa", "mobile", "desktop", "chatbot"),
                }
            )
            break
    return tuple(fixes)


def _lint_diagnostics(
    source: str,
    errors: Iterable[str],
    warnings: Iterable[str],
    suggestions: Iterable[str],
) -> tuple[dict, ...]:
    """Return structured diagnostics suitable for IDEs and CI annotations."""
    diagnostics = []
    for message in errors:
        diagnostics.append(_diagnostic(source, "error", message))
    for message in warnings:
        diagnostics.append(_diagnostic(source, "warning", message))
    for message in suggestions:
        diagnostics.append(_diagnostic(source, "suggestion", message))
    return tuple(diagnostics)


def _diagnostic_severity_counts(
    errors: Iterable[str],
    warnings: Iterable[str],
    suggestions: Iterable[str],
) -> dict:
    return {
        "error": len(tuple(errors)),
        "warning": len(tuple(warnings)),
        "suggestion": len(tuple(suggestions)),
    }


def _diagnostic(source: str, severity: str, message: str) -> dict:
    code = _diagnostic_code(message)
    token = _diagnostic_token(message)
    line, column = _locate_token(source, token)
    diagnostic = {
        "severity": severity,
        "code": code,
        "message": message,
        "line": line,
        "column": column,
        "fix_ids": _diagnostic_fix_ids(code),
    }
    hint = _diagnostic_hint(message)
    if hint:
        diagnostic["hint"] = hint
    return diagnostic


def _diagnostic_code(message: str) -> str:
    if message == "DSL source is empty.":
        return "empty_source"
    if message.startswith("Unbalanced braces"):
        return "unbalanced_braces"
    if message.startswith("Unknown app targets"):
        return "unknown_app_target"
    if message.startswith("Unknown field type"):
        return "unknown_field_type"
    if message.startswith("Multi-hop lookup chain breaks"):
        return "multi_hop_lookup_break"
    if message.startswith("Unresolved lookup path"):
        return "unresolved_lookup_path"
    if message.startswith("Unknown view table"):
        return "unknown_view_table"
    if message.startswith("Unknown view field"):
        return "unknown_view_field"
    if message.startswith("Unknown component field"):
        return "unknown_component_field"
    if message.startswith("Unknown visual component"):
        return "unknown_visual_component"
    if message.startswith("Rule expression uses single ="):
        return "rule_single_equals"
    if message.startswith("Flow strict state"):
        return "strict_flow_state"
    if message.startswith("Human task has no assignee"):
        return "unassigned_human_task"
    if message.startswith("Unknown PBC catalog entry"):
        return "unknown_pbc_catalog_entry"
    if message.startswith("Unknown cross-PBC contract"):
        return "unknown_cross_pbc_contract"
    if message.startswith("Private PBC table access"):
        return "private_pbc_table_access"
    if message.startswith("Unknown agent skill target"):
        return "unknown_agent_skill_target"
    if message.startswith("Agent write-capable skill"):
        return "agent_write_skill_permission"
    if message.startswith("Unknown agent provider"):
        return "unknown_agent_provider"
    if message.startswith("Unknown relation target table"):
        return "unknown_relation_target_table"
    if message.startswith("Unknown relation target field"):
        return "unknown_relation_target_field"
    if message.startswith("Unknown reference target table"):
        return "unknown_reference_target_table"
    if message.startswith("Unknown reference target field"):
        return "unknown_reference_target_field"
    if message.startswith("Unknown derived-field reference"):
        return "unknown_derived_field"
    if message.startswith("Duplicate"):
        return "duplicate_declaration"
    if "Prefer arrow references" in message:
        return "prefer_arrow_reference"
    if "environment variable" in message:
        return "literal_api_key"
    if "canonical DSL modifier words" in message:
        return "modifier_alias"
    if "canonical DSL words" in message:
        return "authoring_alias"
    if "visual component" in message:
        return "missing_view_blocks"
    if "agentic behavior" in message:
        return "missing_agentic_blocks"
    if "Add at least one table" in message:
        return "missing_tables"
    if "app declaration" in message:
        return "missing_app_declaration"
    return "dsl_feedback"


def _diagnostic_token(message: str) -> str | None:
    for pattern in (
        r"Unknown app targets: ([^.]+)\.",
        r"Unknown field type: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Multi-hop lookup chain breaks: [^.]+\.([A-Za-z_][A-Za-z0-9_.]*)",
        r"Unresolved lookup path: [^.]+\.([A-Za-z_][A-Za-z0-9_.]*)",
        r"Unknown view table: [^.]+ for ([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown view field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown component field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown visual component: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Flow strict state is undeclared: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Human task has no assignee: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown PBC catalog entry: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown agent provider: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown agent skill target: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown (?:relation|reference) target table: ([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown (?:relation|reference) target field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Duplicate [^:]+ declaration: ([A-Za-z_][A-Za-z0-9_]*)",
    ):
        match = re.search(pattern, message)
        if match:
            return match.group(1).split(",", 1)[0].strip()
    return None


def _locate_token(source: str, token: str | None) -> tuple[int | None, int | None]:
    if not token:
        return None, None
    index = source.find(token)
    if index < 0:
        return None, None
    line = source.count("\n", 0, index) + 1
    previous_newline = source.rfind("\n", 0, index)
    column = index if previous_newline < 0 else index - previous_newline - 1
    return line, column


def _diagnostic_fix_ids(code: str) -> tuple[str, ...]:
    fixes = {
        "empty_source": ("insert_minimal_app",),
        "missing_app_declaration": ("add_app_declaration",),
        "prefer_arrow_reference": ("replace_ref_with_arrow",),
        "literal_api_key": ("use_api_key_env",),
        "authoring_alias": ("normalize_authoring_aliases",),
        "modifier_alias": ("normalize_modifier_aliases",),
        "unknown_app_target": ("normalize_targets",),
        "rule_single_equals": ("replace_rule_equals_with_eqeq",),
        "literal_api_key": ("use_api_key_env",),
    }
    return fixes.get(code, ())


def _diagnostic_hint(message: str) -> str | None:
    if "Did you mean" in message:
        return message.rsplit("Did you mean", 1)[1].strip().rstrip("?")
    if message.startswith("Unknown app targets"):
        return "Run normalize_targets to keep only web, pwa, mobile, desktop, and chatbot."
    return None


def _semantic_suggestions(source: str, errors: Iterable[str]) -> tuple[str, ...]:
    """Return typo-oriented suggestions for semantic linter errors."""
    table_fields = _declared_table_fields_for_suggestions(source)
    view_tables = _declared_view_tables_for_suggestions(source)
    llm_names = _declared_block_names(source, "llm")
    table_names = tuple(table_fields)
    suggestions = []
    for error in errors:
        if error.startswith(("Unknown view field:", "Unknown component field:")):
            view_name, field_name = _split_qualified_error(error)
            table_name = view_tables.get(view_name)
            match = _closest(field_name, table_fields.get(table_name or "", ()))
            if match:
                suggestions.append(f"{error} Did you mean {match}?")
        elif error.startswith("Unknown agent provider:"):
            _agent_name, provider_name = _split_qualified_error(error)
            match = _closest(provider_name, llm_names)
            if match:
                suggestions.append(f"{error} Did you mean {match}?")
        elif error.startswith(("Unknown relation target table:", "Unknown reference target table:")):
            table_name = error.rsplit(":", 1)[1].strip()
            match = _closest(table_name, table_names)
            if match:
                suggestions.append(f"{error} Did you mean {match}?")
        elif error.startswith(("Unknown relation target field:", "Unknown reference target field:")):
            table_name, field_name = _split_qualified_error(error)
            match = _closest(field_name, table_fields.get(table_name, ()))
            if match:
                suggestions.append(f"{error} Did you mean {match}?")
    return tuple(suggestions)


def _split_qualified_error(error: str) -> tuple[str, str]:
    qualified = error.rsplit(":", 1)[1].strip()
    if "." not in qualified:
        return "", qualified
    left, right = qualified.split(".", 1)
    return left, right


def _closest(value: str, choices: Iterable[str]) -> str | None:
    matches = difflib.get_close_matches(value, tuple(choices), n=1, cutoff=0.6)
    return matches[0] if matches else None


def _declared_block_names(source: str, kind: str) -> tuple[str, ...]:
    normalized = _normalize_modifier_aliases(_normalize_authoring_aliases(source or ""))
    return tuple(
        match.group(1)
        for match in re.finditer(
            r"\b" + re.escape(kind) + r"\s+([A-Za-z_][A-Za-z0-9_]*)\b",
            normalized,
        )
    )


def _declared_view_tables_for_suggestions(source: str) -> dict[str, str]:
    normalized = _normalize_modifier_aliases(_normalize_authoring_aliases(source or ""))
    return {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"\bview\s+([A-Za-z_][A-Za-z0-9_]*)\s+for\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{",
            normalized,
        )
    }


def _declared_table_fields_for_suggestions(source: str) -> dict[str, tuple[str, ...]]:
    normalized = _normalize_modifier_aliases(_normalize_authoring_aliases(source or ""))
    fields: dict[str, tuple[str, ...]] = {}
    pattern = re.compile(r"\btable\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{(?P<body>.*?)\}", re.S)
    for match in pattern.finditer(normalized):
        names = []
        for line in re.split(r"[;\n]+", match.group("body")):
            stripped = line.strip()
            if not stripped or stripped.startswith("..."):
                continue
            field_match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", stripped)
            if field_match:
                names.append(field_match.group(1))
        fields[match.group(1)] = tuple(names)
    return fields


def schema_from_dsl(text: str, *, source_name: str | None = None) -> AppSchema:
    """Parse AppGen DSL source into the canonical app schema."""
    text = _normalize_app_option_sugar(
        _normalize_table_line_boundaries(
            _normalize_reference_sugar(_normalize_modifier_aliases(_normalize_authoring_aliases(text)))
        )
    )
    tree = _parse(text)
    app_decl = tree.appDecl()
    app_name = _app_name(app_decl) if app_decl else None
    app_options = _app_options(app_decl) if app_decl else {}
    _validate_app_options(app_options)

    tables: list[TableSchema] = []
    relations: list[RelationSchema] = []
    views: list[ViewSchema] = []
    flows: list[FlowSchema] = []
    roles: list[RoleSchema] = []
    rules: list[RuleSchema] = []
    enums: list[EnumSchema] = []
    llm_providers: list[LLMProviderSchema] = []
    agents: list[AgentSchema] = []
    platform_blocks: list[PlatformBlockSchema] = []
    api_contracts: list[EnterpriseContractSchema] = []
    event_contracts: list[EnterpriseContractSchema] = []
    job_contracts: list[EnterpriseContractSchema] = []
    report_contracts: list[EnterpriseContractSchema] = []
    menu_contracts: list[EnterpriseContractSchema] = []
    component_contracts: list[EnterpriseContractSchema] = []
    package_contracts: list[EnterpriseContractSchema] = []
    test_contracts: list[EnterpriseContractSchema] = []
    groups = {
        element.groupDecl().IDENT().getText(): element.groupDecl().tableBody()
        for element in tree.element()
        if element.groupDecl()
    }

    for element in tree.element():
        if element.tableDecl():
            table, table_relations = _table(element.tableDecl(), groups)
            tables.append(table)
            relations.extend(table_relations)
        elif element.relationDecl():
            relations.append(_relation(element.relationDecl()))
        elif element.enumDecl():
            enums.append(_enum(element.enumDecl()))
        elif element.viewDecl():
            views.append(_view(element.viewDecl()))
        elif element.flowDecl():
            flows.append(_flow(element.flowDecl()))
        elif element.roleDecl():
            roles.append(_role(element.roleDecl()))
        elif element.ruleDecl():
            rules.append(_rule(element.ruleDecl()))
        elif element.llmDecl():
            llm_providers.append(_llm_provider(element.llmDecl()))
        elif element.agentDecl():
            agents.append(_agent(element.agentDecl()))
        elif element.pbcDecl():
            platform_blocks.append(_pbc_block(element.pbcDecl()))
        elif element.compositionDecl():
            platform_blocks.append(_composition_block(element.compositionDecl()))
        elif element.auditDecl():
            platform_blocks.append(_agentic_platform_block("audit", element.auditDecl()))
        elif element.deploymentDecl():
            platform_blocks.append(_deployment_block(element.deploymentDecl()))
        elif element.versionDecl():
            platform_blocks.append(_agentic_platform_block("version", element.versionDecl()))
        elif element.operationDecl():
            platform_blocks.append(_operation_block(element.operationDecl()))
        elif element.securityDecl():
            platform_blocks.append(_security_block(element.securityDecl()))
        elif element.apiDecl():
            api_contracts.append(_enterprise_contract("api", element.apiDecl()))
        elif element.eventDecl():
            event_contracts.append(_enterprise_contract("event", element.eventDecl()))
        elif element.jobDecl():
            job_contracts.append(_enterprise_contract("job", element.jobDecl()))
        elif element.reportDecl():
            report_contracts.append(_enterprise_contract("report", element.reportDecl()))
        elif element.menuDecl():
            menu_contracts.append(_enterprise_contract("menu", element.menuDecl()))
        elif element.componentDecl():
            component_contracts.append(_enterprise_contract("component", element.componentDecl()))
        elif element.packageDecl():
            package_contracts.append(_enterprise_contract("package", element.packageDecl()))
        elif element.testDecl():
            test_contracts.append(_enterprise_contract("test", element.testDecl()))

    tables = _apply_external_relations(tables, relations)
    schema = AppSchema(
        tables=tuple(tables),
        relations=tuple(relations),
        source=source_name,
        app_name=app_name,
        app_options=app_options,
        views=tuple(views),
        flows=tuple(flows),
        roles=tuple(roles),
        rules=tuple(rules),
        enums=tuple(enums),
        llm_providers=tuple(llm_providers),
        agents=tuple(agents),
        platform_blocks=tuple(platform_blocks),
        api_contracts=tuple(api_contracts),
        event_contracts=tuple(event_contracts),
        job_contracts=tuple(job_contracts),
        report_contracts=tuple(report_contracts),
        menu_contracts=tuple(menu_contracts),
        component_contracts=tuple(component_contracts),
        package_contracts=tuple(package_contracts),
        test_contracts=tuple(test_contracts),
    )
    _validate_schema(schema)
    return schema


def _lint_summary(schema: AppSchema | None) -> dict:
    if schema is None:
        return {
            "tables": 0,
            "fields": 0,
            "views": 0,
            "flows": 0,
            "roles": 0,
            "rules": 0,
            "llm_providers": 0,
            "agents": 0,
            "platform_blocks": 0,
            "enterprise_contracts": 0,
            "targets": (),
        }
    targets, unknown = normalize_platform_targets(schema.app_options.get("targets"))
    return {
        "app": schema.app_name,
        "tables": len(schema.tables),
        "fields": sum(len(table.columns) for table in schema.tables),
        "views": len(schema.views),
        "flows": len(schema.flows),
        "roles": len(schema.roles),
        "rules": len(schema.rules),
        "llm_providers": len(schema.llm_providers),
        "agents": len(schema.agents),
        "platform_blocks": len(schema.platform_blocks),
        "enterprise_contracts": len(_enterprise_contracts(schema)),
        "targets": targets,
        "unknown_targets": unknown,
    }


def _dsl_snippets() -> tuple[dict, ...]:
    return (
        {
            "label": "Application",
            "insert": "app MyApp { targets: web, mobile, desktop }",
            "kind": "snippet",
            "detail": "Name the app and choose generation targets.",
        },
        {
            "label": "Table",
            "insert": "table Customer {\n  id: int pk\n  name: string required search\n}",
            "kind": "snippet",
            "detail": "Data model block.",
        },
        {
            "label": "Form",
            "insert": "view CustomerForm for Customer {\n  Main: name\n}",
            "kind": "snippet",
            "detail": "Generated form/view block.",
        },
        {
            "label": "Visual Component",
            "insert": "@ name TextBox 0 0 6 1",
            "kind": "snippet",
            "detail": "Drop a component at x y width height.",
        },
        {
            "label": "Local LLM",
            "insert": "llm LocalModel {\n  provider: ollama\n  mode: local\n  model: llama3\n}",
            "kind": "snippet",
            "detail": "Local LLM provider.",
        },
        {
            "label": "Agent",
            "insert": "agent Assistant {\n  provider: LocalModel\n  goal: \"Help users finish work\"\n  tools: schema, forms, reports\n}",
            "kind": "snippet",
            "detail": "Agentic workflow block.",
        },
        {
            "label": "API Contract",
            "insert": "api OrdersApi {\n  GET \"/orders\" -> ListOrders\n  auth: Order.read\n}",
            "kind": "snippet",
            "detail": "Generated API operation contract.",
        },
        {
            "label": "Package",
            "insert": "package Release {\n  targets: web, mobile, desktop\n  channel: stable\n}",
            "kind": "snippet",
            "detail": "Generated app packaging contract.",
        },
    )


def _outline_blocks(source: str, schema: AppSchema) -> tuple[dict, ...]:
    names = [("app", schema.app_name)] if schema.app_name else []
    names.extend(("table", table.name) for table in schema.tables)
    names.extend(("enum", enum.name) for enum in schema.enums)
    names.extend(("view", view.name) for view in schema.views)
    names.extend(("flow", flow.name) for flow in schema.flows)
    names.extend(("role", role.name) for role in schema.roles)
    names.extend(("rule", rule.name) for rule in schema.rules)
    names.extend(("llm", provider.name) for provider in schema.llm_providers)
    names.extend(("agent", agent.name) for agent in schema.agents)
    names.extend((block.kind, block.name) for block in schema.platform_blocks)
    names.extend((contract.kind, contract.name) for contract in _enterprise_contracts(schema))
    return tuple(_outline_block(source, kind, name) for kind, name in names if name)


def _outline_block(source: str, kind: str, name: str) -> dict:
    line, column = _locate_token(source, name)
    return {"kind": kind, "name": name, "line": line, "column": column}


def _regex_outline(source: str, *, source_name: str | None = None, error: str | None = None) -> dict:
    normalized = _normalize_modifier_aliases(_normalize_authoring_aliases(source or ""))
    app_match = re.search(r"\bapp\s+(\"[^\"]+\"|'[^']+'|[A-Za-z_][A-Za-z0-9_]*)?", normalized)
    app_name = None
    if app_match and app_match.group(1):
        app_name = app_match.group(1).strip("'\"")
    tables = tuple(
        {
            "name": table_name,
            "fields": fields,
            "search_fields": (),
            "hidden_fields": (),
            "relations": (),
        }
        for table_name, fields in _declared_table_fields_for_suggestions(normalized).items()
    )
    return {
        "format": "appgen.dsl-outline.v1",
        "source": source_name,
        "ok": False,
        "app": app_name,
        "targets": (),
        "blocks": tuple(
            _outline_block(normalized, kind, name)
            for kind in (
                "table",
                "enum",
                "view",
                "flow",
                "role",
                "rule",
                "llm",
                "agent",
                "api",
                "event",
                "job",
                "report",
                "menu",
                "component",
                "package",
                "test",
            )
            for name in _declared_block_names(normalized, kind)
        ),
        "tables": tables,
        "views": tuple(
            {
                "name": view_name,
                "table": table_name,
                "fields": (),
                "sections": (),
                "components": (),
            }
            for view_name, table_name in _declared_view_tables_for_suggestions(normalized).items()
        ),
        "flows": tuple({"name": name, "steps": ()} for name in _declared_block_names(normalized, "flow")),
        "roles": _declared_block_names(normalized, "role"),
        "rules": _declared_block_names(normalized, "rule"),
        "llms": _declared_block_names(normalized, "llm"),
        "agents": _declared_block_names(normalized, "agent"),
        "summary": {"tables": len(tables), "fields": sum(len(table["fields"]) for table in tables)},
        "parse_error": error,
    }


def _parse(source: str):
    lexer = appgenLexer(InputStream(source))
    parser = appgenParser(CommonTokenStream(lexer))
    errors = _CollectingErrorListener()
    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    lexer.addErrorListener(errors)
    parser.addErrorListener(errors)
    tree = parser.schema()
    if errors.errors:
        raise AppGenSyntaxError("; ".join(errors.errors))
    return tree


_FIELD_ARROW_REF_RE = re.compile(
    r"^(?P<prefix>\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*[A-Za-z_][A-Za-z0-9_]*(?:\([0-9]+\))?(?:\[\])?(?P<mods>(?:\s+(?!->)[^;\n]+?)?)?)\s*->\s*(?P<target>[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)(?P<cardinality>\s*\[[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)?\])?\s*(?P<suffix>;?\s*)$"
)
_EXTERNAL_ARROW_REF_RE = re.compile(
    r"^(?P<prefix>\s*)(?P<source>[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)\s*->\s*(?P<target>[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)(?P<cardinality>\s*\[[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)?\])?\s*(?P<suffix>;?\s*)$"
)
_DOTTED_APP_OPTION_RE = re.compile(r"(\brls\s*:\s*)([^;\n}]+)")
_DOTTED_VALUE_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*")
AUTHORING_ALIASES = {
    "entity": "table",
    "model": "table",
    "form": "view",
    "screen": "view",
    "workflow": "flow",
}
MODIFIER_ALIASES = {
    "hide": "hidden",
    "searchable": "search",
}
CORE_KEYWORDS = (
    "app",
    "table",
    "enum",
    "view",
    "for",
    "flow",
    "role",
    "rule",
    "pbc",
    "composition",
    "audit",
    "deploy",
    "version",
    "operation",
    "security",
    "api",
    "event",
    "job",
    "report",
    "menu",
    "component",
    "package",
    "test",
    "pk",
    "required",
    "unique",
    "hidden",
    "search",
    "default",
    "in",
    "llm",
    "agent",
)
KEYWORD_LIMIT = 32
PARSER_GOLDEN_REQUIRED_CONSTRUCTS = (
    "app",
    "app_option",
    "table",
    "field",
    "field_group",
    "spread",
    "derived_field",
    "field_modifier",
    "relation",
    "relation_cardinality",
    "table_directive",
    "enum",
    "view",
    "view_section",
    "component_placement",
    "handler",
    "flow",
    "flow_step",
    "flow_directive",
    "role",
    "permission",
    "rule",
    "rule_expression",
    "llm",
    "agent",
    "agentic_option",
    "contract_arrow",
    "pbc",
    "composition",
    "composition_include",
    "composition_require",
    "composition_expose",
    "composition_connect",
    "audit",
    "deploy",
    "deploy_unit",
    "deploy_scale",
    "deploy_health",
    "deploy_check",
    "deploy_resource",
    "deploy_binding",
    "deploy_directive",
    "version",
    "operation",
    "security",
    "api",
    "event",
    "job",
    "report",
    "menu",
    "component",
    "package",
    "test",
)
PARSER_GOLDEN_FIXTURES = (
    {
        "name": "enterprise_surface_valid.appgen",
        "valid": True,
        "constructs": PARSER_GOLDEN_REQUIRED_CONSTRUCTS,
        "source": """
app FinanceSuite { targets: web, mobile, desktop }

AddressFields {
  street: string
  city: string search
}

table Customer {
  id: int pk
  ... AddressFields
  name: string required unique search
  status: string default active
}

table Invoice {
  id: int pk
  customer_id: int -> Customer.id [many-to-one]
  subtotal: decimal default 0
  tax: decimal default 0
  total: decimal = subtotal + tax
  index(total)
}

Customer.id -> Invoice.customer_id [one-to-many]

enum InvoiceStatus { draft approved posted voided }

view InvoiceForm for Invoice {
  Main: customer.name, subtotal, tax, total
  @ customer.name Lookup 0 0 6 1
  on Save -> SubmitInvoice;
}

flow InvoiceApproval {
  draft -> reviewed;
  reviewed -> posted;
  human Review assigned Accountant -> reviewed;
  timer reviewed "P2D" -> escalated;
  compensate posted -> ReverseInvoice;
}

role Accountant {
  Invoice: read, write
  Customer: read
}

rule InvoicePolicy for Invoice {
  total required "Invoice total is required"
  total >= 0 and exists(customer.name) -> SubmitInvoice;
}

llm LocalModel {
  provider: ollama
  mode: local
  model: "qwen3.5-4b"
}

agent InvoiceAssistant {
  provider: LocalModel
  tools: read
  Invoice: read
  on Draft -> SubmitInvoice;
  recommend Invoice -> SubmitInvoice;
}

pbc Billing {
  owns: Invoice, Customer
  contract InvoiceApi -> InvoiceApproved;
  Invoice: read, write
}

composition EnterpriseSuite {
  include pbc gl_core version 1.0.0
  require database postgresql, mysql
  expose endpoint InvoiceApi
  connect Billing domain_event InvoiceApproved -> gl_core domain_event JournalPosted
}

audit FinancialAudit {
  retention: P7Y
  pii: masked
}

deploy Production {
  unit Billing as microservice
  scale Billing min 1 max 3
  health Billing "/health"
  check ready http "/ready"
  resource cpu request 500
  env DATABASE_URL APP_DATABASE_URL
  restart Billing rolling
}

version Release2026 {
  number: 1.0.0
  channel: stable
}

operation SubmitInvoice {
  draft -> posted;
  on Approve -> InvoiceApproved;
  emit InvoiceApproved -> JournalPosted;
}

security TenantSecurity {
  Invoice: read, write
  tenancy: org
}

api InvoiceApi {
  on Create -> SubmitInvoice;
  request Invoice -> InvoiceApproved;
  Invoice: read, write
}

event InvoiceApproved {
  payload Invoice -> JournalPosted;
  topic: finance.invoice.approved
}

job ReconcileInvoices {
  schedule daily -> SubmitInvoice;
  cron: "0 2 * * *"
}

report TrialBalance {
  source Invoice -> InvoiceApi;
  columns: subtotal, tax, total
}

menu MainMenu {
  on OpenInvoice -> SubmitInvoice;
  item invoices -> InvoiceForm;
}

component MoneyInput {
  on Change -> SubmitInvoice;
  bind total -> Invoice;
}

package DesktopRelease {
  target: desktop
  splash: FinanceSplash
  start_menu: MainMenu
}

test InvoiceHappyPath {
  case happy -> passed;
  expects: InvoiceApproved
}
""",
    },
    {
        "name": "compact_contracts_valid.appgen",
        "valid": True,
        "constructs": (
            "api",
            "event",
            "job",
            "report",
            "menu",
            "component",
            "package",
            "test",
            "handler",
            "contract_arrow",
            "agentic_option",
            "permission",
        ),
        "source": """
api CustomerApi { on Lookup -> CustomerFound; Customer: read }
event CustomerFound { topic: crm.customer.found }
job CustomerSync { run nightly -> CustomerFound }
report CustomerList { source CustomerApi -> CustomerFound }
menu CustomerMenu { item customers -> CustomerList }
component CustomerLookup { on Select -> CustomerFound }
package WebRelease { target: web }
test CustomerLookupWorks { case lookup -> passed }
""",
    },
    {
        "name": "invalid_unbalanced_block.appgen",
        "valid": False,
        "constructs": ("syntax_error",),
        "source": "app Broken { table Missing { id: int pk ",
    },
    {
        "name": "invalid_table_component_placement.appgen",
        "valid": False,
        "constructs": ("table_item_error",),
        "source": "table Bad { @ id Text 0 0 1 1 }",
    },
    {
        "name": "invalid_view_missing_close.appgen",
        "valid": False,
        "constructs": ("view_error",),
        "source": "view Bad for Invoice { Main: id",
    },
)
DIAGNOSTIC_RANGES = (
    ("AGX0000-AGX0099", "Syntax and parser errors."),
    ("AGX0100-AGX0199", "Naming, duplicates, reserved words, and style."),
    ("AGX0200-AGX0299", "Tables, fields, types, defaults, calculated fields, and directives."),
    ("AGX0300-AGX0399", "Relationships, foreign keys, lookup paths, and multi-hop traversal."),
    ("AGX0400-AGX0499", "Views, visual components, handlers, menus, and UI binding."),
    ("AGX0500-AGX0599", "Rules, expressions, required checks, and policy actions."),
    ("AGX0600-AGX0699", "Flows, workflow states, timers, human tasks, and compensation."),
    ("AGX0700-AGX0799", "Roles, permissions, security, tenancy, and secrets."),
    ("AGX0800-AGX0899", "APIs, events, jobs, reports, packages, deployment, audit, and versioning."),
    ("AGX0900-AGX0999", "PBC catalog, composition, cross-PBC contracts, and package manifests."),
    ("AGX1000-AGX1099", "LLMs, agents, skills, tools, and model/provider configuration."),
    ("AGX1100-AGX1199", "Migration planning and destructive-change detection."),
    ("AGX1200-AGX1299", "Natural-language change plans and agent safety."),
    ("AGX9000-AGX9999", "Internal tooling errors and unsupported parser states."),
)
DIAGNOSTIC_SPECS = (
    {"code": "AGX0001", "severity": "error", "title": "Source cannot be parsed", "trigger": "Source cannot be parsed.", "example_fix": "Show syntax location and nearest valid construct."},
    {"code": "AGX0101", "severity": "error", "title": "Duplicate declaration", "trigger": "Duplicate top-level declaration in the same namespace.", "example_fix": "Rename one symbol."},
    {"code": "AGX0201", "severity": "error", "title": "Unknown field type", "trigger": "Field references unknown type where no custom type is allowed.", "example_fix": "Create enum/table/type or choose known scalar."},
    {"code": "AGX0202", "severity": "error", "title": "Unknown calculated-field reference", "trigger": "Calculated field references unknown field.", "example_fix": "Create field or fix expression."},
    {"code": "AGX0301", "severity": "error", "title": "Unknown relationship table", "trigger": "Relationship target table does not exist.", "example_fix": "Create table or correct target."},
    {"code": "AGX0302", "severity": "error", "title": "Unknown relationship field", "trigger": "Relationship target field does not exist.", "example_fix": "Create field or correct target."},
    {"code": "AGX0303", "severity": "error", "title": "Unresolved lookup path", "trigger": "Lookup path cannot be resolved.", "example_fix": "Add relationship or change binding."},
    {"code": "AGX0304", "severity": "error", "title": "Broken multi-hop lookup chain", "trigger": "Multi-hop lookup chain breaks at an intermediate segment.", "example_fix": "Add missing relationship."},
    {"code": "AGX0401", "severity": "error", "title": "Unknown view table", "trigger": "View subject table does not exist.", "example_fix": "Create table or correct for target."},
    {"code": "AGX0402", "severity": "error", "title": "Invalid database-backed view binding", "trigger": "Database-backed view binding is not a field, calculated field, or lookup path.", "example_fix": "Replace binding or create valid field/path."},
    {"code": "AGX0403", "severity": "error", "title": "Unknown handler target", "trigger": "Handler target does not resolve.", "example_fix": "Create operation/flow/agent/contract target."},
    {"code": "AGX0404", "severity": "warning", "title": "Unknown visual component", "trigger": "Component is unknown to the registered component catalog.", "example_fix": "Use known component or register one."},
    {"code": "AGX0501", "severity": "error", "title": "Invalid rule equality operator", "trigger": "Rule expression uses single = instead of ==.", "example_fix": "Rewrite equality operator."},
    {"code": "AGX0502", "severity": "error", "title": "Unknown rule field", "trigger": "Rule references unknown field.", "example_fix": "Correct field or lookup path."},
    {"code": "AGX0601", "severity": "error", "title": "Invalid strict workflow state", "trigger": "Flow transition references undeclared or unreachable state where strict mode is enabled.", "example_fix": "Add transition or state directive."},
    {"code": "AGX0602", "severity": "warning", "title": "Unassigned human task", "trigger": "Human task has no assignee/participant.", "example_fix": "Add participant or assignment."},
    {"code": "AGX0701", "severity": "error", "title": "Unknown permission resource", "trigger": "Permission references unknown resource.", "example_fix": "Create resource or correct permission subject."},
    {"code": "AGX0702", "severity": "error", "title": "Secret literal in source", "trigger": "Secret literal appears in source.", "example_fix": "Replace with env/secret binding."},
    {"code": "AGX0801", "severity": "error", "title": "Invalid deployment or contract reference", "trigger": "Deployment unit target is unknown.", "example_fix": "Use supported unit kind."},
    {"code": "AGX0802", "severity": "error", "title": "Invalid package or target reference", "trigger": "Package target does not match app targets.", "example_fix": "Add app target or change package target."},
    {"code": "AGX0901", "severity": "error", "title": "Unknown PBC catalog entry", "trigger": "Composition includes unknown PBC key.", "example_fix": "Register PBC or correct key."},
    {"code": "AGX0902", "severity": "error", "title": "Unknown cross-PBC contract", "trigger": "Cross-PBC connection references unknown event/API/command.", "example_fix": "Declare contract or correct reference."},
    {"code": "AGX0903", "severity": "error", "title": "Private PBC table access", "trigger": "PBC attempts shared private-table access.", "example_fix": "Use API/event/projection contract."},
    {"code": "AGX1001", "severity": "error", "title": "Unknown agent reference", "trigger": "Agent skill target does not resolve.", "example_fix": "Create operation/flow/contract target."},
    {"code": "AGX1002", "severity": "error", "title": "Write-capable agent skill lacks permission", "trigger": "Agent has write-capable skill with no permission.", "example_fix": "Add permission or remove skill."},
    {"code": "AGX1101", "severity": "warning", "title": "Destructive migration", "trigger": "Migration plan contains destructive drop.", "example_fix": "Require explicit migration approval."},
    {"code": "AGX1201", "severity": "error", "title": "Unsupported natural-language plan", "trigger": "Natural-language plan cannot be represented as DSL diff.", "example_fix": "Ask for narrower DSL-scoped change."},
)
_DIAGNOSTIC_BASE_SOURCE = """
app DiagnosticDemo { targets: web }

table Customer {
  id: int pk
  name: string
}

table Invoice {
  id: int pk
  customer_id: int -> Customer.id
  total: decimal
}

view InvoiceForm for Invoice {
  Main: customer.name, total
}

operation SubmitInvoice {
  draft -> done
}
"""
DIAGNOSTIC_FIXTURES = (
    {"name": "agx0001_parse.appgen", "runner": "lint", "expected_codes": ("AGX0001",), "source": "app Broken { table Missing { id: int pk "},
    {"name": "agx0101_duplicate.appgen", "runner": "lint", "expected_codes": ("AGX0101",), "source": "app D { targets: web } table Customer { id: int pk } table Customer { id: int pk }"},
    {"name": "agx0201_unknown_type.appgen", "runner": "lint", "expected_codes": ("AGX0201",), "source": "app D { targets: web } table Customer { id: int pk; name: galaxy }"},
    {"name": "agx0202_calculated.appgen", "runner": "lint", "expected_codes": ("AGX0202",), "source": "app D { targets: web } table Invoice { id: int pk; total: decimal = subtotal + tax }"},
    {"name": "agx0301_relation_table.appgen", "runner": "lint", "expected_codes": ("AGX0301",), "source": "app D { targets: web } table Invoice { id: int pk; customer_id: int -> Missing.id }"},
    {"name": "agx0302_relation_field.appgen", "runner": "lint", "expected_codes": ("AGX0302",), "source": "app D { targets: web } table Customer { id: int pk } table Invoice { id: int pk; customer_id: int -> Customer.missing }"},
    {"name": "agx0303_lookup.appgen", "runner": "lint", "expected_codes": ("AGX0303",), "source": "app D { targets: web } table Customer { id: int pk; name: string } table Invoice { id: int pk; customer_id: int -> Customer.id } view InvoiceForm for Invoice { Main: customer.missing }"},
    {"name": "agx0304_multihop.appgen", "runner": "lint", "expected_codes": ("AGX0304",), "source": "app D { targets: web } table City { id: int pk; name: string } table Customer { id: int pk; city_id: int } table Invoice { id: int pk; customer_id: int -> Customer.id } view InvoiceForm for Invoice { Main: customer.city.name }"},
    {"name": "agx0401_view_table.appgen", "runner": "lint", "expected_codes": ("AGX0401",), "source": "app D { targets: web } table Customer { id: int pk } view MissingForm for Missing { Main: id }"},
    {"name": "agx0402_view_binding.appgen", "runner": "lint", "expected_codes": ("AGX0402",), "source": "app D { targets: web } table Customer { id: int pk } view CustomerForm for Customer { Main: missing }"},
    {"name": "agx0403_handler.appgen", "runner": "lint", "expected_codes": ("AGX0403",), "source": "app D { targets: web } table Customer { id: int pk } view CustomerForm for Customer { Main: id; on Save -> MissingOperation }"},
    {"name": "agx0404_component.appgen", "runner": "lint", "expected_codes": ("AGX0404",), "source": "app D { targets: web } table Customer { id: int pk; name: string } view CustomerForm for Customer { Main: name; @ name UnknownWidget 0 0 4 1 }"},
    {"name": "agx0501_rule_operator.appgen", "runner": "lint", "expected_codes": ("AGX0501",), "source": "app D { targets: web } table Customer { id: int pk; status: string } rule CustomerPolicy for Customer { status = active }"},
    {"name": "agx0502_rule_field.appgen", "runner": "lint", "expected_codes": ("AGX0502",), "source": "app D { targets: web } table Customer { id: int pk; status: string } rule CustomerPolicy for Customer { missing == active }"},
    {"name": "agx0601_flow_strict.appgen", "runner": "lint", "expected_codes": ("AGX0601",), "source": "app D { targets: web } table Customer { id: int pk } flow Review { draft -> approved; strict on; timer missing \"P1D\" -> escalated }"},
    {"name": "agx0602_human_task.appgen", "runner": "lint", "expected_codes": ("AGX0602",), "source": "app D { targets: web } table Customer { id: int pk } flow Review { draft -> approved; human Review -> approved }"},
    {"name": "agx0701_permission.appgen", "runner": "lint", "expected_codes": ("AGX0701",), "source": "app D { targets: web } table Customer { id: int pk } role Clerk { Missing: read }"},
    {"name": "agx0702_secret.appgen", "runner": "lint", "expected_codes": ("AGX0702",), "source": "app D { targets: web } table Customer { id: int pk } llm ApiModel { provider: openai; api_key: \"sk-secret\" }"},
    {"name": "agx0801_deploy.appgen", "runner": "lint", "expected_codes": ("AGX0801",), "source": "app D { targets: web } table Customer { id: int pk } deploy Production { unit Missing as microservice }"},
    {"name": "agx0802_package.appgen", "runner": "lint", "expected_codes": ("AGX0802",), "source": "app D { targets: web } table Customer { id: int pk } package MobileRelease { target: satellite }"},
    {"name": "agx0901_pbc.appgen", "runner": "lint", "expected_codes": ("AGX0901",), "source": "app D { targets: web } table Customer { id: int pk } composition Suite { include pbc missing_pbc version 1.0.0 }"},
    {"name": "agx0902_pbc_contract.appgen", "runner": "lint", "expected_codes": ("AGX0902",), "source": "app D { targets: web } table Customer { id: int pk } composition Suite { include pbc gl_core version 1.0.0; include pbc ap_automation version 1.0.0; connect ap_automation domain_event MissingEvent -> gl_core domain_event MissingCommand }"},
    {"name": "agx0903_pbc_table.appgen", "runner": "lint", "expected_codes": ("AGX0903",), "source": "app D { targets: web } table Customer { id: int pk } composition Suite { include pbc gl_core version 1.0.0; include pbc ap_automation version 1.0.0; connect ap_automation private_table invoice -> gl_core private_table journal_entry }"},
    {"name": "agx1001_agent_target.appgen", "runner": "lint", "expected_codes": ("AGX1001",), "source": "app D { targets: web } table Customer { id: int pk } llm LocalModel { provider: ollama; mode: local } agent Assistant { provider: LocalModel; on Run -> MissingOperation }"},
    {"name": "agx1002_agent_permission.appgen", "runner": "lint", "expected_codes": ("AGX1002",), "source": "app D { targets: web } table Customer { id: int pk } llm LocalModel { provider: ollama; mode: local } agent Assistant { provider: LocalModel; tools: write }"},
    {"name": "agx1101_migration.appgen", "runner": "migration", "expected_codes": ("AGX1101",), "previous_source": _DIAGNOSTIC_BASE_SOURCE, "source": "app DiagnosticDemo { targets: web }\n\ntable Customer { id: int pk; name: string }\n"},
    {"name": "agx1201_nl.appgen", "runner": "nl-plan", "expected_codes": ("AGX1201",), "prompt": "Replace the runtime with hand-written generated code outside the DSL", "source": _DIAGNOSTIC_BASE_SOURCE},
)
LEGACY_CONTEXTUAL_TOKENS = ("ref", "include", "require", "expose", "connect")
KEYWORD_FREE_SYNTAX = (
    "-> references",
    "[cardinality] relation metadata",
    "... field groups",
    "type[] arrays",
    "= derived fields",
    "@ component placements",
    "on Event -> Handler wiring",
    "generic app options",
    "PBC composition, audit, deployment, versioning, operations, and security blocks",
    "API, event, job, report, menu, component, package, and test contract blocks",
    "deployment unit/scale/health/check topology inside deploy blocks",
    "entity/model/form/screen/workflow authoring aliases",
    "hide/searchable modifier aliases",
)
_DEPLOYMENT_PATTERNS = (
    "embedded",
    "function",
    "job",
    "microservice",
    "module",
    "monolith",
    "process",
    "sidecar",
    "worker",
)
LEARNING_PATH = (
    {"step": 1, "goal": "Model data", "constructs": ("app", "table", "enum", "->")},
    {"step": 2, "goal": "Shape screens", "constructs": ("view", "hidden", "search", "@")},
    {"step": 3, "goal": "Add behavior", "constructs": ("flow", "role", "rule")},
    {"step": 4, "goal": "Add intelligence", "constructs": ("llm", "agent")},
)
DSL_ERGONOMICS_SAMPLE = """app Ergonomic {
  targets: web, mobile, desktop
}

table Author {
  id: int pk
  name: string required search
}

table Book {
  id: int pk
  title: string required search
  author_id: int -> Author.id [many-to-one]
}

view BookForm for Book {
  Main: title, author_id
  @ title TextBox 0 0 6 1
}

flow Publish {
  draft -> published
}

llm LocalModel {
  provider: ollama
  mode: local
  model: llama3
}

agent Reviewer {
  provider: LocalModel
  goal: "Review books"
  tools: schema, forms
}
"""
_AUTHORING_ALIAS_RE = re.compile(
    r"(?P<prefix>^[ \t]*|\}[ \t]*)(?P<alias>entity|model|form|screen|workflow)\b(?=\s+[A-Za-z_][A-Za-z0-9_]*(?:\s+for\s+[A-Za-z_][A-Za-z0-9_]*)?\s*\{)",
    flags=re.IGNORECASE | re.MULTILINE,
)
_FIELD_MODIFIER_ALIAS_RE = re.compile(
    r"(?P<prefix>(?:^|[{\n;])\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*[A-Za-z_][A-Za-z0-9_]*(?:\([0-9]+\))?(?:\[\])?(?:\s+(?:pk|required|unique|hidden|search|default\s+[^;{}\n]+|in\s+[^;{}\n]+|->\s*[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*(?:\s*\[[^\]]+\])?))*\s+)(?P<alias>hide|searchable)\b",
    flags=re.IGNORECASE,
)
_TABLE_FIELD_BEFORE_DIRECTIVE_RE = re.compile(
    r"(?m)^(\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*[^;\n{}]+)\n(?=\s*(?:unique|index|lookup|fk|foreign_key|check|constraint)\b)"
)


def dsl_keyword_budget() -> dict:
    """Return the canonical keyword-budget contract for the AppGen DSL."""
    return {
        "format": "appgen.dsl-keyword-budget.v1",
        "limit": KEYWORD_LIMIT,
        "count": len(CORE_KEYWORDS),
        "canonical_keyword_count": len(CORE_KEYWORDS),
        "ok": len(CORE_KEYWORDS) <= KEYWORD_LIMIT,
        "keywords": CORE_KEYWORDS,
        "legacy_contextual_tokens": LEGACY_CONTEXTUAL_TOKENS,
        "legacy_policy": "accepted_for_existing_sources_but_linted_to_arrow_syntax",
        "keyword_free_syntax": KEYWORD_FREE_SYNTAX,
        "authoring_aliases": dict(AUTHORING_ALIASES),
        "modifier_aliases": dict(MODIFIER_ALIASES),
    }


def dsl_antlr_integrity_report() -> dict:
    """Return drift evidence between the canonical grammar and generated parser."""
    grammar_path = Path(__file__).resolve().parents[2] / "lang" / "appgen.g4"
    parser_path = _GENERATED_DIR / "appgenParser.py"
    lexer_path = _GENERATED_DIR / "appgenLexer.py"
    grammar_text = grammar_path.read_text() if grammar_path.exists() else ""
    grammar_tokens = tuple(re.findall(r"^([A-Z_]+)\s*:", grammar_text, flags=re.MULTILINE))
    grammar_rules = tuple(
        re.findall(r"^([a-z][A-Za-z0-9_]*)\s*(?:\n\s*)?:", grammar_text, flags=re.MULTILINE)
    )
    grammar_literals = {
        token: literal
        for token, literal in re.findall(
            r"^([A-Z_]+)\s*:\s*'([^']+)'", grammar_text, flags=re.MULTILINE
        )
    }
    parser_symbols = tuple(name for name in appgenParser.symbolicNames if name != "<INVALID>")
    lexer_symbols = tuple(name for name in appgenLexer.symbolicNames if name != "<INVALID>")
    parser_literals = {
        symbol: appgenParser.literalNames[index].strip("'")
        for index, symbol in enumerate(appgenParser.symbolicNames)
        if symbol != "<INVALID>"
        and index < len(appgenParser.literalNames)
        and appgenParser.literalNames[index].startswith("'")
    }
    grammar_token_set = set(grammar_tokens)
    parser_symbol_set = set(parser_symbols)
    lexer_symbol_set = set(lexer_symbols)
    grammar_rule_set = set(grammar_rules)
    parser_rule_set = set(appgenParser.ruleNames)
    canonical_keyword_tokens = tuple(
        token for token, literal in grammar_literals.items() if literal in CORE_KEYWORDS
    )
    keyword_literal_mismatches = tuple(
        {
            "token": token,
            "grammar": literal,
            "parser": parser_literals.get(token),
        }
        for token, literal in grammar_literals.items()
        if literal in CORE_KEYWORDS and parser_literals.get(token) != literal
    )
    required_rules = (
        "schema",
        "tableDecl",
        "tableDirective",
        "viewDecl",
        "componentPlacement",
        "flowDecl",
        "flowItem",
        "flowDirective",
        "llmDecl",
        "agentDecl",
        "agentItem",
        "pbcDecl",
        "pbcItem",
        "compositionDecl",
        "auditDecl",
        "deploymentDecl",
        "deploymentItem",
        "deployUnit",
        "deployScale",
        "deployHealth",
        "deployCheck",
        "deployResource",
        "deployBinding",
        "deployDirective",
        "versionDecl",
        "operationDecl",
        "securityDecl",
        "apiDecl",
        "eventDecl",
        "jobDecl",
        "reportDecl",
        "menuDecl",
        "componentDecl",
        "packageDecl",
        "testDecl",
        "contractItem",
        "contractDirective",
        "handlerDecl",
    )
    missing_required_rules = tuple(rule for rule in required_rules if rule not in parser_rule_set)
    missing_parser_tokens = tuple(token for token in grammar_tokens if token not in parser_symbol_set)
    missing_lexer_tokens = tuple(token for token in grammar_tokens if token not in lexer_symbol_set)
    missing_parser_rules = tuple(rule for rule in grammar_rules if rule not in parser_rule_set)
    extra_parser_tokens = tuple(
        token
        for token in parser_symbols
        if token not in grammar_token_set and token not in {"EOF"}
    )
    extra_parser_rules = tuple(rule for rule in appgenParser.ruleNames if rule not in grammar_rule_set)
    ok = (
        grammar_path.exists()
        and parser_path.exists()
        and lexer_path.exists()
        and not missing_parser_tokens
        and not missing_lexer_tokens
        and not missing_parser_rules
        and not extra_parser_tokens
        and not extra_parser_rules
        and not keyword_literal_mismatches
        and not missing_required_rules
        and len(canonical_keyword_tokens) == len(CORE_KEYWORDS)
    )
    return {
        "format": "appgen.dsl-antlr-integrity.v1",
        "ok": ok,
        "grammar": "lang/appgen.g4",
        "parser": "src/pyAppGen/dsl_generated/lang/appgenParser.py",
        "lexer": "src/pyAppGen/dsl_generated/lang/appgenLexer.py",
        "grammar_token_count": len(grammar_tokens),
        "parser_token_count": len(parser_symbols),
        "lexer_token_count": len(lexer_symbols),
        "grammar_rule_count": len(grammar_rules),
        "parser_rule_count": len(appgenParser.ruleNames),
        "canonical_keyword_tokens": canonical_keyword_tokens,
        "missing_parser_tokens": missing_parser_tokens,
        "missing_lexer_tokens": missing_lexer_tokens,
        "missing_parser_rules": missing_parser_rules,
        "missing_required_rules": missing_required_rules,
        "extra_parser_tokens": extra_parser_tokens,
        "extra_parser_rules": extra_parser_rules,
        "keyword_literal_mismatches": keyword_literal_mismatches,
        "legacy_contextual_tokens": LEGACY_CONTEXTUAL_TOKENS,
    }


def dsl_language_quality_contract() -> dict:
    """Return learnability, ANTLR, and keyword-budget evidence for the DSL."""
    budget = dsl_keyword_budget()
    antlr = dsl_antlr_integrity_report()
    checks = (
        {"check": "antlr_grammar", "ok": (Path(__file__).resolve().parents[2] / "lang" / "appgen.g4").exists()},
        {"check": "generated_antlr_parser", "ok": (_GENERATED_DIR / "appgenParser.py").exists()},
        {"check": "antlr_grammar_parser_sync", "ok": antlr["ok"], "evidence": antlr},
        {"check": "keyword_budget", "ok": budget["ok"], "value": budget["count"]},
        {"check": "authoring_aliases_without_new_keywords", "ok": set(AUTHORING_ALIASES.values()) <= set(CORE_KEYWORDS)},
        {"check": "modifier_aliases_without_new_keywords", "ok": set(MODIFIER_ALIASES.values()) <= set(CORE_KEYWORDS)},
        {"check": "keyword_free_relationships", "ok": "-> references" in KEYWORD_FREE_SYNTAX},
        {"check": "legacy_ref_not_canonical", "ok": "ref" not in CORE_KEYWORDS and "ref" in LEGACY_CONTEXTUAL_TOKENS},
        {"check": "progressive_learning_path", "ok": len(LEARNING_PATH) == 4},
    )
    return {
        "format": "appgen.dsl-language-quality.v1",
        "ok": all(item["ok"] for item in checks),
        "grammar": "lang/appgen.g4",
        "parser": "src/pyAppGen/dsl_generated/lang/appgenParser.py",
        "antlr_integrity": antlr,
        "budget": budget,
        "keywords": CORE_KEYWORDS,
        "canonical_keyword_count": len(CORE_KEYWORDS),
        "legacy_contextual_tokens": LEGACY_CONTEXTUAL_TOKENS,
        "keyword_policy": {
            "canonical": "Only CORE_KEYWORDS count against the compact DSL budget.",
            "legacy": "Legacy contextual tokens remain parse-compatible and receive linter quick fixes.",
        },
        "learning_path": LEARNING_PATH,
        "checks": checks,
    }


def _uses_authoring_aliases(source: str) -> bool:
    return bool(_AUTHORING_ALIAS_RE.search(source))


def _normalize_authoring_aliases(source: str) -> str:
    """Normalize beginner-friendly aliases before ANTLR parsing without adding keywords."""

    def repl(match: re.Match[str]) -> str:
        alias = match.group("alias")
        canonical = AUTHORING_ALIASES[alias.lower()]
        return f"{match.group('prefix')}{canonical}"

    return _AUTHORING_ALIAS_RE.sub(repl, source)


def _uses_modifier_aliases(source: str) -> bool:
    return bool(_FIELD_MODIFIER_ALIAS_RE.search(source or ""))


def _normalize_modifier_aliases(source: str) -> str:
    """Normalize field modifier aliases before ANTLR parsing without adding keywords."""

    def repl(match: re.Match[str]) -> str:
        alias = match.group("alias")
        canonical = MODIFIER_ALIASES[alias.lower()]
        return f"{match.group('prefix')}{canonical}"

    previous = source or ""
    while True:
        current = _FIELD_MODIFIER_ALIAS_RE.sub(repl, previous)
        if current == previous:
            return current
        previous = current


def _normalize_reference_sugar(source: str) -> str:
    """Normalize arrow reference sugar to the generated parser's legacy form."""
    normalized_lines = []
    for line in source.splitlines():
        field_match = _FIELD_ARROW_REF_RE.match(line)
        if field_match:
            normalized_lines.append(
                f"{field_match.group('prefix')} ref {field_match.group('target')}{field_match.group('cardinality') or ''}{field_match.group('suffix')}"
            )
            continue
        external_match = _EXTERNAL_ARROW_REF_RE.match(line)
        if external_match:
            normalized_lines.append(
                f"{external_match.group('prefix')}ref {external_match.group('source')} -> {external_match.group('target')}{external_match.group('cardinality') or ''}{external_match.group('suffix')}"
            )
            continue
        normalized_lines.append(line)
    return "\n".join(normalized_lines)


def _normalize_table_line_boundaries(source: str) -> str:
    """Prevent table directives from being consumed as field modifiers."""
    return _TABLE_FIELD_BEFORE_DIRECTIVE_RE.sub(r"\1;\n", source or "")


def _normalize_app_option_sugar(source: str) -> str:
    """Allow dotted app option values without reserving more grammar keywords."""

    def repl(match: re.Match[str]) -> str:
        prefix, raw_values = match.groups()
        values = []
        for value in raw_values.split(","):
            stripped = value.strip()
            if _DOTTED_VALUE_RE.fullmatch(stripped):
                values.append(f'"{stripped}"')
            else:
                values.append(stripped)
        return prefix + ", ".join(values)

    return _DOTTED_APP_OPTION_RE.sub(repl, source)


def _app_name(ctx) -> str | None:
    if ctx is None:
        return None
    ident = ctx.IDENT()
    if ident:
        return ident.getText()
    string = ctx.STRING()
    if string:
        return _literal_text(string.getText())
    return None


def _app_options(ctx) -> dict[str, str]:
    if ctx is None or ctx.appBlock() is None:
        return {}
    options = {}
    for option in ctx.appBlock().appOption():
        values = tuple(_literal(literal) for literal in option.literal())
        options[option.IDENT().getText()] = values[0] if len(values) == 1 else ",".join(values)
    return options


def _validate_app_options(app_options: dict[str, str]) -> None:
    if "targets" not in app_options:
        return
    targets, unknown = normalize_platform_targets(app_options["targets"])
    if unknown:
        known = ", ".join(normalize_platform_targets(None)[0])
        bad = ", ".join(unknown)
        raise AppGenSyntaxError(f"Unknown app targets: {bad}. Supported targets: {known}")
    if not targets:
        known = ", ".join(normalize_platform_targets(None)[0])
        raise AppGenSyntaxError(f"App targets cannot be empty. Supported targets: {known}")


def _validate_schema(schema: AppSchema) -> None:
    table_map = {table.name: table for table in schema.tables}
    field_map = {table.name: _field_names(table) for table in schema.tables}
    enum_names = {enum.name for enum in schema.enums}
    errors: list[str] = []

    errors.extend(_duplicate_name_errors("table", (table.name for table in schema.tables)))
    errors.extend(_duplicate_name_errors("enum", (enum.name for enum in schema.enums)))
    errors.extend(_duplicate_name_errors("view", (view.name for view in schema.views)))
    errors.extend(_duplicate_name_errors("flow", (flow.name for flow in schema.flows)))
    errors.extend(_duplicate_name_errors("role", (role.name for role in schema.roles)))
    errors.extend(_duplicate_name_errors("rule", (rule.name for rule in schema.rules)))
    errors.extend(
        _duplicate_name_errors("llm provider", (provider.name for provider in schema.llm_providers))
    )
    errors.extend(_duplicate_name_errors("agent", (agent.name for agent in schema.agents)))
    for kind, contracts in _enterprise_contract_groups(schema).items():
        errors.extend(_duplicate_name_errors(kind, (contract.name for contract in contracts)))

    for relation in schema.relations:
        if relation.source_table not in table_map:
            errors.append(f"Unknown relation source table: {relation.source_table}")
            continue
        if relation.source_column not in field_map[relation.source_table]:
            errors.append(
                f"Unknown relation source field: {relation.source_table}.{relation.source_column}"
            )
        if relation.target_table not in table_map:
            errors.append(f"Unknown relation target table: {relation.target_table}")
            continue
        if relation.target_column not in field_map[relation.target_table]:
            errors.append(
                f"Unknown relation target field: {relation.target_table}.{relation.target_column}"
            )

    for table in schema.tables:
        for column in table.columns:
            if not _known_field_type(column.type_name, table_map, enum_names):
                errors.append(f"Unknown field type: {table.name}.{column.name} uses {column.type_name}")
            if column.references:
                target_table, target_column = column.references
                if target_table not in table_map:
                    errors.append(f"Unknown reference target table: {target_table}")
                elif target_column not in field_map[target_table]:
                    errors.append(f"Unknown reference target field: {target_table}.{target_column}")
            if column.derived and column.expression:
                unknown = _unknown_expression_fields(column.expression, field_map[table.name])
                for field_name in unknown:
                    errors.append(
                        f"Unknown derived-field reference: {table.name}.{column.name} uses {field_name}"
                    )
        errors.extend(_table_directive_errors(table, table_map, field_map))

    for view in schema.views:
        if view.table not in table_map:
            errors.append(f"Unknown view table: {view.name} for {view.table}")
            continue
        allowed = field_map[view.table]
        for field_name in view.fields:
            if field_name not in allowed and not _valid_lookup_path(view.table, field_name, table_map, field_map):
                if _lookup_breaks_mid_chain(view.table, field_name, table_map, field_map):
                    errors.append(f"Multi-hop lookup chain breaks: {view.name}.{field_name}")
                elif _lookup_starts_with_relationship(view.table, field_name, table_map):
                    errors.append(f"Unresolved lookup path: {view.name}.{field_name}")
                else:
                    errors.append(f"Unknown view field: {view.name}.{field_name}")
        for component in view.components:
            if component.field and component.field not in allowed and not _valid_lookup_path(
                view.table, component.field, table_map, field_map
            ):
                if _lookup_breaks_mid_chain(view.table, component.field, table_map, field_map):
                    errors.append(f"Multi-hop lookup chain breaks: {view.name}.{component.field}")
                elif _lookup_starts_with_relationship(view.table, component.field, table_map):
                    errors.append(f"Unresolved lookup path: {view.name}.{component.field}")
                else:
                    errors.append(f"Unknown component field: {view.name}.{component.field}")

    for role in schema.roles:
        for permission in role.permissions:
            if permission.resource not in table_map:
                errors.append(f"Unknown role resource: {role.name}.{permission.resource}")

    for rule in schema.rules:
        if rule.table not in table_map:
            errors.append(f"Unknown rule table: {rule.name} for {rule.table}")
            continue
        allowed = field_map[rule.table]
        for condition in rule.conditions:
            if condition.field not in allowed:
                errors.append(f"Unknown rule field: {rule.name}.{condition.field}")

    provider_names = {provider.name for provider in schema.llm_providers}
    if provider_names:
        for agent in schema.agents:
            if agent.provider and agent.provider not in provider_names:
                errors.append(f"Unknown agent provider: {agent.name}.{agent.provider}")

    operation_names = {flow.name for flow in schema.flows}
    operation_names.update(block.name for block in schema.platform_blocks if block.kind == "operation")
    handler_targets = set(operation_names)
    handler_targets.update(agent.name for agent in schema.agents)
    handler_targets.update(contract.name for contract in _enterprise_contracts(schema))
    deployable_targets = set(handler_targets)
    deployable_targets.update(block.name for block in schema.platform_blocks if block.kind == "pbc")
    for view in schema.views:
        for handler in view.handlers:
            if handler.target not in handler_targets:
                errors.append(f"Unknown handler target: {view.name}.{handler.target}")
    for block in schema.platform_blocks:
        if block.kind != "deploy":
            continue
        for unit in block.deployment_units:
            if unit.target not in deployable_targets:
                errors.append(f"Unknown deployment unit target: {block.name}.{unit.target}")
            if unit.pattern not in _DEPLOYMENT_PATTERNS:
                patterns = ", ".join(sorted(_DEPLOYMENT_PATTERNS))
                errors.append(f"Unknown deployment pattern: {block.name}.{unit.pattern}. Supported: {patterns}")
        for scale in block.deployment_scales:
            if scale.target not in deployable_targets:
                errors.append(f"Unknown deployment scale target: {block.name}.{scale.target}")
            if scale.minimum > scale.maximum:
                errors.append(f"Invalid deployment scale range: {block.name}.{scale.target}")
        for health in block.deployment_health:
            if health.target not in deployable_targets:
                errors.append(f"Unknown deployment health target: {block.name}.{health.target}")
        for statement in block.statements:
            if statement.target and statement.target not in deployable_targets:
                errors.append(f"Unknown deployment directive target: {block.name}.{statement.target}")
    for contract in _enterprise_contracts(schema):
        for handler in contract.handlers:
            if handler.target not in handler_targets:
                errors.append(f"Unknown handler target: {contract.name}.{handler.target}")
        for statement in contract.statements:
            if statement.target and statement.target not in handler_targets:
                errors.append(f"Unknown contract target: {contract.name}.{statement.target}")
        if contract.kind == "package":
            package_targets = contract.options.get("target", ()) or contract.options.get("targets", ())
            if package_targets:
                _targets, unknown = normalize_platform_targets(package_targets)
                for target in unknown:
                    errors.append(f"Unknown package target: {contract.name}.{target}")

    for table_name, field_name in _explicit_rls_targets(schema.app_options):
        if table_name not in table_map:
            errors.append(f"Unknown RLS target table: {table_name}")
            continue
        if field_name not in field_map[table_name]:
            errors.append(f"Unknown RLS target field: {table_name}.{field_name}")

    if errors:
        raise AppGenSyntaxError("; ".join(errors))


def _explicit_rls_targets(app_options: dict[str, str]) -> tuple[tuple[str, str], ...]:
    raw_targets = app_options.get("rls")
    if not raw_targets:
        return ()
    targets: list[tuple[str, str]] = []
    for raw_target in raw_targets.split(","):
        target = raw_target.strip()
        if not target:
            continue
        if not _DOTTED_VALUE_RE.fullmatch(target):
            raise AppGenSyntaxError(
                f"Invalid RLS target: {target}. Use Table.field, for example Project.tenant_id"
            )
        table_name, field_name = target.split(".", 1)
        targets.append((table_name, field_name))
    return tuple(targets)


def _preparse_tooling_errors(source: str) -> tuple[str, ...]:
    errors: list[str] = []
    for block in re.finditer(r"\brule\s+[A-Za-z_][A-Za-z0-9_]*\s+for\s+[A-Za-z_][A-Za-z0-9_]*\s*\{(?P<body>.*?)\}", source, re.S):
        body = block.group("body")
        if re.search(r"(?<![!<>=])=(?!=)", body):
            errors.append("Rule expression uses single = instead of ==.")
    return tuple(errors)


def _tooling_policy_diagnostics(schema: AppSchema) -> tuple[tuple[str, ...], tuple[str, ...]]:
    table_map = {table.name: table for table in schema.tables}
    field_map = {table.name: _field_names(table) for table in schema.tables}
    handler_targets = _handler_target_names(schema)
    pbc_catalog = _pbc_catalog_by_key()
    errors: list[str] = []
    warnings: list[str] = []

    for view in schema.views:
        for component in view.components:
            if component.component not in _known_component_names(schema):
                warnings.append(f"Unknown visual component: {view.name}.{component.component}")
            if component.x < 0 or component.y < 0 or component.w <= 0 or component.h <= 0:
                errors.append(f"Invalid component placement: {view.name}.{component.field}")

    for flow in schema.flows:
        states = {state for step in flow.steps for state in (step.source, step.target)}
        strict = any(
            directive.verb == "strict" and any(value.lower() in {"on", "true", "yes"} for value in directive.values)
            for directive in flow.directives
        )
        for directive in flow.directives:
            if directive.verb == "human" and "assigned" not in directive.values:
                warnings.append(f"Human task has no assignee: {flow.name}.{_first_or_none(directive.values) or 'task'}")
            if strict and directive.verb in {"timer", "compensate"}:
                state = _first_or_none(directive.values)
                if state and state not in states:
                    errors.append(f"Flow strict state is undeclared: {flow.name}.{state}")
                if directive.target and directive.target not in states:
                    errors.append(f"Flow strict state is undeclared: {flow.name}.{directive.target}")

    for block in schema.platform_blocks:
        if block.kind != "composition":
            continue
        included = {_composition_include_key(include) for include in block.options.get("include", ())}
        for key in tuple(included):
            if key and key not in pbc_catalog:
                errors.append(f"Unknown PBC catalog entry: {block.name}.{key}")
        for raw_connection in block.options.get("connect", ()):
            connection = _semantic_composition_connection(raw_connection)
            for side in ("from", "to"):
                key = connection.get(f"{side}_pbc")
                if key and key not in pbc_catalog:
                    errors.append(f"Unknown PBC catalog entry: {block.name}.{key}")
            if str(connection.get("from_kind") or "").endswith("table") or str(connection.get("to_kind") or "").endswith("table"):
                errors.append(f"Private PBC table access: {block.name}.{raw_connection}")
                continue
            if not _pbc_connection_contract_resolves(connection, pbc_catalog):
                errors.append(f"Unknown cross-PBC contract: {block.name}.{raw_connection}")

    for agent in schema.agents:
        for handler in agent.handlers:
            if handler.target not in handler_targets:
                errors.append(f"Unknown agent skill target: {agent.name}.{handler.target}")
        for skill in agent.competencies:
            if skill.target and skill.target not in handler_targets:
                errors.append(f"Unknown agent skill target: {agent.name}.{skill.target}")
            if skill.verb.lower() in {"write", "create", "update", "delete", "mutate", "post"} and not agent.permissions:
                errors.append(f"Agent write-capable skill has no permission: {agent.name}.{skill.verb}")
        if any(tool.lower() in {"write", "create", "update", "delete", "mutate"} for tool in agent.tools) and not agent.permissions:
            errors.append(f"Agent write-capable skill has no permission: {agent.name}.tools")

    return tuple(errors), tuple(warnings)


def _known_field_type(type_name: str, table_map: dict[str, TableSchema], enum_names: set[str]) -> bool:
    base = re.sub(r"\(.*\)$", "", type_name or "").removesuffix("[]")
    known = {
        "bool",
        "boolean",
        "date",
        "datetime",
        "decimal",
        "email",
        "file",
        "float",
        "image",
        "int",
        "integer",
        "json",
        "jsonb",
        "money",
        "number",
        "string",
        "text",
        "time",
        "uuid",
    }
    return base in known or base in table_map or base in enum_names


def _lookup_breaks_mid_chain(
    table_name: str,
    path: str,
    table_map: dict[str, TableSchema],
    field_map: dict[str, set[str]],
) -> bool:
    parts = path.split(".")
    if len(parts) < 3 or table_name not in table_map:
        return False
    current_table = table_name
    for index, part in enumerate(parts[:-1]):
        if part not in field_map.get(current_table, set()):
            return index > 0
        reference = _reference_for_lookup_part(table_map[current_table], part)
        if reference is None:
            return True
        current_table = reference[0]
    return False


def _lookup_starts_with_relationship(
    table_name: str,
    path: str,
    table_map: dict[str, TableSchema],
) -> bool:
    first, dot, _rest = path.partition(".")
    if not dot or table_name not in table_map:
        return False
    return _reference_for_lookup_part(table_map[table_name], first) is not None


def _known_component_names(schema: AppSchema) -> set[str]:
    names = {
        "Button",
        "Checkbox",
        "DatePicker",
        "EmailInput",
        "FileUpload",
        "Grid",
        "GroupBox",
        "Label",
        "ListBox",
        "Lookup",
        "NumberInput",
        "Panel",
        "RadioButton",
        "RadioGroup",
        "Select",
        "TextArea",
        "TextBox",
        "TreeView",
    }
    names.update(contract.name for contract in schema.component_contracts)
    return names


def _handler_target_names(schema: AppSchema) -> set[str]:
    targets = {flow.name for flow in schema.flows}
    targets.update(agent.name for agent in schema.agents)
    targets.update(block.name for block in schema.platform_blocks if block.kind == "operation")
    targets.update(contract.name for contract in _enterprise_contracts(schema))
    return targets


def _pbc_connection_contract_resolves(connection: dict, catalog: dict[str, dict]) -> bool:
    for side in ("from", "to"):
        key = connection.get(f"{side}_pbc")
        kind = connection.get(f"{side}_kind")
        contract = connection.get(f"{side}_contract")
        if not key or key not in catalog or not kind or not contract:
            return False
        pbc = catalog[key]
        if kind in {"event", "emits", "consumes"} and contract not in set(pbc.get("emits", ())) | set(pbc.get("consumes", ())):
            return False
        if kind in {"api", "command"}:
            api_names = set(pbc.get("apis", ()))
            api_tokens = {token for api in api_names for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", api)}
            if contract not in api_names and contract not in api_tokens:
                return False
        if kind not in {"api", "command", "event", "emits", "consumes"}:
            return False
    return True


def _duplicate_name_errors(kind: str, names: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for name in names:
        if name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    return [f"Duplicate {kind} declaration: {name}" for name in duplicates]


def _field_names(table: TableSchema) -> set[str]:
    names = {column.name for column in table.columns}
    for column in table.columns:
        if column.references and column.name.endswith("_id"):
            names.add(column.name[:-3])
    return names


def _table_directive_errors(
    table: TableSchema,
    table_map: dict[str, TableSchema],
    field_map: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    field_directives = {"index", "unique", "key", "lookup", "fk", "foreign_key"}
    for directive in table.directives:
        verb = directive.verb.lower()
        if verb not in field_directives:
            continue
        for value in directive.values:
            if not _valid_lookup_path(table.name, value, table_map, field_map):
                errors.append(f"Unknown table directive field: {table.name}.{directive.verb}.{value}")
        for target in directive.targets:
            if not _valid_external_target(target, table_map, field_map):
                errors.append(f"Unknown table directive target: {table.name}.{directive.verb}.{target}")
    return errors


def _valid_external_target(
    target: str,
    table_map: dict[str, TableSchema],
    field_map: dict[str, set[str]],
) -> bool:
    parts = target.split(".")
    if len(parts) != 2:
        return False
    table_name, field_name = parts
    return table_name in table_map and field_name in field_map[table_name]


def _valid_lookup_path(
    table_name: str,
    path: str,
    table_map: dict[str, TableSchema],
    field_map: dict[str, set[str]],
) -> bool:
    if table_name not in table_map or not path:
        return False
    if re.search(r"[=<>+*/()]", path):
        return _unknown_expression_fields(path, field_map[table_name]) == ()
    parts = path.split(".")
    current_table = table_name
    for index, part in enumerate(parts):
        if part not in field_map.get(current_table, set()):
            return False
        if index == len(parts) - 1:
            return True
        reference = _reference_for_lookup_part(table_map[current_table], part)
        if reference is None:
            return False
        current_table = reference[0]
    return True


def _reference_for_lookup_part(table: TableSchema, part: str) -> tuple[str, str] | None:
    for column in table.columns:
        if column.name == part and column.references:
            return column.references
        if column.name == f"{part}_id" and column.references:
            return column.references
    return None


def _unknown_expression_fields(expression: str, known_fields: set[str]) -> tuple[str, ...]:
    unknown: list[str] = []
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression):
        if token in {"true", "false"} or token in known_fields:
            continue
        if token not in unknown:
            unknown.append(token)
    return tuple(unknown)


def _table(ctx, groups) -> tuple[TableSchema, list[RelationSchema]]:
    table_name = ctx.IDENT().getText()
    columns, relations, directives = _table_items(table_name, ctx.tableBody(), groups)
    columns = _dedupe_columns(table_name, columns)

    if not any(column.primary_key for column in columns):
        columns.insert(0, ColumnSchema("id", "int", nullable=False, primary_key=True))
    return TableSchema(table_name, tuple(columns), tuple(directives)), relations


def _table_items(
    table_name: str, body_ctx, groups, stack=()
) -> tuple[list[ColumnSchema], list[RelationSchema], list[TableDirectiveSchema]]:
    columns: list[ColumnSchema] = []
    relations: list[RelationSchema] = []
    directives: list[TableDirectiveSchema] = []

    for item in body_ctx.tableItem():
        if item.fieldDecl():
            source_group = stack[-1] if stack else None
            column, relation = _field(table_name, item.fieldDecl(), source_group=source_group)
            columns.append(column)
            if relation is not None:
                relations.append(relation)
        elif item.spreadDecl():
            group_name = item.spreadDecl().IDENT().getText()
            if group_name not in groups:
                raise AppGenSyntaxError(f"Unknown field group: {group_name}")
            if group_name in stack:
                cycle = " -> ".join((*stack, group_name))
                raise AppGenSyntaxError(f"Cyclic field group spread: {cycle}")
            group_columns, group_relations, group_directives = _table_items(
                table_name, groups[group_name], groups, (*stack, group_name)
            )
            columns.extend(group_columns)
            relations.extend(group_relations)
            directives.extend(group_directives)
        elif item.relationDecl():
            relations.append(_relation(item.relationDecl()))
        elif item.tableDirective():
            directives.append(_table_directive(item.tableDirective()))
    return columns, relations, directives


def _dedupe_columns(table_name: str, columns: list[ColumnSchema]) -> list[ColumnSchema]:
    ordered: list[ColumnSchema] = []
    positions: dict[str, int] = {}
    for column in columns:
        if column.name in positions:
            existing = ordered[positions[column.name]]
            if existing.source_group and column.source_group is None:
                ordered[positions[column.name]] = column
                continue
            if existing.source_group and column.source_group:
                raise AppGenSyntaxError(
                    f"Duplicate field declaration: {table_name}.{column.name} "
                    f"from {existing.source_group} and {column.source_group}"
                )
            raise AppGenSyntaxError(f"Duplicate field declaration: {table_name}.{column.name}")
            continue
        positions[column.name] = len(ordered)
        ordered.append(column)
    return ordered


def _field(table_name: str, ctx, *, source_group: str | None = None) -> tuple[ColumnSchema, RelationSchema | None]:
    column_name = ctx.IDENT().getText()
    type_name = ctx.typeRef().getText()
    nullable = True
    primary_key = False
    unique = False
    default = None
    references = None
    reference_cardinality = "many-to-one"
    hidden = False
    searchable = False
    expression = None

    if ctx.derivedExpr():
        expression = ctx.derivedExpr().expression().getText()
        nullable = False
        hidden = True

    for modifier in ctx.modifier():
        text = modifier.getText()
        if text == "pk":
            primary_key = True
            nullable = False
        elif text == "required":
            nullable = False
        elif text == "unique":
            unique = True
        elif text == "hidden":
            hidden = True
        elif text == "search":
            searchable = True
        elif modifier.DEFAULT():
            default = _literal(modifier.literal())
        elif modifier.REF() or modifier.ARROW():
            target = _target(modifier.target())
            references = target
            reference_cardinality = _relation_cardinality(modifier.relationCardinality())

    relation = None
    if references is not None:
        relation = RelationSchema(
            source_table=table_name,
            source_column=column_name,
            target_table=references[0],
            target_column=references[1],
            cardinality=reference_cardinality,
        )

    return (
        ColumnSchema(
            name=column_name,
            type_name=type_name,
            nullable=nullable,
            primary_key=primary_key,
            unique=unique,
            default=default,
            references=references,
            hidden=hidden,
            searchable=searchable,
            derived=expression is not None,
            expression=expression,
            source_group=source_group,
        ),
        relation,
    )


def _relation(ctx) -> RelationSchema:
    source_target, target_target = ctx.target()
    source_table, source_column = _target(source_target)
    target_table, target_column = _target(target_target)
    return RelationSchema(
        source_table=source_table,
        source_column=source_column,
        target_table=target_table,
        target_column=target_column,
        cardinality=_relation_cardinality(ctx.relationCardinality()),
    )


def _table_directive(ctx) -> TableDirectiveSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    verb = ctx.children[0].getText()
    name_index = 1 if identifiers and identifiers[0] == verb else 0
    name = identifiers[name_index] if len(identifiers) > name_index else None
    values = []
    targets = []
    after_arrow = False
    for child in ctx.children:
        text = child.getText()
        if text == "->":
            after_arrow = True
            continue
        if child.__class__.__name__ == "DirectiveValueContext":
            value = _directive_value(child)
            if after_arrow:
                targets.append(value)
            else:
                values.append(value)
    return TableDirectiveSchema(verb=verb, name=name, values=tuple(values), targets=tuple(targets))


def _relation_cardinality(ctx) -> str:
    if ctx is None:
        return "many-to-one"
    value = _agentic_value(ctx.agenticValue()).replace("_", "-").lower()
    allowed = {"many-to-one", "one-to-one", "one-to-many", "many-to-many"}
    if value not in allowed:
        known = ", ".join(sorted(allowed))
        raise AppGenSyntaxError(f"Unknown relation cardinality: {value}. Supported: {known}")
    return value


def _enum(ctx) -> EnumSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    return EnumSchema(identifiers[0], tuple(identifiers[1:]))


def _view(ctx) -> ViewSchema:
    fields: list[str] = []
    sections: list[ViewSectionSchema] = []
    components: list[FormComponentSchema] = []
    handlers: list[HandlerSchema] = []
    for item in ctx.viewItem():
        if item.handlerDecl():
            handlers.append(_handler(item.handlerDecl()))
            continue
        if item.componentPlacement():
            components.append(_component_placement(item.componentPlacement()))
            continue
        if item.COLON():
            section_fields = tuple(field.getText() for field in item.qualifiedName())
            sections.append(ViewSectionSchema(item.IDENT().getText(), section_fields))
            fields.extend(section_fields)
        else:
            fields.extend(field.getText() for field in item.qualifiedName())
    view_name = ctx.IDENT(0).getText()
    return ViewSchema(
        view_name,
        ctx.IDENT(1).getText(),
        tuple(fields),
        tuple(sections),
        tuple(components),
        tuple(handlers),
    )


def _component_placement(ctx) -> FormComponentSchema:
    field_name = ctx.qualifiedName().getText()
    component = ctx.IDENT().getText()
    numbers = [int(token.getText()) for token in ctx.INT()]
    return FormComponentSchema(
        name=field_name,
        component=component,
        field=field_name,
        x=numbers[0],
        y=numbers[1],
        w=numbers[2],
        h=numbers[3],
    )


def _flow(ctx) -> FlowSchema:
    steps = []
    directives = []
    for item in ctx.flowItem():
        if item.flowStep():
            source, target = [token.getText() for token in item.flowStep().IDENT()]
            steps.append(FlowStepSchema(source, target))
        elif item.flowDirective():
            directives.append(_flow_directive(item.flowDirective()))
    return FlowSchema(ctx.IDENT().getText(), tuple(steps), tuple(directives))


def _flow_directive(ctx) -> EnterpriseStatementSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    values = tuple(_agentic_value(value) for value in ctx.agenticValue())
    target = identifiers[-1] if ctx.ARROW() else None
    return EnterpriseStatementSchema(verb=identifiers[0], values=values, target=target)


def _role(ctx) -> RoleSchema:
    permissions = []
    for permission in ctx.permission():
        identifiers = [token.getText() for token in permission.IDENT()]
        permissions.append(PermissionSchema(identifiers[0], tuple(identifiers[1:])))
    return RoleSchema(ctx.IDENT().getText(), tuple(permissions))


def _rule(ctx) -> RuleSchema:
    identifiers = ctx.IDENT()
    conditions = []
    for item in ctx.ruleItem():
        if item.REQUIRED():
            field_name = item.IDENT(0).getText()
            message = _literal_text(item.STRING().getText()) if item.STRING() else None
            conditions.append(
                RuleConditionSchema(
                    field=field_name,
                    operator="required",
                    message=message,
                )
            )
            continue
        expression = item.ruleExpression()
        expression_text = expression.getText()
        terms = _collect_rule_terms(expression) or _rule_expression_terms(expression_text)
        field_name = _first_identifier(terms[0] if terms else expression_text)
        action = item.IDENT().getText() if item.ARROW() else None
        values = tuple(value for value in terms[1:] if value != field_name)
        conditions.append(
            RuleConditionSchema(
                field=field_name,
                operator=_rule_operator_text(expression),
                values=values,
                action=action,
            )
        )
    return RuleSchema(identifiers[0].getText(), identifiers[1].getText(), tuple(conditions))


def _rule_expression_terms(text: str) -> tuple[str, ...]:
    ignored = {"and", "or", "not", "exists", "is", "null", "in", "true", "false"}
    terms = []
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_.]*|\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*'|[0-9]+(?:\.[0-9]+)?", text):
        if token.lower() in ignored:
            continue
        terms.append(_literal_text(token) if token.startswith(("\"", "'")) else token)
    return tuple(terms)


def _collect_rule_terms(ctx) -> tuple[str, ...]:
    terms: list[str] = []

    def walk(node) -> None:
        if node.__class__.__name__ == "RuleTermContext":
            terms.append(node.getText())
            return
        for child in getattr(node, "children", ()) or ():
            walk(child)

    walk(ctx)
    return tuple(terms)


def _first_identifier(text: str) -> str:
    match = re.search(r"[A-Za-z_][A-Za-z0-9_]*", text)
    if not match:
        raise AppGenSyntaxError(f"Rule expression must start with a field reference: {text}")
    return match.group(0)


def _rule_operator_text(ctx) -> str:
    text = ctx.getText()
    for operator in ("==", "!=", ">=", "<=", ">", "<", "in"):
        if operator in text:
            return operator
    for operator in ("and", "or", "not", "exists", "isnull", "isnotnull"):
        if operator in text:
            return "expr"
    return "expr"


def _agentic_platform_block(kind: str, ctx) -> PlatformBlockSchema:
    return PlatformBlockSchema(kind=kind, name=ctx.IDENT().getText(), options=_agentic_options(ctx))


def _pbc_block(ctx) -> PlatformBlockSchema:
    options: dict[str, tuple[str, ...]] = {}
    statements: list[EnterpriseStatementSchema] = []
    handlers: list[HandlerSchema] = []
    permissions: list[PermissionSchema] = []
    for item in ctx.pbcItem():
        if item.handlerDecl():
            handlers.append(_handler(item.handlerDecl()))
        elif item.contractArrow():
            statements.append(_contract_arrow(item.contractArrow()))
        elif item.permission():
            identifiers = [token.getText() for token in item.permission().IDENT()]
            permissions.append(PermissionSchema(identifiers[0], tuple(identifiers[1:])))
        elif item.agenticOption():
            option = item.agenticOption()
            values = tuple(_agentic_value(value) for value in option.agenticValue())
            key = option.IDENT().getText()
            if _looks_like_permission(key, values):
                permissions.append(PermissionSchema(key, values))
            else:
                options[key] = values
    return PlatformBlockSchema(
        kind="pbc",
        name=ctx.IDENT().getText(),
        options=options,
        statements=tuple(statements),
        handlers=tuple(handlers),
        permissions=tuple(permissions),
    )


def _enterprise_contracts(schema: AppSchema) -> tuple[EnterpriseContractSchema, ...]:
    return (
        *schema.api_contracts,
        *schema.event_contracts,
        *schema.job_contracts,
        *schema.report_contracts,
        *schema.menu_contracts,
        *schema.component_contracts,
        *schema.package_contracts,
        *schema.test_contracts,
    )


def _enterprise_contract_groups(schema: AppSchema) -> dict[str, tuple[EnterpriseContractSchema, ...]]:
    return {
        "api": schema.api_contracts,
        "event": schema.event_contracts,
        "job": schema.job_contracts,
        "report": schema.report_contracts,
        "menu": schema.menu_contracts,
        "component": schema.component_contracts,
        "package": schema.package_contracts,
        "test": schema.test_contracts,
    }


def _enterprise_contract(kind: str, ctx) -> EnterpriseContractSchema:
    options: dict[str, tuple[str, ...]] = {}
    statements: list[EnterpriseStatementSchema] = []
    handlers: list[HandlerSchema] = []
    permissions: list[PermissionSchema] = []
    for item in ctx.contractItem():
        if item.handlerDecl():
            handlers.append(_handler(item.handlerDecl()))
        elif item.contractArrow():
            statements.append(_contract_arrow(item.contractArrow()))
        elif item.contractDirective():
            statements.append(_contract_directive(item.contractDirective()))
        elif item.permission():
            identifiers = [token.getText() for token in item.permission().IDENT()]
            permissions.append(PermissionSchema(identifiers[0], tuple(identifiers[1:])))
        elif item.agenticOption():
            option = item.agenticOption()
            values = tuple(_agentic_value(value) for value in option.agenticValue())
            options[option.IDENT().getText()] = values
    return EnterpriseContractSchema(
        kind=kind,
        name=ctx.IDENT().getText(),
        options=options,
        statements=tuple(statements),
        handlers=tuple(handlers),
        permissions=tuple(permissions),
    )


def _deployment_block(ctx) -> PlatformBlockSchema:
    options: dict[str, tuple[str, ...]] = {}
    units: list[DeploymentUnitSchema] = []
    scales: list[DeploymentScaleSchema] = []
    health_checks: list[DeploymentHealthSchema] = []
    statements: list[EnterpriseStatementSchema] = []
    for item in ctx.deploymentItem():
        if item.deployUnit():
            units.append(_deploy_unit(item.deployUnit()))
        elif item.deployScale():
            scales.append(_deploy_scale(item.deployScale()))
        elif item.deployHealth():
            health_checks.append(_deploy_health(item.deployHealth()))
        elif item.deployCheck():
            health_checks.append(_deploy_check(item.deployCheck()))
        elif item.deployResource():
            statements.append(_deploy_resource(item.deployResource()))
        elif item.deployBinding():
            statements.append(_deploy_binding(item.deployBinding()))
        elif item.deployDirective():
            statements.append(_deploy_directive(item.deployDirective()))
        elif item.agenticOption():
            option = item.agenticOption()
            values = tuple(_agentic_value(value) for value in option.agenticValue())
            options[option.IDENT().getText()] = values
    return PlatformBlockSchema(
        kind="deploy",
        name=ctx.IDENT().getText(),
        options=options,
        statements=tuple(statements),
        deployment_units=tuple(units),
        deployment_scales=tuple(scales),
        deployment_health=tuple(health_checks),
    )


def _deploy_unit(ctx) -> DeploymentUnitSchema:
    target, pattern = [token.getText() for token in ctx.IDENT()]
    return DeploymentUnitSchema(target=target, pattern=pattern)


def _deploy_scale(ctx) -> DeploymentScaleSchema:
    target = ctx.IDENT().getText()
    minimum, maximum = [int(token.getText()) for token in ctx.INT()]
    return DeploymentScaleSchema(target=target, minimum=minimum, maximum=maximum)


def _deploy_health(ctx) -> DeploymentHealthSchema:
    target = ctx.IDENT().getText()
    return DeploymentHealthSchema(target=target, path=_literal_text(ctx.STRING().getText()))


def _deploy_check(ctx) -> DeploymentHealthSchema:
    target, kind = [token.getText() for token in ctx.IDENT()]
    return DeploymentHealthSchema(target=target, path=_literal_text(ctx.STRING().getText()), kind=kind)


def _deploy_directive(ctx) -> EnterpriseStatementSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    values = tuple(_agentic_value(value) for value in ctx.agenticValue())
    return EnterpriseStatementSchema(verb=identifiers[0], values=values, target=identifiers[1])


def _deploy_resource(ctx) -> EnterpriseStatementSchema:
    target, resource_name = [token.getText() for token in ctx.IDENT()]
    value = _agentic_value(ctx.agenticValue())
    return EnterpriseStatementSchema(verb="resource", values=(resource_name, value), target=target)


def _deploy_binding(ctx) -> EnterpriseStatementSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    if ctx.ENV():
        verb = "env"
        target = identifiers[0]
    else:
        verb = identifiers[0]
        target = identifiers[1]
    value = _agentic_value(ctx.agenticValue())
    return EnterpriseStatementSchema(verb=verb, values=(value,), target=target)


def _handler(ctx) -> HandlerSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    if ctx.ON():
        trigger, event, target = "on", identifiers[0], identifiers[1]
    else:
        trigger, event, target = identifiers
    return HandlerSchema(trigger=trigger, event=event, target=target)


def _contract_arrow(ctx) -> EnterpriseStatementSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    values = tuple(_agentic_value(value) for value in ctx.agenticValue())
    return EnterpriseStatementSchema(verb=identifiers[0], values=values, target=identifiers[-1])


def _contract_directive(ctx) -> EnterpriseStatementSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    values = tuple(_agentic_value(value) for value in ctx.agenticValue())
    return EnterpriseStatementSchema(verb=identifiers[0], values=values)


def _composition_block(ctx) -> PlatformBlockSchema:
    options: dict[str, tuple[str, ...]] = {}
    for item in ctx.compositionItem():
        text = item.getText()
        if item.agenticOption():
            values = tuple(_agentic_value(value) for value in item.agenticOption().agenticValue())
            options[item.agenticOption().IDENT().getText()] = values
        elif text.startswith("includepbc"):
            key = item.IDENT(0).getText()
            version_values = tuple(_agentic_value(value) for value in item.agenticValue())
            version = version_values[0] if version_values else ""
            options["include"] = (*options.get("include", ()), f"{key} version {version}".strip())
        elif text.startswith("require"):
            options["require"] = (*options.get("require", ()), text.replace("require", "", 1))
        elif text.startswith("expose"):
            options["expose"] = (*options.get("expose", ()), text.replace("expose", "", 1))
        elif text.startswith("connect"):
            identifiers = [token.getText() for token in item.IDENT()]
            if len(identifiers) == 6:
                connection = f"{identifiers[0]} {identifiers[1]} {identifiers[2]} -> {identifiers[3]} {identifiers[4]} {identifiers[5]}"
            else:
                connection = text.replace("connect", "", 1)
            options["connect"] = (*options.get("connect", ()), connection)
    return PlatformBlockSchema(kind="composition", name=ctx.IDENT().getText(), options=options)


def _operation_block(ctx) -> PlatformBlockSchema:
    steps: list[FlowStepSchema] = []
    options: dict[str, tuple[str, ...]] = {}
    handlers: list[HandlerSchema] = []
    statements: list[EnterpriseStatementSchema] = []
    for item in ctx.operationItem():
        if item.flowStep():
            source, target = [token.getText() for token in item.flowStep().IDENT()]
            steps.append(FlowStepSchema(source, target))
        elif item.handlerDecl():
            handlers.append(_handler(item.handlerDecl()))
        elif item.contractArrow():
            statements.append(_contract_arrow(item.contractArrow()))
        elif item.agenticOption():
            values = tuple(_agentic_value(value) for value in item.agenticOption().agenticValue())
            options[item.agenticOption().IDENT().getText()] = values
    return PlatformBlockSchema(
        kind="operation",
        name=ctx.IDENT().getText(),
        options=options,
        steps=tuple(steps),
        statements=tuple(statements),
        handlers=tuple(handlers),
    )


def _security_block(ctx) -> PlatformBlockSchema:
    permissions: list[PermissionSchema] = []
    options: dict[str, tuple[str, ...]] = {}
    for item in ctx.securityItem():
        if item.permission():
            identifiers = [token.getText() for token in item.permission().IDENT()]
            permissions.append(PermissionSchema(identifiers[0], tuple(identifiers[1:])))
        elif item.agenticOption():
            values = tuple(_agentic_value(value) for value in item.agenticOption().agenticValue())
            key = item.agenticOption().IDENT().getText()
            if _looks_like_permission(key, values):
                permissions.append(PermissionSchema(key, values))
            else:
                options[key] = values
    return PlatformBlockSchema(
        kind="security",
        name=ctx.IDENT().getText(),
        options=options,
        permissions=tuple(permissions),
    )


def _llm_provider(ctx) -> LLMProviderSchema:
    options = _agentic_options(ctx)
    return LLMProviderSchema(
        name=ctx.IDENT().getText(),
        provider=options.get("provider", ("openai",))[0],
        mode=options.get("mode", ("api",))[0],
        model=_first_or_none(options.get("model")),
        endpoint=_first_or_none(options.get("endpoint")),
        api_key=_first_or_none(options.get("api_key")),
    )


def _agent(ctx) -> AgentSchema:
    options: dict[str, tuple[str, ...]] = {}
    competencies: list[EnterpriseStatementSchema] = []
    handlers: list[HandlerSchema] = []
    permissions: list[PermissionSchema] = []
    for item in ctx.agentItem():
        if item.handlerDecl():
            handlers.append(_handler(item.handlerDecl()))
        elif item.contractArrow():
            competencies.append(_contract_arrow(item.contractArrow()))
        elif item.permission():
            identifiers = [token.getText() for token in item.permission().IDENT()]
            permissions.append(PermissionSchema(identifiers[0], tuple(identifiers[1:])))
        elif item.agenticOption():
            values = tuple(_agentic_value(value) for value in item.agenticOption().agenticValue())
            key = item.agenticOption().IDENT().getText()
            if _looks_like_permission(key, values):
                permissions.append(PermissionSchema(key, values))
            else:
                options[key] = values
    max_steps = _first_or_none(options.get("max_steps")) or "8"
    return AgentSchema(
        name=ctx.IDENT().getText(),
        provider=_first_or_none(options.get("provider")),
        goal=_first_or_none(options.get("goal")),
        tools=options.get("tools", ()),
        memory=_first_or_none(options.get("memory")) or "session",
        max_steps=int(max_steps),
        competencies=tuple(competencies),
        handlers=tuple(handlers),
        permissions=tuple(permissions),
    )


def _agentic_options(ctx) -> dict[str, tuple[str, ...]]:
    options: dict[str, tuple[str, ...]] = {}
    for option in ctx.agenticOption():
        values = tuple(_agentic_value(value) for value in option.agenticValue())
        options[option.IDENT().getText()] = values
    return options


def _looks_like_permission(key: str, values: tuple[str, ...]) -> bool:
    return bool(key[:1].isupper() and values and all(re.fullmatch(r"[a-z_]+", value) for value in values))


def _agentic_value(ctx) -> str:
    text = "".join(token.getText() for token in ctx.children)
    if text.startswith(("\"", "'")):
        return _literal_text(text)
    return text


def _directive_value(ctx) -> str:
    return _literal_text(ctx.getText()) if ctx.getText().startswith(("\"", "'")) else ctx.getText()


def _first_or_none(values: tuple[str, ...] | None) -> str | None:
    if not values:
        return None
    return values[0]


def _target(ctx) -> tuple[str, str]:
    table, column = ctx.IDENT()
    return table.getText(), column.getText()


def _literal(ctx) -> str:
    return _literal_text(ctx.getText())


def _literal_text(text: str) -> str:
    if text.startswith(("\"", "'")):
        return ast.literal_eval(text)
    return text


def _apply_external_relations(
    tables: list[TableSchema], relations: list[RelationSchema]
) -> list[TableSchema]:
    relation_map = {
        (relation.source_table, relation.source_column): relation for relation in relations
    }
    updated_tables: list[TableSchema] = []

    for table in tables:
        columns = []
        for column in table.columns:
            relation = relation_map.get((table.name, column.name))
            if relation is None or column.references is not None:
                columns.append(column)
                continue
            columns.append(
                ColumnSchema(
                    name=column.name,
                    type_name=column.type_name,
                    nullable=column.nullable,
                    primary_key=column.primary_key,
                    unique=column.unique,
                    default=column.default,
                    references=(relation.target_table, relation.target_column),
                    hidden=column.hidden,
                    searchable=column.searchable,
                    derived=column.derived,
                    expression=column.expression,
                    source_group=column.source_group,
                )
            )
        updated_tables.append(TableSchema(table.name, tuple(columns), table.directives))
    return updated_tables
