from pydantic import BaseModel, EmailStr
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



#Items
class Stars(BaseModel):
    user_id: str
    star: int
    
class Item(BaseModel):
    name: str
    description: str
    image: str | None
    price: int
    stars: list[Stars | None]
    amount_in_stock: int


#Carts
class ItemInCart(BaseModel):
    id: str
    name: str
    description: str
    image: str | None
    price: int
    stars: list
    amount_in_stock: int
    quantity: int
    
class Carts(BaseModel):
    carts: list
    email_user_cart: str
    
class RemoveItemCart(BaseModel):
    email_user_cart: str
    id_item: str
    
class UpdateItemCart(BaseModel):
    email_user_cart: str
    id_item: str
    plus: bool
    minus: bool