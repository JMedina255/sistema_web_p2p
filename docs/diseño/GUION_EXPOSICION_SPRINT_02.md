# GUION DE EXPOSICIÓN TÉCNICA, PRESENTACIÓN FORMAL Y DEFENSA DE ARQUITECTURA
## SPRINT 02: ROLES, CURRÍCULO, PERFILES Y CONSENTIMIENTO INFORMADO (LEY N° 29733)

**Proyecto:** Sistema Web P2P de Mentoría entre Pares  
**Institución:** Universidad Privada de Tacna (UPT) — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas (EPIS)  
**Código de Documento:** `GUION-S02-V1.0`  
**Autores:** Joan Sebastian Medina Lopez, Renzo Gabriel Paredes Rivas  
**Fecha:** 26 de Octubre de 2026  
**Audiencia Objetivo:** Equipo de Desarrollo, Arquitectos de Software, Evaluadores Técnicos y Docentes de Taller de Proyectos  

---

## 🎯 1. Propósito y Estructura del Guion

Este documento constituye la guía formal para la exposición técnica y defensa metodológica del **Sprint 02**. Su propósito es proporcionar al equipo de desarrollo y a los evaluadores la fundamentación de **por qué** se diseñó de esta forma el sistema, **qué requerimientos oficiales** lo respaldan, **cómo funciona internamente la arquitectura** y **cómo se verificó con 150 pruebas automatizadas**.

La presentación sigue el principio de **Trazabilidad Continua en 9 Eslabones**:
$$\text{Necesidad} \longrightarrow \text{Requerimiento} \longrightarrow \text{Historia} \longrightarrow \text{Caso de Uso} \longrightarrow \text{Análisis (SRS)} \longrightarrow \text{Diseño (SAD)} \longrightarrow \text{Código} \longrightarrow \text{Prueba} \longrightarrow \text{Métricas}$$

---

## 🧭 2. El Recorrido de Trazabilidad en 4 Pilares Funcionales

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              CADENA DE TRAZABILIDAD SPRINT 02                               │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │
             ┌─────────────────────────────────┼─────────────────────────────────┐
             ▼                                 ▼                                 ▼
   ┌───────────────────┐             ┌───────────────────┐             ┌───────────────────┐
   │     PILAR A       │             │     PILAR B       │             │     PILAR C/D     │
   │  CONSENTIMIENTO   │             │ ROLES Y MÉRITO    │             │ MALLA Y HORARIOS  │
   │   (Ley N° 29733)  │             │     (RN-03)       │             │   (Matriz 6x11)   │
   └─────────┬─────────┘             └─────────┬─────────┘             └─────────┬─────────┘
             │                                 │                                 │
             ▼                                 ▼                                 ▼
       RF02 / RN-02                      RF03 / RN-03                      RF04, RF05, RNF09
       HU-03 / CUS01                     HU-04 / CUS10                     HU-05, HU-06 / CUS15, CUS21
             │                                 │                                 │
             ▼                                 ▼                                 ▼
   Diagrama Kroki 09/13              Diagrama Kroki 10/13              Diagrama Kroki 11/14
   (Secuencia / Estados)             (Secuencia / Mérito)              (Secuencia / ERD)
             │                                 │                                 │
             ▼                                 ▼                                 ▼
   consent.py / ConsentModal         roles.py / RoleSelector           profiles.py / ScheduleGrid
   RLS `consentimientos_legales`     RLS `usuario_roles`               RLS `disponibilidades_horarias`
             │                                 │                                 │
             ▼                                 ▼                                 ▼
   CP-01..CP-08 (14 tests)           CP-09..CP-14 (12 tests)           CP-15..CP-26 (16 tests)
```

---

### 2.1. Pilar A: Consentimiento Legal Informado y Protección de Datos

1. **Necesidad del Negocio:** En el contexto universitario peruano, almacenar y procesar datos académicos y perfiles de estudiantes sin autorización expresa viola la Ley N° 29733 (Ley de Protección de Datos Personales). Sin consentimiento explícito, la plataforma se expone a sanciones administrativas y desconfianza estudiantil.
2. **Requerimiento Funcional:** `RF02` (Gestión de Consentimiento Informado) y `RNF02` (Cumplimiento de Privacidad Legal).
3. **Regla de Negocio:** `RN-02` — Todo estudiante debe consentir expresamente el tratamiento de datos. El rechazo o revocación bloquea de inmediato las funciones operativas de emparejamiento.
4. **Historia de Usuario:** `HU-03` — Criterios de aceptación en Gherkin: modal forzado en primer login, persistencia inmutable de versión y timestamp, y revocación con cierre de sesión.
5. **Caso de Uso y Narrativa:** `CUS01` (Gestionar Consentimiento Informado). Flujo principal de aceptación y flujos alternativos de revocación y rechazo.
6. **Diagramas de Respaldo:**
   - Análisis: Diagrama de Casos de Uso del Sprint 02 (`08_diagrama_casos_de_uso_sprint02.png`).
   - Diseño: Diagrama de Secuencia de Consentimiento (`09_secuencia_consentimiento_ley29733.png`) y Máquina de Estados del Consentimiento (`13_maquina_estados_consentimiento_roles.png`).
7. **Implementación Técnica:**
   - Frontend: [ConsentModal.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/components/ConsentModal.vue).
   - Backend: [consent.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/routers/consent.py) con endpoints `POST /consent` y `GET /consent/history`.
   - Base de Datos: Tabla `consentimientos_legales` con política RLS `consent_owner_all`.
8. **Pruebas y Validación:** Casos `CP-01` a `CP-08` en el Catálogo Excel; pruebas automatizadas en [test_consent.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_consent.py) (14 tests pasando al 100%).
9. **Resultado y Métricas:** 100% de cobertura en trazabilidad legal; 0 bypasses posibles gracias al aislamiento en base de datos.

---

### 2.2. Pilar B: Asignación de Roles y Verificación de Mérito Académico

1. **Necesidad del Negocio:** Para que el modelo de mentoría entre pares funcione y tenga credibilidad académica, un alumno de primeros ciclos no puede instruir a sus pares en materias avanzadas. Solo los alumnos con madurez académica (ciclo VII o superior) deben ejercer la mentoría.
2. **Requerimiento Funcional:** `RF03` (Asignación y Cambio de Rol de Usuario).
3. **Regla de Negocio:** `RN-03` — Restricción de Mérito Académico: el rol de Mentor (`rol_id = 2`) está reservado exclusivamente a estudiantes con `ciclo_actual >= 7`. Estudiantes de ciclos I a VI solo pueden ser Estudiantes (`rol_id = 1`) o Administradores (`rol_id = 3` por designación institucional).
4. **Historia de Usuario:** `HU-04` — Criterios de aceptación: bloqueo visual en frontend y rechazo con error HTTP 403 Forbidden en backend ante intentos de asignación fraudulenta.
5. **Caso de Uso y Narrativa:** `CUS10` (Cambiar Rol Activo). Flujo principal para alumnos de ciclo $\ge$ VII; flujo de excepción 3a disparado si `ciclo_actual < 7`.
6. **Diagramas de Respaldo:**
   - Diseño: Diagrama de Secuencia de Verificación de Mérito RN-03 (`10_secuencia_roles_merito_rn03.png`) y Máquina de Estados (`13_maquina_estados_consentimiento_roles.png`).
7. **Implementación Técnica:**
   - Frontend: [RoleSelector.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/components/RoleSelector.vue).
   - Backend: [roles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/routers/roles.py) validando explícitamente `if request.role_id == 2 and profile.ciclo_actual < 7: raise HTTPException(status_code=403, detail="...")`.
   - Base de Datos: Tablas `roles` y `usuario_roles` con políticas RLS `user_roles_read_all` y `user_roles_modify_own`.
8. **Pruebas y Validación:** Casos `CP-09` a `CP-14` del catálogo; pruebas automatizadas en [test_roles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_roles.py) (12 tests pasando).
9. **Resultado y Métricas:** Imposibilidad técnica de saltarse el mérito académico, garantizando la solvencia pedagógica del sistema.

---

### 2.3. Pilar C: Catálogo y Malla Curricular Oficial de la EPIS

1. **Necesidad del Negocio:** En mentorías tradicionales, los alumnos suelen crear ofertas o solicitudes con nombres de cursos ambiguos o no estandarizados (ej. "Mate 1", "Cálculo", "Matemáticas I"), lo que destruye cualquier capacidad algorítmica de emparejamiento. Se requiere una taxonomía oficial normalizada.
2. **Requerimiento Funcional:** `RF04` (Exploración del Catálogo y Malla Curricular).
3. **Regla de Negocio:** Vinculación con el Plan de Estudios oficial vigente de la EPIS-UPT, organizando cursos por código, nombre oficial, ciclo lectivo (I a X) y área formativa.
4. **Historia de Usuario:** `HU-05` — Búsqueda en tiempo real por texto predictivo y filtrado facetado por ciclo.
5. **Caso de Uso y Narrativa:** `CUS21` (Explorar Malla Curricular y Cursos).
6. **Diagramas de Respaldo:**
   - Diseño: Diagrama Entidad-Relación (`14_diagrama_entidad_relacion_sprint02.png`) mostrando el acoplamiento con perfiles académicos.
7. **Implementación Técnica:**
   - Frontend: [CurriculumView.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/views/CurriculumView.vue) y catálogo en store.
   - Backend: [curriculum.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/routers/curriculum.py) con filtrado por parámetros de consulta.
8. **Pruebas y Validación:** Casos `CP-27` a `CP-31`; suite de pruebas en [test_curriculum.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_curriculum.py) (8 tests pasando).
9. **Resultado y Métricas:** Tiempos de respuesta menores a 50 ms en catálogo curricular en memoria/BD.

---

### 2.4. Pilar D: Perfiles Académicos y Matriz de Disponibilidad Semanal 6×11

1. **Necesidad del Negocio:** Para coordinar sesiones de mentoría sin solapamientos ni fricciones de mensajería externa, mentores y estudiantes deben pactar su disponibilidad en un esquema predecible de bloques discretos de 1 hora.
2. **Requerimiento Funcional:** `RF05` (Registro de Perfil Académico y Disponibilidad Horaria) y `RNF09` (Tiempo de Respuesta < 1.0 s).
3. **Historia de Usuario:** `HU-06` — Cuadrícula semanal interactiva lunes a sábado de 08:00 a 19:00 (66 celdas seleccionables).
4. **Caso de Uso y Narrativa:** `CUS15` (Gestionar Perfil y Disponibilidad Semanal). Flujo de guardado atómico con transaccionalidad completa (`DELETE FROM disponibilidades_horarias WHERE usuario_id = :id` seguido de inserción masiva).
5. **Diagramas de Respaldo:**
   - Diseño: Diagrama de Secuencia de Guardado Atómico de Disponibilidad (`11_secuencia_perfil_disponibilidad_atomic.png`) y Diagrama de Seguridad Multiusuario con RLS (`12_secuencia_seguridad_multiusuario_rls.png`).
6. **Implementación Técnica:**
   - Frontend: [ScheduleGrid.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/components/ScheduleGrid.vue) y [ProfileView.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/views/ProfileView.vue).
   - Backend: [profiles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/routers/profiles.py) con transacción SQLAlchemy ACID.
   - Base de Datos: Tablas `perfiles_academicos` y `disponibilidades_horarias` con políticas RLS `profiles_owner_all` y `availability_owner_all`.
7. **Pruebas y Validación:** Casos `CP-15` a `CP-26`; pruebas automatizadas en [test_profiles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_profiles.py) y [test_authorization.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_authorization.py) (18 tests combinados).
8. **Resultado y Métricas:** Persistencia atómica probada frente a fallos; aislamiento multi-usuario verificado (un usuario jamás puede sobreescribir la disponibilidad de otro).

---

## 📽️ 3. Propuesta de Diapositivas para la Exposición (Storyboard)

A continuación se detalla la propuesta de 11 diapositivas optimizada para una presentación ejecutiva y técnica de **20 a 25 minutos**:

| N° | Título de la Diapositiva | Objetivo Principal | Recursos Visuales | Talking Points (Notas del Orador) | Tiempo |
|:---|:---|:---|:---|:---|:---|
| **01** | **Sprint 02: Fundamentos del Ecosistema P2P** | Introducir el hito, el equipo y la meta del sprint. | Logo UPT/EPIS, Ficha técnica, tabla de métricas (150 tests, >90% cobertura). | *"Bienvenidos. Hoy presentamos el Sprint 02, la columna vertebral de roles, privacidad y disponibilidad horaria que hace viable el sistema de mentorías..."* | 1.5 min |
| **02** | **Cadena de Trazabilidad: Del Requisito al Código** | Demostrar el rigor metodológico sin fisuras. | Esquema conceptual de los 9 eslabones, referencias SRS v2.1 y SAD v2.0. | *"No escribimos una sola línea de código sin un requerimiento aprobado. Cada componente frontend y endpoint responde a una historia formal y tiene pruebas asociadas..."* | 2.0 min |
| **03** | **Pilar 1: Consentimiento Legal y Ley N° 29733** | Explicar el cumplimiento legal y la arquitectura de privacidad. | Kroki 09 (Secuencia) y Kroki 13 (Estados), captura de `ConsentModal.vue`. | *"En el Perú, la Ley 29733 prohíbe tratar datos sin consentimiento. Diseñamos un flujo bloqueante de primer login y persistencia con firma temporal inmutable..."* | 2.5 min |
| **04** | **Pilar 2: Roles y Restricción de Mérito Académico (RN-03)** | Demostrar cómo se protege la calidad pedagógica. | Kroki 10 (Secuencia RN-03), snippet de validación en `roles.py`, captura `RoleSelector.vue`. | *"La mentoría exige solvencia. La regla de negocio RN-03 exige estar en ciclo VII o superior para ser Mentor. Esta regla se valida en backend con HTTP 403 y en frontend con controles deshabilitados..."* | 2.5 min |
| **05** | **Pilar 3: Malla Curricular y Estandarización de Cursos** | Explicar la estructuración formal del catálogo de materias. | Kroki 14 (ERD - fragmento cursos), captura de `CurriculumView.vue`. | *"Evitamos el caos de nombres ambiguos integrando la taxonomía oficial de la EPIS organizada por ciclos y áreas de formación para alimentar el motor de matching..."* | 2.0 min |
| **06** | **Pilar 4: Perfiles y Matriz Semanal Atómica 6×11** | Presentar la innovación de la disponibilidad horaria discreta. | Kroki 11 (Secuencia Atómica), captura interactiva de `ScheduleGrid.vue`. | *"Diseñamos una cuadrícula de 6 días por 11 horas (66 bloques). La persistencia es atómica: o se guarda la agenda completa o se hace rollback, evitando estados corruptos..."* | 2.5 min |
| **07** | **Seguridad en Profundidad: PostgreSQL Row-Level Security (RLS)** | Justificar la protección de datos multi-inquilino en base de datos. | Kroki 12 (Secuencia RLS), extracto SQL de `supabase_rls_sprint02.sql`. | *"No confiamos únicamente en la capa de FastAPI. La base de datos aplica políticas RLS: incluso con una inyección SQL o falla en backend, un alumno solo puede acceder a sus propios datos..."* | 2.5 min |
| **08** | **Modelo de Datos Relacional y Migraciones Alembic** | Mostrar la arquitectura física normalizada. | Kroki 14 (ERD Completo de Sprint 02), tabla de claves foráneas e índices. | *"5 tablas relacionales en 3FN gestionadas mediante migraciones reproducibles con Alembic (`002_roles_and_profiles.py`), garantizando integridad referencial estricta..."* | 2.0 min |
| **09** | **Estrategia de Aseguramiento de Calidad y Pruebas** | Evidenciar la verificación automatizada exhaustiva. | Tabla de 35 casos de prueba de análisis vinculados a 150 tests automatizados en vivo. | *"Auditamos los 35 casos del catálogo formal de análisis y los respaldamos con 84 tests en Pytest y 66 tests en Vitest. Todas las suites superan el 90% de cobertura..."* | 2.5 min |
| **10** | **Demostración Práctica en Vivo (Live Demo)** | Validar en tiempo real los flujos implementados. | Navegador web ejecutando el flujo: Login $\rightarrow$ Consentimiento $\rightarrow$ Cambio de Rol $\rightarrow$ Agenda. | *"Veamos la aplicación en vivo: observen cómo el modal bloquea la interacción, cómo el ciclo VI deshabilita el botón de mentor y cómo se guarda la matriz horaria..."* | 3.5 min |
| **11** | **Conclusiones, Cumplimiento de DoD y Puerta al Sprint 03** | Resumir el éxito del sprint y dar paso a la sesión de preguntas. | Checklist DoD al 100%, enlace al Sprint 03 (Ofertas y Matching). | *"El Sprint 02 cerró con el 100% de criterios de aceptación cumplidos. Dejamos el terreno listo para la publicación de sesiones y el motor de recomendación. Quedamos atentos a sus preguntas..."* | 1.5 min |

---

## ❓ 4. Preguntas Técnicas Frecuentes y Respuestas Fundamentadas (FAQ)

Anticipación de dudas técnicas de desarrolladores, arquitectos y evaluadores docentes durante la ronda de sustentación:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                       MATRIZ DE DEFENSA TÉCNICA ANTE EL EQUIPO                              │
├──────────────────────────────────────┬──────────────────────────────────────────────────────┤
│ Pregunta Técnica Clave               │ Fundamento Oficial y Referencia                      │
├──────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ 1. ¿Por qué matriz relacional y no   │ Rendimiento en cruces SQL y soporte de índices       │
│    JSONB en disponibilidad?          │ SAD v2.0 §5.4 / DDL disponibilidades_horarias        │
├──────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ 2. ¿Dónde se valida la regla RN-03   │ Doble anillo: Backend (403) y Frontend (Disabled)   │
│    y por qué en ambos lados?         │ SRS v2.1 §3.2 / roles.py L45-52 / RoleSelector.vue   │
├──────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ 3. ¿Qué ocurre ante la revocación    │ Inactivación en BD y expulsión de sesión activa      │
│    del consentimiento legal?         │ RN-02 / consent.py L68-80 / ConsentModal.vue         │
├──────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ 4. ¿Cómo se protege la atomicidad    │ Transacción ACID con DELETE masivo previo a INSERT   │
│    en el guardado de la agenda?      │ SAD v2.0 §4.3 / profiles.py L112-135 / Kroki 11      │
├──────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ 5. ¿Por qué RLS si FastAPI ya        │ Principio de Defensa en Profundidad (OWASP ASVS)     │
│    valida tokens JWT?                │ SAD v2.0 §6.1 / supabase_rls_sprint02.sql / Kroki 12 │
├──────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ 6. ¿Dónde está la prueba que frena   │ Test unitario automatizado con mock de alumno c6     │
│    un POST fraudulento de Mentor?    │ test_roles.py::test_assign_mentor_role_denied_low_sem │
└──────────────────────────────────────┴──────────────────────────────────────────────────────┘
```

### Detalle de Respuestas Fundamentadas:

#### P1: ¿Por qué se utilizó una tabla normalizada `disponibilidades_horarias` con celda atómica `(dia_semana, bloque_horario)` en vez de almacenar un JSONB o un string en el perfil?
> **Respuesta del Orador:**  
> *"La decisión se tomó pensando en el motor de recomendación del Sprint 03 y Sprint 04. Si almacenáramos los horarios en un arreglo JSONB o string dentro del perfil, encontrar mentores disponibles para una sesión en un horario determinado requeriría escaneo completo de tablas (`full table scans`) o funciones de desanidamiento JSON costosas. Con la tabla relacional `disponibilidades_horarias` normalizada con clave primaria compuesta `(usuario_id, dia_semana, bloque_horario)` e índice B-Tree, el motor puede hacer un `INNER JOIN` directo indexado en milisegundos. Esta justificación técnica está formalizada en el SAD v2.0, Sección 5.4."*

#### P2: ¿Dónde se valida la regla de negocio `RN-03` (mérito de ciclo $\ge$ VII) y por qué ahí?
> **Respuesta del Orador:**  
> *"Se aplica el principio de **Validación en Dos Anillos**. En el Frontend ([RoleSelector.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/components/RoleSelector.vue)), la opción de 'Mentor' se muestra deshabilitada (`disabled`) con un tooltip pedagógico si `user.profile.ciclo_actual < 7`, protegiendo la experiencia de usuario (UX). Pero como el cliente web nunca es de confianza, el Backend ([roles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/routers/roles.py)) es la autoridad final: evalúa de forma ineludible `if request.role_id == 2 and profile.ciclo_actual < 7:` y responde con `HTTP 403 Forbidden`. Esto está verificado en el caso de prueba `CP-11` y `test_roles.py`."*

#### P3: ¿Cómo interactúa el frontend con el backend en el flujo de revocación de consentimiento legal y qué consecuencias inmediatas tiene en la sesión?
> **Respuesta del Orador:**  
> *"Cuando el estudiante decide revocar su consentimiento desde la configuración de su perfil, [ConsentModal.vue](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/components/ConsentModal.vue) despacha un `POST /consent` con `otorgado: false`. El backend registra un nuevo registro histórico inmutable en `consentimientos_legales` con la marca de tiempo de revocación. Inmediatamente después, el interceptor de Axios en el frontend borra el token JWT del almacenamiento local y redirige al usuario a la pantalla de login, impidiendo que siga interactuando con las funciones del sistema. Esto cumple estrictamente con el artículo 20 de la Ley N° 29733."*

#### P4: ¿Qué pasa si falla el registro de disponibilidad horaria a mitad de una transacción o si la red se corta mientras se guardan las celdas?
> **Respuesta del Orador:**  
> *"La operación está blindada bajo un bloque de transacción ACID de SQLAlchemy en [profiles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/routers/profiles.py). El algoritmo primero ejecuta `DELETE FROM disponibilidades_horarias WHERE usuario_id = :id` y seguidamente inserta el lote de nuevas celdas. Si la conexión falla, se cancela o una celda viene con formato inválido, el bloque `try...except` ejecuta un `db.rollback()` inmediato. La base de datos nunca quedará con una disponibilidad a medio guardar. Esto se modeló en el diagrama de secuencia Kroki 11 y se probó en `test_profiles.py`."*

#### P5: ¿Cómo se garantiza la seguridad e integridad de datos multi-usuario sin depender exclusivamente de FastAPI?
> **Respuesta del Orador:**  
> *"A través de **PostgreSQL Row-Level Security (RLS)** documentado en [supabase_rls_sprint02.sql](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/supabase_rls_sprint02.sql). Aunque un desarrollador cometa un error en una consulta backend olvidando filtrar por `WHERE usuario_id = current_user`, el motor PostgreSQL intercepta la consulta a nivel de filas mediante la política `USING (usuario_id = auth.uid())`. Si un usuario autenticado intenta leer o modificar los datos de otro, la base de datos retorna 0 filas o deniega el acceso. La seguridad no descansa únicamente en la aplicación, sino en el motor de persistencia."*

#### P6: ¿Dónde está la prueba que demuestra que un estudiante de VI ciclo no puede forzar su asignación como Mentor mediante Postman o curl?
> **Respuesta del Orador:**  
> *"La prueba está codificada en el archivo [test_roles.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_roles.py), específicamente en el método `test_assign_mentor_role_denied_low_semester()`. En esta prueba, generamos un usuario autenticado con perfil en ciclo 6 y simulamos una petición directa `POST /roles/assign` enviando `{"role_id": 2}`. La aserción comprueba que el servidor responda inequívocamente con `response.status_code == 403` y el mensaje de error correspondiente a la regla RN-03. La prueba pasa de forma automatizada en el pipeline de CI."*

---

## 📖 5. Glosario Técnico y Normativo de la Presentación

- **Ley N° 29733 (LPDP):** Ley de Protección de Datos Personales del Perú. Obliga a que el tratamiento de cualquier dato personal sea libre, previo, expreso, informado e inequívoco.
- **RBAC (Role-Based Access Control):** Control de acceso basado en roles. Modelo de seguridad que restringe el acceso al sistema en función de los roles asignados a los usuarios (Estudiante, Mentor, Administrador).
- **RLS (Row-Level Security):** Característica de seguridad de PostgreSQL que permite definir políticas a nivel de tabla para restringir qué filas puede consultar, insertar, actualizar o eliminar un usuario según su contexto de autenticación (`auth.uid()`).
- **DoD (Definition of Done):** Criterio formal acordado por el equipo Scrum para declarar terminado un incremento de software (código probado, sin errores de linting, cobertura $>90\%$, documentación de diseño actualizada y migración ejecutada).
- **Matriz Atómica 6×11:** Representación horaria semanal de 6 días (lunes a sábado) por 11 bloques de 60 minutos (08:00 a 19:00), dando un espacio discreto de 66 celdas binarias independientes.
- **Alembic:** Herramienta de migración de bases de datos para SQLAlchemy en Python. Gestiona de forma secuencial y versionada la evolución del esquema físico de la base de datos.
- **Pytest:** Framework de pruebas para Python utilizado para verificar endpoints, lógica de negocio y autorizaciones del backend.
- **Vitest:** Framework de pruebas unitarias y de componentes para Vite/Vue 3 que ejecuta pruebas rápidas en el frontend con soporte para jsdom.
- **Kroki:** Servicio de renderizado de diagramas como código que transforma especificaciones PlantUML en gráficos vectoriales SVG e imágenes rasterizadas PNG de alta resolución.

---

## 🏁 6. Checklist de Cierre para el Presentador

Antes de iniciar la exposición, verificar los siguientes puntos en el entorno:
- [x] Backend activo en puerto 8000 (`http://localhost:8000/docs`).
- [x] Frontend activo en puerto 5173 (`http://localhost:5173`).
- [x] Base de datos Supabase con migración `002_roles_and_profiles.py` aplicada.
- [x] Terminal lista para ejecutar la suite de pruebas:
  - Backend: `python -m pytest aplicacion/backend/tests/test_consent.py aplicacion/backend/tests/test_roles.py aplicacion/backend/tests/test_profiles.py aplicacion/backend/tests/test_authorization.py aplicacion/backend/tests/test_curriculum.py --no-cov`
  - Frontend: `npm --prefix aplicacion/frontend test -- --run`
- [x] Navegador con sesión limpia para demostrar el flujo de primer login con consentimiento.
