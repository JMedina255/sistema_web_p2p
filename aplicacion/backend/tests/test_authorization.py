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
