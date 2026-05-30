# Sports Venue Event Operations PBC

## Purpose

`sports_venue_event_operations` is a standalone sports venue command package for venue/zone/seat configuration, event calendar control, ingress/egress, staffing, concessions, ticketing coordination, credentialing, security, crowd management, incidents, weather delays, broadcast/production readiness, sponsor activations, cleaning/turnover, accessibility, lost/found, emergency operations, and revenue/attendance analytics.

## Operating Constraints

- Eventing standard: AppGen-X only.
- Stream engine picker: forbidden and hidden.
- Database backends: PostgreSQL, MySQL, and MariaDB.
- Boundary: the package writes only `sports_venue_event_operations_*` tables and package-local AppGen-X event tables.

## Owned Tables

- `sports_venue_event_operations_venue`
- `sports_venue_event_operations_venue_zone`
- `sports_venue_event_operations_seat_inventory`
- `sports_venue_event_operations_event_calendar`
- `sports_venue_event_operations_ingress_plan`
- `sports_venue_event_operations_egress_plan`
- `sports_venue_event_operations_staffing_plan`
- `sports_venue_event_operations_concession_plan`
- `sports_venue_event_operations_ticketing_coordination`
- `sports_venue_event_operations_credential`
- `sports_venue_event_operations_security_plan`
- `sports_venue_event_operations_crowd_observation`
- `sports_venue_event_operations_incident`
- `sports_venue_event_operations_weather_delay`
- `sports_venue_event_operations_production_readiness`
- `sports_venue_event_operations_sponsor_activation`
- `sports_venue_event_operations_cleaning_turnover`
- `sports_venue_event_operations_accessibility_case`
- `sports_venue_event_operations_lost_found_item`
- `sports_venue_event_operations_emergency_operation`
- `sports_venue_event_operations_revenue_attendance_snapshot`
- governance tables for policy rules, runtime parameters, schema extensions, control assertions, and governed models
- AppGen-X outbox, inbox, and dead-letter tables

## Standalone Workflow Surface

Service methods in the standalone app cover:
- venue and seat layout creation
- event calendar scheduling and turnover planning
- ingress/egress coordination
- staffing, concessions, ticketing, and credential issuance
- security posture and crowd snapshot handling
- incident logging and emergency command activation
- weather delays and restart readiness
- broadcast/production readiness and sponsor activations
- accessibility requests and lost/found logging
- revenue and attendance capture
- governed AI document intake and CRUD previews

## UI Surface

The package provides forms, wizards, and controls for operator workflows.

Forms include venue layout, event calendar, ingress/egress, security and crowd, and revenue/attendance planning.

Wizards include event command setup, weather delay response, incident command, accessibility assistance, and broadcast/production readiness.

Controls include gate opening, weather hold approval, emergency activation, and seat kill approval.

## Workbench

The workbench summarizes:
- event count, incidents, delays, staffing gaps, attendance, and gross revenue
- event calendar board
- gate and queue monitor
- staffing and credential status
- security and incident board
- weather and emergency board
- broadcast, sponsor, and turnover board

## Agent and Governance

The agent surface contributes a single sports venue event operations assistant namespace with document intake, workbench navigation, governed datastore CRUD previews, and policy explanation. Mutation previews always require human confirmation and remain within owned tables.

## Release Evidence

Package readiness is proven through runtime smoke, standalone smoke, UI and agent contract checks, owned-boundary validation, documentation presence, and source/package/spec/agent/implementation/capability/generation audits.
