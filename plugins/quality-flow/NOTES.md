# NOTES — quality-flow

## What the plugin does

`quality-flow` packages a code-quality workflow that works on any codebase and language (JS/TS, Python, Go, Rust, Java/Kotlin, C#, PHP, Ruby). One command, `/quality-flow:audit [path]`, runs three subagents:

- **code-reviewer** — detects the stack, reads entry points, handlers and the data layer, and reports bugs, missing validation and convention breaks;
- **coverage-mapper** — matches every endpoint + status code (web apps) or public function + outcome (libraries/CLIs) against the existing tests and lists the gaps;
- **test-writer** — writes the missing tests in the project's style and runs the suite until it is green, marking tests that expose real bugs with the runner's own expected-failure/skip mechanism.

It also ships the `test-conventions` skill (general testing rules plus a per-language reference: runner, file layout, in-process HTTP client, how to mark known bugs) and a `PostToolUse` hook that lints every file Claude writes or edits with the linter its language already has installed.

## How to install

From any Claude Code session:

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install quality-flow@bryan-plugins
```

Then open the project you want to check and run `/quality-flow:audit [path]` (default: the current project).

For local development, from the repo root: `claude --plugin-dir plugins/quality-flow`, and use `/reload-plugins` after editing.

## Scoping decision — why each subagent got its tools and model

- **code-reviewer: `Read, Grep, Glob` + `opus`.** Reviewing is the hardest reasoning in the flow — spotting a `NaN` id, a leaked mutable array or a missing `400` branch means understanding intent, not just matching text — so it gets the strongest model. It gets *only* read-and-search tools because a reviewer that can edit tends to "fix" things silently; keeping it read-only makes its output a report you can trust and lets it run in parallel with no risk of conflicting writes.
- **coverage-mapper: `Read, Grep, Glob` + `haiku`.** Its job is mechanical: list routes, list tests, match them. A small, fast model is enough and keeps the parallel step cheap. No Bash — it only reads handlers and test files.
- **test-writer: `Read, Grep, Glob, Edit, Write, Bash` + `sonnet`.** It's the only agent that changes files, so it's the only one with `Edit`/`Write`, and it needs `Bash` to run the project's test command (`npm test`, `pytest`, `go test ./...`, `cargo test`, `dotnet test`…) and iterate. Writing tests in an existing style is well-defined work, so `sonnet` balances quality and cost. Its prompt also limits it to test files — application fixes stay a human decision.

## Orchestration decision — parallel vs. sequential

- **Parallel: code-reviewer + coverage-mapper.** Neither needs the other's output and neither writes anything, so running them together is safe and roughly halves the wall-clock time of the first step. They look at the same code from two angles ("what is wrong?" vs. "what is untested?").
- **Sequential: test-writer waits for both.** Its input *is* their output: the gaps tell it what to cover, the review tells it which behaviours are likely broken and deserve a test. Starting it earlier would mean guessing, duplicating existing tests or missing the bugs the reviewer found. It is also the only step that writes files, so running it alone avoids edits happening while other agents are still reading.
- **Report in the main session.** Merging three short reports doesn't need a fresh context, so it's done by the orchestrator instead of a fourth agent.

## Language-agnostic design (v0.2.0)

- **Detect, don't assume.** v0.1 was hard-wired to Express + `node:test`. Now every agent starts by reading the manifests to detect language, framework and runner, and the test-writer must reuse the runner already in the project; it only picks a default when there are no tests at all.
- **One skill, per-language reference.** `SKILL.md` keeps the rules that are true everywhere; the per-language details live in `references/languages.md`, which Claude only reads when needed (progressive disclosure keeps the context small).
- **Hook uses what's installed.** The plugin ships no linters. `lint-on-edit.js` maps the file extension to a chain of tools (e.g. ruff → flake8 → py_compile) and uses the first one available, looking in the project first (`node_modules`, `.venv`). Unknown languages or missing tools exit 0 silently, so the hook never blocks work.
- **Portable execution.** Tools run with `spawnSync` and no shell, so paths with spaces or `&` work on Windows. Files are stored with LF (`.gitattributes`) so frontmatter parses on every OS.
