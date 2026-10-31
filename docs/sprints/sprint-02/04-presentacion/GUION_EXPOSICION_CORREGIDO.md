# Guion de Exposición Técnica, Presentación Formal y Defensa de Arquitectura — Sprint 02
## «Gobernanza de Consentimiento Digital (Ley N° 29733), Jerarquía de Roles y Mérito Académico, Catálogo Avanzado y Perfiles con Matriz de Disponibilidad Horaria Semanal»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Institución:** Universidad Privada de Tacna (UPT) — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas (EPIS)  
**Curso:** Construcción de Software I (Semestre 2026-II)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Código del Documento:** `GUION-S02-V2.0`  
**Autores Oficiales:** Joan Cristian Medina Quispe (2022074255) y Renzo Antonio Antayhua Mamani (2022073504)  
**Fecha de Presentación Oficial:** 24 de Octubre de 2026 (según cronograma del plan maestro)  
**Audiencia Objetivo:** Docente de Cátedra, Evaluadores Técnicos, Arquitectos de Software y Estudiantes de la EPIS-UPT  

---

## 1. Propósito y Estructura Pedagógica del Guion

Este documento constituye la guía formal para la exposición técnica y defensa metodológica del **Sprint 02**. Su propósito es proporcionar al equipo expositor la fundamentación de **por qué** se diseñó de esta forma el sistema, **qué requerimientos oficiales** lo respaldan, **cómo funciona internamente la arquitectura** bajo el modelo 4+1, y **cómo se verificó con 150 pruebas automatizadas sin fallos**.

La defensa se estructura en torno al principio de **Trazabilidad Continua en 12 Eslabones Canónicos**:
$$\text{PBI} \longrightarrow \text{RF/RNF} \longrightarrow \text{RN} \longrightarrow \text{HU} \longrightarrow \text{CUS} \longrightarrow \text{Narrativa SRS} \longrightarrow \text{Diag. SRS} \longrightarrow \text{Diag. SAD} \longrightarrow \text{Código Fuente} \longrightarrow \text{Pruebas} \longrightarrow \text{Evidencias} \longrightarrow \text{Métricas}$$

---

## 2. Los 4 Pilares Funcionales y Técnicos del Sprint 02

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CADENA DE TRAZABILIDAD SPRINT 02                      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│    PILAR A    │              │    PILAR B    │              │   PILAR C/D   │
│ CONSENTIMIENTO│              │ ROLES Y MÉRITO│              │ MALLA Y AGENDA│
│ (Ley N° 29733)│              │    (RN-03)    │              │ (Matriz 6×11) │
└───────┬───────┘              └───────┬───────┘              └───────┬───────┘
        ▼                              ▼                              ▼
  RF02 / RN-02                   RF03 / RN-03                   RF05, RF04, RNF09
  HU-03 / CUS01                  HU-04 / CUS10                  HU-05, HU-06 / CUS21, CUS15
        ▼                              ▼                              ▼
Diagramas 08, 09, 13           Diagramas 08, 10, 13           Diagramas 08, 11, 14
(CUS / Secuencia / Estados)    (CUS / Secuencia / Mérito)     (CUS / Secuencia / ERD)
        ▼                              ▼                              ▼
ConsentModalView.tsx           RoleSelector (UI)              CurriculumCatalogView.tsx
consent.py / consent_service   roles.py / role_service        ProfileAvailabilityView.tsx
RLS consentimientos_legales    RLS usuario_roles              profiles.py / profile_service
        ▼                              ▼                              ▼
CUS01-U01..A01 (19 tests)      CUS10-U01..A01 (12 tests)      CUS21/CUS15-U01..A01 (48 tests)
```

---

### 2.1. Pilar A: Consentimiento Legal Informado y Protección de Datos

1. **Necesidad del Negocio:** Almacenar perfiles académicos, notas o historiales de estudiantes universitarios sin autorización expresa vulnera la Ley N° 29733 (Ley de Protección de Datos Personales). Sin consentimiento previo e inequívoco, la plataforma se expondría a sanciones y desconfianza.
2. **Requerimiento Funcional y No Funcional:** `RF02` (Formalización del Consentimiento Informado Digital) y `RNF02` (Privacidad, Aislamiento y Protección de Datos Académicos).
3. **Regla de Negocio:** `RN-02` — Consentimiento Legal Digital: todo estudiante debe consentir expresamente el tratamiento de sus datos con fines formativos en su primer login. El rechazo o revocación bloquea de inmediato las funciones operativas del sistema.
4. **Historia de Usuario:** `HU-03` — Criterios de aceptación en Gherkin: modal forzado en primer inicio de sesión, persistencia de versión, dirección IP y marca temporal UTC, y revocación con terminación de sesión.
5. **Caso de Uso y Narrativa:** `CUS01` (Iniciar Sesión Institucional con 2FA y Consentimiento Legal). Flujo principal de aceptación y flujos alternativos de rechazo/revocación.
6. **Diagramas de Respaldo:**
   - Análisis: Diagrama de Casos de Uso del Sprint 02 (`08_diagrama_casos_de_uso_sprint02.png`).
   - Arquitectura: Diagrama de Secuencia de Consentimiento (`09_secuencia_consentimiento_ley29733.png`) y Máquina de Estados del Consentimiento (`13_maquina_estados_consentimiento_roles.png`).
7. **Implementación Técnica Real:**
   - Frontend: `aplicacion/frontend/src/components/ConsentModalView.tsx` y servicio tipado `src/services/consentService.ts`.
   - Backend: `aplicacion/backend/app/api/v1/endpoints/consent.py` y servicio `app/services/consent_service.py` con endpoints `POST /consent` y `GET /consent/history`.
   - Base de Datos: Tabla `consentimientos_legales` con política RLS `consent_owner_all`.
8. **Pruebas y Validación:** Casos `CUS01-U03`, `CUS01-F01`, `CUS01-F02`, `CUS01-A01` del Catálogo Excel; pruebas automatizadas en `aplicacion/backend/tests/test_consent.py` (14 tests) y `ConsentModalView.test.tsx` (4 tests).
9. **Métricas y Resultados:** 100% de cobertura en trazabilidad legal; 0 bypasses posibles gracias al aislamiento nativo por base de datos. *(Nota ética: la implementación se alinea con la Ley 29733, pendiente de certificación jurídica institucional externa).*

---

### 2.2. Pilar B: Asignación de Roles y Verificación de Mérito Académico

1. **Necesidad del Negocio:** Para que el modelo de mentoría entre pares funcione con solvencia pedagógica, un estudiante de primeros ciclos no puede instruir a sus compañeros en materias avanzadas. Solo los alumnos con madurez académica (ciclo VII o superior) deben ejercer la mentoría.
2. **Requerimiento Funcional:** `RF03` (Gestión y Asignación Administrativa de Roles de Usuario).
3. **Regla de Negocio:** `RN-03` — Restricción de Mérito Académico: el rol de Mentor (`rol_id = 2` o `'mentor'`) está reservado exclusivamente a estudiantes con `ciclo_actual >= 7`. Estudiantes de ciclos I a VI solo pueden ser Mentoreados (`'estudiante'`).
4. **Historia de Usuario:** `HU-04` — Criterios de aceptación: advertencia reactiva en cliente y rechazo estricto en backend ante postulaciones fraudulentas.
5. **Caso de Uso y Narrativa:** `CUS10` (Gestionar Asignación y Elevación de Roles). Flujo principal para alumnos de ciclo $\ge \text{VII}$; flujo de excepción si `ciclo_actual < 7` denegado con **HTTP 400 Bad Request** (`MERIT_RULE_VIOLATION`); intento de autopromoción denegado con **HTTP 403 Forbidden**.
6. **Diagramas de Respaldo:**
   - Arquitectura: Diagrama de Secuencia de Mérito RN-03 (`10_secuencia_roles_merito_rn03.png`), Máquina de Estados de Roles (`13_maquina_estados_consentimiento_roles.png`) y Modelo Entidad-Relación (`14_diagrama_entidad_relacion_sprint02.png`).
7. **Implementación Técnica Real:**
   - Frontend: Control reactivo de selección en `aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`.
   - Backend: `aplicacion/backend/app/api/v1/endpoints/roles.py` y `app/services/role_service.py` validando explícitamente:
     ```python
     if ciclo < 7:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail={"code": "MERIT_RULE_VIOLATION", "message": "Conforme a RN-03..."}
         )
     ```
     Y para autopromoción no autorizada:
     ```python
     if caller_email == payload.email and "administrador" not in caller_roles:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Autopromoción no permitida...")
     ```
   - Base de Datos: Tablas `roles` y `usuario_roles` con políticas RLS de lectura global y modificación restringida.
8. **Pruebas y Validación:** Casos `CUS10-U01`, `CUS10-U02`, `CUS10-U03`, `CUS10-F01`, `CUS10-A01` del Catálogo Excel; pruebas automatizadas en `aplicacion/backend/tests/test_roles.py` (12 tests pasando) y `test_authorization.py`.
9. **Métricas y Resultados:** Imposibilidad técnica de vulnerar el mérito académico, garantizando la credibilidad pedagógica de la plataforma.

---

### 2.3. Pilar C: Catálogo y Malla Curricular Oficial de la EPIS-UPT

1. **Necesidad del Negocio:** En sistemas informales de tutoría, los alumnos publican ofertas con nombres ambiguos o informales ("Mate 1", "Progra"), destruyendo la capacidad algorítmica de recomendación. Se requiere una taxonomía normalizada vinculada al Plan de Estudios de la EPIS-UPT.
2. **Requerimiento Funcional:** `RF05` (Gestión del Catálogo de Asignaturas Críticas y Temarios Silábicos).
3. **Regla de Negocio:** Alineación con el Plan de Estudios vigente, estructurando asignaturas por código, créditos, ciclo lectivo (I al X) y unidades temáticas silábicas.
4. **Historia de Usuario:** `HU-05` — Búsqueda predictiva en tiempo real y filtrado facetado por ciclo.
5. **Caso de Uso y Narrativa:** `CUS21` (Explorar Malla Curricular y Cursos).
6. **Diagramas de Respaldo:**
   - Análisis: Diagrama de Casos de Uso del Sprint 02 (`08_diagrama_casos_de_uso_sprint02.png`).
   - Arquitectura: Diagrama Entidad-Relación (`14_diagrama_entidad_relacion_sprint02.png`), tablas `asignaturas_filtro` y `temas_conceptuales`.
7. **Implementación Técnica Real:**
   - Frontend: `aplicacion/frontend/src/components/CurriculumCatalogView.tsx`.
   - Backend: `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y modelos en `app/models/curriculum.py`.
8. **Pruebas y Validación:** Casos `CUS21-U01`, `CUS21-U02`, `CUS21-F01`, `CUS21-A01`; suites `CurriculumCatalogView.test.tsx` (6 tests) y `test_curriculum.py` (8 tests).
9. **Métricas y Resultados:** Consulta subsegundo en UI (<50 ms en backend), filtrado en memoria sin peticiones redundantes.

---

### 2.4. Pilar D: Perfiles Formativos y Disponibilidad Horaria Semanal (6×11)

1. **Necesidad del Negocio:** El motor de recomendación Top-k (Sprint 4) requiere conocer los horarios libres comunes entre mentores y mentoreados para calcular la compatibilidad de agenda.
2. **Requerimiento Funcional y No Funcional:** `RF04` (Configuración de Perfil Formativo y Matriz de Disponibilidad Horaria), `RNF07` (Consistencia Transaccional ACID) y `RNF02` (Aislamiento de Datos).
3. **Regla de Negocio:** Matriz horaria semanal discreta de **6 días (Lunes a Sábado) × 11 bloques horarios (08:00 a 19:00)** = 66 celdas binarias; validación de orden temporal estricto (`hora_inicio < hora_fin`).
4. **Historia de Usuario:** `HU-06` — Configuración de perfil formativo y marcado visual de franjas horarias libres.
5. **Caso de Uso y Narrativa:** `CUS15` (Configurar Perfil Formativo y Matriz Horaria).
6. **Diagramas de Respaldo:**
   - Arquitectura: Diagrama de Secuencia de Reemplazo Atómico (`11_secuencia_perfil_disponibilidad_atomic.png`), Secuencia de Aislamiento RLS (`12_secuencia_seguridad_multiusuario_rls.png`) y Modelo ER (`14_diagrama_entidad_relacion_sprint02.png`).
7. **Implementación Técnica Real:**
   - Frontend: `aplicacion/frontend/src/components/ProfileAvailabilityView.tsx` y `src/services/profileService.ts`.
   - Backend: `aplicacion/backend/app/api/v1/endpoints/profiles.py` y `app/services/profile_service.py`. Reemplazo atómico transaccional:
     ```python
     # Transacción ACID: borrado previo e inserción masiva
     db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == clean_email).delete()
     db.bulk_save_objects(nuevas_franjas)
     db.commit()
     ```
   - Base de Datos: Tablas `perfiles_academicos` y `disponibilidades_horarias` con políticas RLS activas (`supabase_rls_sprint02.sql`).
8. **Pruebas y Validación:** Casos `CUS15-U01`, `CUS15-U02`, `CUS15-F01`, `CUS15-A01` del Catálogo Excel; pruebas automatizadas en `test_profiles.py` (22 tests), `ProfileAvailabilityView.test.tsx` (6 tests) y `test_authorization.py` (11 tests).
9. **Métricas y Resultados:** Reemplazo atómico sin registros huérfanos; cero solapamientos; aislamiento multi-usuario certificado con RLS.

---

## 3. Guion de Diapositivas: Estructura Pedagógica de la Presentación

### Diapositiva 1: Portada Académica Formal
- **Título:** Sistema Web P2P de Mentorías Académicas — EPIS UPT
- **Subtítulo:** Defensa Técnica y Trazabilidad de Construcción — Sprint 02
- **Datos Oficiales:** Construcción de Software I (2026-II) | Docente: Dr. Ricardo Eduardo Valcárcel Alvarado | Integrantes: Joan Cristian Medina Quispe (2022074255) y Renzo Antonio Antayhua Mamani (2022073504)
- **Notas del Orador:** «Buenos días, Dr. Valcárcel y evaluadores. Presentamos la defensa técnica del Sprint 02, donde demostraremos la trazabilidad bidireccional entre los requerimientos aprobados en el SRS, las decisiones de arquitectura del SAD, el código React/FastAPI implementado y la verificación empírica de 150 pruebas automatizadas sin fallos.»

### Diapositiva 2: Planteamiento del Problema y Objetivos del Sprint 02
- **Contenido:**
  - El desafío del Sprint 02: cómo dotar a la plataforma de gobernanza legal, validación estricta de mérito académico y disponibilidad horaria estructurada.
  - Los 5 PBI abordados: PB-003, PB-005, PB-006, PB-007 y PB-008.
  - Distribución del esfuerzo: 14 horas de desarrollo (Joan 7 h, Renzo 7 h).
- **Notas del Orador:** «En el Sprint 01 sentamos la base de acceso OTP y CI. En este Sprint 02 abordamos cuatro problemas críticos: la protección legal de los datos del estudiante bajo la Ley N° 29733, la garantía de que solo alumnos destacados puedan ser mentores (RN-03), la normalización curricular oficial y la captura atómica de disponibilidades horarias en una grilla de 6×11.»

### Diapositiva 3: Cadena de Trazabilidad Integral (Los 12 Eslabones)
- **Contenido:**
  - Diagrama de flujo de trazabilidad desde la necesidad hasta la prueba automatizada.
  - Cuadro resumen de los 5 PBI, tareas T-04 a T-13 y su mapeo exacto a casos de uso CUS01, CUS10, CUS15, CUS21.
- **Notas del Orador:** «Ninguna línea de código de este incremento se desarrolló sin justificación. Cada componente responde a una cadena formal: el PBI se desglosa en requerimientos del SRS, se formaliza en historias de usuario con criterios Gherkin, se modela en diagramas UML del SAD y se valida con pruebas unitarias y de integración.»

### Diapositiva 4: Análisis Funcional — Historias de Usuario HU-03 a HU-07
- **Contenido:**
  - `HU-03` (Consentimiento Digital): modal obligatorio y persistencia de auditoría.
  - `HU-04` (Mérito Académico RN-03): exclusión estricta de ciclo $< 7$.
  - `HU-05` (Catálogo Curricular): búsqueda predictiva silábica.
  - `HU-06` (Perfil y Matriz 6×11): configuración de agenda semanal.
  - `HU-07` (Seguridad RLS): aislamiento multiusuario y prevención de fugas.
- **Notas del Orador:** «Las historias de usuario no son meros enunciados informales; todas cuentan con criterios de aceptación en sintaxis Gherkin (Dado/Cuando/Entonces), cubriendo tanto los caminos felices como los flujos de rechazo y excepción.»

### Diapositiva 5: Modelo 4+1 — Vistas Arquitectónicas del Incremento
- **Contenido:**
  - Vista de Casos de Uso: Diagrama 08 (delimitación de actores y casos).
  - Vista Lógica: Patrón desacoplado React SPA + FastAPI RESTful.
  - Vista de Procesos: Diagramas de secuencia 09, 10 y 11.
  - Vista de Desarrollo / Seguridad: Diagrama 12 (políticas RLS).
  - Vista de Datos: Diagrama 14 (Modelo ER físico con 5 tablas en 3FN).
- **Notas del Orador:** «Aplicamos el modelo 4+1 de Philippe Kruchten documentado en el SAD FD04 v2.1. Cada vista responde a una inquietud arquitectónica concreta: la vista lógica define las interfaces Pydantic; la de procesos, la concurrencia y transaccionalidad; la de datos, la integridad referencial; y la de seguridad, el aislamiento mediante RLS.»

### Diapositiva 6: Diseño Técnico — Consentimiento y Gobernanza (RN-02)
- **Contenido:**
  - Diagrama de Secuencia 09 (`09_secuencia_consentimiento_ley29733.png`).
  - Máquina de Estados 13 (`13_maquina_estados_consentimiento_roles.png`).
  - Explicación de la persistencia de IP, User-Agent, versión y timestamp UTC inmutable.
- **Notas del Orador:** «Observen el diagrama de secuencia 09. Si el estudiante rechaza el consentimiento, la sesión se aborta de inmediato y el token de acceso queda invalidado. Si acepta, se registra la marca temporal UTC en base de datos. Ningún usuario puede interactuar con el sistema sin este consentimiento explícito.»

### Diapositiva 7: Diseño Técnico — Restricción de Mérito Académico (RN-03)
- **Contenido:**
  - Diagrama de Secuencia 10 (`10_secuencia_roles_merito_rn03.png`).
  - La distinción semántica fundamental:
    - Incumplimiento de mérito (`ciclo_actual < 7`): **HTTP 400 Bad Request** (`MERIT_RULE_VIOLATION`).
    - Autopromoción sin privilegios de administrador: **HTTP 403 Forbidden**.
- **Notas del Orador:** «La regla RN-03 protege la solvencia de la mentoría. Aplicamos Defensa en Profundidad: en el frontend, el selector advierte que la mentoría exige ciclo VII o superior; si un usuario intenta saltarse la interfaz e invocar la API por curl, el backend consulta el perfil y responde de forma determinista con HTTP 400 Bad Request. Y si intenta autopromoverse sin rol de administrador, responde HTTP 403 Forbidden.»

### Diapositiva 8: Diseño Técnico — Perfil y Matriz Semanal Transaccional (6×11)
- **Contenido:**
  - Diagrama de Secuencia 11 (`11_secuencia_perfil_disponibilidad_atomic.png`).
  - Diagrama Entidad-Relación 14 (`14_diagrama_entidad_relacion_sprint02.png`).
  - Algoritmo de reemplazo atómico transaccional ACID en SQLAlchemy.
- **Notas del Orador:** «La disponibilidad se organiza en una grilla discreta de 6 días por 11 franjas horarias. Para evitar solapamientos o franjas huérfanas ante caídas de conexión, el servicio ejecuta una transacción ACID: elimina las franjas anteriores del usuario e inserta el nuevo bloque masivo en una única operación atómica.»

### Diapositiva 9: Diseño Técnico — Seguridad Multi-Inquilino y Supabase RLS
- **Contenido:**
  - Diagrama de Secuencia 12 (`12_secuencia_seguridad_multiusuario_rls.png`).
  - Políticas de Row Level Security sobre las 5 tablas relacionales.
  - Extracción segura del claim `auth.jwt() ->> 'email'`.
- **Notas del Orador:** «La seguridad no descansa únicamente en FastAPI. Aunque un programador cometa un descuido en un endpoint omitiendo el filtro de usuario, PostgreSQL aplica Row Level Security a nivel del motor de base de datos. Un estudiante jamás podrá ver ni modificar la disponibilidad o perfil de otro.»

### Diapositiva 10: Evidencias de la Aplicación en Ejecución
- **Contenido:**
  - Capturas reales del sistema: modal legal (01), catálogo predictivo (02), validación de mérito (03), grilla horaria 6×11 (04) y Swagger OpenAPI (05).
  - Breve ficha técnica por captura: componente, archivo y tarea.
- **Notas del Orador:** «Estas son capturas auténticas del sistema en ejecución sobre la rama de integración. Podemos observar el modal accesible de la Ley 29733, la búsqueda silábica en tiempo real, la advertencia visual de mérito y la grilla de disponibilidad semanal.»

### Diapositiva 11: Verificación, Catálogo Oficial y Batería de Pruebas
- **Contenido:**
  - Vinculación con el Catálogo Excel `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`.
  - Desglose de las 150 pruebas automatizadas acumuladas al corte del Sprint 02:
    - 84 en Backend con Pytest (cobertura **90.64%**).
    - 66 en Frontend con Vitest (cobertura **91.10%**).
  - Pruebas positivas (112) frente a pruebas negativas/seguridad (38).
- **Notas del Orador:** «Acreditamos empíricamente la calidad del software con 150 pruebas automatizadas pasando al 100%. Ambas capas superan holgadamente el 70% exigido en el requerimiento RNF09, alcanzando 90.64% en backend y 91.10% en frontend. Hemos probado exhaustivamente tanto los caminos felices como los intentos de ataque y datos inválidos.»

### Diapositiva 12: Demostración en Vivo y Protocolo de Contingencia
- **Contenido:**
  - Flujo secuencial de 7 pasos para la demostración en vivo.
  - Cuentas de demostración sanitizadas (sin datos personales reales).
  - Procedimiento alternativo de contingencia con capturas y suites locales.
- **Notas del Orador:** «Procederemos con la demostración en vivo siguiendo un guion reproducible: iniciaremos sesión con un usuario nuevo para ver el consentimiento; demostraremos el bloqueo por rechazo; exploraremos el catálogo silábico; intentaremos postular a mentor con ciclo 4 para evidenciar el rechazo por mérito; configuraremos la matriz horaria semanal y verificaremos la persistencia y las pruebas en consola.»

### Diapositiva 13: Conclusiones y Transición hacia los Sprints 03 y 04
- **Contenido:**
  - Balance de los 5 PBI concluidos al 100%.
  - Respeto del presupuesto de 14 horas de esfuerzo.
  - Habilitación para la publicación de ofertas docentes (Sprint 3) y el algoritmo Top-k EdRecSys (Sprint 4).
- **Notas del Orador:** «El Sprint 02 concluye con el 100% de los compromisos cumplidos y verificados. Agradecemos su atención y quedamos atentos a las preguntas de la cátedra.»

---

## 4. Banco de Preguntas y Respuestas Técnicas (Defensa de Arquitectura)

#### P1: ¿Por qué eligieron React 19 y FastAPI en lugar de un framework monolítico como Django o Laravel?
> **Respuesta del Orador:**  
> «Por estricto apego al requerimiento no funcional **RNF09**, que prescribe una arquitectura desacoplada y modular. FastAPI proporciona validación estricta de tipos en tiempo de compilación/ejecución con Pydantic v2 y serialización asíncrona de altísima velocidad, ideal para el motor de recomendación. Por su parte, React 19 con TypeScript permite una grilla horaria interactiva de 6×11 altamente reactiva sin recargas de página, asegurando la separación nítida entre la lógica de presentación y los servicios de negocio.»

#### P2: ¿Por qué el rechazo de mérito académico (RN-03) devuelve HTTP 400 Bad Request y no HTTP 403 Forbidden?
> **Respuesta del Orador:**  
> «Porque responde a la semántica estándar de HTTP y REST. Una solicitud donde un estudiante de ciclo inferior a VII postula a mentor contiene un error semántico en los datos de entrada según las reglas del dominio de negocio (**RN-03**); por ello, el backend responde **HTTP 400 Bad Request** con el código de error estructurado `MERIT_RULE_VIOLATION`. En contraste, **HTTP 403 Forbidden** se reserva exclusivamente para fallos de autorización: cuando el usuario está autenticado pero carece de permisos para ejecutar la acción solicitada, como ocurre cuando un estudiante intenta autopromoverse a mentor sin privilegios de administrador institucional.»

#### P3: ¿Cómo garantiza el sistema que la base de datos no quede con horarios corruptos si falla la conexión mientras el usuario guarda su matriz semanal?
> **Respuesta del Orador:**  
> «Mediante el patrón de **Reemplazo Atómico Transaccional** implementado en `aplicacion/backend/app/services/profile_service.py` bajo el requerimiento **RNF07**. Toda la operación de guardado se ejecuta dentro de un único bloque de transacción ACID de SQLAlchemy. El algoritmo ejecuta primero el borrado de las franjas previas del usuario (`db.delete`) y a continuación la inserción masiva (`bulk_save_objects`). Si ocurre cualquier anomalía o fallo en una franja, se dispara automáticamente un `db.rollback()`. Es imposible que la agenda quede parcialmente guardada.»

#### P4: ¿Por qué afirman que la plataforma respeta la Ley N° 29733 si no cuentan con una certificación de la autoridad de protección de datos?
> **Respuesta del Orador:**  
> «Aclaramos con rigor académico que nuestro proyecto ha implementado los **mecanismos técnicos de control** inspirados en los principios rectores de la Ley N° 29733 (consentimiento libre, previo, expreso, informado e inequívoco, registro de marca temporal UTC inmutable, dirección IP y bloqueo funcional por rechazo). Reconocemos abiertamente que no constituye una certificación jurídica formal emitida por la Dirección General de Protección de Datos Personales, sino un incremento de software universitario técnicamente alineado a la normativa vigente.»

#### P5: ¿Cómo demuestran que un estudiante no puede alterar la matriz horaria de otro compañero enviando una petición HTTP directa con curl?
> **Respuesta del Orador:**  
> «Mediante dos capas de seguridad. En la capa de aplicación, el endpoint `/api/v1/profiles` extrae la identidad del usuario a partir del token Bearer JWT firmado criptográficamente, ignorando cualquier identificador arbitrario en la URL. En la capa de persistencia, Supabase PostgreSQL tiene activas políticas de **Row Level Security (RLS)** documentadas en `scripts/supabase_rls_sprint02.sql`. Aunque existiese una vulnerabilidad en la consulta del backend, el motor de base de datos filtra automáticamente con `USING (email = auth.jwt() ->> 'email')`. Esto se probó automatizadamente en la suite `test_authorization.py` con 11 pruebas pasando.»

---

## 5. Recorrido Reproducible para la Demostración en Vivo

1. **Precondición:** Backend ejecutándose en `http://localhost:8000` y Frontend en `http://localhost:5173`. Base de datos con migración `002_roles_and_profiles.py` aplicada.
2. **Paso 1 (Inicio de Sesión y Modal Legal):** Ingresar con un correo institucional nuevo `@upt.pe`. El sistema despliega el modal obligatorio de consentimiento de la **Ley N° 29733**.
3. **Paso 2 (Bloqueo por Rechazo RN-02):** Hacer clic en "Rechazar". El sistema muestra una alerta de terminación de sesión y bloquea la navegación, confirmando la regla **RN-02**.
4. **Paso 3 (Aceptación y Persistencia):** Reingresar y hacer clic en "Aceptar Consentimiento". El sistema persiste la marca temporal UTC y da acceso al catálogo y perfil.
5. **Paso 4 (Exploración Curricular CUS21):** Navegar a "Catálogo Curricular". Escribir "Algoritmos" en el buscador interactivo; filtrar por Ciclo III; expandir las unidades temáticas silábicas oficiales.
6. **Paso 5 (Validación de Mérito RN-03):** Ir a "Mi Perfil". Indicar `Ciclo Actual: IV` e intentar seleccionar el rol de "Mentor". El frontend muestra la advertencia institucional de mérito formativo.
7. **Paso 6 (Matriz Horaria Semanal CUS15):** Seleccionar 6 bloques horarios en la grilla semanal de 6×11 (Lunes, Miércoles y Viernes de 08:00 a 10:00). Guardar los cambios.
8. **Paso 7 (Verificación de Persistencia y Pruebas):** Recargar la página para confirmar que la agenda persiste íntegra. Abrir la terminal y ejecutar `pytest` y `npm test` para evidenciar las 150 pruebas en verde.
