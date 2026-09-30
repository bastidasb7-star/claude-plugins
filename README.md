# claude-plugins

Marketplace de plugins de Claude Code de Bryan Bastidas.

## Instalar

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install qa-kit@bryan-plugins
/plugin install quality-flow@bryan-plugins
/plugin install project-memory@bryan-plugins
```

Para actualizar después de un cambio: `/plugin marketplace update bryan-plugins`.

## Plugins

| Plugin | Qué incluye | Uso |
|--------|-------------|-----|
| [qa-kit](plugins/qa-kit) | Comando `summarize-changes` + subagente `code-reviewer` (solo lectura) | `/qa-kit:summarize-changes` antes de abrir un PR |
| [quality-flow](plugins/quality-flow) | 3 subagentes (reviewer, coverage-mapper, test-writer), comando `audit`, skill `api-test-conventions`, hook de ESLint | `/quality-flow:audit <ruta-de-la-api>` |
| [project-memory](plugins/project-memory) | Skill `project-bootstrap` + script que genera `AGENTS.md`, `CLAUDE.md` y `docs/` (estado, handoff, arquitectura…) | `/project-memory:project-bootstrap` en la raíz de un repo |

## Estructura

```text
.claude-plugin/marketplace.json   # catálogo: cada plugin apunta a ./plugins/<nombre>
plugins/
  qa-kit/                         # origen: bastidasb7-star/claude-assemble-and-ship
  quality-flow/                   # origen: bastidasb7-star/claude-multi-agent-workflow
  project-memory/                 # origen: skill local ~/.claude/skills/project-bootstrap
```

## Añadir un plugin nuevo

1. Crear `plugins/<nombre>/.claude-plugin/plugin.json` con `name` y `version`, y las carpetas `agents/`, `commands/`, `skills/`, `hooks/` en la raíz del plugin (no dentro de `.claude-plugin/`).
2. Añadir la entrada en `.claude-plugin/marketplace.json` con `"source": "./plugins/<nombre>"`.
3. Validar con `claude plugin validate .` y hacer push.
4. Al cambiar un plugin, subir su `version` en `plugin.json` y en el marketplace.
