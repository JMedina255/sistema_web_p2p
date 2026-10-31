# Bitácora Oficial de Ejecución y Cierre DoD — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Sprint:** 02 — Roles, Currículo, Perfiles y Consentimiento Informado (Ley N° 29733)  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Rama de Trabajo:** `feat/sprint-02-roles-curriculo-perfiles`  
**Fecha de Cierre Técnico:** 23/10/2026  
**Commits de Consolidación:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74) (Frontend Joan) y [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f) (Backend Renzo)  

---

## 1. Bitácora Cronológica de Ejecución Técnica

### Sesión 1: 19/10/2026 — Apertura del Sprint 02 y Modelado de Base de Datos
- **Actividades de Renzo:**
  - Análisis del Diccionario Físico de Datos del SAD FD04 para las 5 tablas de S2 (`consentimientos_legales`, `roles`, `usuario_roles`, `perfiles_academicos`, `disponibilidades_horarias`).
  - Creación de la migración Alembic `002_roles_and_profiles.py` con restricciones `CHECK` (`ciclo_actual BETWEEN 1 AND 10`, `dia_semana BETWEEN 1 AND 6`).
  - Redacción del script DDL de políticas Row Level Security `supabase_rls_sprint02.sql`.
- **Actividades de Joan:**
  - Diseño de la arquitectura de componentes funcionales en React para el modal de consentimiento (`ConsentModalView.tsx`) y servicio tipado `consentService.ts`.
  - Definición de los estados locales de consentimiento (`PENDING`, `ACCEPTED`, `REJECTED`).

### Sesión 2: 21/10/2026 — Lógica de Negocio y Reglas Institucionales
- **Actividades de Renzo:**
  - Implementación de `consent_service.py` con endpoints `POST /consent` y `GET /consent/history`.
  - Implementación de `role_service.py` con verificación estricta de mérito académico (**RN-03**): rechazo determinista con **HTTP 400 Bad Request** (`MERIT_RULE_VIOLATION`) si `ciclo_actual < 7`.
  - Implementación de control de autopromoción en `/api/v1/roles`: denegación con **HTTP 403 Forbidden** para usuarios sin credenciales de administrador.
- **Actividades de Joan:**
  - Desarrollo de `CurriculumCatalogView.tsx` con búsqueda predictiva por texto y filtrado por ciclo lectivo.
  - Maquetación y desarrollo interactivo de la grilla semanal de disponibilidad de 6 días por 11 franjas horarias (`ProfileAvailabilityView.tsx`), incorporando advertencia reactiva de mérito en cliente.

### Sesión 3: 23/10/2026 — Transaccionalidad, Seguridad Multi-Usuario y Pruebas Automatizadas
- **Actividades de Renzo:**
  - Implementación de `profile_service.py` con lógica de reemplazo atómico transaccional de franjas horarias: `db.delete(franjas_anteriores)` + `db.bulk_save_objects(nuevas_franjas)` dentro del mismo bloque de transacción.
  - Creación y ejecución de 84 pruebas automatizadas en Pytest (`test_consent.py`, `test_roles.py`, `test_profiles.py`, `test_authorization.py`). Cobertura lograda: **90.64%**.
- **Actividades de Joan:**
  - Creación y ejecución de 66 pruebas automatizadas en Vitest (`ConsentModalView.test.tsx`, `CurriculumCatalogView.test.tsx`, `ProfileAvailabilityView.test.tsx`, servicios tipados). Cobertura lograda: **91.10%**.
  - Commit de consolidación frontend [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74).
  - Commit de consolidación backend y diseño [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f).

---

## 2. Evaluación de Criterios de Aceptación (Definition of Done — DoD)

| Criterio DoD Oficial | Estado Técnico | Evidencia Verificable |
| :--- | :---: | :--- |
| **1. Código implementado conforme a la arquitectura SAD FD04** | **Cumplido** ✅ | Estructura en capas en `aplicacion/`: endpoints v1, servicios desacoplados, modelos ORM SQLAlchemy 2.0 y esquemas Pydantic v2. |
| **2. Pruebas automatizadas aprobadas al 100%** | **Cumplido** ✅ | 150 pruebas pasando (84 en Pytest y 66 en Vitest), 0 fallos. |
| **3. Cobertura de código superior al 70% (RNF09)** | **Cumplido** ✅ | Backend: **90.64%** (+20.64%). Frontend: **91.10%** (+21.10%). Reportes visuales capturados en `05-evidencias/capturas/`. |
| **4. Integridad de reglas de negocio institucionales** | **Cumplido** ✅ | **RN-02:** Modal legal con bloqueo forzado probado.<br>**RN-03:** Rechazo HTTP 400 Bad Request probado en `test_roles.py` y advertencia en `ProfileAvailabilityView.tsx`. |
| **5. Consistencia y transaccionalidad de datos (RNF07)** | **Cumplido** ✅ | Reemplazo atómico de horarios en `profile_service.py` verificado sin registros huérfanos. |
| **6. Seguridad multiusuario y aislamiento RLS (RNF02)** | **Cumplido** ✅ | 11 pruebas de aislamiento en `test_authorization.py`; script `supabase_rls_sprint02.sql` con políticas por usuario activo. |
| **7. Linteo y análisis estático sin errores** | **Cumplido** ✅ | Ruff 0.9 y ESLint 9 ejecutados sin infracciones ni advertencias. |
| **8. Trazabilidad completa hacia SRS y SAD** | **Cumplido** ✅ | Matriz de 12 eslabones canónicos documentada en `docs/sprints/sprint-02/02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md`. |

---

## 3. Dictamen de Cierre del Sprint 02
El equipo declara el **Sprint 02 como 100% completado, verificado y cerrado satisfactoriamente**, quedando la base operativa y documental plenamente consolidada para la transición hacia el Sprint 03.
