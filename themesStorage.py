# used for storing theme stylesheets.

DARK_MODE_STYLESHEET = """
QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
}
QLabel {
    color: #ffffff;
}
QLineEdit, QComboBox {
    padding: 10px;
    border: 2px solid #404040;
    border-radius: 6px;
    background-color: #262626;
    min-width: 280px;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #007acc;
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
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    padding: 12px 25px;
    background: #262626;
    color: #a0a0a0;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background: #2a2a2a;
    color: #ffffff;
    border-bottom: 3px solid #007acc;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #404040;
}
QComboBox::down-arrow {
    image: url("||arrow_svg||");
    width: 12px;
    height: 12px;
}
QComboBox QAbstractItemView {
    background: #262626;
    selection-background-color: #007acc;
}
"""

LIGHT_MODE_STYLESHEET = """
QWidget {
    background-color: #ffffff;
    color: #000000;
}
QLabel {
    color: #000000;
}
QLineEdit, QComboBox {
    padding: 10px;
    border: 2px solid #cccccc;
    border-radius: 6px;
    background-color: #f0f0f0;
    min-width: 280px;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #6699cc;
}
QPushButton {
    padding: 8px 25px;
    border: none;
    border-radius: 5px;
    background-color: #6699cc;
    color: white;
    font-size: 13px;
    min-width: 160px;
}
QPushButton:hover {
    background-color: #5588bb;
}
QPushButton:pressed {
    background-color: #4477aa;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    padding: 12px 25px;
    background: #f0f0f0;
    color: #333333;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background: #e0e0e0;
    color: #000000;
    border-bottom: 3px solid #6699cc;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #cccccc;
}
QComboBox::down-arrow {
    image: url("||arrow_svg||");
    width: 12px;
    height: 12px;
}
QComboBox QAbstractItemView {
    background: #f0f0f0;
    selection-background-color: #6699cc;
}
"""

AVATAR_TAB_STYLESHEET = """
QLineEdit {
    min-width: 100px;
}
QLabel {
    min-width: 50px;
    padding-right: 5px;
    text-align: right;
}
"""

PLACE_LABEL_STYLESHEET = "QLabel { margin-left: 8px; }"