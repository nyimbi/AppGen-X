# Utilities Metering and Billing Implementation Plan

## Source Reviewed

- `improve1.md` utility metering and billing backlog.
- Existing manifest, runtime, services, routes, UI, agent, release evidence, migrations, and package-local tests.
- Worker-created `slice_app.py` executable surface, preserved as the primary operating engine.

## Implementation Intent

Make `utilities_metering_billing` usable as a one-PBC utility billing app with service point identity, meter assets, meter exchanges, read provenance, validation ladders, interval gaps, estimates, tariffs, billing cycles, bill simulation, adjustments, payment-boundary evidence, disputes, exception queues, regulatory reporting, UI controls, and confirmation-gated AI assistance.

## Delivery Steps

1. Keep ordinary PBC eventing on the AppGen-X contract and backend policy limited to PostgreSQL, MySQL, and MariaDB.
2. Preserve the PBC-local `slice_app.py` implementation and expose it via standalone/forms/wizards/controls wrappers.
3. Wire standalone smoke evidence into package and release contracts.
4. Add focused tests proving the one-PBC app, UI/control coverage, negative paths, governed CRUD, and smoke behavior.
5. Run compile, PBC tests, diff check, and focused source/package/spec/agent/implementation/capability/generation audits.
