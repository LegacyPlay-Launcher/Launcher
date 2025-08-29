from typing import Any


import os
import sys
import urllib.request
import subprocess
from PySide6.QtWidgets import QDialog, QMessageBox

class UpdatesManager(QDialog):
    CURRENT_VER_URL = "https://legacyplay.retify.lol/current_ver.txt"
    UPDATER_URL = "https://legacyplay.retify.lol/content/LegacyPlay_Updater.exe"

    def __init__(self, current_version) -> None:
        super().__init__()
        self.current_version = current_version
        self.setWindowTitle("LegacyPlay Update Check")
        self.setFixedSize(400, 180)
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
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #006bb3;
            }
            QPushButton:pressed {
                background-color: #005c99;
            }
        """)

    def checkUpdates(self) -> None:
        try:
            with urllib.request.urlopen(self.CURRENT_VER_URL, timeout=10) as response:
                online_version = response.read().decode('utf-8').strip()
        except Exception as e:
            print(f"Failed to check updates: {e}")
            return

        if online_version == self.current_version:
            return

        print(f"Update avaliable! From {self.current_version} -> {online_version}")

        prompt = f"Would you like to upgrade LegacyPlay from version {self.current_version} to {online_version}?\n\nThis will save your data and cached assets."
        reply = self._ask_user(prompt)

        if not reply:
            print("User denied the update, proceed to launcher.")
            return

        updater_path = self._download_updater()

        if not updater_path:
            print("Failed to download the updater. The webserver might be down. Contact the owner.")
            self._show_message("Update Error", "Failed to download the updater.", critical=True)
            return

        try:
            exe_dir = os.path.dirname(sys.executable)
            subprocess.Popen([updater_path, exe_dir], shell=False)
        except Exception as e:
            print("Failed to download the updater. Might be a build issue. Contact the owner.")
            self._show_message("Update Error", f"Failed to launch the updater: {e}", critical=True)
            return

        sys.exit(0)

    def _ask_user(self, message) -> Any:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Update Available")
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Question)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setDefaultButton(QMessageBox.Yes)
        dlg.setStyleSheet(self.styleSheet())
        return dlg.exec() == QMessageBox.Yes

    def _show_message(self, title, message, critical=False) -> None:
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical if critical else QMessageBox.Information)
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setStyleSheet(self.styleSheet())
        dlg.exec()

    def _download_updater(self) -> str | None:
        temp_dir = os.environ.get("TEMP") or os.environ.get("TMP")
        if not temp_dir:
            return None

        filename = "LegacyPlay_UpdaterApplication.exe"
        path = os.path.join(temp_dir, filename)

        try:
            urllib.request.urlretrieve(self.UPDATER_URL, path)
            return path
        except Exception as e:
            print(f"Failed to download updater: {e}")
            return None
