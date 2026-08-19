from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from backend.routers import home_router
from fastapi.staticfiles import StaticFiles
from backend.routers import employee_documents
from backend.routers import employee_details
from backend.routers import performance
from backend.database import Base, engine
from backend.routers import me
from backend.routers import auth
from backend.routers import users
from backend.routers import employees
from backend.routers import departments
from backend.routers import attendance
from backend.routers import dashboard
from backend.routers import leave
from backend.routers import payroll
from backend.routers import reports
from backend.routers import profile
from backend.routers import onboarding
from backend.routers import offboarding
from backend.routers import employee_profile
from backend.routers import change_password
from backend.routers import profile_photo
import backend.models
from backend.routers.profile_router import router as profile_router
from backend.routers.ai_router import router as ai_router
from backend.routers.resume_router import router as resume_router
from backend.routers.hr_ai_router import router as hr_ai_router
from backend.routers.sentiment_router import router as sentiment_router
# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Employee Management Portal API",
    description="Professional HRMS Backend using FastAPI",
    version="1.0.0"
)
# Create upload folder if it doesn't exist
os.makedirs("backend/uploads/profile_photos", exist_ok=True)

# Serve uploaded profile photos
app.mount(
    "/uploads",
    StaticFiles(directory="backend/uploads"),
    name="uploads"
)
app.mount(
    "/backend/uploads",
    StaticFiles(directory="backend/uploads"),
    name="uploads"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://13.53.158.40:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(home_router.router)
app.include_router(employee_details.router)
# Register all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(attendance.router)
app.include_router(dashboard.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(reports.router)
app.include_router(profile.router)
app.include_router(me.router)
app.include_router(performance.router)
app.include_router(onboarding.router)
app.include_router(offboarding.router)
app.include_router(employee_profile.router)
app.include_router(change_password.router)
app.include_router(profile_router)
app.include_router(employee_documents.router)
app.include_router(ai_router)
app.include_router(profile_photo.router)
app.include_router(resume_router)
app.include_router(hr_ai_router)
app.include_router(sentiment_router)
@app.get("/")
def home():
    return {
        "message": "Employee Management Portal API is Running Successfully 🚀"
    }