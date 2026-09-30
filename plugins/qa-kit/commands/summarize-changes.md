---
description: Resume lo que cambió en la rama actual, listo para pegar en la descripción de un PR.
argument-hint: "[rama base, por defecto: la rama principal del repo]"
---

Resume los cambios de la rama actual. Funciona con cualquier lenguaje o tipo de proyecto: solo usa git.

1. Elegir la rama base: `$ARGUMENTS` si se indicó; si no, la rama por defecto del remoto (`git symbolic-ref refs/remotes/origin/HEAD`), y si no existe, `main` o `master`.
2. Reunir los cambios con `git diff --stat <base>...HEAD` y `git log --oneline <base>..HEAD`. Incluir también los cambios sin commit (`git status --short`) y marcarlos como tales.
3. Leer los diffs necesarios para entender cada cambio. No adivinar por el nombre del archivo.

Devolver Markdown que se pueda pegar directamente en un pull request, en el idioma de la conversación:

```
## Resumen
<1–2 frases sobre qué hace esta rama y por qué>

## Cambios
- `ruta/al/archivo` — <descripción en una línea de lo que cambió>

## Notas
- <cambios incompatibles, migraciones, dependencias nuevas, cambios de config/variables de entorno, o "Ninguna">
```

Si hay más de unos 10 archivos, agruparlos por área (por ejemplo `src/`, `tests/`, `docs/`, configuración). Mantenerlo breve.
