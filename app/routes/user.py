from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, database, utils, schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def find_user(id):
    user = database.collection_users.find_one({"_id": ObjectId(id)})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id}")
    
    return {"data": schemas.initial_user(user)}

@router.put("/change_password/{id}", status_code=status.HTTP_202_ACCEPTED)
async def change_password(id, user: models.UserChangePassword):
    
    find_user_check_owner = database.collection_users.find_one({"_id": ObjectId(id)})
    user_find = schemas.initial_user(find_user_check_owner)
    
    if not find_user_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to update!")
    elif not utils.verify(user.old_password, user_find.get('password')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Old password not match with your account!")
    else:
        hashed_password = utils.has_password(user.password)
        
        database.collection_users.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(password = hashed_password)
        })
    
    user_after_update = database.collection_users.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_user(user_after_update)}

@router.put("/update_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id, user: models.UserUpdate):
    
    find_user_check_owner = database.collection_users.find_one({"_id": ObjectId(id)})
    
    if not find_user_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to update!")
    else:
        database.collection_users.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(user)
        })
    
    user_after_update = database.collection_users.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_user(user_after_update)}