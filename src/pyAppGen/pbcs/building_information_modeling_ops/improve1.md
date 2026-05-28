# Building Information Modeling Operations Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `building_information_modeling_ops`.
- Manifest description: BIM models, versions, clashes, assets, handover data, model governance, and digital twin operations.
- Owned tables named in the manifest: `bim_model`, `model_version`, `clash_issue`, `asset_object`, `handover_package`, `model_review`, `digital_twin_link`, `building_information_modeling_ops_policy_rule`, `building_information_modeling_ops_runtime_parameter`, `building_information_modeling_ops_schema_extension`, `building_information_modeling_ops_control_assertion`, `building_information_modeling_ops_governed_model`.
- Public APIs named in the manifest: `POST /bim-models`, `POST /model-versions`, `POST /clash-issues`, `POST /asset-objects`, `POST /handover-packages`, `GET /building-information-modeling-ops-workbench`.
- Emitted events named in the manifest: `BuildingInformationModelingOpsCreated`, `BuildingInformationModelingOpsUpdated`, `BuildingInformationModelingOpsApproved`, `BuildingInformationModelingOpsExceptionOpened`.
- Consumed events named in the manifest: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- UI fragments named in the manifest: `BuildingInformationModelingOpsWorkbench`, `BuildingInformationModelingOpsDetail`, `BuildingInformationModelingOpsAssistantPanel`.
- Release-oriented docs named in the manifest: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Federation registry and discipline package map
**Justification:** Federated review breaks down when architectural, structural, services, civil, and interiors packages arrive without a governed record of origin, role, and intended use in the combined model.
**Improvement:** Add a federation registry around `bim_model` and `model_version` that records discipline, authoring party, coordinate basis, issue purpose, spatial coverage, level-of-development target, and allowed inclusion rules for review federations.
**Acceptance evidence:** A workbench view listing active federations by discipline, tests proving only approved model-version combinations can enter a federation, and release evidence that captures checksum plus approval state for every contributing package.

### 2. Shared coordinates and georeferencing assurance
**Justification:** Many coordination failures are not geometry defects but misaligned origins, rotated survey bases, or silently shifted reference points across incoming models.
**Improvement:** Validate every `model_version` against declared project coordinates, survey point, project base point, true north, elevation datum, and unit scale before it can participate in clash or quantity workflows.
**Acceptance evidence:** Ingestion checks that flag offset and rotation deviations, model-review screens that show the accepted coordinate basis, and release evidence proving the approved federation uses one declared spatial reference.

### 3. Model issue purpose governance
**Justification:** Teams need to distinguish work-in-progress, shared coordination, construction issue, record issue, and handover issue models because each state carries different approval and downstream consumption expectations.
**Improvement:** Extend `model_version` lifecycle metadata so each version has a governed issue purpose, publish gate, superseded-by linkage, and allowed downstream actions in `clash_issue`, `asset_object`, and `handover_package`.
**Acceptance evidence:** State transition tests for issue-purpose promotion, workbench badges that show current issue purpose, and audit trails proving downstream records were created only from allowed version states.

### 4. Drawing-to-model revision linkage
**Justification:** Construction teams work from sheets, views, and schedules as much as federated models, so revision trust depends on showing how drawings and model versions move together.
**Improvement:** Add revision-link records that connect `model_version` changes to impacted drawings, view sets, detail references, and package transmittals, with explicit supersession and approval history.
**Acceptance evidence:** A revision matrix showing model-version to drawing relationships, tests that block drawing release when a linked model revision is still unapproved, and release evidence bundling both model and drawing revision lists.

### 5. Spatial hierarchy completeness controls
**Justification:** Asset data, quantities, and issue routing lose operational meaning when spaces, levels, zones, buildings, and campuses are not governed as a coherent hierarchy.
**Improvement:** Model spatial hierarchy rules so `asset_object`, `clash_issue`, and `handover_package` records always reference valid site, building, storey, zone, and space context, with inheritance rules for higher-level approvals.
**Acceptance evidence:** Validation fixtures for missing or conflicting spatial parents, workbench filters by campus-to-space hierarchy, and release evidence reporting hierarchy completeness percentages by project area.

### 6. Quantity extraction baseline and measurement snapshots
**Justification:** Quantity trust depends on proving which version, measurement rules, and exclusion assumptions produced each takeoff, not just storing a final count.
**Improvement:** Add quantity snapshot support to `model_review` and `model_version` so governed measurements can be stored with unit rules, extraction date, excluded categories, manual overrides, and revision comparisons.
**Acceptance evidence:** Side-by-side quantity delta screens between versions, tests showing quantity baselines remain immutable after approval, and release evidence exporting measurement assumptions with every approved snapshot.

### 7. Clash taxonomy tuned for construction coordination
**Justification:** A single undifferentiated clash list overwhelms teams and hides the difference between hard clashes, clearance issues, access conflicts, workflow conflicts, and temporary tolerance exceptions.
**Improvement:** Expand `clash_issue` classification to include clash type, severity, impacted systems, responsible trade, required-by date, buildability risk, and allowed disposition options such as accepted, waived, redesign, or site-resolution required.
**Acceptance evidence:** Search and dashboards grouped by clash class, tests that enforce valid dispositions by severity, and release evidence showing closed-versus-open clash counts by trade and level.

### 8. Clash grouping and duplicate suppression
**Justification:** Teams waste review time when one underlying condition appears as dozens of near-identical clashes across adjacent elements and repeated federations.
**Improvement:** Add grouping logic for `clash_issue` that clusters duplicates by location, discipline pairing, affected systems, and root condition so coordination meetings operate on one governed issue with linked instances.
**Acceptance evidence:** Review screens that show grouped clashes and instance counts, tests proving duplicate detection is stable across reruns, and release evidence reporting duplicate reduction achieved per federation cycle.

### 9. Model issue ledger for design, construction, and handover
**Justification:** BIM operations need one governed place to manage issues from clash review, field verification, design comments, and handover defects instead of splitting them into disconnected logs.
**Improvement:** Introduce an issue-ledger workflow around `clash_issue` and `model_review` that captures source, assignee, due date, revision target, closure evidence, and whether the issue must be resolved before construction issue or handover approval.
**Acceptance evidence:** Workbench issue boards by status and source, tests that keep unresolved blocking issues from passing release gates, and audit history showing closure evidence for every closed issue.

### 10. Approval matrix by discipline, zone, and issue purpose
**Justification:** One approval path does not fit concept review, coordination issue, construction issue, and record issue releases across multiple disciplines and project zones.
**Improvement:** Add approval policies in `building_information_modeling_ops_policy_rule` so required approvers can vary by model discipline, impacted spatial area, issue purpose, and risk score.
**Acceptance evidence:** Policy-driven approval routing tests, workbench approval queues grouped by required role, and release evidence showing which approvals satisfied each model-version promotion.

### 11. Partial publish rules for staged model release
**Justification:** Large projects often release selected buildings, levels, or systems before the whole project is ready, and the PBC should support that without corrupting model governance.
**Improvement:** Allow `model_version` and `handover_package` records to declare controlled scope slices such as building wing, storey range, system family, or asset class, with rules for what can be published independently.
**Acceptance evidence:** Scope-aware release tests, workbench indicators that distinguish full versus partial issue status, and release evidence that explicitly states the approved scope slice for every staged release.

### 12. Delta evidence between successive model versions
**Justification:** Review effort is more efficient when teams can focus on changed spaces, systems, quantities, and assets rather than manually rediscovering the delta every cycle.
**Improvement:** Generate governed change summaries between successive `model_version` records covering geometry changes, deleted objects, reclassified assets, quantity shifts, moved spaces, and new unresolved issues.
**Acceptance evidence:** Version-comparison views with filterable deltas, tests verifying delta output stays tied to the compared versions, and release evidence attaching a signed change summary to every approved revision.

### 13. Asset tagging completeness and uniqueness rules
**Justification:** Handover and operations fail when equipment tags, space numbers, and system identifiers are duplicated, missing, or changed without traceable approval.
**Improvement:** Add validation around `asset_object` for tag uniqueness, tag format by asset class, superseded tag history, and reserved sequences for future installation lots.
**Acceptance evidence:** Duplicate-tag rejection tests, workbench completeness charts by asset class, and handover evidence listing asset records that passed uniqueness and format checks.

### 14. Structured handover data aligned to COBie-like expectations
**Justification:** Asset handover depends on reliable facility, floor, space, system, component, type, and document relationships even when the project is not exporting a named vendor format.
**Improvement:** Expand `handover_package` and `asset_object` coverage so the PBC can validate facility-management-ready datasets for spaces, systems, components, contacts, spares, warranties, and maintenance attributes using open, vendor-neutral mappings.
**Acceptance evidence:** Handover completeness rules for space, type, component, and document relationships, export previews before approval, and release evidence summarizing pass rates for each required handover data group.

### 15. Space and room data integrity checks
**Justification:** Downstream occupancy, equipment servicing, and wayfinding depend on spaces being complete, non-overlapping, and tied to the right room data.
**Improvement:** Add `model_review` checks for missing room numbers, overlapping spaces, inconsistent room names across models and drawings, and unassigned operational classifications such as plant room, riser, circulation, or tenant space.
**Acceptance evidence:** Automated room-integrity findings, workbench maps of invalid spaces, and approval gates that block handover release when required room metadata is incomplete.

### 16. System and zone membership governance
**Justification:** Operational analytics and maintenance planning require every governed asset to belong to a traceable system and, where relevant, a fire, security, environmental, or service zone.
**Improvement:** Extend `asset_object` and `handover_package` rules so system membership, zone membership, and service relationships are mandatory for defined asset classes before approval.
**Acceptance evidence:** Tests for missing system assignments, workbench drill-down from zone to assets, and release evidence showing system-assignment completeness by discipline and building area.

### 17. Location-to-asset consistency validation
**Justification:** Equipment records lose operational value when the declared space, level, and installed location do not match the approved model or drawing context.
**Improvement:** Validate `asset_object` location claims against spatial hierarchy, associated drawings, and current approved model versions, with explicit exceptions for off-model fabricated items and future phases.
**Acceptance evidence:** Location mismatch queues, traceable exception approvals for off-model assets, and handover evidence that every approved maintainable asset has a resolved installed location.

### 18. Drawing register and dependency awareness
**Justification:** Model approval often depends on related sheets, details, and schedules being at the same revision state, especially for construction issue releases.
**Improvement:** Add a governed drawing register linked to `model_version` and `model_review` so the PBC can track which sheets, schedules, and details are required companions for each release.
**Acceptance evidence:** Dependency tests that stop release when required sheets lag behind, workbench views of revision misalignment, and release evidence listing the approved drawing set attached to each model release.

### 19. Revision transmittal control
**Justification:** Coordination is weakened when teams cannot prove who received which revision, when it was issued, and what superseded it.
**Improvement:** Add transmittal records tied to `model_version` and `handover_package` that store issue date, recipients, issued purpose, superseded transmittal, and receipt acknowledgment where required.
**Acceptance evidence:** Transmittal history views, tests that keep superseded issues visible but non-current, and release evidence exporting the full revision transmittal chain for approved packages.

### 20. Construction work-package snapshots
**Justification:** Site teams often need focused packages by area or trade rather than full federations, and those slices must remain auditable after later revisions arrive.
**Improvement:** Allow `model_version` and `handover_package` to create immutable work-package snapshots for defined construction scopes such as slab pour area, riser zone, or equipment room fit-out.
**Acceptance evidence:** Snapshot creation tests, workbench views showing which site packages derive from which approved model versions, and release evidence bundling snapshot checksum, scope, and approval lineage.

### 21. Field verification intake for site observations
**Justification:** BIM operations are incomplete if field deviations, as-installed conditions, and survey confirmations cannot return into the governed model workflow.
**Improvement:** Add site-observation intake that turns field findings into `clash_issue` or `model_review` records with linked location, photo evidence, observation source, and required revision response.
**Acceptance evidence:** Intake fixtures for survey and field-walk observations, workbench queues for unresolved site findings, and release evidence proving all blocking site observations were resolved or formally waived.

### 22. Temporary works and construction-method model controls
**Justification:** Temporary supports, access zones, cranage paths, and protection works can materially affect clashes and approvals even though they are not permanent assets.
**Improvement:** Extend `bim_model` governance so temporary works models have distinct issue-purpose rules, review cadence, expiry dates, and separation from permanent handover content.
**Acceptance evidence:** Policy tests for temporary-versus-permanent model treatment, workbench filters for temporary works packages, and release evidence showing expired temporary packages were not carried into record issue or handover.

### 23. As-built reconciliation workflow
**Justification:** Record issue and handover quality depend on reconciling planned, installed, and verified conditions rather than assuming the latest construction issue model equals reality.
**Improvement:** Add an as-built reconciliation flow across `model_version`, `asset_object`, and `handover_package` that records deviations, accepted field changes, and outstanding gaps before record issue approval.
**Acceptance evidence:** Reconciliation dashboards showing planned-versus-installed differences, tests requiring closure of critical deviations before record issue, and release evidence attaching reconciliation summaries to approved as-built packages.

### 24. Handover readiness dashboard
**Justification:** Teams need a clear answer to whether a building, level, or system is ready for handover without manually cross-checking assets, issues, documents, and approvals.
**Improvement:** Build readiness scoring in `BuildingInformationModelingOpsWorkbench` using `handover_package`, `asset_object`, `clash_issue`, and `model_review` to show completeness, blockers, and projected readiness date by scope.
**Acceptance evidence:** Workbench dashboards by building and system, scoring tests for known readiness states, and release evidence capturing the readiness snapshot at approval time.

### 25. O and M document linkage to asset and system records
**Justification:** Operations handover is weakened when manuals, datasheets, certificates, and maintenance plans exist but are not tied to the right equipment, system, or space.
**Improvement:** Require `handover_package` to validate document-to-asset and document-to-system linkage, including document purpose, revision, approval state, and supersession history.
**Acceptance evidence:** Missing-document reports by asset class, tests blocking approval when mandatory document links are absent, and release evidence exporting the final document linkage matrix.

### 26. Commissioning prerequisite tracking
**Justification:** An asset may be geometrically complete in the model yet still unready for operations because tests, balancing, witness points, or certificates are missing.
**Improvement:** Extend `asset_object` and `handover_package` so maintainable assets can declare commissioning prerequisites, completion status, and gating effect on system or building handover.
**Acceptance evidence:** Commissioning status queues by system, approval tests that stop handover when mandatory prerequisites remain open, and release evidence that shows prerequisite completion at asset and system level.

### 27. Digital twin activation gates
**Justification:** A digital twin link should activate only when source models, asset attributes, and event interfaces are stable enough to support trustworthy runtime operations.
**Improvement:** Add activation criteria to `digital_twin_link` that require approved asset identifiers, stable spatial hierarchy, accepted handover data, and verified event mappings before twin synchronization begins.
**Acceptance evidence:** Activation checklists in the detail view, tests that block activation when handover gaps remain, and release evidence showing the exact approved inputs that enabled each twin link.

### 28. Quantity change approval thresholds
**Justification:** Large quantity shifts between revisions can indicate real scope change, modeling error, or omitted elements, and they should not pass as a silent side effect of model upload.
**Improvement:** Add threshold policies in `building_information_modeling_ops_policy_rule` so material quantity deltas by trade, zone, or asset class trigger review tasks and approval routing before version promotion.
**Acceptance evidence:** Threshold-trigger tests, workbench alerts for significant quantity shifts, and release evidence showing who approved each material quantity change.

### 29. Naming and classification policy enforcement
**Justification:** Model coordination, handover, and analytics all depend on stable naming and classification of spaces, systems, elements, and assets.
**Improvement:** Add configurable naming and classification rules for `bim_model`, `model_version`, and `asset_object`, including accepted code lists, reserved prefixes, and controlled exceptions with expiry dates.
**Acceptance evidence:** Validation reports showing non-compliant objects, workbench policy exception queues, and release evidence demonstrating classification compliance by discipline.

### 30. Units and measurement normalization
**Justification:** Mixed units quietly corrupt quantities, elevations, and clearance checks, especially when packages come from different authoring contexts.
**Improvement:** Normalize all measurement fields used by `model_version`, `clash_issue`, and `asset_object` with declared project units, conversion provenance, and tolerance rules for imported content.
**Acceptance evidence:** Tests covering unit conversion and tolerance limits, workbench visibility of declared project units, and release evidence confirming the unit baseline used for each approved package.

### 31. Model health score with actionable factors
**Justification:** Teams need one high-signal indicator of model readiness, but it must be explainable and decomposed into fixable causes.
**Improvement:** Add a health score to `model_review` driven by clash severity, quantity variance, missing classifications, unresolved site findings, handover completeness, and policy exceptions.
**Acceptance evidence:** Score breakdown views in the workbench, calibration tests across known good and poor packages, and release evidence storing the final health score and factor weights at approval.

### 32. External event boundary for controlled downstream updates
**Justification:** BIM operations should publish domain events outward without leaking internal table structure or forcing downstream consumers to infer meaning from generic updates.
**Improvement:** Expand emitted events beyond coarse lifecycle notifications so approvals, revision supersessions, clash-closure milestones, handover readiness changes, and digital twin activation are explicit domain events.
**Acceptance evidence:** Event contract tests for each outward-facing event type, examples in `RELEASE_EVIDENCE.md`, and proof that outgoing payloads carry domain identifiers without exposing internal persistence structure.

### 33. Incoming event handling for policy and KPI changes
**Justification:** Consumed policy and KPI events matter only if the PBC can explain which records were affected and what action followed.
**Improvement:** Use `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` to re-evaluate approval thresholds, seal audit artifacts, refresh readiness metrics, and open targeted review tasks where BIM records are now out of tolerance.
**Acceptance evidence:** Idempotent handler tests, workbench traces from source event to affected records, and release evidence showing which inbound events altered readiness or approval outcomes.

### 34. API boundary for heavy-model and metadata workflows
**Justification:** Geometry packages, metadata updates, and approval actions have different performance and retry characteristics and should not be collapsed into one command shape.
**Improvement:** Split the current API surface into clear command boundaries for model registration, metadata revision, clash ingestion, asset enrichment, handover validation, and approval promotion, each with idempotency semantics suited to the domain action.
**Acceptance evidence:** Route contracts documenting command purpose, tests proving repeated submissions do not duplicate approved records, and release evidence showing stable API behavior across representative large-model workflows.

### 35. Release evidence bundle generator
**Justification:** BIM release decisions need one authoritative bundle of model versions, drawings, issues, approvals, quantities, and handover checks rather than scattered screenshots and ad hoc exports.
**Improvement:** Generate release bundles from `model_version`, `model_review`, `clash_issue`, `handover_package`, and `building_information_modeling_ops_control_assertion`, with immutable timestamps and approval lineage.
**Acceptance evidence:** One-click bundle generation in the workbench, tests proving the bundle contents are immutable after approval, and package-local release evidence artifacts that map each approval to its supporting checks.

### 36. Continuous control assertions for BIM governance
**Justification:** Governance is stronger when release controls are evaluated continuously, not only at the final signoff meeting.
**Improvement:** Use `building_information_modeling_ops_control_assertion` to run scheduled checks for missing approvals, unresolved blocking clashes, incomplete handover attributes, stale drawings, and invalid asset locations.
**Acceptance evidence:** Control dashboards with pass-fail history, tests for control firing and suppression behavior, and release evidence linking every approved package to passing control assertions at the moment of signoff.

### 37. Agent skill for clash triage summaries
**Justification:** Coordination meetings are faster when the assistant can summarize the real pattern of unresolved clashes instead of just listing raw issue counts.
**Improvement:** Add an assistant skill in `BuildingInformationModelingOpsAssistantPanel` that groups `clash_issue` records by trade pair, level, room, system, and repeated root cause, then drafts a concise meeting brief with recommended focus areas.
**Acceptance evidence:** Prompt-to-brief demos grounded in live clash data, tests that include source citations back to the underlying issues, and release evidence showing assistant summaries were reviewable before use.

### 38. Agent skill for handover gap detection
**Justification:** Handover packages often fail because the missing data is scattered across spaces, assets, documents, and approvals, which is tedious to detect manually.
**Improvement:** Add an assistant skill that reviews `handover_package` and `asset_object` completeness, identifies the minimum missing evidence for approval, and drafts targeted remediation tasks by discipline or system.
**Acceptance evidence:** Assistant-generated remediation plans with cited missing fields, tests that verify no completion claim is made without supporting data, and release evidence showing reviewer acceptance or correction of the assistant output.

### 39. Agent skill for revision impact briefs
**Justification:** Supervisors need to know whether a revision changes quantities, spaces, critical assets, or approval scope before they decide on release urgency.
**Improvement:** Add an assistant workflow that compares two `model_version` records and produces an impact brief covering changed zones, shifted quantities, affected drawings, reopened issues, and handover implications.
**Acceptance evidence:** Comparison prompts that return cited impact briefs, tests for correct handling of superseded versions, and release evidence storing the approved impact brief alongside the promoted revision.

### 40. Federation operations workbench
**Justification:** Model federation decisions are central operational work and deserve a dedicated interface rather than being buried inside generic record pages.
**Improvement:** Expand `BuildingInformationModelingOpsWorkbench` with a federation workspace showing participating models, coordinate status, last reviewed version, current health score, and pending publish blockers.
**Acceptance evidence:** Route-level UI tests for the federation workspace, empty and degraded-state handling, and release evidence screenshots demonstrating federation status before approval.

### 41. Issue triage workbench
**Justification:** Coordination teams need a fast way to work through model issues by location, trade, severity, and due date during live review sessions.
**Improvement:** Add an issue-triage view that surfaces `clash_issue` and site-derived findings with filters for building, level, room, system, responsible trade, and blocking status.
**Acceptance evidence:** UI tests for triage filtering and bulk status actions, workbench exports for meeting minutes, and release evidence showing unresolved blocking issues were visible at signoff.

### 42. Asset and handover workbench
**Justification:** Handover readiness is too broad for one generic detail page and requires a focused workbench for assets, documents, spaces, and commissioning status.
**Improvement:** Add a dedicated handover workspace that brings together `asset_object`, `handover_package`, missing document links, commissioning prerequisites, and spatial assignment gaps.
**Acceptance evidence:** UI coverage for readiness cards and drill-down paths, tests for permission-sensitive actions, and release evidence snapshots of asset and handover completeness at package approval.

### 43. Approval and evidence workbench
**Justification:** Approvers need to see exactly what they are signing, what changed, and which controls passed without navigating across multiple disconnected views.
**Improvement:** Create an approval desk that assembles revision delta, unresolved issues, quantity changes, control assertions, required approvers, and generated release bundle for each candidate approval.
**Acceptance evidence:** UI tests proving all approval prerequisites are visible in one route, approval action logs with rationale capture, and release evidence confirming the approver saw the generated bundle before signoff.

### 44. Exception taxonomy and service levels
**Justification:** Not every defect should carry the same urgency, and BIM operations need explicit response expectations for blocking coordination, field-safety, and handover-critical exceptions.
**Improvement:** Define exception classes in `building_information_modeling_ops_runtime_parameter` and `building_information_modeling_ops_policy_rule` for coordination-critical, construction-critical, handover-critical, and informational issues, each with target response and escalation rules.
**Acceptance evidence:** Timed exception workflows in the workbench, SLA-breach tests, and release evidence reporting exception aging and escalation outcomes for the approved release.

### 45. Multi-project and multi-tenant isolation with shared standards
**Justification:** Organizations often run several projects with shared naming standards but distinct approval paths, data residency constraints, and access boundaries.
**Improvement:** Ensure `building_information_modeling_ops_governed_model` supports project-specific policies, scope filters, and evidence bundles while preserving shared standard libraries and preventing cross-project data leakage.
**Acceptance evidence:** Tenant isolation and project isolation tests, policy inheritance views showing standard-versus-project overrides, and release evidence proving project bundles contain only project-scoped records.

### 46. Controlled schema extension for client-specific handover attributes
**Justification:** Different owners require different warranty, maintenance, sustainability, or asset-criticality fields, and those extensions should be governed rather than copied into ad hoc payloads.
**Improvement:** Use `building_information_modeling_ops_schema_extension` to add client-specific handover and asset attributes with validation rules, migration history, and compatibility checks against existing exports and approvals.
**Acceptance evidence:** Extension registration tests, workbench visibility of active extensions, and release evidence showing which client-specific attributes were mandatory for the approved handover package.

### 47. Carbon and sustainability metadata tied to quantities and assets
**Justification:** Sustainability reporting is increasingly part of BIM operations, but it needs auditable ties back to model quantities, assemblies, and approved revisions.
**Improvement:** Extend `model_review`, `asset_object`, and quantity snapshots so embodied and operational sustainability indicators can be traced to approved model versions, material quantities, and system assignments.
**Acceptance evidence:** Sustainability drill-down views from metric to source quantity, tests for revision-to-metric traceability, and release evidence exporting the approved sustainability summary with source links.

### 48. Construction sequencing and location-readiness checks
**Justification:** A federated model may be geometrically correct while still being unready for site use because sequence logic, access zones, or predecessor scopes are unresolved.
**Improvement:** Add sequencing-aware checks in `model_review` so location packages can declare predecessor completion, access constraints, temporary works dependencies, and readiness for upcoming trade work.
**Acceptance evidence:** Readiness boards by construction zone, tests that block site package release when predecessor checks fail, and release evidence showing location-readiness status for each staged construction package.

### 49. Archive, supersession, and legal retention governance
**Justification:** BIM records have long-lived operational value, so the PBC must preserve approved versions, transmittals, and evidence without confusing current use with historical archive.
**Improvement:** Add retention and archive rules for `bim_model`, `model_version`, `handover_package`, and release bundles so superseded packages remain queryable, immutable, and clearly marked as non-current.
**Acceptance evidence:** Archive retrieval tests, workbench history views that separate current from superseded releases, and release evidence showing the immutable archive record created at supersession time.

### 50. Operational KPI pack for BIM release confidence
**Justification:** Leadership needs a compact, defensible set of metrics that expresses whether BIM operations are improving release quality, not just moving records faster.
**Improvement:** Use `OperationalKpiChanged` and package analytics to publish KPIs for federation health, blocking clash burn-down, asset-data completeness, handover readiness, approval latency, revision churn, and release rework rate.
**Acceptance evidence:** KPI definitions wired into the analytics workbench, tests for metric calculation and period consistency, and release evidence attaching the KPI pack that was current at the time of approval.
