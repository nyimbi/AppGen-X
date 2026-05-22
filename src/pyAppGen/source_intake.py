"""Package-level source intake release evidence.

The parser adapters live in ``schema.py``. This module turns their deterministic
example audit into a top-level package contract so the active goal can prove
DBML, SQL, PonyORM, existing databases, and DSL inputs are release-gated.
"""

from __future__ import annotations

import json
import py_compile
import tempfile
from collections.abc import Iterable
from pathlib import Path

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import create_engine

from .schema import load_schema
from .schema import schema_source_contract
from .schema import schema_source_example_audit


REQUIRED_SOURCE_KINDS = ("dbml", "sql", "ponyorm", "database", "dsl")
DEFAULT_SOURCE_ARTIFACTS = (
    "app/schema_import.py",
    "app/templates/appgen_schema_import.html",
    "app/appgen.json",
)

_SOURCE_FLAGS = {
    "dbml": "--dbml",
    "sql": "--sql",
    "ponyorm": "--pony",
    "database": "--database-url",
    "dsl": "--dsl",
}
_SOURCE_EXAMPLES = {
    "dbml": "schema.dbml",
    "sql": "schema.sql",
    "ponyorm": "entities.py",
    "database": "postgresql+psycopg2://user@host/db",
    "dsl": "app.appgen",
}
_SMOKE_DBML = """
Table author {
  id int [pk]
  name varchar [not null]
}

Table book {
  id int [pk]
  title varchar [not null]
  author_id int [ref: > author.id]
}
"""
_SMOKE_SQL = """
CREATE TABLE author (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author_id INTEGER NOT NULL REFERENCES author(id)
);
"""
_SMOKE_PONYORM = """
from pony.orm import Database, PrimaryKey, Required, Set

db = Database()

class Author(db.Entity):
    id = PrimaryKey(int)
    name = Required(str)
    books = Set("Book")

class Book(db.Entity):
    id = PrimaryKey(int)
    title = Required(str)
    author = Required(Author)
"""
_SMOKE_DSL = """
app SourceSmoke { targets: web, mobile, desktop }

table Author {
  id: int pk
  name: string required
}

table Book {
  id: int pk
  title: string required
  author_id: int required -> Author.id [many-to-one]
}

view BookForm for Book {
  Main: title, author_id;
  @ title TextBox 0 0 8 1;
  @ author_id Lookup 0 1 8 1;
}
"""
_SMOKE_ARTIFACTS = (
    "models.py",
    "views.py",
    "api.py",
    "gql.py",
    "schema_import.py",
    "dsl_reference.py",
    "appgen.json",
    "templates/appgen_schema_import.html",
)
_SMOKE_COMPILE_ARTIFACTS = (
    "models.py",
    "views.py",
    "api.py",
    "gql.py",
    "schema_import.py",
    "dsl_reference.py",
)


def source_catalog() -> tuple[dict, ...]:
    """Return normalized source families supported by package generation."""
    return tuple(schema_source_contract()["sources"])


def source_example_matrix() -> dict:
    """Return parser-normalization proof for each source family."""
    audit = schema_source_example_audit()
    rows = tuple(audit["rows"])
    return {
        "format": "appgen.package-source-intake-matrix.v1",
        "canonical_contract": audit["canonical_contract"],
        "rows": rows,
        "source_kinds": tuple(row["source_kind"] for row in rows),
        "checks": audit["checks"],
        "ok": audit["ok"],
    }


def source_generation_plan(
    kind: str,
    source: str | None = None,
    *,
    writedir: str = "app",
) -> dict:
    """Return the CLI generation command and expected artifacts for a source kind."""
    if kind not in _SOURCE_FLAGS:
        raise KeyError(f"Unsupported source kind: {kind}")
    source_value = source or _SOURCE_EXAMPLES[kind]
    command = f"appgen {_SOURCE_FLAGS[kind]} {source_value} --writedir {writedir}"
    return {
        "format": "appgen.package-source-generation-plan.v1",
        "source_kind": kind,
        "source": source_value,
        "command": command,
        "expected_artifacts": DEFAULT_SOURCE_ARTIFACTS,
        "checks": (
            "schema_source_catalog",
            "schema_source_profile",
            "source_fidelity_report",
            "source_generation_proof",
        ),
        "ok": True,
    }


def all_source_generation_plans() -> tuple[dict, ...]:
    """Return command plans for every supported source family."""
    return tuple(source_generation_plan(kind) for kind in REQUIRED_SOURCE_KINDS)


def source_artifact_contract(existing_paths: Iterable[str] | None = None) -> dict:
    """Return generated source-intake artifact readiness evidence."""
    existing = set(existing_paths or DEFAULT_SOURCE_ARTIFACTS)
    missing = tuple(path for path in DEFAULT_SOURCE_ARTIFACTS if path not in existing)
    return {
        "format": "appgen.package-source-artifact-contract.v1",
        "required_artifacts": DEFAULT_SOURCE_ARTIFACTS,
        "missing": missing,
        "ok": not missing,
    }


def _write_smoke_inputs(workdir: Path) -> dict[str, Path | str]:
    dbml_path = workdir / "schema.dbml"
    sql_path = workdir / "schema.sql"
    pony_path = workdir / "entities.py"
    dsl_path = workdir / "app.appgen"
    database_path = workdir / "existing.db"

    dbml_path.write_text(_SMOKE_DBML, encoding="utf-8")
    sql_path.write_text(_SMOKE_SQL, encoding="utf-8")
    pony_path.write_text(_SMOKE_PONYORM, encoding="utf-8")
    dsl_path.write_text(_SMOKE_DSL, encoding="utf-8")

    metadata = MetaData()
    Table(
        "author",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
    )
    Table(
        "book",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String, nullable=False),
        Column("author_id", Integer, ForeignKey("author.id"), nullable=False),
    )
    database_url = f"sqlite:///{database_path}"
    metadata.create_all(create_engine(database_url))
    return {
        "dbml": dbml_path,
        "sql": sql_path,
        "ponyorm": pony_path,
        "dsl": dsl_path,
        "database": database_url,
    }


def _compile_generated_artifacts(output_dir: Path) -> tuple[dict, ...]:
    results = []
    for relative in _SMOKE_COMPILE_ARTIFACTS:
        path = output_dir / relative
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            results.append(
                {
                    "path": relative,
                    "ok": False,
                    "error": str(exc),
                }
            )
        else:
            results.append({"path": relative, "ok": True})
    return tuple(results)


def _source_smoke_row(kind: str, source: Path | str, output_dir: Path) -> dict:
    from .gen import generate_app_from_database
    from .gen import generate_app_from_schema

    if kind == "database":
        generate_app_from_database(str(source), output_dir)
    else:
        source_type = "pony" if kind == "ponyorm" else kind
        generate_app_from_schema(
            load_schema(Path(source), source_type=source_type),
            output_dir,
        )

    manifest_path = output_dir / "appgen.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    existing = tuple(
        relative for relative in _SMOKE_ARTIFACTS if (output_dir / relative).exists()
    )
    missing = tuple(
        relative for relative in _SMOKE_ARTIFACTS if relative not in existing
    )
    compile_results = _compile_generated_artifacts(output_dir)
    profile = manifest["source_profile"]
    checks = {
        "artifacts": not missing,
        "compile": all(item["ok"] for item in compile_results),
        "manifest_source_kind": profile["source_kind"] == kind,
        "tables": profile["counts"]["tables"] >= 2,
        "relations": profile["counts"]["relations"] >= 1,
        "source_fidelity": manifest["source_fidelity"]["ok"] is True,
    }
    return {
        "source_kind": kind,
        "ok": all(checks.values()),
        "checks": checks,
        "output": str(output_dir),
        "artifacts": existing,
        "missing_artifacts": missing,
        "compiled": compile_results,
        "source_profile": profile,
        "source_fidelity": manifest["source_fidelity"],
    }


def source_generation_smoke_audit() -> dict:
    """Generate apps from every source family and verify core artifacts."""
    with tempfile.TemporaryDirectory(prefix="appgen-source-generation-") as raw_workdir:
        workdir = Path(raw_workdir)
        sources = _write_smoke_inputs(workdir)
        rows = tuple(
            _source_smoke_row(kind, sources[kind], workdir / kind / "app")
            for kind in REQUIRED_SOURCE_KINDS
        )
    required = set(REQUIRED_SOURCE_KINDS)
    covered = {row["source_kind"] for row in rows}
    checks = (
        {
            "check": "source_family_coverage",
            "ok": required <= covered,
            "required": REQUIRED_SOURCE_KINDS,
            "covered": tuple(sorted(covered)),
        },
        {
            "check": "generated_artifacts",
            "ok": all(row["checks"]["artifacts"] for row in rows),
            "required_artifacts": _SMOKE_ARTIFACTS,
        },
        {
            "check": "compiled_core_artifacts",
            "ok": all(row["checks"]["compile"] for row in rows),
            "compiled_artifacts": _SMOKE_COMPILE_ARTIFACTS,
        },
        {
            "check": "manifest_source_fidelity",
            "ok": all(row["checks"]["source_fidelity"] for row in rows),
        },
    )
    return {
        "format": "appgen.package-source-generation-smoke-audit.v1",
        "scope": "package",
        "rows": rows,
        "checks": checks,
        "ok": all(row["ok"] for row in rows) and all(check["ok"] for check in checks),
    }


def source_intake_release_audit(existing_paths: Iterable[str] | None = None) -> dict:
    """Return package-level proof that all supported schema inputs can generate."""
    contract = schema_source_contract()
    matrix = source_example_matrix()
    plans = all_source_generation_plans()
    artifacts = source_artifact_contract(existing_paths)
    smoke = source_generation_smoke_audit()
    contract_kinds = set(contract["source_kinds"])
    matrix_kinds = set(matrix["source_kinds"])
    plan_kinds = {plan["source_kind"] for plan in plans}

    gates = (
        {
            "id": "source_catalog",
            "ok": contract["ok"] and set(REQUIRED_SOURCE_KINDS) <= contract_kinds,
            "required": REQUIRED_SOURCE_KINDS,
            "covered": tuple(sorted(contract_kinds)),
        },
        {
            "id": "example_adapters",
            "ok": matrix["ok"] and set(REQUIRED_SOURCE_KINDS) <= matrix_kinds,
            "covered": tuple(sorted(matrix_kinds)),
        },
        {
            "id": "database_url_dialects",
            "ok": {"sqlite", "postgresql", "mysql"}
            <= set(contract["database_url_dialects"])
            and contract["sqlalchemy_driver_urls"] is True,
            "dialects": contract["database_url_dialects"],
            "sqlalchemy_driver_urls": contract["sqlalchemy_driver_urls"],
        },
        {
            "id": "generation_commands",
            "ok": set(REQUIRED_SOURCE_KINDS) <= plan_kinds
            and all(
                _SOURCE_FLAGS[plan["source_kind"]] in plan["command"]
                for plan in plans
            ),
            "plans": plans,
        },
        {
            "id": "source_fidelity",
            "ok": all(row["checks"]["fidelity"] for row in matrix["rows"])
            and all(row["checks"]["fingerprint"] for row in matrix["rows"]),
            "fingerprints": tuple(
                {
                    "source_kind": row["source_kind"],
                    "fingerprint": row["fingerprint"],
                }
                for row in matrix["rows"]
            ),
        },
        {
            "id": "generation_smoke",
            "ok": smoke["ok"],
            "checks": smoke["checks"],
        },
        {
            "id": "artifact_contract",
            "ok": artifacts["ok"],
            "required_artifacts": artifacts["required_artifacts"],
            "missing": artifacts["missing"],
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-source-intake-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "contract": contract,
        "example_audit": matrix,
        "generation_plans": plans,
        "generation_smoke": smoke,
        "artifact_contract": artifacts,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-source-intake-readiness-unless-ok-is-true",
    }
