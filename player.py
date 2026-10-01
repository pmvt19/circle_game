import numpy as np
import time
import pygame

class CirclePlayer():
    def __init__(self, location=(0, 0), color=(0,0,255)):
        self.size = 50
        self.location = np.array(location)
        self.color = color

        self.min_size = 20

        self.shot_cooldown = 0.5
        self.time_since_last_shot = time.time()

    def get_location(self):
        return self.location

    def get_size(self):
        return self.size

    # May not be used
    def get_formatted_size(self):
        # return f"{self.size:.2f}"
        return f"{int(self.size)}"

    def get_color(self):
        return self.color

    def update_location(self, location):
        self.location = location

    def increment_size(self):
        self.size += 0.01

    def got_shot(self, magnitude):
        self.size -= 10 * magnitude

    def get_direction_vector(self, cursor_position):
        # TODO: Ensure no divide by Zero
        direction = cursor_position - self.location
        direction_magnitude = np.linalg.norm(direction)
        direction = direction / direction_magnitude
        return direction

    def can_shoot(self):
        return time.time() - self.time_since_last_shot > self.shot_cooldown and self.size >= self.min_size

    def should_shoot(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_SPACE]

    def get_mouse_position(self):
        pygame.event.get() # Update Mouse Positions
        return np.array(pygame.mouse.get_pos())

    def shoot(self, direction=None):
        # TODO: Clean this logic up
        if direction is None:
            print("Not shooting no direction")
            return None
        if not self.can_shoot():
            return None

        if not self.should_shoot():
            return None
        self.size -= 5
        self.time_since_last_shot = time.time()
        direction = self.get_direction_vector(direction)
        return CirclePellet(self, direction)

class CirclePellet():
    def __init__(self, parent: CirclePlayer, direction_vector: np.ndarray):
        self.parent = parent
        self.direction_vector = direction_vector

        self.size = 5
        self.speed = 4

        self.location = self._compute_spawn_location()

    def get_size(self):
        return self.size

    def get_color(self):
        return self.parent.get_color()

    def get_location(self):
        return self.location

    def _compute_spawn_location(self):
        radius = self.parent.get_size()
        return self.parent.get_location() + self.direction_vector * (radius + self.size)

    def step_location(self):
        self.location += self.direction_vector * self.speed

# TBD

class ReadOnlyCirclePlayer(CirclePlayer):
    def __init__(self, size: int, location: tuple[int, int], color: tuple[int, int, int]):
        self.size = size
        self.location = np.array(location)
        self.color = color

    def get_location(self):
        return self.location

    def get_size(self):
        return self.size

    def get_formatted_size(self):
        return f"{int(self.size)}"

    def get_color(self):
        return self.color

    def get_mouse_position(self):
        raise NotImplementedError

    def update_state(self):
        pass
    
    def update_location(self, location):
        raise NotImplementedError

    def increment_size(self):
        raise NotImplementedError

    def got_shot(self, magnitude):
        raise NotImplementedError

    def get_direction_vector(self, cursor_position):
        return NotImplementedError

    def can_shoot(self):
        return NotImplementedError

    def should_shoot(self):
        return NotImplementedError

    def shoot(self, direction=None):
        return NotImplementedError


class WriteCirclePlayer(CirclePlayer):
    def __init__(self, size: int, location: tuple[int, int], color: tuple[int, int, int]):
        self.size = size
        self.location = np.array(location)
        self.color = color

    def get_location(self):
        return self.location

    def get_size(self):
        return self.size

    def get_formatted_size(self):
        return f"{int(self.size)}"

    def get_color(self):
        return self.color

    def get_mouse_position(self):
        raise NotImplementedError
    
    def update_location(self, location):
        raise NotImplementedError

    def increment_size(self):
        raise NotImplementedError

    def got_shot(self, magnitude):
        raise NotImplementedError

    def get_direction_vector(self, cursor_position):
        return NotImplementedError

    def can_shoot(self):
        return NotImplementedError

    def should_shoot(self):
        return NotImplementedError

    def shoot(self, direction=None):
        return NotImplementedError



    
    
# Ideas for AI:

# Shoot in the direction of the user circle
# Shoot in a random direction


# Ideas for Items: 
# Costless Shooting (Shooting pellets doesn't cost size)
# Instant growth (Though you would have to be careful as to not collide with your own pellets)
# Speed Boost (Again would require special tuning to not collide with your own pellets)

# Negative Items? - Items you actively want to avoid