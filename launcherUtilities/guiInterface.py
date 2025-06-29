import os
import random
import json
from typing import Never
import webbrowser
import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QFormLayout, QHBoxLayout, QFileDialog, QMessageBox, QTabWidget, QSpacerItem, QCheckBox,
    QDialog, QDialogButtonBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

from localization import localizationTable
from themesStorage import *
from misc import *

from clientUtilities.clientManager import ClientManager
from launcherUtilities.webserverManager import WebServerManager
from launcherUtilities.widgets import AvatarWidget
from launcherUtilities.cookieGrabber import CookieGrabber
from launcherUtilities.dialogs import ColorPickerDialog

discord_url = "https://discord.gg/vMjXzuKqs5"

class GUIInterface(QWidget):
    RANDOM_PHRASES = ["NO CONTENT IS RETRIEVED"]

    def __init__(self, webserver_manager: WebServerManager, cookie_grabber: CookieGrabber) -> None:
        super().__init__()
        self.current_language = "en"
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
        self.hatIds = "0"
        self.shirtId = "0"
        self.pantsId = "0"
        self.hat_id_input = None
        self.shirt_id_input = None
        self.pants_id_input = None
        self.dark_mode = True
        self.load_user_data()
        self.load_launcher_data()

        print(f"Current Local Settings Language: {self.current_language}.")

        self.localizationTableFCLS = localizationTable.get(self.current_language, None) # localization Table For Current Local Settings

        if self.localizationTableFCLS:
            print(f"Got the localization table for the language {self.current_language}.")
        else:
            print(f"Failed to get localization table for language {self.current_language}. Falling back to en.")
            self.localizationTableFCLS = localizationTable.get("en", {})

            if self.localizationTableFCLS == {}:
                print("Everything has failed in getting the localization table, falling back to the hardcoded strings.")
            else:
                print("Got the localization table for the language en.")

        self.RANDOM_PHRASES = self.localizationTableFCLS.get("randomPhrases", ["If you see this, the localization fucked itself up. Contact VMsLover."])

        self.check_roblox_cookie()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_launch_tab(), self.localizationTableFCLS.get("title_lp_tab0", "Launch"))
        self.tabs.addTab(self.create_settings_tab(), self.localizationTableFCLS.get("title_lp_tab1", "User Configuration"))
        self.tabs.addTab(self.create_launcher_settings_tab(), self.localizationTableFCLS.get("title_lp_tab2", "Launcher Settings"))
        self.tabs.addTab(self.create_avatar_tab(), self.localizationTableFCLS.get("title_lp_tab3", "Avatar"))
        self.tabs.addTab(self.create_about_tab(), self.localizationTableFCLS.get("title_lp_tab4", "About LegacyPlay"))

        self.save_user_data()

        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.apply_avatar_colors()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.rpc = None
        self.apply_theme()

        print("GUIInterface initialization success.")

    def create_launch_tab(self) -> QWidget:
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
        
        form_layout.addRow(self.localizationTableFCLS.get("server_ip_label", "Server IP:"), self.ip_field)
        form_layout.addRow(self.localizationTableFCLS.get("server_port_label", "Server Port:"), self.port_field)
        form_layout.addRow(self.localizationTableFCLS.get("client_version_label", "Client:"), self.client_select)
        
        button_container = QHBoxLayout()
        play_btn = QPushButton(self.localizationTableFCLS.get("play_button", "Start Playing"))
        host_btn = QPushButton(self.localizationTableFCLS.get("host_button", "Host Server"))
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

    def create_settings_tab(self) -> QWidget:
        settings_tab = QWidget()
        main_layout = QVBoxLayout(settings_tab)
        
        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel(self.localizationTableFCLS.get("title_lp_tab1", "User Configuration"))
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
        self.place_label = QLabel(self.localizationTableFCLS.get("place_label_default", "No place file selected"))
        self.place_label.setMaximumWidth(280)
        self.place_label.setStyleSheet(PLACE_LABEL_STYLESHEET)
        
        form_layout.addRow(self.localizationTableFCLS.get("username_label", "Username:"), self.settings_username_field)
        form_layout.addRow(self.localizationTableFCLS.get("user_id_label", "User ID:"), self.settings_user_id_field)
        form_layout.addItem(QSpacerItem(20, 10))
        form_layout.addRow(self.localizationTableFCLS.get("place_file_label", "Place File:"), self.place_label)
        
        file_btn = QPushButton(self.localizationTableFCLS.get("select_place_button", "Select Place File"))
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

    def create_launcher_settings_tab(self) -> QWidget:
        launcher_settings_tab = QWidget()
        main_layout = QVBoxLayout(launcher_settings_tab)
        
        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel(self.localizationTableFCLS.get("title_lp_tab2", "Launcher Settings"))
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        dark_mode_checkbox = QCheckBox(self.localizationTableFCLS.get("dark_mode_label", "Dark Mode"))
        dark_mode_checkbox.setChecked(self.dark_mode)
        dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        
        dark_mode_container = QWidget()
        dark_mode_layout = QHBoxLayout(dark_mode_container)
        dark_mode_layout.addStretch()
        dark_mode_layout.addWidget(dark_mode_checkbox)
        dark_mode_layout.addStretch()
        
        language_container = QWidget()
        language_layout = QHBoxLayout(language_container)
        language_layout.setContentsMargins(0, 0, 0, 0)
        
        language_label = QLabel(self.localizationTableFCLS.get("language_label", "Language:"))
        self.language_combo = QComboBox()
        self.language_combo.setFixedWidth(200)
        
        for lang_code in localizationTable.keys():
            self.language_combo.addItem(lang_code.upper(), lang_code)
        
        current_index = self.language_combo.findData(self.current_language)
        if current_index >= 0:
            self.language_combo.setCurrentIndex(current_index)
        
        self.language_combo.currentIndexChanged.connect(self.change_language)
        
        language_layout.addStretch()
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(dark_mode_container, alignment=Qt.AlignCenter)
        layout.addSpacing(15)
        layout.addWidget(language_container, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        main_layout.addStretch()
        main_layout.addWidget(center_widget)
        main_layout.addStretch()
        
        return launcher_settings_tab

    def create_avatar_tab(self) -> QWidget:
        avatar_tab = QWidget()
        layout = QVBoxLayout(avatar_tab)
        
        title = QLabel(self.localizationTableFCLS.get("title_lp_tab3", "Avatar"))
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtext = QLabel(self.localizationTableFCLS.get("subtext_avatar_tab", "To use multiple avatar items, separate hat IDs using a semi-colon."))
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
        hat_id_label = QLabel(self.localizationTableFCLS.get("hat_ids_label", "Hat IDs:"))
        self.hat_id_input = QLineEdit(self.hatIds)
        hat_id_layout.addWidget(hat_id_label)
        hat_id_layout.addWidget(self.hat_id_input)

        shirt_id_layout = QHBoxLayout()
        shirt_id_label = QLabel(self.localizationTableFCLS.get("shirt_id_label", "Shirt ID:"))
        self.shirt_id_input = QLineEdit(self.shirtId)
        shirt_id_layout.addWidget(shirt_id_label)
        shirt_id_layout.addWidget(self.shirt_id_input)

        pants_id_layout = QHBoxLayout()
        pants_id_label = QLabel(self.localizationTableFCLS.get("pants_id_label", "Pants ID:"))
        self.pants_id_input = QLineEdit(self.pantsId)
        pants_id_layout.addWidget(pants_id_label)
        pants_id_layout.addWidget(self.pants_id_input)

        self.load_user_data()

        self.shirt_id_input.textChanged.connect(self.on_id_changed)
        self.pants_id_input.textChanged.connect(self.on_id_changed)
        self.hat_id_input.textChanged.connect(self.on_id_changed)

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

        avatar_tab.setStyleSheet(AVATAR_TAB_STYLESHEET)
        
        return avatar_tab
    
    def create_about_tab(self) -> QWidget:
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)
        
        title = QLabel(self.localizationTableFCLS.get("title_lp_tab4", "About LegacyPlay"))
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        content = QLabel(
            f"{self.localizationTableFCLS.get("subtext_about_tab", "LegacyPlay Launcher Application\n\n")}"
            f"{"\n".join(self.localizationTableFCLS.get("about_content", ["NO CONTENT IS RETRIEVED"]))}\n"
        )
        content.setFont(QFont('Segoe UI', 11))
        content.setAlignment(Qt.AlignCenter)

        link_label = QLabel(
            self.localizationTableFCLS.get("link_label", "If assets don't work, <a href=\"#change_cookie\" style=\"text-decoration: underline; color: #007acc;\">click here</a> to change the cookie.<br>")
        )
        link_label.setFont(QFont('Segoe UI', 11))
        link_label.setAlignment(Qt.AlignCenter)
        link_label.setTextFormat(Qt.RichText)
        link_label.setOpenExternalLinks(False)
        link_label.linkActivated.connect(self.change_cookie)

        link_label2 = QLabel(
            self.localizationTableFCLS.get("link_label2", "Join our <a href=\"#discord_server\" style=\"text-decoration: underline; color: #007acc;\">Discord community server</a> to stay updated!")
        )
        link_label2.setFont(QFont('Segoe UI', 11))
        link_label2.setAlignment(Qt.AlignCenter)
        link_label2.setTextFormat(Qt.RichText)
        link_label2.setOpenExternalLinks(False)
        link_label2.linkActivated.connect(self.open_discord_url)

        footer = QLabel(
            f"\n{self.localizationTableFCLS.get("footer_about_tab", "© 2025 LegacyPlay Development Team\n\nWe do not own the client binaries, all credits go to the Roblox Corporation.")}"
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

    def change_language(self, index) -> None:
        theme = self.get_current_theme_colors()

        lang_code = self.language_combo.itemData(index)
        self.current_language = lang_code
        self.save_launcher_data()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Notification")
        msg.setText("To fully apply the localization changes, you must restart LegacyPlay.")
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

    def get_current_tab_index(self) -> int:
        return self.tabs.currentIndex()

    def setRPC(self, rpcClass) -> None:
        self.rpc = rpcClass
        self.clManager.setRPC(rpcClass)
    
    def get_current_theme_colors(self) -> dict[str, str]:
        return theme["dark" if self.dark_mode else "light"]

    def darken_color(self, hex_color, factor) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_color_picker(self, part) -> None:
        dialog = ColorPickerDialog(self, dark_mode=self.dark_mode)
        dialog.colorSelected.connect(lambda cid: self.update_avatar_color(part, cid))
        dialog.exec()
    
    def update_avatar_color(self, part, color_id) -> None:
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

    def apply_avatar_colors(self) -> None:
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
    
    def on_tab_changed(self, index) -> None:
        tab_names = {
            0: "in the launch menu",
            1: "configuring the user",
            2: "updating launcher settings",
            3: "customizing avatar",
            4: "viewing the about page"
        }
        if self.rpc and not self.clManager.isPlaying:
            self.rpc.updatePresence(tab_names.get(index, 'unknown').capitalize())

    def load_user_data(self) -> None:
        default_data = {
            "username": f"LegacyUser_{random.randint(1000, 9999)}",
            "user_id": str(random.randint(10000000, 99999999)),
            "bodyColors": [1, 1, 1, 1, 1, 1],
            "hatIds": "0",
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

                    self.hatIds = data.get("hatIds", default_data["hatIds"])
                    self.shirtId = data.get("shirtId", default_data["shirtId"])
                    self.pantsId = data.get("pantsId", default_data["pantsId"])
            else:
                self.username = default_data["username"]
                self.user_id = default_data["user_id"]
                self.body_colors = default_data["bodyColors"]
                self.hatIds = default_data["hatIds"]
                self.shirtId = default_data["shirtId"]
                self.pantsId = default_data["pantsId"]
        except Exception:
            self.username = default_data["username"]
            self.user_id = default_data["user_id"]
            self.body_colors = default_data["bodyColors"]
            self.hatIds = default_data["hatIds"]
            self.shirtId = default_data["shirtId"]
            self.pantsId = default_data["pantsId"]

        print(f"Current colors: {self.body_colors}")
        print(f"Current hat IDs: {self.hatIds}")

    def on_id_changed(self) -> None:
        self.hatId = self.hat_id_input.text()
        self.shirtId = self.shirt_id_input.text()
        self.pantsId = self.pants_id_input.text()

        self.save_user_data()

    def save_user_data(self) -> None:
        data = {
            "username": self.settings_username_field.text(),
            "user_id": self.settings_user_id_field.text(),
            "bodyColors": [int(c) for c in self.body_colors],
            "hatIds": self.hat_id_input.text() if self.hat_id_input else "0",
            "shirtId": self.shirt_id_input.text() if self.shirt_id_input else "0",
            "pantsId": self.pants_id_input.text() if self.pants_id_input else "0"
        }

        if len(data["bodyColors"]) != 6:
            data["bodyColors"] = [1, 1, 1, 1, 1, 1]
        
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_launcher_data(self) -> None:
        default_data = {
            "dark_mode": True,
            "language": "en",
            "robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87": ""
        }
        try:
            if os.path.exists(self.launcher_data_file):
                with open(self.launcher_data_file, 'r') as f:
                    data = json.load(f)
                    self.dark_mode = data.get("dark_mode", default_data["dark_mode"])
                    self.current_language = data.get("language", default_data["language"])
                    self.roblox_cookie = data.get("robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87", default_data["robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87"])
            else:
                self.dark_mode = default_data["dark_mode"]
                self.current_language = default_data["language"]
                self.roblox_cookie = default_data["robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87"]
        except Exception:
            self.dark_mode = default_data["dark_mode"]
            self.current_language = default_data["language"]
            self.roblox_cookie = default_data["robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87"]

    def save_launcher_data(self) -> None:
        data = {
            "dark_mode": self.dark_mode,
            "language": self.current_language,
            "robloxCookie_cc434b1ae21827962753dcb87aa9f49e2e18fc273e8d2f73b955b8e37abd4c47ca0bf5e6a9f4098fe8333d4a52ed26e221f234a493ab10ce241d4b5bf72d57db3f1df9ad3ae40bb03b2cfece398e1fd446a718055fc18e946c2e087cd0a415647ff84fce855ea0edd665fdc56df2fc7f7ba7c7c959b501a88ec8331c0137fde9fb5bd6de71492dfb4ba63d2eb9cb2b97b98151c37fe46771dfcda74cd460b602a9422d648177d89ac32b47c136d122f0a97b6d038e6058e22f59cfb5c4ebe40027a55cc6a0581768b5161e36f61549ab6a6a4f6c6992b0ea2b0e508032e36986668f9a4f1a81f07f3a2167758857fbcbfe67e10001e5f6d4539762aa41090a87": self.roblox_cookie
        }
        with open(self.launcher_data_file, 'w') as f:
            json.dump(data, f)

    def choose_place(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Place File", "", 
            "Roblox Files (*.rbxl *.rbxlx);;All Files (*)"
        )
        if file_name:
            self._place_file_path = file_name
            self.place_label.setText(os.path.basename(file_name))

    def open_discord_url(self) -> None:
        webbrowser.open(discord_url)

    def change_cookie(self) -> None:
        self.prompt_for_roblox_cookie(initial=False)

    def check_roblox_cookie(self) -> None:
        if not self.roblox_cookie:
            print(".ROBLOSECURITY cookie is required, prompting...")
            self.prompt_for_roblox_cookie(initial=True)
        else:
            print("Cookie is in the launcher data file, no action needed.")

    def retrieve_cookie_auto(self, input_field: QLineEdit) -> None:
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
            msg_box.setWindowTitle(self.localizationTableFCLS.get("failed", "Failed"))
            msg_box.setText(self.localizationTableFCLS.get("cookie_retrieve_failed", "Failed to retrieve the cookie automatically, please get one yourself from https://www.roblox.com/."))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet(message_box_style)
            msg_box.exec()
            return
        
        input_field.setText(retrieved_cookie)

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(self.localizationTableFCLS.get("success", "Success"))
        msg_box.setText(self.localizationTableFCLS.get("cookie_retrieve_success", "Successfully retrieved cookie! You may continue now by pressing the \"Save Cookie\" button."))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(message_box_style)
        msg_box.exec()

    def prompt_for_roblox_cookie(self, initial=True) -> None:
        theme = self.get_current_theme_colors()
        dialog = QDialog(self)
        dialog.setWindowTitle(self.localizationTableFCLS.get("cookie_dialog_title", "Action Required") if initial else self.localizationTableFCLS.get("cookie_change_title", "Change Roblox Cookie"))
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

        title_label = QLabel(self.localizationTableFCLS.get("cookie_dialog_title2", "Roblox Cookie is required") if initial else self.localizationTableFCLS.get("cookie_change_title2", "Change your Roblox Cookie"))
        title_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        info_label = QLabel(
            self.localizationTableFCLS.get("cookie_info", "LegacyPlay requires your .ROBLOSECURITY cookie for Roblox APIs authentication. This will be stored locally and only used for assets downloading.")
            if initial else
            self.localizationTableFCLS.get("cookie_change_info", "You can change your .ROBLOSECURITY cookie below. This will be stored locally and only used for assets downloading.")
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)

        input_field = QLineEdit()
        input_field.setPlaceholderText(self.localizationTableFCLS.get("cookie_placeholder", "Paste your .ROBLOSECURITY cookie here..."))
        input_field.setEchoMode(QLineEdit.Password)
        input_field.setMinimumHeight(40)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        auto_button = QPushButton(self.localizationTableFCLS.get("retrieve_cookie_button", "Retrieve it"))
        auto_button.setFixedSize(100, 32)
        auto_button.clicked.connect(lambda: self.retrieve_cookie_auto(input_field))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        button_box.button(QDialogButtonBox.Ok).setText(self.localizationTableFCLS.get("save_cookie_button", "Save Cookie"))
        button_box.button(QDialogButtonBox.Ok).setFixedSize(150, 32)
        button_box.button(QDialogButtonBox.Cancel).setText(self.localizationTableFCLS.get("exit_button", "Exit"))
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
            def reject() -> None:
                pass
            dialog.reject = reject
            dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)
            dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        dialog.exec()

    def save_cookie_and_close(self, cookie, dialog) -> None:
        theme = self.get_current_theme_colors()

        if not cookie:
            print("Cookie is empty.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(self.localizationTableFCLS.get("invalid_input_label", "Invalid Input"))
            msg.setText(self.localizationTableFCLS.get("cookie_empty", "Cookie cannot be empty!"))
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
            msg.setWindowTitle(self.localizationTableFCLS.get("invalid_input_label", "Invalid Input"))
            msg.setText(self.localizationTableFCLS.get("cookie_invalid", "This is not a valid .ROBLOSECURITY cookie!"))
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

    def close_app_with_warning(self, dialog) -> Never:
        print("User rejected to paste the cookie, preparing to quit.")

        dialog.reject()
        
        theme = self.get_current_theme_colors()
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(self.localizationTableFCLS.get("cookie_dialog_title2", "Roblox Cookie is required"))
        msg.setText(self.localizationTableFCLS.get("cookie_required", "LegacyPlay requires a Roblox cookie to function properly.\n\nThe application will now exit."))
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

    def get_place_file_path(self) -> str | None:
        return self._place_file_path

    def get_client_name(self) -> str:
        return self.client_select.currentText()

    def get_ip(self) -> str:
        return self.ip_field.text()

    def get_port(self) -> str:
        return self.port_field.text()

    def addClients(self, clientsDir) -> None:
        try:
            clients = [d for d in os.listdir(clientsDir) if os.path.isdir(os.path.join(clientsDir, d))]
            self.client_select.addItems(clients)
        except Exception as e:
            print(f"Client loading error: {str(e)}")

    def on_combobox_changed(self, index) -> None:
        self.clManager.setClient(self.client_select.itemText(index))

    def prepareHost(self) -> None:
        if not self.validate_hosting():
            return
        self.webserver_manager.clear_www()
        self.webserver_manager.unzip_template_website(self.get_client_name())
        self.clManager.copy_place(self._place_file_path)
        result, message = self.clManager.host(self.get_port())
        if not result:
            self.show_error(self.localizationTableFCLS.get("failed", "Failed"), message)

    def preparePlay(self) -> None:
        if not self.validate_connection():
            return
        
        if self.clManager.isPlaying:
            QMessageBox.warning(self, self.localizationTableFCLS.get("failed", "Failed"), self.localizationTableFCLS.get("cannot_join_error", "Cannot join when you are already ingame. Please try closing and try again."))
            return
        
        nonFinalCharData = ";".join(map(str, self.body_colors))

        try:
            finalCharData = f"{nonFinalCharData};{self.shirtId};{self.pantsId};{self.hatId}"
        except:
            finalCharData = f"{nonFinalCharData};{self.shirtId};{self.pantsId}"

        print(f"Final character data: {finalCharData}")
        
        self.webserver_manager.clear_www()
        self.webserver_manager.unzip_template_website(self.get_client_name())
        result, message = self.clManager.join(
            self.get_ip(), self.get_port(),
            finalCharData
        )

        if not result:
            self.show_error(self.localizationTableFCLS.get("failed", "Failed"), message)

    def validate_hosting(self) -> bool:
        if not self._place_file_path:
            self.show_error(self.localizationTableFCLS.get("failed", "Failed"), self.localizationTableFCLS.get("missing_file_error", "Please select a place file to host."))
            return False
        if not self.get_port():
            self.show_error(self.localizationTableFCLS.get("failed", "Failed"), self.localizationTableFCLS.get("invalid_port_error", "Please specify a valid port number."))
            return False
        return True

    def validate_connection(self) -> bool:
        if not self.get_ip():
            self.show_error(self.localizationTableFCLS.get("failed", "Failed"), self.localizationTableFCLS.get("invalid_ip_error", "Please enter a valid server address."))
            return False
        if not self.get_port():
            self.show_error(self.localizationTableFCLS.get("failed", "Failed"), self.localizationTableFCLS.get("invalid_port_error", "Please specify a valid port number."))
            return False
        return True

    def show_error(self, title, message) -> None:
        QMessageBox.warning(self, title, f"{message}\n\n{self.localizationTableFCLS.get("general_recommendation", "Please check your settings and try again.")}")

    def toggle_dark_mode(self, state) -> None:
        self.dark_mode = bool(state)
        self.save_launcher_data()
        self.apply_theme()

    def apply_theme(self) -> None:
        arrow_svg = './Assets/arrow-down-dark.svg' if self.dark_mode else './Assets/arrow-down-light.svg'
        if self.dark_mode:
            self.setStyleSheet(DARK_MODE_STYLESHEET.replace("||arrow_svg||", arrow_svg))
        else:
            self.setStyleSheet(LIGHT_MODE_STYLESHEET.replace("||arrow_svg||", arrow_svg))

        print(f"Theme applied, is dark: {self.dark_mode}")