# Travel Management PBC

`travel_management` is a standalone AppGen-X packaged business capability for corporate travel operations. It owns trip requests, traveler profiles, travel policies, approval routing, booking intents, air/hotel/ground bookings, itinerary timelines, duty-of-care alerts, disruptions, unused ticket recovery, expense handoffs, supplier offers, carbon records, and governed assistant previews.

## Owned Domain

The PBC owns travel operational records and AppGen-X event artifacts. Employee identity, expense reports, payments, suppliers, agency feeds, risk feeds, and booking providers remain external projections or APIs. The package does not share foreign tables and does not expose stream-engine choices to users.

## Standalone Application Surface

`TravelManagementStandaloneApp` provides executable methods for traveler profile readiness, policy versioning, trip readiness gates, approval graph routing, booking intent comparison, air/hotel bookings, semantic itinerary confirmation, duty-of-care response, disruption counterfactuals, unused ticket recovery, carbon comparison, trip completion, expense handoff, and confirmation-gated assistant CRUD previews.

## UI, Wizards, and Controls

The forms and wizards surface trip readiness, policy coaching, approval routing, booking selection, itinerary ingestion, duty-of-care, disruption rebooking, unused-ticket recovery, expense handoff, and assistant mutation preview workflows. Controls fail closed for missing trip evidence, incomplete traveler profiles, high-risk destination mitigation, unconfirmed itinerary ingestion, untriaged disruptions, unused-ticket owner gaps, premature expense handoffs, carbon assumptions, and assistant mutations.

## Verification

See `implementation-status.md` for compile, pytest, diff-check, and focused PBC audit evidence.
