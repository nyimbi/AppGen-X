# Case and Knowledge Management

This package is an executable AppGen-X PBC slice for support operations and knowledge management. It models the operational path from support-case intake through classification, queue routing, assignment, SLA monitoring, interactions, escalation, resolution, knowledge authoring, article quality, freshness, and grounded agent recommendations.

## What It Includes

- Owned model/schema metadata for support, knowledge, governance, and AppGen-X event tables.
- `application.py` with a package-local runtime that can execute the domain workflow without touching shared generator code.
- Service, route, event, handler, UI, RBAC, configuration, rule, parameter, and agent surfaces built on the same runtime.
- Governed document-instruction and CRUD planning that rejects foreign-table mutations.
- Release evidence and focused tests for a realistic one-PBC app slice.

## Main Domain Slice

The slice supports these primary commands:

- `create_support_case`
- `classify_case`
- `route_case_queue`
- `assign_case`
- `start_sla_timer`
- `record_case_interaction`
- `open_case_escalation`
- `resolve_case`
- `publish_knowledge_article`
- `approve_knowledge_article`
- `version_article`
- `capture_article_feedback`
- `score_article_quality`
- `identify_root_cause`
- `link_duplicate_case`
- `resolve_case_exception`
- `record_case_deflection`
- `recommend_next_best_resolution`

## Package-Local Execution

The fastest way to use the slice in tests or local code is through `create_app()`:

```python
from pyAppGen.pbcs.case_knowledge_management.application import create_app

app = create_app()
created = app.create_support_case(
    {
        "tenant": "tenant-acme",
        "title": "API requests fail after token rotation",
        "summary": "Customers receive repeated 500 responses from the public API.",
        "severity": "high",
        "product_area": "platform",
        "customer_ref": "acme-01",
    }
)
case_id = created["record"]["id"]
app.classify_case({"case_id": case_id})
app.route_case_queue({"case_id": case_id})
app.assign_case({"case_id": case_id})
app.start_sla_timer({"case_id": case_id})
app.recommend_next_best_resolution({"case_id": case_id})
```

## Boundaries

- All mutable data lives under `case_knowledge_management_*`.
- Cross-PBC integration is represented only through AppGen-X events and API-style contracts.
- Agent CRUD planning requires confirmation for mutations and rejects foreign tables.

## Verification

Focused tests for this slice live in `tests/test_contract.py` and `tests/test_app_slice.py`.
