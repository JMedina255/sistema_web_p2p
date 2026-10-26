from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.main import app
from app.models.profile import PerfilAcademico
from app.models.roles import Rol, UsuarioRol
from app.services.profile_service import set_profile_in_memory
from app.services.role_service import RoleService

client = TestClient(app)


def test_get_user_roles_default_is_mentoreado():
    email = "2024011111@upt.pe"
    response = client.get(f"/api/v1/roles/users/{email}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert "mentoreado" in data["roles"]


def test_promote_mentor_rejects_when_cycle_below_7_rn03():
    # Estudiante de ciclo 5
    email = "2023055555@upt.pe"
    set_profile_in_memory(email, {"ciclo_actual": 5, "email": email})

    response = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": email, "assigned_by": "sistema@upt.pe"},
    )
    assert response.status_code == 400
    data = response.json()
    # Verificación estricta del código canónico MERIT_RULE_VIOLATION (RN-03)
    assert "MERIT_RULE_VIOLATION" in str(data)


def test_promote_mentor_success_when_cycle_7_or_above():
    # Estudiante de ciclo 8
    email = "2021088888@upt.pe"
    set_profile_in_memory(email, {"ciclo_actual": 8, "email": email})

    response = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": email, "assigned_by": "admin@upt.pe"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["role"] == "mentor"
    assert "mentor" in data["roles"]

    # Verificar consulta de roles
    roles_res = client.get(f"/api/v1/roles/users/{email}")
    assert roles_res.status_code == 200
    assert "mentor" in roles_res.json()["roles"]


def test_revoke_mentor_success():
    email = "2021088888@upt.pe"
    response = client.post(
        "/api/v1/roles/revoke-mentor",
        json={"email": email, "revoked_by": "admin@upt.pe"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "mentor" not in data["roles"]


def test_promote_mentor_rejects_external_email():
    response = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": "externo@yahoo.com"},
    )
    assert response.status_code == 422
    assert "dominio institucional @upt.pe" in response.text


def test_role_service_with_real_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # 1. Sembrar roles
    r_mentoreado = Rol(id_rol=1, nombre_rol="mentoreado", descripcion="Rol mentoreado")
    r_mentor = Rol(id_rol=2, nombre_rol="mentor", descripcion="Rol mentor")
    db.add_all([r_mentoreado, r_mentor])
    db.commit()

    student_low = "2023012345@upt.pe"
    student_high = "2021012345@upt.pe"

    # Perfil con ciclo 4 (no elegible para mentor)
    p_low = PerfilAcademico(
        email=student_low,
        ciclo_actual=4,
        rol_postulacion="mentoreado",
        materias_interes=[],
        temas_seleccionados=[],
    )
    # Perfil con ciclo 9 (elegible para mentor)
    p_high = PerfilAcademico(
        email=student_high,
        ciclo_actual=9,
        rol_postulacion="mentor",
        materias_interes=[],
        temas_seleccionados=[],
    )
    db.add_all([p_low, p_high])
    db.commit()

    # 2. Comprobar rechazo por mérito RN-03 para student_low
    import pytest
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        RoleService.promote_to_mentor(db, student_low, assigned_by="admin@upt.pe")
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == "MERIT_RULE_VIOLATION"

    # 3. Comprobar promoción exitosa para student_high
    res_high = RoleService.promote_to_mentor(db, student_high, assigned_by="admin@upt.pe")
    assert res_high.success is True
    assert "mentor" in res_high.roles

    # Comprobar entidad en BD
    asig = db.query(UsuarioRol).filter(UsuarioRol.email == student_high, UsuarioRol.id_rol == 2).first()
    assert asig is not None
    assert asig.activo is True

    # 4. Revocación
    res_revoke = RoleService.revoke_mentor(db, student_high)
    assert res_revoke.success is True
    assert "mentor" not in res_revoke.roles

    asig_updated = (
        db.query(UsuarioRol).filter(UsuarioRol.email == student_high, UsuarioRol.id_rol == 2).first()
    )
    assert asig_updated.activo is False

    db.close()
    engine.dispose()


def test_promote_and_revoke_with_invalid_token_rejected():
    from app.core.security import create_access_token

    email = "2021088888@upt.pe"

    # Token con firma inválida en promote
    res_promote_inv = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": email},
        headers={"Authorization": "Bearer token_invalido_firma_falsa"},
    )
    assert res_promote_inv.status_code == 401

    # Token malformado (sin Bearer)
    res_promote_bad_hdr = client.post(
        "/api/v1/roles/promote-mentor",
        json={"email": email},
        headers={"Authorization": "Basic 123456"},
    )
    assert res_promote_bad_hdr.status_code == 401

    # Token con firma inválida en revoke
    res_revoke_inv = client.post(
        "/api/v1/roles/revoke-mentor",
        json={"email": email},
        headers={"Authorization": "Bearer token_invalido_firma_falsa"},
    )
    assert res_revoke_inv.status_code == 401

    # Usuario no-admin intentando revocar mentor a otro estudiante
    user_other = "otro@upt.pe"
    token_other = create_access_token({"sub": user_other, "roles": ["mentoreado"]})
    res_cross_revoke = client.post(
        "/api/v1/roles/revoke-mentor",
        json={"email": email},
        headers={"Authorization": f"Bearer {token_other}"},
    )
    assert res_cross_revoke.status_code == 403
