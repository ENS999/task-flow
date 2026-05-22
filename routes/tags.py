from schemas import TagRequest, TaskTagRequest
from fastapi import APIRouter, HTTPException, Depends
from manager import manager
from dependencies import get_current_user

router = APIRouter()

@router.post("/tags", status_code=201)
def create_tags(request: TagRequest, user_id: int = Depends(get_current_user)):
    result = manager.create_tags(request.name)
    if result is None:
        raise HTTPException(status_code=409, detail="Tag already exists")
    return {"tag_id": result, "message": "Tag created successfully"}

@router.get("/tags")
def get_tags(user_id: int = Depends(get_current_user)):
    result = manager.get_tags()
    return result

@router.post("/tasks/{task_id}/tags", status_code=201)
def add_task_tag(task_id: int, request: TaskTagRequest, user_id: int = Depends(get_current_user)):
    result = manager.add_task_tag(task_id, request.tag_id, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task or tag not found")
    elif result == "duplicate":
        raise HTTPException(status_code=409, detail="Tag already exists")
    return {"result": result, "message": "Tag add successfully"}

@router.delete("/tasks/{task_id}/tags/{tag_id}")
def remove_task_tag(task_id: int, tag_id: int, user_id: int = Depends(get_current_user)):
    result = manager.remove_task_tag(task_id, tag_id, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task-tag association not found")
    return {"result": result, "message": "Task-tag remove successfully"}