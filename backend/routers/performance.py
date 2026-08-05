from fastapi import APIRouter, Depends

from backend.schemas import PerformanceCreate
from backend.auth import verify_admin, verify_token
from backend.models import User
from backend.services import performance_service

router = APIRouter(
    tags=["Performance Management"]
)


# ==========================
# Create Performance Review
# ==========================
@router.post("/performance")
def create_performance(
    performance: PerformanceCreate,
    admin: User = Depends(verify_admin)
):
    return performance_service.create_performance(performance)


@router.get("/performance")
def get_performance(
    current_user: str = Depends(verify_token)
):
    return performance_service.get_performance()


# Put this BEFORE /performance/{employee_id}
@router.get("/performance/me")
def my_performance(
    current_user: str = Depends(verify_token)
):
    return performance_service.get_my_performance(current_user)


@router.get("/performance/{employee_id}")
def get_employee_performance(
    employee_id: int,
    current_user: str = Depends(verify_token)
):
    return performance_service.get_employee_performance(employee_id)


@router.delete("/performance/{review_id}")
def delete_performance(
    review_id: int,
    admin: User = Depends(verify_admin)
):
    return performance_service.delete_performance(review_id)