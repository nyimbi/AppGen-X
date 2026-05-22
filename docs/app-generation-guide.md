# App Generation Guide

This guide explains how to generate applications from each supported source and
how to review the generated output.

## Install

```console
pip install appgen
```

For repository development:

```console
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

## Generate From AppGen DSL

Create `invoice.appgen`:

```appgen
app InvoiceDesk { theme: sage; targets: web, pwa, mobile, desktop }

table Customer {
  id: int pk
  name: string required search
  email: email unique
}

table Invoice {
  id: int pk
  invoice_number: string required unique search
  customer_id: int required -> Customer.id [many-to-one]
  status: string default "draft"
}
```

Lint and generate:

```console
appgen --lint-dsl invoice.appgen
appgen --dsl invoice.appgen --writedir generated/invoice/app
```

## Generate From DBML

```console
appgen --dbml schema.dbml --writedir generated/dbml-app/app
```

DBML intake preserves tables, fields, enums, primary keys, unique constraints,
relations, composite reference pairings, `TableGroup` source grouping metadata,
and literal defaults where the source provides them.

## Generate From SQL

```console
appgen --sql schema.sql --writedir generated/sql-app/app
```

SQL intake supports primary keys, foreign keys, unique constraints, indexes,
defaults, generated columns, schema-qualified references, PostgreSQL enum
types, enum-like `CHECK IN` domains, and post-create `ALTER TABLE` constraints.

## Generate From PonyORM

```console
appgen --pony entities.py --writedir generated/pony-app/app
```

PonyORM intake is static. AppGen parses entity declarations instead of executing
the script. `PrimaryKey`, `Required`, `Optional`, direct entity references,
`Set(...)`, composite primary keys, unique metadata, indexes, defaults, Python
enums, `Decimal`, `LongStr`, `Json`, and module-qualified datetime types are
normalized into the generated schema.

## Generate From A Live Database

```console
appgen --database-url sqlite:///existing.db --writedir generated/db-app/app
appgen --database-url postgresql+psycopg2://user@host/db --writedir generated/db-app/app
appgen --database-url mysql+pymysql://user@host/db --writedir generated/db-app/app
```

Live database introspection uses SQLAlchemy metadata. It preserves reflected
tables, primary keys, foreign keys, single-column unique constraints, unique
indexes, ordinary indexes as search hints, computed columns, server defaults,
and exposed enum metadata.

## Generate From Natural Language

Use natural language to plan and produce reviewable DSL patches:

```console
appgen --nl-plan "Add customer support tickets, a TicketForm, a SupportAgent, and target web mobile desktop"
appgen --nl-dsl "Add customer support tickets, a TicketForm, a SupportAgent, and target web mobile desktop"
```

Natural-language evolution can propose database tables, fields, forms,
workflows, reports, dashboards, chatbots, agents, ERP modules, and target
changes. Review the plan and generated DSL before committing it.

## Generate ERP Starters

List available ERP templates:

```console
appgen --erp-template-catalog
```

Export a starter:

```console
appgen --erp-template invoicing > invoicing.appgen
appgen --dsl invoicing.appgen --writedir generated/invoicing/app
```

ERP templates cover ledgers, accounts, invoicing, accounts payable, accounts
receivable, inventory, purchasing, sales, HR, payroll, CRM, projects, assets,
tax, reporting, and approvals.

## Review Generated Output

After generation, inspect:

- `app/appgen.json` for source fingerprint, source type, and generation
  metadata.
- `app/models.py`, `app/views.py`, `app/api.py`, and `app/gql.py` for the main
  web application surface.
- `app/studio.py` for generated IDE/management contracts.
- `app/dsl_reference.py` for generated language guidance and linter helpers.
- `app/form_designer.py` for form component layout and RAD-style design
  contracts.
- `app/branding.py` for theme tokens, splash screens, editable menus,
  right-click/context menus, accessibility, responsive UI contracts, and visual
  release gates.
- `app/designer.py` for visual database modeling, ERD, and schema refactor
  contracts.
- `app/agents.py` for local/API LLM providers and agent workbench payloads.
- `app/platforms.py`, `native/`, PWA assets, and `chatbots/` for target output.
- `deploy/`, `Dockerfile`, and `docker-compose.yml` for operations.

## Validate The Generated App

Run package-level source and target audits:

```console
appgen --source-intake-release-audit
appgen --target-release-audit
appgen --generated-app-excellence-audit
```

Run the full package objective proof:

```console
appgen --package-goal-audit
```

Generated code should also be compiled or tested in the target project:

```console
python -m py_compile generated/invoice/app/app/*.py
```

## Regeneration Strategy

Keep source files authoritative:

- Commit DSL, DBML, SQL, PonyORM, or database migration sources.
- Regenerate into a clean output directory when possible.
- Keep hand-written extensions isolated from generated files.
- Use natural-language output as a proposal, then commit the resulting DSL.
- Run the relevant release audit after changing source adapters, DSL grammar,
  Studio contracts, target output, deployment assets, or ERP templates.
