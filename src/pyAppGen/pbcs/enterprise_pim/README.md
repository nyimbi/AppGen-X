# Enterprise PIM Standalone Package

`enterprise_pim` is a package-local AppGen-X PBC for enterprise product-information governance. It owns taxonomy, attribute, localization, validation, dependency, publication-readiness, stewardship, exception, and release-evidence concerns inside `src/pyAppGen/pbcs/enterprise_pim`.

## Standalone App Surface

The package now includes `standalone.py`, which exposes an in-memory one-PBC application harness:

- `EnterprisePimStandaloneApp`
- `create_standalone_app()`
- deterministic bootstrap using package-local configuration, rules, parameters, dependency schemas, and seed steps
- route dispatch over the declared PBC route surface
- UI descriptors for forms, wizards, controls, and workbench views
- agent/chatbot/document/CRUD planning hooks
- release-evidence and seed-bundle inspection

## Bootstrap Flow

The standalone bootstrap configures:

- supported database backend and AppGen-X topic
- default locales and channels
- completeness, translation-quality, SLA, inheritance-depth, retry, and anomaly parameters
- readiness rules and required approvers
- accepted dependency schemas
- a demo lifecycle covering taxonomy creation, attribute governance, localization, workflow approval, dependency event intake, and publication readiness

## Key Modules

- `runtime.py`: owned-domain behavior and in-memory state transitions
- `standalone.py`: one-PBC executable harness
- `seed_data.py`: runtime bootstrap bundle and deterministic seed rows
- `permissions.py`: runtime-aligned permission contract
- `release_evidence.py`: package-local release evidence derived from actual artifacts
- `agent.py`: chatbot, document, and CRUD planning surface
- `tests/test_standalone.py`: focused standalone verification

## Verification

Preferred local checks:

```bash
python3 -m compileall src/pyAppGen/pbcs/enterprise_pim
python3 -m unittest discover -s src/pyAppGen/pbcs/enterprise_pim/tests -p 'test_standalone.py'
```
