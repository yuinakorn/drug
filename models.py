from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from database import Base


class DrugAllergy(Base):
    __tablename__ = "t_drugallergy"
    cid = Column(String(13), primary_key=True)
    dname = Column(String, primary_key=True)

