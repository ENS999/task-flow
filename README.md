# Task-flow API

任務管理系統，透過 FastAPI 實現 RESTful API。功能包含：任務 CRUD、分類與標籤管理、狀態流轉控制（done 不可回退）、篩選 / 排序 / 分頁、JWT 認證與授權、13 項整合測試。

A task management API built with FastAPI. Features include task CRUD, categories, tags, status flow control (todo → in_progress → done), filtering, sorting, pagination, and JWT authentication.

**Live Demo:**

---

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Authentication:** JWT (python-jose + passlib bcrypt)
- **Validation:** Pydantic
- **Testing:** pytest (13 tests)
- **Containerization:** Docker
- **Deployment:** Render

---

## Project Structure

```
task-flow/
├── main.py
├── config.py           # Environment variables (SSOT)
├── manager.py          # Manager (business logic)
├── database.py
├── schemas.py
├── dependencies.py     # JWT token verification
├── workers/
│   ├── user_worker.py
│   ├── task_worker.py
│   ├── category_worker.py
│   └── tag_worker.py
├── routes/
│   ├── auth.py
│   ├── categories.py
│   ├── tasks.py
│   └── tags.py
├── test_app.py         # pytest test cases
├── Dockerfile
├── requirements.txt
├── .env.example
└── .dockerignore
```

---

## API Endpoints

| Method | Endpoint                         | Description          | Auth |
| ------ | -------------------------------- | -------------------- | ---- |
| POST   | `/register`                      | Register             | No   |
| POST   | `/login`                         | Login                | No   |
| POST   | `/tasks`                         | Create task          | Yes  |
| GET    | `/tasks`                         | Get all tasks        | Yes  |
| GET    | `/tasks/{task_id}`               | Get task by ID       | Yes  |
| PUT    | `/tasks/{task_id}`               | Update task          | Yes  |
| DELETE | `/tasks/{task_id}`               | Delete task          | Yes  |
| POST   | `/categories`                    | Create category      | Yes  |
| GET    | `/categories`                    | Get all categories   | Yes  |
| POST   | `/tags`                          | Create tag           | Yes  |
| GET    | `/tags`                          | Get all tags         | Yes  |
| POST   | `/tasks/{task_id}/tags`          | Add tag to task      | Yes  |
| DELETE | `/tasks/{task_id}/tags/{tag_id}` | Remove tag from task | Yes  |

---

## How to Run

### Local

Clone the repo and enter the project directory:

```
git clone
cd
```

Install dependencies:

```
pip install -r requirements.txt
```

Set up environment variables:

```
cp .env.example .env
```

Edit `.env` and set your own `SECRET_KEY`.

Run the server:

```
uvicorn main:app --reload
```

Open browser: http://127.0.0.1:8000/docs

### Docker

```
docker build -t task-flow .
docker run --env-file .env -p 8000:8000 task-flow
```

Open browser: http://localhost:8000/docs

---

## Run Tests

```
pytest test_app.py -v
```
