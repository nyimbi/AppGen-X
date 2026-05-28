# Checkout Processing Implementation Plan

## Goal

Turn `checkout_processing` into a coherent one-PBC checkout app surface that remains fully package-local. The runtime already covers cart, session, handoff, risk, payment, completion, and AppGen-X event behavior. This slice focuses on making that runtime consumable through domain-specific app surfaces and release evidence.

## Scope

- Keep all edits under `src/pyAppGen/pbcs/checkout_processing`.
- Preserve the owned-table boundary and AppGen-X event contract.
- Improve domain coherence instead of broadening scope into central generator or other PBCs.

## Work Items

1. Align package contracts with the checkout runtime
   - Tighten RBAC, configuration, rules, and parameters around actual checkout concerns.
   - Remove generic contract drift where package-local modules disagree with `runtime.py`.

2. Add one-PBC app surfaces
   - Add package-local `forms.py`, `wizards.py`, and `controls.py`.
   - Expose those surfaces through services, routes, and workbench UI metadata.

3. Improve agent and chatbot support
   - Make document/instruction intake domain-specific for checkout operations.
   - Return governed CRUD previews that stay inside owned checkout tables and named permissions.

4. Strengthen release evidence
   - Ensure release evidence covers forms, wizards, controls, assistant preview, and workbench bindings.
   - Refresh package-local README and implementation status.

5. Add focused tests
   - Cover forms/wizards/controls catalogs and validation.
   - Cover assistant document/instruction CRUD preview.
   - Cover route and service visibility for the new one-PBC app surfaces.

## Non-Goals

- No edits to AppGen-X central generator, DSL, or shared framework.
- No cross-PBC schema, docs, or runtime changes.
- No new third-party dependencies.

## Verification Plan

- Run package-local `pytest` for `src/pyAppGen/pbcs/checkout_processing/tests`.
- Run Python compilation checks on modified modules.
- Use existing runtime smoke plus focused new tests as the primary evidence.
