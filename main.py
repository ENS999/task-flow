from manager import manager
from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router
from routes.categories import router as categories_router
from routes.tags import router as tags_router
import uvicorn

app = FastAPI()
manager.create_all_table()

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(categories_router)
app.include_router(tags_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)