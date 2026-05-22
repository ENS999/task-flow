from psycopg2 import IntegrityError
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM
from database import Database
from workers.user_worker import UserWorker
from workers.task_worker import TaskWorker
from workers.category_worker import CategoryWorker
from workers.tag_worker import TagWorker

class Manager:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()
        self.user_worker = UserWorker(self.cursor)
        self.task_worker = TaskWorker(self.cursor)
        self.category_worker = CategoryWorker(self.cursor)
        self.tag_worker = TagWorker(self.cursor)

    def commit(self):
        self.db.connection.commit()

    def rollback(self):
        self.db.connection.rollback()

    def close(self):
        self.cursor.close()
        self.db.close()

    def create_all_table(self):
        users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id       BIGSERIAL    PRIMARY KEY,
            user_name     VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at    TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
            );
            """

        categories_sql = """
        CREATE TABLE IF NOT EXISTS categories (
            category_id   BIGSERIAL    PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL UNIQUE,
            created_at    TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
            );
            """

        tags_sql = """
        CREATE TABLE IF NOT EXISTS tags (
            tag_id     BIGSERIAL    PRIMARY KEY,
            tag_name   VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
            );
            """

        tasks_sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id     BIGSERIAL    PRIMARY KEY,
            title       VARCHAR(255) NOT NULL,
            description TEXT,
            status      VARCHAR      NOT NULL CHECK (status IN ('todo', 'in_progress', 'done')),
            priority    VARCHAR      NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
            due_date    TIMESTAMP,
            user_id     BIGINT       NOT NULL,
            category_id BIGINT       NOT NULL,
            created_at  TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)     REFERENCES users(user_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
            );
            """

        task_tags = """
        CREATE TABLE IF NOT EXISTS task_tags (
            task_id    BIGINT      NOT NULL,
            tag_id     BIGINT      NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(task_id, tag_id),
            FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id)  REFERENCES tags(tag_id)
            );
            """
        try:
            self.cursor.execute(users_sql)
            self.cursor.execute(categories_sql)
            self.cursor.execute(tags_sql)
            self.cursor.execute(tasks_sql)
            self.cursor.execute(task_tags)
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_category_id ON tasks(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_task_tags_tag_id ON task_tags(tag_id)")
            self.commit()
            print("Tables created.")
        except Exception as e:
            self.rollback()
            print(f"Error: {e}")

    def register(self, user_name, password):
        try:
            user_id = self.user_worker.create_user(user_name, password)
            self.commit()
            return user_id
        except IntegrityError:
            self.rollback()
            return None
        except Exception:
            self.rollback()
            raise

    def login(self, user_name, password):
        try:
            result = self.user_worker.verify_user(user_name, password)
            if result is None:
                return None
            token = jwt.encode(
                {"user_id": result, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
                SECRET_KEY,
                algorithm=ALGORITHM
            )
            return token
        except Exception:
            self.rollback()
            raise

    def create_task(self, title, description, status, priority, due_date, user_id, category_id):
        try:
            task_id = self.task_worker.create_task(title, description, status, priority, due_date, user_id, category_id)
            if task_id is None:
                return None
            self.commit()
            return task_id
        except Exception:
            self.rollback()
            raise

    def get_tasks(self, user_id, status, priority, due_date, category_id, sort_by, sort_order, page, limit):
        result = self.task_worker.get_tasks(user_id, status, priority, due_date, category_id, sort_by, sort_order, page, limit)
        return result

    def get_task(self, task_id, user_id):
        result = self.task_worker.get_task(task_id, user_id)
        return result

    def put_task(self, task_id, title, description, status, priority, due_date, user_id, category_id):
        try:
            old_status = self.task_worker.get_task(task_id, user_id)
            if old_status is None:
                return "task not found"
            elif old_status[3] == "done":
                return "done not update"
            result = self.task_worker.put_task(task_id, title, description, status, priority, due_date, user_id, category_id)
            if result is None:
                return None
            self.commit()
            return result
        except Exception:
            self.rollback()
            raise

    def del_task(self, task_id,  user_id):
        try:
            result = self.task_worker.del_task(task_id, user_id)
            if result == 0:
                return None
            self.commit()
            return result
        except Exception:
            self.rollback()
            raise

    def create_categories(self, category_name):
        try:
            result = self.category_worker.create_categories(category_name)
            self.commit()
            return result
        except IntegrityError:
            self.rollback()
            return None
        except Exception:
            self.rollback()
            raise

    def get_categories(self):
        result = self.category_worker.get_categories()
        return result

    def create_tags(self, tag_name):
        try:
            result = self.tag_worker.create_tags(tag_name)
            self.commit()
            return result
        except IntegrityError:
            self.rollback()
            return None
        except Exception:
            self.rollback()
            raise

    def get_tags(self):
        result = self.tag_worker.get_tags()
        return result

    def add_task_tag(self, task_id, tag_id, user_id):
        try:
            result = self.tag_worker.add_task_tag(task_id, tag_id, user_id)
            if result is None:
                return None
            self.commit()
            return result
        except IntegrityError:
            self.rollback()
            return "duplicate"
        except Exception:
            self.rollback()
            raise

    def remove_task_tag(self, task_id, tag_id, user_id):
        try:
            result = self.tag_worker.remove_task_tag(task_id, tag_id, user_id)
            if result is None:
                return None
            if result == 0:
                return None
            self.commit()
            return result
        except Exception:
            self.rollback()
            raise

manager = Manager()