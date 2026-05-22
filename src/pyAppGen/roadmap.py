"""Package-level roadmap release audit helpers.

Generated apps already expose roadmap evidence in ``low_code_features.py``.
This module gives the AppGen CLI the same kind of top-level proof before an app
has been generated.
"""

from __future__ import annotations

from pathlib import Path

from .capabilities import DEFAULT_CAPABILITIES


ROADMAP_DOCUMENTS = (
    {
        "path": "docs/ideas.md",
        "required_phrases": (
            "JHipster",
            "Generate a mobile app",
            "Generate a desktop app",
            "database design tool",
            "Data Model Library for an ERP",
        ),
    },
    {
        "path": "docs/base_features.md",
        "required_phrases": (
            "JHipster superset",
            "Delphi-style form design",
            "ERP templates",
            "agentic-system design",
            "natural-language evolution",
            "multi-platform generation",
        ),
    },
    {
        "path": "docs/Lo-code features.md",
        "required_phrases": (
            "Visual, drag-and-drop interface",
            "Cross-platform development support",
            "Pre-built templates",
            "custom widgets/components",
            "CRM and ERP systems",
        ),
    },
)

ROADMAP_CAPABILITY_REQUIREMENTS = (
    {
        "id": "schema-sources",
        "description": (
            "Generate applications from DBML, SQL, PonyORM, DSL, and existing "
            "databases."
        ),
        "capabilities": ("schema.import",),
    },
    {
        "id": "antlr-dsl",
        "description": (
            "Keep an intuitive ANTLR-backed DSL with linter, formatter, and "
            "release gates."
        ),
        "capabilities": ("dsl.language-design",),
    },
    {
        "id": "delphi-form-designer",
        "description": "Allow users to drop components onto forms in a Delphi-style designer.",
        "capabilities": ("ui.form-designer", "ui.visual-modeling"),
    },
    {
        "id": "multi-platform-generation",
        "description": "Generate web, PWA, mobile, desktop, and chatbot targets.",
        "capabilities": ("platform.targets", "platform.native"),
    },
    {
        "id": "agentic-systems",
        "description": "Design agentic systems connected to local and API-key LLM providers.",
        "capabilities": ("ai.agentic-systems",),
    },
    {
        "id": "natural-language-evolution",
        "description": (
            "Use natural language to evolve tables, forms, workflows, chatbots, "
            "agents, and ERP modules."
        ),
        "capabilities": ("ui.nl-evolution",),
    },
    {
        "id": "erp-templates",
        "description": (
            "Provide ERP modules for ledgers, accounts, invoicing, AP, AR, "
            "inventory, HR, and reports."
        ),
        "capabilities": ("components.erp-templates", "operations.finance"),
    },
    {
        "id": "robust-ide",
        "description": (
            "Provide an IDE for app generation, DSL authoring, database design, "
            "diagnostics, and management."
        ),
        "capabilities": ("devops.studio", "devops.ide-integration"),
    },
    {
        "id": "jhipster-plus",
        "description": "Preserve JHipster overlap while proving AppGen-only superiority areas.",
        "capabilities": (
            "platform.jhipster",
            "platform.jhipster-superiority",
            "platform.competitive-benchmark",
        ),
    },
    {
        "id": "secure-reliable-apps",
        "description": (
            "Generate secure, reliable, documented, testable, and "
            "runtime-assured applications."
        ),
        "capabilities": (
            "security.rbac",
            "security.session",
            "security.https",
            "ops.assurance",
            "quality.test-coverage",
        ),
    },
)


def _read_document(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def roadmap_document_checks(root: Path | str | None = None) -> tuple[dict, ...]:
    """Return checks that prove the current roadmap documents are present."""
    base = Path(root) if root is not None else Path.cwd()
    checks = []
    for document in ROADMAP_DOCUMENTS:
        text = _read_document(base, document["path"])
        missing_phrases = tuple(
            phrase
            for phrase in document["required_phrases"]
            if phrase.lower() not in text.lower()
        )
        checks.append(
            {
                "path": document["path"],
                "exists": bool(text),
                "required_phrases": document["required_phrases"],
                "missing_phrases": missing_phrases,
                "ok": bool(text) and not missing_phrases,
            }
        )
    return tuple(checks)


def roadmap_capability_checks() -> tuple[dict, ...]:
    """Return checks binding roadmap requirements to implemented capabilities."""
    capability_status = {
        capability.key: capability.status for capability in DEFAULT_CAPABILITIES
    }
    checks = []
    for requirement in ROADMAP_CAPABILITY_REQUIREMENTS:
        missing = tuple(
            key
            for key in requirement["capabilities"]
            if capability_status.get(key) != "implemented"
        )
        checks.append(
            {
                "id": requirement["id"],
                "description": requirement["description"],
                "capabilities": requirement["capabilities"],
                "missing_capabilities": missing,
                "ok": not missing,
            }
        )
    return tuple(checks)


def roadmap_release_audit(root: Path | str | None = None) -> dict:
    """Return package-level proof that roadmap docs map to implemented features."""
    documents = roadmap_document_checks(root)
    capability_checks = roadmap_capability_checks()
    gates = (
        {
            "id": "roadmap_documents",
            "ok": all(document["ok"] for document in documents),
            "documents": documents,
        },
        {
            "id": "capability_requirements",
            "ok": all(check["ok"] for check in capability_checks),
            "requirements": capability_checks,
        },
        {
            "id": "low_code_features_included",
            "ok": any(
                document["path"] == "docs/Lo-code features.md" and document["ok"]
                for document in documents
            ),
            "document": "docs/Lo-code features.md",
        },
        {
            "id": "jhipster_superset_claim_guarded",
            "ok": any(check["id"] == "jhipster-plus" and check["ok"] for check in capability_checks),
            "required_capabilities": (
                "platform.jhipster",
                "platform.jhipster-superiority",
                "platform.competitive-benchmark",
            ),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.roadmap-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "documents": documents,
        "requirements": capability_checks,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }
