import os
import random
import json
import datetime
import webbrowser
import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QFormLayout, QHBoxLayout, QFileDialog, QMessageBox, QTabWidget, QSpacerItem, QCheckBox,
    QGridLayout, QDialog, QScrollArea, QDialogButtonBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, Signal

from clientUtilities.clientManager import ClientManager
from launcherUtilities.webserverManager import WebServerManager
from launcherUtilities.widgets import AvatarWidget
from launcherUtilities.cookieGrabber import CookieGrabber

discord_url = "https://discord.gg/vMjXzuKqs5"

brick_colors = {
    1: {"name": "White", "hex": "#F2F3F3"},
    2: {"name": "Grey", "hex": "#A1A5A2"},
    3: {"name": "Light yellow", "hex": "#F9E999"},
    5: {"name": "Brick yellow", "hex": "#D7C59A"},
    6: {"name": "Light green (Mint)", "hex": "#C2DAB9"},
    9: {"name": "Light reddish violet", "hex": "#E8BCC8"},
    11: {"name": "Pastel Blue", "hex": "#80BBD9"},
    12: {"name": "Light orange brown", "hex": "#CC8541"},
    18: {"name": "Nougat", "hex": "#CC8E69"},
    21: {"name": "Bright red", "hex": "#C4281C"},
    22: {"name": "Medium reddish violet", "hex": "#C470A0"},
    23: {"name": "Bright blue", "hex": "#0D69AC"},
    24: {"name": "Bright yellow", "hex": "#F5CD30"},
    25: {"name": "Earth orange", "hex": "#624732"},
    26: {"name": "Black", "hex": "#1B2A35"},
    27: {"name": "Dark grey", "hex": "#6D6E6C"},
    28: {"name": "Dark green", "hex": "#A28F47"},
    29: {"name": "Medium green", "hex": "#A2C58C"},
    36: {"name": "Light yellowish orange", "hex": "#F3CF9B"},
    37: {"name": "Bright green", "hex": "#4B976B"},
    38: {"name": "Dark orange", "hex": "#A05F35"},
    39: {"name": "Light bluish violet", "hex": "#C1CADF"},
    40: {"name": "Transparent", "hex": "#ECECEC"},
    41: {"name": "Tr. Red", "hex": "#CD544B"},
    42: {"name": "Tr. Light blue", "hex": "#C1DFF0"},
    43: {"name": "Tr. Blue", "hex": "#7BB6E8"},
    44: {"name": "Tr. Yellow", "hex": "#F7F18D"},
    45: {"name": "Light blue", "hex": "#B4D2E4"},
    47: {"name": "Tr. Fluorescent Reddish orange", "hex": "#D9856C"},
    48: {"name": "Tr. Green", "hex": "#84B68D"},
    49: {"name": "Tr. Fluorescent Green", "hex": "#F8F184"},
    50: {"name": "Phosphorescent White", "hex": "#ECE8DE"},
    100: {"name": "Light red", "hex": "#EEC4B6"},
    101: {"name": "Medium red", "hex": "#DA867A"},
    102: {"name": "Medium blue", "hex": "#6E99CA"},
    103: {"name": "Light grey", "hex": "#C7C1B7"},
    104: {"name": "Bright violet", "hex": "#6B327C"},
    105: {"name": "Bright yellowish orange", "hex": "#E29B40"},
    106: {"name": "Bright orange", "hex": "#DA8541"},
    107: {"name": "Bright bluish green", "hex": "#00939C"},
    108: {"name": "Earth yellow", "hex": "#685C43"},
    110: {"name": "Bright bluish violet", "hex": "#435493"},
    111: {"name": "Transparent Brown", "hex": "#BFB7B1"},
    112: {"name": "Medium bluish violet", "hex": "#6874AC"},
    113: {"name": "Transparent Medium reddish violet", "hex": "#E5ADC8"},
    115: {"name": "Medium yellowish green", "hex": "#C7D23C"},
    116: {"name": "Medium bluish green", "hex": "#55A5AF"},
    118: {"name": "Light bluish green", "hex": "#B7D7D5"},
    119: {"name": "Bright yellowish green", "hex": "#A4BD47"},
    120: {"name": "Light yellowish green", "hex": "#D9E4A7"},
    121: {"name": "Medium yellowish orange", "hex": "#E7AC58"},
    123: {"name": "Bright reddish orange", "hex": "#D36F4C"},
    124: {"name": "Bright reddish violet", "hex": "#923978"},
    125: {"name": "Light orange", "hex": "#EAB98E"}
}

class ColorPickerDialog(QDialog):
    colorSelected = Signal(int)

    def __init__(self, parent=None, dark_mode=False):
        super().__init__(parent)
        self.setWindowTitle("Choose a color!")
        self.setFixedSize(600, 400)
        self.setModal(True)

        theme = {
            "dark": {
                "primary": "#1a1a1a",
                "secondary": "#2d2d2d",
                "text": "#e0e0e0",
                "border": "#404040",
                "hover": "#007acc",
                "scrollbar": "#606060",
                "tooltip_bg": "#505050",
                "tooltip_text": "#ffffff"
            },
            "light": {
                "primary": "#ffffff",
                "secondary": "#f8f9fa",
                "text": "#212529",
                "border": "#dee2e6",
                "hover": "#007acc",
                "scrollbar": "#dee2e6",
                "tooltip_bg": "#ffffff",
                "tooltip_text": "#212529"
            }
        }
        self.t = theme["dark"] if dark_mode else theme["light"]

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

        self.title_label = QLabel("Choose a color!")
        self.title_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
        self.layout.addWidget(self.title_label)

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

    def populate_colors(self):
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

class GUIInterface(QWidget):
    RANDOM_PHRASES = [
        "Welcome to LegacyPlay!",
        "LegacyPlay creators hope you will enjoy it.",
        "Reviving classic ROBLOX experience",
        "Preserving retro clients since early 2025",
        "Version: Beta 0.784 | Build Date 0806",
        "Open-Source. Local. Retro.",
        "Powered by Python with the help of Qt 6/PySide6",
        f"You've launched LegacyPlay on {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "The official LegacyPlay Build",
        "Thank you for playing LegacyPlay 💙",
        "Go to the About tab to change your cookie!",
        "LegacyPlay was created on 01/01/2025.",
        "LegacyPlay wishes you a great gameplay!",
        "LegacyPlay has 2010L - 2014L.",
        "LegacyPlay was created by VMsLover on Discord.",
        f"Join our Discord! {discord_url}"
    ]

    def __init__(self, webserver_manager: WebServerManager, cookie_grabber: CookieGrabber):
        super().__init__()
        self.webserver_manager = webserver_manager
        self.cookie_grabber = cookie_grabber
        self.clManager = ClientManager(self.webserver_manager, self)
        self.setWindowTitle("LegacyPlay")
        self.setFixedSize(720, 600)
        self.icon = QIcon("./Assets/IconSmall.png")
        self.setWindowIcon(self.icon)
        self._place_file_path = None
        self.user_data_file = "./Data/user_data.json"
        self.launcher_data_file = "./Data/launcher_data.json"
        self.body_colors = [1, 1, 1, 1, 1, 1]
        self.shirtId = "0"
        self.pantsId = "0"
        self.shirt_id_input = None
        self.pants_id_input = None
        self.dark_mode = True
        self.load_user_data()
        self.load_launcher_data()
        self.check_roblox_cookie()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_launch_tab(), "Launch")
        self.tabs.addTab(self.create_settings_tab(), "Settings")
        self.tabs.addTab(self.create_launcher_settings_tab(), "Launcher Settings")
        self.tabs.addTab(self.create_avatar_tab(), "Avatar")
        self.tabs.addTab(self.create_about_tab(), "About")

        self.save_user_data()

        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.apply_avatar_colors()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.rpc = None
        self.apply_theme()

        print("GUIInterface initialization success.")

    def get_current_tab_index(self):
        return self.tabs.currentIndex()

    def setRPC(self, rpcClass):
        self.rpc = rpcClass
        self.clManager.setRPC(rpcClass)

    def create_launch_tab(self):
        launch_tab = QWidget()
        main_layout = QVBoxLayout(launch_tab)
        
        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("LegacyPlay")
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        subtext = QLabel(random.choice(self.RANDOM_PHRASES))
        subtext.setFont(QFont('Segoe UI', 10))
        subtext.setStyleSheet("color: #a0a0a0;")
        subtext.setAlignment(Qt.AlignCenter)

        form_widget = QWidget()
        form_widget.setMaximumWidth(400)
        form_layout = QFormLayout(form_widget)
        form_layout.setVerticalSpacing(12)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        self.ip_field = QLineEdit("127.0.0.1")
        self.port_field = QLineEdit("53640")
        self.client_select = QComboBox()
        
        form_layout.addRow("Server IP:", self.ip_field)
        form_layout.addRow("Server Port:", self.port_field)
        form_layout.addRow("Client Version:", self.client_select)
        
        button_container = QHBoxLayout()
        play_btn = QPushButton("Start Playing")
        host_btn = QPushButton("Host Server")
        play_btn.setFixedHeight(40)
        host_btn.setFixedHeight(40)
        button_container.addWidget(play_btn)
        button_container.addWidget(host_btn)
        
        layout.addWidget(title)
        layout.addWidget(subtext)
        layout.addSpacing(20)
        layout.addWidget(form_widget)
        layout.addSpacing(30)
        layout.addLayout(button_container)
        
        main_layout.addStretch()
        main_layout.addWidget(center_widget)
        main_layout.addStretch()
        
        host_btn.clicked.connect(self.prepareHost)
        play_btn.clicked.connect(self.preparePlay)
        self.client_select.currentIndexChanged.connect(self.on_combobox_changed)
        
        return launch_tab

    def create_settings_tab(self):
        settings_tab = QWidget()
        main_layout = QVBoxLayout(settings_tab)
        
        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("User Configuration")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        form_widget = QWidget()
        form_widget.setMaximumWidth(400)
        form_layout = QFormLayout(form_widget)
        form_layout.setVerticalSpacing(12)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        self.settings_username_field = QLineEdit(self.username)
        self.settings_user_id_field = QLineEdit(self.user_id)
        self.place_label = QLabel("No place file selected")
        self.place_label.setMaximumWidth(280)
        self.place_label.setStyleSheet("QLabel { margin-left: 8px; }")
        
        form_layout.addRow("Username:", self.settings_username_field)
        form_layout.addRow("User ID:", self.settings_user_id_field)
        form_layout.addItem(QSpacerItem(20, 10))
        form_layout.addRow("Place File:", self.place_label)
        
        file_btn = QPushButton("Select Place File")
        file_btn.setFixedHeight(35)
        
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(form_widget)
        layout.addSpacing(15)
        layout.addWidget(file_btn, alignment=Qt.AlignCenter)
        
        main_layout.addStretch()
        main_layout.addWidget(center_widget)
        main_layout.addStretch()
        
        self.settings_username_field.editingFinished.connect(self.save_user_data)
        self.settings_user_id_field.editingFinished.connect(self.save_user_data)

        file_btn.clicked.connect(self.choose_place)
        
        return settings_tab

    def create_launcher_settings_tab(self):
        launcher_settings_tab = QWidget()
        main_layout = QVBoxLayout(launcher_settings_tab)
        
        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Launcher Settings")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        dark_mode_checkbox = QCheckBox("Dark Mode")
        dark_mode_checkbox.setChecked(self.dark_mode)
        dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        dark_mode_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox {{
                spacing: 10px;
                font-size: 14px;
            }}
        """)
        
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(dark_mode_checkbox, alignment=Qt.AlignCenter)
        
        main_layout.addStretch()
        main_layout.addWidget(center_widget)
        main_layout.addStretch()
        
        return launcher_settings_tab

    def create_avatar_tab(self):
        avatar_tab = QWidget()
        layout = QVBoxLayout(avatar_tab)
        
        title = QLabel("Avatar")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtext = QLabel("To use multiple avatar items, seperate hat IDs using a semi-colon.")
        subtext.setFont(QFont('Segoe UI', 10))
        subtext.setStyleSheet("color: #a0a0a0;")
        subtext.setAlignment(Qt.AlignCenter)

        self.avatar_widget = AvatarWidget()
        self.avatar_widget.setFixedSize(200, 300)
        self.avatar_widget.setStyleSheet("background-color: transparent;")

        self.avatar_widget.headClicked.connect(lambda: self.open_color_picker('head'))
        self.avatar_widget.torsoClicked.connect(lambda: self.open_color_picker('torso'))
        self.avatar_widget.leftArmClicked.connect(lambda: self.open_color_picker('left_arm'))
        self.avatar_widget.rightArmClicked.connect(lambda: self.open_color_picker('right_arm'))
        self.avatar_widget.leftLegClicked.connect(lambda: self.open_color_picker('left_leg'))
        self.avatar_widget.rightLegClicked.connect(lambda: self.open_color_picker('right_leg'))

        ids_layout = QVBoxLayout()

        hat_id_layout = QHBoxLayout()
        hat_id_label = QLabel("Hat IDs:")
        hat_id_input = QLineEdit()
        hat_id_layout.addWidget(hat_id_label)
        hat_id_layout.addWidget(hat_id_input)

        shirt_id_layout = QHBoxLayout()
        shirt_id_label = QLabel("Shirt ID:")
        self.shirt_id_input = QLineEdit(self.shirtId)
        shirt_id_layout.addWidget(shirt_id_label)
        shirt_id_layout.addWidget(self.shirt_id_input)

        pants_id_layout = QHBoxLayout()
        pants_id_label = QLabel("Pants ID:")
        self.pants_id_input = QLineEdit(self.pantsId)
        pants_id_layout.addWidget(pants_id_label)
        pants_id_layout.addWidget(self.pants_id_input)

        self.load_user_data()

        self.shirt_id_input.textChanged.connect(self.on_id_changed)
        self.pants_id_input.textChanged.connect(self.on_id_changed)

        ids_layout.addLayout(hat_id_layout)
        ids_layout.addLayout(shirt_id_layout)
        ids_layout.addLayout(pants_id_layout)

        avatar_id_layout = QHBoxLayout()
        avatar_id_layout.addWidget(self.avatar_widget, alignment=Qt.AlignLeft)
        avatar_id_layout.addLayout(ids_layout)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtext)
        layout.addSpacing(20)
        layout.addLayout(avatar_id_layout)
        layout.addStretch()

        avatar_tab.setStyleSheet("""
            QLineEdit {
                min-width: 100px;
            }
            QLabel {
                min-width: 50px;
                padding-right: 5px;
                text-align: right;
            }
        """)
        
        return avatar_tab
    
    def create_about_tab(self):
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)
        
        title = QLabel("About LegacyPlay")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        content = QLabel(
            "LegacyPlay Launcher Application\n\n"
            "Version: Beta 0.784 | Build Date 0806\n"
            f"Compiled using Python {sys.version_info.major}.{sys.version_info.minor}\n"
            "Graphics Framework used: Qt 6/PySide6\n"
        )
        content.setFont(QFont('Segoe UI', 11))
        content.setAlignment(Qt.AlignCenter)

        link_label = QLabel(
            "If assets don't work, <a href=\"#change_cookie\" style=\"text-decoration: underline; color: #007acc;\">click here</a> to change the cookie.<br>"
        )
        link_label.setFont(QFont('Segoe UI', 11))
        link_label.setAlignment(Qt.AlignCenter)
        link_label.setTextFormat(Qt.RichText)
        link_label.setOpenExternalLinks(False)
        link_label.linkActivated.connect(self.change_cookie)

        link_label2 = QLabel(
            "Join our <a href=\"#discord_server\" style=\"text-decoration: underline; color: #007acc;\">Discord community server</a> to stay updated!"
        )
        link_label2.setFont(QFont('Segoe UI', 11))
        link_label2.setAlignment(Qt.AlignCenter)
        link_label2.setTextFormat(Qt.RichText)
        link_label2.setOpenExternalLinks(False)
        link_label2.linkActivated.connect(self.open_discord_url)

        footer = QLabel(
            "\n© 2025 LegacyPlay Development Team\n\n"
            "We do not own the client binaries, all credits go to the Roblox Corporation."
        )
        footer.setFont(QFont('Segoe UI', 11))
        footer.setAlignment(Qt.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(content)
        layout.addWidget(link_label)
        layout.addWidget(link_label2)
        layout.addWidget(footer)
        layout.addStretch()
        
        return about_tab
    
    def get_current_theme_colors(self):
        return {
            "dark": {
                "primary": "#1a1a1a",
                "secondary": "#262626",
                "text": "#e0e0e0",
                "border": "#404040",
                "hover": "#007acc",
                "tooltip_bg": "#505050",
                "tooltip_text": "#ffffff"
            },
            "light": {
                "primary": "#ffffff",
                "secondary": "#f8f9fa",
                "text": "#212529",
                "border": "#dee2e6",
                "hover": "#6699cc",
                "tooltip_bg": "#ffffff",
                "tooltip_text": "#212529"
            }
        }["dark" if self.dark_mode else "light"]

    def darken_color(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_color_picker(self, part):
        dialog = ColorPickerDialog(self, dark_mode=self.dark_mode)
        dialog.colorSelected.connect(lambda cid: self.update_avatar_color(part, cid))
        dialog.exec()
    
    def update_avatar_color(self, part, color_id):
        print(f"Color change received for {part} - ID: {color_id if color_id else None}")
        
        part_indices = {
            'head': 0, 'right_arm': 1, 'torso': 2,
            'left_arm': 3, 'right_leg': 4, 'left_leg': 5
        }
        
        try:
            color_id = int(color_id)
            color_info = brick_colors.get(color_id, brick_colors[1])
        except (ValueError, KeyError):
            color_id = 1
            color_info = brick_colors[1]
        
        index = part_indices.get(part, 0)
        self.body_colors[index] = color_id

        setattr(self.avatar_widget, f"{part}_color", color_info['hex'])
        self.avatar_widget.update()
        
        print(f"Current colors: {self.body_colors}")
        self.save_user_data()

    def apply_avatar_colors(self):
        try:
            self.body_colors = [int(c) for c in self.body_colors]
        except (ValueError, TypeError):
            self.body_colors = [1, 1, 1, 1, 1, 1]
        
        parts = ['head', 'right_arm', 'torso', 'left_arm', 'right_leg', 'left_leg']
        
        for i, part in enumerate(parts):
            color_id = self.body_colors[i]
            color_info = brick_colors.get(color_id, brick_colors[1])
            hex_color = color_info['hex']
            setattr(self.avatar_widget, f"{part}_color", hex_color)
        
        self.avatar_widget.update()
    
    def on_tab_changed(self, index):
        tab_names = {
            0: "in the launch menu",
            1: "configuring settings",
            2: "updating launcher settings",
            3: "customizing avatar",
            4: "viewing the about page"
        }
        if self.rpc and not self.clManager.isPlaying:
            self.rpc.updatePresence(tab_names.get(index, 'unknown').capitalize())

    def load_stylesheet(self, arrow_svg):
        return f"""
        QWidget {{
            background-color: #1a1a1a;
            color: #e0e0e0;
        }}
        QLabel {{
            color: #ffffff;
        }}
        QLineEdit, QComboBox {{
            padding: 10px;
            border: 2px solid #404040;
            border-radius: 6px;
            background-color: #262626;
            min-width: 280px;
            font-size: 13px;
        }}
        QLineEdit:focus, QComboBox:focus {{
            border-color: #007acc;
        }}
        QPushButton {{
            padding: 8px 25px;
            border: none;
            border-radius: 5px;
            background-color: #007acc;
            color: white;
            font-size: 13px;
            min-width: 160px;
        }}
        QPushButton:hover {{
            background-color: #006bb3;
        }}
        QPushButton:pressed {{
            background-color: #005c99;
        }}
        QTabWidget::pane {{
            border: none;
        }}
        QTabBar::tab {{
            padding: 12px 25px;
            background: #262626;
            color: #a0a0a0;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            margin-right: 4px;
        }}
        QTabBar::tab:selected {{
            background: #2a2a2a;
            color: #ffffff;
            border-bottom: 3px solid #007acc;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 1px solid #404040;
        }}
        QComboBox::down-arrow {{
            image: url({arrow_svg});
            width: 12px;
            height: 12px;
        }}
        QComboBox QAbstractItemView {{
            background: #262626;
            selection-background-color: #007acc;
        }}
        """

    def load_user_data(self):
        default_data = {
            "username": f"LegacyUser_{random.randint(1000, 9999)}",
            "user_id": str(random.randint(10000000, 99999999)),
            "bodyColors": [1, 1, 1, 1, 1, 1],
            "shirtId": "0",
            "pantsId": "0"
        }
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r') as f:
                    data = json.load(f)
                    self.username = data.get("username", default_data["username"])
                    self.user_id = data.get("user_id", default_data["user_id"])
                    self.body_colors = data.get("bodyColors", default_data["bodyColors"])

                    if len(self.body_colors) != 6 or not all(isinstance(x, int) for x in self.body_colors):
                        self.body_colors = default_data["bodyColors"]

                    self.shirtId = data.get("shirtId", default_data["shirtId"])
                    self.pantsId = data.get("pantsId", default_data["pantsId"])
            else:
                self.username = default_data["username"]
                self.user_id = default_data["user_id"]
                self.body_colors = default_data["bodyColors"]
                self.shirtId = default_data["shirtId"]
                self.pantsId = default_data["pantsId"]
        except Exception:
            self.username = default_data["username"]
            self.user_id = default_data["user_id"]
            self.body_colors = default_data["bodyColors"]
            self.shirtId = default_data["shirtId"]
            self.pantsId = default_data["pantsId"]

        print(f"Current colors: {self.body_colors}")

    def on_id_changed(self):
        self.shirtId = self.shirt_id_input.text()
        self.pantsId = self.pants_id_input.text()

        self.save_user_data()

    def save_user_data(self):
        data = {
            "username": self.settings_username_field.text(),
            "user_id": self.settings_user_id_field.text(),
            "bodyColors": [int(c) for c in self.body_colors],
            "shirtId": self.shirt_id_input.text() if self.shirt_id_input else "0",
            "pantsId": self.pants_id_input.text() if self.pants_id_input else "0"
        }

        if len(data["bodyColors"]) != 6:
            data["bodyColors"] = [1, 1, 1, 1, 1, 1]
        
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_launcher_data(self):
        default_data = {
            "dark_mode": True,
            "robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87": ""
        }
        try:
            if os.path.exists(self.launcher_data_file):
                with open(self.launcher_data_file, 'r') as f:
                    data = json.load(f)
                    self.dark_mode = data.get("dark_mode", default_data["dark_mode"])
                    self.roblox_cookie = data.get("robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87", default_data["robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87"])
            else:
                self.dark_mode = default_data["dark_mode"]
                self.roblox_cookie = default_data["robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87"]
        except Exception:
            self.dark_mode = default_data["dark_mode"]
            self.roblox_cookie = default_data["robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87"]

    def save_launcher_data(self):
        data = {
            "dark_mode": self.dark_mode,
            "robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87": self.roblox_cookie
        }
        with open(self.launcher_data_file, 'w') as f:
            json.dump(data, f)

    def choose_place(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Place File", "", 
            "Roblox Files (*.rbxl *.rbxlx);;All Files (*)"
        )
        if file_name:
            self._place_file_path = file_name
            self.place_label.setText(os.path.basename(file_name))

    def open_discord_url(self):
        webbrowser.open(discord_url)

    def change_cookie(self):
        self.prompt_for_roblox_cookie(initial=False)

    def check_roblox_cookie(self):
        if not self.roblox_cookie:
            print(".ROBLOSECURITY cookie is required, prompting...")
            self.prompt_for_roblox_cookie(initial=True)
        else:
            print("Cookie is in the launcher data file, no action needed.")

    def retrieve_cookie_auto(self, input_field: QLineEdit):
        theme = self.get_current_theme_colors()
        retrieved_cookie = self.cookie_grabber.get_cookie_from_system()

        message_box_style = f"""
            QMessageBox {{
                background-color: {theme['primary']};
                color: {theme['text']};
            }}
            QMessageBox QLabel {{
                color: {theme['text']};
                font-size: 13px;
            }}
            QMessageBox QPushButton {{
                padding: 8px 25px;
                border: none;
                border-radius: 5px;
                background-color: {theme['hover']};
                color: white;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {self.darken_color(theme['hover'], 0.9)};
            }}
            QMessageBox QPushButton:pressed {{
                background-color: {self.darken_color(theme['hover'], 0.8)};
            }}
        """

        if not retrieved_cookie:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Failed")
            msg_box.setText("Failed to retrieve the cookie automatically, please get one yourself from https://www.roblox.com/.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet(message_box_style)
            msg_box.exec()
            return
        
        input_field.setText(retrieved_cookie)

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Successfully retrieved cookie! You may continue now by pressing the \"Save Cookie\" button.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(message_box_style)
        msg_box.exec()

    def prompt_for_roblox_cookie(self, initial=True):
        theme = self.get_current_theme_colors()
        dialog = QDialog(self)
        dialog.setWindowTitle("Action Required" if initial else "Change Roblox Cookie")
        dialog.setWindowIcon(self.icon)
        dialog.setFixedSize(500, 230)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['primary']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 8px;
            }}
            QLabel {{
                color: {theme['text']};
                font-size: 13px;
            }}
            QLineEdit {{
                background-color: {theme['secondary']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 8px;
                color: {theme['text']};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {theme['hover']};
            }}
            QPushButton {{
                padding: 8px 25px;
                border: none;
                border-radius: 5px;
                background-color: {theme['hover']};
                color: white;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(theme['hover'], 0.9)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(theme['hover'], 0.8)};
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_label = QLabel("Roblox Cookie is required" if initial else "Change your Roblox Cookie.")
        title_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        info_label = QLabel(
            "LegacyPlay requires your .ROBLOSECURITY cookie for Roblox APIs authentication. This will be stored locally and only used for assets downloading.\n"
            if initial else
            "You can change your .ROBLOSECURITY cookie below. This will be stored locally and only used for assets downloading.\n"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)

        input_field = QLineEdit()
        input_field.setPlaceholderText("Paste your .ROBLOSECURITY cookie here...")
        input_field.setEchoMode(QLineEdit.Password)
        input_field.setMinimumHeight(40)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        auto_button = QPushButton("Retrieve it")
        auto_button.setFixedSize(100, 32)
        auto_button.clicked.connect(lambda: self.retrieve_cookie_auto(input_field))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        button_box.button(QDialogButtonBox.Ok).setText("Save Cookie")
        button_box.button(QDialogButtonBox.Ok).setFixedSize(150, 32)
        button_box.button(QDialogButtonBox.Cancel).setText("Exit")
        button_box.button(QDialogButtonBox.Cancel).setFixedSize(100, 32)
        button_box.accepted.connect(lambda: self.save_cookie_and_close(input_field.text(), dialog))

        if initial:
            button_box.rejected.connect(lambda: self.close_app_with_warning(dialog))
        else:
            button_box.rejected.connect(dialog.reject)

        buttons_layout.addWidget(auto_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(button_box)

        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addWidget(input_field)
        layout.addLayout(buttons_layout)

        if initial:
            def reject():
                pass
            dialog.reject = reject
            dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)
            dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        dialog.exec()

    def save_cookie_and_close(self, cookie, dialog):
        theme = self.get_current_theme_colors()

        if not cookie:
            print("Cookie is empty.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid Input")
            msg.setText("Cookie cannot be empty!")
            msg.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme['primary']};
                    color: {theme['text']};
                }}
                QLabel {{
                    color: {theme['text']};
                    font-size: 13px;
                }}
                QPushButton {{
                    padding: 8px 25px;
                    border: none;
                    border-radius: 5px;
                    background-color: {theme['hover']};
                    color: white;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(theme['hover'], 0.9)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(theme['hover'], 0.8)};
                }}
            """)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.exec()
            return
        elif not cookie.startswith("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|"):
            print("Invalid cookie.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid Input")
            msg.setText("This is not a valid .ROBLOSECURITY cookie!")
            msg.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme['primary']};
                    color: {theme['text']};
                }}
                QLabel {{
                    color: {theme['text']};
                    font-size: 13px;
                }}
                QPushButton {{
                    padding: 8px 25px;
                    border: none;
                    border-radius: 5px;
                    background-color: {theme['hover']};
                    color: white;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(theme['hover'], 0.9)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(theme['hover'], 0.8)};
                }}
            """)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.exec()
            return
        
        self.roblox_cookie = cookie
        self.save_launcher_data()
        dialog.accept()

        print("Successfully saved cookie!")

    def close_app_with_warning(self, dialog):
        print("User rejected to paste the cookie, preparing to quit.")

        dialog.reject()
        
        theme = self.get_current_theme_colors()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Cookie Required")
        msg.setText("LegacyPlay requires a Roblox cookie to function properly.\n\nThe application will now exit.")
        msg.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['primary']};
                color: {theme['text']};
            }}
            QLabel {{
                color: {theme['text']};
                font-size: 13px;
            }}
            QPushButton {{
                padding: 8px 25px;
                border: none;
                border-radius: 5px;
                background-color: {theme['hover']};
                color: white;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(theme['hover'], 0.9)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(theme['hover'], 0.8)};
            }}
        """)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("Understood")
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
        msg.exec()
        
        sys.exit()

    def get_place_file_path(self):
        return self._place_file_path

    def get_client_name(self):
        return self.client_select.currentText()

    def get_ip(self):
        return self.ip_field.text()

    def get_port(self):
        return self.port_field.text()

    def addClients(self, clientsDir):
        try:
            clients = [d for d in os.listdir(clientsDir) if os.path.isdir(os.path.join(clientsDir, d))]
            self.client_select.addItems(clients)
        except Exception as e:
            print(f"Client loading error: {str(e)}")

    def on_combobox_changed(self, index):
        self.clManager.setClient(self.client_select.itemText(index))

    def prepareHost(self):
        if not self.validate_hosting():
            return
        self.webserver_manager.clear_www()
        self.webserver_manager.unzip_template_website(self.get_client_name())
        self.clManager.copy_place(self._place_file_path)
        result, message = self.clManager.host(self.get_port())
        if not result:
            self.show_error("Hosting Failed", message)

    def preparePlay(self):
        if not self.validate_connection():
            return
        
        if self.clManager.isPlaying:
            QMessageBox.warning(self, "Cannot join", "Cannot join when you are already ingame. Please try closing and try again.")
            return
        
        nonFinalCharData = ";".join(map(str, self.body_colors))
        finalCharData = f"{nonFinalCharData};{self.shirtId};{self.pantsId}"

        print(f"Final character data: {finalCharData}")
        
        self.webserver_manager.clear_www()
        self.webserver_manager.unzip_template_website(self.get_client_name())
        result, message = self.clManager.join(
            self.get_ip(), self.get_port(),
            finalCharData
        )

        if not result:
            self.show_error("Connection Failed", message)

    def validate_hosting(self):
        if not self._place_file_path:
            self.show_error("Missing File", "Please select a place file to host.")
            return False
        if not self.get_port():
            self.show_error("Invalid Port", "Please specify a valid port number.")
            return False
        return True

    def validate_connection(self):
        if not self.get_ip():
            self.show_error("Invalid IP", "Please enter a valid server address.")
            return False
        if not self.get_port():
            self.show_error("Invalid Port", "Please specify a valid port number.")
            return False
        return True

    def show_error(self, title, message):
        QMessageBox.warning(self, title, f"{message}\n\nPlease check your settings and try again.")

    def toggle_dark_mode(self, state):
        self.dark_mode = bool(state)
        self.save_launcher_data()
        self.apply_theme()

    def apply_theme(self):
        arrow_svg = './Assets/arrow-down-dark.svg' if self.dark_mode else './Assets/arrow-down-light.svg'
        if self.dark_mode:
            self.setStyleSheet(self.load_stylesheet(arrow_svg))
        else:
            self.setStyleSheet(f"""
            QWidget {{
                background-color: #ffffff;
                color: #000000;
            }}
            QLabel {{
                color: #000000;
            }}
            QLineEdit, QComboBox {{
                padding: 10px;
                border: 2px solid #cccccc;
                border-radius: 6px;
                background-color: #f0f0f0;
                min-width: 280px;
                font-size: 13px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: #6699cc;
            }}
            QPushButton {{
                padding: 8px 25px;
                border: none;
                border-radius: 5px;
                background-color: #6699cc;
                color: white;
                font-size: 13px;
                min-width: 160px;
            }}
            QPushButton:hover {{
                background-color: #5588bb;
            }}
            QPushButton:pressed {{
                background-color: #4477aa;
            }}
            QTabWidget::pane {{
                border: none;
            }}
            QTabBar::tab {{
                padding: 12px 25px;
                background: #f0f0f0;
                color: #333333;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 4px;
            }}
            QTabBar::tab:selected {{
                background: #e0e0e0;
                color: #000000;
                border-bottom: 3px solid #6699cc;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #cccccc;
            }}
            QComboBox::down-arrow {{
                image: url({arrow_svg});
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background: #f0f0f0;
                selection-background-color: #6699cc;
            }}
            """)