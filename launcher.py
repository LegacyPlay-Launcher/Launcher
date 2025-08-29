"""

LEGACYPLAY LAUNCHER APPLICATION

Copyright (c) 2025, LegacyPlay Development Team
All rights reserved.

All programs provided in this launcher belong to their owners. We DO NOT own the client binaries, all credits go to the Roblox Corporation.

"""
# webserver_manager.unzip_template_website("2012L") - unzips a template (2012L can be replaced with any template name)

from PySide6.QtWidgets import QApplication
import sys

from launcherUtilities.guiInterface import GUIInterface
from launcherUtilities.redistManager import RedistManager
from launcherUtilities.webserverManager import WebServerManager
from launcherUtilities.adminCheck import AdminCheck
from launcherUtilities.hostsManager import HostsManager
from launcherUtilities.sslManager import SSLManager
from launcherUtilities.rpcManager import RPCManager
from launcherUtilities.logger import Tee
from launcherUtilities.updatesManager import UpdatesManager
from launcherUtilities.cookieGrabber import CookieGrabber
from clientUtilities.clientManager import ClientManager

print("\n----------------------------------------------------------------------------\n")

print("LEGACYPLAY LAUNCHER APPLICATION\n")

print("Copyright (c) 2025, LegacyPlay Development Team")
print("All rights reserved.\n")

print("----------------------------------------------------------------------------\n")

SSL_PATH = "./Certificate/roblox.crt"
CLIENT_ID = '1348257279983616141'

currentVer = "0_900B"

open('./launcher.log', 'w').close()
log_file = open('./launcher.log', 'a')

if __name__ == "__main__":
    print("Logging is initializing...")

    sys.stdout = Tee(sys.__stdout__, log_file)

    print("QApplication is initializing...")

    app = QApplication([])

    print("Is admin? ", end='')

    admin_check = AdminCheck()
    is_admin = admin_check.is_admin()

    if not is_admin:
        print("No")
        sys.exit(1)

    print("Yes")

    print("Checking for any updates...")

    updManager = UpdatesManager(currentVer)
    updManager.checkUpdates()

    print("Classes are initializing...")

    webserver_manager = WebServerManager()
    client_manager = ClientManager(webserver_manager)
    ssl_manager = SSLManager()
    cookie_grabber = CookieGrabber()

    print("Instancing the GUI and calling neccesary functions...")

    window = GUIInterface(webserver_manager, cookie_grabber)
    window.addClients("./Clients/")

    print("Running checks (except the admin check)...")

    redist_manager = RedistManager()

    if not redist_manager.check_redist_installed():
        redist_manager.exec()
    else:
        print("VC++ Redist x64 is already installed, skip.")

    print(r"Editing hosts file at C:\Windows\System32\drivers\etc\hosts")

    hosts_manager = HostsManager()
    hosts_manager.addHosts()

    print("Attempting to start webserver...")

    try:
        webserver_manager.start_webserver()
        print("Webserver started with no errors!")
    except Exception as e:
        print("Error! Shutting down LegacyPlay, removing hosts...")
        print(f"The error message provided by Python: {e}")
        hosts_manager.removeHosts()
        print("Halting...")
        sys.exit(1)

    print("Checking for the SSL certificate installation...")

    if not ssl_manager.checkForSSLInstalled(SSL_PATH):
        print("Installing the SSL certificate...")
        ssl_manager.installSSL(SSL_PATH)
    else:
        print("The SSL certificate is already installed, skip.")

    print("Initializing RPC Manager class (manages Discord RPC)...")

    rpc = RPCManager(CLIENT_ID)
    
    window.setRPC(rpc)
    window.on_tab_changed(0)

    print(f"Successful! Client ID: {CLIENT_ID}")

    print("Initializing tasks have been completed, ready to show the LegacyPlay GUI...")

    window.show()
    app.exec()

    print("Received a GUI shutdown, stopping services.")

    print("Shutting down the webserver...")
    webserver_manager.stop_webserver()

    print("Closing the RPC connection...")
    rpc.close()

    print("Cleaning up...")
    client_manager.killAllClients()
    hosts_manager.removeHosts()
    webserver_manager.clear_www()

    print("Finished.")