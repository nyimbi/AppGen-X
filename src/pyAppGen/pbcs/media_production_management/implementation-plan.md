# Media Production Management Implementation Plan

## Boundary

This PBC is a standalone media production operating system for one composed application or a larger AppGen-X composition. It owns production, budget, engagement, location, shoot-day, post, rights, delivery, policy, runtime, extension, control, model, outbox, inbox, and dead-letter tables under the `media_production_management_` prefix. Cross-PBC integration is through AppGen-X APIs, events, projections, and agent skills only.

## Executable Capability Slices

1. Development slate and greenlight: script package, creative deck, attachments, financing state, lifecycle state, and greenlight controls.
2. Budget top sheet and revisions: locked baselines, forecast variance, contingency draw, change reasons, and approver gates.
3. Engagement packets: principal cast, background, crew, vendor packets, rate cards, deal memo evidence, work guarantees, and availability windows.
4. Locations and permits: jurisdiction, curfew, permit evidence, insurance, restrictions, and contingency locations.
5. Stripboard, readiness, and call sheets: scene blocks, cast/crew confirmations, equipment, transport, weather, safety plans, nearest hospital, contacts, and supersede versioning.
6. Daily production control: daily report, first call, first shot, meals, wrap, pages, delays, overtime, incidents, and variance.
7. Dailies and editorial handoff: expected versus received cards, checksum, sync, continuity notes, missing media exceptions, and editorial-ready status.
8. Post/VFX/finishing: milestone dependencies, VFX turnover completeness, vendors, shot codes, and approval readiness.
9. Rights and deliverables: music/location/archive rights, platform/territory/language matrix, captions, audio layouts, checksums, QC routing, package delivery, and archive readiness.
10. Agent and UI surface: forms, wizards, controls, exception-first workbench, document instruction intake, safe CRUD previews, and composed-agent skill contribution.

## Controls

Blocking controls include greenlight evidence, locked-budget revision approval, shoot-day readiness, high-risk safety planning, dailies completeness, VFX turnover packages, rights clearance, QC ownership, and human-confirmed agent mutation previews.

## Verification

The standalone smoke test runs a full negative-and-positive rehearsal from development through delivery. Tests assert blocked edge cases, executable UI forms/wizards/controls, agent preview safety, AppGen-X event contract use, side-effect-free plans, and boundary metadata.
