from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=72)

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=72)

class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    status: StatusEnum
    priority: PriorityEnum
    due_date: Optional[datetime] = None
    category_id: int

class CategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class TagRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class TaskTagRequest(BaseModel):
    tag_id: int

class SortBy(str, Enum):
    status = "status"
    priority = "priority"
    due_date = "due_date"
    category_id = "category_id"
    created_at = "created_at"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"