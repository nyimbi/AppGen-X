# federated_iam

`federated_iam` is the AppGen-X packaged bounded context for federated identity and access management. The package can run as a standalone one-PBC app using only package-local runtime, services, routes, UI metadata, seeds, event handlers, permissions, agent planning, and release evidence.

The standalone surface is anchored by:
- `standalone.py` for one-PBC composition and bootstrap
- `runtime.py` for owned-domain execution and release-grade capability proofs
- `services.py` and `routes.py` for executable service and route wrappers
- `ui.py` for workbench, forms, wizards, and controls
- `seed_data.py` for deterministic bootstrap state and install steps
- `release_evidence.py` for package-local release gates

## Standalone Scope

The package owns tenant registry, principal registry, provider registration, federated identity links, credential verification, role assignment, policy decisions, token grants, sessions, privileged access, rules, parameters, configuration, AppGen-X outbox/inbox/dead-letter evidence, and the PBC workbench.

## Bootstrap

Use `create_standalone_app()` to compose the PBC into a deterministic one-package app bundle. It seeds a tenant, principals, identity provider, linked identity, credential verification, role assignment, policy decision, token grant, privileged access request, and one consumed event projection.

## Verification

Focused verification for this package is designed to work with plain `python3` by calling the package smoke tests directly when `pytest` is unavailable in the environment.
