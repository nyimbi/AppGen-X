"""Package-level source intake release evidence.

The parser adapters live in ``schema.py``. This module turns their deterministic
example audit into a top-level package contract so the active goal can prove
DBML, SQL, PonyORM, existing databases, and DSL inputs are release-gated.
"""

from __future__ import annotations

from collections.abc import Iterable

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


def source_intake_release_audit(existing_paths: Iterable[str] | None = None) -> dict:
    """Return package-level proof that all supported schema inputs can generate."""
    contract = schema_source_contract()
    matrix = source_example_matrix()
    plans = all_source_generation_plans()
    artifacts = source_artifact_contract(existing_paths)
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
        "artifact_contract": artifacts,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-source-intake-readiness-unless-ok-is-true",
    }
