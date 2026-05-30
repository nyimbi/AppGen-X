# Food Safety Quality Compliance Standalone Slice

`food_safety_quality_compliance` is a package-local standalone slice for HACCP version governance, CCP definition, inspection escalation, nonconformance management, supplier audit monitoring, quality holds, recall readiness, governed assistant previews, and release evidence.

## Scope

- Owns only `food_safety_quality_compliance_*` tables plus local AppGen-X inbox/outbox/dead-letter tables.
- Uses declared projections for recall impact analysis and explicitly rejects foreign table references.
- Pins inspections and holds to the effective HACCP plan version in force at execution time.
- Requires citations and human confirmation for assistant-generated mutation previews.

## Primary Entry Points

- Runtime: `food_safety_quality_compliance_runtime_capabilities()`
- Service harness: `FoodSafetyQualityComplianceService`
- Slice app: `slice_app.py`
- UI/workbench: `food_safety_quality_compliance_render_workbench()`
- Release evidence: `build_release_evidence()`

## Focused Behaviors

- HACCP plans cannot be approved until required hazards are mapped to CCPs and approvals are complete.
- Critical or allergen/temperature/foreign-material inspection findings open holds and nonconformances automatically.
- Major nonconformances cannot close without root cause, preventive action, and effectiveness evidence.
- Hold release requires approved disposition, full quantity reconciliation, and the configured approver threshold.
- Mock recall drills are side-effect free and produce evidence packets from genealogy and shipment projections.
