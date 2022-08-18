import pygame, sys
from settings import *
from level import Level

## pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

## Create level according to level_map
level = Level(level_map, screen)

## Draw everything and update in this while loop: Game Loop
while True:
    # Event loop
    for event in pygame.event.get():

        # Enabling user to exit from the game
        if event.type == pygame.QUIT:
            pygame.quit() # this uninitalizes everything which was initialized with 'pygame.init()'
            sys.exit() # exit Enabling user to exit from the game will exit the whole program

    screen.fill('black')

    level.run()

    pygame.display.update()
    clock.tick(fps) #This tells python that this while loop should not run more than 'fps' (= 60 in this case) times in one second. Thefore sets the ceil value for framerate.