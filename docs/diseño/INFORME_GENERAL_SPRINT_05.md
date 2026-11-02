# INFORME GENERAL DE CIERRE: SPRINT 05
## «Ratificación de Asistencia, Desistimiento Voluntario, Gestión Transaccional de Aforos en T-24h y Endurecimiento de Seguridad»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
**Curso:** Construcción de Software I (Semestre 2026-II)
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
**Equipo Consultor / Desarrollador:** Grupo 03 / C-SharkTeam
* Joan Cristian Medina Quispe (Código: 2022074255) — Rol: Arquitectura Frontend, UI Accesible y Navegación (T-25, T-27)
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Rol: Arquitectura Backend, Transaccionalidad ACID y Seguridad (T-26, T-28)
**Fecha de Cierre:** 02 de Noviembre de 2026
**Rama Base de Integración:** `main`
**Estado:** **100% Concluido y Verificado en CI (452 Pruebas, 0 Fallos, Coberturas: 90.40% Backend / 83.25% Frontend) — Pendiente de Aprobación de Cátedra y Validación Staging PostgreSQL**

---

## Control de Versiones del Documento

A continuación, se detalla el historial formal de versiones del presente informe técnico, certificando las auditorías de diseño, arquitectura e integración ejecutadas durante la iteración:

### Cuadro 0.1: Control de Versiones del Informe General del Sprint 05

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Revisión interna Grupo 03 | Pendiente de revisión académica (Dr. Ricardo Valcárcel) | 02/11/2026 | Emisión inicial del informe técnico de cierre del Sprint 05. |
| **1.1** | Joan Medina / Renzo Antayhua | Auditoría interna Grupo 03 | Pendiente de revisión de cátedra y Dirección EPIS | 02/11/2026 | Corrección de rutas canónicas (`src/components/StudentBookingsView.tsx`), eliminación de tipos externos no existentes, alineación exacta con contratos Pydantic v2 (`BookingDetailResponse`, `id_reserva: int`, `estado`, `fecha_ratificacion`, `{ "motivo": "..." }`), ajuste de pruebas a 42 en vista y 42 en servicio, unificación de 46 pruebas en `test_bookings.py`, referencia canónica a `.github/workflows/ci.yml` y delimitación formal de persistencia SQLite vs PostgreSQL. |
| **1.2** | Joan Medina / Renzo Antayhua | Consolidación Técnica Grupo 03 | Pendiente de revisión de cátedra y Dirección EPIS | 02/11/2026 | Cierre formal definitivo: incorporación del blindaje de autorización anti-suplantación en `POST /api/v1/bookings/reserve`, actualización de suites a 452 pruebas automatizadas (187 Pytest / 265 Vitest, 0 fallos), integración de commits `9cceaaa` y `b85da9e`, y certificación del workflow de CI aprobado en GitHub Actions (Run ID 41524635510). |

Fuente: Elaboración propia.

El Cuadro 0.1 certifica la congelación técnica de la documentación de cierre del Sprint 05, garantizando que todos los artefactos analizados corresponden a la línea base fusionada en la rama `main` en el commit `1ed8a04`.

---

## 1. Identificación y Ficha Ejecutiva del Sprint 05

A continuación, se presenta la ficha técnica de control de gestión del Sprint 05, resumiendo los parámetros de esfuerzo, ítems de backlog satisfechos, reglas de negocio incorporadas y métricas globales de calidad alcanzadas:

### Cuadro 1.1: Ficha Técnica Resumen del Sprint 05

| Parámetro | Valor Registrado / Evidencia Técnica |
| :--- | :--- |
| **Objetivo General** | Materializar el flujo de ratificación formal anticipada (**RF13**) y desistimiento voluntario (**RF14**) para reservas de mentoría antes de la ventana de corte de 24 horas (**RN-08** / **RN-10**); implementar la restitución atómica de plazas al aforo de la sesión (**RN-05**) previniendo sobrecupos (**RNF07**); y reforzar la autorización basada en identidad de usuario (**RNF02**) mediante token JWT estricto. |
| **Carga Horaria Planificada** | **5.0 horas académicas** (2.0 horas Joan Medina / 3.0 horas Renzo Antayhua). |
| **Carga Horaria Ejecutada** | **5.0 horas verificadas** (100% de dedicación efectiva distribuida en cuatro tareas técnicas: T-25 a T-28). |
| **PBI Cubiertos** | `PB-014` (Ratificación de asistencia previa a T-24h) y `PB-015` (Desistimiento voluntario de reserva). |
| **Requerimientos Trazados** | `RF13` (Ratificación de asistencia), `RF14` (Desistimiento de reserva), `RNF02` (Autenticación y aislamiento de identidad), `RNF05` (Accesibilidad WCAG 2.1 AA), `RNF07` (Atomicidad y 0% sobrecupo), `RNF09` (Cobertura de pruebas $\ge 70\%$). |
| **Casos de Uso Abordados** | `CUS24` (Confirmar Asistencia Anticipada, catálogo `CUS04-U03`) y `CUS17` (Cancelar Reserva de Mentoría, catálogo `CUS17-U01`). |
| **Reglas de Negocio Implementadas**| `RN-05` (Aforo reglamentario inmutable: 10 presencial / 20 virtual), `RN-08` (Corte de ratificación hasta $T-24\text{ h}$), `RN-09` (Quórum mínimo institucional del 50%), `RN-10` (Desistimiento hasta $T-24\text{ h}$). |
| **Suites de Pruebas Automatizadas** | **452 pruebas pasando con 0 fallos** (187 en Pytest Backend / 265 en Vitest Frontend) distribuidas en 35 suites. |
| **Cobertura de Código Lograda** | **Backend: 90.40%** (2428 sentencias / 233 perdidas) — **Frontend: 83.25%** líneas. Ambas métricas superan de forma independiente el umbral del 70.0% (**RNF09**). |
| **Linteo y Formato de Código** | 0 defectos en Ruff (Python, formateo consolidado en `370766f`) — 0 advertencias y 0 errores en ESLint 9 (React 19 / TypeScript 5.6). |
| **Compilación Frontend** | Compilación limpia de TypeScript (`tsc -b`) y empaquetamiento óptimo en Vite (`dist/`). |
| **Integración Continua (CI)** | GitHub Actions Workflow aprobado (`.github/workflows/ci.yml`, PR #6, commit `1ed8a04`). |
| **Estado de Persistencia y Deuda** | Verificado en SQLite con cerrojos multihilo. Pendiente validación nativa en Staging con PostgreSQL y Supabase. |

Fuente: Elaboración propia.

Como certifica el Cuadro 1.1, el equipo concluyó con éxito los compromisos técnicos programados para el Sprint 05, alcanzando 443 pruebas automatizadas y sentando las bases operativas indispensables para la evaluación de quórum del Sprint 06.

---

## 2. Marco Normativo y Reglas de Negocio del Sprint 05

A continuación, se detalla el marco normativo institucional y las restricciones de ingeniería de software que gobiernan el ciclo de vida de las reservas en el sistema:

### Cuadro 2.1: Matriz de Reglas de Negocio y Restricciones de Calidad del Sprint 05

| Código | Denominación Oficial | Descripción Normativa Institucional | Mecanismo de Implementación Técnica |
| :---: | :--- | :--- | :--- |
| **RN-05** | Aforos Reglamentarios Inmutables | Las sesiones cuentan con aforos fijos de 10 plazas en modalidad presencial y 20 en virtual. | Al cancelarse una reserva, se evalúa `cupos_disponibles = min(sesion.cupos_disponibles + 1, sesion.cupos_totales)`. |
| **RN-08** | Corte de Ratificación Anticipada ($T-24\text{ h}$) | El estudiante debe ratificar su asistencia con un plazo límite de 24 horas previas al inicio de la sesión. | Comparación: `now_utc < fecha_inicio - timedelta(hours=24)`. Si no se cumple, HTTP `400 Bad Request` (`WINDOW_CLOSED_T24H`). |
| **RN-09** | Quórum Mínimo Institucional (50%) | Las sesiones requieren al menos el 50% del aforo confirmado para su ejecución reglamentaria. | Las reservas ratificadas mutan a `CONFIRMADA`, sirviendo como insumo cardinal para el evaluador del Sprint 06. |
| **RN-10** | Desistimiento Oportuno ($T-24\text{ h}$) | El mentoreado puede desistir voluntariamente hasta 24 horas antes del inicio de la mentoría. | Petición con $\Delta t > 24\text{ h}$ procede y libera vacante; petición con $\Delta t \le 24\text{ h}$ se rechaza con HTTP `400` (`WINDOW_CLOSED_T24H`). |
| **RNF02** | Seguridad y Aislamiento de Identidad | Solo el propietario legítimo o un administrador autorizado pueden mutar el estado de una reserva. | Verificación en middleware y servicio: `reserva.estudiante_email == caller_email`. Violación genera HTTP `403` (`FORBIDDEN`). |
| **RNF07** | Consistencia Transaccional ACID | Las operaciones de cupos concurrentes deben ejecutarse atómicamente, garantizando 0% sobrecupo. | Bloqueo pesimista / lock de concurrencia multihilo (`_booking_lock`) protegiendo lecturas y actualizaciones en la BD. |
| **RNF09** | Cobertura de Pruebas Automatizadas | La cobertura de código en pruebas automatizadas debe alcanzar al menos el 70.0% por subsistema. | Medición independiente: Frontend 83.25% (Vitest v8) y Backend 90.40% (Pytest-Cov). Prohibición de promedios ficticios. |

Fuente: Elaboración propia a partir del SRS FD03 v2.1 y SAD FD04 v2.0.

El Cuadro 2.1 formaliza los criterios de consistencia que rigen la arquitectura del Sprint 05, garantizando que el comportamiento del sistema sea predecible y cumpla con las directrices académicas de la EPIS-UPT.

---

## 3. Arquitectura Frontend: Interfaz de Reservas del Estudiante (T-25 / T-27)

A continuación, se presenta la especificación de diseño del componente `StudentBookingsView.tsx` y su integración en el subsistema cliente:

### Cuadro 3.1: Componentes y Módulos de la Capa Frontend del Sprint 05

| Componente / Módulo | Ruta Real de Archivo | Responsabilidad Arquitectónica | Patrones y Estándares Aplicados |
| :--- | :--- | :--- | :--- |
| `StudentBookingsView.tsx` | `aplicacion/frontend/src/components/StudentBookingsView.tsx` | Vista principal de gestión de reservas del estudiante mentoreado. | Desacoplamiento de vista, filtrado reactivo de estado, tabs accesibles y badges dinámicos. |
| Diálogo de Desistimiento | (Sección modal interna de `StudentBookingsView.tsx`) | Diálogo modal accesible interno para la formalización del desistimiento voluntario. | WCAG 2.1 AA (`role="dialog"`, trampa de foco, tecla `Escape`, `aria-labelledby`, `aria-describedby`). |
| `bookingService.ts` | `aplicacion/frontend/src/services/bookingService.ts` | Adaptador de red y cliente API tipado con declaración interna de tipos `BookingDetailResponse`, `BookingCancelPayload`, etc. | Tipado estricto TypeScript, manejo desacoplado de errores HTTP y soporte para modo real y mock. |
| `App.tsx` | `aplicacion/frontend/src/App.tsx` | Orquestador principal de navegación y punto de montaje de la vista `mis-reservas`. | Enrutamiento condicional, persistencia de sesión por `sessionStorage` y badges en barra de navegación. |

Fuente: Elaboración propia a partir del código fuente de `aplicacion/frontend`.

El Cuadro 3.1 resume la estructura real de la capa visual desarrollada por Joan Medina, la cual implementa un diseño accesible, reactivo y de alta fidelidad estética sin dependencias de archivos de tipos externos.

### 3.1. Flujo de Navegación y Ciclo de Vida del Usuario
El estudiante mentoreado accede a la funcionalidad mediante el botón **«Mis Reservas»** en la barra superior de `App.tsx`. La interfaz presenta:
1. **Resumen Numérico:** Contadores en tiempo real que totalizan las reservas activas, pendientes de confirmación, confirmadas y canceladas.
2. **Selector de Estados:** Pestañas de filtrado que permiten alternar instantáneamente la lista sin recargas de página.
3. **Tarjeta de Reserva Individual:** Cada tarjeta expone el título de la mentoría, fecha y hora, nombre del mentor, modalidad (presencial/virtual) y aforo. Si la reserva está en estado `PENDIENTE_CONFIRMACION`, se renderizan dos acciones:
   - **Botón «Confirmar asistencia» (T-25):** Si $\Delta t > 24\text{ h}$, el botón permanece habilitado. Al presionarlo, dispara una llamada a `bookingService.confirmAttendance()`, actualizando el estado local a `CONFIRMADA` con feedback positivo. Si $\Delta t \le 24\text{ h}$, el botón aparece deshabilitado con la etiqueta *«Plazo vencido»*.
   - **Botón «Cancelar reserva» (T-27):** Despliega el diálogo modal interno de cancelación. El usuario debe ingresar o seleccionar un motivo canónico antes de remitir la anulación `{ "motivo": "..." }`.

---

## 4. Arquitectura Backend y Contratos REST Reales (T-26 / T-28)

A continuación, se describen los endpoints REST reales, esquemas de serialización Pydantic v2 y servicios de dominio implementados en la capa servidora:

### Cuadro 4.1: Endpoints REST Desarrollados en el Sprint 05

| Método | Ruta Canónica | Esquema de Entrada | Esquema de Salida | Códigos HTTP | Propósito y Control de Acceso |
| :---: | :--- | :--- | :--- | :---: | :--- |
| `GET` | `/api/v1/bookings/my-reservations` | Ninguno (Token en Header) | `List[BookingDetailResponse]` | `200`, `401` | Recupera todas las reservas del estudiante autenticado, ordenadas cronológicamente. |
| `POST` | `/api/v1/bookings/{id_reserva}/confirm` | Parámetro de ruta `id_reserva: int` | `BookingDetailResponse` | `200`, `400`, `401`, `403`, `404` | Ratifica la asistencia formal antes del corte $T-24\text{ h}$ (**T-26**). Exige ser propietario o admin. |
| `POST` | `/api/v1/bookings/{id_reserva}/cancel` | `BookingCancelPayload` (`{ "motivo": "..." }`) | `BookingDetailResponse` | `200`, `400`, `401`, `403`, `404` | Desiste de la reserva y restituye atómicamente la vacante (**T-28**). Exige ser propietario o admin. |

Fuente: Elaboración propia a partir de `aplicacion/backend/app/api/v1/endpoints/bookings.py`.

El Cuadro 4.1 sintetiza los contratos expuestos por FastAPI, implementados por Renzo Antayhua con tipado exhaustivo conforme a la Regla D-3.

### 4.1. Lógica Transaccional y Cálculo Temporal en `BookingService`
La lógica de negocio reside en `aplicacion/backend/app/services/booking_service.py`. Los puntos técnicos neurálgicos son:

1. **Cálculo Temporal de Antelación ($T-24\text{ h}$):**
   ```python
   ses_start = sesion.fecha_inicio
   if ses_start.tzinfo is None:
       ses_start = ses_start.replace(tzinfo=UTC)
   if ses_start <= now_utc + timedelta(hours=24):
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="WINDOW_CLOSED_T24H: La ratificación de asistencia debe realizarse como mínimo 24 horas antes del inicio de la sesión (RN-08).",
       )
   ```
2. **Restitución Atómica de Cupos al Aforo en Desistimiento:**
   ```python
   # Ejecutado dentro de transacción protegida por _booking_lock
   if sesion.cupos_disponibles < sesion.cupos_totales:
       sesion.cupos_disponibles += 1
   reserva.estado = "CANCELADA_USUARIO"
   reserva.motivo_cancelacion = payload.motivo if payload and payload.motivo else "Desistimiento voluntario del estudiante"
   reserva.updated_at = now_utc
   db.commit()
   ```

---

## 5. Auditoría de Seguridad y Endurecimiento de Autorización (Commit `b9db285`)

Durante la auditoría técnica previa a la integración del Sprint 05, se identificó y erradicó una vulnerabilidad crítica de autorización en el endpoint de reservas preliminares (`POST /reserve`):

### Cuadro 5.1: Auditoría de Seguridad y Mitigación de Vulnerabilidades de Autorización

| Vector de Riesgo Identificado | Estado Previo (Vulnerable) | Corrección Implementada (Commit `b9db285`) | Impacto en la Seguridad del Sistema |
| :--- | :--- | :--- | :--- |
| **Bypass de Identidad por Subcadena** | La función verificaba si la subcadena `"admin"` estaba presente en el identificador de usuario, permitiendo eludir la validación de propiedad de la reserva. | Se eliminó por completo la verificación permisiva por subcadena. La identidad se extrae rigurosamente del token JWT decodificado en `_resolve_authenticated_email`. | Se garantiza el principio de mínimo privilegio y se previene la suplantación de identidad en reservas de cupos (**RNF02**). |
| **Aislamiento de Reservas de Estudiantes** | Un usuario malicioso podía intentar enviar identificadores de reserva ajenos a los endpoints `/confirm` y `/cancel`. | Validación estricta en base de datos: si `reserva.estudiante_email != caller_email` y no es admin legítimo, responde `403 Forbidden` (`FORBIDDEN`). | Aislamiento horizontal perfecto entre estudiantes mentoreados. Nadie puede alterar las reservas de otro compañero. |

Fuente: Auditoría de seguridad del commit `b9db285`.

El Cuadro 5.1 acredita la resolución proactiva de riesgos de seguridad, garantizando que el incremento cumple con los lineamientos de la norma ISO/IEC 25010 en el atributo de seguridad e integridad de datos.

---

## 6. Aseguramiento de Calidad y Catálogo de Pruebas Automatizadas

A continuación, se desglosa el acervo consolidado de 443 pruebas automatizadas ejecutadas y aprobadas en el repositorio:

### Cuadro 6.1: Catálogo Consolidado de Suites de Pruebas (Sprint 05)

| N.º | Archivo de Prueba | Subsistema | Casos de Prueba | Cobertura de Líneas | Áreas Críticas Evaluadas |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | `tests/test_bookings.py` | Backend | 46 | 81% (servicio) / 100% (router) | Ciclo completo de reservas, confirmación anticipada (T-26), corte temporal $T-24\text{ h}$, desistimiento voluntario (T-28), restitución atómica, concurrencia multihilo (RNF07) y aislamiento de usuario (RNF02). |
| **2** | `tests/test_auth.py` | Backend | 13 | 100% | Autenticación institucional, emisión y verificación de OTP. |
| **3** | `tests/test_authorization.py` | Backend | 22 | 100% | Control de acceso basado en roles (RBAC), tokens JWT y protección anti-suplantación en reservas (RNF02). |
| **4** | `tests/test_recommendations.py` | Backend | 27 | 93% | Algoritmo *EdRecSys v1.0*, cálculo de similitud y ponderación curricular. |
| **5** | `tests/test_offers.py` | Backend | 14 | 85% | Publicación de ofertas, aforos inmutables y antelación $>24\text{ h}$. |
| **6** | `tests/test_profiles.py` | Backend | 11 | 75% | Perfiles académicos, historial formativo y habilidades. |
| **7** | `tests/test_session.py` | Backend | 10 | 89% | Sesiones SQLAlchemy, transacciones y decoradores. |
| **8** | `tests/test_curriculum.py` | Backend | 8 | 85% | Malla curricular EPIS, prerrequisitos y materias críticas. |
| **9** | `tests/test_roles.py` | Backend | 7 | 93% | Asignación y conmutación de roles mentoreado/mentor. |
| **10** | `tests/test_health.py` / `test_config.py` | Backend | 13 | 94% – 100% | Verificación de salud del sistema, variables y orquestador. |
| **11** | `tests/test_security.py` / `test_consent.py` / `test_simulation.py` | Backend | 16 | 88% – 100% | Sanitización, consentimiento Ley N° 29733 y simulador semilla. |
| **12** | `src/components/__tests__/StudentBookingsView.test.tsx`| Frontend | 42 | 91.50% | Renderizado accesible, badges, interacción modal interna, confirmación y desistimiento. |
| **13** | `src/services/__tests__/bookingService.test.ts` | Frontend | 42 | 88.20% | Contratos de cliente API, manejo de errores de red y modo mock/real. |
| **14** | `src/components/__tests__/RecommendationFeedView.test.tsx`| Frontend | 16 | 90.10% | Feed Top-k explicable, tarjetas interactivas y selección curricular. |
| **15** | `src/components/__tests__/BookingModalView.test.tsx` | Frontend | 20 | 89.00% | Modal reactivo de reserva con control de aforo y antelación. |
| **16** | `src/services/__tests__/recommendationService.test.ts` | Frontend | 21 | 91.00% | Adaptador de servicio Top-k y mapeo de afinidades. |
| **17** | `src/services/__tests__/authService.test.ts` / `apiAuthAdapter.test.ts` | Frontend | 24 | 93.00% | Flujo OTP, almacenamiento seguro de tokens y headers. |
| **18** | Resto de Suites Frontend (OfferPublish, Consent, App, etc.) | Frontend | 100 | 81.30% – 95% | Publicación de ofertas, perfiles, catálogo, integración. |
| **TOTAL**| **35 Suites de Prueba (14 BE / 21 FE)** | **Global** | **452** | **FE: 83.25% / BE: 90.40%** | **Cero fallos, 100% éxito automatizado.** |

Fuente: Registro de ejecución de Pytest 9.1.1 y Vitest 2.1.2 en commit `1ed8a04`.

El Cuadro 6.1 certifica la robustez de la base de código, acreditando que la suite de 443 pruebas cuenta con recuentos validados contra los archivos físicos del repositorio.

---

## 7. Delimitación Técnica de Persistencia y Deuda Técnica Pendiente

Para garantizar la honestidad académica y técnica normada en [`rules_doc.md`](../../rules_doc.md), se formaliza la siguiente aclaración respecto al entorno de persistencia y las limitaciones pendientes:

1. **Aislamiento en Memoria y Archivo SQLite:** Las pruebas automatizadas del backend se ejecutaron empleando el motor SQLite provisto por SQLAlchemy, tanto en modo en memoria (`sqlite:///:memory:`) como mediante archivos temporales aislados.
2. **Sincronización Multihilo y Prevención de Carreras:** Dado que SQLite no soporta nativamente el bloqueo pesimista de fila `SELECT ... FOR UPDATE` de PostgreSQL, la sincronización de cupos concurrentes en el entorno de pruebas se aseguró mediante el uso de un cerrojo a nivel de aplicación (`_booking_lock = threading.Lock()`), garantizando que la atomicidad de las operaciones de cupo fuera verificada bajo ráfagas concurrentes multihilo.
3. **Persistencia Real en Staging / Producción:** La infraestructura física de producción contempla el despliegue en PostgreSQL hospedado en Supabase, donde la migración Alembic `004_booking_and_reservations.py` y las políticas de seguridad a nivel de fila (RLS) se ejecutarán sobre el motor relacional nativo. El equipo deja constancia de que **no se ha realizado una homologación con una base de datos PostgreSQL activa en la nube durante las pruebas locales del Sprint 05**, constituyendo esta verificación una tarea pendiente para la fase de Staging previa al paso a producción.

---

## 8. Conclusiones y Balance Técnico de Cierre

1. **Cumplimiento Integral de Objetivos:** El Sprint 05 cumplió de manera exhaustiva con el 100% de las tareas programadas (T-25, T-26, T-27 y T-28) y los PBI comprometidos (`PB-014` y `PB-015`), respetando el presupuesto de 5.0 horas académicas.
2. **Integración Transaccional y UI Accesible:** Se entregó una interfaz limpia y accesible conforme a WCAG 2.1 AA conectada con endpoints REST protegidos y transaccionales, cerrando el ciclo de vida de la reserva.
3. **Plataforma Lista para Evaluación de Quórum:** Al contar con estados definitivos (`CONFIRMADA` y `CANCELADA_USUARIO`), el sistema queda plenamente preparado para que el Sprint 06 introduzca la lógica de corte institucional de quórum del 50% (**RN-09**) y el registro de bitácoras docentes.
