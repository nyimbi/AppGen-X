# AppGen DSL Grammar

The AppGen DSL is an ANTLR-backed language for describing data models, forms,
workflows, roles, rules, LLM providers, agents, and target platforms with a
small keyword budget.

The canonical grammar lives in `lang/appgen.g4`. This document explains the
supported surface in user-facing terms.

## Top Level

```antlr
schema  : appDecl? element* EOF ;
element : tableDecl
        | groupDecl
        | enumDecl
        | relationDecl
        | viewDecl
        | flowDecl
        | roleDecl
        | ruleDecl
        | llmDecl
        | agentDecl ;
```

A file may start with an `app` block and then any number of declarations.

```appgen
app Library { theme: sage; targets: web, mobile, desktop }
```

## Tables And Fields

```antlr
tableDecl : TABLE IDENT tableBody ;
fieldDecl : IDENT COLON typeRef derivedExpr? modifier* SEMI? ;
typeRef   : IDENT (LPAREN INT RPAREN)? (LBRACK RBRACK)? ;
```

```appgen
table Book {
  id: int pk
  title: string required search
  tags: string[]
  score: decimal = rating * 2
}
```

Field modifiers are `pk`, `required`, `unique`, `hidden`, `search`,
`default`, and references.

## References

Prefer arrow references. They preserve readability without spending more
keywords.

```appgen
table Book {
  author_id: int required -> Author.id [many-to-one]
}
```

External relation declarations are also supported:

```appgen
Book.author_id -> Author.id [many-to-one]
```

Allowed cardinalities are `many-to-one`, `one-to-one`, `one-to-many`, and
`many-to-many`.

## Reusable Groups

Groups are named field blocks. Use `...Name` to spread them into tables.

```appgen
Audit {
  created_at: datetime required
  updated_at: datetime
}

table Invoice {
  id: int pk
  ...Audit
}
```

## Enums

```appgen
enum Status { draft published archived }
```

Use enum names as field types.

## Views And Delphi-Style Components

```antlr
viewDecl           : VIEW IDENT FOR IDENT LBRACE viewItem* RBRACE ;
componentPlacement : AT IDENT IDENT INT INT INT INT SEMI? ;
```

```appgen
view BookForm for Book {
  Main: title, author_id;
  @ title TextBox 0 0 6 1;
  @ author_id Lookup 0 1 6 1;
}
```

The component placement format is:

```text
@ field Component x y w h
```

## Workflows

```appgen
flow Publish {
  draft -> published
  published -> archived
}
```

## Roles

```appgen
role Editor {
  Book: read, create, update
}
```

## Rules

```appgen
rule PublishPolicy for Book {
  title required "Title is required"
  status in draft, published -> review
}
```

Supported operators are `==`, `!=`, `>=`, `<=`, `>`, `<`, and `in`.

## LLMs And Agents

```appgen
llm LocalModel {
  provider: ollama
  mode: local
  model: llama3
}

llm CloudModel {
  provider: openai
  mode: api
  model: gpt-4.1-mini
  api_key: OPENAI_API_KEY
}

agent Reviewer {
  provider: LocalModel
  goal: "Review submitted records"
  tools: schema, forms, reports
}
```

API keys should be environment variable names, not literal secrets.

## Comments

```appgen
// line comment
# line comment
/* block comment */
```

