from app.models.auth import AuthChallenge
from app.models.consent import ConsentimientoLegal
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.models.roles import Rol, UsuarioRol

__all__ = [
    "Asignatura",
    "TemaConceptual",
    "AuthChallenge",
    "ConsentimientoLegal",
    "Rol",
    "UsuarioRol",
    "PerfilAcademico",
    "DisponibilidadHoraria",
]
