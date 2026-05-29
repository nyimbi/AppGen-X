"""Command-line entry point."""

from __future__ import annotations

import sys

_TOOLING_SUBCOMMANDS = {
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
    "pbc",
    "designer-sync",
    "diagnostics",
    "parser-golden",
    "drift",
    "doctor",
    "tooling-audit",
}


def _tooling_argv(*args, **kwargs):
    argv = kwargs.get("args")
    if argv is None and args:
        argv = args[0]
    if argv is None and len(sys.argv) > 1:
        argv = sys.argv[1:]
    return tuple(argv or ())


def _run_tooling(argv):
    from .dsl import dsl_tooling_cli

    raise SystemExit(dsl_tooling_cli(argv))


if _tooling_argv() and _tooling_argv()[0] in _TOOLING_SUBCOMMANDS:

    def main(*args, **kwargs):
        """Dispatch tooling subcommands without importing the legacy generator."""
        _run_tooling(_tooling_argv(*args, **kwargs))

else:
    from .gen import main as main

    _legacy_click_main = main.main

    def _tooling_aware_main(*args, **kwargs):
        """Dispatch new DSL tooling subcommands before legacy Click parsing."""
        argv = _tooling_argv(*args, **kwargs)
        if argv and argv[0] in _TOOLING_SUBCOMMANDS:
            _run_tooling(argv)
        return _legacy_click_main(*args, **kwargs)

    main.main = _tooling_aware_main


if __name__ == "__main__":
    main(prog_name="appgen")  # pragma: no cover
