# Release Evidence - Hospitality Property Operations

Package directory: `pbcs/hospitality_property_operations`.

This package contains owned schema metadata, aligned migration DDL, source-package runtime contracts, and a package-local standalone hotel operations slice with sqlite-backed execution.

## Evidence Summary

- Source artifacts: schema, service, API, event, handler, governance, UI, agent, and package metadata surfaces are materialized.
- Owned datastore boundary: every owned table starts with `hospitality_property_operations_` and foreign-table mutation is rejected.
- Standalone app: room readiness, reservation, check-in, guest request recovery, occupancy, and workbench flows execute locally through the package route surface.
- Documentation: `README.md`, `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`, and `implementation-status.md` exist inside this package.

## Recommended Verification

```python
from pyAppGen.pbcs.hospitality_property_operations.release_evidence import build_release_evidence

result = build_release_evidence()
print(result["ok"])
print([check for check in result["checks"] if not check["ok"]])
```
