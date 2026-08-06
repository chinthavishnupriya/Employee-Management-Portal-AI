import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Employee

UPLOAD_FOLDER = "backend/uploads/profile_photos"


async def upload_photo(current_user, photo: UploadFile):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.email == current_user
        ).first()

        if employee is None:
            return {
                "message": "Employee not found"
            }

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        extension = photo.filename.split(".")[-1]

        filename = f"{employee.employee_id}.{extension}"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )
        print("Saving image to:", filepath)
        with open(filepath, "wb") as file:
            file.write(await photo.read())
        print("Saving image to:", filepath)

        with open(filepath, "wb") as file:
            file.write(await photo.read())

        print("Image saved successfully")
        # Save URL, NOT filesystem path
        employee.profile_photo = f"/uploads/profile_photos/{filename}"

        db.commit()

        return {
            "message": "Profile photo uploaded successfully",
            "photo_path": employee.profile_photo
        }

    finally:
        db.close()