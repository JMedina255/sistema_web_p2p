# Carpeta de Evidencias Técnicas y Gráficas — Sprint 06

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani)  
**Fecha de Corte:** 07 de Noviembre de 2026  
**Commit Oficial de Cierre:** [`c43b455`](https://github.com/JMedina255/sistema_web_p2p/commit/c43b455) / [`1b43eea`](https://github.com/JMedina255/sistema_web_p2p/commit/1b43eea)  

---

## 1. Contenido y Propósito de la Carpeta

Esta carpeta almacena el acervo consolidado de evidencias gráficas, capturas visuales auténticas, reportes de ejecución automatizada y diagramas del incremento correspondiente al **Sprint 06: Evaluación Automatizada de Quórum en T-24h, Resolución de Contingencias, Control de Asistencias por QR Dinámico TOTP y Registro de Bitácoras Pedagógicas con Sello SHA-256**.

### Cuadro 1.1: Inventario de Evidencias Técnicas del Sprint 06

| Artefacto / Evidencia | Referencia Documental Canónica | Descripción Técnica y Cobertura |
| :--- | :--- | :--- |
| **Reporte Pytest Backend (188 pruebas)** | [`sprint-06.md`](../sprint-06.md) (Sección 6) | Batería de 188 pruebas automatizadas pasando con 87.42% de cobertura de líneas en Pytest, incluyendo suites en `test_quorum.py`, `test_quorum_decision.py`, `test_attendance.py` y `test_bitacora.py`. |
| **Reporte Vitest Frontend (277 pruebas)**| [`sprint-06.md`](../sprint-06.md) (Sección 6) | Batería de 277 pruebas pasando con 83.25% de cobertura de líneas en Vitest (24 suites), incluyendo `MentorSessionsView.test.tsx`, `SessionAttendanceView.test.tsx`, `BitacoraFormView.test.tsx` y `SessionClosureIntegration.test.tsx`. |
| **Flujo de Integración Continua** | GitHub Actions (`.github/workflows/ci.yml`) | Aprobación del flujo de CI en PR #7, consolidando 465 pruebas passing con 0 fallos y linteo estricto (Ruff y ESLint). |
| **Diagramas de Secuencia y Estados** | [`sprint-06.md`](../sprint-06.md) (Sección 4.7) | Diagramas PlantUML de secuencia de evaluación de quórum a T-24h, decisión de contingencia del mentor y ciclo de vida de la bitácora pedagógica. |
| **Capturas Gráficas del Sistema (10 PNGs)** | [`sprint-06.md`](../sprint-06.md) (Sección 7) | Diez capturas visuales auténticas generadas mediante Playwright sobre el sistema en ejecución a resolución estandarizada 1440 × 900. |

Fuente: Elaboración propia.

El Cuadro 1.1 certifica los registros de verificación formal que respaldan el cierre técnico del Sprint 06, cuyos enlaces relativos resuelven con exactitud hacia los documentos canónicos del proyecto.

---

## 2. Inventario Maestro de Capturas Gráficas (Resolución 1440 × 900)

A continuación, se detalla la matriz quíntuple de capturas visuales incorporadas en el acervo documental del Sprint 06:

### Cuadro 1.2: Inventario Detallado de Capturas Gráficas Oficiales del Sprint 06

| Archivo PNG | Figura Canónica | Tarea / Hito | Requisitos & Reglas | Descripción y Propósito Técnico | Fuente, Entorno y Commit |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `01_notificacion_quorum_insuficiente.png` | **Fig. 7.1** | T-29 / T-30 / T-32 | RF15, CUS23, RN-08, RN-09, RN-10 | Vista de «Mis Sesiones» (`MentorSessionsView.tsx`) destacando sesión `SES-0010` con borde ámbar, insignia de quórum insuficiente (2/10 inscritos a T-18h) y botón «⚡ Resolver Contingencia». | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `02_modal_resolucion_contingencia.png` | **Fig. 7.2** | T-32 / T-33 | RF16, CUS07, RN-10, RNF05 | Diálogo modal accesible WAI-ARIA de resolución de contingencia con diagnóstico de aforo y las tres alternativas canónicas del mentor: Proceder, Reprogramar o Cancelar. | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `03_reprogramacion_antelacion_24h.png` | **Fig. 7.3** | T-32 / T-33 | RF16, CUS07, RN-04, RN-10 | Formulario interactivo de reprogramación en modal con selector `datetime-local` validando antelación $> 24\text{ h}$ para reapertura del período de inscripción. | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `04_cancelacion_definitiva_motivo.png` | **Fig. 7.4** | T-32 / T-33 | RF16, CUS07, RN-10, PB-018 | Captura de justificación académica de cancelación obligatoria en `<textarea>` para su notificación automática a los estudiantes ratificados. | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `05_proyeccion_codigo_qr_totp.png` | **Fig. 7.5** | T-34 / T-36 | RF17, CUS12, RN-05, RN-12, RNF05 | Componente `SessionAttendanceView.tsx` proyectando código QR SVG de alta resolución con temporizador regresivo de 30s y código de respaldo de 6 dígitos. | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `06_lista_asistencia_tiempo_real.png` | **Fig. 7.6** | T-34 / T-36 | RF17, CUS12, RN-12, RNF05 | Pase de lista reactivo en tiempo real con banner verde de confirmación de check-in, insignia «Presente» y registro de marca temporal. | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `07_formulario_bitacora_silabica.png` | **Fig. 7.7** | T-34 / T-35 | RF17, CUS13, RN-12, RNF05 | Formulario `BitacoraFormView.tsx` con selección de temas silábicos de la malla curricular, nivel de dificultad y contador reactivo en advertencia ($< 50$ caracteres). | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `08_validacion_bitacora_sello_sha256.png` | **Fig. 7.8** | T-34 / T-35 | RF17, CUS13, RN-12, RN-14, RNF02 | Confirmación de bitácora sellada criptográficamente con hash inmutable SHA-256, declaración jurada suscrita y cómputo de horas académicas provisionales. | Playwright Chromium · Local Alfa · Commit `c43b455` |
| `09_swagger_api_docs_sprint06.png` | **Fig. 7.9** | T-29 a T-36 | RF15, RF16, RF17, CUS07, CUS12, CUS13, CUS23 | Catálogo OpenAPI 3.1.0 / Swagger UI exponiendo los contratos REST normalizados para evaluación de quórum, decisión de contingencia, asistencia TOTP y bitácoras. | Chrome Headless · FastAPI /docs · Commit `c43b455` |
| `10_pruebas_automatizadas_sprint06.png` | **Fig. 7.10** | T-29 a T-37 | RNF02, RNF07, RNF09 | Panel consolidado de suites automatizadas y flujo CI de GitHub Actions: 465 pruebas aprobadas (188 BE / 277 FE), coberturas $> 80\%$ y 0 fallos. | GitHub Actions Runner · CI Ubuntu · Commit `c43b455` |

Fuente: Elaboración propia conforme a los estándares de [`rules_doc.md`](../../../rules_doc.md).

---

## 3. Script de Reproducción de Evidencias

La totalidad de capturas gráficas e instrumentaciones de prueba es reproducible de manera automatizada ejecutando el script oficial:

```bash
# Desde la raíz del repositorio
python aplicacion/backend/scripts/generate_sprint06_evidence.py
```

El script utiliza el binario oficial de Google Chrome y Playwright para instanciar la SPA React en `http://localhost:5173/?tab=sessions`, inyectar tokens JWT con dominio `@upt.pe`, simular las transiciones de estado HTTP 200 y capturar las pantallas a resolución estandarizada de 1440 × 900 píxeles, replicándolas bidireccionalmente hacia `docs/sprints/sprint-06/05-evidencias/` y `docs/diseño/imagenes/sprint-06/`.
