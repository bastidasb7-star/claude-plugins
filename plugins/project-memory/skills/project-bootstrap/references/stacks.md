# Dónde encontrar los hechos según el stack

Referencia para el Paso 1. Usar solo la sección del stack detectado. Todo comando que se documente en `RUNBOOK.md` debe salir de estos archivos, no de la memoria.

| Stack | Manifiesto / config | Comandos (instalar · ejecutar · test · lint · build) | Migraciones / datos | API / rutas |
|-------|---------------------|------------------------------------------------------|---------------------|-------------|
| JavaScript / TypeScript (Node, Bun, Deno) | `package.json` (`scripts`), lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`), `tsconfig.json`, `deno.json`, `nx.json`/`turbo.json` (monorepo) | `scripts` de `package.json`; gestor según el lockfile (npm/pnpm/yarn/bun) | `prisma/schema.prisma` + `prisma/migrations`, `migrations/` (Knex, TypeORM, Sequelize), `drizzle/` | Express/Fastify/Koa: `routes/`, `app.*`; NestJS: `*.controller.ts`; Next.js: `app/api`, `pages/api` |
| Python | `pyproject.toml`, `requirements*.txt`, `Pipfile`, `setup.cfg`, `tox.ini`, `noxfile.py` | `[project.scripts]`, `[tool.poetry.scripts]`, `Makefile`, `tox`/`nox`; tests `pytest` | Django: `*/migrations/`; Alembic: `alembic/versions/`; SQLAlchemy models | Django: `urls.py`; FastAPI/Flask: decoradores `@app.get`, `@router.*`, `@bp.route` |
| Go | `go.mod`, `Makefile`, `Taskfile.yml` | `go build ./...`, `go test ./...`, `golangci-lint run` si hay config | `migrations/` (golang-migrate, goose), `sqlc.yaml` | `http.HandleFunc`, routers Gin/Echo/Chi/Fiber en `cmd/`, `internal/` |
| Rust | `Cargo.toml` (workspace), `rust-toolchain.toml` | `cargo build`, `cargo test`, `cargo clippy`, `cargo fmt` | `migrations/` (sqlx, diesel), `diesel.toml` | axum `Router::new().route`, actix `#[get]`/`web::resource` |
| Java / Kotlin / Scala | `pom.xml`, `build.gradle(.kts)`, `settings.gradle`, `build.sbt`, wrappers `mvnw`/`gradlew` | `./mvnw …`/`./gradlew tasks`, `sbt test` | Flyway `db/migration/V*__*.sql`, Liquibase `changelog`, entidades JPA `@Entity` | Spring `@RestController`, `@RequestMapping`; Ktor `routing {}` |
| C# / .NET | `*.sln`, `*.csproj`, `global.json`, `Directory.Build.props` | `dotnet restore`, `dotnet run --project …`, `dotnet test`, `dotnet build` | EF Core `Migrations/`, `DbContext` | Controllers `[ApiController]`, minimal APIs `app.MapGet` |
| PHP | `composer.json` (`scripts`), `artisan`, `symfony.lock` | `composer install`, `php artisan …`, `vendor/bin/phpunit` | Laravel `database/migrations`, Doctrine `migrations/` | Laravel `routes/*.php`; Symfony atributos `#[Route]` |
| Ruby | `Gemfile`, `Rakefile`, `.ruby-version` | `bundle install`, `bin/rails …`, `bundle exec rspec`, `rubocop` | Rails `db/migrate`, `db/schema.rb` | Rails `config/routes.rb`; Sinatra `get '/…'` |
| Elixir | `mix.exs` | `mix deps.get`, `mix phx.server`, `mix test` | `priv/repo/migrations` | Phoenix `router.ex` |
| Dart / Flutter | `pubspec.yaml`, `analysis_options.yaml` | `flutter pub get`, `flutter run`, `flutter test`, `dart analyze` | — | — |
| Swift / iOS | `Package.swift`, `*.xcodeproj`, `Podfile` | `swift build`, `swift test`, `xcodebuild` | Core Data `*.xcdatamodeld` | Vapor `routes.swift` |
| C / C++ | `CMakeLists.txt`, `Makefile`, `meson.build`, `conanfile.*`, `vcpkg.json` | `cmake --build`, `ctest`, `make`, `make test` | — | — |

## En cualquier stack

- **Contenedores e infraestructura:** `Dockerfile`, `docker-compose*.yml`, `k8s/`, `helm/`, `*.tf` (Terraform).
- **CI/CD:** `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`. Suelen ser la mejor fuente de los comandos reales de test y build.
- **Variables de entorno:** `.env.example`, `appsettings*.json`, `application*.yml`, `config/`. Documentar solo los **nombres** de las variables, nunca sus valores.
- **Monorepos:** detectar cada subproyecto por su propio manifiesto y documentar sus comandos por separado en `RUNBOOK.md`.

## Carpetas a ignorar

`.git`, `node_modules`, `vendor`, `dist`, `build`, `out`, `target`, `bin`, `obj`, `.gradle`, `.venv`, `venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.next`, `.nuxt`, `.angular`, `.svelte-kit`, `.dart_tool`, `Pods`, `DerivedData`, `.terraform`, `coverage`, `.idea`, `.vs`, además de binarios y artefactos grandes.
