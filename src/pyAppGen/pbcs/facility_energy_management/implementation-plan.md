# Facility Energy Management Implementation Plan

## Goal

Make `facility_energy_management` a one-PBC AppGen-X application that can operate a realistic facility energy program without companion PBCs.

## Slices

1. Replace generic scaffold evidence with hand-crafted facility energy forms, wizards, controls, and standalone app proof.
2. Model core energy operations: meter hierarchy, interval read quality, tariff calendars, HVAC schedule hierarchy, demand response, baselines, optimization handoffs, and anomaly investigation.
3. Keep mutation paths side-effect-free, package-local, governed by permissions, and backed by AppGen-X outbox/inbox/dead-letter evidence.
4. Surface the assistant as `facility_energy_management_skills` with document/instruction intake and bounded CRUD previews.
5. Prove behavior through package-local tests, compile, release validation, and focused AppGen-X PBC audits.

## Non-Goals

- No shared generator or DSL changes.
- No external building automation device writes.
- No cross-PBC table access.
