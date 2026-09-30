"""Crea la estructura base de memoria técnica de un proyecto (cualquier lenguaje).

Copia las plantillas de ../templates al proyecto sin sobrescribir archivos
existentes. No añade nada específico de un lenguaje al proyecto.

Uso:
    python bootstrap_project.py [ruta]          # crea lo que falte
    python bootstrap_project.py --check [ruta]  # solo comprueba qué falta
"""
from pathlib import Path
import argparse
import sys

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

# Documentos que todo proyecto debe tener; el resto de plantillas es opcional
# (API, base de datos, skills locales) y solo se informa en --check.
REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    "docs/INDEX.md",
    "docs/PROJECT.md",
    "docs/PROJECT_STATE.md",
    "docs/SESSION_HANDOFF.md",
    "docs/ARCHITECTURE.md",
    "docs/RUNBOOK.md",
    "docs/BUSINESS_RULES.md",
    "docs/DECISIONS.md",
    "docs/TODO.md",
    "docs/WORKLOG.md",
]


def template_files():
    return sorted(p.relative_to(TEMPLATES).as_posix() for p in TEMPLATES.rglob("*") if p.is_file())


def bootstrap(root):
    created, kept = [], []
    for rel in template_files():
        target = root / rel
        if target.exists():
            kept.append(rel)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((TEMPLATES / rel).read_bytes())
        created.append(rel)

    print(f"Proyecto: {root}")
    print(f"Creados: {len(created)}")
    for rel in created:
        print(f"  + {rel}")
    if kept:
        print(f"Conservados (ya existían): {len(kept)}")
        for rel in kept:
            print(f"  = {rel}")
    print("\nSiguiente paso: completar la documentación con hechos comprobados en el código.")


def check(root):
    missing = [rel for rel in REQUIRED if not (root / rel).exists()]
    pending = [rel for rel in REQUIRED if (root / rel).exists()
               and "Por completar" in (root / rel).read_text(encoding="utf-8", errors="ignore")]
    print(f"Proyecto: {root}")
    if missing:
        print("Faltan:")
        for rel in missing:
            print(f"  - {rel}")
    if pending:
        print("Aún con 'Por completar':")
        for rel in pending:
            print(f"  ~ {rel}")
    if not missing and not pending:
        print("Documentación base: OK")
    return 1 if missing else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project", nargs="?", default=".", help="Ruta del proyecto")
    parser.add_argument("--check", action="store_true", help="Solo comprobar, no crear nada")
    args = parser.parse_args()
    # Windows consoles default to a legacy code page; keep accents readable.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = Path(args.project).expanduser().resolve()
    if args.check:
        sys.exit(check(root))
    root.mkdir(parents=True, exist_ok=True)
    bootstrap(root)


if __name__ == "__main__":
    main()
