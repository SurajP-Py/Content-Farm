# games/4_ball_drop.py

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

        for i in platforms:
            if (self.x - self.r <= i.get_x() + PLATFORM_WIDTH and self.x + self.r >= i.get_x()) and ((self.y + self.r >= i.get_y() and self.y + self.r <= i.get_y() + 30) or (self.y + self.vy + self.r >= i.get_y() and self.y + self.vy + self.r <= i.get_y() + 30)) and self.vy > 0:
                self.vy *= -0.75

        if self.y >= config.HEIGHT * 9 / 10:
            self.g = 0
            self.vy = 0
            self.vx = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def is_done(self):
        return self.y >= config.HEIGHT * 9 / 10

class Platform:
    def __init__(self, x, y, w, l):
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.v = random.choice([random.randint(5,15) * -1, random.randint(5,15)])

    def update(self):
        self.x += self.v

        if self.x < 0 or self.x + self.w > config.WIDTH:
            self.v *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, consts.GREY, (self.x, self.y, self.w, self.l))

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

class FourBallDrop(Game):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.platforms = [Platform(random.randint(0, config.WIDTH - PLATFORM_WIDTH), config.HEIGHT // 6 * (i + 1), PLATFORM_WIDTH, 20) for i in range(5)]
        self.red = Ball(config.WIDTH / 5, config.HEIGHT // 10, 20, consts.RED)
        self.yellow = Ball(config.WIDTH * 2 / 5, config.HEIGHT // 10, 20, consts.YELLOW)
        self.blue = Ball(config.WIDTH * 3 / 5, config.HEIGHT // 10, 20, consts.BLUE)
        self.purple = Ball(config.WIDTH * 4 / 5, config.HEIGHT // 10, 20, consts.PURPLE)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
    
    def update(self):
        self.screen.fill("black")
        for i in self.platforms:
            i.update()

        self.red.update(self.platforms)
        self.yellow.update(self.platforms)
        self.blue.update(self.platforms)
        self.purple.update(self.platforms)
    
    def draw(self):
        for i in self.platforms:
            i.draw(self.screen)

        pygame.draw.rect(self.screen, consts.GREEN, (0, config.HEIGHT // 6 * 5 + 40, config.WIDTH, config.HEIGHT // 6 * 5))

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
