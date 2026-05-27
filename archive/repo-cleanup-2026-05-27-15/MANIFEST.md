# Repo Cleanup Archive - 2026-05-27

This archive captures files moved out of the active repository tree during a
conservative unused-file cleanup pass.

## Moved tracked files

- `lang/FEEL_1_1.g4` -> `lang-unused/FEEL_1_1.g4`
- `lang/RuleSet.g4` -> `lang-unused/RuleSet.g4`
- `lang/apg.g4` -> `lang-unused/apg.g4`
- `lang/cel.g4` -> `lang-unused/cel.g4`
- `lang/spec.g4` -> `lang-unused/spec.g4`
- `lang/test.ags` -> `lang-unused/test.ags`
- `lang/types.txt` -> `lang-unused/types.txt`

Reason: repo references and DSL quality checks use `lang/appgen.g4` as the
canonical grammar. These additional grammar/sample files had no references
outside their own declarations.

## Moved ignored runtime artifacts

- `.pytest_cache`
- `tests/__pycache__`
- `src/pyAppGen/**/__pycache__`
- post-verification `src/pyAppGen/__pycache__` and `tests/__pycache__`
- post-focused-test `.pytest_cache`, `tests/__pycache__`, and
  `src/pyAppGen/**/__pycache__`
- final post-test `src/pyAppGen/pbcs/**/__pycache__` sweep

Reason: regenerated runtime caches are not source artifacts and should not
remain in the active tree after verification.
