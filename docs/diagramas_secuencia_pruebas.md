# Diagramas de Secuencia en Fase de Análisis (Ambiente de Pruebas)

**Proyecto:** Sistema Web P2P con Algoritmo de Recomendación para la Personalización de Mentorías Académicas en la EPIS-UPT  
**Fase Metodológica:** Análisis Orientado a Objetos (RUP / UWE)  
**Institución:** Universidad Privada de Tacna – Facultad de Ingeniería – Escuela Profesional de Ingeniería de Sistemas  
**Fecha:** Tacna – Perú, 2026  

---

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Equipo de Desarrollo P2P | Comité de Calidad EPIS | Dirección de Escuela | 28/09/2026 | Creación del documento de pruebas para diagramas de secuencia en lenguaje de análisis (ECB) para los 4 casos de uso núcleo del sistema. |

---

## 1. Introducción y Marco de Análisis

El presente documento consolida la modelación dinámica de los cuatro casos de uso arquitectónicamente más significativos del **Sistema Web P2P de Mentorías**, estructurados rigurosamente bajo el **lenguaje de análisis** del Proceso Unificado (RUP) y la Ingeniería Web Basada en Modelos (UWE).

En esta etapa de análisis conceptual, los diagramas de secuencia prescinden de consideraciones tecnológicas particulares de bajo nivel (tales como sintaxis SQL, librerías ORM específicas o endpoints REST particulares), concentrándose en el **intercambio de mensajes semánticos** entre los estereotipos de análisis propuestos por Ivar Jacobson:
- **Actores (`actor`):** Entidades humanas o temporizadores externos que desencadenan o consumen los servicios del sistema.
- **Objetos Frontera (`boundary`):** Elementos mediadores que canalizan la interacción entre el entorno externo y el sistema interno.
- **Objetos de Control (`control`):** Componentes orquestadores que encapsulan las reglas de negocio, coordinan algoritmos y dirigen el flujo transaccional.
- **Objetos de Entidad (`entity`):** Representaciones conceptuales del dominio que encapsulan el estado y comportamiento de los datos del negocio.

### Cuadro 1.1: Matriz de Casos de Uso Críticos Modelados en Secuencia de Análisis

| Código CUS | Nombre del Caso de Uso | Actores Participantes | Objeto de Control Principal | Objeto Entidad Clave | Justificación Arquitectónica |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **CUS06** | Búsqueda y Recomendación Inteligente Top-k de Mentores | Estudiante Mentoreado | `Ctrl_RecomendacionTopK` | `PerfilEstudiante`, `OfertaMentoria` | Núcleo de inteligencia algorítmica para el emparejamiento adaptativo estudiante-mentor. |
| **CUS07** | Reserva y Aseguramiento Transaccional de Cupo en Sesión | Estudiante Mentoreado | `Ctrl_GestionReservas` | `SesionMentoria`, `ReservaCupo` | Manejo de aforo, control de concurrencia y prevención de conflictos de horario. |
| **CUS23** | Monitoreo y Corte Automático de Quórum en $T-24\text{ h}$ | Temporizador Programado, Estudiante Mentor, Estudiante Mentoreado | `Ctrl_VerificacionQuorum` | `SesionMentoria`, `ReservaCupo` | Automatización de la viabilidad logística y aprovisionamiento perentorio de recursos. |
| **CUS13** | Marcación y Verificación de Asistencia por Código QR Dinámico | Estudiante Mentor, Estudiante Mentoreado | `Ctrl_ControlAsistencia` | `TokenAsistenciaQR`, `RegistroAsistencia` | Blindaje antifraude y fe pública en la constancia de presencia académica. |

Fuente: Elaboración propia.

---

## 2. Diagrama de Secuencia S-01: Búsqueda y Recomendación Inteligente Top-k de Mentores (`CUS06`)

### 2.1. Presentación Contextual del Caso de Uso CUS06
El caso de uso `CUS06` describe la secuencia interactiva mediante la cual un estudiante de ciclo temprano (I a IV ciclo) ingresa sus dificultades temáticas en una asignatura específica y solicita recomendaciones personalizadas. El sistema extrae el perfil académico del estudiante, valida que la asignatura no presente impedimentos de prerrequisitos, filtra las ofertas de mentoría activas y orquesta la ejecución del motor de afinidad para entregar un ordenamiento Top-k jerarquizado.

### Diagrama S-01: Diagrama de Secuencia de Análisis - Recomendación Inteligente Top-k de Mentores (CUS06)

```plantuml
@startuml
title Diagrama de Secuencia de Análisis S-01: Recomendación Top-k de Mentores (CUS06)\nLenguaje Conceptual ECB (Entity-Control-Boundary)

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Mentoreado\n(I - IV Ciclo)" as Alumno
boundary "IU_RecomendacionMentoria" as IU_Rec
control "Ctrl_RecomendacionTopK" as Ctrl_Rec
entity "PerfilEstudiante" as Ent_Perfil
entity "MallaCurricular" as Ent_Malla
entity "OfertaMentoria" as Ent_Oferta
control "MotorCalculoAfinidad" as Ctrl_IA

Alumno -> IU_Rec : solicitarRecomendacion(temaDificultad, asignaturaId, horarioPreferencia)
activate IU_Rec

IU_Rec -> Ctrl_Rec : obtenerRecomendaciones(estudianteId, criteriosBusqueda)
activate Ctrl_Rec

Ctrl_Rec -> Ent_Perfil : consultarHistorialAcademico(estudianteId)
activate Ent_Perfil
Ent_Perfil --> Ctrl_Rec : datosRendimiento, cursosAprobados
deactivate Ent_Perfil

Ctrl_Rec -> Ent_Malla : validarPrerrequisitosMatricula(asignaturaId, estudianteId)
activate Ent_Malla
Ent_Malla --> Ctrl_Rec : estadoHabilitacionValido
deactivate Ent_Malla

Ctrl_Rec -> Ent_Oferta : consultarOfertasActivas(asignaturaId, horarioPreferencia)
activate Ent_Oferta
Ent_Oferta --> Ctrl_Rec : listaOfertasCompatibles
deactivate Ent_Oferta

Ctrl_Rec -> Ctrl_IA : computarAfinidadTopK(datosRendimiento, listaOfertasCompatibles)
activate Ctrl_IA
note right of Ctrl_IA
  Calcula similitud temática,
  ponderación por CSAT histórico
  y compatibilidad horaria.
end note
Ctrl_IA --> Ctrl_Rec : rankingOrdenadoTopK
deactivate Ctrl_IA

Ctrl_Rec --> IU_Rec : entregarListaRecomendaciones(rankingOrdenadoTopK)
deactivate Ctrl_Rec

IU_Rec --> Alumno : presentarMentoresSugeridos(listaDetallada)
deactivate IU_Rec

@enduml
```

Fuente: Elaboración propia.

### 2.2. Análisis del Flujo Dinámico y Ciclo de Vida
El diagrama S-01 formaliza cómo el objeto de control `Ctrl_RecomendacionTopK` asume la responsabilidad de coordinar las consultas a las entidades `PerfilEstudiante` y `MallaCurricular` antes de solicitar el conjunto de ofertas de mentoría. De este modo, se garantiza que el motor de afinidad opere únicamente sobre candidatos viables desde la perspectiva reglamentaria de la carrera, optimizando el procesamiento y entregando al mentoreado una nómina precalificada y ordenada por pertinencia pedagógica.

---

## 3. Diagrama de Secuencia S-02: Reserva y Aseguramiento Transaccional de Cupo en Sesión (`CUS07`)

### 3.1. Presentación Contextual del Caso de Uso CUS07
El caso de uso `CUS07` modela la secuencia de operaciones requeridas para que un estudiante asegure una vacante en una sesión grupal o individual ofertada por un mentor. El flujo contempla la verificación rigurosa de incompatibilidades horarias personales y la comprobación atómica del aforo disponible, derivando en la confirmación de la plaza o en la incorporación ordenada a una lista de espera.

### Diagrama S-02: Diagrama de Secuencia de Análisis - Reserva y Aseguramiento de Cupo (CUS07)

```plantuml
@startuml
title Diagrama de Secuencia de Análisis S-02: Reserva y Aseguramiento de Cupo (CUS07)\nLenguaje Conceptual ECB (Entity-Control-Boundary)

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Mentoreado\n(I - IV Ciclo)" as Alumno
boundary "IU_ReservaSesion" as IU_Res
control "Ctrl_GestionReservas" as Ctrl_Res
entity "HorarioEstudiante" as Ent_Horario
entity "SesionMentoria" as Ent_Sesion
entity "ReservaCupo" as Ent_Reserva
boundary "ServicioNotificacion" as Srv_Notif

Alumno -> IU_Res : confirmarIntencionReserva(sesionId)
activate IU_Res

IU_Res -> Ctrl_Res : procesarReserva(estudianteId, sesionId)
activate Ctrl_Res

Ctrl_Res -> Ent_Horario : verificarCruceHorario(estudianteId, fechaHoraSesion)
activate Ent_Horario
Ent_Horario --> Ctrl_Res : estadoCruce (SinCruce / ConConflicto)
deactivate Ent_Horario

alt [Sin Cruce Horario]
    Ctrl_Res -> Ent_Sesion : consultarAforoDisponible(sesionId)
    activate Ent_Sesion
    Ent_Sesion --> Ctrl_Res : cuposDisponibles
    deactivate Ent_Sesion

    alt [Cupos Disponibles > 0]
        Ctrl_Res -> Ent_Sesion : decrementarAforo(sesionId)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Res : aforoActualizado
        deactivate Ent_Sesion

        Ctrl_Res -> Ent_Reserva : registrarReserva(estudianteId, sesionId, Estado: CONFIRMADA)
        activate Ent_Reserva
        Ent_Reserva --> Ctrl_Res : reservaRegistradaId
        deactivate Ent_Reserva

        Ctrl_Res -> Srv_Notif : emitirComprobanteReserva(estudianteId, reservaRegistradaId)
        activate Srv_Notif
        Srv_Notif --> Ctrl_Res : comprobanteDespachado
        deactivate Srv_Notif

        Ctrl_Res --> IU_Res : confirmarReservaExitosa(reservaRegistradaId)
        IU_Res --> Alumno : desplegarConstanciaReserva(detallesSesion)

    else [Cupos Disponibles == 0 (Aforo Completo)]
        Ctrl_Res -> Ent_Reserva : registrarEnListaEspera(estudianteId, sesionId, Estado: EN_ESPERA)
        activate Ent_Reserva
        Ent_Reserva --> Ctrl_Res : posicionListaEspera
        deactivate Ent_Reserva

        Ctrl_Res --> IU_Res : notificarAforoCompleto(posicionListaEspera)
        IU_Res --> Alumno : mostrarAvisoListaEspera(posicionListaEspera)
    end

else [Con Conflicto de Horario]
    Ctrl_Res --> IU_Res : denegarPorIncompatibilidadHoraria(detalleConflicto)
    IU_Res --> Alumno : mostrarAlertaCruceHorario(detalleConflicto)
end

deactivate Ctrl_Res
deactivate IU_Res

@enduml
```

Fuente: Elaboración propia.

### 3.2. Análisis del Flujo Dinámico y Manejo de Alternativas
La lógica de control de `Ctrl_GestionReservas` implementa una doble barrera de integridad: primero salvaguarda la agenda académica del alumno interactuando con `HorarioEstudiante`, y posteriormente realiza la reserva atómica sobre `SesionMentoria`. Al discriminar entre cupo confirmado y lista de espera, el sistema garantiza un uso equitativo del límite máximo de 5 estudiantes por sesión presencial o virtual establecido en los requerimientos normativos.

---

## 4. Diagrama de Secuencia S-03: Monitoreo y Corte Automático de Quórum en $T-24\text{ h}$ (`CUS23`)

### 4.1. Presentación Contextual del Caso de Uso CUS23
El caso de uso `CUS23` describe la orquestación temporal que se activa de forma desatendida 24 horas antes del inicio programado de cualquier sesión de mentoría. Un temporizador del sistema invoca al controlador para auditar si se cumple el umbral mínimo reglamentario (2 estudiantes). En caso positivo, se ratifica la sesión y se gestiona el ambiente físico o virtual; en caso negativo, se cancela preventivamente liberando la disponibilidad de los participantes.

### Diagrama S-03: Diagrama de Secuencia de Análisis - Corte Automático de Quórum en T-24h (CUS23)

```plantuml
@startuml
title Diagrama de Secuencia de Análisis S-03: Monitoreo y Corte de Quórum en T-24h (CUS23)\nLenguaje Conceptual ECB (Entity-Control-Boundary)

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "TemporizadorProgramado\n(Cron del Sistema)" as Actor_Cron
control "Ctrl_VerificacionQuorum" as Ctrl_Quorum
entity "SesionMentoria" as Ent_Sesion
entity "ReservaCupo" as Ent_Reserva
boundary "ServicioAprovisionamiento" as Srv_Aprovisiona
boundary "ServicioNotificacion" as Srv_Notif
actor "Estudiante Mentor" as Actor_Mentor
actor "Estudiante Mentoreado" as Actor_Alumno

Actor_Cron -> Ctrl_Quorum : ejecutarCorteTemporalQuorum(tiempoActual)
activate Ctrl_Quorum

Ctrl_Quorum -> Ent_Sesion : consultarSesionesEnVentanaCorte(T_menos_24h)
activate Ent_Sesion
Ent_Sesion --> Ctrl_Quorum : listaSesionesPorEvaluar
deactivate Ent_Sesion

loop Por cada sesión pendiente en ventana T-24h
    Ctrl_Quorum -> Ent_Reserva : contabilizarReservasConfirmadas(sesionId)
    activate Ent_Reserva
    Ent_Reserva --> Ctrl_Quorum : totalInscritosConfirmados
    deactivate Ent_Reserva

    alt [totalInscritosConfirmados >= QuorumMinimo (2 alumnos)]
        Ctrl_Quorum -> Ent_Sesion : ratificarEstadoSesion(sesionId, Estado: RATIFICADA)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Quorum : estadoActualizado
        deactivate Ent_Sesion

        Ctrl_Quorum -> Srv_Aprovisiona : solicitarAmbienteOSala(modalidad, aforoConfirmado)
        activate Srv_Aprovisiona
        Srv_Aprovisiona --> Ctrl_Quorum : datosUbicacionOEnlace(aulaOEnlaceVirtual)
        deactivate Srv_Aprovisiona

        Ctrl_Quorum -> Ent_Sesion : registrarCoordenadasAcceso(sesionId, aulaOEnlaceVirtual)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Quorum : sesionAprovisionada
        deactivate Ent_Sesion

        Ctrl_Quorum -> Srv_Notif : notificarSesionRatificada(mentorId, listaAlumnos, aulaOEnlaceVirtual)
        activate Srv_Notif
        Srv_Notif -> Actor_Mentor : remitirConfirmacionYAcceso(detallesSesion)
        Srv_Notif -> Actor_Alumno : remitirConfirmacionYAcceso(detallesSesion)
        Srv_Notif --> Ctrl_Quorum : notificacionesEnviadas
        deactivate Srv_Notif

    else [totalInscritosConfirmados < QuorumMinimo (Quórum Insuficiente)]
        Ctrl_Quorum -> Ent_Sesion : cancelarSesion(sesionId, Motivo: FALTA_DE_QUORUM)
        activate Ent_Sesion
        Ent_Sesion --> Ctrl_Quorum : sesionCancelada
        deactivate Ent_Sesion

        Ctrl_Quorum -> Ent_Reserva : anularReservas(sesionId, Motivo: SESION_CANCELADA)
        activate Ent_Reserva
        Ent_Reserva --> Ctrl_Quorum : reservasAnuladas
        deactivate Ent_Reserva

        Ctrl_Quorum -> Srv_Notif : notificarCancelacionPorQuorum(mentorId, listaAlumnos)
        activate Srv_Notif
        Srv_Notif -> Actor_Mentor : alertarCancelacionTemprana(motivo)
        Srv_Notif -> Actor_Alumno : alertarCancelacionYLiberacion(motivo)
        Srv_Notif --> Ctrl_Quorum : alertasEnviadas
        deactivate Srv_Notif
    end
end

deactivate Ctrl_Quorum

@enduml
```

Fuente: Elaboración propia.

### 4.2. Análisis del Flujo Dinámico y Resiliencia Operativa
El diagrama S-03 ilustra el carácter proactivo de la plataforma. Al delegar la evaluación en un temporizador de sistema y en el controlador `Ctrl_VerificacionQuorum`, se elimina la necesidad de arbitraje manual por parte del mentor o los alumnos. Asimismo, la integración conceptual con `ServicioAprovisionamiento` garantiza que ningún recurso físico (aulas de laboratorio) o virtual (enlaces de Google Meet) sea reservado en vano para sesiones desiertas.

---

## 5. Diagrama de Secuencia S-04: Marcación y Verificación de Asistencia por Código QR Dinámico (`CUS13`)

### 5.1. Presentación Contextual del Caso de Uso CUS13
El caso de uso `CUS13` modela el procedimiento mediante el cual se certifica la presencia física o sincrónica de los estudiantes en la mentoría. A fin de evitar el plagio o la divulgación no autorizada de credenciales, el mentor solicita a través de su interfaz la emisión de códigos QR efímeros cuya vigencia se encuentra estrictamente acotada a una ventana de tiempo (60 segundos). La captura oportuna por parte del mentoreado valida el token, asienta la asistencia de forma fehaciente y alimenta la bitácora de control docente.

### Diagrama S-04: Diagrama de Secuencia de Análisis - Verificación de Asistencia por Código QR Dinámico (CUS13)

```plantuml
@startuml
title Diagrama de Secuencia de Análisis S-04: Verificación de Asistencia por QR Dinámico (CUS13)\nLenguaje Conceptual ECB (Entity-Control-Boundary)

autonumber
skinparam style strictuml
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

actor "Estudiante Mentor" as Actor_Mentor
actor "Estudiante Mentoreado" as Actor_Alumno
boundary "IU_GestionSesion" as IU_Mentor
boundary "IU_MarcacionAsistencia" as IU_Alumno
control "Ctrl_ControlAsistencia" as Ctrl_Asist
entity "SesionMentoria" as Ent_Sesion
entity "TokenAsistenciaQR" as Ent_TokenQR
entity "RegistroAsistencia" as Ent_Asistencia
entity "BitacoraDocente" as Ent_Bitacora

== Emisión de Token QR Efímero por el Mentor ==
Actor_Mentor -> IU_Mentor : solicitarProyeccionQRAsistencia(sesionId)
activate IU_Mentor

IU_Mentor -> Ctrl_Asist : generarTokenQREfimero(sesionId, mentorId)
activate Ctrl_Asist

Ctrl_Asist -> Ent_Sesion : verificarEstadoSesion(sesionId)
activate Ent_Sesion
Ent_Sesion --> Ctrl_Asist : estadoSesion (EN_CURSO)
deactivate Ent_Sesion

Ctrl_Asist -> Ent_TokenQR : crearTokenDinamico(sesionId, vigencia: 60s)
activate Ent_TokenQR
Ent_TokenQR --> Ctrl_Asist : tokenEfimeroGenerado
deactivate Ent_TokenQR

Ctrl_Asist --> IU_Mentor : entregarCodigoQR(imagenQR, vigenciaRestante)
IU_Mentor --> Actor_Mentor : proyectarQREnPantalla(imagenQR)

== Escaneo y Validación por el Estudiante Mentoreado ==
Actor_Alumno -> IU_Alumno : escanearCodigoProyectado(imagenQR)
activate IU_Alumno

IU_Alumno -> Ctrl_Asist : registrarAsistenciaConToken(estudianteId, tokenLeido, timestampCaptura)

Ctrl_Asist -> Ent_TokenQR : validarVigenciaYFirma(tokenLeido, timestampCaptura)
activate Ent_TokenQR
Ent_TokenQR --> Ctrl_Asist : resultadoValidacion (Valido / Expirado)
deactivate Ent_TokenQR

alt [Token Válido (Dentro de los 60s)]
    Ctrl_Asist -> Ent_Asistencia : verificarAsistenciaPrevia(sesionId, estudianteId)
    activate Ent_Asistencia
    Ent_Asistencia --> Ctrl_Asist : yaRegistrado (Falso / Verdadero)
    deactivate Ent_Asistencia

    alt [No Registrado Previamente]
        Ctrl_Asist -> Ent_Asistencia : asentarAsistencia(sesionId, estudianteId, Estado: PRESENTE)
        activate Ent_Asistencia
        Ent_Asistencia --> Ctrl_Asist : registroConformeId
        deactivate Ent_Asistencia

        Ctrl_Asist -> Ent_Bitacora : registrarPresenciaEnBitacora(sesionId, estudianteId)
        activate Ent_Bitacora
        Ent_Bitacora --> Ctrl_Asist : bitacoraActualizada
        deactivate Ent_Bitacora

        Ctrl_Asist --> IU_Alumno : notificarAsistenciaConforme(registroConformeId)
        IU_Alumno --> Actor_Alumno : mostrarConfirmacionAsistenciaExitosa()

        Ctrl_Asist --> IU_Mentor : actualizarListaAsistentesEnVivo(estudianteId, Estado: PRESENTE)
        IU_Mentor --> Actor_Mentor : refrescarPanelAsistencia()

    else [Ya Registrado Previamente]
        Ctrl_Asist --> IU_Alumno : advertirAsistenciaDuplicada()
        IU_Alumno --> Actor_Alumno : mostrarAlertaAsistenciaYaRegistrada()
    end

else [Token Expirado o Inválido (> 60 segundos)]
    Ctrl_Asist --> IU_Alumno : denegarPorTokenExpirado()
    IU_Alumno --> Actor_Alumno : mostrarErrorTokenVencidoReintentar()
end

deactivate Ctrl_Asist
deactivate IU_Alumno
deactivate IU_Mentor

@enduml
```

Fuente: Elaboración propia.

### 5.2. Análisis del Flujo Dinámico y Mitigación de Fraude
La interacción entre `TokenAsistenciaQR` y `Ctrl_ControlAsistencia` materializa el principio de no repudio y presencia física efectiva. Al restringir la validez a un token con ciclo de vida corto ($60\text{ s}$), se previene que una captura de pantalla sea reenviada a estudiantes ausentes. La sincronización simultánea con `IU_Mentor` otorga al mentor visibilidad inmediata sobre los alumnos incorporados a la sesión antes del cierre formal en `BitacoraDocente`.

---

## 6. Conclusiones Metodológicas y Trazabilidad

1. **Separación de Responsabilidades:** Los cuatro diagramas evidencian que ninguna interfaz interactúa directamente con objetos de entidad; todas las decisiones operativas, cálculos de umbrales y validaciones temporales quedan resguardadas dentro de los objetos de control (`Ctrl_*`).
2. **Robustez ante Situaciones Excepcionales:** Cada diagrama modela explícitamente los fragmentos combinados `alt` / `else` para tratar condiciones de carrera (aforo completo), incompatibilidades de agenda (cruces de horarios), deserciones tempranas (falta de quórum) y ventanas temporales de expiración (tokens QR obsoletos).
3. **Alineación con el SAD:** Los objetos de control modelados se corresponden unívocamente con los componentes identificados en la Vista Lógica preliminar y en el Diagrama Contextual de la arquitectura del sistema.
