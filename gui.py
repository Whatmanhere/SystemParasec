from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget, QTabWidget, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
import process_manager
import network_monitor
import service_manager
import user_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Parasec")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('tools/parasec.png'))

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

    
        self.create_process_tab()
        self.create_network_tab()
        self.create_services_tab()
        self.create_users_tab()

        self.process_timer = QTimer(self)
        self.process_timer.timeout.connect(self.refresh_process_table)
        self.process_timer.start(3000)

        self.network_timer = QTimer(self)
        self.network_timer.timeout.connect(self.refresh_network_table)
        self.network_timer.start(5000)

        self.services_timer = QTimer(self)
        self.services_timer.timeout.connect(self.refresh_services_table)
        self.services_timer.start(10000)

        self.users_timer = QTimer(self)
        self.users_timer.timeout.connect(self.refresh_users_table)
        self.users_timer.start(15000)

        self.create_context_menu() 

    def create_process_tab(self):
        process_tab = QWidget()
        layout = QVBoxLayout()

        
        self.process_table = QTableWidget()
        layout.addWidget(QLabel("Processes"))
        layout.addWidget(self.process_table)
        process_manager.display_processes(self.process_table)

        process_tab.setLayout(layout)
        self.tabs.addTab(process_tab, "Processes")

    def create_network_tab(self):
        network_tab = QWidget()
        layout = QVBoxLayout()

    
        self.network_table = QTableWidget()
        layout.addWidget(QLabel("Network Activity"))
        layout.addWidget(self.network_table)
        network_monitor.display_network_info(self.network_table)

        network_tab.setLayout(layout)
        self.tabs.addTab(network_tab, "Network")

    def create_services_tab(self):
        services_tab = QWidget()
        layout = QVBoxLayout()

        
        self.services_table = QTableWidget()
        layout.addWidget(QLabel("Windows Services"))
        layout.addWidget(self.services_table)
        service_manager.display_services(self.services_table)

        services_tab.setLayout(layout)
        self.tabs.addTab(services_tab, "Services")

    def create_users_tab(self):
        users_tab = QWidget()
        layout = QVBoxLayout()

        
        self.users_table = QTableWidget()
        layout.addWidget(QLabel("Users"))
        layout.addWidget(self.users_table)
        user_manager.display_users(self.users_table)

        users_tab.setLayout(layout)
        self.tabs.addTab(users_tab, "Users")

    def create_context_menu(self):
        self.process_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.process_table.customContextMenuRequested.connect(self.show_process_menu)

    def show_process_menu(self, pos):
        item = self.process_table.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            properties_action = menu.addAction("View Properties")
            action = menu.exec_(self.process_table.viewport().mapToGlobal(pos))
            if action == properties_action:
                self.show_process_properties(item.row())

    def show_process_properties(self, row):
        pid_item = self.process_table.item(row, 0)
        if pid_item:
            pid = pid_item.text()
            
            print(f"Showing properties for PID: {pid}")

    def refresh_process_table(self):
        process_manager.display_processes(self.process_table)

    def refresh_network_table(self):
        network_monitor.display_network_info(self.network_table)

    def refresh_services_table(self):
        service_manager.display_services(self.services_table)

    def refresh_users_table(self):
        user_manager.display_users(self.users_table)
