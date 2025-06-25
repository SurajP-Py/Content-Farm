# games/random_racers.py

import pygame
import random
from game_framework import Game
from games import consts
from recording import config

RACER_COUNT = 4
RACER_WIDTH = 40
RACER_HEIGHT = 40
FINISH_LINE = 50

class Racer:
    def __init__(self, index):
        self.x = config.WIDTH - 100
        self.y = config.HEIGHT * (index + 1) / 5
        self.speed = random.uniform(2, 4)
        self.color = [consts.RED, consts.YELLOW, consts.BLUE, consts.PURPLE][index]

    def update(self):
        self.x -= random.uniform(0, self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, RACER_WIDTH, RACER_HEIGHT))

    def has_finished(self):
        return self.x <= FINISH_LINE

class RandomRacers(Game):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.racers = [Racer(i) for i in range(RACER_COUNT)]
        self.winner = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        self.screen.fill("black")

        # Draw finish line
        pygame.draw.line(self.screen, consts.GREEN, (FINISH_LINE, 0), (FINISH_LINE, config.HEIGHT), 5)

        for racer in self.racers:
            if not self.done:
                racer.update()
            racer.draw(self.screen)

        if not self.winner:
            for i, racer in enumerate(self.racers):
                if racer.has_finished():
                    self.winner = i
                    self.done = True

    def draw(self):
        pass  # Already drawn in update

    def run_frame(self):
        self.handle_events(pygame.event.get())
        self.update()
        pygame.display.flip()

    def is_done(self):
        return self.done
