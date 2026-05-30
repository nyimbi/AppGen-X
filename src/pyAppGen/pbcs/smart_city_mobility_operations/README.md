# Smart City Mobility Operations PBC

`smart_city_mobility_operations` is a standalone AppGen-X packaged business capability for municipal mobility command centers. It gives a composed app enough local domain depth to operate corridors, intersections, signals, transit priority, emergency preemption, curb allocation, parking, micromobility, incidents, planned disruptions, street-use permits, sensor feeds, congestion pricing, accessibility detours, public notifications, multimodal reliability, and environmental analytics.

## Owned Domain

The PBC owns city mobility command records, including corridor and intersection registries, signal plans, transit priority rule packs, emergency preemption policies, curb zones, parking assets, micromobility docks, traffic incidents, planned disruptions, permits, sensor feeds, congestion pricing policies, accessibility disruptions, public notifications, trip reliability snapshots, environmental analytics, and governed instruction previews. External transport, identity, billing, and communications systems integrate through declared APIs or AppGen-X events rather than shared tables.

## Standalone Application Surface

The standalone app exposes package-local storage, service operations, route dispatch, workbench rendering, release evidence, and a smoke path that seeds and verifies a representative city mobility day. Operators can register corridors and intersections, review signal plans, configure transit priority, quarantine bad feeds, coordinate closures and incidents, publish accessibility detours and public alerts, analyze reliability and emissions, and prepare confirmation-gated AI previews for operational changes.

## UI and Agent

The UI contract surfaces the mobility workbench, corridor and intersection detail views, command boards, reliability/environment metrics, and assistant panels. The agent can parse documents and instructions such as closure memos or event permits, propose PBC-owned CRUD operations, identify relevant wizards, and require human confirmation before mutation.

## Verification

See `implementation-status.md` for exact compile, pytest, diff-check, and focused audit evidence.
