# Permitting Licensing and Inspections Implementation Plan

## Goal

Converge the package from generated scaffolding to a believable standalone
one-PBC AppGen-X slice without touching shared generator or language assets.

## Plan

- Replace generic runtime placeholders with package-local permitting workflow
  state, contracts, and workbench metadata.
- Add standalone usability surfaces: forms, wizards, controls, UI shell, and
  stateful standalone bootstrap orchestration.
- Update agent, manifest, release evidence, and package exports so the new
  surfaces are package-discoverable.
- Add focused tests and docs proving bootstrap, routing, rendering, and release
  readiness inside this package only.

## Non-Goals

- No edits to shared generators, language assets, or the repo progress ledger.
- No new external dependencies.
- No attempt to turn the package into a live server-backed application in this
  scope.
