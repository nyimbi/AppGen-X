# PBC Specification

This guide is for agents and developers building Packaged Business Capabilities
that integrate cleanly with AppGen-X. A PBC must be independently understandable,
self-registering, and composable with other PBCs through APIs and events.

## What A PBC Is

A PBC is a bounded business capability with:

- one stable `pbc` key;
- one mesh classification;
- one owned datastore boundary;
- one approved open-source datastore backend;
- owned tables only;
- command/query APIs;
- emitted and consumed domain events;
- optional UI fragments for the composition canvas;
- optional permissions, configuration, migrations, seed data, tests, and docs.
- optional stream processor profile for event handling.

Do not model a PBC as a shared module that reaches into another PBC's tables.
Cross-PBC integration happens through API calls, projections, or event
subscriptions.

## Package Layout

A reusable PBC package should use this layout:

```text
my_pbc/
  __init__.py
  manifest.py
  api.py
  events.py
  models.py
  ui.py
  permissions.py
  migrations/
    001_initial.sql
  seed/
    sample_data.json
  tests/
    test_contract.py
  docs/
    my-pbc.md
```

The package must expose a `register_pbc()` entrypoint:

```python
def register_pbc() -> dict:
    return {
        "pbc": "warranty_claims",
        "label": "Warranty Claims",
        "mesh": "relationship",
        "description": "Manage warranty intake, eligibility, adjudication, and claim resolution.",
        "datastore_backend": "postgresql",
        "tables": ("warranty_claim", "claim_line", "eligibility_check"),
        "apis": ("POST /warranty-claims", "POST /eligibility-checks", "GET /claim-status"),
        "emits": ("WarrantyClaimOpened", "WarrantyClaimApproved"),
        "consumes": ("ProductPublished", "CustomerUpdated", "OrderShipped"),
        "template": None,
        "ui_fragments": ("WarrantyClaimsWorkbench", "WarrantyClaimDetail"),
        "permissions": ("warranty_claim.read", "warranty_claim.create", "warranty_claim.approve"),
        "configuration": ("WARRANTY_DEFAULT_REGION",),
        "migrations": ("migrations/001_initial.sql",),
        "seed_data": ("seed/sample_data.json",),
        "tests": ("tests/test_contract.py",),
        "docs": ("docs/warranty-claims.md",),
    }
```

## Required Manifest Fields

- `pbc`: lowercase snake_case key. This becomes the datastore, route, event
  topic, and generated table prefix.
- `label`: human-readable catalog label.
- `mesh`: one of the platform meshes from `pbc_mesh_catalog()`.
- `description`: concise bounded-context purpose.
- `datastore_backend`: one of `postgresql`, `mysql`, `mariadb`, `sqlite`,
  `duckdb`, `clickhouse`, `mongodb`, or `opensearch`.
- `tables`: owned table names.
- `apis`: command/query route contracts.
- `emits`: domain events emitted by the PBC.
- `consumes`: domain events consumed from other PBCs or external systems.

Optional fields include `template`, `owner`, `version`, `ui_fragments`,
`stream_processor`, `stream_exception_evidence`, `permissions`,
`configuration`, `migrations`, `seed_data`, `tests`, and `docs`.

`datastore_backend` is also opinionated for ordinary generated work. Prefer
`postgresql`. Use `mysql` or `mariadb` only when that is the project standard.
Other open-source backends are specialized platform-service or integration
choices; they should not expand the ordinary PBC generation path.

`stream_processor` is intentionally opinionated to prevent a combinatorial
backend matrix. For ordinary PBCs, developers have one visible choice:
`appgen_event_contract`. Omit the field. The validator normalizes the missing
field to the platform default, and generated code must route through AppGen-X
outbox/inbox adapters instead of importing a stream library directly in
business logic. Developers and coding agents should model event contracts,
handlers, retry policies, idempotency keys, and dead-letter behavior; they
should not choose a stream library for normal generated applications.
The implementation recipe is fixed: declare commands and events, generate owned
tables, generate transactional outbox/inbox tables, generate typed handlers,
wire handlers through the AppGen-X event adapter, and prove retry,
idempotency, dead-letter, and release-audit coverage. The complete developer
standard lives in `docs/kafka-alternatives.md`.

The generated implementation is fixed for ordinary work: transactional
outbox/inbox tables, the AppGen-X event adapter, the platform default
service-runtime profile, and generated retry/idempotency/dead-letter/release
audit contracts. The IDE and natural-language generator may show that decision
as read-only metadata, but they must not render a stream-engine picker.
Use `lint_pbc_eventing_choice()` before generation to enforce that contract.
The linter accepts an omitted `stream_processor`, rejects hand-authored default
profile fields for ordinary manifests, blocks direct profile-specific imports
from generated business logic, and returns a `remove_stream_processor` quick
fix for ordinary manifests that start branching.

Use the first matching rule:

| Workload | Result |
| --- | --- |
| Ordinary business, ERP, workflow, chatbot, agent, integration, approval, or PBC event handling | Generate `appgen_event_contract` and omit `stream_processor`. |
| Telemetry, time-series, high-volume ingestion, or windowed metrics | Split into a specialized PBC and use `quix_streams` only with `stream_exception_evidence`. |
| Complex parallel dataflow, CPU-heavy transforms, or multi-stage analytical pipelines | Split into a specialized PBC and use `bytewax` only with `stream_exception_evidence`. |
| Anything unclear | Generate `appgen_event_contract` and omit `stream_processor`. |

Allowed values:

- `faust_streaming`: platform default behind the event adapter for
  event-driven microservices, actor-style services, asynchronous workflows,
  saga orchestration, and service-owned local state.
- `quix_streams`: exception for high-throughput event streams, telemetry,
  time-series streams, large ingestion, and windowed operational metrics.
- `bytewax`: exception for complex parallel transformations, stateful dataflow
  graphs, CPU-heavy stream transforms, and multi-stage analytical pipelines.

Do not introduce additional stream processors for ordinary PBC work. The
platform release audit treats this as one default implementation path with two
audited exception profiles, not a three-way preference matrix.

Exception profiles must include machine-checkable `stream_exception_evidence`
in the manifest with `workload_name`, `throughput_or_latency_reason`,
`state_shape`, and `operational_owner`. The same evidence should be explained
in the PBC package docs. The complete platform policy is documented in
[Opinionated Event Processing Guidance](kafka-alternatives.md) and exposed by
`acp_stream_processing_policy()`.

The IDE and natural-language generator should not expose a free-form
stream-engine selector. They should show the default as a generated decision and
open an exception workflow only when the PBC author supplies the required
evidence.
The executable policy's `developer_guidance` field is the source of truth for
Studio controls, DSL lint rules, natural-language generation, and coding-agent
prompts. It tells those tools to generate the standard outbox/inbox adapter
path for ordinary work, hide stream-engine selection, and require exception
evidence before `quix_streams` or `bytewax` can enter a manifest.
For constrained generators, use `acp_event_processing_developer_guidance()`
and read its `decision_brief`: it gives one headline, one ordinary manifest
rule, the compact code-generation prompt, the IDE controls to show, and the
stream-selection controls to hide. This prevents templates and agents from
reopening the alternatives matrix.

For ordinary generated applications, the developer-facing standard event stack
is:

- generated transactional outbox and inbox tables;
- platform event backbone adapter;
- read-only platform default service-runtime profile behind that adapter;
- PBC-owned datastore state only;
- generated release-audit evidence.

The backing broker and adapter implementation are platform infrastructure
concerns. PBC packages declare events and handlers; they do not own a custom
broker, topic client, or state-store selection.

## Validation

Use the platform validator before publishing:

```python
from pyAppGen.pbc import validate_pbc_manifest

report = validate_pbc_manifest(register_pbc())
assert report["ok"]
```

For a publishable PBC, the report should also have `publishable: true`, which
requires tests and docs. Draft PBCs can be valid but not publishable.

The validator rejects:

- missing required fields;
- non-snake-case PBC keys;
- unknown mesh names;
- unsupported datastore backends;
- unsupported stream processor profiles;
- duplicate PBC keys;
- duplicate datastore ownership;
- malformed table/API/event lists.

## Self Registration

Registration is represented as a side-effect-free plan:

```python
from pyAppGen.pbc import register_pbc_manifest

plan = register_pbc_manifest(register_pbc())
assert plan["ok"]
```

The platform then uses the registration plan to expose:

- catalog entry;
- datastore boundary;
- datastore backend;
- stream processor profile;
- API route namespace;
- event topics;
- UI fragments;
- permissions;
- configuration keys;
- migrations and seed data;
- docs and tests.

The registry step should not silently overwrite an existing PBC. A duplicate key
or datastore is a blocking validation error.

Packages can also be loaded directly by the platform:

```python
from pyAppGen.pbc import load_pbc_package

report = load_pbc_package("my_claims_pbc")
```

For local development, pass a source directory containing `__init__.py` and a
`register_pbc()` entrypoint. The loader imports the entrypoint, validates the
returned manifest, and returns a side-effect-free catalog patch instead of
mutating the built-in catalog.

A package index is a JSON file with a `packages` list. Each entry points to a
local `source` path or an importable `module`:

```json
{
  "packages": [
    {
      "name": "Claims",
      "source": "claims_pbc",
      "version": "1.0.0"
    }
  ]
}
```

Use `discover_pbc_package_index(index_path)` to load every entry and return the
validated package reports plus catalog patches.

## Composition Contract

Once registered, the PBC can be selected by key, starter stack, or natural
language. The composition plan verifies owned datastores, deployment units,
internal event dependencies, and external event obligations:

```python
from pyAppGen.pbc import pbc_composition_plan

plan = pbc_composition_plan(("warranty_claims",), app_name="WarrantyDesk")
```

When a PBC consumes an event that is not emitted by the selected set, the plan
records it under `external_event_contracts`. That is not automatically invalid;
it means the generated application needs an integration or upstream event
source.

## Implementation Checklist

1. Define the manifest and `register_pbc()` entrypoint.
2. Keep owned tables scoped to the PBC.
3. Choose `postgresql`, `mysql`, or another approved open-source backend.
4. Define API contracts with HTTP method and path.
5. Omit `stream_processor` for ordinary event handling and let validation use
   the default. Add `quix_streams` or `bytewax` only through the audited
   exception workflow with `stream_exception_evidence`.
6. Define emitted and consumed event names.
7. Add UI fragments for the composition canvas if the PBC has a user surface.
8. Add permissions and configuration keys.
9. Add migrations and seed data.
10. Add contract tests that validate the manifest and generated composition.
11. Add user/operator documentation.
12. Run `pbc_release_audit()` or the CLI release audit before publishing.

## Useful Commands

```console
appgen --pbc-catalog
appgen --pbc-topology
appgen --pbc-release-audit
appgen --pbc-dsl application_composition_platform > acp.appgen
appgen --pbc-dsl gl_core --pbc-dsl ap_automation > finance.appgen
```

## Agent Instructions

When using another coding agent to build a PBC, give it these acceptance
criteria:

- Produce a package with `register_pbc() -> dict`.
- Validate the manifest with `validate_pbc_manifest()`.
- Include docs and tests so `publishable` is true.
- Do not share another PBC's datastore or tables.
- Use only approved open-source datastore backends.
- Omit `stream_processor` for ordinary event handling; use an exception profile
  only when the workload and `stream_exception_evidence` satisfy the platform
  policy.
- Use events for cross-PBC communication.
- Include UI fragments, permissions, configuration, migrations, and seed data
  when relevant.
- Provide a composition smoke test using `pbc_composition_dsl()`.
