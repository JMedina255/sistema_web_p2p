# Instrucciones del agente

## Alcance

Este repositorio implementa el Sistema Web P2P de Mentorías Académicas de la EPIS-UPT. El hito documental activo se limita a revisar **CUS-001 — Iniciar sesión institucional con 2FA**, sus dos diagramas y la preparación del entorno documental. No modificar CUS-002 a CUS-024, ni ampliar el alcance al SRS o SAD, sin autorización expresa.

## Convenciones documentales

- Usar `NARRATIVAS_CASOS_DE_USO.md` como catálogo vigente y `docs/narrativas/ESTANDAR_REDACCION.md` como norma de redacción.
- Redactar desde la perspectiva del usuario, sin detalles internos de React, FastAPI, endpoints, SQL o archivos fuente.
- Distinguir entre funcionalidad verificada, implementada sin validación suficiente, especificada y futura.
- Mantener las tablas de interacción con las columnas `Acción del Actor` y `Respuesta del Sistema`.
- Editar únicamente fuentes PlantUML necesarias y regenerar solo sus imágenes afectadas.

## Protección del repositorio

- Trabajar en una rama documental; no editar directamente `main`.
- No usar `git reset --hard`, `git clean -fd`, `git push --force`, rebase, stash ni merges automáticos para resolver divergencias.
- No sobrescribir trabajo local ni borrar ramas o commits.
- No leer, modificar ni publicar secretos, credenciales, certificados o archivos `.env`.
- Detenerse ante cambios ajenos, divergencias o dudas que impidan preservar el historial.

## Uso de herramientas y verificación

- Preferir búsquedas focalizadas a cargar documentos extensos completos.
- Usar un único agente de trabajo activo y la herramienta o modelo menos costoso que resuelva correctamente la actividad.
- Verificar Markdown, enlaces locales, coherencia narrativa-diagramas, alcance del diff, `git diff --check` y ausencia de secretos antes de entregar.
- No ejecutar suites completas de frontend o backend para cambios exclusivamente documentales.

## Contexto persistente

- Estado: `.agents/state/CURRENT_STATE.md`
- Siguiente microincremento: `.agents/state/NEXT_TASK.md`
- Reanudación: `.agents/state/HANDOFF.md`
- Flujo documental: `.agents/workflows/DOCUMENTATION_WORKFLOW.md`
