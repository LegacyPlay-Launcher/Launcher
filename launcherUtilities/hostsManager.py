class HostsManager:
    def __init__(self) -> None:
        self.hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'
        self.entries = {
            "127.0.0.1 roblox.com\n",
            "127.0.0.1 www.roblox.com\n",
            "127.0.0.1 api.roblox.com\n",
            "127.0.0.1 clientsettings.api.roblox.com\n",
            "127.0.0.1 assetgame.roblox.com\n",
            "127.0.0.1 wiki.roblox.com\n"
        }

        print("HostsManager initialization success.")

    def addHosts(self) -> None:
        with open(self.hosts_file_path, 'r') as hosts_file:
            existing_lines = set(hosts_file.readlines())
        with open(self.hosts_file_path, 'a') as hosts_file:
            for entry in self.entries - existing_lines:
                hosts_file.write(entry)

        print(f"Written lines to {self.hosts_file_path}")

    def removeHosts(self) -> None:
        with open(self.hosts_file_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        with open(self.hosts_file_path, 'w') as hosts_file:
            hosts_file.writelines(line for line in lines if line not in self.entries)

        print(f"Removed lines from {self.hosts_file_path}")