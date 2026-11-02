# Mapa Maestro de Fuentes, Trazabilidad y Fundamentación Técnica — Sprint 05

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend, UI Accesible y Navegación  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Lógica de Dominio y Concurrencia Transaccional  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Documento Técnico:** `docs/sprints/sprint-05/02-trazabilidad/MAPA_FUENTES_SPRINT_05.md`  
**Estado:** Documento Maestro de Trazabilidad — Versión 1.0 (Línea Base Oficial Consolidada)  

---

## 1. Información de Auditoría y Metodología de Trazabilidad

A continuación, se detalla el entorno de control de configuración y los parámetros formales bajo los cuales se consolida la trazabilidad técnica del Sprint 05, garantizando la correspondencia biunívoca entre la ingeniería de requisitos, el diseño arquitectónico y el software ejecutable:

### Cuadro 1.1: Ficha Metodológica de Auditoría del Sprint 05

| Parámetro | Valor Registrado / Identificador Canónico |
| :--- | :--- |
| **Repositorio Oficial** | `https://github.com/JMedina255/sistema_web_p2p` |
| **Rama Base de Cierre** | `main` (integrada mediante PR #6: `integration/sprint-05`) |
| **Commit Oficial de Cierre (HEAD)** | [`1ed8a046e0b214082042a3172b12d2c98b3d0b90`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) (Commit corto: `1ed8a04`) |
| **Fecha de Corte Documental** | 02 de noviembre de 2026 |
| **Carga Horaria Planificada** | **5.0 horas académicas** (Joan Medina: 2.0 h / Renzo Antayhua: 3.0 h) |
| **Carga Horaria Ejecutada** | **5.0 horas verificadas** (100% de dedicación distribuida en T-25 a T-28) |
| **Alcance Funcional Comprometido** | `PB-014` (Ratificación de Asistencia en $T-24\text{ h}$) y `PB-015` (Desistimiento Voluntario de Reserva) |
| **Batería Consolidada de Pruebas** | **443 pruebas automatizadas pasando** (265 frontend / 178 backend) con 0 fallos |
| **Cobertura Independiente Lograda** | Frontend: **83.25%** líneas (Vitest v8) — Backend: **90.40%** líneas (Pytest-Cov) |
| **Estado en Integración Continua** | GitHub Actions Workflow aprobado (`PR #6`, Job `125486199988`) |

Fuente: Elaboración propia a partir del registro Git y la bitácora de ejecución de CI/CD.

El Cuadro 1.1 acredita que el repositorio cuenta con una línea base congelada y verificada en el commit `1ed8a04`, donde se articulan las modificaciones frontend y backend correspondientes al ciclo de vida posterior a la reserva provisional de cupos, cumpliendo con los estándares de control documental de la cátedra de Construcción de Software I.

---

## 2. Índice Maestro de Fuentes Técnicas Auditadas

Para asegurar la rigurosidad de la auditoría y evitar referencias circulares o ambiguas, se establece el inventario exhaustivo de fuentes documentales, analíticas, físicas y de código fuente auditadas en el Sprint 05:

### Cuadro 2.1: Catálogo Exhaustivo de Fuentes Autoritativas del Sprint 05

| N.º | Identificador de Artefacto | Tipo de Fuente | Ruta Relativa en Repositorio | Rango de Líneas / Componente | Descripción de la Autoridad Técnica |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **F-01** | `SRS-FD03-v2.1` | Documento Maestro | `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` | Secciones RF13, RF14, CUS17, CUS24, RN-05, RN-08, RN-09, RN-10 | Especificación canónica de requisitos funcionales y reglas de corte temporal de reservas. |
| **F-02** | `SAD-FD04-v2.0` | Documento Maestro | `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` | Vistas Lógica, de Datos y de Procesos | Arquitectura modular de reservas, estados de sesión y garantías de concurrencia ACID. |
| **F-03** | `PLAN-SP-5.6` | Plan de Sprints | `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` | Secciones 4.5, Tabla 5.6 | Distribución oficial de PBI (PB-014, PB-015), tareas T-25 a T-28 y estimación horaria. |
| **F-04** | `RULE-DOC` | Estándar Documental | `rules_doc.md` | Secciones 3.1, 3.2 | Reglas vinculantes de 11 secciones, diagramas PlantUML, delimitación de mocks y cobertura. |
| **F-05** | `RULE-DES` | Reglas de Diseño | `reglas_documentacion_diseño.md` | Reglas D-1 a D-5 | Regla quíntuple de cuadros, contratos REST tipados, esquema físico y control prescriptivo. |
| **F-06** | `MOD-BOOKING` | Modelo de Datos | `aplicacion/backend/app/models/booking.py` | Líneas 1-135 (`ReservaCupo`, `EstadoReserva`) | Definición de enumeraciones de estado, claves foráneas, índices y restricciones CHECK. |
| **F-07** | `SCH-BOOKING` | Esquemas Pydantic | `aplicacion/backend/app/schemas/booking.py` | Líneas 1-140 | Contratos de payload de confirmación y cancelación (`BookingCancelPayload`, `BookingResponse`). |
| **F-08** | `SRV-BOOKING` | Servicio de Dominio | `aplicacion/backend/app/services/booking_service.py` | Líneas 650-980 | Métodos `confirm_attendance`, `cancel_reservation`, control temporal $T-24\text{ h}$ y bloqueo pesimista. |
| **F-09** | `API-BOOKING` | Router REST FastAPI | `aplicacion/backend/app/api/v1/endpoints/bookings.py` | Líneas 1-180 | Endpoints `/my-reservations`, `/{id_reserva}/confirm` y `/{id_reserva}/cancel` con JWT estricto. |
| **F-10** | `SEC-AUTH` | Middleware de Auth | `aplicacion/backend/app/core/security.py` | Líneas 1-110 | Resolución tipada de identidad del mentoreado y eliminación de derivaciones inseguras. |
| **F-11** | `UI-BOOKINGS` | Componente Frontend | `aplicacion/frontend/src/views/StudentBookingsView.tsx` | Líneas 1-320 | Vista reactiva accesible con pestañas de filtrado, badges de estado y modal de desistimiento. |
| **F-12** | `SRV-FE-BOOK` | Cliente TypeScript | `aplicacion/frontend/src/services/bookingService.ts` | Líneas 1-210 | Adaptador tipado cliente con métodos `getMyReservations`, `confirmAttendance` y `cancelReservation`. |
| **F-13** | `TYP-BOOKING` | Contratos TypeScript | `aplicacion/frontend/src/types/booking.ts` | Líneas 1-85 | Interfaces `Booking`, `BookingCancelPayload`, `BookingState` y discriminadores de unión. |
| **F-14** | `APP-ROUTER` | Orquestador Global | `aplicacion/frontend/src/App.tsx` | Líneas 80-250 | Montaje de vista `mis-reservas` en navegación principal, badges numéricos y persistencia de sesión. |
| **F-15** | `TST-BE-BOOK` | Pruebas Backend | `aplicacion/backend/tests/test_bookings.py` | 46 pruebas automatizadas | Batería de pruebas unitarias y de integración de reservas, ratificación, corte y cancelación. |
| **F-16** | `TST-FE-BOOK` | Pruebas Frontend | `aplicacion/frontend/src/views/__tests__/StudentBookingsView.test.tsx` | 36 pruebas automatizadas | Batería de pruebas de interfaz, accesibilidad ARIA, interacción modal y filtros de estado. |

Fuente: Elaboración propia.

El Cuadro 2.1 unifica y valida los 16 artefactos clave que fundamentan la solución construida en el Sprint 05, garantizando que ninguna afirmación técnica en los informes posteriores carezca de una contraparte fáctica en el repositorio.

---

## 3. Matriz de Trazabilidad Bidireccional de Requerimientos (Sprint 05)

A continuación, se presenta la matriz de trazabilidad biunívoca que articula verticalmente cada Ítem del Product Backlog (PBI) con sus requisitos funcionales, casos de uso canónicos, reglas de negocio, tareas técnicas, código fuente, pruebas unitarias y hashes de commit:

### Cuadro 3.1: Matriz de Trazabilidad Bidireccional de Requerimientos del Sprint 05

| PBI | Requerimiento Funcional | Caso de Uso | Reglas de Negocio y RNF | Tarea ID | Responsable | Componentes de Código Fuente | Casos de Prueba Verificados | Commit Hash Oficial |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- | :--- | :---: |
| **PB-014** | **RF13**: Ratificación de asistencia a mentoría | **CUS24**: Confirmar asistencia anticipada | `RN-08`: Ratificación antes de $T-24\text{ h}$<br>`RN-09`: Quórum mínimo institucional del 50%<br>`RNF02`: Autenticación JWT y aislamiento de usuario<br>`RNF09`: Cobertura $\ge 70\%$ | **T-25** | Joan Medina (Frontend) | `StudentBookingsView.tsx`<br>`bookingService.ts`<br>`booking.ts`<br>`App.tsx` | `StudentBookingsView.test.tsx`<br>- Renderizado de botón confirmar<br>- Deshabilitación si $\Delta t \le 24\text{ h}$<br>- Feedback de ratificación exitosa | [`3047afb`](https://github.com/JMedina255/sistema_web_p2p/commit/3047afb)<br>[`017f65a`](https://github.com/JMedina255/sistema_web_p2p/commit/017f65a)<br>[`00fc4c3`](https://github.com/JMedina255/sistema_web_p2p/commit/00fc4c3) |
| **PB-014** | **RF13**: Ratificación de asistencia a mentoría | **CUS24**: Confirmar asistencia anticipada | `RN-08`: Bloqueo de confirmación en $\Delta t \le 24\text{ h}$<br>`RNF02`: Prohibición de actuar sobre reservas ajenas<br>`RNF07`: Consistencia ACID en cambio de estado | **T-26** | Renzo Antayhua (Backend) | `endpoints/bookings.py`<br>`services/booking_service.py`<br>`schemas/booking.py`<br>`models/booking.py` | `test_bookings.py`<br>- `test_confirm_attendance_success`<br>- `test_confirm_attendance_outside_window`<br>- `test_confirm_attendance_forbidden_user`<br>- `test_confirm_attendance_invalid_state` | [`d13c0ab`](https://github.com/JMedina255/sistema_web_p2p/commit/d13c0ab)<br>[`b9db285`](https://github.com/JMedina255/sistema_web_p2p/commit/b9db285) |
| **PB-015** | **RF14**: Desistimiento voluntario de reserva | **CUS17**: Cancelar reserva de mentoría | `RN-10`: Cancelación permitida antes de $T-24\text{ h}$<br>`RN-05`: Restitución al aforo inmutable<br>`RNF07`: Atomicidad con bloqueo pesimista | **T-27** | Joan Medina (Frontend) | `StudentBookingsView.tsx`<br>`bookingService.ts`<br>`types/booking.ts`<br>`App.tsx` | `StudentBookingsView.test.tsx`<br>- Apertura de modal de confirmación<br>- Selector accesible de motivo<br>- Mutación a badge `CANCELADA`<br>- Actualización reactiva de cupo | [`fb7c051`](https://github.com/JMedina255/sistema_web_p2p/commit/fb7c051)<br>[`00fc4c3`](https://github.com/JMedina255/sistema_web_p2p/commit/00fc4c3) |
| **PB-015** | **RF14**: Desistimiento voluntario de reserva | **CUS17**: Cancelar reserva de mentoría | `RN-10`: Cancelación extemporánea bloqueada ($400$)<br>`RN-05`: Incremento atómico de `cupos_disponibles`<br>`RNF07`: Bloqueo de concurrencia y $0.0\%$ sobrecupo | **T-28** | Renzo Antayhua (Backend) | `endpoints/bookings.py`<br>`services/booking_service.py`<br>`schemas/booking.py`<br>`models/booking.py` | `test_bookings.py`<br>- `test_cancel_reservation_success`<br>- `test_cancel_reservation_outside_window`<br>- `test_cancel_reservation_atomic_seat_release`<br>- `test_cancel_reservation_forbidden_non_owner` | [`dd7e3cc`](https://github.com/JMedina255/sistema_web_p2p/commit/dd7e3cc)<br>[`370766f`](https://github.com/JMedina255/sistema_web_p2p/commit/370766f) |

Fuente: Elaboración propia a partir del SRS FD03 v2.1, SAD FD04 v2.0 y el registro de pruebas del repositorio.

El Cuadro 3.1 demuestra el cierre de trazabilidad de los dos PBI asignados al Sprint 05, corroborando que cada comportamiento exigido por las reglas de negocio cuenta con validaciones de interfaz en frontend, validaciones transaccionales en backend y casos de prueba que impiden regresiones.

---

## 4. Matriz de Reglas de Negocio, Restricciones No Funcionales y Manejo de Errores

Para garantizar el cumplimiento de los requerimientos no funcionales de seguridad, integridad y rendimiento, se detallan las políticas implementadas en el sistema:

### Cuadro 4.1: Reglas de Negocio, Criterios de Aceptación y Códigos de Error HTTP

| Código | Descripción Canónica | Criterio de Verificación Empírica | Comportamiento del Sistema y Código HTTP |
| :---: | :--- | :--- | :--- |
| **RN-05** | **Aforos inmutables por modalidad:** 10 plazas en modalidad presencial y 20 plazas en virtual. | Al cancelarse una reserva válida, `cupos_disponibles` se incrementa en $1$ sin superar jamás el tope reglamentario (`cupos_totales`). | Se evalúa `cupos_disponibles = min(sesion.cupos_disponibles + 1, sesion.cupos_totales)`. HTTP `200 OK`. |
| **RN-08** | **Corte temporal de ratificación ($T-24\text{ h}$):** El estudiante debe confirmar su asistencia hasta 24 horas antes del inicio. | Si la solicitud de confirmación llega a menos de 24 horas del inicio de la sesión ($\Delta t \le 24\text{ h}$), el sistema rechaza la operación. | HTTP `400 Bad Request` con código institucional `VENTANA_CONFIRMACION_CERRADA` o `PLAZO_VENCIDO`. |
| **RN-09** | **Quórum mínimo del 50%:** Base para la evaluación de viabilidad de la sesión de mentoría a ejecutarse en el Sprint 06. | Las reservas ratificadas computan como `CONFIRMADA` para el posterior cálculo del umbral de viabilidad institucional. | Estado persistido en BD relacional: `reserva.estado_reserva = EstadoReserva.CONFIRMADA`. |
| **RN-10** | **Desistimiento voluntario oportuno ($T-24\text{ h}$):** El mentoreado puede anular su plaza hasta 24 horas antes del evento. | Si el usuario solicita cancelación con $\Delta t > 24\text{ h}$, se libera la vacante; si $\Delta t \le 24\text{ h}$, la cancelación queda bloqueada. | $\Delta t > 24\text{ h} \implies$ HTTP `200 OK` (`CANCELADA_USUARIO`).<br>$\Delta t \le 24\text{ h} \implies$ HTTP `400 Bad Request` (`PLAZO_CANCELACION_VENCIDO`). |
| **RNF02** | **Seguridad y Aislamiento de Identidad:** Control estricto de acceso basado en identidad verificada por token JWT. | Ningún usuario mentoreado puede confirmar o desistir de reservas pertenecientes a otro estudiante. Bypass "admin" eliminado. | Verificación: `reserva.id_estudiante == current_user.id_usuario`. Violación genera HTTP `403 Forbidden` (`NO_AUTORIZADO_RESERVA`). |
| **RNF05** | **Diseño Accesible (WCAG 2.1 Nivel AA):** Elementos interactivos navegables por teclado y con roles ARIA. | Modales de cancelación cuentan con `role="dialog"`, foco atrapado accesible y soporte nativo de tecla `Escape`. | Componentes conformes en Vitest (`StudentBookingsView.test.tsx`) y sin violaciones de accesibilidad. |
| **RNF07** | **Atomicidad y Prevención de Carreras:** Consistencia ACID en liberación y ocupación concurrente de cupos. | Ráfagas de cancelaciones concurrentes coordinadas mediante transacción pesimista / lock de concurrencia. | Tasa de inconsistencia o sobrecupo de exactamente $0.0\%$. Transacciones atómicas garantizadas. |
| **RNF09** | **Cobertura de Pruebas Automatizadas $\ge 70\%$:** Evaluación independiente por subsistema. | Medición independiente mediante suites de prueba sin promedio ficticio entre entornos. | Frontend: **83.25%** (Vitest).<br>Backend: **90.40%** (Pytest). Ambas superan el umbral normativo. |

Fuente: Elaboración propia a partir de las especificaciones del SRS FD03 y SAD FD04.

El Cuadro 4.1 resume los mecanismos de control que protegen el dominio académico del sistema, garantizando que el estado de las vacantes sea determinista y que ningún usuario no autenticado o extemporáneo pueda alterar el aforo institucional.

---

## 5. Registro Cronológico de Commits y Responsabilidades del Sprint 05

A continuación, se detalla la secuencia de cambios de software incorporados en el repositorio oficial durante el Sprint 05, consignando los autores, ramas de trabajo y alcances de cada commit:

### Cuadro 5.1: Historial Cronológico de Commits del Sprint 05

| Commit SHA | Fecha y Hora (UTC-5) | Autor | Mensaje Canónico del Commit | Tarea / Hito | Alcance Técnico Implementado |
| :---: | :---: | :---: | :--- | :---: | :--- |
| [`0a1f1f7`](https://github.com/JMedina255/sistema_web_p2p/commit/0a1f1f7) | 02/11/2026 09:15 | Joan Medina | `fix(frontend): enforce secure service mode resolution and remove hardcoded student identity fallback (audit B.1/B.2)` | Auditoría S5 | Corrección de seguridad en frontend eliminando mocks automáticos y asegurando resolución estricta de modo real/mock. |
| [`017f65a`](https://github.com/JMedina255/sistema_web_p2p/commit/017f65a) | 02/11/2026 10:04 | Joan Medina | `feat(frontend): prepare attendance confirmation and withdrawal service contracts (S5)` | Contratos S5 | Declaración de interfaces TypeScript `Booking`, `BookingCancelPayload`, cliente `bookingService.ts` y 206 pruebas pasando. |
| [`3047afb`](https://github.com/JMedina255/sistema_web_p2p/commit/3047afb) | 02/11/2026 10:48 | Joan Medina | `feat(frontend): implement attendance confirmation interface (T-25)` | **T-25** | Desarrollo de la vista `StudentBookingsView.tsx`, acciones de ratificación, cálculo de ventana $T-24\text{ h}$ y 229 pruebas. |
| [`fb7c051`](https://github.com/JMedina255/sistema_web_p2p/commit/fb7c051) | 02/11/2026 11:22 | Joan Medina | `feat(frontend): implement voluntary booking withdrawal interface (T-27)` | **T-27** | Modal interactivo accesible de desistimiento, selector de motivos, mutación reactiva a `CANCELADA` y 248 pruebas. |
| [`00fc4c3`](https://github.com/JMedina255/sistema_web_p2p/commit/00fc4c3) | 02/11/2026 11:50 | Joan Medina | `feat(frontend): integrate student bookings navigation and lifecycle workflows (S5)` | Integración FE | Enrutamiento en `App.tsx`, botón "Mis Reservas", badges de notificación, feedback accesible y 265 pruebas (83.25%). |
| [`b9db285`](https://github.com/JMedina255/sistema_web_p2p/commit/b9db285) | 02/11/2026 12:10 | Renzo Antayhua | `fix(backend): enforce authenticated booking ownership and authorization` | Seguridad BE | Eliminación de bypass inseguro `"admin"` en `/reserve`, forzando extracción tipada de usuario y propiedad de reserva. |
| [`d13c0ab`](https://github.com/JMedina255/sistema_web_p2p/commit/d13c0ab) | 02/11/2026 12:45 | Renzo Antayhua | `feat(backend): implement attendance confirmation endpoint (T-26)` | **T-26** | Endpoint `POST /bookings/{id}/confirm`, validación de ventana $>24\text{ h}$, transición a `CONFIRMADA` y esquemas Pydantic v2. |
| [`dd7e3cc`](https://github.com/JMedina255/sistema_web_p2p/commit/dd7e3cc) | 02/11/2026 13:18 | Renzo Antayhua | `feat(backend): implement atomic booking cancellation and seat release (T-28)` | **T-28** | Endpoint `POST /bookings/{id}/cancel`, restitución atómica de vacante en sesión, transacción protegida y 178 pruebas (90.40%). |
| [`3568118`](https://github.com/JMedina255/sistema_web_p2p/commit/3568118) | 02/11/2026 13:35 | Joan / Renzo | `merge: integrate feat/sprint-05-backend into integration/sprint-05` | Integración Local | Fusión limpia de las ramas `feat/sprint-05-frontend` y `feat/sprint-05-backend` en la rama integradora local. |
| [`370766f`](https://github.com/JMedina255/sistema_web_p2p/commit/370766f) | 02/11/2026 13:52 | Renzo Antayhua | `style(backend): format booking endpoints and test files according to ruff` | Calidad de Código | Formateo estricto conforme a reglas Ruff en endpoints y pruebas de reservas, resolviendo el job de CI. |
| [`1ed8a04`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) | 02/11/2026 14:10 | Joan / Renzo | `Merge pull request #6 from JMedina255/integration/sprint-05` | Cierre Sprint 05 | Fusión oficial del Sprint 05 en `main` tras aprobación íntegra de GitHub Actions (443 pruebas passing). |

Fuente: Historial oficial de Git del repositorio `sistema_web_p2p`.

El Cuadro 5.1 acredita la ejecución coordinada y modular del Sprint 05, demostrando que los componentes frontend y backend evolucionaron bajo commits atómicos y descriptivos que facilitan la trazabilidad retrospectiva y el análisis forense de la arquitectura.
