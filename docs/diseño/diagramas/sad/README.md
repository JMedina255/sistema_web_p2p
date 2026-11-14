# Repositorio de Diagramas Oficiales del Documento SAD v3.1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Equipo Consultor:** C-SharkTeam (Grupo 03)  
**Autores:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  
**Cátedra:** Construcción de Software I (Semestre 2026-II)  
**Fecha:** 14 de noviembre de 2026  

---

## 1. Estructura del Directorio

- `puml/`: Contiene los **14 archivos de código fuente PlantUML (`.puml`)** correspondientes a las vistas arquitectónicas del SAD.
- `img/`: Contiene las **imágenes renderizadas en formato PNG de alta resolución** listas para incrustación directa en el documento Markdown maestro y su exportación a Microsoft Word (`.docx`) y Google Docs.

## 2. Catálogo de los 14 Diagramas Arquitectónicos del SAD

| N° | Identificador / Vista Arquitectónica | Archivo PUML | Archivo Renderizado |
|:---:|:---|:---|:---|
| 01 | **Diagrama 2.1: Vista de Escenarios Arquitectónicos Nucleares (+1 de Kruchten)** | `diag_001_sec02_kruchten_escenarios.puml` | `diag_001_sec02_kruchten_escenarios.png` |
| 02 | **Diagrama 2.2: Vista Lógica en Capas y Subsistemas ECB** | `diag_002_sec02_vista_logica_ecb.puml` | `diag_002_sec02_vista_logica_ecb.png` |
| 03 | **Diagrama 2.3: Vista de Procesos, Concurrencia y Sincronización Transaccional** | `diag_003_sec02_vista_procesos_concurrencia.puml` | `diag_003_sec02_vista_procesos_concurrencia.png` |
| 04 | **Diagrama 2.4: Vista de Desarrollo y Organización de Paquetes de Software** | `diag_004_sec02_vista_desarrollo_paquetes.puml` | `diag_004_sec02_vista_desarrollo_paquetes.png` |
| 05 | **Diagrama 2.5: Vista Física y Topología de Despliegue en Red** | `diag_005_sec02_vista_fisica_despliegue.puml` | `diag_005_sec02_vista_fisica_despliegue.png` |
| 06 | **Diagrama 5.1: Casos de Uso Canónicos Oficiales agrupados por los 8 Módulos (CUS-001 al CUS-024)** | `diag_006_sec05_casos_uso_8modulos.puml` | `diag_006_sec05_casos_uso_8modulos.png` |
| 07 | **Diagrama 6.1: Límites del Sistema Web P2P y Sistemas Externos** | `diag_007_sec06_limites_contexto_sistema.puml` | `diag_007_sec06_limites_contexto_sistema.png` |
| 08 | **Diagrama 7.1: Diagrama de Actividades del Proceso As-Is de Mentorías Informales** | `diag_008_sec07_actividades_proceso_as_is.puml` | `diag_008_sec07_actividades_proceso_as_is.png` |
| 09 | **Diagrama 7.2: Diagrama de Actividades del Proceso Propuesto (To-Be) de Mentorías P2P** | `diag_009_sec07_actividades_proceso_to_be.puml` | `diag_009_sec07_actividades_proceso_to_be.png` |
| 10 | **Diagrama 8.1: Diagrama de Contenedores de Software (C4 Nivel 2 / Metodología UWE)** | `diag_010_sec08_c4_contenedores_software.puml` | `diag_010_sec08_c4_contenedores_software.png` |
| 11 | **Diagrama 9.1: Componentes de Software y Módulos Canónicos del Backend** | `diag_011_sec09_componentes_backend.puml` | `diag_011_sec09_componentes_backend.png` |
| 12 | **Diagrama 10.1: Diagrama Entidad-Relación Físico (15 Tablas Relacionales en PostgreSQL / Supabase)** | `diag_012_sec10_der_fisico_15tablas.puml` | `diag_012_sec10_der_fisico_15tablas.png` |
| 13 | **Diagrama 11.4: Máquina de Estados Finitos de la Sesión de Mentoría (13 Estados Canónicos)** | `diag_013_sec11_fsm_sesion_mentoria.puml` | `diag_013_sec11_fsm_sesion_mentoria.png` |
| 14 | **Diagrama 11.5: Máquina de Estados Finitos de la Reserva de Cupo (9 Estados Canónicos)** | `diag_014_sec11_fsm_reserva_cupo.puml` | `diag_014_sec11_fsm_reserva_cupo.png` |

Fuente: Elaboración propia a partir del documento oficial SAD.
