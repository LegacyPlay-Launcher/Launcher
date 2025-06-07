# OUTDATED CODE

# DO NOT USE IN PRODUCTION!

class TestValues:
    def __init__(self):
        pass

    def test(self, app):
        print(f"Current client: {app.get_client_name()}")
        print(f"Current username: {app.get_username()}")
        print(f"Current user ID: {app.get_user_id()}")
        print(f"Current IP: {app.get_ip()}")
        print(f"Current port: {app.get_port()}")