# Especificación de Diagramas de Secuencia en Fase de Análisis

**Proyecto:** Sistema Web P2P con Algoritmo de Recomendación para la Personalización de Mentorías Académicas en la EPIS-UPT  
**Documento Metodológico:** Documento de Arquitectura de Software (SAD) — Vista Dinámica y de Procesos  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna – Facultad de Ingeniería – Escuela Profesional de Ingeniería de Sistemas  
**Lugar y Fecha:** Tacna – Perú, 2026  

---

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | RAM / JCM | RAM | RVA | 05/09/2026 | Estructuración inicial y formateo de secuencias preliminares. |
| **2.0** | RAM / JCM | Comité de Calidad EPIS | Dirección de Escuela | 28/09/2026 | Refactorización integral hacia el estándar SAD de Análisis: adopción estricta del patrón conceptual ECB (Entity-Control-Boundary), eliminación de acoplamientos técnicos prematuros, adición de títulos formales normalizados y enriquecimiento analítico de flujos alternativos. |

---

## Tabla de Contenidos

1. [Marco Metodológico y Matriz de Trazabilidad](#1-marco-metodológico-y-matriz-de-trazabilidad)
2. [Flujo 1: Autenticación Segura y Consentimiento Informado Digital (Ley N° 29733)](#2-flujo-1-autenticación-segura-y-consentimiento-informado-digital-ley-n-29733)
3. [Flujo 2: Búsqueda Temática y Emparejamiento Híbrido Top-k de Mentores (CUS06)](#3-flujo-2-búsqueda-temática-y-emparejamiento-híbrido-top-k-de-mentores-cus06)
4. [Flujo 3: Agendamiento, Aseguramiento de Cupo y Gobernanza de Quórum en T-24h (CUS07 / CUS08)](#4-flujo-3-agendamiento-aseguramiento-de-cupo-y-gobernanza-de-quórum-en-t-24h-cus07--cus08)
5. [Flujo 4: Certificación de Asistencia por QR Dinámico, Bitácora y Acreditación de Horas (CUS11 / CUS13 / CUS14)](#5-flujo-4-certificación-de-asistencia-por-qr-dinámico-bitácora-y-acreditación-de-horas-cus11--cus13--cus14)
6. [Conclusiones Arquitectónicas de la Vista Dinámica](#6-conclusiones-arquitectónicas-de-la-vista-dinámica)

---

## 1. Marco Metodológico y Matriz de Trazabilidad

En el marco del **Documento de Arquitectura de Software (SAD)**, la modelación de la interacción dinámica durante la **fase de análisis** tiene como propósito capturar la semántica de colaboración entre los objetos del dominio sin supeditar las decisiones a tecnologías o librerías de implementación física de bajo nivel.

Para ello, los diagramas adoptan rigurosamente el patrón de análisis **ECB (Entity-Control-Boundary)** estandarizado por Ivar Jacobson y consolidado en la metodología RUP y la Ingeniería Web Basada en Modelos (UWE):
- **Actores (`actor`):** Usuarios finales (estudiantes mentoreados, mentores, directores de escuela) o disparadores temporales desatendidos (*cron daemons*) que interactúan con el sistema.
- **Objetos Frontera (`boundary`):** Elementos que median la comunicación entre los actores externos y el dominio interno del sistema web, tales como interfaces de usuario y adaptadores de servicios periféricos.
- **Objetos de Control (`control`):** Componentes orquestadores que encapsulan las reglas del negocio institucional, dirigen los algoritmos de afinidad, gobiernan la concurrencia y validan condiciones temporales críticas.
- **Objetos de Entidad (`entity`):** Representaciones conceptuales del negocio que gestionan el estado, la integridad referencial y las operaciones fundamentales de los datos académicos.

### Cuadro 1.1: Matriz de Trazabilidad entre Flujos Dinámicos y Requerimientos de Software

| N° Flujo | Código Diagrama | Caso de Uso Canónico | Requerimientos Asociados | Estereotipos Clave (Boundary / Control / Entity) | Impacto Arquitectónico y Gobernanza |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | **Diagrama S-01** | `CUS01`, `CUS02` | `RF01`, `RF02`, `RNF01` | `IU_AutenticacionAcceso`, `IU_ConsentimientoInformado`<br>`Ctrl_GestionIdentidadAcceso`<br>`CuentaUsuarioInstitucional`, `RegistroConsentimientoLegal` | Cumplimiento vinculante con la Ley N° 29733 (Protección de Datos Personales) y aislamiento de identidades académicas. |
| **2** | **Diagrama S-02** | `CUS06` | `RF04`, `RF05`, `RF06`, `RF07` | `IU_BusquedaRecomendacion`<br>`Ctrl_RecomendacionAfinidad`, `MotorInferenciaAfinidad`<br>`PerfilAcademicoEstudiante`, `MallaCurricularEPIS`, `OfertaMentoriaActiva` | Optimización del emparejamiento adaptativo mediante cálculo de similitud coseno vectorial y ponderación de desempeño histórico. |
| **3** | **Diagrama S-03** | `CUS07`, `CUS08`, `CUS23` | `RF08`, `RF09`, `RN-08`, `RN-09`, `RN-10` | `IU_ReservaSesion`, `Srv_AprovisionamientoEspacios`, `Srv_NotificacionInstitucional`<br>`Ctrl_GestionReservasQuorum`<br>`AgendaEstudiantil`, `SesionMentoria`, `ReservaCupo` | Control de concurrencia y aforo en reservas; auditoría desatendida y mitigación de deserciones en $T-24\text{ h}$. |
| **4** | **Diagrama S-04** | `CUS11`, `CUS13`, `CUS14` | `RF10`, `RF11`, `RF12`, `RF13`, `RN-12` | `IU_GestionEncuentro`, `IU_MarcacionAsistencia`, `IU_EncuestaCalidadCSAT`<br>`Ctrl_GestionAsistenciaAcreditacion`<br>`TokenPresenciaQR`, `RegistroAsistencia`, `BitacoraDocente`, `BolsaHorasReconocidas` | Fe pública de asistencia mediante tokens de vida corta (60s), trazabilidad docente de contenidos y cómputo de horas oficiales. |

Fuente: Elaboración propia.

---

## 2. Flujo 1: Autenticación Segura y Consentimiento Informado Digital (Ley N° 29733)

### 2.1. Presentación Contextual del Flujo de Autenticación y Privacidad
El presente flujo modela los protocolos de entrada y validación legal que rigen el acceso a la plataforma. Conforme a las exigencias de la **Ley N° 29733** (Ley de Protección de Datos Personales del Perú) y el Estatuto de la Universidad Privada de Tacna, todo estudiante debe autenticar su pertenencia institucional y, con carácter mandatorio durante su primera sesión, manifestar su consentimiento informado previo y expreso para el tratamiento analítico de sus calificaciones y registros curriculares. La arquitectura impide cualquier redirección hacia el catálogo formativo en tanto este consentimiento no se encuentre asentado con estampa cronológica inviolable.

### Diagrama S-01: Diagrama de Secuencia de Análisis - Autenticación y Consentimiento Informado (Ley N° 29733)

```plantuml
@startuml
title <size:12><b>Diagrama S-01: Diagrama de Secuencia de Análisis - Autenticación y Consentimiento Informado (Ley N° 29733)</b></size>\n<size:10><i>Fase de Análisis Conceptual (Modelo ECB) — Sistema Web P2P EPIS-UPT</i></size>

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Universitario\n(Pregrado EPIS)" as User
boundary "IU_AutenticacionAcceso" as IU_Auth
boundary "IU_ConsentimientoInformado" as IU_Consent
control "Ctrl_GestionIdentidadAcceso" as Ctrl_Auth
entity "CuentaUsuarioInstitucional" as Ent_User
entity "RegistroConsentimientoLegal" as Ent_Consent

User -> IU_Auth : ingresarCredencialesInstitucionales(correoUPT, contrasenia)
activate IU_Auth

IU_Auth -> Ctrl_Auth : validarIdentidadUsuario(correoUPT, contrasenia)
activate Ctrl_Auth

Ctrl_Auth -> Ent_User : verificarExistenciaYEstado(correoUPT)
activate Ent_User
Ent_User --> Ctrl_Auth : credencialesValidas, usuarioId, rolAcademico
deactivate Ent_User

Ctrl_Auth -> Ent_Consent : consultarEstadoConsentimiento(usuarioId)
activate Ent_Consent
Ent_Consent --> Ctrl_Auth : consentimientoRegistrado (Verdadero / Falso)
deactivate Ent_Consent

alt [Primer Acceso al Sistema: Consentimiento No Otorgado (Falso)]
    Ctrl_Auth --> IU_Auth : requerirAceptacionLegal(usuarioId, tokenProvisional)
    IU_Auth -> IU_Consent : invocarFormularioConsentimiento(terminosLegalesLey29733)
    deactivate IU_Auth
    activate IU_Consent

    IU_Consent --> User : desplegarTerminosTratamientoDatosAcademicos()
    User -> IU_Consent : confirmarAceptacionExpresa(autorizacionDatosSensibles: true)

    IU_Consent -> Ctrl_Auth : registrarConsentimientoInformado(usuarioId, true, estampaTiempo)
    activate Ctrl_Auth

    Ctrl_Auth -> Ent_Consent : almacenarAsientoConsentimiento(usuarioId, versionTerminos, estampaTiempo)
    activate Ent_Consent
    Ent_Consent --> Ctrl_Auth : registroLegalConforme
    deactivate Ent_Consent

    Ctrl_Auth --> IU_Consent : confirmarValidacionJuridica()
    deactivate Ctrl_Auth

    IU_Consent --> User : notificarActivacionDeCuenta()
    deactivate IU_Consent
end

Ctrl_Auth -> Ctrl_Auth : generarSesionSegura(usuarioId, rolAcademico)
Ctrl_Auth --> IU_Auth : autorizarIngresoConCredencial(contextoSesion)
activate IU_Auth
IU_Auth --> User : redireccionarAlPanelPrincipal(perfilEstudiantil)
deactivate IU_Auth
deactivate Ctrl_Auth

@enduml
```

Fuente: Elaboración propia.

### 2.2. Análisis del Flujo Dinámico y Tratamiento Jurídico-Técnico
El intercambio de mensajes evidencia una estricta segregación entre el objeto frontera `IU_AutenticacionAcceso` y la entidad `CuentaUsuarioInstitucional`, delegando en el controlador `Ctrl_GestionIdentidadAcceso` la responsabilidad de verificar el cumplimiento del consentimiento informado antes de liberar el contexto de sesión principal. La entidad `RegistroConsentimientoLegal` actúa como repositorio inmutable para fines de auditoría forense ante la Autoridad Nacional de Protección de Datos Personales, registrando inequívocamente la versión de los términos aceptados y el instante temporal de suscripción.

---

## 3. Flujo 2: Búsqueda Temática y Emparejamiento Híbrido Top-k de Mentores (CUS06)

### 3.1. Presentación Contextual del Algoritmo de Emparejamiento
El caso de uso `CUS06` describe la secuencia algorítmica y orquestación colaborativa activada cuando un alumno de ciclos tempranos (I a IV) experimenta dificultades académicas en materias filtro críticas (*Cálculo I/II, Algoritmos, Programación Orientada a Objetos, Bases de Datos*). La solución combina una comprobación de elegibilidad curricular con un motor de inferencia matemática que evalúa la cercanía semántica entre los descriptores de necesidad y las fortalezas del mentor, jerarquizando las $k$ alternativas más viables pedagógica y cronológicamente.

### Diagrama S-02: Diagrama de Secuencia de Análisis - Búsqueda Temática y Emparejamiento Híbrido Top-k (CUS06)

```plantuml
@startuml
title <size:12><b>Diagrama S-02: Diagrama de Secuencia de Análisis - Búsqueda Temática y Emparejamiento Híbrido Top-k (CUS06)</b></size>\n<size:10><i>Fase de Análisis Conceptual (Modelo ECB) — Sistema Web P2P EPIS-UPT</i></size>

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Mentoreado\n(I - IV Ciclo)" as Alumno
boundary "IU_BusquedaRecomendacion" as IU_Rec
control "Ctrl_RecomendacionAfinidad" as Ctrl_Rec
entity "PerfilAcademicoEstudiante" as Ent_Perfil
entity "MallaCurricularEPIS" as Ent_Malla
entity "OfertaMentoriaActiva" as Ent_Oferta
control "MotorInferenciaAfinidad" as Ctrl_MotorIA

Alumno -> IU_Rec : ingresarCriteriosBusqueda(asignaturaId, temaDificultad, preferenciaHoraria)
activate IU_Rec

IU_Rec -> Ctrl_Rec : solicitarRecomendacionOptimizada(estudianteId, criteriosBusqueda)
activate Ctrl_Rec

Ctrl_Rec -> Ent_Perfil : consultarHistorialAcademico(estudianteId)
activate Ent_Perfil
Ent_Perfil --> Ctrl_Rec : historialNotas, nivelRendimiento, cursosAprobados
deactivate Ent_Perfil

Ctrl_Rec -> Ent_Malla : validarCondicionMatriculaYPrerrequisito(asignaturaId, estudianteId)
activate Ent_Malla
Ent_Malla --> Ctrl_Rec : estadoHabilitacion (Apto / Bloqueado)
deactivate Ent_Malla

alt [Estudiante Apto para Recibir Mentoría en la Asignatura]
    Ctrl_Rec -> Ent_Oferta : recuperarOfertasVigentes(asignaturaId, preferenciaHoraria)
    activate Ent_Oferta
    Ent_Oferta --> Ctrl_Rec : catalogoOfertasDisponibles
    deactivate Ent_Oferta

    Ctrl_Rec -> Ctrl_MotorIA : ejecutarCalculoAfinidadHibrida(perfilEstudiante, catalogoOfertasDisponibles)
    activate Ctrl_MotorIA
    note right of Ctrl_MotorIA
      1. Similitud Coseno de descriptores temáticos.
      2. Ponderación histórica CSAT e insignias del mentor.
      3. Coeficiente de afinidad horaria y aforo libre.
    end note
    Ctrl_MotorIA --> Ctrl_Rec : rankingJerarquizadoTopK
    deactivate Ctrl_MotorIA

    Ctrl_Rec --> IU_Rec : remitirResultadosTopK(rankingJerarquizadoTopK)
    IU_Rec --> Alumno : desplegarTarjetasMentoresSugeridos(listaRankingConDetalle)

else [Estudiante Inhabilitado por Incumplimiento de Prerrequisitos]
    Ctrl_Rec --> IU_Rec : denegarSolicitudPorNormativaCurricular(motivoInhabilitacion)
    IU_Rec --> Alumno : presentarAlertaRestriccionAcademica(motivoInhabilitacion)
end

deactivate Ctrl_Rec
deactivate IU_Rec

@enduml
```

Fuente: Elaboración propia.

### 3.2. Análisis del Flujo Dinámico y Eficiencia de Selección
El controlador `Ctrl_RecomendacionAfinidad` desacopla la formulación de consultas al motor matemático `MotorInferenciaAfinidad`, garantizando que únicamente se envíen como vectores de entrada aquellas ofertas cuyos mentores poseen disponibilidad real y cuya asignatura haya sido visada curricularmente por `MallaCurricularEPIS`. Esta disposición protege la sobrecarga computacional del servidor de inferencia y reduce el tiempo de respuesta del sistema percibido por el estudiante a valores inferiores a un segundo.

---

## 4. Flujo 3: Agendamiento, Aseguramiento de Cupo y Gobernanza de Quórum en T-24h (CUS07 / CUS08)

### 4.1. Presentación Contextual de la Gobernanza Temporal y Aforo
La viabilidad logística de las mentorías académicas en la EPIS-UPT exige una doble disciplina de gestión: por un lado, asegurar que las reservas se realicen sin traslapes en la carga lectiva del estudiante ni sobrecupos en las sesiones (aforo máximo: 5 estudiantes); y por otro, ejecutar un monitoreo perentorio automatizado en la cota temporal de $T-24\text{ h}$ (24 horas antes del inicio programado). Si para dicho instante la sesión no alcanza el quórum mínimo normativo (2 estudiantes confirmados), el sistema procede a su anulación automática y desasignación de ambientes.

### Diagrama S-03: Diagrama de Secuencia de Análisis - Agendamiento, Reserva y Quórum T-24h (CUS07 / CUS08)

```plantuml
@startuml
title <size:12><b>Diagrama S-03: Diagrama de Secuencia de Análisis - Agendamiento, Reserva y Quórum T-24h (CUS07/CUS08)</b></size>\n<size:10><i>Fase de Análisis Conceptual (Modelo ECB) — Sistema Web P2P EPIS-UPT</i></size>

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Mentoreado" as Alumno
boundary "IU_ReservaSesion" as IU_Res
control "Ctrl_GestionReservasQuorum" as Ctrl_Res
entity "AgendaEstudiantil" as Ent_Agenda
entity "SesionMentoria" as Ent_Sesion
entity "ReservaCupo" as Ent_Reserva
boundary "Srv_NotificacionInstitucional" as Srv_Notif
actor "TemporizadorProgramado\n(Daemon Quórum T-24h)" as Actor_Cron
boundary "Srv_AprovisionamientoEspacios" as Srv_Espacios
actor "Estudiante Mentor" as Mentor

== Fase A: Solicitud y Bloqueo Transaccional de Cupo ==
Alumno -> IU_Res : seleccionarSesionYConfirmarReserva(sesionId)
activate IU_Res

IU_Res -> Ctrl_Res : procesarReservaCupo(estudianteId, sesionId)
activate Ctrl_Res

Ctrl_Res -> Ent_Agenda : verificarIncompatibilidadHoraria(estudianteId, fechaHoraSesion)
activate Ent_Agenda
Ent_Agenda --> Ctrl_Res : resultadoCruce (SinConflicto / ConConflicto)
deactivate Ent_Agenda

alt [Sin Conflicto de Horario]
    Ctrl_Res -> Ent_Sesion : consultarCapacidadDisponible(sesionId)
    activate Ent_Sesion
    Ent_Sesion --> Ctrl_Res : cuposRestantes
    deactivate Ent_Sesion

    alt [Cupos Restantes > 0 (Aforo Disponible)]
        Ctrl_Res -> Ent_Sesion : bloquearCupoTransaccional(sesionId)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Res : cupoBloqueado
        deactivate Ent_Sesion

        Ctrl_Res -> Ent_Reserva : registrarReserva(estudianteId, sesionId, Estado: CONFIRMADA)
        activate Ent_Reserva
        Ent_Reserva --> Ctrl_Res : reservaRegistradaId
        deactivate Ent_Reserva

        Ctrl_Res -> Srv_Notif : enviarComprobanteReserva(estudianteId, reservaRegistradaId)
        activate Srv_Notif
        Srv_Notif --> Ctrl_Res : envioExitoso
        deactivate Srv_Notif

        Ctrl_Res --> IU_Res : notificarReservaExitosa(reservaRegistradaId)
        IU_Res --> Alumno : presentarConstanciaReserva(detallesSesion)

    else [Cupos Restantes == 0 (Aforo Agotado)]
        Ctrl_Res -> Ent_Reserva : inscribirEnListaEspera(estudianteId, sesionId, Estado: EN_ESPERA)
        activate Ent_Reserva
        Ent_Reserva --> Ctrl_Res : posicionListaEspera
        deactivate Ent_Reserva

        Ctrl_Res --> IU_Res : notificarAforoCompletoConEspera(posicionListaEspera)
        IU_Res --> Alumno : desplegarMensajeListaEspera(posicionListaEspera)
    end

else [Con Conflicto de Horario]
    Ctrl_Res --> IU_Res : denegarPorTraslapeHorario(detalleConflicto)
    IU_Res --> Alumno : desplegarAlertaIncompatibilidadHoraria(detalleConflicto)
end
deactivate Ctrl_Res
deactivate IU_Res

== Fase B: Evaluación Desatendida de Quórum en T-24h ==
Actor_Cron -> Ctrl_Res : auditarQuorumSesionesEnCorte(estampaActual)
activate Ctrl_Res

Ctrl_Res -> Ent_Sesion : consultarSesionesEnVentana(T_menos_24h)
activate Ent_Sesion
Ent_Sesion --> Ctrl_Res : listaSesionesEvaluables
deactivate Ent_Sesion

loop Por cada sesión pendiente de corte en T-24h
    Ctrl_Res -> Ent_Reserva : contarInscritosConfirmados(sesionId)
    activate Ent_Reserva
    Ent_Reserva --> Ctrl_Res : totalConfirmados
    deactivate Ent_Reserva

    alt [totalConfirmados >= QuorumMinimo (>= 2 estudiantes)]
        Ctrl_Res -> Ent_Sesion : ratificarSesion(sesionId, Estado: RATIFICADA)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Res : estadoActualizado
        deactivate Ent_Sesion

        Ctrl_Res -> Srv_Espacios : solicitarAprovisionamiento(modalidad, totalConfirmados)
        activate Srv_Espacios
        Srv_Espacios --> Ctrl_Res : coordenadasAcceso(aulaFisicaOEnlaceVirtual)
        deactivate Srv_Espacios

        Ctrl_Res -> Ent_Sesion : consolidarUbicacionAcceso(sesionId, aulaFisicaOEnlaceVirtual)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Res : sesionConfirmada
        deactivate Ent_Sesion

        Ctrl_Res -> Srv_Notif : despacharNotificacionSesionLista(mentorId, listaAlumnos, coordenadasAcceso)
        activate Srv_Notif
        Srv_Notif -> Mentor : notificarConfirmacionSesion(detallesCompletos)
        Srv_Notif -> Alumno : notificarConfirmacionYAcceso(detallesCompletos)
        Srv_Notif --> Ctrl_Res : despachoMasivoConcluido
        deactivate Srv_Notif

    else [totalConfirmados < QuorumMinimo (< 2 estudiantes)]
        Ctrl_Res -> Ent_Sesion : registrarCancelacionPorQuorum(sesionId, Motivo: INSUFICIENCIA_QUORUM)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Res : sesionCancelada
        deactivate Ent_Sesion

        Ctrl_Res -> Ent_Reserva : anularReservasAsociadas(sesionId)
        activate Ent_Reserva
        Ent_Reserva --> Ctrl_Res : reservasLiberadas
        deactivate Ent_Reserva

        Ctrl_Res -> Srv_Notif : despacharAlertasCancelacionTemprana(mentorId, listaAlumnos)
        activate Srv_Notif
        Srv_Notif -> Mentor : alertarSesionCanceladaPorFaltaQuorum()
        Srv_Notif -> Alumno : alertarCancelacionYLiberacionDeHorario()
        Srv_Notif --> Ctrl_Res : alertasDespachadas
        deactivate Srv_Notif
    end
end
deactivate Ctrl_Res

@enduml
```

Fuente: Elaboración propia.

### 4.2. Análisis del Flujo Dinámico y Mitigación de Deserciones
El diagrama S-03 articula el comportamiento reactivo e interactivo del sistema: el primer segmento asegura la concurrencia atómica de plazas previniendo la sobreventa (*overselling*) de cupos formativos; mientras que el segundo segmento sustituye la incertidumbre de cancelaciones tardías por un proceso determinístico desatendido. Al ejecutar la cancelación en $T-24\text{ h}$, el mentor recupera su disponibilidad para estudiar o descansar, y los mentoreados quedan habilitados inmediatamente para buscar otras sesiones antes del fin de semana.

---

## 5. Flujo 4: Certificación de Asistencia por QR Dinámico, Bitácora y Acreditación de Horas (CUS11 / CUS13 / CUS14)

### 5.1. Presentación Contextual de la Acreditación y Fe Pública
El ciclo virtuoso de la mentoría concluye formalmente con la fiscalización y certificación fehaciente del servicio pedagógico prestado. El presente flujo ilustra la marcación antifraude de presencia mediante tokens QR rotativos con caducidad efímera (60 segundos), la obligatoria redacción de la bitácora docente por parte del mentor dentro de las 24 horas post-sesión, y la consecuente acumulación de horas de servicio universitario en la hoja de vida académica del mentor junto con la recolección anónima de retroalimentación CSAT.

### Diagrama S-04: Diagrama de Secuencia de Análisis - Asistencia QR Dinámico, Bitácora y Acreditación de Horas (CUS11 / CUS13 / CUS14)

```plantuml
@startuml
title <size:12><b>Diagrama S-04: Diagrama de Secuencia de Análisis - Asistencia QR Dinámico, Bitácora y Acreditación de Horas</b></size>\n<size:10><i>Fase de Análisis Conceptual (Modelo ECB) — Sistema Web P2P EPIS-UPT</i></size>

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Mentor\n(VII - X Ciclo)" as Mentor
actor "Estudiante Mentoreado\n(I - IV Ciclo)" as Alumno
boundary "IU_GestionEncuentro" as IU_Mentor
boundary "IU_MarcacionAsistencia" as IU_Alumno
boundary "IU_EncuestaCalidadCSAT" as IU_CSAT
control "Ctrl_GestionAsistenciaAcreditacion" as Ctrl_Log
entity "SesionMentoria" as Ent_Sesion
entity "TokenPresenciaQR" as Ent_TokenQR
entity "RegistroAsistencia" as Ent_Asist
entity "BitacoraDocente" as Ent_Bitacora
entity "BolsaHorasReconocidas" as Ent_Horas

== Segmento 1: Control de Presencia y Marcación QR Dinámico ==
Mentor -> IU_Mentor : solicitarProyeccionQRPresencia(sesionId)
activate IU_Mentor

IU_Mentor -> Ctrl_Log : generarTokenRotativo(sesionId, mentorId)
activate Ctrl_Log

Ctrl_Log -> Ent_Sesion : verificarEstadoEnCurso(sesionId)
activate Ent_Sesion
Ent_Sesion --> Ctrl_Log : sesionHabilitada (EN_CURSO)
deactivate Ent_Sesion

Ctrl_Log -> Ent_TokenQR : generarTokenEfimeroCifrado(sesionId, vigencia: 60s)
activate Ent_TokenQR
Ent_TokenQR --> Ctrl_Log : tokenEfimeroValido
deactivate Ent_TokenQR

Ctrl_Log --> IU_Mentor : proyectarGraficoQRDinamico(imagenQR, vigenciaRestante)
IU_Mentor --> Mentor : visualizaCodigoEnProyectorOPantalla()

Alumno -> IU_Alumno : escanearCodigoConDispositivo(imagenQR)
activate IU_Alumno

IU_Alumno -> Ctrl_Log : remitirCapturaAsistencia(estudianteId, tokenLeido, estampaTiempo)

Ctrl_Log -> Ent_TokenQR : validarVigenciaYFirma(tokenLeido, estampaTiempo)
activate Ent_TokenQR
Ent_TokenQR --> Ctrl_Log : tokenConforme (Valido / Expirado)
deactivate Ent_TokenQR

alt [Token Conforme y Dentro del Tiempo (<= 60s)]
    Ctrl_Log -> Ent_Asist : verificarInscripcionPrevia(sesionId, estudianteId)
    activate Ent_Asist
    Ent_Asist --> Ctrl_Log : yaAsentado (Falso / Verdadero)
    deactivate Ent_Asist

    alt [No Asentado Previamente]
        Ctrl_Log -> Ent_Asist : registrarAsistencia(sesionId, estudianteId, Estado: PRESENTE)
        activate Ent_Asist
        Ent_Asist --> Ctrl_Log : constanciaAsistenciaId
        deactivate Ent_Asist

        Ctrl_Log --> IU_Alumno : notificarAsistenciaRegistradaExitosa(constanciaAsistenciaId)
        IU_Alumno --> Alumno : desplegarMensajeConformidad()

        Ctrl_Log --> IU_Mentor : actualizarNavegacionAsistentesEnVivo(estudianteId, PRESENTE)
        IU_Mentor --> Mentor : reflejarAsistenteEnLista()

    else [Ya Asentado Previamente]
        Ctrl_Log --> IU_Alumno : advertirMarcacionPreexistente()
        IU_Alumno --> Alumno : desplegarAvisoRegistroDuplicado()
    end

else [Token Expirado o Fuera de Intervalo (> 60s)]
    Ctrl_Log --> IU_Alumno : denegarPorCaducidadDeToken()
    IU_Alumno --> Alumno : alertarTokenVencidoReintentar()
end

deactivate IU_Alumno

== Segmento 2: Rendición de Bitácora Docente y Cierre de Sesión ==
Mentor -> IU_Mentor : formalizarCierreDeSesion(sesionId, temasTratados, observacionesPedagogicas)
IU_Mentor -> Ctrl_Log : consignarBitacoraYCierre(sesionId, datosPedagogicos)

Ctrl_Log -> Ent_Bitacora : asentarBitacoraDocente(sesionId, temasTratados, totalAsistentes)
activate Ent_Bitacora
Ent_Bitacora --> Ctrl_Log : bitacoraAsentadaId
deactivate Ent_Bitacora

Ctrl_Log -> Ent_Sesion : actualizarEstado(sesionId, Estado: FINALIZADA_PENDIENTE_VISADO)
activate Ent_Sesion
Ent_Sesion --> Ctrl_Log : sesionFinalizada
deactivate Ent_Sesion

Ctrl_Log --> IU_Mentor : acusarReciboBitacoraExitosa()
IU_Mentor --> Mentor : mostrarConstanciaDeRendicion()
deactivate IU_Mentor

== Segmento 3: Encuesta CSAT y Acreditación de Horas Universitarias ==
Ctrl_Log -> IU_CSAT : habilitarEncuestaSatisfaccion(listaEstudiantesPresentes)
activate IU_CSAT
IU_CSAT --> Alumno : solicitarEvaluacionPedagogica(escala1a5, aspectosAMejorar)
Alumno -> IU_CSAT : remitirEvaluacionAnonimizada(puntaje, comentarioAnonimo)
IU_CSAT -> Ctrl_Log : procesarCSATAnonimizado(sesionId, puntaje)
deactivate IU_CSAT

Ctrl_Log -> Ent_Horas : acumularHorasPedagogicas(mentorId, horasEfectivasSesion)
activate Ent_Horas
Ent_Horas --> Ctrl_Log : totalHorasAcumuladas, insigniasDesbloqueadas
deactivate Ent_Horas

Ctrl_Log --> Mentor : notificarIncrementoDeBolsaHoras(totalHorasAcumuladas)
deactivate Ctrl_Log

@enduml
```

Fuente: Elaboración propia.

### 5.2. Análisis del Flujo Dinámico y Fe Pública Institucional
El diagrama S-04 expone la convergencia entre tres dimensiones críticas de la solución:
1. **No repudio de presencia:** La interacción efímera entre `IU_MarcacionAsistencia`, `Ctrl_GestionAsistenciaAcreditacion` y `TokenPresenciaQR` invalida cualquier intento de registrar asistencias de manera remota mediante capturas compartidas por mensajería instantánea.
2. **Responsabilidad pedagógica:** El cierre formal de la sesión queda supeditado al asiento de `BitacoraDocente`, requisito reglamentario indispensable para que la Dirección de Escuela o el Comité de Tutoría procedan al visado oficial de horas (`CUS22`).
3. **Reconocimiento y Gamificación:** La entidad `BolsaHorasReconocidas` actualiza el balance de horas de servicio social acreditables para el egreso universitario del mentor, vinculando el estímulo institucional directamente a la calidad formativa evaluada en la encuesta CSAT.

---

## 6. Conclusiones Arquitectónicas de la Vista Dinámica

1. **Aislamiento Funcional mediante el Patrón ECB:** La modelación en cuatro flujos demuestra que ninguna capa visual interactúa de forma directa con los almacenes de datos o entidades de dominio. Todas las operaciones se encuentran canalizadas y custodiadas por controladores de análisis (`Ctrl_*`), garantizando alta cohesión y bajo acoplamiento.
2. **Robustez Transaccional y Tratamiento de Excepciones:** Los diagramas contemplan formalmente caminos alternativos (`alt` / `else`) ante contingencias del mundo real universitario: inhabilitación por prerrequisitos curriculares, incompatibilidades de cruce de horario, quórum insuficiente en $T-24\text{ h}$ y expiración de tokens dinámicos en aula.
3. **Consistencia con el Catálogo de Casos de Uso del SRS y SAD:** Los objetos de análisis modelados reflejan con fidelidad unívoca la arquitectura funcional documentada en el **FD03 (SRS)** y el **FD04 (SAD)**, garantizando una trazabilidad metodológica del 100% en el ciclo de vida del proyecto.