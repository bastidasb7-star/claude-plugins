# Per-language test reference

Use the section for the project's language. "Default runner" is only for projects that have no tests yet.

## JavaScript / TypeScript

- **Default runner:** `vitest` for Vite/TS projects, otherwise `node:test` (no dependency). Keep `jest` if it's already there.
- **Files:** `*.test.ts` / `*.test.js` next to the code or in `tests/`/`__tests__/`.
- **HTTP:** `supertest` against the exported app (`request(app).get('/users')`); export the app without calling `listen()`.
- **Run:** `npm test` (or `npx vitest run`, `node --test`).
- **Known bug:** `test('…', { todo: 'bug: …' }, fn)` (node:test), `it.todo` / `test.fails` (vitest), `test.failing` (jest).

```js
test('POST /users returns 400 when email is missing', async () => {
  const res = await request(app).post('/users').send({ name: 'Ada' });
  assert.equal(res.status, 400);
});
```

## Python

- **Default runner:** `pytest`. Keep `unittest` if the project uses it.
- **Files:** `tests/test_<module>.py`; functions `test_<behaviour>`; shared fixtures in `conftest.py`.
- **HTTP:** FastAPI/Starlette `TestClient`, Flask `app.test_client()`, Django `self.client` / `pytest-django`.
- **Run:** `pytest` (or `python -m pytest -q`).
- **Known bug:** `@pytest.mark.xfail(reason="bug: …", strict=True)`; unittest: `@unittest.expectedFailure`.

```python
def test_create_user_rejects_empty_email(client):
    res = client.post("/users", json={"name": "Ada", "email": ""})
    assert res.status_code == 400
```

## Go

- **Runner:** `go test` (standard library `testing`), table-driven tests with `t.Run`.
- **Files:** `<file>_test.go` in the same package; `TestXxx(t *testing.T)`.
- **HTTP:** `net/http/httptest` (`httptest.NewRecorder()`, `httptest.NewServer`).
- **Run:** `go test ./...`.
- **Known bug:** `t.Skip("bug: …")` at the top of the test.

```go
func TestGetUser_NotFound(t *testing.T) {
    rec := httptest.NewRecorder()
    router.ServeHTTP(rec, httptest.NewRequest("GET", "/users/999", nil))
    if rec.Code != http.StatusNotFound { t.Fatalf("got %d", rec.Code) }
}
```

## Rust

- **Runner:** `cargo test`. Unit tests in a `#[cfg(test)] mod tests` in the same file; integration tests in `tests/`.
- **HTTP:** axum/tower `ServiceExt::oneshot`, actix `test::init_service` + `test::call_service`.
- **Run:** `cargo test`.
- **Known bug:** `#[ignore = "bug: …"]` (or `#[should_panic]` only when panicking is the intended behaviour).

## Java / Kotlin

- **Default runner:** JUnit 5 (+ AssertJ if present); Kotlin may use Kotest if already in use.
- **Files:** `src/test/java/.../<Class>Test.java` mirroring the main package.
- **HTTP:** Spring `MockMvc` / `WebTestClient` with `@WebMvcTest` or `@SpringBootTest`.
- **Run:** `./mvnw test` or `./gradlew test`.
- **Known bug:** `@Disabled("bug: …")`.

## C# / .NET

- **Default runner:** xUnit (keep NUnit/MSTest if present).
- **Files:** a `<Project>.Tests` project; classes `<Class>Tests`, methods `Method_Scenario_Expected`.
- **HTTP:** `WebApplicationFactory<Program>` + `HttpClient`.
- **Run:** `dotnet test`.
- **Known bug:** `[Fact(Skip = "bug: …")]` (xUnit), `[Ignore("bug: …")]` (NUnit/MSTest).

## PHP

- **Default runner:** PHPUnit (keep Pest if present).
- **Files:** `tests/Unit`, `tests/Feature`; classes `<Thing>Test` extending `TestCase`, methods `test_…`.
- **HTTP:** Laravel `$this->postJson('/users', [...])->assertStatus(400)`; Symfony `WebTestCase`.
- **Run:** `vendor/bin/phpunit` (or `php artisan test`, `vendor/bin/pest`).
- **Known bug:** `$this->markTestIncomplete('bug: …');`.

## Ruby

- **Default runner:** RSpec (keep Minitest if present).
- **Files:** `spec/**/*_spec.rb` (RSpec) or `test/**/*_test.rb` (Minitest).
- **HTTP:** Rails request specs (`post "/users", params: {...}`), `rack-test` for Sinatra.
- **Run:** `bundle exec rspec` or `bin/rails test`.
- **Known bug:** `pending "bug: …"` (RSpec), `skip "bug: …"` (Minitest).
