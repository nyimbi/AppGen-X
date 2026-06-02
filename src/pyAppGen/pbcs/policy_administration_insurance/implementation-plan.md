# Implementation Plan - Policy Administration Insurance

## Goal

Deepen `src/pyAppGen/pbcs/policy_administration_insurance` into a stronger standalone one-PBC package without modifying shared AppGen-X generator infrastructure or any other PBC.

## Plan

1. Add package-local standalone composition.
   Create `standalone.py` as a local harness over the existing runtime contract, with deterministic defaults, lifecycle execution helpers, document planning, workbench rendering, and smoke evidence.

2. Enrich UI metadata.
   Replace the minimal fragment-only UI contract with explicit forms, wizards, controls, and a standalone workbench blueprint tailored to insurance policy issuance, endorsement, renewal, cancellation, billing, and document workflows.

3. Enrich agent planning.
   Extend the agent surface with a standalone workspace contract plus document and CRUD planning outputs that point to package-local forms, wizards, controls, and service methods.

4. Extend release and manifest evidence.
   Update package-local release evidence, manifest docs/tests coverage, and exports so standalone readiness is discoverable through existing package entrypoints.

5. Lock behavior with focused tests.
   Add package-local standalone tests covering bootstrap, lifecycle execution, document planning, rendered workbench output, release evidence, and documentation presence.
