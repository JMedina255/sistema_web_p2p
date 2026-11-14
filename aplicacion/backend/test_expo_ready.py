import json
import urllib.request
import urllib.parse
from app.core.security import create_access_token

BASE = 'http://127.0.0.1:8000/api/v1'

def check(name, path, params=None, token_user=None, token_roles=None):
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {}
    if token_user:
        token = create_access_token({"sub": token_user, "roles": token_roles or ["mentoreado"]})
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            count = len(data) if isinstance(data, list) else len(data.keys())
            print(f"[OK] {name}: HTTP {resp.status} (elements/keys: {count})")
            if isinstance(data, dict):
                if 'horas_visadas' in data:
                    print(f"     -> Horas Visadas: {data.get('horas_visadas')} | Horas Provisionales: {data.get('horas_provisionales')}")
                if 'codigo_folio' in data.get('constancia_emitida', {}):
                    print(f"     -> Folio Oficial: {data['constancia_emitida']['codigo_folio']}")
            elif isinstance(data, list) and len(data) > 0:
                for idx, item in enumerate(data[:4], 1):
                    if 'codigo_reserva' in item:
                        print(f"     -> Reserva [{item.get('codigo_reserva')}]: {item.get('codigo_sesion')} | {item.get('estado')} | {item.get('asignatura_nombre')}")
                    elif 'codigo_sesion' in item:
                        print(f"     -> Sesion [{item.get('codigo_sesion')}]: {item.get('estado')} | {item.get('fecha_inicio')}")
                    elif 'id_demanda' in item:
                        print(f"     -> Demanda [{item.get('id_demanda')}]: {item.get('asignatura_nombre')} ({item.get('tema_nombre')}) - {item.get('estado')}")
    except urllib.error.HTTPError as e:
        print(f"[ERR] {name}: HTTP {e.code} -> {e.read().decode('utf-8')[:200]}")
    except Exception as e:
        print(f"[ERR] {name}: Exception -> {e}")

if __name__ == "__main__":
    print("==================================================================")
    print("      VERIFICACION INTEGRAL DE DATOS PARA DEMOSTRACION (EXPO)    ")
    print("==================================================================")
    check("1. Cursos del Plan de Estudios", "/curriculum/courses")
    check("2. Recomendaciones Top-k para Mentoreado", "/recommendations/offers", {"mentee_email": "ra2022073504@virtual.upt.pe", "top_k": 5})
    check("3. Banco Institucional de Demandas (RF07)", "/bookings/requests")
    check("4. Reservas del Mentoreado ra2022073504@virtual.upt.pe", "/bookings/my-reservations", 
          token_user="ra2022073504@virtual.upt.pe", token_roles=["mentoreado", "mentor"])
    check("5. Catálogo de Ofertas del Mentor mentor.avanzado@upt.pe", "/offers", {"mentor_email": "mentor.avanzado@upt.pe"})
    check("6. Resumen de Certificación del Mentor (>= 20h)", "/certificates/summary", 
          params={"mentor_email": "mentor.avanzado@upt.pe"},
          token_user="mentor.avanzado@upt.pe", token_roles=["mentor"])
