## Scope

Implement one executable improvement slice from `improve1.md` by combining:

- federation registry and discipline package map
- shared coordinates and georeferencing assurance
- model issue purpose governance

The slice will stay package-local and keep these constraints intact:

- AppGen-X eventing only
- no stream-engine picker
- no shared table access
- no edits outside this package directory

## Planned Code Changes

1. Extend the runtime with package-local BIM federation governance functions:
   - project coordinate baseline registration
   - model package registration with discipline, approval, checksum, and spatial metadata
   - coordinate validation against the declared baseline
   - federation assembly that rejects unapproved or incompatible model versions
   - workbench projection for active federations by discipline
   - release evidence generation for approved federation packages

2. Surface the slice through package-local contracts:
   - runtime capability list
   - service operations
   - route and UI/workbench projections
   - event metadata and inbound-event handling traces

3. Add focused tests under `tests/` for:
   - coordinate validation pass/fail cases
   - issue-purpose and approval gating
   - federation assembly and duplicate protection
   - release evidence contents
   - inbound event re-evaluation behavior

## Review Pass

After implementation:

- run the package-local tests
- run a Python compile pass on the package
- review the touched files for contract drift, duplicated logic, and boundary violations
- fix any issues found before writing `README.md` and `implementation-status.md`

## Validation Commands

Planned validation commands:

- `python3 -m pytest src/pyAppGen/pbcs/building_information_modeling_ops/tests`
- `python3 -m compileall src/pyAppGen/pbcs/building_information_modeling_ops`
