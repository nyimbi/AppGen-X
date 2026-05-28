# Learning AppGen-X: A 100-Page Textbook

This textbook is a long-form learning path for AppGen-X. It is organized as one hundred explicit pages so teams can assign readings, cite sections in reviews, and use the material as a structured onboarding course. Each page focuses on one practical idea and connects that idea to the AppGen-X DSL.

The book assumes you want to generate and manage serious enterprise applications: web, mobile, desktop, chatbot, service, worker, and composable PBC-based systems. The examples use finance, operations, supply chain, HR, and commerce patterns because those domains exercise the language surface deeply.

Read it in order the first time. On later passes, use the page titles as a field guide while reviewing DSL changes from humans or agents.

## Page 001. The AppGen-X Mindset

AppGen-X treats enterprise software as explicit, lintable intent. The DSL records the decisions that must survive regeneration: what data exists, who can use it, which screens edit it, which processes move it, which agents may act on it, and how it is packaged and deployed.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 002. A Small Language For Large Systems

The language stays small at the parser layer so humans and small local models can edit it safely. Structural blocks describe stable platform concepts, while contextual directives let teams express domain detail without turning every business noun into a global keyword.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 003. Applications As Durable Intent

Generated code changes as frameworks evolve, but business intent should remain durable. A concise AppGen-X source file can outlive UI rewrites, service packaging changes, database migration tooling, and agent implementation strategies.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
view ExampleForm for Example {
  Main: code, name
  @ code TextBox 0 0 4 1
  on Save -> SaveExample
}
```

## Page 004. Tables As Business Memory

Tables capture durable business facts. A good table has identity, business keys, required fields, relationship fields, calculated fields where useful, and directives that explain search, lookup, indexes, and constraints.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 005. Relationships And Lookup Paths

Relationships drive more than database constraints. They create lookup controls, joins, report groupings, navigation, validation, and display labels. Multi-hop paths are powerful, but only when each hop is declared and unambiguous.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 006. Forms As Lintable UI

A visual form can still be textually reviewable. Sections explain information architecture, component placements explain the design surface, and handlers connect user actions to named behavior.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
pbc ExampleCapability {
  domain: operations
  owns: Example
  exposes ExampleApi -> public
}
```

## Page 007. Handlers And Operations

Button handlers, menu commands, and right-click actions should route to operations, flows, or agents. This prevents duplicated UI code and gives generated class/component architecture a stable call graph.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 008. Rules As Policy

Rules keep validation and policy close to the model. They should be small, testable, and attached to a clear subject. A rule that cannot be explained in one sentence usually needs to be split.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 009. Workflows As Enterprise Motion

Flows describe work over time: states, transitions, human tasks, timers, escalation, compensation, and evidence. They are the bridge between data records and real operating processes.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
app EnterpriseOps { targets: web, mobile, desktop; database: postgresql }
```

## Page 010. Roles And Security

Security belongs in the DSL because generated software needs consistent behavior across APIs, screens, menus, reports, background jobs, and agents. Roles and security blocks make that behavior reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 011. Agentic Systems

Agents are safe only when tools, model backends, permissions, and skills are declared. AppGen-X treats agents as constrained application actors rather than invisible shortcuts around the domain model.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 012. PBC Thinking

A Packaged Business Capability is a bounded business capability with its own data ownership, contracts, and lifecycle. It should be independently buildable, testable, deployable, and composable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
rule ExamplePolicy for Example {
  code required "Code is required"
  name is not null
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 013. Composition

Composition assembles PBCs into applications by version and contract. It records what is included, what is required, what is exposed, and how capabilities connect through APIs, events, and commands.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 014. Deployment Patterns

A capability may run in-process, as a service, as a worker, as a scheduled job, or as an edge unit. Deployment blocks make topology explicit so packaging, operations, and tests can follow.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 015. Packaging

Packaging is part of the product contract. Web, mobile, desktop, chatbot, service, and worker outputs need declared targets, formats, signing posture, startup behavior, splash assets, menus, and update policy.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
composition ExampleSuite {
  include pbc ExampleCapability version 1.0.0
  require database postgresql
}
```

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 016. Natural Language Evolution

Natural language should change applications by producing a DSL diff first. The diff is the safety boundary: it can be linted, reviewed, committed, regenerated, and tested before code spreads.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 017. Token-Efficient Generation

Small models perform better when the task is represented as constrained DSL edits. Ask for narrow changes: add a field, add a view, add a lookup, add a rule, add an agent skill, or connect two PBCs.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 018. Enterprise Scale

Enterprise platforms are repeated patterns: ledgers, accounts, invoices, HR records, inventory, procurement, manufacturing, commerce, reports, roles, workflows, integrations, and operational controls.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
table Example {
  id: int pk
  code: string required unique search
  name: string required search
}
```

## Page 019. Quality And Evidence

Generated platforms must emit evidence. Linter output, migrations, tests, package descriptors, release metadata, audit policy, and deployment checks prove that generation produced something reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 020. Working With Agents

External coding agents can build PBCs safely when the PBC specification is complete. Ownership, contracts, datastore, events, APIs, tests, deployment, and self-registration must all be declared.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 021. The AppGen-X Mindset

AppGen-X treats enterprise software as explicit, lintable intent. The DSL records the decisions that must survive regeneration: what data exists, who can use it, which screens edit it, which processes move it, which agents may act on it, and how it is packaged and deployed.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
flow ExampleApproval {
  draft -> submitted
  human Review assigned Reviewer -> approved
}
```

## Page 022. A Small Language For Large Systems

The language stays small at the parser layer so humans and small local models can edit it safely. Structural blocks describe stable platform concepts, while contextual directives let teams express domain detail without turning every business noun into a global keyword.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 023. Applications As Durable Intent

Generated code changes as frameworks evolve, but business intent should remain durable. A concise AppGen-X source file can outlive UI rewrites, service packaging changes, database migration tooling, and agent implementation strategies.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 024. Tables As Business Memory

Tables capture durable business facts. A good table has identity, business keys, required fields, relationship fields, calculated fields where useful, and directives that explain search, lookup, indexes, and constraints.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
deploy Production {
  unit example as service
  health example "/health"
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 025. Relationships And Lookup Paths

Relationships drive more than database constraints. They create lookup controls, joins, report groupings, navigation, validation, and display labels. Multi-hop paths are powerful, but only when each hop is declared and unambiguous.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 026. Forms As Lintable UI

A visual form can still be textually reviewable. Sections explain information architecture, component placements explain the design surface, and handlers connect user actions to named behavior.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 027. Handlers And Operations

Button handlers, menu commands, and right-click actions should route to operations, flows, or agents. This prevents duplicated UI code and gives generated class/component architecture a stable call graph.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
view ExampleForm for Example {
  Main: code, name
  @ code TextBox 0 0 4 1
  on Save -> SaveExample
}
```

## Page 028. Rules As Policy

Rules keep validation and policy close to the model. They should be small, testable, and attached to a clear subject. A rule that cannot be explained in one sentence usually needs to be split.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 029. Workflows As Enterprise Motion

Flows describe work over time: states, transitions, human tasks, timers, escalation, compensation, and evidence. They are the bridge between data records and real operating processes.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 030. Roles And Security

Security belongs in the DSL because generated software needs consistent behavior across APIs, screens, menus, reports, background jobs, and agents. Roles and security blocks make that behavior reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
pbc ExampleCapability {
  domain: operations
  owns: Example
  exposes ExampleApi -> public
}
```

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 031. Agentic Systems

Agents are safe only when tools, model backends, permissions, and skills are declared. AppGen-X treats agents as constrained application actors rather than invisible shortcuts around the domain model.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 032. PBC Thinking

A Packaged Business Capability is a bounded business capability with its own data ownership, contracts, and lifecycle. It should be independently buildable, testable, deployable, and composable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 033. Composition

Composition assembles PBCs into applications by version and contract. It records what is included, what is required, what is exposed, and how capabilities connect through APIs, events, and commands.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
app EnterpriseOps { targets: web, mobile, desktop; database: postgresql }
```

## Page 034. Deployment Patterns

A capability may run in-process, as a service, as a worker, as a scheduled job, or as an edge unit. Deployment blocks make topology explicit so packaging, operations, and tests can follow.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 035. Packaging

Packaging is part of the product contract. Web, mobile, desktop, chatbot, service, and worker outputs need declared targets, formats, signing posture, startup behavior, splash assets, menus, and update policy.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 036. Natural Language Evolution

Natural language should change applications by producing a DSL diff first. The diff is the safety boundary: it can be linted, reviewed, committed, regenerated, and tested before code spreads.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
rule ExamplePolicy for Example {
  code required "Code is required"
  name is not null
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 037. Token-Efficient Generation

Small models perform better when the task is represented as constrained DSL edits. Ask for narrow changes: add a field, add a view, add a lookup, add a rule, add an agent skill, or connect two PBCs.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 038. Enterprise Scale

Enterprise platforms are repeated patterns: ledgers, accounts, invoices, HR records, inventory, procurement, manufacturing, commerce, reports, roles, workflows, integrations, and operational controls.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 039. Quality And Evidence

Generated platforms must emit evidence. Linter output, migrations, tests, package descriptors, release metadata, audit policy, and deployment checks prove that generation produced something reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
composition ExampleSuite {
  include pbc ExampleCapability version 1.0.0
  require database postgresql
}
```

## Page 040. Working With Agents

External coding agents can build PBCs safely when the PBC specification is complete. Ownership, contracts, datastore, events, APIs, tests, deployment, and self-registration must all be declared.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 041. The AppGen-X Mindset

AppGen-X treats enterprise software as explicit, lintable intent. The DSL records the decisions that must survive regeneration: what data exists, who can use it, which screens edit it, which processes move it, which agents may act on it, and how it is packaged and deployed.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 042. A Small Language For Large Systems

The language stays small at the parser layer so humans and small local models can edit it safely. Structural blocks describe stable platform concepts, while contextual directives let teams express domain detail without turning every business noun into a global keyword.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
table Example {
  id: int pk
  code: string required unique search
  name: string required search
}
```

## Page 043. Applications As Durable Intent

Generated code changes as frameworks evolve, but business intent should remain durable. A concise AppGen-X source file can outlive UI rewrites, service packaging changes, database migration tooling, and agent implementation strategies.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 044. Tables As Business Memory

Tables capture durable business facts. A good table has identity, business keys, required fields, relationship fields, calculated fields where useful, and directives that explain search, lookup, indexes, and constraints.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 045. Relationships And Lookup Paths

Relationships drive more than database constraints. They create lookup controls, joins, report groupings, navigation, validation, and display labels. Multi-hop paths are powerful, but only when each hop is declared and unambiguous.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
flow ExampleApproval {
  draft -> submitted
  human Review assigned Reviewer -> approved
}
```

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 046. Forms As Lintable UI

A visual form can still be textually reviewable. Sections explain information architecture, component placements explain the design surface, and handlers connect user actions to named behavior.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 047. Handlers And Operations

Button handlers, menu commands, and right-click actions should route to operations, flows, or agents. This prevents duplicated UI code and gives generated class/component architecture a stable call graph.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 048. Rules As Policy

Rules keep validation and policy close to the model. They should be small, testable, and attached to a clear subject. A rule that cannot be explained in one sentence usually needs to be split.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
deploy Production {
  unit example as service
  health example "/health"
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 049. Workflows As Enterprise Motion

Flows describe work over time: states, transitions, human tasks, timers, escalation, compensation, and evidence. They are the bridge between data records and real operating processes.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 050. Roles And Security

Security belongs in the DSL because generated software needs consistent behavior across APIs, screens, menus, reports, background jobs, and agents. Roles and security blocks make that behavior reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 051. Agentic Systems

Agents are safe only when tools, model backends, permissions, and skills are declared. AppGen-X treats agents as constrained application actors rather than invisible shortcuts around the domain model.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
view ExampleForm for Example {
  Main: code, name
  @ code TextBox 0 0 4 1
  on Save -> SaveExample
}
```

## Page 052. PBC Thinking

A Packaged Business Capability is a bounded business capability with its own data ownership, contracts, and lifecycle. It should be independently buildable, testable, deployable, and composable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 053. Composition

Composition assembles PBCs into applications by version and contract. It records what is included, what is required, what is exposed, and how capabilities connect through APIs, events, and commands.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 054. Deployment Patterns

A capability may run in-process, as a service, as a worker, as a scheduled job, or as an edge unit. Deployment blocks make topology explicit so packaging, operations, and tests can follow.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
pbc ExampleCapability {
  domain: operations
  owns: Example
  exposes ExampleApi -> public
}
```

## Page 055. Packaging

Packaging is part of the product contract. Web, mobile, desktop, chatbot, service, and worker outputs need declared targets, formats, signing posture, startup behavior, splash assets, menus, and update policy.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 056. Natural Language Evolution

Natural language should change applications by producing a DSL diff first. The diff is the safety boundary: it can be linted, reviewed, committed, regenerated, and tested before code spreads.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 057. Token-Efficient Generation

Small models perform better when the task is represented as constrained DSL edits. Ask for narrow changes: add a field, add a view, add a lookup, add a rule, add an agent skill, or connect two PBCs.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
app EnterpriseOps { targets: web, mobile, desktop; database: postgresql }
```

## Page 058. Enterprise Scale

Enterprise platforms are repeated patterns: ledgers, accounts, invoices, HR records, inventory, procurement, manufacturing, commerce, reports, roles, workflows, integrations, and operational controls.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 059. Quality And Evidence

Generated platforms must emit evidence. Linter output, migrations, tests, package descriptors, release metadata, audit policy, and deployment checks prove that generation produced something reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 060. Working With Agents

External coding agents can build PBCs safely when the PBC specification is complete. Ownership, contracts, datastore, events, APIs, tests, deployment, and self-registration must all be declared.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
rule ExamplePolicy for Example {
  code required "Code is required"
  name is not null
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 061. The AppGen-X Mindset

AppGen-X treats enterprise software as explicit, lintable intent. The DSL records the decisions that must survive regeneration: what data exists, who can use it, which screens edit it, which processes move it, which agents may act on it, and how it is packaged and deployed.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 062. A Small Language For Large Systems

The language stays small at the parser layer so humans and small local models can edit it safely. Structural blocks describe stable platform concepts, while contextual directives let teams express domain detail without turning every business noun into a global keyword.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 063. Applications As Durable Intent

Generated code changes as frameworks evolve, but business intent should remain durable. A concise AppGen-X source file can outlive UI rewrites, service packaging changes, database migration tooling, and agent implementation strategies.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
composition ExampleSuite {
  include pbc ExampleCapability version 1.0.0
  require database postgresql
}
```

## Page 064. Tables As Business Memory

Tables capture durable business facts. A good table has identity, business keys, required fields, relationship fields, calculated fields where useful, and directives that explain search, lookup, indexes, and constraints.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 065. Relationships And Lookup Paths

Relationships drive more than database constraints. They create lookup controls, joins, report groupings, navigation, validation, and display labels. Multi-hop paths are powerful, but only when each hop is declared and unambiguous.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 066. Forms As Lintable UI

A visual form can still be textually reviewable. Sections explain information architecture, component placements explain the design surface, and handlers connect user actions to named behavior.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
table Example {
  id: int pk
  code: string required unique search
  name: string required search
}
```

## Page 067. Handlers And Operations

Button handlers, menu commands, and right-click actions should route to operations, flows, or agents. This prevents duplicated UI code and gives generated class/component architecture a stable call graph.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 068. Rules As Policy

Rules keep validation and policy close to the model. They should be small, testable, and attached to a clear subject. A rule that cannot be explained in one sentence usually needs to be split.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 069. Workflows As Enterprise Motion

Flows describe work over time: states, transitions, human tasks, timers, escalation, compensation, and evidence. They are the bridge between data records and real operating processes.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
flow ExampleApproval {
  draft -> submitted
  human Review assigned Reviewer -> approved
}
```

## Page 070. Roles And Security

Security belongs in the DSL because generated software needs consistent behavior across APIs, screens, menus, reports, background jobs, and agents. Roles and security blocks make that behavior reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 071. Agentic Systems

Agents are safe only when tools, model backends, permissions, and skills are declared. AppGen-X treats agents as constrained application actors rather than invisible shortcuts around the domain model.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 072. PBC Thinking

A Packaged Business Capability is a bounded business capability with its own data ownership, contracts, and lifecycle. It should be independently buildable, testable, deployable, and composable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
deploy Production {
  unit example as service
  health example "/health"
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 073. Composition

Composition assembles PBCs into applications by version and contract. It records what is included, what is required, what is exposed, and how capabilities connect through APIs, events, and commands.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 074. Deployment Patterns

A capability may run in-process, as a service, as a worker, as a scheduled job, or as an edge unit. Deployment blocks make topology explicit so packaging, operations, and tests can follow.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 075. Packaging

Packaging is part of the product contract. Web, mobile, desktop, chatbot, service, and worker outputs need declared targets, formats, signing posture, startup behavior, splash assets, menus, and update policy.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
view ExampleForm for Example {
  Main: code, name
  @ code TextBox 0 0 4 1
  on Save -> SaveExample
}
```

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 076. Natural Language Evolution

Natural language should change applications by producing a DSL diff first. The diff is the safety boundary: it can be linted, reviewed, committed, regenerated, and tested before code spreads.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 077. Token-Efficient Generation

Small models perform better when the task is represented as constrained DSL edits. Ask for narrow changes: add a field, add a view, add a lookup, add a rule, add an agent skill, or connect two PBCs.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 078. Enterprise Scale

Enterprise platforms are repeated patterns: ledgers, accounts, invoices, HR records, inventory, procurement, manufacturing, commerce, reports, roles, workflows, integrations, and operational controls.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
pbc ExampleCapability {
  domain: operations
  owns: Example
  exposes ExampleApi -> public
}
```

## Page 079. Quality And Evidence

Generated platforms must emit evidence. Linter output, migrations, tests, package descriptors, release metadata, audit policy, and deployment checks prove that generation produced something reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 080. Working With Agents

External coding agents can build PBCs safely when the PBC specification is complete. Ownership, contracts, datastore, events, APIs, tests, deployment, and self-registration must all be declared.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 081. The AppGen-X Mindset

AppGen-X treats enterprise software as explicit, lintable intent. The DSL records the decisions that must survive regeneration: what data exists, who can use it, which screens edit it, which processes move it, which agents may act on it, and how it is packaged and deployed.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
app EnterpriseOps { targets: web, mobile, desktop; database: postgresql }
```

## Page 082. A Small Language For Large Systems

The language stays small at the parser layer so humans and small local models can edit it safely. Structural blocks describe stable platform concepts, while contextual directives let teams express domain detail without turning every business noun into a global keyword.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 083. Applications As Durable Intent

Generated code changes as frameworks evolve, but business intent should remain durable. A concise AppGen-X source file can outlive UI rewrites, service packaging changes, database migration tooling, and agent implementation strategies.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 084. Tables As Business Memory

Tables capture durable business facts. A good table has identity, business keys, required fields, relationship fields, calculated fields where useful, and directives that explain search, lookup, indexes, and constraints.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
rule ExamplePolicy for Example {
  code required "Code is required"
  name is not null
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 085. Relationships And Lookup Paths

Relationships drive more than database constraints. They create lookup controls, joins, report groupings, navigation, validation, and display labels. Multi-hop paths are powerful, but only when each hop is declared and unambiguous.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 086. Forms As Lintable UI

A visual form can still be textually reviewable. Sections explain information architecture, component placements explain the design surface, and handlers connect user actions to named behavior.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 087. Handlers And Operations

Button handlers, menu commands, and right-click actions should route to operations, flows, or agents. This prevents duplicated UI code and gives generated class/component architecture a stable call graph.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
composition ExampleSuite {
  include pbc ExampleCapability version 1.0.0
  require database postgresql
}
```

## Page 088. Rules As Policy

Rules keep validation and policy close to the model. They should be small, testable, and attached to a clear subject. A rule that cannot be explained in one sentence usually needs to be split.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 089. Workflows As Enterprise Motion

Flows describe work over time: states, transitions, human tasks, timers, escalation, compensation, and evidence. They are the bridge between data records and real operating processes.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 090. Roles And Security

Security belongs in the DSL because generated software needs consistent behavior across APIs, screens, menus, reports, background jobs, and agents. Roles and security blocks make that behavior reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
table Example {
  id: int pk
  code: string required unique search
  name: string required search
}
```

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Page 091. Agentic Systems

Agents are safe only when tools, model backends, permissions, and skills are declared. AppGen-X treats agents as constrained application actors rather than invisible shortcuts around the domain model.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 092. PBC Thinking

A Packaged Business Capability is a bounded business capability with its own data ownership, contracts, and lifecycle. It should be independently buildable, testable, deployable, and composable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 093. Composition

Composition assembles PBCs into applications by version and contract. It records what is included, what is required, what is exposed, and how capabilities connect through APIs, events, and commands.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
flow ExampleApproval {
  draft -> submitted
  human Review assigned Reviewer -> approved
}
```

## Page 094. Deployment Patterns

A capability may run in-process, as a service, as a worker, as a scheduled job, or as an edge unit. Deployment blocks make topology explicit so packaging, operations, and tests can follow.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 095. Packaging

Packaging is part of the product contract. Web, mobile, desktop, chatbot, service, and worker outputs need declared targets, formats, signing posture, startup behavior, splash assets, menus, and update policy.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

## Page 096. Natural Language Evolution

Natural language should change applications by producing a DSL diff first. The diff is the safety boundary: it can be linted, reviewed, committed, regenerated, and tested before code spreads.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
deploy Production {
  unit example as service
  health example "/health"
}
```

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

## Page 097. Token-Efficient Generation

Small models perform better when the task is represented as constrained DSL edits. Ask for narrow changes: add a field, add a view, add a lookup, add a rule, add an agent skill, or connect two PBCs.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 098. Enterprise Scale

Enterprise platforms are repeated patterns: ledgers, accounts, invoices, HR records, inventory, procurement, manufacturing, commerce, reports, roles, workflows, integrations, and operational controls.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

## Page 099. Quality And Evidence

Generated platforms must emit evidence. Linter output, migrations, tests, package descriptors, release metadata, audit policy, and deployment checks prove that generation produced something reviewable.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Example pattern:

```appgen
view ExampleForm for Example {
  Main: code, name
  @ code TextBox 0 0 4 1
  on Save -> SaveExample
}
```

## Page 100. Working With Agents

External coding agents can build PBCs safely when the PBC specification is complete. Ownership, contracts, datastore, events, APIs, tests, deployment, and self-registration must all be declared.

The central habit is to write the smallest contract that captures the business decision. A contract may be a table, a view, a rule, a workflow, an operation, a PBC, a deployment unit, or a package. Once the contract exists, the linter can validate references, the generator can emit artifacts, and reviewers can reason about behavior without reverse-engineering handwritten code.

Practitioner note: keep business vocabulary stable and implementation vocabulary flexible. Names such as `Invoice`, `StockBalance`, `Employee`, `JournalEntry`, and `Customer` should be clear to a domain expert. Details such as service names, package formats, model providers, and deployment units can evolve as platform policy matures.

Review checklist: ask whether the page's idea has an owner, a boundary, a generated artifact, a validation rule, and an operational consequence. If any answer is missing, write the missing intent in the DSL before asking an agent to generate or modify code.

Common mistake: allowing a natural-language request to skip the DSL and edit generated code directly. That creates behavior that may disappear on regeneration and cannot be checked by the language linter. Capture the change as DSL first, then regenerate.

Reflection: identify the table, view, flow, rule, PBC, deployment unit, or package that owns the concept on this page. If the answer is unclear, the model probably needs a clearer boundary.

Exercise: make a one-screen DSL change that demonstrates this page. Lint it, inspect the generated diff, and write down the semantic check that protected you from an invalid model. Commit the DSL change separately from any generated output so reviewers can see intent first.

## Appendix A. Course Project

Build a composable operations suite with these PBCs: General Ledger, Accounts Payable, Accounts Receivable, Inventory Positioning, Procurement, Personnel Directory, Time Tracking, Product Catalog, and Customer Engagement. Each PBC must declare owned tables, contracts, emitted events, consumed events, operations, roles, tests, and deployment units.

## Appendix B. Review Rubric

A complete AppGen-X submission should answer these questions: Are all database-backed form fields real columns, calculated fields, or lookup paths? Are multi-table foreign-key chains declared? Are lookup controls generated for relationship fields? Are handlers routed through operations or flows? Are PBCs integrated through contracts instead of private tables? Are deployment and package targets explicit? Are LLMs and agents constrained by declared permissions? Are generated tests present?

## Appendix C. Agent Assignment Template

When assigning another agent to build a PBC, provide the PBC name, business purpose, owned tables, events emitted, events consumed, APIs exposed, workflows, reports, roles, security policy, deployment pattern, package outputs, test expectations, and self-registration requirements. Require the agent to return a DSL diff first, followed by implementation changes and verification evidence.

## Appendix D. Next Reading

After this textbook, read the language manual for exact syntax and gotchas, then read the one-hour tutorial again while building the course project from scratch.
