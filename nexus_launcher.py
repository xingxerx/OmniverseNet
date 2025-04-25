import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import psutil
import requests
from PySide6.QtCore import QCoreApplication, QProcess, Qt, QThread, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from nexus_launcher_ui import Ui_MainWindow

class NexusLauncher(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Nexus Launcher")
        self.setWindowIcon(QIcon(":/icons/nexus_icon.png"))
        self.nexus_process = None
        self.nexus_thread = None
        self.nexus_port = 8080
        self.nexus_path = ""
        self.nexus_config_path = ""
        self.nexus_log_path = ""
        self.nexus_data_path = ""
        self.nexus_pid = 0
        self.nexus_url = f"http://localhost:{self.nexus_port}"
        self.nexus_running = False
        self.nexus_config_file = "nexus.properties"
        self.nexus_log_file = "nexus.log"
        self.nexus_data_folder = "data"
        self.nexus_bin_folder = "bin"
        self.nexus_etc_folder = "etc"
        self.nexus_work_folder = "work"
        self.nexus_default_port = 8080
        self.nexus_default_host = "0.0.0.0"
        self.nexus_default_context_path = "/"
        self.nexus_default_args = ""
        self.nexus_default_jvm_args = ""
        self.nexus_default_log_level = "INFO"
        self.nexus_default_log_pattern = "%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%