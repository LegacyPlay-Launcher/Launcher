from PySide6.QtCore import QTimer, QObject, Signal
from pypresence import Presence
import time

class RPCManager(QObject):
    update_presence_signal = Signal(str)
    RATE_LIMIT = 11

    def __init__(self, client_id) -> None:
        super().__init__()
        self.client_id = client_id
        self.rpc = Presence(client_id)
        self.connected = self._connect_rpc()
        self.last_update_time = 0
        self.queued_state = None
        self.update_timer = QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._process_queued_update)

        self.update_presence_signal.connect(self._handle_update_presence)

        print("RPCManager initialization success.")

    def _connect_rpc(self) -> bool:
        try:
            self.rpc.connect()
            print("Connected to Discord RPC!")
            return True
        except Exception as e:
            print(f"Failed to connect to Discord RPC: {e}")
            return False

    def updatePresence(self, state) -> None:
        self.update_presence_signal.emit(state)

    def _handle_update_presence(self, state) -> None:
        if not self.connected:
            self.connected = self._connect_rpc()
            if not self.connected:
                return

        current_time = time.time()
        time_since_last_update = current_time - self.last_update_time

        if time_since_last_update >= self.RATE_LIMIT:
            self._send_presence_update(state)
        else:
            self.queued_state = state
            delay = (self.RATE_LIMIT - time_since_last_update) * 1000
            if not self.update_timer.isActive():
                self.update_timer.start(delay)

    def _send_presence_update(self, state) -> None:
        try:
            self.rpc.update(
                state=state,
                large_image="iconsmall",
                large_text="LegacyPlay Logo",
            )
            self.last_update_time = time.time()
            self.queued_state = None
            print(f"Presence updated: {state}")
        except Exception as e:
            print(f"Failed to update presence: {e}")

    def _process_queued_update(self) -> None:
        if self.queued_state:
            self._send_presence_update(self.queued_state)

    def close(self):
        if self.connected:
            self.rpc.close()
            print("RPC connection closed.")
        else:
            print("No RPC connection present, cannot close. Ignoring.")