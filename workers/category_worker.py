class CategoryWorker():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_categories(self, category_name):
        self.cursor.execute(
            "INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id",
            (category_name,)
        )
        result = self.cursor.fetchone()[0]
        return result

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()