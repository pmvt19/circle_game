# HOlds information about all the circles, but not references to them

# For example, know where every circle is and their size and their id

# Then each AI will read from the broadcaster to get info about the other circles

class PlayerInfo:
    player_id: int
    location: tuple[float, float]
    is_human: bool

    def __repr__(self):
        return f"Player Id: {self.player_id}, Location: {self.location}, Is Human: {self.is_human}"

class Broadcaster:
    def __init__(self):
        self.info: dict[int, PlayerInfo] = {}

    def publish_info(self, player_info: PlayerInfo):
        self.info[player_info.player_id] = player_info

    def get_game_info(self):
        return self.info