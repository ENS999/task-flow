from schemas import CategoryRequest
from fastapi import APIRouter, HTTPException, Depends
from manager import manager
from dependencies import get_current_user

router = APIRouter()

@router.post("/categories", status_code=201)
def create_categories(request: CategoryRequest, user_id: int = Depends(get_current_user)):
    result = manager.create_categories(request.name)
    if result is None:
        raise HTTPException(status_code=409, detail="Category already exists")
    return {"category_id": result, "message": "Category created successfully"}

@router.get("/categories")
def get_categories(user_id: int = Depends(get_current_user)):
    result = manager.get_categories()
    return result