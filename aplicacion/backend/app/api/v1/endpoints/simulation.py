from typing import Any

from fastapi import APIRouter, status

from app.services.simulation_service import SimulationService

router = APIRouter()


@router.get(
    "/benchmark",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Ejecutar testbench de evaluación de Precision@k y latencias RNF03 (T-45 / RF06)",
)
def run_simulation_benchmark() -> dict[str, Any]:
    """
    Ejecuta el banco de pruebas algorítmico y retorna Precision@3, Precision@5,
    latencias por inferencia y validación de determinismo y casos frontera.
    """
    return SimulationService.run_benchmark()
