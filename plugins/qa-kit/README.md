# qa-kit

A small Claude Code plugin with two quality helpers: a command that summarises the changes on your branch, and a subagent that reviews recent code.

## What it adds

| Component | Type | What it does |
|---|---|---|
| `/qa-kit:summarize-changes` | Slash command | Lists each file touched on the current branch with a one-line description of the change. The output is short enough to paste into a pull-request description. |
| `code-reviewer` | Subagent | Reviews recent changes for bugs, missing error handling and unclear names. Returns findings grouped by severity (high, medium, low), each naming the file and the fix. Uses read-only tools (Read, Grep, Glob). |

## Structure

```
.
├── .claude-plugin/
│   └── plugin.json            # manifest: name + version
├── commands/
│   └── summarize-changes.md
├── agents/
│   └── code-reviewer.md
└── README.md
```

Only `plugin.json` lives inside `.claude-plugin/`. The component folders sit at the repo root.

## Usage

Load the plugin locally from the repo root:

```bash
claude --plugin-dir .
```

Then, inside Claude Code:

- Run `/qa-kit:summarize-changes` to get a summary of the branch.
- Ask something like "review my recent changes" and Claude will delegate to the `code-reviewer` subagent. You can also name it directly: "use the code-reviewer agent".
- After editing any plugin file, run `/reload-plugins` to pick up the changes.

## Validation

The **Validate plugin** GitHub Action runs on every push. It checks that the manifest exists, is valid JSON and has a name, that component folders are at the root, and that at least one component is present. Run it locally with:

```bash
node .github/scripts/validate-plugin.js
```
