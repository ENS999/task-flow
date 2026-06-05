import os
import time
import subprocess
import httpx
import pytest
from playwright.sync_api import Playwright
from manager import Manager

@pytest.fixture(scope="session")
def server():
    proc = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        env={**os.environ, "DB_NAME": "taskflow_test"}
    )

    for _ in range(20):
        try:
            httpx.get("http://127.0.0.1:8000/")
            break
        except httpx.ConnectError:
            time.sleep(0.5)
    else:
        proc.terminate()
        raise RuntimeError("Server failed to start within 10 seconds")

    yield

    proc.terminate()
    proc.wait()

@pytest.fixture(autouse=True)
def clean_db(server):
    os.environ["DB_NAME"] = "taskflow_test"
    manager = Manager()
    manager.cursor.execute("DELETE FROM task_tags")
    manager.cursor.execute("DELETE FROM tasks")
    manager.cursor.execute("DELETE FROM categories")
    manager.cursor.execute("DELETE FROM tags")
    manager.cursor.execute("DELETE FROM users")
    manager.commit()
    manager.close()
    yield

@pytest.fixture()
def api(playwright: Playwright, server):
    context = playwright.request.new_context(
        base_url="http://127.0.0.1:8000"
    )
    yield context
    context.dispose()