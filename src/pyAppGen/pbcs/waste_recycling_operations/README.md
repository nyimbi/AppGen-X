# Waste and Recycling Operations PBC

`waste_recycling_operations` is a standalone AppGen-X packaged business capability for route-based waste, recycling, organics, bulky, hazardous exception, disposal, and diversion operations. A composed application with only this PBC can release routes, manage bins, define material stream rules, prove pickups, triage missed service, handle contamination, reconcile disposal tickets, calculate recycling yields, and prepare governed assistant CRUD previews.

## Owned Domain

The PBC owns waste route, bin asset, pickup event, material stream, contamination finding, disposal ticket, recycling yield, policy rule, runtime parameter, schema extension, control assertion, governed model, and AppGen-X event tables. Fleet, crew, customer case, billing, enforcement, and facility systems remain external projections or event/API dependencies; this PBC does not mutate foreign tables.

## Standalone Application Surface

`WasteRecyclingOperationsStandaloneApp` provides executable methods for route release, bin registration, material stream setup, pickup proof, missed pickup classification, contamination finding, hazardous exception, disposal ticket reconciliation, recycling yield calculation, assistant preview, and workbench snapshots. Forms, wizards, and controls expose the same capabilities to generated UI/workbench surfaces.

## UI and Agent

The UI includes route release, bin, pickup proof, material stream, contamination, disposal ticket, recycling yield, bulky job, hazardous exception, and governed assistant preview forms. Guided workflows cover route release, missed pickup recovery, contamination education, disposal reconciliation, hazardous material handoff, diversion reporting, and assistant instruction previews. The agent uses `waste_recycling_operations_skills`, validates owned-table CRUD, and requires human confirmation for mutations.

## Verification

See `implementation-status.md` for compile, pytest, diff-check, and focused audit evidence.
