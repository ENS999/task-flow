class TagWorker():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_tags(self, tag_name):
        self.cursor.execute(
            "INSERT INTO tags (tag_name) VALUES (%s) RETURNING tag_id",
            (tag_name,)
        )
        tag_id = self.cursor.fetchone()[0]
        return tag_id

    def get_tags(self):
        self.cursor.execute(
            "SELECT * FROM tags"
        )
        result = self.cursor.fetchall()
        return result

    def add_task_tag(self, task_id, tag_id, user_id):
        self.cursor.execute(
            "SELECT task_id, user_id FROM tasks WHERE task_id=%s AND user_id=%s",
            (task_id, user_id)
        )
        check_user = self.cursor.fetchone()
        if check_user is None:
            return None

        self.cursor.execute(
            "SELECT tag_id FROM tags WHERE tag_id=%s",
            (tag_id,)
        )
        check_tag = self.cursor.fetchone()
        if check_tag is None:
            return None

        self.cursor.execute(
            "INSERT INTO task_tags (task_id, tag_id) VALUES (%s, %s)",
            (task_id, tag_id)
        )
        result = self.cursor.rowcount
        return result

    def remove_task_tag(self, task_id, tag_id, user_id):
        self.cursor.execute(
            "SELECT task_id, user_id FROM tasks WHERE task_id=%s AND user_id=%s",
            (task_id, user_id)
        )
        check_user = self.cursor.fetchone()
        if check_user is None:
            return None
        self.cursor.execute(
            "DELETE FROM task_tags WHERE task_id=%s AND tag_id=%s",
            (task_id, tag_id)
        )
        result = self.cursor.rowcount
        return result