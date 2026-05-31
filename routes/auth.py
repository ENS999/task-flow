from fastapi import APIRouter, HTTPException, Depends
from manager import Manager, get_manager
from schemas import RegisterRequest, LoginRequest

router = APIRouter()

@router.post("/register", status_code=201)
def register(request: RegisterRequest, mgr: Manager = Depends(get_manager)):
    user_id = mgr.register(request.username, request.password)
    if user_id is None:
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"user_id": user_id, "message": "User registered successfully"}

@router.post("/login")
def login(request: LoginRequest, mgr: Manager = Depends(get_manager)):
    token = mgr.login(request.username, request.password)
    if token is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"token": token}