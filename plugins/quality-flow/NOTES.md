# NOTAS — quality-flow

## Qué hace el plugin

`quality-flow` empaqueta un flujo de calidad de código que funciona sobre cualquier proyecto y lenguaje (JS/TS, Python, Go, Rust, Java/Kotlin, C#, PHP, Ruby). Un comando, `/quality-flow:audit [ruta]`, ejecuta tres subagentes:

- **code-reviewer**: detecta el stack, lee puntos de entrada, handlers y la capa de datos, e informa de bugs, validaciones que faltan y convenciones que no se cumplen;
- **coverage-mapper**: cruza cada endpoint + código de estado (aplicaciones web) o función pública + resultado (librerías/CLIs) con los tests existentes y lista los huecos;
- **test-writer**: escribe los tests que faltan con el estilo del proyecto y ejecuta la suite hasta que pasa, marcando los tests que revelan bugs reales con el mecanismo de fallo esperado/omitido del propio runner.

Además incluye la skill `test-conventions` (reglas generales de testing más una referencia por lenguaje: runner, ubicación de archivos, cliente HTTP en proceso, cómo marcar bugs conocidos) y un hook `PostToolUse` que pasa a cada archivo que Claude escribe o edita el linter que su lenguaje ya tiene instalado.

## Cómo instalarlo

Desde cualquier sesión de Claude Code:

```text
/plugin marketplace add bastidasb7-star/claude-plugins
/plugin install quality-flow@bryan-plugins
```

Después, abre el proyecto que quieres revisar y ejecuta `/quality-flow:audit [ruta]` (por defecto, el proyecto actual).

Para desarrollo local, desde la raíz del repo: `claude --plugin-dir plugins/quality-flow`, y `/reload-plugins` después de cada cambio.

## Decisión de alcance: por qué cada subagente tiene sus herramientas y su modelo

- **code-reviewer: `Read, Grep, Glob` + `opus`.** Revisar es el razonamiento más difícil del flujo: detectar un id que se convierte en `NaN`, un array mutable expuesto o una rama de `400` que falta exige entender la intención, no solo buscar texto. Por eso recibe el modelo más potente. Tiene *solo* herramientas de lectura y búsqueda porque un revisor que puede editar tiende a "arreglar" cosas en silencio; al ser de solo lectura, su salida es un informe fiable y puede ejecutarse en paralelo sin riesgo de escrituras en conflicto.
- **coverage-mapper: `Read, Grep, Glob` + `haiku`.** Su trabajo es mecánico: listar unidades, listar tests y cruzarlos. Un modelo pequeño y rápido basta y abarata el paso en paralelo. Sin Bash: solo lee handlers y archivos de test.
- **test-writer: `Read, Grep, Glob, Edit, Write, Bash` + `sonnet`.** Es el único agente que cambia archivos, así que es el único con `Edit`/`Write`, y necesita `Bash` para ejecutar el comando de tests del proyecto (`npm test`, `pytest`, `go test ./...`, `cargo test`, `dotnet test`…) e iterar. Escribir tests siguiendo un estilo existente es un trabajo bien definido, así que `sonnet` equilibra calidad y coste. Su prompt además lo limita a archivos de test: los arreglos de la aplicación siguen siendo decisión de una persona.

## Decisión de orquestación: paralelo vs. secuencial

- **En paralelo: code-reviewer + coverage-mapper.** Ninguno necesita la salida del otro y ninguno escribe nada, así que ejecutarlos juntos es seguro y reduce aproximadamente a la mitad el tiempo del primer paso. Miran el mismo código desde dos ángulos ("¿qué está mal?" vs. "¿qué no está testeado?").
- **En secuencia: el test-writer espera a los dos.** Su entrada *es* la salida de ellos: los huecos le dicen qué cubrir y la revisión le dice qué comportamientos probablemente fallan y merecen un test. Empezar antes supondría adivinar, duplicar tests existentes o no cubrir los bugs que encontró el revisor. Además es el único paso que escribe archivos, así que ejecutarlo solo evita ediciones mientras otros agentes todavía están leyendo.
- **Informe en la sesión principal.** Unir tres informes cortos no necesita un contexto nuevo, así que lo hace el orquestador en lugar de un cuarto agente.

## Diseño independiente del lenguaje (v0.2)

- **Detectar, no suponer.** La v0.1 estaba atada a Express + `node:test`. Ahora cada agente empieza leyendo los manifiestos para detectar lenguaje, framework y runner, y el test-writer debe reutilizar el runner que ya tiene el proyecto; solo elige uno por defecto cuando no hay ningún test.
- **Una skill, referencia por lenguaje.** `SKILL.md` contiene las reglas que valen en todas partes; los detalles de cada lenguaje están en `references/languages.md`, que Claude solo lee cuando lo necesita (carga progresiva para mantener pequeño el contexto).
- **El hook usa lo que ya está instalado.** El plugin no incluye linters. `lint-on-edit.js` asocia la extensión del archivo a una cadena de herramientas (p. ej. ruff → flake8 → py_compile) y usa la primera disponible, buscando primero en el proyecto (`node_modules`, `.venv`). Los lenguajes desconocidos o las herramientas que faltan terminan con código 0 en silencio, así que el hook nunca bloquea el trabajo. Si no hay Node.js, el hook tampoco hace nada.
- **Ejecución portable.** Las herramientas se lanzan con `spawnSync` sin shell, así que las rutas con espacios o `&` funcionan en Windows. Los archivos se guardan con saltos de línea LF (`.gitattributes`) para que el frontmatter se lea igual en cualquier sistema.
