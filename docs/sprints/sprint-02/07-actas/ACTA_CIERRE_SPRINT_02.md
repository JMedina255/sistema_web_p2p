# Acta Formal de Cierre y Entrega Técnica — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Sprint:** 02 — Roles, Currículo, Perfiles y Consentimiento Informado (Ley N° 29733)  
**Curso:** Construcción de Software I (Semestre 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Responsable:** Grupo 03 / C-SharkTeam  
**Código del Acta:** `ACTA-CIERRE-S02-2026-II`  
**Fecha de Suscripción:** 23 de Octubre de 2026  
**Lugar:** Tacna, Perú — Escuela Profesional de Ingeniería de Sistemas  

---

## 1. Participantes y Horas de Esfuerzo Ejecutadas

Reunidos los integrantes del equipo de desarrollo, se certifica la dedicación horaria efectiva y la culminación de las tareas comprometidas según la planificación académica:

| Integrante | Código UPT | Rol en el Incremento | Tareas Oficiales Ejecutadas | Horas Planificadas | Horas Ejecutadas | Estado |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| **MEDINA QUISPE, Joan Cristian** | 2022074255 | Frontend Lead, Arquitectura UI & CI | **T-04** (Consentimiento UI), **T-10** (Catálogo avanzado), **T-11** (Perfil y grilla 6×11) | 7.0 h | 7.0 h | **100% Concluido** ✅ |
| **ANTAYHUA MAMANI, Renzo Antonio** | 2022073504 | Backend Lead, Persistencia ORM & RLS | **T-05** (Persistencia legal), **T-08** (Roles y mérito RN-03), **T-12** (API horarios), **T-13** (Seguridad RLS) | 7.0 h | 7.0 h | **100% Concluido** ✅ |
| **Total del Sprint 02** | — | — | **7 Tareas Oficiales (PB-003, PB-005, PB-006, PB-007, PB-008)** | **14.0 h** | **14.0 h** | **100% Concluido** ✅ |

---

## 2. Acuerdos y Constatación de Entregables Técnicos

El equipo hace constar que los entregables del Sprint 02 se encuentran implementados, probados y respaldados en el repositorio oficial de Git bajo la rama `feat/sprint-02-roles-curriculo-perfiles`:

1. **Commit de Consolidación Frontend:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74)
   - Componentes React 19: `ConsentModalView.tsx`, `CurriculumCatalogView.tsx`, `ProfileAvailabilityView.tsx`.
   - Servicios tipados: `consentService.ts`, `profileService.ts`.
   - Suite de 66 pruebas automatizadas en Vitest con **91.10%** de cobertura.
2. **Commit de Consolidación Backend:** [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f)
   - Endpoints REST en FastAPI: `/api/v1/consent`, `/api/v1/roles`, `/api/v1/profiles`.
   - Servicios y modelos ORM: `consent_service.py`, `role_service.py`, `profile_service.py`, migración Alembic `002_roles_and_profiles.py`.
   - Políticas RLS en Supabase: `scripts/supabase_rls_sprint02.sql`.
   - Suite de 84 pruebas automatizadas en Pytest con **90.64%** de cobertura.
3. **Total de Pruebas Acumuladas:** **150 pruebas automatizadas**, 0 fallos, superando el umbral de 70% estipulado en **RNF09**.

---

## 3. Declaración de Limitaciones Técnicas y Ética Académica

En estricto apego al principio de transparencia metodológica:
1. **Tratamiento Legal (Ley N° 29733):** El equipo deja constancia de que los mecanismos técnicos desarrollados (modal forzado, persistencia de marcas UTC, dirección IP y bloqueo por rechazo) fueron diseñados para cumplir con las directrices operativas de la Ley N° 29733 en el marco del prototipo académico. No constituyen una certificación legal homologada por la Autoridad Nacional de Protección de Datos Personales (ANPDS) ni sustituyen la asesoría jurídica institucional.
2. **Aprobación de la Cátedra:** El presente incremento se somete a revisión y calificación del docente de cátedra, **Dr. Ricardo Eduardo Valcárcel Alvarado**, sin asumir aprobación tácita ni institucional de la Dirección de la EPIS hasta la sustentación formal del sprint.
3. **Autonomía del Incremento:** Las funcionalidades de búsqueda algorítmica *Top-k* (EdRecSys) y reservas transaccionales quedan reservadas para los Sprints 03 y 04 según la planificación maestra.

---

## 4. Firmas de Conformidad del Equipo de Desarrollo

En señal de conformidad con los términos del presente documento y la exactitud de los resultados reportados, firman los responsables técnicos:

```text
_________________________________________         _________________________________________
     Joan Cristian Medina Quispe                       Renzo Antonio Antayhua Mamani
          Código: 2022074255                                Código: 2022073504
      Frontend Lead & CI Grupo 03                       Backend Lead & RLS Grupo 03
```
