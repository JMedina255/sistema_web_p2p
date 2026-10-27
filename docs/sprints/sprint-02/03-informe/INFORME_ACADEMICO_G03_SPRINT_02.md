# Informe de Desarrollo y Resultados Académicos — Sprint 02

## «Gobernanza de Consentimiento Digital (Ley N° 29733), Jerarquía de Roles y Mérito Académico, Catálogo Avanzado y Perfiles con Matriz de Disponibilidad Horaria Semanal»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas.  
**Curso:** Construcción de Software I.  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado.  
**Semestre Académico:** 2026-II.  
**Equipo:** Grupo 03 / C-SharkTeam.  
**Integrantes:** Joan Cristian Medina Quispe (Código: 2022074255) y Renzo Antonio Antayhua Mamani (Código: 2022073504).  
**Periodo Planificado:** 19/10/2026 al 23/10/2026.  
**Periodo Real Documentado:** 19/10/2026 al 23/10/2026.  
**Fecha de Presentación Oficial:** 24/10/2026 (según cronograma del plan maestro).  
**Repositorio Oficial:** [https://github.com/JMedina255/sistema_web_p2p](https://github.com/JMedina255/sistema_web_p2p).  
**Rama y Commit Evaluados:** `feat/sprint-02-roles-curriculo-perfiles` / [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74) (Frontend) y [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f) (Backend).  
**Estado del Informe:** Versión final consolidada para evaluación docente de cátedra.  

**Balance del Sprint al Corte:**  
Objetivo logrado en la totalidad del alcance comprometido para el Sprint 02. Se encuentran operativas y verificadas:
1. La gobernanza de consentimiento informado digital bajo el marco legal de la **Ley N° 29733** con persistencia de marca temporal UTC, IP y bloqueo preventivo ante rechazo (**RF02** / **RN-02**).
2. La jerarquía y administración de roles institucionales con verificación estricta de mérito académico restringiendo la tutoría avanzada a estudiantes de ciclo formativo $\ge \text{VII}$ (**RF03** / **CUS10** / **RN-03**) con respuesta **HTTP 400 Bad Request** (`MERIT_RULE_VIOLATION`) y denegación de autopromoción con **HTTP 403 Forbidden**.
3. La consulta interactiva avanzada del catálogo curricular con búsqueda silábica profunda en tiempo real (**RF05** / **CUS21**).
4. La captura estructurada de perfiles formativos y la matriz semanal de disponibilidad horaria de **6 días por 11 franjas** (**RF04** / **CUS15**) con reemplazo atómico transaccional.
5. El aislamiento criptográfico multiusuario garantizado mediante políticas de **Row Level Security (RLS)** en Supabase PostgreSQL (**RNF02**).

Todo el incremento cuenta con una suite consolidada de **150 pruebas automatizadas** (84 en backend y 66 en frontend) con cero fallos y coberturas de **90.64% en backend** y **91.10% en frontend**, superando con holgura el umbral mínimo del 70% estipulado en **RNF09**.

---

### Control de Versiones del Informe

#### Cuadro 0.1: Historial de Versiones del Informe Académico G03

| Versión | Fecha | Responsable | Revisión / Aprobación Registrada | Cambio Realizado |
| :---: | :---: | :--- | :--- | :--- |
| **1.0** | 23/10/2026 | Joan Medina / Renzo Antayhua | Revisión interna Grupo 03 (Sometido a evaluación de cátedra) | Elaboración formal y consolidación del informe del Sprint 02 conforme a la estructura canónica institucional de 11 secciones, integrando evidencias visuales, contratos de API REST, matriz de trazabilidad de PBI, diseño relacional DDL, políticas RLS, batería de 150 pruebas automatizadas y balance técnico de cierre. |
| **2.0** | 26/10/2026 | Joan Medina / Renzo Antayhua | Auditoría de fuentes y estandarización canónica | Reorganización en `docs/sprints/sprint-02/`, depuración de enlaces `file:///`, corrección de códigos de error HTTP (400 vs 403), ajuste de numeración canónica RF04/RF05 y alineación con catálogo oficial de pruebas. |

Fuente: Historial de edición documental del repositorio [sistema_web_p2p](https://github.com/JMedina255/sistema_web_p2p).

---

### Índice de Secciones

1. [Introducción](#1-introducción)
2. [Presentación breve del proyecto](#2-presentación-breve-del-proyecto)
3. [Planificación general de los sprints](#3-planificación-general-de-los-sprints)
4. [Descripción y planificación del sprint informado](#4-descripción-y-planificación-del-sprint-informado)
5. [Desarrollo del sprint y evidencias de verificación](#5-desarrollo-del-sprint-y-evidencias-de-verificación)
6. [Balance de los ítems del Product Backlog](#6-balance-de-los-ítems-del-product-backlog)
7. [Importancia y dependencias del trabajo que continúa](#7-importancia-y-dependencias-del-trabajo-que-continúa)
8. [Conclusiones del sprint](#8-conclusiones-del-sprint)
9. [Recomendaciones para los siguientes sprints](#9-recomendaciones-para-los-siguientes-sprints)
10. [Referencias y documentos de respaldo](#10-referencias-y-documentos-de-respaldo)
11. [Anexos y control de la entrega](#11-anexos-y-control-de-la-entrega)

---

## 1. Introducción

El presente informe formaliza el cierre académico, técnico y metodológico del **Sprint 02** en el marco de la asignatura Construcción de Software I (2026-II). En esta fase del ciclo de vida, el sistema transitó desde la infraestructura base construida en el Sprint 01 hacia la habilitación de los mecanismos centrales de gobernanza de datos personales, jerarquía formativa, catalogación curricular y disponibilidad horaria de los usuarios.

La construcción se desarrolló bajo los lineamientos del Documento de Especificación de Requerimientos de Software ([SRS v2.0/v2.2](../../analisis/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md)) y el Documento de Arquitectura de Software ([SAD v2.1](../../diseño/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md)), garantizando que ninguna funcionalidad implementada carezca de trazabilidad o respaldo en pruebas automatizadas.

---

## 2. Presentación breve del proyecto

### 2.1. Problemática y contexto
En la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna (EPIS-UPT), asignaturas de alta complejidad algorítmica y matemática como *Cálculo I/II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos* registran índices recurrentes de desaprobación y rezago estudiantil. Si bien existen iniciativas informales de tutoría entre pares, la ausencia de una plataforma normalizada dificulta el emparejamiento oportuno, la verificación de la solvencia académica de los mentores y la protección de los datos personales de los estudiantes.

### 2.2. Propósito, usuarios y valor esperado
La plataforma busca estructurar un ecosistema web P2P donde estudiantes de ciclos iniciales (*Mentoreados*, ciclos I a IV) se conecten con estudiantes sobresalientes de ciclos superiores (*Mentores*, ciclos VII a X) mediante un algoritmo de recomendación personalizado (*Top-k*).

Los tres actores del sistema son:
- **Mentoreado:** Estudiante matriculado que busca reforzamiento temático en materias filtro.
- **Mentor:** Estudiante avanzado que brinda orientación formativa acreditando mérito académico.
- **Administrador:** Personal docente o de coordinación que gestiona el catálogo curricular y supervisa las tutorías.

### 2.3. Solución tecnológica y alcance del incremento
La arquitectura se sustenta en una aplicación desacoplada (**RNF09**):
- **Frontend SPA:** Desarrollado con React 19, TypeScript 5.6 y Vite, aplicando Tailwind CSS y pruebas en Vitest.
- **Backend RESTful:** Construido con FastAPI (Python 3.13), esquemas Pydantic v2, ORM SQLAlchemy 2.0 y pruebas en Pytest.
- **Persistencia y Seguridad:** Base de datos relacional PostgreSQL desplegada en Supabase con políticas activas de Row Level Security (RLS).

---

## 3. Planificación general de los sprints

### 3.1. Organización del desarrollo
El proyecto se rige por el **Plan Maestro de 8 Sprints** consolidado en [PLAN_SPRINTS_Y_TAREAS.md](../01-planificacion/PLAN_SPRINT_02.md), con un esfuerzo total planificado de 91 horas-persona distribuidas entre Joan (45 h) y Renzo (46 h).

#### Cuadro 3.1: Calendario Maestro de los 8 Sprints

| Sprint | Fechas de Trabajo | Presentación | Objetivo Central | Joan (h) | Renzo (h) | Total (h) | Estado al Corte |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **S1** | 13–18/10/2026 | 19/10/2026 | Base técnica, acceso OTP institucional y CI | 9.0 | 9.0 | 18.0 | **Culminado** (96 tests) |
| **S2** | 19–23/10/2026 | 24/10/2026 | Roles, currículo, perfiles y consentimiento Ley 29733 | 7.0 | 7.0 | 14.0 | **Culminado** (150 tests) |
| **S3** | 24–25/10/2026 | 26/10/2026 | Publicación de ofertas docentes de mentoría | 2.0 | 3.0 | 5.0 | Siguiente hito |
| **S4** | 26–30/10/2026 | 31/10/2026 | Algoritmo Top-k y reservas transaccionales | 7.5 | 7.5 | 15.0 | Planificado |
| **S5** | 31/10–01/11/2026 | 02/11/2026 | Ratificación T-24h y desistimiento | 2.0 | 3.0 | 5.0 | Planificado |
| **S6** | 02–06/11/2026 | 07/11/2026 | Corte de quórum y bitácora docente | 7.0 | 7.0 | 14.0 | Planificado |
| **S7** | 07–08/11/2026 | 09/11/2026 | Encuestas posmentoría y visado de horas | 3.0 | 2.0 | 5.0 | Planificado |
| **S8** | 09–13/11/2026 | 14/11/2026 | Integración final, constancias PDF y demostración MVP | 7.5 | 7.5 | 15.0 | Planificado |
| **Total** | — | — | **Horizonte Integral de Construcción de Software I** | **45.0** | **46.0** | **91.0** | — |

### 3.2. Relación del sprint actual con los anteriores y posteriores
- **Dependencia de S1:** El Sprint 02 requirió la autenticación institucional y los tokens JWT para vincular las marcas de consentimiento digital y aplicar Row Level Security en la base de datos.
- **Habilitación para S3 y S4:** La agenda semanal de disponibilidad de 6×11 y las asignaturas formativas seleccionadas en el perfil constituyen el insumo indispensable para alimentar el motor de recomendación *EdRecSys v1.0* (Sprint 4) y la programación de ofertas docentes (Sprint 3).

---

## 4. Descripción y planificación del sprint informado

### 4.1. Objetivos del Sprint 02
1. Formalizar el consentimiento informado digital obligatorio bajo la **Ley N° 29733** (**RF02** / **RN-02**).
2. Administrar la asignación institucional de roles aplicando la restricción estricta de mérito académico (**RF03** / **RN-03**).
3. Habilitar la consulta predictiva avanzada del catálogo curricular oficial con temarios silábicos (**RF05** / **CUS21**).
4. Capturar el perfil formativo y la matriz semanal de disponibilidad horaria de 6 días por 11 franjas (**RF04** / **CUS15**).
5. Blindar el aislamiento multiusuario mediante políticas RLS en base de datos PostgreSQL (**RNF02**).

#### Cuadro 4.1: Tareas y Esfuerzo Planificado vs. Ejecutado en Sprint 02

| ID | Actividad Oficial | Responsable | Estimación (h) | Ejecutado (h) | Estado Técnico |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **T-04** | Desarrollar formulario de consentimiento digital accesible | Joan | 2.0 | 2.0 | ✅ Conforme |
| **T-05** | Implementar persistencia relacional del consentimiento y marcas UTC | Renzo | 1.0 | 1.0 | ✅ Conforme |
| **T-08** | Desarrollar endpoints de administración de roles y validación mérito | Renzo | 3.0 | 3.0 | ✅ Conforme |
| **T-10** | Implementar interfaz de consulta avanzada del catálogo curricular | Joan | 2.0 | 2.0 | ✅ Conforme |
| **T-11** | Desarrollar formulario de perfil y matriz semanal 6×11 de disponibilidad | Joan | 3.0 | 3.0 | ✅ Conforme |
| **T-12** | Implementar API REST de perfiles y horarios con reemplazo atómico | Renzo | 2.0 | 2.0 | ✅ Conforme |
| **T-13** | Ejecutar pruebas de autorización multiusuario y aislar con RLS | Renzo | 1.0 | 1.0 | ✅ Conforme |
| **Total** | **7 Tareas Oficiales** | **Equipo** | **14.0 h** | **14.0 h** | **100% Ejecutado** |

---

## 5. Desarrollo del sprint y evidencias de verificación

### 5.1. Consentimiento Informado Digital (Ley N° 29733) — T-04 y T-05
Se implementó un modal forzado en el primer inicio de sesión del usuario. El rechazo voluntario cierra de inmediato la sesión y bloquea la navegación operativa (**RN-02**). La aceptación persiste la versión del texto legal, la dirección IP, el User-Agent y una marca temporal UTC inmutable en la tabla `consentimientos_legales`.

![Figura 5.1: Formulario institucional de consentimiento informado Ley N° 29733](../05-evidencias/capturas/01_consent_modal_ley29733.png)

### 5.2. Exploración Avanzada del Catálogo Curricular — T-10
Interfaz interactiva que permite a estudiantes y mentores filtrar asignaturas por ciclo lectivo (I al X) y realizar búsquedas predictivas por código o nombre de materia, desplegando los temarios silábicos normalizados.

![Figura 5.2: Exploración curricular avanzada con búsqueda temática silábica](../05-evidencias/capturas/02_curriculum_advanced_search.png)

### 5.3. Validación de Mérito Académico (RN-03) y Administración de Roles — T-08
Se implementó una arquitectura de validación en dos niveles (Defensa en Profundidad):
1. **Validación Reactiva en Cliente:** Advertencia visual preventiva si el estudiante indica un ciclo formativo inferior al VII.
2. **Validación Coercitiva en Servidor:** Si una solicitud de elevación a mentor proviene de un alumno con `ciclo_actual < 7`, el backend responde **HTTP 400 Bad Request** con payload `{"code": "MERIT_RULE_VIOLATION"}`. Si intenta autopromoverse sin privilegios de administrador, se deniega con **HTTP 403 Forbidden**.

![Figura 5.3: Validación reactiva de mérito institucional para postulantes a mentor](../05-evidencias/capturas/03_profile_merit_validation.png)

### 5.4. Perfiles Formativos y Matriz Semanal de Disponibilidad (6×11) — T-11 y T-12
Grilla interactiva que cubre 6 días lectivos (Lunes a Sábado) y 11 franjas horarias (08:00 a 19:00). La actualización en backend se ejecuta mediante una transacción ACID que efectúa el borrado previo y la inserción masiva atómica de franjas, previniendo estados inconsistentes o solapamientos (**RNF07**).

![Figura 5.4: Grilla semanal interactiva de disponibilidad horaria 6×11](../05-evidencias/capturas/04_weekly_availability_grid.png)

### 5.5. Contratos de Interfaces RESTful y Documentación OpenAPI
Los endpoints implementados en `/api/v1/consent`, `/api/v1/roles` y `/api/v1/profiles` se encuentran documentados interactivamente bajo Swagger UI / OpenAPI v3, con esquemas fuertemente tipados en Pydantic v2.

![Figura 5.5: Documentación interactiva OpenAPI de los endpoints del Sprint 02](../05-evidencias/capturas/05_swagger_api_docs_sprint02.png)

### 5.6. Aseguramiento de Calidad y Pruebas Automatizadas
Al corte del Sprint 02, se consolidaron **150 pruebas automatizadas**:
- **Backend (Pytest):** 84 pruebas pasando al 100%, con **90.64% de cobertura**.
- **Frontend (Vitest):** 66 pruebas pasando al 100%, con **91.10% de cobertura**.

![Figura 5.6: Cobertura de pruebas automatizadas en Backend (Pytest-Cov)](../05-evidencias/capturas/06_backend_pytest_coverage_sprint02.png)

![Figura 5.7: Cobertura de pruebas automatizadas en Frontend (Vitest)](../05-evidencias/capturas/07_frontend_vitest_coverage_sprint02.png)

---

## 6. Balance de los ítems del Product Backlog

| PBI | Estado al Inicio de S2 | Estado al Cierre de S2 | Justificación del Dictamen Técnico |
| :---: | :---: | :---: | :--- |
| **PB-003** | No iniciado | **100% Concluido** ✅ | Modal accesible operativo, persistencia de auditoría y 19 pruebas vinculadas. |
| **PB-005** | No iniciado | **100% Concluido** ✅ | Verificación estricta de mérito RN-03, HTTP 400 documentado y 12 pruebas Pytest. |
| **PB-006** | Base en S1 | **100% Concluido** ✅ | Buscador predictivo en tiempo real y temarios silábicos con 14 pruebas. |
| **PB-007** | No iniciado | **100% Concluido** ✅ | Perfil formativo y grilla semanal 6×11 con reemplazo atómico y 34 pruebas. |
| **PB-008** | Base en S1 | **100% Concluido** ✅ | RLS activo en 5 tablas de base de datos y 11 pruebas de aislamiento superadas. |

---

## 7. Importancia y dependencias del trabajo que continúa

El incremento del Sprint 02 habilita directamente las siguientes capacidades críticas para el Sprint 03 y Sprint 04:
1. **Publicación de Ofertas Docentes (Sprint 03, T-14 a T-18):** Los mentores verificados bajo RN-03 pueden publicar sesiones utilizando las asignaturas normalizadas en T-10.
2. **Motor de Recomendación Algorítmica EdRecSys (Sprint 04, T-15):** La matriz horaria semanal de 6×11 y las materias seleccionadas constituyen el vector de características del estudiante para calcular la compatibilidad horaria y temática (*Jaccard / Similitud Coseno*).

---

## 8. Conclusiones del sprint

1. **Gobernanza de Datos:** Se implementaron los controles técnicos necesarios para el consentimiento informado conforme a los principios de la Ley N° 29733, garantizando trazabilidad y bloqueo por rechazo.
2. **Garantía Institucional de Mérito:** La restricción RN-03 asegura la credibilidad académica del modelo P2P, reservando la tutoría a estudiantes con suficiente madurez formativa ($\ge \text{VII}$ ciclo).
3. **Consistencia Transaccional:** La disponibilidad horaria semanal opera bajo transacciones atómicas seguras (**RNF07**), eliminando franjas huérfanas o duplicadas.
4. **Seguridad Multi-Inquilino:** Las políticas RLS en Supabase y el aislamiento por token Bearer JWT previenen eficazmente la alteración o fuga de datos entre usuarios (**RNF02**).
5. **Calidad y Madurez del Código:** La suite de 150 pruebas automatizadas con coberturas superiores al 90% en ambas capas certifica la estabilidad y robustez del software entregado (**RNF09**).

---

## 9. Recomendaciones para los siguientes sprints

1. **Reutilización de Validaciones Reactivas:** Aprovechar la experiencia del validador de mérito para programar las reglas RN-04 (antelación mínima en publicación de ofertas) y RN-05 (control inmutable de aforo) en el Sprint 03.
2. **Optimización de Índices de Base de Datos:** Crear índices compuestos en `disponibilidades_horarias` sobre las columnas `(email, dia_semana)` para acelerar las consultas vectoriales de emparejamiento algorítmico en el Sprint 04.

---

## 10. Referencias y documentos de respaldo

1. Congreso de la República del Perú. (2011). *Ley N° 29733: Ley de Protección de Datos Personales*. Diario Oficial El Peruano.
2. Ministerio de Justicia y Derechos Humanos. (2013). *Reglamento de la Ley N° 29733 (D.S. N° 003-2013-JUS)*.
3. Congreso de la República del Perú. (2014). *Ley Universitaria N° 30220 (Artículo 40: Tutoría y asesoría)*.
4. IEEE Computer Society. (1998). *IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications*.
5. Kruchten, P. (1995). *Architectural Blueprints — The "4+1" View Model of Software Architecture*. IEEE Software, 12(6), 42-50.
6. Documentos Oficiales en Repositorio GitHub:
   - [SRS v2.0 / v2.2](../../analisis/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md).
   - [SAD v2.1](../../diseño/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md).
   - [Matriz Oficial de Trazabilidad](../02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md).
   - [Matriz de Pruebas](../06-pruebas/MATRIZ_PRUEBAS_CATALOGO_OFICIAL.md).

---

## 11. Anexos y control de la entrega

### 11.1. Índice de evidencias visuales
- **Figura 5.1:** Formulario institucional de consentimiento informado Ley N° 29733 (`01_consent_modal_ley29733.png`).
- **Figura 5.2:** Exploración curricular avanzada con búsqueda temática silábica (`02_curriculum_advanced_search.png`).
- **Figura 5.3:** Validación reactiva de mérito institucional para postulantes a mentor (`03_profile_merit_validation.png`).
- **Figura 5.4:** Grilla semanal interactiva de disponibilidad horaria 6×11 (`04_weekly_availability_grid.png`).
- **Figura 5.5:** Documentación interactiva OpenAPI de los endpoints del Sprint 02 (`05_swagger_api_docs_sprint02.png`).
- **Figura 5.6:** Reporte de cobertura de backend alcanzando 90.64% con Pytest-Cov (`06_backend_pytest_coverage_sprint02.png`).
- **Figura 5.7:** Reporte de cobertura de frontend alcanzando 91.10% con Vitest (`07_frontend_vitest_coverage_sprint02.png`).

### 11.2. Material complementario del repositorio
- Script de migración relacional: `aplicacion/backend/app/db/migrations/versions/002_roles_and_profiles.py`.
- Script DDL de políticas RLS: `aplicacion/backend/scripts/supabase_rls_sprint02.sql`.
- Guion de exposición corregido: `docs/sprints/sprint-02/04-presentacion/GUION_EXPOSICION_CORREGIDO.md`.

---
*Informe académico elaborado por el Grupo 03 para la Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna (2026).*
