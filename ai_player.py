import time
import numpy as np
from player import CirclePlayer, CirclePellet
from random import randint, random

from broadcaster import Broadcaster


class AiCirclePlayerEngine:
    def __init__(self, broadcaster: Broadcaster):
        self.last_updated_time = 0

        self.update_threshold = 0.5

        self.current_mouse_location = None

        self.broadcaster = broadcaster

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

class SmartAiCirclePlayerEngine:
    def __init__(self, broadcaster: Broadcaster):
        self.last_updated_time = 0

        self.update_threshold = 0.5

        self.current_mouse_location = None

        self.broadcaster = broadcaster

        self.follow_user_probability = 0.2

    def get_mouse_position(self):
        # HACK: Hardcoded right now for testing

        if random() < self.follow_user_probability and 0 in self.broadcaster.info:
            potential_mouse_location = self.broadcaster.info[0].location
        else:
            x = randint(0, 1400)
            y = randint(0, 500)
            potential_mouse_location = (x, y)

        if time.time() - self.last_updated_time > self.update_threshold:
            self.current_mouse_location = potential_mouse_location

            # Update Last Updated Time to Current Time
            self.last_updated_time = time.time()
            return self.current_mouse_location

        assert (self.current_mouse_location is not None)
        return self.current_mouse_location

    def get_mouse_position_for_shooting(self):
        if 0 in self.broadcaster.info:
            potential_mouse_location = self.broadcaster.info[0].location
        else:
            x = randint(0, 1400)
            y = randint(0, 500)
            potential_mouse_location = (x, y)

        return potential_mouse_location

    def should_shoot(self):
        if 0 in self.broadcaster.info:
            user_location = np.array(self.broadcaster.info[0].location)
            player_location = np.array(self.broadcaster.info[1].location)

            dist = np.linalg.norm(player_location - user_location)

            if dist < 300:
                return True

        return False


class AiCirclePlayer(CirclePlayer):
    def __init__(self, ai_engine: AiCirclePlayerEngine, location=(0,0), color=(255,0,0)):
        self.ai_engine = ai_engine
        super().__init__(location=location, color=color)

    def get_mouse_position(self):
        return self.ai_engine.get_mouse_position()


    def shoot(self, direction=None):
        if self.ai_engine.should_shoot():
            if self.size < self.min_size:
                return None
            self.size -= 5
            direction = np.array(self.ai_engine.get_mouse_position_for_shooting()) - self.location
            direction_magnitude = np.linalg.norm(direction)
            direction = direction / direction_magnitude

            return CirclePellet(self, direction)
        return None