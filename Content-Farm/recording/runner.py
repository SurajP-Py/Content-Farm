# recording/runner.py

import pygame
import random
import time
import importlib
import pkgutil
from pathlib import Path
from recording import config
from recording.video import Video

def get_all_games():
    import games
    games_list = []

    # Dynamically find all modules in games folder
    package_path = Path(games.__file__).parent

    for _, modname, ispkg in pkgutil.iter_modules([str(package_path)]):
        if not ispkg:
            module = importlib.import_module(f"games.{modname}")
            # Expect each module to have a single Game class named with capitalized modname or "Game"
            # For flexibility, search for classes inheriting from base Game
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                try:
                    bases = getattr(attr, '__bases__', ())
                    # Adjust this check if you have a common base Game class to inherit from
                    if 'Game' in [base.__name__ for base in bases]:
                        games_list.append(attr)
                except Exception:
                    continue
    return games_list

def run_and_record():
    width, height = config.WIDTH, config.HEIGHT

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    video = Video((width, height))

    games = get_all_games()
    if not games:
        print("No games found in the games folder.")
        return
    
    #print(games)
    #GameClass = games[]
    GameClass = random.choice(games)

    print(f"Selected game: {GameClass.__name__}")
    game = GameClass(screen)
    game.update()
    game.draw()

    for _ in range(30 * config.START_DELAY):
        video.make_png(screen)

    running = True
    timer = 0
    max_time = config.DURATION * 1000

    while running and not game.done:
        dt = clock.tick(config.FPS)
        timer += dt

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                game.done = True

        game.handle_events(events)
        game.update()
        game.draw()
        pygame.display.flip()

        video.make_png(screen)

        if timer >= max_time or game.is_done():
            running = False

    for _ in range(30 * config.END_DELAY):
        video.make_png(screen)
    pygame.quit()

    video.make_mp4()
