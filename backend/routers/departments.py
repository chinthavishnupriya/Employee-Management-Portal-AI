from fastapi import APIRouter, Depends

from backend.schemas import DepartmentCreate
from backend.auth import verify_admin, verify_token
from backend.models import User
from backend.services import department_service

router = APIRouter(
    tags=["Departments"]
)


# ==========================
# Create Department
# ==========================
@router.post("/departments")
def create_department(
    department: DepartmentCreate,
    admin: User = Depends(verify_admin)
):
    return department_service.create_department(department)


# ==========================
# Get All Departments
# ==========================
@router.get("/departments")
def get_departments(
    current_user: str = Depends(verify_token)
):
    return department_service.get_departments()


# ==========================
# Update Department
# ==========================
@router.put("/departments/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentCreate,
    admin: User = Depends(verify_admin)
):
    return department_service.update_department(
        department_id,
        department
    )


# ==========================
# Delete Department
# ==========================
@router.delete("/departments/{department_id}")
def delete_department(
    department_id: int,
    admin: User = Depends(verify_admin)
):
    return department_service.delete_department(department_id)