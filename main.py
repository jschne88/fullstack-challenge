from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db import models, crud, database, schemas
import bcrypt
import jwt


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/login", response_model=schemas.User)
def login_user(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db) ):
    db_user = crud.login_user(db, user=user)
    if db_user:
        encoded_jwt = jwt.encode({"userId": db_user.id}, "secret", algorithm="HS256")
        response.set_cookie(key="access_token", value=encoded_jwt)
        return db_user
        
    raise HTTPException(status_code=400, detail="Incorrect email or password")
