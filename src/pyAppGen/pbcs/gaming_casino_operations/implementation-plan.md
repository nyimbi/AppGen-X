# Gaming Casino Operations Standalone Plan

## Scope

Package-local uplift only. No shared generator files, ledgers, or sibling PBCs are modified.

## Backlog themes implemented

The standalone slice targets the highest-value items from `improve1.md`:

1. patron identity confidence, duplicate review, and restriction semantics
2. table shift ownership, bankroll reconciliation, and inventory movement evidence
3. slot configuration governance, conversion approval, and fault recovery
4. unified wager-session context and player-rating evidence
5. payout approval, suspicious-activity flagging, and cage-ready hand-pay flow
6. responsible-gaming intervention and compliance/surveillance case handling
7. jurisdiction rule registry, runtime parameters, and governed agent workflows
8. dead-letter visibility and floor-supervisor workbench coverage

## File plan

- deepen `models.py`, `runtime.py`, `services.py`, `routes.py`, `ui.py`, `agent.py`, `events.py`, `handlers.py`, `config.py`, `permissions.py`, `seed_data.py`, `release_evidence.py`, and `__init__.py`
- add `standalone.py` plus focused `tests/test_standalone.py`
- align `migrations/001_initial.sql` and docs with the executable package surface

## Validation plan

- `python3 -m py_compile` on modified package modules
- `pytest -q src/pyAppGen/pbcs/gaming_casino_operations/tests`
- targeted `pbc_source_artifact_contract`, `pbc_implementation_release_audit`, and `pbc_generation_smoke_audit`
- git diff review limited to `src/pyAppGen/pbcs/gaming_casino_operations`
