# Carpeta de Evidencias Técnicas y Gráficas — Sprint 05

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
**Curso:** Construcción de Software I (2026-II)
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani)

---

## 1. Contenido de la Carpeta

Esta carpeta almacena el acervo de evidencias técnicas, reportes de ejecución automatizada y diagramas del incremento correspondiente al **Sprint 05: Ratificación de Asistencia, Desistimiento Voluntario y Gestión Transaccional de Aforos en T-24h**.

### Cuadro 1.1: Inventario de Evidencias Técnicas del Sprint 05

| Artefacto / Evidencia | Referencia Documental Canónica | Descripción Técnica |
| :--- | :--- | :--- |
| **Reporte Pytest Backend (178 pruebas)** | [`EVIDENCIA_PRUEBAS_SPRINT_05.md`](../../../diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md) | Batería de 178 pruebas pasando con 90.40% de cobertura de líneas en Pytest, incluyendo la suite integrada de concurrencia multihilo en `test_bookings.py` (46 pruebas). |
| **Reporte Vitest Frontend (265 pruebas)**| [`EVIDENCIA_PRUEBAS_SPRINT_05.md`](../../../diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md) | Batería de 265 pruebas pasando con 83.25% de cobertura de líneas en Vitest, incluyendo 42 pruebas en `StudentBookingsView.test.tsx` y 42 en `bookingService.test.ts`. |
| **Flujo de Integración Continua** | GitHub Actions (`.github/workflows/ci.yml`) | Aprobación del flujo de CI en PR #6 tras corrección de formato Ruff (`370766f`). |
| **Diagramas de Secuencia y Estados** | [`G03_EPIS_Informe_Sprint_05.md`](../../../diseño/G03_EPIS_Informe_Sprint_05.md) | Diagramas PlantUML de secuencia de ratificación/cancelación y ciclo de vida de la reserva. |

Fuente: Elaboración propia.

El Cuadro 1.1 certifica los registros de verificación formal que respaldan el cierre técnico del Sprint 05, cuyos enlaces relativos resuelven con exactitud hacia la carpeta `docs/diseño/`.
