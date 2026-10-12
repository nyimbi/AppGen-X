"""`_dsl_reference_text` must render for a schema with no tables.

The function builds the generated app's DSL reference from the first table in
the schema, and falls back to a literal `Book` table when there is none. That
fallback referenced `TableSchema`, which `gen.py` never imported, so the
no-tables branch raised `NameError: name 'TableSchema' is not defined`.

No test reached it: `tests/test_main.py` exercises `dsl_reference.py` a dozen
times, but always through a schema with tables, and pyright's
`reportUndefinedVariable` was the only thing that had noticed. A source with no
tables is a real input (an empty DSL document, an introspection that found
nothing), and it fails at generation time with a `NameError` rather than at the
point the fallback is chosen, so the message names neither the file nor the
reason.
"""

from __future__ import annotations

from pyAppGen.gen import _dsl_reference_text
from pyAppGen.schema import AppSchema, ColumnSchema, TableSchema


def test_the_empty_schema_fallback_renders() -> None:
    """An app with no tables still gets a reference, built from the fallback."""
    text = _dsl_reference_text(AppSchema(app_name="Empty", tables=()), "Empty")
    example = text[text.index("app Empty {"):]
    assert "table Book {" in example
    assert "view BookForm for Book {" in example


def test_a_schema_with_tables_still_uses_its_first_table() -> None:
    """The fallback must not shadow a real schema, or the reference goes stale."""
    schema = AppSchema(
        app_name="Ledger",
        tables=(
            TableSchema(
                name="journal_entry",
                columns=(
                    ColumnSchema("id", "integer", nullable=False, primary_key=True),
                    ColumnSchema("memo", "string", nullable=False),
                ),
            ),
        ),
    )
    text = _dsl_reference_text(schema, "Ledger")
    # `Book` is not unique to the fallback: it also names a table in the static
    # syntax glossary and in `DSL_EXPERIENCE_SAMPLE`. So the check reads the
    # generated example's own opening block, from `app Ledger {` to the first
    # `view`, which is the part that must track the schema.
    start = text.index("app Ledger {")
    example = text[start : text.index("view ", start)]
    assert "table journal_entry {" in example
    assert "table Book {" not in example


def test_the_fallback_canary_fails_when_the_name_is_missing(monkeypatch) -> None:
    """Point the check at the defect's own shape and confirm it raises.

    The fix is an import, so the canary removes it: with `TableSchema` unbound
    in the module namespace the no-tables branch must raise `NameError`. If it
    passes, the fallback is not being reached and the two tests above prove
    nothing about it.
    """
    from pyAppGen import gen

    monkeypatch.delattr(gen, "TableSchema", raising=False)
    try:
        _dsl_reference_text(AppSchema(app_name="Empty", tables=()), "Empty")
    except NameError as exc:
        assert "TableSchema" in str(exc)
    else:
        raise AssertionError("the no-tables branch no longer resolves TableSchema")
