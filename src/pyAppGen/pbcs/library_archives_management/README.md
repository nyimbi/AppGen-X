# Library and Archives Management Standalone Slice

This package-local AppGen-X standalone slice turns `library_archives_management` into an executable one-PBC workbench without leaving the owned package boundary.

## Scope

The standalone surface covers:

- accessioning and acquisitions with source-of-custody detail
- cataloging, authority control, and hierarchical finding aids
- circulation, holds, and supervised reading-room access
- preservation, conservation, digitization, and rights gating
- provenance, deaccession governance, audits, and assistant CRUD previews

## Modules

- `forms.py` defines domain-deep operator intake forms with example payloads and validation
- `wizards.py` groups forms into archival and library workflows
- `controls.py` executes guardrails for release, owned-boundary, assistant preview, and stewardship checks
- `standalone.py` composes the package-local app contract and domain walkthrough smoke flow
- `tests/test_standalone.py` verifies domain coverage, owned-boundary previews, and standalone execution

## Execution

Typical verification commands, using any environment that already has `pytest` available and the package rooted at `src/`:

```bash
PYTHONPATH=src python -m pytest src/pyAppGen/pbcs/library_archives_management/tests/test_standalone.py -q
PYTHONPATH=src python -m pytest src/pyAppGen/pbcs/library_archives_management/tests -q
python -m compileall src/pyAppGen/pbcs/library_archives_management
```

## Boundary

All behavior remains inside `src/pyAppGen/pbcs/library_archives_management`. No shared generator, language, or progress-ledger files are touched by this slice.
