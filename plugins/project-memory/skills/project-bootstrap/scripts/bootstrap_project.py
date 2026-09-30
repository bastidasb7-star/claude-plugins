from pathlib import Path
import argparse
import sys

AGENTS_MD = """# Instrucciones del repositorio

## Lectura inicial
Antes de cambios significativos leer:
1. `docs/PROJECT_STATE.md`
2. `docs/SESSION_HANDOFF.md`
3. `docs/PROJECT.md`

Leer después solo la documentación relacionada con la tarea.

## Fuente de verdad
El código, configuración, migraciones y tests actuales tienen prioridad sobre documentación desactualizada.

## Continuidad
Después de un cambio significativo actualizar `docs/PROJECT_STATE.md` y `docs/SESSION_HANDOFF.md`, además de la documentación técnica afectada.

No guardar secretos, contraseñas, tokens ni claves en documentación.
"""

CLAUDE_MD = """# Instrucciones del repositorio (Claude Code)

Lee `AGENTS.md` en la raíz de este repositorio y síguelo: contiene las reglas de trabajo, qué documentos de `docs/` leer primero y cómo mantener la continuidad entre sesiones.
"""

PROJECT_SKILL_MD = """---
name: project
description: Trabajar y dar continuidad al proyecto actual usando su estado, handoff, arquitectura, runbook, reglas de negocio y decisiones.
---

# Continuidad del proyecto

Antes de trabajar:
1. leer `AGENTS.md`;
2. leer `docs/PROJECT_STATE.md`;
3. leer `docs/SESSION_HANDOFF.md`;
4. leer `docs/PROJECT.md`;
5. leer solo documentación relacionada con la tarea.

Después de cambios significativos:
1. actualizar `PROJECT_STATE.md`;
2. actualizar `SESSION_HANDOFF.md`;
3. actualizar documentación técnica afectada;
4. actualizar decisiones, pendientes y worklog cuando corresponda.

El código real es la fuente de verdad.
No guardar secretos.
"""

FILES = {
"AGENTS.md": AGENTS_MD,
"CLAUDE.md": CLAUDE_MD,
"docs/INDEX.md": """# Índice de documentación

- `PROJECT.md`: descripción estable.
- `PROJECT_STATE.md`: estado actual.
- `SESSION_HANDOFF.md`: punto exacto para retomar.
- `ARCHITECTURE.md`: arquitectura.
- `RUNBOOK.md`: ejecución y verificación.
- `DATABASE.md`: datos/persistencia.
- `API.md`: contratos.
- `BUSINESS_RULES.md`: reglas funcionales.
- `DECISIONS.md`: decisiones duraderas.
- `TODO.md`: pendientes.
- `WORKLOG.md`: cambios significativos.
""",
"docs/PROJECT.md": """# Proyecto

Última actualización: Por completar

## Nombre
Por completar.

## Propósito
Por completar.

## Usuarios o actores
Por completar.

## Módulos principales
Por completar.

## Stack confirmado
Por completar.

## Estructura principal
Por completar.

## Integraciones externas
Por completar.

## Restricciones importantes
Por completar.
""",
"docs/PROJECT_STATE.md": """# Estado actual del proyecto

Última actualización: Por completar

## Funcionando
- Por completar.

## En desarrollo
- Por completar.

## En pruebas
- Por completar.

## Problemas conocidos
- Por completar.

## Áreas delicadas
- Por completar.

## Próximo objetivo recomendado
- Por completar.
""",
"docs/SESSION_HANDOFF.md": """# Handoff de la sesión

Actualizado: Por completar

## Objetivo en curso
Por completar.

## Último trabajo realizado
Por completar.

## Archivos o módulos clave
- Por completar.

## Verificación realizada
- Por completar.

## Falta por hacer
- Por completar.

## Siguiente paso concreto
Por completar.

## Advertencias / contexto
- Por completar.
""",
"docs/ARCHITECTURE.md": """# Arquitectura

Última actualización: Por completar

## Vista general
Por completar.

## Componentes
Por completar.

## Flujo principal
Por completar.

## Dependencias internas
Por completar.

## Integraciones externas
Por completar.

## Riesgos técnicos
Por completar.
""",
"docs/RUNBOOK.md": """# Runbook

Última actualización: Por completar

Documentar únicamente comandos comprobados.

## Requisitos
Por completar.

## Instalación
Por confirmar.

## Configuración
Por completar.

## Ejecutar
Por confirmar.

## Pruebas
Por confirmar.

## Lint / validaciones
Por confirmar.

## Build
Por confirmar.

## Migraciones
No aplica o por confirmar.

## Despliegue
No aplica o por confirmar.
""",
"docs/DATABASE.md": """# Base de datos y persistencia

Última actualización: Por completar

Si no existe persistencia, indicar `No aplica`.

## Motor / tecnología
Por confirmar.

## Entidades o tablas
Por completar.

## Relaciones
Por completar.

## Restricciones
Por completar.

## Migraciones
Por completar.

## Integridad / riesgos
Por completar.
""",
"docs/API.md": """# API

Última actualización: Por completar

Si no existe API relevante, indicar `No aplica`.

## Autenticación
Por confirmar.

## Endpoints
Por completar.

## Contratos
Por completar.

## Roles
Por completar.

## Errores
Por completar.
""",
"docs/BUSINESS_RULES.md": """# Reglas de negocio

Última actualización: Por completar

## Reglas confirmadas
- Por completar.

## Permisos / roles
- Por completar.

## Validaciones críticas
- Por completar.

## Flujos que no deben romperse
- Por completar.

## Por confirmar
- Por completar.
""",
"docs/DECISIONS.md": """# Decisiones

Registrar solo decisiones con impacto duradero.

Todavía no hay decisiones registradas.
""",
"docs/TODO.md": """# Pendientes

Última actualización: Por completar

## Alta
- [ ] Por completar.

## Media
- [ ] Por completar.

## Baja
- [ ] Por completar.

## Bloqueados
- [ ] Por completar.
""",
"docs/WORKLOG.md": """# Historial de trabajo

Registrar cambios significativos, no conversaciones completas.

Todavía no hay cambios registrados.
""",
".agents/skills/project/SKILL.md": PROJECT_SKILL_MD,
".claude/skills/project/SKILL.md": PROJECT_SKILL_MD,
"scripts/project_docs_check.py": """from pathlib import Path
import sys

REQUIRED = [
    'AGENTS.md',
    'docs/INDEX.md',
    'docs/PROJECT.md',
    'docs/PROJECT_STATE.md',
    'docs/SESSION_HANDOFF.md',
    'docs/ARCHITECTURE.md',
    'docs/RUNBOOK.md',
    'docs/BUSINESS_RULES.md',
    'docs/DECISIONS.md',
    'docs/TODO.md',
    'docs/WORKLOG.md',
]

OPTIONAL = [
    'CLAUDE.md',
    'docs/DATABASE.md',
    'docs/API.md',
    '.agents/skills/project/SKILL.md',
    '.claude/skills/project/SKILL.md',
]

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
missing = [p for p in REQUIRED if not (root / p).exists()]
print('Proyecto:', root)
if missing:
    print('Faltan:')
    for p in missing:
        print(' -', p)
    raise SystemExit(1)
print('Documentación base: OK')
""",
}

def main():
    parser = argparse.ArgumentParser(
        description="Crea la estructura base de continuidad de proyecto (multi-IA) sin sobrescribir archivos."
    )
    parser.add_argument("project", nargs="?", default=".", help="Ruta del proyecto")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    for rel, content in FILES.items():
        p = root / rel
        if p.exists():
            skipped.append(rel)
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
        created.append(rel)

    print(f"Proyecto: {root}")
    print(f"Creados: {len(created)}")
    for p in created:
        print(f"  + {p}")
    if skipped:
        print(f"Conservados (ya existían): {len(skipped)}")
        for p in skipped:
            print(f"  = {p}")

    print("\nSiguiente paso:")
    print("Pide a tu asistente de IA (Claude Code, Codex u otro) que analice el repositorio")
    print("y complete la documentación con hechos comprobados.")

if __name__ == "__main__":
    main()
