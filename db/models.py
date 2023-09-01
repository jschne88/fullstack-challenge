from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, name="Full Address")
    class_description = Column(String, name="CLASS_DESCRIPTION")
    estimated_market_value = Column(Integer, name="ESTIMATED_MARKET_VALUE")
    bldg_use = Column(String, name="BLDG_USE")
    bldg_sq_ft = Column(Integer, name="BUILDING_SQ_FT")

class UserProperty(Base):
    __tablename__ = "user_properties"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))

    property = relationship("Property")
