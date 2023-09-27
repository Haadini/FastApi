from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'table_name'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    num = Column(Integer)
    user = Column(String(length=5000))
    brand = Column(String(length=5000))
    percentage = Column(Float)
    tag = Column(String(length=5000))