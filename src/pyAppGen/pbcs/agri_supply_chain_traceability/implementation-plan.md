## Implementation Plan

### Scope

Deliver a standalone one-PBC executable surface for
`agri_supply_chain_traceability` strictly inside this package.

### Slice Selected

Use the existing package-local release gate as the operational center of the
slice, then wrap it with the missing standalone app composition required to make
this PBC independently executable and auditable.

### Why This Slice

- `improve1.md` explicitly calls for release-readiness, recall readiness,
  document-led intake, operator tooling, and richer API and event boundaries.
- The package already owns the core evidence tables needed to implement a real
  release decision without crossing into shared infrastructure.
- A package-local standalone surface closes the gap between metadata contracts
  and a functional one-PBC app entrypoint.

### Work Items

1. Keep the existing package-local runtime and extend it only where the slice
   needs missing executable coverage.
2. Add a stateful service layer that executes runtime commands against owned
   package state instead of returning metadata only.
3. Replace placeholder routes with a real route catalog and dispatcher for the
   standalone app surface while preserving legacy compatibility aliases.
4. Expand UI metadata to include a standalone shell, navigation, forms,
   wizards, controls, and a rendered workbench view over package-local state.
5. Strengthen agent planning and model contracts so document intake and CRUD
   previews point to real package-local operations and owned tables.
6. Add standalone release evidence and focused tests for repo-gate style source,
   implementation, and generation audits.
7. Refresh package docs to match the implemented standalone slice.

### Constraints

- Stay inside `src/pyAppGen/pbcs/agri_supply_chain_traceability`.
- Do not edit shared generator, DSL, or progress-ledger files.
- Do not add dependencies.
- Keep all writes within owned package tables and AppGen-X event surfaces.

### Verification Plan

- Compile all modified package modules with `python3 -m py_compile`.
- Run focused pytest for package-local tests.
- Run available package-local release evidence and smoke audits.
- Check git diff to confirm the change stayed inside this PBC directory.
