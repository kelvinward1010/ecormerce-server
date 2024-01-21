from fastapi import APIRouter, HTTPException, status, Response
from .. import models, schemas, database, utils, oauth2
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: models.User):
    
    user_find_checked = database.collection_users.find_one({"email": user.email})
    
    if user_find_checked:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"This account have {user.email} already exists!")
    
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    user_add = database.collection_users.insert_one(dict(
                                                        user, 
                                                        created_at = datetime.utcnow(), 
                                                        updated_at = datetime.now()),
                                                    )
    
    if not user_add:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't register account!")
    
    user_after_created = database.collection_users.find_one({"_id": ObjectId(user_add.inserted_id)})
    
    return schemas.initial_user(user_after_created)

@router.post("/login")
async def login(user_credentials: models.UserAuth, responses: Response):
    
    user_query = database.collection_users.find_one({"email": user_credentials.email})
    
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with email: {user_credentials.email} to login!")
    
    user = schemas.initial_user(user_query)
    
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    if not utils.verify(user_credentials.password, user.get('password')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password!")
    
    access_token = oauth2.create_access_token(data = {"id": user["id"]})
    
    responses.set_cookie("access_token", access_token, httponly=True)
    
    return {
        "current_user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(responses: Response):
    
    responses.delete_cookie("access_token", secure=True, samesite=None)

    return {"Message": f"Logout!"}
