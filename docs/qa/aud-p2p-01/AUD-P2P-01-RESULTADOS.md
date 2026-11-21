# AUD-P2P-01 — Informe de Resultados y Verificación Posterior

**Proyecto:** Sistema Web P2P de Mentorías Académicas EPIS UPT  
**Fecha:** 21 de noviembre de 2026  
**Rama de Trabajo:** `fix/auditoria-integral-qa-20261121`  
**Commit Inicial Base:** `4400a14ef3b805179ce581b94d5aeb87d328ae61`  
**Commit de Corrección:** `8be2a28b57be28fec3da810ff408542b85d95856`  

---

## 1. Resumen de Correcciones Implementadas

En esta sesión se abordó de manera prioritaria la incidencia confirmada **P2P-BUG-001** (Prioridad P1), relativa a la fragilidad temporal en las pruebas unitarias de desistimiento voluntario de reservas (`cancelReservation`) en el frontend.

### Detalle de Modificación:
* **Archivo:** `aplicacion/frontend/src/services/__tests__/bookingService.test.ts`
* **Naturaleza del Cambio:** Desacoplamiento de fixtures estáticas absolutas hacia fechas relativas calculadas a partir del reloj simulado del adaptador en memoria.
* **Líneas Modificadas:**
  - Línea 677: Fecha de inicio de sesión previa ajustada dinámicamente con `mockAdapter.getCurrentTime() + 72h`.
  - Línea 697: Fecha de sesión de prueba de control de acceso ajeno ajustada dinámicamente con `mockAdapter.getCurrentTime() + 72h`.
  - Línea 852: Cálculo dinámico de `futureSession` a +72 horas del reloj del adaptador para la prueba de fachada `cancelReservation(888)`, garantizando que la diferencia `startTime - now` supere siempre el límite de 24 horas estipulado en la regla institucional `RN-10`.

---

## 2. Comparativa de Resultados Antes vs. Después

| Suite / Herramienta | Métrica / Indicador | Estado Antes (Línea Base) | Estado Después de la Remediación | Variación |
| :--- | :--- | :---: | :---: | :---: |
| **Vitest Frontend** | Suites de prueba | 36 PASS / 1 FAIL (37 total) | **37 PASS / 0 FAIL (37 total)** | **+1 suite recuperada (100% PASS)** |
| **Vitest Frontend** | Pruebas individuales | 365 PASS / 1 FAIL (366 total) | **366 PASS / 0 FAIL (366 total)** | **+1 prueba aprobada (100% PASS)** |
| **Frontend Coverage** | Cobertura de declaraciones | No generada (abortó por fallo) | **82.44% Statements** | **Supera meta (> 80%)** |
| **Frontend Coverage** | Cobertura de líneas | No generada (abortó por fallo) | **82.44% Lines** | **Supera meta (> 80%)** |
| **Frontend Coverage** | Cobertura de ramas | No generada (abortó por fallo) | **75.82% Branches** | **Estable** |
| **Frontend Build** | Compilación producción | PASS (2.63s) | **PASS (2.58s)** | **Sin regresiones** |
| **Frontend Linter** | ESLint | 0 errores / 0 warnings | **0 errores / 0 warnings** | **Limpio** |
| **Pytest Backend** | Pruebas ejecutadas | 376 PASS / 1 SKIP / 0 FAIL | **376 PASS / 1 SKIP / 0 FAIL** | **100% Estable** |
| **Backend Coverage** | Cobertura total Pytest | 83.66% | **83.66%** | **Supera umbral (70.0%)** |
| **Backend Linter** | Ruff | All checks passed (134 files) | **All checks passed (134 files)** | **Limpio** |
| **Diagnóstico Auth** | `run_auth_diagnostics.py` | 16/16 PASS | **16/16 PASS** | **100% Estable** |
| **Expo Demo Ready** | `test_expo_ready.py` | 6/6 endpoints HTTP 200 | **6/6 endpoints HTTP 200** | **100% Estable** |

---

## 3. Estado del Inventario de Incidencias Post-Intervención

| Identificador | Título del Hallazgo | Prioridad | Estado Final |
| :---: | :--- | :---: | :---: |
| **P2P-BUG-001** | Fragilidad temporal en prueba unitaria de `bookingService.test.ts` | **P1 (Alta)** | **RESUELTO** |
| **P2P-BUG-002** | Directorio residual `frontend/` en raíz | **P2 (Media)** | **DOCUMENTADO (Mitigado)** |
| **P2P-BUG-003** | Desalineación de migración 006 en Supabase producción | **P2 (Media)** | **DOCUMENTADO (Preparado)** |
| **P2P-BUG-004** | Advertencias de deprecación externa en Pytest | **P3 (Baja)** | **DOCUMENTADO (Deuda Técnica)** |

---

## 4. Trazabilidad de Commits Generados

* **Commit `8be2a28`:**
  - **Mensaje:** `fix(tests): desacoplar fixtures temporales en bookingService.test.ts para prevenir expiracion de cortes T-24h (P2P-BUG-001)`
  - **Hash Completo:** `8be2a28b57be28fec3da810ff408542b85d95856`
  - **Archivos Modificados:** `aplicacion/frontend/src/services/__tests__/bookingService.test.ts` (+7 / -5 líneas).
* **Commit `f6bf53d`:**
  - **Mensaje:** `docs(qa): incorporar documentacion integral de auditoria y remediacion AUD-P2P-01`
  - **Hash Completo:** `f6bf53d2d9adfa914972e293a54d5b78b021d749`
  - **Archivos Modificados:** 4 documentos en `docs/qa/aud-p2p-01/` (+385 líneas).
* **Commit de Integración en `main` (Merge PR #19):**
  - **Mensaje:** `Merge pull request #19 from JMedina255/fix/auditoria-integral-qa-20261121`
  - **Hash Completo:** `432220960f4a4ec13c2382236689e363f766e57d`
  - **Resultado en GitHub Actions CI:** Run #106 completado con veredicto **SUCCESS** (100% aprobado).

---

## 5. Riesgos Residuales y Recomendaciones de Despliegue

1. **Riesgo Residual R-01 (Migración 006):**
   - La tabla `auth_rate_limits` debe crearse en Supabase ejecutando `alembic upgrade head` en la ventana de mantenimiento autorizada antes de activar `STRICT_DATABASE_MODE=true` en producción.
2. **Riesgo Residual R-02 (SMTP Institucional):**
   - El envío y recepción de correos en buzones reales `@upt.pe` debe validarse mediante el Protocolo de 5 Momentos documentado una vez ingresadas las credenciales oficiales `SMTP_USER` y `SMTP_PASSWORD` en el entorno productivo.
