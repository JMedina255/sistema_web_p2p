# Control de Avance — Catálogo de Narrativas y Diagramas de Casos de Uso

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.
**Línea base documental:** DOC-SRS-02
**Fecha de corte:** 23 de noviembre de 2026
**Responsables:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian

---

## 1. Resumen Cuantitativo General

| Indicador | Meta general | Alcance actual | Porcentaje (%) | Estado |
|---|---:|---:|---:|---|
| **Narrativas de casos de uso** | 24 | 1 | 4.2 % | En validación (CUS-001) |
| **Diagramas de actividades** | 24 | 1 | 4.2 % | Renderizado (CUS-001) |
| **Diagramas de casos de uso** | 24 | 1 | 4.2 % | Renderizado (CUS-001) |
| **Total de diagramas** | 48 | 2 | 4.2 % | 2 de 48 completados |

---

## 2. Matriz de Detalle por Caso de Uso

| Módulo | Id | Caso de Uso | Narrativa | Diagrama Actividades | Diagrama Caso de Uso | Estado Hito DOC-SRS-02 |
|---|---|---|:---:|:---:|:---:|---|
| **MOD-01** | **CUS-001** | **Iniciar sesión institucional con 2FA** | **Revisado H01** | **Actualizado y renderizado** | **Actualizado y renderizado** | **Versión revisable (Pendiente de Aprobación)** |
| MOD-01 | CUS-010 | Gestionar asignación de roles de usuario | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-02 | CUS-006 | Registrar oferta de mentoría académica | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-02 | CUS-008 | Gestionar demanda insatisfecha de mentoría | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-02 | CUS-005 | Postular al rol de estudiante mentor | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-02 | CUS-021 | Evaluar postulaciones a mentor por comité | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-03 | CUS-002 | Consultar catálogo de mentorías con recomendación | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-03 | CUS-003 | Reservar cupo para sesión de mentoría | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-03 | CUS-004 | Ratificar asistencia a sesión de mentoría (T-24h) | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-03 | CUS-023 | Evaluar quórum y ejecutar corte automático (T-24h) | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-03 | CUS-024 | Cancelar reserva de cupo por estudiante | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-04 | CUS-007 | Registrar asistencia y bitácora pedagógica | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-04 | CUS-012 | Registrar calificación y feedback bidireccional | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-04 | CUS-013 | Consultar historial académico de mentorías | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-04 | CUS-014 | Emitir constancia de horas de mentoría | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-04 | CUS-018 | Gestionar justificación de inasistencia a sesión | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-04 | CUS-019 | Consultar bitácoras de mentoría por tutor | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-009 | Consultar analítica institucional de mentorías | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-011 | Exportar reportes ejecutivos consolidados | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-015 | Configurar parámetros del algoritmo de recomendación | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-016 | Gestionar auditoría de eventos de seguridad | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-017 | Configurar ambientes físicos y virtuales | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-020 | Gestionar catálogo curricular y asignaturas | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |
| MOD-05 | CUS-022 | Configurar parámetros de corte y penalización | Pendiente | Pendiente | Pendiente | No iniciado (En espera de aprobación CUS-001) |

---

## 3. Criterio de Detención y Siguiente Iteración

De conformidad con las restricciones obligatorias del hito **DOC-SRS-02**:
- Se ha desarrollado de manera **exclusiva** el caso de uso **CUS-001**.
- Se han generado y renderizado **exclusivamente** los diagramas de actividades y de caso de uso del **CUS-001**.
- **Punto de detención mandatorio:** No se iniciará la reconstrucción de los 23 casos de uso restantes (CUS-002 al CUS-024) hasta recibir la aprobación formal y por escrito del presente modelo para CUS-001.

### Actualización administrativa H01 — 2026-11-28

- Los PR #26 y #27 ya se encuentran incorporados en `main`; esta integración confirma trazabilidad de Git, no aprobación funcional de la narrativa.
- CUS-001 fue recontrastado con la interfaz, los servicios y las pruebas vigentes sobre la base `ded3afa`.
- La narrativa y sus dos diagramas quedaron en estado **revisable, pendiente de aprobación**.
- Los hallazgos y pendientes de SRS, SAD y README se registran en `docs/revision_srs/CUS-001/MATRIZ_REVISION_H01.md` sin ampliar el alcance a otros casos de uso.
