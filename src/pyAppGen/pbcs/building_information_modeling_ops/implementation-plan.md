# Implementation Plan

## Scope

Implement one executable standalone slice from `improve1.md` by combining:

- federation registry and discipline package mapping
- shared coordinates and georeferencing assurance
- model issue-purpose governance
- assistant-backed document-instruction and CRUD planning
- package-local standalone app bootstrap and release evidence

Constraints preserved:

- AppGen-X eventing only
- no stream-engine picker
- no shared table access
- no edits outside `src/pyAppGen/pbcs/building_information_modeling_ops`

## Delivery Plan

1. Keep the package-local federation runtime, models, schema contract, services, routes, UI, events, handlers, permissions, and release evidence aligned around one owned-table BIM slice.
2. Make the standalone surface explicit through `standalone.py` so a one-PBC app can bootstrap configuration, parameters, rules, coordinates, model packages, federation assembly, workbench rendering, assistant planning, and release snapshots.
3. Keep governance deterministic by compiling rules with a stable digest instead of process-local Python hash values.
4. Lock the slice with focused tests for federation behavior, contract coverage, standalone bootstrap, assistant planning, and deterministic rule compilation.
5. Refresh package docs with fresh validation evidence from the isolated branch.

## Validation Commands

- `python3 -m unittest discover -s src/pyAppGen/pbcs/building_information_modeling_ops/tests -t src`
- `python3 -m compileall src/pyAppGen/pbcs/building_information_modeling_ops`
- `python3 -c "import sys; sys.path.insert(0, 'src'); from pyAppGen.pbcs.building_information_modeling_ops.standalone import smoke_test; result = smoke_test(); print({'ok': result['ok'], 'active_federations': result['loaded']['workbench']['workbench']['kpis']['active_federations'], 'doc_plan_ok': result['document_plan']['ok'], 'crud_plan_ok': result['crud_plan']['ok']})"`
- `python3 - <<'PY' ... package-local smoke audit across package, agent, capability, config, events, handlers, permissions, release, routes, runtime, standalone, and UI ... PY`
