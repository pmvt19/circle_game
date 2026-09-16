import numpy as np

class CirclePlayer():
    def __init__(self, location=(0, 0), color=(0,0,255)):
        self.size = 50
        self.location = np.array(location)
        self.color = color

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
        self.size -= 5
        return CirclePellet(self)

class CirclePellet():
    def __init__(self, parent: CirclePlayer):
        self.parent = parent
