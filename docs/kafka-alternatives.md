# Opinionated Event Processing Guidance

AppGen-X does not expose every stream-processing option to every generated
application. That creates an exponential support matrix and makes PBC packages
hard to reason about. The platform therefore supports one default event
processor profile and two narrow exception profiles.

## Platform Decision

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

## Allowed Profiles

| Profile | Decision | Use only when |
| --- | --- | --- |
| `faust_streaming` | Default | The PBC is an event-driven service, workflow participant, saga orchestrator, outbox consumer, or agent task handler. |
| `quix_streams` | Exception | The PBC owns high-throughput telemetry, time-series streams, large ingestion, or windowed operational metrics. |
| `bytewax` | Exception | The PBC owns complex parallel dataflow, CPU-heavy transformation graphs, stateful analytical pipelines, or multi-stage transformations. |

Do not add another profile for a single PBC. A fourth option requires a
platform architecture decision and a new release-audit gate.

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

## Exception Evidence

Any PBC using `quix_streams` or `bytewax` must document:

- `workload_name`: the named stream workload;
- `throughput_or_latency_reason`: why the default is not enough;
- `state_shape`: what state is kept and how it is recovered;
- `operational_owner`: who owns runtime operations and incidents.

This evidence belongs in the PBC package docs and can be summarized in the
PBC manifest comments or package README.

## What Is Prohibited

- Per-PBC custom stream engines.
- Mixing multiple stream processors inside one PBC.
- Sharing stream-state stores across PBC datastore boundaries.
- Selecting an exception profile because it is newer, faster in theory, or
  preferred by a developer.
- Adding a fourth profile without updating `pbc.py`, the PBC specification,
  generated docs, tests, and release audits.

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
        "tables": ("telemetry_sample", "telemetry_window"),
        "apis": ("POST /telemetry", "GET /telemetry-windows"),
        "emits": ("TelemetryWindowCalculated",),
        "consumes": ("MachineSignalReceived",),
    }
```

## Platform Enforcement

The executable policy lives in `src/pyAppGen/pbc.py`:

- `acp_stream_processing_policy()` returns the default, allowed profiles,
  decision tree, required exception evidence, and prohibited patterns.
- `select_acp_stream_processor()` maps a workload description to the default
  or an exception profile.
- `validate_pbc_manifest()` rejects unsupported profiles and normalizes missing
  profiles to the default.
- `pbc_release_audit()` includes an `opinionated_stream_processing_policy`
  release gate.

This means the recommendation is part of the platform contract, not only
documentation.
