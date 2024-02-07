import pygame as pg

pg.init()
screen = pg.display.set_mode((1, 1))

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
# Colours
BG = (144, 201, 120)

ball_img = pg.image.load("img/playerBlock.png").convert_alpha()
