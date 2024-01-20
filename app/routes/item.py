from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, database, utils, schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/item",
    tags=["Item"]
)

@router.get("/get_all")
async def get_items():
    items = schemas.list_items(database.collection_items.find())
    return items