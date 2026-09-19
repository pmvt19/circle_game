import pygame
import time
from player import CirclePellet, CirclePlayer
from ai_player import AiCirclePlayer, AiCirclePlayerEngine
import numpy as np

pygame.init()

class Engine:
    def __init__(self):
        self.user: CirclePlayer = CirclePlayer()
        self.players: list[AiCirclePlayer] = [AiCirclePlayer(AiCirclePlayerEngine())]
        self.resolution = (1400, 1000)
        self.screen = pygame.display.set_mode(self.resolution)

        self.scaling_factor = 2.0

        self.pellets: list[CirclePellet] = []

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
            radius=player.get_size()

            pygame.draw.circle(surface, color, center, radius, width=0)

            text_surface = font.render(str(player.get_formatted_size()), True, (0, 0, 0))
    
            text_rect = text_surface.get_rect()
            text_rect.center = player.get_location()

            surface.blit(text_surface, text_rect)

    def draw_circle_pellets(self, surface):
        for pellet in self.pellets:
            color=pellet.get_color()
            center=pellet.get_location()
            radius=pellet.get_size()

            pygame.draw.circle(surface, color, center, radius, width=0)

    def draw_game_frame(self, surface):
        self.draw_circles(surface)
        self.draw_circle_pellets(surface)

        self.screen.fill((255, 255, 255)) # Optional: Make the window background white
        self.screen.blit(surface, (0,0))

    def get_direction_vector(self, cursor_position):
        cursor_position = np.array(cursor_position)
        user_location = self.user.get_location()

        direction_vector = cursor_position - user_location
        return direction_vector

    def step_pellet_locations(self):
        for pellet in self.pellets:
            pellet.step_location()


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
        for player in self.players:
            cursor_position = np.array(player.get_mouse_position())
            player_location = player.get_location()

            direction_vector = cursor_position - player_location
            direction_magnitude = np.linalg.norm(direction_vector)

            if direction_magnitude > 0:
                normalized_direction_vector = direction_vector / direction_magnitude

                updated_location = player.get_location() + normalized_direction_vector * self.scaling_factor

                player.update_location(updated_location)
            else:
                print("Failed to update user location")

    def update_circle_sizes(self):
        self.user.increment_size()
        for player in self.players:
            player.increment_size()

    def handle_user_shoot(self, cursor_position):
        direction_vector = self.get_direction_vector(cursor_position)
        direction_magnitude = np.linalg.norm(direction_vector)

        normalized_direction_vector = direction_vector / direction_magnitude
        pellet = self.user.shoot(normalized_direction_vector)
        if pellet:
            self.pellets.append(pellet)

    def handle_non_user_circle_shoot(self):
        pass

    def run_game(self):
        running = True
        while running:
            surface = pygame.Surface(self.resolution)
            surface.fill((255, 255, 255))
            self.draw_game_frame(surface)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.handle_user_shoot(pygame.mouse.get_pos())

                    # Stop Game If User Presses "q"
                    if event.key == pygame.K_q:
                        running = False

            self.update_user_circle_pos(pygame.mouse.get_pos())
            self.update_non_user_circle_pos() 

            self.handle_non_user_circle_shoot()
            self.update_circle_sizes()

            self.step_pellet_locations()

            print(f"Number of Pellets in Game: {len(self.pellets)}", end="\r")

engine = Engine()
engine.run_game()
