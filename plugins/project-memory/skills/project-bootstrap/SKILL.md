---
name: project-bootstrap
description: Inicializa o actualiza la memoria técnica de un proyecto de software. Usar al comenzar un repositorio nuevo o existente que necesite continuidad entre sesiones, documentación base, arquitectura, estado actual, reglas de negocio, API, base de datos, runbook y handoff.
---

# Project Bootstrap

Objetivo: convertir el repositorio actual en un proyecto fácil de retomar en futuras sesiones —con cualquier asistente de IA compatible (Claude Code, Codex u otro)— sin inventar información ni generar documentación innecesaria.

## Resultado esperado

El repositorio debe quedar con, como mínimo:

- `AGENTS.md`
- `CLAUDE.md`
- `docs/INDEX.md`
- `docs/PROJECT.md`
- `docs/PROJECT_STATE.md`
- `docs/SESSION_HANDOFF.md`
- `docs/ARCHITECTURE.md`
- `docs/RUNBOOK.md`
- `docs/BUSINESS_RULES.md`
- `docs/DECISIONS.md`
- `docs/TODO.md`
- `docs/WORKLOG.md`
- `.agents/skills/project/SKILL.md`
- `.claude/skills/project/SKILL.md`

Crear también cuando aplique:

- `docs/DATABASE.md`
- `docs/API.md`

## Regla principal

El código, los manifiestos, las migraciones, la configuración y los tests reales son la fuente de verdad.

No inventar:
- versiones;
- endpoints;
- tablas;
- relaciones;
- roles;
- comandos;
- servicios;
- estados;
- funcionalidades.

Cuando un hecho no pueda comprobarse, marcarlo como `Por confirmar`.

## Paso 1 — inspeccionar sin ruido

Antes de crear o completar documentos:

1. Identificar la raíz del repositorio.
2. Revisar estructura de directorios.
3. Ignorar carpetas generadas o de dependencias:
   - `.git`
   - `node_modules`
   - `dist`
   - `build`
   - `target`
   - `.gradle`
   - `.venv`
   - `venv`
   - `__pycache__`
   - `.next`
   - `.angular`
   - `coverage`
   - binarios y artefactos grandes.
4. Detectar manifiestos y archivos de configuración relevantes:
   - `package.json`
   - `angular.json`
   - `pom.xml`
   - `build.gradle*`
   - `requirements*.txt`
   - `pyproject.toml`
   - `Pipfile`
   - `Cargo.toml`
   - `go.mod`
   - `*.csproj`
   - `Dockerfile`
   - `docker-compose*.yml`
   - configuraciones de CI
   - migraciones de base de datos.
5. Detectar módulos principales.
6. Detectar tests.
7. Detectar comandos de ejecución, build, lint y pruebas.
8. Detectar API y datos solo cuando sean relevantes.

## Paso 2 — crear estructura base

Si faltan archivos, usar el script incluido en esta skill (`scripts/bootstrap_project.py`):

```bash
# Instalada como plugin de Claude Code (project-memory)
python "${CLAUDE_PLUGIN_ROOT}/skills/project-bootstrap/scripts/bootstrap_project.py" .

# Instalada como skill suelta en Codex (~/.agents/skills)
python ~/.agents/skills/project-bootstrap/scripts/bootstrap_project.py .
```

Si la variable no se resolvió, usar la carpeta base de esta skill (la que se indica al cargarla) + `scripts/bootstrap_project.py`. En Windows, si `python` no existe, probar con `py`.

El script no debe sobrescribir archivos existentes.

Si no es posible ejecutar el script, crear manualmente la misma estructura usando las plantillas que contiene `scripts/bootstrap_project.py`.

## Paso 3 — completar documentación

Completar los archivos recién creados y actualizar con cuidado los existentes.

### `docs/PROJECT.md`

Guardar hechos relativamente estables:

- nombre;
- propósito;
- usuarios/actores;
- módulos;
- stack y versiones confirmadas;
- repositorios o aplicaciones internas si existen;
- dependencias externas importantes.

### `docs/PROJECT_STATE.md`

Debe representar el estado actual, no el historial completo:

- funcionando;
- en desarrollo;
- en pruebas;
- problemas conocidos;
- áreas delicadas;
- siguiente objetivo recomendado;
- fecha de última actualización.

Mantenerlo corto y útil.

### `docs/SESSION_HANDOFF.md`

Debe permitir que una nueva sesión —con el mismo asistente o con otro— continúe rápido:

- objetivo en curso;
- último cambio realizado;
- archivos clave;
- qué se verificó;
- qué falta;
- siguiente paso concreto;
- advertencias relevantes.

Reemplazar el contenido anterior con el handoff actual cuando cambie el punto de continuidad. No acumular sesiones históricas aquí.

### `docs/ARCHITECTURE.md`

Documentar:

- componentes;
- responsabilidades;
- flujo de datos;
- dependencias entre módulos;
- integraciones;
- límites del sistema;
- decisiones estructurales ya comprobadas.

### `docs/RUNBOOK.md`

Documentar solamente comandos confirmados para:

- instalar;
- configurar;
- ejecutar;
- probar;
- lint/formato;
- build;
- migrar;
- desplegar, si está documentado en el repositorio.

No inventar comandos.

### `docs/DATABASE.md`

Solo si hay persistencia/base de datos.

Incluir:

- motor;
- entidades/tablas principales;
- relaciones;
- claves y restricciones relevantes;
- migraciones;
- reglas de integridad;
- riesgos de cascada o borrado.

No copiar secretos de cadenas de conexión.

### `docs/API.md`

Solo si existe API.

Incluir:

- base path si está confirmado;
- endpoints importantes;
- método;
- request/response a nivel útil;
- autenticación/autorización;
- errores relevantes;
- consumidores conocidos.

### `docs/BUSINESS_RULES.md`

Guardar reglas funcionales que sería peligroso perder y que no son evidentes solo mirando un archivo.

Diferenciar:
- regla confirmada por código/tests;
- regla confirmada por el usuario;
- pendiente de confirmar.

### `docs/DECISIONS.md`

Registrar decisiones arquitectónicas o funcionales duraderas.

Cada entrada:
- fecha;
- decisión;
- contexto;
- motivo;
- consecuencias.

No registrar arreglos triviales.

### `docs/TODO.md`

Solo pendientes reales y accionables.

Separar cuando sea útil:
- alta;
- media;
- baja.

Eliminar tareas completadas o mover su resultado a `WORKLOG.md`.

### `docs/WORKLOG.md`

Registrar cambios significativos:

- fecha;
- problema/objetivo;
- causa si se conoce;
- solución;
- archivos o módulos afectados;
- verificación;
- resultado.

No pegar conversaciones completas, logs enormes ni diffs enteros.

## Paso 4 — crear reglas locales adecuadas

Actualizar `AGENTS.md` con información real del repositorio:

- layout;
- comandos reales;
- convenciones;
- restricciones;
- pasos de verificación;
- reglas de documentación.

Mantener `AGENTS.md` conciso. Detalles largos deben vivir en `docs/`.

`CLAUDE.md` debe quedar como un puntero corto a `AGENTS.md` (Claude Code lee `CLAUDE.md`, no `AGENTS.md`, por lo que ambos deben existir). No dupliques el contenido completo en `CLAUDE.md`.

## Paso 5 — comprobar coherencia

Antes de finalizar:

1. comparar documentación contra el código;
2. eliminar afirmaciones no verificadas o marcarlas `Por confirmar`;
3. comprobar que no se registraron secretos;
4. comprobar que los comandos documentados existen;
5. comprobar que `PROJECT_STATE.md` y `SESSION_HANDOFF.md` contienen el estado actual;
6. ejecutar `python scripts/project_docs_check.py` si el script existe.

## Actualización de un proyecto ya inicializado

Si los documentos ya existen:

- no reinicializarlos;
- leer primero estado y handoff;
- inspeccionar el código relevante;
- corregir documentación obsoleta;
- preservar decisiones e historial válidos;
- actualizar solamente lo necesario.

## Final

Informar de forma compacta:

- stack detectado;
- documentación creada;
- documentación actualizada;
- elementos `Por confirmar`;
- próximo punto recomendado para continuar.
