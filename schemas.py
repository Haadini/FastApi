from pydantic import BaseModel
from datetime import date

class ItemCreate(BaseModel):
    date: date
    num: int
    user: str
    brand: str
    percentage: float
    tag: str

class Item(ItemCreate):
    id: int

class Config:
    from_attributes = True