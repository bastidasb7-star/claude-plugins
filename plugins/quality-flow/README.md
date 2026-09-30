# quality-flow

Plugin de Claude Code que ejecuta un **flujo de calidad de código sobre cualquier proyecto, en cualquier lenguaje**: dos subagentes de solo lectura revisan el código y mapean la cobertura de tests en paralelo, y después un subagente escritor convierte sus hallazgos en tests que pasan, usando el runner de tests del propio proyecto.

Funciona con JavaScript/TypeScript, Python, Go, Rust, Java/Kotlin, C#/.NET, PHP y Ruby: APIs web (endpoints y códigos de estado) y también librerías y CLIs (funciones públicas y sus casos de error).

Forma parte del marketplace [bryan-plugins](../../README.md). Se creó y probó primero sobre una API Express en [bastidasb7-star/claude-multi-agent-workflow](https://github.com/bastidasb7-star/claude-multi-agent-workflow).

## Instalar

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install quality-flow@bryan-plugins
```

Desde la terminal (por ejemplo, si usas la extensión de VS Code, donde `/plugin` no está disponible):

```bash
claude plugin marketplace add bastidasb7-star/claude-plugins
claude plugin install quality-flow@bryan-plugins
```

O cargarlo directamente desde un clon de este repo, sin instalarlo:

```bash
claude --plugin-dir plugins/quality-flow
```

## Uso

```text
/quality-flow:audit                 # audita el proyecto actual
/quality-flow:audit services/api    # audita una carpeta (p. ej. un proyecto de un monorepo)
```

## Contenido

| Componente | Nombre (con namespace) | Qué hace |
|------------|------------------------|----------|
| Comando | `/quality-flow:audit [ruta]` | Detecta el stack y ejecuta el flujo completo. |
| Subagente | `quality-flow:code-reviewer` | Solo lectura (`Read, Grep, Glob`, opus). Encuentra bugs, validaciones que faltan y problemas de manejo de errores y seguridad, con el estilo de cada lenguaje. |
| Subagente | `quality-flow:coverage-mapper` | Solo lectura (`Read, Grep, Glob`, haiku). Cruza endpoints o funciones públicas y sus resultados con los tests existentes. |
| Subagente | `quality-flow:test-writer` | Escritor (`Read, Grep, Glob, Edit, Write, Bash`, sonnet). Añade los tests que faltan con el runner del proyecto y ejecuta la suite hasta que pasa. |
| Skill | `quality-flow:test-conventions` | Reglas de testing válidas para cualquier lenguaje + una referencia por lenguaje (runner, ubicación de archivos, cliente HTTP de tests, cómo marcar bugs conocidos). |
| Hook | `PostToolUse` en `Write\|Edit\|MultiEdit` | Pasa el linter de su lenguaje a cada archivo editado (ver abajo) y le devuelve los errores a Claude. |

## El flujo

```text
/quality-flow:audit [ruta]

  Paso 0  detectar stack (lenguaje, framework, comando de tests)
  Paso 1 (paralelo)    code-reviewer ─┐
                       coverage-mapper ┘─► Paso 2 (dependiente) test-writer ─► Paso 3 informe
```

1. **Revisión + mapa de cobertura** se ejecutan a la vez: los dos solo leen el código.
2. **El test-writer** empieza solo cuando ambos terminan, usando sus huecos y hallazgos como entrada.
3. La sesión principal une todo en un informe: hallazgos, cobertura antes/después, resultado de la suite y bugs a corregir.

Los tests que revelan bugs reales se mantienen y se marcan con el mecanismo del propio runner (`todo`, `xfail`, `t.Skip`, `#[ignore]`, `@Disabled`, `Skip =`, `pending`…), para que la suite siga en verde y el bug siga visible. El código de la aplicación nunca se modifica.

## Hook de lint — lenguajes soportados

El hook solo usa herramientas que el proyecto o el equipo ya tienen; si no encuentra ninguna, no hace nada.

| Archivos | Herramientas que prueba, en orden |
|----------|-----------------------------------|
| `.js .jsx .mjs .cjs .ts .tsx .mts .cts .vue` | ESLint local del proyecto (`node_modules`) |
| `.py` | `ruff` (`.venv` del proyecto o PATH) → `flake8` → `python -m py_compile` |
| `.go` | `gofmt -e` |
| `.php` | `php -l` |
| `.rb` | `ruby -wc` |
| `.sh .bash` | `shellcheck` → `bash -n` |
| `.json` | parseo JSON interno (omite `tsconfig`, `.vscode`, etc., que admiten comentarios) |

El script del hook se ejecuta con Node.js si está en el PATH; sin Node, el hook se omite en silencio. Los lenguajes compilados (Java, C#, Rust, C/C++) se comprueban con el build/tests que ejecuta el test-writer, no en cada edición.

## Estructura

```text
.claude-plugin/plugin.json
agents/                # code-reviewer, coverage-mapper, test-writer
commands/audit.md      # el comando del flujo
skills/test-conventions/
  SKILL.md
  references/languages.md
hooks/hooks.json       # usa ${CLAUDE_PLUGIN_ROOT}/scripts/lint-on-edit.js
scripts/lint-on-edit.js
NOTES.md               # decisiones de diseño
```

## Versiones

La versión está en `.claude-plugin/plugin.json` (y se repite en la entrada del marketplace). Hay que subirla en cada publicación para que las copias instaladas reciban la actualización con `/plugin marketplace update bryan-plugins`.

Ver [NOTES.md](NOTES.md) para las decisiones de diseño.
