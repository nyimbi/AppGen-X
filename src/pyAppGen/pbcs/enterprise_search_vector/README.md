# Enterprise Search Vector

`enterprise_search_vector` is a standalone AppGen-X PBC for governed semantic
and hybrid search. It owns search indexes, vector documents, embedding jobs,
query traces, ranking simulations, freshness forecasts, policy screening,
relevance controls, retention and deletion evidence, governed models, and its
AppGen-X event runtime tables.

## What The Package Provides

- Package-owned schema, models, migration evidence, and boundary validation.
- Executable runtime commands for configuration, indexing, ingestion,
  embeddings, search, quality remediation, policy screening, relevance
  controls, proofs, retention, and governed-model registration.
- A standalone one-PBC application composition in [standalone.py](./standalone.py).
- A workbench UI contract with forms, wizards, dashboards, and operator
  controls for bootstrap, discovery, and governance tasks.
- Agent/chatbot/document/CRUD planning surfaces for the composed application
  assistant.
- Dynamic release evidence that reads local contracts, migration SQL, and
  package documentation.

## Standalone Flow

1. Bootstrap runtime configuration, parameters, rules, and indexes with the
   package seed bundle.
2. Ingest documents and run embedding jobs against owned search indexes.
3. Execute hybrid queries with ACL filtering and result explanations.
4. Run governance flows such as intent-risk scoring, policy screening,
   relevance controls, freshness forecasting, proofs, and retention actions.

## Key Files

- [runtime.py](./runtime.py) — executable package runtime and evidence builders
- [standalone.py](./standalone.py) — standalone one-PBC app composition
- [ui.py](./ui.py) — workbench forms, wizards, controls, and render contract
- [seed_data.py](./seed_data.py) — deterministic standalone bootstrap bundle
- [release_evidence.py](./release_evidence.py) — dynamic release readiness proof
- [tests/test_contract.py](./tests/test_contract.py) — focused contract and runtime tests
