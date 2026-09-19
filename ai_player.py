import time

from player import CirclePlayer
from random import randint


class AiCirclePlayerEngine:
    def __init__(self):
        self.last_updated_time = 0

        self.update_threshold = 0.5

        self.current_mouse_location = None

    def get_mouse_position(self):
        if time.time() - self.last_updated_time > self.update_threshold:
            x = randint(0, 1400)
            y = randint(0, 500)
            self.current_mouse_location = (x, y)

            # Update Last Updated Time to Current Time
            self.last_updated_time = time.time()
            return self.current_mouse_location

        assert (self.current_mouse_location is not None)
        return self.current_mouse_location

    def should_shoot(self):
        pass


class AiCirclePlayer(CirclePlayer):
    def __init__(self, ai_engine: AiCirclePlayerEngine, location=(0,0), color=(255,0,0)):
        self.ai_engine = ai_engine
        super().__init__(location=location, color=color)

    def get_mouse_position(self):
        return self.ai_engine.get_mouse_position()