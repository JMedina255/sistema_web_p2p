# Snapshot de Cierre: Sprint 2

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II) — EPIS, UPT  
**Docente:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Fecha de Congelamiento:** 26/10/2026  
**Commit Git de Referencia:** [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd62) / [`af65fc7`](https://github.com/JMedina255/sistema_web_p2p/commit/af65fc7)  
**Rama Base:** `main`  
**Estado:** ✅ **Cerrado, Verificado y Homologado**

---

## 1. Propósito de este Snapshot

Este directorio constituye un **respaldo inmutable de sólo lectura** que captura con total fidelidad el estado final alcanzado al concluir el **Sprint 2: Roles, Currículo, Perfiles y Gobernanza de Consentimiento Digital (Ley N° 29733)**, así como la base técnica sobre la cual se inicia la transición al Sprint 3.

Permite auditar retrospectivamente:
1. El estado exacto de la documentación técnica y arquitectónica ([`docs/`](file:///d:/sistema_web_p2p/sprints/sprint-02/docs)) en la etapa de diseño de software (SRS v2.2, SAD v2.1, Informe General de Sprint 2 y Catálogo de Evidencias).
2. El código fuente limpio ([`aplicacion/`](file:///d:/sistema_web_p2p/sprints/sprint-02/aplicacion)) con el 100% de sus pruebas automatizadas operativas, libre de dependencias compiladas y caches (`node_modules`, `.venv`, `.pytest_cache`, `.ruff_cache`, `dist`, `coverage`).

---

## 2. Contenido del Respaldo

```text
sprints/sprint-02/
├── SNAPSHOT_INFO.md              # Este archivo de metadatos y auditoría
├── docs/                         # Documentación viva congelada al cierre de Sprint 2
│   ├── analisis/                 # Documentación histórica de la fase de análisis
│   ├── diseño/                   # Documentación prescriptiva de la fase de diseño
│   │   ├── INFORME_GENERAL_SPRINT_01.md
│   │   ├── INFORME_GENERAL_SPRINT_02.md     # Informe maestro exhaustivo de Sprint 2 (1,494 líneas)
│   │   ├── EVIDENCIA_PRUEBAS_SPRINT_01.md
│   │   ├── EVIDENCIA_PRUEBAS_SPRINT_02.md   # Catálogo probatorio de 150 pruebas automatizadas
│   │   ├── FD03-EPIS-Informe SRS de Proyecto.md # SRS actualizado a v2.2
│   │   ├── FD04-EPIS-Informe SAD de Proyecto.md # SAD actualizado a v2.1 con 5 tablas y RLS
│   │   └── imagenes/sprint-02/              # 7 capturas de pantalla reales del sistema
│   ├── sprints/
│   │   ├── PLAN_SPRINTS_Y_TAREAS.md         # Plan maestro de los 5 sprints
│   │   ├── sprint-01.md                     # Bitácora técnica del Sprint 1
│   │   ├── sprint-02.md                     # Bitácora técnica y cierre DoD del Sprint 2
│   │   └── PLANTILLA_INFORME_SPRINT.md      # Plantilla oficial de la cátedra
│   └── diagramas_general.md                 # Bóveda PlantUML con 17 diagramas sobrios
└── aplicacion/                   # Código fuente congelado (limpio de caches y vendors)
    ├── backend/                  # FastAPI, SQLAlchemy 2.0, Alembic, Pytest (84 tests, 90.64% cov)
    │   ├── app/                  # Endpoints REST (consent, roles, profiles, curriculum, auth, health)
    │   ├── scripts/              # Script DDL de políticas RLS para Supabase
    │   └── tests/                # 10 suites de prueba automatizadas
    └── frontend/                 # React 19, TypeScript 5.6, Vite, Vitest (87 tests, >90% cov)
        ├── src/components/       # ConsentModalView, CurriculumCatalogView, ProfileAvailabilityView, OfferPublishView, LoginOtpView
        └── src/services/         # Adaptadores tipados (consentService, profileService, offerService, authService)
```

---

## 3. Métricas de Calidad y Cierre del Sprint 2

| Dimensión de Control | Métrica Obtenida | Umbral / Meta Exigida | Dictamen |
| :--- | :---: | :---: | :---: |
| **Horas ejecutadas** | 14 h (7 h Joan / 7 h Renzo) | 14 horas planificadas | ✅ Cumplido al 100% |
| **Pruebas Backend (Pytest)** | 84 pruebas aprobadas | $\ge 40$ pruebas | ✅ Superado (+44 tests) |
| **Pruebas Frontend (Vitest)** | 87 pruebas aprobadas | $\ge 40$ pruebas | ✅ Superado (+47 tests) |
| **Total Pruebas Automatizadas** | **171 pruebas pasando (100%)** | $\ge 80$ pruebas | ✅ Aprobado con excelencia |
| **Cobertura de Backend** | **90.64%** | $\ge 70\%$ (**RNF09**) | ✅ Superado (+20.64%) |
| **Cobertura de Frontend** | **>90.0%** | $\ge 70\%$ (**RNF09**) | ✅ Superado (+20.0%) |
| **Linteo de Código** | 0 errores (Ruff / ESLint 9) | Cero infracciones de estilo | ✅ Conforme |
| **Compilación Frontend** | Vite bundle generado (`dist/`) | 0 errores de tipado TypeScript | ✅ Conforme |
| **Base de Datos & RLS** | Migración Alembic 002 y RLS en Supabase | `relrowsecurity = True` (5 tablas) | ✅ Conforme |

---

## 4. Trazabilidad de Tareas Culminadas del Sprint 2

* **T-04 (Joan, 2 h):** Formulario modal accesible de consentimiento digital para tratamiento de datos personales conforme a la **Ley N° 29733** y bloqueo preventivo ante rechazo voluntario (**RN-02**).
* **T-05 (Renzo, 1 h):** Tabla `consentimientos_legales`, marcas temporales UTC, persistencia relacional y endpoints `/api/v1/consent/accept` y `/revoke`.
* **T-08 (Renzo, 3 h):** Tabla `usuario_roles`, endpoints de promoción y verificación de mérito académico estricto (**RN-03**): rechazo perentorio con **HTTP 400 `MERIT_RULE_VIOLATION`** si `ciclo_actual < 7`.
* **T-10 (Joan, 2 h):** Interfaz interactiva de consulta avanzada del catálogo curricular con búsqueda por asignaturas, materias críticas y navegación silábica profunda (**CUS21** / **RF05**).
* **T-11 (Joan, 3 h):** Formulario de perfil académico formativo con advertencia preventiva de mérito institucional y grilla interactiva de disponibilidad semanal de **6 días $\times$ 11 franjas horarias** (**CUS15** / **RF04**).
* **T-12 (Renzo, 2 h):** API REST de perfiles y agenda horaria con validaciones de orden temporal estricto (`hora_inicio < hora_fin`), no solapamiento y reemplazo atómico de horarios en base de datos.
* **T-13 (Renzo, 1 h):** Pruebas de seguridad multi-usuario, aislamiento criptográfico Bearer JWT, denegación de autopromoción (**HTTP 403 Forbidden**) y políticas RLS activas en Supabase (**RNF02**).

---
*Fin del registro de snapshot para Sprint 2.*
