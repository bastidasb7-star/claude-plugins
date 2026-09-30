---
name: test-conventions
description: Conventions for writing unit and HTTP/API tests in any language — JavaScript/TypeScript, Python, Go, Rust, Java/Kotlin, C#, PHP and Ruby. Use when adding or fixing tests, covering error paths, choosing a test runner for a project without tests, or when asked "how should I test this?".
---

# Test conventions (any language)

Apply these whenever you write or change tests. The project's existing tests always win over these defaults — copy their style first.

## 1. Detect before writing

1. Find the manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `composer.json`, `Gemfile`).
2. Find the runner already in use (dev dependencies, config files like `jest.config.*`, `vitest.config.*`, `pytest.ini`, `phpunit.xml`, `.rspec`) and the test script (`"test"` in `package.json`, `Makefile`, CI workflow).
3. Open one or two existing tests and copy: imports, fixtures/helpers, setup/teardown, naming, file placement.
4. Only if there are no tests: use the default runner for the stack from [references/languages.md](references/languages.md).

## 2. Rules that apply everywhere

- **One behaviour per test**, named after the behaviour: `creates a user`, `returns 404 when the user is missing`, `test_parse_raises_on_empty_input`, `TestParse_EmptyInput`.
- **Arrange → Act → Assert.** Assert the most important thing first (status code / return value / error type), then details.
- **Isolated and repeatable:** reset state between tests (fixtures, `beforeEach`, `t.Cleanup`, transactions rolled back). No test depends on another's order.
- **No real network, clock or randomness** unless the project already does that in tests; inject or fake them.
- **Cover per unit:** the happy path, each validation/error branch, and the not-found / empty case.
- **HTTP APIs:** test through the framework's in-process client (supertest, FastAPI `TestClient`, Django test client, `httptest`, `MockMvc`/`WebTestClient`, `WebApplicationFactory`, Laravel HTTP tests, `rack-test`) — never start a real server on a port.
- **Error shape:** if the project documents one (e.g. `{ "error": "message" }`), assert it.

## 3. When a test exposes a real bug

Don't change application code while writing tests. Keep the test, mark it with the runner's expected-failure/skip mechanism and a `bug:` reason, so the suite stays green and the bug stays visible. The exact syntax per language is in [references/languages.md](references/languages.md).

## 4. Running

Use the project's own command (`npm test`, `pytest`, `go test ./...`, `cargo test`, `mvn test` / `gradle test`, `dotnet test`, `vendor/bin/phpunit`, `bundle exec rspec`). Run the affected tests first, then the full suite once. On Windows, if a script shim fails because of special characters in the path, call the tool directly (e.g. `node --test`, `python -m pytest`).
