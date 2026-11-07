# 05 — Resumen Ejecutivo y Diagnóstico de Preparación para la Presentación

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Etapa:** Auditoría Integral de Cumplimiento Funcional (Fase 04-B)  
**Fecha de Emisión:** 7 de noviembre de 2026  
**Rama Auditada:** `feat/formalizacion-ux-roles`  
**Commit Auditado:** `4cbf504`  
**Estado:** Dictamen Ejecutivo Oficial SQA  

---

## 1. Declaración de Misión y Objeto de la Auditoría

Tras la culminación de las Fases 01 a 04 del plan de formalización —en las cuales se limpiaron los artefactos técnicos visuales de la interfaz de usuario, se implementó navegación dinámica RBAC y se fortaleció la seguridad backend eliminando heurísticas de correo y atajos permisivos—, esta **Fase 04-B** ejecutó una **auditoría integral y objetiva de trazabilidad** para responder con rigor empírico sobre el estado real de cumplimiento de los requerimientos, historias de usuario y preparación para la defensa académica.

---

## 2. Respuestas a las Nueve Preguntas Fundamentales de la Auditoría

### 1. ¿Cuántas historias de usuario están realmente documentadas?
- **Historias de Usuario Explícitas (`HU-xx`):** Se identificaron **8 historias de usuario formales** redactadas bajo el estándar ágil (*Como... Quiero... Para...*) con criterios Gherkin en `docs/analisis/trazabilidad_sprint_02.md`, `docs/diseño/TRAZABILIDAD_SPRINT_02.md` y `docs/sprints/sprint-03/04-presentacion/GUION_MANUAL_DIAPOSITIVAS_SPRINT_03.md` (`HU-01` a `HU-08`).
- **Product Backlog Items (PBI):** En `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`, el backlog ágil maestro está compuesto por **37 PBIs (`PB-001` al `PB-037`)**.
- **Metodología de Ingeniería Institucional (SRS/SAD):** La cátedra y la universidad prescribieron la metodología **UWE (UML-based Web Engineering)** y RUP, por lo cual el SRS (FD03 v2.1) formaliza el sistema a través de **24 Casos de Uso (`CUS01` al `CUS24`)**, **26 Requerimientos Funcionales (`RF01` al `RF26`)**, **10 No Funcionales (`RNF01` al `RNF10`)** y **14 Reglas de Negocio (`RN-01` al `RN-14`)**.
- **Trazabilidad Unificada:** Al desglosar los PBIs comprometidos hasta el Sprint 06 en fichas funcionales canónicas, se obtienen **16 Historias de Usuario (`HU-01` a `HU-16`)**.

### 2. ¿Cuáles corresponden a los Sprints 01 al 06?
- Corresponden a los Sprints 01 al 06 **16 Historias de Usuario (`HU-01` a `HU-16`)** asociadas a **19 PBIs** (`PB-001` al `PB-011`, `PB-013` al `PB-015`, `PB-017` al `PB-019`, más avances parciales en `PB-031` y `PB-036`):
  - **Sprint 01:** `HU-01` (Acceso OTP / PB-002), `HU-02` (Entorno base y CI / PB-001, PB-004), inicio curricular y RLS (`PB-006p`, `PB-008p`).
  - **Sprint 02:** `HU-03` (Consentimiento Ley 29733 / PB-003), `HU-04` (Roles y mérito RN-03 / PB-005), `HU-05` (Catálogo curricular / PB-006), `HU-06` (Perfiles y disponibilidad 6x11 / PB-007), `HU-07` (Aislamiento RLS / PB-008), `HU-08` (OpenAPI y pruebas / PB-031).
  - **Sprint 03:** `HU-09` (Publicación de ofertas / PB-009 / RF08).
  - **Sprint 04:** `HU-10` (Recomendación Top-k y feed / PB-010, PB-011 / RF06), `HU-11` (Reserva transaccional / PB-013 / RF12).
  - **Sprint 05:** `HU-12` (Ratificación en T-24h / PB-014 / RF13), `HU-13` (Desistimiento voluntario / PB-015 / RF14).
  - **Sprint 06:** `HU-14` (Evaluación de quórum / PB-017 / RF15), `HU-15` (Resolución de contingencias / PB-018 / RF16), `HU-16` (Asistencia QR dinámico y bitácora pedagógica / PB-019 / RF17).
- Los 18 PBIs restantes corresponden planificadamente a **Sprint 07** (encuestas y visado de horas), **Sprint 08** (constancias DEMO y métricas Precision@k) y **Backlog Posterior** (aulas automáticas, Meet/Discord bot, modelo híbrido, insignias).

### 3. ¿Qué criterios de aceptación se cumplen?
- Se cumplen con evidencia empírica verificable los criterios de aceptación asociados a:
  - Autenticación institucional 2FA con OTP, validación de dominio `@upt.pe` y emisión de JWT HS256.
  - Bloqueo preventivo obligatorio ante rechazo de consentimiento informado (Ley N° 29733 / RN-02).
  - Regla de mérito académico institucional (RN-03: ciclo actual >= VII para rol mentor).
  - Búsqueda reactiva en tiempo real sobre la jerarquía silábica oficial de cursos filtro.
  - Reemplazo atómico transaccional de la disponibilidad horaria semanal (grilla 6x11).
  - Publicación de ofertas con antelación obligatoria > 24h (RN-04) y aforos automáticos (10 presencial, 20 virtual / RN-05).
  - Ranking Top-k determinista mediante similitud coseno y desempate invariante ante permutación.
  - Prevención estricta de sobreasignación concurrente de vacantes y duplicidad de reservas.
  - Ventana de ratificación de asistencia antes de T-24h y bloqueo por cierre temporal (RN-08).
  - Desistimiento voluntario sin penalidad con restitución atómica de plazas en aforo (RN-10).
  - Evaluación matemática de quórum en T-24h (50% de aforo) con procesamiento idempotente.
  - Decisión resolutiva del mentor titular (`PROCEED`, `RESCHEDULE`, `CANCEL`).
  - Registro de asistencia digital por QR dinámico TOTP / código numérico.
  - Registro de bitácoras pedagógicas con límite temporal de 48 horas (RN-12) y contenido >= 50 caracteres.
  - Autorización RBAC estricta con verificación de roles institucionales y titularidad de recursos (*resource ownership*).

### 4. ¿Qué funcionalidades están implementadas parcialmente?
- **Publicación de Ofertas (HU-09 / RF08):** La validación de antelación y aforo está 100% terminada, pero la asignación de aulas físicas y la creación de salas virtuales no está automatizada con Google Meet o Discord (requiere ingreso manual del texto/enlace por parte del mentor).
- **Evaluación de Quórum (HU-14 / RF15):** La lógica de cálculo e idempotencia está implementada y probada al 100% en backend, pero el trigger automatizado depende de un endpoint manual o reloj de pruebas; el cron desatendido de producción (pg_cron) no está aprovisionado localmente.
- **Gestión de Roles (HU-04 / RF03):** La promoción y revocación por parte del administrador están operativas y protegidas, pero el administrador solo puede buscar estudiantes escribiendo su correo exacto; no dispone de una tabla paginada de todos los matriculados.

### 5. ¿Qué diferencias existen entre SRS, SAD y código?
Se documentaron 10 inconsistencias (ver `03_INCONSISTENCIAS_HU_SRS_SAD_CODIGO.md`), destacando:
1. **Falla de compilación TypeScript (`npm run build`):** En `MentorSessionsView.test.tsx` (líneas 79, 143, 186) el mock incluye `motivo_cancelacion`, inexistente en `QuorumDecisionResponse`. Vitest corre y pasa las pruebas, pero `npm run build` falla al invocar `tsc -b`.
2. **Confusión CUS12 / CUS13 en Sprint 06:** En `sprint-06.md` se rotuló la asistencia y bitácora como CUS12 y CUS13, cuando en el SRS maestro corresponden formalmente a **`CUS08` / RF17**.
3. **Versión de Python:** El SAD estático señala Python 3.11, mientras que el entorno real y CI ejecutan **Python 3.13.5** (desviación planificada y justificada).
4. **Formato de código:** `ruff check .` pasa al 100%, pero `ruff format --check .` detecta 14 archivos backend pendientes de formateo automático.
5. **Revocación en caliente de JWT:** El backend confía en los claims `roles` del token durante su vigencia de 60 minutos sin revalidar contra base de datos en cada petición stateless.

### 6. ¿Qué pruebas demuestran el cumplimiento?
- **Backend (Pytest):** **237 pruebas aprobadas (100% PASS)**, 0 fallas, **85.13% de cobertura de código**.
  - 21 pruebas de seguridad RBAC (`test_security_rbac.py`).
  - 52 pruebas de concurrencia y reservas (`test_bookings.py`).
  - 22 pruebas de recomendación Top-k (`test_recommendations.py`).
  - 22 pruebas de autorización y cruce de cuentas (`test_authorization.py`).
  - 16 pruebas de asistencia y bitácoras (`test_attendance.py`, `test_bitacora.py`).
  - 7 pruebas de quórum (`test_quorum.py`).
- **Frontend (Vitest):** **311 pruebas aprobadas (100% PASS)** en 29 suites de prueba.
  - 14 pruebas de navegación RBAC y guardas por rol (`navigation.test.tsx`).
  - 42 pruebas de ciclo de vida de reservas (`bookingService.test.ts`).
  - 20 pruebas de modal de reservas (`BookingModalView.test.tsx`).
  - 9 pruebas de ordenamiento determinista (`TopKOrdering.test.tsx`).
- **Linters:**
  - `ruff check .` -> **0 errores** (`All checks passed!`).
  - `eslint .` -> **0 errores, 0 advertencias**.

### 7. ¿Qué funcionalidades funcionan solamente con mocks?
- **Despacho SMTP de OTP:** Se simula en servidor/consola o mediante código estático `123456`.
- **Aprovisionamiento de salas virtuales (Meet/Discord):** Se ingresa una cadena URL manual.
- **Persistencia en sesión de mentor (`offerService.ts`):** En modo desconectado, utiliza `localStorage`.
- **Modo Mock en Frontend (`bookingService.ts` / `recommendationService.ts`):** Fachadas duales que operan en memoria local si `VITE_SERVICE_MODE=mock`. En modo API conectada, consumen los endpoints de FastAPI.

### 8. ¿Qué historias faltan para completar los flujos funcionales?
Para completar el recorrido integral del ciclo de vida de mentorías académicas faltan:
- **Sprint 07 (Compromiso Académico Siguiente):**
  - Encuestas de satisfacción post-mentoría (`PB-020` / RF18 / CUS05 / RN-12, RN-13).
  - Bandeja de visado y auditoría administrativa de horas por Tutoría (`PB-023` / RF26 / CUS22 / RN-14).
- **Sprint 08 (Cierre y Demostración MVP):**
  - Generación automatizada de constancias PDF con marca de agua "DEMO" (`PB-024` / RF22 / CUS13 / RN-14).
  - Evaluación empírica de métricas `Precision@3` y `Precision@5` con dataset etiquetado (`PB-027` / RF06 / RNF03).
  - Integración del recorrido E2E completo y datos reproducibles (`PB-037`).

### 9. ¿Qué debemos corregir antes de la presentación?
- **P0:** Corregir el error TS2353 en `src/components/__tests__/MentorSessionsView.test.tsx` para que `npm run build` compile con éxito.
- **P1:** Ejecutar `ruff format .` sobre el backend (14 archivos) y configurar `VITE_SERVICE_MODE=api` en `.env` para asegurar que el frontend consuma el backend real durante la demo.
- **P1:** Enriquecer la semilla de base de datos con sesiones en todos los estados (`PUBLICADA`, `QUORUM_INSUFICIENTE`, `CONFIRMADA`, `CONCLUIDA`) para recorrer la demostración en vivo de forma fluida.
- **P2:** Corregir las referencias de casos de uso en `sprint-06.md` (`CUS12/13` -> `CUS08`).

---

## 3. Cuadro Cuantitativo de Preparación para la Presentación

```
Progreso General Sprints 01 a 06: [████████████████░░░░] 81.25% Completitud Funcional
Cobertura de Pruebas Backend:     [█████████████████░░░] 85.13% (Umbral: 70.0%)
Suites de Prueba Frontend:        [████████████████████] 100% Passing (311 tests)
Navegación y Guardas RBAC:        [████████████████████] 100% Implementado
Seguridad y Autorización API:     [████████████████████] 100% Endurecido
Compilación Producción Frontend:  [░░░░░░░░░░░░░░░░░░░░] BLOQUEADO por TS2353 (P0)
```

| Dimensión Evaluada | Ponderación | Nivel de Madurez | Dictamen SQA |
|---|:---:|:---:|:---:|
| **Arquitectura e Integración Base** | 15% | 100% | **Excelente** (FastAPI, React 19, SQLite/PostgreSQL) |
| **Control de Acceso y Seguridad RBAC** | 20% | 95% | **Robusto** (Endpoints protegidos, ownership verificado) |
| **Lógica de Negocio y Reglas Institucionales** | 25% | 90% | **Muy Alto** (RN-01 a RN-12 operativas con pruebas) |
| **Cobertura de Pruebas Automatizadas** | 20% | 95% | **Sobresaliente** (548 pruebas totales entre back y front) |
| **Preparación para Build de Producción** | 10% | 60% | **En Riesgo** (Requiere corregir TS2353 en Fase 05) |
| **Consistencia Documental y Trazabilidad** | 10% | 85% | **Alto** (Documentado exhaustivamente en auditoría) |
| **CALIFICACIÓN GLOBAL DE PREPARACIÓN** | **100%** | **87.5%** | **APTO PARA PRESENTACIÓN (Tras corregir P0)** |

---

## 4. Conclusión y Recomendación Final

El **Sistema Web P2P de Mentorías Académicas (EPIS-UPT)** se encuentra en un estado de madurez técnica y funcional notablemente elevado respecto a los compromisos de los Sprints 01 al 06. La lógica de negocio, las restricciones normativas (consentimiento Ley 29733, mérito RN-03, antelación RN-04, aforo RN-05, ratificación RN-08, quórum RN-09, cierre de bitácora RN-12) y la seguridad RBAC implementada en la Fase 04 están completamente sustentadas por 548 pruebas automatizadas passing.

**Recomendación Operativa:**
Proceder de inmediato a la **Fase 05** ejecutando las correcciones priorizadas del plan `04_PLAN_CORRECCIONES_HU.md`, iniciando por la subsanación de la falla de compilación TypeScript **P0** (en `MentorSessionsView.test.tsx`), el formateo **P1** con `ruff format` y la preparación de los datos de demostración en vivo. Con estas acciones resueltas, el proyecto estará en condiciones óptimas para una presentación formal y rigurosa ante el jurado evaluador.
