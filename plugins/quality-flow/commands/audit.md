---
description: Ejecuta el flujo de calidad sobre cualquier código (cualquier lenguaje): revisión y mapa de cobertura en paralelo, y después escribe los tests que faltan.
argument-hint: "[ruta a auditar, por defecto: el proyecto actual]"
---

Ejecuta el flujo **quality-flow** sobre `$ARGUMENTS`. Si no se indicó ruta, usa el directorio de trabajo actual. A cada subagente de abajo hay que darle esta ruta y debe trabajar dentro de ella.

## Paso 0 — Detectar el stack (tú, rápido)

Busca los manifiestos en la ruta (`package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `composer.json`, `Gemfile`…) y anota lenguaje(s), framework y comando de tests. Pasa este resumen de una línea a cada subagente. Si la ruta contiene varios proyectos (un monorepo), lístalos y audita los que le interesan al usuario; pregunta si no está claro.

## Paso 1 — Revisión y mapa de cobertura (en paralelo)

Estos dos trabajos son independientes y de solo lectura, así que lánzalos **a la vez, en un único mensaje con dos llamadas a Agent**:

- Subagente **code-reviewer**: revisa el código de la ruta y devuelve su tabla de hallazgos y la sección "Comportamientos que merecen un test".
- Subagente **coverage-mapper**: cruza cada unidad (endpoints, o funciones/clases/comandos públicos) y sus resultados con los tests existentes y devuelve la tabla de cobertura, los huecos, el comando para ejecutar, los archivos de test a ampliar y el estilo de los tests.

Espera a que **ambos** hayan terminado antes de seguir. Si alguno falla, detente e informa cuál y por qué.

## Paso 2 — Escribir los tests que faltan (depende del Paso 1)

Lanza el subagente **test-writer** solo cuando el Paso 1 haya terminado. Pásale, tal cual:

1. la ruta y el resumen del stack;
2. del coverage-mapper: "Huecos", comando para ejecutar, "Archivo(s) de test a ampliar" y "Estilo de los tests";
3. del code-reviewer: "Comportamientos que merecen un test" y los hallazgos de severidad alta/media.

Indícale que elimine duplicados entre ambas listas, añada los tests y ejecute la suite hasta que pase (marcando como fallo esperado/omitido, con el mecanismo del propio runner, los tests que revelen bugs reales de la aplicación).

## Paso 3 — Informe

Hazlo tú, sin otro subagente. Combina los tres resultados en un informe breve:

```
# Auditoría quality-flow — <ruta> (<lenguaje> · <framework>)

## Hallazgos de la revisión        (del code-reviewer)
## Cobertura antes → después       (huecos del coverage-mapper, tests añadidos por el test-writer)
## Resultado de la suite           (del test-writer, con el comando usado)
## Bugs a corregir después         (hallazgos confirmados primero por un test fallido/xfail)
```

En este flujo no se modifica el código de la aplicación: solo el test-writer cambia archivos, y solo archivos de test.
