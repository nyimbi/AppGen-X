"""ANTLR-backed parser for the AppGen low-code DSL."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Iterable

from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from .schema import AppSchema
from .schema import AgentSchema
from .schema import ColumnSchema
from .schema import EnumSchema
from .schema import FormComponentSchema
from .schema import FlowSchema
from .schema import FlowStepSchema
from .schema import LLMProviderSchema
from .schema import PermissionSchema
from .schema import RelationSchema
from .schema import RuleConditionSchema
from .schema import RuleSchema
from .schema import RoleSchema
from .schema import TableSchema
from .schema import ViewSchema
from .schema import ViewSectionSchema
from .schema import normalize_platform_targets


_GENERATED_DIR = Path(__file__).resolve().parent / "dsl_generated" / "lang"
if str(_GENERATED_DIR) not in sys.path:
    sys.path.insert(0, str(_GENERATED_DIR))

from appgenLexer import appgenLexer  # type: ignore  # noqa: E402
from appgenParser import appgenParser  # type: ignore  # noqa: E402


class AppGenSyntaxError(ValueError):
    """Raised when AppGen DSL parsing fails."""


class _CollectingErrorListener(ErrorListener):
    def __init__(self) -> None:
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # noqa: N802
        self.errors.append(f"{line}:{column}: {msg}")


def schema_from_dsl_file(path: str | Path) -> AppSchema:
    path = Path(path)
    return schema_from_dsl(path.read_text(), source_name=str(path))


def schema_from_dsl(text: str, *, source_name: str | None = None) -> AppSchema:
    """Parse AppGen DSL source into the canonical app schema."""
    text = _normalize_reference_sugar(text)
    tree = _parse(text)
    app_decl = tree.appDecl()
    app_name = _app_name(app_decl) if app_decl else None
    app_options = _app_options(app_decl) if app_decl else {}
    _validate_app_options(app_options)

    tables: list[TableSchema] = []
    relations: list[RelationSchema] = []
    views: list[ViewSchema] = []
    flows: list[FlowSchema] = []
    roles: list[RoleSchema] = []
    rules: list[RuleSchema] = []
    enums: list[EnumSchema] = []
    llm_providers: list[LLMProviderSchema] = []
    agents: list[AgentSchema] = []
    groups = {
        element.groupDecl().IDENT().getText(): element.groupDecl().tableBody()
        for element in tree.element()
        if element.groupDecl()
    }

    for element in tree.element():
        if element.tableDecl():
            table, table_relations = _table(element.tableDecl(), groups)
            tables.append(table)
            relations.extend(table_relations)
        elif element.relationDecl():
            relations.append(_relation(element.relationDecl()))
        elif element.enumDecl():
            enums.append(_enum(element.enumDecl()))
        elif element.viewDecl():
            views.append(_view(element.viewDecl()))
        elif element.flowDecl():
            flows.append(_flow(element.flowDecl()))
        elif element.roleDecl():
            roles.append(_role(element.roleDecl()))
        elif element.ruleDecl():
            rules.append(_rule(element.ruleDecl()))
        elif element.llmDecl():
            llm_providers.append(_llm_provider(element.llmDecl()))
        elif element.agentDecl():
            agents.append(_agent(element.agentDecl()))

    tables = _apply_external_relations(tables, relations)
    schema = AppSchema(
        tables=tuple(tables),
        relations=tuple(relations),
        source=source_name,
        app_name=app_name,
        app_options=app_options,
        views=tuple(views),
        flows=tuple(flows),
        roles=tuple(roles),
        rules=tuple(rules),
        enums=tuple(enums),
        llm_providers=tuple(llm_providers),
        agents=tuple(agents),
    )
    _validate_schema(schema)
    return schema


def _parse(source: str):
    lexer = appgenLexer(InputStream(source))
    parser = appgenParser(CommonTokenStream(lexer))
    errors = _CollectingErrorListener()
    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    lexer.addErrorListener(errors)
    parser.addErrorListener(errors)
    tree = parser.schema()
    if errors.errors:
        raise AppGenSyntaxError("; ".join(errors.errors))
    return tree


_FIELD_ARROW_REF_RE = re.compile(
    r"^(?P<prefix>\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*[A-Za-z_][A-Za-z0-9_]*(?:\([0-9]+\))?(?:\[\])?(?P<mods>(?:\s+(?!->)[^;\n]+?)?)?)\s*->\s*(?P<target>[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)(?P<cardinality>\s*\[[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)?\])?\s*(?P<suffix>;?\s*)$"
)
_EXTERNAL_ARROW_REF_RE = re.compile(
    r"^(?P<prefix>\s*)(?P<source>[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)\s*->\s*(?P<target>[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)(?P<cardinality>\s*\[[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)?\])?\s*(?P<suffix>;?\s*)$"
)


def _normalize_reference_sugar(source: str) -> str:
    """Normalize arrow reference sugar to the generated parser's legacy form."""
    normalized_lines = []
    for line in source.splitlines():
        field_match = _FIELD_ARROW_REF_RE.match(line)
        if field_match:
            normalized_lines.append(
                f"{field_match.group('prefix')} ref {field_match.group('target')}{field_match.group('cardinality') or ''}{field_match.group('suffix')}"
            )
            continue
        external_match = _EXTERNAL_ARROW_REF_RE.match(line)
        if external_match:
            normalized_lines.append(
                f"{external_match.group('prefix')}ref {external_match.group('source')} -> {external_match.group('target')}{external_match.group('cardinality') or ''}{external_match.group('suffix')}"
            )
            continue
        normalized_lines.append(line)
    return "\n".join(normalized_lines)


def _app_name(ctx) -> str | None:
    if ctx is None:
        return None
    ident = ctx.IDENT()
    if ident:
        return ident.getText()
    string = ctx.STRING()
    if string:
        return _literal_text(string.getText())
    return None


def _app_options(ctx) -> dict[str, str]:
    if ctx is None or ctx.appBlock() is None:
        return {}
    options = {}
    for option in ctx.appBlock().appOption():
        values = tuple(_literal(literal) for literal in option.literal())
        options[option.IDENT().getText()] = values[0] if len(values) == 1 else ",".join(values)
    return options


def _validate_app_options(app_options: dict[str, str]) -> None:
    if "targets" not in app_options:
        return
    targets, unknown = normalize_platform_targets(app_options["targets"])
    if unknown:
        known = ", ".join(normalize_platform_targets(None)[0])
        bad = ", ".join(unknown)
        raise AppGenSyntaxError(f"Unknown app targets: {bad}. Supported targets: {known}")
    if not targets:
        known = ", ".join(normalize_platform_targets(None)[0])
        raise AppGenSyntaxError(f"App targets cannot be empty. Supported targets: {known}")


def _validate_schema(schema: AppSchema) -> None:
    table_map = {table.name: table for table in schema.tables}
    field_map = {table.name: _field_names(table) for table in schema.tables}
    errors: list[str] = []

    errors.extend(_duplicate_name_errors("table", (table.name for table in schema.tables)))
    errors.extend(_duplicate_name_errors("enum", (enum.name for enum in schema.enums)))
    errors.extend(_duplicate_name_errors("view", (view.name for view in schema.views)))
    errors.extend(_duplicate_name_errors("flow", (flow.name for flow in schema.flows)))
    errors.extend(_duplicate_name_errors("role", (role.name for role in schema.roles)))
    errors.extend(_duplicate_name_errors("rule", (rule.name for rule in schema.rules)))
    errors.extend(
        _duplicate_name_errors("llm provider", (provider.name for provider in schema.llm_providers))
    )
    errors.extend(_duplicate_name_errors("agent", (agent.name for agent in schema.agents)))

    for relation in schema.relations:
        if relation.source_table not in table_map:
            errors.append(f"Unknown relation source table: {relation.source_table}")
            continue
        if relation.source_column not in field_map[relation.source_table]:
            errors.append(
                f"Unknown relation source field: {relation.source_table}.{relation.source_column}"
            )
        if relation.target_table not in table_map:
            errors.append(f"Unknown relation target table: {relation.target_table}")
            continue
        if relation.target_column not in field_map[relation.target_table]:
            errors.append(
                f"Unknown relation target field: {relation.target_table}.{relation.target_column}"
            )

    for table in schema.tables:
        for column in table.columns:
            if column.references:
                target_table, target_column = column.references
                if target_table not in table_map:
                    errors.append(f"Unknown reference target table: {target_table}")
                elif target_column not in field_map[target_table]:
                    errors.append(f"Unknown reference target field: {target_table}.{target_column}")
            if column.derived and column.expression:
                unknown = _unknown_expression_fields(column.expression, field_map[table.name])
                for field_name in unknown:
                    errors.append(
                        f"Unknown derived-field reference: {table.name}.{column.name} uses {field_name}"
                    )

    for view in schema.views:
        if view.table not in table_map:
            errors.append(f"Unknown view table: {view.name} for {view.table}")
            continue
        allowed = field_map[view.table]
        for field_name in view.fields:
            if field_name not in allowed:
                errors.append(f"Unknown view field: {view.name}.{field_name}")
        for component in view.components:
            if component.field and component.field not in allowed:
                errors.append(f"Unknown component field: {view.name}.{component.field}")

    for role in schema.roles:
        for permission in role.permissions:
            if permission.resource not in table_map:
                errors.append(f"Unknown role resource: {role.name}.{permission.resource}")

    for rule in schema.rules:
        if rule.table not in table_map:
            errors.append(f"Unknown rule table: {rule.name} for {rule.table}")
            continue
        allowed = field_map[rule.table]
        for condition in rule.conditions:
            if condition.field not in allowed:
                errors.append(f"Unknown rule field: {rule.name}.{condition.field}")

    provider_names = {provider.name for provider in schema.llm_providers}
    if provider_names:
        for agent in schema.agents:
            if agent.provider and agent.provider not in provider_names:
                errors.append(f"Unknown agent provider: {agent.name}.{agent.provider}")

    if errors:
        raise AppGenSyntaxError("; ".join(errors))


def _duplicate_name_errors(kind: str, names: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for name in names:
        if name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    return [f"Duplicate {kind} declaration: {name}" for name in duplicates]


def _field_names(table: TableSchema) -> set[str]:
    names = {column.name for column in table.columns}
    for column in table.columns:
        if column.references and column.name.endswith("_id"):
            names.add(column.name[:-3])
    return names


def _unknown_expression_fields(expression: str, known_fields: set[str]) -> tuple[str, ...]:
    unknown: list[str] = []
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expression):
        if token in {"true", "false"} or token in known_fields:
            continue
        if token not in unknown:
            unknown.append(token)
    return tuple(unknown)


def _table(ctx, groups) -> tuple[TableSchema, list[RelationSchema]]:
    table_name = ctx.IDENT().getText()
    columns, relations = _table_items(table_name, ctx.tableBody(), groups)
    columns = _dedupe_columns(table_name, columns)

    if not any(column.primary_key for column in columns):
        columns.insert(0, ColumnSchema("id", "int", nullable=False, primary_key=True))
    return TableSchema(table_name, tuple(columns)), relations


def _table_items(table_name: str, body_ctx, groups, stack=()) -> tuple[list[ColumnSchema], list[RelationSchema]]:
    columns: list[ColumnSchema] = []
    relations: list[RelationSchema] = []

    for item in body_ctx.tableItem():
        if item.fieldDecl():
            source_group = stack[-1] if stack else None
            column, relation = _field(table_name, item.fieldDecl(), source_group=source_group)
            columns.append(column)
            if relation is not None:
                relations.append(relation)
        elif item.spreadDecl():
            group_name = item.spreadDecl().IDENT().getText()
            if group_name not in groups:
                raise AppGenSyntaxError(f"Unknown field group: {group_name}")
            if group_name in stack:
                cycle = " -> ".join((*stack, group_name))
                raise AppGenSyntaxError(f"Cyclic field group spread: {cycle}")
            group_columns, group_relations = _table_items(
                table_name, groups[group_name], groups, (*stack, group_name)
            )
            columns.extend(group_columns)
            relations.extend(group_relations)
        elif item.relationDecl():
            relations.append(_relation(item.relationDecl()))
    return columns, relations


def _dedupe_columns(table_name: str, columns: list[ColumnSchema]) -> list[ColumnSchema]:
    ordered: list[ColumnSchema] = []
    positions: dict[str, int] = {}
    for column in columns:
        if column.name in positions:
            existing = ordered[positions[column.name]]
            if existing.source_group and column.source_group is None:
                ordered[positions[column.name]] = column
                continue
            if existing.source_group and column.source_group:
                raise AppGenSyntaxError(
                    f"Duplicate field declaration: {table_name}.{column.name} "
                    f"from {existing.source_group} and {column.source_group}"
                )
            raise AppGenSyntaxError(f"Duplicate field declaration: {table_name}.{column.name}")
            continue
        positions[column.name] = len(ordered)
        ordered.append(column)
    return ordered


def _field(table_name: str, ctx, *, source_group: str | None = None) -> tuple[ColumnSchema, RelationSchema | None]:
    column_name = ctx.IDENT().getText()
    type_name = ctx.typeRef().getText()
    nullable = True
    primary_key = False
    unique = False
    default = None
    references = None
    reference_cardinality = "many-to-one"
    hidden = False
    searchable = False
    expression = None

    if ctx.derivedExpr():
        expression = ctx.derivedExpr().expression().getText()
        nullable = False
        hidden = True

    for modifier in ctx.modifier():
        text = modifier.getText()
        if text == "pk":
            primary_key = True
            nullable = False
        elif text == "required":
            nullable = False
        elif text == "unique":
            unique = True
        elif text == "hidden":
            hidden = True
        elif text == "search":
            searchable = True
        elif modifier.DEFAULT():
            default = _literal(modifier.literal())
        elif modifier.REF():
            target = _target(modifier.target())
            references = target
            reference_cardinality = _relation_cardinality(modifier.relationCardinality())

    relation = None
    if references is not None:
        relation = RelationSchema(
            source_table=table_name,
            source_column=column_name,
            target_table=references[0],
            target_column=references[1],
            cardinality=reference_cardinality,
        )

    return (
        ColumnSchema(
            name=column_name,
            type_name=type_name,
            nullable=nullable,
            primary_key=primary_key,
            unique=unique,
            default=default,
            references=references,
            hidden=hidden,
            searchable=searchable,
            derived=expression is not None,
            expression=expression,
            source_group=source_group,
        ),
        relation,
    )


def _relation(ctx) -> RelationSchema:
    source_target, target_target = ctx.target()
    source_table, source_column = _target(source_target)
    target_table, target_column = _target(target_target)
    return RelationSchema(
        source_table=source_table,
        source_column=source_column,
        target_table=target_table,
        target_column=target_column,
        cardinality=_relation_cardinality(ctx.relationCardinality()),
    )


def _relation_cardinality(ctx) -> str:
    if ctx is None:
        return "many-to-one"
    value = _agentic_value(ctx.agenticValue()).replace("_", "-").lower()
    allowed = {"many-to-one", "one-to-one", "one-to-many", "many-to-many"}
    if value not in allowed:
        known = ", ".join(sorted(allowed))
        raise AppGenSyntaxError(f"Unknown relation cardinality: {value}. Supported: {known}")
    return value


def _enum(ctx) -> EnumSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    return EnumSchema(identifiers[0], tuple(identifiers[1:]))


def _view(ctx) -> ViewSchema:
    fields: list[str] = []
    sections: list[ViewSectionSchema] = []
    components: list[FormComponentSchema] = []
    for item in ctx.viewItem():
        if item.componentPlacement():
            components.append(_component_placement(item.componentPlacement()))
            continue
        identifiers = [token.getText() for token in item.IDENT()]
        if item.COLON():
            section_fields = tuple(identifiers[1:])
            sections.append(ViewSectionSchema(identifiers[0], section_fields))
            fields.extend(section_fields)
        else:
            fields.extend(identifiers)
    view_name = ctx.IDENT(0).getText()
    return ViewSchema(
        view_name,
        ctx.IDENT(1).getText(),
        tuple(fields),
        tuple(sections),
        tuple(components),
    )


def _component_placement(ctx) -> FormComponentSchema:
    identifiers = [token.getText() for token in ctx.IDENT()]
    numbers = [int(token.getText()) for token in ctx.INT()]
    return FormComponentSchema(
        name=identifiers[0],
        component=identifiers[1],
        field=identifiers[0],
        x=numbers[0],
        y=numbers[1],
        w=numbers[2],
        h=numbers[3],
    )


def _flow(ctx) -> FlowSchema:
    steps = []
    for step in ctx.flowStep():
        source, target = [token.getText() for token in step.IDENT()]
        steps.append(FlowStepSchema(source, target))
    return FlowSchema(ctx.IDENT().getText(), tuple(steps))


def _role(ctx) -> RoleSchema:
    permissions = []
    for permission in ctx.permission():
        identifiers = [token.getText() for token in permission.IDENT()]
        permissions.append(PermissionSchema(identifiers[0], tuple(identifiers[1:])))
    return RoleSchema(ctx.IDENT().getText(), tuple(permissions))


def _rule(ctx) -> RuleSchema:
    identifiers = ctx.IDENT()
    conditions = []
    for item in ctx.ruleItem():
        field_name = item.IDENT(0).getText()
        if item.REQUIRED():
            message = _literal_text(item.STRING().getText()) if item.STRING() else None
            conditions.append(
                RuleConditionSchema(
                    field=field_name,
                    operator="required",
                    message=message,
                )
            )
            continue
        values = tuple(_literal(literal) for literal in item.ruleValue().literal())
        action = item.IDENT(1).getText() if len(item.IDENT()) > 1 else None
        conditions.append(
            RuleConditionSchema(
                field=field_name,
                operator=item.ruleOperator().getText(),
                values=values,
                action=action,
            )
        )
    return RuleSchema(identifiers[0].getText(), identifiers[1].getText(), tuple(conditions))


def _llm_provider(ctx) -> LLMProviderSchema:
    options = _agentic_options(ctx)
    return LLMProviderSchema(
        name=ctx.IDENT().getText(),
        provider=options.get("provider", ("openai",))[0],
        mode=options.get("mode", ("api",))[0],
        model=_first_or_none(options.get("model")),
        endpoint=_first_or_none(options.get("endpoint")),
        api_key=_first_or_none(options.get("api_key")),
    )


def _agent(ctx) -> AgentSchema:
    options = _agentic_options(ctx)
    max_steps = _first_or_none(options.get("max_steps")) or "8"
    return AgentSchema(
        name=ctx.IDENT().getText(),
        provider=_first_or_none(options.get("provider")),
        goal=_first_or_none(options.get("goal")),
        tools=options.get("tools", ()),
        memory=_first_or_none(options.get("memory")) or "session",
        max_steps=int(max_steps),
    )


def _agentic_options(ctx) -> dict[str, tuple[str, ...]]:
    options: dict[str, tuple[str, ...]] = {}
    for option in ctx.agenticOption():
        values = tuple(_agentic_value(value) for value in option.agenticValue())
        options[option.IDENT().getText()] = values
    return options


def _agentic_value(ctx) -> str:
    text = "".join(token.getText() for token in ctx.children)
    if text.startswith(("\"", "'")):
        return _literal_text(text)
    return text


def _first_or_none(values: tuple[str, ...] | None) -> str | None:
    if not values:
        return None
    return values[0]


def _target(ctx) -> tuple[str, str]:
    table, column = ctx.IDENT()
    return table.getText(), column.getText()


def _literal(ctx) -> str:
    return _literal_text(ctx.getText())


def _literal_text(text: str) -> str:
    if text.startswith(("\"", "'")):
        return ast.literal_eval(text)
    return text


def _apply_external_relations(
    tables: list[TableSchema], relations: list[RelationSchema]
) -> list[TableSchema]:
    relation_map = {
        (relation.source_table, relation.source_column): relation for relation in relations
    }
    updated_tables: list[TableSchema] = []

    for table in tables:
        columns = []
        for column in table.columns:
            relation = relation_map.get((table.name, column.name))
            if relation is None or column.references is not None:
                columns.append(column)
                continue
            columns.append(
                ColumnSchema(
                    name=column.name,
                    type_name=column.type_name,
                    nullable=column.nullable,
                    primary_key=column.primary_key,
                    unique=column.unique,
                    default=column.default,
                    references=(relation.target_table, relation.target_column),
                    hidden=column.hidden,
                    searchable=column.searchable,
                    derived=column.derived,
                    expression=column.expression,
                    source_group=column.source_group,
                )
            )
        updated_tables.append(TableSchema(table.name, tuple(columns)))
    return updated_tables
