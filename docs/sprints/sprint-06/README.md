# Índice Maestro de Documentación y Artefactos – Sprint 06

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna – Facultad de Ingeniería – Escuela Profesional de Ingeniería de Sistemas  
**Equipo Consultor:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255)  
* Renzo Antonio Antayhua Mamani (Código: 2022073504)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Commits Oficiales de Cierre:** [`c43b455`](https://github.com/JMedina255/sistema_web_p2p/commit/c43b455) y [`1b43eea`](https://github.com/JMedina255/sistema_web_p2p/commit/1b43eea) (07/11/2026)  
**Estado:** **Sprint 06 – 100% Concluido y Homologado en CI (465 Pruebas Automatizadas: 188 Backend / 277 Frontend) – Cierre Oficial y Transición a Sprint 07**

---

## 1. Guía de Navegación de Artefactos del Sprint 06

A continuación, se detalla el índice formal de documentos, evidencias y especificaciones técnicas generadas para el Sprint 06:

### Cuadro 1.1: Inventario Canónico de Documentos del Sprint 06

| Documento / Artefacto | Ubicación en Repositorio | Tipo y Propósito Técnico |
| :--- | :--- | :--- |
| **Bitácora Maestra del Sprint 06** | [`docs/sprints/sprint-06.md`](../sprint-06.md) | Bitácora técnica exhaustiva de especificación, arquitectura, contratos REST y registro de tareas T-29 a T-37. |
| **Narrativas de Diseño Consolidadas** | [`docs/diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md`](../../diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md) | Especificación de 24 casos de uso en fase de diseño con trazabilidad de código completa (CUS-001 a CUS-024). |
| **Diagramas de Secuencia Consolidados** | [`docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md`](../../diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md) | 24 diagramas PlantUML de diseño desglosados en 7 capas técnicas más el Diagrama 6.15 de ciclo transaccional. |
| **Informe SRS de Proyecto (FD03)** | [`docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md`](../../diseño/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md) | Especificación formal del software con narrativas en 6.2.3 y diagramas de secuencia en 6.3.3. |
| **Informe SAD de Proyecto (FD04)** | [`docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md`](../../diseño/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md) | Documento de arquitectura con matriz de procesos a diagramas de secuencia en sección 7.3 (Cuadro 7.3). |
| **Plan de Sprints y Tareas Oficial** | [`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`](../PLAN_SPRINTS_Y_TAREAS.md) | Cronograma y planificación técnica vigente (Cuadro 4.6 y Tabla 5.7). |

Fuente: Elaboración propia.

---

## 2. Resumen Técnico del Incremento Sprint 6

- **Alcance Funcional Comprometido:**
  1. Evaluación automatizada de quórum a $T-24\text{ h}$ con control de ejecuciones repetidas e idempotencia (**PB-017** / **RF15** / **CUS23** / **T-29 / T-30**).
  2. Gestión resolutiva de sesiones ante quórum insuficiente por el mentor titular (**PB-018** / **RF16** / **CUS07** / **T-32 / T-33**).
  3. Pase de asistencia digital con código QR dinámico TOTP y formulario de bitácoras pedagógicas con firma digital inmutable (**PB-019** / **RF17** / **CUS12 / CUS13** / **T-34 / T-35 / T-36**).
- **Reglas de Negocio Gobernadas:**
  - **RN-04:** Ventana de antelación mínima de 24 horas para reprogramaciones contingentes ($T > 24\text{ h}$).
  - **RN-05:** Aforo máximo institucional (10 presencial / 20 virtual).
  - **RN-09:** Umbral reglamentario de quórum mínimo: 50% de cupos o al menos 3 estudiantes confirmados en presencial.
  - **RN-10:** Principio de no cancelación unilateral: el sistema nunca cancela por iniciativa propia ante quórum insuficiente; delega la decisión al mentor.
  - **RN-12:** Plazo perentorio de 48 horas post-sesión para el registro de bitácoras; observaciones sustantivas $\ge 50$ caracteres; acumulación de horas provisionales condicionadas a visado.
- **Calidad y Cobertura (RNF09):**
  - **465 pruebas automatizadas passing** con 0 fallos (188 en backend con Pytest y 277 en frontend con Vitest distribuidas en 24 suites).
  - Coberturas de código: **87.42% Backend** y **83.25% Frontend**, superando con holgura el umbral del 70.0% requerido.
- **Integración Continua (CI):**
  - Workflow de GitHub Actions (`ci.yml`) en estado verde exitoso.
