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

To apply safe deterministic quick fixes to a file, run:

```bash
appgen --fix-dsl appgen.appgen
```

`--fix-dsl` rewrites only the explicit file you pass. It prints a JSON fix
report without echoing the full before/after source text, then exits with `0`
only when the fixed file passes the linter.

Example output:

```json
{
  "ok": true,
  "errors": [],
  "warnings": [],
  "suggestions": [
    "Add view blocks to design forms and Delphi-style component layouts."
  ],
  "fixes": [
    {
      "id": "add_app_declaration",
      "title": "Add an app declaration",
      "kind": "insert"
    }
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
from pyAppGen.dsl import apply_lint_fixes, lint_dsl, lint_dsl_file

report = lint_dsl_file("invoice.appgen")
assert report["ok"], report["errors"]

result = apply_lint_fixes("table Book { title: string ref Author.id }")
print(result["fixed"])
```

## Output Contract

Both the CLI and Python API return the same JSON-serializable structure:

```json
{
  "ok": false,
  "source": "invoice.appgen",
  "errors": ["Unknown view field: InvoiceForm.missing"],
  "warnings": ["Use an environment variable name for api_key, not a literal secret."],
  "suggestions": ["Add llm and agent blocks when the app needs agentic behavior."],
  "fixes": [
    {
      "id": "use_api_key_env",
      "title": "Use an environment variable for api_key",
      "kind": "regex_replace"
    }
  ],
  "summary": {
    "app": "InvoiceDesk",
    "tables": 3,
    "fields": 18,
    "views": 2,
    "flows": 1,
    "roles": 2,
    "rules": 1,
    "llm_providers": 1,
    "agents": 1,
    "targets": ["web", "pwa", "mobile", "desktop"],
    "unknown_targets": []
  }
}
```

Use `ok` as the machine gate. Use `errors` for blocking fixes, `warnings` for
risky but parseable source, `suggestions` for authoring guidance, and `fixes`
for structured IDE/CI actions such as adding an app declaration, replacing
legacy `ref` syntax with `->`, normalizing targets, or moving literal API keys
to environment-variable references.

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

It also returns structured quick fixes for common authoring feedback:

- `add_app_declaration`
- `insert_minimal_app`
- `replace_ref_with_arrow`
- `use_api_key_env`
- `normalize_targets`

The same fixes can be applied through `pyAppGen.dsl.apply_lint_fixes`. The
result has `format: appgen.dsl-fix-result.v1`, `applied`, `skipped`,
`changed`, `before`, `after`, `original`, and `fixed` fields so IDEs can show a
preview before writing.

## CI Gate

Use the CLI in CI before generation:

```bash
appgen --lint-dsl appgen.appgen
```

The command exits with status `1` when `ok` is false. A minimal pipeline can
then generate and compile artifacts:

```bash
appgen --lint-dsl appgen.appgen
appgen --dsl appgen.appgen --writedir build/generated-app
python -m py_compile build/generated-app/app/models.py
```

For pull requests, store the JSON output as an artifact so reviewers can see
the exact syntax, semantic, and style feedback that shaped the generated app.

## Generated App Linter

Generated apps also include `app/dsl_reference.py` with `dsl_lint(source)`.
That helper powers the generated DSL reference cockpit and the in-app Developer
Studio DSL editor. Generated lint reports include the same `fixes` shape so the
Studio can present deterministic quick actions without adding new language
keywords.

The generated linter is intentionally lightweight for in-app authoring. The
package-level `pyAppGen.dsl.lint_dsl` remains the authoritative gate because it
uses the ANTLR parser and canonical `AppSchema` validator.
