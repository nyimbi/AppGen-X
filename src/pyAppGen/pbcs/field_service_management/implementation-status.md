

## 2026-05-30 improve1 Field-Control Execution Slice

- Added `field_control.py` as the executable per-feature control layer for all 50 Field Service Management improve1 capabilities.
- Wired the control contract into runtime capabilities, release evidence, and UI workbench surfaces so generated applications can discover field-service-specific gates.
- Rebuilt `IMPROVE1_TRACEABILITY.md` so each feature maps to code/model, UI surface, service/API, test, and release evidence.
- Added `tests/test_domain_behavior.py` with negative guardrails for request triage, lifecycle transitions, stale asset projections, technician profile completeness, certification expiry, location consent, route hard constraints, reoptimization approval, skill-location-tool scoring, calibration/tool custody, mobile offline merge, task dependencies, safety gates, quote approval, site readiness, finance/fleet boundaries, agent confirmation, cross-PBC mutation boundaries, release evidence packs, and complete role workbench coverage.

