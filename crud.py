from sqlalchemy.orm import Session
import models, schemas
from auth import hash_password, verify_password

def create_user(db: Session, user: schemas.RegisterModel):
    hashed_pwd = hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def filter_tasks(db: Session, user_id: int, priority: str = None, status: str = None):
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if status:
        query = query.filter(models.Task.status == status)
    return query.all()

def update_task(db: Session, task_id: int, new_task: schemas.TaskCreate, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if db_task:
        for key, value in new_task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
