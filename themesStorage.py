# used for storing theme stylesheets.

DARK_MODE_STYLESHEET = """
QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: "Segoe UI", Arial, sans-serif;
}

QLabel {
    color: #ffffff;
    font-size: 13px;
}

QLineEdit, QComboBox {
    padding: 10px;
    border: 2px solid #404040;
    border-radius: 8px;
    background-color: #262626;
    min-width: 280px;
    font-size: 13px;
    selection-background-color: #007acc;
    selection-color: #ffffff;
}

QLineEdit:focus, QComboBox:focus {
    border-color: #0088ff;
    background-color: #2c2c2c;
    outline: none;
}

QPushButton {
    padding: 9px 25px;
    border: none;
    border-radius: 6px;
    background-color: #007acc;
    color: white;
    font-size: 13px;
    font-weight: 500;
    min-width: 160px;
    text-align: center;
}

QPushButton:hover {
    background-color: #0088ff;
    box-shadow: 0 1px 3px rgba(0, 122, 204, 0.3);
}

QPushButton:pressed {
    background-color: #0066b3;
    padding-top: 10px;
    padding-bottom: 7px;
}

QTabWidget::pane {
    border: none;
    margin-top: 8px;
}

QTabBar::tab {
    padding: 12px 25px;
    background: #262626;
    color: #aaaaaa;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 4px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: #2a2a2a;
    color: #ffffff;
    border-bottom: 3px solid #007acc;
}

QTabBar::tab:!selected {
    border-bottom: 3px solid transparent;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #404040;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}

QComboBox::down-arrow {
    image: url("||arrow_svg||");
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background: #262626;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 5px;
    outline: none;
    selection-background-color: #007acc;
    selection-color: white;
    margin: 2px;
}

QComboBox QAbstractItemView::item {
    padding: 6px 10px;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #0055a5;
    color: white;
}
"""

LIGHT_MODE_STYLESHEET = """
QWidget {
    background-color: #ffffff;
    color: #2b2b2b;
    font-family: "Segoe UI", Arial, sans-serif;
}

QLabel {
    color: #2b2b2b;
    font-size: 13px;
}

QLineEdit, QComboBox {
    padding: 10px;
    border: 2px solid #d0d0d0;
    border-radius: 8px;
    background-color: #fafafa;
    min-width: 280px;
    font-size: 13px;
    selection-background-color: #6699cc;
    selection-color: white;
}

QLineEdit:focus, QComboBox:focus {
    border-color: #5a8fcc;
    background-color: #f5f9ff;
    outline: none;
}

QPushButton {
    padding: 9px 25px;
    border: none;
    border-radius: 6px;
    background-color: #6699cc;
    color: white;
    font-size: 13px;
    font-weight: 500;
    min-width: 160px;
    text-align: center;
}

QPushButton:hover {
    background-color: #5a8fcc;
    box-shadow: 0 1px 3px rgba(90, 143, 204, 0.2);
}

QPushButton:pressed {
    background-color: #4d7dbf;
    padding-top: 10px;
    padding-bottom: 7px;
}

QTabWidget::pane {
    border: none;
    margin-top: 8px;
}

QTabBar::tab {
    padding: 12px 25px;
    background: #f0f0f0;
    color: #555555;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 4px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #2b2b2b;
    border-bottom: 3px solid #6699cc;
}

QTabBar::tab:!selected {
    border-bottom: 3px solid transparent;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #d0d0d0;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}

QComboBox::down-arrow {
    image: url("||arrow_svg||");
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 5px;
    outline: none;
    selection-background-color: #6699cc;
    selection-color: white;
    margin: 2px;
}

QComboBox QAbstractItemView::item {
    padding: 6px 10px;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #e6f0fa;
    color: #2b2b2b;
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