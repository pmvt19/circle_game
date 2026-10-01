from game_engine import Engine


class MultiplayerEngine(Engine):
    def __init__(self):
        super().__init__()

        self.user = None