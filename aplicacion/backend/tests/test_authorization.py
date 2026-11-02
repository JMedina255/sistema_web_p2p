from datetime import timedelta

from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app
from app.services.profile_service import set_profile_in_memory

client = TestClient(app)


def test_authorization_header_valid_jwt_access():
    email = "2022074255@upt.pe"
    token = create_access_token({"sub": email, "roles": ["mentoreado"]})

    response = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email


def test_authorization_expired_or_invalid_jwt_rejected():
    # Token con firma adulterada
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.payload"

    response = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )
    assert response.status_code == 401
    assert "expirado o inválido" in response.json()["detail"]


def test_authorization_expired_token_rejected():
    email = "2022074255@upt.pe"
    # Token expirado hace 10 minutos
    expired_token = create_access_token(
        {"sub": email, "roles": ["mentoreado"]},
        expires_delta=timedelta(minutes=-10),
    )

    response = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401


def test_user_cannot_access_or_modify_another_users_profile_forbidden():
    email_user1 = "estudiante1@upt.pe"
    email_user2 = "estudiante2@upt.pe"
    token_user1 = create_access_token({"sub": email_user1, "roles": ["mentoreado"]})

    # 1. Intento de lectura no autorizada del perfil de otro usuario
    res_get = client.get(
        f"/api/v1/profiles/me?email={email_user2}",
        headers={"Authorization": f"Bearer {token_user1}"},
    )
    assert res_get.status_code == 403
    assert "Violación de autorización" in res_get.json()["detail"]

    # 2. Intento de modificación no autorizada del perfil de otro usuario
    payload_profile = {
        "email": email_user2,
        "ciclo_actual": 4,
        "rol_postulacion": "mentoreado",
        "biografia": "Modificación no autorizada",
    }
    res_put_prof = client.put(
        "/api/v1/profiles/me",
        json=payload_profile,
        headers={"Authorization": f"Bearer {token_user1}"},
    )
    assert res_put_prof.status_code == 403
    assert "Violación de autorización" in res_put_prof.json()["detail"]

    # 3. Intento de modificación no autorizada de la disponibilidad de otro usuario
    payload_avail = {
        "email": email_user2,
        "slots": [{"dia_semana": 1, "hora_inicio": "08:00", "hora_fin": "09:00"}],
    }
    res_put_avail = client.put(
        "/api/v1/profiles/availability",
        json=payload_avail,
        headers={"Authorization": f"Bearer {token_user1}"},
    )
    assert res_put_avail.status_code == 403
    assert "Violación de autorización" in res_put_avail.json()["detail"]


def test_denial_of_self_promotion_to_mentor_without_admin():
    student_email = "2021099999@upt.pe"
    token_student = create_access_token({"sub": student_email, "roles": ["mentoreado"]})

    # El estudiante normal intenta autopromoverse pasando su propio token
    response = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": student_email},
        headers={"Authorization": f"Bearer {token_student}"},
    )
    assert response.status_code == 403
    assert "autopromoción al rol de mentor no está permitida" in response.json()["detail"]


def test_admin_can_promote_and_access():
    admin_email = "admin@upt.pe"
    token_admin = create_access_token({"sub": admin_email, "roles": ["administrador"]})

    target_student = "2021077777@upt.pe"
    set_profile_in_memory(target_student, {"ciclo_actual": 8, "email": target_student})

    # 1. Administrador consulta perfil de otro usuario
    res_admin_get = client.get(
        f"/api/v1/profiles/me?email={target_student}",
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert res_admin_get.status_code == 200

    # 2. Administrador promueve al estudiante a mentor
    res_promote = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": target_student},
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert res_promote.status_code == 200
    assert res_promote.json()["success"] is True
    assert "mentor" in res_promote.json()["roles"]


def test_unauthenticated_request_rejected_without_email_or_token():
    response = client.get("/api/v1/profiles/me")
    assert response.status_code == 401
    assert "Se requiere autenticación" in response.json()["detail"]


def test_admin_can_update_other_profile_and_revoke_with_token():
    admin_email = "admin@upt.pe"
    token_admin = create_access_token({"sub": admin_email, "roles": ["administrador"]})
    target_student = "2021077777@upt.pe"

    # Admin actualiza perfil de otro estudiante
    up_res = client.put(
        "/api/v1/profiles/me",
        json={
            "email": target_student,
            "ciclo_actual": 8,
            "rol_postulacion": "mentor",
            "biografia": "Actualizado por admin",
        },
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert up_res.status_code == 200
    assert up_res.json()["biografia"] == "Actualizado por admin"

    # Admin revoca rol de mentor con Bearer token
    revoke_res = client.post(
        "/api/v1/roles/revoke-mentor",
        json={"email": target_student},
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert revoke_res.status_code == 200
    assert "mentor" not in revoke_res.json()["roles"]


def test_token_without_subject_rejected():
    token_no_sub = create_access_token({"roles": ["mentoreado"]})
    res = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token_no_sub}"},
    )
    assert res.status_code == 401
    assert "identidad de usuario válida" in res.json()["detail"]


def test_malformed_authorization_header_rejected():
    res = client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": "TokenNotBearer 12345"},
    )
    assert res.status_code == 401
    assert "Formato de cabecera Authorization inválido" in res.json()["detail"]


def test_production_unauthenticated_request_rejected(monkeypatch):
    from app.core.config import settings

    # Simular entorno de producción
    monkeypatch.setattr(settings, "APP_ENV", "production")

    # Intento de acceso a profiles sin token
    res = client.get("/api/v1/profiles/me?email=estudiante@upt.pe")
    assert res.status_code == 401
    assert "entornos de producción se requiere cabecera Authorization" in res.json()["detail"]

    # Intento de promover mentor en producción sin token
    res_promote = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": "estudiante@upt.pe"},
    )
    assert res_promote.status_code == 401
    assert "Se requiere autenticación" in res_promote.json()["detail"]

    # Intento de reservar en producción sin token
    res_reserve = client.post(
        "/api/v1/bookings/reserve",
        json={"id_sesion": 1, "estudiante_email": "estudiante@upt.pe"},
    )
    assert res_reserve.status_code == 401
    assert "entornos de producción se requiere cabecera Authorization" in res_reserve.json()["detail"]

    # Intento de ratificar asistencia en producción sin token
    res_confirm = client.post("/api/v1/bookings/1/confirm")
    assert res_confirm.status_code == 401
    assert "Authorization: Bearer <token>" in res_confirm.json()["detail"]

    # Intento de desistir en producción sin token
    res_cancel = client.post("/api/v1/bookings/1/cancel")
    assert res_cancel.status_code == 401
    assert "Authorization: Bearer <token>" in res_cancel.json()["detail"]


def test_reserve_booking_admin_substring_in_email_does_not_grant_admin_privileges():
    """Valida que un correo que contenga la subcadena 'admin' no obtenga privilegios ilegítimos."""
    fake_admin_email = "admin_student@upt.pe"
    victim_email = "victima2026@upt.pe"
    token = create_access_token({"sub": fake_admin_email, "roles": ["mentoreado"]})

    res = client.post(
        "/api/v1/bookings/reserve",
        headers={"Authorization": f"Bearer {token}"},
        json={"id_sesion": 1, "estudiante_email": victim_email},
    )
    assert res.status_code == 403
    assert "no tiene permisos" in res.json()["detail"] or "No tiene autorización" in res.json()["detail"]


def test_reserve_booking_with_verified_admin_role_permits_override():
    """Valida que un usuario con claim verificado 'administrador' pueda reservar para un estudiante."""
    admin_email = "coordinador.epis@upt.pe"
    target_student = "2023078888@upt.pe"
    token_admin = create_access_token({"sub": admin_email, "roles": ["administrador"]})

    res = client.post(
        "/api/v1/bookings/reserve",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={"id_sesion": 1, "estudiante_email": target_student},
    )
    assert res.status_code == 201
    assert res.json()["estudiante_email"] == target_student


def test_reserve_booking_unauthenticated_different_student_rejected_403():
    """Valida que un solicitante sin token no pueda reservar a nombre de otro estudiante usando student_email."""
    res = client.post(
        "/api/v1/bookings/reserve?student_email=atacante@upt.pe",
        json={"id_sesion": 1, "estudiante_email": "victima2026@upt.pe"},
    )
    assert res.status_code == 403
    assert "No tiene autorización" in res.json()["detail"] or "no tiene permisos" in res.json()["detail"]


def test_confirm_attendance_admin_override_permitted():
    """Valida que un administrador autenticado pueda ratificar la asistencia de cualquier estudiante."""
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import _memory_bookings

    now = datetime.now(UTC)
    student = "estudiante_confirm_admin@upt.pe"
    _memory_bookings.append(
        {
            "id_reserva": 709,
            "codigo_reserva": "RES-MEM-709",
            "id_sesion": 1,
            "estudiante_email": student,
            "estado": "PENDIENTE_CONFIRMACION",
            "fecha_reserva": (now - timedelta(hours=2)).isoformat(),
            "fecha_inicio": (now + timedelta(hours=48)).isoformat(),
        }
    )

    admin_token = create_access_token({"sub": "admin.coordinador@upt.pe", "roles": ["administrador"]})
    res = client.post(
        "/api/v1/bookings/709/confirm",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    assert res.json()["estado"] == "CONFIRMADA"
    assert res.json()["fecha_ratificacion"] is not None


def test_confirm_attendance_invalid_id_zero_or_negative_400():
    """Valida que identificadores de reserva no positivos sean rechazados con 400 Bad Request."""
    token = create_access_token({"sub": "estudiante@upt.pe", "roles": ["mentoreado"]})
    res_zero = client.post("/api/v1/bookings/0/confirm", headers={"Authorization": f"Bearer {token}"})
    assert res_zero.status_code == 400
    assert "VALIDATION_ERROR" in res_zero.json()["detail"]

    res_neg = client.post("/api/v1/bookings/-5/confirm", headers={"Authorization": f"Bearer {token}"})
    assert res_neg.status_code == 400
    assert "VALIDATION_ERROR" in res_neg.json()["detail"]


def test_cancel_reservation_invalid_id_zero_or_negative_400():
    """Valida que identificadores de reserva no positivos sean rechazados con 400 Bad Request en cancelación."""
    token = create_access_token({"sub": "estudiante@upt.pe", "roles": ["mentoreado"]})
    res_zero = client.post("/api/v1/bookings/0/cancel", headers={"Authorization": f"Bearer {token}"})
    assert res_zero.status_code == 400
    assert "VALIDATION_ERROR" in res_zero.json()["detail"]

    res_neg = client.post("/api/v1/bookings/-1/cancel", headers={"Authorization": f"Bearer {token}"})
    assert res_neg.status_code == 400
    assert "VALIDATION_ERROR" in res_neg.json()["detail"]


def test_confirm_attendance_admin_substring_rejected_403():
    """Valida que un correo con 'admin' en la subcadena no pueda ratificar una reserva ajena sin rol de admin."""
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import _memory_bookings

    now = datetime.now(UTC)
    victim = "victima_sub@upt.pe"
    _memory_bookings.append(
        {
            "id_reserva": 710,
            "codigo_reserva": "RES-MEM-710",
            "id_sesion": 1,
            "estudiante_email": victim,
            "estado": "PENDIENTE_CONFIRMACION",
            "fecha_reserva": (now - timedelta(hours=2)).isoformat(),
            "fecha_inicio": (now + timedelta(hours=48)).isoformat(),
        }
    )

    fake_admin_token = create_access_token({"sub": "admin_student@upt.pe", "roles": ["mentoreado"]})
    res = client.post(
        "/api/v1/bookings/710/confirm",
        headers={"Authorization": f"Bearer {fake_admin_token}"},
    )
    assert res.status_code == 403
    assert "FORBIDDEN" in res.json()["detail"]


def test_confirm_attendance_unauthenticated_rejects_401():
    """Valida que un llamado a confirmación sin token ni student_email sea rechazado con 401."""
    res = client.post("/api/v1/bookings/1/confirm")
    assert res.status_code == 401
    assert "Se requiere autenticación" in res.json()["detail"]


def test_cancel_reservation_unauthenticated_rejects_401():
    """Valida que un llamado a desistimiento sin token ni student_email sea rechazado con 401."""
    res = client.post("/api/v1/bookings/1/cancel")
    assert res.status_code == 401
    assert "Se requiere autenticación" in res.json()["detail"]


def test_service_confirm_and_cancel_without_caller_email_rejects_401():
    """Valida que invocar confirm_attendance o cancel_reservation en el servicio sin caller_email lance 401."""
    from datetime import UTC, datetime, timedelta

    import pytest
    from fastapi import HTTPException

    from app.services.booking_service import BookingService, _memory_bookings

    now = datetime.now(UTC)
    _memory_bookings.append(
        {
            "id_reserva": 799,
            "codigo_reserva": "RES-MEM-799",
            "id_sesion": 1,
            "estudiante_email": "estudiante_799@upt.pe",
            "estado": "PENDIENTE_CONFIRMACION",
            "fecha_reserva": (now - timedelta(hours=2)).isoformat(),
            "fecha_inicio": (now + timedelta(hours=48)).isoformat(),
        }
    )

    with pytest.raises(HTTPException) as exc_confirm:
        BookingService.confirm_attendance(db=None, id_reserva=799, caller_email=None, is_admin=False)
    assert exc_confirm.value.status_code == 401
    assert "UNAUTHORIZED" in exc_confirm.value.detail

    with pytest.raises(HTTPException) as exc_cancel:
        BookingService.cancel_reservation(db=None, id_reserva=799, caller_email=None, is_admin=False)
    assert exc_cancel.value.status_code == 401
    assert "UNAUTHORIZED" in exc_cancel.value.detail


def test_service_reserve_seat_admin_override_and_ownership_guards():
    """Valida la autorización a nivel de servicio para reserve_seat con admin override y rechazo 403."""
    import pytest
    from fastapi import HTTPException

    from app.schemas.booking import BookingCreatePayload
    from app.services.booking_service import BookingService

    target_student = "estudiante_directo@upt.pe"
    payload = BookingCreatePayload(id_sesion=1, estudiante_email=target_student)

    # 1. Atacante sin rol admin intentando reservar para target_student
    with pytest.raises(HTTPException) as exc_forbidden:
        BookingService.reserve_seat(
            db=None,
            payload=payload,
            caller_email="atacante@upt.pe",
            is_admin=False,
        )
    assert exc_forbidden.value.status_code == 403
    assert "No tiene autorización" in exc_forbidden.value.detail

    # 2. Administrador verificado reservando directamente para target_student
    res_admin = BookingService.reserve_seat(
        db=None,
        payload=payload,
        caller_email="admin.directo@upt.pe",
        is_admin=True,
    )
    assert res_admin.estudiante_email == target_student
    assert res_admin.estado == "PENDIENTE_CONFIRMACION"
