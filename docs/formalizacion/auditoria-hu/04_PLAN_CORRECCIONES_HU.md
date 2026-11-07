# 04 — Plan Priorizado de Correcciones Funcionales y Técnicas para la Fase 05

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Etapa:** Auditoría Integral de Cumplimiento Funcional (Fase 04-B)  
**Fecha de Emisión:** 7 de noviembre de 2026  
**Rama:** `feat/formalizacion-ux-roles`  
**Estado:** Plan Operativo de Intervención SQA  

---

## 1. Estrategia y Niveles de Prioridad

Con base en los hallazgos de la auditoría de historias de usuario, cumplimiento funcional y seguridad, se establece un plan de intervención escalonado para ser ejecutado durante la **Fase 05**, previo a la presentación formal de avances del proyecto.

Las acciones se clasifican bajo los siguientes criterios de severidad:
- **P0 — Bloqueante Inmediato:** Impide la compilación de producción, rompe la integración continua o causa errores en tiempo de ejecución.
- **P1 — Crítico de Calidad y Presentación:** Impacta directamente en la demostración en vivo ante los evaluadores académicos o en la consistencia de seguridad del sistema.
- **P2 — Inconsistencia Documental y Ergonomía:** Discrepancias entre artefactos formales (SRS/SAD/Bitácoras) que dificultan la defensa metodológica.
- **P3 — Deuda Técnica y Producción Futura:** Mejoras de arquitectura planificadas para los Sprints 07, 08 o el pase a producción masiva.

---

## 2. Matriz del Plan de Correcciones

| ID Tarea | Prioridad | Componente / Archivo | Problema / Causa | Acción Concreta de Corrección | Esfuerzo Estimado |
|---|:---:|---|---|---|:---:|
| **CORR-01** | **P0** | `aplicacion/frontend/src/components/__tests__/MentorSessionsView.test.tsx` | Error TS2353 en `npm run build`: la propiedad `motivo_cancelacion` en el mock no existe en `QuorumDecisionResponse`. | Eliminar la propiedad `motivo_cancelacion` en las líneas 79, 143 y 186 del archivo de prueba, o incluirla como opcional en `QuorumDecisionResponse` en `offerService.ts`. | 15 min |
| **CORR-02** | **P1** | `aplicacion/backend/` (14 archivos) | `python -m ruff format --check .` reporta 14 archivos con diferencias de espaciado y saltos de línea. | Ejecutar `python -m ruff format .` para estandarizar el estilo visual en todo el backend sin alterar la lógica. | 5 min |
| **CORR-03** | **P1** | `aplicacion/backend/app/db/seed_data.py` / scripts SQL | Para la demo en vivo, se requiere transicionar sesiones sin esperar 24 horas reales. | Suministrar una semilla enriquecida con sesiones en estados `PUBLICADA`, `QUORUM_INSUFICIENTE`, `CONFIRMADA` y `CONCLUIDA`. | 30 min |
| **CORR-04** | **P1** | `aplicacion/frontend/.env.example` y `.env` | En desarrollo, el frontend podría inicializarse en modo mock por defecto si no se explicita la variable. | Asegurar que `VITE_SERVICE_MODE=api` esté configurado en `.env` para garantizar que la demo consuma los endpoints de FastAPI. | 10 min |
| **CORR-05** | **P2** | `docs/sprints/sprint-06.md` y `docs/sprints/sprint-06/README.md` | Confusión de casos de uso: Sprint 06 rotuló Asistencia y Bitácora como CUS12/CUS13 en vez de `CUS08` (RF17). | Corregir las referencias en los documentos del Sprint 06 para armonizarlos con el Cuadro 5.5 del SRS FD03 maestro. | 20 min |
| **CORR-06** | **P2** | `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` | El SAD menciona Python 3.11 en el apartado §2.5, cuando el proyecto utiliza oficialmente Python 3.13.5. | Homologar la versión en el texto del SAD reflejando la decisión tomada en el Sprint 01 (`PLAN_SPRINTS_Y_TAREAS.md`). | 10 min |
| **CORR-07** | **P2** | `aplicacion/frontend/src/services/offerService.ts` | En modo desconectado, `offerService` almacena sesiones en `localStorage` de forma aislada a la API. | Sincronizar la lectura del listado de sesiones del mentor con el backend FastAPI cuando `VITE_SERVICE_MODE=api`. | 45 min |
| **CORR-08** | **P3** | `aplicacion/backend/app/core/dependencies.py` | JWT stateless confía en claims `roles` sin consultar base de datos durante los 60 min de vida del token. | Para operaciones administrativas de alto impacto, añadir consulta directa a `RoleService.get_user_roles(db, email)`. | 30 min |
| **CORR-09** | **P3** | `aplicacion/backend/app/services/auth_service.py` | Despacho SMTP de OTP simulado en consola local. | Integrar adaptador de proveedor SMTP institucional o servicio transaccional (Resend / AWS SES) con variables de entorno. | 2 horas (Sprint 08) |
| **CORR-10** | **P3** | `OfferPublishView.tsx` | Aprovisionamiento de aulas y enlaces virtuales manual (RF09 diferido a PB-033/034). | Mantener advertencia explicativa en interfaz y preparar guion de defensa académica. | Documental |

---

## 3. Protocolo de Verificación Posterior a Correcciones

Una vez ejecutadas las correcciones en la Fase 05, se deberá comprobar de manera estricta:

1. **Compilación de Producción Frontend:**
   ```powershell
   Set-Location "aplicacion/frontend"
   npm run build
   ```
   *Criterio de éxito:* Salida en verde con generación de directorio `dist/` y **0 errores TypeScript**.

2. **Linter y Formato Backend:**
   ```powershell
   Set-Location "aplicacion/backend"
   python -m ruff check .
   python -m ruff format --check .
   ```
   *Criterio de éxito:* Ambos comandos retornan `0` con mensaje `All checks passed!` y `0 files would be reformatted`.

3. **Batería Completa de Pruebas:**
   - Backend: `python -m pytest tests/ -q` (237 pruebas passing, >= 85% cobertura).
   - Frontend: `npm test -- --run` (311 pruebas passing).
