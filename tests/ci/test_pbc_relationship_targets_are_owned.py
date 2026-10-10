"""Every relationship a PBC contract declares must point inside that PBC.

A contract's relationships are what the generated app turns into foreign keys.
`_table_contract` builds them from a logical `primary_table`, and the packages
spell that name two ways: `ar_credit` says `ar_customer` (the key prefixes it),
while `procurement_sourcing` says `procurement_sourcing_purchase_requisition`
(already physical). Prefixing unconditionally produced
`procurement_sourcing_procurement_sourcing_purchase_requisition`, which is in no
package's owned set.

The audit's `owned_tables` check is what caught it, and only after the table name
beside it stopped doubling: while both sides were doubled the subset test held by
accident. This test asserts the property directly, so a target that leaves the
owned set fails here rather than in a check that has to be reached through the
whole release audit.
"""

import pytest

from pyAppGen import pbc

REFERENCE_PBCS = ("dam_core", "gl_core", "ar_credit")


def _contract(key: str) -> dict:
    return pbc.pbc_implementation_contract(key)["owned_schema"]


def _outside_targets(key: str) -> list[str]:
    """Return relationship targets the package does not own."""
    schema = _contract(key)
    owned = {table["owned_table"] for table in schema["tables"]}
    return sorted({rel["target_table"] for rel in schema["relationships"]} - owned)


@pytest.mark.parametrize("key", REFERENCE_PBCS)
def test_a_reference_pbc_declares_relationships_inside_its_owned_set(key: str) -> None:
    """The three reference PBCs resolve every target to a table they own."""
    assert _outside_targets(key) == [], key


def test_no_pbc_declares_a_relationship_outside_its_owned_set() -> None:
    """The property holds across the whole implemented catalog, not just three.

    The defect was one unguarded prefix in shared code, so it could appear in any
    package whose service tables are named physically. Checking all of them costs
    about two seconds and is the only way to know the class is closed.
    """
    offenders = {key: outside for key in pbc.IMPLEMENTED_PBC_KEYS if (outside := _outside_targets(key))}
    assert not offenders, f"relationship targets outside the owned set: {offenders}"


def test_the_check_canaries_against_the_unguarded_prefix() -> None:
    """Point the check at the bug's own shape and confirm it reports it.

    `procurement_sourcing` is the package that exposed the defect. Applying the
    old, unguarded prefix to its relationship targets must produce names outside
    its owned set; if this canary passes, the check above is measuring something
    that can fail.
    """
    key = "procurement_sourcing"
    schema = _contract(key)
    owned = {table["owned_table"] for table in schema["tables"]}
    unguarded = {f"{key}_{rel['target_table']}" for rel in schema["relationships"]}

    assert unguarded - owned, "the canary produced no outside target, so the check is blind"
    assert _outside_targets(key) == [], "the shipped contract must not carry the unguarded form"
