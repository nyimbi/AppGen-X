# price_promotion_engine Implementation Status

## Improve1 Slice

- Status: executable improve1 price promotion controls implemented for all 50 backlog features.
- Code artifact/model: `pricing_control.py` maps every feature to price-promotion-owned control tables, required fields, and proof fields.
- UI surface: `ui.py` exposes 50 pricing control panels, service actions, and agent tools while preserving standalone forms, wizards, controls, and repository surfaces.
- Service/API: `runtime.py` exposes `evaluate_pricing_control` and `improve1_pricing_control_contract`; each feature has a `POST /price-promotion-engine/improve1/<slug>` service route contract.
- Release evidence: `release_evidence.py` and runtime release evidence include the improve1 pricing control contract.
- Tests: `tests/test_domain_behavior.py` verifies all 50 controls, price book/quote/margin/promotion/coupon gates, AppGen-X eventing, database allowlist, owned-table boundaries, projection-only dependencies, and side-effect-free sample payloads.

## Constraints

- Datastore backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and the package topic.
- Cross-PBC dependencies are represented as declared APIs, events, or projections, not shared table access.
- Agent-assisted price, promotion, coupon, settlement, and quote operations remain preview-first and require human confirmation before mutation.
