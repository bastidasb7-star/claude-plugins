# project-memory

Plugin de Claude Code que crea y mantiene la **memoria técnica** de un proyecto **en cualquier lenguaje o stack** (JS/TS, Python, Go, Rust, Java/Kotlin, .NET, PHP, Ruby, Elixir, Flutter, Swift, C/C++, monorepos…), para que cualquier sesión (de Claude Code, Codex u otro asistente compatible con `AGENTS.md`) pueda retomarlo sin perder contexto.

## Instalar

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install project-memory@bryan-plugins
```

## Uso

En la raíz del repositorio:

```text
/project-memory:project-bootstrap
```

Claude también la usa por su cuenta cuando pides algo como “inicializa la documentación del proyecto” o “prepara este repo para retomarlo en otra sesión”.

## Qué hace

1. Detecta el stack y analiza el repo (manifiestos, config, rutas, migraciones, tests, comandos de CI) sin inventar nada: el código es la fuente de verdad. [`references/stacks.md`](skills/project-bootstrap/references/stacks.md) le dice dónde mirar en cada ecosistema.
2. Copia desde `templates/` la estructura base que falte, sin sobrescribir archivos existentes (con Python si está disponible; si no, con `cp -Rn` o creando los archivos directamente). Al proyecto solo se añade Markdown:
   - `AGENTS.md` y `CLAUDE.md`
   - `docs/`: `INDEX`, `PROJECT`, `PROJECT_STATE`, `SESSION_HANDOFF`, `ARCHITECTURE`, `RUNBOOK`, `BUSINESS_RULES`, `DECISIONS`, `TODO`, `WORKLOG` (y `API`/`DATABASE` si aplican)
   - la skill local `project` en `.claude/skills/` y `.agents/skills/`
3. Completa esos documentos con lo que encontró en el código.

## Contenido

| Componente | Nombre | Descripción |
|------------|--------|-------------|
| Skill | `project-memory:project-bootstrap` | Instrucciones del proceso de bootstrap |
| Plantillas | `skills/project-bootstrap/templates/` | Los archivos que se copian al proyecto |
| Script (opcional) | `skills/project-bootstrap/scripts/bootstrap_project.py` | Copia las plantillas que falten y, con `--check`, informa de lo que falta o sigue `Por completar`. Python 3 opcional |
| Referencia | `skills/project-bootstrap/references/stacks.md` | Dónde encontrar comandos, migraciones y rutas en cada stack |
| Referencia | `skills/project-bootstrap/references/project-documentation-standard.md` | Estándar de documentación que siguen los archivos generados |
