import pygame
import time
from player import CirclePellet, CirclePlayer
import numpy as np

pygame.init()

class Engine:
    def __init__(self):
        self.user: CirclePlayer = CirclePlayer()
        self.players: list[CirclePlayer] = []
        self.resolution = (1400, 1400)
        self.screen = pygame.display.set_mode(self.resolution)

        self.scaling_factor = 3.0

    def draw_circles(self, surface):
        pygame.draw.circle(surface, self.user.get_color(), self.user.get_location(), self.user.get_size(), width=0)
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(self.user.get_formatted_size()), True, (0, 0, 0))

        text_rect = text_surface.get_rect()
        text_rect.center = self.user.get_location()

        surface.blit(text_surface, text_rect)

        for player in self.players:
            color=player.get_color()
            center=player.get_location()
            radius=10

            pygame.draw.circle(surface, color, center, radius, width=0)

    def draw_game_frame(self, surface):
        self.draw_circles(surface)

        self.screen.fill((255, 255, 255)) # Optional: Make the window background white
        self.screen.blit(surface, (0,0))

    def update_user_circle_pos(self, cursor_position):
        cursor_position = np.array(cursor_position)
        user_location = self.user.get_location()

        direction_vector = cursor_position - user_location
        direction_magnitude = np.linalg.norm(direction_vector)

        if direction_magnitude > 0:
            normalized_direction_vector = direction_vector / direction_magnitude

            updated_location = self.user.get_location() + normalized_direction_vector * self.scaling_factor

            self.user.update_location(updated_location)
        else:
            print("Failed to update user location")

    def update_non_user_circle_pos(self):
        pass

    def update_circle_sizes(self):
        self.user.increment_size()

    def run_game(self):
        while True:
            surface = pygame.Surface(self.resolution)
            surface.fill((255, 255, 255))
            self.draw_game_frame(surface)

            pygame.display.flip()
            pygame.event.get()

            self.update_user_circle_pos(pygame.mouse.get_pos())
            self.update_circle_sizes()

engine = Engine()
engine.run_game()
