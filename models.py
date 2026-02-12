from sqlalchemy import Column, Integer, String, Date
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    priority = Column(String)
    status = Column(String)
    user_id = Column(Integer)