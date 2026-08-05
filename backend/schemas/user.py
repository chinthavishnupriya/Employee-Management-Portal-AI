from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "Employee"
class UserLogin(BaseModel):
    email: str
    password: str
class ChangePassword(BaseModel):
    current_password: str
    new_password: str