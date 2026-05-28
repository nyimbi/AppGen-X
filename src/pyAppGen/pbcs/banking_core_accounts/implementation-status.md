# Banking Core Accounts Implementation Status

## Outcome

Implemented an executable deposit-account lifecycle slice that makes `banking_core_accounts` usable as a one-PBC app for this domain slice. The package now exposes database-backed lifecycle fields, executable lifecycle commands and queries, package-local forms, wizards, controls, workbench views, assistant help, and lifecycle-focused tests.

## Code-Review Findings Resolved

1. Nondeterministic evidence hashes were still using Python `hash()` in package code. Fixed by switching agent/document and rule/event hashing to SHA-256.
2. Schema contract migration metadata pointed to non-existent generated migration paths. Fixed by binding the schema contract to the real package migration file: `migrations/001_initial.sql`.
3. `seed_data.py` referenced an undefined symbol and did not describe the lifecycle slice. Fixed by replacing it with package-local lifecycle seed data for `banking_core_accounts_deposit_account`.

## Validation Evidence

### Passed

Command:

```bash
/Volumes/Media/src/pjs/appgen/.venv/bin/python -m compileall /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts
```

Result:

- Exit code `0`
- Compiled updated package modules successfully

Command:

```bash
/Volumes/Media/src/pjs/appgen/.venv/bin/python -m pytest /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts/tests -q
```

Result:

- Exit code `0`
- `11 passed in 0.36s`

Command:

```bash
PYTHONPATH=/Volumes/Media/src/pjs/appgen/src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c "from pyAppGen.pbcs.banking_core_accounts.runtime import banking_core_accounts_runtime_smoke; smoke=banking_core_accounts_runtime_smoke(); print(smoke['ok']); print(smoke['reopened']['account']['lifecycle_state']); print(smoke['workbench']['summary']['total_accounts']); print(len(smoke['app_surface']['forms']), len(smoke['app_surface']['wizards']), len(smoke['app_surface']['controls']))"
```

Result:

- Exit code `0`
- `True`
- `reopened`
- `1`
- `3 2 5`

### Residual Gap

Command:

```bash
/bin/zsh -lc '/Volumes/Media/src/pjs/appgen/.venv/bin/mypy /Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/banking_core_accounts 2>&1 | tail -n 5'
```

Result:

- Exit code `0` for the shell wrapper
- mypy summary: `Found 279 errors in 17 files (checked 22 source files)`
- Interpretation: the package still has broad pre-existing typing debt outside this implementation slice. The lifecycle slice compiles and tests cleanly, but strict mypy is not yet green for the full PBC.

## Changed Files

- `agent.py`
- `capability_assurance.py`
- `config.py`
- `events.py`
- `implementation-plan.md`
- `lifecycle.py`
- `manifest.py`
- `migrations/001_initial.sql`
- `models.py`
- `README.md`
- `RELEASE_EVIDENCE.md`
- `release_evidence.py`
- `routes.py`
- `runtime.py`
- `seed_data.py`
- `services.py`
- `SPECIFICATION.md`
- `tests/test_contract.py`
- `tests/test_lifecycle_app.py`
- `ui.py`

## Remaining Risks

- Strict package-level typing remains red and will need a separate cleanup pass.
- The current slice focuses on deposit-account lifecycle and one-PBC usability. Balance decomposition, hold waterfalls, overdraft rules, and statement operations remain backlog items from `improve1.md`.
