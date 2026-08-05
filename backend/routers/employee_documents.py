from fastapi import APIRouter, Depends, UploadFile, File, Form

from backend.auth import verify_token
from backend.services import employee_document_service

router = APIRouter(
    tags=["Employee Documents"]
)


@router.post("/employee/documents/upload")
async def upload_document(
    document_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):
    return employee_document_service.upload_document(
        current_user=current_user,
        document_type=document_type,
        file=file
    )


@router.get("/employee/documents")
def get_my_documents(
    current_user: str = Depends(verify_token)
):
    return employee_document_service.get_my_documents(
        current_user
    )

# ==========================================
# Admin - View All Documents
# ==========================================

@router.get("/admin/documents")
def all_documents():

    return employee_document_service.get_all_documents()


# ==========================================
# Admin - Approve
# ==========================================

@router.put("/admin/documents/{document_id}/approve")
def approve(document_id: int):

    return employee_document_service.approve_document(
        document_id
    )


# ==========================================
# Admin - Reject
# ==========================================

@router.put("/admin/documents/{document_id}/reject")
def reject(document_id: int):

    return employee_document_service.reject_document(
        document_id
    )
# ==========================================
# Delete Document
# ==========================================

@router.delete("/employee/documents/{document_id}")
def delete_document(document_id: int):

    return employee_document_service.delete_document(
        document_id
    )