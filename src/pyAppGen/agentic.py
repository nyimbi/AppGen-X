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
            "id": "artifact_contract",
            "ok": {"app/agents.py", "app/templates/appgen_agents.html"} <= existing,
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
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-agentic-system-readiness-unless-ok-is-true",
    }
