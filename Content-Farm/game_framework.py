# game_framework.py

import pygame
import sys

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.done = False
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
    
    def update(self):
        pass
    
    def draw(self):
        pass
    
    def run_frame(self):
        self.handle_events(pygame.event.get())
        self.update()
        self.draw()
        pygame.display.flip()

    def is_done(self):
        return self.done
