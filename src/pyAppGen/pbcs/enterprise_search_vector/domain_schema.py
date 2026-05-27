"""Domain schema metadata for the enterprise_search_vector PBC."""

PBC_KEY = "enterprise_search_vector"
TABLE_PREFIX = f"{PBC_KEY}_"

BUSINESS_TABLES = ("search_index", "embedding_job", "vector_document", "query_trace")
RUNTIME_TABLES = (
    "enterprise_search_vector_appgen_outbox_event",
    "enterprise_search_vector_appgen_inbox_event",
    "enterprise_search_vector_dead_letter_event",
)

BASE_FIELDS = (
    {"name": "id", "type": "integer", "primary_key": True, "nullable": False},
    {"name": "tenant", "type": "string", "required": True},
    {"name": "status", "type": "string", "required": True},
    {"name": "version", "type": "integer", "required": True},
    {"name": "created_at", "type": "datetime", "required": True},
    {"name": "updated_at", "type": "datetime", "required": True},
)

DOMAIN_FIELDS = {
    "search_index": (
        {"name": "index_id", "type": "string", "required": True, "unique": True},
        {"name": "name", "type": "string", "required": True},
        {"name": "source", "type": "string", "required": True},
        {"name": "locale", "type": "string", "required": True},
        {"name": "ranking_mode", "type": "string", "required": True},
        {"name": "document_count", "type": "integer", "required": True},
        {"name": "ready_document_count", "type": "integer", "required": True},
        {"name": "feedback_count", "type": "integer", "required": True},
        {"name": "last_embedding_job_id", "type": "string", "required": False},
        {"name": "last_refresh_id", "type": "string", "required": False},
        {"name": "audit_proof", "type": "string", "required": True},
    ),
    "embedding_job": (
        {"name": "job_id", "type": "string", "required": True, "unique": True},
        {"name": "index_id", "type": "string", "required": True},
        {"name": "document_ids", "type": "json", "required": True},
        {"name": "document_count", "type": "integer", "required": True},
        {"name": "vector_dimensions", "type": "integer", "required": True},
        {"name": "started_at", "type": "datetime", "required": False},
        {"name": "completed_at", "type": "datetime", "required": False},
        {"name": "failure_reason", "type": "string", "required": False},
        {"name": "audit_proof", "type": "string", "required": True},
    ),
    "vector_document": (
        {"name": "document_id", "type": "string", "required": True, "unique": True},
        {"name": "index_id", "type": "string", "required": True},
        {"name": "source", "type": "string", "required": True},
        {"name": "locale", "type": "string", "required": True},
        {"name": "title", "type": "string", "required": True},
        {"name": "body", "type": "text", "required": True},
        {"name": "chunks", "type": "json", "required": True},
        {"name": "token_count", "type": "integer", "required": True},
        {"name": "chunk_count", "type": "integer", "required": True},
        {"name": "embedding", "type": "json", "required": False},
        {"name": "acl", "type": "json", "required": True},
        {"name": "embedding_job_id", "type": "string", "required": False},
        {"name": "feedback_score", "type": "decimal", "required": True},
        {"name": "freshness_score", "type": "decimal", "required": True},
        {"name": "authority_score", "type": "decimal", "required": True},
        {"name": "quality_review_status", "type": "string", "required": True},
        {"name": "audit_proof", "type": "string", "required": True},
    ),
    "query_trace": (
        {"name": "query_id", "type": "string", "required": True, "unique": True},
        {"name": "index_id", "type": "string", "required": False},
        {"name": "query_text", "type": "text", "required": True},
        {"name": "locale", "type": "string", "required": True},
        {"name": "principal_permissions", "type": "json", "required": True},
        {"name": "ranking_mode", "type": "string", "required": True},
        {"name": "result_count", "type": "integer", "required": True},
        {"name": "results", "type": "json", "required": True},
        {"name": "explanations", "type": "json", "required": True},
        {"name": "feedback", "type": "json", "required": False},
        {"name": "audit_proof", "type": "string", "required": True},
    ),
    "enterprise_search_vector_appgen_outbox_event": (
        {"name": "event_id", "type": "string", "required": True},
        {"name": "event_type", "type": "string", "required": True},
        {"name": "topic", "type": "string", "required": True},
        {"name": "payload", "type": "json", "required": True},
        {"name": "idempotency_key", "type": "string", "required": True},
        {"name": "attempts", "type": "integer", "required": True},
        {"name": "published_at", "type": "datetime", "required": False},
    ),
    "enterprise_search_vector_appgen_inbox_event": (
        {"name": "event_id", "type": "string", "required": True},
        {"name": "event_type", "type": "string", "required": True},
        {"name": "payload", "type": "json", "required": True},
        {"name": "idempotency_key", "type": "string", "required": True},
        {"name": "attempts", "type": "integer", "required": True},
        {"name": "consumed_at", "type": "datetime", "required": False},
    ),
    "enterprise_search_vector_dead_letter_event": (
        {"name": "event_id", "type": "string", "required": False},
        {"name": "event_type", "type": "string", "required": True},
        {"name": "payload", "type": "json", "required": True},
        {"name": "idempotency_key", "type": "string", "required": False},
        {"name": "attempts", "type": "integer", "required": True},
        {"name": "failure_reason", "type": "text", "required": True},
    ),
}

RELATIONSHIPS = (
    {"from": "embedding_job.index_id", "to": "search_index.index_id", "type": "owned_reference"},
    {"from": "vector_document.index_id", "to": "search_index.index_id", "type": "owned_reference"},
    {"from": "vector_document.embedding_job_id", "to": "embedding_job.job_id", "type": "owned_reference"},
    {"from": "query_trace.index_id", "to": "search_index.index_id", "type": "owned_reference"},
    {"from": "query_trace.results", "to": "vector_document.document_id", "type": "owned_projection"},
)


def logical_table(table: str) -> str:
    return table.removeprefix(TABLE_PREFIX)


def owned_table(table: str) -> str:
    return table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"


def fields_for(table: str) -> tuple[dict, ...]:
    logical = table if table in RUNTIME_TABLES else logical_table(table)
    return BASE_FIELDS + DOMAIN_FIELDS[logical]


def field_names_for(table: str) -> tuple[str, ...]:
    return tuple(field["name"] for field in fields_for(table))


def relationships_for(table: str) -> tuple[dict, ...]:
    logical = logical_table(table)
    return tuple(item for item in RELATIONSHIPS if item["from"].startswith(f"{logical}."))


def class_name_for(table: str) -> str:
    return "".join(part.capitalize() for part in owned_table(table).split("_"))
