# Bitácora de Especificación Técnica, Desarrollo y Cierre — Sprint 05: Ratificación de Asistencia, Desistimiento Voluntario y Gestión Transaccional de Aforos en T-24h

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
**Curso:** Construcción de Software I (Semestre Académico 2026-II)
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
**Equipo Consultor:** Grupo 03 / C-SharkTeam
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend, UI Accesible y Navegación
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Persistencia ORM y Concurrencia Transaccional
**Rama Base de Integración:** `main`
**Commit Oficial de Cierre:** [`1ed8a046e0b214082042a3172b12d2c98b3d0b90`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) (02/11/2026)
**Estado:** **100% Concluido y Verificado en CI (443 Pruebas Automatizadas) — Pendiente de Revisión y Aprobación de Cátedra**

---

## 1. Visión General y Alcance del Sprint 05

El **Sprint 05** consolida la gestión operativa posterior a la reserva preliminar de cupos de mentoría, formalizando dos flujos normativos fundamentales de la plataforma P2P de la EPIS-UPT:
1. **Ratificación Formal de Asistencia (**PB-014** / **RF13** / **CUS24** / catálogo `CUS04-U03`):** Permite a los estudiantes mentoreados consultar sus inscripciones vigentes y ratificar formalmente su asistencia antes de la ventana de corte de 24 horas previas al inicio de la sesión (**RN-08**). Las reservas ratificadas mutan a estado `CONFIRMADA`, registran `fecha_ratificacion` y constituyen el insumo cardinal para la evaluación de quórum mínimo institucional del 50% (**RN-09**) que se ejecutará en el Sprint 06.
2. **Desistimiento Voluntario de Reserva (**PB-015** / **RF14** / **CUS17** / catálogo `CUS17-U01`):** Permite a los estudiantes anular oportunamente su plaza provisional antes del corte de 24 horas (**RN-10**), justificando el motivo en un diálogo modal interno accesible (WCAG 2.1 AA). La anulación muta la reserva a `CANCELADA_USUARIO` y restituye de forma atómica la vacante al aforo de la sesión (**RN-05**), garantizando una tasa de sobrecupo de exactamente $0.0\%$ (**RNF07**).

A continuación, se detalla la matriz de actividades, responsables, esfuerzo planificado y alcance técnico del Sprint 05 de conformidad con [`PLAN_SPRINTS_Y_TAREAS.md`](PLAN_SPRINTS_Y_TAREAS.md):

### Cuadro 1.1: Matriz de Tareas y Planificación Técnica del Sprint 05

| ID | Actividad Oficial | Responsable | Esfuerzo Planificado (h) | Estado de Entrega | Entregable y Criterio Verificable |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **T-25** | Implementar interfaz de confirmación de asistencia. | Joan Medina | 1.0 h | **100% Concluido** | Componente `src/components/StudentBookingsView.tsx`, botón de ratificación, cálculo temporal de corte $T-24\text{ h}$ y 42 pruebas en Vitest. |
| **T-26** | Desarrollar API de ratificación con control temporal. | Renzo Antayhua | 2.0 h | **100% Concluido** | Router `/api/v1/bookings/{id_reserva}/confirm`, validación de ventana $>24\text{ h}$, transición a `CONFIRMADA`, retorno `BookingDetailResponse` y suite en Pytest. |
| **T-27** | Implementar opción de desistimiento en la interfaz. | Joan Medina | 1.0 h | **100% Concluido** | Diálogo modal interno accesible de desistimiento, selector de motivos `{ "motivo": "..." }`, mutación a `CANCELADA_USUARIO` y suite integrada en Vitest. |
| **T-28** | Desarrollar anulación y liberación atómica de cupos. | Renzo Antayhua | 1.0 h | **100% Concluido** | Router `/api/v1/bookings/{id_reserva}/cancel`, restitución atómica de `cupos_disponibles` con cerrojo de concurrencia y suite multihilo en `test_bookings.py`. |

Fuente: Elaboración propia a partir del plan maestro [`PLAN_SPRINTS_Y_TAREAS.md`](PLAN_SPRINTS_Y_TAREAS.md), apartado 4.5.

El Cuadro 1.1 demuestra que las 5.0 horas académicas presupuestadas fueron cumplidas íntegramente, concluyendo las cuatro tareas comprometidas.

---

## 2. Historial de Commits y Registro Cronológico de Integración

A continuación, se presenta la secuencia oficial de commits que conforman el incremento del Sprint 05 en el repositorio:

### Cuadro 2.1: Historial de Commits del Sprint 05

| Commit SHA | Fecha y Hora (UTC-5) | Autor | Mensaje Canónico del Commit | Tarea / Hito |
| :---: | :---: | :---: | :--- | :---: |
| [`0a1f1f7`](https://github.com/JMedina255/sistema_web_p2p/commit/0a1f1f7) | 02/11/2026 09:15 | Joan Medina | `fix(frontend): enforce secure service mode resolution and remove hardcoded student identity fallback (audit B.1/B.2)` | Auditoría S5 |
| [`017f65a`](https://github.com/JMedina255/sistema_web_p2p/commit/017f65a) | 02/11/2026 10:04 | Joan Medina | `feat(frontend): prepare attendance confirmation and withdrawal service contracts (S5)` | Contratos S5 |
| [`3047afb`](https://github.com/JMedina255/sistema_web_p2p/commit/3047afb) | 02/11/2026 10:48 | Joan Medina | `feat(frontend): implement attendance confirmation interface (T-25)` | **T-25** |
| [`fb7c051`](https://github.com/JMedina255/sistema_web_p2p/commit/fb7c051) | 02/11/2026 11:22 | Joan Medina | `feat(frontend): implement voluntary booking withdrawal interface (T-27)` | **T-27** |
| [`00fc4c3`](https://github.com/JMedina255/sistema_web_p2p/commit/00fc4c3) | 02/11/2026 11:50 | Joan Medina | `feat(frontend): integrate student bookings navigation and lifecycle workflows (S5)` | Integración FE |
| [`b9db285`](https://github.com/JMedina255/sistema_web_p2p/commit/b9db285) | 02/11/2026 12:10 | Renzo Antayhua | `fix(backend): enforce authenticated booking ownership and authorization` | Seguridad BE |
| [`d13c0ab`](https://github.com/JMedina255/sistema_web_p2p/commit/d13c0ab) | 02/11/2026 12:45 | Renzo Antayhua | `feat(backend): implement attendance confirmation endpoint (T-26)` | **T-26** |
| [`dd7e3cc`](https://github.com/JMedina255/sistema_web_p2p/commit/dd7e3cc) | 02/11/2026 13:18 | Renzo Antayhua | `feat(backend): implement atomic booking cancellation and seat release (T-28)` | **T-28** |
| [`3568118`](https://github.com/JMedina255/sistema_web_p2p/commit/3568118) | 02/11/2026 13:35 | Joan / Renzo | `merge: integrate feat/sprint-05-backend into integration/sprint-05` | Integración Local |
| [`370766f`](https://github.com/JMedina255/sistema_web_p2p/commit/370766f) | 02/11/2026 13:52 | Renzo Antayhua | `style(backend): format booking endpoints and test files according to ruff` | Calidad de Código |
| [`1ed8a04`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) | 02/11/2026 14:10 | Joan / Renzo | `Merge pull request #6 from JMedina255/integration/sprint-05` | Cierre Sprint 05 |

Fuente: Registro Git del repositorio oficial.

El Cuadro 2.1 documenta la secuencia atómica de construcción del Sprint 05, garantizando la trazabilidad histórica de cada componente y corrección de software.

---

## 3. Métricas de Calidad y Verificación Automatizada

A continuación, se certifican las métricas de aseguramiento de la calidad alcanzadas al cierre de la iteración:

### Cuadro 3.1: Resumen de Calidad y Cobertura Independiente (Sprint 05)

| Métrica / Criterio | Frontend (React / Vitest) | Backend (FastAPI / Pytest) | Meta Normativa RNF09 | Estado de Cumplimiento |
| :--- | :---: | :---: | :---: | :---: |
| **Pruebas Automatizadas** | **265 aprobadas (0 fallos)** | **178 aprobadas (0 fallos)** | 100% de éxito | **Cumplido (443 totales)** |
| **Cobertura de Líneas** | **83.25%** | **90.40%** | $\ge 70.0\%$ | **Superado con holgura** |
| **Linteo de Código** | ESLint 9 (0 errores / 0 adv.) | Ruff 0.8.0 (0 defectos) | 0 errores | **Cumplido** |
| **Compilación Tipada** | TypeScript (`tsc -b`, 0 err) | Pydantic v2 (tipado estricto)| 100% estricto | **Cumplido** |
| **Tasa de Sobrecupo (RNF07)**| N/A | **0.00%** (20 hilos concurrentes) | Exactamente 0.0% | **Cumplido** |
| **Integración Continua** | GitHub Actions (`ci.yml`) | GitHub Actions (`ci.yml`) | Workflow verde | **Cumplido** |
| **Persistencia en Pruebas** | Mocks y jsdom | SQLite (cerrojo multihilo) | Pendiente PostgreSQL | **Delimitado** |

Fuente: Reportes de ejecución de Vitest, Pytest y GitHub Actions en commit `1ed8a04`.

El Cuadro 3.1 certifica que el software satisface los requerimientos no funcionales de calidad y mantenibilidad, manteniendo ambas suites libres de advertencias o errores.

---

## 4. Documentos Maestros Relacionados

Para un análisis detallado, consulte los siguientes documentos técnicos elaborados en esta entrega:
- [Informe Académico Canónico (G03)](../diseño/G03_EPIS_Informe_Sprint_05.md) — Informe institucional formal de 11 secciones.
- [Informe General Técnico de Cierre](../diseño/INFORME_GENERAL_SPRINT_05.md) — Memoria técnica exhaustiva de diseño, contratos REST y seguridad.
- [Catálogo de Evidencia de Pruebas](../diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md) — Inventario de 443 pruebas y comandos de reproducción.
- [Mapa Maestro de Trazabilidad](sprint-05/02-trazabilidad/MAPA_FUENTES_SPRINT_05.md) — Matriz de trazabilidad bidireccional completa.
- [Propuesta de Diapositivas Canva](sprint-05/04-presentacion/PROPUESTA_DIAPOSITIVAS_CANVA.md) — Guion estructurado de 14 diapositivas para sustentación.
