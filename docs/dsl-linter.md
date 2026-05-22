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

To normalize spacing and indentation without applying semantic quick fixes, run:

```bash
appgen --format-dsl appgen.appgen
```

`--format-dsl` rewrites only the explicit file you pass. It prints an
`appgen.dsl-format-result.v1` JSON report without echoing the full before/after
source text, then exits with `0` only when the formatted file passes the linter.

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
from pyAppGen.dsl import apply_lint_fixes, dsl_code_actions, lint_dsl, lint_dsl_file

report = lint_dsl_file("invoice.appgen")
assert report["ok"], report["errors"]

actions = dsl_code_actions("table Book { title: string ref Author.id }")
print(actions[0]["fixed_preview"])

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
  "diagnostics": [
    {
      "severity": "error",
      "code": "unknown_view_field",
      "message": "Unknown view field: InvoiceForm.missing",
      "line": 12,
      "column": 8,
      "fix_ids": [],
      "hint": "invoice_number"
    }
  ],
  "fixes": [
    {
      "id": "use_api_key_env",
      "title": "Use an environment variable for api_key",
      "kind": "regex_replace"
    }
  ],
  "code_actions": [
    {
      "format": "appgen.dsl-code-action.v1",
      "id": "use_api_key_env",
      "title": "Use an environment variable for api_key",
      "kind": "quickfix",
      "diagnostic_codes": ["literal_api_key"],
      "edits": [
        {
          "range": {
            "start": {"line": 4, "character": 34},
            "end": {"line": 4, "character": 51}
          },
          "replacement": "api_key: OPENAI_API_KEY"
        }
      ]
    }
  ],
  "severity_counts": {
    "error": 1,
    "warning": 1,
    "suggestion": 1
  },
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
risky but parseable source, `suggestions` for authoring guidance,
`diagnostics` for IDE/CI annotations, `severity_counts` for status badges, and
`fixes` plus `code_actions` for structured IDE/CI actions
such as adding an app declaration, replacing legacy `ref` syntax with `->`,
normalizing targets, or moving literal API keys to environment-variable
references. Diagnostics include stable `code`, `severity`, optional line/column
location, related `fix_ids`, and typo hints for unknown view fields, component
fields, relation targets, and agent providers. It also reports authoring aliases
such as `entity`, `model`, `form`, `screen`, and `workflow`, which are accepted
before ANTLR parsing but should be normalized to `table`, `view`, and `flow` in
committed source.

Use `pyAppGen.dsl.dsl_authoring_release_gate(source)` as the stronger release
gate for the complete authoring loop. It combines language quality,
syntax/semantic linting, formatter stability, IDE navigation, code actions,
weighted authoring guidance, and source-family coverage for DBML, SQL, PonyORM,
live databases, and DSL files.

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
- Normalize authoring aliases to canonical DSL words without expanding the
  keyword budget.
- Normalize field modifier aliases, such as `searchable` and `hide`, to
  canonical `search` and `hidden` without expanding the keyword budget.
- Include `language_quality` with the ANTLR grammar path, generated parser path,
  keyword budget, keyword-free syntax, aliases, legacy contextual tokens, and
  learning path.
- Include `antlr_integrity` from `dsl_antlr_integrity_report()` so CI can catch
  drift between `lang/appgen.g4` and the generated ANTLR lexer/parser token and
  rule metadata.

It also returns structured quick fixes for common authoring feedback:

- `add_app_declaration`
- `insert_minimal_app`
- `replace_ref_with_arrow`
- `use_api_key_env`
- `normalize_authoring_aliases`
- `normalize_modifier_aliases`
- `normalize_targets`

The same fixes can be applied through `pyAppGen.dsl.apply_lint_fixes`. The
result has `format: appgen.dsl-fix-result.v1`, `applied`, `skipped`,
`changed`, `before`, `after`, `original`, and `fixed` fields so IDEs can show a
preview before writing.

Use `pyAppGen.dsl.dsl_code_actions` when an IDE needs quick-fix commands with
LSP-style edit ranges, related diagnostic codes, and a `fixed_preview`. These
actions use `format: appgen.dsl-code-action.v1` and reference the same stable
fix IDs returned by the linter, so editors can either apply the precise edits
or delegate to the `appgen.applyDslFix` command.

Use `pyAppGen.dsl.format_dsl` when the source is already semantically valid but
needs stable layout. The formatter returns `appgen.dsl-format-result.v1` with
the original text, formatted text, and before/after lint reports so IDEs and CI
can show a deterministic formatting preview without changing the keyword
budget.

## Language Service

Use `pyAppGen.dsl.dsl_language_service(source)` when an IDE, web editor, or
agent needs the complete authoring payload in one call. The result has
`format: appgen.dsl-language-service.v1` and includes:

- `lint`: the ANTLR-backed linter report.
- `outline`: `appgen.dsl-outline.v1` with app, table, field, view, component,
  flow, role, rule, LLM, and agent structure. Valid source is parsed through the
  canonical schema; incomplete drafts fall back to a regex outline so editors
  can still show navigation while the user is typing.
- `completions`: compact keyword completions, Delphi-style component snippets,
  app/table/form/LLM/agent snippets, and schema-aware table, field, reference,
  and provider symbols.
- `code_actions`: quick-fix commands with related diagnostics, LSP-style edit
  ranges, and deterministic fixed previews.
- `formatting`: the deterministic formatter preview.
- `language_quality`: the keyword-budget and ANTLR grammar evidence.
- `authoring_score`: weighted readiness checks and next actions that help IDEs
  guide users from a draft into a complete, canonical, formatted DSL source.

Lower-level integrations can call `dsl_outline(source)` and
`dsl_completion_items(prefix, source=source)` directly. These helpers are
package-level so generated Studio, external IDE plugins, and natural-language
agents can share one authoring contract.

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
