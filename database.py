import sqlite3

class TaskDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority INTEGER NOT NULL,
                due_date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_task(self, title, priority, due_date):
        self.conn.execute("INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)", (title, priority, due_date))
        self.conn.commit()

    def get_tasks(self, order_by="priority"):
        if order_by == "priority":
            cursor = self.conn.execute("SELECT id, title, priority, due_date FROM tasks ORDER BY priority ASC")
        elif order_by == "due_date":
            cursor = self.conn.execute("SELECT id, title, priority, due_date FROM tasks ORDER BY due_date ASC")
        else:
            cursor = self.conn.execute("SELECT id, title, priority, due_date FROM tasks")
        return cursor.fetchall()

    def get_task_id_by_title(self, title):
        cursor = self.conn.execute("SELECT id FROM tasks WHERE title = ?", (title,))
        result = cursor.fetchone()
        return result[0] if result else None

    def update_task(self, task_id, new_title, new_priority, new_due_date):
        self.conn.execute(
            "UPDATE tasks SET title = ?, priority = ?, due_date = ? WHERE id = ?",
            (new_title, new_priority, new_due_date, task_id)
        )
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def clear_all_tasks(self):
        self.conn.execute("DELETE FROM tasks")
        self.conn.commit()
