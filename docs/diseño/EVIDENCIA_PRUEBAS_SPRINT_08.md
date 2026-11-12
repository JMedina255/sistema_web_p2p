# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 08
## «Priorización Académica, Analítica Institucional, Auditoría y Cierre de Construcción (627 Pruebas Automatizadas)»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Estado:** **627 de 627 Pruebas Superadas (100% Satisfactorio, 0 Fallos, Cobertura >85%) — SISTEMA 100% VALIDADO**

---

## Resumen Ejecutivo de Pruebas Finales (Cierre del Sistema)

| Métrica | Backend (Pytest) | Frontend (Vitest) | Total Consolidado |
| :--- | :---: | :---: | :---: |
| **Suites de Pruebas** | 21 suites | 35 suites | **56 suites** |
| **Pruebas Aprobadas** | 280 casos | 347 casos | **627 casos (100% éxito)** |
| **Cobertura de Código**| 89.6% | 85.2% | **>85% Cobertura Global** |

### Desglose de Pruebas por Módulos:
1. **MOD-01 (Seguridad y Gobernanza):** 36 pruebas (Autenticación 2FA, OTP, JWT, Consentimiento Ley N° 29733, RBAC).
2. **MOD-02 (Ofertas y Espacios):** 48 pruebas (Publicación, detección de solapamientos, parser de horarios, reprogramaciones).
3. **MOD-03 (Perfil y Catálogo):** 38 pruebas (Matriz semanal 6×11, árbol curricular, temarios silábicos).
4. **MOD-04 (Demanda y Recomendaciones):** 52 pruebas (Motor híbrido EdRecSys, similitud coseno, banco de solicitudes).
5. **MOD-05 (Quórum y Concurrencia):** 96 pruebas (Cerrojos pesimistas FOR UPDATE, ratificación, desistimiento, corte T-24h).
6. **MOD-06 (Asistencia y Bitácoras):** 84 pruebas (Pase QR TOTP, bitácoras con hash SHA-256 en 48h, encuestas de calidad).
7. **MOD-07 (Gamificación y Certificados):** 72 pruebas (Insignias, reputación, control de umbral 20h, ReportLab PDF y QR).
8. **MOD-08 (Analítica y Configuración):** 73 pruebas (Tablero analítico, métricas ICACIT, auditoría de bitácoras, settings).
9. **Pruebas de Navegación, Layout y Seguridad:** 128 pruebas (Guarda RBAC `RoleGuard`, accesibilidad WCAG 2.1 AA, suites de integración).

**Total General:** **627 pruebas automatizadas ejecutadas y superadas con 0 fallos.**
