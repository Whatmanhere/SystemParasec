import psutil
from PyQt5.QtWidgets import QTableWidgetItem

def display_services(table_widget):
    services = list(psutil.win_service_iter())
    table_widget.setRowCount(len(services))
    table_widget.setColumnCount(2)
    table_widget.setHorizontalHeaderLabels(["Service Name", "Status"])

    for row, service in enumerate(services):
        try:
            service_info = service.as_dict(attrs=['name', 'status'])
            items = [
                QTableWidgetItem(service_info['name']),
                QTableWidgetItem(service_info['status'])
            ]

            for item in items:
                table_widget.setItem(row, items.index(item), item)

        except Exception:
            continue
