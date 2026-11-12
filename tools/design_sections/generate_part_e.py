# -*- coding: utf-8 -*-
"""
Generator for Part E of docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
Covers:
- Sección 6.3.4: Diagramas de Clases del Modelo Lógico - Diagrama 6.16 y 24 vistas lógicas parciales (Diagramas 6.16.1 al 6.16.24)
- Sección 6.3.5: Máquinas de Estados Finitas (FSM) - Diagramas 6.17, 6.18, 6.19
- Sección 6.3.6: Modelo Físico de Base de Datos Relacional y Diccionario DDL - Diagrama 6.20, Diccionario de 15 tablas y RLS
"""

from design_sections.generate_part_c import CUS_METADATA

def generate_class_diagram(cid, idx, name, mod_code, mod_name, b_name, c_name, e_name):
    clean_c = c_name.split(" / ")[0].strip().split()[0]
    e_first = e_name.split(",")[0].strip()
    return f"""### 6.3.4.{idx}. {cid} – Vista Lógica Parcial de Clases: {name}

La vista lógica parcial para `{cid}` delimita el conjunto de clases de dominio, servicios de aplicación y adaptadores de infraestructura que participan en la ejecución del caso de uso dentro de `{mod_code}: {mod_name}`. Se explicitan los atributos privados fuertemente tipados, las operaciones públicas de verificación de negocio y las relaciones estructurales de composición y dependencia.

#### Diagrama 6.16.{idx}: Diagrama de Clases Lógico Parcial - {cid}: {name}

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - {cid}: {name}\\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {{
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}}

class "{clean_c}" as Controller {{
  +ejecutarOperacion(payload: DTO): ResponseDTO
  -validarReglasNegocio(db: Session): Boolean
}}

class "{e_first}" as Entity {{
  -id: UUID
  -estado: String
  -fecha_creacion: DateTime
  +actualizarEstado(nuevo: String): Void
}}

Controller ..> Entity : manipula
@enduml
```

Fuente: Elaboración propia a partir del diseño de {mod_code}.
"""

def get_part_e():
    out = []
    
    # Header 6.3.4
    out.append(r'''## 6.3.4. Diagrama de Clases del Modelo Lógico

### Presentación del Diagrama de Clases
El diagrama de clases del modelo lógico formaliza la estructura orientada a objetos de la solución, definiendo las responsabilidades, atributos, métodos y asociaciones entre las entidades del dominio, los servicios de aplicación y los controladores RESTful. Integra los modelos relacionales de SQLAlchemy 2.0 y los esquemas de validación Pydantic v2 en estricta consonancia con las reglas de negocio institucionales (RN-01 al RN-14). A continuación, se presenta el Diagrama General de Clases del Modelo Lógico (Diagrama 6.16), seguido de las 24 vistas lógicas parciales para cada caso de uso canónico.

### Diagrama 6.16: Diagrama de Clases del Modelo Lógico del Sistema Web P2P

```plantuml
@startuml
title Diagrama de Clases del Modelo Lógico General - Sistema Web P2P EPIS UPT
skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

class Usuario {
  -id: UUID
  -codigo_estudiante: String
  -email: String
  -nombres: String
  -apellidos: String
  -activo: Boolean
  +validarEmailUpt(): Boolean
}

class ConsentimientoLegal {
  -id: UUID
  -usuario_id: UUID
  -ip_address: String
  -user_agent: String
  -fecha_aceptacion: DateTime
}

class CursoCritico {
  -id: UUID
  -codigo: String
  -nombre: String
  -ciclo: Integer
  -es_prioritario: Boolean
}

class TemaCurricular {
  -id: UUID
  -curso_id: UUID
  -unidad: Integer
  -titulo: String
}

class OfertaMentoria {
  -id: UUID
  -mentor_id: UUID
  -curso_id: UUID
  -tema_id: UUID
  -modalidad: String
  -aforo_maximo: Integer
  -fecha_inicio: DateTime
  -estado: String
}

class SesionMentoria {
  -id: UUID
  -oferta_id: UUID
  -espacio_id: UUID
  -enlace_virtual: String
  -estado: String
  -quorum_alcanzado: Boolean
}

class ReservaCupo {
  -id: UUID
  -sesion_id: UUID
  -mentoreado_id: UUID
  -estado: String
  -fecha_reserva: DateTime
  +confirmar(): Void
  +cancelar(): Void
}

class AsistenciaSesion {
  -id: UUID
  -sesion_id: UUID
  -estudiante_id: UUID
  -estado: String
  -metodo_checkin: String
  -fecha_checkin: DateTime
}

class BitacoraPedagogica {
  -id: UUID
  -sesion_id: UUID
  -mentor_id: UUID
  -temas_impartidos: Text
  -observaciones: Text
  -hash_sha256: String
  -estado_visado: String
  +calcularHash(): String
}

class CertificadoHoras {
  -id: UUID
  -mentor_id: UUID
  -folio_correlativo: String
  -horas_acreditadas: Float
  -hash_documento: String
  -url_qr: String
  -fecha_emision: DateTime
}

Usuario "1" *-- "0..1" ConsentimientoLegal
CursoCritico "1" *-- "1..*" TemaCurricular
Usuario "1" -- "0..*" OfertaMentoria : publica
OfertaMentoria "1" *-- "1" SesionMentoria
SesionMentoria "1" *-- "0..*" ReservaCupo
SesionMentoria "1" *-- "0..*" AsistenciaSesion
SesionMentoria "1" *-- "0..1" BitacoraPedagogica
Usuario "1" -- "0..*" CertificadoHoras : recibe
@enduml
```

Fuente: Elaboración propia.

---
''')

    # 24 Partial Class Diagrams
    for cid, idx, name, mod_code, mod_name, b_name, c_name, e_name in CUS_METADATA:
        out.append(generate_class_diagram(cid, idx, name, mod_code, mod_name, b_name, c_name, e_name))
        out.append("\n---\n")

    # Section 6.3.5: FSM
    out.append(r'''## 6.3.5. Diagramas de Máquinas de Estados Finitas (FSM)

### Presentación de las Máquinas de Estados Finitas
Para garantizar el determinismo, la integridad referencial y el cumplimiento riguroso de las reglas de negocio institucionales (RN-05, RN-08, RN-09, RN-10, RN-12, RN-14), el ciclo de vida de las entidades neurálgicas del sistema se formaliza mediante Máquinas de Estados Finitas (*Finite State Machines - FSM*). Las transiciones de estado están gobernadas por constraints a nivel de base de datos (`chk_sesion_estado`, `chk_reserva_estado`, `chk_bitacora_visado`) y por verificadores lógicos de precondiciones en los servicios de backend.

### Diagrama 6.17: Máquina de Estados Finitos - Ciclo de Vida de SesionMentoria

```plantuml
@startuml
title Diagrama 6.17: FSM del Ciclo de Vida de SesionMentoria\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam state {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

[*] --> PROGRAMADA : Publicación de Oferta (RN-04: T >= 24h)

state PROGRAMADA {
  PROGRAMADA : Acepta reservas concurrentes
  PROGRAMADA : Ventana de confirmación abierta
}

PROGRAMADA --> CONFIRMADA : Corte T-24h y Quórum >= 50% (RN-09)
PROGRAMADA --> QUORUM_INSUFICIENTE : Corte T-24h y Quórum < 50% (RN-09)
PROGRAMADA --> CANCELADA_MENTOR : Cancelación justificada por el mentor (RN-10)

state QUORUM_INSUFICIENTE {
  QUORUM_INSUFICIENTE : Espera resolución del mentor
}

QUORUM_INSUFICIENTE --> CONFIRMADA : Mentor decide continuar (RN-09)
QUORUM_INSUFICIENTE --> CANCELADA_QUORUM : Mentor cancela por falta de quórum (RN-10)

state CONFIRMADA {
  CONFIRMADA : Espacio asegurado (Aula/Virtual)
  CONFIRMADA : Notificación enviada a participantes
}

CONFIRMADA --> EN_CURSO : Hora de inicio de la sesión
CONFIRMADA --> CANCELADA_MENTOR : Imprevisto de fuerza mayor justificado

state EN_CURSO {
  EN_CURSO : Marcación QR TOTP activa
  EN_CURSO : Desarrollo de contenidos
}

EN_CURSO --> FINALIZADA : Cierre de sesión y registro de bitácora en 48h (RN-12)

state FINALIZADA {
  FINALIZADA : Bitácora firmada con SHA-256
  FINALIZADA : Encuesta habilitada por 24h (RN-13)
  FINALIZADA : Horas acumuladas para auditoría
}

CANCELADA_QUORUM --> [*] : Recursos liberados
CANCELADA_MENTOR --> [*] : Recursos liberados
FINALIZADA --> [*]
@enduml
```

Fuente: Elaboración propia a partir de los constraints de PostgreSQL (`chk_sesion_estado`).

---

### Diagrama 6.18: Máquina de Estados Finitos - Ciclo de Vida de ReservaCupo

```plantuml
@startuml
title Diagrama 6.18: FSM del Ciclo de Vida de ReservaCupo\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam state {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

[*] --> PENDIENTE_CONFIRMACION : Reserva de cupo con cerrojo pesimista FOR UPDATE (RN-05)

state PENDIENTE_CONFIRMACION {
  PENDIENTE_CONFIRMACION : Cupo bloqueado temporalmente
  PENDIENTE_CONFIRMACION : Ventana abierta hasta T-24h
}

PENDIENTE_CONFIRMACION --> CONFIRMADA : Estudiante ratifica asistencia antes de T-24h (RN-08)
PENDIENTE_CONFIRMACION --> CANCELADA_USUARIO : Estudiante desiste voluntariamente antes de T-24h (RN-10)
PENDIENTE_CONFIRMACION --> NO_CONFIRMADA : Vence plazo T-24h sin ratificación (RN-08)

state CONFIRMADA {
  CONFIRMADA : Computa formalmente para quórum
  CONFIRMADA : Pase QR dinámico habilitado
}

CONFIRMADA --> CANCELADA_USUARIO : Desistimiento extraordinario justificado
CONFIRMADA --> ASISTIO : Check-in exitoso con pase QR TOTP o lista (RN-12)
CONFIRMADA --> INASISTENCIA : Cierre de bitácora sin registro de check-in (RN-12)

state ASISTIO {
  ASISTIO : Habilitado para responder encuesta (24h)
}

state INASISTENCIA {
  INASISTENCIA : Inhabilitado para evaluar
}

NO_CONFIRMADA --> [*] : Cupo liberado inmediatamente
CANCELADA_USUARIO --> [*] : Cupo liberado inmediatamente
ASISTIO --> [*]
INASISTENCIA --> [*]
@enduml
```

Fuente: Elaboración propia a partir de los constraints de PostgreSQL (`chk_reserva_estado`).

---

### Diagrama 6.19: Máquina de Estados Finitos - Ciclo de Vida de BitacoraPedagogica y CertificadoHoras

```plantuml
@startuml
title Diagrama 6.19: FSM de BitacoraPedagogica y CertificadoHoras\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam state {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

[*] --> PENDIENTE_REGISTRO : Sesión culminada (Ventana perentoria de 48h - RN-12)

state PENDIENTE_REGISTRO {
  PENDIENTE_REGISTRO : Espera reporte temático y asistencia
}

PENDIENTE_REGISTRO --> REGISTRADA : Mentor envía bitácora con hash SHA-256
PENDIENTE_REGISTRO --> VENCIDA_NO_REGISTRADA : Expiran 48h sin registro (horas no computables)

state REGISTRADA {
  REGISTRADA : Sometida a fiscalización administrativa
}

REGISTRADA --> VISADA_APROBADA : Comisión de Tutoría aprueba contenidos (RN-14)
REGISTRADA --> OBSERVADA : Discrepancia temática o documental

state OBSERVADA {
  OBSERVADA : Requiere subsanación por el mentor
}

OBSERVADA --> REGISTRADA : Mentor subsana observaciones

state VISADA_APROBADA {
  VISADA_APROBADA : Horas computables formalmente
}

VISADA_APROBADA --> CERTIFICADO_EMITIDO : Suma >= 20 horas semestrales auditadas (RN-14)

state CERTIFICADO_EMITIDO {
  CERTIFICADO_EMITIDO : Folio correlativo institucional asignado
  CERTIFICADO_EMITIDO : Documento PDF/A compilado con ReportLab
  CERTIFICADO_EMITIDO : Código QR institucional de validación en línea
}

CERTIFICADO_EMITIDO --> [*]
VENCIDA_NO_REGISTRADA --> [*]
@enduml
```

Fuente: Elaboración propia.

---

## 6.3.6. Modelo Físico de Base de Datos Relacional y Diccionario DDL

### Presentación del Modelo Físico
El modelo físico de base de datos materializa la arquitectura de persistencia sobre el motor relacional **PostgreSQL v15+ (Supabase)**. Está compuesto por **15 tablas físicas relacionales**, estructuradas bajo la Tercera Forma Normal (3FN), con tipos de datos nativos fuertemente tipados, claves primarias basadas en UUID v4 para prevenir la enumeración de recursos, restricciones de integridad referencial con cascadas controladas (`ON DELETE CASCADE` / `ON DELETE RESTRICT`), índices de cobertura para optimización de consultas concurrentes y políticas de seguridad a nivel de fila (**Row Level Security - RLS**) en cumplimiento vinculante de la Ley N° 29733 de Protección de Datos Personales del Perú.

### Diagrama 6.20: Diagrama Entidad-Relación Físico (15 Tablas Relacionales) - PostgreSQL

```plantuml
@startuml
title Diagrama 6.20: Diagrama Entidad-Relación Físico (15 Tablas Relacionales)\nSistema Web P2P - PostgreSQL / Supabase
hide circle
skinparam linetype ortho
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam entity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

entity "usuarios" as tbl_usuarios {
  *id : uuid <<PK>>
  --
  *codigo_estudiante : varchar(20) <<UQ>>
  *email : varchar(100) <<UQ>>
  *nombres : varchar(100)
  *apellidos : varchar(100)
  *activo : boolean
  *created_at : timestamptz
}

entity "roles" as tbl_roles {
  *id : integer <<PK>>
  --
  *codigo : varchar(30) <<UQ>>
  *nombre : varchar(50)
}

entity "usuario_roles" as tbl_usuario_roles {
  *usuario_id : uuid <<PK, FK>>
  *rol_id : integer <<PK, FK>>
  --
  *asignado_en : timestamptz
}

entity "consentimientos_legales" as tbl_consentimientos {
  *id : uuid <<PK>>
  --
  *usuario_id : uuid <<FK, UQ>>
  *ip_address : varchar(45)
  *user_agent : text
  *version_politica : varchar(20)
  *aceptado_en : timestamptz
}

entity "codigos_otp" as tbl_otp {
  *id : uuid <<PK>>
  --
  *email : varchar(100)
  *codigo_hash : varchar(64)
  *intentos : integer
  *expira_en : timestamptz
  *consumido : boolean
}

entity "perfiles_formativos" as tbl_perfiles {
  *id : uuid <<PK>>
  --
  *usuario_id : uuid <<FK, UQ>>
  *biografia : text
  *ciclo_actual : integer
  *reputacion : numeric(3,2)
  *horas_acumuladas : numeric(5,2)
}

entity "disponibilidades_horarias" as tbl_disponibilidad {
  *id : uuid <<PK>>
  --
  *usuario_id : uuid <<FK>>
  *dia_semana : integer <<CHECK 1-6>>
  *hora_inicio : time
  *hora_fin : time
}

entity "cursos_criticos" as tbl_cursos {
  *id : uuid <<PK>>
  --
  *codigo : varchar(20) <<UQ>>
  *nombre : varchar(120)
  *ciclo : integer
  *es_prioritario : boolean
}

entity "temas_curriculares" as tbl_temas {
  *id : uuid <<PK>>
  --
  *curso_id : uuid <<FK>>
  *unidad : integer
  *titulo : varchar(150)
  *descripcion : text
}

entity "espacios_fisicos" as tbl_espacios {
  *id : uuid <<PK>>
  --
  *codigo_ambiente : varchar(30) <<UQ>>
  *pabellon : varchar(50)
  *capacidad : integer
  *activo : boolean
}

entity "ofertas_mentoria" as tbl_ofertas {
  *id : uuid <<PK>>
  --
  *mentor_id : uuid <<FK>>
  *curso_id : uuid <<FK>>
  *tema_id : uuid <<FK>>
  *modalidad : varchar(20) <<CHECK>>
  *aforo_maximo : integer
  *fecha_inicio : timestamptz
  *fecha_fin : timestamptz
  *estado : varchar(30) <<CHECK>>
}

entity "sesiones_mentoria" as tbl_sesiones {
  *id : uuid <<PK>>
  --
  *oferta_id : uuid <<FK, UQ>>
  *espacio_id : uuid <<FK>>
  *enlace_virtual : varchar(255)
  *estado : varchar(30) <<CHECK>>
  *quorum_alcanzado : boolean
}

entity "reservas_cupos" as tbl_reservas {
  *id : uuid <<PK>>
  --
  *sesion_id : uuid <<FK>>
  *mentoreado_id : uuid <<FK>>
  *estado : varchar(30) <<CHECK>>
  *fecha_reserva : timestamptz
  *fecha_ratificacion : timestamptz
}

entity "asistencias_sesiones" as tbl_asistencias {
  *id : uuid <<PK>>
  --
  *sesion_id : uuid <<FK>>
  *estudiante_id : uuid <<FK>>
  *estado : varchar(20) <<CHECK>>
  *metodo_checkin : varchar(30)
  *fecha_checkin : timestamptz
}

entity "bitacoras_pedagogicas" as tbl_bitacoras {
  *id : uuid <<PK>>
  --
  *sesion_id : uuid <<FK, UQ>>
  *mentor_id : uuid <<FK>>
  *temas_impartidos : text
  *observaciones : text
  *hash_sha256 : varchar(64)
  *estado_visado : varchar(20) <<CHECK>>
  *fecha_registro : timestamptz
}

tbl_usuarios ||--o| tbl_consentimientos
tbl_usuarios ||--o{ tbl_usuario_roles
tbl_roles ||--o{ tbl_usuario_roles
tbl_usuarios ||--o| tbl_perfiles
tbl_usuarios ||--o{ tbl_disponibilidad

tbl_cursos ||--o{ tbl_temas
tbl_usuarios ||--o{ tbl_ofertas
tbl_cursos ||--o{ tbl_ofertas
tbl_temas ||--o{ tbl_ofertas

tbl_ofertas ||--|| tbl_sesiones
tbl_espacios ||--o{ tbl_sesiones

tbl_sesiones ||--o{ tbl_reservas
tbl_usuarios ||--o{ tbl_reservas

tbl_sesiones ||--o{ tbl_asistencias
tbl_usuarios ||--o{ tbl_asistencias

tbl_sesiones ||--o| tbl_bitacoras
@enduml
```

Fuente: Elaboración propia.

---

### Diccionario de Datos DDL del Sistema Web P2P (15 Tablas Relacionales)

#### 1. Tabla: `usuarios`
Almacena el padrón oficial de cuentas institucionales universitarias autorizadas para operar en la plataforma.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador universal único del usuario (anonimizado). |
| `codigo_estudiante` | `VARCHAR(20)` | `NOT NULL, UNIQUE` | Código institucional de matrícula de la UPT. |
| `email` | `VARCHAR(100)` | `NOT NULL, UNIQUE, CHECK email LIKE '%@upt.pe'` | Dirección electrónica oficial institucional. |
| `nombres` | `VARCHAR(100)` | `NOT NULL` | Nombres del estudiante según registro académico. |
| `apellidos` | `VARCHAR(100)` | `NOT NULL` | Apellidos paterno y materno del estudiante. |
| `activo` | `BOOLEAN` | `NOT NULL, DEFAULT TRUE` | Bandera de habilitación o suspensión administrativa. |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT NOW()` | Marca de tiempo UTC de registro de la cuenta. |

#### 2. Tabla: `roles`
Catálogo de roles institucionales canónicos del sistema de control de acceso RBAC.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY, GENERATED ALWAYS AS IDENTITY` | Identificador unívoco del rol. |
| `codigo` | `VARCHAR(30)` | `NOT NULL, UNIQUE` | Código programático (`mentoreado`, `mentor`, `administrador`). |
| `nombre` | `VARCHAR(50)` | `NOT NULL` | Nombre descriptivo legible del rol institucional. |

#### 3. Tabla: `usuario_roles`
Tabla intermedia asociativa de asignación jerárquica de roles por usuario (M:N).
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `usuario_id` | `UUID` | `NOT NULL, REFERENCES usuarios(id) ON DELETE CASCADE` | Llave foránea hacia el usuario asignado. |
| `rol_id` | `INTEGER` | `NOT NULL, REFERENCES roles(id) ON DELETE CASCADE` | Llave foránea hacia el rol institucional otorgado. |
| `asignado_en` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT NOW()` | Fecha y hora UTC en que se formalizó la asignación. |

#### 4. Tabla: `consentimientos_legales`
Registro inmutable de formalización de consentimiento informado digital bajo la Ley N° 29733.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco del registro de consentimiento. |
| `usuario_id` | `UUID` | `NOT NULL, UNIQUE, REFERENCES usuarios(id) ON DELETE CASCADE` | Llave foránea hacia el titular del consentimiento. |
| `ip_address` | `VARCHAR(45)` | `NOT NULL` | Dirección IP v4/v6 desde la que se formalizó el consentimiento. |
| `user_agent` | `TEXT` | `NOT NULL` | Cabecera User-Agent del navegador web del usuario. |
| `version_politica`| `VARCHAR(20)` | `NOT NULL, DEFAULT 'v1.0'` | Versión normativa de la política institucional aceptada. |
| `aceptado_en` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT NOW()` | Marca de tiempo UTC inmutable de aceptación expresa. |

#### 5. Tabla: `codigos_otp`
Almacén transaccional efímero de códigos de un solo uso (OTP) para autenticación multifactor 2FA.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco de la solicitud OTP. |
| `email` | `VARCHAR(100)` | `NOT NULL` | Dirección de correo institucional destino. |
| `codigo_hash` | `VARCHAR(64)` | `NOT NULL` | Hash criptográfico SHA-256 del código numérico de 6 dígitos. |
| `intentos` | `INTEGER` | `NOT NULL, DEFAULT 0, CHECK intentos <= 3` | Contador de reintentos fallidos de validación. |
| `expira_en` | `TIMESTAMPTZ` | `NOT NULL` | Marca temporal límite de expiración (5 minutos / 300 s). |
| `consumido` | `BOOLEAN` | `NOT NULL, DEFAULT FALSE` | Bandera de consumo atómico para prevenir reutilización. |

#### 6. Tabla: `perfiles_formativos`
Expediente pedagógico y métricas de reputación del estudiante o mentor.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador del perfil formativo. |
| `usuario_id` | `UUID` | `NOT NULL, UNIQUE, REFERENCES usuarios(id) ON DELETE CASCADE` | Llave foránea al usuario titular. |
| `biografia` | `TEXT` | `NULL` | Breve reseña de competencias y áreas de interés. |
| `ciclo_actual` | `INTEGER` | `NOT NULL, CHECK ciclo_actual BETWEEN 1 AND 10` | Ciclo lectivo cursado en el semestre activo. |
| `reputacion` | `NUMERIC(3,2)`| `NOT NULL, DEFAULT 5.00, CHECK reputacion BETWEEN 1 AND 5` | Promedio ponderado de calificaciones post-sesión. |
| `horas_acumuladas`| `NUMERIC(5,2)`| `NOT NULL, DEFAULT 0.00` | Total de horas de mentoría efectivamente dictadas y auditadas. |

#### 7. Tabla: `disponibilidades_horarias`
Franjas horarias semanales declaradas por mentores y mentoreados (Matriz 6×11).
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador de la franja horaria. |
| `usuario_id` | `UUID` | `NOT NULL, REFERENCES usuarios(id) ON DELETE CASCADE` | Llave foránea hacia el usuario. |
| `dia_semana` | `INTEGER` | `NOT NULL, CHECK dia_semana BETWEEN 1 AND 6` | Día de la semana (1=Lunes, 2=Martes, ..., 6=Sábado). |
| `hora_inicio` | `TIME` | `NOT NULL` | Hora de inicio del bloque de disponibilidad. |
| `hora_fin` | `TIME` | `NOT NULL, CHECK hora_fin > hora_inicio` | Hora de culminación del bloque horario. |

#### 8. Tabla: `cursos_criticos`
Catálogo oficial de asignaturas formativas críticas de I a IV ciclo de la EPIS-UPT.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco del curso crítico. |
| `codigo` | `VARCHAR(20)` | `NOT NULL, UNIQUE` | Código curricular oficial en el plan de estudios. |
| `nombre` | `VARCHAR(120)` | `NOT NULL` | Denominación formal de la asignatura formativa. |
| `ciclo` | `INTEGER` | `NOT NULL, CHECK ciclo BETWEEN 1 AND 10` | Ciclo sugerido en la malla curricular. |
| `es_prioritario` | `BOOLEAN` | `NOT NULL, DEFAULT FALSE` | Bandera de priorización académica fijada por tutoría. |

#### 9. Tabla: `temas_curriculares`
Taxonomía jerárquica de unidades y contenidos silábicos oficiales de los cursos filtro.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco del tema curricular. |
| `curso_id` | `UUID` | `NOT NULL, REFERENCES cursos_criticos(id) ON DELETE CASCADE` | Llave foránea hacia la asignatura de pertenencia. |
| `unidad` | `INTEGER` | `NOT NULL, CHECK unidad BETWEEN 1 AND 4` | Número de unidad didáctica del sílabo. |
| `titulo` | `VARCHAR(150)` | `NOT NULL` | Título del contenido temático silábico. |
| `descripcion` | `TEXT` | `NULL` | Desglose conceptual de competencias y ejercicios. |

#### 10. Tabla: `espacios_fisicos`
Registro de infraestructura de aulas y laboratorios de cómputo de la EPIS-UPT.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco del espacio físico. |
| `codigo_ambiente` | `VARCHAR(30)` | `NOT NULL, UNIQUE` | Código institucional de aula o laboratorio (ej. `LAB-SIS-01`). |
| `pabellon` | `VARCHAR(50)` | `NOT NULL` | Pabellón o edificio dentro del campus universitario. |
| `capacidad` | `INTEGER` | `NOT NULL, DEFAULT 10, CHECK capacidad > 0` | Aforo máximo reglamentario para mentorías. |
| `activo` | `BOOLEAN` | `NOT NULL, DEFAULT TRUE` | Estado operativo del ambiente físico. |

#### 11. Tabla: `ofertas_mentoria`
Ofertas formativas programadas y publicadas por mentores acreditados.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco de la oferta de mentoría. |
| `mentor_id` | `UUID` | `NOT NULL, REFERENCES usuarios(id) ON DELETE RESTRICT` | Llave foránea al mentor que imparte la clase. |
| `curso_id` | `UUID` | `NOT NULL, REFERENCES cursos_criticos(id) ON DELETE RESTRICT` | Asignatura curricular asociada. |
| `tema_id` | `UUID` | `NOT NULL, REFERENCES temas_curriculares(id) ON DELETE RESTRICT` | Tema silábico específico a desarrollar. |
| `modalidad` | `VARCHAR(20)` | `NOT NULL, CHECK modalidad IN ('PRESENCIAL', 'VIRTUAL')` | Modalidad pedagógica de la sesión. |
| `aforo_maximo` | `INTEGER` | `NOT NULL, CHECK aforo_maximo <= 20` | Límite estricto de asistentes (10 presencial, 20 virtual). |
| `fecha_inicio` | `TIMESTAMPTZ` | `NOT NULL` | Fecha y hora de inicio de la mentoría. |
| `fecha_fin` | `TIMESTAMPTZ` | `NOT NULL, CHECK fecha_fin > fecha_inicio` | Fecha y hora de finalización prevista. |
| `estado` | `VARCHAR(30)` | `NOT NULL, DEFAULT 'PUBLICADA'` | Estado operativo (`PUBLICADA`, `CERRADA`, `CANCELADA`). |

#### 12. Tabla: `sesiones_mentoria`
Instancia operativa transaccional vinculada al ciclo de reservas, quórum y ejecución.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco de la sesión de mentoría. |
| `oferta_id` | `UUID` | `NOT NULL, UNIQUE, REFERENCES ofertas_mentoria(id) ON DELETE CASCADE` | Llave foránea 1:1 hacia la oferta correspondiente. |
| `espacio_id` | `UUID` | `NULL, REFERENCES espacios_fisicos(id) ON DELETE SET NULL` | Llave foránea al aula física asignada (si aplica). |
| `enlace_virtual` | `VARCHAR(255)` | `NULL` | URL validada de la sala virtual de videoconferencia. |
| `estado` | `VARCHAR(30)` | `NOT NULL, DEFAULT 'PROGRAMADA'` | Estado gobernado por constraint `chk_sesion_estado`. |
| `quorum_alcanzado`| `BOOLEAN` | `NOT NULL, DEFAULT FALSE` | Bandera booleana evaluada al corte de $T-24\text{ h}$. |

#### 13. Tabla: `reservas_cupos`
Inscripciones y reservas individuales de plazas efectuadas por mentoreados.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco de la reserva de cupo. |
| `sesion_id` | `UUID` | `NOT NULL, REFERENCES sesiones_mentoria(id) ON DELETE CASCADE` | Llave foránea a la sesión reservada. |
| `mentoreado_id` | `UUID` | `NOT NULL, REFERENCES usuarios(id) ON DELETE RESTRICT` | Llave foránea al estudiante inscrito. |
| `estado` | `VARCHAR(30)` | `NOT NULL, DEFAULT 'PENDIENTE_CONFIRMACION'` | Estado gobernado por constraint `chk_reserva_estado`. |
| `fecha_reserva` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT NOW()` | Marca temporal UTC en que se reservó el cupo. |
| `fecha_ratificacion`| `TIMESTAMPTZ`| `NULL` | Marca temporal UTC en que se ratificó la asistencia. |

#### 14. Tabla: `asistencias_sesiones`
Registro de presencia efectiva y check-in verificado mediante código QR TOTP.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco del registro de asistencia. |
| `sesion_id` | `UUID` | `NOT NULL, REFERENCES sesiones_mentoria(id) ON DELETE CASCADE` | Llave foránea a la sesión dictada. |
| `estudiante_id` | `UUID` | `NOT NULL, REFERENCES usuarios(id) ON DELETE RESTRICT` | Llave foránea al estudiante participante. |
| `estado` | `VARCHAR(20)` | `NOT NULL, CHECK estado IN ('ASISTIO', 'FALTO')` | Condición final de asistencia presencial/virtual. |
| `metodo_checkin`| `VARCHAR(30)` | `NOT NULL, DEFAULT 'QR_TOTP'` | Medio de verificación (`QR_TOTP`, `MANUAL_MENTOR`). |
| `fecha_checkin` | `TIMESTAMPTZ` | `NOT NULL, DEFAULT NOW()` | Marca temporal UTC exacta de marcación de asistencia. |

#### 15. Tabla: `bitacoras_pedagogicas`
Acta pedagógica formal de contenidos impartidos, firmada criptográficamente con SHA-256.
| Columna | Tipo de Dato | Modificadores | Descripción Técnica |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Identificador unívoco de la bitácora pedagógica. |
| `sesion_id` | `UUID` | `NOT NULL, UNIQUE, REFERENCES sesiones_mentoria(id) ON DELETE RESTRICT` | Llave foránea a la sesión culminada. |
| `mentor_id` | `UUID` | `NOT NULL, REFERENCES usuarios(id) ON DELETE RESTRICT` | Llave foránea al mentor que dictó la sesión. |
| `temas_impartidos`| `TEXT` | `NOT NULL` | Desglose detallado de los contenidos desarrollados. |
| `observaciones` | `TEXT` | `NULL` | Anotaciones metodológicas sobre el desempeño estudiantil. |
| `hash_sha256` | `VARCHAR(64)` | `NOT NULL` | Hash criptográfico inmutable de verificación de integridad. |
| `estado_visado` | `VARCHAR(20)` | `NOT NULL, DEFAULT 'PENDIENTE', CHECK estado_visado IN ('PENDIENTE', 'APROBADO', 'OBSERVADO')` | Estado de fiscalización por tutoría universitaria. |
| `fecha_registro`| `TIMESTAMPTZ` | `NOT NULL, DEFAULT NOW()` | Marca temporal de cierre formal de la bitácora. |

---

### Políticas de Seguridad a Nivel de Fila (Row Level Security - RLS)

En cumplimiento de la Ley N° 29733 de Protección de Datos Personales, todas las consultas y mutaciones sobre datos académicos están protegidas en PostgreSQL mediante políticas RLS nativas:

```sql
-- Habilitación general de Row Level Security
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE consentimientos_legales ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_formativos ENABLE ROW LEVEL SECURITY;
ALTER TABLE disponibilidades_horarias ENABLE ROW LEVEL SECURITY;
ALTER TABLE reservas_cupos ENABLE ROW LEVEL SECURITY;
ALTER TABLE asistencias_sesiones ENABLE ROW LEVEL SECURITY;
ALTER TABLE bitacoras_pedagogicas ENABLE ROW LEVEL SECURITY;

-- Política 1: Aislamiento de expediente de usuario (Solo propietario o Administrador)
CREATE POLICY rls_usuario_propio ON usuarios
  FOR ALL
  USING (id = auth.uid() OR EXISTS (
    SELECT 1 FROM usuario_roles ur JOIN roles r ON ur.rol_id = r.id
    WHERE ur.usuario_id = auth.uid() AND r.codigo = 'administrador'
  ));

-- Política 2: Consulta y mutación de reservas propias
CREATE POLICY rls_reservas_propias ON reservas_cupos
  FOR ALL
  USING (mentoreado_id = auth.uid() OR EXISTS (
    SELECT 1 FROM sesiones_mentoria sm JOIN ofertas_mentoria om ON sm.oferta_id = om.id
    WHERE sm.id = reservas_cupos.sesion_id AND om.mentor_id = auth.uid()
  ));

-- Política 3: Inmutabilidad de consentimientos legales registrados
CREATE POLICY rls_consentimiento_insert ON consentimientos_legales
  FOR INSERT WITH CHECK (usuario_id = auth.uid());

CREATE POLICY rls_consentimiento_select ON consentimientos_legales
  FOR SELECT USING (usuario_id = auth.uid() OR EXISTS (
    SELECT 1 FROM usuario_roles ur JOIN roles r ON ur.rol_id = r.id
    WHERE ur.usuario_id = auth.uid() AND r.codigo = 'administrador'
  ));
```

---
''')

    return "\n".join(out)
