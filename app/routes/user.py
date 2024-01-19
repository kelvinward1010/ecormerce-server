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

@router.put("/update_user_follow_token/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id, user: models.User, current_user = Depends(oauth2.get_current_user)):
    
    find_user_check_owner = database.collection_users.find_one({"_id": ObjectId(id)})
    
    if not find_user_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to update!")
    
    if str(find_user_check_owner['_id']) != str(current_user['id']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to updated!")
    else:
        hashed_password = utils.has_password(user.password)
        user.password = hashed_password
        
        database.collection_users.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(user)
        })
    
    user_after_update = database.collection_users.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_user(user_after_update)}