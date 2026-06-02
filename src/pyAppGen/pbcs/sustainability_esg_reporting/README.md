# Sustainability ESG Reporting PBC

`sustainability_esg_reporting` is a standalone AppGen-X packaged business capability for ESG and sustainability reporting. It can operate as a one-PBC application for teams that need governed metric definitions, materiality, facility and activity data capture, emissions calculations, renewable claims, social and governance measures, assurance evidence, disclosure preparation, board reporting, regulator filing, and AI-assisted document/instruction previews.

## Owned Domain

The PBC owns sustainability reporting records under the `sustainability_esg_reporting_` prefix, including ESG metrics, materiality assessments, framework mappings, facilities, activity records, emissions factors and calculations, scope boundaries, renewable instruments, water/waste/social/governance records, supplier ESG inputs, assurance controls and evidence, exceptions, restatements, targets and progress, climate scenarios, disclosure packets, board packs, filings, governed documents, governed instructions, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X event tables.

## Standalone Application Surface

The slice app supports a full ESG reporting workflow: define metrics, assess materiality, register facilities, capture activity data, apply factors, calculate Scope 1 and Scope 2 emissions, track targets, attach assurance evidence, build disclosure packets, prepare board packs, submit filings, simulate climate scenarios, and render workbench summaries.

## UI and Agent

The workbench exposes forms, wizards, and controls for metrics, facility/activity capture, emissions, renewable claims, assurance, restatements, disclosure packets, board packs, regulator filings, and governed AI previews. The agent contributes `sustainability_esg_reporting_skills` to the composed assistant, can draft owned-table CRUD previews, and refuses foreign-table writes.

## Verification

See `implementation-status.md` for compile, pytest, diff-check, and focused audit evidence.
