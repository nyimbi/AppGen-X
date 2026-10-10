"""The composition DSL must declare each PBC's real tables, not a stub.

The starter DSL for a PBC composition is what a user generates an app from. It
declared three tables per PBC with the same `code`/`status`/`updated_at` body,
so a three-PBC app declared eighteen tables and described none of them:
`gl_core_journal_entry` had no journal, no debit, and no credit. The workbench
view was written against four columns that exist together in no package.

Both defects are the same one: a control (`pbc_schema`, which parses each
package's migration) existed and was not applied. These tests hold the DSL to
the migration's own inventory, and the view to the columns its bound table
actually has, so the stub cannot come back.
"""

import re

import pytest

from pyAppGen import pbc
from pyAppGen import pbc_schema
from pyAppGen.dsl import schema_from_dsl

COMPOSITION = ("dam_core", "gl_core", "ar_credit")


@pytest.fixture(scope="module")
def composed():
    """Return the parsed composition DSL for the three reference PBCs."""
    dsl = pbc.pbc_composition_dsl(COMPOSITION, app_name="LegoLedger")
    return dsl, schema_from_dsl(dsl, source_name="lego.appgen")


def test_every_owned_table_of_every_selected_pbc_is_declared(composed) -> None:
    """The declared set is the union of the three migrations' tables.

    The migration is the physical inventory, and it is the wider of the two
    surfaces: `gl_core`'s manifest names 24 tables while its migration declares
    31. A table the app does not declare cannot be rendered, so the DSL must
    carry the migration's set.
    """
    _dsl, schema = composed
    declared = {table.name for table in schema.tables}
    expected = set()
    for key in COMPOSITION:
        expected |= set(pbc_schema.owned_schema(key))

    assert declared == expected


def test_the_declared_tables_carry_their_real_columns(composed) -> None:
    """A declared table must describe its own columns, not a shared stub.

    The stub gave every table an `id`/`code`/`status`/`updated_at` body. The
    journal entry is the clearest counterexample: its identity is a journal and
    a period, and it has neither under the stub.
    """
    _dsl, schema = composed
    tables = {table.name: table for table in schema.tables}

    journal = {column.name for column in tables["gl_core_journal_entry"].columns}
    assert {"journal_id", "period_id", "approval_state"} <= journal

    invoice = {column.name for column in tables["ar_credit_ar_invoice"].columns}
    assert {"invoice_id", "customer_id", "total", "open_amount"} <= invoice

    asset = {column.name for column in tables["dam_core_asset"].columns}
    assert {"asset_id", "filename", "mime_type", "fingerprint"} <= asset


def test_no_declared_table_has_the_stub_body(composed) -> None:
    """`code`/`status`/`updated_at` and nothing else is the signature to catch."""
    _dsl, schema = composed
    stub = {"id", "code", "status", "updated_at"}
    offenders = [
        table.name
        for table in schema.tables
        if {column.name for column in table.columns} == stub
    ]
    assert not offenders, f"tables still carry the stub body: {offenders}"


def test_every_workbench_view_binds_columns_its_table_has(composed) -> None:
    """The view was written against columns no package's outbox declares.

    `gl_core` and `ar_credit` have no `status` or `published_at` on the outbox,
    so the view referenced columns the table did not have. Parsing enforces
    this, but the assertion is stated so a future regression names the cause.
    """
    _dsl, schema = composed
    tables = {table.name: {column.name for column in table.columns} for table in schema.tables}

    assert schema.views, "the composition declares no workbench view"
    for view in schema.views:
        assert view.table in tables, view.table
        missing = set(view.fields) - tables[view.table]
        assert not missing, f"{view.name} binds {sorted(missing)} which {view.table} lacks"


def test_each_selected_pbc_gets_exactly_one_workbench_view(composed) -> None:
    """A composition of three PBCs is three workbenches, one per PBC."""
    _dsl, schema = composed
    assert len(schema.views) == len(COMPOSITION)
    for key in COMPOSITION:
        assert any(view.table.startswith(f"{key}_") for view in schema.views), key


def test_the_dsl_declares_no_table_twice(composed) -> None:
    """A doubled prefix or a repeated name would declare one table as two."""
    dsl, _schema = composed
    declared = re.findall(r"(?m)^table\s+([A-Za-z_][A-Za-z0-9_]*)", dsl)
    assert len(declared) == len(set(declared)), "a table is declared more than once"

    # `dam_core_dam_core_asset` is the doubled prefix the logical-name path
    # produced before the owned name was used directly.
    doubled = [name for name in declared if name.split("_", 1)[0] + "_" + name.split("_", 1)[0] + "_" in name]
    assert not doubled, f"tables carry a doubled key prefix: {doubled}"
