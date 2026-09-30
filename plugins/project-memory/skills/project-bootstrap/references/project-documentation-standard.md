# Estándar de memoria técnica del proyecto

## Propósito

La memoria técnica existe para responder rápidamente:

1. ¿Qué es este proyecto?
2. ¿Cómo está construido?
3. ¿Cómo se ejecuta y verifica?
4. ¿Qué reglas no deben romperse?
5. ¿Cuál es el estado actual?
6. ¿Dónde quedó el trabajo?
7. ¿Qué decisiones importantes ya se tomaron?
8. ¿Qué queda pendiente?

## Separación de responsabilidades

### Estado presente
`PROJECT_STATE.md`

### Continuidad inmediata
`SESSION_HANDOFF.md`

### Historia resumida
`WORKLOG.md`

### Decisiones duraderas
`DECISIONS.md`

### Pendientes
`TODO.md`

No mezclar estas funciones.

## Regla de tamaño

Preferir documentos cortos y mantenibles.

Si una sección crece demasiado:
- resumir;
- mover detalles especializados a otro archivo;
- mantener enlaces desde `INDEX.md`.

## Fuente de verdad

Prioridad de evidencia:

1. código y configuración actual;
2. tests;
3. migraciones/esquema;
4. documentación actual del repositorio;
5. reglas explícitas del usuario.

Si existe contradicción, investigarla y documentarla.

## Seguridad

Nunca copiar:
- `.env`;
- tokens;
- cookies;
- passwords;
- API keys;
- private keys;
- secretos de CI/CD.

Se puede documentar el NOMBRE de una variable de entorno, pero no su valor secreto.
