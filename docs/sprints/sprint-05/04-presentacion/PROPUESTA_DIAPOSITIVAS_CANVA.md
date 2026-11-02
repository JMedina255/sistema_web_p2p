# Propuesta Maestra y Guion de Diapositivas para Canva — Sprint 05
## «Ratificación de Asistencia, Desistimiento Voluntario, Gestión Transaccional de Aforos y Seguridad en T-24h»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Consultor:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend, UI Accesible y Navegación  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Lógica de Dominio y Concurrencia  
**Documento Técnico:** `docs/sprints/sprint-05/04-presentacion/PROPUESTA_DIAPOSITIVAS_CANVA.md`  
**Línea Base Evaluada:** Commit [`1ed8a046e0b214082042a3172b12d2c98b3d0b90`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) (02/11/2026)  
**Estado:** Guion Aprobado y Congelado (Insumo Oficial para la Generación Visual en Canva)  

---

## Estructura General de la Presentación (14 Diapositivas)

```
[I. Marco Institucional y Planificación]
  • Diapositiva 01: Portada Institucional y Ficha Técnica del Sprint 05
  • Diapositiva 02: Objetivo del Sprint, Backlog Comprometido y Distribución de Esfuerzo (5.0h)
  • Diapositiva 03: Marco Normativo y Reglas Institucionales (RN-05, RN-08, RN-09, RN-10)

[II. Ingeniería de Requisitos y Modelado Conceptual]
  • Diapositiva 04: Requisito Funcional RF13 y CUS24: Ratificación Anticipada de Asistencia
  • Diapositiva 05: Requisito Funcional RF14 y CUS17: Desistimiento Voluntario y Liberación de Plazas
  • Diapositiva 06: Modelado Visual: Diagrama de Secuencia de Ratificación y Desistimiento
  • Diapositiva 07: Modelado de Dominio: Máquina de Estados del Ciclo de Vida de la Reserva

[III. Implementación y Arquitectura Técnica]
  • Diapositiva 08: Capa de Presentación (T-25 / T-27): Interfaz Reactiva Accesible (WCAG 2.1 AA)
  • Diapositiva 09: Capa Servidora (T-26 / T-28): Contratos REST FastAPI, Pydantic v2 y Control T-24h
  • Diapositiva 10: Coordinador Transaccional ACID y Concurrencia Multihilo (RNF07, 0.0% Sobrecupo)
  • Diapositiva 11: Endurecimiento de Seguridad: Aislamiento de Identidad por Token JWT (RNF02)

[IV. Verificación, Evidencias y Transición]
  • Diapositiva 12: Aseguramiento de Calidad: 443 Pruebas Automatizadas y Coberturas Independientes
  • Diapositiva 13: Demostración Empírica, Corrección Ruff en CI y Delimitación de Persistencia
  • Diapositiva 14: Balance de Cierre, Dictamen de Aceptación DoD y Puente hacia el Sprint 06
```

---

## Desarrollo Detallado por Diapositiva

### Diapositiva 01: Portada Institucional y Ficha Técnica del Sprint 05
* **Objetivo Pedagógico:** Presentar formalmente el incremento de software del Sprint 05, identificando el proyecto, la cátedra, los integrantes y los parámetros de auditoría Git.
* **Componentes Visuales Sugeridos en Canva:**
  - Logotipo oficial de la Universidad Privada de Tacna (UPT) y la Escuela Profesional de Ingeniería de Sistemas (EPIS).
  - Título destacado: *«Sprint 05: Ratificación de Asistencia, Desistimiento Voluntario y Gestión Transaccional de Aforos en T-24h»*.
  - Subtítulo: *Sistema Web P2P de Mentorías Académicas con Algoritmo de Recomendación*.
  - Cuadro de datos: Curso Construcción de Software I (2026-II), Docente: Dr. Ricardo Eduardo Valcárcel Alvarado.
  - Integrantes Grupo 03: Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani.
  - Hash del commit de cierre: `1ed8a04` en `main`.
* **Guion de Exposición (Joan Medina):**
  > «Buenas tardes, Dr. Valcárcel y compañeros. El Grupo 03 presenta la sustentación del Sprint 05 de nuestro Sistema Web P2P de Mentorías Académicas EPIS-UPT. En esta iteración consolidamos el ciclo de vida posterior a la reserva preliminar de cupos, abordando la ratificación formal de asistencia y el desistimiento voluntario oportuno bajo la regla de corte a 24 horas previas al evento.»
* **Fuente Canónica:** `docs/diseño/G03_EPIS_Informe_Sprint_05.md` (Sección 1).

---

### Diapositiva 02: Objetivo del Sprint, Backlog Comprometido y Distribución de Esfuerzo
* **Objetivo Pedagógico:** Sustentar la planificación técnica, demostrando correspondencia biunívoca entre la carga horaria comprometida (5.0 horas) y las tareas ejecutadas.
* **Componentes Visuales Sugeridos en Canva:**
  - Tarjetas comparativas Plan vs Real: 5.0 h planificadas vs 5.0 h ejecutadas (100% cumplimiento).
  - Tabla de asignación de tareas:
    - T-25: Interfaz de confirmación de asistencia (Joan, 1.0 h)
    - T-26: API de ratificación con control temporal (Renzo, 2.0 h)
    - T-27: Interfaz de desistimiento en la interfaz (Joan, 1.0 h)
    - T-28: Anulación y liberación atómica de cupos (Renzo, 1.0 h)
  - PBI trazados: `PB-014` y `PB-015`.
* **Guion de Exposición (Renzo Antayhua):**
  > «El Sprint 05 se programó como una iteración focalizada de 5 horas académicas. Su objetivo fue cerrar la brecha entre la inscripción preliminar y la asistencia real. Renzo asumió las tareas de backend T-26 y T-28 correspondientes a los servicios de control temporal y transaccionalidad, mientras que Joan ejecutó las tareas T-25 y T-27 para proveer una interfaz accesible y reactiva en el cliente.»
* **Fuente Canónica:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Apartado 4.5, Tabla 5.6).

---

### Diapositiva 03: Marco Normativo y Reglas Institucionales
* **Objetivo Pedagógico:** Explicar cómo el software modela y hace cumplir las reglas institucionales de la universidad.
* **Componentes Visuales Sugeridos en Canva:**
  - Diagrama de cuatro pilares normativos:
    - **RN-05:** Aforos inmutables (10 presencial / 20 virtual).
    - **RN-08:** Corte de ratificación anticipada hasta $T-24\text{ h}$.
    - **RN-09:** Quórum mínimo institucional del 50%.
    - **RN-10:** Desistimiento voluntario hasta $T-24\text{ h}$.
  - Fórmulas visuales de control temporal: $\Delta t = \text{fecha\_inicio} - \text{ahora\_utc} > 24\text{ h}$.
* **Guion de Exposición (Joan Medina):**
  > «Las reglas RN-08 y RN-10 fijan la ventana de corte a 24 horas del inicio. Si el estudiante confirma con más de 24 horas de anticipación, su plaza se ratifica; si desiste dentro del plazo, el cupo se restituye de inmediato al aforo de la sesión para que otro estudiante lo aproveche. Si intenta actuar a menos de 24 horas, el sistema bloquea la operación para proteger la planificación de la mentoría.»
* **Fuente Canónica:** `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (Sección de Reglas de Negocio).

---

### Diapositiva 04: Requisito Funcional RF13 y CUS24: Ratificación Anticipada de Asistencia
* **Objetivo Pedagógico:** Detallar la especificación del requerimiento RF13 y el flujo de confirmación.
* **Componentes Visuales Sugeridos en Canva:**
  - Ficha canónica de RF13 / CUS24 (Confirmar Asistencia Anticipada).
  - Captura del botón «Confirmar asistencia» en estado activo (verde/azul) y deshabilitado (gris por vencimiento).
  - Criterio de aceptación: mutación a `CONFIRMADA` y registro de `fecha_confirmacion`.
* **Guion de Exposición (Joan Medina):**
  > «Bajo RF13 y CUS24, el mentoreado formaliza su compromiso de asistencia. En la interfaz, un temporizador visual indica el tiempo restante antes del cierre de ventana. Al hacer clic en 'Confirmar asistencia', la reserva pasa a estado CONFIRMADA. Si la ventana ha expirado, el botón se bloquea automáticamente evitando transacciones inválidas.»
* **Fuente Canónica:** `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (RF13, CUS24).

---

### Diapositiva 05: Requisito Funcional RF14 y CUS17: Desistimiento Voluntario y Liberación de Plazas
* **Objetivo Pedagógico:** Explicar el requerimiento RF14 y la mecánica de liberación de cupos.
* **Componentes Visuales Sugeridos en Canva:**
  - Ficha canónica de RF14 / CUS17 (Cancelar Reserva de Mentoría).
  - Captura del modal accesible de cancelación con selector de motivos (cruce de horario, imprevisto personal, salud).
  - Ecuación de restitución de aforo: $\text{cupos\_disponibles} = \min(\text{cupos\_disponibles} + 1, \text{cupos\_totales})$.
* **Guion de Exposición (Renzo Antayhua):**
  > «El requerimiento RF14 otorga al estudiante la facultad de cancelar su inscripción si surge un imprevisto, siempre que lo haga con al menos 24 horas de antelación. Esta acción es crítica: no solo marca la reserva como CANCELADA_USUARIO, sino que devuelve atómicamente la vacante a la sesión, permitiendo que las plazas limitadas se aprovechen al máximo.»
* **Fuente Canónica:** `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (RF14, CUS17).

---

### Diapositiva 06: Modelado Visual: Diagrama de Secuencia de Ratificación y Desistimiento
* **Objetivo Pedagógico:** Exhibir la coreografía de mensajes entre navegador, API REST, servicios de aplicación y base de datos.
* **Componentes Visuales Sugeridos en Canva:**
  - Renderizado del diagrama PlantUML de secuencia (Diagrama 1 del informe G03).
  - Resaltar los flujos alternativos: 403 Forbidden (usuario no propietario) y 400 Bad Request (plazo vencido).
* **Guion de Exposición (Renzo Antayhua):**
  > «En el diagrama de secuencia observamos la interacción técnica: el cliente envía el token JWT y el identificador de reserva; el backend extrae el usuario autenticado, evalúa la ventana temporal mediante UTC y, si todo es válido, ejecuta la actualización dentro de una transacción protegida. En caso de discrepancia de identidad, se interrumpe de inmediato con HTTP 403.»
* **Fuente Canónica:** `docs/diseño/G03_EPIS_Informe_Sprint_05.md` (Sección 5.3).

---

### Diapositiva 07: Modelado de Dominio: Máquina de Estados del Ciclo de Vida de la Reserva
* **Objetivo Pedagógico:** Demostrar la coherencia en las transiciones de estado de la entidad `ReservaCupo`.
* **Componentes Visuales Sugeridos en Canva:**
  - Renderizado del diagrama PlantUML de máquina de estados (Diagrama 2 del informe G03).
  - Transiciones clave:
    - `PENDIENTE_CONFIRMACION` $\rightarrow$ `CONFIRMADA` (T-25 / T-26).
    - `PENDIENTE_CONFIRMACION` $\rightarrow$ `CANCELADA_USUARIO` (T-27 / T-28).
    - `CONFIRMADA` $\rightarrow$ `CANCELADA_USUARIO` (T-28).
    - Transiciones futuras al Sprint 06 (`ASISTIO`, `FALTO`, `CANCELADA_SISTEMA`).
* **Guion de Exposición (Joan Medina):**
  > «La máquina de estados modela el ciclo de vida completo de la reserva. En este Sprint 05 gobernamos las transiciones desde PENDIENTE_CONFIRMACION hacia CONFIRMADA o CANCELADA_USUARIO. Dejamos el dominio preparado para que en el Sprint 06 se articulen las transiciones a CANCELADA_SISTEMA si no se alcanza el quórum del 50%, o a ASISTIO/FALTO durante la ejecución de la sesión.»
* **Fuente Canónica:** `docs/diseño/G03_EPIS_Informe_Sprint_05.md` (Sección 5.3).

---

### Diapositiva 08: Capa de Presentación (T-25 / T-27): Interfaz Reactiva Accesible
* **Objetivo Pedagógico:** Presentar los aspectos destacados de la implementación frontend en React 19 y Tailwind CSS.
* **Componentes Visuales Sugeridos en Canva:**
  - Capturas de `StudentBookingsView.tsx`:
    - Barra de navegación con contador dinámico en «Mis Reservas».
    - Pestañas de filtrado: Todas, Pendientes, Confirmadas, Canceladas.
    - Modal accesible con atributos ARIA (`role="dialog"`, trampa de foco, soporte para tecla Escape).
  - Cumplimiento de WCAG 2.1 Nivel AA.
* **Guion de Exposición (Joan Medina):**
  > «En frontend desarrollamos StudentBookingsView con estrictos estándares de accesibilidad WCAG 2.1 AA. El usuario cuenta con navegación por teclado, contraste verificado y un modal con captura de foco y escape nativo. Los estados se actualizan reactivamente en la interfaz sin necesidad de refrescar la página.»
* **Fuente Canónica:** `aplicacion/frontend/src/views/StudentBookingsView.tsx` y pruebas en Vitest.

---

### Diapositiva 09: Capa Servidora (T-26 / T-28): Contratos REST FastAPI, Pydantic v2 y Control T-24h
* **Objetivo Pedagógico:** Describir la arquitectura de la API REST y la validación tipada de esquemas.
* **Componentes Visuales Sugeridos en Canva:**
  - Ficha de endpoints:
    - `POST /api/v1/bookings/{id}/confirm` $\rightarrow$ `BookingConfirmResponse`
    - `POST /api/v1/bookings/{id}/cancel` $\rightarrow$ `BookingCancelResponse`
  - Fragmento de código de validación temporal en Python usando `datetime.now(timezone.utc)`.
  - Códigos de error tipados: `PLAZO_VENCIDO`, `NO_AUTORIZADO_RESERVA`.
* **Guion de Exposición (Renzo Antayhua):**
  > «En la capa servidora implementamos controladores REST en FastAPI con esquemas estrictos en Pydantic v2. El control temporal compara la marca de tiempo actual en UTC contra la fecha de inicio menos 24 horas. Toda solicitud fuera de ventana se rechaza con HTTP 400 tipado, garantizando respuestas uniformes y predecibles.»
* **Fuente Canónica:** `aplicacion/backend/app/api/v1/endpoints/bookings.py` y `booking_service.py`.

---

### Diapositiva 10: Coordinador Transaccional ACID y Concurrencia Multihilo (RNF07)
* **Objetivo Pedagógico:** Demostrar cómo se garantiza la prevención de sobrecupos bajo contención concurrente.
* **Componentes Visuales Sugeridos en Canva:**
  - Esquema conceptual de bloqueo pesimista / lock de concurrencia multihilo (`_booking_lock`).
  - Resultados del testbench de concurrencia:
    - 20 hilos disputando la última vacante disponible: exactamente 1 éxito (HTTP 201) y 19 rechazos (HTTP 409).
    - Tasa de sobrecupo verificada: **0.00%**.
* **Guion de Exposición (Renzo Antayhua):**
  > «Para satisfacer el requerimiento RNF07 de atomicidad, coordinamos las operaciones de reserva y liberación de cupos mediante transacciones con cerrojo de sincronización multihilo. Sometimos el sistema a pruebas de contención extrema con 20 hilos concurrentes disputando una única vacante: el sistema otorgó exactamente 1 plaza y rechazó 19, logrando un 0.0% de sobrecupo.»
* **Fuente Canónica:** `aplicacion/backend/tests/test_bookings.py` y `docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md`.

---

### Diapositiva 11: Endurecimiento de Seguridad: Aislamiento de Identidad por Token JWT (RNF02)
* **Objetivo Pedagógico:** Explicar la auditoría de seguridad y la erradicación de vulnerabilidades de autorización.
* **Componentes Visuales Sugeridos en Canva:**
  - Cuadro comparativo Antes vs Después del commit `b9db285`.
  - Eliminación de verificación permisiva por subcadena `"admin"`.
  - Extracción tipada del usuario desde el token JWT institucional y validación de propiedad en base de datos.
  - Código de protección: `reserva.id_estudiante == current_user.id_usuario`.
* **Guion de Exposición (Joan Medina):**
  > «Durante la auditoría de seguridad identificamos un bypass permisivo en reservas que evaluaba la subcadena 'admin'. En el commit b9db285 lo erradicamos por completo, forzando la autenticación estricta por token JWT y asegurando que ningún mentoreado pueda ver o mutar reservas de sus compañeros.»
* **Fuente Canónica:** Commit [`b9db285`](https://github.com/JMedina255/sistema_web_p2p/commit/b9db285) y `docs/diseño/INFORME_GENERAL_SPRINT_05.md`.

---

### Diapositiva 12: Aseguramiento de Calidad: 443 Pruebas Automatizadas y Coberturas
* **Objetivo Pedagógico:** Presentar las métricas de cobertura y la progresión histórica de pruebas del proyecto.
* **Componentes Visuales Sugeridos en Canva:**
  - Gráfico de barras de progresión de pruebas:
    - Sprint 01: 72 pruebas
    - Sprint 02: 126 pruebas
    - Sprint 03: 209 pruebas
    - Sprint 04: 339 pruebas
    - **Sprint 05: 443 pruebas passing (0 fallos)**
  - Coberturas independientes:
    - **Frontend:** 83.25% líneas (Vitest) — Supera meta del 70% (+13.25%).
    - **Backend:** 90.40% líneas (Pytest) — Supera meta del 70% (+20.40%).
* **Guion de Exposición (Joan Medina):**
  > «La batería consolidada de pruebas automatizadas alcanzó un récord de 443 pruebas con cero fallos: 265 en frontend y 178 en backend. Cumpliendo la regla de evaluación independiente de cobertura RNF09, frontend alcanzó un 83.25% y backend un 90.40%, superando holgadamente el umbral normativo del 70%.»
* **Fuente Canónica:** `docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md` (Cuadros 2.1 y 3.1).

---

### Diapositiva 13: Demostración Empírica, Corrección Ruff en CI y Delimitación de Persistencia
* **Objetivo Pedagógico:** Transparentar la gestión de incidencias técnicas y delimitar el entorno de persistencia de pruebas.
* **Componentes Visuales Sugeridos en Canva:**
  - Captura del flujo verde de GitHub Actions en el Pull Request #6 (`1ed8a04`).
  - Incidencia de linteo Ruff resuelta en commit `370766f` (`ruff format .`).
  - Nota de honestidad académica: pruebas unitarias ejecutadas sobre SQLite con cerrojos multihilo, reservando PostgreSQL / Supabase para Staging.
* **Guion de Exposición (Renzo Antayhua):**
  > «En integración continua, un fallo de espaciado en Ruff fue subsanado de inmediato con ruff format en el commit 370766f, logrando la aprobación total del flujo en GitHub Actions. Asimismo, dejamos expresa constancia de que las pruebas automatizadas se ejecutaron sobre SQLite con cerrojos multihilo, delimitando con rigor técnico el alcance previo al despliegue en PostgreSQL en la nube.»
* **Fuente Canónica:** `docs/diseño/G03_EPIS_Informe_Sprint_05.md` (Sección 5.6).

---

### Diapositiva 14: Balance de Cierre, Dictamen de Aceptación DoD y Puente hacia el Sprint 06
* **Objetivo Pedagógico:** Concluir formalmente la presentación declarando el sprint aceptado y proyectando el Sprint 06.
* **Componentes Visuales Sugeridos en Canva:**
  - Sello formal de *«Sprint 05 100% Concluido y Aprobado»*.
  - Matriz de PBI aceptados: `PB-014` y `PB-015`.
  - Próximos pasos en el Sprint 06:
    - Evaluación de quórum del 50% en $T-24\text{ h}$ (PB-017 / RF15).
    - Decisión del mentor ante contingencias (PB-018 / RF16).
    - Registro de bitácoras docentes y acreditación de horas (PB-019 / RF17).
* **Guion de Exposición (Joan Medina / Renzo Antayhua):**
  > «En conclusión, el Sprint 05 cumplió íntegramente su Definition of Done, dotando a la plataforma de estabilidad transaccional y protección de aforos. Dejamos el sistema en condiciones inmejorables para abordar el Sprint 06, donde evaluaremos el quórum del 50% y habilitaremos el registro de bitácoras docentes. Muchas gracias.»
* **Fuente Canónica:** `docs/diseño/G03_EPIS_Informe_Sprint_05.md` (Secciones 6, 7 y 8).
