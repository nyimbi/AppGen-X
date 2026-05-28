# Construction Project Controls

This package now behaves as a package-local one-PBC construction controls app slice focused on:

- WBS-first project setup and hierarchy rollups
- frozen baseline approval and tracking
- quantity-based progress measurement with evidence gates
- earned-value and forecast rollups
- float-driven schedule risk escalation
- governed assistant previews for document-to-draft workflows

## Package Shape

- Runtime: `runtime.py`
- Services: `services.py`
- Routes: `routes.py`
- UI: `ui.py`
- Forms: `forms.py`
- Wizards: `wizards.py`
- Controls: `controls.py`
- Agent/chatbot support: `agent.py`
- Seed scenarios: `seed_data.py`
- Release evidence: `RELEASE_EVIDENCE.md`

## Primary Flow

1. Create a construction project through `POST /construction-projects`.
2. Freeze an approved baseline through `POST /construction-projects/{project_id}/baseline-revisions`.
3. Add WBS-coded work packages through `POST /work-packages`.
4. Accept site progress through `POST /site-progress` or the compatibility alias `POST /site-progresss`.
5. Escalate float issues through `POST /schedule-risks`.
6. Freeze a reporting period through `POST /reporting-periods/freeze`.
7. Review the workbench through `GET /construction-project-controls-workbench`.

## Domain Notes

- Work packages own WBS code, parent WBS, control account, discipline, area, contractor, measurement method, and EV cost basis.
- Baselines are stored as approved revisions under the construction project record, with one active frozen revision at a time.
- Progress is accepted only when quantity or weighted-step evidence rules pass.
- Schedule float thresholds open exception events instead of silently degrading dashboard state.
- Assistant previews extract draft intent for progress, RFIs, submittals, and change events but always require confirmation before mutation.

See `implementation-plan.md` for the scoped slice and `implementation-status.md` for the implemented outcome and verification evidence.
