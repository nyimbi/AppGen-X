"""Shared AppGen-X tooling command manifest."""

from __future__ import annotations

TOOLING_SUBCOMMANDS = (
    "lint",
    "semantic",
    "format",
    "validate",
    "generate",
    "graph",
    "graph-suite",
    "explain",
    "migration-plan",
    "nl-plan",
    "agent-handoff",
    "lsp",
    "verify",
    "package",
    "component-publish",
    "pbc",
    "designer-sync",
    "diagnostics",
    "parser-golden",
    "module-boundaries",
    "non-goals",
    "test-strategy",
    "dsl-quality",
    "dsl-antlr",
    "dsl-authoring-gate",
    "dsl-language-service",
    "contract-schema",
    "contract-validate",
    "runtime-contracts",
    "drift",
    "doctor",
    "command-docs",
    "requirements-trace",
    "contributor-tasks",
    "priority-order",
    "implementation-phases",
    "tooling-docs",
    "tooling-status",
    "tooling-audit",
)

TOOLING_HELP_LINES = (
    "lint, semantic, format, validate, generate, graph, graph-suite, explain,",
    "migration-plan, nl-plan, agent-handoff, lsp, verify, package, component-publish, pbc,",
    "designer-sync,",
    "diagnostics, parser-golden, module-boundaries, non-goals, test-strategy,",
    "dsl-quality, dsl-antlr, dsl-authoring-gate, dsl-language-service,",
    "contract-schema, contract-validate, runtime-contracts, drift, doctor,",
    "command-docs, requirements-trace, contributor-tasks, priority-order, implementation-phases,",
    "tooling-docs, tooling-status, and tooling-audit",
)


def tooling_command_set() -> frozenset[str]:
    """Return the command names recognized by lightweight entrypoints."""
    return frozenset(TOOLING_SUBCOMMANDS)


def tooling_help_block(indent: str = "  ") -> str:
    """Return wrapped command help lines for top-level CLI help."""
    return "\n".join(f"{indent}{line}" for line in TOOLING_HELP_LINES)
