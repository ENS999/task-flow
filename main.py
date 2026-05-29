from manager import manager
from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router
from routes.categories import router as categories_router
from routes.tags import router as tags_router
from config import ENV
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

if ENV == "production":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI()

if ENV == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://前端domain.com"],
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

if ENV == "production":
    @app.exception_handler(Exception)
    async def prod_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

manager.create_all_table()

@app.get("/")
def health_check():
    return {"status": "ok", "project": "task-flow"}

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(categories_router)
app.include_router(tags_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)