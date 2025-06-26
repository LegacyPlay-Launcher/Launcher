from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QGridLayout, QDialog, QScrollArea
)
from PySide6.QtCore import Qt, Signal

from misc import *

class ColorPickerDialog(QDialog):
    colorSelected = Signal(int)

    def __init__(self, parent=None, dark_mode=False) -> None:
        super().__init__(parent)
        self.setWindowTitle("Color Picker")
        self.setFixedSize(600, 400)
        self.setModal(True)

        self.t = theme_color_picker["dark"] if dark_mode else theme_color_picker["light"]

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.t['primary']};
                color: {self.t['text']};
            }}
            QScrollBar:horizontal {{
                background: {self.t['secondary']};
                height: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.t['scrollbar']};
                min-width: 30px;
                border-radius: 5px;
            }}
            QToolTip {{
                background-color: {self.t['tooltip_bg']};
                color: {self.t['tooltip_text']};
                padding: 5px;
                border-radius: 4px;
                border: 1px solid {self.t['border']};
                font: 11pt 'Segoe UI';
            }}
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(5, 5, 5, 5)
        
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

        self.populate_colors()

        print("ColorPickerDialog initialization success.")

    def populate_colors(self) -> None:
        row = col = 0
        columns = 12
        
        for color_id, color_info in brick_colors.items():
            btn = QPushButton()
            btn.setToolTip(f"{color_info['name']} (#{color_id})")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_info['hex']};
                    border: 1px solid {self.t['border']};
                    border-radius: 2px;
                    margin: 2px;
                }}
                QPushButton:hover {{
                    border: 2px solid {self.t['hover']};
                }}
            """)

            btn.clicked.connect(lambda _, cid=color_id: (self.colorSelected.emit(cid), self.accept()))
            self.grid.addWidget(btn, row, col)
            
            col += 1
            if col >= columns:
                col = 0
                row += 1