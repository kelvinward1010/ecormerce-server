from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


#Token
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None


#Users
class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    image: str | None

class UserAuth(BaseModel):
    email: EmailStr
    password: str
    
class UserChangePassword(BaseModel):
    email: EmailStr
    old_password: str
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    image: str | None
    
    