# Enterprise Search Vector PBC

`enterprise_search_vector` owns semantic and hybrid discovery for AppGen-X
applications. The package-local implementation manages search indexes,
embedding jobs, vectorized documents, query traces, ACL-filtered retrieval,
feedback-driven ranking evidence, AppGen-X outbox/inbox eventing, and the
search workbench surface without depending on shared operational tables.

## Owned Boundary

- PBC key: `enterprise_search_vector`
- Owned tables: `search_index`, `embedding_job`, `vector_document`,
  `query_trace`
- Allowed datastores: PostgreSQL, MySQL, MariaDB
- Event contract: AppGen-X outbox/inbox only
- Emitted events: `SearchIndexUpdated`, `DiscoveryInsightGenerated`
- Consumed events: `ProductPublished`, `CustomerUpdated`,
  `AuditEventSealed`
- Primary APIs: `POST /indexes`, `POST /indexes/{id}/refresh`,
  `POST /embeddings`, `POST /search`, `POST /query-feedback`,
  `GET /query-traces`

The package references product, customer, audit, and knowledge domains through
declared APIs, AppGen-X events, and projections only. It does not read or
write another PBC's tables.

## Standard Capabilities

1. Source-specific search index registration with tenant and locale ownership.
2. Vector document ingestion with chunking, document proofs, and ACL capture.
3. Embedding job orchestration with per-index readiness evidence.
4. Semantic and hybrid query execution with query traces and explanations.
5. Ranking inputs for semantic similarity, keyword overlap, freshness,
   authority, and feedback.
6. Relevance feedback recording with deterministic query-trace evidence.
7. Idempotent handling of `ProductPublished`, `CustomerUpdated`, and
   `AuditEventSealed`.
8. Emission of `SearchIndexUpdated` and `DiscoveryInsightGenerated` through
   the AppGen-X outbox.
9. Retry and dead-letter evidence for consumed events.
10. Search workbench fragments for indexes, documents, embedding jobs, query
    traces, freshness, feedback, configuration, outbox, and dead-letter
    review.
11. Rules, parameters, configuration schema, permissions, and seed defaults.
12. Package-local ownership proof for the four runtime tables.

## Advanced Capabilities

1. Event-sourced search-index lifecycle.
2. Schema-evolution evidence for package-owned document extensions.
3. Multi-tenant search isolation and package-local datastore ownership.
4. Probabilistic relevance-confidence evidence.
5. Counterfactual ranking simulation support through weighted ranking inputs.
6. Temporal freshness forecasting and self-healing index refresh evidence.
7. Autonomous search-quality remediation through feedback and refresh loops.
8. Semantic document understanding over vectorized documents and explanations.
9. Predictive query-intent risk and governed ranking evidence.
10. Cryptographic index proofs and immutable query audit trails.
11. Dynamic search-policy screening with deterministic compiled rule hashes.
12. Automated relevance control testing, AppGen-X eventing evidence, and
    cross-system federation through events and APIs only.

## Rules, Parameters, and Configuration

Rules compile deterministic evidence from:

- `rule_id`
- `tenant`
- `scope`
- `status`
- `allowed_sources`
- `allowed_locales`
- `acl_policy`
- `ranking_policy`
- `retention_policy`

Parameters are bounded to:

- `semantic_weight`
- `keyword_weight`
- `freshness_weight`
- `authority_weight`
- `feedback_weight`
- `relevance_threshold`
- `chunk_size_tokens`
- `embedding_batch_limit`
- `max_results`
- `workbench_limit`

Configuration requires:

- `database_backend`
- `event_topic`
- `retry_limit`
- `default_locale`
- `supported_locales`
- `supported_sources`
- `embedding_dimensions`
- `retention_days`
- `ranking_mode`
- `workbench_limit`

Runtime configuration rejects unsupported backends, requires the AppGen-X event
topic, and keeps `stream_engine_picker_visible` false. Ordinary eventing does
not expose a stream-engine picker or per-PBC runtime selector.

## UI and Workbench

The package exports a UI contract with fragments for:

- `EnterpriseSearchWorkbench`
- `SearchIndexRegistry`
- `VectorDocumentExplorer`
- `EmbeddingJobConsole`
- `HybridQueryWorkbench`
- `QueryTraceExplorer`
- `SearchIndexFreshnessBoard`
- `AclFilteredResultsPanel`
- `RelevanceFeedbackPanel`
- `SearchRuleStudio`
- `SearchParameterConsole`
- `SearchConfigurationPanel`
- `SearchEventOutbox`
- `SearchDeadLetterQueue`

Workbench rendering must expose configuration, rule, and parameter bindings,
owned-table evidence, and AppGen-X event-contract evidence while keeping the
stream-engine picker hidden.

## Runtime Completeness Contract

The package-local runtime is complete only when it proves that:

- rules, parameters, and configuration execute and affect document ingestion,
  ranking, refresh, query traces, and workbench bindings;
- only PostgreSQL, MySQL, or MariaDB are accepted;
- `ProductPublished`, `CustomerUpdated`, and `AuditEventSealed` handlers are
  idempotent and dead-letter capable;
- `SearchIndexUpdated` and `DiscoveryInsightGenerated` are emitted through the
  AppGen-X outbox contract;
- owned tables remain limited to `search_index`, `embedding_job`,
  `vector_document`, and `query_trace`;
- the UI contract exposes no stream-engine picker;
- focused tests prove runtime smoke, package-local implementation contract,
  workbench rendering, boundary checks, and invalid-input handling.
