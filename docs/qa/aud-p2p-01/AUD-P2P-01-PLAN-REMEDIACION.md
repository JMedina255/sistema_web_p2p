# AUD-P2P-01 — Plan de Remediación y Mitigación de Riesgos

**Proyecto:** Sistema Web P2P de Mentorías Académicas EPIS UPT  
**Fecha:** 21 de noviembre de 2026  
**Rama de Intervención:** `fix/auditoria-integral-qa-20261121`  

---

## 1. Orden y Secuencia de Intervención

De acuerdo con el protocolo técnico establecido, el trabajo de remediación se ejecuta en fases estrictamente ordenadas por severidad e impacto:

```
[Fase 1: P0/P1 Críticos] ➔ [Fase 2: Verificación TDD] ➔ [Fase 3: P2 Riesgos Operativos] ➔ [Fase 4: P3 Deuda Técnica]
```

### Matriz de Priorización de Tareas:

| Tarea | Incidencia | Módulo | Severidad | Acción Programada | Estado en esta Sesión |
| :---: | :---: | :--- | :---: | :--- | :---: |
| **T-REM-01** | `P2P-BUG-001` | Frontend / Reservas | **P1 (Alta)** | Desacoplar fixtures de fecha estática en `bookingService.test.ts` | **COMPLETADO (PASS 100%)** |
| **T-REM-02** | `P2P-BUG-002` | Arquitectura / Raíz | **P2 (Media)** | Documentar ruta canónica y mantener exclusión en `.gitignore` | **COMPLETADO (MITIGADO)** |
| **T-REM-03** | `P2P-BUG-003` | Base de Datos / Supabase | **P2 (Media)** | Protocolizar aplicación de migración `006` en ventana de mantenimiento | **DOCUMENTADO (PREPARADO)** |
| **T-REM-04** | `P2P-BUG-004` | Backend / Calidad | **P3 (Baja)** | Modernización de imports `fitz` → `pymupdf` y filtros de warnings | **PROGRAMADO (PRÓXIMA ITERACIÓN)** |

---

## 2. Detalle de Ejecución de Tareas Prioritarias

### Tarea T-REM-01: Corrección de P2P-BUG-001 (Ciclo TDD)

* **Objetivo:** Erradicar la fragilidad de calendario en las pruebas de desistimiento voluntario de reservas (`cancelReservation`), asegurando que la aserción evalúe la transición de estado sin colisionar con la regla temporal de corte a 24 horas (`RN-10`).
* **Estrategia TDD:**
  1. **RED:** Reproducir el fallo ejecutando `vitest run src/services/__tests__/bookingService.test.ts` (Fallo constatado: `BookingException: WINDOW_CLOSED_T24H`).
  2. **GREEN:** Modificar `bookingService.test.ts` para que la propiedad `fecha_inicio` de la reserva semillada se determine como:
     ```typescript
     const mockNow = bookingService.getMockAdapter().getCurrentTime();
     const futureSession = new Date(mockNow + 72 * 3600 * 1000).toISOString();
     ```
     Asimismo, armonizar las fixtures de los escenarios complementarios (8 y 9) para prevenir fallos futuros en noviembre de 2026.
  3. **REFACTOR:** Mantener la claridad semántica y el aislamiento de estado mediante `bookingService.resetToDefaults()`.
  4. **REGRESSION:** Ejecutar la suite completa de 37 archivos en Vitest (366/366 aprobados) y verificar la compilación de producción con `npm run build`.
* **Criterio de Aceptación:** 100% de pruebas aprobadas en Frontend, cero fallos y cobertura superior al 80%.

---

### Tarea T-REM-02: Mitigación de P2P-BUG-002 (Estructura de Directorios)

* **Objetivo:** Evitar ambigüedades operativas para desarrolladores respecto a las carpetas `frontend/` y `aplicacion/frontend/`.
* **Estrategia:**
  1. Confirmar que no existan archivos versionados en `frontend/` mediante `git ls-files frontend`.
  2. Verificar que `.gitignore` excluya explícitamente `frontend/dist/` y `frontend/node_modules/`.
  3. Establecer en la documentación oficial de arquitectura que `aplicacion/frontend/` es la única ruta autorizada para desarrollo, linting, testing y build.
* **Criterio de Aceptación:** Cero impacto en el control de versiones y ausencia de rutas ambiguas en scripts de CI.

---

### Tarea T-REM-03: Protocolo para P2P-BUG-003 (Migración 006 en Supabase)

* **Objetivo:** Establecer el procedimiento seguro para la aplicación de la migración `006_auth_rate_limits.py` en la base de datos de producción Supabase sin generar indisponibilidad ni conflictos RLS.
* **Estrategia Operativa:**
  1. **Pre-condición:** Creación de un snapshot / respaldo de base de datos en el panel de Supabase.
  2. **Ventana de Mantenimiento:** Seleccionar un horario de bajo tráfico institucional.
  3. **Comando de Ejecución:**
     ```bash
     cd aplicacion/backend
     alembic upgrade head
     ```
  4. **Verificación Post-Migración:**
     - Comprobar que `alembic_version` contenga `20261116_006`.
     - Verificar que la tabla `auth_rate_limits` exista con su clave primaria `key` y RLS habilitado.
     - Constatar que roles públicos (`anon`, `authenticated`) tengan acceso revocado y `service_role` tenga permisos completos.
  5. **Verificación de Regresión:** Ejecutar `tools/run_auth_diagnostics.py --allow-remote-db` (validando únicamente claves de prueba con prefijo `test:` o `diag:`).

---

## 3. Plan de Pruebas de Regresión Integral

Para validar la solidez del sistema tras las correcciones, se establece la siguiente batería de comprobación:

| Nivel | Herramienta | Comando | Criterio de Éxito |
| :--- | :--- | :--- | :--- |
| **Backend Lint** | Ruff | `cd aplicacion/backend; ruff check .; ruff format --check .` | 0 errores en 134 archivos |
| **Backend Tests** | Pytest | `cd aplicacion/backend; pytest` | 376 PASS, 1 SKIP, 0 FAIL (Cobertura > 83%) |
| **Backend Diagnostics** | Python | `python tools/run_auth_diagnostics.py` | 16/16 PASS (100%) |
| **Frontend Lint** | ESLint | `cd aplicacion/frontend; npm run lint` | 0 errores / 0 advertencias |
| **Frontend Types & Build** | Vite / TSC | `cd aplicacion/frontend; npm run build` | Compilación limpia en `dist/` |
| **Frontend Tests** | Vitest | `cd aplicacion/frontend; npm test` | 366/366 PASS (37 suites) |
| **Frontend Coverage** | Vitest v8 | `cd aplicacion/frontend; npm run test:coverage` | Cobertura > 82% Stmts / Lines |
