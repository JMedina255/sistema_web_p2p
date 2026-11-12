# -*- coding: utf-8 -*-
"""
Generator for Part C of docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
Covers:
- Sección 6.3: Introducción al Modelo Lógico
- Sección 6.3.1: Análisis de Objetos (Modelo ECB) - Diagrama 6.13 y CUS-001 al CUS-024 (Diagramas 6.13.1 al 6.13.24)
- Sección 6.3.2: Diagramas de Actividades con Flujo de Objetos - Diagrama 6.14 y CUS-001 al CUS-024 (Diagramas 6.14.1 al 6.14.24)
"""

CUS_METADATA = [
    # (cid, num, name, mod_code, mod_name, boundary, control, entity)
    ("CUS-001", 1, "Iniciar sesión institucional con 2FA", "MOD-01", "Seguridad, Autenticación y Gobernanza",
     "UI_LoginOtpView / UI_ConsentModal", "AuthService / ConsentService / JWTGenerator", "Usuario, CodigoOTP, ConsentimientoLegal"),
    ("CUS-010", 2, "Gestionar asignación de roles de usuario", "MOD-01", "Seguridad, Autenticación y Gobernanza",
     "UI_AdminRolesView / UI_PromoteModal", "RoleService / MeritValidator", "Usuario, Rol, UsuarioRol"),
    ("CUS-006", 3, "Publicar oferta de mentoría académica", "MOD-02", "Ofertas de Mentoría y Gestión de Recursos",
     "UI_PublishMentorshipView / UI_MentorOffers", "MentorshipService / SpaceValidationService", "OfertaMentoria, SesionMentoria, EspacioFisico"),
    ("CUS-008", 4, "Consultar disponibilidad de espacios y recursos", "MOD-02", "Ofertas de Mentoría y Gestión de Recursos",
     "UI_SpaceSelectorView / UI_ScheduleImport", "SpaceService / ScheduleParserService", "EspacioFisico, HorarioOcupacion"),
    ("CUS-005", 5, "Gestionar perfil formativo y disponibilidad horaria", "MOD-03", "Perfil del Mentor y Plan de Aprendizaje",
     "UI_ProfileAvailabilityView / UI_Grid6x11", "ProfileService / AvailabilityManager", "PerfilFormativo, DisponibilidadHoraria"),
    ("CUS-021", 6, "Explorar catálogo curricular de asignaturas filtro", "MOD-03", "Perfil del Mentor y Plan de Aprendizaje",
     "UI_CurriculumCatalogView / UI_CourseTree", "CurriculumService / TopicSearchEngine", "CursoCritico, TemaCurricular"),
    ("CUS-002", 7, "Explorar recomendaciones personalizadas Top-k", "MOD-04", "Demanda y Recomendaciones Personalizadas",
     "UI_RecommendationsView / UI_RecommendationCard", "RecommendationService / EdRecSysEngine", "PerfilFormativo, TemaCurricular, OfertaMentoria"),
    ("CUS-003", 8, "Registrar solicitud de demanda académica", "MOD-04", "Demanda y Recomendaciones Personalizadas",
     "UI_DemandsBankView / UI_DemandCreateModal", "DemandService / NotificationDispatcher", "SolicitudDemanda, CursoCritico, TemaCurricular"),
    ("CUS-004", 9, "Reservar cupo de mentoría académica", "MOD-05", "Quórum, Confirmación y Cancelaciones",
     "UI_BookingModalView / UI_StudentBookings", "BookingService (SELECT FOR UPDATE) / CapacityManager", "SesionMentoria, ReservaCupo"),
    ("CUS-024", 10, "Ratificar asistencia a sesión de mentoría", "MOD-05", "Quórum, Confirmación y Cancelaciones",
     "UI_StudentBookingsView / UI_ConfirmButton", "BookingService / DeadlineValidator", "ReservaCupo, SesionMentoria"),
    ("CUS-017", 11, "Desistir voluntariamente de reserva", "MOD-05", "Quórum, Confirmación y Cancelaciones",
     "UI_StudentBookingsView / UI_CancelDialog", "BookingService / CapacityRestorer", "ReservaCupo, SesionMentoria"),
    ("CUS-023", 12, "Evaluar quórum automático a T-24h", "MOD-05", "Quórum, Confirmación y Cancelaciones",
     "UI_NotificationCenterView / DaemonRunner", "QuorumCronService / QuorumEvaluator", "SesionMentoria, ReservaCupo, Notificacion"),
    ("CUS-007", 13, "Decisión del mentor ante quórum insuficiente", "MOD-05", "Quórum, Confirmación y Cancelaciones",
     "UI_MentorSessionActionView / UI_DecisionModal", "MentorshipService / ResolutionHandler", "SesionMentoria, ReservaCupo, EspacioFisico"),
    ("CUS-012", 14, "Registrar asistencia a sesión de mentoría", "MOD-06", "Asistencia, Bitácoras y Feedback",
     "UI_QrScannerView / UI_QrPassView", "AttendanceService / TotpQrValidator", "AsistenciaSesion, SesionMentoria, ReservaCupo"),
    ("CUS-013", 15, "Registrar bitácora académica de sesión", "MOD-06", "Asistencia, Bitácoras y Feedback",
     "UI_BitacoraRegisterView / UI_AttendanceCheck", "BitacoraService / Sha256Signer", "BitacoraPedagogica, SesionMentoria, AsistenciaSesion"),
    ("CUS-014", 16, "Visualizar historial y bitácoras académicas", "MOD-06", "Asistencia, Bitácoras y Feedback",
     "UI_BitacoraHistoryView / UI_DetailModal", "BitacoraService / ResourceService", "BitacoraPedagogica, SesionMentoria, RecursoAcademico"),
    ("CUS-018", 17, "Emitir constancia institucional de horas de mentoría", "MOD-07", "Gamificación e Incentivos",
     "UI_AdminCertificatesView / UI_DownloadView", "CertificateService / ReportLabPdfEngine", "CertificadoHoras, BitacoraPedagogica"),
    ("CUS-019", 18, "Gestionar insignias y reputación gamificada", "MOD-07", "Gamificación e Incentivos",
     "UI_MentorBadgesView / UI_ReputationCard", "GamificationService / BadgeEvaluator", "Insignia, MentorInsignia, ReputacionMentor"),
    ("CUS-009", 19, "Notificar eventos críticos y alertas temporales", "MOD-08", "Analítica, Notificaciones y Configuración",
     "UI_NotificationCenterView / SmtpClientAdapter", "NotificationService / AlertDispatcher", "Notificacion, SesionMentoria, Usuario"),
    ("CUS-011", 20, "Generar reportes e indicadores de analítica académica", "MOD-08", "Analítica, Notificaciones y Configuración",
     "UI_AdminAnalyticsView / UI_ExportModal", "AnalyticsService / ReportExporter", "KpiAcademico, SesionMentoria, AsistenciaSesion"),
    ("CUS-015", 21, "Consultar métricas de retención y desempeño", "MOD-08", "Analítica, Notificaciones y Configuración",
     "UI_AdminAnalyticsView / UI_RetentionCard", "AnalyticsService / RetentionKpiEngine", "KpiAcademico, CursoCritico, SesionMentoria"),
    ("CUS-016", 22, "Auditar trazas de seguridad y consentimiento Ley 29733", "MOD-08", "Analítica, Notificaciones y Configuración",
     "UI_AdminAuditView / UI_ConsentTable", "AuditService / PrivacyInspector", "ConsentimientoLegal, TrazaAuditoria"),
    ("CUS-020", 23, "Configurar parámetros institucionales y umbrales", "MOD-08", "Analítica, Notificaciones y Configuración",
     "UI_AdminSettingsView / UI_ConfigForm", "AdminService / SettingsManager", "ParametroInstitucional"),
    ("CUS-022", 24, "Gestionar catálogo de temas y materias críticas", "MOD-08", "Analítica, Notificaciones y Configuración",
     "UI_AdminCurriculumView / UI_TopicModal", "CurriculumService / CourseCatalogManager", "CursoCritico, TemaCurricular")
]

def generate_ecb_diagram(cid, idx, name, mod_code, mod_name, b_name, c_name, e_name):
    clean_b = b_name.replace(" / ", "_").replace(" ", "_")
    clean_c = c_name.replace(" / ", "_").replace(" ", "_").replace("(", "").replace(")", "")
    
    b_first = b_name.split(" / ")[0].strip()
    c_first = c_name.split(" / ")[0].strip().split()[0]
    e_first = e_name.split(",")[0].strip()
    
    return f"""### 6.3.1.{idx}. {cid} – Análisis de Objetos: {name}

El análisis de objetos para `{cid}` descompone las responsabilidades arquitectónicas conforme al patrón Entidad-Control-Frontera (ECB) en el módulo `{mod_code}: {mod_name}`. Los objetos de frontera canalizan la interacción entre los actores institucionales y el software; los objetos de control orquestan la lógica de negocio, validaciones y reglas institucionales; y los objetos de entidad mantienen la persistencia relacional en PostgreSQL.

#### Diagrama 6.13.{idx}: Análisis de Objetos (Modelo ECB) - {cid}: {name}

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - {cid}: {name}\\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {{
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}}
skinparam boundary {{
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}}
skinparam control {{
    BackgroundColor #FFF2DF
    BorderColor #D97706
}}
skinparam entity {{
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}}

actor "Actor Institucional" as ActUser
boundary "{b_first}" as B_Main
control "{c_first}" as C_Main
entity "{e_first}" as E_Main

ActUser --> B_Main : 1. Solicita operacion ({name})
B_Main --> C_Main : 1.1. ejecutarAccion(payload)
C_Main ..> E_Main : 1.2. validarReglasYPersistir()
E_Main --> C_Main : 1.3. estadoActualizado(OK)
C_Main --> B_Main : 1.4. confirmarResultado(DTO)
B_Main --> ActUser : 2. Despliega estado en pantalla
@enduml
```

Fuente: Elaboración propia a partir del diseño de {mod_code}.
"""

def generate_activity_diagram(cid, idx, name, mod_code, mod_name, b_name, c_name, e_name):
    e_first = e_name.split(",")[0].strip()
    return f"""### 6.3.2.{idx}. {cid} – Actividades con Objetos: {name}

El diagrama de actividades con flujo de objetos modela la secuencia lógica, las compuertas de decisión y las transiciones de estado de los artefactos informáticos para `{cid}` en `{mod_code}`. Se organiza en carriles de ejecución (*swimlanes*) que delimitan las acciones del usuario, los controladores de backend y las entidades de datos persistentes.

#### Diagrama 6.14.{idx}: Diagrama de Actividades con Flujo de Objetos - {cid}: {name}

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - {cid}: {name}\\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Actor Institucional|
|#E8F8F5|Sistema Web P2P (Backend)|
|#FFF2DF|Persistencia (PostgreSQL)|

|Actor Institucional|
start
:Inicia accion para {name};
:Envía formulario / petición técnica;

|Sistema Web P2P (Backend)|
:Valida esquema Pydantic y reglas de negocio;
if (¿Datos válidos y reglas conformes?) then (Sí)
  :Inicia transacción ACID;
  |Persistencia (PostgreSQL)|
  :Ejecuta operaciones SQL sobre {e_first};
  :Transiciona estado de la entidad;
  |Sistema Web P2P (Backend)|
  :Confirma transacción (commit);
  :Genera Response DTO;
  |Actor Institucional|
  :Visualiza confirmación exitosa en Vista React;
  stop
else (No)
  |Sistema Web P2P (Backend)|
  :Genera error controlado (HTTP 4xx);
  |Actor Institucional|
  :Visualiza mensaje de alerta descriptivo;
  stop
endif
@enduml
```

Fuente: Elaboración propia a partir del diseño de {mod_code}.
"""

def get_part_c():
    out = []
    
    # Header 6.3
    out.append(r'''# 6.3. Modelo Lógico

El modelo lógico traduce los requerimientos funcionales y las especificaciones narrativas de los casos de uso en una representación analítica abstracta, orientada a objetos e independiente de la plataforma tecnológica final. Mediante esta modelación, el equipo de ingeniería formaliza las colaboraciones internas, los flujos dinámicos de datos y las responsabilidades operacionales de las entidades del dominio de la EPIS-UPT, asegurando una transición fluida hacia el diseño de software detallado y la implementación bajo el marco metodológico UWE.

---

## 6.3.1. Análisis de Objetos (Modelo ECB)

### Presentación del Análisis de Objetos
Para descomponer las responsabilidades funcionales y aislar la lógica de presentación, de control y de persistencia, se emplea el patrón analítico **Entidad-Control-Frontera (ECB - Entity-Control-Boundary)** propuesto por Ivar Jacobson y adoptado en UWE. El análisis abarca la totalidad de los **24 casos de uso canónicos (CUS-001 al CUS-024)** organizados en los ocho módulos del sistema. A través de este modelo, se explicita cómo las interfaces de usuario (Boundary) canalizan las peticiones de los actores hacia controladores especializados (Control), los cuales hacen cumplir las reglas de negocio (RN-01 a RN-14) interactuando con las entidades de dominio persistentes (Entity) y los servicios de infraestructura externa.

A continuación, se presenta el diagrama general de análisis de objetos correspondiente al ciclo transaccional principal, seguido de los 24 diagramas de análisis de objetos por caso de uso.

### Diagrama 6.13: Diagrama de Análisis de Objetos (Modelo ECB) - Flujo General de Mentorías P2P

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - Flujo General de Mentorías P2P\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante Mentoreado" as ActEst
actor "Estudiante Mentor" as ActMen
actor "Administrador EPIS" as ActAdm
actor "Servicio Cron Backend" as ActCron

boundary "UI_CatalogoYRecomendaciones" as B_Rec
boundary "UI_ReservaYConfirmacion" as B_Res
boundary "UI_OfertasYEspacios" as B_Of
boundary "UI_AsistenciaYBitacora" as B_Bit
boundary "UI_CertificadosYAdmin" as B_Adm

control "ControladorRecomendaciones" as C_Rec
control "ControladorReservas" as C_Res
control "ControladorMentorias" as C_Of
control "ControladorBitacoras" as C_Bit
control "ControladorAdmin" as C_Adm
control "ControladorQuorumCron" as C_Cron

entity "Usuario" as E_User
entity "CursoCritico" as E_Cur
entity "OfertaMentoria" as E_Of
entity "SesionMentoria" as E_Ses
entity "ReservaCupo" as E_Res
entity "BitacoraPedagogica" as E_Bit
entity "CertificadoHoras" as E_Cert

ActEst --> B_Rec : 1. Explora recomendaciones Top-k
B_Rec --> C_Rec : 1.1. inferirRecomendaciones()
C_Rec ..> E_Cur : 1.2. similitudCoseno()
C_Rec --> B_Rec : 1.3. retornoTopK()

ActEst --> B_Res : 2. Reserva cupo de sesion
B_Res --> C_Res : 2.1. reservarCupoPesimista(FOR UPDATE)
C_Res --> E_Ses : 2.2. bloquearSesion()
C_Res --> E_Res : 2.3. registrarReserva()

ActCron --> C_Cron : 3. Dispara corte T-24h
C_Cron --> E_Res : 3.1. revocarNoConfirmadas()
C_Cron --> E_Ses : 3.2. evaluarQuorumMinimo()

ActMen --> B_Bit : 4. Cierra sesion y firma bitacora (SHA-256)
B_Bit --> C_Bit : 4.1. registrarBitacora()
C_Bit --> E_Bit : 4.2. persistirBitacoraConHash()

ActAdm --> B_Adm : 5. Visa bitacoras y emite certificado
B_Adm --> C_Adm : 5.1. emitirCertificadoOficial()
C_Adm --> E_Cert : 5.2. compilarPDFConQR()
@enduml
```

Fuente: Elaboración propia.

---
''')
    
    # 24 ECB diagrams
    for cid, idx, name, mod_code, mod_name, b_name, c_name, e_name in CUS_METADATA:
        out.append(generate_ecb_diagram(cid, idx, name, mod_code, mod_name, b_name, c_name, e_name))
        out.append("\n---\n")

    # Header 6.3.2
    out.append(r'''## 6.3.2. Diagrama de Actividades con objetos

### Presentación del Diagrama de Actividades con Objetos
El diagrama de actividades con flujo de objetos modela la dinámica operacional del sistema, explicitando no solo la secuencia temporal de actividades y las decisiones condicionales, sino también el ciclo de vida y los cambios de estado que experimentan los artefactos de datos (objetos de negocio) a medida que transitan por las diferentes etapas del proceso de mentorías. A continuación se presenta el Diagrama General de Actividades del Ciclo de Mentoría (Diagrama 6.14), seguido de los 24 diagramas de actividades detallados para cada caso de uso canónico.

### Diagrama 6.14: Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Estudiante Mentoreado|
|#E8F8F5|Estudiante Mentor|
|#FEF9C3|Sistema Web P2P (Backend)|
|#FFF1F2|Administración (EPIS)|

|Estudiante Mentor|
start
:Publica oferta de mentoría;
|Sistema Web P2P (Backend)|
:Valida disponibilidad de espacio;
:Crea OfertaMentoria [PUBLICADA];
:Crea SesionMentoria [PROGRAMADA];

|Estudiante Mentoreado|
:Explora recomendaciones Top-k;
:Reserva cupo de sesión;
|Sistema Web P2P (Backend)|
:Adquiere cerrojo pesimista FOR UPDATE;
:Crea ReservaCupo [PENDIENTE_CONFIRMACION];

|Estudiante Mentoreado|
:Ratifica asistencia antes de T-24h;
|Sistema Web P2P (Backend)|
:Transiciona ReservaCupo [CONFIRMADA];

|Sistema Web P2P (Backend)|
:Ejecuta corte automatizado a T-24h;
if (¿Quórum >= 50% de aforo?) then (Sí)
  :Transiciona SesionMentoria [CONFIRMADA];
else (No)
  :Transiciona SesionMentoria [QUORUM_INSUFICIENTE];
  |Estudiante Mentor|
  if (¿Mentor decide continuar?) then (Sí)
    :Ratifica sesión extraordinaria;
  else (No)
    :Cancela sesión;
    |Sistema Web P2P (Backend)|
    :SesionMentoria [CANCELADA_QUORUM];
    stop
  endif
endif

|Estudiante Mentor|
:Desarrolla la sesión de mentoría;
:Registra bitácora pedagógica antes de 48h;
|Sistema Web P2P (Backend)|
:Calcula hash SHA-256 inmutable;
:Crea BitacoraPedagogica [REGISTRADA];
:Transiciona SesionMentoria [FINALIZADA];

|Estudiante Mentoreado|
:Completa encuesta de satisfacción (24h);
|Sistema Web P2P (Backend)|
:Actualiza reputación e insignias del mentor;

|Administración (EPIS)|
:Visa bitácoras docentes;
if (¿Horas acumuladas >= 20h?) then (Sí)
  :Emite certificado digital oficial;
  |Sistema Web P2P (Backend)|
  :Genera CertificadoHoras [EMITIDO_VALIDADO];
endif
stop
@enduml
```

Fuente: Elaboración propia.

---
''')

    # 24 Activity diagrams
    for cid, idx, name, mod_code, mod_name, b_name, c_name, e_name in CUS_METADATA:
        out.append(generate_activity_diagram(cid, idx, name, mod_code, mod_name, b_name, c_name, e_name))
        out.append("\n---\n")

    return "\n".join(out)
