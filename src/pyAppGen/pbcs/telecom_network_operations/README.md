# Telecom Network Operations PBC

`telecom_network_operations` is the AppGen-X Packaged Business Capability for telecom NOC and service assurance operations. It owns operational network records for sites, radio cells, capacity segments, incidents, alarms, assurance cases, planned maintenance, and SLA impact while integrating with neighboring OSS, field, customer, and notification systems through APIs, projections, and AppGen-X events rather than shared tables.

## What This PBC Does

The package supports a standalone NOC application surface:

- Canonical site hierarchy with geospatial identity, power/access context, and parent-child topology.
- Radio cell and sector identity for 2G/3G/4G/5G operations.
- Circuit, service-path, fiber route, protection, and route-diversity modeling.
- Alarm normalization, probable-cause capture, root-cause correlation, and suppression evidence.
- Outage lifecycle and major-incident war-room records with impacted services and restoration ETA.
- Service assurance cases with dispatch state and customer-impact context.
- Planned work and maintenance windows with MOP, rollback, freeze-window, and scope controls.
- SLA clock calculation, exclusion governance, breach forecasting, and audit evidence.
- Capacity and KPI snapshots for radio, transport, fiber, aggregation, and service edge capacity.
- Field restoration evidence without owning external workforce, warehouse, or procurement masters.
- Governed AI assistant previews for alarm triage, outage drafting, ticket summaries, planned-work review, and customer update drafting.

## Boundaries

The PBC owns only telecom operational state required by NOC and assurance workflows. External NMS/PM feeds, workforce dispatch, customer notification, finance, vendor master, and procurement systems remain external owners. This package records references, event facts, evidence, and operational decisions; it does not mutate foreign tables.

Ordinary datastore backend exposure is limited to PostgreSQL, MySQL, and MariaDB. Eventing uses the AppGen-X event contract and does not expose stream-engine picker choices to users.

## User Experience

The workbench is organized around alarm triage, outage control, planned work, capacity risk, SLA risk, field evidence, and assistant previews. Forms and wizards surface site-to-service topology, alarm-to-outage workflows, maintenance risk reviews, SLA impact reviews, capacity degradation investigations, field restoration packets, and assistant alarm triage.

## Developer Entry Points

- `implementation-plan.md` explains the implementation approach.
- `standalone.py` contains the executable one-PBC application contract.
- `forms.py`, `wizards.py`, and `controls.py` expose UI and domain guardrails.
- `tests/test_standalone.py` proves the standalone workflows.
- `implementation-status.md` records code review and verification evidence.
