# AppGen-X DSL Tooling Roadmap

AppGen-X needs a full DSL tooling stack, not just a grammar. The platform
should make authoring, reviewing, generating, packaging, and evolving
applications feel safe and integrated across the CLI, IDE, language server,
visual designers, and agent workflows.

## Required Tooling

1. **Language server**
   - Syntax errors as you type.
   - Semantic validation for missing tables, invalid fields, broken lookup
     paths, and bad handler targets.
   - Completion for keywords, table names, fields, components, flows, roles,
     PBCs, APIs, events, packages, and deployment units.
   - Hover documentation for keywords, directives, generated artifacts, and
     platform conventions.
   - Go-to-definition for table, view, flow, operation, PBC, event, API, role,
     package, and deployment references.
   - Find references across DSL files and generated-contract indexes.
   - Safe symbol rename.
   - Code actions such as create missing table, create operation from handler,
     create event contract, add lookup directive, and add deployment unit.
   - Formatting support.

2. **Linter**
   - Parse validation.
   - Duplicate table, field, view, flow, operation, role, and PBC checks.
   - Invalid relationship target checks.
   - Invalid database-backed form field checks.
   - Invalid multi-hop lookup path checks.
   - Unknown handler target checks.
   - Unknown PBC, event, API, package, and deployment references.
   - Missing package, deployment, audit, version, and test evidence.
   - Naming and style rules.
   - Enterprise safety rules for secret literals, cross-PBC private table
     access, undeclared permissions, unsafe agent tools, and undeclared data
     ownership.

3. **Formatter**
   - Stable block ordering.
   - One field or directive per line.
   - Consistent indentation.
   - Optional semicolon normalization.
   - Canonical modifier ordering, for example `pk`, `required`, `unique`,
     `hidden`, `search`, `default`, then relationship arrows.

4. **Parser and semantic model API**
   - Shared library used by the CLI, IDE, linter, generator, language server,
     natural-language planner, and tests.
   - Produces AST, normalized schema, dependency graph, diagnostics, and symbol
     table.
   - Resolves table fields, calculated fields, lookup paths, handler targets,
     PBC contracts, workflow states, permissions, deployment units, and package
     outputs.
   - Prevents tool drift by making every surface consume the same semantic
     model.

5. **AppGen CLI**
   - `appgen lint`
   - `appgen format`
   - `appgen validate`
   - `appgen generate`
   - `appgen graph`
   - `appgen explain`
   - `appgen doctor`
   - `appgen package`
   - `appgen pbc publish`
   - `appgen pbc verify`

6. **IDE integration**
   - VS Code extension first.
   - Monaco language package for the AppGen-X IDE.
   - Syntax highlighting.
   - Component palette integration.
   - Form designer synchronized with DSL.
   - Database designer synchronized with DSL.
   - Workflow designer synchronized with DSL.
   - PBC composition designer synchronized with DSL.

7. **Graph tooling**
   - Entity relationship graph.
   - PBC dependency graph.
   - Workflow state graph.
   - Handler call graph.
   - Agent/tool permission graph.
   - Deployment topology graph.
   - Package output graph.

8. **Test generator**
   - Schema tests.
   - View binding tests.
   - Handler target tests.
   - Workflow transition tests.
   - PBC contract tests.
   - Package and deployment smoke tests.
   - Security and permission tests.
   - Agent permission and tool-use tests.

9. **Migration planner**
   - Detect destructive schema changes.
   - Generate migration plans.
   - Explain data movement.
   - Flag unsafe rename-vs-drop/add situations.
   - Support PostgreSQL and MySQL-compatible targets.

10. **Natural-language change planner**
    - Converts prompts into DSL diffs.
    - Shows proposed tables, fields, forms, flows, rules, agents, PBCs,
      packages, deployment units, and tests before generation.
    - Runs the linter before generation.
    - Optimizes for small local models by using compact edit plans and
      constrained DSL patches.

11. **Package and verifier tooling**
    - Web build verifier.
    - Mobile package verifier.
    - Desktop installer verifier.
    - PBC self-registration verifier.
    - Release evidence bundle generator.
    - Deployment readiness verifier.

## Priority Order

1. Shared parser and semantic model.
2. Linter.
3. Formatter.
4. Language server.
5. VS Code and Monaco integration.
6. Graph and explain tooling.
7. Migration planner.
8. Natural-language DSL diff planner.
9. Package and release verifiers.

The shared semantic model is the foundation. Without it, every tool will drift:
the linter, IDE, generator, language server, visual designers, and agents will
eventually disagree about what the language means.
