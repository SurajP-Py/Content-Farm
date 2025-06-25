# games/lava_drop.py

import pygame
import random
from game_framework import Game
from games import consts
from recording import config

PLATFORM_WIDTH = config.WIDTH // 3

class Ball:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.g = 2
        self.vy = 0
        self.vx = random.choice([-8, -7, -6, -5, 5, 6, 7, 8])

    def update(self, platforms):
        self.y += self.vy
        self.x += self.vx

        if self.vy < 25:
            self.vy += self.g

        if self.x + self.r >= config.WIDTH or self.x - self.r <= 0:
            self.x -= self.vx
            self.vx *= -1

        for platform in platforms:
            if not platform.is_alive():
                continue
            rect = platform.get_rect()
            ball_rect = pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
            if ball_rect.colliderect(rect) and self.vy > 0:
                self.vy *= -0.75
                platform.hit()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def is_done(self):
        return self.y >= config.HEIGHT * 9 / 10

class Platform:
    def __init__(self, x, y, w, l, hits=1):
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.hits_remaining = hits
        self.alive = True

    def hit(self):
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            self.alive = False

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, consts.GREY, (self.x, self.y, self.w, self.l))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.l)

    def is_alive(self):
        return self.alive

class LavaDrop(Game):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.red = Ball(config.WIDTH / 5, config.HEIGHT // 10, 20, consts.RED)
        self.yellow = Ball(config.WIDTH * 2 / 5, config.HEIGHT // 10, 20, consts.YELLOW)
        self.blue = Ball(config.WIDTH * 3 / 5, config.HEIGHT // 10, 20, consts.BLUE)
        self.purple = Ball(config.WIDTH * 4 / 5, config.HEIGHT // 10, 20, consts.PURPLE)

        self.platforms = []
        rows = 6
        cols = 8
        block_width = config.WIDTH // cols
        block_height = 20
        vertical_spacing = config.HEIGHT // 8

        for row in range(rows):
            y = (row + 1) * vertical_spacing
            for col in range(cols):
                x = col * block_width
                self.platforms.append(Platform(x, y, block_width, block_height))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        self.screen.fill("black")

        self.red.update(self.platforms)
        self.yellow.update(self.platforms)
        self.blue.update(self.platforms)
        self.purple.update(self.platforms)

    def draw(self):
        for platform in self.platforms:
            platform.draw(self.screen)

        pygame.draw.rect(self.screen, consts.ORANGE, (0, config.HEIGHT * 9 / 10, config.WIDTH, config.HEIGHT // 10))

        self.red.draw(self.screen)
        self.yellow.draw(self.screen)
        self.blue.draw(self.screen)
        self.purple.draw(self.screen)

    def run_frame(self):
        self.handle_events(pygame.event.get())
        self.update()
        self.draw()
        pygame.display.flip()

    def is_done(self):
        if self.red.is_done() and self.yellow.is_done() and self.blue.is_done() and self.purple.is_done():
            self.done = True
        return self.done