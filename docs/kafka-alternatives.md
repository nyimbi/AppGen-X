# Opinionated Event Processing Standard

AppGen-X does not expose every stream-processing option to every generated
application. That creates an exponential support matrix and makes PBC packages
hard to reason about. The platform therefore supports one default event
processor profile and two narrow exception profiles.

## Decision Card

If you are building with AppGen-X, use this answer:

```text
Use the generated outbox/inbox event contract.
Use faust_streaming behind the AppGen-X event adapter.
Do not import stream libraries from generated business logic.
Do not expose a stream-engine picker in the IDE or natural-language flow.
Use exceptions only for telemetry/time-series or complex parallel dataflow
workloads with release-audit evidence.
```

This is a platform decision, not a developer preference. Ordinary generated
business applications, ERP PBCs, approval workflows, agents, chatbots, and
integration handlers all use the same default profile. The IDE may display the
profile as generated metadata, but the editable work is the event model:
commands, emitted events, consumed events, handler ownership, retries,
idempotency keys, dead-letter behavior, and operational runbooks.

The AppGen-X event backbone may use different infrastructure in different
deployments, but generated PBC code still targets the AppGen-X adapter. Do not
add broker-specific clients or profile-specific imports to command handlers,
form actions, chatbot tools, agents, or generated UI code.

## Required Choice

Use `faust_streaming`.

Do not ask the application user, coding agent, natural-language generator, or
PBC author to choose a stream engine for ordinary generated applications. The
generated path is:

1. Write domain data through the PBC's normal repository/service layer.
2. Record integration events in the generated transactional outbox table.
3. Let the generated event adapter publish and consume events through the
   platform event backbone.
4. Put handlers in the generated PBC `events.py` or equivalent generated
   service file.
5. Omit `stream_processor` from the manifest unless the workload is a documented
   exception with machine-checkable `stream_exception_evidence`.

The processor names are platform profile IDs, not an invitation to hand-code
library-specific integrations in every PBC. Generated code should depend on the
AppGen-X event contract first; profile-specific adapters sit behind that
contract.

The developer-facing answer is therefore:

```text
Use the generated outbox/inbox event contract.
Use faust_streaming behind the platform adapter.
Do not expose a stream-engine picker.
Escalate only telemetry/time-series or complex dataflow workloads.
```

## Workload Defaults

| Workload | What to use | Why |
| --- | --- | --- |
| ERP, CRM, HR, finance, inventory, commerce, workflow, approval, chatbot, and agentic application events | `faust_streaming` through the AppGen-X event adapter | Predictable Python-native event services, local state, saga routing, and generated outbox/inbox behavior. |
| PBC command handlers, outbox consumers, API-to-event adapters, human approval tasks, and agent task routing | `faust_streaming` through the AppGen-X event adapter | This is the standard generated service model. |
| High-throughput telemetry, time-series ingestion, large event ingestion, and windowed operational metrics | `quix_streams`, only as an audited exception | The workload is stream-volume and time-window oriented rather than normal domain-event orchestration. |
| Complex parallel dataflow, CPU-heavy transformations, stateful transformation graphs, and analytical pipelines | `bytewax`, only as an audited exception | The workload is a specialized dataflow capability that should normally be split from the core PBC. |

When in doubt, use `faust_streaming`. If the exception reason cannot be written
as measurable evidence, it is not an exception.

## Generator And IDE Contract

Natural-language generation, DSL generation, PBC package validation, and the
IDE must all apply the same behavior:

- For ordinary app prompts, omit `stream_processor` and let validation normalize
  it to `faust_streaming`.
- Show the selected profile as read-only generated metadata in normal PBCs.
- Open an exception workflow only after the developer describes a specialized
  workload.
- Ask for exception evidence, not library preference.
- Fail release validation when an exception profile has no evidence.
- Keep profile-specific dependencies behind AppGen-X adapter modules.

The exception workflow asks only three questions:

1. What named workload requires the exception?
2. What throughput, latency, state, or recovery constraint makes the default
   insufficient?
3. Who owns runtime operations and incidents for this specialized workload?

## Platform Stack

For generated applications, the standard stack is:

| Layer | Standard |
| --- | --- |
| Domain writes | PBC-owned service/repository transaction |
| Event durability | Generated transactional outbox and inbox tables |
| Local development | Platform in-memory event bus plus generated adapters |
| Production integration | Platform event backbone adapter |
| Service runtime | `faust_streaming` profile |
| PBC state | Owned datastore boundary only |
| Cross-PBC changes | Declared API call or emitted event |
| Release proof | PBC release audit and stream-policy gate |

The backing broker is an infrastructure detail behind the platform event
backbone. Application authors model events, handlers, retry policies,
idempotency keys, and dead-letter behavior; they do not choose a broker or
stream library while generating ordinary ERP, workflow, agentic, or composition
applications.

## Default Decision

Use `faust_streaming` for ordinary PBC event handling.

This is the default for:

- command/event handlers;
- outbox consumers;
- workflow and saga orchestration;
- agent task routing;
- service-owned local state;
- API-to-event adapters;
- human approval workflows;
- normal ERP, CRM, inventory, HR, finance, and commerce events.

Generated manifests should omit `stream_processor` unless they need an
exception. The validator normalizes missing values to `faust_streaming`.

The platform UI should show the selected profile as a read-only generated
decision for normal PBCs. It should expose an exception workflow only when the
developer provides the evidence listed below.

Natural-language generation must follow the same rule. If the user asks for an
ERP, CRM, HR, inventory, finance, chatbot, agent, or workflow app, the generator
uses the default profile without asking. If the prompt says "massive telemetry
ingestion" or "parallel analytical stream transformation," the generator may
propose an exception but must still emit the required evidence and let validation
approve or reject the manifest.

## Allowed Profiles

| Profile | Decision | Use only when |
| --- | --- | --- |
| `faust_streaming` | Default | The PBC is an event-driven service, workflow participant, saga orchestrator, outbox consumer, or agent task handler. |
| `quix_streams` | Exception | The PBC owns high-throughput telemetry, time-series streams, large ingestion, or windowed operational metrics. |
| `bytewax` | Exception | The PBC owns complex parallel dataflow, CPU-heavy transformation graphs, stateful analytical pipelines, or multi-stage transformations. |

Do not add another profile for a single PBC. A fourth option requires a
platform architecture decision and a new release-audit gate.

Do not combine profiles in one PBC. If a capability has both normal workflow
events and specialized telemetry or dataflow needs, split the specialized
workload into its own PBC or generated integration capability with a separate
manifest and datastore boundary.

## Developer Rule

Start with `faust_streaming`. Move away from it only when the workload has a
measurable reason that matches an exception.

Use this decision tree:

1. Is this ordinary domain-event handling, outbox delivery, workflow
   orchestration, approval routing, or agent task execution? Use
   `faust_streaming`.
2. Is the workload primarily telemetry, time-series, high-volume ingestion, or
   windowed operational metrics? Use `quix_streams`.
3. Is the workload primarily complex parallel transformation, CPU-heavy stream
   processing, or a multi-stage stateful dataflow graph? Use `bytewax`.
4. If none of those exception cases are clearly true, use `faust_streaming`.

For generated ERP, CRM, HR, inventory, finance, workflow, chatbot, and agentic
application logic, the answer is almost always `faust_streaming`.

## What Developers Actually Build

Developers and coding agents should build the same generated surface regardless
of the profile:

- `models.py`: owned tables plus generated outbox and inbox mappings.
- `services.py`: command handlers that mutate owned state and enqueue events.
- `events.py`: typed handlers, idempotency keys, retry policy names, and
  dead-letter contracts.
- `api.py`: synchronous command/query routes.
- `pbc_runtime.py`: manifest, selected stream profile, topic names, and
  release-audit evidence.
- package docs: event contracts, handler ownership, operational owner, and
  exception evidence when applicable.

Do not import `faust_streaming`, `quix_streams`, or `bytewax` directly in
business logic. If generated code needs a profile-specific dependency, it
belongs in the platform adapter layer, not in PBC command handlers, form code,
agents, or generated UI actions.

## Generated Implementation Recipe

For a normal PBC, generate this structure:

- `models.py`: owned tables plus an outbox table or generated outbox mapping.
- `services.py`: command handlers that mutate owned state and enqueue events.
- `events.py`: typed event handlers, retry policy names, and idempotency keys.
- `api.py`: synchronous command/query routes.
- `pbc_runtime.py`: manifest, stream profile, topic names, and release-audit
  evidence.

Handlers should be deterministic, idempotent, and scoped to the owning PBC's
datastore. Cross-PBC changes happen by emitting events or calling declared APIs;
handlers must not reach into another PBC's tables.

For local development and generated smoke tests, use the platform event
backbone abstraction and the generated outbox/inbox adapters. PBC packages
should not hardcode a broker, topic client, or state-store implementation
outside the generated adapter layer.

## Exception Workflow

Exception selection is an audit workflow, not a preference prompt.

1. The PBC author describes the workload.
2. `select_acp_stream_processor()` classifies the workload as default or
   exception.
3. Exception manifests must include `stream_exception_evidence`.
4. `validate_pbc_manifest()` rejects missing or unsupported evidence.
5. `pbc_release_audit()` records the stream policy gate.
6. The IDE shows the exception reason as a generated decision, not a general
   menu of libraries.

If evidence cannot be supplied, use `faust_streaming`.

## Exception Evidence

Any PBC using `quix_streams` or `bytewax` must include
`stream_exception_evidence` in its manifest with:

- `workload_name`: the named stream workload;
- `throughput_or_latency_reason`: why the default is not enough;
- `state_shape`: what state is kept and how it is recovered;
- `operational_owner`: who owns runtime operations and incidents.

This evidence belongs in the PBC manifest and should also be explained in the
package docs or package README.

If the evidence is absent, the PBC must use `faust_streaming` and the release
audit should fail any attempted exception.

## What Is Prohibited

- Per-PBC custom stream engines.
- Mixing multiple stream processors inside one PBC.
- Sharing stream-state stores across PBC datastore boundaries.
- Asking natural-language generation to compare stream libraries.
- Selecting an exception profile because it is newer, faster in theory, or
  preferred by a developer.
- Adding a fourth profile without updating `pbc.py`, the PBC specification,
  generated docs, tests, and release audits.
- Exposing a free-form stream-engine selector in the IDE or natural-language
  generator.
- Importing profile-specific stream libraries directly in generated business
  logic.

## Why This Is The Default

Most AppGen-X applications are generated from natural language, DSL, visual
composition, or PBC selection. They need predictable event contracts more than
an open-ended infrastructure menu. The default profile keeps generated services
small, Python-native, testable, and consistent with the PBC model: each
capability owns its datastore, API, events, and local event-processing state.

The exception profiles exist for specialized workloads that would otherwise
distort the default service model.

## Manifest Examples

Default PBCs should either omit the field:

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

Or state the default explicitly:

```python
"stream_processor": "faust_streaming"
```

Use an exception only with matching evidence:

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

## Platform Enforcement

The executable policy lives in `src/pyAppGen/pbc.py`:

- `acp_stream_processing_policy()` returns the default, allowed profiles,
  opinionated stack, generated outputs, decision tree, required exception
  evidence, and prohibited patterns.
- `select_acp_stream_processor()` maps a workload description to the default
  or an exception profile.
- `validate_pbc_manifest()` rejects unsupported profiles, normalizes missing
  profiles to the default, and blocks exception profiles without
  `stream_exception_evidence`.
- `pbc_release_audit()` includes an `opinionated_stream_processing_policy`
  release gate.

This means the recommendation is part of the platform contract, not only
documentation.
