# Paquete Maestro de Sustentación Oficial — Sprint 04

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend & UI Architecture (T-18, T-20, T-21, T-23)  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Database & Concurrencia Transaccional (T-17, T-19, T-22, T-24)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Ubicación Canónica:** `docs/presentaciones/sprint-04/README.md`  
**Línea Base en Git:** Commits `8bd6583` y `7813a6f` en rama `main`  
**Estado de Calidad:** ✅ **245 de 245 Pruebas Superadas (100% Éxito) | Coberturas: 91.22% Backend / 92.56% Frontend | 0 Defectos Estáticos**  

---

## 1. Mapa de Navegación del Paquete de Sustentación

El presente directorio centraliza los insumos formales preparados para la sustentación académica y técnica del **Sprint 04** (*Recomendación Top-k, Feed de Mentorías, Reserva Transaccional Concurrente con Bloqueo Pesimista RNF07 y Evaluación de Quórum T-24h*):

| Documento / Directorio | Archivo | Propósito y Contenido Principal |
| :--- | :--- | :--- |
| **Guion para Canva (Diapositivas)** | [`PRESENTACION_SPRINT_04.md`](PRESENTACION_SPRINT_04.md) | Guion maestro estructurado en 12 diapositivas 16:9 con textos breves, notas de composición visual, paleta institucional y referencias exactas a las capturas para Canva. |
| **Manual de Exposición Oral (Notas del Orador)** | [`GUION_EXPOSICION_SPRINT_04.md`](GUION_EXPOSICION_SPRINT_04.md) | Discurso oral continuo alternado entre Joan Medina y Renzo Antayhua con marcas de tiempo (16-18 min) y banco de preguntas difíciles de jurado (FAQ técnica). |
| **Matriz de Evidencias Técnicas** | [`MATRIZ_EVIDENCIAS_SPRINT_04.md`](MATRIZ_EVIDENCIAS_SPRINT_04.md) | Fichas técnicas detalladas (EV-S04-01 a EV-S04-16) que acreditan cada resultado real de ejecución, código fuente, transacciones SQL y pruebas automatizadas. |
| **Diagramas Oficiales (PNG)** | [`diagramas/`](diagramas/) | 4 diagramas de arquitectura, flujo de recomendación EdRecSys v1.0, secuencia transaccional y concurrencia pesimista renderizados en alta resolución. |
| **Evidencias Visuales (PNG)** | [`evidencias/`](evidencias/) | 15 capturas técnicas distribuidas en subdirectorios temáticos (`frontend/`, `backend/`, `base_datos/`, `pruebas/`, `calidad/`). |

---

## 2. Inventario Completo de Recursos Gráficos y Diagramas

Todos los artefactos visuales fueron generados a partir de ejecuciones reales del sistema, pruebas automatizadas en terminales limpias y especificaciones canónicas de PlantUML, cumpliendo la directriz de **no emplear mockups ficticios, prototipos de Figma ni imágenes generadas por IA**:

```text
docs/presentaciones/sprint-04/
├── diagramas/
│   ├── arquitectura_sprint04.png                    [115 KB] - Arquitectura Física Multi-Capa (React 19 :5173, FastAPI :8000, Supabase)
│   ├── flujo_recomendacion.png                      [63 KB]  - Pipeline Algorítmico EdRecSys v1.0 (Scoring, Filtros y Multiplicador 1.30x)
│   ├── flujo_reserva.png                            [204 KB] - Diagrama de Secuencia Técnica entre Capas para Reserva Transaccional
│   └── concurrencia_aforo.png                       [128 KB] - Bloqueo Pesimista SELECT FOR UPDATE disputando la última vacante
│
└── evidencias/
    ├── frontend/
    │   ├── 01_recommendation_feed_topk.png          [253 KB] - Feed Interactivo Top-k con tarjetas XAI y selector dual
    │   ├── 02_booking_modal_and_rules.png           [157 KB] - Modal Reactivo de Reserva con advertencia T-24h y aforos RN-05
    │   └── 03_topk_ordering_vitest.png              [111 KB] - Suite Vitest de ordenamiento Top-k en DOM virtual (9 tests)
    │
    ├── backend/
    │   ├── 01_recommendations_endpoint_response.png [134 KB] - Respuesta JSON real de GET /api/v1/recommendations/offers
    │   ├── 02_swagger_api_docs_sprint04.png         [177 KB] - Documentación interactiva Swagger UI de los endpoints S4
    │   ├── 03_quorum_evaluation_cutoff_t24h.png     [134 KB] - Ejecución de evaluación automática de quórum al 50%
    │   └── 04_transactional_service_implementation.png [155 KB] - Código fuente de BookingService.reserve_seat()
    │
    ├── base_datos/
    │   ├── 01_migration_004_reservas_cupo.png       [134 KB] - Migración Alembic 004 DDL con restricciones de unicidad
    │   └── 02_pessimistic_lock_query_select_for_update.png [133 KB] - Traza SQL real en PostgreSQL de SELECT ... FOR UPDATE
    │
    ├── pruebas/
    │   ├── 01_topk_deterministic_ordering_tests.png [134 KB] - Terminal Pytest ORD-01 a ORD-05 (27 tests pasando)
    │   ├── 02_booking_success_and_capacity_409_tests.png [119 KB] - Terminal Pytest Reservas, reglas y HTTP 409 (46 tests)
    │   └── 03_concurrency_pessimistic_lock_rnf07.png [198 KB] - Testbench multihilo de 20 hilos con 0.00% sobrecupo
    │
    └── calidad/
        ├── 01_backend_pytest_coverage_sprint04.png  [127 KB] - Reporte Pytest-Cov al 91.22% (158 tests / 0 fallos)
        ├── 02_frontend_vitest_coverage_sprint04.png [155 KB] - Reporte Vitest Coverage al 92.56% (87 tests / 0 fallos)
        ├── 03_linting_and_formatting_check.png      [87 KB]  - Auditoría de linteo Ruff y ESLint (0 errores / 0 warnings)
        └── 04_production_build_vite.png             [88 KB]  - Compilación y empaquetado de producción en Vite (100 ms)
```

---

## 3. Matriz de Trazabilidad Cruzada del Sprint 04

A continuación, se detalla la correspondencia formal entre ítems del backlog, tareas técnicas, código fuente implementado, pruebas automatizadas y evidencias de sustentación:

| PBI / HU | Tarea | Responsable | Módulo / Componente Construido | Suite de Pruebas | Evidencia Gráfica Principal |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **PB-010** | **T-17** | Renzo | `app/services/recommendation_service.py` | `tests/test_recommendations.py` (ORD-01..05) | `evidencias/backend/01_recommendations_endpoint_response.png`<br>`evidencias/pruebas/01_topk_deterministic_ordering_tests.png` |
| **PB-010** | **T-18** | Joan | `src/services/recommendationService.ts` | `src/services/__tests__/recommendationService.test.ts` | `evidencias/frontend/01_recommendation_feed_topk.png` |
| **PB-010** | **T-19** | Ambos | Algoritmo y DOM de ordenamiento Top-k | `test_recommendations.py` + `TopKOrdering.test.tsx` | `evidencias/pruebas/01_topk_deterministic_ordering_tests.png`<br>`evidencias/frontend/03_topk_ordering_vitest.png` |
| **PB-011** | **T-20** | Joan | `src/components/RecommendationFeedView.tsx` | `src/components/__tests__/RecommendationFeedView.test.tsx` | `evidencias/frontend/01_recommendation_feed_topk.png` |
| **PB-013** | **T-21** | Joan | `src/components/BookingModalView.tsx` | `src/components/__tests__/BookingModalView.test.tsx` | `evidencias/frontend/02_booking_modal_and_rules.png` |
| **PB-013** | **T-22** | Renzo | `app/api/v1/endpoints/bookings.py`<br>`app/models/booking.py`<br>Migración Alembic 004 | `tests/test_bookings.py` (46 tests) | `evidencias/backend/02_swagger_api_docs_sprint04.png`<br>`evidencias/base_datos/01_migration_004_reservas_cupo.png` |
| **PB-013** | **T-23** | Joan | `src/services/bookingService.ts`<br>`src/App.tsx` | `src/services/__tests__/bookingService.test.ts`<br>`src/__tests__/BookingIntegration.test.tsx` | `evidencias/frontend/02_booking_modal_and_rules.png` |
| **PB-013**<br>**PB-014** | **T-24** | Renzo | `app/services/booking_service.py`<br>(Bloqueo pesimista `SELECT ... FOR UPDATE`) | `tests/test_bookings.py` (Suite multihilo 20 hilos) | `evidencias/pruebas/03_concurrency_pessimistic_lock_rnf07.png`<br>`evidencias/base_datos/02_pessimistic_lock_query_select_for_update.png` |

---

## 4. Comandos Reproducibles de Verificación y Auditoría

Para que el jurado docente o evaluador institucional pueda verificar de forma independiente y autónoma las métricas presentadas, se proporcionan los siguientes comandos estándar reproducibles en PowerShell:

### 4.1. Verificación del Backend (FastAPI + SQLAlchemy)

```powershell
# 1. Navegar al backend y activar el entorno virtual
cd aplicacion/backend
.\.venv\Scripts\activate

# 2. Análisis estático y verificación de formato (PEP 8 - 0 defectos)
ruff check .
ruff format --check .

# 3. Ejecución de la suite completa de pruebas con reporte de cobertura
pytest tests/ --cov=app --cov-report=term-missing

# 4. Ejecución del banco de pruebas deterministas Top-k (ORD-01 a ORD-05)
pytest tests/test_recommendations.py -v -k "ord"

# 5. Ejecución del banco transaccional de reservas y testbench multihilo RNF07
pytest tests/test_bookings.py -v -k "reserve_seat or concurrent"

# 6. Levantar servidor local para inspección de Swagger UI
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# Explorar Swagger: http://127.0.0.1:8000/docs
```

### 4.2. Verificación del Frontend (React 19 + TypeScript 5.6 + Vite)

```powershell
# 1. Navegar al frontend
cd aplicacion/frontend

# 2. Auditoría estática y verificación de tipos estrictos
npm run lint
npx tsc -b

# 3. Ejecución de la suite completa de pruebas unitarias y componentes
npm test -- --run

# 4. Ejecución específica de la suite de ordenamiento Top-k en DOM
npm test -- TopKOrdering.test.tsx

# 5. Compilación optimizada de producción
npm run build

# 6. Levantar servidor de desarrollo para inspección visual
npm run dev
# Explorar SPA: http://127.0.0.1:5173
```

---

## 5. Criterios de Calidad y Cumplimiento DoD

| Criterio de Aceptación | Estándar Normativo | Resultado Verificado | Estado de Cumplimiento |
| :--- | :---: | :---: | :---: |
| **Pruebas Automatizadas Totales** | Batería acumulada sin fallos | **245 pruebas superadas (100%)** | ✅ Conforme |
| **Cobertura de Código Backend** | RNF09 ($\ge 70.0\%$) | **91.22%** (+21.22%) | ✅ Superado con Excelencia |
| **Cobertura de Código Frontend** | RNF09 ($\ge 70.0\%$) | **92.56%** (+22.56%) | ✅ Superado con Excelencia |
| **Tasa de Sobrecupo Concurrente** | RNF07 ($0.00\%$) | **0.00%** (20 hilos multihilo) | ✅ Blindado contra colisiones |
| **Latencia Algorítmica EdRecSys** | RNF03 ($< 50\text{ ms}$) | **35.8 µs / candidato** ($0.86\text{ ms}$) | ✅ Superado holgadamente |
| **Auditoría Estática de Código** | Ruff & ESLint | **0 errores, 0 warnings** | ✅ Código Limpio |
| **Compilación de Producción** | Bundle estático | **Generado en 100 ms** (`dist/`) | ✅ Listo para producción |

---

*Paquete oficial consolidado por el Grupo 03 (C-SharkTeam) para la cátedra de Construcción de Software I — EPIS UPT (2026).*
