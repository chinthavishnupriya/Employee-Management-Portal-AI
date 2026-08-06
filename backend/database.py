import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# =====================================
# Database URL
# =====================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Cpriya%2310*@localhost:5432/employee_management"
)

print("=" * 70)
print("DATABASE_URL:", DATABASE_URL)
print("=" * 70)

# =====================================
# SQLAlchemy Engine
# =====================================

engine = create_engine(
    DATABASE_URL,
    echo=True,          # Shows SQL queries (for debugging)
    future=True
)

# =====================================
# Session Factory
# =====================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =====================================
# Base Model
# =====================================

Base = declarative_base()


# =====================================
# Dependency (optional but recommended)
# =====================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()