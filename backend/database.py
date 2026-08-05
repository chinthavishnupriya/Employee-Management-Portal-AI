from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL Database URL
DATABASE_URL = "postgresql://postgres:Cpriya%2310*@localhost:5432/employee_management"

# Database Engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()
