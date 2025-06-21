from typing import Literal, LiteralString


import subprocess
import threading
import os
import shutil
from time import sleep
import base64

from launcherUtilities.webserverManager import WebServerManager

class ClientManager:
    def __init__(self, webserver_manager: WebServerManager = None, guiInterface = None) -> None:
        self._webserver_manager = webserver_manager
        self._rpc_manager = None
        self._guiInterface = guiInterface
        self._client = "2012L"
        self.isPlaying = False

    def _watchThread(self, clientProcess: subprocess.Popen) -> Literal[True]:  
        print("WatchThread: Client started.")
        
        if self._rpc_manager:  
            self._rpc_manager.updatePresence(f"Playing {self._client}")

        print("WatchThread: Changed the RPC.")
        
        while True:
            sleep(0.5)
            retcode = clientProcess.poll()
            if retcode is not None:
                print(f"WatchThread: Client exited with code {retcode}")
                break

        self.isPlaying = False

        currentIndex = self._guiInterface.get_current_tab_index()
        self._guiInterface.on_tab_changed(currentIndex)

        print("WatchThread: Changed the RPC.")

        print("WatchThread: Quitting.")

        return True
    
    def encode(self, text) -> str:
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        return encoded_string
    
    def setRPC(self, rpcClass) -> None:
        self._rpc_manager = rpcClass

    def setClient(self, client) -> None:
        self._client = client

    def copy_place(self, place_path) -> None:
        try:
            if os.path.exists(f"./Clients/{self._client}/content/place"):
                os.remove(f"./Clients/{self._client}/content/place")

            shutil.copy(place_path, f"./Clients/{self._client}/content/place")
        except Exception as e:
            print(f"An error occurred while copying place: {e}")

    def host(self, port) -> tuple[Literal[False], Literal['Clients directory does not exist.']] | tuple[Literal[False], Literal['The selected client\'s directory does not exist.']] | tuple[Literal[False], LiteralString] | tuple[Literal[True], None]:
        clientsDir = os.path.join('.', 'Clients')

        if not os.path.exists(clientsDir):
            return False, "Clients directory does not exist."

        ourClient = os.path.join(clientsDir, self._client)

        if not os.path.exists(ourClient):
            return False, "The selected client's directory does not exist."

        LegacyPlayerBeta = os.path.join(ourClient, 'LegacyPlayerBeta.exe')
        LegacyApp = os.path.join(ourClient, 'LegacyApp.exe') # 2012 and lower

        if not os.path.exists(LegacyPlayerBeta) and not os.path.exists(LegacyApp):
            return False, "Client .exe does not exist. Must be LegacyPlayerBeta.exe or LegacyApp.exe for older clients (2012 and lower)."
        elif os.path.exists(LegacyPlayerBeta):
            print("Detected RobloxPlayerBeta .exe")
            subprocess.Popen([
                LegacyPlayerBeta,
                "-a", "http://www.roblox.com/Login/Negotiate.ashx",
                "-t", "1",
                "-j", f"http://assetgame.roblox.com/Game/gameserver.ashx?port={port}"
            ])
        elif os.path.exists(LegacyApp):
            print("Detected RobloxApp .exe")
            subprocess.Popen([
                LegacyApp,
                "-script", f"dofile('http://assetgame.roblox.com/Game/gameserver.ashx?port={port}')"
            ])

        return True, None
    
    def join(self, ip, port, charData) -> tuple[Literal[False], Literal['Clients directory does not exist.']] | tuple[Literal[False], Literal['The selected client\'s directory does not exist.']] | tuple[Literal[False], LiteralString] | tuple[Literal[True], None]: # charData format: head_bc;left_arm_bc;torso_bc;right_arm_bc;left_leg_bc;right_leg_bc;shirt_id;pants_id;hat_ids
        clientsDir = os.path.join('.', 'Clients')

        if not os.path.exists(clientsDir):
            return False, "Clients directory does not exist."

        ourClient = os.path.join(clientsDir, self._client)

        if not os.path.exists(ourClient):
            return False, "The selected client's directory does not exist."

        LegacyPlayerBeta = os.path.join(ourClient, 'LegacyPlayerBeta.exe')
        LegacyApp = os.path.join(ourClient, 'LegacyApp.exe') # 2012 and lower

        PopenProcess = None

        CharacterDataEncoded = self.encode(charData)

        print(f"Encoded character data: {CharacterDataEncoded}")

        if not os.path.exists(LegacyPlayerBeta) and not os.path.exists(LegacyApp):
            return False, "Client .exe does not exist. Must be LegacyPlayerBeta.exe or LegacyApp.exe for older clients (2012 and lower)."
        elif os.path.exists(LegacyPlayerBeta):
            print("Detected RobloxPlayerBeta .exe")
            PopenProcess = subprocess.Popen([
                LegacyPlayerBeta,
                "-a", "http://www.roblox.com/Login/Negotiate.ashx",
                "-t", "1",
                "-j", f"http://assetgame.roblox.com/Game/join.ashx?ip={ip}&port={port}&charData={CharacterDataEncoded}"
            ])
        elif os.path.exists(LegacyApp):
            print("Detected RobloxApp .exe")
            PopenProcess = subprocess.Popen([
                LegacyApp,
                "-script", f"dofile('http://assetgame.roblox.com/Game/join.ashx?ip={ip}&port={port}&charData={CharacterDataEncoded}')"
            ])

        self.isPlaying = True

        # if self._client != "2010L":
        watchThreadInstance = threading.Thread(target=self._watchThread, args=(PopenProcess,), daemon=True)
        watchThreadInstance.start()

        return True, None
    
    def killAllClients(self) -> None:
        subprocess.Popen(["taskkill", "/F", "/IM", "LegacyPlayerBeta.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["taskkill", "/F", "/IM", "LegacyApp.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)