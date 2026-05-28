## Scope

Implement the `claims_adjudication_healthcare` PBC as a package-local, executable one-PBC adjudication app without touching shared AppGen-X infrastructure or other PBCs.

## Constraints

- Only modify files under `src/pyAppGen/pbcs/claims_adjudication_healthcare`.
- Keep shared package entrypoints stable so existing imports and package discovery keep working.
- Use owned tables, AppGen-X events, and declared projections only; no foreign table reads or writes.
- Prefer a cohesive in-memory reference implementation over scaffold metadata.

## Delivery Plan

1. Replace scaffold contracts with a domain-specific adjudication core:
   - claim intake normalization
   - line-level adjudication
   - benefit rule and parameter governance
   - denial, appeal, and payment-integrity workflows
   - AppGen-X outbox/inbox/dead-letter handling
2. Rebuild package adapters around that core:
   - schema/model contracts
   - services and route dispatch
   - UI/workbench, forms, wizards, and controls
   - RBAC, rules, runtime configuration, and seed data
   - agent/chatbot document-instruction CRUD and governed datastore plans
3. Refresh package-local evidence:
   - `README.md`
   - `implementation-status.md`
   - `RELEASE_EVIDENCE.md`
   - focused migration DDL
4. Add focused package-local tests for:
   - claim adjudication outcomes
   - event idempotency and dead-letter behavior
   - route and agent/document-instruction flows
   - metadata/release evidence integrity
5. Validate with import/compile checks and focused pytest runs if the environment supports them.

## Intended Outcome

The PBC should be executable as a self-contained healthcare claims adjudication slice with meaningful domain behavior rather than generic generated stubs.
