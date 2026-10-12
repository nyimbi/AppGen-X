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

# The four fields the descriptor carries; the other five live only on the
# catalog literal, which is why they are not asserted here.
DESCRIPTOR_BACKED_FIELDS = ("tables", "apis", "emits", "consumes")


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
    target = "`asset_version`"
    assert target in original, "canary target not found; the patch would be a no-op"
    # The replacement must not contain the original token: the check matches by
    # substring, so renaming `asset_version` to `asset_version_renamed` leaves the
    # declared name inside the mutated text and the canary passes against
    # untouched behaviour. That was the first version of this test, and it failed
    # for the right reason -- the canary, not the check.
    try:
        path.write_text(original.replace(target, "`zz_removed_table`", 1))
        contract = pbc.pbc_specification_contract(key)
        assert contract["ok"] is False, "the check passed with a declared table absent"
    finally:
        path.write_text(original)
