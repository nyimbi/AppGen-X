# AppGen DSL Grammar

The AppGen DSL is an ANTLR-backed language for describing data models, forms,
workflows, roles, rules, LLM providers, agents, and target platforms with a
small keyword budget. The canonical grammar lives in `lang/appgen.g4`; this
document is the human reference for that grammar and the validation semantics
enforced by `pyAppGen.dsl`.

## Complete Grammar

This is the supported language surface, grouped by construct. Semicolons are
accepted in most declaration bodies, but newlines are enough because whitespace
is skipped by the lexer.

### Top Level

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

Application options use generic `key: value` pairs so the language can grow
without adding new reserved words.

```antlr
appDecl   : APP (IDENT | STRING)? appBlock? ;
appBlock  : LBRACE appOption* RBRACE ;
appOption : IDENT COLON literal (COMMA literal)* SEMI? ;
```

Dotted row-level security targets are accepted in the `rls` app option as
authoring sugar and normalized to literal option values before parsing.

```appgen
app FieldOps { rls: Project.org_id, Invoice.account_id }
```

Validation then checks that every `Table.field` target exists. Generated
tenancy helpers and PostgreSQL RLS policy SQL use the explicit field before
falling back to conventional tenant field names.

## Keyword-Free Authoring Aliases

The canonical grammar keeps only the core keywords listed below, but the
package parser performs a pre-ANTLR normalization pass for approachable
authoring aliases:

| Alias | Canonical Form |
| --- | --- |
| `entity` | `table` |
| `model` | `table` |
| `form` | `view` |
| `screen` | `view` |
| `workflow` | `flow` |

For example, this source parses as if the canonical words had been written:

```appgen
entity Customer {
  id: int pk
  name: string required
}

form CustomerForm for Customer {
  Main: name
}

workflow Onboard {
  draft -> active
}
```

The linter reports aliases and can rewrite them with
`normalize_authoring_aliases`. The grammar file does not define `ENTITY`,
`FORM`, or `WORKFLOW` tokens, so these helpers improve learnability without
expanding the keyword budget.

The canonical grammar source lives at `lang/appgen.g4`; generated parser files
live under `src/pyAppGen/dsl_generated/lang/`.

## Tables And Fields

```antlr
tableDecl : TABLE IDENT tableBody ;
tableBody : LBRACE tableItem* RBRACE ;
tableItem : fieldDecl | spreadDecl | relationDecl ;
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

```antlr
modifier : PK
         | REQUIRED
         | UNIQUE
         | HIDE
         | SEARCH
         | DEFAULT literal
         | REF target relationCardinality?
         | ARROW target relationCardinality? ;
```

Derived fields use infix expressions over literals, fields, and qualified
targets.

```antlr
derivedExpr    : EQ expression ;
expression     : expressionAtom (operator expressionAtom)* ;
expressionAtom : target | literal | LPAREN expression RPAREN ;
operator       : PLUS | MINUS | STAR | SLASH ;
```

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

```antlr
relationDecl        : REF? target ARROW target relationCardinality? SEMI? ;
relationCardinality : LBRACK agenticValue RBRACK ;
target              : IDENT DOT IDENT ;
```

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

```antlr
groupDecl  : IDENT tableBody ;
spreadDecl : ELLIPSIS IDENT SEMI? ;
```

## Enums

```appgen
enum Status { draft published archived }
```

Use enum names as field types.

```antlr
enumDecl : ENUM IDENT LBRACE IDENT* RBRACE ;
```

## Views And Delphi-Style Components

```antlr
viewDecl           : VIEW IDENT FOR IDENT LBRACE viewItem* RBRACE ;
viewItem           : componentPlacement
                   | IDENT (COLON IDENT (COMMA IDENT)* | (COMMA IDENT)*) SEMI? ;
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

This is the Delphi-style component placement form: a component is dropped on a
named form field with grid coordinates and dimensions. The generated form
designer uses those coordinates for canvas placement, overlap checks, and
property-inspector metadata.

## Workflows

```appgen
flow Publish {
  draft -> published
  published -> archived
}
```

```antlr
flowDecl : FLOW IDENT LBRACE flowStep* RBRACE ;
flowStep : IDENT ARROW IDENT SEMI? ;
```

## Roles

```appgen
role Editor {
  Book: read, create, update
}
```

```antlr
roleDecl   : ROLE IDENT LBRACE permission* RBRACE ;
permission : IDENT COLON IDENT (COMMA IDENT)* SEMI? ;
```

## Rules

```appgen
rule PublishPolicy for Book {
  title required "Title is required"
  status in draft, published -> review
}
```

Supported operators are `==`, `!=`, `>=`, `<=`, `>`, `<`, and `in`.

```antlr
ruleDecl     : RULE IDENT FOR IDENT LBRACE ruleItem* RBRACE ;
ruleItem     : IDENT REQUIRED STRING? SEMI?
             | IDENT ruleOperator ruleValue (ARROW IDENT)? SEMI? ;
ruleValue    : literal (COMMA literal)* ;
ruleOperator : EQEQ | NEQ | GTE | LTE | GT | LT | IN ;
```

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

```antlr
llmDecl       : LLM IDENT LBRACE agenticOption* RBRACE ;
agentDecl     : AGENT IDENT LBRACE agenticOption* RBRACE ;
agenticOption : IDENT COLON agenticValue (COMMA agenticValue)* SEMI? ;
agenticValue  : literal ((DOT | MINUS) literal)* ;
```

The grammar intentionally does not reserve provider-specific option names.
Common options include `provider`, `mode`, `endpoint`, `model`, `api_key`,
`goal`, `tools`, `memory`, and `max_steps`.

## Lexical Rules

Identifiers start with a letter or underscore and may contain letters, digits,
and underscores. Strings may be single-quoted or double-quoted. Integers and
decimals are separate token types.

```antlr
literal : STRING | DECIMAL | INT | BOOL | IDENT ;
BOOL    : 'true' | 'false' ;
DECIMAL : [0-9]+ '.' [0-9]+ ;
INT     : [0-9]+ ;
IDENT   : [A-Za-z_][A-Za-z0-9_]* ;
STRING  : '"' ( '\\' . | ~["\\] )* '"'
        | '\'' ( '\\' . | ~['\\] )* '\'' ;
```

Reserved words are: `app`, `table`, `ref`, `enum`, `view`, `for`, `flow`,
`role`, `rule`, `llm`, `agent`, `pk`, `required`, `unique`, `hidden`,
`search`, `default`, and `in`.

## Comments

```appgen
// line comment
# line comment
/* block comment */
```

## Semantic Validation

Parsing is only the first gate. The package linter also validates:

- supported app targets: `web`, `pwa`, `mobile`, `desktop`, and `chatbot`;
- duplicate table, enum, view, flow, role, rule, LLM provider, and agent names;
- duplicate fields after group spreads are expanded;
- relation source and target tables/fields;
- field-level reference targets;
- derived-field references;
- view section fields and Delphi-style component fields;
- role resources and rule table/field references;
- agent provider names when LLM providers are declared;
- relation cardinality values.
