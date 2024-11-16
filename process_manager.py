import psutil
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QColor, QIcon
import win32process
import win32gui
import win32api
import win32con

def display_processes(table_widget):
    processes = list(psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']))
    processes.sort(key=lambda p: p.info['memory_info'].rss, reverse=True)

    table_widget.setRowCount(len(processes))
    table_widget.setColumnCount(4)
    table_widget.setHorizontalHeaderLabels(["PID", "Icon", "Name", "CPU %", "Memory (MB)"])
    
   
    table_widget.setRowHeight(0, 20)
    for row in range(len(processes)):
        table_widget.setRowHeight(row + 1, 18)

    for row, proc in enumerate(processes):
        try:
            mem_usage_mb = proc.info['memory_info'].rss / (1024 ** 2)
            items = [
                QTableWidgetItem(str(proc.info['pid'])),
                QTableWidgetItem(),
                QTableWidgetItem(proc.info['name']),
                QTableWidgetItem(f"{proc.info['cpu_percent']}%"),
                QTableWidgetItem(f"{mem_usage_mb:.2f} MB")
            ]

            if mem_usage_mb > 1000:
                color = QColor(255, 50, 50)
            elif mem_usage_mb > 500:
                color = QColor(255, 165, 0) 
            else:
                color = QColor(50, 255, 50)

            for index, item in enumerate(items):
                item.setBackground(color)
                table_widget.setItem(row + 1, index, item)

            icon = get_process_icon(proc.info['pid'])
            icon_item = QTableWidgetItem(icon, "")
            table_widget.setItem(row + 1, 1, icon_item)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def get_process_icon(pid):
    try:
        hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
        hWnd = win32process.EnumProcessWindows(hProcess)[0]
        icon = win32gui.GetClassLong(hWnd, win32con.GCL_HICON)
        return QIcon(win32gui.GetIconInfo(icon))
    except Exception as e:
        print(f"Error retrieving icon for PID {pid}: {e}")
        return QIcon()
