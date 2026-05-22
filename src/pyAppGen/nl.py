"""Package-level natural-language evolution helpers.

Generated apps expose a natural-language evolution workbench after code
generation.  This module gives the package CLI the same deterministic planning
surface before generation, so prompts can become auditable DSL patches.
"""

from __future__ import annotations

import re

from .erp import ERP_MODULES
from .erp import erp_module_dsl


SUPPORTED_TARGETS = ("web", "pwa", "mobile", "desktop", "chatbot")
DEFAULT_TARGETS = ("web",)
DEFAULT_TABLE = "Ticket"
LLM_PROVIDER_NAME = "LocalModel"


def evolution_capabilities() -> dict:
    """Return the package-level natural-language evolution contract."""
    return {
        "format": "appgen.nl-evolution-capabilities.v1",
        "scope": "package",
        "inputs": ("natural_language_prompt", "base_dsl"),
        "outputs": ("plan", "dsl_patch", "migration_impact", "rollback_plan"),
        "can_generate": (
            "database_tables",
            "database_fields",
            "forms",
            "workflows",
            "business_rules",
            "reports",
            "dashboards",
            "chatbots",
            "agents",
            "erp_modules",
            "platform_targets",
        ),
        "provider_modes": ("local_llm", "api_key_llm"),
        "guards": ("destructive_intent_detection", "approval_required_for_delete"),
    }


def destructive_intent_report(prompt: str) -> dict:
    """Detect destructive prompt intent before generating a DSL patch."""
    text = prompt.lower()
    table_matches = tuple(
        _canonical_name(match.group("name"))
        for match in re.finditer(r"\b(?:drop|delete|remove)\s+table\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)", prompt, re.I)
    )
    field_matches = tuple(
        _snake_name(match.group("name"))
        for match in re.finditer(r"\b(?:drop|delete|remove)\s+field\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)", prompt, re.I)
    )
    destructive = bool(table_matches or field_matches or re.search(r"\b(drop|delete|remove|purge|truncate)\b", text))
    return {
        "format": "appgen.nl-destructive-intent.v1",
        "destructive": destructive,
        "requires_approval": destructive,
        "tables": table_matches,
        "fields": field_matches,
        "blocked_operations": ("drop_table", "drop_field") if destructive else (),
    }


def evolution_plan(prompt: str) -> dict:
    """Create a deterministic proposal plan from a natural-language prompt."""
    table = _requested_table(prompt)
    proposals: list[dict] = []
    if _mentions_any(prompt, ("table", "entity", "database", "model")):
        proposals.append({"kind": "add_table", "name": table, "source": "natural_language"})

    field_specs = _field_specs(prompt)
    if field_specs and not any(item["kind"] == "add_table" for item in proposals):
        proposals.append({"kind": "add_table", "name": table, "source": "natural_language"})
    for field in field_specs:
        proposals.append({"kind": "add_field", "table": table, **field})

    form_name = _named_after(prompt, ("form", "view")) or f"{table}Form"
    if _mentions_any(prompt, ("form", "view", "screen", "page")):
        proposals.append({"kind": "add_form", "name": form_name, "table": table})

    workflow_name = _named_after(prompt, ("workflow", "flow")) or f"{table}Flow"
    if _mentions_any(prompt, ("workflow", "flow", "state")):
        proposals.append({"kind": "add_workflow", "name": workflow_name, "from": "open", "to": "closed"})

    rule_name = _named_after(prompt, ("rule", "policy")) or f"{table}Policy"
    if _mentions_any(prompt, ("rule", "policy", "validation")):
        proposals.append({"kind": "add_rule", "name": rule_name, "table": table})

    report_name = _named_after(prompt, ("report",)) or f"{table}Report"
    if _mentions_any(prompt, ("report", "export")):
        proposals.append({"kind": "add_report", "name": report_name, "table": table, "formats": ("csv", "pdf")})

    dashboard_name = _named_after(prompt, ("dashboard", "analytics")) or f"{table}Dashboard"
    if _mentions_any(prompt, ("dashboard", "analytics", "kpi")):
        proposals.append({"kind": "add_dashboard", "name": dashboard_name, "table": table, "charts": ("kpi", "bar")})

    chatbot_name = _named_after(prompt, ("chatbot", "bot")) or f"{table}Bot"
    if _mentions_any(prompt, ("chatbot", "bot", "conversation")):
        proposals.append({"kind": "add_chatbot", "name": chatbot_name, "table": table})

    agent_name = _named_after(prompt, ("agent", "assistant")) or f"{table}Agent"
    if _mentions_any(prompt, ("agent", "assistant", "agentic")):
        proposals.append({"kind": "add_agent", "name": agent_name, "provider": LLM_PROVIDER_NAME, "table": table})

    modules = _erp_modules(prompt)
    for module in modules:
        proposals.append({"kind": "add_erp_module", "module": module, "command": f"appgen --erp-template {module}"})

    targets = _target_specs(prompt)
    if targets:
        proposals.append({"kind": "set_targets", "targets": targets})

    return {
        "format": "appgen.nl-evolution-plan.v1",
        "prompt": prompt,
        "table": table,
        "proposals": tuple(proposals),
        "destructive": destructive_intent_report(prompt),
        "capabilities": evolution_capabilities()["can_generate"],
    }


def proposals_to_dsl(plan: dict) -> str:
    """Render a parseable DSL patch with comments for non-DSL artifacts."""
    proposals = tuple(plan.get("proposals", ()))
    table_names = tuple(dict.fromkeys(_proposal_table_names(proposals) or (plan.get("table") or DEFAULT_TABLE,)))
    targets = _proposal_targets(proposals) or DEFAULT_TARGETS
    fields_by_table = _fields_by_table(table_names, proposals)
    lines = [f"app EvolvedApp {{ targets: {', '.join(targets)} }}"]

    for table in table_names:
        lines.append("")
        lines.append(f"table {table} {{")
        fields = fields_by_table[table]
        if "id" not in {field["name"] for field in fields}:
            lines.append("  id: int pk")
        for field in fields:
            lines.append(f"  {_field_to_dsl(field)}")
        lines.append("}")

    llm_written = False
    for proposal in proposals:
        kind = proposal.get("kind")
        if kind == "add_form":
            table = proposal["table"]
            field_names = tuple(field["name"] for field in fields_by_table.get(table, ()) if field["name"] != "id") or ("id",)
            lines.append("")
            lines.append(f"view {proposal['name']} for {table} {{")
            lines.append(f"  Main: {', '.join(field_names)}")
            for index, field_name in enumerate(field_names[:6]):
                component = _component_for_field(field_name)
                lines.append(f"  @ {field_name} {component} 0 {index} 6 1")
            lines.append("}")
        elif kind == "add_workflow":
            lines.append("")
            lines.append(f"flow {proposal['name']} {{")
            lines.append(f"  {proposal['from']} -> {proposal['to']}")
            lines.append("}")
        elif kind == "add_rule":
            first_field = _first_business_field(fields_by_table.get(proposal["table"], ()))
            lines.append("")
            lines.append(f"rule {proposal['name']} for {proposal['table']} {{")
            lines.append(f"  {first_field} required \"{first_field} is required\"")
            lines.append("}")
        elif kind == "add_agent":
            if not llm_written:
                lines.append("")
                lines.append(f"llm {LLM_PROVIDER_NAME} {{ provider: ollama; mode: local; model: llama3 }}")
                lines.append("llm ApiModel { provider: openai; mode: api; model: gpt-4.1-mini; api_key: OPENAI_API_KEY }")
                llm_written = True
            lines.append("")
            lines.append(f"agent {proposal['name']} {{")
            lines.append(f"  provider: {proposal['provider']}")
            lines.append(f"  goal: \"Evolve and operate {proposal['table']} workflows\"")
            lines.append("  tools: schema, forms, chatbots")
            lines.append("  max_steps: 6")
            lines.append("}")
        elif kind == "add_report":
            lines.append("")
            lines.append(f"// add report {proposal['name']} for {proposal['table']} formats {', '.join(proposal['formats'])}")
        elif kind == "add_dashboard":
            lines.append("")
            lines.append(f"// add dashboard {proposal['name']} for {proposal['table']} charts {', '.join(proposal['charts'])}")
        elif kind == "add_chatbot":
            lines.append("")
            lines.append(f"// add chatbot {proposal['name']} for {proposal['table']} using generated intents and agent tools")
        elif kind == "add_erp_module":
            lines.append("")
            lines.append(f"// add ERP module {proposal['module']} with {proposal['command']}")

    return "\n".join(lines).rstrip() + "\n"


def evolution_changeset(prompt: str, base_dsl: str = "") -> dict:
    """Return an auditable natural-language changeset."""
    plan = evolution_plan(prompt)
    dsl_patch = proposals_to_dsl(plan)
    destructive = plan["destructive"]
    return {
        "format": "appgen.nl-evolution-changeset.v1",
        "ok": not destructive["requires_approval"],
        "prompt": prompt,
        "base_dsl_supplied": bool(base_dsl.strip()),
        "plan": plan,
        "dsl_patch": dsl_patch,
        "applied_preview": (base_dsl.rstrip() + "\n\n" + dsl_patch).strip() if base_dsl.strip() else dsl_patch,
        "requires_approval": destructive["requires_approval"],
        "destructive": destructive,
        "migration_impact": migration_impact(plan),
        "rollback_plan": rollback_plan(plan),
    }


def migration_impact(plan: dict) -> dict:
    """Summarize schema and application impact for a plan."""
    proposals = tuple(plan.get("proposals", ()))
    return {
        "format": "appgen.nl-migration-impact.v1",
        "tables_added": tuple(item["name"] for item in proposals if item.get("kind") == "add_table"),
        "fields_added": tuple(
            f"{item['table']}.{item['name']}" for item in proposals if item.get("kind") == "add_field"
        ),
        "app_artifacts": tuple(
            item["kind"]
            for item in proposals
            if item.get("kind") in {"add_form", "add_workflow", "add_rule", "add_report", "add_dashboard", "add_chatbot", "add_agent"}
        ),
        "erp_modules": tuple(item["module"] for item in proposals if item.get("kind") == "add_erp_module"),
    }


def rollback_plan(plan: dict) -> dict:
    """Return deterministic rollback guidance for generated NL patches."""
    impact = migration_impact(plan)
    return {
        "format": "appgen.nl-rollback-plan.v1",
        "steps": (
            "Review generated DSL patch before applying destructive changes.",
            "Keep the previous DSL file in version control.",
            "Revert the DSL patch and rerun generation if validation fails.",
        ),
        "reversible_items": impact["tables_added"] + impact["fields_added"] + impact["app_artifacts"] + impact["erp_modules"],
    }


def nl_evolution_release_audit() -> dict:
    """Return package-level readiness evidence for natural-language evolution."""
    sample = (
        "create table Ticket with fields title required, amount decimal, due_date date "
        "and form TicketForm workflow Triage rule TicketPolicy report TicketReport "
        "dashboard TicketDashboard chatbot SupportBot agent SupportAgent ERP accounts payable "
        "targets web mobile desktop"
    )
    plan = evolution_plan(sample)
    dsl_patch = proposals_to_dsl(plan)
    destructive = destructive_intent_report("remove field title from Ticket and drop table OldTicket")
    required_kinds = {
        "add_table",
        "add_field",
        "add_form",
        "add_workflow",
        "add_rule",
        "add_report",
        "add_dashboard",
        "add_chatbot",
        "add_agent",
        "add_erp_module",
        "set_targets",
    }
    observed_kinds = {item["kind"] for item in plan["proposals"]}
    gates = (
        {
            "id": "capability_contract",
            "ok": set(evolution_capabilities()["can_generate"]) >= {"database_tables", "forms", "agents", "erp_modules"},
        },
        {"id": "proposal_coverage", "ok": required_kinds <= observed_kinds, "observed": tuple(sorted(observed_kinds))},
        {
            "id": "dsl_patch",
            "ok": all(fragment in dsl_patch for fragment in ("table Ticket", "view TicketForm", "flow Triage", "agent SupportAgent")),
        },
        {"id": "local_and_api_llms", "ok": "mode: local" in dsl_patch and "api_key: OPENAI_API_KEY" in dsl_patch},
        {"id": "destructive_guard", "ok": destructive["requires_approval"] is True},
        {"id": "erp_bridge", "ok": "appgen --erp-template accounts_payable" in dsl_patch},
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.nl-evolution-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "gates": gates,
        "sample_plan": plan,
        "sample_dsl": dsl_patch,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
    }


def _requested_table(prompt: str) -> str:
    match = re.search(r"\b(?:table|entity|model)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)", prompt, re.I)
    if match:
        return _canonical_name(match.group("name"))
    return DEFAULT_TABLE


def _field_specs(prompt: str) -> tuple[dict, ...]:
    match = re.search(
        r"\bfields?\s+(?P<body>.*?)(?=\b(?:and\s+)?(?:form|view|workflow|flow|rule|policy|report|dashboard|chatbot|bot|agent|assistant|erp|targets?)\b|$)",
        prompt,
        re.I,
    )
    if not match:
        return ()
    fields = []
    for part in re.split(r"\s*,\s*|\s+and\s+", match.group("body")):
        tokens = tuple(token for token in re.split(r"\s+", part.strip()) if token)
        if not tokens:
            continue
        name = _snake_name(tokens[0])
        if not name or name in {"and", "with"}:
            continue
        token_text = " ".join(tokens[1:]).lower()
        fields.append(
            {
                "name": name,
                "type": _infer_type(name, token_text),
                "required": "required" in token_text or name in {"name", "title", "code"},
                "search": name in {"name", "title", "code", "email"},
            }
        )
    return tuple(fields)


def _target_specs(prompt: str) -> tuple[str, ...]:
    match = re.search(r"\btargets?\s+(?P<body>[A-Za-z0-9_,\s-]+)", prompt, re.I)
    if not match:
        return ()
    targets = []
    for raw in re.split(r"[\s,]+", match.group("body").lower()):
        target = raw.strip().replace("-", "_")
        if target in SUPPORTED_TARGETS and target not in targets:
            targets.append(target)
    return tuple(targets)


def _erp_modules(prompt: str) -> tuple[str, ...]:
    text = prompt.lower().replace("-", " ")
    aliases = {
        "accounts payable": "accounts_payable",
        "ap": "accounts_payable",
        "accounts receivable": "accounts_receivable",
        "ar": "accounts_receivable",
        "general ledger": "general_ledger",
        "ledger": "general_ledger",
        "chart of accounts": "chart_of_accounts",
        "hr": "human_resources",
        "human resources": "human_resources",
    }
    modules = []
    if "erp" not in text and not any(alias in text for alias in aliases):
        return ()
    for alias, module in aliases.items():
        if re.search(rf"\b{re.escape(alias)}\b", text) and module not in modules:
            modules.append(module)
    for module in ERP_MODULES:
        if module.replace("_", " ") in text and module not in modules:
            modules.append(module)
    return tuple(modules)


def _named_after(prompt: str, words: tuple[str, ...]) -> str | None:
    pattern = "|".join(re.escape(word) for word in words)
    match = re.search(rf"\b(?:{pattern})\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)", prompt, re.I)
    return _canonical_name(match.group("name")) if match else None


def _mentions_any(prompt: str, words: tuple[str, ...]) -> bool:
    text = prompt.lower()
    return any(re.search(rf"\b{re.escape(word)}s?\b", text) for word in words)


def _proposal_table_names(proposals: tuple[dict, ...]) -> tuple[str, ...]:
    names = []
    for proposal in proposals:
        if proposal.get("kind") == "add_table":
            names.append(proposal["name"])
        elif "table" in proposal:
            names.append(proposal["table"])
    return tuple(dict.fromkeys(names))


def _proposal_targets(proposals: tuple[dict, ...]) -> tuple[str, ...]:
    for proposal in proposals:
        if proposal.get("kind") == "set_targets":
            return tuple(proposal["targets"])
    return ()


def _fields_by_table(table_names: tuple[str, ...], proposals: tuple[dict, ...]) -> dict[str, tuple[dict, ...]]:
    result = {}
    for table in table_names:
        fields = [
            {"name": proposal["name"], "type": proposal["type"], "required": proposal.get("required", False), "search": proposal.get("search", False)}
            for proposal in proposals
            if proposal.get("kind") == "add_field" and proposal.get("table") == table
        ]
        if not fields:
            fields.append({"name": "name", "type": "string", "required": True, "search": True})
        result[table] = tuple(fields)
    return result


def _field_to_dsl(field: dict) -> str:
    modifiers = []
    if field.get("required"):
        modifiers.append("required")
    if field.get("search"):
        modifiers.append("search")
    suffix = f" {' '.join(modifiers)}" if modifiers else ""
    return f"{field['name']}: {field['type']}{suffix}"


def _component_for_field(field_name: str) -> str:
    if field_name.endswith("_date") or field_name.endswith("_on"):
        return "DatePicker"
    if "amount" in field_name or "quantity" in field_name:
        return "NumberInput"
    if field_name in {"description", "notes", "summary"}:
        return "TextArea"
    return "TextBox"


def _first_business_field(fields: tuple[dict, ...]) -> str:
    for field in fields:
        if field["name"] != "id":
            return field["name"]
    return "id"


def _infer_type(name: str, hints: str) -> str:
    if any(token in hints for token in ("decimal", "money", "amount", "currency")) or "amount" in name or "price" in name:
        return "decimal"
    if "date" in hints or name.endswith("_date") or name.endswith("_on"):
        return "date"
    if "datetime" in hints or name.endswith("_at"):
        return "datetime"
    if "email" in hints or "email" in name:
        return "email"
    if "text" in hints or name in {"description", "notes", "summary"}:
        return "text"
    if "int" in hints or name.endswith("_count"):
        return "int"
    if "bool" in hints or name.startswith("is_") or name.startswith("has_"):
        return "bool"
    return "string"


def _canonical_name(value: str) -> str:
    snake = _snake_name(value)
    return "".join(part.capitalize() for part in snake.split("_") if part) or DEFAULT_TABLE


def _snake_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip())
    value = re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()
    return re.sub(r"_+", "_", value).strip("_")
