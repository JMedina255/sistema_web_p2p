# Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

> **Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
> **Curso:** Construcción de Software I
> **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
> **Autores:**
> - ANTAYHUA MAMANI, Renzo Antonio (2022073504)
> - MEDINA QUISPE, Joan Cristian (2022074255)
>
> **Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
>
> **Semestre Académico:** 2026-II

---

## 📌 1. Visión General del Sistema

El **Sistema Web P2P** es una plataforma institucional orientada a conectar a estudiantes de ciclos formativos iniciales (*Mentoreados*, ciclos I al IV) con estudiantes de rendimiento sobresaliente de ciclos superiores (*Mentores*, ciclos VII al X) para mitigar los altos índices de reprobación y deserción en asignaturas filtro críticas (*Cálculo I/II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos*) de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

**Estado actual:** Fase de construcción — **Sprint 4 Culminado, Verificado y Homologado**. La solución se desarrolla en `aplicacion/` (React 19 SPA + FastAPI RESTful con persistencia en PostgreSQL/Supabase conforme a **RNF09**).

- **Sprint 1 (Base Técnica y Acceso Inicial):** **Culminado y Verificado** (96 pruebas automatizadas). Integración de React con FastAPI, conexión a Supabase (`p2p-epis-dev`), flujo OTP de acceso institucional (`@upt.pe`), catálogo curricular inicial y pipeline de CI en GitHub Actions.
- **Sprint 2 (Roles, Currículo y Perfiles):** **Culminado y Verificado** (150 pruebas automatizadas). Formulario accesible de consentimiento digital bajo la **Ley N° 29733** (**RF02** / **RN-02**), buscador avanzado en tiempo real con temarios silábicos (**RF05** / **CUS21**), configuración de perfil formativo y matriz semanal 6×11 de disponibilidad con regla de mérito **RN-03** (**RF04** / **CUS15**), administración de roles y políticas de seguridad multi-usuario RLS (**RNF02**).
- **Sprint 3 (Publicación de Ofertas, Motor EdRecSys y Testbench):** **Culminado y Verificado** (209 pruebas automatizadas consolidadas).
  - **T-14 (Frontend — Joan):** Formulario reactivo accesible de publicación de ofertas con carga dinámica silábica (`OfferPublishView.tsx`, `offerService.ts`), validación estricta de antelación obligatoria $> 24\text{ h}$ y recomendada $\ge 48\text{ h}$ (**RN-04**), aforo reglamentario inmutable de 10 presencial y 20 virtual (**RN-05**), y asignación de aulas EPIS (**RN-06**) o Meet institucional (**RN-07**).
  - **T-15 (Backend — Renzo):** Motor de recomendación inteligente *Top-k* multifactorial (**EdRecSys v1.0**) combinando similitud temático-silábica (Jaccard/Dice $40\%$), compatibilidad horaria semanal 6×11 ($35\%$), modalidad ($15\%$), afinidad curricular ($10\%$) y multiplicadores de materias filtro ($1.0\text{x}$ a $1.3\text{x}$) con exclusión forzada de mérito (**RN-03**).
  - **T-16 (Backend — Renzo):** Entidad relacional física `sesiones_mentoria`, migración Alembic `003_mentoring_offers.py`, endpoints REST bajo `/api/v1/offers` y `/api/v1/recommendations/*` con esquemas Pydantic v2 tipados y políticas RLS activas.
  - **T-18 (Backend — Renzo):** Servicio `SimulationService` y testbench algorítmico evaluando 4 casos frontera (solapamiento 0, temas disjuntos, catálogo vacío, postulantes ciclo $< 7$), determinismo al 100% y latencia media de $35.8\text{ µs}$ por candidato ($0.86\text{ ms}$ total, superando **RNF03** $< 50\text{ ms}$).
- **Sprint 4 (Recomendación Top-k, Feed, Reserva Transaccional ACID y Quórum T-24h):** **Culminado y Verificado** (245 pruebas automatizadas consolidadas).
  - **T-17 (Backend — Renzo):** Consolidación en `RecommendationService` del cálculo Top-k multifactorial con ponderación curricular de materias filtro EPIS (1.0x a 1.3x), desempate determinista quíntuple y exclusión estricta de postulantes con ciclo < 7 (**RN-03**).
  - **T-18 / T-20 (Frontend — Joan):** Feed interactivo de recomendaciones Top-k (`RecommendationFeedView.tsx`, `recommendationService.ts`) con tarjetas explicables XAI, selector dual de exploración, aforo en tiempo real y panel pedagógico empty-state para solicitudes por demanda (**CUS03**).
  - **T-19 (Backend/Frontend — Renzo / Joan):** Banco de pruebas de ordenamiento determinista Top-k con 5 casos frontera y validación estricta de parámetros de rango 1 <= k <= 20.
  - **T-21 / T-23 (Frontend — Joan):** Modal reactivo de reserva transaccional (`BookingModalView.tsx`, `bookingService.ts`) con advertencia reglamentaria de ratificación obligatoria antes de T-24h (**RN-08**), cláusula de la Ley N° 29733 (**RN-02**) y captura de errores 409.
  - **T-22 (Backend — Renzo):** Modelado relacional de `reservas_cupo` y `solicitudes_demanda`, migración Alembic `004_booking_and_reservations.py`, endpoints `/api/v1/bookings/*` y `/api/v1/quorum/*` con tipado Pydantic v2.
  - **T-24 (Backend — Renzo):** Coordinador transaccional ACID con bloqueo pesimista `SELECT ... FOR UPDATE`, prevención de sobrecupo (tasa 0.00% verificada en suite multihilo de 20 hilos bajo **RNF07**) y corte automático de quórum del 50% (**RN-09**).
- **Aseguramiento de Calidad Global:** Batería consolidada de **245 pruebas automatizadas** (87 en frontend con Vitest y 158 en backend con Pytest) distribuidas en 27 suites con 0 fallos (100% éxito), superando ampliamente el umbral normativo del 70% de **RNF09** con **92.56% de cobertura en frontend** y **91.22% en backend**. Análisis estático limpio con ESLint 9 y Ruff 0.9 (0 errores), y empaquetado de producción de Vite limpio (`dist/`) en 653 ms.

### Pilares Funcionales y Tecnológicos
1. **Acceso y privacidad:** RF01–RF02 y RNF01–RNF02 exigen OTP institucional, consentimiento informado bajo la Ley N° 29733 y protección de datos con políticas RLS de PostgreSQL/Supabase.
2. **Currículo y perfiles:** RF04–RF05 administran las materias formativas críticas, los temarios silábicos oficiales y las agendas semanales de disponibilidad con validación de mérito en ciclos VII al X (RN-03).
3. **Oferta docente de mentoría:** RF08 y CUS06 permiten a los mentores programar clases grupales con control estricto de antelación (RN-04) y aforos estándar inmutables (RN-05).
4. **Recomendación personalizada:** RF06 y CUS02 analizan afinidad temática silábica, coincidencia horaria y balance de carga con el algoritmo *Top-k* (Sprint 4).
5. **Reserva, confirmación y quórum:** RF12–RF16 distinguen reserva provisional (CUS04), ratificación (CUS24), corte T−24 h (CUS23) y decisión del mentor ante quórum insuficiente (CUS07).
6. **Asistencia y bitácora:** RF17 y CUS08 permiten registrar asistencia y bitácora docente post-sesión.
7. **Auditoría y certificación:** CUS22 visa horas antes de la emisión CUS13 de constancias digitales con hash de integridad institucional.

---

## 📚 2. Mapa de Documentación Oficial de Ingeniería de Software

La documentación del proyecto se encuentra formalmente organizada en dos etapas metodológicas consecutivas: la **Fase de Análisis** (línea base original congelada) y la **Fase de Diseño Técnico** (etapa prescriptiva actual bajo las 10 reglas de diseño):

### 2.1. Fase de Diseño Técnico y Cierre de Sprints (docs/diseño/)

| Entregable / Documento | Ubicación | Descripción y Alcance Metodológico |
| :--- | :--- | :--- |
| **INFORME ACADÉMICO SPRINT 1** | [docs/diseño/G03_EPIS_Informe_Sprint_01.md](docs/diseño/G03_EPIS_Informe_Sprint_01.md) | **Informe Canónico del Sprint 01:** Elaborado bajo la plantilla oficial institucional, detallando objetivos, balance de los 5 PBI, secuencia de hitos, figuras de evidencia, matrices de pruebas, contratos y dependencias hacia S2. |
| **INFORME GENERAL SPRINT 1** | [docs/diseño/INFORME_GENERAL_SPRINT_01.md](docs/diseño/INFORME_GENERAL_SPRINT_01.md) | **Reporte Maestro Exhaustivo:** Ficha técnica, diagramas PlantUML, capturas de pantalla, especificación de contratos REST, diccionario físico DDL + RLS, máquinas de estado, ADRs y certificación DoD. |
| **EVIDENCIA DE PRUEBAS S1** | [docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_01.md](docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_01.md) | **Catálogo de Calidad Automatizada S1:** Desglose de las 13 suites, 96 pruebas superadas (50 backend / 46 frontend) y reportes de cobertura (>91%). |
| **PAQUETE CANÓNICO SPRINT 2** | [docs/sprints/sprint-02/README.md](docs/sprints/sprint-02/README.md) | **Paquete Oficial y Canónico del Sprint 02:** Estructura modular autónoma con planificación, trazabilidad, informes G03 y técnico, presentación PPTX/PDF, evidencias visuales, matriz de pruebas y actas. |
| **INFORME ACADÉMICO SPRINT 2** | [docs/sprints/sprint-02/03-informe/INFORME_ACADEMICO_G03_SPRINT_02.md](docs/sprints/sprint-02/03-informe/INFORME_ACADEMICO_G03_SPRINT_02.md) | **Informe Canónico del Sprint 02 (G03):** Elaborado bajo la estructura institucional de 11 secciones: roles, mérito académico (RN-03), consentimiento Ley 29733, matriz semanal 6×11, 7 diagramas Kroki PNG/SVG, matrices y balance de 150 pruebas. |
| **INFORME GENERAL SPRINT 2** | [docs/sprints/sprint-02/03-informe/INFORME_GENERAL_TECNICO_SPRINT_02.md](docs/sprints/sprint-02/03-informe/INFORME_GENERAL_TECNICO_SPRINT_02.md) | **Reporte Maestro Exhaustivo S2:** Roles, consentimiento Ley 29733, matriz semanal 6×11, catálogo avanzado y cierre DoD del Sprint 2 (1,494 líneas con enlaces portables). |
| **TRAZABILIDAD SPRINT 2** | [docs/sprints/sprint-02/02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md](docs/sprints/sprint-02/02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md) | **Matriz Oficial de Trazabilidad S2:** Matriz canónica de 12 eslabones (PBI, Requerimientos, Reglas, HU Gherkin, CUS, Narrativas, Diagramas SRS/SAD, Código, Pruebas y Evidencias). |
| **REGISTRO INCONSISTENCIAS S2** | [docs/sprints/sprint-02/02-trazabilidad/REGISTRO_INCONSISTENCIAS_SPRINT_02.md](docs/sprints/sprint-02/02-trazabilidad/REGISTRO_INCONSISTENCIAS_SPRINT_02.md) | **Auditoría de Inconsistencias S2:** Registro de 9 inconsistencias detectadas y resueltas (Vue vs React, app/routers vs v1, RF04 vs RF05, HTTP 400 vs 403, autores y precedencia). |
| **PRESENTACIÓN OFICIAL S2** | [docs/sprints/sprint-02/04-presentacion/PRESENTACION_OFICIAL_SPRINT_02.pptx](docs/sprints/sprint-02/04-presentacion/PRESENTACION_OFICIAL_SPRINT_02.pptx) / [.pdf](docs/sprints/sprint-02/04-presentacion/PRESENTACION_OFICIAL_SPRINT_02.pdf) | **Presentación Formal PPTX y PDF:** 20 diapositivas 16:9 con diseño académico, evidencias auténticas del incremento, diagramas oficiales y recorrido demostrativo. |
| **GUION DE EXPOSICIÓN S2** | [docs/sprints/sprint-02/04-presentacion/GUION_EXPOSICION_CORREGIDO.md](docs/sprints/sprint-02/04-presentacion/GUION_EXPOSICION_CORREGIDO.md) | **Guion Técnico Corregido:** Cadena de trazabilidad, notas del orador para 20 diapositivas, FAQ técnica fundamentada y guion para demo en vivo. |
| **EVIDENCIA DE PRUEBAS S2** | [docs/sprints/sprint-02/06-pruebas/EVIDENCIA_PRUEBAS_AUTOMATIZADAS.md](docs/sprints/sprint-02/06-pruebas/EVIDENCIA_PRUEBAS_AUTOMATIZADAS.md) | **Catálogo de Calidad Automatizada S2:** Consolidación de 150 pruebas (84 backend / 66 frontend), aislamiento RLS y matrices de cobertura (>90%). |
| **MATRIZ PRUEBAS EXCEL S2** | [docs/sprints/sprint-02/06-pruebas/MATRIZ_PRUEBAS_CATALOGO_OFICIAL.md](docs/sprints/sprint-02/06-pruebas/MATRIZ_PRUEBAS_CATALOGO_OFICIAL.md) | **Homologación con Catálogo Excel:** Mapeo de casos CUS01, CUS10, CUS15, CUS21 hacia suites de Pytest y Vitest (positivas y negativas). |
| **INFORME GENERAL SPRINT 3** | [docs/diseño/INFORME_GENERAL_SPRINT_03.md](docs/diseño/INFORME_GENERAL_SPRINT_03.md) | **Reporte Maestro Exhaustivo S3:** Publicación de ofertas (T-14), motor EdRecSys v1.0 (T-15), persistencia relacional `sesiones_mentoria` (T-16), testbench algorítmico (T-18), 7 diagramas PlantUML, 7 capturas de pantalla y certificación DoD de 209 pruebas. |
| **INFORME ACADÉMICO SPRINT 3** | [docs/diseño/G03_EPIS_Informe_Sprint_03.md](docs/diseño/G03_EPIS_Informe_Sprint_03.md) | **Informe Canónico del Sprint 03:** Elaborado bajo la estructura institucional de 11 secciones, detallando publicación de ofertas (T-14), persistencia relacional (T-16), motor EdRecSys v1.0 (T-15), testbench algorítmico (T-18), balance de PBI y acreditación de 209 pruebas. |
| **EVIDENCIA DE PRUEBAS S3** | [docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_03.md](docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_03.md) | **Catálogo de Calidad Automatizada S3:** Consolidación de 209 pruebas (122 backend / 87 frontend), desglose de las 26 suites, matrices de cobertura (>91% en ambos subsistemas), testbench algorítmico y comandos reproducibles. |
| **INFORME GENERAL SPRINT 4** | [docs/diseño/INFORME_GENERAL_SPRINT_04.md](docs/diseño/INFORME_GENERAL_SPRINT_04.md) | **Reporte Maestro Exhaustivo S4:** Recomendación Top-k (T-17), feed interactivo (T-18/T-20), modal de reserva (T-21/T-23), modelo relacional `reservas_cupo` (T-22), coordinador transaccional ACID con bloqueo pesimista `SELECT FOR UPDATE` (T-24 / RNF07), evaluación de quórum a T-24h (RN-08/RN-09), 6 diagramas PlantUML, 8 capturas técnicas y certificación DoD de 245 pruebas. |
| **EVIDENCIA DE PRUEBAS S4** | [docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_04.md](docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_04.md) | **Catálogo de Calidad Automatizada S4:** Consolidación de 245 pruebas (158 backend / 87 frontend), desglose de las 27 suites, matrices de cobertura (91.22% backend / 92.56% frontend), testbench de concurrencia multihilo (0.00% sobrecupo) y comandos reproducibles. |
| **FD04: Informe SAD (Diseño v2.0)** | [docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md](docs/diseño/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md) | **Arquitectura de Software en Diseño:** Vistas 4+1 prescriptivas, contratos de endpoints, diccionario físico PostgreSQL, políticas RLS, máquinas de estado del dominio y ADRs. |
| **FD03: Informe SRS (Diseño v2.1)** | [docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md](docs/diseño/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md) | **Requerimientos con Trazabilidad:** Especificación alineada a la arquitectura desacoplada y los endpoints construidos. |
| **Reglas de Diseño (Hardening D-1..D-10)** | [reglas_documentacion_diseño.md](reglas_documentacion_diseño.md) | Estándares obligatorios de diseño prescriptivo: contratos REST, diccionario físico, diagramas técnicos PlantUML, máquinas de estado, variables .env y ADRs. |

### 2.2. Gestión de Sprints y Despliegue (docs/sprints/ y Raíz)

| Entregable / Documento | Ubicación | Descripción y Alcance Metodológico |
| :--- | :--- | :--- |
| **Plan de Sprints y Tareas** | [docs/sprints/PLAN_SPRINTS_Y_TAREAS.md](docs/sprints/PLAN_SPRINTS_Y_TAREAS.md) | **Planificación Scrum:** Desglose del Product Backlog (37 PBI), capacidad (91 h) y asignación operativa (T-01 a T-51). |
| **Bitácora de Sprint 1** | [docs/sprints/sprint-01.md](docs/sprints/sprint-01.md) | **Registro de Ejecución S1:** Culminación integral de T-01, T-02, T-03, T-06, T-07 y T-09 con 96 pruebas automatizadas. |
| **Bitácora de Sprint 2** | [docs/sprints/sprint-02/01-planificacion/BITACORA_EJECUCION_SPRINT_02.md](docs/sprints/sprint-02/01-planificacion/BITACORA_EJECUCION_SPRINT_02.md) | **Registro de Ejecución S2:** Culminación integral de T-04, T-05, T-08, T-10, T-11, T-12 y T-13 con 150 pruebas y cierre DoD (también disponible en [docs/sprints/sprint-02.md](docs/sprints/sprint-02.md)). |
| **Bitácora de Sprint 3** | [docs/sprints/sprint-03.md](docs/sprints/sprint-03.md) | **Registro de Ejecución S3:** Culminación integral de T-14, T-15, T-16 y T-18 con 209 pruebas consolidadas, motor EdRecSys v1.0 y testbench. |
| **Bitácora de Sprint 4** | [docs/sprints/sprint-04.md](docs/sprints/sprint-04.md) | **Especificación Técnica y Planificación S4:** Recomendación Top-k, feed interactivo, reservas transaccionales con bloqueo pesimista `SELECT ... FOR UPDATE` (RNF07), control de aforo (RN-05), trazabilidad integral (RF09–RF16, RN-08–RN-13) y banco de pruebas de concurrencia. |
| **Guía de Configuración Supabase** | [docs/supabase_setup_guide.md](docs/supabase_setup_guide.md) | **Paso a paso para el usuario:** Conexión con Session Pooler, migraciones Alembic, scripts RLS y JWT Secret. |

### 2.3. Fase de Análisis Histórica (docs/analisis/)

| Entregable / Documento | Ubicación | Descripción y Alcance Metodológico |
| :--- | :--- | :--- |
| **Resumen Ejecutivo del Sistema** | [docs/analisis/resumen_sistema_y_casos_de_uso.md](docs/analisis/resumen_sistema_y_casos_de_uso.md) | Visión concisa, flujo macro de 5 fases, matriz de 17 CUS críticos, relaciones de precedencia y síntesis analítica. |
| **FD01: Informe de Factibilidad** | [docs/analisis/FD01-EPIS-Informe de Factibilidad.md](docs/analisis/FD01-EPIS-Informe%20de%20Factibilidad.md) | Evaluación exhaustiva de viabilidad operativa, técnica, económica y legal en el ámbito universitario de la UPT. |
| **FD02: Informe Visión del Proyecto** | [docs/analisis/FD02-EPIS-Informe Vision de Proyecto.md](docs/analisis/FD02-EPIS-Informe%20Vision%20de%20Proyecto.md) | Oportunidades de negocio, definición de stakeholders, posicionamiento del producto y características principales. |
| **FD03: SRS Canónico (v2.0)** | [docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md](docs/analisis/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md) | Línea base oficial de requisitos: 24 CUS, modelos ECB, diagramas de actividades y clases preliminares. |
| **FD04: SAD Preliminar (v1.1)** | [docs/analisis/FD04-EPIS-Informe SAD de Proyecto.md](docs/analisis/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md) | SAD preliminar de la fase de análisis con identificación de decisiones abiertas. |
| **Bóveda General de Diagramas** | [docs/diagramas_general.md](docs/diagramas_general.md) | Bóveda consolidada y de hardening de diagramas PlantUML. |
| **Matriz de Inconsistencias** | [docs/analisis/matriz_inconsistencias.md](docs/analisis/matriz_inconsistencias.md) | Registro de auditoría y resolución de discrepancias en requisitos y modelos. |
| **Catálogo de Pruebas (Análisis)** | [docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx](docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) | Matriz formal de casos de prueba funcional de análisis. |
| **Trazabilidad Sprint 2 (Canónica)** | [docs/sprints/sprint-02/02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md](docs/sprints/sprint-02/02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md) | Matriz oficial de 12 eslabones canónicos, requisitos, casos de uso y modelos de arquitectura del Sprint 02 (espejo histórico en [docs/analisis/trazabilidad_sprint_02.md](docs/analisis/trazabilidad_sprint_02.md)). |

---

## 🏛️ 3. Módulos Funcionales del Sistema

La arquitectura del sistema se estructura en 8 módulos interconectados que orquestan el flujo integral de mentoría entre pares:

```text
┌────────────────────────────────────────────────────────┐
│            ECOSISTEMA P2P  -  EPIS UPT (2026)          │
└───────────────────────────┬────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    MOD-01    │     │    MOD-02    │     │    MOD-03    │
│ Autenticación│     │ Recomendación│     │ Oferta y     │
│ 2FA / RLS    │     │ Top-k Híbrido│     │ Demanda P2P  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    MOD-04    │     │    MOD-05    │     │    MOD-06    │
│ Reservas y   │     │ Asistencia QR│     │ Calidad CSAT │
│ Quórum T-24h │     │ y Bitácoras  │     │ e Insignias  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐            ┌──────────────┐
       │    MOD-07    │            │    MOD-08    │
       │ Certificación│            │ Auditoría y  │
       │ SHA-256 + QR │            │ Analítica    │
       └──────────────┘            └──────────────┘
```

---

## 📁 4. Estructura del Repositorio

```text
Proyecto_Sistema_Web_P2P/
├── aplicacion/                                # Aplicación desacoplada oficial
│   ├── backend/                               # API RESTful (FastAPI + SQLAlchemy + Alembic + Pytest)
│   │   ├── app/
│   │   │   ├── api/v1/endpoints/              # Endpoints: health, auth, consent, curriculum, profiles, roles, offers, recommendations
│   │   │   ├── core/                          # Configuración pydantic-settings y seguridad JWT/OTP
│   │   │   ├── db/                            # Conexión diferida, session pooler y migraciones Alembic
│   │   │   │   └── migrations/versions/       # Migraciones 001 (catálogo), 002 (roles/perfiles) y 003 (sesiones_mentoria)
│   │   │   ├── models/                        # Modelos ORM: Asignatura, TemaConceptual, AuthChallenge, Consent, Profile, Role, SesionMentoria
│   │   │   ├── schemas/                       # Esquemas Pydantic tipados (auth, consent, curriculum, profile, roles, offer, recommendation)
│   │   │   ├── services/                      # Servicios: AuthService, CurriculumService, ConsentService, ProfileService, RoleService,
│   │   │   │                                  #            OfferService, RecommendationService (EdRecSys v1.0), SimulationService
│   │   │   └── main.py                        # Punto de entrada de FastAPI con middleware CORS
│   │   ├── scripts/                           # Scripts SQL de RLS para Supabase y generadores de evidencias
│   │   ├── tests/                             # 122 pruebas automatizadas (unitarias, integración, EdRecSys y testbench algorítmico)
│   │   ├── alembic.ini                        # Configuración de migraciones hacia PostgreSQL
│   │   ├── pyproject.toml                     # Configuración centralizada de Ruff, Coverage y Pytest
│   │   └── requirements.txt                   # Dependencias reproducibles fijadas con ==
│   └── frontend/                              # SPA cliente reactiva (React 19 + TypeScript + Vite + Vitest)
│       ├── src/
│       │   ├── components/                    # Componentes UI: LoginOtpView, ConsentModalView, CurriculumCatalogView,
│       │   │                                  #                 ProfileAvailabilityView, OfferPublishView, HealthStatus
│       │   ├── services/                      # Servicios: apiClient.ts, authService.ts, consentService.ts,
│       │   │                                  #            profileService.ts, offerService.ts
│       │   ├── data/                          # Tipos TypeScript de dominio
│       │   ├── App.tsx                        # Orquestador con navegación (Auth, Consent, Catálogo, Perfil, Ofertas, Servicios)
│       │   └── main.tsx                       # Punto de entrada ReactDOM
│       ├── package.json                       # Dependencias y scripts de prueba y cobertura (87 pruebas, 92.52% cobertura)
│       └── vite.config.ts                     # Configuración del empaquetador Vite con soporte de Vitest
├── docs/                                      # Acervo documental formal de ingeniería de software
│   ├── sprints/
│   │   ├── PLAN_SPRINTS_Y_TAREAS.md           # Planificación Scrum canónica (37 PBI, 91 h, S1–S8)
│   │   ├── sprint-01.md                       # Bitácora oficial de ejecución del Sprint 1
│   │   ├── sprint-02/                         # Paquete canónico oficial del Sprint 02 (01 al 07)
│   │   │   ├── 01-planificacion/              # Plan de trabajo y bitácora de ejecución
│   │   │   ├── 02-trazabilidad/               # Matriz de 12 eslabones y registro de inconsistencias
│   │   │   ├── 03-informe/                    # Informes académicos formales (G03 y Técnico)
│   │   │   ├── 04-presentacion/               # Presentación formal (PPTX, PDF) y guion técnico
│   │   │   ├── 05-evidencias/                 # 7 capturas y 7 diagramas oficiales en alta resolución
│   │   │   ├── 06-pruebas/                    # Mapeo de catálogo Excel y acreditación de 150 tests
│   │   │   └── 07-actas/                      # Acta de cierre y declaraciones de limitación
│   │   ├── sprint-02.md                       # Bitácora histórica de ejecución del Sprint 2
│   │   └── sprint-03.md                       # Bitácora oficial de ejecución del Sprint 3 (Cierre integral T-14..T-18)
│   ├── diseño/                                # Documentación de diseño prescriptivo (Hardening D-1..D-10)
│   │   ├── INFORME_GENERAL_SPRINT_01.md       # Informe de cierre exhaustivo del Sprint 1
│   │   ├── INFORME_GENERAL_SPRINT_02.md       # Informe de cierre exhaustivo del Sprint 2
│   │   ├── INFORME_GENERAL_SPRINT_03.md       # Informe de cierre exhaustivo del Sprint 3 (EdRecSys, Ofertas, Testbench)
│   │   ├── EVIDENCIA_PRUEBAS_SPRINT_01.md     # Catálogo de pruebas S1 (96 pruebas, >91% cov)
│   │   ├── EVIDENCIA_PRUEBAS_SPRINT_02.md     # Catálogo de pruebas S2 (150 pruebas, >90% cov)
│   │   ├── EVIDENCIA_PRUEBAS_SPRINT_03.md     # Catálogo de pruebas S3 (209 pruebas, >91% cov)
│   │   └── imagenes/sprint-03/                # 7 capturas de pantalla de alta fidelidad (>100KB)
│   ├── supabase_setup_guide.md                # Guía canónica paso a paso para vincular proyecto Supabase
│   ├── FD01-EPIS-Informe de Factibilidad.md  # Viabilidad operativa, técnica, económica y legal
│   ├── FD02-EPIS-Informe Vision de Proyecto.md # Visión, actores, posicionamiento y alcance
│   ├── FD03-EPIS-Informe SRS de Proyecto.md  # Especificación formal de requisitos (SRS canónico IEEE 830)
│   ├── FD04-EPIS-Informe SAD de Proyecto.md  # Documento formal de arquitectura de software (Modelo 4+1)
│   ├── resumen_sistema_y_casos_de_uso.md     # Síntesis ejecutiva, flujo macro, matriz CUS y reglas de negocio
│   ├── diagramas_general.md                  # Bóveda consolidada de diagramas PlantUML sincronizada
│   └── Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx # Catálogo de pruebas funcionales y de aceptación
├── frontend/                                  # Maqueta funcional de referencia visual (conservada)
├── reglas_documentacion.md                    # Manual de normas de documentación y hardening (v1.3)
└── README.md                                  # Mapa central de navegación del proyecto (este archivo)
```

---

## 🚀 5. Despliegue y Ejecución Local de la Aplicación

### 5.1. Comandos para Validación y Ejecución del Backend

```powershell
cd aplicacion/backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Análisis estático y verificación de formato (Ruff: 0 errores)
ruff check .
ruff format --check .

# Aplicar migraciones a PostgreSQL / Supabase (001, 002 y 003)
alembic upgrade head

# Ejecución de pruebas automatizadas con reporte de cobertura (122 pruebas, 91.83% de cobertura)
pytest tests/ --cov=app --cov-report=term-missing

# Ejecución del banco de evaluación algorítmica y casos frontera (T-18)
pytest tests/test_simulation.py -v -s

# Servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- **Swagger API Docs interactivo:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check & DB:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) | [/db](http://localhost:8000/api/v1/health/db)
- **Catálogo de Ofertas de Mentoría:** [http://localhost:8000/api/v1/offers](http://localhost:8000/api/v1/offers)
- **Recomendación Top-k de Mentores:** [http://localhost:8000/api/v1/recommendations/mentors](http://localhost:8000/api/v1/recommendations/mentors)
- **Recomendación Top-k de Ofertas:** [http://localhost:8000/api/v1/recommendations/offers](http://localhost:8000/api/v1/recommendations/offers)
- **Testbench Algorítmico EdRecSys:** [http://localhost:8000/api/v1/recommendations/simulation/testbench](http://localhost:8000/api/v1/recommendations/simulation/testbench)

### 5.2. Comandos para Validación y Ejecución del Frontend

```powershell
cd aplicacion/frontend
npm ci

# Análisis estático (ESLint 9: 0 errores, 0 advertencias)
npm run lint

# Ejecución de pruebas unitarias y cobertura (Vitest: 87 pruebas, 92.52% de cobertura)
npm run test:coverage

# Compilación de producción limpia
npm run build

# Servidor de desarrollo
npm run dev
```
- **Aplicación Web:** [http://localhost:5173](http://localhost:5173)
- **Pestaña `🔐 Acceso & OTP (T-02)`:** Flujo de acceso institucional de 2 pasos con dominio `@upt.pe`.
- **Pestaña `⚖️ Consentimiento Ley 29733 (T-04)`:** Formulario formal de consentimiento informado con bloqueo reactivo ante rechazo.
- **Pestaña `📚 Catálogo Curricular (T-10)`:** Buscador reactivo por código, nombre y unidades temáticas silábicas.
- **Pestaña `👤 Perfil & Disponibilidad (T-11)`:** Declaración de fortalezas/debilidades, validación de mérito RN-03 y grilla semanal 6×11.
- **Pestaña `🏷️ Publicar Ofertas (T-14)`:** Formulario para mentores con validación de antelación obligatoria RN-04 ($> 24\text{ h}$), aforos estándar inmutables RN-05 (10 presencial / 20 virtual) y asignación de infraestructura física o virtual.
- **Pestaña `🛰️ Monitor de Servicios (T-01)`:** Monitoreo en tiempo real de FastAPI y Supabase (`SELECT 1`).

---

## 🛡️ 6. Normas de Calidad y Reglas de Hardening

El proyecto opera bajo directrices de aseguramiento de la calidad registradas en [`reglas_documentacion.md`](reglas_documentacion.md):
- **Regla 1:** Separación estricta de análisis y diseño; trazabilidad biunívoca con el SRS y SAD.
- **Regla 2:** Estructura quíntuple estándar en toda tabla (Presentación → Título → Tabla MD → Fuente → Análisis/Conclusión).
- **Regla 3:** Uso exclusivo de diagramas PlantUML limpios, ejecutables y mantenibles.
- **Regla 4:** Codificación UTF-8 estricta en archivos Markdown.
- **Regla 5:** Hardening continuo y sincronización inmediata con [`docs/diagramas_general.md`](docs/diagramas_general.md).
- **Regla 6:** Estructura canónica de 4 tablas para las narrativas de casos de uso (Ficha, Flujo Principal, Alternativos, Excepciones).
- **Regla 7:** Sincronización y actualización continua del archivo [`README.md`](README.md) ante cualquier evolución de ingeniería.

---

## ⚖️ 7. Marco Legal y Ético

- **Ley N° 29733 (Ley de Protección de Datos Personales del Perú):** Principio de consentimiento previo, expreso e informado; derecho de revocación y protección de identidad académica en el tratamiento de notas y perfiles.
- **Ley Universitaria N° 30220 (Art. 40 - Tutoría y Consejería):** Reconocimiento formal de la mentoría académica entre pares como actividad formativa y solidaria computable para la convalidación de horas de servicio estudiantil ante la Dirección de Escuela de la EPIS-UPT.

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — 2026*
