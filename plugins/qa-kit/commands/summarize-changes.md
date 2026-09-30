---
description: Summarise what changed on the current branch, ready to paste into a PR description.
argument-hint: "[base branch, default: the repo's default branch]"
---

Summarise the changes on the current branch. This works for any language or project type — it only uses git.

1. Pick the base branch: `$ARGUMENTS` if given; otherwise the remote default branch (`git symbolic-ref refs/remotes/origin/HEAD`), falling back to `main` or `master`.
2. Collect the changes with `git diff --stat <base>...HEAD` and `git log --oneline <base>..HEAD`. Include uncommitted changes (`git status --short`) and mark them as such.
3. Read the diffs you need to understand each change. Don't guess from file names.

Return Markdown that can be pasted straight into a pull request:

```
## Summary
<1–2 sentences on what this branch does and why>

## Changes
- `path/to/file` — <one-line description of what changed>

## Notes
- <breaking changes, migrations, new dependencies, config/env changes, or "None">
```

Group files by area (for example `src/`, `tests/`, `docs/`, config) when there are more than about 10. Keep it short.
