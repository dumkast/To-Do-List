import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QComboBox,
    QDateEdit, QListWidgetItem, QLabel, QFrame, QMessageBox
)
from database import TaskDatabase

class TaskWidget(QWidget):
    def __init__(self, title, priority, due_date):
        super().__init__()

        self.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 8px;
            padding: 8px;
        """)

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.priority_label = QLabel(f"Приоритет: {priority}")
        self.priority_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.priority_label.setStyleSheet(self.priority_style(priority))

        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.priority_label)

        self.date_label = QLabel(f"Дедлайн: {due_date}")
        self.date_label.setStyleSheet("color: #777777; font-size: 12px;")

        layout.addLayout(top_layout)
        layout.addWidget(self.date_label)

        self.setLayout(layout)

    def priority_style(self, priority):
        colors = {
            1: "#FF5722",   # Очень высокий - оранжевый
            2: "#FF9800",   # Высокий
            3: "#FFC107",   # Средний
            4: "#8BC34A",   # Низкий
            5: "#4CAF50",   # Очень низкий
        }
        color = colors.get(priority, "#999999")
        return f"""
            background-color: {color};
            color: white;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
        """

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = TaskDatabase()

        self.setWindowTitle("To-Do List")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(550, 650)

        self.setStyleSheet("""
            background-color: #F5F5F5;
            color: #2C2C2C;
            font-size: 14px;
            font-family: Arial, sans-serif;
        """)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название задачи")
        self.title_input.setStyleSheet(self.input_style())

        self.priority_input = QLineEdit()
        self.priority_input.setPlaceholderText("Приоритет (1-5)")
        self.priority_input.setStyleSheet(self.input_style())

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.calendarWidget().setFixedSize(270, 200)
        self.date_input.setStyleSheet(self.input_style())

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.search_input.setStyleSheet(self.input_style())
        self.search_input.textChanged.connect(self.search_task)

        self.sort_filter = QComboBox()
        self.sort_filter.addItem("Сортировать по приоритету")
        self.sort_filter.addItem("Сортировать по дедлайну")
        self.sort_filter.setStyleSheet(self.input_style())
        self.sort_filter.currentTextChanged.connect(self.load_tasks)

        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.setStyleSheet(self.button_style())
        self.add_btn.clicked.connect(self.add_task)

        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.setStyleSheet(self.button_style())
        self.edit_btn.clicked.connect(self.edit_task)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.setStyleSheet(self.button_style())
        self.delete_btn.clicked.connect(self.delete_task)

        self.clear_btn = QPushButton("Очистить все")
        self.clear_btn.setStyleSheet(self.button_style())
        self.clear_btn.clicked.connect(self.clear_all_tasks)

        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.clear_btn)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            background-color: #F9F9F9;
            border: none;
            
        """)

        main_layout.addWidget(self.title_input)
        main_layout.addWidget(self.priority_input)
        main_layout.addWidget(self.date_input)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.sort_filter)
        main_layout.addWidget(self.task_list)

        self.setLayout(main_layout)

        self.load_tasks()

    def input_style(self):
        return """
            background-color: #FFFFFF;
            padding: 8px;
            border: 1px solid #CCCCCC;
            border-radius: 5px;
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                padding: 8px;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """

    def load_tasks(self):
        self.task_list.clear()
        order = "priority" if self.sort_filter.currentText() == "Сортировать по приоритету" else "due_date"
        tasks = self.db.get_tasks(order_by=order)
        for task in tasks:
            item = QListWidgetItem()
            widget = TaskWidget(task[1], task[2], task[3])
            item.setSizeHint(widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def add_task(self):
        title = self.title_input.text().strip()
        priority = self.priority_input.text().strip()
        due_date = self.date_input.date().toString("dd.MM.yyyy")

        if not title or not priority.isdigit() or not (1 <= int(priority) <= 5):
            self.show_message("Ошибка", "Введите название и корректный приоритет (1-5).")
            return

        self.db.add_task(title, int(priority), due_date)
        self.title_input.clear()
        self.priority_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.load_tasks()

    def delete_task(self):
        selected_item = self.task_list.currentRow()
        if selected_item != -1:
            task_title = self.task_list.itemWidget(self.task_list.item(selected_item)).title_label.text()
            task_id = self.db.get_task_id_by_title(task_title)
            if task_id:
                self.db.delete_task(task_id)
                self.load_tasks()
            else:
                self.show_message("Ошибка", "Не удалось найти задачу.")
        else:
            self.show_message("Ошибка", "Выберите задачу для удаления.")

    def edit_task(self):
        selected_item = self.task_list.currentRow()
        if selected_item != -1:
            task_title = self.task_list.itemWidget(self.task_list.item(selected_item)).title_label.text()
            task_id = self.db.get_task_id_by_title(task_title)

            new_title = self.title_input.text().strip()
            new_priority = self.priority_input.text().strip()
            new_due_date = self.date_input.date().toString("dd.MM.yyyy")

            if not new_title or not new_priority.isdigit() or not (1 <= int(new_priority) <= 5):
                self.show_message("Ошибка", "Введите новое название и корректный приоритет (1-5).")
                return

            if task_id:
                self.db.update_task(task_id, new_title, int(new_priority), new_due_date)
                self.load_tasks()
            else:
                self.show_message("Ошибка", "Не удалось найти задачу для редактирования.")
        else:
            self.show_message("Ошибка", "Выберите задачу для редактирования.")

    def clear_all_tasks(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Удалить все задачи?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setWindowIcon(QIcon("icon.png"))
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.db.clear_all_tasks()
            self.load_tasks()

    def search_task(self, text):
        self.task_list.clear()
        order = "priority" if self.sort_filter.currentText() == "Сортировать по приоритету" else "due_date"
        tasks = self.db.get_tasks(order_by=order)
        for task in tasks:
            if text.lower() in task[1].lower():
                item = QListWidgetItem()
                widget = TaskWidget(task[1], task[2], task[3])
                item.setSizeHint(widget.sizeHint())
                self.task_list.addItem(item)
                self.task_list.setItemWidget(item, widget)

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setWindowIcon(QIcon("warning.png"))
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = ToDoApp()
    todo_app.show()
    sys.exit(app.exec())
