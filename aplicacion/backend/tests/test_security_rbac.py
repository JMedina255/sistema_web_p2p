"""
Suite de Pruebas de Seguridad y Control de Acceso Basado en Roles (RBAC)
========================================================================
Sistema Web P2P de Mentorías Académicas — EPIS UPT.

Cubre exhaustivamente los 18 escenarios de seguridad institucional (SEC-01 a SEC-18)
y los flujos de acceso legítimo previstos en la formalización de la arquitectura.
"""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.security import create_access_token
from app.main import app
from app.services.booking_service import clear_bookings_in_memory
from app.services.offer_service import _memory_offers, clear_offers_in_memory
from app.services.profile_service import set_profile_in_memory
from app.services.role_service import RoleService, clear_user_roles_in_memory

client = TestClient(app)


@pytest.fixture(autouse=True)
def rbac_clean_state():
    """Restaura el estado en memoria antes y después de cada prueba de seguridad."""
    clear_user_roles_in_memory()
    clear_offers_in_memory()
    clear_bookings_in_memory()
    yield
    clear_user_roles_in_memory()
    clear_offers_in_memory()
    clear_bookings_in_memory()


# ==============================================================================
# SEC-01: Petición a endpoint privado sin cabecera Authorization -> 401 Unauthorized
# ==============================================================================
def test_sec_01_private_endpoints_without_authorization_header_rejected_401():
    # 1. Perfiles privados
    res_prof = client.get("/api/v1/profiles/me")
    assert res_prof.status_code == 401
    assert "autenticación" in res_prof.json()["detail"].lower()

    # 2. Disponibilidad horaria
    res_avail = client.get("/api/v1/profiles/availability")
    assert res_avail.status_code == 401

    # 3. Reservas personales
    res_book = client.get("/api/v1/bookings/my-reservations")
    assert res_book.status_code == 401

    # 4. Gestión de roles
    res_roles = client.get("/api/v1/roles/users/2022074255@upt.pe")
    assert res_roles.status_code == 401


# ==============================================================================
# SEC-02: Token JWT malformado o con firma inválida -> 401 Unauthorized
# ==============================================================================
def test_sec_02_malformed_or_tampered_jwt_signature_rejected_401():
    # Token con firma alterada
    tampered_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbHVtbm9AdXB0LnBlIn0.firma_invalida_adulterada"

    res = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {tampered_token}"},
    )
    assert res.status_code == 401
    assert "expirado o inválido" in res.json()["detail"].lower()


# ==============================================================================
# SEC-03: Token JWT expirado -> 401 Unauthorized
# ==============================================================================
def test_sec_03_expired_jwt_rejected_401():
    expired_token = create_access_token(
        data={"sub": "estudiante@upt.pe", "roles": ["mentoreado"]},
        expires_delta=timedelta(minutes=-30),
    )

    res = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert res.status_code == 401
    assert "expirado o inválido" in res.json()["detail"].lower()


# ==============================================================================
# SEC-04: Usuario Mentoreado intenta promover a otro a mentor -> 403 Forbidden
# ==============================================================================
def test_sec_04_mentee_attempts_to_promote_another_student_forbidden_403():
    mentee_token = create_access_token(
        data={"sub": "2024071111@upt.pe", "roles": ["mentoreado"]}
    )

    res = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": "2021088888@upt.pe"},
        headers={"Authorization": f"Bearer {mentee_token}"},
    )
    assert res.status_code == 403
    assert "administrador" in res.json()["detail"].lower()


# ==============================================================================
# SEC-05: Correo con prefijo o subcadena 'admin' sin rol asignado -> 403 Forbidden
# ==============================================================================
def test_sec_05_admin_substring_or_prefix_without_role_forbidden_403():
    # Correo engañoso con prefijo 'admin' pero sin rol administrador
    fake_admin_email = "admin.estudiante.falso@upt.pe"
    fake_token = create_access_token(
        data={"sub": fake_admin_email, "roles": ["mentoreado"]}
    )

    res = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": "2021088888@upt.pe"},
        headers={"Authorization": f"Bearer {fake_token}"},
    )
    assert res.status_code == 403
    assert "administrador" in res.json()["detail"].lower()


# ==============================================================================
# SEC-06: Mentoreado intenta consultar reservas de otro estudiante -> 403 Forbidden
# ==============================================================================
def test_sec_06_mentee_attempts_to_read_another_student_reservations_forbidden_403():
    student_a_token = create_access_token(
        data={"sub": "alumno_a@upt.pe", "roles": ["mentoreado"]}
    )

    res = client.get(
        "/api/v1/bookings/my-reservations?student_email=alumno_b@upt.pe",
        headers={"Authorization": f"Bearer {student_a_token}"},
    )
    assert res.status_code == 403
    assert "violación de autorización" in res.json()["detail"].lower()


# ==============================================================================
# SEC-07: Mentoreado intenta modificar perfil de otro estudiante -> 403 Forbidden
# ==============================================================================
def test_sec_07_mentee_attempts_to_update_another_profile_forbidden_403():
    student_a_token = create_access_token(
        data={"sub": "alumno_a@upt.pe", "roles": ["mentoreado"]}
    )

    payload = {
        "email": "alumno_b@upt.pe",
        "ciclo_actual": 5,
        "rol_postulacion": "mentoreado",
        "biografia": "Suplantación maliciosa",
    }
    res = client.put(
        "/api/v1/profiles/me",
        json=payload,
        headers={"Authorization": f"Bearer {student_a_token}"},
    )
    assert res.status_code == 403
    assert "violación de autorización" in res.json()["detail"].lower()


# ==============================================================================
# SEC-08: Mentor intenta modificar oferta/sesión de otro mentor -> 403 Forbidden
# ==============================================================================
def test_sec_08_mentor_attempts_to_modify_another_mentor_session_forbidden_403():
    mentor_a = "mentor_a@upt.pe"
    mentor_b = "mentor_b@upt.pe"
    token_mentor_a = create_access_token(
        data={"sub": mentor_a, "roles": ["mentor", "mentoreado"]}
    )

    # Sesión propiedad del mentor B
    _memory_offers.append(
        {
            "id_sesion": 8801,
            "codigo_sesion": "SES-8801",
            "mentor_email": mentor_b,
            "estado": "QUORUM_INSUFICIENTE",
            "modalidad": "presencial",
            "fecha_inicio": (datetime.now(UTC) + timedelta(hours=10)).isoformat(),
        }
    )

    # Mentor A intenta resolver la contingencia de la sesión del mentor B
    payload = {
        "decision": "PROCEED",
    }
    res = client.post(
        "/api/v1/offers/8801/quorum-decision",
        json=payload,
        headers={"Authorization": f"Bearer {token_mentor_a}"},
    )
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower() or "mentor titular" in res.json()["detail"].lower()


# ==============================================================================
# SEC-09: Usuario no mentor intenta generar QR/token de asistencia -> 403 Forbidden
# ==============================================================================
def test_sec_09_non_mentor_attempts_to_generate_attendance_token_forbidden_403():
    student_token = create_access_token(
        data={"sub": "alumno@upt.pe", "roles": ["mentoreado"]}
    )

    _memory_offers.append(
        {
            "id_sesion": 8802,
            "codigo_sesion": "SES-8802",
            "mentor_email": "mentor.titular@upt.pe",
            "fecha_inicio": datetime.now(UTC).isoformat(),
            "duracion_minutos": 60,
        }
    )

    res = client.get(
        "/api/v1/sessions/8802/attendance/token",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower()


# ==============================================================================
# SEC-10: Usuario no mentor intenta registrar o editar bitácora -> 403 Forbidden
# ==============================================================================
def test_sec_10_non_mentor_attempts_to_create_bitacora_forbidden_403():
    student_token = create_access_token(
        data={"sub": "alumno@upt.pe", "roles": ["mentoreado"]}
    )

    _memory_offers.append(
        {
            "id_sesion": 8803,
            "codigo_sesion": "SES-8803",
            "mentor_email": "mentor.titular@upt.pe",
            "estado": "CONCLUIDA",
            "fecha_inicio": (datetime.now(UTC) - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    payload = {
        "temas_cubiertos": ["Algoritmos de Ordenamiento"],
        "observaciones": "Descripción pedagógica detallada de la sesión académica formativa con más de 50 caracteres.",
        "nivel_dificultad": "Medio",
    }
    res = client.post(
        "/api/v1/sessions/8803/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower() or "mentor" in res.json()["detail"].lower()


# ==============================================================================
# SEC-11: Administrador con rol oficial realiza operación administrativa -> 200 OK
# ==============================================================================
def test_sec_11_official_verified_admin_executes_privileged_operations_200():
    admin_token = create_access_token(
        data={"sub": "admin.epis@upt.pe", "roles": ["administrador"]}
    )

    target_student = "2021071111@upt.pe"
    set_profile_in_memory(target_student, {"ciclo_actual": 8, "email": target_student})

    # 1. Promover estudiante elegible a mentor
    res_promote = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": target_student},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_promote.status_code == 200
    assert res_promote.json()["success"] is True

    # 2. Consultar roles del estudiante promovido
    res_roles = client.get(
        f"/api/v1/roles/users/{target_student}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_roles.status_code == 200
    assert "mentor" in res_roles.json()["roles"]


# ==============================================================================
# SEC-12: Usuario con múltiples roles opera según rol activo sin escalamiento -> 200 OK
# ==============================================================================
def test_sec_12_multi_role_user_operates_within_authorized_claims_200():
    multi_user = "mentor.estudiante@upt.pe"
    token = create_access_token(
        data={"sub": multi_user, "roles": ["mentoreado", "mentor"]}
    )

    # Opera como mentoreado: consulta su propio perfil
    res_me = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_me.status_code == 200
    assert res_me.json()["email"] == multi_user

    # Intento de operación de administrador no asignada -> denegada (sin escalamiento)
    res_escalation = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": "2021088888@upt.pe"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_escalation.status_code == 403


# ==============================================================================
# SEC-13: Suplantación de identidad mediante explicit_email sin JWT -> 401 Unauthorized
# ==============================================================================
def test_sec_13_identity_spoofing_via_explicit_email_without_jwt_rejected_401():
    # Intento de bypass enviando ?email= sin Bearer token
    res = client.get("/api/v1/profiles/me?email=victima@upt.pe")
    assert res.status_code == 401
    assert "autenticación" in res.json()["detail"].lower()


# ==============================================================================
# SEC-14: Operación privilegiada sin JWT en entorno 'development' -> 401 Unauthorized
# ==============================================================================
def test_sec_14_privileged_operation_without_jwt_in_development_env_rejected_401(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")

    # Acceso a endpoint sin cabecera en desarrollo no admite bypass
    res = client.get("/api/v1/profiles/me")
    assert res.status_code == 401

    res_post = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": "2021088888@upt.pe"},
    )
    assert res_post.status_code == 401


# ==============================================================================
# SEC-15: Usuario cuyo rol fue revocado intenta operación del rol revocado -> 403 Forbidden
# ==============================================================================
def test_sec_15_revoked_role_user_denied_privileged_actions_403():
    student_email = "2021055555@upt.pe"
    admin_token = create_access_token(
        data={"sub": "admin.epis@upt.pe", "roles": ["administrador"]}
    )

    # 1. Asegurar rol inicial en RoleService
    set_profile_in_memory(student_email, {"ciclo_actual": 8, "email": student_email})
    RoleService.promote_to_mentor(None, student_email, "admin")
    assert "mentor" in RoleService.get_user_roles(None, student_email)

    # 2. Administrador revoca el rol de mentor
    res_revoke = client.post(
        "/api/v1/roles/revoke-mentor",
        json={"email": student_email},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_revoke.status_code == 200
    assert "mentor" not in res_revoke.json()["roles"]

    # 3. El usuario ahora solo emite token como mentoreado e intenta registrar bitácora
    demoted_token = create_access_token(
        data={"sub": student_email, "roles": ["mentoreado"]}
    )
    # En memoria, RoleService ya no tiene 'mentor'
    # Intentar publicar con token que carece del claim verificado de mentor
    _memory_offers.append(
        {
            "id_sesion": 8804,
            "codigo_sesion": "SES-8804",
            "mentor_email": "otro@upt.pe",
            "estado": "CONCLUIDA",
            "fecha_inicio": (datetime.now(UTC) - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    res_bitacora = client.post(
        "/api/v1/sessions/8804/bitacora",
        json={
            "temas_cubiertos": ["Tema 1"],
            "observaciones": "Texto de prueba de más de 50 caracteres para la validación de la bitácora.",
            "nivel_dificultad": "Medio",
        },
        headers={"Authorization": f"Bearer {demoted_token}"},
    )
    assert res_bitacora.status_code == 403


# ==============================================================================
# SEC-16: Token simulado o mock rechazado por API real -> 401 Unauthorized
# ==============================================================================
def test_sec_16_mock_simulated_token_rejected_by_api_401():
    mock_token = "mock.eyJzdWIiOiJhZG1pbi5lcGlzQHVwdC5wZSIsInJvbGVzIjpbImFkbWluaXN0cmFkb3IiXX0.sig"

    res = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {mock_token}"},
    )
    assert res.status_code == 401
    assert "expirado o inválido" in res.json()["detail"].lower()


# ==============================================================================
# SEC-17: Fallo o indisponibilidad de Supabase no otorga roles privilegiados
# ==============================================================================
def test_sec_17_db_failure_does_not_grant_privileged_roles():
    unknown_email = "estudiante.nuevo@upt.pe"

    # Con sesión db=None (simulando desconexión de BD)
    roles = RoleService.get_user_roles(db=None, email=unknown_email)
    assert roles == ["mentoreado"]
    assert "administrador" not in roles
    assert "mentor" not in roles


# ==============================================================================
# SEC-18: Usuario sin consentimiento aceptado (RN-02) restringido según normativa
# ==============================================================================
def test_sec_18_unconsented_user_blocked_from_reservations_rn02():
    unconsented_email = "sin_consentimiento@upt.pe"
    token = create_access_token(
        data={"sub": unconsented_email, "roles": ["mentoreado"]}
    )

    payload = {
        "id_sesion": 1,
        "estudiante_email": unconsented_email,
    }
    # La reserva debe rechazar con 403 por falta de consentimiento informado
    res = client.post(
        "/api/v1/bookings/reserve",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert "consentimiento" in res.json()["detail"].lower() or "rn-02" in res.json()["detail"].lower()


# ==============================================================================
# CASOS DE ACCESO LEGÍTIMO
# ==============================================================================
def test_legitimate_mentee_access_own_resources_200():
    email = "2022074255@upt.pe"
    token = create_access_token(data={"sub": email, "roles": ["mentoreado"]})

    # Consulta su propio perfil
    res_prof = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_prof.status_code == 200
    assert res_prof.json()["email"] == email

    # Consulta sus propias reservas
    res_books = client.get(
        "/api/v1/bookings/my-reservations",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_books.status_code == 200


def test_legitimate_mentor_access_own_session_200():
    mentor_email = "2022073504@upt.pe"
    token = create_access_token(
        data={"sub": mentor_email, "roles": ["mentor", "mentoreado"]}
    )

    _memory_offers.append(
        {
            "id_sesion": 9901,
            "codigo_sesion": "SES-9901",
            "mentor_email": mentor_email,
            "estado": "QUORUM_INSUFICIENTE",
            "modalidad": "presencial",
            "fecha_inicio": (datetime.now(UTC) + timedelta(hours=12)).isoformat(),
        }
    )

    # Mentor resuelve contingencia de su propia sesión
    res = client.post(
        "/api/v1/offers/9901/quorum-decision",
        json={"decision": "PROCEED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["estado_nuevo"] == "CONFIRMADA"


def test_legitimate_admin_cross_profile_access_200():
    admin_token = create_access_token(
        data={"sub": "admin.epis@upt.pe", "roles": ["administrador"]}
    )
    target_student = "2022074255@upt.pe"

    # Administrador consulta perfil de cualquier estudiante
    res = client.get(
        f"/api/v1/profiles/me?email={target_student}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    assert res.json()["email"] == target_student
