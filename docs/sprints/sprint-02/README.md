# Paquete Canónico de Entrega, Trazabilidad y Exposición — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo:** Grupo 03 / C-SharkTeam  
- Joan Cristian Medina Quispe (Código: 2022074255) — Rol: Frontend Architecture, UI & CI  
- Renzo Antonio Antayhua Mamani (Código: 2022073504) — Rol: Backend, Persistencia ORM & RLS  
**Periodo Planificado y Ejecutado:** 19/10/2026 al 23/10/2026  
**Fecha de Presentación Oficial:** 24/10/2026 (según cronograma del plan maestro)  
**Commits de Consolidación:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74) (Frontend) y [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f) (Backend)  
**Estado de la Entrega:** ✅ **100% Concluido, Verificado y Homologado en CI**

---

## 📌 1. Objetivo y Alcance del Sprint 02

El **Sprint 02** tuvo como objetivo consolidar las bases funcionales, de gobernanza y de persistencia necesarias para operar el modelo de mentoría entre pares de la EPIS-UPT, habilitando:
1. **Consentimiento Informado Digital (Ley N° 29733):** Formalización técnica del consentimiento obligatorio en primer inicio de sesión con persistencia inmutable de marca temporal UTC, IP y bloqueo preventivo ante rechazo voluntario (**RF02** / **RN-02**).
2. **Jerarquía Institucional y Mérito Académico:** Asignación de roles con validación estricta de mérito formativo (**RN-03**), restringiendo la postulación al rol de Mentor a estudiantes de ciclo formativo $\ge \text{VII}$ (**RF03** / **CUS10**) con respuesta **HTTP 400 Bad Request** (`MERIT_RULE_VIOLATION`) y denegación de autopromoción con **HTTP 403 Forbidden**.
3. **Catálogo Curricular Avanzado:** Consulta interactiva de asignaturas críticas de la EPIS con búsqueda predictiva en tiempo real y temarios silábicos oficiales (**RF05** / **CUS21**).
4. **Perfil Formativo y Matriz Semanal de Disponibilidad (6×11):** Configuración de asignaturas de interés y marcado de 66 franjas horarias (6 días × 11 bloques) con reemplazo atómico transaccional ACID en base de datos (**RF04** / **CUS15**).
5. **Seguridad Multi-Usuario (RLS):** Aislamiento criptográfico de expedientes mediante tokens Bearer JWT y políticas activas de Row Level Security en Supabase PostgreSQL (**RNF02**).

---

## 🗂️ 2. Índice Canónico de Entregables del Sprint 02

El presente directorio estructura de forma autónoma, portable y sin duplicidades contradictorias los 9 entregables oficiales exigidos para la evaluación docente y defensa formal:

```text
docs/sprints/sprint-02/
├── README.md                                  # Este documento maestro de navegación y auditoría
├── 01-planificacion/                          # Plan operativo, distribución horaria y bitácora
│   ├── PLAN_SPRINT_02.md                      # Plan detallado: 5 PBIs, 7 tareas y 14 h de esfuerzo
│   └── BITACORA_EJECUCION_SPRINT_02.md        # Bitácora cronológica de sesiones y evaluación DoD
├── 02-trazabilidad/                           # Auditoría de trazabilidad y gestión de consistencia
│   ├── MATRIZ_TRAZABILIDAD_SPRINT_02.md       # Matriz oficial de 12 eslabones canónicos
│   └── REGISTRO_INCONSISTENCIAS_SPRINT_02.md  # Registro detallado de inconsistencias y correcciones
├── 03-informe/                                # Informes académicos para evaluación de cátedra
│   ├── INFORME_ACADEMICO_G03_SPRINT_02.md     # Informe formal de 11 secciones (formato oficial UPT)
│   └── INFORME_GENERAL_TECNICO_SPRINT_02.md   # Reporte maestro exhaustivo de 1,494 líneas
├── 04-presentacion/                           # Material formal para exposición y defensa técnica
│   ├── PRESENTACION_OFICIAL_SPRINT_02.pptx    # Presentación editable 16:9 con evidencias reales
│   ├── PRESENTACION_OFICIAL_SPRINT_02.pdf     # Presentación exportada a PDF de alta resolución
│   └── GUION_EXPOSICION_CORREGIDO.md          # Guion técnico para expositor, demo y preguntas
├── 05-evidencias/                             # Evidencias visuales auténticas del repositorio
│   ├── capturas/                              # 7 capturas de pantalla reales del sistema
│   │   ├── 01_consent_modal_ley29733.png
│   │   ├── 02_curriculum_advanced_search.png
│   │   ├── 03_profile_merit_validation.png
│   │   ├── 04_weekly_availability_grid.png
│   │   ├── 05_swagger_api_docs_sprint02.png
│   │   ├── 06_backend_pytest_coverage_sprint02.png
│   │   ├── 07_frontend_vitest_coverage_sprint02.png
│   │   └── INDICE_CAPTURAS.md
│   └── diagramas/                             # 7 diagramas oficiales de análisis y arquitectura
│       ├── 08_diagrama_casos_de_uso_sprint02.png (.svg)
│       ├── 09_secuencia_consentimiento_ley29733.png (.svg)
│       ├── 10_secuencia_roles_merito_rn03.png (.svg)
│       ├── 11_secuencia_perfil_disponibilidad_atomic.png (.svg)
│       ├── 12_secuencia_seguridad_multiusuario_rls.png (.svg)
│       ├── 13_maquina_estados_consentimiento_roles.png (.svg)
│       ├── 14_diagrama_entidad_relacion_sprint02.png (.svg)
│       └── INDICE_DIAGRAMAS.md
├── 06-pruebas/                                # Pruebas y homologación con catálogo institucional
│   ├── MATRIZ_PRUEBAS_CATALOGO_OFICIAL.md     # Mapeo con casos Excel CUS01, CUS10, CUS15, CUS21
│   └── EVIDENCIA_PRUEBAS_AUTOMATIZADAS.md     # Desglose de 150 pruebas y coberturas (>90%)
└── 07-actas/                                  # Cierre formal y compromisos éticos
    └── ACTA_CIERRE_SPRINT_02.md               # Acta suscrita por el equipo y declaración de alcance
```

---

## 📖 3. Documentos Fuente y Precedencia Metodológica

En caso de discrepancia, rige el principio de precedencia documental:
$$\text{Requisitos Aprobados (SRS)} \succ \text{Decisiones Arquitectónicas Vigentes (SAD)} \succ \text{Plan Maestro de Sprints} \succ \text{Código y Pruebas} \succ \text{Materiales de Exposición}$$

| Documento Fuente Maestro | Ubicación Canónica | Versión Vigente | Rol en el Proyecto |
| :--- | :--- | :---: | :--- |
| **SRS (Informe de Requerimientos)** | [`docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md`](../../analisis/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md) | **v2.0 / v2.2** | Fuente principal de Requerimientos Funcionales (RF), No Funcionales (RNF), Reglas de Negocio (RN) y Narrativas de Casos de Uso. |
| **SAD (Informe de Arquitectura)** | [`docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md`](../../diseño/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md) | **v2.1** | Fuente principal de Vistas 4+1, Contratos OpenAPI, Diccionario de Datos, Diagramas de Secuencia y Políticas RLS. |
| **Plan de Sprints y Backlog** | [`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`](../PLAN_SPRINTS_Y_TAREAS.md) | **v1.2** | Plan Maestro oficial de 8 Sprints, Product Backlog de 37 PBI y distribución horaria del equipo. |
| **Catálogo de Pruebas** | [`docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`](../../analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) | **v1.0** | Catálogo oficial de casos de prueba del sistema para homologación de pruebas automatizadas. |
| **Snapshot Histórico Sprint 2** | [`sprints/sprint-02/`](../../../sprints/sprint-02/) | **Congelado** | Respaldo inmutable de sólo lectura capturado al cierre del sprint para auditoría retrospectiva. |

---

## 🔗 4. Matriz Resumida de Trazabilidad del Sprint 02

| PBI | Tareas | Requisito | Regla | Historia | Caso de Uso | Componente Clave | Pruebas Automatizadas | Evidencia |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **PB-003** | T-04, T-05 | **RF02** | **RN-02** | **HU-03** | **CUS01** | `ConsentModalView.tsx`, `consent.py` | 19 tests (14 Pytest / 5 Vitest) | Captura 01, Diag 09 |
| **PB-005** | T-08 | **RF03** | **RN-03** | **HU-04** | **CUS10** | `roles.py`, `role_service.py` | 12 tests (HTTP 400 mérito / 403 autoprom.) | Captura 03, Diag 10 |
| **PB-006** | T-10 | **RF05** | Malla EPIS | **HU-05** | **CUS21** | `CurriculumCatalogView.tsx`, `curriculum.py` | 14 tests (Búsqueda predictiva/Filtros) | Captura 02, Diag 14 |
| **PB-007** | T-11, T-12 | **RF04** | 6×11 ACID | **HU-06** | **CUS15** | `ProfileAvailabilityView.tsx`, `profiles.py` | 34 tests (CRUD / Atomic DELETE+INSERT) | Captura 04, Diag 11 |
| **PB-008** | T-13 | **RNF02** | RLS / Ley 29733 | **HU-07** | **CUS01/15** | `supabase_rls_sprint02.sql`, Bearer JWT | 11 tests de aislamiento multiusuario | Diag 12, Captura 06 |

---

## 🧪 5. Verificación, Pruebas y Calidad de Software

Al corte del Sprint 02 (commit `3766a08` / `786dd62`), el incremento cuenta con **150 pruebas automatizadas acumuladas**, 100% aprobadas y 0 fallos:
- **Backend (Pytest 9.1):** 84 pruebas superadas | **90.64% de cobertura** (Superávit de +20.64% sobre **RNF09**).
- **Frontend (Vitest 2.1):** 66 pruebas superadas | **91.10% de cobertura** (Superávit de +21.10% sobre **RNF09**).
- **Análisis Estático:** 0 errores de linteo en Ruff 0.9 y ESLint 9.
- **Compilación de Producción:** Vite bundle limpio (`dist/`) sin errores de tipado TypeScript (`tsc --noEmit`).

Para ejecutar las comprobaciones de manera reproducible:
```bash
# Backend (84 pruebas)
cd aplicacion/backend && pytest tests/test_consent.py tests/test_roles.py tests/test_profiles.py tests/test_authorization.py tests/test_curriculum.py tests/test_auth.py tests/test_health.py --cov=app

# Frontend (66 pruebas)
cd aplicacion/frontend && npm test -- --run --coverage
```

---

## ⚖️ 6. Declaración de Limitaciones Técnicas y Ética Académica
1. **Tratamiento de la Ley N° 29733:** El sistema implementa los controles técnicos de consentimiento informado y auditoría; no obstante, el equipo declara que no constituye una certificación legal emitida por la Dirección General de Protección de Datos Personales (ANPDS).
2. **Evaluación de Cátedra:** La documentación se somete a consideración y calificación del docente de cátedra, Dr. Ricardo Eduardo Valcárcel Alvarado, sin asumir aprobaciones tácitas institucionales.
