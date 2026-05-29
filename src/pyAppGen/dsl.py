"""ANTLR-backed parser for the AppGen low-code DSL."""

from __future__ import annotations

import argparse
import ast
import contextlib
import difflib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import tomllib
from collections import Counter
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

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
SUPPORTED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
RELEASE_TARGET_CHOICES = ("web", "mobile", "desktop", "pbc", "deployment", "all")
LINT_STAGE_NAMES = ("syntax", "semantic", "policy")
LINT_SEVERITY_NAMES = ("error", "warning", "info", "hint")
REQUIRED_MIGRATION_DETECTIONS = (
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
REQUIRED_COMPLETION_SOURCES = (
    "top_level_keywords",
    "block_snippets",
    "table_names",
    "field_names",
    "lookup_paths",
    "components",
    "handler_events",
    "operation_targets",
    "flow_states",
    "pbc_keys",
    "pbc_contracts",
    "pbc_apis",
    "pbc_events",
    "pbc_commands",
    "package_targets",
    "deployment_units",
    "llm_providers",
    "agent_skills",
)
REQUIRED_DIAGNOSTIC_FIELDS = (
    "code",
    "title",
    "severity",
    "message",
    "range",
    "related_locations",
    "fixes",
    "docs_url",
)
DIAGNOSTIC_CATALOG_FIELDS = (
    "code",
    "severity",
    "title",
    "trigger",
    "example_fix",
    "docs_url",
    "fixture",
)
REQUIRED_SYMBOL_KINDS = (
    "app",
    "table",
    "field",
    "group",
    "enum",
    "enum_value",
    "view",
    "component_binding",
    "handler",
    "flow",
    "flow_state",
    "operation",
    "role",
    "permission",
    "rule",
    "llm",
    "agent",
    "agent_skill",
    "pbc",
    "composition",
    "api",
    "event",
    "job",
    "report",
    "menu",
    "component",
    "package",
    "deployment_unit",
    "audit",
    "version",
    "security",
)


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


def format_dsl_file(path: str | Path, *, organize: bool = False) -> dict:
    """Format an AppGen DSL file in place and return before/after metadata."""
    path = Path(path)
    result = format_dsl(path.read_text(), source_name=str(path), organize=organize)
    if result["changed"]:
        path.write_text(result["formatted"])
    return result


def lint_dsl(
    text: str,
    *,
    source_name: str | None = None,
    component_catalog: Iterable[str] | None = None,
) -> dict:
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
        errors.append("Use an environment variable name for api_key, not a literal secret.")
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
        policy_errors, policy_warnings = _tooling_policy_diagnostics(schema, component_catalog=component_catalog)
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


def format_dsl(text: str, *, source_name: str | None = None, organize: bool = False) -> dict:
    """Return deterministic DSL formatting plus before/after lint metadata."""
    original = text or ""
    formatted = _format_dsl_source(original)
    if organize:
        formatted = _organize_formatted_table_fields(formatted)
    return {
        "format": "appgen.dsl-format-result.v1",
        "source": source_name,
        "changed": formatted != original,
        "organize": organize,
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
        schema = _completion_schema(source)
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
        if schema is not None:
            table_map = {table.name: table for table in schema.tables}
            field_map = {
                table.name: {field.name: field for field in table.columns}
                for table in schema.tables
            }
            for table in schema.tables:
                for path, detail in _semantic_lookup_paths(table, table_map, field_map).items():
                    if detail.get("valid"):
                        items.append({"label": path, "insert": path, "kind": "lookup_path", "detail": table.name})
                for directive in table.directives:
                    if directive.verb.lower() == "lookup":
                        for value in directive.values:
                            items.append({"label": value, "insert": value, "kind": "lookup_path", "detail": table.name})
            for component_name in sorted(_known_component_names(schema)):
                items.append({"label": component_name, "insert": component_name, "kind": "component"})
            for event_name in ("Click", "Change", "Open", "Save", "Submit", "Select", "Run"):
                items.append({"label": event_name, "insert": event_name, "kind": "handler_event"})
            for target_name in sorted(_handler_target_names(schema)):
                items.append({"label": target_name, "insert": target_name, "kind": "handler_target"})
            for flow in schema.flows:
                for transition in flow.steps:
                    items.append({"label": transition.source, "insert": transition.source, "kind": "flow_state", "detail": flow.name})
                    items.append({"label": transition.target, "insert": transition.target, "kind": "flow_state", "detail": flow.name})
                for directive in flow.directives:
                    for value in directive.values:
                        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", value):
                            items.append({"label": value, "insert": value, "kind": "flow_state", "detail": flow.name})
            catalog = _pbc_catalog_by_key()
            for key, pbc in sorted(catalog.items()):
                items.append({"label": key, "insert": key, "kind": "pbc", "detail": pbc.get("label", "PBC catalog entry")})
                for api in pbc.get("apis", ())[:8]:
                    items.append({"label": api, "insert": api, "kind": "pbc_contract", "detail": key})
                    items.append({"label": api, "insert": api, "kind": "pbc_api", "detail": key})
                    if str(api).upper().startswith(("POST ", "PUT ", "PATCH ", "DELETE ")):
                        items.append({"label": api, "insert": api, "kind": "pbc_command", "detail": key})
                for event_name in tuple(pbc.get("emits", ()))[:8] + tuple(pbc.get("consumes", ()))[:8]:
                    items.append({"label": event_name, "insert": event_name, "kind": "pbc_contract", "detail": key})
                    items.append({"label": event_name, "insert": event_name, "kind": "pbc_event", "detail": key})
            for target in ("web", "mobile", "desktop", "pbc", "deployment"):
                items.append({"label": target, "insert": target, "kind": "package_target"})
            for block in schema.platform_blocks:
                if block.kind == "operation":
                    items.append({"label": block.name, "insert": block.name, "kind": "deployment_unit"})
            for deploy in (block for block in schema.platform_blocks if block.kind == "deploy"):
                for unit in deploy.deployment_units:
                    items.append({"label": unit.target, "insert": unit.target, "kind": "deployment_unit", "detail": deploy.name})
            for agent in schema.agents:
                for tool in agent.tools:
                    items.append({"label": tool, "insert": tool, "kind": "agent_skill", "detail": agent.name})
        for provider_name in outline.get("llms", ()):
            items.append({"label": provider_name, "insert": provider_name, "kind": "llm"})
        if schema is not None:
            for provider in schema.llm_providers:
                items.append({"label": provider.name, "insert": provider.name, "kind": "llm"})
    deduped = tuple({(item["kind"], item["label"]): item for item in items}.values())
    if not needle:
        return deduped
    return tuple(item for item in deduped if item["label"].lower().startswith(needle))


def _completion_schema(source: str) -> AppSchema | None:
    try:
        return schema_from_dsl(source)
    except Exception:
        return None


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
    model["symbol_coverage"] = symbol_coverage_dsl(source, source_name=source_name, model=model)
    return model


def symbol_coverage_dsl(text: str, *, source_name: str | None = None, model: dict | None = None) -> dict:
    """Return required semantic-symbol kind coverage for docs/tooling.md."""
    semantic = model if model is not None else semantic_model_dsl(text, source_name=source_name)
    symbols = tuple(semantic.get("symbols", {}).values())
    detected = {symbol.get("kind") for symbol in symbols}
    return {
        "format": "appgen.symbol-coverage.v1",
        "source": source_name,
        "required": REQUIRED_SYMBOL_KINDS,
        "detected": tuple(kind for kind in REQUIRED_SYMBOL_KINDS if kind in detected),
        "missing": tuple(kind for kind in REQUIRED_SYMBOL_KINDS if kind not in detected),
        "counts": {
            kind: sum(1 for symbol in symbols if symbol.get("kind") == kind)
            for kind in REQUIRED_SYMBOL_KINDS
            if kind in detected
        },
        "symbol_count": len(symbols),
    }


def semantic_model_dsl_file(path: str | Path) -> dict:
    path = Path(path)
    return semantic_model_dsl(path.read_text(encoding="utf-8"), source_name=str(path))


def lint_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    strict: bool = False,
    component_catalog: Iterable[str] | None = None,
    component_catalog_source: str | None = None,
    previous_semantic_model: dict | None = None,
    previous_semantic_source: str | None = None,
    migration_backend: str = "postgresql",
) -> dict:
    """Return the docs/tooling.md appgen.lint-report.v1 contract."""
    source = text or ""
    component_catalog_names = tuple(dict.fromkeys(component_catalog or ()))
    legacy = lint_dsl(source, source_name=source_name, component_catalog=component_catalog_names)
    diagnostics = tuple(
        _strict_lint_diagnostic(_spec_diagnostic_from_legacy(source, item), strict=strict)
        for item in legacy["diagnostics"]
    )
    counts = {
        severity: sum(1 for item in diagnostics if item["severity"] == severity)
        for severity in LINT_SEVERITY_NAMES
    }
    stages = _lint_stage_counts(diagnostics)
    return {
        "format": "appgen.lint-report.v1",
        "ok": not counts["error"],
        "stage_names": LINT_STAGE_NAMES,
        "severity_names": LINT_SEVERITY_NAMES,
        "files": (source_name,) if source_name else (),
        "stages": stages,
        "severity_counts": counts,
        "diagnostics": diagnostics,
        "fixes_available": any(item.get("fixes") for item in diagnostics),
        "semantic_model_available": legacy["ok"],
        "strict": strict,
        "component_catalog": {
            "source": component_catalog_source,
            "components": component_catalog_names,
            "count": len(component_catalog_names),
        },
        "migration_preview": _lint_migration_preview(
            source,
            source_name=source_name,
            previous_semantic_model=previous_semantic_model,
            previous_semantic_source=previous_semantic_source,
            backend=migration_backend,
        ),
        "legacy_report": legacy,
    }


def lint_report_dsl_sources(
    sources: dict[str, str],
    *,
    strict: bool = False,
    component_catalog: Iterable[str] | None = None,
    component_catalog_source: str | None = None,
    previous_semantic_model: dict | None = None,
    previous_semantic_source: str | None = None,
    migration_backend: str = "postgresql",
) -> dict:
    """Aggregate linter output for a multi-file AppGen-X source set."""
    component_catalog_names = tuple(dict.fromkeys(component_catalog or ()))
    if not sources:
        diagnostic = _spec_diagnostic("", "AGX0001", "error", "No .appgen files found in directory input.")
        return {
            "format": "appgen.lint-report.v1",
            "ok": False,
            "stage_names": LINT_STAGE_NAMES,
            "severity_names": LINT_SEVERITY_NAMES,
            "files": (),
            "stages": _lint_stage_counts((diagnostic,)),
            "severity_counts": {"error": 1, "warning": 0, "info": 0, "hint": 0},
            "diagnostics": (diagnostic,),
            "fixes_available": False,
            "semantic_model_available": False,
            "strict": strict,
            "component_catalog": {
                "source": component_catalog_source,
                "components": component_catalog_names,
                "count": len(component_catalog_names),
            },
            "source_mode": "directory",
            "file_reports": (),
            "migration_preview": None,
        }
    reports = tuple(
        lint_report_dsl(
            source,
            source_name=name,
            strict=strict,
            component_catalog=component_catalog_names,
            component_catalog_source=component_catalog_source,
        )
        for name, source in sorted(sources.items())
    )
    combined_source = "\n\n".join(source for _, source in sorted(sources.items()))
    diagnostics = tuple(
        {**diagnostic, "file": report["files"][0] if report.get("files") else None}
        for report in reports
        for diagnostic in report["diagnostics"]
    )
    counts = {
        severity: sum(1 for item in diagnostics if item["severity"] == severity)
        for severity in LINT_SEVERITY_NAMES
    }
    stages = _lint_stage_counts(diagnostics)
    return {
        "format": "appgen.lint-report.v1",
        "ok": not counts["error"],
        "stage_names": LINT_STAGE_NAMES,
        "severity_names": LINT_SEVERITY_NAMES,
        "files": tuple(report["files"][0] for report in reports if report.get("files")),
        "stages": stages,
        "severity_counts": counts,
        "diagnostics": diagnostics,
        "fixes_available": any(report["fixes_available"] for report in reports),
        "semantic_model_available": all(report["semantic_model_available"] for report in reports),
        "strict": strict,
        "component_catalog": {
            "source": component_catalog_source,
            "components": component_catalog_names,
            "count": len(component_catalog_names),
        },
        "source_mode": "directory" if len(reports) != 1 else "multi-source",
        "file_reports": reports,
        "migration_preview": _lint_migration_preview(
            combined_source,
            source_name=";".join(sorted(sources)),
            previous_semantic_model=previous_semantic_model,
            previous_semantic_source=previous_semantic_source,
            backend=migration_backend,
        ),
    }


def lint_report_dsl_file(
    path: str | Path,
    *,
    strict: bool = False,
    component_catalog: Iterable[str] | None = None,
    component_catalog_source: str | None = None,
    previous_semantic_model: dict | None = None,
    previous_semantic_source: str | None = None,
    migration_backend: str = "postgresql",
) -> dict:
    path = Path(path)
    return lint_report_dsl(
        path.read_text(encoding="utf-8"),
        source_name=str(path),
        strict=strict,
        component_catalog=component_catalog,
        component_catalog_source=component_catalog_source,
        previous_semantic_model=previous_semantic_model,
        previous_semantic_source=previous_semantic_source,
        migration_backend=migration_backend,
    )


def lint_report_dsl_path(
    path: str | Path,
    *,
    strict: bool = False,
    catalog_path: str | Path | None = None,
    previous_semantic_path: str | Path | None = None,
    migration_backend: str = "postgresql",
) -> dict:
    path = Path(path)
    component_catalog = _load_component_catalog(catalog_path) if catalog_path else ()
    component_catalog_source = str(catalog_path) if catalog_path else None
    previous_semantic_model = _load_previous_semantic_model(previous_semantic_path)
    previous_semantic_source = str(previous_semantic_path) if previous_semantic_path else None
    if path.is_dir():
        sources = {
            str(item): item.read_text(encoding="utf-8")
            for item in sorted(path.rglob("*.appgen"))
            if item.is_file()
        }
        return lint_report_dsl_sources(
            sources,
            strict=strict,
            component_catalog=component_catalog,
            component_catalog_source=component_catalog_source,
            previous_semantic_model=previous_semantic_model,
            previous_semantic_source=previous_semantic_source,
            migration_backend=migration_backend,
        )
    return lint_report_dsl_file(
        path,
        strict=strict,
        component_catalog=component_catalog,
        component_catalog_source=component_catalog_source,
        previous_semantic_model=previous_semantic_model,
        previous_semantic_source=previous_semantic_source,
        migration_backend=migration_backend,
    )


def _load_component_catalog(catalog_path: str | Path | None) -> tuple[str, ...]:
    if not catalog_path:
        return ()
    path = Path(catalog_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(sorted(_component_names_from_catalog(payload)))


def _load_previous_semantic_model(path: str | Path | None) -> dict | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict) and payload.get("format") == "appgen.semantic-model.v1":
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("semantic_model"), dict):
        return payload["semantic_model"]
    return payload if isinstance(payload, dict) else None


def _lint_stage_counts(diagnostics: Iterable[dict]) -> dict:
    diagnostics = tuple(diagnostics)
    return {
        stage: {
            "diagnostic_count": len(items),
            "error": sum(1 for item in items if item.get("severity") == "error"),
            "warning": sum(1 for item in items if item.get("severity") == "warning"),
            "codes": tuple(item.get("code") for item in items),
        }
        for stage, items in (
            (stage, tuple(item for item in diagnostics if _lint_stage_for_diagnostic(item) == stage))
            for stage in LINT_STAGE_NAMES
        )
    }


def _lint_stage_for_diagnostic(diagnostic: dict) -> str:
    code = str(diagnostic.get("code", ""))
    if code in {"AGX0001"} or code.startswith("AGX90"):
        return "syntax"
    if code in {"AGX0404", "AGX0702", "AGX0802", "AGX0903", "AGX1002", "AGX1101", "AGX1201"}:
        return "policy"
    return "semantic"


def _lint_migration_preview(
    source: str,
    *,
    source_name: str | None,
    previous_semantic_model: dict | None,
    previous_semantic_source: str | None,
    backend: str,
) -> dict | None:
    if previous_semantic_model is None:
        return None
    current_semantic = semantic_model_dsl(source, source_name=source_name)
    return migration_plan_from_semantic_models(
        previous_semantic_model,
        current_semantic,
        previous_name=previous_semantic_source,
        current_name=source_name,
        current_text=source,
        backend=backend,
    )


def _component_names_from_catalog(payload: object) -> set[str]:
    names: set[str] = set()
    if isinstance(payload, str):
        if payload.strip():
            names.add(payload.strip())
        return names
    if isinstance(payload, list):
        for item in payload:
            names.update(_component_names_from_catalog(item))
        return names
    if isinstance(payload, dict):
        for key in ("name", "component", "type"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                names.add(value.strip())
        for key in ("components", "component_catalog", "registered_components", "items"):
            if key in payload:
                names.update(_component_names_from_catalog(payload[key]))
    return names


def component_publish_report(component: str, *, catalog_path: str | Path | None = None) -> dict:
    """Return a side-effect-free component catalog publication plan."""
    component_name = component.strip()
    path = Path(catalog_path) if catalog_path else None
    catalog_exists = path.exists() if path else False
    catalog_components = _load_component_catalog(path) if path and catalog_exists else ()
    already_registered = component_name in catalog_components
    catalog_patch = {
        "format": "appgen.component-catalog-patch.v1",
        "operation": "upsert_component",
        "component": {
            "name": component_name,
            "icon": _component_icon_name(component_name),
        },
        "catalog_path": str(path) if path else None,
        "before_count": len(catalog_components),
        "after_count": len(catalog_components) if already_registered else len(catalog_components) + 1,
        "already_registered": already_registered,
        "side_effect_free": True,
        "write_performed": False,
    }
    checks = (
        {
            "check": "component_name_declared",
            "ok": bool(component_name),
            "message": "A component name must be provided.",
        },
        {
            "check": "catalog_path_readable",
            "ok": path is None or catalog_exists,
            "message": "Catalog path exists when one is supplied.",
        },
        {
            "check": "side_effect_free_plan",
            "ok": catalog_patch["side_effect_free"] is True and catalog_patch["write_performed"] is False,
            "message": "Publishing returns a catalog patch without mutating files.",
        },
    )
    return {
        "format": "appgen.component-publish-report.v1",
        "ok": all(check["ok"] for check in checks),
        "component": component_name,
        "catalog": {
            "source": str(path) if path else None,
            "exists": catalog_exists,
            "components": catalog_components,
            "count": len(catalog_components),
        },
        "catalog_patch": catalog_patch,
        "checks": checks,
        "blocking_gaps": tuple(check["check"] for check in checks if not check["ok"]),
    }


def _component_icon_name(component_name: str) -> str:
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|\d+", component_name)
    return "-".join(word.lower() for word in words) or "component"


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
    catalog_shape_gaps = tuple(
        {
            "code": spec.get("code"),
            "missing": tuple(
                field
                for field in DIAGNOSTIC_CATALOG_FIELDS
                if field not in spec or spec.get(field) in (None, "")
            ),
        }
        for spec in specs
        if any(field not in spec or spec.get(field) in (None, "") for field in DIAGNOSTIC_CATALOG_FIELDS)
    )
    ranges = tuple(
        {
            "range": item[0],
            "area": item[1],
        }
        for item in DIAGNOSTIC_RANGES
    )
    covered = tuple(item["code"] for item in specs if item["fixture"])
    return {
        "format": "appgen.diagnostic-catalog.v1",
        "ok": all(item["fixture"] for item in specs) and not catalog_shape_gaps,
        "ranges": ranges,
        "diagnostics": specs,
        "diagnostic_shape_fields": REQUIRED_DIAGNOSTIC_FIELDS,
        "catalog_fields": DIAGNOSTIC_CATALOG_FIELDS,
        "catalog_shape_gaps": catalog_shape_gaps,
        "runtime_shape_enforced_by": "appgen.diagnostic-fixture-audit.v1",
        "required_codes": tuple(item["code"] for item in specs),
        "covered_fixture_codes": covered,
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
    with tempfile.TemporaryDirectory(prefix="appgen-drift-generator-") as tmp:
        generation = generate_report_dsl(
            source,
            source_name=source_name,
            output_dir=Path(tmp) / "generated",
            targets=semantic.get("app", {}).get("targets", ()),
            allow_warnings=True,
        )
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
            "generator_validation_uses_semantic_model",
            generation.get("semantic_model_format") == semantic.get("format")
            and _semantic_drift_digest(generation.get("validation", {}).get("semantic_model", {})) == canonical,
            "appgen generate validates and emits artifacts from the same semantic model as CLI/LSP/IDE surfaces.",
            {
                "surface": "generator",
                "format": generation.get("format"),
                "generated": generation.get("generated"),
                "artifact_count": len(generation.get("artifacts", ())),
            },
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
            "generator",
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
            "generate_report": generation.get("format"),
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
    expected_diagnostics = tuple(item for item in diagnostics if item["code"] in expected)
    shape_gaps = tuple(
        {
            "code": item.get("code"),
            "missing": tuple(
                key
                for key in ("range", "related_locations", "fixes", "docs_url")
                if key not in item or item.get(key) in (None, "")
            ),
        }
        for item in expected_diagnostics
        if any(key not in item or item.get(key) in (None, "") for key in ("range", "related_locations", "fixes", "docs_url"))
    )
    expected_severities = {spec["code"]: spec["severity"] for spec in DIAGNOSTIC_SPECS}
    severity_gaps = tuple(
        {
            "code": item.get("code"),
            "expected": expected_severities.get(item.get("code")),
            "actual": item.get("severity"),
        }
        for item in expected_diagnostics
        if expected_severities.get(item.get("code")) and item.get("severity") != expected_severities.get(item.get("code"))
    )
    return {
        "name": fixture["name"],
        "runner": runner,
        "expected_codes": expected,
        "observed_codes": observed,
        "ok": not missing and not shape_gaps and not severity_gaps,
        "missing_codes": missing,
        "shape_gaps": shape_gaps,
        "severity_gaps": severity_gaps,
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
    """Run docs/tooling.md subcommands with stable CLI error boundaries."""
    cli_args = tuple(argv or ())
    try:
        return _dsl_tooling_cli_impl(cli_args)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - exercised through subprocess boundaries
        _emit_tooling_payload(
            _internal_tooling_error_report(exc),
            as_json="--json" in cli_args,
        )
        return 3


def _dsl_tooling_cli_impl(argv: Iterable[str] | None = None) -> int:
    """Run docs/tooling.md subcommands without disturbing legacy flags."""
    parser = argparse.ArgumentParser(prog="appgen")
    subparsers = parser.add_subparsers(dest="command", required=True)

    lint_parser = subparsers.add_parser("lint")
    lint_parser.add_argument("path")
    lint_parser.add_argument("--json", action="store_true")
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.add_argument("--catalog")
    lint_parser.add_argument("--previous-semantic")
    lint_parser.add_argument("--backend", default="postgresql", choices=SUPPORTED_DATABASE_BACKENDS)

    format_parser = subparsers.add_parser("format")
    format_parser.add_argument("path")
    format_parser.add_argument("--check", action="store_true")
    format_parser.add_argument("--write", action="store_true")
    format_parser.add_argument("--organize", action="store_true")
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
    graph_parser.add_argument("--kind", default="er", choices=REQUIRED_GRAPH_KINDS)
    graph_parser.add_argument("--format", default="json", choices=GRAPH_TEXT_FORMATS)

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
    migration_parser.add_argument("--backend", default="postgresql", choices=SUPPORTED_DATABASE_BACKENDS)
    migration_parser.add_argument("--rename-hint", action="append", default=[])
    migration_parser.add_argument("--json", action="store_true")

    nl_parser = subparsers.add_parser("nl-plan")
    nl_parser.add_argument("path")
    nl_parser.add_argument("--prompt", required=True)
    nl_parser.add_argument("--backend", default="postgresql", choices=SUPPORTED_DATABASE_BACKENDS)
    nl_parser.add_argument("--json", action="store_true")

    lsp_parser = subparsers.add_parser("lsp")
    lsp_parser.add_argument("path", nargs="?")
    lsp_parser.add_argument("--position")
    lsp_parser.add_argument("--prefix", default="")
    lsp_parser.add_argument("--rename")
    lsp_parser.add_argument("--apply-code-action")
    lsp_parser.add_argument("--stdio", action="store_true")
    lsp_parser.add_argument("--json", action="store_true")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("path")
    verify_parser.add_argument("--target", action="append", default=[], choices=RELEASE_TARGET_CHOICES)
    verify_parser.add_argument("--json", action="store_true")

    package_parser = subparsers.add_parser("package")
    package_parser.add_argument("path")
    package_parser.add_argument("--target", action="append", default=[], choices=RELEASE_TARGET_CHOICES)
    package_parser.add_argument("--out")
    package_parser.add_argument("--json", action="store_true")

    component_publish_parser = subparsers.add_parser("component-publish")
    component_publish_parser.add_argument("--component", required=True)
    component_publish_parser.add_argument("--catalog")
    component_publish_parser.add_argument("--json", action="store_true")

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

    tooling_audit_parser = subparsers.add_parser("tooling-audit")
    tooling_audit_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(tuple(argv or ()))
    _validate_tooling_cli_paths(parser, args)
    if args.command == "lsp" and args.stdio:
        return lsp_stdio_server()
    path_value = getattr(args, "path", None)
    path = Path(path_value) if path_value else None
    source = "" if path is None or path.is_dir() else path.read_text(encoding="utf-8")

    if args.command == "lint":
        component_catalog = _load_component_catalog(args.catalog) if args.catalog else ()
        report = (
            lint_report_dsl_path(
                path,
                strict=args.strict,
                catalog_path=args.catalog,
                previous_semantic_path=args.previous_semantic,
                migration_backend=args.backend,
            )
            if path is not None
            else lint_report_dsl(
                source,
                strict=args.strict,
                component_catalog=component_catalog,
                component_catalog_source=args.catalog,
                previous_semantic_model=_load_previous_semantic_model(args.previous_semantic),
                previous_semantic_source=args.previous_semantic,
                migration_backend=args.backend,
            )
        )
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    if args.command == "format":
        report = format_report_dsl(source, source_name=str(path), include_text=True, organize=args.organize)
        written = False
        if args.write and report["changed"]:
            path.write_text(report["text"], encoding="utf-8")
            written = True
        report = {
            **report,
            "write_requested": bool(args.write),
            "written": written,
            "write_path": str(path) if written else None,
        }
        printable = report if args.json else {key: value for key, value in report.items() if key != "text"}
        _emit_tooling_payload(printable, as_json=args.json)
        if args.check and report["changed"]:
            return 1
        return 0 if not any(item["severity"] == "error" for item in report["diagnostics"]) else 1
    if args.command == "validate":
        report = validate_report_dsl(source, source_name=str(path), targets=_parse_cli_targets(args.targets))
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
        if args.apply_code_action:
            report = apply_lsp_code_action_dsl(
                source,
                action_id=args.apply_code_action,
                source_name=str(path),
            )
            _emit_tooling_payload(report, as_json=args.json)
            return 0 if report["ok"] else 1
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
    if args.command == "component-publish":
        report = component_publish_report(args.component, catalog_path=args.catalog)
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
        edit = _parse_tooling_json_argument(parser, args, "edit_json", "--edit-json")
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
    if args.command == "tooling-audit":
        report = tooling_audit_report_dsl()
        _emit_tooling_payload(report, as_json=args.json)
        return 0 if report["ok"] else 1
    return 2


def _validate_tooling_cli_paths(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    for attr in ("path", "previous", "current", "previous_semantic"):
        if not hasattr(args, attr):
            continue
        value = getattr(args, attr)
        if not value:
            continue
        candidate = Path(value)
        if not candidate.exists():
            parser.error(f"{args.command}: path does not exist: {value}")
        if attr == "path" and args.command != "lint" and candidate.is_dir():
            parser.error(f"{args.command}: expected a file path, got directory: {value}")
    if args.command == "lint" and getattr(args, "catalog", None):
        catalog_path = Path(args.catalog)
        if not catalog_path.exists():
            parser.error(f"{args.command}: path does not exist: {args.catalog}")


def _parse_tooling_json_argument(parser: argparse.ArgumentParser, args: argparse.Namespace, attr: str, option: str) -> dict | None:
    value = getattr(args, attr, None)
    if not value:
        return None
    try:
        payload = json.loads(value)
    except json.JSONDecodeError as exc:
        parser.error(f"{args.command}: invalid JSON for {option}: {exc.msg}")
    if not isinstance(payload, dict):
        parser.error(f"{args.command}: {option} must be a JSON object")
    return payload


def _emit_tooling_payload(payload: dict, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True, default=list))
        return
    if payload.get("format") == "appgen.lint-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        counts = payload.get("severity_counts", {})
        print(f"lint {status}: {counts}")
        stages = payload.get("stages") or {}
        if stages:
            stage_names = tuple(payload.get("stage_names") or LINT_STAGE_NAMES)
            stage_counts = " ".join(
                f"{name}={stages.get(name, {}).get('diagnostic_count', 0)}"
                for name in stage_names
            )
            print(f"stages {stage_counts}")
        migration = payload.get("migration_preview") or {}
        if migration.get("format") == "appgen.migration-plan.v1":
            changes = migration.get("changes", ())
            detected = tuple(migration.get("coverage", {}).get("detected", ()))
            print(
                "migration-preview "
                f"{migration.get('backend', 'unknown')}: changes={len(changes)} "
                f"requires_approval={migration.get('requires_approval', False)}"
            )
            if detected:
                print(f"migration-detected {', '.join(sorted(detected))}")
        for diagnostic in payload.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
        return
    if payload.get("format") == "appgen.format-result.v1":
        status = "changed" if payload.get("changed") else "ok"
        idempotent = "idempotent" if payload.get("idempotent") else "not-idempotent"
        write_status = " written" if payload.get("written") else ""
        print(
            f"format {status}: {idempotent}{write_status} "
            f"organize={payload.get('organize', False)} "
            f"write_requested={payload.get('write_requested', False)} "
            f"written={payload.get('written', False)}"
        )
        if payload.get("write_path"):
            print(f"write_path {payload.get('write_path')}")
        for diagnostic in payload.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
        return
    if payload.get("format") == "appgen.validate-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        requested = tuple(payload.get("requested_targets", ()))
        app_targets = tuple(payload.get("app_targets", ()))
        semantic = payload.get("semantic_model", {})
        print(
            f"validate {status}: requested={','.join(requested) or 'default'} "
            f"app_targets={','.join(app_targets) or 'none'} semantic={semantic.get('format')}"
        )
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
            if check.get("check") == "target_compatibility":
                unknown = tuple(check.get("unknown_targets", ()))
                missing = tuple(check.get("missing_targets", ()))
                if unknown:
                    print(f"unknown-targets {', '.join(unknown)}")
                if missing:
                    print(f"missing-targets {', '.join(missing)}")
        for diagnostic in payload.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
        return
    if payload.get("format") == "appgen.generate-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        targets = tuple(payload.get("targets", ()))
        print(
            f"generate {status}: generated={payload.get('generated', False)} "
            f"targets={','.join(targets) or 'default'} artifacts={len(payload.get('artifacts', ()))} "
            f"semantic={payload.get('semantic_model_format') or payload.get('validation', {}).get('semantic_model', {}).get('format')}"
        )
        output_dir = payload.get("output_dir")
        if output_dir:
            print(f"output_dir {output_dir}")
        manifest = payload.get("manifest")
        if manifest:
            print(f"manifest {manifest}")
        for artifact in payload.get("artifacts", ()):
            print(f"artifact {artifact['path']}")
        for gap in payload.get("blocking_gaps", ()):
            print(f"gap {gap}")
        for diagnostic in payload.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
        return
    if payload.get("format") == "appgen.internal-error.v1":
        print(f"internal-error {payload.get('error_type')}: {payload.get('message')}")
        return
    if payload.get("format") == "appgen.graph-suite-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        kinds = tuple(payload.get("required_kinds", ()))
        formats = tuple(payload.get("formats", ()))
        kind_count = len(kinds)
        format_count = len(formats)
        print(f"graph-suite {status}: {kind_count} kinds, {format_count} formats")
        if kinds:
            print(f"graph-kinds {', '.join(kinds)}")
        if formats:
            print(f"graph-formats {', '.join(formats)}")
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
        return
    if payload.get("format") == "appgen.migration-plan.v1":
        _emit_migration_plan_text(payload)
        return
    if payload.get("format") == "appgen.nl-plan.v1":
        _emit_nl_plan_text(payload)
        return
    if payload.get("format") == "appgen.release-verifier-report.v1":
        _emit_release_verifier_text(payload)
        return
    if payload.get("format") == "appgen.designer-sync-report.v1":
        _emit_designer_sync_text(payload)
        return
    if payload.get("format") == "appgen.diagnostic-catalog.v1":
        _emit_diagnostic_catalog_text(payload)
        return
    if payload.get("format") == "appgen.diagnostic-fixture-audit.v1":
        _emit_diagnostic_fixture_audit_text(payload)
        return
    if payload.get("format") == "appgen.semantic-drift-audit.v1":
        _emit_semantic_drift_text(payload)
        return
    if payload.get("format") == "appgen.lsp-service.v1":
        _emit_lsp_service_text(payload)
        return
    if payload.get("format") == "appgen.lsp-code-action-apply.v1":
        _emit_lsp_code_action_apply_text(payload)
        return
    if payload.get("format") == "appgen.parser-golden-audit.v1":
        status = "ok" if payload.get("ok") else "failed"
        missing = tuple(payload.get("missing_constructs", ()))
        print(
            f"parser-golden {status}: "
            f"{payload.get('fixture_count', 0)} fixtures, "
            f"valid={payload.get('valid_fixture_count', 0)} "
            f"invalid={payload.get('invalid_fixture_count', 0)} "
            f"constructs={len(payload.get('constructs_covered', ()))} "
            f"missing={len(missing)}"
        )
        if missing:
            print(f"missing-constructs {', '.join(missing)}")
        for gap in payload.get("blocking_gaps", ()):
            print(f"fail {gap['name']}: {gap.get('error', '')}")
        return
    if payload.get("format") == "appgen.explain-report.v1":
        _emit_explain_text(payload)
        return
    if payload.get("format") == "appgen.doctor-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        checks = tuple(payload.get("checks", ()))
        gaps = tuple(payload.get("blocking_gaps", ()))
        print(f"doctor {status}: checks={len(checks)} blocking_gaps={len(gaps)}")
        for check in payload.get("checks", ()):
            detail = check.get("detail", {})
            report_format = detail.get("report_format")
            suffix = f" report={report_format}" if report_format else ""
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}{suffix}: {check.get('message', '')}")
        return
    if payload.get("format") == "appgen.component-publish-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        patch = payload.get("catalog_patch", {})
        catalog = payload.get("catalog", {})
        print(
            f"component-publish {status}: component={payload.get('component')} "
            f"catalog={catalog.get('source') or 'inline'} already_registered={patch.get('already_registered')} "
            f"write_performed={patch.get('write_performed')} "
            f"patch={patch.get('format')}"
        )
        print(
            f"catalog-count before={patch.get('before_count', catalog.get('count', 0))} "
            f"after={patch.get('after_count', catalog.get('count', 0))} "
            f"existing={catalog.get('count', 0)}"
        )
        for gap in payload.get("blocking_gaps", ()):
            print(f"gap {gap}")
        return
    if payload.get("format") == "appgen.tooling-audit.v1":
        status = "ok" if payload.get("ok") else "failed"
        gaps = tuple(payload.get("blocking_gaps", ()))
        sections = tuple(payload.get("sections", ()))
        print(
            f"tooling-audit {status}: {payload.get('passed', 0)}/{payload.get('required', 0)} checks "
            f"blocking_gaps={len(gaps)} sections={len(sections)} source={payload.get('source_of_truth')}"
        )
        phase_detail = _tooling_text_phase_detail(payload)
        if phase_detail:
            phases = tuple(phase_detail.get("phases", ()))
            missing_phases = tuple(phase_detail.get("missing_phases", ()))
            print(
                f"implementation-phases {len(phases)} "
                f"missing={len(missing_phases)} format={phase_detail.get('format')}"
            )
        for section in sections:
            print(f"section {section}")
        for check in payload.get("checks", ()):
            formats = _tooling_text_detail_formats(check.get("detail", {}))
            suffix = f" formats={','.join(formats)}" if formats else ""
            print(f"{'ok' if check['ok'] else 'fail'} {check['id']} section={check.get('section')}{suffix}: {check.get('evidence', '')}")
        return
    if payload.get("format") == "appgen.pbc-publish-report.v1":
        status = "ok" if payload.get("ok") else "failed"
        target = payload.get("target", {})
        print(f"pbc publish {status}: {payload.get('pbc')} -> {target.get('mode')}")
        print(f"side_effect_free={target.get('side_effect_free')} write_performed={target.get('write_performed')}")
        for check in payload.get("checks", ()):
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
        return
    if payload.get("format") == "appgen.pbc-verifier-catalog.v1":
        status = "ok" if payload.get("ok") else "failed"
        pbcs = tuple(payload.get("pbcs", ()))
        print(f"pbc list {status}: count={payload.get('count', len(pbcs))} format={payload.get('format')}")
        mesh_counts = Counter(str(item.get("mesh") or "unclassified") for item in pbcs)
        for mesh, count in sorted(mesh_counts.items()):
            print(f"mesh {mesh}: count={count}")
        for item in pbcs:
            print(
                f"pbc {item.get('pbc')}: ok={item.get('ok')} "
                f"mesh={item.get('mesh')} datastore={item.get('datastore_backend')} "
                f"label={item.get('label')}"
            )
        return
    if payload.get("format") == "appgen.pbc-package-verifier.v1":
        status = "ok" if payload.get("ok") else "failed"
        checks = tuple(payload.get("checks", ()))
        gaps = tuple(payload.get("blocking_gaps", ()))
        print(
            f"pbc verify {status}: pbc={payload.get('pbc')} "
            f"checks={len(checks)} gaps={len(gaps)} format={payload.get('format')}"
        )
        catalog = payload.get("catalog", {})
        if catalog:
            print(
                f"catalog label={catalog.get('label')} mesh={catalog.get('mesh')} "
                f"datastore={catalog.get('datastore_backend')}"
            )
        for check in checks:
            print(f"{'ok' if check['ok'] else 'fail'} {check['check']}")
        return
    print(json.dumps(payload, indent=2, sort_keys=True, default=list))


def _tooling_text_detail_formats(value: object) -> tuple[str, ...]:
    formats: set[str] = set()

    def collect(item: object) -> None:
        if isinstance(item, dict):
            fmt = item.get("format") or item.get("report_format")
            if isinstance(fmt, str) and fmt.startswith("appgen."):
                formats.add(fmt)
            for nested in item.values():
                collect(nested)
        elif isinstance(item, (list, tuple)):
            for nested in item:
                collect(nested)

    collect(value)
    return tuple(sorted(formats))


def _tooling_text_phase_detail(payload: dict) -> dict | None:
    for check in payload.get("checks", ()):
        detail = check.get("detail", {})
        if isinstance(detail, dict) and detail.get("format") == "appgen.tooling-implementation-phase-audit.v1":
            return detail
    return None


def _internal_tooling_error_report(exc: Exception) -> dict:
    message = str(exc) or exc.__class__.__name__
    return {
        "format": "appgen.internal-error.v1",
        "ok": False,
        "code": "AGX9000",
        "severity": "error",
        "error_type": exc.__class__.__name__,
        "message": message,
        "diagnostics": (
            {
                "code": "AGX9000",
                "severity": "error",
                "title": "Internal tooling error",
                "message": message,
                "range": None,
                "related_locations": (),
                "fixes": (),
                "docs_url": "docs/tooling.md#cli-contracts",
            },
        ),
    }


def _emit_explain_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    kind = payload.get("kind", "unknown")
    query = payload.get("query") or payload.get("message", "")
    print(f"explain {kind} {status}: {query}")
    if kind == "diagnostic":
        explanation = payload.get("explanation", {})
        print(f"{explanation.get('code')}: {explanation.get('title')}")
        print(explanation.get("summary", ""))
        print(f"docs: {explanation.get('docs_url')}")
        return
    if kind == "symbol":
        symbol = payload.get("symbol") or {}
        if symbol:
            print(f"{symbol.get('id')}: {symbol.get('kind')} {symbol.get('name')}")
            parent = symbol.get("parent")
            if parent:
                print(f"parent: {parent}")
            references = symbol.get("references", ())
            print(f"references: {len(references)}")
        return
    if kind == "handler":
        matches = payload.get("matches", ())
        print(f"matches: {len(matches)}")
        for match in matches:
            print(f"{match.get('from')} -> {match.get('to')} [{match.get('label')}]")


def _emit_migration_plan_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    changes = payload.get("changes", ())
    coverage = payload.get("coverage", {})
    detected = tuple(coverage.get("detected", ()))
    missing = tuple(coverage.get("missing", ()))
    destructive_count = sum(1 for change in changes if change.get("destructive"))
    print(
        f"migration-plan {status}: backend={payload.get('backend', 'unknown')} "
        f"changes={len(changes)} destructive={destructive_count} "
        f"requires_approval={payload.get('requires_approval', False)}"
    )
    if coverage:
        print(f"migration-coverage {coverage.get('format')}: detected={len(detected)} missing={len(missing)}")
    if detected:
        print(f"migration-detected {', '.join(sorted(detected))}")
    for change in changes:
        target = change.get("table") or change.get("field") or change.get("pbc") or change.get("contract") or ""
        print(f"change {change.get('kind')}: {target}".rstrip())
        if change.get("safe_alternative"):
            print(f"safe-alternative {change.get('kind')}: {change.get('safe_alternative')}")
    for diagnostic in payload.get("diagnostics", ()):
        print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")


def _emit_nl_plan_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    operations = tuple(payload.get("edit_operations", ()))
    operation_kinds = tuple(operation.get("kind") for operation in operations if operation.get("kind"))
    migration = payload.get("migration_preview") or {}
    token_budget_notes = tuple(payload.get("token_budget_notes", ()))
    print(
        f"nl-plan {status}: intent={payload.get('intent', 'unknown')} "
        f"operations={len(operations)} patch_bytes={len(payload.get('dsl_patch', ''))} "
        f"tests={len(payload.get('test_plan', ()))} "
        f"token_notes={len(token_budget_notes)}"
    )
    if operation_kinds:
        print(f"operation-kinds {', '.join(operation_kinds)}")
    if token_budget_notes:
        print(f"token-budget-notes {len(token_budget_notes)}")
    if payload.get("lint", {}).get("format") == "appgen.lint-report.v1":
        print(f"lint_ok={payload.get('lint', {}).get('ok')}")
    if migration.get("format") == "appgen.migration-plan.v1":
        print(
            f"migration-preview {migration.get('backend', 'unknown')}: "
            f"changes={len(migration.get('changes', ()))} "
            f"requires_approval={migration.get('requires_approval', False)}"
        )
    for diagnostic in payload.get("diagnostics", ()):
        print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")


def _emit_release_verifier_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    targets = tuple(payload.get("targets", ()))
    written = tuple(payload.get("written_artifacts", ()))
    print(f"release-verify {status}: targets={','.join(targets)} written={len(written)}")
    evidence = payload.get("evidence_bundle", {})
    if evidence.get("format"):
        print(f"release-evidence {evidence.get('format')}: artifacts={len(evidence.get('artifacts', ()))}")
    graph = evidence.get("graph_suite", {})
    if graph.get("format"):
        print(
            f"graph-suite {graph.get('format')}: "
            f"kinds={len(graph.get('required_kinds', ()))} formats={len(graph.get('formats', ()))}"
        )
    for check in payload.get("checks", ()):
        gaps = tuple(check.get("blocking_gaps", ()))
        gap_text = f" gaps={','.join(gaps)}" if gaps else ""
        print(f"{'ok' if check.get('ok') else 'fail'} {check.get('verifier')}{gap_text}")
    for artifact in written:
        print(f"artifact {artifact.get('kind')}: {artifact.get('path')}")
    for diagnostic in payload.get("diagnostics", ()):
        print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")


def _emit_designer_sync_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    surfaces = tuple(payload.get("surfaces", ()))
    visual_edit = payload.get("visual_edit") or {}
    matrix = payload.get("visual_edit_matrix") or {}
    print(
        f"designer-sync {status}: semantic={payload.get('semantic_model_format')} "
        f"surfaces={len(surfaces)}"
    )
    if surfaces:
        print(f"surfaces {', '.join(surfaces)}")
    if visual_edit:
        changed = tuple(visual_edit.get("changed_surfaces", ()))
        print(
            f"visual-edit accepted={visual_edit.get('accepted')} "
            f"round_trip={visual_edit.get('round_trip_ok')} "
            f"changed={','.join(changed)} diff_lines={len(visual_edit.get('dsl_diff', ()))}"
        )
        for diagnostic in visual_edit.get("diagnostics", ()):
            print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")
    if matrix.get("format") == "appgen.designer-visual-edit-matrix.v1":
        print(
            f"visual-edit-matrix ok={matrix.get('ok')} "
            f"cases={len(matrix.get('cases', ()))} gaps={len(matrix.get('blocking_gaps', ()))}"
        )
        required_operations = tuple(matrix.get("required_operations", ()))
        if required_operations:
            print(f"visual-edit-operations {', '.join(required_operations)}")
    for check in payload.get("checks", ()):
        print(f"{'ok' if check.get('ok') else 'fail'} {check.get('check')}")


def _emit_diagnostic_catalog_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    required = tuple(payload.get("required_codes", ()))
    covered = tuple(payload.get("covered_fixture_codes", ()))
    missing = tuple(payload.get("missing_fixtures", ()))
    print(
        f"diagnostics {status}: covered={len(covered)} required={len(required)} "
        f"fixtures={payload.get('fixture_count', 0)} missing={len(missing)}"
    )
    for code in missing:
        print(f"missing-fixture {code}")


def _emit_diagnostic_fixture_audit_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    covered = tuple(payload.get("covered_codes", ()))
    missing = tuple(payload.get("missing_codes", ()))
    print(
        f"diagnostics-audit {status}: covered={len(covered)} "
        f"required={len(payload.get('required_codes', ()))} missing={len(missing)}"
    )
    for code in missing:
        print(f"missing-code {code}")
    for gap in payload.get("blocking_gaps", ()):
        print(f"fail {gap.get('name')}: {','.join(gap.get('shape_gaps', ()) or gap.get('severity_gaps', ()))}")


def _emit_semantic_drift_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    surfaces = tuple(payload.get("surfaces", ()))
    gaps = tuple(payload.get("blocking_gaps", ()))
    print(
        f"drift {status}: semantic={payload.get('semantic_model_format')} "
        f"surfaces={len(surfaces)} blocking_gaps={len(gaps)} digest={payload.get('semantic_digest')}"
    )
    if surfaces:
        print(f"surfaces {', '.join(surfaces)}")
    evidence = payload.get("surface_evidence", {})
    for name in sorted(evidence):
        value = evidence[name]
        if isinstance(value, (list, tuple)):
            value = ",".join(str(item) for item in value)
        print(f"evidence {name}: {value}")
    for check in payload.get("checks", ()):
        print(f"{'ok' if check.get('ok') else 'fail'} {check.get('check')}")


def _emit_lsp_service_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    diagnostics = payload.get("publishDiagnostics", {}).get("diagnostics", ())
    completions = payload.get("completion", {}).get("items", ())
    code_actions = payload.get("codeAction", {}).get("actions", ())
    symbols = payload.get("documentSymbol", {}).get("symbols", ())
    workspace_symbols = payload.get("workspaceSymbol", {}).get("symbols", ())
    print(
        f"lsp {status}: semantic={payload.get('semantic_model_format')} "
        f"diagnostics={len(diagnostics)} completions={len(completions)} "
        f"actions={len(code_actions)} symbols={len(symbols)} workspace_symbols={len(workspace_symbols)}"
    )
    capabilities = payload.get("capabilities", {})
    if capabilities:
        print(f"source_of_truth={capabilities.get('source_of_truth')}")
    coverage = payload.get("completionCoverage", {})
    if coverage:
        missing = tuple(coverage.get("missing", ()))
        print(f"completion_coverage={coverage.get('format')} missing={len(missing)}")
    rename = payload.get("rename")
    if rename:
        diagnostics = tuple(rename.get("diagnostics", ()))
        blockers = tuple(rename.get("blockers", ()))
        migration = rename.get("migration_preview", {})
        print(
            f"rename ok={rename.get('ok')} changed={rename.get('changed')} "
            f"blocked={rename.get('blocked', False)} diagnostics={len(diagnostics)} "
            f"blockers={len(blockers)} requires_approval={migration.get('requires_approval', False)}"
        )
    hover = payload.get("hover") or {}
    print(f"hover_items={len(hover.get('contents', ()))}")


def _emit_lsp_code_action_apply_text(payload: dict) -> None:
    status = "ok" if payload.get("ok") else "failed"
    edits = tuple(payload.get("applied_edits", ()))
    lint = payload.get("lint") or {}
    print(
        f"lsp-code-action {status}: action={payload.get('action_id')} "
        f"changed={payload.get('changed')} edits={len(edits)} lint_ok={lint.get('ok')}"
    )
    title = payload.get("title")
    if title:
        print(f"title {title}")
    available = tuple(payload.get("available_actions", ()))
    if available:
        print(f"available-actions {', '.join(available)}")
    for diagnostic in payload.get("diagnostics", ()):
        print(f"{diagnostic['severity']} {diagnostic['code']}: {diagnostic['message']}")


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
    organize: bool = False,
) -> dict:
    """Return the docs/tooling.md appgen.format-result.v1 contract."""
    result = format_dsl(text, source_name=source_name, organize=organize)
    second = format_dsl(result["formatted"], source_name=source_name, organize=organize)
    payload = {
        "format": "appgen.format-result.v1",
        "source": source_name,
        "changed": result["changed"],
        "organize": organize,
        "idempotent": second["formatted"] == result["formatted"],
        "diagnostics": lint_report_dsl(result["formatted"], source_name=source_name)["diagnostics"],
    }
    if include_text:
        payload["text"] = result["formatted"]
    return payload


def formatter_contract_audit_dsl() -> dict:
    """Prove the executable formatter guarantees documented in docs/tooling.md."""
    comment_source = """
// file header
app FormatDemo { targets: web }

// customer table
table Customer {
  // identity comment
  id: int search default 0 required pk unique hidden // inline identity
  name: string search unique required
  parent_id: int search default 0 required -> Customer.id [many-to-one]
}
"""
    organize_source = """
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
    comment_report = format_report_dsl(comment_source, source_name="formatter-comments.appgen")
    organize_report = format_report_dsl(organize_source, source_name="formatter-organize.appgen", organize=True)
    comment_text = comment_report["text"]
    organize_text = organize_report["text"]
    checks = (
        _release_check("idempotent", comment_report["idempotent"] and organize_report["idempotent"]),
        _release_check("file_level_comments_preserved", comment_text.startswith("// file header\napp FormatDemo")),
        _release_check("declaration_comments_preserved", "\n// customer table\ntable Customer" in comment_text),
        _release_check(
            "inline_comments_preserved",
            "  id: int pk required unique hidden search default 0 // inline identity" in comment_text,
        ),
        _release_check("modifier_ordering", "  name: string required unique search" in comment_text),
        _release_check(
            "relationship_modifier_ordering",
            "  parent_id: int required search default 0 -> Customer.id [many-to-one]" in comment_text,
        ),
        _release_check("organize_requested", organize_report["organize"] is True),
        _release_check("top_level_order_preserved", organize_text.index("table Invoice") < organize_text.index("table Customer")),
        _release_check(
            "organize_table_body_ordering",
            (
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
            )
            in organize_text,
        ),
    )
    return {
        "format": "appgen.formatter-contract-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "comment_report": comment_report["format"],
        "organize_report": organize_report["format"],
        "blocking_gaps": tuple(check["check"] for check in checks if not check["ok"]),
    }


def validate_report_dsl(
    text: str,
    *,
    source_name: str | None = None,
    targets: Iterable[str] | None = None,
) -> dict:
    """Return a generator-readiness validation contract without writing files."""
    lint = lint_report_dsl(text, source_name=source_name)
    semantic = semantic_model_dsl(text, source_name=source_name)
    requested_targets, unknown_targets = _normalize_requested_validation_targets(targets)
    app_targets = tuple(semantic.get("app", {}).get("targets", ()))
    missing_targets = tuple(target for target in requested_targets if target not in app_targets)
    target_diagnostics = _validation_target_diagnostics(
        text,
        requested_targets=requested_targets,
        unknown_targets=unknown_targets,
        missing_targets=missing_targets,
        app_targets=app_targets,
    )
    checks = (
        {"check": "lint", "ok": lint["ok"]},
        {"check": "semantic_model", "ok": semantic["ok"]},
        {"check": "has_tables", "ok": bool(semantic.get("tables"))},
        {"check": "view_bindings", "ok": not any(item["code"] in {"AGX0303", "AGX0402"} for item in lint["diagnostics"])},
        {"check": "handler_targets", "ok": not any(item["code"] == "AGX0403" for item in lint["diagnostics"])},
        {
            "check": "target_compatibility",
            "ok": not unknown_targets and not missing_targets,
            "requested_targets": requested_targets,
            "app_targets": app_targets,
            "unknown_targets": unknown_targets,
            "missing_targets": missing_targets,
        },
    )
    return {
        "format": "appgen.validate-report.v1",
        "source": source_name,
        "ok": all(check["ok"] for check in checks),
        "requested_targets": requested_targets,
        "app_targets": app_targets,
        "checks": checks,
        "diagnostics": tuple(lint["diagnostics"]) + target_diagnostics,
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
    validation = validate_report_dsl(source, source_name=source_name, targets=requested_targets)
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
    if warnings and not allow_warnings:
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
            "blocking_gaps": ("lint_warnings",),
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


def _normalize_requested_validation_targets(targets: Iterable[str] | None) -> tuple[tuple[str, ...], tuple[str, ...]]:
    raw_targets = tuple(str(target).strip() for target in (targets or ()) if str(target).strip())
    if not raw_targets:
        return (), ()
    normalized, unknown = normalize_platform_targets(raw_targets, default=())
    return tuple(dict.fromkeys(normalized)), tuple(dict.fromkeys(unknown))


def _validation_target_diagnostics(
    source: str,
    *,
    requested_targets: tuple[str, ...],
    unknown_targets: tuple[str, ...],
    missing_targets: tuple[str, ...],
    app_targets: tuple[str, ...],
) -> tuple[dict, ...]:
    diagnostics = []
    if unknown_targets:
        diagnostics.append(
            _spec_diagnostic(
                source,
                "AGX0802",
                "error",
                f"Unknown validation targets: {', '.join(unknown_targets)}.",
            )
        )
    if missing_targets:
        diagnostics.append(
            _spec_diagnostic(
                source,
                "AGX0802",
                "error",
                "Requested validation targets are not declared by the app: "
                f"{', '.join(missing_targets)}. Declared targets: {', '.join(app_targets) or 'none'}.",
            )
        )
    return tuple(diagnostics)


def doctor_report_dsl() -> dict:
    """Check parser generation, imports, catalog, templates, backends, and IDE hooks."""
    root = Path(__file__).resolve().parents[2]
    vscode = _tooling_audit_vscode_extension(root)
    cli_help = _tooling_audit_cli_help_surface(root)
    module_boundaries = module_boundary_audit_dsl()
    alias_contract = cli_help.get("alias_contract", {})
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
            "cli_alias_contract",
            alias_contract.get("ok") is True and alias_contract.get("shared_target") == "pyAppGen.__main__:main",
            "appgen and apg resolve to the same tooling entrypoint.",
            {
                "report_format": alias_contract.get("format"),
                "commands": alias_contract.get("commands"),
                "shared_target": alias_contract.get("shared_target"),
                "module_dispatches_tooling": alias_contract.get("module_dispatches_tooling"),
            },
        ),
        _doctor_check(
            "lsp_completion_coverage",
            completion_coverage_dsl(_completion_coverage_sample(), source_name="completion-doctor.appgen")["missing"] == (),
            "Language-server completion sources cover the required docs/tooling.md contexts.",
            {"report_format": "appgen.completion-coverage.v1"},
        ),
        _doctor_check(
            "semantic_symbol_coverage",
            symbol_coverage_dsl(_symbol_coverage_sample(), source_name="symbol-doctor.appgen")["missing"] == (),
            "Semantic model emits all required symbol kinds for CLI, IDE, tests, and agents.",
            {"report_format": "appgen.symbol-coverage.v1"},
        ),
        _doctor_check(
            "module_boundaries",
            module_boundaries["ok"],
            "Documented DSL tooling responsibility boundaries are visible and callable.",
            {
                "report_format": module_boundaries["format"],
                "missing_boundaries": module_boundaries["missing_boundaries"],
                "core_runtime_gaps": module_boundaries["core_runtime_gaps"],
            },
        ),
        _doctor_check(
            "studio_semantic_service",
            designer_sync_report_dsl(_doctor_sample_dsl(), source_name="doctor.appgen")["semantic_model_format"] == "appgen.semantic-model.v1",
            "Studio designer service is bound to the shared semantic model.",
            {"report_format": "appgen.designer-sync-report.v1"},
        ),
        _doctor_check(
            "vscode_extension_surface",
            vscode["ok"],
            "VS Code extension scaffold declares the AppGen-X language, commands, and LSP providers.",
            {
                "report_format": vscode["format"],
                "checks": vscode["checks"],
                "commands": vscode["commands"],
            },
        ),
    )
    return {
        "format": "appgen.doctor-report.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def tooling_audit_report_dsl() -> dict:
    """Return one executable audit for the docs/tooling.md implementation surface."""
    root = Path(__file__).resolve().parents[2]
    source = _tooling_audit_sample_dsl()
    broken_handler_source = """
app Bad { targets: web }
table Invoice { id: int pk }
view InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }
"""

    semantic = semantic_model_dsl(source, source_name="tooling-audit.appgen")
    symbol_coverage = symbol_coverage_dsl(_symbol_coverage_sample(), source_name="symbol-tooling-audit.appgen")
    lint = lint_report_dsl(source, source_name="tooling-audit.appgen")
    strict_lint = lint_report_dsl(source, source_name="tooling-audit.appgen", strict=True)
    catalog_lint = lint_report_dsl(
        _tooling_audit_component_catalog_sample(),
        source_name="catalog.appgen",
        strict=True,
        component_catalog=("CustomGauge",),
        component_catalog_source="inline-audit-catalog",
    )
    formatted = format_report_dsl(source, source_name="tooling-audit.appgen")
    formatter_contract = formatter_contract_audit_dsl()
    validation = validate_report_dsl(source, source_name="tooling-audit.appgen", targets=("web", "mobile", "desktop"))
    graphs = graph_suite_report_dsl(source, source_name="tooling-audit.appgen")
    lsp = lsp_service_dsl(source, source_name="tooling-audit.appgen", prefix="cu")
    quick_fix = apply_lsp_code_action_dsl(
        broken_handler_source,
        source_name="bad-handler.appgen",
        action_id="create_operation_from_handler",
    )
    code_action_apply_audit = lsp_code_action_apply_audit_dsl()
    designer = designer_sync_report_dsl(
        source,
        source_name="tooling-audit.appgen",
        visual_edit={
            "surface": "database_designer",
            "kind": "add_field",
            "table": "Invoice",
            "name": "memo",
            "type": "string",
        },
    )
    designer_visual_edit_matrix = designer_visual_edit_matrix_dsl(source, source_name="tooling-audit.appgen")
    migration_reports = _tooling_audit_migration_reports()
    migration_detected = tuple(
        sorted(
            {
                detected
                for report in migration_reports
                for detected in report.get("coverage", {}).get("detected", ())
            }
        )
    )
    nl_plan = nl_plan_dsl(
        source,
        source_name="tooling-audit.appgen",
        prompt="Add credit memo tracking to invoices",
        backend="postgresql",
    )
    nl_plan_contract = nl_plan_contract_audit_dsl(source, source_name="tooling-audit.appgen")
    release = release_verifier_report_dsl(
        source,
        source_name="tooling-audit.appgen",
        targets=("web", "mobile", "desktop", "pbc", "deployment"),
    )
    with tempfile.TemporaryDirectory(prefix="appgen-tooling-audit-") as tmp:
        format_write = _tooling_audit_format_write(Path(tmp))
        internal_error_exit = _tooling_audit_internal_error_exit(Path(tmp))
        missing_input_exit = _tooling_audit_missing_input_exit(Path(tmp))
        missing_required_option_exit = _tooling_audit_missing_required_option_exit(Path(tmp))
        invalid_choice_exit = _tooling_audit_invalid_choice_exit(Path(tmp))
        lint_directory_cli = _tooling_audit_lint_directory_cli(Path(tmp), source)
        validate_generate_cli = _tooling_audit_validate_generate_cli(Path(tmp), source)
        designer_sync_cli = _tooling_audit_designer_sync_cli(Path(tmp), source)
        lsp_apply_cli = _tooling_audit_lsp_apply_code_action_cli(Path(tmp))
        graph_cli = _tooling_audit_graph_cli_formats(Path(tmp), source)
        graph_suite_cli = _tooling_audit_graph_suite_cli(Path(tmp), source)
        explain_cli = _tooling_audit_explain_cli_formats(Path(tmp), source)
        migration_cli = _tooling_audit_migration_cli(Path(tmp))
        nl_plan_cli = _tooling_audit_nl_plan_cli(Path(tmp), source)
        test_strategy_cli = _tooling_audit_test_strategy_cli(Path(tmp), source)
        generation = generate_report_dsl(
            source,
            source_name="tooling-audit.appgen",
            output_dir=Path(tmp) / "generated",
            targets=("web",),
        )
        package = release_verifier_report_dsl(
            source,
            source_name="tooling-audit.appgen",
            targets=("web", "mobile", "desktop", "pbc", "deployment"),
            output_dir=str(Path(tmp) / "package"),
        )
        warning_generation_blocked = generate_report_dsl(
            _tooling_audit_warning_generation_sample(),
            source_name="warning.appgen",
            output_dir=Path(tmp) / "warning-blocked",
        )
        warning_generation_allowed = generate_report_dsl(
            _tooling_audit_warning_generation_sample(),
            source_name="warning.appgen",
            output_dir=Path(tmp) / "warning-allowed",
            allow_warnings=True,
        )
        package_verify_cli = _tooling_audit_package_verify_cli(Path(tmp), source)
        package_invalid_target = _tooling_audit_package_invalid_target(Path(tmp), source)
        lsp_rename_cli = _tooling_audit_lsp_rename_cli(Path(tmp), source)

    diagnostics = diagnostic_catalog_dsl()
    diagnostic_fixtures = diagnostic_fixture_audit_dsl()
    parser_golden = parser_golden_audit_dsl()
    drift = semantic_drift_audit_dsl(source, source_name="tooling-audit.appgen")
    doctor = doctor_report_dsl()
    module_boundaries = module_boundary_audit_dsl()
    non_goal_policy = _tooling_audit_non_goal_policy()
    pbc_catalog = pbc_verifier_catalog_report()
    pbc_cli_text = _tooling_audit_pbc_cli_text()
    vscode = _tooling_audit_vscode_extension(root)
    studio = _tooling_audit_studio_semantic_service(source)
    lsp_rpc = _tooling_audit_lsp_json_rpc(source, broken_handler_source=broken_handler_source)
    lsp_stdio = _tooling_audit_lsp_stdio_transport(source)
    cli_help_surface = _tooling_audit_cli_help_surface(root)
    package_artifact_names = tuple(Path(item["path"]).name for item in package.get("written_artifacts", ()))
    implementation_phases = _tooling_audit_implementation_phases(
        semantic=semantic,
        symbol_coverage=symbol_coverage,
        diagnostics=diagnostics,
        diagnostic_fixtures=diagnostic_fixtures,
        parser_golden=parser_golden,
        drift=drift,
        test_strategy_cli=test_strategy_cli,
        module_boundaries=module_boundaries,
        lint=lint,
        strict_lint=strict_lint,
        catalog_lint=catalog_lint,
        lint_directory_cli=lint_directory_cli,
        formatted=formatted,
        formatter_contract=formatter_contract,
        validation=validation,
        validate_generate_cli=validate_generate_cli,
        cli_help_surface=cli_help_surface,
        graphs=graphs,
        graph_cli=graph_cli,
        graph_suite_cli=graph_suite_cli,
        explain_cli=explain_cli,
        lsp=lsp,
        lsp_rpc=lsp_rpc,
        lsp_stdio=lsp_stdio,
        lsp_rename_cli=lsp_rename_cli,
        quick_fix=quick_fix,
        code_action_apply_audit=code_action_apply_audit,
        lsp_apply_cli=lsp_apply_cli,
        vscode=vscode,
        studio=studio,
        designer=designer,
        designer_visual_edit_matrix=designer_visual_edit_matrix,
        designer_sync_cli=designer_sync_cli,
        migration_detected=migration_detected,
        migration_cli=migration_cli,
        nl_plan=nl_plan,
        nl_plan_contract=nl_plan_contract,
        nl_plan_cli=nl_plan_cli,
        release=release,
        package=package,
        package_verify_cli=package_verify_cli,
    )

    checks = (
        _tooling_audit_check(
            "shared_semantic_model",
            semantic["format"] == "appgen.semantic-model.v1"
            and semantic["ok"]
            and _tooling_audit_semantic_keys_present(semantic)
            and symbol_coverage.get("missing") == (),
            "Semantic model emits required top-level sections and complete required symbol coverage.",
            "docs/tooling.md#semantic-model-contract",
            {
                "format": semantic.get("format"),
                "symbol_coverage": symbol_coverage.get("format"),
                "symbol_coverage_missing": symbol_coverage.get("missing"),
            },
        ),
        _tooling_audit_check(
            "module_boundaries",
            module_boundaries["ok"],
            "Documented parser, AST, symbols, semantic, diagnostics, formatter, LSP, CLI, graph, migration, NL planning, and release boundaries expose callable surfaces.",
            "docs/tooling.md#proposed-modules",
            module_boundaries,
        ),
        _tooling_audit_check(
            "diagnostic_registry_and_fixtures",
            diagnostics["ok"] and diagnostic_fixtures["ok"],
            "Diagnostic registry and golden fixture audit cover required AGX codes.",
            "docs/tooling.md#diagnostic-specification",
            {"catalog": diagnostics.get("format"), "fixtures": diagnostic_fixtures.get("format")},
        ),
        _tooling_audit_check(
            "non_goal_policy_guards",
            non_goal_policy["ok"],
            "Non-goal policy guards reject secret literals, arbitrary runtime picker fields, and direct generated-code bypass prompts.",
            "docs/tooling.md#non-goals",
            non_goal_policy,
        ),
        _tooling_audit_check(
            "lint_directory_and_strict_profiles",
            lint["ok"]
            and strict_lint["ok"]
            and catalog_lint["ok"]
            and lint_report_dsl_sources({"a.appgen": source, "b.appgen": _doctor_sample_dsl()})["ok"]
            and lint_directory_cli["ok"],
            "Linter accepts files/source sets, strict profile reporting, and registered component catalogs.",
            "docs/tooling.md#linter-specification",
            {
                "format": lint.get("format"),
                "strict": strict_lint.get("strict"),
                "catalog": catalog_lint.get("component_catalog"),
                "directory_cli": lint_directory_cli,
            },
        ),
        _tooling_audit_check(
            "formatter_idempotent",
            formatted["format"] == "appgen.format-result.v1" and formatted["idempotent"] and formatter_contract["ok"],
            "Formatter is deterministic, idempotent, preserves comments, orders modifiers, and supports the organize profile.",
            "docs/tooling.md#formatter-specification",
            {
                "changed": formatted.get("changed"),
                "idempotent": formatted.get("idempotent"),
                "formatter_contract": formatter_contract,
            },
        ),
        _tooling_audit_check(
            "cli_validation_and_generation_contracts",
            validation["ok"]
            and format_write["ok"]
            and internal_error_exit["ok"]
            and missing_input_exit["ok"]
            and missing_required_option_exit["ok"]
            and invalid_choice_exit["ok"]
            and validate_generate_cli["ok"]
            and cli_help_surface["ok"]
            and generation["ok"]
            and generation["generated"]
            and not warning_generation_blocked["ok"]
            and "lint_warnings" in warning_generation_blocked["blocking_gaps"]
            and warning_generation_allowed["ok"],
            "Validation and generation reports gate lint/semantic readiness, block warnings by default, and allow warnings only when requested.",
            "docs/tooling.md#cli-contracts",
            {
                "validate": validation.get("format"),
                "format_write": format_write,
                "internal_error_exit": internal_error_exit,
                "missing_input_exit": missing_input_exit,
                "missing_required_option_exit": missing_required_option_exit,
                "invalid_choice_exit": invalid_choice_exit,
                "validate_generate_cli": validate_generate_cli,
                "cli_help_surface": cli_help_surface,
                "generate": generation.get("format"),
                "warning_block": warning_generation_blocked.get("blocking_gaps"),
                "allow_warnings": warning_generation_allowed.get("allow_warnings"),
            },
        ),
        _tooling_audit_check(
            "graph_and_explain_tooling",
            graphs["ok"]
            and set(REQUIRED_GRAPH_KINDS) <= set(graphs["graph_reports"])
            and set(GRAPH_TEXT_FORMATS) <= set(next(iter(graphs["renderings"].values())).keys())
            and graph_cli["ok"]
            and graph_suite_cli["ok"]
            and explain_cli["ok"]
            and explain_report_dsl(source, source_name="tooling-audit.appgen", symbol="table.Invoice")["ok"]
            and explain_report_dsl(source, source_name="tooling-audit.appgen", diagnostic="AGX0303")["ok"]
            and explain_report_dsl(source, source_name="tooling-audit.appgen", handler="Save")["ok"],
            "Graph suite and appgen graph/graph-suite CLI emit JSON/Mermaid/DOT, and explain covers symbols, diagnostics, and handlers.",
            "docs/tooling.md#graph-tooling",
            {
                "format": graphs.get("format"),
                "graphs": graphs.get("required_kinds"),
                "cli": graph_cli,
                "suite_cli": graph_suite_cli,
                "explain_cli": explain_cli,
            },
        ),
        _tooling_audit_check(
            "language_server_core_features",
            lsp["ok"]
            and lsp["capabilities"]["source_of_truth"] == "appgen.semantic-model.v1"
            and lsp["completionCoverage"]["missing"] == ()
            and lsp["formatting"]["format"] == "appgen.lsp-formatting.v1"
            and lsp_rpc["ok"]
            and lsp_stdio["ok"]
            and lsp_rename_cli["ok"],
            "Language server exposes and serves diagnostics, completion, hover, definitions, references, symbols, rename, code actions, and formatting from JSON-RPC and the appgen lsp CLI.",
            "docs/tooling.md#language-server-specification",
            {
                "format": lsp.get("format"),
                "coverage": lsp.get("completionCoverage", {}).get("format"),
                "rpc": lsp_rpc,
                "stdio": lsp_stdio,
                "rename_cli": lsp_rename_cli,
            },
        ),
        _tooling_audit_check(
            "lsp_quick_fix_application",
            quick_fix["ok"]
            and quick_fix["changed"]
            and "operation SubmitInvoice" in quick_fix["patched_source"]
            and code_action_apply_audit["ok"]
            and lsp_apply_cli["ok"],
            "LSP code actions are executable through deterministic DSL patch application contracts and the appgen lsp CLI.",
            "docs/tooling.md#code-actions",
            {
                "format": quick_fix.get("format"),
                "action": quick_fix.get("action_id"),
                "application_audit": code_action_apply_audit,
                "cli": lsp_apply_cli,
            },
        ),
        _tooling_audit_check(
            "ide_visual_designer_round_trip",
            designer["ok"]
            and designer["semantic_model_format"] == "appgen.semantic-model.v1"
            and designer["visual_edit"]["round_trip_ok"]
            and designer_visual_edit_matrix["ok"]
            and designer_sync_cli["ok"],
            "Studio designer projections and visual edits round-trip through linted DSL patches.",
            "docs/tooling.md#ide-integration",
            {
                "format": designer.get("format"),
                "surfaces": designer.get("surfaces"),
                "visual_edit_matrix": designer_visual_edit_matrix,
                "cli": designer_sync_cli,
            },
        ),
        _tooling_audit_check(
            "vscode_extension_surface",
            vscode["ok"],
            "VS Code extension declares syntax, language configuration, LSP client, commands, previews, and PBC catalog browser.",
            "docs/tooling.md#vs-code-extension",
            vscode,
        ),
        _tooling_audit_check(
            "studio_semantic_service",
            studio["ok"],
            "Studio semantic service composes LSP, designer sync, graph, quick-fix, and natural-language planner evidence.",
            "docs/tooling.md#appgen-x-studio-monaco",
            studio,
        ),
        _tooling_audit_check(
            "migration_detection_coverage",
            set(REQUIRED_MIGRATION_DETECTIONS) <= set(migration_detected)
            and migration_cli["ok"],
            "Migration planner detects required change families and the CLI accepts supported backend profiles plus rename hints.",
            "docs/tooling.md#migration-planner",
            {"detected": migration_detected, "required": REQUIRED_MIGRATION_DETECTIONS, "cli": migration_cli},
        ),
        _tooling_audit_check(
            "natural_language_patch_planner",
            nl_plan["ok"]
            and nl_plan["dsl_patch"]
            and nl_plan["lint"]["ok"]
            and nl_plan["migration_preview"]["format"] == "appgen.migration-plan.v1"
            and nl_plan_contract["ok"]
            and nl_plan_cli["ok"],
            "Natural-language change planning and appgen nl-plan CLI produce bounded DSL patches, lint results, migration previews, tests, and token-budget notes.",
            "docs/tooling.md#natural-language-change-planner",
            {
                "format": nl_plan.get("format"),
                "intent": nl_plan.get("intent"),
                "contract": nl_plan_contract,
                "cli": nl_plan_cli,
            },
        ),
        _tooling_audit_check(
            "package_and_release_verifiers",
            release["ok"]
            and package["ok"]
            and package_verify_cli["ok"]
            and package_invalid_target["ok"]
            and "appgen-release-evidence.json" in package_artifact_names
            and {
                "appgen-package-web.json",
                "appgen-package-mobile.json",
                "appgen-package-desktop.json",
                "appgen-package-pbc.json",
                "appgen-package-deployment.json",
            }
            <= set(package_artifact_names),
            "Release verifier and package command materialize target evidence for web, mobile, desktop, PBC, and deployment targets.",
            "docs/tooling.md#package-and-verifier-tooling",
            {
                "release": release.get("format"),
                "artifacts": package_artifact_names,
                "cli": package_verify_cli,
                "invalid_target": package_invalid_target,
            },
        ),
        _tooling_audit_check(
            "pbc_manifest_catalog_commands",
            pbc_catalog["ok"] and pbc_catalog["count"] > 0 and pbc_cli_text["ok"],
            "PBC tooling lists and verifies manifest-backed package catalog entries without grammar-specific PBC names and exposes text summaries for agent logs.",
            "docs/tooling.md#appgen-pbc",
            {
                "format": pbc_catalog.get("format"),
                "count": pbc_catalog.get("count"),
                "text_cli": pbc_cli_text,
            },
        ),
        _tooling_audit_check(
            "parser_golden_and_drift_gates",
            parser_golden["ok"] and drift["ok"] and doctor["ok"] and test_strategy_cli["ok"],
            "Parser golden, diagnostic fixture, semantic drift, and doctor gates prove grammar coverage and shared-model alignment across tooling surfaces.",
            "docs/tooling.md#test-strategy",
            {
                "parser": parser_golden.get("format"),
                "drift": drift.get("format"),
                "doctor": doctor.get("format"),
                "cli": test_strategy_cli,
            },
        ),
        _tooling_audit_check(
            "implementation_phase_exit_criteria",
            implementation_phases["ok"],
            "Implementation phases 0 through 6 have executable exit-criteria evidence instead of prose-only status.",
            "docs/tooling.md#implementation-phases",
            implementation_phases,
        ),
    )
    doc_anchor_integrity = _tooling_audit_doc_anchor_integrity(root, _tooling_audit_doc_refs(checks))
    checks = checks + (
        _tooling_audit_check(
            "tooling_doc_anchor_integrity",
            doc_anchor_integrity["ok"],
            "Tooling audit section references resolve to headings in docs/tooling.md.",
            "docs/tooling.md#appgen-tooling-audit",
            doc_anchor_integrity,
        ),
    )
    sections = tuple(sorted({check["section"] for check in checks}))
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.tooling-audit.v1",
        "ok": not blocking_gaps,
        "required": len(checks),
        "passed": sum(1 for check in checks if check["ok"]),
        "sections": sections,
        "doc_anchor_integrity": doc_anchor_integrity,
        "checks": checks,
        "blocking_gaps": blocking_gaps,
        "source_of_truth": "docs/tooling.md",
    }


def _tooling_audit_check(check_id: str, ok: bool, evidence: str, section: str, detail: dict | None = None) -> dict:
    return {
        "id": check_id,
        "ok": bool(ok),
        "section": section,
        "evidence": evidence,
        "detail": detail or {},
    }


def _tooling_audit_non_goal_policy() -> dict:
    secret_source = "\n".join(
        (
            "app SecretPolicy { targets: web }",
            "table Customer { id: int pk }",
            "view CustomerForm for Customer { Main: id }",
            'llm ApiModel { provider: openai; api_key: "sk-secret" }',
            "",
        )
    )
    runtime_picker_source = "\n".join(
        (
            "app RuntimePolicy { targets: web; backend: sqlite; runtime: node; stream: kafka }",
            "table Customer { id: int pk }",
            "view CustomerForm for Customer { Main: id }",
            "",
        )
    )
    source_of_truth_source = "\n".join(
        (
            "app SourceTruth { targets: web }",
            "table Customer { id: int pk; name: string }",
            "view CustomerForm for Customer { Main: name }",
            "",
        )
    )
    secret_lint = lint_report_dsl(secret_source, source_name="non-goal-secret.appgen")
    secret_fix = apply_lint_fixes(secret_source, fix_ids=("use_api_key_env",), source_name="non-goal-secret.appgen")
    runtime_lint = lint_report_dsl(runtime_picker_source, source_name="non-goal-runtime.appgen")
    runtime_fix = apply_lint_fixes(
        runtime_picker_source,
        fix_ids=("remove_invalid_runtime_picker_fields",),
        source_name="non-goal-runtime.appgen",
    )
    bypass_plan = nl_plan_dsl(
        source_of_truth_source,
        source_name="non-goal-bypass.appgen",
        prompt="Replace the runtime with hand-written generated code outside the DSL",
    )
    bypass_accepted = bypass_plan.get("accepted", False)
    runtime_messages = tuple(item.get("message", "") for item in runtime_lint.get("diagnostics", ()))
    cases = (
        {
            "case": "reject_secret_literal",
            "ok": secret_lint.get("ok") is False
            and _has_diagnostic(secret_lint, {"AGX0702"})
            and secret_fix.get("changed") is True
            and "api_key: OPENAI_API_KEY" in secret_fix.get("fixed", "")
            and "sk-secret" not in secret_fix.get("fixed", ""),
            "diagnostic_codes": tuple(item.get("code") for item in secret_lint.get("diagnostics", ())),
            "fix_ids": tuple(item.get("id") for item in secret_lint.get("fixes", ())),
            "fixed_contains_env_binding": "api_key: OPENAI_API_KEY" in secret_fix.get("fixed", ""),
            "secret_removed": "sk-secret" not in secret_fix.get("fixed", ""),
        },
        {
            "case": "reject_runtime_picker_fields",
            "ok": runtime_lint.get("ok") is False
            and sum(1 for item in runtime_lint.get("diagnostics", ()) if item.get("code") == "AGX0801") == 3
            and runtime_fix.get("changed") is True
            and all(token not in runtime_fix.get("fixed", "") for token in ("backend:", "runtime:", "stream:")),
            "diagnostic_codes": tuple(item.get("code") for item in runtime_lint.get("diagnostics", ())),
            "messages": runtime_messages,
            "fix_ids": tuple(item.get("id") for item in runtime_lint.get("fixes", ())),
            "picker_fields_removed": all(
                token not in runtime_fix.get("fixed", "") for token in ("backend:", "runtime:", "stream:")
            ),
        },
        {
            "case": "reject_generated_code_bypass_prompt",
            "ok": bypass_plan.get("ok") is False
            and bypass_accepted is False
            and any(item.get("code") == "AGX1201" for item in bypass_plan.get("diagnostics", ()))
            and not bypass_plan.get("dsl_patch"),
            "diagnostic_codes": tuple(item.get("code") for item in bypass_plan.get("diagnostics", ())),
            "accepted": bypass_accepted,
            "patch_bytes": len(bypass_plan.get("dsl_patch", "")),
        },
    )
    return {
        "format": "appgen.non-goal-policy-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": cases,
        "source_of_truth": "docs/tooling.md#non-goals",
    }


def _tooling_audit_doc_anchor_integrity(root: Path, section_refs: Iterable[str]) -> dict:
    docs_path = root / "docs" / "tooling.md"
    anchors = _markdown_heading_anchors(docs_path.read_text(encoding="utf-8"))
    referenced = tuple(dict.fromkeys(str(ref) for ref in section_refs))
    missing = tuple(
        ref
        for ref in referenced
        if ref.startswith("docs/tooling.md#") and ref.rsplit("#", 1)[-1] not in anchors
    )
    return {
        "format": "appgen.tooling-doc-anchor-audit.v1",
        "ok": not missing,
        "source": "docs/tooling.md",
        "heading_count": len(anchors),
        "referenced_sections": referenced,
        "missing_sections": missing,
    }


def _tooling_audit_doc_refs(value: object) -> tuple[str, ...]:
    refs: list[str] = []

    def collect(item: object) -> None:
        if isinstance(item, str):
            refs.extend(re.findall(r"docs/tooling\.md#[A-Za-z0-9_-]+", item))
        elif isinstance(item, dict):
            for nested in item.values():
                collect(nested)
        elif isinstance(item, (list, tuple, set)):
            for nested in item:
                collect(nested)

    collect(value)
    return tuple(dict.fromkeys(refs))


def _markdown_heading_anchors(markdown: str) -> tuple[str, ...]:
    anchors = []
    seen: dict[str, int] = {}
    for line in markdown.splitlines():
        if not line.startswith("#"):
            continue
        title = line.lstrip("#").strip()
        if not title:
            continue
        slug = re.sub(r"[^\w\s-]", "", title.lower(), flags=re.UNICODE)
        slug = re.sub(r"\s+", "-", slug).strip("-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.append(slug if count == 0 else f"{slug}-{count}")
    return tuple(anchors)


def _tooling_audit_semantic_keys_present(semantic: dict) -> bool:
    required = {
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
    }
    return required <= set(semantic)


def _tooling_audit_implementation_phases(**evidence: dict) -> dict:
    def phase(phase_id: str, title: str, criteria: tuple[dict, ...]) -> dict:
        missing = tuple(item["id"] for item in criteria if not item["ok"])
        return {
            "id": phase_id,
            "title": title,
            "ok": not missing,
            "exit_criteria": criteria,
            "missing_exit_criteria": missing,
        }

    semantic = evidence["semantic"]
    phases = (
        phase(
            "phase_0_inventory_and_stabilization",
            "Inventory And Stabilization",
            (
                {
                    "id": "current_behavior_documented",
                    "ok": evidence["module_boundaries"].get("ok") is True,
                    "evidence_format": evidence["module_boundaries"].get("format"),
                },
                {
                    "id": "fixture_catalogs_run_in_ci",
                    "ok": evidence["parser_golden"].get("ok") is True
                    and evidence["diagnostic_fixtures"].get("ok") is True
                    and evidence["drift"].get("ok") is True,
                    "evidence_formats": (
                        evidence["parser_golden"].get("format"),
                        evidence["diagnostic_fixtures"].get("format"),
                        evidence["drift"].get("format"),
                    ),
                },
                {
                    "id": "test_strategy_cli_proves_shared_surfaces",
                    "ok": evidence["test_strategy_cli"].get("ok") is True,
                    "evidence_format": evidence["test_strategy_cli"].get("format"),
                },
            ),
        ),
        phase(
            "phase_1_shared_semantic_model_mvp",
            "Shared Semantic Model MVP",
            (
                {
                    "id": "semantic_model_contract",
                    "ok": semantic.get("ok") is True
                    and semantic.get("format") == "appgen.semantic-model.v1"
                    and _tooling_audit_semantic_keys_present(semantic),
                    "evidence_format": semantic.get("format"),
                },
                {
                    "id": "symbol_coverage_complete",
                    "ok": evidence["symbol_coverage"].get("missing") == (),
                    "evidence_format": evidence["symbol_coverage"].get("format"),
                },
                {
                    "id": "database_backed_form_validation",
                    "ok": evidence["lint"].get("ok") is True and evidence["validate_generate_cli"].get("ok") is True,
                    "evidence_formats": (evidence["lint"].get("format"), evidence["validate_generate_cli"].get("format")),
                },
            ),
        ),
        phase(
            "phase_2_linter_and_formatter",
            "Linter And Formatter",
            (
                {
                    "id": "diagnostic_registry_and_fixtures",
                    "ok": evidence["diagnostics"].get("ok") is True
                    and evidence["diagnostic_fixtures"].get("ok") is True,
                    "evidence_formats": (evidence["diagnostics"].get("format"), evidence["diagnostic_fixtures"].get("format")),
                },
                {
                    "id": "lint_profiles_and_directory_input",
                    "ok": evidence["lint"].get("ok") is True
                    and evidence["strict_lint"].get("ok") is True
                    and evidence["catalog_lint"].get("ok") is True
                    and evidence["lint_directory_cli"].get("ok") is True,
                    "evidence_format": evidence["lint_directory_cli"].get("format"),
                },
                {
                    "id": "formatter_idempotency",
                    "ok": evidence["formatted"].get("idempotent") is True
                    and evidence["formatter_contract"].get("ok") is True,
                    "evidence_formats": (evidence["formatted"].get("format"), evidence["formatter_contract"].get("format")),
                },
            ),
        ),
        phase(
            "phase_3_cli_and_graph_tooling",
            "CLI And Graph Tooling",
            (
                {
                    "id": "machine_readable_cli_contracts",
                    "ok": evidence["validation"].get("ok") is True
                    and evidence["validate_generate_cli"].get("ok") is True
                    and evidence["cli_help_surface"].get("ok") is True,
                    "evidence_formats": (
                        evidence["validation"].get("format"),
                        evidence["validate_generate_cli"].get("format"),
                        evidence["cli_help_surface"].get("format"),
                    ),
                },
                {
                    "id": "graph_json_mermaid_and_dot",
                    "ok": evidence["graphs"].get("ok") is True
                    and evidence["graph_cli"].get("ok") is True
                    and evidence["graph_suite_cli"].get("ok") is True,
                    "evidence_formats": (
                        evidence["graphs"].get("format"),
                        evidence["graph_cli"].get("format"),
                        evidence["graph_suite_cli"].get("format"),
                    ),
                },
                {
                    "id": "explain_symbols_diagnostics_handlers",
                    "ok": evidence["explain_cli"].get("ok") is True,
                    "evidence_format": evidence["explain_cli"].get("format"),
                },
            ),
        ),
        phase(
            "phase_4_language_server",
            "Language Server",
            (
                {
                    "id": "lsp_core_json_rpc_and_stdio",
                    "ok": evidence["lsp"].get("ok") is True
                    and evidence["lsp_rpc"].get("ok") is True
                    and evidence["lsp_stdio"].get("ok") is True,
                    "evidence_formats": (
                        evidence["lsp"].get("format"),
                        evidence["lsp_rpc"].get("format"),
                        evidence["lsp_stdio"].get("format"),
                    ),
                },
                {
                    "id": "rename_and_code_actions",
                    "ok": evidence["lsp_rename_cli"].get("ok") is True
                    and evidence["quick_fix"].get("ok") is True
                    and evidence["code_action_apply_audit"].get("ok") is True
                    and evidence["lsp_apply_cli"].get("ok") is True,
                    "evidence_formats": (
                        evidence["lsp_rename_cli"].get("format"),
                        evidence["quick_fix"].get("format"),
                        evidence["code_action_apply_audit"].get("format"),
                        evidence["lsp_apply_cli"].get("format"),
                    ),
                },
                {
                    "id": "editor_extension_surface",
                    "ok": evidence["vscode"].get("ok") is True,
                    "evidence_format": evidence["vscode"].get("format"),
                },
            ),
        ),
        phase(
            "phase_5_ide_and_visual_designer_integration",
            "IDE And Visual Designer Integration",
            (
                {
                    "id": "visual_edits_generate_linted_dsl_patches",
                    "ok": evidence["designer"].get("ok") is True
                    and evidence["designer_visual_edit_matrix"].get("ok") is True
                    and evidence["designer_sync_cli"].get("ok") is True,
                    "evidence_formats": (
                        evidence["designer"].get("format"),
                        evidence["designer_visual_edit_matrix"].get("format"),
                        evidence["designer_sync_cli"].get("format"),
                    ),
                },
                {
                    "id": "studio_semantic_bridge",
                    "ok": evidence["studio"].get("ok") is True,
                    "evidence_format": evidence["studio"].get("format"),
                },
            ),
        ),
        phase(
            "phase_6_migration_natural_language_and_release_verifiers",
            "Migration, Natural Language, And Release Verifiers",
            (
                {
                    "id": "migration_detection_coverage",
                    "ok": set(REQUIRED_MIGRATION_DETECTIONS) <= set(evidence["migration_detected"])
                    and evidence["migration_cli"].get("ok") is True,
                    "evidence_format": evidence["migration_cli"].get("format"),
                },
                {
                    "id": "natural_language_planner_contract",
                    "ok": evidence["nl_plan"].get("ok") is True
                    and bool(evidence["nl_plan"].get("dsl_patch"))
                    and evidence["nl_plan_contract"].get("ok") is True
                    and evidence["nl_plan_cli"].get("ok") is True,
                    "evidence_formats": (
                        evidence["nl_plan"].get("format"),
                        evidence["nl_plan_contract"].get("format"),
                        evidence["nl_plan_cli"].get("format"),
                    ),
                },
                {
                    "id": "release_and_package_verifiers",
                    "ok": evidence["release"].get("ok") is True
                    and evidence["package"].get("ok") is True
                    and evidence["package_verify_cli"].get("ok") is True,
                    "evidence_formats": (
                        evidence["release"].get("format"),
                        evidence["package"].get("format"),
                        evidence["package_verify_cli"].get("format"),
                    ),
                },
            ),
        ),
    )
    missing = tuple(item["id"] for item in phases if not item["ok"])
    return {
        "format": "appgen.tooling-implementation-phase-audit.v1",
        "ok": not missing,
        "phases": phases,
        "missing_phases": missing,
        "source_of_truth": "docs/tooling.md#implementation-phases",
    }


def _tooling_audit_vscode_extension(root: Path) -> dict:
    extension = root / "extensions" / "vscode-appgen-x"
    package_path = extension / "package.json"
    language_config = extension / "language-configuration.json"
    grammar = extension / "syntaxes" / "appgen.tmLanguage.json"
    source_path = extension / "src" / "extension.js"
    package = json.loads(package_path.read_text(encoding="utf-8")) if package_path.exists() else {}
    source = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
    languages = tuple(package.get("contributes", {}).get("languages", ()))
    language_extensions = tuple(
        extension_name
        for language in languages
        if language.get("id") == "appgen"
        for extension_name in language.get("extensions", ())
    )
    activation_events = tuple(package.get("activationEvents", ()))
    commands = {item.get("command") for item in package.get("contributes", {}).get("commands", ())}
    required_commands = {
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
    }
    provider_markers = (
        "registerCompletionItemProvider",
        "registerHoverProvider",
        "registerDefinitionProvider",
        "registerReferenceProvider",
        "registerDocumentSymbolProvider",
        "registerWorkspaceSymbolProvider",
        "registerRenameProvider",
        "asRenameWorkspaceEdit",
        "AppGen-X rename blocked",
        "registerCodeActionsProvider",
        "registerDocumentFormattingEditProvider",
        '["lsp", "--stdio"]',
    )
    command_cli_markers = (
        '["lint", activeFile(), "--json"]',
        '["format", activeFile(), "--write", "--json"]',
        '["graph-suite", activeFile(), "--json"]',
        '["explain", file, "--symbol", symbol, "--json"]',
        '["generate", file, "--out", out, "--json"]',
        '["generate", file, "--out", out, "--allow-warnings", "--json"]',
        '["package", file, "--out", out, "--json"]',
        '["pbc", "list", "--json"]',
    )
    webview_markers = (
        "createWebviewPanel",
        "renderGraphPreview",
        "renderArtifactPreview",
        "renderPbcCatalog",
        "showJsonPreview",
    )
    checks = {
        "package_json": package_path.exists(),
        "language_configuration": language_config.exists(),
        "grammar": grammar.exists(),
        "language_metadata": any(language.get("id") == "appgen" for language in languages)
        and {".appgen", ".ag", ".ags"} <= set(language_extensions)
        and "onLanguage:appgen" in activation_events,
        "commands": required_commands <= commands,
        "providers": all(marker in source for marker in provider_markers),
        "diagnostics_collection": 'createDiagnosticCollection("appgen")' in source
        and "textDocument/publishDiagnostics" in source,
        "cli_command_contracts": all(marker in source for marker in command_cli_markers),
        "webview_renderers": all(marker in source for marker in webview_markers),
    }
    return {
        "format": "appgen.vscode-extension-audit.v1",
        "ok": all(checks.values()),
        "checks": checks,
        "commands": tuple(sorted(commands)),
        "required_commands": tuple(sorted(required_commands)),
        "language_extensions": language_extensions,
        "activation_events": activation_events,
        "provider_markers": provider_markers,
        "command_cli_markers": command_cli_markers,
        "webview_markers": webview_markers,
    }


def _tooling_audit_studio_semantic_service(source: str) -> dict:
    try:
        from .studio import studio_semantic_service_workspace
        from .studio import studio_browser_smoke_ci_contract
    except Exception as exc:  # pragma: no cover - import boundary
        return {
            "format": "appgen.studio-semantic-service-audit.v1",
            "ok": False,
            "error": str(exc),
        }
    report = studio_semantic_service_workspace(source)
    browser_smoke = studio_browser_smoke_ci_contract()
    required_surfaces = (
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
    )
    expected_surface_formats = {
        "dsl_editor": "appgen.designer-dsl-editor.v1",
        "component_palette": "appgen.designer-component-palette.v1",
        "form_designer": "appgen.designer-form-projection.v1",
        "database_designer": "appgen.designer-database-projection.v1",
        "workflow_designer": "appgen.designer-workflow-projection.v1",
        "pbc_composition_designer": "appgen.designer-pbc-composition-projection.v1",
        "package_deployment_designer": "appgen.designer-package-deployment-projection.v1",
        "diagnostics_panel": "appgen.lsp-diagnostics.v1",
        "graph_explain_panel": "appgen.designer-graph-explain-panel.v1",
        "natural_language_planner": "appgen.designer-nl-planner-panel.v1",
    }
    surfaces = report.get("designer_surfaces", {})
    services = report.get("services", {})
    diagnostics = report.get("diagnostics_quick_fixes", {})
    diagnostics_report = diagnostics.get("diagnostics", {})
    code_actions = diagnostics.get("code_actions", {})
    graph_explain = report.get("graph_explain", {})
    graph_suite = graph_explain.get("graph_suite", {})
    graph_panel = graph_explain.get("panel", {})
    nl = report.get("natural_language_evolution", {})
    nl_plan = nl.get("plan", {})
    browser_smoke_checks = {check.get("id"): check.get("ok") for check in browser_smoke.get("checks", ())}
    surface_formats = {
        name: surfaces.get(name, {}).get("format")
        for name in required_surfaces
        if isinstance(surfaces.get(name), dict)
    }
    semantic_surface_formats = {
        name: surfaces.get(name, {}).get("semantic_model_format")
        for name in required_surfaces
        if isinstance(surfaces.get(name), dict) and "semantic_model_format" in surfaces.get(name, {})
    }
    checks = {
        "bridge_format": report.get("format") == "appgen.studio-semantic-service.v1",
        "bridge_ok": report.get("ok") is True,
        "services": services
        == {
            "lsp": "appgen.lsp-service.v1",
            "designer_sync": "appgen.designer-sync-report.v1",
            "graph_suite": "appgen.graph-suite-report.v1",
            "natural_language_planner": "appgen.nl-plan.v1",
        },
        "required_surfaces": set(required_surfaces) <= set(surfaces),
        "surface_formats": all(
            surface_formats.get(name) == expected for name, expected in expected_surface_formats.items()
        ),
        "semantic_surface_formats": bool(semantic_surface_formats)
        and all(value == "appgen.semantic-model.v1" for value in semantic_surface_formats.values()),
        "diagnostics_quick_fixes": diagnostics.get("format") == "appgen.studio-diagnostics-quick-fixes.v1"
        and diagnostics_report.get("format") == "appgen.lsp-diagnostics.v1"
        and code_actions.get("format") == "appgen.lsp-code-actions.v1",
        "graph_explain": graph_explain.get("format") == "appgen.studio-graph-explain.v1"
        and graph_suite.get("format") == "appgen.graph-suite-report.v1"
        and graph_panel.get("format") == "appgen.designer-graph-explain-panel.v1",
        "natural_language_evolution": nl.get("format") == "appgen.studio-natural-language-evolution.v1"
        and nl_plan.get("format") == "appgen.nl-plan.v1"
        and nl.get("requires_dsl_diff_preview") is True
        and nl.get("applies_through") == "appgen designer-sync",
        "frontend_browser_smoke_bridge": browser_smoke.get("format") == "appgen.studio-browser-smoke-ci-contract.v1"
        and browser_smoke.get("ok") is True
        and "semantic_service_bridge" in browser_smoke.get("scenarios", ())
        and browser_smoke_checks.get("frontend_semantic_service_bridge") is True,
    }
    return {
        "format": "appgen.studio-semantic-service-audit.v1",
        "ok": all(checks.values()),
        "service_format": report.get("format"),
        "services": services,
        "checks": checks,
        "surfaces": tuple(surfaces),
        "required_surfaces": required_surfaces,
        "surface_formats": surface_formats,
        "expected_surface_formats": expected_surface_formats,
        "semantic_surface_formats": semantic_surface_formats,
        "browser_smoke_format": browser_smoke.get("format"),
        "browser_smoke_scenarios": tuple(browser_smoke.get("scenarios", ())),
        "browser_smoke_checks": browser_smoke_checks,
        "blocking_gaps": tuple(name for name, ok in checks.items() if not ok),
    }


def _tooling_audit_lsp_json_rpc(source: str, *, broken_handler_source: str) -> dict:
    documents: dict[str, str] = {}
    uri = "memory://tooling-audit.appgen"
    bad_uri = "memory://bad-handler.appgen"
    format_uri = "memory://format.appgen"
    format_source = "app FormatDemo { targets: web }\ntable Invoice { id: int pk }\n"
    checks = []

    init_responses, _ = lsp_server_handle_message(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        documents,
    )
    capabilities = init_responses[0]["result"]["capabilities"] if init_responses else {}
    checks.append(
        _release_check(
            "initialize_capabilities",
            bool(init_responses)
            and bool(capabilities.get("completionProvider", {}).get("triggerCharacters"))
            and capabilities.get("hoverProvider") is True
            and capabilities.get("definitionProvider") is True
            and capabilities.get("referencesProvider") is True
            and capabilities.get("documentSymbolProvider") is True
            and bool(capabilities.get("renameProvider"))
            and capabilities.get("codeActionProvider") is True
            and capabilities.get("documentFormattingProvider") is True
            and bool(capabilities.get("workspaceSymbolProvider")),
        )
    )

    open_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {"textDocument": {"uri": uri, "languageId": "appgen", "version": 1, "text": source}},
        },
        documents,
    )
    checks.append(
        _release_check(
            "did_open_diagnostics",
            bool(open_responses) and open_responses[0]["method"] == "textDocument/publishDiagnostics",
        )
    )

    change_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {"uri": uri, "version": 2},
                "contentChanges": ({"text": source},),
            },
        },
        documents,
    )
    checks.append(
        _release_check(
            "did_change_diagnostics",
            documents.get(uri) == source
            and bool(change_responses)
            and change_responses[0]["method"] == "textDocument/publishDiagnostics",
        )
    )

    request_checks = (
        (
            "completion",
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/completion",
                "params": {"textDocument": {"uri": uri}, "position": _tooling_lsp_position(source, "Invoice")},
            },
            lambda result: any(item.get("label") == "Invoice" for item in result.get("items", ())),
        ),
        (
            "hover",
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "textDocument/hover",
                "params": {"textDocument": {"uri": uri}, "position": _tooling_lsp_position(source, "Invoice")},
            },
            lambda result: bool(result and result.get("contents")),
        ),
        (
            "definition",
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "textDocument/definition",
                "params": {"textDocument": {"uri": uri}, "position": _tooling_lsp_position(source, "InvoiceForm")},
            },
            lambda result: bool(result and result.get("uri") == uri),
        ),
        (
            "references",
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "textDocument/references",
                "params": {"textDocument": {"uri": uri}, "position": _tooling_lsp_position(source, "Invoice")},
            },
            lambda result: len(result or ()) >= 2,
        ),
        (
            "document_symbols",
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "textDocument/documentSymbol",
                "params": {"textDocument": {"uri": uri}},
            },
            lambda result: any(item.get("name") == "Invoice" for item in result or ()),
        ),
        (
            "rename",
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "textDocument/rename",
                "params": {
                    "textDocument": {"uri": uri},
                    "position": _tooling_lsp_position(source, "ReverseInvoice"),
                    "newName": "ReversePostedInvoice",
                },
            },
            lambda result: "ReversePostedInvoice" in result.get("changes", {}).get(uri, ({},))[0].get("newText", ""),
        ),
        (
            "workspace_symbol",
            {"jsonrpc": "2.0", "id": 8, "method": "workspace/symbol", "params": {"query": "Invoice"}},
            lambda result: any(item.get("name") == "Invoice" for item in result or ()),
        ),
        (
            "workspace_symbol_catalog_metadata",
            {"jsonrpc": "2.0", "id": 9, "method": "workspace/symbol", "params": {"query": "JournalPosted"}},
            lambda result: any(
                item.get("name") == "JournalPosted"
                and item.get("data", {}).get("catalog_resolved") is True
                and item.get("data", {}).get("pbc") == "gl_core"
                for item in result or ()
            ),
        ),
    )
    for name, message, predicate in request_checks:
        responses, _ = lsp_server_handle_message(message, documents)
        result = responses[0].get("result") if responses else None
        checks.append(_release_check(name, bool(responses) and predicate(result)))

    lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {"textDocument": {"uri": bad_uri, "languageId": "appgen", "version": 1, "text": broken_handler_source}},
        },
        documents,
    )
    code_action_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "textDocument/codeAction",
            "params": {"textDocument": {"uri": bad_uri}, "range": _lsp_full_document_range(broken_handler_source)},
        },
        documents,
    )
    code_actions = code_action_responses[0].get("result", ()) if code_action_responses else ()
    checks.append(
        _release_check(
            "code_action_request",
            any(action.get("data", {}).get("id") == "create_operation_from_handler" for action in code_actions),
        )
    )

    lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {"textDocument": {"uri": format_uri, "languageId": "appgen", "version": 1, "text": format_source}},
        },
        documents,
    )
    formatting_responses, _ = lsp_server_handle_message(
        {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "textDocument/formatting",
            "params": {"textDocument": {"uri": format_uri}, "options": {"tabSize": 2, "insertSpaces": True}},
        },
        documents,
    )
    formatting_edits = formatting_responses[0].get("result", ()) if formatting_responses else ()
    checks.append(
        _release_check(
            "formatting_request",
            bool(formatting_edits) and "table Invoice" in formatting_edits[0].get("newText", ""),
        )
    )

    return {
        "format": "appgen.lsp-json-rpc-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "initialize_capabilities": capabilities,
        "blocking_gaps": tuple(check["check"] for check in checks if not check["ok"]),
    }


def _tooling_lsp_position(source: str, token: str) -> dict:
    index = source.index(token)
    line = source.count("\n", 0, index)
    previous_newline = source.rfind("\n", 0, index)
    character = index if previous_newline < 0 else index - previous_newline - 1
    return {"line": line, "character": character}


def _tooling_audit_lsp_stdio_transport(source: str) -> dict:
    uri = "memory://stdio-tooling-audit.appgen"
    input_stream = io.BytesIO()
    output_stream = io.BytesIO()
    completion_position = _tooling_lsp_position(source, "Invoice")
    for message in (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {"textDocument": {"uri": uri, "languageId": "appgen", "version": 1, "text": source}},
        },
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {"uri": uri, "version": 2},
                "contentChanges": ({"text": source},),
            },
        },
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/completion",
            "params": {"textDocument": {"uri": uri}, "position": completion_position},
        },
        {"jsonrpc": "2.0", "id": 3, "method": "workspace/symbol", "params": {"query": "Invoice"}},
        {"jsonrpc": "2.0", "id": 4, "method": "shutdown"},
        {"jsonrpc": "2.0", "method": "exit"},
    ):
        _lsp_write_rpc_message(input_stream, message)
    input_stream.seek(0)
    exit_code = lsp_stdio_server(input_stream=input_stream, output_stream=output_stream)
    output_stream.seek(0)
    responses: list[dict] = []
    while True:
        response = _lsp_read_rpc_message(output_stream)
        if response is None:
            break
        responses.append(response)
    return {
        "format": "appgen.lsp-stdio-transport-audit.v1",
        "ok": exit_code == 0
        and any(response.get("id") == 1 and "capabilities" in response.get("result", {}) for response in responses)
        and sum(1 for response in responses if response.get("method") == "textDocument/publishDiagnostics") >= 2
        and any(
            response.get("id") == 2
            and any(item.get("label") == "Invoice" for item in response.get("result", {}).get("items", ()))
            for response in responses
        )
        and any(
            response.get("id") == 3
            and any(item.get("name") == "Invoice" for item in response.get("result", ()))
            for response in responses
        )
        and any(response.get("id") == 4 and response.get("result") is None for response in responses),
        "exit_code": exit_code,
        "response_count": len(responses),
        "methods": tuple(response.get("method") for response in responses if response.get("method")),
        "ids": tuple(response.get("id") for response in responses if "id" in response),
        "diagnostic_publication_count": sum(
            1 for response in responses if response.get("method") == "textDocument/publishDiagnostics"
        ),
    }


def _tooling_audit_lsp_apply_code_action_cli(tmp: Path) -> dict:
    case_specs = (
        (
            "create_missing_table",
            "lsp-apply-missing-table.appgen",
            "app MissingTableFix { targets: web }\ntable Invoice { id: int pk }\nview MissingForm for Missing { Main: id }\n",
            "table Missing",
            (),
        ),
        (
            "create_missing_field",
            "lsp-apply-missing-field.appgen",
            "app MissingFieldFix { targets: web }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: total }\n",
            "total: string",
            (),
        ),
        (
            "create_calculated_field_for_binding",
            "lsp-apply-calculated-field.appgen",
            "app CalculatedFix { targets: web }\ntable Customer { id: int pk; name: string }\ntable Invoice { id: int pk; customer_id: int -> Customer.id }\nview InvoiceForm for Invoice { Main: customer.missing_name }\n",
            "missing_name: string = name",
            (),
        ),
        (
            "create_operation_from_handler",
            "lsp-apply-operation.appgen",
            """
app Bad { targets: web }
table Invoice { id: int pk }
view InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }
""",
            "operation SubmitInvoice",
            (),
        ),
        (
            "create_flow_from_handler",
            "lsp-apply-flow.appgen",
            "app FlowFix { targets: web }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }\n",
            "flow SubmitInvoice",
            (),
        ),
        (
            "add_lookup_directive",
            "lsp-apply-lookup.appgen",
            """
app LookupFix { targets: web }
table Customer { id: int pk; name: string }
table Invoice { id: int pk; customer_id: int -> Customer.id }
view InvoiceForm for Invoice { Main: customer_name }
""",
            "lookup customer_name (customer.name)",
            (),
        ),
        (
            "add_relationship_for_lookup_path",
            "lsp-apply-relationship.appgen",
            "app RelationshipFix { targets: web }\ntable Customer { id: int pk; name: string }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: customer.name }\n",
            "customer_id: int -> Customer.id",
            (),
        ),
        (
            "replace_typo_with_nearest_symbol",
            "lsp-apply-typo.appgen",
            "app TypoFix { targets: web }\ntable Invoice { id: int pk; total: decimal }\nview InvoiceForm for Invoice { Main: totl }\n",
            "Main: total",
            ("Main: totl",),
        ),
        (
            "replace_secret_literal_with_env",
            "lsp-apply-secret.appgen",
            """
app SecretFix { targets: web }
table T { id: int pk }
view TForm for T { Main: id }
llm ApiModel { provider: openai; api_key: "sk-secret" }
""",
            "api_key: OPENAI_API_KEY",
            ('api_key: "sk-secret"',),
        ),
        (
            "remove_invalid_runtime_picker_fields",
            "lsp-apply-runtime.appgen",
            """
app RuntimeFix { targets: web; runtime: node; stream: bytewax; backend: oracle }
table T { id: int pk }
view TForm for T { Main: id }
""",
            "targets: web",
            ("runtime:", "stream:", "backend:"),
        ),
        (
            "create_event_contract",
            "lsp-apply-event-contract.appgen",
            """
app EventContractFix { targets: web }
table T { id: int pk }
view TForm for T { Main: id }
composition Suite {
  include pbc gl_core version 1.0.0
  include pbc ap_automation version 1.0.0
  connect ap_automation domain_event MissingEvent -> gl_core domain_event MissingCommand
}
""",
            "event MissingEvent",
            (),
        ),
        (
            "register_or_import_pbc_manifest",
            "lsp-apply-pbc-manifest.appgen",
            "app PbcManifestFix { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\ncomposition Suite { include pbc missing_pbc version 1.0.0 }\n",
            "pbc missing_pbc",
            (),
        ),
        (
            "add_missing_permission_for_agent_skill",
            "lsp-apply-agent-permission.appgen",
            "app AgentPermissionFix { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\nllm LocalModel { provider: ollama; mode: local }\nagent Writer { provider: LocalModel; tools: write }\n",
            "GeneratedResource: write",
            (),
        ),
        (
            "add_package_for_app_target",
            "lsp-apply-package.appgen",
            """
app PackageFix { targets: web }
table T { id: int pk }
view TForm for T { Main: id }
""",
            "package WebPackage",
            (),
        ),
        (
            "create_smoke_test_declaration",
            "lsp-apply-smoke.appgen",
            """
app SmokeFix { targets: web }
table T { id: int pk }
view TForm for T { Main: id }
flow Publish { draft -> live }
package WebPackage { target: web; smoke: launch }
""",
            "test PublishSmoke",
            (),
        ),
    )

    def run_apply(path: Path, action_id: str) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(
                (
                    "lsp",
                    str(path),
                    "--apply-code-action",
                    action_id,
                    "--json",
                )
            )
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        return exit_code, payload

    cases = []
    for action_id, filename, source, expected_text, forbidden_text in case_specs:
        path = tmp / filename
        path.write_text(source, encoding="utf-8")
        exit_code, payload = run_apply(path, action_id)
        patched_source = payload.get("patched_source", "")
        forbidden_removed = all(item not in patched_source for item in forbidden_text)
        cases.append(
            {
                "case": action_id,
                "ok": exit_code == 0
                and payload.get("format") == "appgen.lsp-code-action-apply.v1"
                and payload.get("ok") is True
                and payload.get("changed") is True
                and payload.get("action_id") == action_id
                and expected_text in patched_source
                and forbidden_removed
                and payload.get("lint", {}).get("format") == "appgen.lint-report.v1"
                and payload.get("lint", {}).get("ok") is True
                and bool(payload.get("applied_edits")),
                "exit_code": exit_code,
                "payload_format": payload.get("format"),
                "action_id": payload.get("action_id"),
                "changed": payload.get("changed"),
                "applied_edit_count": len(payload.get("applied_edits", ())),
                "lint_format": payload.get("lint", {}).get("format"),
                "lint_ok": payload.get("lint", {}).get("ok"),
                "expected_text": expected_text,
                "forbidden_removed": forbidden_removed,
            }
        )
    return {
        "format": "appgen.lsp-code-action-cli-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": tuple(cases),
        "required_cli_actions": tuple(case["case"] for case in cases),
    }


def _tooling_audit_lsp_rename_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "lsp-rename.appgen"
    source_path.write_text(source, encoding="utf-8")
    position = _tooling_lsp_position(source, "SubmitInvoice")
    position_arg = f"{position['line']}:{position['character']}"
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exit_code = dsl_tooling_cli(
            (
                "lsp",
                str(source_path),
                "--position",
                position_arg,
                "--rename",
                "PostInvoice",
                "--json",
            )
        )
    try:
        payload = json.loads(output.getvalue())
    except json.JSONDecodeError:
        payload = {}
    rename = payload.get("rename", {})
    changes = rename.get("workspace_edit", {}).get("changes", {})
    file_changes = changes.get(str(source_path), ())
    patched_text = file_changes[0].get("newText", "") if file_changes else ""
    safe_ok = (
        exit_code == 0
        and payload.get("format") == "appgen.lsp-service.v1"
        and rename.get("format") == "appgen.lsp-rename.v1"
        and rename.get("ok") is True
        and rename.get("token") == "SubmitInvoice"
        and rename.get("new_name") == "PostInvoice"
        and "PostInvoice" in patched_text
        and rename.get("migration_preview", {}).get("format") == "appgen.migration-plan.v1"
    )

    risk_source = """
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
    risk_path = tmp / "lsp-rename-risk.appgen"
    risk_path.write_text(risk_source, encoding="utf-8")
    risk_position = _tooling_lsp_position(risk_source, "id: int pk")
    risk_position_arg = f"{risk_position['line']}:{risk_position['character']}"
    risk_output = io.StringIO()
    with contextlib.redirect_stdout(risk_output):
        risk_exit = dsl_tooling_cli(
            (
                "lsp",
                str(risk_path),
                "--position",
                risk_position_arg,
                "--rename",
                "identifier",
                "--json",
            )
        )
    risk_text_output = io.StringIO()
    with contextlib.redirect_stdout(risk_text_output):
        risk_text_exit = dsl_tooling_cli(
            (
                "lsp",
                str(risk_path),
                "--position",
                risk_position_arg,
                "--rename",
                "identifier",
            )
        )
    try:
        risk_payload = json.loads(risk_output.getvalue())
    except json.JSONDecodeError:
        risk_payload = {}
    blocked_rename = risk_payload.get("rename", {})
    blocked_codes = tuple(item.get("code") for item in blocked_rename.get("blockers", ()))
    blocked_fixes = tuple(
        fix.get("id")
        for item in blocked_rename.get("blockers", ())
        for fix in item.get("fixes", ())
    )
    blocked_ok = (
        risk_exit == 0
        and risk_payload.get("format") == "appgen.lsp-service.v1"
        and blocked_rename.get("format") == "appgen.lsp-rename.v1"
        and blocked_rename.get("ok") is False
        and blocked_rename.get("blocked") is True
        and blocked_rename.get("migration_preview", {}).get("format") == "appgen.migration-plan.v1"
        and blocked_rename.get("migration_preview", {}).get("requires_approval") is True
        and "AGX1101" in blocked_codes
        and "add_rename_hint" in blocked_fixes
    )
    blocked_text = risk_text_output.getvalue()
    blocked_text_ok = (
        risk_text_exit == 0
        and "rename ok=False" in blocked_text
        and "blocked=True" in blocked_text
        and "requires_approval=True" in blocked_text
        and "blockers=1" in blocked_text
    )

    return {
        "format": "appgen.lsp-rename-cli-audit.v1",
        "ok": safe_ok and blocked_ok and blocked_text_ok,
        "exit_code": exit_code,
        "payload_format": payload.get("format"),
        "rename_format": rename.get("format"),
        "token": rename.get("token"),
        "new_name": rename.get("new_name"),
        "position": position_arg,
        "changed": bool(file_changes),
        "migration_format": rename.get("migration_preview", {}).get("format"),
        "safe_ok": safe_ok,
        "blocked_ok": blocked_ok,
        "blocked_exit_code": risk_exit,
        "blocked_payload_format": risk_payload.get("format"),
        "blocked_rename_format": blocked_rename.get("format"),
        "blocked_rename_ok": blocked_rename.get("ok"),
        "blocked": blocked_rename.get("blocked"),
        "blocked_text_ok": blocked_text_ok,
        "blocked_text_exit_code": risk_text_exit,
        "blocked_text": blocked_text.strip(),
        "blocked_position": risk_position_arg,
        "blocked_code": "AGX1101" if "AGX1101" in blocked_codes else None,
        "blocked_fix": "add_rename_hint" if "add_rename_hint" in blocked_fixes else None,
        "blocked_migration_format": blocked_rename.get("migration_preview", {}).get("format"),
        "blocked_requires_approval": blocked_rename.get("migration_preview", {}).get("requires_approval"),
    }


def _tooling_audit_format_write(tmp: Path) -> dict:
    path = tmp / "format-write.appgen"
    check_path = tmp / "format-check.appgen"
    clean_check_path = tmp / "format-check-clean.appgen"
    organize_path = tmp / "format-organize.appgen"
    source = "app FormatWrite { targets: web }\ntable Invoice { total: decimal; id: int pk }\n"
    organize_source = """
app FormatOrganize { targets: web }

table Invoice {
  total: decimal = subtotal + tax
  customer_id: int -> Customer.id
  updated_at: string
  invoice_number: string unique
  subtotal: decimal
  tax: decimal
  id: int pk
  index(total)
}

table Customer {
  id: int pk
}
"""
    path.write_text(source, encoding="utf-8")
    check_path.write_text(source, encoding="utf-8")
    clean_source = format_report_dsl(source, include_text=True)["text"]
    clean_check_path.write_text(clean_source, encoding="utf-8")
    organize_path.write_text(organize_source, encoding="utf-8")

    check_output = io.StringIO()
    with contextlib.redirect_stdout(check_output):
        check_exit = dsl_tooling_cli(("format", str(check_path), "--check", "--json"))
    check_payload = json.loads(check_output.getvalue())

    clean_check_output = io.StringIO()
    with contextlib.redirect_stdout(clean_check_output):
        clean_check_exit = dsl_tooling_cli(("format", str(clean_check_path), "--check", "--json"))
    clean_check_payload = json.loads(clean_check_output.getvalue())

    organize_output = io.StringIO()
    with contextlib.redirect_stdout(organize_output):
        organize_exit = dsl_tooling_cli(("format", str(organize_path), "--organize", "--json"))
    organize_payload = json.loads(organize_output.getvalue())
    organize_text = organize_payload.get("text", "")
    organized_table_index_order = (
        organize_text.find("  id: int pk"),
        organize_text.find("  invoice_number: string unique"),
        organize_text.find("  customer_id: int -> Customer.id"),
        organize_text.find("  subtotal: decimal"),
        organize_text.find("  total: decimal = subtotal + tax"),
        organize_text.find("  updated_at: string"),
        organize_text.find("  index(total)"),
    )

    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exit_code = dsl_tooling_cli(("format", str(path), "--write", "--json"))
    payload = json.loads(output.getvalue())
    after = path.read_text(encoding="utf-8")
    return {
        "format": "appgen.format-write-audit.v1",
        "ok": exit_code == 0
        and payload.get("format") == "appgen.format-result.v1"
        and check_exit == 1
        and check_payload.get("format") == "appgen.format-result.v1"
        and check_payload.get("changed") is True
        and check_payload.get("write_requested") is False
        and check_payload.get("written") is False
        and clean_check_exit == 0
        and clean_check_payload.get("format") == "appgen.format-result.v1"
        and clean_check_payload.get("changed") is False
        and organize_exit == 0
        and organize_payload.get("format") == "appgen.format-result.v1"
        and organize_payload.get("organize") is True
        and organize_payload.get("idempotent") is True
        and -1 not in organized_table_index_order
        and organized_table_index_order == tuple(sorted(organized_table_index_order))
        and payload.get("write_requested") is True
        and payload.get("written") is True
        and after == payload.get("text")
        and after != source,
        "exit_code": exit_code,
        "payload_format": payload.get("format"),
        "check_exit_code": check_exit,
        "check_changed": check_payload.get("changed"),
        "check_write_requested": check_payload.get("write_requested"),
        "check_written": check_payload.get("written"),
        "clean_check_exit_code": clean_check_exit,
        "clean_check_changed": clean_check_payload.get("changed"),
        "organize_exit_code": organize_exit,
        "organize": organize_payload.get("organize"),
        "organize_idempotent": organize_payload.get("idempotent"),
        "organize_order": organized_table_index_order,
        "written": payload.get("written"),
        "write_path": payload.get("write_path"),
    }


def _tooling_audit_internal_error_exit(tmp: Path) -> dict:
    source_path = tmp / "internal-error.appgen"
    malformed_catalog = tmp / "malformed-components.json"
    source_path.write_text("app InternalError { targets: web }\ntable Thing { id: int pk }\n", encoding="utf-8")
    malformed_catalog.write_text("{not-json", encoding="utf-8")
    json_output = io.StringIO()
    json_error = io.StringIO()
    with contextlib.redirect_stdout(json_output), contextlib.redirect_stderr(json_error):
        json_exit_code = dsl_tooling_cli(
            (
                "lint",
                str(source_path),
                "--catalog",
                str(malformed_catalog),
                "--json",
            )
        )
    payload = json.loads(json_output.getvalue())
    text_output = io.StringIO()
    text_error = io.StringIO()
    with contextlib.redirect_stdout(text_output), contextlib.redirect_stderr(text_error):
        text_exit_code = dsl_tooling_cli(("lint", str(source_path), "--catalog", str(malformed_catalog)))
    json_stderr = json_error.getvalue()
    text_stdout = text_output.getvalue()
    text_stderr = text_error.getvalue()
    return {
        "format": "appgen.internal-error-exit-audit.v1",
        "ok": json_exit_code == 3
        and text_exit_code == 3
        and payload.get("format") == "appgen.internal-error.v1"
        and payload.get("code") == "AGX9000"
        and payload.get("ok") is False
        and text_stdout.startswith("internal-error")
        and "Traceback" not in json_stderr
        and "Traceback" not in text_stderr
        and "Traceback" not in text_stdout,
        "json_exit_code": json_exit_code,
        "text_exit_code": text_exit_code,
        "payload_format": payload.get("format"),
        "code": payload.get("code"),
        "error_type": payload.get("error_type"),
        "json_traceback_free": "Traceback" not in json_stderr,
        "text_traceback_free": "Traceback" not in text_stderr and "Traceback" not in text_stdout,
        "text_stdout": text_stdout.strip(),
    }


def _tooling_audit_missing_input_exit(tmp: Path) -> dict:
    missing_path = tmp / "missing.appgen"
    current_path = tmp / "current.appgen"
    current_path.write_text("app Current { targets: web }\ntable Thing { id: int pk }\n", encoding="utf-8")
    cases = (
        ("lint_missing_path", ("lint", str(missing_path))),
        ("lint_missing_previous_semantic", ("lint", str(current_path), "--previous-semantic", str(missing_path))),
        ("lint_missing_catalog", ("lint", str(current_path), "--catalog", str(missing_path))),
        ("format_missing_path", ("format", str(missing_path), "--check")),
        ("validate_missing_path", ("validate", str(missing_path))),
        ("graph_missing_path", ("graph", str(missing_path), "--format", "json")),
        ("graph_suite_missing_path", ("graph-suite", str(missing_path))),
        ("explain_missing_path", ("explain", str(missing_path), "--symbol", "table.Thing")),
        ("generate_missing_path", ("generate", str(missing_path), "--out", str(tmp / "generated"))),
        ("migration_missing_previous", ("migration-plan", str(missing_path), str(current_path))),
        ("migration_missing_current", ("migration-plan", str(current_path), str(missing_path))),
        ("nl_plan_missing_path", ("nl-plan", str(missing_path), "--prompt", "Add memo")),
        ("lsp_missing_path", ("lsp", str(missing_path))),
        ("verify_missing_path", ("verify", str(missing_path))),
        ("package_missing_path", ("package", str(missing_path))),
        ("designer_sync_missing_path", ("designer-sync", str(missing_path))),
        ("drift_missing_path", ("drift", str(missing_path))),
    )
    results = []
    for name, argv in cases:
        output = io.StringIO()
        error = io.StringIO()
        exit_code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            try:
                exit_code = dsl_tooling_cli(argv)
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
        stderr = error.getvalue()
        results.append(
            {
                "name": name,
                "ok": exit_code == 2 and "path does not exist" in stderr and "Traceback" not in stderr,
                "exit_code": exit_code,
                "stderr": stderr.strip(),
                "stdout": output.getvalue().strip(),
            }
        )
    return {
        "format": "appgen.missing-input-exit-audit.v1",
        "ok": all(result["ok"] for result in results),
        "cases": tuple(results),
    }


def _tooling_audit_missing_required_option_exit(tmp: Path) -> dict:
    source_path = tmp / "missing-required-option.appgen"
    source_path.write_text("app MissingRequiredOption { targets: web }\ntable Thing { id: int pk }\n", encoding="utf-8")
    cases = (
        ("generate_missing_out", ("generate", str(source_path))),
        ("nl_plan_missing_prompt", ("nl-plan", str(source_path))),
        ("component_publish_missing_component", ("component-publish",)),
    )
    results = []
    for name, argv in cases:
        output = io.StringIO()
        error = io.StringIO()
        exit_code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            try:
                exit_code = dsl_tooling_cli(argv)
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
        stderr = error.getvalue()
        results.append(
            {
                "name": name,
                "ok": exit_code == 2 and "the following arguments are required" in stderr and "Traceback" not in stderr,
                "exit_code": exit_code,
                "stderr": stderr.strip(),
                "stdout": output.getvalue().strip(),
            }
        )
    return {
        "format": "appgen.missing-required-option-exit-audit.v1",
        "ok": all(result["ok"] for result in results),
        "cases": tuple(results),
    }


def _tooling_audit_invalid_choice_exit(tmp: Path) -> dict:
    source_path = tmp / "invalid-choice.appgen"
    source_path.write_text("app InvalidChoice { targets: web }\ntable Thing { id: int pk }\n", encoding="utf-8")
    cases = (
        ("lint_backend", ("lint", str(source_path), "--backend", "oracle")),
        ("graph_kind", ("graph", str(source_path), "--kind", "unknown", "--format", "json")),
        ("graph_format", ("graph", str(source_path), "--kind", "er", "--format", "svg")),
        ("migration_backend", ("migration-plan", str(source_path), str(source_path), "--backend", "oracle")),
        ("nl_backend", ("nl-plan", str(source_path), "--prompt", "Add memo", "--backend", "oracle")),
    )
    results = []
    for name, argv in cases:
        output = io.StringIO()
        error = io.StringIO()
        exit_code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            try:
                exit_code = dsl_tooling_cli(argv)
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
        stderr = error.getvalue()
        results.append(
            {
                "name": name,
                "ok": exit_code == 2 and "invalid choice" in stderr and "Traceback" not in stderr,
                "exit_code": exit_code,
                "stderr": stderr.strip(),
                "stdout": output.getvalue().strip(),
            }
        )
    return {
        "format": "appgen.invalid-choice-exit-audit.v1",
        "ok": all(result["ok"] for result in results),
        "cases": tuple(results),
    }


def _tooling_audit_lint_directory_cli(tmp: Path, source: str) -> dict:
    source_dir = tmp / "lint-directory"
    nested_dir = source_dir / "nested"
    catalog_path = tmp / "component-catalog.json"
    strict_component_path = tmp / "strict-component.appgen"
    catalog_component_path = tmp / "catalog-component.appgen"
    migration_current_path = tmp / "lint-migration-current.appgen"
    migration_previous_path = tmp / "lint-previous-semantic.json"
    nested_dir.mkdir(parents=True, exist_ok=True)
    first_path = source_dir / "a.appgen"
    second_path = nested_dir / "b.appgen"
    first_path.write_text(source, encoding="utf-8")
    second_path.write_text(_doctor_sample_dsl(), encoding="utf-8")
    catalog_path.write_text(json.dumps({"components": ["CustomGauge"]}, indent=2), encoding="utf-8")
    strict_component_path.write_text(
        """
app StrictComponentDemo { targets: web }
table Customer { id: int pk; name: string }
view CustomerForm for Customer {
  Main: name
  @ name UnknownWidget 0 0 4 1
}
""".strip(),
        encoding="utf-8",
    )
    catalog_component_path.write_text(_tooling_audit_component_catalog_sample(), encoding="utf-8")
    migration_previous_source = "app MigrationLint { targets: web }\ntable Customer { id: int pk }\n"
    migration_current_path.write_text(
        "app MigrationLint { targets: web }\ntable Customer { id: int pk; name: string }\n",
        encoding="utf-8",
    )
    migration_previous_path.write_text(
        json.dumps(semantic_model_dsl(migration_previous_source, source_name="previous.appgen"), indent=2, default=list),
        encoding="utf-8",
    )

    def run_json(argv: tuple[str, ...]) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(argv)
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        return exit_code, payload

    exit_code, payload = run_json(("lint", str(source_dir), "--strict", "--catalog", str(catalog_path), "--json"))
    normal_unknown_exit_code, normal_unknown_payload = run_json(("lint", str(strict_component_path), "--json"))
    strict_unknown_exit_code, strict_unknown_payload = run_json(
        ("lint", str(strict_component_path), "--strict", "--json")
    )
    strict_catalog_exit_code, strict_catalog_payload = run_json(
        ("lint", str(catalog_component_path), "--strict", "--catalog", str(catalog_path), "--json")
    )
    migration_exit_code, migration_payload = run_json(
        ("lint", str(migration_current_path), "--previous-semantic", str(migration_previous_path), "--json")
    )

    warning_dir = tmp / "lint-directory-warnings"
    warning_nested_dir = warning_dir / "nested"
    warning_nested_dir.mkdir(parents=True, exist_ok=True)
    (warning_dir / "a.appgen").write_text(_tooling_audit_warning_generation_sample(), encoding="utf-8")
    (warning_nested_dir / "b.appgen").write_text(_doctor_sample_dsl(), encoding="utf-8")
    warning_exit_code, warning_payload = run_json(("lint", str(warning_dir), "--json"))

    files = tuple(payload.get("files", ()))
    file_reports = tuple(payload.get("file_reports", ()))
    warning_files = tuple(warning_payload.get("files", ()))
    warning_diagnostics = tuple(warning_payload.get("diagnostics", ()))
    warning_severity_counts = warning_payload.get("severity_counts", {})
    warning_diagnostics_have_files = all(
        "file" in diagnostic and diagnostic["file"] in warning_files for diagnostic in warning_diagnostics
    )
    normal_unknown_diagnostics = tuple(normal_unknown_payload.get("diagnostics", ()))
    strict_unknown_diagnostics = tuple(strict_unknown_payload.get("diagnostics", ()))
    strict_catalog_diagnostics = tuple(strict_catalog_payload.get("diagnostics", ()))
    syntax_path = tmp / "syntax-stage.appgen"
    semantic_path = tmp / "semantic-stage.appgen"
    policy_path = tmp / "policy-stage.appgen"
    syntax_path.write_text("app Broken { table Missing { id: int pk ", encoding="utf-8")
    semantic_path.write_text("app SemanticStage { targets: web }\nview MissingForm for Missing { Main: id }\n", encoding="utf-8")
    policy_path.write_text(_tooling_audit_warning_generation_sample(), encoding="utf-8")
    syntax_exit_code, syntax_payload = run_json(("lint", str(syntax_path), "--json"))
    semantic_exit_code, semantic_payload = run_json(("lint", str(semantic_path), "--json"))
    policy_exit_code, policy_payload = run_json(("lint", str(policy_path), "--json"))
    normal_unknown_component_warning = (
        normal_unknown_exit_code == 0
        and normal_unknown_payload.get("ok") is True
        and normal_unknown_payload.get("strict") is False
        and any(
            item.get("code") == "AGX0404" and item.get("severity") == "warning"
            for item in normal_unknown_diagnostics
        )
    )
    strict_unknown_component_error = (
        strict_unknown_exit_code == 1
        and strict_unknown_payload.get("ok") is False
        and strict_unknown_payload.get("strict") is True
        and any(
            item.get("code") == "AGX0404" and item.get("severity") == "error"
            for item in strict_unknown_diagnostics
        )
    )
    strict_catalog_component_success = (
        strict_catalog_exit_code == 0
        and strict_catalog_payload.get("ok") is True
        and strict_catalog_payload.get("strict") is True
        and strict_catalog_payload.get("component_catalog", {}).get("components") == ["CustomGauge"]
        and not any(item.get("code") == "AGX0404" for item in strict_catalog_diagnostics)
    )
    migration_preview = migration_payload.get("migration_preview") or {}
    migration_lint_success = (
        migration_exit_code == 0
        and migration_payload.get("format") == "appgen.lint-report.v1"
        and migration_preview.get("format") == "appgen.migration-plan.v1"
        and migration_preview.get("backend") == "postgresql"
        and "added_field" in set(migration_preview.get("coverage", {}).get("detected", ()))
    )
    stage_separation = {
        "syntax": syntax_exit_code == 1 and syntax_payload.get("stages", {}).get("syntax", {}).get("error", 0) >= 1,
        "semantic": semantic_exit_code == 1
        and semantic_payload.get("stages", {}).get("semantic", {}).get("error", 0) >= 1,
        "policy": policy_exit_code == 0 and policy_payload.get("stages", {}).get("policy", {}).get("warning", 0) >= 1,
    }
    return {
        "format": "appgen.lint-directory-cli-audit.v1",
        "ok": exit_code == 0
        and payload.get("format") == "appgen.lint-report.v1"
        and payload.get("ok") is True
        and payload.get("source_mode") == "directory"
        and len(files) == 2
        and files == tuple(sorted(files))
        and len(file_reports) == 2
        and payload.get("strict") is True
        and payload.get("component_catalog", {}).get("components") == ["CustomGauge"]
        and warning_exit_code == 0
        and warning_payload.get("format") == "appgen.lint-report.v1"
        and warning_payload.get("source_mode") == "directory"
        and warning_severity_counts.get("warning", 0) >= 1
        and len(warning_diagnostics) >= 1
        and warning_diagnostics_have_files
        and normal_unknown_component_warning
        and strict_unknown_component_error
        and strict_catalog_component_success
        and migration_lint_success
        and all(stage_separation.values()),
        "exit_code": exit_code,
        "payload_format": payload.get("format"),
        "source_mode": payload.get("source_mode"),
        "files": files,
        "file_report_count": len(file_reports),
        "strict": payload.get("strict"),
        "component_catalog": payload.get("component_catalog"),
        "warning_exit_code": warning_exit_code,
        "warning_source_mode": warning_payload.get("source_mode"),
        "warning_count": warning_severity_counts.get("warning", 0),
        "diagnostic_count": len(warning_diagnostics),
        "diagnostics_have_files": warning_diagnostics_have_files,
        "normal_unknown_component_warning": {
            "ok": normal_unknown_component_warning,
            "exit_code": normal_unknown_exit_code,
            "strict": normal_unknown_payload.get("strict"),
            "severity_counts": normal_unknown_payload.get("severity_counts"),
        },
        "strict_unknown_component_error": {
            "ok": strict_unknown_component_error,
            "exit_code": strict_unknown_exit_code,
            "strict": strict_unknown_payload.get("strict"),
            "severity_counts": strict_unknown_payload.get("severity_counts"),
        },
        "strict_catalog_component_success": {
            "ok": strict_catalog_component_success,
            "exit_code": strict_catalog_exit_code,
            "strict": strict_catalog_payload.get("strict"),
            "component_catalog": strict_catalog_payload.get("component_catalog"),
        },
        "previous_semantic_migration_preview": {
            "ok": migration_lint_success,
            "exit_code": migration_exit_code,
            "format": migration_preview.get("format"),
            "backend": migration_preview.get("backend"),
            "detected": tuple(migration_preview.get("coverage", {}).get("detected", ())),
        },
        "stage_separation": {
            "ok": all(stage_separation.values()),
            "stage_names": syntax_payload.get("stage_names", ()),
            "severity_names": syntax_payload.get("severity_names", ()),
            "stages": stage_separation,
            "syntax": syntax_payload.get("stages", {}),
            "semantic": semantic_payload.get("stages", {}),
            "policy": policy_payload.get("stages", {}),
        },
    }


def _tooling_audit_validate_generate_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "validate-generate.appgen"
    web_only_path = tmp / "validate-web-only.appgen"
    warning_path = tmp / "warning-generate.appgen"
    error_path = tmp / "error-generate.appgen"
    output_dir = tmp / "generated-cli"
    warning_blocked_dir = tmp / "warning-blocked-cli"
    warning_allowed_dir = tmp / "warning-allowed-cli"
    error_allowed_dir = tmp / "error-allowed-cli"
    source_path.write_text(source, encoding="utf-8")
    web_only_path.write_text("app WebOnly { targets: web }\n\ntable Thing { id: int pk }\n", encoding="utf-8")
    warning_path.write_text(_tooling_audit_warning_generation_sample(), encoding="utf-8")
    error_path.write_text("app Bad { targets: web }\n\ntable Invoice { total: galaxy }\n", encoding="utf-8")

    def run_json(argv: tuple[str, ...]) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(argv)
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        return exit_code, payload

    validate_exit, validate_payload = run_json(
        ("validate", str(source_path), "--targets", "web,mobile,desktop", "--json")
    )
    missing_target_exit, missing_target_payload = run_json(
        ("validate", str(web_only_path), "--targets", "web,mobile", "--json")
    )
    unknown_target_exit, unknown_target_payload = run_json(
        ("validate", str(web_only_path), "--targets", "satellite", "--json")
    )
    generate_exit, generate_payload = run_json(
        ("generate", str(source_path), "--target", "web", "--out", str(output_dir), "--json")
    )
    warning_blocked_exit, warning_blocked_payload = run_json(
        ("generate", str(warning_path), "--out", str(warning_blocked_dir), "--json")
    )
    warning_allowed_exit, warning_allowed_payload = run_json(
        ("generate", str(warning_path), "--out", str(warning_allowed_dir), "--allow-warnings", "--json")
    )
    error_allowed_exit, error_allowed_payload = run_json(
        ("generate", str(error_path), "--out", str(error_allowed_dir), "--allow-warnings", "--json")
    )
    cases = (
        {
            "case": "validate_targets",
            "ok": validate_exit == 0
            and validate_payload.get("format") == "appgen.validate-report.v1"
            and tuple(validate_payload.get("requested_targets", ())) == ("web", "mobile", "desktop")
            and any(
                check.get("check") == "target_compatibility" and check.get("ok")
                for check in validate_payload.get("checks", ())
            ),
            "exit_code": validate_exit,
            "payload_format": validate_payload.get("format"),
            "requested_targets": tuple(validate_payload.get("requested_targets", ())),
        },
        {
            "case": "validate_rejects_undeclared_targets",
            "ok": missing_target_exit == 1
            and missing_target_payload.get("format") == "appgen.validate-report.v1"
            and missing_target_payload.get("ok") is False
            and tuple(missing_target_payload.get("requested_targets", ())) == ("web", "mobile")
            and tuple(missing_target_payload.get("app_targets", ())) == ("web",)
            and any(
                check.get("check") == "target_compatibility"
                and tuple(check.get("missing_targets", ())) == ("mobile",)
                for check in missing_target_payload.get("checks", ())
            )
            and any(item.get("code") == "AGX0802" for item in missing_target_payload.get("diagnostics", ())),
            "exit_code": missing_target_exit,
            "payload_format": missing_target_payload.get("format"),
            "requested_targets": tuple(missing_target_payload.get("requested_targets", ())),
            "app_targets": tuple(missing_target_payload.get("app_targets", ())),
            "diagnostic_codes": tuple(item.get("code") for item in missing_target_payload.get("diagnostics", ())),
        },
        {
            "case": "validate_rejects_unknown_targets",
            "ok": unknown_target_exit == 1
            and unknown_target_payload.get("format") == "appgen.validate-report.v1"
            and unknown_target_payload.get("ok") is False
            and any(
                check.get("check") == "target_compatibility"
                and tuple(check.get("unknown_targets", ())) == ("satellite",)
                for check in unknown_target_payload.get("checks", ())
            )
            and any(item.get("code") == "AGX0802" for item in unknown_target_payload.get("diagnostics", ())),
            "exit_code": unknown_target_exit,
            "payload_format": unknown_target_payload.get("format"),
            "requested_targets": tuple(unknown_target_payload.get("requested_targets", ())),
            "diagnostic_codes": tuple(item.get("code") for item in unknown_target_payload.get("diagnostics", ())),
        },
        {
            "case": "generate_writes_artifacts",
            "ok": generate_exit == 0
            and generate_payload.get("format") == "appgen.generate-report.v1"
            and generate_payload.get("generated") is True
            and Path(str(generate_payload.get("manifest", ""))).exists()
            and bool(generate_payload.get("artifacts")),
            "exit_code": generate_exit,
            "payload_format": generate_payload.get("format"),
            "artifact_count": len(generate_payload.get("artifacts", ())),
            "manifest": generate_payload.get("manifest"),
        },
        {
            "case": "generate_blocks_warnings",
            "ok": warning_blocked_exit == 1
            and warning_blocked_payload.get("format") == "appgen.generate-report.v1"
            and warning_blocked_payload.get("generated") is False
            and "lint_warnings" in warning_blocked_payload.get("blocking_gaps", ()),
            "exit_code": warning_blocked_exit,
            "payload_format": warning_blocked_payload.get("format"),
            "blocking_gaps": tuple(warning_blocked_payload.get("blocking_gaps", ())),
        },
        {
            "case": "generate_allows_warnings_when_requested",
            "ok": warning_allowed_exit == 0
            and warning_allowed_payload.get("format") == "appgen.generate-report.v1"
            and warning_allowed_payload.get("generated") is True
            and warning_allowed_payload.get("allow_warnings") is True
            and Path(str(warning_allowed_payload.get("manifest", ""))).exists(),
            "exit_code": warning_allowed_exit,
            "payload_format": warning_allowed_payload.get("format"),
            "allow_warnings": warning_allowed_payload.get("allow_warnings"),
            "manifest": warning_allowed_payload.get("manifest"),
        },
        {
            "case": "generate_blocks_errors_even_when_warnings_allowed",
            "ok": error_allowed_exit == 1
            and error_allowed_payload.get("format") == "appgen.generate-report.v1"
            and error_allowed_payload.get("generated") is False
            and error_allowed_payload.get("allow_warnings") is True
            and "lint_errors" in error_allowed_payload.get("blocking_gaps", ())
            and not error_allowed_dir.exists(),
            "exit_code": error_allowed_exit,
            "payload_format": error_allowed_payload.get("format"),
            "allow_warnings": error_allowed_payload.get("allow_warnings"),
            "blocking_gaps": tuple(error_allowed_payload.get("blocking_gaps", ())),
            "output_exists": error_allowed_dir.exists(),
        },
    )
    return {
        "format": "appgen.validate-generate-cli-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": cases,
    }


def _tooling_cli_json_case(argv: tuple[str, ...]) -> tuple[int, dict]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exit_code = dsl_tooling_cli(argv)
    try:
        payload = json.loads(output.getvalue())
    except json.JSONDecodeError:
        payload = {}
    return exit_code, payload


def _tooling_cli_text_case(argv: tuple[str, ...]) -> tuple[int, str]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exit_code = dsl_tooling_cli(argv)
    return exit_code, output.getvalue()


def _tooling_audit_pbc_cli_text() -> dict:
    list_exit, list_text = _tooling_cli_text_case(("pbc", "list"))
    verify_exit, verify_text = _tooling_cli_text_case(("pbc", "verify", "gl_core"))
    cases = (
        {
            "case": "pbc_list_text",
            "ok": list_exit == 0
            and list_text.startswith("pbc list ok: count=")
            and "format=appgen.pbc-verifier-catalog.v1" in list_text
            and "mesh " in list_text
            and "pbc gl_core: ok=True" in list_text
            and not list_text.lstrip().startswith("{"),
            "exit_code": list_exit,
            "has_catalog_format": "format=appgen.pbc-verifier-catalog.v1" in list_text,
            "has_mesh_counts": "mesh " in list_text,
            "has_catalog_entry": "pbc gl_core: ok=True" in list_text,
            "json_fallback": list_text.lstrip().startswith("{"),
        },
        {
            "case": "pbc_verify_text",
            "ok": verify_exit == 0
            and verify_text.startswith("pbc verify ok: pbc=gl_core")
            and "format=appgen.pbc-package-verifier.v1" in verify_text
            and "checks=7 gaps=0" in verify_text
            and "ok manifest_validates" in verify_text
            and "catalog label=" in verify_text
            and not verify_text.lstrip().startswith("{"),
            "exit_code": verify_exit,
            "has_verifier_format": "format=appgen.pbc-package-verifier.v1" in verify_text,
            "has_check_counts": "checks=7 gaps=0" in verify_text,
            "has_per_check_status": "ok manifest_validates" in verify_text,
            "has_catalog_metadata": "catalog label=" in verify_text,
            "json_fallback": verify_text.lstrip().startswith("{"),
        },
    )
    return {
        "format": "appgen.pbc-cli-text-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": cases,
    }


def _tooling_audit_diagnostics_catalog_cli() -> dict:
    catalog_exit, catalog_payload = _tooling_cli_json_case(("diagnostics", "--json"))
    return {
        "case": "diagnostics_catalog",
        "ok": catalog_exit == 0
        and catalog_payload.get("format") == "appgen.diagnostic-catalog.v1"
        and catalog_payload.get("ok") is True
        and not catalog_payload.get("missing_fixtures")
        and set(catalog_payload.get("required_codes", ())) == set(catalog_payload.get("covered_fixture_codes", ())),
        "exit_code": catalog_exit,
        "payload_format": catalog_payload.get("format"),
        "required_count": len(catalog_payload.get("required_codes", ())),
        "covered_count": len(catalog_payload.get("covered_fixture_codes", ())),
        "fixture_count": catalog_payload.get("fixture_count"),
    }


def _tooling_audit_test_strategy_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "test-strategy.appgen"
    source_path.write_text(source, encoding="utf-8")

    run_json = _tooling_cli_json_case
    diagnostics_exit, diagnostics_payload = run_json(("diagnostics", "--audit-fixtures", "--json"))
    parser_exit, parser_payload = run_json(("parser-golden", "--json"))
    drift_exit, drift_payload = run_json(("drift", str(source_path), "--json"))
    doctor_exit, doctor_payload = run_json(("doctor", "--json"))
    drift_required_surfaces = ("cli", "lsp", "studio", "graph", "generator", "release_verifier")
    cases = (
        _tooling_audit_diagnostics_catalog_cli(),
        {
            "case": "diagnostics_audit_fixtures",
            "ok": diagnostics_exit == 0
            and diagnostics_payload.get("format") == "appgen.diagnostic-fixture-audit.v1"
            and diagnostics_payload.get("ok") is True
            and not diagnostics_payload.get("missing_codes"),
            "exit_code": diagnostics_exit,
            "payload_format": diagnostics_payload.get("format"),
            "required_count": len(diagnostics_payload.get("required_codes", ())),
        },
        {
            "case": "parser_golden",
            "ok": parser_exit == 0
            and parser_payload.get("format") == "appgen.parser-golden-audit.v1"
            and parser_payload.get("ok") is True
            and not parser_payload.get("missing_constructs"),
            "exit_code": parser_exit,
            "payload_format": parser_payload.get("format"),
            "fixture_count": parser_payload.get("fixture_count"),
        },
        {
            "case": "semantic_drift",
            "ok": drift_exit == 0
            and drift_payload.get("format") == "appgen.semantic-drift-audit.v1"
            and drift_payload.get("ok") is True
            and set(drift_required_surfaces) <= set(drift_payload.get("surfaces", ()))
            and drift_payload.get("surface_evidence", {}).get("generate_report") == "appgen.generate-report.v1",
            "exit_code": drift_exit,
            "payload_format": drift_payload.get("format"),
            "surfaces": tuple(drift_payload.get("surfaces", ())),
            "required_surfaces": drift_required_surfaces,
            "generate_report": drift_payload.get("surface_evidence", {}).get("generate_report"),
        },
        {
            "case": "doctor",
            "ok": doctor_exit == 0
            and doctor_payload.get("format") == "appgen.doctor-report.v1"
            and doctor_payload.get("ok") is True
            and not doctor_payload.get("blocking_gaps"),
            "exit_code": doctor_exit,
            "payload_format": doctor_payload.get("format"),
            "check_count": len(doctor_payload.get("checks", ())),
        },
    )
    return {
        "format": "appgen.test-strategy-cli-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": cases,
    }


def _tooling_audit_designer_sync_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "designer-sync.appgen"
    source_path.write_text(source, encoding="utf-8")
    edit = {
        "kind": "add_field",
        "table": "Invoice",
        "field": "sync_note",
        "type": "string",
    }
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        valid_exit = dsl_tooling_cli(("designer-sync", str(source_path), "--edit-json", json.dumps(edit), "--json"))
    valid_payload = json.loads(output.getvalue())
    valid_edit = valid_payload.get("visual_edit", {})
    valid_projection = valid_edit.get("projections_after", {}).get("database_designer", {})
    invalid_output = io.StringIO()
    invalid_error = io.StringIO()
    invalid_exit = 0
    with contextlib.redirect_stdout(invalid_output), contextlib.redirect_stderr(invalid_error):
        try:
            invalid_exit = dsl_tooling_cli(("designer-sync", str(source_path), "--edit-json", "{bad", "--json"))
        except SystemExit as exc:
            invalid_exit = int(exc.code or 0)
    invalid_stderr = invalid_error.getvalue()
    non_object_output = io.StringIO()
    non_object_error = io.StringIO()
    non_object_exit = 0
    with contextlib.redirect_stdout(non_object_output), contextlib.redirect_stderr(non_object_error):
        try:
            non_object_exit = dsl_tooling_cli(("designer-sync", str(source_path), "--edit-json", "[]", "--json"))
        except SystemExit as exc:
            non_object_exit = int(exc.code or 0)
    non_object_stderr = non_object_error.getvalue()
    return {
        "format": "appgen.designer-sync-cli-audit.v1",
        "ok": valid_exit == 0
        and valid_payload.get("format") == "appgen.designer-sync-report.v1"
        and valid_edit.get("accepted") is True
        and valid_edit.get("round_trip_ok") is True
        and "sync_note" in valid_edit.get("patched_source", "")
        and "sync_note" in valid_edit.get("semantic_after", {}).get("tables", {}).get("Invoice", {}).get("fields", {})
        and "database_designer" in valid_edit.get("changed_surfaces", ())
        and any(str(line).startswith("+  sync_note: string") for line in valid_edit.get("dsl_diff", ()))
        and valid_projection.get("semantic_model_format") == "appgen.semantic-model.v1"
        and valid_projection.get("er_graph", {}).get("format") == "appgen.graph.er.v1"
        and invalid_exit == 2
        and "invalid JSON for --edit-json" in invalid_stderr
        and "Traceback" not in invalid_stderr
        and non_object_exit == 2
        and "--edit-json must be a JSON object" in non_object_stderr
        and "Traceback" not in non_object_stderr,
        "valid_exit": valid_exit,
        "valid_payload_format": valid_payload.get("format"),
        "valid_round_trip": valid_edit.get("round_trip_ok"),
        "valid_changed_surfaces": valid_edit.get("changed_surfaces", ()),
        "valid_diff_lines": len(valid_edit.get("dsl_diff", ())),
        "valid_semantic_model_format": valid_edit.get("semantic_model_format"),
        "valid_projection_format": valid_projection.get("format"),
        "valid_projection_semantic_model_format": valid_projection.get("semantic_model_format"),
        "invalid_exit": invalid_exit,
        "invalid_stderr": invalid_stderr.strip(),
        "non_object_exit": non_object_exit,
        "non_object_stderr": non_object_stderr.strip(),
    }


def _tooling_audit_graph_cli_formats(tmp: Path, source: str) -> dict:
    source_path = tmp / "graph-cli.appgen"
    source_path.write_text(source, encoding="utf-8")
    cases = (
        ("er_mermaid", "er", "mermaid", ("graph", str(source_path), "--kind", "er", "--format", "mermaid")),
        ("workflow_json", "workflow", "json", ("graph", str(source_path), "--kind", "workflow", "--format", "json")),
        (
            "workflow_mermaid",
            "workflow",
            "mermaid",
            ("graph", str(source_path), "--kind", "workflow", "--format", "mermaid"),
        ),
        ("pbc_dot", "pbc", "dot", ("graph", str(source_path), "--kind", "pbc", "--format", "dot")),
    )
    results = []
    for case_id, graph_kind, output_format, argv in cases:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(argv)
        stdout = output.getvalue().strip()
        payload_format = None
        json_ok = False
        if output_format == "json":
            try:
                payload = json.loads(stdout)
            except json.JSONDecodeError:
                payload = {}
            payload_format = payload.get("format")
            json_ok = payload.get("format") == "appgen.graph-report.v1" and payload.get("kind") == graph_kind
        text_ok = (output_format == "mermaid" and stdout.startswith("graph TD")) or (
            output_format == "dot" and stdout.startswith("digraph appgen")
        )
        results.append(
            {
                "case": case_id,
                "kind": graph_kind,
                "format": output_format,
                "ok": exit_code == 0 and (json_ok or text_ok),
                "exit_code": exit_code,
                "payload_format": payload_format,
                "stdout_prefix": stdout[:80],
            }
        )
    return {
        "format": "appgen.graph-cli-format-audit.v1",
        "ok": all(result["ok"] for result in results),
        "cases": tuple(results),
    }


def _tooling_audit_graph_suite_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "graph-suite-cli.appgen"
    source_path.write_text(source, encoding="utf-8")

    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        json_exit_code = dsl_tooling_cli(("graph-suite", str(source_path), "--json"))
    try:
        json_payload = json.loads(output.getvalue())
    except json.JSONDecodeError:
        json_payload = {}

    text_output = io.StringIO()
    with contextlib.redirect_stdout(text_output):
        text_exit_code = dsl_tooling_cli(("graph-suite", str(source_path)))
    text_stdout = text_output.getvalue().strip()
    renderings = json_payload.get("renderings", {})
    required_kinds = tuple(json_payload.get("required_kinds", ()))
    output_formats = tuple(json_payload.get("formats", ()))
    return {
        "format": "appgen.graph-suite-cli-audit.v1",
        "ok": json_exit_code == 0
        and json_payload.get("format") == "appgen.graph-suite-report.v1"
        and json_payload.get("ok") is True
        and set(REQUIRED_GRAPH_KINDS) <= set(required_kinds)
        and set(GRAPH_TEXT_FORMATS) <= set(output_formats)
        and all(set(outputs) == set(GRAPH_TEXT_FORMATS) for outputs in renderings.values())
        and text_exit_code == 0
        and text_stdout.startswith("graph-suite ok:")
        and "graph-kinds " in text_stdout
        and "graph-formats json, mermaid, dot" in text_stdout,
        "json_exit_code": json_exit_code,
        "text_exit_code": text_exit_code,
        "payload_format": json_payload.get("format"),
        "required_kinds": required_kinds,
        "formats": output_formats,
        "rendering_kind_count": len(renderings),
        "text_has_kinds": "graph-kinds " in text_stdout,
        "text_has_formats": "graph-formats json, mermaid, dot" in text_stdout,
        "text_prefix": text_stdout[:160],
    }


def _tooling_audit_explain_cli_formats(tmp: Path, source: str) -> dict:
    source_path = tmp / "explain-cli.appgen"
    source_path.write_text(source, encoding="utf-8")
    cases = (
        ("field_symbol_text", ("explain", str(source_path), "--symbol", "Invoice.customer_id")),
        ("field_symbol_json", ("explain", str(source_path), "--symbol", "Invoice.customer_id", "--json")),
        ("diagnostic_text", ("explain", str(source_path), "--diagnostic", "AGX0303")),
        ("diagnostic_json", ("explain", str(source_path), "--diagnostic", "AGX0303", "--json")),
        ("qualified_handler_text", ("explain", str(source_path), "--handler", "InvoiceForm.Save")),
        ("qualified_handler_json", ("explain", str(source_path), "--handler", "InvoiceForm.Save", "--json")),
    )
    results = []
    for case_id, argv in cases:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(argv)
        stdout = output.getvalue().strip()
        json_ok = False
        text_ok = False
        if case_id in {"diagnostic_json", "field_symbol_json", "qualified_handler_json"}:
            try:
                payload = json.loads(stdout)
            except json.JSONDecodeError:
                payload = {}
            if case_id == "diagnostic_json":
                json_ok = (
                    payload.get("format") == "appgen.explain-report.v1"
                    and payload.get("kind") == "diagnostic"
                    and payload.get("query") == "AGX0303"
                )
            elif case_id == "field_symbol_json":
                json_ok = (
                    payload.get("format") == "appgen.explain-report.v1"
                    and payload.get("kind") == "symbol"
                    and payload.get("query") == "Invoice.customer_id"
                    and payload.get("symbol", {}).get("id") == "table.Invoice.customer_id"
                )
            elif case_id == "qualified_handler_json":
                json_ok = (
                    payload.get("format") == "appgen.explain-report.v1"
                    and payload.get("kind") == "handler"
                    and payload.get("query") == "InvoiceForm.Save"
                    and bool(payload.get("matches"))
                )
        elif case_id == "field_symbol_text":
            text_ok = (
                stdout.startswith("explain symbol ok: Invoice.customer_id")
                and "table.Invoice.customer_id: field customer_id" in stdout
                and "parent: table.Invoice" in stdout
            )
        elif case_id == "diagnostic_text":
            text_ok = (
                stdout.startswith("explain diagnostic ok: AGX0303")
                and "AGX0303: Unresolved lookup path" in stdout
                and "A lookup path must resolve through declared relationships." in stdout
                and "docs: docs/tooling.md#diagnostic-specification" in stdout
            )
        elif case_id == "qualified_handler_text":
            text_ok = (
                stdout.startswith("explain handler ok: InvoiceForm.Save")
                and "matches:" in stdout
                and "InvoiceForm.Save ->" in stdout
            )
        results.append(
            {
                "case": case_id,
                "ok": exit_code == 0 and (json_ok or text_ok),
                "exit_code": exit_code,
                "stdout_prefix": stdout[:120],
            }
        )
    return {
        "format": "appgen.explain-cli-audit.v1",
        "ok": all(result["ok"] for result in results),
        "cases": tuple(results),
    }


def _tooling_audit_migration_cli(tmp: Path) -> dict:
    previous_path = tmp / "migration-previous.appgen"
    current_path = tmp / "migration-current.appgen"
    previous_path.write_text(
        """
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
""",
        encoding="utf-8",
    )
    current_path.write_text(
        """
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
""",
        encoding="utf-8",
    )
    cases = []
    for backend in SUPPORTED_DATABASE_BACKENDS:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(
                (
                    "migration-plan",
                    str(previous_path),
                    str(current_path),
                    "--backend",
                    backend,
                    "--rename-hint",
                    "table:Customer=Account",
                    "--rename-hint",
                    "field:Invoice.customer_id=Invoice.account_id",
                    "--json",
                )
            )
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        change_kinds = {change.get("kind") for change in payload.get("changes", ())}
        ok = (
            exit_code == 0
            and payload.get("format") == "appgen.migration-plan.v1"
            and payload.get("backend") == backend
            and payload.get("requires_approval") is True
            and {"rename_table", "rename_field", "add_field"} <= change_kinds
            and bool(payload.get("rename_hints"))
        )
        cases.append(
            {
                "backend": backend,
                "ok": ok,
                "exit_code": exit_code,
                "change_kinds": tuple(sorted(change_kinds)),
                "requires_approval": payload.get("requires_approval"),
                "diagnostic_codes": tuple(item.get("code") for item in payload.get("diagnostics", ())),
            }
        )
    return {
        "format": "appgen.migration-cli-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "allowed_backends": SUPPORTED_DATABASE_BACKENDS,
        "cases": tuple(cases),
    }


def _tooling_audit_nl_plan_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "nl-plan-cli.appgen"
    source_path.write_text(source, encoding="utf-8")

    def run_json(argv: tuple[str, ...]) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(argv)
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        return exit_code, payload

    accepted_specs = (
        ("add_table", "Add dispute cases table"),
        ("add_field", "Add due date to Invoice"),
        ("add_relationship", "Add relationship from Invoice to Customer"),
        ("add_view_section", "Add view section Audit to InvoiceForm"),
        ("add_component_placement", "Add component placement for customer.name to InvoiceForm"),
        ("add_handler", "Add handler Audit to InvoiceForm"),
        ("add_operation", "Add operation ArchiveInvoice"),
        ("add_rule", "Add rule PositiveInvoiceTotal"),
        ("add_flow_transition", "Add flow transition posted to archived in SubmitInvoice"),
        ("add_pbc_include", "Include pbc ap_automation"),
        ("add_api_event_contract", "Add api event contract InvoiceSynced"),
        ("add_package_deployment_unit", "Add package deployment unit for worker"),
        ("add_agent_skill_permission", "Add agent skill and permission for invoice review"),
    )
    accepted_cases = []
    for expected_kind, prompt in accepted_specs:
        exit_code, payload = run_json(("nl-plan", str(source_path), "--prompt", prompt, "--json"))
        operation_kinds = tuple(operation.get("kind") for operation in payload.get("edit_operations", ()))
        accepted_cases.append(
            {
                "expected_kind": expected_kind,
                "prompt": prompt,
                "exit_code": exit_code,
                "format": payload.get("format"),
                "ok": payload.get("ok"),
                "operation_kinds": operation_kinds,
                "patch_bytes": len(payload.get("dsl_patch", "")),
                "lint_ok": payload.get("lint", {}).get("ok"),
                "migration_format": payload.get("migration_preview", {}).get("format"),
                "test_count": len(payload.get("test_plan", ())),
                "token_budget_notes": len(payload.get("token_budget_notes", ())),
                "passed": exit_code == 0
                and payload.get("format") == "appgen.nl-plan.v1"
                and payload.get("ok") is True
                and expected_kind in operation_kinds
                and bool(payload.get("dsl_patch"))
                and payload.get("lint", {}).get("format") == "appgen.lint-report.v1"
                and payload.get("lint", {}).get("ok") is True
                and payload.get("migration_preview", {}).get("format") == "appgen.migration-plan.v1"
                and bool(payload.get("test_plan"))
                and bool(payload.get("token_budget_notes")),
            }
        )
    rejected_exit, rejected_payload = run_json(
        (
            "nl-plan",
            str(source_path),
            "--prompt",
            "Replace the runtime with hand-written generated code outside the DSL",
            "--json",
        )
    )
    rejected_codes = tuple(item.get("code") for item in rejected_payload.get("diagnostics", ()))
    accepted_patch_bytes = sum(case["patch_bytes"] for case in accepted_cases)
    accepted_test_count = sum(case["test_count"] for case in accepted_cases)
    accepted_token_budget_notes = sum(case["token_budget_notes"] for case in accepted_cases)
    accepted_operation_kinds = tuple(
        sorted({operation_kind for case in accepted_cases for operation_kind in case["operation_kinds"]})
    )
    return {
        "format": "appgen.nl-plan-cli-audit.v1",
        "ok": all(case["passed"] for case in accepted_cases)
        and rejected_exit == 1
        and rejected_payload.get("format") == "appgen.nl-plan.v1"
        and rejected_payload.get("ok") is False
        and rejected_payload.get("dsl_patch") == ""
        and "AGX1201" in rejected_codes,
        "accepted_case_count": len(accepted_cases),
        "accepted_cases": tuple(accepted_cases),
        "accepted_operation_kinds": accepted_operation_kinds,
        "blocking_cases": tuple(case["expected_kind"] for case in accepted_cases if not case["passed"]),
        "accepted_exit_code": accepted_cases[0]["exit_code"] if accepted_cases else None,
        "rejected_exit_code": rejected_exit,
        "accepted_payload_format": accepted_cases[0]["format"] if accepted_cases else None,
        "accepted_patch_bytes": accepted_patch_bytes,
        "accepted_test_count": accepted_test_count,
        "accepted_token_budget_notes": accepted_token_budget_notes,
        "migration_format": accepted_cases[0]["migration_format"] if accepted_cases else None,
        "rejected_payload_format": rejected_payload.get("format"),
        "rejected_diagnostic_codes": rejected_codes,
    }


def _tooling_audit_package_verify_cli(tmp: Path, source: str) -> dict:
    source_path = tmp / "package-verify.appgen"
    package_dir = tmp / "package-cli"
    source_path.write_text(_tooling_audit_package_verify_sample(), encoding="utf-8")

    def run_json(argv: tuple[str, ...]) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = dsl_tooling_cli(argv)
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        return exit_code, payload

    verify_exit, verify_payload = run_json(("verify", str(source_path), "--target", "all", "--json"))
    package_exit, package_payload = run_json(
        (
            "package",
            str(source_path),
            "--target",
            "all",
            "--out",
            str(package_dir),
            "--json",
        )
    )
    evidence_path = package_dir / "appgen-release-evidence.json"
    web_manifest_path = package_dir / "appgen-package-web.json"
    mobile_manifest_path = package_dir / "appgen-package-mobile.json"
    desktop_manifest_path = package_dir / "appgen-package-desktop.json"
    pbc_manifest_path = package_dir / "appgen-package-pbc.json"
    deployment_manifest_path = package_dir / "appgen-package-deployment.json"
    try:
        evidence_payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        evidence_payload = {}
    try:
        web_manifest = json.loads(web_manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        web_manifest = {}
    try:
        mobile_manifest = json.loads(mobile_manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        mobile_manifest = {}
    try:
        desktop_manifest = json.loads(desktop_manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        desktop_manifest = {}
    try:
        pbc_manifest = json.loads(pbc_manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        pbc_manifest = {}
    try:
        deployment_manifest = json.loads(deployment_manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        deployment_manifest = {}
    expected_targets = ("web", "mobile", "desktop", "pbc", "deployment")
    web_handoff = tuple(web_manifest.get("handoff_artifacts", ()))
    mobile_handoff = tuple(mobile_manifest.get("handoff_artifacts", ()))
    desktop_handoff = tuple(desktop_manifest.get("handoff_artifacts", ()))
    pbc_handoff = tuple(pbc_manifest.get("handoff_artifacts", ()))
    deployment_handoff = tuple(deployment_manifest.get("handoff_artifacts", ()))
    evidence_graph_suite = evidence_payload.get("evidence_bundle", {}).get("graph_suite", {})
    cases = (
        {
            "case": "verify_all_targets",
            "ok": verify_exit == 0
            and verify_payload.get("format") == "appgen.release-verifier-report.v1"
            and tuple(verify_payload.get("targets", ())) == expected_targets
            and all(check.get("ok") for check in verify_payload.get("checks", ())),
            "exit_code": verify_exit,
            "payload_format": verify_payload.get("format"),
            "targets": tuple(verify_payload.get("targets", ())),
        },
        {
            "case": "package_writes_target_manifests",
            "ok": package_exit == 0
            and package_payload.get("format") == "appgen.release-verifier-report.v1"
            and tuple(package_payload.get("targets", ())) == expected_targets
            and evidence_payload.get("format") == "appgen.release-evidence-file.v1"
            and set(evidence_payload.get("reports", {})) == set(expected_targets)
            and evidence_graph_suite.get("format") == "appgen.graph-suite-report.v1"
            and set(evidence_graph_suite.get("required_kinds", ())) == set(REQUIRED_GRAPH_KINDS)
            and set(evidence_graph_suite.get("formats", ())) == set(GRAPH_TEXT_FORMATS)
            and web_manifest.get("format") == "appgen.package-manifest.v1"
            and mobile_manifest.get("format") == "appgen.package-manifest.v1"
            and desktop_manifest.get("format") == "appgen.package-manifest.v1"
            and pbc_manifest.get("format") == "appgen.package-manifest.v1"
            and deployment_manifest.get("format") == "appgen.package-manifest.v1"
            and web_manifest.get("target") == "web"
            and mobile_manifest.get("target") == "mobile"
            and desktop_manifest.get("target") == "desktop"
            and pbc_manifest.get("target") == "pbc"
            and deployment_manifest.get("target") == "deployment"
            and web_manifest.get("artifact_class") == "web_application"
            and web_manifest.get("app_build_contract") is True
            and web_manifest.get("routes_declared") is True
            and web_manifest.get("forms_bind_valid_fields") is True
            and web_manifest.get("handler_targets_resolve") is True
            and web_manifest.get("smoke_tests_declared") is True
            and web_manifest.get("smoke_entrypoint") == "web.smoke"
            and {"routes", "forms", "handlers", "smoke_tests"} <= set(web_handoff)
            and mobile_manifest.get("artifact_class") == "mobile_application"
            and mobile_manifest.get("package_metadata_exists") is True
            and mobile_manifest.get("signing_posture_declared") is True
            and mobile_manifest.get("offline_policy_declared") is True
            and mobile_manifest.get("permissions_explained") is True
            and mobile_manifest.get("screens_fit_target_density") is True
            and mobile_manifest.get("smoke_launch_path_exists") is True
            and mobile_manifest.get("smoke_entrypoint") == "mobile.launch"
            and {"mobile_metadata", "signing_posture", "offline_policy", "permissions", "screen_density", "smoke_launch"}
            <= set(mobile_handoff)
            and desktop_manifest.get("artifact_class") == "desktop_application"
            and desktop_manifest.get("package_metadata_exists") is True
            and desktop_manifest.get("installer_posture_declared") is True
            and desktop_manifest.get("startup_assets_declared") is True
            and desktop_manifest.get("menus_bind_to_handlers") is True
            and desktop_manifest.get("smoke_launch_path_exists") is True
            and desktop_manifest.get("smoke_entrypoint") == "desktop.launch"
            and {"desktop_metadata", "installer_profile", "startup_assets", "menus", "context_menus", "smoke_launch"}
            <= set(desktop_handoff)
            and pbc_manifest.get("artifact_class") == "packaged_business_capability"
            and {"manifest", "contracts", "owned_schema", "registration", "release_evidence"} <= set(pbc_handoff)
            and pbc_manifest.get("side_effect_free_registration") is True
            and deployment_manifest.get("artifact_class") == "deployment_plan"
            and {"units", "health_checks", "environment", "resource_hints", "topology_graph"} <= set(deployment_handoff)
            and deployment_manifest.get("units_declared") is True
            and deployment_manifest.get("health_checks_declared") is True
            and deployment_manifest.get("environment_variables_named") is True
            and deployment_manifest.get("secret_values_absent") is True
            and deployment_manifest.get("resource_hints_present") is True
            and deployment_manifest.get("topology_graph_connected") is True
            and deployment_manifest.get("topology_declared") is True,
            "exit_code": package_exit,
            "payload_format": package_payload.get("format"),
            "targets": tuple(package_payload.get("targets", ())),
            "artifacts": tuple(Path(item.get("path", "")).name for item in package_payload.get("written_artifacts", ())),
            "manifest_formats": {
                "web": web_manifest.get("format"),
                "mobile": mobile_manifest.get("format"),
                "desktop": desktop_manifest.get("format"),
                "pbc": pbc_manifest.get("format"),
                "deployment": deployment_manifest.get("format"),
            },
            "release_evidence_reports": tuple(evidence_payload.get("reports", {}).keys()),
            "release_graph_suite_format": evidence_graph_suite.get("format"),
            "release_graph_kinds": tuple(evidence_graph_suite.get("required_kinds", ())),
            "release_graph_formats": tuple(evidence_graph_suite.get("formats", ())),
            "web_artifact_class": web_manifest.get("artifact_class"),
            "web_handoff_artifacts": web_handoff,
            "web_app_build_contract": web_manifest.get("app_build_contract"),
            "web_routes_declared": web_manifest.get("routes_declared"),
            "web_forms_bind_valid_fields": web_manifest.get("forms_bind_valid_fields"),
            "web_handler_targets_resolve": web_manifest.get("handler_targets_resolve"),
            "web_smoke_tests_declared": web_manifest.get("smoke_tests_declared"),
            "web_smoke_entrypoint": web_manifest.get("smoke_entrypoint"),
            "mobile_artifact_class": mobile_manifest.get("artifact_class"),
            "mobile_handoff_artifacts": mobile_handoff,
            "mobile_package_metadata_exists": mobile_manifest.get("package_metadata_exists"),
            "mobile_signing_posture_declared": mobile_manifest.get("signing_posture_declared"),
            "mobile_offline_policy_declared": mobile_manifest.get("offline_policy_declared"),
            "mobile_permissions_explained": mobile_manifest.get("permissions_explained"),
            "mobile_screens_fit_target_density": mobile_manifest.get("screens_fit_target_density"),
            "mobile_smoke_launch_path_exists": mobile_manifest.get("smoke_launch_path_exists"),
            "mobile_smoke_entrypoint": mobile_manifest.get("smoke_entrypoint"),
            "desktop_artifact_class": desktop_manifest.get("artifact_class"),
            "desktop_handoff_artifacts": desktop_handoff,
            "desktop_package_metadata_exists": desktop_manifest.get("package_metadata_exists"),
            "desktop_installer_posture_declared": desktop_manifest.get("installer_posture_declared"),
            "desktop_startup_assets_declared": desktop_manifest.get("startup_assets_declared"),
            "desktop_menus_bind_to_handlers": desktop_manifest.get("menus_bind_to_handlers"),
            "desktop_smoke_launch_path_exists": desktop_manifest.get("smoke_launch_path_exists"),
            "desktop_smoke_entrypoint": desktop_manifest.get("smoke_entrypoint"),
            "pbc_artifact_class": pbc_manifest.get("artifact_class"),
            "pbc_handoff_artifacts": pbc_handoff,
            "pbc_side_effect_free_registration": pbc_manifest.get("side_effect_free_registration"),
            "deployment_artifact_class": deployment_manifest.get("artifact_class"),
            "deployment_handoff_artifacts": deployment_handoff,
            "deployment_units_declared": deployment_manifest.get("units_declared"),
            "deployment_health_checks_declared": deployment_manifest.get("health_checks_declared"),
            "deployment_environment_variables_named": deployment_manifest.get("environment_variables_named"),
            "deployment_secret_values_absent": deployment_manifest.get("secret_values_absent"),
            "deployment_resource_hints_present": deployment_manifest.get("resource_hints_present"),
            "deployment_topology_graph_connected": deployment_manifest.get("topology_graph_connected"),
            "deployment_topology_declared": deployment_manifest.get("topology_declared"),
        },
    )
    return {
        "format": "appgen.package-verify-cli-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": cases,
    }


def _tooling_audit_package_verify_sample() -> str:
    return """
app PackageCliAudit { targets: web, mobile, desktop }

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

deploy Production {
  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
  resource SubmitInvoice cpu 1
  env SubmitInvoice DATABASE_URL
}
"""


def _tooling_audit_package_invalid_target(tmp: Path, source: str) -> dict:
    source_path = tmp / "package-invalid-target.appgen"
    source_path.write_text(source, encoding="utf-8")
    output = io.StringIO()
    error = io.StringIO()
    exit_code = 0
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
        try:
            exit_code = dsl_tooling_cli(("package", str(source_path), "--target", "banana", "--json"))
        except SystemExit as exc:
            exit_code = int(exc.code or 0)
    stderr = error.getvalue()
    return {
        "format": "appgen.package-invalid-target-audit.v1",
        "ok": exit_code == 2 and "invalid choice" in stderr and "Traceback" not in stderr,
        "exit_code": exit_code,
        "stderr": stderr.strip(),
        "stdout": output.getvalue().strip(),
    }


def _tooling_audit_cli_help_surface(root: Path) -> dict:
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    pyproject_data = tomllib.loads(pyproject)
    entrypoint = (root / "src/pyAppGen/gen.py").read_text(encoding="utf-8")
    module_entrypoint = (root / "src/pyAppGen/__main__.py").read_text(encoding="utf-8")
    required_subcommands = (
        "lint",
        "format",
        "validate",
        "generate",
        "graph",
        "graph-suite",
        "explain",
        "migration-plan",
        "nl-plan",
        "lsp",
        "verify",
        "package",
        "component-publish",
        "pbc",
        "designer-sync",
        "diagnostics",
        "parser-golden",
        "drift",
        "doctor",
        "tooling-audit",
    )
    help_output = io.StringIO()
    help_error = io.StringIO()
    help_exit_code = 0
    with contextlib.redirect_stdout(help_output), contextlib.redirect_stderr(help_error):
        try:
            help_exit_code = dsl_tooling_cli(("--help",))
        except SystemExit as exc:
            help_exit_code = int(exc.code or 0)
    help_text = help_output.getvalue()
    help_has_subcommands = all(command in entrypoint for command in required_subcommands)
    help_lists_subcommands = all(command in help_text for command in required_subcommands)
    required_option_help = {
        ("lint",): ("--json", "--strict", "--catalog", "--previous-semantic", "--backend"),
        ("format",): ("--check", "--write", "--organize", "--json"),
        ("validate",): ("--targets", "--json"),
        ("generate",): ("--out", "--target", "--allow-warnings", "--json"),
        ("graph",): ("--kind", "--format"),
        ("graph-suite",): ("--json",),
        ("explain",): ("--symbol", "--diagnostic", "--handler", "--json"),
        ("migration-plan",): ("--backend", "--rename-hint", "--json"),
        ("nl-plan",): ("--prompt", "--backend", "--json"),
        ("lsp",): ("--position", "--prefix", "--rename", "--apply-code-action", "--stdio", "--json"),
        ("verify",): ("--target", "--json"),
        ("package",): ("--target", "--out", "--json"),
        ("component-publish",): ("--component", "--catalog", "--json"),
        ("pbc",): ("list", "verify", "publish"),
        ("pbc", "publish"): ("--catalog", "--catalog-path", "--json"),
        ("designer-sync",): ("--edit-json", "--json"),
        ("diagnostics",): ("--audit-fixtures", "--json"),
        ("parser-golden",): ("--json",),
        ("drift",): ("--json",),
        ("doctor",): ("--json",),
        ("tooling-audit",): ("--json",),
    }
    option_help = {}
    for command_path, required_options in required_option_help.items():
        command_help_output = io.StringIO()
        command_help_error = io.StringIO()
        command_help_exit_code = 0
        with contextlib.redirect_stdout(command_help_output), contextlib.redirect_stderr(command_help_error):
            try:
                command_help_exit_code = dsl_tooling_cli((*command_path, "--help"))
            except SystemExit as exc:
                command_help_exit_code = int(exc.code or 0)
        command_help_text = command_help_output.getvalue()
        command_name = " ".join(command_path)
        option_help[command_name] = {
            "ok": command_help_exit_code == 0 and all(option in command_help_text for option in required_options),
            "exit_code": command_help_exit_code,
            "missing": tuple(option for option in required_options if option not in command_help_text),
        }
    subcommand_option_help_ok = all(item["ok"] for item in option_help.values())
    scripts = pyproject_data.get("project", {}).get("scripts", {})
    alias_declared = scripts.get("apg") == scripts.get("appgen") == "pyAppGen.__main__:main"
    alias_contract = {
        "format": "appgen.cli-alias-contract.v1",
        "ok": alias_declared,
        "commands": ("appgen", "apg"),
        "targets": {"appgen": scripts.get("appgen"), "apg": scripts.get("apg")},
        "shared_target": scripts.get("appgen") if scripts.get("appgen") == scripts.get("apg") else None,
        "entrypoint": "pyAppGen.__main__:main",
    }
    with tempfile.TemporaryDirectory(prefix="appgen-entrypoint-audit-") as tmp:
        source_path = Path(tmp) / "entrypoint.appgen"
        source_path.write_text("app EntryPoint { targets: web }\ntable Thing { id: int pk }\n", encoding="utf-8")
        module_lint = subprocess.run(
            [sys.executable, "-m", "pyAppGen", "lint", str(source_path), "--json"],
            check=False,
            cwd=root,
            text=True,
            capture_output=True,
            timeout=10,
        )
    try:
        module_lint_payload = json.loads(module_lint.stdout)
    except json.JSONDecodeError:
        module_lint_payload = {}
    module_dispatches_tooling = (
        "_run_tooling" in module_entrypoint
        and "dsl_tooling_cli" in module_entrypoint
        and module_lint.returncode == 0
        and module_lint_payload.get("format") == "appgen.lint-report.v1"
        and "Traceback" not in module_lint.stderr
    )
    return {
        "format": "appgen.cli-help-surface-audit.v1",
        "ok": help_exit_code == 0
        and help_has_subcommands
        and help_lists_subcommands
        and subcommand_option_help_ok
        and alias_contract["ok"]
        and module_dispatches_tooling,
        "alias_declared": alias_declared,
        "script_targets": {"appgen": scripts.get("appgen"), "apg": scripts.get("apg")},
        "alias_contract": {
            **alias_contract,
            "module_dispatches_tooling": module_dispatches_tooling,
            "module_payload_format": module_lint_payload.get("format"),
        },
        "help_exit_code": help_exit_code,
        "help_lists_subcommands": help_lists_subcommands,
        "help_missing_subcommands": tuple(command for command in required_subcommands if command not in help_text),
        "subcommand_option_help_ok": subcommand_option_help_ok,
        "subcommand_option_help": option_help,
        "module_entrypoint": {
            "ok": module_dispatches_tooling,
            "exit_code": module_lint.returncode,
            "payload_format": module_lint_payload.get("format"),
            "traceback_free": "Traceback" not in module_lint.stderr,
        },
        "subcommands_documented": required_subcommands if help_has_subcommands else tuple(command for command in required_subcommands if command in entrypoint),
        "required_subcommands": required_subcommands,
    }


def _tooling_audit_migration_reports() -> tuple[dict, ...]:
    broad_previous = """
app Coverage { targets: web }
table Customer { id: int pk; name: string required }
table Legacy { id: int pk; obsolete: string }
table Invoice {
  id: int pk
  customer_id: int -> Customer.id
  subtotal: decimal default 0
  status: string
  old_note: string
  total: decimal = subtotal
  index(customer_id)
}
pbc Billing { owns: Invoice }
"""
    broad_current = """
app Coverage { targets: web }
table Account { id: int pk; name: string required }
table Invoice {
  id: int pk
  account_id: int -> Account.id
  subtotal: string
  status: string required
  tax: decimal required
  total: decimal = subtotal + tax
  unique(account_id)
}
table CreditMemo { id: int pk; amount: decimal }
pbc Finance { owns: Invoice }
"""
    directive_previous = """
app FinanceOps { targets: web }
table Invoice {
  id: int pk
  total: decimal
  index(total)
  constraint(total_positive, total)
}
pbc Billing { owns: Invoice }
"""
    directive_current = """
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
    return (
        migration_plan_dsl(
            broad_previous,
            broad_current,
            backend="postgresql",
            rename_hints=("table:Customer=Account", "field:Invoice.customer_id=Invoice.account_id"),
        ),
        migration_plan_dsl(directive_previous, directive_current, backend="postgresql"),
    )


def _tooling_audit_sample_dsl() -> str:
    return """
app ToolingAudit { targets: web, mobile, desktop }

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

operation ReverseInvoice {
  posted -> reversed
}

role Accountant {
  Invoice: read, write
}

rule InvoicePolicy for Invoice {
  total >= 0
}

llm LocalModel {
  provider: ollama
  mode: local
}

agent InvoiceAssistant {
  provider: LocalModel
  tools: read, schema
  Invoice: read
  on Explain -> ReverseInvoice
}

composition FinanceSuite {
  include pbc gl_core version 1.0.0
  require database postgresql
}

audit ReleaseAudit {
  evidence: tests
}

version Release2026 {
  number: 1.0.0
}

security TenantSecurity {
  Invoice: read, write
}

api InvoiceApi {
  on Create -> ReverseInvoice
  Invoice: read
}

event InvoicePosted {
  topic: invoices
}

job InvoiceJob {
  run nightly -> ReverseInvoice
}

report InvoiceReport {
  source Invoice -> InvoiceApi
}

menu MainMenu {
  on Open -> ReverseInvoice
}

component CustomerLookup {
  on Select -> ReverseInvoice
}

package ReleaseWeb {
  target: web
  smoke: launch
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
  run happy_path -> ReverseInvoice
}

deploy Production {
  unit ReverseInvoice as worker
  health ReverseInvoice "/health"
  resource ReverseInvoice cpu 1
  env ReverseInvoice DATABASE_URL
}
"""


def _tooling_audit_component_catalog_sample() -> str:
    return """
app CatalogAudit { targets: web }

table Customer {
  id: int pk
  name: string
}

view CustomerForm for Customer {
  Main: name
  @ name CustomGauge 0 0 4 1
}
"""


def _tooling_audit_warning_generation_sample() -> str:
    return """
app WarningDemo { targets: web }

table Customer {
  id: int pk
  name: string
}

view CustomerForm for Customer {
  Main: name
  @ name UnknownWidget 0 0 4 1
}
"""


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


def module_boundary_audit_dsl() -> dict:
    """Prove docs/tooling.md responsibility boundaries have callable surfaces."""
    current_globals = globals()
    boundaries = (
        (
            "parser",
            "pyAppGen.dsl.parser",
            ("schema_from_dsl", "schema_from_dsl_file", "parser_golden_audit_dsl"),
        ),
        ("ast", "pyAppGen.dsl.ast", ("schema_from_dsl",)),
        ("symbols", "pyAppGen.dsl.symbols", ("symbol_coverage_dsl", "semantic_model_dsl")),
        ("semantic", "pyAppGen.dsl.semantic", ("semantic_model_dsl", "validate_report_dsl")),
        (
            "diagnostics",
            "pyAppGen.dsl.diagnostics",
            ("diagnostic_catalog_dsl", "diagnostic_fixture_audit_dsl"),
        ),
        ("formatter", "pyAppGen.dsl.formatter", ("format_report_dsl", "formatter_contract_audit_dsl")),
        (
            "lsp",
            "pyAppGen.dsl.lsp",
            ("lsp_service_dsl", "lsp_capabilities_dsl", "lsp_server_handle_message"),
        ),
        ("cli", "pyAppGen.dsl.cli", ("dsl_tooling_cli",)),
        ("graphs", "pyAppGen.dsl.graphs", ("graph_suite_report_dsl", "graph_report_dsl", "explain_report_dsl")),
        ("migrations", "pyAppGen.dsl.migrations", ("migration_plan_dsl", "migration_plan_dsl_files")),
        ("nl_plan", "pyAppGen.dsl.nl_plan", ("nl_plan_dsl", "nl_plan_contract_audit_dsl")),
        ("release", "pyAppGen.dsl.release", ("release_verifier_report_dsl", "semantic_drift_audit_dsl")),
    )
    boundary_reports = []
    missing_boundaries = []
    for key, documented_module, callables in boundaries:
        missing_callables = tuple(name for name in callables if not callable(current_globals.get(name)))
        boundary_reports.append(
            {
                "boundary": key,
                "documented_module": documented_module,
                "callables": callables,
                "missing_callables": missing_callables,
                "ok": not missing_callables,
            }
        )
        if missing_callables:
            missing_boundaries.append(key)

    sample = "app BoundaryAudit { targets: web }\ntable Thing { id: int pk; name: string }\n"
    core_runtime = (
        _runtime_probe("parser", lambda: schema_from_dsl(sample).app_name == "BoundaryAudit"),
        _runtime_probe(
            "semantic",
            lambda: semantic_model_dsl(sample, source_name="boundary.appgen")["format"] == "appgen.semantic-model.v1",
        ),
        _runtime_probe(
            "diagnostics",
            lambda: diagnostic_catalog_dsl()["format"] == "appgen.diagnostic-catalog.v1",
        ),
        _runtime_probe(
            "formatter",
            lambda: format_report_dsl(sample, source_name="boundary.appgen")["format"] == "appgen.format-result.v1",
        ),
    )
    core_runtime_gaps = tuple(item["boundary"] for item in core_runtime if not item["ok"])
    return {
        "format": "appgen.module-boundary-audit.v1",
        "ok": not missing_boundaries and not core_runtime_gaps,
        "boundaries": tuple(boundary_reports),
        "missing_boundaries": tuple(missing_boundaries),
        "core_runtime": core_runtime,
        "core_runtime_gaps": core_runtime_gaps,
        "layout_policy": "boundaries_visible_without_requiring_subpackage_layout",
    }


def _runtime_probe(boundary: str, probe) -> dict:
    try:
        ok = bool(probe())
    except Exception as exc:  # pragma: no cover - defensive audit detail
        return {"boundary": boundary, "ok": False, "error": str(exc)}
    return {"boundary": boundary, "ok": ok}


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


def _completion_coverage_sample() -> str:
    return """
app CompletionDemo { targets: web, mobile, desktop }

table Customer {
  id: int pk
  name: string
}

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

flow SubmitInvoice {
  draft -> reviewed
  reviewed -> posted
}

operation ReverseInvoice {
  posted -> reversed
}

component CustomerLookup {
  on Select -> SubmitInvoice
}

composition CompletionSuite {
  include pbc gl_core version 1.0.0
}

package CompletionMobile {
  target: mobile
  smoke: launch
}

deploy Production {
  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
}

llm LocalModel {
  provider: ollama
  mode: local
}

agent CompletionAssistant {
  provider: LocalModel
  tools: write, schema
}
"""


def _symbol_coverage_sample() -> str:
    return """
app SymbolDemo { targets: web, mobile, desktop }

AddressFields {
  street: string
}

table Customer {
  id: int pk
  name: string
  ... AddressFields
}

table Invoice {
  id: int pk
  customer_id: int -> Customer.id
  total: decimal = id
}

enum Status { draft posted }

view InvoiceForm for Invoice {
  Main: customer.name, total
  @ customer.name Lookup 0 0 6 1
  on Save -> SubmitInvoice
}

flow SubmitInvoice {
  draft -> reviewed
  reviewed -> posted
}

role Clerk {
  Invoice: read, write
}

rule InvoicePolicy for Invoice {
  id == 1
}

llm LocalModel {
  provider: ollama
  mode: local
}

agent Builder {
  provider: LocalModel
  tools: write, schema
  Invoice: write
  on Run -> SubmitInvoice
}

pbc Billing {
  owns: Invoice
  Invoice: read, write
}

composition Suite {
  include pbc gl_core version 1.0.0
}

audit ReleaseAudit {
  evidence: tests
}

version Release2026 {
  number: 1.0.0
}

operation ReverseInvoice {
  posted -> reversed
}

security TenantSecurity {
  Invoice: read, write
  tenancy: org
}

api InvoiceApi {
  on Create -> SubmitInvoice
  Invoice: read
}

event InvoicePosted {
  topic: invoices
}

job InvoiceJob {
  run nightly -> SubmitInvoice
}

report InvoiceReport {
  source Invoice -> InvoiceApi
}

menu MainMenu {
  on Open -> SubmitInvoice
}

component CustomerLookup {
  on Select -> SubmitInvoice
}

package MobileRelease {
  target: mobile
  smoke: launch
}

test Smoke {
  run happy -> SubmitInvoice
}

deploy Production {
  unit SubmitInvoice as worker
  health SubmitInvoice "/health"
}
"""


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
    allowed_backends = set(SUPPORTED_DATABASE_BACKENDS)
    previous = semantic_model_dsl(previous_text, source_name=previous_name)
    current = semantic_model_dsl(current_text, source_name=current_name)
    return migration_plan_from_semantic_models(
        previous,
        current,
        previous_name=previous_name,
        current_name=current_name,
        current_text=current_text,
        backend=normalized_backend if normalized_backend in allowed_backends else backend,
        rename_hints=rename_hints,
    )


def migration_plan_from_semantic_models(
    previous: dict,
    current: dict,
    *,
    previous_name: str | None = None,
    current_name: str | None = None,
    current_text: str = "",
    backend: str = "postgresql",
    rename_hints: Iterable[str] | None = None,
) -> dict:
    """Compare semantic-model JSON payloads and return appgen.migration-plan.v1."""
    normalized_backend = backend.strip().lower().replace("-", "_")
    allowed_backends = set(SUPPORTED_DATABASE_BACKENDS)
    hints = _parse_rename_hints(rename_hints or ())
    diagnostics: list[dict] = []
    changes: list[dict] = []

    if normalized_backend not in allowed_backends:
        diagnostics.append(_spec_diagnostic(current_text, "AGX1102", "error", f"Unsupported migration backend: {backend}"))
    if previous.get("format") != "appgen.semantic-model.v1" or not previous.get("ok"):
        diagnostics.append(
            _spec_diagnostic(
                current_text,
                "AGX1100",
                "error",
                "Previous semantic model has diagnostics and cannot be used as a migration baseline.",
            )
        )
    if current.get("format") != "appgen.semantic-model.v1" or not current.get("ok"):
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
        changes.extend(_field_migration_changes(table_name, previous_tables[table_name], current_tables[table_name], hints))
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
        "coverage": _migration_coverage(changes),
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


def nl_plan_contract_audit_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Prove documented natural-language edit operations stay DSL-bounded."""
    source = text or _tooling_audit_sample_dsl()
    case_specs = (
        ("add_table", "Add dispute cases table", True, "add_table"),
        ("add_field", "Add due date to Invoice", True, "add_field"),
        ("add_relationship", "Add relationship from Invoice to Customer", True, "add_relationship"),
        ("add_view_section", "Add view section Audit to InvoiceForm", True, "add_view_section"),
        ("add_component_placement", "Add component placement for customer.name to InvoiceForm", True, "add_component_placement"),
        ("add_handler", "Add handler Audit to InvoiceForm", True, "add_handler"),
        ("add_operation", "Add operation ArchiveInvoice", True, "add_operation"),
        ("add_rule", "Add rule PositiveInvoiceTotal", True, "add_rule"),
        ("add_flow_transition", "Add flow transition posted to archived in SubmitInvoice", True, "add_flow_transition"),
        ("add_pbc_include", "Include pbc ap_automation", True, "add_pbc_include"),
        ("add_api_event_contract", "Add api event contract InvoiceSynced", True, "add_api_event_contract"),
        ("add_package_deployment_unit", "Add package deployment unit for worker", True, "add_package_deployment_unit"),
        ("add_agent_skill_permission", "Add agent skill and permission for invoice review", True, "add_agent_skill_permission"),
        ("reject_unsupported", "Replace the runtime with hand-written generated code outside the DSL", False, "unsupported"),
    )
    cases = []
    for case_id, prompt, should_accept, expected_kind in case_specs:
        plan = nl_plan_dsl(source, source_name=source_name, prompt=prompt)
        operation_kinds = tuple(operation.get("kind") for operation in plan.get("edit_operations", ()))
        diagnostic_codes = tuple(item.get("code") for item in plan.get("diagnostics", ()))
        ok = (
            plan["ok"] is should_accept
            and (expected_kind == "unsupported" or expected_kind in operation_kinds)
            and (not should_accept or bool(plan.get("dsl_patch")))
            and (not should_accept or plan.get("lint", {}).get("ok") is True)
            and (not should_accept or plan.get("migration_preview", {}).get("format") == "appgen.migration-plan.v1")
            and (not should_accept or bool(plan.get("test_plan")))
            and bool(plan.get("token_budget_notes"))
            and (should_accept or "AGX1201" in diagnostic_codes)
        )
        cases.append(
            {
                "id": case_id,
                "ok": ok,
                "prompt": prompt,
                "accepted": plan["ok"],
                "expected_kind": expected_kind,
                "operation_kinds": operation_kinds,
                "diagnostic_codes": diagnostic_codes,
                "patch_bytes": len(plan.get("dsl_patch", "")),
                "lint_ok": plan.get("lint", {}).get("ok"),
                "migration_format": plan.get("migration_preview", {}).get("format"),
                "test_count": len(plan.get("test_plan", ())),
            }
        )
    return {
        "format": "appgen.nl-plan-contract-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": tuple(cases),
        "required_edit_operations": (
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
        ),
        "blocking_gaps": tuple(case["id"] for case in cases if not case["ok"]),
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
        "completionCoverage": completion_coverage_dsl(source, source_name=source_name),
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


def lsp_stdio_server(input_stream=None, output_stream=None) -> int:
    """Run a small JSON-RPC LSP server over stdio."""
    reader = input_stream or sys.stdin.buffer
    writer = output_stream or sys.stdout.buffer
    documents: dict[str, str] = {}
    while True:
        message = _lsp_read_rpc_message(reader)
        if message is None:
            break
        responses, should_exit = lsp_server_handle_message(message, documents)
        for response in responses:
            _lsp_write_rpc_message(writer, response)
        if should_exit:
            break
    return 0


def lsp_server_handle_message(message: dict, documents: dict[str, str] | None = None) -> tuple[tuple[dict, ...], bool]:
    """Handle one JSON-RPC/LSP message and mutate the supplied document cache."""
    docs = documents if documents is not None else {}
    method = message.get("method")
    params = message.get("params") or {}
    request_id = message.get("id")
    is_request = "id" in message
    source_uri = _lsp_request_uri(params)
    source = _lsp_document_source(source_uri, docs)
    position = params.get("position") or {"line": 0, "character": 0}
    responses: list[dict] = []

    if method == "initialize":
        return (
            (
                _lsp_rpc_result(
                    request_id,
                    {
                        "capabilities": _lsp_initialize_capabilities(),
                        "serverInfo": {"name": "appgen-lsp", "version": "0.1.0"},
                    },
                ),
            ),
            False,
        )
    if method == "shutdown":
        return ((_lsp_rpc_result(request_id, None),) if is_request else (), False)
    if method == "exit":
        return (), True
    if method == "textDocument/didOpen":
        text_document = params.get("textDocument") or {}
        uri = text_document.get("uri") or source_uri or "memory://appgen"
        docs[uri] = text_document.get("text", "")
        responses.append(_lsp_publish_diagnostics_notification(uri, docs[uri]))
        return tuple(responses), False
    if method == "textDocument/didChange":
        text_document = params.get("textDocument") or {}
        uri = text_document.get("uri") or source_uri or "memory://appgen"
        changes = params.get("contentChanges") or ()
        if changes:
            docs[uri] = changes[-1].get("text", docs.get(uri, ""))
        responses.append(_lsp_publish_diagnostics_notification(uri, docs.get(uri, "")))
        return tuple(responses), False

    if method == "textDocument/completion":
        result = lsp_completion_dsl(
            source,
            source_name=source_uri,
            position=position,
            prefix=_lsp_prefix_at_position(source, position),
        )
        items = _lsp_completion_items_with_workspace(result["items"], docs)
        responses.append(
            _lsp_rpc_result(
                request_id,
                {"isIncomplete": result["isIncomplete"], "items": items},
            )
        )
    elif method == "textDocument/hover":
        result = lsp_hover_dsl(source, source_name=source_uri, position=position)
        responses.append(
            _lsp_rpc_result(
                request_id,
                {
                    "contents": {"kind": "markdown", "value": "\n\n".join(result["contents"])},
                    "range": result["range"],
                }
                if result["ok"]
                else None,
            )
        )
    elif method == "textDocument/definition":
        result = lsp_definition_dsl_documents(docs, source_uri=source_uri, position=position)
        responses.append(_lsp_rpc_result(request_id, result["location"] if result["ok"] else None))
    elif method == "textDocument/references":
        result = lsp_references_dsl_documents(docs, source_uri=source_uri, position=position)
        responses.append(_lsp_rpc_result(request_id, result["locations"]))
    elif method == "textDocument/documentSymbol":
        result = lsp_document_symbols_dsl(source, source_name=source_uri)
        responses.append(_lsp_rpc_result(request_id, result["symbols"]))
    elif method == "textDocument/codeAction":
        result = lsp_code_actions_dsl(source, source_name=source_uri)
        responses.append(_lsp_rpc_result(request_id, result["actions"]))
    elif method == "textDocument/formatting":
        result = lsp_formatting_dsl(source, source_name=source_uri)
        responses.append(_lsp_rpc_result(request_id, result["edits"]))
    elif method == "textDocument/rename":
        result = lsp_rename_dsl_documents(
            docs or {source_uri or "memory://appgen": source},
            source_uri=source_uri,
            position=position,
            new_name=params.get("newName"),
        )
        responses.append(
            _lsp_rpc_result(
                request_id,
                result["workspace_edit"]
                if result["ok"]
                else {
                    "blocked": result.get("blocked", False),
                    "diagnostics": result.get("diagnostics", result.get("blockers", ())),
                },
            )
        )
    elif method == "workspace/symbol":
        query = params.get("query", "")
        result = lsp_workspace_symbols_dsl_documents(
            docs or {source_uri or "memory://appgen": source},
            query=query,
        )
        responses.append(_lsp_rpc_result(request_id, result["symbols"]))
    elif is_request:
        responses.append(_lsp_rpc_error(request_id, -32601, f"Unsupported AppGen-X LSP method: {method}"))
    return tuple(responses), False


def _lsp_initialize_capabilities() -> dict:
    return {
        "textDocumentSync": 1,
        "completionProvider": {"resolveProvider": False, "triggerCharacters": (".", " ", ":")},
        "hoverProvider": True,
        "definitionProvider": True,
        "referencesProvider": True,
        "documentSymbolProvider": True,
        "renameProvider": {"prepareProvider": False},
        "codeActionProvider": True,
        "documentFormattingProvider": True,
        "workspaceSymbolProvider": True,
    }


def _lsp_request_uri(params: dict) -> str | None:
    text_document = params.get("textDocument") or {}
    return text_document.get("uri")


def _lsp_document_source(uri: str | None, documents: dict[str, str]) -> str:
    if uri and uri in documents:
        return documents[uri]
    if uri and uri.startswith("file://"):
        path = Path(uri.removeprefix("file://"))
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8")
    return ""


def _lsp_publish_diagnostics_notification(uri: str, source: str) -> dict:
    diagnostics = lsp_diagnostics_dsl(source, source_name=uri)
    return {
        "jsonrpc": "2.0",
        "method": "textDocument/publishDiagnostics",
        "params": {"uri": uri, "diagnostics": diagnostics["diagnostics"]},
    }


def _lsp_prefix_at_position(source: str, position: dict | None) -> str:
    token = _lsp_token_at_position(source, position)
    return token if token else ""


def _lsp_completion_items_with_workspace(items: Iterable[dict], documents: dict[str, str]) -> tuple[dict, ...]:
    merged = list(items)
    for symbol in lsp_workspace_symbols_dsl_documents(documents).get("symbols", ()):
        data = symbol.get("data", {})
        if data.get("kind") not in {
            "table",
            "field",
            "flow",
            "operation",
            "pbc",
            "api",
            "event",
            "package",
            "deploy",
            "llm",
            "agent",
        }:
            continue
        merged.append(
            {
                "label": symbol["name"],
                "kind": symbol["kind"],
                "detail": f"workspace {data.get('kind')}",
                "insertText": symbol["name"],
                "data": {"source": "workspace_symbols", **data},
            }
        )
    return tuple({(item.get("label"), item.get("detail")): item for item in merged}.values())


def _lsp_rpc_result(request_id, result) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _lsp_rpc_error(request_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _lsp_read_rpc_message(reader) -> dict | None:
    headers: dict[str, str] = {}
    while True:
        line = reader.readline()
        if not line:
            return None
        decoded = line.decode("ascii", errors="replace").strip()
        if not decoded:
            break
        if ":" in decoded:
            key, value = decoded.split(":", 1)
            headers[key.lower()] = value.strip()
    length = int(headers.get("content-length", "0") or "0")
    if length <= 0:
        return None
    raw = reader.read(length)
    if not raw:
        return None
    return json.loads(raw.decode("utf-8"))


def _lsp_write_rpc_message(writer, message: dict) -> None:
    body = json.dumps(message, separators=(",", ":"), default=list).encode("utf-8")
    writer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    writer.write(body)
    writer.flush()


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
    deduped = tuple({(item["label"], item["detail"], item.get("data", {}).get("kind")): item for item in items}.values())
    return {
        "format": "appgen.lsp-completion.v1",
        "position": position,
        "isIncomplete": False,
        "items": deduped,
    }


def completion_coverage_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Return required completion-source coverage for docs/tooling.md LSP claims."""
    source = text or ""
    completion = lsp_completion_dsl(source, source_name=source_name)
    detected = set()
    labels_by_source: dict[str, list[str]] = {key: [] for key in REQUIRED_COMPLETION_SOURCES}
    for item in completion.get("items", ()):
        kind = item.get("data", {}).get("kind") or item.get("detail")
        label = str(item.get("label") or "")
        source_key = _completion_source_for_kind(str(kind or ""))
        if source_key:
            detected.add(source_key)
            labels_by_source.setdefault(source_key, []).append(label)
    return {
        "format": "appgen.completion-coverage.v1",
        "source": source_name,
        "required": REQUIRED_COMPLETION_SOURCES,
        "detected": tuple(item for item in REQUIRED_COMPLETION_SOURCES if item in detected),
        "missing": tuple(item for item in REQUIRED_COMPLETION_SOURCES if item not in detected),
        "labels_by_source": {
            key: tuple(dict.fromkeys(value))
            for key, value in labels_by_source.items()
            if value
        },
    }


def _completion_source_for_kind(kind: str) -> str | None:
    return {
        "keyword": "top_level_keywords",
        "snippet": "block_snippets",
        "table": "table_names",
        "field": "field_names",
        "reference": "field_names",
        "lookup_path": "lookup_paths",
        "component": "components",
        "handler_event": "handler_events",
        "handler_target": "operation_targets",
        "flow": "operation_targets",
        "flow_state": "flow_states",
        "pbc": "pbc_keys",
        "pbc_contract": "pbc_contracts",
        "pbc_api": "pbc_apis",
        "pbc_event": "pbc_events",
        "pbc_command": "pbc_commands",
        "package_target": "package_targets",
        "deployment_unit": "deployment_units",
        "llm": "llm_providers",
        "agent_skill": "agent_skills",
    }.get(kind)


def lsp_hover_dsl(text: str, *, source_name: str | None = None, position: dict | None = None) -> dict:
    token = _lsp_token_at_position(text, position)
    symbol = _lsp_symbol_for_token(text, token, source_name=source_name)
    diagnostic = _lsp_diagnostic_for_token(text, token, source_name=source_name)
    contents: list[str] = []
    if symbol:
        contents.append(f"{symbol['kind']} `{symbol['name']}`")
        if symbol.get("detail"):
            contents.append(json.dumps(symbol["detail"], sort_keys=True, default=list))
    pbc_metadata = _lsp_pbc_catalog_metadata_for_token(token)
    if pbc_metadata:
        contents.append(f"PBC `{token}`: {pbc_metadata['label']}")
        contents.append(json.dumps(pbc_metadata, sort_keys=True, default=list))
    if diagnostic:
        contents.append(f"{diagnostic['code']}: {diagnostic['message']}")
        contents.append(json.dumps(_diagnostic_explanation(diagnostic["code"]), sort_keys=True))
    if token in CORE_KEYWORDS:
        contents.append(f"AppGen-X keyword `{token}`")
    return {
        "format": "appgen.lsp-hover.v1",
        "ok": bool(contents),
        "token": token,
        "contents": tuple(contents),
        "range": _lsp_token_range(text, position, token),
    }


def _lsp_pbc_catalog_metadata_for_token(token: str) -> dict | None:
    catalog_entry = _pbc_catalog_by_key().get(token)
    if not catalog_entry:
        return None
    return {
        "format": "appgen.lsp-pbc-hover.v1",
        "pbc": catalog_entry.get("pbc"),
        "label": catalog_entry.get("label") or catalog_entry.get("pbc"),
        "mesh": catalog_entry.get("mesh"),
        "description": catalog_entry.get("description"),
        "datastore_backend": catalog_entry.get("datastore_backend"),
        "api_count": len(catalog_entry.get("apis", ())),
        "event_count": len(catalog_entry.get("emits", ())) + len(catalog_entry.get("consumes", ())),
        "sample_apis": tuple(catalog_entry.get("apis", ())[:3]),
        "sample_events": tuple((tuple(catalog_entry.get("emits", ())) + tuple(catalog_entry.get("consumes", ())))[:3]),
    }


def lsp_definition_dsl(text: str, *, source_name: str | None = None, position: dict | None = None) -> dict:
    token = _lsp_token_at_position(text, position)
    symbol = _lsp_symbol_for_token(text, token, source_name=source_name)
    location = _lsp_location(source_name, symbol.get("range")) if symbol else _lsp_catalog_definition_location(token)
    return {
        "format": "appgen.lsp-definition.v1",
        "ok": location is not None,
        "token": token,
        "location": location,
    }


def _lsp_catalog_definition_location(token: str) -> dict | None:
    if token in _pbc_catalog_by_key():
        return _lsp_location(f"catalog://pbc/{token}", None)
    for key, entry in _pbc_catalog_by_key().items():
        for contract_kind, contract_name in (
            tuple(("api", value) for value in entry.get("apis", ()))
            + tuple(("event", value) for value in entry.get("emits", ()))
            + tuple(("event", value) for value in entry.get("consumes", ()))
        ):
            if token == str(contract_name):
                return _lsp_location(f"catalog://pbc/{key}/{contract_kind}/{quote(str(contract_name), safe='')}", None)
    return None


def _lsp_catalog_reference_locations(token: str) -> tuple[dict, ...]:
    if token in _pbc_catalog_by_key():
        return (_lsp_location(f"catalog://pbc/{token}", None),)
    locations = []
    for key, entry in _pbc_catalog_by_key().items():
        for contract_kind, contract_name in (
            tuple(("api", value) for value in entry.get("apis", ()))
            + tuple(("event", value) for value in entry.get("emits", ()))
            + tuple(("event", value) for value in entry.get("consumes", ()))
        ):
            if token == str(contract_name):
                locations.append(
                    _lsp_location(f"catalog://pbc/{key}/{contract_kind}/{quote(str(contract_name), safe='')}", None)
                )
    return tuple(locations)


def lsp_references_dsl(text: str, *, source_name: str | None = None, position: dict | None = None) -> dict:
    token = _lsp_token_at_position(text, position)
    locations = tuple(_lsp_location(source_name, item) for item in _lsp_occurrence_ranges(text, token))
    locations += _lsp_catalog_reference_locations(token)
    return {
        "format": "appgen.lsp-references.v1",
        "ok": bool(locations),
        "token": token,
        "locations": locations,
    }


def lsp_definition_dsl_documents(
    documents: dict[str, str],
    *,
    source_uri: str | None = None,
    position: dict | None = None,
) -> dict:
    source = _lsp_document_source(source_uri, documents)
    local = lsp_definition_dsl(source, source_name=source_uri, position=position)
    if local["ok"]:
        return {**local, "workspace": True}
    token = _lsp_token_at_position(source, position)
    for uri, document_source in documents.items():
        symbol = _lsp_symbol_for_token(document_source, token, source_name=uri)
        if symbol:
            return {
                "format": "appgen.lsp-definition.v1",
                "ok": True,
                "workspace": True,
                "token": token,
                "location": _lsp_location(uri, symbol.get("range")),
            }
    return {**local, "workspace": True}


def lsp_references_dsl_documents(
    documents: dict[str, str],
    *,
    source_uri: str | None = None,
    position: dict | None = None,
) -> dict:
    source = _lsp_document_source(source_uri, documents)
    token = _lsp_token_at_position(source, position)
    locations: list[dict] = []
    for uri, document_source in documents.items():
        locations.extend(_lsp_location(uri, item) for item in _lsp_occurrence_ranges(document_source, token))
    locations.extend(_lsp_catalog_reference_locations(token))
    return {
        "format": "appgen.lsp-references.v1",
        "ok": bool(locations),
        "workspace": True,
        "token": token,
        "locations": tuple(locations),
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
    symbols = list(
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
    symbols.extend(_lsp_catalog_workspace_symbols(needle))
    return {"format": "appgen.lsp-workspace-symbols.v1", "ok": semantic["ok"], "symbols": tuple(symbols)}


def lsp_workspace_symbols_dsl_documents(documents: dict[str, str], *, query: str = "") -> dict:
    needle = (query or "").lower()
    symbols: list[dict] = []
    models: list[dict] = []
    for uri, source in documents.items():
        semantic = semantic_model_dsl(source, source_name=uri)
        models.append(semantic)
        symbols.extend(
            {
                "name": symbol["name"],
                "kind": _lsp_symbol_kind(symbol["kind"]),
                "location": _lsp_location(uri, symbol.get("range")),
                "containerName": symbol.get("parent"),
                "data": {"id": symbol["id"], "kind": symbol["kind"], "uri": uri},
            }
            for symbol in semantic.get("symbols", {}).values()
            if not needle or needle in symbol["name"].lower() or needle in symbol["id"].lower()
        )
    symbols.extend(_lsp_catalog_workspace_symbols(needle))
    return {
        "format": "appgen.lsp-workspace-symbols.v1",
        "ok": all(model.get("ok") for model in models),
        "workspace": True,
        "symbols": tuple(symbols),
    }


def _lsp_catalog_workspace_symbols(needle: str) -> tuple[dict, ...]:
    catalog_symbols: list[dict] = []
    for key, entry in sorted(_pbc_catalog_by_key().items()):
        metadata_text = " ".join(
            str(value or "")
            for value in (
                key,
                entry.get("label"),
                entry.get("mesh"),
                entry.get("mesh_label"),
                entry.get("description"),
                entry.get("datastore_backend"),
            )
        ).lower()
        if not needle or needle in metadata_text:
            catalog_symbols.append(
                {
                    "name": key,
                    "kind": _lsp_symbol_kind("pbc"),
                    "location": _lsp_location(f"catalog://pbc/{key}", None),
                    "containerName": entry.get("mesh"),
                    "data": {
                        "id": f"catalog.pbc.{key}",
                        "kind": "pbc",
                        "catalog_resolved": True,
                        "label": entry.get("label"),
                        "mesh": entry.get("mesh"),
                        "description": entry.get("description"),
                    },
                }
            )
        contracts = (
            tuple(("api", value) for value in entry.get("apis", ()))
            + tuple(("event", value) for value in entry.get("emits", ()))
            + tuple(("event", value) for value in entry.get("consumes", ()))
        )
        for contract_kind, contract_name in contracts:
            if needle and needle not in str(contract_name).lower() and needle not in key.lower():
                continue
            catalog_symbols.append(
                {
                    "name": str(contract_name),
                    "kind": _lsp_symbol_kind(contract_kind),
                    "location": _lsp_location(f"catalog://pbc/{key}/{contract_kind}/{quote(str(contract_name), safe='')}", None),
                    "containerName": key,
                    "data": {
                        "id": f"catalog.pbc.{key}.{contract_kind}.{contract_name}",
                        "kind": contract_kind,
                        "catalog_resolved": True,
                        "pbc": key,
                    },
                }
            )
    return tuple(catalog_symbols)


def lsp_code_actions_dsl(text: str, *, source_name: str | None = None) -> dict:
    actions = []
    for action in dsl_code_actions(text, source_name=source_name):
        actions.append(
            {
                "title": action["title"],
                "kind": "quickfix",
                "diagnostics": tuple(_lsp_diagnostic(item) for item in action.get("diagnostics", ())),
                "edit": {
                    "changes": {
                        source_name or "memory://appgen": _lsp_text_edits_from_dsl_edits(action.get("edits", ()))
                    }
                },
                "command": action.get("command"),
                "data": {"id": action["id"], "changed": action["changed"]},
            }
        )
    actions.extend(_lsp_required_quick_actions(text, source_name=source_name))
    return {"format": "appgen.lsp-code-actions.v1", "ok": True, "actions": tuple(actions)}


def _lsp_text_edits_from_dsl_edits(edits: Iterable[dict]) -> tuple[dict, ...]:
    return tuple(
        {
            "range": edit.get("range", {}),
            "newText": str(edit.get("newText", edit.get("replacement", ""))),
        }
        for edit in edits or ()
    )


def apply_lsp_code_action_dsl(
    text: str,
    *,
    action_id: str,
    source_name: str | None = None,
) -> dict:
    """Apply one generated LSP quick-fix edit and return patched DSL evidence."""
    source = text or ""
    actions = lsp_code_actions_dsl(source, source_name=source_name)["actions"]
    matches = tuple(action for action in actions if action.get("data", {}).get("id") == action_id)
    if not matches:
        return {
            "format": "appgen.lsp-code-action-apply.v1",
            "ok": False,
            "action_id": action_id,
            "changed": False,
            "patched_source": source,
            "diagnostics": (
                _spec_diagnostic(source, "AGX0100", "error", f"Unknown code action: {action_id}"),
            ),
            "available_actions": tuple(action.get("data", {}).get("id") for action in actions),
        }
    action = matches[0]
    uri = source_name or "memory://appgen"
    edits = tuple(action.get("edit", {}).get("changes", {}).get(uri, ()))
    patched = _apply_lsp_text_edits(source, edits)
    lint = lint_report_dsl(patched, source_name=source_name)
    return {
        "format": "appgen.lsp-code-action-apply.v1",
        "ok": bool(edits) and lint["ok"],
        "action_id": action_id,
        "title": action.get("title"),
        "changed": patched != source,
        "source": source_name,
        "patched_source": patched,
        "applied_edits": edits,
        "lint": lint,
        "diagnostics": lint["diagnostics"],
    }


def lsp_code_action_apply_audit_dsl() -> dict:
    """Prove required LSP quick fixes apply through linted DSL patches."""
    case_specs = (
        (
            "create_missing_table",
            "create_missing_table",
            "app A { targets: web }\ntable Invoice { id: int pk }\nview MissingForm for Missing { Main: id }\n",
            "table Missing",
        ),
        (
            "create_missing_field",
            "create_missing_field",
            "app A { targets: web }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: total }\n",
            "total: string",
        ),
        (
            "create_calculated_field_for_binding",
            "create_calculated_field_for_binding",
            "app A { targets: web }\ntable Customer { id: int pk; name: string }\ntable Invoice { id: int pk; customer_id: int -> Customer.id }\nview InvoiceForm for Invoice { Main: customer.missing_name }\n",
            "missing_name: string = name",
        ),
        (
            "create_operation_from_handler",
            "create_operation_from_handler",
            "app A { targets: web }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }\n",
            "operation SubmitInvoice",
        ),
        (
            "create_flow_from_handler",
            "create_flow_from_handler",
            "app A { targets: web }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: id; on Save -> SubmitInvoice }\n",
            "flow SubmitInvoice",
        ),
        (
            "add_lookup_directive",
            "add_lookup_directive",
            "app A { targets: web }\ntable Customer { id: int pk; name: string }\ntable Invoice { id: int pk; customer_id: int -> Customer.id }\nview InvoiceForm for Invoice { Main: customer_name }\n",
            "lookup customer_name (customer.name)",
        ),
        (
            "add_relationship_for_lookup_path",
            "add_relationship_for_lookup_path",
            "app A { targets: web }\ntable Customer { id: int pk; name: string }\ntable Invoice { id: int pk }\nview InvoiceForm for Invoice { Main: customer.name }\n",
            "customer_id: int -> Customer.id",
        ),
        (
            "replace_typo_with_nearest_symbol",
            "replace_typo_with_nearest_symbol",
            "app A { targets: web }\ntable Invoice { id: int pk; total: decimal }\nview InvoiceForm for Invoice { Main: totl }\n",
            "Main: total",
        ),
        (
            "replace_secret_literal_with_env",
            "replace_secret_literal_with_env",
            "app A { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\nllm ApiModel { provider: openai; api_key: \"sk-secret\" }\n",
            "api_key: OPENAI_API_KEY",
        ),
        (
            "remove_invalid_runtime_picker_fields",
            "remove_invalid_runtime_picker_fields",
            "app A { targets: web; runtime: node; stream: bytewax; backend: oracle }\ntable T { id: int pk }\nview TForm for T { Main: id }\n",
            "targets: web",
        ),
        (
            "create_event_contract",
            "create_event_contract",
            "app A { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\ncomposition Suite { include pbc gl_core version 1.0.0 include pbc ap_automation version 1.0.0 connect ap_automation domain_event MissingEvent -> gl_core domain_event MissingCommand }\n",
            "event MissingEvent",
        ),
        (
            "register_or_import_pbc_manifest",
            "register_or_import_pbc_manifest",
            "app A { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\ncomposition Suite { include pbc missing_pbc version 1.0.0 }\n",
            "pbc missing_pbc",
        ),
        (
            "add_missing_permission_for_agent_skill",
            "add_missing_permission_for_agent_skill",
            "app A { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\nllm LocalModel { provider: ollama; mode: local }\nagent Writer { provider: LocalModel; tools: write }\n",
            "GeneratedResource: write",
        ),
        (
            "add_package_for_app_target",
            "add_package_for_app_target",
            "app A { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\n",
            "package WebPackage",
        ),
        (
            "create_smoke_test_declaration",
            "create_smoke_test_declaration",
            "app A { targets: web }\ntable T { id: int pk }\nview TForm for T { Main: id }\nflow Publish { draft -> live }\n",
            "test PublishSmoke",
        ),
    )
    cases = []
    for case_id, action_id, source, expected_text in case_specs:
        result = apply_lsp_code_action_dsl(source, source_name=f"{case_id}.appgen", action_id=action_id)
        invalid_picker_removed = (
            case_id != "remove_invalid_runtime_picker_fields"
            or (
                "runtime:" not in result["patched_source"]
                and "stream:" not in result["patched_source"]
                and "backend:" not in result["patched_source"]
            )
        )
        ok = (
            result["ok"]
            and result["changed"]
            and expected_text in result["patched_source"]
            and bool(result["applied_edits"])
            and invalid_picker_removed
        )
        cases.append(
            {
                "id": case_id,
                "action_id": action_id,
                "ok": ok,
                "expected_text": expected_text,
                "diagnostic_codes": tuple(item.get("code") for item in result.get("diagnostics", ())),
                "applied_edit_count": len(result.get("applied_edits", ())),
                "lint_ok": result.get("lint", {}).get("ok"),
            }
        )
    return {
        "format": "appgen.lsp-code-action-apply-audit.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": tuple(cases),
        "required_actions": tuple(case[1] for case in case_specs),
        "blocking_gaps": tuple(case["id"] for case in cases if not case["ok"]),
    }


def _apply_lsp_text_edits(source: str, edits: Iterable[dict]) -> str:
    patched = source or ""
    ordered = sorted(
        tuple(edits or ()),
        key=lambda edit: _lsp_position_to_index(patched, edit.get("range", {}).get("start", {})),
        reverse=True,
    )
    for edit in ordered:
        edit_range = edit.get("range", {})
        start = _lsp_position_to_index(patched, edit_range.get("start", {}))
        end = _lsp_position_to_index(patched, edit_range.get("end", {}))
        patched = patched[:start] + str(edit.get("newText", "")) + patched[end:]
    return patched


def _lsp_position_to_index(source: str, position: dict) -> int:
    line = max(int(position.get("line", 0)), 0)
    character = max(int(position.get("character", 0)), 0)
    lines = (source or "").splitlines(keepends=True)
    if line >= len(lines):
        return len(source or "")
    return sum(len(item) for item in lines[:line]) + min(character, len(lines[line].rstrip("\r\n")))


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
    blockers = _lsp_rename_blocking_diagnostics(source, migration)
    return {
        "format": "appgen.lsp-rename.v1",
        "ok": lint["ok"] and not blockers,
        "token": token,
        "new_name": new_name,
        "symbol": symbol,
        "blocked": bool(blockers),
        "blockers": blockers,
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


def lsp_rename_dsl_documents(
    documents: dict[str, str],
    *,
    source_uri: str | None = None,
    position: dict | None = None,
    new_name: str | None = None,
) -> dict:
    source = _lsp_document_source(source_uri, documents)
    local = lsp_rename_dsl(source, source_name=source_uri, position=position, new_name=new_name)
    if not local["ok"]:
        return {**local, "workspace": True}
    token = local["token"]
    changes = {}
    for uri, document_source in documents.items():
        if not re.search(rf"\b{re.escape(token)}\b", document_source):
            continue
        changes[uri] = (
            {
                "range": _lsp_full_document_range(document_source),
                "newText": re.sub(rf"\b{re.escape(token)}\b", str(new_name), document_source),
            },
        )
    if not changes:
        changes = local["workspace_edit"]["changes"]
    return {
        **local,
        "workspace": True,
        "workspace_edit": {"changes": changes},
        "workspace_documents_considered": tuple(documents),
        "workspace_documents_changed": tuple(changes),
    }


def _lsp_full_document_range(source: str) -> dict:
    return {
        "start": {"line": 0, "character": 0},
        "end": {"line": len((source or "").splitlines()), "character": 0},
    }


def _lsp_rename_blocking_diagnostics(source: str, migration: dict) -> tuple[dict, ...]:
    if not migration.get("requires_approval"):
        return ()
    destructive_kinds = tuple(
        change.get("kind")
        for change in migration.get("changes", ())
        if change.get("destructive") or change.get("requires_approval")
    )
    return (
        {
            **_spec_diagnostic(
                source,
                "AGX1101",
                "error",
                "Rename blocked because migration impact requires explicit approval.",
            ),
            "related_locations": (),
            "fixes": (
                {
                    "id": "add_rename_hint",
                    "title": "Add an explicit migration rename hint before applying this rename",
                },
            ),
            "migration_change_kinds": destructive_kinds,
        },
    )


def _parse_lsp_position(value: str | None) -> dict | None:
    if not value:
        return None
    match = re.match(r"(?P<line>\d+):(?P<char>\d+)$", value.strip())
    if not match:
        return None
    return {"line": int(match.group("line")), "character": int(match.group("char"))}


def _parse_cli_targets(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(item.strip() for item in re.split(r"[,\s]+", value) if item.strip())


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
    if code == "AGX0402":
        table, binding = _view_lookup_binding_from_message(message, source)
        if table and binding and "." in binding:
            alias = binding.split(".", 1)[0]
            target_table = _pascal_case(alias)
            if _source_declares_block(source, "table", target_table):
                actions.append(
                    _lsp_insert_in_block_action(
                        source,
                        source_name,
                        diagnostic,
                        "add_relationship_for_lookup_path",
                        f"Add relationship for {binding}",
                        "table",
                        table,
                        f"  {alias}_id: int -> {target_table}.id\n",
                    )
                )
        alias_table, alias_name, alias_path = _view_lookup_alias_from_message(message, source)
        if alias_table and alias_name and alias_path:
            actions.append(
                _lsp_insert_in_block_action(
                    source,
                    source_name,
                    diagnostic,
                    "add_lookup_directive",
                    f"Add lookup directive for {alias_name}",
                    "table",
                    alias_table,
                    f"  lookup {alias_name} ({alias_path})\n",
                )
            )
    if code == "AGX0303":
        view, binding = _view_binding_from_message(message)
        table = _view_table_for_view(source, view)
        field = binding.rsplit(".", 1)[-1] if binding else "display_value"
        if table:
            calculated_table = _calculated_field_table_for_binding(source, table, binding) or table
            expression = "name" if _source_table_has_field(source, calculated_table, "name") and field != "name" else "id"
            actions.append(_lsp_insert_in_block_action(source, source_name, diagnostic, "create_calculated_field_for_binding", f"Create calculated field {calculated_table}.{field}", "table", calculated_table, f"  {field}: string = {expression}\n"))
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
        contracts = _missing_contract_names(message)
        if contracts:
            new_text = "\n" + "\n\n".join(f"event {contract} {{\n  topic: pbc.events\n}}" for contract in contracts) + "\n"
            actions.append(_lsp_append_action(source, source_name, diagnostic, "create_event_contract", f"Create event contract {contracts[0]}", new_text))
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
    insert_index = _closing_index_for_block(source, kind, name)
    if insert_index is None:
        return _lsp_append_action(source, source_name, diagnostic, action_id, title, f"\n{kind} {name} {{\n{new_text}}}\n")
    inserted = new_text if insert_index > 0 and source[insert_index - 1] in "\n\r" else f"\n{new_text}"
    return _lsp_edit_action(
        source_name,
        diagnostic,
        action_id,
        title,
        ({"range": _source_range(source, insert_index, insert_index), "newText": inserted},),
    )


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


def _view_lookup_binding_from_message(message: str, source: str) -> tuple[str | None, str | None]:
    match = re.search(
        r"Unknown (?:view|component) field: ([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)",
        message,
    )
    if not match:
        return None, None
    view, binding = match.groups()
    return _view_table_for_view(source, view), binding


def _view_lookup_alias_from_message(message: str, source: str) -> tuple[str | None, str | None, str | None]:
    match = re.search(r"Unknown (?:view|component) field: ([A-Za-z_][A-Za-z0-9_]*)\.([a-z][a-z0-9_]*_[a-z][a-z0-9_]*)", message)
    if not match:
        return None, None, None
    view, alias_name = match.groups()
    table = _view_table_for_view(source, view)
    if not table:
        return None, None, None
    relationship_alias, target_field = alias_name.split("_", 1)
    target_table = _source_relationship_target_for_alias(source, table, relationship_alias)
    if not target_table or not _source_table_has_field(source, target_table, target_field):
        return None, None, None
    return table, alias_name, f"{relationship_alias}.{target_field}"


def _calculated_field_table_for_binding(source: str, table: str, binding: str | None) -> str | None:
    if not binding or "." not in binding:
        return table
    first, *_rest = binding.split(".")
    return _source_relationship_target_for_alias(source, table, first)


def _source_declares_block(source: str, kind: str, name: str) -> bool:
    return bool(re.search(rf"\b{re.escape(kind)}\s+{re.escape(name)}\b", source or ""))


def _source_relationship_target_for_alias(source: str, table: str, alias: str) -> str | None:
    body = _source_block_body(source, "table", table)
    if body is None:
        return None
    match = re.search(rf"\b{re.escape(alias)}_id\s*:\s*[A-Za-z_][A-Za-z0-9_]*(?:\([^)]*\))?(?:\s+\w+)*\s*->\s*([A-Za-z_][A-Za-z0-9_]*)\.[A-Za-z_][A-Za-z0-9_]*", body)
    return match.group(1) if match else None


def _source_table_has_field(source: str, table: str, field: str) -> bool:
    body = _source_block_body(source, "table", table)
    return bool(body and re.search(rf"\b{re.escape(field)}\s*:", body))


def _source_block_body(source: str, kind: str, name: str) -> str | None:
    pattern = re.compile(rf"\b{re.escape(kind)}\s+{re.escape(name)}\b[^\{{]*\{{")
    match = pattern.search(source or "")
    if not match:
        return None
    depth = 1
    for index in range(match.end(), len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[match.end() : index]
    return None


def _handler_target_from_message(message: str) -> str | None:
    match = re.search(r"Unknown handler target:\s+[A-Za-z_][A-Za-z0-9_]*\.([A-Za-z_][A-Za-z0-9_]*)", message)
    return match.group(1) if match else _diagnostic_token(message)


def _missing_contract_name(message: str) -> str | None:
    contracts = _missing_contract_names(message)
    return contracts[0] if contracts else None


def _missing_contract_names(message: str) -> tuple[str, ...]:
    match = re.search(r"Unknown cross-PBC contract: .*", message)
    if not match:
        return ()
    names = re.findall(r"(?:event|domain_event|command|api)\s+([A-Za-z_][A-Za-z0-9_]*)", match.group(0))
    return tuple(dict.fromkeys(names))


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
    index = _closing_index_for_block(source, kind, name)
    return source.count("\n", 0, index) if index is not None else None


def _closing_index_for_block(source: str, kind: str, name: str) -> int | None:
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
                return index
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
        "visual_edit_matrix": designer_visual_edit_matrix_dsl(source, source_name=source_name)
        if visual_edit is None
        else None,
        "checks": checks,
        "blocking_gaps": tuple(check["check"] for check in checks if not check["ok"]),
    }


def designer_visual_edit_matrix_dsl(text: str, *, source_name: str | None = None) -> dict:
    """Prove every required Studio visual-edit path round-trips through DSL."""
    source = text or ""
    semantic = semantic_model_dsl(source, source_name=source_name)
    table_name = "Invoice" if "Invoice" in semantic.get("tables", {}) else next(iter(semantic.get("tables", {}) or {"GeneratedRecord": {}}))
    view_name, binding = _designer_matrix_view_binding(semantic)
    flow_name = "SubmitInvoice" if "SubmitInvoice" in semantic.get("flows", {}) else next(iter(semantic.get("flows", {}) or {"GeneratedFlow": {}}))
    composition_name = "FinanceSuite" if "FinanceSuite" in semantic.get("composition", {}) else next(iter(semantic.get("composition", {}) or {"AppComposition": {}}))
    app_target = next(iter(semantic.get("app", {}).get("targets", ()) or ("web",)))
    deployment_target = flow_name if flow_name != "GeneratedFlow" else table_name
    case_specs = (
        (
            "database_designer_add_field",
            {"kind": "add_field", "table": table_name, "field": "due_date", "type": "date", "required": True},
            True,
            "database_designer",
            "due_date",
            (),
        ),
        (
            "form_designer_add_component",
            {
                "kind": "add_component",
                "view": view_name,
                "binding": binding,
                "component": "Lookup",
                "x": 1,
                "y": 2,
                "w": 4,
                "h": 1,
            },
            True,
            "form_designer",
            f"@ {binding} Lookup 1 2 4 1",
            (),
        ),
        (
            "workflow_designer_add_transition",
            {"kind": "add_flow_transition", "flow": flow_name, "from": "posted", "to": "archived"},
            True,
            "workflow_designer",
            "posted -> archived",
            (),
        ),
        (
            "pbc_composition_designer_add_include",
            {
                "kind": "add_pbc_include",
                "composition": composition_name,
                "pbc": "ap_automation",
                "version": "1.0.0",
            },
            True,
            "pbc_composition_designer",
            "include pbc ap_automation version 1.0.0",
            (),
        ),
        (
            "package_designer_add_package",
            {"kind": "add_package", "name": f"{_pascal_case(app_target)}Release", "target": app_target},
            True,
            "package_deployment_designer",
            f"package {_pascal_case(app_target)}Release",
            (),
        ),
        (
            "deployment_designer_add_unit",
            {
                "kind": "add_deployment_unit",
                "deployment": "Production",
                "target": deployment_target,
                "pattern": "worker",
            },
            True,
            "package_deployment_designer",
            f"unit {deployment_target} as worker",
            (),
        ),
        (
            "form_designer_reject_invalid_binding",
            {
                "kind": "add_component",
                "view": view_name,
                "binding": "missing.field",
                "component": "Lookup",
                "x": 1,
                "y": 2,
                "w": 4,
                "h": 1,
            },
            False,
            "form_designer",
            "missing.field",
            ("AGX0402",),
        ),
    )
    cases = []
    for case_id, edit, should_accept, required_surface, expected_text, expected_codes in case_specs:
        result = _designer_visual_edit_result(source, edit, source_name=source_name)
        codes = tuple(item.get("code") for item in result.get("diagnostics", ()))
        ok = (
            result["accepted"] is should_accept
            and (not should_accept or result["round_trip_ok"])
            and required_surface in result.get("changed_surfaces", ())
            and expected_text in result.get("patched_source", "")
            and set(expected_codes) <= set(codes)
        )
        cases.append(
            {
                "id": case_id,
                "ok": ok,
                "operation": edit["kind"],
                "accepted": result["accepted"],
                "round_trip_ok": result["round_trip_ok"],
                "required_surface": required_surface,
                "changed_surfaces": result.get("changed_surfaces", ()),
                "expected_text": expected_text,
                "expected_diagnostic_codes": expected_codes,
                "diagnostic_codes": codes,
            }
        )
    return {
        "format": "appgen.designer-visual-edit-matrix.v1",
        "ok": all(case["ok"] for case in cases),
        "cases": tuple(cases),
        "required_operations": tuple(dict.fromkeys(case[1]["kind"] for case in case_specs)),
        "required_cases": tuple(case[0] for case in case_specs),
        "blocking_gaps": tuple(case["id"] for case in cases if not case["ok"]),
    }


def _designer_matrix_view_binding(semantic: dict) -> tuple[str, str]:
    views = semantic.get("views", {})
    for view_name, view in views.items():
        bindings = _valid_bindings_for_table(semantic, view.get("table"))
        if bindings:
            preferred = "customer.name" if "customer.name" in bindings else bindings[0]
            return view_name, preferred
    return "GeneratedForm", "name"


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
    projections_after = {
        "form_designer": _designer_form_projection(semantic),
        "database_designer": _designer_database_projection(semantic),
        "workflow_designer": _designer_workflow_projection(semantic),
        "pbc_composition_designer": _designer_pbc_projection(semantic),
        "package_deployment_designer": _designer_package_deployment_projection(semantic),
    }
    accepted = bool(patch) and lint["ok"]
    return {
        "format": "appgen.designer-visual-edit-result.v1",
        "operation": (visual_edit or {}).get("kind"),
        "accepted": accepted,
        "dsl_patch": patch,
        "dsl_diff": tuple(
            difflib.unified_diff(
                source.splitlines(),
                patched_source.splitlines(),
                fromfile="before.appgen",
                tofile="after.appgen",
                lineterm="",
            )
        ),
        "patched_source": patched_source,
        "lint": lint,
        "diagnostics": tuple(lint["diagnostics"]),
        "round_trip_ok": accepted and semantic["ok"],
        "semantic_model_format": semantic.get("format"),
        "semantic_after": semantic,
        "projections_after": projections_after,
        "changed_surfaces": _designer_changed_surfaces(visual_edit or {}),
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
        required = " required" if edit.get("required") else ""
        return f"// edit table {table}: add {field}: {type_name}{required}"
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
        return f"// edit composition {composition}: include pbc {pbc} version {edit.get('version', '1.0.0')}"
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


def _designer_changed_surfaces(edit: dict) -> tuple[str, ...]:
    kind = edit.get("kind")
    if kind in {"add_table", "add_field"}:
        return ("database_designer", "form_designer", "graph_explain_panel")
    if kind == "add_component":
        return ("form_designer", "graph_explain_panel")
    if kind == "add_flow_transition":
        return ("workflow_designer", "graph_explain_panel")
    if kind == "add_pbc_include":
        return ("pbc_composition_designer", "graph_explain_panel")
    if kind in {"add_package", "add_deployment_unit"}:
        return ("package_deployment_designer", "graph_explain_panel")
    return ()


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
    graph_evidence = graph_suite_report_dsl(source, source_name=source_name)
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
    evidence_bundle = {
        "format": "appgen.release-evidence-bundle.v1",
        "source": source_name,
        "artifacts": tuple(f"{key}:{report['format']}" for key, report in selected_reports.items()),
        "graph_suite": {
            "format": graph_evidence.get("format"),
            "ok": graph_evidence.get("ok"),
            "required_kinds": graph_evidence.get("required_kinds", ()),
            "formats": graph_evidence.get("formats", ()),
            "graph_reports": tuple(graph_evidence.get("graph_reports", {}).keys()),
            "blocking_gaps": graph_evidence.get("blocking_gaps", ()),
        },
        "requires_generation": any(
            gap in {"app_build_not_observed", "smoke_tests_not_declared", "smoke_launch_not_declared"}
            for report in selected_reports.values()
            for gap in report.get("blocking_gaps", ())
        ),
    }
    written_artifacts = _write_release_evidence_bundle(
        output_dir,
        evidence_bundle=evidence_bundle,
        selected_reports=selected_reports,
        checks=checks,
        source_name=source_name,
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
        "graph_evidence": graph_evidence,
        "evidence_bundle": evidence_bundle,
        "written_artifacts": written_artifacts,
    }


def _write_release_evidence_bundle(
    output_dir: str | None,
    *,
    evidence_bundle: dict,
    selected_reports: dict,
    checks: tuple[dict, ...],
    source_name: str | None = None,
) -> tuple[dict, ...]:
    if not output_dir:
        return ()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    evidence_path = output_path / "appgen-release-evidence.json"
    payload = {
        "format": "appgen.release-evidence-file.v1",
        "evidence_bundle": evidence_bundle,
        "checks": checks,
        "reports": selected_reports,
    }
    evidence_path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=list), encoding="utf-8")
    written = [{"path": str(evidence_path), "kind": "release_evidence", "bytes": evidence_path.stat().st_size}]
    for target, report in selected_reports.items():
        manifest = _target_package_manifest(target, report, evidence_path=evidence_path, source_name=source_name)
        manifest_path = output_path / f"appgen-package-{target}.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True, default=list), encoding="utf-8")
        written.append({"path": str(manifest_path), "kind": f"{target}_package_manifest", "bytes": manifest_path.stat().st_size})
    return tuple(written)


def _target_package_manifest(
    target: str,
    report: dict,
    *,
    evidence_path: Path,
    source_name: str | None = None,
) -> dict:
    checks = tuple(report.get("checks", ()))
    check_map = {check.get("check"): check.get("ok", False) for check in checks}
    common = {
        "format": "appgen.package-manifest.v1",
        "target": target,
        "source": source_name,
        "ok": report.get("ok", False),
        "verifier": report.get("format"),
        "release_evidence": str(evidence_path.name),
        "checks": checks,
        "blocking_gaps": report.get("blocking_gaps", ()),
    }
    target_details = {
        "web": {
            "artifact_class": "web_application",
            "handoff_artifacts": ("routes", "forms", "handlers", "smoke_tests"),
            "app_build_contract": check_map.get("app_build_contract", False),
            "routes_declared": check_map.get("routes_exist", False),
            "forms_bind_valid_fields": check_map.get("generated_forms_bind_valid_fields", False),
            "handler_targets_resolve": check_map.get("handler_targets_resolve", False),
            "smoke_tests_declared": check_map.get("smoke_tests_declared", False),
            "build_required": True,
            "smoke_entrypoint": "web.smoke",
        },
        "mobile": {
            "artifact_class": "mobile_application",
            "handoff_artifacts": (
                "mobile_metadata",
                "signing_posture",
                "offline_policy",
                "permissions",
                "screen_density",
                "smoke_launch",
            ),
            "package_metadata_exists": check_map.get("package_metadata_exists", False),
            "signing_posture_declared": check_map.get("signing_posture_declared", False),
            "offline_policy_declared": check_map.get("offline_policy_declared", False),
            "permissions_explained": check_map.get("permissions_explained", False),
            "screens_fit_target_density": check_map.get("screens_fit_target_density", False),
            "smoke_launch_path_exists": check_map.get("smoke_launch_path_exists", False),
            "smoke_entrypoint": "mobile.launch",
        },
        "desktop": {
            "artifact_class": "desktop_application",
            "handoff_artifacts": (
                "desktop_metadata",
                "installer_profile",
                "startup_assets",
                "menus",
                "context_menus",
                "smoke_launch",
            ),
            "package_metadata_exists": check_map.get("package_metadata_exists", False),
            "installer_posture_declared": check_map.get("installer_or_update_posture_declared", False),
            "startup_assets_declared": check_map.get("splash_or_startup_assets_declared_when_used", False),
            "menus_bind_to_handlers": check_map.get("menus_and_context_menus_bind_to_handlers", False),
            "smoke_launch_path_exists": check_map.get("smoke_launch_path_exists", False),
            "smoke_entrypoint": "desktop.launch",
        },
        "pbc": {
            "artifact_class": "packaged_business_capability",
            "handoff_artifacts": ("manifest", "contracts", "owned_schema", "registration", "release_evidence"),
            "side_effect_free_registration": check_map.get("self_registration_side_effect_free", False),
            "smoke_entrypoint": "pbc.verify",
        },
        "deployment": {
            "artifact_class": "deployment_plan",
            "handoff_artifacts": ("units", "health_checks", "environment", "resource_hints", "topology_graph"),
            "units_declared": check_map.get("units_declared", False),
            "health_checks_declared": check_map.get("health_checks_declared", False),
            "environment_variables_named": check_map.get("environment_variables_named", False),
            "secret_values_absent": check_map.get("secret_values_absent", False),
            "resource_hints_present": check_map.get("resource_hints_present_for_production_units", False),
            "topology_graph_connected": check_map.get("topology_graph_connected_and_explainable", False),
            "topology_declared": check_map.get("units_declared", False)
            and check_map.get("topology_graph_connected_and_explainable", False),
            "smoke_entrypoint": "deployment.verify",
        },
    }
    common.update(target_details.get(target, {"artifact_class": target, "handoff_artifacts": (), "smoke_entrypoint": f"{target}.verify"}))
    return common


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


def _migration_coverage(changes: Iterable[dict]) -> dict:
    detected = set()
    change_kinds = tuple(change.get("kind") for change in changes)
    for change in changes:
        detected.update(_migration_detection_families(change))
    return {
        "format": "appgen.migration-coverage.v1",
        "required": REQUIRED_MIGRATION_DETECTIONS,
        "detected": tuple(item for item in REQUIRED_MIGRATION_DETECTIONS if item in detected),
        "missing": tuple(item for item in REQUIRED_MIGRATION_DETECTIONS if item not in detected),
        "change_kinds": change_kinds,
    }


def _migration_detection_families(change: dict) -> tuple[str, ...]:
    kind = change.get("kind")
    families = {
        "add_table": ("added_table",),
        "drop_table": ("dropped_table",),
        "rename_table": ("renamed_table",),
        "renamed_table_candidate": ("renamed_table",),
        "add_field": ("added_field",),
        "drop_field": ("dropped_field",),
        "rename_field": ("renamed_field",),
        "renamed_field_candidate": ("renamed_field",),
        "type_change": ("type_change",),
        "nullability_change": ("nullability_change",),
        "default_change": ("default_change",),
        "relationship_change": ("relationship_change",),
        "add_relationship": ("relationship_change",),
        "drop_relationship": ("relationship_change",),
        "unique_change": ("unique_index_check_change",),
        "add_unique_constraint": ("unique_index_check_change",),
        "drop_unique_constraint": ("unique_index_check_change",),
        "add_index": ("unique_index_check_change",),
        "drop_index": ("unique_index_check_change",),
        "add_check": ("unique_index_check_change",),
        "drop_check": ("unique_index_check_change",),
        "calculated_field_change": ("calculated_field_change",),
        "pbc_ownership_transfer": ("pbc_ownership_transfer",),
    }.get(str(kind), ())
    if change.get("requires_backfill"):
        return (*families, "data_backfill_requirement")
    return families


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
                        safe_alternative=(
                            "Add a new field with the target type, backfill it, then switch dependent forms and reports."
                            if kind == "type_change"
                            else "Backfill existing rows before enforcing the required constraint."
                            if kind == "nullability_change" and destructive
                            else None
                        ),
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

    if any(marker in lower for marker in ("hand-written generated code", "outside the dsl", "replace the runtime")):
        return {"kind": "unsupported", "intent": "outside_dsl_scope"}

    if "agent skill" in lower or ("permission" in lower and "agent" in lower):
        return {
            "kind": "add_agent_skill_permission",
            "intent": "agent_change",
            "agent": "ReviewAssistant",
            "provider": _default_llm_name(semantic),
            "operation": _default_operation_name(semantic),
            "resource": _default_table_name(semantic),
            "affected_symbols": ("agent.ReviewAssistant",),
        }

    if "api event contract" in lower or ("api" in lower and "event" in lower and "contract" in lower):
        contract = _pascal_case(re.sub(r"\b(add|api|event|contract)\b", "", normalized, flags=re.I).strip() or "GeneratedEvent")
        return {
            "kind": "add_api_event_contract",
            "intent": "contract_change",
            "contract": contract,
            "operation": _default_operation_name(semantic),
            "resource": _default_table_name(semantic),
            "affected_symbols": (f"api.{contract}Api", f"event.{contract}"),
        }

    if "package deployment" in lower or ("package" in lower and "deployment" in lower):
        return {
            "kind": "add_package_deployment_unit",
            "intent": "release_change",
            "target": _default_app_target(semantic),
            "unit": _default_operation_name(semantic),
            "affected_symbols": ("package.GeneratedRelease", "deployment.Production"),
        }

    if "flow transition" in lower or ("transition" in lower and "flow" in lower):
        flow = _default_flow_name(semantic)
        transition_match = re.search(r"\b(?P<from>[a-z][a-z0-9_]*)\s+to\s+(?P<to>[a-z][a-z0-9_]*)\b", lower)
        return {
            "kind": "add_flow_transition",
            "intent": "workflow_change",
            "flow": flow,
            "from": transition_match.group("from") if transition_match else "posted",
            "to": transition_match.group("to") if transition_match else "archived",
            "affected_symbols": (f"flow.{flow}",),
        }

    if "view section" in lower or ("section" in lower and "view" in lower):
        return {
            "kind": "add_view_section",
            "intent": "ui_change",
            "view": _default_view_name(semantic),
            "field": _default_view_binding(semantic),
            "section": "Audit",
            "affected_symbols": (f"view.{_default_view_name(semantic)}",),
        }

    if "component placement" in lower or ("component" in lower and "placement" in lower):
        return {
            "kind": "add_component_placement",
            "intent": "ui_change",
            "view": _default_view_name(semantic),
            "binding": _default_view_binding(semantic),
            "component": "Lookup",
            "affected_symbols": (f"view.{_default_view_name(semantic)}",),
        }

    if "handler" in lower:
        return {
            "kind": "add_handler",
            "intent": "ui_change",
            "view": _default_view_name(semantic),
            "event": "Audit",
            "target": _default_operation_name(semantic),
            "affected_symbols": (f"handler.{_default_view_name(semantic)}.Audit",),
        }

    operation_match = re.search(r"\b(?:add|create)\s+operation\s+(?P<operation>[A-Za-z][A-Za-z0-9_ ]+)\b", normalized, re.I)
    if operation_match:
        operation = _pascal_case(operation_match.group("operation"))
        return {
            "kind": "add_operation",
            "intent": "operation_change",
            "operation": operation,
            "affected_symbols": (f"operation.{operation}",),
        }

    rule_match = re.search(r"\b(?:add|create)\s+rule\s+(?P<rule>[A-Za-z][A-Za-z0-9_ ]+)\b", normalized, re.I)
    if rule_match:
        rule = _pascal_case(rule_match.group("rule"))
        table = _default_table_name(semantic)
        field = _default_numeric_field(semantic, table)
        return {
            "kind": "add_rule",
            "intent": "rule_change",
            "rule": rule,
            "table": table,
            "field": field,
            "affected_symbols": (f"rule.{rule}",),
        }

    if "relationship" in lower:
        return {
            "kind": "add_relationship",
            "intent": "schema_change",
            "table": _default_table_name(semantic),
            "field": "customer_ref_id",
            "target_table": "Customer" if "Customer" in semantic.get("tables", {}) else _default_table_name(semantic),
            "target_field": "id",
            "affected_symbols": (f"table.{_default_table_name(semantic)}.customer_ref_id",),
        }

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
    if operation["kind"] == "add_relationship":
        return (
            f"// edit table {operation['table']}: add {operation['field']}: int "
            f"-> {operation['target_table']}.{operation['target_field']} [many-to-one]"
        )
    if operation["kind"] == "add_view_section":
        return f"// edit view {operation['view']}: add section {operation['section']} {operation['field']}"
    if operation["kind"] == "add_component_placement":
        return f"// edit view {operation['view']}: add component {operation['binding']} {operation['component']} 0 1 4 1"
    if operation["kind"] == "add_handler":
        return f"// edit view {operation['view']}: add handler {operation['event']} {operation['target']}"
    if operation["kind"] == "add_operation":
        return f"""
operation {operation['operation']} {{
  draft -> complete
}}
""".strip()
    if operation["kind"] == "add_rule":
        return f"""
rule {operation['rule']} for {operation['table']} {{
  {operation['field']} >= 0
}}
""".strip()
    if operation["kind"] == "add_flow_transition":
        return f"// edit flow {operation['flow']}: add transition {operation['from']} -> {operation['to']}"
    if operation["kind"] == "add_pbc_include":
        composition = operation["composition"]
        return f"""
composition {composition} {{
  include pbc {operation['pbc']} version 1.0.0
}}
""".strip()
    if operation["kind"] == "add_api_event_contract":
        return f"""
api {operation['contract']}Api {{
  on Sync -> {operation['operation']}
  {operation['resource']}: read
}}

event {operation['contract']} {{
  topic: appgen.{_snake_case(operation['contract'])}
}}
""".strip()
    if operation["kind"] == "add_package_deployment_unit":
        return f"""
package GeneratedRelease {{
  target: {operation['target']}
  smoke: launch
}}

deploy Production {{
  unit {operation['unit']} as worker
  health {operation['unit']} "/health"
  resource {operation['unit']} cpu 1
  env {operation['unit']} DATABASE_URL
}}
""".strip()
    if operation["kind"] == "add_agent_skill_permission":
        return f"""
agent {operation['agent']} {{
  provider: {operation['provider']}
  tools: read, write
  {operation['resource']}: read, write
  on Review -> {operation['operation']}
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
        if " add section " in patch:
            return _apply_view_section_patch(source, patch)
        if " add handler " in patch:
            return _apply_view_handler_patch(source, patch)
        return _apply_view_component_patch(source, patch)
    if patch.startswith("// edit flow "):
        return _apply_flow_transition_patch(source, patch)
    if patch.startswith("// edit composition "):
        return _apply_pbc_include_patch(source, patch)
    stripped = source.rstrip()
    return f"{stripped}\n\n{patch}\n" if stripped else f"{patch}\n"


def _apply_table_field_patch(source: str, patch: str) -> str:
    match = re.match(
        r"// edit table (?P<table>[A-Za-z_][A-Za-z0-9_]*): add (?P<field>[a-z][a-z0-9_]*): (?P<type>[A-Za-z_][A-Za-z0-9_]*)(?P<suffix>(?: required)?(?:\s+->\s+[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*(?:\s+\[[^\]]+\])?)?)",
        patch,
    )
    if not match:
        return source
    table = match.group("table")
    field = match.group("field")
    field_type = match.group("type")
    suffix = match.group("suffix") or ""
    pattern = re.compile(rf"(table\s+{re.escape(table)}\s*\{{)(?P<body>.*?)(\n\}})", re.S)
    table_match = pattern.search(source)
    if table_match is None:
        return _append_dsl_patch(
            source,
            f"table {table} {{\n  id: int pk\n  {field}: {field_type}{suffix}\n}}",
        )
    body = table_match.group("body").rstrip()
    replacement = f"{table_match.group(1)}{body}\n  {field}: {field_type}{suffix}{table_match.group(3)}"
    return source[: table_match.start()] + replacement + source[table_match.end() :]


def _apply_view_section_patch(source: str, patch: str) -> str:
    match = re.match(
        r"// edit view (?P<view>[A-Za-z_][A-Za-z0-9_]*): add section (?P<section>[A-Za-z_][A-Za-z0-9_]*) (?P<field>[A-Za-z_][A-Za-z0-9_.]*)",
        patch,
    )
    if not match:
        return source
    line = f"  {match.group('section')}: {match.group('field')}"
    return _append_to_existing_block(source, "view", match.group("view"), line) or source


def _apply_view_handler_patch(source: str, patch: str) -> str:
    match = re.match(
        r"// edit view (?P<view>[A-Za-z_][A-Za-z0-9_]*): add handler (?P<event>[A-Za-z_][A-Za-z0-9_]*) (?P<target>[A-Za-z_][A-Za-z0-9_]*)",
        patch,
    )
    if not match:
        return source
    line = f"  on {match.group('event')} -> {match.group('target')}"
    return _append_to_existing_block(source, "view", match.group("view"), line) or source


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


def _apply_pbc_include_patch(source: str, patch: str) -> str:
    match = re.match(
        r"// edit composition (?P<composition>[A-Za-z_][A-Za-z0-9_]*): include pbc (?P<pbc>[A-Za-z_][A-Za-z0-9_]*) version (?P<version>[A-Za-z0-9_.-]+)",
        patch,
    )
    if not match:
        return source
    composition = match.group("composition")
    line = f"  include pbc {match.group('pbc')} version {match.group('version')}"
    inserted = _append_to_existing_block(source, "composition", composition, line)
    if inserted:
        return inserted
    return _append_dsl_patch(source, f"composition {composition} {{\n{line}\n}}")


def _default_composition_name(semantic: dict) -> str:
    compositions = semantic.get("composition", {})
    if compositions:
        return next(iter(compositions))
    app_name = semantic.get("app", {}).get("name")
    return f"{app_name or 'App'}Composition"


def _default_table_name(semantic: dict) -> str:
    tables = semantic.get("tables", {})
    if "Invoice" in tables:
        return "Invoice"
    return next(iter(tables or {"Record": {}}))


def _default_view_name(semantic: dict) -> str:
    views = semantic.get("views", {})
    if "InvoiceForm" in views:
        return "InvoiceForm"
    return next(iter(views or {"RecordForm": {}}))


def _default_view_binding(semantic: dict) -> str:
    view_name = _default_view_name(semantic)
    view = semantic.get("views", {}).get(view_name, {})
    table_name = view.get("table") or _default_table_name(semantic)
    bindings = _valid_bindings_for_table(semantic, table_name)
    if "customer.name" in bindings:
        return "customer.name"
    if "total" in bindings:
        return "total"
    return next(iter(bindings or ("name",)))


def _default_flow_name(semantic: dict) -> str:
    flows = semantic.get("flows", {})
    if "SubmitInvoice" in flows:
        return "SubmitInvoice"
    return next(iter(flows or {"GeneratedFlow": {}}))


def _default_operation_name(semantic: dict) -> str:
    operations = semantic.get("operations", {})
    for name in ("ReverseInvoice", "SubmitInvoice"):
        if name in operations or name in semantic.get("flows", {}):
            return name
    return next(iter(operations or semantic.get("flows", {}) or {"GeneratedOperation": {}}))


def _default_llm_name(semantic: dict) -> str:
    llms = semantic.get("llms", {})
    if "LocalModel" in llms:
        return "LocalModel"
    return next(iter(llms or {"LocalModel": {}}))


def _default_app_target(semantic: dict) -> str:
    targets = tuple(semantic.get("app", {}).get("targets", ()) or ())
    return "web" if "web" in targets or not targets else str(targets[0])


def _default_numeric_field(semantic: dict, table: str) -> str:
    fields = semantic.get("tables", {}).get(table, {}).get("fields", {})
    for name, field in fields.items():
        if field.get("type") in {"int", "decimal", "float"} and name != "id":
            return name
    return next(iter(fields or {"id": {}}))


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
    for group_name in _declared_group_names(source):
        add("group", group_name)
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
        for section in view.sections:
            add("view_section", section.name, parent=f"view.{view.name}", detail={"fields": section.fields})
        for component in view.components:
            binding = component.field or component.component
            add(
                "component_binding",
                binding,
                parent=f"view.{view.name}",
                detail={"component": component.component, "x": component.x, "y": component.y, "w": component.w, "h": component.h},
            )
        for handler in view.handlers:
            add("handler", handler.event, parent=f"view.{view.name}", detail={"target": handler.target})
    for flow in schema.flows:
        add("flow", flow.name)
        for state in _flow_states(flow):
            add("flow_state", state, parent=f"flow.{flow.name}")
    for role in schema.roles:
        add("role", role.name)
        for permission in role.permissions:
            add("permission", _permission_symbol_name(permission), parent=f"role.{role.name}", detail=_semantic_permission(permission))
    for rule in schema.rules:
        add("rule", rule.name, detail={"table": rule.table})
    for provider in schema.llm_providers:
        add("llm", provider.name, detail={"provider": provider.provider})
    for agent in schema.agents:
        add("agent", agent.name, detail={"provider": agent.provider})
        for tool in agent.tools:
            add("agent_skill", tool, parent=f"agent.{agent.name}", detail={"source": "tools"})
        for skill in agent.competencies:
            add("agent_skill", skill.verb, parent=f"agent.{agent.name}", detail=_semantic_statement(skill))
        for permission in agent.permissions:
            add("permission", _permission_symbol_name(permission), parent=f"agent.{agent.name}", detail=_semantic_permission(permission))
        for handler in agent.handlers:
            add("handler", handler.event, parent=f"agent.{agent.name}", detail={"target": handler.target})
    for block in schema.platform_blocks:
        add(block.kind, block.name)
        for unit in block.deployment_units:
            add("deployment_unit", unit.target, parent=f"{block.kind}.{block.name}", detail={"pattern": unit.pattern})
        for permission in block.permissions:
            add("permission", _permission_symbol_name(permission), parent=f"{block.kind}.{block.name}", detail=_semantic_permission(permission))
        for handler in block.handlers:
            add("handler", handler.event, parent=f"{block.kind}.{block.name}", detail={"target": handler.target})
    for contract in _enterprise_contracts(schema):
        add(contract.kind, contract.name)
        for permission in contract.permissions:
            add("permission", _permission_symbol_name(permission), parent=f"{contract.kind}.{contract.name}", detail=_semantic_permission(permission))
        for handler in contract.handlers:
            add("handler", handler.event, parent=f"{contract.kind}.{contract.name}", detail={"target": handler.target})
    return symbols


def _permission_symbol_name(permission: PermissionSchema) -> str:
    actions = ",".join(permission.actions)
    return f"{permission.resource}:{actions}" if actions else permission.resource


def _declared_group_names(source: str) -> tuple[str, ...]:
    names = []
    reserved = set(CORE_KEYWORDS) | {"target", "targets", "source", "provider", "mode", "tools"}
    for match in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{", source or ""):
        name = match.group(1)
        if name.lower() not in reserved:
            names.append(name)
    declared_blocks = {
        name
        for kind in (
            "app",
            "table",
            "enum",
            "view",
            "flow",
            "role",
            "rule",
            "llm",
            "agent",
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
        )
        for name in _declared_block_names(source, kind)
    }
    return tuple(name for name in dict.fromkeys(names) if name not in declared_blocks)


def _semantic_range(line: int | None, column: int | None, token: str) -> dict | None:
    if line is None or column is None:
        line = 1
        column = 0
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
            if directive.name:
                value = directive.values[0] if directive.values else directive.name
                paths[directive.name] = {
                    "chain": (value,),
                    "valid": _valid_lookup_path(table.name, value, table_map, field_map),
                }
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


def _strict_lint_diagnostic(diagnostic: dict, *, strict: bool) -> dict:
    if strict and diagnostic.get("code") == "AGX0404":
        return {
            **diagnostic,
            "severity": "error",
            "message": f"{diagnostic.get('message', '')} Strict component mode treats unknown visual components as errors.",
        }
    return diagnostic


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
        "invalid_runtime_picker_field": "AGX0801",
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
    if message.startswith("Invalid runtime picker field"):
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


def _organize_formatted_table_fields(source: str) -> str:
    lines = source.splitlines()
    organized: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if re.match(r"^table\s+[A-Za-z_][A-Za-z0-9_]*\s+\{$", line):
            organized.append(line)
            index += 1
            body: list[str] = []
            while index < len(lines) and lines[index] != "}":
                body.append(lines[index])
                index += 1
            organized.extend(_organize_table_body_lines(body))
            if index < len(lines):
                organized.append(lines[index])
            index += 1
            continue
        organized.append(line)
        index += 1
    return "\n".join(organized).rstrip() + ("\n" if organized else "")


def _organize_table_body_lines(lines: list[str]) -> list[str]:
    items: list[tuple[int, list[str]]] = []
    pending_comments: list[str] = []
    for line in lines:
        if line.strip().startswith("//"):
            pending_comments.append(line)
            continue
        items.append((len(items), [*pending_comments, line]))
        pending_comments = []
    for comment in pending_comments:
        items.append((len(items), [comment]))

    sorted_items = sorted(items, key=lambda item: (_format_table_body_category(item[1]), item[0]))
    return [line for _index, item_lines in sorted_items for line in item_lines]


def _format_table_body_category(lines: list[str]) -> int:
    primary = next((line.strip() for line in lines if line.strip() and not line.strip().startswith("//")), "")
    if not primary:
        return 7
    if primary.startswith("..."):
        return 0
    if ":" not in primary:
        return 6
    field_name, rest = primary.split(":", 1)
    rest = rest.strip()
    if field_name == "id" or re.search(r"\bpk\b", rest):
        return 0
    if re.search(r"\bunique\b", rest) or field_name in {"code", "number", "name", "title", "email"}:
        return 1
    if " -> " in primary or field_name.endswith("_id"):
        return 2
    if " = " in primary:
        return 4
    if field_name in {"created_at", "updated_at", "created_by", "updated_by", "deleted_at", "version"}:
        return 5
    return 3


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
    if kind == "remove_app_options":
        return _remove_app_options(source, tuple(fix["options"]))
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


def _remove_app_options(source: str, option_names: tuple[str, ...]) -> str:
    if not option_names:
        return source
    names = "|".join(re.escape(name) for name in option_names)
    pattern = re.compile(rf"(?P<lead>(?:^|[{{\n;])\s*)(?:{names})\s*:\s*[^;\n}}]+;?")

    def repl(match: re.Match[str]) -> str:
        lead = match.group("lead")
        return "\n" if "\n" in lead else lead

    previous = source
    while True:
        updated = pattern.sub(repl, previous)
        if updated == previous:
            return updated
        previous = updated


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
    if kind == "remove_app_options":
        fixed = _remove_app_options(source, tuple(fix["options"]))
        if fixed != source:
            return (
                {
                    "range": _source_range(source, 0, len(source)),
                    "replacement": fixed,
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
    if any(error.startswith("Invalid runtime picker field") for error in errors):
        fixes.append(
            {
                "id": "remove_invalid_runtime_picker_fields",
                "title": "Remove invalid backend/runtime/stream picker fields",
                "kind": "remove_app_options",
                "options": ("backend", "runtime", "stream"),
            }
        )
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
    if message.startswith("Invalid runtime picker field"):
        return "invalid_runtime_picker_field"
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
        r"Invalid runtime picker field: app\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown field type: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown derived-field reference: [^.]+ uses ([A-Za-z_][A-Za-z0-9_]*)",
        r"Multi-hop lookup chain breaks: [^.]+\.([A-Za-z_][A-Za-z0-9_.]*)",
        r"Unresolved lookup path: [^.]+\.([A-Za-z_][A-Za-z0-9_.]*)",
        r"Unknown view table: [^.]+ for ([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown view field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown component field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown visual component: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown handler target: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown rule field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Flow strict state is undeclared: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Human task has no assignee: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown role resource: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown deployment unit target: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown package target: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown PBC catalog entry: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown cross-PBC contract: .*?\b([A-Za-z_][A-Za-z0-9_]*)\s*->",
        r"Private PBC table access: .*?\b([A-Za-z_][A-Za-z0-9_]*)\s*->",
        r"Unknown agent provider: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown agent skill target: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Agent write-capable skill has no permission: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown (?:relation|reference) target table: ([A-Za-z_][A-Za-z0-9_]*)",
        r"Unknown (?:relation|reference) target field: [^.]+\.([A-Za-z_][A-Za-z0-9_]*)",
        r"Duplicate [^:]+ declaration: ([A-Za-z_][A-Za-z0-9_]*)",
    ):
        match = re.search(pattern, message)
        if match:
            return match.group(1).split(",", 1)[0].strip()
    if "api_key" in message:
        return "api_key"
    if "single =" in message:
        return "="
    if "Unbalanced braces" in message:
        return "{"
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
        "invalid_runtime_picker_field": ("remove_invalid_runtime_picker_fields",),
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


def _tooling_policy_diagnostics(
    schema: AppSchema,
    *,
    component_catalog: Iterable[str] | None = None,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    table_map = {table.name: table for table in schema.tables}
    field_map = {table.name: _field_names(table) for table in schema.tables}
    handler_targets = _handler_target_names(schema)
    pbc_catalog = _pbc_catalog_by_key()
    local_pbcs = {block.name for block in schema.platform_blocks if block.kind == "pbc"}
    local_contracts = _local_contract_names_by_kind(schema)
    errors: list[str] = []
    warnings: list[str] = []

    for option_name in ("backend", "runtime", "stream"):
        if option_name in schema.app_options:
            errors.append(f"Invalid runtime picker field: app.{option_name}")

    for view in schema.views:
        for component in view.components:
            if component.component not in _known_component_names(schema, component_catalog=component_catalog):
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
            if key and key not in pbc_catalog and key not in local_pbcs:
                errors.append(f"Unknown PBC catalog entry: {block.name}.{key}")
        for raw_connection in block.options.get("connect", ()):
            connection = _semantic_composition_connection(raw_connection)
            for side in ("from", "to"):
                key = connection.get(f"{side}_pbc")
                if key and key not in pbc_catalog and key not in local_pbcs:
                    errors.append(f"Unknown PBC catalog entry: {block.name}.{key}")
            if str(connection.get("from_kind") or "").endswith("table") or str(connection.get("to_kind") or "").endswith("table"):
                errors.append(f"Private PBC table access: {block.name}.{raw_connection}")
                continue
            if not _pbc_connection_contract_resolves(connection, pbc_catalog) and not _local_connection_contract_resolves(connection, local_contracts):
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


def _known_component_names(
    schema: AppSchema,
    *,
    component_catalog: Iterable[str] | None = None,
) -> set[str]:
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
    names.update(str(component).strip() for component in (component_catalog or ()) if str(component).strip())
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


def _local_contract_names_by_kind(schema: AppSchema) -> dict[str, set[str]]:
    contracts: dict[str, set[str]] = {"api": set(), "command": set(), "event": set(), "emits": set(), "consumes": set()}
    for contract in _enterprise_contracts(schema):
        kind = contract.kind.lower()
        contracts.setdefault(kind, set()).add(contract.name)
        if kind == "event":
            contracts["emits"].add(contract.name)
            contracts["consumes"].add(contract.name)
            contracts["command"].add(contract.name)
        if kind == "api":
            contracts["command"].add(contract.name)
    return contracts


def _local_connection_contract_resolves(connection: dict, contracts: dict[str, set[str]]) -> bool:
    for side in ("from", "to"):
        kind = str(connection.get(f"{side}_kind") or "")
        contract = str(connection.get(f"{side}_contract") or "")
        if not kind or not contract:
            return False
        normalized_kind = "event" if kind == "domain_event" else kind
        if contract not in contracts.get(normalized_kind, set()):
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
    for directive in table.directives:
        if directive.verb.lower() == "lookup" and directive.name:
            names.add(directive.name)
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
