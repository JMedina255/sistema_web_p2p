# Repositorio de Diagramas Oficiales del Informe SRS v3.1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Equipo Consultor:** C-SharkTeam (Grupo 03)  
**Autores:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  
**Cátedra:** Construcción de Software I (Semestre 2026-II)  
**Fecha:** 14 de noviembre de 2026  

---

## 1. Estructura del Directorio

- `puml/`: Contiene los **119 archivos de código fuente PlantUML (`.puml`)** extraídos del informe SRS v3.1.
- `img/`: Contiene las **imágenes renderizadas en formato PNG de alta resolución** listas para incrustación directa en el documento Markdown maestro y su exportación a Microsoft Word (`.docx`) y Google Docs.

## 2. Convención de Nomenclatura

Los archivos se nombran conforme al patrón estándar:  
`diag_{correlativo:03d}_{seccion}_{tipo_o_cus}.puml`

Ejemplos:
- `diag_001_sec24_organigrama_consultor.puml`: Organigrama funcional del equipo consultor (Diagrama 2.1).
- `diag_002_sec41_actividades_proceso_as_is.puml`: Actividades del proceso actual de asesoría informal (Diagrama 4.1).
- `diag_003_sec42_actividades_proceso_to_be.puml`: Actividades del proceso propuesto P2P (Diagrama 4.2).
- `diag_007_sec622_casos_uso_general_24cus.puml`: Casos de uso general consolidado de los 24 CUS (Diagrama 6.4).
- `diag_016_sec631_ecb_general_consolidado.puml`: Modelo ECB general de análisis (Diagrama 6.13).
- `diag_017_sec631_ecb_cus001.puml` al `diag_040_sec631_ecb_cus022.puml`: Vistas ECB individuales por CUS.
- `diag_041_sec632_act_general_consolidado.puml`: Actividades del dominio general (Diagrama 6.14).
- `diag_042_sec632_act_cus001.puml` al `diag_065_sec632_act_cus022.puml`: Actividades por CUS.
- `diag_066_sec633_seq_general_integracion.puml`: Diagrama de secuencia DSS de integración (Diagrama 6.15).
- `diag_067_sec633_seq_cus001.puml` al `diag_090_sec633_seq_cus022.puml`: Diagramas de secuencia DSS por CUS.
- `diag_091_sec634_clases_logico_general.puml`: Diagrama de clases del modelo lógico general (Diagrama 6.16).
- `diag_092_sec634_clases_logico_cus001.puml` al `diag_115_sec634_clases_logico_cus022.puml`: Clases lógicas por CUS.
- `diag_116_sec635_fsm_sesion_mentoria.puml`: FSM del ciclo de vida de sesión (Diagrama 6.17).
- `diag_117_sec635_fsm_reserva_cupo.puml`: FSM del ciclo de vida de reserva (Diagrama 6.18).
- `diag_118_sec635_fsm_bitacora_certificado.puml`: FSM de bitácoras y constancias (Diagrama 6.19).
- `diag_119_sec636_der_fisico_15tablas.puml`: Diagrama DER físico de las 15 tablas relacionales (Diagrama 6.20).

## 3. Guía de Renderizado y Automatización

El renderizado de todos los archivos `.puml` hacia `.png` se realiza mediante el script oficial:
```bash
python tools/render_srs_diagrams.py
```
El script procesa cada archivo de `puml/` y genera su contraparte en `img/` manteniendo el mismo nombre base.

## 4. Catálogo de Archivos Extraídos (Total: 119)

| N° | Archivo PUML | Diagrama Oficial | Título |
|:---:|:---|:---:|:---|
| 001 | `diag_001_sec24_organigrama_consultor.puml` | **Diagrama 2.1** | Organigrama Funcional del Equipo Consultor C-SharkTeam |
| 002 | `diag_002_sec41_actividades_proceso_as_is.puml` | **Diagrama 4.1** | Diagrama de Actividades del Proceso Actual de Asesoría Informal (As-Is) |
| 003 | `diag_003_sec42_actividades_proceso_to_be.puml` | **Diagrama 4.2** | Diagrama de Actividades del Proceso Propuesto de Mentorías P2P (To-Be) |
| 004 | `diag_004_sec60_ciclo_vida_metodologia.puml` | **Diagrama 6.1** | Fases del Ciclo de Vida del Desarrollo de Software (Metodología UWE - Semestre 2026-II) |
| 005 | `diag_005_sec62_clases_conceptuales_dominio.puml` | **Diagrama 6.2** | Diagrama de Clases Conceptuales del Dominio - Sistema Web P2P EPIS-UPT |
| 006 | `diag_006_sec621_paquetes_arquitecturales.puml` | **Diagrama 6.3** | Diagrama de Paquetes Arquitecturales y Subsistemas del Sistema Web P2P |
| 007 | `diag_007_sec622_casos_uso_general_24cus.puml` | **Diagrama 6.4** | Diagrama de Casos de Uso General Consolidado del Sistema Web P2P (CUS-001 al CUS-024) |
| 008 | `diag_008_sec622_casos_uso_mod01.puml` | **Diagrama 6.5** | Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza |
| 009 | `diag_009_sec622_casos_uso_mod02.puml` | **Diagrama 6.6** | Diagrama de Casos de Uso - MOD-02: Ofertas de Mentoría y Gestión de Recursos |
| 010 | `diag_010_sec622_casos_uso_mod03.puml` | **Diagrama 6.7** | Diagrama de Casos de Uso - MOD-03: Perfil del Mentor y Plan de Aprendizaje |
| 011 | `diag_011_sec622_casos_uso_mod04.puml` | **Diagrama 6.8** | Diagrama de Casos de Uso - MOD-04: Demanda y Recomendaciones Personalizadas |
| 012 | `diag_012_sec622_casos_uso_mod05.puml` | **Diagrama 6.9** | Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones |
| 013 | `diag_013_sec622_casos_uso_mod06.puml` | **Diagrama 6.10** | Diagrama de Casos de Uso - MOD-06: Asistencia, Bitácoras y Feedback |
| 014 | `diag_014_sec622_casos_uso_mod07.puml` | **Diagrama 6.11** | Diagrama de Casos de Uso - MOD-07: Gamificación e Incentivos |
| 015 | `diag_015_sec622_casos_uso_mod08.puml` | **Diagrama 6.12** | Diagrama de Casos de Uso - MOD-08: Analítica, Notificaciones y Configuración |
| 016 | `diag_016_sec631_ecb_general_consolidado.puml` | **Diagrama 6.13** | Diagrama de Análisis de Objetos (Modelo ECB) - Flujo General de Mentorías P2P |
| 017 | `diag_017_sec631_ecb_cus001.puml` | **Diagrama 6.13.1** | Análisis de Objetos (Modelo ECB) - CUS-001: Iniciar sesión institucional con 2FA |
| 018 | `diag_018_sec631_ecb_cus010.puml` | **Diagrama 6.13.2** | Análisis de Objetos (Modelo ECB) - CUS-010: Gestionar asignación de roles de usuario |
| 019 | `diag_019_sec631_ecb_cus006.puml` | **Diagrama 6.13.3** | Análisis de Objetos (Modelo ECB) - CUS-006: Publicar oferta de mentoría académica |
| 020 | `diag_020_sec631_ecb_cus008.puml` | **Diagrama 6.13.4** | Análisis de Objetos (Modelo ECB) - CUS-008: Consultar disponibilidad de espacios y recursos |
| 021 | `diag_021_sec631_ecb_cus005.puml` | **Diagrama 6.13.5** | Análisis de Objetos (Modelo ECB) - CUS-005: Gestionar perfil formativo y disponibilidad horaria |
| 022 | `diag_022_sec631_ecb_cus021.puml` | **Diagrama 6.13.6** | Análisis de Objetos (Modelo ECB) - CUS-021: Explorar catálogo curricular de asignaturas filtro |
| 023 | `diag_023_sec631_ecb_cus002.puml` | **Diagrama 6.13.7** | Análisis de Objetos (Modelo ECB) - CUS-002: Explorar recomendaciones personalizadas Top-k |
| 024 | `diag_024_sec631_ecb_cus003.puml` | **Diagrama 6.13.8** | Análisis de Objetos (Modelo ECB) - CUS-003: Registrar solicitud de demanda académica |
| 025 | `diag_025_sec631_ecb_cus004.puml` | **Diagrama 6.13.9** | Análisis de Objetos (Modelo ECB) - CUS-004: Reservar cupo de mentoría académica |
| 026 | `diag_026_sec631_ecb_cus024.puml` | **Diagrama 6.13.10** | Análisis de Objetos (Modelo ECB) - CUS-024: Ratificar asistencia a sesión de mentoría |
| 027 | `diag_027_sec631_ecb_cus017.puml` | **Diagrama 6.13.11** | Análisis de Objetos (Modelo ECB) - CUS-017: Desistir voluntariamente de reserva |
| 028 | `diag_028_sec631_ecb_cus023.puml` | **Diagrama 6.13.12** | Análisis de Objetos (Modelo ECB) - CUS-023: Evaluar quórum automático a T-24h |
| 029 | `diag_029_sec631_ecb_cus007.puml` | **Diagrama 6.13.13** | Análisis de Objetos (Modelo ECB) - CUS-007: Decisión del mentor ante quórum insuficiente |
| 030 | `diag_030_sec631_ecb_cus012.puml` | **Diagrama 6.13.14** | Análisis de Objetos (Modelo ECB) - CUS-012: Registrar asistencia a sesión de mentoría |
| 031 | `diag_031_sec631_ecb_cus013.puml` | **Diagrama 6.13.15** | Análisis de Objetos (Modelo ECB) - CUS-013: Registrar bitácora académica de sesión |
| 032 | `diag_032_sec631_ecb_cus014.puml` | **Diagrama 6.13.16** | Análisis de Objetos (Modelo ECB) - CUS-014: Visualizar historial y bitácoras académicas |
| 033 | `diag_033_sec631_ecb_cus018.puml` | **Diagrama 6.13.17** | Análisis de Objetos (Modelo ECB) - CUS-018: Emitir constancia institucional de horas de mentoría |
| 034 | `diag_034_sec631_ecb_cus019.puml` | **Diagrama 6.13.18** | Análisis de Objetos (Modelo ECB) - CUS-019: Gestionar insignias y reputación gamificada |
| 035 | `diag_035_sec631_ecb_cus009.puml` | **Diagrama 6.13.19** | Análisis de Objetos (Modelo ECB) - CUS-009: Notificar eventos críticos y alertas temporales |
| 036 | `diag_036_sec631_ecb_cus011.puml` | **Diagrama 6.13.20** | Análisis de Objetos (Modelo ECB) - CUS-011: Generar reportes e indicadores de analítica académica |
| 037 | `diag_037_sec631_ecb_cus015.puml` | **Diagrama 6.13.21** | Análisis de Objetos (Modelo ECB) - CUS-015: Consultar métricas de retención y desempeño |
| 038 | `diag_038_sec631_ecb_cus016.puml` | **Diagrama 6.13.22** | Análisis de Objetos (Modelo ECB) - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733 |
| 039 | `diag_039_sec631_ecb_cus020.puml` | **Diagrama 6.13.23** | Análisis de Objetos (Modelo ECB) - CUS-020: Configurar parámetros institucionales y umbrales |
| 040 | `diag_040_sec631_ecb_cus022.puml` | **Diagrama 6.13.24** | Análisis de Objetos (Modelo ECB) - CUS-022: Gestionar catálogo de temas y materias críticas |
| 041 | `diag_041_sec632_act_general_consolidado.puml` | **Diagrama 6.14** | Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría |
| 042 | `diag_042_sec632_act_cus001.puml` | **Diagrama 6.14.1** | Diagrama de Actividades con Flujo de Objetos - CUS-001: Iniciar sesión institucional con 2FA |
| 043 | `diag_043_sec632_act_cus010.puml` | **Diagrama 6.14.2** | Diagrama de Actividades con Flujo de Objetos - CUS-010: Gestionar asignación de roles de usuario |
| 044 | `diag_044_sec632_act_cus006.puml` | **Diagrama 6.14.3** | Diagrama de Actividades con Flujo de Objetos - CUS-006: Publicar oferta de mentoría académica |
| 045 | `diag_045_sec632_act_cus008.puml` | **Diagrama 6.14.4** | Diagrama de Actividades con Flujo de Objetos - CUS-008: Consultar disponibilidad de espacios y recursos |
| 046 | `diag_046_sec632_act_cus005.puml` | **Diagrama 6.14.5** | Diagrama de Actividades con Flujo de Objetos - CUS-005: Gestionar perfil formativo y disponibilidad horaria |
| 047 | `diag_047_sec632_act_cus021.puml` | **Diagrama 6.14.6** | Diagrama de Actividades con Flujo de Objetos - CUS-021: Explorar catálogo curricular de asignaturas filtro |
| 048 | `diag_048_sec632_act_cus002.puml` | **Diagrama 6.14.7** | Diagrama de Actividades con Flujo de Objetos - CUS-002: Explorar recomendaciones personalizadas Top-k |
| 049 | `diag_049_sec632_act_cus003.puml` | **Diagrama 6.14.8** | Diagrama de Actividades con Flujo de Objetos - CUS-003: Registrar solicitud de demanda académica |
| 050 | `diag_050_sec632_act_cus004.puml` | **Diagrama 6.14.9** | Diagrama de Actividades con Flujo de Objetos - CUS-004: Reservar cupo de mentoría académica |
| 051 | `diag_051_sec632_act_cus024.puml` | **Diagrama 6.14.10** | Diagrama de Actividades con Flujo de Objetos - CUS-024: Ratificar asistencia a sesión de mentoría |
| 052 | `diag_052_sec632_act_cus017.puml` | **Diagrama 6.14.11** | Diagrama de Actividades con Flujo de Objetos - CUS-017: Desistir voluntariamente de reserva |
| 053 | `diag_053_sec632_act_cus023.puml` | **Diagrama 6.14.12** | Diagrama de Actividades con Flujo de Objetos - CUS-023: Evaluar quórum automático a T-24h |
| 054 | `diag_054_sec632_act_cus007.puml` | **Diagrama 6.14.13** | Diagrama de Actividades con Flujo de Objetos - CUS-007: Decisión del mentor ante quórum insuficiente |
| 055 | `diag_055_sec632_act_cus012.puml` | **Diagrama 6.14.14** | Diagrama de Actividades con Flujo de Objetos - CUS-012: Registrar asistencia a sesión de mentoría |
| 056 | `diag_056_sec632_act_cus013.puml` | **Diagrama 6.14.15** | Diagrama de Actividades con Flujo de Objetos - CUS-013: Registrar bitácora académica de sesión |
| 057 | `diag_057_sec632_act_cus014.puml` | **Diagrama 6.14.16** | Diagrama de Actividades con Flujo de Objetos - CUS-014: Visualizar historial y bitácoras académicas |
| 058 | `diag_058_sec632_act_cus018.puml` | **Diagrama 6.14.17** | Diagrama de Actividades con Flujo de Objetos - CUS-018: Emitir constancia institucional de horas de mentoría |
| 059 | `diag_059_sec632_act_cus019.puml` | **Diagrama 6.14.18** | Diagrama de Actividades con Flujo de Objetos - CUS-019: Gestionar insignias y reputación gamificada |
| 060 | `diag_060_sec632_act_cus009.puml` | **Diagrama 6.14.19** | Diagrama de Actividades con Flujo de Objetos - CUS-009: Notificar eventos críticos y alertas temporales |
| 061 | `diag_061_sec632_act_cus011.puml` | **Diagrama 6.14.20** | Diagrama de Actividades con Flujo de Objetos - CUS-011: Generar reportes e indicadores de analítica académica |
| 062 | `diag_062_sec632_act_cus015.puml` | **Diagrama 6.14.21** | Diagrama de Actividades con Flujo de Objetos - CUS-015: Consultar métricas de retención y desempeño |
| 063 | `diag_063_sec632_act_cus016.puml` | **Diagrama 6.14.22** | Diagrama de Actividades con Flujo de Objetos - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733 |
| 064 | `diag_064_sec632_act_cus020.puml` | **Diagrama 6.14.23** | Diagrama de Actividades con Flujo de Objetos - CUS-020: Configurar parámetros institucionales y umbrales |
| 065 | `diag_065_sec632_act_cus022.puml` | **Diagrama 6.14.24** | Diagrama de Actividades con Flujo de Objetos - CUS-022: Gestionar catálogo de temas y materias críticas |
| 066 | `diag_066_sec633_seq_general_integracion.puml` | **Diagrama 6.15** | Diagrama de Secuencia General del Ciclo Transaccional de Mentorías |
| 067 | `diag_067_sec633_seq_cus001.puml` | **Diagrama 6.15.1** | Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA |
| 068 | `diag_068_sec633_seq_cus010.puml` | **Diagrama 6.15.2** | Diagrama de Secuencia - CUS-010: Gestionar asignación de roles de usuario |
| 069 | `diag_069_sec633_seq_item_69.puml` | **Diagrama 69** | Diagrama UML |
| 070 | `diag_070_sec633_seq_cus008.puml` | **Diagrama 6.15.4** | Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios y recursos |
| 071 | `diag_071_sec633_seq_cus005.puml` | **Diagrama 6.15.5** | Diagrama de Secuencia - CUS-005: Gestionar perfil académico y disponibilidad horaria |
| 072 | `diag_072_sec633_seq_cus021.puml` | **Diagrama 6.15.6** | Diagrama de Secuencia - CUS-021: Explorar catálogo curricular de asignaturas filtro |
| 073 | `diag_073_sec633_seq_cus002.puml` | **Diagrama 6.15.7** | Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k |
| 074 | `diag_074_sec633_seq_cus003.puml` | **Diagrama 6.15.8** | Diagrama de Secuencia - CUS-003: Registrar solicitud de demanda académica |
| 075 | `diag_075_sec633_seq_cus004.puml` | **Diagrama 6.15.9** | Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica |
| 076 | `diag_076_sec633_seq_cus024.puml` | **Diagrama 6.15.10** | Diagrama de Secuencia - CUS-024: Ratificar asistencia a sesión de mentoría |
| 077 | `diag_077_sec633_seq_cus017.puml` | **Diagrama 6.15.11** | Diagrama de Secuencia - CUS-017: Desistir voluntariamente de reserva |
| 078 | `diag_078_sec633_seq_cus023.puml` | **Diagrama 6.15.12** | Diagrama de Secuencia - CUS-023: Evaluar quórum automático a T-24h |
| 079 | `diag_079_sec633_seq_cus007.puml` | **Diagrama 6.15.13** | Diagrama de Secuencia - CUS-007: Decisión del mentor ante quórum insuficiente |
| 080 | `diag_080_sec633_seq_cus012.puml` | **Diagrama 6.15.14** | Diagrama de Secuencia - CUS-012: Registrar asistencia a sesión de mentoría |
| 081 | `diag_081_sec633_seq_cus013.puml` | **Diagrama 6.15.15** | Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica de sesión |
| 082 | `diag_082_sec633_seq_cus014.puml` | **Diagrama 6.15.16** | Diagrama de Secuencia - CUS-014: Visualizar historial y bitácoras académicas |
| 083 | `diag_083_sec633_seq_cus018.puml` | **Diagrama 6.15.17** | Diagrama de Secuencia - CUS-018: Emitir constancia institucional de horas de mentoría |
| 084 | `diag_084_sec633_seq_cus019.puml` | **Diagrama 6.15.18** | Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada |
| 085 | `diag_085_sec633_seq_cus009.puml` | **Diagrama 6.15.19** | Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas temporales |
| 086 | `diag_086_sec633_seq_cus011.puml` | **Diagrama 6.15.20** | Diagrama de Secuencia - CUS-011: Generar reportes e indicadores analíticos |
| 087 | `diag_087_sec633_seq_cus015.puml` | **Diagrama 6.15.21** | Diagrama de Secuencia - CUS-015: Consultar métricas de retención y desempeño |
| 088 | `diag_088_sec633_seq_cus016.puml` | **Diagrama 6.15.22** | Diagrama de Secuencia - CUS-016: Auditar trazas de seguridad y consentimiento |
| 089 | `diag_089_sec633_seq_cus020.puml` | **Diagrama 6.15.23** | Diagrama de Secuencia - CUS-020: Configurar parámetros institucionales y umbrales |
| 090 | `diag_090_sec633_seq_cus022.puml` | **Diagrama 6.15.24** | Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas y materias críticas |
| 091 | `diag_091_sec634_clases_logico_general.puml` | **Diagrama 6.16** | Diagrama de Clases del Modelo Lógico del Sistema Web P2P |
| 092 | `diag_092_sec634_clases_logico_cus001.puml` | **Diagrama 6.16.1** | Diagrama de Clases Lógico Parcial - CUS-001: Iniciar sesión institucional con 2FA |
| 093 | `diag_093_sec634_clases_logico_cus010.puml` | **Diagrama 6.16.2** | Diagrama de Clases Lógico Parcial - CUS-010: Gestionar asignación de roles de usuario |
| 094 | `diag_094_sec634_clases_logico_cus006.puml` | **Diagrama 6.16.3** | Diagrama de Clases Lógico Parcial - CUS-006: Publicar oferta de mentoría académica |
| 095 | `diag_095_sec634_clases_logico_cus008.puml` | **Diagrama 6.16.4** | Diagrama de Clases Lógico Parcial - CUS-008: Consultar disponibilidad de espacios y recursos |
| 096 | `diag_096_sec634_clases_logico_cus005.puml` | **Diagrama 6.16.5** | Diagrama de Clases Lógico Parcial - CUS-005: Gestionar perfil formativo y disponibilidad horaria |
| 097 | `diag_097_sec634_clases_logico_cus021.puml` | **Diagrama 6.16.6** | Diagrama de Clases Lógico Parcial - CUS-021: Explorar catálogo curricular de asignaturas filtro |
| 098 | `diag_098_sec634_clases_logico_cus002.puml` | **Diagrama 6.16.7** | Diagrama de Clases Lógico Parcial - CUS-002: Explorar recomendaciones personalizadas Top-k |
| 099 | `diag_099_sec634_clases_logico_cus003.puml` | **Diagrama 6.16.8** | Diagrama de Clases Lógico Parcial - CUS-003: Registrar solicitud de demanda académica |
| 100 | `diag_100_sec634_clases_logico_cus004.puml` | **Diagrama 6.16.9** | Diagrama de Clases Lógico Parcial - CUS-004: Reservar cupo de mentoría académica |
| 101 | `diag_101_sec634_clases_logico_cus024.puml` | **Diagrama 6.16.10** | Diagrama de Clases Lógico Parcial - CUS-024: Ratificar asistencia a sesión de mentoría |
| 102 | `diag_102_sec634_clases_logico_cus017.puml` | **Diagrama 6.16.11** | Diagrama de Clases Lógico Parcial - CUS-017: Desistir voluntariamente de reserva |
| 103 | `diag_103_sec634_clases_logico_cus023.puml` | **Diagrama 6.16.12** | Diagrama de Clases Lógico Parcial - CUS-023: Evaluar quórum automático a T-24h |
| 104 | `diag_104_sec634_clases_logico_cus007.puml` | **Diagrama 6.16.13** | Diagrama de Clases Lógico Parcial - CUS-007: Decisión del mentor ante quórum insuficiente |
| 105 | `diag_105_sec634_clases_logico_cus012.puml` | **Diagrama 6.16.14** | Diagrama de Clases Lógico Parcial - CUS-012: Registrar asistencia a sesión de mentoría |
| 106 | `diag_106_sec634_clases_logico_cus013.puml` | **Diagrama 6.16.15** | Diagrama de Clases Lógico Parcial - CUS-013: Registrar bitácora académica de sesión |
| 107 | `diag_107_sec634_clases_logico_cus014.puml` | **Diagrama 6.16.16** | Diagrama de Clases Lógico Parcial - CUS-014: Visualizar historial y bitácoras académicas |
| 108 | `diag_108_sec634_clases_logico_cus018.puml` | **Diagrama 6.16.17** | Diagrama de Clases Lógico Parcial - CUS-018: Emitir constancia institucional de horas de mentoría |
| 109 | `diag_109_sec634_clases_logico_cus019.puml` | **Diagrama 6.16.18** | Diagrama de Clases Lógico Parcial - CUS-019: Gestionar insignias y reputación gamificada |
| 110 | `diag_110_sec634_clases_logico_cus009.puml` | **Diagrama 6.16.19** | Diagrama de Clases Lógico Parcial - CUS-009: Notificar eventos críticos y alertas temporales |
| 111 | `diag_111_sec634_clases_logico_cus011.puml` | **Diagrama 6.16.20** | Diagrama de Clases Lógico Parcial - CUS-011: Generar reportes e indicadores de analítica académica |
| 112 | `diag_112_sec634_clases_logico_cus015.puml` | **Diagrama 6.16.21** | Diagrama de Clases Lógico Parcial - CUS-015: Consultar métricas de retención y desempeño |
| 113 | `diag_113_sec634_clases_logico_cus016.puml` | **Diagrama 6.16.22** | Diagrama de Clases Lógico Parcial - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733 |
| 114 | `diag_114_sec634_clases_logico_cus020.puml` | **Diagrama 6.16.23** | Diagrama de Clases Lógico Parcial - CUS-020: Configurar parámetros institucionales y umbrales |
| 115 | `diag_115_sec634_clases_logico_cus022.puml` | **Diagrama 6.16.24** | Diagrama de Clases Lógico Parcial - CUS-022: Gestionar catálogo de temas y materias críticas |
| 116 | `diag_116_sec635_fsm_sesion_mentoria.puml` | **Diagrama 6.17** | Máquina de Estados Finitos - Ciclo de Vida de SesionMentoria |
| 117 | `diag_117_sec635_fsm_reserva_cupo.puml` | **Diagrama 6.18** | Máquina de Estados Finitos - Ciclo de Vida de ReservaCupo |
| 118 | `diag_118_sec635_fsm_bitacora_certificado.puml` | **Diagrama 6.19** | Máquina de Estados Finitos - Ciclo de Vida de BitacoraPedagogica y CertificadoHoras |
| 119 | `diag_119_sec636_der_fisico_15tablas.puml` | **Diagrama 6.20** | Diagrama Entidad-Relación Físico (15 Tablas Relacionales) - PostgreSQL |

---
*Repositorio de diagramas generado en Hito D02.*
