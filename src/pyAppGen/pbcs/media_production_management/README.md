# Media Production Management PBC

`media_production_management` is a standalone AppGen-X Packaged Business Capability for development-to-delivery media production operations.

## What It Implements

The package covers development slate management, greenlight evidence, script and creative package tracking, budget top sheets and revisions, cast/crew/vendor engagement packets, location packages, shoot-day readiness, call sheets, daily production reports, dailies ingest, editorial handoff, post/VFX/finishing dependencies, rights clearances, QC handling, platform deliverables, archive evidence, operational controls, and AI-assisted document-to-CRUD previews.

## Files

- `standalone.py` - executable one-PBC app and smoke rehearsal.
- `forms.py` - role-specific forms for development, budget, engagement, locations, shoot days, DPR, post/VFX, and deliverables.
- `wizards.py` - guided development, scheduling, daily wrap, dailies, post, delivery, and document-instruction workflows.
- `controls.py` - blocking and warning controls for greenlight, budget, safety, dailies, VFX, rights, QC, and agent mutations.
- `tests/test_standalone.py` - focused executable coverage.

## Composition Contract

The PBC uses only PostgreSQL/MySQL/MariaDB datastore backends, emits and consumes through the AppGen-X event contract, hides stream-engine pickers, exposes a single-agent skill namespace, and rejects foreign table CRUD plans.
