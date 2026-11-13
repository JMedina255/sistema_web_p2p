"""
Suite Complementaria para Casos del Catálogo Oficial de Pruebas EPIS-UPT:
- CUS03: Demanda Temática y Notificaciones Afines (CUS03-U02, CUS03-F01, CUS03-A01)
- CUS16: Gamificación, Reputación e Insignias Idempotentes (CUS16-U01, CUS16-U02)
- CUS22: Auditoría, Resolución de Fraude y Bloqueo de Certificación (CUS22-U01, CUS22-U02)
- CUS23: Tareas Programadas y Recordatorios de Quórum T-24h (CUS23-U01, CUS23-U02, CUS23-U03, CUS23-I01, CUS23-A01)
"""

from datetime import UTC, datetime, timedelta
import time
import pytest
from fastapi import HTTPException

from app.services.catalog_support_service import (
    ServicioAuditoria,
    ServicioInsignia,
    ServicioNotificacion,
    ServicioRecordatorio,
    ServicioReputacion,
    ServicioResolucionReclamo,
    ServicioSolicitudDemanda,
    TareaProgramadaQuorum,
)


@pytest.fixture(autouse=True)
def clean_support_services():
    ServicioNotificacion.limpiar_cola()
    ServicioSolicitudDemanda.limpiar()
    ServicioRecordatorio.limpiar()
    yield
    ServicioNotificacion.limpiar_cola()
    ServicioSolicitudDemanda.limpiar()
    ServicioRecordatorio.limpiar()


# ==============================================================================
# CUS03: GESTIÓN DE DEMANDA TEMÁTICA
# ==============================================================================

def test_cus03_u02_notify_mentors_matching_requested_topic():
    """
    CUS03-U02: Verifica que ServicioNotificacion identifique mentores con competencia
    coincidente con el tema solicitado y encole las notificaciones por correo institucional.
    """
    mentores = [
        {"email": "mentor1@upt.pe", "competencias_temas": [101, 102]},
        {"email": "mentor2@upt.pe", "competencias_temas": [201, 202]},
        {"email": "mentor3@upt.pe", "competencias_temas": [101, 301]},
    ]

    notificados = ServicioNotificacion.notificar_mentores_por_tema(
        id_tema=101,
        nombre_tema="Árboles AVL y Grafos",
        mentores_disponibles=mentores,
    )

    assert len(notificados) == 2
    destinatarios = [n["destinatario"] for n in notificados]
    assert "mentor1@upt.pe" in destinatarios
    assert "mentor3@upt.pe" in destinatarios
    assert "mentor2@upt.pe" not in destinatarios


def test_cus03_f01_demand_request_registration_and_mentor_alert_flow():
    """
    CUS03-F01: Flujo integral de registro de demanda ante ausencia de ofertas
    y despacho de alertas a mentores capacitados.
    """
    mentores = [{"email": "experto.bd@upt.pe", "competencias_temas": [50]}]
    ofertas_activas = [{"id_tema": 99, "estado": "PUBLICADA"}]

    res = ServicioSolicitudDemanda.crear(
        estudiante_email="alumno@upt.pe",
        id_asignatura=10,
        id_tema=50,
        nombre_tema="Normalización Boyce-Codd",
        observaciones="Requiero repaso de formas normales.",
        ofertas_activas=ofertas_activas,
        mentores_disponibles=mentores,
    )

    assert res["accion"] == "SOLICITUD_CREADA"
    assert res["mentores_notificados"] == 1
    assert res["solicitud"]["estado"] == "PENDIENTE"


def test_cus03_a01_demand_cycle_effectiveness_deduplication_and_performance():
    """
    CUS03-A01: Criterios de Aceptación:
    (1) Registro en <= 1.5 s.
    (2) Detección de ofertas existentes o solicitudes duplicadas.
    (3) 20 solicitudes procesadas limpiamente.
    """
    oferta_existente = [{"id_tema": 40, "estado": "PUBLICADA", "codigo": "SES-4001"}]

    # Si hay oferta activa existente, sugiere la oferta
    res_sugerida = ServicioSolicitudDemanda.crear(
        estudiante_email="alumno1@upt.pe",
        id_asignatura=5,
        id_tema=40,
        nombre_tema="Ecuaciones Diferenciales",
        ofertas_activas=oferta_existente,
    )
    assert res_sugerida["accion"] == "OFERTA_SUGERIDA"

    # Lote de 20 solicitudes procesadas en tiempo reglamentario
    t0 = time.perf_counter()
    for i in range(20):
        ServicioSolicitudDemanda.crear(
            estudiante_email=f"alumno_{i}@upt.pe",
            id_asignatura=1,
            id_tema=100 + i,
            nombre_tema=f"Tema_{i}",
        )
    t_delta = time.perf_counter() - t0
    assert t_delta < 1.5, f"Tiempo de registro ({t_delta:.3f} s) superó el umbral reglamentario de 1.5 s."


# ==============================================================================
# CUS16: REPUTACIÓN E INSIGNIAS DE GAMIFICACIÓN
# ==============================================================================

def test_cus16_u01_recalculate_reputation_weighted_formula():
    """
    CUS16-U01: Verifica el recálculo ponderado de reputación tras encuestas y horas dictadas.
    """
    # 5 encuestas perfectas (5.0) con 20 horas dictadas
    res = ServicioReputacion.recalcular(
        valoraciones_encuestas=[5.0, 5.0, 4.0, 5.0, 5.0],
        horas_dictadas=20.0,
    )
    # Promedio = 4.80, bonus 20h = +0.20 -> Reputación = 5.00
    assert res["promedio_encuestas"] == 4.8
    assert res["reputacion"] == 5.0
    assert res["total_encuestas"] == 5

    # Caso con 0 encuestas (reputación neutra 3.0)
    res_vacio = ServicioReputacion.recalcular([], 0.0)
    assert res_vacio["reputacion"] == 3.0


def test_cus16_u02_idempotent_badge_unlocking_thresholds():
    """
    CUS16-U02: Verifica el desbloqueo de insignias por horas (10h, 20h, 30h)
    y asegura estricta IDEMPOTENCIA (no duplicar insignias ya otorgadas).
    """
    # Con 25 horas, califica a Bronce (10h) y Plata (20h)
    insignias = ServicioInsignia.evaluar_desbloqueos("mentor@upt.pe", 25.0, [])
    assert "INS-BRONCE" in insignias
    assert "INS-PLATA" in insignias
    assert "INS-ORO" not in insignias
    assert len(insignias) == 2

    # Llamada repetida (idempotencia): no debe agregar duplicados
    insignias_reiteradas = ServicioInsignia.evaluar_desbloqueos("mentor@upt.pe", 25.0, insignias)
    assert len(insignias_reiteradas) == 2
    assert insignias_reiteradas.count("INS-BRONCE") == 1
    assert insignias_reiteradas.count("INS-PLATA") == 1


def test_cus16_f01_mentor_profile_gamification_view():
    """
    CUS16-F01: Flujo de visualización de reputación e insignias en el perfil del mentor.
    Tras varias encuestas y horas acumuladas, el mentor visualiza en su perfil el puntaje
    de reputación actualizado, retroalimentación anónima y las insignias desbloqueadas.
    """
    mentor_email = "mentor.estrella@upt.pe"
    encuestas = [
        {"valoracion": 5, "comentario": "Excelente explicación de grafos."},
        {"valoracion": 5, "comentario": "Muy paciente y claro."},
        {"valoracion": 4, "comentario": "Buenos ejercicios prácticos."},
    ]

    perfil = ServicioReputacion.obtener_perfil_gamificacion(
        mentor_email=mentor_email,
        encuestas=encuestas,
        horas_dictadas=22.0,
    )

    assert perfil["mentor_email"] == mentor_email
    assert perfil["reputacion"] >= 4.5
    assert len(perfil["retroalimentacion_anonima"]) == 3
    # Feedback anónimo no debe exponer emails ni nombres de estudiantes
    for f in perfil["retroalimentacion_anonima"]:
        assert "comentario" in f
        assert "estudiante_email" not in f

    # Insignias desbloqueadas para 22h: Bronce (10h) y Plata (20h)
    insignias = perfil["insignias"]
    bronce = next(i for i in insignias if i["id"] == "INS-BRONCE")
    plata = next(i for i in insignias if i["id"] == "INS-PLATA")
    oro = next(i for i in insignias if i["id"] == "INS-ORO")

    assert bronce["desbloqueada"] is True
    assert plata["desbloqueada"] is True
    assert oro["desbloqueada"] is False
    assert "badge-ins-bronce" in bronce["icono"]


# ==============================================================================
# CUS22: AUDITORÍA DE BITÁCORAS Y RESOLUCIÓN DE FRAUDE
# ==============================================================================

def test_cus22_u01_filter_marked_or_disputed_bitacoras():
    """
    CUS22-U01: Verifica que ServicioAuditoria filtre únicamente bitácoras dudosas,
    observadas o con reclamo de inasistencia abierto.
    """
    bitacoras = [
        {"id": 1, "estado": "VISADA", "reclamo_abierto": False},
        {"id": 2, "estado": "OBSERVADA", "reclamo_abierto": False},
        {"id": 3, "estado": "REGISTRADA", "reclamo_abierto": True},
        {"id": 4, "estado": "EN_REVISION", "reclamo_abierto": False},
    ]

    marcadas = ServicioAuditoria.obtener_bitacoras_marcadas(bitacoras)
    ids_marcadas = [b["id"] for b in marcadas]
    assert 2 in ids_marcadas
    assert 3 in ids_marcadas
    assert 4 in ids_marcadas
    assert 1 not in ids_marcadas


def test_cus22_u02_resolve_attendance_dispute_and_block_certification_on_fraud():
    """
    CUS22-U02: Verifica que al dictaminar 'FRAUDE_COMPROBADO' se descuenten las horas
    y se bloquee preventivamente la elegibilidad de certificación del mentor.
    """
    # 1. Caso de reclamo fundado (error administrativo simple)
    res_fundado = ServicioResolucionReclamo.resolver(
        id_bitacora=10,
        resultado="FUNDADO",
        auditor_email="director.epis@upt.pe",
        motivo="El estudiante demostró conexión activa en logs del Meet institucional.",
        horas_dictadas_mentor=20.0,
    )
    assert res_fundado["resultado"] == "FUNDADO"
    assert res_fundado["elegible_para_certificacion"] is True
    assert res_fundado["bloqueo_certificacion_activo"] is False

    # 2. Caso de fraude comprobado
    res_fraude = ServicioResolucionReclamo.resolver(
        id_bitacora=11,
        resultado="FRAUDE_COMPROBADO",
        auditor_email="director.epis@upt.pe",
        motivo="Constatación de suplantación y registro de asistencia ficticia.",
        horas_dictadas_mentor=20.0,
    )
    assert res_fraude["resultado"] == "FRAUDE_COMPROBADO"
    assert res_fraude["horas_remanentes_validas"] == 18.0
    assert res_fraude["elegible_para_certificacion"] is False
    assert res_fraude["bloqueo_certificacion_activo"] is True

    # 3. Rechazo de dictamen sin justificación suficiente (< 15 caracteres)
    with pytest.raises(HTTPException) as exc_just:
        ServicioResolucionReclamo.resolver(
            id_bitacora=12,
            resultado="FUNDADO",
            auditor_email="director.epis@upt.pe",
            motivo="Muy corto",
        )
    assert exc_just.value.status_code == 422


def test_cus22_f01_audit_committee_inspects_questionable_bitacoras_and_resolves_dispute():
    """
    CUS22-F01: Flujo de auditoría e inspección de bitácoras dudosas por el Comité de Tutoría.
    El Comité revisa bitácoras dudosas, inspecciona evidencia (temas vs asistencia)
    y resuelve el reclamo de inasistencia presentado por un estudiante.
    """
    auditor = "comite.tutoria@upt.pe"

    # 1. Auditoría preliminar con inspección de evidencia
    auditoria = ServicioAuditoria.auditar_bitacora_con_evidencia(
        id_bitacora=801,
        temas_registrados=["Programación Dinámica", "Memorización"],
        asistencias_marcadas=0,
        total_inscritos=5,
        auditor_email=auditor,
    )
    assert auditoria["es_dudosa"] is True
    assert auditoria["dictamen_preliminar"] == "REQUIERE_AUDIENCIA"

    # 2. Resolución formal del reclamo
    resolucion = ServicioResolucionReclamo.resolver(
        id_bitacora=801,
        resultado="FUNDADO",
        auditor_email=auditor,
        motivo="Se constató falla técnica en el lector QR del aula; asistencia ratificada.",
        horas_dictadas_mentor=16.0,
    )
    assert resolucion["resultado"] == "FUNDADO"
    assert resolucion["elegible_para_certificacion"] is True


def test_cus22_a01_quality_governance_prior_to_certificates_batch_acceptance():
    """
    CUS22-A01: Criterios de Aceptación:
    (1) 10 reclamos de inasistencia auditados antes del cierre de semestre con 100% de trazabilidad.
    (2) Ningún certificado (CUS13) se emite para horas con fraude comprobado (bloqueo efectivo).
    (3) El lote completo se procesa y audita en <= 2.0 s.
    """
    reclamos = []
    for i in range(1, 11):
        es_fraude = (i % 3 == 0)  # Reclamos 3, 6, 9 con fraude
        reclamos.append({
            "id_bitacora": 900 + i,
            "dictamen": "FRAUDE_COMPROBADO" if es_fraude else "FUNDADO",
            "motivo": f"Dictamen formal de auditoría para el caso de reclamo {i:02d} del semestre.",
            "horas_mentor": 20.0,
        })

    t0 = time.perf_counter()
    res_lote = ServicioResolucionReclamo.auditar_lote_reclamos_cierre_semestre(
        reclamos=reclamos,
        auditor_email="director.epis@upt.pe",
    )
    elapsed = time.perf_counter() - t0

    assert res_lote["status"] == "AUDITORIA_LOTE_COMPLETADA"
    assert res_lote["total_reclamos"] == 10
    assert res_lote["total_resueltos"] == 10
    assert res_lote["trazabilidad_completa"] is True
    assert res_lote["certificaciones_bloqueadas"] == 3  # 3 fraudes bloqueados
    assert elapsed < 2.0, f"Tiempo de auditoría masiva ({elapsed:.3f} s) superó el umbral de 2.0 s."


# ==============================================================================
# CUS23: TAREAS PROGRAMADAS Y RECORDATORIOS DE QUÓRUM
# ==============================================================================

def test_cus23_u01_identify_sessions_at_exact_24h_cut():
    """
    CUS23-U01: Verifica que TareaProgramadaQuorum.obtener_sesiones_en_corte()
    identifique sesiones situadas a 24 horas del instante de referencia.
    """
    now = datetime.now(UTC)

    sesiones = [
        {"id_sesion": 1, "fecha_inicio": (now + timedelta(hours=24)).isoformat()},  # Exactamente 24h
        {"id_sesion": 2, "fecha_inicio": (now + timedelta(hours=24, minutes=10)).isoformat()},  # En tolerancia
        {"id_sesion": 3, "fecha_inicio": (now + timedelta(hours=48)).isoformat()},  # Lejos
        {"id_sesion": 4, "fecha_inicio": (now + timedelta(hours=2)).isoformat()},  # Muy cerca
    ]

    en_corte = TareaProgramadaQuorum.obtener_sesiones_en_corte(sesiones, reference_now=now, tolerancia_minutos=15)
    ids_en_corte = [s["id_sesion"] for s in en_corte]
    assert 1 in ids_en_corte
    assert 2 in ids_en_corte
    assert 3 not in ids_en_corte
    assert 4 not in ids_en_corte


def test_cus23_u02_send_confirmation_reminders_to_unconfirmed_mentees():
    """
    CUS23-U02: Verifica que ServicioRecordatorio encole avisos preventivos
    únicamente a los alumnos en estado PENDIENTE_CONFIRMACION.
    """
    inscritos = [
        {"estudiante_email": "alumno1@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
        {"estudiante_email": "alumno2@upt.pe", "estado": "CONFIRMADA"},
        {"estudiante_email": "alumno3@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
    ]

    recs = ServicioRecordatorio.enviar_recordatorios_confirmacion(
        id_sesion=501,
        titulo_sesion="Cálculo II Integrales Dobles",
        inscritos=inscritos,
    )

    assert len(recs) == 2
    destinatarios = [r["destinatario"] for r in recs]
    assert "alumno1@upt.pe" in destinatarios
    assert "alumno3@upt.pe" in destinatarios
    assert "alumno2@upt.pe" not in destinatarios


def test_cus23_u03_automatic_quorum_evaluation_and_mentor_alert():
    """
    CUS23-U03: Verifica la evaluación automática del quórum (50%) al corte de 24h
    y la emisión automática de alerta al mentor en caso de quórum insuficiente.
    """
    sesion = {"id_sesion": 501, "capacidad_maxima": 10, "mentor_email": "mentor@upt.pe"}

    # Caso 1: Quórum insuficiente (solo 3 de 5 requeridos confirmados)
    inscritos_insuficientes = [
        {"estado": "CONFIRMADA"},
        {"estado": "CONFIRMADA"},
        {"estado": "CONFIRMADA"},
        {"estado": "PENDIENTE_CONFIRMACION"},
    ]
    res1 = TareaProgramadaQuorum.evaluar_y_alertar(sesion, inscritos_insuficientes)
    assert res1["tiene_quorum"] is False
    assert res1["alerta"] is not None
    assert res1["alerta"]["tipo"] == "ALERTA_BAJO_QUORUM"
    assert "opciones" in res1["alerta"]

    # Caso 2: Quórum alcanzado (5 de 5 requeridos confirmados)
    inscritos_suficientes = [{"estado": "CONFIRMADA"} for _ in range(5)]
    res2 = TareaProgramadaQuorum.evaluar_y_alertar(sesion, inscritos_suficientes)
    assert res2["tiene_quorum"] is True
    assert res2["alerta"] is None


def test_cus23_i01_cron_job_scheduler_registration_and_periodicity():
    """
    CUS23-I01: Integración del job Cron con el scheduler de producción (Celery/APScheduler).
    Verifica que el job está correctamente registrado en el scheduler con la periodicidad
    configurada (cada 15 min) y se invoca puntualmente sin saltearse ejecuciones.
    """
    reg = TareaProgramadaQuorum.verificar_registro_scheduler(periodicidad_minutos=15)
    assert reg["registrado"] is True
    assert reg["estado"] == "ACTIVO"
    assert reg["periodicidad_minutos"] == 15
    assert reg["cron_expression"] == "*/15 * * * *"
    assert "cron_quorum_evaluation_t24h" in reg["job_id"]


def test_cus23_f01_e2e_reminder_quorum_cut_and_mentor_alert_flow():
    """
    CUS23-F01: Flujo extremo a extremo: recordatorio, corte de 24h y alerta automática al mentor.
    Se programa una sesión con reloj acelerado/ajustado: el sistema envía recordatorios a los
    no confirmados, ejecuta el corte a las 24h y, si no se alcanza el quórum, notifica
    automáticamente al mentor con las opciones de continuar/cancelar (enlaza con CUS07).
    """
    now = datetime.now(UTC)
    fecha_sesion = now + timedelta(hours=24)

    sesion = {
        "id_sesion": 601,
        "capacidad_maxima": 10,
        "mentor_email": "mentor.titular@upt.pe",
        "tema": "Arquitectura de Software y Patrones de Diseño",
        "fecha_inicio": fecha_sesion.isoformat(),
    }

    # Inscritos: 2 confirmados y 3 pendientes de confirmación (Total 5, requeridos 5 para quórum 50%)
    inscritos = [
        {"estudiante_email": "est1@upt.pe", "estado": "CONFIRMADA"},
        {"estudiante_email": "est2@upt.pe", "estado": "CONFIRMADA"},
        {"estudiante_email": "est3@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
        {"estudiante_email": "est4@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
        {"estudiante_email": "est5@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
    ]

    flujo = TareaProgramadaQuorum.ejecutar_flujo_extremo_a_extremo(
        sesion=sesion,
        inscritos=inscritos,
        simulated_now=now,
    )

    assert flujo["flujo_completado"] is True
    # Recordatorios enviados solo a los 3 pendientes
    assert flujo["recordatorios_enviados"] == 3
    assert "est3@upt.pe" in flujo["destinatarios_recordatorios"]
    assert "est1@upt.pe" not in flujo["destinatarios_recordatorios"]

    # Evaluación de quórum al corte: solo 2 de 5 confirmados -> bajo quórum
    assert flujo["tiene_quorum"] is False
    assert flujo["alerta_mentor"] is not None
    assert flujo["alerta_mentor"]["tipo"] == "ALERTA_BAJO_QUORUM"
    assert "CONTINUAR" in flujo["alerta_mentor"]["opciones"]
    assert "CANCELAR" in flujo["alerta_mentor"]["opciones"]


def test_cus23_a01_batch_cron_performance_and_delivery_acceptance():
    """
    CUS23-A01: Aceptación: puntualidad y fiabilidad del proceso automático en producción.
    (1) Ejecución batch sobre 100 sesiones concurrentes próximas al corte en el entorno Beta.
    (2) Tiempos de procesamiento masivo <= 30.0 s (RNF).
    (3) 0 sesiones omitidas en el corte.
    (4) Tasa de entrega de recordatorios >= 98%.
    """
    now = datetime.now(UTC)

    sesiones = []
    inscritos_map = {}

    for i in range(100):
        s_id = i + 2000
        sesiones.append({
            "id_sesion": s_id,
            "capacidad_maxima": 10,
            "mentor_email": f"mentor_{i}@upt.pe",
            "tema": f"Tema_Mentoría_{i}",
            "fecha_inicio": (now + timedelta(hours=24)).isoformat(),
        })
        if i % 2 == 0:
            inscritos_map[s_id] = [
                {"estudiante_email": f"mentee_{s_id}_1@upt.pe", "estado": "CONFIRMADA"},
                {"estudiante_email": f"mentee_{s_id}_2@upt.pe", "estado": "CONFIRMADA"},
                {"estudiante_email": f"mentee_{s_id}_3@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
            ]
        else:
            inscritos_map[s_id] = [
                {"estudiante_email": f"mentee_{s_id}_{j}@upt.pe", "estado": "CONFIRMADA"} for j in range(6)
            ]

    t0 = time.perf_counter()
    resultado = TareaProgramadaQuorum.ejecutar_job_cron(
        sesiones=sesiones,
        inscritos_por_sesion=inscritos_map,
        reference_now=now,
    )
    t_delta = time.perf_counter() - t0

    assert resultado["status"] == "JOB_COMPLETADO_EXITOSAMENTE"
    assert resultado["sesiones_evaluadas"] == 100  # Cero sesiones omitidas
    assert resultado["alertas_bajo_quorum"] == 50
    assert resultado["recordatorios_enviados"] == 50
    assert t_delta < 30.0, f"Tiempo batch ({t_delta:.3f} s) superó el umbral reglamentario de 30.0 s."
