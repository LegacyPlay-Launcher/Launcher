import ctypes
from PySide6.QtWidgets import QMessageBox

class AdminCheck:
    def __init__(self) -> None:
        self.admin = False

        try:
            self.admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            pass

    def is_admin(self) -> bool:
        if not self.admin:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Admin Check")
            msg_box.setText("Please run the launcher as an administrator.")
            msg_box.setIcon(QMessageBox.Critical)
            stylesheet = """
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
            """
            msg_box.setStyleSheet(stylesheet)
            msg_box.show()
            msg_box.exec()
            return False
        
        return True
