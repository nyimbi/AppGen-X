"""The catalog descriptor must say what the package actually does.

A PBC's descriptor is what composition, the workbench, and the release audit
read. Its package is what runs. They were allowed to drift because the catalog
row was hand-maintained and the package was not, so `dam_core`'s row declared
four tables while its package owned forty-nine.

The descriptor is now derived from the package: `_pbc_descriptor` reads the
runtime constants for owned tables and for emitted and consumed events. That
makes "descriptor equals runtime" true by construction, so the property worth
gating is the one that can still fail: the package publishes its event surface
*twice*, as `*_EMITTED_EVENT_TYPES` in `runtime.py` and as `emits` in its
manifest, and those two hand-maintained lists had drifted apart in a dozen
packages in both directions. This file holds every PBC to agreement, and holds
the descriptor's declared tables to resolving one-to-one into the owned
inventory.
"""

import importlib

import pytest

from pyAppGen import pbc
from pyAppGen.pbc import IMPLEMENTED_PBC_KEYS


def _runtime(key: str):
    """Return the package module that holds the PBC's runtime constants."""
    return importlib.import_module(f"pyAppGen.pbcs.{key}.runtime")


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_descriptor_owned_tables_cover_the_package_runtime(key: str) -> None:
    """The descriptor must carry every table the package's runtime declares.

    `*_OWNED_TABLES` is the base declaration. `_owned_tables` folds it together
    with `*_RUNTIME_TABLES` and `*_runtime_capabilities().owned_tables`, which
    is where an extended package (a `domain_depth` or `slice_app` layer) reports
    the rest of its inventory. The descriptor must be the folded, complete set:
    a base constant that is smaller than the folded set is a package that
    extends itself, not drift, so the property is containment, not equality.
    """
    prefix = key.upper()
    runtime = _runtime(key)
    declared = set(getattr(runtime, f"{prefix}_OWNED_TABLES"))
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])

    assert declared <= set(descriptor["owned_tables"]), key
    assert set(descriptor["owned_tables"]) == set(pbc._owned_tables(key)), key


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_manifest_events_match_the_package_runtime(key: str) -> None:
    """The manifest and the runtime constant must name the same events.

    Both are hand-maintained. They drifted apart in a dozen packages: some
    manifests carried events with no emit site (`ForecastUpdated` for
    `product_catalog_pim`), and some runtime constants omitted events the code
    really emits (`field_service_management`'s eight workforce events). The
    descriptor reads the runtime constant, so a manifest that disagrees is a
    package that lies about its own surface.
    """
    prefix = key.upper()
    runtime = _runtime(key)
    manifest = pbc._package_manifest(key)

    emitted = set(getattr(runtime, f"{prefix}_EMITTED_EVENT_TYPES", ()))
    consumed = set(getattr(runtime, f"{prefix}_CONSUMED_EVENT_TYPES", ()))

    assert set(manifest.get("emits", ())) == emitted, key
    assert set(manifest.get("consumes", ())) == consumed, key


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_descriptor_events_match_the_package_runtime(key: str) -> None:
    """The descriptor's event surface is the package's, exactly."""
    prefix = key.upper()
    runtime = _runtime(key)
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])

    emitted = tuple(getattr(runtime, f"{prefix}_EMITTED_EVENT_TYPES"))
    consumed = tuple(getattr(runtime, f"{prefix}_CONSUMED_EVENT_TYPES"))

    assert set(descriptor["emits"]) == set(emitted), key
    assert set(descriptor["consumes"]) == set(consumed), key


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_declared_tables_resolve_into_the_owned_inventory(key: str) -> None:
    """The manifest's logical tables must name tables the package owns.

    A declared name resolves to exactly one owned physical table, and no two
    declared names collide on the same one. That is what lets `_table_contract`
    build a physical name without guessing.
    """
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])
    owned = pbc._owned_tables(key)

    resolved = [pbc._owned_table_name(key, table, owned) for table in descriptor["tables"]]
    unresolved = [name for name in resolved if name not in owned]
    assert not unresolved, f"{key} declares tables its package does not own: {unresolved}"
    assert len(set(resolved)) == len(resolved), f"{key} has two logical tables on one physical table"


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_the_descriptor_is_not_a_stub(key: str) -> None:
    """A descriptor that under-reports its package is the defect being closed.

    `gl_core` and `ar_credit` each own more than their manifest declares, so a
    test that only compared `tables` would have passed on the drift. The owned
    inventory is what must be complete.
    """
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])
    assert len(descriptor["owned_tables"]) >= len(descriptor["tables"]), key
    assert descriptor["owned_tables"], key


@pytest.mark.parametrize("key", IMPLEMENTED_PBC_KEYS)
def test_descriptive_fields_come_from_the_package(key: str) -> None:
    """The descriptor's label, mesh, and description are the package's.

    These were read from the catalog literal, which is a second copy of a fact
    the package owns. `description` had drifted in 22 packages (`dom`'s literal
    still described order verification while the package had grown to a full
    order-management suite) and `label`/`mesh` agreed by luck.

    The assertion is against the *package*, not against the descriptor's own
    fallback expression, so it fails if the read is reverted to the literal:
    the literal disagrees with the package for 22 descriptions, so a revert
    cannot pass. That is the regression this pins.
    """
    manifest = pbc._package_manifest(key)
    descriptor = pbc._pbc_descriptor(key, pbc.PBC_CATALOG[key])

    if manifest.get("label"):
        assert descriptor["label"] == manifest["label"], key
    if manifest.get("mesh"):
        assert descriptor["mesh"] == manifest["mesh"], key
    if manifest.get("description"):
        assert descriptor["description"] == manifest["description"], key


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
