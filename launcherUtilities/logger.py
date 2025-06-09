class Tee:
    def __init__(self, *streams) -> None:
        self.streams = [s for s in streams if s is not None]

    def write(self, message) -> None:
        for s in self.streams:
            s.write(message)
            s.flush()

    def flush(self) -> None:
        for s in self.streams:
            s.flush()