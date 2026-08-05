from backend.database import SessionLocal
from backend.models import User
from backend.auth import hash_password

db = SessionLocal()

email = "shyam@gmail.com"
new_password = "123456"

user = db.query(User).filter(User.email == email).first()

if user:
    user.password = hash_password(new_password)
    db.commit()
    print("Password reset successful!")
    print(f"Email: {email}")
    print(f"New Password: {new_password}")
else:
    print("User not found!")

db.close()