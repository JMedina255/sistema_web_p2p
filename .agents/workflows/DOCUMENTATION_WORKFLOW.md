# Flujo de actualización documental

1. **Delimitar.** Confirmar rama, árbol limpio, microincremento y archivos autorizados.
2. **Localizar.** Buscar identificadores, encabezados, mensajes y controles concretos antes de leer secciones extensas.
3. **Contrastar.** Comparar catálogo, estándar, requisitos, diseño, interfaz, pruebas y evidencias visuales.
4. **Clasificar.** Marcar cada comportamiento como verificado, implementado pendiente de validación, solo especificado o futuro.
5. **Registrar.** Mantener una matriz compacta con documento, problema, evidencia, prioridad y acción recomendada.
6. **Redactar.** Editar únicamente el caso autorizado, con lenguaje funcional, visible y conciso; evitar detalles internos.
7. **Alinear diagramas.** Revisar PlantUML contra la narrativa; modificar y renderizar solo el gráfico afectado.
8. **Verificar.** Comprobar Markdown, enlaces locales, coherencia narrativa-diagramas, imágenes regeneradas, alcance del diff, `git diff --check` y ausencia de secretos.
9. **Cerrar.** Actualizar `CURRENT_STATE.md`, `NEXT_TASK.md` y `HANDOFF.md`; crear un commit local identificable y publicar solo la rama documental si no hay riesgos.
10. **Detener.** Entregar el informe del microincremento y esperar aprobación antes de ampliar el alcance.

## Reglas de economía de contexto

- No cargar documentos extensos completos si bastan índices, encabezados o rangos concretos.
- Reutilizar referencias existentes sin duplicarlas en `.agents/`.
- No repetir auditorías sin una razón verificable.
- Mantener el estado breve y dejar un punto de recuperación al cerrar cada incremento.
