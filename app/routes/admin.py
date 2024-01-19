from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, database, utils, schemas, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: models.User):
    
    user_find_checked = database.collection_users.find_one({"email": user.email})
    
    if user_find_checked:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User have {user.email} already exists!")
    
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    user_add = database.collection_users.insert_one(dict(user, created_at = datetime.utcnow(), updated_at = datetime.now()))
    
    if not user_add:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't create user!")
    
    user_after_created = database.collection_users.find_one({"_id": ObjectId(user_add.inserted_id)})
    
    return schemas.initial_user(user_after_created)