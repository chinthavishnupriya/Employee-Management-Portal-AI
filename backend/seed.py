from backend.database import SessionLocal
from backend.models.user import User
from backend.models.employee import Employee
from backend.auth import hash_password

db = SessionLocal()

try:
    if db.query(User).count() == 0:
        users = [
            User(
                username="admin",
                email="admin@example.com",
                password=hash_password("admin123"),
                role="Admin",
            ),
            User(
                username="shyam",
                email="shyam@gmail.com",
                password=hash_password("123456"),
                role="Employee",
            ),
        ]
        db.add_all(users)
        db.commit()

    if db.query(Employee).count() == 0:
        employees = [
            Employee(
                employee_id="EMP001",
                full_name="Administrator",
                email="admin@example.com",
                department_id=1,
                designation="Administrator",
                salary=100000,
            ),
            Employee(
                employee_id="EMP002",
                full_name="Shyam",
                email="shyam@gmail.com",
                department_id=1,
                designation="Employee",
                salary=50000,
            ),
        ]
        db.add_all(employees)
        db.commit()

    print("Database seeded successfully.")

finally:
    db.close()