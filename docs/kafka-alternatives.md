# Opinionated Event Processing Standard

This document is the developer-facing answer to "what should I use instead of
Kafka?" in AppGen-X.

The answer for ordinary generated applications is not a product comparison:

```text
Use appgen_event_contract.
Omit stream_processor.
Generate transactional outbox/inbox tables and typed handlers.
Route handlers through the AppGen-X event adapter.
Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.
```

Developers, Studio users, DSL authors, natural-language generators, package
templates, and coding agents should all receive that same answer. The platform
owns the runtime profile behind the adapter.

## Normative Choice

AppGen-X exposes one ordinary event-processing choice:

| Question | Platform answer |
| --- | --- |
| Public event contract | `appgen_event_contract` |
| Ordinary manifest rule | Omit `stream_processor` |
| Ordinary database rule | PostgreSQL by default; MySQL/MariaDB when that is the project standard |
| Generated durability | `appgen_outbox_event` and `appgen_inbox_event` |
| Generated handler API | Typed handlers through the AppGen-X event adapter |
| Developer-visible stream-engine choices | `0` |
| Developer-visible event-contract choices | `1` |
| Runtime profile visibility | Read-only generated metadata |

The platform currently records `faust_streaming` as the default internal
service-runtime profile after validation. Treat it as platform metadata, not as
a field ordinary developers choose or hand-author.

## Why This Is Mandatory

Every extra visible event runtime multiplies generated-app validation across:

- datastore backend;
- target packaging for web, mobile, and desktop;
- generated adapter code;
- deployment profile;
- PBC ownership boundary;
- local development mode;
- release-audit evidence;
- external coding-agent prompts.

That creates an exponential support matrix. AppGen-X avoids it by making the
ordinary path a single generated event contract and moving runtime details
behind the platform adapter.

## What Developers Build

Developers model business intent:

- commands;
- events;
- business tables;
- handler functions;
- retry and dead-letter semantics;
- ownership and operational notes.

AppGen-X generates:

- owned table mappings;
- `appgen_outbox_event`;
- `appgen_inbox_event`;
- typed command and event handlers;
- event adapter bindings;
- retry policy;
- idempotency keys;
- dead-letter envelope;
- release-audit evidence.

Generated business logic imports the AppGen-X event adapter only. It must not
import `faust_streaming`, `quix_streams`, `bytewax`, broker clients, or
profile-specific state-store libraries directly.

## Ordinary Manifest Shape

Use this shape for ordinary PBCs and generated modules:

```python
def register_pbc() -> dict:
    return {
        "pbc": "invoicing",
        "label": "Invoicing",
        "mesh": "finops",
        "description": "Issue invoices, post invoice events, and track payment status.",
        "datastore_backend": "postgresql",
        "tables": ("invoice", "invoice_line", "payment_allocation"),
        "apis": ("POST /invoices", "GET /invoices/{id}"),
        "emits": ("InvoiceIssued", "InvoicePaid"),
        "consumes": ("OrderReleased", "PaymentReceived"),
    }
```

Notice what is absent: ordinary manifests do not include `stream_processor`.
Validation records the selected internal runtime profile as generated metadata.

## Selection Algorithm

Use this first-match algorithm in Studio, DSL linting, natural-language
generation, package templates, and external coding-agent prompts:

```text
if workload is ordinary business/workflow/integration/agent/PBC event handling:
    public_contract = appgen_event_contract
    manifest.stream_processor = omitted
elif workload is telemetry, time-series, high-volume ingestion, or windowed metrics:
    require stream_exception_evidence
    split specialized PBC
    manifest.stream_processor = quix_streams
elif workload is complex parallel dataflow, CPU-heavy transformation, or multi-stage analytical pipeline:
    require stream_exception_evidence
    split specialized PBC
    manifest.stream_processor = bytewax
else:
    public_contract = appgen_event_contract
    manifest.stream_processor = omitted
```

If the request is unclear, use `appgen_event_contract` and omit
`stream_processor`.

## Exception Lanes

There are exactly two exception profiles. They are audit workflows, not user
preferences.

| Workload | Exception profile | Required evidence |
| --- | --- | --- |
| Telemetry, time-series, high-volume ingestion, or windowed operational metrics | `quix_streams` | `stream_exception_evidence` |
| Complex parallel dataflow, CPU-heavy transformations, or multi-stage analytical pipelines | `bytewax` | `stream_exception_evidence` |

If a PBC has both ordinary domain events and a specialized telemetry or
dataflow workload, split the specialized workload into its own PBC with its own
datastore boundary and manifest.

## Exception Evidence

An exception manifest must include machine-checkable evidence:

```python
def register_pbc() -> dict:
    return {
        "pbc": "machine_telemetry",
        "label": "Machine Telemetry",
        "mesh": "opsmfg",
        "description": "Ingest and aggregate equipment telemetry windows.",
        "datastore_backend": "postgresql",
        "stream_processor": "quix_streams",
        "stream_exception_evidence": {
            "workload_name": "equipment telemetry windows",
            "throughput_or_latency_reason": "high-volume time-series ingestion",
            "state_shape": "per-machine rolling windows persisted by watermark",
            "operational_owner": "opsmfg telemetry platform team",
        },
        "tables": ("telemetry_sample", "telemetry_window"),
        "apis": ("POST /telemetry", "GET /telemetry-windows"),
        "emits": ("TelemetryWindowCalculated",),
        "consumes": ("MachineSignalReceived",),
    }
```

Without `workload_name`, `throughput_or_latency_reason`, `state_shape`, and
`operational_owner`, validation must reject the exception and generators must
fall back to the ordinary event contract.

## Studio, DSL, And Agent Rules

Build the ordinary path and hide the runtime matrix.

| Surface | Build this | Do not build this |
| --- | --- | --- |
| Studio | Event contract designer, handler registry editor, retry/idempotency/dead-letter editor, read-only runtime profile badge | Stream-engine picker, broker picker, state-store picker, per-PBC runtime preference |
| DSL linter | Missing `stream_processor` as the valid ordinary form, quick fix to remove explicit default profile, exception evidence gate, direct runtime-import blocker | Rules that ask ordinary PBC authors to select a stream runtime |
| Natural-language generation | Map ordinary ERP, workflow, chatbot, agent, integration, approval, and PBC prompts to `appgen_event_contract` | Runtime comparison prompts or generated decision matrices |
| Package templates | Outbox/inbox tables, adapter bindings, retry, idempotency, dead-letter, release evidence | Profile-specific imports in generated business logic |
| External coding agents | Short prompt that names the ordinary contract and stop rule | Prompts that ask agents to compare stream engines for ordinary apps |

For small local models and token-constrained agents, use this exact prompt:

```text
Use appgen_event_contract. Omit stream_processor. Generate outbox/inbox tables,
typed handlers, retry, idempotency, dead-letter, and release evidence through
the AppGen-X event adapter. Do not compare runtimes. Open an exception only for
telemetry/time-series or complex dataflow with stream_exception_evidence.
```

## Generated Files

Ordinary generated PBCs should produce this event surface:

| File or surface | Responsibility |
| --- | --- |
| `models.py` | Owned business tables plus generated outbox/inbox mappings |
| `events.py` | Typed event schemas, handler registry, idempotency keys, retry policy names, dead-letter shape |
| `services.py` | Command handlers that mutate owned state and enqueue events in one transaction |
| `api.py` | Synchronous command/query routes |
| `pbc_runtime.py` | Manifest, topic names, read-only runtime profile metadata, release evidence |
| package docs | Event contracts, handler ownership, operational owner, exception evidence when present |

## Enforcement

The executable source of truth is `src/pyAppGen/pbc.py`.

Use these APIs rather than reimplementing the decision:

```python
from pyAppGen.pbc import acp_event_processing_developer_guidance
from pyAppGen.pbc import lint_pbc_eventing_choice
from pyAppGen.pbc import resolve_acp_event_processing_choice

guidance = acp_event_processing_developer_guidance()
assert guidance["answer"] == "Use appgen_event_contract."
assert guidance["ordinary_manifest_instruction"] == "Omit stream_processor."

decision = resolve_acp_event_processing_choice("build invoicing approvals")
assert decision["action"] == "generate_appgen_event_contract"

report = lint_pbc_eventing_choice(register_pbc())
assert report["ok"]
```

The linter must:

- accept ordinary manifests that omit `stream_processor`;
- reject ordinary manifests that hand-author the default runtime profile;
- require `stream_exception_evidence` for exception profiles;
- block profile-specific imports from generated business logic;
- offer a `remove_stream_processor` quick fix for ordinary manifests.

The PBC release audit includes an `opinionated_stream_processing_policy` gate,
so this guidance is a platform contract, not only documentation.

## Prohibited

Do not add these to ordinary generated applications:

- stream-engine picker;
- broker picker;
- state-store picker;
- per-PBC runtime preference;
- multiple stream profiles in one PBC;
- direct imports of stream-processing libraries from generated business logic;
- natural-language prompts that compare runtimes for ordinary generated work;
- project-specific fourth stream profile without a platform architecture
  decision, executable validation, release gate, generated tests, and docs.

## Short Answer

For ordinary AppGen-X applications:

```text
Use appgen_event_contract.
Omit stream_processor.
Generate outbox/inbox tables and typed handlers through the AppGen-X event adapter.
Do not ask the developer to choose a stream engine.
```

For telemetry/time-series or complex dataflow, split a specialized PBC and
require evidence. Everything else stays on the ordinary contract.
