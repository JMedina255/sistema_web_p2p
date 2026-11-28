"""
Script de Empaquetado de Evidencias Oficiales - Sprint 07 y Sprint 08
Proyecto: Sistema Web P2P - EPIS UPT (Grupo 03 / C-SharkTeam)
Genera el archivo ZIP consolidado listo para adjuntar al informe académico.
"""

import os
import zipfile

BASE_DIR = os.path.abspath(".")
S07_DIR = os.path.join(BASE_DIR, "docs", "sprints", "sprint-07", "05-evidencias")
S08_DIR = os.path.join(BASE_DIR, "docs", "sprints", "sprint-08", "05-evidencias")

ZIP_NAME = "Evidencias_Sprint07_Sprint08_P2P_EPIS.zip"
ZIP_ROOT_PATH = os.path.join(BASE_DIR, ZIP_NAME)
ZIP_SPRINTS_PATH = os.path.join(BASE_DIR, "docs", "sprints", ZIP_NAME)

INDEX_MD = """# Índice General de Evidencias Técnicas — Sprint 07 y Sprint 08
**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT\x20\x20
**Curso:** Construcción de Software I (2026-II)\x20\x20
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas\x20\x20
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani)\x20\x20
**Total de Evidencias:** 14 oficiales (6 de Sprint 07 + 8 de Sprint 08) + 1 documento PDF original compilado.

---

## Sprint 07 – Encuestas y Visado Administrativo (6 Evidencias)
1. `01_formulario_encuesta_post_mentoria.png`: Captura de la encuesta de satisfacción que completa el mentoreado (`PostSessionSurveyModal.tsx`) con 4 dimensiones, escala 1-5 estrellas, retroalimentación cualitativa $\\ge 20$ car. y ventana temporal 24h (RN-12, RN-13, RF18).
2. `02_encuesta_completada_confirmacion.png`: Mensaje de confirmación y ticket `ENC-2026-II-0042` (HTTP 201 Created), mostrando bloqueo reactivo del botón para impedir reenvíos duplicados (RN-13).
3. `03_panel_administrador_bitacoras_pendientes.png`: Bandeja centralizada de auditoría en `AdminDashboardView.tsx` con KPIs directivos, filtros y listado de bitácoras pendientes de fiscalización (CUS22, RF26).
4. `04_visado_bitacora_aprobacion.png`: Modal de inspección técnica con contenidos de la malla curricular, asistencia 100% QR TOTP, validación de firma SHA-256 y visado formal con acreditación de +2.0 hrs (RN-14).
5. `05_estado_horas_acreditadas.png`: Récord académico del mentor certificando 20.0 / 20.0 horas validadas por Dirección, historial auditable de 10 sesiones y calificación promedio de 4.95 / 5.0 ★.
6. `06_pruebas_api_swagger_encuestas_visado.png`: Catálogo Swagger OpenAPI 3.1.0 interactivo con endpoints de encuestas (`POST /api/v1/sessions/{id}/survey`) y visado administrativo (`POST /api/v1/bitacoras/{id}/visar`).

---

## Sprint 08 – Integración Final del MVP (8 Evidencias)
1. `01_pantalla_principal_dashboard_mvp.png`: Dashboard inicial del MVP en `App.tsx` con navegación por pestañas guiadas, conmutador de roles (RBAC) y métricas globales del programa formativo.
2. `02_flujo_mentoria_recomendacion_topk_reserva.png`: Recorrido completo E2E: cartelera Top-k con afinidad del 96%, selección del mentor Renzo Antayhua y confirmación de reserva `RES-2026-1048`.
3. `03_gestion_sesiones_finalizada_bitacora.png`: Ficha de sesión en `MentorSessionsView.tsx` demostrando cierre integral: quórum superado, asistencia digital QR TOTP 100% y bitácora visada con hash SHA-256.
4. `04_interfaz_generacion_constancias.png`: Interfaz `CertificateDownloadView.tsx` verificando el cumplimiento del umbral de 20.0 horas visadas (RN-14) y habilitación de descarga.
5. `05_constancia_pdf_oficial.png` (y archivo `05_constancia_mentoria_oficial.pdf`): Documento oficial emitido con membrete EPIS, folio `CERT-2026-II-EPIS-003`, código QR institucional, sello SHA-256 y marca de agua "DEMO - FINES ACADÉMICOS".
6. `06_metricas_precision_at_k_algoritmo.png`: Reporte experimental del testbench algorítmico certificando $\\text{Precision@3} = 83.3\\%$, $\\text{Precision@5} = 80.0\\%$ y latencia media de $12.4\\text{ ms}$ (RNF03).
7. `07_pruebas_automatizadas_pytest_vitest.png`: Terminal consolidada certificando **717 pruebas automatizadas 100% aprobadas** (354 en Backend Pytest con 84% de cobertura y 363 en Frontend Vitest con 83.5% de cobertura).
8. `08_github_actions_pipeline_aprobado.png`: Flujo de CI en GitHub Actions con todos los checks aprobados (lint, test backend, test frontend, build y security audit) en el release final.
"""


def package_zip():
    print("=== Creando Archivo ZIP Consolidado de Evidencias ===")
    with zipfile.ZipFile(ZIP_ROOT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Agregar Índice General
        zf.writestr("Evidencias_Sprint07_Sprint08/INDICE_EVIDENCIAS_SPRINT07_SPRINT08.md", INDEX_MD)

        # 2. Agregar Archivos Sprint 07
        s07_files = sorted(os.listdir(S07_DIR))
        print(f"\nAñadiendo {len(s07_files)} archivos de Sprint 07...")
        for fname in s07_files:
            fpath = os.path.join(S07_DIR, fname)
            arcname = os.path.join("Evidencias_Sprint07_Sprint08", "Sprint_07_Encuestas_y_Visado", fname)
            zf.write(fpath, arcname)
            print(f"  [+] {arcname} ({os.path.getsize(fpath):,} bytes)")

        # 3. Agregar Archivos Sprint 08
        s08_files = sorted(os.listdir(S08_DIR))
        print(f"\nAñadiendo {len(s08_files)} archivos de Sprint 08...")
        for fname in s08_files:
            fpath = os.path.join(S08_DIR, fname)
            arcname = os.path.join("Evidencias_Sprint07_Sprint08", "Sprint_08_Integracion_Final_MVP", fname)
            zf.write(fpath, arcname)
            print(f"  [+] {arcname} ({os.path.getsize(fpath):,} bytes)")

    # Copiar también a docs/sprints/
    with open(ZIP_ROOT_PATH, "rb") as fsrc, open(ZIP_SPRINTS_PATH, "wb") as fdst:
        fdst.write(fsrc.read())

    size = os.path.getsize(ZIP_ROOT_PATH)
    print("\n[ÉXITO] Archivo ZIP generado exitosamente:")
    print(f"  -> {ZIP_ROOT_PATH} ({size:,} bytes / {size / (1024 * 1024):.2f} MB)")
    print(f"  -> {ZIP_SPRINTS_PATH} ({size:,} bytes / {size / (1024 * 1024):.2f} MB)")


if __name__ == "__main__":
    package_zip()
