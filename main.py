from fastapi import FastAPI, HTTPException, Depends, Query, Request, Header
from sqlalchemy.orm import Session
from databases import Database
from sqlalchemy import create_engine, engine
from schemas import ItemCreate, Item as ItemSchema
from models import Base, Item
from datetime import date
from typing import List, Dict, Any
import requests
import json
import logging

DATABASE_URL = "mysql+mysqlconnector://User:Password@xxx.xx.x.xx:3306/DataBaseName"
database = Database(DATABASE_URL)

app = FastAPI()
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.DEBUG)


@app.on_event("startup")
async def startup_db():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_db():
    await database.disconnect()


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/items/")
def read_items_in_date_range(
        start_date: date = Query(..., description="Start date of the range"),
        end_date: date = Query(..., description="End date of the range"),
        tage: str = Query(..., description="tag"),
        user: str = Query(..., description="User's name"),
        db: Session = Depends(get_db)
):

    db_items = db.query(Item).filter(Item.date >= start_date, Item.date <= end_date, Item.label == label, Item.customer == customer_name).all()
    return db_items


@app.post("/")
def get_items(
        # start_date: date,
        # end_date: date,
        # customers: List[str],
        # labels: List[str]
        # num_parts: int = Query(..., description="List of customer names to filter by"),
        req: Dict[Any, Any] = None,
        access_token: str = Header(None, convert_underscores=False)
):


    db = Session(bind=engine)
    query = db.query(Item)

    if 'start_date' not in req:
        req.setdefault("start_date", "2000-08-17")

    if 'end_date' not in req:
        req.setdefault("end_date", "2090-08-17")

    if 'upper_num' not in req:
        req.setdefault("upper_num", 100000000000000000000000)

    if 'lower_num' not in req:
        req.setdefault("lower_num", -1)

    if 'upper_percentage' not in req:
        req.setdefault("upper_percentage", 1.0000000000)

    if 'lower_percentage' not in req:
        req.setdefault("lower_percentage", 0.00000000000)

    if 'users' not in req:
        all_customers = [user for user, in db.query(Item.user).distinct()]

        req.setdefault("customers", all_customers)

    if 'brands' not in req:
        all_brands = [brand for brand, in db.query(Item.brand).distinct()]
        req.setdefault("brands", all_brands)

    if 'tags' not in req:
        all_tags = [tag for tag, in db.query(Item.label).distinct()]
        req.setdefault("tags", all_tags)

    query = query.filter(Item.num >= req["lower_num"],
                            Item.num <= req["upper_num"],
                            Item.percentage >= req["percentage"],
                            Item.percentage <= req["percentage"],
                            Item.date >= req["start_date"],
                            Item.date <= req["end_date"],
                            Item.brand.in_(req["brands"]),
                            Item.user.in_(req["users"]),
                            Item.tag.in_(req["tags"]))

    items = query.all()
    db.close()
    return items