"""Package-level DSL quality release evidence."""

from __future__ import annotations

import importlib.util
import py_compile
import tempfile
from collections.abc import Iterable
from pathlib import Path

from .dsl import dsl_antlr_integrity_report
from .dsl import dsl_authoring_release_gate
from .dsl import format_dsl
from .dsl import lint_dsl


DEFAULT_DSL_ARTIFACTS = (
    "app/dsl_reference.py",
    "app/templates/appgen_dsl_reference.html",
)
DSL_DOC_REQUIREMENTS = (
    {
        "path": "docs/dsl.md",
        "required_phrases": (
            "AppGen DSL",
            "dsl_authoring_release_gate",
            "dsl_antlr_integrity_report",
        ),
    },
    {
        "path": "docs/dsl-grammar.md",
        "required_phrases": (
            "AppGen DSL Grammar",
            "Complete Grammar",
            "Lexical Rules",
        ),
    },
    {
        "path": "docs/dsl-user-guide.md",
        "required_phrases": (
            "AppGen DSL User Guide",
            "Linting Workflow",
            "CI Workflow",
        ),
    },
    {
        "path": "docs/dsl-tutorial.md",
        "required_phrases": (
            "AppGen DSL Tutorial",
            "Lint And Generate",
            "Review The Generated Studio",
        ),
    },
    {
        "path": "docs/dsl-linter.md",
        "required_phrases": (
            "AppGen DSL Linter",
            "dsl_authoring_release_gate",
            "quick fixes",
        ),
    },
    {
        "path": "docs/index.md",
        "required_phrases": (
            "dsl-grammar",
            "dsl-user-guide",
            "dsl-tutorial",
            "dsl-linter",
        ),
    },
)


def package_dsl_sample() -> str:
    """Return a canonical sample that exercises schema, UI, targets, and agents."""
    source = """
    app QualityDemo { targets: web, mobile, desktop }
    table Author { id: int pk; name: string required search; }
    table Book {
      id: int pk;
      title: string required search;
      author_id: int -> Author.id [many-to-one];
    }
    view BookForm for Book {
      Main: title, author_id;
      @ title TextBox 0 0 8 1;
      @ author_id Lookup 0 1 8 1;
    }
    llm LocalModel { provider: ollama; mode: local; model: llama3; }
    agent CatalogAgent { provider: LocalModel; goal: "Help librarians manage books"; }
    """
    return format_dsl(source)["formatted"]


def dsl_documentation_catalog(root: Path | str | None = None) -> tuple[dict, ...]:
    """Return DSL documentation coverage evidence."""
    base = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    rows = []
    for item in DSL_DOC_REQUIREMENTS:
        path = base / item["path"]
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        missing = tuple(
            phrase for phrase in item["required_phrases"] if phrase not in text
        )
        rows.append(
            {
                "path": item["path"],
                "exists": path.exists(),
                "required_phrases": item["required_phrases"],
                "missing": missing,
                "ok": path.exists() and not missing,
            }
        )
    return tuple(rows)


def dsl_linter_release_contract(sample: str | None = None) -> dict:
    """Return package-level evidence that DSL linting is release-grade."""
    source = sample or package_dsl_sample()
    valid = lint_dsl(source, source_name="package-sample")
    invalid = lint_dsl(
        "app Broken { targets: toaster } table Book { title: string }",
        source_name="invalid-sample",
    )
    legacy = lint_dsl(
        "app Legacy { targets: web } table Author { id: int pk } "
        "table Book { id: int pk; author_id: int ref Author.id }",
        source_name="legacy-sample",
    )
    return {
        "format": "appgen.package-dsl-linter-contract.v1",
        "valid_sample": valid,
        "invalid_sample": invalid,
        "legacy_sample": legacy,
        "ok": valid["ok"]
        and invalid["ok"] is False
        and legacy["ok"]
        and bool(legacy["fixes"]),
    }


def dsl_artifact_contract(existing_paths: Iterable[str] | None = None) -> dict:
    """Return generated DSL reference artifact evidence."""
    existing = set(existing_paths or DEFAULT_DSL_ARTIFACTS)
    missing = tuple(path for path in DEFAULT_DSL_ARTIFACTS if path not in existing)
    return {
        "format": "appgen.package-dsl-artifact-contract.v1",
        "required_artifacts": DEFAULT_DSL_ARTIFACTS,
        "missing": missing,
        "ok": not missing,
    }


def generated_dsl_reference_smoke_audit(sample: str | None = None) -> dict:
    """Generate an app and exercise its generated DSL reference tooling."""
    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    source = sample or package_dsl_sample()
    with tempfile.TemporaryDirectory(prefix="appgen-dsl-reference-") as raw_workdir:
        project_dir = Path(raw_workdir) / "dsl-reference"
        generate_app_from_schema(
            schema_from_dsl(source, source_name="dsl-reference-smoke.appgen"),
            project_dir / "app",
        )
        paths = {
            "app/dsl_reference.py": project_dir / "app" / "dsl_reference.py",
            "app/templates/appgen_dsl_reference.html": project_dir
            / "app"
            / "templates"
            / "appgen_dsl_reference.html",
        }
        missing = tuple(relative for relative, path in paths.items() if not path.exists())
        compile_result = _compile_generated_dsl_reference(paths["app/dsl_reference.py"])
        generated = _load_generated_module(
            paths["app/dsl_reference.py"],
            "appgen_generated_dsl_reference",
        )
        quality = generated.dsl_language_quality_contract()
        authoring_gate = generated.dsl_authoring_release_gate()
        alias_fix = generated.apply_dsl_fixes(
            "entity Book { title: string searchable; secret: string hide } "
            "form BookForm for Book { Main: title }"
        )
        legacy_fix = generated.apply_dsl_fixes(
            "app Bad { targets: web, toaster } table Author { id: int pk } "
            "table Book { id: int pk; author_id: int ref Author.id }"
        )
        formatted = generated.format_dsl(
            "app Library{targets:web,desktop} table Book{id:int pk; title:string required}"
        )
    checks = (
        {
            "check": "generated_artifacts",
            "ok": not missing,
            "missing": missing,
        },
        {
            "check": "compiled_reference",
            "ok": compile_result["ok"],
            "path": "app/dsl_reference.py",
        },
        {
            "check": "generated_language_quality",
            "ok": quality["ok"]
            and quality["canonical_keyword_count"] <= quality["budget"]["limit"]
            and quality["antlr_integrity"]["ok"],
        },
        {
            "check": "generated_authoring_gate",
            "ok": authoring_gate["ok"]
            and {"language_ergonomics", "language_experience"}
            <= {gate["gate"] for gate in authoring_gate["gates"]},
        },
        {
            "check": "generated_quick_fixes",
            "ok": {"normalize_authoring_aliases", "normalize_modifier_aliases"}
            <= set(alias_fix["applied"])
            and {"replace_ref_with_arrow", "normalize_targets"} <= set(legacy_fix["applied"])
            and "toaster" not in legacy_fix["fixed"],
        },
        {
            "check": "generated_formatter",
            "ok": formatted["after"]["ok"]
            and "app Library {\n  targets: web, desktop\n}" in formatted["formatted"],
        },
    )
    return {
        "format": "appgen.generated-dsl-reference-smoke-audit.v1",
        "scope": "package",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "compile": compile_result,
        "language_quality": {
            "format": quality["format"],
            "ok": quality["ok"],
            "canonical_keyword_count": quality["canonical_keyword_count"],
        },
        "authoring_gate": {
            "format": authoring_gate["format"],
            "ok": authoring_gate["ok"],
        },
    }


def _compile_generated_dsl_reference(path: Path) -> dict:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True}


def _load_generated_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load generated module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dsl_release_audit(
    existing_paths: Iterable[str] | None = None,
    *,
    root: Path | str | None = None,
) -> dict:
    """Return package-level proof for DSL linter, grammar, docs, and UX."""
    sample = package_dsl_sample()
    authoring_gate = dsl_authoring_release_gate(
        sample,
        source_name="package-sample",
    )
    antlr = dsl_antlr_integrity_report()
    linter = dsl_linter_release_contract(sample)
    docs = dsl_documentation_catalog(root)
    artifacts = dsl_artifact_contract(existing_paths)
    generated_reference = generated_dsl_reference_smoke_audit(sample)
    cli_commands = (
        "appgen --lint-dsl app.appgen",
        "appgen --fix-dsl app.appgen",
        "appgen --format-dsl app.appgen",
        "appgen --dsl-authoring-gate app.appgen",
        "appgen --dsl-antlr-report",
        "appgen --dsl-release-audit",
    )

    gates = (
        {
            "id": "authoring_release_gate",
            "ok": authoring_gate["ok"],
            "format": authoring_gate["format"],
        },
        {
            "id": "antlr_grammar_sync",
            "ok": antlr["ok"],
            "grammar": antlr["grammar"],
            "parser": antlr["parser"],
        },
        {
            "id": "linter_diagnostics_and_fixes",
            "ok": linter["ok"],
            "diagnostic_counts": linter["valid_sample"]["severity_counts"],
        },
        {
            "id": "documentation_coverage",
            "ok": all(row["ok"] for row in docs),
            "documents": docs,
        },
        {
            "id": "cli_contract",
            "ok": all(command.startswith("appgen --") for command in cli_commands),
            "commands": cli_commands,
        },
        {
            "id": "artifact_contract",
            "ok": artifacts["ok"],
            "required_artifacts": artifacts["required_artifacts"],
            "missing": artifacts["missing"],
        },
        {
            "id": "generated_reference_smoke",
            "ok": generated_reference["ok"],
            "checks": generated_reference["checks"],
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-dsl-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "sample": sample,
        "authoring_gate": authoring_gate,
        "antlr_integrity": antlr,
        "linter": linter,
        "documentation": docs,
        "artifact_contract": artifacts,
        "generated_reference_smoke": generated_reference,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-dsl-readiness-unless-ok-is-true",
    }
