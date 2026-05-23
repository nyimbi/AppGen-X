# Opinionated Event Processing Standard

AppGen-X does not ask application developers, natural-language generators,
coding agents, or Studio users to choose among stream-processing engines for
ordinary generated applications. That choice would create a support matrix that
grows faster than the platform can validate.

The platform choice is:

```text
Use generated transactional outbox/inbox tables.
Use the AppGen-X event adapter.
Use faust_streaming behind that adapter for ordinary generated work.
Do not import stream libraries from generated business logic.
```

This document is the developer-facing companion to the executable policy in
`src/pyAppGen/pbc.py`.

## Required Default

Use `faust_streaming` for ordinary generated applications and PBCs.

Ordinary work includes:

- ERP, CRM, HR, finance, inventory, commerce, and operations events;
- PBC command handlers and outbox consumers;
- workflow sagas and approval routing;
- chatbot events and agent task routing;
- API-to-event adapters and integration handlers;
- form actions and generated UI actions that emit business events.

Generated manifests should normally omit `stream_processor`. Validation
normalizes the missing value to `faust_streaming`.

```python
def register_pbc() -> dict:
    return {
        "pbc": "warranty_claims",
        "label": "Warranty Claims",
        "mesh": "relationship",
        "description": "Manage warranty intake and claim resolution.",
        "datastore_backend": "postgresql",
        "tables": ("warranty_claim", "claim_line"),
        "apis": ("POST /warranty-claims", "GET /claim-status"),
        "emits": ("WarrantyClaimOpened",),
        "consumes": ("OrderShipped", "CustomerUpdated"),
    }
```

The explicit default is accepted, but it is not required:

```python
"stream_processor": "faust_streaming"
```

## What Developers Actually Use

Developers and agents build against the AppGen-X event contract, not a broker
or stream library. Generate the same surface for normal PBCs every time:

| File or surface | Generated responsibility |
| --- | --- |
| `models.py` | Owned tables plus generated transactional outbox/inbox mappings. |
| `services.py` | Command handlers that mutate owned state and enqueue events. |
| `events.py` | Typed handlers, idempotency keys, retry policies, and dead-letter contracts. |
| `api.py` | Synchronous command/query routes. |
| `pbc_runtime.py` | Manifest, topic names, selected profile metadata, and release-audit evidence. |
| package docs | Event contracts, handler ownership, operational owner, and exception evidence when present. |

Generated business logic must not import `faust_streaming`, `quix_streams`, or
`bytewax` directly. Profile-specific dependencies belong behind platform
adapter modules.

## Allowed Profiles

AppGen-X allows one default and two audited exceptions.

| Profile | Decision | Use only when |
| --- | --- | --- |
| `faust_streaming` | Default | The PBC is an event-driven service, workflow participant, saga orchestrator, outbox consumer, integration handler, or agent task handler. |
| `quix_streams` | Exception | The PBC owns high-throughput telemetry, time-series streams, large ingestion, or windowed operational metrics. |
| `bytewax` | Exception | The PBC owns complex parallel dataflow, CPU-heavy transformation graphs, stateful analytical pipelines, or multi-stage transformations. |

Do not add another profile for a project. A fourth option requires a platform
architecture decision, executable validation, release-audit coverage, generated
documentation, and tests.

Do not mix profiles inside one PBC. If a capability has ordinary business
events plus a specialized telemetry or dataflow workload, split the specialized
workload into its own PBC or generated integration capability with a separate
manifest and datastore boundary.

## Decision Tree

Use this decision tree in docs, prompts, IDE controls, DSL linting, and
generator code:

1. Is this ordinary domain-event handling, outbox delivery, workflow
   orchestration, approval routing, integration handling, or agent task
   execution? Use `faust_streaming`.
2. Is the workload primarily telemetry, time-series ingestion, high-volume
   event ingestion, or windowed operational metrics? Use `quix_streams`, but
   only with exception evidence.
3. Is the workload primarily complex parallel transformation, CPU-heavy stream
   processing, or a multi-stage stateful dataflow graph? Use `bytewax`, but
   only with exception evidence.
4. If the exception case is not clear and measurable, use `faust_streaming`.

The default answer is not "choose a Kafka alternative." The default answer is
"generate the AppGen-X outbox/inbox contract and route through the platform
adapter."

## Exception Evidence

Exception selection is an audit workflow, not a preference prompt.

Any PBC using `quix_streams` or `bytewax` must include
`stream_exception_evidence` with:

- `workload_name`: the named specialized workload;
- `throughput_or_latency_reason`: the measurable reason the default is not
  enough;
- `state_shape`: what state is kept and how it is recovered;
- `operational_owner`: who owns runtime operations and incidents.

Example:

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

Without the evidence, use `faust_streaming`.

## IDE, DSL, And Agent Contract

Studio, DSL tooling, natural-language generation, and external coding agents
must all follow the same contract:

- hide stream-engine selection for ordinary app generation;
- show the selected profile as read-only generated metadata;
- ask developers to model commands, events, handlers, retries, idempotency,
  dead-letter behavior, and ownership;
- open an exception workflow only after the workload matches one of the two
  exception categories;
- ask for exception evidence, not library preference;
- fail release validation when an exception profile has no evidence;
- keep profile-specific dependencies behind AppGen-X adapter modules.

For prompts such as "build invoicing," "add HR onboarding," "create an
inventory workflow," "add a support chatbot," or "generate an approval agent,"
the generator must use the default silently and emit the standard event
artifacts.

## Platform Stack

For ordinary generated applications, the standard stack is:

| Layer | Standard |
| --- | --- |
| Domain writes | PBC-owned service/repository transaction. |
| Event durability | Generated transactional outbox and inbox tables. |
| Local development | AppGen-X in-memory event bus plus generated adapters. |
| Production integration | Platform event backbone adapter. |
| Service runtime | `faust_streaming` profile. |
| PBC state | Owned datastore boundary only. |
| Cross-PBC changes | Declared API call or emitted event. |
| Release proof | PBC release audit and stream-policy gate. |

The backing broker is infrastructure behind the event backbone. Application
authors model event contracts; they do not own broker selection, topic client
selection, or stream-state-store selection.

## What Is Prohibited

- Per-PBC custom stream engines.
- Mixing multiple stream processors inside one PBC.
- Sharing stream-state stores across PBC datastore boundaries.
- Asking natural-language generation to compare stream libraries.
- Selecting an exception profile because it is newer, faster in theory, or
  preferred by a developer.
- Exposing a free-form stream-engine selector in the Studio or natural-language
  generator.
- Importing profile-specific stream libraries directly in generated business
  logic.

## Enforcement

The executable policy lives in `src/pyAppGen/pbc.py`:

- `acp_stream_processing_policy()` returns the default, allowed profiles,
  decision card, developer guidance, generated outputs, decision tree, required
  exception evidence, and prohibited patterns.
- `select_acp_stream_processor()` classifies workload descriptions as default
  or exception candidates.
- `validate_pbc_manifest()` rejects unsupported profiles, normalizes missing
  profiles to the default, and blocks exception profiles without
  `stream_exception_evidence`.
- `pbc_release_audit()` includes an `opinionated_stream_processing_policy`
  release gate.

This makes the recommendation part of the platform contract, not only a
documentation preference.
