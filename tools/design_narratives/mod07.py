# -*- coding: utf-8 -*-
"""
Modulo 07: Gamificación e Incentivos (Fase de Diseño)
Contiene: CUS-018, CUS-019
"""

def get_mod07():
    return """### MOD-07: Gamificación e Incentivos

#### CUS-018 - Emitir constancia institucional de horas de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-018** (CUS-018) |
| **Nombre** | Emitir constancia oficial de horas de mentoría con firma criptográfica y QR |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-022 (Parametrización institucional de umbrales y emisión de certificados), RF-023 (Descarga y verificación institucional de certificados); RN-14 (Umbral mínimo de 20 horas acreditadas con bitácoras visadas) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional, Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 - Sprint 07 |
| **Descripción** | Permite a los estudiantes mentores solicitar y descargar una constancia institucional de horas de mentoría acreditadas una vez alcanzado el umbral reglamentario de 20 horas efectivas de dictado (RN-14) con bitácoras pedagógicas debidamente registradas y visadas por la administración. El componente `CertificateView.tsx` despacha la solicitud mediante `POST /api/v1/certificates/generate` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/certificates.py`. El servicio `CertificateService` verifica en base de datos la suma de horas dictadas (`SUM(duracion_minutos)/60 >= 20`), genera un código de serie alfanumérico único, calcula el sello criptográfico SHA-256 del documento, genera un código QR de verificación institucional que apunta al validador público de la universidad, y compila el documento en formato PDF. Persiste la entidad `CertificadoHoras` (`app/models/certificate.py`) y retorna el identificador del archivo para su descarga segura. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-07: Gamificación, Reputación y Certificación)<br>Reglamento de Prácticas Pre-Profesionales y Responsabilidad Social EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/CertificateView.tsx`<br>`aplicacion/frontend/src/services/certificateService.ts` (`CertificateService`, `ApiCertificateAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/certificates.py` (`POST /api/v1/certificates/generate`, `GET /api/v1/certificates/{id}/download`, `GET /api/v1/certificates/verify/{code}`)<br>`aplicacion/backend/app/services/certificate_service.py` (`CertificateService.generate_certificate`, `CertificateService.verify_code`)<br>`aplicacion/backend/app/models/certificate.py` (`CertificadoHoras`), `app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. Estudiante mentor autenticado con token JWT institucional activo.<br>2. Suma acumulada de al menos 20 horas de mentoría con bitácoras pedagógicas aprobadas en el semestre.<br>3. Inexistencia de constancia duplicada activa para el mismo período académico. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `certificados_horas` con código de verificación alfanumérico y hash SHA-256.<br>2. Archivo PDF estructurado generado en almacenamiento seguro con código QR embebido.<br>3. Despliegue del botón de descarga directa y registro del evento en la auditoría institucional. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de acumulado de horas y verificación de umbral** | |
| **1.** El estudiante mentor accede a `"Mis Certificados"` en `CertificateView.tsx`. | **2.** En `certificateService.ts`, se despacha `GET /api/v1/certificates/summary`. En `certificates.py`, `CertificateService` ejecuta `SELECT sum(s.duracion_minutos)/60.0 as horas_totales FROM sesiones_mentoria s JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id WHERE s.id_mentor = :mid AND s.estado = 'BITACORA_REGISTRADA'`. Retorna HTTP 200 con el total de horas acumuladas. En `CertificateView.tsx`, se renderiza una barra de progreso porcentual hacia la meta reglamentaria de 20 horas (RN-14) en color azul institucional. Si las horas son iguales o mayores a 20, se habilita el botón `"Emitir Constancia Oficial"`. (Si el total de horas acumuladas es menor a 20, salta a E001). |
| **Fase 2: Solicitud de emisión y previsualización de datos** | |
| **3.** El mentor presiona el botón `"Emitir Constancia Oficial"`. | **4.** En `CertificateView.tsx`, se abre una ventana modal de previsualización que muestra: nombres completos del mentor, código universitario, semestre académico, total de horas acreditadas y una vista preliminar del código QR de validación. El mentor verifica sus datos y presiona el botón `"Confirmar y Generar PDF Cifrado"`. |
| **Fase 3: Generación criptográfica, persistencia y descarga del PDF** | |
| **5.** El mentor observa la animación de compilación segura del documento. | **6.** En `certificateService.ts`, se despacha `POST /api/v1/certificates/generate` con el período semestral. En `certificates.py`, `CertificateService.generate_certificate` inicia una transacción ACID. Genera un identificador alfanumérico único (e.g. `UPT-EPIS-2026-I-0042`), calcula el hash de integridad SHA-256 de los datos y compila el documento PDF oficial incorporando membrete institucional, firma digital del Director de Escuela y código QR de verificación web. Inserta el registro en `certificados_horas`, ejecuta `db.commit()` y retorna HTTP 201 Created con el payload del certificado. En cliente, `CertificateView.tsx` renderiza la vista previa del documento y habilita el botón de descarga directa en formato PDF. |

##### Flujos de Excepción

##### Flujo de excepción E001: Horas acreditadas insuficientes para el umbral institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `CertificateService` comprueba que el acumulado de horas con bitácoras registradas es menor a 20 (`horas_totales < 20.0`). Lanza `HTTPException(status_code=400, detail="INSUFFICIENT_HOURS: Requiere al menos 20 horas de mentoría con bitácora registrada para emitir la constancia oficial (Horas actuales: {horas_totales}).")`.<br><br>En `CertificateView.tsx`, se mantiene el botón de emisión deshabilitado y se despliega un panel informativo en color ámbar indicando las horas faltantes para alcanzar la certificación. |
| **E001-1.2** Hace clic en el botón "Ver Sesiones Pendientes". | **E001-1.3** Redirige a la vista de sesiones para completar bitácoras pendientes y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-019 - Gestionar insignias y reputación gamificada

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-019** (CUS-019) |
| **Nombre** | Gestionar insignias de logro formativo y reputación gamificada de mentores |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-021 (Cálculo dinámico de reputación y visualización de insignias); RN-13 (Gamificación: puntaje por calificaciones, asistencias y puntualidad) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor, Estudiante Mentoreado |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 - Sprint 07 |
| **Descripción** | Permite a la comunidad académica visualizar el progreso, insignias de honor alcanzadas y nivel de reputación formativa de los mentores mediante el componente cliente `GamificationView.tsx` y el servicio `gamificationService.ts`. El backend en `aplicacion/backend/app/api/v1/endpoints/gamification.py` y `app/services/reputation_service.py` expone las consultas de logros `GET /api/v1/gamification/badges` y el cuadro de honor `GET /api/v1/gamification/leaderboard`. El motor de reputación calcula periódicamente el puntaje global $R = 0.5 \times ValoracionPromedio + 0.3 \times HorasAcreditadas + 0.2 \times TasaPuntualidad$ (RN-13), desbloqueando automáticamente insignias de nivel (tales como "Mentor Destacado", "Puntualidad Impecable" y "Especialista en Algoritmos") en la tabla física `insignias_usuarios` (`app/models/gamification.py`), fomentando la participación y el compromiso entre pares. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-07: Gamificación, Reputación y Certificación)<br>Estrategias de Gamificación en la Educación Superior Universitaria |
| **Anexos** | `aplicacion/frontend/src/components/GamificationView.tsx`<br>`aplicacion/frontend/src/services/gamificationService.ts` (`GamificationService`, `ApiGamificationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/gamification.py` (`GET /api/v1/gamification/badges`, `GET /api/v1/gamification/leaderboard`)<br>`aplicacion/backend/app/services/reputation_service.py` (`ReputationService.get_user_badges`, `ReputationService.calculate_rank`)<br>`aplicacion/backend/app/models/gamification.py` (`Insignia`, `InsigniaUsuario`, `ReputacionUsuario`) |
| **Precondiciones** | 1. Usuario institucional autenticado en la plataforma.<br>2. Catálogo de insignias y reglas de desbloqueo configuradas en la base de datos.<br>3. Registro de calificaciones de sesiones o asistencias efectivas en el sistema. |
| **PostCondiciones** | 1. Nómina de insignias obtenidas y bloqueadas con porcentaje de avance retornadas en JSON.<br>2. Tabla de clasificación (leaderboard) calculada en tiempo real de sólo lectura.<br>3. Despliegue interactivo en la interfaz con animación de logros y posición en el cuadro de honor. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de insignias personales y progreso de nivel** | |
| **1.** El usuario hace clic en el enlace `"Insignias y Reputación"` en `GamificationView.tsx`. | **2.** En `gamificationService.ts`, se despacha `GET /api/v1/gamification/badges`. En `gamification.py`, `ReputationService` consulta la tabla `insignias_usuarios` unida con `insignias` para el usuario y calcula las métricas de avance hacia las insignias bloqueadas. Retorna HTTP 200 con el listado completo. En `GamificationView.tsx`, se renderiza una vitrina virtual: las insignias desbloqueadas se muestran en color dorado con su fecha de concesión, y las bloqueadas en color gris con una barra de progreso que indica el porcentaje completado. |
| **Fase 2: Exploración de criterios de logro y detalle de insignia** | |
| **3.** El usuario hace clic sobre una insignia específica (e.g. "Mentor Destacado"). | **4.** En `GamificationView.tsx`, se despliega un panel lateral interactivo con el nombre de la insignia, descripción pedagógica, icono gráfico y requisitos de desbloqueo (e.g. *"Haber dictado más de 10 sesiones con calificación promedio mayor o igual a 4.8 estrellas"*). |
| **Fase 3: Visualización del cuadro de honor institucional (Leaderboard)** | |
| **5.** El usuario hace clic en la pestaña `"Cuadro de Honor de la Escuela"`. | **6.** En `gamificationService.ts`, se despacha `GET /api/v1/gamification/leaderboard`. El backend recupera el Top-10 de mentores clasificados por puntaje de reputación global calculados bajo RN-13. Retorna HTTP 200 con los nombres, cursos y puntuación. `GamificationView.tsx` renderiza la tabla clasificatoria destacando a los tres primeros lugares con medallas de honor, e indicando la posición del usuario en el ranking general con un marco en color azul institucional. (Si el usuario ha configurado su perfil en modo privado con alias anónimo, salta a A001). |

##### Flujos Alternativos

##### Flujo alternativo A001: Visualización en el cuadro de honor con alias anónimo
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 6 del Flujo Normal, el usuario tiene activada la opción de privacidad en su perfil institucional. | **A001-1.2** En `gamification.py`, `ReputationService` anonimiza los datos personales del usuario reemplazando sus nombres oficiales por un seudónimo aleatorio o su código universitario parcial (e.g. *"Mentor EPIS-742"*). |
| **A001-1.3** El usuario visualiza su puntaje de reputación en el ranking garantizando la confidencialidad de su identidad ante terceros. | **A001-1.4** El sistema muestra el interruptor de visibilidad para permitir conmutar a nombre público en cualquier momento y retorna al paso 6 del Flujo Normal de Eventos. |
"""
