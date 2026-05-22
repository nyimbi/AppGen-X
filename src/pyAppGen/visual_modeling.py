"""Package-level visual modeling and database-design contracts."""

from __future__ import annotations

from .dsl import schema_from_dsl


VISUAL_MODEL_SAMPLE_DSL = """
app VisualModelAudit { targets: web, mobile, desktop }

table Author {
  id: int pk
  name: string required
}

table Book {
  id: int pk
  title: string required search
  author_id: int -> Author.id [many-to-one]
}

flow Publish {
  draft -> review
  review -> published
}
"""


def visual_schema(source: str = VISUAL_MODEL_SAMPLE_DSL) -> dict:
    """Parse DSL into the package-level visual modeling schema."""
    schema = schema_from_dsl(source, source_name="visual-model-audit.appgen")
    return {
        "format": "appgen.package-visual-schema.v1",
        "app": schema.app_name,
        "tables": tuple(
            {
                "name": table.name,
                "fields": tuple(
                    {
                        "name": column.name,
                        "type": column.type_name,
                        "primary_key": column.primary_key,
                        "required": not column.nullable,
                        "references": column.references,
                    }
                    for column in table.columns
                ),
            }
            for table in schema.tables
        ),
        "flows": tuple(
            {"name": flow.name, "steps": tuple((step.source, step.target) for step in flow.steps)}
            for flow in schema.flows
        ),
        "relations": tuple(
            {
                "table": relation.source_table,
                "field": relation.source_column,
                "target_table": relation.target_table,
                "target_field": relation.target_column,
                "cardinality": relation.cardinality,
            }
            for relation in schema.relations
        ),
    }


def visual_graph(source: str = VISUAL_MODEL_SAMPLE_DSL) -> dict:
    """Return graph nodes and edges for a visual schema designer."""
    model = visual_schema(source)
    nodes = tuple(
        {"id": table["name"], "type": "table", "label": table["name"]}
        for table in model["tables"]
    ) + tuple(
        {"id": flow["name"], "type": "flow", "label": flow["name"]}
        for flow in model["flows"]
    )
    edges = tuple(
        {
            "source": relation["table"],
            "target": relation["target_table"],
            "field": relation["field"],
            "type": "relationship",
            "cardinality": relation["cardinality"],
        }
        for relation in model["relations"]
    ) + tuple(
        {
            "source": source,
            "target": target,
            "type": "workflow",
            "flow": flow["name"],
        }
        for flow in model["flows"]
        for source, target in flow["steps"]
    )
    return {
        "format": "appgen.package-visual-graph.v1",
        "ok": bool(nodes) and any(edge["type"] == "relationship" for edge in edges),
        "nodes": nodes,
        "edges": edges,
    }


def erd_mermaid(source: str = VISUAL_MODEL_SAMPLE_DSL) -> str:
    """Return Mermaid ERD generated from the visual model."""
    model = visual_schema(source)
    lines = ["erDiagram"]
    for table in model["tables"]:
        lines.append(f"  {table['name']} {{")
        for field in table["fields"]:
            key = " PK" if field["primary_key"] else ""
            lines.append(f"    {field['type']} {field['name']}{key}")
        lines.append("  }")
    for relation in model["relations"]:
        lines.append(
            f"  {relation['target_table']} ||--o{{ {relation['table']} : {relation['field']}"
        )
    return "\n".join(lines) + "\n"


def visual_model_exports(source: str = VISUAL_MODEL_SAMPLE_DSL) -> dict:
    """Return DBML, SQL, PonyORM, and DSL exports from a visual model."""
    model = visual_schema(source)
    return {
        "format": "appgen.package-visual-model-exports.v1",
        "dsl": source.strip() + "\n",
        "dbml": _dbml(model),
        "sql": _sql(model),
        "ponyorm": _ponyorm(model),
        "ok": True,
    }


def table_proposal(name: str, fields: tuple[dict, ...] = ()) -> dict:
    """Return a reviewable visual table proposal."""
    proposal_fields = fields or ({"name": "name", "type": "string", "required": True},)
    return {
        "format": "appgen.package-visual-table-proposal.v1",
        "kind": "add_table",
        "name": name,
        "fields": proposal_fields,
        "dsl": _table_dsl(name, proposal_fields),
        "review_required": True,
    }


def field_proposal(table: str, name: str, type_name: str = "string", *, required: bool = False) -> dict:
    """Return a reviewable visual field proposal."""
    flags = " required" if required else ""
    return {
        "format": "appgen.package-visual-field-proposal.v1",
        "kind": "add_field",
        "table": table,
        "name": name,
        "type": type_name,
        "dsl": f"  {name}: {type_name}{flags}",
        "review_required": True,
    }


def relationship_proposal(
    source_table: str,
    source_field: str,
    target_table: str,
    target_field: str = "id",
    *,
    cardinality: str = "many-to-one",
) -> dict:
    """Return a reviewable visual relationship proposal."""
    return {
        "format": "appgen.package-visual-relationship-proposal.v1",
        "kind": "add_relationship",
        "source_table": source_table,
        "source_field": source_field,
        "target_table": target_table,
        "target_field": target_field,
        "cardinality": cardinality,
        "dsl": f"  {source_field}: int -> {target_table}.{target_field} [{cardinality}]",
        "review_required": True,
    }


def migration_preview(proposal: dict) -> dict:
    """Return the migration operations implied by a visual proposal."""
    if proposal["kind"] == "add_table":
        operations = ({"op": "create_table", "table": proposal["name"]},)
    elif proposal["kind"] == "add_field":
        operations = (
            {
                "op": "add_column",
                "table": proposal["table"],
                "column": proposal["name"],
                "type": proposal["type"],
            },
        )
    elif proposal["kind"] == "add_relationship":
        operations = (
            {
                "op": "add_column",
                "table": proposal["source_table"],
                "column": proposal["source_field"],
                "type": "int",
            },
            {
                "op": "add_foreign_key",
                "table": proposal["source_table"],
                "column": proposal["source_field"],
                "target": f"{proposal['target_table']}.{proposal['target_field']}",
            },
        )
    else:
        raise ValueError(f"Unknown visual proposal kind: {proposal['kind']}")
    return {
        "format": "appgen.package-visual-migration-preview.v1",
        "operations": operations,
        "requires_review": True,
        "rollback_plan": ("snapshot_schema", "apply_reverse_migration", "rerun_generation"),
    }


def code_generation_plan(proposal: dict) -> dict:
    """Return generated code/database artifacts affected by a visual model edit."""
    return {
        "format": "appgen.package-visual-code-generation-plan.v1",
        "proposal": proposal,
        "artifacts": (
            "appgen.dsl",
            "app/models.py",
            "app/views.py",
            "migrations/versions/*.py",
            "app/appgen.json",
        ),
        "checks": ("dsl_lint", "schema_diff", "migration_preview", "py_compile"),
        "review_required": True,
    }


def visual_modeling_release_audit(existing_paths: set[str] | None = None) -> dict:
    """Return package-level proof for visual modeling readiness."""
    existing = (
        {"app/designer.py", "app/templates/appgen_designer.html", "app/appgen.json"}
        if existing_paths is None
        else existing_paths
    )
    graph = visual_graph()
    exports = visual_model_exports()
    table = table_proposal("Publisher")
    field = field_proposal("Book", "subtitle", required=False)
    relation = relationship_proposal("Book", "publisher_id", "Publisher")
    migration = migration_preview(relation)
    generation = code_generation_plan(relation)
    gates = (
        {
            "id": "visual_graph",
            "ok": graph["ok"] and {"Author", "Book"} <= {node["id"] for node in graph["nodes"]},
        },
        {
            "id": "erd_export",
            "ok": erd_mermaid().startswith("erDiagram\n") and "Author ||--o{ Book" in erd_mermaid(),
        },
        {
            "id": "schema_exports",
            "ok": all(fragment in exports[key] for key, fragment in {
                "dbml": "Table Book",
                "sql": "CREATE TABLE Book",
                "ponyorm": "class Book(db.Entity)",
            }.items()),
        },
        {
            "id": "proposal_breadth",
            "ok": {table["kind"], field["kind"], relation["kind"]}
            == {"add_table", "add_field", "add_relationship"},
        },
        {
            "id": "migration_preview",
            "ok": migration["requires_review"] and migration["operations"][0]["op"] == "add_column",
        },
        {
            "id": "code_generation_plan",
            "ok": "app/models.py" in generation["artifacts"] and "migration_preview" in generation["checks"],
        },
        {
            "id": "artifact_contract",
            "ok": {"app/designer.py", "app/templates/appgen_designer.html", "app/appgen.json"} <= existing,
        },
    )
    ok = all(gate["ok"] for gate in gates)
    return {
        "format": "appgen.package-visual-modeling-release-audit.v1",
        "scope": "package",
        "ok": ok,
        "decision": "approved" if ok else "blocked",
        "graph": graph,
        "erd": erd_mermaid(),
        "exports": exports,
        "proposals": (table, field, relation),
        "migration": migration,
        "generation": generation,
        "gates": gates,
        "blocking_gaps": tuple(gate for gate in gates if not gate["ok"]),
        "stop_condition": "do-not-claim-visual-modeling-unless-ok-is-true",
    }


def _table_dsl(name: str, fields: tuple[dict, ...]) -> str:
    body = "\n".join(
        f"  {field['name']}: {field['type']}{' required' if field.get('required') else ''}"
        for field in fields
    )
    return f"table {name} {{\n{body}\n}}"


def _dbml(model: dict) -> str:
    lines = []
    for table in model["tables"]:
        lines.append(f"Table {table['name']} {{")
        for field in table["fields"]:
            flags = " [pk]" if field["primary_key"] else ""
            lines.append(f"  {field['name']} {field['type']}{flags}")
        lines.append("}")
    for relation in model["relations"]:
        lines.append(
            f"Ref: {relation['table']}.{relation['field']} > "
            f"{relation['target_table']}.{relation['target_field']}"
        )
    return "\n".join(lines) + "\n"


def _sql(model: dict) -> str:
    statements = []
    for table in model["tables"]:
        columns = []
        for field in table["fields"]:
            sql_type = {"string": "TEXT", "int": "INTEGER"}.get(field["type"], "TEXT")
            suffix = " PRIMARY KEY" if field["primary_key"] else ""
            if field["references"]:
                target_table, target_field = field["references"]
                suffix += f" REFERENCES {target_table}({target_field})"
            columns.append(f"  {field['name']} {sql_type}{suffix}")
        statements.append(f"CREATE TABLE {table['name']} (\n" + ",\n".join(columns) + "\n);")
    return "\n\n".join(statements) + "\n"


def _ponyorm(model: dict) -> str:
    lines = ["from pony.orm import Database, PrimaryKey, Required, Optional", "", "db = Database()"]
    for table in model["tables"]:
        lines.append("")
        lines.append(f"class {table['name']}(db.Entity):")
        for field in table["fields"]:
            if field["primary_key"]:
                lines.append(f"    {field['name']} = PrimaryKey(int)")
            elif field["references"]:
                lines.append(f"    {field['name']} = Optional('{field['references'][0]}')")
            elif field["required"]:
                lines.append(f"    {field['name']} = Required(str)")
            else:
                lines.append(f"    {field['name']} = Optional(str)")
    return "\n".join(lines) + "\n"
