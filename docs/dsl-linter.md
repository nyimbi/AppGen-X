# AppGen DSL Linter

The AppGen DSL linter validates syntax, semantics, and authoring style before
generation.

## CLI

```bash
appgen --lint-dsl appgen.appgen
```

The command prints JSON and exits with:

- `0` when the DSL is valid.
- `1` when syntax or semantic errors are found.

Example output:

```json
{
  "ok": true,
  "errors": [],
  "warnings": [],
  "suggestions": [
    "Add view blocks to design forms and Delphi-style component layouts."
  ],
  "summary": {
    "tables": 2,
    "views": 1,
    "targets": ["web", "mobile"]
  }
}
```

## Python API

```python
from pyAppGen.dsl import lint_dsl, lint_dsl_file

report = lint_dsl_file("invoice.appgen")
assert report["ok"], report["errors"]
```

## Checks

The package-level linter uses the ANTLR parser and schema validator, so it
checks:

- Syntax errors with line and column details from ANTLR.
- Unknown app targets.
- Duplicate tables, enums, views, flows, roles, rules, LLM providers, agents,
  and fields.
- Unknown relation source or target tables/fields.
- Unknown view fields and component placement fields.
- Unknown role resources and rule fields.
- Unknown agent LLM providers.
- Derived field references.

It also adds style feedback:

- Prefer `->` references over legacy `ref`.
- Use environment variable names for `api_key`.
- Add an `app` declaration for generated naming and targets.
- Add `view` blocks for form design.
- Add `llm` and `agent` blocks when agentic behavior is needed.

## Generated App Linter

Generated apps also include `app/dsl_reference.py` with `dsl_lint(source)`.
That helper powers the generated DSL reference cockpit and the in-app Developer
Studio DSL editor.

