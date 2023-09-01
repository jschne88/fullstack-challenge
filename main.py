from fastapi import FastAPI, Depends, HTTPException, Query, Response, Request
from sqlalchemy.orm import Session
from db import models, crud, database, schemas
import bcrypt
import jwt
import pandas as pd
from sqlalchemy import create_engine

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

xlsx_path = './Enodo_Skills_Assessment_Data_File.xlsx'
df = pd.read_excel(xlsx_path, engine='openpyxl')

if df is not None:
    df.insert(0, 'id', range(1, 1 + len(df)))
    df.to_sql('properties', database.engine, if_exists='replace', index=False)
    print("Data successfully imported to SQLite database using SQLAlchemy!")
else:
    print("Dataframe is empty!")

# Middleware to get user from jwt
@app.middleware("http")
async def get_user_id_from_jwt(request: Request, call_next):
    jwt_token = request.cookies.get("access_token")
    if jwt_token:
        payload = jwt.decode(jwt_token, "secret", algorithms=["HS256"])
        request.state.user_id = payload.get("userId")
    response = await call_next(request)
    return response

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

@app.post("/property/add", response_model=schemas.UserProperty)
def add_property_to_list(property: schemas.UserProperty, request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=400, detail="User not logged in")
    db_property = crud.get_property_by_id(db, property_id=property.property_id)
    if db_property:
        return crud.add_property_to_user_list(db, property_id=property.property_id, user_id=user_id)
    raise HTTPException(status_code=400, detail="Property does not exist")

@app.get("/property/list/user", response_model=list[schemas.Property])
def get_user_property_list(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=400, detail="User not logged in")
    return crud.get_user_property_list(db, user_id=user_id)

@app.get("/property/list", response_model=list[schemas.Property])
def get_property_list(q: str | None = None, v: str | None = None, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_property_list(db, q=q, v=v, skip=skip, limit=limit)
