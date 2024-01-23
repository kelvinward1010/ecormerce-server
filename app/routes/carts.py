from fastapi import APIRouter, HTTPException, status
from .. import models, database, utils, schemas
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/carts",
    tags=["Carts"],
)

#Items
@router.get("/all_carts")
async def get_all_carts():
    carts = database.collection_carts.find()
    return {"data": schemas.list_carts(carts)}

@router.get("/cart_find")
async def get_cart_find(email_user_cart):
    cart_user = database.collection_carts.find_one({"email_user_cart": email_user_cart})
    if not cart_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found your cart!")
    return {"data": schemas.initial_cart(cart_user)}

@router.post("/create_cart", status_code=status.HTTP_201_CREATED)
async def create_cart(cart: models.Carts):
    if not cart.email_user_cart and not cart.carts:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You need have infomation!")
    if cart.email_user_cart == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You need have all infomation!")
    
    newCart = database.collection_carts.insert_one(dict(cart, created_at = datetime.utcnow(), updated_at = datetime.now()))    
    cart_after_created = database.collection_carts.find_one({"_id": ObjectId(newCart.inserted_id)})
    
    return {"data": schemas.initial_cart(cart_after_created)}

@router.put("/add_item_to_cart")
async def add_item_to_cart(email_user_cart, item_cart: models.ItemInCart):
    find_cart = database.collection_carts.find_one({"email_user_cart": str(email_user_cart)})

    if not find_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found cart to update!")
    
    for cart in find_cart['carts']:
        if cart['id'] == item_cart.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"This item is aleady in cart!")
    id = find_cart['_id']
    database.collection_carts.find_one_and_update({"_id": ObjectId(id)}, {
        "$push": dict(carts = {
            "id": item_cart.id,
            "name": item_cart.name,
            "description": item_cart.description,
            "image": item_cart.image,
            "price": item_cart.price,
            "stars": item_cart.stars,
        })
    })
    find_cart_after_update = database.collection_carts.find_one({"_id": ObjectId(id)})
    return {"data": schemas.initial_cart(find_cart_after_update)}

@router.put("/remove_item_in_cart")
async def remove_item_in_cart(email_user_cart, id_item):
    find_cart = database.collection_carts.find_one({"email_user_cart": str(email_user_cart)})

    if not find_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found cart to update!")
    
    id_carts = find_cart['_id']
    
    database.collection_carts.find_one_and_update({"_id": ObjectId(id_carts)}, {
        "$pull": dict(carts = {
            "id": str(id_item),
        })
    })
    find_cart_after_update = database.collection_carts.find_one({"_id": ObjectId(id_carts)})
    return {"data": schemas.initial_cart(find_cart_after_update)}