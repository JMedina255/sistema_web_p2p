# Plan de Trabajo y Compromisos — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Documento Fuente Oficial:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (v1.2, Secciones 2, 3 y 4.2)  
**Sprint:** 02 — Roles, Currículo, Perfiles y Consentimiento Informado (Ley N° 29733)  
**Semestre Académico:** 2026-II — Cátedra de Construcción de Software I  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo:** Grupo 03 / C-SharkTeam  
- Joan Cristian Medina Quispe (2022074255) — Capacidad: 7 horas  
- Renzo Antonio Antayhua Mamani (2022073504) — Capacidad: 7 horas  
**Periodo Planificado de Trabajo:** 19/10/2026 al 23/10/2026  
**Fecha de Presentación Oficial:** 24/10/2026 (según cronograma del plan maestro)  
**Esfuerzo Total Comprometido:** 14 horas-persona (7 h Joan / 7 h Renzo)  
**Rama Base de Integración:** `feat/sprint-02-roles-curriculo-perfiles`  

---

## 1. Objetivo y Justificación del Sprint 02

El **Sprint 02** tiene como propósito construir las bases de gobernanza legal, control de acceso basado en roles, catalogación académica y captura de disponibilidad horaria que permitirán el funcionamiento confiable del posterior algoritmo de recomendación (*EdRecSys*, Sprint 4).

Aborda cuatro pilares esenciales:
1. **Gobernanza y Protección de Datos:** Implementar el consentimiento informado obligatorio bajo la **Ley N° 29733**, garantizando que ningún dato de estudiantes sea procesado sin autorización explícita (**RF02**, **RN-02**).
2. **Jerarquía y Solvencia Académica:** Establecer una restricción estricta de mérito académico (**RN-03**) que impida que estudiantes de ciclos formativos iniciales ejerzan mentorías, reservando el rol a alumnos de ciclos VII al X (**RF03**).
3. **Normalización Curricular:** Proveer una interfaz interactiva de consulta profunda del catálogo y la malla oficial de la EPIS-UPT, desglosando unidades temáticas silábicas (**RF05**).
4. **Captura de Disponibilidad Semanal:** Diseñar y persistir una matriz semanal interactiva de 6 días por 11 franjas horarias con consistencia transaccional y validación temporal (**RF04**), protegida mediante aislamiento multiusuario con Row Level Security (**RNF02**).

---

## 2. Elementos del Product Backlog Comprometidos (PBIs)

| PBI | Denominación Funcional | Requisitos Asociados | Casos de Uso | Prioridad | Asignación en Sprint |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **PB-003** | Consentimiento digital informado bajo Ley N° 29733 | RF02, RNF02, RN-02 | CUS01 | **P0** (Bloqueante) | Sprint 02 (T-04, T-05) |
| **PB-005** | Gestión y asignación administrativa de roles | RF03, RN-03 | CUS10 | **P0** (Bloqueante) | Sprint 02 (T-08) |
| **PB-006** | Catálogo curricular avanzado y temarios silábicos | RF05 | CUS21 | **P0** | Sprint 01 (base), Sprint 02 (T-10 avanzado) |
| **PB-007** | Perfiles formativos y matriz semanal de disponibilidad | RF04, RNF07 | CUS15 | **P0** | Sprint 02 (T-11, T-12) |
| **PB-008** | Protección y aislamiento multiusuario con RLS | RNF01, RNF02 | CUS01, CUS15 | **P0** | Sprint 01 (base), Sprint 02 (T-13 RLS 5 tablas) |

---

## 3. Desglose de Tareas y Distribución de Carga Horaria

| Tarea | Descripción de la Actividad Técnica | Responsable | Esfuerzo (h) | Entregable Esperado | Criterio de Aceptación |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **T-04** | Desarrollar formulario modal accesible de consentimiento digital. | Joan | 2 | `ConsentModalView.tsx`, `consentService.ts`, tests Vitest. | Modal forzado en primer login; botones claros de aceptación y rechazo; bloqueo de navegación ante rechazo. |
| **T-05** | Implementar persistencia relacional del consentimiento y marcas UTC. | Renzo | 1 | Endpoints `/api/v1/consent`, modelo `ConsentimientoLegal`, tests Pytest. | Registro de IP, User-Agent, versión y timestamp UTC inmutable en BD; verificación de estado previo. |
| **T-08** | Desarrollar endpoints de administración de roles y validación de mérito RN-03. | Renzo | 3 | Endpoints `/api/v1/roles`, modelo `Rol`/`UsuarioRol`, tests Pytest. | Rechazo con **HTTP 400 `MERIT_RULE_VIOLATION`** si `ciclo_actual < 7`; denegación de autopromoción con **HTTP 403 Forbidden**. |
| **T-10** | Implementar interfaz de consulta avanzada del catálogo curricular. | Joan | 2 | `CurriculumCatalogView.tsx`, tests Vitest. | Búsqueda predictiva en tiempo real; filtrado facetado por ciclo (I a X); visualización de unidades temáticas silábicas. |
| **T-11** | Desarrollar formulario de perfil formativo y matriz semanal 6×11 de disponibilidad. | Joan | 3 | `ProfileAvailabilityView.tsx`, `profileService.ts`, tests Vitest. | Grilla interactiva de 6 días $\times$ 11 franjas horarias (08:00 a 19:00); advertencia preventiva de mérito en cliente. |
| **T-12** | Implementar API REST de perfiles y agenda horaria con reemplazo atómico. | Renzo | 2 | Endpoints `/api/v1/profiles`, modelo `PerfilAcademico`/`DisponibilidadHoraria`. | Validación `hora_inicio < hora_fin`; transacción ACID de borrado masivo y recreación sin franjas huérfanas ni solapadas. |
| **T-13** | Ejecutar pruebas de autorización multiusuario y aislar datos con RLS. | Renzo | 1 | `supabase_rls_sprint02.sql`, tests `test_authorization.py`. | 5 tablas con `ROW LEVEL SECURITY` activa en Supabase; cero fugas de datos entre cuentas en suites automatizadas. |
| **Total** | **7 Actividades Oficiales del Sprint 02** | **Equipo** | **14 h** | **Incremento Operativo y 150 Pruebas** | **Cumplimiento al 100% del alcance planificado** |

---

## 4. Criterios de Aceptación del Incremento (Definition of Done)
1. **Lógica de Negocio Verificada:** Reglas **RN-02** y **RN-03** implementadas con rechazo determinista probado en cliente y servidor.
2. **Cobertura Automatizada Superior al Umbral:** Cobertura de código superior al 70% estipulado en **RNF09** tanto en frontend como en backend.
3. **Persistencia Relacional y Seguridad:** Migración Alembic 002 aplicada con claves foráneas, restricciones de integridad y políticas RLS configuradas.
4. **Análisis Estático Limpio:** Cero infracciones de estilo o errores de linteo en Ruff 0.9 y ESLint 9.
5. **Compilación de Producción Exitosa:** Empaquetado de frontend en Vite sin errores de tipado TypeScript (`tsc --noEmit`).
