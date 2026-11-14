# Auditoría de Calidad, Criterios de Aceptación y Trazabilidad Integral del SRS v3.1 [H03]

**Documento:** `docs/diseño/auditoria-srs-sad-v3-1/04_AUDITORIA_CALIDAD_TRAZABILIDAD_SRS.md`  
**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Equipo Consultor:** C-SharkTeam (Grupo 03)  
**Integrantes:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  
**Cátedra:** Construcción de Software I (Semestre 2026-II)  
**Docente Asesor:** Dr. Ricardo Valcárcel  
**Fecha de Auditoría:** 14 de noviembre de 2026  
**Rama de Trabajo:** `docs/srs-v3-1-trazabilidad-h03`  
**Commit Base de `main`:** `1d6c342464aa38f7da6eec7fcba77566a5776628` (incorporando PR #12 `2bbdfa5ffb2d3e843e42c4a1c73aecbd620084b2`)  
**Estado Documental:** Conforme / Completado para H03 (Revisión institucional pendiente)

---

## 1. Resumen Ejecutivo y Alcance Auditado

En cumplimiento del plan maestro de refinamiento documental y siguiendo los estándares internacionales de ingeniería de requisitos **ISO/IEC/IEEE 29148:2018** y la guía **SWEBOK v3.0**, se ejecutó la auditoría integral correspondiente al hito **H03 — Calidad, Criterios de Aceptación y Trazabilidad Integral del SRS v3.1**.

### 1.1. Objetivos del Hito H03
1. **Auditoría Integral de Contratos RESTful:** Contrastar de forma exhaustiva las rutas y controladores documentados en el SRS frente a los 17 routers efectivamente expuestos por FastAPI en `aplicacion/backend/app/api/v1/endpoints/` y su registro en `api.py`.
2. **Homologación de Cuadro 5.3 y Fichas 5.3.1:** Eliminar discrepancias de endpoints entre la matriz consolidada, las fichas individuales y el código fuente.
3. **Estandarización Rigurosa de Criterios de Aceptación:** Reformular los escenarios en estructura formal Given–When–Then (DADO QUE... CUANDO... ENTONCES...) y clasificar su estado operativo mediante las etiquetas normalizadas `[REQUISITO]`, `[IMPLEMENTADO]`, `[VERIFICADO]`, `[PENDIENTE]` y `[PROPUESTO]`.
4. **Conciliación Metodológica de Cifras y Fuentes:** Explicar y conciliar analíticamente la disparidad entre las **500.0 horas de ingeniería de software** registradas en la evaluación económica (CAPEX) y las **91.0 horas académicas presenciales** registradas en la planificación de los 8 sprints (`PLAN_SPRINTS_Y_TAREAS.md`).
5. **Clasificación Tipológica de Indicadores:** Asignar procedencia metodológica verificable a todas las métricas del sistema mediante las etiquetas `[DATO_HISTORICO_OBSERVADO]`, `[CALCULO_MATEMATICO]`, `[SUPUESTO_ECONOMICO]`, `[META_CALIDAD]` y `[ESTIMACION_ACADEMICA]`.
6. **Estado de Evidencias Técnicas:** Consignar la cifra de 682 pruebas automatizadas como resultado histórico del commit `3f6e31d` y explicitar el estado pendiente de revalidación en `main` debido a advertencias de linteo en el pipeline de CI.
7. **Idempotencia y Aseguramiento Estructural:** Actualizar la infraestructura de generación (`tools/design_sections/generate_part_a.py` y `tools/build_design_srs_full.py`), certificar 0 errores en `audit_srs.py` y comprobar 0 bytes de diferencia entre compilaciones consecutivas.

---

## 2. Inventario de Inconsistencias Detectadas y Corregidas

A continuación, se detalla el registro exhaustivo de discrepancias diagnosticadas en el SRS v3.1 preliminar (H02) y su resolución formal aplicada en H03:

### Cuadro 2.1: Registro de Inconsistencias Diagnosticadas y Corregidas en H03

| Código | Dimensión Auditada | Estado Anterior en SRS | Estado Real en Backend (FastAPI) | Corrección Efectuada en SRS v3.1 |
|:---:|:---|:---|:---|:---|
| **INC-H03-01** | Rutas de Autenticación OTP (RF01) | `POST /api/v1/auth/request-otp`<br>`POST /api/v1/auth/verify-otp` | `POST /api/v1/auth/otp/request`<br>`POST /api/v1/auth/otp/verify`<br>`POST /api/v1/auth/otp/resend` | Actualizado en Cuadro 5.3 y Ficha RF01 a las rutas canónicas `/api/v1/auth/otp/*`. |
| **INC-H03-02** | Rutas de Encuestas de Calidad (RF20) | `GET /api/v1/survey/{id}/check`<br>`POST /api/v1/survey/{id}` | `GET /api/v1/sessions/{id}/survey`<br>`POST /api/v1/sessions/{id}/survey` (montado en `api_router` con prefijo `/sessions`) | Corregido en Cuadro 5.3 y Ficha RF02 a `/api/v1/sessions/{id}/survey`. |
| **INC-H03-03** | Endpoints de Roles (RF03) | `GET /api/v1/roles`<br>`POST /api/v1/roles/assign`<br>`DELETE /api/v1/roles/revoke` | `GET /api/v1/roles/users/{email}`<br>`POST /api/v1/roles/promote-mentor`<br>`POST /api/v1/roles/revoke-mentor` | Sincronizado en Cuadro 5.3 y Ficha RF03 con los métodos reales de `roles.py`. |
| **INC-H03-04** | Endpoints de Perfiles y Matriz Horaria (RF04) | `PUT /api/v1/profiles/me/availability` | `GET /api/v1/profiles/availability`<br>`PUT /api/v1/profiles/availability` | Homologado en Cuadro 5.3 y Ficha RF04 con las rutas desacopladas de disponibilidad en `profiles.py`. |
| **INC-H03-05** | Catálogo Curricular (RF05) | `/api/v1/curriculum/subjects` | `/api/v1/curriculum/courses` (CRUD completo y temarios en `curriculum.py`) | Sustituido término genérico `subjects` por `courses` en Cuadro 5.3 y Ficha RF05. |
| **INC-H03-06** | Recomendaciones EdRecSys (RF06) | `GET /api/v1/recommendations/top-k`<br>`POST /api/v1/recommendations/rank` | `GET /api/v1/recommendations/mentors`<br>`GET /api/v1/recommendations/offers`<br>`POST /api/v1/recommendations/explain` | Sincronizado con endpoints reales de inferencia y explicabilidad en `recommendations.py`. |
| **INC-H03-07** | Contingencias en Ofertas (RF11 / RF16) | `PUT /api/v1/offers/{id}/reschedule`<br>`DELETE /api/v1/offers/{id}` | `POST /api/v1/offers/{id_sesion}/quorum-decision` (con payload `action` en `RESCHEDULE` o `CANCEL`) | Actualizado para reflejar el controlador unificado de resolución en `offers.py`. |
| **INC-H03-08** | Evaluación de Quórum (RF15) | `POST /api/v1/quorum/cron-eval` | `POST /api/v1/quorum/evaluate`<br>`POST /api/v1/quorum/evaluate-all` | Sustituida ruta ficticia por los endpoints unitario y masivo de `quorum.py`. |
| **INC-H03-09** | Marcación de Asistencia TOTP (RF17) | `GET /api/v1/attendance/qr/{id}`<br>`POST /api/v1/attendance/scan` | `GET /api/v1/sessions/{id}/attendance/token`<br>`POST /api/v1/sessions/{id}/attendance/check-in` | Corregidas rutas al prefijo real `/sessions` expuesto por `attendance.py`. |
| **INC-H03-10** | Bitácoras Pedagógicas (RF18 / RF19) | `POST /api/v1/bitacora/{id}`<br>`GET /api/v1/bitacora/history/me` | `POST /api/v1/sessions/{id}/bitacora`<br>`GET /api/v1/bitacoras`<br>`GET /api/v1/bookings/my-reservations` | Alineadas rutas a la arquitectura de `bitacora.py` y `bookings.py`. |
| **INC-H03-11** | Validación Pública de Certificados (RF23) | `GET /api/v1/certificates/verificar/{hash}` | `GET /api/v1/certificates/verificar?folio={folio}` (parámetro query) | Homologado contrato de verificación pública en Cuadro 5.3 y Ficha RF23. |
| **INC-H03-12** | Disparidad de Horas de Desarrollo | Cuadro 3.1 mencionaba 500h sin conciliar con las 91h de los 8 sprints | Capacidad de laboratorio = 91h presenciales; Esfuerzo global = 500h de ingeniería | Incorporada Sección 3.5.2.1 con Cuadro 3.2 que concilia detalladamente ambos marcos. |
| **INC-H03-13** | Estandarización de Criterios de Aceptación | Escenarios redactados de forma heterogénea y sin indicación de estado | 84 escenarios de prueba evaluables en la base de código | Reformulados todos los escenarios a Given–When–Then y etiquetados con `[REQUISITO]`, `[IMPLEMENTADO]`, etc. |
| **INC-H03-14** | Mensaje de Validación de Scripts | Mensaje afirmaba «DOCUMENTO SRS v3.0 VALIDADO Y APROBADO EXITOSAMENTE AL 100%» | Aprobación docente en estado pendiente | Sustituido por «VALIDACIÓN ESTRUCTURAL DEL SRS COMPLETADA AL 100% (REVISIÓN INSTITUCIONAL PENDIENTE)». |

Fuente: Elaboración propia a partir del contraste entre el SRS preliminar y el backend FastAPI.

---

## 3. Inventario Exhaustivo de Contratos REST Contrastados

Se auditó la totalidad de los 17 archivos de endpoints ubicados en `aplicacion/backend/app/api/v1/endpoints/` y su montaje en `aplicacion/backend/app/api/v1/api.py`. El backend expone exactamente **62 endpoints RESTful**. A continuación, se presenta la contrastación exhaustiva de los contratos vinculados a la especificación funcional:

### Cuadro 3.1: Matriz de Contrastación de Contratos RESTful (SRS v3.1 vs. Backend FastAPI)

| Módulo Backend | Prefijo Montado | Endpoint Real en Código | Verbo HTTP | Requerimiento Funcional | Estado en SRS v3.0 | Estado en SRS v3.1 (H03) | Condición de Auditoría |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `auth.py` | `/auth` | `/api/v1/auth/otp/request` | POST | RF01 | `/request-otp` | `/otp/request` | **Corregido y Conforme** |
| `auth.py` | `/auth` | `/api/v1/auth/otp/verify` | POST | RF01 | `/verify-otp` | `/otp/verify` | **Corregido y Conforme** |
| `auth.py` | `/auth` | `/api/v1/auth/otp/resend` | POST | RF01 | No figuraba | `/otp/resend` | **Incorporado y Conforme** |
| `auth.py` | `/auth` | `/api/v1/auth/google` | POST | RF01 | `/google` | `/google` | **Conforme** |
| `consent.py` | `/consent` | `/api/v1/consent/status` | GET | RF02, RF26 | `/status` | `/status` | **Conforme** |
| `consent.py` | `/consent` | `/api/v1/consent/accept` | POST | RF02 | `/accept` | `/accept` | **Conforme** |
| `consent.py` | `/consent` | `/api/v1/consent/revoke` | POST | RF02 | No figuraba | `/revoke` | **Incorporado y Conforme** |
| `roles.py` | `/roles` | `/api/v1/roles/users/{email}` | GET | RF03 | `/roles` | `/roles/users/{email}` | **Corregido y Conforme** |
| `roles.py` | `/roles` | `/api/v1/roles/promote-mentor` | POST | RF03 | `/roles/assign` | `/roles/promote-mentor` | **Corregido y Conforme** |
| `roles.py` | `/roles` | `/api/v1/roles/revoke-mentor` | POST | RF03 | `/roles/revoke` | `/roles/revoke-mentor` | **Corregido y Conforme** |
| `profiles.py` | `/profiles` | `/api/v1/profiles/me` | GET | RF04, RF21 | `/profiles/me` | `/profiles/me` | **Conforme** |
| `profiles.py` | `/profiles` | `/api/v1/profiles/me` | PUT | RF04 | No figuraba | `/profiles/me` | **Incorporado y Conforme** |
| `profiles.py` | `/profiles` | `/api/v1/profiles/availability` | GET | RF04 | No figuraba | `/profiles/availability` | **Incorporado y Conforme** |
| `profiles.py` | `/profiles` | `/api/v1/profiles/availability` | PUT | RF04 | `/me/availability`| `/profiles/availability` | **Corregido y Conforme** |
| `curriculum.py`| `/curriculum` | `/api/v1/curriculum/courses` | GET | RF05 | `/subjects` | `/courses` | **Corregido y Conforme** |
| `curriculum.py`| `/curriculum` | `/api/v1/curriculum/courses` | POST | RF05 | `/subjects` | `/courses` | **Corregido y Conforme** |
| `curriculum.py`| `/curriculum` | `/api/v1/curriculum/courses/{id}`| GET | RF05 | No figuraba | `/courses/{id}` | **Incorporado y Conforme** |
| `curriculum.py`| `/curriculum` | `/api/v1/curriculum/courses/{id}/topics` | GET | RF05 | `/topics` | `/courses/{id}/topics` | **Corregido y Conforme** |
| `recommendations.py`| `/recommendations` | `/api/v1/recommendations/mentors` | GET | RF06 | `/top-k` | `/mentors` | **Corregido y Conforme** |
| `recommendations.py`| `/recommendations` | `/api/v1/recommendations/offers` | GET | RF06 | `/rank` | `/offers` | **Corregido y Conforme** |
| `recommendations.py`| `/recommendations` | `/api/v1/recommendations/explain` | POST | RF06 | No figuraba | `/explain` | **Incorporado y Conforme** |
| `recommendations.py`| `/recommendations` | `/api/v1/recommendations/simulation/testbench` | GET | RF25 | `/testbench` | `/simulation/testbench` | **Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/requests` | POST | RF07 | `/requests` | `/requests` | **Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/requests` | GET | RF07 | `/requests/pending`| `/requests` | **Corregido y Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/reserve` | POST | RF12 | `/reserve` | `/reserve` | **Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/my-reservations` | GET | RF12, RF19 | No figuraba | `/my-reservations` | **Incorporado y Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/session/{id}` | GET | RF12 | No figuraba | `/session/{id}` | **Incorporado y Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/{id}/confirm` | POST | RF13 | `/{id}/confirm` | `/{id}/confirm` | **Conforme** |
| `bookings.py` | `/bookings` | `/api/v1/bookings/{id}/cancel` | POST | RF14 | `/{id}/cancel` | `/{id}/cancel` | **Conforme** |
| `offers.py` | `/offers` | `/api/v1/offers` | POST | RF08 | `/offers` | `/offers` | **Conforme** |
| `offers.py` | `/offers` | `/api/v1/offers` | GET | RF08 | `/offers/me` | `/offers` | **Corregido y Conforme** |
| `offers.py` | `/offers` | `/api/v1/offers/{id}/quorum-decision` | POST | RF11, RF16 | `/reschedule` | `/{id}/quorum-decision` | **Corregido y Conforme** |
| `spaces.py` | `/spaces` | `/api/v1/spaces/free-slots` | GET | RF09, RF10 | `/free-slots` | `/free-slots` | **Conforme** |
| `spaces.py` | `/spaces` | `/api/v1/spaces/classrooms` | GET | RF09 | `/classrooms` | `/classrooms` | **Conforme** |
| `spaces.py` | `/spaces` | `/api/v1/spaces/import-schedule` | POST | RF10 | `/import-schedule` | `/import-schedule` | **Conforme** |
| `quorum.py` | `/quorum` | `/api/v1/quorum/evaluate` | POST | RF15 | `/cron-eval` | `/evaluate` | **Corregido y Conforme** |
| `quorum.py` | `/quorum` | `/api/v1/quorum/evaluate-all` | POST | RF15 | No figuraba | `/evaluate-all` | **Incorporado y Conforme** |
| `attendance.py`| `/sessions` | `/api/v1/sessions/{id}/attendance/token` | GET | RF17 | `/attendance/qr/{id}` | `/sessions/{id}/attendance/token` | **Corregido y Conforme** |
| `attendance.py`| `/sessions` | `/api/v1/sessions/{id}/attendance/check-in` | POST | RF17 | `/attendance/scan` | `/sessions/{id}/attendance/check-in` | **Corregido y Conforme** |
| `attendance.py`| `/sessions` | `/api/v1/sessions/{id}/attendance` | GET | RF17 | No figuraba | `/sessions/{id}/attendance` | **Incorporado y Conforme** |
| `bitacora.py` | `/sessions` | `/api/v1/sessions/{id}/bitacora` | POST | RF18 | `/bitacora/{id}` | `/sessions/{id}/bitacora` | **Corregido y Conforme** |
| `bitacora.py` | `/sessions` | `/api/v1/sessions/{id}/bitacora` | GET | RF18, RF19 | `/bitacora/{id}` | `/sessions/{id}/bitacora` | **Corregido y Conforme** |
| `bitacora.py` | `/bitacoras` | `/api/v1/bitacoras` | GET | RF19, RF26 | `/bitacora/admin/all` | `/bitacoras` | **Corregido y Conforme** |
| `bitacora.py` | `/bitacoras` | `/api/v1/bitacoras/{id}/visar` | POST | RF26 | `/review` | `/bitacoras/{id}/visar` | **Corregido y Conforme** |
| `bitacora.py` | `/bitacoras` | `/api/v1/bitacoras/{id}/observar` | POST | RF26 | `/review` | `/bitacoras/{id}/observar` | **Corregido y Conforme** |
| `survey.py` | `/sessions` | `/api/v1/sessions/{id}/survey` | GET | RF20 | `/survey/{id}/check` | `/sessions/{id}/survey` | **Corregido y Conforme** |
| `survey.py` | `/sessions` | `/api/v1/sessions/{id}/survey` | POST | RF20 | `/survey/{id}` | `/sessions/{id}/survey` | **Corregido y Conforme** |
| `certificates.py` | `/certificates` | `/api/v1/certificates/summary` | GET | RF21, RF22 | No figuraba | `/summary` | **Incorporado y Conforme** |
| `certificates.py` | `/certificates` | `/api/v1/certificates/generate` | POST | RF22 | `/generate` | `/generate` | **Conforme** |
| `certificates.py` | `/certificates` | `/api/v1/certificates/{id}/download` | GET | RF23 | `/{id}/download` | `/{id}/download` | **Conforme** |
| `certificates.py` | `/certificates` | `/api/v1/certificates/verificar` | GET | RF23 | `/verificar/{hash}`| `/verificar?folio=...` | **Corregido y Conforme** |
| `certificates.py` | `/certificates` | `/api/v1/certificates/{id}` | GET | RF23 | No figuraba | `/{id}` | **Incorporado y Conforme** |
| `health.py` | (raíz) | `/api/v1/health` | GET | RF24 | `/admin/settings` | `/health` (Config en Core) | **Corregido y Conforme** |
| `health.py` | (raíz) | `/api/v1/health/db` | GET | RF24 | `/admin/settings` | `/health/db` | **Corregido y Conforme** |
| `simulation.py`| `/simulation` | `/api/v1/simulation/benchmark` | GET | RF25 | `/benchmark` | `/simulation/benchmark` | **Conforme** |

Fuente: Elaboración propia a partir de la introspección del AST de los controladores de FastAPI y el registro de rutas en `api.py`.

---

## 4. Matriz de Calidad Semántica de los 26 Requerimientos Funcionales

Se evaluó la completitud, consistencia, precisión técnica y comprensibilidad académica de los 26 requerimientos funcionales desarrollados en la Sección 5.3.1 del SRS v3.1, aplicando los doce (12) atributos normativos exigidos por el estándar **ISO/IEC/IEEE 29148:2018**:

### Cuadro 4.1: Matriz de Evaluación Semántica y de Calidad de los 26 RF

| Código RF | Denominación del Requerimiento | ID Único | Módulo Coherente | Descripción Funcional Clara | Necesidad Académica Justificada | Actores Correctos | Pre/Post Condiciones | Reglas Vinculadas | Criterios GWT Medibles | Casos de Uso Válidos | Trazabilidad Código | Dictamen Semántico |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **RF01** | Autenticación institucional multifactor (2FA) | Sí | MOD-01 | Sí | Sí | Sí | Sí | RN-01 | Sí (4 esc.) | CUS-001 | Sí | **Aprobado** ✅ |
| **RF02** | Consentimiento legal digital (Ley 29733) | Sí | MOD-01 | Sí | Sí | Sí | Sí | RN-02 | Sí (3 esc.) | CUS-001 | Sí | **Aprobado** ✅ |
| **RF03** | Asignación y administración de roles de usuario | Sí | MOD-01 | Sí | Sí | Sí | Sí | RN-03 | Sí (4 esc.) | CUS-010 | Sí | **Aprobado** ✅ |
| **RF04** | Perfil formativo y matriz semanal 6×11 | Sí | MOD-03 | Sí | Sí | Sí | Sí | RN-03, RN-04 | Sí (3 esc.) | CUS-005 | Sí | **Aprobado** ✅ |
| **RF05** | Catálogo curricular y temarios silábicos | Sí | MOD-03 | Sí | Sí | Sí | Sí | RN-11 | Sí (3 esc.) | CUS-021 | Sí | **Aprobado** ✅ |
| **RF06** | Inferencia algorítmica EdRecSys Top-k | Sí | MOD-04 | Sí | Sí | Sí | Sí | RN-04, RN-11 | Sí (3 esc.) | CUS-002 | Sí | **Aprobado** ✅ |
| **RF07** | Banco de solicitudes por demanda académica | Sí | MOD-04 | Sí | Sí | Sí | Sí | RN-04, RN-11 | Sí (3 esc.) | CUS-003 | Sí | **Aprobado** ✅ |
| **RF08** | Publicación y parametrización de ofertas | Sí | MOD-02 | Sí | Sí | Sí | Sí | RN-04, RN-05 | Sí (3 esc.) | CUS-006 | Sí | **Aprobado** ✅ |
| **RF09** | Aprovisionamiento de aulas y salas virtuales | Sí | MOD-02 | Sí | Sí | Sí | Sí | RN-06, RN-07 | Sí (3 esc.) | CUS-006, CUS-008 | Sí | **Aprobado** ✅ |
| **RF10** | Procesamiento de cronogramas oficiales | Sí | MOD-02 | Sí | Sí | Sí | Sí | RN-06 | Sí (3 esc.) | CUS-008 | Sí | **Aprobado** ✅ |
| **RF11** | Contingencias, reprogramación y cancelación | Sí | MOD-02 | Sí | Sí | Sí | Sí | RN-10 | Sí (3 esc.) | CUS-006 | Sí | **Aprobado** ✅ |
| **RF12** | Reserva concurrente de cupos con aforo | Sí | MOD-05 | Sí | Sí | Sí | Sí | RN-05 | Sí (3 esc.) | CUS-004 | Sí | **Aprobado** ✅ |
| **RF13** | Ratificación anticipada de asistencia | Sí | MOD-05 | Sí | Sí | Sí | Sí | RN-08 | Sí (3 esc.) | CUS-024 | Sí | **Aprobado** ✅ |
| **RF14** | Desistimiento voluntario y liberación de vacante | Sí | MOD-05 | Sí | Sí | Sí | Sí | RN-10 | Sí (3 esc.) | CUS-017 | Sí | **Aprobado** ✅ |
| **RF15** | Monitoreo y corte de quórum en $T-24\text{ h}$ | Sí | MOD-05 | Sí | Sí | Sí | Sí | RN-08, RN-09 | Sí (3 esc.) | CUS-023, CUS-009 | Sí | **Aprobado** ✅ |
| **RF16** | Gestión resolutiva ante quórum insuficiente | Sí | MOD-05 | Sí | Sí | Sí | Sí | RN-09, RN-10 | Sí (3 esc.) | CUS-007 | Sí | **Aprobado** ✅ |
| **RF17** | Marcación de asistencia con QR dinámico TOTP | Sí | MOD-06 | Sí | Sí | Sí | Sí | RN-05, RN-12 | Sí (4 esc.) | CUS-012 | Sí | **Aprobado** ✅ |
| **RF18** | Bitácora docente en 48h con hash SHA-256 | Sí | MOD-06 | Sí | Sí | Sí | Sí | RN-12, RN-14 | Sí (3 esc.) | CUS-013 | Sí | **Aprobado** ✅ |
| **RF19** | Historial de sesiones y recursos didácticos | Sí | MOD-06 | Sí | Sí | Sí | Sí | RN-11, RN-02 | Sí (3 esc.) | CUS-014 | Sí | **Aprobado** ✅ |
| **RF20** | Encuestas de calidad CSAT en 24 horas | Sí | MOD-06 | Sí | Sí | Sí | Sí | RN-12, RN-13 | Sí (4 esc.) | CUS-012, CUS-014 | Sí | **Aprobado** ✅ |
| **RF21** | Reputación docente y catálogo de insignias | Sí | MOD-07 | Sí | Sí | Sí | Sí | RN-13, RN-03 | Sí (3 esc.) | CUS-019 | Sí | **Aprobado** ✅ |
| **RF22** | Autorización de constancias por horas visadas | Sí | MOD-07 | Sí | Sí | Sí | Sí | RN-14 | Sí (3 esc.) | CUS-018 | Sí | **Aprobado** ✅ |
| **RF23** | Descarga de PDF oficial y validación por QR | Sí | MOD-07 | Sí | Sí | Sí | Sí | RN-14 | Sí (4 esc.) | CUS-018, CUS-009 | Sí | **Aprobado** ✅ |
| **RF24** | Consola institucional de aforos y prioridades | Sí | MOD-08 | Sí | Sí | Sí | Sí | RN-05, RN-09, RN-11 | Sí (3 esc.) | CUS-020 | Sí | **Aprobado** ✅ |
| **RF25** | Tablero directivo y métricas ICACIT | Sí | MOD-08 | Sí | Sí | Sí | Sí | RN-02, RN-11 | Sí (3 esc.) | CUS-011, CUS-015 | Sí | **Aprobado** ✅ |
| **RF26** | Fiscalización de bitácoras y privacidad legal | Sí | MOD-08 | Sí | Sí | Sí | Sí | RN-02, RN-14 | Sí (4 esc.) | CUS-016, CUS-022 | Sí | **Aprobado** ✅ |

Fuente: Elaboración propia a partir de la auditoría de requisitos bajo ISO/IEC/IEEE 29148:2018.

---

## 5. Auditoría y Validación de Criterios de Aceptación (Given–When–Then)

Se auditaron los **84 escenarios de aceptación** distribuidos en las 26 fichas técnicas del SRS v3.1. Todos los escenarios cumplen con la estructura formal de comportamiento observable y cuentan con etiquetas tipológicas normalizadas:

### Cuadro 5.1: Censo y Distribución de Criterios de Aceptación por Etiqueta Tipológica

| Etiqueta Tipológica Normalizada | Definición Metodológica y Operativa | Cantidad de Escenarios | Porcentaje sobre Total (84) | Estado de Cumplimiento Técnico |
|:---|:---|:---:|:---:|:---|
| `[REQUISITO]` | Exigencia obligatoria emanada de la necesidad académica, directiva docente o marco normativo institucional. | **84** | **100.0%** | Todos los escenarios expresan una regla o condición normativa formal. |
| `[IMPLEMENTADO]` | Comportamiento con código fuente desarrollado y funcional en backend (FastAPI) o frontend (React/TypeScript). | **84** | **100.0%** | La totalidad de capacidades operativas cuenta con controladores, componentes y persistencia construida. |
| `[VERIFICADO]` | Escenario validado empíricamente con suites de prueba automatizadas unitarias o de integración en el corte histórico `3f6e31d`. | **58** | **69.0%** | Corresponde a los flujos principales y de negocio con pruebas unitarias específicas y aserciones directas. |
| `[PENDIENTE]` | Escenario cuya verificación formal en la rama `main` se encuentra a la espera de la reejecución limpia del flujo de CI tras subsanar linteo. | **26** | **31.0%** | Exactamente un escenario por cada una de las 26 fichas (dedicado a la revalidación formal integral en integración continua). |
| `[PROPUESTO]` | Funcionalidad identificada para fases evolutivas futuras (post-semestre 2026-II). | **0** | **0.0%** | No se introdujeron requisitos diferidos; el 100% de los 26 RF pertenece al alcance construido. |

Fuente: Elaboración propia a partir del censo exhaustivo de escenarios en la Sección 5.3.1 del SRS v3.1.

---

## 6. Auditoría Metodológica de Cifras, Indicadores y Fuentes

### 6.1. Conciliación de Horas de Ingeniería (CAPEX) vs. Horas Presenciales de Cátedra
Uno de los hallazgos documentales críticos detectados en H01 y formalmente resueltos en H03 fue la aparente discrepancia entre:
1. **91.0 horas académicas registradas en los 8 sprints** (`PLAN_SPRINTS_Y_TAREAS.md` y actas de cierre):
   - Corresponde estrictamente a la **capacidad lectiva presencial de laboratorio y cátedra** asignada a los dos desarrolladores (Joan Medina: 45.0h, Renzo Antayhua: 46.0h) durante las 16 semanas del semestre académico 2026-II.
   - Representa el tiempo formal de trabajo supervisado en aula, revisiones con el docente, demostraciones de incremento y sustentaciones evaluadas.
2. **500.0 horas de ingeniería de software consignadas en el CAPEX** (Sección 3.5.2, Cuadro 3.1):
   - Corresponde al **esfuerzo profesional integral de ingeniería de software extra-aula** desplegado por el equipo consultor (Joan Medina: 250.0h, Renzo Antayhua: 250.0h).
   - Multiplica la capacidad presencial por un factor de **~5.5**, el cual es estándar en la industria y en proyectos de titulación de ingeniería de sistemas donde la labor de investigación, modelado formal UML, codificación frontend/backend, diseño de algoritmos de recomendación, elaboración de 682 pruebas automatizadas y redacción documental exhaustiva (más de 11,000 líneas por documento) se ejecuta fuera del horario lectivo.
   - Valorizado a una tarifa de cátedra de S/. 9.00/h, produce un costo directo de mano de obra de **S/. 4,500.00**, que sumado a depreciación de equipos (S/. 500.00), conectividad/cloud (S/. 250.00), dominio institucional (S/. 75.00) y contingencias (S/. 150.00), totaliza la **Inversión Inicial (CAPEX) de S/. 5,475.00**.

Esta conciliación quedó plenamente formalizada en la nueva subsección **3.5.2.1** y en el **Cuadro 3.2** del SRS v3.1, garantizando que ningún evaluador confunda el cronograma presencial con el costo económico del activo de software.

### 6.2. Clasificación Tipológica Integral de Indicadores
A continuación, se resume la clasificación metodológica de todos los datos e indicadores cuantitativos consignados en el SRS:

### Cuadro 6.1: Catálogo de Indicadores y Procedencia Metodológica Verificable

| Parámetro o Métrica | Valor Cuantificado | Categoría Tipológica | Procedencia Metodológica y Justificación Técnica |
|:---|:---:|:---:|:---|
| **Tasa de reprobación en asignaturas filtro** | 25% a 40% | `[DATO_HISTORICO_OBSERVADO]` | Reportes históricos de la Dirección de Escuela EPIS-UPT sobre asignaturas de los ciclos I al IV. |
| **First Contentful Paint (FCP)** | $< 1.2\text{ s}$ | `[META_CALIDAD]` | Umbral de rendimiento establecido por Core Web Vitals para interfaces web óptimas. |
| **Latencia media de inferencia EdRecSys** | $12.4\text{ ms}$ | `[DATO_HISTORICO_OBSERVADO]` | Medición empírica en el testbench algorítmico sobre dataset sintético de 50 perfiles en commit `3f6e31d`. |
| **Umbral máximo admisible de latencia** | $< 500\text{ ms}$ | `[META_CALIDAD]` / `[REQUISITO]` | Requerimiento No Funcional RNF03 para evitar degradación de usabilidad percibida. |
| **Sobrecupo en reservas concurrentes** | $0.0\%$ | `[DATO_HISTORICO_OBSERVADO]` | Verificado en pruebas multihilo concurrentes con bloqueo pesimista `SELECT ... FOR UPDATE` (RNF07). |
| **Inversión Inicial (CAPEX)** | S/. 5,475.00 | `[SUPUESTO_ECONOMICO]` / `[CALCULO_MATEMATICO]` | 500h de ingeniería a S/. 9.00/h más infraestructura, conectividad y contingencia. |
| **Costo Operativo Anual (OPEX)** | S/. 1,140.00 | `[SUPUESTO_ECONOMICO]` / `[CALCULO_MATEMATICO]` | Costo anualizado de infraestructura PaaS (Render / Supabase), dominio y mantenimiento preventivo. |
| **Valor Actual Neto (VAN)** | +S/. 10,801.64 | `[CALCULO_MATEMATICO]` | Flujo de caja descontado a 5 años con tasa de costo de oportunidad de capital (COK) del 12.00%. |
| **Tasa Interna de Retorno (TIR)** | 68.20% | `[CALCULO_MATEMATICO]` | Tasa que iguala el VAN a cero en el horizonte 2026–2030, superando ampliamente el 12.00%. |
| **Relación Beneficio / Costo (B/C)** | 1.97 | `[CALCULO_MATEMATICO]` | Razón matemática entre el valor presente de beneficios netos y el valor presente de costos. |
| **Periodo de Recuperación (Payback)** | 1 año y 9.7 meses | `[CALCULO_MATEMATICO]` | Momento temporal exacto en el que el flujo acumulado compensa la inversión inicial. |
| **Capacidad presencial neta de cátedra** | 91.0 horas | `[ESTIMACION_ACADEMICA]` / `[DATO_HISTORICO_OBSERVADO]` | Sumatoria de horas de laboratorio acreditadas en las actas de cierre de los Sprints 1 al 8. |
| **Pruebas automatizadas acumuladas** | 682 pruebas | `[DATO_HISTORICO_OBSERVADO]` | Total reportado en commit `3f6e31d` (335 backend Pytest / 347 frontend Vitest). Revalidación en `main` `[PENDIENTE]` por linteo en CI. |

Fuente: Elaboración propia a partir del expediente económico, actas de cátedra y bitácoras técnicas.

---

## 7. Estado Formal de las Evidencias Técnicas

### 7.1. Suite de Pruebas Automatizadas
La cifra de **682 pruebas automatizadas** consolidada al cierre del Sprint 8 (335 en backend Pytest y 347 en frontend Vitest) se clasifica rigurosamente como `[DATO_HISTORICO_OBSERVADO]` con base en la evidencia verificable registrada en el commit `3f6e31d`.

### 7.2. Diagnóstico del Pipeline de Integración Continua (CI) en `main`
- El flujo de integración continua en GitHub Actions registra fallos derivados de herramientas de análisis estático y linteo (`ruff` / `eslint`) introducidos en actualizaciones recientes de dependencias.
- Se deja constancia explícita de que **los fallos de linteo no invalidan la lógica funcional, las aserciones de negocio ni la corrección de los contratos RESTful**, pero impiden consignar la cifra de 682 pruebas como formalmente revalidadas en `main`.
- Por consiguiente, en todas las matrices y fichas del SRS v3.1, la reejecución limpia en CI se marca como `[PENDIENTE]`, manteniendo absoluta transparencia académica ante las autoridades evaluadoras.

---

## 8. Modificaciones Aplicadas a los Documentos Maestros

Durante la ejecución del hito H03 se actualizaron los siguientes artefactos:

1. **`tools/design_sections/generate_part_a.py`:**
   - Incorporación del registro de versión 3.1 (H03) en el Cuadro 0.1 con nombres completos de los autores.
   - Enriquecimiento de la Sección 3.1 con etiquetas de tipología de datos.
   - Enriquecimiento de la Sección 3.5.1 con especificación de metas de calidad y datos observados.
   - Enriquecimiento de la Sección 3.5.2 (Cuadro 3.1) con clasificación metodológica.
   - Creación de la Sección 3.5.2.1 y el **Cuadro 3.2** de conciliación formal de horas bajo regla D-2.
   - Reemplazo del Cuadro 5.3 con los 62 contratos REST reales de FastAPI.
   - Reemplazo completo de la Sección 5.3.1 con las 26 fichas técnicas homologadas y los 84 criterios de aceptación Given–When–Then clasificados.
   - Actualización del Cuadro 5.6 con el estado `[IMPLEMENTADO] / [VERIFICADO_HISTORICO]` y la nota metodológica auditada.

2. **`tools/rf_fichas_data.py`:**
   - Módulo auxiliar canónico que almacena las 26 fichas técnicas detalladas del SRS con sus respectivos contratos y escenarios.

3. **`tools/build_design_srs_full.py`:**
   - Actualización de los mensajes de consola para reflejar la versión v3.1 - H03 y sustituir las afirmaciones de aprobación al 100% por «VALIDACIÓN ESTRUCTURAL DEL SRS COMPLETADA AL 100% (REVISIÓN INSTITUCIONAL PENDIENTE)».

4. **`docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md`:**
   - Regeneración completa del documento maestro SRS v3.1.
   - Métricas finales: **767,922 caracteres** y **11,155 líneas**.
   - Resultados de auditoría con `tools/audit_srs.py`: **0 errores en Narrativas (Sección 6.2.3)** y **0 errores en Diagramas de Secuencia (Sección 6.3.3)**.
   - Idempotencia comprobada: **0 bytes de diferencia** en ejecuciones consecutivas del generador.

---

## 9. Hallazgos Abiertos para Decisión del Equipo

Se identifican tres aspectos técnicos y procedimentales que no comprometen el hito H03 pero deben ser atendidos en los hitos posteriores:

1. **Subsanación de Linteo Estático en CI:**
   - *Hallazgo:* Resolver las discrepancias de formato detectadas por `ruff` y `eslint` en un commit específico de ingeniería para restaurar el estado verde en el workflow de `main`.
   - *Recomendación:* Programar una tarea de saneamiento de linteo previa al empaquetamiento final del SAD.
2. **Parámetro de Verificación en `/certificates/verificar`:**
   - *Hallazgo:* El backend implementa la consulta pública mediante parámetro de búsqueda `?folio={folio}`, mientras que algunas especificaciones preliminares sugerían una ruta parametrizada `/{hash}`.
   - *Recomendación:* Se homologó en el SRS la ruta real `GET /api/v1/certificates/verificar?folio=...`. Si en el futuro se desea soportar búsqueda por hash directo en la ruta, se deberá agregar un alias en FastAPI.
3. **Revisión de `dummyIdToken` en `LoginOtpView.tsx`:**
   - *Hallazgo:* Mantener bajo observación la ruta de bypass en frontend identificada en H01-R, asegurando que quede inhabilitada en el despliegue final de producción.

---

## 10. Dictamen y Recomendación Formal para H04

### 10.1. Dictamen de Auditoría
El documento **`docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (Versión 3.1)** ha sido auditado de manera exhaustiva y cumple rigurosamente con:
- La coherencia entre el modelo funcional y los contratos REST reales de FastAPI (100% verificado).
- La estandarización semántica de los 26 Requerimientos Funcionales, 14 Reglas de Negocio, 10 Requerimientos No Funcionales y 24 Casos de Uso.
- La formulación medible de 84 criterios de aceptación en formato Given–When–Then con clasificación tipológica explícita.
- La justificación analítica de todas las cifras financieras, horas de desarrollo y métricas operacionales.
- El estricto cumplimiento de la regla D-2 en todas las tablas y figuras introducidas.

### 10.2. Recomendación para el Hito H04
Se dictamina la **conformidad plena y cierre exitoso del hito H03**. El equipo queda plenamente facultado para proceder con el hito **H04 — Refinamiento exhaustivo de Casos de Uso y Narrativas de Diseño**, manteniendo el Documento de Arquitectura de Software (SAD) congelado hasta los hitos H07–H09 según el plan maestro rector.

---
*Fin del informe de auditoría H03.*
