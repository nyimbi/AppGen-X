# Workflow Orchestration Release Evidence

Directory: `src/pyAppGen/pbcs/workflow_orchestration`

## Included Evidence

- Runtime release checks from `runtime.py`
- Repository, models, service, route, event, permission, UI, and agent package
  contracts
- Standalone app bootstrap and workbench smoke
- Package artifact presence for:
  - `README.md`
  - `implementation-plan.md`
  - `implementation-status.md`
  - `RELEASE_EVIDENCE.md`
  - `repository.py`
  - `standalone.py`
  - `tests/test_contract.py`
  - `tests/test_standalone.py`

## Repo Gates

- `pbc_source_artifact_contract`
- `pbc_implementation_release_audit`
- `pbc_generation_smoke_audit`

## Validation Commands

```bash
python3 -m py_compile src/pyAppGen/pbcs/workflow_orchestration/*.py \
  src/pyAppGen/pbcs/workflow_orchestration/tests/*.py

PYTHONPATH=src python3 - <<'PY'
from pyAppGen.pbcs.workflow_orchestration.tests import test_contract, test_standalone
for module in (test_contract, test_standalone):
    for name in sorted(dir(module)):
        if name.startswith('test_'):
            getattr(module, name)()
            print(f'passed:{module.__name__}:{name}')
PY

PYTHONPATH=src python3 - <<'PY'
from pyAppGen.pbcs.workflow_orchestration import smoke_test
from pyAppGen.pbcs.workflow_orchestration.runtime import workflow_orchestration_runtime_smoke
from pyAppGen.pbc import pbc_implementation_release_audit
print(smoke_test()['ok'])
print(workflow_orchestration_runtime_smoke()['ok'])
print(pbc_implementation_release_audit(('workflow_orchestration',))['ok'])
PY
```

## Notes

- `tests/test_runtime_capabilities.py` remains present, but direct execution in
  this environment is blocked by missing `pytest`.
- The standalone app stays entirely within the package boundary and does not
  require edits outside `workflow_orchestration`.
