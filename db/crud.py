from sqlalchemy.orm import Session
import bcrypt

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    db_user = models.User(email=user.email, hashed_password=hashed_password, salt=salt)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        if bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password):
            return db_user
    return None

def get_property_by_id(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()

def add_property_to_user_list(db: Session, property_id: int, user_id: int):
    # db_property = get_property_by_id(db, property_id=property.property_id)
    # if db_property
    db_user_property = models.UserProperty(user_id=user_id, property_id=property_id)
    db.add(db_user_property)
    db.commit()
    db.refresh(db_user_property)
    return db_user_property

def get_user_property_list(db: Session, user_id: int):
    return db.query(models.Property).join(models.UserProperty).filter(models.UserProperty.user_id == user_id).all()

def get_property_list(db: Session, q: str | None = None, v: str | None = None, skip: int = 0, limit: int = 100):
    search_map = {
        "address": models.Property.address,
        "class_description": models.Property.class_description,
        "estimated_market_value": models.Property.estimated_market_value,
        "bldg_use": models.Property.bldg_use,
        "bldg_sq_ft": models.Property.bldg_sq_ft
    } 
    if q is not None and v is not None:
        if q in search_map:
            return db.query(models.Property).filter(search_map[q].like(f"%{v}%")).offset(skip).limit(limit).all()
    return db.query(models.Property).limit(limit).all()
