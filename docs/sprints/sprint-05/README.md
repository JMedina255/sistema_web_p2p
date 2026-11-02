# Índice Maestro de Documentación y Artefactos — Sprint 05

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo Consultor:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255)  
* Renzo Antonio Antayhua Mamani (Código: 2022073504)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Commit Oficial de Cierre:** [`1ed8a046e0b214082042a3172b12d2c98b3d0b90`](https://github.com/JMedina255/sistema_web_p2p/commit/1ed8a04) (02/11/2026)  
**Estado:** **Sprint 05 — 100% Concluido y Homologado en CI (443 Pruebas Automatizadas)**

---

## 1. Guía de Navegación de Artefactos del Sprint 05

A continuación, se detalla el índice formal de documentos, evidencias y especificaciones técnicas generadas para el Sprint 05:

### Cuadro 1.1: Inventario Canónico de Documentos del Sprint 05

| Documento / Artefacto | Ubicación en Repositorio | Tipo y Propósito Técnico |
| :--- | :--- | :--- |
| **Informe Académico Canónico (G03)** | [`docs/diseño/G03_EPIS_Informe_Sprint_05.md`](../../diseño/G03_EPIS_Informe_Sprint_05.md) | Informe formal de 11 secciones normado por [`rules_doc.md`](../../../rules_doc.md) para la cátedra de Construcción de Software I. |
| **Informe General Técnico de Cierre** | [`docs/diseño/INFORME_GENERAL_SPRINT_05.md`](../../diseño/INFORME_GENERAL_SPRINT_05.md) | Memoria técnica exhaustiva de arquitectura, contratos REST tipados, seguridad JWT y concurrencia transaccional. |
| **Catálogo de Evidencia de Pruebas** | [`docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md`](../../diseño/EVIDENCIA_PRUEBAS_SPRINT_05.md) | Reporte de 443 pruebas automatizadas (265 FE / 178 BE), métricas de cobertura independiente y comandos de reproducción. |
| **Mapa Maestro de Trazabilidad** | [`docs/sprints/sprint-05/02-trazabilidad/MAPA_FUENTES_SPRINT_05.md`](02-trazabilidad/MAPA_FUENTES_SPRINT_05.md) | Matriz biunívoca vertical: PBI $\leftrightarrow$ RF $\leftrightarrow$ CUS $\leftrightarrow$ RN $\leftrightarrow$ Tarea $\leftrightarrow$ Código $\leftrightarrow$ Pruebas $\leftrightarrow$ Commits. |
| **Propuesta de Diapositivas Canva** | [`docs/sprints/sprint-05/04-presentacion/PROPUESTA_DIAPOSITIVAS_CANVA.md`](04-presentacion/PROPUESTA_DIAPOSITIVAS_CANVA.md) | Guion maestro pedagógico de 14 diapositivas para sustentación académica y sincronización visual en Canva. |
| **Bitácora de Planificación S05** | [`docs/sprints/sprint-05.md`](../sprint-05.md) | Bitácora técnica y registro de tareas ejecutadas del Sprint 05. |
| **Carpeta de Evidencias y Capturas** | [`docs/sprints/sprint-05/05-evidencias/`](05-evidencias/) | Repositorio de evidencias gráficas y de ejecución de pruebas del sprint. |

Fuente: Elaboración propia.

El Cuadro 1.1 centraliza el acceso a los artefactos oficiales del Sprint 05, garantizando que docentes, evaluadores y desarrolladores dispongan de una referencia rápida y auditable.

---

## 2. Resumen Técnico del Incremento

- **Alcance Funcional Comprometido:** Ratificación de asistencia formal (**PB-014** / **RF13** / **CUS24**) y desistimiento voluntario con restitución de aforo (**PB-015** / **RF14** / **CUS17**).
- **Reglas de Negocio Gobernadas:** Aforos inmutables (**RN-05**), corte a 24 horas previas (**RN-08** y **RN-10**) y preparación del quórum mínimo del 50% (**RN-09**).
- **Seguridad Reforzada (RNF02):** Eliminación de bypass permisivo `"admin"` en commit `b9db285`, garantizando aislamiento de identidad por token JWT.
- **Concurrencia ACID (RNF07):** Restitución atómica de cupos y 0.0% de sobrecupo verificados bajo contención multihilo de 20 peticiones concurrentes.
- **Calidad y Cobertura (RNF09):** 443 pruebas automatizadas passing con 0 fallos (Frontend: 83.25%, Backend: 90.40%).
- **Integración Continua:** Aprobado en GitHub Actions tras la corrección de linteo Ruff (`370766f`) en el PR #6.
