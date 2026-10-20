# Diagramas de Secuencia del SAD — Fase de Análisis

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS-UPT.<br>
**Fase:** Análisis — desarrollo del SAD.<br>
**Estado:** Modelos propuestos; pendientes de revisión e implementación.<br>
**Fuente canónica:** SRS FD03 v2.0, secciones 5.1–5.5 y narrativas 6.2.3.

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | RAM / JCM | RAM | RVA | 05/09/2026 | Estructuración inicial y formateo de secuencias preliminares. |
| **2.0** | RAM / JCM | Comité de Calidad EPIS | Dirección de Escuela | 28/09/2026 | Refactorización hacia el estándar SAD de Análisis conceptual (Modelo ECB). |
| **2.1** | RAM / JCM | Comité de Calidad EPIS | Dirección de Escuela | 28/09/2026 | **Incorporación explícita de componentes arquitectónicos del SAD:** Delimitación de subsistemas mediante bloques `box`, especificación de componentes de software (Frontend SPA, Backend Routers/Services, Persistencia Supabase, Caché Redis y Adaptadores Externos), formalización de títulos PlantUML y vinculación con la Vista de Componentes (Diagrama 9.1). |
| **2.2** | Asistencia de Codex a solicitud del equipo | Pendiente | Pendiente | 28/09/2026 | Alineación de CUS/RF/RNF al SRS; corrección de OTP, reserva provisional, quórum y horas sujetas a visado. |

El historial se conserva; esta revisión no supone aprobación institucional. Las secuencias expresan responsabilidades y mensajes conceptuales para el análisis, sin establecer endpoints ni tablas implementados.

## Contenido

1. [Marco y trazabilidad](#1-marco-y-trazabilidad)
2. [Acceso y consentimiento](#2-acceso-y-consentimiento-cus01)
3. [Recomendaciones](#3-recomendaciones-cus02)
4. [Reserva, confirmación y quórum](#4-reserva-confirmación-y-quórum-cus04-cus24-cus23-cus07)
5. [Asistencia, bitácora y visado](#5-asistencia-bitácora-encuesta-y-visado-cus08-cus05-cus22)
6. [Pendientes de diseño](#6-pendientes-de-diseño)

## 1. Marco y trazabilidad

Las fronteras recogen acciones de usuarios, los controles coordinan reglas de negocio y los repositorios representan acceso a entidades del dominio. Los servicios corresponden a las responsabilidades propuestas en las secciones 4, 6 y 9 del SAD. El parser se mantiene interno a MOD-04; el correo, Meet y Discord se tratan como integraciones externas.

La matriz permite localizar los requisitos y las restricciones que justifican cada secuencia. El QR forma parte del flujo alternativo de CUS08; CUS11 mantiene su significado de carga de horarios.

### Cuadro 1.1: Trazabilidad de secuencias al SRS

| Diagrama | CUS | RF | RN / RNF | Componentes propuestos |
| :--- | :--- | :--- | :--- | :--- |
| S-01 | CUS01 | RF01, RF02 | RN-01, RN-02; RNF01, RNF02, RNF10 | AuthenticationService, ConsentService, repositorio y correo institucional. |
| S-02 | CUS02; configuración previa CUS12 | RF06, RF24 | RN-11; RNF03, RNF09 | TopKRecommendationEngine, perfiles/ofertas y caché candidata. |
| S-03 | CUS04, CUS24, CUS23, CUS07 | RF12, RF13, RF15, RF16 | RN-05, RN-08, RN-09, RN-10; RNF07, RNF10 | BookingTransactionCoordinator, QuorumEvaluatorCronService, QuorumResolutionService y notificaciones. |
| S-04 | CUS08, CUS05, CUS22 | RF17, RF18, RF26 | RN-12, RN-13, RN-14; RNF02, RNF09 | BitacoraWorkflowService, QRCodeCryptoValidator, SurveyService y AuditService. |

Fuente: SRS FD03 v2.0 y matriz 4.3 del SAD.

Los cuatro flujos cubren escenarios seleccionados. El alcance completo de los 24 CUS se mantiene en el SRS y en el Cuadro 5.1 del SAD; estas secuencias no lo reducen ni sustituyen sus narrativas.

## 2. Acceso y consentimiento (CUS01)

El usuario solicita acceso institucional. La identidad debe validarse con un OTP enviado al correo UPT, cuya vigencia máxima es de cinco minutos. Una vez validado, se verifica el consentimiento; su rechazo impide habilitar funciones. El token de sesión definitivo respeta RNF01, con HMAC-SHA256 y expiración de ocho horas.

### Diagrama S-01: Acceso institucional y consentimiento

```plantuml
@startuml
title S-01: CUS01 — RF01 / RF02
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
actor "Usuario institucional" as Usuario
boundary "Vista de acceso y consentimiento" as Vista
control "AuthenticationService" as Auth
control "ConsentService" as Consent
entity "Repositorio de usuarios y consentimiento" as Repo
participant "Correo institucional UPT" as Correo
Usuario -> Vista : Solicitar acceso con cuenta institucional
Vista -> Auth : Validar cuenta y solicitar desafío
Auth -> Repo : Verificar cuenta institucional habilitada
alt Cuenta no válida
  Auth --> Vista : Rechazar acceso
else Cuenta válida
  Auth -> Correo : Enviar OTP (vigencia máxima 5 minutos)
  alt Fallo del correo
    Auth --> Vista : Informar indisponibilidad controlada (RNF10)
  else Desafío enviado
    Usuario -> Vista : Introducir OTP recibido
    Vista -> Auth : Verificar OTP
    alt Código inválido, vencido o ya consumido
      Auth --> Vista : Rechazar autenticación
    else Código válido
      Auth -> Auth : Consumir desafío para evitar reutilización
      Auth -> Consent : Consultar consentimiento del titular
      Consent -> Repo : Recuperar constancia vigente
      opt Primer acceso sin consentimiento
        Consent --> Vista : Presentar política y decisión
        Usuario -> Vista : Aceptar o rechazar
        Vista -> Consent : Registrar decisión
        Consent -> Repo : Persistir constancia si acepta
      end
      alt Consentimiento aceptado
        Auth -> Auth : Emitir JWT HMAC-SHA256 (8 horas)
        Auth --> Vista : Habilitar sesión según rol
      else Consentimiento rechazado
        Auth --> Vista : Abortar acceso funcional
      end
    end
  end
end
@enduml
```

Fuente: Elaboración propia a partir de CUS01, RF01–RF02 y RNF01–RNF02.

El flujo incorpora explícitamente el OTP, evitando confundirlo con una contraseña o con TOTP de una aplicación autenticadora. Los permisos de acceso a persistencia y la revocación se precisarán en diseño; la abstracción de repositorio no demuestra por sí misma la aplicación de RLS.

## 3. Recomendaciones (CUS02)

El mentoreado consulta recomendaciones para una necesidad académica. El servicio analiza perfil, disponibilidad, competencias y ofertas elegibles. RN-11 establece similitud temática y desempates; RF24 incorpora la condición de prioridad institucional. La fórmula concreta debe conciliar ambos criterios sin fijar en este documento pesos nuevos.

### Diagrama S-02: Consulta de recomendaciones

```plantuml
@startuml
title S-02: CUS02 — RF06 / RF24
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
actor "Mentoreado" as Alumno
boundary "RecommendationView" as Vista
control "TopKRecommendationEngine" as Motor
entity "Repositorio de perfiles, currículo y ofertas" as Repo
participant "Caché candidata" as Cache
Alumno -> Vista : Consultar mentorías para una necesidad
Vista -> Motor : Solicitar ranking con contexto autorizado
Motor -> Repo : Recuperar perfil, disponibilidad y ofertas elegibles
Repo --> Motor : Candidatos y restricciones
alt Sin candidatos elegibles
  Motor --> Vista : Informar ausencia de coincidencias
  Vista --> Alumno : Ofrecer registro de demanda (CUS03)
else Candidatos disponibles
  opt Caché adoptada tras evaluación de diseño
    Motor -> Cache : Consultar representaciones vigentes
    Cache --> Motor : Datos disponibles o fallo recuperable
  end
  Motor -> Motor : Calcular similitud temática
  Motor -> Motor : Aplicar desempates RN-11 y prioridad RF24
  Motor --> Vista : Devolver Top-k y criterios de afinidad
  Vista --> Alumno : Presentar recomendaciones
end
@enduml
```

Fuente: Elaboración propia a partir de CUS02, RF06, RF24 y RN-11.

RNF03 exige inferencia de hasta 500 ms bajo hasta 50 solicitudes por minuto. Es una meta futura por medir. La elección de caché, estrategia de cómputo y separación del servicio debe justificarse con datos representativos, manteniendo el contrato de RNF09.

## 4. Reserva, confirmación y quórum (CUS04, CUS24, CUS23, CUS07)

Reservar y confirmar son acciones distintas. La reserva bloquea provisionalmente una vacante y requiere ratificación antes de T−24 h. El corte revoca las pendientes y compara las confirmadas con el 50% del aforo. La decisión de continuar o cancelar ante quórum insuficiente pertenece al mentor.

### Diagrama S-03: Reserva provisional, ratificación y resolución de quórum

```plantuml
@startuml
title S-03: CUS04 / CUS24 / CUS23 / CUS07
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
actor "Mentoreado" as Alumno
actor "Mentor" as Mentor
boundary "Vistas de reserva y contingencia" as Vista
control "BookingTransactionCoordinator" as Booking
control "QuorumEvaluatorCronService" as Cron
control "QuorumResolutionService" as Resolution
entity "Repositorio transaccional de sesión y reservas" as Repo
participant "Notificaciones institucionales" as Notify
participant "Gestión de espacios" as Space
== CUS04: Reserva provisional ==
Alumno -> Vista : Solicitar vacante en oferta PUBLICADA
Vista -> Booking : Reservar cupo
Booking -> Repo : Validar elegibilidad, horario, duplicidad y aforo
group Operación atómica sobre la sesión
  Repo -> Repo : Bloquear sesión y volver a comprobar condiciones
  alt Cupo disponible y operación válida
    Repo -> Repo : Crear PENDIENTE_CONFIRMACION y ajustar cupos
    Repo --> Booking : Reserva provisional registrada
  else Sin cupo o condiciones inválidas
    Repo --> Booking : Rechazo sin nueva reserva
  end
end
Booking --> Vista : Resultado y plazo de confirmación
== CUS24: Confirmación explícita ==
Alumno -> Vista : Ratificar asistencia
Vista -> Booking : Confirmar reserva propia
Booking -> Repo : Validar estado y hora del servidor bajo el mismo bloqueo
alt Ventana abierta antes de T-24h y reserva pendiente
  Repo -> Repo : Cambiar a CONFIRMADA
  Repo --> Vista : Confirmación registrada
else Ventana cerrada o reserva no válida
  Repo --> Vista : Rechazar confirmación tardía
end
== CUS23: Corte T-24h ==
Cron -> Repo : Obtener sesiones con corte vencido aún no aplicado
loop Por cada sesión
  group Operación atómica e idempotente propuesta
    Repo -> Repo : Bloquear sesión y comprobar corte no aplicado
    Repo -> Repo : Pasar pendientes a NO_CONFIRMADA y liberar cupos
    Repo -> Repo : Contar CONFIRMADAS sobre aforo de sesión
    alt Confirmadas >= 50% del aforo
      Repo -> Repo : Sesión a CONFIRMADA
    else Confirmadas < 50% del aforo (incluye cero)
      Repo -> Repo : Sesión a QUORUM_INSUFICIENTE
    end
    Repo -> Repo : Registrar corte aplicado y confirmar operación
  end
  Repo --> Cron : Resultado del corte
  Cron -> Notify : Notificar confirmación o solicitar decisión del mentor
end
== CUS07: Resolución por el mentor ==
Mentor -> Vista : Consultar sesión con QUORUM_INSUFICIENTE
Mentor -> Vista : Elegir dictado excepcional o cancelación
Vista -> Resolution : Resolver contingencia autorizada
alt Dictado excepcional
  Resolution -> Repo : Cambiar a CONFIRMADA_EXCEPCIONAL
  Resolution -> Notify : Notificar a participantes confirmados
else Cancelación por quórum
  Resolution -> Repo : Sesión CANCELADA_QUORUM; reservas CANCELADA_SISTEMA
  Resolution -> Space : Liberar aula o sala (RN-10)
  Resolution -> Notify : Notificar cancelación sin penalización por quórum
end
note over Cron,Resolution
La excepción E01 de CUS07 contempla inacción hasta T-6h.
Debe conservarse al detallar la planificación de contingencias;
no equivale a cancelar automáticamente en el corte T-24h.
end note
@enduml
```

Fuente: Elaboración propia a partir de RF12–RF16, CUS04/CUS24/CUS23/CUS07 y RN-05/RN-08/RN-09/RN-10.

El modelo elimina la confirmación automática al reservar, la lista de espera no incluida en la línea base y el umbral fijo de dos alumnos. El aforo proviene de RN-05: hasta 10 en presencial y 20 en virtual; el quórum se calcula con RN-09. Los espacios se asignan al publicar mediante CUS06, no se aprovisionan por primera vez al corte. El mecanismo de bloqueo, recuperación y entrega de notificaciones queda pendiente de diseño y pruebas según RNF07 y RNF10.

## 5. Asistencia, bitácora, encuesta y visado (CUS08, CUS05, CUS22)

El mentor registra asistencia efectiva y cierra la bitácora dentro del plazo de la narrativa CUS08. El QR es un flujo alternativo: el mentoreado presenta su ticket y el mentor lo escanea. El cierre genera horas provisionales, habilita encuestas solo a asistentes y remite evidencias a auditoría. Responder una encuesta no acredita horas oficiales.

### Diagrama S-04: Registro pedagógico y validación institucional

```plantuml
@startuml
title S-04: CUS08 / CUS05 / CUS22
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
actor "Mentoreado" as Alumno
actor "Mentor" as Mentor
actor "Administrador / Tutoría" as Admin
boundary "Vistas de asistencia, encuesta y auditoría" as Vista
control "BitacoraWorkflowService" as Logbook
control "QRCodeCryptoValidator (alternativa)" as QR
control "SurveyService" as Survey
control "AuditService" as Audit
entity "Repositorio de sesión y evidencias" as Repo
== CUS08: Asistencia y bitácora ==
Mentor -> Vista : Abrir nómina de sesión autorizada
Vista -> Logbook : Consultar participantes confirmados
Logbook -> Repo : Verificar mentor, sesión y participantes
alt Marcación manual
  Mentor -> Vista : Marcar ASISTIDA o INASISTENCIA para cada alumno
else Escaneo de ticket del alumno (FA01)
  Alumno -> Mentor : Presentar ticket QR
  Mentor -> Vista : Escanear ticket
  Vista -> QR : Validar ticket, sesión y participante
  QR -> Repo : Comprobar vinculación y registro previo
  alt Ticket válido y participante autorizado
    QR --> Vista : Marcar ASISTIDA
  else Ticket inválido o ajeno
    QR --> Vista : Rechazar marcado automático
  end
end
Mentor -> Vista : Completar bitácora y confirmar cierre
Vista -> Logbook : Registrar contenido y nómina
Logbook -> Repo : Validar plazo, completitud y autorización
alt Cierre válido
  Repo -> Repo : Persistir bitácora REGISTRADA y asistencias
  Repo -> Repo : Sesión FINALIZADA; horas PROVISIONALES
  Logbook --> Vista : Cierre registrado y pendiente de visado
else Fuera de plazo o datos incompletos
  Logbook --> Vista : Rechazo; revisión extraordinaria si corresponde CUS08 E03
end
== CUS05: Encuesta ==
Alumno -> Vista : Enviar evaluación de sesión
Vista -> Survey : Validar elegibilidad y ventana
Survey -> Repo : Verificar ASISTIDA, cierre y ausencia de respuesta previa
alt Asistente y dentro de 24h del cierre
  Survey -> Repo : Registrar respuesta bajo política de privacidad por definir
  Survey --> Vista : Confirmar recepción sin acreditar horas oficiales
else Inasistente, duplicada o extemporánea
  Survey --> Vista : Rechazar evaluación
end
note over Survey,Repo
RN-13: al cerrar la ventana se procesan las calificaciones
para actualizar reputación (RF21 / MOD-07).
La separación de identidad y respuestas debe diseñarse y probarse.
end note
== CUS22: Auditoría y visado ==
Admin -> Vista : Revisar bitácora, asistencia y horas
Vista -> Audit : Registrar dictamen autorizado
Audit -> Repo : Consultar evidencias y estado previo
alt Dictamen favorable
  Audit -> Repo : Bitácora VISADA; oficializar horas sin doble cómputo
else Observaciones
  Audit -> Repo : Bitácora OBSERVADA; mantener horas sin oficializar
end
Audit --> Vista : Dictamen registrado
note over Audit,Repo
CUS13 emitirá certificados solo tras alcanzar el umbral
configurado con horas auditadas (RN-14).
CUS09 permite su descarga y verificación institucional.
end note
@enduml
```

Fuente: Elaboración propia a partir de RF17, RF18, RF26 y narrativas CUS08, CUS05 y CUS22.

La política de tokens QR no hereda una duración de RNF04, que regula la carga de interfaz. Su vigencia y prevención de reutilización requieren diseño. El vínculo de encuesta con reserva permite reidentificación en el modelo preliminar; la protección de RNF02 debe resolverse antes de afirmar anonimato. La certificación queda subordinada al visado y al umbral de RN-14.

## 6. Pendientes de diseño

Estas secuencias sirven para revisar reglas, actores y estados durante el análisis del SAD. Queda por concretar contratos REST, permisos de persistencia, estrategia de concurrencia y reintentos, planificación del corte y de su recuperación, política de QR y separación de datos personales en encuestas. La implementación y las pruebas se programarán en sus fases correspondientes.
