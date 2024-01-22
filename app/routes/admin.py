from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, database, utils, schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


#Users
@router.get("/all_users")
async def get_all_users():
    users = schemas.list_users(database.collection_users.find())
    return users

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: models.User):
    
    user_find_checked = database.collection_users.find_one({"email": user.email})
    
    if user_find_checked:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User have {user.email} already exists!")
    
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    newUser = database.collection_users.insert_one(dict(user, created_at = datetime.utcnow(), updated_at = datetime.now()))
    
    if not newUser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't create user!")
    
    user_after_created = database.collection_users.find_one({"_id": ObjectId(newUser.inserted_id)})
    
    return schemas.initial_user(user_after_created)

@router.delete("/delete_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(id):
    
    find_user_delete = database.collection_users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not find_user_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id}")
    
    return {"Message": f"Delete successfully with id {id}"}



#Items
@router.get("/all_items")
async def get_all_items():
    items = schemas.list_items(database.collection_items.find())
    return items

@router.post("/create_item", status_code=status.HTTP_201_CREATED)
async def create_item(item: models.Item):
    newItem = database.collection_items.insert_one(dict(item, created_at = datetime.utcnow(), updated_at = datetime.now()))
    
    item_after_created = database.collection_items.find_one({"_id": ObjectId(newItem.inserted_id)})
    
    return {"data": schemas.initial_item(item_after_created), "Message": "Created successfully!!!", }

@router.put("/update_item/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_item(id, item: models.Item):
    
    find_and_update = database.collection_items.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(item)
    })
    
    if not find_and_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    after_update = database.collection_items.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_item(after_update)}

@router.delete("/delete_item/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_item(id):
    find_delete = database.collection_items.find_one_and_delete({"_id": ObjectId(id)})
    
    if not find_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": f"Delete successfully with id {id}"}