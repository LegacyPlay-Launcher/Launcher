from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, Signal

class AvatarWidget(QWidget):
    headClicked = Signal()
    torsoClicked = Signal()
    leftArmClicked = Signal()
    rightArmClicked = Signal()
    leftLegClicked = Signal()
    rightLegClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 300)
        self.setStyleSheet("background-color: transparent;")
        self.head_color = "#F2F3F3"
        self.torso_color = "#F2F3F3"
        self.left_arm_color = "#F2F3F3"
        self.right_arm_color = "#F2F3F3"
        self.left_leg_color = "#F2F3F3"
        self.right_leg_color = "#F2F3F3"

        print("AvatarWidget initialization success.")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor(self.head_color))
        painter.drawRect(75, 20, 50, 50)

        painter.setBrush(QColor(self.torso_color))
        painter.drawRect(70, 80, 60, 80)

        painter.setBrush(QColor(self.left_arm_color))
        painter.drawRect(25, 80, 40, 80)

        painter.setBrush(QColor(self.right_arm_color))
        painter.drawRect(135, 80, 40, 80)

        painter.setBrush(QColor(self.left_leg_color))
        painter.drawRect(70, 170, 30, 80)

        painter.setBrush(QColor(self.right_leg_color))
        painter.drawRect(100, 170, 30, 80)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            if 75 <= x <= 125 and 20 <= y <= 70:
                self.headClicked.emit()
            elif 70 <= x <= 130 and 80 <= y <= 160:
                self.torsoClicked.emit()
            elif 25 <= x <= 65 and 80 <= y <= 160:
                self.leftArmClicked.emit()
            elif 135 <= x <= 175 and 80 <= y <= 160:
                self.rightArmClicked.emit()
            elif 70 <= x <= 100 and 170 <= y <= 250:
                self.leftLegClicked.emit()
            elif 100 <= x <= 130 and 170 <= y <= 250:
                self.rightLegClicked.emit()