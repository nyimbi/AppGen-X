# AppGen DSL User Guide

Use the AppGen DSL when you want a readable source of truth for generated
applications. The same DSL can drive database schema, forms, generated REST and
GraphQL APIs, PWA assets, mobile and desktop starters, chatbots, agents,
reports, ERP templates, deployment files, and quality checks.

## Minimal App

```appgen
app Library { theme: sage; targets: web, mobile, desktop }

table Author {
  id: int pk
  name: string required search
  email: string unique
}

table Book {
  id: int pk
  title: string required search
  author_id: int required -> Author.id [many-to-one]
}
```

Generate from the DSL:

```bash
appgen --dsl library.appgen --writedir generated/app
```

Lint without generating:

```bash
appgen --lint-dsl library.appgen
```

## Modeling Guidance

Use one table per business object. Use explicit `id: int pk` fields when you
want stable identifiers, or let AppGen add one when omitted.

Use `required` for fields that must be entered. Use `search` on fields that
should appear in generated search contracts. Use `hidden` for generated or
internal fields. Use `unique` for natural keys like invoice numbers and email
addresses.

Prefer arrow references:

```appgen
customer_id: int required -> Customer.id [many-to-one]
```

## Designing Forms

Basic form sections:

```appgen
view BookForm for Book {
  Main: title, author_id;
}
```

Delphi-style component placement:

```appgen
view BookForm for Book {
  @ title TextBox 0 0 8 1;
  @ author_id Lookup 0 1 8 1;
}
```

The generated form designer can use these placements for drag/drop previews,
snap-to-grid placement, overlap detection, and property sheets.

## Choosing Targets

Supported targets are `web`, `pwa`, `mobile`, `desktop`, and `chatbot`.

```appgen
app FieldOps { targets: web, pwa, mobile, desktop, chatbot }
```

`mobile` generates a Kivy starter. `desktop` generates a BeeWare starter.
`web` and `pwa` generate Flask-AppBuilder and PWA assets. `chatbot` generates
bot contracts and provider exports.

## Adding Behavior

Use `flow` for state transitions:

```appgen
flow Publish {
  draft -> published
  published -> archived
}
```

Use `rule` for validation and decisions:

```appgen
rule PublishPolicy for Book {
  title required "Title is required"
  status in draft, published -> review
}
```

Use `role` for generated access policies:

```appgen
role Editor {
  Book: read, create, update
}
```

## Agentic Systems

Declare LLM providers separately from agents. This makes local and API-backed
providers explicit and keeps API keys out of source.

```appgen
llm LocalOps {
  provider: ollama
  mode: local
  endpoint: http://localhost:11434
  model: llama3
}

llm CloudOps {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent InvoiceAssistant {
  provider: CloudOps
  goal: "Help users create and review invoices"
  tools: schema, forms, reports
}
```

## Natural Language Evolution

Generated apps include natural-language evolution contracts. A builder can ask
for changes such as:

```text
Create table Ticket with fields title and status, add TicketForm, add SupportBot,
and target web mobile desktop.
```

The generated change set must still be reviewed. AppGen treats natural language
as an authoring assistant, not as an unreviewed mutation path.

