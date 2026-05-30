# Research Grants Management Improve1 Implementation Status

- Slice: executable improve1 traceability controls for all 50 Research Grants Management backlog capabilities.
- Scope: package-local files under `src/pyAppGen/pbcs/research_grants_management` only.
- Runtime evidence: `research_grants_management_control.py` maps every backlog feature to owned control tables, required opportunity/proposal/budget/compliance/award/subaward/reporting/effort/closeout fields, UI panels, service/API routes, AppGen-X event contract evidence, declared dependencies, tests, and release evidence.
- Guardrails: PostgreSQL/MySQL/MariaDB only, AppGen-X eventing only, no stream-engine picker, no shared-table access, agent recommendations remain preview/confirmation gated, and pre-award/compliance/financial controls fail closed when evidence is absent.
