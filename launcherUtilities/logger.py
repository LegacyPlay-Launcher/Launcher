class Tee:
    def __init__(self, *streams):
        self.streams = [s for s in streams if s is not None]

    def write(self, message):
        for s in self.streams:
            s.write(message)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()