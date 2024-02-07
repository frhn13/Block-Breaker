import pygame as pg

from Constants import SCREEN_WIDTH, SCREEN_HEIGHT

pg.init()
screen = pg.display.set_mode((1, 1))
block_img = pg.image.load("img/Block.png").convert_alpha()


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(block_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
