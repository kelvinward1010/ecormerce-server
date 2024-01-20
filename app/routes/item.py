from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, database, utils, schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.get("/get_all")
async def get_items():
    items = schemas.list_items(database.collection_items.find())
    return items

@router.get("/search")
async def get_search_items(search):
    myquery_name = { "name": { "$regex": search }}
    items_query_title = schemas.list_items(database.collection_items.find(myquery_name))
    return items_query_title