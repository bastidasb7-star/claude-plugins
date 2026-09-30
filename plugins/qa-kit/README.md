# qa-kit

Plugin pequeño de Claude Code con dos ayudas de calidad que funcionan en cualquier lenguaje: un comando que resume los cambios de tu rama y un subagente que revisa el código reciente.

Forma parte del marketplace [bryan-plugins](../../README.md).

## Instalar

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install qa-kit@bryan-plugins
```

Desde la terminal (por ejemplo, si usas la extensión de VS Code, donde `/plugin` no está disponible):

```bash
claude plugin marketplace add bastidasb7-star/claude-plugins
claude plugin install qa-kit@bryan-plugins
```

## Qué añade

| Componente | Tipo | Qué hace |
|------------|------|----------|
| `/qa-kit:summarize-changes [rama-base]` | Comando | Compara la rama con su base (por defecto, la rama principal del repo) usando solo git y devuelve un resumen listo para el PR: qué hace la rama, una línea por archivo y notas sobre cambios incompatibles, migraciones o dependencias nuevas. |
| `qa-kit:code-reviewer` | Subagente | Revisa los cambios recientes en cualquier lenguaje buscando bugs, errores sin manejar, nombres poco claros y problemas de seguridad evidentes, con el estilo de cada lenguaje. Devuelve los hallazgos agrupados por severidad (alta, media, baja), cada uno con archivo y arreglo. Solo usa herramientas de lectura (`Read, Grep, Glob`). |

## Uso

Dentro de Claude Code:

- Ejecuta `/qa-kit:summarize-changes` para obtener el resumen de la rama.
- Pide algo como "revisa mis cambios recientes" y Claude delegará en el subagente `code-reviewer`. También puedes nombrarlo directamente: "usa el agente code-reviewer".

Para probarlo sin instalarlo, desde la raíz de este repo:

```bash
claude --plugin-dir plugins/qa-kit
```

Después de editar cualquier archivo del plugin, ejecuta `/reload-plugins` para cargar los cambios.

## Estructura

```text
plugins/qa-kit/
├── .claude-plugin/
│   └── plugin.json            # manifiesto: name + version
├── commands/
│   └── summarize-changes.md
├── agents/
│   └── code-reviewer.md
└── README.md
```

Dentro de `.claude-plugin/` solo va `plugin.json`. Las carpetas de componentes están en la raíz del plugin.

## Validación

```bash
claude plugin validate plugins/qa-kit
```
