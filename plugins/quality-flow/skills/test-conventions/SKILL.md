---
name: test-conventions
description: Convenciones para escribir tests unitarios y de HTTP/API en cualquier lenguaje: JavaScript/TypeScript, Python, Go, Rust, Java/Kotlin, C#, PHP y Ruby. Usar al añadir o arreglar tests, cubrir casos de error, elegir un runner para un proyecto sin tests, o cuando alguien pregunta "¿cómo debería testear esto?".
---

# Convenciones de tests (cualquier lenguaje)

Aplicar siempre que se escriban o cambien tests. Los tests que ya tiene el proyecto mandan sobre estos valores por defecto: copiar primero su estilo.

## 1. Detectar antes de escribir

1. Encontrar el manifiesto (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `composer.json`, `Gemfile`).
2. Encontrar el runner que ya se usa (dependencias de desarrollo, archivos de config como `jest.config.*`, `vitest.config.*`, `pytest.ini`, `phpunit.xml`, `.rspec`) y el script de tests (`"test"` en `package.json`, `Makefile`, workflow de CI).
3. Abrir uno o dos tests existentes y copiar: imports, fixtures/helpers, setup/teardown, nombres y ubicación de archivos.
4. Solo si no hay tests: usar el runner por defecto del stack según [references/languages.md](references/languages.md).

## 2. Reglas que valen en todos los lenguajes

- **Un comportamiento por test**, con un nombre que lo describa: `creates a user`, `returns 404 when the user is missing`, `test_parse_raises_on_empty_input`, `TestParse_EmptyInput` (usar el idioma que ya usen los tests del proyecto).
- **Preparar → Actuar → Comprobar** (Arrange → Act → Assert). Comprobar primero lo más importante (código de estado / valor devuelto / tipo de error) y después los detalles.
- **Aislados y repetibles:** reiniciar el estado entre tests (fixtures, `beforeEach`, `t.Cleanup`, transacciones con rollback). Ningún test depende del orden de otro.
- **Sin red, reloj ni aleatoriedad reales**, salvo que el proyecto ya lo haga en sus tests; inyectarlos o simularlos.
- **Cubrir por unidad:** el camino feliz, cada rama de validación/error y el caso de "no encontrado" / vacío.
- **APIs HTTP:** testear con el cliente en proceso del framework (supertest, `TestClient` de FastAPI, cliente de tests de Django, `httptest`, `MockMvc`/`WebTestClient`, `WebApplicationFactory`, tests HTTP de Laravel, `rack-test`); nunca levantar un servidor real en un puerto.
- **Formato de errores:** si el proyecto documenta uno (p. ej. `{ "error": "message" }`), comprobarlo.

## 3. Cuando un test revela un bug real

No cambiar el código de la aplicación mientras se escriben tests. Mantener el test y marcarlo con el mecanismo de fallo esperado/omitido del runner y un motivo `bug:`, para que la suite siga en verde y el bug siga visible. La sintaxis exacta de cada lenguaje está en [references/languages.md](references/languages.md).

## 4. Ejecutar

Usar el comando propio del proyecto (`npm test`, `pytest`, `go test ./...`, `cargo test`, `mvn test` / `gradle test`, `dotnet test`, `vendor/bin/phpunit`, `bundle exec rspec`). Ejecutar primero los tests afectados y después la suite completa una vez. En Windows, si un script falla por caracteres especiales en la ruta, llamar a la herramienta directamente (p. ej. `node --test`, `python -m pytest`).
