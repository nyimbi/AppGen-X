"""Package manifest for the workflow_orchestration PBC."""

from .runtime import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS
from .runtime import workflow_orchestration_build_api_contract


PBC_MANIFEST = {
    "pbc": "workflow_orchestration",
    "label": "Distributed Workflow Orchestration Engine",
    "mesh": "platform",
    "description": "Workflow definitions, versions, instances, signals, timers, sagas, compensations, human tasks, policy gates, AppGen-X eventing, and governed orchestration telemetry.",
    "datastore_backend": "postgresql",
    "tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES + WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
    "apis": tuple(route["route"] for route in workflow_orchestration_build_api_contract()["routes"]),
    "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
    "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
        "WorkflowWorkbench",
        "StateMachineDesigner",
        "WorkflowInstanceMonitor",
        "SignalInbox",
        "TimerConsole",
        "SagaStepBoard",
        "CompensationPlanner",
        "HumanTaskQueue",
        "WorkflowReleaseWorkbench",
        "WorkflowConfigurationPanel",
    ),
    "permissions": (
        "workflow_orchestration.define",
        "workflow_orchestration.start",
        "workflow_orchestration.signal",
        "workflow_orchestration.compensate",
        "workflow_orchestration.event",
        "workflow_orchestration.configure",
        "workflow_orchestration.audit",
        "workflow_orchestration.read",
    ),
    "configuration": (
        "WORKFLOW_ORCHESTRATION_DATABASE_URL",
        "WORKFLOW_ORCHESTRATION_EVENT_TOPIC",
        "WORKFLOW_ORCHESTRATION_RETRY_LIMIT",
        "WORKFLOW_ORCHESTRATION_DEFAULT_TIMEZONE",
        "WORKFLOW_ORCHESTRATION_ALLOWED_SIGNAL_SOURCES",
    ),
    "capabilities": tuple(f"workflow_orchestration.{table}" for table in WORKFLOW_ORCHESTRATION_OWNED_TABLES + WORKFLOW_ORCHESTRATION_RUNTIME_TABLES),
    "standard_features": WORKFLOW_ORCHESTRATION_STANDARD_FEATURE_KEYS,
    "advanced_capabilities": WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS,
    "workflows": (
        "command_workflow_definitions",
        "command_workflow_instances",
        "command_workflow_signals",
        "command_timer_tasks",
        "command_saga_steps",
        "command_compensations",
        "command_event_inbox",
        "query_workflow_orchestration_workbench",
        "standalone_workflow_authoring",
    ),
    "analytics": (
        "workflow_start_rate",
        "saga_step_latency",
        "timer_breach_risk",
        "compensation_rate",
        "human_task_sla",
        "workflow_completed_throughput",
    ),
    "advanced_runtime": WORKFLOW_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_runtime_capabilities.py", "tests/test_standalone.py"),
    "docs": ("README.md", "RELEASE_EVIDENCE.md", "SPECIFICATION.md", "implementation-plan.md", "implementation-status.md"),
}
