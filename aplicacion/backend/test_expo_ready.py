from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


def check(name, path, params=None, user=None, roles=None):
    headers = {}
    if user:
        token = create_access_token({"sub": user, "roles": roles or ["mentoreado"]})
        headers["Authorization"] = f"Bearer {token}"
    r = client.get(f"/api/v1{path}", params=params, headers=headers)
    print(f"{name}: HTTP {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        count = len(data) if isinstance(data, list) else len(data.keys())
        print(f"   Total elementos/claves: {count}")
        if isinstance(data, list) and len(data) > 0 and "codigo_reserva" in data[0]:
            for item in data[:4]:
                print(
                    f"   -> Reserva [{item.get('codigo_reserva')}]: {item.get('codigo_sesion')} | {item.get('estado')} | {item.get('asignatura_nombre')}"
                )
        elif isinstance(data, list) and len(data) > 0 and "id_demanda" in data[0]:
            for item in data:
                print(
                    f"   -> Demanda [{item.get('id_demanda')}]: {item.get('estudiante_email')} - {item.get('asignatura_nombre')} ({item.get('estado')})"
                )
        elif isinstance(data, dict) and "horas_visadas" in data:
            print(
                f"   -> Horas Visadas: {data.get('horas_visadas')} | Folio: {data.get('constancia_emitida', {}).get('codigo_folio')}"
            )


if __name__ == "__main__":
    print("==================================================================")
    print("      VERIFICACION INTEGRAL DE DATOS PARA DEMOSTRACION (EXPO)    ")
    print("==================================================================")
    check("1. Cursos del Plan de Estudios", "/curriculum/courses")
    check("2. Banco Institucional de Demandas (RF07)", "/bookings/requests")
    check(
        "3. Reservas Mentoreado Joan Medina",
        "/bookings/my-reservations",
        user="jm2022074255@virtual.upt.pe",
        roles=["mentoreado"],
    )
    check(
        "4. Reservas Mentoreado Renzo Antayhua",
        "/bookings/my-reservations",
        user="ra2022073504@virtual.upt.pe",
        roles=["mentoreado"],
    )
    check(
        "5. Catálogo de Ofertas Mentor Avanzado", "/offers", params={"mentor_email": "mentor.avanzado@upt.pe"}
    )
    check(
        "6. Resumen Certificación Mentor",
        "/certificates/summary",
        params={"mentor_email": "mentor.avanzado@upt.pe"},
        user="mentor.avanzado@upt.pe",
        roles=["mentor"],
    )
