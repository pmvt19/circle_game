import pygame
import time
from player import CirclePellet, CirclePlayer
from ai_player import AiCirclePlayer, AiCirclePlayerEngine, SmartAiCirclePlayerEngine
import numpy as np

from broadcaster import Broadcaster, PlayerInfo

pygame.init()


class Engine:
    def __init__(self):
        self.broadcaster: Broadcaster = Broadcaster()

        self.players: list[CirclePlayer] = [CirclePlayer(), AiCirclePlayer(SmartAiCirclePlayerEngine(self.broadcaster))]
        self.resolution = (1400, 1000)
        self.screen = pygame.display.set_mode(self.resolution)

        self.scaling_factor = 2.0

        self.pellets: list[CirclePellet] = []

    def draw_circles(self, surface):
        font = pygame.font.Font(None, 50)

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

    def step_pellet_locations(self):
        for pellet in self.pellets:
            pellet.step_location()

    def update_circle_positions(self):
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
        for player in self.players:
            player.increment_size()

    def handle_circle_shoot(self):
        for player in self.players:
            pellet = player.shoot(player.get_mouse_position())
            if pellet:
                self.pellets.append(pellet)

    def broadcast_info(self):
        for player_id, player in enumerate(self.players):
            player_info = PlayerInfo()
            player_info.location = player.get_location()
            player_info.is_human = False if player_id > 0 else True # TODO: Make this Robust by looking at class instance
            player_info.player_id = player_id # TODO: Fix this CirclePlayer should also know Id

            self.broadcaster.publish_info(player_info)

    def _should_delete_pellet(self, pellet: CirclePellet):
        x, y = pellet.get_location()

        if x >= 0 and x < self.resolution[0] and y >= 0 and y < self.resolution[1]:
            return False

        return True

    def _should_delete_player(self, player: CirclePlayer):
        return player.get_size() <= 0

    def despawn_pellets(self):
        idx = len(self.pellets) - 1 

        while idx >= 0:
            pellet = self.pellets[idx]

            if self._should_delete_pellet(pellet):
                self.pellets.pop(idx)

            idx -= 1

    def pellet_players_collision_check(self):
        pellet_locations = []
        for pellet in self.pellets:
            x, y = pellet.get_location()
            pellet_locations.append((x, y, pellet.get_size()))

        player_locations = []
        for player in self.players:
            x, y = player.get_location()
            player_locations.append((x, y, player.get_size()))

        if not pellet_locations or not player_locations:
            return

        pellet_locations = np.array(pellet_locations).reshape(-1, 3)
        player_locations = np.array(player_locations).reshape(-1, 3)

        distance_mat = np.sqrt(np.sum(player_locations[:, :2]**2, axis=1, keepdims=True) + np.sum(pellet_locations[:, :2]**2, axis=1, keepdims=True).T + (-2 * (player_locations[:, :2] @ pellet_locations[:, :2].T)))

        player_radii = player_locations[:, 2:]
        pellet_radii = pellet_locations[:, 2:]

        thresholds = player_radii.reshape(-1, 1) + pellet_radii.reshape(1, -1)

        collision_mat = distance_mat < thresholds

        penalty_per_player = np.sum(collision_mat, axis=1)

        for i, player in enumerate(self.players):
            player.got_shot(penalty_per_player[i])

        pellets_to_remove = np.sum(collision_mat, axis=0) > 0

        # Remove Pellets which hit a player
        for i in reversed(range(len(pellets_to_remove))):
            if pellets_to_remove[i]:
                self.pellets.pop(i)

    def despawn_players(self):
        idx = len(self.players) - 1 
        
        while idx >= 1:
            player = self.players[idx]

            if self._should_delete_player(player):
                self.players.pop(idx)

            idx -= 1

        if self._should_delete_player(self.players[0]):
            return True
        
        return False

    def draw_gameover_screen(self, surface):
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Game Over", True, (0, 0, 0))

        text_rect = text_surface.get_rect()
        text_rect.center = (self.resolution[0]/2, self.resolution[1]/2)

        surface.blit(text_surface, text_rect)

    def step_game_frame(self):
        self.update_circle_positions() 
        
        self.handle_circle_shoot()
        self.update_circle_sizes()

        self.step_pellet_locations()

        self.broadcast_info()
        self.despawn_pellets()

        self.pellet_players_collision_check()

        if self.despawn_players():
            return False
        return True
        
    def run_game(self):
        running = True
        while running:
            start_time = time.time()
            surface = pygame.Surface(self.resolution)
            surface.fill((255, 255, 255))
            self.draw_game_frame(surface)

            pygame.display.flip()
        
            running = self.step_game_frame()

            # Handle User Manually Quitting
            if pygame.key.get_pressed()[pygame.K_q]:
                running = False

            end_time = time.time()

            print(f"FPS: {1 / (end_time - start_time)}", end="\r")

        # TODO: Fix the game over screen
        surface = pygame.Surface(self.resolution)
        surface.fill((255, 255, 255))
        self.draw_gameover_screen(surface)
        self.screen.blit(surface, (0,0))
        pygame.display.flip()
        time.sleep(100)


engine = Engine()
engine.run_game()
