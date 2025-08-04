"""

LEGACYPLAY LAUNCHER

Copyright (c) 2025, LegacyPlay Development Team
All rights reserved.

All programs provided in this launcher belong to their owners.

This launcher is provided "as is" and comes with no warranty.

"""

# TestValues().test(window) - tests every value inputs (OUTDATED)
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
# from launcherUtilities.tests import TestValues (OUTDATED)

print("\n----------------------------------------------------------------------------\n")

print("LEGACYPLAY LAUNCHER\n")

print("Copyright (c) 2025, LegacyPlay Development Team")
print("All rights reserved.\n")

print("This launcher is provided \"as is\" and comes with no warranty.\n")

print("----------------------------------------------------------------------------\n")

SSL_PATH = "./Certificate/roblox.crt"
CLIENT_ID = '1348257279983616141'

currentVer = "0_861B"

open('./launcher.log', 'w').close()
log_file = open('./launcher.log', 'a')

if __name__ == "__main__":
    print("Logging init...")

    sys.stdout = Tee(sys.__stdout__, log_file)

    print("QApplication init...")

    app = QApplication([])

    print("Running admin check...")

    admin_check = AdminCheck()
    is_admin = admin_check.is_admin()

    if not is_admin:
        print("Did not pass admin rights check, halting...")
        sys.exit(1)

    print("Passed admin rights check - nice.")

    print("Checking for updates...")

    updManager = UpdatesManager(currentVer)
    updManager.checkUpdates()

    print("Classes init...")

    webserver_manager = WebServerManager()
    client_manager = ClientManager(webserver_manager)
    ssl_manager = SSLManager()
    cookie_grabber = CookieGrabber()

    print("Instancing GUI and calling neccesary functions...")

    window = GUIInterface(webserver_manager, cookie_grabber)
    window.addClients("./Clients/")

    print("Running checks (except admin check)...")

    redist_manager = RedistManager()

    if not redist_manager.check_redist_installed():
        redist_manager.exec()
    else:
        print("VC++ Redist x64 is already installed.")

    print(r"Editing hosts file at C:\Windows\System32\drivers\etc\hosts")

    hosts_manager = HostsManager()
    hosts_manager.addHosts()

    print("Attempting to start webserver...")

    try:
        webserver_manager.start_webserver()
        print("Webserver started with no errors!")
    except:
        print("Fallback: removing hosts...")
        hosts_manager.removeHosts()
        print("Fallback: Failed to start webserver, halting...")
        sys.exit(1)

    print("Checking for SSL installation (needed for self-signed certs)...")

    if not ssl_manager.checkForSSLInstalled(SSL_PATH):
        print("Installing SSL...")
        ssl_manager.installSSL(SSL_PATH)
    else:
        print("SSL is already installed.")

    print("Initializing RPC Manager class (manages Discord RPC)...")

    rpc = RPCManager(CLIENT_ID)
    
    window.setRPC(rpc)
    window.on_tab_changed(0)

    print("Success.")

    print("Init tasks fully finished, ready to start the LegacyPlay core...")

    window.show()
    app.exec()

    print("Received shutdown callback.")

    print("Shutting down webserver...")
    webserver_manager.stop_webserver()

    print("Closing RPC connection...")
    rpc.close()

    print("Cleaning up...")
    client_manager.killAllClients()
    hosts_manager.removeHosts()
    webserver_manager.clear_www()

    print("Done.")