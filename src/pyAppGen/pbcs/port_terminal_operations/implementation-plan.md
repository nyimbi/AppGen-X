# Implementation Plan

## Goal

Deliver a standalone, package-local Port Terminal Operations application slice without touching shared generators, language assets, or global ledgers.

## Plan

1. Reuse the existing runtime, domain-depth, event, and package metadata contracts as the source of truth.
2. Add package-local `forms`, `wizards`, and `controls` modules to define the standalone UI surface.
3. Hand-craft `standalone.py` with an in-memory application shell, route contracts, document-intake support, and standalone smoke coverage.
4. Wire the new standalone surface into `ui.py`, `agent.py`, `release_evidence.py`, `manifest.py`, and package exports.
5. Add focused standalone tests and package-local documentation, then validate with compile and pytest.
