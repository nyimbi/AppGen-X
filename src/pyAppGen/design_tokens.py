"""Single source for AppGen-X design tokens.

``design/tokens.json`` is the canonical definition. The generated app's
stylesheet, the branding contract, and the Studio all read it through this
module, so a colour or spacing value cannot mean two things in two places.

The file is read once and cached. It ships inside the installed package at
``pyAppGen/design/tokens.json``; a repository checkout that carries the file at
the project root is used when the packaged copy is absent, which keeps the
generator working from a source tree before a build.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

__all__ = (
    "TOKEN_FILE_NAME",
    "focus_ring_value",
    "load_tokens",
    "palette_for_theme",
    "theme_names",
    "token_css_variables",
)

TOKEN_FILE_NAME = "tokens.json"


def _candidate_paths() -> tuple[Path, ...]:
    """Return token-file locations, most specific first."""
    here = Path(__file__).resolve()
    return (
        here.parent / "design" / TOKEN_FILE_NAME,
        here.parents[2] / "design" / TOKEN_FILE_NAME,
    )


@lru_cache(maxsize=1)
def load_tokens() -> dict:
    """Return the canonical token document.

    Raises:
        FileNotFoundError: when no token file is reachable, because a missing
            token source must fail loudly rather than fall back to stale
            hardcoded values.
    """
    for path in _candidate_paths():
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    searched = ", ".join(str(path) for path in _candidate_paths())
    raise FileNotFoundError(f"design token source not found; looked in: {searched}")


def theme_names() -> tuple[str, ...]:
    """Return the selectable theme names, in file order."""
    return tuple(load_tokens()["palette"])


def palette_for_theme(theme: str) -> dict[str, str]:
    """Return a copy of the palette for ``theme``.

    An unknown theme falls back to the ``appgen`` preset, matching the
    generator's long-standing behaviour of never failing on a bad theme name.
    """
    palettes = load_tokens()["palette"]
    return dict(palettes.get(theme, palettes["appgen"]))


def focus_ring_value(primary: str) -> str:
    """Return the focus-ring box-shadow for a primary colour.

    Built from the theme's primary so the ring reads as a tint of the brand
    rather than a fixed colour, with a documented fallback when the primary is
    not a six-digit hex.
    """
    spec = load_tokens()["focus_ring"]
    color = primary.lstrip("#")
    if len(color) == 6:
        try:
            red = int(color[0:2], 16)
            green = int(color[2:4], 16)
            blue = int(color[4:6], 16)
        except ValueError:
            pass
        else:
            return (
                f"0 0 0 {spec['spread']}px "
                f"rgba({red}, {green}, {blue}, {spec['alpha']})"
            )
    return spec["fallback"]


def _emittable(group: dict) -> tuple[tuple[str, str], ...]:
    """Return a token group's entries, skipping ``$``-prefixed annotations.

    The JSON carries prose under ``$comment`` keys for the humans reading it;
    those are documentation, not tokens, and must not become CSS variables.
    """
    return tuple(
        (name, value) for name, value in group.items() if not name.startswith("$")
    )


def token_css_variables(palette: dict[str, str]) -> tuple[tuple[str, str], ...]:
    """Return ``(--appgen-name, value)`` pairs for the whole token set.

    Palette entries come first so a consumer reading the variables in order
    sees the theme before the geometry. Values are strings; callers join them
    into a stylesheet.
    """
    tokens = load_tokens()
    variables: list[tuple[str, str]] = [
        ("--appgen-primary", palette["primary"]),
        ("--appgen-accent", palette["accent"]),
        ("--appgen-surface", palette["surface"]),
        ("--appgen-text", palette["text"]),
        ("--appgen-muted", palette["muted"]),
        ("--appgen-focus-ring", focus_ring_value(palette["primary"])),
    ]
    variables.extend(
        (f"--appgen-radius-{name}", value) for name, value in _emittable(tokens["radius"])
    )
    variables.extend(
        (f"--appgen-space-{name}", value) for name, value in _emittable(tokens["space"])
    )
    variables.extend(
        (f"--appgen-shadow-{name}", value) for name, value in _emittable(tokens["shadow"])
    )
    variables.extend(
        (f"--appgen-{name}", value)
        for name, value in _emittable(tokens["surface_detail"])
    )
    variables.extend(
        (f"--appgen-state-{name}", value) for name, value in _emittable(tokens["state"])
    )
    variables.append(("--appgen-touch-target", tokens["touch_target"]))
    typography = tokens["typography"]
    variables.append(("--appgen-font-body", typography["font_body"]))
    variables.extend(
        (f"--appgen-font-size-{name.removeprefix('size_')}", value)
        for name, value in _emittable(typography)
        if name.startswith("size_")
    )
    variables.append(("--appgen-line-height", typography["line_height"]))
    variables.append(("--appgen-content-max", tokens["content"]["max"]))
    variables.append(("--appgen-density-row", tokens["density"]["row"]))
    return tuple(variables)
