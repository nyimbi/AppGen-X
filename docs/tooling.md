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

`appgen.non-goal-policy-audit.v1` is embedded in `appgen.tooling-audit.v1` and
proves these guards with executable lint and planning evidence: secret literals
must emit `AGX0702` with an environment-binding fix, unsupported
backend/runtime/stream picker fields must emit policy diagnostics with a removal
fix, and natural-language prompts that try to bypass the DSL source of truth
or skip linting, semantic validation, or release evidence must be rejected
before any patch is produced. The policy audit reports case, passing-case,
diagnostic-code, fix, rejected-prompt, and zero-patch-rejection counts so these
non-goals remain measurable release gates rather than prose warnings.
It also reports required, observed, and missing picker field names plus
per-field removal evidence for `backend`, `runtime`, and `stream`; the aggregate
gate requires both missing picker lists to be empty, so three generic diagnostics
cannot hide a missing picker-family guard.
`appgen non-goals` exposes the same policy report directly. Text mode lists
each policy case and diagnostic codes; JSON mode emits
`appgen.non-goal-policy-audit.v1`.

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
`appgen.module-boundary-audit.v1` is the executable proof for this section. It
maps each documented responsibility boundary to concrete callable surfaces and
reports `boundary_count` and `callable_count` so release evidence captures the
observed surface area. It also reports passing-boundary, missing-boundary,
missing-callable, passing-core-runtime, and core-runtime-gap counts. It proves
the parser, semantic model, diagnostic catalog, and formatter can run as core
library services without starting Studio or a generated application.
`appgen module-boundaries` exposes the same proof directly in JSON or compact
text form, including boundary counts, callable counts, and core runtime gaps.

## Semantic Model Contract

The semantic model should be serializable to JSON and stable enough for CLI,
IDE, tests, and agents.
The top-level tooling audit also embeds `appgen.dsl-language-quality.v1`, which
combines `appgen.dsl-antlr-integrity.v1` and `appgen.dsl-keyword-budget.v1`.
That release gate proves `lang/appgen.g4`, the generated parser/lexer, required
enterprise grammar rules, the compact keyword budget, authoring aliases, and the
progressive learning path remain synchronized before semantic-model evidence is
accepted.

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
- `human_task`
- `timer`
- `compensation`
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
handlers, flow states, permissions, agent skills, and deployment units. The
semantic model reports `contract_counts` with required/present/missing top-level
field counts, symbol count, symbol-kind count, and diagnostic count; symbol
coverage reports required/detected/missing kind counts plus per-kind symbol
counts so shared-model release evidence can be reviewed without expanding the
full symbol table.

### Source Sets

Real applications are usually split across many `.appgen` files. The semantic
model therefore treats a file or directory as one source set and emits
`appgen.semantic-source-set.v1` inside the `source_set` field. Directory mode
loads every nested `.appgen` file in sorted order, parses the combined workspace
as one application, keeps `source_files` stable, and rewrites declaration
symbols back to the file that actually owns each app, table, view, flow, package,
agent, rule, deployment, or nested field declaration.

Source-set metadata includes:

- `source_mode`: `file` or `directory`;
- `file_count` and ordered `source_files`;
- per-file `appgen.semantic-file-report.v1` parse summaries;
- `source_file_symbol_counts`, so agents can tell which file owns each edit;
- `file_diagnostic_counts`, so CI can surface noisy files without reparsing the
  full JSON model.

The executable contract `appgen.semantic-source-set-cli-audit.v1` proves that a
directory workspace resolves cross-file table relationships, lookup paths,
database-backed form bindings, and workflow handlers into one
`appgen.semantic-model.v1` payload. The audit also proves text mode lists every
`source-file`, every `symbol-file`, the embedded
`appgen.semantic-source-set.v1` format, symbol coverage, and contract counts, so
external coding agents can operate without consuming the full JSON payload.
The source-set audit must cover a representative enterprise workspace, not only
CRUD files: app, table, view, flow, rule, LLM provider, agent, deployment, and
package declarations must all be discovered across separate files and each
symbol must point back to the file that owns it. Nested ownership is part of
the same contract: table fields, view sections, component bindings, handlers,
flow states, agent skills, permissions, and deployment units must resolve inside
their parent block and must not be claimed by another file that happens to reuse
the same token.

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

Workflow internals are first-class symbols. A flow with `human Review assigned
Accountant -> reviewed`, `timer reviewed "P2D" -> escalated`, and
`compensate posted -> ReverseInvoice` emits `human_task`, `timer`, and
`compensation` symbols owned by `flow.SubmitInvoice`, with source ranges scoped
to the owning flow block. Directory-mode semantic audits require those symbols
to point back to the workflow file, so large applications can split tables,
forms, rules, agents, and workflows across files without losing IDE navigation
or release evidence.

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

The diagnostic catalog publishes this required runtime shape as
`diagnostic_shape_fields`, publishes the registry row shape as `catalog_fields`,
and records `runtime_shape_enforced_by: appgen.diagnostic-fixture-audit.v1` so
tools can distinguish catalog completeness from fixture-level diagnostic JSON
validation. The catalog reports range, diagnostic, required-code,
covered-fixture-code, shape-field, catalog-field, catalog-shape-gap, and
missing-fixture counts. The fixture audit reports required, covered, and missing
code counts; fixture, passing-fixture, blocking-gap, shape-gap, severity-gap,
and report-format counts; and the exact report formats exercised by the
fixtures, so release evidence can prove diagnostic breadth without expanding
every fixture payload.

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
| `AGX0603` | error | Strict workflow human task assignee is not a declared role or agent. | Declare the participant or assign to an existing participant. |
| `AGX0604` | error | Strict workflow timer duration is not a recognizable ISO-8601 duration. | Use a duration such as `P2D`, `PT4H`, or `P1DT2H`. |
| `AGX0605` | error | Strict workflow compensation target is not a declared operation or flow. | Declare the compensation operation or target an existing flow. |
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
| `AGX9000` | error | Internal tooling error occurred. | Report traceback-free internal error evidence. |

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
`appgen.lint-report.v1` exposes these stages under `stages.syntax`,
`stages.semantic`, and `stages.policy`, with diagnostic counts, severity
counts, and codes for each lane. Every lint report also publishes
`stage_names: ["syntax", "semantic", "policy"]` and
`severity_names: ["error", "warning", "info", "hint"]` so CI, IDEs, and agents
can validate the report schema without hard-coding the prose specification.
Each report also carries top-level stage, severity, file, diagnostic, and fix
counts, plus `fixes_available`, so release evidence can prove report breadth
without expanding every diagnostic item.
`appgen.lint-directory-cli-audit.v1` proves that syntax errors, semantic
reference errors, and policy warnings are reported through distinct stage
buckets. It publishes named scenario ids, failing-scenario counts, named
failing scenarios, expected and observed exit codes by scenario, expected and
observed `appgen.lint-report.v1` payload formats by scenario, per-scenario `ok`
status, stage-profile ids, expected and observed stage-profile exit codes,
per-stage-profile `ok` status, passing/failing stage-profile counts, and
required/observed/missing stage and severity names so release evidence can show
which exact lint contract regressed without replaying the full CLI log.

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
`file_reports`. Without `--json`, directory lint also prints source mode and
discovered file count so CI and agent logs can distinguish directory source-set
linting from a single-file lint pass.
`--previous-semantic` loads a previous `appgen.semantic-model.v1` JSON payload
and attaches an `appgen.migration-plan.v1` migration preview to the lint report,
so CI, IDEs, and agents can see schema drift while they are already reviewing
semantic diagnostics. The lint CLI audit exercises this path through
`appgen.lint-directory-cli-audit.v1`, which reports `file_order_sorted` and
`file_relative_order` so release evidence proves deterministic recursive
discovery rather than only reporting a file count.
The same audit reports scenario, passing-scenario, and stage-profile counts so
release evidence proves strict component gating, catalog success, migration
preview, stage separation, warning diagnostics, and deterministic file ordering
were all exercised.
The aggregate tooling audit exposes this proof independently as
`lint_cli_directory_contracts`. That gate fails when strict mode, component
catalog allow-listing, deterministic directory discovery, file-scoped
diagnostics, previous-semantic migration previews, stage separation, or
human-readable lint markers regress. It also requires zero named missing entries
for scenario exit codes, payload formats, scenario `ok` status, stage-profile
exit codes, and stage-profile `ok` status, so a generic passing count cannot mask
a hidden CLI status, envelope, or stage-proof regression.

### Linter Outputs

Text mode is for humans. JSON mode is for CI, IDEs, agents, and generated apps.

```json
{
  "format": "appgen.lint-report.v1",
  "ok": false,
  "stage_names": ["syntax", "semantic", "policy"],
  "severity_names": ["error", "warning", "info", "hint"],
  "files": ["finance.appgen"],
  "stages": {
    "syntax": {"diagnostic_count": 0, "error": 0, "warning": 0, "codes": []},
    "semantic": {"diagnostic_count": 1, "error": 1, "warning": 0, "codes": ["AGX0402"]},
    "policy": {"diagnostic_count": 0, "error": 0, "warning": 0, "codes": []}
  },
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
directives. The formatter contract reports check, passing-check,
failed-check, comment-check, ordering-check, report, idempotent-report,
changed-report, diagnostic, diagnostic-error, diagnostic-severity, and output
byte counts so release evidence captures both formatting scenarios and the
breadth of formatter guarantees without hiding non-blocking lint hints.

## CLI Contracts

The installed command should expose current compatibility flags and the newer
subcommands below. `apg` is a supported short alias for the same command surface
as `appgen`. Existing flags may remain as aliases. The executable
`appgen.cli-help-surface-audit.v1` contract invokes top-level help, each
important subcommand help surface, and nested package/component-publish help so
new flags cannot be implemented without being discoverable by humans, scripts,
and coding agents. It also embeds `appgen.cli-alias-contract.v1`, which proves
that `appgen` and `apg` resolve to the same `pyAppGen.__main__:main` entrypoint
and that both the module entrypoint and the repo-local `./apg` command dispatch
into the tooling CLI. The audit also reports required/documented/listed
subcommand counts plus option-surface, required-option, missing-option, module
entrypoint, and repo-alias execution evidence, so release evidence can prove CLI
discoverability breadth without scraping nested help payloads.
The audit also emits missing documented-subcommand details, option help
exit-failure details, per-command missing-option details, command-alias counts,
entrypoint-dispatch counts, failing-entrypoint-dispatch counts, named
entrypoint ids, per-entrypoint dispatch booleans, expected and observed
per-entrypoint exit codes, expected and observed per-entrypoint payload formats,
per-entrypoint traceback-free status, failing-option-surface counts,
listed-subcommand counts, and top-level help byte counts. These detail lists
must be empty, `entrypoint_dispatch_count` must prove both module and repo-local
alias dispatch, `failing_entrypoint_dispatch_count` must be zero, every
entrypoint id must be observed, every entrypoint must exit with code `0`, every
entrypoint must emit `appgen.lint-report.v1`, every entrypoint must be
traceback-free, and
`passing_option_surface_count` must equal `subcommand_option_surface_count`,
before the CLI help surface is considered tooling-complete.
The same audit also runs a breadth matrix across the module entrypoint and
repo-local alias for `lint`, `contract-schema`, `contract-validate`, `lsp`, and
`agent-handoff`; every case must return the expected machine contract and no
traceback, which prevents newly added parser subcommands from existing only
behind one command path.
Top-level help, lightweight entrypoint dispatch, and the CLI audit use the
shared `TOOLING_SUBCOMMANDS` manifest so command names are not copied between
the launcher and release evidence.
`appgen.missing-required-option-exit-audit.v1` covers required command options,
including generator output directories, natural-language prompts, and component
publication names, plus the required `appgen explain` selector family
(`--symbol`, `--diagnostic`, or `--handler`).
`appgen.missing-input-exit-audit.v1`, `appgen.invalid-choice-exit-audit.v1`,
and `appgen.internal-error-exit-audit.v1` cover file-not-found, unsupported
choice, and controlled internal-error paths. These audits report case or mode
counts, passing counts, failing-case counts, exact case ids, failing-case ids,
expected-message counts, stdout-empty counts where required, command-family
coverage for missing inputs, and traceback-free counts so release evidence
proves failure behavior across the CLI surface instead of only recording exit
codes.
They also publish required, observed, and missing case ids; missing-input command
families and missing command-family names; cases missing the expected
`path does not exist`, required-option, or `invalid choice` messages; and the
expected required-option message family by case. The aggregate gate fails on any
missing named case, missing command family, missing expected message, or
traceback-bearing failure path.
The usage audits also publish named stdout, traceback, and unexpected-exit-code
case lists. All three lists must be empty for missing-input, missing-required-
option, and invalid-choice audits, so a usage failure cannot pass by writing a
partial payload to stdout, changing the expected exit code, or hiding a Python
traceback behind aggregate counts.
The aggregate tooling audit exposes those failure paths as a separate
`cli_usage_failure_contracts` gate. It reports internal-error mode counts,
missing-input case/stdout/traceback counts, missing-required-option case
counts, invalid-choice message counts, and help-surface discovery counts, and
it can fail independently from the validation/generation gate.
The CLI help and alias surface is also a separate
`cli_help_alias_contracts` gate. It fails independently when top-level help
omits a documented subcommand, a subcommand help page omits a required option,
`appgen` and `apg` stop sharing the same entrypoint, module execution via
`python -m pyAppGen` stops dispatching to tooling, or the repo-local `./apg`
command stops producing the same lint contract.
Governance commands are also direct CLI contracts: `appgen module-boundaries`
emits `appgen.module-boundary-audit.v1`, `appgen non-goals` emits
`appgen.non-goal-policy-audit.v1`, `appgen implementation-phases` emits
`appgen.tooling-implementation-phase-audit.v1`, and `appgen tooling-docs`
emits `appgen.tooling-docs-audit.v1` with embedded anchor and section coverage.
These commands keep architectural and documentation guardrails callable without
requiring contributors to expand the full aggregate audit.
Test strategy and roadmap commands are first-class CLI contracts:
`appgen test-strategy <file>` emits the same cross-tool strategy evidence used
by the aggregate audit, `appgen contributor-tasks` prints the evidence-backed
good-first/intermediate/advanced task list, and `appgen priority-order` prints
the dependency-ordered implementation roadmap. These commands exist so
contributors and coding agents do not have to run the full `tooling-audit`
payload just to decide what to build next or verify that a DSL file still
exercises the required strategy surface.
Coding-agent handoff is a direct CLI contract: `appgen agent-handoff` emits
`appgen.agent-handoff-report.v1` and is governed by
`appgen.agent-handoff-cli-audit.v1` so Claude Code, OpenAI Codex, OpenCode,
Ollama, vLLM, and API-key backed runners can receive launcher names, allowed
backends, required outputs, compact model briefs, token-budget notes, guardrails,
and the canonical AppGen-X command sequence without first creating an
`appgen.nl-plan.v1` patch. This makes external agents first-class development
vectors even when the user already knows the desired operation, and the audit
gate verifies both JSON and text handoffs for vector/backend filtering.
DSL language-quality commands are first-class CLI contracts: `appgen
dsl-quality`, `appgen dsl-antlr`, `appgen dsl-authoring-gate <file>`, and
`appgen dsl-language-service <file>` expose the same grammar, parser, keyword,
authoring, and editor-service evidence used by the aggregate tooling audit.
The package-level DSL authoring service also has schema-backed subcontracts for
quick-fix application, formatting, outline/navigation, code actions, authoring
score, ergonomics, experience, release gates, and the combined language-service
payload: `appgen.dsl-fix-result.v1`, `appgen.dsl-format-result.v1`,
`appgen.dsl-outline.v1`, `appgen.dsl-code-action.v1`,
`appgen.dsl-authoring-score.v1`,
`appgen.dsl-language-ergonomics.v1`,
`appgen.dsl-language-experience-gate.v1`,
`appgen.dsl-authoring-release-gate.v1`, and
`appgen.dsl-language-service.v1`. Editors and coding agents should validate
these direct payloads instead of relying on loosely shaped nested objects.
`appgen.dsl-language-cli-audit.v1` exercises those commands in JSON and text
modes, reports JSON/text case counts, payload formats, failing cases, and
completion counts. It also reports required, observed, and missing JSON/text
case ids; expected versus observed exit codes by case; case `ok` status by case;
expected versus observed payload formats by case; text exit codes by case;
required text markers by case; missing text markers; and text JSON-fallback
status by text case. The aggregate tooling audit blocks when agents or CI cannot
query the language-quality gate directly, when any expected command mode
disappears, when JSON payload formats drift, when text commands return the wrong
process status, when text output falls back to raw JSON, or when text logs lose
the markers external coding agents rely on.

### `appgen contract-schema`

```console
appgen contract-schema --json
appgen contract-schema appgen.semantic-model.v1 --json
appgen contract-schema
```

`appgen contract-schema` exports reusable JSON Schema documents for the core
machine contracts that agents, IDEs, CI jobs, and downstream package verifiers
consume. The command returns `appgen.contract-schema-catalog.v1`, using the
JSON Schema 2020-12 dialect, and includes schemas for `appgen.diagnostic.v1`,
`appgen.lint-report.v1`, `appgen.semantic-model.v1`,
`appgen.symbol-coverage.v1`, `appgen.semantic-source-set.v1`,
`appgen.semantic-file-report.v1`,
`appgen.semantic-source-set-cli-audit.v1`,
`appgen.module-boundary-audit.v1`, `appgen.non-goal-policy-audit.v1`,
`appgen.dsl-keyword-budget.v1`, `appgen.dsl-antlr-integrity.v1`,
`appgen.dsl-language-quality.v1`, `appgen.dsl-language-cli-audit.v1`,
`appgen.dsl-fix-result.v1`, `appgen.dsl-format-result.v1`,
`appgen.dsl-outline.v1`, `appgen.dsl-code-action.v1`,
`appgen.dsl-authoring-score.v1`,
`appgen.dsl-language-ergonomics.v1`,
`appgen.dsl-language-experience-gate.v1`,
`appgen.dsl-authoring-release-gate.v1`,
`appgen.dsl-language-service.v1`,
`appgen.format-result.v1`, `appgen.format-text-renderer.v1`,
`appgen.formatter-contract-audit.v1`, `appgen.format-write-audit.v1`,
`appgen.validate-report.v1`,
`appgen.generate-report.v1`, `appgen.validate-generate-text-renderer.v1`,
`appgen.validate-generate-cli-audit.v1`, `appgen.graph-report.v1`,
`appgen.graph.er.v1`, `appgen.graph.lookup.v1`,
`appgen.graph.workflow.v1`, `appgen.graph.handler.v1`,
`appgen.graph.pbc.v1`, `appgen.graph.security.v1`,
`appgen.graph.agent.v1`, `appgen.graph.deployment.v1`,
`appgen.graph.package.v1`, `appgen.graph-suite-report.v1`,
`appgen.graph-explain-text-renderer.v1`,
`appgen.graph-cli-format-audit.v1`,
`appgen.graph-suite-cli-audit.v1`, `appgen.explain-report.v1`,
`appgen.explain-cli-audit.v1`, `appgen.lsp-service.v1`,
`appgen.lsp-capabilities.v1`, `appgen.lsp-diagnostics.v1`,
`appgen.lsp-completion.v1`, `appgen.completion-coverage.v1`,
`appgen.lsp-hover.v1`, `appgen.lsp-definition.v1`,
`appgen.lsp-references.v1`, `appgen.lsp-document-symbols.v1`,
`appgen.lsp-workspace-symbols.v1`, `appgen.lsp-symbol-coverage.v1`,
`appgen.lsp-code-actions.v1`, `appgen.lsp-code-action-apply.v1`,
`appgen.lsp-code-action-apply-audit.v1`,
`appgen.lsp-code-action-cli-audit.v1`, `appgen.lsp-formatting.v1`,
`appgen.lsp-prepare-rename.v1`, `appgen.lsp-rename.v1`,
`appgen.lsp-rename-cli-audit.v1`,
`appgen.lsp-json-rpc-audit.v1`, `appgen.lsp-stdio-transport-audit.v1`,
`appgen.lsp-service-text-renderer.v1`, and
`appgen.lsp-code-action-text-renderer.v1`,
`appgen.internal-error.v1`, `appgen.internal-error-exit-audit.v1`,
`appgen.missing-input-exit-audit.v1`,
`appgen.missing-required-option-exit-audit.v1`,
`appgen.invalid-choice-exit-audit.v1`, `appgen.cli-alias-contract.v1`, and
`appgen.cli-help-surface-audit.v1`,
`appgen.designer-dsl-editor.v1`,
`appgen.designer-component-palette.v1`,
`appgen.designer-form-projection.v1`,
`appgen.designer-database-projection.v1`,
`appgen.designer-workflow-projection.v1`,
`appgen.designer-pbc-composition-projection.v1`,
`appgen.designer-package-deployment-projection.v1`,
`appgen.designer-graph-explain-panel.v1`,
`appgen.designer-nl-planner-panel.v1`,
`appgen.designer-sync-report.v1`,
`appgen.designer-sync-cli-audit.v1`,
`appgen.designer-visual-edit-result.v1`,
`appgen.designer-visual-transaction-result.v1`,
`appgen.designer-visual-edit-matrix.v1`,
`appgen.studio-semantic-service.v1`,
`appgen.studio-semantic-service-audit.v1`,
`appgen.studio-diagnostics-quick-fixes.v1`,
`appgen.studio-graph-explain.v1`,
`appgen.studio-natural-language-evolution.v1`,
`appgen.studio-browser-smoke-ci-contract.v1`,
`appgen.frontend-semantic-service-audit.v1`,
`appgen.frontend-dsl-editor-audit.v1`,
`appgen.frontend-data-service-catalog-audit.v1`,
`appgen.frontend-interaction-audit.v1`,
`appgen.vscode-extension-audit.v1`, diagnostic catalog, fixture audit, and
diagnostic text-renderer reports, parser-golden and parser-golden text-renderer
audits, semantic-drift and semantic-drift text-renderer audits,
`appgen.migration-plan.v1`,
`appgen.nl-plan.v1`, `appgen.release-verifier-report.v1`,
`appgen.release-evidence-file.v1`,
`appgen.package-invalid-target-audit.v1`,
`appgen.component-publish-cli-audit.v1`,
`appgen.component-publish-report.v1`, `appgen.doctor-report.v1`,
`appgen.tooling-audit.v1`, `appgen.contract-schema-catalog.v1`, and
`appgen.contract-validation-report.v1`,
`appgen.runtime-contract-inventory.v1`, and
`appgen.runtime-contract-inventory-cli-audit.v1`,
`appgen.tooling-doc-language-audit.v1`,
plus the package-level release audit family:
`appgen.package-dsl-release-audit.v1`,
`appgen.package-studio-release-audit.v1`,
`appgen.package-form-designer-release-audit.v1`,
`appgen.package-visual-modeling-release-audit.v1`,
`appgen.package-security-release-audit.v1`,
`appgen.package-source-intake-release-audit.v1`,
`appgen.package-config-editor-release-audit.v1`,
`appgen.package-distribution-release-audit.v1`,
`appgen.package-reporting-release-audit.v1`,
`appgen.package-ops-release-audit.v1`,
`appgen.package-integration-release-audit.v1`,
`appgen.package-agentic-release-audit.v1`,
`appgen.package-target-release-audit.v1`,
`appgen.nl-evolution-release-audit.v1`, and
`appgen.erp-template-release-audit.v1`,
plus the first-class agentic development-vector contracts:
`appgen.package-agentic-dsl-contract.v1`,
`appgen.package-agent-provider-matrix.v1`,
`appgen.package-agent-tool-policy.v1`,
`appgen.package-agent-execution-matrix.v1`,
`appgen.coding-agent-backend-matrix.v1`,
`appgen.coding-agent-development-workflow.v1`,
`appgen.coding-agent-release-gate.v1`,
`appgen.agent-handoff-report.v1`,
`appgen.agent-handoff-cli-audit.v1`, and
`appgen.agentic-generation-smoke-audit.v1`,
plus the Application Composition Platform and compact generation contracts:
`appgen.acp-stream-processing-policy.v1`,
`appgen.acp-event-processing-developer-guidance.v1`,
`appgen.acp-stream-processor-selection.v1`,
`appgen.acp-event-processing-choice-resolution.v1`,
`appgen.application-composition-topology.v1`,
`appgen.acp-capability-coverage.v1`,
`appgen.compact-generation-brief.v1`, and
`appgen.compact-full-app-generation-gate.v1`,
plus the top-level package support contracts:
`appgen.base-feature-document-check.v1`,
`appgen.base-feature-generation-smoke-audit.v1`,
`appgen.base-feature-release-audit.v1`,
`appgen.config-editor-generation-smoke-audit.v1`,
`appgen.package-config-editor-catalog.v1`,
`appgen.package-config-production-status.v1`,
`appgen.package-config-update.v1`,
`appgen.cookiecutter-template.v1`,
`appgen.distribution-generation-smoke-audit.v1`,
`appgen.fab-extension-package.v1`,
`appgen.generated-coverage-manifest.v1`,
`appgen.package-distribution-artifacts.v1`,
`appgen.seed-fixture.v1`,
`appgen.seed-script-manifest.v1`,
`appgen.generated-dsl-reference-smoke-audit.v1`,
`appgen.package-dsl-artifact-contract.v1`,
`appgen.package-dsl-linter-contract.v1`,
`appgen.erp-generation-smoke-audit.v1`,
`appgen.erp-starter.v1`,
`appgen.erp-template-catalog.v1`,
`appgen.ideas-document-check.v1`,
`appgen.ideas-generation-smoke-audit.v1`,
`appgen.ideas-release-audit.v1`,
`appgen.generated-app-excellence-audit.v1`,
`appgen.generated-app-excellence-smoke-audit.v1`,
`appgen.jhipster-superiority-audit.v1`,
`appgen.low-code-roadmap-generation-smoke-audit.v1`,
`appgen.package-goal-audit.v1`, and
`appgen.roadmap-release-audit.v1`,
plus the binding-designer runtime contracts:
`appgen.binding-accessibility-contract.v1`,
`appgen.binding-authoring-session.v1`,
`appgen.binding-bulk-edit-contract.v1`,
`appgen.binding-conflict-resolution-workflow.v1`,
`appgen.binding-conflict-validation-contract.v1`,
`appgen.binding-dataset-cursor-sync-contract.v1`,
`appgen.binding-dependency-execution-plan-contract.v1`,
`appgen.binding-design-runtime-session-replay-contract.v1`,
`appgen.binding-designer-family-contract.v1`,
`appgen.binding-designer-transaction-replay-contract.v1`,
`appgen.binding-diagnostics-contract.v1`,
`appgen.binding-edit-transaction-contract.v1`,
`appgen.binding-expression-editor-transaction-replay.v1`,
`appgen.binding-expression-sandbox-contract.v1`,
`appgen.binding-expression-validation.v1`,
`appgen.binding-graph-editing-surface-contract.v1`,
`appgen.binding-graph-json.v1`,
`appgen.binding-graph-validation-contract.v1`,
`appgen.binding-history-contract.v1`,
`appgen.binding-hit-testing-contract.v1`,
`appgen.binding-lifecycle-release-replay.v1`,
`appgen.binding-lookup-contract.v1`,
`appgen.binding-master-detail-contract.v1`,
`appgen.binding-offline-replay-contract.v1`,
`appgen.binding-pipeline-contract.v1`,
`appgen.binding-preview-evaluation-contract.v1`,
`appgen.binding-preview-runtime-parity-contract.v1`,
`appgen.binding-round-trip-contract.v1`,
`appgen.binding-runtime-failure-recovery-contract.v1`,
`appgen.binding-runtime-gate-contract.v1`,
`appgen.binding-runtime-propagation-replay-contract.v1`,
`appgen.binding-runtime-wiring-contract.v1`,
`appgen.binding-scope-context-contract.v1`, and
`appgen.binding-update-scheduler-contract.v1`,
plus the native Pascal/runtime workbench contracts:
`appgen.pascal-apply-property-delta-operation.v1`,
`appgen.pascal-compile-package-transaction-replay.v1`,
`appgen.pascal-compile-preview-operation.v1`,
`appgen.pascal-compiler-pipeline-contract.v1`,
`appgen.pascal-compiler-recovery-contract.v1`,
`appgen.pascal-component-inheritance-contract.v1`,
`appgen.pascal-debug-session-transaction-replay.v1`,
`appgen.pascal-debug-symbol-contract.v1`,
`appgen.pascal-debug-watch-transaction-replay.v1`,
`appgen.pascal-design-edit-session-replay-contract.v1`,
`appgen.pascal-diagnostic-mapping-contract.v1`,
`appgen.pascal-event-binding-contract.v1`,
`appgen.pascal-event-handler-wiring-contract.v1`,
`appgen.pascal-event-stub-evolution-contract.v1`,
`appgen.pascal-form-stream-schema-contract.v1`,
`appgen.pascal-incremental-compile-contract.v1`,
`appgen.pascal-incremental-invalidation-contract.v1`,
`appgen.pascal-language-frontend-contract.v1`,
`appgen.pascal-open-design-stream-operation.v1`,
`appgen.pascal-package-dependency-contract.v1`,
`appgen.pascal-package-target-matrix-contract.v1`,
`appgen.pascal-refresh-resources-operation.v1`,
`appgen.pascal-reload-runtime-preview-operation.v1`,
`appgen.pascal-resource-manifest-hash-contract.v1`,
`appgen.pascal-resource-round-trip-fidelity-contract.v1`,
`appgen.pascal-resource-streaming-contract.v1`,
`appgen.pascal-round-trip-stream-operation.v1`,
`appgen.pascal-rtti-contract.v1`,
`appgen.pascal-runtime-actionable-operations.v1`,
`appgen.pascal-runtime-artifact-parity-contract.v1`,
`appgen.pascal-runtime-authoring-replay-matrix.v1`,
`appgen.pascal-runtime-authoring-scenario-operation.v1`,
`appgen.pascal-runtime-debug-authoring-contract.v1`,
`appgen.pascal-runtime-lifecycle-contract.v1`,
`appgen.pascal-runtime-memory-model-contract.v1`,
`appgen.pascal-runtime-module-replay-matrix.v1`,
`appgen.pascal-runtime-readiness-contract.v1`,
`appgen.pascal-runtime-session-replay-contract.v1`,
`appgen.pascal-runtime-workbench.v1`,
`appgen.pascal-semantic-validation-contract.v1`,
`appgen.pascal-start-debug-preview-operation.v1`,
`appgen.pascal-static-analysis-contract.v1`,
`appgen.pascal-toolchain-adapter-contract.v1`,
`appgen.pascal-unit-contract.v1`, and
`appgen.pascal-unit-parse-contract.v1`,
plus the target packaging and native binary adapter contracts:
`appgen.package-desktop-target-contract.v1`,
`appgen.package-mobile-target-contract.v1`,
`appgen.package-target-dsl-contract.v1`,
`appgen.package-target-generation-smoke-audit.v1`,
`appgen.package-target-matrix.v1`,
`appgen.target-binary-adapter-ci-contract.v1`,
`appgen.target-binary-adapter-execution-audit.v1`,
`appgen.target-binary-adapter-transcript-schema.v1`,
`appgen.target-generated-runtime-smoke.v1`,
`appgen.target-package-artifact-audit.v1`,
`appgen.target-packager-execution-preflight.v1`, and
`appgen.target-runtime-packaging-proof.v1`,
plus visual database/modeling contracts:
`appgen.migration-preview.v1`,
`appgen.package-visual-code-generation-plan.v1`,
`appgen.package-visual-field-proposal.v1`,
`appgen.package-visual-graph.v1`,
`appgen.package-visual-migration-preview.v1`,
`appgen.package-visual-model-exports.v1`,
`appgen.package-visual-relationship-proposal.v1`,
`appgen.package-visual-schema.v1`,
`appgen.package-visual-table-proposal.v1`, and
`appgen.visual-modeling-generation-smoke-audit.v1`,
plus generated application foundation contracts:
`appgen.api-security-test-plan.v1`,
`appgen.dependency-security-plan.v1`,
`appgen.health-release-gate.v1`,
`appgen.health-summary.v1`,
`appgen.secret-exposure-scan.v1`,
`appgen.security-gate-plan.v1`,
`appgen.security-signoff.v1`,
`appgen.security-threat-model.v1`,
`appgen.security-workbench.v1`,
`appgen.workflow-approval-route.v1`,
`appgen.workflow-audit-event.v1`,
`appgen.workflow-authorization-flow.v1`,
`appgen.workflow-authorization.v1`,
`appgen.workflow-release-gate.v1`,
`appgen.workflow-sla.v1`,
`appgen.workflow-transition-authorization.v1`,
`appgen.workflow-transition-runbook.v1`, and
`appgen.workflow-workbench.v1`,
plus generated module contract schemas:
`appgen.native-form-module-contract.v1`,
`appgen.native-form-module-manifest.v1`,
`appgen.native-form-module-operation.v1`,
`appgen.native-form-module-operation-steps.v1`,
`appgen.native-form-module-validation-steps.v1`,
`appgen.native-form-module-smoke-test.v1`,
`appgen.native-form-module-generated-test-smoke.v1`,
`appgen.runtime-operation-module-contract.v1`,
`appgen.runtime-operation-module-manifest.v1`,
`appgen.runtime-operation-module-result.v1`,
`appgen.runtime-operation-module-operation-steps.v1`,
`appgen.runtime-operation-module-validation-steps.v1`,
`appgen.runtime-operation-module-smoke-test.v1`,
`appgen.runtime-operation-module-generated-test-smoke.v1`,
`appgen.compiler-runtime-module-contract.v1`,
`appgen.compiler-runtime-module-manifest.v1`,
`appgen.compiler-runtime-module-result.v1`,
`appgen.compiler-runtime-module-operation-steps.v1`,
`appgen.compiler-runtime-module-validation-steps.v1`,
`appgen.compiler-runtime-module-smoke-test.v1`,
`appgen.compiler-runtime-module-generated-test-smoke.v1`,
`appgen.deep-runtime-module-contract.v1`,
`appgen.deep-runtime-module-manifest.v1`,
`appgen.deep-runtime-module-result.v1`,
`appgen.deep-runtime-module-operation-steps.v1`,
`appgen.deep-runtime-module-validation-steps.v1`,
`appgen.deep-runtime-module-smoke-test.v1`,
`appgen.deep-runtime-module-generated-test-smoke.v1`,
`appgen.ui-chrome-module-contract.v1`,
`appgen.ui-chrome-module-operation.v1`,
`appgen.ui-chrome-module-runtime-manifest.v1`,
`appgen.ui-chrome-module-operation-steps.v1`,
`appgen.ui-chrome-module-validation-steps.v1`,
`appgen.ui-chrome-module-smoke-test.v1`,
`appgen.ui-chrome-module-generated-test-smoke.v1`,
`appgen.wizard-module-contract.v1`,
`appgen.wizard-module-manifest.v1`,
`appgen.wizard-module-operation.v1`,
`appgen.wizard-module-operation-steps.v1`,
`appgen.wizard-module-validation-steps.v1`,
`appgen.wizard-module-release-context.v1`,
`appgen.wizard-module-smoke-test.v1`,
`appgen.wizard-module-generated-test-smoke.v1`,
`appgen.database-ops-module-contract.v1`,
`appgen.database-ops-module-manifest.v1`,
`appgen.database-ops-module-operation.v1`,
`appgen.database-ops-module-release-context.v1`,
`appgen.database-ops-module-operation-steps.v1`,
`appgen.database-ops-module-validation-steps.v1`,
`appgen.database-ops-module-smoke-test.v1`,
`appgen.database-ops-module-generated-test-smoke.v1`,
`appgen.data-access-module-contract.v1`,
`appgen.data-access-module-manifest.v1`,
`appgen.data-access-module-operation.v1`,
`appgen.data-access-module-release-context.v1`,
`appgen.data-access-module-operation-steps.v1`,
`appgen.data-access-module-validation-steps.v1`,
`appgen.data-access-module-smoke-test.v1`,
`appgen.data-access-module-generated-test-smoke.v1`,
`appgen.data-exchange-module-contract.v1`,
`appgen.data-exchange-module-manifest.v1`,
`appgen.data-exchange-module-operation.v1`,
`appgen.data-exchange-module-release-context.v1`,
`appgen.data-exchange-module-operation-steps.v1`,
`appgen.data-exchange-module-validation-steps.v1`,
`appgen.data-exchange-module-smoke-test.v1`,
`appgen.data-exchange-module-generated-test-smoke.v1`,
`appgen.schema-import-module-contract.v1`,
`appgen.schema-import-module-manifest.v1`,
`appgen.schema-import-module-operation.v1`,
`appgen.schema-import-module-release-context.v1`,
`appgen.schema-import-module-smoke-test.v1`,
`appgen.schema-import-module-generated-test-smoke.v1`,
`appgen.backup-module-contract.v1`,
`appgen.backup-module-manifest.v1`,
`appgen.backup-module-operation.v1`,
`appgen.backup-module-release-context.v1`,
`appgen.backup-module-smoke-test.v1`,
`appgen.backup-module-generated-test-smoke.v1`,
`appgen.seed-module-contract.v1`,
`appgen.seed-module-manifest.v1`,
`appgen.seed-module-operation.v1`,
`appgen.seed-module-release-context.v1`,
`appgen.seed-module-smoke-test.v1`,
`appgen.seed-module-generated-test-smoke.v1`,
`appgen.integration-module-contract.v1`,
`appgen.integration-module-manifest.v1`,
`appgen.integration-module-operation.v1`,
`appgen.integration-module-release-context.v1`,
`appgen.integration-module-smoke-test.v1`,
`appgen.integration-module-generated-test-smoke.v1`,
`appgen.productivity-module-contract.v1`,
`appgen.productivity-module-manifest.v1`,
`appgen.productivity-module-operation.v1`,
`appgen.productivity-module-release-context.v1`,
`appgen.productivity-module-smoke-test.v1`,
`appgen.productivity-module-generated-test-smoke.v1`,
`appgen.lifecycle-module-contract.v1`,
`appgen.lifecycle-module-manifest.v1`,
`appgen.lifecycle-module-operation.v1`,
`appgen.lifecycle-module-release-context.v1`,
`appgen.lifecycle-module-smoke-test.v1`,
`appgen.lifecycle-module-generated-test-smoke.v1`,
`appgen.emerging-module-contract.v1`,
`appgen.emerging-module-manifest.v1`,
`appgen.emerging-module-operation.v1`,
`appgen.emerging-module-release-context.v1`,
`appgen.emerging-module-smoke-test.v1`,
`appgen.emerging-module-generated-test-smoke.v1`,
`appgen.platform-module-contract.v1`,
`appgen.platform-module-manifest.v1`,
`appgen.platform-module-operation.v1`,
`appgen.platform-module-release-context.v1`,
`appgen.platform-module-smoke-test.v1`,
`appgen.platform-module-generated-test-smoke.v1`,
`appgen.pwa-module-contract.v1`,
`appgen.pwa-module-manifest.v1`,
`appgen.pwa-module-operation.v1`,
`appgen.pwa-module-release-context.v1`,
`appgen.pwa-module-smoke-test.v1`,
`appgen.pwa-module-generated-test-smoke.v1`,
`appgen.microservice-module-contract.v1`,
`appgen.microservice-module-manifest.v1`,
`appgen.microservice-module-operation.v1`,
`appgen.microservice-module-release-context.v1`,
`appgen.microservice-module-smoke-test.v1`,
`appgen.microservice-module-generated-test-smoke.v1`,
`appgen.realtime-module-contract.v1`,
`appgen.realtime-module-manifest.v1`,
`appgen.realtime-module-operation.v1`,
`appgen.realtime-module-release-context.v1`,
`appgen.realtime-module-smoke-test.v1`,
`appgen.realtime-module-generated-test-smoke.v1`,
`appgen.event-module-contract.v1`,
`appgen.event-module-manifest.v1`,
`appgen.event-module-operation.v1`,
`appgen.event-module-release-context.v1`,
`appgen.event-module-smoke-test.v1`,
`appgen.event-module-generated-test-smoke.v1`,
`appgen.rpa-module-contract.v1`,
`appgen.rpa-module-manifest.v1`,
`appgen.rpa-module-operation.v1`,
`appgen.rpa-module-release-context.v1`,
`appgen.rpa-module-smoke-test.v1`,
`appgen.rpa-module-generated-test-smoke.v1`,
`appgen.diagnostics-module-contract.v1`,
`appgen.diagnostics-module-manifest.v1`,
`appgen.diagnostics-module-operation.v1`,
`appgen.diagnostics-module-release-context.v1`,
`appgen.diagnostics-module-smoke-test.v1`,
`appgen.diagnostics-module-generated-test-smoke.v1`,
`appgen.api-testing-module-contract.v1`,
`appgen.api-testing-module-manifest.v1`,
`appgen.api-testing-module-operation.v1`,
`appgen.api-testing-module-release-context.v1`,
`appgen.api-testing-module-smoke-test.v1`,
`appgen.api-testing-module-generated-test-smoke.v1`,
`appgen.code-review-module-contract.v1`,
`appgen.code-review-module-manifest.v1`,
`appgen.code-review-module-operation.v1`,
`appgen.code-review-module-release-context.v1`,
`appgen.code-review-module-smoke-test.v1`,
`appgen.code-review-module-generated-test-smoke.v1`,
`appgen.collaboration-module-contract.v1`,
`appgen.collaboration-module-manifest.v1`,
`appgen.collaboration-module-operation.v1`,
`appgen.collaboration-module-release-context.v1`,
`appgen.collaboration-module-smoke-test.v1`,
`appgen.collaboration-module-generated-test-smoke.v1`,
`appgen.devtools-module-contract.v1`,
`appgen.devtools-module-manifest.v1`,
`appgen.devtools-module-operation.v1`,
`appgen.devtools-module-operation-steps.v1`,
`appgen.devtools-module-validation-steps.v1`,
`appgen.devtools-module-release-context.v1`,
`appgen.devtools-module-smoke-test.v1`, and
`appgen.devtools-module-generated-test-smoke.v1`,
plus generated IDE/productivity module schemas:
`appgen.project-management-module-contract.v1`,
`appgen.project-management-module-manifest.v1`,
`appgen.project-management-module-operation.v1`,
`appgen.project-management-module-release-context.v1`,
`appgen.project-management-module-smoke-test.v1`,
`appgen.project-management-module-generated-test-smoke.v1`,
`appgen.erp-template-module-contract.v1`,
`appgen.erp-template-module-manifest.v1`,
`appgen.erp-template-module-operation.v1`,
`appgen.erp-template-module-release-context.v1`,
`appgen.erp-template-module-smoke-test.v1`,
`appgen.erp-template-module-generated-test-smoke.v1`,
`appgen.version-control-module-contract.v1`,
`appgen.version-control-module-manifest.v1`,
`appgen.version-control-module-operation.v1`,
`appgen.version-control-module-operation-steps.v1`,
`appgen.version-control-module-validation-steps.v1`,
`appgen.version-control-module-release-context.v1`,
`appgen.version-control-module-smoke-test.v1`,
`appgen.version-control-module-generated-test-smoke.v1`,
`appgen.package-manager-module-contract.v1`,
`appgen.package-manager-module-manifest.v1`,
`appgen.package-manager-module-operation.v1`,
`appgen.package-manager-module-operation-steps.v1`,
`appgen.package-manager-module-validation-steps.v1`,
`appgen.package-manager-module-smoke-test.v1`,
`appgen.package-manager-module-generated-test-smoke.v1`,
`appgen.binding-module-contract.v1`,
`appgen.binding-module-manifest.v1`,
`appgen.binding-module-operation.v1`,
`appgen.binding-module-operation-steps.v1`,
`appgen.binding-module-validation-steps.v1`,
`appgen.binding-module-smoke-test.v1`,
`appgen.binding-module-generated-test-smoke.v1`,
`appgen.binding-designer-family-module-contract.v1`,
`appgen.binding-designer-family-module-manifest.v1`,
`appgen.binding-designer-family-module-operation.v1`,
`appgen.binding-designer-family-module-operation-steps.v1`,
`appgen.binding-designer-family-module-validation-steps.v1`,
`appgen.binding-designer-family-module-smoke-test.v1`,
`appgen.binding-designer-family-module-generated-test-smoke.v1`,
`appgen.component-wiring-module-contract.v1`,
`appgen.component-wiring-module-manifest.v1`,
`appgen.component-wiring-module-operation.v1`,
`appgen.component-wiring-module-operation-steps.v1`,
`appgen.component-wiring-module-validation-steps.v1`,
`appgen.component-wiring-module-smoke-test.v1`,
`appgen.component-wiring-module-generated-test-smoke.v1`,
`appgen.form-interaction-family-module-contract.v1`,
`appgen.form-interaction-family-module-manifest.v1`,
`appgen.form-interaction-family-module-operation-steps.v1`,
`appgen.form-interaction-family-module-validation-steps.v1`,
`appgen.form-interaction-family-module-smoke-test.v1`,
`appgen.form-interaction-family-module-generated-test-smoke.v1`,
`appgen.handler-architecture-module-contract.v1`,
`appgen.handler-architecture-module-manifest.v1`,
`appgen.handler-architecture-module-operation-steps.v1`,
`appgen.handler-architecture-module-validation-steps.v1`,
`appgen.handler-architecture-module-smoke-test.v1`,
`appgen.handler-architecture-module-generated-test-smoke.v1`,
`appgen.handler-source-ide-module-contract.v1`,
`appgen.handler-source-ide-module-manifest.v1`,
`appgen.handler-source-ide-module-operation.v1`,
`appgen.handler-source-ide-module-operation-steps.v1`,
`appgen.handler-source-ide-module-validation-steps.v1`,
`appgen.handler-source-ide-module-smoke-test.v1`,
`appgen.handler-source-ide-module-generated-test-smoke.v1`,
`appgen.property-editor-family-module-contract.v1`,
`appgen.property-editor-family-module-manifest.v1`,
`appgen.property-editor-family-module-operation.v1`,
`appgen.property-editor-family-module-operation-steps.v1`,
`appgen.property-editor-family-module-validation-steps.v1`,
`appgen.property-editor-family-module-smoke-test.v1`,
`appgen.property-editor-family-module-generated-test-smoke.v1`,
`appgen.event-editor-family-module-contract.v1`,
`appgen.event-editor-family-module-manifest.v1`,
`appgen.event-editor-family-module-operation.v1`,
`appgen.event-editor-family-module-operation-steps.v1`,
`appgen.event-editor-family-module-validation-steps.v1`,
`appgen.event-editor-family-module-smoke-test.v1`,
`appgen.event-editor-family-module-generated-test-smoke.v1`,
`appgen.component-editor-family-module-contract.v1`,
`appgen.component-editor-family-module-manifest.v1`,
`appgen.component-editor-family-module-operation.v1`,
`appgen.component-editor-family-module-operation-steps.v1`,
`appgen.component-editor-family-module-validation-steps.v1`,
`appgen.component-editor-family-module-smoke-test.v1`,
`appgen.component-editor-family-module-generated-test-smoke.v1`,
`appgen.custom-designer-family-module-contract.v1`,
`appgen.custom-designer-family-module-manifest.v1`,
`appgen.custom-designer-family-module-operation.v1`,
`appgen.custom-designer-family-module-operation-steps.v1`,
`appgen.custom-designer-family-module-validation-steps.v1`,
`appgen.custom-designer-family-module-smoke-test.v1`,
`appgen.custom-designer-family-module-generated-test-smoke.v1`,
`appgen.inspector-module-contract.v1`,
`appgen.inspector-module-editor-manifest.v1`,
`appgen.inspector-module-operation.v1`,
`appgen.inspector-module-operation-steps.v1`,
`appgen.inspector-module-validation-steps.v1`,
`appgen.inspector-module-smoke-test.v1`,
`appgen.inspector-module-generated-test-smoke.v1`,
`appgen.data-tooling-module-contract.v1`,
`appgen.data-tooling-module-smoke-plan.v1`,
`appgen.data-tooling-module-read-only-probe.v1`,
`appgen.data-tooling-module-operation-steps.v1`,
`appgen.data-tooling-module-validation-steps.v1`,
`appgen.data-tooling-module-smoke-test.v1`,
`appgen.data-tooling-module-generated-test-smoke.v1`,
`appgen.deep-data-tooling-module-contract.v1`,
`appgen.deep-data-tooling-module-smoke-test.v1`,
`appgen.deep-data-tooling-module-generated-test-smoke.v1`,
`appgen.enterprise-data-ide-module-contract.v1`,
`appgen.enterprise-data-ide-module-smoke-test.v1`,
`appgen.enterprise-data-ide-module-generated-test-smoke.v1`,
`appgen.visual-design-ide-module-contract.v1`,
`appgen.visual-design-ide-module-smoke-test.v1`,
`appgen.visual-design-ide-module-generated-test-smoke.v1`,
`appgen.visual-runtime-pipeline-module-contract.v1`, and
`appgen.visual-runtime-pipeline-module-smoke-test.v1`, plus generated runtime and module
manifest schemas:
`appgen.visual-runtime-pipeline-module-generated-test-smoke.v1`,
`appgen.component-family-module-contract.v1`,
`appgen.component-family-module-smoke-test.v1`,
`appgen.component-family-module-generated-test-smoke.v1`,
`appgen.component-module-smoke-test.v1`,
`appgen.component-package-module-operation-steps.v1`,
`appgen.component-package-module-validation-steps.v1`,
`appgen.component-package-module-smoke-test.v1`,
`appgen.generated-visual-component-module-manifest.v1`,
`appgen.generated-visual-component-test-module-manifest.v1`,
`appgen.generated-visual-design-ide-module-manifest.v1`,
`appgen.generated-visual-design-ide-test-module-manifest.v1`,
`appgen.generated-visual-runtime-pipeline-module-manifest.v1`,
`appgen.generated-visual-runtime-pipeline-test-module-manifest.v1`,
`appgen.generated-data-tooling-module-file-manifest.v1`,
`appgen.generated-data-tooling-module-test-file-manifest.v1`,
`appgen.generated-deep-data-tooling-module-file-manifest.v1`,
`appgen.generated-deep-data-tooling-module-test-file-manifest.v1`,
`appgen.generated-enterprise-data-ide-module-file-manifest.v1`,
`appgen.generated-enterprise-data-ide-module-test-file-manifest.v1`,
`appgen.generated-data-tooling-module-runtime-replay-matrix.v1`,
`appgen.generated-data-module-runtime-manifest.v1`,
`appgen.generated-binding-module-file-manifest.v1`,
`appgen.generated-binding-module-test-file-manifest.v1`,
`appgen.generated-binding-module-runtime-replay-matrix.v1`,
`appgen.generated-package-manager-module-file-manifest.v1`,
`appgen.generated-package-manager-module-test-file-manifest.v1`,
`appgen.generated-package-manager-module-runtime-replay-matrix.v1`,
`appgen.generated-inspector-module-file-manifest.v1`,
`appgen.generated-inspector-module-test-file-manifest.v1`,
`appgen.generated-inspector-module-runtime-replay-matrix.v1`,
`appgen.generated-native-form-module-file-manifest.v1`,
`appgen.generated-native-form-module-test-file-manifest.v1`,
`appgen.generated-runtime-operation-module-file-manifest.v1`,
`appgen.generated-runtime-operation-module-test-file-manifest.v1`,
`appgen.generated-compiler-runtime-module-file-manifest.v1`,
`appgen.generated-compiler-runtime-module-test-file-manifest.v1`,
`appgen.generated-deep-runtime-module-file-manifest.v1`,
`appgen.generated-deep-runtime-module-test-file-manifest.v1`,
`appgen.generated-native-runtime-module-replay-matrix.v1`,
`appgen.generated-device-api-component-module-manifest.v1`,
`appgen.generated-device-api-component-test-module-manifest.v1`,
`appgen.designer-module-contract.v1`,
`appgen.designer-module-manifest.v1`,
`appgen.designer-module-operation.v1`,
`appgen.designer-module-release-context.v1`,
`appgen.designer-module-smoke-test.v1`,
`appgen.designer-module-generated-test-smoke.v1`,
`appgen.designer-module-file-manifest.v1`,
`appgen.designer-module-test-file-manifest.v1`,
`appgen.generated-ui-chrome-module-file-manifest.v1`,
`appgen.generated-ui-chrome-module-test-file-manifest.v1`,
`appgen.extension-module-contract.v1`,
`appgen.extension-module-manifest.v1`,
`appgen.extension-module-operation.v1`,
`appgen.extension-module-release-context.v1`,
`appgen.extension-module-smoke-test.v1`,
`appgen.extension-module-generated-test-smoke.v1`,
`appgen.extension-module-file-manifest.v1`,
`appgen.extension-module-test-file-manifest.v1`,
`appgen.seed-module-file-manifest.v1`,
`appgen.seed-module-test-file-manifest.v1`,
`appgen.generated-backup-module-file-manifest.v1`,
`appgen.generated-backup-module-test-file-manifest.v1`,
`appgen.generated-data-access-module-file-manifest.v1`,
`appgen.generated-data-access-module-test-file-manifest.v1`,
`appgen.generated-schema-import-module-file-manifest.v1`,
`appgen.generated-schema-import-module-test-file-manifest.v1`,
`appgen.generated-database-ops-module-file-manifest.v1`,
`appgen.generated-database-ops-module-test-file-manifest.v1`,
`appgen.generated-data-exchange-module-file-manifest.v1`,
`appgen.generated-data-exchange-module-test-file-manifest.v1`,
`appgen.integration-module-file-manifest.v1`,
`appgen.integration-module-test-file-manifest.v1`,
`appgen.productivity-module-file-manifest.v1`,
`appgen.productivity-module-test-file-manifest.v1`,
`appgen.lifecycle-module-file-manifest.v1`,
`appgen.lifecycle-module-test-file-manifest.v1`,
`appgen.emerging-module-file-manifest.v1`,
`appgen.emerging-module-test-file-manifest.v1`,
`appgen.voice-module-contract.v1`,
`appgen.voice-module-manifest.v1`,
`appgen.voice-module-operation.v1`,
`appgen.voice-module-release-context.v1`,
`appgen.voice-module-smoke-test.v1`,
`appgen.voice-module-generated-test-smoke.v1`,
`appgen.voice-module-file-manifest.v1`,
`appgen.voice-module-test-file-manifest.v1`,
`appgen.text-quality-module-contract.v1`,
`appgen.text-quality-module-manifest.v1`,
`appgen.text-quality-module-operation.v1`,
`appgen.text-quality-module-release-context.v1`,
`appgen.text-quality-module-smoke-test.v1`,
`appgen.text-quality-module-generated-test-smoke.v1`,
`appgen.text-quality-module-file-manifest.v1`,
`appgen.text-quality-module-test-file-manifest.v1`,
`appgen.notification-module-contract.v1`,
`appgen.notification-module-manifest.v1`,
`appgen.notification-module-operation.v1`,
`appgen.notification-module-release-context.v1`,
`appgen.notification-module-smoke-test.v1`,
`appgen.notification-module-generated-test-smoke.v1`,
`appgen.notification-module-file-manifest.v1`,
`appgen.notification-module-test-file-manifest.v1`,
`appgen.agentic-module-contract.v1`,
`appgen.agentic-module-manifest.v1`,
`appgen.agentic-module-operation.v1`,
`appgen.agentic-module-release-context.v1`,
`appgen.agentic-module-smoke-test.v1`,
`appgen.agentic-module-generated-test-smoke.v1`,
`appgen.agentic-module-file-manifest.v1`,
`appgen.agentic-module-test-file-manifest.v1`,
`appgen.view-composition-module-contract.v1`,
`appgen.view-composition-module-manifest.v1`,
`appgen.view-composition-module-operation.v1`,
`appgen.view-composition-module-release-context.v1`,
`appgen.view-composition-module-operation-steps.v1`,
`appgen.view-composition-module-validation-steps.v1`,
`appgen.view-composition-module-smoke-test.v1`, and
`appgen.view-composition-module-generated-test-smoke.v1`, plus application/component
runtime schemas:
`appgen.accessibility-audit.v1`,
`appgen.accessibility-workbench.v1`,
`appgen.agent-execution-matrix.v1`,
`appgen.agent-provider-matrix.v1`,
`appgen.agent-tool-policy.v1`,
`appgen.agentic-release-gate.v1`,
`appgen.agentic-workbench.v1`,
`appgen.api-test-fixture-strategy.v1`,
`appgen.api-testing-module-file-manifest.v1`,
`appgen.api-testing-module-test-file-manifest.v1`,
`appgen.api-testing-release-gate.v1`,
`appgen.api-testing-workbench.v1`,
`appgen.app-shell-chrome-contract.v1`,
`appgen.app-shell-chrome-transaction-replay.v1`,
`appgen.application-creation-plan.v1`,
`appgen.application-diff-plan.v1`,
`appgen.application-export-package.v1`,
`appgen.application-import-plan.v1`,
`appgen.application-open-plan.v1`,
`appgen.application-portfolio-check.v1`,
`appgen.application-registry.v1`,
`appgen.application-release-gate.v1`,
`appgen.application-restore-plan.v1`,
`appgen.application-snapshot-plan.v1`,
`appgen.application-version-history.v1`,
`appgen.assistant-check.v1`,
`appgen.assistant-release-gate.v1`,
`appgen.assistant-workbench.v1`,
`appgen.backup-release-gate.v1`,
`appgen.backup-workbench.v1`,
`appgen.backup.manifest.v1`,
`appgen.backup.v1`,
`appgen.branding-workbench.v1`,
`appgen.caddy-proxy-contract.v1`,
`appgen.chatbot-provider-export-matrix.v1`,
`appgen.chatbot-provider-release-gate.v1`,
`appgen.chatbot-release-gate.v1`,
`appgen.ci-pipeline-contract.v1`,
`appgen.ci-release-gate.v1`,
`appgen.code-review-module-file-manifest.v1`,
`appgen.code-review-module-test-file-manifest.v1`,
`appgen.code-review-release-gate.v1`,
`appgen.code-review-workbench.v1`,
`appgen.collaboration-conflicts.v1`,
`appgen.collaboration-module-file-manifest.v1`,
`appgen.collaboration-module-test-file-manifest.v1`,
`appgen.collaboration-release-gate.v1`,
`appgen.collaboration-workbench.v1`,
`appgen.compliance-release-gate.v1`,
`appgen.compliance-workbench.v1`,
`appgen.component-analog-group-audit.v1`,
`appgen.component-analog-workbench.v1`,
`appgen.component-behavior-contract.v1`,
`appgen.component-behavior-workbench.v1`,
`appgen.component-binding-surface-contract.v1`,
`appgen.component-capability-contract.v1`,
`appgen.component-design-surface-contract.v1`,
`appgen.component-designer-metadata-contract.v1`,
`appgen.component-drag-payload.v1`,
`appgen.component-drag-start-operation.v1`,
`appgen.component-drop-commit-operation.v1`,
`appgen.component-drop-instance.v1`,
`appgen.component-drop-preview-operation.v1`,
`appgen.component-drop-wiring-handler-contract.v1`,
`appgen.component-editor-execution-contract.v1`,
`appgen.component-editor-family-contract.v1`,
`appgen.component-event-binding-operation.v1`,
`appgen.component-event-dispatch-contract.v1`,
`appgen.component-event-dispatch-result.v1`,
`appgen.component-family-manifest.v1`,
`appgen.component-family-operation-steps.v1`,
`appgen.component-family-readiness-context.v1`,
`appgen.component-family-replay.v1`,
`appgen.component-family-runtime-replay-matrix.v1`,
`appgen.component-family-validation-steps.v1`,
`appgen.component-generated-test-smoke.v1`,
`appgen.component-handler-definition-operation.v1`,
`appgen.component-ide-readiness-catalog.v1`,
`appgen.component-instance-json.v1`,
`appgen.component-module-contract.v1`,
`appgen.component-module-file-manifest.v1`,
`appgen.component-module-generated-test-smoke.v1`,
`appgen.component-module-implementation-contract.v1`,
`appgen.component-module-manifest.v1`,
`appgen.component-module-operation-steps.v1`,
`appgen.component-module-operation.v1`,
`appgen.component-module-release-context.v1`,
`appgen.component-module-replay-matrix.v1`,
`appgen.component-module-test-file-manifest.v1`,
`appgen.component-module-validation-steps.v1`,
`appgen.component-package-actionable-operations.v1`,
`appgen.component-package-adapter-smoke-contract.v1`,
`appgen.component-package-behavior-contract.v1`,
`appgen.component-package-behavior-workbench.v1`,
`appgen.component-package-compatibility-smoke-suite.v1`,
`appgen.component-package-contract.v1`,
`appgen.component-package-dependency-conflict-transaction-replay.v1`,
`appgen.component-package-dependency-graph.v1`,
`appgen.component-package-dependency-order-contract.v1`,
`appgen.component-package-failure-isolation-contract.v1`,
`appgen.component-package-generated-test-smoke.v1`,
`appgen.component-package-hot-reload-transaction-replay.v1`,
`appgen.component-package-icon-asset-transaction-replay.v1`,
`appgen.component-package-install-session-replay.v1`,
`appgen.component-package-installation-scenario-operation.v1`,
`appgen.component-package-lifecycle-execution.v1`,
`appgen.component-package-lifecycle-transaction-replay.v1`,
`appgen.component-package-load-policy.v1`,
`appgen.component-package-load-validation.v1`,
`appgen.component-package-lockfile-integrity-contract.v1`,
`appgen.component-package-marketplace-publication-contract.v1`,
`appgen.component-package-module-implementation-contract.v1`,
`appgen.component-package-palette-refresh-contract.v1`,
`appgen.component-package-preview-load-contract.v1`,
`appgen.component-package-preview-load-operation.v1`,
`appgen.component-package-readiness-contract.v1`,
`appgen.component-package-registration-consistency-contract.v1`,
`appgen.component-package-registry-commit-operation.v1`,
`appgen.component-package-resolve-metadata-operation.v1`,
`appgen.component-package-rollback-contract.v1`,
`appgen.component-package-sandbox-policy-contract.v1`,
`appgen.component-package-signature-validation.v1`,
`appgen.component-package-test-plan.v1`,
`appgen.component-package-uninstall-operation.v1`,
`appgen.component-package-uninstall-plan-contract.v1`,
`appgen.component-package-update-operation.v1`,
`appgen.component-package-update-plan-contract.v1`,
`appgen.component-package-version-conflict-contract.v1`,
`appgen.component-package-workbench.v1`,
`appgen.component-palette-registration-contract.v1`,
`appgen.component-parity-readiness-contract.v1`,
`appgen.component-parity-scenario-operation.v1`,
`appgen.component-prop-validation-contract.v1`,
`appgen.component-prop-validation.v1`,
`appgen.component-property-apply-result.v1`,
`appgen.component-release-gate.v1`,
`appgen.component-render-contract.v1`,
`appgen.component-render-node.v1`,
`appgen.component-runtime-contract.v1`, and
`appgen.component-serialization-contract.v1`, plus design/data runtime schemas:
`appgen.component-state-model-contract.v1`,
`appgen.component-target-adapter-contract.v1`,
`appgen.component-template-package.v1`,
`appgen.component-template-workbench.v1`,
`appgen.component-test-plan.v1`,
`appgen.component-usability-workbench.v1`,
`appgen.composition-dependency-audit.v1`,
`appgen.composition-graph.v1`,
`appgen.composition-install-plan.v1`,
`appgen.composition-package.v1`,
`appgen.composition-preview.v1`,
`appgen.composition-release-gate.v1`,
`appgen.composition-workbench.v1`,
`appgen.config-admin-release-gate.v1`,
`appgen.config-admin-workbench.v1`,
`appgen.conflict-resolution-plan.v1`,
`appgen.context-menu-action-plan.v1`,
`appgen.coverage-area-catalog.v1`,
`appgen.coverage-release-gate.v1`,
`appgen.coverage-workbench.v1`,
`appgen.cross-platform-visual-depth-contract.v1`,
`appgen.cross-service-relationship-consistency.v1`,
`appgen.cross-service-relationship-resolver.v1`,
`appgen.cross-target-3d-scene-authoring-contract.v1`,
`appgen.cross-target-3d-scene-contract.v1`,
`appgen.cross-target-animation-timeline-contract.v1`,
`appgen.cross-target-asset-import-transaction-replay.v1`,
`appgen.cross-target-asset-import-workflow.v1`,
`appgen.cross-target-author-scene-operation.v1`,
`appgen.cross-target-author-style-operation.v1`,
`appgen.cross-target-author-timeline-operation.v1`,
`appgen.cross-target-effect-budget-contract.v1`,
`appgen.cross-target-effect-editor-transaction-replay.v1`,
`appgen.cross-target-effect-fallback-matrix-contract.v1`,
`appgen.cross-target-effect-render-workflow.v1`,
`appgen.cross-target-effect-stack-validation-contract.v1`,
`appgen.cross-target-effects-pipeline-contract.v1`,
`appgen.cross-target-hit-test-transform-operation.v1`,
`appgen.cross-target-import-visual-asset-operation.v1`,
`appgen.cross-target-material-binding-contract.v1`,
`appgen.cross-target-preview-runtime-diff-workflow.v1`,
`appgen.cross-target-run-visual-component-scenario-operation.v1`,
`appgen.cross-target-runtime-artifact-transaction-replay.v1`,
`appgen.cross-target-scene-camera-light-transaction-replay.v1`,
`appgen.cross-target-scene-graph-integrity-contract.v1`,
`appgen.cross-target-scene-hit-test-contract.v1`,
`appgen.cross-target-scene-material-editor-transaction-replay.v1`,
`appgen.cross-target-scene-transform-gizmo-contract.v1`,
`appgen.cross-target-scene-transform-transaction-replay.v1`,
`appgen.cross-target-scene-validation-workflow.v1`,
`appgen.cross-target-shader-material-editor-contract.v1`,
`appgen.cross-target-state-graph-contract.v1`,
`appgen.cross-target-style-cascade-contract.v1`,
`appgen.cross-target-style-inheritance-trace-contract.v1`,
`appgen.cross-target-style-override-transaction-replay.v1`,
`appgen.cross-target-style-resolution-workflow.v1`,
`appgen.cross-target-style-resource-contract.v1`,
`appgen.cross-target-style-token-validation-contract.v1`,
`appgen.cross-target-timeline-editor-transaction-replay.v1`,
`appgen.cross-target-timeline-interpolation-contract.v1`,
`appgen.cross-target-timeline-playback-workflow.v1`,
`appgen.cross-target-timeline-runtime-export-contract.v1`,
`appgen.cross-target-timeline-scrub-contract.v1`,
`appgen.cross-target-validate-effect-stack-operation.v1`,
`appgen.cross-target-validate-visual-component-operation.v1`,
`appgen.cross-target-visual-actionable-operations.v1`,
`appgen.cross-target-visual-asset-import-contract.v1`,
`appgen.cross-target-visual-component-spec-contract.v1`,
`appgen.cross-target-visual-depth-workbench.v1`,
`appgen.cross-target-visual-designer-transaction-replay-contract.v1`,
`appgen.cross-target-visual-lifecycle-replay.v1`,
`appgen.cross-target-visual-preview-runtime-contract.v1`,
`appgen.cross-target-visual-readiness-contract.v1`,
`appgen.cross-target-visual-runtime-package.v1`,
`appgen.cross-target-visual-runtime-replay-contract.v1`,
`appgen.custom-designer-activation-contract.v1`,
`appgen.custom-designer-family-contract.v1`,
`appgen.custom-widget-preview.v1`,
`appgen.custom-widget-registration.v1`,
`appgen.custom-widget.v1`,
`appgen.dashboard-release-gate.v1`,
`appgen.data-access-release-gate.v1`,
`appgen.data-access-workbench.v1`,
`appgen.data-change-capture-lineage-contract.v1`,
`appgen.data-connection-failover-contract.v1`,
`appgen.data-connection-pool-contract.v1`,
`appgen.data-connection-test-contract.v1`,
`appgen.data-dataset-designer-workflow-contract.v1`,
`appgen.data-dataset-field-catalog-contract.v1`,
`appgen.data-dataset-state-machine-contract.v1`,
`appgen.data-dictionary.v1`,
`appgen.data-driver-capability-matrix.v1`,
`appgen.data-exchange-release-gate.v1`,
`appgen.data-exchange-workbench.v1`,
`appgen.data-lookup-editor-pipeline-contract.v1`,
`appgen.data-migration-rehearsal-contract.v1`,
`appgen.data-module-generation-contract.v1`,
`appgen.data-module-runtime-smoke-contract.v1`,
`appgen.data-offline-queue-integrity-contract.v1`,
`appgen.data-offline-replay-contract.v1`,
`appgen.data-offline-sync-contract.v1`,
`appgen.data-parameter-binding-contract.v1`,
`appgen.data-query-plan-visualizer-contract.v1`,
`appgen.data-query-preview-contract.v1`,
`appgen.data-relationship-join-plan.v1`,
`appgen.data-relationship-lookup-lifecycle-replay.v1`,
`appgen.data-relationship-navigation-contract.v1`,
`appgen.data-replication-monitor-contract.v1`,
`appgen.data-resource-publish-contract.v1`,
`appgen.data-schema-adapter-diff-contract.v1`,
`appgen.data-schema-browser-contract.v1`,
`appgen.data-schema-checkpoint-contract.v1`,
`appgen.data-server-method-invocation-contract.v1`,
`appgen.data-service-contract-test-plan.v1`,
`appgen.data-service-invocation-trace-contract.v1`,
`appgen.data-service-method-contract.v1`,
`appgen.data-service-resource-contract.v1`,
`appgen.data-service-security-contract.v1`,
`appgen.data-service-telemetry-contract.v1`,
`appgen.data-service-versioning-contract.v1`,
`appgen.data-sql-authoring-safety-contract.v1`,
`appgen.data-stored-procedure-workflow-contract.v1`,
`appgen.data-tooling-actionable-operations.v1`,
`appgen.data-tooling-browse-schema-operation.v1`,
`appgen.data-tooling-connection-designer-transaction-replay.v1`,
`appgen.data-tooling-design-dataset-operation.v1`,
`appgen.data-tooling-design-runtime-session-replay-contract.v1`,
`appgen.data-tooling-failover-transaction-replay.v1`,
`appgen.data-tooling-ide-scenario-operation.v1`,
`appgen.data-tooling-lookup-editor-operation.v1`,
`appgen.data-tooling-module-replay-matrix.v1`,
`appgen.data-tooling-monitor-replication-operation.v1`,
`appgen.data-tooling-preview-query-operation.v1`,
`appgen.data-tooling-publish-resource-operation.v1`,
`appgen.data-tooling-publish-transaction-replay-contract.v1`,
`appgen.data-tooling-query-designer-transaction-replay.v1`,
`appgen.data-tooling-readiness-contract.v1`,
`appgen.data-tooling-rehearse-offline-replay-operation.v1`,
`appgen.data-tooling-run-module-smoke-operation.v1`,
`appgen.data-tooling-runtime-replay-contract.v1`,
`appgen.data-tooling-schema-diff-operation.v1`,
`appgen.data-tooling-service-contract-tests.v1`,
`appgen.data-tooling-service-method-transaction-replay.v1`,
`appgen.data-tooling-test-connection-operation.v1`,
`appgen.data-transaction-rehearsal-contract.v1`,
`appgen.database-addon-release-gate.v1`,
`appgen.database-backed-form-column-guard.v1`,
`appgen.database-cutover-plan.v1`,
`appgen.database-design-release-gate.v1`,
`appgen.database-migration-risk.v1`,
`appgen.database-ops-workbench.v1`,
`appgen.decision-trace.v1`,
`appgen.decision-tree.v1`,
`appgen.deep-data-tooling-operation-manifest.v1`,
`appgen.deep-data-tooling-operation-steps.v1`,
`appgen.deep-data-tooling-runtime-context.v1`,
`appgen.deep-data-tooling-surface-checks.v1`,
`appgen.deep-data-tooling-validation-steps.v1`,
`appgen.deployment-release-gate.v1`,
`appgen.deployment-scaling-profile.v1`,
`appgen.deployment-workbench.v1`,
`appgen.design-system.v1`,
`appgen.design-time-package-install-session.v1`,
`appgen.design-time-package-manager-workbench.v1`,
`appgen.desktop-cache-snapshot.v1`,
`appgen.desktop-change-set.v1`,
`appgen.desktop-sync-plan.v1`,
`appgen.device-api-component-design-tools.v1`,
`appgen.device-api-component-event-dispatch.v1`,
`appgen.device-api-component-generated-test-smoke.v1`,
`appgen.device-api-component-operation-steps.v1`,
`appgen.device-api-component-prop-validation.v1`,
`appgen.device-api-component-render-node.v1`,
`appgen.device-api-component-scenario.v1`,
`appgen.device-api-component-smoke-test.v1`,
`appgen.device-api-component-spec.v1`,
`appgen.device-api-component-validation-steps.v1`,
`appgen.devtools-module-file-manifest.v1`,
`appgen.devtools-module-replay-matrix.v1`,
`appgen.devtools-module-test-file-manifest.v1`,
`appgen.devtools-release-gate.v1`,
`appgen.devtools-workbench.v1`,
`appgen.dfm-binary-round-trip.v1`,
`appgen.dfm-parse-result.v1`,
`appgen.dfm-round-trip.v1`,
`appgen.dfm-stream-diff-merge-contract.v1`,
`appgen.dfm-stream-migration-contract.v1`,
`appgen.dfm-stream-variant-round-trip-contract.v1`,
`appgen.dfm-streaming-contract.v1`,
`appgen.diagnostics-module-file-manifest.v1`,
`appgen.diagnostics-module-test-file-manifest.v1`,
`appgen.diagnostics-release-gate.v1`,
`appgen.diagnostics-remediation.v1`,
`appgen.diagnostics-workbench.v1`,
`appgen.disaster-recovery-plan.v1`,
`appgen.document-management-workbench.v1`,
`appgen.document-release-gate.v1`,
`appgen.documentation-workbench.v1`,
`appgen.dsl-source.v1`,
`appgen.emerging-release-gate.v1`,
`appgen.emerging-workbench.v1`,
`appgen.enterprise-data-ide-embedded-store-operation.v1`,
`appgen.enterprise-data-ide-failover-replay-operation.v1`,
`appgen.enterprise-data-ide-operation-steps.v1`,
`appgen.enterprise-data-ide-operation.v1`,
`appgen.enterprise-data-ide-runtime-context.v1`,
`appgen.enterprise-data-ide-surface-manifest.v1`,
`appgen.enterprise-data-ide-validation-steps.v1`,
`appgen.erasure-plan.v1`,
`appgen.erp-domain-coverage.v1`,
`appgen.erp-implementation-roadmap.v1`,
`appgen.erp-migration-plan.v1`,
`appgen.erp-release-gate.v1`,
`appgen.erp-template-module-file-manifest.v1`,
`appgen.erp-template-module-test-file-manifest.v1`,
`appgen.erp-template-workbench.v1`,
`appgen.event-editor-family-contract.v1`,
`appgen.event-module-file-manifest.v1`,
`appgen.event-module-test-file-manifest.v1`,
`appgen.event-processing.choice-lock.v1`,
`appgen.event-processing.decision-runbook.v1`,
`appgen.event-processing.default-stack.v1`,
`appgen.event-processing.developer-action.v1`,
`appgen.event-processing.implementation-playbook.v1`,
`appgen.event-processing.recommendation-card.v1`,
`appgen.event-processing.standard.v1`,
`appgen.event-processing.use-this.v1`,
`appgen.event-release-gate.v1`,
`appgen.event-workbench.v1`,
`appgen.exchange.v1`,
`appgen.extension-release-gate.v1`,
`appgen.extension-workbench.v1`,
`appgen.finance-release-gate.v1`,
`appgen.finance-workbench.v1`,
`appgen.form-designer-generation-smoke-audit.v1`,
`appgen.form-designer-release-gate.v1`,
`appgen.form-designer-workbench.v1`,
`appgen.form-interaction-family-contract.v1`,
`appgen.form-interaction-family-operation.v1`, and
`appgen.frontend-environment.v1`, plus generated frontend/component runtime schemas:
`appgen.frontend-framework-parity-matrix.v1`,
`appgen.frontend-generation-experience-gate.v1`,
`appgen.frontend-quality-matrix.v1`,
`appgen.frontend-release-gate.v1`,
`appgen.generated-app-excellence-gate.v1`,
`appgen.generated-app-shell-chrome-contract.v1`,
`appgen.generated-app-shell-chrome-transaction-replay.v1`,
`appgen.generated-binding-accessibility-contract.v1`,
`appgen.generated-binding-authoring-session.v1`,
`appgen.generated-binding-bulk-edit-contract.v1`,
`appgen.generated-binding-conflict-resolution-workflow.v1`,
`appgen.generated-binding-conflict-validation-contract.v1`,
`appgen.generated-binding-dataset-cursor-sync-contract.v1`,
`appgen.generated-binding-dependency-execution-plan-contract.v1`,
`appgen.generated-binding-design-runtime-session-replay-contract.v1`,
`appgen.generated-binding-designer-family-contract.v1`,
`appgen.generated-binding-designer-family-module-file-manifest.v1`,
`appgen.generated-binding-designer-family-module-test-file-manifest.v1`,
`appgen.generated-binding-designer-transaction-replay-contract.v1`,
`appgen.generated-binding-diagnostics-contract.v1`,
`appgen.generated-binding-edit-transaction-contract.v1`,
`appgen.generated-binding-expression-editor-transaction-replay.v1`,
`appgen.generated-binding-expression-sandbox-contract.v1`,
`appgen.generated-binding-expression-validation.v1`,
`appgen.generated-binding-graph-editing-surface-contract.v1`,
`appgen.generated-binding-graph-json.v1`,
`appgen.generated-binding-graph-validation-contract.v1`,
`appgen.generated-binding-history-contract.v1`,
`appgen.generated-binding-hit-testing-contract.v1`,
`appgen.generated-binding-lifecycle-release-replay.v1`,
`appgen.generated-binding-lookup-contract.v1`,
`appgen.generated-binding-master-detail-contract.v1`,
`appgen.generated-binding-offline-replay-contract.v1`,
`appgen.generated-binding-pipeline-contract.v1`,
`appgen.generated-binding-preview-evaluation-contract.v1`,
`appgen.generated-binding-preview-runtime-parity-contract.v1`,
`appgen.generated-binding-round-trip-contract.v1`,
`appgen.generated-binding-runtime-failure-recovery-contract.v1`,
`appgen.generated-binding-runtime-gate-contract.v1`,
`appgen.generated-binding-runtime-manifest.v1`,
`appgen.generated-binding-runtime-propagation-replay-contract.v1`,
`appgen.generated-binding-runtime-replay.v1`,
`appgen.generated-binding-runtime-smoke.v1`,
`appgen.generated-binding-runtime-validation.v1`,
`appgen.generated-binding-runtime-wiring-contract.v1`,
`appgen.generated-binding-scope-context-contract.v1`,
`appgen.generated-binding-update-scheduler-contract.v1`,
`appgen.generated-component-analog-group-audit.v1`,
`appgen.generated-component-analog-workbench.v1`,
`appgen.generated-component-behavior-contract.v1`,
`appgen.generated-component-behavior-workbench.v1`,
`appgen.generated-component-binding-surface-contract.v1`,
`appgen.generated-component-capability-contract.v1`,
`appgen.generated-component-design-surface-contract.v1`,
`appgen.generated-component-designer-metadata-contract.v1`,
`appgen.generated-component-drag-start-operation.v1`,
`appgen.generated-component-drop-commit-operation.v1`,
`appgen.generated-component-drop-preview-operation.v1`,
`appgen.generated-component-drop-wiring-handler-contract.v1`,
`appgen.generated-component-editor-execution-contract.v1`,
`appgen.generated-component-editor-family-contract.v1`,
`appgen.generated-component-editor-family-module-file-manifest.v1`,
`appgen.generated-component-editor-family-module-test-file-manifest.v1`,
`appgen.generated-component-event-binding-operation.v1`,
`appgen.generated-component-event-dispatch-contract.v1`,
`appgen.generated-component-family-runtime-replay-matrix.v1`,
`appgen.generated-component-handler-definition-operation.v1`,
`appgen.generated-component-ide-readiness-catalog.v1`,
`appgen.generated-component-module-implementation-contract.v1`,
`appgen.generated-component-package-actionable-operations.v1`,
`appgen.generated-component-package-adapter-smoke-contract.v1`,
`appgen.generated-component-package-behavior-contract.v1`,
`appgen.generated-component-package-behavior-workbench.v1`,
`appgen.generated-component-package-compatibility-smoke-suite.v1`,
`appgen.generated-component-package-contract.v1`,
`appgen.generated-component-package-dependency-conflict-transaction-replay.v1`,
`appgen.generated-component-package-dependency-graph.v1`,
`appgen.generated-component-package-dependency-order-contract.v1`,
`appgen.generated-component-package-failure-isolation-contract.v1`,
`appgen.generated-component-package-hot-reload-transaction-replay.v1`,
`appgen.generated-component-package-icon-asset-transaction-replay.v1`,
`appgen.generated-component-package-install-session-replay.v1`,
`appgen.generated-component-package-installation-scenario-operation.v1`,
`appgen.generated-component-package-lifecycle-execution.v1`,
`appgen.generated-component-package-lifecycle-transaction-replay.v1`,
`appgen.generated-component-package-load-policy.v1`,
`appgen.generated-component-package-load-validation.v1`,
`appgen.generated-component-package-lockfile-integrity-contract.v1`,
`appgen.generated-component-package-marketplace-publication-contract.v1`,
`appgen.generated-component-package-module-implementation-contract.v1`,
`appgen.generated-component-package-palette-refresh-contract.v1`,
`appgen.generated-component-package-preview-load-contract.v1`,
`appgen.generated-component-package-preview-load-operation.v1`,
`appgen.generated-component-package-readiness-contract.v1`,
`appgen.generated-component-package-registration-consistency-contract.v1`,
`appgen.generated-component-package-registry-commit-operation.v1`,
`appgen.generated-component-package-resolve-metadata-operation.v1`,
`appgen.generated-component-package-rollback-contract.v1`,
`appgen.generated-component-package-sandbox-policy-contract.v1`,
`appgen.generated-component-package-signature-validation.v1`,
`appgen.generated-component-package-uninstall-operation.v1`,
`appgen.generated-component-package-uninstall-plan-contract.v1`,
`appgen.generated-component-package-update-operation.v1`,
`appgen.generated-component-package-update-plan-contract.v1`,
`appgen.generated-component-package-version-conflict-contract.v1`,
`appgen.generated-component-package-workbench.v1`,
`appgen.generated-component-palette-registration-contract.v1`,
`appgen.generated-component-parity-readiness-contract.v1`,
`appgen.generated-component-parity-runtime-manifest.v1`,
`appgen.generated-component-parity-runtime-replay.v1`,
`appgen.generated-component-parity-runtime-smoke.v1`,
`appgen.generated-component-parity-runtime-validation.v1`,
`appgen.generated-component-parity-scenario-operation.v1`,
`appgen.generated-component-prop-validation-contract.v1`,
`appgen.generated-component-render-contract.v1`,
`appgen.generated-component-runtime-contract.v1`,
`appgen.generated-component-serialization-contract.v1`,
`appgen.generated-component-state-model-contract.v1`,
`appgen.generated-component-target-adapter-contract.v1`, and
`appgen.generated-component-usability-workbench.v1`, plus generated visual/data/mobile
runtime schemas:
`appgen.generated-component-wiring-module-file-manifest.v1`,
`appgen.generated-component-wiring-module-test-file-manifest.v1`,
`appgen.generated-cross-platform-visual-depth-contract.v1`,
`appgen.generated-cross-target-3d-scene-authoring-contract.v1`,
`appgen.generated-cross-target-3d-scene-contract.v1`,
`appgen.generated-cross-target-animation-timeline-contract.v1`,
`appgen.generated-cross-target-asset-import-transaction-replay.v1`,
`appgen.generated-cross-target-asset-import-workflow.v1`,
`appgen.generated-cross-target-author-scene-operation.v1`,
`appgen.generated-cross-target-author-style-operation.v1`,
`appgen.generated-cross-target-author-timeline-operation.v1`,
`appgen.generated-cross-target-effect-budget-contract.v1`,
`appgen.generated-cross-target-effect-editor-transaction-replay.v1`,
`appgen.generated-cross-target-effect-fallback-matrix-contract.v1`,
`appgen.generated-cross-target-effect-render-workflow.v1`,
`appgen.generated-cross-target-effect-stack-validation-contract.v1`,
`appgen.generated-cross-target-effects-pipeline-contract.v1`,
`appgen.generated-cross-target-hit-test-transform-operation.v1`,
`appgen.generated-cross-target-import-visual-asset-operation.v1`,
`appgen.generated-cross-target-material-binding-contract.v1`,
`appgen.generated-cross-target-preview-runtime-diff-workflow.v1`,
`appgen.generated-cross-target-run-visual-component-scenario-operation.v1`,
`appgen.generated-cross-target-runtime-artifact-transaction-replay.v1`,
`appgen.generated-cross-target-scene-camera-light-transaction-replay.v1`,
`appgen.generated-cross-target-scene-graph-integrity-contract.v1`,
`appgen.generated-cross-target-scene-hit-test-contract.v1`,
`appgen.generated-cross-target-scene-material-editor-transaction-replay.v1`,
`appgen.generated-cross-target-scene-transform-gizmo-contract.v1`,
`appgen.generated-cross-target-scene-transform-transaction-replay.v1`,
`appgen.generated-cross-target-scene-validation-workflow.v1`,
`appgen.generated-cross-target-shader-material-editor-contract.v1`,
`appgen.generated-cross-target-state-graph-contract.v1`,
`appgen.generated-cross-target-style-cascade-contract.v1`,
`appgen.generated-cross-target-style-inheritance-trace-contract.v1`,
`appgen.generated-cross-target-style-override-transaction-replay.v1`,
`appgen.generated-cross-target-style-resolution-workflow.v1`,
`appgen.generated-cross-target-style-resource-contract.v1`,
`appgen.generated-cross-target-style-token-validation-contract.v1`,
`appgen.generated-cross-target-timeline-editor-transaction-replay.v1`,
`appgen.generated-cross-target-timeline-interpolation-contract.v1`,
`appgen.generated-cross-target-timeline-playback-workflow.v1`,
`appgen.generated-cross-target-timeline-runtime-export-contract.v1`,
`appgen.generated-cross-target-timeline-scrub-contract.v1`,
`appgen.generated-cross-target-validate-effect-stack-operation.v1`,
`appgen.generated-cross-target-validate-visual-component-operation.v1`,
`appgen.generated-cross-target-visual-actionable-operations.v1`,
`appgen.generated-cross-target-visual-asset-import-contract.v1`,
`appgen.generated-cross-target-visual-component-spec-contract.v1`,
`appgen.generated-cross-target-visual-depth-workbench.v1`,
`appgen.generated-cross-target-visual-designer-transaction-replay-contract.v1`,
`appgen.generated-cross-target-visual-lifecycle-replay.v1`,
`appgen.generated-cross-target-visual-preview-runtime-contract.v1`,
`appgen.generated-cross-target-visual-readiness-contract.v1`,
`appgen.generated-cross-target-visual-runtime-package.v1`,
`appgen.generated-cross-target-visual-runtime-replay-contract.v1`,
`appgen.generated-custom-designer-activation-contract.v1`,
`appgen.generated-custom-designer-family-contract.v1`,
`appgen.generated-custom-designer-family-module-file-manifest.v1`,
`appgen.generated-custom-designer-family-module-test-file-manifest.v1`,
`appgen.generated-data-change-capture-lineage-contract.v1`,
`appgen.generated-data-connection-failover-contract.v1`,
`appgen.generated-data-connection-pool-contract.v1`,
`appgen.generated-data-connection-runtime-manifest.v1`,
`appgen.generated-data-connection-test-contract.v1`,
`appgen.generated-data-dataset-designer-workflow-contract.v1`,
`appgen.generated-data-dataset-field-catalog-contract.v1`,
`appgen.generated-data-dataset-state-machine-contract.v1`,
`appgen.generated-data-driver-capability-matrix.v1`,
`appgen.generated-data-lookup-editor-pipeline-contract.v1`,
`appgen.generated-data-migration-rehearsal-contract.v1`,
`appgen.generated-data-module-generation-contract.v1`,
`appgen.generated-data-module-runtime-smoke-contract.v1`,
`appgen.generated-data-offline-queue-integrity-contract.v1`,
`appgen.generated-data-offline-replay-contract.v1`,
`appgen.generated-data-offline-sync-contract.v1`,
`appgen.generated-data-parameter-binding-contract.v1`,
`appgen.generated-data-query-plan-visualizer-contract.v1`,
`appgen.generated-data-query-preview-contract.v1`,
`appgen.generated-data-relationship-join-plan.v1`,
`appgen.generated-data-relationship-lookup-lifecycle-replay.v1`,
`appgen.generated-data-relationship-lookup-runtime-manifest.v1`,
`appgen.generated-data-relationship-navigation-contract.v1`,
`appgen.generated-data-replication-monitor-contract.v1`,
`appgen.generated-data-resource-publish-contract.v1`,
`appgen.generated-data-schema-adapter-diff-contract.v1`,
`appgen.generated-data-schema-browser-contract.v1`,
`appgen.generated-data-schema-checkpoint-contract.v1`,
`appgen.generated-data-server-method-invocation-contract.v1`,
`appgen.generated-data-service-contract-test-plan.v1`,
`appgen.generated-data-service-invocation-trace-contract.v1`,
`appgen.generated-data-service-method-contract.v1`,
`appgen.generated-data-service-resource-contract.v1`,
`appgen.generated-data-service-runtime-manifest.v1`,
`appgen.generated-data-service-security-contract.v1`,
`appgen.generated-data-service-telemetry-contract.v1`,
`appgen.generated-data-service-versioning-contract.v1`,
`appgen.generated-data-sql-authoring-safety-contract.v1`,
`appgen.generated-data-stored-procedure-workflow-contract.v1`,
`appgen.generated-data-tooling-actionable-operations.v1`,
`appgen.generated-data-tooling-browse-schema-operation.v1`,
`appgen.generated-data-tooling-connection-designer-transaction-replay.v1`,
`appgen.generated-data-tooling-design-dataset-operation.v1`,
`appgen.generated-data-tooling-design-runtime-session-replay-contract.v1`,
`appgen.generated-data-tooling-failover-transaction-replay.v1`,
`appgen.generated-data-tooling-ide-scenario-operation.v1`,
`appgen.generated-data-tooling-lookup-editor-operation.v1`,
`appgen.generated-data-tooling-module-replay-matrix.v1`,
`appgen.generated-data-tooling-monitor-replication-operation.v1`,
`appgen.generated-data-tooling-preview-query-operation.v1`,
`appgen.generated-data-tooling-publish-resource-operation.v1`,
`appgen.generated-data-tooling-publish-transaction-replay-contract.v1`,
`appgen.generated-data-tooling-query-designer-transaction-replay.v1`,
`appgen.generated-data-tooling-readiness-contract.v1`,
`appgen.generated-data-tooling-rehearse-offline-replay-operation.v1`,
`appgen.generated-data-tooling-run-module-smoke-operation.v1`,
`appgen.generated-data-tooling-runtime-manifest.v1`,
`appgen.generated-data-tooling-runtime-replay-contract.v1`,
`appgen.generated-data-tooling-runtime-replay.v1`,
`appgen.generated-data-tooling-runtime-smoke.v1`,
`appgen.generated-data-tooling-runtime-validation.v1`,
`appgen.generated-data-tooling-schema-diff-operation.v1`,
`appgen.generated-data-tooling-service-method-transaction-replay.v1`,
`appgen.generated-data-tooling-test-connection-operation.v1`,
`appgen.generated-data-transaction-rehearsal-contract.v1`,
`appgen.generated-data-transaction-runtime-manifest.v1`,
`appgen.generated-dataset-runtime-manifest.v1`,
`appgen.generated-design-time-package-install-session.v1`,
`appgen.generated-design-time-package-manager-workbench.v1`,
`appgen.generated-device-api-component-runtime-replay-matrix.v1`,
`appgen.generated-device-api-component-scenario-matrix.v1`,
`appgen.generated-dfm-binary-round-trip.v1`,
`appgen.generated-dfm-parse-result.v1`,
`appgen.generated-dfm-round-trip.v1`,
`appgen.generated-dfm-stream-diff-merge-contract.v1`,
`appgen.generated-dfm-stream-migration-contract.v1`,
`appgen.generated-dfm-stream-variant-round-trip-contract.v1`,
`appgen.generated-dfm-streaming-contract.v1`,
`appgen.generated-effect-runtime-assets.v1`,
`appgen.generated-event-editor-family-contract.v1`,
`appgen.generated-event-editor-family-module-file-manifest.v1`,
`appgen.generated-event-editor-family-module-test-file-manifest.v1`,
`appgen.generated-form-interaction-family-contract.v1`,
`appgen.generated-form-interaction-family-module-file-manifest.v1`,
`appgen.generated-form-interaction-family-module-test-file-manifest.v1`,
`appgen.generated-handler-architecture-module-file-manifest.v1`,
`appgen.generated-handler-architecture-module-test-file-manifest.v1`,
`appgen.generated-handler-source-ide-contract.v1`,
`appgen.generated-handler-source-ide-module-file-manifest.v1`,
`appgen.generated-handler-source-ide-module-test-file-manifest.v1`,
`appgen.generated-handler-source-round-trip-replay.v1`,
`appgen.generated-inspector-action-registry-contract.v1`,
`appgen.generated-inspector-binding-designer-bridge.v1`,
`appgen.generated-inspector-component-editor-history-contract.v1`,
`appgen.generated-inspector-component-editor-result.v1`,
`appgen.generated-inspector-component-editor-transaction.v1`,
`appgen.generated-inspector-component-handler-invocation.v1`,
`appgen.generated-inspector-component-tree-sync-contract.v1`,
`appgen.generated-inspector-cross-component-session-replay-contract.v1`,
`appgen.generated-inspector-cross-handler-invocation-contract.v1`,
`appgen.generated-inspector-custom-designer-hit-test-contract.v1`,
`appgen.generated-inspector-custom-designer-lifecycle-contract.v1`,
`appgen.generated-inspector-custom-designer-registration-replay-contract.v1`,
`appgen.generated-inspector-custom-designer-registration-result.v1`,
`appgen.generated-inspector-custom-designer-render-workflow.v1`,
`appgen.generated-inspector-custom-designer-transaction-replay.v1`,
`appgen.generated-inspector-design-surface-transaction-replay-contract.v1`,
`appgen.generated-inspector-diagnostics-contract.v1`,
`appgen.generated-inspector-edit-session-replay-contract.v1`,
`appgen.generated-inspector-editor-lifecycle-replay.v1`,
`appgen.generated-inspector-editor-registry.v1`,
`appgen.generated-inspector-editor-scenario-operation.v1`,
`appgen.generated-inspector-editor-surface-contract.v1`,
`appgen.generated-inspector-event-edit-workflow.v1`,
`appgen.generated-inspector-event-handler-result.v1`,
`appgen.generated-inspector-event-handler-signature-contract.v1`,
`appgen.generated-inspector-event-lifecycle-contract.v1`,
`appgen.generated-inspector-event-rename-result.v1`,
`appgen.generated-inspector-event-signature-routing-contract.v1`,
`appgen.generated-inspector-family-replay-matrix.v1`,
`appgen.generated-inspector-family-runtime-replay-matrix.v1`,
`appgen.generated-inspector-metadata-json.v1`,
`appgen.generated-inspector-multi-select-contract.v1`,
`appgen.generated-inspector-multi-select-property-transaction-replay.v1`,
`appgen.generated-inspector-property-dependency-contract.v1`,
`appgen.generated-inspector-property-edit-result.v1`,
`appgen.generated-inspector-property-edit-workflow.v1`,
`appgen.generated-inspector-property-editor-surface-transaction-replay.v1`,
`appgen.generated-inspector-property-grouping-contract.v1`,
`appgen.generated-inspector-property-validation-contract.v1`,
`appgen.generated-inspector-property-value-pipeline-contract.v1`,
`appgen.generated-inspector-round-trip-contract.v1`,
`appgen.generated-inspector-runtime-manifest.v1`,
`appgen.generated-inspector-runtime-replay.v1`,
`appgen.generated-inspector-runtime-smoke.v1`,
`appgen.generated-inspector-runtime-validation.v1`,
`appgen.generated-inspector-state-persistence-contract.v1`,
`appgen.generated-inspector-state-restore-workflow.v1`,
`appgen.generated-livebindings-actionable-operations.v1`,
`appgen.generated-livebindings-conflict-operation.v1`,
`appgen.generated-livebindings-designer-contract.v1`,
`appgen.generated-livebindings-designer-scenario-operation.v1`,
`appgen.generated-livebindings-graph.v1`,
`appgen.generated-livebindings-link-operation.v1`,
`appgen.generated-livebindings-preview-operation.v1`,
`appgen.generated-livebindings-readiness-contract.v1`,
`appgen.generated-livebindings-reroute-operation.v1`,
`appgen.generated-livebindings-runtime-wiring-operation.v1`,
`appgen.generated-livebindings-workbench.v1`,
`appgen.generated-local-backup-restore-verification-contract.v1`,
`appgen.generated-local-database-contract.v1`,
`appgen.generated-local-database-maintenance-contract.v1`,
`appgen.generated-local-database-maintenance-schedule-contract.v1`,
`appgen.generated-mobile-adapter-dispatch-workflow.v1`,
`appgen.generated-mobile-api-capability-matrix-contract.v1`,
`appgen.generated-mobile-app-lifecycle-delivery-contract.v1`,
`appgen.generated-mobile-background-delivery-contract.v1`,
`appgen.generated-mobile-background-resume-operation.v1`,
`appgen.generated-mobile-background-resume-workflow.v1`,
`appgen.generated-mobile-component-adapter-contract.v1`, and
`appgen.generated-mobile-deep-link-routing-contract.v1`, plus mobile/native/IDE runtime
schemas:
`appgen.generated-mobile-device-api-replay.v1`,
`appgen.generated-mobile-device-capability-lifecycle-replay.v1`,
`appgen.generated-mobile-device-component-spec-contract.v1`,
`appgen.generated-mobile-device-designer-transaction-replay-contract.v1`,
`appgen.generated-mobile-device-event-trace-contract.v1`,
`appgen.generated-mobile-device-runtime-manifest.v1`,
`appgen.generated-mobile-device-runtime-smoke.v1`,
`appgen.generated-mobile-device-runtime-validation.v1`,
`appgen.generated-mobile-device-scenario-matrix-contract.v1`,
`appgen.generated-mobile-device-simulator-contract.v1`,
`appgen.generated-mobile-device-target-scenario-matrix-contract.v1`,
`appgen.generated-mobile-dispatch-adapter-operation.v1`,
`appgen.generated-mobile-media-file-pipeline-contract.v1`,
`appgen.generated-mobile-native-api-actionable-operations.v1`,
`appgen.generated-mobile-native-api-contract.v1`,
`appgen.generated-mobile-native-api-readiness-contract.v1`,
`appgen.generated-mobile-native-api-runtime-replay-contract.v1`,
`appgen.generated-mobile-native-api-workbench.v1`,
`appgen.generated-mobile-native-bridge-error-contract.v1`,
`appgen.generated-mobile-native-bridge-matrix-contract.v1`,
`appgen.generated-mobile-native-call-transaction-replay.v1`,
`appgen.generated-mobile-offline-device-event-queue-contract.v1`,
`appgen.generated-mobile-permission-manifest-contract.v1`,
`appgen.generated-mobile-permission-prompt-workflow.v1`,
`appgen.generated-mobile-permission-revocation-contract.v1`,
`appgen.generated-mobile-permission-revocation-transaction-replay.v1`,
`appgen.generated-mobile-permission-state-machine-contract.v1`,
`appgen.generated-mobile-platform-fallback-operation.v1`,
`appgen.generated-mobile-platform-fallback-workflow.v1`,
`appgen.generated-mobile-privacy-review-operation.v1`,
`appgen.generated-mobile-privacy-review-workflow.v1`,
`appgen.generated-mobile-replay-simulator-operation.v1`,
`appgen.generated-mobile-request-permission-operation.v1`,
`appgen.generated-mobile-run-device-scenario-operation.v1`,
`appgen.generated-mobile-simulator-fixture-integrity-contract.v1`,
`appgen.generated-mobile-simulator-replay-workflow.v1`,
`appgen.generated-mobile-store-privacy-manifest-contract.v1`,
`appgen.generated-mobile-validate-device-component-operation.v1`,
`appgen.generated-native-form-runtime-manifest.v1`,
`appgen.generated-native-form-runtime-replay.v1`,
`appgen.generated-native-form-runtime-smoke.v1`,
`appgen.generated-native-form-runtime-validation.v1`,
`appgen.generated-native-runtime-operation-result.v1`,
`appgen.generated-native-runtime-operations-manifest.v1`,
`appgen.generated-native-runtime-operations-smoke.v1`,
`appgen.generated-native-runtime-operations-validation.v1`,
`appgen.generated-object-inspector-contract.v1`,
`appgen.generated-object-inspector-readiness-contract.v1`,
`appgen.generated-object-inspector-workbench.v1`,
`appgen.generated-offline-conflict-review-contract.v1`,
`appgen.generated-package-manager-module-replay-matrix.v1`,
`appgen.generated-package-manager-runtime-manifest.v1`,
`appgen.generated-package-manager-runtime-replay.v1`,
`appgen.generated-package-manager-runtime-smoke.v1`,
`appgen.generated-package-manager-runtime-validation.v1`,
`appgen.generated-pascal-apply-property-delta-operation.v1`,
`appgen.generated-pascal-compile-package-transaction-replay.v1`,
`appgen.generated-pascal-compile-preview-operation.v1`,
`appgen.generated-pascal-compiler-pipeline-contract.v1`,
`appgen.generated-pascal-compiler-recovery-contract.v1`,
`appgen.generated-pascal-component-inheritance-contract.v1`,
`appgen.generated-pascal-debug-session-transaction-replay.v1`,
`appgen.generated-pascal-debug-symbol-contract.v1`,
`appgen.generated-pascal-debug-watch-transaction-replay.v1`,
`appgen.generated-pascal-design-edit-session-replay-contract.v1`,
`appgen.generated-pascal-diagnostic-mapping-contract.v1`,
`appgen.generated-pascal-event-binding-contract.v1`,
`appgen.generated-pascal-event-handler-wiring-contract.v1`,
`appgen.generated-pascal-event-stub-evolution-contract.v1`,
`appgen.generated-pascal-form-stream-schema-contract.v1`,
`appgen.generated-pascal-incremental-compile-contract.v1`,
`appgen.generated-pascal-incremental-invalidation-contract.v1`,
`appgen.generated-pascal-language-frontend-contract.v1`,
`appgen.generated-pascal-open-design-stream-operation.v1`,
`appgen.generated-pascal-package-dependency-contract.v1`,
`appgen.generated-pascal-package-target-matrix-contract.v1`,
`appgen.generated-pascal-refresh-resources-operation.v1`,
`appgen.generated-pascal-reload-runtime-preview-operation.v1`,
`appgen.generated-pascal-resource-manifest-hash-contract.v1`,
`appgen.generated-pascal-resource-round-trip-fidelity-contract.v1`,
`appgen.generated-pascal-resource-streaming-contract.v1`,
`appgen.generated-pascal-round-trip-stream-operation.v1`,
`appgen.generated-pascal-rtti-contract.v1`,
`appgen.generated-pascal-runtime-actionable-operations.v1`,
`appgen.generated-pascal-runtime-artifact-parity-contract.v1`,
`appgen.generated-pascal-runtime-authoring-replay-matrix.v1`,
`appgen.generated-pascal-runtime-authoring-scenario-operation.v1`,
`appgen.generated-pascal-runtime-debug-authoring-contract.v1`,
`appgen.generated-pascal-runtime-lifecycle-contract.v1`,
`appgen.generated-pascal-runtime-memory-model-contract.v1`,
`appgen.generated-pascal-runtime-module-replay-matrix.v1`,
`appgen.generated-pascal-runtime-readiness-contract.v1`,
`appgen.generated-pascal-runtime-session-replay-contract.v1`,
`appgen.generated-pascal-runtime-workbench.v1`,
`appgen.generated-pascal-semantic-validation-contract.v1`,
`appgen.generated-pascal-start-debug-preview-operation.v1`,
`appgen.generated-pascal-static-analysis-contract.v1`,
`appgen.generated-pascal-toolchain-adapter-contract.v1`,
`appgen.generated-pascal-unit-contract.v1`,
`appgen.generated-pascal-unit-parse-contract.v1`,
`appgen.generated-platform-parity-lifecycle-replay.v1`,
`appgen.generated-platform-parity-requirement-audit.v1`,
`appgen.generated-property-editor-family-contract.v1`,
`appgen.generated-property-editor-family-module-file-manifest.v1`,
`appgen.generated-property-editor-family-module-test-file-manifest.v1`,
`appgen.generated-rad-data-tooling-contract.v1`,
`appgen.generated-rad-data-tooling-workbench.v1`,
`appgen.generated-rad-parity-workbench.v1`,
`appgen.generated-rad-query-designer-contract.v1`,
`appgen.generated-scene-runtime-assets.v1`,
`appgen.generated-style-runtime-assets.v1`,
`appgen.generated-third-party-component-import-contract.v1`,
`appgen.generated-third-party-component-install-plan.v1`,
`appgen.generated-timeline-runtime-assets.v1`,
`appgen.generated-visual-depth-runtime-manifest.v1`,
`appgen.generated-visual-depth-runtime-replay.v1`,
`appgen.generated-visual-depth-runtime-smoke.v1`,
`appgen.generated-visual-depth-runtime-validation.v1`,
`appgen.generated-visual-design-ide-replay-matrix.v1`,
`appgen.generated-visual-design-ide-runtime-replay-matrix.v1`,
`appgen.generated-visual-runtime-asset-manifest.v1`,
`appgen.generated-visual-runtime-asset-validation.v1`,
`appgen.generated-visual-runtime-assets-smoke.v1`,
`appgen.generated-visual-runtime-pipeline-replay-matrix.v1`,
`appgen.generated-visual-runtime-pipeline-runtime-replay-matrix.v1`,
`appgen.generated-wizard-module-file-manifest.v1`,
`appgen.generated-wizard-module-replay-matrix.v1`,
`appgen.generated-wizard-module-test-file-manifest.v1`,
`appgen.generation-artifacts.v1`,
`appgen.generation-job-log.v1`,
`appgen.generation-job-queue.v1`,
`appgen.generation-job-status.v1`,
`appgen.generation-job.v1`,
`appgen.gl-core-advanced-ledger-blueprint.v1`,
`appgen.handler-architecture-cross-call.v1`,
`appgen.handler-architecture-invocation.v1`,
`appgen.handler-source-ide-contract.v1`,
`appgen.handler-source-round-trip-replay.v1`,
`appgen.https-release-gate.v1`,
`appgen.https-workbench.v1`,
`appgen.i18n-missing.v1`,
`appgen.i18n-payload.v1`,
`appgen.i18n-release-gate.v1`,
`appgen.i18n-workbench.v1`,
`appgen.ide-capability-matrix.v1`,
`appgen.ide-diagnostics.v1`,
`appgen.ide-superiority-profile.v1`,
`appgen.ide-workflow-blueprint.v1`,
`appgen.identity-release-gate.v1`,
`appgen.identity-workbench.v1`,
`appgen.infrastructure-scaling-plan.v1`,
`appgen.inspector-action-registry-contract.v1`,
`appgen.inspector-binding-designer-bridge.v1`,
`appgen.inspector-component-editor-history-contract.v1`,
`appgen.inspector-component-editor-result.v1`,
`appgen.inspector-component-editor-transaction.v1`,
`appgen.inspector-component-handler-invocation.v1`,
`appgen.inspector-component-tree-sync-contract.v1`,
`appgen.inspector-cross-component-session-replay-contract.v1`,
`appgen.inspector-cross-handler-invocation-contract.v1`,
`appgen.inspector-custom-designer-hit-test-contract.v1`,
`appgen.inspector-custom-designer-lifecycle-contract.v1`,
`appgen.inspector-custom-designer-registration-replay-contract.v1`,
`appgen.inspector-custom-designer-registration-result.v1`,
`appgen.inspector-custom-designer-render-workflow.v1`,
`appgen.inspector-custom-designer-transaction-replay.v1`,
`appgen.inspector-design-surface-transaction-replay-contract.v1`,
`appgen.inspector-diagnostics-contract.v1`,
`appgen.inspector-edit-session-replay-contract.v1`,
`appgen.inspector-editor-lifecycle-replay.v1`,
`appgen.inspector-editor-registry.v1`,
`appgen.inspector-editor-scenario-operation.v1`,
`appgen.inspector-editor-surface-contract.v1`,
`appgen.inspector-event-edit-workflow.v1`,
`appgen.inspector-event-handler-result.v1`,
`appgen.inspector-event-handler-signature-contract.v1`,
`appgen.inspector-event-lifecycle-contract.v1`,
`appgen.inspector-event-rename-result.v1`,
`appgen.inspector-event-signature-routing-contract.v1`,
`appgen.inspector-family-replay-matrix.v1`,
`appgen.inspector-metadata-json.v1`,
`appgen.inspector-multi-select-contract.v1`,
`appgen.inspector-multi-select-property-transaction-replay.v1`,
`appgen.inspector-property-dependency-contract.v1`,
`appgen.inspector-property-edit-result.v1`,
`appgen.inspector-property-edit-workflow.v1`,
`appgen.inspector-property-editor-surface-transaction-replay.v1`,
`appgen.inspector-property-grouping-contract.v1`,
`appgen.inspector-property-validation-contract.v1`,
`appgen.inspector-property-value-pipeline-contract.v1`,
`appgen.inspector-round-trip-contract.v1`,
`appgen.inspector-state-persistence-contract.v1`,
`appgen.inspector-state-restore-workflow.v1`,
`appgen.integration-generation-smoke-audit.v1`,
`appgen.integration-release-gate.v1`,
`appgen.integration-workbench.v1`,
`appgen.integration.entando.v1`,
`appgen.integration.invenio.v1`,
`appgen.intelligence-release-gate.v1`,
`appgen.intelligence-workbench.v1`,
`appgen.inventory-release-gate.v1`,
`appgen.inventory-workbench.v1`,
`appgen.jhipster-adoption-plan.v1`,
`appgen.jhipster-capability-depth-index.v1`,
`appgen.jhipster-capability-proof-matrix.v1`,
`appgen.jhipster-feature-superiority-index.v1`,
`appgen.jhipster-frontier-gate.v1`,
`appgen.jhipster-gap-analysis.v1`,
`appgen.jhipster-migration-release-gate.v1`,
`appgen.jhipster-superiority-tiers.v1`,
`appgen.jhipster-superset-blueprint.v1`,
`appgen.jhipster-superset-certification.v1`,
`appgen.jhipster-superset-evidence.v1`,
`appgen.jhipster-superset-scorecard.v1`,
`appgen.jhipster-upgrade-migration-plan.v1`,
`appgen.layout-workbench.v1`,
`appgen.lifecycle-release-gate.v1`,
`appgen.lifecycle-workbench.v1`,
`appgen.livebindings-actionable-operations.v1`,
`appgen.livebindings-conflict-operation.v1`,
`appgen.livebindings-designer-contract.v1`,
`appgen.livebindings-designer-scenario-operation.v1`,
`appgen.livebindings-graph.v1`,
`appgen.livebindings-link-operation.v1`,
`appgen.livebindings-preview-operation.v1`,
`appgen.livebindings-readiness-contract.v1`,
`appgen.livebindings-reroute-operation.v1`,
`appgen.livebindings-runtime-wiring-operation.v1`,
`appgen.livebindings-workbench.v1`,
`appgen.load-profile.v1`,
`appgen.load-test-matrix.v1`,
`appgen.load-test-runbook.v1`,
`appgen.local-backup-restore-verification-contract.v1`,
`appgen.local-database-contract.v1`,
`appgen.local-database-maintenance-contract.v1`,
`appgen.local-database-maintenance-schedule-contract.v1`,
`appgen.lookup-workbench.v1`,
`appgen.manufacturing-release-gate.v1`,
`appgen.manufacturing-workbench.v1`,
`appgen.media-release-gate.v1`,
`appgen.media-workbench.v1`,
`appgen.menu-edit-plan.v1`,
`appgen.menu-edit-schema.v1`,
`appgen.merge-queue.v1`,
`appgen.microservice-module-file-manifest.v1`,
`appgen.microservice-module-test-file-manifest.v1`,
`appgen.microservice-release-gate.v1`,
`appgen.microservice-workbench.v1`,
`appgen.migration-batch.v1`,
`appgen.migration-release-gate.v1`,
`appgen.migration-review-checklist.v1`,
`appgen.migration-revision-plan.v1`,
`appgen.migration-rollback-plan.v1`,
`appgen.migration-sql-preview.v1`,
`appgen.migration-workbench.v1`,
`appgen.mobile-adapter-dispatch-workflow.v1`,
`appgen.mobile-api-capability-matrix-contract.v1`,
`appgen.mobile-app-lifecycle-delivery-contract.v1`, and
`appgen.mobile-background-delivery-contract.v1`. The catalog is intentionally complete:
every `appgen.*.v1` envelope named in this document, including IDE, frontend,
visual designer, LSP hover-depth, migration, natural-language, packaging,
release, component/PBC wrapper, and project-governance contracts, is exported as
a selectable schema and covered by representative sample validation.

Package release-audit schemas share one envelope shape: `format`, `ok`,
`decision`, `gates`, and `blocking_gaps` are required, with optional `scope`,
gate counts, release evidence, and stop-condition fields. This keeps every
top-level package release gate consumable by CI, IDE panels, and external coding
agents without making the aggregate schema audit execute each heavyweight
package verifier every time.

Agentic development-vector schemas make Claude Code, OpenAI Codex, OpenCode,
Ollama, vLLM, and API-key provider handoffs machine-validatable. The provider
matrix proves local/API-key model posture and secret handling, the tool-policy
and execution-matrix contracts prove generated agents are bounded by reviewed
tools and human review gates, the coding-agent backend/workflow/release contracts
prove `api-key`, `ollama`, and `vllm` development vectors, and the generated
agentic smoke audit proves generated apps expose the same contracts without
calling an external provider.

ACP composition schemas make event-processing guidance, composable topology,
capability coverage, and compact natural-language generation reusable by IDEs,
CI, and coding agents. The stream-processing policy and choice-resolution
contracts prove ordinary enterprise apps use the opinionated AppGen-X event
contract instead of a developer-facing runtime selector, while the topology and
capability-coverage contracts prove the composable runtime fabric and catalog
depth. The compact generation contracts prove small local models can receive a
bounded brief, emit DSL patches, and pass the full-app natural-language gate.

Top-level package support schemas make roadmap, base-feature, config-editor,
distribution, DSL-quality, ERP-template, and ideas evidence reusable without
running heavyweight generated-app smoke checks during every schema audit. These
schemas keep package release gates, generated smoke envelopes, template
manifests, seed fixtures, and goal-readiness audits visible to CI and external
agents while the runtime inventory enforces the zero-actionable-backlog contract
for top-level non-PBC runtime formats.

Binding-designer schemas make visual data-binding handoffs reusable without
scraping generated release audits. IDEs and agents can validate graph JSON,
expression validation, staged graph edits, lookup and master-detail wiring,
runtime propagation, offline replay, diagnostics, accessibility routes, and
full lifecycle replay from the same `appgen contract-schema` catalog used by CI.

Native Pascal/runtime schemas make form streaming, unit generation, compiler
planning, package target matrices, event handler wiring, resource hashes,
incremental invalidation, debugging previews, runtime reloads, and authoring
replay matrices machine-validatable. IDEs and package verifiers can now consume
these payloads directly instead of mining the aggregate form-designer workbench.

Target packaging schemas make web, PWA, mobile, desktop, chatbot, native
packager preflight, produced-artifact audits, binary adapter execution
transcripts, and runtime packaging proofs machine-validatable. CI and external
agents can validate host-packager readiness, mobile/desktop package plans,
generated runtime smoke checks, and native binary handoff evidence without
re-running the whole package release audit.

Visual modeling schemas make database designer edits first-class contracts.
IDEs and agents can validate schema graphs, visual table/field/relationship
proposals, migration previews, rollback plans, generated-code plans, DBML/SQL/
PonyORM exports, and generated visual-designer smoke evidence before applying
database-backed form or schema changes.

Generated application foundation schemas make security, workflow, and health
runtime evidence validate like every other first-class tooling contract. Release
automation can now inspect threat models, secret scans, dependency/security test
plans, security signoff/workbench payloads, workflow authorization and runbooks,
approval routes, SLA metadata, workflow workbench/release gates, and generated
health summaries without scraping generated source files.

Generated module schemas make the first large wave of generated app module
contracts validate through the same catalog: native form modules, runtime
operation modules, compiler/deep runtime modules, UI chrome, wizard, database
operations, data access/exchange, schema import, backup, seed, integration,
productivity, lifecycle, emerging feature, platform, PWA, microservice,
realtime, event, RPA, diagnostics, API testing, code review, collaboration, and
devtools module contracts. Their manifests, operation steps, validation steps,
release contexts, smoke tests, generated-test smoke payloads, and results now
share a schema-backed envelope for CI and external agents.

Generated IDE/productivity module schemas extend that envelope to project
management, ERP templates, version control, package management, binding modules,
binding-designer families, component wiring, form interaction, handler
architecture/source IDEs, property/event/component editors, custom designers,
inspector modules, data tooling, deep data tooling, enterprise data IDE,
visual-design IDE, and visual runtime pipeline modules. This keeps their
operations, editor manifests, validation steps, smoke plans, read-only probes,
and generated-test evidence selectable by `appgen contract-schema`.

Generated runtime/module manifest schemas extend the same contract family to
visual runtime replay, component-family and package-module smoke tests,
generated file/test manifests, replay matrices, designer and extension modules,
seed, backup, data access, schema import, database operations, data exchange,
voice, text-quality, notification, agentic, and view-composition module runtime
evidence. This lets generated app modules publish self-contained manifests and
runtime replay evidence that CI, IDE panels, and external agents can validate
without importing the generated application.

Application/component runtime schemas promote the high-traffic authoring path:
accessibility and agent workbenches, application create/open/import/export/
snapshot/restore/version plans, assistant and chatbot release gates, CI and
collaboration evidence, compliance workbenches, component drag/drop payloads,
event binding and dispatch, component family readiness/replay, component module
manifests, and package installation, dependency, lifecycle, palette, preview,
rollback, sandbox, signature, uninstall, update, render, runtime, and
serialization contracts. This makes the visual component ecosystem auditable as
machine-readable contracts instead of relying on prose-only release notes.

Design/data runtime schemas extend that machine-readable envelope across
composition packages, context menus, coverage gates, cross-target 3D scene
editing, animation timelines, visual effects, style resources, shader/material
editing, custom designers, data connection failover, dataset design, lookup
editors, offline replay, query previews, relationship navigation, replication,
published resources, schema adapters, service contracts, SQL safety, stored
procedure workflows, database-backed form column guards, deployment scaling,
desktop sync snapshots, device API components, diagnostics, documentation, ERP
coverage, event-processing defaults, finance gates, and form-designer evidence.
These contracts let IDEs and external agents validate visual and data-heavy app
composition without opening generated source projects.

Generated frontend/component runtime schemas mirror the authoring contracts in
the generated application surface. They cover frontend release parity and
quality, generated app shell chrome, generated binding lifecycle/runtime
contracts, generated component analog and behavior workbenches, component
design surfaces, drag/drop handler wiring, editor-family manifests, event
dispatch, package lifecycle and dependency evidence, palette registration,
parity runtime manifests, render/runtime/serialization contracts, target
adapters, and usability workbenches. This keeps generated UI packages
contract-validatable after code generation instead of treating them as opaque
frontend artifacts.

Generated visual/data/mobile runtime schemas continue the generated-app mirror
for cross-target scene authoring, animation timelines, effects, shader/material
editing, visual runtime replay, custom designers, data connection and service
manifests, dataset and relationship lookup replay, data-tooling operations,
design-time package management, device API replay matrices, form-stream
round-trips, handler source round-trips, generated object-inspector workflows,
generated binding workbenches, local database maintenance, and mobile lifecycle
delivery. Generated applications can therefore prove visual, database-backed,
inspector, and mobile behavior through contract payloads after packaging.

Mobile/native/IDE runtime schemas extend schema-backed evidence across generated
mobile device APIs, native bridge errors, permission workflows, simulator
replays, privacy/store manifests, generated native form and runtime operation
manifests, generated language/runtime workbench contracts, platform parity,
property editors, visual runtime assets, wizard manifests, generation job
queues, handler cross-calls, HTTPS/i18n/identity gates, IDE capability matrices,
object-inspector workflows, integration workbenches, capability-superiority
evidence, livebinding operations, local database maintenance, manufacturing and
media gates, menus, microservice packaging, migration plans, and mobile
background delivery. This keeps native, IDE, integration, and deployment-facing
tooling evidence first-class in the generated contract catalog.

Studio generation queues are executable lifecycle contracts, not passive backlog
records. `appgen.package-generation-job.v1` must identify a deterministic
`job_id`, runnable status, current stage, lifecycle states through queued,
generated, verified, and packaged, target list, changed source paths, quality
gates, required artifacts, release-evidence formats, commands, and blocking
gaps. `appgen.package-generation-queue.v1` must aggregate those jobs with job,
runnable, blocked, command, status, stage, artifact, evidence, and blocking-gap
counters. The `studio_generation_queue_lifecycle` tooling-audit gate fails when
the Studio exposes a planned-only generation record, omits `run_generation`,
`open_artifacts`, or `rerun_quality`, drops package/release evidence, or embeds
a generation queue in `appgen.package-studio-workspace.v1` that cannot be run.
The same gate also exercises the Studio runner: validation must emit
`appgen.validate-report.v1`, source generation must emit
`appgen.generate-report.v1` with generated artifacts, and release packaging must
emit `appgen.release-verifier-report.v1`, `appgen.release-evidence-bundle.v1`,
and target package manifests before the queue can be treated as runnable.
Generated applications inherit the same runnable semantics through
`appgen.generation-job.v1` and `appgen.generation-job-queue.v1`: generated Studio
modules must expose queued runnable jobs, stage/gate/artifact/evidence counters,
required commands, zero blocking gaps, and queue health that release gates can
consume directly.

Remaining non-PBC runtime schemas complete the schema-backed runtime inventory for mobile offline/background flows, monitoring, native packaging, natural-language evolution, package management, platform release evidence, operations workbenches, reports, resilience, schema tooling, security, source intake, UI customization, visual runtime verification, wizarding, and database/search deployment plans. This tranche intentionally excludes active PBC package contracts and the unsupported-schema sentinel. The promoted formats are: `appgen.mobile-background-resume-operation.v1`, `appgen.mobile-background-resume-workflow.v1`, `appgen.mobile-component-adapter-contract.v1`, `appgen.mobile-deep-link-routing-contract.v1`, `appgen.mobile-device-capability-lifecycle-replay.v1`, `appgen.mobile-device-component-spec-contract.v1`, `appgen.mobile-device-designer-transaction-replay-contract.v1`, `appgen.mobile-device-event-trace-contract.v1`, `appgen.mobile-device-scenario-matrix-contract.v1`, `appgen.mobile-device-simulator-contract.v1`, `appgen.mobile-device-target-scenario-matrix-contract.v1`, `appgen.mobile-dispatch-adapter-operation.v1`, `appgen.mobile-media-file-pipeline-contract.v1`, `appgen.mobile-native-api-actionable-operations.v1`, `appgen.mobile-native-api-contract.v1`, `appgen.mobile-native-api-readiness-contract.v1`, `appgen.mobile-native-api-runtime-replay-contract.v1`, `appgen.mobile-native-api-workbench.v1`, `appgen.mobile-native-bridge-error-contract.v1`, `appgen.mobile-native-bridge-matrix-contract.v1`, `appgen.mobile-native-call-transaction-replay.v1`, `appgen.mobile-offline-device-event-queue-contract.v1`, `appgen.mobile-offline-replay.v1`, `appgen.mobile-offline-sync-batch.v1`, `appgen.mobile-permission-manifest-contract.v1`, `appgen.mobile-permission-prompt-workflow.v1`, `appgen.mobile-permission-revocation-contract.v1`, `appgen.mobile-permission-revocation-transaction-replay.v1`, `appgen.mobile-permission-state-machine-contract.v1`, `appgen.mobile-platform-fallback-operation.v1`, `appgen.mobile-platform-fallback-workflow.v1`, `appgen.mobile-privacy-review-operation.v1`, `appgen.mobile-privacy-review-workflow.v1`, `appgen.mobile-replay-simulator-operation.v1`, `appgen.mobile-request-permission-operation.v1`, `appgen.mobile-run-device-scenario-operation.v1`, `appgen.mobile-simulator-fixture-integrity-contract.v1`, `appgen.mobile-simulator-replay-workflow.v1`, `appgen.mobile-store-privacy-manifest-contract.v1`, `appgen.mobile-sync-conflict.v1`, `appgen.mobile-validate-device-component-operation.v1`, `appgen.monitoring-release-gate.v1`, `appgen.monitoring-workbench.v1`, `appgen.native-package-artifact-gate.v1`, `appgen.native-packager-execution-plan.v1`, `appgen.native-packaging-release-gate.v1`, `appgen.native-release-gate.v1`, `appgen.nl-changeset.v1`, `appgen.nl-destructive-intent.v1`, `appgen.nl-evolution-capabilities.v1`, `appgen.nl-evolution-changeset.v1`, `appgen.nl-evolution-module-contract.v1`, `appgen.nl-evolution-module-file-manifest.v1`, `appgen.nl-evolution-module-generated-test-smoke.v1`, `appgen.nl-evolution-module-manifest.v1`, `appgen.nl-evolution-module-operation.v1`, `appgen.nl-evolution-module-release-context.v1`, `appgen.nl-evolution-module-smoke-test.v1`, `appgen.nl-evolution-module-test-file-manifest.v1`, `appgen.nl-evolution-plan.v1`, `appgen.nl-evolution-release-gate.v1`, `appgen.nl-evolution-workbench.v1`, `appgen.nl-generation-smoke-audit.v1`, `appgen.nl-migration-impact.v1`, `appgen.nl-rollback-plan.v1`, `appgen.nl-test-plan.v1`, `appgen.node-red-release-gate.v1`, `appgen.node-red-workbench.v1`, `appgen.notification-check.v1`, `appgen.notification-release-gate.v1`, `appgen.notification-workbench.v1`, `appgen.object-inspector-contract.v1`, `appgen.object-inspector-readiness-contract.v1`, `appgen.object-inspector-workbench.v1`, `appgen.offline-conflict-review-contract.v1`, `appgen.onprem-readiness.v1`, `appgen.openapi-release-gate.v1`, `appgen.openapi-workbench.v1`, `appgen.ops-generation-smoke-audit.v1`, `appgen.package-application-management.v1`, `appgen.package-authorization-decision.v1`, `appgen.package-compliance-contract.v1`, `appgen.package-database-design-workspace.v1`, `appgen.package-database-ops-contract.v1`, `appgen.package-deployment-contract.v1`, `appgen.package-dsl-editor-state.v1`, `appgen.package-form-canvas.v1`, `appgen.package-form-design-validation.v1`, `appgen.package-form-design.v1`, `appgen.package-form-drop-proposal.v1`, `appgen.package-form-property-inspector.v1`, `appgen.package-generation-job.v1`, `appgen.package-generation-queue.v1`, `appgen.package-manager-module-replay-matrix.v1`, `appgen.package-node-red-contract.v1`, `appgen.package-report-delivery.v1`, `appgen.package-search-contract.v1`, `appgen.package-secret-exposure-scan.v1`, `appgen.package-security-audit-event.v1`, `appgen.package-session-hardening-policy.v1`, `appgen.package-source-artifact-contract.v1`, `appgen.package-source-generation-plan.v1`, `appgen.package-source-generation-smoke-audit.v1`, `appgen.package-source-intake-matrix.v1`, `appgen.package-source-intake.v1`, `appgen.package-studio-workspace.v1`, `appgen.package-tenant-rls-contract.v1`, `appgen.packaging-release-gate.v1`, `appgen.packaging-workbench.v1`, `appgen.palette-balance.v1`, `appgen.patroni-cluster-plan.v1`, `appgen.performance-release-gate.v1`, `appgen.performance-workbench.v1`, `appgen.platform-module-file-manifest.v1`, `appgen.platform-module-test-file-manifest.v1`, `appgen.platform-parity-lifecycle-replay.v1`, `appgen.platform-parity-requirement-audit.v1`, `appgen.platform-release-gate.v1`, `appgen.platform-target-experience-gate.v1`, `appgen.postgraphile-schema-plan.v1`, `appgen.privacy-request.v1`, `appgen.productivity-release-gate.v1`, `appgen.productivity-workbench.v1`, `appgen.project-management-module-file-manifest.v1`, `appgen.project-management-module-test-file-manifest.v1`, `appgen.project-management-release-gate.v1`, `appgen.project-management-workbench.v1`, `appgen.property-editor-family-contract.v1`, `appgen.prototyping-module-contract.v1`, `appgen.prototyping-module-file-manifest.v1`, `appgen.prototyping-module-generated-test-smoke.v1`, `appgen.prototyping-module-manifest.v1`, `appgen.prototyping-module-operation.v1`, `appgen.prototyping-module-release-context.v1`, `appgen.prototyping-module-smoke-test.v1`, `appgen.prototyping-module-test-file-manifest.v1`, `appgen.prototyping-release-gate.v1`, `appgen.prototyping-workbench.v1`, `appgen.pwa-installability-matrix.v1`, `appgen.pwa-module-file-manifest.v1`, `appgen.pwa-module-test-file-manifest.v1`, `appgen.pwa-release-gate.v1`, `appgen.rad-data-tooling-contract.v1`, `appgen.rad-data-tooling-workbench.v1`, `appgen.rad-parity-workbench.v1`, `appgen.rad-query-designer-contract.v1`, `appgen.realtime-module-file-manifest.v1`, `appgen.realtime-module-test-file-manifest.v1`, `appgen.realtime-release-gate.v1`, `appgen.realtime-workbench.v1`, `appgen.release-promotion-plan.v1`, `appgen.report-delivery-release-gate.v1`, `appgen.reporting-generation-smoke-audit.v1`, `appgen.reports-release-gate.v1`, `appgen.reports-workbench.v1`, `appgen.resilience-release-gate.v1`, `appgen.resilience-workbench.v1`, `appgen.responsive-workbench.v1`, `appgen.retention-disposition-review.v1`, `appgen.rls-release-gate.v1`, `appgen.rls-workbench.v1`, `appgen.roadmap-source-report.v1`, `appgen.rpa-module-file-manifest.v1`, `appgen.rpa-module-test-file-manifest.v1`, `appgen.rpa-release-gate.v1`, `appgen.rpa-workbench.v1`, `appgen.rules-release-gate.v1`, `appgen.rules-workbench.v1`, `appgen.runtime-assurance-workbench.v1`, `appgen.runtime-assurance.v1`, `appgen.runtime-security-release-gate.v1`, `appgen.runtime-security-workbench.v1`, `appgen.schema-diagram-release-gate.v1`, `appgen.schema-diff.v1`, `appgen.schema-import-apply-plan.v1`, `appgen.schema-import-release-gate.v1`, `appgen.schema-normalization.v1`, `appgen.schema-refactor-plan.v1`, `appgen.schema-roundtrip-diff.v1`, `appgen.schema-source-contract.v1`, `appgen.schema-source-example-audit.v1`, `appgen.schema-source-fidelity.v1`, `appgen.schema-source-generation-proof.v1`, `appgen.schema-source-profile.v1`, `appgen.schema-source-validation.v1`, `appgen.sdk-release-gate.v1`, `appgen.sdk-workbench.v1`, `appgen.search-release-gate.v1`, `appgen.search-workbench.v1`, `appgen.security-generation-smoke-audit.v1`, `appgen.seed-plan.v1`, `appgen.seed-release-gate.v1`, `appgen.seed-workbench.v1`, `appgen.seed.v1`, `appgen.semantic-model-wrapper.v1`, `appgen.service-mesh-policy.v1`, `appgen.service-traffic-shift.v1`, `appgen.source-intake-workspace.v1`, `appgen.splash-screen.v1`, `appgen.sql-explain-plan.v1`, `appgen.sql-filter-plan.v1`, `appgen.sql-select-builder.v1`, `appgen.sql-workbench.v1`, `appgen.studio-browser-smoke.v1`, `appgen.studio-generation-smoke-audit.v1`, `appgen.studio-module-contract.v1`, `appgen.studio-module-file-manifest.v1`, `appgen.studio-module-generated-test-smoke.v1`, `appgen.studio-module-manifest.v1`, `appgen.studio-module-operation.v1`, `appgen.studio-module-release-context.v1`, `appgen.studio-module-smoke-test.v1`, `appgen.studio-module-test-file-manifest.v1`, `appgen.studio-release-gate.v1`, `appgen.subject-export.v1`, `appgen.support-bundle.v1`, `appgen.support-center-module-contract.v1`, `appgen.support-center-module-file-manifest.v1`, `appgen.support-center-module-generated-test-smoke.v1`, `appgen.support-center-module-manifest.v1`, `appgen.support-center-module-operation.v1`, `appgen.support-center-module-release-context.v1`, `appgen.support-center-module-smoke-test.v1`, `appgen.support-center-module-test-file-manifest.v1`, `appgen.support-center-release-gate.v1`, `appgen.support-center-workbench.v1`, `appgen.tabbed-view-module-contract.v1`, `appgen.tabbed-view-module-file-manifest.v1`, `appgen.tabbed-view-module-generated-test-smoke.v1`, `appgen.tabbed-view-module-manifest.v1`, `appgen.tabbed-view-module-operation.v1`, `appgen.tabbed-view-module-release-context.v1`, `appgen.tabbed-view-module-smoke-test.v1`, `appgen.tabbed-view-module-test-file-manifest.v1`, `appgen.tabbed-views-release-gate.v1`, `appgen.tabbed-views-workbench.v1`, `appgen.target-experience-matrix.v1`, `appgen.target-package-matrix.v1`, `appgen.tenancy-release-gate.v1`, `appgen.tenancy-workbench.v1`, `appgen.text-quality-check.v1`, `appgen.text-quality-release-gate.v1`, `appgen.text-quality-workbench.v1`, `appgen.theme-quality.v1`, `appgen.third-party-component-import-contract.v1`, `appgen.third-party-component-install-plan.v1`, `appgen.trusted-header-plan.v1`, `appgen.ui-chrome-readiness-contract.v1`, `appgen.ui-customization-workbench.v1`, `appgen.ui-experience-excellence-gate.v1`, `appgen.ui-experience-release-gate.v1`, `appgen.ui-validation.v1`, `appgen.unknown-diagnostic-fixture.v1`, `appgen.usage-analytics-release-gate.v1`, `appgen.usage-analytics-workbench.v1`, `appgen.validation-release-gate.v1`, `appgen.validation-result.v1`, `appgen.version-control-module-file-manifest.v1`, `appgen.version-control-module-replay-matrix.v1`, `appgen.version-control-module-test-file-manifest.v1`, `appgen.version-control-release-gate.v1`, `appgen.version-control-workbench.v1`, `appgen.view-composition-module-file-manifest.v1`, `appgen.view-composition-module-replay-matrix.v1`, `appgen.view-composition-module-test-file-manifest.v1`, `appgen.view-composition-release-gate.v1`, `appgen.view-composition-workbench.v1`, `appgen.view-empty-state.v1`, `appgen.view-error-state.v1`, `appgen.view-experience-module-contract.v1`, `appgen.view-experience-module-file-manifest.v1`, `appgen.view-experience-module-generated-test-smoke.v1`, `appgen.view-experience-module-manifest.v1`, `appgen.view-experience-module-operation.v1`, `appgen.view-experience-module-release-context.v1`, `appgen.view-experience-module-smoke-test.v1`, `appgen.view-experience-module-test-file-manifest.v1`, `appgen.view-experience-release-gate.v1`, `appgen.view-experience-workbench.v1`, `appgen.view-loading-state.v1`, `appgen.view-shell.v1`, `appgen.view-state-matrix.v1`, `appgen.visual-component-design-tools.v1`, `appgen.visual-component-generated-test-smoke.v1`, `appgen.visual-component-operation-steps.v1`, `appgen.visual-component-prop-validation.v1`, `appgen.visual-component-render-node.v1`, `appgen.visual-component-scenario.v1`, `appgen.visual-component-smoke-test.v1`, `appgen.visual-component-spec.v1`, `appgen.visual-component-validation-steps.v1`, `appgen.visual-design-ide-operation-steps.v1`, `appgen.visual-design-ide-operation.v1`, `appgen.visual-design-ide-replay-matrix.v1`, `appgen.visual-design-ide-runtime-context.v1`, `appgen.visual-design-ide-surface-manifest.v1`, `appgen.visual-design-ide-validation-steps.v1`, `appgen.visual-experience-quality.v1`, `appgen.visual-modeling-release-gate.v1`, `appgen.visual-modeling-workbench.v1`, `appgen.visual-regression.v1`, `appgen.visual-runtime-pipeline-manifest.v1`, `appgen.visual-runtime-pipeline-operation-steps.v1`, `appgen.visual-runtime-pipeline-operation.v1`, `appgen.visual-runtime-pipeline-replay-matrix.v1`, `appgen.visual-runtime-pipeline-validation-steps.v1`, `appgen.visual-test-matrix.v1`, `appgen.visualization-workbench.v1`, `appgen.voice-release-gate.v1`, `appgen.voice-workbench.v1`, `appgen.wizard-release-gate.v1`, `appgen.wizard-session.v1`, `appgen.wizard-submission-plan.v1`, `appgen.wizard-workbench.v1`, `appgen.zombodb-index-plan.v1`.

PBC runtime schemas complete the generated and packaged PBC evidence surface without hard-coding any specific business capability into the language. `appgen contract-schema` exports and sample-validates generated PBC runtime manifests, package discovery and metadata validation, registration plans, service/schema contracts, implementation and release audits, catalog/topology reports, natural-language selection, source packages, source artifact evidence, lifecycle documentation, runtime test coverage, and table-stakes evidence. The promoted formats are: `appgen.generated-pbc-composition-runtime-workbench.v1`, `appgen.generated-pbc-package-discovery-plan.v1`, `appgen.generated-pbc-package-metadata-validation.v1`, `appgen.generated-pbc-package-metadata.v1`, `appgen.generated-pbc-registration-plan.v1`, `appgen.generated-pbc-release-evidence.v1`, `appgen.generated-pbc-runtime-manifest.v1`, `appgen.generated-pbc-runtime-smoke.v1`, `appgen.generated-pbc-runtime-validation.v1`, `appgen.generated-pbc-schema-contract.v1`, `appgen.generated-pbc-service-contract.v1`, `appgen.implemented-pbc-capability-audit.v1`, `appgen.pbc-advanced-runtime-evidence.v1`, `appgen.pbc-agent-capability-contract.v1`, `appgen.pbc-agent-capability-release-audit.v1`, `appgen.pbc-catalog-report.v1`, `appgen.pbc-composition-plan.v1`, `appgen.pbc-domain-functionality-contract.v1`, `appgen.pbc-eventing-choice-lint.v1`, `appgen.pbc-generation-smoke-audit.v1`, `appgen.pbc-implementation-contract.v1`, `appgen.pbc-implementation-release-audit.v1`, `appgen.pbc-lifecycle-documentation-audit.v1`, `appgen.pbc-manifest-schema.v1`, `appgen.pbc-manifest-validation.v1`, `appgen.pbc-natural-language-selection.v1`, `appgen.pbc-package-contract.v1`, `appgen.pbc-package-discovery-report.v1`, `appgen.pbc-package-index-discovery-report.v1`, `appgen.pbc-package-index-schema.v1`, `appgen.pbc-package-loading-smoke-audit.v1`, `appgen.pbc-package-local-assurance-audit.v1`, `appgen.pbc-package-local-assurance-contract.v1`, `appgen.pbc-registration-plan.v1`, `appgen.pbc-release-audit.v1`, `appgen.pbc-source-artifact-contract.v1`, `appgen.pbc-source-artifact-release-audit.v1`, `appgen.pbc-source-package.v1`, `appgen.pbc-source-runtime-test-coverage-audit.v1`, `appgen.pbc-specification-contract.v1`, `appgen.pbc-specification-manifest-traceability.v1`, `appgen.pbc-specification-release-audit.v1`, `appgen.pbc-table-stakes-evidence.v1`, and `appgen.pbc-topology-report.v1`.

The optional positional format selects one schema from the catalog. Unknown
schema names return the same `appgen.contract-schema-catalog.v1` envelope with
`ok: false`, a named `missing_requested_schema_formats` entry, and exit code
`1`, so callers can distinguish an unsupported contract name from a malformed
CLI invocation. Text mode prints `contract-schema ...`, one `schema ...` line
per selected contract, and named `missing-schema ...` lines without falling back
to raw JSON.

`appgen.contract-schema-cli-audit.v1` proves the schema catalog command in
catalog JSON, single-schema JSON, missing-schema JSON, and text modes. It
reports required, available, and missing schema formats; required/observed case
ids; expected and observed exit codes; expected and observed payload formats;
semantic-model required fields; representative payload validation counts;
required text markers; and text JSON-fallback status. The representative
payload validation pass validates live report payloads for every required schema
format, including formatter write-mode, validation, generation, graph, explain,
LSP, designer-sync, Studio bridge, Studio browser-smoke, frontend bridge,
diagnostic, parser-golden, drift, migration, natural-language, release,
component-publish, doctor, schema-catalog, and validation-report
payloads. The aggregate `contract_schema_cli_contracts` gate fails when any core
schema disappears, the CLI stops exposing a selected semantic-model schema, a
missing schema no longer returns a controlled contract payload, representative
payload validation fails for any required format, or human-readable schema
output loses its named markers.

### `appgen contract-validate`

```console
appgen contract-validate semantic.json --json
appgen contract-validate semantic.json --format appgen.semantic-model.v1 --json
appgen contract-validate semantic.json
```

`appgen contract-validate` validates a machine-readable tooling payload against
the JSON Schema contracts exported by `appgen contract-schema`. When `--format`
is omitted, the command infers the schema from the payload's `format` field. The
command returns `appgen.contract-validation-report.v1` with the selected schema
format, the observed payload format, whether the schema was available, whether
the payload format was inferred, normalized diagnostics, and grouped counts for
missing required fields, type errors, constant mismatches, enum mismatches, and
pattern mismatches.

Validation is intentionally dependency-light so coding agents and small local
models can run it without installing a separate JSON Schema engine. It enforces
the schema subset emitted by the platform catalog: object/array/string/boolean/
integer/number/null types, `required`, `properties`, `items`, local `$defs`
references, `const`, `enum`, `pattern`, and `minimum`. Unknown schema names,
payloads with no inferrable format, malformed JSON, and missing required fields
return the same report format with `ok: false` and exit code `1`.

`appgen.contract-validation-cli-audit.v1` proves valid inferred JSON,
self-validation of `appgen.contract-validation-report.v1`, valid explicit JSON,
missing-required-field JSON, unknown-schema JSON, malformed JSON, and text modes.
It reports required/observed case ids, expected/observed exit codes,
expected/observed payload formats, required text markers, text JSON-fallback
status, the validated payload/schema format pair, self-report validation
formats, missing-field error counts, unknown-schema availability, and
malformed-JSON diagnostic counts.
The aggregate `contract_validation_cli_contracts` gate fails when contract
validation stops rejecting broken payloads, exits with the wrong process status,
falls back to raw JSON in text mode, or loses the stable markers external agents
use to decide whether a generated contract is safe to consume.

### `appgen runtime-contracts`

```console
appgen runtime-contracts --json
appgen runtime-contracts
```

Inventories `appgen.*.v1` runtime envelopes across top-level package modules
outside the active PBC implementation tree. The command returns
`appgen.runtime-contract-inventory.v1` with module-level format lists,
documented format counts, schema-promoted format counts, and explicit
unpromoted/undocumented format lists. The inventory is now a blocking
completion gate for non-PBC top-level runtime contracts: actionable
`unpromoted_runtime_formats` and `undocumented_runtime_formats` must both be
empty. The only allowed non-schema runtime literal is the controlled
missing-schema sentinel `appgen.missing-contract.v1`, reported separately in
`sentinel_runtime_formats` so contract-schema negative tests do not look like
real implementation backlog.

Text mode prints the inventory envelope format, runtime format count,
schema-promoted count, documented count, unpromoted count, undocumented count,
sentinel count, module count, controlled sentinel names, and any actionable
unpromoted/undocumented format names. JSON remains the authoritative handoff.

`appgen.runtime-contract-inventory-cli-audit.v1` proves JSON and text modes for
this command. The aggregate tooling audit exposes it through
`runtime_contract_inventory_contracts`, which fails if the inventory command
stops scanning package modules, stops skipping PBC paths, loses text markers,
falls back to raw JSON, leaves an actionable non-PBC schema/documentation
backlog, or loses the controlled missing-schema sentinel.
`appgen.tooling-doc-language-audit.v1` guards the same policy in this document:
the runtime-contracts section must say zero-actionable-backlog, name
`sentinel_runtime_formats`, name `appgen.missing-contract.v1`, and avoid stale
phrases that describe the runtime inventory as a larger or intentionally
non-blocking backlog.

### `appgen semantic`

```console
appgen semantic app.appgen
appgen semantic app.appgen --json
appgen semantic src/appgen --json
```

`appgen semantic` emits the shared `appgen.semantic-model.v1` contract directly.
When the input path is a directory it loads all nested `.appgen` files as one
source set, resolves cross-file references, and reports
`appgen.semantic-source-set.v1` metadata. Text mode prints a compact summary
with source mode, file count, symbol count, table/view counts, diagnostic count,
every source file, per-file symbol counts, symbol-coverage totals, and semantic
contract counts. JSON mode is the full machine contract for IDEs, CI, graphing,
release verification, and agentic application editing.

### `appgen lint`

```console
appgen lint app.appgen
appgen lint app.appgen --json
appgen lint src/appgen --strict --catalog docs/pbc-catalog.json
appgen lint app.appgen --previous-semantic previous-semantic.json --json
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
diagnostics instead of a Python traceback; text mode prints
`internal-error failed: format=appgen.internal-error.v1` with the `AGX9000`
code, error type, and message.
Argparse usage/configuration failures remain exit code `2`. Missing
user-supplied input paths are treated as configuration errors and return exit
code `2` before the tooling engine reads or generates artifacts; the executable
missing-input audit covers lint, semantic, format, validate, graph, graph-suite, explain,
generate, migration-plan, nl-plan, lsp, verify, package, designer-sync, drift,
previous-semantic baseline paths, and component-catalog paths. The audit also
proves these failures emit no stdout payload, so agents do not mistake a usage
failure for a partial tooling report. Invalid enumerated options, including
graph kind, graph output format, database backend, release target, and PBC
publication catalog choices, are also rejected by argparse with exit code `2`.

The executable CLI contract tests cover JSON schemas, default text summaries,
success and failure exit codes, and argparse usage failures for invalid choices
or missing required options. The help-surface audit also proves discoverability
for linter semantic-baseline flags, generator target flags, graph formats,
migration backends and rename hints, language-service rename/code-action flags,
release package targets, designer-sync edits, and diagnostics/golden/drift
audit commands. The default `appgen lint` text output renders the
`appgen.lint-report.v1` envelope format and stage counts in the report's
published `stage_names` order, currently syntax, semantic, and policy
diagnostics, source file names as `source-file ...`, and when
`--previous-semantic` is provided it also prints a
migration-preview summary with the embedded `appgen.migration-plan.v1` format
as `format=...`, backend as `backend=...`, approval flag, change count, and
detected migration families.
`appgen.lint-text-renderer.v1` is embedded in the tooling audit to prove lint
text logs preserve source mode, file count, source file names, ordered stage
counts, migration preview metadata, detected migration families, and diagnostic
lines without JSON parsing. Its contract reports required-fragment,
missing-fragment, output-line, and marker-line counts so release evidence can
distinguish complete text coverage from a partially rendered summary.
It also reports source-file-line, stage-line, migration-line,
migration-preview-line, migration-detected-line, diagnostic-line, error-line,
and warning-line counts so lint release logs prove source coverage, stage
coverage, migration preview evidence, and diagnostic severity visibility. It
also publishes required and emitted source files, stage names, detected
migration families, diagnostic codes, and diagnostic severities with named
missing lists for each family, so a partially rendered lint summary fails by the
exact hidden source, stage, migration family, code, or severity.
The same text-renderer contract publishes required, emitted, missing, and
missing-count evidence for text surfaces, embedded contract formats, source
modes, migration backends, approval markers, and exact stage-count markers.
The aggregate lint CLI gate requires zero named missing entries, so a generic
`source-file`, `stages`, `migration-preview`, or diagnostic line cannot mask a
lost directory mode, backend, approval posture, or stage separation summary.
`appgen diagnostics`
text output summarizes the `appgen.diagnostic-catalog.v1` format in the header,
registry coverage, required registry codes as `required-code ...`, covered
fixture codes as `covered-fixture-code ...`, and fixture gaps; `appgen diagnostics --audit-fixtures`
summarizes the `appgen.diagnostic-fixture-audit.v1` format in the header plus
covered diagnostic codes as `covered-code ...` lines and missing diagnostic
codes as `missing-code ...` lines. `appgen.diagnostics-text-renderer.v1` is embedded in the
tooling audit to prove both diagnostic text summaries keep required-code,
covered-fixture, missing-code, and blocking-gap evidence visible without JSON
parsing. The renderer contract reports summary-line, required-code-line,
covered-fixture-line, covered-code-line, missing-code-line, and
blocking-gap-line counts so diagnostic release logs prove catalog coverage,
fixture coverage, missing diagnostic coverage, and blocking fixture gaps. It
also reports required and emitted code lists for required registry codes,
covered fixture codes, fixture-audit covered codes, fixture-audit missing codes,
and blocking-gap ids, with named missing lists for each family.
The same renderer publishes required, emitted, missing, and missing-count
evidence for diagnostic text surfaces and embedded diagnostic contract formats.
The aggregate diagnostic gate requires zero named missing entries, so generic
diagnostic line counts cannot mask a hidden catalog summary, fixture summary,
code family, blocking-gap line, or format marker.
The aggregate tooling audit exposes this proof independently as
`diagnostic_catalog_fixture_contracts`. That gate fails when required AGX codes
lose fixture coverage, diagnostic shape or severity enforcement regresses, docs
links disappear from the registry, text output hides catalog or fixture markers,
or any named code or blocking fixture gap stops being visible in release logs.
`appgen drift`
summarizes the
`appgen.semantic-drift-audit.v1` format, semantic-model format as
`semantic_format=...`, drift surfaces,
evidence formats, blocking gap count, named blocking gaps as `gap ...`, digest,
and per-surface checks.
`appgen.semantic-drift-text-renderer.v1` is embedded in the tooling audit to
prove those shared-model drift summaries keep surface, evidence, named-gap,
digest, and check-result markers visible without JSON parsing. The diagnostics
and drift renderer contracts also report required-fragment, missing-fragment,
output-line, and marker-line counts for their human-readable evidence.
The drift renderer additionally reports summary-line, surface-line, gap-line,
evidence-line, check-line, passing-check-line, failing-check-line, and
digest-line counts so shared semantic-model release logs prove surface coverage,
evidence references, named gaps, check outcomes, and digest identity.

### `appgen format`

```console
appgen format app.appgen --check
appgen format app.appgen --write
appgen format app.appgen --json
```

`--check` exits `1` when formatting changes are needed.
`--write` rewrites the source file when the formatted text differs and the JSON
payload reports `write_requested`, `written`, and `write_path` so IDEs and CI can
distinguish a preview from an actual file mutation. The default text output
also reports the formatter report format in the header, `organize`, `write_requested`,
`written`, and `write_path` when a write occurs.
`appgen.format-text-renderer.v1` is embedded in the tooling audit to prove
format text logs preserve the formatter envelope, idempotence state,
organize/write flags, write path, and diagnostic lines without JSON parsing.
The format text contract reports fragment and marker counts for the formatter
header, mutation posture, write path, and diagnostic markers. It also reports
summary-line, write-path-line, diagnostic-line, warning-line, error-line,
write-flag-line, idempotence-line, and organize-line counts so formatter text
logs prove mutation posture, write status, idempotence, organize mode, and
diagnostics remain visible. It also publishes required and emitted write paths,
write-requested values, written values, organize values, idempotence states,
diagnostic codes, and diagnostic severities with named missing lists, so
formatter release logs fail on the exact hidden mutation or diagnostic marker.
The formatter text gate also publishes required, emitted, missing, and
missing-count evidence for text surfaces, embedded formatter contract formats,
and mutation states. The aggregate formatter gate requires zero named missing
entries, so a generic formatter header or warning line cannot hide a missing
write path, write flag, organize flag, idempotence state, mutation state, or
contract marker.
`--organize` enables the optional table-body organization profile: identity
fields and spreads, business keys, relationships, editable scalar fields,
calculated fields, audit fields, and directives are ordered inside each table
without reordering top-level declarations. The format write audit reports this
as `organize_table_body_order` so the release evidence names the applied
categories instead of only recording byte offsets. It also reports total and
passing scenario counts, failing scenario counts, scenario ids, failing
scenario ids, blocking-gap counts, write-mode counts, check-mode counts, and
organize category counts across dirty-check, clean-check, organize, JSON-write,
and text-write scenarios.
The aggregate tooling audit exposes this proof independently as
`formatter_write_organize_contracts`. That gate fails when formatter
idempotence, comment preservation, modifier ordering, check/write exit
semantics, write metadata, table-body organization categories, diagnostics, or
human-readable format markers regress.

### `appgen validate`

```console
appgen validate app.appgen --targets web,mobile,desktop --json
```

Runs lint plus generator-readiness checks without writing generated code.
Requested `--targets` are normalized with the same platform target policy as
the app declaration. Validation fails with `AGX0802` when a requested target is
unknown or is not declared by `app ... { targets: ... }`, and the
`appgen.validate-report.v1` payload includes `requested_targets`, `app_targets`,
requested/app target counts, check and passing-check counts, blocking-check
counts, diagnostic counts, target-diagnostic counts, and a
`target_compatibility` check. The default text output prints requested
targets, app-declared targets, the `appgen.validate-report.v1` envelope format
in the header, semantic-model format as `semantic_format=...`, checks, missing or unknown target details,
and diagnostics. `appgen.validate-generate-text-renderer.v1` is embedded in
the tooling audit to prove validation and generation text logs keep target,
semantic-model, diagnostic, artifact, manifest, and blocking-gap evidence
visible without JSON parsing. Its renderer contract reports fragment and marker
counts across both validation and generation summaries so target failures,
artifacts, manifests, gaps, and diagnostics are measurable in release logs. It
also reports summary-line, check-line, passing-check-line, failing-check-line,
target-detail-line, artifact-line, manifest-line, gap-line, diagnostic-line,
warning-line, and error-line counts so release triage can identify whether
validation checks, target mismatch details, generated handoff artifacts, or
diagnostics disappeared from text output. It also publishes required and emitted
requested targets, app targets, generated targets, validation check ids,
passing/failing check ids, unknown/missing targets, artifact paths, manifest
paths, blocking-gap ids, diagnostic codes, and diagnostic severities with named
missing lists, so validation and generation release logs fail on the exact
hidden target, check, artifact, manifest, gap, or diagnostic marker.
The same renderer publishes required, emitted, missing, and missing-count
evidence for text surfaces, validate/generate contract formats, semantic-model
formats, validate and generate statuses, generated flags, output directories,
and artifact size markers. The aggregate validation and generation gates
require zero named missing entries, so a generic summary, artifact, manifest,
gap, or diagnostic line cannot hide a lost semantic contract, generated flag,
output directory, or handoff artifact size.
The aggregate tooling audit exposes validation readiness independently as
`validate_target_contracts`. That gate fails when target normalization,
`target_compatibility`, `AGX0802` target diagnostics, or validate text markers
for requested/app targets disappear.

### `appgen generate`

```console
appgen generate app.appgen --out generated/app
appgen generate app.appgen --target web --target mobile --out generated/app
```

Generation fails before writing artifacts when lint has errors. Lint warnings
also block generation by default; `--allow-warnings` permits warning-only
sources and does not permit errors. The default text output prints requested or
resolved targets, artifact count, the `appgen.generate-report.v1` envelope
format in the header, semantic-model format as `semantic_format=...`, output directory, manifest path,
artifact paths, artifact byte counts when summaries provide them as
`artifact ... bytes=...`, blocking gaps, and diagnostics.
Generated reports publish `artifact_count`, `manifest_exists`,
`diagnostic_count`, and `blocking_gap_count` at the top level so release
evidence can prove generation readiness without expanding artifact arrays or
nested validation payloads.
`appgen.validate-generate-cli-audit.v1` proves the successful generation path
hands off resolved targets, output directory, semantic-model format, validation
report format, manifest existence, manifest app name, artifact count, and
artifact path existence, while still proving warning-only sources require
`--allow-warnings` and lint errors block generation even with that flag. The
audit reports total, passing, failing, validation, and generation case counts
so release evidence can distinguish target-validation coverage from
artifact-generation coverage. It also reports case ids, failing case ids,
generation success cases, generation blocked cases, validation rejection cases,
manifest case counts, existing-manifest case counts, artifact handoff case
counts, artifact-path case counts, artifact-path-missing counts, blocked-output
absence counts, payload-format counts, generated blocking-gap names, and
blocking-gap case counts so agents can review generation readiness without
expanding every case.
It also reports required, observed, and missing case ids plus expected and
observed payload formats by case, expected and observed exit codes by case, and
per-case `ok` status, so validation and generation scenarios cannot disappear,
drift report envelope formats, return the wrong process status, or pass with
false-positive aggregate case and payload counts.
The aggregate tooling audit exposes generation handoff independently as
`generate_artifact_policy_contracts`. That gate fails when successful
generation stops writing manifests/artifacts, warning-only sources stop blocking
by default, `--allow-warnings` stops permitting warning-only generation, lint
errors become generatable, or generate text logs lose artifact, manifest,
blocking-gap, or diagnostic markers.

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
the same semantic model. Text mode prints both the required graph kind names and
the supported output format names, plus the `appgen.graph-suite-report.v1`
envelope format, so release logs remain reviewable without parsing JSON.
Every individual graph command emits `appgen.graph-report.v1`, whose nested
`graph` object is one of the schema-backed graph contracts:
`appgen.graph.er.v1`, `appgen.graph.lookup.v1`,
`appgen.graph.workflow.v1`, `appgen.graph.handler.v1`,
`appgen.graph.pbc.v1`, `appgen.graph.security.v1`,
`appgen.graph.agent.v1`, `appgen.graph.deployment.v1`, or
`appgen.graph.package.v1`. This lets IDE previews, release packages, and
external agents validate graph payloads directly instead of trusting only the
aggregate graph-suite envelope.
The workflow graph models more than state-to-state transitions: human tasks,
timers, and compensation directives become graph nodes with labeled edges for
assignment, timer expiry, and rollback execution. Workflow designers can render
review queues, escalation paths, and compensation operations from the same
`appgen.graph.workflow.v1` contract used by release evidence.
`appgen.graph-suite-cli-audit.v1` reports `rendering_formats_by_kind` and
`missing_renderings` so CI can prove every required graph kind has JSON,
Mermaid, and DOT renderings rather than relying on a count alone. It also
reports expected rendering count, present rendering count, complete rendering
kind count, missing format count, and named text-fragment ids so graph-suite
regressions reveal whether the JSON rendering matrix or human release markers
failed.
`appgen.graph-cli-format-audit.v1` reports case, passing-case, failing-case,
case-id, failing-case, covered-kind, missing-required-kind, covered-format,
JSON-case, Mermaid-case, DOT-case, payload-format, and text-marker counts
across every required graph kind, so graph release evidence captures both
individual CLI examples and full graph breadth. It also reports required,
observed, and missing case ids; expected and observed exit codes by case; case
`ok` status by case; expected and observed output formats by case; expected and
observed JSON payload formats by case; required plus missing Mermaid/DOT text
markers by case; and raw-JSON fallback status for text graph cases. This makes a
missing documented graph example, a format drift, a JSON payload envelope
regression, a text-renderer marker regression, a wrong process status, or a text
mode JSON fallback fail by name rather than only changing an aggregate count.
The graph-suite CLI audit reports required, observed, and missing JSON/text
mode case ids; expected and observed modes; expected and observed exit codes;
per-mode `ok` status; expected and observed JSON payload formats; text-mode
raw-JSON fallback status; required-kind, missing-required-kind, output-format,
missing-rendering, text-fragment, and missing-text-fragment counts. CI can
therefore prove JSON and text release logs preserve the same graph contract
markers and that neither mode silently regressed behind aggregate rendering
counts.
The in-process `appgen.graph-suite-report.v1` also reports required, present,
and missing graph-kind counts; format, graph-report, rendering,
expected-rendering, missing-rendering, diagnostic, check, passing-check, and
blocking-gap counts; and the exact missing kind/rendering lists, so release
evidence can prove graph breadth without expanding every rendered graph body.
`appgen.graph-explain-text-renderer.v1` is embedded in the tooling audit to
prove graph-suite and explain logs keep graph kind, graph format, check,
symbol, diagnostic-doc, and handler-edge evidence visible without JSON parsing.
Its contract reports required-fragment, missing-fragment, output-line, and
marker-line counts across graph-suite, symbol, diagnostic, and handler summaries.
It also publishes required and emitted graph kinds, graph formats, graph check
ids, symbol ids, diagnostic codes, diagnostic docs URLs, and handler edges with
named missing lists, so graph/explain release logs fail on the exact hidden
review marker.
The same renderer publishes required, emitted, missing, and missing-count
evidence for graph/explain text surfaces, embedded graph-suite and explain
report formats, explain kinds, symbol reference count markers, and handler
match count markers. The aggregate explain gate requires zero named missing
entries, so generic graph or explain lines cannot mask a hidden symbol detail,
diagnostic docs link, handler edge, report format, or navigation count.
The aggregate tooling audit exposes graph rendering as its own
`graph_rendering_contracts` gate. It fails independently when a required graph
kind is missing, JSON/Mermaid/DOT renderings drift, graph CLI cases fail, or
graph CLI named case/format/payload/text-marker contracts or graph-suite text
markers disappear.

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
Default explanations print the `appgen.explain-report.v1` envelope format.
Default symbol explanations print the resolved symbol id, kind, parent, and
reference count. Default diagnostic explanations print the diagnostic code,
title, summary, and documentation anchor. Default handler explanations print
matching handler edges. `appgen.explain-cli-audit.v1` proves the symbol,
diagnostic, and handler text modes all include the same `format=...` envelope
marker as JSON mode, so release logs and agents can identify explain contracts
without parsing prose. The audit also reports total, text, JSON, and
report-format-covered case counts plus passing-case, exit-failure,
missing-report-format, symbol-case, diagnostic-case, and handler-case counts so
release evidence can prove all six explain modes remain covered. It also
reports failing-case names, case ids, text and JSON report-format counts,
navigation-detail case names, and symbol, diagnostic, and handler navigation
detail counts so explain regressions identify the exact missing mode or
navigational payload. It also reports required, observed, and missing case ids;
expected and observed output modes by case; expected and observed exit codes by
case; case `ok` status by case; expected and observed JSON payload formats by
case; required and missing report-format case names; required and missing
text-mode markers; text JSON-fallback status by case; and required versus
missing navigation-detail cases, so a missing explain example, text/JSON mode
drift, wrong process status, lost JSON envelope, raw JSON fallback in text mode,
lost envelope marker, or lost navigation payload fails by name. JSON mode also
reports `symbol_id`, `symbol_kind`,
`symbol_parent`, `symbol_reference_count`, `diagnostic_title`,
`diagnostic_docs_url`, `handler_match_count`, and `handler_edges` from JSON
mode so CLI release evidence carries the same navigational details as IDE
integrations.
The aggregate tooling audit exposes explain behavior as
`explain_cli_contracts`, which fails independently when symbol, diagnostic, or
handler text/JSON modes lose the `appgen.explain-report.v1` marker, named text
markers, navigation details, output-mode contracts, exit-code contracts, JSON
payload envelopes, text-mode non-JSON output, or graph/explain text renderer
evidence.

### `appgen doctor`

Checks parser generation, Python package imports, catalog availability, template
paths, generator backends, and optional IDE/LSP dependencies. The doctor report
also embeds the CLI alias contract and a VS Code extension surface check so the
short command alias, editor scaffold, command palette entries, language
configuration, syntax grammar, and LSP provider registrations are verified from
the same command used in CI. The default text output prints the doctor report
format, total check count, blocking gap count, each check status, and embedded
audit formats as `detail_format=...` markers for parser-golden, completion
coverage, semantic and LSP symbol coverage, CLI alias contract, module
boundaries, designer sync, and extension audits.
`appgen.doctor-text-renderer.v1` is embedded in the tooling audit to prove
doctor text logs keep check status, blocking-gap counts, and embedded
`detail_format=...` evidence visible without JSON parsing. The renderer
contract also reports required-fragment, check-line, and detail-format-line
counts so release evidence can prove the text summary preserved every expected
status and embedded audit marker. It also reports required, emitted, and missing
doctor check ids plus required and emitted detail formats by check, so a missing
doctor readiness check or embedded audit marker fails by name instead of only
changing an aggregate line count.
The same renderer publishes required, emitted, missing, and missing-count
evidence for doctor check outcomes, text surfaces, and report formats. The
aggregate doctor gate requires zero named missing entries, so a generic
`detail_format=...` line cannot mask a hidden summary, blocking-gap marker,
failed-check outcome, or embedded readiness report.
`appgen.doctor-cli-audit.v1` separately invokes `appgen doctor --json` and
`appgen doctor` text mode. It reports required, observed, and missing mode case
ids; expected and observed output modes; expected and observed exit codes;
per-case `ok` status; expected and observed JSON payload formats; required and
observed doctor check ids; required and observed embedded detail formats by
check; required and missing text markers by case; blocking-gap counts; and
text-mode raw-JSON fallback status. The aggregate doctor gate requires every
named gap list to be empty, so the executable command cannot drift away from the
in-process doctor report or hide failed CLI dispatch behind a green renderer
contract.
The aggregate tooling audit exposes this proof independently as
`doctor_cli_text_contracts`. That gate fails when doctor stops proving parser,
package import, catalog, template writer, backend, semantic-model, alias, LSP,
Studio, or editor-extension readiness, or when text output hides embedded audit
format markers, named doctor checks, JSON payload envelopes, exit-code
contracts, or text-mode non-JSON output.

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
prose or scattered manual checks. The default text output reports pass count,
the top-level `appgen.tooling-audit.v1` envelope format, blocking gap count,
named blocking gaps as `blocking-gap ...`, covered documentation sections,
source-of-truth document, and embedded report formats for each check so release
logs remain useful without requiring JSON parsing. The report embeds
`appgen.tooling-doc-anchor-audit.v1`, which proves every emitted
`docs/tooling.md#...` section reference resolves to a real heading anchor in
this document. The same audit extracts every `appgen.*.v1` contract format
named in this document and reports missing runtime or test references, so a
documented contract cannot silently drift into prose-only status. It also
publishes a per-format reference matrix with documentation, runtime, and test
reference counts, covered runtime/test format counts, missing-reference gap
counts, and minimum runtime/test reference counts so release reviewers can see
which exact contract format lost implementation or test provenance. The audit
renderer also embeds `appgen.tooling-section-coverage-audit.v1` through the
`tooling_section_coverage_contracts` gate, proving every major `##` section and
every concrete `###` subsection in this specification has at least one executable
audit gate.
`appgen tooling-docs` exposes these documentation governance checks directly as
`appgen.tooling-docs-audit.v1`, embedding both the anchor audit and the section
coverage audit so CI can distinguish missing anchors, missing major sections,
missing subsections, runtime format reference gaps, and test reference gaps.
The text
renderer must include embedded audit format names such as
`appgen.non-goal-policy-audit.v1` and
`appgen.tooling-doc-anchor-audit.v1` so policy and documentation-link gates are
visible in human release logs. `appgen.tooling-audit-text-renderer.v1` proves
the human-readable renderer itself keeps the top-level envelope, sections,
embedded report formats, source document, blocking-gap count, named blocking
gaps, and
implementation-phase marker visible without requiring the full audit to run,
including the explicitly called-out non-goal policy and documentation-anchor
audit format markers.
Its contract reports fragment and marker counts for top-level summaries, source
markers, section markers, embedded format markers, check lines, blocking gaps,
and implementation-phase evidence. It also reports check-line,
passing-check-line, failing-check-line, detail-format-line, section-line,
blocking-gap-line, and implementation-phase-line counts so release triage can
see whether a human log lost checks, sections, embedded audit formats, or
failure markers. The same renderer contract publishes required, emitted, and
missing check ids, section anchors, embedded detail formats, and blocking-gap ids,
and the aggregate `tooling_audit_text_renderer` gate fails if any named release
log marker is missing.
It also publishes required, emitted, missing, and missing-count evidence for
text surfaces, status markers, top-level audit formats, source documents, and
implementation-phase markers. The aggregate gate requires zero named missing
entries, so generic audit summary lines cannot mask a hidden source marker,
failed-audit status, top-level format, or phase exit-criteria marker.
When implementation-phase evidence is present, the text output also reports the
number of audited phases, missing phase count, passing/total exit-criterion
counts, missing exit-criterion count, and the
`appgen.tooling-implementation-phase-audit.v1` format marker.
The implementation-phase audit reports phase ids, phase counts, passing-phase
counts, exit-criterion ids, exit-criterion counts, passing-exit-criterion
counts, passing-exit-criterion ids, per-phase exit-criterion counts, per-phase
passing ids and counts, per-phase missing counts, missing-phase counts,
missing-exit-criterion counts, missing-exit-criteria grouped by phase, and
evidence-format maps for each criterion so completion claims can be reviewed
without expanding every nested criterion.

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
The web package manifest carries explicit verifier booleans for application
build contract, route declaration, valid generated form bindings, handler target
resolution, smoke-test declaration, and the `web.smoke` handoff entrypoint so
web builders do not infer readiness from generic artifact names.
`appgen.package-verify-cli-audit.v1` exercises `appgen verify --target all` and
`appgen package --target all --out ...`, then proves that release evidence and
per-target manifests exist for web, mobile, desktop, PBC, and deployment
handoffs. The audit checks target-specific handoff metadata rather than only
successful command exit codes, so downstream builders receive stable contracts
for routes/forms/handlers, mobile signing/offline launch, desktop installer and
startup assets, PBC publication, and deployment topology verification.
It reports case, passing-case, target, manifest, and handoff-artifact counts so
release evidence captures breadth across all package targets instead of only a
single success boolean. It also reports failing-case names, case ids, expected
targets, required/observed/missing case ids, expected and observed exit codes by
case, expected and observed release-verifier payload formats by case, per-case
`ok` status, manifest target coverage, missing manifest targets, manifest
formats, handoff counts by target, release-evidence report counts, missing
release reports, and release graph kind/format gaps so package failures identify
the missing target handoff directly.
For package handoff artifacts, the audit reports required, emitted, and missing
artifact names by target. This prevents a package from passing because it has
the right number of handoff entries while omitting a named contract such as
`desktop.context_menus`, `mobile.smoke_launch`, or
`deployment.topology_graph`.
It also publishes a target readiness matrix for web, mobile, desktop, PBC, and
deployment handoffs, including the named readiness checks for smoke entrypoints,
signing/offline posture, installer/startup metadata, PBC registration, and
deployment topology. The aggregate `package_manifest_handoff_contracts` gate
fails when any required handoff artifact or readiness check is missing and
reports the exact `target.artifact_name` and `target.check_name` gaps.
The default text output for both `appgen verify` and `appgen package` summarizes
the release verifier report format, selected targets, written artifacts,
the `appgen.release-evidence-bundle.v1` bundle format and
`appgen.graph-suite-report.v1` graph-suite evidence as `format=...` markers,
graph-suite kinds as `graph-kinds ...`, graph-suite rendering formats as
`graph-formats ...`, per-target verifier status, blocking gaps, and artifact paths;
`--json` remains the complete machine-readable report.
When `--out` writes the release evidence artifact, the file envelope is
`appgen.release-evidence-file.v1`. It contains the evidence bundle, target
checks, and target reports in a stable machine contract so CI systems can
validate the written artifact directly instead of trusting only the package
command response.
The JSON report also publishes target, check, passing-check, failing-check,
report, diagnostic, graph-kind, graph-format, evidence-artifact, and
written-artifact counts at the top level, and each target verifier publishes
check, passing-check, and blocking-gap counts. Agents and release gates should
use these counts to prove package breadth before expanding target-specific
handoff details.
`appgen.release-verifier-text-renderer.v1` is embedded in the tooling audit to
prove those human-readable handoff logs keep the envelope, evidence bundle,
graph-suite kind/format, per-target status, blocking-gap, and artifact markers
without depending on JSON parsing.
The renderer contract reports fragment and marker counts for release, graph,
verifier, blocking-gap, and artifact lines. It also reports release-line,
graph-line, target-status-line, passing-target-line, failing-target-line,
blocking-gap-line, and artifact-line counts so release logs can prove package
handoff evidence did not lose target status, graph-suite context, or written
artifact paths.
It also reports required, emitted, and missing marker families for release
envelope markers, graph-suite markers, target statuses, blocking gaps, and
artifact markers. This keeps the check specific enough to fail when, for
example, the desktop target line or a named package artifact disappears even if
the total line count still looks plausible.
The same renderer also publishes named required, emitted, missing, and
missing-count evidence for text surfaces, embedded contract formats, graph
kinds, graph output formats, target outcomes, and artifact paths. The aggregate
release-text and implementation-phase gates require zero named missing entries,
so a release log cannot pass by printing generic graph, target, or artifact
lines that omit a required target outcome, graph format, or package handoff
path.
The aggregate tooling audit also exposes package handoff and release text as
separate gates. `package_manifest_handoff_contracts` proves the written web,
mobile, desktop, PBC, and deployment manifests carry target-specific handoff
metadata, graph-suite evidence, and downstream-builder readiness booleans.
`appgen.package-invalid-target-audit.v1` is the negative package-target
contract: it proves unsupported package targets fail with the expected
diagnostic shape and cannot silently produce partial handoff artifacts.
`release_text_evidence_contracts` proves the human release log retains release,
graph-suite, target-status, blocking-gap, and artifact markers without falling
back to raw JSON, and fails if any required marker family reports missing named
entries.

### `appgen component-publish`

```console
appgen component-publish --component CustomGauge --catalog components.json --json
```

Prepares a reusable visual-component catalog publication plan without mutating
the catalog file. The command emits `appgen.component-publish-report.v1` with a
side-effect-free `appgen.component-catalog-patch.v1`, existing catalog component
names when a catalog path is supplied, the upsert target, and explicit
`side_effect_free`/`write_performed` evidence. This command is the non-PBC
publication lane for components used by strict linting and visual designers.
Without `--json`, the command prints the component name, catalog source,
registration state, side-effect-free flag, write-performed flag, existing
catalog component names as `catalog-existing ...`, the
`appgen.component-publish-report.v1` envelope format, catalog patch format, and
before/after catalog counts.
`appgen.component-publish-text-renderer.v1` is embedded in the tooling audit to
prove this human-readable component publication log remains side-effect-aware
and exposes the catalog patch contract plus existing-catalog context without
parsing JSON.
`appgen.component-publish-cli-audit.v1` is the executable CLI contract for that
surface. It validates JSON, text, and missing-catalog modes, requires the
published report and catalog patch envelopes to remain named, and keeps
component publication usable by coding agents without scraping prose.
The renderer contract reports fragment and marker counts for the component
summary, catalog metadata, side-effect posture, and patch contract. It also
reports summary-line, catalog-line, side-effect-line, patch-contract-line, and
existing-catalog-line counts so component publication logs prove catalog
context and non-mutating publication posture did not disappear. It also reports
required and emitted catalog sources, side-effect values, write-performed
values, patch formats, and existing catalog component names with named missing
lists, so the release gate fails on the exact hidden publication marker.
The same contract now publishes required, emitted, missing, and missing-count
evidence for text surfaces, embedded report/patch contract formats,
registration-state values, and before/after/existing catalog count markers.
The aggregate component-publish gate requires zero named missing entries, so a
generic catalog or side-effect line cannot hide a missing patch contract,
registration state, or catalog-count transition.
The aggregate tooling audit exposes this proof independently as
`component_publish_catalog_contracts`. That gate fails when
`appgen component-publish` stops returning an `appgen.component-catalog-patch.v1`
upsert plan, stops deriving component icons, mutates catalogs implicitly, hides
existing catalog context in text mode, or accepts a missing catalog path without
a blocking gap. The CLI audit publishes named case ids, failing-case counts,
missing-catalog exit status, missing-catalog blocking gaps, and side-effect
markers for the rejected missing-catalog path so the release gate proves even
failure paths remain non-mutating.
It also reports required, observed, and missing case ids; required and missing
text markers; expected and observed exit codes by case; per-case `ok` status;
and required versus observed missing-catalog blocking gaps. The aggregate gate
fails if a JSON/text/missing-catalog case disappears, returns the wrong process
status, silently fails its own case proof, if the human log loses a side-effect
or catalog marker, or if the rejected missing catalog path stops naming
`catalog_path_readable`.

### `appgen pbc`

```console
appgen pbc list
appgen pbc verify src/pyAppGen/pbcs/gl_core
appgen pbc publish src/pyAppGen/pbcs/gl_core --catalog local
```

PBC commands operate on manifests and package directories, not grammar changes.
`list --json` emits `appgen.pbc-verifier-catalog.v1`, a schema-backed catalog
contract containing the selectable key, health, label, mesh, and datastore
backend for each registered PBC. Agents use this contract to discover
composable capabilities before planning an application instead of scraping
human CLI text or hard-coding a built-in PBC list.
`publish` emits `appgen.pbc-publish-report.v1`; it loads the package
entrypoint, validates the manifest, proves the manifest is publishable, returns
the catalog patch, attaches release-evidence verification, and records that the
publish plan is side-effect-free. Catalog writes are an explicit downstream
step, not an implicit CLI side effect. Without `--json`, `list` prints the
catalog report format, total count, mesh counts, and each selectable PBC key;
`verify` prints the verifier format, selected PBC key, check count, blocking gap
count, catalog metadata, and per-check status. `appgen.pbc-cli-text-audit.v1`
is embedded in the tooling audit to prove the text output is not a raw JSON
fallback.
`appgen.pbc-publish-text-renderer.v1` is also embedded in the tooling audit to
prove publish text logs expose the target catalog mode, catalog path as
`catalog_path ...`, side-effect-free flag, write-performed flag, catalog patch
entries as `catalog-patch ...`, and per-check publication status without
loading a package during renderer verification or parsing JSON.
The aggregate tooling audit exposes this proof independently as
`pbc_publish_side_effect_contracts`. That gate fails when PBC list/verify text
falls back to JSON, publish stops attaching `appgen.pbc-package-verifier.v1`
release evidence, catalog publication stops being side-effect-free, file
catalog paths or catalog patches disappear from text output, or any PBC publish
check reports a blocking gap.
The same schema catalog exports `appgen.pbc-package-load-report.v1` and
`appgen.pbc-publish-cli-audit.v1`, so agent runners can validate package-load,
publish CLI, release-evidence, and catalog-patch envelopes without expanding
the full aggregate audit.

### `appgen nl-plan`

```console
appgen nl-plan app.appgen --prompt "Add credit memos to accounts receivable" --json
```

Produces a proposed DSL diff, lint report, migration preview, and test plan. It
must not write generated code unless the DSL diff validates. Without `--json`,
the command prints a concise text summary with intent, operation count, patch
size, generated test count, token-budget note count, operation kinds,
`appgen.nl-plan.v1` format, lint report format/status as a `format=...` marker,
and migration-preview format/backend/status as `format=...` and `backend=...`
markers so agents can inspect the plan without parsing the full JSON payload.

## Language Server Specification

The language server should use the same parser, semantic model, diagnostics,
formatter, and graph builders as the CLI.

The executable launch path is:

```bash
appgen lsp --stdio
```

`--stdio` starts the JSON-RPC language server over standard input/output. It
accepts `initialize`, `shutdown`, `exit`, `textDocument/didOpen`,
`textDocument/didChange`, `textDocument/didSave`, `textDocument/didClose`,
completion, hover, definition, references, document
symbols, prepare-rename, rename, code actions, formatting, and workspace symbol
requests. The
server keeps an in-memory document cache for open `.appgen` buffers and
publishes diagnostics after open/change/save notifications using the same
`appgen.semantic-model.v1` and linter reports as the CLI. Workspace symbol,
definition, reference, and completion requests scan each open DSL document
individually instead of concatenating files, so editor features keep working
when an application is split across multiple `.appgen` files. Rename uses the
active document for identifier validation and migration safety, then returns a
workspace edit that updates the matching identifier across every open DSL
document. Prepare-rename returns the exact code-identifier range, placeholder,
symbol metadata, and lexical scope before the edit is offered, and returns
`null` for comments, string literals, or unknown symbols. Close notifications
remove the document from the in-memory workspace and publish an empty diagnostic
set so editors clear stale errors immediately.

The executable tooling audit includes `appgen.lsp-stdio-transport-audit.v1`,
which sends real `Content-Length` JSON-RPC frames through the stdio transport
and verifies initialize, diagnostics publication, shutdown, and exit handling.
The JSON-RPC audit reports check, passing-check, provider, enabled-provider,
missing-provider, request-check, passing-request-check, code-action,
formatting-edit, and blocking-gap counts plus provider names, missing provider
names, and request-check ids so release evidence proves the language server
surface is broad enough for editor and agent workflows rather than merely
returning an initialize response. The same JSON-RPC audit checks the documented
LSP method matrix. For every method in the capabilities table, it
reports the method name, provider/notification source, advertised status,
exercised status, backing check id, passing method count, and missing method
count. The aggregate `lsp_transport_rpc_contracts` gate fails if any documented
method is not both advertised where applicable and exercised by the JSON-RPC
audit.
The same audit now carries a named editor-lifecycle workflow contract that
executes initialize, open diagnostics, completion, hover, definition,
references, document symbols, prepare-rename, rename, changed-buffer
diagnostics, code actions, formatting, save diagnostics, close/diagnostic clearing, workspace symbol
search, shutdown, and exit as one continuous
session. It reports required/observed/missing case ids, expected/observed
methods by case, expected/observed result shapes by case, failing cases,
diagnostic-transition status, and shutdown/exit status. The aggregate transport
gate requires all of those named gaps to be empty, so the IDE path cannot pass by
testing isolated requests while the actual editing lifecycle is broken.
The lifecycle audit also proves the advertised semantic cache. `didOpen`,
`didChange`, and `didSave` refresh a versioned semantic/diagnostic cache;
document-symbol and workspace-symbol requests reuse that cached semantic model;
`didClose` removes the cached document and clears diagnostics. The JSON-RPC
audit reports cache document, refresh, hit, miss, revision, version, diagnostic,
and symbol counts, and includes a `semantic_cache_lifecycle` check so the server
cannot claim `full-document-with-semantic-cache` while only storing raw text.
It also checks
`workspace_document_scan_and_rename`, which opens multiple DSL buffers and
proves definition, references, completion, workspace symbol, and rename
requests resolve across open documents without concatenating source files.
It also promotes lexical reference-scope evidence into the aggregate navigation
gate: expected code-reference line counts, matched line counts, excluded
comment/string match counts, and the exact expected/excluded line sets are
reported so a reference request cannot silently degrade into broad text search.
The stdio audit reports request-message, response, id-response, notification,
method, diagnostic-publication, total-message, notification-message,
expected-id, missing-response-id, completion-response, workspace-symbol-response,
changed-source, changed-diagnostic, changed-error, changed-diagnostic-code, and
shutdown-response counts so framed transport coverage remains measurable
separately from in-process JSON-RPC handling. The changed-diagnostic evidence is
required so `didChange` cannot pass by only echoing a publish notification; it
must prove that the in-memory buffer was updated and re-linted through the
shared semantic model.
Without `--json`, `appgen lsp <file>` prints a concise service summary with
the `appgen.lsp-service.v1` envelope format, semantic-model format as
`semantic_format=...`, diagnostic
count, completion count, code-action count, document-symbol count,
workspace-symbol count, source-of-truth contract, hover evidence, completion
coverage format as a `format=...` marker and missing-source count, definition
contract format/status, reference contract format/location count, formatting
contract format/edit count, and rename status when a rename is requested.
`appgen.lsp-service-text-renderer.v1` is embedded in the tooling audit to prove
those editor-service summaries keep diagnostics, completions, actions, symbols,
source-of-truth, service-count summaries, navigation, formatting, hover content
as `hover ...`, completion coverage gaps as `completion-missing ...`, and rename
safety markers visible without JSON parsing. The contract also reports
summary-line, service-count-line, source-line, completion-line,
completion-missing-line, navigation-line, formatting-line, rename-line,
rename-blocker-line, hover-summary-line, and hover-line counts so text-mode
regressions identify the missing service surface directly.
Those counts are backed by named evidence, not accepted on their own. The
renderer publishes required, emitted, missing, and missing-count fields for
text surfaces (`service_counts`, `source_of_truth`, completion coverage and
missing-source markers, definition, references, formatting, rename,
rename-blocker, hover summary, and hover content), embedded editor contract
formats, navigation surfaces, completion gaps, hover items, rename blocker
codes, and rename fix ids. The aggregate
`lsp_navigation_completion_contracts` gate fails unless every named list has
zero missing entries, so a renderer cannot satisfy the release audit by printing
an unrelated line with the right prefix.
The JSON service payload also carries `service_counts` with diagnostic,
completion, required/detected/missing completion-source, hover-content,
reference, document-symbol, LSP symbol-coverage, code-action, formatting-edit,
workspace-symbol, and rename-edit counts. `appgen.completion-coverage.v1`
carries matching required/detected/missing source counts, total completion label
count, and label counts by source so agents can prove completion breadth
without walking every nested completion item. `appgen.lsp-symbol-coverage.v1`
proves every required semantic symbol kind also appears in both document-symbol
and workspace-symbol LSP surfaces, so editor navigation cannot silently lag
behind the semantic model.
The renderer contract reports fragment and marker counts for service, coverage,
navigation, definition, reference, formatting, rename, blocker, and hover lines.
The aggregate tooling audit exposes two narrower language-server gates in
addition to `language_server_core_features`. `lsp_transport_rpc_contracts`
proves JSON-RPC provider breadth and stdio `Content-Length` framing, including
diagnostics publication, completion, workspace-symbol, and shutdown responses.
The stdio transport audit publishes expected and observed response ids by
method, required and observed notification methods, required diagnostic-code
families for changed/saved buffers, and close-diagnostic clearing counts. The
transport gate requires the named missing method, notification, diagnostic-family,
and close-clearing lists to be empty, so initialize, completion,
workspace-symbol, shutdown, save/close lifecycle, and diagnostics regressions
fail by method name rather than only by aggregate response counts.
`lsp_navigation_completion_contracts` proves completion coverage, LSP symbol
coverage, lexical reference scoping, definition/reference text markers,
navigation, formatting, hover, and text-summary evidence remain complete and
reviewable.
Rename text output includes the `appgen.lsp-rename.v1` contract format, whether
the rename was blocked, blocker count, the nested `appgen.migration-plan.v1`
migration-preview as `migration_format=...`, and whether that migration preview
requires explicit approval. When a rename is blocked, text output also prints
each blocker code and available fix id, including `AGX1101` and
`add_rename_hint`, so agents and editor logs can surface the exact safe next
step without parsing JSON. Rename edits operate on code identifiers, not raw
text: comments and string literals must remain unchanged, and the rename report
must expose the lexical scope plus occurrence counts so editors and agents can
distinguish a symbol refactor from a broad textual replacement. Operation and
workflow renames are scoped to declarations plus handler/transition targets, so
same-named fields or unrelated declarations are not rewritten by a refactor.
Table renames produce the same scoped candidate edit for table declarations,
database-backed view subjects, relationship targets, and report sources while
preserving same-named fields and non-code text; because table renames can imply
schema migration risk, the candidate may still be blocked by migration safety
until an explicit rename hint or migration decision is supplied.
View renames produce scoped candidate edits for view declarations and menu item
navigation targets while preserving same-named fields, operation targets,
comments, and string literals; if the surrounding migration/safety preview is
ambiguous, the candidate remains visible but blocked.
Field renames are table-scoped: they update the owning table declaration,
calculated-field expressions in that table, and database-backed view bindings or
component placements for views over that table. They preserve same-named fields
on other tables, handler targets, lookup-path leaf names, operation names,
comments, and string literals. Field rename candidates are still routed through
the migration safety gate, so inferred rename candidates that need an explicit
hint remain visible but blocked.
Enterprise-surface renames are also scoped. PBC key renames update PBC
declarations, composition includes, composition connection endpoints, and
deployment unit/health/resource/env targets that deploy the PBC while preserving
same-named fields and non-code evidence. Event and API contract renames update
contract declarations and composition/API references while preserving
same-named operations and handlers. Package renames update package declarations
without rewriting evidence text. Deployment-unit renames update the unit plus
its health, resource, and environment declarations while preserving the
operation or PBC declaration that the unit points at.
The rename CLI audit publishes required and observed scenario ids, required and
observed execution modes, and required and observed lexical scopes for every
safe or blocked refactor scenario. The language-server gate requires the named
missing scenario, mode, and scope lists to be empty, so deleting a table, field,
view, operation, workflow, PBC, event, package, or deployment-unit rename
scenario cannot hide behind aggregate scenario counts.

### Capabilities

| LSP Feature | Required Behavior |
| --- | --- |
| `textDocument/didOpen`, `didChange`, `didSave`, and `didClose` | Incrementally parse, rebuild affected semantic model parts, publish diagnostics, and clear diagnostics when a buffer closes. |
| `textDocument/completion` | Complete keywords, block-local directives, table names, fields, lookup paths, components, handler events, operation targets, flow states, workflow directive snippets, PBC keys, APIs, events, package targets, deployment units, LLM providers, and agent skills. |
| `textDocument/hover` | Show keyword docs, symbol summary, field type, relationship target, lookup resolution, handler target, PBC catalog metadata, and diagnostic explanation. |
| `textDocument/definition` | Navigate from references to declarations for fields, tables, views, flows, operations, roles, PBCs, APIs, events, packages, and deployment units. |
| `textDocument/references` | Find all references across workspace DSL files and generated contract indexes. |
| `textDocument/documentSymbol` | Return hierarchical outline: app, tables, fields, views, sections, components, handlers, flows, operations, PBCs, packages, deployment. |
| `textDocument/prepareRename` | Return the exact renameable identifier range, placeholder, symbol metadata, and lexical scope; reject comments, string literals, and unknown symbols before a workspace edit is offered. |
| `textDocument/rename` | Rename symbols safely and update references; block unsafe renames when migration impact is ambiguous. |
| `textDocument/codeAction` | Offer quick fixes for missing declarations, typo suggestions, create operation from handler, create event contract, add lookup directive, add permission, remove secret literal, and remove invalid stream/runtime picker fields. |
| `textDocument/formatting` | Call the shared formatter. |
| `workspace/symbol` | Search declarations by name, kind, and catalog metadata. |

Document-symbol outline depth is executable. View symbols include child
`view_section`, `component_binding`, and `handler` entries so IDE outline trees
can navigate form layout sections, dropped components, and event wiring without
reparsing view bodies.
Flow symbols include child `flow_state`, `human_task`, `timer`, and
`compensation` entries so workflow designers can navigate transitions, human
work queues, escalation timers, and rollback logic from the same outline tree.
Symbol-surface coverage is executable through `appgen.lsp-symbol-coverage.v1`.
The language service includes this report as `symbolCoverage`, and
`appgen doctor --json` checks `lsp_symbol_coverage` against a fixture that
exercises tables, fields, groups, enums, views, handlers, flows, workflow
states, human tasks, timers, compensation, roles, permissions, rules, LLMs,
agents, PBCs, composition, APIs, events, jobs, reports, menus, component
contracts, packages, tests, deployments, audits, versions, and security blocks.

Hover depth is executable. Hovering a registered PBC key returns
`appgen.lsp-pbc-hover.v1` metadata with label, mesh, datastore profile, and
sample API/event contracts. Hovering a symbol that participates in a diagnostic
returns the diagnostic code plus the same explanation object used by
`appgen explain --diagnostic`, so IDEs and agents can show the cause and docs
target without duplicating diagnostic registries. Relationship fields expose
`appgen.lsp-relationship-hover.v1` target-table metadata, and database-backed
lookup paths expose `appgen.lsp-lookup-hover.v1` resolution chains. The JSON-RPC
audit checks this as `hover_relationship_lookup_depth`, so field relationship
and lookup hover regressions fail the tooling release gate. Handler target
hover emits `appgen.lsp-handler-target-hover.v1` with owner, event, target,
target kind, target symbol id, and handler-graph edge metadata; the JSON-RPC
audit checks this as `hover_handler_target_depth`.
The same JSON-RPC audit reports named hover surfaces for PBC catalog metadata,
diagnostic explanations, relationship fields, lookup paths, and handler targets
through `required_hover_surfaces`, `observed_hover_surfaces`,
`missing_hover_surfaces`, and `hover_surface_checks`. The aggregate
`lsp_navigation_completion_contracts` gate requires all five hover surfaces to
be observed with zero named missing surfaces, so hover coverage cannot regress
while the generic hover provider still returns a response.

Workspace symbol search includes catalog-backed results. In addition to open
DSL declarations, `workspace/symbol` returns `catalog://pbc/...` locations for
registered PBCs and their API/event contracts when the query matches PBC names,
labels, mesh metadata, descriptions, or contract names. This lets editors and
agents discover selectable PBCs without hard-coding the catalog into grammar
rules.
The JSON-RPC audit reports this as `workspace_symbol_catalog_result_depth`,
including catalog query names, passing/missing query counts, PBC result counts,
contract result counts, catalog URI sets, PBC keys, and contract names. The
aggregate `lsp_navigation_completion_contracts` gate requires the catalog PBC
query and catalog contract query to both pass, so catalog-backed discovery does
not silently fall back to ordinary workspace-only symbols.
Definition navigation uses the same catalog location scheme for registered PBC
keys and API/event contract tokens, so `textDocument/definition` can jump from
composition references to read-only catalog declarations as well as to ordinary
DSL declarations.
For ordinary DSL declarations, definition is context-aware: a token used as an
API/event contract target or deployment health/resource/env target resolves to
the event or deployment-unit declaration even when an operation or field has the
same name.
The JSON-RPC audit reports this through `enterprise_definition_context` with
named contexts for PBC includes, API/event targets, deployment health targets,
deployment resource targets, and deployment environment targets. It publishes
expected line numbers, observed line numbers, passing/missing context counts,
and missing context names, and the aggregate `lsp_navigation_completion_contracts`
gate requires all definition contexts to resolve to their intended declarations.
Reference search also includes those read-only catalog indexes. When a user or
agent asks for references to a PBC key or catalog API/event contract,
`textDocument/references` returns ordinary workspace occurrences plus the
matching `catalog://pbc/...` index location, which keeps generated PBC contracts
discoverable without making catalog entries look like editable DSL source.
The JSON-RPC audit reports this as `reference_catalog_index_depth`, with
separate workspace and catalog counts for PBC-key references and event-contract
references. The aggregate `lsp_navigation_completion_contracts` gate requires
both the editable workspace occurrence and the read-only catalog index
occurrence for each reference family, so generated catalog references remain
discoverable without being confused with editable DSL source.
Reference locations are lexical code references: comments, string literals, and
block comments are preserved as authoring evidence and must not be returned as
symbol references.

Rename safety is an executable gate. The language service still returns the
candidate workspace edit and migration preview, but `textDocument/rename`
returns `ok: false` with an `AGX1101` blocker when the preview requires
explicit migration approval, such as destructive relationship changes. The
blocker includes an `add_rename_hint` fix suggestion so agents and IDEs can ask
for an explicit migration decision before applying the edit. The
`appgen.lsp-rename-cli-audit.v1` gate also exercises lexical-scope safety by
renaming handler, table, and view targets while proving matching names in fields,
operations, comments, and string literals are preserved. It publishes expected
and observed exit codes by scenario, JSON service-envelope formats by scenario,
and per-scenario `ok` status so safe and blocked rename paths cannot pass through
aggregate scope counts alone.

### Completion Sources

Completions should be context-aware:

- top-level: language constructs such as `table`, `view`, `flow`, `pbc`,
  `composition`, `deploy`, `agent`;
- table body: field snippets, directives, relationship targets, group spreads;
- view body: table fields, lookup paths, component names, handler snippets;
- flow body: state names, `human`, `timer`, and `compensate` directive snippets,
  operation targets;
- composition body: registered PBC keys, versions, APIs, events, commands;
- deploy body: declared units, target kinds, health/check/resource snippets;
- agent body: LLM names, operation targets, permission subjects.

Completion coverage is executable through `appgen.completion-coverage.v1`.
The language service includes this report as `completionCoverage`, and
`appgen doctor --json` checks `lsp_completion_coverage` against a fixture that
exercises keywords, snippets, table names, fields, lookup paths, components,
handler events, operation targets, flow states, workflow directive snippets, PBC
keys, aggregate PBC contracts, explicit PBC APIs, PBC events, PBC command-style
contracts, package targets, deployment units, LLM providers, and agent skills.
JSON-RPC completion requests must also report the detected cursor context and
filter labels to the relevant completion family; top-level, table, view, flow,
composition, deployment, package, and agent contexts are release-audited
through `completion_context_filtering`. The audit publishes the context names,
passing and missing context counts, missing expected labels, and forbidden label
leaks. The aggregate `lsp_navigation_completion_contracts` gate fails unless all
eight contexts pass with zero missing labels and zero forbidden labels.

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
Without `--json`, the same command prints the
`appgen.lsp-code-action-apply.v1` format, action id, change status, edit count,
lint status, title, applied edit text as `edit ...`, available actions for
unknown ids, and diagnostics.
`appgen.lsp-code-action-text-renderer.v1` is embedded in the tooling audit to
prove quick-fix logs keep success, failure, title, available-action, lint, edit
text, and diagnostic evidence visible without JSON parsing.
Its renderer contract reports fragment and marker counts for success/failure
summaries, titles, edits, available-action lists, and diagnostics.
Those counts are also backed by named required, emitted, missing, and
missing-count evidence for text surfaces, action ids, edit snippets,
available-action fallback ids, diagnostic codes, and status markers
(`ok`, `failed`, `lint_ok=True`, `lint_ok=False`, `changed=True`, and
`changed=False`). The aggregate quick-fix text gates require zero named missing
entries, so a log line with the right prefix cannot mask a missing quick-fix
action, edit, diagnostic, or fallback action.
This is the evidence path for missing-operation, lookup-directive,
event-contract, relationship, typo, secret-literal replacement, invalid
runtime/stream/backend picker removal, PBC manifest, agent-permission, package
creation for app targets, and smoke-test declaration quick fixes used by IDEs
and agents. `appgen.lsp-code-action-cli-audit.v1` must cover the same required
action ids as the in-process `appgen.lsp-code-action-apply-audit.v1` release
gate so external agents and editor integrations are not weaker than library
callers. Both audits report `required_action_ids`, `observed_action_ids`, and
`missing_required_action_ids`; the top-level tooling audit fails when the CLI
quick-fix surface is missing an action required by the in-process patch
contract. The in-process apply audit reports case, passing-case,
failing-case, required-action, observed-action, missing-required-action,
applied-edit, lint-passing-case, lint-failing-case, diagnostic-code, and
blocking-gap counts so library consumers get measurable quick-fix breadth and
failure evidence from the top-level report. It also reports required, observed,
and missing case ids; expected text by case; expected-text matched cases;
applied-edit cases; changed cases; cleanup cases; and lint-passing cases so the
library-side gate identifies the exact quick-fix family that lost its patch,
cleanup, expected text, or lint handoff.
The CLI audit also reports case, passing-case, required-action, observed-action,
missing-action, applied-edit, lint-passing-case, lint-failing-case,
changed-case, unchanged-case, and blocking-gap counts so external agents can
verify quick-fix coverage without expanding every case. It also reports
case ids, failing-case names, expected and observed exit codes by case, expected
and observed `appgen.lsp-code-action-apply.v1` payload formats by case,
per-case `ok` status, expected-text match counts, forbidden-text removal counts,
and lint-format counts so regressions can be traced to the exact quick-fix
family and whether the process status, report envelope, patch, cleanup, or lint
handoff failed.
It publishes required, observed, and missing case ids; expected text by case;
expected-text matched cases; forbidden text by case; forbidden-removed cases;
changed cases; applied-edit cases; lint-format cases; and lint-passing cases.
The aggregate gate fails when any named quick-fix case loses its edit, expected
text, cleanup, lint report, lint pass, changed status, or required action id.
The top-level tooling audit publishes three separate release gates for this
surface: `lsp_quick_fix_coverage_contracts` proves required quick-fix families
apply as linted DSL patches; `lsp_quick_fix_cli_contracts` proves the CLI has
the same required action ids and zero blocking gaps as the in-process contract;
and `lsp_quick_fix_text_contracts` proves text logs keep success, failure,
title, edit, changed, lint, available-action, and diagnostic evidence visible
for agents and IDEs that consume human-readable logs.
`appgen.lsp-rename-cli-audit.v1` reports safe, blocked JSON, and blocked text
scenario counts plus blocker-code and suggested-fix counts for rename safety.
It also reports named scenario ids, failing-scenario counts, and failing
scenario names, expected and observed exit codes by scenario, expected and
observed `appgen.lsp-service.v1` payload formats for JSON scenarios, and
per-scenario `ok` status so rename regressions identify the exact lexical scope,
process status, service envelope, or approval-blocker path that failed.

## IDE Integration

Two editor surfaces are required.

### VS Code Extension

The VS Code extension should provide:

- language-server activation for `.appgen` files;
- syntax highlighting;
- diagnostics panel integration;
- code actions and quick fixes;
- outline tree;
- activity-bar views for workspace actions, release reports, and agent handoffs;
- graph previews;
- generated artifact preview;
- command palette actions for lint, semantic JSON, semantic preview, format,
  validation, graph, designer sync, migration planning, natural-language
  planning, coding-agent handoff preparation, explain, generate, release
  verification, package, doctor, tooling audit, contract schema browsing, and
  semantic contract validation;
- PBC catalog browser.

The repository ships the extension scaffold at `extensions/vscode-appgen-x`.
It contributes the `appgen` language for `.appgen`, `.ag`, and `.ags` files,
syntax highlighting, language configuration, command palette entries, and a
dependency-free JSON-RPC client that launches `appgen lsp --stdio`. The client
registers VS Code providers for diagnostics, completion, hover, definition,
references, document symbols, workspace symbols, rename, code actions, and
formatting, while command palette actions call the same CLI contracts for lint,
semantic model extraction, validation, format, graph, designer sync, migration
planning, natural-language change planning, explain, generate, release
planning, coding-agent handoff preparation, explain, generate, release
verification, package, doctor, tooling audit, contract schema browsing,
semantic contract validation, and PBC catalog browsing. It also contributes an
AppGen-X activity-bar container with Workspace, Reports, and Agent Handoffs
views. These views expose the same command contracts as clickable tree actions,
so users can drive application design, database validation, release evidence,
and coding-agent handoffs without memorizing CLI flags.
Semantic model previews, validation reports, graph previews, designer sync
reports, migration plans, natural-language change plans, generated artifact
previews, release-verifier reports, doctor/tooling-audit reports, contract
schema and contract validation reports, coding-agent handoff reports, and the
PBC catalog browser render CLI JSON reports in webview panels rather than
relying on editor-specific state.
`appgen.vscode-extension-audit.v1` checks this surface explicitly: language
metadata, syntax grammar, command contributions, LSP providers, diagnostics
collection, command activation events, command palette membership, CLI command
configuration, activity-bar view contributions, welcome content, CLI-backed
command argument contracts, named activity-bar tree actions, and
semantic/validation/graph/designer/migration/NL
plan/agent-handoff/artifact/release/tooling/contract/PBC webview renderers must all be present before
the extension is counted as tooling-complete. The audit also reports command,
activation-event, view, provider-marker, CLI-contract-marker, and webview-marker
counts so release evidence captures the editor surface breadth, not only pass/fail booleans. It
also reports missing-command, missing-activation-event, missing-palette-entry,
missing-view, missing-view-welcome, missing-provider-marker,
missing-activity-tree-command, missing-CLI-contract-marker, and
missing-webview-marker counts, which must all be zero for the extension gate to
pass. The activity tree action contract requires Workspace actions for
validation, designer sync, graph preview, generation, and packaging; Reports
actions for doctor, tooling audit, contract schema browsing, semantic contract
validation, release verification, and migration planning;
and Agent Handoff actions for natural-language planning, semantic preview, and
the PBC catalog browser.

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
Each Studio panel projection is a schema-backed handoff contract:
`appgen.designer-dsl-editor.v1`, `appgen.designer-component-palette.v1`,
`appgen.designer-form-projection.v1`,
`appgen.designer-database-projection.v1`,
`appgen.designer-workflow-projection.v1`,
`appgen.designer-pbc-composition-projection.v1`,
`appgen.designer-package-deployment-projection.v1`,
`appgen.designer-graph-explain-panel.v1`, and
`appgen.designer-nl-planner-panel.v1`. Single visual edits return
`appgen.designer-visual-edit-result.v1`, while multi-edit transactions return
the transaction-specific contract below. Agents and IDE clients should validate
the panel projection they consume directly instead of unpacking the aggregate
designer-sync report by convention.
Designer edits may also be submitted as an atomic transaction with
`kind: "transaction"` and an `edits` array. A transaction can span database
field creation, form component placement, workflow transition edits,
menu/context-menu edits, splash/startup asset edits, style-token edits,
package/deployment edits, and other designer surfaces in one request. The
transaction returns `appgen.designer-visual-transaction-result.v1`, per-edit
patch evidence, combined DSL diff evidence, changed-surface evidence, and an
attempted-source preview. If any edit makes the database-backed form invalid,
the transaction is rejected atomically: the returned `patched_source` remains
the original source, diagnostics explain the invalid binding, and the attempted
source shows what would have been applied.
The designer-sync audit reports scenario, passing-scenario, changed-surface,
projection, invalid-case, and traceback-free counts across accepted edits,
bulk transactions, malformed JSON, and non-object edit payloads.
It also reports required, observed, missing, and failing scenario ids; required
projection ids; missing projection ids; required changed surfaces; required
diff fragments; invalid-case ids; traceback-free case ids; and missing
traceback-free cases. The aggregate IDE gate fails when a named designer-sync
scenario, projection surface, changed surface, diff preview fragment, or
invalid-payload rejection contract disappears.
For bulk transactions, the audit also reports atomic status, operation count,
operation names, required/observed/missing changed surfaces, patch count, and
semantic-model format. The aggregate IDE and implementation-phase gates require
the bulk transaction to round-trip with zero missing surface gaps, so Studio
cannot claim visual-designer readiness while only supporting one edit at a
time.
The required visual edit matrix includes menu creation, context-menu creation,
splash-screen package metadata, and style-token component contracts in addition
to table fields, form placements, workflow transitions, PBC composition,
packages, and deployment units. This is the executable tooling path for
fine-tuning application menus, right-click menus, startup screens, and UI theme
tokens from the IDE.
The CLI audit also publishes expected and observed exit codes for valid and
invalid designer-sync scenarios and expected versus observed payload formats for
accepted visual edits, plus per-scenario `ok` status. The aggregate IDE gate
requires those named missing lists to be empty, so malformed edit payloads must
remain exit-code `2` and accepted visual edits must keep the
`appgen.designer-sync-report.v1` envelope instead of passing through scenario
counts alone.
Without `--json`, `appgen designer-sync` prints the
`appgen.designer-sync-report.v1` format, semantic-model format as
`semantic_format=...`, surface count and names, visual edit acceptance,
round-trip status, changed surfaces, DSL diff line count, DSL diff preview lines
as `dsl-diff ...`, visual-edit matrix coverage, required visual
edit operation names, executed matrix case ids as `visual-edit-case ...`, and
sync checks.
`appgen.designer-sync-text-renderer.v1` is embedded in the tooling audit to
prove those designer handoff logs keep round-trip, projection, diff-preview,
matrix, required-operation, and executed-case evidence visible without JSON
parsing. The renderer contract reports fragment and marker counts for the
designer summary, surface list, visual edit, DSL diff, matrix, and check lines.
It also reports summary-line, surface-line, visual-edit-line, dsl-diff-line,
matrix-line, operation-line, case-line, check-line, passing-check-line, and
failing-check-line counts so designer release logs prove round-trip,
projection, and matrix evidence did not collapse into prose.
Those counts are backed by named evidence: the renderer publishes required,
emitted, missing, and missing-count fields for designer surfaces, changed
surfaces, visual edit operations, matrix case ids, check ids, DSL diff snippets,
text surfaces, embedded contract formats, and status markers. The aggregate IDE
gate requires zero named missing entries, so a generic designer-sync line cannot
mask a hidden changed surface, operation, case, diff preview, matrix format, or
round-trip marker.
`--edit-json` must be a JSON object; malformed edit payloads are CLI
configuration errors and return exit code `2` before any designer mutation is
accepted.
Designer edit coverage is executable through
`appgen.designer-visual-edit-matrix.v1`. The matrix proves database field
edits, form component placement, workflow transitions, PBC composition
includes, package creation, deployment-unit creation, multi-surface transaction
acceptance, atomic transaction rejection, and invalid form binding rejection all
pass through the same linted DSL patch and projection refresh path before
acceptance.

The package-level Studio now exposes `appgen.studio-semantic-service.v1` as the
shared web IDE bridge. That contract composes `appgen.lsp-service.v1`,
`appgen.designer-sync-report.v1`, `appgen.graph-suite-report.v1`, and
`appgen.nl-plan.v1` so the DSL editor, component palette, form designer,
database designer, workflow designer, PBC composition designer,
package/deployment designer, diagnostics panel, graph/explain panel, and
natural-language planner all prove they are reading the same semantic source.
The browser Studio now includes a concrete DSL Editor workbench rather than a
placeholder panel. It renders editable source, diagnostics, semantic outline,
completion templates for schema/UI/workflow/agent/release constructs, quick
fixes for missing handlers and weak status fields, and compact agent handoff
cues. Its static frontend audit is `appgen.frontend-dsl-editor-audit.v1`, and
the interaction bridge requires the named
`dsl_editor_lint_completion_quick_fix` scenario before Studio readiness can
pass. The Python Studio smoke contract inspects both `dslEditorCatalog.ts` and
`DslEditorWorkbench.tsx` and reports diagnostic-code, quick-fix, completion
category, catalog-helper, and workbench-marker missing lists. The aggregate
tooling audit includes a dedicated `frontend_dsl_editor_bridge` gate so a
broken browser DSL editor cannot be hidden behind a passing generic interaction
audit.
`appgen.studio-semantic-service-audit.v1` is the executable audit for that
bridge. It verifies every required Studio panel is present, every panel emits
the expected contract format, semantic-bound panels report
`appgen.semantic-model.v1`, diagnostics and quick fixes come from the LSP
contracts, graph/explain comes from the graph-suite and designer explain-panel
contracts, and natural-language evolution requires a DSL diff preview applied
through `appgen designer-sync`. The audit reports `required_service_formats`,
`observed_service_formats`, `missing_service_formats`, and the corresponding
service-format counts so release evidence proves the Studio bridge is not only
present but composed from the documented LSP, designer-sync, graph-suite, and
natural-language planner contracts. It also reports required/present surface
counts, missing required surface names/counts, surface-format counts,
surface-format gap names/counts, semantic-surface-format counts,
semantic-surface-format gap names/counts, check/pass/fail counts, blocking-gap
counts, and panel-count totals before verifying panel payload depth: component
palette entries, form views, database tables, workflows, PBC composition
entries, package/deployment counts, diagnostic rows, graph/explain graphs, and
natural-language edit operations must be exposed, so a panel cannot pass with
only an empty format envelope.
The frontend renders the same bridge through a dedicated semantic-service
panel, and the browser smoke contract includes that panel as a required
scenario. The browser-smoke CI contract embeds
`appgen.frontend-semantic-service-audit.v1`, which statically verifies the
frontend `semanticServiceContract.ts` service evidence, required surface ids,
surface contract formats, and the `SemanticServicePanel` rendering hooks before
the Studio bridge counts as complete in Python release evidence. It also embeds
`appgen.frontend-interaction-audit.v1`, which proves the frontend interaction
audit covers palette category/search/empty states, component drag payloads,
actionable drop preview/commit operations with handler definition evidence,
device and data workbench render inputs, status-rail audit inputs, and the
semantic-service bridge before the Studio browser-smoke gate can pass.
The browser-smoke script must assert the rendered interaction-count text that
matches `appgen.frontend-interaction-audit.v1`'s required scenario count, so a
stale browser smoke expectation cannot pass while the interaction audit has
grown.
The top-level `appgen.tooling-audit.v1` treats these as first-class gates:

The raw Studio bridge payloads are also schema-backed contracts, not just
nested audit details. `appgen.studio-diagnostics-quick-fixes.v1` validates the
diagnostic and quick-fix panel payload, `appgen.studio-graph-explain.v1`
validates the graph-suite/explain bridge payload,
`appgen.studio-natural-language-evolution.v1` validates the prompt-to-DSL-diff
evolution payload, and `appgen.studio-browser-smoke-ci-contract.v1` validates
the executable browser-smoke handoff. This lets IDE clients, CI agents, and
external coding agents validate each Studio bridge surface independently before
they trust the aggregate semantic-service audit.
`frontend_semantic_service_bridge` reports service, surface, surface-contract,
required/observed/missing-name, and missing-count evidence from
`appgen.frontend-semantic-service-audit.v1`; the browser-side audit function
must return the same named required/observed/missing fields for services,
surfaces, and surface contracts so release evidence is not only reconstructed
from static Python parsing;
`frontend_interaction_audit_bridge` reports scenario, audit-input, helper, and
required/observed/missing-name evidence from
`appgen.frontend-interaction-audit.v1`. Either gate can fail independently of
the aggregate Studio semantic-service audit, so browser-facing regressions are
visible in release evidence without expanding nested Studio details. The release
gate also requires observed frontend services, surfaces, surface contracts,
interaction scenarios, audit inputs, and helpers to meet their required totals
with empty named-missing tuples. Drag/drop readiness is not counted from static
markup alone: the audit must see palette drag payload construction, drop preview,
drop commit, and generated handler wiring helpers, which keeps browser-facing
bridge regressions actionable in CI logs.
`frontend_data_service_catalog_depth` reports
`appgen.frontend-data-service-catalog-audit.v1` evidence for the data-service
workbench catalog itself: required capability names, required lanes,
missing-capability/lane/audit-field counters, and weak-generation-term hits. It
must prove source, query, publish, embedded database, resilience, and security
lanes with concrete generated artifacts, and it rejects hollow terms such as
stub, placeholder, TODO, TBD, or fake. The browser-smoke script also checks
rendered data-service generated-artifact text, including the failover policy's
operational runbook package, so a visually present but implementation-hollow
data-service card cannot satisfy the Studio gate.

## Graph Tooling

Graph output must be available from CLI, IDE, tests, and release evidence.
`appgen.release-evidence-bundle.v1` embeds graph-suite evidence with the
required graph kinds and output formats, so packaged releases carry the same
reviewable graph contract as the CLI and IDE previews.

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
backfill cases instead of inferring coverage from prose. The top-level
`appgen.migration-plan.v1` report also publishes allowed-backend,
change, destructive-change, diagnostic, and rename-hint counts so agents can
review migration risk without expanding every change object.

Destructive changes must require explicit approval and should include suggested
safe alternatives when possible. Without `--json`, `appgen migration-plan`
prints the `appgen.migration-plan.v1` format, backend, change count,
destructive change count, approval requirement, the
`appgen.migration-coverage.v1` nested coverage format as a `format=...` marker,
missing-family count, detected migration families as `migration-detected ...`,
missing migration families as `migration-missing ...`, each change kind, safe
alternatives when present, and diagnostics; JSON remains the machine-readable
source of truth.
`appgen.migration-plan-text-renderer.v1` is embedded in the tooling audit to
prove migration text logs keep backend, destructive-count, approval, coverage,
detected-family, missing-family, change, safe-alternative, and diagnostic
markers visible without JSON parsing.
The renderer contract reports fragment and marker counts across coverage,
detected/missing families, changes, safe-alternatives, and diagnostics.
It also reports summary-line, coverage-line, detected-family-line,
missing-family-line, change-line, safe-alternative-line, diagnostic-line,
warning-line, error-line, approval-line, and destructive-summary-line counts so
migration release logs prove safety posture, coverage breadth, destructive
change count, and mitigation guidance remain visible.
Those counts are backed by named required, emitted, missing, and missing-count
evidence for text surfaces, detected migration families, intentionally missing
coverage families, change targets, safe-alternative families, diagnostic codes,
and embedded migration contract formats. The migration safety gates require
zero named missing entries, so a release log cannot satisfy the audit by
printing generic `change`, `safe-alternative`, or `warning` lines while omitting
the required migration family or approval evidence.
`appgen.migration-cli-audit.v1` reports case, passing-case, failing-case,
allowed/observed/missing backend, required/observed/missing change-kind,
approval-required, and rename-hint case counts so supported database profiles,
required migration families, and rename-hint behavior are visible in release
evidence without expanding every per-backend case. It also reports required,
observed, and missing backend case ids; expected and observed backend names by
case; required and missing change kinds by case; expected and observed
`appgen.migration-plan.v1` payload formats by case; approval-required case ids;
and expected versus observed rename-hint counts by case. This makes a missing
backend profile, wrong backend payload, missing migration family, lost approval
posture, lost rename hint, or report-envelope regression fail by named case
rather than only changing an aggregate count.
The same CLI audit publishes expected and observed exit codes, destructive
change counts, safe-alternative counts, and required diagnostic codes by backend
case. The migration safety gate requires those named missing lists to be empty,
so each supported backend must prove the destructive migration warning
(`AGX1101`), an explicit approval posture, and at least one safe alternative
instead of only returning a successful JSON envelope.
`appgen migration-plan` accepts either raw DSL files or serialized
`appgen.semantic-model.v1` JSON baselines for its previous and current inputs.
This lets CI, IDEs, and composition pipelines diff frozen semantic baselines
without reparsing old source text, while still preserving source-file names,
rename hints, backend selection, destructive-change approval evidence, and
`appgen.migration-coverage.v1` output. The human text renderer emits a
`migration-inputs previous=... current=... semantic_inputs=...` line so release
logs show whether the plan was generated from DSL text, semantic JSON, or a
mixed input pair. `appgen.migration-semantic-input-cli-audit.v1` proves the CLI
accepts semantic JSON baselines, preserves both baseline paths in
`source_files`, reports two semantic inputs, detects table and field renames
plus additive changes, and avoids falling back to raw JSON for text output.
The aggregate tooling audit exposes migration safety and text evidence as
`migration_safety_text_contracts`. This gate fails independently when required
detection families are missing, supported backend profiles fail, destructive
changes do not require approval, rename-hint evidence disappears,
semantic-baseline support disappears, safe-alternative text disappears, report
payload formats drift, or migration text output falls back to raw JSON.

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
rejected with `AGX1201` instead of generating code. The contract audit reports
case, passing-case, accepted-case, rejected-case, required-operation,
observed-operation-kind, missing-required-operation-kind, token-budget-case,
and blocking-gap counts so the natural-language development vector stays
measurable before the CLI layer is involved.
The aggregate tooling audit exposes this proof independently as
`natural_language_operation_contracts`. That gate fails when any documented
operation cannot be represented as DSL, accepted requests omit patch, lint,
migration, test, or token-budget evidence, unsupported requests stop emitting
`AGX1201`, or the observed operation family no longer covers the documented
surface.
The CLI proof mirrors the same operation family through
`appgen.nl-plan-cli-audit.v1`: each supported edit operation is exercised
through `appgen nl-plan --json`, then checked for the expected operation kind,
linted patch, migration preview, generated test plan, and token-budget notes.
It reports required, observed, and missing accepted JSON case ids; expected and
observed operation kinds by case; expected and observed `appgen.nl-plan.v1`
payload formats by case; cases missing lint, migration-preview, test-plan, or
token-budget evidence; and required versus missing text markers.
It also runs an accepted request without `--json` and requires the text output
to expose the `appgen.nl-plan.v1` envelope, nested lint and migration-preview
format markers, PostgreSQL backend marker, generated test-plan entries as
`test-plan ...`, token-budget notes marker, and individual
`token-budget-note ...` guidance lines. The audit reports total,
accepted, accepted-passing, accepted-failing, rejected, text-case,
required-operation, accepted-operation-kind, missing-accepted-operation-kind,
text-marker, blocking-case, test-plan-line, token-budget-note-line, and
rejection-status counts so token-efficient agent workflows can verify breadth
without expanding every generated patch.
The aggregate tooling audit exposes this proof independently as
`natural_language_cli_agent_contracts`. That gate fails when JSON output stops
carrying bounded DSL patches, accepted text output hides report, lint,
migration, test-plan, or token-budget markers, rejected prompts stop returning
`AGX1201`, named accepted operation cases disappear, per-case payload/lint/
migration/test/token evidence drifts, or blocking cases appear. This is the
release gate for Claude Code, OpenAI Codex, OpenCode, Ollama, vLLM, and small
local models using natural language as a first-class development vector.
Every accepted `appgen nl-plan` response now carries `agent_handoffs` for
Claude Code, OpenAI Codex, and OpenCode with launcher names, supported
`api-key`/`ollama`/`vllm` backends, required outputs, and guardrails. Text mode
prints `agent-handoff ...` lines so external coding agents can pick the right
execution vector without expanding the full JSON payload. The same response
also carries compact model briefs for `qwen3.5-2b`, `qwen3.5-4b`, and a vLLM
4B profile with prompt and patch token estimates, and text mode prints
`compact-model ...` lines for CI and local-agent routing.
The CLI audit also publishes expected and observed accepted-case exit codes,
accepted-case `ok` booleans, rejected-case exit codes, rejected payload formats,
required rejected diagnostic codes, and rejected empty-patch evidence by named
case. The aggregate gate requires those named missing lists to be empty, so
small-model agent workflows cannot pass by emitting a patch-shaped payload for
unsupported requests, returning the wrong process status, or hiding an
out-of-DSL rejection behind aggregate counts.

### `appgen agent-handoff`

```console
appgen agent-handoff app.appgen --prompt "Add invoice approval" --operation add_flow_transition --json
appgen agent-handoff --vector openai_codex --backend ollama
```

`appgen agent-handoff` emits `appgen.agent-handoff-report.v1`, a compact
development-vector contract for external coding agents. It returns the supported
agent vectors (`claude_code`, `openai_codex`, and `opencode`), launcher names,
`api-key`/`ollama`/`vllm` backend filters, required outputs, AppGen-X guardrails,
canonical follow-up commands, token-budget notes, and compact model briefs for
small local models. If a DSL file is provided, the report includes semantic
symbol counts and a compact prompt digest so agents can operate on symbols plus
bounded DSL diffs instead of the full generated project.

Text mode prints `agent-handoff ...`, one `agent-handoff <vector> ...` line per
runner, `compact-model ...` lines, command lines, and `token-budget-note ...`
guidance. This lets CI, local shells, and small local models route work without
parsing the full JSON payload.

The aggregate tooling audit includes the `agent_handoff_cli_contracts` gate and
the standalone `appgen.agent-handoff-cli-audit.v1` contract. That audit runs the
command in all-vector JSON mode, filtered OpenAI Codex plus Ollama JSON mode,
and filtered text mode. It requires the three supported development vectors,
the `api-key`/`ollama`/`vllm` backend set, semantic-model provenance for file
inputs, compact generation briefs, token-budget notes, canonical follow-up
commands, non-JSON text output, and zero missing case, exit-code, payload, or
marker gaps.

The test-strategy CLI audit reports case, passing-case, failing-case, case-id,
required-surface, observed-surface, missing-surface, payload-format, and
doctor-check counts across diagnostics, parser golden, semantic drift, and
doctor gates, so release evidence proves the generator, IDE, LSP, graph, and
release-verifier surfaces share the same semantic model without expanding every
nested report.
It is directly callable:

```console
appgen test-strategy path/to/app.appgen
appgen test-strategy path/to/app.appgen --json
```

Text mode prints a `test-strategy ...` summary, one line per diagnostics,
parser-golden, drift, and doctor case, and an `observed-surfaces ...` line for
the shared semantic-model surfaces. JSON mode emits
`appgen.test-strategy-cli-audit.v1` with the source file name and this section
as `source_of_truth`.
It also reports required, observed, and missing case ids; expected and observed
exit codes by case; case `ok` status by case; expected and observed payload
formats by case; expected text markers by case; text exit codes by case;
text-marker presence by case; and text JSON-fallback status by case. The
aggregate gate requires all named missing lists to be empty, so diagnostics,
parser-golden, drift, and doctor evidence cannot disappear, return the wrong
process status, drift JSON format, lose human-readable text, or fall back to raw
JSON while the aggregate case count still looks correct.
The semantic drift text renderer also publishes required, emitted, missing, and
missing-count evidence for drift text surfaces, embedded drift/semantic/generator
contract formats, and semantic digests. The aggregate semantic gate requires
zero named missing entries, so generic drift line counts cannot mask a hidden
surface list, evidence line, check result, format marker, or model digest.
This keeps agent-facing development paths honest; a capability is not counted
as available just because an in-process helper can produce it.
The aggregate tooling audit also publishes
`appgen.test-family-contract-audit.v1` through the
`test_strategy_family_contracts` gate. That gate maps every required Test
Strategy row to executable evidence: parser golden, semantic, diagnostic
golden, formatter, CLI, LSP, graph, migration, natural-language planner,
verifier, and drift families must all have passing evidence formats and zero
missing families before `docs/tooling.md` can be considered implemented.

## Package And Verifier Tooling

Release verifiers should generate evidence for each target.

Web verifier:
`appgen.web-verifier.v1`

- app builds;
- routes exist;
- generated forms bind valid fields;
- handler targets resolve;
- smoke tests run.

Mobile verifier:
`appgen.mobile-verifier.v1`

- package metadata exists;
- signing posture declared;
- offline policy declared where needed;
- permissions are explained;
- generated screens fit target density;
- smoke launch path exists.
  Mobile package manifests must carry the same evidence as handoff metadata:
  signing posture, offline policy, permissions, screen-density fit, and smoke
  launch readiness plus the launch entrypoint.

Desktop verifier:
`appgen.desktop-verifier.v1`

- package metadata exists;
- installer/update posture declared;
- splash/startup assets declared where used;
- menus and context menus bind to handlers;
- smoke launch path exists.
  Desktop package manifests must carry installer posture, startup assets,
  menu/context-menu handler binding, and smoke launch entrypoint as handoff
  metadata, including explicit package-metadata and smoke-launch readiness
  booleans.

PBC verifier:
`appgen.pbc-verifier.v1`

- manifest validates;
- package artifacts exist;
- owned tables have migrations/models;
- APIs/events/handlers are declared;
- no private cross-PBC table mutation;
- self-registration is side-effect-free;
- release evidence exists.

Deployment verifier:
`appgen.deployment-verifier.v1`

- units declared;
- health checks declared;
- environment variables named;
- secret values absent;
- resource hints present for production units;
- topology graph is connected and explainable.
  Deployment package manifests must carry the same readiness booleans as
  handoff metadata: units, health checks, environment variable names,
  secret-value absence, resource hints, and connected topology graph evidence.

The package invalid-target audit reports case, passing-case, failing-case,
invalid-choice-message, traceback-free, and case-id counts for unsupported
`package` and `verify` target handling, so package tooling has explicit
failure-path evidence in addition to successful target manifests. It also
reports required, observed, and missing case ids; invalid-choice-message cases;
traceback-free cases; expected exit codes by case; and missing expected-exit
cases so unsupported target handling fails by named command path instead of only
changing aggregate failure counts.
The package handoff audit publishes required and observed manifest formats,
artifact classes, and smoke entrypoints by target, with named missing target
lists for each family. The aggregate package manifest gate requires those lists
to be empty, so web, mobile, or desktop packaging cannot pass by only reaching
the expected manifest count while losing the target-specific package class,
manifest envelope, or smoke launch entrypoint.
Readiness checks are also grouped by target in `missing_readiness_checks_by_target`
and folded into the package audit `ok` status, so a mobile signing, desktop
menu, web handler, PBC registration, or deployment topology regression fails
with the exact target/check pair instead of only changing aggregate readiness
counts.
Release evidence reports publish target-specific verifier formats, verifier
kinds, ok flags, and blocking-gap counts. The aggregate package manifest gate
requires all release report format, kind, ok, and blocking-gap target lists to
pass, so a generated package cannot claim release evidence by only writing five
report keys with incomplete verifier payloads.

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
- `required_construct_count`, `covered_construct_count`, and
  `missing_construct_count`: top-level coverage counters for release gates and
  token-efficient agents;
- `fixture_count`, `valid_fixture_count`, `invalid_fixture_count`,
  `passing_fixture_count`, `failing_fixture_count`, `parsed_fixture_count`,
  `valid_parsed_fixture_count`, `invalid_rejected_fixture_count`, and
  `blocking_gap_count`: fixture outcome counters that prove both valid and
  invalid examples ran through the parser;
- `fixtures`: per-fixture parse outcome, validity expectation, construct tags, and syntax error text;
- `blocking_gaps`: the exact fixture failures that should block CI.

Without `--json`, `appgen parser-golden` prints the pass/fail status, report
format in the header, total fixture count, valid and invalid fixture counts, required
construct count, covered construct count, covered construct names as
`covered-constructs ...`, missing construct count, missing construct names when
present, and blocking fixture gaps. JSON remains the
machine-readable source of truth.

`appgen.parser-golden-text-renderer.v1` is embedded in the tooling audit to prove parser-golden text logs keep fixture counts, covered construct names, missing construct names, and blocking gap evidence visible without JSON parsing. The parser-golden renderer contract reports fragment and marker counts for the header, covered/missing construct lines, and blocking fixture gaps.
It also publishes required, emitted, missing, and missing-count evidence for
covered constructs, intentionally missing constructs, blocking gap ids, text
surfaces, report formats, and exact fixture-count markers. The aggregate parser
golden gate requires zero named missing entries, so generic parser-golden lines
cannot mask a hidden construct list, gap id, report format, or fixture summary
marker.
The aggregate tooling audit exposes this proof independently as
`parser_golden_fixture_contracts`. That gate fails when any required construct
lacks a valid fixture, invalid fixtures stop rejecting, blocking parser gaps
appear, or parser-golden text output loses construct/gap markers.

The required construct set includes application options, table fields, reusable field groups, spreads, derived fields, modifiers, relationships, relationship cardinality, table directives, enums, views, component placement, handlers, flows, workflow directives, roles, permissions, rules, rule expressions, LLM definitions, agents, PBCs, PBC composition include/require/expose/connect clauses, audit blocks, deployment units/scale/health/check/resource/env/directives, version blocks, operations, security, APIs, events, jobs, reports, menus, component contracts, packages, and tests.

When a new keyword, block, nested item, or syntax form is added to `lang/appgen.g4`, the same change must add or extend a parser golden fixture before the grammar is considered release-ready. Diagnostic golden fixtures are still required for semantic behavior, but parser-golden fixtures prove that the grammar itself accepts and rejects the intended language forms.
The aggregate tooling audit also exposes shared-model drift as
`semantic_drift_surface_contracts`. That gate fails when CLI, LSP, Studio,
graph, generator, generator-readiness, release-verifier, or tests stop proving
they consume the same `appgen.semantic-model.v1`, or when drift text output
loses surface, evidence, check, digest, or gap markers. The drift text renderer
also publishes required and emitted surface names, blocking-gap ids, evidence
keys, check ids, passing-check ids, and failing-check ids with named missing
lists, so shared-model release evidence fails on the exact hidden drift marker.

## Implementation Phases

Phase completion is an executable contract, not a planning note.
`appgen.tooling-implementation-phase-audit.v1` is embedded in
`appgen.tooling-audit.v1` and maps each phase below to concrete exit-criteria
evidence. A phase is counted as complete only when every listed exit criterion
has a current machine-readable proof from the CLI, semantic model, LSP, designer
sync, migration planner, natural-language planner, release verifier, or fixture
audit surfaces.
The audit also exposes `passing_exit_criteria_by_phase`,
`required_phase_ids`, `missing_required_phase_ids`,
`required_exit_criteria_by_phase`, `observed_exit_criteria_by_phase`,
`missing_required_exit_criteria_by_phase`,
`exit_criterion_evidence_formats_by_phase`, and
`evidence_formats_by_criterion` on each phase. Those fields are intended for
release dashboards and agents that need to prove which phase criteria are
complete, which machine-readable reports supported them, and which named
criteria still block completion. The aggregate gate fails when a required phase
or a named exit criterion is removed, hidden, or no longer backed by passing
runtime evidence.
`appgen implementation-phases` exposes the same phase audit directly. Text mode
prints per-phase pass/fail and exit-criterion totals; JSON mode emits
`appgen.tooling-implementation-phase-audit.v1` with the full evidence map.
`appgen.implementation-phase-doc-alignment.v1` is embedded beside it through
the `implementation_phase_doc_alignment_contracts` gate. It proves the seven
documented phase headings, titles, and representative exit criteria remain
aligned with the executable phase IDs and that each phase keeps an `Exit
criteria:` block in this document.

### Phase 0: Inventory And Stabilization

- Inventory existing parser, linter, formatter, release-audit, PBC catalog, and
  generator code.
- Identify duplicate semantic logic.
- Define JSON schemas for diagnostics and semantic model.
- Expose the reusable contract schema catalog through
  `appgen contract-schema --json`.
- Add fixture directories and built-in fixture catalogs for parser-golden,
  diagnostic-golden, formatter, semantic drift, graph, migration, generator,
  and verifier tests.

Exit criteria:

- Current behavior documented.
- No new generator behavior required.
- Tooling fixtures can run in CI, including `appgen parser-golden --json`,
  `appgen diagnostics --audit-fixtures --json`, and `appgen drift <file> --json`.
- `appgen.dsl-language-quality.v1` proves grammar/parser synchronization,
  required enterprise grammar rules, keyword budget, authoring aliases, and the
  progressive learning path.
- `appgen.contract-schema-cli-audit.v1` proves core diagnostic, lint,
  semantic-model, formatter, validate/generate, graph-suite, explain, LSP,
  semantic symbol-coverage, source-set, source-file, module-boundary,
  non-goal-policy, DSL keyword-budget, ANTLR-integrity, language-quality, and
  language-CLI contracts,
  lint directory CLI/text, formatter text/audit, validate-generate CLI/text,
  graph CLI/suite/text, explain CLI, diagnostics text, parser-golden text,
  semantic-drift text, and doctor CLI/text contracts,
  LSP capability, diagnostic, completion, hover, navigation, symbol, code-action,
  formatting, rename, JSON-RPC, stdio, and text-renderer subcontracts,
  CLI alias/help, missing-input, missing-required-option, invalid-choice, and
  internal-error contracts,
  designer-sync, visual designer, Studio/frontend bridge, diagnostic catalog,
  parser-golden, drift, migration, natural-language, release-verifier,
  package-manifest, component/PBC wrapper, doctor, tooling-audit,
  project-governance, schema-catalog, contract-validation, runtime inventory,
  package release-audit, agentic development-vector, ACP composition, compact
  generation, and top-level package support report schemas are available from CLI
  JSON and text modes. The schema audit validates representative payloads for all
  303
  documented `appgen.*.v1` formats, so
  adding a documented contract without a matching runtime sample fails the
  release gate.
- `appgen.contract-validation-cli-audit.v1` proves those JSON contracts can be
  enforced against real payloads, including valid semantic-model payloads,
  missing required fields, unknown schemas, malformed JSON, and text mode.
- The test-strategy CLI audit requires `appgen drift` to prove CLI, LSP,
  Studio, graph, generator, and release-verifier surfaces share one semantic
  model, including `appgen.generate-report.v1` evidence.

### Phase 1: Shared Semantic Model MVP

- Create shared parser wrapper.
- Create AST conversion layer.
- Build symbol table.
- Resolve tables, fields, relationships, lookup paths, views, handlers, flows,
  operations, PBC includes, packages, and deployment units.
- Emit `appgen.semantic-model.v1`.
- Load directory source sets and attribute symbols back to owning files.

Exit criteria:

- CLI and tests can load the same semantic model.
- `appgen semantic <directory> --json` emits `appgen.semantic-source-set.v1`
  metadata and per-file symbol ownership.
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

- Add subcommands for lint, semantic, format, validate, graph, explain, package, PBC, and
  natural-language planning.
- Add `appgen contract-schema` so JSON contract schemas are discoverable without
  reading source code.
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

Contributor tasks are executable coverage checkpoints, not only onboarding
advice. `appgen.contributor-task-contract-audit.v1` is embedded in the
aggregate tooling audit through `contributor_task_breakdown_contracts`. It maps
the good-first, intermediate, and advanced task lists below to concrete parser,
semantic, diagnostic, formatter, CLI, LSP, graph, migration, natural-language,
designer, release, and drift evidence. The gate fails when any listed task no
longer has a passing evidence format, when one of the three task groups is
missing, or when a required task name disappears from the runtime contract.
`appgen contributor-tasks` exposes the same report directly. Text mode prints
`group::task` lines with each evidence format; JSON mode emits
`appgen.contributor-task-contract-audit.v1` with the parent tooling-audit check
id so external agents can pick one bounded task without expanding the aggregate
audit.

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
- code action application for the full required quick-fix family;
- generator drift evidence proving `appgen generate` validates from the same
  semantic model as CLI, LSP, Studio, graph, and release-verifier surfaces.

Advanced tasks:

- safe rename across workspace;
- natural-language patch planner;
- visual designer round-trip engine;
- release evidence bundle verifier;
- cross-tool drift tests.

## Priority Order

Priority order is also executable release evidence. The aggregate tooling audit
embeds `appgen.priority-order-contract-audit.v1` through
`priority_order_contracts`; it proves the numbered list below stays in the
documented order and each priority has a passing evidence format before later
tooling is counted on top of an unstable foundation. It also publishes
`required_priority_ids` and `missing_required_priority_ids`, so a deleted or
renamed priority fails by name instead of only changing the priority count.
`appgen priority-order` exposes the same ordered roadmap directly. Text mode
prints each numbered priority with its evidence format; JSON mode emits
`appgen.priority-order-contract-audit.v1` with the parent tooling-audit check id.

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
