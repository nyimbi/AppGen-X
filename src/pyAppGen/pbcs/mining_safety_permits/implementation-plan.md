# Mining Safety and Permits Implementation Plan

This PBC is a standalone permit-to-work and mine safety control center. It owns mine permits, shift rosters, blast plans, safety inspections, incident reports, regulatory submissions, control actions, policy/rule/runtime tables, and AppGen-X outbox/inbox/dead-letter tables.

Executable scope covers permit classing, lifecycle approval, isolation and lockout, confined-space gas testing, ventilation dependency checks, ground control, blasting clearance and re-entry, competency/fatigue controls, shift handover, incident precursor capture, high-potential escalation, regulatory evidence packs, UI forms/wizards/controls, and safety-aware assistant previews/refusals.

All integrations are through AppGen-X events and PBC APIs. No shared tables or stream-engine picker are exposed.
