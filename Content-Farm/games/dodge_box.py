# games/dodge_box.py

import pygame
import random
from game_framework import Game
from games import consts
from recording import config

PLAYER_SIZE = 20
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 60
OBSTACLE_SPEED = 8
SPAWN_INTERVAL = 1000  # milliseconds

class Player:
    def __init__(self):
        self.x = config.WIDTH // 2
        self.y = config.HEIGHT - PLAYER_SIZE - 10
        self.speed = 10
        self.color = consts.GREEN
        self.direction = random.choice(["left", "right"])

    def move(self):
        # Randomly switch direction
        if random.random() < 0.02:
            self.direction = "left" if self.direction == "right" else "right"

        if self.direction == "left" and self.x - self.speed > 0:
            self.x -= self.speed
        elif self.direction == "right" and self.x + self.speed + PLAYER_SIZE < config.WIDTH:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)

class Obstacle:
    def __init__(self):
        self.x = random.randint(0, config.WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT

    def update(self):
        self.y += OBSTACLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, consts.RED, (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

class DodgeBox(Game):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.player = Player()
        self.obstacles = []
        self.last_spawn_time = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        self.screen.fill("black")

        # Autonomous player movement
        self.player.move()

        # Spawn obstacles
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= SPAWN_INTERVAL:
            self.obstacles.append(Obstacle())
            self.last_spawn_time = current_time

        # Update and draw obstacles
        for obs in self.obstacles:
            obs.update()
            obs.draw(self.screen)
            if obs.get_rect().colliderect(self.player.get_rect()):
                self.done = True

        self.player.draw(self.screen)

    def draw(self):
        pass  # Already drawn during update()

    def run_frame(self):
        self.handle_events(pygame.event.get())
        self.update()
        pygame.display.flip()

    def is_done(self):
        return self.done
