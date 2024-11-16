import psutil
from PyQt5.QtWidgets import QTableWidgetItem

def display_network_info(table_widget):
    net_io = psutil.net_io_counters(pernic=True)
    table_widget.setRowCount(len(net_io))
    table_widget.setColumnCount(2)
    table_widget.setHorizontalHeaderLabels(["Interface", "Data Transferred (MB)"])

    for row, (interface, stats) in enumerate(net_io.items()):
        items = [
            QTableWidgetItem(interface),
            QTableWidgetItem(f"Sent: {stats.bytes_sent / (1024 ** 2):.2f} MB | Received: {stats.bytes_recv / (1024 ** 2):.2f} MB")
        ]

        for item in items:
            table_widget.setItem(row, items.index(item), item)
