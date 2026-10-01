import time

import pygame

from game_engine import Engine
from player import CirclePlayer, ReadOnlyCirclePlayer

class MultiplayerEngine(Engine):
    def __init__(self):
        super().__init__()

    def add_player(self, player: CirclePlayer):
        self.players.append(player)

    def publish_game_info(self):
        # Publish Game Info to all Connected Clients
        pass

    def read_client_inputs(self):
        # Reads inputs from the client and updates the game accordingly
        pass

    def run_game(self):
        running = True
        while running:
            start_time = time.time()

            running = self.step_game_frame()

            self.publish_game_info()

            end_time = time.time()

            print(f"FPS: {1 / (end_time - start_time)}", end="\r")

class ClientMultiplayerEngine(Engine):
    def __init__(self):
        self.players: list[ReadOnlyCirclePlayer] = []

    def update_player_info(self):
        # Should Read the Data Published from the Server and Update the Circle States
        pass

    def run_game(self):
        running = True
        while running:
            start_time = time.time()
            surface = pygame.Surface(self.resolution)
            surface.fill((255, 255, 255))
            self.draw_game_frame(surface)

            pygame.display.flip()

            end_time = time.time()
            print(f"FPS: {1 / (end_time - start_time)}", end="\r")

            self.update_player_info()

        # TODO: Fix the game over screen
        surface = pygame.Surface(self.resolution)
        surface.fill((255, 255, 255))
        self.draw_gameover_screen(surface)
        self.screen.blit(surface, (0,0))
        pygame.display.flip()
        time.sleep(100)