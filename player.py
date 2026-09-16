import numpy as np

class CirclePlayer():
    def __init__(self, location=(0, 0), color=(0,0,255)):
        self.size = 50
        self.location = np.array(location)
        self.color = color

        self.min_size = 20

    def get_location(self):
        return self.location

    def get_size(self):
        return self.size

    # May not be used
    def get_formatted_size(self):
        return f"{self.size:.2f}"

    def get_color(self):
        return self.color

    def update_location(self, location):
        self.location = location

    def increment_size(self):
        self.size += 0.1

    def shoot(self, direction):
        if self.size < self.min_size:
            return None
        self.size -= 5
        return CirclePellet(self, direction)

class CirclePellet():
    def __init__(self, parent: CirclePlayer, direction_vector: np.ndarray):
        self.parent = parent
        self.direction_vector = direction_vector
        self.location = self._compute_spawn_location()

        self.speed = 1

        self.size = 5

    def get_size(self):
        return self.size

    def get_color(self):
        return self.parent.get_color()

    def get_location(self):
        return self.location

    def _compute_spawn_location(self):
        radius = self.parent.get_size()
        return self.parent.get_location() + self.direction_vector * radius

    def step_location(self):
        self.location += self.direction_vector * self.speed
