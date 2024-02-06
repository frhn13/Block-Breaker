import pygame as pg
from Player import Player

pg.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Block Breaker")

# Set the frame rate
clock = pg.time.Clock()

running = True
player = Player(200, 200, 5, 100, 20)

while running:
    clock.tick(FPS)

    pg.draw.rect(screen, (255, 0, 0), (player.x, player.y, player.width, player.height))
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
