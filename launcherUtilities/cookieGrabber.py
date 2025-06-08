import os
import json
import re
import base64

class CookieGrabber:
    def __init__(self) -> None:
        pass

    def get_cookie_from_system(self) -> str | None:
        '''
        Taken from the RFD Project by Windows81 on GitHub.
        https://github.com/Windows81/Roblox-Freedom-Distribution/blob/main/Source/assets/extractor.py
        '''
        roblox_cookies_path = os.path.join(
            os.getenv("USERPROFILE", ""),
            "AppData",
            "Local",
            "Roblox",
            "LocalStorage",
            "RobloxCookies.dat",
        )

        if not os.path.exists(roblox_cookies_path):
            return

        with open(roblox_cookies_path, 'r', encoding='utf-8') as file:
            file_content = json.load(file)

        encoded_cookies = file_content.get("CookiesData")
        if encoded_cookies is None:
            return

        try:
            import win32crypt
        except ImportError:
            return

        decoded_cookies = base64.b64decode(encoded_cookies)
        decrypted_cookies: bytes = win32crypt.CryptUnprotectData(
            decoded_cookies, None, None, None, 0,
        )[1]

        match = re.search(br'\.ROBLOSECURITY\t([^;]+)', decrypted_cookies)
        if match == None:
            return
        return match[1].decode('utf-8', errors='ignore')