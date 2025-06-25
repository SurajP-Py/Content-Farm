# games/box_fighters.py

import pygame
import random
from game_framework import Game
from games import consts
from recording import config

BOX_SIZE = 150
MAX_HP = 5

class Box:
    def __init__(self, x, y, color, side_strength):
        self.rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
        self.color = color
        self.vx = random.choice([-8, -7, -6, -5, 5, 6, 7, 8])
        self.vy = self.vx * random.choice([-1, 1])
        self.hp = MAX_HP
        self.alive = True
        self.side_strength = side_strength  # "top" or "side"

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= config.WIDTH:
            self.vx *= -1
        if self.rect.top <= 0.5 * config.WIDTH or self.rect.bottom >= 1.5 * config.WIDTH:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Health bar
        pygame.draw.rect(screen, consts.WHITE, (self.rect.x, self.rect.y - 20, BOX_SIZE, 5), 1)
        if self.alive:
            pygame.draw.rect(screen, consts.GREEN, (self.rect.x, self.rect.y - 20, BOX_SIZE * (self.hp / MAX_HP), 5))

        # Show strength direction
        if self.side_strength == "top":
            pygame.draw.polygon(screen, consts.YELLOW, [
                (self.rect.centerx, self.rect.top - 8),
                (self.rect.centerx - 5, self.rect.top - 2),
                (self.rect.centerx + 5, self.rect.top - 2)
            ])
            pygame.draw.polygon(screen, consts.YELLOW, [
                (self.rect.centerx, self.rect.bottom + 8),
                (self.rect.centerx - 5, self.rect.bottom + 2),
                (self.rect.centerx + 5, self.rect.bottom + 2)
            ])
        elif self.side_strength == "side":
            pygame.draw.polygon(screen, consts.YELLOW, [
                (self.rect.right + 6, self.rect.centery),
                (self.rect.right, self.rect.centery - 5),
                (self.rect.right, self.rect.centery + 5)
            ])
            pygame.draw.polygon(screen, consts.YELLOW, [
                (self.rect.left - 6, self.rect.centery),
                (self.rect.left, self.rect.centery - 5),
                (self.rect.left, self.rect.centery + 5)
            ])

    def take_hit(self, direction):
        if direction == "side":
            self.rect.x -= self.vx
            self.vx *= -1
        if direction == "top":
            self.rect.y -= self.vy
            self.vy *= -1
        
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def bounce(self, direction):
        if direction == "side":
            self.rect.x -= self.vx
            self.vx *= -1
        if direction == "top":
            self.rect.y -= self.vy
            self.vy *= -1

class BoxFighters(Game):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.box_a = Box(config.WIDTH / 2, 0.5 * config.WIDTH + 1, consts.RED, side_strength="top")
        self.box_b = Box(config.WIDTH / 2, 1.5 * config.WIDTH - BOX_SIZE - 1, consts.BLUE, side_strength="side")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True

    def update(self):
        if not self.box_a.alive or not self.box_b.alive:
            self.done = True
            return

        self.box_a.update()
        self.box_b.update()

        if self.box_a.rect.colliderect(self.box_b.rect):
            dx = self.box_b.rect.centerx - self.box_a.rect.centerx
            dy = self.box_b.rect.centery - self.box_a.rect.centery
            if abs(dy) > abs(dx):  # Vertical collision
                if self.box_a.side_strength == "top" and dy < BOX_SIZE:
                    self.box_b.take_hit("top")
                    self.box_a.bounce("top")
                elif self.box_b.side_strength == "top" and dy > BOX_SIZE * -1:
                    self.box_a.take_hit("top")
                    self.box_b.bounce("top")
            else:  # Horizontal collision
                if self.box_a.side_strength == "side" and dx < BOX_SIZE:
                    self.box_b.take_hit("side")
                    self.box_a.bounce("side")
                elif self.box_b.side_strength == "side" and dx > BOX_SIZE * -1:
                    self.box_a.take_hit("side")
                    self.box_b.bounce("side")

    def draw(self):
        self.screen.fill((20, 20, 20))
        pygame.draw.rect(self.screen, consts.WHITE, (0, 0.5 * config.WIDTH, config.WIDTH, config.WIDTH), 4)
        if self.box_a.alive:
            self.box_a.draw(self.screen)
        if self.box_b.alive:
            self.box_b.draw(self.screen)

    def run_frame(self):
        self.handle_events(pygame.event.get())
        self.update()
        self.draw()
        pygame.display.flip()

    def is_done(self):
        return self.done
