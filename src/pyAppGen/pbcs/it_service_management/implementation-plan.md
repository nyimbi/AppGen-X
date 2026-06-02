# IT Service Management Implementation Plan

## Intent

Make `it_service_management` usable as a complete single-PBC application, not only a generated contract. The slice adds executable domain behavior and UI surface evidence while staying inside the PBC directory.

## Plan

1. Add domain forms for major incident, catalog request, access request, change, CAB, RCA, CMDB, SLA, and knowledge workflows.
2. Add guided wizards for major incident command, catalog fulfillment, governed access, change approval, problem-to-known-error, and CMDB impact preview.
3. Add controls that block unsafe incident, request, change, problem, CMDB, and SLA actions until required evidence exists.
4. Implement a standalone ITSM application that configures runtime rules/parameters, opens and correlates incidents, manages milestone SLAs, validates requests, governs access, models CMDB relationships, scores change risk, records PIRs, creates problems, publishes known errors, and previews assistant CRUD actions.
5. Extend UI and release evidence so generated apps surface forms, wizards, controls, standalone app metadata, and assistant contribution.
6. Add tests proving executable happy paths and critical blockers.

## Boundaries

The implementation references only `it_service_management_*` owned tables, uses AppGen-X event contracts, and keeps database backends constrained to PostgreSQL, MySQL, and MariaDB.
