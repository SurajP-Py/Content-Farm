# games/box_powerups.py

import pygame
import random
from game_framework import Game
from games import consts
from recording import config

BOX_SIZE = 150
MAX_HP = 4
BASE_DMG = 0
POWERUP_SIZE = 25

class PowerUp:
    def __init__(self, kind):
        self.kind = kind  # "heal" or "weapon"
        self.rect = pygame.Rect(
            random.randint(50, config.WIDTH - 50),
            random.randint(int(0.5 * config.WIDTH) + 50, int(1.5 * config.WIDTH) - 50),
            POWERUP_SIZE,
            POWERUP_SIZE
        )
        self.color = consts.GREEN if kind == "heal" else consts.YELLOW

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Box:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
        self.color = color
        self.vx = random.choice([-8, -7, -6, -5, 5, 6, 7, 8])
        self.vy = self.vx * random.choice([-1, 1])
        self.hp = MAX_HP
        self.alive = True
        self.damage = BASE_DMG
        self.power_timer = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= config.WIDTH:
            self.vx *= -1
        if self.rect.top <= 0.5 * config.WIDTH or self.rect.bottom >= 1.5 * config.WIDTH:
            self.vy *= -1

        if self.damage > BASE_DMG:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.damage = BASE_DMG

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, consts.WHITE, (self.rect.x, self.rect.y - 20, BOX_SIZE, 5), 1)
        if self.alive:
            pygame.draw.rect(screen, consts.GREEN, (self.rect.x, self.rect.y - 20, BOX_SIZE * (self.hp / MAX_HP), 5))
            if self.damage == 1:
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

    def take_hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

    def collect(self, powerup):
        if powerup.kind == "heal":
            self.hp = min(MAX_HP, self.hp + 1)
        elif powerup.kind == "weapon":
            self.damage = 1
            self.power_timer = 180  # 3 seconds at 60fps

    def remove(self):
        self.damage = 0

class BoxPowerUps(Game):
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.box_a = Box(config.WIDTH / 2 - BOX_SIZE // 2, 0.5 * config.WIDTH + 1, consts.RED)
        self.box_b = Box(config.WIDTH / 2 - BOX_SIZE // 2, 1.5 * config.WIDTH - BOX_SIZE - 1, consts.BLUE)
        self.powerups = []
        self.spawn_timer = 60

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

        # Powerup logic
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = random.randint(90, 180)
            if random.random() < 0.25:
                kind = "heal"
            else:
                kind = "weapon"
            self.powerups.append(PowerUp(kind))

        for p in self.powerups[:]:
            if self.box_a.rect.colliderect(p.rect):
                self.box_a.collect(p)
                self.powerups.remove(p)
            elif self.box_b.rect.colliderect(p.rect):
                self.box_b.collect(p)
                self.powerups.remove(p)

        # Box collision
        if self.box_a.rect.colliderect(self.box_b.rect):
            self.box_a.take_hit(self.box_b.damage)
            self.box_b.take_hit(self.box_a.damage)
            self.box_a.remove()
            self.box_b.remove()

            # Bounce
            dx = self.box_b.rect.centerx - self.box_a.rect.centerx
            dy = self.box_b.rect.centery - self.box_a.rect.centery
            if abs(dy) > abs(dx):
                self.box_a.rect.y -= self.box_a.vy
                self.box_b.rect.y -= self.box_b.vy
                self.box_a.vy *= -1
                self.box_b.vy *= -1
            else:
                self.box_a.rect.x -= self.box_a.vx
                self.box_b.rect.x -= self.box_b.vx
                self.box_a.vx *= -1
                self.box_b.vx *= -1

    def draw(self):
        self.screen.fill((20, 20, 20))
        pygame.draw.rect(self.screen, consts.WHITE, (0, 0.5 * config.WIDTH, config.WIDTH, config.WIDTH), 4)

        for p in self.powerups:
            p.draw(self.screen)

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
