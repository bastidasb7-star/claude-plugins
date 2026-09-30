# Referencia de tests por lenguaje

Usar la sección del lenguaje del proyecto. El "runner por defecto" es solo para proyectos que todavía no tienen tests.

## JavaScript / TypeScript

- **Runner por defecto:** `vitest` en proyectos Vite/TS; si no, `node:test` (sin dependencias). Mantener `jest` si ya está.
- **Archivos:** `*.test.ts` / `*.test.js` junto al código o en `tests/`/`__tests__/`.
- **HTTP:** `supertest` contra la app exportada (`request(app).get('/users')`); exportar la app sin llamar a `listen()`.
- **Ejecutar:** `npm test` (o `npx vitest run`, `node --test`).
- **Bug conocido:** `test('…', { todo: 'bug: …' }, fn)` (node:test), `it.todo` / `test.fails` (vitest), `test.failing` (jest).

```js
test('POST /users returns 400 when email is missing', async () => {
  const res = await request(app).post('/users').send({ name: 'Ada' });
  assert.equal(res.status, 400);
});
```

## Python

- **Runner por defecto:** `pytest`. Mantener `unittest` si el proyecto lo usa.
- **Archivos:** `tests/test_<modulo>.py`; funciones `test_<comportamiento>`; fixtures compartidas en `conftest.py`.
- **HTTP:** `TestClient` de FastAPI/Starlette, `app.test_client()` de Flask, `self.client` de Django / `pytest-django`.
- **Ejecutar:** `pytest` (o `python -m pytest -q`).
- **Bug conocido:** `@pytest.mark.xfail(reason="bug: …", strict=True)`; en unittest: `@unittest.expectedFailure`.

```python
def test_create_user_rejects_empty_email(client):
    res = client.post("/users", json={"name": "Ada", "email": ""})
    assert res.status_code == 400
```

## Go

- **Runner:** `go test` (librería estándar `testing`), tests por tabla con `t.Run`.
- **Archivos:** `<archivo>_test.go` en el mismo paquete; `TestXxx(t *testing.T)`.
- **HTTP:** `net/http/httptest` (`httptest.NewRecorder()`, `httptest.NewServer`).
- **Ejecutar:** `go test ./...`.
- **Bug conocido:** `t.Skip("bug: …")` al principio del test.

```go
func TestGetUser_NotFound(t *testing.T) {
    rec := httptest.NewRecorder()
    router.ServeHTTP(rec, httptest.NewRequest("GET", "/users/999", nil))
    if rec.Code != http.StatusNotFound { t.Fatalf("got %d", rec.Code) }
}
```

## Rust

- **Runner:** `cargo test`. Tests unitarios en un `#[cfg(test)] mod tests` dentro del mismo archivo; tests de integración en `tests/`.
- **HTTP:** `ServiceExt::oneshot` de axum/tower, `test::init_service` + `test::call_service` de actix.
- **Ejecutar:** `cargo test`.
- **Bug conocido:** `#[ignore = "bug: …"]` (o `#[should_panic]` solo cuando el pánico es el comportamiento esperado).

## Java / Kotlin

- **Runner por defecto:** JUnit 5 (+ AssertJ si está); Kotlin puede usar Kotest si ya se usa.
- **Archivos:** `src/test/java/.../<Clase>Test.java`, replicando el paquete principal.
- **HTTP:** `MockMvc` / `WebTestClient` de Spring con `@WebMvcTest` o `@SpringBootTest`.
- **Ejecutar:** `./mvnw test` o `./gradlew test`.
- **Bug conocido:** `@Disabled("bug: …")`.

## C# / .NET

- **Runner por defecto:** xUnit (mantener NUnit/MSTest si ya están).
- **Archivos:** un proyecto `<Proyecto>.Tests`; clases `<Clase>Tests`, métodos `Metodo_Escenario_Esperado`.
- **HTTP:** `WebApplicationFactory<Program>` + `HttpClient`.
- **Ejecutar:** `dotnet test`.
- **Bug conocido:** `[Fact(Skip = "bug: …")]` (xUnit), `[Ignore("bug: …")]` (NUnit/MSTest).

## PHP

- **Runner por defecto:** PHPUnit (mantener Pest si ya está).
- **Archivos:** `tests/Unit`, `tests/Feature`; clases `<Algo>Test` que extienden `TestCase`, métodos `test_…`.
- **HTTP:** Laravel `$this->postJson('/users', [...])->assertStatus(400)`; Symfony `WebTestCase`.
- **Ejecutar:** `vendor/bin/phpunit` (o `php artisan test`, `vendor/bin/pest`).
- **Bug conocido:** `$this->markTestIncomplete('bug: …');`.

## Ruby

- **Runner por defecto:** RSpec (mantener Minitest si ya está).
- **Archivos:** `spec/**/*_spec.rb` (RSpec) o `test/**/*_test.rb` (Minitest).
- **HTTP:** request specs de Rails (`post "/users", params: {...}`), `rack-test` para Sinatra.
- **Ejecutar:** `bundle exec rspec` o `bin/rails test`.
- **Bug conocido:** `pending "bug: …"` (RSpec), `skip "bug: …"` (Minitest).
