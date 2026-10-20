# Snapshot de Cierre: Sprint 1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II) — EPIS, UPT  
**Docente:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Fecha de Congelamiento:** 19/10/2026  
**Commit Git de Referencia:** [`3cda166`](https://github.com/JMedina255/sistema_web_p2p/commit/3cda166)  
**Rama Base:** `main`  
**Estado:** ✅ **Cerrado, Verificado y Homologado**

---

## 1. Propósito de este Snapshot

Este directorio constituye un **respaldo inmutable de sólo lectura** que captura con total fidelidad el estado final alcanzado al concluir el **Sprint 1: Base técnica, acceso inicial y catálogo curricular**.

Permite auditar retrospectivamente:
1. El estado exacto de la documentación técnica y arquitectónica ([`docs/`](file:///d:/sistema_web_p2p/sprints/sprint-01/docs)) en la transición de la fase de análisis/diseño hacia la construcción.
2. El código fuente limpio ([`aplicacion/`](file:///d:/sistema_web_p2p/sprints/sprint-01/aplicacion)) con el 100% de sus pruebas automatizadas operativas al momento del cierre.

---

## 2. Contenido del Respaldo

```text
sprints/sprint-01/
├── SNAPSHOT_INFO.md              # Este archivo de metadatos y auditoría
├── docs/                         # Documentación viva congelada al Sprint 1
│   ├── FD01-EPIS-Informe de Factibilidad.md
│   ├── FD02-EPIS-Informe Vision de Proyecto.md
│   ├── FD03-EPIS-Informe SRS de Proyecto.md     # Línea base de requerimientos (v2.0)
│   ├── FD04-EPIS-Informe SAD de Proyecto.md     # Arquitectura de software (v1.1)
│   ├── diagramas_general.md                     # Modelos UML y diagramas PlantUML
│   ├── diagramas_de_secuencia.md
│   ├── diagramas_secuencia_pruebas.md
│   ├── flujos_por_perfil_y_diagrama_paquetes.md
│   ├── matriz_inconsistencias.md
│   ├── supabase_setup_guide.md                  # Guía de aprovisionamiento en Supabase
│   └── sprints/
│       ├── PLAN_SPRINTS_Y_TAREAS.md             # Plan maestro de 4 sprints (72 horas)
│       └── sprint-01.md                         # Acta y registro de ejecución de Sprint 1
└── aplicacion/                   # Código fuente congelado (limpio de caches y vendors)
    ├── backend/                  # FastAPI, SQLAlchemy 2.0, Alembic, Pytest (50 tests)
    └── frontend/                 # React 19, TypeScript, Vite, Vitest (46 tests)
```

---

## 3. Métricas de Calidad y Cierre del Sprint 1

| Dimensión de Control | Métrica Obtenida | Umbral / Meta Exigida | Dictamen |
| :--- | :---: | :---: | :---: |
| **Horas ejecutadas** | 18 h (9 h Joan / 9 h Renzo) | 18 horas planificadas | ✅ Cumplido al 100% |
| **Pruebas Backend (Pytest)** | 50 pruebas aprobadas | $\ge 20$ pruebas unitarias | ✅ Superado holgadamente |
| **Pruebas Frontend (Vitest)** | 46 pruebas aprobadas | $\ge 20$ pruebas unitarias | ✅ Superado holgadamente |
| **Total Pruebas Automatizadas** | **96 pruebas pasando** | $\ge 40$ pruebas | ✅ Aprobado |
| **Cobertura de Backend** | **91.62%** | $\ge 70\%$ (**RNF09**) | ✅ Superado |
| **Cobertura de Frontend** | **93.81%** | $\ge 70\%$ (**RNF09**) | ✅ Superado |
| **Linteo de Código** | 0 errores (Ruff / ESLint) | Cero infracciones de estilo | ✅ Conforme |
| **Compilación Frontend** | Vite bundle generado (`dist/`) | 0 errores de tipado TypeScript | ✅ Conforme |

---

## 4. Trazabilidad de Tareas Culminadas

* **T-01 (Joan, 4 h):** Entorno desacoplado React 19 + FastAPI + conexión a base de datos PostgreSQL/Supabase lazy y sanitizada.
* **T-02 (Joan, 2 h):** Interfaz visual de autenticación OTP ([`LoginOtpView.tsx`](file:///d:/sistema_web_p2p/sprints/sprint-01/aplicacion/frontend/src/components/LoginOtpView.tsx)) con validación estricta `@upt.pe`.
* **T-06 (Joan, 3 h):** Pipeline de Integración Continua ([`.github/workflows/ci.yml`](file:///d:/sistema_web_p2p/.github/workflows/ci.yml)) verificado en GitHub Actions.
* **T-09 (Renzo, 2 h):** Modelos ORM, migración Alembic con secuencias sincronizadas y endpoint del catálogo con las **5 materias filtro críticas** de la EPIS-UPT.
* **T-03 (Renzo, 4 h):** API REST de autenticación OTP con invalidación de desafíos anteriores (**RN-01**), tokens JWT de 8 horas (**RNF01**) y adaptador frontend real.
* **T-07 (Renzo, 3 h):** Script de políticas de seguridad por filas (RLS) para Supabase con permisos granulares para `anon`, `authenticated` y `service_role`.

---
*Fin del registro de snapshot para Sprint 1.*
