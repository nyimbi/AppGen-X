"""Command-line entry point."""

from __future__ import annotations

import sys

from .gen import main as main


_TOOLING_SUBCOMMANDS = {
    "lint",
    "format",
    "validate",
    "graph",
    "explain",
    "migration-plan",
    "nl-plan",
    "lsp",
    "verify",
    "package",
    "pbc",
    "designer-sync",
    "diagnostics",
    "drift",
}
_legacy_click_main = main.main


def _tooling_aware_main(*args, **kwargs):
    """Dispatch new DSL tooling subcommands before legacy Click parsing."""
    argv = kwargs.get("args")
    if argv is None and args:
        argv = args[0]
    if argv is None and len(sys.argv) > 1:
        argv = sys.argv[1:]
    if argv is not None and len(argv) > 0 and argv[0] in _TOOLING_SUBCOMMANDS:
        from .dsl import dsl_tooling_cli

        raise SystemExit(dsl_tooling_cli(argv))
    return _legacy_click_main(*args, **kwargs)


main.main = _tooling_aware_main


if __name__ == "__main__":
    main(prog_name="appgen")  # pragma: no cover
