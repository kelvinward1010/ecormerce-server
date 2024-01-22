from fastapi import APIRouter, HTTPException, status
from .. import database, schemas
from bson import ObjectId

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

@router.get("/find_item/{id}")
async def find_item(id):
    item = database.collection_items.find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    return {"data": schemas.initial_item(item)}