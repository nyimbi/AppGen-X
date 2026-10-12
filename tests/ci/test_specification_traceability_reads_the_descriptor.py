"""The traceability check must read the descriptor, not the deleted literal.

`_pbc_specification_manifest_traceability` walked `PBC_CATALOG[key]` for nine
fields. The three reference PBCs had their `tables`, `emits`, and `consumes`
literals deleted when the descriptor moved to the package, so for those the loop
ran over an empty set, `missing` stayed empty, and the check certified a
specification against nothing. It passed while `dam_core`'s appendix named four
tables and its package owned forty-nine. A check that loops over a deleted
literal is the "gate that never ran" again: exit zero from a gate you have never
watched fail is not evidence, and neither is exit zero from a gate whose input
set is empty.

The check now reads `_pbc_descriptor`, which sources those four fields from the
package. These tests pin that: the declared counts must equal the package's own
inventory, and the appendix must name every one of them, so an empty declared set
fails instead of passing.
"""

import pathlib

import pytest

from pyAppGen import pbc
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS

# Every field the check reads is carried on the descriptor, which sources it
# from the package. Four come from the runtime constants directly; the five
# declared surfaces come from a runtime constant where one exists and the
# manifest otherwise.
DESCRIPTOR_BACKED_FIELDS = (
    "tables",
    "apis",
    "emits",
    "consumes",
    "ui_fragments",
    "permissions",
    "configuration",
    "standard_features",
    "advanced_capabilities",
)


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_traceability_declares_every_descriptor_surface(key: str) -> None:
    """The check must count the package's surface, not an empty literal.

    A `declared_count` of zero for `tables` on a package that owns tables is the
    vacuity this pins shut: the appendix can then name nothing and still pass.
    """
    contract = pbc.pbc_specification_contract(key)
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])
    declared = {
        field["field"]: field["declared_count"]
        for field in contract["manifest_traceability"]["fields"]
    }
    for field in DESCRIPTOR_BACKED_FIELDS:
        expected = len(descriptor.get(field) or ())
        assert declared[field] == expected, (key, field, declared[field], expected)


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_every_declared_surface_is_named_in_the_specification(key: str) -> None:
    """Every table and event the package declares must appear in its spec.

    The appendix is the specification's own traceability claim, so a table the
    package owns and the spec never names is the gap the check exists to find.
    """
    contract = pbc.pbc_specification_contract(key)
    for field in contract["manifest_traceability"]["fields"]:
        assert not field["missing"], (key, field["field"], field["missing"][:5])


def test_the_check_fails_when_a_declared_surface_is_absent() -> None:
    """Canary: removing a declared table name must fail the check.

    A passing canary is a bug in the canary, so this asserts the mutation
    actually applies before reading the result, and restores the text from a
    copy rather than with `git checkout`, which would revert unrelated work.
    """
    key = "dam_core"
    path = pathlib.Path(f"src/pyAppGen/pbcs/{key}/SPECIFICATION.md")
    original = path.read_text()
    target = "`asset_fingerprint`"
    assert target in original, "canary target not found; the patch would be a no-op"
    # The target must occur exactly once: the check matches by substring over the
    # whole specification, so a table name that is also a prefix of another
    # declared surface survives the mutation inside that longer token and the
    # canary passes against untouched behaviour. `asset_version` is a prefix of
    # the standard feature `asset_versioning`, which is why this uses
    # `asset_fingerprint`. That was the second version of this test, and it failed
    # for the right reason -- the canary, not the check.
    try:
        path.write_text(original.replace(target, "`zz_removed_table`", 1))
        contract = pbc.pbc_specification_contract(key)
        assert contract["ok"] is False, "the check passed with a declared table absent"
    finally:
        path.write_text(original)


def test_the_check_fails_when_a_declared_ui_fragment_is_absent() -> None:
    """Canary for a five-field surface, not just the four the descriptor had.

    `ui_fragments` used to be read from the catalog literal, which the descriptor
    migration emptied, so the check passed while `gl_core`'s appendix said "None
    declared" for thirteen real fragments. Now the descriptor carries it from the
    runtime constant, so removing a declared fragment from the appendix must fail
    the check. This is the canary the four-field test could not be: the defect
    lived in exactly the fields that test did not cover.
    """
    key = "gl_core"
    path = pathlib.Path(f"src/pyAppGen/pbcs/{key}/SPECIFICATION.md")
    original = path.read_text()
    target = "`GeneralLedgerWorkbench`"
    assert target in original, "canary target not found; the patch would be a no-op"
    try:
        path.write_text(original.replace(target, "`zz_removed_fragment`", 1))
        contract = pbc.pbc_specification_contract(key)
        assert contract["ok"] is False, "the check passed with a declared fragment absent"
    finally:
        path.write_text(original)
