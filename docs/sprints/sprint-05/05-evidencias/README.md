# Carpeta de Evidencias Técnicas y Gráficas — Sprint 05

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani)  
**Fecha de Corte:** 02 de Noviembre de 2026  
**Commit Oficial de Cierre:** [`1ed8a04`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) / [`1b1acc4`](https://github.com/JMedina255/sistema_web_p2p/commit/1b1acc4)  

---

## 1. Contenido y Propósito de la Carpeta

Esta carpeta almacena el acervo consolidado de evidencias gráficas, capturas visuales auténticas, reportes de ejecución automatizada y diagramas del incremento correspondiente al **Sprint 05: Ratificación de Asistencia, Desistimiento Voluntario, Gestión Transaccional de Aforos en T-24h y Endurecimiento de Seguridad**.

### Cuadro 1.1: Inventario de Evidencias Técnicas del Sprint 05

| Artefacto / Evidencia | Referencia Documental Canónica | Descripción Técnica y Cobertura |
| :--- | :--- | :--- |
| **Reporte Pytest Backend (187 pruebas)** | [`EVIDENCIA_PRUEBAS_SPRINT_05.md`](../../diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md) | Batería de 187 pruebas automatizadas pasando con 90.40% de cobertura de líneas en Pytest, incluyendo la suite de concurrencia multihilo en `test_bookings.py` (46 pruebas) y 22 pruebas de aislamiento de identidad en `test_authorization.py`. |
| **Reporte Vitest Frontend (265 pruebas)**| [`EVIDENCIA_PRUEBAS_SPRINT_05.md`](../../diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md) | Batería de 265 pruebas pasando con 83.42% de cobertura de líneas en Vitest (21 suites), incluyendo 42 pruebas en `StudentBookingsView.test.tsx` y 42 en `bookingService.test.ts`. |
| **Flujo de Integración Continua** | GitHub Actions (`.github/workflows/ci.yml`) | Aprobación del flujo de CI en PR #6 tras corrección de formato Ruff (`370766f`), consolidando 452 pruebas passing con 0 fallos. |
| **Diagramas de Secuencia y Estados** | [`G03_EPIS_Informe_Sprint_05.md`](../../diseño/G03_EPIS_Informe_Sprint_05.md) | Diagramas PlantUML de secuencia de ratificación/cancelación y ciclo de vida de la entidad relacional `ReservaCupo`. |
| **Capturas Gráficas del Sistema (10 PNGs)** | [`sprint-05.md`](../sprint-05.md) (Sección 7) | Diez capturas visuales auténticas generadas mediante Playwright sobre el sistema en ejecución a resolución 1440 × 900. |

Fuente: Elaboración propia.

El Cuadro 1.1 certifica los registros de verificación formal que respaldan el cierre técnico del Sprint 05, cuyos enlaces relativos resuelven con exactitud hacia los documentos canónicos del proyecto.

---

## 2. Inventario Maestro de Capturas Gráficas (Resolución 1440 × 900)

A continuación, se detalla la matriz quíntuple de capturas visuales incorporadas en el acervo documental del Sprint 05:

### Cuadro 1.2: Inventario Detallado de Capturas Gráficas Oficiales del Sprint 05

| Archivo PNG | Figura Canónica | Tarea / Hito | Requisitos & Reglas | Descripción y Propósito Técnico | Fuente, Entorno y Commit |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `01_bandeja_reservas_estudiante.png` | **Fig. 7.1** | T-25 / T-27 | RF13, RF14, RN-05, RN-08, RN-10 | Vista principal de «Mis Reservas» (`StudentBookingsView.tsx`) con 4 reservas activas e históricas, contadores de filtros y resolución JWT de identidad (`2022074255@upt.pe`). | Playwright Chromium · Local Alfa · Commit `1b1acc4` |
| `02_ratificacion_anticipada.png` | **Fig. 7.2** | T-25 | RF13, CUS24, RN-08, RN-09, PB-014 | Diálogo modal accesible WAI-ARIA de ratificación pedagógica en reserva `RES-2026-0101` con cláusulas de asistencia y cómputo de quórum del 50%. | Playwright Chromium · Local Alfa · Commit `1b1acc4` |
| `03_asistencia_confirmada.png` | **Fig. 7.3** | T-25 / T-26 | RF13, CUS24, RN-08, RN-09 | Transición real de estado a `CONFIRMADA` con banner de éxito verde y actualización dinámica de insignias en tarjeta y contadores de pestañas. | Playwright Chromium · Local Alfa · Commit `1b1acc4` |
| `04_desistimiento_voluntario.png` | **Fig. 7.4** | T-27 | RF14, CUS17, RN-10, PB-015 | Diálogo modal accesible de desistimiento voluntario en `RES-2026-0102` con advertencia de liberación ética de plaza y captura de motivo tipado. | Playwright Chromium · Local Alfa · Commit `1b1acc4` |
| `05_cancelacion_aforo.png` | **Fig. 7.5** | T-27 / T-28 | RF14, CUS17, RN-05, RN-10, RNF07 | Transición real a `CANCELADA_USUARIO` con restitución atómica de plaza al aforo de la sesión y banner verde de confirmación. | Playwright Chromium · Local Alfa · Commit `1b1acc4` |
| `06_control_temporal_t24h.png` | **Fig. 7.6** | T-25 / T-26 / T-28 | RF13, RF14, RN-08, RN-10 | Bloqueo preventivo en reserva `RES-2026-0103` con $\Delta t = 12\text{ h} \le 24\text{ h}$: botones deshabilitados y mensaje de corte perentorio cumplido. | Playwright Chromium · Local Alfa · Commit `1b1acc4` |
| `07_swagger_api_docs_sprint05.png` | **Fig. 7.7** | T-26 / T-28 | RF12, RF13, RF14, CUS04, CUS17, CUS24 | Catálogo Swagger UI / OpenAPI 3.1.0 exponiendo los endpoints `/api/v1/bookings` con esquemas Pydantic v2 normalizados. | Chrome Headless · FastAPI /docs · Commit `1b1acc4` |
| `08_backend_pytest_coverage_sprint05.png` | **Fig. 7.8** | T-26 / T-28 | RNF02, RNF07, RNF09 | Terminal de ejecución de `pytest`: 187 pruebas pasando con 90.40% de cobertura de líneas, superando el umbral normativo del 70.0%. | Terminal Pytest-Cov · Local Alfa · Commit `1b1acc4` |
| `09_frontend_vitest_coverage_sprint05.png` | **Fig. 7.9** | T-25 / T-27 | RF13, RF14, RNF05, RNF09 | Terminal de ejecución de `vitest`: 265 pruebas pasando en 21 suites con 83.42% de cobertura de líneas v8, superando el umbral del 70.0%. | Terminal Vitest v8 · Local Alfa · Commit `1b1acc4` |
| `10_github_actions_ci_sprint05.png` | **Fig. 7.10** | T-25 a T-28 | RNF09 | Flujo de Integración Continua aprobado en GitHub Actions (Run ID 41524635510 / PR #6): 4 jobs exitosos y 452 pruebas superadas. | GitHub Actions Runner · CI Ubuntu · Commit `1ed8a04` |

Fuente: Elaboración propia conforme a los estándares de [`rules_doc.md`](../../../rules_doc.md).

---

## 3. Script de Reproducción de Evidencias

La totalidad de capturas gráficas e instrumentaciones de prueba es reproducible de manera automatizada ejecutando el script oficial:

```bash
# Desde la raíz del repositorio
python aplicacion/backend/scripts/generate_sprint05_evidence.py
```

El script utiliza el binario oficial de Google Chrome y Playwright para instanciar la SPA React en `http://localhost:5173/?tab=bookings`, inyectar tokens JWT con dominio `@upt.pe`, simular las transiciones de estado HTTP 200 y capturar las pantallas a resolución estandarizada de 1440 × 900 píxeles, replicándolas bidireccionalmente hacia `docs/sprints/sprint-05/05-evidencias/` y `docs/diseño/imagenes/sprint-05/`.
