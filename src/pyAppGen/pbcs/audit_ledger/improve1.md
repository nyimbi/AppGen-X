# Audit Ledger PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `audit_ledger`. The focus is immutable evidence, signature-chain integrity, retention governance, forensic exports, continuous control assurance, disclosure minimization, and agent-assisted audit operations.

## Current Domain Evidence Used

- Domain purpose: immutable evidence and assurance for domain mutations, access decisions, routing changes, workflow outcomes, package registration actions, configuration changes, release controls, forensic exports, and disclosure proofs.
- Owned boundary: audit events, signature chains, retention policies, forensic exports, access evidence, control assertions, rules, parameters, configuration, projection links, schema extensions, disclosure proofs, anomaly signals, identity credentials, resilience drills, crypto key epochs, carbon processing windows, governed models, inbox/outbox, and dead-letter evidence.
- Existing command surface: configure runtime, record/seal audit events, verify signature chains, capture access evidence, define retention policy, prepare forensic exports, assert controls, process inbox events, publish projections, generate disclosure proofs, run resilience and crypto operations, register governed models, build workbench views, and verify owned-table boundaries.
- Existing events and dependencies: emits `AuditEventSealed`, `SignatureChainVerified`, `RetentionPolicyChanged`, `ForensicExportPrepared`, `ControlAssertionFailed`, and `AuditProjectionPublished`; consumes identity, workflow, gateway, schema, deployment, and composition events through AppGen-X.

## 50 Better-Than-World-Class Improvements

### 1. Evidence envelope completeness gate

**Justification:** An audit event without actor, action, source, aggregate, classification, timestamp basis, payload digest, and causality is weak evidence.

**Improvement:** Add an evidence envelope validator that rejects or quarantines incomplete events, records missing fields, and explains whether the event is admissible for controls, forensic export, or release evidence.

### 2. Per-tenant sequence integrity proof

**Justification:** Hash chains are only meaningful if sequence gaps, duplicates, reorders, and cross-tenant contamination are detectable.

**Improvement:** Build sequence integrity proofs that verify contiguous tenant sequences, previous-hash linkage, event-hash agreement, timestamp monotonicity policy, and genesis anchor. Expose proof status and gaps in the chain verification UI.

### 3. Multi-algorithm signature agility

**Justification:** Signature policy must support crypto migration without invalidating historic evidence.

**Improvement:** Track signature algorithm, key epoch, canonicalization rules, verification algorithm, and migration status per event and chain link. Provide dual-signing and verification windows during crypto epoch rotation.

### 4. Canonical payload digest strategy

**Justification:** Digest mismatches often arise from serialization differences rather than tampering.

**Improvement:** Define canonicalization profiles for JSON-like payloads, descriptor payloads, and redacted views. Store canonicalization version with each digest and add tests proving equivalent payloads hash consistently.

### 5. Tamper triage workflow

**Justification:** A failed hash check needs containment, owner assignment, evidence preservation, and recovery path, not just a boolean failure.

**Improvement:** Add tamper cases with severity, affected sequence range, suspected cause, related deployments, chain gap, owner, containment action, and closure evidence. The agent should summarize risk and propose non-destructive investigation steps.

### 6. Append-only mutation guard

**Justification:** The ledger must prove records are never updated or deleted as a side effect of ordinary commands.

**Improvement:** Add release tests and runtime checks for append-only audit event behavior, immutable sealed fields, and explicit corrective-event patterns. Corrected audit data should be represented by new linked events, not mutation of sealed rows.

### 7. Access decision replay

**Justification:** Auditors need to reconstruct why access was allowed or denied with the policy context available at the time.

**Improvement:** Add replay records linking access evidence to policy projection version, actor claims digest, resource reference, decision reason, and as-of timestamp. Provide a replay panel that distinguishes historical policy from current policy.

### 8. Disclosure minimization planner

**Justification:** Forensic exports must reveal only what is necessary while still proving integrity.

**Improvement:** Add a planner that selects minimal event fields, redaction rules, proof hashes, and disclosure justifications for an export request. Show withheld fields, legal basis, and verifier instructions.

### 9. Forensic export approval workflow

**Justification:** Audit exports are high-risk disclosures that require approvals, purpose, recipient, retention, and revocation evidence.

**Improvement:** Model export lifecycle from draft to approved, prepared, delivered, expired, revoked, and closed. Store approvers, disclosure purpose, recipient class, expiry, watermark/checksum, and access constraints.

### 10. Export chain-of-custody tracking

**Justification:** Evidence value depends on tracking who prepared, accessed, delivered, verified, and disposed of an export.

**Improvement:** Add chain-of-custody records for export package creation, checksum verification, recipient handoff, download, reissue, and disposal proof. Surface custody timeline in the forensic export UI.

### 11. Retention policy conflict resolver

**Justification:** Retention can be governed by classification, tenant, jurisdiction, legal hold, export status, and source PBC requirements.

**Improvement:** Build a resolver that computes effective retention from overlapping policies, explains precedence, blocks unsafe disposal, and flags records whose policy is ambiguous or expired.

### 12. Legal hold lifecycle

**Justification:** Legal holds need scope, authority, reason, notification, periodic review, and release evidence.

**Improvement:** Add legal hold records linked to retention policies and event ranges with custodian, matter reference, active period, review cadence, release approval, and blocked disposal proof.

### 13. Disposal proof generation

**Justification:** When evidence is lawfully disposed, the system needs proof without exposing disposed payloads.

**Improvement:** Generate disposal proofs with event range, policy basis, legal-hold check, actor, timestamp, digest summary, and irreversible disposal evidence. Retain only the disposal proof where policy allows.

### 14. Continuous control library

**Justification:** Control assertions should be reusable, versioned assurance tests, not ad hoc records.

**Improvement:** Add control definitions for chain integrity, configuration drift, dead-letter age, access evidence completeness, export approval, retention compliance, projection freshness, and release gates. Assertions should reference control versions and evidence sources.

### 15. Control failure remediation lifecycle

**Justification:** Failed controls need assignment, triage, remediation, retest, waiver, and release-blocking governance.

**Improvement:** Expand control assertions with owner, root cause, remediation task, retest evidence, waiver expiry, release-blocking status, and escalation. The agent should draft remediation steps but not close failures without evidence.

### 16. Audit projection contract governance

**Justification:** Downstream PBCs consume audit projections and need stable contracts around fields, freshness, minimization, and policy basis.

**Improvement:** Add projection contracts with consumer, purpose, allowed fields, freshness SLA, minimization rule, and revocation behavior. Publication should emit evidence and block consumers that request overbroad audit data.

### 17. Projection freshness monitoring

**Justification:** Governance consumers may act on stale audit projections.

**Improvement:** Track last projection publish, event sequence included, lag, failure reason, and consumer acknowledgement. Surface stale projections and emit `AuditProjectionPublished` only with precise range metadata.

### 18. Audit event causality graph

**Justification:** Isolated audit rows do not explain how a route change, access decision, workflow approval, and domain mutation are related.

**Improvement:** Build a causality graph using correlation IDs, aggregate IDs, source PBC, AppGen-X event references, and workflow/composition projections. UI drilldowns should show related evidence without reading foreign tables.

### 19. Actor identity attestation

**Justification:** Audit trails are weak if actor identifiers cannot be tied to a trusted identity at the time of action.

**Improvement:** Store actor credential evidence, issuer, assurance level, validity period, and verification result for high-risk actions. Link access evidence and audit events to the relevant attestation.

### 20. Service and agent actor distinction

**Justification:** Human, service, scheduled job, and AI agent actions carry different accountability and approval requirements.

**Improvement:** Add actor class, delegation chain, agent skill, human approver, and automation purpose to audit envelopes. Release evidence should prove agent-originated mutations are separately searchable.

### 21. Agent action audit preview

**Justification:** Audit agents can help search and prepare evidence, but exporting or mutating audit policy must be tightly controlled.

**Improvement:** Require agent previews for export preparation, retention changes, projection publication, control waivers, and tamper-case closure. Each preview should include records touched, disclosure fields, permissions, emitted events, and rollback limits.

### 22. Natural-language audit query parser

**Justification:** Auditors often ask for evidence in plain language by actor, action, date, tenant, source PBC, or incident.

**Improvement:** Build a query parser that maps natural-language requests to safe filters, classification constraints, result limits, and export eligibility. The agent should cite the parsed filters and ask for approval before preparing disclosures.

### 23. Evidence search relevance model

**Justification:** Large audit ledgers need ranking by relevance, not only exact filters.

**Improvement:** Add relevance scoring over actor, source PBC, action, aggregate, time proximity, incident tags, control failures, and causality graph distance. Persist model governance and deterministic fallback order.

### 24. Audit anomaly taxonomy

**Justification:** A generic anomaly signal is not enough for meaningful investigation.

**Improvement:** Classify anomalies as sequence gap, signature mismatch, unusual actor/action, privileged action burst, export spike, retention conflict, projection lag, dead-letter surge, or control failure pattern. Each class should map to a triage workflow.

### 25. Entropy-based evidence health scoring

**Justification:** Information-theoretic signals can reveal missing or suspiciously uniform audit patterns.

**Improvement:** Compute evidence health scores using event diversity, actor/action distribution, source PBC coverage, missing classification ratio, and sequence behavior. Show why a score changed and which records contributed.

### 26. Release evidence notarization bundle

**Justification:** Release audits need portable proof that controls, chain checks, and boundary checks passed at release time.

**Improvement:** Generate notarization bundles with release id, chain range, control assertions, configuration digest, dead-letter status, boundary proof, and signature. Publish summary events and retain bundle proof.

### 27. Boundary proof against shared tables

**Justification:** Audit Ledger must not inspect operational tables directly even when gathering evidence from other PBCs.

**Improvement:** Add static and runtime tests proving audit commands use only owned tables plus declared APIs/events/projections. Include fixtures that attempt direct reads of identity, workflow, gateway, schema, and business tables and fail release audit.

### 28. Evidence classification enforcement

**Justification:** Classification drives retention, export eligibility, access policy, and redaction.

**Improvement:** Make classification mandatory with allowed values from configuration, rule-based escalation for sensitive classes, and release checks for unclassified events. UI should show classification gaps by source PBC.

### 29. Redacted audit views

**Justification:** Users need to inspect audit records without seeing sensitive payload details they are not authorized to view.

**Improvement:** Add redacted view generation per role, classification, export mode, and disclosure purpose. Preserve digest verification for redacted views so recipients can trust minimized evidence.

### 30. Multi-tenant audit isolation harness

**Justification:** Audit ledgers are especially sensitive to tenant leakage through sequence numbers, search results, exports, projections, and agent summaries.

**Improvement:** Add tenant isolation tests for event recording, chain verification, queries, exports, projections, dead letters, and agent responses. Fail release evidence on cross-tenant result leakage.

### 31. Inbox failure forensics

**Justification:** Failed consumed events can create audit gaps that undermine assurance.

**Improvement:** Build inbox failure analysis showing event type, source, attempt count, handler error, expected audit effect, dead-letter risk, and safe replay plan. The workbench should prioritize failures that create evidence gaps.

### 32. Dead-letter closure proof

**Justification:** Dead letters should not disappear after manual handling.

**Improvement:** Add closure records with root cause, replay decision, compensating audit event, ignored reason, approver, and proof that the missing evidence risk is resolved or accepted.

### 33. Configuration drift audit

**Justification:** Changes in signature algorithm, classifications, export modes, retry limit, or retention defaults affect assurance quality.

**Improvement:** Record configuration snapshots and compare active configuration to approved baselines. Control assertions should fail on unapproved drift and link to the exact config delta.

### 34. Rule change impact simulation

**Justification:** Audit rules can alter retention, exportability, control failures, and release blocking across millions of events.

**Improvement:** Simulate rule changes against representative event ranges, showing affected classifications, controls, exports, retention decisions, and projections. Require approval for high-impact rule activation.

### 35. Forensic export sampling validation

**Justification:** Export filters can accidentally omit required evidence or include excessive records.

**Improvement:** Add preview sampling that shows included/excluded event classes, sequence ranges, classifications, source PBCs, and proof coverage. The agent should explain export completeness and minimization risks.

### 36. Immutable audit correction pattern

**Justification:** Incorrect audit entries must be corrected without rewriting history.

**Improvement:** Add correction event types that link to original events, state correction reason, corrected fields, authority, and verification status. Search and export should show original and correction together.

### 37. Regulator and external reviewer workspaces

**Justification:** External reviewers need scoped, time-bound, minimized access to evidence bundles.

**Improvement:** Add reviewer workspace descriptors with purpose, allowed exports, accessible proof bundles, expiry, watermark, access log, and revocation. Keep the workspace evidence in audit-owned tables.

### 38. Evidence quality scoring by source PBC

**Justification:** Some source PBCs may underproduce classification, actor, causality, or payload digest evidence.

**Improvement:** Score source PBC evidence quality across completeness, timeliness, classification, correlation, and retry health. Publish feedback projections and release blockers for chronically poor evidence quality.

### 39. Control coverage map

**Justification:** Assurance teams need to know which controls cover which event classes, PBCs, configurations, and releases.

**Improvement:** Build a coverage map from control definitions to audit evidence classes, source PBCs, release gates, and projection consumers. UI should reveal uncovered evidence classes and redundant controls.

### 40. Audit-ledger resilience drills

**Justification:** The ledger must keep preserving evidence during projection outages, duplicate events, handler failures, and crypto rotation.

**Improvement:** Add executable drills for duplicate AppGen-X events, stale dependency projections, dead-letter replay, chain verification under partial failure, and export generation under load. Store drill results in release evidence.

### 41. Carbon-aware background audit processing

**Justification:** Heavy exports, anomaly sweeps, and proof generation can be scheduled when not release-critical.

**Improvement:** Add policy that separates urgent assurance work from deferrable analytics/export work and schedules only deferrable tasks into carbon processing windows. Record why each job ran immediately or was deferred.

### 42. Audit event retention forecast

**Justification:** Storage, legal hold, and disposal planning require forecasting evidence growth and retention exposure.

**Improvement:** Forecast event volume, retained bytes, legal-hold expansion, disposal eligibility, and export workload by source PBC and classification. Surface future capacity and compliance risks.

### 43. Cryptographic proof verifier UI

**Justification:** Users should not need to understand hashes to validate an evidence bundle.

**Improvement:** Add a verifier view that accepts a proof bundle, validates hashes/signatures/chain ranges, shows included disclosures, and explains pass/fail reasons in reviewer language.

### 44. Audit package metadata completeness

**Justification:** Generated applications and external packages need to understand audit capabilities, permissions, event types, and proof formats.

**Improvement:** Enrich package metadata with audit competencies, proof formats, supported classifications, export modes, control library, retention policy types, UI fragments, and agent skills. Validate metadata in release audit.

### 45. UI surface for every audit capability

**Justification:** An audit PBC is incomplete if advanced functions are backend-only.

**Improvement:** Expand the workbench into event search, chain verifier, tamper cases, retention policy studio, legal holds, forensic exports, reviewer workspaces, control assertions, anomaly signals, projections, dead letters, crypto epochs, and agent query panels.

### 46. Control assertion DSL descriptors

**Justification:** Composed applications should express audit controls and release gates declaratively.

**Improvement:** Add DSL descriptors for control definitions, release evidence bundles, projection contracts, retention rules, proof bundles, and audit-agent competencies. Generated DSL should round-trip into runtime release checks.

### 47. Audit evidence lineage for generated apps

**Justification:** Generated applications need to know which runtime actions emit which audit events and controls.

**Improvement:** Generate an evidence lineage map from route/command descriptors to expected audit events, access evidence, control assertions, and release proofs. Fail smoke audits when a generated command lacks audit lineage.

### 48. Agent competency catalog for audit work

**Justification:** The composed single agent must know which audit tasks it can perform safely and which require approval.

**Improvement:** Publish competencies for audit search, evidence explanation, export drafting, control triage, tamper-case summarization, retention simulation, proof verification, and dead-letter recovery. Declare permissions, safe reads, mutation previews, and disclosure limits for each competency.

### 49. World-class audit documentation set

**Justification:** Audit systems require operator, auditor, developer, and regulator-facing documentation, not only runtime evidence.

**Improvement:** Generate documentation for event envelopes, chain verification, retention, export workflow, proof verification, control library, privacy/redaction, boundary rules, and agent-safe operations. Validate docs exist in release evidence.

### 50. Audit readiness score

**Justification:** Users need a concise measure of whether audit evidence is complete enough for release, assurance, and investigation.

**Improvement:** Compute an audit readiness score from chain health, event completeness, projection freshness, control coverage, dead-letter risk, retention conflicts, export governance, tenant isolation, boundary proof, UI coverage, and agent competency coverage. Show blockers and next best remediation actions.
