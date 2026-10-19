# Plan de sprints y distribución de tareas — Sistema Web P2P

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.  
**Repositorio de implementación:** https://github.com/JMedina255/sistema_web_p2p  
**Equipo:** Grupo 03 — Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani.  
**Versión:** 1.0 — 19/10/2026.  
**Ubicación prevista:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`.  
**Tipo:** contexto operativo para el equipo y el agente de IDE; no es un reporte de ejecución.

> **Alcance activo:** Sprint 1, tareas de Joan **T-01, T-02 y T-06**, mediante cuatro hitos y sus commits. Las tareas de Renzo y los sprints posteriores se incluyen como contexto y dependencias. No implementarlos automáticamente. Ejecutar únicamente el hito solicitado y detenerse al terminarlo.

## 1. Cómo utilizar este documento

Antes de implementar un hito, el agente debe leer este archivo y revisar el estado real del repositorio. Las asignaciones y horas provienen de la planificación académica vigente; las instrucciones de implementación del Sprint 1 concretan lo acordado con Joan.

1. Revisar `git status`, rama actual, `README.md` y cualquier `AGENTS.md` aplicable.
2. Leer `reglas_documentacion.md`, `rules_doc.md`, `docs/FD03-EPIS-Informe SRS de Proyecto.md` y `docs/FD04-EPIS-Informe SAD de Proyecto.md`. Si una ruta cambió, localizar el documento antes de asumir que falta.
3. Conservar los cambios locales existentes. Trabajar en `feat/sprint-01-base-acceso-ci`; si existe, reutilizarla sin borrar trabajo ni reescribir historial.
4. Crear el desarrollo en `aplicacion/`. Mantener `frontend/` como maqueta de referencia visual y reutilizar componentes útiles sin alterarla innecesariamente.
5. Implementar el hito solicitado, ejecutar sus comprobaciones y actualizar `README.md` y `docs/sprints/sprint-01.md` con resultados reales.
6. Revisar el diff y crear el commit del hito cuando sus comprobaciones disponibles pasen. Incluir solo sus archivos; excluir secretos, entornos y archivos generados.
7. Informar archivos relevantes, comprobaciones, resultado, pendientes y hash del commit. Detenerse antes de comenzar el siguiente hito.

**Fuentes y discrepancias:** la planificación vigente determina sprints, responsables y horas; el SRS define requisitos y reglas de negocio; el SAD orienta la estructura técnica. Este documento no sustituye esas fuentes. Registrar discrepancias y brechas sin renumerar requisitos ni declarar cumplimiento integral de una funcionalidad parcial. Las referencias antiguas a una fase de análisis no impiden el desarrollo del Sprint 1 solicitado por el usuario.

**Convenciones:** `PB-xxx` identifica un PBI (elemento del Product Backlog); `T-xx`, una tarea; `RFxx`, un requisito funcional; `RNFxx`, uno no funcional; `CUSxx`, un caso de uso; `RN-xx`, una regla de negocio. Las tareas conservan sus IDs originales aunque no sean consecutivas dentro de un sprint. No asignar cargos de Product Owner o Scrum Master: no están definidos en la fuente revisada.

## 2. Alcance y capacidad de la planificación

El producto contempla mentoreados, mentores y administradores. La demostración final busca recorrer: acceso, publicación de oferta, recomendación Top-k inicial, reserva, ratificación, corte de quórum, bitácora, encuesta, visado de horas y constancia PDF marcada **DEMO**.

- Línea base: 26 RF, 10 RNF, 24 CUS y 37 PBI.
- Horizonte: ocho presentaciones con ventanas de trabajo desiguales; no son sprints de duración uniforme.
- Disponibilidad: 14 horas semanales por integrante; 128 horas-persona brutas en la ventana del plan.
- Capacidad neta: 96 horas-persona con un factor de foco provisional del 75%.
- Asignación: 91 horas-persona — Joan 45 y Renzo 46 — y reserva de 5 horas.
- Las 51 tareas tienen una reestimación de 150 h optimistas, 199 h probables, 209,7 h PERT y 312 h pesimistas. Las 416 h del backlog integral corresponden a otra profundidad de alcance y no se suman a estas cifras.

El plan de 91 h es reducido y optimista. Reestimar después del Sprint 1 con tiempos reales y registrar cambios de alcance. Las fechas siguientes son las fechas planificadas de 2026: no prueban que un sprint haya comenzado o terminado ni deben desplazarse automáticamente.

La distribución siguiente permite identificar el orden de entrega y la carga de cada integrante.

### Cuadro 2.1. Calendario y esfuerzo por sprint

| Sprint | Trabajo previsto | Presentación | Objetivo | Joan (h) | Renzo (h) | Total (h) |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: |
| S1 | 13–18/10/2026 | 19/10/2026 | Base técnica y acceso inicial | 9 | 9 | 18 |
| S2 | 19–23/10/2026 | 24/10/2026 | Roles, currículo y perfiles | 7 | 7 | 14 |
| S3 | 24–25/10/2026 | 26/10/2026 | Publicación de ofertas | 2 | 3 | 5 |
| S4 | 26–30/10/2026 | 31/10/2026 | Top-k y reservas | 7,5 | 7,5 | 15 |
| S5 | 31/10–01/11/2026 | 02/11/2026 | Ratificación y desistimiento | 2 | 3 | 5 |
| S6 | 02–06/11/2026 | 07/11/2026 | Quórum y bitácoras | 7 | 7 | 14 |
| S7 | 07–08/11/2026 | 09/11/2026 | Encuestas y visado de horas | 3 | 2 | 5 |
| S8 | 09–13/11/2026 | 14/11/2026 | Integración y demostración | 7,5 | 7,5 | 15 |
| **Total** | | | | **45** | **46** | **91** |

Fuente: planificación vigente, tablas 5.1 y 5.10.

S1, S4 y S8 consumen toda su capacidad neta prevista. Los demás sprints disponen de una hora de reserva cada uno. Las horas son estimaciones, no tiempos registrados ni puntos de historia.

## 3. Product Backlog de referencia

La tabla conserva los 37 PBI y su trazabilidad resumida. La columna de sprint indica el compromiso parcial del plan; «Posterior» significa que el PBI permanece en el backlog sin asignación explícita a los ocho incrementos.

### Cuadro 3.1. PBI, requisitos y asignación planificada

| PBI | Funcionalidad | RF / RNF y CUS | Prioridad | Sprint |
| :--- | :--- | :--- | :---: | :--- |
| PB-001 | Entorno ejecutable | Transversal | P0 | S1 |
| PB-002 | Autenticación OTP | RF01 · CUS01 | P0 | S1 |
| PB-003 | Consentimiento digital | RF02 · CUS01 | P0 | S2 |
| PB-004 | CI y validación inicial | RNF09 | P0 | S1 |
| PB-005 | Gestión de roles | RF03 · CUS10 | P0 | S2 |
| PB-006 | Catálogo curricular | RF05 · CUS21 | P0 | S1, S2 |
| PB-007 | Perfiles y disponibilidad | RF04 · CUS15 | P0 | S2 |
| PB-008 | Protección RLS | RNF02 | P0 | S1, S2 |
| PB-009 | Publicar ofertas | RF08 · CUS06 | P0 | S3 |
| PB-010 | Top-k inicial | RF06 · CUS02 | P0 | S4 |
| PB-011 | Feed de recomendaciones | RF06 · CUS02 | P0 | S4 |
| PB-012 | Solicitudes por demanda | RF07 · CUS03 | P1 | Posterior |
| PB-013 | Reserva transaccional | RF12 · CUS04 | P0 | S4 |
| PB-014 | Ratificar T-24h | RF13 · CUS24 | P0 | S5 |
| PB-015 | Desistir de reserva | RF14 · CUS17 | P0 | S5 |
| PB-016 | Reprogramar o cancelar | RF11 · CUS18 | P1 | Posterior |
| PB-017 | Corte de quórum | RF15 · CUS23 | P0 | S6 |
| PB-018 | Decisión ante quórum bajo | RF16 · CUS07 | P0 | S6 |
| PB-019 | Bitácora y asistencia | RF17 · CUS08 | P0 | S6 |
| PB-020 | Encuesta posmentoría | RF18 · CUS05 | P0 | S7 |
| PB-021 | Historial de sesiones | RF19 · CUS19 | P1 | Posterior |
| PB-022 | Recursos educativos | RF20 · CUS20 | P1 | Posterior |
| PB-023 | Visado de horas | RF26 · CUS22 | P0 | S7 |
| PB-024 | Constancia PDF | RF22 · CUS13 | P0 | S8 |
| PB-025 | Verificación QR del certificado | RF23 · CUS09 | P0 | Posterior |
| PB-026 | Reputación e insignias | RF21 · CUS16 | P1 | Posterior |
| PB-027 | Precision@k | RF06 · RNF03 | P0 | S8 |
| PB-028 | Modelo híbrido | RF06 · CUS02 | P1 | Posterior |
| PB-029 | Prioridad institucional | RF24 · CUS12 | P1 | Posterior |
| PB-030 | Analíticas institucionales | RF25 · CUS14 | P1 | Posterior |
| PB-031 | Cobertura de pruebas | RNF09 | P0 | Posterior; avance parcial en T-06 |
| PB-032 | Parser de horarios | RF10 · CUS11 | P1 | Posterior |
| PB-033 | Asignación de aulas | RF09 · CUS06 | P1 | Posterior |
| PB-034 | Meet/Discord automático | RF09 · CUS06 | P1 | Posterior |
| PB-035 | Pruebas de carga y seguridad | RNF02/03/07/10 | P0 | Posterior |
| PB-036 | Usabilidad y navegadores | RNF04/05/08 | P1 | Posterior; exploración parcial en T-49 |
| PB-037 | Pruebas E2E y cierre | RNF06/09/10 | P0 | S8 |

Fuente: planificación vigente, tabla 4.1 y apartados 5.1–5.8. Las notas de avance parcial vinculan las tareas previstas sin ampliar el compromiso original.

P0 identifica fundamentos y flujo crítico; P1, ampliaciones. Una prioridad alta no significa que el alcance integral esté comprometido en estas 91 horas. No marcar un PBI completo por disponer de una pantalla o un mock.

## 4. Tareas de los ocho sprints

### 4.1. Sprint 1 — Base técnica y acceso inicial

**Objetivo:** comunicar React, FastAPI y PostgreSQL/Supabase y habilitar acceso de prueba. **PBI:** PB-001, PB-002, PB-004, PB-006 y PB-008. El reparto distingue la base e interfaz de Joan de la autenticación, protección de datos y catálogo de Renzo.

#### Cuadro 4.1. Tareas del Sprint 1

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-01 | Configurar entorno React, FastAPI y Supabase. | Joan | 4 |
| T-02 | Desarrollar interfaz de acceso y OTP de prueba. | Joan | 2 |
| T-03 | Implementar API de autenticación y OTP de prueba. | Renzo | 4 |
| T-06 | Configurar integración continua y pruebas iniciales. | Joan | 3 |
| T-07 | Implementar políticas RLS iniciales. | Renzo | 3 |
| T-09 | Crear tablas y datos iniciales del catálogo curricular. | Renzo | 2 |

Fuente: planificación vigente, tabla 5.2.

Son 18 h: 9 por integrante. **Aceptación conjunta:** servicios ejecutables, comunicación frontend–backend, OTP válido/inválido y vencido verificable, restricciones iniciales de datos y pipeline ejecutado. **Evidencias:** capturas, pruebas API, consultas SQL y ejecución de CI. SMTP institucional y validación integral de seguridad permanecen pendientes. Completar las tres tareas de Joan no cierra todo S1.

### 4.2. Sprint 2 — Roles, currículo y perfiles

**Objetivo:** registrar consentimiento, administrar roles y configurar perfiles y disponibilidad. **PBI:** PB-003, PB-005, PB-006, PB-007 y PB-008. Estas tareas amplían los datos y la protección preparados en S1.

#### Cuadro 4.2. Tareas del Sprint 2

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-04 | Desarrollar formulario de consentimiento digital. | Joan | 2 |
| T-05 | Implementar persistencia del consentimiento. | Renzo | 1 |
| T-08 | Desarrollar endpoints de administración de roles. | Renzo | 3 |
| T-10 | Implementar interfaz de consulta del catálogo curricular. | Joan | 2 |
| T-11 | Desarrollar formulario de perfiles y disponibilidad. | Joan | 3 |
| T-12 | Implementar API de perfiles y horarios. | Renzo | 2 |
| T-13 | Ejecutar pruebas de autorización entre usuarios. | Renzo | 1 |

Fuente: planificación vigente, tabla 5.3.

Son 14 h: 7 por integrante. **Aceptación:** perfiles y horarios persistidos, rechazo del consentimiento bloqueante, roles administrados con autorización y modificación de datos ajenos restringida. **Evidencias:** interfaces, consultas y pruebas de autorización. El consentimiento pertenece a S2 aunque comparta CUS01 con el acceso de S1.

### 4.3. Sprint 3 — Publicación de ofertas

**Objetivo:** publicar ofertas asociadas a asignaturas, temarios y horarios. **PBI:** PB-009; **trazabilidad:** RF08 / CUS06. Requiere mentores habilitados y catálogo curricular disponible.

#### Cuadro 4.3. Tareas del Sprint 3

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-14 | Desarrollar formulario de publicación de ofertas. | Joan | 2 |
| T-15 | Implementar API básica de gestión de ofertas. | Renzo | 2 |
| T-16 | Crear estructura de datos y relaciones de ofertas. | Renzo | 1 |

Fuente: planificación vigente, tabla 5.4.

Son 5 h: Joan 2 y Renzo 3. **Aceptación:** oferta persistida con asignatura y horario válidos; publicación no autorizada rechazada. Comprobar la antelación de RN-04 antes de cerrar RF08. **Evidencias:** formulario, API y registro en BD. Infraestructura física y aprovisionamiento virtual automatizado quedan pendientes.

### 4.4. Sprint 4 — Top-k y reservas

**Objetivo:** recomendar por afinidad temática y reservar con control transaccional de aforo. **PBI:** PB-010, PB-011 y PB-013; **trazabilidad:** RF06 / CUS02 y RF12 / CUS04. Requiere perfiles y ofertas disponibles.

#### Cuadro 4.4. Tareas del Sprint 4

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-17 | Implementar algoritmo inicial de similitud coseno. | Renzo | 3 |
| T-18 | Integrar perfiles y ofertas con API Top-k. | Joan | 2 |
| T-19 | Ejecutar pruebas del ordenamiento de recomendaciones. | Ambos | 1 |
| T-20 | Desarrollar interfaz de recomendaciones. | Joan | 2 |
| T-21 | Implementar formulario de reserva. | Joan | 2 |
| T-22 | Desarrollar API de reservas. | Renzo | 2 |
| T-23 | Integrar interfaz y servicio de reservas. | Joan | 1 |
| T-24 | Implementar transacción y prueba concurrente básica. | Renzo | 2 |

Fuente: planificación vigente, tabla 5.5.

Son 15 h: 7,5 por integrante; T-19 distribuye 0,5 h a cada uno. **Aceptación:** ranking ordenado, conjunto vacío controlado y reserva `PENDIENTE_CONFIRMACION`; dos solicitudes concurrentes no ocupan la misma última vacante. **Evidencias:** ranking, pruebas, API y registros. El modelo híbrido y las pruebas formales de rendimiento quedan pendientes.

### 4.5. Sprint 5 — Ratificación y desistimiento

**Objetivo:** confirmar o desistir de reservas respetando el corte T-24h. **PBI:** PB-014 y PB-015; **trazabilidad:** RF13 / CUS24 y RF14 / CUS17. Requiere reservas y estados persistidos.

#### Cuadro 4.5. Tareas del Sprint 5

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-25 | Implementar interfaz de confirmación de asistencia. | Joan | 1 |
| T-26 | Desarrollar API de ratificación con control temporal. | Renzo | 2 |
| T-27 | Implementar opción de desistimiento en la interfaz. | Joan | 1 |
| T-28 | Desarrollar anulación y liberación de cupos. | Renzo | 1 |

Fuente: planificación vigente, tabla 5.6.

Son 5 h: Joan 2 y Renzo 3. **Aceptación:** ratificación permitida antes del corte y rechazada fuera de plazo; desistimiento permitido cambia a `CANCELADA_USUARIO` y libera cupo. **Evidencias:** estados, respuestas API y pruebas con reloj controlado.

### 4.6. Sprint 6 — Quórum y bitácoras

**Objetivo:** evaluar quórum, permitir la decisión del mentor y registrar bitácoras y asistencias. **PBI:** PB-017, PB-018 y PB-019; **trazabilidad:** RF15 / CUS23, RF16 / CUS07 y RF17 / CUS08. Requiere confirmaciones y control temporal.

#### Cuadro 4.6. Tareas del Sprint 6

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-29 | Implementar reglas de evaluación de quórum en T-24h. | Renzo | 3 |
| T-30 | Incorporar control preliminar de ejecuciones repetidas. | Renzo | 1 |
| T-31 | Diseñar pruebas con reloj controlado. | Joan | 2 |
| T-32 | Desarrollar interfaz de decisión del mentor. | Joan | 1 |
| T-33 | Implementar API de gestión de contingencias. | Renzo | 1 |
| T-34 | Desarrollar formulario de bitácora y asistencias. | Joan | 3 |
| T-35 | Implementar API de bitácoras. | Renzo | 1 |
| T-36 | Registrar asistencias y horas provisionales en BD. | Renzo | 1 |
| T-37 | Ejecutar prueba de cierre de sesión. | Joan | 1 |

Fuente: planificación vigente, tabla 5.7.

Son 14 h: 7 por integrante. **Aceptación:** 4 confirmados de 10 cupos presenciales producen `QUORUM_INSUFICIENTE`; 5 cumplen el mínimo. El sistema no cancela unilateralmente: decide el mentor. La bitácora genera horas provisionales. **Evidencias:** transiciones, pruebas temporales, bitácoras y consultas. Cron de producción y notificaciones institucionales quedan pendientes.

### 4.7. Sprint 7 — Encuestas y visado de horas

**Objetivo:** evaluar mentorías y auditar horas. **PBI:** PB-020 y PB-023; **trazabilidad:** RF18 / CUS05 y RF26 / CUS22. Requiere asistencias y bitácoras registradas.

#### Cuadro 4.7. Tareas del Sprint 7

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-38 | Desarrollar interfaz de encuesta para asistentes. | Joan | 2 |
| T-39 | Implementar API de encuestas y ventana de 24 horas. | Renzo | 1 |
| T-40 | Desarrollar bandeja administrativa de bitácoras. | Joan | 1 |
| T-41 | Implementar aprobación u observación de bitácoras. | Renzo | 1 |

Fuente: planificación vigente, tabla 5.8.

Son 5 h: Joan 3 y Renzo 2. **Aceptación:** encuesta solo para asistentes efectivos y dentro del plazo; visado u observación solo por administrador autorizado; cómputo únicamente de horas aprobadas. **Evidencias:** capturas por rol, API, pruebas de permisos y consultas de horas.

### 4.8. Sprint 8 — Integración y demostración del MVP

**Objetivo:** integrar el recorrido completo, emitir constancias DEMO y evaluar Precision@k. **PBI:** PB-024, PB-027 y PB-037; **trazabilidad:** RF22 / CUS13, RF06 y calidad asociada. Requiere los incrementos anteriores integrados.

#### Cuadro 4.8. Tareas del Sprint 8

| ID | Actividad | Responsable | Horas |
| :--- | :--- | :--- | ---: |
| T-42 | Implementar generación de constancias PDF de demostración. | Renzo | 2 |
| T-43 | Desarrollar interfaz de descarga de constancias. | Joan | 1 |
| T-44 | Registrar constancias y folios de prueba. | Renzo | 1 |
| T-45 | Evaluar Precision@3 y Precision@5 con datos etiquetados. | Renzo | 2 |
| T-46 | Documentar resultados y limitaciones de Precision@k. | Joan | 1 |
| T-47 | Integrar navegación del flujo completo en React. | Joan | 2 |
| T-48 | Ejecutar pruebas integrales por rol. | Renzo | 2 |
| T-49 | Realizar pruebas exploratorias de interfaz. | Joan | 1 |
| T-50 | Preparar entorno y datos reproducibles de demostración. | Joan | 2 |
| T-51 | Consolidar documentación y evidencias finales. | Ambos | 1 |

Fuente: planificación vigente, tabla 5.9.

Son 15 h: 7,5 por integrante; T-51 distribuye 0,5 h a cada uno. **Aceptación:** recorrido integrado hasta la constancia marcada DEMO, emitida solo con horas visadas suficientes; Precision@3 y Precision@5 evaluadas con relevancia previamente etiquetada y limitaciones documentadas. **Evidencias:** recorrido, PDF, métricas, pruebas y guía reproducible. Certificación oficial, QR público e integraciones externas permanecen pendientes.

## 5. Instrucciones activas para el agente de Joan — Sprint 1

### 5.1. Estructura y decisiones de implementación

- `aplicacion/frontend/`: React, TypeScript y Vite; conservar `package-lock.json` y fijar versiones compatibles. Elegir y documentar una versión de Node compatible con Vite; usarla también en CI.
- `aplicacion/backend/`: Python 3.11, FastAPI, Uvicorn y pydantic-settings; entorno `.venv` y dependencias reproducibles con versiones fijadas.
- Backend según el SAD: `app/api`, `app/core`, `app/services`, `app/models` y `app/db`. Configuración central en `app/core`; migraciones Alembic en `app/db`; SQLAlchemy y psycopg 3 para PostgreSQL.
- `docs/sprints/sprint-01.md`: bitácora de ejecución, comandos, decisiones, resultados, evidencias y pendientes. Complementa este plan; no lo sustituye.
- `.github/workflows/ci.yml`: workflow en la raíz del repositorio, con directorios de trabajo de la nueva aplicación.

No añadir Redis, Docker, despliegue productivo ni módulos futuros por anticipación. Documentar comandos para Windows/PowerShell. Las decisiones técnicas de este apartado concretan los hitos acordados; no afirman que los archivos existan.

### 5.2. Hitos y commits

T-01 se divide en dos hitos para separar la base ejecutable de la conexión. Ambos comparten sus cuatro horas planificadas: dividirlos no incrementa la estimación ni crea nuevas tareas oficiales.

#### Cuadro 5.1. Entregas del agente de Joan

| Hito | Tarea | Resultado verificable | Commit |
| :--- | :--- | :--- | :--- |
| H1 | T-01, parte 1 | React–FastAPI y health operativos | `chore(s1): configurar estructura React y FastAPI [T-01]` |
| H2 | T-01, parte 2 | Conexión inicial PostgreSQL/Supabase | `feat(s1): conectar FastAPI con Supabase [T-01]` |
| H3 | T-02 | Interfaz de acceso y OTP de prueba | `feat(s1): implementar interfaz de acceso OTP de prueba [T-02]` |
| H4 | T-06 | Pruebas iniciales y GitHub Actions | `ci(s1): agregar pruebas iniciales e integracion continua [T-06]` |

Fuente: descomposición operativa acordada con Joan para las tareas de la tabla 5.2 de la planificación.

Mantener este orden y un commit de implementación por hito. Si ya existe trabajo, verificarlo y completar solo lo pendiente. Las correcciones posteriores se registran sin borrar commits ni atribuir resultados inexistentes.

### 5.3. H1 — Estructura y comunicación React–FastAPI

1. Preparar ambos proyectos con la estructura anterior y las dependencias necesarias.
2. Implementar `GET /api/v1/health`: HTTP 200 y `{"status":"ok"}`, independiente de la BD. Comprobar `/docs`.
3. Configurar CORS para el origen local de React y `VITE_API_BASE_URL` mediante `.env.example`.
4. Mostrar en React el resultado real de la consulta de salud, con estados de carga y error.
5. Actualizar `.gitignore`: excluir `.env` privados, `.venv`, `node_modules`, `dist` y cachés; conservar `.env.example`.
6. Registrar arranque local, versiones elegidas y comandos reproducibles.

**Aceptación:** ambos servicios arrancan, React consulta FastAPI y `npm run build` y `npm run lint` pasan. Crear el commit H1 y detenerse.

### 5.4. H2 — Conexión inicial a Supabase

**Preparación local:** crear o seleccionar el proyecto de desarrollo `p2p-epis-dev` en Supabase. Obtener en **Connect → Session pooler** la cadena real, conservando host, puerto y usuario. El modo sesión permite acceder desde redes IPv4. Usar la contraseña de PostgreSQL, no una API key, y codificar sus caracteres reservados para URL.

Guardar solo en `aplicacion/backend/.env` una cadena con el dialecto de psycopg 3; este ejemplo contiene marcadores, no credenciales:

```dotenv
APP_ENV=development
DATABASE_URL="postgresql+psycopg://postgres.PROJECT_REF:PASSWORD_URL_ENCODED@POOLER_HOST:5432/postgres?sslmode=require"
```

1. Cargar la configuración desde el `.env` del backend. Centralizar conexión, apertura diferida, timeout y cierre de recursos.
2. Preparar Alembic sin crear tablas de negocio: pertenecen a las tareas de datos de Renzo.
3. Implementar `GET /api/v1/health/db`, solo en desarrollo: ejecutar `SELECT 1`; devolver 200 si funciona y 503 si falta configuración o falla la conexión. En otros entornos, no exponer este endpoint.
4. Sanitizar respuestas y logs: no mostrar cadenas, contraseñas ni trazas internas al cliente. Mantener `/api/v1/health` disponible aunque la BD no funcione.
5. Verificar conexión real y fallo controlado, dejando evidencia sin secretos. Si faltan credenciales, documentar «conexión real pendiente» y conservar el arranque y las pruebas sin BD.

**Aceptación:** `SELECT 1` real satisfactorio y fallo controlado. La configuración puede quedar versionada con comprobaciones locales correctas, pero T-01 no se declara completamente verificada mientras falte la prueba real. Crear el commit H2 conforme al resultado documentado y detenerse.

**Límite con T-07:** una conexión exitosa no verifica RLS. La conexión administrativa del ejemplo solo sirve para esta comprobación técnica. Antes de acceder a datos de usuarios, acordar con Renzo un rol efectivo sin `BYPASSRLS`, que tampoco eluda RLS como propietario de tablas, y la propagación segura de identidad por transacción. Un JWT de prueba no configura automáticamente `auth.uid()` en una conexión SQLAlchemy. Mantener separados permisos de migración y de ejecución. No colocar `DATABASE_URL`, contraseñas o claves `service_role` en variables `VITE_*`.

`sslmode=require` exige cifrado; no acredita por sí solo todos los requisitos de RNF02. Las políticas de tablas expuestas y sus pruebas negativas corresponden a T-07, coordinadas con la creación de tablas de T-09.

### 5.5. H3 — Interfaz de acceso y OTP de prueba

1. Reutilizar colores, tipografía y componentes de la maqueta. Implementar correo institucional `@upt.pe` y OTP de seis dígitos con vigencia máxima de cinco minutos, según CUS01 y RNF01.
2. Incluir estados de carga, correo inválido, OTP incorrecto, expiración, reenvío y error de conexión; usar etiquetas accesibles.
3. Centralizar acceso al servicio en `src/services/authService.ts`. Documentar solicitud y verificación de OTP, datos, errores y expiración; contrastar el contrato con T-03 antes de integrarlo.
4. Si existe la API de T-03, reutilizar su contrato. Si no existe, preparar un adaptador mock explícito, habilitado solo en desarrollo, con aviso visible **«Acceso de prueba»**.
5. El mock debe permitir reproducir OTP correcto, incorrecto, vencido y código anterior invalidado por reenvío. No emitirá JWT ni concederá acceso a datos reales. No activar el mock silenciosamente cuando falle una API real.
6. Utilizar `expires_at` para el contador. Con la API integrada, la validación definitiva y el vencimiento corresponden al backend.
7. Mostrar una confirmación mínima después de verificar el código. El consentimiento T-04/T-05 y los paneles funcionales corresponden a trabajo posterior; no simular que ya están implementados.

**Aceptación:** escenarios reproducibles y modo mock/API claramente documentado. No declarar RF01 ni RNF01 completos: faltan componentes institucionales y del flujo integral. Crear el commit H3 y detenerse.

### 5.6. H4 — Pruebas e integración continua

1. Frontend: Vitest y React Testing Library; cubrir correo inválido, OTP correcto, incorrecto, vencido, reenvío y errores del servicio.
2. Backend: pytest, TestClient y Ruff; cubrir health y health/db con conexión sustituida: éxito, falta de configuración y fallo controlado. Comprobar que health/db no está expuesto fuera de desarrollo.
3. Las pruebas habituales deben funcionar sin credenciales, SMTP ni llamadas reales a Supabase. Separar la comprobación manual de conexión real.
4. Configurar `.github/workflows/ci.yml` con jobs independientes de frontend y backend, para `pull_request` y `push` a `main` y `feat/sprint-01-base-acceso-ci`.
5. Frontend: `npm ci`, lint, pruebas sin watch y build. Backend: instalación reproducible, Ruff y pytest. Utilizar las versiones de Node/Python documentadas localmente.
6. Generar cobertura de ambos componentes y registrar porcentaje y alcance medido. RNF09 establece una meta mínima del 70%; la cobertura de estos componentes iniciales no acredita todo el sistema.
7. Documentar resultados locales. Después de subir la rama, verificar GitHub Actions y registrar enlace y resultado reales.

**Aceptación:** comprobaciones locales correctas y workflow preparado. Crear el commit H4 y detenerse. Mantener la ejecución remota como pendiente hasta observarla; no presentar «workflow creado» como «CI remoto aprobado».

Al finalizar los hitos y revisar sus commits, la subida de la rama acordada se realiza con:

```bash
git push -u origin feat/sprint-01-base-acceso-ci
```

No fusionar con `main` ni desplegar a producción como parte de estos hitos.

## 6. Coordinación con Renzo y límites de responsabilidad

Las dependencias del Sprint 1 deben integrarse sin duplicar implementaciones ni cambiar silenciosamente contratos compartidos.

#### Cuadro 6.1. Puntos de integración del Sprint 1

| Responsable | Tarea | Entrega esperada | Coordinación necesaria |
| :--- | :--- | :--- | :--- |
| Joan | T-01 | Entorno, configuración y conectividad | Compartir comandos y `.env.example` sin secretos con Renzo. |
| Joan | T-02 | Interfaz y adaptador del servicio OTP | Usar contrato de T-03; señalar mock mientras no exista API. |
| Renzo | T-03 | API OTP de prueba | Acordar rutas, payloads, errores, expiración, reenvío y mecanismo de sesión de prueba. |
| Joan | T-06 | Pruebas iniciales y CI | Ejecutar sin servicios externos; incorporar verificaciones de la integración disponible. |
| Renzo | T-07 | Políticas RLS iniciales | Definir identidad y rol efectivo de conexión; verificar accesos permitidos y denegados. |
| Renzo | T-09 | Tablas y datos del catálogo | Usar la estructura de migraciones común y coordinar permisos con T-07. |

Fuente: responsabilidades de la planificación y acuerdos operativos de integración del Sprint 1.

El agente de Joan puede preparar adaptadores y puntos de conexión para estas entregas. La implementación de T-03, T-07 o T-09 requiere una ampliación explícita del encargo. Usar datos ficticios en la demostración y no tratar una identidad simulada como acceso institucional validado.

## 7. Registro de avance y definición de terminado

Al crear este documento **no se ha verificado la ejecución de ninguna tarea en el entorno local del usuario**. Inspeccionar código, commits y evidencias antes de asignar estados. Conservar en este archivo la línea base planificada; registrar avances y desviaciones en `docs/sprints/sprint-01.md`.

Estados sugeridos: **No verificado**, **Pendiente**, **En curso**, **Bloqueado**, **Verificado localmente**, **Integrado**. Añadir de forma independiente el alcance **Simulado**, **Parcial** o **Real**. Un estado local satisfactorio puede coexistir con integración remota pendiente.

Para cada entrega, registrar:

- Hito, tarea, PBI y RF/RNF/CUS relacionados.
- Responsable y fecha real; horas reales separadas de las planificadas.
- Archivos modificados, decisión técnica y contrato utilizado.
- Comandos ejecutados y resultados observados; porcentaje y alcance de cobertura cuando corresponda.
- Evidencias reproducibles y enlace a CI cuando exista; hash real del commit.
- Limitaciones, dependencias y siguiente paso.

**DoD del incremento:** comportamiento ejecutable y reproducible, código integrado, aceptación del alcance acordado, pruebas ejecutadas y registradas, ausencia de defectos críticos para ese alcance y evidencias archivadas. Si hay mock o entrega parcial, mantener visible la brecha frente al SRS.

**Cierre de las tareas de Joan:** H1–H4 comprobados, conexión real acreditada para T-01, modo de acceso identificado y CI remoto verificado para cerrar T-06. **Cierre del Sprint 1 completo:** además, integrar y verificar T-03, T-07 y T-09 con sus evidencias. No inferir el cierre por fecha ni por número de commits.

Usar Markdown UTF-8 sin BOM. Mantener presentación, título, tabla, fuente y explicación en los cuadros; usar PlantUML si se añaden diagramas. Actualizar el README en cada ciclo y sincronizar la bóveda de diagramas cuando corresponda por cambios en los artefactos del SRS/SAD. Este plan no modifica esos documentos.

## 8. Fuentes y mantenimiento

- **Planificación vigente:** `G03_S2_Planificación de Sprint.docx (2).pdf`, copia del 19/10/2026, 24 páginas. PBI: pp. 6–8; calendario y tareas: pp. 9–18; trazabilidad: pp. 20–21; viabilidad y DoD: p. 22.
- **Requisitos:** [FD03 — SRS](https://github.com/JMedina255/sistema_web_p2p/blob/main/docs/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md), consultado el 19/10/2026; blob `b134df9b6cb912edf66ef71c05bef6200e982238`.
- **Arquitectura:** [FD04 — SAD](https://github.com/JMedina255/sistema_web_p2p/blob/main/docs/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md), consultado el 19/10/2026; blob `cc8fe92b6d7fc1cb04ee44dd54c73854d2ca1c2a`.
- **Estándares:** [reglas_documentacion.md](https://github.com/JMedina255/sistema_web_p2p/blob/main/reglas_documentacion.md) y [rules_doc.md](https://github.com/JMedina255/sistema_web_p2p/blob/main/rules_doc.md).
- **Referencia técnica de conexión:** [Supabase — conectar PostgreSQL](https://supabase.com/docs/guides/database/connecting-to-postgres) y [SQLAlchemy — psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg).
- **Referencia técnica de permisos:** [Supabase — RLS](https://supabase.com/docs/guides/database/postgres/row-level-security).

El PDF cita el repositorio documental `Sistema_Web_P2P_con_algoritmo_de_recomendaci-n`; el usuario indicó `sistema_web_p2p` como repositorio de implementación para este trabajo. Conservar esa distinción y no cambiar remotos por inferencia.

**Mantenimiento:** al aprobar una replanificación, actualizar versión, fecha y motivo, conservando trazabilidad de IDs, responsables, horas y cambios de alcance. La lectura de este archivo proporciona contexto; el prompt del usuario selecciona el hito que debe ejecutarse.
