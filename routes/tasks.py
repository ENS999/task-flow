from fastapi import APIRouter, HTTPException, Query, Depends
from manager import manager
from schemas import TaskRequest, StatusEnum, PriorityEnum, SortBy, SortOrder
from dependencies import get_current_user
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.post("/tasks", status_code=201)
def create_task(request: TaskRequest, user_id: int = Depends(get_current_user)):
    result = manager.create_task(request.title, request.description, request.status, request.priority, request.due_date, user_id, request.category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"task_id": result, "message": "Task created successfully"}

@router.get("/tasks")
def get_tasks(
    user_id: int = Depends(get_current_user),
    status: Optional[StatusEnum] = Query(None),
    priority: Optional[PriorityEnum] = Query(None),
    due_date: Optional[datetime] = Query(None),
    category_id: Optional[int] = Query(None),
    sort_by: Optional[SortBy] = Query(None),
    sort_order: Optional[SortOrder] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
    ):
    query = manager.get_tasks(user_id, status, priority, due_date, category_id, sort_by, sort_order, page, limit)
    return query

@router.get("/tasks/{task_id}")
def get_task(task_id: int, user_id: int = Depends(get_current_user)):
    result = manager.get_task(task_id, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.put("/tasks/{task_id}")
def put_task(task_id: int, request: TaskRequest, user_id: int = Depends(get_current_user)):
    result = manager.put_task(task_id, request.title, request.description, request.status, request.priority, request.due_date, user_id, request.category_id)
    if result == "done not update":
        raise HTTPException(status_code=403, detail="Done not update")
    elif result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    elif result == "task not found":
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated successfully"}

@router.delete("/tasks/{task_id}")
def del_task(task_id: int, user_id: int = Depends(get_current_user)):
    result = manager.del_task(task_id, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}