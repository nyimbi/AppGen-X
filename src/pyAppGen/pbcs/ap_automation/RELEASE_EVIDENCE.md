# Accounts Payable Automation Release Evidence

Directory: `pbcs/ap_automation`

## Standalone surfaces covered

- Runtime workflows in `runtime.py`
- Repository bindings in `repository.py`
- Database-backed forms in `forms.py`
- Guided AP wizards in `wizards.py`
- Control library in `controls.py`
- UI/workbench wiring in `ui.py`
- Assistant contribution in `agent.py`
- Package release validation in `release_evidence.py`

## Release checks

- owned schema depth and migration coverage
- service command depth
- AppGen-X event contract lock
- permissions covering command execution
- backend allowlist
- no shared-table access
- execution service bound
- UI contract bound
- agent contribution bound
- repository bound
- forms bound
- wizards bound
- controls bound
