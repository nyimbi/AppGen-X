# Opinionated Event Processing Standard

## Developer Recommendation Card

Use this answer for ordinary generated applications and PBCs:

```text
Use appgen_event_contract.
Omit stream_processor.
Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.
```

Developers write commands, events, business tables, and handler functions.
AppGen-X generates:

- `appgen_outbox_event`
- `appgen_inbox_event`
- event adapter bindings
- retry policy
- idempotency keys
- dead-letter contract
- release-audit evidence

Do not ask developers to choose a stream engine, broker client, state store, or
per-PBC runtime profile for ordinary work. The service-runtime profile is
platform-owned metadata behind the AppGen-X event adapter. It can be shown as a
read-only badge after generation, but it is not a manifest field, wizard
question, or Studio picker.

Only two exits exist:

| Exit | When it is allowed | Required evidence |
| --- | --- | --- |
| Telemetry exception | Telemetry, time-series, high-volume ingestion, or windowed operational metrics | `stream_exception_evidence` |
| Dataflow exception | Complex parallel dataflow, CPU-heavy transformations, or multi-stage analytical pipelines | `stream_exception_evidence` |

If the prompt is unclear, ordinary business work, ERP, workflow, chatbot,
agentic orchestration, integration, approval, or PBC event handling, use the
ordinary answer and stop branching.

## Start Here: The Platform Choice

AppGen-X makes the event-processing choice for application developers.
Developers should not choose a Kafka alternative, stream engine, broker client,
state store, or per-PBC runtime profile for ordinary generated applications.

Use this for ordinary ERP, workflow, chatbot, agentic, integration, approval,
and PBC event handling:

```text
Use appgen_event_contract.
Omit stream_processor.
Generate appgen_outbox_event and appgen_inbox_event.
Generate typed command/event handlers through the AppGen-X event adapter.
Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.
```

That is the developer-facing answer. The platform may record
`faust_streaming` as read-only generated runtime metadata behind the adapter,
but developers and coding agents must not author that as an ordinary manifest
choice.

The only exception lanes are evidence-gated specialized PBCs:

| Workload | What to use | Required evidence |
| --- | --- | --- |
| Ordinary business events, ERP, workflow, approval, chatbot, agent, integration, or PBC event handling | `appgen_event_contract`; omit `stream_processor` | None |
| Telemetry, time-series, high-volume ingestion, or windowed metrics | `quix_streams` exception profile | `stream_exception_evidence` |
| Complex parallel dataflow, CPU-heavy transformations, or multi-stage analytical pipelines | `bytewax` exception profile | `stream_exception_evidence` |
| Anything unclear | `appgen_event_contract`; omit `stream_processor` | None |

This first-match rule is mandatory. If the request does not clearly name one
of the two exception workloads and include evidence, generators must stop
branching and produce the ordinary AppGen-X event contract.

## Anti-Explosion Rule

The support matrix is capped as a platform invariant:

```text
ordinary visible event contracts: 1
ordinary visible stream-engine choices: 0
ordinary visible runtime-profile choices: 0
stream profiles per PBC: 1
exception profiles: 2
```

Do not derive a product-selection matrix from the comparison background. The
generator, IDE, DSL linter, natural-language flow, package template, and
external coding-agent prompt must all read the same executable policy:

```python
from pyAppGen.pbc import acp_event_processing_developer_guidance

guidance = acp_event_processing_developer_guidance()
assert guidance["answer"] == "Use appgen_event_contract."
assert guidance["ordinary_manifest_instruction"] == "Omit stream_processor."
assert guidance["developer_action_contract"]["developer_visible_options"] == (
    "appgen_event_contract",
)
```

For token-constrained models, pass this exact prompt fragment:

```text
Use appgen_event_contract. Omit stream_processor. Generate outbox/inbox tables,
typed handlers, retry, idempotency, dead-letter, and release evidence through
the AppGen-X event adapter. Do not compare runtimes. Open an exception only for
telemetry/time-series or complex dataflow with stream_exception_evidence.
```

Generated business logic imports only the AppGen-X event adapter. Direct
imports of `faust_streaming`, `quix_streams`, `bytewax`, broker clients, or
profile-specific state-store libraries belong in platform adapter modules, not
in generated PBC services.

## Developer Default Stack

Do not ask application developers which event-streaming runtime, broker client,
or state store to use for ordinary generated applications. The platform answer
is fixed:

```text
database: PostgreSQL by default, or MySQL/MariaDB when that is the project standard
public contract: appgen_event_contract
durability: appgen_outbox_event + appgen_inbox_event
handlers: typed command handlers + typed event handlers
integration API: AppGen-X event adapter
operations: idempotency, retry, dead-letter, and release evidence
manifest: omit stream_processor
developer choice count: 1
```

This is the stack that the IDE, DSL linter, natural-language generator,
package templates, and coding agents must generate for ordinary ERP, workflow,
chatbot, agent, integration, approval, and PBC event handling. The runtime
profile is read-only platform metadata. It is not a developer-authored
manifest field and it is not a picker in the IDE.

The platform intentionally blocks the expansion axes that create the support
matrix explosion:

- no stream-engine picker for ordinary applications;
- no broker-client picker for ordinary applications;
- no state-store picker for ordinary applications;
- no per-PBC runtime preference for ordinary applications;
- no direct imports of stream-processing libraries from generated business
  logic;
- no natural-language prompt that compares runtimes for ordinary generated
  work.

Use the executable contract when generating code:

```python
from pyAppGen.pbc import acp_event_processing_developer_guidance

guidance = acp_event_processing_developer_guidance()
stack = guidance["developer_default_stack"]
assert stack["use"] == "appgen_event_contract"
assert stack["ordinary_manifest"] == {"stream_processor": "omit"}
```

## Implementation Decision

Developers should use one answer for ordinary AppGen-X work:

```text
Use appgen_event_contract.
Omit stream_processor.
Generate transactional outbox/inbox tables and typed handlers.
Route handlers through the AppGen-X event adapter.
```

This is not a chooser. Studio, DSL templates, natural-language generation,
PBC package templates, and external coding agents must not present stream
runtime options for ordinary generated applications. The platform records its
service-runtime profile as read-only metadata after validation.

Only two exception workflows are available:

| Workload evidence | Exception profile |
| --- | --- |
| Telemetry, time-series, high-volume ingestion, or windowed metrics | `quix_streams` |
| Complex parallel dataflow, CPU-heavy transformations, or multi-stage analytical pipelines | `bytewax` |

Both exception profiles require `stream_exception_evidence`. If the request is
ordinary ERP, workflow, chatbot, agent, integration, approval, or PBC event
handling, the generator must stop at `appgen_event_contract` and avoid stream
runtime comparison.

## Developer Action Contract

When a developer, Studio screen, DSL linter, package template, natural-language
generator, or external coding agent needs the short answer, use the executable
`developer_action_contract` exposed by
`acp_event_processing_developer_guidance()`:

```text
Use appgen_event_contract.
Omit stream_processor.
Generate owned tables, appgen_outbox_event, appgen_inbox_event, typed handlers,
retry, idempotency, dead-letter, and release evidence through the AppGen-X
event adapter.
Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.
Do not compare runtimes.
```

The ordinary choice budget is fixed:

```text
ordinary visible event contracts: 1
ordinary visible stream-engine choices: 0
ordinary visible runtime-profile choices: 0
stream profiles per PBC: 1
```

Hide stream-engine, runtime-profile, broker, state-store, and per-PBC runtime
preference controls on the ordinary generation path. Show the selected runtime
profile only as read-only generated metadata after validation.

Exception workflows are not preferences. They open only when the workload and
evidence are explicit:

- `quix_streams`: telemetry, time-series, high-volume ingestion, or windowed
  metrics with `stream_exception_evidence`;
- `bytewax`: complex parallel dataflow or CPU-heavy transformations with
  `stream_exception_evidence`.

If the exception workload and evidence are not explicit, generate
`appgen_event_contract` and omit `stream_processor`.

## Developer Guidance

Use the generated AppGen-X event contract.

For ordinary generated applications, ERP modules, workflows, chatbots, agents,
integrations, and PBCs, developers do not select a broker, stream processor,
state store, or library. They model commands and events; AppGen-X generates
owned tables, transactional outbox/inbox tables, typed handlers, retry,
idempotency, dead-letter, and release evidence behind the platform event
adapter.

The ordinary manifest rule is:

```text
Use appgen_event_contract.
Omit stream_processor.
```

Only two exception lanes exist, and both require `stream_exception_evidence`:

- telemetry, time-series, high-volume ingestion, or windowed metrics use the
  telemetry exception profile;
- complex parallel dataflow, CPU-heavy stream transforms, or multi-stage
  analytical pipelines use the dataflow exception profile.

If the workload is unclear, generate the ordinary contract and stop branching.
This is how AppGen-X avoids multiplying every generated app by stream runtime,
datastore, adapter, target package, deployment profile, and PBC variant.

## What To Use

The developer answer is not a product comparison. Use this every time for
ordinary application generation:

```text
public contract: appgen_event_contract
manifest: omit stream_processor
generated durability: appgen_outbox_event and appgen_inbox_event
generated handlers: typed command/event handlers through the AppGen-X adapter
runtime profile: read-only platform metadata
developer choice count: 1
```

Developers, Studio screens, DSL templates, and coding agents should call the
same executable guardrail before generation:

```python
from pyAppGen.pbc import lint_pbc_eventing_choice

report = lint_pbc_eventing_choice(register_pbc())
assert report["ok"]
```

That linter is intentionally stricter than manifest normalization. A missing
`stream_processor` is the correct ordinary manifest. A hand-written
`stream_processor: faust_streaming` is treated as branching and receives the
`remove_stream_processor` quick fix, because the runtime profile belongs to
platform metadata after validation, not to the developer-authored contract.

If generated business logic imports profile-specific stream libraries, the
linter fails with `generated_business_logic_imports_appgen_event_adapter_only`.
That is the practical rule that closes the exponential matrix: business code
uses the AppGen-X adapter; platform adapter modules own runtime details.

## Platform Developer Playbook

When adding event-processing support to AppGen-X surfaces, build the ordinary
path and hide the runtime matrix.

| Surface | Build this | Do not build this |
| --- | --- | --- |
| Studio | Event contract designer, handler registry editor, retry/idempotency/dead-letter editor, and read-only runtime profile badge | Stream-engine picker, broker picker, state-store picker, or per-PBC runtime preference |
| DSL linter | `ordinary_pbc_manifest_omits_stream_processor`, `remove_stream_processor` quick fix, exception evidence gate, and profile-specific import blocker | Rules that ask ordinary PBC authors to select a stream runtime |
| Natural-language generation | Map ordinary ERP, workflow, chatbot, agent, integration, approval, and PBC prompts to `appgen_event_contract` | Runtime comparison prompts or generated decision matrices |
| Package templates | `appgen_outbox_event`, `appgen_inbox_event`, adapter bindings, retry policy, idempotency keys, dead-letter contract, and release evidence | Direct imports of profile-specific stream libraries in generated business logic |

The executable source of truth is:

```python
from pyAppGen.pbc import acp_event_processing_developer_guidance

playbook = acp_event_processing_developer_guidance()["implementation_playbook"]
assert playbook["coding_agent_prompt"].startswith("Use appgen_event_contract.")
assert "hide_stream_engine_picker" in playbook["studio"]
assert "ordinary_manifest_has_no_stream_processor" in playbook["acceptance_criteria"]
```

Use the playbook as the acceptance checklist for pull requests that touch event
processing. A change is not complete if ordinary generated business logic can
import a stream runtime directly, if Studio exposes a runtime picker, or if an
ordinary manifest keeps `stream_processor`.

## Normative Decision

AppGen-X makes the event-processing choice for platform developers.

For ordinary generated applications and PBCs, use exactly this public contract:

```text
appgen_event_contract
```

That means:

- generate transactional outbox/inbox tables;
- generate typed command and event handlers;
- generate retry, idempotency, dead-letter, and release-audit evidence;
- route all event work through the AppGen-X event adapter;
- omit `stream_processor` from ordinary PBC manifests;
- show any selected runtime profile only as read-only generated metadata.

Do not ask developers, Studio users, natural-language generators, or coding
agents to choose between stream engines for ordinary work. The platform keeps
`faust_streaming` behind the adapter as the default service-runtime profile.
`quix_streams` and `bytewax` are exception profiles, not choices in a picker.

The first-match rule is mandatory:

| Workload | Developer-facing answer | Manifest rule |
| --- | --- | --- |
| Business events, ERP, workflow, approval, chatbot, agent, integration, or normal PBC event handling | `appgen_event_contract` | Omit `stream_processor` |
| Telemetry, time-series, high-volume ingestion, or windowed metrics with evidence | Specialized telemetry PBC | `stream_processor: quix_streams` plus `stream_exception_evidence` |
| Complex parallel dataflow, CPU-heavy stream transforms, or multi-stage analytical pipelines with evidence | Specialized dataflow PBC | `stream_processor: bytewax` plus `stream_exception_evidence` |
| Anything unclear | `appgen_event_contract` | Omit `stream_processor` |

The exception workflow must prove why the ordinary generated adapter is not
enough. Without named workload evidence, measurable throughput or latency
reasoning, state/recovery shape, and an operational owner, the generator must
fall back to `appgen_event_contract`.

## Platform Decision Record

The executable decision record is `appgen.event-processing.standard.v1`.

| Field | Value |
| --- | --- |
| Status | Mandatory |
| Developer answer | Use `appgen_event_contract` and omit `stream_processor`. |
| Ordinary event contracts | `1` |
| Ordinary visible stream-engine choices | `0` |
| Ordinary visible runtime profiles | `0` |
| Exception profiles | `2`: `quix_streams`, `bytewax` |
| Profiles per PBC | `1` |

This is the support-matrix cap for the platform. The generator must not turn
every PBC into a Cartesian product of event contracts, stream engines,
datastores, generated targets, deployment profiles, and adapter variants.
Ordinary generated applications get one event path: generated owned tables,
transactional outbox/inbox tables, typed handlers, the AppGen-X event adapter,
and read-only runtime profile metadata.

Tooling must therefore:

- hide stream-engine pickers for ordinary PBC creation;
- lint ordinary manifests that set `stream_processor`;
- block exception profiles without `stream_exception_evidence`;
- fail generated business logic that imports profile-specific stream libraries.

## One Page Recommendation

The platform decision is made: ordinary AppGen-X applications use the generated
AppGen-X event contract. They do not choose Kafka alternatives, stream engines,
topic clients, or state-store libraries.

Use this:

```text
AppGen-X event contract
transactional outbox/inbox
typed event handlers
platform event adapter
read-only runtime profile metadata
```

Do not use this for ordinary generated work:

```text
Kafka alternative comparison
stream-engine picker
per-PBC runtime preference
direct imports of stream-processing libraries
```

The developer-facing choice count is one: `appgen_event_contract`.
Generated applications model commands, events, handlers, retries,
idempotency, dead-letter behavior, and release evidence. The platform owns the
runtime profile behind the adapter.

The default generated stack is therefore:

```text
public API: appgen_event_contract
generated durability: transactional outbox + transactional inbox
generated code: typed handlers behind the AppGen-X event adapter
hidden service profile: faust_streaming
exception profiles: quix_streams or bytewax with evidence only
developer selection UI: none for ordinary applications
```

AppGen-X does not ask application developers, natural-language generators,
coding agents, or Studio users to choose among stream-processing engines for
ordinary generated applications. That choice would create a support matrix that
grows faster than the platform can validate.

The platform choice is one visible developer option:

```text
Use the generated AppGen-X event contract.
Generate transactional outbox/inbox tables and typed handlers.
Route through the AppGen-X event adapter.
Do not choose or import a stream engine for ordinary generated work.
```

## Developer Start Here

For a normal generated app or PBC, the instruction is deliberately short:

```text
Use appgen_event_contract.
Omit stream_processor.
Generate transactional outbox/inbox tables.
Write typed handlers through the AppGen-X event adapter.
Use PostgreSQL unless the project standard is MySQL or MariaDB.
```

That is the whole ordinary path. A developer should not decide between Kafka
alternatives, Python stream libraries, state stores, brokers, topic clients,
or per-target runtime combinations. The platform owns those choices behind the
adapter.

Tooling should consume the same compact contract exposed by
`acp_event_processing_developer_guidance()`:

| Field | Required value |
| --- | --- |
| `answer` | `Use appgen_event_contract.` |
| `visible_options` | `("appgen_event_contract",)` |
| `ordinary_manifest_instruction` | `Omit stream_processor.` |
| `ordinary_datastore_instruction` | `Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.` |
| `exception_options` | `("quix_streams", "bytewax")` |

The same object includes a `decision_brief` for token-constrained generators,
DSL linting, package templates, and IDE controls. Use it as the single
developer-facing card:

```text
headline: Use appgen_event_contract.
ordinary_manifest_rule: Omit stream_processor.
ordinary_codegen_prompt: Generate AppGen-X outbox/inbox events through the platform adapter. Omit stream_processor. Do not compare stream engines.
developer_visible_options: appgen_event_contract
studio_controls_to_hide: stream_engine_picker, per_pbc_runtime_preference
```

This compact guidance object is the source that IDE controls, DSL linting,
natural-language generation, package templates, and external coding-agent
prompts should read when they need the short answer. The long comparison is
background. The product behavior is one default generated contract, one
ordinary visible option, and two evidence-gated exception workflows.

The executable policy also exposes `developer_use_policy` and `choice_budget`.
Those fields are the platform's guardrail against exponential option growth:

| Policy field | Required interpretation |
| --- | --- |
| `developer_use_policy.ordinary_applications.use` | Always `appgen_event_contract`. |
| `developer_use_policy.ordinary_applications.manifest_rule` | Always omit `stream_processor`. |
| `developer_use_policy.ordinary_applications.generated_stack` | Generate owned tables, outbox/inbox tables, typed handlers, retry, idempotency, dead-letter, and release evidence. |
| `choice_budget.ordinary_public_event_contracts` | Exactly `1`. |
| `choice_budget.ordinary_visible_stream_engine_choices` | Exactly `0`. |
| `choice_budget.exception_profiles` | Only `quix_streams` and `bytewax`, and only with exception evidence. |

Generators and IDE screens should not derive their own matrix from the
comparison text. Read the policy object, apply the first matching rule, and
stop. If the request is not clearly telemetry/time-series or complex dataflow,
the answer remains `appgen_event_contract`.

Use this manifest shape for ordinary work:

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

Notice what is missing: there is no `stream_processor`. Validation records the
platform runtime profile as generated metadata after the manifest has been
accepted. Developers author the business contract; AppGen-X supplies the
runtime adapter path.

If a prompt, package template, or IDE screen cannot prove that the workload is
telemetry/time-series or complex parallel dataflow, it must use the ordinary
path above. This keeps the generated surface small enough for constrained
coding agents and prevents the platform from multiplying every PBC by every
possible stream runtime, datastore, packaging target, and deployment profile.

## Normative Platform Choice

The standard answer is mandatory for ordinary generated work:

| Question | Platform answer |
| --- | --- |
| What should a developer use? | `appgen_event_contract`. |
| What should a manifest do? | Omit `stream_processor` unless this is an evidence-backed exception PBC. |
| What should the generator emit? | Owned tables, transactional outbox/inbox tables, typed handlers, retry, idempotency, dead-letter, and release-audit evidence. |
| What should generated business logic import? | The AppGen-X event adapter only. |
| What should the IDE show? | Read-only generated profile metadata, not a stream-engine picker. |
| What should small coding models receive? | A short instruction to generate outbox/inbox events through the AppGen-X adapter. |

This is intentionally not a decision matrix. The platform has one ordinary
implementation recipe:

1. declare commands and events;
2. generate owned tables;
3. generate transactional outbox/inbox tables;
4. generate typed handlers;
5. wire handlers through the AppGen-X event adapter;
6. prove retry, idempotency, dead-letter, and release-audit coverage.

The profile names below are internal platform profiles. They are not ordinary
developer preferences, UI options, or natural-language generation branches.
They exist so the platform can validate and package the generated adapter path
without exposing a combinatorial design surface to users.

## The Developer Answer

When a developer, Studio user, DSL author, or coding agent asks "what should I
use?", answer with this rule:

```text
Use the generated AppGen-X event contract.
Do not compare Kafka alternatives.
Do not choose a stream engine for ordinary generated applications.
Open the exception workflow only for telemetry/time-series or complex
parallel dataflow workloads with evidence.
```

That means ordinary applications, generated PBCs, ERP workflows, integrations,
chatbots, and agentic systems all use the same default:

1. declare commands and events in the DSL or manifest;
2. generate owned tables plus transactional outbox/inbox tables;
3. write handlers against the AppGen-X event adapter API;
4. let the platform keep the service-runtime profile behind the adapter;
5. use release validation to prove idempotency, retry, dead-letter, and owner
   coverage.

Do not start by comparing stream-processing products. Start by modeling the
business event contract. The platform owns the runtime choice.

This document is the developer-facing companion to the executable policy in
`src/pyAppGen/pbc.py`.

## Platform Selection Contract

The platform uses a first-match contract. Developers do not score products,
compare stream libraries, or vote on runtimes.

| Step | Workload description | What to generate | Manifest rule | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Ordinary business, ERP, workflow, chatbot, agent, integration, or PBC event handling | AppGen-X event contract | Omit `stream_processor` | None |
| 2 | Telemetry, time-series ingestion, high-volume ingestion, or windowed operational metrics | Specialized telemetry PBC | `stream_processor: quix_streams` | Required |
| 3 | Complex parallel dataflow, CPU-heavy stream transformation, or multi-stage analytical pipeline | Specialized dataflow PBC | `stream_processor: bytewax` | Required |
| 4 | Anything else or unclear | AppGen-X event contract | Omit `stream_processor` | None |

The ordinary-workload prompt contract is:

```text
Generate commands, events, transactional outbox/inbox tables, typed handlers,
idempotency, retry, dead-letter, and release evidence through the AppGen-X event
adapter. Omit stream_processor.
```

Generated ordinary PBCs should emit these files:

```text
models.py
events.py
services.py
api.py
pbc_runtime.py
```

Those files may mention the read-only selected profile in metadata, but domain
services must not import `faust_streaming`, `quix_streams`, or `bytewax`
directly. If a prompt is ambiguous, use the default contract and keep
`stream_processor` out of the manifest.

## What To Actually Generate

For every ordinary PBC, ERP module, workflow, chatbot, agent, integration, or
generated UI action, generate the same event surface:

```text
models.py
  - owned business tables
  - appgen_outbox_event table
  - appgen_inbox_event table

events.py
  - typed event dataclasses or schemas
  - handler registry
  - idempotency key derivation
  - retry policy names
  - dead-letter envelope shape

services.py
  - command functions
  - one transaction per state mutation
  - enqueue outbox event in the same transaction

pbc_runtime.py
  - read-only selected profile metadata
  - event topic names
  - release-audit evidence
```

Generated domain code imports only the AppGen-X event adapter. It must not
import `faust_streaming`, `quix_streams`, `bytewax`, Kafka clients, or
profile-specific state-store libraries. Adapter-specific code belongs in the
platform runtime, not in generated business logic.

The default datastore answer is equally narrow: use PostgreSQL unless the
project standard is MySQL or MariaDB. Other open-source datastores can appear
only as specialized platform services or explicitly modeled integration
capabilities, not as a reason to branch the ordinary PBC generation path.

## Generator Guardrail

Generated prompts, DSL linters, package templates, and IDE screens must treat
the decision as a choice budget, not a comparison exercise:

```text
ordinary_visible_event_contracts = 1
ordinary_visible_stream_engine_choices = 0
exception_profiles = quix_streams, bytewax
stream_profiles_per_pbc = 1
```

When a natural-language request says "build invoicing," "add onboarding,"
"create inventory," "generate a support chatbot," "wire an approval agent," or
anything similar, stop branching immediately and generate the ordinary event
contract. Do not spend tokens comparing runtimes. Do not emit direct imports of
`faust_streaming`, `quix_streams`, or `bytewax` in generated business logic.

The smallest valid coding-agent instruction is:

```text
Use appgen_event_contract. Omit stream_processor. Generate outbox/inbox tables,
typed handlers, retry, idempotency, dead-letter, and release evidence through
the AppGen-X event adapter. Open an exception only for telemetry/time-series or
complex dataflow with stream_exception_evidence.
```

## Generator And IDE Rules

Natural-language generation, DSL linting, Studio controls, package templates,
and external coding-agent prompts must apply these rules:

1. Do not ask the user to choose a stream engine for ordinary generated work.
2. Do not render a stream-engine picker on the ordinary PBC creation path.
3. Omit `stream_processor` from ordinary manifests.
4. Normalize the missing profile to the platform default during validation.
5. Show the selected profile only as read-only metadata after generation.
6. Open an exception form only when the workload is telemetry/time-series or
   complex parallel dataflow.
7. Require `stream_exception_evidence` before accepting an exception profile.
8. Fail release validation when generated code imports profile-specific stream
   libraries directly.

For token-constrained coding agents, use this exact instruction:

```text
Generate commands, events, transactional outbox/inbox tables, typed handlers,
idempotency, retry, dead-letter, and release evidence through the AppGen-X event
adapter. Omit stream_processor unless the prompt names telemetry/time-series or
complex parallel dataflow and includes exception evidence.
```

## Required Default For Developers

Use the generated AppGen-X event contract for ordinary generated applications
and PBCs. The platform currently backs that contract with the
`faust_streaming` service-runtime profile, but developers should treat that as
read-only platform metadata, not as a design choice.

Ordinary work includes:

- ERP, CRM, HR, finance, inventory, commerce, and operations events;
- PBC command handlers and outbox consumers;
- workflow sagas and approval routing;
- chatbot events and agent task routing;
- API-to-event adapters and integration handlers;
- form actions and generated UI actions that emit business events.

Generated manifests should normally omit `stream_processor`. Validation
normalizes the missing value to the platform default.

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

The explicit default is accepted only for generated metadata and compatibility,
but do not write it by hand in ordinary PBC manifests:

```python
"stream_processor": "faust_streaming"
```

If a generator sees that value in ordinary generated metadata, it should treat
it as read-only platform output. If a developer is authoring a normal PBC
manifest, the field should be omitted.

## What Developers Actually Use

Developers and agents build against the AppGen-X event contract, not a broker,
Kafka alternative, stream library, topic client, or state store. Generate the
same surface for normal PBCs every time:

| File or surface | Generated responsibility |
| --- | --- |
| `models.py` | Owned tables plus generated transactional outbox/inbox mappings. |
| `services.py` | Command handlers that mutate owned state and enqueue events. |
| `events.py` | Typed handlers, idempotency keys, retry policies, and dead-letter contracts. |
| `api.py` | Synchronous command/query routes. |
| `pbc_runtime.py` | Manifest, topic names, read-only selected profile metadata, and release-audit evidence. |
| package docs | Event contracts, handler ownership, operational owner, and exception evidence when present. |

Generated business logic must not import `faust_streaming`, `quix_streams`, or
`bytewax` directly. Profile-specific dependencies belong behind platform
adapter modules.

The visible choice count for ordinary work is one: `appgen_event_contract`.
This is the rule the IDE, DSL linter, natural-language generator, package
templates, and coding-agent prompts should expose.

## Internal Runtime Profiles

AppGen-X carries one default runtime profile and two audited exception profiles
behind the event adapter. Treat this table as platform routing metadata, not as
a product-selection guide for application authors.

| Profile | Decision | Use only when |
| --- | --- | --- |
| `faust_streaming` | Platform default behind the adapter | The PBC is an event-driven service, workflow participant, saga orchestrator, outbox consumer, integration handler, or agent task handler. |
| `quix_streams` | Exception | The PBC owns high-throughput telemetry, time-series streams, large ingestion, or windowed operational metrics. |
| `bytewax` | Exception | The PBC owns complex parallel dataflow, CPU-heavy transformation graphs, stateful analytical pipelines, or multi-stage transformations. |

Do not add another profile for a project. A fourth option requires a platform
architecture decision, executable validation, release-audit coverage, generated
documentation, and tests. Until that exists, the answer remains
`appgen_event_contract` plus the two audited exception workflows.

Do not mix profiles inside one PBC. If a capability has ordinary business
events plus a specialized telemetry or dataflow workload, split the specialized
workload into its own PBC or generated integration capability with a separate
manifest and datastore boundary.

## Decision Tree

Use this decision tree in docs, prompts, IDE controls, DSL linting, and
generator code:

1. Is this ordinary domain-event handling, outbox delivery, workflow
   orchestration, approval routing, integration handling, or agent task
   execution? Use `appgen_event_contract`; the platform records the default
   runtime profile as read-only metadata.
2. Is the workload primarily telemetry, time-series ingestion, high-volume
   event ingestion, or windowed operational metrics? Use `quix_streams`, but
   only with exception evidence.
3. Is the workload primarily complex parallel transformation, CPU-heavy stream
   processing, or a multi-stage stateful dataflow graph? Use `bytewax`, but
   only with exception evidence.
4. If the exception case is not clear and measurable, generate
   `appgen_event_contract`, omit `stream_processor`, and let validation record
   the default runtime profile as read-only metadata.

The default answer is not "choose a Kafka alternative." The default answer is
"generate the AppGen-X outbox/inbox contract and route through the platform
adapter."

## Selection Algorithm

The selection algorithm is intentionally small:

```text
if workload is ordinary business/workflow/integration/agent event handling:
    public_contract = appgen_event_contract
    stream_processor = omitted in manifest
    runtime_profile = faust_streaming metadata after validation
elif workload is telemetry/time-series/high-volume windowing:
    require stream_exception_evidence
    stream_processor = quix_streams
elif workload is complex parallel dataflow or CPU-heavy transformation graph:
    require stream_exception_evidence
    stream_processor = bytewax
else:
    public_contract = appgen_event_contract
    stream_processor = omitted in manifest
```

Do not add secondary scoring, library comparisons, developer preferences,
per-environment overrides, or per-PBC runtime votes. Those reopen the
exponential matrix this standard is meant to close.

## Exception Budget

The platform deliberately has no open-ended stream-runtime extension point for
ordinary generated applications. Every additional visible option multiplies the
test matrix across datastore backend, packaging target, generated adapter,
local development mode, deployment profile, PBC ownership, and release audit.

To keep generated apps reliable and token-efficient:

- ordinary generated work has exactly one public event contract;
- profile names are platform-owned adapter metadata;
- exception profiles are allowed only for the two documented workload classes;
- a PBC may use at most one stream profile;
- a specialized workload that needs an exception should be split into its own
  PBC or generated integration capability;
- adding a fourth profile requires a platform architecture decision, executable
  validation, docs, release gates, and generated tests before it is exposed.

This rule is also the small-model prompt contract:

```text
Generate AppGen-X outbox/inbox events through the platform adapter. Do not
compare stream engines. Omit stream_processor unless exception evidence is
provided for telemetry/time-series or complex parallel dataflow.
```

## Copy-Paste Rules For Generated PBCs

Use these rules in PBC authoring guides, package templates, Studio help text,
and coding-agent prompts:

```text
For normal generated applications:
- omit stream_processor from the PBC manifest;
- model commands, events, handlers, retries, idempotency, and dead-letter flows;
- keep event logic behind the AppGen-X event adapter;
- use PostgreSQL by default, or MySQL/MariaDB when that is the project standard;
- never import stream-engine libraries from generated domain services.

For telemetry or time-series workloads:
- split the workload into its own PBC;
- use quix_streams only with stream_exception_evidence.

For complex parallel dataflow workloads:
- split the workload into its own PBC;
- use bytewax only with stream_exception_evidence.
```

Small local models should receive this compressed instruction:

```text
Generate AppGen-X outbox/inbox events. Omit stream_processor unless this is a
telemetry/time-series PBC or a complex parallel dataflow PBC. Never compare
stream engines in generated app code.
```

This keeps natural-language generation token-efficient and prevents an
exponential combination of stream engines, backends, adapters, and deployment
profiles.

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

Without the evidence, return to the ordinary path: omit `stream_processor`,
generate the AppGen-X event contract, and let validation record the default
runtime profile as read-only platform metadata.

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
- `acp_event_processing_developer_guidance()` returns the compact one-answer
  guidance object that IDE controls, DSL linting, natural-language generation,
  package templates, and external coding-agent prompts should use.
  Its `developer_action_contract` is the shortest authoritative contract for
  platform developers and small coding models.
- `select_acp_stream_processor()` classifies workload descriptions as default
  or exception candidates.
- `validate_pbc_manifest()` rejects unsupported profiles, normalizes missing
  profiles to the default, and blocks exception profiles without
  `stream_exception_evidence`.
- `pbc_release_audit()` includes an `opinionated_stream_processing_policy`
  release gate.

This makes the recommendation part of the platform contract, not only a
documentation preference.
