# Enterprise Search Vector Implementation Plan

## Goal

Make `enterprise_search_vector` function as a standalone one-PBC AppGen-X app
without leaving its package boundary. The package should expose executable
runtime behavior, package-owned schema and migration evidence, standalone app
composition, UI workbench metadata, governance controls, AppGen-X eventing,
agent/chatbot planning, focused tests, and release/readiness proof.

## Constraints

- Edit only `src/pyAppGen/pbcs/enterprise_search_vector`.
- Do not rely on shared-table access or cross-PBC writes.
- Keep the implementation side-effect-free and executable in-package.
- Preserve the existing package contract shape where possible.

## Chosen Backlog Themes

The backlog in `improve1.md` is broad. This implementation targets the highest
leverage package-local themes that materially improve standalone usability:

1. Standalone app composition and domain workflows.
2. UI forms, wizards, and operator controls for search operations.
3. Search governance evidence for ACL screening, relevance controls, retention,
   governed models, and proof generation.
4. Better runtime record completeness for advanced search operations.
5. Dynamic release evidence and migration coverage derived from actual package
   code and SQL artifacts.
6. Agent/chatbot/document/CRUD planning validation in focused tests.

## Planned Code Changes

1. Add a package-local standalone composition module.
   - Build a standalone app definition from existing manifest, routes,
     services, UI, permissions, events, seed data, agent contribution, and
     release evidence.
   - Add executable workflow helpers for bootstrap, ingestion/embedding,
     governed search, and governance review.
   - Add a standalone smoke test path.

2. Expand the UI contract to cover forms, wizards, and controls.
   - Add structured form definitions for index setup, document ingestion,
     embedding jobs, hybrid search, governance rules, and governed models.
   - Add wizard definitions for bootstrap, governed retrieval, and quality
     remediation.
   - Add operator controls for ranking weights, ACL preview, freshness,
     query-risk screening, and proof generation.
   - Surface those definitions in workbench rendering.

3. Tighten runtime domain behavior.
   - Fix advanced runtime issues that are currently under-tested, including
     query-intent-risk scoring and field alignment for advanced records.
   - Ensure deleted or purged documents are excluded from retrieval and index
     counts.
   - Add more explicit governance metadata where the runtime already owns the
     corresponding records.

4. Improve seed and bootstrap coverage.
   - Replace thin seed rows with a richer package-local seed bundle for
     configuration, parameters, rules, indexes, sample documents, and governed
     models used by the standalone app bootstrap.

5. Replace stale hard-coded release evidence.
   - Generate release evidence dynamically from package contracts.
   - Parse the package SQL migration to prove every owned/runtime table is
     created by the package-local migration artifact.
   - Include standalone app readiness and documentation coverage.

6. Extend focused tests.
   - Add standalone app tests.
   - Add agent/chatbot/document/CRUD planning tests.
   - Add migration evidence coverage tests.
   - Add advanced runtime data-shape and regression tests.

## Verification Plan

- Run `python3 -m compileall` on the package.
- Run the package contract tests through a direct Python harness because the
  worktree currently does not have a working `pytest` executable/module.
- Review the final diff for schema/runtime mismatches and stale references.

## Expected Deliverables

- `implementation-plan.md`
- Standalone composition code
- Updated runtime/UI/seed/release evidence code
- Expanded focused tests
- `implementation-status.md`
- Package `README.md`
