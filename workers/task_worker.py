class TaskWorker():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_task(self, title, description, status, priority, due_date, user_id, category_id):
        self.cursor.execute(
            "SELECT category_id FROM categories WHERE category_id=%s",
            (category_id,)
        )
        check_id = self.cursor.fetchone()
        if check_id is None:
            return None

        self.cursor.execute(
            "INSERT INTO tasks (title, description, status, priority, due_date, user_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING task_id",
            (title, description, status, priority, due_date, user_id, category_id)
        )
        task_id = self.cursor.fetchone()['task_id']
        return task_id

    def get_tasks(self, user_id, status, priority, due_date, category_id, sort_by, sort_order, page, limit):
        conditions = ["user_id=%s"]
        params = [user_id]
        offset = (page - 1) * limit

        if status is not None:
            conditions.append("status=%s")
            params.append(status)
        if priority is not None:
            conditions.append("priority=%s")
            params.append(priority)
        if due_date is not None:
            conditions.append("due_date=%s")
            params.append(due_date)
        if category_id is not None:
            conditions.append("category_id=%s")
            params.append(category_id)

        where_clause = " AND ".join(conditions)
        sql = f"SELECT * FROM tasks WHERE {where_clause}"

        if sort_by is not None:
            sql += f" ORDER BY {sort_by.value}"
            if sort_order is not None:
                sql += f" {sort_order.value}"
        sql += " LIMIT %s OFFSET %s"
        params.append(limit)
        params.append(offset)

        self.cursor.execute(sql, tuple(params))
        result = self.cursor.fetchall()
        return result


    def get_task(self, task_id, user_id):
        self.cursor.execute(
            "SELECT * FROM tasks WHERE task_id=%s AND user_id=%s",
            (task_id, user_id)
        )
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result

    def put_task(self, task_id, title, description, status, priority, due_date, user_id, category_id):
        self.cursor.execute(
            "SELECT category_id FROM categories WHERE category_id=%s",
            (category_id,)
        )
        check_category = self.cursor.fetchone()
        if check_category is None:
            return None

        self.cursor.execute(
            "UPDATE tasks SET title=%s, description=%s, status=%s, priority=%s, due_date=%s, category_id=%s WHERE task_id=%s AND user_id=%s",
            (title, description, status, priority, due_date, category_id, task_id, user_id)
        )
        result = self.cursor.rowcount
        return result

    def del_task(self, task_id, user_id):
        self.cursor.execute(
            "DELETE FROM tasks WHERE task_id = %s AND user_id = %s",
            (task_id, user_id)
        )
        result = self.cursor.rowcount
        return result