# Implementation Plan

## Goal

Turn `federated_iam` into a coherent standalone one-PBC app surface without touching files outside this package.

## Planned Changes

1. Replace thin generated wrappers with package-local executable wrappers around `runtime.py` for permissions, seeds, services, routes, handlers, and release evidence.
2. Add a standalone composition surface that bootstraps a deterministic package-local app bundle with workbench, routes, agent/chatbot metadata, and install steps.
3. Extend UI metadata with forms, wizards, controls, and workflow routes that map to the runtime operations.
4. Fix agent/document/CRUD planning so owned tables and route workflows are correct for logical and runtime tables.
5. Add focused standalone tests and refresh docs/status artifacts to match the implementation.

## Verification Plan

- Compile the package with `python3 -m compileall`
- Run package smoke tests and focused test functions through `python3`
- Review changed files for internal consistency and package-boundary compliance
