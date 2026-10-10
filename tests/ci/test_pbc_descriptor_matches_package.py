"""The catalog descriptor must say what the package actually does.

A PBC's descriptor is what composition, the workbench, and the release audit
read. Its package is what runs. They were allowed to drift because the catalog
row was hand-maintained and the package was not, so `dam_core`'s row declared
four tables while its package owned forty-nine.

The three reference PBCs are the ones the composition pass is proven on, so
their descriptors are held to exact equality with the package runtime: the same
owned tables, the same emitted events, the same consumed events. The manifest's
declared `tables` is a logical view of that inventory and is asserted to resolve
one-to-one into it, which is the weaker property that holds across all 147
packages while the stronger one is proven on three.
"""

import importlib

import pytest

from pyAppGen import pbc

REFERENCE_PBCS = ("dam_core", "gl_core", "ar_credit")


def _runtime(key: str):
    """Return the package module that holds the PBC's runtime constants."""
    return importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")


@pytest.mark.parametrize("key", REFERENCE_PBCS)
def test_descriptor_owned_tables_match_the_package_runtime(key: str) -> None:
    """Every table the package owns must appear in the descriptor."""
    prefix = key.upper()
    runtime = _runtime(key)
    declared = tuple(getattr(runtime, f"{prefix}_OWNED_TABLES"))
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])

    assert set(descriptor["owned_tables"]) == set(declared), key
    assert set(pbc._owned_tables(key)) == set(declared), key


@pytest.mark.parametrize("key", REFERENCE_PBCS)
def test_descriptor_events_match_the_package_runtime(key: str) -> None:
    """The emitted and consumed sets must be the package's, exactly."""
    prefix = key.upper()
    runtime = _runtime(key)
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])

    emitted = tuple(getattr(runtime, f"{prefix}_EMITTED_EVENT_TYPES"))
    consumed = tuple(getattr(runtime, f"{prefix}_CONSUMED_EVENT_TYPES"))

    assert set(descriptor["emits"]) == set(emitted), key
    assert set(descriptor["consumes"]) == set(consumed), key


@pytest.mark.parametrize("key", REFERENCE_PBCS)
def test_declared_tables_resolve_into_the_owned_inventory(key: str) -> None:
    """The manifest's logical tables must name tables the package owns.

    This is the property that holds for every package: a declared name resolves
    to exactly one owned physical table, and no two declared names collide on
    the same one. It is what lets `_table_contract` build a physical name
    without guessing.
    """
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])
    owned = pbc._owned_tables(key)

    resolved = [pbc._owned_table_name(key, table, owned) for table in descriptor["tables"]]
    unresolved = [name for name in resolved if name not in owned]
    assert not unresolved, f"{key} declares tables its package does not own: {unresolved}"
    assert len(set(resolved)) == len(resolved), f"{key} has two logical tables on one physical table"


def test_the_descriptor_is_not_a_stub_for_the_reference_pbcs() -> None:
    """A descriptor that under-reports its package is the defect being closed.

    `gl_core` and `ar_credit` each own more than their manifest declares, so a
    test that only compared `tables` would have passed on the drift. The owned
    inventory is what must be complete.
    """
    for key in REFERENCE_PBCS:
        descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])
        assert len(descriptor["owned_tables"]) >= len(descriptor["tables"]), key
        assert descriptor["owned_tables"], key


def test_gl_core_and_ar_credit_own_more_than_they_declare() -> None:
    """Pin the measured gap so a silent widening or narrowing fails CI.

    Both packages own event plumbing (`*_appgen_outbox_event`,
    `*_appgen_inbox_event`, `*_dead_letter_event`) that no manifest declares.
    `gl_core` additionally owns four domain tables its manifest omits. If a
    future manifest catches up, this test should be updated deliberately rather
    than drift unnoticed.
    """
    plumbing = ("appgen_outbox_event", "appgen_inbox_event", "dead_letter_event")

    def undeclared(key: str) -> set[str]:
        """Physical tables the package owns that its manifest never declares."""
        descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])
        owned = pbc._owned_tables(key)
        claimed = {pbc._owned_table_name(key, table, owned) for table in descriptor["tables"]}
        return set(owned) - claimed

    assert undeclared("gl_core") == {
        "gl_core_journal_event",
        "gl_core_account_projection",
        "gl_core_policy_rule",
        "gl_core_financial_model",
        *(f"gl_core_{name}" for name in plumbing),
    }
    assert undeclared("ar_credit") == {f"ar_credit_{name}" for name in plumbing}
    assert undeclared("dam_core") == set()
