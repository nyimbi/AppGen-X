# AppGen DSL Grammar

The AppGen DSL is an ANTLR-backed language for describing enterprise data
models, forms, workflows, roles, rules, LLM providers, agents, PBC composition,
APIs, events, jobs, reports, menus, reusable components, packages, tests, and
target platforms with a small keyword budget. The canonical grammar lives in
`lang/appgen.g4`; this document is the human reference for that grammar and the
validation semantics enforced by `pyAppGen.dsl`.

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
        | agentDecl
        | pbcDecl
        | compositionDecl
        | auditDecl
        | deploymentDecl
        | versionDecl
        | operationDecl
        | securityDecl
        | apiDecl
        | eventDecl
        | jobDecl
        | reportDecl
        | menuDecl
        | componentDecl
        | packageDecl
        | testDecl ;
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
Field modifier aliases are handled the same way: `searchable` becomes `search`
and `hide` becomes `hidden` through `normalize_modifier_aliases`; the grammar
does not add separate `SEARCHABLE` or `HIDE` tokens.

`pyAppGen.dsl.dsl_language_quality_contract()` exposes this as a machine-readable
contract with the grammar path, generated parser path, keyword budget, keyword-free
syntax list, authoring aliases, and four-step learning path. Generated apps expose
the same evidence through `app/dsl_reference.py` and
`/dsl-reference/language-quality.json`.
`pyAppGen.dsl.dsl_antlr_integrity_report()` is the stricter drift check: it
compares `lang/appgen.g4` with the generated ANTLR lexer/parser token and rule
metadata, verifies that compact keyword literals still match, and reports any
missing parser tokens, lexer tokens, parser rules, required rules, or keyword
literal mismatches before generation is trusted.
`pyAppGen.dsl.dsl_authoring_score()` complements the quality contract with
weighted IDE checks and next actions for complete, canonical, formatted DSL
source without increasing the keyword budget.

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
`default`, and references. Arrow references are the canonical form. The legacy
`ref` token remains accepted for existing projects and is linted to the arrow
form, but it is not counted as a canonical keyword.

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

## Views And RAD-Style Components

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

This is the RAD-style component placement form: a component is dropped on a
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
             | ruleExpression (ARROW IDENT)? SEMI? ;
ruleExpression : ruleTerm ((ruleOperator | IDENT) ruleTerm (COMMA ruleTerm)*)* ;
ruleTerm       : qualifiedName | literal | LPAREN ruleExpression RPAREN ;
ruleOperator : EQEQ | NEQ | GTE | LTE | GT | LT | IN ;
```

Rules can use compact boolean expressions such as
`status == posted and amount > 0 -> Review`.

## Enterprise Contracts

Enterprise software contracts use typed top-level blocks while keeping detailed
domain words as identifiers, options, or arrow statements.

```appgen
api JournalsApi {
  GET "/journals" -> PostJournal
  auth: Journal.read
}

event JournalPosted {
  publish JournalPosted -> PostJournal
  topic: pbc.gl_core.events
}

job NightlyClose {
  daily -> CloseBooks
  retry: 3
}

report TrialBalance {
  source: Journal
  export: csv, pdf
}

menu MainMenu {
  on Open -> PostJournal
}

component StatusBadge {
  on Click -> PostJournal
  prop: status
}

package DesktopMobileWeb {
  targets: web, mobile, desktop
  channel: stable
}

test JournalSmoke {
  run happy_path -> PostJournal
  assert: ok
}
```

```antlr
apiDecl       : API IDENT LBRACE contractItem* RBRACE ;
eventDecl     : EVENT IDENT LBRACE contractItem* RBRACE ;
jobDecl       : JOB IDENT LBRACE contractItem* RBRACE ;
reportDecl    : REPORT IDENT LBRACE contractItem* RBRACE ;
menuDecl      : MENU IDENT LBRACE contractItem* RBRACE ;
componentDecl : COMPONENT IDENT LBRACE contractItem* RBRACE ;
packageDecl   : PACKAGE IDENT LBRACE contractItem* RBRACE ;
testDecl      : TEST IDENT LBRACE contractItem* RBRACE ;
contractItem  : handlerDecl | contractArrow | permission | agenticOption ;
handlerDecl   : IDENT IDENT ARROW IDENT SEMI? ;
contractArrow : IDENT agenticValue* ARROW IDENT SEMI? ;
```

The linter validates handler and contract arrow targets against declared flows,
operations, and enterprise contracts. Package targets must normalize to
supported platform targets.

## Deployment Topology

`deploy` blocks can describe whether each PBC or operation runs as a
microservice, process, worker, function, module, sidecar, embedded unit, or
monolith. Deployment topology words are contextual statements inside `deploy`;
they do not add new global keywords.

```appgen
deploy Production {
  runtime: kubernetes
  mesh: mtls
  unit gl_core as microservice
  unit CloseBooks as process
  unit NightlyClose as worker
  scale gl_core min 2 max 10
  health gl_core "/healthz"
  check gl_core readiness "/readyz"
}
```

```antlr
deploymentDecl : DEPLOY IDENT LBRACE deploymentItem* RBRACE ;
deploymentItem : deployUnit | deployScale | deployHealth | deployCheck | agenticOption ;
deployUnit     : IDENT IDENT IDENT IDENT SEMI? ;
deployScale    : IDENT IDENT IDENT INT IDENT INT SEMI? ;
deployHealth   : IDENT IDENT STRING SEMI? ;
deployCheck    : IDENT IDENT IDENT STRING SEMI? ;
```

Semantic validation checks that deployment unit, scale, health, and check
targets resolve to declared PBCs, operations, flows, or enterprise contracts.
Supported deployment patterns are `microservice`, `process`, `worker`, `job`,
`function`, `module`, `sidecar`, `embedded`, and `monolith`.

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

Canonical reserved words are: `app`, `table`, `enum`, `view`, `for`, `flow`,
`role`, `rule`, `pbc`, `composition`, `audit`, `deploy`, `version`,
`operation`, `security`, `api`, `event`, `job`, `report`, `menu`, `component`,
`package`, `test`, `llm`, `agent`, `pk`, `required`, `unique`, `hidden`,
`search`, `default`, and `in`.

Legacy compatibility token: `ref`. It remains parse-compatible so older DSL
files can be upgraded in place, but `dsl_language_quality_contract()` excludes
it from the canonical keyword list and the linter offers `replace_ref_with_arrow`.

## Comments

```appgen
// line comment
# line comment
/* block comment */
```

## Semantic Validation

Parsing is only the first gate. The package linter also validates:

- supported app targets: `web`, `pwa`, `mobile`, `desktop`, and `chatbot`;
- duplicate table, enum, view, flow, role, rule, LLM provider, agent, and
  enterprise contract names;
- duplicate fields after group spreads are expanded;
- relation source and target tables/fields;
- field-level reference targets;
- derived-field references;
- view section fields and RAD-style component fields;
- role resources and rule table/field references;
- agent provider names when LLM providers are declared;
- relation cardinality values;
- handler and contract targets;
- package targets;
- deployment topology targets, scale ranges, and supported deployment patterns.
