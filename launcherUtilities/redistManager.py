import os
import subprocess
import urllib.request
from PySide6.QtWidgets import (QDialog, QLabel, QPushButton, QVBoxLayout, 
                              QProgressDialog, QMessageBox)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QObject, QThread, Signal, QTimer
import winreg

class RedistWorker(QObject):
    finished = Signal(bool, str)

    def run(self):
        temp_path = os.path.join(os.environ["TEMP"], "vc_redist.x64.exe")
        try:
            urllib.request.urlretrieve(RedistManager.VC_REDIST_URL, temp_path)
            self.run_installer(temp_path)
        except Exception as e:
            self.finished.emit(False, f"Failed to download or run installer: {e}")

    def run_installer(self, installer_path):
        try:
            subprocess.run([installer_path, "/quiet", "/norestart"], check=True)
            self.finished.emit(True, "Installation completed successfully.")
        except subprocess.CalledProcessError as e:
            self.finished.emit(False, f"Installation failed: {e}")

class RedistManager(QDialog):
    VC_REDIST_URL = "https://aka.ms/vs/17/release/vc_redist.x64.exe"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VC++ Redistributable Check")
        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 25px;
                border: none;
                border-radius: 5px;
                background-color: #007acc;
                color: white;
                font-size: 13px;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #006bb3;
            }
            QPushButton:pressed {
                background-color: #005c99;
            }
        """)
        
        message_label = QLabel("VC++ Redist x64 2022 is required. Would you like to install it automatically?", self)
        message_label.setWordWrap(True)
        message_label.setFont(QFont('Arial', 10, QFont.Bold))
        message_label.setAlignment(Qt.AlignCenter)

        install_button = QPushButton("Install", self)
        continue_button = QPushButton("Continue", self)

        install_button.setFont(QFont('Arial', 10))
        continue_button.setFont(QFont('Arial', 10))

        install_button.clicked.connect(self.start_installation)
        continue_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(message_label)
        layout.addWidget(install_button)
        layout.addWidget(continue_button)
        self.setLayout(layout)

        self.thread = None
        self.worker = None

        print("RedistManager initialization success.")

    def check_redist_installed(self):
        keys_to_check = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for base_key in keys_to_check:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_key) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name) as sub_key:
                            try:
                                display_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                                if "Visual C++" in display_name and "2022" in display_name and "x64" in display_name.lower():
                                    return True
                            except FileNotFoundError:
                                continue
            except Exception:
                continue
        return False

    def start_installation(self):
        self.progress = QProgressDialog("Downloading and Installing VC++ Redist x64...", "Cancel", 0, 0, self)
        self.progress.setWindowTitle("Installation Progress")
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setAutoClose(False)
        self.progress.setAutoReset(False)
        self.progress.setValue(0)

        self.progress.setStyleSheet("""
            QProgressDialog {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 8px;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QProgressBar {
                border: 1px solid #404040;
                border-radius: 5px;
                background-color: #262626;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                width: 20px;
            }
            QPushButton {
                padding: 5px 15px;
                border: none;
                border-radius: 5px;
                background-color: #007acc;
                color: white;
            }
            QPushButton:hover {
                background-color: #006bb3;
            }
        """)
        
        self.progress.show()

        self.thread = QThread()
        self.worker = RedistWorker()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.on_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_finished(self, success, message):
        redist_path = os.path.join(os.environ["TEMP"], "vc_redist.x64.exe")
        if os.path.exists(redist_path):
            os.remove(redist_path)

        self.progress.setValue(1)
        self.progress.close()
        self.thread.quit()
        self.thread.wait()

        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 25px;
                border: none;
                border-radius: 5px;
                background-color: #007acc;
                color: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #006bb3;
            }
        """)
        msg_box.setWindowTitle("Installation Result")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information if success else QMessageBox.Critical)
        msg_box.show()

        QTimer.singleShot(3000, msg_box.accept)
        self.accept()