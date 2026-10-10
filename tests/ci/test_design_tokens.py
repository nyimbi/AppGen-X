"""Tests for the canonical design-token source.

The token file is the single definition every consumer reads, so these tests
pin the two things that matter: the file is reachable and complete, and the
Python consumers derive from it rather than from literals of their own.
"""

import json
from pathlib import Path

import pytest

from pyAppGen import design_tokens
from pyAppGen.design_tokens import (
    focus_ring_value,
    load_tokens,
    palette_for_theme,
    theme_names,
    token_css_variables,
)


def test_token_file_is_reachable_from_the_package():
    tokens = load_tokens()

    assert isinstance(tokens, dict)
    assert tokens["version"]
    assert set(tokens["palette"]) >= {"appgen", "sage", "indigo", "slate"}


def test_every_theme_has_the_full_palette():
    required = {"primary", "accent", "surface", "text", "muted"}

    for theme in theme_names():
        palette = palette_for_theme(theme)
        assert required <= set(palette), theme
        for name, value in palette.items():
            assert value.startswith("#") and len(value) == 7, (theme, name, value)


def test_unknown_theme_falls_back_to_the_default_preset():
    assert palette_for_theme("no_such_theme") == palette_for_theme("appgen")


def test_focus_ring_is_derived_from_the_primary_colour():
    ring = focus_ring_value("#0f766e")

    assert ring == "0 0 0 3px rgba(15, 118, 110, 0.28)"


def test_focus_ring_falls_back_on_a_non_hex_primary():
    assert focus_ring_value("not-a-colour") == load_tokens()["focus_ring"]["fallback"]


def test_css_variables_carry_no_annotation_keys():
    """``$``-prefixed JSON keys are prose for readers, not CSS variables.

    The token file documents groups with ``$comment`` entries. If one leaked
    into the emitted variables it would render as a nonsense custom property.
    """
    names = [name for name, _ in token_css_variables(palette_for_theme("appgen"))]

    assert not any("$" in name for name in names)
    assert len(names) == len(set(names)), "duplicate custom property"


def test_theme_css_reads_the_token_file(tmp_path, monkeypatch):
    """The emitted stylesheet must change when the token file changes.

    This is the drift guard: if ``_theme_css_text`` ever goes back to
    hardcoded literals, editing the token file stops moving the output and
    this test fails.
    """
    from pyAppGen.gen import _branding_contract, _theme_css_text
    from pyAppGen.dsl import schema_from_dsl
    from pyAppGen.roadmap import EXCELLENCE_SAMPLE_DSL

    schema = schema_from_dsl(EXCELLENCE_SAMPLE_DSL, source_name="token-drift.appgen")
    baseline = _theme_css_text(_branding_contract(schema))
    assert "--appgen-space-4: 16px;" in baseline

    tokens = json.loads(json.dumps(load_tokens()))
    tokens["space"]["4"] = "17px"
    mutated = tmp_path / "tokens.json"
    mutated.write_text(json.dumps(tokens), encoding="utf-8")

    monkeypatch.setattr(design_tokens, "_candidate_paths", lambda: (mutated,))
    design_tokens.load_tokens.cache_clear()
    try:
        drifted = _theme_css_text(_branding_contract(schema))
        assert "--appgen-space-4: 17px;" in drifted
        assert "--appgen-space-4: 16px;" not in drifted
    finally:
        design_tokens.load_tokens.cache_clear()


def test_theme_css_matches_the_shipped_default_palette():
    """The default theme's variables must equal the file's appgen palette."""
    palette = palette_for_theme("appgen")
    variables = dict(token_css_variables(palette))

    assert variables["--appgen-primary"] == palette["primary"]
    assert variables["--appgen-accent"] == palette["accent"]
    assert variables["--appgen-touch-target"] == "44px"


@pytest.mark.parametrize("theme", theme_names())
def test_every_theme_emits_a_complete_variable_set(theme):
    variables = dict(token_css_variables(palette_for_theme(theme)))

    for required in (
        "--appgen-primary",
        "--appgen-focus-ring",
        "--appgen-radius-md",
        "--appgen-space-5",
        "--appgen-state-invalid",
        "--appgen-font-size-xl",
        "--appgen-density-row",
    ):
        assert required in variables, (theme, required)


def test_repo_root_token_path_resolves_to_the_packaged_file():
    """``design/tokens.json`` and the packaged copy must be one file.

    Two files would be two sources and therefore two truths, so the repo-root
    path is a symlink onto the packaged copy.
    """
    repo_root = Path(__file__).resolve().parents[2]
    root_token = repo_root / "design" / "tokens.json"
    packaged = repo_root / "src" / "pyAppGen" / "design" / "tokens.json"

    assert root_token.exists()
    assert packaged.exists()
    assert root_token.resolve() == packaged.resolve()


def test_studio_stylesheet_is_in_sync_with_the_token_source():
    """The Studio's generated ``tokens.css`` must match a fresh render.

    The Studio is TypeScript and cannot import the token module, so it reads a
    generated stylesheet. If someone edits that file by hand, or changes the
    token file without regenerating, the Studio's tokens silently diverge from
    the generated apps'. This is the guard against that.
    """
    from pyAppGen.design_tokens_export import render_studio_tokens_css

    repo_root = Path(__file__).resolve().parents[2]
    on_disk = repo_root / "appgen-frontend" / "src" / "tokens.css"

    assert on_disk.exists(), "run `python -m pyAppGen.design_tokens_export`"
    assert on_disk.read_text(encoding="utf-8") == render_studio_tokens_css()


def test_studio_entry_imports_the_token_stylesheet():
    """The generated stylesheet only counts if the Studio loads it."""
    repo_root = Path(__file__).resolve().parents[2]
    main_tsx = (repo_root / "appgen-frontend" / "src" / "main.tsx").read_text(
        encoding="utf-8"
    )

    assert "./tokens.css" in main_tsx
