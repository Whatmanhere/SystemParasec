import psutil
from PyQt5.QtWidgets import QTableWidgetItem

def display_users(table_widget):
    users = psutil.users()
    table_widget.setRowCount(len(users))
    table_widget.setColumnCount(2)
    table_widget.setHorizontalHeaderLabels(["User", "Terminal"])

    for row, user in enumerate(users):
        items = [
            QTableWidgetItem(user.name),
            QTableWidgetItem(user.terminal if user.terminal else "N/A")
        ]

        for item in items:
            table_widget.setItem(row, items.index(item), item)
