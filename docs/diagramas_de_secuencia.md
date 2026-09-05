# Diagramas de Secuencia del Sistema Web P2P

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna – Facultad de Ingeniería – Escuela Profesional de Ingeniería de Sistemas  
**Lugar y Fecha:** Tacna – Perú, 2026  

---

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | RAM / JCM | RAM | RVA | 05/09/2026 | Estructuración y formateo en Markdown de los diagramas de secuencia (PlantUML y Mermaid). |

---

## Tabla de Contenidos

1. [Introducción y Matriz de Trazabilidad](#1-introducción-y-matriz-de-trazabilidad)
2. [Flujo 1: Autenticación y Consentimiento Informado (Ley N° 29733)](#2-flujo-1-autenticación-y-consentimiento-informado-ley-n-29733)
3. [Flujo 2: Consulta y Generación del Emparejamiento Híbrido](#3-flujo-2-consulta-y-generación-del-emparejamiento-híbrido)
4. [Flujo 3: Agendamiento y Confirmación de Sesión P2P](#4-flujo-3-agendamiento-y-confirmación-de-sesión-p2p)
5. [Flujo 4: Cierre de Sesión, Evaluación y Gamificación](#5-flujo-4-cierre-de-sesión-evaluación-y-gamificación)

---

## 1. Introducción y Matriz de Trazabilidad

El presente documento modela la dinámica temporal y el intercambio de mensajes entre los distintos componentes del sistema para los casos de uso más críticos: la interfaz de usuario (*React SPA*), el servidor de aplicaciones (*Python FastAPI*), el motor de recomendación híbrido (*Scikit-Learn / NumPy*) y la capa de persistencia (*PostgreSQL / Supabase con RLS*).

### Matriz de Mapeo con Requerimientos Funcionales

| N° | Diagrama de Secuencia | Requerimientos Asociados | Actores / Componentes Principales |
| :---: | :--- | :--- | :--- |
| **1** | Autenticación y Consentimiento Informado | **RF01**, **RF02** | Estudiante, React SPA, FastAPI, Supabase DB |
| **2** | Consulta y Generación del Emparejamiento Híbrido | **RF04**, **RF05**, **RF06**, **RF07** | Estudiante Mentoreado, React SPA, FastAPI, Motor Recomendador, Supabase DB |
| **3** | Agendamiento y Confirmación de Sesión P2P | **RF08**, **RF09** | Estudiante Mentoreado, Estudiante Mentor, React SPA, FastAPI, Supabase DB |
| **4** | Cierre de Sesión, Evaluación y Gamificación | **RF10**, **RF11**, **RF12**, **RF13** | Estudiante Mentor, Estudiante Mentoreado, React SPA, FastAPI, Supabase DB |

---

## 2. Flujo 1: Autenticación y Consentimiento Informado (Ley N° 29733)

### Descripción del Flujo
Modela el acceso seguro y la validación legal obligatoria previa al consumo del sistema. En cumplimiento con la **Ley N° 29733** (Ley de Protección de Datos Personales del Perú), todo usuario en su primer inicio de sesión debe autorizar de forma expresa e informada el tratamiento de sus datos académicos y de rendimiento antes de poder acceder al panel general.

### Diagrama Visual (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User as Estudiante
    participant Frontend as Cliente Web<br/>(React SPA)
    participant API as Backend API<br/>(Python FastAPI)
    participant DB as PostgreSQL / RLS<br/>(Supabase)

    User->>Frontend: Ingresa credenciales institucionales
    Frontend->>API: POST /api/v1/auth/login (email, password)
    API->>DB: Validar credenciales y consultar estado de usuario
    DB-->>API: Usuario autenticado + estado_consentimiento

    alt Primer inicio de sesión (consentimiento == false)
        API-->>Frontend: Token provisional + Requiere Consentimiento
        Frontend->>User: Muestra Términos y Consentimiento Digital (Ley N° 29733)
        User->>Frontend: Acepta tratamiento de datos académicos
        Frontend->>API: POST /api/v1/auth/consent (user_uuid, true)
        API->>DB: UPDATE usuarios SET consent_date = NOW(), consent = true
        DB-->>API: Confirmación de actualización
    end

    API-->>Frontend: 200 OK + JWT de Sesión (Rol, UUID)
    Frontend->>User: Redirecciona al Tablero Principal (Dashboard)
```

### Código Fuente (PlantUML)

```plantuml
@startuml
autonumber
skinparam style strictuml
skinparam sequenceMessageAlign center

actor "Estudiante" as User
participant "Cliente Web\n(React SPA)" as Frontend
participant "Backend API\n(Python FastAPI)" as API
database "PostgreSQL / RLS\n(Supabase)" as DB

User -> Frontend : Ingresa credenciales institucionales
Frontend -> API : POST /api/v1/auth/login (email, password)
API -> DB : Validar credenciales y consultar estado de usuario
DB --> API : Usuario autenticado + estado_consentimiento

alt Primer inicio de sesión (consentimiento == false)
    API --> Frontend : Token provisional + Requiere Consentimiento
    Frontend -> User : Muestra Términos y Consentimiento Digital (Ley N° 29733)
    User -> Frontend : Acepta tratamiento de datos académicos
    Frontend -> API : POST /api/v1/auth/consent (user_uuid, true)
    API -> DB : UPDATE usuarios SET consent_date = NOW(), consent = true
    DB --> API : Confirmación de actualización
end

API --> Frontend : 200 OK + JWT de Sesión (Rol, UUID)
Frontend -> User : Redirecciona al Tablero Principal (Dashboard)
@enduml
```

---

## 3. Flujo 2: Consulta y Generación del Emparejamiento Híbrido

### Descripción del Flujo
Muestra la interacción entre la interfaz de usuario, la API y el motor de recomendación híbrido para generar el ranking *Top-k* de mentores sugeridos. El motor ejecuta en memoria el cálculo matricial combinando **filtrado basado en contenido** (similitud coseno entre descriptores temáticos) y **filtrado colaborativo** (ponderación histórica de calificaciones y coincidencia de horarios).

### Diagrama Visual (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor Student as Estudiante<br/>Mentoreado
    participant Frontend as Cliente Web<br/>(React SPA)
    participant API as Backend API<br/>(Python FastAPI)
    participant Engine as Motor Recomendador<br/>(Scikit-Learn / NumPy)
    participant DB as PostgreSQL<br/>(Supabase DB)

    Student->>Frontend: Selecciona materia filtro y tema de refuerzo
    Frontend->>API: GET /api/v1/recommendations?subject_id=X&topic=Y (JWT)
    API->>DB: SELECT * FROM mentores_disponibles WHERE subject_id = X
    DB-->>API: Lista de mentores, competencias y matriz histórica

    API->>Engine: calculate_hybrid_match(mentoreado_req, mentores_data)
    activate Engine
    Note over Engine: 1. Vectorizar requerimiento y temas
    Note over Engine: 2. Similitud Coseno (Filtrado de Contenido)
    Note over Engine: 3. Ponderar ratings y compatibilidad horaria (Colaborativo)
    Note over Engine: 4. Ordenar y rankear Top-k
    Engine-->>API: Lista Top-k ordenada con % de compatibilidad
    deactivate Engine

    API-->>Frontend: 200 OK (JSON con Top-k mentores)
    Frontend->>Student: Renderiza tarjetas de mentores recomendados
```

### Código Fuente (PlantUML)

```plantuml
@startuml
autonumber
skinparam style strictuml
skinparam sequenceMessageAlign center

actor "Estudiante\nMentoreado" as Student
participant "Cliente Web\n(React SPA)" as Frontend
participant "Backend API\n(Python FastAPI)" as API
participant "Motor Recomendador\n(Scikit-Learn / NumPy)" as Engine
database "PostgreSQL\n(Supabase DB)" as DB

Student -> Frontend : Selecciona materia filtro y tema de refuerzo
Frontend -> API : GET /api/v1/recommendations?subject_id=X&topic=Y (JWT)
API -> DB : SELECT * FROM mentores_disponibles WHERE subject_id = X
DB --> API : Lista de mentores, competencias y matriz histórica

API -> Engine : calculate_hybrid_match(mentoreado_req, mentores_data)
activate Engine
Engine -> Engine : 1. Vectorizar requerimiento y temas
Engine -> Engine : 2. Similitud Coseno (Filtrado de Contenido)
Engine -> Engine : 3. Ponderar ratings y compatibilidad horaria (Colaborativo)
Engine -> Engine : 4. Ordenar y rankear Top-k
Engine --> API : Lista Top-k ordenada con % de compatibilidad
deactivate Engine

API --> Frontend : 200 OK (JSON con Top-k mentores)
Frontend -> Student : Renderiza tarjetas de mentores recomendados
@enduml
```

---

## 4. Flujo 3: Agendamiento y Confirmación de Sesión P2P

### Descripción del Flujo
Describe la reserva directa de franjas horarias y la sincronización asíncrona entre pares estudiantiles. Una vez que el mentoreado elige un bloque disponible, el estado de la sesión se fija como `PENDIENTE` y el horario pasa a `RESERVADO` para evitar colisiones. El mentor es notificado internamente para confirmar o rechazar la sesión.

### Diagrama Visual (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor Student as Estudiante<br/>Mentoreado
    participant Frontend as Cliente Web<br/>(React SPA)
    participant API as Backend API<br/>(FastAPI)
    participant DB as PostgreSQL<br/>(Supabase DB)
    actor Mentor as Estudiante<br/>Mentor

    Student->>Frontend: Selecciona mentor del Top-k y elige bloque horario
    Frontend->>API: POST /api/v1/sessions/book (mentor_id, slot_id, topic)
    API->>DB: INSERT INTO sesiones (status='PENDIENTE')<br/>UPDATE horarios SET status='RESERVADO'
    DB-->>API: Sesión registrada con éxito
    API-->>Frontend: 201 Created (Sesión programada)
    Frontend->>Student: Muestra confirmación de reserva pendiente

    API-)Mentor: Notificación interna: "Nueva solicitud de mentoría"
    Mentor->>Frontend: Accede a su panel y revisa solicitud
    Mentor->>Frontend: Hace clic en "Aceptar Sesión"
    Frontend->>API: PATCH /api/v1/sessions/{id}/confirm
    API->>DB: UPDATE sesiones SET status='CONFIRMADA' WHERE id={id}
    DB-->>API: Registro actualizado
    API-->>Frontend: 200 OK
    Frontend->>Mentor: Actualiza vista de agenda confirmada
```

### Código Fuente (PlantUML)

```plantuml
@startuml
autonumber
skinparam style strictuml
skinparam sequenceMessageAlign center

actor "Estudiante\nMentoreado" as Student
participant "Cliente Web\n(React SPA)" as Frontend
participant "Backend API\n(FastAPI)" as API
database "PostgreSQL\n(Supabase DB)" as DB
actor "Estudiante\nMentor" as Mentor

Student -> Frontend : Selecciona mentor del Top-k y elige bloque horario
Frontend -> API : POST /api/v1/sessions/book (mentor_id, slot_id, topic)
API -> DB : INSERT INTO sesiones (status='PENDIENTE')\nUPDATE horarios SET status='RESERVADO'
DB --> API : Sesión registrada con éxito
API --> Frontend : 201 Created (Sesión programada)
Frontend -> Student : Muestra confirmación de reserva pendiente

API -> Mentor : Notificación interna: "Nueva solicitud de mentoría"
Mentor -> Frontend : Accede a su panel y revisa solicitud
Mentor -> Frontend : Hace clic en "Aceptar Sesión"
Frontend -> API : PATCH /api/v1/sessions/{id}/confirm
API -> DB : UPDATE sesiones SET status='CONFIRMADA' WHERE id={id}
DB --> API : Registro actualizado
API --> Frontend : 200 OK
Frontend -> Mentor : Actualiza vista de agenda confirmada
@enduml
```

---

## 5. Flujo 4: Cierre de Sesión, Evaluación y Gamificación

### Descripción del Flujo
Modela el ciclo de retroalimentación post-mentoría: registro formal de temas impartidos, valoración numérica (1 a 5 estrellas) con reseña por parte del mentoreado, y ejecución de la transacción de gamificación (acumulación de horas de servicio universitario y actualización de reputación e insignias del mentor).

### Diagrama Visual (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor Student as Estudiante<br/>Mentoreado
    participant Frontend as Cliente Web<br/>(React SPA)
    participant API as Backend API<br/>(FastAPI)
    participant DB as PostgreSQL<br/>(Supabase DB)
    actor Mentor as Estudiante<br/>Mentor

    Mentor->>Frontend: Marca sesión como "Completada" y registra temas
    Frontend->>API: POST /api/v1/sessions/{id}/complete (log_notes)
    API->>DB: UPDATE sesiones SET status='COMPLETADA', completed_at=NOW()
    DB-->>API: OK

    Frontend->>Student: Solicita evaluación post-mentoría
    Student->>Frontend: Envía valoración (1 a 5 estrellas + reseña)
    Frontend->>API: POST /api/v1/reviews (session_id, rating, feedback)

    rect rgb(240, 245, 255)
        Note over API,DB: Transacción de Gamificación y Horas
        API->>DB: INSERT INTO calificaciones (rating, feedback)
        API->>DB: UPDATE mentores SET total_horas = total_horas + duracion_sesion
        API->>DB: Recalcular reputación promedio y verificar insignias
        DB-->>API: Datos actualizados
    end

    API-->>Frontend: 200 OK (Métricas actualizadas)
    Frontend->>Student: Muestra mensaje de agradecimiento
    Frontend->>Mentor: Actualiza contador de horas e insignias en su perfil
```

### Código Fuente (PlantUML)

```plantuml
@startuml
autonumber
skinparam style strictuml
skinparam sequenceMessageAlign center

actor "Estudiante\nMentoreado" as Student
participant "Cliente Web\n(React SPA)" as Frontend
participant "Backend API\n(FastAPI)" as API
database "PostgreSQL\n(Supabase DB)" as DB
actor "Estudiante\nMentor" as Mentor

Mentor -> Frontend : Marca sesión como "Completada" y registra temas
Frontend -> API : POST /api/v1/sessions/{id}/complete (log_notes)
API -> DB : UPDATE sesiones SET status='COMPLETADA', completed_at=NOW()
DB --> API : OK

Frontend -> Student : Solicita evaluación post-mentoría
Student -> Frontend : Envía valoración (1 a 5 estrellas + reseña)
Frontend -> API : POST /api/v1/reviews (session_id, rating, feedback)

group Transacción de Gamificación y Horas
    API -> DB : INSERT INTO calificaciones (rating, feedback)
    API -> DB : UPDATE mentores SET total_horas = total_horas + duracion_sesion
    API -> DB : Recalcular reputación promedio y verificar insignias
    DB --> API : Datos actualizados
end

API --> Frontend : 200 OK (Métricas actualizadas)
Frontend -> Student : Muestra mensaje de agradecimiento
Frontend -> Mentor : Actualiza contador de horas e insignias en su perfil
@enduml
```