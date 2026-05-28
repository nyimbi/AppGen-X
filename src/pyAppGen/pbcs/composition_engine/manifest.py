"""Package manifest for the composition_engine PBC."""

from __future__ import annotations

from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import composition_engine_build_api_contract

PBC_KEY = 'composition_engine'

PBC_MANIFEST = {
    "pbc": "composition_engine",
    "label": "Low-Code Composition Engine",
    "mesh": "platform",
    "description": "Drag-and-drop PBC assembly, component registry, layout engine, package registration, and experience composition.",
    "datastore_backend": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS[0],
    "tables": COMPOSITION_ENGINE_OWNED_TABLES,
    "apis": tuple(route["route"] for route in composition_engine_build_api_contract()["routes"]),
    "emits": COMPOSITION_ENGINE_EMITTED_EVENT_TYPES,
    "consumes": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
        "CompositionWorkbench",
        "WorkspaceSelector",
        "SelectionImpactPreview",
        "ComponentRegistry",
        "FragmentCatalog",
        "LayoutCanvas",
        "ReleaseRehearsalPanel",
        "ReleaseEvidenceBoard",
        "CompositionRuleStudio",
        "CompositionParameterConsole",
        "CompositionConfigurationPanel",
        "AssistantPreviewWorkbench",
        "CompositionWizardLauncher",
        "CompositionControlCenter",
        "DocumentationMatrix",
        "SecurityReviewPanel",
    ),
    "permissions": (
        "composition_engine.read",
        "composition_engine.compose",
        "composition_engine.approve",
        "composition_engine.publish",
        "composition_engine.event",
        "composition_engine.configure",
        "composition_engine.audit",
    ),
    "configuration": (
        "COMPOSITION_ENGINE_DATABASE_URL",
        "COMPOSITION_ENGINE_EVENT_TOPIC",
        "COMPOSITION_ENGINE_RETRY_LIMIT",
        "COMPOSITION_ENGINE_ALLOWED_TARGETS",
        "COMPOSITION_ENGINE_ALLOWED_LAYOUT_MODES",
        "COMPOSITION_ENGINE_PUBLICATION_MODE",
        "COMPOSITION_ENGINE_DEFAULT_TIMEZONE",
    ),
    "capabilities": COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS,
    "standard_features": COMPOSITION_ENGINE_STANDARD_FEATURE_KEYS,
    "workflows": tuple(
        item
        for route in composition_engine_build_api_contract()["routes"]
        for item in (route.get("command") or route.get("query"),)
        if item
    ),
    "analytics": (
        "composition_published_throughput",
        "pbc_deployed_throughput",
        "composition_plan_validation_rate",
        "package_registration_plan_latency",
        "layout_density_score",
        "release_risk_score",
        "dead_letter_recovery_rate",
    ),
    "advanced_capabilities": COMPOSITION_ENGINE_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_runtime_capabilities.py", "tests/test_orchestration_app.py"),
    "docs": (
        "SPECIFICATION.md",
        "RELEASE_EVIDENCE.md",
        "README.md",
        "implementation-plan.md",
        "implementation-status.md",
    ),
}
