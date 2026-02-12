from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, crud
from auth import create_access_token, decode_access_token
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/register")
def register(user: schemas.RegisterModel, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    crud.create_user(db, user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.create_task(db, task, user.id)

@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_tasks(db, user.id)

@app.get("/tasks/filter", response_model=list[schemas.TaskOut])
def filter_tasks(priority: str = None, status: str = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.filter_tasks(db, user.id, priority, status)

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = crud.update_task(db, task_id, task, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    deleted = crud.delete_task(db, task_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}