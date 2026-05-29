# AppGen-X DSL Tooling Specification

AppGen-X needs a complete DSL tooling stack, not just a grammar. The platform
must make authoring, reviewing, generating, packaging, and evolving applications
safe across the CLI, IDE, language server, visual designers, generated apps,
and agent workflows.

This document is the implementation specification for that tooling. It keeps the
language surface generic while making the surrounding tooling strong enough for
enterprise application generation, PBC composition, database-backed form design,
workflow design, agentic-system design, and natural-language evolution.

## Goals

The tooling stack must provide:

- one shared parser and semantic model used by every surface;
- deterministic linting, formatting, and validation;
- IDE feedback while the user types;
- safe refactors across tables, fields, views, flows, operations, PBC contracts,
  packages, and deployment units;
- generator-ready normalized application metadata;
- machine-readable diagnostics and fix suggestions;
- graph and explain output for human review;
- migration planning for PostgreSQL and MySQL-compatible backends;
- natural-language change planning that produces DSL diffs before code changes;
- release evidence for generated apps and PBCs.

## Non-Goals

The tooling must not:

- hard-code specific PBC names into the grammar;
- let visual designers create database-backed fields that do not resolve to
  columns, calculated fields, or valid lookup paths;
- treat generated code as the source of truth when the DSL can express the
  intent;
- expose arbitrary backend/runtime pickers that multiply the generator matrix;
- accept direct secret literals in DSL files;
- let agents bypass linting, semantic validation, or release evidence.

## Core Architecture

All tooling should consume the same pipeline.

```text
source files
  -> parse tree
  -> AST
  -> symbol table
  -> normalized semantic model
  -> diagnostics
  -> graphs and indexes
  -> generator, CLI, LSP, IDE, tests, natural-language planner
```

The parser is necessary but not sufficient. The semantic model is the contract
that prevents drift between the linter, IDE, generator, language server, visual
designers, and natural-language tools.

### Proposed Modules

| Module | Responsibility |
| --- | --- |
| `pyAppGen.dsl.parser` | Parse source text through the generated ANTLR parser and return parse trees plus syntax diagnostics. |
| `pyAppGen.dsl.ast` | Convert parse trees into stable dataclass-style AST nodes. |
| `pyAppGen.dsl.symbols` | Build symbol tables for apps, tables, fields, views, flows, operations, roles, rules, PBCs, APIs, events, jobs, reports, menus, components, packages, tests, LLMs, agents, deployments, audit blocks, versions, and security blocks. |
| `pyAppGen.dsl.semantic` | Resolve references, normalize schema, resolve lookup paths, build workflow graphs, bind PBC catalog entries, and produce semantic diagnostics. |
| `pyAppGen.dsl.diagnostics` | Define diagnostic codes, severities, related locations, and fix IDs. |
| `pyAppGen.dsl.formatter` | Produce stable formatted DSL while preserving comments where possible. |
| `pyAppGen.dsl.lsp` | Implement language-server features on top of the semantic model. |
| `pyAppGen.dsl.cli` | Provide command-line entry points and JSON/text report contracts. |
| `pyAppGen.dsl.graphs` | Emit ER, lookup, workflow, handler, PBC, security, agent, package, and deployment graphs. |
| `pyAppGen.dsl.migrations` | Compare semantic models and generate migration plans. |
| `pyAppGen.dsl.nl_plan` | Convert natural-language requests into constrained DSL edit plans. |
| `pyAppGen.dsl.release` | Produce release evidence and drift checks for generated applications. |

The exact file layout can evolve, but these boundaries should remain visible.
The parser, semantic model, diagnostics, and formatter must be usable without
starting a web app or generator.

## Semantic Model Contract

The semantic model should be serializable to JSON and stable enough for CLI,
IDE, tests, and agents.

Required top-level fields:

```json
{
  "format": "appgen.semantic-model.v1",
  "source_files": [],
  "app": {},
  "symbols": {},
  "tables": {},
  "views": {},
  "flows": {},
  "operations": {},
  "rules": {},
  "roles": {},
  "security": {},
  "agents": {},
  "llms": {},
  "pbcs": {},
  "composition": {},
  "contracts": {},
  "deployment": {},
  "packages": {},
  "graphs": {},
  "diagnostics": []
}
```

### Symbol Table

Every named declaration must produce a symbol:

```json
{
  "id": "table.Invoice",
  "kind": "table",
  "name": "Invoice",
  "file": "finance.appgen",
  "range": {"start": {"line": 4, "character": 0}, "end": {"line": 15, "character": 1}},
  "references": ["view.InvoiceForm", "rule.InvoicePolicy"]
}
```

Symbol kinds include:

- `app`
- `table`
- `field`
- `group`
- `enum`
- `enum_value`
- `view`
- `component_binding`
- `handler`
- `flow`
- `flow_state`
- `operation`
- `role`
- `permission`
- `rule`
- `llm`
- `agent`
- `agent_skill`
- `pbc`
- `composition`
- `api`
- `event`
- `job`
- `report`
- `menu`
- `component`
- `package`
- `deployment_unit`
- `audit`
- `version`
- `security`

Symbol coverage is executable through `appgen.symbol-coverage.v1`. The semantic
model includes this report as `symbol_coverage`, and `appgen doctor --json`
checks `semantic_symbol_coverage` against a fixture that exercises top-level
declarations plus nested groups, fields, enum values, component bindings,
handlers, flow states, permissions, agent skills, and deployment units.

### Table Model

Each table should normalize fields, directives, relationships, calculated
fields, lookup aliases, indexes, uniqueness, checks, and backend constraints.

```json
{
  "name": "Invoice",
  "fields": {
    "customer_id": {
      "type": "int",
      "required": true,
      "relationship": {
        "target_table": "Customer",
        "target_field": "id",
        "cardinality": "many-to-one",
        "alias": "customer"
      }
    },
    "total": {
      "type": "decimal",
      "calculated": true,
      "expression": "subtotal + tax"
    }
  },
  "lookup_paths": {
    "customer.name": {
      "chain": ["Invoice.customer_id", "Customer.name"],
      "valid": true
    }
  }
}
```

### View Model

Views must bind only to real fields, calculated fields, or valid lookup paths.
The model should distinguish section fields from component placements and event
handlers.

```json
{
  "name": "InvoiceForm",
  "table": "Invoice",
  "sections": [{"name": "Header", "fields": ["invoice_number", "customer.name"]}],
  "components": [
    {"binding": "customer.name", "component": "Lookup", "x": 4, "y": 0, "w": 4, "h": 1}
  ],
  "handlers": [{"event": "Save", "target": "SubmitInvoice"}]
}
```

### Workflow Model

Flows should normalize states, transitions, directives, participants, human
tasks, timers, compensation, and handler targets.

```json
{
  "name": "SubmitInvoice",
  "states": ["draft", "reviewed", "approved", "posted"],
  "transitions": [
    {"from": "draft", "to": "reviewed"},
    {"from": "approved", "to": "posted"}
  ],
  "human_tasks": [
    {"name": "FinanceReview", "assignee": "Accountant", "to": "approved"}
  ],
  "timers": [{"state": "reviewed", "duration": "P2D", "to": "escalated"}],
  "compensations": [{"state": "posted", "operation": "ReverseInvoice"}]
}
```

### PBC And Composition Model

The grammar remains generic. Concrete PBC names are resolved through the
registered PBC catalog and package manifests.

```json
{
  "composition": "FinanceSuite",
  "includes": [
    {"pbc": "gl_core", "version": "1.0.0", "catalog_resolved": true},
    {"pbc": "ap_automation", "version": "1.0.0", "catalog_resolved": true}
  ],
  "connections": [
    {
      "from_pbc": "ap_automation",
      "from_kind": "event",
      "from_contract": "InvoiceApproved",
      "to_pbc": "gl_core",
      "to_kind": "command",
      "to_contract": "PostJournal"
    }
  ]
}
```

## Diagnostic Specification

Diagnostics must be machine-readable, stable, and documented. Every diagnostic
has:

- `code`
- `title`
- `severity`: `error`, `warning`, `info`, or `hint`
- `message`
- `range`
- `related_locations`
- `fixes`
- `docs_url`

### Diagnostic Code Ranges

| Range | Area |
| --- | --- |
| `AGX0000-AGX0099` | Syntax and parser errors. |
| `AGX0100-AGX0199` | Naming, duplicates, reserved words, and style. |
| `AGX0200-AGX0299` | Tables, fields, types, defaults, calculated fields, and directives. |
| `AGX0300-AGX0399` | Relationships, foreign keys, lookup paths, and multi-hop traversal. |
| `AGX0400-AGX0499` | Views, visual components, handlers, menus, and UI binding. |
| `AGX0500-AGX0599` | Rules, expressions, required checks, and policy actions. |
| `AGX0600-AGX0699` | Flows, workflow states, timers, human tasks, and compensation. |
| `AGX0700-AGX0799` | Roles, permissions, security, tenancy, and secrets. |
| `AGX0800-AGX0899` | APIs, events, jobs, reports, packages, deployment, audit, and versioning. |
| `AGX0900-AGX0999` | PBC catalog, composition, cross-PBC contracts, and package manifests. |
| `AGX1000-AGX1099` | LLMs, agents, skills, tools, and model/provider configuration. |
| `AGX1100-AGX1199` | Migration planning and destructive-change detection. |
| `AGX1200-AGX1299` | Natural-language change plans and agent safety. |
| `AGX9000-AGX9999` | Internal tooling errors and unsupported parser states. |

### Required Diagnostics

| Code | Severity | Trigger | Example Fix |
| --- | --- | --- | --- |
| `AGX0001` | error | Source cannot be parsed. | Show syntax location and nearest valid construct. |
| `AGX0101` | error | Duplicate top-level declaration in the same namespace. | Rename one symbol. |
| `AGX0201` | error | Field references unknown type where no custom type is allowed. | Create enum/table/type or choose known scalar. |
| `AGX0202` | error | Calculated field references unknown field. | Create field or fix expression. |
| `AGX0301` | error | Relationship target table does not exist. | Create table or correct target. |
| `AGX0302` | error | Relationship target field does not exist. | Create field or correct target. |
| `AGX0303` | error | Lookup path cannot be resolved. | Add relationship or change binding. |
| `AGX0304` | error | Multi-hop lookup chain breaks at an intermediate segment. | Add missing relationship. |
| `AGX0401` | error | View subject table does not exist. | Create table or correct `for` target. |
| `AGX0402` | error | Database-backed view binding is not a field, calculated field, or lookup path. | Replace binding or create valid field/path. |
| `AGX0403` | error | Handler target does not resolve. | Create operation/flow/agent/contract target. |
| `AGX0404` | warning | Component is unknown to the registered component catalog. | Use known component or register one. |
| `AGX0501` | error | Rule expression uses single `=` instead of `==`. | Rewrite equality operator. |
| `AGX0502` | error | Rule references unknown field. | Correct field or lookup path. |
| `AGX0601` | error | Flow transition references undeclared or unreachable state where strict mode is enabled. | Add transition or state directive. |
| `AGX0602` | warning | Human task has no assignee/participant. | Add participant or assignment. |
| `AGX0701` | error | Permission references unknown resource. | Create resource or correct permission subject. |
| `AGX0702` | error | Secret literal appears in source. | Replace with env/secret binding. |
| `AGX0801` | error | Deployment unit target is unknown. | Use supported unit kind. |
| `AGX0802` | error | Package target does not match app targets. | Add app target or change package target. |
| `AGX0901` | error | Composition includes unknown PBC key. | Register PBC or correct key. |
| `AGX0902` | error | Cross-PBC connection references unknown event/API/command. | Declare contract or correct reference. |
| `AGX0903` | error | PBC attempts shared private-table access. | Use API/event/projection contract. |
| `AGX1001` | error | Agent skill target does not resolve. | Create operation/flow/contract target. |
| `AGX1002` | error | Agent has write-capable skill with no permission. | Add permission or remove skill. |
| `AGX1101` | warning | Migration plan contains destructive drop. | Require explicit migration approval. |
| `AGX1201` | error | Natural-language plan cannot be represented as DSL diff. | Ask for narrower DSL-scoped change. |

### Diagnostic Example

Bad DSL:

```appgen
view InvoiceForm for Invoice {
  Main: customer.display_name
}
```

If `Invoice.customer_id -> Customer.id` exists but `Customer.display_name` does
not, the linter should return:

```json
{
  "code": "AGX0303",
  "severity": "error",
  "title": "Unresolved lookup path",
  "message": "customer.display_name does not resolve from table Invoice.",
  "range": {"start": {"line": 2, "character": 8}, "end": {"line": 2, "character": 29}},
  "fixes": [
    {"id": "replace_with_customer.name", "title": "Use customer.name"},
    {"id": "create_customer_display_name", "title": "Create calculated field Customer.display_name"}
  ]
}
```

## Linter Specification

The linter must run in three stages:

1. **Syntax stage**: parser errors, invalid tokens, unterminated strings,
   malformed blocks.
2. **Semantic stage**: references, lookup paths, handler targets, workflows,
   PBC catalog bindings, permissions, deployment/package compatibility.
3. **Policy stage**: enterprise safety, style, secrets, catalog rules,
   release-readiness checks.

### Linter Inputs

- One `.appgen` file.
- A directory containing multiple `.appgen` files.
- Optional registered PBC catalog path.
- Optional component catalog path.
- Optional generator target profile.
- Optional previous semantic-model JSON for migration comparison.

Directory input is an executable contract, not just a planned mode:
`appgen lint path/to/appgen --json` recursively discovers `*.appgen` files,
sorts them for deterministic output, runs the same single-file lint contract for
each file, aggregates diagnostics with a `file` field, and returns one
`appgen.lint-report.v1` payload with `source_mode: "directory"` and nested
`file_reports`.

### Linter Outputs

Text mode is for humans. JSON mode is for CI, IDEs, agents, and generated apps.

```json
{
  "format": "appgen.lint-report.v1",
  "ok": false,
  "files": ["finance.appgen"],
  "severity_counts": {"error": 1, "warning": 0, "info": 0, "hint": 0},
  "diagnostics": [],
  "fixes_available": true,
  "semantic_model_available": false
}
```

### Linter Rules By Domain

Tables:

- primary key exists or can be generated;
- field names are unique inside a table;
- defaults match field type where known;
- calculated expressions reference existing fields;
- relationship targets resolve;
- table directives reference existing fields/calculated fields/lookup paths.

Views and forms:

- `for` table exists;
- section fields resolve;
- component bindings resolve;
- placement rectangles are non-negative and non-zero;
- unknown components are warnings unless strict component mode is enabled;
- handlers target declared operations, flows, agents, APIs, events, jobs, or
  supported navigation targets.

Workflows:

- transitions form a valid graph;
- directives are captured in the workflow model;
- human tasks have assignable participants in strict mode;
- timers use recognizable duration literals;
- compensation targets resolve to operations or flows.

PBCs and composition:

- included PBCs are declared locally or registered in the catalog;
- versions are present for catalog PBC includes;
- cross-PBC connections reference exposed APIs, events, or commands;
- private tables are not referenced across PBC boundaries;
- datastore backend is one of the allowed backends.

Agents:

- LLM provider references resolve;
- agent skill targets resolve;
- write-capable skills require permissions;
- API keys use environment variable references;
- local model endpoints are configuration, not secrets.

Deployment and packages:

- package targets match app targets;
- deployment units have supported kinds;
- health checks target declared units;
- environment bindings name variables without literal secret values;
- mobile and desktop packages declare signing posture before release.

## Formatter Specification

The formatter must be deterministic and idempotent. Running it twice must
produce byte-identical output.

### Formatting Rules

- Two-space indentation.
- One declaration statement per line inside blocks.
- One blank line between top-level declarations.
- Keep comments attached to the nearest following node when possible.
- Preserve file-level comments at the top of the file.
- Normalize optional semicolons away by default, except in compact one-line
  examples if preserve mode is enabled.
- Place field modifiers in this order: `pk`, `required`, `unique`, `hidden`,
  `search`, `default`, relationship arrow.
- Keep calculated expression immediately after the type: `total: decimal = subtotal + tax`.
- Order table fields as identity, business keys, relationship fields, editable
  scalar fields, calculated fields, audit fields, directives when `--organize`
  is enabled.
- Do not reorder top-level declarations by default; users often keep domain
  context by proximity.

### Formatter Output

```json
{
  "format": "appgen.format-result.v1",
  "changed": true,
  "idempotent": true,
  "diagnostics": [],
  "text": "app FinanceOps { ... }"
}
```

The executable formatter contract also proves comment preservation for
file-level, declaration-adjacent, and inline comments, plus canonical field
modifier ordering for `pk`, `required`, `unique`, `hidden`, `search`, `default`,
and relationship arrows.
`appgen.formatter-contract-audit.v1` is the machine-readable proof for these
guarantees. It also verifies that the organize profile preserves top-level
declaration order while ordering table bodies by identity, business keys,
relationships, editable fields, calculated fields, audit fields, and
directives.

## CLI Contracts

The installed command should expose current compatibility flags and the newer
subcommands below. `apg` is a supported short alias for the same command surface
as `appgen`. Existing flags may remain as aliases.

### `appgen lint`

```console
appgen lint app.appgen
appgen lint app.appgen --json
appgen lint src/appgen --strict --catalog docs/pbc-catalog.json
```

`--catalog` loads a component catalog JSON file. The catalog may list component
names directly or under `components`, `component_catalog`,
`registered_components`, or `items` entries. `--strict` is an executable
component-catalog gate. In normal mode, unknown visual components remain
`AGX0404` warnings so drafts can be explored. In strict mode, the same
diagnostics are promoted to errors and the command exits `1`, which lets CI,
agents, and release flows block unregistered component use while still allowing
catalog-registered components.

Exit codes:

- `0`: no errors;
- `1`: lint errors;
- `2`: CLI usage/configuration error;
- `3`: internal tool error.

Internal tool errors emit `appgen.internal-error.v1` with `AGX9000`
diagnostics instead of a Python traceback. Argparse usage/configuration
failures remain exit code `2`. Missing user-supplied input paths are treated as
configuration errors and return exit code `2` before the tooling engine reads
or generates artifacts. Invalid enumerated options, including graph kind and
database backend choices, are also rejected by argparse with exit code `2`.

The executable CLI contract tests cover JSON schemas, default text summaries,
success and failure exit codes, and argparse usage failures for invalid choices
or missing required options.

### `appgen format`

```console
appgen format app.appgen --check
appgen format app.appgen --write
appgen format app.appgen --json
```

`--check` exits `1` when formatting changes are needed.
`--write` rewrites the source file when the formatted text differs and the JSON
payload reports `write_requested`, `written`, and `write_path` so IDEs and CI can
distinguish a preview from an actual file mutation.
`--organize` enables the optional table-body organization profile: identity
fields and spreads, business keys, relationships, editable scalar fields,
calculated fields, audit fields, and directives are ordered inside each table
without reordering top-level declarations.

### `appgen validate`

```console
appgen validate app.appgen --targets web,mobile,desktop --json
```

Runs lint plus generator-readiness checks without writing generated code.
Requested `--targets` are normalized with the same platform target policy as
the app declaration. Validation fails with `AGX0802` when a requested target is
unknown or is not declared by `app ... { targets: ... }`, and the
`appgen.validate-report.v1` payload includes `requested_targets`, `app_targets`,
and a `target_compatibility` check.

### `appgen generate`

```console
appgen generate app.appgen --out generated/app
appgen generate app.appgen --target web --target mobile --out generated/app
```

Generation fails before writing artifacts when lint has errors. Lint warnings
also block generation by default; `--allow-warnings` permits warning-only
sources and does not permit errors.

### `appgen graph`

```console
appgen graph app.appgen --kind er --format mermaid
appgen graph app.appgen --kind workflow --format json
appgen graph app.appgen --kind pbc --format dot
```

### `appgen graph-suite`

```console
appgen graph-suite app.appgen --json
```

Emits `appgen.graph-suite-report.v1` release evidence for every required graph
kind and renders each graph as JSON, Mermaid, and DOT. This command is the
preferred CI and IDE health check because it proves that graph previews,
documentation diagrams, release evidence, and downstream graph tooling all use
the same semantic model.

Supported graph kinds:

- `er`
- `lookup`
- `workflow`
- `handler`
- `pbc`
- `security`
- `agent`
- `deployment`
- `package`

### `appgen explain`

```console
appgen explain app.appgen --symbol Invoice.customer_id
appgen explain app.appgen --diagnostic AGX0303
appgen explain app.appgen --handler InvoiceForm.Save
```

Explain output should be human-readable by default and JSON with `--json`.

### `appgen doctor`

Checks parser generation, Python package imports, catalog availability, template
paths, generator backends, and optional IDE/LSP dependencies. The doctor report
also embeds a VS Code extension surface check so the editor scaffold, command
palette entries, language configuration, syntax grammar, and LSP provider
registrations are verified from the same command used in CI.

### `appgen tooling-audit`

```console
appgen tooling-audit --json
```

Emits `appgen.tooling-audit.v1`, the executable release gate for this document.
The audit composes evidence from the shared semantic model, diagnostic fixtures,
linter, formatter, validation/generation contracts, graph/explain tooling,
language server, code-action application, visual designer round trips, VS Code
extension surface, Studio semantic service, migration coverage,
natural-language planner, package/release verifiers, PBC catalog tooling,
parser golden fixtures, drift audit, and doctor checks. The language-server
portion exercises the JSON-RPC request handlers for open/change diagnostics,
completion, hover, definition, references, symbols, code actions, formatting,
rename, and workspace symbol search. A passing report means every audited
requirement section has a concrete machine-readable proof instead of relying on
prose or scattered manual checks.

### `appgen package`

```console
appgen package app.appgen --target desktop --out dist
appgen package app.appgen --target mobile --out dist
```

Runs package validation, signing posture checks, release evidence generation,
and target-specific smoke checks.
`--target` accepts only `web`, `mobile`, `desktop`, `pbc`, `deployment`, or
`all`; invalid package targets are CLI configuration errors and return exit
code `2`.

When `--out` is provided, the command writes `appgen-release-evidence.json`
plus one `appgen-package-<target>.json` manifest per selected target. These
target manifests use `appgen.package-manifest.v1` and provide deterministic
handoff evidence for downstream web builders, mobile signing/offline launch
pipelines, desktop installer/startup packaging, PBC publication, and deployment
verification. Generated installers and app-store bundles remain downstream
builders' responsibility, but the package command now materializes the stable
contract those builders consume.
`appgen.package-verify-cli-audit.v1` exercises `appgen verify --target all` and
`appgen package --target all --out ...`, then proves that release evidence and
per-target manifests exist for web, mobile, desktop, PBC, and deployment
handoffs. The audit checks target-specific handoff metadata rather than only
successful command exit codes, so downstream builders receive stable contracts
for routes/forms/handlers, mobile signing/offline launch, desktop installer and
startup assets, PBC publication, and deployment topology verification.

### `appgen pbc`

```console
appgen pbc list
appgen pbc verify src/pyAppGen/pbcs/gl_core
appgen pbc publish src/pyAppGen/pbcs/gl_core --catalog local
```

PBC commands operate on manifests and package directories, not grammar changes.
`publish` emits `appgen.pbc-publish-report.v1`; it loads the package
entrypoint, validates the manifest, proves the manifest is publishable, returns
the catalog patch, attaches release-evidence verification, and records that the
publish plan is side-effect-free. Catalog writes are an explicit downstream
step, not an implicit CLI side effect.

### `appgen nl-plan`

```console
appgen nl-plan app.appgen --prompt "Add credit memos to accounts receivable" --json
```

Produces a proposed DSL diff, lint report, migration preview, and test plan. It
must not write generated code unless the DSL diff validates.

## Language Server Specification

The language server should use the same parser, semantic model, diagnostics,
formatter, and graph builders as the CLI.

The executable launch path is:

```bash
appgen lsp --stdio
```

`--stdio` starts the JSON-RPC language server over standard input/output. It
accepts `initialize`, `shutdown`, `exit`, `textDocument/didOpen`,
`textDocument/didChange`, completion, hover, definition, references, document
symbols, rename, code actions, formatting, and workspace symbol requests. The
server keeps an in-memory document cache for open `.appgen` buffers and
publishes diagnostics after open/change notifications using the same
`appgen.semantic-model.v1` and linter reports as the CLI. Workspace symbol,
definition, reference, and completion requests scan each open DSL document
individually instead of concatenating files, so editor features keep working
when an application is split across multiple `.appgen` files. Rename uses the
active document for identifier validation and migration safety, then returns a
workspace edit that updates the matching identifier across every open DSL
document.

The executable tooling audit includes `appgen.lsp-stdio-transport-audit.v1`,
which sends real `Content-Length` JSON-RPC frames through the stdio transport
and verifies initialize, diagnostics publication, shutdown, and exit handling.

### Capabilities

| LSP Feature | Required Behavior |
| --- | --- |
| `textDocument/didOpen` and `didChange` | Incrementally parse, rebuild affected semantic model parts, publish diagnostics. |
| `textDocument/completion` | Complete keywords, block-local directives, table names, fields, lookup paths, components, handler events, operation targets, flow states, PBC keys, APIs, events, package targets, deployment units, LLM providers, and agent skills. |
| `textDocument/hover` | Show keyword docs, symbol summary, field type, relationship target, lookup resolution, handler target, PBC catalog metadata, and diagnostic explanation. |
| `textDocument/definition` | Navigate from references to declarations for fields, tables, views, flows, operations, roles, PBCs, APIs, events, packages, and deployment units. |
| `textDocument/references` | Find all references across workspace DSL files and generated contract indexes. |
| `textDocument/documentSymbol` | Return hierarchical outline: app, tables, fields, views, sections, components, handlers, flows, operations, PBCs, packages, deployment. |
| `textDocument/rename` | Rename symbols safely and update references; block unsafe renames when migration impact is ambiguous. |
| `textDocument/codeAction` | Offer quick fixes for missing declarations, typo suggestions, create operation from handler, create event contract, add lookup directive, add permission, remove secret literal, and remove invalid stream/runtime picker fields. |
| `textDocument/formatting` | Call the shared formatter. |
| `workspace/symbol` | Search declarations by name, kind, and catalog metadata. |

Document-symbol outline depth is executable. View symbols include child
`view_section`, `component_binding`, and `handler` entries so IDE outline trees
can navigate form layout sections, dropped components, and event wiring without
reparsing view bodies.

Hover depth is executable. Hovering a registered PBC key returns
`appgen.lsp-pbc-hover.v1` metadata with label, mesh, datastore profile, and
sample API/event contracts. Hovering a symbol that participates in a diagnostic
returns the diagnostic code plus the same explanation object used by
`appgen explain --diagnostic`, so IDEs and agents can show the cause and docs
target without duplicating diagnostic registries.

Workspace symbol search includes catalog-backed results. In addition to open
DSL declarations, `workspace/symbol` returns `catalog://pbc/...` locations for
registered PBCs and their API/event contracts when the query matches PBC names,
labels, mesh metadata, descriptions, or contract names. This lets editors and
agents discover selectable PBCs without hard-coding the catalog into grammar
rules.
Definition navigation uses the same catalog location scheme for registered PBC
keys and API/event contract tokens, so `textDocument/definition` can jump from
composition references to read-only catalog declarations as well as to ordinary
DSL declarations.
Reference search also includes those read-only catalog indexes. When a user or
agent asks for references to a PBC key or catalog API/event contract,
`textDocument/references` returns ordinary workspace occurrences plus the
matching `catalog://pbc/...` index location, which keeps generated PBC contracts
discoverable without making catalog entries look like editable DSL source.

Rename safety is an executable gate. The language service still returns the
candidate workspace edit and migration preview, but `textDocument/rename`
returns `ok: false` with an `AGX1101` blocker when the preview requires
explicit migration approval, such as destructive relationship changes. The
blocker includes an `add_rename_hint` fix suggestion so agents and IDEs can ask
for an explicit migration decision before applying the edit.

### Completion Sources

Completions should be context-aware:

- top-level: language constructs such as `table`, `view`, `flow`, `pbc`,
  `composition`, `deploy`, `agent`;
- table body: field snippets, directives, relationship targets, group spreads;
- view body: table fields, lookup paths, component names, handler snippets;
- flow body: state names, directive snippets, operation targets;
- composition body: registered PBC keys, versions, APIs, events, commands;
- deploy body: declared units, target kinds, health/check/resource snippets;
- agent body: LLM names, operation targets, permission subjects.

Completion coverage is executable through `appgen.completion-coverage.v1`.
The language service includes this report as `completionCoverage`, and
`appgen doctor --json` checks `lsp_completion_coverage` against a fixture that
exercises keywords, snippets, table names, fields, lookup paths, components,
handler events, operation targets, flow states, PBC keys, aggregate PBC
contracts, explicit PBC APIs, PBC events, PBC command-style contracts, package
targets, deployment units, LLM providers, and agent skills.

### Code Actions

Required code actions:

- create missing table;
- create missing field;
- create calculated field for unresolved form binding;
- create operation from handler target;
- create flow from handler target;
- create event contract;
- add relationship for lookup path;
- replace typo with nearest symbol;
- add missing permission for agent skill;
- replace secret literal with `env` binding;
- register or import PBC manifest;
- add package for app target;
- create smoke test declaration for operation/flow/PBC.

Code-action application is executable through
`appgen.lsp-code-action-apply.v1`. The CLI supports
`appgen lsp app.appgen --apply-code-action <id> --json`, returning patched DSL,
applied text edits, and the lint result after applying the selected quick fix.
This is the evidence path for missing-operation, lookup-directive,
event-contract, relationship, typo, secret-literal replacement, invalid
runtime/stream/backend picker removal, PBC manifest, agent-permission, package
creation for app targets, and smoke-test declaration quick fixes used by IDEs
and agents. `appgen.lsp-code-action-cli-audit.v1` must cover the same required
action ids as the in-process `appgen.lsp-code-action-apply-audit.v1` release
gate so external agents and editor integrations are not weaker than library
callers.

## IDE Integration

Two editor surfaces are required.

### VS Code Extension

The VS Code extension should provide:

- language-server activation for `.appgen` files;
- syntax highlighting;
- diagnostics panel integration;
- code actions and quick fixes;
- outline tree;
- graph previews;
- generated artifact preview;
- command palette actions for lint, format, graph, explain, generate, and
  package;
- PBC catalog browser.

The repository ships the extension scaffold at `extensions/vscode-appgen-x`.
It contributes the `appgen` language for `.appgen`, `.ag`, and `.ags` files,
syntax highlighting, language configuration, command palette entries, and a
dependency-free JSON-RPC client that launches `appgen lsp --stdio`. The client
registers VS Code providers for diagnostics, completion, hover, definition,
references, document symbols, workspace symbols, rename, code actions, and
formatting, while command palette actions call the same CLI contracts for lint,
format, graph, explain, generate, and package. Graph previews, generated
artifact previews, and the PBC catalog browser render CLI JSON reports in
webview panels rather than relying on editor-specific state.

### AppGen-X Studio / Monaco

The web IDE should reuse the same language server or a compatible semantic
service.

Required Studio surfaces:

- DSL editor;
- component palette;
- form designer synchronized with DSL;
- database designer synchronized with DSL;
- workflow designer synchronized with DSL;
- PBC composition designer synchronized with DSL;
- package/deployment designer synchronized with DSL;
- diagnostics and quick-fix panel;
- graph/explain panel;
- natural-language change planner with DSL diff preview.

Visual designers must never create state that cannot round-trip through the
DSL semantic model. The executable `appgen designer-sync` contract returns DSL
diff previews, patched source, the after-edit semantic model, changed designer
surfaces, and refreshed projections for accepted visual edits. Form, database,
workflow, PBC composition, and package/deployment edit paths must validate the
patched DSL before the Studio accepts the visual operation.
`--edit-json` must be a JSON object; malformed edit payloads are CLI
configuration errors and return exit code `2` before any designer mutation is
accepted.
Designer edit coverage is executable through
`appgen.designer-visual-edit-matrix.v1`. The matrix proves database field
edits, form component placement, workflow transitions, PBC composition
includes, package creation, deployment-unit creation, and invalid form binding
rejection all pass through the same linted DSL patch and projection refresh
path before acceptance.

The package-level Studio now exposes `appgen.studio-semantic-service.v1` as the
shared web IDE bridge. That contract composes `appgen.lsp-service.v1`,
`appgen.designer-sync-report.v1`, `appgen.graph-suite-report.v1`, and
`appgen.nl-plan.v1` so the DSL editor, component palette, form designer,
database designer, workflow designer, PBC composition designer,
package/deployment designer, diagnostics panel, graph/explain panel, and
natural-language planner all prove they are reading the same semantic source.
The frontend renders the same bridge through a dedicated semantic-service
panel, and the browser smoke contract includes that panel as a required
scenario.

## Graph Tooling

Graph output must be available from CLI, IDE, tests, and release evidence.

| Graph | Nodes | Edges | Use |
| --- | --- | --- | --- |
| Entity relationship | Tables, fields | Foreign keys | Database review, migration planning. |
| Lookup | Table fields, relationship aliases, lookup paths | Path hops | Form validation and automatic lookup controls. |
| Workflow | States, tasks, timers, operations | Transitions | Workflow review and generated runtime checks. |
| Handler | Views, components, events, operations, flows, agents | Event calls | UI architecture and test generation. |
| PBC | PBCs, APIs, events, commands | Contract connections | Composition review. |
| Security | Roles, permissions, resources, agents | Grants | Authorization review. |
| Agent | Agents, LLMs, skills, operations, permissions | Tool access | Agent safety review. |
| Deployment | Units, packages, resources, health checks | Runs-on and depends-on | Operations review. |
| Package | Targets, packages, signing, assets | Builds | Release review. |

Formats:

- JSON for tools;
- Mermaid for docs and previews;
- DOT for graph tooling;
- SVG/PNG only as generated artifacts, not as source of truth.

## Migration Planner

The migration planner compares two semantic models.

Inputs:

- previous semantic model;
- current semantic model;
- target backend: `postgresql`, `mysql`, or compatible profile;
- optional rename hints.

Output:

```json
{
  "format": "appgen.migration-plan.v1",
  "ok": false,
  "backend": "postgresql",
  "changes": [],
  "destructive": true,
  "requires_approval": true,
  "diagnostics": []
}
```

Required detections:

- added table;
- dropped table;
- renamed table candidate;
- added field;
- dropped field;
- renamed field candidate;
- type change;
- nullability change;
- default change;
- relationship change;
- unique/index/check change;
- calculated-field change;
- PBC ownership transfer;
- data backfill requirement.

Executable migration tests now prove first-class change records for table-level
index directives, uniqueness constraints, constraint/check directives, and PBC
table ownership transfer. Unknown table directives are still reported as
generic directive changes so generators can remain conservative.

Every migration report includes `appgen.migration-coverage.v1`, listing the
required detection families, the families detected by the current comparison,
and the missing families. CI, IDE previews, and agents should use this coverage
object to prove that a fixture or migration scenario exercises the required
table, field, relationship, directive, calculated-field, PBC ownership, and
backfill cases instead of inferring coverage from prose.

Destructive changes must require explicit approval and should include suggested
safe alternatives when possible.

## Natural-Language Change Planner

Natural language is a development vector, but it must produce DSL diffs first.

Pipeline:

```text
user request
  -> intent classification
  -> bounded edit plan
  -> DSL patch
  -> lint
  -> migration preview
  -> generated test plan
  -> user/agent review
  -> generation
```

Planner output:

```json
{
  "format": "appgen.nl-plan.v1",
  "prompt": "Add credit memos",
  "intent": "domain_feature",
  "dsl_patch": "...",
  "affected_symbols": [],
  "lint": {},
  "migration_preview": {},
  "test_plan": [],
  "token_budget_notes": []
}
```

Small-model guidance:

- prefer constrained edit operations over free-form rewriting;
- provide symbol tables and snippets, not whole projects;
- require agents to return patches, not regenerated code blobs;
- run lint after every proposed patch;
- reject plans that cannot be represented as DSL.

Supported edit operations:

- add table;
- add field;
- add relationship;
- add view section;
- add component placement;
- add handler;
- add operation;
- add rule;
- add flow transition;
- add PBC include;
- add API/event contract;
- add package/deployment unit;
- add agent skill and permission.

`appgen.nl-plan-contract-audit.v1` is the executable proof for this list. It
runs a fixture prompt for each supported operation, verifies that accepted
requests produce DSL patches, lint results, migration previews, generated test
plans, and token-budget notes, and verifies that out-of-DSL requests are
rejected with `AGX1201` instead of generating code.
The CLI proof mirrors the same operation family through
`appgen.nl-plan-cli-audit.v1`: each supported edit operation is exercised
through `appgen nl-plan --json`, then checked for the expected operation kind,
linted patch, migration preview, generated test plan, and token-budget notes.
This keeps agent-facing development paths honest; a capability is not counted
as available just because an in-process helper can produce it.

## Package And Verifier Tooling

Release verifiers should generate evidence for each target.

Web verifier:

- app builds;
- routes exist;
- generated forms bind valid fields;
- handler targets resolve;
- smoke tests run.

Mobile verifier:

- package metadata exists;
- signing posture declared;
- offline policy declared where needed;
- permissions are explained;
- generated screens fit target density;
- smoke launch path exists.

Desktop verifier:

- package metadata exists;
- installer/update posture declared;
- splash/startup assets declared where used;
- menus and context menus bind to handlers;
- smoke launch path exists.

PBC verifier:

- manifest validates;
- package artifacts exist;
- owned tables have migrations/models;
- APIs/events/handlers are declared;
- no private cross-PBC table mutation;
- self-registration is side-effect-free;
- release evidence exists.

Deployment verifier:

- units declared;
- health checks declared;
- environment variables named;
- secret values absent;
- resource hints present for production units;
- topology graph is connected and explainable.

## Test Strategy

Tooling tests must be fixture-driven and deterministic.

| Test Family | Required Coverage |
| --- | --- |
| Parser golden tests | Valid/invalid DSL examples for every grammar construct, enforced by `appgen parser-golden --json` and the `appgen.parser-golden-audit.v1` report. |
| Semantic tests | Symbol table, lookup paths, handler targets, PBC catalog binding, workflows, packages, deployments. |
| Diagnostic golden tests | Every diagnostic code has at least one fixture and expected JSON output. |
| Formatter tests | Idempotency, comment preservation, modifier ordering, stable output. |
| CLI contract tests | Exit codes, JSON schemas, text summaries, bad arguments. |
| LSP tests | Completion, hover, definition, references, rename, code actions, formatting. |
| Graph tests | ER, lookup, workflow, handler, PBC, security, agent, package, deployment graph output. |
| Migration tests | Add/drop/rename/type/nullability/default/relationship/index scenarios. |
| Natural-language planner tests | Prompt-to-DSL patch fixtures, lint integration, rejected unsafe plans. |
| Verifier tests | Web/mobile/desktop/PBC/deployment release evidence contracts. |
| Drift tests | CLI, LSP, IDE, generator, and tests consume the same semantic model. |

### Parser Golden Audit

`appgen parser-golden --json` is the executable gate for grammar coverage. It is intentionally independent of project files: the command runs the checked-in golden fixture catalog and fails when any valid fixture stops parsing, any invalid fixture starts parsing, or any required grammar construct is not represented by a valid fixture.

The report contract is `appgen.parser-golden-audit.v1`:

- `ok`: true only when fixture outcomes and construct coverage pass;
- `constructs_required`: the grammar surface the platform promises to keep covered;
- `constructs_covered`: constructs proven by valid fixtures;
- `missing_constructs`: constructs that need new valid examples before release;
- `fixtures`: per-fixture parse outcome, validity expectation, construct tags, and syntax error text;
- `blocking_gaps`: the exact fixture failures that should block CI.

The required construct set includes application options, table fields, reusable field groups, spreads, derived fields, modifiers, relationships, relationship cardinality, table directives, enums, views, component placement, handlers, flows, workflow directives, roles, permissions, rules, rule expressions, LLM definitions, agents, PBCs, PBC composition include/require/expose/connect clauses, audit blocks, deployment units/scale/health/check/resource/env/directives, version blocks, operations, security, APIs, events, jobs, reports, menus, component contracts, packages, and tests.

When a new keyword, block, nested item, or syntax form is added to `lang/appgen.g4`, the same change must add or extend a parser golden fixture before the grammar is considered release-ready. Diagnostic golden fixtures are still required for semantic behavior, but parser-golden fixtures prove that the grammar itself accepts and rejects the intended language forms.

## Implementation Phases

### Phase 0: Inventory And Stabilization

- Inventory existing parser, linter, formatter, release-audit, PBC catalog, and
  generator code.
- Identify duplicate semantic logic.
- Define JSON schemas for diagnostics and semantic model.
- Add fixture directories and built-in fixture catalogs for parser-golden,
  diagnostic-golden, formatter, semantic drift, graph, migration, and verifier
  tests.

Exit criteria:

- Current behavior documented.
- No new generator behavior required.
- Tooling fixtures can run in CI, including `appgen parser-golden --json`,
  `appgen diagnostics --audit-fixtures --json`, and `appgen drift <file> --json`.

### Phase 1: Shared Semantic Model MVP

- Create shared parser wrapper.
- Create AST conversion layer.
- Build symbol table.
- Resolve tables, fields, relationships, lookup paths, views, handlers, flows,
  operations, PBC includes, packages, and deployment units.
- Emit `appgen.semantic-model.v1`.

Exit criteria:

- CLI and tests can load the same semantic model.
- Database-backed form field validation uses the shared model.
- PBC catalog validation uses the shared model.

### Phase 2: Linter And Formatter

- Implement diagnostic registry.
- Implement linter stage separation.
- Implement formatter idempotency.
- Add JSON/text CLI output.
- Add quick-fix IDs.

Exit criteria:

- All required diagnostic families have fixtures.
- `appgen lint --json` and `appgen format --check` are stable.
- Existing DSL release audit consumes the new reports.

### Phase 3: CLI And Graph Tooling

- Add subcommands for lint, format, validate, graph, explain, package, PBC, and
  natural-language planning.
- Add graph builders.
- Add explain output for symbols and diagnostics.

Exit criteria:

- CI can use command outputs without parsing prose.
- Graph output is available in JSON and Mermaid.

### Phase 4: Language Server

- Implement LSP server using the shared semantic model.
- Add diagnostics, completion, hover, definition, references, document symbols,
  rename, code actions, and formatting.
- Add fixture-based LSP tests.

Exit criteria:

- VS Code can edit `.appgen` with live diagnostics and completion.
- Rename/code actions update all references safely in fixtures.

### Phase 5: IDE And Visual Designer Integration

- Integrate Monaco or the LSP semantic service.
- Bind form designer, database designer, workflow designer, PBC designer,
  package designer, and deployment designer to semantic-model changes.
- Prove round-trip DSL sync.

Exit criteria:

- Visual edits generate DSL patches.
- DSL edits update visual designers.
- Invalid visual edits are rejected with diagnostics.

### Phase 6: Migration, Natural Language, And Release Verifiers

- Implement migration planner.
- Implement natural-language DSL patch planner.
- Implement package and deployment verifiers.
- Emit release evidence bundles.

Exit criteria:

- Natural-language changes produce linted DSL diffs.
- Migration plans detect destructive changes.
- Web/mobile/desktop/PBC/deployment verifiers produce machine-readable evidence.

## Contributor Task Breakdown

Good first implementation tasks:

- define diagnostic dataclasses and JSON schema;
- add diagnostic code registry tests;
- create semantic-model dataclasses;
- write table/field symbol extraction;
- write relationship target resolution;
- write lookup path resolution;
- write view binding validation;
- write handler target validation;
- add `appgen lint --json` contract tests;
- add formatter idempotency tests.

Intermediate tasks:

- PBC catalog binding in semantic model;
- workflow graph extraction;
- graph output in Mermaid and JSON;
- migration diff detection;
- LSP completion and hover;
- code action application for missing operations and lookup directives.

Advanced tasks:

- safe rename across workspace;
- natural-language patch planner;
- visual designer round-trip engine;
- release evidence bundle verifier;
- cross-tool drift tests.

## Priority Order

1. Shared parser and semantic model.
2. Diagnostic registry and linter.
3. Formatter.
4. CLI JSON contracts.
5. Graph and explain tooling.
6. Language server.
7. VS Code and Monaco integration.
8. Migration planner.
9. Natural-language DSL diff planner.
10. Package and release verifiers.

The shared semantic model is the foundation. Without it, every tool will drift:
the linter, IDE, generator, language server, visual designers, and agents will
eventually disagree about what the language means.
