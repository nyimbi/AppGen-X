# Schema Registry PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `schema_registry`. The emphasis is on governed schema evolution, compatibility precision, consumer impact, payload validation, contract federation, release blocking, and agent-assisted contract stewardship.

## Current Domain Evidence Used

- Domain purpose: subject catalogs, schema versions, compatibility rules, consumer and producer bindings, validation runs, contract violations, contract projections, AppGen-X event evidence, rules, parameters, configuration, UI fragments, and release validation for API, event, projection, document, and package contracts.
- Owned boundary: schema subjects, aliases, namespaces, versions, fields, fingerprints, semantic tags, diffs, evolution plans, compatibility rules/matrices/exceptions, producer/consumer bindings, consumer impact, validation samples/errors, contract violations/remediations/projections, federation views, crypto epochs, governance models, seed data, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command surface: runtime configuration, parameter and rule registration, owned schema extensions, AppGen-X inbox intake, subject registration, compatibility rules, consumer binding, schema submission, compatibility checks, payload validation, violation recording, projection publishing, proof generation, policy screening, federation, identity checks, resilience drills, crypto epoch rotation, carbon-aware validation, schema diff optimization, consumer impact allocation, control testing, governed model registration, and boundary verification.
- Existing events and dependencies: emits `SchemaSubjectRegistered`, `SchemaAccepted`, `BreakingSchemaBlocked`, `PayloadValidated`, `ContractViolationRecorded`, and `ContractProjectionPublished`; consumes deployment, event-contract proposal, route-publication, access-policy, and package-registration events through AppGen-X.

## 50 Better-Than-World-Class Improvements

### 1. Canonical contract identity model

**Justification:** Subject names alone do not establish durable identity across aliases, namespaces, package versions, route projections, event subjects, and tenant boundaries.

**Improvement:** Add canonical contract identity records with immutable subject UID, namespace lineage, alias history, owner PBC, contract kind, channel, tenant scope, deprecation state, and collision evidence. All schema versions, consumer bindings, violations, and projections should reference this canonical identity rather than mutable display names.

### 2. Namespace governance with reserved vocabularies

**Justification:** Contract estates degrade when teams create inconsistent namespaces, ambiguous ownership, or field names that conflict across event, API, projection, and document contracts.

**Improvement:** Implement namespace policies for reserved prefixes, ownership delegation, subject naming, semantic tag vocabularies, lifecycle states, and permitted contract formats. The UI should show namespace health and the agent should reject or propose alternatives for non-compliant subject requests.

### 3. Compatibility rule precedence engine

**Justification:** Compatibility decisions often combine global, tenant, subject, channel, consumer, package, and emergency rules; unclear precedence leads to contradictory approval outcomes.

**Improvement:** Build a deterministic precedence engine that explains which rule won, which rules were shadowed, and why. Persist compatibility decision traces and add tests for priority, inheritance, override expiry, and tenant isolation.

### 4. Full semantic compatibility analysis

**Justification:** Backward/forward checks catch structural breaks but miss semantic breaks such as unit changes, enum meaning shifts, nullable meaning changes, money precision changes, or timestamp interpretation changes.

**Improvement:** Extend compatibility checks with semantic tags for units, currency, precision, timezone, identifier class, PII class, lifecycle meaning, and cardinality intent. Block or require review when a structurally compatible change alters semantic interpretation.

### 5. Consumer blast-radius graph

**Justification:** A breaking change matters because of the consumers it affects, their versions, release windows, business criticality, and alternative paths.

**Improvement:** Build a consumer impact graph linking producer bindings, consumer bindings, routes, workflows, projections, packages, and validation evidence. Show affected consumers, minimum accepted versions, remediation owners, deadlines, and release-blocking severity in the workbench.

### 6. Producer readiness scoring

**Justification:** Producers can publish schemas without enough evidence that generated code, payload samples, documentation, and rollout plans are ready.

**Improvement:** Add producer readiness checks for schema examples, fixture coverage, owner approval, payload validation, compatibility results, version notes, migration plan, and projection publication. Low-readiness versions remain draft even if structural compatibility passes.

### 7. Consumer consent workflow

**Justification:** Some non-breaking changes still require consumer review, especially for high-risk domains, constrained clients, or externally published contracts.

**Improvement:** Implement consumer consent records with required reviewers, review SLA, accepted version range, objections, waiver reasons, and approval expiry. Release gates should block when mandatory consumers have not consented or their waiver has expired.

### 8. Schema evolution plan compiler

**Justification:** Complex migrations need staged compatibility, dual-write, dual-read, projection rebuilds, and deprecation windows rather than a single schema submission.

**Improvement:** Add an evolution plan compiler that turns proposed changes into staged actions: add optional field, emit both fields, migrate consumers, mark old field deprecated, remove after threshold, publish projections, and close violations. The agent should draft plans from natural-language change requests.

### 9. Field-level lifecycle state

**Justification:** Contracts need field states such as experimental, active, deprecated, forbidden, internal-only, shadow, and removal-pending.

**Improvement:** Add field lifecycle metadata and enforce allowed transitions through compatibility checks. The UI should expose field timelines, consumers still reading deprecated fields, and removal readiness evidence.

### 10. Contract diff taxonomy

**Justification:** A generic diff does not separate harmless metadata changes from catastrophic payload incompatibility.

**Improvement:** Classify diffs by field addition/removal, type widening/narrowing, enum expansion/contraction, requiredness change, semantic tag change, format change, default change, constraint change, documentation-only change, and policy classification change. Each class should map to a rule, severity, and remediation path.

### 11. Fixture-based compatibility tests

**Justification:** Static schema comparison misses real payload edge cases and historically troublesome examples.

**Improvement:** Store curated payload fixtures per subject/version, including boundary values, null behavior, enum examples, malformed payloads, and legacy samples. Compatibility checks should replay fixtures against proposed schemas and persist validation outcomes.

### 12. Payload sampling with privacy protection

**Justification:** Real payload validation is valuable, but sampled payloads can leak sensitive data into registry tables or agent context.

**Improvement:** Add redaction-aware payload sample capture with route/field policies, PII classification, irreversible masking, retention periods, sample purpose, and access controls. Release tests should prove raw sensitive values cannot be persisted in validation evidence.

### 13. Format-specific validators

**Justification:** API, event, projection, document, and package contracts have different compatibility and validation semantics across JSON Schema, OpenAPI-like descriptors, Avro-like records, SQL projections, and package metadata.

**Improvement:** Provide pluggable but package-owned validators for each supported format, with shared decision envelopes and format-specific checks. Runtime configuration should allow formats but never expose event-stream engine selection.

### 14. Contract quality score

**Justification:** A schema can be compatible yet low quality: vague names, missing descriptions, weak constraints, untyped maps, unstable enums, or undocumented nullable fields.

**Improvement:** Add quality scoring for documentation, naming, constraints, semantic tags, examples, deprecation clarity, error models, and consumer coverage. Workbench filters should prioritize low-quality contracts even when they are not release blockers.

### 15. Error contract governance

**Justification:** Error envelopes are often under-governed, yet client behavior depends heavily on error codes, retry hints, and remediation fields.

**Improvement:** Treat error contracts as first-class subjects with code registries, severity semantics, retryability, localization keys, support reference fields, and backward-compatibility checks. Link gateway error-normalization policies to accepted error contracts.

### 16. Event contract causality metadata

**Justification:** Event payload shape is insufficient without causality, idempotency, ordering, correlation, producer intent, and replay semantics.

**Improvement:** Extend event subjects with causality fields, event id, idempotency key, correlation id, aggregate reference, replay policy, ordering expectation, and tombstone semantics. Block event contract acceptance when handlers cannot safely consume the declared behavior.

### 17. Projection contract staleness policy

**Justification:** Projection consumers need to know freshness guarantees, rebuild behavior, and stale-read tolerances, not only field shapes.

**Improvement:** Add projection contract metadata for freshness SLA, rebuild trigger, lag tolerance, source events, snapshot cadence, and degradation behavior. Compatibility checks should flag changes that alter freshness or rebuild requirements.

### 18. Command and query contract completeness

**Justification:** Generated applications need command/query contracts that capture permissions, idempotency, validation, events, and response semantics.

**Improvement:** Add contract templates for commands and queries with permission descriptors, idempotency requirements, validation rules, emitted events, returned projections, pagination, filtering, and error envelopes. Release evidence should require complete command/query contracts for generated routes.

### 19. Breaking-change waiver governance

**Justification:** Real organizations sometimes approve breaking changes, but waivers must be explicit, time-bound, reviewed, and auditable.

**Improvement:** Add compatibility exception lifecycle with scope, impacted consumers, compensating controls, owner, expiry, approval chain, and rollback plan. The workbench should alert on expired or overbroad waivers and release audit should count active exceptions.

### 20. Schema acceptance proof bundle

**Justification:** Accepted schemas should carry enough evidence for downstream PBCs to trust them without duplicating validation logic.

**Improvement:** Produce an acceptance proof bundle containing fingerprint, rules evaluated, compatibility matrix, consumer impact, validation samples, policy screening, approvals, and projection publication status. Publish this bundle through AppGen-X events and descriptor APIs.

### 21. Immutable fingerprint strategy

**Justification:** Fingerprints must distinguish meaningful content, canonical formatting, metadata-only changes, and tenant-specific policy overlays.

**Improvement:** Implement multiple fingerprints: canonical shape, semantic shape, documentation metadata, policy classification, and package descriptor. Store hash algorithm, crypto epoch, canonicalization rules, and collision checks for each fingerprint.

### 22. Schema signing and crypto epoch rotation

**Justification:** Consumers need assurance that a contract version has not been tampered with and was accepted under a known signing policy.

**Improvement:** Add schema-signature records bound to crypto epochs, signing purpose, accepted fingerprint, key identifier, and verification state. Rotation workflows should simulate which consumers still rely on old signatures before epoch activation.

### 23. Contract federation reconciliation

**Justification:** Composed applications may include multiple package registries, gateways, workflows, and external contract sources that describe related contracts differently.

**Improvement:** Add federation reconciliation that compares local subjects to external contract projections, detects drift, maps aliases, flags ownership conflicts, and proposes merge or quarantine actions. Keep all remote state as projections, never direct shared tables.

### 24. Package registration schema gate

**Justification:** External PBC packages should not register unless their manifests, events, APIs, models, UI fragments, and agent competencies have accepted contracts.

**Improvement:** Add a package registration gate that validates package metadata against required subject types and publishes pass/fail evidence. Failed packages should receive precise remediation items tied to missing or incompatible contract subjects.

### 25. Access-policy-aware contract screening

**Justification:** Some schema fields imply permissions, purposes, or data classifications that must align with identity policy.

**Improvement:** Consume access-policy projections to screen fields, endpoints, and event subjects for required permissions and purpose constraints. Compatibility checks should flag changes that expose new sensitive fields without matching access policy.

### 26. Audit-ready contract timelines

**Justification:** Auditors need to reconstruct who proposed, reviewed, accepted, blocked, waived, published, and consumed a contract version over time.

**Improvement:** Build temporal contract timelines from subject events, versions, approvals, violations, projections, and dead letters. Support as-of views that show accepted state and active rules at any historical timestamp.

### 27. Contract violation triage lifecycle

**Justification:** Violations must move through investigation, assignment, remediation, retest, waiver, or escalation with clear accountability.

**Improvement:** Expand violations with state transitions, owner assignment, root cause, affected consumers, remediation tasks, retest evidence, SLA timers, escalation path, and release-blocking status. The agent should summarize open violations and draft remediation plans.

### 28. Autonomous remediation drafts

**Justification:** Schema owners benefit from suggested fixes, but automatic mutation must remain safe and explainable.

**Improvement:** Implement agent-generated remediation drafts for required-field removal, type narrowing, enum contraction, missing semantic tags, invalid examples, and consumer version gaps. Each draft should include proposed schema changes, expected compatibility result, consumer impact, and rollback notes.

### 29. Natural-language schema intake

**Justification:** Teams describe contract needs in documents, tickets, emails, and specifications rather than perfect schema files.

**Improvement:** Add document ingestion that extracts subjects, fields, examples, constraints, semantic tags, producers, consumers, and lifecycle dates. The agent should create draft schema versions with confidence markers and citations to source sections.

### 30. Version negotiation service

**Justification:** Consumers and producers need to agree on compatible versions during rollout, especially when multiple versions are valid.

**Improvement:** Provide a version negotiation query that returns acceptable producer/consumer pairs, lowest safe version, latest preferred version, known exceptions, and migration deadline. Use this in route publication, package composition, and workflow validation.

### 31. Contract dependency cycle detection

**Justification:** Schemas can reference each other in ways that create impossible deployment ordering or recursive projection rebuilds.

**Improvement:** Analyze subject references, package contracts, workflow contracts, and projection dependencies to detect cycles, unresolved references, and unsafe deployment sequences. Surface ordered rollout plans or explicit blockers.

### 32. Enum lifecycle governance

**Justification:** Enum additions, removals, aliases, and semantic meaning changes are frequent sources of consumer breaks.

**Improvement:** Add enum value lifecycle state, alias, canonical meaning, deprecation date, consumer support evidence, and unknown-value handling policy. Compatibility decisions should distinguish additive enum changes from consumer-unsafe enum changes.

### 33. Numeric precision and unit controls

**Justification:** Financial, quantity, measurement, and scheduling contracts can break silently when precision, scale, units, or rounding rules change.

**Improvement:** Add unit and precision metadata with validation rules, allowed conversions, rounding policy, and semantic compatibility checks. Flag changes from integer to decimal, minor units to major units, or timezone-naive to timezone-aware timestamps.

### 34. Data classification propagation

**Justification:** Sensitive-field tags need to flow into gateway, audit, workflow, and generated UI contracts.

**Improvement:** Track field classification, purpose, retention class, masking policy, and exportability. Publish classification projections and fail release when downstream contracts omit required privacy or access controls.

### 35. Generated SDK contract evidence

**Justification:** Consumers often discover contract breaks in generated client/server code, not raw schema files.

**Improvement:** Add optional generated SDK evidence descriptors showing language target, generated types, compile status, backwards-compatibility tests, and unsupported features. Keep artifacts as metadata so the PBC remains language-neutral where needed.

### 36. Contract documentation consistency check

**Justification:** Documentation often drifts from schemas and misleads consumers even when validation passes.

**Improvement:** Compare field descriptions, examples, version notes, error descriptions, and migration guides against actual schema fields and constraints. Add documentation mismatch warnings and block external publication for severe mismatches.

### 37. Release-gate integration matrix

**Justification:** Contract validation must serve composition, gateway, workflow, audit, and package release gates with precise pass/fail semantics.

**Improvement:** Add a release integration matrix that maps each subject type to required consumers, projections, release gates, blocking severities, and emitted events. Generated apps should use the matrix to know which contracts must exist before deployment.

### 38. Validation anomaly detection

**Justification:** A sudden rise in validation errors can indicate bad deployments, producer bugs, hidden consumer behavior, or contract misunderstanding.

**Improvement:** Add anomaly detection over validation error rate, fields failing, producers, tenants, and schema versions. Findings should include deterministic thresholds, probable causes, related route/workflow changes, and recommended containment actions.

### 39. Contract exposure forecasting

**Justification:** Schema risk depends on future rollout, consumer adoption, open violations, and deprecation timelines, not only current state.

**Improvement:** Forecast exposure for planned schema changes using consumer adoption curves, release schedules, violation age, and waiver expiry. The workbench should show future dates when a safe change becomes unsafe or a breaking change becomes removable.

### 40. Review-capacity allocation

**Justification:** Schema review teams can be bottlenecked by many proposed changes with uneven business risk.

**Improvement:** Allocate reviews by impact, release deadline, consumer criticality, violation severity, and reviewer expertise. The PBC should recommend review order and publish explainable reviewer workload evidence.

### 41. Carbon-aware validation scheduling guardrails

**Justification:** Heavy compatibility sweeps can be deferred, but release-critical validation cannot be delayed blindly.

**Improvement:** Add scheduling policy that distinguishes release-blocking checks from bulk revalidation, assigns carbon-aware windows only to deferrable work, and records why validation ran immediately or was deferred.

### 42. Schema resilience drill

**Justification:** The registry itself must keep validating contracts during dependency outages, projection lag, and outbox replay.

**Improvement:** Implement resilience drills that simulate stale access-policy projections, gateway projection outages, duplicate events, malformed event proposals, and dead-letter replay. Store drill results as release evidence.

### 43. Agent competency for contract review

**Justification:** The composed application agent must know what the schema-registry agent can safely do and which actions need human approval.

**Improvement:** Define DSL-expressible competencies for schema intake, compatibility explanation, impact analysis, violation triage, remediation drafting, and release evidence explanation. Each competency should declare permissions, safe read operations, unsafe mutations, document inputs, and confirmation requirements.

### 44. Agent-safe schema mutation previews

**Justification:** Natural-language schema changes can break downstream systems if applied without a precise diff and impact preview.

**Improvement:** Require the agent to produce mutation previews with old/new schema snippets, diff taxonomy, compatibility result, affected consumers, emitted events, rollback option, and approval state before submitting any schema version.

### 45. Workbench coverage for all schema capabilities

**Justification:** A complete registry cannot hide core operations in backend commands; experts need rich UI surfaces for contract stewardship.

**Improvement:** Expand UI into subject catalog, schema editor, diff viewer, compatibility decision trace, consumer impact graph, validation sample console, violation board, federation reconciler, release-gate matrix, projection publisher, and agent review panel.

### 46. Queryable compatibility matrix history

**Justification:** Teams need to know which producer/consumer version pairs were compatible at different times and under which rules.

**Improvement:** Persist compatibility matrix snapshots by subject, producer version, consumer version, rule version, tenant, and decision timestamp. Support queries for current compatibility, historical compatibility, and planned compatibility after a proposed evolution plan.

### 47. Contract ownership hygiene

**Justification:** Orphaned subjects, aliases, and violations create operational risk and slow releases.

**Improvement:** Add ownership hygiene reports for subjects without active owners, consumers without contacts, stale aliases, inactive producers, expired waivers, and abandoned violations. The agent should draft reassignment tasks and block high-risk orphaned contract publication.

### 48. Boundary proof for schema-only ownership

**Justification:** The registry must not become a hidden shared database for gateway, identity, workflow, audit, or business-domain state.

**Improvement:** Add release checks proving operations use only owned tables plus declared API/event/projection dependencies. Include tests for direct foreign-table reference attempts and evidence that projections remain snapshots, not shared-table shortcuts.

### 49. Contract seed-data governance

**Justification:** Seed contracts can silently define critical platform defaults and should be versioned, testable, and override-aware.

**Improvement:** Add seed-data descriptors for default compatibility rules, namespace policies, semantic tags, classifications, error envelopes, and sample subjects. Validate seeds through the same compatibility, ownership, and release gates as user-created contracts.

### 50. Schema-registry release readiness score

**Justification:** Release evidence needs a concise but defensible view of whether the registry is complete for a composed application.

**Improvement:** Compute a readiness score from subject coverage, accepted versions, consumer bindings, unresolved violations, projection freshness, rule tests, payload validation, waiver risk, documentation quality, agent competency coverage, UI coverage, and boundary proof. Expose the score in package release evidence and generated app workbenches.
