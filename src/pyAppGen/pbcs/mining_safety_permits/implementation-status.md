# Mining Safety and Permits Implementation Status

Implemented in this branch:

- `standalone.py` with a full in-memory mine permit control center.
- `forms.py`, `wizards.py`, and `controls.py` for field forms, guided workflows, and blocking controls.
- UI, release evidence, manifest, and package exports wired to the standalone surface.
- Focused tests for permit lifecycle, isolations, gas testing, ground control, blasting, incidents, regulatory packs, and assistant safety refusal.

Known gaps: browser rendering and live database execution are not run in this PBC-only branch; generated app bindings provide those integrations.
