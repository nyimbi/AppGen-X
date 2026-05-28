# Composition Engine PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `composition_engine`. The focus is application composition correctness: PBC selection, dependency boundaries, UI fragment assembly, generated DSL, side-effect-free package registration, release evidence, and agent-assisted composition planning.

## Current Domain Evidence Used

- Domain purpose: application composition plane for turning selected PBCs into generated applications through workspaces, selected PBCs, component registrations, UI fragments, layout bindings, generated DSL, package registration plans, index entries, release evidence, and publication events.
- Owned boundary: composition workspaces, component registry, UI fragments, layout bindings, DSL artifacts, composition plans, validation runs, package registration plans, package index entries, release evidence, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command surface: workspace creation, PBC selection, component registration, fragment registration, layout binding, plan validation, side-effect-free package planning, DSL generation, publication, control testing, boundary verification, rule/parameter/configuration management, and AppGen-X inbox handling.
- Existing events and dependencies: emits `CompositionWorkspaceCreated`, `PbcSelectedForComposition`, `ComponentRegistered`, `UiFragmentRegistered`, `LayoutBound`, `CompositionPlanValidated`, `PackageRegistrationPlanned`, `CompositionPublished`, and `PbcDeployed`; consumes schema, route, audit, access-policy, workflow, and package-registration events through AppGen-X projections.

## 50 Better-Than-World-Class Improvements

### 1. Capability selection rationale graph

**Justification:** Selecting PBCs is a design decision that should preserve user intent, business scope, dependencies, rejected alternatives, and expected generated surfaces.

**Improvement:** Add a rationale graph linking prompts, selected PBCs, required capabilities, optional capabilities, rejected PBCs, dependencies, and release assumptions. The agent should explain why each PBC is included and which requirement would fail if removed.

### 2. Composition boundary proof

**Justification:** Composition can accidentally create shared-table coupling when pages, generated services, or projections blur PBC boundaries.

**Improvement:** Build a boundary proof that enumerates every selected PBC table, generated route, projection, event, and API dependency, then proves no direct foreign-table references exist. Fail validation when a binding or generated DSL crosses an undeclared boundary.

### 3. Dependency compatibility solver

**Justification:** A composed app is only viable when selected PBCs agree on schema versions, events, permissions, routes, agent competencies, and release gates.

**Improvement:** Add a solver that consumes schema, gateway, identity, workflow, and audit projections to compute compatible dependency sets, missing contracts, version conflicts, and required upgrades. The workbench should show satisfiable and unsatisfiable dependency reasons.

### 4. Prompt-to-composition traceability

**Justification:** Natural-language generation must be auditable; users need to know how prompt text became selected PBCs, pages, routes, and DSL.

**Improvement:** Store prompt spans, extracted intents, mapped PBCs, inferred constraints, confidence, and human overrides. Generated DSL should include trace metadata linking back to source intent without storing sensitive prompt content unnecessarily.

### 5. Workspace lifecycle governance

**Justification:** Composition workspaces move through exploration, draft, review, validation, publication, and retirement; a generic status field is not enough.

**Improvement:** Define explicit workspace lifecycle states, allowed transitions, review requirements, freeze behavior, publication locks, retirement rules, and audit evidence. UI actions should be state-aware and permission-filtered.

### 6. PBC selection impact preview

**Justification:** Adding or removing a PBC changes schema, routes, UI, workflow, permissions, agent skills, tests, and release evidence.

**Improvement:** Add impact previews for PBC selection changes showing added/removed tables, services, UI fragments, permissions, events, dependencies, generated files, DSL blocks, smoke tests, and release blockers.

### 7. Mesh-level architecture validation

**Justification:** Composed applications must respect platform fabric, finance, supply-chain, HCM, commerce, and intelligence mesh boundaries while still integrating through declared contracts.

**Improvement:** Validate mesh assignments, cross-mesh dependency direction, required platform-fabric PBCs, forbidden cycles, and operational topology. Provide architecture warnings when a composition lacks identity, audit, schema, gateway, workflow, or composition governance.

### 8. UI fragment capability contract

**Justification:** A UI fragment is more than a component key; it needs data requirements, permissions, events, slots, navigation, empty states, and agent affordances.

**Improvement:** Extend fragment registration with required projections, command bindings, permissions, responsive modes, route ownership, emitted events, consumed events, empty/error states, and agent actions. Validate bindings against this contract before layout publication.

### 9. Layout constraint solver

**Justification:** Drag-and-drop layouts break under responsive constraints, required fragments, route nesting, and permission-driven visibility.

**Improvement:** Add a layout solver for slot capacity, responsive breakpoints, required/optional fragments, navigation depth, accessibility order, permission hiding, and route density. Store solved alternatives and rejected layouts.

### 10. Route map collision detector

**Justification:** Selected PBC fragments can generate conflicting page routes, nested paths, permissions, or navigation labels.

**Improvement:** Detect route collisions, ambiguous navigation, duplicate page names, path shadowing, permission mismatch, and gateway route conflicts. Block DSL generation until conflicts are resolved or explicitly remapped.

### 11. Composition DSL round-trip tests

**Justification:** Generated DSL is only useful if it can be parsed, validated, regenerated, and compared without losing meaning.

**Improvement:** Add round-trip tests for every DSL artifact: generated DSL, parsed model, regenerated DSL, checksum, selected PBCs, pages, projections, agent skills, deployment topology, and release evidence. Show lossy fields as validation blockers.

### 12. DSL diff and review workflow

**Justification:** Reviewers need to understand composition changes as semantic deltas, not raw text diffs.

**Improvement:** Add DSL diffs for PBC selections, pages, bindings, events, projections, permissions, agents, tests, deployment units, and package metadata. The workbench should support approve/reject with comments and release impact.

### 13. Side-effect-free package registration simulator

**Justification:** Package registration must be previewable without mutating package indexes or deployment state.

**Improvement:** Strengthen registration planning with simulated index entries, required approvals, package metadata validation, version conflicts, rollback steps, and external registration API calls marked as planned-only. Tests should prove no side effects occur during planning.

### 14. Package index quality scoring

**Justification:** A package index entry should be discoverable, trustworthy, and complete.

**Improvement:** Score package entries for domain description, capabilities, PBC list, version, compatibility, UI fragments, agent competencies, release evidence, docs, tags, ownership, and support metadata. Block publication of low-quality entries.

### 15. Release evidence completeness matrix

**Justification:** Composition release evidence must combine selected PBC evidence, generated app evidence, DSL evidence, package plan evidence, and integration evidence.

**Improvement:** Build a matrix mapping every selected PBC to schema, model, service, route, event, handler, UI, RBAC, configuration, seed, agent, test, smoke, boundary, and release evidence. Show missing cells as actionable blockers.

### 16. Cross-PBC UI navigation model

**Justification:** A composed app needs coherent navigation across fragments from many PBCs without flattening domain boundaries.

**Improvement:** Add navigation descriptors with menu groups, route hierarchy, default landing pages, cross-PBC links, breadcrumbs, permission visibility, and deep-link policy. Validate navigation density and role-specific views.

### 17. Projection freshness gating

**Justification:** Composition validation depends on projections from schema, gateway, identity, workflow, audit, and package registration.

**Improvement:** Track projection freshness, source event, lag, error, and validation impact. Block publication when required projections are stale or mark the exact risk when non-critical projections are degraded.

### 18. Permission merge and conflict analysis

**Justification:** Selected PBCs expose many permissions that must become coherent app roles without overgranting.

**Improvement:** Merge permission descriptors, detect duplicate semantics, conflicting scopes, missing role mappings, orphaned UI actions, and overbroad grants. Generate least-privilege role suggestions with human approval.

### 19. Agent competency composition

**Justification:** The composed application agent must merge PBC-specific skills into one safe assistant while preserving permissions and boundaries.

**Improvement:** Add competency composition records for each selected PBC skill, required permission, safe reads, mutation previews, document inputs, handoff rules, and confirmation gates. Generate a single agent capability map in the DSL.

### 20. Agent routing and handoff policy

**Justification:** A single application agent must know which PBC skill owns a question or action, and when multiple PBCs must cooperate.

**Improvement:** Build routing policies that map intents to PBC competencies, required context, dependency projections, escalation paths, and conflict resolution. Store explanations for why the agent chose a given PBC skill.

### 21. Document-driven composition intake

**Justification:** Users describe desired applications in requirements documents, operating procedures, spreadsheets, and package descriptions.

**Improvement:** Add document ingestion that extracts domains, workflows, roles, pages, data objects, reports, integrations, and constraints. The agent should create draft composition plans with citations, confidence, and unresolved questions.

### 22. Composition risk model governance

**Justification:** Release-risk scoring affects publication decisions and must be explainable.

**Improvement:** Govern risk models with feature lineage, deterministic fallback, drift checks, approval status, confidence, and explanation. Risk scores should list concrete contributors such as stale projection, route conflict, missing UI, or weak test evidence.

### 23. Counterfactual composition simulation

**Justification:** Users need to compare alternative PBC sets, layouts, and release plans before committing.

**Improvement:** Simulate scenarios such as including/excluding a PBC, changing layout mode, adding workflow orchestration, or deferring an integration. Compare generated files, route count, dependencies, risk, and release readiness.

### 24. Fragment-slot allocation economics

**Justification:** Limited screen space should prioritize high-value workflows, role needs, and required controls.

**Improvement:** Add allocation policies that score fragments by role importance, task frequency, regulatory need, dependency freshness, and layout density. Persist rejected allocations and show why a fragment was placed or omitted.

### 25. Responsive and accessibility validation

**Justification:** Composed UI fragments must remain usable across device sizes and accessibility modes.

**Improvement:** Validate responsive slots, keyboard order, labels, contrast metadata, landmark structure, focus routes, and hidden-action behavior for every layout binding. Block publication when required fragments cannot satisfy accessibility constraints.

### 26. Generated app smoke plan synthesis

**Justification:** Each composition needs tests that reflect its selected PBCs and cross-PBC routes, not only generic package tests.

**Improvement:** Generate a smoke plan from selected PBCs, routes, events, handlers, UI fragments, agent skills, and dependency projections. Include expected files, commands, assertions, and release gates in DSL artifacts.

### 27. Dependency cycle and startup order analysis

**Justification:** Some selected PBCs can create event/projection or deployment cycles that complicate generated app startup.

**Improvement:** Analyze dependency graphs for cycles, required bootstrap order, optional degraded mode, and missing seed prerequisites. Generate startup phases and readiness checks for the composed application.

### 28. Deployment topology synthesis

**Justification:** Composition should produce deployable units, not only application code.

**Improvement:** Generate deployment topology descriptors for services, workers, jobs, sidecars, embedded modules, and monolith groupings based on selected PBCs and workload needs. Validate scale, health checks, and dependency readiness in the DSL.

### 29. Composition rollback planning

**Justification:** Publication can break users if the generated app, package index, or deployment topology must be rolled back without a plan.

**Improvement:** Add rollback plans covering prior DSL artifact, previous package index entry, generated files, route map, deployment topology, and data migration constraints. Publication should store rollback evidence and limits.

### 30. Workspace branch and merge

**Justification:** Teams need to explore competing compositions and merge approved changes.

**Improvement:** Add branch records, merge requests, conflict detection for PBC selections/layout/routes/DSL/package metadata, reviewer decisions, and merge audit evidence. The UI should show semantic conflicts rather than raw file conflicts.

### 31. Composition ownership model

**Justification:** Workspaces, package plans, PBC selections, and publication decisions need accountable owners.

**Improvement:** Add ownership metadata for business owner, technical owner, release approver, package publisher, and support group. Release evidence should block ownerless published compositions.

### 32. Tenant-specific composition variants

**Justification:** Generated applications may need tenant-specific layouts, enabled PBCs, package entries, or policies without breaking base composition.

**Improvement:** Model base composition plus tenant overlays for fragments, permissions, parameters, and route visibility. Validate overlays for boundary safety and compatibility with base release evidence.

### 33. Marketplace readiness workflow

**Justification:** A composed app package should be ready for discovery, review, installation, and support before publication.

**Improvement:** Add marketplace readiness checks for package metadata, screenshots or UI descriptors, capability list, compatibility, install steps, support policy, release evidence, and rollback plan. Keep registration plan side-effect-free until publish approval.

### 34. External PBC intake validation

**Justification:** External self-registering PBCs can introduce incomplete contracts, unsafe dependencies, or poor UI/agent capabilities.

**Improvement:** Validate external PBC manifests, owned schema, API/event contracts, UI fragments, agent competencies, release evidence, dependency declarations, and backend/eventing constraints before allowing selection in a composition.

### 35. Composition policy rule compiler

**Justification:** Composition rules need deterministic behavior and test cases.

**Improvement:** Compile rules for required fragments, allowed meshes, route budgets, approval requirements, publication modes, and tenant constraints. Each rule version should include fixtures and a stable compiled hash.

### 36. Route-budget economics

**Justification:** Route count affects usability, security review, gateway load, and generated app complexity.

**Improvement:** Add route-budget analysis by PBC, page, role, API, and workflow. Recommend consolidation, grouping, or hidden advanced routes when budgets are exceeded.

### 37. Generated artifact lineage

**Justification:** Every generated file should be traceable to selected PBCs, DSL nodes, UI fragments, schemas, or agent competencies.

**Improvement:** Store lineage from DSL artifacts to generated models, services, routes, UI, tests, config, and docs. Workbench users should inspect why a file exists and what input would change it.

### 38. Composition observability

**Justification:** Operators need to know how compositions are changing over time and where publication repeatedly fails.

**Improvement:** Track workspace count, validation blockers, route conflicts, missing fragments, stale projections, package plan failures, publication latency, and release readiness trends. Add analytics panels with drilldowns.

### 39. Publication freeze and emergency override

**Justification:** Composition publication may need to freeze during incidents or proceed under emergency controls.

**Improvement:** Add freeze policies with scope, reason, expiry, allowed exceptions, approver, and audit evidence. Emergency publication should require explicit risk acceptance and rollback plan.

### 40. Release note generation

**Justification:** Composed app users need clear release notes describing PBC additions, route changes, UI changes, permissions, agent skills, and known limitations.

**Improvement:** Generate release notes from DSL diffs, PBC selection changes, layout changes, package index changes, and release evidence. The agent should draft notes and link them to publication records.

### 41. Composition-specific seed orchestration

**Justification:** Selected PBCs may require seeds that must be ordered, scoped, and validated in the generated app.

**Improvement:** Build seed orchestration plans that order PBC seeds, resolve tenant overlays, detect conflicts, verify idempotency, and include rollback or cleanup guidance. Include seed proof in release evidence.

### 42. Generated configuration harmonization

**Justification:** Selected PBCs expose parameters and configuration that can conflict or overwhelm users.

**Improvement:** Merge configuration schemas into a composition-level configuration plan with defaults, constraints, ownership, UI grouping, secrets handling, and validation. Keep per-PBC ownership while generating a coherent app settings surface.

### 43. Documentation coverage matrix

**Justification:** A composed application is incomplete without user, operator, developer, package, and agent documentation.

**Improvement:** Generate a documentation matrix for selected PBCs, generated routes, UI fragments, agent skills, deployment topology, package registration, and release evidence. Block marketplace publication when required docs are missing.

### 44. Composition release rehearsal

**Justification:** Publication should be rehearsed before it mutates release evidence or package index state.

**Improvement:** Add release rehearsal that validates DSL parse, generated artifact plan, package registration plan, dependency projections, route map, UI layout, and smoke plan without publishing. Store rehearsal results separately from actual publication.

### 45. Cross-PBC workflow stitching

**Justification:** Compositions often need workflows that link selected PBCs through events and APIs.

**Improvement:** Generate workflow stitching candidates using selected PBC events, commands, UI actions, and agent skills. Validate each candidate through workflow orchestration contracts before adding it to generated DSL.

### 46. Composition security review panel

**Justification:** Security posture emerges from the combination of PBCs, permissions, routes, agents, documents, and deployment topology.

**Improvement:** Add a security panel that highlights exposed routes, sensitive fields, overbroad permissions, missing audit lineage, risky agent actions, external PBCs, and tenant overlays. Link each finding to a release blocker or accepted risk.

### 47. Data residency and deployment fit

**Justification:** Composed apps may select PBCs whose data residency, deployment units, or tenancy assumptions are incompatible.

**Improvement:** Validate residency tags, allowed regions, tenant isolation mode, deployment topology, and cross-region dependencies for selected PBCs. Show deployment-fit blockers before publication.

### 48. Composition agent safety tests

**Justification:** Composed agents with many PBC skills can accidentally perform cross-domain mutations or expose data.

**Improvement:** Generate tests for agent routing, permission denial, mutation preview, document ingestion redaction, cross-PBC handoff, and unsafe request refusal. Include results in composition release evidence.

### 49. Package discovery feedback loop

**Justification:** Published packages need feedback from install attempts, search behavior, compatibility failures, and user ratings to improve discoverability.

**Improvement:** Add feedback projections and package-index metrics for searches, installs, failures, version conflicts, and missing capabilities. Use them to suggest metadata, docs, or compatibility improvements without mutating external indexes directly.

### 50. Composition-engine competency catalog

**Justification:** The composed application agent needs first-class composition skills for planning, explaining, validating, and publishing apps.

**Improvement:** Publish competencies for prompt intake, PBC selection rationale, layout planning, DSL review, dependency solving, package registration preview, release readiness explanation, and rollback planning. Each competency should declare permissions, safe reads, mutation previews, document inputs, and emitted AppGen-X events.
