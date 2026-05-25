"""Packaged Business Capability catalog and composition contracts.

Composable enterprise apps are assembled from independently owned business
capabilities instead of one large shared module.  This module keeps that
catalog executable: every entry declares its datastore boundary, API surface,
event contracts, generated tables, and dependency evidence.
"""

from __future__ import annotations

import importlib.util
import json
import py_compile
import re
import sys
import tempfile
from pathlib import Path


PBC_MANIFEST_REQUIRED_FIELDS = (
    "pbc",
    "label",
    "mesh",
    "description",
    "datastore_backend",
    "tables",
    "apis",
    "emits",
    "consumes",
)
PBC_MANIFEST_OPTIONAL_FIELDS = (
    "template",
    "owner",
    "version",
    "stream_processor",
    "stream_exception_evidence",
    "ui_fragments",
    "permissions",
    "configuration",
    "migrations",
    "seed_data",
    "tests",
    "docs",
)
PBC_ALLOWED_DATASTORE_BACKENDS = (
    "postgresql",
    "mysql",
    "mariadb",
    "sqlite",
    "duckdb",
    "clickhouse",
    "mongodb",
    "opensearch",
)
ACP_STREAM_PROCESSORS: dict[str, dict] = {
    "faust_streaming": {
        "label": "Faust-Streaming",
        "core_architecture": "pure_python_asyncio_actor_mesh",
        "state_preservation": "embedded_rocksdb_or_in_memory",
        "primary_use_case": "event_driven_microservices_and_asynchronous_workflows",
        "concurrency_model": "asyncio_event_loops",
        "best_for": ("event_driven_service", "async_workflow", "saga_orchestration"),
    },
    "quix_streams": {
        "label": "Quix Streams",
        "core_architecture": "pure_python_rocksdb_state_backend",
        "state_preservation": "embedded_rocksdb_on_disk",
        "primary_use_case": "high_throughput_time_series_and_event_data_processing",
        "concurrency_model": "python_multiprocessing_threads",
        "best_for": ("time_series", "event_processing", "high_throughput_ingestion"),
    },
    "bytewax": {
        "label": "Bytewax",
        "core_architecture": "rust_core_python_dataflow_api",
        "state_preservation": "local_in_memory_distributed_recovery",
        "primary_use_case": "complex_parallel_transformations_and_stateful_pipelines",
        "concurrency_model": "rust_multithreaded_execution_threads",
        "best_for": ("parallel_dataflow", "stateful_pipeline", "complex_transform"),
    },
}
ACP_DEFAULT_STREAM_PROCESSOR = "faust_streaming"
ACP_STREAM_PROCESSOR_DECISION_RULES = (
    {
        "processor": "faust_streaming",
        "decision": "default",
        "use_when": (
            "event-driven PBC service",
            "asynchronous workflow",
            "saga orchestration",
            "service-owned local state",
        ),
    },
    {
        "processor": "quix_streams",
        "decision": "exception",
        "use_when": (
            "high-throughput telemetry",
            "time-series stream",
            "large event ingestion",
            "windowed operational metrics",
        ),
    },
    {
        "processor": "bytewax",
        "decision": "exception",
        "use_when": (
            "complex parallel dataflow",
            "stateful transformation graph",
            "CPU-heavy stream transform",
            "multi-stage analytical pipeline",
        ),
    },
)
ACP_STREAM_PROCESSING_POLICY = {
    "default": ACP_DEFAULT_STREAM_PROCESSOR,
    "allowed_processors": tuple(ACP_STREAM_PROCESSORS),
    "developer_guidance": {
        "standard_answer": (
            "Use the generated AppGen-X event contract: transactional "
            "outbox/inbox tables, typed handlers, retries, idempotency, "
            "dead-letter flows, and the platform event adapter. Do not choose "
            "a stream engine for ordinary work."
        ),
        "prescriptive_choice": "appgen_event_contract_only",
        "developer_decision_count": 1,
        "visible_developer_choice": "appgen_event_contract",
        "visible_choice_count": 1,
        "hidden_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "public_contract": (
            "AppGen-X event contract with generated transactional outbox/inbox, "
            "typed handlers, retry, idempotency, dead-letter, and release evidence."
        ),
        "runtime_owner": "platform_event_adapter",
        "choice_limit_reason": (
            "Every extra visible stream option multiplies generated-app "
            "validation across datastore, adapter, target package, deployment, "
            "PBC ownership, and release-audit surfaces."
        ),
        "implementation_recipe": (
            "declare_commands_and_events",
            "generate_owned_tables",
            "generate_transactional_outbox_inbox",
            "generate_typed_handlers",
            "wire_handlers_through_appgen_event_adapter",
            "prove_retry_idempotency_dead_letter_and_release_audit",
        ),
        "normal_workloads": (
            "ERP, CRM, HR, finance, inventory, commerce, approvals, workflow "
            "sagas, chatbot events, agent task routing, and PBC integration "
            "handlers."
        ),
        "manifest_rule": (
            "Omit stream_processor for ordinary PBCs; validation normalizes "
            "the manifest to faust_streaming."
        ),
        "ide_rule": (
            "Do not render a stream-engine picker for ordinary app generation; "
            "show the selected profile as read-only generated metadata."
        ),
        "agent_rule": (
            "Coding agents must generate event contracts and adapter calls, "
            "not direct stream-library imports."
        ),
        "exception_gate": (
            "Open the exception workflow only for telemetry/time-series "
            "ingestion or complex parallel dataflow workloads with evidence."
        ),
        "exception_policy": "two_audited_exception_profiles_not_user_preferences",
        "split_rule": (
            "If a PBC needs both ordinary domain events and specialized stream "
            "processing, split the specialized workload into its own PBC."
        ),
    },
    "developer_guidance_contract": {
        "question": "What should a developer actually use?",
        "answer": "Use appgen_event_contract.",
        "visible_options": ("appgen_event_contract",),
        "visible_option_count": 1,
        "ordinary_manifest_instruction": "Omit stream_processor.",
        "ordinary_datastore_instruction": "Use PostgreSQL by default, or MySQL/MariaDB when that is the project standard.",
        "ordinary_generation_instruction": (
            "Generate owned tables, appgen_outbox_event, appgen_inbox_event, "
            "typed handlers, idempotency keys, retry policies, dead-letter "
            "envelopes, and release evidence through the AppGen-X event adapter."
        ),
        "small_model_instruction": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables and typed handlers through the AppGen-X "
            "event adapter. Open an exception only for telemetry/time-series "
            "or complex parallel dataflow with evidence."
        ),
        "exception_options": ("quix_streams", "bytewax"),
        "exception_rule": (
            "Exception profiles are audit workflows, not developer preferences; "
            "split the specialized workload into its own PBC and require "
            "stream_exception_evidence."
        ),
        "hard_limits": {
            "ordinary_visible_choices": 1,
            "stream_profiles_per_pbc": 1,
            "ordinary_stream_engine_picker": False,
            "direct_profile_imports_in_generated_business_logic": False,
        },
        "developer_choice_lock": {
            "default_action": "generate_appgen_event_contract",
            "ordinary_manifest": {"stream_processor": "omit"},
            "ordinary_runtime_selection": "not_developer_selectable",
            "ide_surface": "show_event_contract_controls_only",
            "natural_language_surface": "do_not_expand_into_stream_runtime_comparison",
            "exception_unlocks": (
                "telemetry_time_series_high_volume_windowing_with_evidence",
                "complex_parallel_dataflow_with_evidence",
            ),
        },
        "stop_generating_options_when": (
            "The workload is ordinary business, ERP, workflow, chatbot, agent, "
            "integration, approval, or PBC event handling."
        ),
        "route_to_exception_workflow_when": (
            "The prompt names telemetry/time-series/high-volume windowing or "
            "complex parallel dataflow/CPU-heavy transformation and includes "
            "evidence."
        ),
        "developer_facing_apis": (
            "acp_event_processing_developer_guidance",
            "resolve_acp_event_processing_choice",
            "lint_pbc_eventing_choice",
        ),
        "platform_internal_apis": (
            "acp_stream_processor_catalog",
            "select_acp_stream_processor",
        ),
        "api_rule": (
            "Studio, DSL generation, package templates, and external coding "
            "agents use the developer-facing APIs. They must not expose the "
            "stream processor catalog or selector as an ordinary app choice."
        ),
    },
    "developer_action_contract": {
        "id": "appgen.event-processing.developer-action.v1",
        "question": "What should platform developers actually use?",
        "answer": "Use appgen_event_contract.",
        "use_this_stack": (
            "postgresql_default_or_mysql_mariadb_project_standard",
            "appgen_event_contract",
            "appgen_outbox_event",
            "appgen_inbox_event",
            "typed_command_handlers",
            "typed_event_handlers",
            "appgen_event_adapter",
            "generated_retry_idempotency_dead_letter_release_evidence",
        ),
        "ordinary_manifest_rule": "omit_stream_processor",
        "ordinary_codegen_rule": (
            "Generate owned tables, appgen_outbox_event, appgen_inbox_event, "
            "typed handlers, retry, idempotency, dead-letter, and release "
            "evidence through the AppGen-X event adapter."
        ),
        "ordinary_backend_rule": "postgresql_default_mysql_or_mariadb_project_standard",
        "developer_visible_options": ("appgen_event_contract",),
        "do_not_expose": (
            "stream_engine_picker",
            "runtime_profile_picker",
            "broker_picker",
            "state_store_picker",
            "per_pbc_runtime_preference",
        ),
        "do_not_generate": (
            "direct_stream_library_imports",
            "developer_selected_broker_clients",
            "per_pbc_stream_runtime_branches",
            "runtime_comparison_prompts",
            "custom_event_state_stores_for_ordinary_pbc_logic",
        ),
        "ordinary_path": (
            "declare_commands_and_events",
            "generate_owned_tables",
            "generate_appgen_outbox_event",
            "generate_appgen_inbox_event",
            "generate_typed_handlers",
            "wire_handlers_through_appgen_event_adapter",
            "prove_retry_idempotency_dead_letter_and_release_evidence",
        ),
        "exception_paths": (
            {
                "profile": "quix_streams",
                "only_for": "telemetry_time_series_high_volume_windowed_metrics",
                "requires": "stream_exception_evidence",
            },
            {
                "profile": "bytewax",
                "only_for": "complex_parallel_dataflow_cpu_heavy_transformations",
                "requires": "stream_exception_evidence",
            },
        ),
        "choice_budget": {
            "ordinary_visible_event_contracts": 1,
            "ordinary_visible_stream_engine_choices": 0,
            "ordinary_visible_runtime_profile_choices": 0,
            "exception_profiles": 2,
            "stream_profiles_per_pbc": 1,
        },
        "fallback_rule": (
            "If the exception workload and evidence are not explicit, generate "
            "appgen_event_contract and omit stream_processor."
        ),
        "api_call_order": (
            "acp_event_processing_developer_guidance",
            "resolve_acp_event_processing_choice",
            "lint_pbc_eventing_choice",
        ),
        "internal_api_boundary": (
            "Do not call select_acp_stream_processor from ordinary generated-app "
            "templates or Studio controls; it is platform-runtime metadata for "
            "exception validation."
        ),
        "token_efficient_prompt": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables and typed handlers through the AppGen-X event "
            "adapter. Do not compare runtimes. Open an exception only for "
            "telemetry/time-series or complex dataflow with evidence."
        ),
    },
    "developer_use_card": {
        "id": "appgen.event-processing.use-this.v1",
        "title": "Use appgen_event_contract for ordinary generated applications.",
        "decision": "mandatory_default",
        "use": "appgen_event_contract",
        "ordinary_manifest": {"stream_processor": "omit"},
        "ordinary_datastores": ("postgresql", "mysql", "mariadb"),
        "developer_writes": (
            "commands",
            "domain_events",
            "owned_tables",
            "handler_functions",
            "retry_policy_names",
            "idempotency_key_fields",
            "dead_letter_ownership_notes",
        ),
        "platform_generates": (
            "appgen_outbox_event",
            "appgen_inbox_event",
            "typed_command_handlers",
            "typed_event_handlers",
            "event_adapter_bindings",
            "release_audit_evidence",
        ),
        "studio_exposes": (
            "event_contract_designer",
            "handler_registry_editor",
            "retry_idempotency_dead_letter_editor",
            "read_only_runtime_profile_badge",
        ),
        "studio_hides": (
            "stream_engine_picker",
            "broker_picker",
            "state_store_picker",
            "per_pbc_runtime_profile_picker",
        ),
        "ordinary_stop_rule": (
            "For ERP, workflow, chatbot, agent, integration, approval, and "
            "ordinary PBC events, stop at appgen_event_contract and do not "
            "generate a runtime comparison."
        ),
        "exception_unlocks": (
            "telemetry_time_series_high_volume_windowing_with_stream_exception_evidence",
            "complex_parallel_dataflow_with_stream_exception_evidence",
        ),
        "fallback": "When uncertain, use appgen_event_contract and omit stream_processor.",
    },
    "developer_decision_brief": {
        "headline": "Use appgen_event_contract.",
        "ordinary_answer": (
            "Generate the AppGen-X event contract with transactional "
            "outbox/inbox tables, typed handlers, retries, idempotency, "
            "dead-letter handling, and release evidence."
        ),
        "ordinary_manifest_rule": "Omit stream_processor.",
        "ordinary_codegen_prompt": (
            "Generate AppGen-X outbox/inbox events through the platform "
            "adapter. Omit stream_processor. Do not compare stream engines."
        ),
        "developer_visible_options": ("appgen_event_contract",),
        "developer_visible_option_count": 1,
        "default_runtime_profile_visibility": "read_only_generated_metadata",
        "studio_controls": (
            "event_contract_designer",
            "handler_registry_editor",
            "retry_idempotency_dead_letter_editor",
            "read_only_runtime_profile_badge",
        ),
        "studio_controls_to_hide": ("stream_engine_picker", "per_pbc_runtime_preference"),
        "linter_rules": (
            "ordinary_pbc_manifest_omits_stream_processor",
            "generated_business_logic_imports_appgen_event_adapter_only",
            "exception_profiles_require_stream_exception_evidence",
            "one_stream_profile_per_pbc",
        ),
        "allowed_exceptions": ("quix_streams", "bytewax"),
        "exception_gate": (
            "Use an exception profile only for telemetry/time-series/high-volume "
            "windowing or complex parallel dataflow with evidence."
        ),
        "small_model_stop_rule": (
            "When the request is ordinary business, ERP, workflow, chatbot, "
            "agent, integration, or PBC event handling, stop branching and use "
            "the ordinary answer."
        ),
        "api_contract": (
            "Call resolve_acp_event_processing_choice for generation decisions; "
            "render acp_event_processing_developer_guidance for help text; run "
            "lint_pbc_eventing_choice before release."
        ),
    },
    "developer_implementation_playbook": {
        "id": "appgen.event-processing.implementation-playbook.v1",
        "purpose": "tell platform developers exactly what to build for ordinary evented apps",
        "studio": (
            "show_event_contract_designer",
            "show_handler_registry_editor",
            "show_retry_idempotency_dead_letter_editor",
            "show_read_only_runtime_profile_badge",
            "hide_stream_engine_picker",
            "hide_per_pbc_runtime_preference",
        ),
        "dsl_linter": (
            "require_ordinary_manifests_to_omit_stream_processor",
            "offer_remove_stream_processor_quick_fix",
            "block_exception_profiles_without_stream_exception_evidence",
            "block_profile_specific_imports_in_generated_business_logic",
        ),
        "natural_language_generation": (
            "map_ordinary_business_prompts_to_appgen_event_contract",
            "generate_outbox_inbox_tables_and_typed_handlers",
            "avoid_runtime_comparison_prompts",
            "open_exception_workflow_only_with_named_evidence",
        ),
        "package_templates": (
            "include_appgen_outbox_event",
            "include_appgen_inbox_event",
            "include_event_adapter_bindings",
            "include_retry_policy",
            "include_idempotency_keys",
            "include_dead_letter_contract",
            "include_release_audit_evidence",
        ),
        "coding_agent_prompt": (
            "Use appgen_event_contract. Omit stream_processor. Generate "
            "outbox/inbox tables, typed handlers, retry, idempotency, "
            "dead-letter, and release evidence through the AppGen-X event "
            "adapter. Do not compare runtimes."
        ),
        "acceptance_criteria": (
            "ordinary_manifest_has_no_stream_processor",
            "generated_business_logic_imports_only_appgen_event_adapter",
            "studio_has_no_stream_runtime_picker",
            "exception_profiles_require_stream_exception_evidence",
            "release_audit_records_event_contract_outputs",
            "ordinary_generators_do_not_call_stream_processor_selector",
        ),
    },
    "developer_choice_algorithm": (
        {
            "step": 1,
            "if": "ordinary business, ERP, workflow, chatbot, agent, integration, or PBC event handling",
            "then": "generate the AppGen-X event contract",
            "manifest": "omit stream_processor",
            "runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
            "requires_evidence": False,
        },
        {
            "step": 2,
            "if": "telemetry, time-series ingestion, high-volume ingestion, or windowed operational metrics",
            "then": "split into a specialized PBC and request the telemetry exception profile",
            "manifest": "stream_processor=quix_streams",
            "runtime_profile": "quix_streams",
            "requires_evidence": True,
        },
        {
            "step": 3,
            "if": "complex parallel dataflow, CPU-heavy stream transformation, or multi-stage analytical pipeline",
            "then": "split into a specialized PBC and request the dataflow exception profile",
            "manifest": "stream_processor=bytewax",
            "runtime_profile": "bytewax",
            "requires_evidence": True,
        },
        {
            "step": 4,
            "if": "anything else or unclear",
            "then": "generate the AppGen-X event contract",
            "manifest": "omit stream_processor",
            "runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
            "requires_evidence": False,
        },
    ),
    "developer_use_policy": {
        "ordinary_applications": {
            "use": "appgen_event_contract",
            "developer_instruction": (
                "Generate transactional outbox/inbox tables and typed handlers "
                "through the AppGen-X event adapter."
            ),
            "manifest_rule": "omit_stream_processor",
            "datastore_rule": "postgresql_by_default_mysql_or_mariadb_when_project_standard",
            "generated_stack": (
                "owned_tables",
                "appgen_outbox_event",
                "appgen_inbox_event",
                "typed_event_handlers",
                "retry_policy",
                "idempotency_keys",
                "dead_letter_contract",
                "release_audit_evidence",
            ),
            "visible_developer_options": ("appgen_event_contract",),
        },
        "telemetry_exception": {
            "use": "quix_streams_exception_workflow",
            "developer_instruction": (
                "Split telemetry, time-series, high-volume ingestion, or "
                "windowed metrics into a specialized PBC and provide evidence."
            ),
            "manifest_rule": "stream_processor=quix_streams_with_stream_exception_evidence",
            "requires_evidence": True,
        },
        "dataflow_exception": {
            "use": "bytewax_exception_workflow",
            "developer_instruction": (
                "Split complex parallel dataflow, CPU-heavy transforms, or "
                "multi-stage analytical pipelines into a specialized PBC and "
                "provide evidence."
            ),
            "manifest_rule": "stream_processor=bytewax_with_stream_exception_evidence",
            "requires_evidence": True,
        },
    },
    "choice_budget": {
        "ordinary_public_event_contracts": 1,
        "ordinary_visible_stream_engine_choices": 0,
        "ordinary_visible_runtime_choices": ("appgen_event_contract",),
        "exception_profiles": ("quix_streams", "bytewax"),
        "exception_profile_count": 2,
        "stream_profiles_per_pbc": 1,
        "additional_profile_requires": (
            "architecture_decision",
            "executable_policy",
            "manifest_validation",
            "release_audit_gate",
            "generated_tests",
            "developer_documentation",
        ),
    },
    "ordinary_workload_contract": {
        "public_choice": "appgen_event_contract",
        "developer_prompt": (
            "Generate commands, events, transactional outbox/inbox tables, "
            "typed handlers, idempotency, retry, dead-letter, and release "
            "evidence through the AppGen-X event adapter."
        ),
        "manifest_fields": ("commands", "events", "tables", "apis", "emits", "consumes"),
        "manifest_fields_to_omit": ("stream_processor",),
        "generated_files": ("models.py", "events.py", "services.py", "api.py", "pbc_runtime.py"),
        "forbidden_imports": ("faust_streaming", "quix_streams", "bytewax"),
        "studio_control": "read_only_runtime_profile_badge",
    },
    "developer_default_stack": {
        "id": "appgen.event-processing.default-stack.v1",
        "scope": "ordinary_generated_applications_and_pbcs",
        "use": "appgen_event_contract",
        "database": "postgresql_default_mysql_or_mariadb_when_project_standard",
        "durability": ("appgen_outbox_event", "appgen_inbox_event"),
        "handler_api": "appgen_event_adapter",
        "handler_shape": ("typed_command_handlers", "typed_event_handlers"),
        "operations": (
            "idempotency_keys",
            "retry_policy",
            "dead_letter_contract",
            "release_audit_evidence",
        ),
        "ordinary_manifest": {"stream_processor": "omit"},
        "runtime_visibility": "read_only_platform_metadata",
        "developer_choice_count": 1,
        "small_model_prompt": (
            "Use appgen_event_contract with generated outbox/inbox tables and "
            "typed handlers through the AppGen-X event adapter. Omit "
            "stream_processor. Do not compare runtimes."
        ),
        "blocked_expansion_axes": (
            "stream_engine",
            "broker_client",
            "state_store",
            "per_pbc_runtime",
            "direct_stream_library_import",
        ),
    },
    "developer_recommendation_card": {
        "id": "appgen.event-processing.recommendation-card.v1",
        "title": "Use appgen_event_contract.",
        "status": "mandatory_for_ordinary_generated_work",
        "recommendation": (
            "Use the AppGen-X event contract with generated outbox/inbox "
            "tables and typed handlers. Developers author commands, events, "
            "and handlers; the platform owns the runtime adapter."
        ),
        "developer_writes": (
            "commands",
            "events",
            "handler_functions",
            "business_tables",
        ),
        "platform_generates": (
            "appgen_outbox_event",
            "appgen_inbox_event",
            "event_adapter_bindings",
            "retry_policy",
            "idempotency_keys",
            "dead_letter_contract",
            "release_audit_evidence",
        ),
        "ordinary_manifest": {"stream_processor": "omit"},
        "ordinary_database_backends": ("postgresql", "mysql", "mariadb"),
        "hidden_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "visible_developer_options": ("appgen_event_contract",),
        "visible_choice_count": 1,
        "not_a_question_for_developers": (
            "stream_engine",
            "broker_client",
            "state_store",
            "per_pbc_runtime_profile",
        ),
        "exception_exit_criteria": (
            "telemetry_time_series_high_volume_windowing_with_stream_exception_evidence",
            "complex_parallel_dataflow_with_stream_exception_evidence",
        ),
        "fallback": "Use appgen_event_contract and omit stream_processor.",
    },
    "decision_card": {
        "answer": "Use the AppGen-X generated outbox/inbox event contract; the platform keeps faust_streaming behind the adapter for ordinary work.",
        "default_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "choice_contract": "one_default_two_audited_exceptions",
        "public_contract": "appgen_event_contract",
        "do_this": (
            "model commands and events",
            "generate transactional outbox/inbox tables",
            "write typed handlers behind the AppGen-X event adapter",
            "prove retry, idempotency, dead-letter, and release-audit coverage",
        ),
        "do_not_do_this": (
            "compare Kafka alternatives for ordinary generated work",
            "render a stream-engine picker",
            "generate per-PBC runtime preferences",
            "import stream-processing libraries directly from generated business logic",
        ),
        "ordinary_developer_choices": ("appgen_event_contract",),
        "ordinary_developer_choice_count": 1,
        "selection_mode": "read_only_default_with_audited_exceptions",
        "do_not_ask_users_to_choose": True,
        "developer_selection": "not_user_selectable_for_ordinary_app_generation",
        "ide_behavior": "show the generated default profile and open an exception request only when evidence is supplied",
        "nl_generator_behavior": "choose the default for ordinary business, workflow, chatbot, agent, and ERP prompts",
        "business_logic_rule": "generated business logic imports the AppGen-X event adapter, not profile-specific stream libraries",
        "selection_algorithm": "first_matching_rule_from_developer_choice_algorithm",
    },
    "developer_choice_lock": {
        "id": "appgen.event-processing.choice-lock.v1",
        "purpose": "limit_exponential_stream_runtime_choice_growth",
        "ordinary_answer": "appgen_event_contract",
        "ordinary_manifest_fields": {"stream_processor": "omit"},
        "ordinary_visible_choices": ("appgen_event_contract",),
        "ordinary_visible_choice_count": 1,
        "developer_selectable_runtime_profiles": (),
        "platform_owned_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "exception_profiles": ("quix_streams", "bytewax"),
        "exception_requires": "stream_exception_evidence",
        "stop_rule": (
            "If the prompt is ordinary business, ERP, workflow, chatbot, "
            "agent, integration, approval, or PBC event handling, stop at "
            "appgen_event_contract and do not compare stream runtimes."
        ),
    },
    "developer_decision_record": {
        "id": "appgen.event-processing.standard.v1",
        "status": "mandatory",
        "decision": "ordinary_generated_applications_use_appgen_event_contract",
        "developer_answer": "Use appgen_event_contract and omit stream_processor.",
        "reason": (
            "The platform can validate one ordinary event path across PBCs, "
            "datastores, generated targets, adapters, tests, and release "
            "audits. A user-facing stream-engine choice would multiply that "
            "support matrix for every generated capability."
        ),
        "ordinary_path": (
            "generate_owned_tables",
            "generate_transactional_outbox_inbox",
            "generate_typed_handlers",
            "route_through_platform_event_adapter",
            "record_runtime_profile_as_read_only_metadata",
        ),
        "support_matrix_cap": {
            "ordinary_event_contracts": 1,
            "ordinary_visible_stream_engines": 0,
            "ordinary_visible_runtime_profiles": 0,
            "exception_profiles": 2,
            "profiles_per_pbc": 1,
        },
        "exception_gate": (
            "Only telemetry/time-series or complex parallel dataflow workloads "
            "may request an exception, and only with stream_exception_evidence."
        ),
        "tooling_obligations": (
            "hide_stream_engine_picker",
            "lint_ordinary_manifests_that_set_stream_processor",
            "block_exception_profiles_without_evidence",
            "fail_generated_business_logic_with_profile_specific_imports",
            "route_generators_through_event_choice_resolver",
        ),
    },
    "opinionated_stack": {
        "default_event_adapter": "appgen_outbox_inbox_faust_streaming",
        "development": "appgen_in_memory_event_bus_with_generated_outbox_inbox",
        "production": "appgen_event_backbone_adapter_with_generated_outbox_inbox",
        "service_runtime": ACP_DEFAULT_STREAM_PROCESSOR,
        "state_boundary": "owned_by_one_pbc_datastore",
        "selection_mode": "platform_default_unless_exception_evidence_is_present",
        "visible_runtime_choices": ("appgen_event_contract",),
    },
    "developer_rule": (
        "Do not choose a stream engine for ordinary generated applications. "
        "Use the platform event contract, generated outbox/inbox adapters, "
        "and the default processor. Select an exception processor only when "
        "the workload matches a documented exception profile and includes "
        "machine-checkable evidence."
    ),
    "generation_rule": (
        "Generated manifests omit stream_processor unless they need an "
        "exception. Validation normalizes missing values to the default."
    ),
    "implementation_directive": (
        "Generate transactional outbox/inbox tables, typed event handlers, "
        "idempotency keys, retry policies, dead-letter contracts, and release "
        "audit evidence. Do not generate direct imports of faust_streaming, "
        "quix_streams, or bytewax in PBC business logic; profile-specific code "
        "belongs only in platform adapter modules."
    ),
    "generator_outputs": (
        "transactional_outbox",
        "transactional_inbox",
        "typed_event_handlers",
        "idempotency_keys",
        "retry_policy_names",
        "dead_letter_contracts",
        "release_audit_evidence",
    ),
    "decision_ladder": (
        "omit_stream_processor_for_ordinary_apps",
        "normalize_missing_profile_to_faust_streaming",
        "require_exception_evidence_for_quix_streams_or_bytewax",
        "split_specialized_stream_workloads_into_their_own_pbc",
        "block_release_when_exception_evidence_is_missing",
    ),
    "workload_defaults": (
        {"workload": "erp_crm_hr_finance_inventory_commerce", "processor": ACP_DEFAULT_STREAM_PROCESSOR, "decision": "default"},
        {"workload": "workflow_saga_approval_agent_task_routing", "processor": ACP_DEFAULT_STREAM_PROCESSOR, "decision": "default"},
        {"workload": "chatbot_agentic_application_events", "processor": ACP_DEFAULT_STREAM_PROCESSOR, "decision": "default"},
        {"workload": "telemetry_time_series_large_ingestion", "processor": "quix_streams", "decision": "exception"},
        {"workload": "complex_parallel_dataflow_cpu_heavy_transform", "processor": "bytewax", "decision": "exception"},
    ),
    "exception_prompts": (
        "What named workload requires the exception?",
        "What throughput, latency, state, or recovery constraint makes the default insufficient?",
        "Who owns runtime operations and incidents for this specialized workload?",
    ),
    "exception_required_evidence": (
        "workload_name",
        "throughput_or_latency_reason",
        "state_shape",
        "operational_owner",
    ),
    "prohibited": (
        "per-PBC custom stream engines",
        "mixing multiple processors inside one PBC",
        "shared stream-state stores across PBC datastore boundaries",
        "adding a fourth processor without a platform architecture decision",
        "asking natural-language generation to compare stream libraries",
        "exposing a free-form stream-engine selector in the IDE",
        "importing profile-specific stream libraries from generated business logic",
    ),
    "decision_tree": (
        {
            "when": "ordinary domain events, commands, sagas, outbox handlers, workflow services, or agent tasks",
            "use": ACP_DEFAULT_STREAM_PROCESSOR,
        },
        {
            "when": "high-throughput telemetry, time-series streams, large ingestion, or windowed operational metrics",
            "use": "quix_streams",
        },
        {
            "when": "complex parallel dataflows, CPU-heavy transforms, stateful transformation graphs, or analytical pipelines",
            "use": "bytewax",
        },
    ),
}


PBC_MESHES: dict[str, dict] = {
    "finops": {
        "label": "Financial Operations",
        "description": "Monetary, compliance, accounting, and treasury capabilities.",
    },
    "scl": {
        "label": "Supply Chain and Logistics",
        "description": "Physical movement, storage, sourcing, and fulfillment capabilities.",
    },
    "hcm": {
        "label": "Human Capital Management",
        "description": "Personnel, identity, labor, payroll, and talent capabilities.",
    },
    "opsmfg": {
        "label": "Operations and Manufacturing",
        "description": "Planning, production, quality, and asset maintenance capabilities.",
    },
    "cx": {
        "label": "Commerce and Customer Experience",
        "description": "Demand capture, order orchestration, catalog, and customer capabilities.",
    },
    "platform": {
        "label": "Core Platform, Integration, and Governance",
        "description": "Identity, gateway, contract validation, workflow, audit, and composition fabric.",
    },
    "commerce": {
        "label": "Advanced Commerce and Fulfillment",
        "description": "Checkout, order routing, payments, subscriptions, returns, and cross-border commerce.",
    },
    "content": {
        "label": "Product Content, Information, and Assets",
        "description": "Product information, digital assets, pricing, promotions, and content governance.",
    },
    "relationship": {
        "label": "Relationship, Support, and Marketing",
        "description": "Pipeline, support, notifications, customer segmentation, and loyalty capabilities.",
    },
    "intelligence": {
        "label": "Analytics, Business Intelligence, and Artificial Intelligence",
        "description": "Streaming analytics, search, forecasting, fraud, and predictive intelligence.",
    },
}


PBC_CATALOG: dict[str, dict] = {
    "gl_core": {
        "label": "General Ledger Core",
        "mesh": "finops",
        "description": "Immutable financial truth, journal orchestration, chart of accounts, and balances.",
        "tables": ("journal_entry", "journal_line", "ledger_account", "accounting_period"),
        "apis": ("POST /journals", "GET /trial-balance", "GET /chart-of-accounts"),
        "emits": ("JournalPosted", "PeriodClosed", "TrialBalanceCalculated"),
        "consumes": ("InvoiceApproved", "PaymentCaptured", "DepreciationCalculated", "OrderShipped"),
        "template": "general_ledger",
    },
    "ap_automation": {
        "label": "Accounts Payable Automation",
        "mesh": "finops",
        "description": "Vendor obligations, OCR intake, invoice matching, approval, and withholding.",
        "tables": ("vendor", "ap_bill", "ap_payment", "ap_match_exception"),
        "apis": ("POST /vendor-bills", "POST /matches", "POST /approvals"),
        "emits": ("InvoiceApproved", "VendorPaymentRequested", "MatchExceptionRaised"),
        "consumes": ("PurchaseOrderIssued", "GoodsReceiptPosted", "TaxCalculated"),
        "template": "accounts_payable",
    },
    "ar_credit": {
        "label": "Accounts Receivable and Credit",
        "mesh": "finops",
        "description": "Customer invoicing, receivables, collections, aging, and credit limits.",
        "tables": ("customer", "ar_invoice", "ar_payment", "credit_profile"),
        "apis": ("POST /customer-invoices", "GET /aging", "POST /credit-decisions"),
        "emits": ("InvoiceIssued", "PaymentCaptured", "CreditLimitChanged"),
        "consumes": ("OrderShipped", "CustomerUpdated", "TaxCalculated"),
        "template": "accounts_receivable",
    },
    "treasury_cash": {
        "label": "Treasury and Cash Management",
        "mesh": "finops",
        "description": "Multi-currency cash, forecasting, statement ingestion, and reconciliation.",
        "tables": ("bank_account", "bank_statement", "cash_forecast", "reconciliation_item"),
        "apis": ("POST /statements", "GET /cash-position", "POST /reconciliations"),
        "emits": ("CashPositionUpdated", "BankReconciled"),
        "consumes": ("VendorPaymentRequested", "PaymentCaptured", "JournalPosted"),
        "template": None,
    },
    "asset_lifecycle": {
        "label": "Asset Lifecycle and Depreciation",
        "mesh": "finops",
        "description": "Fixed assets, lifecycle state, statutory depreciation, and journal emission.",
        "tables": ("fixed_asset", "asset_event", "depreciation_schedule", "depreciation_run"),
        "apis": ("POST /assets", "POST /depreciation-runs", "GET /asset-register"),
        "emits": ("DepreciationCalculated", "AssetRetired"),
        "consumes": ("AssetPlacedInService", "MaintenanceCompleted"),
        "template": None,
    },
    "tax_localization": {
        "label": "Tax Compliance and Localization",
        "mesh": "finops",
        "description": "Regional tax, VAT, duties, product taxonomies, and jurisdiction rules.",
        "tables": ("tax_jurisdiction", "tax_rule", "tax_calculation", "tax_filing"),
        "apis": ("POST /tax-quotes", "POST /filings", "GET /jurisdictions"),
        "emits": ("TaxCalculated", "TaxFilingPrepared"),
        "consumes": ("ProductClassified", "InvoiceIssued", "OrderPriced"),
        "template": None,
    },
    "inventory_positioning": {
        "label": "Inventory Positioning and State",
        "mesh": "scl",
        "description": "Quantity, allocation, availability, quarantine, in-transit state, and node positions.",
        "tables": ("item", "inventory_node", "inventory_position", "allocation"),
        "apis": ("GET /availability", "POST /allocations", "POST /inventory-events"),
        "emits": ("InventoryAllocated", "InventoryReleased", "GoodsReceiptPosted"),
        "consumes": ("OrderVerified", "ShipmentDelivered", "QualityHoldReleased"),
        "template": "inventory",
    },
    "wms_core": {
        "label": "Warehouse Management Core",
        "mesh": "scl",
        "description": "Putaway, picking, packing, cross-docking, and warehouse edge workflows.",
        "tables": ("warehouse", "bin_location", "pick_wave", "pack_task"),
        "apis": ("POST /putaway", "POST /pick-waves", "POST /pack-tasks"),
        "emits": ("Picked", "Packed", "GoodsReceiptPosted", "OrderShipped"),
        "consumes": ("InventoryAllocated", "InboundArrived"),
        "template": "warehouse_management",
    },
    "procurement_sourcing": {
        "label": "Procurement and Strategic Sourcing",
        "mesh": "scl",
        "description": "Requisitions, RFQs, contracts, purchase orders, and vendor performance.",
        "tables": ("purchase_requisition", "rfq", "vendor_contract", "purchase_order"),
        "apis": ("POST /requisitions", "POST /rfqs", "POST /purchase-orders"),
        "emits": ("PurchaseOrderIssued", "SupplierSelected"),
        "consumes": ("MaterialShortageDetected", "VendorPerformanceUpdated"),
        "template": "purchasing",
    },
    "transportation_management": {
        "label": "Transportation Management",
        "mesh": "scl",
        "description": "Freight routing, carrier choice, shipment tracking, telematics, and ETA updates.",
        "tables": ("shipment", "carrier", "freight_route", "tracking_event"),
        "apis": ("POST /shipments", "POST /carrier-selection", "GET /eta"),
        "emits": ("InboundArrived", "ShipmentDelivered", "EtaUpdated"),
        "consumes": ("Packed", "PurchaseOrderIssued"),
        "template": None,
    },
    "personnel_identity": {
        "label": "Personnel Directory and Identity",
        "mesh": "hcm",
        "description": "Employee master data, organization charts, RBAC attributes, and identity facts.",
        "tables": ("department", "employee", "role_assignment", "identity_attribute"),
        "apis": ("POST /employees", "GET /org-chart", "GET /identity-attributes"),
        "emits": ("EmployeeCreated", "RoleChanged", "CustomerUpdated"),
        "consumes": ("EmployeeProvisioned",),
        "template": "human_resources",
    },
    "time_labor": {
        "label": "Time Attendance and Labor Tracking",
        "mesh": "hcm",
        "description": "Shifts, overtime, absence, geo-fenced clock actions, and payroll-ready hours.",
        "tables": ("shift", "time_entry", "absence", "labor_summary"),
        "apis": ("POST /clock-events", "POST /absences", "GET /labor-summaries"),
        "emits": ("LaborHoursApproved", "AbsenceRecorded"),
        "consumes": ("EmployeeCreated", "RoleChanged"),
        "template": None,
    },
    "payroll_engine": {
        "label": "Compensation and Payroll Engine",
        "mesh": "hcm",
        "description": "Gross-to-net payroll, deductions, benefits, and localized payroll filings.",
        "tables": ("payroll_run", "payslip", "deduction", "benefit_allocation"),
        "apis": ("POST /payroll-runs", "GET /payslips", "POST /payroll-filings"),
        "emits": ("PayrollPosted", "PayrollFilingPrepared"),
        "consumes": ("LaborHoursApproved", "TaxCalculated"),
        "template": "payroll",
    },
    "talent_onboarding": {
        "label": "Talent Acquisition and Onboarding",
        "mesh": "hcm",
        "description": "Applicant pipelines, checks, onboarding tasks, and day-one provisioning.",
        "tables": ("candidate", "job_requisition", "background_check", "onboarding_task"),
        "apis": ("POST /candidates", "POST /offers", "POST /onboarding"),
        "emits": ("EmployeeProvisioned", "CandidateHired"),
        "consumes": ("RoleChanged",),
        "template": None,
    },
    "mrp_engine": {
        "label": "Material Requirements Planning Engine",
        "mesh": "opsmfg",
        "description": "BOM graph analysis, inventory demand, production plans, and procurement schedules.",
        "tables": ("bill_of_material", "material_demand", "mrp_run", "planned_order"),
        "apis": ("POST /mrp-runs", "GET /planned-orders", "GET /shortages"),
        "emits": ("MaterialShortageDetected", "PlannedOrderReleased"),
        "consumes": ("InventoryReleased", "OrderVerified", "ForecastUpdated"),
        "template": "manufacturing",
    },
    "production_control": {
        "label": "Production Scheduling and Floor Control",
        "mesh": "opsmfg",
        "description": "Routings, work centers, capacity, assembly sequencing, OEE, and downtime events.",
        "tables": ("work_center", "production_order", "routing_step", "downtime_event"),
        "apis": ("POST /production-orders", "POST /downtime", "GET /schedule"),
        "emits": ("ProductionCompleted", "AssetPlacedInService", "DowntimeCaptured"),
        "consumes": ("PlannedOrderReleased", "MaintenanceCompleted"),
        "template": "manufacturing",
    },
    "quality_assurance": {
        "label": "Quality Assurance and Compliance",
        "mesh": "opsmfg",
        "description": "Inspection checklists, SPC sampling, non-conformance, and quality holds.",
        "tables": ("inspection_plan", "inspection_result", "quality_hold", "non_conformance"),
        "apis": ("POST /inspections", "POST /non-conformances", "POST /quality-holds"),
        "emits": ("QualityHoldReleased", "NonConformanceRaised"),
        "consumes": ("ProductionCompleted", "GoodsReceiptPosted"),
        "template": "quality_management",
    },
    "eam": {
        "label": "Enterprise Asset Management",
        "mesh": "opsmfg",
        "description": "Preventive and predictive maintenance, MTBF, work orders, and spare parts use.",
        "tables": ("equipment", "maintenance_plan", "work_order", "spare_part_usage"),
        "apis": ("POST /work-orders", "GET /maintenance-plan", "POST /asset-events"),
        "emits": ("MaintenanceCompleted", "VendorPerformanceUpdated"),
        "consumes": ("DowntimeCaptured", "NonConformanceRaised"),
        "template": None,
    },
    "dom": {
        "label": "Distributed Order Management",
        "mesh": "cx",
        "description": "Order verification, fraud screening, allocation, and fulfillment orchestration.",
        "tables": ("sales_order", "order_line", "fulfillment_plan", "fraud_screen"),
        "apis": ("POST /orders", "POST /allocation", "GET /fulfillment-plans"),
        "emits": ("OrderVerified", "OrderPriced", "OrderShipped"),
        "consumes": ("InventoryAllocated", "TaxCalculated", "CustomerUpdated"),
        "template": "sales",
    },
    "product_catalog_pim": {
        "label": "Enterprise Product Catalog and PIM",
        "mesh": "cx",
        "description": "Product schemas, pricing, localized descriptions, media, and read models.",
        "tables": ("product", "product_price", "product_media", "product_attribute"),
        "apis": ("POST /products", "GET /product-read-models", "POST /prices"),
        "emits": ("ProductClassified", "ProductPublished", "ForecastUpdated"),
        "consumes": ("TaxCalculated",),
        "template": "crm",
    },
    "customer_360": {
        "label": "Customer 360 and Engagement Registry",
        "mesh": "cx",
        "description": "Profiles, touchpoints, preferences, channel history, and customer read models.",
        "tables": ("customer_profile", "engagement_event", "communication_preference", "touchpoint"),
        "apis": ("POST /profiles", "POST /touchpoints", "GET /customer-timeline"),
        "emits": ("CustomerUpdated", "PreferenceChanged"),
        "consumes": ("InvoiceIssued", "PaymentCaptured", "CandidateHired"),
        "template": "crm",
    },
}

PBC_CATALOG.update(
    {
        "federated_iam": {
            "label": "Federated Identity and Access Management",
            "mesh": "platform",
            "description": "Context-aware RBAC/ABAC, tenant isolation, OIDC, verification loops, and token issuance.",
            "tables": ("tenant", "principal", "access_policy", "token_grant"),
            "apis": ("POST /tokens", "GET /principals", "POST /policy-decisions"),
            "emits": ("AccessPolicyChanged", "PrincipalVerified"),
            "consumes": ("RoleChanged", "TenantProvisioned"),
            "template": None,
        },
        "api_gateway_mesh": {
            "label": "Dynamic API Gateway and Service Mesh",
            "mesh": "platform",
            "description": "Ingress routing, rate limiting, service discovery, mTLS policy, and telemetry.",
            "tables": ("service_route", "rate_limit_policy", "mtls_identity", "traffic_sample"),
            "apis": ("POST /routes", "POST /rate-limits", "GET /service-map"),
            "emits": ("RoutePublished", "ServiceHealthChanged"),
            "consumes": ("PbcDeployed", "AccessPolicyChanged"),
            "template": None,
        },
        "schema_registry": {
            "label": "Schema Registry and Contract Validation",
            "mesh": "platform",
            "description": "Synchronous and asynchronous contract validation with compatibility gates.",
            "tables": ("schema_subject", "schema_version", "compatibility_rule", "contract_violation"),
            "apis": ("POST /schemas", "POST /compatibility-checks", "GET /subjects"),
            "emits": ("SchemaAccepted", "BreakingSchemaBlocked"),
            "consumes": ("PbcDeployed", "EventContractProposed"),
            "template": None,
        },
        "workflow_orchestration": {
            "label": "Distributed Workflow Orchestration Engine",
            "mesh": "platform",
            "description": "Visual state-machine orchestration, sagas, timers, retries, and compensation.",
            "tables": ("workflow_definition", "workflow_instance", "saga_step", "timer_task"),
            "apis": ("POST /workflows", "POST /instances", "POST /signals"),
            "emits": ("WorkflowStarted", "SagaCompensated", "WorkflowCompleted"),
            "consumes": ("InvoiceApproved", "OrderVerified", "ShipmentDelivered"),
            "template": None,
        },
        "audit_ledger": {
            "label": "Unified Audit Trail and Cryptographic Ledger",
            "mesh": "platform",
            "description": "Append-only signed mutation, security, and user-action evidence.",
            "tables": ("audit_event", "signature_chain", "retention_policy", "forensic_export"),
            "apis": ("POST /audit-events", "GET /signature-chain", "POST /exports"),
            "emits": ("AuditEventSealed", "ForensicExportPrepared"),
            "consumes": ("AccessPolicyChanged", "WorkflowCompleted", "RoutePublished"),
            "template": None,
        },
        "composition_engine": {
            "label": "Low-Code Composition Engine",
            "mesh": "platform",
            "description": "Drag-and-drop PBC assembly, component registry, layout engine, and experience composition.",
            "tables": ("composition_workspace", "ui_fragment", "component_registry", "layout_binding"),
            "apis": ("POST /compositions", "POST /fragments", "GET /component-registry"),
            "emits": ("CompositionPublished", "PbcDeployed"),
            "consumes": ("SchemaAccepted", "RoutePublished"),
            "template": None,
        },
        "global_inventory_visibility": {
            "label": "Global Inventory Visibility and Pool Management",
            "mesh": "commerce",
            "description": "Unified availability across locations, in-transit cargo, vendors, and third-party logistics.",
            "tables": ("inventory_pool", "inventory_projection", "supply_node", "availability_snapshot"),
            "apis": ("GET /global-availability", "POST /pool-rules", "GET /supply-nodes"),
            "emits": ("AvailabilityProjected", "InventoryPoolChanged"),
            "consumes": ("GoodsReceiptPosted", "ShipmentDelivered", "InventoryAllocated"),
            "template": "inventory",
        },
        "order_routing_optimization": {
            "label": "Distributed Order Routing and Optimization",
            "mesh": "commerce",
            "description": "Fulfillment route optimization by distance, cost, tax, and node capacity.",
            "tables": ("routing_rule", "route_candidate", "capacity_snapshot", "routing_decision"),
            "apis": ("POST /route-orders", "GET /route-candidates", "POST /capacity"),
            "emits": ("FulfillmentRouteSelected", "NodeCapacityReserved"),
            "consumes": ("OrderVerified", "AvailabilityProjected", "TaxCalculated"),
            "template": "sales",
        },
        "checkout_processing": {
            "label": "Headless Cart and Checkout Processing",
            "mesh": "commerce",
            "description": "Cart state, pricing, promotions, coupons, and checkout persistence.",
            "tables": ("cart", "cart_line", "checkout_session", "promotion_redemption"),
            "apis": ("POST /carts", "POST /checkout", "POST /coupons"),
            "emits": ("OrderPriced", "CheckoutCompleted"),
            "consumes": ("ProductPublished", "PriceOptimized", "TaxCalculated"),
            "template": "sales",
        },
        "payment_orchestration": {
            "label": "Multi-Gateway Payment Orchestration",
            "mesh": "commerce",
            "description": "Gateway routing, fee optimization, localized checks, and payment token controls.",
            "tables": ("payment_gateway", "payment_intent", "payment_token", "fraud_check"),
            "apis": ("POST /payment-intents", "POST /gateway-routes", "POST /tokens"),
            "emits": ("PaymentCaptured", "PaymentFailed", "FraudCheckRequested"),
            "consumes": ("CheckoutCompleted", "FraudRiskScored"),
            "template": None,
        },
        "subscription_billing": {
            "label": "Subscription and Recurring Billing Management",
            "mesh": "commerce",
            "description": "Subscriptions, metering, dunning, renewals, and deferred revenue support.",
            "tables": ("subscription", "usage_meter", "billing_schedule", "dunning_notice"),
            "apis": ("POST /subscriptions", "POST /usage", "POST /renewals"),
            "emits": ("SubscriptionRenewed", "UsageRated", "InvoiceApproved"),
            "consumes": ("PaymentCaptured", "PriceOptimized"),
            "template": "invoicing",
        },
        "returns_reverse_logistics": {
            "label": "Returns RMA and Reverse Logistics",
            "mesh": "commerce",
            "description": "Return authorizations, labels, inspection grading, and credit adjustments.",
            "tables": ("return_authorization", "return_label", "inspection_grade", "credit_adjustment"),
            "apis": ("POST /returns", "POST /labels", "POST /inspection-grades"),
            "emits": ("ReturnAuthorized", "CreditAdjustmentIssued"),
            "consumes": ("OrderShipped", "PaymentCaptured"),
            "template": None,
        },
        "cross_border_trade": {
            "label": "Cross-Border Trade and Customs Compliance",
            "mesh": "commerce",
            "description": "HS code assignment, landed cost, export controls, and customs declarations.",
            "tables": ("hs_classification", "landed_cost_quote", "export_control_check", "customs_declaration"),
            "apis": ("POST /landed-cost", "POST /export-checks", "POST /declarations"),
            "emits": ("CustomsDeclarationPrepared", "LandedCostCalculated"),
            "consumes": ("ProductClassified", "OrderPriced"),
            "template": None,
        },
        "enterprise_pim": {
            "label": "Enterprise Product Information Management",
            "mesh": "content",
            "description": "Taxonomies, multilingual attributes, inheritance, localization, and validation.",
            "tables": ("product_taxonomy", "product_attribute", "localized_content", "validation_workflow"),
            "apis": ("POST /taxonomies", "POST /attributes", "POST /localized-content"),
            "emits": ("ProductClassified", "ProductPublished"),
            "consumes": ("SchemaAccepted",),
            "template": "crm",
        },
        "dam_core": {
            "label": "Digital Asset Management Core",
            "mesh": "content",
            "description": "Media storage, transformation, transcoding, metadata tagging, and rights controls.",
            "tables": ("asset", "asset_rendition", "rights_policy", "metadata_tag"),
            "apis": ("POST /assets", "POST /renditions", "GET /rights"),
            "emits": ("AssetPublished", "RightsPolicyChanged"),
            "consumes": ("ProductPublished",),
            "template": None,
        },
        "price_promotion_engine": {
            "label": "Dynamic Price Optimization and Promotion Engine",
            "mesh": "content",
            "description": "Context pricing, loyalty tiers, volume breaks, demand signals, and promotions.",
            "tables": ("price_rule", "promotion", "loyalty_tier", "price_decision"),
            "apis": ("POST /price-quotes", "POST /promotions", "GET /price-decisions"),
            "emits": ("PriceOptimized", "PromotionApplied"),
            "consumes": ("CustomerSegmentUpdated", "ForecastUpdated"),
            "template": None,
        },
        "lead_opportunity": {
            "label": "Enterprise Lead and Opportunity Management",
            "mesh": "relationship",
            "description": "Pipeline, deal velocity, account hierarchy, and interaction history.",
            "tables": ("lead", "opportunity", "account_hierarchy", "sales_activity"),
            "apis": ("POST /leads", "POST /opportunities", "GET /pipeline"),
            "emits": ("OpportunityWon", "CustomerUpdated"),
            "consumes": ("CustomerSegmentUpdated",),
            "template": "crm",
        },
        "service_ticketing": {
            "label": "Customer Service Ticketing and SLA Orchestration",
            "mesh": "relationship",
            "description": "Multi-channel support, routing, escalation, and SLA tracking.",
            "tables": ("support_ticket", "sla_policy", "case_assignment", "escalation_event"),
            "apis": ("POST /tickets", "POST /assignments", "GET /sla-status"),
            "emits": ("SupportCaseOpened", "SlaBreached"),
            "consumes": ("CustomerUpdated", "PreferenceChanged"),
            "template": None,
        },
        "notifications": {
            "label": "Omni-Channel Communication and Notifications",
            "mesh": "relationship",
            "description": "SMS, email, chat, push, preferences, templates, and delivery abstractions.",
            "tables": ("notification_template", "delivery_channel", "message_delivery", "preference_snapshot"),
            "apis": ("POST /messages", "POST /templates", "GET /delivery-status"),
            "emits": ("MessageDelivered", "MessageFailed"),
            "consumes": ("PreferenceChanged", "SlaBreached", "WorkflowCompleted"),
            "template": None,
        },
        "cdp_segmentation": {
            "label": "Customer Data Platform Segmentation",
            "mesh": "relationship",
            "description": "Clickstream, transactions, profiles, and real-time segment activation.",
            "tables": ("customer_event", "segment_definition", "segment_membership", "profile_property"),
            "apis": ("POST /events", "POST /segments", "GET /memberships"),
            "emits": ("CustomerSegmentUpdated", "ProfileEnriched"),
            "consumes": ("CustomerUpdated", "PaymentCaptured", "OrderShipped"),
            "template": "crm",
        },
        "loyalty_rewards": {
            "label": "Customer Loyalty Points and Rewards",
            "mesh": "relationship",
            "description": "Rewards, tiers, point balances, earning rules, and redemption validation.",
            "tables": ("reward_account", "points_ledger", "earning_rule", "redemption"),
            "apis": ("POST /points", "POST /redemptions", "GET /reward-accounts"),
            "emits": ("RewardBalanceChanged", "CustomerSegmentUpdated"),
            "consumes": ("PaymentCaptured", "PromotionApplied"),
            "template": None,
        },
        "streaming_analytics": {
            "label": "Streaming Analytics and Real-Time Aggregation",
            "mesh": "intelligence",
            "description": "Windowed metrics, counts, KPI state, and operational dashboard models.",
            "tables": ("metric_stream", "aggregation_window", "kpi_snapshot", "dashboard_projection"),
            "apis": ("POST /metric-streams", "GET /kpis", "GET /projections"),
            "emits": ("ForecastUpdated", "OperationalKpiChanged"),
            "consumes": ("AuditEventSealed", "OrderShipped", "PaymentCaptured"),
            "template": "reporting",
        },
        "enterprise_search_vector": {
            "label": "Enterprise Search and Vector Discovery",
            "mesh": "intelligence",
            "description": "Semantic search across products, customers, transactions, and knowledge sources.",
            "tables": ("search_index", "embedding_job", "vector_document", "query_trace"),
            "apis": ("POST /indexes", "POST /embeddings", "POST /search"),
            "emits": ("SearchIndexUpdated", "DiscoveryInsightGenerated"),
            "consumes": ("ProductPublished", "CustomerUpdated", "AuditEventSealed"),
            "template": None,
        },
        "predictive_demand": {
            "label": "Predictive Demand Forecasting",
            "mesh": "intelligence",
            "description": "Time-series prediction for demand, depletion, cash flow, and resource constraints.",
            "tables": ("forecast_model", "forecast_run", "demand_signal", "forecast_result"),
            "apis": ("POST /forecast-runs", "GET /forecast-results", "POST /signals"),
            "emits": ("ForecastUpdated", "MaterialShortageDetected"),
            "consumes": ("OperationalKpiChanged", "OrderShipped", "InventoryPoolChanged"),
            "template": None,
        },
        "fraud_anomaly_detection": {
            "label": "Anomalous Activity and Fraud Detection",
            "mesh": "intelligence",
            "description": "Behavior baselines, anomaly scores, fraud checks, and operational risk flags.",
            "tables": ("risk_signal", "anomaly_score", "fraud_rule", "risk_case"),
            "apis": ("POST /risk-events", "POST /fraud-checks", "GET /risk-cases"),
            "emits": ("FraudRiskScored", "RiskCaseOpened"),
            "consumes": ("CheckoutCompleted", "PaymentCaptured", "AccessPolicyChanged"),
            "template": None,
        },
    }
)


PBC_STARTER_STACKS = {
    "finance_mesh": ("gl_core", "ap_automation", "ar_credit", "treasury_cash", "tax_localization"),
    "distribution_mesh": ("inventory_positioning", "wms_core", "transportation_management", "dom"),
    "people_mesh": ("personnel_identity", "time_labor", "payroll_engine", "talent_onboarding"),
    "manufacturing_mesh": ("mrp_engine", "production_control", "quality_assurance", "eam"),
    "customer_order_mesh": ("customer_360", "product_catalog_pim", "dom", "ar_credit", "tax_localization"),
    "enterprise_core": ("gl_core", "ap_automation", "ar_credit", "inventory_positioning", "personnel_identity", "dom"),
    "application_composition_platform": (
        "federated_iam",
        "api_gateway_mesh",
        "schema_registry",
        "workflow_orchestration",
        "audit_ledger",
        "composition_engine",
    ),
    "digital_commerce_platform": (
        "checkout_processing",
        "payment_orchestration",
        "order_routing_optimization",
        "global_inventory_visibility",
        "returns_reverse_logistics",
        "cross_border_trade",
    ),
    "customer_intelligence_platform": (
        "customer_360",
        "cdp_segmentation",
        "loyalty_rewards",
        "streaming_analytics",
        "enterprise_search_vector",
        "fraud_anomaly_detection",
    ),
}


def pbc_mesh_catalog() -> tuple[dict, ...]:
    """Return enterprise mesh groups with catalog counts."""
    return tuple(
        {
            "mesh": key,
            **value,
            "pbc_count": sum(1 for item in PBC_CATALOG.values() if item["mesh"] == key),
        }
        for key, value in PBC_MESHES.items()
    )


def pbc_catalog(mesh: str | None = None) -> tuple[dict, ...]:
    """Return selectable PBC descriptors for the IDE catalog."""
    selected = tuple(
        (key, value)
        for key, value in PBC_CATALOG.items()
        if mesh is None or value["mesh"] == mesh
    )
    return tuple(_pbc_descriptor(key, value) for key, value in selected)


def pbc_starter_stacks() -> tuple[dict, ...]:
    """Return recommended multi-PBC stacks users can select as app starters."""
    return tuple(
        {
            "stack": name,
            "pbcs": pbcs,
            "meshes": tuple(sorted({PBC_CATALOG[key]["mesh"] for key in pbcs})),
        }
        for name, pbcs in PBC_STARTER_STACKS.items()
    )


def acp_stream_processor_catalog() -> tuple[dict, ...]:
    """Return supported Python-native stream/event processing profiles."""
    return tuple(
        {
            "processor": key,
            **value,
        }
        for key, value in ACP_STREAM_PROCESSORS.items()
    )


def acp_stream_processing_policy() -> dict:
    """Return the platform's opinionated stream-processing choice policy."""
    return {
        "format": "appgen.acp-stream-processing-policy.v1",
        "ok": True,
        "default": ACP_STREAM_PROCESSING_POLICY["default"],
        "allowed_processors": ACP_STREAM_PROCESSING_POLICY["allowed_processors"],
        "developer_guidance": ACP_STREAM_PROCESSING_POLICY["developer_guidance"],
        "developer_guidance_contract": ACP_STREAM_PROCESSING_POLICY["developer_guidance_contract"],
        "developer_action_contract": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"],
        "developer_use_card": ACP_STREAM_PROCESSING_POLICY["developer_use_card"],
        "developer_decision_brief": ACP_STREAM_PROCESSING_POLICY["developer_decision_brief"],
        "developer_implementation_playbook": ACP_STREAM_PROCESSING_POLICY["developer_implementation_playbook"],
        "decision_card": ACP_STREAM_PROCESSING_POLICY["decision_card"],
        "developer_choice_lock": ACP_STREAM_PROCESSING_POLICY["developer_choice_lock"],
        "developer_decision_record": ACP_STREAM_PROCESSING_POLICY["developer_decision_record"],
        "developer_choice_algorithm": ACP_STREAM_PROCESSING_POLICY["developer_choice_algorithm"],
        "developer_use_policy": ACP_STREAM_PROCESSING_POLICY["developer_use_policy"],
        "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
        "ordinary_workload_contract": ACP_STREAM_PROCESSING_POLICY["ordinary_workload_contract"],
        "developer_default_stack": ACP_STREAM_PROCESSING_POLICY["developer_default_stack"],
        "developer_recommendation_card": ACP_STREAM_PROCESSING_POLICY["developer_recommendation_card"],
        "developer_rule": ACP_STREAM_PROCESSING_POLICY["developer_rule"],
        "generation_rule": ACP_STREAM_PROCESSING_POLICY["generation_rule"],
        "implementation_directive": ACP_STREAM_PROCESSING_POLICY["implementation_directive"],
        "opinionated_stack": ACP_STREAM_PROCESSING_POLICY["opinionated_stack"],
        "generator_outputs": ACP_STREAM_PROCESSING_POLICY["generator_outputs"],
        "decision_ladder": ACP_STREAM_PROCESSING_POLICY["decision_ladder"],
        "workload_defaults": ACP_STREAM_PROCESSING_POLICY["workload_defaults"],
        "exception_prompts": ACP_STREAM_PROCESSING_POLICY["exception_prompts"],
        "exception_required_evidence": ACP_STREAM_PROCESSING_POLICY["exception_required_evidence"],
        "prohibited": ACP_STREAM_PROCESSING_POLICY["prohibited"],
        "decision_tree": ACP_STREAM_PROCESSING_POLICY["decision_tree"],
        "profiles": acp_stream_processor_catalog(),
        "rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
    }


def acp_event_processing_developer_guidance() -> dict:
    """Return the one-answer event-processing guidance for app developers."""
    contract = ACP_STREAM_PROCESSING_POLICY["developer_guidance_contract"]
    return {
        "format": "appgen.acp-event-processing-developer-guidance.v1",
        "ok": True,
        **contract,
        "developer_action_contract": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"],
        "developer_use_card": ACP_STREAM_PROCESSING_POLICY["developer_use_card"],
        "decision_brief": ACP_STREAM_PROCESSING_POLICY["developer_decision_brief"],
        "implementation_playbook": ACP_STREAM_PROCESSING_POLICY["developer_implementation_playbook"],
        "choice_lock": ACP_STREAM_PROCESSING_POLICY["developer_choice_lock"],
        "developer_default_stack": ACP_STREAM_PROCESSING_POLICY["developer_default_stack"],
        "developer_recommendation_card": ACP_STREAM_PROCESSING_POLICY["developer_recommendation_card"],
        "policy_format": acp_stream_processing_policy()["format"],
        "default_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
    }


def lint_pbc_eventing_choice(manifest: dict, *, generated_imports: tuple[str, ...] = ()) -> dict:
    """Lint the developer-facing PBC eventing choice before generation."""
    validation = validate_pbc_manifest(manifest, existing_catalog={})
    stream_processor = manifest.get("stream_processor")
    exception_profiles = set(ACP_STREAM_PROCESSING_POLICY["developer_guidance_contract"]["exception_options"])
    forbidden_imports = ACP_STREAM_PROCESSING_POLICY["ordinary_workload_contract"]["forbidden_imports"]
    diagnostics = []
    quick_fixes = []
    if stream_processor == ACP_DEFAULT_STREAM_PROCESSOR:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "ordinary_pbc_manifest_omits_stream_processor",
                "message": "Ordinary PBC manifests must omit stream_processor; the platform records the default profile as read-only metadata.",
            }
        )
        quick_fixes.append(
            {
                "id": "remove_stream_processor",
                "field": "stream_processor",
                "replacement": None,
            }
        )
    elif stream_processor and stream_processor not in exception_profiles:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "unsupported_stream_processor",
                "message": "Use appgen_event_contract for ordinary work; only audited exception profiles are accepted.",
            }
        )
    elif stream_processor in exception_profiles and validation["missing_stream_exception_evidence"]:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "exception_profiles_require_stream_exception_evidence",
                "message": (
                    "Exception profiles require workload_name, throughput_or_latency_reason, "
                    "state_shape, and operational_owner."
                ),
            }
        )
    import_violations = tuple(
        module
        for module in generated_imports
        if module.split(".", 1)[0] in forbidden_imports
    )
    if import_violations:
        diagnostics.append(
            {
                "severity": "error",
                "rule": "generated_business_logic_imports_appgen_event_adapter_only",
                "message": "Generated business logic must import the AppGen-X event adapter, not profile-specific stream libraries.",
                "imports": import_violations,
            }
        )
    normal_form = dict(manifest)
    if not stream_processor or stream_processor == ACP_DEFAULT_STREAM_PROCESSOR:
        normal_form.pop("stream_processor", None)
    return {
        "format": "appgen.pbc-eventing-choice-lint.v1",
        "ok": validation["ok"] and not diagnostics,
        "developer_answer": "Use appgen_event_contract.",
        "ordinary_manifest_rule": "omit_stream_processor",
        "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
        "decision_ladder": ACP_STREAM_PROCESSING_POLICY["decision_ladder"],
        "choice_lock": ACP_STREAM_PROCESSING_POLICY["developer_choice_lock"],
        "validation": validation,
        "diagnostics": tuple(diagnostics),
        "quick_fixes": tuple(quick_fixes),
        "normal_form_manifest": normal_form,
        "generated_imports": generated_imports,
    }


def select_acp_stream_processor(workload: str) -> dict:
    """Select the platform-owned runtime profile for an APC workload description."""
    text = workload.lower().replace("-", "_")
    if any(term in text for term in ("time_series", "telemetry", "high_throughput", "event_data", "ingestion")):
        selected = "quix_streams"
    elif any(term in text for term in ("parallel", "dataflow", "transform", "pipeline")):
        selected = "bytewax"
    else:
        selected = ACP_DEFAULT_STREAM_PROCESSOR
    profile = ACP_STREAM_PROCESSORS[selected]
    return {
        "format": "appgen.acp-stream-processor-selection.v1",
        "ok": True,
        "workload": workload,
        "selected": selected,
        "default": ACP_DEFAULT_STREAM_PROCESSOR,
        "decision": "default" if selected == ACP_DEFAULT_STREAM_PROCESSOR else "exception",
        "profile": {"processor": selected, **profile},
        "reason": profile["primary_use_case"],
        "rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
        "developer_visible": False,
        "selection_owner": "platform_runtime",
        "ordinary_generator_api": "resolve_acp_event_processing_choice",
        "ordinary_developer_answer": "Use appgen_event_contract.",
    }


def resolve_acp_event_processing_choice(workload: str, *, has_stream_exception_evidence: bool = False) -> dict:
    """Return the developer-facing event-processing action for generation."""
    candidate = select_acp_stream_processor(workload)
    is_exception_candidate = candidate["decision"] == "exception"
    exception_allowed = is_exception_candidate and has_stream_exception_evidence
    if exception_allowed:
        selected_profile = candidate["selected"]
        return {
            "format": "appgen.acp-event-processing-choice-resolution.v1",
            "ok": True,
            "workload": workload,
            "action": "generate_exception_pbc",
            "developer_answer": f"Use the {selected_profile} exception profile only for this split specialized PBC.",
            "public_contract": "specialized_exception_pbc",
            "manifest_rule": f"stream_processor={selected_profile}",
            "selected_runtime_profile": selected_profile,
            "candidate_profile": selected_profile,
            "requires_stream_exception_evidence": True,
            "missing_stream_exception_evidence": False,
            "must_split_workload": True,
            "developer_visible_options": ("appgen_event_contract",),
            "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
            "do_not_compare_runtimes": True,
            "generated_business_logic_import_rule": "appgen_event_adapter_only",
            "api_call_order": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"]["api_call_order"],
            "stream_selector_exposed_to_developer": False,
        }
    action = "fallback_to_appgen_event_contract" if is_exception_candidate else "generate_appgen_event_contract"
    return {
        "format": "appgen.acp-event-processing-choice-resolution.v1",
        "ok": True,
        "workload": workload,
        "action": action,
        "developer_answer": "Use appgen_event_contract.",
        "public_contract": "appgen_event_contract",
        "manifest_rule": "omit_stream_processor",
        "selected_runtime_profile": ACP_DEFAULT_STREAM_PROCESSOR,
        "candidate_profile": candidate["selected"],
        "blocked_exception_profile": candidate["selected"] if is_exception_candidate else None,
        "requires_stream_exception_evidence": is_exception_candidate,
        "missing_stream_exception_evidence": is_exception_candidate,
        "must_split_workload": False,
        "developer_visible_options": ("appgen_event_contract",),
        "choice_budget": ACP_STREAM_PROCESSING_POLICY["choice_budget"],
        "do_not_compare_runtimes": True,
        "generated_business_logic_import_rule": "appgen_event_adapter_only",
        "api_call_order": ACP_STREAM_PROCESSING_POLICY["developer_action_contract"]["api_call_order"],
        "stream_selector_exposed_to_developer": False,
    }


def pbc_manifest_schema() -> dict:
    """Return the contract every self-registering PBC package must implement."""
    return {
        "format": "appgen.pbc-manifest-schema.v1",
        "required_fields": PBC_MANIFEST_REQUIRED_FIELDS,
        "optional_fields": PBC_MANIFEST_OPTIONAL_FIELDS,
        "field_contracts": {
            "pbc": "Stable lowercase snake_case key. Used in routes, datastore, topics, and generated tables.",
            "label": "Human-facing catalog label.",
            "mesh": f"One of: {', '.join(sorted(PBC_MESHES))}.",
            "description": "One-sentence bounded-context purpose.",
            "datastore_backend": (
                "One of the approved open-source datastore backends: "
                + ", ".join(PBC_ALLOWED_DATASTORE_BACKENDS)
                + "."
            ),
            "tables": "Tuple of owned table names. Do not list tables owned by another PBC.",
            "apis": "Tuple of command/query route contracts, for example POST /orders.",
            "emits": "Tuple of domain events emitted by this PBC.",
            "consumes": "Tuple of domain events consumed from other PBCs or external systems.",
            "template": "Optional ERP template bridge key.",
            "stream_processor": (
                "Optional event processing backend key. One of: "
                + ", ".join(sorted(ACP_STREAM_PROCESSORS))
                + "."
            ),
            "stream_exception_evidence": (
                "Required only when stream_processor is an exception profile. "
                "Must include workload_name, throughput_or_latency_reason, "
                "state_shape, and operational_owner."
            ),
            "ui_fragments": "Optional generated UI fragment descriptors for the composition canvas.",
            "permissions": "Optional RBAC/ABAC permission strings exposed by the PBC.",
            "configuration": "Optional environment/configuration keys required at install time.",
            "migrations": "Optional migration artifact paths owned by the PBC package.",
            "seed_data": "Optional seed artifact paths owned by the PBC package.",
            "tests": "Optional test artifact paths that prove the PBC package contract.",
            "docs": "Optional documentation artifact paths for builders and operators.",
        },
        "self_registration_entrypoint": "register_pbc() -> dict",
        "stream_processing_policy": acp_stream_processing_policy(),
        "registration_rules": (
            "Return a manifest matching this schema.",
            "Never share a datastore key with another PBC.",
            "Expose at least one API, one emitted event, and one owned table.",
            "Use event contracts for cross-PBC integration.",
            "Include tests and docs before publishing a reusable PBC package.",
        ),
    }


def validate_pbc_manifest(manifest: dict, *, existing_catalog: dict[str, dict] | None = None) -> dict:
    """Validate one PBC manifest before catalog registration."""
    catalog = existing_catalog if existing_catalog is not None else PBC_CATALOG
    missing = tuple(field for field in PBC_MANIFEST_REQUIRED_FIELDS if not manifest.get(field))
    key = manifest.get("pbc")
    mesh = manifest.get("mesh")
    invalid = []
    if key and not re.fullmatch(r"[a-z][a-z0-9_]*", str(key)):
        invalid.append("pbc must be lowercase snake_case")
    if mesh and mesh not in PBC_MESHES:
        invalid.append(f"mesh must be one of {', '.join(sorted(PBC_MESHES))}")
    backend = manifest.get("datastore_backend")
    if backend and backend not in PBC_ALLOWED_DATASTORE_BACKENDS:
        invalid.append(
            "datastore_backend must be one of "
            + ", ".join(PBC_ALLOWED_DATASTORE_BACKENDS)
        )
    stream_processor = manifest.get("stream_processor")
    if stream_processor and stream_processor not in ACP_STREAM_PROCESSORS:
        invalid.append(
            "stream_processor must be one of "
            + ", ".join(sorted(ACP_STREAM_PROCESSORS))
        )
    normalized_stream_processor = stream_processor or ACP_DEFAULT_STREAM_PROCESSOR
    exception_required = normalized_stream_processor != ACP_DEFAULT_STREAM_PROCESSOR
    evidence = manifest.get("stream_exception_evidence", {})
    if exception_required:
        if not isinstance(evidence, dict):
            invalid.append("stream_exception_evidence must be an object for exception stream processors")
            missing_exception_evidence = ACP_STREAM_PROCESSING_POLICY["exception_required_evidence"]
        else:
            missing_exception_evidence = tuple(
                field
                for field in ACP_STREAM_PROCESSING_POLICY["exception_required_evidence"]
                if not evidence.get(field)
            )
            if missing_exception_evidence:
                invalid.append(
                    "stream_exception_evidence missing required fields: "
                    + ", ".join(missing_exception_evidence)
                )
    else:
        missing_exception_evidence = ()
    if key and key in catalog:
        invalid.append(f"pbc key already registered: {key}")
    for field in ("tables", "apis", "emits", "consumes"):
        value = manifest.get(field, ())
        if value and (not isinstance(value, (tuple, list)) or not all(isinstance(item, str) and item for item in value)):
            invalid.append(f"{field} must be a tuple/list of strings")
    datastore = f"{key}_store" if key else None
    existing_datastores = {f"{name}_store" for name in catalog}
    if datastore and datastore in existing_datastores:
        invalid.append(f"datastore already exists: {datastore}")
    required_artifacts = ("tests", "docs")
    missing_publish_artifacts = tuple(field for field in required_artifacts if not manifest.get(field))
    return {
        "format": "appgen.pbc-manifest-validation.v1",
        "ok": not missing and not invalid,
        "publishable": not missing and not invalid and not missing_publish_artifacts,
        "manifest": manifest,
        "missing_fields": missing,
        "invalid": tuple(invalid),
        "stream_processor_decision": "default" if not exception_required else "exception",
        "missing_stream_exception_evidence": missing_exception_evidence,
        "missing_publish_artifacts": missing_publish_artifacts,
        "datastore": datastore,
        "normalized_descriptor": _pbc_descriptor_from_manifest(manifest) if not missing and not invalid else None,
    }


def register_pbc_manifest(manifest: dict, *, existing_catalog: dict[str, dict] | None = None) -> dict:
    """Return a side-effect-free self-registration plan for a PBC package."""
    validation = validate_pbc_manifest(manifest, existing_catalog=existing_catalog)
    if not validation["ok"]:
        return {
            "format": "appgen.pbc-registration-plan.v1",
            "ok": False,
            "decision": "blocked",
            "validation": validation,
            "catalog_patch": None,
            "next_actions": ("Fix manifest validation errors before registering.",),
        }
    descriptor = validation["normalized_descriptor"]
    return {
        "format": "appgen.pbc-registration-plan.v1",
        "ok": True,
        "decision": "approved" if validation["publishable"] else "draft",
        "validation": validation,
        "catalog_patch": {
            descriptor["pbc"]: {
                "label": descriptor["label"],
                "mesh": descriptor["mesh"],
                "description": descriptor["description"],
                "tables": descriptor["tables"],
                "datastore_backend": descriptor["datastore_backend"],
                "stream_processor": descriptor["stream_processor"],
                "stream_exception_evidence": descriptor["stream_exception_evidence"],
                "apis": descriptor["apis"],
                "emits": descriptor["emits"],
                "consumes": descriptor["consumes"],
                "template": descriptor["template"],
            }
        },
        "registration_steps": (
            "Load package register_pbc() entrypoint.",
            "Validate returned manifest.",
            "Add descriptor to the catalog registry.",
            "Expose API routes, event topics, UI fragments, permissions, docs, and tests.",
            "Run pbc_release_audit() before publishing.",
        ),
        "next_actions": ()
        if validation["publishable"]
        else ("Add tests and docs before publishing as a reusable PBC.",),
    }


def pbc_package_contract(package_name: str, manifest: dict) -> dict:
    """Return the installable package contract for a third-party PBC."""
    registration = register_pbc_manifest(manifest)
    descriptor = registration["validation"].get("normalized_descriptor")
    return {
        "format": "appgen.pbc-package-contract.v1",
        "ok": registration["ok"],
        "package": package_name,
        "entrypoint": f"{package_name}:register_pbc",
        "registration": registration,
        "descriptor": descriptor,
        "install_surfaces": (
            "catalog",
            "datastore",
            "api_routes",
            "event_topics",
            "ui_fragments",
            "permissions",
            "configuration",
            "docs",
            "tests",
        ),
        "usable": registration["ok"] and descriptor is not None,
    }


def load_pbc_package(package_ref: str | Path, *, existing_catalog: dict[str, dict] | None = None) -> dict:
    """Load a PBC package entrypoint from an importable module or local path."""
    ref = Path(package_ref) if not isinstance(package_ref, Path) else package_ref
    source_kind = "module"
    entrypoint = str(package_ref)
    try:
        if ref.exists():
            source_kind = "directory" if ref.is_dir() else "file"
            entry_file = ref / "__init__.py" if ref.is_dir() else ref
            if not entry_file.exists():
                return {
                    "format": "appgen.pbc-package-load-report.v1",
                    "ok": False,
                    "source": str(package_ref),
                    "source_kind": source_kind,
                    "error": f"missing entry file: {entry_file}",
                }
            module_name = f"appgen_pbc_package_{abs(hash(str(entry_file.resolve())))}"
            spec = importlib.util.spec_from_file_location(module_name, entry_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"cannot create import spec for {entry_file}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            entrypoint = f"{entry_file}:register_pbc"
        else:
            module = importlib.import_module(str(package_ref))
            entrypoint = f"{package_ref}:register_pbc"
        register = getattr(module, "register_pbc", None)
        if not callable(register):
            return {
                "format": "appgen.pbc-package-load-report.v1",
                "ok": False,
                "source": str(package_ref),
                "source_kind": source_kind,
                "entrypoint": entrypoint,
                "error": "register_pbc entrypoint is missing or not callable",
            }
        manifest = register()
        if not isinstance(manifest, dict):
            return {
                "format": "appgen.pbc-package-load-report.v1",
                "ok": False,
                "source": str(package_ref),
                "source_kind": source_kind,
                "entrypoint": entrypoint,
                "error": "register_pbc must return a manifest dict",
            }
        registration = register_pbc_manifest(manifest, existing_catalog=existing_catalog)
        contract = pbc_package_contract(str(package_ref), manifest)
        return {
            "format": "appgen.pbc-package-load-report.v1",
            "ok": registration["ok"],
            "source": str(package_ref),
            "source_kind": source_kind,
            "entrypoint": entrypoint,
            "manifest": manifest,
            "registration": registration,
            "contract": contract,
            "descriptor": registration["validation"].get("normalized_descriptor"),
        }
    except Exception as exc:  # pragma: no cover - surfaced in returned report
        return {
            "format": "appgen.pbc-package-load-report.v1",
            "ok": False,
            "source": str(package_ref),
            "source_kind": source_kind,
            "entrypoint": entrypoint,
            "error": str(exc),
        }


def discover_pbc_packages(package_refs: tuple[str | Path, ...] | list[str | Path]) -> dict:
    """Load multiple PBC packages without mutating the built-in catalog."""
    reports = tuple(load_pbc_package(ref) for ref in package_refs)
    return {
        "format": "appgen.pbc-package-discovery-report.v1",
        "ok": all(report["ok"] for report in reports),
        "loaded": reports,
        "catalog_patches": tuple(
            report["registration"]["catalog_patch"]
            for report in reports
            if report.get("registration", {}).get("catalog_patch")
        ),
        "blocking_gaps": tuple(report for report in reports if not report["ok"]),
    }


def pbc_package_index_schema() -> dict:
    """Return the package index contract for reusable PBC packages."""
    return {
        "format": "appgen.pbc-package-index-schema.v1",
        "required_fields": ("packages",),
        "package_fields": {
            "name": "Stable package name shown in the package catalog.",
            "source": "Optional local directory or file path containing register_pbc().",
            "module": "Optional importable module path exposing register_pbc().",
            "version": "Optional semantic package version.",
            "publisher": "Optional package publisher or owning team.",
        },
        "rules": (
            "Each package entry must provide either source or module.",
            "Relative source paths resolve from the index file directory.",
            "Loading an index returns validation reports and catalog patches without mutating the built-in catalog.",
        ),
    }


def discover_pbc_package_index(index_path: str | Path) -> dict:
    """Load a package index file and validate each referenced PBC package."""
    path = Path(index_path)
    try:
        index = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "format": "appgen.pbc-package-index-discovery-report.v1",
            "ok": False,
            "index": str(index_path),
            "schema": pbc_package_index_schema(),
            "error": str(exc),
            "loaded": (),
            "blocking_gaps": ({"id": "index_read", "ok": False, "error": str(exc)},),
        }
    packages = index.get("packages", ())
    if not isinstance(packages, list):
        return {
            "format": "appgen.pbc-package-index-discovery-report.v1",
            "ok": False,
            "index": str(index_path),
            "schema": pbc_package_index_schema(),
            "error": "packages must be a list",
            "loaded": (),
            "blocking_gaps": ({"id": "packages_list", "ok": False},),
        }
    loaded = []
    invalid_entries = []
    for position, entry in enumerate(packages):
        if not isinstance(entry, dict) or (not entry.get("source") and not entry.get("module")):
            invalid_entries.append({"position": position, "entry": entry, "error": "entry must provide source or module"})
            continue
        raw_ref = entry.get("source") or entry["module"]
        if entry.get("source"):
            candidate = Path(raw_ref)
            package_ref = candidate if candidate.is_absolute() else path.parent / candidate
        else:
            package_ref = raw_ref
        report = load_pbc_package(package_ref)
        loaded.append(
            {
                "name": entry.get("name") or str(raw_ref),
                "version": entry.get("version"),
                "publisher": entry.get("publisher"),
                "source_kind": "source" if entry.get("source") else "module",
                "report": report,
            }
        )
    blocking = tuple(invalid_entries) + tuple(item for item in loaded if not item["report"]["ok"])
    return {
        "format": "appgen.pbc-package-index-discovery-report.v1",
        "ok": not blocking and bool(loaded),
        "index": str(index_path),
        "schema": pbc_package_index_schema(),
        "loaded": tuple(loaded),
        "catalog_patches": tuple(
            item["report"]["registration"]["catalog_patch"]
            for item in loaded
            if item["report"].get("registration", {}).get("catalog_patch")
        ),
        "blocking_gaps": blocking,
    }


def pbc_package_loading_smoke_audit() -> dict:
    """Prove PBC packages can be loaded from local source and import paths."""
    source_manifest = {**example_pbc_manifest(), "pbc": "source_warranty_claims"}
    module_manifest = {**example_pbc_manifest(), "pbc": "module_warranty_claims"}
    with tempfile.TemporaryDirectory(prefix="appgen-pbc-package-load-") as raw_tmp:
        root = Path(raw_tmp)
        source_pkg = root / "source_claims_pbc"
        source_pkg.mkdir()
        source_pkg.joinpath("__init__.py").write_text(
            "def register_pbc():\n"
            f"    return {source_manifest!r}\n",
            encoding="utf-8",
        )
        module_pkg = root / "module_claims_pbc"
        module_pkg.mkdir()
        module_pkg.joinpath("__init__.py").write_text(
            "def register_pbc():\n"
            f"    return {module_manifest!r}\n",
            encoding="utf-8",
        )
        source_report = load_pbc_package(source_pkg)
        sys.path.insert(0, str(root))
        try:
            sys.modules.pop("module_claims_pbc", None)
            module_report = load_pbc_package("module_claims_pbc")
            index_path = root / "pbc-packages.json"
            index_path.write_text(
                json.dumps(
                    {
                        "packages": [
                            {
                                "name": "Source Claims",
                                "source": "source_claims_pbc",
                                "version": "1.0.0",
                                "publisher": "appgen-tests",
                            },
                            {
                                "name": "Module Claims",
                                "module": "module_claims_pbc",
                                "version": "1.0.0",
                                "publisher": "appgen-tests",
                            },
                        ]
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            index_discovery = discover_pbc_package_index(index_path)
        finally:
            try:
                sys.path.remove(str(root))
            except ValueError:
                pass
            sys.modules.pop("module_claims_pbc", None)
        discovery = discover_pbc_packages((source_pkg,))
    checks = (
        {"id": "local_source_directory", "ok": source_report["ok"] and source_report["source_kind"] == "directory"},
        {"id": "importable_module", "ok": module_report["ok"] and module_report["source_kind"] == "module"},
        {"id": "discovery_aggregate", "ok": discovery["ok"] and bool(discovery["catalog_patches"])},
        {"id": "package_index_discovery", "ok": index_discovery["ok"] and len(index_discovery["loaded"]) == 2},
        {
            "id": "side_effect_free_registration",
            "ok": source_report.get("registration", {}).get("decision") == "approved"
            and module_report.get("registration", {}).get("decision") == "approved",
        },
    )
    return {
        "format": "appgen.pbc-package-loading-smoke-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "source_report": source_report,
        "module_report": module_report,
        "discovery": discovery,
        "index_discovery": index_discovery,
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def example_pbc_manifest() -> dict:
    """Return a minimal publishable PBC manifest for documentation and tests."""
    return {
        "pbc": "warranty_claims",
        "label": "Warranty Claims",
        "mesh": "relationship",
        "description": "Manage warranty intake, eligibility, adjudication, and claim resolution.",
        "datastore_backend": "postgresql",
        "stream_processor": "faust_streaming",
        "tables": ("warranty_claim", "claim_line", "eligibility_check"),
        "apis": ("POST /warranty-claims", "POST /eligibility-checks", "GET /claim-status"),
        "emits": ("WarrantyClaimOpened", "WarrantyClaimApproved"),
        "consumes": ("ProductPublished", "CustomerUpdated", "OrderShipped"),
        "template": None,
        "ui_fragments": ("WarrantyClaimsWorkbench", "WarrantyClaimDetail"),
        "permissions": ("warranty_claim.read", "warranty_claim.create", "warranty_claim.approve"),
        "configuration": ("WARRANTY_DEFAULT_REGION",),
        "migrations": ("migrations/001_warranty_claims.sql",),
        "seed_data": ("seed/warranty_reasons.json",),
        "tests": ("tests/test_warranty_claims_contract.py",),
        "docs": ("docs/warranty-claims.md",),
    }


def example_stream_exception_manifest() -> dict:
    """Return a valid PBC manifest that uses a stream-processing exception profile."""
    return {
        **example_pbc_manifest(),
        "pbc": "machine_telemetry",
        "label": "Machine Telemetry",
        "mesh": "opsmfg",
        "description": "Ingest and aggregate equipment telemetry windows.",
        "stream_processor": "quix_streams",
        "tables": ("telemetry_sample", "telemetry_window"),
        "apis": ("POST /telemetry", "GET /telemetry-windows"),
        "emits": ("TelemetryWindowCalculated",),
        "consumes": ("MachineSignalReceived",),
        "stream_exception_evidence": {
            "workload_name": "equipment telemetry windows",
            "throughput_or_latency_reason": "high-volume time-series ingestion with windowed operational metrics",
            "state_shape": "per-machine rolling windows persisted by watermark",
            "operational_owner": "opsmfg telemetry platform team",
        },
        "tests": ("tests/test_machine_telemetry_contract.py",),
        "docs": ("docs/machine-telemetry.md",),
    }


def application_composition_topology() -> dict:
    """Return the ACP runtime topology required for composable apps."""
    layers = (
        {
            "layer": "composed_digital_experience",
            "purpose": "Assemble UI fragments and channel experiences from selected PBCs.",
            "required_pbcs": ("composition_engine",),
        },
        {
            "layer": "composition_layer",
            "purpose": "Coordinate low-code composition, BFF endpoints, GraphQL mesh, and orchestration.",
            "required_pbcs": ("composition_engine", "workflow_orchestration", "federated_iam"),
        },
        {
            "layer": "event_backbone_gateway_fabric",
            "purpose": "Provide routing, service discovery, event contracts, schema compatibility, and audit.",
            "required_pbcs": ("api_gateway_mesh", "schema_registry", "audit_ledger"),
        },
        {
            "layer": "domain_meshes",
            "purpose": "Host independently deployable business capabilities across enterprise domains.",
            "required_meshes": ("finops", "scl", "hcm", "opsmfg", "cx", "commerce", "content", "relationship", "intelligence"),
        },
    )
    return {
        "format": "appgen.application-composition-topology.v1",
        "ok": all(
            set(layer.get("required_pbcs", ())) <= set(PBC_CATALOG)
            and set(layer.get("required_meshes", ())) <= set(PBC_MESHES)
            for layer in layers
        ),
        "layers": layers,
        "runtime_fabric": (
            "low_code_composition",
            "bff_graphql_mesh",
            "event_backbone",
            "python_stream_processor_abstraction",
            "schema_registry",
            "gateway_service_mesh",
            "domain_pbc_meshes",
        ),
        "stream_processors": acp_stream_processor_catalog(),
        "stream_processor_default": ACP_DEFAULT_STREAM_PROCESSOR,
        "stream_processor_rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
    }


def acp_capability_coverage() -> dict:
    """Return coverage evidence for the ACP component catalog."""
    required = {
        "platform": {
            "federated_iam",
            "api_gateway_mesh",
            "schema_registry",
            "workflow_orchestration",
            "audit_ledger",
            "composition_engine",
        },
        "commerce": {
            "global_inventory_visibility",
            "order_routing_optimization",
            "checkout_processing",
            "payment_orchestration",
            "subscription_billing",
            "returns_reverse_logistics",
            "cross_border_trade",
        },
        "content": {"enterprise_pim", "dam_core", "price_promotion_engine"},
        "relationship": {
            "lead_opportunity",
            "service_ticketing",
            "notifications",
            "cdp_segmentation",
            "loyalty_rewards",
        },
        "intelligence": {
            "streaming_analytics",
            "enterprise_search_vector",
            "predictive_demand",
            "fraud_anomaly_detection",
        },
    }
    coverage = tuple(
        {
            "mesh": mesh,
            "required": tuple(sorted(keys)),
            "missing": tuple(sorted(key for key in keys if key not in PBC_CATALOG)),
            "ok": all(key in PBC_CATALOG for key in keys),
        }
        for mesh, keys in required.items()
    )
    return {
        "format": "appgen.acp-capability-coverage.v1",
        "ok": all(item["ok"] for item in coverage),
        "coverage": coverage,
    }


def pbc_selection_from_prompt(prompt: str) -> dict:
    """Resolve a natural-language app request to a composable PBC selection."""
    text = prompt.lower()
    explicit = [
        key
        for key, pbc in PBC_CATALOG.items()
        if key.replace("_", " ") in text
        or pbc["label"].lower() in text
        or any(word in text for word in _selection_terms(key, pbc))
    ]
    if any(term in text for term in ("application composition platform", "acp", "apc")):
        explicit.extend(PBC_STARTER_STACKS["application_composition_platform"])
    for stack, pbcs in PBC_STARTER_STACKS.items():
        if stack.replace("_", " ") in text:
            explicit.extend(pbcs)
    if not explicit and any(term in text for term in ("erp", "enterprise", "back office")):
        explicit.extend(PBC_STARTER_STACKS["enterprise_core"])
    selection = tuple(dict.fromkeys(explicit))
    return {
        "format": "appgen.pbc-natural-language-selection.v1",
        "prompt": prompt,
        "pbcs": selection,
        "matched": bool(selection),
        "composition": pbc_composition_plan(selection, app_name=_app_name_from_prompt(prompt)) if selection else None,
    }


def pbc_composition_plan(
    selected_pbcs: tuple[str, ...] | list[str],
    *,
    app_name: str = "ComposableEnterprise",
    targets: tuple[str, ...] = ("web", "pwa", "mobile", "desktop"),
) -> dict:
    """Return a bounded-context composition plan for selected PBCs."""
    selected = tuple(dict.fromkeys(selected_pbcs))
    missing = tuple(key for key in selected if key not in PBC_CATALOG)
    services = tuple(_service_contract(key) for key in selected if key in PBC_CATALOG)
    emitted = {
        event: service["pbc"]
        for service in services
        for event in service["emits"]
    }
    dependencies = tuple(
        {
            "from": service["pbc"],
            "event": event,
            "provider": emitted.get(event),
            "resolved": emitted.get(event) is not None,
        }
        for service in services
        for event in service["consumes"]
        if emitted.get(event) is not None
    )
    unresolved_external_events = tuple(
        {
            "pbc": service["pbc"],
            "event": event,
            "policy": "external-event-contract",
        }
        for service in services
        for event in service["consumes"]
        if emitted.get(event) is None
    )
    datastores = tuple(service["datastore"] for service in services)
    shared_datastores = tuple(
        datastore for datastore in datastores if datastores.count(datastore) > 1
    )
    return {
        "format": "appgen.pbc-composition-plan.v1",
        "ok": not missing and not shared_datastores and bool(services),
        "app_name": app_name,
        "targets": targets,
        "pbcs": selected,
        "services": services,
        "dependencies": dependencies,
        "external_event_contracts": unresolved_external_events,
        "missing_pbcs": missing,
        "shared_datastores": tuple(dict.fromkeys(shared_datastores)),
        "integration_style": "event-first-with-api-command-surface",
        "deployment_units": tuple(f"services/{service['pbc']}" for service in services),
        "stop_condition": "do-not-compose-pbcs-unless-each-selected-capability-has-an-owned-datastore",
    }


def pbc_composition_dsl(
    selected_pbcs: tuple[str, ...] | list[str],
    *,
    app_name: str = "ComposableEnterprise",
    targets: tuple[str, ...] = ("web", "pwa", "mobile", "desktop"),
) -> str:
    """Render a compact AppGen DSL starter for a selected PBC composition."""
    plan = pbc_composition_plan(tuple(selected_pbcs), app_name=app_name, targets=targets)
    if not plan["ok"]:
        raise ValueError(f"Invalid PBC composition: {plan['missing_pbcs'] or plan['shared_datastores']}")
    lines = [f"app {app_name} {{ targets: {', '.join(targets)} }}"]
    for service in plan["services"]:
        for table in service["tables"][:3]:
            table_name = f"{service['pbc']}_{table}"
            lines.extend(
                (
                    "",
                    f"table {table_name} {{",
                    "  id: int pk",
                    "  code: string required search",
                    "  status: string required",
                    "  updated_at: datetime",
                    "}",
                )
            )
        event_table = f"{service['pbc']}_event_outbox"
        lines.extend(
            (
                "",
                f"table {event_table} {{",
                "  id: int pk",
                "  event_type: string required search",
                "  payload: text required",
                "  published_at: datetime",
                "}",
                "",
                f"view {service['class_name']}Workbench for {event_table} {{",
                "  Main: event_type, payload, published_at",
                "  @ event_type TextBox 0 0 6 1",
                "  @ payload TextArea 0 1 12 3",
                "  @ published_at DateTimePicker 0 4 6 1",
                "}",
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def pbc_release_audit() -> dict:
    """Return package-level proof for composable PBC app generation."""
    sample = PBC_STARTER_STACKS["enterprise_core"]
    composition = pbc_composition_plan(sample, app_name="EnterpriseCore")
    acp_composition = pbc_composition_plan(PBC_STARTER_STACKS["application_composition_platform"], app_name="AppCompositionPlatform")
    topology = application_composition_topology()
    acp_coverage = acp_capability_coverage()
    stream_policy = acp_stream_processing_policy()
    invalid_exception = validate_pbc_manifest(
        {
            **example_pbc_manifest(),
            "pbc": "machine_telemetry_missing_evidence",
            "stream_processor": "quix_streams",
        }
    )
    valid_exception = validate_pbc_manifest(example_stream_exception_manifest())
    ordinary_manifest = dict(example_pbc_manifest())
    ordinary_manifest.pop("stream_processor", None)
    ordinary_eventing_lint = lint_pbc_eventing_choice(ordinary_manifest)
    branching_eventing_lint = lint_pbc_eventing_choice(
        {
            **example_pbc_manifest(),
            "stream_processor": ACP_DEFAULT_STREAM_PROCESSOR,
        },
        generated_imports=("faust_streaming",),
    )
    package_loading = pbc_package_loading_smoke_audit()
    nl_selection = pbc_selection_from_prompt(
        "Build an enterprise ERP back office with GL, AP, AR, inventory, people, and order management"
    )
    smoke = pbc_generation_smoke_audit(sample)
    required_meshes = {"finops", "scl", "hcm", "opsmfg", "cx", "platform", "commerce", "content", "relationship", "intelligence"}
    gates = (
        {
            "id": "catalog_depth",
            "ok": len(PBC_CATALOG) >= 46 and required_meshes <= {item["mesh"] for item in PBC_CATALOG.values()},
            "count": len(PBC_CATALOG),
            "meshes": tuple(sorted({item["mesh"] for item in PBC_CATALOG.values()})),
        },
        {
            "id": "bounded_context_contracts",
            "ok": all(
                item["datastore"]
                and item["datastore_backend"] in PBC_ALLOWED_DATASTORE_BACKENDS
                and item["apis"]
                and item["emits"]
                and item["tables"]
                for item in pbc_catalog()
            ),
        },
        {
            "id": "starter_stacks",
            "ok": {"finance_mesh", "distribution_mesh", "people_mesh", "manufacturing_mesh", "enterprise_core", "application_composition_platform"}
            <= {item["stack"] for item in pbc_starter_stacks()},
        },
        {
            "id": "acp_platform_fabric",
            "ok": topology["ok"]
            and acp_coverage["ok"]
            and acp_composition["ok"]
            and len(acp_composition["services"]) == 6,
            "topology": topology["format"],
            "coverage": acp_coverage["format"],
        },
        {
            "id": "self_registering_pbc_spec",
            "ok": register_pbc_manifest(example_pbc_manifest())["ok"]
            and pbc_package_contract("warranty_claims_pbc", example_pbc_manifest())["usable"],
            "schema": pbc_manifest_schema()["format"],
        },
        {
            "id": "pbc_package_loader",
            "ok": package_loading["ok"],
            "checks": package_loading["checks"],
        },
        {
            "id": "open_source_datastore_backends",
            "ok": all(item["datastore_backend"] in PBC_ALLOWED_DATASTORE_BACKENDS for item in pbc_catalog()),
            "allowed": PBC_ALLOWED_DATASTORE_BACKENDS,
        },
        {
            "id": "stream_processor_abstraction",
            "ok": {
                "bytewax",
                "quix_streams",
                "faust_streaming",
            }
            == {item["processor"] for item in acp_stream_processor_catalog()}
            and ACP_DEFAULT_STREAM_PROCESSOR == "faust_streaming"
            and select_acp_stream_processor("async workflow saga")["selected"] == "faust_streaming"
            and select_acp_stream_processor("high throughput telemetry")["selected"] == "quix_streams"
            and select_acp_stream_processor("parallel transformation pipeline")["selected"] == "bytewax",
            "processors": tuple(item["processor"] for item in acp_stream_processor_catalog()),
            "default": ACP_DEFAULT_STREAM_PROCESSOR,
            "decision_rules": ACP_STREAM_PROCESSOR_DECISION_RULES,
        },
        {
            "id": "opinionated_stream_processing_policy",
            "ok": stream_policy["default"] == "faust_streaming"
            and stream_policy["allowed_processors"] == ("faust_streaming", "quix_streams", "bytewax")
            and stream_policy["decision_card"]["choice_contract"] == "one_default_two_audited_exceptions"
            and stream_policy["developer_decision_brief"]["developer_visible_options"] == ("appgen_event_contract",)
            and "stream_engine_picker" in stream_policy["developer_decision_brief"]["studio_controls_to_hide"]
            and stream_policy["opinionated_stack"]["default_event_adapter"] == "appgen_outbox_inbox_faust_streaming"
            and stream_policy["decision_ladder"][0] == "omit_stream_processor_for_ordinary_apps"
            and all(item["use"] in stream_policy["allowed_processors"] for item in stream_policy["decision_tree"])
            and "adding a fourth processor without a platform architecture decision" in stream_policy["prohibited"]
            and not invalid_exception["ok"]
            and valid_exception["ok"]
            and valid_exception["stream_processor_decision"] == "exception",
            "default": stream_policy["default"],
            "allowed_processors": stream_policy["allowed_processors"],
            "decision_tree": stream_policy["decision_tree"],
            "invalid_exception": invalid_exception,
            "valid_exception": valid_exception,
        },
        {
            "id": "eventing_choice_linter",
            "ok": ordinary_eventing_lint["ok"]
            and not branching_eventing_lint["ok"]
            and branching_eventing_lint["quick_fixes"][0]["id"] == "remove_stream_processor"
            and branching_eventing_lint["diagnostics"][0]["rule"] == "ordinary_pbc_manifest_omits_stream_processor",
            "ordinary": ordinary_eventing_lint,
            "branching": branching_eventing_lint,
        },
        {
            "id": "composition_plan",
            "ok": composition["ok"]
            and not composition["shared_datastores"]
            and len(composition["services"]) == len(sample),
        },
        {
            "id": "natural_language_selection",
            "ok": nl_selection["matched"]
            and {"gl_core", "ap_automation", "ar_credit", "inventory_positioning", "personnel_identity", "dom"}
            <= set(nl_selection["pbcs"]),
        },
        {
            "id": "generation_smoke",
            "ok": smoke["ok"],
            "checks": smoke["checks"],
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.pbc-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "meshes": pbc_mesh_catalog(),
        "catalog": pbc_catalog(),
        "starter_stacks": pbc_starter_stacks(),
        "topology": topology,
        "acp_coverage": acp_coverage,
        "acp_composition": acp_composition,
        "stream_processors": acp_stream_processor_catalog(),
        "manifest_schema": pbc_manifest_schema(),
        "example_registration": register_pbc_manifest(example_pbc_manifest()),
        "package_loading": package_loading,
        "sample_composition": composition,
        "nl_selection": nl_selection,
        "generation_smoke": smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }


def pbc_generation_smoke_audit(selected_pbcs: tuple[str, ...] | list[str] | None = None) -> dict:
    """Generate and compile a small app from a PBC composition DSL."""
    from .dsl import schema_from_dsl
    from .gen import generate_app_from_schema

    selected = tuple(selected_pbcs or PBC_STARTER_STACKS["enterprise_core"])
    dsl = pbc_composition_dsl(selected, app_name="PbcSmoke")
    schema = schema_from_dsl(dsl, source_name="pbc-composition.appgen")
    with tempfile.TemporaryDirectory(prefix="appgen-pbc-composition-") as raw_workdir:
        project_dir = Path(raw_workdir) / "pbc-smoke"
        output_dir = project_dir / "app"
        generate_app_from_schema(schema, output_dir)
        artifacts = ("app/models.py", "app/views.py", "app/pbc_runtime.py", "app/appgen.json", "docs/schema.md")
        missing = tuple(path for path in artifacts if not (project_dir / path).exists())
        compiled = []
        compile_failures = []
        for relative in ("app/models.py", "app/views.py", "app/pbc_runtime.py"):
            path = project_dir / relative
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"path": relative, "error": str(exc)})
            else:
                compiled.append(relative)
        runtime_smoke = {"ok": False, "error": "app/pbc_runtime.py was not loaded"}
        runtime_manifest = {}
        runtime_workbench = {}
        runtime_registration = {}
        runtime_path = output_dir / "pbc_runtime.py"
        if runtime_path.exists() and not any(item["path"] == "app/pbc_runtime.py" for item in compile_failures):
            try:
                spec = importlib.util.spec_from_file_location("generated_pbc_runtime_smoke", runtime_path)
                generated_pbc_runtime = importlib.util.module_from_spec(spec)
                assert spec.loader is not None
                spec.loader.exec_module(generated_pbc_runtime)
                runtime_manifest = generated_pbc_runtime.pbc_runtime_manifest()
                runtime_workbench = generated_pbc_runtime.pbc_composition_runtime_workbench()
                runtime_registration = generated_pbc_runtime.register_generated_pbc_package(
                    {
                        **example_pbc_manifest(),
                        "pbc": "generated_warranty_claims",
                        "tests": ("tests/test_generated_warranty_claims.py",),
                        "docs": ("README.md",),
                    }
                )
                runtime_smoke = generated_pbc_runtime.smoke_test()
            except Exception as exc:  # pragma: no cover - reported in audit payload
                runtime_smoke = {"ok": False, "error": str(exc)}
    checks = (
        {
            "id": "dsl_tables",
            "ok": len(schema.tables) >= len(selected) * 2,
            "table_count": len(schema.tables),
        },
        {
            "id": "required_artifacts",
            "ok": not missing,
            "missing": missing,
        },
        {
            "id": "compiled_artifacts",
            "ok": not compile_failures and set(compiled) == {"app/models.py", "app/views.py", "app/pbc_runtime.py"},
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "generated_pbc_runtime",
            "ok": runtime_smoke["ok"]
            and runtime_manifest.get("format") == "appgen.generated-pbc-runtime-manifest.v1"
            and tuple(selected) == tuple(runtime_manifest.get("selected_pbcs", ()))
            and runtime_workbench.get("ok") is True
            and runtime_registration.get("ok") is True,
            "manifest": runtime_manifest,
            "workbench": runtime_workbench,
            "registration": runtime_registration,
            "smoke": runtime_smoke,
        },
    )
    return {
        "format": "appgen.pbc-generation-smoke-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "selected_pbcs": selected,
        "dsl": dsl,
        "checks": checks,
    }


def _pbc_descriptor(key: str, pbc: dict) -> dict:
    return {
        "pbc": key,
        "label": pbc["label"],
        "mesh": pbc["mesh"],
        "mesh_label": PBC_MESHES[pbc["mesh"]]["label"],
        "description": pbc["description"],
        "datastore": f"{key}_store",
        "datastore_backend": pbc.get("datastore_backend", "postgresql"),
        "stream_processor": pbc.get("stream_processor", "faust_streaming"),
        "stream_exception_evidence": dict(pbc.get("stream_exception_evidence", {})),
        "tables": pbc["tables"],
        "apis": pbc["apis"],
        "emits": pbc["emits"],
        "consumes": pbc["consumes"],
        "template": pbc["template"],
        "selectable": True,
    }


def _pbc_descriptor_from_manifest(manifest: dict) -> dict:
    key = manifest["pbc"]
    return {
        "pbc": key,
        "label": manifest["label"],
        "mesh": manifest["mesh"],
        "mesh_label": PBC_MESHES[manifest["mesh"]]["label"],
        "description": manifest["description"],
        "datastore": f"{key}_store",
        "datastore_backend": manifest["datastore_backend"],
        "stream_processor": manifest.get("stream_processor", "faust_streaming"),
        "stream_exception_evidence": dict(manifest.get("stream_exception_evidence", {})),
        "tables": tuple(manifest["tables"]),
        "apis": tuple(manifest["apis"]),
        "emits": tuple(manifest["emits"]),
        "consumes": tuple(manifest["consumes"]),
        "template": manifest.get("template"),
        "ui_fragments": tuple(manifest.get("ui_fragments", ())),
        "permissions": tuple(manifest.get("permissions", ())),
        "configuration": tuple(manifest.get("configuration", ())),
        "migrations": tuple(manifest.get("migrations", ())),
        "seed_data": tuple(manifest.get("seed_data", ())),
        "tests": tuple(manifest.get("tests", ())),
        "docs": tuple(manifest.get("docs", ())),
        "selectable": True,
    }


def _service_contract(key: str) -> dict:
    pbc = PBC_CATALOG[key]
    class_name = "".join(part.capitalize() for part in key.split("_"))
    return {
        **_pbc_descriptor(key, pbc),
        "class_name": class_name,
        "api_base": f"/api/pbc/{key}",
        "event_topic": f"pbc.{key}.events",
        "inbox_topic": f"pbc.{key}.inbox",
        "owner": key,
    }


def _selection_terms(key: str, pbc: dict) -> tuple[str, ...]:
    terms = set(key.split("_"))
    terms.update(word.lower() for word in re.findall(r"[A-Za-z]+", pbc["label"]) if len(word) > 2)
    terms.update(word.lower() for table in pbc["tables"] for word in table.split("_") if len(word) > 2)
    aliases = {
        "gl_core": ("gl", "ledger"),
        "ap_automation": ("ap", "payable", "vendor"),
        "ar_credit": ("ar", "receivable", "credit"),
        "inventory_positioning": ("inventory", "stock"),
        "personnel_identity": ("people", "hr", "employee"),
        "dom": ("order", "orders", "fulfillment"),
    }
    terms.update(aliases.get(key, ()))
    return tuple(sorted(terms))


def _app_name_from_prompt(prompt: str) -> str:
    match = re.search(r"\b(?:app|application|system)\s+(?P<name>[A-Za-z][A-Za-z0-9_]*)", prompt, re.I)
    if not match:
        return "ComposableEnterprise"
    raw = match.group("name")
    return raw[:1].upper() + raw[1:]
