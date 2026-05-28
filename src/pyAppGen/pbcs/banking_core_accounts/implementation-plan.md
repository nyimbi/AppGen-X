# Banking Core Accounts Improvement Plan

## Selected Slice

Implement the canonical deposit-account lifecycle slice from `improve1.md` with executable package-local code:

- formal lifecycle states for `deposit_account`
- guarded state transitions with maker-checker enforcement for sensitive actions
- AppGen-X outbox evidence for lifecycle commands
- account detail and workbench queries that expose current state and next allowed actions

This is intentionally narrower than the full backlog. It strengthens the package where the current code is weakest without widening scope into statements, shared projections, or foreign-table integrations.

## Scope Boundaries

- Stay inside `src/pyAppGen/pbcs/banking_core_accounts`
- Keep eventing AppGen-X only
- Do not add any stream-engine picker behavior
- Do not introduce shared-table access or foreign-table reads
- Do not add dependencies
- Keep the runtime side-effect-free and package-testable

## Planned Code Changes

1. Add a package-local lifecycle module that owns:
   - lifecycle states
   - allowed transitions
   - maker-checker rules
   - idempotent command receipts
   - account detail / workbench projections
2. Update `runtime.py` to:
   - initialize lifecycle-aware state
   - delegate deposit-account open / transition / query flows to the lifecycle module
   - expose lifecycle evidence from runtime smoke and release evidence builders
3. Update `services.py` and `routes.py` to publish the new executable surface:
   - `open_deposit_account`
   - `transition_deposit_account`
   - `query_account_detail`
   - lifecycle-aware workbench query metadata
4. Update package docs to reflect the implemented slice and record validation evidence.

## Validation Plan

- Run package-local pytest for existing and new tests
- Run Python compile validation on the package directory
- Run a targeted runtime smoke command that exercises open, approve, activate, close, reopen, and detail query flows
- Review the changed files for contract drift, nondeterministic evidence, and boundary violations before finalizing docs

## Out of Scope

- statement-cycle execution
- balance decomposition and replay
- hold waterfall logic
- overdraft engine
- shared customer projections
- cross-PBC reads or shared tables
