#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to apply required fixes to tools/build_srs_narratives.py,
regenerate docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md,
and inject the updated Section 6.2.3 into both:
- docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md
- docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
"""

import re
import os

def patch_build_script():
    filepath = "tools/build_srs_narratives.py"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. CUS-001: Add jump to A002 in step 4
    old_cus001_s4 = '''| **3.** El usuario revisa en pantalla el resumen de su correo institucional y presiona el botón `"Solicitar Código de Acceso"`. | **4.** El sistema genera un código OTP criptográficamente aleatorio de 6 dígitos numéricos, le asigna un tiempo de expiración estricto de 5 minutos conforme a RN-01, e invoca al servicio SMTP institucional para despacharlo al buzón universitario del solicitante. Muestra en primer plano una ventana modal con seis casillas individuales para el ingreso del código, un temporizador regresivo de 5 minutos en color azul institucional y el botón `"Verificar e Ingresar"`. |'''
    new_cus001_s4 = '''| **3.** El usuario revisa en pantalla el resumen de su correo institucional y presiona el botón `"Solicitar Código de Acceso"`. | **4.** El sistema genera un código OTP criptográficamente aleatorio de 6 dígitos numéricos, le asigna un tiempo de expiración estricto de 5 minutos conforme a RN-01, e invoca al servicio SMTP institucional para despacharlo al buzón universitario del solicitante. Muestra en primer plano una ventana modal con seis casillas individuales para el ingreso del código, un temporizador regresivo de 5 minutos en color azul institucional y el botón `"Verificar e Ingresar"`. (Si el usuario no recibe el código en su buzón tras 60 segundos o el temporizador expira, salta a A002). |'''

    # 2. CUS-010: Add jump to A001 in step 2
    old_cus010_s2 = '''| **1.** El Administrador ingresa al panel de `"Gestión de Usuarios y Roles"`, escribe el código de matrícula o apellido del estudiante en el cuadro de búsqueda y presiona la tecla de consulta. | **2.** El sistema filtra el padrón institucional y despliega una tabla con los resultados, mostrando el código universitario, nombres completos, ciclo académico actual, rol vigente indicado mediante una insignia en color gris secundario (`Mentoreado`) y el botón `"Evaluar Postulación"`. |'''
    new_cus010_s2 = '''| **1.** El Administrador ingresa al panel de `"Gestión de Usuarios y Roles"`, escribe el código de matrícula o apellido del estudiante en el cuadro de búsqueda y presiona la tecla de consulta. | **2.** El sistema filtra el padrón institucional y despliega una tabla con los resultados, mostrando el código universitario, nombres completos, ciclo académico actual, rol vigente indicado mediante una insignia en color gris secundario (`Mentoreado`) y el botón `"Evaluar Postulación"`. (Si el Administrador requiere revocar o suspender el rol de un mentor activo, salta a A001). |'''

    # 3. CUS-006: Add jump to A001 in step 1
    old_cus006_s1 = '''| **1.** El Mentor ingresa a su panel docente y presiona el botón `"Nueva Oferta de Mentoría"`. | **2.** El sistema presenta el formulario de publicación con encabezado en color azul institucional, mostrando el menú desplegable `"Asignatura Formativa"` con las materias en las que el mentor posee acreditación, un menú dinámico `"Tema Silábico"` y campos de fecha y horario. |'''
    new_cus006_s1 = '''| **1.** El Mentor ingresa a su panel docente y presiona el botón `"Nueva Oferta de Mentoría"`. (Si la oferta se formula a partir de una solicitud de demanda académica existente, salta a A001). | **2.** El sistema presenta el formulario de publicación con encabezado en color azul institucional, mostrando el menú desplegable `"Asignatura Formativa"` con las materias en las que el mentor posee acreditación, un menú dinámico `"Tema Silábico"` y campos de fecha y horario. |'''

    # 4. CUS-008: Add jump to A001 in step 1
    old_cus008_s1 = '''| **1.** El Mentor accede a la opción `"Disponibilidad de Recintos"` e introduce el día calendario, la hora de inicio, la hora de fin y el tipo de espacio requerido (*Aula Teórica* o *Laboratorio Especializado*). | **2.** El sistema valida que el rango horario especificado sea coherente y pertenezca al horario operativo permitido de la universidad (07:00 a 22:00 horas). (Si el horario está fuera de rango operativo, salta a E001). |'''
    new_cus008_s1 = '''| **1.** El Mentor accede a la opción `"Disponibilidad de Recintos"` e introduce el día calendario, la hora de inicio, la hora de fin y el tipo de espacio requerido (*Aula Teórica* o *Laboratorio Especializado*). (Si el mentor requiere consultar la disponibilidad de canales y salas virtuales supervisadas, salta a A001). | **2.** El sistema valida que el rango horario especificado sea coherente y pertenezca al horario operativo permitido de la universidad (07:00 a 22:00 horas). (Si el horario está fuera de rango operativo, salta a E001). |'''

    # 5. CUS-005: Add jump to A001 in step 3
    old_cus005_s3 = '''| **3.** El estudiante marca las asignaturas filtro en las que solicita apoyo (si es Mentoreado) o en las que se encuentra acreditado para brindar orientación (si es Mentor). | **4.** El sistema valida que las selecciones correspondan al ciclo y rol reglamentario del usuario. (Si un mentoreado intenta seleccionarse como mentor en cursos no aprobados, salta a E001). |'''
    new_cus005_s3 = '''| **3.** El estudiante marca las asignaturas filtro en las que solicita apoyo (si es Mentoreado) o en las que se encuentra acreditado para brindar orientación (si es Mentor). (Si el mentor desea adjuntar enlaces externos o recursos de contacto pedagógico, salta a A001). | **4.** El sistema valida que las selecciones correspondan al ciclo y rol reglamentario del usuario. (Si un mentoreado intenta seleccionarse como mentor en cursos no aprobados, salta a E001). |'''

    # 6. CUS-002: Closure in E001-1.4
    old_cus002_e001 = '''| **E001-1.3** El estudiante pulsa `"Crear Solicitud por Demanda"`. | **E001-1.4** El sistema redirige al formulario del caso de uso `CUS-003` y finaliza el flujo de recomendación sin generar errores. |'''
    new_cus002_e001 = '''| **E001-1.3** El estudiante pulsa `"Crear Solicitud por Demanda"`. | **E001-1.4** El sistema redirige al formulario del caso de uso `CUS-003` y finaliza el caso de uso sin generar registros. |'''

    # 7. CUS-003: Add jump to A001 in step 1, closure in A001-1.4
    old_cus003_s1 = '''| **1.** El estudiante accede a la pestaña `"Solicitudes por Demanda"` y presiona el botón `"Registrar Nueva Solicitud"`. | **2.** El sistema despliega una ventana modal con el encabezado en color azul institucional, proveyendo un menú desplegable de asignaturas filtro, un selector de unidad silábica, un cuadro de texto multilínea para el detalle del requerimiento temático y casillas para la franja horaria preferida. |'''
    new_cus003_s1 = '''| **1.** El estudiante accede a la pestaña `"Solicitudes por Demanda"` y presiona el botón `"Registrar Nueva Solicitud"`. (Si el estudiante encuentra una solicitud afín en el catálogo y opta por sumarse a ella, salta a A001). | **2.** El sistema despliega una ventana modal con el encabezado en color azul institucional, proveyendo un menú desplegable de asignaturas filtro, un selector de unidad silábica, un cuadro de texto multilínea para el detalle del requerimiento temático y casillas para la franja horaria preferida. |'''

    old_cus003_a001 = '''| **A001-1.3** El estudiante presiona el botón `"+1 Me Interesa"`. | **A001-1.4** El sistema incrementa el contador de interesados, registra la adhesión del usuario para notificarle cuando un mentor abra la oferta (`CUS-006`) y el sistema finaliza la interacción mostrando una notificación en color verde con el mensaje: *"Te has sumado exitosamente a esta solicitud"*. |'''
    new_cus003_a001 = '''| **A001-1.3** El estudiante presiona el botón `"+1 Me Interesa"`. | **A001-1.4** El sistema incrementa el contador de interesados, registra la adhesión del usuario para notificarle cuando un mentor abra la oferta (`CUS-006`), despliega una notificación en color verde de éxito con el mensaje: *"Te has sumado exitosamente a esta solicitud"* y el sistema finaliza el caso de uso. |'''

    # 8. CUS-023: Closure in E001-1.4
    old_cus023_e001 = '''| **E001-1.3** El mentor hace clic en la alerta recibida. | **E001-1.4** El sistema transfiere el control al flujo del caso de uso `CUS-007` y finaliza la evaluación del servicio desatendido. |'''
    new_cus023_e001 = '''| **E001-1.3** El mentor hace clic en la alerta recibida. | **E001-1.4** El sistema transfiere el control al caso de uso resolutivo `CUS-007` y finaliza el caso de uso sin generar registros de confirmación. |'''

    # 9. CUS-007: Add jump to E001 in step 2, closure in E001-1.4
    old_cus007_s2 = '''| **1.** El Mentor recibe la alerta institucional en su bandeja y hace clic en el enlace `"Gestionar Sesión con Quórum Insuficiente"` o ingresa a su panel docente. | **2.** El sistema presenta una pantalla de contingencia con el encabezado en color ámbar de advertencia, informando la asignatura, el tema silábico, el aforo total, el número real de alumnos confirmados (e.g. *"3 de 10 estudiantes confirmados"*), y dos botones de acción resolutiva: `"Dictar Sesión Excepcionalmente"` y `"Cancelar Sesión sin Penalidad"`. |'''
    new_cus007_s2 = '''| **1.** El Mentor recibe la alerta institucional en su bandeja y hace clic en el enlace `"Gestionar Sesión con Quórum Insuficiente"` o ingresa a su panel docente. | **2.** El sistema presenta una pantalla de contingencia con el encabezado en color ámbar de advertencia, informando la asignatura, el tema silábico, el aforo total, el número real de alumnos confirmados (e.g. *"3 de 10 estudiantes confirmados"*), y dos botones de acción resolutiva: `"Dictar Sesión Excepcionalmente"` y `"Cancelar Sesión sin Penalidad"`. (Si el mentor no adopta ninguna resolución antes de cumplirse las 12 horas previas a la sesión, salta a E001). |'''

    old_cus007_e001 = '''| **E001-1.3** El mentor accede con posterioridad a la plataforma. | **E001-1.4** El sistema muestra una alerta informativa en color rojo y finaliza el caso de uso sin posibilidad de dictado. |'''
    new_cus007_e001 = '''| **E001-1.3** El mentor accede con posterioridad a la plataforma. | **E001-1.4** El sistema muestra una alerta informativa en color rojo y el sistema finaliza el caso de uso sin posibilidad de dictado. |'''

    # 10. CUS-013: Fix CUS-022 typo to CUS-018 in PostCondiciones, closure in E002-1.4
    old_cus013_post = '''| **PostCondiciones** | 1. La entidad `BitacoraSesion` es persistida en la base de datos vinculada a la sesión y al mentor.<br>2. La sesión de mentoría transiciona al estado canónico `FINALIZADA`.<br>3. Se habilita la encuesta de satisfacción para los alumnos asistentes por 24 horas (`RN-13`) y las horas se registran como `PROVISIONALES` para futura auditoría (`CUS-022`). |'''
    new_cus013_post = '''| **PostCondiciones** | 1. La entidad `BitacoraSesion` es persistida en la base de datos vinculada a la sesión y al mentor.<br>2. La sesión de mentoría transiciona al estado canónico `FINALIZADA`.<br>3. Se habilita la encuesta de satisfacción para los alumnos asistentes por 24 horas (`RN-13`) y las horas se registran como `PROVISIONALES` para futura auditoría y certificación (`CUS-018`). |'''

    old_cus013_e002 = '''| **E002-1.3** El Mentor presiona el botón `"Ir a Control de Asistencia"`. | **E002-1.4** El sistema redirige al caso de uso `CUS-012` para completar el registro y finaliza la excepción. |'''
    new_cus013_e002 = '''| **E002-1.3** El Mentor presiona el botón `"Ir a Control de Asistencia"`. | **E002-1.4** El sistema redirige al caso de uso `CUS-012` para completar el registro y finaliza el caso de uso sin generar registros de bitácora. |'''

    # 11. CUS-018: Fix CUS-022 typo to CUS-014 in Descripción, Precondiciones, E002-1.1, E002-1.3, E002-1.4
    old_cus018_meta = '''| **Descripción** | Permite al Administrador Institucional verificar el cumplimiento del umbral mínimo de horas acumuladas de mentoría académica por parte de los mentores en el periodo lectivo (según la regla RN-14), comprobar que la totalidad de sus bitácoras de sesión hayan sido auditadas y visadas favorablemente (`CUS-022`), y generar formalmente el certificado digital con folio institucional único, firma criptográfica hash SHA-256 y código QR de validación pública para su posterior convalidación de créditos extracurriculares ante la Dirección de Escuela. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Tablero de Auditoría y Certificación Semestral, Previsualizador de Certificado Digital con QR, Plantilla Institucional de Constancia en PDF. |
| **Precondiciones** | 1. El Administrador ha iniciado sesión con facultades directivas (`CUS-001`).<br>2. El estudiante mentor ha acumulado un número de horas auditadas igual o superior al umbral configurado por la escuela (`RN-14`).<br>3. Todas las bitácoras pedagógicas del periodo han sido visadas sin observaciones pendientes (`CUS-022`). |'''
    new_cus018_meta = '''| **Descripción** | Permite al Administrador Institucional verificar el cumplimiento del umbral mínimo de horas acumuladas de mentoría académica por parte de los mentores en el periodo lectivo (según la regla RN-14), comprobar que la totalidad de sus bitácoras de sesión hayan sido auditadas y visadas favorablemente (`CUS-014`), y generar formalmente el certificado digital con folio institucional único, firma criptográfica hash SHA-256 y código QR de validación pública para su posterior convalidación de créditos extracurriculares ante la Dirección de Escuela. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Tablero de Auditoría y Certificación Semestral, Previsualizador de Certificado Digital con QR, Plantilla Institucional de Constancia en PDF. |
| **Precondiciones** | 1. El Administrador ha iniciado sesión con facultades directivas (`CUS-001`).<br>2. El estudiante mentor ha acumulado un número de horas auditadas igual o superior al umbral configurado por la escuela (`RN-14`).<br>3. Todas las bitácoras pedagógicas del periodo han sido visadas sin observaciones pendientes (`CUS-014`). |'''

    old_cus018_e002 = '''##### Flujo de excepción E002: Existencia de bitácoras pendientes de auditoría o con observaciones
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Administrador intenta emitir la constancia pero el sistema detecta que el mentor posee sesiones finalizadas sin dictamen de auditoría en el módulo `CUS-022`. | **E002-1.2** El sistema presenta un aviso en color ámbar de advertencia con el mensaje literal: *"Auditoría incompleta: Existen bitácoras pedagógicas pendientes de revisión o con observaciones no resueltas. Debe visar la totalidad de sesiones antes de certificar"*. |
| **E002-1.3** El Administrador pulsa `"Ir a Auditoría de Bitácoras"`. | **E002-1.4** El sistema redirige al caso de uso `CUS-022` y finaliza la excepción. |'''
    new_cus018_e002 = '''##### Flujo de excepción E002: Existencia de bitácoras pendientes de auditoría o con observaciones
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Administrador intenta emitir la constancia pero el sistema detecta que el mentor posee sesiones finalizadas sin dictamen de auditoría en el módulo de bitácoras académicas (`CUS-014`). | **E002-1.2** El sistema presenta un aviso en color ámbar de advertencia con el mensaje literal: *"Auditoría incompleta: Existen bitácoras pedagógicas pendientes de revisión o con observaciones no resueltas. Debe visar la totalidad de sesiones antes de certificar"*. |
| **E002-1.3** El Administrador pulsa `"Ir a Historial y Bitácoras"`. | **E002-1.4** El sistema redirige al módulo de bitácoras académicas (`CUS-014`) para subsanar observaciones y finaliza el caso de uso sin generar registros de certificación. |'''

    # 12. CUS-019: Add jump to E001 in step 2, closure in E001-1.4
    old_cus019_s2 = '''| **1.** Al cerrarse la ventana de 24 horas para encuestas de una sesión finalizada (`RN-13`), el servicio de gamificación recupera las valoraciones numéricas registradas por los alumnos asistentes. | **2.** El sistema procesa la media ponderada de satisfacción descartando valores espurios y actualiza la reputación global del mentor (con escala de 1.0 a 5.0 estrellas). |'''
    new_cus019_s2 = '''| **1.** Al cerrarse la ventana de 24 horas para encuestas de una sesión finalizada (`RN-13`), el servicio de gamificación recupera las valoraciones numéricas registradas por los alumnos asistentes. | **2.** El sistema procesa la media ponderada de satisfacción descartando valores espurios y actualiza la reputación global del mentor (con escala de 1.0 a 5.0 estrellas). (Si el mentor posee menos de 3 encuestas consolidadas para el cálculo de su reputación inicial, salta a E001). |'''

    old_cus019_e001 = '''| **E001-1.3** El mentor revisa su estado inicial. | **E001-1.4** El sistema finaliza el caso de uso sin generar anomalías. |'''
    new_cus019_e001 = '''| **E001-1.3** El mentor revisa su estado inicial. | **E001-1.4** El sistema asigna la calificación inicial provisional y finaliza el caso de uso sin generar registros de penalización. |'''

    # 13. CUS-022: Closure in E002-1.4
    old_cus022_e002 = '''| **E002-1.3** El Administrador selecciona `"Inactivar Tema"`. | **E002-1.4** El sistema oculta el tema para nuevas ofertas manteniendo la integridad histórica y el sistema finaliza el caso de uso sin errores. |'''
    new_cus022_e002 = '''| **E002-1.3** El Administrador selecciona `"Inactivar Tema"`. | **E002-1.4** El sistema oculta el tema para nuevas ofertas manteniendo la integridad histórica y el sistema finaliza el caso de uso sin generar registros eliminados. |'''

    replacements = [
        (old_cus001_s4, new_cus001_s4, "CUS-001 step 4 jump to A002"),
        (old_cus010_s2, new_cus010_s2, "CUS-010 step 2 jump to A001"),
        (old_cus006_s1, new_cus006_s1, "CUS-006 step 1 jump to A001"),
        (old_cus008_s1, new_cus008_s1, "CUS-008 step 1 jump to A001"),
        (old_cus005_s3, new_cus005_s3, "CUS-005 step 3 jump to A001"),
        (old_cus002_e001, new_cus002_e001, "CUS-002 E001 closure"),
        (old_cus003_s1, new_cus003_s1, "CUS-003 step 1 jump to A001"),
        (old_cus003_a001, new_cus003_a001, "CUS-003 A001 closure"),
        (old_cus023_e001, new_cus023_e001, "CUS-023 E001 closure"),
        (old_cus007_s2, new_cus007_s2, "CUS-007 step 2 jump to E001"),
        (old_cus007_e001, new_cus007_e001, "CUS-007 E001 closure"),
        (old_cus013_post, new_cus013_post, "CUS-013 postconditions CUS-018 ref"),
        (old_cus013_e002, new_cus013_e002, "CUS-013 E002 closure"),
        (old_cus018_meta, new_cus018_meta, "CUS-018 metadata CUS-014 refs"),
        (old_cus018_e002, new_cus018_e002, "CUS-018 E002 closure & CUS-014 refs"),
        (old_cus019_s2, new_cus019_s2, "CUS-019 step 2 jump to E001"),
        (old_cus019_e001, new_cus019_e001, "CUS-019 E001 closure"),
        (old_cus022_e002, new_cus022_e002, "CUS-022 E002 closure"),
    ]

    for old_val, new_val, label in replacements:
        if old_val not in content:
            print(f"ERROR: Could not find target chunk for {label} in {filepath}!")
            return False
        content = content.replace(old_val, new_val, 1)
        print(f"Applied patch: {label}")

    # Add auto-injection logic to tools/build_srs_narratives.py main
    injection_code = '''
def inject_into_srs(filepath, section_content):
    print(f"Injecting Section 6.2.3 into {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        doc = f.read()
    
    m_start = re.search(r'## 6\\.2\\.3\\.?\\s+Escenarios de Casos de Uso', doc)
    m_next = re.search(r'#+\\s+6\\.3\\.?\\s+Modelo L[oó]gico', doc)
    if not m_start or not m_next:
        raise RuntimeError(f"Could not find section 6.2.3 or 6.3 in {filepath}")
        
    replacement = section_content.rstrip() + "\\n\\n---\\n\\n"
    new_doc = doc[:m_start.start()] + replacement + doc[m_next.start():]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_doc)
    print(f"Successfully injected into {filepath} ({len(new_doc)} chars)")

if __name__ == "__main__":
    import re
    full_sec = generate_full_section()
    print(f"Generated {len(full_sec)} characters of Section 6.2.3")
    
    # 1. Save to standalone markdown
    with open("docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md", "w", encoding="utf-8") as f:
        f.write(full_sec)
    print("Saved to docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md")

    # 2. Inject into docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md
    inject_into_srs("docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md", full_sec)

    # 3. Inject into docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
    inject_into_srs("docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md", full_sec)
'''

    # Replace the existing if __name__ == '__main__': block in tools/build_srs_narratives.py
    main_pat = r'if __name__ == "__main__":.*'
    content = re.sub(main_pat, lambda m: injection_code.strip(), content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully updated {filepath}")
    return True

if __name__ == "__main__":
    ok = patch_build_script()
    if not ok:
        exit(1)
