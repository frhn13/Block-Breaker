import pygame as pg


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
