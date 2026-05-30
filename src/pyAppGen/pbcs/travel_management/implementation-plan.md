# Travel Management Implementation Plan

## Source Reviewed

- `improve1.md` travel management backlog.
- Existing manifest, domain-depth contract, runtime, services, routes, UI, agent, release evidence, and PBC-local tests.

## Implementation Intent

Make `travel_management` usable as a one-PBC application for travel operations. The app must cover request readiness, traveler profile completeness, policy versioning, approval routing, booking intent lifecycle, air/hotel/ground booking controls, itinerary integrity, duty-of-care, disruption response, unused-ticket recovery, expense handoff, carbon comparison, and governed AI assistance while keeping employee, expense, supplier, booking-provider, payment, and risk-feed data behind declared API/event boundaries.

## Delivery Steps

1. Preserve AppGen-X eventing and PostgreSQL/MySQL/MariaDB backend policy.
2. Add PBC-local forms, wizards, controls, standalone app methods, and focused tests.
3. Wire standalone smoke evidence into package and release contracts.
4. Run compile, PBC-local tests, diff check, and focused source/package/spec/agent/implementation/capability/generation audits.
