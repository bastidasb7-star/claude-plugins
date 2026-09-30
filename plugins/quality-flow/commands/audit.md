---
description: Run the quality workflow on any codebase (any language) — review and coverage mapping in parallel, then write the missing tests.
argument-hint: "[path to audit, default: current project]"
---

Run the **quality-flow** workflow on `$ARGUMENTS`. If no path was given, use the current working directory. Every subagent below must be told this path and must work inside it.

## Step 0 — Detect the stack (you, quickly)

Glob the manifests at the path (`package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `composer.json`, `Gemfile`…) and note the language(s), framework and test command. Pass this one-line summary to every subagent. If the path holds several projects (a monorepo), list them and audit each one the user cares about — ask if unclear.

## Step 1 — Review and map coverage (in parallel)

These two jobs are independent and read-only, so start them **at the same time, in a single message with two Agent calls**:

- **code-reviewer** subagent: review the code at the path and return its findings table plus "Behaviours worth a test".
- **coverage-mapper** subagent: map every unit (endpoints, or public functions/classes/commands) and outcome against the existing tests and return the coverage table, the gaps, the run command, the test file(s) to extend and the test style.

Wait until **both** have returned before moving on. If either fails, stop and report which one and why.

## Step 2 — Write the missing tests (depends on Step 1)

Start the **test-writer** subagent only after Step 1 is complete. Pass it, verbatim:

1. the path and the stack summary;
2. the coverage-mapper's "Gaps", run command, "Test file(s) to extend" and "Test style";
3. the code-reviewer's "Behaviours worth a test" and any high/medium findings.

Tell it to remove duplicates between the two lists, add the tests, and run the suite until it is green (marking tests that expose real application bugs as expected-to-fail/skipped with the runner's own mechanism).

## Step 3 — Report

Do this yourself, without another subagent. Combine the three results into one short report:

```
# quality-flow audit — <path> (<language> · <framework>)

## Review findings            (from code-reviewer)
## Coverage before → after    (gaps from coverage-mapper, tests added by test-writer)
## Suite result               (from test-writer, with the command used)
## Bugs to fix next           (reviewer findings confirmed by a failing/xfail test first)
```

Do not modify application code in this workflow — only the test-writer changes files, and only test files.
