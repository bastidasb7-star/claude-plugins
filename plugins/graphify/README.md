# graphify

Empaquetado como plugin de Claude Code de la skill de [Graphify](https://github.com/Graphify-Labs/graphify) (Apache-2.0, © Safi Shamsi y los contribuidores de Graphify; ver [LICENSE](LICENSE) y [NOTICE](NOTICE)). El contenido de la skill es el original, sin modificar.

Convierte una carpeta (código, docs, PDFs, imágenes, vídeo) en un **grafo de conocimiento** que se consulta en lugar de hacer grep: `graphify-out/graph.html` interactivo, `graph.json` y `GRAPH_REPORT.md`.

## Requisito: la CLI de Python

La skill solo orquesta; el trabajo lo hace la CLI `graphify` (paquete PyPI `graphifyy`, con doble y). Instalarla una vez:

```bash
uv tool install graphifyy     # o: pipx install graphifyy
```

No hace falta ejecutar `graphify install`: este plugin ya registra la skill en Claude Code.

## Instalar

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install graphify@bryan-plugins
```

## Uso

```text
/graphify:graphify .                      # grafo del directorio actual
/graphify:graphify <ruta> --update        # re-extrae solo lo cambiado
/graphify:graphify query "¿cómo fluye la autenticación?"
```

Claude también la usa por su cuenta ante preguntas de arquitectura cuando existe `graphify-out/`.

## Actualizar desde upstream

Origen: `Graphify-Labs/graphify` — `graphify/skill.md` → `skills/graphify/SKILL.md` y `graphify/skills/claude/references/` → `skills/graphify/references/`. Versión empaquetada: **0.9.87** (commit `7536dc0`). Al actualizar, copiar de nuevo esos archivos, subir `version` aquí y en el marketplace, y mantener la versión de la CLI alineada.
