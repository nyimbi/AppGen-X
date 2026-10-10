"""The component kit is one source, and it must stay token-driven.

The kit is the shared block layer: the Studio aliases it from the repo and the
generator copies it into every generated app. Two failure modes matter here and
neither shows up in a type check.

First, a component that carries its own colour. The kit exists so a theme is a
palette swap; a literal hex in `components.css` is a component that will not
follow the theme, which is the divergence the design system was built to stop.

Second, a component the generator never emits. The kit is copied wholesale, so
a missing file is silent: the app builds, and one screen renders unstyled.

Both are asserted against the files on disk, so a new component cannot skip
them.
"""

import re
from pathlib import Path

import pytest

from pyAppGen.gen import write_ui_kit

REPO_ROOT = Path(__file__).resolve().parents[2]
KIT_SRC = REPO_ROOT / "src" / "pyAppGen" / "ui_kit" / "src"

# Colours belong in `design/tokens.json` and reach CSS as `var(--appgen-*)`.
# A component stylesheet carrying one of these is the defect.
LITERAL_COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(")


def _component_files() -> list[Path]:
    return sorted(path for path in KIT_SRC.glob("*.tsx"))


def test_the_kit_exists_and_exports_a_barrel():
    assert KIT_SRC.is_dir(), KIT_SRC
    barrel = (KIT_SRC / "index.ts").read_text(encoding="utf-8")

    for component in _component_files():
        name = component.stem
        assert f"from './{name}'" in barrel, f"{name} is not exported from the kit barrel"


def test_every_component_is_exported_and_no_export_is_dangling():
    barrel = (KIT_SRC / "index.ts").read_text(encoding="utf-8")
    exported = set(re.findall(r"from '\./([A-Za-z]+)'", barrel))
    present = {path.stem for path in KIT_SRC.glob("*.ts*")} - {"index"}

    assert exported == present, f"barrel and files disagree: {exported ^ present}"


def test_component_styles_carry_no_literal_colour():
    """A literal colour is a component that ignores the theme."""
    stylesheet = (KIT_SRC / "components.css").read_text(encoding="utf-8")
    body = re.sub(r"/\*.*?\*/", "", stylesheet, flags=re.DOTALL)

    offenders = [
        line.strip()
        for line in body.splitlines()
        if LITERAL_COLOUR.search(line) and "var(--appgen-" not in line
    ]

    assert not offenders, "literal colours in components.css:\n" + "\n".join(offenders)


def test_component_styles_use_tokens():
    stylesheet = (KIT_SRC / "components.css").read_text(encoding="utf-8")

    assert "var(--appgen-" in stylesheet
    # Every component the barrel exports should have at least one rule.
    for name in ("appgen-button", "appgen-card", "appgen-table", "appgen-dialog", "appgen-toast"):
        assert f".{name}" in stylesheet, name


def test_kit_is_copied_into_a_generated_app(tmp_path):
    target = write_ui_kit(tmp_path / "app")

    written = {path.name for path in target.iterdir()}
    source = {path.name for path in KIT_SRC.iterdir()}
    assert written == source, "the generated kit is missing files the source has"
    assert "index.ts" in written
    assert "components.css" in written

    copied = (target / "components.css").read_text(encoding="utf-8")
    assert copied == (KIT_SRC / "components.css").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", ["Button", "Input", "Select", "Card", "Table", "Badge", "Tabs", "Dialog", "Toast", "Tooltip", "EmptyState", "AppShell", "NavRail", "PageHeader", "WorkbenchLayout"])
def test_named_components_are_present(name):
    assert (KIT_SRC / f"{name}.tsx").is_file(), f"{name}.tsx is missing from the kit"
