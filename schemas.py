from pydantic import BaseModel, EmailStr
from datetime import date

class RegisterModel(BaseModel):
    email: EmailStr
    password: str

class TaskBase(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    priority: str
    status: str

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True