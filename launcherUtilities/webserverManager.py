import subprocess
import zipfile
import os
import shutil

class WebServerManager:
    def __init__(self):
        pass

    def start_webserver(self):
        webserverap_path = os.path.abspath(".\\WebServerApache")

        subprocess.Popen(
            [os.path.join(webserverap_path, "WebServer.exe")],
            creationflags=subprocess.CREATE_NO_WINDOW,
            cwd=webserverap_path
        )

    def stop_webserver(self):
        subprocess.Popen(
            ["taskkill", "/F", "/IM", "WebServer.exe"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        subprocess.Popen(
            ["taskkill", "/F", "/IM", "httpd.exe"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    def clear_www(self):
        try:
            if os.path.exists("./WebServerApache/Apache24/htdocs"):
                shutil.rmtree("./WebServerApache/Apache24/htdocs/")

            os.mkdir("./WebServerApache/Apache24/htdocs/")
        except Exception as e:
            print(f"An error occurred while clearing htdocs directory: {e}")

    def unzip_template_website(self, template_name):
        try:
            with zipfile.ZipFile(f"./WebsiteTemplates/{template_name}.zip", "r") as zip_ref:
                zip_ref.extractall("./WebServerApache/Apache24/htdocs/")
        except Exception as e:
            print(f"An error occurred while unzipping template: {e}")