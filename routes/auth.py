from fastapi import APIRouter, HTTPException
from manager import manager
from schemas import RegisterRequest, LoginRequest

router = APIRouter()

@router.post("/register", status_code=201)
def register(request: RegisterRequest):
    user_id = manager.register(request.username, request.password)
    if user_id is None:
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"user_id": user_id, "message": "User registered successfully"}

@router.post("/login")
def login(request: LoginRequest):
    token = manager.login(request.username, request.password)
    if token is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"token": token}