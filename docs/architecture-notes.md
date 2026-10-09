# Architecture notes

This is a working map of the codebase as it actually behaves, not a description
of intent. It records what the code does, how the pieces connect, and which
claims do not survive inspection. Where a number appears, it was measured in
this checkout on 2026-10-09; the commands to reproduce each measurement are at
the end.

For the intended design, read `architecture.md` and `pbc-specification.md`.
This document is the layer underneath: mechanisms, invariants, and defects.

## The one idea

Everything normalizes to a single canonical model, and every stage attaches an
executable evidence contract that can prove what it produced. The generator
itself is ordinary string emission. The unusual part is the audit layer: about
750 `*_contract()` functions and two dozen `*_release_audit()` functions that
return a dict shaped
`{"format": "appgen.<name>.v1", "ok": bool, "checks": (...),
"blocking_gaps": (...)}`. `ok` propagates upward, and the top-level audits fold
hundreds of checks into an `approved` or `blocked` decision.

The audits, not the generator, are the center of gravity. A change that keeps
generation working but breaks an audit is a change that failed.

## Scale and layout

| Area | Files | Lines |
|---|---|---|
| Core modules (`src/pyAppGen/*.py`) | 39 | 602,911 |
| PBC packages (`src/pyAppGen/pbcs/`) | 2,984 | 417,805 |
| Top-level tests (`tests/`) | 175 | 50,111 |
| Total tracked Python | 3,023 | 703,223 |

The distribution is extreme. Five files hold most of the core:

| File | Lines | Role |
|---|---|---|
| `gen.py` | 98,996 | generator, embedded templates, Click CLI |
| `form_designer.py` | 32,984 | form designer contracts, DFM serialization |
| `pbc.py` | 17,241 | PBC catalog, composition, release audits |
| `dsl.py` | 11,318 | DSL parser, linter, LSP, tooling CLI |
| `schema.py` | 2,033 | canonical model and source importers |

All 3,023 files compile. `gen.py` has 739 top-level functions and zero classes.

## Canonical model

`AppSchema` (`schema.py:366`) is a frozen dataclass of tuples, so it is
immutable and hashable. It carries tables, relations, views, flows, roles,
rules, enums, LLM providers, agents, platform blocks, and nine
`EnterpriseContractSchema` tuples for API, event, job, report, menu, component,
package, and test contracts. Twenty-four frozen dataclasses sit beneath it,
starting at `ColumnSchema:124`.

Five importers produce it:

- `schema_from_database_url:768` reflects a live database through SQLAlchemy.
- `schema_from_metadata:775` converts an existing `MetaData`.
- `schema_from_dbml:828` uses `pydbml`.
- `schema_from_sql:884` is a hand-written regex DDL parser.
- `schema_from_ponyorm:1002` walks the AST without executing the module.
- The DSL importer is `dsl.schema_from_dsl`, which lives in `dsl.py`, not here.

Provenance is first class. `source_profile()` (`schema.py:397`) hashes table,
relation, and enum signatures into a `sha256[:16]` fingerprint.
`source_fidelity_report():453` records per-source `lossy_features` and
`roundtrip_targets`, so a generated app can state what was preserved and what
needs review.

## DSL subsystem

The grammar is `lang/appgen.g4`: 572 lines, 81 parser rules, 85 lexer tokens.
The generated ANTLR parser is checked in at `src/pyAppGen/dsl_generated/lang/`
and imported by prepending that directory to `sys.path` (`dsl.py:50`).

Nothing regenerates the parser at build time. Sync is enforced only by a runtime
check, `dsl_antlr_integrity_report` (`dsl.py:9836`), which re-reads the `.g4`
with regexes and diffs its tokens and rules against the generated parser's
`symbolicNames` and `ruleNames`. That check currently passes.

Source is normalized before lexing. `schema_from_dsl` runs alias rewrites first
(`dsl.py:9027`): `entity`, `model` become `table`; `form`, `screen` become
`view`; `workflow` becomes `flow`; `hide` becomes `hidden`; `searchable` becomes
`search`. The canonical `->` reference arrow is rewritten back into the
grammar's legacy `ref` form, so the grammar's preferred surface and the
documented surface differ.

The language has two front doors. `__main__.py` intercepts nineteen subcommands
(`lint`, `format`, `validate`, `generate`, `graph`, `graph-suite`, `explain`,
`migration-plan`, `nl-plan`, `lsp`, `verify`, `package`, `pbc`, `designer-sync`,
`diagnostics`, `parser-golden`, `drift`, `doctor`, `tooling-audit`) and routes
them to `dsl_tooling_cli` (`dsl.py:1170`). Anything else falls through to the
legacy Click app in `gen.py`, which keeps the flag forms (`--lint-dsl`,
`--dsl`, `--format-dsl`). Both paths call the same functions in `dsl.py`.

The language server is real. `dsl.py` implements JSON-RPC over stdio, and
`extensions/vscode-appgen-x/src/extension.js` is a genuine client that
implements completion, hover, definition, references, document symbols, code
actions, rename, and workspace symbols, and that also shells out to CLI
subcommands for graph, explain, generate, package, and PBC listing.

`form_designer.py` serializes form designs to a subset of the Delphi DFM text
format and to a binary frame beginning `AGDFM\x01` followed by a length and a
checksum. `gen.py:53551` contains a second, independent copy of the same DFM
implementation for generated apps.

`nl.py` makes no network calls. It imports only `py_compile`, `re`,
`tempfile`, and `pathlib`. Natural-language handling is deterministic regex
parsing of a prompt into proposals, plus a prompt-brief renderer for small
models. There is no HTTP client anywhere in the module.

## Generation engine

`generate_app_from_schema` (`gen.py:31873`) runs a fixed spine of roughly 190
`write_*` calls: core Flask-AppBuilder code first, then assurance and ops, the
data plane, platform modules, UI and IDE modules, about sixty HTML templates,
and finally the project scaffold. `generate_app_from_database` (`gen.py:31698`)
does the same thing after introspection. The two functions share 76 identical
statements; the database version differs only in a three-line prologue.

There is no template engine. Everything is `f.write("...")` concatenation or a
triple-quoted f-string returned by a `_*_text` helper.

Fan-out comes from 79 `*_MODULES` tuples (`gen.py:2369` through `2947`), which
are lists of generated module basenames. Each `write_<family>_module_files`
loops over its tuple and writes `<name>.py` plus a mirrored `test_<name>.py`.
The 79 tuples hold 450 module names.

The output is large. Generating a two-table `InvoiceDesk` app produced 1,266
files across 133 directories, 42 MB total, all compiling. `write_project_scaffold`
writes to the parent of the app directory, so the project root gets `config.py`
(with `SQLALCHEMY_DATABASE_URI`), `deploy/` (Dockerfile, Caddyfile, Kubernetes,
Terraform for three clouds), `frontends/` for six frameworks, `sdks/` for four
languages, `native/mobile`, `native/desktop`, and a JHipster `app.jdl`.

Five `def main()` definitions appear in `gen.py`. Only one is real
(`gen.py:97782`, the Click CLI). The other four are literal text inside f-string
templates that get written to disk as the generated `seed.py`, the Kivy app, the
BeeWare app, and a quality script.

The CLI has 43 options, 24 of them audit flags. Each audit flag rejects any
other option, calls its `*_release_audit()`, prints JSON, and exits with the
audit's `ok` as the status code.

## PBC subsystem

There are 147 packages under `src/pyAppGen/pbcs/<key>/`. The catalog in `pbc.py`
lists 147 entries, and the on-disk directory set matches exactly.

Each package carries a fixed 19-file contract. The load-bearing file is
`runtime.py`, typically 1,500 to 2,000 lines, which holds the owned-table
tuples, the capability keys, the event inbox and outbox state machine, every
domain command, and the contract builders. `__init__.py` re-exports each
`<key>_*` symbol and defines six discovery entrypoints that delegate to the
shared helpers in `pbcs/source_contract.py`. The remaining files are thinner:
`manifest.py` is the catalog record, `models.py` is model metadata rather than
ORM classes, `services.py` is the command and query facade with an outbox,
`routes.py` derives route contracts from the services and dispatches through
`getattr`, `events.py` fixes the AppGen-X outbox, inbox, and dead-letter
contract, and `handlers.py` proves idempotency with a module-level set of
processed keys.

Most packages were emitted by `_pbc_package_file_contents` (`gen.py:24167`)
through `write_pbc_package_files:2957`. That generator does not emit
`runtime.py`, `standalone.py`, or `capability_assurance.py`; those are written by
hand. A generated `manifest.py` is literally `PBC_MANIFEST = {...!r}`, and a
generated `services.py` embeds one giant literal `EVENT_CONTRACT`. Twenty-two
packages were later upgraded to import from `.runtime` instead.

`pbc.py` is two files in one. Lines 1 to 15,526 hold the catalog, composition
logic, and audits. Lines 15,527 to 17,241 are about 1,500 re-export import lines
covering only 47 of the 147 packages. The other hundred are present in
`PBC_CATALOG` as data but cannot be imported through `pbc.py`.
`pbc_implementation_contract:13310` resolves each PBC's advanced runtime through
a 46-branch `if key == ...` chain.

Standalone operation is a recent, unfinished thread. Only three packages have a
`standalone.py` (`dam_core`, `customer_360`, `dom`), and they use two different
designs: `dam_core` keeps state in memory, while `customer_360` and `dom` back it
with a real SQLite store. Two more packages use `slice_app.py`, three use
`application.py`, and six use a bespoke `*_app.py`. No repository gate verifies
standalone behavior, and `composition_engine`, the orchestration package, has
none.

## Composition

`application_composition_topology():14072` defines a four-layer application
composition platform: composed digital experience, a composition layer with BFF
and GraphQL mesh and orchestration, an event backbone with gateway fabric and
schema registry and audit ledger, and nine domain meshes. `PBC_MESHES:2063`
assigns each package to one of ten meshes.

`pbc_composition_plan:14197` is the composition algorithm. It indexes every
emitted event by provider, resolves each consumed event against that index,
collects unresolvable consumed events as external contracts, and flags any
datastore that appears twice as shared. Its stop condition is the platform's
central invariant: do not compose PBCs unless each selected capability has an
owned datastore. Integration is by APIs, events, and projections, never shared
tables.

`pbc_selection_from_prompt:14170` is keyword matching, not a model call. It
lowercases the prompt and matches package keys, labels, and a hand-maintained
alias table.

Stream processing is locked by policy. Three internal profiles exist (Faust,
Quix, Bytewax), but the developer-visible picker is forced off everywhere:
manifests carry `stream_engine_picker_visible: False` and
`lint_pbc_eventing_choice:11757` rejects any manifest that sets a
`stream_processor`.

## Evidence and audit architecture

Evidence comes in three layers.

In the generated tree, `write_manifest` writes `app/appgen.json` containing the
schema and the capability list, and each selected PBC contributes a
`release_evidence.py` and a `RELEASE_EVIDENCE.md`.

Package audits are self-contained. Twenty-one core modules generate a throwaway
app into a `tempfile.TemporaryDirectory`, enumerate the resulting paths, and
assert that the required artifacts exist and compile. The audit builds a fresh
app each time it runs.

Aggregation happens at the top. `pbc_release_audit` folds seventeen gates into
an `approved` or `blocked` decision, and `package_goal_audit` (`roadmap.py:830`)
imports and folds twenty-two sub-audits.

The unifying convention is the `format` string and the `ok` boolean. That
convention is what makes hundreds of independent checks composable.

## Verified defects and drift

These were observed directly in this checkout. Each one has a reproduction
command at the end of the document.

**The `unique` modifier is dropped during generation.** A DSL field declared
`email: email unique` reaches the canonical schema with `unique=True`, and
`appgen.json` records it, but the generated `models.py` emits
`Column(String, nullable=True)` with no `unique=True` and no
`UniqueConstraint`. The contract and the code disagree.

**The PBC release audit is blocked on this worktree.**
`pbc_agent_capability_release_audit` fails with six gaps (`ar_credit`,
`composition_engine`, `contract_lifecycle`, `customer_success_management`,
`banking_core_accounts`, `claims_adjudication_healthcare`), and
`pbc_package_local_assurance_audit` fails `contract_lifecycle`. The
source-artifact, specification, and implementation audits all pass. Because
`pbc_release_audit` requires all of them, the platform's own top-level gate
cannot reach `approved` here.

**Every capability is marked implemented.** All 93 rows in
`capabilities.py` carry `status: "implemented"`, so the field distinguishes
nothing. Each row also carries a long prose `evidence` string, and no gate
checks that the prose matches what the writers actually emit. The generated
`appgen.json` for a two-table app advertises all 93 capabilities, including
mobile, desktop, voice, and agentic surfaces that the app does not contain.

**The generated app does not describe itself.** The 1,266-file output has no
README, no run instructions, and no entrypoint. The app directory is named by
`--writedir`, but the generated package imports itself as `from app.`, so the
directory must be named `app`.

**`tests/ci/` does not exist and `ruff` is not a dependency.** Both
`~/src/pjs/CLAUDE.md` and this repository's `CLAUDE.md` instruct
`pytest tests/ci` and `ruff check .`. The actual toolchain is black, flake8,
isort, darglint, mypy, and nox. There is no pytest configuration file anywhere,
so a bare `pytest` also walks `archive/`.

**The test suite does not pass as checked in.** With the environment
partially provisioned, the suite reports 449 passed, 71 failed, and 3 collection
errors. Most failures come from missing third-party packages (`inflection`,
`graphene`, `pydbml`, `plotly`) in the interpreter the subprocess tests spawn,
but some are genuine contract drift, such as `test_pbc_dam_core_runtime`
expecting a runtime capability-key set that `dam_core` no longer emits.

**CI cannot pass as written.** `requires-python` is `>=3.14`, but the test and
release workflows use `actions/setup-python@v3`, which predates that release.
The release and safety workflows install `poetry==1.1.13`, which cannot read the
PEP 621 `[project]` table the build now depends on. Coverage is configured with
`fail_under = 100`. The workflows also use the deprecated `::set-output` and the
retired `actions/upload-artifact@v3`.

**The React frontend talks to nothing.** `appgen-frontend/` has no `fetch`, no
socket, and no CLI call; every panel is populated from local TypeScript catalog
modules. `studio.py:269` asserts the "integration" by reading the frontend's own
source files and checking for expected substrings. The frontend is also excluded
from the Poetry build (`pyproject.toml:60`), so it never ships on PyPI.

**The `doctor` check reports a false failure in a bare interpreter.** Its
`template_writers` check fails when `gen.py` cannot import `inflection`, which
is a declared dependency. The three writer functions it looks for exist. This is
an environment artifact, not code drift.

**Repository hygiene.** One hundred forty-eight `.DS_Store` files show as
untracked because the top-level `.gitignore` has no rule for them. The
`archive/` directory is tracked despite its own manifest claiming Git ignores
it, and it contains 218 committed `.pyc` files.

**A documented gotcha is inaccurate.** The project `CLAUDE.md` states that every
generator run writes evidence to a per-build audit directory. No such directory
exists. Evidence is embedded in the output tree, and the per-build behavior that
does exist is that each audit regenerates a throwaway app.

## Where changes are expensive

Two structures will fight every future change.

`gen.py` has two nearly identical generation spines. Any new writer must be
added to both `generate_app_from_database` and `generate_app_from_schema`, or
the two source paths diverge silently.

`pbc.py` has a 46-branch dispatch chain and 1,500 re-export lines that cover
only a third of the catalog. Adding a PBC means touching the chain, the
re-export block, and the catalog update blocks.

Two claims undermine the platform's own thesis and are worth repairing first:
the dropped `unique` constraint, and the blocked `pbc_release_audit`. Both are
places where the code contradicts the contract it publishes.

## Reproducing these measurements

Set `PYTHONPATH` to `src` and install `inflection` first; several checks import
`gen.py`, which imports it at module scope.

```console
# Compile every source file and report failures.
python3 - <<'EOF'
import pathlib, py_compile, tempfile, os
tmp = tempfile.mkdtemp(); bad = []; n = 0
for p in pathlib.Path('src/pyAppGen').rglob('*.py'):
    if '__pycache__' in str(p):
        continue
    n += 1
    try:
        py_compile.compile(str(p), doraise=True, cfile=os.path.join(tmp, f"{n}.pyc"))
    except Exception as e:
        bad.append((str(p), str(e)[:90]))
print("compiled", n, "failures", len(bad))
EOF

# Count files and lines.
find src -name '*.py' -not -path '*__pycache__*' | wc -l
git ls-files 'src/pyAppGen/*.py' | xargs wc -l | tail -1

# Run the suite without aborting on collection errors.
PYTHONPATH=src python3 -m pytest tests -q --continue-on-collection-errors

# Reproduce the unique-modifier drop.
PYTHONPATH=src python3 -c "
from pyAppGen.dsl import schema_from_dsl
from pyAppGen.gen import generate_app_from_schema
import tempfile, pathlib
dsl = 'app T { targets: web }\n\ntable Customer {\n  id: int pk\n  email: string unique\n}\n'
s = schema_from_dsl(dsl)
print('schema unique:', [c.unique for c in s.table('Customer').columns])
d = tempfile.mkdtemp()
generate_app_from_schema(s, d)
print('unique=True in models.py:', 'unique=True' in (pathlib.Path(d)/'models.py').read_text())
"

# Reproduce the blocked release audit.
PYTHONPATH=src python3 -c "
from pyAppGen.pbc import pbc_release_audit, pbc_agent_capability_release_audit
print('full:', pbc_release_audit()['decision'])
print('agent gaps:', len(pbc_agent_capability_release_audit()['blocking_gaps']))
"

# Reproduce the DSL gate results.
PYTHONPATH=src python3 -c "
from pyAppGen.dsl import doctor_report_dsl, dsl_antlr_integrity_report
print('doctor:', [c['check'] for c in doctor_report_dsl()['checks'] if not c['ok']])
print('antlr:', dsl_antlr_integrity_report()['ok'])
"
```
