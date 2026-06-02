# Library and Archives Management Implementation Plan

## Goal

Deliver a package-local AppGen-X standalone slice for `library_archives_management` with executable forms, guided workflows, controls, tests, and release evidence while staying inside the PBC directory.

## Selected Backlog Themes

- accession register and acquisition intake with provenance and donor restrictions
- cataloging templates, authority control, and hierarchical finding aids
- circulation, hold queues, and reading-room request management
- preservation, conservation, digitization triage, and rights review
- deaccession governance, stewardship audits, and assistant CRUD preview guardrails
- standalone workbench composition and release evidence alignment

## Execution Steps

1. Add package-local `forms.py`, `wizards.py`, `controls.py`, and `standalone.py` so the PBC exposes executable operator surfaces without shared-generator edits.
2. Update `__init__.py`, `manifest.py`, `ui.py`, and `release_evidence.py` so the new standalone surfaces are discoverable in package metadata and release evidence.
3. Add focused standalone tests that prove domain coverage, wizard readiness, control guardrails, and end-to-end standalone execution.
4. Record verification evidence and residual risks in `implementation-status.md`.
