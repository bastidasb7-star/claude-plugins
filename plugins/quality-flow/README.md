# quality-flow

A Claude Code plugin that runs a **code-quality workflow on any codebase, in any language**: two read-only subagents review the code and map test coverage in parallel, then a test-writing subagent turns their findings into passing tests using the project's own test runner.

Works with JavaScript/TypeScript, Python, Go, Rust, Java/Kotlin, C#/.NET, PHP and Ruby — web APIs (endpoints and status codes) as well as libraries and CLIs (public functions and their error cases).

Part of the [bryan-plugins](../../README.md) marketplace. First built and tested against an Express API in [bastidasb7-star/claude-multi-agent-workflow](https://github.com/bastidasb7-star/claude-multi-agent-workflow).

## Install

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install quality-flow@bryan-plugins
```

Or load it straight from a clone of this repo, without installing:

```bash
claude --plugin-dir plugins/quality-flow
```

## Usage

```text
/quality-flow:audit                 # audit the current project
/quality-flow:audit services/api    # audit one folder (e.g. one project of a monorepo)
```

## What's inside

| Component | Name (namespaced) | What it does |
|-----------|-------------------|--------------|
| Command | `/quality-flow:audit [path]` | Detects the stack and runs the whole workflow. |
| Subagent | `quality-flow:code-reviewer` | Read-only (`Read, Grep, Glob`, opus). Finds bugs, missing validation, error-handling and security issues in the idiom of each language. |
| Subagent | `quality-flow:coverage-mapper` | Read-only (`Read, Grep, Glob`, haiku). Maps endpoints or public functions and their outcomes against existing tests. |
| Subagent | `quality-flow:test-writer` | Writer (`Read, Grep, Glob, Edit, Write, Bash`, sonnet). Adds the missing tests with the project's runner and runs the suite until green. |
| Skill | `quality-flow:test-conventions` | Language-agnostic testing rules + a per-language reference (runner, file layout, HTTP test client, how to mark known bugs). |
| Hook | `PostToolUse` on `Write\|Edit\|MultiEdit` | Lints each edited file with the linter its language already has (see below) and feeds errors back to Claude. |

## The workflow

```text
/quality-flow:audit [path]

  Step 0  detect stack (language, framework, test command)
  Step 1 (parallel)   code-reviewer ─┐
                      coverage-mapper ┘─► Step 2 (dependent) test-writer ─► Step 3 report
```

1. **Review + coverage map** run at the same time — both only read the code.
2. **Test writer** starts only after both return, using their gaps and findings as its input.
3. The main session merges everything into one report: findings, coverage before/after, suite result, bugs to fix next.

Tests that expose real bugs are kept and marked with the runner's own mechanism (`todo`, `xfail`, `t.Skip`, `#[ignore]`, `@Disabled`, `Skip =`, `pending`…) so the suite stays green and the bug stays visible. Application code is never modified.

## Lint hook — supported languages

The hook uses only tools the project or machine already has; if none is found it does nothing.

| Files | Tools tried, in order |
|-------|-----------------------|
| `.js .jsx .mjs .cjs .ts .tsx .mts .cts .vue` | project-local ESLint (`node_modules`) |
| `.py` | `ruff` (project `.venv` or PATH) → `flake8` → `python -m py_compile` |
| `.go` | `gofmt -e` |
| `.php` | `php -l` |
| `.rb` | `ruby -wc` |
| `.sh .bash` | `shellcheck` → `bash -n` |
| `.json` | built-in JSON parse (skips `tsconfig`, `.vscode`, etc., which allow comments) |

Requires Node.js on the PATH to run the hook script. Compiled languages (Java, C#, Rust, C/C++) are checked by the test-writer's build/test run instead of per edit.

## Layout

```text
.claude-plugin/plugin.json
agents/                # code-reviewer, coverage-mapper, test-writer
commands/audit.md      # the workflow command
skills/test-conventions/
  SKILL.md
  references/languages.md
hooks/hooks.json       # uses ${CLAUDE_PLUGIN_ROOT}/scripts/lint-on-edit.js
scripts/lint-on-edit.js
NOTES.md               # design notes
```

## Versioning

The version lives in `.claude-plugin/plugin.json` (and is mirrored in the marketplace entry). Bump it on every release so installed copies pick up the update with `/plugin marketplace update bryan-plugins`.

See [NOTES.md](NOTES.md) for the design decisions.
