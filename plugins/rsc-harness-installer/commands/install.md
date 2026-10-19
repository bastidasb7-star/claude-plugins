---
description: Instala rsc-harness (ericrisco/rsc-harness) en el proyecto actual.
---

Instalar rsc-harness en el proyecto actual, siguiendo el flujo oficial que
documenta el propio proyecto (https://github.com/ericrisco/rsc-harness):

1. Confirmar que `npx` está disponible (`npx --version`). Si no lo está,
   informar el error al usuario y detenerse — no intentar instalarlo de otra
   forma.
2. Ejecutar `npx @ericrisco/rsc@latest onboard` en la raíz del proyecto
   actual.
3. Seguir el onboarding interactivo que ese comando dispara: responder las
   preguntas que pida, mostrar el plan exacto que proponga, y esperar la
   aceptación explícita del usuario antes de que escriba o modifique ningún
   archivo del proyecto.
4. No asumir ninguna configuración en nombre del usuario; si el onboarding
   pide una decisión, preguntarle a él.

Esto instala la versión más reciente publicada en npm de rsc-harness, no
depende del submódulo vendorizado en `plugins/rsc-harness` de este
marketplace (ese es solo una copia navegable del código fuente).
