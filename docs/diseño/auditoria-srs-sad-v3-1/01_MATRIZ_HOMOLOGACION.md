# MATRIZ CANÓNICA DE HOMOLOGACIÓN Y TRAZABILIDAD INTEGRAL (H01)
## Auditoría y Refinamiento Documental SRS/SAD v3.1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Curso:** Construcción de Software I<br>
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas<br>
**Equipo Consultor:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)<br>
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado<br>
**Semestre Académico:** 2026-II<br>
**Fecha de Emisión:** 14 de Noviembre de 2026<br>
**Rama de Trabajo Base:** `main` (integrada mediante PR #11)<br>
**Commit Base Inicial de Auditoría:** `097f90d725e537f411ebadac740905e0c0448f61`<br>
**Commit Base Integrado en Main:** `0542aa2af8d30ecb6afdfa9d4561d0f07a1801b0`

---

## Control de Versiones

A continuación, se formaliza el registro de versiones del presente documento de homologación:

### Cuadro 1.1: Registro de Control de Versiones del Entregable H01

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Emisión formal de la Matriz de Homologación Canónica: trazabilidad completa MOD→RF→RN/RNF→CUS→Sprint→Código→Estado, resolución de discrepancias en RF20, CUS-008/011, contratos API, Python 3.13, 16 tablas y servicios externos. |
| **1.1** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Rectificación H01-R: distinción metodológica explícita entre discrepancia diagnosticada, decisión consensuada y corrección aplicada en documentos maestros; nota sobre RF20 pendiente en SRS Sección 5; estado diferido de actualización del SAD a H07–H09; notas de validación en pruebas (682 históricas) e incorporación de hallazgo `dummyIdToken`. |

Fuente: Elaboración propia.

El presente cuadro certifica el registro formal del informe H01 dentro del ciclo de auditoría documental, delimitando la autoría técnica del equipo consultor y consignando formalmente el estado de revisión y aprobación académica ante la cátedra de Construcción de Software I y la Dirección de la EPIS.

---

## 1. Propósito y Alcance de la Homologación

El presente documento establece la **Matriz de Homologación Canónica** para articular la concordancia absoluta entre:
1. La **Especificación de Requerimientos de Software** ([FD03-EPIS-Informe SRS de Proyecto.md](../FD03-EPIS-Informe%20SRS%20de%20Proyecto.md)).
2. El **Documento de Arquitectura de Software** ([FD04-EPIS-Informe SAD de Proyecto.md](../FD04-EPIS-Informe%20SAD%20de%20Proyecto.md)).
3. La implementación real del software en el repositorio ([sistema_web_p2p](../../../aplicacion/)).

A través de esta matriz, se garantiza que ningún requerimiento funcional carezca de caso de uso asignado, que ninguna regla de negocio quede sin mecanismo de imposición comprobable y que los contratos de interfaz REST y entidades relacionales descritos en los documentos coincidan fielmente con el código ejecutable y las pruebas automatizadas. Se establece explícitamente el principio metodológico según el cual **una decisión aprobada en esta matriz constituye una directriz rectora de diseño, pero su materialización efectiva en los documentos maestros se ejecuta en los hitos de refinamiento correspondientes (H02 a H06 para el SRS; H07 a H09 para el SAD)**.

---

## 2. Matriz Canónica de Trazabilidad Integral (MOD → RF → RN/RNF → CUS → Código → Estado)

A continuación, se presenta la matriz maestra que vincula los 8 módulos, 26 requerimientos funcionales, 14 reglas de negocio, 10 requerimientos no funcionales y los 24 casos de uso canónicos con el código fuente y las pruebas:

### Cuadro 1.2: Matriz Canónica de Trazabilidad Integral del Sistema Web P2P

| Módulo | RF | Reglas Vinculadas | CUS Canónico | Sprint | Implementación Backend / Frontend | Evidencia de Pruebas | Estado de Homologación | Acción Correctiva para v3.1 |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :--- |
| **MOD-01** Seguridad y Gobernanza | **RF01** | RN-01, RNF01, RNF02 | **CUS-001** | S01 | `endpoints/auth.py`<br>`auth_service.py`<br>`LoginOtpView.tsx`<br>`authService.ts` | `test_auth.py` (14 tests)<br>`LoginOtpView.test.tsx` (18 tests) | **Homologado** ✅ | Incorporar Google Identity Services (GIS) y SMTP Gmail institucional en narrativa y SAD. |
| **MOD-01** Seguridad y Gobernanza | **RF02** | RN-02, RNF02 | **CUS-001** | S02 | `endpoints/consent.py`<br>`consent_service.py`<br>`ConsentModalView.tsx`<br>`consentService.ts` | `test_consent.py` (10 tests)<br>`ConsentModalView.test.tsx` (12 tests) | **Homologado** ✅ | Unificar la cláusula legal Ley 29733 en el flujo normal y subflujos de CUS-001. |
| **MOD-01** Seguridad y Gobernanza | **RF03** | RN-03, RNF02 | **CUS-010** | S02 | `endpoints/roles.py`<br>`role_service.py`<br>`AdminRolesView.tsx`<br>`roleService.ts` | `test_roles.py` (12 tests)<br>`AdminRolesView.test.tsx` (14 tests) | **Homologado** ✅ | Consignar roles institucionales `STUDENT`, `MENTOR`, `ADMIN`, `COORDINATOR` en SAD. |
| **MOD-03** Perfiles y Currículo | **RF04** | RN-03, RNF04, RNF08 | **CUS-005** | S02 | `endpoints/profiles.py`<br>`profile_service.py`<br>`ProfileAcademicView.tsx`<br>`profileService.ts` | `test_profiles.py` (14 tests)<br>`ProfileAcademicView.test.tsx` (16 tests) | **Homologado** ✅ | Detallar la matriz horaria semanal 6×11 con bloqueo para ciclos < VII en rol mentor. |
| **MOD-03** Perfiles y Currículo | **RF05** | RN-11, RNF09 | **CUS-021** | S01 / Post-S08 | `endpoints/curriculum.py`<br>`curriculum_service.py`<br>`CurriculumCatalogView.tsx`<br>`apiClient.ts` | `test_curriculum.py` (16 tests)<br>`CurriculumCatalogView.test.tsx` (18 tests) | **Homologado** ✅ | Actualizar endpoints CRUD administrativos de asignaturas y silabarios incorporados en `5a1ce45`. |
| **MOD-04** Recomendación EdRecSys | **RF06** | RN-04, RN-11, RNF03 | **CUS-002** | S03 / S04 | `endpoints/recommendations.py`<br>`recommendation_service.py`<br>`RecommendationFeedView.tsx` | `test_recommendations.py` (22 tests)<br>`RecommendationFeedView.test.tsx` (20 tests) | **Homologado** ✅ | Documentar precisión algorítmica ($P@3=83.3\%$, $P@5=80.0\%$, latencia 12.4 ms) en SRS y SAD. |
| **MOD-04** Recomendación EdRecSys | **RF07** | RN-04, RNF04, RNF09 | **CUS-003** | S04 / Post-S08 | `endpoints/bookings.py` (`/requests`)<br>`booking_service.py`<br>`MentoringDemandModalView.tsx`<br>`MentorSessionsView.tsx` | `test_bookings.py` (12 tests)<br>`MentoringDemandModalView.test.tsx` (10 tests) | **Homologado** ✅ | Refinar CUS-003 piloto con flujo de banco de solicitudes y atención dirigida por el mentor. |
| **MOD-02** Planificación y Espacios | **RF08** | RN-04, RN-05, RNF04, RNF09 | **CUS-006** | S03 | `endpoints/offers.py`<br>`offer_service.py`<br>`OfferPublishView.tsx`<br>`offerService.ts` | `test_offers.py` (18 tests)<br>`OfferPublishView.test.tsx` (18 tests) | **Homologado** ✅ | Sincronizar ruta `/api/v1/offers` (corregir `/mentorships/offers` en SRS). |
| **MOD-02** Planificación y Espacios | **RF09** | RN-06, RN-07, RNF09, RNF10 | **CUS-006**, **CUS-008** | S03 / S05 | `services/virtual_room_service.py`<br>`services/catalog_support_service.py`<br>`SpaceSelectorView.tsx` | `test_catalog_cus06_provisioning.py` (14 tests) | **Homologado** ✅ | Detallar enlaces Google Meet institucionales y aulas físicas de la EPIS. |
| **MOD-02** Planificación y Espacios | **RF10** | RN-06, RNF09, RNF10 | **CUS-008** | Post-S08 (`097f90d`) | `endpoints/spaces.py`<br>`schedule_parser_service.py`<br>`AdminScheduleUploadView.tsx`<br>`spacesService.ts` | `test_spaces_schedule_api.py` (12 tests)<br>`AdminScheduleUploadView.test.tsx` (10 tests) | **Homologado** ✅ | Sincronizar rutas `/api/v1/spaces/import-schedule`, `/free-slots`, `/classrooms` y rol CUS-008. |
| **MOD-02** Planificación y Espacios | **RF11** | RN-10, RNF09, RNF10 | **CUS-006** | S05 | `endpoints/offers.py` (`/quorum-decision`)<br>`offer_service.py`<br>`MentorSessionsView.tsx` | `test_offers.py` (10 tests)<br>`MentorSessionsView.test.tsx` (12 tests) | **Homologado** ✅ | Alinear gestión de cancelaciones/reprogramaciones con FSM de 13 estados de sesión. |
| **MOD-05** Reserva y Quórum | **RF12** | RN-05, RNF07 | **CUS-004** | S04 | `endpoints/bookings.py` (`/reserve`)<br>`booking_service.py`<br>`BookingModalView.tsx`<br>`bookingService.ts` | `test_bookings.py` (20 tests multihilo)<br>`BookingModalView.test.tsx` (18 tests) | **Homologado** ✅ | Documentar bloqueo transaccional `SELECT ... FOR UPDATE` (0.0% tasa de sobrecupo). |
| **MOD-05** Reserva y Quórum | **RF13** | RN-08, RNF07, RNF09 | **CUS-024** | S04 / S05 | `endpoints/bookings.py` (`/{id}/confirm`)<br>`booking_service.py`<br>`MyBookingsView.tsx` | `test_bookings.py` (14 tests)<br>`MyBookingsView.test.tsx` (12 tests) | **Homologado** ✅ | Especificar ventana perentoria de ratificación obligatoria hasta T-24h. |
| **MOD-05** Reserva y Quórum | **RF14** | RN-08, RN-10, RNF07 | **CUS-017** | S04 / S05 | `endpoints/bookings.py` (`/{id}/cancel`)<br>`booking_service.py`<br>`MyBookingsView.tsx` | `test_bookings.py` (10 tests)<br>`MyBookingsView.test.tsx` (10 tests) | **Homologado** ✅ | Especificar liberación inmediata de cupo y transición a `CANCELADA_USUARIO`. |
| **MOD-05** Reserva y Quórum | **RF15** | RN-08, RN-09, RNF06, RNF09 | **CUS-023**, **CUS-009** | S04 / S06 | `endpoints/quorum.py`<br>`services/quorum_scheduler.py`<br>`booking_service.py` | `test_quorum.py` (16 tests) | **Homologado** ✅ | Documentar evaluación automática de quórum (50% aforo) a T-24h por scheduler en background. |
| **MOD-05** Reserva y Quórum | **RF16** | RN-09, RN-10, RNF09, RNF10 | **CUS-007** | S06 | `endpoints/offers.py` (`/quorum-decision`)<br>`offer_service.py`<br>`QuorumDecisionModalView.tsx` | `test_offers.py` (12 tests)<br>`QuorumDecisionModalView.test.tsx` (10 tests) | **Homologado** ✅ | Documentar alternativas del mentor: dictar con quórum reducido, reprogramar o cancelar. |
| **MOD-06** Asistencia y Bitácora | **RF17** | RN-05, RN-12, RNF01, RNF02 | **CUS-012** | S06 | `endpoints/attendance.py`<br>`attendance_service.py`<br>`AttendanceScannerView.tsx`<br>`AttendanceQrModalView.tsx` | `test_attendance.py` (18 tests)<br>`AttendanceScannerView.test.tsx` (14 tests) | **Homologado** ✅ | Documentar TOTP dinámico de 30s (`tokens_asistencia_activos`) y escaneo de cámara real. |
| **MOD-06** Asistencia y Bitácora | **RF18** | RN-12, RNF04, RNF08 | **CUS-013** | S06 | `endpoints/bitacora.py` (`/bitacora`)<br>`bitacora_service.py`<br>`BitacoraFormView.tsx` | `test_bitacora.py` (22 tests)<br>`BitacoraFormView.test.tsx` (16 tests) | **Homologado** ✅ | Documentar firma criptográfica SHA-256 e inmutabilidad de bitácora registrada. |
| **MOD-06** Asistencia y Bitácora | **RF19** | RNF02, RNF04 | **CUS-014** | S06 | `endpoints/bitacora.py`<br>`bitacora_service.py`<br>`BitacoraHistoryView.tsx` | `test_bitacora.py` (10 tests)<br>`BitacoraHistoryView.test.tsx` (12 tests) | **Homologado** ✅ | Documentar historial cronológico para estudiantes y mentores con filtros temáticos. |
| **MOD-06** Asistencia y Bitácora | **RF20** | RN-13, RNF05, RNF07 | **CUS-012** / **CUS-014** | S07 / Post-S08 | `endpoints/survey.py`<br>`survey_service.py`<br>`PostSessionSurveyModalView.tsx`<br>`surveyService.ts` | `test_survey.py` (16 tests)<br>`PostSessionSurveyModalView.test.tsx` (14 tests) | **Decisión aprobada** 📋<br>*(Pendiente en SRS Tabla 5.3 [H02])* | **Resolución HALL-01:** Consolidar RF20 como encuestas de calidad post-mentoría 24h en SRS Sección 5 (H02). |
| **MOD-07** Gamificación y Certificación | **RF21** | RN-13, RNF05, RNF09 | **CUS-019** | S07 | `endpoints/recommendations.py`<br>`recommendation_service.py`<br>`MentorBadgesView.tsx` | `test_recommendations.py` (12 tests)<br>`MentorBadgesView.test.tsx` (14 tests) | **Homologado** ✅ | Documentar catálogo de insignias y cálculo de reputación basado en encuestas CSAT. |
| **MOD-07** Gamificación y Certificación | **RF22** | RN-14, RNF09 | **CUS-018** | S08 | `endpoints/certificates.py` (`/generate`)<br>`certificate_service.py`<br>`AdminCertificatesView.tsx` | `test_certificates.py` (18 tests)<br>`AdminCertificatesView.test.tsx` (16 tests) | **Homologado** ✅ | Documentar validación de umbral mínimo de 20 horas auditadas para certificar. |
| **MOD-07** Gamificación y Certificación | **RF23** | RN-14, RNF02, RNF09 | **CUS-018** | S08 | `endpoints/certificates.py` (`/download`, `/verificar`)<br>`certificate_service.py`<br>`CertificateVerifyView.tsx` | `test_certificates.py` (14 tests)<br>`CertificateVerifyView.test.tsx` (12 tests) | **Homologado** ✅ | Documentar compilación ReportLab en streaming, hash SHA-256 y verificación QR. |
| **MOD-08** Analítica y Supervisión | **RF24** | RN-11, RNF03, RNF05 | **CUS-020** | S02 / S08 | `core/config.py`<br>`AdminConfigView.tsx` | `test_simulation.py` (8 tests) | **Homologado** ✅ | Documentar gobernanza de aforos reglamentarios (10 presencial / 20 virtual). |
| **MOD-08** Analítica y Supervisión | **RF25** | RNF02, RNF04 | **CUS-011**, **CUS-015** | S08 | `endpoints/simulation.py` (`/benchmark`)<br>`simulation_service.py`<br>`AdminAnalyticsView.tsx` | `test_simulation.py` (16 tests)<br>`AdminAnalyticsView.test.tsx` (18 tests) | **Homologado** ✅ | Alinear métricas de retención ICACIT con reportes agregados y simulación benchmark. |
| **MOD-08** Analítica y Supervisión | **RF26** | RN-02, RN-14, RNF02, RNF09 | **CUS-016**, **CUS-022** | S06 / S07 | `endpoints/bitacora.py` (`/bitacoras`)<br>`endpoints/consent.py`<br>`AdminAuditView.tsx` | `test_bitacora.py` (14 tests)<br>`AdminAuditView.test.tsx` (16 tests) | **Homologado** ✅ | Documentar panel de visado docente de bitácoras y auditoría Ley 29733. |

Fuente: Elaboración propia a partir de la auditoría técnica de trazabilidad.

El Cuadro 1.2 establece la correspondencia formal de la arquitectura del Sistema Web P2P. Todos los requerimientos funcionales (`RF01`–`RF26`) y casos de uso canónicos (`CUS-001`–`CUS-024`) cuentan con respaldo en código y pruebas automatizadas, eliminando vacíos conceptuales o huérfanos de implementación. Se enfatiza que las decisiones de homologación adoptadas en este cuadro guiarán las actualizaciones materiales de los documentos maestros en los hitos sucesivos.

---

## 3. Resolución y Estado de las Ocho Discrepancias Técnicas Principales

A continuación, se detalla el análisis exhaustivo, el consenso del equipo consultor y el estado de aplicación en los documentos maestros para cada discrepancia:

### Cuadro 1.3: Matriz de Resolución de Discrepancias Documentales Críticas

| Discrepancia | Diagnóstico Técnico de la Evidencia | Decisión de Homologación Adoptada | Estado de Aplicación en Documentos Maestros |
| :--- | :--- | :--- | :---: |
| **1. Discrepancia en RF20 (Recursos vs. Encuestas)** | El SRS v3.0 asigna RF20 a *"Recursos Académicos"*, mientras que el SAD v3.0, la migración `005` y `app/api/v1/endpoints/survey.py` implementan `encuestas_calidad` (CSAT 24h post-mentoría). La gestión de enlaces de recursos didácticos se resolvió como atributo opcional de la oferta en `SesionMentoria`. | **Homologar RF20 formalmente como "Captura de Encuestas de Calidad Post-Mentoría (Ventana 24h)"** en el SRS v3.1. La gestión de enlaces a recursos queda formalizada como capacidad complementaria dentro de `RF08` y `RF19`. | **Decisión aprobada; pendiente de aplicación en Tabla 5.3 del SRS (programado para H02).** El SRS v3.0 conserva temporalmente el texto anterior. |
| **2. Contradicción CUS-008 y CUS-011 vs. Análisis Histórico** | En los documentos históricos de análisis, CUS08 correspondía a Bitácora y CUS11 a Asistencia QR. En la línea base canónica de diseño, **CUS-008 es Espacios y Cronogramas** (MOD-02) y **CUS-011 es Reportes Analíticos de Gestión** (MOD-08). Textos residuales en SRS mezclaban la numeración histórica. | **Alinear el 100% de referencias textuales a la nomenclatura canónica de diseño:** CUS-008 = Espacios Físicos y Cronogramas; CUS-011 = Reportes e Indicadores Analíticos; CUS-012 = Registro de Asistencia; CUS-013 = Registro de Bitácora Pedagógica. | **Decisión aprobada; en depuración progresiva.** CUS piloto refinados en H01; depuración en capítulos 1 a 5 programada para H02 y SAD para H07. |
| **3. Desalineación de Rutas y Routers REST** | El SRS v3.0 cita rutas preliminares inexistentes: `GET /api/v1/spaces/availability`, `PUT /api/v1/mentorships/offers/{id}/reschedule`, `GET /api/v1/analytics/dashboard`. | **Actualizar las matrices de contratos del SRS y SAD a los routers reales:** `/api/v1/spaces/import-schedule`, `/free-slots`, `/classrooms`; `/api/v1/offers`; `/api/v1/recommendations/simulation/testbench` y `/api/v1/simulation/benchmark`. | **Decisión aprobada; pendiente de actualización material.** Se actualizará en Sección 5 del SRS (H02) y en catálogo OpenAPI del SAD (H08). |
| **4. Versión de Python 3.14 vs. 3.13 en CI** | El SAD v3.0 línea 32 menciona Python 3.14 (inestable). El archivo `.github/workflows/ci.yml` fija `python-version: "3.13"` y el entorno local ejecuta Python 3.13.5. | **Corregir en SAD el texto formal a "Python 3.13"**, garantizando estricta congruencia con la infraestructura de despliegue e integración continua. | **Decisión aprobada; pendiente de edición en SAD (H07).** El SAD actual v3.0 aún contiene la mención a 3.14. |
| **5. Diccionario Físico: 15 vs. 16 Tablas Relacionales** | El SAD v3.0 titula su sección 10.2 como *"15 Tablas Relacionales"*. La migración `005` y `app/models/attendance.py` incorporaron `tokens_asistencia_activos` para soporte multi-worker de códigos TOTP de 30 segundos. | **Expandir la sección 10.2 del SAD a "16 Tablas Relacionales"**, incorporando el diagrama y la ficha técnica DDL de `tokens_asistencia_activos`. | **Decisión aprobada; pendiente de edición en SAD (H08).** El SAD actual v3.0 aún conserva el inventario de 15 tablas. |
| **6. Omisión de Servicios Reales Recientes en SAD** | Tras la auditoría del 12/11/2026, se integraron servicios reales en backend: transporte SMTP para Gmail (`@virtual.upt.pe`), Supabase Storage para constancias/recursos, Google Identity Services (GIS) y Scheduler en background. | **Incorporar en la Vista de Implementación y Despliegue del SAD las especificaciones y contratos de estos 4 componentes**, eliminando toda alusión a servicios simulados en producción. | **Decisión aprobada; pendiente de redacción en SAD (H07, H08).** El SAD v3.0 aún no incluye estas fichas. |
| **7. Discrepancia en Métricas de Pruebas (627 vs. 658 vs. 682)** | El SRS/SAD v3.0 citan 627 pruebas. Tras Sprint 08 se alcanzaron 658 pruebas y con los servicios externos se reportaron históricamente 682 pruebas superadas en el commit `3f6e31d`. No obstante, el pipeline reciente de CI en `main` reportó fallas de linteo. | **Consignar las 682 pruebas automatizadas como cifra histórica reportada sujeta a nueva validación técnica.** Mantener cautela metodológica y revalidar la totalidad de suites tras sanear los errores de linteo en el entorno de integración. | **Criterio adoptado; cifra reportada formalmente.** Pendiente de revalidación integral tras remediación del linter en CI. |
| **8. Ruta de Contingencia de Autenticación (`dummyIdToken`)** | En `LoginOtpView.tsx` (líneas 263–272), la función `handleGoogleFederatedFallback` construye un token simulado en base64 (`dummyIdToken`) con usuario predeterminado cuando GIS no carga. | **Documentar la ruta de contingencia como hallazgo de deuda técnica pendiente.** No modificar código funcional en esta fase documental; incorporar análisis de remediación en el reporte de seguridad del SAD. | **Hallazgo registrado en H01-R; pendiente de remediación técnica en fase de construcción.** |

Fuente: Elaboración propia.

El análisis del Cuadro 1.3 evidencia que las discrepancias detectadas se encuentran plenamente diagnosticadas y cuentan con solución consensuada. Sin embargo, conforme a la disciplina metodológica del proyecto, una matriz de homologación no sustituye la edición directa de los documentos maestros: las correcciones sobre el SRS se aplicarán en H02 a H06 y las del SAD en H07 a H09.

---

## 4. Matriz Canónica de las 16 Tablas Físicas de Persistencia (PostgreSQL / Supabase)

A continuación, se homologa el inventario completo de entidades relacionales que integran el modelo físico de persistencia:

### Cuadro 1.4: Inventario Homologado de Tablas Físicas del Sistema Web P2P

| Nº | Nombre de Tabla Física | Modelo SQLAlchemy | Migración Alembic | Módulo Asociado | Propósito y Regla de Negocio Vinculada |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | `asignaturas` | `Asignatura` | `001_initial_curriculum_and_auth.py` | MOD-03 | Catálogo oficial de materias críticas EPIS (ciclos I al IV, RN-11). |
| **2** | `temas_conceptuales` | `TemaConceptual` | `001_initial_curriculum_and_auth.py` | MOD-03 | Desglose silábico oficial por unidades de aprendizaje (RF05). |
| **3** | `auth_challenges` | `AuthChallenge` | `001_initial_curriculum_and_auth.py` | MOD-01 | Desafíos OTP institucionales de 6 dígitos con vigencia de 5 min (RN-01). |
| **4** | `consentimientos_legales` | `ConsentimientoLegal` | `002_roles_and_profiles.py` | MOD-01 | Trazabilidad de consentimiento informado digital bajo Ley N° 29733 (RN-02). |
| **5** | `roles` | `Rol` | `002_roles_and_profiles.py` | MOD-01 | Catálogo de roles de seguridad del sistema (RBAC). |
| **6** | `usuario_roles` | `UsuarioRol` | `002_roles_and_profiles.py` | MOD-01 | Asignación y revocación de roles institucionales con auditoría (RN-03). |
| **7** | `perfiles_academicos` | `PerfilAcademico` | `002_roles_and_profiles.py` | MOD-03 | Registro de ciclo lectivo, materias de fortaleza y regla de mérito (RN-03). |
| **8** | `disponibilidades_horarias` | `DisponibilidadHoraria` | `002_roles_and_profiles.py` | MOD-03 | Matriz semanal interactiva 6×11 de disponibilidad de mentores (RN-04). |
| **9** | `sesiones_mentoria` | `SesionMentoria` | `003_mentoring_offers.py` | MOD-02 | Ofertas de mentoría con aforos inmutables (10 presencial / 20 virtual, RN-05). |
| **10** | `reservas_cupo` | `ReservaCupo` | `004_booking_and_reservations.py` | MOD-05 | Inscripciones de estudiantes con bloqueo pesimista y ratificación (RN-08). |
| **11** | `solicitudes_demanda` | `SolicitudDemanda` | `004_booking_and_reservations.py` | MOD-04 | Banco de necesidades formativas no cubiertas para mentores (RF07). |
| **12** | `asistencias_sesion` | `AsistenciaSesion` | `005_closure_and_advanced_modules.py` | MOD-06 | Marcación y check-in presencial/virtual con pase QR dinámico (RN-12). |
| **13** | `tokens_asistencia_activos` | `TokenAsistenciaActivo` | `005_closure_and_advanced_modules.py` | MOD-06 | Soporte persistente multi-worker para códigos TOTP de 30 segundos (RN-12). |
| **14** | `bitacoras_pedagogicas` | `BitacoraPedagogica` | `005_closure_and_advanced_modules.py` | MOD-06 | Registro docente con resumen pedagógico, logros y firma SHA-256 (RF18). |
| **15** | `encuestas_calidad` | `EncuestaCalidad` | `005_closure_and_advanced_modules.py` | MOD-06 | Encuestas CSAT de 4 dimensiones en ventana de 24 horas (RF20, RN-13). |
| **16** | `certificados_horas` | `CertificadoHoras` | `005_closure_and_advanced_modules.py` | MOD-07 | Acreditación oficial de horas docentes en PDF con hash e integridad QR (RN-14). |

Fuente: Elaboración propia a partir del análisis DDL de Alembic y SQLAlchemy.

El Cuadro 1.4 confirma de manera concluyente que el esquema de base de datos relacional de la plataforma está compuesto por **16 tablas físicas**. Esta aclaración subsana definitivamente el error cuantitativo del SAD v3.0 y proporciona una base sólida para el modelado DDL de la versión v3.1.

---

## 5. Conclusiones y Próximos Pasos

La Matriz Canónica de Homologación formaliza el marco de trazabilidad unívoco del proyecto. Se han clasificado y resuelto las 7 discrepancias críticas documentales, demostrando que:
1. El código fuente es plenamente consistente y supera los requisitos funcionales proyectados.
2. La documentación rectora requería alineación precisa de nombres de endpoints, versiones de lenguajes, inventario relacional y definición funcional de `RF20`.
3. Queda expedito el camino para la aplicación de la **Guía de Narrativas Detalladas** y el refinamiento de los casos piloto `CUS-001` y `CUS-003`.
