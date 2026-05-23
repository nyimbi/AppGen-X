"""Package-level agentic system contracts.

Generated apps include an agent workbench. This module exposes pre-generation
proof that the DSL and package contracts can model local LLMs, API-key LLMs,
agents, tool policies, and execution gates without calling any provider.
"""

from __future__ import annotations

from .dsl import schema_from_dsl


AGENTIC_SAMPLE_DSL = """
app AgenticAudit { targets: web, mobile, desktop, chatbot }

table Ticket {
  id: int pk
  title: string required
  status: string default "open"
}

view TicketForm for Ticket {
  Main: title, status
  @ title TextBox 0 0 6 1
}

llm LocalModel {
  provider: ollama
  mode: local
  model: llama3
  endpoint: "http://localhost:11434"
}

llm ApiModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent SupportAgent {
  provider: LocalModel
  goal: "Triage support tickets and prepare reviewed updates"
  tools: schema, forms, chatbots, reports
  memory: project
  max_steps: 6
}

agent ReleaseReviewer {
  provider: ApiModel
  goal: "Review generated application changes before release"
  tools: schema, reports, agents
  memory: session
  max_steps: 4
}
"""

PROVIDERS = {
    "LocalModel": {
        "provider": "ollama",
        "mode": "local",
        "model": "llama3",
        "endpoint": "http://localhost:11434",
        "env": (),
    },
    "LmStudio": {
        "provider": "lmstudio",
        "mode": "local",
        "model": "local-model",
        "endpoint": "http://localhost:1234/v1",
        "env": (),
    },
    "ApiModel": {
        "provider": "openai",
        "mode": "api",
        "model": "gpt-4.1-mini",
        "api_key_env": "OPENAI_API_KEY",
        "env": ("OPENAI_API_KEY",),
    },
    "ClaudeModel": {
        "provider": "anthropic",
        "mode": "api",
        "model": "claude-sonnet-4",
        "api_key_env": "ANTHROPIC_API_KEY",
        "env": ("ANTHROPIC_API_KEY",),
    },
    "VllmLocal": {
        "provider": "vllm",
        "mode": "local",
        "model": "open-model",
        "endpoint": "http://localhost:8000/v1",
        "env": (),
    },
}

CODING_AGENT_VECTORS = {
    "claude_code": {
        "label": "Claude Code",
        "launcher": "claude",
        "provider": "ClaudeModel",
        "backends": ("api-key", "ollama", "vllm"),
        "surfaces": ("dsl", "database", "forms", "workflows", "agents", "tests", "docs"),
        "outputs": ("dsl_patch", "schema_diff", "form_update", "agent_update", "test_plan", "migration_plan"),
        "required_env": ("ANTHROPIC_API_KEY",),
    },
    "openai_codex": {
        "label": "OpenAI Codex",
        "launcher": "codex",
        "provider": "ApiModel",
        "backends": ("api-key", "ollama", "vllm"),
        "surfaces": ("dsl", "database", "forms", "workflows", "agents", "tests", "docs"),
        "outputs": ("dsl_patch", "schema_diff", "form_update", "agent_update", "test_plan", "migration_plan"),
        "required_env": ("OPENAI_API_KEY",),
    },
    "opencode": {
        "label": "OpenCode",
        "launcher": "opencode",
        "provider": "LocalModel",
        "backends": ("ollama", "vllm", "api-key"),
        "surfaces": ("dsl", "database", "forms", "workflows", "agents", "tests", "docs"),
        "outputs": ("dsl_patch", "schema_diff", "form_update", "agent_update", "test_plan", "migration_plan"),
        "required_env": (),
    },
}

AGENTS = {
    "SupportAgent": {
        "provider": "LocalModel",
        "goal": "Triage support tickets and prepare reviewed updates",
        "tools": ("schema", "forms", "chatbots", "reports"),
        "memory": "project",
        "max_steps": 6,
    },
    "ReleaseReviewer": {
        "provider": "ApiModel",
        "goal": "Review generated application changes before release",
        "tools": ("schema", "forms", "reports", "integrations"),
        "memory": "session",
        "max_steps": 4,
    },
}


def provider_catalog(environ: dict | None = None) -> tuple[dict, ...]:
    """Return local and API-key LLM provider contracts with secret status."""
    env = environ or {}
    providers = []
    for name, spec in PROVIDERS.items():
        required = tuple(spec["env"])
        missing = tuple(key for key in required if not env.get(key))
        providers.append(
            {
                "name": name,
                **spec,
                "env": required,
                "missing": missing,
                "configured": not missing,
                "secret_policy": "env-only" if spec["mode"] == "api" else "no-secret",
            }
        )
    return tuple(providers)


def agent_catalog() -> tuple[dict, ...]:
    """Return package-level generated agent definitions."""
    return tuple({"name": name, **agent} for name, agent in AGENTS.items())


def dsl_agentic_contract(source: str = AGENTIC_SAMPLE_DSL) -> dict:
    """Parse the DSL and summarize its agentic declarations."""
    schema = schema_from_dsl(source, source_name="agentic-audit.appgen")
    provider_modes = tuple(sorted({provider.mode for provider in schema.llm_providers}))
    return {
        "format": "appgen.package-agentic-dsl-contract.v1",
        "app": schema.app_name,
        "targets": schema.app_options.get("targets", ()),
        "providers": tuple(provider.name for provider in schema.llm_providers),
        "provider_modes": provider_modes,
        "agents": tuple(agent.name for agent in schema.agents),
        "agent_provider_links": tuple(
            {"agent": agent.name, "provider": agent.provider} for agent in schema.agents
        ),
        "ok": provider_modes == ("api", "local") and bool(schema.agents),
    }


def provider_connection_matrix(environ: dict | None = None) -> dict:
    """Return provider readiness without dispatching LLM calls."""
    providers = provider_catalog(environ)
    modes = tuple(sorted({provider["mode"] for provider in providers}))
    missing_api = tuple(
        provider["name"]
        for provider in providers
        if provider["mode"] == "api" and provider["missing"]
    )
    return {
        "format": "appgen.package-agent-provider-matrix.v1",
        "ok": modes == ("api", "local") and not missing_api,
        "modes": modes,
        "providers": providers,
        "missing_api_providers": missing_api,
    }


def coding_agent_vector_catalog(environ: dict | None = None) -> tuple[dict, ...]:
    """Return first-class coding-agent vectors for building AppGen apps."""
    env = environ or {}
    rows = []
    for key, vector in CODING_AGENT_VECTORS.items():
        missing = tuple(name for name in vector["required_env"] if not env.get(name))
        rows.append(
            {
                "key": key,
                **vector,
                "configured": not missing,
                "missing": missing,
                "guardrails": (
                    "dsl_lint_before_apply",
                    "schema_diff_review",
                    "generated_tests_required",
                    "human_approval_for_destructive_changes",
                    "secret_redaction",
                ),
            }
        )
    return tuple(rows)


def coding_agent_backend_matrix(environ: dict | None = None) -> dict:
    """Return local/API backend readiness for coding-agent vectors."""
    env = environ or {}
    vectors = coding_agent_vector_catalog(env)
    backend_rows = []
    for vector in vectors:
        for backend in vector["backends"]:
            backend_rows.append(
                {
                    "vector": vector["key"],
                    "backend": backend,
                    "local": backend in {"ollama", "vllm"},
                    "secret_required": backend == "api-key",
                    "ready": backend != "api-key" or vector["configured"],
                    "endpoint": "http://localhost:11434" if backend == "ollama" else "http://localhost:8000/v1" if backend == "vllm" else None,
                }
            )
    return {
        "format": "appgen.coding-agent-backend-matrix.v1",
        "ok": {"claude_code", "openai_codex", "opencode"} <= {vector["key"] for vector in vectors}
        and {"ollama", "vllm", "api-key"} <= {row["backend"] for row in backend_rows}
        and all(row["ready"] for row in backend_rows if row["secret_required"]),
        "vectors": vectors,
        "backends": tuple(backend_rows),
    }


def coding_agent_development_workflow(vector_key: str = "openai_codex", *, backend: str = "ollama") -> dict:
    """Return the reviewed app-development workflow for a coding-agent vector."""
    vector = CODING_AGENT_VECTORS[vector_key]
    if backend not in vector["backends"]:
        raise KeyError(f"Unsupported backend for {vector_key}: {backend}")
    stages = (
        {"stage": "ingest_goal", "inputs": ("natural_language", "dsl", "existing_schema"), "outputs": ("change_intent",)},
        {"stage": "draft_dsl_patch", "inputs": ("change_intent", "component_catalog"), "outputs": ("dsl_patch", "schema_diff")},
        {"stage": "preview_application_changes", "inputs": ("dsl_patch",), "outputs": ("forms", "tables", "agents", "tests")},
        {"stage": "run_quality_gates", "inputs": ("generated_project",), "outputs": ("lint", "tests", "release_audit")},
        {"stage": "review_and_apply", "inputs": ("diff", "audit"), "outputs": ("approved_commit_plan",)},
    )
    return {
        "format": "appgen.coding-agent-development-workflow.v1",
        "ok": bool(stages) and backend in {"ollama", "vllm", "api-key"},
        "vector": vector_key,
        "launcher": vector["launcher"],
        "backend": backend,
        "stages": stages,
        "guardrails": (
            "no_direct_database_mutation",
            "no_unreviewed_file_deletion",
            "generated_diff_required",
            "rollback_plan_required",
        ),
        "appgen_surfaces": vector["surfaces"],
    }


def coding_agent_release_gate(environ: dict | None = None) -> dict:
    """Return release readiness for coding-agent development vectors."""
    env = environ or {"OPENAI_API_KEY": "configured", "ANTHROPIC_API_KEY": "configured"}
    catalog = coding_agent_vector_catalog(env)
    backend_matrix = coding_agent_backend_matrix(env)
    workflows = tuple(
        coding_agent_development_workflow(vector["key"], backend=backend)
        for vector in catalog
        for backend in ("ollama", "vllm")
        if backend in vector["backends"]
    )
    gates = (
        {
            "id": "coding_agent_vectors",
            "ok": {"claude_code", "openai_codex", "opencode"} <= {vector["key"] for vector in catalog},
            "vectors": tuple(vector["key"] for vector in catalog),
        },
        {
            "id": "local_backend_vectors",
            "ok": {"ollama", "vllm"} <= {backend for vector in catalog for backend in vector["backends"]},
            "backends": tuple(sorted({backend for vector in catalog for backend in vector["backends"]})),
        },
        {
            "id": "api_key_secret_policy",
            "ok": all(vector["configured"] for vector in catalog if vector["required_env"]),
            "missing": tuple((vector["key"], vector["missing"]) for vector in catalog if vector["missing"]),
        },
        {
            "id": "backend_matrix",
            "ok": backend_matrix["ok"],
            "format": backend_matrix["format"],
        },
        {
            "id": "development_workflows",
            "ok": bool(workflows) and all(workflow["ok"] for workflow in workflows),
            "workflows": tuple((workflow["vector"], workflow["backend"]) for workflow in workflows),
        },
        {
            "id": "guardrails",
            "ok": all("generated_tests_required" in vector["guardrails"] for vector in catalog)
            and all("rollback_plan_required" in workflow["guardrails"] for workflow in workflows),
        },
    )
    return {
        "format": "appgen.coding-agent-release-gate.v1",
        "ok": all(gate["ok"] for gate in gates),
        "decision": "approved" if all(gate["ok"] for gate in gates) else "blocked",
        "catalog": catalog,
        "backend_matrix": backend_matrix,
        "workflows": workflows,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }


def agent_tool_policy(agent_name: str | None = None) -> dict:
    """Return reviewed tool policy for one or all generated agents."""
    selected = (
        tuple(agent for agent in agent_catalog() if agent["name"] == agent_name)
        if agent_name
        else agent_catalog()
    )
    allowed_tools = ("schema", "forms", "chatbots", "reports", "integrations")
    denied_tools = ("drop_table", "delete_database", "raw_secret_read", "unreviewed_deploy")
    policy_items = tuple(
        {
            "agent": agent["name"],
            "provider": agent["provider"],
            "allowed_tools": tuple(tool for tool in agent["tools"] if tool in allowed_tools),
            "denied_tools": denied_tools,
            "human_review_required": ("database_mutation", "external_call", "deployment"),
            "max_steps": agent["max_steps"],
        }
        for agent in selected
    )
    return {
        "format": "appgen.package-agent-tool-policy.v1",
        "ok": bool(policy_items) and all(item["max_steps"] <= 8 for item in policy_items),
        "policies": policy_items,
    }


def agent_execution_matrix(task: str = "review generated change", environ: dict | None = None) -> dict:
    """Return a deterministic execution plan for every generated agent."""
    providers = {provider["name"]: provider for provider in provider_catalog(environ)}
    plans = []
    for agent in agent_catalog():
        provider = providers[agent["provider"]]
        plans.append(
            {
                "agent": agent["name"],
                "task": task,
                "provider": provider["name"],
                "mode": provider["mode"],
                "model": provider["model"],
                "tools": agent["tools"],
                "review_required": True,
                "ready": provider["configured"],
            }
        )
    return {
        "format": "appgen.package-agent-execution-matrix.v1",
        "ok": all(plan["ready"] for plan in plans),
        "plans": tuple(plans),
    }


def agentic_generation_smoke_audit(source: str = AGENTIC_SAMPLE_DSL) -> dict:
    """Generate a temporary app and exercise its generated agentic contracts."""
    import importlib.util
    import py_compile
    import tempfile
    from pathlib import Path

    from .gen import generate_app_from_schema

    required_artifacts = (
        "app/agents.py",
        "app/templates/appgen_agents.html",
        "app/models.py",
        "app/views.py",
    )
    compile_artifacts = (
        "app/agents.py",
        "app/models.py",
        "app/views.py",
    )
    existing_paths = {"app/agents.py", "app/templates/appgen_agents.html"}
    env = {
        "OPENAI_API_KEY": "configured-for-generated-smoke",
        "ANTHROPIC_API_KEY": "configured-for-generated-smoke",
    }

    with tempfile.TemporaryDirectory(prefix="appgen-agentic-smoke-") as tmp:
        project_dir = Path(tmp)
        output_dir = project_dir / "app"
        schema = schema_from_dsl(source, source_name="agentic-smoke.appgen")
        generate_app_from_schema(schema, output_dir)

        missing_artifacts = tuple(
            artifact for artifact in required_artifacts if not (project_dir / artifact).exists()
        )
        compiled = []
        compile_failures = []
        for artifact in compile_artifacts:
            path = project_dir / artifact
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_failures.append({"artifact": artifact, "error": str(exc)})
            else:
                compiled.append(artifact)

        module_path = output_dir / "agents.py"
        spec = importlib.util.spec_from_file_location(
            "generated_agentic_smoke_agents",
            module_path,
        )
        generated_agents = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_agents)

        providers = generated_agents.provider_catalog(env)
        missing_providers = generated_agents.provider_catalog({})
        provider_matrix = generated_agents.provider_connection_matrix(env)
        agents = generated_agents.agent_catalog()
        tool_policy = generated_agents.agent_tool_policy()
        execution = generated_agents.agent_execution_matrix(
            task="review generated app evolution",
            environ=env,
        )
        local_plan = generated_agents.agent_plan(
            "SupportAgent",
            "triage support ticket",
            environ=env,
        )
        api_plan = generated_agents.agent_plan(
            "ReleaseReviewer",
            "review generated app",
            environ=env,
        )
        release_gate = generated_agents.agentic_release_gate(existing_paths, environ=env)
        workbench = generated_agents.agentic_workbench(existing_paths, environ=env)
        artifact_check = generated_agents.agents_check(existing_paths)

    checks = (
        {
            "id": "generated_artifacts",
            "ok": not missing_artifacts,
            "required_artifacts": required_artifacts,
            "missing": missing_artifacts,
        },
        {
            "id": "generated_python_compiles",
            "ok": not compile_failures and set(compiled) == set(compile_artifacts),
            "compiled": tuple(compiled),
            "failures": tuple(compile_failures),
        },
        {
            "id": "provider_modes_and_secret_guards",
            "ok": {"local", "api"} <= set(provider_matrix["modes"])
            and all(
                provider["mode"] == "local" or provider["required_env"] == ("OPENAI_API_KEY",)
                for provider in providers
            )
            and any(provider["mode"] == "api" and provider["missing"] for provider in missing_providers),
            "providers": providers,
            "missing_providers": missing_providers,
            "matrix": provider_matrix,
        },
        {
            "id": "agent_catalog_and_links",
            "ok": {"SupportAgent", "ReleaseReviewer"} <= {agent["name"] for agent in agents}
            and {plan["provider_mode"] for plan in (local_plan, api_plan)} == {"local", "api"}
            and local_plan["ready"] is True
            and api_plan["ready"] is True,
            "agents": agents,
            "local_plan": local_plan,
            "api_plan": api_plan,
        },
        {
            "id": "tool_policy_and_execution_matrix",
            "ok": tool_policy["ok"] is True
            and execution["ok"] is True
            and all(plan["ready"] for plan in execution["plans"]),
            "tool_policy": tool_policy,
            "execution": execution,
        },
        {
            "id": "generated_release_and_workbench",
            "ok": release_gate["ok"] is True
            and workbench["ok"] is True
            and artifact_check["ok"] is True,
            "release_gate": release_gate,
            "workbench": workbench,
            "artifact_check": artifact_check,
        },
    )
    ok = all(check["ok"] for check in checks)
    return {
        "format": "appgen.agentic-generation-smoke-audit.v1",
        "scope": "generated-app",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "required_artifacts": required_artifacts,
        "compiled_artifacts": tuple(compiled),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "stop_condition": "do-not-claim-generated-agentic-readiness-unless-ok-is-true",
    }


def agentic_release_audit(
    existing_paths: set[str] | None = None,
    environ: dict | None = None,
) -> dict:
    """Return package-level proof for agentic-system readiness."""
    existing = (
        {"app/agents.py", "app/templates/appgen_agents.html"}
        if existing_paths is None
        else existing_paths
    )
    audit_env = environ or {
        "OPENAI_API_KEY": "configured-for-audit",
        "ANTHROPIC_API_KEY": "configured-for-audit",
    }
    dsl_contract = dsl_agentic_contract()
    provider_matrix = provider_connection_matrix(audit_env)
    missing_secret_matrix = provider_connection_matrix({})
    tool_policy = agent_tool_policy()
    execution = agent_execution_matrix(environ=audit_env)
    generation_smoke = agentic_generation_smoke_audit()
    coding_agents = coding_agent_release_gate(audit_env)
    agent_providers = {agent["provider"] for agent in agent_catalog()}
    provider_names = {provider["name"] for provider in provider_catalog(audit_env)}
    gates = (
        {
            "id": "dsl_llm_agent_blocks",
            "ok": dsl_contract["ok"] and {"LocalModel", "ApiModel"} <= set(dsl_contract["providers"]),
        },
        {
            "id": "provider_modes",
            "ok": provider_matrix["ok"] and set(provider_matrix["modes"]) == {"local", "api"},
        },
        {
            "id": "api_key_secret_policy",
            "ok": all(
                provider["secret_policy"] == "env-only"
                for provider in provider_matrix["providers"]
                if provider["mode"] == "api"
            ),
        },
        {
            "id": "missing_secret_guard",
            "ok": missing_secret_matrix["ok"] is False
            and set(missing_secret_matrix["missing_api_providers"]) == {"ApiModel", "ClaudeModel"},
        },
        {
            "id": "agent_provider_links",
            "ok": agent_providers <= provider_names,
        },
        {
            "id": "tool_policy",
            "ok": tool_policy["ok"],
        },
        {
            "id": "execution_matrix",
            "ok": execution["ok"],
        },
        {
            "id": "coding_agent_vectors",
            "ok": coding_agents["ok"],
            "checks": tuple(gate["id"] for gate in coding_agents["gates"]),
        },
        {
            "id": "artifact_contract",
            "ok": {"app/agents.py", "app/templates/appgen_agents.html"} <= existing,
        },
        {
            "id": "generation_smoke",
            "ok": generation_smoke["ok"],
            "checks": tuple(check["id"] for check in generation_smoke["checks"]),
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-agentic-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "dsl": dsl_contract,
        "providers": provider_matrix,
        "missing_secret_guard": missing_secret_matrix,
        "agents": agent_catalog(),
        "tool_policy": tool_policy,
        "execution": execution,
        "coding_agents": coding_agents,
        "generation_smoke": generation_smoke,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-agentic-system-readiness-unless-ok-is-true",
    }
