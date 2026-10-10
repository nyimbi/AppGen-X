"""Emit design-token stylesheets for consumers outside Python.

The Studio (``appgen-frontend``) is TypeScript, so it cannot import the token
module. It reads a generated ``tokens.css`` instead. This module writes that
file, and a test compares the checked-in copy against a fresh render so the two
cannot drift.

Run after editing ``design/tokens.json``::

    python -m pyAppGen.design_tokens_export
"""

from __future__ import annotations

import sys
from pathlib import Path

from .design_tokens import palette_for_theme, token_css_variables

__all__ = ("HEADER", "render_studio_tokens_css", "write_studio_tokens")

HEADER = """/* Generated from design/tokens.json by pyAppGen.design_tokens.
   Do not edit by hand: run `python -m pyAppGen.design_tokens_export` after
   changing the token file. A test fails if this drifts from the source. */
"""


def render_studio_tokens_css(theme: str = "appgen") -> str:
    """Return the Studio's token stylesheet for ``theme``."""
    lines = [HEADER, "", ":root {"]
    lines.extend(
        f"  {name}: {value};" for name, value in token_css_variables(palette_for_theme(theme))
    )
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def write_studio_tokens(repo_root: Path | None = None, theme: str = "appgen") -> Path:
    """Write the Studio token stylesheet and return its path."""
    root = repo_root or Path(__file__).resolve().parents[2]
    target = root / "appgen-frontend" / "src" / "tokens.css"
    target.write_text(render_studio_tokens_css(theme), encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    """Write the Studio token stylesheet."""
    target = write_studio_tokens()
    sys.stdout.write(f"wrote {target}\n")
    return 0


if __name__ == "__main__":  # pragma: no cover - module entrypoint
    raise SystemExit(main())
