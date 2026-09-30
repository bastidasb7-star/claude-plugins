# project-memory

Plugin de Claude Code que crea y mantiene la **memoria técnica** de un proyecto, para que cualquier sesión (de Claude Code, Codex u otro asistente compatible con `AGENTS.md`) pueda retomarlo sin perder contexto.

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

1. Analiza el repo (manifiestos, config, rutas, migraciones, tests, comandos) sin inventar nada: el código es la fuente de verdad.
2. Crea con `scripts/bootstrap_project.py` la estructura base que falte, sin sobrescribir archivos existentes:
   - `AGENTS.md` y `CLAUDE.md`
   - `docs/`: `INDEX`, `PROJECT`, `PROJECT_STATE`, `SESSION_HANDOFF`, `ARCHITECTURE`, `RUNBOOK`, `BUSINESS_RULES`, `DECISIONS`, `TODO`, `WORKLOG` (y `API`/`DATABASE` si aplican)
   - la skill local `project` en `.claude/skills/` y `.agents/skills/`
3. Completa esos documentos con lo que encontró en el código.

## Contenido

| Componente | Nombre | Descripción |
|------------|--------|-------------|
| Skill | `project-memory:project-bootstrap` | Instrucciones del proceso de bootstrap |
| Script | `skills/project-bootstrap/scripts/bootstrap_project.py` | Genera la estructura base (requiere Python 3) |
| Referencia | `skills/project-bootstrap/references/project-documentation-standard.md` | Estándar de documentación que siguen los archivos generados |
